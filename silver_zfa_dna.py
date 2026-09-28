#!/usr/bin/env python3
"""
silver_zfa_dna.py -- the silver thread: the value the substrate's own lattice makes.

THE QUESTION (Jim, 2026-09-28): "in nature phi is sort of a special case, most have different values,
we are interested in production of values that actually happen in nature." golden_zfa_dna.py found
that counting cannot select phi. So ask the other way round: which irrational does the substrate's
OWN structure produce?

The closure walk lives on Z^4 (Closure_Walk.md): the eight twists are the eight signed unit vectors
+-e_a. Additively that is exactly Z[zeta_8], the ring of eighth roots of unity -- e_a -> zeta^a, with
zeta^4 = -1 carrying each twist to its conjugate. Its real subring is Z[sqrt 2], whose fundamental
unit is the SILVER RATIO 1 + sqrt 2. phi lives in Z[zeta_5], a different lattice.

  sec 1  the silver twist DNA: t -> t- t t+ (each twist flanked by its octagonal neighbours).
         ZFA at every depth; it scales the plane by exactly 1 + sqrt 2.
  sec 2  cut-and-project from Z^4: the octagonal (Ammann-Beenker) quasicrystal, exactly in Z[sqrt 2],
         with its 8-fold symmetry and its silver self-similarity checked.
  sec 3  a proposition, proved and checked: an integer inflation of Z^4 that respects the octagonal
         structure (commutes with the order-8 rotation and a reflection) and is invertible on the
         lattice has eigenvalues +-(1 + sqrt 2)^k and nothing else -- never phi, never 2 + sqrt 3.
  sec 4  scope, and the natural record: octagonal quasicrystals are observed (Wang, Chen & Kuo 1987).

Exact arithmetic: numbers in Q(sqrt 2) are pairs (p, q) = p + q.sqrt 2 of Fractions; comparisons are
decided by squaring. Floats only for display and the SVG.

Run:  python3 silver_zfa_dna.py
      python3 silver_zfa_dna.py --svg      (writes diagrams/zfa_silver_octagonal.svg)

Companions: ZFA_DNA.md sec 12 (the write-up), golden_zfa_dna.py (phi, which counting cannot select),
Closure_Walk.md (the Z^4 walk), natural_ratios.py (the comparison with nature).
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction

from qucalc_search import max_excursion
from twist_core import is_zfa

# the octagonal order of the eight twists: +e0 +e1 +e2 +e3 -e0 -e1 -e2 -e3  (axes ^v >< /\ +-)
RING = ['^', '>', '/', '+', 'v', '<', '\\', '-']


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# exact Q(sqrt 2)
# --------------------------------------------------------------------------- #
class Q2:
    """p + q.sqrt(2), p and q Fractions."""
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p, self.q = Fraction(p), Fraction(q)

    def __add__(self, o): return Q2(self.p + o.p, self.q + o.q)
    def __sub__(self, o): return Q2(self.p - o.p, self.q - o.q)
    def __neg__(self): return Q2(-self.p, -self.q)
    def __mul__(self, o): return Q2(self.p * o.p + 2 * self.q * o.q, self.p * o.q + self.q * o.p)
    def __eq__(self, o): return self.p == o.p and self.q == o.q
    def __hash__(self): return hash((self.p, self.q))
    def __float__(self): return float(self.p) + float(self.q) * math.sqrt(2)

    def sign(self) -> int:
        """Exact sign of p + q.sqrt 2."""
        p, q = self.p, self.q
        if p >= 0 and q >= 0:
            return 0 if p == 0 and q == 0 else 1
        if p <= 0 and q <= 0:
            return -1
        # opposite signs: compare p^2 with 2 q^2
        if p > 0:
            return 1 if p * p > 2 * q * q else (-1 if p * p < 2 * q * q else 0)
        return 1 if 2 * q * q > p * p else (-1 if 2 * q * q < p * p else 0)

    def __le__(self, o): return (o - self).sign() >= 0


HALF_R2 = Q2(0, Fraction(1, 2))          # 1/sqrt 2 = sqrt 2 / 2


def physical(n) -> tuple[Q2, Q2]:
    """Z^4 -> the plane: e_a -> zeta_8^a.  zeta = (1 + i)/sqrt 2."""
    n0, n1, n2, n3 = (Q2(x) for x in n)
    return n0 + (n1 - n3) * HALF_R2, n2 + (n1 + n3) * HALF_R2


def internal(n) -> tuple[Q2, Q2]:
    """Z^4 -> the internal plane: e_a -> zeta_8^(3a)  (the Galois partner, sqrt 2 -> -sqrt 2)."""
    n0, n1, n2, n3 = (Q2(x) for x in n)
    return n0 + (n3 - n1) * HALF_R2, -n2 + (n1 + n3) * HALF_R2


def rotate(n):
    """Multiplication by zeta on Z[zeta_8]: e0->e1->e2->e3->-e0."""
    n0, n1, n2, n3 = n
    return (-n3, n0, n1, n2)


def inflate(n):
    """The silver inflation t -> t- + t + t+ on counts: multiplication by 1 + zeta + zeta^-1 = 1 + sqrt 2."""
    a = n
    b = rotate(n)
    c = rotate(rotate(rotate(rotate(rotate(rotate(rotate(n)))))))   # zeta^-1 = zeta^7
    return tuple(x + y + z for x, y, z in zip(a, b, c))


# --------------------------------------------------------------------------- #
# sec 1 -- the silver twist DNA
# --------------------------------------------------------------------------- #
def pell(n: int) -> int:
    """Pell numbers 0, 1, 2, 5, 12, 29, 70, 169, ... -- the silver ratio's Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, 2 * b + a
    return a


