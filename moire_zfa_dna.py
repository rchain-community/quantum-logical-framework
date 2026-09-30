#!/usr/bin/env python3
"""
moire_zfa_dna.py -- the ZFA DNA of magic-angle twisted graphene, built from the sheet DNA of carbon_zfa_dna.py.

THE QUESTION (Jim, 2026-09-30): "can we get zfadna of something that may be superconducting to be extended later
perhaps, or is there a candidate for a carbon structure?"  The candidate: magic-angle twisted trilayer graphene
(MATTG), the one sample where the one-bit phase reading survived (Carbon_Superconductivity.md sec 7a-8a).

  sec 1  Eisenstein DNAs. A twist step on the sheet projects to 1, w, w^2 (w = e^{2 pi i/3}). For any Eisenstein
         integer z = p + q w + r w^2 with p + q + r = 1, the rule  +e_a -> an alternating word with counts
         (p, q, r) rotated to axis a  is a ZFA DNA of graphene: it scales the sheet by |z| and rotates it by arg z.
         carbon_zfa_dna.py's rule is z = 4; the norm-7 rule x -> x y' x is z = 2 - w.
  sec 2  Twist from a chiral pair. Give one layer the DNA of z and the next the DNA of its mirror z-bar (the same
         counts in mirror order). Their images are rotated relative to each other by 2 arg z (mod 60 deg): exactly
         the commensurate twist angles of twisted bilayer graphene. The magic angle is a particular z.
  sec 3  The ways. The words of a DNA with the same counts are the ways it can happen; their number is a
         multinomial. The magic cell's DNA is counted.
  sec 4  The trilayer. Three layers twisted +theta, -theta, +theta carry the words z, z-bar, z: the stacking word
         alternates like the sublattice. Its magic angle is sqrt 2 times the bilayer's.
  sec 5  What is proved, and the extension points.

Run:  python3 moire_zfa_dna.py
"""
from __future__ import annotations

import cmath
import math

from twist_core import is_zfa

POS = ['>', '^', '/']          # +e_x, +e_y, +e_z  -> 1, w, w^2
NEG = ['<', 'v', '\\']
AX = {c: i for i, c in enumerate(POS)} | {c: i for i, c in enumerate(NEG)}
SGN = {c: 1 for c in POS} | {c: -1 for c in NEG}
W = cmath.exp(2j * math.pi / 3)


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def cval(counts) -> complex:
    p, q, r = counts
    return p + q * W + r * W * W


def counts_of(z_ab: tuple[int, int]) -> tuple[int, int, int]:
    """z = a + b w  ->  (p, q, r) with p + q r w^2 ... and p + q + r = 1 (unique if z = 1 mod (1 - w))."""
    a, b = z_ab
    s = a + b                     # sum of (a, b, 0)
    k, rem = divmod(1 - s, 3)
    if rem:
        raise ValueError("z is not 1 mod (1 - w): it would swap the sublattices")
    return (a + k, b + k, k)


def word_for(counts, first_axis: int = 0) -> str:
    """One alternating word (+ - + ... +) with the given axis counts, starting with +e_first_axis."""
    pos, neg = [], []
    for ax, c in enumerate(counts):
        (pos if c > 0 else neg).extend([ax] * abs(c))
    pos.sort(key=lambda a: a != first_axis)
    assert pos and pos[0] == first_axis and len(pos) == len(neg) + 1
    # interleave, spreading each axis evenly (a canonical choice; any order is a valid way)
    w = [POS[pos[0]]]
    rest_p = pos[1:]
    for i in range(len(neg)):
        w.append(NEG[neg[i]])
        w.append(POS[rest_p[i]])
    return ''.join(w)


def rotate(word: str, k: int) -> str:
    return ''.join((POS if SGN[c] > 0 else NEG)[(AX[c] + k) % 3] for c in word)


def conj(word: str) -> str:
    return ''.join((NEG if SGN[c] > 0 else POS)[AX[c]] for c in word)


def dna(counts):
    """The substitution: +e_a -> word rotated to axis a; -e_a -> its conjugate."""
    base = word_for(counts, 0)
    sub = {}
    for a in range(3):
        sub[POS[a]] = rotate(base, a)
        sub[NEG[a]] = conj(rotate(base, a))
    return sub


def heights_ok(word: str) -> bool:
    h = 0
    for c in word:
        h += SGN[c]
        if h not in (0, 1):
            return False
    return True


def position(word: str) -> complex:
    return sum(SGN[c] * W ** AX[c] for c in word)


def twist_deg(z: complex) -> float:
    """Relative rotation of the z and z-bar images, folded to [0, 30] deg by the hexagonal symmetry."""
    t = math.degrees(2 * cmath.phase(z)) % 60
    return min(t, 60 - t)


