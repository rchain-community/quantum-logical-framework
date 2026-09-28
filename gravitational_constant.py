#!/usr/bin/env python3
"""
gravitational_constant.py -- G reduced to one number, and that number tested.

THE QUESTION (Jim, 2026-09-28): "can we now make progress on the gravitational constant?"

WHERE G STANDS. The structural G = L_P^2 c^3/hbar is derived (QLF_GravityFromDelay); the SI number is a unit
convention. The physics is how weak gravity is, alpha_G = G m_p^2/(hbar c) = (m_p/M_Pl)^2, and QLF derives
it from dimensional transmutation, ln(M_Pl/m_p) = 2 pi/(b0 alpha_s), with b0 = 7 (QLF_BetaFunction) and the
posit alpha_s(substrate) = 1/b0^2 (QLF_AlphaS): ln = 14 pi, alpha_G = exp(-28 pi) (QLF_GravitationalCoupling),
0.068 % on the log, 6.2 % on the value.

  sec 0  PRE-REGISTRATION -- predictions fixed before sec 2 was run.
  sec 1  G IS ONE NUMBER: measured G fixes 1/alpha_s(substrate) exactly -- 49 + a residual.
  sec 2  the continuum check: run the measured alpha_s(M_Z) to the Planck mass (1, 2, 3 loops, top
         threshold) and compare with what G requires.
  sec 3  the census-tail transfer: does alpha's census machinery, at alpha_s's bare coupling 1/49,
         bracket the residual? (computed while scoping -- disclosed, not blind)
  sec 4  verdict and scope.

Run:  python3 gravitational_constant.py
"""
from __future__ import annotations

import math

PREREGISTRATION = """
PRE-REGISTRATION (fixed in the commit that adds this file, before sec 2 was run).

  G1  (exact inference, no prediction) Measured G and m_p fix the substrate coupling the 14 pi route needs:
      1/alpha_s(substrate) = 7 ln(M_Pl/m_p) / (2 pi) = 49 + delta. G is equivalent to this one number.

  G2  (the continuum check -- a real test) Run alpha_s(M_Z) = 0.1180 +- 0.0009 (PDG) up to the (non-reduced)
      Planck mass in MS-bar at 1, 2 and 3 loops, n_f = 5 -> 6 at the top threshold. Let sigma be the
      propagated alpha_s(M_Z) uncertainty plus the spread between 2- and 3-loop. PREDICTION: the result is
      NOT within 3 sigma of the value G requires. I.e. the posit alpha_s = 1/b0^2 is a structural
      identification, not the MS-bar coupling at the Planck mass, and standard running does not close G.
      If it IS within 3 sigma, record that as support for the posit.

  G3  (census-tail transfer -- NOT blind) Alpha's census tail (irreducible and total closure tails at the
      bare coupling), transplanted to alpha_s with bare coupling 1/49, gives a bracket for delta. Its ends
      were computed while scoping this file (about 0.043 and 0.131), so this is recorded, not predicted:
      the bracket excludes delta, and the naive transfer fails, as the proton cross-test found for the
      1/2 mix (Alpha_Residual.md sec 9o).

  G4  (observation, not a claim) delta is close to alpha's residual 0.036. Close numbers are not evidence
      (Alpha_Residual.md sec 9k); it is recorded with that warning.
"""

HBAR, C, G, G_ERR = 1.054571817e-34, 299792458.0, 6.67430e-11, 0.00015e-11
M_P_KG = 1.67262192595e-27                          # proton mass
GEV = 1.602176634e-10                                # J per GeV
MZ, MT = 91.1876, 172.57                              # GeV
AS_MZ, AS_ERR = 0.1180, 0.0009


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def planck_mass_gev() -> float:
    return math.sqrt(HBAR * C / G) * C ** 2 / GEV


def sec1() -> float:
    rule("sec 1  G IS ONE NUMBER")
    mpl_kg = math.sqrt(HBAR * C / G)
    L = math.log(mpl_kg / M_P_KG)
    inv = 7 * L / (2 * math.pi)
    d_inv = 7 * (0.5 * G_ERR / G) / (2 * math.pi)
    aG = G * M_P_KG ** 2 / (HBAR * C)
    print(f"""
  ln(M_Pl/m_p) measured           {L:.9f}      14 pi = {14 * math.pi:.9f}   (diff {L - 14 * math.pi:+.6f})
  alpha_G measured                {aG:.6e}   exp(-28 pi) = {math.exp(-28 * math.pi):.6e}  ({math.exp(-28 * math.pi) / aG - 1:+.2%})

  So the 14 pi route reproduces measured G exactly when
      1/alpha_s(substrate) = 7 ln(M_Pl/m_p)/(2 pi) = {inv:.8f}  +- {d_inv:.1e} (from G's own uncertainty)
                           = 49 + {inv - 49:.6f}

  G, alpha_G and the proton's absolute depth are one number: the substrate strong coupling, b0^2 = 49
  plus a residual of {inv - 49:+.4f} -- the same shape as alpha^-1 = 137 + 0.036.""")
    return inv


