# Curvature

**Gravity, magnetism, and de Sitter cosmology as signed deformations of the primordial Markov blanket.**

**Repository:** [`rchain-community/quantum-logical-framework`](https://github.com/rchain-community/quantum-logical-framework)
**Author:** Jim Whitescarver
**Date:** June 8, 2026

---

## The one premise, and the thesis

This document rests on the single conditional the whole framework rests on:

> **The universe IS a quantum-logical system, and physical reality is the subset of admissible histories that achieve Zero Free Action (ZFA = 0).**

From it, curvature is not a property of a pre-existing smooth manifold. It is **deformation of the discrete geodesic sphere that every Markov blanket is**. A blanket can be deformed in exactly two ways — it can **expand** or it can **contract** — and the whole of gravity, magnetism, and cosmology is which of those happens, where, and in which direction. The thesis:

> **One signed expand/contract deformation, at two scales.** Magnetism is the *local, anisotropic* form — spin-up expands and spin-down contracts the blanket along the vacuum spin axis. de Sitter/AdS cosmology is the *global* form — replication expands the cosmic blanket (de Sitter), entanglement contracts it (AdS). **Gravity is the isotropic, single-sign special case**: mass contracts the blanket in every direction at once.

The chain is: §1 builds the canvas (the blanket and its irreducible curvature), §2 the two deformations, §3–§5 gravity / magnetism / cosmology as instances, §6 the unification, §7 the framing.

---

## 1. The blanket and its irreducible curvature

In QLF an observer, a particle, a horizon — any closed system — is a **Markov blanket**: a topologically closed surface of ZFA-balanced half-spin closures screening its interior from its exterior. That surface is concrete and discrete: a **Fuller geodesic sphere** ([`Primordial_Markov_Blankets.md`](Primordial_Markov_Blankets.md); [`lean/QLF_PrimordialMarkovBlanket.lean`](lean/QLF_PrimordialMarkovBlanket.lean)). At Fuller frequency v it has

$$V = 10v^2 + 2, \qquad E = 30v^2, \qquad F = 20v^2, \qquad V - E + F = 2,$$

machine-verified as `primordial_blanket_euler` at every frequency. A flat triangular tiling has six triangles at every vertex; to *close* into a sphere, the surface must carry an **information deficit** — and the Euler characteristic requires it to appear at exactly **twelve 5-valent vertices** (`pentamon_count = 12`), the rest 6-valent. The twelve pentamons are the **irreducible, intrinsic curvature** of any closed blanket. They are present at v = 1 (the bare icosahedron) and at v ≈ 6.7 × 10⁶⁰ (the cosmic horizon) alike — curvature is a topological signature, not a quantity that can be tuned to zero.

This is curvature as **discrete topological deficit**, not Regge angular deficit and not smooth Riemannian curvature. The familiar metric is recovered as the **continuum limit** of the blanket. The blanket's depth sets the scale,

$$v(R) = \sqrt{\tfrac{\pi}{5}}\,\frac{R}{L_{\text{Planck}}} \approx 0.793\,\frac{R}{L_{\text{Planck}}}, \qquad F_v = 20v^2 = \frac{4\pi R^2}{L_{\text{Planck}}^2},$$

so the face count *is* the Bekenstein–Hawking area in substrate units (`holographic_event_count_blanket_eq`). (The blanket's closure symmetry is the binary icosahedral group 2I, which by the McKay correspondence carries E₈ implicitly — the symmetry backbone beneath everything that follows.)

Everything below is what happens when this canvas is deformed.

## 1a. Curvature, orthogonality, and the Lie algebra

The pentamon deficit (§1) is curvature as a *topological* signature. There is a second, complementary
face of curvature — the **gauge / holonomy** curvature — and it is exactly the **Lie bracket of the
one-bit orthogonal axes**. Machine-checked skeleton (reuse-only): [`QLF_CurvatureLie`](lean/QLF_CurvatureLie.lean).

1. **Orthogonality is one bit.** Each orthogonal axis is a binary / Hermitian-conjugate distinction
   resolved to `log 2` (`orthogonal_distinction_is_one_bit`, [`Geometry_Of_Space.md`](Geometry_Of_Space.md)
   §3c); the three orthogonal axes are `σx, σy, σz`.
2. **The one-bit orthogonal axes ARE the su(2) generators.** They close the su(2) Lie algebra
   `[σᵢ,σⱼ] = 2i·εᵢⱼₖ·σₖ` ([`QLF_Spin`](lean/QLF_Spin.lean), `su2_comm_xy/yz/zx`).
3. **Curvature = the non-commutativity of the orthogonal axes = the non-abelian holonomy = the Lie
   bracket.** The Wilson-loop plaquette (field strength) around a loop of orthogonal one-bit steps is
   `σxσyσxσy = −1 ≠ 1` — **curved** — precisely because su(2) is non-abelian
   ([`QLF_GaugeHolonomy`](lean/QLF_GaugeHolonomy.lean), `nonabelian_plaquette`); when the distinctions
   **commute** (abelian, the photon) the plaquette is `1` — **flat** (`em_plaquette_trivial`).

So the **structure constants `εᵢⱼₖ` *are* the curvature** — the amount by which going around a loop of
orthogonal one-bit steps rotates you — and the **one bit** (`log 2` = half-spin, the SU(2) double cover,
the `−I`/720° closure) quantizes the minimal curvature into the `−I` unit. *Abelian orthogonality is flat
(the massless photon); non-abelian orthogonality is curved (the self-interacting gluon/W — and the
gravitational self-interaction).* This is the same `6+2` / three-axis substrate as everything else
([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)).

**Metric curvature (a plausible extension).** The Riemann/metric curvature of §3–§6 is the continuum
limit; read through the frame bundle it is the curvature of the **Lorentz spin connection**
(`so(1,3) ≅ su(2)⊕su(2)`, [`QLF_LorentzCover`](lean/QLF_LorentzCover.lean) `SL(2,ℂ)→SO⁺(1,3)`), with the
one-bit orthogonal spatial axes as the su(2) spin frame — so metric curvature is *also* Lie-algebra-valued.
**Honest scope:** the gauge-curvature = Lie-bracket identity is a structural reading of proven pieces (the
standard gauge field-strength identity); the metric-curvature/spin-connection reading is a further
structural reading — QLF's metric is the Benincasa–Dowker continuum limit ([`QLF_CausalDimension`](lean/QLF_CausalDimension.lean)),
and the differential-geometric tensor step stays the named open piece ([`Einstein_Equations.md`](Einstein_Equations.md)).
The discrete Lie bracket is the *infinitesimal generator* that becomes the differential-geometric
curvature 2-form in the limit — one instance of differential calculus emerging as the continuum rendering
of the discrete substrate ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md)).

