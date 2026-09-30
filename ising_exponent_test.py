#!/usr/bin/env python3
"""
ising_exponent_test.py -- the pre-registered test of Carbon_Superconductivity.md sec 8.

Under H_1bit (the condensate phase held to one bit) the measured stiffness is the Ising interface tension, which in
2D vanishes linearly at T_c: rho_s ~ (T* - T)^x with x = 1 exactly. BKT gives a finite drop at the (2/pi) k_B T line.
Frozen in commit a8b31f0: fit rho_s = A (T* - T)^x to the points with rho_s <= 0.5 rho_s(0) (at least 5),
A, T*, x free.   Ising FAILS if x + 2 sigma < 1;  SURVIVES if |x - 1| <= 2 sigma;  no verdict if x - 2 sigma > 1.

Data: Tanaka et al., Nature 638, 99 (2025), arXiv:2406.13740, Supplementary Fig. 16 (magic-angle twisted bilayer
graphene). The figure is a raster image; the markers below were located automatically (colour segmentation,
centroids) and calibrated to the axis box, which the embedded image fills exactly. They fall on the 0.02 K
measurement grid. The last electron-side marker is clipped by the axis at D_s = 0 (its centroid reads 0.015e8).
Banerjee et al. Fig. 2c (trilayer) has no curve that reaches its end, so it contributes nothing.

Stdlib only. The fit profiles (T*, x) on a grid with A solved exactly; sigma_x is the profile width at
delta chi^2 = 1 with the noise variance set by the residuals.

Run:  python3 ising_exponent_test.py
"""
from __future__ import annotations

import math

HBAR, E, KB = 1.054571817e-34, 1.602176634e-19, 1.380649e-23

# (T in K, D_s in 1e8 H^-1)
CURVES = {
    "hole side, V_BG = -6.9 V": [
        (0.025, 1.5965), (0.030, 1.7368), (0.040, 1.6814), (0.075, 1.6130), (0.120, 1.6121), (0.140, 1.6087),
        (0.160, 1.5775), (0.180, 1.5429), (0.200, 1.4632), (0.220, 1.4147), (0.240, 1.3887), (0.260, 1.3472),
        (0.280, 1.3056), (0.300, 1.2156), (0.320, 1.1515), (0.340, 1.0476), (0.360, 1.0026), (0.380, 1.0320),
        (0.400, 0.9541), (0.420, 0.9212), (0.440, 0.8260), (0.460, 0.7827), (0.480, 0.7048), (0.500, 0.7671),
        (0.520, 0.5576), (0.600, 0.3134)],
    "electron side, V_BG = 3.16 V": [
        (0.062, 1.1406), (0.120, 1.1315), (0.140, 1.1276), (0.160, 1.1081), (0.180, 1.0978), (0.200, 1.0770),
        (0.220, 1.0549), (0.240, 1.0082), (0.260, 1.0381), (0.280, 1.0043), (0.300, 0.9381), (0.320, 0.8421),
        (0.340, 0.8940), (0.360, 0.8577), (0.380, 0.7578), (0.400, 0.6851), (0.420, 0.7318), (0.440, 0.6605),
        (0.460, 0.6708), (0.480, 0.6553), (0.500, 0.5294), (0.520, 0.5151), (0.540, 0.5813), (0.580, 0.3893),
        (0.600, 0.2894), (0.620, 0.2102), (0.660, 0.0152)],
}


def rss_fixed(pts, Ts: float, x: float) -> float:
    """Residual sum of squares of A (Ts - T)^x with the best A (closed form)."""
    g = [(Ts - t) ** x for t, _ in pts]
    A = sum(gi * y for gi, (_, y) in zip(g, pts)) / sum(gi * gi for gi in g)
    return sum((A * gi - y) ** 2 for gi, (_, y) in zip(g, pts))


def fit(pts):
    tmax = max(t for t, _ in pts)
    Ts_grid = [tmax + 1e-4 + 0.002 * i for i in range(150)]
    x_grid = [0.05 + 0.005 * j for j in range(500)]
    prof = []                       # profile over x: min over T*
    for x in x_grid:
        prof.append(min((rss_fixed(pts, Ts, x), Ts) for Ts in Ts_grid))
    best = min(range(len(x_grid)), key=lambda j: prof[j][0])
    rss0, Ts0 = prof[best]
    s2 = rss0 / (len(pts) - 3)
    inside = [x_grid[j] for j in range(len(x_grid)) if (prof[j][0] - rss0) / s2 <= 1.0]
    sigma = (max(inside) - min(inside)) / 2
    rss1 = min(rss_fixed(pts, Ts, 1.0) for Ts in Ts_grid)
    return x_grid[best], sigma, Ts0, rss0, rss1


def verdict(x: float, s: float) -> str:
    if x + 2 * s < 1:
        return "FAIL"
    return "SURVIVES" if abs(x - 1) <= 2 * s else "no verdict"


def bkt_line(T: float) -> float:
    """8 e^2 k_B T / (pi hbar^2), in 1e8 H^-1: the stiffness at which BKT unbinding sets in."""
    return 8 * E ** 2 * KB * T / (math.pi * HBAR ** 2) / 1e8


def main() -> None:
    print("Frozen rule: points with D_s <= 0.5 D_s(0); fit A (T* - T)^x.\n")
    for name, pts in CURVES.items():
        d0 = sorted(y for t, y in pts if t < 0.2)[len([1 for t, _ in pts if t < 0.2]) // 2]
        sel = [(t, y) for t, y in pts if y <= 0.5 * d0]
        x, s, Ts, rss0, rss1 = fit(sel)
        print(f"  {name:<30} n = {len(sel)}  x = {x:.2f} +- {s:.2f}  T* = {Ts:.3f} K"
              f"   rss(x free)/rss(x = 1) = {rss0 / rss1:.2f}   -> Ising {verdict(x, s)}")
    print("\nRobustness (diagnostic, not the verdict): the same fit with other cutoffs.\n")
    for name, pts in CURVES.items():
        d0 = sorted(y for t, y in pts if t < 0.2)[len([1 for t, _ in pts if t < 0.2]) // 2]
        row = []
        for frac in (0.5, 0.6, 0.7, 0.8):
            sel = [(t, y) for t, y in pts if y <= frac * d0]
            x, s, *_ = fit(sel)
            row.append(f"{frac}: {x:.2f}+-{s:.2f}")
        print(f"  {name:<30} " + "   ".join(row))
    print("\nBKT jump (test U, sec 7): points below the (2/pi) k_B T line, as (T, D_s, line):\n")
    for name, pts in CURVES.items():
        below = [(t, y, round(bkt_line(t), 3)) for t, y in pts if y < bkt_line(t)]
        print(f"  {name:<30} {below}")
    print("""
Reading. The electron-side curve, the one that reaches D_s = 0, gives x = 0.62 +- 0.07: Ising FAILS by the frozen
rule. The hole-side curve has only five points under the cutoff and cannot decide (x = 0.64 +- 1.17), but every
wider cutoff puts it at x = 0.58-0.67 as well. So both bilayer curves vanish with x ~ 0.6, not 1.

That retires two readings at once for this bilayer: the one-bit (Ising interface) stiffness, and BCS mean-field
(also x = 1). The stiffness also falls continuously through the BKT line, with no jump -- the same observation as
sec 7a, now with the points below the line listed. x ~ 0.6 sits near the 3D-XY value 0.67, but a single 2D sample
with twist-angle disorder can round the end of a curve in either direction, so that is noted and not claimed.""")


if __name__ == "__main__":
    main()
