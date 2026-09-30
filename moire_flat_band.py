#!/usr/bin/env python3
"""
moire_flat_band.py -- extension point 2 of moire_zfa_dna.py: the flat band as a signed count.

In the continuum model of twisted bilayer graphene (Bistritzer & MacDonald 2011) a Dirac state of layer 1 at
momentum p hops to layer 2 at p + q_j (j = 1, 2, 3; three vectors at 120 deg), and back by -q_j. The momentum
states and hops form a two-layer graph in which every step alternates layer: layer 1 -> 2 is a "+" step along
one of three axes, 2 -> 1 a "-" step. That is the alternating three-axis slab of carbon_zfa_dna.py sec 1 --
the momentum lattice of the moire IS the honeycomb of sign-alternating twists, and every closed hopping path is
an alternating ZFA word. Each hop carries a Pauli-valued amplitude T_j = w1 (sigma_x cos phi_j + sigma_y sin phi_j),
phi_j = 2 pi (j - 1)/3 (chiral limit, w0 = 0: Tarnopolsky, Kruchkov & Vishwanath 2019).

The Dirac velocity at the moire K point is then a sum over closed words, with signs from those Pauli phases:
   v*/v = 1 - 3 alpha^2 + ...      (alpha = w1 / (v k_theta))
the "1" being the empty word and "-3 alpha^2" the three words up-and-back. The magic angle is where the signed
sum cancels, v* = 0: the band goes flat.

  sec 1  capacity R = the longest word kept (the momentum ball of walk radius R). Compute v*(alpha) exactly
         within it, and the first zero alpha_1(R). R = 1 is the up-and-back words only.
  sec 2  convergence with R to the known first magic value, alpha_1 = 0.586 (Tarnopolsky et al.), and the
         second, 2.221.
  sec 3  the conversion to a twist angle, and the multilayer family (alpha_eff = 2 cos(pi/(n+1)) alpha).
  sec 4  what it gives the coupling J, and what it does not.

Stdlib only (complex LU in pure Python).   Run:  python3 moire_flat_band.py        (~1 min)
"""
from __future__ import annotations

import cmath
import math

S3 = math.sqrt(3)
Q = [complex(0, -1), complex(S3 / 2, 0.5), complex(-S3 / 2, 0.5)]      # q_1, q_2, q_3 in units of k_theta
PHI = [2 * math.pi * j / 3 for j in range(3)]


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def momentum_ball(R: int):
    """Sites reachable from the layer-1 origin in <= R alternating steps: (position, layer). The walk graph."""
    key = lambda p: (round(p.real, 6), round(p.imag, 6))
    sites = {key(0j): (0j, 1)}
    frontier = [(0j, 1)]
    edges = []
    for _ in range(R):
        nxt = []
        for p, layer in frontier:
            for j in range(3):
                q = p + Q[j] if layer == 1 else p - Q[j]
                k = key(q)
                if k not in sites:
                    sites[k] = (q, 3 - layer)
                    nxt.append((q, 3 - layer))
        frontier = nxt
    idx = {k: i for i, k in enumerate(sites)}
    lst = list(sites.values())
    for k, (p, layer) in sites.items():
        if layer != 1:
            continue
        for j in range(3):
            k2 = key(p + Q[j])
            if k2 in idx:
                edges.append((idx[k], idx[k2], j))      # layer-1 site -> layer-2 site by +q_j
    return lst, edges


def build_D(sites, edges, alpha):
    """Chiral block D (B <- A): diagonal p_x + i p_y (Dirac), off-diagonal alpha e^{i phi_j} both ways."""
    n = len(sites)
    D = [[0j] * n for _ in range(n)]
    for i, (p, _) in enumerate(sites):
        D[i][i] = complex(p.real, p.imag)
    for a, b, j in edges:
        amp = alpha * cmath.exp(1j * PHI[j])
        D[b][a] += amp
        D[a][b] += amp
    return D


def lu(M):
    n = len(M)
    A = [row[:] for row in M]
    piv = list(range(n))
    for k in range(n):
        m = max(range(k, n), key=lambda i: abs(A[i][k]))
        if abs(A[m][k]) < 1e-300:
            A[m][k] = 1e-300
        if m != k:
            A[k], A[m] = A[m], A[k]
            piv[k], piv[m] = piv[m], piv[k]
        inv = 1 / A[k][k]
        rk = A[k]
        for i in range(k + 1, n):
            f = A[i][k] * inv
            if f != 0:
                A[i][k] = f
                ri = A[i]
                for c in range(k + 1, n):
                    ri[c] -= f * rk[c]
    return A, piv


