# Active-Inference Mathematics

**A mathematical system with active inference built into its foundation.** For the part of mathematics that has a physical or agent-constructible referent — what we will call **"not mathematical fantasy"** — QLF is a candidate replacement for ZFC and a candidate Theory of Everything. Not classical mathematics (ZFC's incompleteness and Busy Beaver independence rule out "all mathematics" as a coherent scope), not standard constructive mathematics (no agent) — a third thing: the math that an agent inside a Markov blanket constructs by free-energy-minimizing pruning of its possibility tree, where every admissible step is a half-spin ZFA closure carrying exactly `log 2` nats of resolved information.

This document is the meta-level entry point to QLF's mathematical foundations. Specialized derivations live in their own docs; this one names the system, fixes its primitives, states its single rule, and inventories what's been done with honest scoping (derived / partial / open).

## 1. The framing

Classical mathematics (ZFC) takes propositions to be true or false in a static platonic universe. Standard constructive mathematics (Bishop, Martin-Löf, Coquand) takes propositions to be proved or unproved by terminating algorithms. QLF takes a third view:

**Propositions are admissible trajectories of a free-energy-minimizing agent.**

The agent is a Markov blanket (in the [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) sense). The trajectory is a sequence of ZFA closures. The free-energy minimization is the per-event `ΔF = −log 2` saturation derived in [MRE.md §2.1](MRE.md). The proposition is "the trajectory exists in the possibility tree the blanket can integrate."

This is mathematics with **active inference built in**. For the part of mathematics that has a physical / agent-constructible referent — what §6.1 defines as "not mathematical fantasy" — QLF is a candidate foundation that replaces ZFC.

| | Classical (ZFC) | Constructive (BISH/CIC) | **Active-inference (QLF)** |
|---|---|---|---|
| Truth value | Platonic | Provable by terminating algorithm | **Admissible trajectory in possibility tree** |
| Agent / observer | None | None | **Markov blanket inside every closure** |
| Selection principle | Logical consequence | Termination | **Per-event ΔF = −log 2 saturation** |
| Boundary | Universal | Universal | **Observer-relative; emerges with the math** |
| Math object | Set | Computable term | **Half-spin ZFA closure (Hermitian pair)** |
| Continuum | Postulated | Built from Cauchy/Dedekind | **Statistical shadow of finite closure ensembles** |
| Infinity | Completed | Approximable, never realised | **Emergent — only finite closures survive** |
| Probability | Added (measure theory) | Added | **Intrinsic — Born rule derived from path-counting** |
| Information | Added (Shannon/von Neumann) | Added | **Per-atom `log 2` quantum, built in** |
| Proof style | Often non-constructive | Constructive | **Mechanizable in Lean 4; RCA₀ floor** |

## 2. Primitives

Three primitives suffice:

1. **The 8-twist alphabet** `{^, v, <, >, /, \, +, -}` — generative kernel for all admissible structures ([eight-twists-sufficiency.md](eight-twists-sufficiency.md), [QuCalc.md](QuCalc.md)). Higher dimensions and richer geometries are not added; they emerge from parallel composition (`|`) of strings in this alphabet.

2. **ZFA closure** — count balance ∧ Pauli closure ([Experimental_Consistency.md §2.1](Experimental_Consistency.md)). The 8-twist algebra has a Pauli structure (the Σ₈ generators of [Lagrangian_Formulation.md](Lagrangian_Formulation.md)); ZFA selects sequences whose matrix product folds to a scalar (the Pauli group elements `{±I, ±iI}`) AND whose pos/neg counts balance.

3. **The Markov blanket** — topological boundary screening internal free-action deficits ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md)). Every agent in QLF is a Markov blanket at some scale; every Markov blanket is a closed ZFA loop with internal admissible compositions and external causal-frontier exposure.

No axiom of choice. No appeal to large-cardinal infinities. No assumed continuum. Just discrete sequences over a finite alphabet, a single closure rule, and the boundary that separates "internal admissible composition" from "external causal frontier."

