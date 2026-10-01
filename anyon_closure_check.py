#!/usr/bin/env python3
"""
anyon_closure_check.py -- are the substrate's closures anyonic in two dimensions? (Carbon_Superconductivity.md sec 18)

THE QUESTION (Jim, 2026-10-01): "closures may be affected by anyon behaviour since 2d is more fundamental than 3."
In 2D the exchange of two particles is a braid, and the braid group allows any phase e^{i theta}
(QLF_Anyons.lean); in 3D only +1 and -1. Does the twist substrate, restricted to two spatial axes, realise
anything beyond +-1?

  sec 1  exchange in the fold algebra: swap two strands P, Q and compare fold(PQ) with fold(QP), over every pair of
         words up to length 4 on the full alphabet and on the two-axis alphabet (x, y, gauge).
  sec 2  braiding on the closure walk: the half-spin phase is a Z2 connection on the walk graph (QLF_EdgeSign),
         pi flux through each mixed spatial plaquette. Holonomies of every closed walk on the x-y plane up to length 10.
  sec 3  the half-exchange: an anyonic exchange needs an operator whose square is not a scalar. The Ising-anyon
         braid of two Pauli-labelled strands is B = exp(pi/4 sigma_x sigma_y) = (1 + i sigma_z)/sqrt2, with B^2 = i
         sigma_z and B^8 = 1. Is B in the group the twist folds generate?
  sec 4  reading.

Stdlib only.   Run:  python3 anyon_closure_check.py
"""
from __future__ import annotations

import itertools
import math

from twist_core import pauli_fold

FULL = ['^', 'v', '<', '>', '/', '\\', '+', '-']
TWO_AXIS = ['<', '>', '^', 'v', '+', '-']              # x, y and the gauge axis


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def mul(a, b):
    (a0, a1, a2, a3), (b0, b1, b2, b3) = a, b
    return (a0 * b0 + a1 * b2, a0 * b1 + a1 * b3, a2 * b0 + a3 * b2, a2 * b1 + a3 * b3)


def ratio(m1, m2):
    """The scalar c with m1 = c m2, or None if they are not proportional."""
    for x, y in zip(m1, m2):
        if abs(y) > 1e-12:
            c = x / y
            break
    else:
        return None
    if all(abs(x - c * y) < 1e-9 for x, y in zip(m1, m2)):
        return complex(round(c.real, 9), round(c.imag, 9))
    return None


def sec1():
    rule("sec 1  EXCHANGE IN THE FOLD ALGEBRA")
    for name, alpha in (("full alphabet", FULL), ("two spatial axes + gauge", TWO_AXIS)):
        words = [''.join(w) for L in range(1, 5) for w in itertools.product(alpha, repeat=L)]
        folds = {w: pauli_fold(w) for w in words}
        # distinct fold values suffice: the exchange ratio depends only on the folds
        vals = list({tuple(complex(round(c.real, 9), round(c.imag, 9)) for c in f) for f in folds.values()})
        phases = set()
        for a in vals:
            for b in vals:
                r = ratio(mul(a, b), mul(b, a))
                phases.add(r)
        print(f"  {name:<28} words up to length 4: {len(words):>5}; distinct folds {len(vals):>2}; "
              f"exchange phases fold(PQ)/fold(QP) = {sorted(phases, key=lambda z: (z.real, z.imag))}")
    print("""
  Every exchange of two strands gives +1 or -1. The folds form the Pauli group, whose commutators are only +-1,
  so this holds at every length, in two dimensions as in three: the fold algebra has boson and fermion exchange
  and nothing between. (Closed strands fold to +-I and always commute: +1.)""")


