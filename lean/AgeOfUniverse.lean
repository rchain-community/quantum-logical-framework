/-
AgeOfUniverse.lean
Quantum Logical Framework — a frequency-spectrum model of the effective cosmic age

A toy model (`AgeOfUniverse.md` §2): the effective Hubble rate is set by an event rate over a frequency
band, and the age is its inverse. What is proved: for any band `0 < ω_min < ω_max` the effective age is
finite and positive (`age_is_finite_and_positive`). The quantities are unitless and the model carries no
dimensional scale, so it computes no age in years; `totalEventRate` integrates a flat band
(`ω_max − ω_min`), not the `1/ω` spectrum `zpePhotonNumberDensity` describes.
-/

import SpacetimeDynamics
import Mathlib.Analysis.SpecialFunctions.Sqrt

open Real

/-! # Frequency Distribution Model -/

/-- ZPE photon number density: n(ω) ∝ 1/ω -/
noncomputable def zpePhotonNumberDensity (omega : ℝ) : ℝ :=
  if omega > 0 then 1 / omega else 0

/-- Event rate over the band, as a flat-band integral `ω_max − ω_min` (not the `1/ω` spectrum) -/
noncomputable def totalEventRate (omega_min omega_max : ℝ) : ℝ :=
  omega_max - omega_min

/-- Effective Hubble parameter: H² ∝ event rate (QLF Friedmann) -/
noncomputable def hubbleFromZpeSpectrum (omega_min omega_max : ℝ) : ℝ :=
  sqrt ((omega_max - omega_min) / 3)

/-- Effective cosmic age ≈ 1/H₀ -/
noncomputable def effectiveCosmicAge (omega_min omega_max : ℝ) : ℝ :=
  let H0 := hubbleFromZpeSpectrum omega_min omega_max
  if H0 > 0 then 1 / H0 else 0

/-! # Theorems -/

theorem age_is_finite_and_positive (omega_min omega_max : ℝ)
    (h_min : omega_min > 0) (h_range : omega_max > omega_min) :
    effectiveCosmicAge omega_min omega_max > 0 := by
  simp only [effectiveCosmicAge, hubbleFromZpeSpectrum]
  have h_pos : (omega_max - omega_min) / 3 > 0 := by positivity
  have h_sqrt : sqrt ((omega_max - omega_min) / 3) > 0 := sqrt_pos.mpr h_pos
  simp only [h_sqrt, if_true]
  exact div_pos one_pos h_sqrt
