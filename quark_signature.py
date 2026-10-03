#!/usr/bin/env python3
"""
quark_signature.py -- the quark twist signature (Carbon_Superconductivity.md sec 30; frozen in commit ebc9792).

  S1  conserved (w(conj t) = -w(t)), colour-blind (cycTwist-invariant) twist charges form Q = a N + b n_g.
  S2  the charged electron (^<v>+, Q = -1) gives b = -1; the sec-29 lock and quark charges 2/3, -1/3 leave
      a = -1/3 (d-bare: u = d + '-') or a = 2/3 (u-bare: d = u + '+').
  S3  hadron charges and beta-decay conservation under each signature (additive; cannot fail).
  T1  tie-break: (a) beta decay as a single-twist transfer; (b) twist-count mass ordering m_n > m_p, m_d > m_u.
  T2  weak colour-blindness: is D(v_d) a phase times D(v_u) in the sec-27 colour structure?

Exact arithmetic (Fractions). Colour vectors from lean/QLF_ColourFlux.lean; Weyl matrices from weyl_sl3.py.
Run:  python3 quark_signature.py
"""
from __future__ import annotations

from fractions import Fraction as Fr

import weyl_sl3 as W

TW = ['>', '<', '^', 'v', '/', '\\', '+', '-']
CONJ = {'>': '<', '<': '>', '^': 'v', 'v': '^', '/': '\\', '\\': '/', '+': '-', '-': '+'}
CYC = {'>': '^', '<': 'v', '^': '/', 'v': '\\', '/': '>', '\\': '<', '+': '+', '-': '-'}
SP = {'>': 1, '<': -1, '^': 1, 'v': -1, '/': 1, '\\': -1, '+': 0, '-': 0}
GA = {'+': 1, '-': -1}


def N(w):
    return sum(SP[c] for c in w)


def ng(w):
    return sum(GA.get(c, 0) for c in w)


def bar(w):
    return ''.join(CONJ[c] for c in reversed(w))


def rule(t):
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def main():
    rule("S1  conserved, colour-blind twist charges")
    # Unknowns w(t) for 8 twists. Constraints: w(t) + w(conj t) = 0; w(cyc t) - w(t) = 0. Rank via orbits.
    classes = {}
    for t in TW:
        orbit = {t}
        while True:
            new = orbit | {CYC[x] for x in orbit} | {CONJ[x] for x in orbit}
            if new == orbit:
                break
            orbit = new
        classes[frozenset(orbit)] = None
    print(f"orbits of <cycTwist, conj>: {[sorted(o) for o in classes]}")
    # Within an orbit, cyc preserves the value and conj negates it, so one free value per orbit, fixed by sign.
    print("each orbit is {positive twists} u {their conjugates}: one free parameter per orbit ->"
          " Q = a*N + b*n_g (2 parameters)")
    assert len(classes) == 2

    rule("S2  fixing a and b")
    e = '^<v>+'
    print(f"charged electron {e}: N = {N(e)}, n_g = {ng(e)}; Q = -1  =>  b = -1")
    sigs = {}
    for a in (Fr(-1, 3), Fr(2, 3)):
        Q = (lambda a: (lambda w: a * N(w) - ng(w)))(a)
        lock = all((3 * Q(w) + N(w)) % 3 == 0 for w in ('>', '>+', '>-', '>>', '^<v>+', '>^/'))
        sigs[a] = Q
        print(f"a = {str(a):>4}: single twist '>' has Q = {Q('>')};  lock 3Q+N = 0 mod 3: {lock}")
    up, dn = {}, {}
    up[Fr(-1, 3)], dn[Fr(-1, 3)] = '>-', '>'          # d-bare
    up[Fr(2, 3)], dn[Fr(2, 3)] = '>', '>+'            # u-bare
    names = {Fr(-1, 3): "d-bare (d = >, u = >-)", Fr(2, 3): "u-bare (u = >, d = >+)"}

    rule("S3  hadron charges (additive; consistency only)")
    for a, Q in sigs.items():
        u, d = up[a], dn[a]
        uy, dy = u.replace('>', '^'), d.replace('>', '^')
        uz, dz = u.replace('>', '/'), d.replace('>', '/')
        had = {
            "p = u u d": u + uy + dz, "n = u d d": u + dy + dz, "Delta++ = uuu": u + uy + uz,
            "Delta- = ddd": d + dy + dz, "pi+ = u dbar": u + bar(d), "pi- = d ubar": d + bar(u),
            "ud diquark": u + dy, "H = p + e": u + uy + dz + '^<v>+',
            "generation nu+e+3u+3d": '^v' + '^<v>+' + u + uy + uz + d + dy + dz,
        }
        print(names[a])
        for k, w in had.items():
            print(f"   {k:24} {w:16} Q = {Q(w)}")
        nb, pb = u + dy + dz, u + uy + dz
        rhs = pb + '^<v>+' + bar('^v')
        print(f"   n -> p e nubar: Q {Q(nb)} -> {Q(rhs)}; n_g {ng(nb)} -> {ng(rhs)}; N {N(nb)} -> {N(rhs)}")
        assert Q(nb) == Q(rhs)

    rule("T1  tie-break")
    res = {}
    for a in sigs:
        u, d = up[a], dn[a]
        # (a) d -> u + W-: the W must carry the gauge difference d - u.
        diff = ng(d) - ng(u)
        transfer = (len(d) > len(u)) and d.startswith(u) and d[len(u):] == '+'
        pair = not transfer
        # (b) twist counts
        p = u + u.replace('>', '^') + d.replace('>', '/')
        n = u + d.replace('>', '^') + d.replace('>', '/')
        mass_np = len(n) > len(p)
        mass_du = len(d) > len(u)
        res[a] = (transfer, mass_np, mass_du)
        dpp = u + u.replace('>', '^') + u.replace('>', '/')
        print(f"   (outside the rule) Delta++ has {len(dpp)} twists vs p {len(p)}: m_Delta > m_p {'holds' if len(dpp) > len(p) else 'FAILS'}")
        print(f"{names[a]:24}: W- carries n_g {diff:+d}; beta decay is a transfer of the '+': {transfer}"
              f" (else a gauge pair is created: {pair});  twists p {len(p)}, n {len(n)} -> m_n > m_p: {mass_np};"
              f"  m_d > m_u: {mass_du}")
    adopted = [a for a, r in res.items() if all(r)]
    print(f"adopted: {[names[a] for a in adopted]}")

    rule("T2  weak colour-blindness in the sec-27 colour structure")
    for a in sigs:
        u, d = up[a], dn[a]
        vu = (sum(W.VEC[c][0] for c in u) % 3, sum(W.VEC[c][1] for c in u) % 3)
        vd = (sum(W.VEC[c][0] for c in d) % 3, sum(W.VEC[c][1] for c in d) % 3)
        same = any(W.meq(W.D(vd), W.msc(W.OMP[k], W.D(vu))) for k in range(3))
        line = lambda v: [t for t in W.TW if W.VEC[t] in (v, W.neg(v))]
        print(f"{names[a]:24}: colour displacement u {vu} (axis of {line(vu)}), d {vd} (axis of {line(vd)});"
              f"  D(v_d) = phase * D(v_u): {same}")
    print("The W (one gauge twist) moves the quark's colour displacement to a different line:"
          " colour is changed, triality (N mod 3) is not.")


if __name__ == "__main__":
    main()
