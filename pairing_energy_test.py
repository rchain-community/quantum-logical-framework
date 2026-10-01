#!/usr/bin/env python3
"""
pairing_energy_test.py -- the pre-registered test of Carbon_Superconductivity.md sec 15 (frozen in 961bd07).

Route A (one bit, coherence-limited, flat-band geometry):  2 Delta / k_B T_c = 4 pi / (2.63 N sqrt(nu(1-nu)) G),
   in [2.39, 7.22] for N in {2, 4}, nu in [1/8, 1/2], G = 1 (G >= 1 only lowers it). BKT: >= 8/(N sqrt(nu(1-nu)) G).
Route A' (stiffness from the gap):  rho_s0 = N Delta sqrt(nu(1-nu)) G / 2pi, against the measured stiffness.
Route B (the log 2 closure quantum as the gap):  2 Delta / k_B T_c = 2 log 2 = 1.386, or 2 / log 2 = 2.885.

Data, as reported:
  Kim et al., Nature 606, 494 (2022), arXiv:2109.12127 (trilayer, STM): Delta ~ 1.6 meV (coherence peak to peak
     = 2 Delta), T_c ~ 2-2.5 K, "2 Delta / k_B T_C ~ 15-19".
  Oh et al., Nature 600, 240 (2021), arXiv:2109.13944 (bilayer, STM + point-contact): two gaps. Tunneling,
     2 Delta_T / k_B T_c = 27 (device A'), identified by the authors as a pseudogap that persists above T_c and B_c;
     Andreev, 2 Delta_AR / k_B T_c = 5.8 (devices A' and G: 2 Delta_AR = 0.6 meV, T_c = 1.2 K), which disappears
     when phase-coherent superconductivity is absent.
  Stiffness: Banerjee 2025 trilayer rho_s0 ~ 0.48 K at the dome top (Fig. 3b); Tanaka 2025 bilayer
     D_s ~ 1.7e8 H^-1 = 1.33 K (Fig. 3c).

Run:  python3 pairing_energy_test.py
"""
from __future__ import annotations

import math

KB_MEV = 0.08617333          # meV per K
LOG2 = math.log(2)


def a_ratio(N: int, nu: float, G: float = 1.0) -> float:
    return 4 * math.pi / (2.63 * N * math.sqrt(nu * (1 - nu)) * G)


def bkt_floor(N: int, nu: float, G: float = 1.0) -> float:
    return 8 / (N * math.sqrt(nu * (1 - nu)) * G)


def rho_pred(delta_mev: float, N: int, nu: float, G: float = 1.0) -> float:
    return N * (delta_mev / KB_MEV) * math.sqrt(nu * (1 - nu)) * G / (2 * math.pi)


MEASURED = [  # (label, 2Delta/kTc low, high, material, coherence-limited?, kind)
    ("trilayer, Kim 2022 (STM coherence peaks)", 15.0, 19.0, "TTG", True, "tunneling"),
    ("bilayer, Oh 2021 (tunneling, pseudogap)", 25.0, 27.0, "TBG", False, "tunneling"),
    ("bilayer, Oh 2021 (Andreev, devices A', G)", 5.8, 5.8, "TBG", False, "Andreev"),
]


def main() -> None:
    lo_a = min(a_ratio(N, nu) for N in (2, 4) for nu in (1 / 8, 1 / 4, 1 / 2))
    hi_a = max(a_ratio(N, nu) for N in (2, 4) for nu in (1 / 8, 1 / 4, 1 / 2))
    print(f"Route A band: 2 Delta / k_B T_c in [{lo_a:.2f}, {hi_a:.2f}]  (central N=4, nu=1/4: {a_ratio(4, 0.25):.2f});"
          f"  BKT floor >= {bkt_floor(4, 0.5):.2f} - {bkt_floor(2, 1 / 8):.2f}")
    print(f"Route B: H_L1 = 2 log 2 = {2 * LOG2:.3f};  H_L2 = 2/log 2 = {2 / LOG2:.3f}\n")
    print(f"  {'measurement':<44}{'2D/kTc':>10}   {'route A':<34}{'H_L1':>7}{'H_L2':>7}")
    for lab, lo, hi, mat, coh, kind in MEASURED:
        inside = lo <= hi_a and hi >= lo_a
        if inside:
            va = "consistent"
        elif coh:
            va = "FAILS (coherence-limited)"
        else:
            va = "outside band (rule n/a: not coh.-lim.)"
        vb1 = "FAIL" if abs(lo - 2 * LOG2) / (2 * LOG2) > 0.3 else "ok"
        vb2 = "FAIL" if abs(lo - 2 / LOG2) / (2 / LOG2) > 0.3 else "ok"
        rng = f"{lo:.1f}" if lo == hi else f"{lo:.0f}-{hi:.0f}"
        print(f"  {lab:<44}{rng:>10}   {va:<34}{vb1:>7}{vb2:>7}")

    print("\nRoute A': stiffness predicted from the gap (G = 1), against the measured stiffness")
    rows = [("trilayer, Kim gap 1.6 meV vs Banerjee 0.48 K", 1.6, 0.48),
            ("bilayer, Oh tunneling gap 1.4 meV vs Tanaka 1.33 K", 1.4, 1.33),
            ("bilayer, Oh Andreev gap 0.3 meV vs Tanaka 1.33 K", 0.3, 1.33)]
    for lab, d, meas in rows:
        p4, p2 = rho_pred(d, 4, 0.25), rho_pred(d, 2, 0.25)
        print(f"  {lab:<52} predicted {p4:.2f} K (N=4) / {p2:.2f} K (N=2);  measured/predicted = "
              f"{meas / p4:.2f} / {meas / p2:.2f}")
    print(f"""
Reading.
  Route B fails outright: no superconductor here has 2 Delta / k_B T_c near 1.39 or 2.89; the log 2 quantum at T_c
  is not the pairing energy.
  Route A, by the letter: the trilayer's STM gap gives 15-19, above the one-bit band [2.39, 7.22], in a material
  whose T_c is coherence-limited -- A FAILS for the trilayer with that gap. The same gap predicts a stiffness about
  10x the measured one (ratio 0.09-0.19, below the 0.3 flag).
  The bilayer shows why that may not be the last word: there the tunneling gap (27; stiffness ratio 0.30-0.59) is a
  pseudogap, and the Andreev gap tied to phase coherence gives 5.8 -- inside the band, with a stiffness ratio of
  1.4-2.8. Every number that fails here comes from a tunneling gap; the one coherence-tied gap passes. It does not
  discriminate, though: 5.8 is also above the BKT floor (4.62 at the centre), and the bilayer is not
  coherence-limited (sec 7a), so its consistency with route A is weak support.
  So the pre-registered prediction for new data: the trilayer's Andreev (phase-coherent) gap should give
  2 Delta_AR / k_B T_c in [{lo_a:.2f}, {hi_a:.2f}], i.e. Delta_AR in [{lo_a * 2.25 * KB_MEV / 2:.2f}, {hi_a * 2.25 * KB_MEV / 2:.2f}] meV at T_c = 2.25 K --
  2 to 7 times smaller than the STM coherence-peak gap, as in the bilayer.""")


