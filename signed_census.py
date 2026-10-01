#!/usr/bin/env python3
"""
signed_census.py -- the Z2 loop gas with the histories' phases (Carbon_Superconductivity.md sec 22, frozen in f093c18).

Each closed-loop configuration C on the L x L torus gets amplitude eta(C) w^|C|, eta = product of the QLF_EdgeSign edge
signs in the plane: an x-edge at row y carries (-1)^y (the sign (-1)^(sum of spatial coordinates beyond its axis)),
a y-edge carries +1. Every plaquette then has exactly one negative edge: pi flux. This is the high-temperature
expansion of the fully frustrated Ising model. Exact transfer matrices give the four winding sectors; R_s =
Z_s(odd x-winding) / Z_s(even). Deconfined: |R_s| -> 1 with L; confined: |R_s| -> 0.

Also prints the unsigned gas (sec 19) beside it for comparison.

Run:  python3 signed_census.py        (needs numpy)
"""
from __future__ import annotations

import math


def sectors(L: int, w: float, signed: bool, np):
    n = 1 << L
    full = n - 1
    rotl = lambda v: ((v << 1) | (v >> (L - 1))) & full
    pc = [bin(k).count("1") for k in range(n)]
    # sign of a set of horizontal edges crossing the cut: product over occupied rows y of (-1)^y
    hsign = [(-1) ** sum(1 for y in range(L) if (k >> y) & 1 and y % 2 == 1) for k in range(n)]
    T = np.zeros((2 * n, 2 * n))
    for h_in in range(n):
        for v in range(n):
            h_out = h_in ^ v ^ rotl(v)
            wt = w ** (pc[v] + pc[h_out]) * (hsign[h_out] if signed else 1)
            dy = (v >> (L - 1)) & 1
            for y in (0, 1):
                T[2 * h_out + (y ^ dy), 2 * h_in + y] += wt
    M = np.linalg.matrix_power(T, L)
    Z = {}
    for h in range(n):
        for y in (0, 1):
            key = (pc[h] & 1, y)
            Z[key] = Z.get(key, 0.0) + M[2 * h + y, 2 * h]
    return Z


def main():
    import numpy as np
    ws = [0.3, 0.414, 0.5, 0.7, 0.9, 1.0]
    Ls = (4, 6, 8, 10)
    for signed in (False, True):
        print(("SIGNED census (history phases, pi flux)" if signed else "unsigned gas (sec 19, for comparison)")
              + ":  |R| = |Z(odd x-winding)/Z(even)|")
        print(f"  {'w':>6}" + "".join(f"{'L=' + str(L):>12}" for L in Ls) + f"{'6 -> 10':>12}")
        for w in ws:
            row = []
            for L in Ls:
                Z = sectors(L, w, signed, np)
                row.append(abs(Z[(1, 0)] / Z[(0, 0)]) if Z[(0, 0)] != 0 else float("nan"))
            trend = "falls" if row[3] < row[1] else "grows"
            print(f"  {w:>6.3f}" + "".join(f"{r:>12.5f}" for r in row) + f"{trend:>12}")
        print()


if __name__ == "__main__":
    main()
    print("""At w = 1 the signed sum of every sector is exactly 0 (printed as nan): flipping one plaquette, C -> C + dp, is a
bijection of each sector that keeps the weight (equal weight per way) and flips the sign (the plaquette's holonomy is
-1), so the sum equals minus itself. Just below w = 1 the cancellations are near-total and floating point cannot
resolve them; the pre-registered values stop at w = 0.9.""")
