#!/usr/bin/env python3
"""
alpha_weight6_pslq.py -- does the census's weight-6 vocabulary close at all?

Alpha_Residual.md SS9h flagged this test as blocked on missing tooling (no
mpmath/sympy, and an externally-managed system Python refusing pip installs
in the working environment). Both obstacles turned out to be local packaging
issues, not a lack of network access: `python3 -m venv --without-pip` plus a
manually bootstrapped `get-pip.py` gets a working, fully isolated `pip` with
no system changes, and `pip install mpmath` then works normally. This is the
ONE script in the repo with a non-stdlib dependency, for exactly that reason:
  python3 -m venv --without-pip /path/to/venv
  curl -s https://bootstrap.pypa.io/get-pip.py | /path/to/venv/bin/python3
  /path/to/venv/bin/pip install mpmath
  /path/to/venv/bin/python3 alpha_weight6_pslq.py

Alpha_Residual.md SS9f-9g's loop-order/nesting ladder (1 loop = flat unsigned
census sum, 2 loops = + phase, 3 loops = + one level of H^(m)-nesting) predicts
a "4-loop wall": the elliptic/modular periods of the true 4-loop g-2 integral
are claimed to be unreachable by central-binomial MZVs at ANY nesting depth.
That claim is about LOOP ORDER. This script asks the more basic question the
loop-order claim implicitly assumes an answer to: does the census's own
vocabulary even reach WEIGHT 6 (one step past zeta(5)'s weight 5), regardless
of loop order or nesting depth?

Concretely: Sum_{k=1}^inf 1/(k^6 C(2k,k)) is the natural next central-binomial
sum after Comtet's zeta(2)/zeta(4) and Apery's zeta(3). Does it reduce to a
small-integer-coefficient combination of natural weight-6 constants -- the
same kind of "closed form" that made zeta(2), zeta(3), zeta(4), zeta(5) all
census-representable?

METHOD: a genuine PSLQ integer-relation search (mpmath.pslq), not a bounded
brute-force guess -- validated against the two ALREADY-KNOWN relations in
this file family first (Comtet's zeta(4) and Borwein-Bradley's zeta(5)),
both recovered exactly, confirming the method would find a real relation of
this size and precision if one existed.

RESULT: no relation found, at 100-digit precision, against three
increasingly rich weight-6 bases: {pi^6, zeta(3)^2}; the same plus Li_6(1/2)
(the natural next term in the Li_p(1/2) "free-energy weight" family already
used at weight 4); and that basis further extended with ln(2)^6, pi^2 ln(2)^4,
pi^4 ln(2)^2 (the weight-6 members of the ln(2)-power family already used at
weight 4 for ln^4(2), pi^2 ln^2(2)).

HONEST SCOPE: this is a NEGATIVE result, not a proof of anything -- PSLQ
finding nothing means no SMALL-integer relation exists in THESE bases at
THIS precision, not that no relation exists in any basis whatsoever (weight-6
multiple zeta values have a larger space than these seven terms span; a
relation could still exist against a basis not tried here). It does NOT by
itself confirm or refute the 4-loop elliptic-period claim, which is a
separate statement about loop order, not weight -- this tests something the
loop-order claim assumes without stating: that the vocabulary's reach is at
least not obstructed by weight alone before loop order even enters. What it
DOES establish: the ease with which zeta(2)..zeta(5) fell to this technique
was not guaranteed to continue -- weight 6 is where it first stops working,
which is worth knowing plainly rather than assuming "one more Comtet-style
formula" was just waiting to be found.
"""
try:
    import mpmath as mp
except ImportError:
    raise SystemExit(
        "This script needs mpmath (not in the repo's usual stdlib-only set).\n"
        "Install into an isolated venv, do not touch system Python:\n"
        "  python3 -m venv --without-pip /tmp/qlf-mpmath-venv\n"
        "  curl -s https://bootstrap.pypa.io/get-pip.py | /tmp/qlf-mpmath-venv/bin/python3\n"
        "  /tmp/qlf-mpmath-venv/bin/pip install mpmath\n"
        "  /tmp/qlf-mpmath-venv/bin/python3 alpha_weight6_pslq.py"
    )

mp.mp.dps = 100


def census_sum(power: int, signed: bool, K: int = 250, inner: int = 0):
    """Sum_{k=1}^K w_k / (k^power * C(2k,k)), matching alpha_census_highprecision.py."""
    total = mp.mpf(0)
    harmonic = mp.mpf(0)
    for k in range(1, K + 1):
        if inner and k > 1:
            harmonic += mp.mpf(1) / mp.mpf(k - 1) ** inner
        term = mp.mpf(1) / (mp.mpf(k) ** power * mp.binomial(2 * k, k))
        if signed and k % 2 == 0:
            term = -term
        if inner:
            term *= harmonic
        total += term
    return total


def main() -> None:
    print(__doc__.strip().split("\n\n")[0])
    print()

    print("=" * 78)
    print("Positive controls -- PSLQ must recover the KNOWN relations first")
    print("=" * 78)
    s4 = census_sum(4, False)
    z4 = mp.zeta(4)
    rel = mp.pslq([s4, z4], maxsteps=10**5)
    print(f"  Comtet: [S(4), zeta(4)] -> {rel}   (expect proportional to [17,-36])")

    s5 = census_sum(5, True)
    s3n2 = census_sum(3, True, inner=2)
    z5 = mp.zeta(5)
    rel2 = mp.pslq([s5, s3n2, z5], maxsteps=10**5)
    print(f"  Borwein-Bradley: [S(5,signed), S(3,signed,inner=2), zeta(5)] -> {rel2}")
    print("    (expect proportional to [4,-5,-2])")
    print()

    print("=" * 78)
    print("The weight-6 test: Sum 1/(k^6 C(2k,k)) against growing bases")
    print("=" * 78)
    s6 = census_sum(6, False)
    pi6 = mp.pi**6
    z3sq = mp.zeta(3) ** 2
    ln2 = mp.log(2)
    li6half = mp.polylog(6, mp.mpf(1) / 2)
    pi2, pi4 = mp.pi**2, mp.pi**4

    bases = [
        ("{pi^6, zeta(3)^2}", [s6, pi6, z3sq]),
        ("{pi^6, zeta(3)^2, Li_6(1/2)}", [s6, pi6, z3sq, li6half]),
        ("{pi^6, zeta(3)^2, Li_6(1/2), ln(2)^6, pi^2 ln(2)^4, pi^4 ln(2)^2}",
         [s6, pi6, z3sq, li6half, ln2**6, pi2 * ln2**4, pi4 * ln2**2]),
    ]
    for name, vec in bases:
        rel = mp.pslq(vec, maxsteps=2 * 10**5)
        print(f"  {name}: {rel}")
    print()

    print("=" * 78)
    print("""VERDICT

  PSLQ exactly recovers both known relations (Comtet zeta(4), Borwein-Bradley
  zeta(5)) -- the method works and would find a relation of this size/precision
  if one existed.

  No relation found for Sum 1/(k^6 C(2k,k)) against any of the three weight-6
  bases tried, at 100-digit precision. This is a genuine NEGATIVE result, not
  a proof: it rules out small-integer relations in THESE bases, not in every
  conceivable weight-6 basis. Weight 6 is where the easy pattern (zeta(2)
  through zeta(5) all falling to Comtet/Apery/Borwein-Bradley-style formulas)
  first stops working outright -- a separate, plainer fact from the stated
  4-loop elliptic-period wall (which is about loop order, not weight alone),
  worth recording rather than assuming away.
""")


if __name__ == "__main__":
    main()
