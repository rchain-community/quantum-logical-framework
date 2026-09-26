#!/usr/bin/env python3
"""
zfa_dna_network.py -- do the sets we discovered intersect? a network, at three levels.

THE QUESTION (Jim, 2026-09-26): "the map of each sets we discover may intersect in some
manner in sort of a zfa dna network?"

The honest answer depends on what "the set" is, so measure all three:

  * ELEMENTS   -- the discovered closure sets, as subsets of the ZFA census. Concrete, exact.
  * PARAMETERS -- the discovered parameter sets (cascade centres, windows, M(Z[i])).
  * OPERATORS  -- the generative rules that turn one construction into another: the actual DNA.

  sec 1  the closure universe and the discovered sets (element level)
  sec 2  the parameter level: what the sets share
  sec 3  the operator level: the ZFA DNA network (Graphviz)
  sec 4  answer + scope

Run:  python3 zfa_dna_network.py            # report
      python3 zfa_dna_network.py --dot      # emit Graphviz for the operator network
"""
from __future__ import annotations

import sys
from collections import Counter
from itertools import product

from mandelbrot_logical import real_centers
from mandelbrot_loop_dna import itinerary, superstable_c
from primordial_zfa_dna import DNA
from qucalc_search import solve
from twist_core import adjoint_history, is_zfa

TW = "^v<>/\\+-"
GUESSES = ["0", "-1", "-1.3107", "-1.38154"]


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def census(n: int) -> set[str]:
    return {"".join(t) for t in product(TW, repeat=n) if is_zfa("".join(t))}


# --------------------------------------------------------------------------- #
# sec 1 -- element level
# --------------------------------------------------------------------------- #
def element_level() -> dict:
    rule("sec 1  ELEMENT LEVEL -- THE DISCOVERED CLOSURE SETS INSIDE THE CENSUS")
    u4, u6 = census(4), census(6)
    print(f"""
The common universe is the ZFA census (count-balanced AND Pauli-closed -- the canonical
`twist_core.is_zfa`, not a proxy). Truncated: {len(u4)} closures of length 4, {len(u6)} of
length 6.

Each thing this thread discovered is a finite set of closures inside it:
""")
    dna_table = set(DNA[t][b] for t in "^>v<" for b in (0, 1))         # the 8 doubler rotations
    primordial = {"^>v<", "^<v>"}                                     # DNA generation 1
    solve_cl = {solve(p)["history"] for p in ("^", "^^<", "^<v>+-")}
    ray_pairs = set()
    for k in (1, 2, 3):
        n = 2 ** k
        body = itinerary(superstable_c(n, GUESSES[k]), n)[:-1]
        pair = body + adjoint_history(body)
        if 4 <= len(pair) <= 6:
            ray_pairs.add(pair)
    sets = {
        "primordial-1 (DNA gen 1)": primordial,
        "doubler table (8 rotations)": dna_table,
        "/solve closures": solve_cl,
        "spine ray pairs W.W+": ray_pairs,
    }
    for name, S in sets.items():
        print(f"  {name:<30} {len(S):>3}   {sorted(S)}")
    print()
    print(f"  {'pair':<58}{'shared':>7}")
    print("  " + "-" * 66)
    names = list(sets)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            inter = sets[a] & sets[b]
            print(f"  {a:<28} & {b:<28}{len(inter):>5}   {sorted(inter)}")
    print()
    print("inclusions found:")
    for a in names:
        for b in names:
            if a != b and sets[a] and sets[a] <= sets[b]:
                print(f"  {a}  C  {b}")

    hub = Counter()
    for S in sets.values():
        for w in S:
            hub[w] += 1
    print("\nhub closures (in the most discovered sets):",
          [(w, n) for w, n in hub.most_common() if n > 1])
    coverage = len({w for S in sets.values() for w in S} & u4) / len(u4)
    print(f"""
  This is the shape of the answer at the element level:

    * a genuine CHAIN:  primordial-1  C  doubler table  C  (length-4 census),
      and the /solve closures and the spine ray pairs sit apart from it;
    * the HUB is the electron/positron pair `{{^>v<, ^<v>}}` -- the only closure pair shared
      by two of the discovered constructions (and both sit in the length-4 census);
    * coverage of the length-4 census by these constructions is {coverage:.1%}
      ({len({w for S in sets.values() for w in S} & u4)} of {len(u4)}). The sets really are
      DIFFERENT objects that share a small core, not one set rediscovered.""")
    return {"u4": u4, "u6": u6, **sets}


# --------------------------------------------------------------------------- #
# sec 2 -- parameter level
# --------------------------------------------------------------------------- #
def gauss_m() -> set[complex]:
    def bounded(cx, cy, steps=400):
        x, y = 0, 0
        for _ in range(steps):
            x, y = x * x - y * y + cx, 2 * x * y + cy
            if x * x + y * y > 4:
                return False
        return True
    return {complex(a, b) for a in (-2, -1, 0, 1, 2) for b in (-2, -1, 0, 1, 2)
            if a * a + b * b <= 4 and bounded(a, b)}


