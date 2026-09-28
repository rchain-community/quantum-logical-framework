#!/usr/bin/env python3
"""
alpha_selection.py -- does the census / selection engine constrain the alpha residual?

THE QUESTION. ZFA_DNA.md sec 10 says the framework's method is two steps: *generate every
closure*, then *select the invariant* (least free action, shallowest horizon, most ways). Applied
to the fine-structure constant: the leading value alpha^-1 = 128 + 9 = 137 is exact, the measured
137.035999 leaves a residual +0.036, and the census brackets it between two machine-verified
closed forms. Does the engine *select* the measured value, or only bound it?

WHAT IS COMPUTED HERE (all exact / high precision, no fitting):

  sec 1  the two census tails, verified as SERIES (so the closed forms are not taken on trust):
           counts  C(2n,n)          (every closure)      ->  total
           counts  2.Catalan(n-1)   (irreducible only)   ->  irred
         the tail is 128 x (the census series from order 2 up), and the sums equal the closed
         forms  total = 512.sqrt(62)/31 - 130  and  irred = 126 - 16.sqrt(62)  to 45 digits.
  sec 2  the bracket, and that CODATA sits strictly inside it.
  sec 3  the selection rule applied: each half of the criterion picks an END of the bracket;
         the substrate's actual choice is the scale-invariant one (w = 1/2) -> 137.032002.
  sec 4  many weights reach it: how many simple weights land within 0.001 of CODATA. Each is a
         way; if many are, a single match cannot say which way dominates.
  sec 5  verdict, and scope.

Run:  python3 alpha_selection.py

Companions: Alpha.md (the leading derivation), Alpha_Residual.md sec 1-2a (the door this tests),
genesis.py sec 5b/5c (the octave scale-invariance measurement), lean/QLF_AlphaBound.lean.
"""
from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

S62 = Decimal(62).sqrt()
IRRED = Decimal(126) - 16 * S62                 # 126 - 16.sqrt(62)   [LEAN] irreducible cap
TOTAL = 512 * S62 / 31 - 130                    # 512.sqrt(62)/31 - 130  [LEAN] census cap
LEADING = Decimal(137)                          # 128 + 9, exact
CODATA = Decimal("137.035999206")               # q^2->0 value: Rb recoil 2020 (Morel et al.,
                                                # Nature 588, 61). Not CODATA proper: CODATA 2022
                                                # is 137.035999177(21); same 189 fits, same 58/93.
CODATA_SD = Decimal("0.000000011")


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def d(x, n: int = 12) -> str:
    """Format a Decimal to n significant digits for reading (full precision stays in the maths)."""
    return f"{x:.{n}g}"


# --------------------------------------------------------------------------- #
# sec 1 -- the tails, verified as series
# --------------------------------------------------------------------------- #
def all_closures(n: int) -> int:
    """Every ZFA closure at order n: the central binomial C(2n, n) = 6, 20, 70, 252, ..."""
    return math.comb(2 * n, n)


def irreducible_closures(n: int) -> int:
    """Prime / irreducible closures at order n: 2.Catalan(n-1) = 2, 4, 10, 28, ..."""
    return 2 * math.comb(2 * n - 2, n - 1) // n


def census_tail(count, terms: int = 400) -> Decimal:
    """128 x sum_{n>=2} count(n) / 128^n  -- the residual, one bare coupling 1/128 per order.

    The n = 0 and n = 1 terms (128 and 2 -- the `- 130` in the closed form) are subtracted; the
    residual is what the census adds from order 2 on. The leading 137 = 2^7 + 3^2 is a separate
    derivation (Alpha.md), not a partial sum of this series.
    """
    s = Decimal(0)
    for n in range(2, terms + 1):
        s += Decimal(count(n)) / (Decimal(128) ** n)
    return 128 * s