def sec2():
    rule("sec 2  BRAIDING ON THE CLOSURE WALK (x-y PLANE)")
    # QLF_EdgeSign: edge x -> x + s e_a carries s * (-1)^(sum of spatial coordinates x_b with b > a).
    # Axes in the plane: a = 0 (x), a = 1 (y).
    steps = [(0, 1), (0, -1), (1, 1), (1, -1)]

    def edge_sign(pos, a, s):
        return s * (-1) ** sum(pos[b] for b in range(a + 1, 2))

    hol = {}
    plaq = None
    for L in range(2, 11, 2):
        vals = set()
        for word in itertools.product(range(4), repeat=L):
            pos = [0, 0]
            sign = 1
            for k in word:
                a, s = steps[k]
                sign *= edge_sign(pos, a, s)
                pos[a] += s
            if pos == [0, 0]:
                vals.add(sign)
                if L == 4 and word == (0, 2, 1, 3):
                    plaq = sign
        hol[L] = sorted(vals)
    print(f"  holonomies of closed planar walks, by length: {hol}")
    print(f"  the elementary plaquette x, y, -x, -y: {plaq:+d}  (pi flux)")
    print("""
  The connection takes the values +-1, so every holonomy is +-1: carrying one closure around another picks up
  (-1)^(number of enclosed mixed plaquettes). The flux per plaquette is pi, the only nontrivial value a Z2
  connection has. A continuous braiding phase would need flux other than 0 or pi.""")


def sec3():
    rule("sec 3  THE HALF-EXCHANGE")
    r = 1 / math.sqrt(2)
    B = (complex(r, r), 0j, 0j, complex(r, -r))          # (1 + i sigma_z)/sqrt2
    P = B
    powers = []
    for k in range(1, 9):
        powers.append(P)
        P = mul(P, B)
    is_scalar = lambda m: abs(m[1]) < 1e-12 and abs(m[2]) < 1e-12 and abs(m[0] - m[3]) < 1e-12
    first_scalar = next(k for k, m in enumerate(powers, 1) if is_scalar(m))
    print(f"  B = (1 + i sigma_z)/sqrt2: eigenphases e^(+-i pi/4); B^2 = i sigma_z (not a scalar);"
          f" first scalar power B^{first_scalar} = {powers[first_scalar - 1][0]:.0f} I")
    # the group generated by the single-twist folds is the Pauli group: entries in {0, +-1, +-i}
    folds = {tuple(complex(round(c.real, 9), round(c.imag, 9)) for c in pauli_fold(''.join(w)))
             for L in range(1, 5) for w in itertools.product(FULL, repeat=L)}
    entries = {c for f in folds for c in f}
    print(f"  entries of every fold: {sorted(entries, key=lambda z: (z.real, z.imag))}")
    print("""
  B has entries (1 +- i)/sqrt2, which no fold has: the half-exchange is outside the group the twists generate.
  It lies in the Clifford group, one level above the Pauli group. So the Ising-anyon braid is not native to the
  substrate either; it would be an extension, a closure that can be half-exchanged.""")


def sec4():
    rule("sec 4  READING")
    print("""
The substrate's own algebra is Z2 in two dimensions as in three. Fold exchanges give +-1 (sec 1), the walk's
connection gives +-1 holonomies with pi flux (sec 2), and the half-exchange that anyons need is not generated by
twists (sec 3). So `QLF_BalancedPhaseReal` (closures fold to +-I) is not a 3D import: it is algebraic and holds on
two axes too.

Anyons enter QLF in one way so far: flux attachment, closures binding flux -- the composite-fermion construction
of QLF_FQHE, which derives the odd-denominator rule. To make 2D closures anyonic natively, the substrate would
need a connection with flux other than 0 and pi (U(1) or Z_N, not Z2), or Clifford half-exchanges. Either is a new
physical claim, not a consequence of what is proved.

For the superconductivity thread this sharpens sec 7: the one-bit phase was not a 3D import, so its failure in
aluminium and in the bilayer is a real failure of the one-bit reading, not an artefact of dimension. The continuous
phase those samples show comes, on this reading, from the collective rendering of many closures (vortex winding of
the condensate), not from anyonic single closures.""")


if __name__ == "__main__":
    sec1()
    sec2()
    sec3()
    sec4()
