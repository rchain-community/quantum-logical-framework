#!/usr/bin/env python3
"""
moire_one_bit.py -- the one-bit phase of Carbon_Superconductivity.md sec 7 placed on the moire lattice (sec 11).

Extension point 3 of moire_zfa_dna.py. Under H_1bit the condensate phase is one bit per coherence patch, and the
ways of the condensate are an Ising model on the lattice of patches. On the moire the patches are fixed by the
flat-band Wannier orbitals: they sit on the AB/BA stacking regions, a HONEYCOMB lattice (Koshino et al. 2018;
Kang & Vafek 2018; Po et al. 2018). The alternative, one patch per AA region (where the charge peaks), is the
TRIANGULAR lattice. The coupling J between patches needs extension point 1 (interlayer closures); the ratio
r = k_B T_c / D_s(0) does not, because both T_c and D_s(0) are proportional to J.

  sec 1  the moire cell from the DNA: atoms per cell and period, checked against the known 1.05 deg cell.
  sec 2  r for one bit and for two bits (the mu_4 clock), on the two moire lattices, exact.
  sec 3  against the trilayer measurement (Banerjee 2025; seen before this was written, so a check, not a test):
         the stiffness underestimate each hypothesis needs.
  sec 4  the pre-registered test for new data: an independent measurement of that underestimate.

Convention (as sec 7): neighbouring patches couple as -J cos(theta_i - theta_j); D_s(0) is the stiffness the same
bonds would have for a continuous phase, so that BKT reads k_B T_BKT = (pi/2) D_s(T_BKT).

Run:  python3 moire_one_bit.py
"""
from __future__ import annotations

import math

A_GRAPHENE = 0.246  # nm


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def stiffness_factor(lattice: str) -> float:
    """D_s(0)/J for a -J cos coupling on nearest-neighbour bonds of unit length (a uniform twist k costs
    (J/2) sum_bonds (k.d)^2 per unit area = (D_s/2) k^2)."""
    if lattice == "honeycomb":        # 3 bonds per 2-site cell of area 3 sqrt3 / 2; sum of cos^2 over 3 directions = 3/2
        return (3 / 2) / (3 * math.sqrt(3) / 2)
    if lattice == "triangular":       # 3 bonds per 1-site cell of area sqrt3 / 2
        return (3 / 2) / (math.sqrt(3) / 2)
    raise ValueError(lattice)


def ising_tc(lattice: str) -> float:
    """Exact critical temperature of the Ising model -J s s, in units of J."""
    return {"honeycomb": 2 / math.log(2 + math.sqrt(3)),
            "triangular": 4 / math.log(3)}[lattice]


def sec1() -> None:
    rule("sec 1  THE MOIRE CELL FROM THE DNA")
    print("""
For the commensurate family of moire_zfa_dna.py (counts (m+1, -m, 0), norm |z|^2 = 3m^2 + 3m + 1), the supercell
vector is the DNA's inflation: its length is |z| lattice constants. A bilayer cell holds 2 layers x 2 sublattices
x |z|^2 atoms, and the period matches the moire formula a / (2 sin(theta/2)).
""")
    print(f"  {'m':>3}{'theta':>10}{'|z|^2':>8}{'atoms/cell':>12}{'|z| a (nm)':>12}{'a/2sin(th/2)':>14}")
    for m in (1, 10, 30, 31):
        n = 3 * m * m + 3 * m + 1
        th = math.acos((3 * m * m + 3 * m + 0.5) / n)
        print(f"  {m:>3}{math.degrees(th):>9.4f}°{n:>8}{4 * n:>12}{math.sqrt(n) * A_GRAPHENE:>12.3f}"
              f"{A_GRAPHENE / (2 * math.sin(th / 2)):>14.3f}")
        assert abs(math.sqrt(n) * A_GRAPHENE - A_GRAPHENE / (2 * math.sin(th / 2))) < 1e-9
    print("""
m = 31 is the familiar 1.05° commensurate cell with 11,908 atoms. Each
moire cell holds one AA region and two AB/BA regions, so the Wannier orbitals form a honeycomb of period
|z| a, and the AA regions a triangular lattice of the same period.""")