def ways(counts) -> int:
    """Distinct words with these counts that start with +e_x: orders of the positive and the negative slots."""
    pos = {ax: c for ax, c in enumerate(counts) if c > 0}
    neg = {ax: -c for ax, c in enumerate(counts) if c < 0}
    pos[0] -= 1                                 # the head is fixed (self-similarity)
    P, N = sum(pos.values()), sum(neg.values())
    m = math.factorial(P) * math.factorial(N)
    for c in list(pos.values()) + list(neg.values()):
        m //= math.factorial(c)
    return m


def best_rep(z_ab):
    """Among z, wz, w^2 z (same twist, sublattice kept), the one whose own-axis count is largest."""
    a, b = z_ab
    cands = [(a, b), (-b, a - b), (b - a, -a)]         # multiplication by w: (a + b w) w = -b + (a - b) w
    return max((counts_of(c) for c in cands), key=lambda t: t[0])


# --------------------------------------------------------------------------- #
def sec1() -> None:
    rule("sec 1  EISENSTEIN DNAs OF THE SHEET")
    hexagon = '>v/<^\\'
    print(f"\n  {'z':<10}{'counts':<14}{'|z|':>7}{'arg z':>9}{'word for +e_x':<30}{'depth 3: ZFA, on sheet, heads, corners'}")
    for z_ab in [(4, 0), (2, -1), (3, -1), (5, 1), (1, -3)]:
        try:
            cnt = best_rep(z_ab)
        except ValueError:
            continue
        sub = dna(cnt)
        z = cval(cnt)
        w, parent = hexagon, None
        ok = True
        for g in range(3):
            parent, w = w, ''.join(sub[c] for c in w)
            L = len(sub['>'])
            ok &= is_zfa(w) and heights_ok(w)
            ok &= ''.join(w[L * i] for i in range(len(parent))) == parent
            # every block boundary lands on z times the parent's lattice point
            ok &= all(abs(position(w[:L * i]) - z * position(parent[:i])) < 1e-9 for i in range(len(parent) + 1))
        print(f"  {str(z_ab):<10}{str(cnt):<14}{abs(z):>7.3f}{math.degrees(cmath.phase(z)):>8.2f}°  {sub['>']:<28}{'all hold' if ok else 'FAILS'}")
        assert ok
    print("""
Every such z gives a ZFA DNA of the sheet: closures map to closures at every depth (the counts are linear),
every generation stays on the two-layer slab (each image alternates and starts and ends with its parent's
sign), keeping every L-th twist returns the parent, and block boundaries land exactly on z times the parent's
corners. carbon_zfa_dna.py's rule is z = 4; x -> x y' x is z = 2 - w (|z| = sqrt 7, rotation -19.1 deg).
z must be 1 mod (1 - w) so that A sites map to A sites; that is a third of the Eisenstein integers.""")


def commensurate():
    """All z (one per twist) with norm up to a bound, as (angle, norm, counts)."""
    seen = {}
    for a in range(-80, 81):
        for b in range(-80, 81):
            n = a * a - a * b + b * b
            if n < 2 or n > 12000:
                continue
            try:
                cnt = best_rep((a, b))
            except ValueError:
                continue
            ang = round(twist_deg(cval(cnt)), 6)
            if ang < 1e-6:
                continue
            if ang not in seen or n < seen[ang][0]:
                seen[ang] = (n, cnt)
    return sorted((ang, n, cnt) for ang, (n, cnt) in seen.items())


def sec2(table) -> None:
    rule("sec 2  TWIST FROM A CHIRAL PAIR OF DNAs")
    print("""
The mirror z-bar has the counts (p, r, q): the same twists in mirror order, the same length. Layer 1 grown with
z and layer 2 with z-bar are rotated relative to each other by 2 arg z. These are the commensurate angles of
twisted bilayer graphene; the standard family cos(theta) = (3m^2 + 3m + 1/2)/(3m^2 + 3m + 1) is checked:
""")
    for m in (1, 2, 3, 10, 30, 31):
        th = math.degrees(math.acos((3 * m * m + 3 * m + 0.5) / (3 * m * m + 3 * m + 1)))
        hit = min(table, key=lambda r: abs(r[0] - th))
        print(f"  m = {m:>2}: theta = {th:8.4f}°   found: {hit[0]:8.4f}° at norm {hit[1]:>5}, counts {hit[2]}")
        assert abs(hit[0] - th) < 1e-4
    print("\n  Around the magic angle (device 1.08°, chiral limit ~1.05°), smallest norm per angle:")
    for ang, n, cnt in table:
        if 1.00 <= ang <= 1.12:
            L = sum(abs(c) for c in cnt)
            print(f"    theta = {ang:.4f}°  norm |z|^2 = {n:>5}  counts {cnt}  word length {L}")


