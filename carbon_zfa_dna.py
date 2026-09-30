#!/usr/bin/env python3
"""
carbon_zfa_dna.py -- the ZFA DNA of carbon: graphene is the substrate's three spatial axes.

THE QUESTION (Jim, 2026-09-30): "graphene, start the superconductivity work. zfa dna for
superconducting carbon structure."

  sec 1  carbon's lattices from the twist alphabet. A walk whose twists alternate in sign, + - + - ...,
         never leaves a two-layer slab of Z^k. Projected along (1,...,1), the slab is carbyne (k = 2),
         graphene (k = 3) and diamond (k = 4). A closed walk on the lattice IS a ZFA word.
  sec 2  the carbon DNA: t -> t u' t w' t (u' = the negative twist of axis u). It inflates graphene by 4,
         keeps every generation on the sheet and ZFA, and carries one free order bit per twist:
         h = 1/4 bit per twist, the graphene counterpart of the primordial DNA's 1/3.
  sec 3  the magic-angle family: n graphene layers twisted +theta, -theta, ... are flat-banded at
         theta_n = theta_2 * 2cos(pi/(n+1)) (Khalaf et al. 2019): 1, sqrt 2, phi, sqrt 3 -- the ratios of
         ZFA_DNA.md sec 11-13. Compared with the superconducting devices of Park et al. (2022).
  sec 4  scope.

Run:  python3 carbon_zfa_dna.py
"""
from __future__ import annotations

import itertools
import math
from collections import Counter

from twist_core import is_zfa, pauli_fold

# The four axes of the alphabet, each as (positive twist, negative twist). The first three are the
# Pauli spatial axes x, y, z; the fourth is the gauge axis.
AXES = [('>', '<'), ('^', 'v'), ('/', '\\'), ('+', '-')]
SIGN = {p: +1 for p, _ in AXES} | {n: -1 for _, n in AXES}
AXIS = {c: a for a, pair in enumerate(AXES) for c in pair}


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def alternating_words(k: int, length: int):
    """Every word over the first k axes whose signs run + - + - ... (a walk starting on sublattice A)."""
    pos = [AXES[a][0] for a in range(k)]
    neg = [AXES[a][1] for a in range(k)]
    for choice in itertools.product(range(k), repeat=length):
        yield ''.join(pos[a] if i % 2 == 0 else neg[a] for i, a in enumerate(choice))


def heights(word: str) -> list[int]:
    """Running sum of twist signs = the coordinate along (1,...,1); the slab is {0, 1}."""
    h, out = 0, [0]
    for c in word:
        h += SIGN[c]
        out.append(h)
    return out


def lattice_point(word: str, k: int) -> tuple[int, ...]:
    v = [0] * k
    for c in word:
        v[AXIS[c]] += SIGN[c]
    return tuple(v)


def returns(k: int, n: int) -> int:
    """Closed alternating walks of length 2n on k axes: sum over compositions of (multinomial)^2."""
    total = 0
    for comp in itertools.product(range(n + 1), repeat=k):
        if sum(comp) == n:
            m = math.factorial(n)
            for c in comp:
                m //= math.factorial(c)
            total += m * m
    return total


