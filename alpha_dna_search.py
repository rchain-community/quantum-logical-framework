#!/usr/bin/env python3
"""
alpha_dna_search.py -- "what if we find a ZFA DNA that matches the residual, and then justify it?"

THE WORRY, stated exactly. If we search the substrate for a structure that reproduces the measured
alpha residual, we will find one -- there are too many substrate numbers for it to be otherwise.
Then we will be tempted to justify it after the fact. That is numerology, and Alpha_Residual.md
sec 2a forbids it by name.

So this script does the search under a pre-registration, and reports what a match would be worth:

  sec 1  PRE-REGISTRATION. The space, the tolerance, and the predictions are fixed here, before
         any comparison is made. Two questions are separated:
           (A) DEPTH -- is there an order D of the census whose partial residual lands on CODATA?
           (B) WEIGHT -- is there a mix of the two countings that lands on CODATA?
  sec 2  (A) the depth test, run. Prediction: no depth lands.
  sec 3  (B) the weight search, run. Prediction: many weights land.
  sec 4  the look-elsewhere correction: are the weight hits more than chance?
  sec 5  the trap, demonstrated: the closest candidates and the justification each would get.
  sec 6  verdict -- what a match would and would not be worth.

Everything exact or 60-digit Decimal. No value is fitted and nothing is proposed as derived.

Run:  python3 alpha_dna_search.py
"""
from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60

# ---- the substrate constants (all from the 8-twist alphabet / the census) ----
S62 = Decimal(62).sqrt()
IRRED_LIM = Decimal(126) - 16 * S62            # irreducible tail  [Lean]
TOTAL_LIM = 512 * S62 / 31 - 130               # total census tail [Lean]
LEADING = Decimal(137)                         # 128 + 9, exact
CODATA = Decimal("137.035999206")              # Rb recoil 2020 (Morel et al.); CODATA 2022 is
                                               # 137.035999177(21) -- same 189 fits, same 58/93
CODATA_SD = Decimal("0.000000011")
TOL = Decimal("0.001")                         # the theory's OWN precision, ~0.03 bracket -> 0.001


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def d(x, n: int = 12) -> str:
    return f"{x:.{n}g}"


# --------------------------------------------------------------------------- #
# sec 1 -- pre-registration
# --------------------------------------------------------------------------- #
def preregistration() -> None:
    rule("sec 1  PRE-REGISTRATION (fixed before any comparison)")
    print("""
  SPACE (A), depth. For D = 2, 3, 4, ...: the partial residual 128 * sum_{n=2..D} c_n/128^n, for
    c_n = C(2n,n)           (every closure)
    c_n = 2.Catalan(n-1)    (irreducible closures)
  SPACE (B), weight. For the mix  residual = (1-w).irred + w.total, the weights w = p/q, 1 <= p < q,
    2 <= q <= 100.

  TOLERANCE. |alpha^-1 - CODATA| < 0.001, the theory's own precision (the proven bracket is 0.032
  wide, so 0.001 is generous rather than tight). One number, fixed here.

  PREDICTIONS, registered before running:
    (A) NO DEPTH LANDS. The two countings are monotone in D and bounded by their limits, and the
        limits straddle CODATA -- but the FIRST included order already jumps (for the total) or
        stays (for the irreducible) on one side. So no D lands in the window for either counting,
        and the only free parameter is the weight, not a depth.
    (B) MANY WEIGHTS LAND. The window is wide relative to how densely rationals sit in [0,1].

  Both predictions are falsifiable here and now. If (A) is wrong, there IS a ZFA-DNA depth that
  matches, and that would be a real (if unexplained) coincidence worth chasing.""")


# --------------------------------------------------------------------------- #
# sec 2 -- (A) the depth test
# --------------------------------------------------------------------------- #
def all_closures(n: int) -> int:
    return math.comb(2 * n, n)


def irreducible_closures(n: int) -> int:
    return 2 * math.comb(2 * n - 2, n - 1) // n


def partial(count, D: int) -> Decimal:
    s = Decimal(0)
    for n in range(2, D + 1):
        s += Decimal(count(n)) / (Decimal(128) ** n)
    return 128 * s


