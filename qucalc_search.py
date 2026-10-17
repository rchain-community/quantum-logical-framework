#!/usr/bin/env python3
"""
qucalc_search.py — the "what closes next" query service over `twist_core`.

Given a QuCalc position (a twist history `qc`), enumerate the admissible
**continuations** — the twist words you can append so that the whole thing is a
ZFA closure (count-balanced ∧ Pauli-closed). Shortest continuations first.

This is a *query*, not a stored layer: nothing is cached, nothing is written,
the answer is always current with `twist_core.py`. The census inventory
(`census_inventory.py`) stores per-stratum summaries; this streams the actual
histories reachable from one point.

Why no precompute / no on-disk index: a depth-6 continuation search is ~260k
candidates (count-prefiltered to a few thousand before the Pauli fold ever
runs), which is a few seconds even on a slow machine and sub-second elsewhere —
cheaper than reading a ~1 MB cache entry back over a slow mount. See the
`--time` mode for the numbers on the current host.

    # CLI — print closures reachable from "^<v>+-" within 6 appended twists
    python3 qucalc_search.py "^<v>+-" --max-depth 6

    # CLI — just the count, and as NDJSON
    python3 qucalc_search.py "^<v>+-" --max-depth 6 --count-only
    python3 qucalc_search.py "^<v>+-" --max-depth 6 --json

    # the one closure the substrate takes from a position (least free action)
    python3 qucalc_search.py "^^<" --solve

    # HTTP endpoint — streams NDJSON, one closure per line, flushed as found
    python3 qucalc_search.py --serve --port 8765
    curl -N 'http://127.0.0.1:8765/search?qc=%5E%3Cv%3E%2B-&max_depth=6&limit=10000'

    # exposed for quantum-os / other research ops: bind all interfaces, set the
    # per-deployment ceiling and the concurrent-search cap for the host's RAM
    python3 qucalc_search.py --serve --host 0.0.0.0 --port 8765 \
            --max-depth-cap 7 --max-concurrent 2

HTTP contract (stable; consumers such as quantum-os depend on it):

    GET /                 -> {service, version, usage, alphabet, caps}
    GET /health           -> {ok: true}
    GET /search?qc=<hist>&max_depth=<int>&limit=<int>
        200 application/x-ndjson, streamed:
          line 1        {"_meta": true, "qc", "max_depth", "limit", "version"}
                        (params after clamping to the deployment caps)
          lines 2..k    {"cont", "history", "len", "depth", "phase"}
                        one ZFA closure each, shortest `depth` first;
                        `phase` is the Pauli scalar the whole history folds to
                        ({"+1","-1","+i","-i"}, per QLF_PhaseRule)
          last line     {"_done": true, "found": k, "elapsed_s": F,
                         "truncated": <hit limit?>}
        400  {"error": "..."}   bad qc / non-integer params
        429  {"error": "..."}   host at --max-concurrent, try later
    GET /solve?qc=<hist>&max_depth=<int>   (comma-separated qc is concatenated)
        200 application/json, one answer:
          {"solved": true,  "cont", "history", "depth", "phase",
           "peak_excursion", "arrangements", "considered", "version"}
          {"solved": false, "residual": [v,h,d,l], "floor_depth", "reason",
           "completion", "version"}
        the one closure the substrate takes — least free action, by the cascade
          least peak excursion -> shortest -> phase +1 -> lexicographic
        (deterministic, so independent callers agree). See `solve()`.

CORS: `Access-Control-Allow-Origin: *` on every response; `OPTIONS` preflight
answered. The service is read-only and stateless — nothing is written, no
history is retained between requests.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
import threading
import time
from collections import Counter
from typing import Iterator, Optional

from twist_core import (
    TWISTS,
    MIN_ZFA_LENGTH,
    calculate_action,
    pauli_fold,
    validate_history,
)

VERSION = "1.0"

# Guard rails. The HTTP endpoint clamps requests to these; the CLI does not
# (you asked for it explicitly there). `--serve` can tighten the depth cap and
# set the concurrent-search limit per host — depth 8 is ~minutes on a small box.
MAX_DEPTH_CAP = 7            # 8^7 ≈ 2.1M raw candidates, count-prefiltered
MAX_LIMIT_CAP = 100_000
DEFAULT_MAX_DEPTH = 6
DEFAULT_LIMIT = 10_000
DEFAULT_MAX_CONCURRENT = 3   # simultaneous /search enumerations
SOLVE_CONSIDER = 5_000      # /solve caps the event set it ranks (winner is shallow)

_PAULI_TOL = 1e-9


# --------------------------------------------------------------------------- #
# core search
# --------------------------------------------------------------------------- #
def _classify_phase(fold) -> Optional[str]:
    """Return '+1' / '-1' / '+i' / '-i' if `fold` is a Pauli scalar, else None."""
    a, b, c, d = fold
    if abs(b) > _PAULI_TOL or abs(c) > _PAULI_TOL or abs(a - d) > _PAULI_TOL:
        return None
    for scalar, name in ((1 + 0j, "+1"), (-1 + 0j, "-1"), (1j, "+i"), (-1j, "-i")):
        if abs(a - scalar) < _PAULI_TOL:
            return name
    return None


def _action_of(combo: tuple[str, ...]) -> tuple[int, int, int, int]:
    """Signed action vector (v, h, d, l) of a tuple of twist chars — no string build."""
    c = Counter(combo)
    return (c["^"] - c["v"], c[">"] - c["<"], c["/"] - c["\\"], c["+"] - c["-"])


def _feasible(need: tuple[int, int, int, int], depth: int) -> bool:
    """Can `depth` appended twists realise the action vector `need` at all?

    Each axis needs `#pos + #neg` twists with `#pos - #neg = need_i`, so
    `#axis_i ≥ |need_i|` and `#axis_i ≡ need_i (mod 2)`. Summing:
    `depth ≥ Σ|need_i|` and `depth ≡ Σ|need_i| (mod 2)`.
    """
    s = sum(abs(x) for x in need)
    return depth >= s and (depth - s) % 2 == 0


def search(
    qc: str,
    max_depth: int = DEFAULT_MAX_DEPTH,
    limit: Optional[int] = DEFAULT_LIMIT,
    min_total_len: int = MIN_ZFA_LENGTH,
    absorbing: bool = False,
) -> Iterator[dict]:
    """Yield ZFA closures reachable from `qc` by appending 1..`max_depth` twists.

    Shortest continuations first. Each result is a dict with keys
    `cont`, `history`, `len`, `depth`, `phase`. If the `limit` is reached the
    generator stops without a marker — callers that need to know should compare
    the count to `limit`.

    **possibilities vs events** (`absorbing`):

    * `absorbing=False` (default) — the **possibilities**: *every* closure within
      `max_depth`, including continuations whose own prefix already closed.
    * `absorbing=True` — the **events**: a closure *is* an event, so a branch is
      not extended past its first closure. The continuations are prefix-free —
      each is the *first* way that branch closes — which is the absorbing census
      of `contextual_census.py --first-closure` and the `closures` layer of
      `census_inventory.py`.

    The count-balance constraint is applied to the continuation *before* any
    string is built or Pauli fold is run — the fold only touches the small
    fraction of candidates that already balance.
    """
    validate_history(qc)
    seed_action = calculate_action(qc)
    need = tuple(-x for x in seed_action)          # continuation must supply this
    n_found = 0
    closed_prefixes: set[str] = set()              # continuations that already closed

    for depth in range(1, max_depth + 1):
        if not _feasible(need, depth):
            continue
        if len(qc) + depth < min_total_len:
            continue
        for combo in itertools.product(TWISTS, repeat=depth):
            if _action_of(combo) != need:
                continue
            cont = "".join(combo)
            if absorbing and any(cont[:k] in closed_prefixes
                                 for k in range(max(1, min_total_len - len(qc)), depth)):
                continue                            # a shorter prefix already closed
            history = qc + cont
            phase = _classify_phase(pauli_fold(history))
            if phase is None:                      # count-balanced but not Pauli-closed
                continue
            if absorbing:
                closed_prefixes.add(cont)
            yield {
                "cont": cont,
                "history": history,
                "len": len(history),
                "depth": depth,
                "phase": phase,
            }
            n_found += 1
            if limit is not None and n_found >= limit:
                return


# --------------------------------------------------------------------------- #
# listeners — one enumeration, several rollups reporting in parallel
# --------------------------------------------------------------------------- #
def max_excursion(history: str) -> int:
    """Max over prefixes of the total free action `|v|+|h|+|d|+|l|` — how far the
    walk strays from ZFA balance. A capacity-`R` listener hears a closure iff this
    is `≤ R` (`QLF_ClosureDepthLaw.closedAtHorizon_iff_maxExcursion_le`)."""
    v = h = d = l = 0
    m = 0
    for t in history:
        if t == "^": v += 1
        elif t == "v": v -= 1
        elif t == ">": h += 1
        elif t == "<": h -= 1
        elif t == "/": d += 1
        elif t == "\\": d -= 1
        elif t == "+": l += 1
        elif t == "-": l -= 1
        e = abs(v) + abs(h) + abs(d) + abs(l)
        if e > m:
            m = e
    return m


class Listener:
    """Consumes the closure stream once, reports a rollup. `feed` must be cheap —
    it runs per closure, inside the enumeration."""
    name = "listener"

    def feed(self, rec: dict) -> None: ...
    def report(self) -> dict: ...


class _Count(Listener):
    name = "count"

    def __init__(self) -> None:
        self.n = 0

    def feed(self, rec):
        self.n += 1

    def report(self):
        return {"total": self.n}


class _Phase(Listener):
    name = "phase"

    def __init__(self) -> None:
        self.c = {"+1": 0, "-1": 0, "+i": 0, "-i": 0}

    def feed(self, rec):
        self.c[rec["phase"]] += 1

    def report(self):
        return dict(self.c)


class _Depth(Listener):
    name = "depth"

    def __init__(self) -> None:
        self.c: dict[int, int] = {}

    def feed(self, rec):
        d = rec["depth"]
        self.c[d] = self.c.get(d, 0) + 1

    def report(self):
        return {str(k): self.c[k] for k in sorted(self.c)}


class _Capacity(Listener):
    """The QLF *listening*: how many closures a capacity-`R` horizon receives."""

    def __init__(self, r: int) -> None:
        self.r = r
        self.name = f"capacity:{r}"
        self.heard = 0
        self.missed = 0

    def feed(self, rec):
        if max_excursion(rec["history"]) <= self.r:
            self.heard += 1
        else:
            self.missed += 1

    def report(self):
        return {"R": self.r, "heard": self.heard, "missed": self.missed}


class _Head(Listener):
    name = "head"

    def __init__(self, n: int) -> None:
        self.n = n
        self.items: list[str] = []

    def feed(self, rec):
        if len(self.items) < self.n:
            self.items.append(rec["cont"])

    def report(self):
        return {"n": self.n, "conts": self.items}


def parse_listeners(spec: str) -> list[Listener]:
    """`"phase,depth,capacity:2,capacity:3,head:20"` → listener objects.
    `count` is always included."""
    out: list[Listener] = [_Count()]
    for tok in (spec or "").split(","):
        tok = tok.strip()
        if not tok:
            continue
        kind, _, arg = tok.partition(":")
        if kind == "phase":
            out.append(_Phase())
        elif kind == "depth":
            out.append(_Depth())
        elif kind == "capacity":
            out.append(_Capacity(max(0, int(arg or 0))))
        elif kind == "head":
            out.append(_Head(max(1, int(arg or 10))))
        elif kind == "count":
            pass  # already added
        else:
            raise ValueError(f"unknown listener {tok!r} "
                             f"(phase|depth|capacity:R|head:N)")
    return out


def run_search(
    seeds: list[str],
    max_depth: int,
    limit: Optional[int],
    listeners: list[Listener],
    on_closure=None,
    absorbing: bool = False,
) -> dict:
    """Run `search` over one or more seeds, feeding every listener and calling
    `on_closure(rec)` per result if given. Returns the assembled report.

    `limit` is the total across all seeds. Multiple seeds run in sequence (the
    host this is built for cannot parallelise usefully); the listeners aggregate
    across all of them, which is the "concurrent search, one set of listeners"
    shape. `absorbing` switches possibilities → events (see `search`).
    """
    t0 = time.time()
    n = 0
    per_seed: dict[str, int] = {}
    for qc in seeds:
        seed_n = 0
        remaining = None if limit is None else max(0, limit - n)
        if remaining == 0:
            break
        for rec in search(qc, max_depth=max_depth, limit=remaining, absorbing=absorbing):
            rec = dict(rec, qc=qc) if len(seeds) > 1 else rec
            for L in listeners:
                L.feed(rec)
            if on_closure is not None:
                on_closure(rec)
            n += 1
            seed_n += 1
        per_seed[qc] = seed_n
    rep = {L.name: L.report() for L in listeners}
    return {
        "seeds": seeds,
        "max_depth": max_depth,
        "mode": "events" if absorbing else "possibilities",
        "found": n,
        "truncated": limit is not None and n >= limit,
        "elapsed_s": round(time.time() - t0, 3),
        "per_seed": per_seed if len(seeds) > 1 else None,
        "listeners": rep,
    }


# --------------------------------------------------------------------------- #
# solve — the complement of search: the one closure the substrate takes
# --------------------------------------------------------------------------- #
_PHASE_RANK = {"+1": 0, "-1": 1, "+i": 2, "-i": 3}


def _residual_to_twists(r: list[int]) -> str:
    """One concrete continuation supplying exactly the residual action vector —
    count-balances the position (its twists may not fold to a Pauli scalar in
    that order). Mirrors quantum-os `residualToTwists`."""
    axes = (("^", "v"), (">", "<"), ("/", "\\"), ("+", "-"))
    return "".join((axes[i][0] if r[i] >= 0 else axes[i][1]) * abs(r[i]) for i in range(4))


def solve(qc: str, max_depth: int = MAX_DEPTH_CAP,
          min_total_len: int = MIN_ZFA_LENGTH) -> dict:
    """Pick the one closure the substrate takes from `qc` — **least free
    action** — or report the residual a completion still owes.

    Deterministic cascade, so independent callers agree without coordinating:

        least peak excursion  →  shortest depth  →  phase +1  →  lexicographic

    "Least peak excursion" is least free action: the shallowest-horizon closure
    is the one reached first (`closedAtHorizon_mono`), which is ZFA selection
    applied to pick a representative. It is not the depth reached the most ways
    (`depth_one_not_modal`; MostWays_First.md). `absorbing` is implied — the events, not every possibility.

    Depth strategy: the natural closure depths are `floor` and `floor + 2`
    (parity), `floor = Σ|residual|`; search there first, only pay for the full
    `max_depth` sweep if that misses.
    """
    validate_history(qc)
    t0 = time.time()
    max_depth = max(1, min(max_depth, MAX_DEPTH_CAP))
    seed_action = calculate_action(qc)
    residual = [-x for x in seed_action]
    floor = sum(abs(x) for x in residual)

    if seed_action == (0, 0, 0, 0) and len(qc) >= min_total_len:
        phase = _classify_phase(pauli_fold(qc))
        if phase is not None:
            n = len(qc)
            return {
                "solved": True, "qc": qc, "already_closed": True,
                "cont": "", "history": qc, "depth": 0, "phase": phase,
                "peak_excursion": max_excursion(qc),
                "arrangements": math.comb(n, n // 2),
                "considered": 0, "searched_depth": 0,
                "elapsed_s": round(time.time() - t0, 3), "version": VERSION,
            }

    first = min(max(floor + 2, 2), max_depth)
    tries = [first, max_depth] if first < max_depth else [max_depth]
    events: list[dict] = []
    searched = 0
    for w in tries:
        searched = w
        events = list(search(qc, max_depth=w, limit=SOLVE_CONSIDER,
                             min_total_len=min_total_len, absorbing=True))
        if events:
            break

    if not events:
        completion = _residual_to_twists(residual)
        return {
            "solved": False, "qc": qc, "residual": residual, "floor_depth": floor,
            "searched_depth": searched,
            "reason": "beyond max_depth" if floor > searched else "no short event",
            "completion": completion or None,
            "elapsed_s": round(time.time() - t0, 3), "version": VERSION,
        }

    events.sort(key=lambda r: (max_excursion(r["history"]), r["depth"],
                               _PHASE_RANK[r["phase"]], r["history"]))
    best = events[0]
    bn = best["len"]
    return {
        "solved": True, "qc": qc,
        "cont": best["cont"], "history": best["history"],
        "depth": best["depth"], "phase": best["phase"],
        "peak_excursion": max_excursion(best["history"]),
        "arrangements": math.comb(bn, bn // 2),
        "considered": len(events),
        "truncated": len(events) >= SOLVE_CONSIDER,
        "searched_depth": searched,
        "elapsed_s": round(time.time() - t0, 3), "version": VERSION,
    }


# --------------------------------------------------------------------------- #
# HTTP endpoint
# --------------------------------------------------------------------------- #
def _make_handler(depth_cap: int, sem: threading.BoundedSemaphore):
    from http.server import BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

    class Handler(BaseHTTPRequestHandler):
        # HTTP/1.0 so we can stream to EOF without chunked-encoding bookkeeping.
        protocol_version = "HTTP/1.0"
        server_version = "qucalc_search/" + VERSION

        def _cors(self) -> None:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")

        def _send_json(self, code: int, obj: dict) -> None:
            body = json.dumps(obj).encode()
            self.send_response(code)
            self._cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def log_message(self, fmt, *args):  # quieter default logging
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

        def do_OPTIONS(self):
            self.send_response(204)
            self._cors()
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self):
            parsed = urlparse(self.path)
            route = parsed.path.rstrip("/") or "/"
            params = parse_qs(parsed.query)

            if route == "/":
                self._send_json(200, {
                    "service": "qucalc_search",
                    "version": VERSION,
                    "usage": {
                        "search": "/search?qc=<history[,history…]>&max_depth=<1..%d>"
                                  "&limit=<1..%d>&listeners=<phase,depth,capacity:R,head:N>"
                                  "&stream=<0|1>&mode=<possibilities|events>"
                                  % (depth_cap, MAX_LIMIT_CAP),
                        "solve": "/solve?qc=<history[,history…]>&max_depth=<1..%d>"
                                 % depth_cap,
                    },
                    "alphabet": TWISTS,
                    "caps": {"max_depth": depth_cap, "max_limit": MAX_LIMIT_CAP},
                    "listeners": ["phase", "depth", "capacity:R", "head:N", "count (always on)"],
                    "response": {
                        "search": "application/x-ndjson; first line _meta, last line _done",
                        "solve": "application/json; one answer, {solved: true|false, …}",
                    },
                })
                return
            if route == "/health":
                self._send_json(200, {"ok": True})
                return
            if route == "/solve":
                raw = (params.get("qc") or [""])[0]
                position = "".join(s for s in raw.split(",") if s)
                if not position:
                    self._send_json(400, {"error": "qc required"})
                    return
                try:
                    validate_history(position)
                except ValueError as e:
                    self._send_json(400, {"error": str(e)})
                    return
                try:
                    md = int((params.get("max_depth") or [depth_cap])[0])
                except ValueError:
                    self._send_json(400, {"error": "max_depth must be an integer"})
                    return
                md = max(1, min(md, depth_cap))
                if not sem.acquire(blocking=False):
                    self._send_json(429, {"error": "host at capacity (--max-concurrent); retry"})
                    return
                try:
                    self._send_json(200, solve(position, max_depth=md))
                finally:
                    sem.release()
                return
            if route != "/search":
                self._send_json(404, {"error": "not found", "path": route})
                return

            raw_qc = (params.get("qc") or [""])[0]
            seeds = [s for s in raw_qc.split(",") if s]
            if not seeds:
                self._send_json(400, {"error": "qc required (comma-separate for several)"})
                return
            try:
                for s in seeds:
                    validate_history(s)
            except ValueError as e:
                self._send_json(400, {"error": str(e)})
                return
            try:
                max_depth = int((params.get("max_depth") or [DEFAULT_MAX_DEPTH])[0])
                limit = int((params.get("limit") or [DEFAULT_LIMIT])[0])
            except ValueError:
                self._send_json(400, {"error": "max_depth and limit must be integers"})
                return
            try:
                listeners = parse_listeners((params.get("listeners") or [""])[0])
            except ValueError as e:
                self._send_json(400, {"error": str(e)})
                return
            stream = (params.get("stream") or ["1"])[0] != "0"
            absorbing = (params.get("mode") or ["possibilities"])[0] == "events" \
                or (params.get("absorbing") or ["0"])[0] == "1"
            max_depth = max(1, min(max_depth, depth_cap))
            limit = max(1, min(limit, MAX_LIMIT_CAP))

            if not sem.acquire(blocking=False):
                self._send_json(429, {"error": "host at capacity (--max-concurrent); retry"})
                return
            try:
                self.send_response(200)
                self._cors()
                self.send_header("Content-Type", "application/x-ndjson")
                self.end_headers()
                self.wfile.write((json.dumps({
                    "_meta": True, "qc": seeds, "max_depth": max_depth,
                    "limit": limit, "stream": stream,
                    "mode": "events" if absorbing else "possibilities",
                    "version": VERSION,
                }) + "\n").encode())
                self.wfile.flush()

                def emit(rec):
                    if stream:
                        self.wfile.write((json.dumps(rec) + "\n").encode())
                        self.wfile.flush()

                rep = run_search(seeds, max_depth, limit, listeners,
                                 on_closure=emit, absorbing=absorbing)
                rep["_done"] = True
                self.wfile.write((json.dumps(rep) + "\n").encode())
            except (BrokenPipeError, ConnectionResetError):
                pass  # client hung up mid-stream
            finally:
                sem.release()

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8765,
          depth_cap: int = MAX_DEPTH_CAP,
          max_concurrent: int = DEFAULT_MAX_CONCURRENT) -> None:
    from http.server import ThreadingHTTPServer
    depth_cap = max(1, min(depth_cap, MAX_DEPTH_CAP))
    sem = threading.BoundedSemaphore(max(1, max_concurrent))
    httpd = ThreadingHTTPServer((host, port), _make_handler(depth_cap, sem))
    sys.stderr.write(
        "qucalc_search %s on http://%s:%d  (depth_cap=%d, max_concurrent=%d)\n"
        % (VERSION, host, port, depth_cap, max_concurrent)
    )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nstopped\n")
        httpd.server_close()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _time_mode() -> None:
    """Print the candidate/closure/latency numbers on the current host."""
    for seed in ("^<v>+-", "^v<>+-", "+-+-"):
        for md in (4, 6):
            t0 = time.time()
            n = sum(1 for _ in search(seed, max_depth=md, limit=None))
            print(f"  seed {seed!r:10s} max_depth {md}: {n:6d} closures  {time.time()-t0:6.2f}s")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("qc", nargs="?", help="QuCalc position(s) to search from — comma-separate for several")
    p.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH,
                   help=f"max appended twists (default {DEFAULT_MAX_DEPTH})")
    p.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                   help=f"stop after this many closures (default {DEFAULT_LIMIT}; 0 = no limit)")
    p.add_argument("--listeners", default="",
                   help="rollups to report: phase,depth,capacity:R,head:N (count always on)")
    p.add_argument("--events", action="store_true",
                   help="absorbing: stop each branch at its first closure (events, not possibilities)")
    p.add_argument("--solve", action="store_true",
                   help="pick the one closure the substrate takes (least free action); JSON answer")
    p.add_argument("--json", action="store_true", help="emit NDJSON instead of plain words")
    p.add_argument("--count-only", action="store_true", help="print only the closure count")
    p.add_argument("--serve", action="store_true", help="run the HTTP endpoint instead")
    p.add_argument("--host", default="127.0.0.1",
                   help="bind address (default 127.0.0.1; use 0.0.0.0 to expose)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--max-depth-cap", type=int, default=MAX_DEPTH_CAP,
                   help=f"per-deployment /search depth ceiling (default {MAX_DEPTH_CAP})")
    p.add_argument("--max-concurrent", type=int, default=DEFAULT_MAX_CONCURRENT,
                   help=f"simultaneous /search enumerations (default {DEFAULT_MAX_CONCURRENT})")
    p.add_argument("--time", action="store_true", help="benchmark search on this host and exit")
    args = p.parse_args(argv)

    if args.serve:
        serve(args.host, args.port, args.max_depth_cap, args.max_concurrent)
        return 0
    if args.time:
        _time_mode()
        return 0
    if not args.qc:
        p.error("qc position required (or use --serve / --time)")
    seeds = [s for s in args.qc.split(",") if s]
    try:
        for s in seeds:
            validate_history(s)
        listeners = parse_listeners(args.listeners)
    except ValueError as e:
        p.error(str(e))

    if args.solve:
        position = "".join(seeds)
        # solve reaches to the cap by default (it widens from floor+2 only as needed)
        md = args.max_depth if args.max_depth != DEFAULT_MAX_DEPTH else MAX_DEPTH_CAP
        print(json.dumps(solve(position, max_depth=md), indent=2))
        return 0

    limit = None if args.limit == 0 else args.limit

    def show(rec):
        if args.count_only:
            return
        if args.json:
            print(json.dumps(rec))
        else:
            print(f"{rec['cont']:<{args.max_depth}}  ->  {rec['history']}  [{rec['phase']}]"
                  + (f"  <{rec['qc']}>" if "qc" in rec else ""))

    rep = run_search(seeds, args.max_depth, limit, listeners,
                     on_closure=show, absorbing=args.events)
    if args.count_only and not args.listeners:
        print(rep["found"])
    if args.listeners:
        print(json.dumps(rep["listeners"], indent=2))
    sys.stderr.write(f"{rep['found']} closures from {seeds} within {args.max_depth} twists "
                     f"in {rep['elapsed_s']}s\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
