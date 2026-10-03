#!/usr/bin/env python3
"""
asymptotic_freedom.py -- asymptotic freedom from QLF's colour carriers
(Carbon_Superconductivity.md sec 31; frozen in commit 53c08ea).

Nielsen-Hughes one-loop form: b_s = -(-1)^{2s} [(2s)^2 - 1/3] T(R), beta0 = -sum b_s, AF iff beta0 > 0.
QLF supplies C_A = 3, T_F = 1/2, n_f = 6, spin-1/2 quarks, and the colour carriers: the shortest bosonic words
with nonzero colour displacement under the sec-27b amendment, spin read from the Pauli fold (cross-axis pair ->
a single Pauli matrix, s = 1; same-axis same-sign pair -> +-I, s = 0), weighted by ways.

  A1  sign: beta0_QLF(6) > 0.
  A2  size: |beta0_QLF(5) - 23/3| <= 10 % of 23/3.

Exact arithmetic (Fractions). Stdlib only (plus twist_core for the fold).
Run:  python3 asymptotic_freedom.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction as Fr

from twist_core import pauli_fold

VEC = {'>': (0, 1), '<': (0, 2), '^': (2, 1), 'v': (1, 2), '/': (1, 1), '\\': (2, 2)}   # QLF_ColourFlux.colVec
SPATIAL = list(VEC)
C_A, T_F = 3, Fr(1, 2)
THIRD = 2 * Fr(1, 6)          # orbital term = 2 x census_split (int_0^1 x(1-x) dx = 1/6)


def nh(s):
    """Nielsen-Hughes factor per unit T(R): -(-1)^{2s} [(2s)^2 - 1/3]."""
    sign = 1 if (2 * s) % 2 == 0 else -1
    return -sign * ((2 * s) ** 2 - THIRD)


def fold_kind(w):
    a, b, c, d = pauli_fold(w)
    scalar = abs(b) < 1e-12 and abs(c) < 1e-12 and abs(a - d) < 1e-12
    return 'scalar' if scalar else 'vector'


def beta0(f1, f0, nf):
    gluon = C_A * (f1 * -nh(Fr(1)) + f0 * -nh(Fr(0)))
    quarks = nf * 2 * T_F * -(-nh(Fr(1, 2)))       # Dirac = 2 Weyl; contributes -(4/3) T_F per flavour
    return gluon - quarks


def main():
    print("Nielsen-Hughes factors -b/T:  s=1:", -nh(Fr(1)), " s=1/2 (Weyl):", -nh(Fr(1, 2)), " s=0:", -nh(Fr(0)))
    assert beta0(Fr(1), Fr(0), 6) == 7 and beta0(Fr(1), Fr(0), 5) == Fr(23, 3)
    print("QCD check (vector-only gluons): beta0(6) = 7, beta0(5) = 23/3  [cannot fail; reproduces QCD]")

    words = []
    for t, u in itertools.product(SPATIAL, repeat=2):
        disp = ((VEC[t][0] + VEC[u][0]) % 3, (VEC[t][1] + VEC[u][1]) % 3)
        if disp == (0, 0):
            continue                         # colour-neutral reversal pair
        words.append((t + u, fold_kind(t + u), disp))
    n1 = sum(1 for w in words if w[1] == 'vector')
    n0 = sum(1 for w in words if w[1] == 'scalar')
    print(f"\nshortest coloured bosonic words (length 2, spatial): {len(words)}  vector (s=1): {n1}  scalar (s=0): {n0}")
    print("  scalar words:", [w[0] for w in words if w[1] == 'scalar'])
    cross = all((w[1] == 'vector') == (VEC_axis(w[0][0]) != VEC_axis(w[0][1])) for w in words)
    print(f"  vector <=> cross-axis: {cross}")
    f1, f0 = Fr(n1, len(words)), Fr(n0, len(words))
    b6, b5 = beta0(f1, f0, 6), beta0(f1, f0, 5)
    qcd5 = Fr(23, 3)
    dev = (b5 - qcd5) / qcd5
    nf_max = (C_A * (f1 * -nh(Fr(1)) + f0 * -nh(Fr(0)))) / (2 * T_F * -(-nh(Fr(1, 2))))
    print(f"\nf1 = {f1}, f0 = {f0}")
    print(f"beta0_QLF(6) = {b6} = {float(b6):.4f}   (QCD 7)")
    print(f"beta0_QLF(5) = {b5} = {float(b5):.4f}   (QCD 23/3 = {float(qcd5):.4f}); deviation {float(dev):+.1%}")
    print(f"largest n_f with AF: {float(nf_max):.2f}   (QCD 16.5)")
    print(f"\nA1 (sign, beta0(6) > 0): {'PASS' if b6 > 0 else 'FAIL'}")
    print(f"A2 (size within 10 % at n_f = 5): {'PASS' if abs(dev) <= Fr(1, 10) else 'FAIL'}")


def VEC_axis(t):
    return {'>': 'x', '<': 'x', '^': 'y', 'v': 'y', '/': 'z', '\\': 'z'}[t]


if __name__ == "__main__":
    main()