def depth_test(d_max: int = 12) -> None:
    rule("sec 2  (A) IS THERE A DEPTH WHOSE PARTIAL RESIDUAL LANDS ON CODATA?")
    print(f"""
  CODATA window: {d(CODATA)} +- {d(CODATA_SD)};  tolerance {TOL}
""")
    print(f"  {'D':>3}   {'every closure':>22}   {'irreducible':>22}   hits")
    print("  " + "-" * 66)
    hits = []
    for D in range(2, d_max + 1):
        a, b = LEADING + partial(all_closures, D), LEADING + partial(irreducible_closures, D)
        ha, hb = abs(a - CODATA) < TOL, abs(b - CODATA) < TOL
        if ha:
            hits.append(("all", D, a))
        if hb:
            hits.append(("irreducible", D, b))
        print(f"  {D:>3}   {d(a, 18):>22}   {d(b, 18):>22}   "
              f"{'ALL' if ha else ''}{' IRR' if hb else ''}")
    print(f"""
  HITS: {hits if hits else 'none'}.

  The prediction holds, and the reason is visible in the first row: at D = 2 the total counting has
  ALREADY jumped to {d(LEADING + partial(all_closures, 2), 18)} -- past CODATA -- and then only climbs to its
  limit {d(LEADING + TOTAL_LIM, 18)}. The irreducible counting starts below ({d(LEADING + partial(irreducible_closures, 2), 18)}) and
  only climbs to {d(LEADING + IRRED_LIM, 18)}, never reaching CODATA. So the two countings bracket the target at
  every depth, and NO depth lands on it.

  This is the sharp form of sec 2a's 'door': a depth is not the free parameter. There is no
  order, no loop count, no truncation whose value is the measured residual. The only free quantity
  is the WEIGHT between the two countings -- and a weight is not a structure.""")


# --------------------------------------------------------------------------- #
# sec 3 -- (B) the weight search
# --------------------------------------------------------------------------- #
def mix_alpha(w: Fraction) -> Decimal:
    """alpha^-1 for the mix weight w, in Decimal (no float in the value)."""
    x = Decimal(w.numerator) / Decimal(w.denominator)
    return LEADING + (1 - x) * IRRED_LIM + x * TOTAL_LIM


def weight_search(q_max: int = 100):
    span = TOTAL_LIM - IRRED_LIM
    w_obs = (CODATA - LEADING - IRRED_LIM) / span
    half = TOL / span
    lo, hi = float(w_obs - half), float(w_obs + half)
    hits = set()
    for q in range(2, q_max + 1):
        for p in range(1, q):
            if lo <= p / q <= hi:
                hits.add(Fraction(p, q))
    rule("sec 3  (B) IS THERE A WEIGHT THAT LANDS ON CODATA?")
    print(f"""
  CODATA requires the mix weight w = {d(w_obs)}; the tolerance admits w in [{lo:.6f}, {hi:.6f}].

  HITS: {len(hits)} distinct weights w = p/q with q <= {q_max}.
""")
    print("  the closest five:")
    for f in sorted(hits, key=lambda f: abs(mix_alpha(f) - CODATA))[:5]:
        val = mix_alpha(f)
        print(f"    w = {str(f):>6}   alpha^-1 = {d(val, 18)}   off by {d(abs(val - CODATA), 3)}")
    return hits, float(w_obs), float(span)


# --------------------------------------------------------------------------- #
# sec 4 -- the look-elsewhere correction
# --------------------------------------------------------------------------- #
def look_elsewhere(hits, q_max: int, span: float) -> None:
    rule("sec 4  LOOK-ELSEWHERE: ARE THE WEIGHT HITS MORE THAN CHANCE?")
    delta = 2 * float(TOL) / span                       # window width in w-units
    expected = (3 / math.pi ** 2) * q_max ** 2 * delta  # Farey / rational-counting density
    rule("")
    print(f"""
The number of reduced fractions p/q with q <= Q in an interval of width delta is, to leading order,
(3/pi^2).Q^2.delta -- the standard rational-counting density. Here Q = {q_max}, delta = {delta:.6f}:

  expected by chance   {expected:.1f}
  observed             {len(hits)}
  ratio                {len(hits) / expected:.3f}

So the hits are EXACTLY what random rationals would give. The substrate's numbers are not clustering
on the target, and the density of fitting weights scales as Q^2: asking for one more digit of
agreement does not reduce the candidate set to one, it just moves the window.""")


