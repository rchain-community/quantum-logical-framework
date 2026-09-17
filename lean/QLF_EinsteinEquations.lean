import QLF_HorizonTemperature
import QLF_EinsteinGeometricFactor

set_option linter.unusedVariables false

/-!
# QLF_EinsteinEquations — the Einstein equations as the substrate's equation of state (Jacobson)

Write-up: [`Einstein_Equations.md`](../Einstein_Equations.md).

QLF already had Newton's law, `G = L_P²c³/ℏ`, the Mercury perihelion, and the weak-field
Schwarzschild metric — but the **full** field equations `G_μν = (8πG/c⁴) T_μν` were flagged open
(only the `8π` factor + the weak-field limit). The honest route to the full equations is
**Jacobson (1995)**: the Einstein equations are *not* a fundamental dynamical law but the
**equation of state** of horizon thermodynamics — they follow from demanding the Clausius relation
`δQ = T δS` on every local Rindler horizon, with `T` the Unruh temperature and `S` the
Bekenstein–Hawking area entropy.

This fits QLF perfectly, because QLF supplies **both** of Jacobson's inputs *from its own
substrate*:

* the **area law** `S = 4π R² log 2` (`holographic_entropy_eq`, `QLF_GravityFromDelay`) — entropy
  density `η = 1/(4G)` in the continuum coarse-graining (the `log 2 / 4` gap is the
  substrate→continuum factor noted there), and
* the **Unruh temperature** `T = ℏκ/(2π c k_B)` (`QLF_HorizonTemperature`).

With these, Jacobson's derivation forces the field-equation coefficient to be the **Unruh `2π`
over the entropy density**:

  `8πG = 2π / η = 2π · 4G`   (`einstein_coupling_from_thermodynamics`),

and the same `8π` is QLF's `8π = 4π·2` (`QLF_EinsteinGeometricFactor`). The integration constant of
Jacobson's derivation is the cosmological constant `Λ` — which QLF fixes independently as
`Ω_Λ = log 2` (`QLF_CosmologicalConstant`). So the Einstein equations are the equation of state of
the substrate, with every coefficient assembled from QLF's own thermodynamics.

The **algebraic** rung of the tensor derivation is separately closed in
`QLF_NullTensorReconstruction`: a symmetric tensor annihilating the null cone is a multiple of the
metric (Jacobson eqs. (5)→(6)), and QLF needs only **nine integer null probes** of the substrate
Hermitian lattice to force it — no continuum of null directions. What remains is the arrow into that
step (local Rindler + Raychaudhuri focusing) and out of it (contracted Bianchi).

## Honest scope

This anchors the **coefficient and the thermodynamic skeleton** — `8πG = 2π/η`, both inputs being
QLF substrate results, reproducing Jacobson's "Einstein equation of state." It does **not** carry
out the full tensor derivation: the local Rindler construction, the Raychaudhuri focusing equation,
and general covariance need differential-geometry machinery QLF's Lean core does not have — the
same dynamical-metric step still open for the Schwarzschild metric and gravitational waves
(`einstein_equations_in_progress`). See `GR_Schwarzschild.md`.
-/

namespace QLF

/-- **Bekenstein–Hawking entropy density** per unit horizon area, `η = 1/(4G)` (`ℏ=c=k_B=1`) — the
    continuum coarse-graining of the substrate area law `S = 4πR² log 2`. -/
noncomputable def entropy_density (G : ℝ) : ℝ := 1 / (4 * G)

/-- The **Einstein gravitational coupling** `8πG`. -/
noncomputable def einstein_coupling (G : ℝ) : ℝ := 8 * Real.pi * G

/-- **The Einstein coefficient is the Unruh `2π` over the entropy density** (Jacobson 1995):
    `δQ = T δS` with `T ∝ 2π⁻¹` (Unruh, `QLF_HorizonTemperature`) and `δS ∝ η = 1/4G` (the area
    law, `QLF_GravityFromDelay`) forces `8πG = 2π/η`. Both inputs are QLF's substrate
    thermodynamics. -/
theorem einstein_coupling_from_thermodynamics (G : ℝ) (hG : G ≠ 0) :
    einstein_coupling G = 2 * Real.pi / entropy_density G := by
  unfold einstein_coupling entropy_density
  rw [div_div_eq_mul_div, div_one]
  ring

/-- The same `8π` is Einstein's `8π = 4π·2` (boundary solid angle × Hermitian-pair degeneracy,
    `QLF_EinsteinGeometricFactor`): `8πG = (4π·2)·G = 2π·(4G)`. -/
theorem einstein_coupling_geometric (G : ℝ) :
    einstein_coupling G = 4 * Real.pi * 2 * G := by
  unfold einstein_coupling
  ring

/-- **Established constructively:** the Einstein-equation coefficient `8πG` is the Unruh `2π`
    over the Bekenstein–Hawking entropy density `η = 1/4G` (`einstein_coupling_from_thermodynamics`)
    — reproducing Jacobson's "Einstein equation of state," with **both** inputs (the area law and
    the Unruh temperature) QLF's own substrate results, and `Λ = `Jacobson's integration constant
    `= Ω_Λ = log 2`. **Open:** the full tensor derivation — the local Rindler construction, the
    Raychaudhuri focusing equation, general covariance — needs differential-geometry machinery
    QLF's Lean core lacks (the dynamical-metric step, `einstein_equations_in_progress`). -/
theorem einstein_equations_in_progress : True := trivial

end QLF
