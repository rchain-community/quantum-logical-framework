#!/usr/bin/env python3
"""
borromean_colour_weight.py -- the cost of a colour step (Carbon_Superconductivity.md sec 21, frozen in 992cd72).

Assumption A: a gauge line on k of the substrate's axes has per-step weight p_k, the probability that the walk on
those axes ever closes (Polya). Confined iff p_k < 1/(1+sqrt N), N the centre order (sec 19-20).

  F1 (stdlib)  QLF's own count: the cylinder mass of first closures on the three-axis alphabet (6 twists),
               sum over first-closure words of 6^-|w|, from exact closed-word counts, the renewal relation, and a
               tail fit -- as Closure_Walk.md does for p4. Cross-checked against brute-force enumeration with
               twist_core.is_zfa for short words.
  F2 (numpy)   R3 = Z(x-flux 1)/Z(x-flux 0) of the Z3 flow gas at w = p3, L = 3-6 (z3_quark_centre.py).

Run:  python3 borromean_colour_weight.py
"""
from __future__ import annotations

import itertools
import math

from twist_core import is_zfa

AX3 = ['>', '<', '^', 'v', '/', '\\']          # the three spatial axes, both signs


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def closed_words_3axis(n: int) -> int:
    """Number of closed (count-balanced) words of length 2n over the six spatial twists:
    sum over i + j + k = n of (2n)! / (i! i! j! j! k! k!)."""
    f = math.factorial
    tot = 0
    for i in range(n + 1):
        for j in range(n - i + 1):
            k = n - i - j
            tot += f(2 * n) // (f(i) ** 2 * f(j) ** 2 * f(k) ** 2)
    return tot


def f1(N: int = 400):
    rule("F1  QLF's COUNT OF FIRST CLOSURES ON THREE AXES")
    # brute-force cross-check with the substrate's own closure test
    for L in (2, 4, 6):
        brute = sum(1 for w in itertools.product(AX3, repeat=L) if is_zfa(''.join(w), min_length=2))
        assert brute == closed_words_3axis(L // 2), (L, brute)
    print("  closed-word counts 6, 90, 1860 (lengths 2, 4, 6) agree with brute force over is_zfa")
    # u_n = closed / 6^{2n} (cylinder mass of closed words of length 2n), exact rationals then floats
    u = [1.0] + [closed_words_3axis(n) / 6 ** (2 * n) for n in range(1, N + 1)]
    # first closures by renewal: u_n = sum_{k=1}^{n} f_k u_{n-k}
    f = [0.0] * (N + 1)
    for n in range(1, N + 1):
        f[n] = u[n] - sum(f[k] * u[n - k] for k in range(1, n))
    P = []
    acc = 0.0
    for n in range(1, N + 1):
        acc += f[n]
        P.append(acc)
    # tail: f_n ~ n^{-3/2}, so P(N) = p - a N^{-1/2} - b N^{-1}; fit through three N
    pts = [(N // 2, P[N // 2 - 1]), (3 * N // 4, P[3 * N // 4 - 1]), (N, P[N - 1])]
    # solve p - a x - b y = P for (p, a, b), x = N^{-1/2}, y = 1/N
    A = [[1, -n ** -0.5, -1 / n] for n, _ in pts]
    bvec = [v for _, v in pts]
    # Cramer's rule
    def det3(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    D = det3(A)
    Ap = [[bvec[r]] + A[r][1:] for r in range(3)]
    p_fit = det3(Ap) / D
    G = math.gamma
    u3 = math.sqrt(6) / (32 * math.pi ** 3) * G(1 / 24) * G(5 / 24) * G(7 / 24) * G(11 / 24)
    p_watson = 1 - 1 / u3
    print(f"  partial sums of the first-closure mass:  P(100) = {P[99]:.6f}   P(200) = {P[199]:.6f}   P({N}) = {P[-1]:.6f}")
    print(f"  tail fit p - a N^-1/2 - b N^-1 through N = {N // 2}, {3 * N // 4}, {N}:  p3 = {p_fit:.6f}")
    print(f"  Polya / Watson:  p3 = 1 - 1/u3 = {p_watson:.6f}   (difference {abs(p_fit - p_watson):.2e})")
    return p_fit, p_watson


def f2(p3):
    rule("F2  THE Z3 FLOW GAS AT w = p3")
    try:
        import numpy as np
        from z3_quark_centre import z3_sectors
    except ImportError:
        print("  numpy not available: F2 skipped")
        return None
    row = []
    for L in (3, 4, 5, 6):
        Z = z3_sectors(L, p3, np)
        row.append(Z[1] / Z[0])
    print("  R3(w = p3):  " + "   ".join(f"L={L}: {r:.5f}" for L, r in zip((3, 4, 5, 6), row)))
    falling = all(a > b for a, b in zip(row, row[1:]))
    print(f"  falls with L: {falling}  ->  {'confined' if falling else 'NOT confined at these sizes'}"
          f"   (threshold 1/(1+sqrt3) = {1 / (1 + math.sqrt(3)):.4f}; p3 is {100 * (1 - p3 * (1 + math.sqrt(3))):.1f} % below)")
    return row


def f3(p3):
    rule("F3  THE CLASSIFICATION (not blind: p3 was known)")
    rows = [("electromagnetism", "gauge axis", 1, "U(1)", float("inf")),
            ("weak isospin", "three spatial axes", 3, "Z2", 2),
            ("colour", "three spatial axes", 3, "Z3", 3)]
    p = {1: 1.0, 2: 1.0, 3: p3, 4: 0.19320}
    for name, ax, k, cen, N in rows:
        thr = 0.0 if N == float("inf") else 1 / (1 + math.sqrt(N))
        conf = p[k] < thr
        print(f"  {name:<18}{ax:<20} p_{k} = {p[k]:.4f}   threshold {thr:.4f}   -> "
              f"{'confined / screened' if conf else 'deconfined (long range)'}")


if __name__ == "__main__":
    pf, pw = f1()
    f2(pw)
    f3(pw)
