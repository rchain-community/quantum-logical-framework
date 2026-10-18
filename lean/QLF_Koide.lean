/-
QLF_Koide.lean — the Koide invariant Q = 2/3 from the closure structure.

The empirical Koide relation among the charged-lepton masses,

    Q = (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  2/3   (to 0.0009%),

is exactly equivalent to writing the three √-masses as three balanced phases of
a common amplitude:  √m_k = M(1 + A·c_k),  k = 0,1,2, where the c_k carry the
three-fold 120° structure (Σc_k = 0, Σc_k² = 3/2) and A is the amplitude.

A short algebraic fact (proved below) is that for THIS structure

    Q = (1 + A²/2) / N,            (N = number of balanced phases).

HONEST SCOPE (2026-10-18 correction). This form restricts nothing: ANY three
positive numbers can be written as √m_k = M(1 + A·cos(δ + 2πk/3)) — it is the
discrete Fourier transform over the three generations (one constant mode M,
one harmonic of amplitude A·M and phase δ). So `r² = 2` is not an input that
FORCES Q = 2/3; it IS Q = 2/3 in Fourier coordinates. `koide_three_phase_iff`
proves the equivalence in both directions. Earlier text here called Q = 2/3
"forced by the two transverse axes"; that reading is an identification, not a
derivation, and the per-axis version of it (equal power per axis) gives Q = 1.

The basis-free content is `koide_iff_equal_power`: Q = 2/3 holds exactly when
the √-mass vector's constant (generation-blind) part and its varying
(generation-distinguishing) part carry EQUAL power — equivalently the √-mass
vector sits at 45° to (1,1,1) (Foot 1994). Measured ratio 0.99998. Why nature
splits the power 50/50 is the open question. Koide (1981–83) found the
relation; Brannen (2006) the phase δ ≈ 2/9. See Lepton_Generations_Fourier.md
and Weak_Force.md §5b–§5c⁗.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.LinearCombination

namespace QLF

/-- **Koide identity from three balanced phases of amplitude √2.**
    With `sₖ = M(1 + r cₖ)` (the √-masses), `r² = 2` (amplitude √2 — the two
    transverse axes), and the three-fold balanced-phase structure
    `Σcₖ = 0`, `Σcₖ² = 3/2` (three axes 120° apart), the Koide combination
    satisfies `3·Σsₖ² = 2·(Σsₖ)²` — independent of the scale `M` and the
    overall phase. This is the algebraic content of `Q = 2/3`. -/
theorem koide_three_phase (M r c0 c1 c2 : ℝ)
    (hr : r ^ 2 = 2) (hsum : c0 + c1 + c2 = 0) (hsq : c0 ^ 2 + c1 ^ 2 + c2 ^ 2 = 3 / 2) :
    3 * ((M * (1 + r * c0)) ^ 2 + (M * (1 + r * c1)) ^ 2 + (M * (1 + r * c2)) ^ 2)
      = 2 * ((M * (1 + r * c0)) + (M * (1 + r * c1)) + (M * (1 + r * c2))) ^ 2 := by
  linear_combination (M ^ 2 * (-6 * r - 2 * r ^ 2 * (c0 + c1 + c2))) * hsum
    + (3 * M ^ 2 * r ^ 2) * hsq + (9 / 2 * M ^ 2) * hr

/-- **Q = 2/3.** Dividing the identity by `(Σsₖ)² ≠ 0`, the Koide ratio is
    exactly `2/3` — forced by `N = 3` (three axes) and `A² = 2` (two transverse
    axes). -/
theorem koide_two_thirds (M r c0 c1 c2 : ℝ)
    (hr : r ^ 2 = 2) (hsum : c0 + c1 + c2 = 0) (hsq : c0 ^ 2 + c1 ^ 2 + c2 ^ 2 = 3 / 2)
    (hS : (M * (1 + r * c0)) + (M * (1 + r * c1)) + (M * (1 + r * c2)) ≠ 0) :
    ((M * (1 + r * c0)) ^ 2 + (M * (1 + r * c1)) ^ 2 + (M * (1 + r * c2)) ^ 2)
      / ((M * (1 + r * c0)) + (M * (1 + r * c1)) + (M * (1 + r * c2))) ^ 2 = 2 / 3 := by
  rw [div_eq_iff (pow_ne_zero 2 hS)]
  linear_combination (1 / 3 : ℝ) * koide_three_phase M r c0 c1 c2 hr hsum hsq

/-- **The amplitude hypothesis is the conclusion.** Under the balanced-phase
    structure and `M ≠ 0`, the Koide identity holds IFF `r² = 2`. So `r² = 2`
    restates `Q = 2/3` in Fourier coordinates rather than deriving it. -/
theorem koide_three_phase_iff (M r c0 c1 c2 : ℝ) (hM : M ≠ 0)
    (hsum : c0 + c1 + c2 = 0) (hsq : c0 ^ 2 + c1 ^ 2 + c2 ^ 2 = 3 / 2) :
    3 * ((M * (1 + r * c0)) ^ 2 + (M * (1 + r * c1)) ^ 2 + (M * (1 + r * c2)) ^ 2)
      = 2 * ((M * (1 + r * c0)) + (M * (1 + r * c1)) + (M * (1 + r * c2))) ^ 2
    ↔ r ^ 2 = 2 := by
  have key : 3 * ((M * (1 + r * c0)) ^ 2 + (M * (1 + r * c1)) ^ 2 + (M * (1 + r * c2)) ^ 2)
      - 2 * ((M * (1 + r * c0)) + (M * (1 + r * c1)) + (M * (1 + r * c2))) ^ 2
      = M ^ 2 * (9 / 2) * (r ^ 2 - 2) := by
    linear_combination (-6 * r * M ^ 2 - 2 * r ^ 2 * M ^ 2 * (c0 + c1 + c2)) * hsum
      + (3 * r ^ 2 * M ^ 2) * hsq
  constructor
  · intro h
    have h0 : M ^ 2 * (9 / 2) * (r ^ 2 - 2) = 0 := by linear_combination h - key
    have hM2 : M ^ 2 * (9 / 2) ≠ 0 := mul_ne_zero (pow_ne_zero 2 hM) (by norm_num)
    have h1 := (mul_eq_zero.mp h0).resolve_left hM2
    linear_combination h1
  · intro hr
    exact koide_three_phase M r c0 c1 c2 hr hsum hsq

/-- **Koide as a power balance (basis-free).** For any three reals `sₖ` (the
    √-masses), `3·Σs² = 2·(Σs)²` — i.e. `Q = 2/3` — holds iff the power in the
    varying part, `Σs² − (Σs)²/3`, equals the power in the constant part,
    `(Σs)²/3`. Equal power in the generation-blind and generation-distinguishing
    Fourier modes; equivalently a 45° angle between the √-mass vector and
    `(1,1,1)`. No phase structure is assumed. -/
theorem koide_iff_equal_power (s0 s1 s2 : ℝ) :
    3 * (s0 ^ 2 + s1 ^ 2 + s2 ^ 2) = 2 * (s0 + s1 + s2) ^ 2
    ↔ (s0 ^ 2 + s1 ^ 2 + s2 ^ 2) - (s0 + s1 + s2) ^ 2 / 3 = (s0 + s1 + s2) ^ 2 / 3 := by
  constructor
  · intro h; linear_combination h / 3
  · intro h; linear_combination 3 * h

/-- The three-fold balanced-phase hypotheses are satisfiable (non-vacuous):
    the `δ = 0` representative `(c₀,c₁,c₂) = (1, −1/2, −1/2)` (the `cos(2πk/3)`
    values) has `Σc = 0` and `Σc² = 3/2`. -/
theorem koide_phase_witness :
    (1 : ℝ) + (-1 / 2) + (-1 / 2) = 0 ∧ (1 : ℝ) ^ 2 + (-1 / 2) ^ 2 + (-1 / 2) ^ 2 = 3 / 2 := by
  norm_num

end QLF
