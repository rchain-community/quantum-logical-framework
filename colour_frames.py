#!/usr/bin/env python3
"""
colour_frames.py -- Carbon_Superconductivity.md sec 35 (frozen in commit 6616f1d).

Part 1  g for commutator carriers: eigenvalues of ad(sigma_z) (coupling) against ad(sigma_z / 2) (spin) on the
        adjoint span of the Pauli carriers. Ratio 2 by construction (QLF's g = 2 rule); recorded, not a test.
Part 2  the phased colour frames D(w)V of sec 28a put c_t = omega^{-<w, v_cycTwist t>} on each relabeled spatial
        twist (gauge twists colour-trivial after sec 27b). Over every count-balanced word up to length 8,
        the product of the c_t must be 1 in all six phased frames: no closure count distinguishes the frames.

Exact integer arithmetic. Stdlib only.
Run:  python3 colour_frames.py
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Fr

VEC = {'>': (0, 1), '<': (0, 2), '^': (2, 1), 'v': (1, 2), '/': (1, 1), '\\': (2, 2), '+': (1, 0), '-': (2, 0)}
CYC = {'>': '^', '<': 'v', '^': '/', 'v': '\\', '/': '>', '\\': '<', '+': '+', '-': '-'}
STEP = {'>': (1, 0, 0, 0), '<': (-1, 0, 0, 0), '^': (0, 1, 0, 0), 'v': (0, -1, 0, 0),
        '/': (0, 0, 1, 0), '\\': (0, 0, -1, 0), '+': (0, 0, 0, 1), '-': (0, 0, 0, -1)}
TW = list(VEC)


def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0]) % 3


def part1():
    # Pauli matrices over Q(i) as (re, im) Fraction pairs; adjoint action on span{sx, sy, sz}.
    def cm(x, y): return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])
    def ca(x, y): return (x[0] + y[0], x[1] + y[1])
    Z, O, I, N = (Fr(0), Fr(0)), (Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(-1), Fr(0))
    sx = [[Z, O], [O, Z]]
    sy = [[Z, (Fr(0), Fr(-1))], [I, Z]]
    sz = [[O, Z], [Z, N]]
    mm = lambda A, B: [[ca(cm(A[i][0], B[0][j]), cm(A[i][1], B[1][j])) for j in range(2)] for i in range(2)]
    sub = lambda A, B: [[(A[i][j][0] - B[i][j][0], A[i][j][1] - B[i][j][1]) for j in range(2)] for i in range(2)]
    sc = lambda c, A: [[cm(c, x) for x in r] for r in A]
    splus = [[ca(sx[i][j], cm(I, sy[i][j])) for j in range(2)] for i in range(2)]   # sx + i sy
    for name, gen in (("coupling ad(sigma_z)", sz), ("spin ad(sigma_z/2)", sc((Fr(1, 2), Fr(0)), sz))):
        img = sub(mm(gen, splus), mm(splus, gen))
        # img = lambda * splus; read lambda off the (0,1) entry
        lam = (img[0][1][0] / splus[0][1][0]) if splus[0][1][0] != 0 else None
        print(f"  {name}: eigenvalue on sigma_+ = {lam}")
    print("  ratio coupling/spin = 2 on the transverse carriers: g = 2 for spin-1 commutator carriers"
          " (by construction; QLF's g = 2 rule)")


def part2(amended=True):
    ws = [w for w in ((a, b) for a in range(3) for b in range(3)) if symp((1, 0), w) != 0]   # off the gauge line
    LMAX = 8
    bad = defaultdict(int)
    totals = {}
    for w in ws:
        def c(t):
            if amended and t in '+-':
                return 0
            return (-symp(w, VEC[CYC[t]])) % 3
        state = {((0, 0, 0, 0), 0): 1}
        for L in range(1, LMAX + 1):
            new = defaultdict(int)
            for (x, k), n in state.items():
                for t in TW:
                    x2 = tuple(a + b for a, b in zip(x, STEP[t]))
                    if sum(abs(q) for q in x2) > LMAX - L:
                        continue
                    new[(x2, (k + c(t)) % 3)] += n
            state = new
            if L % 2 == 0:
                for (x, k), n in state.items():
                    if x == (0, 0, 0, 0):
                        totals[(w, L)] = totals.get((w, L), 0) + n
                        if k != 0:
                            bad[(w, L)] += n
    for L in range(2, LMAX + 1, 2):
        n = totals[(ws[0], L)]
        b = sum(bad[(w, L)] for w in ws)
        print(f"  L = {L}: {n} closures x {len(ws)} phased frames; closures whose phase differs from"
              f" the phase-free frame: {b}")
    return sum(bad.values())


def main():
    print("Part 1  g for commutator carriers")
    part1()
    print("\nPart 2  can a closure count see the colour frame?  (gauge twists colour-trivial, sec 27b)")
    b = part2(True)
    print(f"  => {'HOLDS: no closure distinguishes the frames' if b == 0 else 'FAILS'}")
    print("\n  (also without the amendment, gauge twists phased:)")
    b2 = part2(False)
    print(f"  => {'holds there too' if b2 == 0 else 'fails without the amendment'}")


if __name__ == "__main__":
    main()
