#!/usr/bin/env python3
"""
lepton_flavor_interleave.py — candidate mu/tau twist loops, built the same way
as the verified electron anchor.

Toward issue #140 (lepton flavor mass-ratio map + mu/tau colour content).
`lepton_flavor_axes.py` classifies every short spatial ZFA singlet by which
axes it engages; this script narrows that space with the one structural
feature the electron's verified loop actually has: `^<v>` = [up, left, down,
right] is Y,X,Y,X — it never repeats an axis on the next twist, cyclically
(`interleaved_xlvr_folds_to_negI`, lean/QLF_TwistAlphabet.lean).

**What this finds, searched exhaustively (not guessed) over lengths 4/6/8:**

  - Length 4 (depth 2, the electron's depth): every 2-axis pair has exactly
    8 cyclically-interleaved B=0 singlets, ALL folding to -I. `^<v>` is one
    of the 8 in {x,y}; {x,z} and {y,z} have symmetric octets. No 3-axis
    interleaved candidate exists at length 4 (odd axis-count parity).

  - Length 6 (depth 3) is a DEAD END for this construction, for two
    different reasons: a 2-axis interleaved loop of length 6 needs 3
    occurrences of each axis, which can never count-balance (3 is odd —
    a parity obstruction). A 3-axis interleaved loop of length 6 DOES have
    768 count-balanced (B=0) candidates, but not one of them achieves Pauli
    closure — an algebraic obstruction, not a parity one. So there is no
    depth-3 sibling of the electron in this family, of either colour.

  - Length 8 (depth 4) is where both families reopen: every 2-axis pair has
    72 interleaved B=0 singlets and the 3-axis case has 288 — and this time
    EVERY one of them folds to +I, the opposite sign from length 4.

Reading: the natural next-generation candidates are not at "one step deeper"
(length 6) but at depth 4 — a **mu candidate** staying in the electron's two
transverse axes ({x,y}, depth 4, fold +I) and a **tau candidate** that is the
first to reach the longitudinal axis z ({x,y,z}, depth 4, fold +I) — sitting
at the SAME fold depth as each other, distinguished by axis content rather
than depth, with depth 3 structurally forbidden to this whole family.

HONEST SCOPE: this is a structural narrowing by one clean, verified-pattern-
derived criterion (cyclic interleaving), exhaustively searched — not a claim
that these specific loops ARE the muon and tau. Nothing here yet connects
this small "fold depth" (2, 4, ...) to the astronomically larger Markov-
blanket depth R that actually sets the absolute mass scale
(Per_Qubit_Mass_Quantum.md), nor to the Koide phase 2*pi*k/3. Those
identifications remain the open part of #140. Reuses twist_core.py and
lepton_flavor_axes.py; no other deps.
Run:  python3 lepton_flavor_interleave.py
"""
import itertools

from lepton_flavor_axes import AXIS, SPATIAL, axes_engaged, baryon_number, fold_str, spatial_zfa


def is_interleaved(h: str) -> bool:
    """No two CYCLICALLY adjacent twists share an axis -- the electron
    ^<v> = Y,X,Y,X pattern, generalized to any length/axis content."""
    ax = [AXIS[t] for t in h]
    return all(ax[i] != ax[(i + 1) % len(ax)] for i in range(len(ax)))


def enumerate_interleaved(L: int, require_zfa: bool = True) -> dict:
    """Cyclically-interleaved B=0 singlets of length L, grouped by axis
    content. With require_zfa=False, groups by (B=0, count-balanced only)
    instead -- used to distinguish parity obstructions from Pauli-closure
    obstructions."""
    found: dict[str, list[str]] = {}
    for combo in itertools.product(SPATIAL, repeat=L):
        h = "".join(combo)
        if not is_interleaved(h) or baryon_number(h) != 0:
            continue
        if require_zfa:
            ok = spatial_zfa(h)
        else:
            from twist_core import calculate_action
            ok = all(x == 0 for x in calculate_action(h))
        if ok:
            found.setdefault(axes_engaged(h), []).append(h)
    return found


def report_bucket(label: str, loops: list[str], show: int = 4) -> None:
    folds: dict[str, int] = {}
    for h in loops:
        folds[fold_str(h)] = folds.get(fold_str(h), 0) + 1
    print(f"  {label:4} {len(loops):4} interleaved B=0 singlets   fold tally: {folds}")
    for h in loops[:show]:
        print(f"       {h}")


def main() -> None:
    print(__doc__.strip().split("\n\n")[0])
    print()

    print("Verified anchor -- electron, length 4, {x,y}, interleaved:")
    print(f"  ^<v>      axes=XY  fold={fold_str('^<v>')}  B={baryon_number('^<v>'):+d}"
          f"  interleaved={is_interleaved('^<v>')}")
    print()

    print("=" * 72)
    print("Length 4 (depth 2, electron's depth)")
    print("=" * 72)
    for ax, loops in sorted(enumerate_interleaved(4).items(), key=lambda kv: (len(kv[0]), kv[0])):
        report_bucket(ax, loops)
    print()

    print("=" * 72)
    print("Length 6 (depth 3) -- checking WHY nothing survives")
    print("=" * 72)
    balanced_only = enumerate_interleaved(6, require_zfa=False)
    zfa_only = enumerate_interleaved(6, require_zfa=True)
    for ax in sorted(set(balanced_only) | set(zfa_only), key=lambda a: (len(a), a)):
        nb = len(balanced_only.get(ax, []))
        nz = len(zfa_only.get(ax, []))
        print(f"  {ax:4} count-balanced(B=0): {nb:4}   also Pauli-closed (true ZFA): {nz:4}")
    print("  -> {x,y}/{x,z}/{y,z}: 0 count-balanced at all (3 occurrences/axis is odd --")
    print("     parity obstruction). {x,y,z}: 768 count-balanced, 0 Pauli-closed (an")
    print("     algebraic obstruction, not a parity one). No depth-3 candidate exists.")
    print()

    print("=" * 72)
    print("Length 8 (depth 4) -- both families reopen")
    print("=" * 72)
    for ax, loops in sorted(enumerate_interleaved(8).items(), key=lambda kv: (len(kv[0]), kv[0])):
        report_bucket(ax, loops)
    print()

    print("Reading:")
    print("  - mu candidate: {x,y} (or {x,z}/{y,z}), length 8, fold +I -- same colour as")
    print("    e, one interleaved period family deeper (depth 4, skipping the forbidden")
    print("    depth 3).")
    print("  - tau candidate: {x,y,z}, length 8, fold +I -- the first interleaved singlet")
    print("    to reach the longitudinal axis z, matching the Particle_Ladder.md #140")
    print("    hypothesis. Notably tau's candidate sits at the SAME depth as mu's here,")
    print("    not deeper -- axis content, not depth, is what could distinguish them in")
    print("    this family.")
    print("  - The sign flip -I (depth 2) -> +I (depth 4) is itself a clean, checked fact")
    print("    about this construction, independent of any e/mu/tau identification.")
    print()
    print("Still open (#140): picking ONE specific loop per generation (Lean has verified")
    print("only the electron's), and connecting this small fold depth to the Koide phase")
    print("2*pi*k/3 and to the Markov-blanket depth R that sets the actual mass scale.")


if __name__ == "__main__":
    main()