def tails() -> None:
    rule("sec 1  THE TWO CENSUS TAILS, VERIFIED AS SERIES")
    print("""
Each order n of the closure census contributes one bare coupling alpha_bare = 1/128. Summing
the higher orders gives the residual. Two closed forms carry it, both machine-verified in Lean
(`censusTail_eq`, `irreducibleTail_eq`). Check them against the series rather than trusting them:
""")
    t_all = census_tail(all_closures)
    t_irr = census_tail(irreducible_closures)
    print(f"  every closure   C(2n,n)        series -> {t_all}")
    print(f"                                 closed -> {TOTAL}   [Lean censusTail_eq]")
    print(f"  irreducible     2.Catalan(n-1) series -> {t_irr}")
    print(f"                                 closed -> {IRRED}   [Lean irreducibleTail_eq]")
    assert abs(t_all - TOTAL) < Decimal("1e-45"), "census series != closed form"
    assert abs(t_irr - IRRED) < Decimal("1e-45"), "irreducible series != closed form"
    print(f"""
  Both agree to 45 digits, so the closed forms ARE the resummations of the census from order 2
  up. (Orders 0 and 1 give 128 + 2 = 130, the subtracted part; the leading 137 = 2^7 + 3^2 is
  Alpha.md's separate derivation, not a partial sum of this series.) Nothing here is fitted.

  Counts (integers, exact):  every closure   {all_closures(2)}, {all_closures(3)}, {all_closures(4)}, {all_closures(5)}, ...
                            irreducible     {irreducible_closures(2)}, {irreducible_closures(3)}, {irreducible_closures(4)}, {irreducible_closures(5)}, ...""")


# --------------------------------------------------------------------------- #
# sec 2 -- the bracket
# --------------------------------------------------------------------------- #
def bracket() -> None:
    rule("sec 2  THE BRACKET, AND CODATA INSIDE IT")
    lo = LEADING + IRRED
    hi = LEADING + TOTAL
    print(f"""
  irreducible count  <=  true residual  <=  total count   (each closure screens positively)
  {d(lo)}   <   alpha^-1   <   {d(hi)}

  CODATA {CODATA} +- {CODATA_SD} sits strictly inside:  {lo < CODATA < hi}
  bracket width: {d(hi - lo)}      (this is the theory's precision, ~0.03, not the lab's 1e-11)""")


# --------------------------------------------------------------------------- #
# sec 3 -- the selection rule
# --------------------------------------------------------------------------- #
def selection() -> None:
    rule("sec 3  THE SELECTION RULE: IT BRACKETS, AND THE SUBSTRATE CHOOSES THE MIDDLE")
    print("""
The bracket's two ends are also the two halves of the selection criterion -- a reading, flagged
as such: 'generate every closure / most ways' counts every closure (the total tail), while
'least free action / shallowest' keeps only the irreducible ones. So each half of the engine
picks an END:

  select by MOST WAYS (every closure counted by multiplicity)   w = 1   ->  alpha^-1 = 137.048130
  select by LEAST ACTION (irreducible closures only)            w = 0   ->  alpha^-1 = 137.015874

Neither is what the substrate does. The measured octave hierarchy is scale-invariant -- the
self-similarity ratio tends to 2 with no anomaly and the log-periodic DFT power is a null
(genesis.py sec 5b/5c) -- so no scale is privileged, neither tail is favoured, and the two enter
with EQUAL weight:
""")
    w_sub = Decimal(1) / Decimal(2)
    res_sub = (1 - w_sub) * IRRED + w_sub * TOTAL
    pred = LEADING + res_sub
    print(f"  select by NO PRIVILEGED SCALE (equal weight)                  w = 1/2 ->  alpha^-1 = {d(pred)}")
    print(f"""
  {d(pred)} is the pure-ZFA prediction: a falsifiable number produced before any CODATA comparison.

  What CODATA would require instead:
""")
    w_obs = (CODATA - LEADING - IRRED) / (TOTAL - IRRED)
    print(f"  CODATA-implied weight      w = {d(w_obs)}")
    print(f"""
  So the engine does NOT select the measured value. It constrains the residual to one number,
  {d(res_sub)} (alpha^-1 = {d(pred)}), and brackets the truth to [{d(LEADING + IRRED)}, {d(LEADING + TOTAL)}].
  The distance from the prediction to CODATA is {d(CODATA - pred)}, which is 4 x the whole width of the
  selection gap w: 1/2 -> {d(w_obs)} -- and that gap is the continuum vacuum-polarisation running
  (how many 1PI insertions contribute as q^2 -> 0), which is not a combinatorial truncation at
  all. Alpha_Residual.md sec 2a closes that door; sec 4 below shows why it must stay closed.""")


