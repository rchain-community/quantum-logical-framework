#!/usr/bin/env python3
"""
penrose_zfa.py -- the Penrose tiling: where the golden ratio enters the substrate.

THE QUESTION (Jim, 2026-09-28): "have we considered penrose tiling?"

silver_zfa_dna.py showed the substrate's own LATTICE (Z^4 = Z[zeta_8], the eight twists) makes the silver
ratio and never phi. The Penrose tiling is phi's tiling, with 5-fold symmetry. So where can it come from?

  sec 1  NOT FROM THE LATTICE. The twist lattice's full symmetry group -- the 384 signed permutations of
         four axes -- has no element of order 5, so no 5-fold symmetry. And the standard (de Bruijn) Penrose
         construction needs ten signed directions, while the Lean theorem alphabetSize_trichotomy allows
         alphabets of only 2, 4 or 8 twists.
  sec 2  FROM THE SPIN. The weak-isospin quaternions tau = i.sigma (Q_8, BraKetRhoQuCalc) sit inside the binary
         icosahedral group 2I (order 120), the closure-symmetry group of Geometry_Of_Space.md (McKay -> E_8).
         Extending Q_8 to 2I forces coordinates in Z[phi]: phi is the trace of a 5-fold spin rotation.
  sec 3  THE TILING, EXACTLY. The Penrose rhomb tiling by Robinson-triangle substitution, computed in
         Z[zeta_5] (exact; no float). Its tile counts are Fibonacci numbers, its inflation is phi^2, and its
         substitution matrix is the square of the golden ZFA DNA's matrix (golden_zfa_dna.py): the golden
         block genome is the one-dimensional shadow of the Penrose inflation.
  sec 4  scope: two sources of irrationals -- the lattice gives silver, the spin gives golden.

Run:  python3 penrose_zfa.py
      python3 penrose_zfa.py --svg     (writes diagrams/zfa_penrose.svg)
"""
from __future__ import annotations

import itertools
import math
import sys
from fractions import Fraction


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# sec 1 -- not from the lattice
# --------------------------------------------------------------------------- #
def signed_perms():
    for perm in itertools.permutations(range(4)):
        for signs in itertools.product((1, -1), repeat=4):
            yield tuple((perm[i], signs[i]) for i in range(4))


def order(g) -> int:
    """Order of a signed permutation g: axis i -> sign * axis perm[i]."""
    def compose(a, b):                       # apply b then a
        return tuple((a[b[i][0]][0], a[b[i][0]][1] * b[i][1]) for i in range(4))
    ident = tuple((i, 1) for i in range(4))
    h, k = g, 1
    while h != ident:
        h, k = compose(g, h), k + 1
    return k


def sec1() -> None:
    rule("sec 1  NOT FROM THE LATTICE: THE TWIST FRAME HAS NO 5-FOLD SYMMETRY")
    orders = {}
    for g in signed_perms():
        orders[order(g)] = orders.get(order(g), 0) + 1
    assert sum(orders.values()) == 384 and 5 not in orders and 10 not in orders
    print(f"""
The symmetries of the eight twists are the signed permutations of the four axes: 4! x 2^4 = 384 of them
(the hyperoctahedral group). Their orders, counted:
      {dict(sorted(orders.items()))}
No element of order 5 (or 10) -- as it must be, since 5 does not divide 384. So nothing in the twist
frame can rotate by 72 degrees, and a Penrose tiling cannot be the frame's own projection, the way the
octagonal tiling is (silver_zfa_dna.py).

The standard construction confirms it from the other side. De Bruijn's Penrose tiling is a projection
of Z^5: ten signed directions. A ten-twist alphabet is excluded by the Lean theorem
alphabetSize_trichotomy (lean/QLF_AlphabetNecessity.lean): a closed axis frame has 2, 4 or 8 twists.""")