def solve(LU, piv, b):
    """Solve M x = b."""
    n = len(LU)
    y = [b[piv[i]] for i in range(n)]
    for i in range(n):
        s = y[i]
        row = LU[i]
        for c in range(i):
            s -= row[c] * y[c]
        y[i] = s
    for i in range(n - 1, -1, -1):
        s = y[i]
        row = LU[i]
        for c in range(i + 1, n):
            s -= row[c] * y[c]
        y[i] = s / row[i]
    return y


def solve_h(LU, piv, b):
    """Solve M^dagger x = b using M's LU (P M = L U  =>  M^dag = U^dag L^dag P)."""
    n = len(LU)
    z = b[:]
    for i in range(n):                         # U^dag z' = b  (lower triangular)
        s = z[i]
        for c in range(i):
            s -= LU[c][i].conjugate() * z[c]
        z[i] = s / LU[i][i].conjugate()
    for i in range(n - 1, -1, -1):             # L^dag w = z'  (upper, unit diagonal)
        s = z[i]
        for c in range(i + 1, n):
            s -= LU[c][i].conjugate() * z[c]
        z[i] = s
    x = [0j] * n
    for i in range(n):
        x[piv[i]] = z[i]
    return x


def normalise(v):
    s = math.sqrt(sum(abs(c) ** 2 for c in v))
    return [c / s for c in v]


def velocity(sites, edges, alpha, iters=6):
    """v*/v at the moire K point: the overlap <psi_B|psi_A> of the two near-zero modes of D (A: D psi = 0,
    B: D^dag psi = 0), phases fixed so that both are real-positive on the origin site. Inverse iteration."""
    D = build_D(sites, edges, alpha)
    LU, piv = lu(D)
    n = len(D)
    xa = [1.0 + 0j] + [0j] * (n - 1)
    xb = xa[:]
    for _ in range(iters):
        xa = normalise(solve(LU, piv, solve_h(LU, piv, xa)))      # (D^dag D)^-1
        xb = normalise(solve_h(LU, piv, solve(LU, piv, xb)))      # (D D^dag)^-1
    fa = xa[0] / abs(xa[0]) if abs(xa[0]) > 1e-14 else 1
    fb = xb[0] / abs(xb[0]) if abs(xb[0]) > 1e-14 else 1
    xa = [c / fa for c in xa]
    xb = [c / fb for c in xb]
    return sum(b.conjugate() * a for a, b in zip(xa, xb)).real


def first_zero(sites, edges, lo, hi, steps=24):
    """Scan for a sign change of v*, then bisect."""
    grid = [lo + (hi - lo) * k / steps for k in range(steps + 1)]
    vals = [velocity(sites, edges, a) for a in grid]
    for (a1, v1), (a2, v2) in zip(zip(grid, vals), zip(grid[1:], vals[1:])):
        if v1 * v2 < 0:
            for _ in range(22):
                m = (a1 + a2) / 2
                vm = velocity(sites, edges, m)
                if v1 * vm <= 0:
                    a2, v2 = m, vm
                else:
                    a1, v1 = m, vm
            return (a1 + a2) / 2
    return None


