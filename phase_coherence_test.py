#!/usr/bin/env python3
"""
phase_coherence_test.py -- the pre-registered test of Carbon_Superconductivity.md sec 7.

H_1bit (Jim, 2026-09-30): "stiffness is to one bit precision". A closed history folds to +-I, so each coherence
patch of the pair condensate carries a phase in {0, pi}, and the ways of the condensate are an Ising model. If
coherence limits T_c:  r = k_B T_c / D_s(0) = 2/ln(1+sqrt2), (4/ln3)/sqrt3, sqrt3 * 2/ln(2+sqrt3)
= 2.27, 2.10, 2.63 on the square, triangular and honeycomb patch lattices.
H_BKT (continuous phase, vortex count): r <= pi/2 always, and a universal stiffness jump (2/pi) k_B T_c.

Frozen in commit 8c7b2ee before any value was read. D_s is in the convention where k_B T_BKT = (pi/2) D_s(T_BKT).

Run:  python3 phase_coherence_test.py
"""
from __future__ import annotations

import math

HBAR, E, KB = 1.054571817e-34, 1.602176634e-19, 1.380649e-23
PI2 = math.pi / 2


def ising_ratios() -> dict[str, float]:
    return {
        "square": 2 / math.log(1 + 2 ** 0.5),                    # D_s(0) = J
        "triangular": (4 / math.log(3)) / 3 ** 0.5,              # D_s(0) = sqrt3 J
        "honeycomb": (2 / math.log(2 + 3 ** 0.5)) * 3 ** 0.5,    # D_s(0) = J / sqrt3
    }


def stiffness_kelvin(inv_LK: float) -> float:
    """Sheet stiffness 1/L_K (H^-1) -> D_s in kelvin: D_s = hbar^2 / (4 e^2 L_K) / k_B."""
    return HBAR ** 2 * inv_LK / (4 * E ** 2) / KB


# Tanaka et al., Nature 638, 99 (2025), arXiv:2406.13740, Fig. 3d (read off the figure; D_s at base
# temperature, three T_c definitions). The largest-stiffness hole-doped points, where the ratio is highest.
TANAKA = [  # (label, D_s in H^-1, T_c in K)
    ("MATBG hole, T_c(zero)",  1.70e8, 0.70),
    ("MATBG hole, T_c(0.5)",   1.70e8, 1.05),
    ("MATBG hole, T_c(onset)", 1.68e8, 2.45),   # the highest onset point in Fig. 3d
    ("MATBG electron, T_c(onset)", 1.30e8, 1.65),
]

# Banerjee et al., Nature 638, 93 (2025), arXiv:2406.13742, Fig. 3b, read by pixel calibration of the
# 400-dpi rendering (reading error about +-0.01 K in rho_s0, +-0.02 K in T_c; the plotted error bars are
# larger, typically +-0.02-0.05 K in T_c). T_c is the onset of non-zero DC resistance, so it is the
# zero-resistance temperature. rho_s0 is already in kelvin in the BKT convention (rho_c = 2T/pi).
BANERJEE = [  # (label, rho_s0 in K, T_c in K, sigma_rho, sigma_T)
    ("TTG, lowest-stiffness point", 0.08, 0.22, 0.01, 0.03),
    ("TTG, lower branch", 0.15, 0.35, 0.01, 0.04),
    ("TTG, upper branch", 0.13, 0.54, 0.01, 0.04),
    ("TTG, mid dome", 0.27, 0.92, 0.01, 0.05),
    ("TTG, dome top (lowest r)", 0.48, 1.07, 0.04, 0.03),
    ("TTG, the authors' fitted line", 1.0, 3.04, 0.0, 0.10),   # slope of the dashed T_c line, as a ratio
]


def main() -> None:
    ir = ising_ratios()
    print("Predictions: H_1bit (coherence-limited) r = " + ", ".join(f"{k} {v:.2f}" for k, v in ir.items())
          + f";  H_BKT r <= pi/2 = {PI2:.3f}\n")

    print("Test R -- Tanaka 2025, magic-angle twisted bilayer graphene:")
    for lab, ds, tc in TANAKA:
        dk = stiffness_kelvin(ds)
        print(f"  {lab:<30} D_s = {dk:.3f} K   T_c = {tc:.2f} K   r = {tc / dk:.2f}   r/(pi/2) = {tc / dk / PI2:.2f}")
    print("""  Every zero- and half-resistance point lies below the BKT line (r <= 0.8). Only resistive-onset points
  reach above it, by up to ~18 %, and onset marks where the resistance starts to fall, not where the
  phase locks. No uncertainty on onset is given. -> no support for H_1bit from the bilayer.
""")
    print("Test R -- Banerjee 2025, magic-angle twisted trilayer graphene:")
    for lab, rho, tc, sr, st in BANERJEE:
        r = tc / rho
        sig = r * math.hypot(sr / rho, st / tc)
        print(f"  {lab:<30} rho_s0 = {rho:.2f} K   T_c = {tc:.2f} K   r = {r:.2f} +- {sig:.2f}"
              f"   (r - pi/2)/sigma = {(r - PI2) / sig:+.1f}")
    print("""  Every trilayer point has r > pi/2, the lowest by more than 2 sigma. By the frozen rule this supports
  H_1bit and excludes H_BKT for this sample. The fitted slope, 3.0, is 15-45 % above the one-bit band
  (2.10-2.63); the dome-top points, 2.2-2.9, overlap it.

  The caveat the rule did not price. The authors attribute the excess to inhomogeneity: if the supercurrent
  runs in filaments of total width w* < w, the microwave measurement underestimates the sheet stiffness
  by w*/w. They estimate w/w* ~ 3 by assuming T_BKT ~ T_c, which assumes the conclusion this test is
  checking, so it cannot be used as a correction here. It cannot be excluded either. So the support is
  conditional: it holds if the measured rho_s0 is the sheet stiffness.
""")
    print("""Test U -- stiffness jump:
  Hebard & Fiory 1980 (aluminium films): the authors report complex-impedance evidence of Kosterlitz-
  Thouless vortex-antivortex dissociation. Read from the abstract; the full text was not accessible. ->
  H_1bit fails for aluminium, as the stated prior expected.
  Tanaka 2025 (bilayer): D_s(T) falls steeply through the BKT line to zero over ~0.1 K, with no discontinuity
  (their Fig. 16). No jump is not evidence either way (frozen rule).
  Banerjee 2025 (trilayer): rho_s(T) crosses the BKT plane at T_0 ~ T_c/3, with superconductivity persisting
  above it -- no jump at T_c. No verdict (frozen rule).

Verdict. H_1bit is not universal: the conventional aluminium film behaves as a continuous phase. In the
magic-angle trilayer the raw data break the BKT ceiling by a factor of about 2 and sit at or just above the
one-bit band. That makes the trilayer a real lead for one-bit coherence, conditional on the stiffness being
what was measured. The bilayer does not discriminate.""")


if __name__ == "__main__":
    main()