# --------------------------------------------------------------------------- #
# exact Q(sqrt 5)
# --------------------------------------------------------------------------- #
class Q5:
    """p + q.sqrt 5."""
    __slots__ = ("p", "q")

    def __init__(self, p=0, q=0):
        self.p, self.q = Fraction(p), Fraction(q)

    def __add__(self, o): return Q5(self.p + o.p, self.q + o.q)
    def __sub__(self, o): return Q5(self.p - o.p, self.q - o.q)
    def __neg__(self): return Q5(-self.p, -self.q)
    def __mul__(self, o): return Q5(self.p * o.p + 5 * self.q * o.q, self.p * o.q + self.q * o.p)
    def __eq__(self, o): return self.p == o.p and self.q == o.q
    def __hash__(self): return hash((self.p, self.q))
    def __float__(self): return float(self.p) + float(self.q) * math.sqrt(5)


PHI = Q5(Fraction(1, 2), Fraction(1, 2))
PHI_INV = Q5(Fraction(-1, 2), Fraction(1, 2))      # phi - 1
HALF = Q5(Fraction(1, 2))
ZERO, ONE = Q5(0), Q5(1)


def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0 * b0 - a1 * b1 - a2 * b2 - a3 * b3,
            a0 * b1 + a1 * b0 + a2 * b3 - a3 * b2,
            a0 * b2 - a1 * b3 + a2 * b0 + a3 * b1,
            a0 * b3 + a1 * b2 - a2 * b1 + a3 * b0)


def even_perms4():
    for p in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
        if inv % 2 == 0:
            yield p


def binary_icosahedral():
    """The 120 unit icosians: 24 Hurwitz units and 96 even permutations of (0, +-1, +-phi^-1, +-phi)/2."""
    els = set()
    for i in range(4):
        for s in (1, -1):
            v = [ZERO] * 4
            v[i] = Q5(s)
            els.add(tuple(v))
    for signs in itertools.product((1, -1), repeat=4):
        els.add(tuple(Q5(Fraction(s, 2)) for s in signs))
    base = [ZERO, HALF, PHI_INV * HALF, PHI * HALF]
    for p in even_perms4():
        for s1, s2, s3 in itertools.product((1, -1), repeat=3):
            v = [base[0], base[1] * Q5(s1), base[2] * Q5(s2), base[3] * Q5(s3)]
            els.add(tuple(v[p[i]] for i in range(4)))
    return els