### 1b. What these two curvatures cannot do — a boundary found by using them

Both curvatures above are **divisions of the turn**: the holonomy plaquette takes values in the Pauli fold group `μ₄ = {±I, ±iI}` (a quarter-turn unit), and the pentamon deficit `2π − 5·(π/3) = π/3` is a sixth of one. Neither is an **arc-over-radius** ratio — `n` unit steps at radius `R` — and that turns out to be a real boundary rather than a bookkeeping remark.

The lepton Koide phase `Δ = 3δ = 2/3` is a *rational number of radians*. [`Weak_Force.md`](Weak_Force.md) §5c⁗ shows that no division of the circle can produce it (as a fraction of a turn it is `1/(3π)`; the smallest turn-fraction fitting the measurement is `33/311`), so **if** the phase is a curvature it must be an arc-over-radius one. §5c⁗ then computes curvature directly on the lepton ladder closures — closed walks in `ℤ³`, since count balance *is* closure — and finds no rung-independent ratio equal to `2/3`; the complete set is `{1/2, 1, 2}`.

So the two curvatures of §1–§1a are excluded from that job **twice over, by their own value sets**, and QLF as it stands carries no third object of the required shape. Recorded here because it is a genuine limit of the curvature notions this document builds on, not a defect of the lepton sector: a curvature that is a **ratio of counts** rather than a holonomy or a topological deficit would be a new primitive, and nothing above supplies one.

### 1c. The third curvature — Ollivier–Ricci on the possibility graph

§1b is a specification with nothing yet filling it: a curvature that is a **ratio of counts** — not a holonomy (a finite group, a division of the turn) and not a bare deficit count. Exactly one standard discrete curvature meets it.

$$\kappa(x,y) \;=\; 1 \;-\; \frac{W_1(m_x, m_y)}{d(x,y)}$$

**Ollivier–Ricci curvature** (Ollivier 2009): `mₓ` is the lazy random-walk measure at `x`, `W₁` the optimal-transport cost between the two measures, `d` the graph distance. Both numerator and denominator are pure step counts, so `κ` is rational by construction — no angle, no metric, no finite group. It is the discrete Ricci curvature in the sense that matters: `κ > 0` on spheres and complete graphs, `κ = 0` on flat lattices, `κ < 0` on trees and hyperbolic graphs.

| candidate | why it does or does not qualify |
|---|---|
| Regge angular deficit | a division of the turn — **no** |
| pentamon deficit (§1) | a count with no radius — **no** |
| holonomy / Wilson plaquette (§1a) | valued in the finite group `μ₄` — **no** |
| Benincasa–Dowker (`QLF_CausalContinuum`) | needs a length scale `ℓ²` to be a curvature — **no** |
| Forman–Ricci | combinatorial but integer-valued, not a ratio — partial |
| **Ollivier–Ricci** | `1 − W₁/d`, counts only — **yes** |

**QLF has two graphs, and they read oppositely under it.** Validated first on graphs of known curvature (`C₈ → 0`; `K₅ → +0.625`; `6×6` grid `→ 0` interior; `3`-regular tree `→ −1/3` interior, its positive values all leaf edges — a truncation artefact worth remembering):

