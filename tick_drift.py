#!/usr/bin/env python3
"""
tick_drift.py — Route 3 (a drifting Planck tick) of Log2_Search.md.

Pre-registered before this script was run. If tau_P ~ t^beta against cosmic/atomic time, the age in ticks
times today's tick is t0/(1-beta). Reconciling that with 1/H0 needs beta = 1 - H0 t0. The drift of
tau_P/tau_atomic = alpha^2 sqrt(G m_e^2 / hbar c) is compared with measured bounds:
  optical clocks  alpha_dot/alpha = 1.0(1.1)e-18 /yr   (Lange et al., PRL 126, 011102, 2021)
  lunar ranging   G_dot/G         = (7.1 +- 7.6)e-14 /yr (Hofmann & Muller, CQG 35, 035015, 2018)
Pure Python.
"""
import math

GYR_YR = 1e9


def flat_lcdm_H0t0(OL):
    x = math.atanh(math.sqrt(OL))
    return (2 / 3) * x / math.tanh(x)


def main():
    print("Route 3 — a drifting Planck tick (Log2_Search.md)\n")
    t0 = 13.80  # Gyr, Planck 2018 LCDM
    # T1 check by direct integration: N * tau_now = int_0^t0 (t0/t)^beta dt
    for beta in (0.0, 0.049, 0.2):
        n, steps = 0.0, 200000
        for i in range(steps):
            t = t0 * (i + 0.5) / steps
            n += (t0 / steps) * (t0 / t) ** beta
        print(f"T1  beta = {beta:<5}: ticks x today's tick = {n:.4f} Gyr;  t0/(1-beta) = {t0 / (1 - beta):.4f} Gyr")
    print()
    for label, OL in (("Planck LCDM (Omega_L = 0.6847)", 0.6847), ("Omega_L = log 2", math.log(2))):
        H0t0 = flat_lcdm_H0t0(OL)
        beta = 1 - H0t0
        drift = beta / (t0 * GYR_YR)
        print(f"T2  {label}: H0 t0 = {H0t0:.4f} -> beta = {beta:.4f}")
        print(f"T3      drift today beta/t0 = {drift:.2e} /yr")
        a_needed = drift / 2
        g_needed = 2 * drift
        print(f"        via alpha alone:  alpha_dot/alpha = {a_needed:.2e} /yr vs bound 1.0(1.1)e-18 "
              f"-> excess x{a_needed / 2.2e-18:.1e} (over 1-sigma upper edge)")
        print(f"        via gravity alone: G_dot/G-equivalent = {g_needed:.2e} /yr vs (7.1 +- 7.6)e-14 "
              f"-> {(g_needed - 7.1e-14) / 7.6e-14:.0f} sigma")
        print()
    print("T4  a drift this size shifts which epoch is 'now'; it does not produce an O(1) share such as log 2.")


if __name__ == "__main__":
    main()
