import QLF_DynamicalDarkEnergy
import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_InflationObserver — every observer sees inflation behind and expansion ahead

`QLF_CosmicInflation` reads the cosmic history from **our** epoch: inflation in the past, dark energy
in the future. This module proves the reading holds for **every** observer, at every epoch. No epoch
is special. The statements P1–P5 were pre-registered in `Curvature.md` §8a (commit `c2d795e`) before
this proof was written.

**The definition.** Each closure makes its own time. The vacuum event rate is `f(t) = 1/t`
(`ZFAEventDynamics`). An observer at epoch `t₀` ticks at `f(t₀)`, so the rate at epoch `s`, measured in
that observer's own clock, is `r(t₀, s) = f(s)/f(t₀) = t₀/s`. "Inflation" means more than one e-fold per
own tick (`r > 1`). "Expansion" means positive but less than one (`0 < r < 1`). This is an
observer-relative quantity (a *listening*). It is **not** the standard `ä > 0`: `H ∝ 1/t` is a power law,
which decelerates in the usual sense.

**The results.**
* P1 `past_inflates`: for every observer, every earlier epoch has `r > 1`.
* P2 `future_expands`: every later epoch has `0 < r < 1`. Expansion slows but never stops.
* P3 `no_privileged_epoch`: `r(k·t₀, k·s) = r(t₀, s)`. Every observer sees the identical profile.
* P4 `floor_breaks_self_similarity`: the falsifier. For the rate law `1/t + c` with `c ≥ 0`, P3 holds at
  `(t₀, s, k) = (1, 2, 2)` **iff `c = 0`**. A constant floor (ΛCDM's constant `Λ`) gives the rate a
  built-in time scale, and early and late observers then see different histories. So P1–P3 are not
  true of every rate law. They rest on the scale-free premise, and P4 shows that premise does the work.
* P5 `omegaLambda_eq_log_two`: because `ρ_Λ ∝ H²` (`rhoLambda_prop_Hsq`), the dark-energy fraction
  `Ω_Λ = ρ_Λ/ρ_crit` equals `log 2` at every `H`. Every observer measures the same `Ω_Λ`.

## Honest scope

The arithmetic is short. The physical content is the premise that the cosmic rate is `f = 1/t` with no
built-in scale, and P4 is what makes that premise testable. **Open:** the `ä > 0` version; the
observer's own first tick, which has no past inside its domain; whether `ρ_Λ ∝ H²` survives the data;
and the inflation observables (`cosmic_inflation_in_progress`). No new axioms.
-/

namespace QLF.InflationObserver

open QLF QLF.DynamicalDarkEnergy

/-! ### 1. The observer's own clock -/

/-- The vacuum event rate at epoch `t`: `f = 1/t` (each closure makes its own time). -/
noncomputable def vacuumRate (t : ℝ) : ℝ := 1 / t

/-- The rate at epoch `s`, measured in the own clock of an observer at epoch `t₀`. -/
noncomputable def observedRate (t₀ s : ℝ) : ℝ := vacuumRate s / vacuumRate t₀

/-- The observed rate is the epoch ratio `t₀/s`. -/
theorem observedRate_eq {t₀ s : ℝ} (ht : t₀ ≠ 0) (hs : s ≠ 0) :
    observedRate t₀ s = t₀ / s := by
  unfold observedRate vacuumRate
  field_simp

/-! ### 2. P1 and P2: inflation behind, expansion ahead -/

/-- **P1 — the past inflates.** For an observer at any epoch `t₀`, every earlier epoch runs faster
    than one e-fold per own tick. -/
theorem past_inflates {t₀ s : ℝ} (hs : 0 < s) (hst : s < t₀) : 1 < observedRate t₀ s := by
  have ht : 0 < t₀ := hs.trans hst
  rw [observedRate_eq ht.ne' hs.ne', lt_div_iff₀ hs]
  linarith

/-- **P2 — the future expands, and never stops.** Every later epoch runs slower than the observer's
    own tick, but at a strictly positive rate. -/
theorem future_expands {t₀ s : ℝ} (ht : 0 < t₀) (hts : t₀ < s) :
    0 < observedRate t₀ s ∧ observedRate t₀ s < 1 := by
  have hs : 0 < s := ht.trans hts
  rw [observedRate_eq ht.ne' hs.ne']
  exact ⟨div_pos ht hs, (div_lt_one hs).mpr hts⟩

/-! ### 3. P3: no privileged epoch -/

/-- **P3 — no privileged epoch.** Rescaling every epoch by the same factor leaves the observed profile
    unchanged, so an observer at `k·t₀` sees exactly what an observer at `t₀` sees. -/
theorem no_privileged_epoch {t₀ s k : ℝ} (ht : 0 < t₀) (hs : 0 < s) (hk : 0 < k) :
    observedRate (k * t₀) (k * s) = observedRate t₀ s := by
  rw [observedRate_eq (mul_pos hk ht).ne' (mul_pos hk hs).ne', observedRate_eq ht.ne' hs.ne']
  exact mul_div_mul_left t₀ s hk.ne'

/-! ### 4. P4: the falsifier — a constant floor breaks it -/

/-- A rate law with a constant floor `c`, the shape a constant `Λ` gives: `1/t + c`. -/
noncomputable def flooredRate (c t : ℝ) : ℝ := 1 / t + c

/-- The floored rate at epoch `s`, in the own clock of an observer at `t₀`. -/
noncomputable def flooredObserved (c t₀ s : ℝ) : ℝ := flooredRate c s / flooredRate c t₀

/-- **P4 — the falsifier.** Compare the observer at `t₀ = 1` looking at `s = 2` with the observer at
    `t₀ = 2·1` looking at `s = 2·2`. With a constant floor `c ≥ 0` the two agree **iff `c = 0`**. Any
    built-in scale gives early and late observers different histories, so P3 is a property of the
    scale-free law `f = 1/t`, not of every rate law. -/
theorem floor_breaks_self_similarity {c : ℝ} (hc : 0 ≤ c) :
    flooredObserved c 2 4 = flooredObserved c 1 2 ↔ c = 0 := by
  unfold flooredObserved flooredRate
  have hA : (0 : ℝ) < 1 / 2 + c := by linarith
  have hB : (0 : ℝ) < 1 / 1 + c := by linarith
  rw [div_eq_div_iff hA.ne' hB.ne']
  constructor
  · intro h
    have h4 : c / 4 = 0 := by linear_combination h
    linarith
  · intro h
    rw [h]
    norm_num

/-- The scale-free law is the `c = 0` case of the floored law: P3 holds for it at the same points. -/
theorem scale_free_is_unfloored :
    flooredObserved 0 2 4 = flooredObserved 0 1 2 :=
  (floor_breaks_self_similarity le_rfl).mpr rfl

/-! ### 5. P5: every observer measures `Ω_Λ = log 2` -/

/-- The critical energy density at expansion rate `H`: `ρ_crit = 3c²H²/(8πG)`. -/
noncomputable def criticalDensity (G c H : ℝ) : ℝ := 3 * c ^ 2 * H ^ 2 / (8 * Real.pi * G)

/-- The dark-energy fraction at expansion rate `H`, using QLF's `ρ_Λ = (prefactor·c²/G)·H²`. -/
noncomputable def omegaLambda (G c H : ℝ) : ℝ :=
  rhoLambdaCoeff G c * H ^ 2 * (8 * Real.pi * G) / (3 * c ^ 2 * H ^ 2)

/-- `omegaLambda` is `ρ_Λ / ρ_crit`. -/
theorem omegaLambda_is_ratio {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    omegaLambda G c H = rhoLambdaCoeff G c * H ^ 2 / criticalDensity G c H := by
  have hπ : Real.pi ≠ 0 := Real.pi_pos.ne'
  have hG' : G ≠ 0 := hG.ne'
  have hc' : c ≠ 0 := hc.ne'
  have hH' : H ≠ 0 := hH.ne'
  unfold omegaLambda criticalDensity
  rw [div_div_eq_mul_div]

/-- **P5 — every observer measures `Ω_Λ = log 2`.** Since `ρ_Λ ∝ H²` and `ρ_crit ∝ H²`, the ratio
    does not depend on `H`, so it is the same at every epoch. Under a constant `Λ` it would fall as
    `1/H²`, and observers at different epochs would measure different fractions. -/
theorem omegaLambda_eq_log_two {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    omegaLambda G c H = Real.log 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_pos.ne'
  have hG' : G ≠ 0 := hG.ne'
  have hc' : c ≠ 0 := hc.ne'
  have hH' : H ≠ 0 := hH.ne'
  unfold omegaLambda rhoLambdaCoeff vacuum_energy_prefactor
  field_simp

/-! ### Summary -/

/-- **Every observer's vantage, packaged.** For an observer at any epoch `t₀ > 0`: every earlier epoch
    inflates (`r > 1`), every later epoch expands at a positive but slower rate (`0 < r < 1`), and an
    observer at any rescaled epoch sees the identical profile. -/
theorem every_observer_inflation_behind_expansion_ahead {t₀ : ℝ} (ht : 0 < t₀) :
    (∀ s : ℝ, 0 < s → s < t₀ → 1 < observedRate t₀ s) ∧
    (∀ s : ℝ, t₀ < s → 0 < observedRate t₀ s ∧ observedRate t₀ s < 1) ∧
    (∀ s k : ℝ, 0 < s → 0 < k → observedRate (k * t₀) (k * s) = observedRate t₀ s) :=
  ⟨fun _ hs hst => past_inflates hs hst,
   fun _ hts => future_expands ht hts,
   fun _ _ hs hk => no_privileged_epoch ht hs hk⟩

/-- **Established constructively:** P1–P5 of `Curvature.md` §8a. In their own clocks, every observer
    sees inflation behind (`past_inflates`), expansion ahead (`future_expands`), no privileged epoch
    (`no_privileged_epoch`) and the same `Ω_Λ = log 2` (`omegaLambda_eq_log_two`). The scale-free
    premise is shown to carry the weight (`floor_breaks_self_similarity`). **Open:** the `ä > 0`
    version; the observer's own first tick; whether `ρ_Λ ∝ H²` survives the data; and the inflation
    observables. -/
theorem inflation_observer_in_progress : True := trivial

end QLF.InflationObserver
