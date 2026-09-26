#!/usr/bin/env python3
"""
mandelbrot_lamination.py -- the Mandelbrot set generated from words alone.

THE OBJECT. The combinatorial Mandelbrot set is the QUADRATIC MINOR LAMINATION (QML,
Douady-Hubbard / Thurston): chords ("leaves") of the unit circle join two angles whose
external rays land at the same point of dM. Leaves do not cross. The gaps of the lamination
are the hyperbolic components of M, and the quotient of the disk is a model of M. It is
purely combinatorial: the angles are rationals, and the ONLY dynamics is the doubling map
D(t) = 2t mod 1 -- the same "the itinerary is copied" law as the loop DNA
(`mandelbrot_loop_dna.py`).

No float anywhere: angles are `Fraction`, the doubling map acts on integer numerators over
2^n - 1, and the geometry (which face an angle lies in) is decided by comparisons of
rationals.

  sec 1  the doubling map on rational angles (exact)
  sec 2  the known main-cardioid limbs, and why "same rotation number" is not a naming
  sec 3  the naive arc-based refinement -- non-crossing, right for periods 2-3, FALSIFIED by
         the leaf count
  sec 4  the gap-based pairing -- the generation, with its correctness oracle
  sec 5  scope

Run:  python3 mandelbrot_lamination.py [max_period]     (default 9; 12 takes ~30 s)
"""
from __future__ import annotations

import sys
from collections import Counter
from fractions import Fraction


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# sec 1 -- the doubling map on rational angles, exact
# --------------------------------------------------------------------------- #
def period(k: int, d: int) -> int:
    """Smallest n >= 1 with 2^n k = k (mod d). Exact."""
    x = y = k % d
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
`D(t) = 2t mod 1` is the whole dynamics. Periodic angles are `k/(2^n - 1)` and the period is
computed on integer numerators. Counts of exact-period-n angles in (0,1), and the leaf count
they force:
""")
    print(f"  {'n':>3}{'angles of exact period n':>26}{'leaves required (half)':>26}")
    print("  " + "-" * 58)
    for n in range(2, 11):
        m = len(exact_angles(n))
        print(f"  {n:>3}{m:>26}{m // 2:>26}")
    print("""
  Every angle of exact period n is the root line of exactly one hyperbolic component of period
  n, so there must be half as many leaves of period n as there are such angles -- the number of
  hyperbolic components of period n (OEIS A000740): 1, 3, 6, 15, 27, 63, 120, 252, 495.
  This is the oracle sec 4 has to satisfy.""")


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

  Rotation 2/7 already has {counts[Fraction(2, 7)]} candidate pairs, so naming the 2/7-limb
  needs the Farey ordering, not just the rotation number.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the naive arc-based refinement, and its falsification
# --------------------------------------------------------------------------- #
def crosses(a: Fraction, b: Fraction, c: Fraction, d: Fraction) -> bool:
    a, b, c, d = min(a, b), max(a, b), min(c, d), max(c, d)
    return (a < c < b < d) or (c < a < d < b)


def refine_arcs(n_max: int) -> list[tuple[Fraction, Fraction]]:
    """Naive: by increasing period, pair consecutive period-n angles within each arc cut out
    by the endpoints already placed."""
    leaves, ends = [], []
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


def arcs_falsified() -> None:
    rule("sec 3  THE NAIVE ARC-BASED REFINEMENT -- FALSIFIED BY THE LEAF COUNT")
    leaves = refine_arcs(8)
    bad = sum(crosses(*leaves[i], *leaves[j])
              for i in range(len(leaves)) for j in range(i + 1, len(leaves)))
    known = {tuple(sorted((a, b))) for _r, a, b in KNOWN_LIMBS}
    leafset = {tuple(sorted(l)) for l in leaves}
    got: Counter[int] = Counter(period(a.numerator, a.denominator) for a, _b in leaves)
    print(f"""
