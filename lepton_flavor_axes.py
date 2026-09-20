#!/usr/bin/env python3
"""
lepton_flavor_axes.py — the axis (colour) content of lepton-like closures.

An easy step toward issue #140 (lepton flavor mass-ratio map + μ/τ colour
content). QLF says colour = the three spatial axes; a lepton is a colour
**singlet** (B = 0, free), but the electron loop `^<v>` is machine-verified to
engage **two** axes {x, y} (`interleaved_xlvr_folds_to_negI`). The open question
is each generation's axis/colour **content**.

This tool reads off, for any twist loop, which spatial axes it engages
(`^v`=Y, `><`=X, `/\\`=Z), its Pauli fold, and whether it closes (ZFA) — reusing
`twist_core.py`. It then **enumerates** short spatial ZFA loops and classifies
them by axis content, exhibiting the candidate space for e / μ / τ: the
electron's {x, y} is the verified anchor, and 1-axis, other-2-axis, and 3-axis
singlet closures also exist — candidate deeper-generation contents.

HONEST SCOPE: this maps the *available* axis contents; it does **not** assert
which loop is the muon or tau — that is the open derivation (#140). Reuses
`twist_core.py`; no other deps.  Run:  python3 lepton_flavor_axes.py
"""
import itertools
from twist_core import pauli_fold, is_pauli_closed, calculate_action

SPATIAL = "^v<>/\\"                                   # the six spatial twists (no gauge +-)
AXIS = {'^': 'Y', 'v': 'Y', '>': 'X', '<': 'X', '/': 'Z', '\\': 'Z'}   # axOf

# baryonNumber = Σ signTriple over sliding triples (QLF_BaryonWinding.lean):
# signTriple is the Levi-Civita of the three axes (±1 on x,y,z permutations, else 0).
_EVEN = {('X', 'Y', 'Z'), ('Y', 'Z', 'X'), ('Z', 'X', 'Y')}
_ODD = {('X', 'Z', 'Y'), ('Z', 'Y', 'X'), ('Y', 'X', 'Z')}


def sign_triple(a, b, c) -> int:
    t = (a, b, c)
    return 1 if t in _EVEN else -1 if t in _ODD else 0


def baryon_number(h: str) -> int:
    """B = Σ signTriple(axOf aᵢ, axOf aᵢ₊₁, axOf aᵢ₊₂) — the 3-axis winding.
    B = 0 ⟺ colour singlet (a free lepton); B ≠ 0 ⟺ a confined Borromean baryon."""
    ax = [AXIS.get(t) for t in h]
    return sum(sign_triple(ax[i], ax[i + 1], ax[i + 2]) for i in range(len(ax) - 2))


def axes_engaged(h: str) -> str:
    """The set of spatial axes a loop engages, as a sorted string e.g. 'XY'."""
    return "".join(sorted({AXIS[t] for t in h if t in AXIS}))


def fold_str(h: str) -> str:
    a, _, _, _ = pauli_fold(h)
    if not is_pauli_closed(h):
        return "open"
    for s, name in ((1, "+I"), (-1, "-I"), (1j, "+iI"), (-1j, "-iI")):
        if abs(a - s) < 1e-9:
            return name
    return f"{a:.2g}I"


def spatial_zfa(h: str) -> bool:
    """A spatial ZFA closure: count-balanced on each axis AND Pauli-closed.
    (Bypasses twist_core.is_zfa's min-length gate so length-4 loops like the
    electron count.)"""
    return all(x == 0 for x in calculate_action(h)) and is_pauli_closed(h)


def report(h: str, label: str = "") -> None:
    tag = f"   ({label})" if label else ""
    print(f"  {h:8}  axes={axes_engaged(h) or '—':3}  fold={fold_str(h):4}  "
          f"B={baryon_number(h):+d}  zfa={spatial_zfa(h)!s:5}  depth={len(h)//2}{tag}")


def main() -> None:
    print(__doc__.strip().split("\n\n")[0])
    print()
    print("Verified anchor — the electron (B=0 colour singlet, free):")
    report("^<v>", "{x,y}, -I  (interleaved_xlvr_folds_to_negI)")
    print()

    for L in (4, 6):
        # bucket by (axis content, is-lepton-singlet?)
        lept: dict[str, list[str]] = {}     # B = 0  → free-lepton candidates
        bary: dict[str, list[str]] = {}     # B ≠ 0  → confined baryons
        for combo in itertools.product(SPATIAL, repeat=L):
            h = "".join(combo)
            if spatial_zfa(h):
                (lept if baryon_number(h) == 0 else bary).setdefault(axes_engaged(h), []).append(h)
        nl = sum(len(v) for v in lept.values())
        nb = sum(len(v) for v in bary.values())
        print(f"Spatial ZFA loops of length {L}:  {nl} lepton singlets (B=0)  +  {nb} baryons (B≠0)")
        print(f"  {'axes':4}  {'lepton (B=0)':>13}  {'baryon (B≠0)':>13}   lepton example")
        for ax in sorted(set(lept) | set(bary), key=lambda a: (len(a), a)):
            ex = lept.get(ax, [""])[0]
            print(f"  {ax or '—':4}  {len(lept.get(ax, [])):>13}  {len(bary.get(ax, [])):>13}   {ex}")
        print()

    print("Reading:")
    print("  • Every axis content — 1-axis, each 2-axis pair, and the full 3-axis {x,y,z} —")
    print("    has B=0 SINGLET closures: legitimate free-lepton candidates. The electron is")
    print("    a 2-axis {x,y} singlet; a 3-axis {x,y,z} B=0 singlet (e.g. `^v<>/\\`) is a")
    print("    concrete candidate 'three-colour' lepton content for the τ.")
    print("  • The B≠0 closures at length 6 are the confined Borromean baryons — correctly")
    print("    NOT free leptons (they carry a net 3-axis winding).")
    print("  Next (#140): among the B=0 singlets, pick the μ/τ contents at the right fold")
    print("  depth (m=1/R) that reproduce the Koide-constrained mass ratios.")


if __name__ == "__main__":
    main()
