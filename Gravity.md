# Gravity in the Quantum Logical Framework

**Repository:** [`quantum-logical-framework`](README.md)
**Document:** `Gravity.md` — the conceptual overview of gravity in [QLF](README.md).

> **Two gravity docs, one story.** This doc is the **conceptual foundation** — *what* gravity is in
> QLF and *why* it emerges. The companion [`Gravity_From_Delay.md`](Gravity_From_Delay.md) is the
> **quantitative engine** — Newton's law, `G`, the strength of gravity `α_G`, horizon temperatures,
> and the Bekenstein-bound derivation, all Lean-anchored. Read this for the picture; read that for the
> arithmetic. The two are complementary, not redundant.

## Abstract

Gravity is **not** a fundamental force or the curvature of a pre-existing spacetime. It is the
**relational distortion** that emerges when the full Zero Free Action (ZFA) network of distinctions is
partially deconstructed by an observer's Markov blanket. Unresolved distinctions cannot vanish; they are
screened **holographically** on the blanket boundary, and the accumulated information gradient is what
pulls masses together. Every quantitative statement below reduces to two substrate primitives — the
holographic surface event count `4π R²` and the per-event `log 2` quantum — so gravity, black-hole
thermodynamics, and cosmic acceleration are one algebraic phenomenon read at different scales.

## 1. Emergence from deconstruction

The complete ZFA history string is a flat relational web of balanced distinctions. Entropy (tracing-out
beyond the Markov blanket) deconstructs this web into a single consistent observer slicing. The
unresolved distinctions must be screened on the holographic boundary, and this screening produces:

- **local contraction** around high-density gauge-folded regions — gravity;
- **future-directed expansion** in low-density regions — the dark-energy equivalent.

No extra fields and no spacetime background are required: gravity is the geometric back-reaction to
logical information hiding. This is the substrate-language form of Jacobson's *Einstein equation of
state* (1995) and Verlinde's *entropic gravity* (2011) — both now derived from QLF primitives
([`Einstein_Equations.md`](Einstein_Equations.md), [`Gravity_From_Delay.md`](Gravity_From_Delay.md)).

## 2. Gauge folding — the microscopic source

The presence of **local gauge twists** (`+` and `−`) determines whether a closure acts as a gravity
source:

- **Gauge-folded closures** (`+`–`−`) are primordial quantum black holes. Their constructing delay
  `Δt = R/f` (topological depth `R` at vacuum frequency `f`) creates **local time** inside the fold;
  the high logical density biases the spin network inward — gravity.
- **Non-gauge closures** (no `+`/`−`) are massless: they create **local space** only (zero temporal
  depth), with no constructing delay and no local contraction.

The density-dependent space/time role swap — high density makes *time* the dominant local axis — is the
substrate mechanism of geodesic deviation and curvature. A gauge-folded closure is literally a
sub-Planck black hole whose horizon is its own Markov blanket (the Compton–Schwarzschild self-dual point
`μ²=1/2`, [`QLF_PlanckScale`](lean/QLF_PlanckScale.lean), [`Planck_Scale.md`](Planck_Scale.md)); the same
primitive at the hadronic extreme is [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md).

Every synthesized closure is classified automatically by the QuCalc engine
([`particles.py`](particles.py)): a `+`–`−` fold reports `primordial_BH`, "creates local: time", "high
logical density → time is the local axis", and its Hawking radiation channel. That inward bias passes
directly into the spin-network geometry, reproducing Newtonian gravity, the post-Newtonian corrections,
and the Schwarzschild metric as emergent coarse-grained limits — with no new fields.

| Entity | Fold type | Local axis | Logical density | Geometric effect | Emergent phenomenon |
|---|---|---|---|---|---|
| Primordial quantum BH | `+`–`−` | Time | High | Inward radial bias | Gravity (local contraction) |
| Massless closure | no `+`–`−` | Space | Low | Transverse expansion | Null geodesics / propagation |
| Cosmological vacuum | Mixed | Density-dependent swap | Average | Net future-expansion bias | Dark energy |

## 3. The quantitative program — an index

The qualitative picture above is backed by a Lean-anchored quantitative program. Gravity is no longer a
single result but a **sector**: every entry below reuses the same `4π R²` count and per-event `log 2`.

