#!/usr/bin/env python3
"""
entanglement_order_alpha.py -- does the order of entanglement close the alpha residual?
(Carbon_Superconductivity.md sec 46; pre-registered in commit 23fc39a, before this script was written.)

Alphabet: all 8 twists with twist_core.PAULI_MAP. A word of length 2n is a closure when count-balanced (it then folds
to +-I); it is prime when no proper prefix is count-balanced. For each multiset M of twists, S(M) = sum of the fold
signs of M's prime orders. K_n = sum_M |S(M)| over the P_n prime words of length 2n; f_n = K_n / P_n.

To alpha: the one-axis irreducible coefficient 2 Catalan(n-1) becomes 2 Catalan(n-1) f_n; the total follows from
G = 1/(1 - I), every composite counted; alpha^-1 = 137 + sum_{n>=2} g_n (1/128)^(n-1), as in censusTail.

  Q0  balanced-word counts 8, 168, 5120, 190120 (lengths 2-8); sampled prime words agree with pauli_fold;
      f_n = 1 gives the cap 137.048130
  Q1  pass iff |alpha^-1 - 137.035999| < 0.0040 (closer to CODATA than w = 1/2, 137.032002)
  Q2  f_n per order, the global signed fraction |sum_M S(M)| / P_n, and the equivalent w

Method: a dynamic program over prefixes carrying the twist counts and the exact Pauli product (phase i^k times
I, X, Y, Z); prefixes that are count-balanced are dropped, so only prime words reach the end. Exact integers.

Run:  python3 entanglement_order_alpha.py [--max-n N]   (default N = 7, about a minute)
"""
from __future__ import annotations

import argparse
import random
from collections import defaultdict
from fractions import Fraction as Fr
from math import comb

from twist_core import PAULI_MAP, pauli_fold

CODATA = 137.035999177
W_HALF = 137.032002
X = Fr(1, 128)

# Pauli group element: (k, p) = i^k * sigma_p, p in 0..3 = I, X, Y, Z
_LETTER = {'^': (0, 2), 'v': (2, 2), '>': (0, 1), '<': (2, 1), '/': (0, 3), '\\': (2, 3), '+': (0, 0), '-': (2, 0)}
_LETTERS = sorted(_LETTER)
_PAIR = {'^': 'v', 'v': '^', '>': '<', '<': '>', '/': '\\', '\\': '/', '+': '-', '-': '+'}
_AXES = [('^', 'v'), ('>', '<'), ('/', '\\'), ('+', '-')]
_IDX = {c: i for i, c in enumerate(_LETTERS)}


def _pmul(a, b):
    (ka, pa), (kb, pb) = a, b
    if pa == 0:
        return ((ka + kb) % 4, pb)
    if pb == 0 or pa == pb:
        return ((ka + kb) % 4, 0 if pa == pb else pa)
    pc = 6 - pa - pb
    sgn = 1 if (pa, pb) in ((1, 2), (2, 3), (3, 1)) else 3   # sigma_a sigma_b = +- i sigma_c
    return ((ka + kb + sgn) % 4, pc)


def _balanced(counts):
    return all(counts[_IDX[a]] == counts[_IDX[b]] for a, b in _AXES)


def census(max_len, prime_only):
    """{length: {counts: {pauli: ways}}} for words (prime or all) that are balanced at that length."""
    layer = {(tuple([0] * 8), (0, 0)): 1}
    out = {}
    for L in range(1, max_len + 1):
        nxt = defaultdict(int)
        for (counts, P), w in layer.items():
            for c in _LETTERS:
                cc = list(counts)
                cc[_IDX[c]] += 1
                nxt[(tuple(cc), _pmul(P, _LETTER[c]))] += w
        closed = defaultdict(lambda: defaultdict(int))
        keep = {}
        for (counts, P), w in nxt.items():
            if _balanced(counts):
                closed[counts][P] += w
                if not prime_only:
                    keep[(counts, P)] = w
            else:
                keep[(counts, P)] = w
        out[L] = closed
        layer = keep
    return out