| QLF graph | what it is | Ollivier–Ricci |
|---|---|---|
| the `ℤ³` lattice | **synthesized space** | `κ = 0` on every interior edge — **Ollivier-flat** |
| closure classes under the causal parent relation | the **census / possibility space** | `κ < 0` on **every** interior edge (`−0.801 … −0.112`) — **hyperbolic** |

> **This does not say space is flat — and the reason matters.** §1a is the primary statement: every fold carries **one bit**, and the plaquette of the one-bit orthogonal axes is `σₓσᵧσₓσᵧ = −I ≠ +I` (`nonabelian_plaquette`; the electron loop `^<v>` folds to `−I`). **That is curvature**, and it is present at every fold. So the `κ = 0` above cannot be read as "space is flat."
>
> Is it an artefact of throwing the fold away? Tested directly: **lift** the lattice by the fold — vertices `(position, fold element)`, edges carrying the twist's Pauli factor, the graph space actually is; the six twists generate a fold group of order 16. On a `4³` chunk (1024 vertices, 384 interior edges) the answer is **`κ = 0` again**.
>
> So the blindness is **structural, not an artefact**. Ollivier–Ricci is a metric-combinatorial quantity: it sees neighbourhood matching and graph distance, and holonomy is invisible to it by construction — which is exactly *why* it was reached for ([`Weak_Force.md`](Weak_Force.md) §5c⁗ excluded holonomy curvatures on independent grounds). Reading "space is flat" off it measures the instrument, not the space. The correct statement is a pair:
>
> | | holonomy curvature (§1a) | transport curvature (§1c) |
> |---|---|---|
> | **space** | **curved** — one bit per fold, plaquette `−I` | flat |
> | **possibility graph** | free — its edges carry no `σ` | **hyperbolic** |
>
> The two notions are **complementary, not competing**: each is blind to precisely the curvature the other measures. That is the substantive content — not a flat/curved verdict on space.

Computed on the half-spin free first-return closure classes, extended to `L = 4, 6, 8, 10, 12` (1, 2, 12, 165, 1964 classes; 1597 connected vertices, 2773 edges) so that three layers are interior rather than boundary. Every positive value sits on the outermost truncation layer — the leaf artefact the tree control exhibits — while **all 162 interior edges are negative without exception.**

**The truncation was tested, not assumed.** At four layers the interior sample is 14 edges; adding the fifth does two things, both diagnostic:

| | 4 layers (`L ≤ 10`) | 5 layers (`L ≤ 12`) |
|---|---|---|
| `L6–L8` interior edges | 14, `κ ∈ [−0.646, −0.125]` | 14, **identical to the last digit** |
| `L8–L10` interior edges | — (boundary) | 148, `κ ∈ [−0.801, −0.112]`, all negative |
| interior total | 14, all negative | **162, all negative** |

The existing values do not move at all — a deeper layer cannot shorten any distance in their transport problems — and the newly interior edges are a ten-times larger sample with the same sign throughout. The positive values simply migrate to the new outermost layer, which is exactly what a leaf artefact does. **Hyperbolicity is not a truncation effect.**

> **Possibility is hyperbolic — under the very notion that cannot see space's curvature.** That is the discrete AdS signature, and it is precisely what QLF's holography says in words ([`Holographic.md`](Holographic.md); [`README.md`](README.md) §holography): *the bulk is the space of unresolved internal nodes of the generator tree, the boundary is the ZFA-closed leaves.* A generator tree is negatively curved; here that is **measured** rather than asserted, with a curvature that is a ratio of counts. **Honest scope:** a finite census (stable under extension, but still finite), one curvature estimator, and a structural reading — not a derivation of AdS/CFT. And per the box above, it is *not* a flat-vs-curved verdict on space: the deformation picture of §2–§6 acts on a substrate that is already holonomy-curved at every fold, and what §1c adds is that the possibility graph carries transport curvature of definite negative sign, intrinsically, before any deformation.

**The sign has a machine-verified structural core** ([`lean/QLF_CensusCurvature.lean`](lean/QLF_CensusCurvature.lean)). The measurement is a finite census, however stable; the Lean module supplies what no truncation can. Proven with **no axiom**: the causal parent relation deletes exactly two twists, so adjacency changes the length by exactly `2`, so the graph is **layered** (`length % 4` flips across every edge) and irreflexive — hence **triangle-free**, because three mutual neighbours would need three lengths pairwise differing by `2` and no three naturals do. Also proven: the parent relation **preserves count balance**, so the census really is a graph *on* ZFA closures. One cited bridge — `jost_liu_triangle_free` (Jost & Liu 2014: triangle-free ⟹ `κ ≤ 0`), named because Mathlib carries no discrete optimal transport — makes **`census_nowhere_positively_curved`** a theorem: the possibility graph is nowhere positively curved **at every length**. Note the trade honestly: the numerical result is *stronger* where it applies (`κ < 0`, strict) but truncation-bounded; the theorem is *weaker* (`κ ≤ 0`) and unbounded in scope. Strict negativity does not follow from triangle-freeness and remains numerical.

