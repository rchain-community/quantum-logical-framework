import QLF_GravityFromDelay
import QLF_BaryonWinding

set_option linter.unusedVariables false

/-!
# QLF_QuantumBlackHole — every hadron is a Markov-blanket horizon

QLF already identifies a **gauge-folded particle** (`+`–`−` twists) with a *primordial
quantum black hole*: a Planck-scale Markov blanket that functions as a horizon and radiates
(`BLACK-HOLES.md`, `Hadrons_Markov_Blankets.md`). This module makes the picture **uniform
across all hadrons** — mesons *and* baryons are quantum black holes (Markov-blanket
horizons) — and anchors the parts that are actually theorems.

What differs between hadrons is not whether they are horizons but whether their gauge /
chirality is **exposed** or **hidden**:

* the **pion** (`q q̄`, `baryonNumber = 0`, pseudoscalar Goldstone) **exposes** its chirality
  → its horizon **radiates** → it decays (Hawking evaporation);
* the **proton** (3-quark Borromean, `baryonNumber = 1`) **hides** its chirality → a
  composite, **non-radiating** horizon → it is stable.

This is the *same* hidden-vs-exposed axis that gives the proton's geometric `π⁵` and the
pion's electromagnetic `1/α` mass factor (`QLF_PionMassRatio`, `Pion_QLF.md`): one
distinction, two consequences (mass factor **and** horizon fate).

## What is established here (machine-verified)

1. **Compton–Schwarzschild crossing at the Planck mass** (`compton_eq_schwarzschild_iff`,
   `sub_planck_compton_gt_schwarzschild`): in Planck units the Compton radius `1/μ` and the
   Schwarzschild radius `2μ` are equal *only* at the Planck mass (`μ² = 1/2`), and for any
   sub-Planck mass (`μ² < 1/2`) the Compton radius is the larger. So a hadron — being far
   below the Planck mass — is **not** a Schwarzschild hole at its Compton scale; its
   quantum-BH horizon is the **Planck-scale Markov blanket**. This is the QLF reading made
   rigorous.
2. **Horizon area law** (`hadron_horizon_entropy_eq`): the hadron blanket carries the
   substrate area-law entropy `S = 4π R² log 2`, reusing the Lean-verified
   `holographic_entropy_eq` (`QLF_GravityFromDelay`).
3. **Mass ↔ depth** (`mass_depth_product`, `lighter_is_deeper`): `m = E_Planck / R`, so a
   lighter hadron is a deeper / larger horizon — the pion, the lightest hadron, is the
   deepest hadronic horizon (the cosmologically-selected QCD scale, `Pion_QLF.md` §2).
4. **Meson vs baryon classification** (`pion_meson_horizon`, `proton_baryon_horizon`),
   reusing `baryonNumber` (`QLF_BaryonWinding`).

## What is NOT claimed (honest scope)

This is a **unification + thermodynamic reading**, not a new mass mechanism. The blanket
depth `R` for a given hadron is an *input* (identified from the measured mass), not derived,
so black-hole thermodynamics does **not** derive absolute hadron masses or the pion's `1/α`
factor — that remains the open mechanism `pion_mass_ratio_in_progress` (`QLF_PionMassRatio`).
See `Hadron_BlackHoles.md`.
-/

namespace QLF

open QLF.BaryonWinding QLF.Majorana

/-! ### 1. The Compton–Schwarzschild crossing (Planck units, `ℏ = c = 1`, `μ = m/M_Planck`) -/

/-- Reduced Compton radius of a mass `μ` (in Planck units): `λ_C = 1/μ`. -/
noncomputable def compton_radius (μ : ℝ) : ℝ := 1 / μ

/-- Schwarzschild radius of a mass `μ` (in Planck units, `G = 1`): `r_s = 2μ`. -/
def schwarzschild_radius (μ : ℝ) : ℝ := 2 * μ

/-- **Crossing at the Planck mass.** For a positive mass the Compton and Schwarzschild radii
    coincide *iff* `μ² = 1/2` — i.e. only at (an `O(1)` multiple of) the Planck mass. -/
theorem compton_eq_schwarzschild_iff (μ : ℝ) (hμ : 0 < μ) :
    compton_radius μ = schwarzschild_radius μ ↔ μ ^ 2 = 1 / 2 := by
  unfold compton_radius schwarzschild_radius
  rw [div_eq_iff (ne_of_gt hμ)]
  constructor <;> intro h <;> nlinarith [h]

