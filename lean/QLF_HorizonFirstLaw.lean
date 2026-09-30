import QLF_DeSitterCount
import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_HorizonFirstLaw — QLF's own Hawking temperature fixes the horizon entropy at `A/4`

`QLF_HolographicDensity` leaves the `4 log 2` residual between QLF's one-bit-per-Planck-patch count and
Bekenstein–Hawking open, as a choice between (a) a discrete-floor deviation and (b) an area-element
reading. This module applies the **first law** `dE = T dS` at a Schwarzschild horizon, with the Hawking
temperature QLF already proves (`hawking_temperature_eq`). Statements F1–F4 were pre-registered in
`Gravity_From_Delay.md` §9a (commit `e3d4df5`) before this proof was written.

* F1 `bh_entropy_first_law`: `S(M) = 4πGk_B M²/(ħc)` satisfies `dS/dM = c²/T_H`.
* F2 `bhEntropyOfMass_eq_area`: that `S` is `k_B A/(4L_P²)` with `A = 4π(2GM/c²)²`, `L_P² = ħG/c³`.
* F3 `naive_count_breaks_first_law`: the naive count `4 log 2 · S` has `dS/dM = 4 log 2 · c²/T_H`, and
  `4 log 2 ≠ 1`.
* F4 `half_lt_log_two`, `log_two_lt_one` (reused from `QLF_DeSitterCount`).

The route is Hawking's (1975), not new. What it settles inside QLF: with QLF's own temperature, the
naive count breaks the first law by exactly the residual. The derivative fixes `S` only up to an additive
constant; `S(0) = 0` picks this one.

## Conditions and scope

Branch (a) is closed **given** (i) QLF's Hawking temperature (proved, `QLF_HorizonTemperature`); (ii)
`E = Mc²` with `R = 2GM/c²` (the GR input); and (iii) the first law at the horizon. In QLF, (iii) holds only
in the mean, since energy conservation is statistical (`Conservation.md` §2a). Branch (b) is then forced:
one bit occupies `4 log 2 · L_P²` of horizon. **Consequence for dark energy** (`Cosmological_Constant.md` §3,
§5.8): counting with `S_BH` gives `Ω_Λ = 1/4` (with `f_gauge`) or `1` (without); neither is `log 2`
(`firstlaw_count_omega`). No new axioms.
-/

namespace QLF.HorizonFirstLaw

open QLF QLF.DeSitterCount QLF.HolographicDensity

/-- The Bekenstein–Hawking entropy as a function of mass, `S(M) = 4πGk_B M²/(ħc)`. -/
noncomputable def bhEntropyOfMass (hbar G c kB : ℝ) (M : ℝ) : ℝ :=
  4 * Real.pi * G * kB / (hbar * c) * (M * M)

/-- **F1 — the first law holds for `S_BH` with QLF's Hawking temperature.** `dS/dM = c²/T_H`, i.e.
    `T_H dS = d(Mc²)`. -/
theorem bh_entropy_first_law {hbar G c kB M : ℝ}
    (hh : hbar ≠ 0) (hG : G ≠ 0) (hM : M ≠ 0) (hc : c ≠ 0) (hkB : kB ≠ 0) :
    HasDerivAt (bhEntropyOfMass hbar G c kB)
      (c ^ 2 / hawking_temperature hbar G M c kB) M := by
  have h : HasDerivAt (fun x : ℝ => x * x) (1 * M + M * 1) M :=
    (hasDerivAt_id M).mul (hasDerivAt_id M)
  have hπ : Real.pi ≠ 0 := Real.pi_ne_zero
  have hv : c ^ 2 / hawking_temperature hbar G M c kB
      = 4 * Real.pi * G * kB / (hbar * c) * (1 * M + M * 1) := by
    rw [hawking_temperature_eq hbar G M c kB hG hM hc hkB]
    field_simp
    ring
  rw [hv]
  exact h.const_mul (4 * Real.pi * G * kB / (hbar * c))

/-- **F2 — it is the area law.** `S(M) = k_B A/(4L_P²)` with horizon area `A = 4π(2GM/c²)²` and
    `L_P² = ħG/c³`. -/
theorem bhEntropyOfMass_eq_area {hbar G c kB M : ℝ} (hh : hbar ≠ 0) (hG : G ≠ 0) (hc : c ≠ 0) :
    bhEntropyOfMass hbar G c kB M
      = kB * (4 * Real.pi * (2 * G * M / c ^ 2) ^ 2) / (4 * (hbar * G / c ^ 3)) := by
  unfold bhEntropyOfMass
  field_simp
  ring

/-- **F3 — the naive count breaks the first law by exactly the residual.** QLF's one-bit-per-patch
    entropy is `4 log 2 · S_BH` (`holographic_bh_ratio`). Its mass gradient is `4 log 2 · c²/T_H`, and
    `4 log 2 ≠ 1`, so it cannot satisfy `T_H dS = d(Mc²)`. -/
theorem naive_count_breaks_first_law {hbar G c kB M : ℝ}
    (hh : hbar ≠ 0) (hG : G ≠ 0) (hM : M ≠ 0) (hc : c ≠ 0) (hkB : kB ≠ 0) :
    HasDerivAt (fun x => 4 * Real.log 2 * bhEntropyOfMass hbar G c kB x)
      (4 * Real.log 2 * (c ^ 2 / hawking_temperature hbar G M c kB)) M ∧
    4 * Real.log 2 ≠ 1 := by
  refine ⟨(bh_entropy_first_law hh hG hM hc hkB).const_mul (4 * Real.log 2), ?_⟩
  have := half_lt_log_two
  intro h
  linarith

/-- **Consequence for §3.** Recount §3's horizon energy with the first-law entropy `S_BH` in place of
    `N log 2`. In Planck units the energy is `f_gauge · S_BH · T_dS = (1/4)·(R/2)` with `f_gauge`, or
    `R/2` without it. Against the de Sitter energy `R/2` (`bh_energy_eq_desitter_energy`), that is
    `Ω_Λ = 1/4` or `1`, not `log 2`. -/
theorem firstlaw_count_omega {R : ℝ} (hR : R ≠ 0) :
    gauge_axis_fraction * bekensteinHawkingEntropy R * planckDeSitterTemperature R = 1 / 4 * (R / 2) ∧
    bekensteinHawkingEntropy R * planckDeSitterTemperature R = 1 * (R / 2) := by
  have h := (bh_energy_eq_desitter_energy hR).1
  constructor
  · rw [gauge_axis_fraction_eq, mul_assoc, h]
  · rw [h, one_mul]

end QLF.HorizonFirstLaw
