#!/usr/bin/env python3
"""stationary_phase_census.py — the SIGNED half of `Stationary_Action.md`, tested.

`QLF_StationaryAction` proves the unsigned statement: the census multiplicity W(x) of
histories ending at displacement x is symmetric about balance, so its first variation
vanishes there and balance is its mode. That is the classical (Euclidean) half. Feynman's
argument is about the signed sum: phases e^{iS/ħ} cancel away from the stationary path.

In QLF the phase of a history is the ℤ₂ holonomy of the edge-sign connection
(`closure_walk.edge_sign`, Lean `QLF_EdgeSign.holonomy_eq_invCount`). It is defined for
every history, open or closed. So the signed amplitude A_L(x) is the sum of phases over all
length-L histories ending at x ∈ ℤ⁴. It is computed exactly on the state (x, running sign).

Pre-registered (fixed before the first run, at the commit adding this file):

  S1  |A_L(x)| is symmetric under x → −x                    (signed conjugate symmetry)
  S2  argmax_x |A_L(x)| is x = 0 for even L                 (signed mode at balance)
  S3  the coherence |A_L(x)| / W_L(x) is largest at x = 0   (stationary PHASE: least
      cancellation on the balanced class)

Each is reported PASS / FAIL. A FAIL is recorded, not tuned away. Exact integers only.

Result (added after the run, L ≤ 12): S1 PASS, S2 PASS (maximum unique at the origin), S3 FAIL.
S3 was badly posed: an endpoint reached by one path has coherence exactly 1. S2 is now a theorem
for every m: `QLF_StationaryPhase.signed_mode_at_balance`; so is the identity behind it,
A_{2m}(0) = (−1)^m Σ_y A_m(y)² (`return_amplitude_sum_sq`). See Stationary_Action.md §5a.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from fractions import Fraction

from closure_walk import _AX, edge_sign

STEPS = list(_AX.values())          # (axis, sign) for the eight twists


def layer(L: int):
    """Return {x: (W, A)} for all length-L histories: W = count, A = signed phase sum."""
    cur = {(0, 0, 0, 0): (1, 1)}
    for _ in range(L):
        nxt = defaultdict(lambda: [0, 0])
        for x, (w, amp) in cur.items():
            xl = list(x)
            for a, s in STEPS:
                e = edge_sign(xl, a, s)
                y = list(x)
                y[a] += s
                t = nxt[tuple(y)]
                t[0] += w
                t[1] += e * amp
        cur = {k: (v[0], v[1]) for k, v in nxt.items()}
    return cur


def analyse(L: int) -> dict:
    lay = layer(L)
    neg = lambda x: tuple(-c for c in x)
    s1 = all(abs(A) == abs(lay[neg(x)][1]) for x, (_, A) in lay.items())
    origin = (0, 0, 0, 0)
    W0, A0 = lay.get(origin, (0, 0))
    maxA = max(abs(A) for _, A in lay.values())
    arg = sorted(x for x, (_, A) in lay.items() if abs(A) == maxA)
    s2 = (L % 2 == 0) and abs(A0) == maxA and arg == [origin]
    coh = {x: Fraction(abs(A), W) for x, (W, A) in lay.items()}
    c0 = coh.get(origin, Fraction(0))
    maxc = max(coh.values())
    s3 = (L % 2 == 0) and c0 == maxc
    # unsigned mode check (the proven half), for the record
    maxW = max(W for W, _ in lay.values())
    return {
        "L": L, "W0": W0, "A0": A0, "max_abs_A": maxA,
        "argmax_abs_A": [list(x) for x in arg[:6]], "n_argmax": len(arg),
        "coherence_origin": str(c0), "coherence_max": str(maxc),
        "unsigned_mode_at_origin": (L % 2 == 1) or W0 == maxW,
        "S1_symmetric": s1, "S2_signed_mode_at_balance": s2 if L % 2 == 0 else None,
        "S3_stationary_phase": s3 if L % 2 == 0 else None,
    }


def main(argv=None) -> int:
    max_len = int((argv or sys.argv[1:] or ["10"])[0])
    rows = [analyse(L) for L in range(1, max_len + 1)]
    for r in rows:
        print(f"L={r['L']:2d}  W0={r['W0']:>12}  A0={r['A0']:>10}  max|A|={r['max_abs_A']:>10}"
              f"  #argmax={r['n_argmax']:3d}  coh0={r['coherence_origin']:>12}  cohmax={r['coherence_max']:>8}"
              f"  S1={r['S1_symmetric']}  S2={r['S2_signed_mode_at_balance']}  S3={r['S3_stationary_phase']}")
    with open("data/stationary_phase.json", "w") as f:
        json.dump({"max_len": max_len, "rows": rows}, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
