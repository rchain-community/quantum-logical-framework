#!/usr/bin/env python3
"""game_log_analysis.py — score a recorded live game against its pre-registered predictions.

Reads the structured records the QuantumOS `observer` agent writes
(`<state>/rooms/<room>/games/<ts>-<label>.json`, schema `qos-game/1`; see quantum-os
`scripts/qos-cli/game-log.mjs`) and reports, per game:

  * the game as pre-registered: payoffs (a,b,c,d) = (u(S|S), u(S|H), u(H|S), u(H|H)), the
    payoff-dominant and risk-dominant options, and Young's basin threshold
    p* = (d − b) / ((a − c) + (d − b)) — the share of Stag players above which Stag is the
    best reply (Game_Theory_QLF.md §3; QLF_PotentialGames.risk_dominance_is_potential_order);
  * every closed poll: which option is Stag/Hare (from `stag=`/`hare=` in the start command, else
    a keyword heuristic), the Stag share raw and trust-weighted, the majority, and whether the
    poll came before or after the first commitment (`/lemma`);
  * the three predictions pre-registered on quantum-os #137, each held / killed / not testable:
      P1  without a commitment round the room converges on the safe convention;
      P2  a commitment round flips it (the KMR step-function — a device works iff it moves p*
          across ½ — needs the device's payoff effect stated; the record shows flip / no flip);
      P3  scoring by the shared objective selects the ambitious option (a poll whose question
          names welfare / collective / shared value).

    python3 game_log_analysis.py path/to/game.json [more.json ...] [--json]

Everything here is read off the record; nothing is fitted. A "not testable" verdict means the
record does not contain the round the prediction is about.
"""
import argparse
import json
import re
import sys

STAG_WORDS = re.compile(r"stag|ambitious|cooperat|commit|all-in|big", re.I)
HARE_WORDS = re.compile(r"hare|safe|defect|cautious|small|solo", re.I)


def classify_game(p):
    a, b, c, d = p["a"], p["b"], p["c"], p["d"]
    coord = a > c and d > b
    pd = "S" if a > d else ("H" if d > a else "tie")
    rd = "S" if (a - c) > (d - b) else ("H" if (d - b) > (a - c) else "tie")
    den = (a - c) + (d - b)
    pstar = (d - b) / den if den else None
    return {"coordination": coord, "payoff_dominant": pd, "risk_dominant": rd, "p_star": pstar}


def option_role(text, spec):
    t = (text or "").lower()
    if spec.get("stag") and spec["stag"].lower() in t:
        return "S"
    if spec.get("hare") and spec["hare"].lower() in t:
        return "H"
    if STAG_WORDS.search(t) and not HARE_WORDS.search(t):
        return "S"
    if HARE_WORDS.search(t) and not STAG_WORDS.search(t):
        return "H"
    return None


def stag_share(poll, spec, weighted=False):
    """Share of ballots (latest per peer) that approve / rank first a Stag option."""
    roles = {o["id"]: option_role(o.get("text"), spec) for o in poll.get("options", [])}
    weights = poll.get("tally", {}).get("weights") if weighted else None
    tot = s = 0.0
    for peer, choices in (poll.get("finalBallots") or {}).items():
        w = (weights or {}).get(peer, 1) if weighted else 1
        if not choices:
            continue
        first = choices[0] if poll.get("method") == "ranked" else None
        picked = [first] if first else choices
        if any(roles.get(cid) == "S" for cid in picked):
            s += w
        tot += w
    return (s / tot if tot else None), int(tot if not weighted else round(tot))