**What the sign closes: a wrong route to the Yang–Mills mass gap.** Positive Ollivier curvature buys a *spectral gap* — Ollivier's graph Lichnerowicz bound, `κ ≥ κ₀ > 0` on every edge `⟹ λ₁ ≥ κ₀`. That makes "the gap is the curvature of the possibility graph" a natural-looking alternative to QLF's actual derivation (the gap **is** the `log 2` closure quantum, `gaugeMassGap`, [`QLF_MassGap`](lean/QLF_MassGap.lean)). **The route is closed, twice over.** The hypothesis fails structurally — `census_nowhere_positively_curved` proves `κ ≤ 0` at every length, so the bound yields nothing. And the conclusion fails empirically: the normalized-Laplacian gap of the census collapses geometrically as the census deepens,

| census | component | `λ₁` |
|---|---|---|
| `L ≤ 8` | 14 vertices | `0.3169` |
| `L ≤ 10` | 119 vertices | `0.0810` |
| `L ≤ 12` | 1572 vertices | `0.0192` |

— a factor of `≈ 4` per added layer, heading to zero, which is exactly what a hyperbolic (tree-like) graph does. **The possibility graph has no spectral gap, so it is not where a mass gap can come from.** That leaves QLF's `log 2` derivation not merely intact but preferred, by elimination of the competitor. (It also puts the census emphatically outside the Ramanujan/expander class, so the *graph* Riemann hypothesis of the Ihara zeta fails here too — a fact about this graph, carrying no implication for the classical `ζ` or for [`QLF_Riemann`](lean/QLF_Riemann.lean).)

The notion was found by looking for what the lepton Koide phase would need ([`Weak_Force.md`](Weak_Force.md) §5c⁗). **It does not supply that phase** — there is no positive interior curvature anywhere and no value equal to `2/3` — so the curvature route to `Δ` is closed at all three notions. The notion itself outlived the question that produced it.

## 2. Two deformations: expand and contract

A blanket changes shape by gaining or losing substrate events on its surface. There are exactly two primitives, and they recur at every scale:

- **Expansion** — *more* events inserted between closures. Two like-oriented half-spin closures cannot occupy the same closure state (Pauli exclusion); the substrate separates them, **inserting Planck events** and stretching the local surface. Replication (`*P`) is the same move globally: each new distinction adds events outward.
- **Contraction** — *fewer* events; surface released. Two opposite-oriented closures pair into a singlet whose joint Pauli product `(−I)(−I) = +I` is closed; the events that hosted them are **released back to the vacuum**, drawing the surface in. Entanglement (`P | Q`) is the same move globally: interlocking closures share blankets and contract.

Expansion is the outward, negative-pressure deformation; contraction the inward, positive-pressure one. Which dominates, and along which axis, is the entire content of the three sections that follow.

## 3. Gravity — isotropic, single-sign curvature

Mass is a dense cluster of gauge-folded (`+`/`−`) closures — high logical density, high local event rate. A massive body raises the constructing-delay `Δt = R/f` of its neighbourhood and **lowers** the count of available ZFA closures (`W_ZFA`) around it, so test histories drift toward it: the blanket **contracts inward** ([`Gravity.md`](Gravity.md); [`Gravity_From_Delay.md`](Gravity_From_Delay.md)). In the continuum limit this is the Schwarzschild metric — `g_tt = -(1 - R_s/r)` from the cross-frequency gravitational redshift, `g_rr = (1 - R_s/r)^{-1}` from radial event scaling ([`GR_Schwarzschild.md`](GR_Schwarzschild.md)) — recovering Newton's `F = GMm/r²` and Mercury's 42.99″/century to 0.03% ([`Mercury_Perihelion.md`](Mercury_Perihelion.md)).

Two features distinguish gravity from everything else:

- **It is isotropic.** Mass contracts the blanket equally in all directions; there is no preferred axis.
- **It is single-sign.** Gravity only ever contracts (attracts). There is no "negative mass" deformation — gauge-fold density can only add inward bias.

And because the deficit is carried by a *finite* count of pentamons on a discrete surface, **curvature is bounded by event density**: no point of infinite curvature can form. Singularities are not in the space of admissible blankets ([`Quantum_Gravity.md`](Quantum_Gravity.md), [`UniversalRelativity.md`](UniversalRelativity.md) §4). Gravity is the isotropic, single-sign **limit** of the signed deformation — the case where only contraction, and only the radial direction, is in play.

### 3.1 Worked example — the Moon's orbit as inward inflow

A mass "eats" space at a rate equal to its gravitational acceleration. Earth's surface rate is `g⊕ = 9.80665 m/s² = 32.174 ft/s²`; the Moon's is `g☾ = 1.62 m/s² = 5.32 ft/s²` — Earth's is `9.80665 / 1.62 = 6.05×` the Moon's, the familiar "one-sixth" Moon gravity. But these are *surface* rates. What holds the Moon in orbit is the inflow each body produces **at their separation** `d = 384,400 km = 3.844×10⁸ m`, and the inflow falls off as the inverse square of distance — the blanket's fixed deficit spread over its `4πr²` area (§1). The exact inflow at distance `d` is `GM/d²` (equivalently the surface rate times `(R/d)²`):

