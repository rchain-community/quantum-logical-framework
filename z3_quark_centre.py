#!/usr/bin/env python3
"""
z3_quark_centre.py -- the quark centre Z3 on the closure graph, and transient quark pairs.
The pre-registered test of Carbon_Superconductivity.md sec 20 (frozen in 8fcd9b7).

  C1 (stdlib)  qutrit toric code on an L x L torus, oriented edges: vertex A_v = Z on out-edges, Z^-1 on in-edges;
               plaquette B_p = X around the circulation, X^-1 against it. Ground state is a stabilizer state, so
               S_A = (rank_GF(3)(G|_A) - |A|) log 3; gamma by Kitaev-Preskill. Control: a product state.
  C2 (numpy)   divergence-free Z3 flows on the edges, weight w per nonzero edge (the high-temperature expansion of the
               3-state Potts model); exact transfer matrices; R3 = Z(x-flux 1) / Z(x-flux 0), y-flux 0.
  P  (numpy)   the Z2 loop gas with open ends: fugacity t per odd-degree vertex (= the Ising model in a field,
               tanh h = t). Pair susceptibility chi = (d^2 ln Z / dt^2) / N, its maximum over w, for L = 4, 6, 8.

Run:  python3 z3_quark_centre.py      (C1 always; C2 and P if numpy is available)
"""
from __future__ import annotations

import math

from z2_topological_entropy import kp_regions


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# C1: qutrit toric code
# --------------------------------------------------------------------------- #
def z3_toric(L: int):
    """Generators as lists of length 2n over GF(3): (x_0..x_{n-1}, z_0..z_{n-1})."""
    E, mids = {}, []
    for i in range(L):
        for j in range(L):
            E[('h', i, j)] = len(mids); mids.append((i + 0.5, j))
            E[('v', i, j)] = len(mids); mids.append((i, j + 0.5))
    n = len(mids)
    gens = []
    for i in range(L):
        for j in range(L):
            g = [0] * (2 * n)
            for e, c in ((E[('h', i, j)], 1), (E[('v', i, j)], 1),                 # out-edges: Z
                         (E[('h', (i - 1) % L, j)], 2), (E[('v', i, (j - 1) % L)], 2)):   # in-edges: Z^-1
                g[n + e] = (g[n + e] + c) % 3
            gens.append(g)
    for i in range(L):
        for j in range(L):
            g = [0] * (2 * n)
            for e, c in ((E[('h', i, j)], 1), (E[('v', (i + 1) % L, j)], 1),       # with the circulation: X
                         (E[('h', i, (j + 1) % L)], 2), (E[('v', i, j)], 2)):       # against it: X^-1
                g[e] = (g[e] + c) % 3
            gens.append(g)
    # logical Z loops, to fix one ground state. They must cut ACROSS edges (dual paths): Z on the vertical edges of a
    # row and on the horizontal edges of a column, so each plaquette meets them in two edges whose X powers sum to 3.
    for loop in ([E[('v', i, 0)] for i in range(L)], [E[('h', 0, j)] for j in range(L)]):
        g = [0] * (2 * n)
        for e in loop:
            g[n + e] = 1
        gens.append(g)
    return gens, mids, n


def symplectic(a, b, n):
    return (sum(a[k] * b[n + k] - a[n + k] * b[k] for k in range(n))) % 3


def rank_gf3(rows):
    rows = [r[:] for r in rows]
    rank, col = 0, 0
    ncol = len(rows[0]) if rows else 0
    while rank < len(rows) and col < ncol:
        piv = next((r for r in range(rank, len(rows)) if rows[r][col] % 3), None)
        if piv is None:
            col += 1
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        inv = 1 if rows[rank][col] == 1 else 2                 # inverse mod 3
        rows[rank] = [(x * inv) % 3 for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col]:
                f = rows[r][col]
                rows[r] = [(x - f * y) % 3 for x, y in zip(rows[r], rows[rank])]
        rank += 1
        col += 1
    return rank


def entropy_log3(gens, region, n):
    idx = sorted(region)
    rows = [[g[e] for e in idx] + [g[n + e] for e in idx] for g in gens]
    return rank_gf3(rows) - len(idx)


def c1():
    rule("C1  THE QUTRIT (Z3) TORIC CODE: gamma in units of log 3")
    for L in (6, 8):
        gens, mids, n = z3_toric(L)
        assert all(symplectic(a, b, n) == 0 for a in gens for b in gens), "generators must commute"
        full = rank_gf3(gens)
        for radius in (2.5, (L - 2) / 2):
            A, B, C = kp_regions(mids, L, radius)
            S = lambda R: entropy_log3(gens, R, n)
            g = -(S(A) + S(B) + S(C) - S(A | B) - S(B | C) - S(C | A) + S(A | B | C))
            print(f"  L = {L}: generators commute, rank {full} = n = {n} (pure state); radius {radius}: "
                  f"gamma = {g} x log 3")
    gens, mids, n = z3_toric(8)
    prod = []
    for e in range(n):
        g = [0] * (2 * n)
        g[n + e] = 1
        prod.append(g)
    A, B, C = kp_regions(mids, 8, 3.0)
    S = lambda R: entropy_log3(prod, R, n)
    g0 = -(S(A) + S(B) + S(C) - S(A | B) - S(B | C) - S(C | A) + S(A | B | C))
    print(f"  control, product state (L = 8, radius 3): gamma = {g0}")


