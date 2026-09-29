import QLF_InflationObserver
import QLF_HolographicDensity
import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_DeSitterCount — counting on the de Sitter horizon forces the prefactor to 1

`Cosmological_Constant.md` §5.7 excludes every *evolving* horizon for `ρ_Λ = 3 log 2 · M_p²/L²`. This module
proves the no-go for the natural *fixed* horizon, the final de Sitter radius, and locates where §3's `log 2`
comes from. Statements D1–D4 were pre-registered in `Cosmological_Constant.md` §5.8 (commit `e3d4df5`)
before this proof was written.

* D1 `desitter_count_ratio`: on `R = c/H`, §3's density is `log 2 × ρ_crit(H)`.
* D2 `selfconsistent_iff_unit_prefactor`: a counted density `p · ρ_crit` is self-consistent de Sitter iff
  `p = 1`. This is algebra (bookkeeping by `CLAUDE.md` rule 4), stated as the anchor. The content is the
  identification of the counted horizon with the de Sitter horizon.
* D3 `qlf_count_not_selfconsistent`: QLF's count is not, because `log 2 ≠ 1` (`log_two_lt_one`).
* D4 `section3_energy_eq_log_two_mul_bh` and `bh_energy_eq_desitter_energy` (Planck units): §3's horizon
  energy is `log 2 × S_BH · T_dS`, and `S_BH · T_dS = ρ_dS · V = R/2` on `R = 1/H`. So §3's `log 2` is the
  per-event quantum on top of the Bekenstein–Hawking count, the same `log 2` as the `4 log 2` entropy
  residual (`QLF_HolographicDensity`, `Gravity_From_Delay.md` §9a).

## Scope

The no-go is about the de Sitter radius. A fixed radius `√(log 2)·c/H∞` would be algebraically
self-consistent, but it is not a horizon, and for any fixed radius today's `Ω_Λ = (H∞/H₀)²` depends on the
epoch. No new axioms.
-/

namespace QLF.DeSitterCount

open QLF QLF.DynamicalDarkEnergy QLF.InflationObserver QLF.HolographicDensity

/-- `log 2 < 1`, from `log x < x − 1` at `x = 2`. -/
theorem log_two_lt_one : Real.log 2 < 1 := by
  have h := Real.log_lt_sub_one_of_pos (by norm_num : (0 : ℝ) < 2) (by norm_num)
  linarith

/-- `1/2 < log 2`, from `log x < x − 1` at `x = 1/2`. -/
theorem half_lt_log_two : 1 / 2 < Real.log 2 := by
  have h := Real.log_lt_sub_one_of_pos (by norm_num : (0 : ℝ) < 2⁻¹) (by norm_num)
  rw [Real.log_inv] at h
  linarith

/-- The critical (de Sitter) density is positive for physical `G, c, H > 0`. -/
theorem criticalDensity_pos {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    0 < criticalDensity G c H := by
  unfold criticalDensity
  exact div_pos (mul_pos (mul_pos (by norm_num) (pow_pos hc 2)) (pow_pos hH 2))
    (mul_pos (mul_pos (by norm_num) Real.pi_pos) hG)

/-- **D1 — §3 on the Hubble/de Sitter radius.** Counting on `R = c/H` gives `log 2` times the density a
    de Sitter universe with that `H` must have. -/
theorem desitter_count_ratio {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    vacuum_energy_density_QLF G c (c / H) = Real.log 2 * criticalDensity G c H := by
  rw [rhoLambda_prop_Hsq G c H hG.ne' hc.ne' hH.ne']
  have h := omegaLambda_eq_log_two hG hc hH
  unfold omegaLambda at h
  exact (div_eq_iff (criticalDensity_pos hG hc hH).ne').mp h

/-- **D2 — self-consistency forces a unit prefactor.** A density counted as `p · ρ_crit(H)` on the
    de Sitter horizon of that same `H` is the de Sitter density iff `p = 1`. Algebra; the physics is the
    identification of the counted horizon with the de Sitter horizon. -/
theorem selfconsistent_iff_unit_prefactor {G c H p : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    p * criticalDensity G c H = criticalDensity G c H ↔ p = 1 := by
  have hY := (criticalDensity_pos hG hc hH).ne'
  constructor
  · intro h
    exact mul_right_cancel₀ hY (h.trans (one_mul _).symm)
  · rintro rfl
    exact one_mul _

/-- **D3 — QLF's count is not self-consistent on the de Sitter horizon**, because `log 2 ≠ 1`. -/
theorem qlf_count_not_selfconsistent {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    vacuum_energy_density_QLF G c (c / H) ≠ criticalDensity G c H := by
  rw [desitter_count_ratio hG hc hH]
  intro h
  exact absurd ((selfconsistent_iff_unit_prefactor hG hc hH).mp h) log_two_lt_one.ne

/-- The de Sitter horizon temperature in Planck units, `T_dS = 1/(2πR)`. -/
noncomputable def planckDeSitterTemperature (R : ℝ) : ℝ := 1 / (2 * Real.pi * R)

/-- **D4a — §3's energy is `log 2` times the Bekenstein–Hawking energy.** In Planck units, §3's horizon
    energy `f_gauge · (N log 2) · T_dS` equals `log 2 × S_BH · T_dS`, with `S_BH = N/4`. -/
theorem section3_energy_eq_log_two_mul_bh (R : ℝ) :
    gauge_axis_fraction * holographic_entropy R * planckDeSitterTemperature R
      = Real.log 2 * (bekensteinHawkingEntropy R * planckDeSitterTemperature R) := by
  rw [gauge_axis_fraction_eq]
  unfold holographic_entropy bekensteinHawkingEntropy per_event_entropy
  ring

/-- **D4b — the Bekenstein–Hawking energy is the self-consistent de Sitter energy.** In Planck units,
    `S_BH · T_dS = R/2`, and so is `ρ_dS · V = (3/8π)·(1/R)² · (4/3)πR³` on `R = 1/H`. -/
theorem bh_energy_eq_desitter_energy {R : ℝ} (hR : R ≠ 0) :
    bekensteinHawkingEntropy R * planckDeSitterTemperature R = R / 2 ∧
    3 / (8 * Real.pi) * (1 / R) ^ 2 * (4 / 3 * Real.pi * R ^ 3) = R / 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  constructor
  · unfold bekensteinHawkingEntropy holographic_event_count planckDeSitterTemperature
    field_simp
  · field_simp
    ring

/-- **Established:** D1–D4 of `Cosmological_Constant.md` §5.8. Counting on the de Sitter horizon forces
    the prefactor to 1 (`selfconsistent_iff_unit_prefactor`), so QLF's `log 2` count is not
    self-consistent there (`qlf_count_not_selfconsistent`). §3's `log 2` is the per-event quantum on top of
    the Bekenstein–Hawking count (`section3_energy_eq_log_two_mul_bh`, `bh_energy_eq_desitter_energy`), so
    it stands or falls with the `4 log 2` entropy residual (`Gravity_From_Delay.md` §9a). -/
theorem desitter_count_summary {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    vacuum_energy_density_QLF G c (c / H) = Real.log 2 * criticalDensity G c H ∧
    vacuum_energy_density_QLF G c (c / H) ≠ criticalDensity G c H :=
  ⟨desitter_count_ratio hG hc hH, qlf_count_not_selfconsistent hG hc hH⟩

end QLF.DeSitterCount
