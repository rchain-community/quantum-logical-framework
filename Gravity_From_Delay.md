# Gravity from substrate time delay: G and Newton's law from holographic event-counting

**Scoping doc — Newton's law `F = G M m / r²` from [QLF](README.md) substrate primitives.** Every interaction takes one Planck tick per Planck length: round-trip between two masses at distance `r` requires `R = r / L_Planck` substrate ticks. During the delay, vacuum events accumulate on the holographic boundary enclosing each mass. The accumulated entropy gradient pulls the masses together — Verlinde's entropic-gravity derivation, but with the substrate event count and per-event `log 2` quantum as the only inputs.

**G is unit-conversion bookkeeping.** In QLF's substrate-first ontology, `L_Planck` and `τ_Planck` are *primitives* (one of each per substrate event). The Planck mass `M_Planck = E_Planck / c² = ℏ / (c² τ_Planck)` follows. Newton's constant `G = L_Planck³ / (M_Planck τ_Planck²)` is then just the ratio of substrate primitives expressed in SI units — its CODATA value `6.674 × 10⁻¹¹ m³/(kg·s²)` is the SI calibration of the substrate event quantum, not a separate empirical input.

**1/r² is the 3D substrate signature.** The 1/r² fall-off follows from substrate surface-area scaling `~R²` in 3 spatial dimensions. The 3-dimensionality of the substrate comes from the 8-twist alphabet's 6+2 split (6 spatial twists = 3 axis pairs, [`Magic_numbers.md`](Magic_numbers.md)). Counterfactual: in d spatial dimensions Newton's law would be `F ∝ 1/r^(d−1)`. The observed 1/r² is a structural prediction tied to the substrate 3D, the same 3D that produced α via the `N = 9 = 3²` directional tensor.

---

## §1 The G question

Newton's constant has the value `G = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²` in SI. In Planck units G = 1 by definition (since L_Planck, τ_Planck, M_Planck are *defined* from {ℏ, c, G}). Standard physics offers no first-principles derivation of why G has this numerical value — it is taken as a fundamental constant of nature.

