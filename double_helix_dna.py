#!/usr/bin/env python3
"""
double_helix_dna.py -- the second axis is the complementary history: the ZFA double helix.

THE QUESTION (Jim, 2026-09-26): "a second axis? complimentary history? double helix? zfa dna!"

`mandelbrot_logical.py` flagged the second axis as the open edge: the full 2D set needs a
second conjugate pair, and the real-spine DNA supplies only one. This script tests the
proposal that the second axis is the COMPLEMENTARY history -- the Hermitian adjoint, the
other strand of a double helix -- and that the double helix itself is the ZFA DNA.

  * THE RUNG. `W . W-dagger` closes (ZFA): the adjoint reverses order and flips each twist,
    so the two strands are antiparallel and complementary. One rung is one closure.

  * THE IDENTIFICATION. On the Pauli fold the adjoint IS complex conjugation:
    `fold(W-dagger) = (-1)^|W| . fold(W)-dagger`, so for the even-length words that close it
    is exactly the adjoint. A history and its complement are therefore a complex PAIR
    `(A + iB, A - iB)`: `A` is the self-adjoint (rung) direction, `iB` the anti-self-adjoint
    (second) axis. The complement is what makes the plane two-dimensional.

  * THE DNA. A chain of rungs is the helix; its folds are the base pairs; its closure is the
    two strands pairing. Then `z |-> z^2 + c` (squaring reproduces both strands, `+c` splices
    a rung) is a two-axis map, and its bounded-orbit set is the Mandelbrot set of the helix.

  sec 0  the complement is conjugation (and the (-1)^|W| it carries)
  sec 1  the rung, and the double helix as the ZFA DNA
  sec 2  the two axes: self-adjoint (rung) + anti-self-adjoint (complement)
  sec 3  generate the 2D set -- EXACT on the Gaussian integers, then rendered
  sec 4  scope

Run:  python3 double_helix_dna.py
"""
from __future__ import annotations

from twist_core import adjoint_history, closure_with_adjoint, pauli_fold


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def matrix_adjoint(M):
    """(A^dagger)_{ij} = conj(A_{ji}) for a 2x2 matrix stored (a, b, c, d)."""
    a, b, c, d = M
    return (a.conjugate(), c.conjugate(), b.conjugate(), d.conjugate())


def same(P, Q, tol: float = 1e-9) -> bool:
    return all(abs(x - y) < tol for x, y in zip(P, Q))


def fmt(M) -> str:
    def one(x):
        return f"{x.real:g}" if abs(x.imag) < 1e-9 else f"{x.real:g}{x.imag:+g}i"
    return "[" + " ".join(one(x) for x in M) + "]"


# --------------------------------------------------------------------------- #
# sec 0 -- the complement is conjugation
# --------------------------------------------------------------------------- #
def complement_is_conjugation() -> None:
    rule("sec 0  THE COMPLEMENTARY HISTORY IS COMPLEX CONJUGATION")
    print("""
The adjoint `adjoint_history` reverses a word and flips every twist (`^<->v`, `<->`>`, ...).
On the Pauli fold that is the matrix adjoint, up to one global sign:
""")
    print(f"  {'W':<10}{'|W|':>4}   {'fold(W-dagger) == (-1)^|W| . fold(W)-dagger'}")
    print("  " + "-" * 60)
    ok = True
    for W in ("^", ">", "<^", "^<", "^v<>", "^^^^<<<<", "^<v>", "/\\+-"):
        n = len(W)
        lhs = pauli_fold(adjoint_history(W))
        rhs = tuple((-1) ** n * x for x in matrix_adjoint(pauli_fold(W)))
        good = same(lhs, rhs)
        ok &= good
        print(f"  {W:<10}{n:>4}   {good}")
    assert ok
    print("""
  So the complementary strand is the conjugate of the strand -- a genuine conjugation, with a
  global sign `(-1)^|W|` that is invisible to closure (ZFA is closure up to an overall phase,
  and every closing word here has even length, where the sign is +1). Note: `twist_core`'s
  `adjoint_history` docstring says "Hermitian adjoint"; the matrix adjoint of an ODD-length word
  differs by that sign. It is harmless where it is used, and this script computes the true
  adjoint explicitly.""")