def sign_of(P):
    k, p = P
    assert p == 0 and k in (0, 2), f"fold not +-I: {P}"
    return 1 if k == 0 else -1


def is_prime(word):
    cnt = defaultdict(int)
    for i, c in enumerate(word[:-1]):
        cnt[c] += 1
        if all(cnt[a] == cnt[b] for a, b in _AXES):
            return False
    return True


def alpha_inv(f):
    N = len(f) - 1
    I = [Fr(0)] + [2 * comb(2 * n - 2, n - 1) // n * f[n] for n in range(1, N + 1)]
    G = [Fr(1)] + [Fr(0)] * N
    for n in range(1, N + 1):
        G[n] = sum(I[k] * G[n - k] for k in range(1, n + 1))
    return 137 + sum(G[n] * X ** (n - 1) for n in range(2, N + 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--max-n', type=int, default=7)
    N = ap.parse_args().max_n
    assert set(_LETTERS) == set(PAULI_MAP)

    print("Q0  method")
    allw = census(8, prime_only=False)
    tot = [sum(sum(d.values()) for d in allw[L].values()) for L in (2, 4, 6, 8)]
    print(f"    balanced words, lengths 2-8: {tot}  (sec 43: [8, 168, 5120, 190120])")
    assert tot == [8, 168, 5120, 190120]
    rng = random.Random(46)
    checked = 0
    while checked < 3000:
        n = rng.randint(1, 5)
        word = []
        for _ in range(n):
            a, b = rng.choice(_AXES)
            word += [a, b]
        rng.shuffle(word)
        w = ''.join(word)
        if not is_prime(w):
            continue
        P = (0, 0)
        for c in w:
            P = _pmul(P, _LETTER[c])
        m = pauli_fold(w)
        ref = 1 if abs(m[0] - 1) < 1e-9 else (-1 if abs(m[0] + 1) < 1e-9 else 0)
        assert abs(m[1]) < 1e-9 and abs(m[2]) < 1e-9 and abs(m[0] - m[3]) < 1e-9 and ref == sign_of(P), w
        checked += 1
    print(f"    {checked} sampled prime words agree with pauli_fold")
    cap = alpha_inv([Fr(1)] * (N + 1))
    print(f"    f_n = 1: alpha^-1 = {float(cap):.6f}  (cap 137.048130)")

    print("\nQ2  prime survival by order")
    pr = census(2 * N, prime_only=True)
    f = [Fr(1)]
    print(f"    {'n':>2} {'P_n':>14} {'K_n':>14} {'f_n':>22} {'global |sum S|/P_n':>20} {'multisets':>9}")
    for n in range(1, N + 1):
        d = pr[2 * n]
        P = K = Sg = 0
        for counts, folds in d.items():
            S = sum(sign_of(Pp) * w for Pp, w in folds.items())
            P += sum(folds.values())
            K += abs(S)
            Sg += S
        fn = Fr(K, P)
        f.append(fn)
        print(f"    {n:>2} {P:>14} {K:>14} {str(fn):>14} = {float(fn):.5f} {abs(Sg) / P:>20.5f} {len(d):>9}")
    assert f[1] == 1 and f[2] == Fr(7, 13), "hand count of sec 46"

    a = alpha_inv(f)
    irr = 263 - 16 * 62 ** 0.5   # irreducible cap, Alpha_Residual sec 1
    capf = float(cap)
    w_eq = (float(a) - irr) / (capf - irr)
    print("\nQ1  alpha")
    print(f"    alpha^-1 = {float(a):.6f}   CODATA {CODATA:.6f}   diff {float(a) - CODATA:+.6f}")
    print(f"    w = 1/2 gives {W_HALF:.6f}, diff {W_HALF - CODATA:+.6f}")
    print(f"    equivalent w = {w_eq:.4f}  (measured 0.6239); overshoot removed: "
          f"{(capf - float(a)) / (capf - CODATA):.1%}")
    ok = abs(float(a) - CODATA) < 0.0040
    print(f"    Q1: {'PASS' if ok else 'FAIL'}  (pass iff |diff| < 0.0040)")


if __name__ == '__main__':
    main()
