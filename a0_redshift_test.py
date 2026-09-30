#!/usr/bin/env python3
"""
a0_redshift_test.py — the pre-registered a0(z) test of DarkMatter.md §5c.

Which clock sets a0? M_E: a0(z)/a0(0) = H(z)/H0 (QLF expansion clock); M_T: = t0/t(z) (age clock);
M_C: constant (standard MOND). Data: MUSE-DARK III (Ciocan et al. 2026, arXiv:2604.22613) Fig. 3, four
redshift bins, digitized by eye (D1); D2 = D1 x 2.19/2.38 (their MOND-framework vs DC14, Fig. 2).
Test S: one free normalization per model, chi^2 with 3 dof. Test N: normalization fixed at SPARC 1.20.
Pure Python.
"""
import math

OM, OL = 0.315, 0.685
BINS = [(0.50, 1.99, 0.08), (0.83, 2.20, 0.10), (1.05, 2.57, 0.11), (1.28, 2.71, 0.14)]
MOND_SCALE = 2.19 / 2.38
A_SPARC = 1.20


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def age(z):  # flat LCDM, units of 1/H0
    return (2 / (3 * math.sqrt(OL))) * math.asinh(math.sqrt(OL / OM) * (1 + z) ** -1.5)


MODELS = {
    "M_E expansion clock H(z)/H0": E,
    "M_T age clock t0/t(z)      ": lambda z: age(0) / age(z),
    "M_C constant               ": lambda z: 1.0,
}


def chi2_p(x, dof):
    if dof == 3:
        return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    if dof == 4:
        return math.exp(-x / 2) * (1 + x / 2)
    raise ValueError


def fit(data, shape):
    num = sum(y * shape(z) / s ** 2 for z, y, s in data)
    den = sum(shape(z) ** 2 / s ** 2 for z, y, s in data)
    A = num / den
    chi2 = sum(((y - A * shape(z)) / s) ** 2 for z, y, s in data)
    return A, chi2


def run(label, data):
    print(f"{label}")
    print("  S (shape, A free, 3 dof):")
    res = {}
    for name, f in MODELS.items():
        A, c2 = fit(data, f)
        res[name] = c2
        print(f"    {name}: A = {A:.3f}  chi2 = {c2:6.2f}  p = {chi2_p(c2, 3):.3g}")
    best = min(res.values())
    for name, c2 in res.items():
        tag = "preferred" if c2 == best else ("disfavored" if c2 - best > 4 else "not disfavored")
        print(f"      {name}: dchi2 = {c2 - best:6.2f}  -> {tag}")
    print("  N (A fixed at SPARC 1.20, 4 dof):")
    for name, f in MODELS.items():
        c2 = sum(((y - A_SPARC * f(z)) / s) ** 2 for z, y, s in data)
        preds = ", ".join(f"{A_SPARC * f(z):.2f}" for z, _, _ in data)
        print(f"    {name}: predicted [{preds}]  chi2 = {c2:7.2f}  p = {chi2_p(c2, 4):.3g}")
    print()


def main():
    print("a0(z) test — DarkMatter.md §5c (MUSE-DARK III bins)\n")
    print("  shapes at the bin redshifts:")
    for z, y, s in BINS:
        print(f"    z = {z}: H/H0 = {E(z):.3f}   t0/t = {age(0) / age(z):.3f}   data a0 = {y}")
    print()
    run("D1 (as published, DC14 halo):", BINS)
    run("D2 (scaled to MOND framework, x0.920):", [(z, y * MOND_SCALE, s * MOND_SCALE) for z, y, s in BINS])


if __name__ == "__main__":
    main()
