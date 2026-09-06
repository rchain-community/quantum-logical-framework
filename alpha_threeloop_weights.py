#!/usr/bin/env python3
"""
threeloop_weights.py — is the 3-loop g−2 coefficient's transcendental basis
census-representable?  (continuation of §9f; value-free)

Laporta–Remiddi 1996, the mass-independent electron anomaly at α³ (72 diagrams):

  A₁⁽⁶⁾ = 28259/5184
          + (17101/810) π²
          − (298/9) π² ln2
          + (139/18) ζ(3)
          − (239/2160) π⁴
          + (83/72) π² ζ(3)
          − (215/24) ζ(5)
          + (100/3) [ Li₄(1/2) + (1/24) ln⁴2 − (1/24) π² ln²2 ]
        ≈ 1.181241456587

Census vocabulary (substrate-motivated):
  ζ(p) even  : Comtet central-binomial series  Σ 1/(k^p C(2k,k))          [inverse multiplicity]
  ζ(3)       : Apéry signed series (−1)^{k−1}/(k³ C(2k,k))                 [the phase rule]
  ln2        : −ΔF, the ZFA closure quantum
  Li_p(1/2)  : Σ 2^{−k}/k^p = Σ e^{kΔF}/k^p                               [free-energy weight]
  ζ(5)       : ??? — the test.  No single central-binomial sum gives ζ(5).

Question: is every A₁⁽⁶⁾ constant in ℚ⟨ census generators ⟩, and if ζ(5) needs a
NESTED central-binomial sum, does that nesting = the closure/sub-closure (Russian-doll)
structure — i.e. does census nesting-depth track loop order?
"""
from math import comb, pi, log

def S(power, signed, K=90, inner=0):
    """Σ_{k≥1} w_k / (k^power C(2k,k)),  w_k = (−1)^{k−1} if signed,
    times H^{(inner)}_{k−1} = Σ_{j<k} 1/j^inner  if inner>0."""
    tot = 0.0
    for k in range(1, K + 1):
        t = 1.0 / (k**power * comb(2*k, k))
        if signed and k % 2 == 0:
            t = -t
        if inner:
            t *= sum(1.0/j**inner for j in range(1, k))
        tot += t
    return tot

ln2 = log(2)
z2 = pi**2/6
z3 = 1.2020569031595942854
z4 = pi**4/90
z5 = 1.0369277551433699263
Li4half = sum(0.5**k / k**4 for k in range(1, 200))

print(__doc__)
print("=" * 78)
print("1. census representations — verify each generator\n")

z2_c = 3 * S(2, False)
z3_c = 2.5 * S(3, True)
z4_c = (36/17) * S(4, False)
# Borwein–Bradley:  ζ(5) = 2 Σ(−1)^{k−1}/(k⁵C) − (5/2) Σ(−1)^{k−1} H^{(2)}_{k−1}/(k³C)
z5_c = 2 * S(5, True) - 2.5 * S(3, True, inner=2)

for name, cen, ref in [("ζ(2) = 3·Σ 1/(k²C)", z2_c, z2),
                       ("ζ(3) = (5/2)·Σ(−1)^(k−1)/(k³C)  [Apéry, signed]", z3_c, z3),
                       ("ζ(4) = (36/17)·Σ 1/(k⁴C)  [Comtet]", z4_c, z4),
                       ("ζ(5) = 2·Σ(−1)^(k−1)/(k⁵C) − (5/2)·Σ(−1)^(k−1)H²_{k−1}/(k³C)", z5_c, z5)]:
    ok = abs(cen - ref) < 1e-9
    print(f"   {name}")
    print(f"        census = {cen:.12f}   ref = {ref:.12f}   {'OK' if ok else 'MISMATCH Δ=%.2e'%(cen-ref)}")
print(f"   Li₄(1/2) = Σ 2^(−k)/k⁴ = Σ e^(kΔF)/k⁴ = {Li4half:.12f}   [free-energy weighted; census]")
print(f"   ln2 = −ΔF = {ln2:.12f}   ;  ln⁴2, π²ln²2 = 6ζ(2)ln²2 : products of census generators")

print("\n2. classify every A₁⁽⁶⁾ constant\n")
rows = [
 ("28259/5184",        0, "rational (order counting)",                     "census (wt 0)"),
 ("π² = 6ζ(2)",         2, "3·Σ 1/(k²C)",                                   "census, single sum"),
 ("ζ(3)",               3, "(5/2)·Σ(−1)^(k−1)/(k³C)",                       "census, single sum + phase"),
 ("π²ln2 = 6ζ(2)ln2",   3, "ζ(2)-sum × (−ΔF)",                              "census, product"),
 ("π⁴ = 90ζ(4)",        4, "(36/17)·Σ 1/(k⁴C)",                             "census, single sum"),
 ("Li₄(1/2)",           4, "Σ 2^(−k)/k⁴ = Σ e^(kΔF)/k⁴",                    "census, free-energy weight"),
 ("ln⁴2 = (−ΔF)⁴",      4, "closure quantum^4",                             "census, product"),
 ("π²ln²2 = 6ζ(2)ln²2", 4, "ζ(2)-sum × (−ΔF)²",                             "census, product"),
 ("π²ζ(3) = 6ζ(2)ζ(3)", 5, "ζ(2)-sum × ζ(3)-sum",                           "census, product"),
 ("ζ(5)",               5, "2·Σ(−1)^(k−1)/(k⁵C) − (5/2)·Σ(−1)^(k−1)H²_{k−1}/(k³C)",
                            "census, NESTED sum (sub-closure)"),
]
for c, wt, rep, verdict in rows:
    print(f"   wt {wt}  {c:<20} = {rep:<52} → {verdict}")

# assemble
A6_census = (28259/5184
             + (17101/810)*(6*z2_c)
             - (298/9)*(6*z2_c)*ln2
             + (139/18)*z3_c
             - (239/2160)*(90*z4_c)
             + (83/72)*(6*z2_c)*z3_c
             - (215/24)*z5_c
             + (100/3)*(Li4half + (1/24)*ln2**4 - (1/24)*(6*z2_c)*ln2**2))
A6_lit = 1.181241456587
print(f"\n3. assembly from census generators = {A6_census:.10f}")
print(f"   Laporta–Remiddi value            = {A6_lit:.10f}")
print(f"   census − literature              = {A6_census - A6_lit:+.2e}")

print("\n" + "=" * 78)
print("""VERDICT — 3-loop g−2

  Every A₁⁽⁶⁾ constant is census-representable.  BUT the vocabulary must extend with
  loop order:
    1 loop  →  single unsigned sum        (1/6 = ∫x(1−x), pole order 2)
    2 loops →  single sum + phase          (ζ(3), signed, pole order 3)
    3 loops →  NESTED sums + free-energy weight
               · ζ(5) needs Σ(−1)^{k−1} H^{(2)}_{k−1} / (k³ C(2k,k)) — a central-binomial
                 MZV, i.e. a closure weighted by a sum over its SUB-closures (Russian doll,
                 the IsDiagram nesting clause).
               · Li₄(1/2) = Σ e^{kΔF}/k⁴ needs the closure free-energy weight 2^{−k}.

  So census NESTING DEPTH tracks LOOP ORDER — a sharper form of §9f's prediction.
  The rational coefficients (28259/5184, 17101/810, …) stay rendered, as before.

  4-loop wall unchanged: elliptic/modular periods (Laporta 2017) are NOT central-binomial
  MZVs at any nesting depth — a different motive.  Two independent lines (this + §9e
  π-parity) put the census boundary at 4-loop QED.
""")