def silver_substitution(ring: list[str]) -> dict[str, str]:
    return {t: ring[(i - 1) % 8] + t + ring[(i + 1) % 8] for i, t in enumerate(ring)}


def sec1() -> None:
    rule("sec 1  THE SILVER TWIST DNA: t -> t- t t+ (OCTAGONAL NEIGHBOURS)")
    sub = silver_substitution(RING)
    print("""
Arrange the eight twists in the octagonal order of Z[zeta_8] -- ^ > / + v < \\ - , each next one a
45-degree turn, each opposite one its conjugate -- and replace every twist by itself flanked by its
two neighbours:
""")
    for t in RING:
        print(f"      {t}  ->  {sub[t]}")
    print(f"\n  {'k':>3}{'twists':>9}{'ZFA':>6}{'max exc':>9}{'ratio':>10}")
    w = '^>v<'
    excs = []
    for k in range(1, 7):
        w = ''.join(sub[c] for c in w)
        assert is_zfa(w)
        excs.append(max_excursion(w))
        assert excs[-1] == 3 * pell(k + 1), "excursion is not 3 x Pell"
        ratio = f"{excs[-1] / excs[-2]:.4f}" if len(excs) > 1 else ""
        print(f"  {k:>3}{len(w):>9}{'yes':>6}{excs[-1]:>9}{ratio:>10}")
    print("""
It closes at every depth, for the reason every conjugate-respecting substitution does: the image of
a twist's conjugate is the conjugate of its image, so count balance is carried forward, and by
count_balanced_pauli_closed the Pauli closure comes free. Unlike the block DNAs (excursion 2 at
every depth), this one is heard only at growing capacity -- and the capacity it needs grows by the
same factor as its scale. Exactly: the max excursion at depth k is 3 x Pell(k+1) -- 3 x (2, 5, 12,
29, 70, 169) -- and the Pell numbers are to the silver ratio what the Fibonacci numbers are to phi.

ITS SCALE. On counts the rule is multiplication by 1 + zeta + zeta^-1 in Z[zeta_8]. The eigenvalues
are 1 + 2 cos(k pi/4) for k = 1, 3, 5, 7:""")
    ev = sorted(1 + 2 * math.cos(k * math.pi / 4) for k in (1, 3, 5, 7))
    print("      " + ", ".join(f"{e:.12f}" for e in ev))
    print(f"      1 + sqrt 2 = {1 + math.sqrt(2):.12f},  1 - sqrt 2 = {1 - math.sqrt(2):.12f}")
    assert abs(ev[-1] - (1 + math.sqrt(2))) < 1e-12 and abs(ev[0] - (1 - math.sqrt(2))) < 1e-12

    # the construction's multiplicity: identifications of the signed frame with mu_8
    rules = set()
    for perm in itertools.permutations(range(4)):
        for signs in itertools.product((1, -1), repeat=4):
            ring = [None] * 8
            for a in range(4):
                pos = perm[a] if signs[a] == 1 else (perm[a] + 4) % 8
                ring[pos] = RING[a]
                ring[(pos + 4) % 8] = RING[a + 4]
            rules.add(tuple(sorted(silver_substitution(ring).items())))
    print(f"""
MULTIPLICITY OF THE CONSTRUCTION. The twists can be laid on the octagon in 4! x 2^4 = 384 ways
(the hyperoctahedral group). They give {len(rules)} distinct substitutions (turning the octagon
changes nothing; reflecting it swaps t- and t+). Every one uses all four axes, so every octagon
places the gauge axis +- beside the spatial ones -- a choice the Pauli algebra does not make,
recorded as the construction's caveat.""")


