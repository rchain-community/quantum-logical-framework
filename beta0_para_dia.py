#!/usr/bin/env python3
"""
beta0_para_dia.py -- the para-dia structure of beta0, and how many states a colour carrier has
(Carbon_Superconductivity.md sec 36; frozen in commit 5636e15).

Per real state of a massless carrier in a weak field: c(s_z) = -1/6 (orbital) + (g s_z)^2/2 (spin).

  B1  Is the orbital term census_split's 1/6?  Exact area moments of every count-balanced word of the
      eight-twist alphabet, projected on one spatial plane: r(L) = <A^2>/(sigma^2 L)^2, sigma^2 = 1/4.
      Passes iff 2 r = census_split(n)/n^3 = 1/6 - 1/(6 n^2) at every L, for n = L or n = in-plane steps.
  R3  The carriers' states from the fold: 24 cross-axis spatial commutator words, folds counted by Pauli.
      Three states weighted by ways -> gluon factor 7/2, beta0(nf) = 21/2 - 2 nf/3.
  V2  Running of alpha_s: PDG 2024 tau sub-average run down to m_tau with QCD (4 loops), back up with
      R3's b0 (QCD's b1..b3 kept), compared with the PDG 2024 lattice sub-average.  Pass |pull| <= 2,
      fail > 3, undecided between.  Control: QCD (R2) on the same check.

Exact arithmetic for B1 and R3 (Fractions). Stdlib only (plus twist_core for the fold).
PDG 2024 (Huston, Rabbertz, Zanderighi, QCD review sec 9.4): tau pre-average 0.1173 +- 0.0017; lattice (FLAG 2021,
adopted by PDG) 0.1184 +- 0.0008.
Run:  python3 beta0_para_dia.py --tau 0.1173 0.0017 --lat 0.1184 0.0008     (about a second)
"""
from __future__ import annotations

import argparse
import itertools
import math
from collections import defaultdict
from fractions import Fraction as Fr

from twist_core import pauli_fold