| Result | Value / status | Lean module | Doc |
|---|---|---|---|
| **Newton's law `F = GMm/r²`** | structural (`1/r²` = the 3D substrate signature) | [`QLF_GravityFromDelay`](lean/QLF_GravityFromDelay.lean) | [`Gravity_From_Delay.md`](Gravity_From_Delay.md) |
| **`G`'s structural form `L_P²c³/ℏ`** | unit-conversion bookkeeping (Planck units `G=1`) | `QLF_GravityFromDelay` | Gravity_From_Delay §8 |
| **Strength of gravity `α_G = exp(−28π)`** | 0.068% on the log (from the integer `b₀=7`) | [`QLF_GravitationalCoupling`](lean/QLF_GravitationalCoupling.lean) | Gravity_From_Delay §1.1 |
| **Einstein equations as equation of state** | coefficient `8πG=2π/η`, `Λ=log 2` (Jacobson skeleton) | [`QLF_EinsteinEquations`](lean/QLF_EinsteinEquations.lean) | [`Einstein_Equations.md`](Einstein_Equations.md) |
| **Horizon temperatures (Unruh/Hawking/de Sitter)** | one Unruh master relation `T=ℏa/2πck_B`, three `a` | [`QLF_HorizonTemperature`](lean/QLF_HorizonTemperature.lean) | Gravity_From_Delay §5.1 |
| **Holographic entropy `S=4πR²log2`; BH residual `4 log 2`** | residual = derived product (Einstein quarter × `log 2`) | [`QLF_HolographicDensity`](lean/QLF_HolographicDensity.lean) | Gravity_From_Delay §9 |
| **Planck length = the closure floor** | by construction (`μ²=1/2`), not a posit | [`QLF_PlanckScale`](lean/QLF_PlanckScale.lean) | [`Planck_Scale.md`](Planck_Scale.md) |
| **Substrate = a spin network of half-spin closures (LQG)** | entropy-count correspondence, `γ` fixed | [`QLF_LoopQuantumGravity`](lean/QLF_LoopQuantumGravity.lean) | [`LQG_QLF.md`](LQG_QLF.md) |
| **Schwarzschild weak-field metric** | `g_tt`/`g_rr` from Cross-Frequency Lorentz | (Mercury module) | [`GR_Schwarzschild.md`](GR_Schwarzschild.md) |
| **Mercury perihelion 42.99″/century** | **0.03%** vs Park et al. 2017 | [`QLF_MercuryPerihelion`](lean/QLF_MercuryPerihelion.lean) | [`Mercury_Perihelion.md`](Mercury_Perihelion.md) |
| **Cosmological constant `Ω_Λ = log 2`** | 1.2%, closing the 10¹²² catastrophe | [`QLF_CosmologicalConstant`](lean/QLF_CosmologicalConstant.lean) | [`Cosmological_Constant.md`](Cosmological_Constant.md) |
| **Dark matter / MOND `a₀ = cH₀/2π`** | parameter-free SPARC fit (0.133 dex) | [`QLF_DarkMatter`](lean/QLF_DarkMatter.lean) | [`DarkMatter.md`](DarkMatter.md) |
| **Casimir / accelerated-boundary Unruh** | finite census + `1/a⁴` + shared Unruh `T` | [`QLF_Casimir`](lean/QLF_Casimir.lean) | [`VacuumEnergy.md`](VacuumEnergy.md) §4 |
| **Curvature side (causal-set order→metric)** | number↔volume, BD curvature, one continuum bridge | [`QLF_CausalInterval`](lean/QLF_CausalInterval.lean) + | Einstein_Equations §6a |
| **Gravitational waves — linearized wave equation** | `□_d δρ = 0` (density-perturbation route); speed `c`, spin-2, 2 polarizations; quadrupole leading | [`QLF_GravitationalWaves`](lean/QLF_GravitationalWaves.lean) | [`GR_Schwarzschild.md`](GR_Schwarzschild.md) |

**The dark sector is one root.** `Ω_Λ = log 2`, the horizon temperatures, and the dark-matter scale
`a₀ = cH₀/(2π)` all hang on **one Hubble horizon and one `2π`** (the substrate loop phase, the same `2π`
of `g−2 = α/2π`) — so the holographic counting of this doc is the common source of the whole dark sector
(`mond_accel_is_hubble_over_loop`, [`DarkMatter.md`](DarkMatter.md)).

## 4. Honest scope

- **Derived:** the *form* of Newton's law, the dimensionless *strength* `α_G`, the horizon
  thermodynamics, the Einstein-equation coefficient + `Λ`, and the dark-sector scales — all from the two
  primitives (`4π R²`, `log 2`) plus the substrate 3-dimensionality.
- **Bookkeeping:** the SI *value* of `G` (a kilogram/metre convention), not a separate empirical input.
- **Open:** the full nonlinear tensor **curvature side** of the Einstein equations (a concrete
  causal-set order→metric program, not generic missing geometry —
  [`Einstein_Equations.md`](Einstein_Equations.md) §6a); the gravitational-wave dynamics *beyond* the
  linearized wave equation (`□_d δρ = 0` is now anchored via the density-perturbation route, §3 table —
  what remains is deriving the wave operator from the SOC rate equations + the luminosity coefficient
  `G/(5c⁵)`); and the absolute mass scale feeding absolute `G` (frontier #1, now reduced to the single
  SOC observable `ρ*`). See [`Gravity_From_Delay.md`](Gravity_From_Delay.md) §9 for the full three-tier
  scoping.