## 3. The single rule

**Every event in QLF is a half-spin ZFA closure** — a Hermitian-conjugate-paired sequence whose Pauli matrix product folds to a scalar element of the Pauli group. The minimal such closure is a 4-twist loop (`^v`, `<>`, `/\`, `+-`, or their compositions like `^<v>`); larger structures are parallel compositions.

The closure event carries information `D_KL(q ‖ p) ≤ log 2`, saturated only at the 50/50 binary partition ([MRE.md §2.1](MRE.md)). Each closure therefore:

- Reduces the agent's free energy by exactly `−log 2` nats (the per-event quantum derived in [Hierarchical_Control.md §3](Hierarchical_Control.md))
- Selects one of two equally-weighted possibility-tree branches (the [Born_Rule.md](Born_Rule.md) probability assignment)
- Folds to `−I` in the Pauli group, contributing the −1 phase of a fermion 360° rotation (the spin-statistics origin per [Spin_Statistics.md](Spin_Statistics.md))
- Conserves information bit-for-bit across creation and annihilation ([MRE.md](MRE.md) ↔ [Annihilation.md](Annihilation.md), [Conservation.md §6](Conservation.md))

**Numerical anchor:** the `−log 2` per-closure decrement is verified numerically in `active_inference_vfe_demo.py`: all 4 Hermitian-conjugate pair types produce ZFA closure in both orderings (all 8 sequences fold to `−I` in the Pauli group), the binary partition saturates `D_KL(q ‖ p) = log 2 ≈ 0.6931` nats per closure event, and the brute-force enumeration of all 4-twist sequences shows 168 of 4096 candidates achieve ZFA closure with cumulative `ΔF = −2 log 2` per atom.

This is the math's selection principle. A trajectory is admissible iff every step is a half-spin ZFA closure. The 1/2-spin atom is one principle (half-spin Hermitian closure) decomposed into three algebraic faces — set-theoretic minimality, algebraic Pauli closure, information-theoretic MRE saturation — all three are projections of the same bra-ket-of-a-spin-1/2-spinor structure, not independent constraints that happen to coincide ([HALF-SPIN-ZFA-EMBEDDING.md §3a](HALF-SPIN-ZFA-EMBEDDING.md)). **That spinor-structure claim is itself now machine-verified — and it is what makes the atom carry exactly one bit.** The two-valued spinor alphabet `{+I, −I}` carries `binary_kl 1 (1/2) = log 2` while a *single-valued* (vector) object carries none (`binary_kl 1 1 = 0`), and the `2π` double-valuedness — the spinor's defining sign, `−I ≠ +I` — is reproven from the explicit rotation matrices (`spinor_double_valued_vector_blind`), grounding the spinor **Cartan** discovered in 1913 as the information atom ([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)). So the faces don't merely *share* the spinor structure — the spinor's two-valuedness **is why** the atom carries one bit and no less (*it from bit*, the abstraction realized by the ½-spin closure).

## 4. Mathematical objects as admissible trajectories

A mathematical object in active-inference mathematics is **a sequence of admissible closures that the agent can integrate into its Markov-blanket record**.

- A **number** is a stable closure with a specific length and ZFA signature.
- A **function** is a transformation between admissible closure ensembles.
- A **geometry** is a class of admissible trajectories under a specific compositional constraint ([Holographic.md](Holographic.md) projects 2-component QuCalc logic into 3D observable structure; [Langlands.md §2](Langlands.md) argues QLF can generate any geometry).
- An **equation** is the assertion that two closure trajectories yield the same Markov-blanket record.
- A **proof** is the explicit trajectory the agent traverses; in Lean this becomes a mechanically checkable term in RCA₀ (or higher if the bridge axiom is invoked).

The concrete *emergence ladder* — how the integers, the ring operations (`+` = parallel, `×` = sequence), the unit group `μ₄ = (ℤ[i])ˣ`, and the gauge Lie algebras fall out of counting closures and the two ways they compose (every rung already machine-checked), plus the resolution of the bootstrapping worry (the substrate generates; Mathlib renders; conservativity makes it non-circular) — is [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md).

Continuum mathematics, set theory, and standard analytic objects appear as **statistical shadows** of admissible trajectory ensembles in the large-N limit. The real line is the limit of discrete admissible closure densities; ζ is the analytic image of the QLF generating function under the Mellin transform ([ReverseMathematics.md §4](ReverseMathematics.md)).

## 5. Scoreboard — what has been done

Honest derived / partial / open inventory, matching the standard in [Standard_Model.md](Standard_Model.md):

| Result | QLF anchor | Status |
|---|---|---|
| **1/2-spin algebra (Pauli, Dirac)** | `tau_xy_product` etc. machine-verified | ✓ Derived |
| **Spin-statistics theorem** | parallel-vs-sequence composition; per-atom `−I` fold | ✓ Derived |
| **Hermitian conjugacy as duality** | `E + E^† ≡ ZFA` Lean-verified | ✓ Derived |
| **Per-event `log 2` quantum** | binary-partition info-gain bound; numerically verified in `active_inference_vfe_demo.py`; Lean-anchored as `zfa_closure_minimizes_free_energy` (saturation: delta-on-uniform = log 2) AND `binary_kl_uniform_lt_log_two` (strict bound: every non-delta recognition density on the uniform binary prior achieves strictly less) in `lean/QLF_FreeEnergy.lean` — half-spin closure uniquely maximises per-event information; and the two-valued spinor carries exactly one bit vs *zero* for a single-valued object (`spinor_double_valued_vector_blind`, the `2π` double-cover reproven from the rotation matrices after Cartan 1913, [`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)) | ✓ Lean-verified (both directions) |
| **Born rule** | path-counting + uniform prior on possibility tree | ✓ Derived ([Born_Rule.md](Born_Rule.md)) |
| **Conservation laws (energy / momentum / charge / information / CPT)** | 8-twist symmetries → conserved currents | ✓ Derived ([Conservation.md](Conservation.md)) |
| **No magnetic monopoles** | ZFA closure requires ∇·B = 0 | ✓ Lean-verified (`no_magnetic_monopoles`) |
| **Friston free energy principle** | each ZFA closure minimizes F by `log 2` | ✓ Derived ([Hierarchical_Control.md §3](Hierarchical_Control.md)) |
| **Hydrogen spectrum** | Bohr derivation in ZFA language; 0.053 % NIST match | ✓ Derived ([Hydrogen.md](Hydrogen.md)) |
| **Maxwell field operators** | per-axis Pauli mapping; Lean-verified ∇·B = 0 | ✓ Derived ([Maxwell.md](Maxwell.md)) |
| **Photon as joint ZFA handshake (relational, not projectile)** | Hermitian-conjugate pair across two causal diamonds; null logical loop; no in-flight state | ✓ Derived ([Collective_Electrodynamics.md §2](Collective_Electrodynamics.md)) |
| **Delayed-choice quantum eraser without retrocausality** | half-closure at signal detector + half-closure at idler detector = one joint ZFA event; no preferred temporal order | ✓ Derived ([Delayed_Choice_Eraser.md](Delayed_Choice_Eraser.md)) |
| **No decoherence (universal coherence)** | `decoherence_impossibility` Lean-verified | ✓ Derived ([Decoherence.md](Decoherence.md)) |
| **Atomic shells (s, p through Z = 10)** | Pauli-blocking + orthogonal-axis routing | ✓ Derived ([Atom.md](Atom.md)) |
| **Combinatorial closed form (5ⁿ+3ⁿ)/2 for resonant sum** | binomial expansion separation | ✓ Derived ([Riemann-Conjecture-Proof.md](Riemann-Conjecture-Proof.md)) |
| **Riemann Hypothesis** | conditional on the bridge axiom; MRE motivation stated | ⚠ Conditional ([ReverseMathematics.md §4](ReverseMathematics.md)) |
| **Langlands correspondences** | bottom-up scaffolding; specific dictionary in §3 | ⚠ Scaffolding ([Langlands.md](Langlands.md)) |
| **Cosmological matter dominance** | residual-clustering of LH/RH topology | ⚠ Qualitative ([CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md), [Annihilation.md §5](Annihilation.md)) |
| **Cosmic expansion / age** | ZFA event rate as cosmic clock | ⚠ Order-of-magnitude ([AgeOfUniverse.md](AgeOfUniverse.md)) |
| **Standard Model gauge groups (SU(3), SU(2), U(1))** | structural sketch; U(1) derived, others open | ⚠ Partial ([Standard_Model.md](Standard_Model.md)) |
| **Quantitative mass spectrum** | atomic-system masses (positronium, muonium, hydrogen) as the QLF observables per [`Bound_States_QLF.md`](Bound_States_QLF.md); per-qubit mass quantum `m_qubit c² = ℏω = E_Planck / R_qubit` per [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md); per-bit photon energy per [`Photon_Energy_Bits.md`](Photon_Energy_Bits.md); unifying Wheeler-Fields `ℏω = 1 bit at frequency ω` derivation from QLF first principles per [`Information_Energy_Equivalence.md`](Information_Energy_Equivalence.md); **nuclear magic-number sequence `2, 8, 20, 28, 50, 82, 126` derived end-to-end** via vacuum-as-intruder + ℓ = 3 threshold from the 8-twist alphabet's 6+2 split per [`Magic_numbers.md`](Magic_numbers.md) | ⚠ Structure derived (per-qubit principle reproduces all measured mass ratios exactly; Wheeler-Fields equivalence derived from per-event log 2 + per-event ℏω; magic-number sequence derived from vacuum-coupling structure); first-principles `R_e` derivation still open |
| **CKM / PMNS mixing angles** | chirality rotation between generations | ✗ Open |
| **Lorentz covariance of EM at all scales** | τ_i = iσ_i algebra suggests path | ✗ Open |
| **Full nonlinear GR (continuum curvature bridge)** | discrete→continuum; Mercury + Λ closed, GW linearized wave equation `□_d δρ=0` anchored | ✗ Open (nonlinear) |
| **CKM/PMNS, sterile neutrino, dark sector** | no quantitative prediction | ✗ Open |

