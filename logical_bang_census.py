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

--depth12 (sec 44, pre-registered in commit e7c7e25): entangled = the two loops' spans overlap; remainder any
count-balanced word of length 0, 2 or 4; collinear (P and A pooled) vs orthogonal. Exact signed sums by a dynamic
program over interleavings carrying the Pauli product. Within a category every word has the same number of negative
twists (two per loop, half the remainder), so the fold sign depends only on the axis sequence: each loop is summed
over its 6 ordered axis pairs (x4 sign choices) and each remainder over its axis sequences (x the number of balanced
sign assignments). L0 checks this against the sec 43a totals and against pauli_fold on sampled words.

  L0  sec 43a totals reproduced at lengths 8, 10; entangled O at length 8 has S = 0
  L1  length 12: pass iff C(O, entangled) <= 0.01 C(collinear, entangled) > 0; exact zero reported
  L2  length 10 under the new definition, and every remainder class at length 12

Exact integers. Stdlib only, plus twist_core.
Run:  python3 logical_bang_census.py [--depth12]
"""
from __future__ import annotations

import random
from collections import defaultdict
from fractions import Fraction as Fr
from itertools import combinations, product

import sys
from math import comb

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


# ---------------------------------------------------------------- sec 44: exact signed sums by dynamic program
# Pauli group element = (k, p): i^k * P_p, p in 0..3 = I, X, Y, Z
_MUL = {}
for _p in range(4):
    for _q in range(4):
        if _p == 0:
            _MUL[_p, _q] = (0, _q)
        elif _q == 0:
            _MUL[_p, _q] = (0, _p)
        elif _p == _q:
            _MUL[_p, _q] = (0, 0)
        else:
            _r = 6 - _p - _q
            _MUL[_p, _q] = (1 if (_q - _p) % 3 == 1 else 3, _r)


def _letter(t):
    """Twist -> (k, p) by matching PAULI_MAP."""
    m = PAULI_MAP[t]
    basis = {0: (1, 0, 0, 1), 1: (0, 1, 1, 0), 2: (0, -1j, 1j, 0), 3: (1, 0, 0, -1)}
    for p, b in basis.items():
        for k in range(4):
            ph = 1j ** k
            if all(abs(x - ph * y) < 1e-12 for x, y in zip(m, b)):
                return (k, p)
    raise ValueError(t)


LET = {t: _letter(t) for t in ALL}


def _mul(a, b):
    k, p = _MUL[a[1], b[1]]
    return ((a[0] + b[0] + k) % 4, p)


def signed_interleavings(A, B, R, mode):
    """(N, S) over all interleavings of letter sequences A, B, R (each kept in order).
    mode 'all'; 'AB' = all of A before any of B; 'BA' = all of B before any of A."""
    la, lb, lr = len(A), len(B), len(R)
    cur = {(0, 0, 0): {(0, 0): 1}}
    for _ in range(la + lb + lr):
        nxt = defaultdict(lambda: defaultdict(int))
        for (i, j, k), states in cur.items():
            moves = []
            if i < la and not (mode == 'BA' and j < lb):
                moves.append(((i + 1, j, k), LET[A[i]]))
            if j < lb and not (mode == 'AB' and i < la):
                moves.append(((i, j + 1, k), LET[B[j]]))
            if k < lr:
                moves.append(((i, j, k + 1), LET[R[k]]))
            for key, l in moves:
                tgt = nxt[key]
                for st, c in states.items():
                    tgt[_mul(st, l)] += c
        cur = nxt
    final = cur[(la, lb, lr)]
    n = s = 0
    for (k, p), c in final.items():
        assert p == 0 and k in (0, 2), (k, p)
        n += c
        s += c if k == 0 else -c
    return n, s


def loop_reps():
    """Ordered spatial axis pairs (a, b) -> representative loop (+a, +b, -a, -b), multiplicity 4."""
    pos = {0: '>', 1: '^', 2: '/'}
    neg = {0: '<', 1: 'v', 2: '\\'}
    return [((a, b), pos[a] + pos[b] + neg[a] + neg[b]) for a in range(3) for b in range(3) if a != b]


def remainder_reps(n):
    """Axis sequences of length n with every axis count even -> (representative balanced word, multiplicity)."""
    pos = {0: '>', 1: '^', 2: '/', 3: '+'}
    neg = {0: '<', 1: 'v', 2: '\\', 3: '-'}
    out = []
    for seq in product(range(4), repeat=n):
        cnt = [seq.count(a) for a in range(4)]
        if any(c % 2 for c in cnt):
            continue
        seen = [0] * 4
        w = ''
        for a in seq:
            w += pos[a] if seen[a] < cnt[a] // 2 else neg[a]
            seen[a] += 1
        mult = 1
        for c in cnt:
            mult *= comb(c, c // 2)
        out.append((seq, w, mult))
    return out


def roles(ax1, ax2, seq):
    p1, p2 = set(ax1), set(ax2)
    out = []
    for a in seq:
        if a == 3:
            out.append('g')
        elif p1 == p2:
            out.append('n' if a not in p1 else 'p')
        else:
            out.append('s' if a in p1 and a in p2 else 'n')
    return ''.join(sorted(out)) or '-'


def census_dp(L):
    """{(relation, remainder roles, entangled|separate): [N, S]} for unordered loop pairs."""
    tab = defaultdict(lambda: [0, 0])
    for ax1, A in loop_reps():
        for ax2, B in loop_reps():
            rel = 'collinear' if set(ax1) == set(ax2) else 'O'
            for seq, R, mult in remainder_reps(L - 8):
                w = 4 * 4 * mult
                nt, st = signed_interleavings(A, B, R, 'all')
                nab, sab = signed_interleavings(A, B, R, 'AB')
                nba, sba = signed_interleavings(A, B, R, 'BA')
                key = (rel, roles(ax1, ax2, seq))
                e = tab[key + ('entangled',)]
                e[0] += w * (nt - nab - nba)
                e[1] += w * (st - sab - sba)
                e = tab[key + ('separate',)]
                e[0] += w * (nab + nba)
                e[1] += w * (sab + sba)
    for v in tab.values():               # ordered loop pairs -> unordered
        assert v[0] % 2 == 0 and v[1] % 2 == 0
        v[0] //= 2
        v[1] //= 2
    return tab


def sample_check(L, trials=2000):
    """Random words of each category: the DP's sign rule against pauli_fold."""
    rng = random.Random(44)
    rems = [''.join(w) for w in product(ALL, repeat=L - 8)
            if all(x == 0 for x in calculate_action(''.join(w)))] if L > 8 else ['']
    for _ in range(trials):
        l1, l2, r = rng.choice(ELECTRONS), rng.choice(ELECTRONS), rng.choice(rems)
        labels = [1] * 4 + [2] * 4 + [0] * len(r)
        rng.shuffle(labels)
        it = {1: iter(l1), 2: iter(l2), 0: iter(r)}
        word = ''.join(next(it[x]) for x in labels)
        rep = {}
        # same axis sequence with representative letters
        ax_word = [axis(t) for t in word]
        cnt = [ax_word.count(a) for a in range(4)]
        seen = [0] * 4
        pos = {0: '>', 1: '^', 2: '/', 3: '+'}
        neg = {0: '<', 1: 'v', 2: '\\', 3: '-'}
        w2 = ''
        for a in ax_word:
            w2 += pos[a] if seen[a] < cnt[a] // 2 else neg[a]
            seen[a] += 1
        assert fold_sign(word) == fold_sign(w2), (word, w2)
    return trials


