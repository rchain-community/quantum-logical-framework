#!/usr/bin/env python3
"""
gluon_plasma_dof.py -- three gluon states in a hot gluon plasma? (Carbon_Superconductivity.md sec 37;
frozen in commit c93c6d5).

Stefan-Boltzmann: p_SB/T^4 = d pi^2/90, d = 16 (QCD: 8 x 2) or 24 (R3: 8 x 3, sec 36a).
Leading-order deficit in pure SU(3): p/p_SB = 1 - delta, delta = 15 alpha_s/(4 pi) (Arnold & Zhai 1994),
alpha_s two-loop, n_f = 0, at mu = 2 pi T, Lambda_MSbar from T_c/Lambda = 1.26 +- 0.10.
Verdict on x_h = (p/T^4)_lat / (p_SB/T^4)_h at the highest T:
  pass  1 - 2 delta <= x_h <= 1 + 2 sigma;  fail  x_h < 1 - 3 delta or x_h > 1 + 3 sigma;  else undecided.
Control: QCD must pass.

Data: Borsanyi, Endrodi, Fodor, Katz & Szabo, JHEP 07 (2012) 056, Table 1 (continuum, small volume
Ns/Nt = 8 beyond 10 T_c): p/T^4 at T/T_c = 1000 is 1.7030(52); the table's other high-T rows are printed too.
Cross-check: Giusti & Pepe, Phys. Lett. B 769 (2017) 385, Table 1: p/T^4 = 1.695(7) at T/T_c = 231.3.
Run:  python3 gluon_plasma_dof.py
"""
from __future__ import annotations

import math

TABLE = {  # T/T_c: (p/T^4, error)   Borsanyi et al. 2012, Table 1
    10: (1.6078, 0.0019), 20: (1.6444, 0.0029), 50: (1.6686, 0.0043), 100: (1.6800, 0.0050),
    200: (1.6887, 0.0053), 500: (1.6977, 0.0052), 1000: (1.7030, 0.0052),
}
SB = {16: 16 * math.pi ** 2 / 90, 24: 24 * math.pi ** 2 / 90}


def alpha_s(mu_over_lambda: float) -> float:
    """Two-loop MSbar running, n_f = 0: b0 = 11, b1 = 102."""
    b0, b1 = 11.0, 102.0
    L = math.log(mu_over_lambda ** 2)
    return 4 * math.pi / (b0 * L) * (1 - b1 / b0 ** 2 * math.log(L) / L)


def verdict(x, delta, sig):
    if 1 - 2 * delta <= x <= 1 + 2 * sig:
        return "PASS"
    if x < 1 - 3 * delta or x > 1 + 3 * sig:
        return "FAIL"
    return "UNDECIDED"


def main() -> int:
    print(f"p_SB/T^4: d=16 -> {SB[16]:.4f}   d=24 -> {SB[24]:.4f}\n")
    print(f"{'T/Tc':>6} {'p/T^4':>14} {'x(16)':>8} {'x(24)':>8}  alpha_s(2piT) for Tc/Lambda = 1.16, 1.26, 1.36")
    for t, (p, e) in TABLE.items():
        a = [alpha_s(2 * math.pi * t * r) for r in (1.16, 1.26, 1.36)]
        print(f"{t:>6} {p:>8.4f}({e * 1e4:.0f}) {p / SB[16]:>8.4f} {p / SB[24]:>8.4f}  "
              + "  ".join(f"{v:.4f}" for v in a))

    gp_t, gp_p, gp_e = 231.3, 1.695, 0.007
    print(f"cross-check Giusti & Pepe 2017: T = {gp_t} T_c, p/T^4 = {gp_p}({gp_e * 1e3:.0f}):"
          f" x(16) = {gp_p / SB[16]:.4f}, x(24) = {gp_p / SB[24]:.4f}")

    t = max(TABLE)
    p, e = TABLE[t]
    print(f"\nprimary datum: T = {t} T_c, p/T^4 = {p} +- {e}")
    for r in (1.16, 1.26, 1.36):
        a = alpha_s(2 * math.pi * t * r)
        delta = 15 * a / (4 * math.pi)
        line = [f"Tc/Lambda = {r:.2f}: alpha_s = {a:.4f}, delta = {delta:.4f}, band [1 - 2delta, 1] = [{1 - 2 * delta:.4f}, 1]"]
        for d in (16, 24):
            x, sig = p / SB[d], e / SB[d]
            line.append(f"   d={d}: x = {x:.4f} +- {sig:.4f}  1-x = {1 - x:.4f} = {(1 - x) / delta:.2f} delta  -> {verdict(x, delta, sig)}")
        print("\n".join(line))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
