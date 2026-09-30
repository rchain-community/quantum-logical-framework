#!/usr/bin/env python3
"""
light_bending.py — numbers for GR_Schwarzschild.md §4a (light bending from relatively slower light).

Pre-registered before this script was run. A ray past a point mass through the refractive index
n = 1 - k*phi, phi = -GM/(r c^2): k = 2 (event quantum: space and time rescale together, gamma = 1),
k = 1 (latency only: time slowed, space untouched). The deflection is integrated numerically along the
straight line (the first-order Born approximation) and compared with alpha = k * 2GM/(b c^2).
Pure Python.
"""
import math

GM_SUN = 1.32712440018e20      # m^3/s^2
R_SUN = 6.957e8                # m (IAU nominal)
C = 2.99792458e8
RAD_TO_ARCSEC = 180 / math.pi * 3600


def deflection_numeric(k, b, zmax_factor=1e6, n=200000):
    """alpha = integral over the line of |d n / d b| = k * GM/c^2 * b / (b^2 + z^2)^(3/2)."""
    zmax = zmax_factor * b
    # substitution z = b sinh(u) spreads the samples
    umax = math.asinh(zmax / b)
    du = 2 * umax / n
    total = 0.0
    for i in range(n):
        u = -umax + (i + 0.5) * du
        z = b * math.sinh(u)
        dz = b * math.cosh(u) * du
        total += k * GM_SUN / C ** 2 * b / (b * b + z * z) ** 1.5 * dz
    return total


def main():
    print("Light bending — GR_Schwarzschild.md §4a\n")
    b = R_SUN
    print("B1/B2  light speed vs clock rate at phi = -1e-6 (first order):")
    phi = -1e-6
    clock = math.sqrt(1 + 2 * phi)
    print(f"   clock rate sqrt(1+2phi)          = 1 {clock - 1:+.3e}")
    print(f"   light, event quantum  (1+2phi)   = 1 {2 * phi:+.3e}   ratio to clock slowing {2 * phi / (clock - 1):.4f}")
    print(f"   light, latency only sqrt(1+2phi) = 1 {clock - 1:+.3e}   ratio to clock slowing 1.0000\n")
    print("B3/B4  deflection at the solar limb (b = R_sun):")
    for k, label in ((2, "event quantum, gamma = 1"), (1, "latency only, gamma = 0")):
        a_num = deflection_numeric(k, b)
        a_formula = k * 2 * GM_SUN / (b * C ** 2)
        print(f"   k = {k} ({label}): numeric {a_num * RAD_TO_ARCSEC:.4f}\"   formula {a_formula * RAD_TO_ARCSEC:.4f}\"")
    L = 10 * b
    print(f"\n   finite-length check: int_-L^L = 2L/(b sqrt(b^2+L^2)) at L = 10b: "
          f"{2 * L / (b * math.sqrt(b * b + L * L)) * b:.6f} (x 1/b; -> 2 as L -> inf)")
    print("\n   Cassini: gamma - 1 = (2.1 +- 2.3)e-5  ->  k = 1 + gamma = 2 to 1e-5; latency only (k = 1) excluded")


if __name__ == "__main__":
    main()