**The QLF substrate reading.** L_Planck and τ_Planck are *substrate primitives* — one Planck length and one Planck tick per substrate event, *together* ([`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3, Lean-anchored in [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean)). The Planck mass is then `M_Planck = ℏ / (c² τ_Planck) = ℏ / (c · L_Planck)` — the rest-energy of a single Planck-event qubit. Newton's constant follows:

$$G \;=\; \frac{L_{\text{Planck}}^3}{M_{\text{Planck}} \, \tau_{\text{Planck}}^2} \;=\; \frac{L_{\text{Planck}}^2 \, c^3}{\hbar}$$

The SI numerical value 6.67430 × 10⁻¹¹ reflects the calibration of substrate event quantum to SI units — not a separate empirical input.

**The deeper question.** Why does gravity have the *form* `F ∝ M m / r²`, with `G` as the coefficient? This is the Verlinde-style entropic-gravity question, and QLF substrate primitives answer it directly.

### §1.1 The strength of gravity: `α_G = exp(−28π)`

The SI *value* of `G` is a unit convention (what a kilogram is), but the **physics** content of `G` — *how weak gravity is* — is dimensionless and **derived**. The gravitational coupling (the "gravitational fine-structure constant") is

$$\alpha_G \;=\; \frac{G\,m_p^2}{\hbar c} \;=\; \left(\frac{m_p}{M_{\rm Planck}}\right)^2 \;\approx\; 5.9\times10^{-39}.$$

QLF already derives the mass hierarchy `ln(M_Planck/m_p) = 14π` (dimensional transmutation from the single integer `b₀ = 7`, [`QLF_AlphaS`](lean/QLF_AlphaS.lean)). Since `m_p/M_Planck = exp(−ln(M_Planck/m_p))`, the coupling is its square:

$$\alpha_G \;=\; \exp\!\bigl(-2\,\ln(M_{\rm Planck}/m_p)\bigr) \;=\; \exp(-28\pi).$$

**Machine-verified** ([`lean/QLF_GravitationalCoupling.lean`](lean/QLF_GravitationalCoupling.lean)): `alpha_G_is_ratio_sq` (`α_G = (m_p/M_Pl)²`), `alpha_G_eq_exp_neg_28pi` (at `14π`), and `substrate_gravitational_coupling` (end-to-end from `b₀ = 7`). Numerically `exp(−28π) = 6.27×10⁻³⁹` vs. measured `5.91×10⁻³⁹` — **0.068% on the log**, 6.2% on the value (the exp-sensitivity of the `14π` hierarchy, exactly as `QLF_AlphaS.hierarchy_log_band`). So *the strength of gravity is derived from the single substrate integer `7`*, and the absolute SI `G = α_G·ℏc/m_p²` needs only `m_p`'s SI value (a kilogram convention) — not new physics. (The electron coupling is `α_G^e = (m_e/M_Pl)²` with `m_e = m_p/6π⁵`, so it too follows from the one hierarchy.)

**How absolute `G` improves once the electroweak scale is pinned** (issue [#136](https://github.com/jimscarver/quantum-logical-framework/issues/136)). Absolute `G = α_G·ℏc/m_p²` splits into two independent residuals: (i) the **dimensionless coupling** `α_G = exp(−28π)` — derived from `b₀=7`, above; and (ii) the **mass-scale / hierarchy half** carried by `m_p`, which is tied to the same electroweak scale `v ↔ R_stable = 1/ρ*` now closed structurally to the single SOC observable `ρ* = √(c/k)` (frontier #1: `QLF_ClosureAttraction` → `QLF_SteadyStateDensity` → `QLF_ElectroweakScale`). So **once `ρ*` is known, the mass-scale half of absolute `G` becomes a prediction rather than a kilogram-convention calibration**. The separate **holographic-density residual** (why horizon entropy is `N/4` not `N log 2`, residual exactly `4 log 2`, `QLF_HolographicDensity`) is *independent* of the gauge-fold packing density and remains open. So absolute `G`'s residual is `{α_G` ✓, `ρ*}` + the entropy-normalization factor — the amount previously carried by the unknown scale converts to a prediction, the entropy piece does not.

**Bracketing `α_G` (hence `G`), and the `α` relation.** Because `α_G = exp(−2·hierLog)` is exp-sensitive, the *value* bracket follows the mass-hierarchy band `ln(M_Pl/m_p) ∈ [14π, 104π/7]` (`QLF_AlphaS.hierarchy_log_band`, the running-consistent `α_s ∈ [1/52, 1/49]` window): `α_G ∈ [exp(−208π/7), exp(−28π)] ≈ [2.87×10⁻⁴¹, 6.27×10⁻³⁹]` (`alpha_G_bracket`) — which **contains** the measured `5.91×10⁻³⁹`, near the *upper* (`14π`, `b₀²=49`) edge. **The bracket width is set by `α_s` (strong), not `α` (EM):** committing to `α_s = 1/b₀²` collapses it to the *point* `exp(−28π)` (0.068% on the log), so `α` does not tighten the absolute `G`. Where `α` *does* meet gravity is the dimensionless **EM/gravity force ratio** between two protons, `α/α_G = (1/137)/exp(−28π) = exp(28π)/137` (`em_gravity_coupling_ratio`) — QLF `1.16×10³⁶` vs. measured `1.24×10³⁶` (6%, the same exp-sensitivity) — a real prediction combining *both* substrate constants, but bracketing the gravity-vs-EM *comparison* rather than `G` alone.

The *other* piece of the absolute `G` — the **entropy normalization** `η`/the Bekenstein–Hawking `4 log 2` residual (§4, [`QLF_HolographicDensity`](lean/QLF_HolographicDensity.lean)) — is separate: it touches the absolute *entropy*, not `α_G`, and the `1/r²` law is normalization-independent. The accelerating-Casimir / Unruh temperature is the relevant tool *there* (shared Unruh `T`), not for `α_G`.

---

## §2 Substrate event quantum and the time delay

Per the substrate event quantum ([`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3): every substrate event creates **one Planck length** of spatial extent and **one Planck tick** of duration, *together*. The speed of light `c = L_Planck / τ_Planck` is the ratio of substrate primitives — Lean-anchored as `substrate_light_speed_from_cosmic_ratio` in [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean).

**Time delay for an interaction at distance `r`.** Two masses separated by `r` exchange gauge-twist closures (the substrate primitive for any interaction). The round-trip delay is

$$\Delta t \;=\; \frac{2 r}{c} \;=\; 2 r / c \;=\; 2 R \, \tau_{\text{Planck}}, \qquad R \;\equiv\; r / L_{\text{Planck}}.$$

During the delay, vacuum substrate events accumulate on the topological boundary enclosing each mass. Each event holds `log 2` nats of information ([`MRE.md`](MRE.md), Lean-anchored as `zfa_closure_minimizes_free_energy` in [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)).

The accumulated information *on the holographic boundary* (not in the bulk) generates the gravitational coupling. The key step: how many substrate events sit on a holographic boundary of radius R?

---

## §3 Holographic surface event count: 4π R²

(See [`Primordial_Markov_Blankets.md`](Primordial_Markov_Blankets.md) for the discrete-geometric reading: this `4π R²` event count IS the face count `F_v = 20 v²` of a Fuller frequency-`v(R) = √(π/5)·R/L_Planck` primordial geodesic-sphere Markov blanket with icosahedral symmetry. The substrate's holographic boundary is a discrete geodesic sphere, not a continuous 2-manifold.)

A 2-sphere of physical radius `r` has area `A = 4π r²`. In substrate units, the boundary holds

$$N \;=\; \frac{A}{L_{\text{Planck}}^2} \;=\; 4 \pi \, R^2$$

independent substrate events. Each event is one Planck-length × Planck-length patch of the holographic surface; each one hosts one half-spin ZFA closure.

**Why R² (not R³)?** Substrate-event counting on the 2D boundary, not the 3D bulk. The Bekenstein-Hawking holographic principle says all the information about the bulk is encoded on the boundary — substrate events on the boundary are the substrate-language statement of this. The factor `4π` is the solid angle (one of two factors in the `8π` Einstein-equation coefficient, Lean-anchored as `einstein_eight_pi_decomposition` in [`lean/QLF_EinsteinGeometricFactor.lean`](lean/QLF_EinsteinGeometricFactor.lean)).

**3-dimensionality of the substrate is the structural ingredient.** In `d` spatial dimensions, a `(d−1)`-dimensional holographic boundary at radius `r` has `N ∝ r^(d−1)` substrate events. For QLF's 3D spatial substrate (derived from the 8-twist 6+2 split, [`Magic_numbers.md`](Magic_numbers.md)): `N ∝ R²`. This is what gives Newton's law its `1/r²` form (§7 below).

---

## §4 Entropy on the holographic horizon

Each substrate event holds `log 2` nats of information (per-event MRE quantum, Lean-anchored). Total entropy on the holographic surface:

$$S \;=\; N \cdot \log 2 \;=\; 4\pi R^2 \log 2 \;=\; \frac{4 \pi r^2 \log 2}{L_{\text{Planck}}^2}.$$

Multiplied by `k_B` for SI thermodynamic units: `S = (4π r²/L_Planck²) × k_B log 2`. Compared with the Bekenstein–Hawking horizon entropy `S_BH = k_B A / (4 L_Planck²)`, the ratio is **exactly `S_QLF/S_BH = 4 log 2 ≈ 2.7726`** — QLF's naive one-bit-per-Planck-patch count exceeds the realized thermodynamic entropy by this factor (machine-verified: `holographic_bh_ratio`, [`lean/QLF_HolographicDensity.lean`](lean/QLF_HolographicDensity.lean); this corrects an earlier schematic `≈5.77`). **The residual is not a free parameter** — it is a *product of two already-derived QLF constants*: the **`4`** (the Einstein `8π = 4π·2` factor / the entropy density `η = 1/4G`, `QLF_EinsteinEquations`/`QLF_EinsteinGeometricFactor`) times the **`log 2`** per-event quantum (`QLF_FreeEnergy`) — `residual_is_quarter_times_quantum`. And the `1/r²` force law + structural `G` are **residual-independent** (the normalization cancels in `F = T dS/dx`), so this touches only the *absolute* entropy/`G` normalization. (Honest scope: *why* the realized horizon entropy is the thermodynamic `N/4` rather than the naive `N·log 2` is the open classification — but it is **two-way now, not three**: the correlation/packing branch is **closed**, since a fraction `p/q` of independent patches would force `log 2` rational (`no_rational_packing_factor`) and the required `1/(4 log 2)` is irrational. What remains is a genuine discrete-floor deviation vs. an area-element redefinition, with the weight on the latter — the suppression would have to cancel the very quantum it suppresses, leaving `N/4` with no `log 2` in it (`suppression_cancels_the_quantum`). See §9.)

The point for gravity derivation: entropy is `S ∝ R² × log 2 × k_B`, with the per-event `log 2` quantum carrying the substrate origin.

---

## §5 Vacuum temperature on the horizon

The horizon hosts `N = 4π R²` substrate events, sharing the total energy `M c²` of the enclosed mass `M`. Equipartition gives each event `(1/2) k_B T` of energy:

$$N \cdot \frac{1}{2} k_B T \;=\; M c^2 \;\Rightarrow\; T \;=\; \frac{2 M c^2}{N k_B} \;=\; \frac{M c^2}{2 \pi R^2 k_B}.$$

This is the substrate analog of the Unruh / Bekenstein-Hawking temperature. Notice the scaling: `T ∝ M / r²` — already 1/r² appearing in the temperature, because the surface event count scales as r² in 3D.

In substrate units (substituting `R = r/L_Planck`):

$$T \;=\; \frac{M c^2 L_{\text{Planck}}^2}{2 \pi r^2 k_B}.$$

**This is where G appears.** Substituting `L_Planck² = ℏ G / c³`:

$$T \;=\; \frac{M G \, \hbar}{2 \pi r^2 c \, k_B}.$$

— the standard Unruh-like horizon temperature, with G arising from the substrate event quantum via `L_Planck² = ℏ G / c³`.

### §5.1 The canonical surface-gravity temperature: one relation, three horizons

The equipartition estimate above (`T ∝ M/r²`, a *shell* temperature) is distinct from the
**canonical** horizon temperature `T ∝ 1/M`, which QLF Lean-anchors
([`QLF_HorizonTemperature.lean`](lean/QLF_HorizonTemperature.lean)). Every horizon temperature
is the **Unruh master relation** at the appropriate acceleration `a`, with the universal `2π`
being the **substrate loop phase** — the same `2π` of one full closure that appears in
`g−2 = α/2π` ([`QLF_GMinusTwo.lean`](lean/QLF_GMinusTwo.lean)):

$$T \;=\; \frac{\hbar\, a}{2\pi c\, k_B}$$
(Lean: `unruh_temperature`.)

The three classic temperatures are three values of `a`:

| temperature | acceleration `a` | result | Lean |
|---|---|---|---|
| **Unruh** | proper acceleration `a` | `ℏa/(2πck_B)` | `unruh_temperature` |
| **Hawking** | surface gravity `κ = c⁴/(4GM)` | `ℏc³/(8πGMk_B)` | `hawking_temperature_eq` |
| **de Sitter** | `cH₀ = c²/R_H` | `ℏH₀/(2πk_B)` | `desitter_temperature_eq` |

Hawking's `8π` is the loop `2π` times the `4` in the Schwarzschild surface gravity
`κ = c⁴/(4GM)` — the *same* `8π` as Einstein's `8π = 4π·2`
([`QLF_EinsteinGeometricFactor.lean`](lean/QLF_EinsteinGeometricFactor.lean)). `hawking_is_unruh`
/ `desitter_is_unruh` show both are literally the one relation at different `a`.

**Dark-sector closure.** The de Sitter acceleration `cH₀` is exactly the `hubble_acceleration`
of [`QLF_DarkMatter.lean`](lean/QLF_DarkMatter.lean), and the dark-matter / MOND scale is that
same acceleration reduced by the loop phase: `a₀ = cH₀/(2π) = a_dS/(2π)`
(`mond_accel_is_hubble_over_loop`). So `Ω_Λ = log 2` (`QLF_CosmologicalConstant`), the horizon
temperature, and the dark-matter scale all hang on **one Hubble horizon and one `2π`**. Honest
scope: this is the algebraic unification + the identification of the `2π` as the loop phase,
not a from-scratch QFT-in-curved-spacetime derivation (`horizon_temperature_constructive`).

---

## §6 Bekenstein bound at horizon crossing

A test mass `m` crossing the horizon advances by one Compton wavelength `λ_C = ℏ / (m c)` per Bekenstein cycle. The entropy change for the horizon-crossing is

$$dS \;=\; \frac{2 \pi k_B \, m c}{\hbar} \, dx$$

(Bekenstein 1973, holds for any quantum mechanical particle). In substrate language: each Compton-cycle motion adds one Planck-event closure to the horizon's substrate-event ledger; the `2π` is the angular phase per Compton cycle.

The Bekenstein bound is a quantum-mechanical fact that QLF doesn't yet Lean-anchor at the substrate level (Tier-3 open). But its form is natural: `dS/dx = (2π/λ_C) × k_B = 2π m c k_B / ℏ`, reading as "one substrate event per Compton wavelength of motion."

---

## §7 Force from entropy gradient: F = G M m / r²

Combining §5 (temperature) and §6 (entropy gradient):

$$F \;=\; T \cdot \frac{dS}{dx} \;=\; \frac{M G \hbar}{2\pi r^2 c k_B} \cdot \frac{2 \pi m c k_B}{\hbar} \;=\; \boxed{\frac{G M m}{r^2}}.$$

**Newton's law of gravitation falls out**, with G appearing exactly as the coefficient via `L_Planck² = ℏ G / c³` in the substrate event quantum.

### §7.1 Structural decomposition

| Factor | Substrate origin | Reference |
|---|---|---|
| `1/r²` | Holographic surface event count `N = 4π R²` (3D substrate from 8-twist 6+2 split) | §3, [`Magic_numbers.md`](Magic_numbers.md) |
| `M` | Total energy on horizon, distributed by equipartition over `N` events | §5 |
| `m` | Bekenstein entropy gradient `dS/dx ∝ m c k_B / ℏ` | §6 |
| `G` | Substrate event quantum `L_Planck² = ℏ G / c³` (definitional in QLF substrate) | §2 |
| `4π` | Solid angle (one of two factors in Einstein equation's `8π`, Lean-anchored) | §3 |

The `4π` cancels in the final force formula because it appears once in `N` (numerator of equipartition) and once in the temperature's `(2π R²)` (numerator). The remaining `4π → 1` cancellation is exact in the standard Verlinde derivation.

### §7.2 Counterfactual: dimensional dependence of gravity

In `d` spatial dimensions, the holographic boundary at radius `r` has `N ∝ r^(d−1)` substrate events. The same derivation gives:

$$F \;\propto\; \frac{M m}{r^{d-1}}.$$

For QLF's 3D substrate: `d = 3`, force `∝ 1/r²` — Newton's law. Counterfactual: in 2D substrate Newton's law would be `1/r¹`; in 4D substrate `1/r³`. The observed `1/r²` falls-off **is a structural prediction tied to the 3-dimensionality of the substrate**, the same 3D that produced α via the `N = 9 = 3²` directional tensor in [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean).

This ties Newton's law structurally to the same 6+2 alphabet split that produces α and the nuclear magic numbers — the substrate's 3-dimensionality is the common-source predictor.

---

## §8 G in SI: unit-conversion bookkeeping

In QLF's substrate-first ontology, `L_Planck` and `τ_Planck` are *primitives* (one per substrate event), and `M_Planck = ℏ / (c² τ_Planck)`. Newton's constant in SI is then

$$G \;=\; \frac{L_{\text{Planck}}^3}{M_{\text{Planck}} \, \tau_{\text{Planck}}^2} \;=\; \frac{L_{\text{Planck}}^2 \, c^3}{\hbar}.$$

The CODATA value `G = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²` is the SI calibration of the substrate event quantum — not a separate empirical input. In Planck units G = 1.

**Substrate Tier 1 (structural):** the *form* of Newton's law `F ∝ M m / r²` and the dimensional structure of G fall out from §§3–7. **Tier 2 (numerical):** G in SI = bookkeeping. **Tier 3 (open):** if one wants to *predict* the SI value of G from substrate alone, one would need to derive L_Planck (or M_Planck) in terms of standard observable inputs — the same Planck-scale question that asks "why is the proton 10¹⁹ Planck masses smaller than the Planck mass?" That is the hierarchy problem, scoped in [`HadronicDepth.md`](HadronicDepth.md).

### §8.1 The hierarchy is the blanket-depth (frequency) distribution

That Tier-3 question — why is the proton `~10¹⁹` Planck masses light, equivalently why is `G` so weak — is, in QLF, the **depth/frequency distribution itself**. A particle's mass is its Markov-blanket depth, `R = m_Planck/m = E_Planck/(mc²) = 1/ω` ([`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md)): heavy = shallow (high frequency), light = deep (low frequency). The Planck-to-proton hierarchy is then a ratio of blanket depths, and gravity's weakness falls out exactly:

$$\frac{F_\text{grav}}{F_\text{EM}}\bigg|_{pp} \;=\; \frac{G\,m_p^2}{e^2/4\pi\varepsilon_0} \;=\; \frac{1}{\alpha}\left(\frac{m_p}{m_\text{Planck}}\right)^2 \;=\; \frac{1}{\alpha\,R_p^{\,2}} \;\approx\; 8.1\times10^{-37}.$$

[`gravity_emergence_demo.py`](gravity_emergence_demo.py) confirms this to a ratio of `1.000000` against the direct value (textbook `~8×10⁻³⁷`). **Gravity is weak precisely because the proton sits ~10¹⁹ Planck-depths down** — the gravitational hierarchy *is* the proton's blanket depth squared, and the only constant in it is `α`, which QLF derives from the substrate (`alpha_QLF_eq`, 0.026%; [`Alpha.md`](Alpha.md), [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1).

**The Planck *scale* follows by construction; only its SI *value* and the matter depth are inputs.** The Planck *scale* is the **minimal coherent-closure length** — the Compton–Schwarzschild self-dual point `μ²=1/2`, below which a would-be blanket is inside its own horizon and cannot close ([`QLF_PlanckScale`](lean/QLF_PlanckScale.lean): `coherent_iff_subplanck`, `planck_length_floor`, `planck_self_dual`; [`Planck_Scale.md`](Planck_Scale.md)). So the substrate granularity follows **by construction** from QLF's own emergent gravity + blanket closure, not by posit. What is genuinely an input: (i) the Planck length's **SI value in metres** is a *unit convention*, not a physics question — "what a metre is" does not follow from logic; and (ii) **where the proton sits above the floor** (`R_p`) — the dimensional-transmutation hierarchy `ln R_p = 14π` ([`QLF_AlphaS`](lean/QLF_AlphaS.lean), 0.07%) with a residual few-% `M_Planck` calibration. The frequency distribution collapses the hierarchy from two numbers (`G` and `m_p`) to one (`R_p`); that one is the hierarchy problem — **separate from the granularity question**.

---

## §9 Honest scoping (three-tier)

**Tier 1 (structural — what falls out from substrate primitives).**

- The holographic surface event count `N = 4π R²` from substrate event-counting on the 2-sphere (3D substrate).
- Per-event `log 2` entropy (Lean-anchored).
- Equipartition of horizon energy `Mc²` across `N` events gives `T ∝ M/r²`.
- Bekenstein-form entropy gradient `dS/dx ∝ mc/ℏ` (form structural, Lean-anchoring open).
- Force from entropy gradient: `F = T · dS/dx = GMm/r²` (Newton's law).
- 1/r² is the 3D substrate signature (counterfactual: 2D → 1/r¹, 4D → 1/r³).

**Tier 2 (numerical).**

- G in SI = `L_Planck² c³/ℏ ≈ 6.674 × 10⁻¹¹ m³ kg⁻¹ s⁻²` — unit-conversion bookkeeping (no separate empirical input).
- 1/r² verified by all gravitational observations (Cavendish through binary pulsars).

**Tier 3 (open).**

- Substrate-event-counting prescription on the holographic boundary needs matching to continuous Bekenstein-Hawking `S = A/(4 L_Planck²)`. The residual is **exactly `4·log 2 ≈ 2.7726`** (`holographic_bh_ratio`), and the classification of *why* is **now two-way, not three**: the **packing branch is closed** — a correlation factor making a fraction `p/q` of patches independent would force `log 2 = q/(4p)`, i.e. rational (`no_rational_packing_factor`), and the required `1/(4 log 2) ≈ 0.360674` is irrational. Numerically the near misses bracket without touching: `C(2n,n)/4ⁿ` gives `0.375` at `n=2` (+4.0%) and `0.3125` at `n=3` (−13.4%); `1/e` is +2.0% off. Remaining: a genuine discrete-floor deviation from Bekenstein–Hawking, or an **area-element / what-counts-as-a-patch** redefinition — and `suppression_cancels_the_quantum` weights the latter, since `(N log 2)·(1/(4 log 2)) = N/4` contains **no `log 2` at all**, so the realized horizon entropy is not (a count) × (the per-event bit quantum). **Update (§9a):** the first law with QLF's own Hawking temperature closes branch (a), conditional on the first law holding in the mean at the horizon. Branch (b) is forced: one bit occupies `4 log 2 · L_P²`.
- Lean-anchor the holographic event count `N = 4π R²` from substrate Markov-blanket boundary topology.
- Lean-anchor the Bekenstein bound `dS = (2π m c k_B / ℏ) dx` substrate-derivation.
- GR-quantitative extensions: Mercury perihelion shift, gravitational lensing, GPS time dilation. The structural framing is in [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md); quantitative substrate derivation Tier-3 open.
- Predict numerical G from first principles independently of L_Planck (would reduce to the hierarchy problem, [`HadronicDepth.md`](HadronicDepth.md)).
- Strong-field corrections: derive the full Einstein equations from this substrate framework (the `8π` factor is Lean-anchored; the curvature-side derivation is open).

### §9a The first law fixes the normalization — *pre-registered 2026-09-29*

§4 and §9 leave the `4 log 2` residual as a choice between two branches: (a) a genuine discrete-floor
deviation from Bekenstein–Hawking, or (b) an area-element reading. This section tests a route the repo has
not used: the **first law** `dE = T dS` at a horizon.

QLF already proves the Hawking temperature, `T_H = ħc³/(8πGMk_B)` (`hawking_temperature_eq`,
[`lean/QLF_HorizonTemperature.lean`](lean/QLF_HorizonTemperature.lean), as the Unruh relation at the
surface gravity). With `E = Mc²`, the first law gives `dS/dM = c²/T_H = 8πGk_B M/(ħc)`. Up to an additive
constant, that forces `S = 4πGk_B M²/(ħc) = k_B A/(4L_P²)` on `R = 2GM/c²`. This is Hawking's 1975 route to
the `1/4`, not new. What is new is applying it inside QLF: with QLF's own temperature, the naive count
`N log 2 = 4 log 2 · S_BH` breaks the first law by exactly the residual.

**Pre-registered statements** (to be proved in `lean/QLF_HorizonFirstLaw.lean`, no new axioms):

| | Statement |
|---|---|
| F1 | `S_BH(M) = 4πGk_B M²/(ħc)` satisfies `dS/dM = c²/T_H` with QLF's `T_H` (a `HasDerivAt` statement) |
| F2 | `S_BH(M) = k_B A/(4L_P²)` with `A = 4π(2GM/c²)²` and `L_P² = ħG/c³` |
| F3 | the naive count `4 log 2 · S_BH` has `dS/dM · T_H = 4 log 2 · c² ≠ c²` |
| F4 | `1/2 < log 2 < 1`, so `4 log 2 ≠ 1` and `log 2 ≠ 1` |

**What the result would mean, and its conditions.** If F1–F4 hold, branch (a) is closed *given*
(i) QLF's Hawking temperature, which is proved; (ii) `E = Mc²` with `R = 2GM/c²`, which is the GR input;
and (iii) the first law holding at the horizon. In QLF, (iii) holds only in the mean, because energy
conservation is statistical ([`Conservation.md`](Conservation.md) §2a). Branch (b) would then be forced:
one bit occupies `4 log 2 · L_P²` of horizon, not `L_P²`. QLF's own Einstein coefficient already uses
`η = 1/4G` (`einstein_coupling_from_thermodynamics`), which points the same way.

**Consequence registered in advance for dark energy.** If branch (b) holds, §3 of
[`Cosmological_Constant.md`](Cosmological_Constant.md) overcounts its horizon entropy by `4 log 2`.
Counting with `S_BH` gives `Ω_Λ = 1/4` (keeping `f_gauge`) or `1` (dropping it, the §5.8 de Sitter value).
Neither is `log 2`, so the derivation of `Ω_Λ = log 2` would not survive.

**Failure:** any of F1–F4 fails to prove. Or QLF's horizon temperature turns out to differ from Hawking's,
which would reopen branch (a).

**Result (2026-09-29): all four proved**, no new axioms, in
[`lean/QLF_HorizonFirstLaw.lean`](lean/QLF_HorizonFirstLaw.lean): F1 `bh_entropy_first_law`, F2
`bhEntropyOfMass_eq_area`, F3 `naive_count_breaks_first_law`, F4 `half_lt_log_two` / `log_two_lt_one`. The
consequence is `firstlaw_count_omega`. The statements are the ones frozen above.

**What this settles.** Given the three conditions, branch (a) is closed: a horizon entropy of `N log 2`
would break the first law with QLF's own temperature by exactly `4 log 2`. Branch (b) is what remains:
the realized entropy is `A/(4L_P²)`, and a bit occupies `4 log 2 · L_P²` of horizon, not one Planck area.
The per-event `log 2` survives as the content of a bit. What changes is the count of bits, which is
`A/(4 log 2 · L_P²)`. The proof is for a Schwarzschild horizon. Applying it to the de Sitter horizon uses
the same area-per-bit rule, and Gibbons & Hawking (1977) give `A/4` there too.

**What it costs.** §3 of [`Cosmological_Constant.md`](Cosmological_Constant.md) derives `Ω_Λ = log 2` from
the uncorrected count. Recounted with the first-law entropy it gives `1/4` or `1` (§5.8 there), so that
derivation does not survive. The `(R/L_P)²` reduction of the `10¹²²` catastrophe is untouched, since it
does not depend on the O(1) prefactor. The `1/r²` law and structural `G` are untouched as well (§4).

---

## §10 What this is NOT

- **Not a derivation of G's numerical SI value from substrate alone.** G in SI is bookkeeping; the SI value reflects L_Planck calibration. The *form* of Newton's law and the *structural origin* of G fall out; the SI number is a downstream unit-system question.
- **Not a derivation of full Einstein equations.** Only Newton's `F = GMm/r²` (the weak-field static limit). The **linearized gravitational-wave equation** `□_d δρ = 0` is now anchored via the density-perturbation route ([`QLF_GravitationalWaves`](lean/QLF_GravitationalWaves.lean), the closure-density ripple `δρ` around the SOC `ρ*`); its dynamical-metric derivation (the wave operator from the SOC rate equations) and the quadrupole luminosity coefficient `G/(5c⁵)` remain Tier-3 open (§9). The **Mercury perihelion** (42.99″/century, 0.03% — [`QLF_MercuryPerihelion.lean`](lean/QLF_MercuryPerihelion.lean)) and the **cosmological constant** (`Ω_Λ = log 2`, 1.2% — [`QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)) have since been closed, both reusing the `4π R²` count and per-event `log 2` of this doc. The **dark-matter / MOND scale** `a₀ = cH₀/(2π)` ([`DarkMatter.md`](DarkMatter.md), [`QLF_DarkMatter.lean`](lean/QLF_DarkMatter.lean)) closes on the *same* Hubble horizon as `Ω_Λ` — the holographic counting here is the common root of the whole dark sector. Hadron-scale horizons are the same primitive at the Planck-blanket extreme ([`Hadron_BlackHoles.md`](Hadron_BlackHoles.md)).
- **Not a derivation of the hierarchy problem.** `M_Planck / m_proton ≈ 10¹⁹` is not explained here. That's the `R_p` derivation question scoped in [`HadronicDepth.md`](HadronicDepth.md) and [`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md).
- **Not a new physics claim.** Verlinde (2010) derived Newton's law from entropic gravity; this doc is the QLF substrate-event-count version of that derivation, with the per-event `log 2` and 4π R² counting being the substrate primitives.

---

## §11 References

### Internal

- [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3 — substrate event quantum (one Planck length × one Planck tick *together*); Gap 3 names G as "vacuum's per-event entropy-gradient strength."
- [`VacuumEnergy.md`](VacuumEnergy.md) §6 — vacuum-alignment principle as TOE-completing layer.
- [`MRE.md`](MRE.md) — per-event `log 2` information quantum.
- [`Magic_numbers.md`](Magic_numbers.md) — 3-dimensionality of the substrate from the 8-twist 6+2 split.
- [`HadronicDepth.md`](HadronicDepth.md) — Markov-blanket depths; the hierarchy `R_p ≈ 10¹⁹` question.
- [`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md) — `R_e = R_p · 6π⁵` chirality-hiding resonance.
- [`Gravity.md`](Gravity.md) — gravitational warping as top-down screening; qualitative companion.
- [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1 — substrate α from 3D directional tensor (sibling counterfactual).
- [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean) — `zfa_closure_minimizes_free_energy` (per-event log 2).
- [`lean/QLF_EinsteinGeometricFactor.lean`](lean/QLF_EinsteinGeometricFactor.lean) — `8π = 4π · 2` Einstein-equation factor.
- [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean) — `c = L_Planck / τ_Planck` substrate identity.
- [`lean/QLF_LocalClock.lean`](lean/QLF_LocalClock.lean) — `R = local clock count`.
- [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) — `N = 9 = 3²` 3D directional tensor (sibling 3D-substrate prediction).
- [`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) — Lean anchor for this module.
- [`gravity_delay_demo.py`](gravity_delay_demo.py) — numerical companion.
- [`Experimental_Consistency.md`](Experimental_Consistency.md) §8 — gravity scope; §10 falsifiers.

### External

- Verlinde, E. (2011). *On the Origin of Gravity and the Laws of Newton*. JHEP 04:029. [arXiv:1001.0785](https://arxiv.org/abs/1001.0785) — entropic gravity derivation this doc translates into substrate language.
- Jacobson, T. (1995). *Thermodynamics of Spacetime: The Einstein Equation of State*. Phys. Rev. Lett. 75, 1260 — earlier thermodynamic-gravity derivation.
- Bekenstein, J. D. (1973). *Black Holes and Entropy*. Phys. Rev. D 7, 2333 — original Bekenstein bound `dS = 2π m c k_B dx / ℏ`.
- Hawking, S. W. (1975). *Particle Creation by Black Holes*. Comm. Math. Phys. 43, 199 — Hawking temperature, related substrate identification. Also the first-law route to the `1/4` used in §9a.
- Gibbons, G. W., & Hawking, S. W. (1977). *Cosmological event horizons, thermodynamics, and particle creation*. Phys. Rev. D 15, 2738 — `A/4` for the de Sitter horizon (§9a).
- Padmanabhan, T. (2010). *Thermodynamical Aspects of Gravity*. Rep. Prog. Phys. 73, 046901 — review of thermodynamic-gravity derivations.
- Newton, I. (1687). *Philosophiae Naturalis Principia Mathematica*. — original gravitational inverse-square law.
- CODATA 2022 — `G = 6.67430 × 10⁻¹¹ m³ kg⁻¹ s⁻²`.
