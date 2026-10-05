#!/usr/bin/env python3
"""
z6_spin_colour.py -- the Z6 of spin x colour (Carbon_Superconductivity.md sec 29; frozen in commit eff3a2d).

  SM   sanity check: every Standard Model field satisfies Y = d/2 - t/3 and Q = -t/3 (mod 1), with d the SU(2)
       doublet bit, t the colour triality, Q = T3 + Y. Also shown: the same lock with d read as fermion parity.
  Z1   with the sec-27 colour vectors, triality t(w) = <v_g, sum v> is the net spatial count N mod 3, and the
       spin-1/2 parity d(w) is N mod 2: both centre charges are residues of one integer.
  Z2   the lock then demands 3Q + N = 0 (mod 3) of every particle word named in a Lean theorem.
  Z3   d = 1 for every named fermion?

Exact integer arithmetic. Twist vectors from lean/QLF_ColourFlux.lean.
Run:  python3 z6_spin_colour.py
"""
from __future__ import annotations

import itertools
from fractions import Fraction as Fr

VEC = {'+': (1, 0), '-': (2, 0), '>': (0, 1), '<': (0, 2), '^': (2, 1), 'v': (1, 2), '/': (1, 1), '\\': (2, 2)}
SPATIAL_SIGN = {'>': 1, '<': -1, '^': 1, 'v': -1, '/': 1, '\\': -1, '+': 0, '-': 0}
VG = VEC['+']


def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0]) % 3


def triality(w):
    s = (sum(VEC[c][0] for c in w) % 3, sum(VEC[c][1] for c in w) % 3)
    return symp(VG, s)


def N(w):
    return sum(SPATIAL_SIGN[c] for c in w)


def nspatial(w):
    return sum(1 for c in w if c not in '+-')


def antiparticle(w):
    conj = {'>': '<', '<': '>', '^': 'v', 'v': '^', '/': '\\', '\\': '/', '+': '-', '-': '+'}
    return ''.join(conj[c] for c in reversed(w))


def rule(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def main():
    rule("SM sanity: Y = d/2 - t/3 and Q = -t/3 (mod 1), Q = T3 + Y")
    # (field, colour triality t, doublet d, Y, fermion?)
    sm = [("Q_L", 1, 1, Fr(1, 6), 1), ("u_R", 1, 0, Fr(2, 3), 1), ("d_R", 1, 0, Fr(-1, 3), 1),
          ("L_L", 0, 1, Fr(-1, 2), 1), ("e_R", 0, 0, Fr(-1), 1), ("H", 0, 1, Fr(1, 2), 0)]
    print("field   t  d   Y      Y-(d/2-t/3)   with d=fermion parity")
    for f, t, d, Y, ferm in sm:
        r1 = (Y - (Fr(d, 2) - Fr(t, 3))) % 1
        r2 = (Y - (Fr(ferm, 2) - Fr(t, 3))) % 1
        print(f"{f:5}  {t}  {d}  {str(Y):>5}   {str(r1):>5}          {str(r2):>5}")
        assert r1 == 0
        for T3 in ((Fr(1, 2), Fr(-1, 2)) if d else (Fr(0),)):
            assert (T3 + Y + Fr(t, 3)) % 1 == 0          # Q = -t/3 mod 1
    print("Doublet bit: lock holds for all fields. Fermion parity in place of d: fails for u_R, d_R, e_R, H.")

    rule("Z1: triality = N mod 3, spin-1/2 parity = N mod 2")
    for c in VEC:
        assert symp(VG, VEC[c]) == SPATIAL_SIGN[c] % 3, c
    print("per twist: <v_g, v_s> = +1 for > ^ /, -1 for < v \\, 0 for + -")
    nw = 0
    for L in range(0, 7):
        for w in itertools.product(VEC, repeat=L):
            assert triality(w) == N(w) % 3
            assert nspatial(w) % 2 == N(w) % 2
            nw += 1
    print(f"checked on all {nw} words of length <= 6: (d, t) = (N mod 2, N mod 3), i.e. N mod 6")

    rule("Z2/Z3: the named particle words (Lean dictionary)")
    proton = '>^/'
    words = [
        ("proton", proton, 1, 1, "QLF_BaryonWinding.baryon_proton (+ KnotInvariant, Baryogenesis, QuantumBlackHole)"),
        ("antiproton", antiparticle(proton), -1, 1, "QLF_BaryonWinding.baryon_antiproton"),
        ("meson", proton + antiparticle(proton), 0, 0, "QLF_BaryonWinding.baryon_meson (+ pion_meson_horizon)"),
        ("electron", '^<v>', -1, 1, "QLF_ElectronClosure.electronCycle (+ BaryonWinding, Majorana, NeutrinoMass)"),
        ("electron, charged", '^<v>+', -1, 1, "QLF_ElectronClosure.electronCharged"),
        ("positron", 'v>^<', 1, 1, "QLF_ElectronClosure.positronCycle"),
        ("positron, charged", 'v>^<-', 1, 1, "QLF_ElectronClosure.positronCharged"),
        ("neutrino", '^v', 0, 1, "QLF_Majorana.neutrino_majorana (+ BaryonWinding, Spin, WeakChirality)"),
    ]
    print(f"{'particle':18} {'word':8} {'N':>3} {'t':>2} {'Q':>3}  3Q+N mod 3  Z2    d  fermion  Z3")
    z2 = z3 = True
    for name, w, Q, ferm, src in words:
        r = (3 * Q + N(w)) % 3
        d = nspatial(w) % 2
        ok2, ok3 = r == 0, (d == 1) == bool(ferm)
        z2 &= ok2
        z3 &= ok3
        print(f"{name:18} {w:8} {N(w):>3} {triality(w):>2} {Q:>3}  {r:>10}  {'pass' if ok2 else 'FAIL':5} {d:>2}  {ferm:>7}"
              f"  {'pass' if ok3 else 'FAIL'}")
    print(f"\nZ2 over the named particles: {'PASS' if z2 else 'FAIL'};  Z3: {'pass' if z3 else 'FAIL'}")
    print("Every named particle word has N = 0 mod 3, so Z2 could not have failed on this dictionary.")
    w = '^<v'
    print(f"Not a particle (the electron's open prefix, QLF_ElectronClosure.electronPrefix): {w}, N = {N(w)},"
          f" t = {triality(w)}; with the electron's charge, 3Q + N = {(3 * -1 + N(w)) % 3} (mod 3).")


if __name__ == "__main__":
    main()