- Earth: `GM⊕/d² = 3.986004×10¹⁴ / (3.844×10⁸)² = 2.6976×10⁻³ m/s² = 8.8503×10⁻³ ft/s²`
- Moon: `GM☾/d² = 4.9028×10¹² / (3.844×10⁸)² = 3.3180×10⁻⁵ m/s² = 1.0886×10⁻⁴ ft/s²`

Their **sum, `2.7307×10⁻³ m/s² = 8.9592×10⁻³ ft/s²`, is the relative orbital acceleration** `G(M⊕+M☾)/d²` that keeps the Earth–Moon pair circling their barycentre. The observed value from the 27.32166-day sidereal month, `ω²d` with `ω = 2π/T = 2.6617×10⁻⁶ rad/s`, is `2.7233×10⁻³ m/s² = 8.9349×10⁻³ ft/s²` — agreeing to 0.27% (the residual is mean-vs-osculating distance and eccentricity). Both bodies' "eating" *does* add to the orbit, but it is the inverse-square-projected inflows at the orbital radius that add, not the raw surface rates 32.174 and 5.32. Earth's inflow dominates — this is exactly Newton's 1665 Moon test, `g⊕ / (d/R⊕)² = 9.80665 / 60.34² = 2.6936×10⁻³ m/s²` for the lunar distance of 60.34 Earth radii — and the Moon's inflow contributes the final `3.3180×10⁻⁵ / 2.7307×10⁻³ = 1.22%`. This is the Newtonian content the blanket's `1/r²` deficit-dilution reproduces in the continuum limit.

## 4. Magnetism — differential, two-signed curvature

