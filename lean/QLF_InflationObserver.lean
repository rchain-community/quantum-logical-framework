import QLF_DynamicalDarkEnergy
import ZFAEventDynamics
import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_InflationObserver — every observer sees inflation behind and expansion ahead

`QLF_CosmicInflation` reads the cosmic history from **our** epoch: inflation in the past, dark energy
in the future. This module proves the reading holds for **every** observer, at every epoch. No epoch
is special. The statements P1–P5 were pre-registered in `Curvature.md` §8a (commit `c2d795e`) before
this proof was written.

**The definition.** Each closure makes its own time. The vacuum event rate is `f(t) = 1/t`
(`ZFAEventDynamics`). An observer at epoch `t₀` ticks at `f(t₀)`, so the rate at epoch `s`, relative to
that observer's own clock, is the ratio of rates `r(t₀, s) = f(s)/f(t₀) = t₀/s`. "Inflation" means faster
than the observer's own clock (`r > 1`). "Expansion" means positive but slower (`0 < r < 1`). This is an
observer-relative quantity (a *listening*). It is **not** the standard `ä > 0`: `H ∝ 1/t` is a power law,
which decelerates in the usual sense. `f = 1/t` is proved per event in `ZFAEventDynamics`
(`spacetime_from_zfa_preserves_synthesis`, linked here by `vacuumRate_is_event_rate`). Reading it as the
**cosmic** rate as a function of epoch is a premise, not a theorem.

