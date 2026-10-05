#!/usr/bin/env python3
"""
weyl_sl3.py -- the eight twists as the Weyl basis of sl(3) (Carbon_Superconductivity.md sec 28;
questions frozen in commit fe0389e).

  W1  the eight D(v_t) are traceless and Hilbert-Schmidt orthogonal: a basis of sl(3).
  W2  each axis (a twist and its reverse) spans a Cartan subalgebra, and the four axes are orthogonal under the
      trace form: sl(3) = h_g + h_x + h_y + h_z.
  W3  the bracket table: [D(u), D(v)] = c D(u+v), nonzero iff the axes differ; which axes land where.
  W4  is the sec-27 colour cycle (any Clifford unitary D(w)V that relabels the twist axes as cycTwist does)
      conjugate, up to phase, to QLF_StrongAlgebra's axis permutation P? Invariants: eigenvalue pattern
      (distinct iff trace 0, since A^3 is scalar) and the dimension of sl(3) fixed by conjugation.
  W5  the 't Hooft twist n_mn = <v_m, v_n> and its Pfaffian mod 3 (cannot fail; recorded).

Exact arithmetic in Q(omega). The twist vectors are the ones in lean/QLF_ColourFlux.lean.
Run:  python3 weyl_sl3.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction as Fr

# ---------------------------------------------------------------- Q(omega): a + b omega, omega^2 = -1 - omega
class W:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(s, o): return W(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return W(s.a - o.a, s.b - o.b)
    def __neg__(s): return W(-s.a, -s.b)
    def __mul__(s, o): return W(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a - s.b * o.b)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def conj(s): return W(s.a - s.b, -s.b)                     # omega -> omega^2
    def iszero(s): return s.a == 0 and s.b == 0

    def inv(s):
        n = s.a * s.a - s.a * s.b + s.b * s.b
        c = s.conj()
        return W(c.a / n, c.b / n)

    def __repr__(s):
        names = {(1, 0): "1", (0, 1): "w", (-1, -1): "w2", (-1, 0): "-1", (0, -1): "-w", (1, 1): "-w2",
                 (0, 0): "0"}
        return names.get((s.a, s.b), f"({s.a}{'+' if s.b >= 0 else ''}{s.b}w)")


ZERO, ONE, OM = W(0), W(1), W(0, 1)
OMP = [ONE, OM, OM * OM]


def mat(f):
    return [[f(i, j) for j in range(3)] for i in range(3)]


def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(3)), ZERO) for j in range(3)] for i in range(3)]


def madd(A, B, s=1):
    return [[A[i][j] + (B[i][j] if s == 1 else -B[i][j]) for j in range(3)] for i in range(3)]


def msc(c, A):
    return [[c * x for x in r] for r in A]


def tr(A):
    return A[0][0] + A[1][1] + A[2][2]


def dag(A):
    return [[A[j][i].conj() for j in range(3)] for i in range(3)]


def meq(A, B):
    return all(A[i][j] == B[i][j] for i in range(3) for j in range(3))


I3 = mat(lambda i, j: ONE if i == j else ZERO)
X = mat(lambda i, j: ONE if i == (j + 1) % 3 else ZERO)
Z = mat(lambda i, j: OMP[i] if i == j else ZERO)


def mpow(A, n):
    R = I3
    for _ in range(n % 3):
        R = mm(R, A)
    return R


def D(v):
    """Symmetric Weyl displacement omega^{2pq} X^p Z^q (as in colour_flux.py)."""
    return msc(OMP[(2 * v[0] * v[1]) % 3], mm(mpow(X, v[0]), mpow(Z, v[1])))


def neg(v):
    return ((-v[0]) % 3, (-v[1]) % 3)


def add(u, v):
    return ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3)


def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0]) % 3


# twist vectors from QLF_ColourFlux.colVec
VEC = {'+': (1, 0), '-': (2, 0), '>': (0, 1), '<': (0, 2), '^': (2, 1), 'v': (1, 2), '/': (1, 1), '\\': (2, 2)}
AXIS = {'+': 'g', '-': 'g', '>': 'x', '<': 'x', '^': 'y', 'v': 'y', '/': 'z', '\\': 'z'}
CYC = {'>': '^', '<': 'v', '^': '/', 'v': '\\', '/': '>', '\\': '<', '+': '+', '-': '-'}
TW = list(VEC)
M = (1, 2, 0, 1)                         # the cycle in SL(2,3), QLF_ColourFlux.cycM


def Mv(v):
    return ((M[0] * v[0] + M[1] * v[1]) % 3, (M[2] * v[0] + M[3] * v[1]) % 3)


def coeff_on(A, v):
    """Coefficient of D(v) in A: tr(D(v)^dag A)/3."""
    t = tr(mm(dag(D(v)), A))
    return W(t.a / 3, t.b / 3)


# ---------------------------------------------------------------- linear algebra over Q(omega)
def nullspace(rows, n):
    rows = [r[:] for r in rows]
    piv = []
    r = 0
    for c in range(n):
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
        piv.append(c)
        r += 1
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        sol = [ZERO] * n
        sol[fc] = ONE
        for i, pc in enumerate(piv):
            sol[pc] = -rows[i][fc]
        basis.append(sol)
    return basis


def clifford_V():
    """Solve V D(v) = D(Mv) V for v = (1,0), (0,1): nine unknowns, the entries of V."""
    eqs = []
    for v in ((1, 0), (0, 1)):
        A, B = D(v), D(Mv(v))
        for i in range(3):
            for j in range(3):
                row = [ZERO] * 9
                for k in range(3):
                    row[3 * i + k] = row[3 * i + k] + A[k][j]          # (V A)_ij = sum_k V_ik A_kj
                    row[3 * k + j] = row[3 * k + j] - B[i][k]          # (B V)_ij = sum_k B_ik V_kj
                eqs.append(row)
    ns = nullspace(eqs, 9)
    assert len(ns) == 1, f"Clifford V not unique up to scalar: {len(ns)}"
    s = ns[0]
    return [[s[3 * i + j] for j in range(3)] for i in range(3)]


def inv3(A):
    """Inverse via adjugate."""
    def m(i, j):
        r = [x for x in range(3) if x != i]
        c = [x for x in range(3) if x != j]
        return A[r[0]][c[0]] * A[r[1]][c[1]] - A[r[0]][c[1]] * A[r[1]][c[0]]
    det = sum(((A[0][j] * m(0, j)) if j % 2 == 0 else -(A[0][j] * m(0, j)) for j in range(3)), ZERO)
    di = det.inv()
    return [[(m(j, i) if (i + j) % 2 == 0 else -m(j, i)) * di for j in range(3)] for i in range(3)]


def ad_fixed_dim(A):
    """Dimension of sl(3) fixed by X -> A X A^-1, from the 8x8 matrix in the Weyl basis."""
    Ai = inv3(A)
    basis = [v for v in itertools.product(range(3), repeat=2) if v != (0, 0)]
    cols = []
    for v in basis:
        img = mm(mm(A, D(v)), Ai)
        cols.append([coeff_on(img, u) for u in basis])
    rows = [[cols[j][i] - (ONE if i == j else ZERO) for j in range(8)] for i in range(8)]
    return len(nullspace(rows, 8))


def rule(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def main():
    rule("W1  the eight twists as a basis of sl(3)")
    ok_tr = all(tr(D(VEC[t])).iszero() for t in TW)
    gram = [[tr(mm(dag(D(VEC[s])), D(VEC[t]))) for t in TW] for s in TW]
    ok_hs = all(gram[i][j] == (W(3) if i == j else ZERO) for i in range(8) for j in range(8))
    print(f"traceless: {ok_tr};  Hilbert-Schmidt Gram = 3 I: {ok_hs}  ->  basis of sl(3) (dim 8)")
    assert ok_tr and ok_hs

    rule("W2  the four axes as orthogonal Cartan subalgebras")
    for ax, (p, n) in {'g': '+-', 'x': '><', 'y': '^v', 'z': '/\\'}.items():
        A, B = D(VEC[p]), D(VEC[n])
        comm = madd(mm(A, B), mm(B, A), -1)
        print(f"h_{ax} = span(D({p}), D({n})): commute {all(x.iszero() for r in comm for x in r)}")
    form = {(s, t): tr(mm(D(VEC[s]), D(VEC[t]))) for s in TW for t in TW}
    orth = all(form[(s, t)].iszero() for s in TW for t in TW if AXIS[s] != AXIS[t])
    nondeg = all(not form[(s, t)].iszero() for s in TW for t in TW if VEC[t] == neg(VEC[s]))
    print(f"trace form zero between different axes: {orth};  nondegenerate within each axis: {nondeg}")
    # Cartan: maximal abelian (dim 2 = rank) of semisimple elements; centraliser of a generic element is itself
    for ax, (p, n) in {'g': '+-', 'x': '><', 'y': '^v', 'z': '/\\'}.items():
        A = madd(D(VEC[p]), msc(W(2), D(VEC[n])))
        cent = [t for t in TW if all(x.iszero() for r in madd(mm(A, D(VEC[t])), mm(D(VEC[t]), A), -1) for x in r)]
        print(f"  centraliser of D({p}) + 2D({n}) among the twists: {cent}")
    assert orth and nondeg

    rule("W3  brackets: [D(u), D(v)] = c D(u+v)")
    print("      " + "  ".join(f"{t:>9}" for t in TW))
    for s in TW:
        cells = []
        for t in TW:
            C = madd(mm(D(VEC[s]), D(VEC[t])), mm(D(VEC[t]), D(VEC[s])), -1)
            if all(x.iszero() for r in C for x in r):
                cells.append("0")
            else:
                tgt = add(VEC[s], VEC[t])
                tw = [u for u in TW if VEC[u] == tgt][0]
                c = coeff_on(C, tgt)
                assert meq(C, msc(c, D(tgt)))
                cells.append(f"{c}·{tw}")
        print(f"{s:>4}  " + "  ".join(f"{c:>9}" for c in cells))
    land = {}
    for s in TW:
        for t in TW:
            if AXIS[s] != AXIS[t]:
                tgt = [u for u in TW if VEC[u] == add(VEC[s], VEC[t])][0]
                land.setdefault(frozenset((AXIS[s], AXIS[t])), set()).add(AXIS[tgt])
    for k, v in sorted(land.items(), key=lambda kv: sorted(kv[0])):
        print(f"  [h_{'h_'.join(sorted(k)) if False else ''}{'·'.join(sorted(k))}] lands in axes {sorted(v)}")

    rule("W4  the sec-27 colour cycle versus QLF_StrongAlgebra's axis permutation P")
    V = clifford_V()
    for t in TW:
        assert meq(mm(mm(V, D(VEC[t])), inv3(V)), D(VEC[CYC[t]])), t
    print("Clifford V found (unique up to scalar); V D(v_t) V^-1 = D(v_cycTwist t) exactly, all eight twists.")
    P = mat(lambda i, j: ONE if i == (j + 1) % 3 else ZERO)
    print(f"P (axis permutation): trace {tr(P)};  sl(3) fixed by conjugation: dim {ad_fixed_dim(P)}")
    results = []
    for w in itertools.product(range(3), repeat=2):
        A = mm(D(w), V)
        A3 = mm(mm(A, A), A)
        scalar = all(A3[i][j].iszero() for i in range(3) for j in range(3) if i != j) and \
            A3[0][0] == A3[1][1] == A3[2][2]
        # relabels axes as cycTwist, up to colour phase:
        relabel = all(meq(mm(mm(A, D(VEC[t])), inv3(A)), msc(coeff_on(mm(mm(A, D(VEC[t])), inv3(A)), VEC[CYC[t]]),
                                                             D(VEC[CYC[t]]))) for t in TW)
        fd = ad_fixed_dim(A)
        distinct = tr(A).iszero()
        results.append((w, distinct, fd))
        print(f"  w = {w}:  A^3 scalar {scalar};  relabels as cycTwist {relabel};  trace {tr(A)!r:>10};"
              f"  eigenvalues distinct {distinct};  fixed dim {fd}")
    match = [w for w, d, fd in results if d and fd == 2]
    print(f"phase choices conjugate to P (distinct eigenvalues and fixed dim 2): {match}")
    exact = [r for r in results if r[0] == (0, 0)][0]
    print(f"exact V (w = 0): distinct {exact[1]}, fixed dim {exact[2]}")

    rule("W5  't Hooft twist n = <v_m, v_n> on (g, x, y, z) and its Pfaffian mod 3")
    ax = ['+', '>', '^', '/']
    n = [[symp(VEC[a], VEC[b]) for b in ax] for a in ax]
    for name, r in zip("gxyz", n):
        print(f"  {name}: {r}")
    pf = (n[0][1] * n[2][3] + n[0][2] * n[3][1] + n[0][3] * n[1][2]) % 3
    print(f"Pfaffian kappa = n_gx n_yz + n_gy n_zx + n_gz n_xy = {pf} (mod 3)")


if __name__ == "__main__":
    main()
