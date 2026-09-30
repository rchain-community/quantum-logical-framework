import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_LightBending — relatively slower light near mass bends it twice as much as clocks alone would

A denser vacuum near mass has relatively slower light; locally light always moves at `c`. In a weak field,
with the isotropic metric `ds² = −A c²dt² + B (dx² + dy² + dz²)`, `φ = Φ/c²` and `A = 1 + 2φ`, the
coordinate speed of light squared is `A/B` and clocks run at `√A`. Statements B1–B3 were pre-registered in
`GR_Schwarzschild.md` §4a (commit `b30b7a2`) before this proof was written.

* B1 `event_quantum_light_speed`: if space and time rescale together (the event quantum, `B = 1/A`), the
  coordinate light speed is exactly `1 + 2φ`: slope 2 (`event_quantum_light_first_order`), twice the clock
  rate's slope 1 (`clock_rate_first_order`). In PPN language, `γ = 1`.
* B2 `latency_only_light_speed_sq`: if only time is slowed (`B = 1`), light speed squared equals the clock
  rate squared: light is slowed exactly as much as clocks (Einstein's 1911 half value).
* B3 `deflection_integral`: the transverse-gradient integral along a straight ray at impact parameter `b`,
  `∫_{−L}^{L} b dz/(b² + z²)^{3/2} = 2L/(b√(b² + L²))`, which tends to `2/b`. So a ray through
  `n = 1 − kφ` with `φ = −GM/(rc²)` is deflected by `α = k·2GM/(bc²)`.

The factor 2 rests on the event-quantum premise (`Kitada_Local_Time_GR.md` §5.3), not derived here. The
limit `L → ∞` of B3 is elementary and stated, not formalized. No new axioms.
-/

namespace QLF.LightBending

/-- The coordinate speed of light squared, `A/B`, for the isotropic weak-field metric. -/
noncomputable def lightSpeedSq (A B : ℝ) : ℝ := A / B

/-! ### B1 and B2: light slowed twice as much as clocks, or equally -/

/-- **B1 (squared).** With the event quantum, `B = 1/A`, the light speed squared is `A²`. -/
theorem event_quantum_light_speed_sq (φ : ℝ) :
    lightSpeedSq (1 + 2 * φ) (1 / (1 + 2 * φ)) = (1 + 2 * φ) ^ 2 := by
  unfold lightSpeedSq
  rw [div_div_eq_mul_div, div_one]
  ring

/-- **B1.** With the event quantum, the coordinate light speed is exactly `1 + 2φ`. -/
theorem event_quantum_light_speed {φ : ℝ} (h : 0 ≤ 1 + 2 * φ) :
    Real.sqrt (lightSpeedSq (1 + 2 * φ) (1 / (1 + 2 * φ))) = 1 + 2 * φ := by
  rw [event_quantum_light_speed_sq, Real.sqrt_sq h]

/-- **B2.** Latency only (`B = 1`): the light speed squared equals the clock rate squared, `1 + 2φ`. -/
theorem latency_only_light_speed_sq (φ : ℝ) : lightSpeedSq (1 + 2 * φ) 1 = 1 + 2 * φ := by
  unfold lightSpeedSq
  rw [div_one]

/-- The clock rate `√(1 + 2φ)` has slope 1 at `φ = 0`: clocks slow by `φ`. -/
theorem clock_rate_first_order : HasDerivAt (fun φ : ℝ => Real.sqrt (1 + 2 * φ)) 1 0 := by
  have h1 : HasDerivAt (fun φ : ℝ => 1 + 2 * φ) 2 0 := by
    simpa using ((hasDerivAt_id (0 : ℝ)).const_mul 2).const_add 1
  have h2 := h1.sqrt (by norm_num)
  simpa using h2

/-- With the event quantum the light speed `1 + 2φ` has slope 2: light slows by `2φ`. -/
theorem event_quantum_light_first_order : HasDerivAt (fun φ : ℝ => 1 + 2 * φ) 2 0 := by
  simpa using ((hasDerivAt_id (0 : ℝ)).const_mul 2).const_add 1

/-- **Light is slowed twice as much as clocks** under the event quantum: slopes 2 and 1. -/
theorem light_slowed_twice_clock :
    HasDerivAt (fun φ : ℝ => 1 + 2 * φ) 2 0 ∧
    HasDerivAt (fun φ : ℝ => Real.sqrt (1 + 2 * φ)) 1 0 :=
  ⟨event_quantum_light_first_order, clock_rate_first_order⟩

/-! ### B3: the deflection integral -/

/-- The antiderivative `F(z) = z/(b√(b² + z²))`. -/
noncomputable def deflF (b z : ℝ) : ℝ := z / (b * Real.sqrt (b ^ 2 + z ^ 2))

/-- The transverse-gradient integrand `b/(b² + z²)^{3/2}`, written without `rpow`. -/
noncomputable def deflIntegrand (b z : ℝ) : ℝ := b / ((b ^ 2 + z ^ 2) * Real.sqrt (b ^ 2 + z ^ 2))

/-- The algebra behind `F′`, with `r = √(b² + z²)` given by `r² = b² + z²`. -/
theorem deflF_deriv_value {b z r : ℝ} (hb : 0 < b) (hr : 0 < r) (hrs : r ^ 2 = b ^ 2 + z ^ 2) :
    (1 * (b * r) - z * (b * (2 * z / (2 * r)))) / (b * r) ^ 2 = b / ((b ^ 2 + z ^ 2) * r) := by
  have hb' : b ≠ 0 := hb.ne'
  have hr' : r ≠ 0 := hr.ne'
  have hz : z ^ 2 = r ^ 2 - b ^ 2 := by linarith
  rw [← hrs]
  field_simp
  ring_nf
  rw [hz]
  ring

/-- `F′ = b/(b² + z²)^{3/2}`. -/
theorem deflF_hasDerivAt {b : ℝ} (hb : 0 < b) (z : ℝ) :
    HasDerivAt (deflF b) (deflIntegrand b z) z := by
  have hs : 0 < b ^ 2 + z ^ 2 := add_pos_of_pos_of_nonneg (pow_pos hb 2) (sq_nonneg z)
  have hsq : 0 < Real.sqrt (b ^ 2 + z ^ 2) := Real.sqrt_pos.mpr hs
  have hin : HasDerivAt (fun y : ℝ => b ^ 2 + y ^ 2) (2 * z) z := by
    simpa using ((hasDerivAt_id z).pow 2).const_add (b ^ 2)
  have hroot := hin.sqrt hs.ne'
  have hden := hroot.const_mul b
  have hq := (hasDerivAt_id z).div hden (mul_pos hb hsq).ne'
  rw [show deflIntegrand b z = _ from
    (deflF_deriv_value hb hsq (Real.sq_sqrt hs.le)).symm]
  exact hq

/-- The integrand is continuous for `b > 0`. -/
theorem continuous_deflIntegrand {b : ℝ} (hb : 0 < b) : Continuous (deflIntegrand b) := by
  have h1 : Continuous fun z : ℝ => b ^ 2 + z ^ 2 := continuous_const.add (continuous_pow 2)
  unfold deflIntegrand
  apply Continuous.div continuous_const
  · exact h1.mul (Real.continuous_sqrt.comp h1)
  · intro z
    have hs : 0 < b ^ 2 + z ^ 2 := add_pos_of_pos_of_nonneg (pow_pos hb 2) (sq_nonneg z)
    exact (mul_pos hs (Real.sqrt_pos.mpr hs)).ne'

/-- **B3 — the deflection integral.** `∫_{−L}^{L} b/(b² + z²)^{3/2} dz = 2L/(b√(b² + L²))`, which tends
    to `2/b` as `L → ∞`. With `n = 1 − kφ`, `φ = −GM/(rc²)`, the deflection is `α = k·2GM/(bc²)`. -/
theorem deflection_integral {b : ℝ} (hb : 0 < b) (L : ℝ) :
    ∫ z in (-L)..L, deflIntegrand b z = 2 * L / (b * Real.sqrt (b ^ 2 + L ^ 2)) := by
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (fun z _ => deflF_hasDerivAt hb z)
    ((continuous_deflIntegrand hb).intervalIntegrable _ _)]
  unfold deflF
  rw [neg_sq]
  ring

/-- **Established:** B1–B3 of `GR_Schwarzschild.md` §4a. Under the event quantum light is slowed twice
    as much as clocks (`light_slowed_twice_clock`), giving `γ = 1` and the full deflection
    `α = 4GM/(bc²)` (`deflection_integral`); latency alone slows light only as much as clocks
    (`latency_only_light_speed_sq`), which gives half. -/
theorem light_bending_summary {φ : ℝ} (h : 0 ≤ 1 + 2 * φ) :
    Real.sqrt (lightSpeedSq (1 + 2 * φ) (1 / (1 + 2 * φ))) = 1 + 2 * φ ∧
    lightSpeedSq (1 + 2 * φ) 1 = 1 + 2 * φ :=
  ⟨event_quantum_light_speed h, latency_only_light_speed_sq φ⟩

end QLF.LightBending