# --------------------------------------------------------------------------- #
# sec 1 -- carbon's lattices from the alphabet
# --------------------------------------------------------------------------- #
def sec1() -> None:
    rule("sec 1  CARBON'S LATTICES FROM THE TWIST ALPHABET")
    print("""
Take k axes and let a walk's twists alternate in sign: +, -, +, - ... . The running sign sum (the
coordinate along (1,...,1)) is then always 0 or 1: the walk lives on a two-layer slab of Z^k. Call the
height-0 points A and the height-1 points B. Every A has k neighbours (+e_a) and every B has k (-e_a),
and two slab points never differ by a multiple of (1,...,1), so projecting along it is one-to-one.
The projected bond vectors e_a - (1/k)(1,...,1) meet at cos = -1/(k-1):
""")
    names = {2: 'carbyne (sp)', 3: 'graphene (sp2)', 4: 'diamond (sp3)'}
    print(f"  {'k':>3}  {'lattice':<16}{'bonds':>6}{'bond angle':>13}{'smallest ring':>15}")
    for k in (2, 3, 4):
        ang = math.degrees(math.acos(-1 / (k - 1)))
        ring = None
        for L in range(2, 11, 2):   # smallest closed walk with no immediate step-back
            for w in alternating_words(k, L):
                if lattice_point(w, k) == (0,) * k and all(AXIS[w[i]] != AXIS[w[(i + 1) % L]] for i in range(L)):
                    ring = L
                    break
            if ring:
                break
        print(f"  {k:>3}  {names[k]:<16}{k:>6}{ang:>12.2f}°{(ring or '-'):>15}")
    print("""
180°, 120° and 109.47° are carbon's three hybridisations. Carbyne is a chain with no rings; graphene
and diamond both have six-membered rings -- the hexagon and the chair.

A closed walk on the lattice is a word whose axis counts balance, and count balance implies Pauli
closure (count_balanced_pauli_closed, QLF_TwistAlphabet.lean). So the closed walks on graphene are
exactly the alternating ZFA words over the three spatial axes. Brute force, every alternating word:""")
    oeis = {3: [3, 15, 93, 639], 4: [4, 28, 256, 2716]}     # A002898 (honeycomb), A002899 (diamond)
    for k in (3, 4):
        row = []
        for n in range(1, 5):
            L = 2 * n
            closed = zfa = 0
            for w in alternating_words(k, L):
                assert set(heights(w)) <= {0, 1}
                c = lattice_point(w, k) == (0,) * k
                z = is_zfa(w, min_length=2)
                assert c == z, w
                closed += c
            assert closed == returns(k, n) == oeis[k][n - 1]
            row.append(closed)
        print(f"  {names[k]:<16} closed walks of length 2,4,6,8 = {row}  (OEIS {'A002898' if k == 3 else 'A002899'})"
              f"  every one ZFA, and no other alternating word is")
    hexagon = '>v/<^\\'
    a, b, c, d = pauli_fold(hexagon)
    print(f"""
The hexagon of graphene is the word {hexagon!r}: +x -y +z -x +y -z, six distinct atoms, ZFA
({is_zfa(hexagon)}), Pauli fold {a.real:+.0f}·I. The two sublattices are the two twist signs, so graphene's
sublattice pseudospin -- the label of its Dirac electrons -- is the sign alternation itself.

Graphene uses exactly the three Pauli axes. Diamond needs a fourth direction, and the alphabet's
fourth axis is the gauge axis +-: as in silver_zfa_dna.py, a physical reading of diamond would have to
justify treating the gauge axis as a spatial one. Graphene needs no such step.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the carbon DNA
# --------------------------------------------------------------------------- #
def blocks(k: int, t: str) -> list[str]:
    """Every image of twist t: t, then each other axis' opposite twist, each followed by t again."""
    a, s = AXIS[t], SIGN[t]
    others = [b for b in range(k) if b != a]
    out = []
    for order in itertools.permutations(others):
        w = t
        for b in order:
            w += AXES[b][1 if s > 0 else 0] + t
        out.append(w)
    return out


def sec2() -> None:
    rule("sec 2  THE CARBON DNA:  t -> t u' t w' t")
    print("""
Replace each twist by itself, interleaved with the opposite twists of the other axes:
  > -> > v > \\ >   or   > \\ > v >        < -> < ^ < / <   or   < / < ^ <     (and so on)
The image of +e_x is 3e_x - e_y - e_z = 4e_x - (1,1,1), so on the sheet it is +e_x scaled by 4. An image
starts and ends with its parent's sign, so the sign alternation survives, and the counts are linear,
so a closure maps to a closure. The order of the interleaved twists is free: one bit per twist.
""")
    k = 3
    hexagon = '>v/<^\\'
    gens = [[hexagon]]
    for g in range(1, 4):
        prev = gens[-1]
        nxt = set()
        for w in prev[:40]:                     # enough parents to see the branching
            for imgs in itertools.product(*(blocks(k, t) for t in w)) if g == 1 else [
                    [blocks(k, t)[(i * 7 + g) % 2] for i, t in enumerate(w)]]:
                nxt.add(''.join(imgs))
        gens.append(sorted(nxt))
    print(f"  {'gen':>4}{'length':>9}{'words checked':>15}{'all ZFA':>9}{'on sheet':>10}{'parent back':>13}")
    for g, ws in enumerate(gens):
        zfa = all(is_zfa(w) for w in ws)
        sheet = all(set(heights(w)) <= {0, 1} for w in ws)
        back = g == 0 or all(''.join(w[5 * i] for i in range(len(w) // 5)) in gens[g - 1] for w in ws)
        assert zfa and sheet and back
        print(f"  {g:>4}{len(ws[0]):>9}{len(ws):>15}{'yes':>9}{'yes':>10}{'yes' if g else '-':>13}")
    assert len(gens[1]) == 2 ** 6
    # corners of the gen-1 hexagon: the lattice points at block boundaries are 4x the parent's
    w1 = gens[1][0]
    for i in range(7):
        p1 = lattice_point(w1[:5 * i], k)
        p0 = lattice_point(hexagon[:i], k)
        s = sum(p0)
        assert p1 == tuple(4 * x - s for x in p0)          # 4 p - (sum p)(1,1,1): scale 4 on the sheet
    print(f"""
Generation 1 has all {len(gens[1])} = 2^6 images of the hexagon distinct; each is the side-4 hexagon (block
boundaries land on 4x the parent's corners, checked). Keep every 5th twist and the parent returns.
Generation g has length 6·5^g and 2^((5^g - 1)/4) distinct words per starting twist, so

   h = 1/4 bit per twist   (graphene)     vs   h = 1/3   for the primordial DNA (ZFA_DNA.md sec 1).

The general rule on k axes: block length 2k - 1, inflation k + 1, (k - 1)! orders per twist:""")
    print(f"\n  {'k':>3}  {'lattice':<16}{'block':>7}{'inflation':>11}{'orders':>8}{'h (bits/twist)':>16}")
    for kk, nm in ((2, 'carbyne'), (3, 'graphene'), (4, 'diamond')):
        bl = blocks(kk, '>')
        assert len({len(b) for b in bl}) == 1 and len(bl) == math.factorial(kk - 1)
        L = len(bl[0])
        v = lattice_point(bl[0], kk)
        infl = v[0] - v[1]                                   # (k+1) e_x - (1,...,1)
        h = math.log2(len(bl)) / (L - 1)
        print(f"  {kk:>3}  {nm:<16}{L:>7}{infl:>11}{len(bl):>8}{h:>16.4f}")
    print("""
Carbyne's DNA is forced (h = 0): the chain has one way to grow. Graphene's is the first with a free bit.
The free bit is order only -- it changes no count and no closure, exactly as the primordial DNA's
chirality bit does. So the coarse scale of the sheet is carried in the order of the twists.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the magic-angle family
# --------------------------------------------------------------------------- #
# Park, Cao, Xia, Sun, Watanabe, Taniguchi & Jarillo-Herrero, Nature Materials 21, 877 (2022),
# arXiv:2112.10760: device twist angles of Fig. 1, and Tc,50% where the text states it.
PARK = {2: (1.08, None), 3: (1.57, None), 4: (1.77, 2.76), 5: (1.95, 1.38)}


def sec3() -> None:
    rule("sec 3  THE MAGIC-ANGLE FAMILY OF SUPERCONDUCTING GRAPHENE")
    print("""
Stack n graphene sheets with alternating twists +theta, -theta, +theta ... -- the sign alternation again,
now between layers. In the chiral limit the stack decouples exactly into bilayers with couplings scaled
by the eigenvalues of the n-site chain, 2cos(j pi/(n+1)), so its magic angles are the bilayer's times
those numbers (Khalaf, Kruchkov, Tarnopolsky & Vishwanath, PRB 100, 085109 (2019)):
""")
    phi = (1 + 5 ** 0.5) / 2
    known = {1.0: '1', 2 ** 0.5: 'sqrt 2  (Z[zeta_8], the substrate lattice)', phi: 'phi     (Z[zeta_5])',
             1 / phi: '1/phi', 3 ** 0.5: 'sqrt 3  (Z[zeta_12])'}
    print(f"  {'n':>3}  {'2cos(pi/(n+1))':<55}{'predicted':>10}{'device':>9}{'dev/pred':>10}{'Tc,50%':>9}")
    t2 = PARK[2][0]
    for n in range(2, 6):
        r = 2 * math.cos(math.pi / (n + 1))
        name = next(v for x, v in known.items() if abs(x - r) < 1e-12)
        dev, tc = PARK[n]
        print(f"  {n:>3}  {r:.6f} = {name:<46}{t2 * r:>9.3f}°{dev:>8.2f}°{dev / (t2 * r):>10.3f}"
              f"{(f'{tc:.2f} K' if tc else '-'):>9}")
    extra = [f"{2 * math.cos(j * math.pi / 5):.4f}" for j in (1, 2)]
    print(f"""
The quadrilayer carries both golden values ({extra[0]} and {extra[1]}, phi and 1/phi); the pentalayer
carries sqrt 3 and 1. So the first four superconducting members of the family sit at 1, sqrt 2, phi,
sqrt 3 -- the natural ratios of ZFA_DNA.md sec 11-13, the silver lattice's sqrt 2 among them.

What this is, stated plainly. The ratios are Khalaf et al.'s continuum-model result, not a QLF
derivation; the chain eigenvalue 2cos(pi/(n+1)) is the spectrum of any n-link alternating chain. The
devices were fabricated to hit the calculated magic angles, whose real values sit slightly above the
chiral-limit ones (dev/pred 1.03, 1.01, 1.04), so the agreement is not an independent test of the
ratios. What QLF adds is the placement: the stacking is the same sign alternation as the sublattice,
and the values it produces are the family the ZFA DNA already makes.""")


def sec4() -> None:
    rule("sec 4  SCOPE")
    print("""
Proved here, by construction and brute force: an alternating-sign walk on k axes is confined to a
two-layer slab whose projection is carbyne, graphene or diamond; the closed walks are exactly the
alternating ZFA words (counts match OEIS A002898/A002899 through length 8); t -> t u' t w' t is a ZFA DNA
of graphene with inflation 4 and h = 1/4 bit per twist.

Not claimed: that this explains why carbon superconducts, or any Tc. The slab picture gives carbon's
geometry, not its pairing. Carbon's superconductors (twisted multilayers, intercalated graphite CaC6,
boron-doped diamond, the alkali fullerides) and the log 2 question are taken up in
Carbon_Superconductivity.md, with the tests pre-registered there before any is run.""")


if __name__ == "__main__":
    sec1()
    sec2()
    sec3()
    sec4()