def sec2() -> None:
    rule("sec 2  FROM THE SPIN: Q_8 INSIDE 2I, AND PHI AS A ROTATION'S TRACE")
    G = binary_icosahedral()
    closed = all(qmul(a, b) in G for a in G for b in G)
    q8 = {tuple(Q5(s) if j == i else ZERO for j in range(4)) for i in range(4) for s in (1, -1)}
    traces = sorted({float(g[0] * Q5(2)) for g in G})
    def qorder(g):
        h, k = g, 1
        one = (ONE, ZERO, ZERO, ZERO)
        while h != one:
            h, k = qmul(g, h), k + 1
        return k
    ords = {}
    for g in G:
        ords[qorder(g)] = ords.get(qorder(g), 0) + 1
    assert len(G) == 120 and closed and q8 <= G and 5 in ords
    print(f"""
The spin side of the substrate is SU(2): spin IS the twists (QLF_Spin), and the weak-isospin generators
are the quaternions tau = i.sigma, with tau^2 = -1 (BraKetRhoQuCalc) -- the group Q_8 = {{+-1, +-i, +-j, +-k}}.
Build the binary icosahedral group 2I as unit quaternions, exactly over Q(sqrt 5):

  elements                                  {len(G)}
  closed under multiplication               {closed}
  contains Q_8 (the tau = i.sigma group)    {q8 <= G}
  element orders (order: how many)          {dict(sorted(ords.items()))}
  traces 2.Re(g) that occur                 {', '.join(f'{t:+.6f}' for t in traces)}

The order-5 and order-10 elements are the 72- and 36-degree spin rotations the twist frame lacked, and
their traces are +-phi and +-(phi - 1): extending the spin group from Q_8 to 2I forces coordinates in
Z[phi]. This is the group Geometry_Of_Space.md names as the closure symmetry (mckay_2I_E8_anchor); its
120 elements, over Z[phi], span the icosian ring, a model of the E_8 lattice (Conway & Sloane). So phi
enters the substrate through rotations of the spinor, not through the twist lattice.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the Penrose tiling, exactly in Z[zeta_5]
# --------------------------------------------------------------------------- #
def zmul_zeta(a):
    """Multiply a = a0 + a1 z + a2 z^2 + a3 z^3 (z = zeta_5) by z, using z^4 = -1 - z - z^2 - z^3."""
    a0, a1, a2, a3 = a
    return (-a3, a0 - a3, a1 - a3, a2 - a3)


def zmul(a, b):
    out = (Fraction(0),) * 4
    p = a
    for k in range(4):
        out = tuple(o + b[k] * x for o, x in zip(out, p))
        p = zmul_zeta(p)
    return out


def zadd(a, b): return tuple(x + y for x, y in zip(a, b))
def zsub(a, b): return tuple(x - y for x, y in zip(a, b))


Z_ONE = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
Z_PHI_INV = (Fraction(-1), Fraction(0), Fraction(-1), Fraction(-1))    # zeta + zeta^4 = 2 cos 72 = phi - 1
Z_ZETA10 = (Fraction(0), Fraction(0), Fraction(0), Fraction(-1))       # zeta_10 = -zeta_5^3


def zpow(a, n):
    r = Z_ONE
    for _ in range(n):
        r = zmul(r, a)
    return r


def zfloat(a) -> tuple[float, float]:
    x = y = 0.0
    for k, c in enumerate(a):
        x += float(c) * math.cos(2 * math.pi * k / 5)
        y += float(c) * math.sin(2 * math.pi * k / 5)
    return x, y


def sun():
    """The 10 Robinson half-rhombs around the origin (colour 0 = thin, 1 = thick)."""
    zero = (Fraction(0),) * 4
    tris = []
    for i in range(10):
        B = zpow(Z_ZETA10, i)                  # the usual sun turned by 18 degrees, so every
        C = zpow(Z_ZETA10, i + 1)              # vertex is a 10th root of unity, inside Z[zeta_5]
        if i % 2 == 0:
            B, C = C, B
        tris.append((0, zero, B, C))
    return tris


def subdivide(tris):
    out = []
    for colour, A, B, C in tris:
        if colour == 0:
            P = zadd(A, zmul(zsub(B, A), Z_PHI_INV))
            out += [(0, C, P, B), (1, P, C, A)]
        else:
            Q = zadd(B, zmul(zsub(A, B), Z_PHI_INV))
            R = zadd(B, zmul(zsub(C, B), Z_PHI_INV))
            out += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
    return out


def key(t):
    return (t[0], frozenset(t[1:]))


def sec3(make_svg: bool) -> None:
    rule("sec 3  THE PENROSE TILING, EXACTLY IN Z[zeta_5]")
    tris = sun()
    print("""
Start from a sun of ten half-rhombs (Robinson triangles) and subdivide: every thin half splits into one
thin and one thick, every thick into two thick and one thin, each new vertex a phi^-1 = zeta + zeta^4
point along an edge. Every coordinate stays in Z[zeta_5] (rational coefficients over 1, zeta, zeta^2,
zeta^3): the construction is exact, with no float.
""")
    print(f"  {'gen':>4}{'thin':>8}{'thick':>8}{'thick/thin':>14}{'5-fold':>9}")
    for g in range(0, 7):
        thin = sum(1 for t in tris if t[0] == 0)
        thick = len(tris) - thin
        rot = {key((c,) + tuple(zmul(v, zpow(Z_ZETA10, 2)) for v in (A, B, C))) for c, A, B, C in tris}
        five = rot == {key(t) for t in tris}
        assert five
        ratio = f"{thick / thin:.9f}" if thin else "-"
        fib = lambda m: round(((1 + 5 ** .5) / 2) ** m / 5 ** .5) if m > 0 else 0
        if g > 0:
            assert thin == 10 * fib(2 * g - 1) and thick == 10 * fib(2 * g)
        print(f"  {g:>4}{thin:>8}{thick:>8}{ratio:>14}{'yes':>9}")
        last = (thin, thick)
        if g < 6:
            tris = subdivide(tris)
    thin, thick = last
    print(f"""
  thick/thin -> phi = {(1 + math.sqrt(5)) / 2:.9f}; at generation g there are 10 F(2g-1) thin and 10 F(2g) thick
  half-rhombs (alternate Fibonacci numbers); every
  generation is invariant under rotation by 72 degrees, checked exactly.

  The substitution matrix on (thin, thick) half-rhombs is [[1, 1], [1, 2]] -- the square of the golden
  ZFA DNA's matrix [[1, 1], [1, 0]] (e -> ep, p -> e) up to relabelling, with eigenvalue phi^2. So the
  golden block genome of golden_zfa_dna.py is the one-dimensional shadow of the Penrose inflation.""")
    M = [[1, 1], [1, 0]]
    M2 = [[sum(M[i][k] * M[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert sorted(sum(M2, [])) == sorted([1, 1, 1, 2])
    if make_svg:
        svg(tris)


def svg(tris, path: str = "diagrams/zfa_penrose.svg") -> None:
    s, c = 205, 230
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 460" width="460" height="460">',
           '<rect width="460" height="460" fill="#ffffff"/>']
    fill = {0: "#f59e0b", 1: "#4f46e5"}
    for colour, A, B, C in tris:
        pts = " ".join(f"{c + s * x:.2f},{c - s * y:.2f}" for x, y in map(zfloat, (A, B, C)))
        out.append(f'<polygon points="{pts}" fill="{fill[colour]}" stroke="none"/>')
    for colour, A, B, C in tris:                        # draw the rhomb edges, not the half-rhomb bases
        (ax, ay), (bx, by), (cx, cy) = map(zfloat, (A, B, C))
        for (x1, y1), (x2, y2) in (((ax, ay), (bx, by)), ((cx, cy), (ax, ay))):
            out.append(f'<line x1="{c + s * x1:.2f}" y1="{c - s * y1:.2f}" x2="{c + s * x2:.2f}" '
                       f'y2="{c - s * y2:.2f}" stroke="#ffffff" stroke-width="0.6"/>')
    out.append('</svg>')
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"\n  wrote {path} ({len(tris)} half-rhombs)")


def scope() -> None:
    rule("sec 4  SCOPE: TWO SOURCES OF IRRATIONALS")
    print("""
  1. THE LATTICE GIVES SILVER. The twist frame Z^4 = Z[zeta_8] has no 5-fold symmetry (sec 1); its
     natural projection is octagonal, inflation 1 + sqrt 2 (silver_zfa_dna.py).
  2. THE SPIN GIVES GOLDEN. The spin group's extension from Q_8 to 2I carries 5-fold rotations with
     trace phi (sec 2); the Penrose tiling is phi's tiling, exactly in Z[zeta_5] (sec 3).
  3. NATURE. The phi quasicrystals are the icosahedral and decagonal ones -- built by three-dimensional
     rotations, the spin side -- and they are the most common (Steurer 2004). Silver (octagonal), the
     lattice's own, is rarer. That fits the two-source reading; it is a reading, not a derivation.
  4. KNOWN MATHEMATICS. The Penrose tiling and its Robinson-triangle substitution (Penrose 1974; de Bruijn
     1981); 2I and the icosians (Conway & Sloane, Sphere Packings, Lattices and Groups). None is new here;
     what is this thread's is where each irrational enters the substrate.""")


def main() -> None:
    print(__doc__)
    sec1()
    sec2()
    sec3("--svg" in sys.argv)
    scope()


if __name__ == "__main__":
    main()
