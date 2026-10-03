#!/usr/bin/env python3
"""
singlet_gluon.py -- the singlet gluon of the product rule against torsion balances
(Carbon_Superconductivity.md sec 33; frozen in commit 164cfbd).

R_prod's ninth gluon T0 = I/sqrt(6) couples g_s/sqrt(6) per quark, 3 g_s/sqrt(6) per nucleon: V = (3/2) alpha_1 hbar c / r.
Relative to gravity per atomic mass unit (the convention of the torsion-balance Yukawa V = alpha G (q/mu)1 (q/mu)2
m1 m2 / r): alpha_tilde = (3/2) alpha_1 hbar c / (G m_u^2).

Bound: Schlamminger et al., PRL 100, 041101 (2008), arXiv:0712.0607 (the fallback in the data rule: neither paper
states the infinite-range baryon bound as a number in its text, so it is derived from the stated eta and B/mu).
"""
from math import log10

G, HBAR, C, M_U = 6.67430e-11, 1.054571817e-34, 2.99792458e8, 1.66053906660e-27

ETA, ETA_ERR = 0.3e-13, 1.8e-13            # eta(Be-Ti), Eq. (2), 1 sigma
B_MU_BE, B_MU_TI = 0.99868, 1.001077       # stated in the text
B_MU_EARTH = 1.0                            # approximation; Earth's B/mu is within 0.2 % of 1


def main():
    grav = G * M_U ** 2 / (HBAR * C)
    print(f"G m_u^2 / (hbar c) = {grav:.3e}")
    dq = B_MU_BE - B_MU_TI
    bound = (abs(ETA) + 1.96 * ETA_ERR) / (abs(dq) * B_MU_EARTH)
    print(f"Delta(B/mu)_Be-Ti = {dq:+.6f};  95% bound |alpha_tilde| <= {bound:.2e}  (infinite range, source = Earth)")
    for name, a1 in (("alpha_s(M_Z) = 0.118", 0.118), ("alpha_1 = 1e-3", 1e-3)):
        pred = 1.5 * a1 / grav
        print(f"{name:22}: predicted alpha_tilde = {pred:.2e};  excluded by {log10(pred / bound):.1f} orders")
    print("\nVerdict: R_prod's singlet gluon is EXCLUDED for both alpha_1 (the frozen rule).")
    print("Note: alpha_tilde ~ 1e35-1e37 > 1 would also make nucleons repel far more strongly than gravity binds them.")


if __name__ == "__main__":
    main()
