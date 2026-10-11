#!/usr/bin/env python3
"""
carrier_helicity.py -- why a carrier moving at c has no s_z = 0 state (Carbon_Superconductivity.md sec 38;
pre-registered in commit e189af9, before this script was written).

Readings used, as the pre-registration fixed them:
  momentum of a twist  = its displacement eps * e_a        (the signed action vector)
  spin of a twist      = 1/2 * its Pauli matrix as a vector (PAULI_MAP: M(t) = eps * sigma_a)
  conjugate half       = adjoint_history(t) from twist_core, run backward in time; read forward, time reversal
                         flips both its momentum and its spin

  P1  the helicity of each of the six spatial twists
  C1  the photon [t, t+]: spin along its motion, over all six emitter halves (primary)
  C2  the graviton, two photons along one direction
  C3  massive control: drop D1 (reversals allowed), so each half takes either spin along the axis
  C4  the 24 commutator carriers of sec 32b (not blind; consistency only)

--generator (sec 39, pre-registered in commit 87a8978): spin read from the generator tau = conv * i * sigma,
  S = -(i/2) tau. Time reversal leaves tau unchanged, so the conjugate half keeps tau(t+) = -tau(t) read forward
  (its momentum still flips). Runs conv = +1 (QLF's tau = i sigma) and conv = -1, both fold orders; C4 dropped.

Exact arithmetic (Fractions). Stdlib only, plus twist_core.
Run:  python3 carrier_helicity.py [--generator]
"""
from __future__ import annotations

import sys
from collections import Counter
from fractions import Fraction as Fr

from twist_core import PAULI_MAP, _mat_mul, adjoint_history, calculate_action

SPATIAL = ['^', 'v', '>', '<', '/', '\\']


def momentum(t):
    """Displacement as an (x, y, z) vector, from the canonical action vector (v=y, h=x, d=z, l=gauge)."""
    v, h, d, _ = calculate_action(t)
    return (h, v, d)


def spin(t):
    """Half the Pauli-vector of the twist's matrix: M = n.sigma  ->  S = n/2."""
    a, b, c, dd = PAULI_MAP[t]
    nx = (b + c) / 2            # tr(M sigma_x)/2
    ny = (c - b) / 2j           # tr(M sigma_y)/2  (sigma_y = [[0,-i],[i,0]])
    nz = (a - dd) / 2           # tr(M sigma_z)/2
    vec = []
    for n in (nx, ny, nz):
        assert abs(n.imag) < 1e-12
        vec.append(Fr(round(n.real)) / 2)
    return tuple(vec)


def dot(u, w):
    return sum(Fr(x) * Fr(y) for x, y in zip(u, w))


def neg(u):
    return tuple(-x for x in u)


def forward_mirror(t):
    """The conjugate half, read forward in time: time reversal flips momentum and spin."""
    c = adjoint_history(t)
    return c, neg(momentum(c)), neg(spin(c))


def tau(t, conv):
    """The generator tau = conv * i * sigma as a 2x2 matrix (a, b, c, d)."""
    return tuple(conv * 1j * x for x in PAULI_MAP[t])


def spin_from_generator(m, conv):
    """S = -(i/2) tau, read as a vector; for tau = conv*i*n.sigma this is conv*n/2."""
    herm = tuple(-1j * conv * x for x in m)          # n.sigma, Hermitian
    a, b, c, dd = herm
    vec = []
    for n in ((b + c) / 2, (c - b) / 2j, (a - dd) / 2):
        assert abs(n.imag) < 1e-12
        vec.append(Fr(round(n.real)) / 2)
    return tuple(conv * x for x in vec)


def forward_mirror_generator(t, conv):
    """sec 39 G2: the conjugate half keeps tau(t+) read forward; only its momentum flips."""
    c = adjoint_history(t)
    return c, neg(momentum(c)), spin_from_generator(tau(c, conv), conv)


