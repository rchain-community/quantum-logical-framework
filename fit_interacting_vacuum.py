#!/usr/bin/env python3
"""
fit_interacting_vacuum.py — fit Route 5's interacting vacuum to CMB + BAO + SN (Log2_Search.md, "Route 5 fit").

Model (Route 5 V1): vacuum (w = -1) decays into matter at Q = lambda * H_L * rho_L, with H_L/H = sqrt(Omega_L).
In N = ln a, densities in units of today's critical density:
    d rho_L/dN = -lambda sqrt(rho_L/rho_tot) rho_L
    d rho_m/dN = -3 rho_m + lambda sqrt(rho_L/rho_tot) rho_L
lambda = 0 is flat LCDM exactly. Parameters: Omega_m0, h, omega_b, lambda.

Data:
  CMB   Chen, Huang & Wang 2019 (JCAP 02, 028) distance priors, wCDM set: R, l_A, omega_b (+ correlations);
        z* from their Hu-Sugiyama fit; R uses the early-time matter density.
  BAO   DESI DR2 (arXiv:2503.14738) Table IV: BGS D_V/r_d; LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Lya D_M/r_d, D_H/r_d
        with r_{M,H}. r_d from DESI eq. (2) (Brieden, Gil-Marin & Verde 2023).
  SN    Pantheon+ (Brout et al. 2022): m_b_corr, zHD > 0.01, STAT+SYS covariance, absolute magnitude
        marginalized analytically. Downloaded to data/pantheonplus/ if missing.
Pipeline checks (run first, pre-registered): DESI BAO-only LCDM Omega_m = 0.2975 +- 0.0086, h r_d = 101.54 +- 0.73;
Pantheon+ LCDM Omega_m = 0.334 +- 0.018.

Needs numpy and scipy. Usage: python3 fit_interacting_vacuum.py [--checks-only]
"""
import math
import os
import sys
import urllib.request

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

C_KMS = 299792.458
T_CMB = 2.7255
OMEGA_R_H2 = 4.18e-5          # photons + 3.046 massless-equivalent neutrinos
OMEGA_NU_H2 = 0.00064         # one 0.06 eV neutrino, counted as matter today (Planck base)

# ---------------------------------------------------------------- data
CMB_MEAN = np.array([1.7493, 301.462, 0.02239])
CMB_SIG = np.array([0.00465, 0.0895, 0.00015])
CMB_CORR = np.array([[1.0, 0.47, -0.66], [0.47, 1.0, -0.34], [-0.66, -0.34, 1.0]])
CMB_ICOV = np.linalg.inv(CMB_CORR * np.outer(CMB_SIG, CMB_SIG))

BGS = (0.295, 7.942, 0.075)
BAO_MH = [  # z, DM/rd, sig, DH/rd, sig, r
    (0.510, 13.588, 0.167, 21.863, 0.425, -0.459),
    (0.706, 17.351, 0.177, 19.455, 0.330, -0.404),
    (0.934, 21.576, 0.152, 17.641, 0.193, -0.416),
    (1.321, 27.601, 0.318, 14.176, 0.221, -0.434),
    (1.484, 30.512, 0.760, 12.817, 0.516, -0.500),
    (2.330, 38.988, 0.531, 8.632, 0.101, -0.431),
]

HERE = os.path.dirname(os.path.abspath(__file__))
PP_DIR = os.path.join(HERE, "data", "pantheonplus")
PP_BASE = ("https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/"
           "Pantheon%2B_Data/4_DISTANCES_AND_COVAR/")
PP_FILES = {"Pantheon+SH0ES.dat": "Pantheon%2BSH0ES.dat",
            "Pantheon+SH0ES_STAT+SYS.cov": "Pantheon%2BSH0ES_STAT%2BSYS.cov"}


