"""
yang_mills_census.py -- what the closure census says about a mass gap.

Companion to YangMills_MassGap_QLF.md sec 7. Pure Python, exact integers.

A Euclidean mass gap m shows up as exponential decay e^{-mL} of a return amplitude in the
length L of the path, at fixed normalisation. Three censuses of closed twist histories on Z^4:

  W_L  unsigned: every closure counts 1 (closure_walk.closed_walk_count).
  A_L  signed:   the half-spin phase, the Z2 edge-sign connection (closure_walk.edge_sign,
                 QLF_EdgeSign), pi flux through every mixed spatial plaquette.
  C_L  colour:   the Z3 phase omega^B, B the baryon winding of QLF_BaryonWinding (the signed
                 Levi-Civita sum over consecutive axis triples, i.e. three dimensions at a time).
                 B is invariant exactly under the cyclic axis relabelings (A3 = Z3, see
                 z3_colour_derivation.py), so omega^B is the colour phase that cycle defines.

Each census grows like rho^L times a power of L, where rho is the spectral radius of its
transfer operator. W has rho = 8 and returns like 8^L / L^2: the massless 4-D propagator.
A sector with rho < 8 is suppressed relative to the unsigned census at the rate ln(8/rho) per
step. That is a relative rate between sectors, not a gap inside a sector: each sector still
has a continuous band edge (power-law prefactor), which is what the printout checks.
"""
import cmath
import math
import sys

from closure_walk import closed_walk_count, edge_sign

STEPS = [(a, s) for a in range(4) for s in (1, -1)]


def signed_census(lmax: int) -> dict:
    """A_L, exact: return amplitude of the Z2 edge-sign connection."""
    cur = {(0, 0, 0, 0): 1}
    out = {}
    for L in range(1, lmax + 1):
        nxt = {}
        rem = lmax - L
        for x, v in cur.items():
            xl = list(x)
            for a, s in STEPS:
                y = list(x)
                y[a] += s
                if sum(map(abs, y)) > rem:
                    continue
                t = tuple(y)
                nxt[t] = nxt.get(t, 0) + v * edge_sign(xl, a, s)
        cur = {k: v for k, v in nxt.items() if v}
        if L % 2 == 0:
            out[L] = cur.get((0, 0, 0, 0), 0)
    return out


def eps(a, b, c) -> int:
    """Levi-Civita on the three spatial axes 0,1,2; the gauge axis 3 never links."""
    if 3 in (a, b, c) or len({a, b, c}) < 3:
        return 0
    return 1 if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def _times_omega(z, k):
    """(p + q w) * w^k in Z[w], w^2 = -1 - w."""
    p, q = z
    for _ in range(k % 3):
        p, q = -q, p - q
    return p, q


def colour_census(lmax: int) -> dict:
    """C_L, exact in Z[omega]: sum over closures of omega^B."""
    cur = {((0, 0, 0, 0), None, None): (1, 0)}
    out = {}
    for L in range(1, lmax + 1):
        nxt = {}
        rem = lmax - L
        for (x, a1, a2), z in cur.items():
            for a, s in STEPS:
                y = list(x)
                y[a] += s
                if sum(map(abs, y)) > rem:
                    continue
                k = eps(a1, a2, a) if a1 is not None else 0
                zz = _times_omega(z, k)
                key = (tuple(y), a2, a)
                p, q = nxt.get(key, (0, 0))
                nxt[key] = (p + zz[0], q + zz[1])
        cur = {k: v for k, v in nxt.items() if v != (0, 0)}
        if L % 2 == 0:
            p = q = 0
            for (x, _, _), (pp, qq) in cur.items():
                if x == (0, 0, 0, 0):
                    p += pp
                    q += qq
            out[L] = (p, q)
    return out


def colour_radius(n_iter: int = 4000) -> float:
    """Spectral radius of the zero-momentum colour transfer operator on (previous axis, axis)."""
    w = cmath.exp(2j * math.pi / 3)
    states = [(a, b) for a in range(4) for b in range(4)]
    v = {s: 1.0 + 0.1j * (i % 5) for i, s in enumerate(states)}
    tot = 0.0
    for it in range(n_iter):
        nv = {s: 0j for s in states}
        for (a1, a2), x in v.items():
            for a in range(4):
                nv[(a2, a)] += 2 * x * w ** eps(a1, a2, a)
        n = math.sqrt(sum(abs(x) ** 2 for x in nv.values()))
        if it >= n_iter // 2:
            tot += math.log(n)
        v = {s: x / n for s, x in nv.items()}
    return math.exp(tot / (n_iter - n_iter // 2))


def main() -> None:
    lmax = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    rho_s = 2 + 2 * math.sqrt(3)
    rho_c = colour_radius()
    A = signed_census(lmax)
    C = colour_census(lmax)
    print(f"rho: unsigned 8, signed 2+2*sqrt3 = {rho_s:.4f}, colour {rho_c:.4f}")
    print(f"relative rates ln(8/rho): signed {math.log(8 / rho_s):.4f}, colour {math.log(8 / rho_c):.4f}"
          f"   (log 2 = {math.log(2):.4f})\n")
    print(" L   W_L*L^2/8^L   |A_L|*L^2/rho_s^L   C_L/W_L   (C_L in Z[w]; imaginary part q)")
    for L in sorted(A):
        W = closed_walk_count(L)
        p, q = C[L]
        c = complex(p, 0) + q * cmath.exp(2j * math.pi / 3)
        print(f"{L:2d}   {W * L * L / 8 ** L:10.4f}   {abs(A[L]) * L * L / rho_s ** L:12.4f}"
              f"   {abs(c) / W:9.5f}   q={q}")


if __name__ == "__main__":
    main()