## 4a. `G` reduced to one number, and that number tested ([`gravitational_constant.py`](gravitational_constant.py))

The physics in `G` is `α_G = (m_p/M_Pl)²`. QLF reaches it through `ln(M_Pl/m_p) = 2π/(b₀ α_s)`, with
`b₀ = 7` and the posit `α_s(substrate) = 1/b₀² = 1/49` ([`QLF_AlphaS`](lean/QLF_AlphaS.lean)): `14π`, so
`α_G = e^{−28π}`, 0.068 % on the log and 6.2 % on the value. The predictions below were fixed in the commit
that added the script (`a128472`), before the continuum check ran.

**`G` is exactly one number.** Measured `G` and `m_p` fix the coupling the `14π` route needs:

> **`1/α_s(substrate) = 7 ln(M_Pl/m_p)/(2π) = 49.03355`**, uncertainty `±1 × 10⁻⁵` from `G` itself.

So everything open about `G` — and about `α_G`, and the proton's absolute depth — is the residual **`+0.0336`**
on the posit `b₀² = 49`. It has the same shape as `α⁻¹ = 137 + 0.036`.

**Standard running does not supply it — 63σ.** Running the measured `α_s(M_Z) = 0.1180(9)` up to the
(non-reduced) Planck mass in MS-bar, with the top threshold, gives `1/α_s(M_Pl) = 52.48` at one loop and
`53.02` at two and three loops, with uncertainty `±0.063`. That is `4.0` (8 %) from what `G` requires, `63σ`
away. The posit's stated support ("the measured running gives `≈ 52 ≈ 49`, ~7 %") holds at one loop only.
At the orders that matter, the gap is 8 %, so the physical coupling at the Planck mass is **not** what makes
`14π` work. The prediction that it would not was fixed in advance, and it held. The `14π` match stands as a
structural identification that standard physics does not explain.

**α's census tail does not transfer.** At `α`'s bare coupling `1/128` the census tails bracket `α`'s residual.
At `α_s`'s bare coupling `1/49` they bracket `[0.043, 0.131]`, which excludes `+0.0336`. This was computed
while scoping and is recorded as such. It fails in the same way the ½ mix failed on the proton
([`Alpha_Residual.md`](Alpha_Residual.md) §9o).

**An observation, not a claim.** The residual `0.0336` sits near `α`'s `0.036` (ratio `0.93`). Close numbers
are not evidence ([`Alpha_Residual.md`](Alpha_Residual.md) §9k). A shared mechanism would have to predict that
ratio, and none is proposed. What this section establishes: `G`'s open content is **one number, known to
`10⁻⁵`**, and **not** the Standard Model coupling at the Planck mass.

## 5. Ties to other documents

- [`Gravity_From_Delay.md`](Gravity_From_Delay.md) — **the quantitative companion**: the full Newton /
  `G` / `α_G` / horizon-temperature derivation this doc indexes.
- [`Einstein_Equations.md`](Einstein_Equations.md) & [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md)
  §5 — the Einstein equation of state from `δQ = T δS` at each local (Markov-blanket) clock.
- [`Curvature.md`](Curvature.md) — gravity as the isotropic single-sign deformation of the primordial
  Markov blanket (the Moon-orbit inflow worked example).
- [`SpaceTime.md`](SpaceTime.md) & [`Time.md`](Time.md) — the density-dependent role swap as the origin
  of relativistic frames; gravity as the **local departure from the statistically uniform stateless
  ether**, the same uniformity from which Lorentz invariance emerges.
- [`Entropy.md`](Entropy.md) — gravity screens unresolved distinctions (area law `S = A/4ℓ_P²`).
- [`Frequency_Synchronization.md`](Frequency_Synchronization.md) — constructing delay `R/f` as the
  source of local time.
- [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md) & [`BLACK-HOLES.md`](BLACK-HOLES.md) — the particle ↔
  black-hole equivalence at the hadronic / Planck-blanket extreme.
- [`Hierarchical_Control.md`](Hierarchical_Control.md) — gravity as the macroscopic top-down constraint;
  cosmic-horizon entropy as the highest-level prior.
- [`Quantum_Gravity.md`](Quantum_Gravity.md) — master synthesis tying gravity, holography, cosmic
  expansion, and ER=EPR as four faces of one algebraic event.

## Conclusion

Gravity in QLF is the inevitable geometric consequence of entropy deconstruction inside a ZFA-complete
logical web. The gauge-folding rule makes it computable at the particle scale — only primordial black
holes (`+`–`−` folds) curve space locally, while the same mechanism produces cosmic acceleration
globally. General relativity emerges as the effective, coarse-grained description of QuCalc folds; the
quantitative sector (§3) shows how far that emergence has been carried, and
[`Gravity_From_Delay.md`](Gravity_From_Delay.md) shows the arithmetic.