# --------------------------------------------------------------------------- #
# sec 2 -- cut and project
# --------------------------------------------------------------------------- #
H = Q2(Fraction(1, 2), Fraction(1, 2))          # (1 + sqrt 2)/2 : the octagon's inradius
H2 = Q2(1, Fraction(1, 2))                      # (2 + sqrt 2)/2 = sqrt 2 . H


def in_window(n) -> bool:
    """Is the internal image inside the octagonal window (the projected unit tesseract)?"""
    x, y = internal(n)
    return all(abs_le(v, b) for v, b in ((x, H), (y, H), (x + y, H2), (x - y, H2)))


def abs_le(v: Q2, b: Q2) -> bool:
    return v <= b and -v <= b


def model_set(r: int):
    pts = set()
    for n in itertools.product(range(-r, r + 1), repeat=4):
        if in_window(n):
            pts.add(n)
    return pts


def sec2(make_svg: bool) -> None:
    rule("sec 2  CUT AND PROJECT: THE OCTAGONAL QUASICRYSTAL FROM Z^4, EXACTLY")
    r = 5
    pts = model_set(r)
    R2 = Q2(9)                                              # physical radius^2 for the checks
    def inside(n):
        x, y = physical(n)
        return (x * x + y * y) <= R2
    ball = {n for n in pts if inside(n)}
    rot_ok = all(rotate(n) in pts for n in ball)
    mirror = lambda n: (n[0], -n[3], -n[2], -n[1])        # complex conjugation on Z[zeta_8]
    mir_ok = all(mirror(n) in pts for n in ball)
    infl_ok = all(in_window(inflate(n)) for n in ball)
    print(f"""
Lift the plane to Z^4 twice: physically e_a -> zeta^a, internally e_a -> zeta^(3a) (the Galois
partner). Keep the lattice points whose internal image lies in the octagon that the unit tesseract
projects to -- inradius (1 + sqrt 2)/2 -- and draw their physical images. All in Q(sqrt 2), exactly.

  lattice points kept (coordinates within +-{r}):   {len(pts)}
  of them within physical radius 3:                {len(ball)}
  8-fold: rotating by 45 degrees maps the set to itself        {rot_ok}
  mirror: reflecting maps the set to itself                    {mir_ok}
  silver self-similarity: inflating by 1 + sqrt 2 keeps every point in the set   {infl_ok}

The inflation shrinks the internal image by |1 - sqrt 2| = 0.414..., so an inflated point never
leaves the window: the point set is exactly self-similar under the silver ratio. This is the vertex
set of the Ammann-Beenker octagonal tiling (Beenker 1982; Ammann, Grunbaum & Shephard 1992).""")
    assert rot_ok and mir_ok and infl_ok
    if make_svg:
        big = {n for n in model_set(7) if (lambda x, y: x * x + y * y <= Q2(20))(*physical(n))}
        svg(big)


