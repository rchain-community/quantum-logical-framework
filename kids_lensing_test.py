#!/usr/bin/env python3
"""
kids_lensing_test.py — the pre-registered KiDS-1000 weak-lensing test of DarkMatter.md §5d.

Lensing and dynamics share one vacuum density (two paths of relatively slower light, QLF_LightBending),
so QLF's law fitted to SPARC dynamics must predict the lensing RAR with no free parameter.
Data: Brouwer et al. 2021 (A&A 650, A113) data release, data/kids_rar/. g_obs = 4 G ESD/(1+K).
Models: Q0 QLF law, a0 = 1.127e-10; Q1 QLF law, a0 scaled to <z> = 0.2 by H(z)/H0; M MOND baseline
(McGaugh form, a0 = 1.2e-10), used first as the pipeline check against B21's chi2_red = 4.0 on 7 points.
Pure Python (small matrices; Gauss-Jordan inverse).
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data", "kids_rar")
G_PC = 4.52e-30            # pc^3 / (Msun s^2), as in the B21 README
PC_M = 3.086e16
OM, OL = 0.315, 0.685
A0_SPARC = 1.127e-10
A0_MOND = 1.2e-10
ZLENS = 0.2


def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + OL)


def qlf(gbar, a0):
    return 0.5 * (gbar + math.sqrt(gbar * gbar + 4 * gbar * a0))


def mond(gbar, a0):
    return gbar / (1 - math.exp(-math.sqrt(gbar / a0)))


def read_esd(name):
    rows = []
    for line in open(os.path.join(D, name)):
        if line.startswith("#") or not line.strip():
            continue
        v = [float(x) for x in line.split()]
        gbar, esd, _, err, bias = v[:5]
        rows.append((gbar, 4 * G_PC * esd / bias * PC_M, 4 * G_PC * err / bias * PC_M))
    return rows


def read_cov(name, key=None):
    """Covariance matrix in (m/s^2)^2 for observable bin 'key' (m == n), ordered by g_bar bin."""
    ent, radii = {}, set()
    for line in open(os.path.join(D, name)):
        if line.startswith("#") or not line.strip():
            continue
        m, n, ri, rj, c, _, bias = [float(x) for x in line.split()]
        if key is not None and not (m == key and n == key):
            continue
        ent[(ri, rj)] = c / bias * (4 * G_PC * PC_M) ** 2
        radii.add(ri)
    r = sorted(radii)
    return [[ent[(a, b)] for b in r] for a in r]


def inverse(a):
    n = len(a)
    m = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        pv = m[c][c]
        m[c] = [x / pv for x in m[c]]
        for r in range(n):
            if r != c:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def chi2(rows, cov, model, idx):
    """rows: the selected bins; idx: their positions in the full covariance ordering."""
    C = [[cov[i][j] for j in idx] for i in idx]
    Ci = inverse(C)
    d = [r[1] - model(r[0]) for r in rows]
    return sum(d[i] * Ci[i][j] * d[j] for i in range(len(d)) for j in range(len(d)))


def pval(x, k):
    """chi-square survival function, integer k, by series."""
    if k % 2 == 0:
        s, term = 0.0, 1.0
        for i in range(k // 2):
            if i > 0:
                term *= (x / 2) / i
            s += term
        return math.exp(-x / 2) * s
    s = math.erfc(math.sqrt(x / 2))
    term = math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    for i in range(1, (k + 1) // 2):
        s += term
        term *= x / (2 * i + 1)
    return s


MODELS = {
    "Q0 QLF, a0 = 1.127 (local)   ": lambda g: qlf(g, A0_SPARC),
    "Q1 QLF, a0 x H(0.2)/H0 = 1.250": lambda g: qlf(g, A0_SPARC * E(ZLENS)),
    "M  MOND baseline, a0 = 1.2   ": lambda g: mond(g, A0_MOND),
}


def run(label, rows, cov, idx):
    print(f"{label}  (N = {len(rows)})")
    for name, f in MODELS.items():
        c2 = chi2(rows, cov, f, idx)
        print(f"    {name}: chi2 = {c2:7.2f}  chi2_red = {c2 / len(rows):5.2f}  p = {pval(c2, len(rows)):.3g}")
    print()


def main():
    print("KiDS-1000 weak-lensing RAR test — DarkMatter.md §5d\n")
    iso = read_esd("Fig-4-5-C1_RAR-KiDS-isolated_Nobins.txt")
    iso_cov = read_cov("Fig-4-5-C1_RAR-KiDS-isolated_covmatrix.txt")
    n = len(iso)
    last7 = list(range(n - 7, n))
    d7 = iso[-7:]

    c2m = chi2(d7, iso_cov, MODELS["M  MOND baseline, a0 = 1.2   "], last7)
    print(f"Pipeline check: MOND on D7, chi2_red = {c2m / 7:.2f}  (B21: 4.0)")
    if abs(c2m / 7 - 4.0) > 0.3:
        print("  -> does not reproduce B21; stopping before the QLF test (pre-registered rule).")
        return
    print("  -> reproduced; running the test.\n")

    run("D7  isolated KiDS-bright, 7 highest g_bar bins (primary)", d7, iso_cov, last7)
    run("D15 isolated KiDS-bright, all bins", iso, iso_cov, list(range(n)))
    hot = read_esd("Fig-4_RAR-KiDS-isolated_hotgas_Nobins.txt")
    run("DH  hot-gas g_bar, 7 highest bins", hot[-7:],
        read_cov("Fig-4_RAR-KiDS-isolated_hotgas_covmatrix.txt"), list(range(len(hot) - 7, len(hot))))
    for kind, fname, keys in (("Sersic", "Sersicbins", (0.0, 2.0)), ("Color", "Colorbins", None)):
        covf = f"Fig-8_RAR-KiDS-isolated_{fname}_covmatrix.txt"
        if keys is None:
            ks = sorted({float(l.split()[0]) for l in open(os.path.join(D, covf)) if not l.startswith("#")})
        else:
            ks = keys
        for b, key in enumerate(ks, start=1):
            full = read_esd(f"Fig-8_RAR-KiDS-isolated_{kind}bin_{b}.txt")
            run(f"DT  {kind} bin {b} (observable >= {key}), 7 highest bins", full[-7:], read_cov(covf, key),
                list(range(len(full) - 7, len(full))))


if __name__ == "__main__":
    main()
