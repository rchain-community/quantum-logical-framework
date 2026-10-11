#!/usr/bin/env python3
"""
frequency_weighted_census.py -- the two census readings weighted by their frequency (Carbon_Superconductivity.md
sec 47, a post-hoc record) and the pre-registered transfer to the proton (sec 48, commit aab8642, fixed before this
script was written).

Readings:
  mode   every listening language (Alpha_Residual sec 9n): primes always heard, composites in half the languages
  order  sec 46a: prime closures summed with their fold signs over their orders; the surviving fraction f_n scales
         the irreducible coefficient; every composite counted, G = 1/(1 - I)
Frequency = the cylinder (Kraft) weight 8^-L of a closure. Mass of a reading = summed 8^-L of what it counts:
  mode   p + (G(p) - p)/2,  p = 0.193201673 (Polya's p4, data/closure_walk.json), G(m) = m/(1 - m)
  order  G(q),  q = sum_n K_n 8^-2n  (8-twist prime census, n <= 8)
Weight of the order reading w = m_order / (m_mode + m_order).

sec 47 (record):  alpha^-1 = (1 - w) 137.032002 + w alpha^-1_order
sec 48 (test):    census pi by sector on the one-axis walk at 4^-n (Alpha_Residual sec 9o), pi = 2 sum c_n/(4^n (2n+1)),
                  c_0 = 1; mode pi = 2 + pi/4; order pi from G' = 1/(1 - I'), I' = sum 2 Catalan(n-1) f_n x^n, f_n
                  beyond n = 8 bracketed by 0 and f_8; pi_rule = (1 - w) pi_mode + w pi_order;
                  pass iff |6 pi_rule^5 / 1836.15267343 - 1| < 1e-3 at both ends of the bracket.

--proton-tail (sec 50, pre-registered in commit 895ff8a): m_p/m_e = 6 pi^5 + T, T each reading's alpha tail unchanged
                  (coupling 1/128), against delta_p = 1836.15267343 - 6 pi^5.
                  P1 pass iff |T_freq - delta_p| <= 0.00031 (the frequency reading's miss on alpha);
                  P2 the frequency reading is the closest of the five.

Run:  python3 frequency_weighted_census.py [--proton-tail]   (about 7 s; reuses entanglement_order_alpha.census)
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as Fr

import entanglement_order_alpha as eo

CODATA_ALPHA = 137.035999177
MODE_ALPHA = 137.032002032
MP_ME = 1836.15267343
N_CENSUS = 8          # prime census to length 16 (length 18 needs ~90 s and most of this machine's memory)
N_PI = 6000           # terms of the census-pi sums


def prime_census(nmax):
    pr = eo.census(2 * nmax, prime_only=True)
    f, K = [Fr(1)], [0]
    for n in range(1, nmax + 1):
        P = Kn = 0
        for folds in pr[2 * n].values():
            S = sum(eo.sign_of(Pp) * w for Pp, w in folds.items())
            P += sum(folds.values())
            Kn += abs(S)
        f.append(Fr(Kn, P))
        K.append(Kn)
    return f, K


def order_pi(f_of):
    """2 sum_n g'_n / (4^n (2n+1)) with the coefficients scaled by 4^-n throughout (floats)."""
    a = [0.0] * (N_PI + 1)                       # 2 Catalan(n-1) f_n / 4^n
    cat = 1.0                                    # Catalan(n-1) / 4^(n-1)
    for n in range(1, N_PI + 1):
        if n > 1:
            m = n - 1                            # Catalan(m)/4^m from Catalan(m-1)/4^(m-1)
            cat *= 2 * (2 * m - 1) / (4 * (m + 1))
        a[n] = 2 * cat / 4 * f_of(n)
    b = [1.0] + [0.0] * N_PI
    for n in range(1, N_PI + 1):
        b[n] = sum(a[k] * b[n - k] for k in range(1, n + 1))
    return 2 * sum(b[n] / (2 * n + 1) for n in range(N_PI + 1)), b[N_PI]


