# Completeness Evidence — what supports "only ZFA is happening," and how strongly

**Status:** Evidence ledger, not a proof. This document assembles the case that ZFA closure is the sole substrate of the possibilist universe, **typed by evidential strength**, with the misses listed beside the hits and the defeaters named. It replaces the one-line completeness claim in [`Open_Problems.md`](Open_Problems.md) ("quantum computation is the standing experimental verdict...") with a version every clause of which survives a hostile reader.

**Companion documents:** [`Universality.md`](Universality.md) (the logical-sufficiency pillar), [`Open_Problems.md`](Open_Problems.md) (the gap registry this feeds).

---

## 0. Two claims, kept separate

- **Sufficiency** — ZFA + rational-interval rendering (§2a: measurement outcomes are counts, never reals) accounts for everything observed; no *missing* ingredient.
- **Exclusivity** — ZFA is the *only* thing happening; no *additional* ingredient, and no rival substrate fits equally well.

Evidence for one is not automatically evidence for the other. Most of what follows supports sufficiency directly; exclusivity is supported only by the exclusion results (§4) and would be *established* only by the reconstruction theorem (§6), which does not yet exist. Conflating the two is the single most common overclaim in completeness arguments, and this ledger is structured to make it impossible.

**Exclusivity is invariant-uniqueness, not implementation-uniqueness.** "ZFA is the *only* thing happening" (bullet 2) is a claim about the forced *correctness invariant* — the ZFA closure condition, the isomorphism class every coherent outcome lands on — **not** a claim that a unique substrate machine exists. Multiple realizability is expected and is *not* evidence against exclusivity: infinitely many machines, algorithms, and generative paths compute the same ZFA-closed outcomes (Turing equivalence), and they *converge on* the ZFA invariant — which is the claim, not a problem for it. So "ZFA is correct" reads as *the forced fixed point*, not *a chosen formalism among many*. This is exactly why the reconstruction target (§6) is phrased "isomorphic **to** ZFA": the invariant is forced up to realization. The local, already-proven instance of "many realizations, one invariant" is `comparison_isomorphism` ([`QLF_Motives`](lean/QLF_Motives.lean)) — all faithful Weil realizations agree because they render the one substrate object. This clarifies *what* exclusivity claims; it does not upgrade its status — invariant-uniqueness in general remains the §6 conjecture.

## 1. Evidence typology (strongest first)

| Type | What it establishes | Ceiling |
|---|---|---|
| **T1 — Uniqueness theorems** | Any substrate satisfying the postulates *is* ZFA | Exclusivity, conditional on postulates |
| **T2 — Parameter-free overdetermination** | One structure fixes many independent measured values | Sufficiency; exclusivity by coincidence-cost |
| **T3 — Confirmed exclusions** | Predicted absences searched for and not found | Exclusivity, one rival class at a time |
| **T4 — Inherited no-go theorems** | Whole rival classes experimentally dead | Exclusivity against *added-ingredient* rivals only |
| **T5 — Consistency / universality** | ZFA passes necessary conditions | Neither — shared with all serious rivals |

A completeness claim resting only on T5 is rhetoric. [QLF](README.md)'s current position: strong T2, real T3 and T4, fragments of T1. The program is to climb the table.

## 2. T5 — Necessary conditions passed (non-discriminating; listed first to get the weakest out of the way)

**`qlf_universality`** ([`Universality.md`](Universality.md), [`lean/QLF_Universality.lean`](lean/QLF_Universality.lean)): ZFA generates every terminating finitely-encoded computation. Machine-verified, and **shared with every Turing-complete substrate** — cellular automata pass it too. It proves ZFA is *a* universal generator, not *the* substrate. Weight accordingly: a condition whose failure would kill the theory, whose success discriminates nothing.

**Quantum-computational consistency** (weak half): all exact reconstructions of quantum logic — ZFA, Bohm, Everett — predict identical QC behavior. Perfect answers confirm the equivalence class, not the member. The strong half of the QC evidence is in §4.