# --------------------------------------------------------------------------- #
# C2: Z3 flow gas
# --------------------------------------------------------------------------- #
def z3_sectors(L: int, w: float, np):
    n = 3 ** L

    def digits(k):
        return [(k // 3 ** j) % 3 for j in range(L)]

    def number(d):
        return sum(x * 3 ** j for j, x in enumerate(d))

    D = [digits(k) for k in range(n)]
    nz = [sum(1 for x in d if x) for d in D]
    T = np.zeros((3 * n, 3 * n))
    for h_in in range(n):
        hi = D[h_in]
        for v in range(n):
            vd = D[v]
            ho = [(hi[j] + vd[(j - 1) % L] - vd[j]) % 3 for j in range(L)]
            k = number(ho)
            wt = w ** (nz[v] + nz[k])
            dy = vd[L - 1]
            for y in range(3):
                T[3 * k + (y + dy) % 3, 3 * h_in + y] += wt
    M = np.linalg.matrix_power(T, L)
    Z = {}
    for h in range(n):
        fx = sum(D[h]) % 3
        Z[fx] = Z.get(fx, 0.0) + M[3 * h + 0, 3 * h + 0]          # y-flux 0 at start and end
    return Z


def c2(np):
    rule("C2  Z3 DECONFINEMENT: R3 = Z(x-flux 1) / Z(x-flux 0), exact transfer matrices")
    ws = [0.20, 0.30, 0.34, 0.366, 0.40, 0.50, 0.70, 1.0]
    Ls = (3, 4, 5, 6)
    print(f"  {'w':>7}" + "".join(f"{'L=' + str(L):>11}" for L in Ls))
    for w in ws:
        row = []
        for L in Ls:
            Z = z3_sectors(L, w, np)
            row.append(Z[1] / Z[0])
        print(f"  {w:>7.3f}" + "".join(f"{r:>11.5f}" for r in row))
    f = lambda w: (lambda a, b: a[1] / a[0] - b[1] / b[0])(z3_sectors(6, w, np), z3_sectors(4, w, np))
    lo, hi = 0.30, 0.45
    for _ in range(14):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if f(lo) * f(m) <= 0 else (m, hi)
    ws_ = (lo + hi) / 2
    print(f"\n  crossing of L = 4 and L = 6:  w* = {ws_:.4f}   predicted 1/(1+sqrt3) = {1 / (1 + math.sqrt(3)):.4f}"
          f"   ({100 * abs(ws_ - 1 / (1 + math.sqrt(3))) / (1 / (1 + math.sqrt(3))):.1f} %)")
    return ws_


# --------------------------------------------------------------------------- #
# P: transient pairs
# --------------------------------------------------------------------------- #
def lnZ_open(L: int, w: float, t: float, np):
    """Z2 loop gas with open ends: weight w per occupied edge, t per odd-degree vertex. Periodic torus."""
    n = 1 << L
    full = n - 1
    pc = np.array([bin(k).count("1") for k in range(n)])
    hin = np.arange(n)[None, :]
    hout = np.arange(n)[:, None]
    T = np.zeros((n, n))
    for v in range(n):
        rv = ((v << 1) | (v >> (L - 1))) & full
        odd = (hin ^ hout ^ v ^ rv)                       # vertices whose degree is odd
        T += (w ** (pc[v] + pc[hout])) * (t ** pc[odd]) if t > 0 else \
            (w ** (pc[v] + pc[hout])) * (pc[odd] == 0)
    ev = np.linalg.eigvals(T)
    return math.log(abs(np.sum(ev ** L).real))


def pair_chi(L, w, t, np, d=1e-3):
    N = L * L
    if t == 0:
        return 2 * (lnZ_open(L, w, d, np) - lnZ_open(L, w, 0.0, np)) / d ** 2 / N
    return (lnZ_open(L, w, t + d, np) - 2 * lnZ_open(L, w, t, np) + lnZ_open(L, w, t - d, np)) / d ** 2 / N


def p_test(np):
    rule("P  TRANSIENT PAIRS: open ends with fugacity t (= Ising in a field); pair susceptibility peak")
    ws = [0.05 * k for k in range(1, 21)]          # the full range 0.05 - 1.0
    print(f"  {'t':>6}" + "".join(f"{'chi_max L=' + str(L):>16}" for L in (4, 6, 8)) + f"{'ratio 8/4':>12}{'peak w (L=8)':>15}")
    out = {}
    for t in (0.0, 0.05, 0.1, 0.2):
        peaks = []
        wpk = None
        for L in (4, 6, 8):
            vals = [(pair_chi(L, w, t, np), w) for w in ws]
            m, wm = max(vals)
            peaks.append(m)
            if L == 8:
                wpk = wm
        out[t] = peaks[2] / peaks[0]
        print(f"  {t:>6.2f}" + "".join(f"{p:>16.3f}" for p in peaks) + f"{peaks[2] / peaks[0]:>12.2f}{wpk:>15.2f}")
    return out


if __name__ == "__main__":
    c1()
    try:
        import numpy as np
    except ImportError:
        print("\n  numpy not available: C2 and P skipped")
    else:
        c2(np)
        p_test(np)
