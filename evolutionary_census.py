#!/usr/bin/env python3
"""evolutionary_census.py — evolutionary game theory on the closure census (quantum-os #209).

Step 1–3 of the plan posted on rchain-community/quantum-os#209: the strategy representation,
the pairwise match primitive, and the payoff→multiplicity mapping with its R6a check — run
BEFORE any population dynamics, because the mapping decides whether the test can fail at all.

Representation.  A strategy is a preparation strand: an open twist history over the six spatial
twists (the pattern contextual_census.py uses for preparations).  A match between strategies
`a` and `b` at horizon `t` is MultiParticle.search_for_entanglement's inner loop: each side
extends by `t` twists and the pair closes when the joint history achieves ZFA
(`twist_core.is_zfa` on `a + ca + b + cb` — the gate is the full ZFA predicate, per
QucalcSearch.md's gotcha, not the aggregate).

Two candidate payoff maps, both read off the census with no free parameter:

  P_joint(a,b) = #{(ca,cb) : is_zfa(a+ca+b+cb)}      the number of ways the PAIR closes
  P_own(a|b)   = #{ca : ∃cb, is_zfa(a+ca+b+cb)}      the number of a's own ways that b closes

R6a check on P_joint.  Joint ZFA is count balance of the concatenation (count balance ⟹ Pauli
closure, `count_balanced_pauli_closed`), and count balance is order-blind, so
P_joint(a,b) = P_joint(b,a): both players always receive the same number.  A symmetric
common-payoff 2×2 game is a potential game, and in a potential game the risk-dominant and the
payoff-dominant equilibrium coincide (both maximise the potential).  So under P_joint the
pre-registered test "does most-ways-first pick the risk-dominant equilibrium" cannot fail — it is
bookkeeping (Philosophy.md §3a rule 4).  Verified numerically below, then set aside.

P_own is not symmetric — b may close many of a's ways while a closes few of b's — so it can
produce coordination games in which risk dominance and payoff dominance DISAGREE: the Stag Hunt
proper.  That is where the population dynamics (steps 4–6) have content, and where the two
readings of "most ways happens first" part company:

  H_naive  the state with the larger diagonal multiplicity (payoff-dominant) is selected;
  H_KMR    the risk-dominant state is selected (Kandori–Mailath–Rob 1993, Young 1993 — the
           state reached by the most mutation paths, i.e. most ways to ARRIVE, not most ways AT).

Pre-registered kill condition for H_naive (to be run in step 4): the risk-dominant equilibrium is
the stochastically stable state on a majority of the Stag-Hunt-type seed pairs found here.

RESULT (recorded, not tuned around — ScientificApproach.md R2a).  At horizons 2 and 3:

  * P_joint is symmetric on every pair (as derived), and so is P_own — 0 of 861 seed pairs differ.
    The reason is general: with free same-length continuations on both sides, whether a's
    continuation is closable depends only on imb(a) + imb(b), a symmetric quantity.  So EVERY
    payoff built from joint ZFA of free continuations is a potential game: 216 coordination games,
    risk == payoff dominance in all 216, Stag-Hunt-type pairs: 0.
  * Making the strategy a behavioural rule (`--alphabets`: the move set a player is willing to
    twist — Y, X, Z, XY, YZ, XZ, XYZ) does make P_own asymmetric (u(Y|XYZ)=4 vs u(XYZ|Y)=8), but
    still yields 0 Stag-Hunt-type games: "own ways closed by the partner" is monotone in move-set
    inclusion, so the larger move set is simply dominant.  A Stag Hunt needs the ambitious
    strategy to be VULNERABLE when unmatched (u(S|H) < u(H|H)); free closure counting never
    punishes ambition, because a bigger alphabet closes more against everyone.

Consequence.  With fitness = closure multiplicity the evolutionary game is a potential game, and
for potential games the stochastically stable state IS the potential maximiser by theorem
(Blume 1993; Young 1993) — "most ways happens first" holds exactly, but as bookkeeping: no
distribution over ways could make it false, so steps 4–6 (Moran + mutation) would have no
content.  A discriminating test needs a payoff that breaks the potential structure — a cost of
holding a deep strand open (the free-action ledger, QLF_FreeEnergy) or an order-/capacity-
asymmetric closure — which is a modelling decision to make openly, not to fit here.

    python3 evolutionary_census.py               # seeds of length ≤ 2, horizon 2
    python3 evolutionary_census.py --t 3         # horizon 3 (slower)
    python3 evolutionary_census.py --alphabets   # strategies as move sets, horizons 2 and 3
"""
import argparse
import itertools
import sys
import time
from collections import Counter