**Sufficiency gap, stated plainly:** even the sufficiency direction is only half-theorem. `qlf_universality` proves every terminating computation has a surviving closure encoding; "every *physical event* is such a closure" currently rests on `full_zeno_prune` as posited structure. The connecting theorem is open.

## 2a. The rendering obligation is to ℚ-with-intervals, not to ℝ

A correction that makes the ledger *stronger*, not weaker. It is tempting to state QLF's burden as "render the substrate into the continuum-valued observables physics reports." That concedes far too much, because **no measurement has ever produced a real number.** Every outcome is a finite object — detector counts, cycle counts, a terminating decimal with an error interval. `α⁻¹ = 137.035999206(11)` is a *rational plus a rational interval*, nothing more. Since the 2019 SI redefinition this is explicit all the way down: the units are fixed by exact stipulated integer-valued constants and measurement is *counting against them* — frequency metrology, the most precise measurement humans perform, is literally integer cycle counting. Uncomputable reals are not merely never measured; they are **unmeasurable in principle**, since any measurement protocol is a finite procedure. This is not a QLF thesis but a fact about metrology, and it has a sharp consequence: **the continuum never appears at the measurement interface** — so measurement was never evidence for it at all.

So the rendering obligation shrinks to its true size: **substrate → ℚ-with-intervals, not substrate → ℝ.** QLF owes rational approximants to audited precision (which [`pi_precision_demo.py`](pi_precision_demo.py) already delivers, and whose substrate origin is machine-checked in [`QLF_PiRational`](lean/QLF_PiRational.lean) — the census approximant `returnDensity n : ℚ` is `Real`-free by construction, `returnDensity 1 = 1/4`, `2 = 9/64`, `3 = 25/256`; and each load-bearing `(rational)·π` physics quantity is a proven rational enclosure, `43.982 < 14π < 43.983`, `25.132 < 8π < 25.133`, `6.283 < 2π < 6.284`) and nothing else. Reals in textbook notation are theorist shorthand; every *actual* computation ever run — QED loop integrals included — is finite arithmetic on rationals/floats, and measurement lives even lower, in counts. And counts are closure-receipt territory, which flips the burden:

> **Measurement is counting, and counting is what ZFA does natively — it is the continuum theories that owe a story for why every experiment terminates in an integer.**

This is the balanced-truth reading in miniature: the *balanced, finite, closing* object is the real one; the continuum-valued observable is the fantasy that never shows up when you actually look. Two things it does **not** touch, kept on the record so the concession is not overread: (i) the *translation* obligation for the Clay problem **statements** is about how those problems are written, not about measurement, and stays undischarged (§6, [`TheContinuum.md`](TheContinuum.md)); (ii) the guardrail holds — that measurement never touches the continuum shows ℝ is *empirically inert at the interface* (the fantasy charge), **not** that ℝ is inconsistent (consistency ≠ realizability, [`TheContinuum.md`](TheContinuum.md)).

## 3. T2 — Parameter-free overdetermination (the strongest existing evidence)

One structure — the 8-twist alphabet with its 6+2 split and the closure census — fixing many *independent* measured quantities with zero adjustable parameters:

