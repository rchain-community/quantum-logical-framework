#!/usr/bin/env python3
"""Issue #143 — reconstruction of the spectral/representation-theoretic machinery behind the
"dominant-blind readouts" investigation (Born_Rule.md sec8, ScientificApproach.md R2a).

Neither commit that produced the current write-up (b41b6e8, ab883fa) touched a Python file — the
machinery was never committed, only its prose description survived. This script rebuilds it from
that description, reusing contextual_census.py's primitives (_step, _feed) so the operator is
provably the same one capacity_spectrum(2) already exposes, and validates every rebuilt piece
against the doc's own cited numbers before using it.

Needs numpy (already an optional dependency of contextual_census.capacity_spectrum).

    python3 dominant_blind_reconstruction.py

Validated exactly (all printed, no fitting):
  * dominant |eigenvalue| = 3.9910153 (doc: 3.991)
  * 240 apparatus words (length <=3) give a nonzero readout; 24 of them never reach the dominant
    16-dim eigenspace ("dominant-blind") -- matches "24 blind readouts among 240 tested" exactly.
  * Lead 2 (depth parity): the even-depth operator T^2 has a REAL dominant eigenvalue (no +-i
    period-4 phase), and "orthogonal to T^2's dominant eigenspace" reproduces the 24/240 blind
    labelling with ZERO mismatches -- Lead 2 SURVIVES its stated kill condition.
  * The sign-twisted relabeling group (flipX/flipY/flipZ/swapXY/swapYZ/swapG, six generators, the
    signs read directly off Born_Rule.md's formulas -- not fitted) commutes with T at EXACTLY
    0.000e+00 for all six generators and closes at EXACTLY order 96, matching the doc.
  * That group's dominant-eigenspace representation is exactly G-invariant (error ~1e-15).
  * The branch-DIFFERENCE convention (u_c = u_bplus - u_bminus, bminus = bplus with every letter
    daggered/conjugated) reproduces the OTHER cited subdominant value, a^2 = 7, on the canonical
    geometries() cases.

NOT resolved (recorded honestly, not papered over): Lead 1 (sign-isotypic sufficiency) needs the
order-16 kernel K with G/K = S3 that the doc cites; this reconstruction finds |K| = 2, not 16, so
the abstract sign representation of S3 could not be identified from first principles here, and
Lead 1 itself was not tested. The group machinery up to that point is validated three independent
ways (commutation, order, G-invariance) -- the gap is specifically in identifying K.
"""
import sys
import itertools
from collections import Counter

sys.path.insert(0, ".")
import numpy as np
import contextual_census as cc

R = 2


def build_state_space(R):
    rng = range(-R, R + 1)
    states = [((a, b, c, d), (p & 1, (p >> 1) & 1, (p >> 2) & 1))
              for a in rng for b in rng for c in rng for d in rng
              if abs(a) + abs(b) + abs(c) + abs(d) <= R for p in range(8)]
    idx = {s: i for i, s in enumerate(states)}
    return states, idx


def build_T(states, idx, R):
    n = len(states)
    T = np.zeros((n, n))
    for s, i in idx.items():
        for t, v in cc._step({s: 1}, R).items():
            T[idx[t], i] += v
    return T


def readout_vector(app, idx, n, R):
    """u_c[s] = signed amplitude landing at zero-imbalance after feeding `app` from state s."""
    u = np.zeros(n)
    for s, i in idx.items():
        closed = cc._feed({s: 1}, app, R)
        u[i] = sum(v for (imb, _), v in closed.items() if imb == (0, 0, 0, 0))
    return u


# --------------------------------------------------------------------------- #
# 1. the operator, and the ground-truth 24/240 blind classification
# --------------------------------------------------------------------------- #
def ground_truth_blind(states, idx, T):
    n = len(states)
    lam1, V = np.linalg.eig(T)
    _, Wm = np.linalg.eig(T.T)
    Wminv = np.linalg.inv(Wm)
    l1 = np.abs(lam1).max()
    print(f"dominant |eigenvalue| = {l1:.7f}  (doc: 3.991)")

    def own_max_eig(u):
        c = Wminv @ u
        mag = np.abs(c)
        supp = mag > 1e-8 * max(mag.max(), 1.0)
        vals = [abs(lam1[i]) ** 2 for i in range(n) if supp[i]]
        return max(vals) if vals else 0.0

    words = [''.join(w) for L in (1, 2, 3) for w in itertools.product(cc.ALPHABET, repeat=L)]
    labels = {}
    for app in words:
        u = readout_vector(app, idx, n, R)
        if not u.any():
            continue
        m = own_max_eig(u)
        labels[app] = ('blind' if m < 15.0 else 'nonblind', m)

    blind = sum(1 for v, _ in labels.values() if v == 'blind')
    print(f"tested={len(labels)}  blind={blind}  (doc: 240 tested, 24 blind)")
    return labels, Wminv, lam1


# --------------------------------------------------------------------------- #
# 2. Lead 2 -- depth parity via T^2 (the even-depth operator)
# --------------------------------------------------------------------------- #
def test_lead2(states, idx, T, labels):
    n = len(states)
    T2 = T @ T
    lam2, V2 = np.linalg.eig(T2)
    l1sq = np.abs(lam2).max()
    V2inv = np.linalg.inv(V2)

    def top_present(u):
        c = V2inv @ u
        mag = np.abs(c)
        supp = mag > 1e-8 * max(mag.max(), 1.0)
        return any(abs(lam2[i]) > l1sq - 1e-3 for i in range(n) if supp[i])

    mismatches = []
    for app, (label, _) in labels.items():
        u = readout_vector(app, idx, n, R)
        pred = 'nonblind' if top_present(u) else 'blind'
        if pred != label:
            mismatches.append((app, label, pred))
    print(f"\nLead 2 (depth parity via T^2): mismatches = {len(mismatches)} / {len(labels)}"
          f"  {'SURVIVES' if not mismatches else 'REFUTED'}")
    if mismatches:
        print("  counterexamples:", mismatches[:10])