sys.path.insert(0, ".")
from twist_core import is_zfa

SPATIAL = ['^', 'v', '<', '>', '/', '\\']
PAIRS = (('^', 'v'), ('>', '<'), ('/', '\\'), ('+', '-'))


def count_balanced(h: str) -> bool:
    c = Counter(h)
    return all(c[a] == c[b] for a, b in PAIRS)


def continuations(t: int):
    return [''.join(p) for p in itertools.product(SPATIAL, repeat=t)]


def match(a: str, b: str, t: int, conts):
    """Return (P_joint(a,b), P_own(a|b), P_own(b|a)) at horizon t."""
    joint = 0
    own_a = set()
    own_b = set()
    for ca in conts:
        pa = a + ca
        for cb in conts:
            h = pa + b + cb
            # count balance is the cheap necessary condition; the gate is still the full is_zfa
            if count_balanced(h) and is_zfa(h):
                joint += 1
                own_a.add(ca)
                own_b.add(cb)
    return joint, len(own_a), len(own_b)


def classify(u_xx, u_xy, u_yx, u_yy):
    """2×2 symmetric game with row payoffs u(p|q): p's payoff against q.

    coordination: each strategy is a strict best reply to itself.
    payoff-dominant: the diagonal with the larger payoff.
    risk-dominant (Harsanyi–Selten, symmetric case): x iff (u_xx − u_yx) > (u_yy − u_xy).
    """
    coord = u_xx > u_yx and u_yy > u_xy
    if not coord:
        return None
    pd = 'x' if u_xx > u_yy else ('y' if u_yy > u_xx else 'tie')
    dx, dy = u_xx - u_yx, u_yy - u_xy
    rd = 'x' if dx > dy else ('y' if dy > dx else 'tie')
    return pd, rd


ALPHABETS = {
    'Y': ['^', 'v'], 'X': ['<', '>'], 'Z': ['/', '\\'],
    'XY': ['^', 'v', '<', '>'], 'YZ': ['^', 'v', '/', '\\'], 'XZ': ['<', '>', '/', '\\'],
    'XYZ': ['^', 'v', '<', '>', '/', '\\'],
}


def match_alphabets(A: str, B: str, t: int):
    """Strategies as move sets: P_own(A|B) counts A's continuations (over A's alphabet) that some
    continuation of B (over B's alphabet) closes."""
    ca_ok, cb_ok, joint = set(), set(), 0
    conts_a = [''.join(p) for p in itertools.product(ALPHABETS[A], repeat=t)]
    conts_b = [''.join(p) for p in itertools.product(ALPHABETS[B], repeat=t)]
    for ca in conts_a:
        for cb in conts_b:
            h = ca + cb
            if count_balanced(h) and is_zfa(h):
                joint += 1
                ca_ok.add(ca)
                cb_ok.add(cb)
    return joint, len(ca_ok), len(cb_ok)


