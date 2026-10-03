#!/usr/bin/env python3
"""Phonons' double role in magic-angle graphene: Carbon_Superconductivity.md §26.

Is the phonon population that scatters (linear-in-T resistivity, the bath) the same
population that pairs (the glue)?  If so, lambda_pair ~ lambda_tr = C/2pi, where C is the
Planckian coefficient, hbar/tau = C k_B T.

The constants and verdict rules below were frozen in the §26 pre-registration commit,
before any T_c value was gathered.  DATA is filled in afterwards (§26a).
Stdlib only.
"""
import math

HBAR = 1.054571817e-34      # J s
KB = 1.380649e-23           # J/K
MEV = 1.602176634e-22       # J per meV
A_GRAPHENE = 0.246e-9       # m, graphene lattice constant
V_LA = 2.1e4                # m/s, graphene LA sound velocity
TOL = 2.0                   # allowed lambda_pair / lambda_tr mismatch (alpha^2 F vs alpha_tr^2 F)
MU_STAR = 0.0               # most phonon-favourable Coulomb pseudopotential


def omega_acoustic_meV(theta_deg):
    """hbar v_LA |K_M|: the top of the acoustic phonons that stay inside the moire zone.
    Used as omega_log, which is the most phonon-favourable choice for the acoustic population."""
    L_m = A_GRAPHENE / (2 * math.sin(math.radians(theta_deg) / 2))
    k_m = 4 * math.pi / (3 * L_m)
    return HBAR * V_LA * k_m / MEV


def tc_mcmillan_K(lam, omega_meV, mu=MU_STAR):
    """Allen-Dynes / McMillan with f1 = f2 = 1."""
    den = lam - mu * (1 + 0.62 * lam)
    if den <= 0:
        return 0.0
    return omega_meV * MEV / KB / 1.2 * math.exp(-1.04 * (1 + lam) / den)


def lambda_required(tc_K, omega_meV, mu=MU_STAR):
    """Invert McMillan: the coupling needed to reach tc_K. Bisection."""
    lo, hi = 1e-4, 50.0
    if tc_mcmillan_K(hi, omega_meV, mu) < tc_K:
        return math.inf
    for _ in range(200):
        mid = (lo + hi) / 2
        if tc_mcmillan_K(mid, omega_meV, mu) < tc_K:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def lambda_tr(C):
    """High-T phonon-limited scattering: hbar/tau = 2 pi lambda_tr k_B T."""
    return C / (2 * math.pi)


# Planckian C per filling branch: Cao et al. PRL 124, 076801 (2020), as already tabulated in §5a.
C_BRANCH = {"-2-d": (0.3, 0.1), "-2+d": (1.3, 0.3)}

# Filled in §26a: one row per device reporting a T_c on BOTH sides of nu = -2.
# (source, device, theta_deg, Tc(-2-d) K, sigma, Tc(-2+d) K, sigma)
DATA = []


def p1(rows):
    """Ordering. H_D predicts Tc(-2+d) > Tc(-2-d), because C is larger on -2+d.
    Retired if >= 3 devices and in at least 2/3 of them the -2-d dome is higher by more than
    the combined uncertainty."""
    if len(rows) < 3:
        return "inconclusive (fewer than 3 devices with both domes)"
    against = sum(1 for r in rows if r[3] - r[5] > math.hypot(r[4], r[6]))
    favour = sum(1 for r in rows if r[5] - r[3] > math.hypot(r[4], r[6]))
    if against >= math.ceil(2 * len(rows) / 3):
        return f"H_D RETIRED ({against}/{len(rows)} devices have the low-C dome higher)"
    return f"H_D stands ({favour} for, {against} against, of {len(rows)})"


def p2(branch, tc_K, theta_deg):
    """Magnitude. Retired for a branch if lambda_tr(C + 2 sigma) < lambda_req / TOL."""
    C, s = C_BRANCH[branch]
    lt = lambda_tr(C + 2 * s)
    lr = lambda_required(tc_K, omega_acoustic_meV(theta_deg))
    verdict = "RETIRED" if lt < lr / TOL else "stands"
    return lt, lr, verdict


def frozen_table():
    print("omega_log (acoustic top, meV):",
          ", ".join(f"{t}deg {omega_acoustic_meV(t):.2f}" for t in (1.05, 1.10, 1.16)))
    print("lambda_tr = C/2pi:  " + ", ".join(
        f"{b}: {lambda_tr(c):.3f} (+2s {lambda_tr(c + 2 * s):.3f})" for b, (c, s) in C_BRANCH.items()))
    print("lambda_req at 1.10 deg, mu* = 0:")
    for tc in (0.5, 1.0, 1.5, 2.0, 3.0):
        print(f"  Tc = {tc:.1f} K  ->  {lambda_required(tc, omega_acoustic_meV(1.10)):.3f}"
              f"  (H_D needs lambda_tr >= {lambda_required(tc, omega_acoustic_meV(1.10)) / TOL:.3f})")


if __name__ == "__main__":
    # Sanity: the inversion round-trips.
    w = omega_acoustic_meV(1.10)
    assert abs(tc_mcmillan_K(lambda_required(1.0, w), w) - 1.0) < 1e-9
    # Spontaneous = stimulated emission (n_B = 1) at hbar w = k_B T log 2; equal to both thermal channels at log 3.
    assert abs(1 / (math.exp(math.log(2)) - 1) - 1) < 1e-15
    assert abs(2 / (math.exp(math.log(3)) - 1) - 1) < 1e-15
    frozen_table()
    if DATA:
        print("\nP1:", p1(DATA))
        for r in DATA:
            for b, tc in (("-2-d", r[3]), ("-2+d", r[5])):
                if tc > 0:
                    lt, lr, v = p2(b, tc, r[2])
                    print(f"P2 {r[0]} {r[1]} {b}: lambda_tr<= {lt:.3f}, lambda_req {lr:.3f} -> {v}")
    else:
        print("\nDATA empty: pre-registration only.")
