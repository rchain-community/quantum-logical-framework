#!/usr/bin/env python3
"""
moire_interlayer.py -- extension point 1 of moire_zfa_dna.py: interlayer closures on the twisted pair.

Two layers grown from the chiral pair z / z-bar are twisted by theta. An interlayer closure is the word
   hop up (layer 1 -> layer 2) . a walk in layer 2 . hop down . the walk back in layer 1,
and it closes where a layer-2 site sits over the layer-1 site: the hop's in-plane residual is zero. At finite
capacity (ZFA_DNA.md sec 4; the maxExcursion listening of CLAUDE.md) a residual below the resolution eps counts as
closed. Each closing hop is one of two kinds:
   EVEN  -- it joins equal sublattices (A over A, B over B): the sign alternation of the two layers agrees,
   ODD   -- it joins opposite sublattices (A over B): the two layers' alternations are out of step.
The stacking regions of the moire are exactly where these kinds concentrate: AA (both sublattices, even),
AB and BA (one sublattice each, odd, in the two orientations).

  sec 1  the registry: the local interlayer shift u(r) = (1 - R_-theta) r, and the three closing registries.
  sec 2  closures counted over a commensurate cell (exact positions): where the even and odd hops sit.
  sec 3  the lattices they form: AA triangular, AB + BA honeycomb -- the lattice sec 11 of
         Carbon_Superconductivity.md took from the Wannier-orbital papers, now from the closure count.
  sec 4  what this gives J, and what it does not.

Run:  python3 moire_interlayer.py            (m = 10 cell, 3.15 deg, ~1 s)
      python3 moire_interlayer.py --m 31     (the 1.05 deg cell, 11,908 atoms)
"""
from __future__ import annotations

import argparse
import cmath
import math

W = cmath.exp(2j * math.pi / 3)
A1, A2 = 1.0 + 0j, cmath.exp(1j * math.pi / 3)       # graphene lattice vectors (lattice constant 1)
DELTA = (A1 + A2) / 3                                 # A -> B bond vector (length 1/sqrt3)


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def reduce_to_cell(u: complex) -> complex:
    """u modulo the graphene lattice, returned as the shortest representative."""
    # coordinates in the (A1, A2) basis
    det = (A1.real * A2.imag - A1.imag * A2.real)
    s = (u.real * A2.imag - u.imag * A2.real) / det
    t = (A1.real * u.imag - A1.imag * u.real) / det
    best = None
    for ds in (-1, 0, 1):
        for dt in (-1, 0, 1):
            v = u - (math.floor(s) + ds) * A1 - (math.floor(t) + dt) * A2
            if best is None or abs(v) < abs(best):
                best = v
    return best


def registry(u: complex) -> tuple[str, float]:
    """Nearest closing registry for an interlayer shift u: AA (0), AB (+delta), BA (-delta); and the residual."""
    cands = {"AA": 0j, "AB": DELTA, "BA": -DELTA}
    best = min(cands, key=lambda k: abs(reduce_to_cell(u - cands[k])))
    return best, abs(reduce_to_cell(u - cands[best]))


def sec1(theta: float) -> None:
    rule("sec 1  THE REGISTRY")
    print(f"""
Rotate layer 2 by theta = {math.degrees(theta):.4f}° about an AA point. At position r the two layers are shifted
by u(r) = (1 - R_-theta) r relative to each other, a linear, slowly varying map that scales by 2 sin(theta/2)
and rotates by 90° - theta/2. A hop
from a layer-1 site closes on layer 2 when u(r) is a lattice vector (A over A and B over B: AA, EVEN) or a lattice
vector plus or minus the bond delta (A over B: AB or BA, ODD). The ODD hops change the sublattice, so they flip
the sign alternation of carbon_zfa_dna.py sec 1; the EVEN hops keep it.""")


