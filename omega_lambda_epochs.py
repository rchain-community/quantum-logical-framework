"""
omega_lambda_epochs.py -- what QLF's rho_Lambda does at early epochs, three readings.

Companion to Cosmological_Constant.md sec 5.7 and Curvature.md sec 8a (the named tension).
Pure Python, no numpy.

QLF's vacuum density is rho_Lambda = (3 log 2 / 8 pi) c^4 / (G L^2) with L a horizon length.
In holographic-dark-energy notation (Li 2004) that is rho = 3 C^2 M_p^2 / L^2 with C^2 = log 2.
Which horizon L is, and whether the vacuum exchanges energy with matter, decides the history:

  A. L = Hubble radius c/H, matter conserved separately (the doc's literal reading).
     Then rho_Lambda / rho_crit = log 2 at every epoch and rho_Lambda redshifts like the
     dominant component: w_eff = 0 in the matter era. No acceleration (Hsu 2004).
  B. L = Hubble radius, but the vacuum keeps w = -1 (QLF_CosmicInflation: w = -1) and
     exchanges energy with matter to hold the fraction at log 2. Then H^2 ~ a^{-3(1-log 2)},
     one power law for all time: accelerating today, but never a matter-dominated era.
  C. L = future event horizon (Li 2004), same prefactor C^2 = log 2. Omega_de is no longer
     fixed; it is integrated, and today's value is set to log 2 (the QLF number). Early
     dark energy then falls away on its own.

Inputs held fixed: log 2 (QLF), Omega_r0 = 9.1e-5 (photons + 3 massless nu, h = 0.674),
T0 = 2.7255 K. Reference: Planck 2018 LCDM, Omega_m = 0.315, CMB shift parameter
R = sqrt(Omega_m) * int_0^z* dz/E = 1.7502 +/- 0.0046 (Chen, Huang, Wang 2019).
The shift parameter here is a rough screen, not a likelihood.
"""
import math

LOG2 = math.log(2.0)
C = math.sqrt(LOG2)           # HDE parameter implied by the QLF prefactor
OMR0 = 9.1e-5
Z_STAR = 1089.9
Z_BBN = 1.0e6 * 1.160451812e4 / 2.7255 - 1   # T = 1 MeV
N_NU_EQ = 7.0 / 4.0                           # g* per massless neutrino species at BBN
G_STAR_BBN = 10.75


def rk4(f, y, x0, x1, n):
    h = (x1 - x0) / n
    x = x0
    out = [(x, y)]
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2, [a + h / 2 * b for a, b in zip(y, k1)])
        k3 = f(x + h / 2, [a + h / 2 * b for a, b in zip(y, k2)])
        k4 = f(x + h, [a + h * b for a, b in zip(y, k3)])
        y = [a + h / 6 * (p + 2 * q + 2 * r + s) for a, p, q, r, s in zip(y, k1, k2, k3, k4)]
        x += h
        out.append((x, y))
    return out


def hde_event_horizon(omega0):
    """Integrate y = (Omega_de, ln E) in x = ln a, from today back to BBN."""
    def f(x, y):
        om, lnE = y
        om = min(max(om, 0.0), 1.0)
        a = math.exp(x)
        omr = OMR0 / (a ** 4 * math.exp(2 * lnE))
        w_de = -1.0 / 3.0 - 2.0 * math.sqrt(om) / (3.0 * C)
        dlnE = -1.5 * (1.0 + w_de * om + omr / 3.0)
        dom = om * (-2.0 * (1.0 - math.sqrt(om) / C) - 2.0 * dlnE)
        return [dom, dlnE]
    x_end = -math.log(1 + Z_BBN) - 0.5
    return rk4(f, [omega0, 0.0], 0.0, x_end, 40000)


def interp(track, z):
    x = -math.log(1 + z)
    for (x1, y1), (x2, y2) in zip(track, track[1:]):
        if x2 <= x <= x1:
            t = (x - x1) / (x2 - x1)
            return [a + t * (b - a) for a, b in zip(y1, y2)]
    raise ValueError(z)


def shift_R(E_of_z, omm0, zmax=Z_STAR, n=20000):
    # integrate in ln(1+z) for accuracy
    u1 = math.log(1 + zmax)
    h = u1 / n
    s = 0.0
    for i in range(n + 1):
        u = i * h
        z = math.exp(u) - 1
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * (1 + z) / E_of_z(z)
    return math.sqrt(omm0) * s * h / 3