**Summary**: roughly 13 derived, 4 partial/conditional, 7 fully open. Same intellectual-honesty standard as [Experimental_Consistency.md](Experimental_Consistency.md). Results stated as "admissible trajectories the framework supports" rather than as "theorems of QLF" — RH conditional on the bridge axiom, Langlands as constructive scaffolding, Standard Model gauge identifications as open work.

## 6. Why the substrate believes the Millennium conjectures — the active-inference justification

The scoreboard (§5) lists the Millennium results as *conditional on a bridge axiom*. The active-inference
reading supplies the reason those conjectures should be **true** — not a discharge (the bridge stays the
formal boundary, [`Open_Problems.md`](Open_Problems.md) §"Axiom dischargeability"), but an account of *why*
the substrate side holds and why the bridge should.

**The one principle.** An active-inference agent only ever **actualises** structures that are **balanced**
(`H = H†`, self-dual), **finite-cost** (terminating, finite free energy), and **constructible**. ZFA closure
*is* that filter — `zfa_closure_minimizes_free_energy` (`ΔF = −log 2`,
[`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)); `qlf_universality` (terminating ⟺ ZFA);
`full_zeno_prune` (the non-terminating tail is never realised). And **each Class A conjecture, in QLF's
reformulation, asserts exactly one of those closure conditions on the realised structure.** So the
conjecture is true on everything the substrate constructs; a counterexample would have to be an
*unconstructed* object — an unbalanced closure, an infinite-free-energy history — which active inference
never actualises.

| Conjecture | The closure condition it asserts | Why active inference enforces it |
|---|---|---|
| **Riemann** (Re = ½) | zeros on the self-dual `H↔H†` line | the critical line is the **MRE-saturating (max-entropy) prior** `½` (`mre_prior_is_critical_line`); only balanced, self-adjoint modes are inferred — a zero off the line is an unbalanced closure never realised |
| **Yang–Mills gap** | a positive minimal excitation energy | one closure costs at least one bit, `log 2` (`gaugeMassGap`); no inference step is cheaper, so the lightest excitation has positive mass |
| **Navier–Stokes** (no blow-up) | realised flows stay smooth | a singularity = a non-terminating history = unbounded free-energy debt = **pruned** (`full_zeno_prune`); vorticity is capped at one quantum per Planck cell (`planck_caps_vorticity`) |
| **P vs NP** (generate ≠ verify) | search is not recognition | to **verify** is one closure-recognition (perception, O(n), `realized_is_verify_filter`); to **generate** is active-inference *search* over the branching tree (`C(2n,n)`) — the perception-vs-action asymmetry |
| **BSD** (rank = ord) | two counts of one closure agree | arithmetic rank and analytic order are two **perspectives** on one closure's central multiplicity (the `H↔H†` modularity mirror); one object counted two ways |
| **Hodge** (Hodge = algebraic) | realisable = algebraic | Hodge classes **are** the substrate-realised closures (proven, `hodge_realized_on_substrate`); the substrate only actualises what an agent can construct, and a constructed cycle is algebraic |

**Why they are hard classically — and immediate here.** The classical continuum frame has **no selection
principle**: it treats every continuum object as equally real, so it cannot see that the would-be
counterexamples are exactly the **non-realisable** (non-inferred) structures. The active-inference substrate
has the selection principle built in (active inference = ZFA closure), so it **constructs the answer**
instead of searching for a proof of it — the "physics keeps solving math" pattern
([`TheContinuum.md`](TheContinuum.md)): the inferential substrate *knows* the theorem because the theorem
is its own closure condition; the difficulty lives only in the classical rendering that dropped the agent.

**Honest scope.** This justifies why the **substrate side** of each conjecture is true and why the bridge
*should* hold (the continuum is a faithful rendering of what active inference constructs). It is **not a
discharge** of the Class A bridge axioms — proving them in the classical frame still *is* solving the
problem ([`Open_Problems.md`](Open_Problems.md) §"Axiom dischargeability"). What the active-inference view
supplies is a **principled reason to believe**: the conjectures are the fixed-point / free-energy-minimising
conditions of the construction, not free parameters.

---

## 7. Scope and clarifications

- **A candidate Theory of Everything, for the part of physics that is not mathematical fantasy.** The scoreboard in §5 lists 13 derivations of major physical principles (spin algebra, conservation laws, Born rule, Maxwell, Hydrogen, atomic shells, Friston FEP, no-magnetic-monopoles), 4 conditional results (RH, Langlands, SM gauge groups, cosmological matter dominance), and 7 open quantitative items (mass spectrum, mixing matrices, dark sector, gravitational waves). That structural balance — major principles derived plus a programme for the quantitative open items — is exactly the status any candidate TOE can honestly claim. We do not claim closed quantitative agreement on every open item; we claim the framework is the right foundation for getting there. See [Experimental_Consistency.md](Experimental_Consistency.md) for the empirical status.
- **A replacement for ZFC, for the part of mathematics that is not mathematical fantasy.** ZFC was shown incomplete by Gödel and indecisive by the Busy Beaver result; the sentences it cannot decide are precisely those whose objects have no admissible-trajectory referent. Active-inference mathematics declines to import them. For mathematics whose objects correspond to admissible Markov-blanket trajectories — the math of physical and agent-constructible reality — QLF is the proposed foundation. Standard constructive mathematics (Bishop / Martin-Löf / Coquand) is the closest neighbour and shares the constructive-realisability discipline; QLF adds the active-inference selection principle on top (§3). See §7.1 below for the precise definition of "mathematical fantasy."
- **Not Wolfram-style "everything is computation."** QLF's selection principle is specific (ZFA + MRE saturation); it is not the assertion that anything computable is real. The pruning is structurally enforced, not stipulated by an external Ruliad.
- **Not a denial of Platonism.** It's a relocation: mathematical truth still has structure; that structure is the admissible-trajectory space under active-inference selection. Whether this space is "Platonic" is a separate philosophical question ([Philosophy.md](Philosophy.md), [possibilist-ontology.md](possibilist-ontology.md)).

### 7.1 What "mathematical fantasy" means

The qualifier "for what is not mathematical fantasy" deserves a precise reading. Two well-established results pin it down.

**Gödel's incompleteness theorems (1931).** ZFC, if consistent, cannot prove its own consistency, and there exist true arithmetic sentences ZFC cannot prove. The unprovable sentences are constructed by self-reference — they have no concrete admissible-trajectory referent.

**Busy Beaver independence (Aaronson–Yedidia 2016, Riebel 2023).** The Busy Beaver function `BB(n)` is total and definite on ℕ. Yet there is an explicit 745-state Turing machine whose halting status is independent of ZFC — so `BB(745)` is a perfectly well-defined natural number that ZFC cannot pin down. The indecision is in the foundation, not in the function.

Both results expose what ZFC permits but cannot constructively access: uncountable choice, large-cardinal escalations, non-constructible reals, definite-but-undecidable values. QLF's active-inference selection rules out admitting any of these unless they correspond to an admissible Markov-blanket trajectory. The mathematics of half-spin ZFA closures, Pauli-group folds, conservation laws, the Born rule, Friston free-energy minimization, and the Riemann zeros under the bridge axiom all sit on the admissible side. The mathematics of `BB(745)`, of the continuum hypothesis, of the axiom of choice in its strong forms, sits on the fantasy side.

"Mathematical fantasy" is therefore not a derogation — it is a precise scope marker. The claim is that QLF is the right foundation for the non-fantasy half. Where ZFC could not decide, QLF correctly identifies "no admissible trajectory" and stops; where ZFC was indifferent to physical realisability, QLF supplies the active-inference selection principle that picks out the physically realisable trajectories.

## 8. Open work

- **Lean formalization** of `Active_Inference_Selection` as a unified principle: every admissible RhoProcess minimises a per-event free-energy functional. The per-event quantum is anchored — `zfa_closure_minimizes_free_energy` in [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean) — and the closure structure of admissible processes is anchored — `rho_process_always_zfa`, `bra_ket_always_balanced`, `decoherence_impossibility`. The remaining work is the *selection-rule* statement that ties them: every constructible RhoProcess is the trajectory of an agent minimising the per-event KL divergence. The candidate unifying statement is articulated as the vacuum-alignment principle in [`VacuumEnergy.md`](VacuumEnergy.md) §6.3 — *admissible signals are those that maximise mutual information with the vacuum's prior subject to ZFA closure* — and is fully Lean-anchored across three layers: per-event `vacuum_alignment_selects_zfa` and trajectory-level `global_alignment_selects_zfa` in [`lean/QLF_VacuumAlignment.lean`](lean/QLF_VacuumAlignment.lean), plus the **RhoProcess bridge** `rho_process_alignment_saturates` in [`lean/QLF_RhoProcessBridge.lean`](lean/QLF_RhoProcessBridge.lean). Together with `rho_process_always_zfa` from RhoQuCalc.lean, this completes the formal link: the QLF constructible processes are exactly the trajectories of agents maximising cumulative mutual information against the vacuum prior subject to ZFA closure.
- **Discharge the bridge axioms** flagged across [Riemann-Conjecture-Proof.md](Riemann-Conjecture-Proof.md), [Langlands.md](Langlands.md), [Standard_Model.md](Standard_Model.md), [Quantum_Gravity.md](Quantum_Gravity.md). Each is a specific WKL₀-level claim with an MRE-saturation motivation ([ReverseMathematics.md §4](ReverseMathematics.md)).
- **Quantitative match** against the open items in §5 — mass ratios, mixing matrices, dark sector, gravitational tests.
- **Categorical embedding** — express active-inference mathematics as a category whose objects are admissible trajectories and whose morphisms are ZFA-preserving compositions. Would tie the framework to homotopy type theory and to Friston's own category-theoretic FEP formulation.

## References

### Foundations (internal)

- [Philosophy.md](Philosophy.md) — possibilist ontology; ZFA as the sole selection principle
- [possibilist-ontology.md](possibilist-ontology.md) — explicit ontological framing
- [eight-twists-sufficiency.md](eight-twists-sufficiency.md) — universal generation from the 8-twist alphabet
- [HALF-SPIN-ZFA-EMBEDDING.md](HALF-SPIN-ZFA-EMBEDDING.md) — spin-1/2 set-theoretic embedding
- [MRE.md](MRE.md) — per-event `log 2` quantum
- [Hierarchical_Control.md](Hierarchical_Control.md) — Friston FEP derivation
- [Related_Frameworks.md](Related_Frameworks.md) — where ZFA sits vs. Friston's FEP and the other information-theoretic / discrete-substrate neighbors (the FEP is the *statistical shadow* of the exact closure rule, not a rival)
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — Markov blanket as topological boundary
- [active_inference.md](active_inference.md) + [BayesianMechanics.md](BayesianMechanics.md) — agent-side framing
- [ReverseMathematics.md](ReverseMathematics.md) — RCA₀ floor; bridge axioms at WKL₀
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — Σ₈ algebra; ℒ = 0 variational principle
- [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) — `E + E^† ≡ ZFA`
- [Universality.md](Universality.md) — QLF generates all terminating finitely-encoded computations

### Specialized derivations (internal)

- [Born_Rule.md](Born_Rule.md), [Measurement_Problem.md](Measurement_Problem.md), [Decoherence.md](Decoherence.md), [Conservation.md](Conservation.md), [Spin_Statistics.md](Spin_Statistics.md), [Entanglement.md](Entanglement.md), [Annihilation.md](Annihilation.md), [Maxwell.md](Maxwell.md), [Collective_Electrodynamics.md](Collective_Electrodynamics.md), [Delayed_Choice_Eraser.md](Delayed_Choice_Eraser.md), [Hydrogen.md](Hydrogen.md), [Atom.md](Atom.md), [Quantum_Gravity.md](Quantum_Gravity.md), [Standard_Model.md](Standard_Model.md), [Riemann-Conjecture-Proof.md](Riemann-Conjecture-Proof.md), [Langlands.md](Langlands.md), [Experimental_Consistency.md](Experimental_Consistency.md)

### External

- Friston, K. (2010). *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience 11, 127–138.
- Friston, K. (2019). *A free energy principle for a particular physics.* arXiv:1906.10184.
- Bishop, E. (1967). *Foundations of Constructive Analysis.* McGraw-Hill — classical constructive math.
- Martin-Löf, P. (1984). *Intuitionistic Type Theory.* Bibliopolis.
- Coquand, T., Huet, G. (1988). *The Calculus of Constructions.* Inf. Comput. 76 — type theory foundation.
- Friedman, H. (1975). Reverse Mathematics program — RCA₀ / WKL₀ / ACA₀ hierarchy.
- Gödel, K. (1931). *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I.* Monatshefte für Mathematik 38, 173–198 — first incompleteness theorem.
- Aaronson, S., & Yedidia, A. (2016). *A relatively small Turing machine whose behavior is independent of set theory.* Complex Systems 25, 297–328 — explicit 7918-state TM with ZFC-independent halting.
- Riebel, J. (2023). *The undecidability of BB(748).* Bachelor's thesis, U. Erlangen-Nürnberg — refined the Aaronson–Yedidia construction to 748 states; the bound has since been tightened to 745.