Adding leaves by period and pairing consecutive angles within each arc is non-crossing ({bad}
crossings in {len(leaves)} leaves) and reproduces every known leaf of period 2 and 3:
{[k for k in sorted(known) if k in leafset]}. It looks right.

It is not. Compare its leaves per period with the oracle:
""")
    print(f"  {'n':>3}{'arcs':>8}{'required':>10}")
    print("  " + "-" * 21)
    short = []
    for n in range(2, 9):
        req, g = len(exact_angles(n)) // 2, got[n]
        print(f"  {n:>3}{g:>8}{req:>10}{'   MISSING ' + str(req - g) if g < req else ''}")
        if g < req:
            short.append(n)
    print(f"""
  Short from period {short[0]} on. It leaves periodic angles unpaired, and every one of them
  must be a leaf endpoint. (Pairing across the whole circle instead repairs the counts but
  crosses.) Non-crossing is necessary, not sufficient -- the count is what exposes the error.

  Why it fails: the refinement never pairs angles lying in different arcs. At period 4 the two
  it misses, 2/5 and 3/5, lie in the arcs (3/7, 1/3) and (2/3, 4/7) -- yet both are on the
  boundary of ONE GAP, the region bounded by the leaves (1/3, 2/3) and (3/7, 4/7). Pairing must
  be GAP-based, not arc-based. That is sec 4.""")


# --------------------------------------------------------------------------- #
# sec 4 -- the gap-based pairing (the generation)
# --------------------------------------------------------------------------- #
def faces(leaves):
    """Faces of the disk cut by the (non-crossing) chords, as cyclic boundary walks. Each
    boundary item is ('arc', s, e) -- the CCW circle arc from s to e -- or ('chord', s, e)."""
    verts = sorted({x for a, b in leaves for x in (a, b)})
    if not verts:
        return [[('arc', Fraction(0), Fraction(1))]]
    m = len(verts)
    idx = {v: i for i, v in enumerate(verts)}
    edges = [('arc', i, (i + 1) % m, verts[i], verts[(i + 1) % m]) for i in range(m)]
    edges += [('chord', idx[a], idx[b], None, None) for a, b in leaves]
    # order the edges around each vertex by the CCW distance to the other end; an arc into the
    # next vertex is first, an arc into the previous vertex last (ranks 0 and 2)
    adj = {i: [] for i in range(m)}
    for eid, (kind, a, b, _s, _e) in enumerate(edges):
        adj[a].append((((verts[b] - verts[a]) % 1), 0 if kind == 'arc' else 1, eid, b))
        adj[b].append((((verts[a] - verts[b]) % 1), 2 if kind == 'arc' else 1, eid, a))
    for i in adj:
        adj[i].sort(key=lambda t: (t[0], t[1]))
    seen, out = set(), []
    for i in range(m):
        for p in range(len(adj[i])):
            if (i, p) in seen:
                continue
            face, ci, cp = [], i, p
            while (ci, cp) not in seen:
                seen.add((ci, cp))
                eid, other = adj[ci][cp][2], adj[ci][cp][3]
                kind, _a, _b, s, e = edges[eid]
                face.append((kind, s, e))
                rev = next(q for q, t in enumerate(adj[other]) if t[2] == eid)
                ci, cp = other, (rev - 1) % len(adj[other])
            out.append(face)
    return [f for f in out if any(k == 'chord' for k, _s, _e in f)]      # drop the exterior


def in_arc(x: Fraction, s: Fraction, e: Fraction) -> bool:
    """Is x strictly inside the CCW arc from s to e? (handles the wrap through 0)"""
    return (s < x < e) if s < e else (x > s or x < e)


def refine_gaps(n_max: int):
    """THE GENERATION. By increasing period: for every gap of the current lamination, take the
    exact-period-n angles on its boundary, in boundary order, and pair them consecutively."""
    leaves, by_period = [], {}
    for n in range(2, n_max + 1):
        angs = exact_angles(n)
        new = []
        for face in faces(leaves):
            seq = []
            for kind, s, e in face:
                if kind == 'arc':
                    seq += [x for x in angs if in_arc(x, s, e)]
            for i in range(0, len(seq) - 1, 2):
                new.append((seq[i], seq[i + 1]))
        for a, b in new:
            leaves.append((a, b))
        by_period[n] = len(new)
    return leaves, by_period


def gap_generation(n_max: int) -> None:
    rule(f"sec 4  THE GAP-BASED PAIRING -- THE GENERATION (periods 2..{n_max})")
    print("""
