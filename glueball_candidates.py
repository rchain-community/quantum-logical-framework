#!/usr/bin/env python3
"""
glueball_candidates.py — a first computational pass at glueball-like closures.

QLF's strong SU(3) is the TRACELESS part of the 3x3 directional-coupling
tensor of the three spatial axes: "the eight gluons... the directional
couplings AMONG the three axes" (Forces_From_Three_Axes.md, QLF_StrongAlgebra
.lean's `trace_commutator_zero` / `gluon_commutator_nonzero`). A quark's
colour is a NET WINDING on a single axis (QLF_BaryonWinding.lean's B, reused
from lepton_flavor_axes.py); a gluon, by contrast, is a COUPLING BETWEEN two
different axes -- an axis-changing step, not a single-axis one. A glueball is
a colour-SINGLET built purely from such couplings, with no net single-axis
(quark) colour charge -- i.e. B=0, same confinement rule as the lepton work,
but a candidate distinguishing feature is how symmetrically a closure visits
the three axis PAIRS {x,y},{y,z},{z,x} -- the three "gluon types."

This reuses `lepton_flavor_axes.py`'s enumeration of 3-axis B=0 singlets
(the 144 found at length 6, previously flagged there only as a candidate
"three-colour lepton" family) and asks a question that family was never
split on: does each closure visit the three axis-pairs EQUALLY, the way an
SU(3)-octet-symmetric singlet should?

FINDING (exhaustive, length 6): all 144 are permutations of the six spatial
generators ^v<>/\\ (forced -- three axes x two directions each, count-balanced
means each direction appears exactly once). Reading each as a cyclic axis
sequence and counting how many times each of the three axis-PAIRS is
adjacent splits them cleanly in two:
  - 96 loops (16 up to rotation) visit each pair EXACTLY once -- a genuinely
    axis-pair-symmetric ("SU(3)-octet-like") family. This is the natural
    GLUEBALL-candidate reading: no axis pair is favoured.
  - 48 loops (24 up to rotation) never place one particular pair adjacent,
    and double up on the other two -- an axis-pair-ASYMMETRIC family that
    favours two axes over the third, closer in spirit to the deep-lepton-
    generation candidates from lepton_flavor_interleave.py (which are also
    built by favouring specific axis pairs).
Both families fold to the SAME scalar (-I) -- the fold alone does not see
this split; the axis-pair-adjacency count does.

HONEST SCOPE: "gluon = axis-changing step" is a candidate reading of
Forces_From_Three_Axes.md's prose, not something Lean has verified -- there
is no lean/QLF_Glueball.lean. This narrows and re-characterizes an existing
candidate family by one clean, checked structural criterion; it does not
establish that either sub-family IS a glueball, nor connect this small fold
depth to QLF_MassGap.lean's `gaugeMassGap = log 2` (that module's "lightest
non-vacuum gauge closure" is a generic one-bit ZFA closure, not gluon-
specific -- an open connection, not claimed here). Reuses twist_core.py and
lepton_flavor_axes.py; no other deps. Run:  python3 glueball_candidates.py
"""
import itertools
from collections import Counter

from lepton_flavor_axes import AXIS, SPATIAL, axes_engaged, baryon_number, fold_str, spatial_zfa

PAIRS = (("X", "Y"), ("Y", "Z"), ("Z", "X"))


def pair_hist(h: str) -> Counter:
    """Count of cyclic-adjacent axis CHANGES, by which axis pair they cross --
    the candidate 'gluon type' of each transition."""
    ax = [AXIS[t] for t in h]
    n = len(ax)
    c: Counter = Counter()
    for i in range(n):
        a, b = ax[i], ax[(i + 1) % n]
        if a != b:
            c[frozenset((a, b))] += 1
    return c


def is_pair_symmetric(h: str) -> bool:
    """True if every axis pair is crossed the same (nonzero) number of times."""
    counts = [pair_hist(h).get(frozenset(p), 0) for p in PAIRS]
    return len(set(counts)) == 1 and counts[0] > 0


def canon_rotation(h: str) -> str:
    return min(h[i:] + h[:i] for i in range(len(h)))


def find_three_axis_singlets(L: int) -> list[str]:
    return [
        h for combo in itertools.product(SPATIAL, repeat=L)
        for h in ["".join(combo)]
        if baryon_number(h) == 0 and axes_engaged(h) == "XYZ" and spatial_zfa(h)
    ]


def main() -> None:
    print(__doc__.strip().split("\n\n")[0])
    print()

    L = 6
    found = find_three_axis_singlets(L)
    sym = [h for h in found if is_pair_symmetric(h)]
    asym = [h for h in found if not is_pair_symmetric(h)]

    print(f"Length {L}: {len(found)} colour-singlet (B=0) 3-axis closures "
          f"(Particle_Ladder.md's previously-uncharacterized '144 B=0 singlets').")
    all_perms_of_six = all(sorted(h) == sorted("^v<>/\\") for h in found)
    print(f"All are permutations of the six spatial generators: {all_perms_of_six}")
    print()

    print("GLUEBALL candidates -- axis-pair-symmetric (each pair crossed equally):")
    sym_necklaces = sorted(set(canon_rotation(h) for h in sym))
    print(f"  {len(sym)} closures, {len(sym_necklaces)} distinct up to rotation, "
          f"fold tally {Counter(fold_str(h) for h in sym)}")
    for h in sym_necklaces[:6]:
        print(f"    {h}   pair-hist={dict(pair_hist(h))}")
    print()

    print("Deep-lepton-generation candidates -- axis-pair-asymmetric (one pair skipped):")
    asym_necklaces = sorted(set(canon_rotation(h) for h in asym))
    print(f"  {len(asym)} closures, {len(asym_necklaces)} distinct up to rotation, "
          f"fold tally {Counter(fold_str(h) for h in asym)}")
    for h in asym_necklaces[:6]:
        print(f"    {h}   pair-hist={dict(pair_hist(h))}")
    print()

    print("Reading:")
    print("  - The axis-pair-symmetric family (16 necklaces) touches {x,y},{y,z},{z,x}")
    print("    exactly once each per cycle -- no axis pair privileged. That symmetry is")
    print("    the natural signature of an SU(3)-octet colour SINGLET built from all")
    print("    three 'gluon types' equally, distinct from the lepton family (which")
    print("    privileges specific axis pairs by construction, e.g. the electron's {x,y}).")
    print("  - The asymmetric family (24 necklaces) skips one axis-pair transition")
    print("    entirely -- structurally closer to the interleaved-lepton candidates in")
    print("    lepton_flavor_interleave.py, which are also built by favouring two axes.")
    print("  - Both fold to -I; the split is invisible to the fold value alone.")
    print()
    print("Still open: whether axis-pair symmetry is the RIGHT glueball criterion (no")
    print("Lean formalization of a gluon sub-alphabet exists), the connection to")
    print("gaugeMassGap = log 2 (QLF_MassGap.lean), and whether a length-shorter or")
    print("longer symmetric family exists (this pass checked length 6 only).")


if __name__ == "__main__":
    main()