def main_generator():
    for conv in (1, -1):
        print(f"=== convention tau = {'+' if conv > 0 else '-'}i sigma ===")
        print("P1'  helicities of forward halves and of conjugate halves read forward")
        for t in SPATIAL:
            d = momentum(t)
            c, p2, s2 = forward_mirror_generator(t, conv)
            print(f"  {t!r:5} forward {dot(spin_from_generator(tau(t, conv), conv), d)}   "
                  f"mirror {c!r} (p={p2}) {dot(s2, d)}")

        print("C1  the photon [t, t+], both fold orders")
        c1 = Counter()
        for t in SPATIAL:
            d = momentum(t)
            c, p2, s2 = forward_mirror_generator(t, conv)
            assert p2 == d
            f1 = _mat_mul(tau(t, conv), tau(c, conv))
            f2 = _mat_mul(tau(c, conv), tau(t, conv))
            s_tot = dot(spin_from_generator(tau(t, conv), conv), d) + dot(s2, d)
            c1[s_tot] += 1
            print(f"  emitter {t!r}  s = {s_tot}   folds equal in both orders: "
                  f"{all(abs(x - y) < 1e-12 for x, y in zip(f1, f2))}")
        c1_pass = sorted(c1) == [-1, 1] and c1[-1] == c1[1]
        print(f"  states: {dict(sorted(c1.items()))}  ->  C1 {'PASS' if c1_pass else 'FAIL'}")

        c2 = Counter()
        for t in SPATIAL:
            d = momentum(t)
            for u in SPATIAL:
                if momentum(u) == d:
                    c2[sum(dot(spin_from_generator(tau(w, conv), conv), d)
                           + dot(forward_mirror_generator(w, conv)[2], d) for w in (t, u))] += 1
        print(f"C2  graviton states: {dict(sorted(c2.items()))}  ->  "
              f"C2 {'PASS' if sorted(c2) == [-2, 2] else 'FAIL'}")

        c3 = Counter()
        for pair in (('^', 'v'), ('>', '<'), ('/', '\\')):
            d = momentum(pair[0])
            for h1 in pair:
                for h2 in pair:
                    c3[sum(dot(spin_from_generator(tau(h, conv), conv), d) for h in (h1, h2))] += 1
        print(f"C3  reversals allowed: {dict(sorted(c3.items()))};  with D1 (C1): s = 0 "
              f"{'present -> C3 FAILS' if 0 in c1 else 'absent'}\n")


def main():
    print("P1  helicity of each spatial twist (spin along its own motion)")
    hel = {}
    for t in SPATIAL:
        p, s = momentum(t), spin(t)
        hel[t] = dot(s, p)            # |p| = 1
        print(f"  {t!r:5} p={p}  S={tuple(str(x) for x in s)}  helicity={hel[t]}")
    print(f"  helicities present: {sorted(set(hel.values()))}")

    print("\nC1  the photon [t, t+], spin along its motion")
    c1 = Counter()
    for t in SPATIAL:
        d = momentum(t)
        c, p2, s2 = forward_mirror(t)
        assert p2 == d, "the mirror half, read forward, must move with the emitter"
        s_tot = dot(spin(t), d) + dot(s2, d)
        c1[s_tot] += 1
        print(f"  emitter {t!r}  mirror {c!r} (forward p={p2})  s along motion = {s_tot}")
    states1 = sorted(c1)
    c1_pass = states1 == [-1, 1] and c1[-1] == c1[1]
    print(f"  states: {dict(sorted(c1.items()))}  ->  C1 {'PASS' if c1_pass else 'FAIL'}")

    print("\nC2  the graviton: two photons along one direction")
    c2 = Counter()
    for t in SPATIAL:
        d = momentum(t)
        for u in SPATIAL:
            if momentum(u) != d:
                continue
            s = sum(dot(spin(w), d) + dot(forward_mirror(w)[2], d) for w in (t, u))
            c2[s] += 1
    states2 = sorted(c2)
    c2_pass = states2 == [-2, 2]
    print(f"  states: {dict(sorted(c2.items()))}  ->  C2 {'PASS' if c2_pass else 'FAIL'}")

    print("\nC3  massive control: reversals allowed, each half takes either twist on the axis")
    c3 = Counter()
    for axis_pair in (('^', 'v'), ('>', '<'), ('/', '\\')):
        d = momentum(axis_pair[0])
        for h1 in axis_pair:
            for h2 in axis_pair:
                c3[dot(spin(h1), d) + dot(spin(h2), d)] += 1
    print(f"  states: {dict(sorted(c3.items()))}  ->  "
          f"{'s = 0 present (control passes)' if 0 in c3 else 's = 0 absent (control FAILS)'}")
    print("  data: longitudinal W fraction in top decay F0 = 0.693 +- 0.014 (JHEP 08 (2020) 051); not blind")

    print("\nC4  the 24 commutator carriers [a, b, a+, b+], distinct spatial axes")
    carriers = [(a, b) for a in SPATIAL for b in SPATIAL if momentum(a) != momentum(b)
                and momentum(a) != neg(momentum(b))]
    assert len(carriers) == 24
    axes = [momentum(t) for t in ('>', '^', '/')]
    admissible = Counter()
    for a, b in carriers:
        word = [a, b, adjoint_history(a), adjoint_history(b)]
        for d in axes + [neg(x) for x in axes]:
            steps_on_d = [dot(momentum(w), d) for w in word]
            if all(x >= 0 for x in steps_on_d) and any(x > 0 for x in steps_on_d):
                admissible[d] += 1
    print(f"  carriers that advance along some direction with no reversal on it: {sum(admissible.values())}")
    print("  (every carrier steps both ways on each of its two axes and not at all on the third)")


if __name__ == '__main__':
    main_generator() if '--generator' in sys.argv else main()
