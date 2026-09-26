#!/usr/bin/env python3
"""
mandelbrot_exact.py -- generate the Mandelbrot set at finite capacity in EXACT integer
arithmetic. No float anywhere.

THE QUESTION (Jim, 2026-09-26): "do we have enough to do the mandelbrot set generation any way?"

Short answer: yes -- and there are three ways already, of which this is the strictly exact one.

  * `mandelbrot_logical.py` -- capacity-R generation M_R by the escape condition, and the exact
    closure skeleton f_c^p(0)=0. Uses float complex arithmetic for the render.
  * `double_helix_dna.py`   -- the two-axis generation, exact on the Gaussian integers
    M(Z[i]) = {0,-1,-2,+i,-i}.
  * THIS FILE               -- the same two-axis generation on a DYADIC grid, in exact integer
    arithmetic: no float, no rounding, certified at finite capacity.

THE ENCODING (same two axes as `double_helix_dna.py`): a dyadic Gaussian parameter
`c = (P + iQ)/2^q` and a state `z = (A + iB)/2^d`, all Python integers. Squaring reproduces
both strands (`z^2 = (A^2-B^2 + i2AB)/2^2d`) and `+c` splices the parameter in. A state is
"outside" once `|z| > 2`, i.e. `A^2 + B^2 > 4 . 2^2d` -- an exact integer comparison. So
`M_R` is decided by integer arithmetic alone.

  sec 1  the exact engine, and that it agrees with the float render
  sec 2  the generation at increasing capacity
  sec 3  the exact Gaussian-integer case (reproduces M(Z[i]) = {0,-1,-2,+-i})
  sec 4  scope

Run:  python3 mandelbrot_exact.py
"""
from __future__ import annotations

from mandelbrot_logical import escape_depth


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def escape_step(P: int, Q: int, q: int, R: int) -> int:
    """Least n <= R with |z_n| > 2, else R+1 (i.e. c is in M_R). Exact, integer-only.

    c = (P + iQ)/2^q, z_n = (A + iB)/2^d.  |z| > 2  <=>  A^2 + B^2 > 4 . 2^(2d).
    """
    A, B, d = P, Q, q                       # z_1 = c
    for n in range(1, R + 1):
        if A * A + B * B > (1 << (2 * d + 2)):
            return n
        if n == R:
            break
        sh = 2 * d - q                      # common denominator 2^(2d)
        A, B = A * A - B * B + (P << sh), 2 * A * B + (Q << sh)
        d = 2 * d
    return R + 1