# --------------------------------------------------------------------------- #
# sec 4 -- many weights reach it: each a way, none yet counted
# --------------------------------------------------------------------------- #
def many_ways(q_max: int = 100, window: float = 0.001) -> None:
    rule("sec 4  MANY WEIGHTS REACH IT -- EACH A WAY, NONE YET COUNTED")
    w_obs = float((CODATA - LEADING - IRRED) / (TOTAL - IRRED))
    span = float(TOTAL - IRRED)
    lo, hi = w_obs - window / span, w_obs + window / span
    hits = set()
    for q in range(2, q_max + 1):
        for p in range(1, q):
            w = p / q
            if lo <= w <= hi:
                hits.add(Fraction(p, q))
    print(f"""
The bracket is wide (~0.03), so 'hitting' CODATA within 0.001 -- the theory's own precision --
is cheap. Count the simple rationals p/q, q <= {q_max}, whose mix lands within {window} of CODATA
(i.e. w within {window / span:.4f} of {w_obs:.4f}):
""")
    print(f"  {len(hits)} rationals with q <= {q_max} land within {window} of CODATA.")
    named = {Fraction(5, 8): "5/8", Fraction(9, 14): "9/14"}
    print("  first few: " + ", ".join(named.get(h, f"{h.numerator}/{h.denominator}")
                                       for h in sorted(hits)[:8]))
    print(f"""
  The measured golden-ratio weight phi - 1 = {(math.sqrt(5) - 1) / 2:.4f} is in the window too.
  Each of these is a way the residual closes -- found in finite time, so it happens: a lower
  bound on multiplicity. What proximity cannot do is rank them, so no single one can be named THE
  way. Moving the mode off w = 1/2 needs a count: a discrete-scale-invariance line appearing in a
  census sector BEFORE the CODATA comparison (genesis.py's pre-registered probe is that test, and
  it is null), or the multiplicity of the continuum running. {len(hits)} ways found; none counted.""")
    return len(hits)


# --------------------------------------------------------------------------- #
# sec 5 -- verdict
# --------------------------------------------------------------------------- #
def verdict(n_hits: int) -> None:
    rule("sec 5  VERDICT, AND SCOPE")
    print(f"""
  1. THE ENGINE CONSTRAINS THE RESIDUAL. Two machine-verified closed forms bracket it,
     137.015874 < alpha^-1 < 137.048130, and the census's own mode (no privileged scale, the most
     ways) is w = 1/2 -> 137.032002, computed before the comparison. It is the same engine
     ZFA_DNA.md sec 10 describes.

  2. THE MEASURED VALUE IS ANOTHER WAY, NOT THE MODE. It needs w = 0.624 and sits 0.004 from the
     mode -- four times the theory's 0.001 precision -- so the two are different numbers. They do
     not conflict: the mode is where multiplicity peaks for the census alone; the measurement is a
     way the census closes once the continuum running is included.

  3. SO THE OPEN QUANTITY IS A MULTIPLICITY. {n_hits} simple weights with q <= 100 reach the measured
     value within 0.001; each is a way (found in finite time, so it happens), none is counted. The
     question left is how many ways carry 137.032 to the measured value -- not whether a fit means
     anything.

  4. WHAT WOULD SUPPLY THE COUNT. A discrete-scale-invariance line in a census sector, pre-registered
     and non-null -- or the fermion mass thresholds and Delta-alpha_had that the continuum
     running needs. Neither is claimed here. Scope: no new value is derived; no axiom added.""")


def main() -> None:
    print(__doc__)
    tails()
    bracket()
    selection()
    n_hits = many_ways()
    verdict(n_hits)


if __name__ == "__main__":
    main()