def sec2() -> dict[str, float]:
    rule("sec 2  THE RATIO r = k_B T_c / D_s(0) ON THE MOIRE LATTICES")
    print("""
One bit: theta in {0, pi}, so -J cos(dtheta) = -J s s: Ising with coupling J.
Two bits, independent (the mu_4 clock, theta in {0, pi/2, pi, 3pi/2}): -J cos(dtheta) = -(J/2)(s1 s1' + s2 s2'),
two decoupled Ising models with coupling J/2, so T_c halves.
Continuous phase (BKT): r <= pi/2 = 1.571 on any lattice.
""")
    out = {}
    print(f"  {'lattice':<24}{'D_s(0)/J':>10}{'T_c/J one bit':>15}{'r one bit':>11}{'r two bits':>12}")
    for lat, where in (("honeycomb", "AB/BA, Wannier centres"), ("triangular", "AA, charge peaks")):
        f = stiffness_factor(lat)
        tc = ising_tc(lat)
        out[lat] = tc / f
        print(f"  {lat + ' (' + where.split(',')[0] + ')':<24}{f:>10.4f}{tc:>15.4f}{tc / f:>11.3f}{tc / f / 2:>12.3f}")
    print(f"\n  continuous phase (BKT ceiling):  r <= {math.pi / 2:.3f}")
    print("""
The one-bit values on the moire lattices are the sec 7 values; the moire picks which one. With the Wannier
centres, r = 2.63. The ratio is independent of the twist angle and of the number of layers, since only the
lattice of patches enters: one bit predicts the same slope T_c/rho_s0 for every magic-angle multilayer whose
T_c is set by coherence.""")
    return out


def sec3(r: dict[str, float]) -> None:
    rule("sec 3  AGAINST THE TRILAYER (a check against data already seen)")
    measured = [("fitted slope of T_c vs rho_s0 (Fig. 3b)", 3.04, 0.10),
                ("dome-top points", 2.23, 0.20)]
    print("""
Banerjee et al. 2025 (arXiv:2406.13742) measure r = 2.2-4.2 on the magic-angle trilayer, with a linear T_c vs
rho_s0 of slope 3.0 through the origin (Carbon_Superconductivity.md sec 7a). They argue the microwave response
underestimates the sheet stiffness by a factor alpha = w/w* because the supercurrent runs in filaments. Each
hypothesis needs a particular alpha to match: alpha_needed = r_measured / r_model.
""")
    models = [("one bit, honeycomb (Wannier)", r["honeycomb"]),
              ("one bit, triangular (AA)", r["triangular"]),
              ("two bits (mu_4 clock), honeycomb", r["honeycomb"] / 2),
              ("two bits (mu_4 clock), triangular", r["triangular"] / 2),
              ("continuous phase, at the BKT ceiling", math.pi / 2)]
    print(f"  {'model':<38}{'r':>7}{'alpha (slope 3.04)':>21}{'alpha (dome top 2.23)':>23}")
    for name, rm in models:
        cells = f"{measured[0][1] / rm:>21.2f}{measured[1][1] / rm:>23.2f}"
        print(f"  {name:<38}{rm:>7.3f}{cells}")
    print("""
  (for the continuous phase the ceiling gives the smallest alpha; a real XY lattice has r below pi/2, needing
   more.)  Banerjee et al.'s own estimate, alpha ~ 3, was obtained by assuming T_BKT ~ T_c, i.e. by assuming the
  continuous phase.

Reading. One bit on the Wannier honeycomb needs alpha = 0.85-1.16: the stiffness as measured, to within 16 %.
The continuous phase needs alpha >= 1.4-1.9 (3.4 for the square XY lattice, r = 0.893), and two independent bits need
1.7-2.9. So IF the measured stiffness is the sheet stiffness (alpha ~ 1), only one bit per Wannier centre matches.
If alpha turns out ~ 2-3, the continuous phase and two independent bits both fit, and the stiffness exponent near
T_c separates them (a BKT jump against Ising's x = 1, Carbon_Superconductivity.md sec 8).""")


def sec4() -> None:
    rule("sec 4  THE TEST FOR NEW DATA (pre-registered in Carbon_Superconductivity.md sec 11)")
    print("""
The hypotheses are separated by one number that can be measured without assuming any of them: the ratio alpha of
the true sheet stiffness to the one inferred from the device's full width. Local probes do this (scanning SQUID
or scanning-probe susceptometry map the superfluid density directly), as does comparing devices of different
widths or of uniform twist angle.

  A verdict needs the 2-sigma interval of the measured alpha inside one band (the slope's own +-0.10 adds 3 %):
    alpha <= 1.30        -> one bit per Wannier centre (honeycomb), r = 2.63
    1.30 < alpha < 1.70  -> one bit per AA region (triangular), r = 2.10
    alpha >= 1.90        -> continuous phase or two independent bits; separated by the stiffness exponent near
                            T_c (BKT jump vs Ising x = 1)
    1.70 - 1.90, or an interval spanning two bands -> undecided

A second prediction, independent of alpha: if one bit per Wannier centre is right, every magic-angle multilayer
whose T_c is coherence-limited has T_c / rho_s0 in the same proportion (the same alpha-corrected slope), since in the
Khalaf et al. decomposition every member's flat bands are twisted-bilayer-like, on the same Wannier honeycomb.""")


if __name__ == "__main__":
    sec1()
    r = sec2()
    sec3(r)
    sec4()