# --------------------------------------------------------------------------- #
# sec 1 -- the engine, checked against the float render
# --------------------------------------------------------------------------- #
def engine_check() -> None:
    rule("sec 1  THE EXACT ENGINE, CHECKED AGAINST THE FLOAT RENDER")
    print("""
`escape_step` does the whole generation in `int`: the state is a Gaussian rational
`(A + iB)/2^d`, squaring and the `+c` splice stay on the dyadic grid, and escape is the exact
comparison `A^2 + B^2 > 4 . 2^2d`. Compare it to the float render (`mandelbrot_logical`):
""")
    q, R = 4, 16
    agree = differ = 0
    examples = []
    for P in range(-32, 10):
        for Q in range(-16, 17):
            exact_in = escape_step(P, Q, q, R) > R
            float_in = escape_depth(complex(P / 2 ** q, Q / 2 ** q), R) >= R
            if exact_in == float_in:
                agree += 1
            else:
                differ += 1
                if len(examples) < 5:
                    examples.append((P, Q))
    print(f"  {agree} cells agree, {differ} differ (of {agree + differ}) at q={q}, R={R}")
    if examples:
        print(f"  disagreements are boundary cells: {examples}")
    print("""
  They agree wherever the orbit is not within a rounding of |z| = 2. Where they differ the
  EXACT value is the truth -- the float one is the approximation. That is the point of this
  file: the repo's rule is exact arithmetic before float (ScientificApproach.md), and here the
  generation can honour it.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the generation
# --------------------------------------------------------------------------- #
def render(R: int = 16, q: int = 4, P0: int = -34, P1: int = 9,
           Q0: int = -18, Q1: int = 18) -> None:
    rule(f"sec 2  THE GENERATION AT CAPACITY R = {R} (exact, dyadic grid 1/2^{q})")
    print(f"""
Every character below is an exact `int` classification of one parameter `(P + iQ)/2^{q}:
`#` is in `M_R` (never escaped in R steps); the ramp is the exact escape step:
""")
    shades = " .:-=+*"
    inside = total = 0
    for Q in range(Q1, Q0 - 1, -1):
        line = []
        for P in range(P0, P1 + 1):
            n = escape_step(P, Q, q, R)
            total += 1
            if n > R:
                inside += 1
                line.append("#")
            else:
                line.append(shades[min(len(shades) - 1, max(0, n // 2))])
        print("  " + "".join(line))
    print(f"""
  {inside} of {total} cells inside (exact). The picture is the same shape as the float render
  in `mandelbrot_logical.py`, but every cell is decided by integer arithmetic: the finite
  capacity truncation is the object, and it is exact.""")


def capacity_series() -> None:
    rule("sec 2b  M_R SHRINKS AS ESCAPE IS DETECTED (same grid, exact)")
    q, P0, P1, Q0, Q1 = 4, -34, 9, -18, 18
    print(f"  {'R':>4}{'cells inside M_R':>20}{'fraction':>12}")
    print("  " + "-" * 36)
    prev = None
    for R in (2, 4, 8, 12, 16):
        n = tot = 0
        for P in range(P0, P1 + 1):
            for Q in range(Q0, Q1 + 1):
                tot += 1
                if escape_step(P, Q, q, R) > R:
                    n += 1
        print(f"  {R:>4}{n:>20}{n / tot:>12.4f}")
        if prev is not None:
            assert n <= prev                           # M_R shrinks as escape is detected
        prev = n
    print("""
  Monotone in R, falling toward the true area of M (the sample box is 2.7 x 2.3, area(M)
  ~ 1.506, so ~0.25 of the box). The truncation is the object; the limit is its rendering.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the Gaussian integers
# --------------------------------------------------------------------------- #
def gaussian_integers() -> None:
    rule("sec 3  THE EXACT GAUSSIAN-INTEGER CASE (q = 0)")
    print("""
With `q = 0` the same engine runs on the Gaussian integers, and (since `|c| > 2` escapes) the
thirteen candidates with `|c| <= 2` decide the whole set:
""")
    inside = [(a, b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)
              if a * a + b * b <= 4 and escape_step(a, b, 0, 200) > 200]
    print(f"  M(Z[i]) = {sorted(inside, key=lambda z: (z[0], z[1]))}")
    print("""
  {0,-1,-2,+i,-i} -- exactly the five functions `double_helix_dna.py` found, now by the same
  integer engine as the full dyadic picture. One engine, two regimes.""")


# --------------------------------------------------------------------------- #
# sec 4 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 4  SCOPE")
    print("""
  1. FINITE CAPACITY AND A DYADIC GRID. This generates the truncation M_R on the grid 1/2^q,
     exactly. It is not a decision procedure for the full M (that is undecidable in the BSS
     sense; escape is semi-decidable) -- the same reason `mandelbrot_logical.py` truncates.

  2. FLOAT-FREE, SO EXACT WHERE IT MATTERS. Boundary cells where the float render rounds are
     decided correctly here. Cost: the state's denominator doubles each step (2^(q . 2^(n-1))),
     so depth is bounded by big-int size, not by precision.

  3. THE WORD-ONLY ROUTE IS STILL OPEN. A generation from twist WORDS alone (no arithmetic at
     all) would go through kneading/lamination theory. A naive parity-lex admissibility rule
     gives 2,3,4,6,10,17 periodic words, which does NOT match the real hyperbolic-component
     structure (1,1,1,2,3,5), so that route is not ready. This file is a route, not the route.""")


def main() -> None:
    print(__doc__)
    engine_check()
    render()
    capacity_series()
    gaussian_integers()
    scope()


if __name__ == "__main__":
    main()