def load_pantheon():
    os.makedirs(PP_DIR, exist_ok=True)
    for local, remote in PP_FILES.items():
        path = os.path.join(PP_DIR, local)
        if not os.path.exists(path):
            print(f"  downloading {local} ...")
            urllib.request.urlretrieve(PP_BASE + remote, path)
    with open(os.path.join(PP_DIR, "Pantheon+SH0ES.dat")) as f:
        head = f.readline().split()
        rows = [l.split() for l in f if l.strip()]
    col = {k: i for i, k in enumerate(head)}
    zhd = np.array([float(r[col["zHD"]]) for r in rows])
    zhel = np.array([float(r[col["zHEL"]]) for r in rows])
    mb = np.array([float(r[col["m_b_corr"]]) for r in rows])
    cov = np.loadtxt(os.path.join(PP_DIR, "Pantheon+SH0ES_STAT+SYS.cov"), skiprows=1)
    n = len(rows)
    cov = cov.reshape(n, n)
    keep = zhd > 0.01
    cov = cov[np.ix_(keep, keep)]
    icov = np.linalg.inv(cov)
    return zhd[keep], zhel[keep], mb[keep], icov


# ---------------------------------------------------------------- background
class Background:
    """Solve the interacting-vacuum background backward from a = 1 to a = 1e-8."""

    def __init__(self, om0, h, lam):
        self.h = h
        orad = OMEGA_R_H2 / h ** 2
        self.orad = orad
        ol0 = 1.0 - om0 - orad
        if ol0 <= 0:
            raise ValueError("no vacuum")

        def rhs(N, y):
            rl, rm = y
            rr = orad * math.exp(-4 * N)
            tot = rl + rm + rr
            q = lam * math.sqrt(max(rl, 0.0) / tot) * rl
            return [-q, -3 * rm + q]

        N = np.linspace(0.0, math.log(1e-8), 6001)
        sol = solve_ivp(rhs, (0.0, N[-1]), [ol0, om0], t_eval=N, rtol=1e-9, atol=1e-14, method="LSODA")
        if not sol.success:
            raise ValueError("ode failed")
        self.N = N[::-1]                       # increasing
        rl, rm = sol.y[0][::-1], sol.y[1][::-1]
        a = np.exp(self.N)
        self.E = np.sqrt(rl + rm + orad / a ** 4)
        self.om_early_h2 = rm[0] * a[0] ** 3 * h ** 2   # matter a^3, early (interaction negligible there)
        # comoving distance chi(a) = (c/H0) * int_a^1 da'/(a'^2 E) = (c/H0) int_N^0 e^{-N'} dN'/E
        f = np.exp(-self.N) / self.E
        cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(self.N))])
        self.chi_from_early = cum                   # int from N[0] to N
        self.chi_total = cum[-1]

    def H_over_H0(self, z):
        return np.interp(np.log(1 / (1 + np.asarray(z))), self.N, self.E)

    def DM(self, z):  # Mpc
        c = self.chi_total - np.interp(np.log(1 / (1 + np.asarray(z))), self.N, self.chi_from_early)
        return C_KMS / (100 * self.h) * c

    def DH(self, z):
        return C_KMS / (100 * self.h) / self.H_over_H0(z)

    def rs(self, z, omb_h2):
        """Comoving sound horizon at z (Mpc), Chen et al. c_s = 1/sqrt(3(1 + R_b a))."""
        rb = 31500 * omb_h2 * (T_CMB / 2.7) ** -4
        a_end = 1 / (1 + z)
        m = self.N <= math.log(a_end)
        Nn = np.append(self.N[m], math.log(a_end))
        En = np.interp(Nn, self.N, self.E)
        an = np.exp(Nn)
        f = (1 / np.sqrt(3 * (1 + rb * an))) * np.exp(-Nn) / En
        return C_KMS / (100 * self.h) * float(np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(Nn)))


def zstar(omb, omm):
    g1 = 0.0738 * omb ** -0.238 / (1 + 39.5 * omb ** 0.763)
    g2 = 0.560 / (1 + 21.1 * omb ** 1.81)
    return 1048 * (1 + 0.00124 * omb ** -0.738) * (1 + g1 * omm ** g2)


def rd_desi(omb, ombc):
    return 147.05 * (omb / 0.02236) ** -0.13 * (ombc / 0.1432) ** -0.23


