#!/usr/bin/env python3
"""
colour_flux.py -- the colour flux from the axis cycle as a transport primitive
(Carbon_Superconductivity.md sec 27; construction and failure points frozen in commit 423256b).

  K1/F1  Q8 (one unit-determinant fold per twist) plus U = (1 - i(sx+sy+sz))/2 generates a group T;
         check |T| = 24 and find every isomorphism T -> SL(2, F3), each tested on all 576 products.
  K3/F2  for each isomorphism phi and each v0 on a line fixed by phi(U): t -> phi(q_t) v0 must be a bijection
         from the 8 twists onto the 8 nonzero vectors of F3^2, with reversal -> -v, gauge on the U-fixed line,
         and phi(U) cycling the x, y, z lines as cycTwist does.
  F3     canonicity: every (phi, v0) must give the same flux table up to one global omega <-> omega-bar.
  K5/F4  the flux: explicit 3x3 Weyl displacements over Z[omega]; the plaquette commutator is a scalar omega^k.
  P2     gauge-spatial plaquettes for colour (versus spin, where +-I commutes).
  P3     colour census of ZFA closures (count-balanced words) at lengths 2..8, by scalar colour phase.

Exact arithmetic throughout (Gaussian rationals, F3, Z[omega]). Stdlib only.
Run:  python3 colour_flux.py
"""
from __future__ import annotations

import itertools
from collections import defaultdict
from fractions import Fraction as Fr

from twist_core import pauli_fold

# ---------------------------------------------------------------- Gaussian-rational 2x2 matrices
# A number is (re, im) of Fractions; a matrix is a 4-tuple (a, b, c, d) = [[a, b], [c, d]].
Z0, Z1 = (Fr(0), Fr(0)), (Fr(1), Fr(0))


def cm(x, y):
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def ca(x, y):
    return (x[0] + y[0], x[1] + y[1])


def mm(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (ca(cm(a, e), cm(b, g)), ca(cm(a, f), cm(b, h)), ca(cm(c, e), cm(d, g)), ca(cm(c, f), cm(d, h)))


def sc(s, A):
    return tuple(cm(s, x) for x in A)


I2 = (Z1, Z0, Z0, Z1)
I_ = (Fr(0), Fr(1))
SX = (Z0, Z1, Z1, Z0)
SY = (Z0, (Fr(0), Fr(-1)), (Fr(0), Fr(1)), Z0)
SZ = (Z1, Z0, Z0, (Fr(-1), Fr(0)))
NEG = (Fr(-1), Fr(0))
HALF = (Fr(1, 2), Fr(0))

# Unit-determinant folds, one per twist (twist_core: ^ = +sy, > = +sx, / = +sz, + = +I; reversal = minus).
Q = {'+': I2, '-': sc(NEG, I2),
     '>': sc(I_, SX), '<': sc(NEG, sc(I_, SX)),
     '^': sc(I_, SY), 'v': sc(NEG, sc(I_, SY)),
     '/': sc(I_, SZ), '\\': sc(NEG, sc(I_, SZ))}
REV = {'+': '-', '-': '+', '>': '<', '<': '>', '^': 'v', 'v': '^', '/': '\\', '\\': '/'}
CYC = {'>': '^', '<': 'v', '^': '/', 'v': '\\', '/': '>', '\\': '<', '+': '+', '-': '-'}   # Lean cycTwist
AXIS = {'>': 'x', '<': 'x', '^': 'y', 'v': 'y', '/': 'z', '\\': 'z', '+': 'g', '-': 'g'}
POS = {'x': '>', 'y': '^', 'z': '/', 'g': '+'}

# U = (1 - i(sx + sy + sz))/2
_S = tuple(ca(ca(a, b), c) for a, b, c in zip(SX, SY, SZ))
U = sc(HALF, tuple(ca(e, cm((Fr(0), Fr(-1)), s)) for e, s in zip(I2, _S)))


def generate(gens):
    seen = {I2: ()}
    frontier = [I2]
    while frontier:
        nxt = []
        for g in frontier:
            for k, h in enumerate(gens):
                p = mm(g, h)
                if p not in seen:
                    seen[p] = seen[g] + (k,)
                    nxt.append(p)
        frontier = nxt
    return seen   # element -> a word in the generators


# ---------------------------------------------------------------- SL(2, F3)
def fm(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return ((a * e + b * g) % 3, (a * f + b * h) % 3, (c * e + d * g) % 3, (c * f + d * h) % 3)


SL23 = [M for M in itertools.product(range(3), repeat=4) if (M[0] * M[3] - M[1] * M[2]) % 3 == 1]
FI = (1, 0, 0, 1)


def fv(M, v):
    return ((M[0] * v[0] + M[1] * v[1]) % 3, (M[2] * v[0] + M[3] * v[1]) % 3)


def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0]) % 3