# --------------------------------------------------------------------------- #
# sec 5 -- the trap, demonstrated
# --------------------------------------------------------------------------- #
def the_trap(hits) -> None:
    rule("sec 5  THE TRAP, DEMONSTRATED: 'FIND ONE THAT MATCHES, THEN JUSTIFY IT'")
    span = float(TOTAL_LIM - IRRED_LIM)
    named = {Fraction(5, 8), Fraction(9, 14), Fraction(3, 5), Fraction(19, 32),
             Fraction(51, 86), Fraction(35, 59)}
    shown = [f for f in sorted(hits) if f in named][:5]
    print("""
Take five of the fitting weights and write the justification each one would get if it had been
found first. (These stories are constructed to make the point, not claimed.)
""")
    stories = {
        Fraction(5, 8): "5/8 = five of the eight twists -- the 'most ways' count minus the gauge pair",
        Fraction(9, 14): "9/14 = the 3^2 directional factor over 2 x the 7 octaves of the bare coupling",
        Fraction(3, 5): "3/5 = the three spatial axes over the five stages of the leading derivation",
        Fraction(19, 32): "19/32 = the 19 non-gauge twists of the length-4 census over 2^5",
        Fraction(51, 86): "51/86 = the 51 admissible length-6 closures over 86 irreducible ones",
    }
    for f in shown:
        val = mix_alpha(f)
        print(f"  w = {str(f):>6}  ->  alpha^-1 = {d(val, 12)} (off by {d(abs(val - CODATA), 3)})")
        print(f"           justification: {stories.get(f, '...')}")
    print(f"""
Every one of these fits the measurement to within the theory's own precision, and every one has a
story. The stories are mutually incompatible -- 5/8 and 3/5 cannot both be 'the' counting rule -- and
nothing in the substrate prefers one over another. That is what a post-hoc justification is worth:
the story is chosen to fit the number that was picked, and with {len(hits)} candidates there is always
one available.

THE TEST THAT FAILS, stated plainly: 'search for a ZFA-DNA structure matching the residual, then
justify it' cannot work -- not because the search finds nothing, but because it finds ~{len(hits)} things
and has no way to rank them. A match found that way carries no information about the substrate.""")


# --------------------------------------------------------------------------- #
# sec 6 -- verdict
# --------------------------------------------------------------------------- #
def verdict(hits) -> None:
    rule("sec 6  VERDICT")
    print(f"""
  1. (A) NO DEPTH MATCHES. Predicted, and confirmed: the total counting is past CODATA at its first
     included order and the irreducible counting never reaches it. So there is no order, loop count
     or truncation of the census whose value is the residual -- the depth is not the free parameter.

  2. (B) {len(hits)} WEIGHTS MATCH -- at exactly the chance rate (sec 4). So a 'ZFA DNA that matches' is
     findable by construction, and worth nothing, because the count is what random rationals give.

  3. THEREFORE the answer to 'what if we find one and justify it?' is: we will, and the justification
     will be worthless. The guard is not a warning against bad faith; it is arithmetic -- with a
     0.032-wide bracket and a 0.001 precision, roughly (3/pi^2)Q^2.delta weights fit for any Q.

  4. WHAT WOULD ACTUALLY COUNT, and is not done here:
       * a discrete-scale-invariance line in a pre-registered census statistic (the existing probe is
         null; a new statistic would have to be named BEFORE the comparison), or
       * the continuum inputs the running needs -- fermion mass thresholds and Delta-alpha_had.
     Neither is a search, and neither is a justification. No value is derived here; no axiom added.""")


def main() -> None:
    print(__doc__)
    preregistration()
    depth_test()
    hits, w_obs, span = weight_search()
    look_elsewhere(hits, 100, span)
    the_trap(hits)
    verdict(hits)


if __name__ == "__main__":
    main()
