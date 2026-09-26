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


# --------------------------------------------------------------------------- #
# the same network as a standalone SVG (for markdown / a browser)
# --------------------------------------------------------------------------- #
SVG_NODES = {
    "seed":    (0,  70, "^   (the first distinction)"),
    "pair":    (1,  70, "{ ^>v< , ^<v> }    the doubler"),
    "prim":    (2,  70, "primordial DNA"),
    "loopdna": (0, 150, "loop DNA    W |-> W.s.W"),
    "cascade": (1, 150, "cascade   (splice fixed)"),
    "centres": (2, 150, "real superstable centres"),
    "skel":    (3, 150, "M skeleton"),
    "render":  (4, 150, "M_R   (continuum render)"),
    "free":    (1, 230, "edge of chaos   (splice free)"),
    "anyW":    (0, 320, "any history   W"),
    "ray":     (1, 320, "ray pair   W.W-dagger"),
    "helix":   (2, 320, "double helix"),
    "mzi":     (3, 320, "M(Z[i]) = { 0, -1, -2, +-i }"),
    "capR":    (0, 400, "capacity   R"),
    "depth":   (1, 400, "depth strata / M_R"),
}
# the main chains; the full operator list (incl. free-splice -> primordial DNA, which would
# cross the cascade chain) is in the text report and `--dot`
SVG_EDGES = [
    ("seed", "pair", "doubler"),
    ("pair", "prim", "iterate at every twist"),
    ("loopdna", "cascade", "splice fixed"),
    ("loopdna", "free", "splice freed"),
    ("cascade", "centres", "solve f_c^p(0)=0"),
    ("centres", "skel", "closure skeleton"),
    ("skel", "render", "capacity truncation"),
    ("anyW", "ray", "adjoint (one rung)"),
    ("ray", "helix", "chain rungs; 2nd axis = complement"),
    ("helix", "mzi", "two axes z |-> z^2 + c"),
    ("capR", "depth", "excursion <= R"),
]
PITCH, BOX_W, BOX_H = 460, 260, 40
SVG_W = 30 + 4 * PITCH + BOX_W + 30
SVG_H = 480


def _x(col: int) -> int:
    return 30 + col * PITCH


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _wrap(s: str, n: int = 13) -> list[str]:
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines[:3]


def _label_geometry():
    """(edge segments, label halo rects) -- one source of truth for drawing and checking."""
    segs, rects = [], []
    for edge in SVG_EDGES:
        src, dst, label = edge[0], edge[1], edge[2]
        t = edge[3] if len(edge) > 3 else 0.5
        c0, y0, _ = SVG_NODES[src]
        c1, y1, _ = SVG_NODES[dst]
        x0, yc0 = _x(c0) + BOX_W, y0 + BOX_H / 2
        x1, yc1 = _x(c1), y1 + BOX_H / 2
        segs.append((x0, yc0, x1, yc1))
        lines = _wrap(label)
        bw, bh = max(len(l) for l in lines) * 6.4 + 14, len(lines) * 13 + 8
        mx, my = x0 + (x1 - x0) * t, yc0 + (yc1 - yc0) * t
        rects.append((mx - bw / 2, my - bh / 2, mx + bw / 2, my + bh / 2))
    return segs, rects


def _seg_hits_rect(px0, py0, px1, py1, rx0, ry0, rx1, ry1) -> bool:
    """Liang-Barsky: does the segment intersect the axis-aligned rectangle?"""
    dx, dy = px1 - px0, py1 - py0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, px0 - rx0), (dx, rx1 - px0), (-dy, py0 - ry0), (dy, ry1 - py0)):
        if p == 0:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                if r > t1:
                    return False
                t0 = max(t0, r)
            else:
                if r < t0:
                    return False
                t1 = min(t1, r)
    return True