def sec1_2():
    rule("sec 1-2  THE MAGIC ANGLE AS THE ZERO OF A SIGNED SUM OF CLOSED WORDS")
    print("""
Capacity R keeps every momentum state within R alternating steps of the origin, i.e. every closed word of length
up to about 2R. v*(alpha) is computed exactly inside that capacity.
""")
    s1, e1 = momentum_ball(1)
    print("  R = 1 (the empty word and the three up-and-back words): v*(alpha) vs the formula (1 - 3a^2)/(1 + 3a^2)")
    for a in (1e-6, 0.3, 0.5, 1 / S3, 0.7):
        v = velocity(s1, e1, a)
        print(f"    alpha = {a:.4f}:  v* = {v:+.6f}   formula {((1 - 3 * a * a) / (1 + 3 * a * a)):+.6f}")
    print(f"  so at R = 1 the zero is alpha = 1/sqrt3 = {1 / S3:.4f}: the empty word cancels the three up-and-back words.\n")
    print(f"  {'R':>3}{'states':>8}{'alpha_1(R)':>13}{'alpha_2(R)':>13}")
    rows = []
    for R in (1, 2, 3, 4, 5, 6, 8, 10, 14, 18):
        s, e = momentum_ball(R)
        a1 = first_zero(s, e, 0.40, 0.80)
        a2 = first_zero(s, e, 1.6, 2.6, steps=20) if R >= 4 else None
        rows.append((R, len(s), a1, a2))
        print(f"  {R:>3}{len(s):>8}{a1:>13.4f}{(f'{a2:.4f}' if a2 else '-'):>13}")
    print("""
  known (Tarnopolsky, Kruchkov & Vishwanath 2019):  alpha_1 = 0.586,  alpha_2 = 2.221""")
    s2, e2 = momentum_ball(2)
    lo, hi = 0.60, 0.64
    f = lambda a: velocity(s2, e2, a, iters=12)
    for _ in range(55):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(lo) * f(mid) <= 0 else (mid, hi)
    phi_c = (math.sqrt(5) - 1) / 2
    print(f"""
  The truncated zeros are exact numbers of the finite graphs: R = 1 gives 1/sqrt3; R = 2 gives
  {(lo + hi) / 2:.16f} = 1/phi = (sqrt5 - 1)/2 = {phi_c:.16f}. These belong to the capacity-R graphs,
  not to the physical value 0.5857, which R >= 4 already reaches.""")
    global PHI
    saved = PHI
    PHI = [0.0, 0.0, 0.0]
    s1, e1 = momentum_ball(1)
    s8, e8 = momentum_ball(8)
    z0 = first_zero(s8, e8, 0.6, 1.4, steps=16)
    v_off = velocity(s1, e1, 1.0)
    PHI = saved
    print(f"""
  Without the phases (all phi_j = 0), R = 1 gives v* = 1/(1 + 3 alpha^2), e.g. {v_off:.2f} at
  alpha = 1: the up-and-back words add and never cancel. Longer words do cancel without phases, but at
  alpha = {z0:.4f}, not 0.5857. So the cube-root phases e^(i phi_j) are what make the leading order cancel, and
  they set where the full sum does.""")
    return rows


def sec3(alpha1):
    rule("sec 3  FROM alpha TO THE TWIST ANGLE, AND THE MULTILAYER FAMILY")
    a = 0.246            # nm
    for hv, w1 in ((0.5253, 0.110), (0.6582, 0.110)):   # hbar v in eV nm (v = 0.8e6 and 1.0e6 m/s)
        s = w1 * 3 * a / (8 * math.pi * hv * alpha1)
        th = 2 * math.degrees(math.asin(s))
        print(f"  hbar v = {hv:.4f} eV nm, w1 = {w1 * 1000:.0f} meV:  theta_magic = {th:.3f}°")
    print("""
  alpha = w1 / (hbar v k_theta), k_theta = (8 pi / 3a) sin(theta/2). The angle depends on w1 and v, which the
  count does not supply -- the count fixes alpha_1, the dimensionless ratio.

  Multilayers (Khalaf et al. 2019): an n-layer alternating stack decouples into bilayers with alpha_eff =
  2 cos(j pi/(n+1)) alpha, so each member is flat where alpha_eff = alpha_1: the same zero of the same signed sum,
  reached at an angle sqrt2, phi, sqrt3 times larger (carbon_zfa_dna.py sec 3).""")


def sec4():
    rule("sec 4  WHAT THIS GIVES THE COUPLING J")
    print("""
Given: the magic angle as a cancellation -- the flat band is where the signed sum over closed alternating words
vanishes -- converging with capacity to the known value. The substrate reading: the "1" is the empty word, the
first correction is the three up-and-back words, and their phases e^{i phi_j} (cube roots of unity) turn that
correction negative; without them the leading order cannot cancel, and the full sum cancels at 0.781, not 0.586.

Not given: an absolute J. In a flat band the stiffness is not set by the (vanishing) band velocity but by the
band's quantum geometry times the pairing energy (Peotta & Torma 2015; Hazra, Verma & Randeria 2019). The count
here gives where the band is flat; the one-bit coupling needs the geometry of its wavefunctions (the Wannier
spread on the ODD honeycomb of moire_interlayer.py) and an interaction energy. That is the next extension.""")


if __name__ == "__main__":
    rows = sec1_2()
    sec3(rows[-1][2])
    sec4()