def run_alpha_s(mu_to: float, loops: int, as_mz: float) -> float:
    """MS-bar running of alpha_s from M_Z upward, n_f = 5 below the top, 6 above (continuous matching)."""
    def beta(a: float, nf: int) -> float:              # d alpha / d ln mu
        b0 = 11 - 2 * nf / 3
        b1 = 102 - 38 * nf / 3
        b2 = 2857 / 2 - 5033 * nf / 18 + 325 * nf ** 2 / 54
        x = a / (4 * math.pi)                          # a = alpha_s/(4 pi):  dx/dln mu^2 = -b0 x^2 - b1 x^3 - b2 x^4
        dx = -b0 * x ** 2 - (b1 * x ** 3 if loops >= 2 else 0) - (b2 * x ** 4 if loops >= 3 else 0)
        return 2 * 4 * math.pi * dx
    a, t = as_mz, math.log(MZ)
    for t_end, nf in ((math.log(MT), 5), (math.log(mu_to), 6)):
        n = 20000
        h = (t_end - t) / n
        for _ in range(n):
            k1 = beta(a, nf)
            k2 = beta(a + h * k1 / 2, nf)
            k3 = beta(a + h * k2 / 2, nf)
            k4 = beta(a + h * k3, nf)
            a += h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t = t_end
    return a


def sec2(target: float) -> bool:
    rule("sec 2  THE CONTINUUM CHECK: MEASURED alpha_s RUN TO THE PLANCK MASS")
    mpl = planck_mass_gev()
    vals = {L: 1 / run_alpha_s(mpl, L, AS_MZ) for L in (1, 2, 3)}
    up = 1 / run_alpha_s(mpl, 3, AS_MZ + AS_ERR)
    dn = 1 / run_alpha_s(mpl, 3, AS_MZ - AS_ERR)
    sig_in = abs(up - dn) / 2
    sig_ord = abs(vals[3] - vals[2])
    sigma = math.hypot(sig_in, sig_ord)
    dev = (vals[3] - target) / sigma
    within = abs(dev) <= 3
    print(f"""
  M_Pl = {mpl:.5e} GeV (non-reduced, the convention the 14 pi match uses)

  1/alpha_s(M_Pl), MS-bar, from alpha_s(M_Z) = {AS_MZ}:
      1 loop   {vals[1]:.4f}
      2 loop   {vals[2]:.4f}
      3 loop   {vals[3]:.4f}
  uncertainty: from alpha_s(M_Z) +- {AS_ERR}  {sig_in:.4f};  2- vs 3-loop  {sig_ord:.4f};  combined sigma {sigma:.4f}

  G requires            {target:.4f}
  3-loop minus required {vals[3] - target:+.4f}  = {dev:+.1f} sigma
  the posit's own b0^2  49 -> 3-loop minus 49 = {vals[3] - 49:+.4f}

  G2 prediction (NOT within 3 sigma): {'HELD' if not within else 'FAILED -- the posit is supported; record it'}""")
    return within


def census_tail_bracket(x: float) -> tuple[float, float]:
    """Alpha's census tails at bare coupling x: (1/x) x [sum_{n>=2} count(n) x^n], irreducible and total."""
    tot = 1 / math.sqrt(1 - 4 * x) - 1 - 2 * x
    irr = (1 - math.sqrt(1 - 4 * x)) - 2 * x
    return irr / x, tot / x


def sec3(target: float) -> None:
    rule("sec 3  THE CENSUS-TAIL TRANSFER (NOT BLIND -- COMPUTED WHILE SCOPING)")
    lo, hi = census_tail_bracket(1 / 49)
    a_lo, a_hi = census_tail_bracket(1 / 128)
    d = target - 49
    print(f"""
  alpha:    bare coupling 1/128, tail bracket [{a_lo:.6f}, {a_hi:.6f}], residual 0.036 -- inside
  alpha_s:  bare coupling 1/49,  tail bracket [{lo:.6f}, {hi:.6f}], residual {d:.6f} -- {'inside' if lo <= d <= hi else 'OUTSIDE (below the irreducible end)' if d < lo else 'OUTSIDE (above)'}

  The machinery that brackets alpha's residual does not bracket alpha_s's: transplanted naively, it fails,
  as the 1/2 mix failed on the proton (Alpha_Residual.md sec 9o). Recorded; it was not a blind prediction.""")


def verdict(within: bool, target: float) -> None:
    rule("sec 4  VERDICT AND SCOPE")
    print(f"""
  PROGRESS, stated plainly:
    * G is reduced to one number, exactly: 1/alpha_s(substrate) = {target:.5f}. Everything open about G
      (and alpha_G, and the proton's absolute depth) is the residual {target - 49:+.4f} on the posit b0^2 = 49.
    * The continuum check {'SUPPORTS' if within else 'does NOT support'} identifying that coupling with MS-bar alpha_s
      at the Planck mass, at the precision G needs (sec 2).
    * alpha's census-tail machinery does not transfer to it (sec 3).
  G4 (observation only): the residual {target - 49:.4f} sits near alpha's 0.036 (ratio {(target - 49) / 0.036:.3f}). Close numbers
  are not evidence; a shared mechanism would have to predict the ratio, and none is proposed here.

  Scope: nothing is fitted; no axiom added; the 14 pi route (QLF_AlphaS, QLF_GravitationalCoupling) is used as
  it stands. The MS-bar identification in sec 2 is itself an assumption: the substrate coupling need not be
  the MS-bar one, and the one-loop transmutation formula has no scheme.""")


def main() -> None:
    print(__doc__)
    rule("sec 0  PRE-REGISTRATION")
    print(PREREGISTRATION)
    target = sec1()
    within = sec2(target)
    sec3(target)
    verdict(within, target)


if __name__ == "__main__":
    main()
