"""
Koide's relation applied to neutrino masses, and the pre-registered predictions in
Lepton_Generations_Fourier.md section 6.

Inputs are the measured oscillation splittings only (NuFIT 5.x central values):
    dm21 = 7.42e-5 eV^2, |dm31| = 2.51e-3 eV^2, sin^2(th12) = 0.304, sin^2(th13) = 0.0222.
The lightest mass m_lightest is scanned; Q = sum(m) / (sum(s))^2 with s_k = +-sqrt(m_k).

Findings:
  * all signs positive: Q never reaches 2/3 (max 0.584 normal, 0.499 inverted ordering);
  * one negative sqrt (on m1, the Majorana sign): Q = 2/3 has a solution;
  * if only nu1 is Majorana, the neutrinoless double-beta mass is m_bb = |U_e1|^2 m1.
"""
import numpy as np

def brentq(f, a, b, it=200):
    fa = f(a)
    for _ in range(it):
        c = 0.5 * (a + b); fc = f(c)
        if np.sign(fc) == np.sign(fa): a, fa = c, fc
        else: b = c
    return 0.5 * (a + b)

DM21, DM31 = 7.42e-5, 2.51e-3
S12, S13 = 0.304, 0.0222
UE1 = (1 - S12) * (1 - S13)          # |U_e1|^2

def masses(ml, ordering):
    if ordering == "NO":
        return np.array([ml, np.sqrt(ml**2 + DM21), np.sqrt(ml**2 + DM31)])
    m3 = ml
    m1 = np.sqrt(ml**2 + DM31)
    return np.array([m1, np.sqrt(m1**2 + DM21), m3])

def Q(m, signs):
    s = np.array(signs) * np.sqrt(m)
    return m.sum() / s.sum() ** 2

if __name__ == "__main__":
    grid = np.logspace(-7, -0.5, 4000)
    for o in ("NO", "IO"):
        print(f"{o}: max Q with all signs positive = {max(Q(masses(x, o), (1, 1, 1)) for x in grid):.3f}")
    for o, signs in (("NO", (-1, 1, 1)), ("IO", (1, 1, -1))):
        f = lambda x: Q(masses(x, o), signs) - 2 / 3
        vals = [f(x) for x in grid]
        roots = [brentq(f, grid[i], grid[i + 1]) for i in range(len(grid) - 1)
                 if np.sign(vals[i]) != np.sign(vals[i + 1]) and np.isfinite(vals[i]) and abs(vals[i]) < 1]
        for r in roots:
            m = masses(r, o)
            print(f"{o} signs {signs}: m = {np.round(m*1e3, 2)} meV, sum = {m.sum():.4f} eV")
            if o == "NO":
                print(f"   nu1-only Majorana: m_bb = |U_e1|^2 m1 = {UE1:.3f} x {m[0]*1e3:.2f} = {UE1*m[0]*1e3:.2f} meV")