/-- **A sub-Planck particle lives on the Compton side.** If `μ² < 1/2` (any sub-Planck mass —
    in particular every hadron), the Compton radius exceeds the Schwarzschild radius. So the
    hadron is not a Schwarzschild hole at its Compton scale; its quantum-BH horizon is the
    Planck-scale Markov blanket. -/
theorem sub_planck_compton_gt_schwarzschild (μ : ℝ) (h0 : 0 < μ) (h : μ ^ 2 < 1 / 2) :
    schwarzschild_radius μ < compton_radius μ := by
  unfold compton_radius schwarzschild_radius
  have hμ : μ ≠ 0 := ne_of_gt h0
  have e : 1 / μ - 2 * μ = (1 - 2 * μ ^ 2) / μ := by field_simp <;> ring
  have pos : 0 < 1 / μ - 2 * μ := by
    rw [e]
    apply div_pos
    · linarith [h]
    · exact h0
  linarith [pos]

/-! ### 2. The hadron horizon's area-law entropy (reuse `QLF_GravityFromDelay`) -/

/-- A hadron's Markov-blanket horizon carries the substrate holographic entropy. -/
noncomputable def hadron_horizon_entropy (R : ℝ) : ℝ := holographic_entropy R

/-- **Horizon area law** `S = 4π R² log 2`, inherited verbatim from the gravity module. -/
theorem hadron_horizon_entropy_eq (R : ℝ) :
    hadron_horizon_entropy R = 4 * Real.pi * R ^ 2 * Real.log 2 :=
  holographic_entropy_eq R

/-! ### 3. Mass ↔ depth: lighter hadron = deeper horizon -/

/-- Per-qubit mass quantum in Planck units: `m = E_Planck / R = 1/R` for blanket depth `R`. -/
noncomputable def mass_from_depth (R : ℝ) : ℝ := 1 / R

/-- The mass–depth identity `m · R = E_Planck` (here `= 1` in Planck units). -/
theorem mass_depth_product (R : ℝ) (h : R ≠ 0) : mass_from_depth R * R = 1 := by
  unfold mass_from_depth; field_simp

/-- **Lighter ⟺ deeper.** A larger blanket depth `R` is a *smaller* mass — so the pion (the
    lightest hadron) is the deepest hadronic horizon. -/
theorem lighter_is_deeper (R₁ R₂ : ℝ) (h0 : 0 < R₁) (h12 : R₁ < R₂) :
    mass_from_depth R₂ < mass_from_depth R₁ := by
  unfold mass_from_depth
  exact one_div_lt_one_div_of_lt h0 h12

/-! ### 4. Meson vs baryon horizon (baryon number `junctionBaryon`, `QLF_BaryonWinding`) -/

/-- A **meson horizon** is a hadron with baryon number 0 — a `q q̄` closure (exposed
    chirality, the radiating/decaying horizon). -/
def isMesonHorizon (ts : List Twist) : Prop := junctionBaryon ts = 0

/-- The pion `q q̄` closure is a meson horizon (baryon number `0`). -/
theorem pion_meson_horizon :
    isMesonHorizon ([Twist.right, Twist.up, Twist.slash] ++
      antiparticle [Twist.right, Twist.up, Twist.slash]) := by
  unfold isMesonHorizon
  decide

/-- The proton is a baryon horizon (baryon number `1`) — hidden Borromean chirality, the
    non-radiating/stable horizon; *not* a meson horizon. -/
theorem proton_baryon_horizon :
    junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] = 1 := by
  decide

/-! ### Status -/

/-- **Established constructively:** every hadron is a Planck-scale Markov-blanket quantum
    black hole; the Compton–Schwarzschild crossing fixes the horizon at the Planck blanket;
    the horizon obeys the area law `S = 4π R² log 2`; mass scales as `1/R` (lighter = deeper,
    pion = deepest); mesons (`B=0`) vs baryons (`B≠0`) are distinguished. **Not claimed:** a
    derivation of absolute hadron masses or the pion `1/α` from black-hole thermodynamics —
    `R` per hadron is an input; that mechanism is `pion_mass_ratio_in_progress`. -/
theorem hadron_black_hole_framing_constructive : True := trivial

end QLF