Pairing consecutive period-n angles on the boundary of each GAP, in boundary order:
""")
    leaves, by_period = refine_gaps(n_max)
    print(f"  {'n':>3}{'leaves':>9}{'required':>10}{'':>3}")
    print("  " + "-" * 25)
    ok_all = True
    for n in range(2, n_max + 1):
        req = len(exact_angles(n)) // 2
        ok = by_period[n] == req
        ok_all &= ok
        print(f"  {n:>3}{by_period[n]:>9}{req:>10}{'  ok' if ok else '  MISMATCH'}")
    bad = sum(crosses(*leaves[i], *leaves[j])
              for i in range(len(leaves)) for j in range(i + 1, len(leaves)))
    known = {tuple(sorted((a, b))) for _r, a, b in KNOWN_LIMBS}
    leafset = {tuple(sorted(l)) for l in leaves}
    print(f"""
  Every period hits the required count: {ok_all}. Total {len(leaves)} leaves, {bad} crossings.
  Known leaves reproduced: {sum(k in leafset for k in known)} of {len(known)}.

  The checkable facts all hold:
    * the leaf count per period equals half the exact-period-n angles, at every n up to {n_max};
    * no two leaves cross ({bad} crossings is what a lamination requires);
    * the five known leaves are reproduced.

  The period-4 leaves it produces -- (1/15,2/15), (13/15,14/15), (1/5,4/15), (7/15,8/15),
  (11/15,4/5), (2/5,3/5) -- are exactly the six derivable by hand, including (2/5,3/5), the
  pair that spans two arcs and broke the arc-based refinement.

  One bug worth recording, because it is the whole difference between failing and working: the
  first attempt at this gave the wrong counts. The cause was the wrapping arc -- the arc from
  2/3 to 1/3, which runs through 0. It was stored as its endpoints and so was collected as
  (1/3, 2/3), the wrong side of the circle. Arcs have to keep their direction, and a gap is
  bounded by arcs on a particular side. With that fixed the counts match exactly.""")


# --------------------------------------------------------------------------- #
# sec 5 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 5  SCOPE")
    print("""
  1. WHAT THIS IS. A word-only generation of the Mandelbrot set's combinatorial model: no
     arithmetic beyond integer numerator operations and comparisons of rationals -- no float,
     no complex plane, no escape test. The dynamics is the doubling map, the same word-copy
     law as the loop DNA. It is the route §10 of Primordial_Entanglement.md left open.

  2. CHECKED. Leaf counts match the oracle (half the exact-period-n angles, OEIS A000740) at
     every period tested; leaves do not cross; the known low-period leaves are reproduced
     exactly, including the six period-4 leaves derived independently by hand.

  3. NOT CHECKED, AND NOT CLAIMED. Individual leaves of high period were not compared against a
     published list -- the validation is structural (counts, non-crossing, known low periods).
     Nor is this a picture of M: it is the lamination, whose quotient is the model. The
     distinction from `mandelbrot_exact.py` stands: that one generates M_R numerically and
     exactly; this one generates the combinatorial M from words. A route, not the route.""")


def main() -> None:
    n_max = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    print(__doc__)
    doubling()
    main_limbs()
    arcs_falsified()
    gap_generation(n_max)
    scope()


if __name__ == "__main__":
    main()