def analyze(rec):
    spec = rec.get("spec") or {}
    out = {"label": rec.get("label"), "room": rec.get("room"), "events": rec.get("events"),
           "participants": len(rec.get("participants") or {}), "predictions": spec.get("predictions") or []}
    game = classify_game(spec["payoffs"]) if spec.get("payoffs") else None
    out["game"] = game
    lemmas = sorted(rec.get("lemmas") or [], key=lambda l: l.get("t") or "")
    first_commit = lemmas[0]["t"] if lemmas else None
    rounds = []
    for p in sorted(rec.get("polls") or [], key=lambda p: p.get("openedT") or ""):
        if not p.get("closedT"):
            continue
        share, n = stag_share(p, spec)
        wshare, _ = stag_share(p, spec, weighted=True) if p.get("tally", {}).get("weighted") else (None, None)
        q = (p.get("question") or "")
        rounds.append({
            "id": p.get("id"), "question": q, "closedT": p.get("closedT"), "ballots": n,
            "stag_share": share, "stag_share_weighted": wshare,
            "majority": (None if share is None else ("S" if share > 0.5 else ("H" if share < 0.5 else "tie"))),
            "after_commitment": bool(first_commit and (p.get("openedT") or "") > first_commit),
            "welfare_round": bool(re.search(r"welfare|collective|shared|total|everyone", q, re.I)),
            "winner_text": (p.get("tally") or {}).get("winners"),
        })
    out["rounds"] = rounds
    out["commitments"] = [{"t": l.get("t"), "who": l.get("who"), "name": l.get("name"), "text": l.get("text")} for l in lemmas]

    verdicts = {}
    pre = [r for r in rounds if not r["after_commitment"] and not r["welfare_round"] and r["majority"]]
    post = [r for r in rounds if r["after_commitment"] and not r["welfare_round"] and r["majority"]]
    wel = [r for r in rounds if r["welfare_round"] and r["majority"]]
    if game and game["coordination"] and game["risk_dominant"] != game["payoff_dominant"]:
        safe = game["risk_dominant"]
        if pre:
            verdicts["P1 cold -> safe convention"] = "held" if pre[-1]["majority"] == safe else "killed"
        else:
            verdicts["P1 cold -> safe convention"] = "not testable (no pre-commitment round)"
        if pre and post:
            flipped = pre[-1]["majority"] != post[-1]["majority"] and post[-1]["majority"] == game["payoff_dominant"]
            verdicts["P2 commitment flips it"] = ("flip observed" if flipped else "no flip") + \
                " — the iff-crosses-1/2 part needs the device's payoff effect stated in the pre-registration"
        else:
            verdicts["P2 commitment flips it"] = "not testable (needs a round before and after a /lemma commitment)"
        if wel:
            verdicts["P3 shared-objective scoring -> ambitious"] = "held" if wel[-1]["majority"] == game["payoff_dominant"] else "killed"
        else:
            verdicts["P3 shared-objective scoring -> ambitious"] = "not testable (no welfare-scored round)"
    elif game:
        verdicts["game"] = "not a Stag Hunt as pre-registered (risk- and payoff-dominant coincide or no coordination): P1–P3 do not apply"
    else:
        verdicts["game"] = "no payoffs in the pre-registration: only the descriptive rounds above"
    out["verdicts"] = verdicts
    return out


def report(a):
    print(f"=== {a['label']}  (room {a['room']}, {a['events']} events, {a['participants']} participants)")
    g = a["game"]
    if g:
        ps = f"{g['p_star']:.2f}" if g["p_star"] is not None else "n/a"
        print(f"  pre-registered game: payoff-dominant {g['payoff_dominant']}, risk-dominant {g['risk_dominant']}, "
              f"p* = {ps}{'' if g['coordination'] else '  (NOT a coordination game)'}")
    for i, p in enumerate(a["predictions"], 1):
        print(f"  prediction ({i}): {p}")
    if a["commitments"]:
        print(f"  commitments: " + "; ".join(f"{c['t']} {c['who']}: {c['name']}" + (f" — {c['text']}" if c.get('text') else "") for c in a["commitments"]))
    for r in a["rounds"]:
        sh = "n/a" if r["stag_share"] is None else f"{r['stag_share']:.2f}"
        w = "" if r["stag_share_weighted"] is None else f", weighted {r['stag_share_weighted']:.2f}"
        tag = " [after commitment]" if r["after_commitment"] else ""
        tag += " [welfare-scored]" if r["welfare_round"] else ""
        print(f"  round {r['id']}: \"{r['question'][:60]}\" — {r['ballots']} ballots, Stag share {sh}{w}, majority {r['majority']}{tag}")
    for k, v in a["verdicts"].items():
        print(f"  {k}: {v}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("records", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = []
    for path in args.records:
        with open(path, encoding="utf-8") as f:
            rec = json.load(f)
        if rec.get("schema") != "qos-game/1":
            print(f"{path}: not a qos-game/1 record", file=sys.stderr)
            continue
        a = analyze(rec)
        results.append(a)
        if not args.json:
            report(a)
    if args.json:
        json.dump(results, sys.stdout, indent=2)
        print()


if __name__ == "__main__":
    main()