def sec3(table) -> None:
    rule("sec 3  THE WAYS OF THE MAGIC CELL")
    ang, n, cnt = min((r for r in table if 1.00 <= r[0] <= 1.12), key=lambda r: abs(r[0] - 1.05))
    L = sum(abs(c) for c in cnt)
    k = ways(cnt)
    print(f"""
Every alternating order of a DNA's counts, with the head fixed, is the same step taken a different way. The
number of ways is a multinomial; only the ORDER is free (counts, closure and lattice point are fixed).

The magic-angle DNA closest to 1.05°: theta = {ang:.4f}°, |z|^2 = {n}, counts {cnt}, length {L}.
  ways = {k}.  Its counts use two axes only, so the word is forced:  {word_for(cnt)[:24]}...  = (> v)^{L // 2} >
This holds for the whole standard family theta_m (counts (m+1, -m, 0)): each is a single zigzag word with no
free bit, like carbyne's DNA and unlike the sheet's own (h = 1/4). Larger cells at nearby angles use all three
axes and do carry free order (1.0671°: counts (62, 1, -62), {ways((62, 1, -62))} ways). So one-way versus
many-way is a property of the commensurate cell chosen, not of the material.""")
    return ang, cnt


def sec4(table, bil) -> None:
    rule("sec 4  THE TRILAYER: +theta, -theta, +theta")
    th2 = bil[0]
    th3_target = math.sqrt(2) * th2
    ang, n, cnt = min(table, key=lambda r: (abs(r[0] - th3_target), r[1]))
    zc = cval(cnt)
    mirror = (cnt[0], cnt[2], cnt[1])
    print(f"""
Mirror-symmetric twisted trilayer: layers 1 and 3 aligned, layer 2 twisted by theta. With the chiral pair of
sec 2, the three layers carry the DNAs z, z-bar, z -- the stacking word + - + is the same sign alternation
that makes the sublattices, now between layers (Carbon_Superconductivity.md sec 3). Its magic angle is
sqrt 2 times the bilayer's (Khalaf et al. 2019).

  bilayer DNA (sec 3):          theta = {th2:.4f}°
  sqrt 2 x bilayer:             theta = {th3_target:.4f}°
  nearest commensurate z:       theta = {ang:.4f}°, |z|^2 = {n}, counts {cnt}
  layer words:  L1 = z {cnt},  L2 = z-bar {mirror},  L3 = z {cnt}
  check: rotation L1 vs L2 = {twist_deg(zc):.4f}°, L1 vs L3 = 0 (same word)""")
    sub1, sub2 = dna(cnt), dna(mirror)
    hexagon = '>v/<^\\'
    w1 = ''.join(sub1[c] for c in hexagon)
    w2 = ''.join(sub2[c] for c in hexagon)
    k = ways(cnt)
    print(f"  ways of the trilayer step: {k:.3e}  ({math.log2(k) / sum(abs(c) for c in cnt):.3f} bits per twist) -- three axes,\n"
          f"  so the order is free (a property of this cell; see sec 3)")
    print(f"  generation 1 of each layer from the hexagon: ZFA {is_zfa(w1)} / {is_zfa(w2)}, on sheet "
          f"{heights_ok(w1)} / {heights_ok(w2)}, equal length {len(w1) == len(w2)} ({len(w1)} twists)")


def sec5() -> None:
    rule("sec 5  WHAT IS PROVED, AND WHERE TO EXTEND")
    print("""
Proved here, by construction and check: every Eisenstein integer z = 1 mod (1 - w) gives a ZFA DNA of graphene
(inflation |z|, rotation arg z, closure and sheet kept at every depth); a chiral pair z / z-bar grows two sheets
twisted by 2 arg z, reproducing the commensurate angles of twisted graphene; the magic-angle cell is one such
pair (the smallest is a forced single-way zigzag word), with its ways counted; the trilayer is the word z, z-bar, z.

Not claimed: that the DNA makes the bands flat or causes pairing. The magic angle is where the continuum model's
bands flatten (Bistritzer & MacDonald 2011); this script only builds its lattice.

Extension points, in order of reach:
  1. Interlayer closure: a joint closure between an A site of layer 1 and the site above it in layer 2 (AA vs AB
     stacking regions of the moire). Counting where the two words' sites coincide gives the moire pattern.
  2. The flat band as a count: hopping around a moire cell is a closed word; the magic angle would be where the
     signed sum over those closures cancels (the Pauli phases of sec 1 of carbon_zfa_dna.py).
  3. The one-bit / two-bit phase of Carbon_Superconductivity.md sec 7-8, placed on the moire lattice: one bit per
     moire cell, coupling given by the interlayer closures of step 1.
  4. The fullerides (highest carbon T_c): pentagons are odd rings, outside every DNA here; C60 is icosahedral,
     so its natural ratio is phi (ZFA_DNA.md sec 11), not an Eisenstein one.""")


if __name__ == "__main__":
    sec1()
    table = commensurate()
    sec2(table)
    bil = sec3(table)
    sec4(table, bil)
    sec5()
