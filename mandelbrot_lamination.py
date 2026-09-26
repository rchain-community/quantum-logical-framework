#!/usr/bin/env python3
"""
mandelbrot_lamination.py -- the combinatorial Mandelbrot set as a circle lamination:
what works, and where the naive algorithm breaks.

THE QUESTION (Jim, 2026-09-26): take on the word-only / combinatorial generation of the
Mandelbrot set. The classical object is the QUADRATIC MINOR LAMINATION (QML, Douady-Hubbard /
Thurston): chords ("leaves") of the unit circle connect two angles whose external rays land at
the same point of dM. Leaves do not cross; the gaps of the lamination are the hyperbolic
components of M. It is purely combinatorial: the angles are rationals and the dynamics is the
doubling map D(t) = 2t mod 1 -- the same "the itinerary is copied" law as the loop DNA.

No floats anywhere: angles are `Fraction`, and the doubling map acts on integer numerators
over 2^n - 1.

  sec 1  the doubling map on rational angles (exact)
  sec 2  the known main-cardioid limbs, and why "same rotation number" is not a naming
  sec 3  the naive Lavaurs-style refinement -- non-crossing, right for periods 2-3, then
         FALSIFIED by the leaf count
  sec 4  what the correct construction needs
  sec 5  scope

Run:  python3 mandelbrot_lamination.py
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# sec 1 -- the doubling map on rational angles, exact
# --------------------------------------------------------------------------- #
def period(k: int, d: int) -> int:
    """Smallest n >= 1 with 2^n k = k (mod d). Exact."""
    x = k % d
    y = x
    n = 0
    while True:
        n += 1
        y = (2 * y) % d
        if y == x:
            return n


def exact_angles(n: int) -> list[Fraction]:
    """Angles in (0,1) of exact period n under doubling: k/(2^n - 1)."""
    d = 2 ** n - 1
    return [Fraction(k, d) for k in range(1, d) if period(k, d) == n]


def orbit(t: Fraction) -> list[Fraction]:
    out, x = [], t
    while True:
        out.append(x)
        x = (2 * x) % 1
        if x == t:
            return out


def rotation_number(t: Fraction) -> Fraction:
    """Fraction of the doubling orbit spent in [1/2, 1)."""
    o = orbit(t)
    return Fraction(sum(1 for x in o if x >= Fraction(1, 2)), len(o))


def doubling() -> None:
    rule("sec 1  THE DOUBLING MAP ON RATIONAL ANGLES (exact, no float)")
    print("""
`D(t) = 2t mod 1` is the whole dynamics -- the same "the itinerary is copied" law as the loop
DNA (`mandelbrot_loop_dna.py`). Periodic angles are `k/(2^n - 1)`; the period is computed on
integer numerators. Counts of exact-period-n angles in (0,1), and the leaf count they force:
""")
    print(f"  {'n':>3}{'angles of exact period n':>26}{'leaves required (half)':>26}")
    print("  " + "-" * 58)
    for n in range(2, 9):
        m = len(exact_angles(n))
        print(f"  {n:>3}{m:>26}{m // 2:>26}")
    print("""
  Every angle of exact period n is the root line of exactly one hyperbolic component of period
  n, so the number of QML leaves of period n is half the number of such angles -- the count of
  hyperbolic components of period n (OEIS A000740): 1, 3, 6, 15, 27, 63, 120 for n = 2..8.
  Nothing here uses the complex plane.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the known limbs, and the naming problem
# --------------------------------------------------------------------------- #
KNOWN_LIMBS = [
    (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3)),
    (Fraction(1, 3), Fraction(1, 7), Fraction(2, 7)),
    (Fraction(2, 3), Fraction(5, 7), Fraction(6, 7)),
    (Fraction(1, 4), Fraction(1, 15), Fraction(2, 15)),
    (Fraction(3, 4), Fraction(13, 15), Fraction(14, 15)),
]