# ---------------------------------------------------------------- likelihoods
def chi2_cmb(bg, omb):
    omm = bg.om_early_h2
    zs = zstar(omb, omm)
    dm = bg.DM(zs)
    R = math.sqrt(omm) * 100 / C_KMS * dm
    la = math.pi * dm / bg.rs(zs, omb)
    d = np.array([R, la, omb]) - CMB_MEAN
    return float(d @ CMB_ICOV @ d)


def bao_model(dm_rd, dh_rd, z):
    return dm_rd(z), dh_rd(z)


def chi2_bao_from(dm_rd, dh_rd):
    z, dv, s = BGS
    dvm = (z * dm_rd(z) ** 2 * dh_rd(z)) ** (1 / 3)
    c2 = ((dvm - dv) / s) ** 2
    for z, m, sm, hh, sh, r in BAO_MH:
        d = np.array([dm_rd(z) - m, dh_rd(z) - hh])
        cov = np.array([[sm * sm, r * sm * sh], [r * sm * sh, sh * sh]])
        c2 += float(d @ np.linalg.solve(cov, d))
    return c2


def chi2_bao(bg, omb):
    rd = rd_desi(omb, bg.om_early_h2 - OMEGA_NU_H2)
    return chi2_bao_from(lambda z: float(bg.DM(z)) / rd, lambda z: float(bg.DH(z)) / rd)


SN = None


def chi2_sn(bg):
    zhd, zhel, mb, icov = SN
    dl = (1 + zhel) * bg.DM(zhd)
    mu = 5 * np.log10(dl) + 25
    d = mb - mu
    a = d @ icov @ d
    b = icov.sum(axis=0) @ d
    c = icov.sum()
    return float(a - b * b / c)


def total(theta, use=("cmb", "bao", "sn")):
    om0, h, omb, lam = theta
    if not (0.05 < om0 < 0.7 and 0.4 < h < 1.0 and 0.018 < omb < 0.027 and -5 < lam < 5):
        return 1e10
    try:
        bg = Background(om0, h, lam)
    except ValueError:
        return 1e10
    c = 0.0
    if "cmb" in use:
        c += chi2_cmb(bg, omb)
    if "bao" in use:
        c += chi2_bao(bg, omb)
    if "sn" in use:
        c += chi2_sn(bg)
    return c


def fit(fun, starts):
    best = None
    for s in starts:
        r = minimize(fun, s, method="Nelder-Mead",
                     options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 8000, "maxfev": 12000})
        if best is None or r.fun < best.fun:
            best = r
    return best


# ---------------------------------------------------------------- checks
def lcdm_E(om, z):
    return math.sqrt(om * (1 + z) ** 3 + 1 - om)


def check_bao_only():
    """DESI: flat LCDM, BAO alone, free Omega_m and h*r_d (radiation negligible)."""
    def chi(p):
        om, hrd = p
        if not 0.1 < om < 0.6:
            return 1e10
        def dc(z):
            zz = np.linspace(0, z, 400)
            return float(np.trapezoid(1 / np.array([lcdm_E(om, x) for x in zz]), zz))
        k = C_KMS / 100 / hrd
        return chi2_bao_from(lambda z: k * dc(z), lambda z: k / lcdm_E(om, z))
    r = fit(chi, [[0.30, 101.5], [0.33, 100.0]])
    # 1-sigma from the curvature of chi2 along Omega_m (profiled over h r_d)
    def prof(om):
        return minimize(lambda x: chi([om, x[0]]), [r.x[1]], method="Nelder-Mead").fun
    lo = r.x[0]
    for step in np.linspace(0, 0.05, 501):
        if prof(r.x[0] - step) - r.fun > 1:
            lo = r.x[0] - step
            break
    return r.x, r.x[0] - lo


