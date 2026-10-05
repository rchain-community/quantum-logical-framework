#!/usr/bin/env python3
"""
weyl_qutrit_derivation.py -- why colour is a Weyl qutrit (Carbon_Superconductivity.md sec 34; frozen in bd527c2).

Premises: (A) a colour line is a projective representation of the step group F_p^2; (B) it is covariant under
the transport group SL(2, p); (C) some twist acts non-trivially. K4.2 fails with (C) once (B) allows the phases
spin needs; the post-hoc repair (C*) is non-zero plaquette flux (sec 34a).

  K4.1  cocycle classes c_k(u, v) = zeta^{k B(u, v)} (B bilinear with alternating part the symplectic form):
        centre of the twisted group algebra = #{g : c(g, h) = c(h, g) for all h}. Centre 1 => the algebra is
        M_p(C), one irreducible representation of dimension p. Centre p^2 => p^2 characters.
  K4.2  characters chi_w that are SL(2, p)-invariant (chi_w(gv) = chi_w(v)): only w = 0 survives.
  K4.3  for k != 0, every g in SL(2, p) has V_g with V_g D(v) V_g^-1 = lambda_v D(gv) (solved explicitly).
  Control: p = 2 must give the Pauli qubit.

Exact arithmetic: Q(omega) for p = 3 (weyl_sl3.W), Q(i) for p = 2. Stdlib only.
Run:  python3 weyl_qutrit_derivation.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction as Fr

import weyl_sl3 as W3


# ---------------------------------------------------------------- Q(i) for the p = 2 control
class Gi:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = Fr(a), Fr(b)

    def __add__(s, o): return Gi(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Gi(s.a - o.a, s.b - o.b)
    def __neg__(s): return Gi(-s.a, -s.b)
    def __mul__(s, o): return Gi(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)
    def iszero(s): return s.a == 0 and s.b == 0

    def inv(s):
        n = s.a * s.a + s.b * s.b
        return Gi(s.a / n, -s.b / n)


def nullspace(rows, n, zero, one):
    rows = [r[:] for r in rows]
    piv, r = [], 0
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
    out = []
    for fc in free:
        sol = [zero] * n
        sol[fc] = one
        for i, pc in enumerate(piv):
            sol[pc] = -rows[i][fc]
        out.append(sol)
    return out


# ---------------------------------------------------------------- finite-field pieces
def vecs(p):
    return list(itertools.product(range(p), repeat=2))


def symp(u, v, p):
    return (u[0] * v[1] - u[1] * v[0]) % p


def sl2(p):
    return [M for M in itertools.product(range(p), repeat=4) if (M[0] * M[3] - M[1] * M[2]) % p == 1]


def act(M, v, p):
    return ((M[0] * v[0] + M[1] * v[1]) % p, (M[2] * v[0] + M[3] * v[1]) % p)


def B(u, v, p):
    """A bilinear 2-cocycle whose alternating part B(u,v) - B(v,u) is the symplectic form."""
    return (u[0] * v[1]) % p if p == 2 else symp(u, v, p)


def centre_dim(p, k):
    c = lambda g, h: (k * B(g, h, p)) % p
    return sum(1 for g in vecs(p) if all(c(g, h) == c(h, g) for h in vecs(p)))


def invariant_characters(p):
    """w with chi_w(gv) = chi_w(v) for all g in SL(2,p), v; chi_w(v) = zeta^{symp(w, v)} (all characters)."""
    G = sl2(p)
    return [w for w in vecs(p) if all(symp(w, act(g, v, p), p) == symp(w, v, p) for g in G for v in vecs(p))]


def minus_I_alone(p):
    mI = (p - 1, 0, 0, p - 1)
    return [w for w in vecs(p) if all(symp(w, act(mI, v, p), p) == symp(w, v, p) for v in vecs(p))]


# ---------------------------------------------------------------- K4.3: solve V_g
def solve_V3(g):
    """p = 3, symmetric Weyl displacements: V D(v) = D(gv) V for v = (1,0), (0,1)."""
    eqs = []
    for v in ((1, 0), (0, 1)):
        A, Bm = W3.D(v), W3.D(act(g, v, 3))
        for i in range(3):
            for j in range(3):
                row = [W3.ZERO] * 9
                for k in range(3):
                    row[3 * i + k] = row[3 * i + k] + A[k][j]
                    row[3 * k + j] = row[3 * k + j] - Bm[i][k]
                eqs.append(row)
    return len(nullspace(eqs, 9, W3.ZERO, W3.ONE))


def pauli(v):
    """p = 2 displacements: (1,0) -> X, (0,1) -> Z, (1,1) -> XZ, (0,0) -> I."""
    I0, I1 = Gi(0), Gi(1)
    X = [[I0, I1], [I1, I0]]
    Z = [[I1, I0], [I0, Gi(-1)]]
    Id = [[I1, I0], [I0, I1]]
    mm = lambda A, Bm: [[A[i][0] * Bm[0][j] + A[i][1] * Bm[1][j] for j in range(2)] for i in range(2)]
    R = Id
    if v[0]:
        R = mm(R, X)
    if v[1]:
        R = mm(R, Z)
    return R


def solve_V2(g):
    """p = 2: some phases lambda in {+-1, +-i} with V D(v) = lambda_v D(gv) V for both generators."""
    phases = [Gi(1), Gi(-1), Gi(0, 1), Gi(0, -1)]
    for l1, l2 in itertools.product(phases, repeat=2):
        eqs = []
        for v, lam in (((1, 0), l1), ((0, 1), l2)):
            A, Bm = pauli(v), pauli(act(g, v, 2))
            for i in range(2):
                for j in range(2):
                    row = [Gi(0)] * 4
                    for k in range(2):
                        row[2 * i + k] = row[2 * i + k] + A[k][j]
                        row[2 * k + j] = row[2 * k + j] - lam * Bm[i][k]
                    eqs.append(row)
        ns = nullspace(eqs, 4, Gi(0), Gi(1))
        for sol in ns:
            det = sol[0] * sol[3] - sol[1] * sol[2]
            if not det.iszero():
                return True
    return False


def solve_V2_exact(g):
    eqs = []
    for v in ((1, 0), (0, 1)):
        A, Bm = pauli(v), pauli(act(g, v, 2))
        for i in range(2):
            for j in range(2):
                row = [Gi(0)] * 4
                for k in range(2):
                    row[2 * i + k] = row[2 * i + k] + A[k][j]
                    row[2 * k + j] = row[2 * k + j] - Bm[i][k]
                eqs.append(row)
    return any(not (s[0] * s[3] - s[1] * s[2]).iszero() for s in nullspace(eqs, 4, Gi(0), Gi(1)))


def main():
    for p in (3, 2):
        label = "colour, p = 3" if p == 3 else "control (spin), p = 2"
        print("=" * 78 + f"\n{label}\n" + "-" * 78)
        for k in range(p):
            cd = centre_dim(p, k)
            kind = f"{p * p} characters (dimension 1)" if cd == p * p else \
                (f"simple: M_{p}(C), one irreducible representation of dimension {p}" if cd == 1 else "other")
            print(f"K4.1  class k = {k}: centre dimension {cd} -> {kind}")
        inv = invariant_characters(p)
        print(f"K4.2  SL(2,{p})-invariant characters: {inv}"
              f"{'  (-I alone already forces w = 0: ' + str(minus_I_alone(p)) + ')' if p == 3 else ''}")
        G = sl2(p)
        ok = [solve_V3(g) == 1 for g in G] if p == 3 else [solve_V2(g) for g in G]
        print(f"K4.3  covariant V_g found for {sum(ok)} of {len(G)} elements of SL(2,{p})"
              f"{' (unique up to scalar each)' if p == 3 else ''}")
        if p == 2:
            ex = sum(1 for g in G if solve_V2_exact(g))
            print(f"      phase-free covariance for spin: {ex} of {len(G)} -- spin needs phases, so (B) must allow them")
        print("K4.2' with phases allowed (the standard spin needs), every character is covariant:"
              " chi_w(v) = lambda_v chi_w(gv) with lambda = chi_w / (chi_w o g), itself a character")
        flux = {k: any((k * (B(u, v, p) - B(v, u, p))) % p for u in vecs(p) for v in vecs(p)) for k in range(p)}
        print(f"(C*)  nonzero plaquette flux (non-abelian transport) by class: {flux} -> only k != 0 survives")
        print(f"=>    under (A)+(B)+(C*), the irreducible line has dimension {p}"
              f" {'(three colours)' if p == 3 else '(the Pauli qubit)'}\n")


if __name__ == "__main__":
    main()