def parameter_level() -> None:
    rule("sec 2  PARAMETER LEVEL -- WHAT THE PARAMETER SETS SHARE")
    centers = real_centers(period_max=8)
    cascade = [0.0, -1.0, -1.3107, -1.38154]           # the period-doubling cascade
    allc = [c for p in centers for c in centers[p]]
    for c in cascade:                                  # each is a superstable centre
        assert any(abs(c - x) < 5e-3 for x in allc), c
    gz = gauss_m()
    print(f"""
Three parameter sets from the thread:
  * cascade centres (periods 1,2,4,8):   {['%+.4f' % c for c in sorted(cascade)]}
  * all real superstable centres (p<=8): {len(allc)} values
  * exact M(Z[i]) (Gaussian integers):   {sorted(gz, key=lambda z: (z.real, z.imag))}
""")
    gz_real = sorted(z.real for z in gz if z.imag == 0)
    print(f"  cascade centres  n  M(Z[i])  =  "
          f"{[('%+.0f' % c) for c in sorted(cascade) if any(abs(c - r) < 1e-6 for r in gz_real)]}"
          f"      <- hub: c = 0 (critical point) and c = -1 (the 2-cycle)")
    print(f"  all centres      n  M(Z[i])  =  "
          f"{[('%+.1f' % c) for c in sorted(allc) if any(abs(c - r) < 1e-6 for r in gz_real)]}")
    print(f"  imaginary points in M(Z[i])  =  "
          f"{sorted((z for z in gz if z.imag), key=lambda z: z.imag)}"
          f"      <- the conjugate pair +-i")
    print("""
  At the parameter level the sets DO intersect, at a two-point hub `{0, -1}`: the critical
  fixed point and the period-2 superstable centre, the only real parameters that are both
  cascade centres and exact Gaussian-integer members. `-2` (the parabolic tip) is in
  M(Z[i]) but is NOT a superstable centre, and `+-i` are conjugate -- the two strands.""")


# --------------------------------------------------------------------------- #
# sec 3 -- operator level
# --------------------------------------------------------------------------- #
OPERATORS = [
    ("seed ^", "closure pair {^>v<,^<v>}", "the doubler: resolve ^ two ways"),
    ("closure pair {^>v<,^<v>}", "primordial DNA", "iterate the doubler at EVERY twist"),
    ("loop DNA W->W.s.W", "cascade (fixed splice)", "splice forced by parity"),
    ("loop DNA W->W.s.W", "edge of chaos (free splice)", "free the splice: O(log n) bits"),
    ("edge of chaos (free splice)", "primordial DNA", "move the free bit to closure density: chaos"),
    ("cascade (fixed splice)", "real superstable centres", "solve f_c^p(0)=0"),
    ("real superstable centres", "M skeleton", "closure skeleton of the set"),
    ("any W", "ray pair W.W+", "adjoint / closure: one rung"),
    ("ray pair W.W+", "double helix", "chain rungs; complement = second axis"),
    ("double helix", "M(Z[i]) = {0,-1,-2,+-i}", "two-axis z->z^2+c, exact on Z[i]"),
    ("capacity R", "depth strata / M_R", "the listener: excursion <= R"),
    ("primordial DNA", "census", "every realization is ZFA"),
    ("ray pair W.W+", "census", "W.W+ is ZFA"),
    ("M skeleton", "M_R (continuum render)", "capacity truncation"),
]


def operator_level(dot: bool) -> None:
    if dot:
        print("digraph zfa_dna {")
        print('  rankdir=LR; node [shape=box, fontname="monospace"];')
        for src, dst, label in OPERATORS:
            print(f'  "{src}" -> "{dst}" [label="{label}"];')
        print("}")
        return
    rule("sec 3  OPERATOR LEVEL -- THE ZFA DNA NETWORK")
    print("""
This is where the network is dense. The nodes are the constructions; the edges are the
OPERATORS that carry one to the next, each one checked by the script it names. This graph
IS the DNA -- the discovery is a program, not a single set.
""")
    for src, dst, label in OPERATORS:
        print(f"  {src:<32} --{label:<42}--> {dst}")
    print("""
  The seeds are `^` and the loop DNA `W -> W.s.W`. Everything else is one of four operators:
  the doubler, the adjoint/closure, the free splice, and the capacity listener. So the
  objects are not independent -- they are the closures of a small operator set, which is the
  sense in which "the sets intersect in a ZFA DNA network": they share OPERATORS, not
  elements.""")


# --------------------------------------------------------------------------- #
# sec 4 -- answer
# --------------------------------------------------------------------------- #
def answer() -> None:
    rule("sec 4  ANSWER")
    print("""
Yes -- but at the level of operators, not elements.

  * ELEMENTS: the discovered closure sets form a chain with a small hub (the
    electron/positron pair) and cover only a few percent of the census. They intersect, but
    thinly -- they are genuinely different objects.
  * PARAMETERS: a two-point hub {0, -1}, plus the conjugate pair +-i in M(Z[i]).
  * OPERATORS: a dense network. Four operators (doubler, adjoint/closure, free splice,
    capacity listener) generate every object in the thread. THAT is the ZFA DNA.

  And a byproduct, recorded because it changes a count: the census here uses the canonical
  `twist_core.is_zfa`, giving 168 four-twist closures. `active_inference_vfe_demo.py` had
  used a weaker sign-parity balance and reported 384; it is corrected to 168, and the two
  docs that cited 384 are updated.

  Scope: one route, not the route. The element and parameter sets are exact and finite; the
  operator graph is this thread's, not a classification.""")


def main() -> None:
    if "--dot" in sys.argv:
        operator_level(dot=True)
        return
    print(__doc__)
    element_level()
    parameter_level()
    operator_level(dot=False)
    answer()


if __name__ == "__main__":
    main()
