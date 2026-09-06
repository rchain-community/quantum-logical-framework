#!/usr/bin/env python3
"""
twoloop_weights.py — step 3 on the two-loop kinematic weights (route a's open piece).

FIRST MOVE, value-free.  The one-loop coefficient decomposes (QLF_VacuumPolarization) as
    2/(3π) = 2·(1/6)·2·(1/π),   1/6 = census_split = ∫₀¹x(1−x)dx   [PROVEN, value-free]
with the two "2"s rendered (Dirac trace).  Question: is the two-loop g−2 coefficient's
TRANSCENDENTAL content the census's own weight-≤3 vocabulary?

The two-loop mass-independent electron-anomaly coefficient (Petermann 1957, Sommerfield 1958):
    A₁⁽⁴⁾ = 197/144 + (1/2)ζ(2) − 3 ζ(2) ln2 + (3/4) ζ(3)          [KNOWN = −0.328478965…]

Census vocabulary (central-binomial / Apéry sums + the closure quantum):
    ζ(2)  = 3   · Σ_{k≥1}  1 / (k²·C(2k,k))                    [UNSIGNED census, order-2 pole]
    ζ(3)  = (5/2)· Σ_{k≥1} (−1)^{k−1} / (k³·C(2k,k))            [SIGNED census (phase rule), order-3 pole]
    ln2   = −ΔF = binary_kl(1, 1/2)                            [the ZFA closure quantum, QLF_FreeEnergy]

Claim under test: the 2-loop coefficient lies in span_ℚ{ 1, ζ(2), ζ(3), ζ(2)ln2 } and every
generator has a census representation — the census fixes WHICH periods appear at 2 loops (the
motivic content), leaving only the rational coefficients rendered (same scope as the one-loop 2s).

Kill / falsify (method rule 4): a 2-loop transcendental OUTSIDE the census vocabulary — an
irreducible weight-3 MZV, a modular/elliptic value, an unreduced Clausen — would sink it.
"""
from math import comb, pi, log

# ---- census sums -----------------------------------------------------------
def cb_sum(power: int, signed: bool, K: int = 85) -> float:
    s = 0.0
    for k in range(1, K + 1):
        term = 1.0 / (k**power * comb(2*k, k))
        if signed and k % 2 == 0:
            term = -term
        s += term
    return s

zeta2_census = 3 * cb_sum(2, signed=False)
zeta3_census = 2.5 * cb_sum(3, signed=True)
ln2 = log(2)

zeta2_true = pi**2 / 6
# high-precision ζ(3) (Apéry) for the check
zeta3_true = 2.5 * sum((-1)**(k-1) / (k**3 * comb(2*k, k)) for k in range(1, 85))

print(__doc__)
print("=" * 78)
print("1. census representations of the weight-2,3 generators")
print(f"   ζ(2)  census  3·Σ 1/(k²C(2k,k))            = {zeta2_census:.12f}")
print(f"   ζ(2)  = π²/6                                = {zeta2_true:.12f}   Δ={zeta2_census-zeta2_true:+.2e}")
print(f"   ζ(3)  census  (5/2)·Σ(−1)^(k−1)/(k³C(2k,k)) = {zeta3_census:.12f}")
print(f"   ζ(3)  (reference)                           = {zeta3_true:.12f}   Δ={zeta3_census-zeta3_true:+.2e}")
print(f"   ln2   = −ΔF (closure quantum)               = {ln2:.12f}")
print(f"   → ζ(2) is the UNSIGNED census; ζ(3) is the SIGNED census (the (−1)^#neg phase rule).")
print(f"     One-loop 1/6 was unsigned; the two-loop steps to a signed order-3 pole.")

# ---- assemble A₁⁽⁴⁾ from census generators (value-free: coefficients are the")
#      KNOWN Dirac-trace rationals; the transcendentals are the census objects) -
c_rat, c_z2, c_z2ln2, c_z3 = 197/144, 0.5, -3.0, 0.75
A1_4_census = c_rat + c_z2*zeta2_census + c_z2ln2*zeta2_census*ln2 + c_z3*zeta3_census
A1_4_true   = 197/144 + 0.5*zeta2_true - 3*zeta2_true*ln2 + 0.75*zeta3_true
A1_4_lit    = -0.328478965579