NONZERO = [v for v in itertools.product(range(3), repeat=2) if v != (0, 0)]


def isomorphisms(T, gens):
    """All isomorphisms T -> SL(2,3), by assigning images to the generators and checking every product."""
    words = generate(gens)
    elems = list(words)
    found = []
    for imgs in itertools.product(SL23, repeat=len(gens)):
        phi = {}
        for g, w in words.items():
            M = FI
            for k in w:
                M = fm(M, imgs[k])
            phi[g] = M
        if len(set(phi.values())) != len(elems):
            continue
        if all(phi[mm(a, b)] == fm(phi[a], phi[b]) for a in elems for b in elems):
            found.append(phi)
    return found


# ---------------------------------------------------------------- Z[omega] and 3x3 Weyl displacements
# a + b*omega with omega^2 = -1 - omega.
def wm(x, y):
    a, b = x
    c, d = y
    return (a * c - b * d, a * d + b * c - b * d)


def wa(x, y):
    return (x[0] + y[0], x[1] + y[1])


W0, W1, OM = (0, 0), (1, 0), (0, 1)
OMP = [W1, OM, wm(OM, OM)]     # omega^0, omega^1, omega^2


def m3(A, B):
    return tuple(tuple(
        (lambda acc: acc)(
            sum_w([wm(A[i][k], B[k][j]) for k in range(3)])) for j in range(3)) for i in range(3))


def sum_w(xs):
    s = W0
    for x in xs:
        s = wa(s, x)
    return s


X3 = tuple(tuple(W1 if i == (j + 1) % 3 else W0 for j in range(3)) for i in range(3))      # X|j> = |j+1>
Z3 = tuple(tuple(OMP[i] if i == j else W0 for j in range(3)) for i in range(3))            # Z|j> = omega^j |j>
ID3 = tuple(tuple(W1 if i == j else W0 for j in range(3)) for i in range(3))


def mpow(A, n):
    R = ID3
    for _ in range(n % 3):
        R = m3(R, A)
    return R


def D(v):
    """Weyl displacement D(p,q) = omega^{2pq} X^p Z^q (2 = 1/2 mod 3), the symmetric choice: D(-v) = D(v)^-1."""
    M = m3(mpow(X3, v[0]), mpow(Z3, v[1]))
    w = OMP[(2 * v[0] * v[1]) % 3]
    return tuple(tuple(wm(w, x) for x in row) for row in M)


def cocycle():
    """c(u, v) with D(u) D(v) = omega^c D(u+v), read off the explicit matrices."""
    c = {}
    for u in itertools.product(range(3), repeat=2):
        for v in itertools.product(range(3), repeat=2):
            P = m3(D(u), D(v))
            S = D(((u[0] + v[0]) % 3, (u[1] + v[1]) % 3))
            for k in range(3):
                if P == tuple(tuple(wm(OMP[k], x) for x in row) for row in S):
                    c[(u, v)] = k
            assert (u, v) in c
    return c


def scalar_phase(M):
    """Return k if M = omega^k I, else None."""
    for k in range(3):
        if M == tuple(tuple(OMP[k] if i == j else W0 for j in range(3)) for i in range(3)):
            return k
    return None