def alphabet_scan():
    names = list(ALPHABETS)
    for t in (2, 3):
        own = {}
        for A in names:
            own[(A, A)] = match_alphabets(A, A, t)[1]
        for A, B in itertools.combinations(names, 2):
            _, oa, ob = match_alphabets(A, B, t)
            own[(A, B)], own[(B, A)] = oa, ob
        print(f"\n== strategies as move sets, horizon t={t}: P_own(A|B) ==")
        print("       " + "".join(f"{n:>6}" for n in names))
        for A in names:
            print(f"{A:>6} " + "".join(f"{own[(A, B)]:6d}" for B in names))
        sh, coord, agree = [], 0, 0
        for x, y in itertools.combinations(names, 2):
            c = classify(own[(x, x)], own[(x, y)], own[(y, x)], own[(y, y)])
            if c:
                coord += 1
                if c[0] == c[1]:
                    agree += 1
                elif 'tie' not in c:
                    sh.append((x, y, c))
        print(f"coordination games: {coord}   risk==payoff: {agree}   STAG-HUNT-TYPE: {len(sh)} {sh}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=2, help='horizon: continuation length per side')
    ap.add_argument('--maxseed', type=int, default=2, help='max seed length')
    ap.add_argument('--alphabets', action='store_true', help='strategies as move sets (see docstring)')
    args = ap.parse_args()
    if args.alphabets:
        alphabet_scan()
        return

    seeds = [''.join(p) for L in range(1, args.maxseed + 1)
             for p in itertools.product(SPATIAL, repeat=L)]
    conts = continuations(args.t)
    print(f"seeds: {len(seeds)} (length ≤ {args.maxseed}), continuations per side: {len(conts)} "
          f"(horizon {args.t}), joint pairs per match: {len(conts)**2}")

    t0 = time.time()
    # self-matches and cross-matches, cached; P_own is asymmetric so store both orders
    joint = {}
    own = {}
    for a in seeds:
        j, oa, _ = match(a, a, args.t, conts)
        joint[(a, a)] = j
        own[(a, a)] = oa
    for a, b in itertools.combinations(seeds, 2):
        j, oa, ob = match(a, b, args.t, conts)
        joint[(a, b)] = j
        joint[(b, a)] = j
        own[(a, b)] = oa      # a's ways closed by b
        own[(b, a)] = ob      # b's ways closed by a
    print(f"census done in {time.time() - t0:.1f}s")

    # ---- R6a on P_joint: symmetric ⟹ risk dominance ≡ payoff dominance ----
    print("\n=== R6a: P_joint (ways the PAIR closes) ===")
    import random
    random.seed(0)
    sample = random.sample(list(itertools.combinations(seeds, 2)), min(120, len(seeds) * (len(seeds) - 1) // 2))
    asym = sum(1 for a, b in sample if joint[(a, b)] != match(b, a, args.t, conts)[0])
    print(f"P_joint(a,b) != P_joint(b,a) on {asym} of {len(sample)} sampled pairs "
          f"(expected 0: joint ZFA is count balance, order-blind)")
    n_coord = n_agree = 0
    for x, y in itertools.combinations(seeds, 2):
        c = classify(joint[(x, x)], joint[(x, y)], joint[(y, x)], joint[(y, y)])
        if c:
            n_coord += 1
            if c[0] == c[1]:
                n_agree += 1
    print(f"coordination games under P_joint: {n_coord}; risk-dominant == payoff-dominant in "
          f"{n_agree} of them  (expected all: a symmetric common-payoff game is a potential game)")
    print("=> under P_joint the KMR test cannot fail: bookkeeping, set aside.")

    # ---- P_own: the asymmetric map ----
    print("\n=== P_own (a's OWN ways closed by b) ===")
    n_coord = 0
    stag_hunt = []
    agree = 0
    for x, y in itertools.combinations(seeds, 2):
        u_xx, u_xy, u_yx, u_yy = own[(x, x)], own[(x, y)], own[(y, x)], own[(y, y)]
        c = classify(u_xx, u_xy, u_yx, u_yy)
        if not c:
            continue
        n_coord += 1
        pd, rd = c
        if pd == rd:
            agree += 1
        elif 'tie' not in (pd, rd):
            stag_hunt.append((x, y, (u_xx, u_xy, u_yx, u_yy), pd, rd))
    print(f"seed pairs: {len(seeds) * (len(seeds) - 1) // 2}   coordination games: {n_coord}   "
          f"risk==payoff: {agree}   STAG-HUNT-TYPE (risk != payoff, no tie): {len(stag_hunt)}")
    for x, y, u, pd, rd in stag_hunt[:20]:
        print(f"  {x!r:6} vs {y!r:6}  u(x|x)={u[0]:3d} u(x|y)={u[1]:3d} u(y|x)={u[2]:3d} u(y|y)={u[3]:3d}"
              f"   payoff-dominant={pd}  risk-dominant={rd}")
    if len(stag_hunt) > 20:
        print(f"  ... {len(stag_hunt) - 20} more")
    if stag_hunt:
        print("\nPre-registered for step 4 (Moran process with vanishing mutation on these pairs):")
        print("  H_naive: payoff-dominant state selected;  H_KMR: risk-dominant state selected.")
        print("  Kill condition for H_naive: risk-dominant wins on a majority of the pairs above.")
    else:
        print("\nNo Stag-Hunt-type pair at this horizon: the census game is a pure potential game "
              "here and steps 4–6 would have no content. Try a larger --t before concluding.")


if __name__ == "__main__":
    main()