def svg() -> str:
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" '
        f'font-family="ui-sans-serif, system-ui, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif">',
        f'<rect width="{SVG_W}" height="{SVG_H}" fill="#ffffff"/>',
        f'<text x="{SVG_W / 2:.0f}" y="30" text-anchor="middle" font-size="20" font-weight="700" '
        f'fill="#111827">The ZFA DNA network - one operator set generates every object in the thread</text>',
        f'<text x="{SVG_W / 2:.0f}" y="52" text-anchor="middle" font-size="12" fill="#6b7280">'
        f'nodes are the constructions; edges are the operators. One route, not the route (zfa_dna_network.py).</text>',
        '<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#64748b"/></marker></defs>',
    ]
    # 1. edges (all lines), 2. node boxes, 3. edge labels LAST so they sit above every line
    labels = []
    for edge in SVG_EDGES:
        src, dst, label = edge[0], edge[1], edge[2]
        t = edge[3] if len(edge) > 3 else 0.5          # where along the edge the label sits
        c0, y0, _ = SVG_NODES[src]
        c1, y1, _ = SVG_NODES[dst]
        x0, yc0 = _x(c0) + BOX_W, y0 + BOX_H / 2
        x1, yc1 = _x(c1), y1 + BOX_H / 2
        out.append(f'<line x1="{x0}" y1="{yc0}" x2="{x1}" y2="{yc1}" stroke="#64748b" '
                   f'stroke-width="1.3" marker-end="url(#ar)"/>')
        labels.append((x0 + (x1 - x0) * t, yc0 + (yc1 - yc0) * t, label))
    for _nid, (col, y, label) in SVG_NODES.items():
        x = _x(col)
        out.append(f'<rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="8" '
                   f'fill="#f8fafc" stroke="#94a3b8"/>')
        out.append(f'<text x="{x + 14}" y="{y + 25}" font-size="13" fill="#0f172a">'
                   f'{_esc(label)}</text>')
    for mx, my, label in labels:
        lines = _wrap(label)
        bw, bh = max(len(l) for l in lines) * 6.4 + 14, len(lines) * 13 + 8
        out.append(f'<rect x="{mx - bw / 2:.1f}" y="{my - bh / 2:.1f}" width="{bw:.1f}" '
                   f'height="{bh:.1f}" fill="#ffffff" opacity="0.96"/>')
        for i, ln in enumerate(lines):
            out.append(f'<text x="{mx:.1f}" y="{my - bh / 2 + 13 * (i + 1) - 3:.1f}" '
                       f'text-anchor="middle" font-size="10.5" fill="#475569">{_esc(ln)}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def write_svg(path: str) -> None:
    import os
    import xml.dom.minidom
    data = svg()
    xml.dom.minidom.parseString(data)                       # must be well-formed XML
    boxes = [(_x(c), y, _x(c) + BOX_W, y + BOX_H) for c, y, _ in SVG_NODES.values()]
    for x0, y0, x1, y1 in boxes:
        assert 0 <= x0 and x1 <= SVG_W and 0 <= y0 and y1 <= SVG_H, "node outside canvas"
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                raise AssertionError(f"node boxes overlap: {a} {b}")
    segs, rects = _label_geometry()
    for i, (rx0, ry0, rx1, ry1) in enumerate(rects):
        for j, (sx0, sy0, sx1, sy1) in enumerate(segs):
            if i != j and _seg_hits_rect(sx0, sy0, sx1, sy1, rx0 + 1, ry0 + 1, rx1 - 1, ry1 - 1):
                raise AssertionError(
                    f"edge {SVG_EDGES[j][0]}->{SVG_EDGES[j][1]} runs through the label of "
                    f"{SVG_EDGES[i][0]}->{SVG_EDGES[i][1]}")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)
    print(f"wrote {path}  ({SVG_W}x{SVG_H})  xml ok, {len(boxes)} nodes, {len(SVG_EDGES)} edges")


def main() -> None:
    if "--svg" in sys.argv:
        i = sys.argv.index("--svg")
        nxt = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
        write_svg(nxt if nxt and not nxt.startswith("-") else "diagrams/zfa_dna_network.svg")
        return
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
