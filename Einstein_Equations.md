# The Einstein equations as the substrate's equation of state

**Module:** [`lean/QLF_EinsteinEquations.lean`](lean/QLF_EinsteinEquations.lean) (#68)
**Companions:** [`GR_Schwarzschild.md`](GR_Schwarzschild.md) (the metric), [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.2 (the local-time reading), [`Gravity_From_Delay.md`](Gravity_From_Delay.md) (the area law), [`QLF_HorizonTemperature.lean`](lean/QLF_HorizonTemperature.lean) (the Unruh temperature), [`Cosmological_Constant.md`](Cosmological_Constant.md) (`Λ = Ω_Λ = log 2`), [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) §3b (**gravity as the fourth force** — the geometry of the same closures whose gauge-twist vertex gives EM/weak/strong; mass = constructing delay is the hinge).

---

## §1 The gap this closes

[QLF](README.md) already had Newton's law, `G = L_P²c³/ℏ`, the Mercury perihelion, and the weak-field
Schwarzschild metric — but the **full** field equations

$$
G_{\mu\nu} \;=\; \frac{8\pi G}{c^4}\, T_{\mu\nu}
$$

were flagged open: only the `8π = 4π·2` factor ([`QLF_EinsteinGeometricFactor`](lean/QLF_EinsteinGeometricFactor.lean))
and the weak-field limit ([`GR_Schwarzschild.md`](GR_Schwarzschild.md)) were anchored. The curvature
side — *why the field equations take the form they do at all* — was missing.

The honest route is **Jacobson (1995)**: the field equations as an equation of state.

---

## §2 Jacobson: the field equations are an equation of state

Jacobson, *"Thermodynamics of Spacetime: The Einstein Equation of State"* (Phys. Rev. Lett. **75**,
1260, 1995), showed the Einstein equations are **not** a fundamental dynamical law but the
**equation of state** of horizon thermodynamics. They follow from demanding the Clausius relation

$$
\delta Q \;=\; T\, \delta S
$$

at **every local Rindler horizon** — a separate causal horizon through each spacetime point, as seen
by each local accelerated observer — with `T` the **Unruh temperature** of that observer and `S` the
**Bekenstein–Hawking area entropy** of the horizon. Heat flux across the horizon, equated to the
temperature times the entropy change (the area change via Raychaudhuri focusing), yields the Einstein
tensor. The derivation is **entirely local**: there is no global construction anywhere in it.

This is *exactly* QLF's picture — synthesized spacetime, local clocks, horizon screening — and QLF
supplies **both** of Jacobson's inputs from its own substrate.

---

## §3 QLF supplies both inputs

| Jacobson input | QLF substrate result | Anchor |
|---|---|---|
| Horizon **area entropy** `S = 4πR² log 2` ⟹ entropy density `η = 1/(4G)` | holographic delay area law | [`holographic_entropy_eq`](lean/QLF_GravityFromDelay.lean), [`Gravity_From_Delay.md`](Gravity_From_Delay.md) |
| Horizon **temperature** `T = ℏκ/(2πck_B)` (Unruh) | the loop-phase `2π` master relation | [`unruh_temperature`](lean/QLF_HorizonTemperature.lean) |

The substrate area law carries one `log 2` bit per cell; its continuum coarse-graining is the
Bekenstein–Hawking entropy density `η = 1/(4G)` (the `log 2 / 4` gap is the substrate→continuum
factor noted in [`Gravity_From_Delay.md`](Gravity_From_Delay.md)). The Unruh `2π` is QLF's **loop
phase** — the same `2π` as `g−2 = α/2π` and the horizon temperatures
([`QLF_HorizonTemperature`](lean/QLF_HorizonTemperature.lean)).

---

## §4 The coefficient is fixed

With both inputs fixed, the Clausius relation fixes the field-equation coefficient at the **Unruh
`2π` over the entropy density**:

$$
8\pi G \;=\; \frac{2\pi}{\eta}, \qquad \eta = \frac{1}{4G}.
$$

Machine-verified as
[`einstein_coupling_from_thermodynamics`](lean/QLF_EinsteinEquations.lean):

```lean
theorem einstein_coupling_from_thermodynamics (G : ℝ) (hG : G ≠ 0) :
    einstein_coupling G = 2 * Real.pi / entropy_density G
```

with `einstein_coupling G = 8πG` and `entropy_density G = 1/(4G)`. And the same `8π` is QLF's
geometric `8π = 4π·2` — boundary solid angle × Hermitian-pair degeneracy
([`einstein_coupling_geometric`](lean/QLF_EinsteinEquations.lean),
[`QLF_EinsteinGeometricFactor`](lean/QLF_EinsteinGeometricFactor.lean)):

$$
8\pi G \;=\; (4\pi \cdot 2)\, G \;=\; 2\pi \cdot (4G).
$$

The `2π` is the local horizon's accelerated-observer periodicity; the `4G` is the inverse entropy
density. The Einstein coupling is the **ratio of these two local-horizon quantities**.

---

## §5 The integration constant is the local-clock tick

Jacobson's derivation leaves an undetermined integration constant — the cosmological constant `Λ`.
QLF fixes it independently as `Ω_Λ = log 2` ([`QLF_CosmologicalConstant`](lean/QLF_CosmologicalConstant.lean),
[`Cosmological_Constant.md`](Cosmological_Constant.md)), which is *the same* `log 2` as the per-tick
quantum of every local clock ([`local_clock_tick_is_log_two`](lean/QLF_LocalClock.lean)) and the
per-event free-energy quantum ([`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean)). So

> **the cosmological constant is the local clock's own tick** — the irreducible `log 2` each ZFA
> closure advances, read at cosmic scale.

The "unexplained" constant of Jacobson's derivation is, on the substrate, just the rate the local
clocks tick.

---

## §6 The Kitada local-time reading

Jacobson's derivation is **local** — `δQ = T δS` at *each* local Rindler horizon. QLF already proved
([`markov_blanket_local_clock`](lean/QLF_LocalClock.lean), [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md))
that a Markov blanket **is** a Kitada local clock, and it is also a horizon — carrying the Unruh
temperature and the area entropy. So the three are the **same object**:

> Jacobson's local Rindler horizon **=** QLF's Markov-blanket horizon **=** Kitada's local clock.

Hence the Einstein equation of state is the Clausius relation evaluated **at each Kitada local clock**,
and the global field equations are the statement that every local clock in the network sits in local
thermodynamic equilibrium simultaneously — precisely Hitoshi Kitada's picture of GR as the consistency
condition of the network of local times ([gr-qc/9612043](https://arxiv.org/abs/gr-qc/9612043)). The
local-time reading is developed in [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.2.

---

## §6a The curvature side: from the causal order (Sorkin / Benincasa–Dowker)

Jacobson's route fixes the **coefficient** (`8πG = 2π/η`) and the constant (`Λ = log 2`). QLF supplies
the *other* half of the field equations — the **curvature** side, `G_μν = R_μν − ½ g_μν R` — from the
**same substrate** by a second, independent route: the causal-set order → metric program.

**The substrate is a causal set.** [`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean) makes QLF's
reachability order a Lean object — a partial order of events with no metric: exactly a **causal set**
(Bombelli–Sorkin). And Causal Set Theory's central result is that **geometry is recovered from order +
number**: the **Benincasa–Dowker** discrete d'Alembertian applied to the causal order returns the
**Ricci scalar** `R`, and the causal-set action limits to the **Einstein–Hilbert action** `∫R` in the
continuum. So the curvature side of the Einstein equations is the concrete **order → metric** program
running *on QLF's own closure graph*.

**The first rung is Lean-anchored.** The basic object is the **causal (Alexandrov) interval**
`[A,B] = {C : A ≤ C ≤ B}`, and CST's foundational principle is **number ↔ volume**: counting events
measures spacetime volume / proper time. On QLF's causal set this is
[`QLF_CausalInterval`](lean/QLF_CausalInterval.lean): `intervalVolume A B = |B| − |A| + 1` — the
Markov-blanket **depth difference**, which is exactly the **Kitada local-clock tick count** between the
two events (`Kitada_Local_Time_GR.md`). The geometric content anchored is that **proper time is
additive along a causal chain** (`intervalVolume_additive`) — the discrete seed of the line element
from which `R` and `∫R` are built. (The Minkowski metric itself re-emerges from the *statistics* of
causal links in the dense limit — [`TheContinuum.md`](TheContinuum.md) — the Lorentz-invariant CST
mechanism.)

So the Einstein field equations sit on **two substrate legs that meet**: the **coefficient +
thermodynamics** (Jacobson, §§2–5: `8πG = 2π/η`, `Λ = log 2`) and the **curvature from causal order**
(Sorkin / Benincasa–Dowker, here: `∫R` as the continuum limit of the closure-graph action). Both are
the *same* local object — the Markov-blanket / Kitada clock, which is at once the thermodynamic horizon
*and* a node of the causal set. The field equations are the statement that this one network is
simultaneously in local thermodynamic equilibrium (the coefficient) and rendered from its own causal
order (the curvature).

**Why Hilbert's action is *stationary*.** Benincasa–Dowker supplies *which* functional (`∫R`).
[`Stationary_Action.md`](Stationary_Action.md) supplies *why a functional is stationary at all*: the
realized history is the census mode, and ZFA's conjugate pairing puts that mode at balance with zero
first variation (`QLF_StationaryAction`, no axioms). Identifying the BD count with that multiplicity is
the open step between the two.

**Where the curvature actually lives — the next rung points itself.** Pushing the Lean one step
further sharpens the target: every causal interval *along a single history* is a **chain** — totally
ordered (`interval_isChain`, `causalInterval_eq`: the interval is exactly the prefixes of `B` no
shorter than `A`). A chain is **flat** — one history line carries proper time but no curvature. So the
Ricci scalar cannot come from a single history; it must come from the **branching** of the full closure
graph — *incomparable* histories, antichains, the places where `expand_generation` forks into
distinguishable futures.

That is exactly where the **Benincasa–Dowker** discrete d'Alembertian reads curvature. Its input is the
sequence of **causal layers** `L_k(x) = {y ≤ x : volume[y,x] = k}` ([`layer`](lean/QLF_CausalInterval.lean));
the operator is an alternating sum of their cardinalities `|L_k|` weighted by a balanced stencil
([`bdCoeff`](lean/QLF_CausalInterval.lean): `+1, −2, +1`, with [`bdCoeff_sum_zero`](lean/QLF_CausalInterval.lean)
proving the weights sum to zero — the property that makes it read the *second difference* of the layer
occupations, i.e. curvature, not a bare count), and applied to a constant it returns `−½ R` in the
continuum.

**The operator is Lean-anchored at its flat baseline.** On QLF's single-history substrate the layers are
**singletons** — `layer_unique` proves exactly one event sits at each interval-depth below `x`, so
[`layerCard_chain`](lean/QLF_CausalInterval.lean) gives every in-range layer cardinality `= 1`, and the
BD reading [`bdCurvature`](lean/QLF_CausalInterval.lean) on a history of depth `≥ 2` collapses to the
bare weight sum `+1 − 2 + 1 = 0` ([`bdCurvature_chain_zero`](lean/QLF_CausalInterval.lean)): `R = 0` in
the actual operator, the chain's BD reading being the 1-D discrete second difference annihilating a
constant. So both **the spatial dimensions and the curvature are the same thing**: they are the *growth
of* `|L_k|` once the closure graph branches. This dovetails with the graph-rendering result that space
is 3D ([`SpaceTime.md`](SpaceTime.md) §3a) — the branching that renders into three spatial dimensions is
the same branching whose layer-growth the BD operator turns into `R`.

That layer-growth is anchored in the one case that is exactly a product of chains:
[`QLF_CausalDimension`](lean/QLF_CausalDimension.lean) builds the **2-D causal diamond as the product
order of two chains** — precisely `1+1` Minkowski in light-cone coordinates `(u,v)`, the two null
directions being two QLF histories. Its volume is the **product** of the two chain volumes
(`diamond_eq_product`: `(m+1)(n+1)`), and — the dimension fingerprint — that volume is **many-to-one**
(`diamondVolume_collision`: `1×1`, `0×3`, `3×0` all have volume `4`), whereas the 1-D chain volume is
**injective** (`chainVolume_injective`: one interval per volume, singleton layers). *Multiplicity of
intervals at a fixed volume is the layer growth*, so combining histories literally raises the
Myrheim–Meyer dimension.

**The layer growth is computed directly** ([`prodLayerCard`](lean/QLF_CausalDimension.lean)). On the
actual 2-D product order the Benincasa–Dowker layer cardinality grows past the single-history
singletons: the volume-2 (link) layer below the apex has cardinality `1` for one history
([`prodLayerCard_chain_link`](lean/QLF_CausalDimension.lean)) and `2` once two histories combine
([`prodLayerCard_diamond_link`](lean/QLF_CausalDimension.lean)) — the apex `(1,1)`'s two immediate
predecessors `(0,1)`, `(1,0)`, the two null directions — a size-independent dimension fingerprint
([`prodLayerCard_link_stable`](lean/QLF_CausalDimension.lean)), packaged as
[`layer_growth_from_branching`](lean/QLF_CausalDimension.lean). So `|L_k|` growth past the
`bdCurvature_chain_zero` flat baseline is a verified fact, not just a gesture.

The **continuum limit** is the **statistical sprinkling average** over the substrate's branchings: the
Ricci scalar is this layer-growth read in the mean of a Poisson sprinkling (where flat space reads
`R = 0` in the mean and curvature is the residual), not the finite count of any one small diamond. This
is anchored in [`QLF_CausalContinuum`](lean/QLF_CausalContinuum.lean) in QLF's Millennium pattern — a
verified discrete core plus one named continuum bridge. The **statistical kernel is proven**: under a
Poisson sprinkling of (intensity × volume) `lam` the expected Benincasa–Dowker layer occupation is the
Poisson value `e^{−lam} lam^k / k!` ([`poissonOccupation`](lean/QLF_CausalContinuum.lean)), and the
verified discrete `|L_k|` counts pass to those expectations through the Poisson layer recurrence
([`poissonOccupation_succ`](lean/QLF_CausalContinuum.lean): `⟨N_{k+1}⟩(k+1) = ⟨N_k⟩ lam`). The full
`ρ → ∞` Benincasa–Dowker convergence of the mean to `−½R` is the explicit **bridge axiom**
[`benincasa_dowker_limit`](lean/QLF_CausalContinuum.lean) — the settled Poisson-process + curved-
interval-volume machinery of CST, the `RCA₀ → Lorentzian-analytic` boundary parallel to
`yang_mills_continuum_gap` ([`QLF_MassGap`](lean/QLF_MassGap.lean)) and `continuum_vorticity_planck_capped`
([`QLF_NavierStokes`](lean/QLF_NavierStokes.lean)). From it, **flat space reads `R = 0` in the mean**
([`flat_curvature_zero_in_mean`](lean/QLF_CausalContinuum.lean)) — the statistical survival of the
discrete flat baseline. So the curvature side now stands on the same footing as Riemann / Yang–Mills /
Navier–Stokes: a machine-verified discrete core (the flat reading, the branching layer-growth, the
Poisson kernel) and one explicit continuum bridge. The remaining substrate computation is assembling
the full tensor `G_μν = 8πG T_μν` from the Benincasa–Dowker action and general `d ≥ 3`.

---

## §6b The algebraic rung: nine integer null probes, no continuum of directions

Jacobson's derivation does not need the Benincasa–Dowker operator to manufacture all ten components of
`G_μν`. It reaches a **pointwise null projection** — writing `S_ab := R_ab − κ T_ab`, the Clausius
relation on every local Rindler horizon gives

```
S_ab k^a k^b = 0     for null k
```

— and then an **algebraic** step concludes `S_ab = f g_ab`, after which contracted Bianchi plus
`∇^a T_ab = 0` fixes `f = −R/2 + Λ`. Three arrows:

```
horizon thermodynamics  →  S_ab k^a k^b = 0  →  S_ab = f g_ab  →  f = −R/2 + Λ
                        (Rindler/Raychaudhuri)   (algebraic)      (contracted Bianchi)
```

The **middle arrow is closed** in [`QLF_NullTensorReconstruction`](lean/QLF_NullTensorReconstruction.lean),
and closed *finitely*. The textbook version quantifies over the continuum of null directions; the
substrate needs **nine**, all of them integer points of the discrete Hermitian lattice whose interval is
integer-valued ([`QLF_Minkowski`](lean/QLF_Minkowski.lean), `det X ∈ ℤ`):

```
(1,±1,0,0)   (1,0,±1,0)   (1,0,0,±1)   (5,3,4,0)   (5,3,0,4)   (5,0,3,4)
```

null because `1² = 1²` and `5² = 3² + 4²` — nameable without a square root, hence without a completed
continuum. A generic null direction `(1, cos θ, sin θ, 0)` is *not* a substrate point; these nine are.
The mechanism ([`finite_null_probes_force_metric`](lean/QLF_NullTensorReconstruction.lean)): the six
axis probes give `S.tt ± 2 S.tx + S.xx = 0`, whose difference kills `S.tx` and whose sum pins
`S.xx = −S.tt` (likewise `y`, `z`); each Pythagorean probe then reads
`25 S.tt + 9 S.xx + 16 S.yy + 24 S.xy = 0`, and `25 − 9 − 16 = 0` collapses it to `24 S.xy = 0`.

With the converse direction ([`contract_metricMultiple`](lean/QLF_NullTensorReconstruction.lean): a
metric multiple contracts to `f · interval`, so it annihilates the *whole* cone) this is a
**characterization** — [`null_annihilator_iff_metric_multiple`](lean/QLF_NullTensorReconstruction.lean):
the symmetric tensors vanishing on the null cone are **exactly** the multiples of `g`, a
one-dimensional space, and nine lattice points decide membership. The nine are sharp: the six axis
probes alone admit the pure-`xy` counterexample
([`axis_probes_insufficient`](lean/QLF_NullTensorReconstruction.lean)), so the `3-4-5` triple — the
smallest integer Pythagorean reach into the spatial off-diagonals — is load-bearing.

This is the same *unneeded* strike as the census recovering `π` and `ζ(3)`
([TheContinuum.md](TheContinuum.md) §2): a continuum quantifier in a standard derivation turns out to
be replaceable by finitely many realizable points. It is **only** the algebraic rung — `SymTensor4` is
ten reals, and nothing in that module ties them to a curvature tensor. The first arrow (local Rindler +
Raychaudhuri focusing) and the third (contracted Bianchi) are unchanged in cost, and they are where the
field-equation work now sits.

---

## §6c The third arrow: contracted Bianchi, with zero new axioms

The remaining algebra of Jacobson's derivation is the step *out* of the metric form. Given
`R_ab = κ T_ab + f g_ab`, take the divergence of both sides: conservation `∇^a T_ab = 0` kills the
matter term, metric compatibility gives `∇^a (f g_ab) = ∂_b f`, and the **contracted Bianchi identity**
`∇^a R_ab = ½ ∂_b R` handles the left. So

```
∂_b (f − R/2) = 0   ⟹   f = R/2 − Λ   for a CONSTANT Λ
```

and substituting back yields `R_ab − ½ R g_ab + Λ g_ab = κ T_ab`, i.e.

```
G_ab + Λ g_ab = κ T_ab
```

machine-checked as [`einstein_field_equations`](lean/QLF_BianchiClosure.lean). `Λ` is Jacobson's
integration constant — the one QLF fixes independently as `Ω_Λ = log 2` (§5), and `κ = 8πG` is §4's
coefficient. [`metric_form_from_null_probes`](lean/QLF_BianchiClosure.lean) chains §6b directly into
it, so **arrows two and three compose with nothing left between them**.

**How the differential-geometry boundary is handled — and why it is not an axiom.** QLF's Lean core
carries no connections, so `∇^a` and `∂_b` cannot be *defined* here. Rather than posit them, the
calculus is packaged as a **structure**,
[`DivergenceCalculus`](lean/QLF_BianchiClosure.lean), whose fields are the laws it must satisfy
(divergence additivity and homogeneity, metric compatibility, gradient linearity, and "vanishing
gradient ⟹ constant", i.e. connectedness). Every theorem takes an instance as a hypothesis. So the
module adds **nothing to the axiom inventory** — the boundary is visible in each signature instead,
and a future construction (Mathlib connections, or a substrate difference calculus) discharges it by
*building* an instance rather than by deleting an axiom. The two physics inputs, contracted Bianchi and
conservation, are likewise explicit hypotheses of the main theorem.

**What this leaves.** One arrow: `δQ = T δS ⟹ (R_ab − κ T_ab) k^a k^b = 0`, needing the local Rindler
construction and Raychaudhuri focusing. That is now the *single* remaining substrate question for the
field equations, rather than "the tensor derivation" as a whole.

---

## §7 Honest scope

This anchors the **coefficient and the thermodynamic skeleton** — `8πG = 2π/η`, both inputs being QLF
substrate results, reproducing Jacobson's "Einstein equation of state," with `Λ = Ω_Λ = log 2` the
integration constant = the local-clock tick. Status marker:
[`einstein_equations_in_progress`](lean/QLF_EinsteinEquations.lean).

It does **not** carry out the full **tensor** derivation — but that derivation now splits into three
named arrows (§6b), of which the **algebraic middle one is closed with no axiom**: a symmetric tensor
annihilating the null cone is a metric multiple, forced by **nine integer lattice probes** rather than a
continuum of null directions ([`QLF_NullTensorReconstruction`](lean/QLF_NullTensorReconstruction.lean)).
The arrow *out* of it is closed too (§6c): contracted Bianchi plus conservation force `f = R/2 − Λ`
with `Λ` constant, giving `G_ab + Λ g_ab = κ T_ab` — and with **zero new axioms**, the calculus being an
interface (`DivergenceCalculus`) discharged by construction rather than posited. What is left is the
arrow *into* the metric form: local Rindler + Raychaudhuri focusing.

The remaining open step is *concrete and named*, not "differential geometry QLF lacks": it is the
**causal-set order → metric** program
(Sorkin / Benincasa–Dowker, §6a) running on QLF's own causal set
([`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean)), of which the **number↔volume / proper-time
rung is Lean-anchored** ([`QLF_CausalInterval`](lean/QLF_CausalInterval.lean)). What remains open
(`einstein_curvature_in_progress`): the interval *cardinality* = volume, the discrete
**d'Alembertian → Ricci scalar** (Benincasa–Dowker), and the **continuum limit** to
`G_μν = 8πG T_μν` — the same dynamical-metric step still open for the Schwarzschild metric
([`GR_Schwarzschild.md`](GR_Schwarzschild.md)) and gravitational waves
([`QLF_GravitationalWaves`](lean/QLF_GravitationalWaves.lean) — whose *linearized* wave equation
`□_d δρ = 0` is already anchored via the density-perturbation route; the dynamical-metric derivation of
the operator is this same causal-set step), a definite causal-set computation rather than a missing
toolbox. What is established: the **identification** (Jacobson's local horizon =
QLF's Markov-blanket / Kitada local clock = a node of the causal set), so the Einstein equations sit on
two meeting substrate legs — the equation of state (coefficient) and the causal order (curvature).

---

## §8 Lean anchors

| Theorem | Statement |
|---|---|
| `entropy_density` | `η = 1/(4G)` — Bekenstein–Hawking entropy density (continuum coarse-graining of `S = 4πR² log 2`) |
| `einstein_coupling` | `8πG` — the Einstein gravitational coupling |
| `einstein_coupling_from_thermodynamics` | `8πG = 2π/η` — the coefficient as Unruh `2π` over entropy density (Jacobson) |
| `einstein_coupling_geometric` | `8πG = (4π·2)G = 2π·(4G)` — the same `8π = 4π·2` |
| `einstein_equations_in_progress` | status: coefficient + thermodynamic skeleton anchored; full tensor derivation open |
| `finite_null_probes_force_metric` | nine **integer** null probes force `S_ab = S.tt·diag(1,−1,−1,−1)` — Jacobson eqs. (5)→(6) without a continuum of null directions (§6b) |
| `null_annihilator_iff_metric_multiple` | the null-cone annihilators are **exactly** the metric multiples (one-dimensional, spanned by `g`); nine lattice points decide membership |
| `contract_metricMultiple` | `contract (f·g) v = f · interval v` — a metric multiple annihilates the whole null cone |
| `axis_probes_insufficient` | sharpness: the six axis probes alone fail (pure-`xy` witness), so the `3-4-5` probes are load-bearing |
| `DivergenceCalculus` | the `∇^a`/`∂_b` interface — the differential-geometry boundary as a **structure**, so no axiom is added (§6c) |
| `scalar_multiple_is_curvature` | contracted Bianchi + conservation ⟹ `f = R/2 − Λ` with `Λ` **constant** (the integration step) |
| `einstein_field_equations` | `G_ab + Λ g_ab = κ T_ab` — the field equations over the interface (§6c) |
| `metric_form_from_null_probes` | chains §6b into §6c: nine integer null probes deliver the metric form `einstein_field_equations` needs |

---

## §9 References

- T. Jacobson, *Thermodynamics of Spacetime: The Einstein Equation of State*, Phys. Rev. Lett. **75**, 1260 (1995), [gr-qc/9504004](https://arxiv.org/abs/gr-qc/9504004).
- E. Verlinde, *On the Origin of Gravity and the Laws of Newton*, JHEP **04**, 029 (2011), [arXiv:1001.0785](https://arxiv.org/abs/1001.0785).
- H. Kitada, *Theory of Local Times*, [gr-qc/9612043](https://arxiv.org/abs/gr-qc/9612043) (1996).
- J. D. Bekenstein, *Black Holes and Entropy*, Phys. Rev. D **7**, 2333 (1973).
- W. G. Unruh, *Notes on black-hole evaporation*, Phys. Rev. D **14**, 870 (1976).