# The pre-registered trilayer prediction (sec 15a), tested against data found afterwards:
# Kim, Rai, Crippa et al., arXiv:2505.17200 (2025), MATTG device #1 (theta = 1.61 deg), Fig. 4e,f: Andreev
# (point-contact, BTK) gaps alongside the STM tunneling gap at the same location. Inner-gap onset 1.5 K at
# nu = -2.3 (V_gate ~ -8.6 V), "matching the Andreev signal" (Extended Data Fig. 6); at V_gate = -10 V the Andreev
# signal disappears "around 1K".
KIM2025 = [  # (V_gate, tunneling Delta_T meV, Andreev Delta_A s-wave, d-wave)
    (-8.4, 0.89, 0.38, 0.47),
    (-8.7, 0.70, 0.29, 0.38),
]


def trilayer_andreev() -> None:
    lo_a = min(a_ratio(N, nu) for N in (2, 4) for nu in (1 / 8, 1 / 4, 1 / 2))
    hi_a = max(a_ratio(N, nu) for N in (2, 4) for nu in (1 / 8, 1 / 4, 1 / 2))
    print("\n" + "=" * 78 + "\nThe pre-registered trilayer prediction, tested (Kim et al. 2025, arXiv:2505.17200)\n" + "-" * 78)
    print(f"  prediction: Delta_AR in [0.23, 0.70] meV (at T_c = 2.25 K); 2 Delta_AR / k_B T_c in [{lo_a:.2f}, {hi_a:.2f}];"
          f"\n  2 to 7 times smaller than the tunneling gap.\n")
    print(f"  {'V_gate':>7}{'Delta_T':>9}{'Delta_A (s / d)':>18}{'in window':>11}{'Delta_T/Delta_A':>17}"
          f"{'2D/kTc @1.5K':>15}{'@1.0K':>13}")
    for vg, dt, ds, dd in KIM2025:
        inwin = all(0.23 <= x <= 0.70 for x in (ds, dd))
        r15 = [2 * x / (KB_MEV * 1.5) for x in (ds, dd)]
        r10 = [2 * x / (KB_MEV * 1.0) for x in (ds, dd)]
        print(f"  {vg:>7.1f}{dt:>9.2f}{ds:>10.2f} / {dd:.2f}{('yes' if inwin else 'no'):>11}"
              f"{dt / dd:>9.1f} - {dt / ds:.1f}{r15[0]:>9.1f} - {r15[1]:.1f}{r10[0]:>7.1f} - {r10[1]:.1f}")
    print(f"""
  Absolute window: all four Andreev gaps (0.29-0.47 meV) lie inside [0.23, 0.70] meV. The pre-registered "2 to 7
  times smaller" was against the 1.6 meV STM gap of Kim 2022: here 3.4-5.5 times. This device's own tunneling gap
  is only 1.8-2.4 times the Andreev gap. The ratio with the onset T_c at the nearest filling
  (1.5 K) is 4.5-7.3, inside the band except the d-wave fit at -8.4 V, which sits on its edge (7.27 vs 7.22).
  With the 1 K disappearance quoted for V_gate = -10 V it would be 6.7-10.9. An Andreev gap near the STM value
  (1.6 meV in Kim 2022) would have failed this test; it did not.
  It does not discriminate one bit from the continuous phase: 4.5-7.3 is also above the BKT floor (4.62 at
  the centre). What it supports is the chain's consistency -- flat-band geometry, the derived stiffness and a
  coherence-tied gap -- in the trilayer, the sample where the one-bit reading is still open.""")


if __name__ == "__main__":
    main()
    trilayer_andreev()
