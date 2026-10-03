#!/usr/bin/env python3
"""How many bits does a ZFA closure carry into its own future?

Companion to Memetics_QLF.md. Exact integer counts, no floats until the entropy.

1. Renewal (sampled check of a two-line proof): if `h` is count-balanced then for
   every continuation `c`, `h·c` is balanced iff `c` is, and
   `pauli_fold(h·c) = σ(h)·pauli_fold(c)` with `σ(h) = ±1`. So the future of a closed
   history depends on *which way* it closed only through one sign bit, and
   `max_excursion(h·c) = max(max_excursion(h), max_excursion(c))`.
2. The sign census: for balanced histories (and for primes, i.e. first closures) of
   length L, the split W = W₊ + W₋ and the entropy H(σ) of the surviving bit, beside
   log₂ W, the which-way information the closure erases.
3. Controls: the same split on reduced alphabets. With fewer than two spatial axes
   the sign is fixed by L alone, so a closure carries zero bits forward.

Run: python3 meme_closure_bits.py [--max-len 16] [--samples 20000]
"""
from __future__ import annotations

import argparse
import math
import random
from collections import defaultdict

from closure_walk import edge_sign
from qucalc_search import max_excursion
from twist_core import pauli_fold, TWISTS

# twist -> (axis, step); axis 3 is the gauge axis, as in closure_walk.edge_sign
AX = {"^": (0, 1), "v": (0, -1), ">": (1, 1), "<": (1, -1),
      "/": (2, 1), "\\": (2, -1), "+": (3, 1), "-": (3, -1)}


def balanced(h: str) -> bool:
    x = [0, 0, 0, 0]
    for t in h:
        a, s = AX[t]
        x[a] += s
    return x == [0, 0, 0, 0]


def renewal_check(samples: int, seed: int = 1) -> dict:
    """Sample closures h (by rejection) and arbitrary continuations c."""
    rng = random.Random(seed)
    checked = bad_fold = bad_bal = bad_exc = 0
    while checked < samples:
        n = rng.choice([1, 2, 3])
        h = "".join(rng.choice(TWISTS) for _ in range(2 * n))
        if not balanced(h):
            continue
        c = "".join(rng.choice(TWISTS) for _ in range(rng.randint(1, 8)))
        fh, fc, fhc = pauli_fold(h), pauli_fold(c), pauli_fold(h + c)
        sigma = fh[0].real  # fold is (a, b, c, d); proven ±I for balanced h
        if abs(abs(sigma) - 1) > 1e-9 or any(abs(fh[k] - (sigma if k in (0, 3) else 0)) > 1e-9
                                              for k in range(4)):
            bad_fold += 1
        if any(abs(fhc[k] - sigma * fc[k]) > 1e-9 for k in range(4)):
            bad_fold += 1
        if balanced(h + c) != balanced(c):
            bad_bal += 1
        if max_excursion(h + c) != max(max_excursion(h), max_excursion(c)):
            bad_exc += 1
        checked += 1
    return {"checked": checked, "fold_mismatch": bad_fold,
            "balance_mismatch": bad_bal, "excursion_mismatch": bad_exc}


def sign_census(alphabet: str, max_len: int) -> list[tuple]:
    """Exact DP on (x, σ). Returns rows (L, W+, W-, P+, P-) where W counts all
    balanced histories of length L and P counts primes (first return at L)."""
    steps = [AX[t] for t in alphabet]
    allw = defaultdict(int)                 # all paths
    taboo = defaultdict(int)                # paths not yet returned to 0
    allw[((0, 0, 0, 0), 1)] = 1
    taboo[((0, 0, 0, 0), 1)] = 1
    rows = []
    for L in range(1, max_len + 1):
        na, nt = defaultdict(int), defaultdict(int)
        for src, dst in ((allw, na), (taboo, nt)):
            for (x, sg), w in src.items():
                for a, s in steps:
                    nx = list(x)
                    e = edge_sign(nx, a, s)
                    nx[a] += s
                    dst[(tuple(nx), sg * e)] += w
        zero = (0, 0, 0, 0)
        if L % 2 == 0:
            rows.append((L, na[(zero, 1)], na[(zero, -1)], nt[(zero, 1)], nt[(zero, -1)]))
        for k in list(nt):                  # primes stop at the origin
            if k[0] == zero:
                del nt[k]
        allw, taboo = na, nt
    return rows


def H2(p: float) -> float:
    return 0.0 if p in (0.0, 1.0) else -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def report(name: str, alphabet: str, max_len: int) -> None:
    print(f"\n[{name}] alphabet {alphabet!r}")
    print(f"{'L':>3} {'W':>16} {'A=W+-W-':>16} {'log2 W':>8} {'H(sign)':>8}"
          f" | {'primes P':>14} {'A_P':>14} {'H(sign|prime)':>13}")
    for L, wp, wm, pp, pm in sign_census(alphabet, max_len):
        W, P = wp + wm, pp + pm
        hw = H2(wp / W) if W else 0.0
        hp = H2(pp / P) if P else 0.0
        print(f"{L:>3} {W:>16} {wp - wm:>16} {math.log2(W) if W else 0:>8.3f} {hw:>8.4f}"
              f" | {P:>14} {pp - pm:>14} {hp:>13.4f}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max-len", type=int, default=12)
    ap.add_argument("--samples", type=int, default=20000)
    args = ap.parse_args(argv)

    r = renewal_check(args.samples)
    print("renewal check:", r)
    ok = r["fold_mismatch"] == r["balance_mismatch"] == r["excursion_mismatch"] == 0

    report("full 8-twist alphabet", "^v<>/\\+-", args.max_len)
    report("control: two spatial axes", "^v<>", args.max_len)
    report("control: one spatial axis + gauge", "^v+-", args.max_len)
    report("control: one axis", "+-", args.max_len)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
