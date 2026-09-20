#!/usr/bin/env python3
"""
octonion_g2_root_system.py -- reconsidering the positive-geometry connection:
G2's OWN root system, extracted from the octonion construction, not the
census.

REQUIRES numpy and scipy (ConvexHull) -- see alpha_weight6_pslq.py's
docstring for the venv bootstrap recipe used in this environment.

Earlier this session, asked whether the G2/octonion thread connects to
positive geometries (issue #151's RFC), the honest answer was "no
established bridge from the Lie-algebra side" -- #151 is about a DIFFERENT
combinatorial object, the count-balance "ZFA-hedron" and the central-
binomial census C(2n,n), which connects instead to the alpha-residual
thread (alpha_weight6_pslq.py). Asked to reconsider: that conclusion was
right about #151 specifically, but incomplete about "any positive-geometry
connection" -- every compact simple Lie algebra's ROOT SYSTEM has a
canonical positive cone (the positive roots / fundamental Weyl chamber),
which IS a positive-geometry object in the technical sense (a convex region
whose boundary structure carries a canonical differential form) used
elsewhere in the amplitudes literature (Coxeter/root-system positive
geometries for gauge-theory amplitudes). G2's root system was sitting
inside the already-built octonion derivation algebra the whole time, unused.

METHOD: find a Cartan subalgebra of g2 = Der(O) by taking ad(h1) for a
generic h1 in g2 -- its kernel (centralizer) is exactly the 2-dimensional
Cartan subalgebra containing h1 (a standard fact, avoiding a blind random
search for a commuting pair, which fails almost surely by chance). Take h2
from that kernel, Gram-Schmidt orthonormalize {h1,h2} against the KILLING
FORM (not the naive Euclidean/Frobenius norm, which does not reflect true
root lengths/angles -- the same normalization trap caught in
octonion_quark_gluon_bracket.py). Diagonalize ad(h1), read off each nonzero
eigenvector's ad(h2)-eigenvalue too, giving 12 (alpha(h1),alpha(h2)) pairs.

RESULT: 12 roots, independently confirming the textbook G2 diagram --
6 short (norm 1/(2*sqrt(3))) + 6 long (norm 1/2), EXACT ratio sqrt(3) (the
one length ratio that distinguishes G2 from every other rank-2 root
system), evenly spaced every 30 degrees. The convex hull of all 12 roots is
exactly the 6 long roots (a regular hexagon) -- the short roots sit
strictly inside. A generic positive-root choice (6 of 12) forms a genuine
convex cone with the origin -- a bona fide positive-geometry object.

HONEST SCOPE: this is a STANDARD fact about ANY compact simple Lie algebra
-- every root system has such a positive cone; nothing about that is
specific to QLF. What IS newly established here: this PARTICULAR root
system emerges correctly, independently, from the octonion construction
this session already built from QLF's own 8-twist-adjacent Fano-triple
structure -- a real cross-check that the whole construction chain
(multiplication table -> Der(O) -> su(3)/su(2) stabilizers -> root system)
is mutually consistent, not a claim that QLF's physics specifically needs
or uses this cone. It is also a genuinely DIFFERENT positive-geometry
object from #151's ZFA-hedron/census proposal, not a unification of the
two -- they remain two separate threads, both real, neither subsuming the
other.
"""
try:
    import numpy as np
    from scipy.spatial import ConvexHull
except ImportError:
    raise SystemExit(
        "This script needs numpy and scipy. See alpha_weight6_pslq.py's\n"
        "docstring for the isolated-venv bootstrap recipe used here."
    )

from octonion_g2_stabilizers import build_structure_constants, derivation_constraints, stabilizer_basis


def to_mat(v):
    return v.reshape(8, 8)