| Quantity | Substrate origin | Agreement | Anchor |
|---|---|---|---|
| α⁻¹ leading value | 3² tensor, IR anchor; bounds 137 < α⁻¹ < 137.048; **cross-sector overdetermination joint** (dimension × bare-coupling × elementarity meet at 137, zero slack) | measured 137.036 inside the verified bounds; the leading value is a *machine-checked joint*, not a fit (`d` substrate-derived); **residual open** (reformulated as the #117 running-coefficient tower) | `QLF_AlphaBound`, `QLF_AlphaRigidity` |
| Ω_Λ | 2/8 of the alphabet | consistent | `electroweak_substrate_signature` |
| sin²θ_W (unification) | 3/8 spatial fraction | RG running to 0.231 **open** | `QLF_WeinbergAngle` |
| a₀ = cH₀/2π | closure-loop period, 2π derived | SPARC blind test, parameter-free, 0.133 dex floor | `QLF_MondScale`, `QLF_MondNu` |
| Koide Q = 2/3 | N=3 axes, A²=2 | m_τ to 0.006% (scale is input) | `QLF_Koide` |
| π | closure census, Wallis | derived by construction | `QLF_PhysicalPi` |
| ln R_p = 14π | b₀=7 from N_c=3, n_f=6 | 0.07% at the posit; **band ×15 in value** | `QLF_BetaFunction`, `QLF_AlphaS` |

**Why this bears on exclusivity at all:** each parameter-free hit multiplies the coincidence-cost of any rival substrate. No rival exact reconstruction of quantum logic (Bohm, Everett, bare Hilbert-space QM) delivers *any* of these numbers from its ontology. This is ZFA's positive discriminator within the surviving class of §4.

**And it is the quantitative case for Wheeler's *"it from bit."*** Every row is an *it* — a measured physical quantity — read out of the *bit* census (the ZFA closure count) with zero adjustable parameters. Wheeler's 1990 principle that every physical quantity derives from binary yes/no questions is usually a slogan; here it is a **ledger of derived numbers**, and its unit is no longer informal: the bit itself is a machine-verified object — the two-valued **½-spin closure** carrying exactly `log 2`, a single-valued object carrying none (`QLF_SpinorInformation`; the notions of information it grounds are mapped in [`Information_Physics.md`](Information_Physics.md)). So the overdetermination is evidence at **two levels at once**: that reality is *informational* (the its come from bits) and that the bit is *real and atomic* (a proven closure, not a posit). The finding and the ledger reinforce each other — a proven atom with a body of parameter-free consequences is stronger than either alone.

**The misses, at full weight (a selective ledger is how frameworks fool their authors):** the 137.036 residual; the entire value sector (couplings g₁,g₂,g₃, G_F, Higgs VEV, mixing angles, absolute masses); the hierarchy is a log-level reduction with a ×15 value band; H₀ is an input, and the Hubble-tension residual is **not numerically predicted** (QLF's structural stance — dynamical DE / non-ΛCDM, dark sector voting local, [`DarkMatter.md`](DarkMatter.md) §5a — is a *perspective + data vote*, not a derivation of the value). The overdetermination case is strong *because* it survives this column being written down.

## 4. T3 + T4 — Exclusions: how "only" gets evidence

Evidence that *only* ZFA is happening can only come from absences — extra ingredients leave traces, and the traces are searched for.

### 4a. Inherited no-go theorems (T4) — rival classes killed by others

There is no theorem "no hidden variables." There is a family, each killing a **named class**, premises stated:

- **Bell** — local hidden variables. Dead, loophole-free.
- **Kochen–Specker** — non-contextual value assignments. Dead.
- **PBR** — ψ-epistemic models (given preparation independence). Dead.

**What survives all three: Bohmian mechanics** (nonlocal, contextual). QLF documents must therefore never write "hidden variables are ruled out" without qualification — a referee reaches for Bohm immediately. The inherited result is precise: any rival that **adds** a local, non-contextual, or ψ-epistemic ingredient is experimentally dead.

**The objection QLF must pre-empt (write it before a critic does):** a substrate of definite twist histories superficially *looks like* a hidden-variable theory. The answer is that twist histories are not pre-assigned measurement values: only **closures** are receipts, and closure is **horizon-relative** (`closedAtHorizon`, [`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean)) — the same history reads open or closed depending on the observer's resolution. Measured values are receipt-relative, hence contextual; KS is satisfied *structurally*, not dodged. This paragraph is the doc's insurance policy.

### 4b. Quantum computation as an ongoing exclusion experiment (T3 — the strong half)

Error-corrected QC at increasing scale progressively falsifies the entire **deviation class** of rivals — objective-collapse dynamics (GRW/CSL), Penrose gravitational collapse — because those predict departures from unitarity growing with mass and complexity, and every verified large computation tightens their parameter bounds quantitatively. This is the defensible core of the old "standing experimental verdict" line, restated with its actual scope: **QC excludes rivals that deviate from quantum logic; it cannot distinguish among exact reconstructions** (§2).

The ZFA-specific bonus: certified answers (factoring — the factors multiply or they don't) demonstrate the substrate executing **exact discrete logic** through amplitude machinery — closure-as-integer-receipt behavior — and Clifford-circuit exactness lives on the ℤ[i] lattice ([`QLF_StateSpace`](lean/QLF_StateSpace.lean)) with no continuum invoked.

### 4c. ZFA's own exclusion predictions (T3) — each a named defeater

| Prediction of absence | Anchor | Defeater (what kills ZFA-only) |
|---|---|---|
| No cosmological α drift | `no_cosmological_drift_of_alpha` | Confirmed α drift |
| θ̄ = 0 with **no axion** | `theta_zero_on_closure` | Axion detection |
| Neutrino Majorana → 0νββ exists (ν₁ only) | `neutrino_majorana`, `one_axis_majorana` | 0νββ signal at LEGEND-1000/nEXO reach (≳ 10 meV); m_ββ ≈ 0.25 meV expected |
| No exact global B−L | `QLF_BaryonWinding`, `QLF_Majorana` | Exact B−L conservation established |
| No blow-up in preparable NS flows | `realized_flow_is_stable` | Physically realized blow-up |
| QRNG streams match the ZFA-closure null | [`QRNG_Closure_Observatory.md`](QRNG_Closure_Observatory.md) | Predeclared-sieve deviation |
| No new-physics anomaly in muon g−2 | `QLF_MuonG2` | Confirmed anomaly surviving HVP settlement |

Every searched-and-absent row confirms exclusivity in the only way exclusivity can be confirmed. Every row is also a standing offer to lose. **A universality claim without this table is ideology; with it, it is science.**

## 5. The surviving rivals, and the second-stage argument

After §4, the survivors are exact reconstructions of quantum logic: **Bohm** (adds trajectories) and **Everett** (adds unrealized branches). No experiment inside quantum mechanics separates them from ZFA. (The full positioning against *all* the neighboring frameworks — selection-principle rivals and the information-mathematics QLF builds on — is [`Related_Frameworks.md`](Related_Frameworks.md).) The second stage is therefore argued on non-empirical but principled grounds:

1. **Uniform surplus-structure charge.** Bohmian trajectories and Everettian branches are empirically idle — no observation ever witnesses them — which is *exactly* the charge QLF levels at the continuum's impossible numbers ([`TheContinuum.md`](TheContinuum.md)). For the continuum that charge is now a **theorem**, not a slogan: the non-identifiable tail is a *defined uncountable set* of parameters no finite record can touch ([`Shannon_Overfit.md`](Shannon_Overfit.md) Theorem B, `tail_unconstrained`) — the fantasy tier as arithmetic. Applying the parsimony razor uniformly, ZFA carries no idle ontology: every closure is a receipt, every receipt is a closure. A framework that razors the continuum but tolerates idle trajectories would be inconsistent; QLF razors both.
2. **Constants overdetermination** (§3): the surviving rivals have no story for why α, a₀, sin²θ_W, Koide fall out of their ontology. ZFA does. Within an empirically tied class, explanatory yield is the tiebreaker.
3. **The reconstruction theorem** (§6): the only route to upgrading the tiebreaker into a theorem.

## 6. T1 — The missing keystone: the reconstruction theorem

The one result that would convert exclusivity from an argued position into mathematics:

> **Target.** State postulates, each characterized **without mentioning ZFA** — orthomodularity of the event lattice (Birkhoff–von Neumann), finite information capacity, closure-as-receipt, reversible logic with irreversible realization ([`QLF_Reversibility`](lean/QLF_Reversibility.lean)), no-disconnection — and prove: any event structure satisfying them is isomorphic to ZFA over the 8-twist alphabet.

Its contrapositive is the strongest honest form of "only ZFA": **anything other than ZFA breaks one of five named postulates.** Precedents set the shape and the standard: **Gleason** (the projection lattice forces the Born rule — the model for "the closure lattice forces ZFA realization"), **Solér** (orthomodularity + regularity forces Hilbert space over ℝ/ℂ/ℍ — the finite counterpart should force the ℤ[i] lattice, of which [`QLF_StateSpace`](lean/QLF_StateSpace.lean) is already a fragment), **Hardy/Chiribella** (operational axioms force QM), and **Bell** as the honor standard: few premises, each independently motivated, each experimentally attackable.

**Guardrails, non-negotiable:**
- *Non-circularity:* if "quantum logic" is defined as the logic of ZFA closures, the theorem is a tautology. Each postulate must be stated ZFA-free and must not be equivalent to the conclusion. (Von Neumann's no-go is the cautionary tale: valid, empty, one premise smuggled the conclusion.)
- *Attack surfaces:* each postulate ships with its violation signature — infinite-precision observable (capacity — its formal backing is [`Shannon_Overfit.md`](Shannon_Overfit.md): the negative of `no_real_received` *is* the capacity-violation signature, "an identifiable real exists"), unclosed-event residue (receipt — the QRNG target), non-orthomodular event lattice, etc.
- *The permanent ceiling:* that nature obeys the postulates is empirical, forever. The theorem can only ever be conditional. Its worth is the weakness and independence of its premises, not the grandeur of its conclusion.

**Existing fragments to build from.** Each of the five postulates now has a partial anchor in the verified layer — none is the theorem, but the method-in-miniature and each postulate's violation signature are in hand:

| Postulate (stated ZFA-free) | Fragment(s) in hand | Violation signature |
|---|---|---|
| **Finite information capacity** *(most developed)* | `no_real_received` + `tail_unconstrained` ([`QLF_ShannonOverfit`](lean/QLF_ShannonOverfit.lean)); `no_continuum_in_finite_region` ([`QLF_Realizability`](lean/QLF_Realizability.lean)); the `Real`-free census approximant `returnDensity : ℚ` ([`QLF_PiRational`](lean/QLF_PiRational.lean)) | an *identifiable real exists* (a finite record pinning a real to arbitrary precision) |
| **Closure-as-receipt** | horizon-relative closure `closedAtHorizon` ([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean)) — receipts are resolution-bounded, not a primitive yes/no | an *unclosed-event residue* (the QRNG target, `QRNG_Closure_Observatory.md`) |
| **Reversible logic, irreversible realization** | the reversibility capstone ([`QLF_Reversibility`](lean/QLF_Reversibility.lean)): time-reversal *is* the Hermitian-conjugate involution, forward closure many-to-one | an *injective* physical closure (a reversible macro-process) |
| **Orthomodularity of the event lattice** | the `ℤ[i]` state-ring / `μ₄` phase group ([`QLF_StateSpace`](lean/QLF_StateSpace.lean)); the Minkowski/Lorentz interval structure ([`QLF_Minkowski`](lean/QLF_Minkowski.lean)) | a *non-orthomodular* event lattice |
| **No-disconnection** | connectivity forces every state onto a swap orbit ([`Pointer_Swap_Fuzz.md`](Pointer_Swap_Fuzz.md) §1 — observables are swap-invariants only) | a *disconnected* (isolated) admissible state |

The **method in miniature** is `radialAccel_unique` (a physical law shown *unique* given the closure principle — exactly the shape "the postulates force the ZFA realization" must take at full scale) together with `disjunctive_closure` (the OR-fold that a closure *is*). The finite-capacity row is the session's contribution and the furthest along: its postulate, its two proven theorems, and its violation signature are all in place — the template for bringing the other four rows to the same state.

**The information-theoretic wing has a first executed fragment.** The reconstruction target has an information-measure sub-theorem — *the admissibility structure admits a **unique** consistent information measure* (the Baez–Fritz–Leinster / Knuth "structure forces the measure" move), and two of its rungs are now machine-checked. **Counting wing** ([`QLF_EntropyUniqueness`](lean/QLF_EntropyUniqueness.lean)): additivity on independent ledgers forces `H [] = 0` and `H s = |s|·c` — counting is determined, not chosen, with `c = log 2` — and any two consistent measures agreeing on the generators agree everywhere (`additive_unique`). **Lattice wing** ([`QLF_Reconstruction`](lean/QLF_Reconstruction.lean)): on the finite event lattice a measure additive over *orthogonal* decompositions is atom-determined and unique from its atom values, so the consistent measure on the closure lattice is forced. Both deliberately avoid Gleason's analytic difficulty. **Honest scope:** both are the finite/**Boolean** case (orthogonality = disjointness); the genuinely **Gleason**-hard content — a measure additive on a *non-distributive orthomodular* lattice (dim ≥ 3) being forced to `Tr(ρ·)` — plus the full distributional `−Σ p log p` uniqueness ([#115](https://github.com/jimscarver/quantum-logical-framework/issues/115)) and the postulates→ZFA isomorphism ([#118](https://github.com/jimscarver/quantum-logical-framework/issues/118)) remain open. These are the first *executed* fragments of the uniqueness half.

### 6a. The emergence forcing chain — how far the proof already reaches, and the retargeted goal

Separately from the postulates→ZFA *uniqueness* wing (§6 proper), there is a **forcing chain** from the bare premise — a possibilist, logically-consistent, finite-information realm — toward ZFA structure, several of whose links are *already proven theorems*. It is assembled reuse-only in [`QLF_EmergenceChain`](lean/QLF_EmergenceChain.lean):

1. **Discreteness is forced.** A finite-information realm admits no injection from an infinite state space, so no continuum is realized (`no_continuum_in_finite_region`, [`QLF_Realizability`](lean/QLF_Realizability.lean); `realized_realm_discrete`). The realized realm is discrete — **proven**.
2. **Structure ⟹ signed distinctions.** Any structure at all needs distinguishable elements — a first distinction and its conjugate — i.e. a signed alphabet with an involution. (Near-analytic — "there is structure at all" — rather than a Lean theorem.)
3. **Balanced closure ⟹ the algebra.** Every count-balanced history folds to a fold-target element (`count_balanced_pauli_closed`, [`QLF_TwistAlphabet`](lean/QLF_TwistAlphabet.lean); `closure_folds_to_scalar`) — the closure condition *forces* the algebraic invariant, it is not posited. **Proven.**
4. **The fold-target IS `μ₄ = ℤ/4`.** The fold multiplication carries to `ℤ/4` addition (`toZMod_hom`), faithfully (`toZMod_injective`, [`QLF_AlgebraEmergence`](lean/QLF_AlgebraEmergence.lean); `foldTarget_is_mu4`) — derived from the fold, not imported; su(2)/su(3) follow from the commutators. **Proven.**

`emergence_chain` bundles links 2–4: *any balanced closure folds to an element of the cyclic group `μ₄`, which the fold multiplication realizes as `ℤ/4` addition, faithfully.* So the ZFA closure **invariant** — discreteness + balanced closure + its `μ₄` algebra — emerges by construction.

**The retarget (why this changes the §6 goal).** Under the invariant-vs-machine framing (§0), "ZFA *will* emerge in a possibilist logical realm" should mean *the closure **invariant** is forced* — not *the 8-twist **machine** is the unique substrate*. Those are different bars: the invariant sits at the end of the mostly-proven chain above, whereas machine-uniqueness is neither proven nor, by multiple realizability, the right thing to demand (many alphabets realize one invariant; `comparison_isomorphism` the proven local instance). So the reconstruction goal (§6) is properly stated as **uniqueness of the invariant**, and `QLF_EmergenceChain` is its proven *necessary-condition* spine. **The open residue is exactly two hard steps:** *why this alphabet* (the 8-twist / 6+2 split as forced — [#116](https://github.com/jimscarver/quantum-logical-framework/issues/116), α-rigidity) and the **Gleason-hard uniqueness** of §6 (dim ≥ 3, non-distributive orthomodular). The chain does not close these; it shows the necessary conditions are met and names the residue precisely.

### 6b. The five postulates collapse into the one postulate

The §6 target is usually stated over **five** ZFA-free postulates — orthomodularity, finite information capacity, closure-as-receipt, reversible logic with irreversible realization, no-disconnection. But they are **not five independent axioms.** Read against the one postulate — *physical reality is the finite, self-consistent (closing) subset of logical possibility* — four of them reduce, leaving essentially **one-and-a-half**. Anchored (the two proven rungs) in [`QLF_PostulateReduction`](lean/QLF_PostulateReduction.lean):

- **Finite information capacity — a *component* of the one postulate** (its "finite" clause), not independent; and it forces discreteness (`finite_capacity_forces_discreteness`, reusing `no_continuum_in_finite_region`). **Proven.**
- **Closure-as-receipt — the *selection* clause restated** ("what is real is what closes"); definitional, not independent.
- **Reversible logic with irreversible realization — DERIVED, not assumed.** The reverse is the *involutive* dagger (distinctions carry their conjugate ⟹ `H↔H†`) and the forward closure is *many-to-one* (`C(2n,n) ≥ 2` histories per closure): `reversible_logic_irreversible_realization` (reusing `time_reverse_involutive_but_closure_degenerate`, [`QLF_Reversibility`](lean/QLF_Reversibility.lean)). **Proven** — the one fully-derived rung.
- **No-disconnection — *plausibly derivable*** from the relational nature of closure (a fully disconnected event closes with nothing, so it is never selected; `reachable`/`SharedClosure`, `QLF_ReachableEvent`). Stated, not yet a Lean theorem — the weakest of the reductions.
- **Orthomodularity — the genuine residue, and half-free.** The *orthocomplement* comes for free from the dagger involution (the reversibility rung); only the orthomodular *law* (the specific weakening of distributivity, Birkhoff–von Neumann) is the Gleason-hard content the one postulate does not visibly force.

So the reconstruction target collapses from "five postulates ⟹ ZFA" to

> **the one postulate + the orthomodular law ⟹ ZFA (up to isomorphism)**

with even the orthocomplement half of that supplied by the dagger. The honest open frontier is exactly two things: **(a) the orthomodular law** (why the closure lattice is orthomodular, not merely orthocomplemented) and **(b) the Gleason-hard uniqueness** (the §6 residue, `QLF_Reconstruction` has only the Boolean wing). **Honest scope:** this is a *reduction of the target*, not its closure — four postulates and a half evaporate into the one; the residue (a + b) is not derived. The tiering is real (two rungs proven, one definitional, one plausibly-derivable, orthomodularity the residue).

### 6c. The orthomodular residue narrows too — proper involution + the projection-lattice bridge

Residue (a) — the orthomodular law — is not a monolith either. It **splits**, and the hard half turns out to live in the *rendering* layer, not the substrate core:

- **On the finite substrate core it holds trivially.** QLF's finite closure lattice (`QLF_Reconstruction`, orthogonality = disjointness) is **Boolean**, and every distributive lattice is orthomodular (distributive ⟹ modular ⟹ orthomodular). So the orthomodular law is free on the core — but this is the degenerate case; it does not touch the *quantum* (non-distributive) content.
- **The non-distributive content is a rendering-layer property, not a missing substrate axiom.** Genuine non-distributivity requires *incompatible* propositions — complementary observables with no common refinement, i.e. genuine superposition — which in QLF is precisely the **`T`-gate / magic / continuum-completion** side of [`QLF_StateSpace`](lean/QLF_StateSpace.lean) (the stabilizer/Clifford fragment is the computable core; non-distributivity appears only in the completion). So the hard orthomodular content sits in the *rendered continuum* layer — the same category as QLF's other continuum bridges (`benincasa_dowker_limit`, `yang_mills_continuum_gap`), not a substrate gap.
- **It reduces to one substrate fact + one identification.** The projection lattice of any Rickart/Baer `*`-ring with a **proper** involution (`x† x = 0 ⟹ x = 0`) is orthomodular (Kaplansky/Berberian). QLF's state space is the `ℤ[i]`-lattice with the dagger = conjugate-transpose ([`QLF_Minkowski`](lean/QLF_Minkowski.lean)'s `toMatrix_adjoint`), and that involution **is** proper — `M† M = 0 ⟹ M = 0` is positive-definiteness of the Gaussian-integer inner product, a provable substrate lemma. So residue (a) narrows to **(a1) the dagger is a proper involution** — **now machine-checked** (`substrate_dagger_proper`: `Mᴴ * M = 0 ⟹ M = 0` on the substrate matrices, [`QLF_ProperInvolution`](lean/QLF_ProperInvolution.lean), with the `Form` corollary `form_dagger_proper`) — plus **(a2) the event lattice IS that projection lattice** (a faithfulness identification), with the Baer-`*`-ring→orthomodular theorem the settled-math bridge Mathlib lacks assembled (an axiom-boundary of the `benincasa_dowker_limit` kind).
- **Structural reading — it is the one postulate again.** `a ≤ b ⟹ b = a ∨ (b ∧ a⊥)` says decomposing a proposition `b` relative to a weaker `a` into `a` and its orthogonal remainder **loses nothing** — the whole is conserved. That is **ZFA balance lifted to the proposition lattice**: orthomodularity is the lattice-level closure/conservation law, suggesting it too is a reading of the one postulate rather than an independent axiom.

**Net:** #118's residue is now **(a1) ✅ proven** (`substrate_dagger_proper`) **+ (a2) the projection-lattice bridge + (b) the Gleason-hard uniqueness** — proven on the Boolean core, the proper-involution fact machine-checked, the remainder reduced to named bridges. **Honest scope:** a *further narrowing*, not a derivation — a full Lean proof of the non-distributive orthomodular law still needs orthomodular-lattice machinery + the Baer-`*`-ring theorem that are not in Mathlib; (a1) landed is the substrate fact those bridges consume.

## 7. What this ledger licenses QLF to say

- **Licensed now:** "ZFA is sufficient for all audited observations; overdetermines constants parameter-free; all added-ingredient and deviation-class rivals are experimentally excluded; among surviving exact reconstructions ZFA is uniquely parsimonious and uniquely predictive of constants; exclusivity is conjectured, its defeaters are published (§4c), and its proof target is specified (§6)."
- **Not licensed:** "hidden variables are ruled out" (unqualified); "quantum computation proves the ontology is complete"; "nothing else can happen" (unconditional); any claim of exclusivity that survives the loss of a §4c row.

**Registry patch** (replaces the completeness paragraph in `Open_Problems.md`): *"Sufficiency is supported by parameter-free overdetermination (§3 here) and confirmed exclusions (§4c); Bell/KS/PBR exclude added local, non-contextual, and ψ-epistemic ingredients; error-corrected QC at scale progressively excludes deviation-class dynamics; among surviving exact reconstructions ZFA is distinguished by parsimony and constants overdetermination. Exclusivity is conjectured pending the reconstruction theorem (Completeness_Evidence.md §6). Defeaters: axion detection, α drift, 0νββ signal at LEGEND-1000/nEXO reach (≳ 10 meV), QRNG deviation."*