def main():
    f, K = prime_census(N_CENSUS)
    p = json.load(open('data/closure_walk.json'))['polya_p4']
    q = sum(K[n] / 64 ** n for n in range(1, N_CENSUS + 1))
    G = lambda m: m / (1 - m)
    m_mode, m_order = p + (G(p) - p) / 2, G(q)
    w = m_order / (m_mode + m_order)
    a_order = float(eo.alpha_inv(f))
    a_rule = (1 - w) * MODE_ALPHA + w * a_order

    print("sec 47  frequency masses (record, post hoc)")
    print(f"    p = {p:.9f}   q = {q:.7f}  (last term {K[-1] / 64 ** N_CENSUS:.1e})")
    print(f"    mass mode = {m_mode:.6f}   mass order = {m_order:.6f}   w_order = {w:.4f}")
    print(f"    alpha^-1: mode {MODE_ALPHA:.6f}, order {a_order:.6f}, weighted {a_rule:.6f}"
          f"   (CODATA {CODATA_ALPHA:.6f}, diff {a_rule - CODATA_ALPHA:+.6f})")

    if '--proton-tail' in sys.argv:
        proton_tail(a_order - 137, a_rule - 137)
        return

    print("\nsec 48  the proton (pre-registered)")
    ctrl, _ = order_pi(lambda n: 1.0)       # f_n = 1 is the total sector: pi, up to the tail 2/sqrt(pi N)
    assert abs(ctrl + 2 / math.sqrt(math.pi * N_PI) - math.pi) < 1e-5, ctrl
    print(f"    control: f_n = 1 gives {ctrl + 2 / math.sqrt(math.pi * N_PI):.6f} (pi, with the asymptotic tail)")
    pi_mode = 2 + math.pi / 4
    f8 = float(f[N_CENSUS])
    res = {}
    for label, beyond in (("f_n = 0 beyond n = 8", 0.0), ("f_n = f_8 beyond n = 8", f8)):
        pi_o, tail = order_pi(lambda n: float(f[n]) if n <= N_CENSUS else beyond)
        pi_r = (1 - w) * pi_mode + w * pi_o
        m = 6 * pi_r ** 5
        res[label] = m / MP_ME - 1
        print(f"    {label:<24} pi_order = {pi_o:.6f}  (last coefficient {tail:.1e})")
        print(f"    {'':<24} pi_rule = {pi_r:.6f}   6 pi_rule^5 = {m:.2f}   off {m / MP_ME - 1:+.4f}")
    print(f"    pi_mode = 2 + pi/4 = {pi_mode:.6f};  6 pi^5 = {6 * math.pi ** 5:.4f} (off {6 * math.pi ** 5 / MP_ME - 1:+.1e})")
    bound = (1 - w) * pi_mode + w * math.pi
    print(f"    structural bound: pi_rule <= {bound:.4f}, 6 bound^5 = {6 * bound ** 5:.1f}")
    ok = all(abs(r) < 1e-3 for r in res.values())
    print(f"    sec 48: {'PASS' if ok else 'FAIL'}  (pass iff |off| < 1e-3 at both ends)")


def proton_tail(t_order, t_freq):
    s62 = math.sqrt(62)
    tails = {'irreducible': 126 - 16 * s62, 'total': 512 * s62 / 31 - 130, 'mode (w = 1/2)': MODE_ALPHA - 137,
             'order (sec 46a)': t_order, 'frequency (sec 47)': t_freq}
    lead = 6 * math.pi ** 5
    dp = MP_ME - lead
    da = CODATA_ALPHA - 137
    print("\nsec 50  alpha's census tail on the proton (pre-registered)")
    print(f"    delta_p = {MP_ME} - 6 pi^5 = {dp:.6f}     alpha's residual {da:.6f}")
    print(f"    {'reading':<20} {'T':>9} {'T - delta_p':>12} {'T - delta_alpha':>16} {'m_p/m_e':>15}")
    for k, t in tails.items():
        print(f"    {k:<20} {t:>9.6f} {t - dp:>+12.6f} {t - da:>+16.6f} {lead + t:>15.6f}")
    miss = tails['frequency (sec 47)'] - dp
    best = min(tails, key=lambda k: abs(tails[k] - dp))
    p1 = abs(miss) <= 0.00031
    print(f"    P1: {'PASS' if p1 else 'FAIL'}  (|T_freq - delta_p| = {abs(miss):.6f}, "
          f"{abs(miss) / dp:.1%} of the residual; alpha: {abs(t_freq - da):.6f}, {abs(t_freq - da) / da:.1%})")
    print(f"    P2: {'PASS' if best == 'frequency (sec 47)' else 'FAIL'}  (closest reading: {best})")


if __name__ == '__main__':
    main()