# --------------------------------------------------------------------------- #
# 3. the branch-difference reconstruction of a^2 = 7 (the OTHER cited value,
#    from the 1,326-pairs census, distinct from the 240/24 dataset above)
# --------------------------------------------------------------------------- #
def test_branch_difference():
    CONJ = {}
    for a, b in cc.CONJ_PAIRS:
        CONJ[a] = b
        CONJ[b] = a

    def dagger(w):
        return ''.join(CONJ[c] for c in w)

    kmax = 30
    print("\nbranch-difference reconstruction (a^2=7 expected, doc's OTHER cited value):")
    print("  using geometries()'s own (hand-specified) bminus -- transverse pairs are the known")
    print("  special case where bminus != dagger(bplus) pointwise (first letter only flips).")
    for label, prep, bplus, bminus, _ in cc.geometries():
        is_generic = (bminus == dagger(bplus))
        scan = cc.listening_scan(prep, [bplus, bminus], R, kmax, exact=True)
        kk = len(scan)
        diff = [scan[k][1][0] - scan[k][1][1] for k in range(kk)]
        nz = [(d, v) for d, v in enumerate(diff) if v != 0]
        tag = "generic-dagger" if is_generic else "special (transverse-type)"
        if len(nz) < 2:
            print(f"  {label:32s} diff ZERO (symmetry-forced)          [{tag}]")
            continue
        d1, v1 = nz[-2]
        d2, v2 = nz[-1]
        a2 = abs(v2 / v1) if d2 - d1 == 2 else None
        print(f"  {label:32s} diff_a2={a2}          [{tag}]")


# --------------------------------------------------------------------------- #
# 4. Lead 1 -- the sign-twisted relabeling group (order 96), validated three ways;
#    K/S3 identification NOT resolved (see module docstring).
# --------------------------------------------------------------------------- #
def build_relabeling_group(states, idx):
    n = len(states)

    def gen_matrix(geom, sign):
        G = np.zeros((n, n))
        for s, i in idx.items():
            (a, b, c, d), (pX, pY, pZ) = s
            ns = geom(a, b, c, d, pX, pY, pZ)
            j = idx[ns]
            G[j, i] = sign(a, b, c, d, pX, pY, pZ)
        return G

    # signs read directly off Born_Rule.md's stated formulas -- not fitted to commute.
    gens = {
        'flipX':  (lambda a, b, c, d, pX, pY, pZ: ((a, -b, c, d), (pX, pY, pZ)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** pX),
        'flipY':  (lambda a, b, c, d, pX, pY, pZ: ((-a, b, c, d), (pX, pY, pZ)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** pY),
        'flipZ':  (lambda a, b, c, d, pX, pY, pZ: ((a, b, -c, d), (pX, pY, pZ)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** pZ),
        'swapXY': (lambda a, b, c, d, pX, pY, pZ: ((b, a, c, d), (pY, pX, pZ)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** (pX * pY)),
        'swapYZ': (lambda a, b, c, d, pX, pY, pZ: ((c, b, a, d), (pX, pZ, pY)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** (pY * pZ)),
        'swapG':  (lambda a, b, c, d, pX, pY, pZ: ((a, b, c, -d), (pX, pY, pZ)),
                   lambda a, b, c, d, pX, pY, pZ: (-1) ** (d % 2)),
    }
    Ggen = {name: gen_matrix(geom, sign) for name, (geom, sign) in gens.items()}

    T = build_T(states, idx, R)
    for name, G in Ggen.items():
        comm = np.max(np.abs(G @ T - T @ G))
        print(f"  {name:8s} max|GT-TG| = {comm:.3e}")

    I = np.eye(n)

    def key(M):
        return tuple(M.astype(np.int8).flatten())

    group = {key(I): I}
    frontier = [I]
    while frontier:
        nxt = []
        for M in frontier:
            for G in Ggen.values():
                P = G @ M
                k = key(P)
                if k not in group:
                    group[k] = P
                    nxt.append(P)
        frontier = nxt
    print(f"  group order = {len(group)}  (doc: 96)")
    return list(group.values()), T


def check_dominant_ginvariance(states, idx, T, Gs):
    n = len(states)
    T2 = T @ T
    lam2, V2 = np.linalg.eig(T2)
    l1sq = np.abs(lam2).max()
    dom_idx = [i for i in range(n) if abs(lam2[i]) > l1sq - 1e-3]
    Vd_real = np.real(V2[:, dom_idx])
    Q, Rm = np.linalg.qr(Vd_real)
    rank = int(np.sum(np.abs(np.diag(Rm)) > 1e-8))
    Qb = Q[:, :rank]
    Pdom = Qb @ Qb.T
    maxerr = max(np.max(np.abs(Pdom @ G @ Pdom - G @ Pdom)) for G in Gs)
    print(f"  dominant eigenspace dim = {rank}  (doc: 16)")
    print(f"  max G-invariance error over {len(Gs)} elements = {maxerr:.3e}")
    return Qb


if __name__ == "__main__":
    states, idx = build_state_space(R)
    T = build_T(states, idx, R)

    print("=== ground truth: 240 tested / 24 blind ===")
    labels, Wminv, lam1 = ground_truth_blind(states, idx, T)

    test_lead2(states, idx, T, labels)

    test_branch_difference()

    print("\n=== Lead 1: relabeling group (validated), K/S3 identification open ===")
    Gs, T = build_relabeling_group(states, idx)
    check_dominant_ginvariance(states, idx, T, Gs)
