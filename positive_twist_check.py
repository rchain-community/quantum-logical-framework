#!/usr/bin/env python3
"""
positive_twist_check.py -- the signed censuses of secs 22-23 through their positive-weight spin models
(Carbon_Superconductivity.md sec 23a, statistic fixed in 878a862).

The signed Z2 loop gas (QLF_EdgeSign holonomy, pi flux) is the high-temperature expansion of the fully frustrated
Ising model (bonds K eta_e, tanh K = w); the signed Z3 flow gas (flux 2 pi/3) is that of the 3-state Potts model in a
gauge field (x = (e^K - 1)/(e^K + 2)). Their Boltzmann weights are positive, so nothing cancels. Confinement test:
rho = Z_twisted / Z_periodic -> 1 (spin model disordered = loop gas confined), -> 0 (ordered = deconfined).
Validation: the unsigned (ferromagnetic) models must cross at sqrt2 - 1 and 1/(1+sqrt3).

Run:  python3 positive_twist_check.py        (needs numpy)
"""
from __future__ import annotations

import math


def z2_rho(L: int, w: float, frustrated: bool, np) -> float:
    """L x L torus, L even. Spins on vertices; rows j, columns c. Vertical bonds K; horizontal bonds K (-1)^j if
    frustrated (QLF_EdgeSign: an x-edge at row y carries (-1)^y), else K. Twist: horizontal bonds across one seam
    flipped."""
    K = math.atanh(w)
    n = 1 << L
    S = np.array([[1 if (s >> j) & 1 else -1 for j in range(L)] for s in range(n)], dtype=float)   # n x L
    hsgn = np.array([(-1) ** j if frustrated else 1 for j in range(L)], dtype=float)
    vert = np.exp(K * np.sum(S * np.roll(S, -1, axis=1), axis=1))                                   # within column
    H = np.exp(K * (S * hsgn) @ S.T)                                                                 # H[s, s']
    Htw = np.exp(-K * (S * hsgn) @ S.T)
    T = (H * vert[None, :]).T              # T[s', s] = H[s, s'] * vert[s']
    Ttw = (Htw * vert[None, :]).T
    scale = T.max()
    T, Ttw = T / scale, Ttw / scale
    P = np.linalg.matrix_power(T, L - 1)
    return float(np.trace(Ttw @ P) / np.trace(T @ P))


def z3_rho(L: int, x: float, frustrated: bool, np, M: int | None = None) -> float:
    """L rows x M columns (M multiple of 3). Potts spins; horizontal bonds exp(K delta(t' - t)); vertical bonds in
    column c exp(K delta(t_{j+1} - t_j - A_c)), A_c = c mod 3 if frustrated (flux 1 per plaquette), else 0.
    Twist: horizontal bonds across one seam shifted by 1."""
    M = M or 3 * L
    K = math.log((1 + 2 * x) / (1 - x))
    n = 3 ** L
    D = np.array([[(k // 3 ** j) % 3 for j in range(L)] for k in range(n)])
    eK = math.exp(K)
    # horizontal: H[t, t'] = prod_j exp(K delta(t'_j - t_j - shift))
    def hmat(shift):
        diff = (D[None, :, :] - D[:, None, :] - shift) % 3        # [t, t', j]
        return np.prod(np.where(diff == 0, eK, 1.0), axis=2)
    H0, H1 = hmat(0), hmat(1)
    def vvec(a):
        d = (np.roll(D, -1, axis=1) - D - a) % 3
        return np.prod(np.where(d == 0, eK, 1.0), axis=1)
    Ts, Tws = [], []
    for c in range(3):
        a = c if frustrated else 0
        v = vvec(a)
        Ts.append((H0 * v[None, :]).T)
        Tws.append((H1 * v[None, :]).T)
    scale = max(T.max() for T in Ts)
    Ts = [T / scale for T in Ts]
    Tws = [T / scale for T in Tws]
    # product over columns c = 0 .. M-1 (column c uses Ts[c % 3]); the twist sits on the last step
    P = np.eye(n)
    for c in range(M - 1):
        P = Ts[c % 3] @ P
    num = np.trace(Tws[(M - 1) % 3] @ P)
    den = np.trace(Ts[(M - 1) % 3] @ P)
    return float(num / den)


def crossing(f, La, Lb, lo, hi, it=30):
    g = lambda w: f(Lb, w) - f(La, w)
    for _ in range(it):
        m = (lo + hi) / 2
        lo, hi = (lo, m) if g(lo) * g(m) <= 0 else (m, hi)
    return (lo + hi) / 2


def main():
    import numpy as np
    ws = [0.3, 0.414, 0.5, 0.7, 0.9]
    print("VALIDATION on the unsigned models (rho -> 0 ordered/deconfined, -> 1 disordered/confined)")
    c2 = crossing(lambda L, w: z2_rho(L, w, False, np), 6, 10, 0.3, 0.55)
    c3 = crossing(lambda L, x: z3_rho(L, x, False, np), 4, 6, 0.3, 0.45)
    print(f"  Z2 ferromagnet: rho curves L = 6, 10 cross at w = {c2:.4f}   (sqrt2 - 1 = {math.sqrt(2) - 1:.4f})")
    print(f"  Z3 Potts:       rho curves L = 4, 6 cross at x = {c3:.4f}   (1/(1+sqrt3) = {1 / (1 + math.sqrt(3)):.4f})")

    print("\nZ2 fully frustrated (the signed census of sec 22): rho = Z_twist / Z_periodic, L x L")
    Ls2 = (4, 6, 8, 10)
    print(f"  {'w':>6}" + "".join(f"{'L=' + str(L):>11}" for L in Ls2) + f"{'trend':>9}")
    for w in ws:
        row = [z2_rho(L, w, True, np) for L in Ls2]
        print(f"  {w:>6.3f}" + "".join(f"{r:>11.5f}" for r in row) + f"{('falls' if row[-1] < row[0] - 1e-9 else 'holds'):>9}")

    print("\nZ3 Potts with flux 2 pi/3 (the signed census of sec 23): rho = Z_twist / Z_periodic, L x 3L")
    Ls3 = (3, 4, 5, 6)
    print(f"  {'x':>6}" + "".join(f"{'L=' + str(L):>11}" for L in Ls3) + f"{'trend':>9}")
    for x in ws:
        row = [z3_rho(L, x, True, np) for L in Ls3]
        print(f"  {x:>6.3f}" + "".join(f"{r:>11.5f}" for r in row) + f"{('falls' if row[-1] < row[0] - 1e-9 else 'holds'):>9}")
    print("\n  for comparison, unsigned Z3 Potts at the same sizes:")
    for x in ws:
        row = [z3_rho(L, x, False, np) for L in Ls3]
        print(f"  {x:>6.3f}" + "".join(f"{r:>11.5f}" for r in row))


if __name__ == "__main__":
    main()
