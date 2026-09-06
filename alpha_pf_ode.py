#!/usr/bin/env python3
"""
pf_ode.py — Project 2b, step 1: the Picard–Fuchs ODE for Q(x) = Σ A039699(n) xⁿ
(the 4-D hypercubic lattice Green's function g.f. = the QLF closure-return g.f.),
verified against the exact transfer-recursion terms, then its local exponents at
every singular point — the "resonant frequency" structure per Jim.

ODE (Bradley Klee, OEIS A039699, Aug 2018):  Σ_{j=0..4} P_j(x)·G^(j)(x) = 0
  P_0 = −8 + 768 x
  P_1 = 1 − 424 x + 14592 x²
  P_2 = 7 x − 1172 x² + 25344 x³
  P_3 = 6 x² − 640 x³ + 10240 x⁴
  P_4 = x³ − 80 x⁴ + 1024 x⁵           = x³·1024·(x − 1/16)(x − 1/64)

Singular points:  x = 0 (from x³),  x = 1/16,  x = 1/64,  x = ∞.
"""
from __future__ import annotations
from fractions import Fraction as F
from collections import defaultdict

# ------- exact A039699 via transfer recursion (returns, revisits allowed) -----
_STEPS4 = [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),
           (0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1)]

def A039699(n_max: int):
    R = n_max
    ret = {0: 1}
    live = {(0,0,0,0): 1}
    for step in range(1, 2*n_max+1):
        nxt = defaultdict(int)
        for (a,b,c,d), m in live.items():
            for da,db,dc,dd in _STEPS4:
                p = (a+da,b+db,c+dc,d+dd)
                if abs(p[0])+abs(p[1])+abs(p[2])+abs(p[3]) <= R:
                    nxt[p] += m
        live = nxt
        if step % 2 == 0:
            ret[step//2] = live.get((0,0,0,0), 0)
    return [ret[n] for n in range(n_max+1)]

# ------- polynomials as dict {power: Fraction} --------------------------------
def padd(p, q):
    r = defaultdict(F)
    for k,v in p.items(): r[k]+=v
    for k,v in q.items(): r[k]+=v
    return {k:v for k,v in r.items() if v!=0}

def pscale(p, s):
    return {k: v*s for k,v in p.items() if v*s != 0}

def pshift(p, d):   # multiply by x^d
    return {k+d: v for k,v in p.items()}

P = {
    0: {0:F(-8), 1:F(768)},
    1: {0:F(1), 1:F(-424), 2:F(14592)},
    2: {1:F(7), 2:F(-1172), 3:F(25344)},
    3: {2:F(6), 3:F(-640), 4:F(10240)},
    4: {3:F(1), 4:F(-80), 5:F(1024)},
}

# ------- 1. verify the ODE on the exact power series ------------------------
def verify_ode(a, upto):
    """a[n] = A039699(n).  Check Σ_j P_j(x) G^(j)(x) = 0 coefficient-wise."""
    N = len(a)
    # G^(j) has x^m coefficient  a[m+j] * (m+j)!/m!
    def deriv_coeff(m, j):
        if m + j >= N: return None
        c = a[m+j]
        for t in range(j): c *= (m+1+t)
        return F(c)
    bad = []
    for m in range(upto):
        tot = F(0)
        ok = True
        for j in range(5):
            for k, ck in P[j].items():
                mm = m - k
                if mm < 0: continue
                dc = deriv_coeff(mm, j)
                if dc is None: ok = False; break
                tot += ck * dc
            if not ok: break
        if ok and tot != 0:
            bad.append((m, tot))
    return bad

# ------- 2. verify the scalar recurrence -----------------------------------
def verify_recurrence(a):
    bad = []
    for n in range(2, len(a)):
        lhs = (256*(n-1)**2*(2*n-3)*(2*n-1)*a[n-2]
               - 4*(2*n-1)**2*(5*n*n-5*n+2)*a[n-1]
               + n**4*a[n])
        if lhs != 0: bad.append(n)
    return bad

# ------- 3. indicial equation at a finite singular point x_c ---------------
def indicial_finite(xc):
    """Shift x = xc + s, expand P_j(xc+s) as a poly in s, then substitute
    G ~ s^ρ (so G^(j) ~ ρ^{underline j} s^{ρ-j}) and collect the lowest power
    of s.  Returns (L, indicial_poly_coeffs_in_rho) with poly as {deg: coeff}."""
    # P_j(xc + s):  binomial expand
    Q = {}
    for j, poly in P.items():
        q = defaultdict(F)
        for k, ck in poly.items():
            # (xc+s)^k = Σ_i C(k,i) xc^{k-i} s^i
            from math import comb
            for i in range(k+1):
                q[i] += ck * comb(k, i) * (F(xc)**(k-i))
        Q[j] = {k:v for k,v in q.items() if v != 0}
    # lowest s-power contributed by term j is  (min power of Q[j]) - j
    def lowpow(poly): return min(poly) if poly else 10**9
    L = min(lowpow(Q[j]) - j for j in range(5) if Q[j])
    # coefficient of s^{ρ+L}: sum over j of  [coeff of s^{L+j} in Q[j]] * fallfact(ρ, j)
    # fallfact(ρ,j) = ρ(ρ-1)...(ρ-j+1)  -> polynomial in ρ
    def fallfact(j):
        poly = {0: F(1)}
        for t in range(j):
            newp = defaultdict(F)
            for d,c in poly.items():
                newp[d+1] += c
                newp[d]   += c*(-t)
            poly = {d:c for d,c in newp.items() if c != 0}
        return poly
    ind = defaultdict(F)
    for j in range(5):
        need = L + j
        c = Q[j].get(need, F(0))
        if c == 0: continue
        for d, cc in fallfact(j).items():
            ind[d] += c * cc
    return L, {d:c for d,c in ind.items() if c != 0}

def indicial_infinity():
    """x = 1/w, expand near w = 0.  d/dx = -w^2 d/dw.
    Instead: exponents at infinity ρ_∞ are roots of the indicial poly of the
    transformed operator; easiest is the Fuchs relation cross-check plus a
    direct series test G ~ x^{-ρ}."""
    # Direct: substitute G = x^{-ρ}; G^(j) = (-ρ)(-ρ-1)...(-ρ-j+1) x^{-ρ-j}
    #  P_j(x) ~ leading term  lead_j x^{deg_j}  as x->∞
    # term j contributes  lead_j * risingfact * x^{deg_j - ρ - j}
    # highest power of x:  max_j (deg_j - j).
    lead = {j: P[j][max(P[j])] for j in range(5)}
    deg  = {j: max(P[j]) for j in range(5)}
    H = max(deg[j] - j for j in range(5))
    def pochneg(j):   # (-ρ)(-ρ-1)...(-ρ-j+1) as poly in ρ
        poly = {0: F(1)}
        for t in range(j):
            newp = defaultdict(F)
            for d,c in poly.items():
                newp[d+1] += -c            # * (-ρ ...) ; -ρ - t
                newp[d]   += c*(-t)
            poly = {d:c for d,c in newp.items() if c != 0}
        return poly
    ind = defaultdict(F)
    for j in range(5):
        if deg[j] - j != H: continue
        for d,cc in pochneg(j).items():
            ind[d] += lead[j]*cc
    return H, {d:c for d,c in ind.items() if c != 0}

def roots_of(poly, tries=200):
    """Rational/real roots of a small poly {deg:coeff}; integer/simple-rational
    first, then numeric."""
    if not poly: return []
    deg = max(poly)
    # numeric via companion-ish: just scan + Newton for a quartic max
    import cmath
    coeffs = [complex(poly.get(deg-i, 0)) for i in range(deg+1)]
    # Durand–Kerner
    n = deg
    if n == 0: return []
    roots = [ (0.4+0.9j)**k for k in range(n) ]
    for _ in range(500):
        new = []
        for i in range(n):
            num = sum(c*roots[i]**(n-k) for k,c in enumerate(coeffs))
            den = coeffs[0]
            for j in range(n):
                if j!=i: den *= (roots[i]-roots[j])
            new.append(roots[i] - num/den)
        roots = new
    out = []
    for r in roots:
        rr = r.real
        out.append(round(rr,6) if abs(r.imag)<1e-6 else complex(round(r.real,6),round(r.imag,6)))
    return sorted(out, key=lambda z: (z.real if isinstance(z,complex) else z))

# ---------------------------------------------------------------------------
def main():
    NM = 20
    print(__doc__)
    print("="*78)
    a = A039699(NM)
    print("A039699(0..10):", a[:11])
    OK = [1,8,168,5120,190120,7939008,357713664,16993726464,839358285480]
    print("OEIS match (first 9):", a[:9] == OK)

    print("\n1. ODE verification on the exact series:")
    bad = verify_ode(a, NM-6)
    print(f"   Σ_j P_j(x) G^(j) = 0  for coefficients 0..{NM-7}:",
          "PASS" if not bad else f"FAIL {bad[:3]}")

    print("\n2. scalar recurrence verification:")
    br = verify_recurrence(a)
    print(f"   256(n-1)²(2n-3)(2n-1)a(n-2) − 4(2n-1)²(5n²-5n+2)a(n-1) + n⁴a(n) = 0:",
          "PASS" if not br else f"FAIL at n={br[:3]}")

    print("\n3. local exponents (indicial roots) — the resonance structure")
    print("-"*78)
    for xc, name in [(F(0), "x = 0   (empty-history / MUM end)"),
                     (F(1,64), "x = 1/64  (4-axis threshold — physical return point)"),
                     (F(1,16), "x = 1/16  (2-axis pseudo-threshold)")]:
        L, ind = indicial_finite(xc)
        rts = roots_of(ind)
        print(f"  {name}")
        print(f"     indicial poly in ρ (deg {max(ind)}): {dict(sorted(ind.items(), reverse=True))}")
        print(f"     exponents ρ: {rts}")
        # resonance = integer differences
        reals = sorted(r for r in rts if not isinstance(r, complex))
        diffs = [round(reals[i+1]-reals[i],6) for i in range(len(reals)-1)]
        res = any(abs(d-round(d))<1e-6 for d in diffs)
        print(f"     consecutive gaps: {diffs}  ->  {'RESONANT (log solutions / Jordan block)' if res else 'non-resonant'}")
        print()

    H, indinf = indicial_infinity()
    rts = roots_of(indinf)
    print(f"  x = ∞")
    print(f"     indicial poly in ρ: {dict(sorted(indinf.items(), reverse=True))}")
    print(f"     exponents ρ (G ~ x^(-ρ)): {rts}")
    print()

    # Fuchs relation cross-check: sum of all exponents = (n(n-1)/2)(p-2), n=4,p=4 -> 12
    print("-"*78)
    print("  Fuchs relation: Σ(all exponents over all sing. pts) should be 12  (n=4, p=4)")
    tot = F(0)
    for xc in (F(0), F(1,64), F(1,16)):
        _, ind = indicial_finite(xc)
        d = max(ind)
        # sum of roots = -c_{d-1}/c_d
        tot += -ind.get(d-1, F(0)) / ind[d]
    _, indinf = indicial_infinity()
    d = max(indinf)
    tot += -indinf.get(d-1, F(0)) / indinf[d]
    print(f"  computed Σ = {tot}   ({'OK' if tot == 12 else 'MISMATCH'})")

    print("\n" + "="*78)
    print("READ: x=0 is a MUM point (all exponents equal -> nilpotent monodromy of")
    print("maximal order, the Calabi–Yau 'large complex structure' end). x=1/64 and")
    print("x=1/16 carry the resonant (integer-spaced) exponents whose log solution IS")
    print("the running logarithm — the d=4 marginal signature, now read off the ODE.")

    step3(a)


def step3(a):
    """Step 3: the conifold connection constant at x = 1/64, vs the QED coefficients.
    Q(x) = A + B·(1−64x)·log(1−64x) + analytic  near the conifold; B is exact from
    the tail asymptotic A039699(n) ~ 64ⁿ·κ/n² and Σ(κ/n²)yⁿ = κ·Li₂(y):
        B = κ = 2/π² = 1/(3ζ(2))          (Q, probability level)
        B_P = κ(1−p)²   for P = 1 − 1/Q   (first-return level)"""
    from math import pi
    print("\n" + "="*78)
    print("STEP 3 — conifold connection constant at x = 1/64\n")
    kappa = 2/pi**2
    print(f"  B = κ = 2/π² = 1/(3ζ(2)) = {kappa:.10f}     [EXACT; κ·ζ(2) = 1/3]")
    print("  numeric check  A039699(n)·n²/64ⁿ → κ :  "
          + "  ".join(f"n{n}:{a[n]*n*n/64.0**n:.5f}" for n in (8,10,12,14) if n < len(a)))
    A = 1.2394671218                       # Glasser–Guttmann C₀ = Q(1/64)
    p = 1 - 1/A
    B_P = kappa*(1-p)**2
    print(f"  A = Q(1/64) = {A:.8f} (Glasser–Guttmann),  p = 1−1/A = {p:.8f}")
    print(f"  B_P = κ(1−p)² = {B_P:.10f}\n")
    qed1 = 2/(3*pi)
    print(f"  QED one-loop log coeff 2/(3π) = {qed1:.10f}")
    print(f"    B  /(2/3π) = 3/π           = {kappa/qed1:.8f}   (transcendental)")
    print(f"    B_P/(2/3π) = 3(1−p)²/π     = {B_P/qed1:.8f}   (≈ §2a w — the flagged near-miss)")
    print(f"    B  /(−0.328479 two-loop)   = {kappa/-0.328478965579:.5f}   (not clean)")
    print("\n  VERDICT: B is exact and π-EVEN (1/π², from the 4-D Gaussian (2π)^{d/2}).")
    print("  The QED coefficient 2/(3π) is π-ODD.  B = c·(2/3π) ⇒ c = 3/π, transcendental.")
    print("  Q(x) is a probability-level object (Σ |amp|² returns); its periods are π-even.")
    print("  The coefficient lives at amplitude level, where route (a)'s C(2n,n) census —")
    print("  with its √π signature C(2n,n) ~ 4ⁿ/√(πn) — correctly gives 2/(3π) = (4/π)(1/6).")
    print("  ⇒ route (b) forces the log's EXISTENCE and ORIGIN, not its COEFFICIENT. CLOSED.")


if __name__ == "__main__":
    main()