def delta_neff(frac):
    """Extra non-relativistic-free energy fraction at BBN, as an equivalent Delta N_eff."""
    return frac / (1 - frac) * G_STAR_BBN / N_NU_EQ


def main():
    print("QLF Omega_Lambda across epochs: three readings of rho ~ log2 / L^2")
    print(f"  C^2 = log 2 = {LOG2:.4f}, C = {C:.4f}\n")

    # LCDM reference
    omm_l = 0.315
    E_l = lambda z: math.sqrt(omm_l * (1 + z) ** 3 + OMR0 * (1 + z) ** 4 + (1 - omm_l - OMR0))
    print(f"LCDM (Planck 2018)   R = {shift_R(E_l, omm_l):.4f}   (measured 1.7502 +/- 0.0046)\n")

    # A
    omm_a = 1 - LOG2
    print("A. Hubble horizon, matter conserved")
    print(f"   Omega_Lambda = {LOG2:.3f} at z = 0, {Z_STAR:.0f}, BBN (by construction)")
    print("   w_eff = 0 in matter era  ->  q0 = +0.50 (observed q0 ~ -0.55): no acceleration")
    print(f"   BBN: H boosted x{(1 - LOG2) ** -0.5:.2f}, equivalent Delta N_eff = {delta_neff(LOG2):.1f}"
          "  (bound ~0.3)\n")

    # B
    p = 3 * (1 - LOG2)          # H^2 ~ a^-p
    q0 = p / 2 - 1
    print("B. Hubble horizon, w = -1 with exchange")
    print(f"   H^2 ~ a^-{p:.3f} at all epochs;  q0 = {q0:+.2f} today, but also q = {q0:+.2f} at z = 2")
    print(f"   (LCDM: q(z=2) = {0.5 * (omm_l * 27 - 2 * (1 - omm_l)) / (omm_l * 27 + 1 - omm_l):+.2f}); "
          f"age = {2 / p:.2f}/H0 = {2 / p * 977.8 / 67.4:.1f} Gyr")
    print(f"   Omega_Lambda = {LOG2:.3f} at recombination and BBN (same Delta N_eff = {delta_neff(LOG2):.1f})\n")

    # C
    tr = hde_event_horizon(LOG2)
    om_rec, lnE_rec = interp(tr, Z_STAR)
    om_bbn, _ = interp(tr, Z_BBN)
    om_z2, _ = interp(tr, 2.0)
    E_c = lambda z: math.exp(interp(tr, z)[1])
    omm_c = 1 - LOG2 - OMR0
    w0 = -1 / 3 - 2 * math.sqrt(LOG2) / (3 * C)
    # deceleration-to-acceleration redshift
    zt = None
    prev = None
    for z in [i * 0.005 for i in range(1, 600)]:
        om, lnE = interp(tr, z)
        a = 1 / (1 + z)
        omr = OMR0 / (a ** 4 * math.exp(2 * lnE))
        w_de = -1 / 3 - 2 * math.sqrt(om) / (3 * C)
        qz = 0.5 * (1 + 3 * (w_de * om + omr / 3))
        if prev is not None and prev < 0 <= qz:
            zt = z
            break
        prev = qz
    print("C. Future event horizon, same prefactor, Omega_de(today) = log 2")
    print(f"   w0 = {w0:+.3f}  (= -1 exactly, because sqrt(Omega0) = C when Omega0 = C^2 = log 2)")
    print(f"   Omega_de: z=2 {om_z2:.3f}, recombination {om_rec:.2e}, BBN {om_bbn:.1e}")
    print(f"   BBN equivalent Delta N_eff = {delta_neff(om_bbn):.1e};  deceleration->acceleration at z ~ {zt}")
    print(f"   shift parameter R = {shift_R(E_c, omm_c):.4f}  (screen only; Omega_m h^2 not refit)")
    print()
    print("A '0.035-0.04 ripple' on log 2 moves Omega_Lambda by ~0.025; readings A and B need it")
    print("reduced by >10x at recombination and at BBN. Reading C removes the early problem with no ripple.")


if __name__ == "__main__":
    main()