def svg(points, path: str = "diagrams/zfa_silver_octagonal.svg") -> None:
    xy = [(float(physical(n)[0]), float(physical(n)[1])) for n in points]
    s, cx = 50, 230
    edges = []
    unit = [physical(e) for e in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
    pset = set(points)
    for n in points:
        for a in range(4):
            m = tuple(n[i] + (1 if i == a else 0) for i in range(4))
            if m in pset:
                edges.append((n, m))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 460" width="460" height="460">',
           '<rect width="460" height="460" fill="#ffffff"/>']
    for n, m in edges:
        (x1, y1), (x2, y2) = [(float(physical(p)[0]), float(physical(p)[1])) for p in (n, m)]
        out.append(f'<line x1="{cx + s * x1:.2f}" y1="{cx - s * y1:.2f}" x2="{cx + s * x2:.2f}" '
                   f'y2="{cx - s * y2:.2f}" stroke="#4f46e5" stroke-width="1.2"/>')
    for x, y in xy:
        out.append(f'<circle cx="{cx + s * x:.2f}" cy="{cx - s * y:.2f}" r="2.2" fill="#1e1b4b"/>')
    out.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"\n  wrote {path} ({len(points)} vertices, {len(edges)} unit edges)")


# --------------------------------------------------------------------------- #
# sec 3 -- which inflations the octagonal lattice allows
# --------------------------------------------------------------------------- #
def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def det(M):
    M = [[Fraction(x) for x in r] for r in M]
    d = Fraction(1)
    for c in range(4):
        piv = next((r for r in range(c, 4) if M[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            M[c], M[piv] = M[piv], M[c]
            d = -d
        d *= M[c][c]
        for r in range(c + 1, 4):
            f = M[r][c] / M[c][c]
            M[r] = [M[r][j] - f * M[c][j] for j in range(4)]
    return d


def sec3() -> None:
    rule("sec 3  WHICH INFLATIONS THE OCTAGONAL LATTICE ALLOWS -- PROVED, THEN CHECKED")
    rho = [[0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]     # multiplication by zeta
    ref = [[1, 0, 0, 0], [0, 0, 0, -1], [0, 0, -1, 0], [0, -1, 0, 0]]  # complex conjugation
    # commutant of rho: solve M rho = rho M over Q (16 unknowns)
    rows = []
    for i in range(4):
        for j in range(4):
            row = [0] * 16
            for k in range(4):
                row[i * 4 + k] += rho[k][j]          # (M rho)_ij
                row[k * 4 + j] -= rho[i][k]          # (rho M)_ij
            rows.append([Fraction(x) for x in row])
    rank, r = 0, [row[:] for row in rows]
    for c in range(16):
        piv = next((i for i in range(rank, len(r)) if r[i][c] != 0), None)
        if piv is None:
            continue
        r[rank], r[piv] = r[piv], r[rank]
        for i in range(len(r)):
            if i != rank and r[i][c] != 0:
                f = r[i][c] / r[rank][c]
                r[i] = [a - f * b for a, b in zip(r[i], r[rank])]
        rank += 1
    dim = 16 - rank
    print(f"""
PROPOSITION. Let M be an integer 4x4 matrix acting on Z^4 = Z[zeta_8] that respects the octagonal
structure -- it commutes with the 45-degree rotation rho and with the reflection -- and is invertible
on the lattice (det = +-1). Then M is multiplication by a unit of Z[sqrt 2], and its eigenvalues are
+-(1 + sqrt 2)^k. In particular phi (in Q(sqrt 5)) and 2 + sqrt 3 (in Q(sqrt 3)) never occur.

PROOF. rho has minimal polynomial x^4 + 1, irreducible over Q, so the matrices commuting with it are
exactly the polynomials in rho: the field Q(zeta_8). Commuting also with the reflection (complex
conjugation) leaves the real subfield Q(zeta + zeta^-1) = Q(sqrt 2); integrality leaves Z[sqrt 2],
and det = N(a + b sqrt 2)^2 = +-1 makes it a unit. The units of Z[sqrt 2] are +-(1 + sqrt 2)^k. QED.

CHECKS.
  dimension of the commutant of rho, solved over Q:   {dim}   (the proof says 4)""")
    assert dim == 4
    found = set()
    for c in itertools.product(range(-3, 4), repeat=4):
        M = [[0] * 4 for _ in range(4)]
        P = [[int(i == j) for j in range(4)] for i in range(4)]
        for k in range(4):
            M = [[M[i][j] + c[k] * P[i][j] for j in range(4)] for i in range(4)]
            P = matmul(P, rho)
        if matmul(M, ref) != matmul(ref, M) or abs(det(M)) != 1:
            continue
        # M = a + b(rho + rho^-1) acts as a + b.sqrt 2 on the physical plane
        a, b = M[0][0], M[1][0]
        found.add((a, b))
    lam = sorted({round(abs(a + b * math.sqrt(2)), 9) for a, b in found})
    print(f"  octagonal integer inflations with |coefficients| <= 3 and det +-1:  {len(found)}")
    print(f"  their physical scale factors |a + b sqrt 2|:  {lam}")
    silver = {round((1 + math.sqrt(2)) ** k, 9) for k in range(-4, 5)}
    assert set(lam) <= silver
    print(f"""  all are powers of 1 + sqrt 2 = {1 + math.sqrt(2):.9f}:  True
  phi = {(1 + math.sqrt(5)) / 2:.9f} among them:  False     2 + sqrt 3 = {2 + math.sqrt(3):.9f}:  False

So the substrate's own lattice makes one family of inflations: the silver ratio and its powers.
The golden ratio (5- and 10-fold, Z[zeta_5]) and 2 + sqrt 3 (12-fold, Z[zeta_12]) need a different
lattice. Where nature uses phi, the substrate lattice is not what supplies it.""")


# --------------------------------------------------------------------------- #
# sec 4 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 4  SCOPE, AND THE NATURAL RECORD")
    print("""
  1. KNOWN MATHEMATICS. The Ammann-Beenker tiling, its cut-and-project construction from Z^4 and its
     silver inflation (Beenker 1982; Ammann, Grunbaum & Shephard 1992); Z[zeta_8] and its units.

  2. THIS THREAD'S. The identification: the eight twists ARE the signed frame of Z[zeta_8], the
     closure walk's lattice. So the silver ratio is not chosen -- it is the lattice's own inflation,
     and a twist-level ZFA DNA (t -> t- t t+) carries it, closing at every depth.

  3. NATURE. Octagonal quasicrystals are observed: V-Ni-Si and Cr-Ni-Si (Wang, Chen & Kuo 1987).
     They are rarer than the icosahedral and decagonal (phi) kinds (Steurer 2004), so the value the
     substrate lattice makes natively is a value nature uses, but not its most common one.

  4. CAVEAT. The octagon puts the gauge axis +- beside the spatial axes; the Pauli algebra keeps it
     apart. A physical reading of the octagonal projection would have to justify that.""")


def main() -> None:
    print(__doc__)
    sec1()
    sec2("--svg" in sys.argv)
    sec3()
    scope()


if __name__ == "__main__":
    main()
