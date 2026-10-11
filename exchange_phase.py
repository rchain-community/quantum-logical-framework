#!/usr/bin/env python3
"""
exchange_phase.py -- does the exchange's phase separate spin-flip from no-flip? (Carbon_Superconductivity.md sec 42;
pre-registered in commit d01a5f5, before this script was written).

Phase: A_t(r) = sum over walks P from the origin to r with |r|_1 + 2k steps of the fold sign c_t(P),
sigma(t) F(P) sigma(t)^-1 = c_t(P) F(P) (a step on t's axis gives +1, any other step -1). k = 0 primary (the exchange
at c, the light frame), k = 1 reported.
Absorber: a twist; t+ read forward steps along t's displacement e_t, so it joins r and r + e_t coherently:
B_t(r) = A_t(r) + A_t(r + e_t).
Classes (sec 40a), line of flight d = +x: no-flip = twists on x, spin-flip = twists on y, z; each class takes the
twist with the largest |B|. Along site R x, perpendicular sites R y and R z, R = 1..12.

  Phi1  phase per step along the line (not blind)
  Phi2  coherence C = |B| / (|A(r)| + |A(r + e_t)|); pass iff C0(R x) <= 1/2 and C1(R x) >= 0.9 for R = 4..12
  Phi3  rho0 = |B0(along)| / |B0(perp)|, rho1 likewise (no weight)

Exact integer arithmetic. Stdlib only, plus twist_core.
Run:  python3 exchange_phase.py
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Fr
from functools import lru_cache

from twist_core import calculate_action

SPATIAL = ['^', 'v', '>', '<', '/', '\\']
R_MAX = 12


def disp(t):
    v, h, d, _ = calculate_action(t)
    return (h, v, d)


def axis(vec):
    return next(i for i, x in enumerate(vec) if x)


STEPS = [disp(t) for t in SPATIAL]


@lru_cache(maxsize=None)
def signed_walks(a, n):
    """{endpoint: signed count} of n-step walks from the origin; a step on axis a weighs +1, any other -1."""
    cur = {(0, 0, 0): 1}
    for _ in range(n):
        nxt = defaultdict(int)
        for (x, y, z), w in cur.items():
            for st in STEPS:
                nxt[(x + st[0], y + st[1], z + st[2])] += w * (1 if axis(st) == a else -1)
        cur = dict(nxt)
    return cur


def A(t, r, k):
    n = sum(abs(x) for x in r) + 2 * k
    return signed_walks(axis(disp(t)), n).get(r, 0)


def add(u, w):
    return tuple(x + y for x, y in zip(u, w))


def B(t, r, k):
    r2 = add(r, disp(t))
    a1, a2 = A(t, r, k), A(t, r2, k)
    return a1 + a2, abs(a1) + abs(a2)


def best(cls, r, k):
    """(|B|, coherence) for the twist in the class with the largest |B|."""
    vals = []
    for t in cls:
        b, inc = B(t, r, k)
        vals.append((abs(b), Fr(abs(b), inc) if inc else None, t))
    return max(vals, key=lambda v: v[0])


def main():
    no_flip = [t for t in SPATIAL if axis(disp(t)) == 0]
    flip = [t for t in SPATIAL if axis(disp(t)) != 0]

    print("Phi1  phase along the line, A_t(R x) at k = 0 (sign per R)")
    for t in SPATIAL:
        print(f"  {t!r:5} " + " ".join('+' if A(t, (R, 0, 0), 0) > 0 else '-' if A(t, (R, 0, 0), 0) < 0 else '0'
                                     for R in range(1, R_MAX + 1)))

    for k in (0, 1):
        print(f"\n=== k = {k} {'(primary, the light frame)' if k == 0 else '(reported)'} ===")
        phi2 = True
        rows = []
        for R in range(1, R_MAX + 1):
            along = (R, 0, 0)
            perps = [(0, R, 0), (0, 0, R)]
            b0, c0, t0 = best(no_flip, along, k)
            b1, c1, t1 = best(flip, along, k)
            b0p = max(best(no_flip, p, k)[0] for p in perps)
            b1p = max(best(flip, p, k)[0] for p in perps)
            rho0 = Fr(b0, b0p) if b0p else None
            rho1 = Fr(b1, b1p) if b1p else None
            if R >= 4:
                phi2 &= c0 is not None and c1 is not None and c0 <= Fr(1, 2) and c1 >= Fr(9, 10)
            rows.append((R, b0, c0, t0, b1, c1, t1, b0p, b1p, rho0, rho1))
        print("  R  |B0| C0 (t)      |B1| C1 (t)      |B0perp| |B1perp|  rho0     rho1")
        for R, b0, c0, t0, b1, c1, t1, b0p, b1p, rho0, rho1 in rows:
            f = lambda q: '-' if q is None else str(q)
            print(f"  {R:<2} {b0:<5} {f(c0):<3} ({t0!r:4}) {b1:<5} {f(c1):<3} ({t1!r:4}) "
                  f"{b0p:<8} {b1p:<8}  {f(rho0):<8} {f(rho1)}")
        print(f"  Phi2 (phase only, R = 4..12): {'PASS' if phi2 else 'FAIL'}")
        cs = {c for row in rows for c in (row[2], row[5]) if c is not None}
        print(f"  coherence values seen: {sorted(cs)}")


if __name__ == '__main__':
    main()