# ---------------------------------------------------------------- run
def rule(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def main():
    rule("K1/F1  the transport group T = <Q8, U>")
    T = generate([Q['>'], U])
    q8 = generate([Q['>'], Q['^']])
    assert set(Q.values()) == set(q8), "the eight twists are exactly Q8"
    print(f"|Q8| = {len(q8)} (the eight twist folds), |T| = {len(T)}")
    assert len(T) == 24
    Uinv = [g for g in T if mm(U, g) == I2][0]
    for t in Q:
        assert mm(mm(U, Q[t]), Uinv) == Q[CYC[t]], t
    print("U q_t U^-1 = q_{cycTwist t} for all eight twists")
    isos = isomorphisms(T, [Q['>'], U])
    print(f"isomorphisms T -> SL(2,F3), each checked on all {len(T) ** 2} products: {len(isos)}")
    assert isos, "F1 FAILS"

    rule("K3/F2  twists as vectors; F3 canonicity over every (phi, v0)")
    tables = set()
    n_cases = 0
    for phi in isos:
        PU = phi[U]
        fixed = [v for v in NONZERO if fv(PU, v) in (v, ((-v[0]) % 3, (-v[1]) % 3))]
        for v0 in fixed:
            vec = {t: fv(phi[Q[t]], v0) for t in Q}
            assert sorted(vec.values()) == sorted(NONZERO), "F2: not a bijection"
            for t in Q:
                assert vec[REV[t]] == ((-vec[t][0]) % 3, (-vec[t][1]) % 3), "F2: reversal"
                lam = [l for l in (1, 2) if fv(PU, vec[t]) == ((l * vec[CYC[t]][0]) % 3, (l * vec[CYC[t]][1]) % 3)]
                assert lam, "F2: U does not follow cycTwist"
            assert vec['+'] in (v0, ((-v0[0]) % 3, (-v0[1]) % 3)), "F2: gauge not on the U-fixed line"
            tab = tuple(symp(vec[POS[a]], vec[POS[b]]) for a, b in
                        (('x', 'y'), ('y', 'z'), ('z', 'x'), ('g', 'x'), ('g', 'y'), ('g', 'z')))
            tables.add(tab)
            n_cases += 1
    print(f"(phi, v0) cases: {n_cases}; each line fixed by phi(U): {len(fixed)} vectors")
    print("symplectic tables <v_a, v_b> for (xy, yz, zx, gx, gy, gz):", sorted(tables))
    neg = lambda t: tuple((-k) % 3 for k in t)
    canonical = all(t in tables or neg(t) in tables for t in tables) and len({min(t, neg(t)) for t in tables}) == 1
    uniform = all(len(set(t)) == 1 and t[0] != 0 for t in tables)
    print(f"F3 canonical up to omega <-> omega-bar: {canonical};  F4 every pair nonzero, one orientation: {uniform}")
    assert canonical and uniform

    rule("K5/F4/P2  the flux from explicit Weyl displacements")
    phi, = isos[:1]
    v0 = [v for v in NONZERO if fv(phi[U], v) in (v, ((-v[0]) % 3, (-v[1]) % 3))][0]
    vec = {t: fv(phi[Q[t]], v0) for t in Q}
    for a, b in (('x', 'y'), ('y', 'z'), ('z', 'x'), ('g', 'x'), ('g', 'y'), ('g', 'z')):
        ta, tb = POS[a], POS[b]
        H = m3(m3(D(vec[ta]), D(vec[tb])), m3(D(vec[REV[ta]]), D(vec[REV[tb]])))
        k = scalar_phase(H)
        f = pauli_fold(ta + tb + REV[ta] + REV[tb])     # QLF's own fold of the plaquette word
        spin_s = '+1' if f == (1, 0, 0, 1) else ('-1' if f == (-1, 0, 0, -1) else str(f))
        print(f"plaquette {a}{b}: colour holonomy omega^{k}  (flux {120 * k if k != 2 else -120} deg);"
              f"  spin {spin_s}")
    for v in NONZERO:
        assert m3(D(v), D(((-v[0]) % 3, (-v[1]) % 3))) == ID3, "D(-v) != D(v)^-1"
    print("D(-v) = D(v)^-1 for every v, so the plaquette word is the group commutator.")
    for u in NONZERO:
        for v in NONZERO:
            H = m3(m3(D(u), D(v)), m3(D(((-u[0]) % 3, (-u[1]) % 3)), D(((-v[0]) % 3, (-v[1]) % 3))))
            assert scalar_phase(H) == (-symp(u, v)) % 3
    print("for all u, v: D(u) D(v) D(u)^-1 D(v)^-1 = omega^{-<u,v>} (exact, all 64 pairs).")

    rule("P3  colour census of ZFA closures (count-balanced words)")
    order = list(Q)
    disp = {'>': (1, 0, 0, 0), '<': (-1, 0, 0, 0), '^': (0, 1, 0, 0), 'v': (0, -1, 0, 0),
            '/': (0, 0, 1, 0), '\\': (0, 0, -1, 0), '+': (0, 0, 0, 1), '-': (0, 0, 0, -1)}
    C = cocycle()   # D(u) D(v) = omega^{C[u,v]} D(u+v)
    # State: (Z^4 position, F3^2 displacement, phase exponent).
    state = {((0, 0, 0, 0), (0, 0), 0): 1}
    print("  L   closures   omega^0   omega^1   omega^2   neutral fraction")
    for L in range(1, 9):
        new = defaultdict(int)
        for (x, u, k), n in state.items():
            for t in order:
                v = vec[t]
                x2 = tuple(a + b for a, b in zip(x, disp[t]))
                if sum(abs(c) for c in x2) > 8 - L:
                    continue
                u2 = ((u[0] + v[0]) % 3, (u[1] + v[1]) % 3)
                k2 = (k + C[(u, v)]) % 3
                new[(x2, u2, k2)] += n
        state = new
        if L % 2 == 0:
            by = [0, 0, 0]
            for (x, u, k), n in state.items():
                if x == (0, 0, 0, 0):
                    assert u == (0, 0)
                    by[k] += n
            tot = sum(by)
            print(f"  {L}   {tot:8d}  {by[0]:8d}  {by[1]:8d}  {by[2]:8d}   {by[0] / tot:.4f}")
            assert by[1] == by[2], "P3 mirror check fails"
    print("omega and omega-bar counts equal at every length (mirror check).")


if __name__ == "__main__":
    main()
