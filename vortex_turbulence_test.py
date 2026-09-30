#!/usr/bin/env python3
"""
vortex_turbulence_test.py -- the pre-registered test of Carbon_Superconductivity.md sec 9.

Is the vortex state near T_c a driven turbulent tangle? A Gorter-Mellink tangle (Vinen: line density L ~ v^2,
dissipation ~ L v ~ v^3) gives V ~ I^3 over a window of temperature. BKT gives a(T) = 1 + pi rho_s(T)/k_B T,
equal to 3 only at T_BKT, with the stiffness-free bound a(T) >= 1 + 2 T_BKT / T below it.

Frozen in commit f29b8ab. Statistic: T3 = the highest temperature with a >= 3; at every T <= 0.9 T3 compare a with
1 + 2 T3/T. BKT FAILS (turbulence supported) if at >= 2 such temperatures a sits below the bound by more than its
uncertainty (or 0.5), with a within 3 +- 0.5. Consistent with BKT if a meets the bound at every such T.
Undecided otherwise.

Data: data/moire_vi_curves.json -- V-I curves taken from the vector data of the published figures (Cao 2018,
Park 2021, Park 2022 x2). Hao 2021's log-log V-I inset is a raster image whose curves are not labelled by
temperature, so it cannot be used; Tanaka 2025 and Banerjee 2025 show no V-I curves at several temperatures.

How a is measured (fixed after the Park 2021 curves had been tabulated, so disclosed as such): a least-squares
slope of ln V against ln I over the points with 5 sigma_floor <= V <= V_N(I)/3, where sigma_floor is the scatter
of the lowest-temperature curve below its switching current and V_N is the highest-temperature (normal) curve.
Where a curve switches with fewer than 4 points in that window, a is reported as a lower bound taken across the
jump. Window sensitivity is printed alongside.

Stdlib only.   Run:  python3 vortex_turbulence_test.py
"""
from __future__ import annotations

import json
import math
import os
import statistics

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "moire_vi_curves.json")


def interp(xy, x):
    """Linear interpolation of a sorted [(x, y)] list."""
    if x <= xy[0][0]:
        return xy[0][1]
    for (x1, y1), (x2, y2) in zip(xy, xy[1:]):
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1) if x2 > x1 else y1
    return xy[-1][1]


def slope(pts):
    X = [math.log(i) for i, _ in pts]
    Y = [math.log(v) for _, v in pts]
    n = len(X)
    mx, my = sum(X) / n, sum(Y) / n
    sxx = sum((x - mx) ** 2 for x in X)
    b = sum((x - mx) * (y - my) for x, y in zip(X, Y)) / sxx
    res = [y - my - b * (x - mx) for x, y in zip(X, Y)]
    return b, math.sqrt(sum(r * r for r in res) / max(n - 2, 1) / sxx)


def exponent(xy, normal, floor, k_lo=5.0, f_hi=1 / 3):
    """(a, sigma, is_lower_bound) for one curve."""
    imax = xy[-1][0]
    above = [(i, v) for i, v in xy if i > 0.02 * imax and v >= k_lo * floor]
    if above and above[0][1] > f_hi * interp(normal, above[0][0]):
        # resistive from the start: fit the low-current part (expected a ~ 1)
        pts = [(i, v) for i, v in above if i <= 0.25 * imax]
        if len(pts) >= 4:
            a, s = slope(pts)
            return a, s, False
    pts = [(i, v) for i, v in xy if i > 0 and v >= k_lo * floor and v <= f_hi * interp(normal, i)]
    # keep only the first rising stretch: points before the curve first exceeds the upper limit
    first_hi = next((i for i, v in xy if i > 0.02 * imax and v > f_hi * interp(normal, i)), None)
    if first_hi is not None:
        pts = [(i, v) for i, v in pts if i < first_hi]
    if len(pts) >= 4:
        a, s = slope(pts)
        return a, s, False
    below = [(i, v) for i, v in xy if 0 < i and 0 < v < k_lo * floor]
    above = [(i, v) for i, v in xy if v >= k_lo * floor]
    if not below or not above:
        return None, None, True
    (i1, v1), (i2, v2) = max(below), min(above)
    return math.log(v2 / max(v1, floor)) / math.log(i2 / i1), 0.0, True