def main_limbs() -> None:
    rule("sec 2  THE KNOWN MAIN-CARDIOD LIMBS -- AND WHY THE CRITERION OVER-PRODUCES")
    print("""
A main-cardioid limb of internal angle p/q has two root angles: consecutive fractions
`k/(2^q-1)` and `(k+1)/(2^q-1)` with the same rotation number p/q. Check the known leaves
against exactly that criterion, all in `Fraction`:
""")
    for rot, a, b in KNOWN_LIMBS:
        q = period(a.numerator, a.denominator)
        consecutive = (b - a == Fraction(1, 2 ** q - 1))
        same = rotation_number(a) == rotation_number(b) == rot
        print(f"  internal {rot}   root angles {a}, {b}    consecutive {consecutive}, "
              f"same rotation {same}")
        assert consecutive and same
    pairs = set()
    for q in range(2, 8):
        d = 2 ** q - 1
        for k in range(1, d):
            if period(k, d) == q and period(k + 1, d) == q:
                a, b = Fraction(k, d), Fraction(k + 1, d)
                if rotation_number(a) == rotation_number(b):
                    pairs.add((rotation_number(a), a, b))
    counts = Counter(r for r, _a, _b in pairs)
    print(f"""
  All five known limbs pass. But the criterion does NOT name the limbs: it over-produces.
  Consecutive pairs sharing a rotation number, up to q = 7: {dict(sorted(counts.items()))}

  Rotation 2/7 already has {counts[Fraction(2, 7)]} candidate pairs. Naming the 2/7-limb needs
  the Farey ordering, not just the rotation number -- so even step one needs more than the
  obvious rule.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the naive refinement, and its falsification by the count
# --------------------------------------------------------------------------- #
def crosses(a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> bool:
    a, b, c, d = min(a, b), max(a, b), min(c, d), max(c, d)
    return (a < c < b < d) or (c < a < d < b)


def refine(n_max: int = 8) -> list[tuple[Fraction, Fraction]]:
    """Naive Lavaurs-style refinement: add leaves by increasing period, pairing, within each
    arc cut out by the endpoints already placed, the exact-period-n angles consecutively."""
    leaves: list[tuple[Fraction, Fraction]] = []
    ends: list[Fraction] = []
    for n in range(2, n_max + 1):
        s = sorted(exact_angles(n))
        cuts = sorted(set(ends))
        arcs = [None] if not cuts else list(zip(cuts, cuts[1:] + cuts[:1]))
        new = []
        for arc in arcs:
            if arc is None:
                here = s
            else:
                lo, hi = arc
                here = ([x for x in s if lo < x < hi] if lo < hi
                        else [x for x in s if x > lo or x < hi])
            here = sorted(here)
            for i in range(0, len(here) - 1, 2):
                new.append((here[i], here[i + 1]))
        for a, b in new:
            leaves.append((a, b))
            ends += [a, b]
    return leaves


def naive_and_falsify() -> None:
    rule("sec 3  THE NAIVE REFINEMENT -- NON-CROSSING, THEN FALSIFIED BY THE COUNT")
    leaves = refine(8)
    bad = [(leaves[i], leaves[j]) for i in range(len(leaves)) for j in range(i + 1, len(leaves))
           if crosses(leaves[i][0], leaves[i][1], leaves[j][0], leaves[j][1])]
    known = {tuple(sorted((a, b))) for _r, a, b in KNOWN_LIMBS}
    leafset = {tuple(sorted(l)) for l in leaves}
    print(f"""
The refinement gives {len(leaves)} leaves up to period 8, with {len(bad)} crossings: the
non-crossing property (necessary for a lamination) holds. It reproduces the known leaves of
period 2 and 3: {[k for k in sorted(known) if k in leafset]}.

Now the count. Compare its leaves per period with the required count from sec 1:
""")
    by_period: Counter[int] = Counter()
    for a, _b in leaves:
        by_period[period(a.numerator, a.denominator)] += 1
    print(f"  {'n':>3}{'refinement':>14}{'required':>12}{'':>4}")
    print("  " + "-" * 33)
    fails = []
    for n in range(2, 9):
        req = len(exact_angles(n)) // 2
        got = by_period[n]
        print(f"  {n:>3}{got:>14}{req:>12}{'  MISSING ' + str(req - got) if got < req else ''}")
        if got < req:
            fails.append((n, got, req))
    print(f"""
  It is short from period 4 on: {[(n, g, r) for n, g, r in fails]}. So the refinement is NOT the
  QML -- it leaves periodic angles unpaired, and every one of them must be a leaf endpoint.

  A first, tempting fix also fails. Pairing consecutively across the WHOLE circle (not within
  an arc) gets the counts right but crosses: at period 4 it already gives the crossing pair
  (2/5, 7/15), whose endpoints interleave the period-3 leaf (3/7, 4/7) (.4 < .4286 < .4667).
  The target is therefore a NON-CROSSING PERFECT MATCHING of the period-n angles.

  Diagnosis of the miss. The refinement never pairs angles that lie in different arcs -- but
  the two angles it misses at period 4, 2/5 and 3/5, are exactly such a pair: they lie in the
  arcs (3/7, 1/3) and (2/3, 4/7), yet both are on the boundary of the single GAP bounded by the
  leaves (1/3, 2/3) and (3/7, 4/7). Pairing must be GAP-based, not arc-based.""")


# --------------------------------------------------------------------------- #
# sec 4 -- what the correct construction needs
# --------------------------------------------------------------------------- #
def needs() -> None:
    rule("sec 4  WHAT THE CORRECT CONSTRUCTION STILL NEEDS")
    print("""
The real Lavaurs algorithm is a RENORMALISATION recursion over gaps, not a period-wise pairing:

  1. A gap with minor leaf {a,b} of period p carries a first-return map of the doubling to its
     boundary; rescaled, that is again the doubling map. The gap therefore holds a copy of the
     whole lamination, and its children have period p.m.
  2. The children's root leaves are the preimages, under that renormalisation map, of the
     main-cardioid limb leaves of sec 2 -- which is why pairing must be gap-based.
  3. Iterating gives every component, and the child periods are forced to be multiples of the
     parent's.

So the validated base is in place: exact doubling combinatorics (sec 1), the known limbs
verified (sec 2), and a clean falsification with the exact target (sec 3). What is missing is
the gap-based renormalisation step -- well-defined, but not implemented here.

A direct attempt at it was made, and it is worth recording that it failed too: pairing the
period-n angles on each FACE of the planar subdivision by the non-crossing chords gave the
wrong counts and crossing leaves (4 leaves at period 3 where 3 are required, 8 at period 4
where 6 are required). So the obstacle is not merely "arc versus gap": the renormalisation map
itself -- which pair of angles a gap's children join -- is what has to be got right. Getting it
wrong is easy to detect (counts and crossings), which is what makes it tractable next.""")


# --------------------------------------------------------------------------- #
# sec 5 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 5  SCOPE")
    print("""
  1. DEMONSTRATED. Exact doubling combinatorics (no float); the known main-cardioid limbs
     verified against the rotation-number criterion; the leaf count per period.

  2. FALSIFIED. The naive period-wise refinement is NOT the QML: from period 4 on it leaves
     periodic angles unpaired (5 leaves where 6 are required at period 4), and the angles it
     misses are a pair spanning two arcs of one gap. Non-crossing alone is not enough; the
     count is what exposes it.

  3. NOT DONE. The gap-based renormalisation recursion (sec 4). Until it is implemented and
     validated there is no word-only generation of M; `mandelbrot_exact.py` remains the exact
     route. A route, not the route.""")


def main() -> None:
    print(__doc__)
    doubling()
    main_limbs()
    naive_and_falsify()
    needs()
    scope()


if __name__ == "__main__":
    main()
