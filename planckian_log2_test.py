#!/usr/bin/env python3
"""
planckian_log2_test.py -- the pre-registered test of Carbon_Superconductivity.md sec 5.

Is the strange-metal scattering rate hbar/tau = C k_B T at C = log 2 (one binary closure per scattering,
receipting k_B T log 2) rather than the conventional Planckian C = 1?

The data set, statistic and verdict rules were fixed in commit ad8e36f before any value was gathered:
every C reported with an uncertainty in Legros et al. 2019, Cao et al. 2020 and Grissonnanche et al. 2021,
taken as reported (a range without an uncertainty -> half the range); the inverse-variance weighted mean
C_bar +- s, with chi^2 about the mean reported to show the spread.
  PASS       |C_bar - log 2| <= 2s  and  |C_bar - 1| > 2s
  FAIL       |C_bar - log 2| >  2s
  UNDECIDED  otherwise

Run:  python3 planckian_log2_test.py
"""
from __future__ import annotations

import math

# (source, sample, C, sigma) -- as stated in the arXiv text of each paper.
DATA = [
    # Legros et al., Nature Physics 15, 142 (2019), arXiv:1805.02512. The text gives one value for the two
    # electron-doped cuprates together.
    ("Legros 2019", "PCCO + LCCO (electron-doped)", 1.0, 0.3),
    ("Legros 2019", "Bi2212", 1.1, 0.3),
    ("Legros 2019", "LSCO", 0.9, 0.3),
    ("Legros 2019", "Nd-LSCO", 0.7, 0.4),
    ("Legros 2019", "Bi2201", 1.0, 0.4),
    ("Legros 2019", "(TMTSF)2PF6 (organic)", 1.0, 0.3),
    # Cao et al., PRL 124, 076801 (2020), arXiv:1901.03710: "C ~ 0.2-0.4" for nu = -2 - delta and
    # "C ~ 1.0-1.6" for nu = -2 + delta; no uncertainty given, so half the range.
    ("Cao 2020", "MATBG, nu = -2 - delta", 0.3, 0.1),
    ("Cao 2020", "MATBG, nu = -2 + delta", 1.3, 0.3),
    # Grissonnanche et al., Nature 595, 667 (2021), arXiv:2011.13054.
    ("Grissonnanche 2021", "Nd-LSCO, ADMR", 1.2, 0.4),
]
LOG2 = math.log(2)


def weighted(rows):
    w = [1 / s ** 2 for *_, s in rows]
    m = sum(wi * c for wi, (_, _, c, _) in zip(w, rows)) / sum(w)
    s = 1 / math.sqrt(sum(w))
    chi2 = sum(((c - m) / sd) ** 2 for *_, c, sd in rows)
    return m, s, chi2, len(rows) - 1


def chi2_sf(x: float, k: int) -> float:
    """Upper tail of chi^2 with k degrees of freedom (series; fine for these sizes)."""
    term = total = math.exp(-x / 2) * (x / 2) ** (k / 2) / math.gamma(k / 2 + 1)
    j = 1
    while term > 1e-16 * total:
        term *= (x / 2) / (k / 2 + j)
        total += term
        j += 1
    return 1 - total


def verdict(m: float, s: float) -> str:
    if abs(m - LOG2) > 2 * s:
        return "FAIL"
    return "PASS" if abs(m - 1) > 2 * s else "UNDECIDED"


def report(label: str, rows) -> None:
    m, s, chi2, dof = weighted(rows)
    print(f"  {label:<34} C = {m:.3f} +- {s:.3f}   (C-log2)/s = {(m - LOG2) / s:+.2f}   (C-1)/s = {(m - 1) / s:+.2f}"
          f"   chi2 = {chi2:.1f}/{dof} (p = {chi2_sf(chi2, dof):.4f})   -> {verdict(m, s)}")


if __name__ == "__main__":
    print("The data, as frozen:\n")
    for src, sample, c, s in DATA:
        print(f"  {src:<20}{sample:<32}C = {c:.1f} +- {s:.1f}")
    print("\nThe pre-registered statistic:\n")
    report("all nine values", DATA)
    print("\nDiagnosis (not part of the verdict rule, reported because chi2 says one C does not fit):\n")
    report("cuprates + organic only", [r for r in DATA if not r[0].startswith("Cao")])
    report("without Cao nu = -2 - delta", [r for r in DATA if "- delta" not in r[1]])
    near = [r for r in DATA if abs(r[2] - LOG2) <= r[3]]
    print(f"\n  values within 1 sigma of log 2: {[f'{r[1]} ({r[2]}+-{r[3]})' for r in near]}")
    print("""
Reading. By the frozen rule the verdict is PASS: the weighted mean is 0.61 +- 0.08, 1.0 sigma from log 2 and
5.1 sigma from 1. But chi^2 = 25/8 (p = 0.0015) says the nine values do not share one C. They form two
groups: the cuprates and the organic metal sit at 0.99 +- 0.13, and the magic-angle graphene values sit on
two filling branches at 0.2-0.4 and 1.0-1.6. The mean lands between the groups because one tightly
bounded value (0.3 +- 0.1) carries 57 % of the weight. Three measurements lie within 1 sigma of log 2
(LSCO, Nd-LSCO, Bi2201), and every one of their error bars also covers 1. The hypothesis was a per-event value that every
material should share. No group sits at log 2, and the cuprates alone put it 2.4 sigma away.

So the PASS stands as the rule's output, and it is not evidence for C = log 2. The statistic fixed in
advance assumed one population; the data hold at least two. What the data do show is that magic-angle
graphene's C depends on which side of half filling it is doped, which a single universal C cannot give.""")