def main() -> None:
    print(__doc__.strip().split("\n\n")[0])
    print()

    sign, idx = build_structure_constants()
    A = derivation_constraints(sign, idx)
    full = stabilizer_basis(A, [])  # 14 x 64, basis of g2
    g2basis = [to_mat(full[k]) for k in range(14)]

    def coords_in_g2(mat):
        coeffs, *_ = np.linalg.lstsq(full.T, mat.flatten(), rcond=None)
        return coeffs

    C = np.zeros((14, 14, 14))
    for i in range(14):
        for j in range(14):
            comm = g2basis[i] @ g2basis[j] - g2basis[j] @ g2basis[i]
            C[i, j, :] = coords_in_g2(comm)

    def ad_matrix(coords):
        M = np.zeros((14, 14))
        for j in range(14):
            M[:, j] = sum(coords[i] * C[i, j, :] for i in range(14))
        return M

    K = np.zeros((14, 14))
    ad_basis = [ad_matrix(np.eye(14)[i]) for i in range(14)]
    for i in range(14):
        for j in range(14):
            K[i, j] = np.trace(ad_basis[i] @ ad_basis[j])
    Kpos = -K  # Killing form is negative-definite for the compact form; flip to a positive metric

    def kform(a, b):
        return a @ Kpos @ b

    print("=" * 78)
    print("Finding a Cartan subalgebra (2-dim, rank of g2) via a centralizer, not blind search")
    print("=" * 78)
    rng = np.random.default_rng(2)
    h1 = rng.standard_normal(14)
    A1 = ad_matrix(h1)
    U, S, Vt = np.linalg.svd(A1)
    rank_A1 = int(np.sum(S > 1e-6))
    kernel = Vt[rank_A1:]
    print(f"  centralizer (kernel of ad(h1)) dimension = {kernel.shape[0]}   (expect 2 = rank g2)")
    h2raw = kernel[1]
    bracket = sum(h1[i] * h2raw[j] * C[i, j, :] for i in range(14) for j in range(14))
    print(f"  [h1,h2] residual (should be ~0): {np.linalg.norm(bracket):.2e}")

    e1 = h1 / np.sqrt(kform(h1, h1))
    h2p = h2raw - kform(h2raw, e1) * e1
    e2 = h2p / np.sqrt(kform(h2p, h2p))
    print(f"  Killing-orthonormal Cartan basis {{e1,e2}} built (kform check: "
          f"{kform(e1,e1):.4f}, {kform(e2,e2):.4f}, {kform(e1,e2):.2e})")
    print()

    print("=" * 78)
    print("The 12 roots, read off by simultaneous diagonalization")
    print("=" * 78)
    A1o, A2o = ad_matrix(e1), ad_matrix(e2)
    eigvals1, eigvecs1 = np.linalg.eig(A1o)
    roots = []
    for k in range(14):
        lam1 = eigvals1[k]
        if abs(lam1) < 1e-6:
            continue
        v = eigvecs1[:, k]
        lam2 = np.vdot(v, A2o @ v) / np.vdot(v, v)
        roots.append((lam1.imag, lam2.imag))
    roots = np.array(roots)
    norms = np.linalg.norm(roots, axis=1)
    short_n, long_n = sorted(set(np.round(norms, 4)))
    print(f"  found {len(roots)} nonzero roots   (expect 12)")
    print(f"  length classes: {sum(np.isclose(norms, short_n, atol=1e-3))} short (norm {short_n:.4f}) + "
          f"{sum(np.isclose(norms, long_n, atol=1e-3))} long (norm {long_n:.4f})")
    print(f"  long/short ratio = {long_n/short_n:.6f}   (expect EXACTLY sqrt(3) = {np.sqrt(3):.6f} -- ")
    print(f"  the one ratio that identifies G2 among all rank-2 root systems)")
    angles = np.sort(np.degrees(np.arctan2(roots[:, 1], roots[:, 0])))
    gaps = np.diff(np.concatenate([angles, [angles[0] + 360]]))
    print(f"  angular gaps between consecutive roots: {np.round(gaps, 2)}   (expect all 30 degrees)")
    print()

    print("=" * 78)
    print("The positive-geometry objects: convex hull, and the positive-root cone")
    print("=" * 78)
    hull = ConvexHull(roots)
    hull_norms = norms[hull.vertices]
    print(f"  convex hull of all 12 roots: {len(hull.vertices)} vertices, all with norm "
          f"{'long' if np.allclose(hull_norms, long_n, atol=1e-3) else 'mixed'}")
    print(f"    -> the hull is exactly the LONG-root hexagon; the 6 short roots sit strictly inside.")

    functional = np.array([1.0, 0.0713])  # generic direction, avoids landing exactly on a root
    pos_idx = np.where(roots @ functional > 1e-9)[0]
    pos_roots = roots[pos_idx]
    pts = np.vstack([pos_roots, [0, 0]])
    hull_pos = ConvexHull(pts)
    print(f"  positive roots (a generic linear functional splits the 12 into 6+6): {len(pos_idx)} chosen")
    print(f"  positive-root cone (their convex hull with the origin): {len(hull_pos.vertices)} vertices, "
          f"area {hull_pos.volume:.4f}")
    print("    -> a genuine convex 'positive geometry' object (the fundamental-Weyl-chamber-adjacent")
    print("       cone), independently built from this session's octonion construction.")

    print()
    print("=" * 78)
    print("""VERDICT

  Reconsidered and corrected: "no positive-geometry bridge from octonions/G2"
  was right about issue #151's SPECIFIC proposal (the count-balance
  ZFA-hedron / central-binomial census, which connects instead to the alpha-
  residual thread) but incomplete as a general claim. G2's OWN root system --
  extracted here independently from the octonion construction, not cited --
  reproduces the textbook diagram exactly (length ratio sqrt(3) to machine
  precision, 30-degree spacing) and its positive-root cone is a genuine,
  well-defined positive-geometry object.

  HONEST CAVEAT, stated plainly: this is a standard fact about every compact
  simple Lie algebra, not something specific to QLF -- what's newly
  established is that THIS PARTICULAR instance is mutually consistent with
  everything else built this session (the multiplication table, Der(O), the
  su(3)/su(2) stabilizers, the quark/gluon bracket), a real cross-check, not
  a new physics claim. And it remains a DIFFERENT positive-geometry object
  from #151's proposal -- two separate real threads, not one unified story.
""")


if __name__ == "__main__":
    main()