**The results.**
* P1 `past_inflates`: for every observer, every earlier epoch has `r > 1`.
* P2 `future_expands`: every later epoch has `0 < r < 1`. Expansion slows but never stops.
* P3 `no_privileged_epoch`: `r(k·t₀, k·s) = r(t₀, s)`. Every observer sees the identical profile.
* P4 `floor_breaks_self_similarity`: for the rate law `1/t + c` with `c ≥ 0`, P3 holds at
  `(t₀, s, k) = (1, 2, 2)` **iff `c = 0`**. A constant floor (ΛCDM's constant `Λ`) gives the rate a
  built-in time scale, and early and late observers then see different histories.
* P5 `omegaLambda_eq_log_two`: because `ρ_Λ ∝ H²` (`rhoLambda_prop_Hsq`), `Ω_Λ = ρ_Λ/ρ_crit` does not
  depend on `H`. Its value `log 2` is the input prefactor `3 log 2 / 8π`, so the content is the
  `H`-independence, not the number.

**What carries weight, measured (review of PR #164).** P1 and P2 are *definitional consequences* of a
falling rate. They hold for the floored law too (`floored_past_also_inflates`), so by `CLAUDE.md` rule 4
they are not evidence. P3 is the substantive statement, and it does not single out `1/t`: every power law
`t⁻ⁿ` satisfies it (`power_law_no_privileged_epoch`). P3 and P4 together show the rate has **no built-in
scale**. They do not show that it is `1/t`.

## Honest scope

The arithmetic is short. The physical content is the premise that the cosmic rate has no built-in
scale, and P4 is what makes that premise testable. **Named tension, not an open question:** P5 means
`Ω_Λ = log 2 ≈ 0.69` at recombination and at BBN, if `ρ_Λ ∝ H²` holds at every epoch as
`QLF_DynamicalDarkEnergy` states it. CMB data bound a constant early dark-energy fraction to
`Ω_early < 0.06` at 95% (Doran & Robbers, JCAP 0606:026, 2006), and later data tighten it. At BBN the
same fraction would raise `H` by `(1 − log 2)^(−1/2) ≈ 1.8`. So either `ρ_Λ ∝ H²` fails at early epochs or
this reading is falsified. **Open:** the `ä > 0` version; the observer's own first tick, which has no past
inside its domain; and the inflation observables (`cosmic_inflation_in_progress`). No new axioms.
-/

namespace QLF.InflationObserver

open QLF QLF.DynamicalDarkEnergy

/-! ### 1. The observer's own clock -/

/-- The vacuum event rate at epoch `t`: `f = 1/t` (each closure makes its own time). -/
noncomputable def vacuumRate (t : ℝ) : ℝ := 1 / t

/-- The rate at epoch `s`, measured in the own clock of an observer at epoch `t₀`. -/
noncomputable def observedRate (t₀ s : ℝ) : ℝ := vacuumRate s / vacuumRate t₀

/-- A ratio of reciprocals: `(1/b)/(1/a) = a/b`. -/
private theorem ratio_of_inverses {a b : ℝ} (ha : a ≠ 0) (hb : b ≠ 0) :
    1 / b / (1 / a) = a / b := by
  field_simp

/-- The observed rate is the ratio of rates `t₀/s`. -/
theorem observedRate_eq {t₀ s : ℝ} (ht : t₀ ≠ 0) (hs : s ≠ 0) :
    observedRate t₀ s = t₀ / s := by
  unfold observedRate vacuumRate
  exact ratio_of_inverses ht hs

/-- **The link to the per-event clock.** For every ZFA event, the frequency it synthesizes is
    `vacuumRate` of the time it synthesizes (`spacetime_from_zfa_preserves_synthesis`). This is the
    per-event `f = 1/t`. Using it as the cosmic rate as a function of epoch is the module's premise. -/
theorem vacuumRate_is_event_rate (e : ZFAEvent) :
    e.synthesizeSpacetime.2.2 = vacuumRate e.synthesizeSpacetime.2.1 := by
  unfold vacuumRate
  exact spacetime_from_zfa_preserves_synthesis e

/-! ### 2. P1 and P2: inflation behind, expansion ahead -/

/-- **P1 — the past inflates.** For an observer at any epoch `t₀`, every earlier epoch runs faster
    than the observer's own clock. A consequence of any falling rate (`floored_past_also_inflates`),
    so not evidence on its own. -/
theorem past_inflates {t₀ s : ℝ} (hs : 0 < s) (hst : s < t₀) : 1 < observedRate t₀ s := by
  have ht : 0 < t₀ := hs.trans hst
  rw [observedRate_eq ht.ne' hs.ne', lt_div_iff₀ hs]
  linarith

/-- **P2 — the future expands, and never stops.** Every later epoch runs slower than the observer's
    own tick, but at a strictly positive rate. Like P1, a consequence of any falling positive rate. -/
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

/-- A power-law rate `t⁻ⁿ`, written `1/tⁿ`. -/
noncomputable def powerRate (n : ℕ) (t : ℝ) : ℝ := 1 / t ^ n

/-- The power-law rate at epoch `s`, in the own clock of an observer at `t₀`. -/
noncomputable def powerObserved (n : ℕ) (t₀ s : ℝ) : ℝ := powerRate n s / powerRate n t₀

/-- A power-law observed rate is the `n`-th power of the `1/t` one. -/
theorem powerObserved_eq {n : ℕ} {t₀ s : ℝ} (ht : t₀ ≠ 0) (hs : s ≠ 0) :
    powerObserved n t₀ s = observedRate t₀ s ^ n := by
  unfold powerObserved powerRate
  rw [observedRate_eq ht hs, div_pow]
  exact ratio_of_inverses (pow_ne_zero n ht) (pow_ne_zero n hs)

/-- **P3 does not single out `1/t`.** Every power law `t⁻ⁿ` has no privileged epoch either. What P3
    (with P4) establishes is that the rate has no built-in scale, not which scale-free law it is. -/
theorem power_law_no_privileged_epoch {n : ℕ} {t₀ s k : ℝ} (ht : 0 < t₀) (hs : 0 < s) (hk : 0 < k) :
    powerObserved n (k * t₀) (k * s) = powerObserved n t₀ s := by
  rw [powerObserved_eq (mul_pos hk ht).ne' (mul_pos hk hs).ne', powerObserved_eq ht.ne' hs.ne',
    no_privileged_epoch ht hs hk]

/-! ### 4. P4: the falsifier — a constant floor breaks it -/

/-- A rate law with a constant floor `c`, the shape a constant `Λ` gives: `1/t + c`. -/
noncomputable def flooredRate (c t : ℝ) : ℝ := 1 / t + c

/-- The floored rate at epoch `s`, in the own clock of an observer at `t₀`. -/
noncomputable def flooredObserved (c t₀ s : ℝ) : ℝ := flooredRate c s / flooredRate c t₀

/-- **P1 holds with a floor too, so it is not evidence.** A constant floor `c ≥ 0` still makes every
    earlier epoch faster than the observer's clock. What the floor breaks is P3 (P4 below). -/
theorem floored_past_also_inflates {c t₀ s : ℝ} (hc : 0 ≤ c) (hs : 0 < s) (hst : s < t₀) :
    1 < flooredObserved c t₀ s := by
  have ht : 0 < t₀ := hs.trans hst
  unfold flooredObserved flooredRate
  have hB : 0 < 1 / t₀ + c := by
    have := div_pos one_pos ht
    linarith
  rw [lt_div_iff₀ hB]
  have := one_div_lt_one_div_of_lt hs hst
  linarith

/-- **P4 — the falsifier.** Compare the observer at `t₀ = 1` looking at `s = 2` with the observer at
    `t₀ = 2·1` looking at `s = 2·2`. With a constant floor `c ≥ 0` the two agree **iff `c = 0`**. Any
    built-in scale gives early and late observers different histories, so P3 is a property of
    scale-free rate laws, not of every rate law. -/
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

/-- The dark-energy fraction `Ω_Λ = ρ_Λ/ρ_crit` at expansion rate `H`, with QLF's
    `ρ_Λ = (prefactor·c²/G)·H²` (`rhoLambda_prop_Hsq`). Defined as the ratio, unsimplified. -/
noncomputable def omegaLambda (G c H : ℝ) : ℝ :=
  rhoLambdaCoeff G c * H ^ 2 / criticalDensity G c H

/-- **P5 — every observer measures `Ω_Λ = log 2`.** Since `ρ_Λ ∝ H²` and `ρ_crit ∝ H²`, the ratio
    does not depend on `H`, so it is the same at every epoch. The value `log 2` is the input prefactor
    `3 log 2 / 8π`; the content is the `H`-independence. **Tension:** at recombination and BBN this is
    far above the early dark-energy bound (`Ω_early < 0.06`, Doran & Robbers 2006) — see the module
    header. Under a constant `Λ` the fraction would fall as `1/H²` instead. -/
theorem omegaLambda_eq_log_two {G c H : ℝ} (hG : 0 < G) (hc : 0 < c) (hH : 0 < H) :
    omegaLambda G c H = Real.log 2 := by
  have hπ : Real.pi ≠ 0 := Real.pi_pos.ne'
  have hG' : G ≠ 0 := hG.ne'
  have hc' : c ≠ 0 := hc.ne'
  have hH' : H ≠ 0 := hH.ne'
  unfold omegaLambda criticalDensity
  rw [div_div_eq_mul_div]
  unfold rhoLambdaCoeff vacuum_energy_prefactor
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

/-- **Established constructively:** P1–P5 of `Curvature.md` §8a. `every_observer_…` bundles P1–P3;
    P4 is `floor_breaks_self_similarity` and P5 is `omegaLambda_eq_log_two`. What carries weight is P3
    with P4: the rate has no built-in scale (not specifically `1/t`, `power_law_no_privileged_epoch`).
    P1–P2 follow from any falling rate (`floored_past_also_inflates`). **Named tension:** P5 conflicts
    with early dark-energy bounds at recombination and BBN. **Open:** the `ä > 0` version; the
    observer's own first tick; the inflation observables. -/
theorem inflation_observer_in_progress : True := trivial

end QLF.InflationObserver