def sites(m: int):
    """Layer-1 and layer-2 sites inside one commensurate cell (the m-family), exact positions."""
    # supercell vectors for the (m, m+1) family, in the A1/A2 basis
    t1 = m * A1 + (m + 1) * A2
    t2 = cmath.exp(1j * math.pi / 3) * t1
    n = 3 * m * m + 3 * m + 1
    theta = math.acos((3 * m * m + 3 * m + 0.5) / n)
    det = t1.real * t2.imag - t1.imag * t2.real
    layer1 = []
    R = 3 * m + 4
    for i in range(-R, R + 1):
        for j in range(-R, R + 1):
            for sub, off in (("A", 0j), ("B", DELTA)):
                r = i * A1 + j * A2 + off
                s = (r.real * t2.imag - r.imag * t2.real) / det
                t = (t1.real * r.imag - t1.imag * r.real) / det
                if 0 <= s < 1 - 1e-12 and 0 <= t < 1 - 1e-12:
                    layer1.append((r, sub))
    assert len(layer1) == 2 * n, (len(layer1), 2 * n)
    return layer1, theta, t1, t2, n


def classify(layer1, theta, eps):
    """Each layer-1 site: the hop straight up closes (residual < eps) as AA/AB/BA, or does not."""
    rot = cmath.exp(-1j * theta)
    out = []
    for r, sub in layer1:
        u = r - rot * r                       # (1 - R_-theta) r
        # for a B site the AB/BA labels swap (B over A is the mirror registry)
        reg, res = registry(u)
        if sub == "B" and reg != "AA":
            reg = "BA" if reg == "AB" else "AB"
        out.append((r, sub, reg, res, res < eps))
    return out


def sec2(m: int, eps_list) -> tuple:
    layer1, theta, t1, t2, n = sites(m)
    sec1(theta)
    rule(f"sec 2  CLOSURES COUNTED OVER THE COMMENSURATE CELL (m = {m}, {2 * n} layer-1 sites)")
    print(f"\n  moire period |t1| = {abs(t1):.3f} a;  theta = {math.degrees(theta):.4f}°\n")
    print(f"  {'eps (a)':>8}  {'EVEN (AA)':>10}  {'ODD (AB)':>9}  {'ODD (BA)':>9}  {'open':>7}   closing fraction")
    for eps in eps_list:
        cl = classify(layer1, theta, eps)
        c = {"AA": 0, "AB": 0, "BA": 0}
        for r, sub, reg, res, ok in cl:
            if ok:
                c[reg] += 1
        tot = sum(c.values())
        print(f"  {eps:>8.3f}  {c['AA']:>10}  {c['AB']:>9}  {c['BA']:>9}  {2 * n - tot:>7}   {tot / (2 * n):.3f}")
    print("""
At fine resolution only the hops near the region centres close; as the capacity widens, each closing hop joins
the nearest registry, and the three kinds fill the cell. AB and BA close in nearly equal numbers (mirror images;
the discrete cell breaks the tie by a few sites), and EVEN hops are a third of all closures at every resolution, ODD two thirds: the shift map spreads
the sites evenly over the registry torus, and the three closing registries split it equally.""")
    return layer1, theta, t1, t2


def centres(layer1, theta, eps):
    """Centroid of each connected patch of closing hops, per registry (patches separated by > 1.5 a)."""
    cl = [(r, reg) for r, sub, reg, res, ok in classify(layer1, theta, eps) if ok]
    patches = []
    for r, reg in cl:
        for p in patches:
            if p["reg"] == reg and min(abs(r - q) for q in p["pts"][-40:]) < 1.5:
                p["pts"].append(r)
                break
        else:
            patches.append({"reg": reg, "pts": [r]})
    return [(p["reg"], sum(p["pts"]) / len(p["pts"]), len(p["pts"])) for p in patches if len(p["pts"]) >= 3]