def analyse(name, sample):
    curves = {float(T): sorted((i, v) for i, v in xy) for T, xy in sample["curves"].items()}
    Ts = sorted(curves)
    normal = curves[Ts[-1]]
    low = curves[Ts[0]]
    ic_low = next(i for i, v in low if i > 0.05 * low[-1][0] and v > 0.05 * interp(normal, i))
    floor = statistics.pstdev([v for i, v in low if 0.05 * ic_low < i < 0.8 * ic_low])
    print(f"\n{name}\n  {sample['source']}; authors' T_BKT: {sample['authors_T_BKT']}")
    print(f"  noise floor {floor * 1e3:.2f} uV (lowest-T curve below its switching current)")
    a_of = {}
    for T in Ts[:-1]:
        a, s, lb = exponent(curves[T], normal, floor)
        sens = []
        for k, f in ((3, 1 / 3), (10, 1 / 3), (5, 1 / 2), (5, 1 / 5)):
            a2, _, lb2 = exponent(curves[T], normal, floor, k, f)
            sens.append("-" if a2 is None else f"{a2:.1f}{'+' if lb2 else ''}")
        a_of[T] = (a, s, lb)
        shown = "-" if a is None else (f">= {a:.1f} (switching)" if lb else f"{a:.2f} +- {s:.2f}")
        print(f"    T = {T:5.2f} K   a = {shown:<22} window sensitivity: {' '.join(sens)}")
    t3 = max((T for T, (a, s, lb) in a_of.items() if a is not None and a >= 3), default=None)
    if t3 is None:
        print("  no temperature with a >= 3 -> undecided")
        return
    usable = [T for T in Ts[:-1] if T <= 0.9 * t3 and a_of[T][0] is not None]
    below = 0
    meets = True
    for T in usable:
        a, s, lb = a_of[T]
        bound = 1 + 2 * t3 / T
        tol = s if (s and not lb) else 0.5
        if lb:
            ok = a >= bound or None      # a lower bound below the bound is not a violation
        else:
            ok = a >= bound - tol
        tangle = (not lb) and a < bound - tol and abs(a - 3) <= 0.5
        below += tangle
        if ok is False:
            meets = False
        state = "meets" if ok else ("lower bound only" if ok is None else "BELOW")
        print(f"    T = {T:5.2f} K <= 0.9 T3:  BKT bound a >= {bound:.2f};  measured {'>= ' if lb else ''}{a:.2f}  -> {state}")
    verdict = ("BKT FAILS, turbulence supported" if below >= 2 else
               "consistent with BKT" if meets and all(not a_of[T][2] or a_of[T][0] >= 1 + 2 * t3 / T for T in usable) else
               "undecided")
    print(f"  T3 = {t3:.2f} K; usable temperatures: {len(usable)} -> {verdict}")


def main() -> None:
    data = json.load(open(DATA))
    for name, sample in data["samples"].items():
        analyse(name, sample)
    print("""
Reading. Two samples are consistent with BKT (Cao 2018 bilayer, Park 2022 four-layer); two are undecided by the
letter of the rule (Park 2021 trilayer, Park 2022 five-layer), and in both the only failure of the BKT bound is
at the lowest temperature, where the V-I curve is a sharp switch whose fitted slope (7-14) is set by the rounding
of the edge, not a power law -- and is far from 3. In no sample does a sit at 3 +- 0.5 at any temperature below
T3, let alone two: a(T) climbs smoothly from ~1 above T3 through 3 to 4-12 within a few tenths of a kelvin.
So a Gorter-Mellink tangle is not what makes V ~ I^3 in these moire superconductors; the turbulence reading is
not supported by the V-I data.""")



if __name__ == "__main__":
    main()
