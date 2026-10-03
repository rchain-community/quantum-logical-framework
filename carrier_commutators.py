#!/usr/bin/env python3
"""
carrier_commutators.py -- colour carriers as commutators vs products (Carbon_Superconductivity.md sec 32;
frozen in commit 47e3949).

  R_prod  span of D(t)D(u) over the spatial twists (sec-31 rule extended to all two-twist products)
  R_comm  span of [D(t), D(u)]; the spin (Pauli-fold vector/scalar) of each nonzero commutator
  CF      colour factors implied: su(3) C_F = 4/3, u(3) C_F = 3/2 (T_F = 1/2), C_A = 3 for both
  PN      exploratory: the colour cycle on F2^2 versus the Singer cycle of F4; distinct-pair counts C(2^p, 2)

Exact arithmetic in Q(omega) (weyl_sl3.py). Stdlib only.
Run:  python3 carrier_commutators.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction as Fr
from math import comb

import weyl_sl3 as W
from twist_core import pauli_fold

SPATIAL = ['>', '<', '^', 'v', '/', '\\']
AX = {'>': 'x', '<': 'x', '^': 'y', 'v': 'y', '/': 'z', '\\': 'z'}


def flat(A):
    return [A[i][j] for i in range(3) for j in range(3)]


def rank(vectors):
    rows = [v[:] for v in vectors]
    r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        p = next((i for i in range(r, len(rows)) if not rows[i][c].iszero()), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        iv = rows[r][c].inv()
        rows[r] = [x * iv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and not rows[i][c].iszero():
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def casimir_F(gens):
    """C_F from an orthonormal-in-trace generator set (tr T^a T^b = delta/2): sum_a T^a T^a = C_F I."""
    S = [[W.ZERO] * 3 for _ in range(3)]
    for T in gens:
        S = W.madd(S, W.mm(T, T))
    return S[0][0]


def main():
    D = {t: W.D(W.VEC[t]) for t in SPATIAL}
    prods = [flat(W.mm(D[t], D[u])) for t, u in itertools.product(SPATIAL, repeat=2)]
    comms = []
    spins = []
    for t, u in itertools.product(SPATIAL, repeat=2):
        C = W.madd(W.mm(D[t], D[u]), W.mm(D[u], D[t]), -1)
        if all(x.iszero() for x in flat(C)):
            continue
        comms.append(flat(C))
        a, b, c, d = pauli_fold(t + u)
        spins.append('vector' if (abs(b) > 1e-12 or abs(c) > 1e-12 or abs(a - d) > 1e-12) else 'scalar')
    print("R_prod: span of D(t)D(u), 36 products:", rank(prods), "(9 = gl(3), contains the identity:",
          rank(prods + [flat(W.I3)]) == rank(prods), ")")
    print(f"R_comm: nonzero commutators {len(comms)}; span {rank(comms)} (8 = sl(3)); contains identity:",
          rank(comms + [flat(W.I3)]) == rank(comms))
    print(f"        every nonzero commutator is a cross-axis pair with a vector fold: "
          f"{all(s == 'vector' for s in spins)}  (identical and same-axis pairs give 0)")

    # Colour factors with T_F = 1/2 normalisation: su(3) generators, then add the u(1) singlet I/sqrt(6).
    # sum over an orthonormal basis of sl(3) (tr = 1/2): use C_F = (N^2-1)/(2N), u(N): N/2. Check numerically
    # with the Weyl basis: T_v = D(v)/sqrt(6) is not Hermitian, but sum_v D(v) D(v)^dag / 6 gives the same Casimir.
    S = [[W.ZERO] * 3 for _ in range(3)]
    for v in itertools.product(range(3), repeat=2):
        if v == (0, 0):
            continue
        S = W.madd(S, W.mm(W.D(v), W.dag(W.D(v))))
    cf_su3 = Fr(S[0][0].a, 6)
    cf_u3 = cf_su3 + Fr(1, 6)            # + (I/sqrt6)^2
    print(f"\nC_F(su(3)) = {cf_su3}, C_F(u(3)) = {cf_u3}; C_A = 3 for both;"
          f"  C_A/C_F: R_comm {Fr(3) / cf_su3}, R_prod {Fr(3) / cf_u3}")
    assert cf_su3 == Fr(4, 3) and cf_u3 == Fr(3, 2)

    print("\nPN (exploratory)")
    # Pauli classes mod phase as F2^2: X=(1,0), Z=(0,1), Y=(1,1). The colour cycle maps x -> y -> z.
    pv = {'x': (1, 0), 'y': (1, 1), 'z': (0, 1)}
    # Find the F2-linear map M with M(x)=y, M(y)=z, M(z)=x.
    for m in itertools.product(range(2), repeat=4):
        f = lambda v: ((m[0] * v[0] + m[1] * v[1]) % 2, (m[2] * v[0] + m[3] * v[1]) % 2)
        if f(pv['x']) == pv['y'] and f(pv['y']) == pv['z'] and f(pv['z']) == pv['x']:
            M = m
    tr, det = (M[0] + M[3]) % 2, (M[0] * M[3] - M[1] * M[2]) % 2
    print(f"  colour cycle on F2^2 = {M}; characteristic polynomial x^2 + {tr}x + {det}"
          f" -> x^2 + x + 1 (minimal polynomial of a primitive element of F4): {tr == 1 and det == 1}")
    print("  so the colour Z3 on the three axes is F4* (Singer cycle), order 2^2 - 1 = 3, a Mersenne prime.")
    for p in (1, 2, 3, 5):
        n = 2 ** p
        print(f"  alphabet 2^{p} = {n}: distinct unordered pairs C({n},2) = {comb(n, 2)};"
              f" 2^p - 1 = {n - 1} prime: {all((n - 1) % k for k in range(2, n - 1)) and n - 1 > 1};"
              f" perfect: {sum(d for d in range(1, comb(n, 2)) if comb(n, 2) % d == 0) == comb(n, 2)}")


if __name__ == "__main__":
    main()