def sec3(layer1, theta, t1, t2) -> None:
    rule("sec 3  THE LATTICES THE CLOSURES FORM")
    L = abs(t1)
    # region centres in the continuum: u(r) = target  =>  r = (1 - R_-theta)^{-1} target
    k = 1 - cmath.exp(-1j * theta)
    aa = [(i * A1 + j * A2) / k for i in range(-3, 4) for j in range(-3, 4)]
    ab = [(i * A1 + j * A2 + DELTA) / k for i in range(-3, 4) for j in range(-3, 4)]
    ba = [(i * A1 + j * A2 - DELTA) / k for i in range(-3, 4) for j in range(-3, 4)]

    def nn(points, targets):
        return sorted(abs(p - q) for p in points[:1] for q in targets if abs(p - q) > 1e-6)[:6]

    d_aa = nn([0j], aa)
    d_ab_ba = sorted(abs(ab[len(ab) // 2] - q) for q in ba)[:3]
    d_ab_ab = sorted(abs(ab[len(ab) // 2] - q) for q in ab if abs(ab[len(ab) // 2] - q) > 1e-6)[:6]
    print(f"""
Solving u(r) = registry gives the region centres (exact, from the linear map):
  EVEN (AA):      6 nearest AA at distance {d_aa[0]:.3f} a  (= moire period {L:.3f} a)      -> TRIANGULAR
  ODD (AB, BA):   each AB has 3 BA neighbours at {d_ab_ba[0]:.3f} a (= period / sqrt3 = {L / math.sqrt(3):.3f} a),
                  and 6 AB at {d_ab_ab[0]:.3f} a                                       -> HONEYCOMB
  The honeycomb of ODD closures has the same period as the triangle of EVEN ones and interlaces it: each AA sits
  at the centre of a hexagon of AB/BA.""")
    assert abs(d_aa[0] - L) < 1e-6 and abs(d_ab_ba[0] - L / math.sqrt(3)) < 1e-6
    cs = centres(layer1, theta, 0.08)
    kinds = {}
    for reg, c, npts in cs:
        kinds.setdefault(reg, []).append(npts)
    print(f"\n  Patches of closing hops in the cell at eps = 0.08 a (the cell's edges split its one AA, one AB and one BA\n  region into pieces; sizes = number of closing sites):")
    for reg in ("AA", "AB", "BA"):
        print(f"    {reg}: {len(kinds.get(reg, []))} patch(es), sizes {sorted(kinds.get(reg, []), reverse=True)[:6]}")
    print("""
So the two lattices of sec 11 both come out of the closure count: the EVEN hops (sign kept) sit on the triangular
AA lattice, the ODD hops (sign flipped) on the AB/BA honeycomb. The flat-band Wannier orbitals sit on the
honeycomb (Koshino et al. 2018; Kang & Vafek 2018; Po et al. 2018): the one bit per Wannier centre of sec 11 is
one bit per ODD patch -- per region where the two layers' sign alternations are out of step. That is a reading,
not a derivation of the Wannier centres; it says the honeycomb is the substrate's own ODD-closure lattice.""")


def sec4() -> None:
    rule("sec 4  WHAT THIS GIVES J, AND WHAT IT DOES NOT")
    print("""
Given: both candidate patch lattices of sec 11 are the substrate's own closure lattices -- EVEN on the AA
triangle, ODD on the AB/BA honeycomb -- with the honeycomb's coordination (3 BA per AB; the bonds of J run across
the domain walls between them) and the moire period |z| a. Choosing the ODD honeycomb for the bit, and so
r = 2.63 rather than 2.10, still rests on the Wannier result, or on reading the bit as the sign mismatch itself.

Not given: the value of J. A coupling needs an energy per closure crossing a domain wall, and nothing counted here
has units. Two routes to it, for later:
  (a) calibrate once -- take J from one measured stiffness, D_s(0) = J / sqrt3 on the honeycomb -- and predict
      every other measured T_c (this is what sec 11 already does with the ratio);
  (b) count the closures that link an AB patch to its BA neighbour across a domain wall, as a function of theta,
      and test the predicted angle dependence J(theta) against T_c(theta) -- that needs step 2, the flat band as a
      signed count, because the flat band's bandwidth is what sets the energy scale near the magic angle.""")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--m", type=int, default=10)
    args = ap.parse_args()
    layer1, theta, t1, t2 = sec2(args.m, [0.02, 0.05, 0.10, 0.20, 0.30])
    sec3(layer1, theta, t1, t2)
    sec4()
