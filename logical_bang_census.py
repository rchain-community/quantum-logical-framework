#!/usr/bin/env python3
"""
logical_bang_census.py -- the logical bang as a signed census of two electrons (Carbon_Superconductivity.md sec 43;
pre-registered in commit 5708101, before this script was written).

Electrons: the 24 four-twist fermion closures (fold -I), the loops a b a' b' on two spatial axes. Every ZFA word of
length 8 and 10 that contains two disjoint electron loops as subsequences; at length 10 the rest is one balanced
pair on one axis. One way = (word, unordered choice of the two loops). Each way counts with its word's fold sign.

Relations: P (same plane, same turn), A (same plane, opposite turn), O (orthogonal planes); the remainder for P/A:
no-flip (on the common normal), flip (in the plane), gauge; for O: normal (of either loop), shared (the axis both
planes contain), gauge. Contiguous (each loop in consecutive positions) vs interleaved.
Readout per class: N (ways), S (signed sum), C = |S| / N.

  K0  contiguous classes have C = 1 (control, by construction)
  K1  length 10, interleaved, P and A: pass iff C(no-flip) <= 0.1 C(flip) and C(flip) >= 0.05
  K2  everything else, reported

Exact integers. Stdlib only, plus twist_core.
Run:  python3 logical_bang_census.py
"""
from __future__ import annotations

import random
from collections import defaultdict
from fractions import Fraction as Fr
from itertools import combinations, product

from twist_core import PAULI_MAP, calculate_action, is_zfa, pauli_fold

SPATIAL = ['^', 'v', '>', '<', '/', '\\']
ALL = SPATIAL + ['+', '-']


def disp(t):
    v, h, d, _ = calculate_action(t)
    return (h, v, d)


def axis(t):
    if t in '+-':
        return 3
    return next(i for i, x in enumerate(disp(t)) if x)


def cross(u, w):
    return (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])


def fold_sign(word):
    f = pauli_fold(word)
    assert abs(f[1]) < 1e-9 and abs(f[2]) < 1e-9 and abs(f[0] - f[3]) < 1e-9 and abs(abs(f[0]) - 1) < 1e-9, word
    assert abs(f[0].imag) < 1e-9, word
    return 1 if f[0].real > 0 else -1


# the electrons: every four-twist ZFA word with fold -I
ELECTRONS = [''.join(w) for w in product(ALL, repeat=4) if is_zfa(''.join(w), 4) and fold_sign(''.join(w)) == -1]
assert len(ELECTRONS) == 24


def plane(loop):
    return frozenset(axis(t) for t in loop)


def normal(loop):
    return ({0, 1, 2} - plane(loop)).pop()


def turn(loop):
    return cross(disp(loop[0]), disp(loop[1]))[normal(loop)]


def relation(l1, l2):
    if plane(l1) != plane(l2):
        return 'O'
    return 'P' if turn(l1) == turn(l2) else 'A'


def remainder_class(l1, l2, c):
    if c == 3:
        return 'gauge'
    if plane(l1) == plane(l2):
        return 'no-flip' if c == normal(l1) else 'flip'
    return 'shared' if c in plane(l1) and c in plane(l2) else 'normal'


def patterns(L):
    """Position labels (1 = loop 1, 2 = loop 2, 0 = remainder), loop 1 starting first (unordered loops)."""
    out = []
    for p1 in combinations(range(L), 4):
        rest = [i for i in range(L) if i not in p1]
        for p2 in combinations(rest, 4):
            if p2[0] < p1[0]:
                continue
            p0 = [i for i in rest if i not in p2]
            out.append((p1, p2, tuple(p0)))
    return out


def contiguous(p):
    return p[3] - p[0] == 3


def census(L, check_every=0):
    """{(relation, remainder, contiguity): [N, S]}"""
    rems = [''] if L == 8 else [a + b for a, b in (('^', 'v'), ('v', '^'), ('>', '<'), ('<', '>'),
                                                    ('/', '\\'), ('\\', '/'), ('+', '-'), ('-', '+'))]
    pats = patterns(L)
    tab = defaultdict(lambda: [0, 0])
    rng = random.Random(43)
    for l1 in ELECTRONS:
        for l2 in ELECTRONS:
            rel = relation(l1, l2)
            for r in rems:
                rc = remainder_class(l1, l2, axis(r[0])) if r else '-'
                for p1, p2, p0 in pats:
                    w = [''] * L
                    for i, t in zip(p1, l1):
                        w[i] = t
                    for i, t in zip(p2, l2):
                        w[i] = t
                    for i, t in zip(p0, r):
                        w[i] = t
                    word = ''.join(w)
                    s = fold_sign(word)
                    cont = 'contiguous' if contiguous(p1) and contiguous(p2) else 'interleaved'
                    e = tab[rel, rc, cont]
                    e[0] += 1
                    e[1] += s
    return tab


def show(tab):
    for key in sorted(tab):
        n, s = tab[key]
        print(f"  {key[0]}  {key[1]:8} {key[2]:11}  N={n:<8} S={s:<8} C={float(Fr(abs(s), n)):.4f}")


def main():
    for L in (8, 10):
        print(f"=== length {L} ===")
        tab = census(L)
        show(tab)
        k0 = all(abs(s) == n for (rel, rc, cont), (n, s) in tab.items() if cont == 'contiguous')
        print(f"  K0 contiguous classes all C = 1: {'yes' if k0 else 'NO'}")
        if L == 10:
            ok = True
            for rel in ('P', 'A'):
                cn = Fr(abs(tab[rel, 'no-flip', 'interleaved'][1]), tab[rel, 'no-flip', 'interleaved'][0])
                cf = Fr(abs(tab[rel, 'flip', 'interleaved'][1]), tab[rel, 'flip', 'interleaved'][0])
                print(f"  K1 {rel}: C(no-flip) = {float(cn):.4f}, C(flip) = {float(cf):.4f}, "
                      f"ratio = {float(cn / cf) if cf else float('inf'):.4f}")
                ok &= cf >= Fr(5, 100) and cn <= cf / 10
            print(f"  K1: {'PASS' if ok else 'FAIL'}")
        print()


if __name__ == '__main__':
    main()