def main_depth12():
    print("L0  method checks")
    for L in (8, 10):
        print(f"  sampled words, length {L}: {sample_check(L)} agree with pauli_fold")
    t8 = census_dp(8)
    t10 = census_dp(10)
    tot = lambda tab, rel, r=None: [sum(v[i] for (a, b, c), v in tab.items() if a == rel and (r is None or b == r))
                                     for i in (0, 1)]
    checks = [
        (tot(t8, 'collinear'), [6720, 576]), (tot(t8, 'O'), [13440, 384]),
        (tot(t10, 'collinear', 'nn'), [604800, -5760]), (tot(t10, 'collinear', 'pp'), [1209600, -42240]),
        (tot(t10, 'collinear', 'gg'), [604800, -51840]), (tot(t10, 'O', 'nn'), [2419200, -7680]),
        (tot(t10, 'O', 'ss'), [1209600, -3840]), (tot(t10, 'O', 'gg'), [1209600, -34560]),
    ]
    ok = all(a == b for a, b in checks)
    print(f"  sec 43a totals reproduced: {'yes' if ok else 'NO'}  {checks if not ok else ''}")
    e8 = t8['O', '-', 'entangled']
    print(f"  length 8, entangled O: N={e8[0]} S={e8[1]}")
    assert ok

    for L, tab in ((10, t10), (12, census_dp(12))):
        print(f"\n=== length {L} ===")
        for key in sorted(tab):
            n, s_ = tab[key]
            print(f"  {key[0]:9} {key[1]:5} {key[2]:9}  N={n:<11} S={s_:<9} C={float(Fr(abs(s_), n)) if n else 0:.6f}")
        for rel in ('collinear', 'O'):
            n, s_ = tot({k: v for k, v in tab.items() if k[2] == 'entangled'}, rel)
            print(f"  {rel:9} entangled, all remainders: N={n} S={s_} C={float(Fr(abs(s_), n)):.6f}")
        nc, sc = tot({k: v for k, v in tab.items() if k[2] == 'entangled'}, 'collinear')
        no, so = tot({k: v for k, v in tab.items() if k[2] == 'entangled'}, 'O')
        cc, co = Fr(abs(sc), nc), Fr(abs(so), no)
        if L == 12:
            print(f"  L1: C(O)/C(collinear) = {float(co / cc) if cc else float('inf'):.6f}  ->  "
                  f"{'PASS' if cc > 0 and co <= cc / 100 else 'FAIL'};  exact zero S(O, entangled) = 0: "
                  f"{'yes' if so == 0 else 'no'}")


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
    main_depth12() if '--depth12' in sys.argv else main()