def check_sn_only():
    def chi(p):
        om = p[0]
        if not 0.05 < om < 0.7:
            return 1e10
        return chi2_sn(Background(om, 0.7, 0.0))
    r = fit(chi, [[0.30], [0.35]])
    lo = r.x[0]
    for step in np.linspace(0, 0.06, 601):
        if chi([r.x[0] - step]) - r.fun > 1:
            lo = r.x[0] - step
            break
    return r.x[0], r.x[0] - lo


def main():
    global SN
    print("Interacting vacuum fit — Log2_Search.md (Route 5 fit)\n")
    SN = load_pantheon()
    print(f"  Pantheon+: {len(SN[0])} SNe with zHD > 0.01\n")

    (om_b, hrd_b), s_b = check_bao_only()
    ok_b = abs(om_b - 0.2975) <= 0.0086 and abs(hrd_b - 101.54) <= 0.73
    print(f"Check A, DESI BAO-only LCDM: Omega_m = {om_b:.4f} +- {s_b:.4f} (0.2975 +- 0.0086), "
          f"h r_d = {hrd_b:.2f} (101.54 +- 0.73) -> {'pass' if ok_b else 'FAIL'}")
    om_s, s_s = check_sn_only()
    ok_s = abs(om_s - 0.334) <= 0.018
    print(f"Check B, Pantheon+ LCDM:     Omega_m = {om_s:.4f} +- {s_s:.4f} (0.334 +- 0.018) -> "
          f"{'pass' if ok_s else 'FAIL'}")
    if not (ok_b and ok_s):
        print("\nA pipeline check failed: stopping before the model fit (pre-registered rule).")
        return
    if "--checks-only" in sys.argv:
        return

    starts_l = [[0.31, 0.68, 0.0224, 0.0], [0.30, 0.69, 0.0224, 0.0], [0.32, 0.67, 0.0223, 0.0]]
    for label, use in (("CMB + BAO + SN", ("cmb", "bao", "sn")), ("CMB + BAO", ("cmb", "bao"))):
        print(f"\n=== {label}")
        fl = fit(lambda t: total([t[0], t[1], t[2], 0.0], use), [s[:3] for s in starts_l])
        fi = fit(lambda t: total(t, use),
                 [[fl.x[0], fl.x[1], fl.x[2], l0] for l0 in (-0.5, 0.0, 0.5, 1.0)])
        print(f"  LCDM (lambda = 0): chi2 = {fl.fun:.2f}  Omega_m = {fl.x[0]:.4f}  h = {fl.x[1]:.4f}  "
              f"omega_b = {fl.x[2]:.5f}")
        print(f"  interacting:       chi2 = {fi.fun:.2f}  Omega_m = {fi.x[0]:.4f}  h = {fi.x[1]:.4f}  "
              f"omega_b = {fi.x[2]:.5f}  lambda = {fi.x[3]:+.3f}")
        print(f"  Delta chi2 (LCDM - interacting) = {fl.fun - fi.fun:.2f}  (1 extra parameter)")

        def prof(lam):
            r = fit(lambda t: total([t[0], t[1], t[2], lam], use), [fi.x[:3], fl.x[:3]])
            return r.fun
        grid = sorted(set([round(x, 3) for x in np.linspace(fi.x[3] - 1.5, fi.x[3] + 1.5, 13)] + [0.0, 1.0, 1.106]))
        prof_vals = {lam: prof(lam) - fi.fun for lam in grid}
        print("  profile Delta chi2(lambda):")
        for lam in grid:
            tag = "  <- LCDM" if lam == 0.0 else ("  <- lambda = 1 (Omega* = 0.718)" if lam == 1.0 else
                  ("  <- lambda = 1.106 (Omega* = log 2)" if lam == 1.106 else ""))
            print(f"    lambda = {lam:+.3f}: {prof_vals[lam]:7.2f}{tag}")
        inside = [l for l, v in prof_vals.items() if v <= 1.0]
        inside95 = [l for l, v in prof_vals.items() if v <= 3.84]
        print(f"  68% range (grid): [{min(inside):+.3f}, {max(inside):+.3f}]   95%: [{min(inside95):+.3f}, {max(inside95):+.3f}]")


if __name__ == "__main__":
    main()