# ----------------------------------------------------------------------------- B1
# Steps on Z^4: x = > <, y = ^ v, z = / \, l = + -.  Area is taken in the (x, y) plane.
STEPS = [(1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
         (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)]


def area_moments(L: int):
    """For each even length <= L: (W, sum 2A, sum (2A)^2) over count-balanced words, and the same split by the
    number m of in-plane steps.  2A = sum (x dy - y dx) is an integer.  DP on (x, y, z, l, m) carrying
    (count, S1, S2) -- moments only, so A itself is not a state."""
    st = {(0, 0, 0, 0, 0): (1, 0, 0)}
    out = {}
    for n in range(1, L + 1):
        nxt = defaultdict(lambda: [0, 0, 0])
        for (x, y, z, l, m), (N, S1, S2) in st.items():
            rem = L - n
            for dx, dy, dz, dl in STEPS:
                X, Y, Z, Lg = x + dx, y + dy, z + dz, l + dl
                if abs(X) + abs(Y) + abs(Z) + abs(Lg) > rem:
                    continue                                # cannot return by length L
                d = x * dy - y * dx                         # increment of 2A
                key = (X, Y, Z, Lg, m + (1 if (dx or dy) else 0))
                e = nxt[key]
                e[0] += N
                e[1] += S1 + N * d
                e[2] += S2 + 2 * d * S1 + N * d * d
        st = {k: tuple(v) for k, v in nxt.items()}
        if n % 2 == 0:
            tot = [0, 0, 0]
            bym = defaultdict(lambda: [0, 0, 0])
            for (x, y, z, l, m), v in st.items():
                if x == y == z == l == 0:
                    for i in range(3):
                        tot[i] += v[i]
                        bym[m][i] += v[i]
            out[n] = (tuple(tot), {k: tuple(v) for k, v in sorted(bym.items())})
    return out


def split(n: int) -> Fr:
    """census_split(n)/n^3 = 1/6 - 1/(6 n^2)  (QLF_VacuumPolarization.splitRiemannSum_eq)."""
    return Fr(1, 6) - Fr(1, 6 * n * n)


def part1(L: int) -> None:
    print("=" * 78)
    print("B1  orbital term: area variance of closed walks vs census_split")
    print("=" * 78)
    mom = area_moments(L)
    print(f"{'L':>3} {'W_L':>16} {'<A>':>5} {'r(L)':>12} {'2r(L)':>12} {'split(L)':>12}  match n=L")
    any_L = True
    for n, ((W, S1, S2), bym) in mom.items():
        assert S1 == 0
        A2 = Fr(S2, 4 * W)                      # <A^2>, A = (2A)/2
        r = A2 / (Fr(n, 4) ** 2)
        ok = 2 * r == split(n)
        any_L &= ok
        print(f"{n:>3} {W:>16} {S1:>5} {float(r):>12.6f} {float(2 * r):>12.6f} {float(split(n)):>12.6f}  {ok}")
    print(f"limit 2r -> 1/6 = {1 / 6:.6f} (Levy area; cannot fail)")
    print(f"\nidentification n = L: exact match at every L: {any_L}")

    # n = number of in-plane steps m: the in-plane subword is a closed square-lattice walk of length m, per-axis
    # step variance 1/2, so r'(m) = <A^2 | m>/((m/2)^2).  It must not depend on L (check across L).
    print("\nidentification n = m (in-plane steps):  2 r'(m) = 2<A^2|m>/(m/2)^2  vs split(m)")
    seen = {}
    any_m = True
    for n, (_, bym) in mom.items():
        for m, (W, S1, S2) in bym.items():
            if m == 0:
                continue
            r = Fr(S2, 4 * W) / (Fr(m, 2) ** 2)
            if m in seen:
                assert seen[m] == r, "conditional area variance depends on L"
            seen[m] = r
    for m, r in sorted(seen.items()):
        ok = 2 * r == split(m)
        any_m &= ok
        print(f"  m={m:>3}  2r'={str(2 * r):>14} = {float(2 * r):.6f}   split(m)={float(split(m)):.6f}   {ok}")
    print(f"identification n = m: exact match at every m: {any_m}")
    # closed form found by the run (post hoc, recorded in sec 36a): 2 r'(m) = (1/6)(1 - 1/(m - 1)),
    # i.e. <A^2 | m> = m^2 (m - 2) / (48 (m - 1)); a 1/m correction, where census_split's is 1/m^2
    cf = all(2 * r == Fr(1, 6) * (1 - Fr(1, m - 1)) for m, r in seen.items() if m >= 2)
    print(f"closed form 2r'(m) = (1/6)(1 - 1/(m-1)) holds at every computed m: {cf}")
    # the exact form, for the record
    print("\n  exact <A^2 | m> on closed square-lattice walks:", {m: str(r * Fr(m, 2) ** 2) for m, r in sorted(seen.items())})
    print(f"\nB1: {'PASS' if (any_L or any_m) else 'FAIL'}  (n = L: {any_L}; n = m: {any_m})")


# ----------------------------------------------------------------------------- R3
VEC = {'>': (0, 1), '<': (0, 2), '^': (2, 1), 'v': (1, 2), '/': (1, 1), '\\': (2, 2)}   # QLF_ColourFlux.colVec
AXIS = {'>': 'x', '<': 'x', '^': 'y', 'v': 'y', '/': 'z', '\\': 'z'}
C_A = 3


def which_pauli(w: str) -> str:
    a, b, c, d = pauli_fold(w)
    tol = 1e-12
    if abs(b) < tol and abs(c) < tol and abs(a + d) < tol:
        return 'z'
    if abs(a) < tol and abs(d) < tol and abs(b - c) < tol:
        return 'x'
    if abs(a) < tol and abs(d) < tol and abs(b + c) < tol:
        return 'y'
    return 'scalar'


def gluon_factor(states):
    """sum over states of -1/6 + (g s_z)^2/2 with g = 2."""
    return sum(-Fr(1, 6) + Fr((2 * s) ** 2, 2) for s in states)


def beta0(gf, nf):
    return gf * C_A - Fr(2, 3) * nf


def part2():
    print("\n" + "=" * 78)
    print("R3  the carriers' states from the fold")
    print("=" * 78)
    words = [t + u for t, u in itertools.product(VEC, repeat=2) if AXIS[t] != AXIS[u]]
    assert all(((VEC[w[0]][0] + VEC[w[1]][0]) % 3, (VEC[w[0]][1] + VEC[w[1]][1]) % 3) != (0, 0) for w in words)
    cnt = defaultdict(list)
    for w in words:
        cnt[which_pauli(w)].append(w)
    print(f"cross-axis spatial commutator words: {len(words)}")
    for k in ('x', 'y', 'z', 'scalar'):
        print(f"  fold to sigma_{k}: {len(cnt[k]):>2}  {' '.join(cnt[k])}")
    third = all(which_pauli(w) == ({'x', 'y', 'z'} - {AXIS[w[0]], AXIS[w[1]]}).pop() for w in words)
    print(f"  each folds to the third axis: {third}")
    # with the field along z: sigma_x, sigma_y carriers combine to s_z = +-1, sigma_z carrier has s_z = 0
    w3 = {k: Fr(len(cnt[k]), len(words)) for k in 'xyz'}
    print(f"  ways weights: {w3}")
    gf3 = gluon_factor([1, -1, 0])
    gf2 = gluon_factor([1, -1])
    print(f"\nR3 gluon factor 3(-1/6) + (4+4+0)/2 = {gf3}   R2 (QCD) = {gf2}")
    rows = {}
    for nf in (3, 4, 5, 6):
        rows[nf] = (beta0(gf3, nf), beta0(gf2, nf))
        print(f"  beta0(nf={nf}):  R3 = {rows[nf][0]} = {float(rows[nf][0]):.4f}   QCD = {rows[nf][1]}")
    d5 = (rows[5][0] - rows[5][1]) / rows[5][1]
    print(f"V1 (within 10 % at nf=5; not blind): R3 deviation {float(d5):+.2%} -> {'pass' if abs(d5) <= Fr(1, 10) else 'fail'}")
    return gf3, gf2


# ----------------------------------------------------------------------------- V2
ZETA3 = 1.2020569031595942


def betas(nf, b0_override=None):
    """beta coefficients for a = alpha_s/pi:  da/dlnmu^2 = -sum_i beta_i a^{i+2}."""
    b0 = (11 - 2 * nf / 3) / 4 if b0_override is None else b0_override / 4
    b1 = (102 - 38 * nf / 3) / 16
    b2 = (2857 / 2 - 5033 * nf / 18 + 325 * nf ** 2 / 54) / 64
    b3 = (149753 / 6 + 3564 * ZETA3 - (1078361 / 162 + 6508 * ZETA3 / 27) * nf
          + (50065 / 162 + 6472 * ZETA3 / 81) * nf ** 2 + 1093 * nf ** 3 / 729) / 256
    return b0, b1, b2, b3


def run(alpha, mu0, mu1, nf, b0_override=None, steps=4000):
    """RK4 in t = ln mu^2."""
    bs = betas(nf, b0_override)
    f = lambda a: -sum(b * a ** (i + 2) for i, b in enumerate(bs))
    a = alpha / math.pi
    t0, t1 = math.log(mu0 ** 2), math.log(mu1 ** 2)
    h = (t1 - t0) / steps
    for _ in range(steps):
        k1 = f(a); k2 = f(a + h * k1 / 2); k3 = f(a + h * k2 / 2); k4 = f(a + h * k3)
        a += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return a * math.pi


def evolve(alpha, mu0, mu1, b0fn=None):
    """Between m_tau (nf=4) and M_Z (nf=5), threshold at m_b(m_b), continuous matching."""
    MB = 4.18
    b4 = None if b0fn is None else b0fn(4)
    b5 = None if b0fn is None else b0fn(5)
    if mu0 > mu1:                                   # down: nf=5 to MB, nf=4 below
        a = run(alpha, mu0, MB, 5, b5)
        return run(a, MB, mu1, 4, b4)
    a = run(alpha, mu0, MB, 4, b4)
    return run(a, MB, mu1, 5, b5)


def part3(gf3, tau, lat):
    print("\n" + "=" * 78)
    print("V2  running of alpha_s: tau sub-average vs lattice sub-average (PDG 2024)")
    print("=" * 78)
    MZ, MTAU = 91.1876, 1.77686
    (at, st), (al, sl) = tau, lat
    b0r3 = lambda nf: float(beta0(gf3, nf))
    res = {}
    for name, fn in (("QCD (R2, control)", None), ("QLF R3", b0r3)):
        vals = []
        for a in (at - st, at, at + st):
            a_tau = evolve(a, MZ, MTAU)                  # down with QCD: the measured alpha_s(m_tau)
            vals.append((a_tau, evolve(a_tau, MTAU, MZ, fn)))
        lo, mid, hi = (v[1] for v in vals)
        sig = (hi - lo) / 2
        pull = (mid - al) / math.hypot(sig, sl)
        res[name] = pull
        print(f"{name:>18}: alpha_s(m_tau) = {vals[1][0]:.4f}  ->  alpha_s(M_Z) = {mid:.5f} +- {sig:.5f}"
              f"   lattice {al:.4f} +- {sl:.4f}   pull {pull:+.2f}")
    verdict = lambda p: 'PASS' if abs(p) <= 2 else ('FAIL' if abs(p) > 3 else 'UNDECIDED')
    print(f"\ncontrol (QCD): {verdict(res['QCD (R2, control)'])}")
    print(f"V2 (R3): {verdict(res['QLF R3'])}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--L", type=int, default=24)
    ap.add_argument("--tau", type=float, nargs=2, metavar=("ALPHA", "SIGMA"), default=None,
                    help="PDG 2024 tau-decay sub-average alpha_s(M_Z)")
    ap.add_argument("--lat", type=float, nargs=2, metavar=("ALPHA", "SIGMA"), default=None,
                    help="PDG 2024 lattice sub-average alpha_s(M_Z)")
    args = ap.parse_args(argv)
    part1(args.L)
    gf3, _ = part2()
    if args.tau and args.lat:
        part3(gf3, tuple(args.tau), tuple(args.lat))
    else:
        print("\nV2 needs --tau and --lat (PDG 2024 sub-averages).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
