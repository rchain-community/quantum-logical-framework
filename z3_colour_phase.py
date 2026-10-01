#!/usr/bin/env python3
"""
z3_colour_phase.py -- a Z3 phase for colour (Carbon_Superconductivity.md sec 23, frozen in a3f21e4).

  D1  the element cycling the three spatial axes, U = (1 - i(sx + sy + sz))/2: U sx U^+ = sy, U sy U^+ = sz,
      U sz U^+ = sx, U^3 = -I, eigenphases e^(+-i pi/3); a Clifford element, not a twist fold.
  D2  qutrit clock Z = diag(1, w, w^2) and shift X (cycling the axes): ZX = w XZ; plaquette X Z X^-1 Z^-1 = w^+-1 I.
  T   the signed Z3 census: Z3 flows with amplitude w^(enclosed flux) x^|C|, flux 2 pi/3 per plaquette in the gauge
      w^(n * column) on vertical edges; exact transfer matrices on L x 3L tori, L = 3-6; |R3| = |Z(x-flux 1)/Z(0)|.

Run:  python3 z3_colour_phase.py        (D1, D2 always; T needs numpy)
"""
from __future__ import annotations

import cmath
import math

OM = cmath.exp(2j * math.pi / 3)


def mm(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def dag(A):
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A))]


def close(A, B, tol=1e-12):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(len(A)) for j in range(len(A)))


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def d1():
    rule("D1  THE AXIS-CYCLING ELEMENT (rotation by 2 pi/3 about (1,1,1))")
    sx = [[0, 1], [1, 0]]
    sy = [[0, -1j], [1j, 0]]
    sz = [[1, 0], [0, -1]]
    U = [[(1 - 1j) / 2, (-1j - 1) / 2], [(-1j + 1) / 2, (1 + 1j) / 2]]   # (1 - i(sx + sy + sz))/2
    conj = lambda S: mm(mm(U, S), dag(U))
    I2 = [[1, 0], [0, 1]]
    U3 = mm(mm(U, U), U)
    tr = U[0][0] + U[1][1]
    det = U[0][0] * U[1][1] - U[0][1] * U[1][0]
    disc = cmath.sqrt(tr * tr - 4 * det)
    eig = [(tr + disc) / 2, (tr - disc) / 2]
    print(f"  U sx U+ = sy: {close(conj(sx), sy)};  U sy U+ = sz: {close(conj(sy), sz)};  U sz U+ = sx: {close(conj(sz), sx)}")
    print(f"  U^3 = -I: {close(U3, [[-1, 0], [0, -1]])};  eigenphases: "
          + ", ".join(f"{math.degrees(cmath.phase(e)):+.1f} deg" for e in eig))
    eig2 = [e * e for e in eig]
    print(f"  U^2 eigenvalues: " + ", ".join(f"e^({math.degrees(cmath.phase(e)):+.0f} deg i)" for e in eig2)
          + "  -> omega and omega^2")
    entries = {complex(round(x.real, 9), round(x.imag, 9)) for row in U for x in row}
    print(f"  entries of U: {sorted(entries, key=lambda z: (z.real, z.imag))}  -- not in {{0, +-1, +-i}}: a Clifford element")


def d2():
    rule("D2  QUTRIT CLOCK AND SHIFT: THE COLOUR ANALOGUE OF THE HALF-SPIN PHASE")
    Z = [[1, 0, 0], [0, OM, 0], [0, 0, OM * OM]]
    X = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
    inv = lambda A: dag(A)                                       # unitary
    ZX, XZ = mm(Z, X), mm(X, Z)
    c = ZX[1][0] / XZ[1][0]
    plaq = mm(mm(mm(X, Z), inv(X)), inv(Z))
    print(f"  ZX = c XZ with c = e^({math.degrees(cmath.phase(c)):+.0f} deg i) = omega")
    print(f"  plaquette X Z X^-1 Z^-1 = {plaq[0][0]:.3f} I  (flux {math.degrees(cmath.phase(plaq[0][0])):+.0f} deg = 2 pi/3)")
    print("  qubit analogue: sz sx = - sx sz, plaquette -I, flux pi -- the QLF_EdgeSign half-spin phase.")


def column_matrices(L, x, signed, np):
    n = 3 ** L
    D = [[(k // 3 ** j) % 3 for j in range(L)] for k in range(n)]
    num = lambda d: sum(v * 3 ** j for j, v in enumerate(d))
    nz = [sum(1 for t in d if t) for d in D]
    Ts = []
    for col in range(3):
        T = np.zeros((3 * n, 3 * n), dtype=complex)
        for h_in in range(n):
            hi = D[h_in]
            for v in range(n):
                vd = D[v]
                k = num([(hi[j] + vd[(j - 1) % L] - vd[j]) % 3 for j in range(L)])
                amp = x ** (nz[v] + nz[k])
                if signed:
                    amp *= OM ** ((col * sum(vd)) % 3)          # vertical edges in this column carry w^(n col)
                dy = vd[L - 1]
                for y in range(3):
                    T[3 * k + (y + dy) % 3, 3 * h_in + y] += amp
        Ts.append(T)
    return Ts, D


def sectors(L, x, signed, np):
    Ts, D = column_matrices(L, x, signed, np)
    P = Ts[2] @ Ts[1] @ Ts[0]
    M = np.linalg.matrix_power(P, L)                          # L x 3L torus
    Z = {}
    for h in range(3 ** L):
        fx = sum(D[h]) % 3
        Z[fx] = Z.get(fx, 0) + M[3 * h, 3 * h]
    return Z


def t_test():
    rule("T  THE SIGNED Z3 CENSUS (flux 2 pi/3 per plaquette), L x 3L tori")
    try:
        import numpy as np
    except ImportError:
        print("  numpy not available: T skipped")
        return
    xs = [0.2, 0.3, 0.366, 0.5, 0.7, 0.9]
    Ls = (3, 4, 5, 6)
    Z1 = sectors(3, 1.0, True, np)
    print("  T1, w = 1: signed sector sums " + ", ".join(f"Z({k}) = {abs(v):.2e}" for k, v in sorted(Z1.items()))
          + f"   (unsigned: {sectors(3, 1.0, False, np)[0].real:.3e})")
    for signed in (False, True):
        print(f"\n  {'SIGNED (flux 2pi/3)' if signed else 'unsigned (sec 20 gas, same tori)'}:  |R3| = |Z(x-flux 1)/Z(0)|")
        print(f"  {'w':>6}" + "".join(f"{'L=' + str(L):>12}" for L in Ls) + f"{'3 -> 6':>10}")
        for x in xs:
            row = []
            for L in Ls:
                Z = sectors(L, x, signed, np)
                row.append(abs(Z[1]) / abs(Z[0]))
            print(f"  {x:>6.3f}" + "".join(f"{r:>12.5f}" for r in row) + f"{('falls' if row[-1] < row[0] else 'grows'):>10}")


if __name__ == "__main__":
    d1()
    d2()
    t_test()