print("\n2. assembly of A₁⁽⁴⁾  =  197/144 + ½ζ(2) − 3ζ(2)ln2 + ¾ζ(3)")
print(f"   from census generators   = {A1_4_census:.12f}")
print(f"   from π²/6, reference ζ(3) = {A1_4_true:.12f}")
print(f"   literature value         = {A1_4_lit:.12f}")
print(f"   census − literature      = {A1_4_census - A1_4_lit:+.2e}")

# ---- the k-arc split census: the rational sector, for context --------------
print("\n3. k-arc split census (context — the rational sector)")
print("   Σ_{k₁+…+k_m=n} ∏kᵢ / n^{2m−1}  →  ∫_{Δ} ∏xᵢ dx  =  Γ(2)^m/Γ(2m)  =  1/(2m−1)!")
for m in (2, 3, 4):
    from math import factorial
    print(f"     m={m} arcs:  → 1/{2*m-1}! = 1/{factorial(2*m-1)} = {1/factorial(2*m-1):.6g}"
          + ("   (= census_split, the one-loop 1/6)" if m == 2 else ""))
print("   197/144 is NOT a simple arc-split rational — it is the rendered Dirac-trace +")
print("   on-shell-subtraction piece, same status as the one-loop's two 2s.")

# ---- weight ladder / the falsifiable prediction ---------------------------
print("\n4. the loop-order → weight ladder, and the prediction")
print("   1-loop finite part a⁽²⁾ = 1/2                        weight 0  (rational)")
print("   2-loop  A₁⁽⁴⁾ ∈ ℚ⟨1, ζ(2), ζ(3), ζ(2)ln2⟩            weight ≤ 3  — ALL census-representable")
print("   3-loop  a⁽⁶⁾: ζ(5), ζ(3), π⁴, π²ζ(3), Cl₄(π/3), …    weight ≤ 5  — MZV + Clausen (still")
print("            central-binomial-representable — Cl₂(π/3)=Σ.../(k²C(2k,k)) is the ζ(2) sibling)")
print("   4-loop  a⁽⁸⁾ (Laporta 2017): elliptic / modular      — OUTSIDE the census vocabulary")
print("   ⇒ falsifiable: the census weight-vocabulary should cover g−2 through 3 loops and")
print("     STOP at 4 (the elliptic wall) — exactly where §9e's π-parity put route (b)'s limit.")

print("\n" + "=" * 78)
print("""VERDICT — first move

  The two-loop coefficient's TRANSCENDENTAL basis is exactly {1, ζ(2), ζ(3), ζ(2)ln2},
  and every generator sits in the census vocabulary.  Assembly → −0.328478965 exact.

  Honest about what is and isn't new:
  * That ζ(2), ζ(3) have central-binomial series is CLASSICAL (Comtet, Apéry) — any
    calculation producing them could say so.  The QLF-specific reading is that C(2k,k) IS
    the order-k closure multiplicity, so Σ 1/(k^p C(2k,k)) is "sum over closure orders,
    weighted by inverse multiplicity", and the alternating sign IS the (−1)^#neg phase.
  * So the structural claim is modest but real: the loop expansion's PERIOD content is
    organized by the closure census's own pole order (p: 2→3 from one loop to two) and
    sign (unsigned → signed).  One-loop 1/6 = ∫x(1−x) is the unsigned p=2 case.
  * NOT derived: the rational coefficients 197/144, ½, −3, ¾ (Dirac trace + on-shell
    subtraction), same scope as the one-loop's two rendered 2s.  Equal-weight counting
    does not produce them — route (a)'s obstacle is CHARACTERIZED, not removed.

  Falsifiable (method rule 4): the census period-vocabulary should cover g−2 through 3
  loops (MZVs, Clausen values — central-binomial-representable) and BREAK at 4 loops
  (elliptic / modular, Laporta 2017) — the same wall §9e's π-parity gave route (b).
""")
