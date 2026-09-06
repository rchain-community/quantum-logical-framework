# α — Why 1/137 in QLF (leading value derived; exact 1/137.036 in progress)

> **This is a result of the [Quantum Logical Framework (QLF)](README.md)** — read it in that context.
> QLF derives physics from one substrate (the 8-twist phase-string alphabet, ZFA closure, synthesized
> spacetime), machine-verified in Lean 4 across a [tree of more than a hundred modules](lean/README.md). α is not a
> standalone numerology here; it is a **consequence of QLF's derived 3-D rendering** of the closure
> graph. And that 3-D is **the human/cosmic perspective**: the only dimension in which a relational
> world renders faithfully and comprehensibly, supports stable atoms and chemistry (hence observers),
> and supports stable cosmic structure (Newton's `1/r²`, bound orbits). So the leading `1/137` is *our*
> α's leading value — the coupling of the world **as we, and the cosmos we observe, are rendered** — and the framework derives 3
> rather than assuming it ([`SpaceTime.md`](SpaceTime.md) §3a; the over-determination is §6 below).

> **Status — `alpha_exact_value_in_progress` (leading value + bounds + `w=½` prediction done; the
> continuum tail is the SM's frontier).** QLF derives **why the leading combinatorial value is `1/137`**:
> the bare `2⁻⁷ = 1/128` coupling and the `+d² = 9` directional screening, both fixed by the 8-twist
> substrate and 3-D rendering. The residual to the measured `1/137.035999` (`q²→0` Thomson) is now
> **bounded two-sided and machine-checked** (`137.01587 < α⁻¹ < 137.04813`), and the equal-weight
> prediction **`137.032` is structural** — `w = 1/2` is forced by the free-monoid/bifibration, not
> fitted. The proven bracket + `G = 1/(1−I)` establish that `0.036` **is** in the census's reach (total
> resummation overshoots, one prime term undershoots) — *existence* of the value, not a fit. What is
> open is the **multiplicity** — *which* partial resummation, i.e. how many 1PI insertions contribute
> as `q²→0` — and that count *is* the continuum vacuum-polarisation running, the Standard Model's own
> un-derived frontier. Every substrate mechanism swing is closed (§*Bounds*, [`Alpha_Residual.md`](Alpha_Residual.md) §9c).
> So: **`1/137` = derived leading value; `137.032` = the structural `w=½` prediction; `1/137.036` = the
> exact value, its last `~0.004` the continuum running.** In digits: QLF suggests **~5 significant
> figures** of `α⁻¹` (`137.03`) — of the residual `+0.036`, only its leading `0.03`; the `~0.004` beyond
> is not suggested as a number, and the census provably reaches only to 4-loop QED
> ([`Alpha_Residual.md`](Alpha_Residual.md) §9d–§9g).

**The canonical QLF document for the fine-structure constant `α ≈ 1/137`.** It collects, in one place,
everything QLF says about α and links every related proof:

1. [What α is](#1-what-α-is) · 2. [The first-principles derivation](#2-the-first-principles-derivation)
· 3. [Which scale — the 3-D-rendered IR anchor](#3-which-scale--the-3-d-rendered-ir-anchor) ·
[Bounds on α](#bounds-on-α-machine-checked) ·
4. [The running](#4-the-running--why-α-was-higher-in-the-early-universe) ·
5. [No cosmological-time drift](#5-no-cosmological-time-drift-of-α0) ·
6. [4-D / 5-D and the over-determination of 3-D](#6-4-d--5-d-and-the-over-determination-of-3-d) ·
7. [Parallel derivation pathways](#7-parallel-derivation-pathways) ·
8. [α and the other substrate constants](#8-α-and-the-other-substrate-constants--the-shared-62-split) ·
9. [Forces from α](#9-forces-from-α) · 10. [Where α is used](#10-where-α-is-used--downstream-derivations) ·
11. [The constants mapper](#11-the-constants-mapper) · 12. [Lean-theorem index](#12-lean-theorem-index) ·
13. [Honest scope](#13-honest-scope).

---

## 1. What α is

α is the dimensionless strength of the electromagnetic interaction. Its measured low-energy value is

```
α(0) = 1/137.035999…   (CODATA, the q²→0 / Thomson limit)
```

In the **Standard Model α is a free input** — measured and plugged in; the SM cannot even *formulate*
"why is α ≈ 1/137" ([`Beyond_Standard_Model.md`](Beyond_Standard_Model.md)). **QLF derives the leading
value**: `α_lead = 1/(128 + 9) = 1/137` (exact rational) from the 8-twist substrate alphabet and the
3-dimensionality of synthesized space, with **no observable input** — `0.026%` from CODATA's
`1/137.035999`. The leading value is Lean-verified (`alpha_QLF_eq`, `only_3d_substrate_gives_137`,
[`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean)); the residual `0.036` to
the exact Thomson value is the in-progress census tail (status box above).

---

## 2. The first-principles derivation

A two-stage combinatorial reduction. Full prose: [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md)
§6.1; runnable demo `magnetism_spatial_dynamics_demo.py`.

### Stage 1 — bare combinatorial coupling

Per Planck tick, four independent substrate selectivities multiply:

| Factor | Value | Substrate source |
|---|---|---|
| Naive closure rate | `1/16` | 4 base half-spin closures `{^v, <>, /\, +-}`, prob `1/8` per twist-pair, from the 8-twist alphabet |
| Gauge selectivity | `1/4` | only `+-` (1 of the 4) is the gauge fold that mediates Coulomb binding |
| Phase coherence | `1/2` | binary in-phase / out-of-phase selectivity |
| Spatial co-location | `1` | binding-photon `λ/2 ≈ 45 nm ≫` Bohr radius `a₀ ≈ 0.053 nm` |

```
α_bare = 1/16 × 1/4 × 1/2 × 1 = 1/128 = 2⁻⁷     (alpha_bare_eq)
```

### Stage 2 — the leading screening (bare → leading value)

Energy conservation is **emergent**, not an axiom; its **leading** effect is a screening resummation
`α = α_bare / (1 + N·α_bare)`, with **`N = 9`** the components of the `3 × 3` directional-coupling tensor
(`N_directional_modes_eq_nine`). This is a Dyson sum of a *constant* directional insertion — **not** the
momentum-dependent QED vacuum-polarization loop; that difference is exactly the in-progress residual:

```
α = (1/128) / (1 + 9/128) = 1/137.000     (alpha_QLF_eq)   vs  1/137.036  (0.026%)
```

The `(1+9α)` factor is the **leading** screening step — bare `2⁻⁷=1/128` → leading `1/137`. The
higher-order census closures that would carry it the final `0.036` to the exact Thomson value are the
in-progress tail (§3, status box).

### The closed form and the dimension counterfactuals

The whole chain collapses to a single rational function of the rendering dimension `d`:

```
α(d) = α_bare / (1 + d²·α_bare) = 1 / (128 + d²)     (alpha_at_dim_closed_form)
```

| Substrate dimension | `N = d²` | `α = 1/(128 + d²)` | Theorem |
|---|---|---|---|
| 2-D | `4` | `1/132` (off ~4%) | `alpha_QLF_2d_counterfactual` |
| **3-D** | **`9`** | **`1/137` (0.026%)** | **`alpha_QLF_eq`** |
| 4-D | `16` | `1/144` (off ~5%) | `alpha_QLF_4d_counterfactual` |
| 5-D | `25` | `1/153` (off ~12%) | `alpha_at_dim_five` |

`N = 9 = 3²` is a 3-D object; **α = N = 3² is a *consequence* of the 3-D rendering**
([`SpaceTime.md`](SpaceTime.md) §3a; the `6+2` split, [`Magic_numbers.md`](Magic_numbers.md)). α is a
function of `d` **alone** — the key fact for §5.

**Runnable illustration ([`Genesis.md`](Genesis.md); run [`genesis.py`](genesis.py)).** The census sector is exercised end-to-end: the
`128 + d²` family is tabulated with `d = 3 → 137` the **only prime** in the small range, and — an
independent census-side fingerprint of the same `d` — the closure-census *spectral exponent* is measured
at `−p/2`, so `p = 3` conjugate (spatial) pairs give slope `−3/2` (the `8`-twist/`4`-pair sector gives
`−2`). This is exact combinatorics (`C(2m,m)·c_pair(p,m)` is the closed-walk count on `ℤ^p`), not a fit:

```
 p (pairs)   fitted slope    expected -p/2
         1        -0.4919          -0.5000
         2        -0.9839          -1.0000
         3        -1.4762          -1.5000     <- 3 spatial pairs
         4        -1.9694          -2.0000     <- 8-twist / 4-pair
```

The full annotated run (census, spectral exponent, octave hierarchy, swap-graph, `128 + d²`) is [`Genesis.md`](Genesis.md).

---

## 3. Which scale — the 3-D-rendered IR anchor

The relevant *scale* is the **IR, zero-momentum-transfer (`q²→0`), Thomson limit** — the macroscopic,
fully-screened, large-distance charge, which CODATA quotes as `1/137.035999`. `1/137` is the **leading**
substrate coupling *at* that scale: (1) `N = 9 = 3²` exists only once space renders to dimension 3 (the
macroscopic limit); (2) the `(1+9α)` resummation is the leading screening of the bare `1/128` toward the
large-distance charge. So the *scale* is privileged and physically defined; `1/137` is the derived
**leading** value there, and the residual `0.036` to the exact Thomson value is the in-progress census
tail (status box). `1/137` is the leading value at the IR scale — **not** the exact IR value, which is
`1/137.036`.

### Why 3-D — the human/cosmic perspective

In QLF spacetime is **synthesized**, and an observer's world is the *rendering* of the closure graph at
the observer's scale ([`SpaceTime.md`](SpaceTime.md) §3a: 3 is the *minimal* dimension in which any
relational structure renders faithfully *and comprehensibly*). The fully-rendered 3-D limit is exactly
the **human and cosmic perspective** — the scale at which atoms hold, chemistry and observers exist
(§6), and structure is stable under Newton's `1/r²`. So `α = 1/137` is **our** α: the coupling of the
world *as rendered for observers like us, and for the cosmos we look out on*. The value is not
anthropically *selected* from a landscape — QLF *derives* `3` — but it is anthropically *located*.

---

## Bounds on α (machine-checked)

`α = 1/137` is the **derived leading value** (§2): substrate structure fixes it parameter-free,
`α⁻¹ = 1/α_bare + d² = 2⁷ + 3² = 128 + 9 = 137`. The measured `α⁻¹ = 137.035999` differs by the
higher-order residual `+0.036` (status box) — and that residual is now **bounded**, machine-checked in
[`lean/QLF_AlphaBound.lean`](lean/QLF_AlphaBound.lean):

| Claim | Statement | Assumptions | Theorem |
|---|---|---|---|
| Leading value | `α⁻¹ = 128 + 9 = 137` | substrate structure, parameter-free | `leadInv_eq` / `alpha_QLF_eq` |
| Residual sign | `α⁻¹ > 137` | EM abelian ⟹ screening | `alpha_inv_gt_137` |
| Census cap (upper) | `α⁻¹ < (217 + 512√62)/31 ≈ 137.04813` | every closure once (`α_bare`/order); GF a **theorem** (`central_binom_genfun`, `censusTail_eq` — no axiom) | `alphaInvCap_eq`, `codata_below_alphaInvCap` |
| Irreducible cap (lower) | `α⁻¹ > 263 − 16√62 ≈ 137.01587` | prime closures only (`2·Catalan(n−1)`/order) | `irreducibleCap_eq` |
| Dyson/1PI resummation | `G(x) = 1/(1 − I(x))` — total census = geometric resummation of primes | — | `census_irreducible_resummation` |

So the substrate pins α to a **two-sided window, both ends machine-checked** —
**`137.01587 < α⁻¹ < 137.04813`**, i.e. **`0.0072967 < α < 0.0072992`** (~0.024% wide). The measured
`α⁻¹ = 137.035999` (`α = 0.00729735`) lies **strictly inside**: `0.020` above the irreducible cap,
`0.012` below the census cap. The **pure-ZFA prediction** is the equal-weight resummation `w = 1/2`
between the two caps — `α⁻¹ = 137 + ½(irreducibleTail + censusTail) = 137.032` — and `w = 1/2` is now a
**structural** value, not a fit: unique prime factorisation (`census_irreducible_resummation`) makes the
closures a free monoid, whose geometric generating function gives a *linear* coefficient recurrence,
which has no period-doubling — so the discrete-scale-invariance line that would move `w` off `½` is
**closed by structure** ([`Alpha_Residual.md`](Alpha_Residual.md) §9b, [`Category_Theory_QLF.md`](Category_Theory_QLF.md) §3a).

The genuinely *construction-independent* prediction is the residual's **sign**: EM is abelian
(`em_gauge_abelian`, U(1), no self-interaction), so higher closures only *screen* (add positively) and the
dressed coupling is weaker than the leading value — `α⁻¹ > 137`. It is falsifiable both ways: a measured
`α⁻¹ ≤ 137` refutes the screening picture, and a steeper counting rule caps the residual *below* the
measured value (`steep_map_excludes_codata`), so the data *selects* the shallow one-power-per-order map.

**Settled vs open.** The leading value `137` is derived, the two-sided band is proved, the
generating-function input is a **theorem** (`central_binom_genfun`/`censusTail_eq`, from Mathlib's
`(1+x)^a` binomial series — `QLF_AlphaBound` carries no axiom), and the equal-weight prediction
`137.032` is now structural. The one open piece is the residual *within* the window — the exact
`137.036`, which by the Dyson identity is a **specific partial resummation** of the prime-closure series
(§4a; [`Alpha_Residual.md`](Alpha_Residual.md) §4).

**Existence is proven; the multiplicity is the open number — and that is where CODATA legitimately
enters.** QLF normally refuses CODATA as a target (fitting a substrate number to the answer is
numerology). Here the discipline is respected by an asymmetry the working method makes explicit
([`Philosophy.md`](Philosophy.md) §3a rule 1: *an existence result is a lower bound on multiplicity*).
The proven bracket plus `G = 1/(1−I)` establish that `0.036` **is** in the census's reach — the total
resummation overshoots it (`+0.0481`), one prime term undershoots it (`+0.0159`), so *some* partial
resummation of the primes gives exactly `0.036`. **We have shown one way it manifests, so we know it
*can* happen** — existence, not a fit. What we do not know is *how many* ways — which partial
resummation, i.e. how many 1PI insertions contribute as `q² → 0` — and that count *is* the continuum
vacuum-polarisation running (§4a). CODATA's `137.035999(1)` is then an **estimate of that count**
(`δw ≈ 0.124`, a quarter of the interval), read off after the fact — an observation of where physical
reality's multiplicity landed inside a proven space, not a knob turned to reach it.

The residual is dissected in [`Alpha_Residual.md`](Alpha_Residual.md). **Where it stands:** `α⁻¹ = 128 +
9 = 137` is the *exact leading pure-EM* value — **confirmed by the running**: `128 = 2⁷ ≈ α̂⁻¹(M_Z)` (the
coupling at the weak scale, to `0.05`) and `+9 = 3²` = the EM running `M_Z → IR` (gap `9.086`). The
weak-sector hypothesis for `+0.036` (per Jim) was *tested* (the W-loop running) and **closed** — the `W`
is integrated out below `M_W` so it cannot run down to the IR, and on-shell `α(0)` has no separate `W`
piece (`Π(0)=0`). The residual sits at the higher-order-EM scale (`~5α`; `(α/π)·9 ≈ 0.021`), so `+0.036`
is the **higher-order EM running** correction to `+9` — the same object as the closure-resummation tail,
in running language. The forced bracket (`263 − 16√62 ≈ 137.0159` below, `(217+512√62)/31 ≈ 137.0481`
above; both machine-verified) is the combinatorial form of this sub-leading EM running. The **gauge-projection derivation was tested and fails**: the *natural* projection
(photon = `sinθ_W·W³` ⟹ composite closures screened by `sin²θ_W = 3/8`) gives `137.028`, missing CODATA
by `0.008`; the `5/8` the data wants is not the natural projection, and the alphabet's several
sub-fractions make any match a choice, not a derivation. What the test *did* establish is forced: the
two census generating functions satisfy the **Dyson/1PI resummation `G = 1/(1−I)`** — every closure is an
ordered sequence of prime (irreducible) closures. The **curvature route is also adjudicated**: positive
directional-sphere curvature gives the right *sign* (`d_eff > 3 ⟹ α⁻¹ > 137`), but the *magnitude* is the
wrong scale — `κ = 0.036` is a `0.4%` correction while geometric curvature invariants are O(1) (10–40×
too big); the residual sits at the closure-order scale (`κ ≈ 4.6·α_bare`), so curvature is not a
standalone mechanism but must *be* the closure-order resummation.

**The investigation has now converged** ([`Alpha_Residual.md`](Alpha_Residual.md) §9b–§9c;
[`alpha_residual_bridge.py`](alpha_residual_bridge.py), [`intermittency_bridge.py`](intermittency_bridge.py),
[`intermittency_seeded.py`](intermittency_seeded.py)). The pre-registered census bridge confirmed the
**`2/(3π)` coefficient survives the prime/1PI restriction** (`census_split → 1/6` for the prime census
too); the **turbulence/intermittency swing** was run to the end — its leg 1 *derives* She–Léveque's
`C₀ = 2` from `/solve` axis-minimality (a contribution back to [`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md) §6a),
but its leg 2 finds **no inertial range** in the closure census (vacuum or seeded, converged transfer
recursion) — the census is not a turbulent cascade. Every mechanism swing (weak, gauge, hypercharge,
curvature, 4-D projection, self-similarity×ways, turbulence) is now closed, each forced by an
independent computation. What remains is exactly one object, and it is **not** a census-truncation rule
(none exists — the truncation depth *is* the running): the **continuum vacuum-polarisation running**,
the Standard Model's own un-derived precision frontier, which QLF brackets by design.

---

## 4. The running — why α was higher in the early universe

In the SM the *effective* coupling grows with energy: `α(0)=1/137`, `α(M_Z)≈1/128`, higher beyond; the
hot early universe sampled higher energies, so effective α was larger. This is **vacuum-polarization
screening**, not a change of a fundamental constant. QLF reads it geometrically: the *effective*
dimension is emergent (Myrheim–Meyer, [`lean/QLF_CausalDimension.lean`](lean/QLF_CausalDimension.lean))
and **reduces toward `2` in the UV** (the universal `d→2` of causal sets / CDT / asymptotic safety).
Through `α(d)=1/(128+d²)`, a flow `3→2` takes `α: 1/137→1/132` (`alpha_QLF_2d_counterfactual`) — the
**correct SM direction** (α grows in the UV). Cosmologically: *α was higher because space had not yet
fully rendered to 3-D.*

The RG structure itself is Lean-anchored in [`lean/QLF_RunningCouplings.lean`](lean/QLF_RunningCouplings.lean):
one-loop `1/α(t)=1/α₀+(b/2π)·t` (`inv_coupling`, the `2π` loop phase), asymptotic freedom
(`asymptotic_freedom`) vs screening (`infrared_growth`), the Landau pole *located*
(`landau_pole_location`) but **cut off by the substrate's discrete UV floor** — no continuum UV
catastrophe ([`TheContinuum.md`](TheContinuum.md) §3.1). The strong β-coefficient is substrate-fixed
`b₀=7` (`beta_coefficient_eq_seven`, [`lean/QLF_BetaFunction.lean`](lean/QLF_BetaFunction.lean)), feeding
the `14π` hierarchy ([`lean/QLF_AlphaS.lean`](lean/QLF_AlphaS.lean)).

### 4a. The QED vacuum-polarization running from the census (issue [#117](https://github.com/jimscarver/quantum-logical-framework/issues/117))

The *matter* vacuum-polarization running — the piece the dimension-flow leaves to the β-coefficient
sector — is now derived from census counting, three modules, every factor value-free (committed
before comparison to QED, Step-0):

* **The coefficient `2/(3π)`** ([`lean/QLF_VacuumPolarization.lean`](lean/QLF_VacuumPolarization.lean); **1PI-confirmed** — `census_split → 1/6` holds for the *prime* census `2·Catalan(n−1)` exactly as for the total, so `2/(3π) = (1/6)·(4/π)` is a property of irreducible fermion loops, not an artefact of counting reducible ones, [`alpha_residual_bridge.py`](alpha_residual_bridge.py)).
  The one-loop coefficient decomposes `2/(3π) = 2·(1/6)·2·(1/π)`; the two non-trivial factors are
  counted. The **`3`** is the **two-vertex split census**: a fermion loop cut at its two photon
  vertices splits into arcs `k` and `n−k`, the two-vertex insertion count is `k(n−k)`, and
  `∑_{k=0}^{n} k(n−k) = C(n+1,3)` (`census_split`), so the split-average `→ 1/6 = 1/3!` — **proven** to
  be the Feynman parameter integral `∫₀¹ x(1−x) dx` as a genuine limit (`splitRiemannSum_tendsto`, via
  the exact `= 1/6 − 1/(6n²)`), not just a closed-form match. The **`π`** is the Wallis census return
  density (`QLF_PhysicalPi`). The two `2`s (e⁺e⁻ pair, `μ²=2ln μ` round-trip) are rendered vertex
  structure. Yields `b = −4/3` per unit-charge fermion (`qed_beta_coeff_per_fermion`, screening sign).

* **The running function** ([`lean/QLF_VacuumPolarizationTower.lean`](lean/QLF_VacuumPolarizationTower.lean)):
  **the QED logarithm IS the census octave count.** The horizon map `Q(R)=Q₀·2^R` makes the
  `closedAtHorizon` resolution pass `R` the octave counter (`log_scale_additive`); each octave adds the
  *scale-free* increment `(2/3π)Q_f²·log 2` (octave-independence reused from Kolmogorov's
  `flux_scale_invariant`); and the discrete octave count renders *exactly* to the smooth `ln(Q/m_f)`
  (`octave_tower_recovers_qed_log`). Fermion thresholds are automatic (ℕ-truncated `R_Q−R_f → 0` below
  threshold), and `α⁻¹` decreases monotonically toward the UV (`towerRunning_le_alpha0`, screening).

* **The charge census** ([`lean/QLF_ChargeCensus.lean`](lean/QLF_ChargeCensus.lean)): summed over QLF's
  own Standard-Model content — 3 generations (the axes), 3 colours, charges `1, 2/3, 1/3` (thirds from
  the 3 colours), neutrinos neutral — the vacuum-polarization weight is **`Σ Nᶜ Q_f² = 8 = 2³`**
  (`totalChargeCensus_eq_eight`/`_two_cubed`): the charge census *equals the 8-twist alphabet size*
  (cousin of the `128 = 2⁷` in `α⁻¹ = 128 + d²`), split **leptonic 3 + hadronic 5** (the `Δα_lep ≈
  Δα_had` near-equality). The fully-active slope is `16/(3π)` per `ln Q` (`smRunningSlope_eq`).

So `α⁻¹(Q²) = α⁻¹₀ − Σ_f (2/3π)Q_f²·ln(Q²/m_f²)` is assembled with every factor census-sourced —
coefficient, log, and charges. This **tightens `α(M_Z)`** and complements the `3→2` dimension-flow
reading above (the geometric contribution) with the matter-loop contribution.

**Honest scope:** the dimension-flow gives the right *direction* + a geometric *contribution*, and
§4a now derives the matter vacuum-polarization *structure* (coefficient + running function + charge
census) value-free; the residual for the full running *magnitude* / the `0.036` value is the
**threshold octaves** `R_f` (the fermion mass spectrum — ratios derived, absolute scale the open `g`)
plus the **non-perturbative hadronic** `Δα_had` (open in the Standard Model itself). **Not fitted.**

**How the α-residual improves once the electroweak scale is pinned** (issue
[#136](https://github.com/jimscarver/quantum-logical-framework/issues/136)). The absolute scale that
sets the threshold octaves `R_f` is `v ↔ R_stable`, now closed *structurally* to a single self-organized-
critical observable `ρ* = √(c/k)` (frontier #1: `QLF_ClosureAttraction` → `QLF_SteadyStateDensity` →
`QLF_ElectroweakScale`, `R_stable = 1/ρ*`). So the `0.036` residual splits cleanly into **three
independent pieces**: (i) the **threshold part** — set by the mass spectrum, whose *ratios* are derived
(`m_p/m_e = 6π⁵`, Koide, …) and whose overall scale is `ρ*`; **once `ρ*` is known the thresholds are
predicted, not calibrated**; (ii) the **higher-order census tail** (length-4+ closures) — internal and
independent of `ρ*`; (iii) the **non-perturbative hadronic** `Δα_had` — an external SM-like problem the
SOC work does not touch. So the residual is no longer a single opaque number but `{ρ*}` + two isolated
pieces — cleaner and partially predictive, **without adjusting any rule to force a match**.

---

## 5. No cosmological-time drift of α(0)

**Scoped to the *leading* value `α_lead(d)=1/(128+d²)`: it carries no time argument, so it cannot drift
— obvious within QLF, not a hard-won prediction** (the *exact* value's full scale-dependence is the
running of §4 plus the in-progress census tail). The substrate is pure combinatorics with
**no external scale** (the only scale, the Planck floor, is itself by-construction), so the leading
dimensionless value has nothing to vary against — neither energy nor cosmic time. (The
*effective* coupling `α(μ)` *does* run with energy — §4 — but that is screening of the same fixed
`α(0)`, not a change in it.) Concretely,
`α(d)=1/(128+d²)` has **no scale and no time argument**: `α(0)=α(3)=1/137` is an atemporal, scale-free
structural fact — manifest from the closed form, recorded as `no_cosmological_drift_of_alpha` (with
`alpha_at_dim_closed_form`, `alpha_at_dim_three`, `alpha_at_dim_eq_alpha_QLF`). There is no dynamical
variable for it to drift along; the 8-twist alphabet is the substrate's *definition* (not a field) and
`d=3` is fixed by necessity ([`SpaceTime.md`](SpaceTime.md) §3a). So within QLF this is a **theorem — a
trivial one**, on the **same footing as `α=1/137` itself**; we don't need to belabor proving the obvious,
and the Lean marker simply records it.

It is **sharper than the SM**, which treats `α(0)` as a free input that varying-α models can promote to a
drifting scalar field; QLF *structurally forbids* it. As an empirical claim about the *universe* it is a
falsifiable **prediction** — a confirmed cosmological drift of `α(0)` would falsify the QLF substrate —
but that "does QLF describe our universe?" caveat is the **universal** one attached to *every* QLF result
(`α=1/137` included), not a special weakness here. Distinct from the §4 energy-running of the *effective*
coupling (real, screening); this concerns the *fundamental* value over cosmic *time* (the Webb axis —
mainstream measurements consistent with null).

---

## 6. 4-D / 5-D and the over-determination of 3-D

The counterfactual values `α(4)=1/144`, `α(5)=1/153` (`alpha_QLF_4d_counterfactual`, `alpha_at_dim_five`)
do **not** support a viable physics — and not merely because the number is off. At `d ≥ 4` the physics
collapses, from QLF's own structures, three ways at once:

1. **Atoms — none above 3-D.** QLF derives `F ∝ 1/r^(d−1)` (holographic surface count,
   [`Gravity_From_Delay.md`](Gravity_From_Delay.md)), so `V ∝ 1/r^(d−2)`: stable Bohr orbits at `d=3`
   (`1/r`), critically unstable at `d=4` (`1/r²`), collapse at `d=5` (`1/r³`) — the **Ehrenfest (1917) /
   Tangherlini** theorem, here a *consequence of QLF's own force law*. So `α(4)`, `α(5)` describe
   substrates with **no stable atoms** — they exclude chemistry, they don't support it.
2. **Nuclei — wrong magic numbers.** The `ℓ=3` shell threshold is 3-D-specific
   ([`Magic_numbers.md`](Magic_numbers.md): `d=4→ℓ≥2`, `d=5→ℓ≥1`); the observed `2,8,20,28,50,82,126`
   requires `d=3`.
3. **Forces — unification breaks.** `U(1)×SU(2)×SU(3)` is the algebra of the **3 spatial axes**
   ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)); `sin²θ_W=3/8`, `α=N=3²` are 3-D-locked.
   QLF unifies the three forces as **projections of one 3-axis closure** — it does *not* add dimensions
   to unify (contrast Kaluza–Klein / string, where `5-D`+ *is* the mechanism). So 4-D/5-D *break*
   unification rather than enabling it.

**Over-determination is the real answer.** `α=1/137` (`d=3`) is the unique value simultaneously
consistent with the measured α, stable atoms (Ehrenfest), the magic numbers, Newton's `1/r²`, three
generations, `sin²θ_W=3/8`, and the minimal-faithful-rendering necessity. The 4-D/5-D values fail
several at once — which is why 3-D is a *derivation*, not a coincidence. (Higher `d` appears only as the
*effective* dimension — the §4 UV flow, or effective configuration-space behavior of composed closures,
[`eight-twists-sufficiency.md`](eight-twists-sufficiency.md) — never as the macroscopic rendering.)

---

## 6a. Rigidity — 137 is the *only* reachable value (the anti-Eddington capstone)

§6 settles *which dimension*; this settles *which value*. The over-determination argument answers the
Eddington charge — *did you tune the framework to hit 137?* — in its sharpest, machine-checkable form:
inside a **frozen, substrate-motivated grammar of derivations, no other value is reachable at all.** Had
the construction come out 136, QLF would be **refuted, not revised** — it cannot follow a moving
measurement. This is *rigidity*, not existence (the value is already derived above); the
motivation-first design and the Lean build program are tracked in
[issue #116](https://github.com/jimscarver/quantum-logical-framework/issues/116).

**The construction, operation by operation** (each motivated *without reference to 137*): `α⁻¹ = 128 + 9
= 2⁷ + 3²` — the **product** of the four physical selectivities gives `1/128 = 2⁻⁷` (`alpha_bare`); the
`d×d` input×output **directional-coupling tensor** at the minimal faithful dimension `d=3` gives `N = 9`
(`N_directional_modes`); the self-energy **resummation** `α_bare/(1+Nα_bare)` joins them as
`α⁻¹ = 1/α_bare + N`. The value is the *output* of running these; none of the rows names it.

**The frozen grammar.** The rigidity claim is only as strong as the grammar is honest — every extra
operation inflates the reachable set. So the admissible derivations are *exactly* the operations above:
leaves are the substrate primitives that actually appear as values (the powers-of-2 selectivities and
the axis count `3`), and the operations are `prod`, `pow`, `sum` — nothing else. (The alphabet
cardinality `8` and the `6+2` split are structural *inputs* to the selectivities, not value-leaves of
the `α⁻¹` expression.) Values are count-pairs (`ℚ` = two finite integers); approaching `1/3` or `π`
costs no infinite bits anywhere — a ratio is two finite counts, the binary expansion is display, not
ontology.

**The one physical premise — realization (P1), an explicit axiom.** The *elementarity* half of the
argument rests on one premise, marked as an `axiom` so the checker always reports it: *every arithmetic
factorization of the closure count of an independently existing (ZFE-closed) system is realized by an
available decomposition into independent sub-receipts.* Its motivations are tensor-factorization of
composite-dimension spaces (the isomorphism always exists; physics need not respect any *particular*
one — which is exactly why it is a postulate, not a theorem) and MUB/stabilizer completeness at prime
dimension. **QLF-native scope:** independent existence *is* ZFE closure, so free charges (unterminated
ledgers) are not independent existents and fall **outside** P1 — the resolution of the proton objection,
which reclassifies a bare charge out of scope rather than making it a counterexample. (Isolation
improving stability is recorded as *motivation*; dynamical stability is not counting-theoretic and is
not claimed — the chain routes through elementarity = ZFE-closed ∧ not decomposable.)

**The proof shape** ([`QLF_AlphaRigidity`](lean/QLF_AlphaRigidity.lean); [issue #116](https://github.com/jimscarver/quantum-logical-framework/issues/116)):
invariants kill infinite families, the finite residue is checked directly. **The elementarity spine is
machine-checked:** a prime count admits no factorization, so it is *atomic* (`prime_implies_atomic`, I2);
P1 is the single explicit `axiom` (`realization`); together they give *elementary ⟺ prime*
(`elementary_iff_prime`, I3). **And R1/R2 is machine-checked — as a *cross-sector consistency theorem*, not rigidity over a knob.** `d` is **not** a free parameter: it is substrate-derived (the `6+2` split yields 3 axis-pairs; minimal-faithful-rendering forces the dimension — *not* read off from "our perspective is 3-D," which would feed a measured datum into `128 + d²` and degrade the parameter-free claim to a one-datum fit). So two *independent* substrate derivations — the **dimension** (`d = 3`) and the **bare coupling** (`128 = 2⁷`) — meet, and `alpha_unique` (`128 + d² = 137 ⟺ d = 3`) proves they meet with **zero slack**, at exactly one point. `rival_excluded` re-reads as the no-slack lemma: the sectors are **locked**, since a 4-D rendering would force `144`, so the framework could not have accommodated a mismatch between its own two derivations — and that it did not have to is the checkable fact. This is **overdetermination**, the strongest evidence QLF has. **A third sector agrees:** `137` is prime (`inverseAlpha_three_prime`), hence elementary — dimension, bare coupling and elementarity all meet at `α⁻¹ = 137`. Slogan: **`α⁻¹` counts the rendering dimension** (`alpha_counts_dimension`). **The `136` payoff, both deaths proven:** composite ⟹ non-elementary, *and* unreachable at any dimension (`dimension_136_unreachable`). **Honest scope:** `d = 3` is evidenced at both the *counting* layer and the *mechanism* layer (the receipt-quotient growth dimension = the axis-pair count, #62), so the swap-graph check lands at 3 too; the residuals are the posited atomic-integration→axis-winding map and, on the rigidity side, the full grammar enumeration (#116).

**The `N(d)` look-elsewhere census, computed ([`alpha_rigidity_census.py`](alpha_rigidity_census.py), issue #116).**
The last open acceptance criterion — the reachable-value count over the *full free-`Expr` grammar* — is
now computed, and it delivers an honest, load-bearing clarification rather than a small number. Over the
free grammar the look-elsewhere is **large**: `137` needs depth ≥ 2 (no single op reaches it), but at the
construction's own depth 2 roughly **60 %** of the ±9 integer band `[128, 146]` is already reachable (`137`
among them, not sparse), and by depth 3 the whole band is filled (19/19); ten levels are far more than
enough — the reachable set saturates to every integer up to the cap by depth ≈ 3. So **grammar sparsity
provides no rigidity** — consistent with the already-proven `grammar_reaches_all` (the frozen grammar
excludes nothing, even `136`). The rigidity therefore lives **entirely in the frozen template** `α⁻¹ =
128 + d²` with `d` substrate-derived: there `137` is unique at `d = 3` with **zero slack** and `136` is
unreachable (`d² = 8` has no natural solution) — exactly the `alpha_unique` / `dimension_136_unreachable`
/ cross-sector-overdetermination joint already machine-checked above. The census quantifies *why* "all
rigidity lives in the template" is the correct reading, and pins the `136`-dies-twice anti-Eddington
sentence as a **template** fact (the free grammar *does* reach `136`; the template does not). A Lean
`reachable_finite` over the free grammar would be true but non-load-bearing (the count is large), so the
honest close is the census + the proven template lock, not a Lean enumeration.

**Honest scope.** The identification "this closure structure *is* the electromagnetic coupling" is the
interpretive premise stated in §1 (uncertified). The rigidity claim is about the *integer* value `137`;
the `0.036` residual is the separate registry item (only the proven bound `137 < α⁻¹ < 137.048` of the
[bounds section](#bounds-on-α-machine-checked) is machine-checked, not a from-scratch `137.036`). Prime
*bit*-count is a different claim, not made.

### 6a.1 — "Why 137" is four questions; claim only the layers that hold

"Why 137" is not one question but four, and honesty means answering each at its own status:

1. **Why 137 and not another value *within QLF*** — answered as **cross-sector overdetermination**,
   machine-checked: two independent substrate derivations (the dimension `d = 3` from the 6+2 split, the
   bare coupling `128 = 2⁷`) meet at `137` with **zero slack** (`alpha_unique`: `128 + d² = 137 ⟺ d = 3`;
   `rival_excluded`), and elementarity agrees (`137` prime). `d` is substrate-derived, *not* a fitted or
   observed parameter — so this is not "137 was tuned to hit" but "the sectors could not have missed and
   didn't." *Residual:* that the admissible constructions are *exactly* `{128 + d²}` (no other
   expression-shape admissible) is the Step-0 restriction, not yet a free-grammar enumeration.
2. **Why *this* grammar** — two halves, at different statuses. The **alphabet** half is **proven**:
   `|Σ| ∈ {2,4,8}` with `6` impossible, `8` forced by two distinguishable spatial axes, and the axis
   count `3` unavoidable once more than one spatial direction exists
   ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)) — and the two smaller alphabets are
   degenerate, being abelian with no SU(2), no double cover and no spin, so neither carries
   electromagnetism at all. The `3` and the `8` that feed `128 + 3²` therefore come from a set of size
   three, two of whose members have no α to speak of. The **expression-grammar** half — that the
   admissible shapes are *exactly* `{128 + d²}` — remains the Step-0 restriction, argued in prose
   (§6a), and the free-grammar census shows it is where the look-elsewhere lives.
3. **Why this closure structure *is* the electromagnetic coupling** — the interpretive premise (§1),
   permanently uncertified by Lean.
4. **Why 137.036** — open (the residual registry item).

Filled rigidity gives a real, machine-checked answer to (1), *conditional on* (2) and (3), *silent on*
(4). That is an honest "why 137" of a kind almost nobody has — but it is conditional, and saying so
first is what keeps it credible.

## 6b. Who else pegs α — the landscape (and why exclusion is the empty market)

The genre of "deriving 137" is crowded; QLF's position is only distinctive read against it. Four tiers:

- **Mainstream: nobody.** Quantum theory does *not* predict α's value — it is one of the ~20 external
  parameters of the Standard Model, inserted from experiment. That standing vacuum is what any
  derivation steps into.
- **The nearest serious peer — Singh's octonionic program (TIFR).** Tejinder Singh and collaborators
  propose a pre-quantum, pre-spacetime *trace/matrix dynamics* in which the octonions and the
  **exceptional Jordan algebra** encode the Standard Model, with parameters fixed by roots of the
  algebra's cubic characteristic equation — and the asymptotic low-energy `1/137` is *derived*.
  Published, institutionally serious, and structurally the closest rival: an 8-dimensional algebraic
  substrate yielding the integer. A competent reviewer will make this comparison unprompted, so QLF
  makes it first. **The differentiators QLF can state today:** the Lean verification of the combinatorial
  layer, and the **bounds theorem** (`137 < α⁻¹ < 137.048`, an interval that *could have failed*) — both
  landed and machine-checked. The **cross-sector consistency joint** (§6a) is the further differentiator
  Singh's framework does not attempt — machine-checked: the dimension and bare-coupling sectors meet at
  `137` with zero slack (`alpha_unique`/`rival_excluded`), a third sector (elementarity, `137` prime)
  agreeing, with the full free-grammar look-elsewhere census the named residual.
- **Consistency checks misread as derivations — the MSSM running.** Integrating the β-functions down
  from a unified coupling (`≈ 24.3` at the GUT scale) with threshold corrections reproduces the measured
  α — but it *inputs* the unified coupling and the entire particle content, so it demonstrates
  *compatibility*, not explanation. Worth naming because "the Standard Model already explains α" will be
  raised, and this is what that claim actually amounts to.
- **The swamp — and it is strategically load-bearing.** The genre is dense with 137 derivations:
  geometric-resonance substrates, prime-constant formulas, `1/2⁷` numerology, closed forms claiming
  "a perfect match to all 11 digits, the question closed forever" — with the historical anchor being
  Eddington, who needed a multiplicity of 137 and *defined the constant to fit*. **The density of this
  swamp *is* the look-elsewhere argument made flesh:** producing 137 is demonstrably easy, which is
  exactly why the hit itself carries little weight, and why QLF's hedged framing (bounds not exact value,
  spine landed but exclusion staged) is survival, not modesty — every overclaimed sentence
  pattern-matches into this tier.

**The competitive conclusion is clean.** Many frameworks *reach* 137; none — Singh included — proves its
framework *could not reach anything else*. **Existence proofs are the crowded market; the exclusion
theorem is the empty one.** Many frameworks *reach* 137; none — Singh included — proves its own sectors
could not have missed each other. QLF's machine-checked **overdetermination joint** (dimension × bare
coupling × elementarity, meeting at `137` with zero slack) is that empty-market result, with the
full-grammar look-elsewhere census the named residual — on top of the two differentiators already true
regardless: a Lean-verified combinatorial derivation, and a bounds theorem that could have failed.

---

## 7. Parallel derivation pathways

QLF reaches α by more than one route; their agreement is a non-trivial internal consistency claim:

| Pathway | What it derives | Status | Reference |
|---|---|---|---|
| **Substrate combinatorial** | `α = 1/137` from the 8-twist alphabet + `N=9=3²`, zero input (§2) | ✅ Lean (`alpha_QLF_eq`) | this doc; [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1 |
| **Bohr / Rydberg inversion** | the *identity* `Ry = ½α²m_e c²` (Tier-1, structural) ⇒ `α = √(2Ry/m_e c²)` to 10⁻¹⁰ (Tier-2, with measured `Ry`, `m_e`) | ✅ identity derived; value uses measured inputs | [`Hydrogen.md`](Hydrogen.md) §§2–4; `fine_structure_demo.py` |
| **Chirality-hiding `R_e = R_p·6π⁵`** | α via the electron/proton Markov-blanket depth ratio (the Lenz coincidence) | 🔵 Tier-3 open (needs `R_e` from closure multiplicity) | [`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md) |

The combinatorial route is the one that lands the value with **no observable input**; the three should
converge in a complete theory (open cross-check).

---

## 8. α and the other substrate constants — the shared 6+2 split

**The split is forced, not observed.** The alphabet is the signed axis frame, so `|Σ| = 2·|axes|`, and a
composition-closed axis set is a subgroup of the Klein four-group: the alphabet size is `2`, `4` or `8`
and **never `6`**, the axis count is `1`, `2` or `4` and **never `3`** — two distinct spatial axes carry
the third with them (`two_spatial_axes_force_three`), and the gauge axis is what closure requires rather
than an addition to the spatial six (`frame_contains_I`). So `6+2` is `3 spatial axes + 1 gauge axis`,
each doubled by handedness, and it is the one split of the alphabet there is
([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean), [`QLF_Handedness`](lean/QLF_Handedness.lean),
zero axioms).

That matters for what follows: α's `3²`, the Weinberg `3/8`, and the cosmological `2/8` read off a
partition with **no alternatives**, so agreement across them is overdetermination rather than a shared
convention.

**Two conventions live in the table below, and they are different objects.** A *projection* fraction is
a ratio of **axes to elements** (`sin²θ_W = 3/8` — the SU(5) normalization). A *census* fraction is a
ratio of **elements to elements**, and since ZFA is zero net handedness **per axis**
(`zfa_iff_handedness_balanced`), a census fraction must be a union of whole axes: `2/8, 4/8, 6/8, 8/8`.
`3/8` and `5/8` are not census fractions. See [`Alpha_Residual.md`](Alpha_Residual.md) §3a, where that
constraint closes the gauge-projection route to the residual.

The `6 spatial + 2 gauge` split (the `3` spatial axes) is the *same* structure
behind several constants — α is one face of it:

| Constant | Value | Tie to the `6+2` / `3` | Lean |
|---|---|---|---|
| **α** | `1/137` | `N = 3² = 9` directional tensor | `alpha_QLF_eq` |
| **Weinberg angle** | `sin²θ_W = 3/8` (unification) | spatial fraction `3/8` = SU(5) normalization | `sin2_weinberg_substrate_eq` ([`lean/QLF_WeinbergAngle.lean`](lean/QLF_WeinbergAngle.lean)) |
| **Cosmological constant** | `Ω_Λ = log 2` (1.2%) | gauge fraction `2/8 = 1/4` | `only_2_gauge_matches_observed_Omega_Lambda` ([`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)) |
| **Three generations** | `3` | `num_generations = substrate_spatial_dimension = 3` | `num_generations_eq_three`, `three_axis_signature` ([`lean/QLF_Generations.lean`](lean/QLF_Generations.lean)) |
| **SU(5) generation content** | `5̄⊕10 = 15` | the `5 = colour(3)⊕weak(2)` split | `generation_eq_fifteen` ([`lean/QLF_SU5.lean`](lean/QLF_SU5.lean)) |
| **Newton's law** | `F ∝ 1/r²` | holographic surface `∝ r^(d−1)`, `d=3` | `newton_exponent_only_3d_matches` ([`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean)) |
| **Nuclear magic numbers** | `2,8,20,28,…` (`ℓ=3` threshold) | 3-D-SHO degeneracy `(k+1)(k+2)`, `k>2` | [`Magic_numbers.md`](Magic_numbers.md) |

So α's `3²` and the Weinberg `3/8` and the cosmological `2/8` are **one substrate fact read three ways**
— the strongest cross-check on the 3-dimensionality.

---

## 9. Forces from α

The **dimensionless** Standard-Model force strengths root in α (itself `N=3²`) plus the integers `2,7`;
only the **absolute scale** needs one empirical mass (`m_e` or `m_p`). So the four forces reduce to *one
derived structure (α) + one empirical mass* — [`Forces_From_Alpha.md`](Forces_From_Alpha.md). The forces
are different **projections of the one 3-axis gauge-twist closure** that already produces α
([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md); EM abelian vs weak/strong non-abelian,
`gauge_unification_signature`, [`lean/QLF_GaugeUnification.lean`](lean/QLF_GaugeUnification.lean)).

---

## 10. Where α is used — downstream derivations

The derived α feeds the atomic/EM tree; each derivation *justifies its α* by pointing here:

| Quantity | Relation | Match | Lean / doc |
|---|---|---|---|
| Rydberg / Bohr | `Ry = ½ α² m_e c²`, `a₀ = ℏ/(α m_e c)` | identity exact | [`Hydrogen.md`](Hydrogen.md) §§2–4 |
| Dirac fine structure | spin-orbit / kinematic / Darwin `∝ α²` | closes 0.05% residual | `three_mechanisms_alpha_squared` ([`lean/QLF_DiracCorrection.lean`](lean/QLF_DiracCorrection.lean)) |
| Lamb shift | prefactor `4/(3πn³)` with the loop `α` | structural | `lamb_prefactor_loop_phase` ([`lean/QLF_LambShift.lean`](lean/QLF_LambShift.lean)) |
| Electron `g−2` | `a_e = α/2π` (Schwinger) | 0.2% | `a_e_QLF_eq_schwinger`, `g_factor_QLF_eq` ([`lean/QLF_GMinusTwo.lean`](lean/QLF_GMinusTwo.lean)) |
| von Klitzing | `R_K = h/e² = Z₀/(2α) ≈ 25813 Ω` | 0.026% (= α error) | `von_klitzing_substrate`, `hall_resistance` ([`lean/QLF_CondensedMatter.lean`](lean/QLF_CondensedMatter.lean)); [`Electricity.md`](Electricity.md) §7 |
| Charged pion | `m_π±/m_e = 2/α = 274` | 0.3% | `pion_electron_ratio_eq`, `proton_pion_ratio_eq` ([`lean/QLF_PionMassRatio.lean`](lean/QLF_PionMassRatio.lean)); [`Pion_QLF.md`](Pion_QLF.md) |
| Hyperfine (21 cm) | `ΔE_HFS ∝ α⁴` | reproduced (Tier-2) | [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §5 |

---

## 11. The constants mapper

[`constants_mapper.py`](constants_mapper.py) reports α's **leading value** `α_lead = (1/128)/(1+9/128) =
1/137` as derived (no measured input, `0.026%` from `1/137.036`); the exact value is in progress (status
box). It is distinct from the
`gauge_spatial_count_ratio` (a `[NATIVE]` ensemble observable, *not* α) and bridge quantities like
`G_prediction_SI` (`[BRIDGE]`). Run `python3 constants_mapper.py` to see the full provenance-tagged
report.

---

## 12. Lean-theorem index

All in [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) unless noted; finite
rational arithmetic (`norm_num`), no axioms beyond Lean/Mathlib.

**Derivation:** `naive_closure_rate`, `gauge_selectivity`, `phase_coherence`, `spatial_colocation`,
`alpha_bare`, `alpha_bare_eq`; `substrate_spatial_dimension`, `N_directional_modes`,
`N_directional_modes_eq_nine`; `alpha_QLF`, **`alpha_QLF_eq`** (`= 1/137`).
**Dimension dependence:** `alpha_QLF_2d_counterfactual` (`1/132`), `alpha_QLF_4d_counterfactual` (`1/144`),
`alpha_at_dim`, **`alpha_at_dim_closed_form`** (`α(d)=1/(128+d²)`), `alpha_at_dim_three`,
`alpha_at_dim_five` (`1/153`), `alpha_at_dim_eq_alpha_QLF`, `only_3d_substrate_gives_137`.
**Scale / time:** **`no_cosmological_drift_of_alpha`**.
**Running (context):** `inv_coupling`, `asymptotic_freedom`, `infrared_growth`, `landau_pole_location`,
`running_couplings_structural` ([`QLF_RunningCouplings`](lean/QLF_RunningCouplings.lean));
`beta_coefficient_eq_seven` ([`QLF_BetaFunction`](lean/QLF_BetaFunction.lean)).
**Downstream:** `three_mechanisms_alpha_squared`, `lamb_prefactor_loop_phase`, `a_e_QLF_eq_schwinger`,
`von_klitzing_substrate`, `pion_electron_ratio_eq` (modules in §10).
**Shared `6+2`:** `sin2_weinberg_substrate_eq`, `only_2_gauge_matches_observed_Omega_Lambda`,
`num_generations_eq_three`, `generation_eq_fifteen`, `newton_exponent_only_3d_matches` (modules in §8).
**The split itself:** `frame_axisCount_trichotomy`, `alphabetSize_trichotomy`, `no_six_twist_alphabet`,
`two_spatial_axes_force_three`, `frame_contains_I`, `noncommuting_iff_eight`
([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)); `zfa_iff_handedness_balanced`,
`chiralCharge_eq_handednessOn_gauge` ([`QLF_Handedness`](lean/QLF_Handedness.lean)) — `6+2` is `3 spatial
axes + 1 gauge axis`, each doubled by handedness, with `|Σ| = 6` impossible and an axis count of `2`
unavailable.

---

## 13. Honest scope

**Status on two axes** ([`ScientificApproach.md`](ScientificApproach.md) §3) — mathematical (what is
established about the formal object) and physical (what is established about the world):

| Claim | Mathematical | Physical |
|---|---|---|
| `α_lead = 1/(128 + 3²) = 1/137`, `alpha_QLF_eq` | **Proved** | **Retrodiction** — the comparison target was known |
| `α(d) = 1/(128 + d²)`, `only_3d_substrate_gives_137` | **Proved** | **Internal** |
| bounds `137.01587 < α⁻¹ < 137.04813` (both ends) | **Proved** (`irreducibleCap_eq`, `alphaInvCap_eq`) | **Predicted absent** — a two-sided null CODATA lands inside |
| the equal-weight prediction `α⁻¹ = 137.032` (`w = ½`) | **Proved structural** — `w = ½` forced by the free monoid / no bifurcation | **Prediction** — `~0.004` from CODATA, the gap being the continuum running |
| `no_cosmological_drift_of_alpha` | **Proved** (scoped to the leading value) | **Pre-registered prediction** — the SM permits a varying-α field; the test is not yet decisive |
| the `6+2` split is the only split | **Proved** | **Internal** |
| the exact `1/137.035999` | **Existence proved** (`0.036` strictly inside the bracket; some prime-resummation gives it) | **Open — the multiplicity** (which resummation / how many 1PI insertions = the continuum running; every substrate mechanism swing closed, [`Alpha_Residual.md`](Alpha_Residual.md) §9c) |

`no_cosmological_drift_of_alpha` is the only row here that can *confirm* rather than retrodict — the
leading value's agreement with CODATA is a retrodiction however exact, since `137.036` was in view when
the reading was built ([`Alpha_Residual.md`](Alpha_Residual.md) §0a).

- **Derived (zero free parameters, Lean-verified): the leading value `α_lead = 1/(128+9) = 1/137`** — why
  the substrate's combinatorics + 3-D rendering give the integer `137` (the `2⁻⁷` bare coupling, the
  `+d²=9` directional screening), `0.026%` from CODATA's `1/137.036`.
- **Bounded + structural: `137.01587 < α⁻¹ < 137.04813` (proved both ends), and `137.032` from `w = ½`.**
  The two caps are the total-census (`+0.0481`) and prime-only (`+0.0159`) resummations; `w = ½` between
  them is the equal-weight prediction, and `w = ½` is *forced* — unique prime factorisation → free monoid
  → geometric GF → linear recurrence → no period-doubling → no discrete-scale-invariance line to shift
  it. `137.032` is `~0.004` from CODATA.
- **Existence proved, multiplicity open: the exact `1/137.035999`.** `0.036` lies *strictly inside* the
  proved bracket, and total-resummation overshoots while one prime term undershoots — so *some* partial
  resummation of the primes gives exactly `0.036`. That is **existence**, not a fit: we have shown a way
  it manifests, so it *can* happen. The open number is the **multiplicity** — which partial resummation,
  i.e. how many 1PI insertions contribute as `q²→0` — and `Alpha_Residual.md` §2a shows that count *is*
  the continuum vacuum-polarisation running, not a census-truncation rule (none exists). Every substrate
  mechanism swing — weak, gauge, hypercharge, curvature, 4-D, self-similarity×ways, turbulence — is
  **closed**, each by an independent computation ([`Alpha_Residual.md`](Alpha_Residual.md) §9b–§9c). The
  turbulence swing's leg 1 produced a *side*-derivation: She–Léveque's `C₀ = 2` from `/solve`
  axis-minimality. CODATA's `137.035999(1)` is then an **estimate of the missing count** (`δw ≈ 0.124`),
  read off after the proof — an observation, not a target.
- **Structural (*direction* only):** the QED running ≈ effective-dimension flow `3→2` toward the UV
  (`QLF_CausalDimension` + the `1/132` counterfactual); not the running *magnitude*.
- **Scale/time-invariance of the *leading* value:** `α_lead(d)=1/(128+d²)` has no time argument, so the
  leading value can't drift — a closed-form fact *scoped to the leading value* (`no_cosmological_drift_of_alpha`);
  the exact value's full scale-dependence is the running (§4) + the in-progress tail. The empirical "does
  `α(0)` drift in cosmic time?" is a falsifiable check, with the universal "does QLF describe reality?" caveat.

The honest headline: QLF **derives why the leading value is `1/137`**, **proves the two-sided bracket**,
and shows the **`w = ½` prediction `137.032` is structural**. The exact `1/137.036` is *existence-proved*
(it is reachable by a prime resummation) with its **multiplicity open** — and that missing count is the
continuum vacuum-polarisation running, the Standard Model's own frontier, not a QLF gap.

---

## See also

- [`Alpha_Residual.md`](Alpha_Residual.md) §0a (the discovery/confirmation firewall and the pre-filter),
  §3a (which fractions a census can carry), §6a–§6b (two-axis status; the failure-criterion test),
  §9a (the pre-registered bridge), **§9b–§9c (the investigation converged: `2/(3π)` 1PI-confirmed,
  `w = ½` structural, the turbulence swing run to the end — `C₀ = 2` derived, no inertial range)**.
- [`Category_Theory_QLF.md`](Category_Theory_QLF.md) §3a — why the free-monoid bifibration makes
  `w = ½` a theorem rather than a fit.
- [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) · [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean)
  — the exact-RG recursion (no axiom): the perturbation series as the closure-order expansion,
  renormalization as the capacity horizon, Kraft convergence.

- [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1 — full prose derivation + demo.
- [`SpaceTime.md`](SpaceTime.md) §3a — why space renders 3-D, `α = N = 3²` as a consequence.
- [`TheContinuum.md`](TheContinuum.md) §3.1 — running couplings without a UV catastrophe.
- [`Forces_From_Alpha.md`](Forces_From_Alpha.md) · [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) — the forces from α.
- [`Hydrogen.md`](Hydrogen.md) · [`Dirac_Correction.md`](Dirac_Correction.md) · [`Lamb_Shift.md`](Lamb_Shift.md) · [`g_minus_2.md`](g_minus_2.md) · [`Electricity.md`](Electricity.md) · [`Pion_QLF.md`](Pion_QLF.md) — downstream uses.
- [`Beyond_Standard_Model.md`](Beyond_Standard_Model.md) — α as derived (vs SM free input) + the no-drift prediction.
- [`Open_Problems.md`](Open_Problems.md) — the renormalization / running sector status.
- [`README.md`](README.md) · [`lean/README.md`](lean/README.md) — the project overview and module table.