Magnetism is what happens when the two deformations of §2 are split *by spin orientation along an axis* ([`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §1–§4). Where the vacuum carries a net spin-orientation bias along ẑ:

- a **spin-up** (like-bias) closure meets like-spin exclusion → its substrate **expands** along ẑ;
- a **spin-down** (anti-bias) closure meets singlet annihilation → its substrate **contracts** along ẑ.

The measured **B-field is the directional gradient** of this vacuum spin-bias: expansion along the bias axis, contraction transverse to it. This reads off the standard phenomena directly — Stern–Gerlach (spin-up and spin-down atoms deflect *oppositely* because they roll down expanded vs contracted substrate), the hydrogen hyperfine 21 cm line (parallel/triplet expanded, antiparallel/singlet contracted), and Hund's rule (like-spin shells cost orbital extent). The Pauli-exclusion engine is Lean-anchored: `pauli_exclusion` and `fermi_nonzero_example` ([`lean/PauliExclusion.lean`](lean/PauliExclusion.lean)).

The contrast with gravity is exact and is the heart of this document:

| | direction | sign |
|---|---|---|
| **Gravity** | isotropic (all directions) | single (contraction only) |
| **Magnetism** | anisotropic (along the spin axis) | **two-signed** (up expands, down contracts) |

Gravity uses one deformation in every direction; magnetism uses *both* deformations, split by spin, along one direction. Magnetism is the **differential** form of the same curvature.

## 5. Global curvature is de Sitter

The largest Markov blanket is the **cosmic horizon** (v ≈ 6.7 × 10⁶⁰) — and it carries the same twelve pentamons as the icosahedron. Its global deformation is set by which §2 primitive dominates *the universe as a whole*:

- **de Sitter** (positive Λ, accelerating expansion) is the **replication-dominant** phase: more distinctions are generated outward than can be immediately closed, so the cosmic blanket expands ([`Holographic.md`](Holographic.md), "de Sitter Expansion and Anti-de Sitter Stability").
- **Anti-de Sitter** (negative curvature, stable) is the **entanglement-dominant** phase: interlocking closures share blankets and contract.

Our universe is net-expanding, so its global geometry **is de Sitter**. The cosmological constant is not tuned — it is the residual curvature of the near-uniform vacuum, with the dark-energy fraction *predicted*:

$$\rho_\Lambda = \frac{3\log 2}{8\pi}\,\frac{c^4}{G\,R_H^2}, \qquad \Omega_\Lambda = \log 2 \approx 0.6931,$$

(Planck 2018: 0.685 — a 1.2% match)

with the notorious 10¹²² vacuum catastrophe closed structurally by the `(R_H/L_Planck)²` surface-vs-volume ratio ([`Cosmological_Constant.md`](Cosmological_Constant.md) §3, §5.5; [`VacuumEnergy.md`](VacuumEnergy.md) §5/§6.2; [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)). The event-synthesis tensor `T_μν^(synth)` replaces the bare Λ. de Sitter and AdS are *both* present — "different phases of the same underlying logical dynamics" — exactly as expansion and contraction are both present in magnetism.

## 6. One signed deformation, two scales

Sections 3–5 are the same physics. A blanket expands or it contracts; gravity is the isotropic single-sign limit, and the *signed, differential* case appears at two scales that are structurally the same deformation:

| scale | **expand** | **contract** |
|---|---|---|
| **Magnetism** (local, spin axis, anisotropic) | spin-up / like-spin Pauli exclusion | spin-down / opposite-spin singlet annihilation |
| **Cosmology** (global) | de Sitter / replication `*P` | AdS / entanglement `P \| Q` |
| **Gravity** (isotropic limit) | dark-energy residual | mass / gauge-fold density |

The expand column is one substrate move — closures pushed apart, events inserted (exclusion locally, replication globally). The contract column is its inverse — closures paired and released (annihilation locally, entanglement globally). **Magnetism's up/down differential is the local spin-axis analog of cosmology's de Sitter/AdS differential.** Both are signed deformations of the primordial blanket; gravity is what is left when the sign is fixed and the axis dependence is dropped. The 6+2 split of the twist alphabet (6 spatial axes → 3D; 2 gauge twists → the 1/4 gauge fraction that sets Λ and, via N = 9 = 3², α) is the single substrate that ties magnetism, gravity, and the cosmological constant together.

This answers the question that motivated the document — *does magnetism's up/down relate to de Sitter space?* It does: they are the same expand/contract deformation of the blanket, read at the spin scale and the cosmic scale.

## 7. Framing: one premise, then derivation

Granting the premise at the top, the rest is derivation. Curvature *is* deformation of the discrete blanket; gravity, magnetism, and de Sitter cosmology are its isotropic, differential-local, and differential-global forms. The "warm intuition" that magnetism and cosmology are unrelated is not a constraint to respect — it dissolves once both are seen as signed blanket deformation.

The boundaries that remain are degrees of *specification*, not doubt about the premise:

- **Lean-anchored** — the blanket geometry and its curvature (`primordial_blanket_euler`, `pentamon_count`, `holographic_event_count_blanket_eq`), the magnetic engine (`pauli_exclusion`, `fermi_nonzero_example`), and the cosmological constant (`QLF_CosmologicalConstant.lean`, Ω_Λ = log 2).
- **Entailed by the premise** — that curvature is blanket deformation; that gravity is isotropic/single-sign, magnetism differential/two-signed, and the global geometry de Sitter; that magnetism's up/down and cosmology's dS/AdS are the same signed deformation.
- **Open quantitative / formal targets** — a closed-form magnetic "curvature tensor" matching the continuum field strength term-by-term; and a **formal duality theorem** identifying the local spin-axis expand/contract operator with the global dS/AdS operator (the §6 parallel is asserted structurally; its proof as an exact duality is the natural next Lean target). Open by specification, not because the parallel is in question.

### Predictions and falsifiers

- **Shared quantum.** The magnetic expansion/contraction increment and the cosmological one should both be the per-event `log 2` quantum — the same unit drives the spin-axis and cosmic deformations. A magnetic substrate increment incommensurate with `log 2` would falsify the shared-mechanism claim.
- **No third deformation.** Every curvature phenomenon should reduce to expand, contract, or their isotropic sum. A curvature effect that is neither (a genuinely new substrate deformation) would falsify the two-primitive thesis.
- **de Sitter, not flat.** The global geometry must carry positive residual curvature (Ω_Λ ≈ log 2); a measured Ω_Λ driven to zero (exactly flat, no dark energy) would falsify the replication-dominant reading.

---

## 8. Temporal reading: inflation (past), gravity (present), dark energy (future)

The expand/contract duality of §2 is stated *spatially* (interior contracts → gravity; exterior
expands → dark energy, [`BLACK-HOLES.md §4`](BLACK-HOLES.md)). Read it **temporally** and it
becomes a complete cosmic history. **Every event expands the future and contracts locally** — the
two faces are one per-event quantum, oppositely signed (`event_duality_balanced`,
[`lean/QLF_CosmicInflation.lean`](lean/QLF_CosmicInflation.lean)). What you see then depends on
*where in time* you look:

- **Past (telescopes look backward) → inflation.** Early on, the vacuum energy `V` and event
  frequency `f` were high, so the expansion rate `H ∝ √V` was large and quasi-exponential
  (`higher_energy_faster_expansion`): **inflation**, decaying to the slow Hubble flow.
- **Present, local → gravity.** Here we see the *contraction* face — bound gauge-folds, mass, the
  inward bias of constructing delay.
- **Future / exterior → dark energy.** The residual expansion bias of the low-density vacuum
  (Ω_Λ = log 2).

The unification is already verified: a static event-synthesis field has equation of state
`w = −1` (`zfa_dynamics_drive_acceleration`), so **inflation and dark energy are the *same*
`w = −1` field at two energy scales** — high `V` early, low `V` now
(`inflation_and_dark_energy_same_field`). **Inflation without an inflaton:** the "inflaton" is
QLF's event-synthesis field, not a new field — inflation is just its high-energy limit, the same
field that is dark energy today (the §6 "one signed deformation, two scales", read across
*time* as well as scale).

**Honest scope.** This anchors the duality, the `√V` monotonicity, and the shared-`w=−1`
unification. It does **not** derive the quantitative inflation observables — the number of
e-folds (~60), the spectral index `n_s ≈ 0.965`, the tensor ratio `r`, reheating — nor the
vacuum-frequency evolution law `f(t)`; those remain open (`cosmic_inflation_in_progress`).

### 8a. Every observer's vantage: inflation behind, expansion ahead — *pre-registered 2026-09-29*

§8 reads the history from **our** epoch. The stronger claim is that the reading holds for **every** observer:
*whenever you stand, you see inflation in your past and expansion in your future.* No epoch is the special
one that happens to catch the universe between its inflation and its dark energy. The claim is not free.
In a cosmology with a built-in time scale, it fails for some observers. An observer in the middle of
standard inflation has no inflation behind it.

**The definition (fixed before the proof).** "See" means *measured in the observer's own clock*.
In QLF each closure makes its own time. The vacuum event rate is `f(t) = 1/t` (`ZFAEventDynamics`),
and an observer at epoch `t₀` ticks at its own rate `f(t₀)`. The rate at another epoch `s`, as that
observer measures it, is

$$r(t_0, s) \;=\; \frac{f(s)}{f(t_0)} \;=\; \frac{t_0}{s}.$$

"Inflation" here means **more than one e-fold per own tick** (`r > 1`). "Expansion" means **positive
but less than one** (`0 < r < 1`). This is an observer-relative quantity (a *listening*, not a count).
It is **not** the standard `ä > 0`: `H ∝ 1/t` is a power law, which decelerates in the usual sense.
The `ä > 0` version is a separate, conditional question and is not claimed here.

**Pre-registered statements** (to be proved in `lean/QLF_InflationObserver.lean`, no new axioms):

| | Statement | Meaning |
|---|---|---|
| P1 | `0 < s < t₀ ⟹ r(t₀, s) > 1` | the past inflates, for every observer |
| P2 | `0 < t₀ < s ⟹ 0 < r(t₀, s) < 1` | the future expands and never stops |
| P3 | `r(k·t₀, k·s) = r(t₀, s)` for all `k > 0` | no privileged epoch: every observer sees the identical profile |
| P4 | for the rate law `1/t + c`, P3 holds at `(t₀, s, k) = (1, 2, 2)` **iff `c = 0`** | the falsifier: any constant floor (ΛCDM's constant `Λ`) breaks it |
| P5 | `Ω_Λ(H) = log 2` for every `H > 0` | because `ρ_Λ ∝ H²` (`rhoLambda_prop_Hsq`), every observer measures the same dark-energy fraction |

**What would count as failure.** Any of P1–P5 fails to prove. Or P3 turns out to hold for the constant-floor
law as well. That would make the claim bookkeeping: true of every rate law, and so evidence of nothing
(`CLAUDE.md` rule 4). P4 is there to rule that out. The arithmetic of P1–P3 is short. The physics is in the
premise that the cosmic rate has no built-in scale, and P4 is what shows that premise carries the weight.

**Result (2026-09-29): all five proved**, no new axioms, in
[`lean/QLF_InflationObserver.lean`](lean/QLF_InflationObserver.lean): P1 `past_inflates`, P2
`future_expands`, P3 `no_privileged_epoch`, P4 `floor_breaks_self_similarity`, P5 `omegaLambda_eq_log_two`,
with P1–P3 bundled as `every_observer_inflation_behind_expansion_ahead`. The statements are the ones
frozen above. None were adjusted to fit the proof.

**Amendment after review (2026-09-29, PR #164).** The proofs stand. The pre-registered text above
overstates what they show in four places, corrected here rather than edited in place:

1. **`r` is a ratio of rates**, not "e-folds per own tick". The two agree only if `H = f` exactly.
2. **P1 and P2 are not evidence.** They follow from any falling rate, the floored law `1/t + c`
   included (`floored_past_also_inflates`). "P4 is there to rule that out" is true of P3 only.
3. **P3 does not single out `1/t`.** Every power law `t⁻ⁿ` satisfies it
   (`power_law_no_privileged_epoch`). P3 with P4 shows the rate has *no built-in scale*, not that it is `1/t`.
   The per-event `f = 1/t` is machine-linked (`vacuumRate_is_event_rate`). Using it as the cosmic
   rate as a function of epoch is a premise.
4. **P5 is a named tension, not an open question.** If `ρ_Λ ∝ H²` holds at every epoch, as
   `QLF_DynamicalDarkEnergy` states it, then `Ω_Λ = log 2 ≈ 0.69` at recombination and at BBN. CMB data
   bound a constant early dark-energy fraction to `Ω_early < 0.06` at 95% (Doran & Robbers, *Early dark energy cosmologies*, JCAP 0606:026 (2006)), and
   later data are tighter. At BBN that fraction would raise `H` by `(1 − log 2)^(−1/2) ≈ 1.8`. **Falsifier:**
   either `ρ_Λ ∝ H²` fails before late times, or this reading of QLF's dark energy is ruled out. **The way out is the counted horizon** ([`Cosmological_Constant.md`](Cosmological_Constant.md) §5.7 (PR #165)): with `L = c/H` both readings fail, while the future-event-horizon reading C keeps the `log 2` prefactor, gives `Ω_de ≈ 10⁻⁴` at recombination, and passes the early-epoch test. It gives up P5: `Ω_Λ = log 2` becomes today's value, not every epoch's. **But C is excluded by published full fits:** with CMB + DESI + supernovae, `C = √log 2 ≈ 0.833` sits 5.5–7σ above the fitted value, and event-horizon dark energy is decisively disfavored against ΛCDM (`ln B ≈ −27` to `−30`; Li et al. 2024, arXiv:2411.08639). All three horizon readings fail. What survives is a constant `Λ` with `log 2` as *today's* `Ω_Λ` only. **So P5 is ruled out as physics:** it stays a true theorem about `ρ_Λ ∝ H²`, but the data reject that premise. The
   value `log 2` itself is the input prefactor; P5's content is the `H`-independence.

**Open, and not claimed:** the `ä > 0` version; the observer's own first tick, which has no past inside
its domain (the nested origin, [`BLACK-HOLES.md`](BLACK-HOLES.md) §4a, is an interpretation there, not a
proof); whether `ρ_Λ ∝ H²` survives the data; and the inflation observables of §8.

---

## References

### Internal

- [`Primordial_Markov_Blankets.md`](Primordial_Markov_Blankets.md) — Fuller geodesic-sphere blanket; 12 pentamons as topological curvature; scale invariance; v(R) and the area law
- [`lean/QLF_PrimordialMarkovBlanket.lean`](lean/QLF_PrimordialMarkovBlanket.lean) — `primordial_blanket_euler`, `pentamon_count`, `holographic_event_count_blanket_eq`; binary-icosahedral 2I → E₈ (McKay)
- [`Emergent_Markov_Blankets.md`](Emergent_Markov_Blankets.md), [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) — nested blanket hierarchy across scales
- [`Gravity.md`](Gravity.md), [`Gravity_From_Delay.md`](Gravity_From_Delay.md) — gravity as inward contraction from gauge-fold density; Newton's law from holographic event count
- [`GR_Schwarzschild.md`](GR_Schwarzschild.md), [`Mercury_Perihelion.md`](Mercury_Perihelion.md) — Schwarzschild metric and 42.99″/century as the continuum limit
- [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §1–§4 — like-spin expansion / opposite-spin contraction; B as directional spatial gradient; Stern–Gerlach, hyperfine
- [`lean/PauliExclusion.lean`](lean/PauliExclusion.lean) — `pauli_exclusion`, `fermi_nonzero_example`
- [`Holographic.md`](Holographic.md) — de Sitter (replication/expansion) vs AdS (entanglement/contraction) as phases of one dynamics
- [`Cosmological_Constant.md`](Cosmological_Constant.md) §3, §5.5 — ρ_Λ and Ω_Λ = log 2 from substrate primitives; the 10¹²² closure
- [`VacuumEnergy.md`](VacuumEnergy.md) §5, §6.2, §6.4 — event-synthesis tensor; near-maxent vacuum; spin-orientation substrate of magnetism
- [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean) — Λ and Ω_Λ = log 2 anchors
- [`UniversalRelativity.md`](UniversalRelativity.md) §4, [`Quantum_Gravity.md`](Quantum_Gravity.md), [`AgeOfUniverse.md`](AgeOfUniverse.md) — completed Einstein equations; no singularities; cosmic expansion

### External

- Fuller, R. B. (1975). *Synergetics: Explorations in the Geometry of Thinking.* — geodesic spheres; the 12-pentagon closure of any geodesic triangulation.
- Regge, T. (1961). *General relativity without coordinates.* Nuovo Cimento 19, 558. — discrete (angular-deficit) curvature, contrasted with QLF's topological deficit.
- de Sitter, W. (1917). *On the relativity of inertia.* Proc. KNAW 19, 1217. — the de Sitter solution.
- Maldacena, J. (1998). *The large-N limit of superconformal field theories and supergravity.* Adv. Theor. Math. Phys. 2, 231. — AdS/CFT.
- Maldacena, J. & Susskind, L. (2013). *Cool horizons for entangled black holes.* Fortschr. Phys. 61, 781. — ER = EPR.
- Gerlach, W. & Stern, O. (1922). *Der experimentelle Nachweis der Richtungsquantelung im Magnetfeld.* Z. Phys. 9, 349. — spin-dependent deflection.
- McKay, J. (1980). *Graphs, singularities, and finite groups.* Proc. Symp. Pure Math. 37, 183. — binary icosahedral ↔ E₈.

### See also

- [`TheQuantumBrain.md`](TheQuantumBrain.md) — frequency-isolated Markov blankets in the brain; the same blanket machinery applied to cognition
- [`GodCreatedTheIntegers.md`](GodCreatedTheIntegers.md) — Einstein's singularity-free, deterministic vision; ER = EPR as shared ZFA closure
- [`README.md`](README.md) — the convergence of independent programs on an informational, computable, closure-bounded reality