# --------------------------------------------------------------------------- #
# sec 1 -- the rung and the helix
# --------------------------------------------------------------------------- #
def rung_and_helix() -> None:
    rule("sec 1  ONE RUNG IS ONE CLOSURE -- THE DOUBLE HELIX IS THE ZFA DNA")
    print("""
Strand 1 is a history `W`; strand 2 is its complement `W-dagger` read antiparallel. The rung
is the pair, and the pair closes:
""")
    print(f"  {'W':<10}{'W . W-dagger':<24}{'action':<16}{'ZFA'}")
    print("  " + "-" * 58)
    for W in ("<^", "^v<>", "^^^^<<<<", "^<v>", "/\\+-"):
        r = closure_with_adjoint(W)
        print(f"  {W:<10}{r['cycle']:<24}{str(r['cycle_action']):<16}{r['cycle_is_zfa']}")
        assert r["cycle_action"] == (0, 0, 0, 0) and r["cycle_is_zfa"]
    print("""
  Every rung is count-balanced AND Pauli-closed: the two strands annihilate to a scalar. The
  helix is a chain of rungs, the folds along it are the base pairs, and each base pair is one
  closure event carrying `log 2` (`active_inference_vfe_demo.py`). The DNA is the helix; the
  closure is the zipping.

  Antiparallel is literal: the adjoint REVERSES order. `W = <^` pairs with `v>` -- read the
  second strand right-to-left and it is `>v`, the complement of `<^` in order.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the two axes
# --------------------------------------------------------------------------- #
def two_axes() -> None:
    rule("sec 2  THE TWO AXES: SELF-ADJOINT (RUNG) + ANTI-SELF-ADJOINT (COMPLEMENT)")
    print("""
Decompose the fold into its self-adjoint and anti-self-adjoint parts,
`fold(W) = A + iB` with `A = A-dagger` and `B = B-dagger`. The adjoint conjugates it: `i -> -i`.
The single twists split cleanly, and products can turn anti-self-adjoint:
""")
    print(f"  {'W':<8}{'fold':<34}{'kind'}")
    print("  " + "-" * 58)
    for W in ("^", ">", "/", "+", "^v", "/\\", "^<", "^>"):
        P = pauli_fold(W)
        Ad = tuple((x + y) / 2 for x, y in zip(P, matrix_adjoint(P)))
        Bd = tuple((x - y) / (2j) for x, y in zip(P, matrix_adjoint(P)))
        kind = ("self-adjoint (A)" if max(abs(x) for x in Bd) < 1e-9
                else "anti-self-adjoint (iB)" if max(abs(x) for x in Ad) < 1e-9
                else "mixed")
        print(f"  {W:<8}{fmt(P):<34}{kind}")
    print("""
  So a history and its complement are `(A + iB, A - iB)` -- a complex pair. `A`, the
  self-adjoint part, is the rung (what the two strands agree on); the `iB` direction, the
  anti-self-adjoint part, is the SECOND AXIS (what they disagree on), with `B` the real
  coefficient. One conjugate pair of twists gives one real
  direction; the complement supplies the other. That is the second axis: not another space
  direction, but the strand difference.""")


# --------------------------------------------------------------------------- #
# sec 3 -- generate the 2D set
# --------------------------------------------------------------------------- #
def gaussian_mandelbrot() -> None:
    rule("sec 3  THE 2D SET -- EXACT ON THE GAUSSIAN INTEGERS")
    print("""
With two axes the state is a Gaussian integer `z = x + iy` (x = rung, y = complement) and the
map is the two-strand iteration

    z |-> z^2 + c        squaring reproduces both strands;  +c splices a rung.

Escape lemma: if `|z| > 2` and `|z| >= |c|` then `|z^2 + c| >= |z|^2 - |c| > |z|`, so the orbit
diverges. Since `z_1 = c`, every bounded `c` has `|c| <= 2` -- for a Gaussian integer only 13
candidates. Decide all of them in exact integer arithmetic:
""")
    candidates = [(a, b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)
                  if a * a + b * b <= 4]
    inside = [c for c in candidates if bounded(*c)]
    print(f"  candidates |c| <= 2 : {len(candidates)}")
    print(f"  in M : {len(inside)}   {inside}")
    for c in inside:
        print(f"    c = {c[0]:+d}{c[1]:+d}i   cycle {cycle_of(*c)}")
    print(f"""
  The exact, finite, purely logical Mandelbrot set of the double helix is

      M(Z[i]) = {{ 0, -1, -2, +i, -i }},

  five points. It contains the conjugate pair `+i, -i` -- the two strands again -- and the real
  points `0, -1, -2`: the critical point, its 2-cycle, and the parabolic fixed-point parameter.
  Every one is a closure reached in finite time. No float, no truncation, no continuum.""")


def bounded(cx: int, cy: int, steps: int = 400) -> bool:
    x, y = 0, 0
    for _ in range(steps):
        x, y = x * x - y * y + cx, 2 * x * y + cy
        if x * x + y * y > 4:
            return False
    return True


def cycle_of(cx: int, cy: int, steps: int = 400):
    x, y, seen, path = 0, 0, {}, []
    for _ in range(steps):
        if (x, y) in seen:
            return path[seen[(x, y)]:]
        seen[(x, y)] = len(path)
        path.append((x, y))
        x, y = x * x - y * y + cx, 2 * x * y + cy
    return None


# --------------------------------------------------------------------------- #
# sec 3b -- the render
# --------------------------------------------------------------------------- #
def render(width: int = 72, height: int = 24, R: int = 48) -> None:
    rule("sec 3b  THE SAME SET, RENDERED (the continuum carrying the five points)")
    print(f"""
The Gaussian-integer result is the object; the familiar picture is its rendering at capacity
R = {R}, with the same `z |-> z^2 + c` on the two axes:
""")
    x0, x1, y0, y1 = -2.15, 0.65, -1.15, 1.15
    for row in range(height):
        im = y1 - (y1 - y0) * row / (height - 1)
        line = []
        for col in range(width):
            re = x0 + (x1 - x0) * col / (width - 1)
            z, n = 0j, R
            for k in range(R):
                z = z * z + complex(re, im)
                if abs(z) > 2:
                    n = k + 1
                    break
            line.append("#" if n >= R else ("." if n < 3 else " "))
        print("  " + "".join(line))
    print("""
  The five exact points sit inside the `#` region: `0` and `-1` in the main cardioid/-1 bulb,
  `-2` at the tip of the antenna, `+i`/`-i` in the period-2 bulb. The identification does not
  make the continuum real -- it says the texture is generated by the two complementary
  strands, and the exact object is the five closures.""")


# --------------------------------------------------------------------------- #
# sec 4 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 4  SCOPE")
    print("""
  1. THE IDENTIFICATION IS STRUCTURAL, AND CHECKED. The complement is conjugation on the fold
     (sec 0), a history and its complement form a complex pair (sec 2). What is NOT claimed is
     that the complementary history is the ONLY possible second axis -- the algebra has other
     conjugate pairs (x, y, z); a route, not the route (CLAUDE.md sec 3a rule 5).

  2. THE EXACT RESULT IS FINITE. `M(Z[i]) = {0, -1, -2, +i, -i}` is proved by the escape lemma
     plus a 13-case enumeration, in exact integer arithmetic. It is the logical object; the
     render is a rendering, consistent with Continuum_Choice_Fallacy.md.

  3. THE RUNG IS ALREADY THE REPO'S CLOSURE. `W . W-dagger` is the "W . W-dagger (the ray
     pair)" of `mandelbrot_loop_dna.py` sec 4; this script only names the strand that was
     missing and shows it is the second axis.""")


def main() -> None:
    print(__doc__)
    complement_is_conjugation()
    rung_and_helix()
    two_axes()
    gaussian_mandelbrot()
    render()
    scope()


if __name__ == "__main__":
    main()
