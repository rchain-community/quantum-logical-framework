# Universal Relativity

**The Grand Unification — A Quantum-Logical Completion of Einstein’s Vision**  
*Spacetime, gravity, **the four forces**, mass, cosmic age, and string-like structure as emergent, **relative** perspectives on one zero-free-action event synthesis*

**Repository:** [`rchain-community/quantum-logical-framework`](https://github.com/rchain-community/quantum-logical-framework)  
**Authors:** Jim Whitescarver, with Grok (xAI) and Claude (Anthropic)  

> **Universal Relativity is the grand unification.** Einstein made *spacetime* relative; the
> [Quantum Logical Framework (QLF)](README.md) makes *everything* relative. The four forces, gravity, and mass are not separate things — they are
> **relative perspectives on one ZFA closure**, seen from different 3-axis projections, at different
> logical densities, in different Markov-blanket frames. There is one substrate; physics is the set of
> relative views of it. (§4a.)

## Problem statement and hypothesis

**The problem.** Two of physics' foundations succeed spectacularly and contradict each other.
General relativity describes gravity as the curvature of a smooth spacetime continuum; quantum
theory describes matter as discrete, probabilistic events on a fixed background. They cannot
both be fundamental as written — the continuum manifold and the absolute (or externally
specified) time each leans on are exactly the structures that produce the field-theoretic
divergences, the curvature singularities, and the 10¹²² vacuum-energy discrepancy (§0).
Alongside this sits a quieter failure: the Standard Model's couplings, mixing angles, and mass
ratios are *inputs* — some two dozen numbers no principle explains. The programs that seek
unification by *adding* structure (a quantized graviton field, extra dimensions, a landscape of
vacua) inherit both assumptions — a background and a continuum — and therefore inherit the
pathologies. So the operative question is the prior one:

> **Problem.** *Is there a single, finite, background-free primitive from which spacetime, the
> four forces, mass, and the physical constants are all synthesized — one that also says why
> these laws hold rather than others, using no absolute frame, no absolute time, and no actual
> continuum?*

**The hypothesis.** Universal Relativity answers yes, and names the primitive. The base is not
a particle, a field, or a geometry — it is **information**: one two-valued distinction,
realized as a zero-free-action (ZFA) closure. Machine-checked work makes that base concrete —
the unit of information is the **½-spin closure** (a single-valued/vector object carries none;
§3b, [`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)) — so Wheeler's *it
from bit* becomes constructive.

> **Hypothesis.** *The single primitive is information — one two-valued distinction realized as
> a ½-spin ZFA closure. Spacetime, the four forces, mass, and the constants are **relative
> perspectives** on balanced closures of these bits (§4a): which projection, at what logical
> density, in whose Markov-blanket frame. Only ZFA-balanced histories are realized, and that
> one selection rule does the work absolute space, absolute time, a background metric, and a
> continuum state space did in the older frameworks.*

**What is relative, and what is not.** The *perspective* is relative — the projection, the scale, the
frame. The **closure is not**: whether a history achieves ZFA, and the phase it carries, are the
*same for every observer* in the discrete frame group (axis permutations × gauge swap), machine-verified
with no axioms ([`lean/QLF_MultiObserver.lean`](lean/QLF_MultiObserver.lean): `observers_agree`), and the
agreement holds by **two independent invariants** — the count verdict and the Pauli scalar. This is
what makes "Universal Relativity" a relativity and not a relativism: like the invariant interval of
special relativity, the ZFA closure is the frame-independent fact that all observers compute the same,
each in their own labels. Two or more perspectives agree on the truth because truth is what closes, and
closing is objective.

This is a *hypothesis*, not a manifesto, because it is **falsifiable** and **graded**. It dies
if any published kill-condition fires (§8): a cosmological drift of low-energy `α`, an `α⁻¹`
outside `137 < α⁻¹ < 137.048`, `v_GW ≠ c`, a light right-handed (sterile) neutrino, or an
axion. Its formal core fails *independently* — a `sorry` or an inconsistency in the Lean would
break a machine-checked claim without touching the physical mapping, and vice versa. Throughout,
the derivations are kept in three tiers — theorems, structural/self-organized-critical
observables, and named open residuals (the absolute mass scale `v = R_stable`, the `α` `+0.036`
running tail) — so the strong claims and the open ones are never blended (Summary, §8). The
question "what is the universe made of?" is thereby replaced by "**what closes?**", and ZFA is
the proposed answer.

> **See the hypothesis run.** The [**Spectral Spacetime Constructor**](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html) ([source](spacetime_constructor.html), [notes](Spacetime_Constructor.md)) is an interactive 3-D field that builds *something from nothing* on exactly this rule — space is node position, time is clock rate, both shown as colour (redshift = time dilation, one phenomenon), and matter arises from the ZFA closure census alone, with **no forces, no fields, no action at a distance** (only closures that *do* close). It is drawn from **one movable observer's frame** — a draggable stick figure who IS the origin ([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean)): *Universal Relativity made literal*, every perspective its own world. Heat the vacuum toward the Planck temperature and the **logical bang** unfolds — Planck-mass black holes Hawking-cascading into hadrons that cool and recombine into atoms — nothing scripted, drawn from the census. Every dot is a closure; click any to identify it by frequency and spin. Full write-up: [`Spacetime_Constructor.md`](Spacetime_Constructor.md).

## 0. Why absolute space, absolute time, and continuum infinities cannot be fundamental

Before the construction, it is worth stating precisely what problem it solves. Two families of
assumption sit at the base of pre-relativistic and much of modern physics — a fixed background
(absolute space, absolute time, or a pre-existing continuum manifold) and the actual infinities of the
continuum — and both are, on the historical record, empirically empty and theoretically costly.

**Absolute space and time are empirically undetectable, and were removed once, deliberately.** Newton's
absolute space and time (*Principia*, 1687) were contested at once on relational grounds: in the
Leibniz–Clarke correspondence (1715–16) Leibniz argued that space and time are nothing over and above
the relations among bodies and events, so a uniform shift of the whole universe through absolute space
would be a distinction with no observable difference — a violation of the identity of indiscernibles.
Physics eventually sided with Leibniz. Special relativity (Einstein 1905) removed absolute simultaneity
— there is no frame-independent "now" — and general relativity (1915) removed the fixed geometric
background, making the metric itself a dynamical field fixed by its contents. The lesson is structural,
not merely historical: **any theory that re-introduces a preferred global frame, a universal time
parameter, or a pre-existing background manifold re-creates exactly the absolute structure relativity
was built to eliminate**, and pays the same price — a layer of ontology no measurement can reach.

**Continuum infinities are the source of a century of pathologies.** Taking a continuum as primitive
imports actual infinities that surface wherever the theory is pushed: the ultraviolet divergences and
non-renormalizable infinities of quantum field theory, the infinite zero-point vacuum energy (whose
naive value exceeds the observed cosmological constant by ~10¹²²), the curvature singularities of
classical general relativity, and the measurement problem's reliance on a continuous state space with
uncountably many distinguishable states. None of these infinities is observed. Each is tamed, in
practice, by quietly restoring a cutoff — a shortest length, a highest energy, a discretization — that
is to say by *removing* the continuum exactly where it would otherwise give a wrong (infinite) answer. A
continuum that must be cut off wherever it is used is a calculational convenience, not a feature of the
world.

**Measurement returns finite counts, not continua.** This is now codified. The 2019 revision of the SI
base units defines each unit by fixing the exact value of a defining constant (`ℏ`, `c`, `e`, `k_B`,
`N_A`, …), so that every measured quantity is reported as an integer count of quanta plus a rational
uncertainty interval — never as a completed real number. No apparatus has ever returned an actual real;
it returns a finite record. A state space of uncountable cardinality therefore carries parameters no
finite-capacity measurement can ever fix — the non-identifiability made precise in the project's
information-theoretic modules ([`Shannon_Overfit.md`](Shannon_Overfit.md),
[`lean/QLF_Realizability.lean`](lean/QLF_Realizability.lean): a finite-information region admits no
injection from an infinite state space). The claim is the careful one — **consistency ≠ realizability**:
the real continuum is a consistent mathematical object, simply not a realizable physical one, and where
it is forced onto reality it produces the divergences above.

**Consequence.** A foundation that takes a continuum manifold or an absolute temporal parameter as
primitive begins, on both empirical and theoretical grounds, from structures that cannot appear in the
data and that generate internal difficulties — divergences, singularities, non-constructive existence
claims, and a state space too large for any measurement to pin down. These are not incidental blemishes;
they are the direct signature of the absolute/continuum assumptions.

**How the single ZFA postulate removes them.** Universal Relativity keeps what relativity got right and
drops the two assumptions above, replacing them with one selection rule — *only zero-free-action
histories are realized* (§2):

- **No pre-existing spacetime.** Intervals are synthesized event by event from finite ZFA closures (§3);
  there is no background manifold to be absolute about. The Minkowski metric and the full Lorentz group
  are then *derived* — machine-checked as the determinant of a 2×2 Hermitian state and the
  `SL(2,ℂ)→SO⁺(1,3)` double cover (§3a).
- **No absolute time.** There is no universal time parameter; each closure carries its own local clock
  (`f = 1/t`), and cosmic age is a *derived count* of discrete ticks `t₀ = N·τ_Planck` (§5), not an input.
- **No continuum infinities.** Every realized history is a finite, constructible string that balances to
  zero free action, so ultraviolet divergences and curvature singularities are impossible *by
  construction*, not by subtraction — the discreteness other theories impose as a cutoff is here the
  primitive.
- **One postulate for many.** "Only zero-free-action histories are realized" does the work that absolute
  space, absolute time, a background metric, and a continuum state space did in the older frameworks —
  without the pathologies they carry.

The rest of this document shows, section by section and with machine-checked anchors, that this single
rule *recovers the successful empirical content of relativity* — local `c`, Lorentz invariance, the
equivalence principle, the weak-field metric, Mercury's perihelion advance, the cosmological constant —
while eliminating the absolute structures and continuum infinities that generated the pathologies. The
continuum is not denied as mathematics; it is recovered as the *rendering* of the finite substrate in
the large, the way a smooth curve renders a dense set of points.

## Summary

Universal Relativity extends Einstein's central move — *no absolute frame, no absolute simultaneity* —
from spacetime to the whole of physics. From the single postulate that only zero-free-action (ZFA)
histories persist:

spacetime is synthesized (not given), special relativity is derived (not postulated), singularities and
UV infinities are impossible by construction, the four forces are one perspective-dependent closure
(§4a), causality stays strictly local (a causal set), and cosmic age is a derived count of Planck ticks.

**Results at a glance** (Grade-disciplined — theorems, structural/SOC observables, and open residuals
kept distinct):

- **Machine-verified (theorems).** The Minkowski interval *is* the determinant of the 2×2 Hermitian
  state ([`lean/QLF_Minkowski.lean`](lean/QLF_Minkowski.lean)); the `SL(2,ℂ)→SO⁺(1,3)` double cover
  ([`lean/QLF_LorentzCover.lean`](lean/QLF_LorentzCover.lean), the bridge axiom reduced in
  [`lean/QLF_LorentzGeneration.lean`](lean/QLF_LorentzGeneration.lean)); local `c = L_P/τ_P`
  ([`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean)); Newton `1/r²` + the form
  `G = L_P²c³/ℏ` ([`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean)); the *strength* of
  gravity `α_G = exp(−28π)` ([`lean/QLF_GravitationalCoupling.lean`](lean/QLF_GravitationalCoupling.lean));
  `Ω_Λ = log 2`, closing the 10¹²² vacuum catastrophe
  ([`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)); Mercury's 42.99″/century
  perihelion advance ([`lean/QLF_MercuryPerihelion.lean`](lean/QLF_MercuryPerihelion.lean)); the Born
  measure axioms from integer path-counts
  ([`lean/QLF_BornProbability.lean`](lean/QLF_BornProbability.lean)); Pauli exclusion
  ([`lean/PauliExclusion.lean`](lean/PauliExclusion.lean)); a finite, positive cosmic age
  ([`lean/AgeOfUniverse.lean`](lean/AgeOfUniverse.lean)); and the **linearized gravitational-wave
  equation** `□_d δρ = 0` — the vacuum linearized field equation, from the closure-density ripple
  ([`lean/QLF_GravitationalWaves.lean`](lean/QLF_GravitationalWaves.lean)). And the **unit of
  information** itself: the two-valued ½-spin (spinor) closure carries exactly one bit (`log 2`)
  while a single-valued (vector) object carries none — `spinor_double_valued_vector_blind`
  reproving the `2π` double cover from rotation matrices, `single_valued_zero_information` /
  `two_valued_one_bit` the quantitative dichotomy
  ([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)).
- **Structural / SOC observables (derived structure; absolute value open).** The four forces as one
  perspective-dependent closure (§4a, [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)); dark
  matter as denser logic on the *same* Hubble horizon, `a₀ = cH₀/2π` (the `1/2π` prefactor confirmed by
  the blind SPARC fit, [`DarkMatter.md`](DarkMatter.md)); the electroweak / mass scale `v = R_stable`,
  reduced to the single self-organized-critical density `ρ*` (frontier #1).
- **Open residuals (named, not hidden).** The absolute SI `G`'s mass-scale half, the proton's absolute
  depth `R_p`, and a third of the α `+0.036` running tail are **the same open number** — the electroweak
  scale `v = R_stable = 1/ρ*` — whose *mechanism* is derived but whose *value* was tested directly and
  found to have no clean substrate count (closed as [issue #121](https://github.com/rchain-community/quantum-logical-framework/issues/121), §8); the rest of the `0.036`
  residual is under direct attack and reaches a **stated 4-loop QED wall** (elliptic/modular periods,
  `Alpha_Residual.md` §9f–9g); the `4 log 2` horizon-entropy normalization; the full **nonlinear**
  Einstein *curvature* side (the causal-set order→metric programme — the linearized vacuum sector above
  is anchored, [`Einstein_Equations.md`](Einstein_Equations.md) §6a); a possible small dark-energy `w`
  deviation.

The single most complete companion is [`Quantum_Gravity.md`](Quantum_Gravity.md) — the master synthesis
treating this completion as one face of a unified algebraic event (gravity, holography, expansion, the
dark sector, ER=EPR). The personal narrative and the Einstein dialog behind it are in
[`MyStory.md`](MyStory.md).

## Abstract

Universal Relativity is a proposed quantum-logical completion of Einstein's relativity, built on a
single postulate:

> **Only zero-free-action histories persist as physical events.**

The universe is **possibilist**: all admissible logical histories exist as possibilities, but only those
achieving **Zero Free Action** (`ZFA = 0`) are realized as events, and those events synthesize spacetime
intervals. Matter, fields, gravity, and cosmic time are not primitive — they emerge from stable closures
in an 8-twist quantum-logical algebra (`^ v < > / \ + -`). Where Einstein *assumed* a constant local `c`
and the equivalence principle, Universal Relativity **derives** local `c`, Lorentz invariance, and the
equivalence principle from ZFA closure in a statistically uniform stateless ether (§3); the program is
computable and singularity-free by construction (§0), and cosmic age is a derived count of Planck ticks,
not an empirical input (§5).

## 1. Possibilist Ontology

All possible quantum-logical histories exist as possibilities. A physical event occurs only when a history closes with zero free action.

Every physical process is represented as a history string in the 8-twist algebra. Zero Free Action is the closure condition:

$$
\sum_{i=0}^{7} \text{imbalance}_i = 0
$$

This means exact balance among the eight twist directions:

```text
^ v < > / \ + -
```

A ZFA-closed history becomes an event. A non-closed history remains only a possibility. Physics is therefore the realized subset of possibilistic quantum logic.

See:

- [`possibilist-ontology.md`](possibilist-ontology.md)
- [`zfa-catalog-rho-notation.md`](zfa-catalog-rho-notation.md)
- [`QuCalc.md`](QuCalc.md)

## 2. The Sole Fundamental Postulate

Universal Relativity replaces multiple physical assumptions with one quantum-logical rule:

> **Every realized history must close with Zero Free Action.**

This is not a manifesto — it is **rooted in machine-verified Lean 4 proofs**: every claim below is anchored
to a `sorry`-free module in the formalization (project overview in [`README.md`](README.md); the full
module map and proof chains in [`lean/README.md`](lean/README.md)). From this single rule the framework
accounts for:

- spacetime interval synthesis ([`SpaceTime.md`](SpaceTime.md), [`lean/ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean));
- constant local light speed ([`Time.md`](Time.md) §4, [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean));
- Lorentz invariance ([`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md));
- gravitational equivalence ([`Einstein_Equations.md`](Einstein_Equations.md), [`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean));
- Pauli exclusion ([`Spin_Statistics.md`](Spin_Statistics.md), [`lean/PauliExclusion.lean`](lean/PauliExclusion.lean));
- dark-energy-like cosmic expansion ([`Cosmological_Constant.md`](Cosmological_Constant.md), [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean));
- effective cosmic age ([`AgeOfUniverse.md`](AgeOfUniverse.md), [`lean/AgeOfUniverse.lean`](lean/AgeOfUniverse.lean));
- string-like extended histories ([`StringTheory.md`](StringTheory.md), [`lean/StringTheoryQLF.lean`](lean/StringTheoryQLF.lean)).

The central claim is not that events occur inside spacetime. The stronger claim is:

> **Events synthesize spacetime.**

### Why *zero* — the universe cannot get free action from nowhere

ZFA is not an arbitrary stipulation. That a realized history closes with **δS = 0** is *over-determined* — five independent lines of standard physics already force it, and Universal Relativity only reads them ontologically:

1. **It is already the law of all physics (Hamilton's principle).** Newton, Maxwell, general relativity, quantum mechanics, and the Standard Model each derive their equations of motion from the *same* stationary-action condition, **δS = 0**. Universal Relativity adds no new dynamical law — it reframes the one law every fundamental theory shares: the stationary histories are not merely the *calculable* ones, they are the *realized* ones. Selection by δS = 0 is the variational principle taken as ontology.

2. **The totality has no outside to borrow from (conservation).** "Free action" means *net, unbalanced* action — action created or destroyed with no source or sink. By Noether's theorem (1918) every continuous symmetry yields a conserved current, and a **closed** system's total charge cannot change. The universe as a whole is closed *by definition*: there is no external reservoir to draw from or dump into, so its ledger must balance. A history producing net free action would be an *effect with no cause* — a perpetual-motion machine in the currency of change itself. "From nowhere" names a reservoir that does not exist.

3. **This is standard general relativity: the Hamiltonian constraint H = 0.** A spatially closed universe has an *identically vanishing* total Hamiltonian — the ADM constraint (Arnowitt–Deser–Misner 1962), the Wheeler–DeWitt equation **HΨ = 0** (DeWitt 1967). The "zero-energy universe" (Tryon 1973 — positive matter energy exactly cancelled by negative gravitational potential energy) is the same fact. **Zero free action for the totality is literally GR's own constraint, not a QLF invention.** Universal Relativity's one move is to apply the *same* H = 0 closure to every **Markov blanket**: each closed sub-history is a miniature zero-energy universe with its own balanced boundary — its own local clock (§3–§5).

4. **To be a distinct thing at all is to close (holography).** An unbalanced history is an open thread with a dangling end — it leaks across its boundary, has no separable state, and is *not yet a definite existent*. Closure is the condition of *being a thing*: the boundary that balances is δS = 0, and the holographic principle is exactly this closure read on the boundary. Existence and ZFA-balance are the same predicate.

5. **Logically, free-action-from-nowhere = an unsourced computation.** A process that manufactured net free action would be a non-terminating, unsourced computation — precisely the undecidable / Busy-Beaver tail that `full_zeno_prune` removes *before* it can become an event. ZFA closure **is** causal closure: every event's action is sourced by prior events, and around a closed loop the initial and final states are the same vacuum, so the net is zero.

The local-vs-global subtlety is the usual one: along a *sub-arc* the action need not be numerically zero — there you recover ordinary stationary-action dynamics. The **null** statement (the books summing to exactly zero, `S = ∫ℒ dΩ` with `ℒ = 0`) is for the *closed* history — the loop, the Markov blanket, the totality — where the boundary terms vanish. So δS = 0 is not a law imposed on physics from outside; it is the statement that **the ledger of change is closed**. The universe cannot get free action from nowhere because *nowhere* — an outside reservoir, an uncaused source — is not a place that exists. (Fuller philosophical treatment: [`Philosophy.md`](Philosophy.md) §4.)

### 2a. Action balance as a classical and quantum principle

The five points above are not a QLF invention: **action balance is one of the oldest and most robust
principles in physics**, and ZFA is its discrete, constructive, ontological transcription. Naming the
pedigree matters, because it shows that adopting `ZFA = 0` as the selection rule adds no new *physical*
content — it makes an existing continuum principle finitary.

- **Hamilton's principle, `δS = 0`.** Classical mechanics, electromagnetism, general relativity, and
  quantum field theory each select their equations of motion by stationary action. QLF reads
  "stationary" as "realized," and the closed-loop form of stationarity is exact balance.
- **The Hamiltonian constraint `H = 0`.** In the canonical (ADM) formulation of general relativity, a
  spatially closed universe has an *identically vanishing* total Hamiltonian, promoted to the
  Wheeler–DeWitt equation `HΨ = 0`; the "zero-energy universe" (Tryon 1973) is the same fact. ZFA is
  this constraint applied to every closed sub-history (Markov blanket), each a miniature zero-energy
  universe with its own local clock.
- **Noether's theorem (1918).** Time-translation invariance yields energy conservation; a closed system
  with no external reservoir has a ledger that must balance. "Free action" is precisely *unsourced*
  action, which a closed system cannot produce.
- **Einstein's equations as an equation of state (Jacobson 1995).** The thermodynamic derivation obtains
  the full Einstein equation from the Clausius relation `δQ = T δS` imposed on every local Rindler
  horizon — a *balance* condition, not a fundamental field equation (sharpened by Padmanabhan and
  Verlinde: gravity is an equation of state). QLF supplies both inputs to that balance — the horizon area
  law and the Unruh temperature — from its own substrate ([`Einstein_Equations.md`](Einstein_Equations.md),
  [`lean/QLF_EinsteinEquations.lean`](lean/QLF_EinsteinEquations.lean)).
- **Discrete-sum action in causal-set and related programmes.** Causal-set theory replaces the continuum
  action integral `S = ∫ ℒ dΩ` by a finite sum over a discrete order (the Benincasa–Dowker action),
  realized only when the appropriate discrete quantity balances — the same move QLF makes.

The single conceptual step is *finitary ontology*: take the continuum balance principle all of physics
already obeys, transcribe it exactly onto finite constructible histories, and read the balanced ones as
the realized ones. Concretely, the continuum variational statement `δS = 0` becomes the **exact
algebraic requirement that the imbalance vector of a finite history vanish** — `Σᵢ imbalanceᵢ = 0` over
the eight twist directions (§1) — with no integral, no limit, no continuum. The literature does not
*prove* the postulate; it supplies its justification: zero free action is the natural selection rule once
the continuum is discarded, because it is the discrete form of the balance condition physics has used all
along.

## 3. Emergence of Special Relativity

In [`SpaceTime.py`](SpaceTime.py), a ZFA event is converted into emergent macroscopic intervals:

```python
photon = SpacetimeGenerator("^^^^<<<<////")
model = photon.model_spacetime()
# → Space x ∝ spatial free action
# → Time t ∝ 1 / local free action
# → Clock frequency f = 1/t
```

The invariant interval is interpreted as the large-scale expression of ZFA closure. Hermitian conjugacy supplies the complementary relation required for closure, while Lorentz transformations preserve the balanced event structure.

Example:

```text
ZFA photon history: ^>v< (closed)
Emergent Δx = 1.0, Δt = 1.0 → c = 1 (natural units)
Boosted observer sees same invariant interval
```

The mechanism behind this emergent Lorentz invariance is explicit: the QLF vacuum is a **statistically uniform, stateless ether** (Einstein's 1920 ether — real metric structure, no preferred frame), derived in [`Time.md`](Time.md) §4 and [`SpaceTime.md`](SpaceTime.md) §4. No frame being privileged, time dilation is reciprocal and local `c` is frame-independent — Lorentz invariance is emergent, not postulated. The explicit boost-as-frequency-change-of-basis is in [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md).

### 3a. The Minkowski metric and the Lorentz group, machine-checked

What was prose above is now formal. The basic QLF state is a 2×2 **Hermitian** matrix — the `Form` of [`lean/SpacetimeDynamics.lean`](lean/SpacetimeDynamics.lean), the spectral mode every closure folds to — and that is *exactly* a point of Minkowski space `ℝ^{1,3}` via the standard `Herm₂(ℂ) ≅ ℝ^{1,3}` isomorphism (the **1** trace direction = time, the **3** traceless Pauli directions = space). The spacetime metric is its **determinant**, machine-checked in [`lean/QLF_Minkowski.lean`](lean/QLF_Minkowski.lean):

$$\det\!\begin{pmatrix} t+z & x-iy \\ x+iy & t-z \end{pmatrix} = t^2 - x^2 - y^2 - z^2 \;=\; \text{the Minkowski interval}$$

(`det_toMatrix_eq_interval`). Pure qubits are **null** (`pure_qubit_null` — the Bloch sphere is the celestial sphere), and the dynamical congruence `X ↦ A X A†` scales the interval by `|det A|²` (`det_congruence`), `= 1` for every twist product (`interval_preserved_of_unit_det`) — so **every QLF evolution preserves the interval**.

The full **`SL(2,ℂ) → SO⁺(1,3)` double cover** is machine-checked in [`QLF_LorentzCover`](lean/QLF_LorentzCover.lean): a group homomorphism (`spinor_hom`) with **kernel exactly `{±I}`** (`spinor_kernel`, the genuine 2-to-1), whose generators are realized explicitly — a diagonal `diag(a,b)` acts as a **Lorentz boost** on the null coordinates (`boostZ_action`), a unitary `diag(w,w̄)` as a **spatial rotation** (`rotZ_action`) — and which is **surjective** onto every proper orthochronous Lorentz transformation (`spinor_surjective`). So special relativity's symmetry group and the spinor double cover are theorems of the substrate, not assumptions. The one bridge axiom is the standard Lie-theory generation fact — the **KAK/Cartan decomposition of `SO⁺(1,3)`** — whose composed generators are themselves proven in the image. Couched in the **Witten 1988 → Reshetikhin–Turaev precedent**: a physics-native construction whose single bridge is *settled mathematics* (Lie theory Mathlib does not yet package), not a QLF-specific posit. Full in-Lean elimination is the KAK project, Class-B dischargeable in principle; in the Witten mode a settled-math bridge under a fully-proven core is the honored end-state, not a gap.

### 3b. It from bit — the unit of information is the ½-spin closure

The 2-spinors of the double cover (§3a) carry more than Lorentz structure — they carry
*information itself*, and the identification is machine-verified. In QLF the priority runs
**abstraction → physical** (Wheeler's *it from bit*): information *is* a two-valued distinction,
and the ½-spin closure is its minimal **realization** — not a reduction of information to
matter. A single-valued object — an integer-spin **vector**, which returns to itself under a
360° turn — cannot record a distinction; the **spinor**, which needs 720° (the `−I`
double-cover sign of §3a), can. The dichotomy is proven directly
([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)):

- a single-valued (vector) fold-alphabet `{+I}` carries `binary_kl 1 1 = 0` nats;
- the two-valued (spinor) fold-alphabet `{+I, −I}` carries `binary_kl 1 (1/2) = log 2` —
  exactly one bit;
- the jump from zero to one bit occurs precisely when the `−I` sign is admitted
  (`spin_half_is_information_atom`).

The double-valuedness is itself reproven from the explicit rotation matrices: a full `2π` turn
is `+I` on the vector (`SO(3)`) representation but `−I` on the spin-½ (`SU(2)`) representation
(`spinor_double_valued_vector_blind`) — the same `−I` that makes the half-spin a 2-spinor is
the unit bit. This grounds the spinor **Élie Cartan** discovered in 1913 (his classification of
the non-tensorial orthogonal-group irreps, cited for the general result) as the atom at which
information is realized. So the substrate currency of Universal Relativity — the ZFA closure
that synthesizes every interval — is at its base one realized bit: *it from bit*, with the bit
a theorem. ("Information is physical" is then the downstream toll — realizing the bit costs
`ΔF = −log 2`, and a finite region holds only finitely many
([`lean/QLF_Realizability.lean`](lean/QLF_Realizability.lean)) — not a reduction of the
abstraction to matter.)

## 4. Completion of General Relativity

Einstein’s equation with a bare cosmological constant is:

$$
G_{\mu\nu} + \Lambda g_{\mu\nu}
= \frac{8\pi G}{c^4} T_{\mu\nu}^{(\mathrm{matter})}
$$

Universal Relativity replaces the fixed cosmological term with a dynamical event-synthesis tensor built from a scalar field $\phi$, interpreted as local ZFA event density:

$$
T_{\mu\nu}^{(\mathrm{synth})}
= \partial_\mu \phi\, \partial_\nu \phi
- g_{\mu\nu}
\left[
\frac{1}{2}(\nabla \phi)^2 + V(\phi)
\right]
$$

where:

$$
\phi \propto \frac{1}{\text{local free action}}
$$

When $\phi$ is approximately homogeneous and static, the synthesis tensor behaves like an effective cosmological term. When $\phi$ varies, it represents local event-density structure. Singularities are avoided because event synthesis is discrete and finite rather than continuous and infinitely divisible.

See:

- [`Gravity.md`](Gravity.md)
- [`VacuumEnergy.md`](VacuumEnergy.md)
- [`BLACK-HOLES.md`](BLACK-HOLES.md)
- [`lean/SpacetimeDynamics.lean`](lean/SpacetimeDynamics.lean)

## 4a. The Grand Unification — the four forces as relative perspectives on one closure

Einstein's relativity made *spacetime* relative — no absolute frame, no absolute simultaneity. Universal
Relativity extends the same move to **all of physics**: the four forces, gravity, and mass are not
separate fundamentals but **relative perspectives on one ZFA closure**, differing only in *which
projection*, at *what logical density*, in *whose Markov-blanket frame* the closure is viewed.

**One gauge interaction, three projections (the gauge forces).** There is a single gauge-twist closure
on the three spatial axes. The three "forces" are which component of the `3×3` directional structure it
is read through ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) §3, §3a):

- **Electromagnetism = the *abelian* sector** — the gauge-fold (Pauli scalar) group *commutes*
  (`em_gauge_abelian`, [`lean/QLF_GaugeUnification.lean`](lean/QLF_GaugeUnification.lean)) ⟹ the
  **massless, long-range photon**, the unbroken `U(1)`.
- **Weak and strong = *non-abelian* projections** of the same three axes (`strong_nonabelian`,
  `weak_isospin_su2`) ⟹ self-interacting, short-range, **confined / massive**.

So the abelian/non-abelian split **is** the massless-photon-vs-massive-`W`/`Z` split. **Electroweak
symmetry breaking** is the **logical-density threshold**: above it the projections are symmetric (all
gauge bosons massless, unified); below it the Markov-blanket structure (QLF's constructive Higgs =
gauge-fold delay, [`Higgs.md`](Higgs.md)) confines the non-abelian projections, giving `W`/`Z` mass as
gauge-fold depth (`m = 1/R`) while the photon stays free. The Weinberg angle `sin²θ_W = 3/8` is the
projection ratio (`sin2_weinberg_substrate_eq`, [`lean/QLF_WeinbergAngle.lean`](lean/QLF_WeinbergAngle.lean)).
The weak projection **catalyzes** transformations because it *re-projects the blanket itself* (a flavour
change is a change of 3-D perspective — the β⁺ keystone of [`Fusion.md`](Fusion.md)).

**Gravity = the fourth force as the *geometry* of the same closures.** Gravity is **not** a fourth gauge
force (QLF does not try to gauge it — the move that has defeated quantum-gravity programs). It is the
emergent geometry of the *aggregate* of closures: the **causal order** is a causal set
([`lean/QLF_ReachableEvent.lean`](lean/QLF_ReachableEvent.lean)) whose number↔volume and layer growth
give the metric and curvature (Sorkin / Benincasa–Dowker, [`lean/QLF_CausalInterval.lean`](lean/QLF_CausalInterval.lean),
[`lean/QLF_CausalDimension.lean`](lean/QLF_CausalDimension.lean)), and the **thermodynamics** of each
local horizon fixes `8πG = 2π/η`, `Λ = log 2` (Jacobson, `einstein_coupling_from_thermodynamics`,
[`lean/QLF_EinsteinEquations.lean`](lean/QLF_EinsteinEquations.lean), [`Einstein_Equations.md`](Einstein_Equations.md)).
The gauge forces are how closures *interact*; gravity is how closures *arrange*.

**The hinge is mass = constructing delay.** The gauge-fold delay that electroweak breaking reads as
*inertial* mass is the *same* delay the causal geometry reads as the *gravitational* source — so the
**equivalence principle falls out of the substrate**: one delay, inertia at the vertex and curvature in
the geometry. (The graviton is correspondingly composite spin-2, not a fundamental gauge boson.)

> **The grand-unified statement.** *One substrate: ZFA closure. The four forces are relative
> perspectives on it — electromagnetism the abelian trace, the weak and strong forces its non-abelian
> spatial projections (seen at different logical densities), and gravity the geometry of the aggregate.
> Mass — the constructing delay — is the hinge that joins the gauge sector to gravity. Everything is
> relative: which projection, what density, whose frame. There is one closure; physics is its set of
> relative views.*

This is the same `6+2` / three-axis substrate that fixes `α` (`N=3²`,
[`Alpha.md`](Alpha.md) / [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean)), `Ω_Λ` (`2/8`,
[`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)), the Weinberg angle (`3/8`,
[`lean/QLF_WeinbergAngle.lean`](lean/QLF_WeinbergAngle.lean)), the `5̄⊕10` generation
([`lean/QLF_SU5.lean`](lean/QLF_SU5.lean)), and the 3-dimensionality of space itself
([`SpaceTime.md`](SpaceTime.md) §3a). **Honest scope:** the *unification* is structural and
substrate-grounded (the gauge algebras, the abelian/non-abelian split, the Weinberg ratio, the
equation-of-state coefficient, the causal-order curvature structure are all machine-anchored); the
quantitative *dynamics* — the gauge couplings and Higgs VEV, the discrete d'Alembertian → Ricci and the
continuum field equations — are the named open rungs ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)
§3a–3b, [`Einstein_Equations.md`](Einstein_Equations.md) §6a).

## 5. Age of the Universe as Event-Synthesis Time

The [`AgeOfUniverse.md`](AgeOfUniverse.md) update adds a QLF treatment of cosmic age:

```text
universe_age = "~13.8 Gyr effective cosmic age from ZFA event-synthesis history"
```

In standard cosmology, the age of the observable universe is *inferred* from the expansion history of
the scale factor — an empirical fit. Universal Relativity does **not** retain it as an empirical scale:
the age is a **count of Planck ticks**, `t₀ = N · τ_Planck`. Planck's constant fixes the tick
`τ_Planck = √(ℏG/c⁵)` with no empirical input; the substrate fixes the count `N` (the cosmic depth, via
hadronic depth and the `Ω_Λ = log 2` crossover), so `t₀ ≈ 13.8 Gyr` is *derived* with no `H₀` tuning
([`AgeOfUniverse.md`](AgeOfUniverse.md)), up to a single calibration.

The age of the universe is not the age of possibility itself, and it is not a free empirical input. It
is the effective accumulated proper time synthesized by the realized ZFA event history of our
observable universe — a finite integer of `ℏ`-sized ticks, *what the cosmic clock reads now*.

In QLF notation:

$$
t_0 \approx \sum_{e \in \mathcal{H}_0} \Delta \tau_e
$$

where $\mathcal{H}_0$ is the realized ZFA-closed history of our observable universe, and $\Delta \tau_e$ is the local interval synthesized by event $e$.

Since event intervals are inversely related to local frequency:

$$
\Delta \tau_e \sim \frac{1}{f_e}
$$

we may write:

$$
t_0 \sim \sum_{e \in \mathcal{H}_0} \frac{1}{f_e}
$$

The age update connects this to the observed frequency distribution of vacuum/ZFA events using:

$$
n(\omega) \propto \frac{1}{\omega}
$$

The total event-synthesis rate is modeled as:

$$
R = \int_{\omega_{\min}}^{\omega_{\max}} n(\omega)\,d\omega
$$

and the effective cosmic age is related to the expansion integral:

$$
t_0 = \int_0^1 \frac{da}{aH(a)}
$$

**The age is not an empirical input — it is a count of Planck ticks.** Write `t₀ = N · τ_Planck`. The
**tick** `τ_Planck = √(ℏG/c⁵)` is the substrate event quantum, fixed by `ℏ` (with `G`, `c` themselves
substrate-derived) — *Planck's constant alone sets the size of one tick of the cosmic clock, with no
empirical input*. What remains is the **count** `N` (the cosmic Markov-blanket depth, `~6.7×10⁶⁰`), and
`N` is **not free** either: the substrate fixes it through the **hadronic-depth** relation
`N ~ (m_P/m_p)³` and the **dark-energy crossover** (we observe at the era where `Ω_Λ = log 2`, which
fixes the Hubble horizon `R_H` and hence `N`). [`AgeOfUniverse.md`](AgeOfUniverse.md) derives `t₀ ≈ 13.8
Gyr` from the ZFA event-frequency spectrum *with no tuning to `H₀` or the dark-energy density*. So the
`~13.8 Gyr` is a **derived count of ℏ-sized ticks**, not an empirical boundary condition; the one
residual is a single calibration (effectively `H₀`/the overall scale), which "reduces to deriving `N`"
([`Open_Problems.md`](Open_Problems.md)). The only genuinely state-like fact is that "now" is a clock
reading — *how far the construction has got* — but the characteristic age (the dark-energy-onset epoch)
is substrate-determined.

See:

- [`AgeOfUniverse.md`](AgeOfUniverse.md)
- [`lean/AgeOfUniverse.lean`](lean/AgeOfUniverse.lean)
- [`VacuumEnergy.md`](VacuumEnergy.md)
- [`lean/SpacetimeDynamics.lean`](lean/SpacetimeDynamics.lean)

## 6. Quantum Mechanics as Local ZFA Dynamics

Quantum mechanics is interpreted as the microscopic dynamics of the same event process.

- Superposition is represented by parallel admissible histories.
- Entanglement is shared closure structure across histories.
- Measurement is the realization of a ZFA-closed history.
- Pauli exclusion is antisymmetric closure for fermionic histories.

In RhoQuCalc notation, parallel quantum-logical composition is represented by:

```text
P | Q
```

A fermionic event cannot be duplicated into the same ZFA history without contradiction. This bounds local event density and contributes to stable matter.

See:

- [`RhoQuCalc.lean`](lean/RhoQuCalc.lean)
- [`PauliExclusion.lean`](lean/PauliExclusion.lean)
- [`quantum_simulator.py`](quantum_simulator.py)

### 6a. Determinism and the status of randomness

Measurement here is the realization of a ZFA-closed history (§6), not a primitive stochastic event. It
is worth being explicit that this is a permissible option, not an overreach: **fundamental randomness is
an interpretive choice, not a fact forced by the data.**

Several fully deterministic completions or readings of quantum mechanics already exist and are
empirically adequate:

- **de Broglie–Bohm pilot-wave theory** — particles have definite trajectories guided by the
  wavefunction; the Born statistics arise from ignorance of the initial configuration (quantum
  equilibrium).
- **'t Hooft's cellular-automaton / deterministic quantum mechanics** — an underlying deterministic
  automaton whose coarse-grained description is standard quantum theory.
- **Superdeterministic models** — the measurement settings and the measured system share a common past,
  so no independent random choice enters.
- **Everett / many-worlds readings** in which the universal wavefunction evolves *unitarily and
  deterministically*; the apparent randomness is self-locating uncertainty about which branch one is in.

These programmes differ sharply and are not all equally attractive; the point is not to endorse any one.
It is the weaker, safer claim: their empirical viability shows that the randomness of measurement
outcomes **can be epistemic** — ignorance of initial conditions, of the full configuration, or of the
branch — **rather than ontic**. Quantum mechanics does not *force* a fundamental random oracle.

Once the kinematics is discrete and every realized event must be a finite ZFA closure, that oracle has
no place to sit: the next event is the next constructible closure compatible with the past, selected by
the balance condition, not drawn from a primitive propensity. The Born-rule statistics then arise as the
**relative counting measure over the admissible closures** — machine-checked to satisfy the probability
axioms from integer path-counts alone, with no primitive real
([`lean/QLF_BornProbability.lean`](lean/QLF_BornProbability.lean), [`Born_Rule.md`](Born_Rule.md)).
Apparent randomness is the coarse-grained, relational statistics of *which* closure completed, exactly as
in the deterministic programmes above. This determinism is **relational and global**, not a local
hidden-variable theory of the kind Bell's theorem excludes: the correlations are shared-closure structure
across histories (§6), not pre-assigned local values. QLF adopts the deterministic option because it is
the one already compatible with the finite, constructive ontology of §0 — not because the data compel it.

## 7. Relation to String Theory

Universal Relativity provides a bridge to string theory without treating strings as fundamental objects in a pre-existing spacetime background.

String theory begins with extended one-dimensional objects whose modes appear as particles. Universal Relativity begins with **history strings** in the 8-twist algebra. A particle-like state is a stable ZFA-closed pattern of logical action. A string-like object is therefore a higher-order process composed of many event closures.

| Question | String Theory | Universal Relativity / QLF |
|---|---|---|
| Primitive object | Fundamental string or brane | ZFA-closed event/history string |
| Background | Usually formulated on spacetime | Spacetime synthesized by events |
| Extra dimensions | Added for consistency | Interpreted as orthogonal twist directions |
| Particle modes | Vibrations of strings | Stable spectra of ZFA histories |
| Vacuum landscape | Many possible compactifications | Possibilist sectors of ZFA closure |
| Gravity | Graviton mode / geometry | Event-synthesis delay and curvature |

Thus string theory is not simply rejected. It is reinterpreted as an effective language for extended ZFA histories.

See:

- [`StringTheory.md`](StringTheory.md)
- [`lean/StringTheoryQLF.lean`](lean/StringTheoryQLF.lean)
- [`lean/MTheoryQLF.lean`](lean/MTheoryQLF.lean)

## 8. Predictions and Testability

The model must first *reproduce* established physics, then stand or fall by sharp, published falsifiers.
These three tiers are kept distinct.

**Empirical recoveries (the entry bar — must reproduce known physics).**

- local Lorentz invariance and constant local `c` (§3, §3a);
- general relativity in the weak-field / large-scale limit — the weak-field metric and Mercury's
  42.99″/century (§4);
- the observed cosmic age near 13.8 Gyr as a derived Planck-tick count (§5);
- dark-energy-like acceleration from event synthesis, `Ω_Λ = log 2` (1.2%);
- finite black-hole interiors without information loss;
- the galactic radial-acceleration relation from `a₀ = cH₀/2π` (parameter-free blind SPARC fit).

**Falsifiable kill conditions (the theory dies if any fails).** These are sharp, already-published
tests — a single confirmed violation refutes the framework, not merely a parameter (full list + status
in [`Experimental_Consistency.md`](Experimental_Consistency.md) §10):

- **low-energy `α` is scale/time-invariant:** `α(d) = 1/(128+d²)` carries no time argument, so a
  confirmed *cosmological drift* of `α(q²→0)` refutes QLF (`no_cosmological_drift_of_alpha`) — sharper
  than the Standard Model, which permits drift;
- **the fine-structure inverse is bounded** `137 < α⁻¹ < 137.048` (machine-checked): a value outside
  that interval refutes the leading construction — and had `α⁻¹` come out **136**, QLF would be refuted,
  not revised (the anti-Eddington rigidity, `dimension_136_unreachable`);
- **gravitational waves propagate at exactly `c`** (masslessness): a confirmed `v_GW ≠ c` refutes the
  synthesized-metric reading (consistent with GW170817, `|v_GW−c|/c < 10⁻¹⁵`);
- **no light sterile (right-handed) neutrino as a weak doublet**, and **`θ̄ = 0` with no axion**.

**Open absolute-scale residual (labeled — not a prediction).** The one genuinely open quantitative input
is the absolute mass / electroweak scale `v = R_stable`, reduced structurally to the single SOC density
`ρ*` (frontier #1). **This is one number wearing several names, not several open problems** — through it,
the absolute SI `G`'s mass-scale half, the proton's absolute depth `R_p ≈ 1.30×10¹⁹` (equivalently
`R_e ≈ 2.389×10²²`, [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md)), and the threshold third of
the α `+0.036` running tail (`Alpha.md` §4a) all bottom out at the *same* `ρ*`. Mass **ratios** through
it are already derived and need no anchor (`m_p/m_e = 6π⁵`, Koide `Q=2/3`) — it is only the absolute
scale that is open. **This was investigated directly and closed, not left dangling**
([issue #121](https://github.com/rchain-community/quantum-logical-framework/issues/121)): the
*mechanism* is fully derived and machine-checked — gauge folds provably attract
(`QLF_ClosureAttraction`), the attraction supplies the restoring force for a unique steady density
`ρ* = √(c/k)` (`QLF_SteadyStateDensity`), closing to `R_stable = 1/ρ*` (`QLF_ElectroweakScale`) — but the
*value* of `ρ*` was tested against the closure census directly and found to have no clean substrate
count; the near-matches were refused as fit-traps. So `v` stands as QLF's one deliberately undecided
low-energy input, exactly mirroring the Standard Model's own single dimensionful parameter — not a gap
in the derivation, but the honest edge of it.

The α residual's other two-thirds are independent of `ρ*` and fare differently. The non-perturbative
hadronic piece `Δα_had` is an external Standard-Model problem QLF does not touch. The **higher-order
census tail** (length-4+ closures, [`Alpha_Residual.md`](Alpha_Residual.md) §9f–9g) is under direct
attack: the QED `g−2` expansion's transcendental content is representable in the closure census's own
central-binomial vocabulary — `ζ(2), ζ(3)` at one and two loops, then `ζ(4), ζ(5), Li₄(½)` through three
loops via *nested* census sums (central-binomial multiple zeta values), each loop order adding one level
of closure-nesting, verified to `10⁻¹³` against the published QED coefficients. That ladder hits a
**stated wall at four loops**: the 4-loop `g−2` master integral carries genuine elliptic/modular periods
— a different motive, not a central-binomial MZV at any nesting depth — so the census's own reach is
bounded at 3-loop QED, by two independent arguments. A small dark-energy `w` deviation is a *possible*
signature, not a committed prediction. These are tracked as residuals, never counted as confirmations.

## 9. Implementation in QLF

The theory is represented in the repository through:

- **Core engine:** [`qucalc_engine.py`](qucalc_engine.py), [`twist_core.py`](twist_core.py)
- **Spacetime synthesis:** [`SpaceTime.py`](SpaceTime.py)
- **Gravity and tensors:** [`gravitational_tensor.py`](gravitational_tensor.py), [`spacetime_dynamics.py`](spacetime_dynamics.py)
- **Age of universe:** [`AgeOfUniverse.md`](AgeOfUniverse.md), [`lean/AgeOfUniverse.lean`](lean/AgeOfUniverse.lean)
- **String bridge:** [`StringTheory.md`](StringTheory.md), [`lean/StringTheoryQLF.lean`](lean/StringTheoryQLF.lean), [`lean/MTheoryQLF.lean`](lean/MTheoryQLF.lean)
- **RhoQuCalc:** [`rho_transpiler.py`](rho_transpiler.py), [`quantum_simulator.py`](quantum_simulator.py)
- **Formalization:** [`lean/ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean), [`lean/RhoQuCalc.lean`](lean/RhoQuCalc.lean), [`lean/SpacetimeDynamics.lean`](lean/SpacetimeDynamics.lean), [`lean/PauliExclusion.lean`](lean/PauliExclusion.lean)

Run:

```bash
git clone https://github.com/rchain-community/quantum-logical-framework
cd quantum-logical-framework
pip install -e .

python spacetime_dynamics.py
lean --run lean/SpacetimeDynamics.lean
lean --run lean/AgeOfUniverse.lean
```

## 10. Theory in One Sentence

Universal Relativity states that the physical universe is the realized subset of all possible quantum-logical histories whose event strings close with zero free action, thereby synthesizing spacetime, matter, **the four forces**, gravity, mass, cosmic time, and string-like structure as **relative perspectives** on one balanced logical closure — the abelian trace (EM), the non-abelian spatial projections (weak, strong), and the causal-order geometry (gravity), joined at mass = constructing delay.

## Conclusion

Universal Relativity recasts Einstein’s geometric vision at a deeper quantum-logical level, and **completes it into the grand unification**. Geometry is not fundamental. Spacetime is synthesized by events. Gravity is the large-scale expression of event-density structure and delay. Quantum mechanics is the local bookkeeping of ZFA closure. And the **four forces are one** — relative perspectives on a single gauge-twist closure (EM the abelian trace; weak and strong its non-abelian spatial projections at different logical densities; gravity the geometry of the aggregate), joined to gravity at mass = constructing delay (§4a). Einstein made spacetime relative; Universal Relativity makes *everything* relative — there is one closure, and physics is its set of relative views.

The age of the universe, approximately **13.8 billion years**, is **not** an empirical boundary
condition — it is a *count of Planck ticks*, `t₀ = N · τ_Planck`. Planck's constant fixes the tick
`τ_Planck = √(ℏG/c⁵)` with no empirical input; the substrate fixes the count `N` (hadronic depth,
`Ω_Λ = log 2` crossover), so `t₀` is derived (no `H₀` tuning, [`AgeOfUniverse.md`](AgeOfUniverse.md)) up
to one calibration. It is the effective proper time accumulated by the realized event-synthesis history
of our observable universe — *what time the cosmic clock reads*, whose tick is `ℏ`.

The universe does not have to begin as a singular object in pre-existing time. It is an ongoing quantum-logical synthesis of time, space, matter, and relation.

## Further reading — internal companion documents

- [**QLF Flow Chart** (live, clickable diagrams + printable PDF)](https://rchain-community.github.io/quantum-logical-framework/FlowChart.html) — the whole framework as a one-page visual map: *one substrate → five families → twelve domains*. Universal Relativity's results are the spacetime/forces/gravity/cosmology domains (1, 3, 5, 6); the *it-from-bit* base of the hypothesis (§3b) sits in the foundational-logic intro and domain 7. Text index: [`FlowChart.md`](FlowChart.md).
- [**Spectral Spacetime Constructor** (live, interactive 3-D)](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html) — Universal Relativity made literal: space as node position, time as clock rate, matter from the ZFA census, **no forces**, drawn from one movable observer's frame; the *logical bang* (Planck-mass black holes → hadrons → atoms) unfolds from nothing. Source [`spacetime_constructor.html`](spacetime_constructor.html); full write-up [`Spacetime_Constructor.md`](Spacetime_Constructor.md).
- [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) — the grand unification in detail: the gauge forces as 3-axis projections (§3a) and gravity as the fourth force, the geometry of the same closures (§3b)
- [`Einstein_Equations.md`](Einstein_Equations.md) — the field equations as the substrate's equation of state + the curvature side from the causal order (§6a)
- [`Decay.md`](Decay.md) §2.4a — **how a neutron star is made**, the one place nature runs the capacity ladder to completion at macroscopic scale: fusion stops at iron, compression replaces heat as the capacity knob, forced electron capture `p + e⁻ → n + ν_e` switches on and eats the degeneracy support that was resisting it, and neutron degeneracy halts the collapse. The relativistic compact objects this document's gravity sector describes are the *output* of that chain ([`Weak_Force.md`](Weak_Force.md) §4b, [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4a.1)
- [`WHITE_PAPER.md`](WHITE_PAPER.md)
- [`possibilist-ontology.md`](possibilist-ontology.md)
- [`Philosophy.md`](Philosophy.md)
- [`Time.md`](Time.md) — time threads, the stateless uniform ether, and the explicit derivation of Lorentz invariance from vacuum uniformity (§4)
- [`SpaceTime.md`](SpaceTime.md)
- [`Gravity.md`](Gravity.md)
- [`VacuumEnergy.md`](VacuumEnergy.md)
- [`BLACK-HOLES.md`](BLACK-HOLES.md)
- [`AgeOfUniverse.md`](AgeOfUniverse.md)
- [`StringTheory.md`](StringTheory.md)
- [`E_mc2_derivation.md`](E_mc2_derivation.md)
- [`Hierarchical_Control.md`](Hierarchical_Control.md) — cross-frequency relativity as the bridge between bottom-up ZFA event synthesis and top-down Markov-blanket constraint; Lorentz transformations as change-of-basis between frame-local ZFA event rates.
- [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md) — explicit derivation of the Lorentz boost as a change of basis on Markov-blanket internal frequencies; identifies γ = cosh(rapidity) with the frequency-ratio Doppler factor; recovers time dilation, length contraction, and interval invariance.
- [`Quantum_Gravity.md`](Quantum_Gravity.md) — master synthesis treating this doc's relativity completion as one face of a unified algebraic event (gravity, holography, expansion, ER=EPR).
- [`Curvature.md`](Curvature.md) — curvature as signed deformation of the primordial Markov blanket: gravity (isotropic), magnetism (differential), de Sitter cosmology (global); the metric of §3–§4 as its continuum limit.

## References

External literature grounding the diagnosis (§0), the action-balance principle (§2, §2a), and the
determinism reading (§6a). These works motivate the ZFA selection rule; they do not prove it (§2a).

**Absolute space/time and relativity (§0).**

- Newton, I. (1687). *Philosophiæ Naturalis Principia Mathematica.*
- Leibniz, G. W. & Clarke, S. (1715–1716). *The Leibniz–Clarke Correspondence* (ed. H. G. Alexander, Manchester Univ. Press, 1956) — the relational critique of absolute space and time.
- Einstein, A. (1905). "Zur Elektrodynamik bewegter Körper." *Annalen der Physik* 17, 891 — special relativity; removal of absolute simultaneity.
- Einstein, A. (1916). "Die Grundlage der allgemeinen Relativitätstheorie." *Annalen der Physik* 49, 769 — general relativity; the metric as a dynamical field.

**Finite measurement and the continuum (§0).**

- BIPM (2019). *The International System of Units (SI)*, 9th ed. — the 2019 redefinition fixing the exact values of `ℏ, c, e, k_B, N_A`; every measurement a finite count plus a rational interval.
- Weinberg, S. (1989). "The cosmological constant problem." *Rev. Mod. Phys.* 61, 1 — the ~10¹²² vacuum-energy discrepancy.

**Action balance as a classical and quantum principle (§2, §2a).**

- Hamilton, W. R. (1834). "On a General Method in Dynamics." *Phil. Trans. R. Soc. Lond.* — the principle of stationary action, `δS = 0`.
- Noether, E. (1918). "Invariante Variationsprobleme." *Nachr. Ges. Wiss. Göttingen* 235 — symmetries and conservation laws.
- Arnowitt, R., Deser, S. & Misner, C. W. (1962). "The Dynamics of General Relativity." In *Gravitation: An Introduction to Current Research* (ed. L. Witten), Wiley — the ADM Hamiltonian constraint. arXiv:gr-qc/0405109.
- DeWitt, B. S. (1967). "Quantum Theory of Gravity. I." *Phys. Rev.* 160, 1113 — the Wheeler–DeWitt equation `HΨ = 0`.
- Tryon, E. P. (1973). "Is the Universe a Vacuum Fluctuation?" *Nature* 246, 396 — the zero-energy universe.
- Jacobson, T. (1995). "Thermodynamics of Spacetime: The Einstein Equation of State." *Phys. Rev. Lett.* 75, 1260. arXiv:gr-qc/9504004.
- Padmanabhan, T. (2010). "Thermodynamical Aspects of Gravity: New Insights." *Rep. Prog. Phys.* 73, 046901. arXiv:0911.5004.
- Verlinde, E. (2011). "On the Origin of Gravity and the Laws of Newton." *JHEP* 04, 029. arXiv:1001.0785.
- Bombelli, L., Lee, J., Meyer, D. & Sorkin, R. D. (1987). "Space-time as a causal set." *Phys. Rev. Lett.* 59, 521 — causal-set theory (discrete order + counting).
- Benincasa, D. M. T. & Dowker, F. (2010). "The Scalar Curvature of a Causal Set." *Phys. Rev. Lett.* 104, 181301 — the discrete (Benincasa–Dowker) action.

**Determinism and the status of randomness (§6, §6a).**

- de Broglie, L. (1927); Bohm, D. (1952). "A Suggested Interpretation of the Quantum Theory in Terms of 'Hidden' Variables. I & II." *Phys. Rev.* 85, 166 & 180 — pilot-wave theory.
- Everett, H. (1957). "'Relative State' Formulation of Quantum Mechanics." *Rev. Mod. Phys.* 29, 454.
- Bell, J. S. (1964). "On the Einstein Podolsky Rosen Paradox." *Physics* 1, 195 — the local-hidden-variable no-go.
- 't Hooft, G. (2016). *The Cellular Automaton Interpretation of Quantum Mechanics.* Springer. arXiv:1405.1548.

**Empirical anchors (§8).**

- Abbott, B. P. et al. (LIGO Scientific & Virgo Collaborations) (2017). "Gravitational Waves and Gamma-Rays from a Binary Neutron Star Merger: GW170817." *Astrophys. J. Lett.* 848, L13 — `|v_GW − c|/c < 10⁻¹⁵`.
- Park, R. S. et al. (2017). "Precession of Mercury's Perihelion from Ranging to the MESSENGER Spacecraft." *Astron. J.* 153, 121 — measured `42.98 ± 0.04″/century`.

Welcome to Universal Relativity.
