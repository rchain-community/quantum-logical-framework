# Quantum Logical Framework (QLF)

**The universe is logical.**  
**Spacetime is synthesized.**  
**Physical reality is the subset of possibility that achieves Zero Free Action.**

## What this is

The **Quantum Logical Framework (QLF)** is a new, constructive **foundation for mathematics and physics, built from the bottom up** out of a single finite distinction — one bit, one Zero-Free-Action (ZFA) event.

- **It starts from a fact about measurement, not a QLF claim.** No measurement has ever produced a real number — every outcome is a count plus a rational interval (frequency metrology is integer cycle-counting; the 2019 SI redefinition makes it explicit top to bottom). So QLF asks the question that then asks itself: why is physics *written* in a continuum whose objects can never appear in any lab? — and builds the finite, computable substrate that answers it. ([Completeness_Evidence.md](Completeness_Evidence.md) §2a)
- **Its logic is quantum logic — machine-verified, not analogized.** Propositions are phase-string distinctions in an 8-twist alphabet; truth is decided by *measurement*, which is ZFA closure. The **defining** feature of quantum logic — orthomodular but **non-distributive** (the departure from classical Boolean logic) — is now a Lean theorem: the substrate realizes the minimal quantum logic `MO2` (two incompatible x/z-spin closures whose Paulis don't commute), orthocomplemented, orthomodular, and provably not distributive (`QLF_QuantumLogic`, no bridge axiom). QLF argues this is the **correct** logic — *complete where reality is*, with Gödel/Turing incompleteness confined to the non-terminating tail it physically prunes. ([Quantum_Logic_Foundations.md](Quantum_Logic_Foundations.md))
- **Physics is derived, not assumed — and machine-checkable.** From that one primitive follow spacetime, measurement, entanglement, the Standard-Model gauge groups, gravity, spin, and the fundamental constants — each **verified in Lean 4** across **more than a hundred modules with zero `sorry` blocks**, the combinatorial core within **RCA₀** (no Axiom of Choice, no continuity). *Don't trust it — clone the repo and run `lake build`; the proofs check or they don't.* The same logic derives `α = 1/137`, `m_p/m_e = 6π⁵`, and `Ω_Λ = log 2` from the substrate with zero free parameters (table below), and reformulates the Millennium problems as verified discrete cores plus one honestly-named continuum boundary — a *reformulation*, not a claim to have settled the Clay statements. ([Millennium.md](Millennium.md))
- **It publishes its kill conditions.** QLF is *sufficient* for the audited observations and overdetermines the constants parameter-free; its *exclusivity* — that **only** ZFA is happening — is a **published conjecture with named defeaters**: an axion detection, a confirmed α drift, an exhaustive 0νββ null, a QRNG deviation, and three more — experiments that would end it. Bell/KS/PBR already exclude *added* local, non-contextual, and ψ-epistemic ingredients; among exact reconstructions of quantum logic (Bohm, Everett, ZFA) no experiment separates them, and ZFA is distinguished by parsimony and constants overdetermination. So an item marked "open" is a *value awaiting calculation*; the *exclusivity* claim is the one held open to falsification — and its defeaters are named. ([Completeness_Evidence.md](Completeness_Evidence.md) §4c, [Positioning.md](Positioning.md))

In one line: **the universe is logical, its logic is constructive and sufficient-for-physics, we build it from the bottom up and check it in Lean — and we publish what would refute it.**

> **New to QLF? Read [Introducing_QLF.md →](Introducing_QLF.md)** — a short, link-rich introduction for the general reader (the one idea, the headline results, the frontiers, honest scope). Then **start the deep dive: the [flow chart →](FlowChart.md)** — the whole framework as a linked index (one substrate → five families → twelve domains → the individual results). For the rendered, clickable diagrams + a printable PDF, open the live page on GitHub Pages: [`FlowChart.html`](https://rchain-community.github.io/quantum-logical-framework/FlowChart.html).

> **Prefer to see it move?** Open the [**Spectral Spacetime Constructor**](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html) ([source](spacetime_constructor.html), [notes](Spacetime_Constructor.md)) — an interactive 3-D field where space is node position, time is clock rate, and both are frequency shown as colour (redshift = time dilation, one phenomenon). Heat the vacuum from the **CMB (2.7 K)** to the **Planck temperature** and, driven by **ZFA and the closure census alone** (no forces, no dice, nothing scripted), watch QLF's *logical bang* unfold: **tiny Planck-mass black holes** form and **Hawking-cascade into hadrons** ([▶ see the cascade](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#t=0.95) — opens near the Planck temperature, black holes forming and evaporating into hadrons), which cool and **recombine into atoms** — primordial black holes and the hadron epoch reproduced *from the substrate*, not put in. Every dot is a closure; click any of them to identify it by frequency and spin. Atoms then do **chemistry** by one valence rule — water, CO₂, graphite, rust all self-assemble ([`Chemistry.md`](Chemistry.md), each with a live "(▶ see)" link).

---

## 🚀 Major substrate-derivation discoveries

QLF spans **more than a hundred machine-verified Lean modules** (zero `sorry`) covering the Standard Model, gravity/GR, cosmology, condensed matter, nuclear fusion, and the Millennium problems — see the [module table](#the-lean-formalization) and [`Open_Problems.md`](Open_Problems.md) for the full map. The **ten headline quantitative wins** from ZFA + h alone:

| # | Result | Match | Empirical input | Lean module |
|---|---|---|---|---|
| 1 | **α = 1/137** from substrate combinatorics (8-twist alphabet × 3D directional tensor) — the **leading value** at the IR / 3-D-rendered scale; bounds Lean-verified `137 < α⁻¹ < 137.048` (`QLF_AlphaBound`), residual to 137.036 open. And the leading value is a **machine-checked cross-sector overdetermination joint** (`QLF_AlphaRigidity`, zero axioms): dimension (`d=3`) × bare-coupling (`128=2⁷`) × elementarity (`137` prime) meet with zero slack — *could have failed* (a 4-D rendering forces 144), so it cannot chase a moving measurement — [**Alpha.md**](Alpha.md) §6a | 0.026% | none | [`QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean), [`QLF_AlphaRigidity.lean`](lean/QLF_AlphaRigidity.lean) |
| 2 | **`m_p/m_e = 6π⁵`** Lenz factor (3-quark Borromean closure × 5-angle integration) | 0.002% | none | [`QLF_LenzMassRatio.lean`](lean/QLF_LenzMassRatio.lean) |
| 3 | **γ = 0.5772** Euler-Mascheroni (harmonic-excess identity, bridges to Riemann ζ) | 0.017% | none | [`QLF_EulerMascheroni.lean`](lean/QLF_EulerMascheroni.lean) |
| 4 | **Dirac correction** on hydrogen (Sommerfeld formula composed from substrate) | 0.05% | m_e | [`QLF_DiracCorrection.lean`](lean/QLF_DiracCorrection.lean) |
| 5 | **Lamb shift** α⁵ from substrate Bethe-log range R_n/R_e | ~2.5% (1S–2S) | m_e + k(n,0) | [`QLF_LambShift.lean`](lean/QLF_LambShift.lean) |
| 6 | **g−2 = α/(2π)** Schwinger anomaly, dressed-vertex × loop-phase decomposition | 0.18% | **ZERO** | [`QLF_GMinusTwo.lean`](lean/QLF_GMinusTwo.lean) |
| 7 | **Newton's `F = GMm/r²`** from holographic event count + per-event log 2 | structural | — | [`QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) |
| 8 | **Mercury perihelion 42.99″/century** (Einstein 1915, first GR observational success) | **0.03%** | M_Sun, a, e, T | [`QLF_MercuryPerihelion.lean`](lean/QLF_MercuryPerihelion.lean) |
| 9 | **Ω_Λ = log 2** dark-energy fraction (gauge-axis fraction 2/8 + per-event log 2); **closes 10¹²² vacuum catastrophe** | **1.2%** (Ω_Λ); 8.8% (Λ) | H_0 | [`QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean) |
| 10 | **Primordial Markov blankets** = icosahedral discrete geodesic spheres (Fuller V/E/F + 12 pentamons + McKay → E₈) | exact (combinatorial) | none | [`QLF_PrimordialMarkovBlanket.lean`](lean/QLF_PrimordialMarkovBlanket.lean) |

**Six of these have ZERO empirical input** (#1, #2, #3, #6, #10 are zero; #4 is just m_e). **g−2** at #6 and **Ω_Λ = log 2** at #9 are the headline zero-empirical-input wins — the electron anomalous magnetic moment and the dark-energy fraction both substrate-derived to better than 1.2%. (The `H_0` listed for #9 is the **single residual calibration** of the cosmological sector — and it is the *same* input behind the **age of the universe**, which is **not** empirical but a derived **count of Planck ticks** `t₀ = N·τ_Planck`: `ℏ` fixes the tick, the substrate fixes the count `N` — so "deriving `H_0`" *is* "deriving `N`." See [`UniversalRelativity.md`](UniversalRelativity.md) §5.)

### One discrete census, four continuum universals

The closure census is a **closed `±1` random walk** ([`QLF_CensusBrownian`](lean/QLF_CensusBrownian.lean): a ZFA-balanced string of length `2n` is a walk that returns to origin, count `C(2n,n)`). Four of the most ubiquitous scaling laws in nature are each *one reading* of that single object — no fitting, no free parameter:

<p align="center"><img src="diagrams/census_four_universals.svg" alt="One discrete census — four continuum universals: π, Kolmogorov −5/3, 1/f pink noise, Zipf's law" width="680"></p>

| Universal | Reading of the census | Anchor |
|---|---|---|
| **π** | `1/(n · returnDensity) → π` (Wallis) | [`QLF_PhysicalPi`](lean/QLF_PhysicalPi.lean) |
| **Kolmogorov `−5/3`** | constant `log 2` flux per octave forces `E(k) ∝ k^{−5/3}` | [`QLF_Kolmogorov`](lean/QLF_Kolmogorov.lean) |
| **`1/f` pink noise** | the `p=2` return density is the log-uniform (`1/τ`) relaxation measure | [`Turbulence.md`](Turbulence.md) §4 |
| **Zipf's law** | rank the closure *types* by census frequency → `f(r) ∝ 1/r`, exponent `1.00`, **`p`-independent** | [`Turbulence.md`](Turbulence.md) §7 |

All four are computed exactly (no Monte-Carlo) in [`brownian_closures.py`](brownian_closures.py). **Zipf is discrete-native** — a rank-frequency law over integer ranks with no clean continuum form, yet it falls straight out of the count: native evidence that the discrete substrate is fundamental and the continuum is its (here, lossy) rendering ([`TheContinuum.md`](TheContinuum.md)).

**Beyond the headline ten**, the program reaches across the whole of physics, each result honestly scoped (a verified core + an explicitly-named open piece):
- **Standard Model structure** — spin demystified as the twists (720°/SU(2)→SO(3), `QLF_Spin`); the Majorana neutrino → 0νββ (`QLF_Majorana`); **three generations = the 3 axes** + the Koide relation (`QLF_Generations`, `QLF_Koide`); the Weinberg angle `sin²θ_W=3/8` at unification (`QLF_WeinbergAngle`); CKM/PMNS counting + Kobayashi–Maskawa (`QLF_FlavorMixing`); the strong `SU(3)` and the QCD `b₀=7` from `N_c=3, n_f=6` (`QLF_StrongAlgebra`, `QLF_BetaFunction`); **strong CP `θ̄=0` with no axion** (`QLF_StrongCP`); the pion ratio and hadron quantum black holes (`QLF_PionMassRatio`, `QLF_QuantumBlackHole`); and **information itself is the ½-spin closure** — the two-valued spinor carries one bit (`log 2`), a single-valued vector zero, the `2π` double-valuedness reproven from the rotation matrices (`QLF_SpinorInformation`; *it from bit*, after Cartan 1913).
- **Gravity & cosmology** — the **Einstein field equations as the substrate's equation of state** (Jacobson; `8πG=2π/η`, `Λ=log 2`), tied to **Hitoshi Kitada's local time** — every horizon is a Markov-blanket clock (`QLF_EinsteinEquations`, `QLF_LocalClock`); the **curvature side from the causal order** (Sorkin/Benincasa–Dowker on the closure graph — number↔volume, BD layers, dimension from combining histories; `QLF_ReachableEvent`, `QLF_CausalInterval`, `QLF_CausalDimension`); Unruh/Hawking/de Sitter as one relation (`QLF_HorizonTemperature`); **dark matter** as denser logic — the closure-balance Radial Acceleration Relation, **blind-tested parameter-free on 147 SPARC galaxies** at the observational floor (`a₀=cH₀/2π` derived, = best-fit MOND, vs NFW's 294 fit params; `QLF_DarkMatter`, `SPARC.md`); **inflation = high-scale dark energy, no inflaton** (`QLF_CosmicInflation`); baryogenesis (Sakharov met, `QLF_Baryogenesis`); BBN's quarter-helium universe (`QLF_Nucleosynthesis`); gravitational-wave speed/spin (`QLF_GravitationalWaves`).
- **Force unification** — the three gauge forces are **one substrate gauge interaction**: EM = the *abelian* gauge sector (the photon), weak & strong = *non-abelian* projections of the same three axes, seen at different logical densities; electroweak breaking = the density threshold (`QLF_GaugeUnification`, `QLF_WeinbergAngle`, [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) §3a). And **gravity is the fourth force as the *geometry* of the same closures** — not a gauge force — joined to the gauge sector at **mass = constructing delay** (the equivalence principle from the substrate; §3b).
- **Nuclear fusion & the weak force** — fusion is two Markov blankets joining; two *identical* proton blankets are Pauli-insulated, so the pp-chain's first join needs a weak β⁺ step — the proton/neutron "sex" (`QLF_Fusion`); **muon-catalyzed fusion = legitimate cold fusion**, reproduced in agreement with the Standard Model, with catalysis touching the rate but never the β⁺ necessity (`QLF_MuonCatalysis`).
- **Condensed matter** — the quantum-Hall `R_K=Z₀/2α` from the substrate α, Cooper pairs as bosons (`QLF_CondensedMatter`) ([▶ see them condense](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=electron%20%40%20-1%2C0%2C0%0Aelectron%20%40%201%2C0%2C0%0Aelectron%20%40%200%2C1%2C0%0Aelectron%20%40%200%2C-1%2C0&t=0.06) — four electrons cooled below the condensation threshold pair into bosons; light boson atoms (He) likewise Bose-condense into a superfluid ([▶ superfluid He](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=lattice%20sc%203%203%20He%20%40%200%2C0%2C0&t=0.06)), and anyon braiding statistics (`QLF_Anyons`).
- **The absolute mass spectrum** — every mass = one proton scale × verified ratios, that scale **exponentially generated by dimensional transmutation** with the substrate-fixed `b₀=7` (`QLF_MassSpectrum`). `QLF_AlphaS` then closes `α_s = 1/b₀²`, collapsing the entire `~10¹⁹` Planck/proton hierarchy to the **single integer 7**: `ln(M_P/m_p) = 2π·b₀ = 14π` to **0.07%** on the log, leaving only the ~3% SI calibration open.
- **Millennium problems** — each *reformulated* (not proved) as a verified discrete core + one explicit bridge axiom; for the finitary problems (Hodge, BSD, P vs NP) that bridge is of full conjecture strength, so these are substrate **reformulations**, not proofs (Riemann, Yang–Mills, BSD, Hodge, P vs NP, Navier–Stokes; see [`Millennium.md`](Millennium.md)).
- **Time, reversibility & the arrow** — time-reversal **is** the Hermitian conjugate, and it is an *involution* (reversible **laws**), while the forward ZFA closure is *many-to-one* (irreversible **process**) — so the arrow of time is the non-injectivity of closure, not a separate postulate or a fine-tuned past (`QLF_Reversibility`, [`Reversibility.md`](Reversibility.md)); the `H↔H†` fixed points are the same critical line behind Riemann/BSD/Hodge. **Energy conservation is emergent-local the same way** — each event *creates* energy, lending half to the future (= dark energy), so a TOE that axiomatizes reversibility or global energy conservation mistakes the present-local closure balance for the whole ([`Conservation.md`](Conservation.md) §2b).

**One single 3-dimensional substrate signature** unifies α (via N=9=3² directional tensor), nuclear magic-number ℓ=3 threshold, Newton's 1/r² law, and the cosmological constant Λ (via gauge-axis fraction 2/8) — four independent counterfactual-distinguishable predictions of the 8-twist 6+2 alphabet split.

**Primordial Markov blankets**: every Markov blanket in QLF is a Fuller frequency-`v` geodesic sphere of ZFA closures with icosahedral symmetry. The holographic event count `4π R²/L_Planck²` used in #7 (Newton), #8 (Mercury), #9 (Λ) IS the face count `F_v = 20v²` of this discrete blanket at frequency `v(R) = √(π/5)·R/L_Planck`. **McKay correspondence** then sends the binary icosahedral closure group `2I ⊂ SU(2)` to **E₈** — the largest exceptional Lie group is structurally encoded in the substrate via the primordial-blanket symmetry. Same primitive at every scale, from the v=1 icosahedron up to the v ≈ 10⁶⁰ cosmic Markov blanket.

**The prime ladder, atomic structure, and no free duplication**: the icosahedral blanket geometry extends into an account of matter. *Orthogonality is one bit* — the coarse resolution of the rendered 3-D perspective — and the **prime arrangements (2, 3, 5, 7, 11, 13)** are the substrate's irreducible structure ([`Geometry_Of_Space.md`](Geometry_Of_Space.md) §3c): 2 the bit, 3 the axes/proton, **5 & 13** the icosahedral pair (fold symmetry / `1+12` centered cluster), **7 & 11** the QCD-coupling pair (net `b₀` / gluon antiscreening). This reaches into **atomic structure** ([`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md)): the `s, p, d` shells (orbital dims `1, 3, 5`) are the *unsplit* irreps of the icosahedral group `A₅`, with `f` (dim 7) the first to break — exactly the `ℓ≤2 / ℓ≥3` magic-number boundary. And the substrate **forbids free duplication** ([`Banach_Tarski_QLF.md`](Banach_Tarski_QLF.md)): a conserved ZFA charge + a finite, amenable closure fold mean there is no Banach–Tarski free copy, so real duplication — no-cloning, the no-diproton, cell mitosis — must *pay* in information and energy. The "impossible mathematics" is precisely the continuum + Axiom of Choice the substrate excludes (consistency ≠ realizability).

Reading order:
- Start with [**Active_Inference_Mathematics.md**](Active_Inference_Mathematics.md) for the meta-framing.
- See [**Magnetism_Spatial_Dynamics.md §6**](Magnetism_Spatial_Dynamics.md) for the α derivation that anchors the substrate program.
- See [**Gravity_From_Delay.md**](Gravity_From_Delay.md), [**Einstein_Equations.md**](Einstein_Equations.md) (the field equations as the substrate's equation of state, Jacobson), and [**Mercury_Perihelion.md**](Mercury_Perihelion.md) for the gravity/GR program.
- See [**Experimental_Consistency.md §1.1**](Experimental_Consistency.md) for the full quick-reference scoreboard.

---

At its core is a simple claim, now formally proved:

> **Only histories that achieve Zero Free Action (ZFA) persist.  
> Every terminating computation IS a ZFA string — and ZFA-balanced strings are exactly physical reality.**

From that starting point, QLF derives spacetime, measurement, entanglement, symmetry, gravity, Pauli exclusion, and the Riemann zeta function's critical line — all from finite local logical distinction.

The deepest result is `qlf_universality`: the ZFA filter is not a restriction on what can be computed. It is Church-Turing complete. The filter is a selection principle — it picks physical reality out of the full ruliadic computational universe (Wheeler 1990, Wolfram 2020). The variational physics expression of this principle is S = ∫ℒ dΩ with ℒ = 0 — a null Lagrangian that is the condition of origin, not a cutting rule. See [**Lagrangian_Formulation.md**](Lagrangian_Formulation.md) for the full treatment with machine-verified Lean theorem anchors.

---

## What QLF unifies

QLF is not just an interpretation of quantum mechanics. It is a broader attempt to build a unified framework in which:

- **logical distinction is fundamental** — following Wheeler's "it from bit" (1990) and Zuse's digital physics (1969): the universe is computation, not a manifold
- **spacetime is synthesized event by event** — following Causal Set Theory (Bombelli, Lee, Meyer, Sorkin 1987) and Regge calculus: no background geometry is assumed
- **symmetry is enforced by Zero Free Action** — the ZFA filter (`full_zeno_prune`) is the machine-verified selection principle, proved in RCA₀ with no non-constructive existence
- **measurement is closure, not mystery** — closure under ZFA is the physical event; no separate collapse postulate is needed (compare Zurek decoherence 2003, Everett 1957)
- **stationary action — physics' oldest theory of everything — completed, unifying QM and GR** — from Maupertuis and Planck to Hilbert's 1915 unified-field paper, `δS = 0` has been touted as *the* law of nature, but never explained, and Hilbert's continuum version inherits every continuum singularity (the continuum has produced physical fantasy again and again, most dramatically Banach–Tarski: one solid ball cut into five pieces and reassembled into two — [`TheContinuum.md`](TheContinuum.md)). In QLF it is a theorem: the realized history is the most-ways one, and ZFA's conjugate pairing puts that mode at balance. The **unsigned** count gives classical stationarity, the variational principle behind Einstein's equations (`QLF_StationaryAction`). The **signed** count gives Feynman's stationary phase, the quantum sum over histories (`QLF_StationaryPhase`). Both are machine-verified with no axioms, from one census. Matching the classical half to Hilbert's specific `∫R` functional (via Benincasa–Dowker) is the one open step — [`Stationary_Action.md`](Stationary_Action.md)
- **gravity is emergent, not primitive** — following Jacobson (1995), Verlinde (2011), Padmanabhan: gravity is a thermodynamic consequence of information geometry, derived rather than postulated
- **formal infinities are replaced by constructive finite generation** — following Kronecker, Brouwer intuitionism, and Harvey Friedman's Reverse Mathematics: RCA₀ is the logical floor; everything else is stratified above it

The repository combines:

- **conceptual essays** grounding QLF in the external literature
- **Python experiments and demonstrations** that numerically confirm the Lean theorems
- **Lean 4 machine-verified formalization** of all key structural claims — zero `sorry` blocks
- **physical theory extensions** (strings, M-theory, Loop Quantum Gravity, supersymmetry, holographic QEC, QuantumOS) built on the proved core

---

## Relation to the major Theory-of-Everything candidates

QLF does not compete with the leading quantum-gravity programs — it **grounds the one deep structural
relation each was built around**, as a theorem about half-spin ZFA closures. The recurring move: the
"new fundamental object" each program posits (a string, a spin-network node, a superpartner) is a
*feature of the substrate's closures*, not a new primitive — so QLF reproduces the program's structural
wins from one rule, and explains why its conjectured extra spectrum has not been found.

| Candidate | QLF's grounding (one line) | Companion |
|---|---|---|
| **String / M-theory** | A string is a gauge-fold tower; its level-`n` mode degeneracy is the central binomial `C(2n,n)` — the *same closure census* as Born statistics, P-vs-NP, and π; extra dimensions are twists, the landscape is ZFA-closure sectors (with ZFA the selection rule string theory lacks), and S/T-duality is a ZFA-preserving involution. | [`StringTheory.md`](StringTheory.md), [`lean/StringTheoryQLF.lean`](lean/StringTheoryQLF.lean), [`lean/MTheoryQLF.lean`](lean/MTheoryQLF.lean) |
| **Loop Quantum Gravity** | The substrate *is* a spin network of half-spin (j=½) ZFA closures; the LQG black-hole entropy count (dominant j=½ punctures, each `log 2`) is QLF's holographic entropy `S=4πR²log2`, so the Barbero–Immirzi parameter is fixed by construction; background independence is the synthesized-spacetime ontology. | [`LQG_QLF.md`](LQG_QLF.md), [`lean/QLF_LoopQuantumGravity.lean`](lean/QLF_LoopQuantumGravity.lean) |
| **Supersymmetry** | The supercharge `Q` is the half-spin shift (boson↔fermion = even↔odd closure parity); `{Q,Q†}=2P` is two half-spins closing one spacetime event (the half-spin is the *square root of the event*) — realized **without a doubled spectrum**, so QLF predicts the LHC superpartner null result. | [`SUSY_QLF.md`](SUSY_QLF.md), [`lean/QLF_Supersymmetry.lean`](lean/QLF_Supersymmetry.lean) |
| **Causal Set Theory** | Spacetime is a discrete partial order of causal events — QLF's reachability causal set (`reachable A B := A <+: B`), the pre-temporal driver that the continuum light cone renders. | [`SpaceTime.md`](SpaceTime.md), [`lean/QLF_ReachableEvent.lean`](lean/QLF_ReachableEvent.lean) |

The four forces are grounded the same way: the gauge *force* is the holonomy of the closure connection (abelian-flat photon vs curved non-abelian `W`/gluon), confinement is the singlet-closure obstruction, mass is the gauge-fold delay (the constructive Higgs), and gravity is the *geometry* of the closures — joined at **mass = constructing delay** ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md), [`Forces_From_Alpha.md`](Forces_From_Alpha.md): the couplings root in α, the scale in one mass).

---

## Why This Repo Exists

Standard physics is extraordinarily successful, but its foundations remain unsettled:

| Problem | QLF's specific response |
|---|---|
| The measurement problem | ZFA closure IS the measurement event — no separate collapse, and the closure verdict is **observer-independent**: whether a history closes and the phase it carries are the same in every observer's frame, proven (`QLF_MultiObserver`, `observers_agree`, no axioms). What is relative is the *rendering* (which projection, at what scale); the closure is not |
| The role of the observer | `qlf_universality` grounds the observer: every terminating computation (including observation) is a ZFA string |
| The status of spacetime | Synthesized from ZFA events ([`ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean)) — spacetime is the output, not the input |
| Quantum gravity | Emergent from ZFA event rate and gauge-fold depth — no separate quantization procedure needed |
| Information and physics | ZFA is a Bekenstein-style information bound, machine-verified to be the selection principle for physical reality |
| The limits of classical formalism | The QLF core operates in RCA₀ — below ZFC, below Choice, below the Busy Beaver horizon — so the limits of classical formalism are provably outside the physical universe |

QLF approaches these problems from the bottom up. Instead of starting with continuum fields, collapse postulates, or open-ended formal infinities, it starts with **finite logical possibilities** and asks which histories can actually close.

That makes QLF both a physical proposal and a foundational proposal about mathematics, computation, and explanation — and uniquely, one with machine-verified formal proofs at its core.

---

## Start Here

### 0. Foundations — what kind of mathematics is this?

QLF is the mathematics that has **active inference built into its foundation**. Mathematical objects are admissible trajectories of a free-energy-minimizing agent (a Markov blanket); the single rule is per-event ΔF = −log 2 saturation by half-spin ZFA closure. Not classical mathematics (ZFC), not standard constructive mathematics (no agent), a third thing.

- [**Quantum_Logic_Foundations.md**](Quantum_Logic_Foundations.md) — the positive thesis: quantum logic (propositions = phase-string distinctions, truth = ZFA closure = measurement, algebra = Hermitian) is the **correct** foundation of mathematics, built bottom-up from one finite distinction; the universe's logic is *not* incomplete because incompleteness is exactly the non-physical tail `full_zeno_prune` removes. Positive companion to the continuum/choice critique
- [**Continuum_Choice_Fallacy.md**](Continuum_Choice_Fallacy.md) — the negative thesis: the unrestricted continuum + Axiom of Choice are mathematics' ultraviolet catastrophe (Gödel/Turing/Busy Beaver its shadows); the organizing frame for the Millennium-prize program
- [**Active_Inference_Mathematics.md**](Active_Inference_Mathematics.md) — meta-doc framing the QLF program as active-inference mathematics: primitives, single rule, classical/constructive/active-inference comparison table, honest derived/partial/open scoreboard. Names the system as a candidate TOE and ZFC-replacement for the part of mathematics that is not mathematical fantasy (with the Gödel + Busy Beaver scope marker)
- [**Category_Theory_QLF.md**](Category_Theory_QLF.md) — the category-theoretic structure collected: the causal-set base category, ZFA as an equalizer, the capacity-horizon **bifibration** (whose free prime-factorisation *forces* self-similarity and closes the log-periodic channel — the reason the α-residual weight `w = 1/2` is structural), the Tannakian/anabelian layer, RhoQuCalc as a dagger SMC, `MO2` as the internal logic. A description, not an axiom (method rule 4)
- [**Hierarchical_Control.md**](Hierarchical_Control.md) — the bottom-up/top-down architecture; §3 derives Friston's free energy principle from ZFA
- [**MRE.md**](MRE.md) — the per-event log 2 quantum that is the math's selection principle

### 1. Big-picture orientation
- [**Philosophy.md**](Philosophy.md) — the possibilist foundation of QLF, Zero Free Action, local time synthesis, active inference, holography, the critique of ZFC-style infinity, and (§9) dialectical closure (Aufhebung = cancel/preserve/lift)
- [**Related_Frameworks.md**](Related_Frameworks.md) — where ZFA sits among the neighbors: Part I the selection-principle rivals to differentiate from (Friston FEP, Fredkin/'t Hooft/Wolfram, constructor theory, …), Part II the mathematics of information QLF builds *on* (Shannon, Kolmogorov–Chaitin AIT, quantum information, semantic information) — foundation under the measure stack, not a rival to it
- [**Fredkin_QLF.md**](Fredkin_QLF.md) — Fredkin & Toffoli's conservative logic built on the substrate ([`fredkin_qlf.py`](fredkin_qlf.py), [`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean), [live machine](https://rchain-community.github.io/quantum-logical-framework/fredkin_machine.html)): the gate's conservation law **is** ZFA count balance, so a Fredkin gate cannot take a realized history to an unrealized one — it is a relabelling. A ball is one closed plaquette `^<v>` (168 close at length 4); helium works as a billiard ball *because* valence 0 means no shared closure, hence no bond. Verified: conservativity, involutivity, a Fredkin-only full adder (19 gates, 29 ancillas). **An instantaneous zero-free-action closure is free** — the `−log 2` receipts *many-to-one* closure, and a permutation has none, so Landauer and Bennett are recovered rather than assumed
- [**Information_Physics.md**](Information_Physics.md) — the proof-backed synthesis of *all* the notions of information (Shannon, algorithmic, Fisher, von Neumann/quantum, Bekenstein/Landauer, semantic) on one substrate: information = realized distinction = closure receipt, with the **½-spin closure as its atom** (it from bit), each notion tagged inherited / derived / rendering with its machine-checked anchor
- [**Creation.md**](Creation.md) — the QLF ontology of creation: *nothing comes from nothing* (ZFA enforces it, ℒ = 0 as the condition of origin); everything possible exists *a priori*; a closure is a synthesis of matter and antimatter (the proton = the right/left-handed synthesis, "an abstraction of what adds to nothing which has become actual"); time, space, and energy emerge per event; creation fills every niche just because it is possible — it knows a priori
- [**Evolution.md**](Evolution.md) — biological evolution as ZFA generate-and-select (census-and-closure on genotype space) [structural reading]: genomics has been converging on structured, non-uniform variation (the biological image of the firebreak); the *generate* step is quantum → ZFA (proton tunnelling in DNA, Löwdin / Slocombe–Al-Khalili), so quantum-logical causality is the substrate evolution runs on; anti-teleology by construction (closure is a filter, not a goal — directed mutation refuted and never needed). §3 answers *how a possible niche can stay unfilled* — the three tiers (generated / closing / reached) and five constraints that make the possibility-vs-realization gap non-vacuous. Qualifies [`Creation.md`](Creation.md)'s "creation fills every niche": true in the timeless possibility register, constrained by reachability in any actual history
- [**TheQuantumBrain.md**](TheQuantumBrain.md) — the quantum brain in QLF: frequency-isolated, error-corrected, active-inference coherence as the mechanism of savant cognition; numbers/primes/pitch/calendar as resonant access to the pre-existing logical landscape, not computation
- [**GodCreatedTheIntegers.md**](GodCreatedTheIntegers.md) — a broad framing of QLF in relation to Kronecker, Leibniz, Newton, Einstein, Mach, Noether, Faraday, Wheeler, Shannon, Feynman, Bohm, Schrödinger, Bell, Planck, Gödel, Turing, Penrose, Mead, Cramer, Everett, Zuse, Wolfram, ’t Hooft, Hofstadter, Hawking, and Susskind
- [**SEX.md**](SEX.md) — higher-order closure through complementary specialists: the modelled proton♂/neutron♀ pairing ([`proton_neutron_demo.py`](proton_neutron_demo.py)) — `pn` binds where `pp`/`nn` are Pauli-blocked, and the bond *stabilizes* the otherwise-decaying neutron — scaling to the collective-intelligence factor and quantum-os room best practices

### 2. Core theoretical claims
- [**BraKetRhoQuCalc.md**](BraKetRhoQuCalc.md) — how bra-ket notation maps onto RhoQuCalc: action=ket, lift=bra, parallel=superposition, sequence=composition, ZFA=bra-ket balance (numerical demos in [`braket_rho.py`](braket_rho.py); live evaluation via `/braket` in [quantum-os](https://github.com/rchain-community/quantum-os))
- [**Universality.md**](Universality.md) — the claim that QLF generates finite local logical closures
- [**Riemann-Conjecture-Proof.md**](Riemann-Conjecture-Proof.md) — the current QLF program relating ZFA symmetry, universality, and the critical line
- [**Measurement_Problem.md**](Measurement_Problem.md) — QLF treatment of measurement and observer-dependent closure
- [**UniversalRelativity.md**](UniversalRelativity.md) — emergent relativity and spacetime interpretation inside QLF
- [**Cross_Frequency_Lorentz.md**](Cross_Frequency_Lorentz.md) — Lorentz boost between Markov-blanket frames as a change of basis on internal ZFA event rates; identifies γ = f_A/f_B (the relativistic Doppler factor) and recovers time dilation, length contraction, and interval invariance as direct consequences
- [**TheContinuum.md**](TheContinuum.md) — why the continuum is emergent (not foundational), how QLF dissolves Zeno's paradoxes and the Lorentz invariance trap, and why the Axiom of Choice is replaced by the ZFA filter
- [**ReverseMathematics.md**](ReverseMathematics.md) — QLF as a physical realization of Reverse Mathematics; the RCA₀ core and the WKL₀ axiom boundary
- [**Lagrangian_Formulation.md**](Lagrangian_Formulation.md) — variational formulation of QLF: ℒ=0 as condition of origin, Zeno stationarity, Σ₈ symmetry algebra, decoherence impossibility, and QPU core (Φ₀=U+M); all claims anchored in machine-verified Lean theorems

### 3. Physics and experiments
- [**Experimental_Consistency.md**](Experimental_Consistency.md) — numerical and conceptual links between QLF and known physics
- [**Open_Problems.md**](Open_Problems.md) — gap registry: what is closed, what is a principled boundary, and what is genuinely open, with a pointer to each item's owning doc
- [**Mysteries_Of_Physics.md**](Mysteries_Of_Physics.md) — the canonical open questions of physics (quantum foundations, spacetime/gravity, cosmology, the Standard Model, the deep questions) and what QLF says about each: addressed, value-open, principled boundary, predicted-absent (falsifiable nulls), or genuinely open
- [**Beyond_Standard_Model.md**](Beyond_Standard_Model.md) — honest accounting of where QLF goes past the SM: which free parameters it *fixes by construction* (machine-verified), its falsifiable predictions (Majorana / 0νββ and no α(0) drift, both Lean-anchored), and what it leaves open — with a bright derived/predicted/open line
- [**QRNG_Closure_Observatory.md**](QRNG_Closure_Observatory.md) — a disciplined, falsifiable protocol using ZFA closure as a predeclared sieve (with an analytic null) over quantum-RNG entropy; rigorously separates the testable core from esoteric overclaims
- [**Weak_Force.md**](Weak_Force.md) — the weak sector consolidated: W/Z as gauge-fold closures, the machine-verified weak-isospin SU(2)⊂Σ₈ identification, beta decay, and the τ-decay-vertex blocker (Koide `Q=2/3` derived; `m_τ` predicted to 0.006%)
- [**Forces_From_Three_Axes.md**](Forces_From_Three_Axes.md) — structural conjecture: the Standard-Model gauge group `U(1)×SU(2)×SU(3)` (dim 12 = 1+3+8 = the `N=9` α tensor + the verified weak `su(2)`) as the symmetry of QLF's three spatial axes — "all forces from one gauge-twist mechanism, different projections" (honestly tiered: a dimension alignment, not a derivation)
- [**SpectralGap.md**](SpectralGap.md) — the spectral gap `|count_pos − count_neg|` vanishes iff ZFA-symmetric; unifies Riemann zero spacing (Wigner-Dyson ~ √(πn)), Maxwell Gauss duality (`divB + charge = 0`), and quantum stability (`decoherence_impossibility`)
- [**Maxwell.md**](Maxwell.md) — all four Maxwell equations derived from ZFA, now machine-verified at the conservation level: ∇·B=0 (`no_magnetic_monopoles`), Gauss duality identity `divB=−charge`, and the curl laws Faraday + Ampère-Maxwell as flux-conservation telescoping on the time-indexed event sequence ([`QLF_MaxwellCurl.lean`](lean/QLF_MaxwellCurl.lean): `faraday_integral`, `faraday_closed_cycle`, `ampere_integral`), also confirmed numerically in [`maxwell_qlf.py`](maxwell_qlf.py)
- [**Collective_Electrodynamics.md**](Collective_Electrodynamics.md) — Mead's collective EM in QLF: photon as joint emitter-absorber ZFA handshake (relational, not projectile), fluxoid as ZFA loop, vector potential as unresolved free action, Aharonov-Bohm explained
- [**Electricity.md**](Electricity.md) — current as gauge-fold transport; **resistance as ZFA-closure latency** (`R ∝ 1/W_ZFA`, the same latency as time dilation & gravity); Ohm's law as its linear response; Joule heating = Landauer dissipation; superconductivity = frequency-isolated coherent channel (the quantum-brain isolation); and `R_K = h/e² = Z₀/(2α)` — the quantum of resistance fixed by the substrate-derived `α`. Numerics in [`electricity_demo.py`](electricity_demo.py)
- [**Delayed_Choice_Eraser.md**](Delayed_Choice_Eraser.md) — applies the joint-ZFA reading to the canonical "retrocausality" experiment (Kim 1999, Walborn 2002); the eraser dissolves once the photon is a Hermitian-pair handshake with no preferred temporal direction, not a projectile
- [**Bound_States_QLF.md**](Bound_States_QLF.md) — free leptons are not QLF observables; the natural QLF observables are atomic systems (positronium, muonium, hydrogen) — bound, balanced, joint-ZFA closures. Same structural move as [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) for photons, [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) for quarks: the physical object is the joint closure, not the asymptotic free constituent
- [**Particle_Ladder.md**](Particle_Ladder.md) — one generate-and-close cascade run both directions: **up** from transient vacuum pairs → leptons → the three generations → hadrons → atoms → collective matter, and **down** from black holes by Hawking-unwind back to the vacuum (particle = quantum black hole is the hinge). Assembles the verified rungs (3 generations = 3 axes, Compton = Schwarzschild, decay = Hawking unwind releasing `log 2`, one exponentially-generated mass scale), marks the open ones honestly (the `(R, axis) → mass-ratio` map, the temperature-dependent pair-production rate), and runs live in the constructor (temperature-driven)
- [**Atomic_Structure_QLF.md**](Atomic_Structure_QLF.md) — the detailed companion to [`Atom.md`](Atom.md), combining the substrate origins of atomic structure (**Part I**: shells from Pauli exclusion, the 3-axis orbital ladder, α/scale, the icosahedral s/p/d signature, the twist-fold model of the constituents) with the specific joint-closure topology of each atomic system (**Part II**): positronium (symmetric two-electron-half-loops, mass 2 m_e), hydrogen (electron half-loop + proton internal closure, mass dominated by m_p), muonium (asymmetric electron + antimuon half-loops). Derives the Bohr reduced-mass scaling `E(Mu)/E(Ps) ≈ 2`, `E(H)/E(Mu) ≈ 1`; §7 extends to the heavier-atomic-systems panel (¹H through ²³⁸U) with `R ∝ 1/A` baseline and magic-number BE/A peaks (the ⁵⁶Fe stellar-nucleosynthesis terminator) as vacuum-resonance peaks
- [**Chemistry.md**](Chemistry.md) — chemistry from the one rule: **a bond is a shared closure**, driven by valence saturation, so H₂/H₂O/CO₂/graphite/rust self-assemble with no forces put in by hand (each with a live "▶ see" link into the constructor). Plus the **counting layer**: an atom's valence contributes `(valence−2)/2` to a molecule's closure count, which makes the textbook *degree of unsaturation* the cycle rank — a **double bond and a ring are one phenomenon** — and makes a reaction's change in closure count its change in **molecule count** ([`QLF_Unsaturation`](lean/QLF_Unsaturation.lean)). Its next rung is [**Protein_Folding.md**](Protein_Folding.md), where a **contact is a ZFA closure** and folding is a census of loops that close ([`QLF_Folding`](lean/QLF_Folding.lean))
- [**Quarks.md**](Quarks.md) — the quark account from the nucleon knot ([`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §7): colour = the three axes, with the **machine-proven Borromean three-colour necessity** (`baryon_needs_all_three_axes` — confinement: remove any one colour and `B=0`) and **charge thirds from colour** (`charge_quantum_from_colours` / `down_quark_charge_third`: the `1/3` forced by three colours); confinement as the singlet-closure obstruction (only singlets close). The settled gauge bookkeeping (charge, weak isospin, generations, CKM) vs the open **flavor/Yukawa puzzle**, which the fold picture (`m = 1/R`) reframes as closure *depth* — Koide tier (`Q = 2/3`, `m_τ` to 0.006%), one scale `m_p`, hierarchy `e^{14π}`. Quark + charged-lepton mass tables in `m_p` units; the CKM flavour grid; predictions (dimensional confinement, exotic hadrons molecular). Lean: [`QLF_QuarkStructure`](lean/QLF_QuarkStructure.lean)
- [**Magic_numbers.md**](Magic_numbers.md) — nuclear magic-number sequence `2, 8, 20, 28, 50, 82, 126` derived end-to-end from QLF substrate. Dimensional growth of half-spin closures in d = 2, 3, 4 gives 2, 8, 20 directly; for ℓ_max ≥ 3 the **vacuum itself is the intruder**, coupling in at each frequency to select the `j = ℓ_max + 1/2` orbital at the highest ℓ available. The ℓ = 3 threshold is derived algebraically: `rest > vacuum-selected ⇔ k > 2`, with the "3" coming from the d = 3 of the 3D-SHO degeneracy `(k+1)(k+2)` — exactly the 3 spatial dimensions encoded by the 8-twist alphabet's 6 spatial twists. Counterfactual dimensional shifts (d = 4 → ℓ ≥ 2, d = 2 → no threshold) make the empirical ℓ = 3 a structural prediction of the alphabet's 6+2 split. Companion script: [`magic_numbers_demo.py`](magic_numbers_demo.py)
- [**Per_Qubit_Mass_Quantum.md**](Per_Qubit_Mass_Quantum.md) — **each qubit contributes `ℏω = E_Planck / R_qubit` of rest energy**. Unifying principle that makes the bound-state mass-additivity explicit: `m(Ps) = 2 m_e`, `m(H) = m_e + m_p`, `m(Mu) = m_e + m_μ` as direct sums of constituent-qubit Compton energies. Reproduces every measured mass ratio (`m_p/m_e = 1836.15`, `m_μ/m_e = 206.77`, `m_τ/m_μ = 16.82`) exactly via `m_X/m_Y = R_Y/R_X`. Reformulates the first-principles question: derive `R_e ≈ 2.4 × 10²²` (in Planck units) from QLF closure-multiplicity
- [**Photon_Energy_Bits.md**](Photon_Energy_Bits.md) — photon-side companion: a photon's energy `E = N_bits · ℏω` (bits of joint-closure information × per-bit energy), with mass-equivalence `m_rel = E/c²` but zero rest mass. Photons carry **gauge-free bits**; massive particles carry **gauge-folded qubits**. Same accounting principle: energy = quanta × per-quantum contribution. Pair-production threshold `E_γ = 2 m_e c²` is the bit-to-qubit conversion
- [**Information_Energy_Equivalence.md**](Information_Energy_Equivalence.md) — **`ℏω = 1 bit at frequency ω`** derived from QLF first principles as the conjunction of the per-event `log 2` information quantum (Lean-anchored in [`QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)) and the per-event `ℏω` energy quantum. Formalizes Wheeler's "it from bit" and Chris Fields's information-theoretic physics; recovers Margolus-Levitin (`ℏ` per bit-flip) and Landauer (`kT log 2` per bit erasure) as natural consequences. Unifies the three QLF natural-units quanta: information per event, rest energy per qubit, photon energy per bit
- [**Hydrogen.md**](Hydrogen.md) — hydrogen energy levels E_n = −13.6 eV/n² derived from ZFA (Bohr model): Coulomb from gauge-twist exchange, quantization from ZFA generation depth n; numerically verified to 0.05% in [`hydrogen_qlf.py`](hydrogen_qlf.py). §4.1 reads the Rydberg series as a discrete vacuum-resonance shell spectrum at Markov-blanket depths R_n = R_1 · n², and recovers α to 10⁻¹⁰ via the Bohr-inversion form `α = sqrt(2 Ry / m_e c²)` = `sqrt(2 R_e / R_1)` ([`fine_structure_demo.py`](fine_structure_demo.py))
- [**SpaceTime.md**](SpaceTime.md) — event-synthesized space and time
- [**Gravity.md**](Gravity.md) — emergent gravity in the QLF picture
- [**Curvature.md**](Curvature.md) — gravity (isotropic), magnetism (differential up/down), and de Sitter cosmology as signed expand/contract deformations of the primordial Markov-blanket geodesic sphere; curvature as 12-pentamon topological deficit, metric as continuum limit
- [**ER_EPR_QLF.md**](ER_EPR_QLF.md) — entanglement, geometry, and logical structure
- [**Higgs.md**](Higgs.md) — QLF mass generation via gauge-fold depth; constructive alternative to the Higgs mechanism
- [**HadronicDepth.md**](HadronicDepth.md) — Hadronic Depth Hypothesis: geometric cosmic depth n ≈ 6.7×10⁶⁰ (primordial-blanket v(R_H)) sets cosmic size and age; the proton cube (m_P/m_p)³ ≈ 2.2×10⁵⁷ reproduces it only to ~3–4 orders (large-number coincidence, §2.1)
- [**Proton_Resonance_R_e.md**](Proton_Resonance_R_e.md) — scoping doc decomposing the open `R_e` derivation under the chirality-hiding-resonance reading: `R_e = R_p · 6π⁵`. The Lenz factor `m_p/m_e = 6π⁵` (1951 empirical coincidence, 0.002% agreement) recovered structurally as `|S_3| · π⁵` from `3!` quark permutation symmetry × 5-angle integration over the proton's hidden-chirality configuration space. Cites Kitada's local-time framework (gr-qc/9612043) for the Markov-blanket-depth-as-local-clock reading and the chirality-protection evolutionary-stability argument for why the proton's complexity is selected
- [**VacuumEnergy.md**](VacuumEnergy.md), [**BLACK-HOLES.md**](BLACK-HOLES.md), [**Entropy.md**](Entropy.md) — topic-specific extensions
- [**QuantumOS.md**](QuantumOS.md) — QLF as a capability-secure, formally-verified OS kernel for real quantum hardware (not only simulators; the crystal QPU is the concrete target, §1a): five converging security foundations, intrinsic holographic QEC, a hardware-native **quantum AI** with absolute interpretability, Ruliad/RCA₀ unification — security + error correction + scheduling + GC + inference are all one operation (ZFA enforcement); live demo via `/qucalc` in [quantum-os](https://github.com/rchain-community/quantum-os)
- [**Crystal_QuantumOS.md**](Crystal_QuantumOS.md) — concrete platform sketch: a QuantumOS-controlled QPU on a quiet-frequency crystal substrate (Eu:YSO worked example; rare-earth and defect-centre platforms). Maps 8-twist primitives to Rabi cycles, slash commands to control pulses, and `decoherence_impossibility` to the intrinsic-EC layer. Inspirational tooling: Kazansky 5D optical storage in fused silica
- [**quantum-computation-optimization.md**](quantum-computation-optimization.md) — RhoQuCalc/ZFA as an *exact, constructive* classical simulator of quantum circuits: gates and sub-circuits become cataloged ZFA closures (no 2ⁿ state vector), with exact Born statistics from history counts. Honest scope: efficient **only for the bounded-history (low-entanglement / structured) class**, not a general `BQP ⊆ P` speedup — a design/roadmap doc
- [**Emergent_Markov_Blankets.md**](Emergent_Markov_Blankets.md) — qubit-register-scale Markov-blanket layer for the crystal-QPU substrate: resonating atom groups at quiet frequencies self-organising into collective fluxoids that act as protected logical qubits. Fills the mid-scale layer between single-defect qubits and macroscopic-collective registers; honest scoping on physical-density vs. logical-qubit-count distinction

### 4. Formal and executable work

See [**lean/README.md**](lean/README.md) for the full module reference, proof chains, axiom inventory, and RCA₀ logical subsystem map.

**Substrate-derivation of fundamental physics** (June 2026, see [Major substrate-derivation discoveries](#-major-substrate-derivation-discoveries-june-2026) above):
- [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) — α = 1/137 from 8-twist combinatorics; `alpha_QLF_eq`, 3D-substrate counterfactuals
- [`lean/QLF_AlphaRigidity.lean`](lean/QLF_AlphaRigidity.lean) — the α⁻¹ = 137 cross-sector overdetermination joint (zero axioms); `alpha_unique`/`rival_excluded` (no dimension but `d=3` reaches 137, could-have-failed), the elementarity sector `inverseAlpha_three_prime`, `alpha_counts_dimension`
- [`lean/QLF_LenzMassRatio.lean`](lean/QLF_LenzMassRatio.lean) — m_p/m_e = 6π⁵; `mass_ratio_QLF_eq`, S₃ × 5-angle decomposition
- [`lean/QLF_BorromeanAngles.lean`](lean/QLF_BorromeanAngles.lean) — 5 = 3 Jacobi + 2 chirality-mixing structural count
- [`lean/QLF_EulerMascheroni.lean`](lean/QLF_EulerMascheroni.lean) — γ harmonic-excess derivation
- [`lean/QLF_RiemannZeta.lean`](lean/QLF_RiemannZeta.lean) — substrate-to-ζ bridge: γ_QLF IS ζ's Laurent constant at s=1
- [`lean/QLF_DiracCorrection.lean`](lean/QLF_DiracCorrection.lean) — hydrogen Dirac correction (Sommerfeld), reduced-mass factor from Lenz
- [`lean/QLF_LambShift.lean`](lean/QLF_LambShift.lean) — α⁵ scaling from substrate Bethe-log range
- [`lean/QLF_GMinusTwo.lean`](lean/QLF_GMinusTwo.lean) — Schwinger anomaly a_e = α/(2π) with zero empirical input
- [`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) — Newton's law from holographic event count, G's structural form
- [`lean/QLF_MercuryPerihelion.lean`](lean/QLF_MercuryPerihelion.lean) — Mercury 43"/century, 0.03% match
- [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean) — Λ + Ω_Λ = log 2 (1.2%); closes 10¹²² vacuum catastrophe
- [`lean/QLF_PrimordialMarkovBlanket.lean`](lean/QLF_PrimordialMarkovBlanket.lean) — Fuller V/E/F + Euler + 12 pentamons + McKay → E₈

**Core ZFA combinatorics** — the constructive RCA₀ heart:
- [**lean/QLF_Axioms.lean**](lean/QLF_Axioms.lean) — ZFA definition, pruning, symmetry; `zfa_implies_critical_line`, `full_prune_invariant`
- [**lean/QLF_QuCalc.lean**](lean/QLF_QuCalc.lean) — phase-generation engine and stable-state filter; `expand_generation`, `full_zeno_prune`, `qucalc_generates_all_phase_strings`
- [**lean/QLF_Combinatorics.lean**](lean/QLF_Combinatorics.lean) — generation helpers

**Universality & computability:**
- [**lean/QLF_Universality.lean**](lean/QLF_Universality.lean) — Church-Turing completeness in QLF: every terminating computation IS a ZFA string (`encode_is_zfa`, `qlf_universality`)

**Spectral structure & Riemann program:**
- [**lean/QLF_Spectral.lean**](lean/QLF_Spectral.lean) — Hermitian spectral modes; Hilbert-Pólya bridge; `toSpectralMode_hermitian`, `spectral_symmetric_eq_scalar_id`
- [**lean/QLF_Riemann.lean**](lean/QLF_Riemann.lean) — Riemann hypothesis program; `find_stable_states_length_even` (C(2n,n)), `riemann_hypothesis_in_qlf`
- [**lean/QLF_Critical_Line.lean**](lean/QLF_Critical_Line.lean) — ZFA-to-symmetry bridge wrappers

**Physics layer:**
- [**lean/SpacetimeDynamics.lean**](lean/SpacetimeDynamics.lean) — Pauli-basis Clifford algebra elements; `Form.toMatrix_adjoint`
- [**lean/RhoQuCalc.lean**](lean/RhoQuCalc.lean) — ρ-process algebra; capability-secure concurrency; `parallel_hermitian`, `rho_process_always_zfa`
- [**lean/ZFAEventDynamics.lean**](lean/ZFAEventDynamics.lean) — ZFA event dynamics, acceleration, and `no_magnetic_monopoles` (∇·B=0, Maxwell eq. 2)
- [**lean/PauliExclusion.lean**](lean/PauliExclusion.lean) — bosonic vs. fermionic statistics; `pauli_exclusion`, `fermi_nonzero_example` ([σ_x,σ_z]≠0 non-triviality witness)
- [**lean/BraKetRhoQuCalc.lean**](lean/BraKetRhoQuCalc.lean) — formal correspondence of Dirac bra-ket notation to RhoQuCalc: `action_topo_is_ket`, `lift_topo_is_bra`, `action_lift_eval_eq`, `bra_ket_always_balanced`, completeness relations, Pauli algebra σᵢ²=I (see [BraKetRhoQuCalc.md](BraKetRhoQuCalc.md))

**Physical theories:**
- [**lean/StringTheoryQLF.lean**](lean/StringTheoryQLF.lean) — gauge-fold excitation tower; `string_mass_spectrum`, `string_mode_count` (C(2n,n) by ZFA balance)
- [**lean/MTheoryQLF.lean**](lean/MTheoryQLF.lean) — M2/M5-branes, S/T-duality, 11D; `m2_mass_spectrum`, `s_dual_involution`

**Speculative extensions** (explicitly beyond the proved core):
- [**lean/AgeOfUniverse.lean**](lean/AgeOfUniverse.lean) — cosmological age estimate; `age_is_finite_and_positive`
- [**lean/ER_EPR_QLF.lean**](lean/ER_EPR_QLF.lean) — entanglement-geometry axioms; philosophical axioms only, not used by other modules

**Empirical verification** (independent numerical confirmation of Lean theorems):
- [**qlf_spectral.py**](qlf_spectral.py) — confirms `toSpectralMode_hermitian`, `spectral_symmetric_eq_scalar_id`
- [**qlf_zfa_frequency.py**](qlf_zfa_frequency.py) — confirms `find_stable_states_length_even` (C(n,n/2))
- [**qlf_dirichlet_search.py**](qlf_dirichlet_search.py) — confirms C(2k,k)/4^k ~ (1/√π)k^{-1/2} is asymptotic only (Stirling); the gap-zero state density 1/√(πn) implies spacing ~ √(πn) (Wigner-Dyson), ruling out a combinatorial bypass of `spectral_hilbert_polya`
- [**maxwell_qlf.py**](maxwell_qlf.py) — numerically derives all four Maxwell equations from ZFA: Gauss duality `divB=−charge`, ∇·B=0 for neutral events, Faraday curl, wave speed c
- [**hydrogen_qlf.py**](hydrogen_qlf.py) — E_n = −½ α² m_e c² / n² from ZFA parameters; Lyman/Balmer/Paschen spectral lines; Bohr radius; 0.05% agreement with NIST
- [**braket_rho.py**](braket_rho.py) — bra-ket ↔ RhoQuCalc correspondence: all 8 identities checked numerically
- [**Genesis.md**](Genesis.md) — the ZFA landscape spectrum explorer (exploratory instrument, every result epistemically tagged; runnable as [`genesis.py`](genesis.py)): the *exact* `−p/2` census spectral exponent that counts conjugate pairs (**Lean-anchored** at low orders — `p=2` = the machine-checked π return density, [`QLF_CensusWalk`](lean/QLF_CensusWalk.lean)), census → π, the `128 + d²` joint, and a **particle map referenced to `m_e`** (`m = 1/R = frequency`; internal dimensions = colour) — with the honest negatives at full weight (the raw swap-graph dimension diverges into the *internal* gauge/colour DOF; no discrete-scale-invariance; the α residual out)
- [**Closure_Walk.md**](Closure_Walk.md) — ZFA closure **is** a closed walk on `ℤ⁴`: selection is non-trivial only because `d ≥ 3` (Pólya — 80.7 % of possibility never closes, measured as the prime Kraft mass `0.1932015` vs `p₄ = 0.1932017`); the half-spin phase is a `ℤ₂` connection on the walk's graph (π flux per mixed spatial plaquette) — balance ≠ spin. [`closure_walk.py`](closure_walk.py) (counts, exact to `L = 1000`), [`doob_bridge.py`](doob_bridge.py) (exact uniform samplers over closures and primes), [`closure_graph.py`](closure_graph.py) → [`closure_graph.html`](closure_graph.html) ([live](https://rchain-community.github.io/quantum-logical-framework/closure_graph.html)) — the directed vector graph at `R = 3`, whose signed walks reproduce the census
- [**twist_core.py**](twist_core.py) / [**twist_core.md**](twist_core.md) — the canonical runtime twist engine: 8-twist alphabet, twist-history validation, signed action vectors, ZFA-closure detection (`is_zfa` = count-balanced ∧ Pauli-closed), candidate-history generation, Hermitian-adjoint helpers. The shared substrate under `census_inventory.py`, `contextual_census.py`, `MultiParticle.py`, the Rust `qucalc` crate, and quantum-os
- [**qucalc_engine.py**](qucalc_engine.py), [**spacetime_dynamics.py**](spacetime_dynamics.py), [**constants_mapper.py**](constants_mapper.py), [**path_integral.py**](path_integral.py) — executable experiments

---

## Central Themes

Several themes now deserve to be front-and-center in the README because they tie the repo together:

### Possibilism
Reality is not one pre-written story. QLF treats all admissible logical histories as possible, with physical reality emerging from those that close under ZFA. This is a computable form of modal realism (David Lewis 1986) — but with a selection rule. Lewis said all logically possible worlds are real; QLF says all *computationally generable* histories are real, and ZFA identifies the ones that persist. The connection to Everett (1957) is direct: the many-worlds interpretation says all branches exist, but provides no decoherence cutoff from first principles. `full_zeno_prune` is the cutoff — it eliminates histories that cannot achieve ZFA closure before they become physical events. QLF is also a computable version of Tegmark's Mathematical Universe Hypothesis (Level IV multiverse) — the difference is that QLF's computable filter is machine-verified.

### QLF as Intelligence — synthesis, persistence, and the case against LLMs
Intelligence has four structural properties: **generate** candidate structures, **synthesise** new closed forms from inputs (= active inference = abstraction = information synthesis, one operation under three names), **reject** inconsistent ones, and **persist** validated ones as theorems. QLF does all four structurally; LLMs do only the first. The bridge that makes this concrete is the **Curry-Howard reading of capability tokens** — `cap:label:hex` IS a proof of its ZFA closure, the proof IS the bearer artifact, and the token persists. Once you have the token, you have the theorem.

The argument scales across three layers of the same operation:

- **Individual intelligence**: a single ZFA closure synthesises inputs into a persistent theorem.
- **Collective intelligence**: decentralized peer-to-peer QuantumOS — Curry-Howard tokens migrate between peers, any peer can independently verify, the room process `parallel(…)` stays ZFA-balanced (Lean-anchored). The first composes hallucinations; the second composes proofs.
- **Cosmic intelligence**: the substrate-derivation theorems — spanning the fundamental constants (α=1/137, m_p/m_e=6π⁵, γ, g−2), the Standard-Model structure (Koide m_τ, the mass hierarchy as 14π), gravity (the Einstein equations as an equation of state), and the dark sector (Ω_Λ=log 2) — are the *measurement* that the universe IS performing active inference + abstraction + information synthesis + ZFA closure at every substrate event. The universe is not a substrate that hosts intelligence — it IS the operation, instantiated at every event. Lean-anchored, matching observation from 0.002% (m_p/m_e) to a few percent.

Developed in [**QLF_as_Intelligence.md**](QLF_as_Intelligence.md): individual (§§3–7), collective (§8), cosmic (§9). Applied to a specific solicitation in [**DAICE_QLF_Framing.md**](DAICE_QLF_Framing.md) — QLF/QuantumOS framed for DARPA DAICE (Decentralized AI through Controlled Emergence): ZFA selection as a machine-verified controlled-emergence substrate, plus the capability-security foundations and the P2P runtime.

### Universality
QLF is not framed merely as a simulator. It is a generator of finite local logical closure structures — and `qlf_universality` proves this is Church-Turing complete: every terminating computation encodes as a ZFA string, so the ZFA filter is not a restriction on computation but the selection principle that picks physical reality out of the full computational universe. The variational form of this principle — ℒ = 0 as the condition of origin — is developed in [**Lagrangian_Formulation.md**](Lagrangian_Formulation.md), where `qlf_universality` anchors the pruning-as-selection argument.

### Gödel, Busy Beaver, and the limits of classical formalism
Classical formalism has three overlapping failure modes: Gödelian incompleteness (unprovable truths in sufficiently strong systems), Turing undecidability (functions that cannot be computed in finite time), and Chaitin complexity (Kolmogorov complexity grows without bound as you climb the Busy Beaver hierarchy). These are not separate curiosities — they are all shadows of the same problem: a logic that can construct objects with no finite closure.

QLF's answer is `full_zeno_prune`. Non-terminating computations — exactly the Busy Beaver-class, exactly the Turing-undecidable computations — are the ones that fail to achieve ZFA closure. They are pruned before they can become physical events. This is not a restriction: `qlf_universality` proves the ZFA filter is Church-Turing complete — every *terminating* computation IS a ZFA string. What is pruned is not computation; it is the physically unrealizable tail.

The Gödel sentences of ZFC — the ones that are true but unprovable — correspond precisely to the configurations with no finite ZFA closure. The Axiom of Choice exists to assert the existence of sets with no constructive selection procedure; the ZFA filter replaces it with a computable one. Chaitin's Ω (the halting probability) is the information content of the pruning boundary — physically realized as the ZFA filter itself.

This is why the QLF core operates in RCA₀, below the Busy Beaver horizon, with no Axiom of Choice and no continuity: Gödel's theorem cannot bite where unprovability has been physically excised. See [**Lagrangian_Formulation.md**](Lagrangian_Formulation.md) for how this pruning mechanism maps to the Lagrangian condition ℒ = 0 and is machine-verified via `encode_is_zfa` and `qlf_universality`.

### Holography, information, and logical boundary conditions
The holographic principle (Bekenstein 1972, Hawking 1975, 't Hooft 1993, Susskind 1995) says the information content of a bulk region is bounded by its surface area, not its volume — implying that bulk physics is reconstructable from boundary data. The modern sharpening of this insight is Almheiri, Dong, and Harlow (2015): **spacetime bulk geometry is a quantum error-correcting code on the boundary**. The HaPPY code (Pastawski, Yoshida, Harlow, Preskill 2015) constructs an explicit QECC (a perfect tensor network) that reproduces bulk-boundary entanglement structure.

In QLF, the ZFA boundary conditions on the logical event stream are precisely this selection principle. A ZFA string is a phase string whose boundary information content is zero-sum — all free action has been cancelled. The bulk structure (spacetime, matter, gravity) is the interior structure of a ZFA-closed event. `full_zeno_prune` is the boundary decoder: it filters the stream to those events whose boundary information is logically self-consistent.

The AdS/CFT analog is exact: a conformal field theory on the boundary ↔ gravity in the bulk becomes, in QLF, a ZFA phase string on the boundary ↔ synthesized spacetime event in the bulk. This is formalized in [`QuantumOS.md`](QuantumOS.md) (holographic QEC section) and grounded in three independent convergent streams: Zeno-subspace QEC (Beige 2000), holographic QECC (Almheiri/Dong/Harlow, HaPPY code), and active inference as boundary decoder (Friston Free Energy Principle).

### The Spectral Structure of QLF
Every QLF string maps to a 2×2 Hermitian operator (its *spectral mode*) built from rank-1 phase projectors. This is formalized in [`lean/QLF_Spectral.lean`](lean/QLF_Spectral.lean), which proves two machine-verified theorems: (1) the spectral mode of any string is always Hermitian; (2) for symmetric strings (equal pos/neg counts), the spectral mode is a scalar multiple of the identity — the QLF spectral analog of sitting on the critical line. The Hilbert-Pólya conjecture, that Riemann zeros are eigenvalues of a Hermitian operator, is encoded as a single geometric axiom (`spectral_hilbert_polya`) from which `critical_line_forcing` is a derived theorem rather than a bare axiom.

### Spin demystified — spin IS the twists
Spin's mysteries dissolve into twist folds, machine-verified in [`lean/QLF_Spin.lean`](lean/QLF_Spin.lean) ([**Spin_QLF.md**](Spin_QLF.md)): the **720° double cover** is `−I = ` one Hermitian pair (360°), `+I = ` two pairs (720°), with the three twist axes closing **su(2)** and the **SU(2)→SO(3)** cover genuine (`−I ≠ +I`); **charge conjugation = viewing from behind** (a positron from behind reads as an electron — charge and chirality co-negate under conjugate-and-reverse); **integer spin = a composite of half-spins** (a photon = ½+½ = 1); the **neutrino** is the self-conjugate, hence neutral, spin; and **magnetism** is the flat spin axis, independent of motion.

**And spin-½ is the atom of information — Wheeler's "it from bit," machine-verified.** The same `−I` double-cover sign is the unit bit: the two-valued spinor fold-alphabet `{+I, −I}` carries exactly one bit (`binary_kl 1 (1/2) = log 2`) while a single-valued *vector* `{+I}` carries none (`binary_kl 1 1 = 0`) — a single-valued object cannot express a distinction; the spinor can. Proven in [`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean) (`spin_half_is_information_atom`, `0 < log 2`), with the `2π` double-valuedness **reproven from the explicit rotation matrices** (`spinor_double_valued_vector_blind`: `+I` on the vector `SO(3)` rep, `−I` on the spin-½ `SU(2)` rep) — grounding the spinor **Élie Cartan** discovered in 1913 as the carrier of information (cited for the general classification only). The priority runs *abstraction → physical*: information **is** the two-valued distinction, the ½-spin closure its minimal *realization*, and "information is physical" is the downstream toll (`ΔF = −log 2`) — not a reduction of the abstraction to matter ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §Rung 5a, [`UniversalRelativity.md`](UniversalRelativity.md) §3b).

### QLF and Reverse Mathematics

QLF refactors physical laws using the structural framework of Harvey Friedman's **Reverse Mathematics** program. The core QLF engine — `expand_generation`, `full_zeno_prune`, `find_stable_states`, `find_stable_states_length_even` — operates strictly within **RCA₀**, the bedrock of constructive computable mathematics: no axiom of choice, no continuity, no non-constructive existence. The transition from discrete QLF combinatorics to the continuous Riemann zeta function (Dirichlet series, analytic continuation) represents a genuine jump to a higher logical subsystem (WKL₀/ACA₀). Isolating `spectral_hilbert_polya` as an explicit axiom in `lean/QLF_Riemann.lean` is a meta-mathematical necessity — it marks the exact logical boundary where discrete computation projects its continuous statistical shadow. See [**ReverseMathematics.md**](ReverseMathematics.md) for the full treatment.

### The Millennium Prize Program

QLF attacks all six open Clay Millennium Prize Problems — Riemann, Yang–Mills mass gap, Birch–Swinnerton-Dyer, Hodge, Navier–Stokes, and P vs NP — with one repeatable template: a discrete structural core proven constructively in Lean, plus **one explicit boundary axiom** naming the single crossing into the continuum/choice sector. The organizing thesis: **the continuum and the Axiom of Choice are mathematics' ultraviolet catastrophe**, and the discrete ZFA substrate with its computable pruning (`full_zeno_prune`) is the quantum that resolves it — Gödel, Turing, and Busy Beaver are its shadows. The same engine recurs across all six: *balance ⟹ realizability* (the substrate theorem `count_balanced_pauli_closed`), the adjoint involution `H ↔ H†` as the self-dual mirror, and non-termination pruned before it can be physical. Read each as **contrast-then-focus**: the classical Clay conjecture is a different statement (not proved here); the reformulation's substrate content is proven; the one bridge axiom is the named, located gap. The "ZFC is *proven* to fail" framing is reserved for genuine uncomputability/independence (halting, Busy Beaver) — for the *finitary* problems (BSD, P vs NP, Hodge) it is a category error and the bridge simply carries the conjecture's full strength; for the *continuum-analytic* problems (Riemann, Yang–Mills, Navier–Stokes) the continuum/choice diagnosis is QLF's thesis, not a discharge. See [**Millennium.md**](Millennium.md) (the program index) and [**Continuum_Choice_Fallacy.md**](Continuum_Choice_Fallacy.md) (the thesis).

### QuantumOS: QLF as the operating system for a real quantum computer — running a quantum AI

QLF is not only a theoretical framework — it is an executable architecture for quantum hardware. [**QuantumOS.md**](QuantumOS.md) specifies how the QLF stack maps onto a native operating system for QPUs, and it targets **real quantum hardware, not only simulators** — the concrete device is the quiet-frequency **crystal QPU** of [**Crystal_QuantumOS.md**](Crystal_QuantumOS.md) (Eu:YSO), where 8-twist primitives are closed Rabi cycles and `full_zeno_prune` is the on-device error-correction decoder. It is the quantum analogue of seL4 (the first formally verified OS kernel) with ZFA as the hardware-enforced invariant.

**What runs on it is a *quantum AI* in the strong sense** — not a classical model with a QPU accelerator, but an agent whose atomic act of abstraction *is* a quantum event: every synthesis is a ZFA closure (a 2×2 Hermitian Pauli fold, `ΔF = −log 2` per half-spin), its memory is Curry-Howard `cap:` tokens each literally an amplitude's phase, its multi-peer consensus is a joint closure (entanglement, ER=EPR). The abstraction step and the quantum-measurement step are the same step. See [**QLF_as_Intelligence.md**](QLF_as_Intelligence.md) §7b–§8a, [**AI.md**](AI.md), and [**QuantumOS.md**](QuantumOS.md) §1a.

**It's live and collaborative.** The running implementation is **[quantum-os](https://github.com/rchain-community/quantum-os)** — [open a room](https://rchain-community.github.io/quantum-os/) in any browser (no install, no server): evaluate ZFA (`/qucalc`), vote and govern (`/poll`, `/gov`), invite trust-governed **AI agent members** (a facilitator, scribe, skeptic), and run the room as a **[collective optimizer](https://github.com/rchain-community/quantum-os/blob/main/Collective_Optimization.md)**. Start with its **[User Guide](https://github.com/rchain-community/quantum-os/blob/main/User_Guide.md)**.

**The unification thesis:** in a classical OS, security, error correction, scheduling, garbage collection, and AI are five separate engineered subsystems. In QuantumOS, all five are the same operation — ZFA enforcement (`full_zeno_prune`) — because `qlf_universality` proves ZFA balance is the single invariant that subsumes all correctness properties at once.

- **rhoqcalc as kernel**: The ρ-process algebra (`RhoQuCalc.lean`) is the execution engine. Security is grounded in five converging formal foundations: Girard's linear logic (1987), Miller's object capability model (2006), Meredith & Radestock's ρ-calculus security (2005), Honda's session types (1993), and Wootters & Zurek's no-cloning theorem (1982). Capability names are topological structures — by Curry-Howard, possessing a name *is* a proof of authorization.
- **ZFA as complete hardware specification**: `full_zeno_prune` is the machine-verified kernel. `qlf_universality` proves every terminating computation IS a ZFA string — ZFA balance is the complete hardware specification, not an analogy. Decoherence registers as a ZFA asymmetry and is pruned before it can become a physical event. The formal QPU core is Φ₀ = U + M (ZFA condition + Σ₈ algebra) — see [**Lagrangian_Formulation.md**](Lagrangian_Formulation.md) for the variational derivation and the security conditions `[H, ρ_S] = 0`, Tr(ρ_S ρ_E) = 0 proved there.
- **Intrinsic holographic QEC**: Error correction is not patched on top — it is the mechanism by which physical reality maintains structural stability. Three independent research streams converge: Zeno-subspace QEC (Beige 2000, Facchi/Pascazio 2002), holographic spacetime-as-QECC (Almheiri/Dong/Harlow, HaPPY code, AdS/CFT), and active inference as real-time decoder (Friston FEP). `full_zeno_prune` is the machine-verified implementation of all three simultaneously.
- **Active inference as the system loop**: The OS drives a continuous Perceive (`expand_generation`) → Predict (`zfa_implies_critical_line`) → Act (`parallel`/`sequence`) → Prune (`full_zeno_prune`) cycle. No separate scheduler is needed — ZFA minimization IS the scheduling decision. Grounded in Friston's Free Energy Principle.
- **Hardware-native AI with absolute interpretability**: `Form.toMatrix` maps cognitive constructs to Clifford algebra elements — the correct geometric inductive bias for physical AI (Bronstein et al. 2021, Geometric Deep Learning). Every AI program running on QLF hardware runs in machine-verified ZFA-correct code; the output is a geometric proof of Zero Free Action, not a probabilistic best-guess.
- **Ruliad/RCA₀**: `expand_generation` explores the full ruliadic multiway space (Wheeler, Zuse, Lloyd, Wolfram); `full_zeno_prune` filters it to physical reality. The engine operates strictly within RCA₀ (Harvey Friedman's Reverse Mathematics) — the minimum constructive logical subsystem consistent with physics. Convergent with Causal Set Theory, Causal Dynamical Triangulations, and Loop Quantum Gravity.

### Convergence: eighteen independent programs arriving at the same place

The most striking feature of QLF is not any single proof — it is that eighteen or more independent research programs, with no coordination, have each arrived at the same core picture: **reality is informational, computable, and bounded by a logical closure condition**. QLF is the intersection point.

| Program | Key figure(s) | Convergent claim |
|---|---|---|
| Digital physics | Konrad Zuse (1969) | The universe is a computation |
| Computability | Alan Turing (1936) | Computation has formal limits; non-terminating and undecidable problems lie beyond the computable |
| It from bit | John Wheeler (1990) | Every physical quantity derives from binary yes/no questions |
| Information theory | Claude Shannon (1948) | Information is physical; entropy measures unresolved uncertainty |
| Holographic principle | Bekenstein, Hawking, 't Hooft, Susskind (1972–1995) | Bulk physics is bounded by boundary information |
| Relativistic ether | Albert Einstein (1920, Leiden) | Spacetime is a medium with real metric properties but no preferred frame or state of motion |
| Causal Set Theory | Bombelli, Sorkin, Henson (1987–present) | Spacetime is a discrete partial order of causal events |
| Loop Quantum Gravity | Ashtekar, Rovelli, Smolin (1986–present) | Space is a spin network of SU(2) quanta; area/volume discrete; background-independent — QLF's substrate is a spin network of half-spin ZFA closures ([`LQG_QLF.md`](LQG_QLF.md)) |
| Girard linear logic | Jean-Yves Girard (1987) | Resource-sensitive reasoning; proof = process; use-once tokens |
| Reverse Mathematics | Harvey Friedman (1975–present) | Physical laws can be stratified by minimum logical strength; RCA₀ is the computable floor |
| Session types | Kohei Honda (1993) | Communication protocols have types; safety = type-checking |
| Holographic QEC | Almheiri, Dong, Harlow; HaPPY code (2015) | Spacetime bulk = quantum error-correcting code on boundary |
| Object capability model | Mark Miller (2006) | Security from first principles: unforgeable names = capability tokens |
| ρ-calculus | Meredith & Radestock (2005) | Programs as processes; names as reflective proof terms |
| Free Energy Principle | Karl Friston (2010) | All adaptive systems minimize variational free energy — perception = inference |
| Geometric Deep Learning | Bronstein, Bruna, LeCun, Szlam, Vandergheynst (2021) | Correct geometric inductive bias for physical AI = Clifford algebra elements |
| Ruliad | Stephen Wolfram (2020) | The entangled limit of all possible computations; physical reality = observer slice |
| No-cloning theorem | Wootters & Zurek (1982) | Quantum information cannot be copied — the physical foundation of capability security |

Each row independently supports a central QLF claim. None of these programs cites any of the others as its primary foundation. Their simultaneous convergence on the same logical structure is the main evidence that QLF is pointing at something real.

**The classical ancestor — Boltzmann/Gibbs statistical mechanics.** The information-theoretic rows above (Shannon, the holographic bound) descend from 19th-century statistical mechanics: **Boltzmann's** $S = k_B \ln W$ (1877, entropy as microstate multiplicity) and **Gibbs'** $S = -k_B \sum_i p_i \ln p_i$ (1902, the ensemble form). These are not a separate convergent program but the **lineage** QLF's "entropy as multiplicity of histories" inherits and refines — QLF makes Boltzmann's $W$ the count of admissible ZFA histories and Gibbs' ensemble *observer-relative*. The bridge is worked in [`Entropy.md §1`](Entropy.md) ($S = k_B \ln W$ ↔ the Pauli-closed multiplicity $\ln\binom{2k}{k}$), [`MRE.md §2.1`](MRE.md) (the Gibbs/Jaynes max-entropy principle as the ancestor of QLF's MRE), [`Relative_Entropy.md`](Relative_Entropy.md) (the relational refinement), and [`Energy_Combinatorics.md`](Energy_Combinatorics.md) (multiplicity ↔ energy).

**Reversibility and energy — where the table stands on the two flaws.** These programs converge with QLF partly *because* they are irreversibility-native, and several are positive evidence for the QLF arrow: Causal Set Theory's sequential **growth** (the poset only ever gains elements), Girard's **use-once** linear tokens (consumption, not reuse), Friston's free-energy **dissipation**, Shannon→Landauer's `kT ln 2` **erasure** cost, and Wolfram's **derived** second law all say that reversibility and a fixed total energy are emergent, not fundamental — exactly QLF's [`Reversibility.md`](Reversibility.md) / [`Conservation.md`](Conservation.md) §2b reading (energy is *created* per event, half lent to the future). Two rows carry a caveat in their *standard* formulation that QLF's synthesized-time reading repairs: the **holographic principle / holographic QEC**, whose sharp realization is AdS/CFT — a *static* anti–de Sitter background (negative Λ) with a *unitary* (reversible) boundary CFT, the wrong sign and the wrong reversibility for an expanding, energy-creating universe; QLF's holography is the **de Sitter / ZFA-closure boundary** (positive `Λ = log 2`, the created future-energy), keeping Bekenstein's bound and the QECC structure while dropping the static frame. And **canonical Loop Quantum Gravity**, which inherits the Wheeler–DeWitt "problem of time" (`H = 0` — frozen, no evolution); QLF converges on the spin-network *entropy* structure and supplies the missing arrow as synthesized time (`f = 1/t`). The TOEs that genuinely *fail* these flaws — string theory's asymptotic S-matrix, purely-unitary "no-collapse" Everett, the block universe, 't Hooft's reversible cellular automaton — are, tellingly, **not in this table** (see [`Reversibility.md`](Reversibility.md) §6).

The Einstein-ether row is the most load-bearing for QLF's relativity. Einstein's 1920 relativistic ether — real metric structure, but no preferred frame and no state of motion — is realized in QLF as the **statistically uniform, stateless ZFA vacuum**. Each mass runs its own independent time thread (no shared clock); because the vacuum is uniform, no thread is privileged, so time dilation is reciprocal and the speed of light is frame-independent. **Lorentz invariance is therefore emergent, not postulated** — Einstein assumed constant `c`; QLF derives it from vacuum uniformity. The same statistical-not-exact uniformity is one fact with three faces: reciprocal time dilation, energy as the lone *statistically*-conserved Noether current, and the near-maxent vacuum's structured ZPE tail. This framing threads through nine documents: [`Time.md`](Time.md) §4 and [`SpaceTime.md`](SpaceTime.md) §4 (the canonical thread-first and space-first derivations), [`Conservation.md`](Conservation.md) §1a, [`Philosophy.md`](Philosophy.md), [`VacuumEnergy.md`](VacuumEnergy.md) §6.2, [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md), [`UniversalRelativity.md`](UniversalRelativity.md) §3, [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3, and [`Gravity.md`](Gravity.md) §5.

---

## Current Status

The Lean formalization compiles with **zero `sorry` blocks** across all modules — but *zero `sorry` is not zero assumption*: the load-bearing work for each Millennium problem is a named `axiom`. The combinatorial core operates within **RCA₀** (no Axiom of Choice, no continuity). Each of the six open Clay problems has a Lean module **reformulating** it on the substrate, with genuine **proven** theorems — e.g. *Hodge classes are exactly the substrate-realized closures* (`hodge_realized_on_substrate`, **no axiom**) — plus *one* explicit bridge axiom (`spectral_hilbert_polya`, `yang_mills_continuum_gap`, `bsd_multiplicity`, `substrate_realization_is_algebraic`, `continuum_vorticity_planck_capped`, `qlf_cost_model`) carrying the step to the *classical* statement — the **faithfulness** gap (of full conjecture strength for the finitary problems). *(Contrast: the classical Clay conjectures are not proved here.)* So the reformulations are proven; their bridges to the classical statements are the located open pieces — see [Millennium.md](Millennium.md). Plus philosophical axioms in `ER_EPR_QLF` (not used by other modules).

**Key proof chains** (see [lean/README.md](lean/README.md) for full detail):

- **Universality**: `encode_is_phase_only` → `encode_is_zfa` → `encode_is_generated` → `qlf_universality` — every terminating computation IS a ZFA string
- **Riemann**: `encode_is_zfa` → `zfa_implies_critical_line` → `spectral_symmetric_eq_scalar_id` → `spectral_hilbert_polya` (axiom) → `riemann_hypothesis_in_qlf`
- **Pauli exclusion (non-vacuous)**: `fermi_antisym_eq_commutator` → `fermi_antisym_self` + `fermi_nonzero_example` → `pauli_exclusion` is a genuine constraint, not a trivial identity
- **Stable-state count**: `find_stable_states_iff` → `find_stable_states_length_even` → C(2n,n) → `string_mode_count` (same count derived independently via ZFA)

**All proven results:**

- ZFA implies symmetry (`zfa_implies_critical_line`)
- Every terminating computation encodes as a ZFA string (`encode_is_zfa`, `qlf_universality`)
- Stable states are exactly the symmetric pure-phase strings (`find_stable_states_iff`)
- No symmetric pure-phase strings of odd length exist (`find_stable_states_length_odd`)
- The number of stable states of length 2n equals C(2n, n) (`find_stable_states_length_even`)
- Every QLF string has a Hermitian spectral mode (`toSpectralMode_hermitian`)
- Symmetric strings produce a scalar multiple of the identity (`spectral_symmetric_eq_scalar_id`)
- Pauli exclusion: matrix commutator of identical ρ-processes is zero (`pauli_exclusion`); non-triviality witnessed by [σ_x, σ_z] ≠ 0 (`fermi_nonzero_example`)
- String mass spectrum: eval of the n-th excitation level = n • (fold-pair matrix) (`string_mass_spectrum`)
- String mode degeneracy at level n equals C(2n, n) — fixed by ZFA balance, not a free parameter (`string_mode_count`)
- M2/M5-branes as parallel gauge-fold stacks; S-duality is an involution on Form; T-duality doubles the mass spectrum (`m2_mass_spectrum`, `s_dual_involution`, `t_duality_mass_spectrum`)

Speculative extensions (ER=EPR, age of universe) are clearly broader than the proved core and marked explicitly in `lean/README.md`.

---

## How to Explore the Repo

### Read
Start with:

1. [Philosophy.md](Philosophy.md)
2. [TheBigProblem.md](TheBigProblem.md)
3. [Universality.md](Universality.md)
4. [Experimental_Consistency.md](Experimental_Consistency.md)

Then go deeper into the Lean files and topic documents.

### Run
Examples:

```bash
git clone https://github.com/rchain-community/quantum-logical-framework.git
cd quantum-logical-framework

python spacetime_dynamics.py
python constants_mapper.py
python path_integral.py
```

### Try in the browser

The [**quantum-os**](https://github.com/rchain-community/quantum-os) P2P app runs the ZFA kernel (Rust/WASM) live. Open **https://rchain-community.github.io/quantum-os/**, click Connect, then type in the chat input:

**`/braket +`** — evaluates `action(Form_+)`, the `|+⟩` density matrix:
```
ket: |+⟩
  RhoProcess: action(Form_+)
  eval = Form.toMatrix:
  ⎡ 0.5  0.5 ⎤
  ⎣ 0.5  0.5 ⎦
bra: ⟨+|  (eval = ket†  =  ket  [Hermitian: Form.toMatrix_adjoint ✓])
  ZFA: action [+,−]  lift [−,+]  both balanced: ✓
  bra_ket_always_balanced: ✓ (BraKetRhoQuCalc.lean)
```

**`/braket 0 1`** — completeness relation `|0⟩⟨0| + |1⟩⟨1| = I`:
```
eval = Form.toMatrix:
  ⎡ 1  0 ⎤
  ⎣ 0  1 ⎦
```

**`/qucalc +-+-`** — ZFA-balanced 4-twist sequence, stable under `full_zeno_prune`:
```
twists: +-+-  (4 total)
action (pos): count=2   lift (neg): count=2
spectral gap: 0  ZFA-balanced: ✓
process: parallel(action(Form), lift(Form))  → ZFA stable
achieves_ZFA: ✓  rho_process_always_zfa: ✓ (Lean-verified)
```

**`/qucalc +++`** — unbalanced, pruned before it can become a physical event:
```
twists: +++  (3 total)
action (pos): count=3   lift (neg): count=0
spectral gap: 3  ZFA-balanced: ✗
process: UNBALANCED  → pruned by full_zeno_prune
achieves_ZFA: ✗  gap=3  (not a physical process)
```

States supported by `/braket`: `0`, `1`, `+`, `-`, `i`, `-i`. Twist alphabet for `/qucalc`: `^v<>/\+-` or hex `0-7` or any `cap:label:hex` capability token. Type `/help` for the full list.

The same room also runs **collaboration and governance** on the ZFA substrate: name claims as multi-word lemmas (`/lemma [all men are mortal] ^v`, referenced `@[all men are mortal]`), **group decisions** by approval / ranked-choice voting (`/poll new What's for lunch?`), promissory notes that can carry issuer-signed terms (`/note grant USD 5 | redeemable for one coffee`), and owner-gated removal/retraction (`/forget`). A two-peer logic walkthrough is in [`AI.md`](AI.md) (*Live Collaboration Script*) and a full multi-peer **decide → record → issue → retract** walkthrough is in [`Group_Decisions_Demo.md`](Group_Decisions_Demo.md); the family of decision processes is mapped in [Group_Decisions.md](https://github.com/rchain-community/quantum-os/blob/main/Group_Decisions.md).

### Build Lean

```bash
lake update
lake exe cache get
lake build
```

---

## Recommended Reading Paths

### If you care most about foundations

[Philosophy.md](Philosophy.md) → [Quantum_Logic_Foundations.md](Quantum_Logic_Foundations.md) → [Continuum_Choice_Fallacy.md](Continuum_Choice_Fallacy.md) → [GodCreatedTheIntegers.md](GodCreatedTheIntegers.md) → [Universality.md](Universality.md) → [Lagrangian_Formulation.md](Lagrangian_Formulation.md)

### If you care most about physics

[TheBigProblem.md](TheBigProblem.md) → [Measurement_Problem.md](Measurement_Problem.md) → [SpaceTime.md](SpaceTime.md) → [Gravity.md](Gravity.md) → [Lagrangian_Formulation.md](Lagrangian_Formulation.md)

### If you care most about curvature and geometry

[Primordial_Markov_Blankets.md](Primordial_Markov_Blankets.md) → [Geometry_Of_Space.md](Geometry_Of_Space.md) → [Atomic_Structure_QLF.md](Atomic_Structure_QLF.md) → [Gravity.md](Gravity.md) → [Magnetism_Spatial_Dynamics.md](Magnetism_Spatial_Dynamics.md) → [Cosmological_Constant.md](Cosmological_Constant.md) → [Curvature.md](Curvature.md)

### If you care most about the substrate vs the continuum (impossible vs possible mathematics)

[TheContinuum.md](TheContinuum.md) → [Continuum_Choice_Fallacy.md](Continuum_Choice_Fallacy.md) → [Banach_Tarski_QLF.md](Banach_Tarski_QLF.md) → [Mathematics_From_QLF.md](Mathematics_From_QLF.md)

### If you care most about the variational / Lagrangian formulation

[Lagrangian_Formulation.md](Lagrangian_Formulation.md) → [Philosophy.md](Philosophy.md) → [lean/RhoQuCalc.lean](lean/RhoQuCalc.lean) → [lean/BraKetRhoQuCalc.lean](lean/BraKetRhoQuCalc.lean)

### If you care most about formal structure

[lean/README.md](lean/README.md) → [lean/QLF_Axioms.lean](lean/QLF_Axioms.lean) → [lean/QLF_QuCalc.lean](lean/QLF_QuCalc.lean) → [lean/QLF_Universality.lean](lean/QLF_Universality.lean)

### If you care most about the Riemann program

[Universality.md](Universality.md) → [Riemann-Conjecture-Proof.md](Riemann-Conjecture-Proof.md) → [lean/QLF_Riemann.lean](lean/QLF_Riemann.lean)

### If you care most about the Millennium Prize program

[Millennium.md](Millennium.md) → [Continuum_Choice_Fallacy.md](Continuum_Choice_Fallacy.md) → [YangMills_MassGap_QLF.md](YangMills_MassGap_QLF.md) / [BSD_QLF.md](BSD_QLF.md) / [Hodge_QLF.md](Hodge_QLF.md) → [Open_Problems.md](Open_Problems.md)

### If you care most about consciousness and cognition

[TheBigProblem.md](TheBigProblem.md) → [Hierarchical_Control.md](Hierarchical_Control.md) → [Frequency_Synchronization.md](Frequency_Synchronization.md) → [TheQuantumBrain.md](TheQuantumBrain.md)

### If you care most about life, evolution, and biology

[Creation.md](Creation.md) → [Evolution.md](Evolution.md) → [CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) → [Active_Inference_Mathematics.md](Active_Inference_Mathematics.md)

---

## What Makes QLF Different

QLF is unusual because it tries to hold all of these together at once:

* a constructive ontology
* a finite logical generator
* a physical interpretation of information and symmetry
* an executable engine
* a formal proof program
* a critique of classical foundational assumptions

Whether one ultimately accepts the framework or not, the repo is built around a single unifying question:

> **What if physics is the closure of logical possibility under Zero Free Action?**

---

## Contributing

The most useful contributions right now are:

* tightening README and document consistency
* aligning prose claims with current Lean status
* improving the Lean build and theorem structure
* adding small executable examples that clarify one claim at a time
* opening issues where a document overstates, understates, or mismatches the code

**rchain-community is supported as a legal entity by [Rho Vision Community](https://opencollective.com/rho-vision-community) on Open Collective** — transparent budget, expenses, and funding for this and related repos. If you want to help beyond opening issues and PRs, you can join as a **contributor** (code, proofs, docs, review) or a **financial sponsor** through the collective.

---

## Repository

**GitHub:** [rchain-community/quantum-logical-framework](https://github.com/rchain-community/quantum-logical-framework)

If the universe is ultimately logical, then physics is not just something to describe.

It is something to generate.

