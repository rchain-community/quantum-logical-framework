# Decoherence in QLF

**There is no decoherence in QLF.** What an observer calls "decoherence" is the Markov-blanket cutoff that filters fast micro-events incompatible with the observer's macro state. The underlying universe is fully ZFA-coherent at every closure; the appearance of classical behavior is a top-down constraint from the observer's blanket, not a physical process that destroys quantum information.

This document collects the threads scattered across [Measurement_Problem.md](Measurement_Problem.md) §4a, [Hierarchical_Control.md](Hierarchical_Control.md) §5, [Lagrangian_Formulation.md](Lagrangian_Formulation.md) (the Lean-verified `decoherence_impossibility`), [MRE.md](MRE.md), and [Annihilation.md](Annihilation.md) into a single statement about what decoherence is and is not.

## 1. The Lean-verified core: `decoherence_impossibility`

The starting fact, machine-verified in `lean/BraKetRhoQuCalc.lean`:

```
theorem decoherence_impossibility (p q : RhoProcess) :
  achieves_ZFA (toTopoString (RhoProcess.parallel p q))
```

Parallel composition of any two RhoProcesses produces a ZFA-balanced topology. Combined with `bra_ket_always_balanced` (it is algebraically impossible to construct a ZFA-unbalanced RhoProcess), this means:

**No physically constructible process can take a coherent quantum system into a decoherent classical state.** Decoherence as a fundamental physical process is **algebraically impossible** in the QLF framework.

This is in tension with the standard textbook picture in which decoherence is *the* mechanism by which quantum systems become classical. The resolution is that the textbook picture is **observer-relative**: decoherence appears in the description of a system from the viewpoint of an observer whose Markov blanket cannot resolve the full coherent state.

## 2. What an observer actually sees

A Markov-blanket-bounded observer ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md)) has access only to the slice of the universal history that crosses their causal frontier. Inside the blanket the observer can resolve fast micro-events at the local clock rate ([Frequency_Synchronization.md](Frequency_Synchronization.md), $\Delta t = R/f$). Outside the blanket the events happen but are not part of the observer's accessible state.

A coherent superposition that extends beyond the blanket boundary is **invisible** to the observer as a superposition; it appears instead as a probabilistic mixture, because the observer cannot track the off-diagonal phase coherences that cross the blanket. The off-diagonals are still there in the global state — they're just outside the observer's resolution.

This is the QLF reading of **environment-induced superselection** (the standard decoherence story): the "environment" is everything outside the observer's Markov blanket; "superselection" is the blanket's filter that drops off-diagonal terms. No physical process destroys the off-diagonals; the observer's representation simply doesn't include them.

## 3. Decoherence as top-down constraint

From [Hierarchical_Control.md](Hierarchical_Control.md) §5: "Decoherence from the top-down side — the Markov-blanket boundary's slow priors filter out fast micro-events incompatible with the macro state, producing classical-looking measurement outcomes."

In the bottom-up/top-down architecture:
- **Bottom-up (fast)**: every ZFA closure is fully coherent. The 1/2-spin atom of [MRE.md](MRE.md) carries $\log 2$ nats of information at the vacuum frequency; nothing is lost.
- **Top-down (slow)**: the Markov-blanket boundary integrates many fast events into a slowly-evolving classical-looking macro state. The "classical limit" is the limit in which the blanket's coarse-graining is much slower than the micro-event rate.

Decoherence is the **observer's-side appearance** of this hierarchical coarse-graining. It is real as an *epistemic* phenomenon (the observer's description loses coherence) and unreal as a *physical* phenomenon (no operation in the universal algebra destroys coherence).

## 4. Per-event bookkeeping: no information lost

From [MRE.md §2.1](MRE.md) (creation): each ZFA closure builds $\log 2$ nats of information at the binary-partition optimum.

From [Annihilation.md §3](Annihilation.md) (release): each unwinding releases the same $\log 2$ nats back to the vacuum as massless quanta.

From [Conservation.md §6](Conservation.md) (ledger): the total information across creation + release is exactly zero per atom; **information is conserved at the per-event level**.

Standard decoherence theory faces the **information paradox** of how a unitary universe can produce apparently irreversible classical outcomes. QLF resolves this: information is never destroyed. What appears irreversible is the blanket's coarse-grained record; the underlying coherent state is fully reversible and information-preserving at the algebra level. The classical record is a low-resolution projection of a coherent global state.

This is the same answer QLF gives for **black-hole information**: Hawking radiation carries the gauge-fold information bit-for-bit ([Entropy.md §1a](Entropy.md), [Annihilation.md §4.4](Annihilation.md)). The "information paradox" of black holes and the "decoherence paradox" of measurement are two faces of the same algebraic fact.

## 4a. A measured coherence length: the blanket's capacity sets how long a preparation stays readable

§2–§4 say decoherence is the blanket's resolution limit rather than a physical process. That claim now
carries a **number**, produced as a byproduct of the Born-rule census work
([`Born_Rule.md`](Born_Rule.md) §8, [`contextual_census.py`](contextual_census.py) `--listening`).

Closure is capacity-relative: a horizon of capacity $R$ closes exactly the histories whose excursion
never exceeds $R$ (`closedAtHorizon_iff_maxExcursion_le`,
[`lean/QLF_ClosureDepthLaw.lean`](lean/QLF_ClosureDepthLaw.lean)). Take that literally as the blanket's
listening capacity, prepare an open strand, let it evolve freely inside the capacity, and ask what a
capacity-$R$ listening can still read of the preparation after $k$ twists. Exactly, in integers:

| capacity $R$ | decay of $\lvert P(+) - \tfrac12\rvert$ per twist | coherence length $\tau$ |
|---|---|---|
| 2 | 0.666 | 2.5 twists |
| 3 | 0.868 | 7.1 twists |
| 4 | 0.906 | 10.1 twists |

Three things follow, and they are the quantitative form of this document's thesis:

1. **Capacity controls coherence persistence in this finite census model** — a bigger capacity holds
   a preparation readable for longer, with $\tau$ rising with $R$ at every capacity measured. Stated
   as what it is: a measurement on the twist census at three capacities, not a general theorem. This is the substrate version of "isolate the qubit better" (§5): isolation
   *is* capacity, and there is no other knob.
2. **Nothing is destroyed; the reading degrades.** The history is the same exact object at every $k$;
   what decays is what a bounded listening can *distinguish*. The mechanism is spectral — at fixed
   capacity the walk is a finite signed transfer operator with a degenerate $\pm i\lambda(R)$ leading
   pair, and the preparation-carrying part lives in subdominant modes, which decay no slower than
   the global spectral gap $\lambda_2/\lambda_1$ ($0.752, 0.951, 0.979$ at $R = 2, 3, 4$; the aligned
   geometry above decays faster still). Coarse-graining, not collapse,
   exactly as `decoherence_impossibility` requires.
3. **What is forgotten first is direction.** After many twists the surviving limit depends only on the
   preparation's axis class: a preparation and its reversal become indistinguishable to that listening
   (`/` with `\`, `/>` with `/<`, `/^` with `/v`). The pointer *basis* survives the blanket long after
   the pointer *value* does — a substrate reading of einselection (Zurek 1981), with the selected
   observable being the axis and the erased one being its sense.

The honest scope: this is a measurement on the twist census, not a derivation of a Lindblad rate, and
the same numbers are why the long-horizon route to the Born rule is closed ([`Born_Rule.md`](Born_Rule.md)
§8) — a measurement is a *prompt* joint closure, not an infinite free run.

## 5. Why quantum computing works

In a fully decoherent universe, quantum coherence would be impossible to maintain — every interaction would collapse superpositions. In QLF, coherence is the **default**, and what we colloquially call "decoherence" is just the blanket-resolution limit at which the coherent state becomes intractable to track *for that observer*.

A quantum computer (per `quantum-computation-optimization.md`, `BraKetRhoQuCalc.md`) operates **inside a controlled Markov blanket** that keeps the relevant micro-events resolvable. As long as the blanket boundary doesn't integrate over coherent degrees of freedom faster than the computation runs, the system stays usable. Engineering quantum computers is the practice of designing Markov blankets with high temporal resolution and low boundary leak.

The "decoherence time" of a qubit is the time scale on which the local Markov blanket begins to coarse-grain over the off-diagonal phases. It is not a fundamental limit; it is a property of the engineering of the apparatus.

## 6. Quantum Darwinism in QLF

The standard story of quantum-to-classical transition includes Wojciech Zurek's **quantum Darwinism**: pointer states are those that survive environmental selection because they replicate redundantly into the environment.

QLF gives this a constructive content: **stable Markov-blanket states are exactly those that survive ZFA-closure propagation across many environmental "votes."** A pointer state in QLF is a ZFA closure whose Hermitian-pair structure is preserved under composition with the surrounding vacuum's typical histories. Non-pointer states leak information into the environment in a way that the blanket cannot integrate into a stable record; they appear to "decohere" because the observer's blanket cannot bring them to a consistent macro projection.

The environmental "voting" is the parallel composition of many vacuum atoms with the observed system; stable states are those for which the composition stays Pauli-closed and count-balanced (full ZFA). Non-stable states have one or both halves of ZFA fail under composition, so they are pruned by the algebra itself.

Biology supplies a test of the blanket reading: the quantum effects that survive in warm tissue are tunnelling events and spins, the channels a warm bath disturbs least, while extended electronic coherence in photosynthetic proteins did not hold up. [`Quantum_Biology.md`](Quantum_Biology.md) §5 tabulates the evidence and labels the agreement as consistency, not confirmation.

## 7. The decoherence-impossibility theorem reread

`decoherence_impossibility` is often misread (when QLF is first encountered) as "QLF claims decoherence doesn't happen." That's wrong. The correct reading is:

**No constructible RhoProcess takes a ZFA-balanced state to a ZFA-unbalanced one.** Equivalently: parallel composition with any environment process preserves ZFA balance. Equivalently: the universal state is always fully coherent.

What we colloquially mean by "decoherence" — the apparent emergence of classical-looking outcomes — is a property of the observer-relative coarse-graining, not of the universal state. The theorem rules out one specific picture (the universal state decoheres into a classical mixture); it does not rule out the apparent decoherence the observer experiences.

This is the standard relational-quantum-mechanics framing applied at the QLF substrate: "decoherence" is a property of descriptions, not of the world.

## 8. Open work

- **Lean theorem**: `apparent_decoherence_is_blanket_coarse_graining` formalizing §3 — given a Markov blanket and a fully coherent universal state, the blanket's restricted projection is a probabilistic mixture matching the standard decoherence-master-equation predictions.
- **Numerical demo**: simulate a small QLF system + environment, compute the blanket-restricted density matrix, verify it matches Lindblad-equation decoherence dynamics for the same Hamiltonian.
- **Recovery experiments**: a precise prediction — under what conditions can an apparently-decohered state be recovered by carefully integrating the environment back into the observer's blanket? QLF predicts this is always possible in principle; standard decoherence theory often hedges.
- **Quantum-error-correction connection**: error-correcting codes work because they distribute logical information across many physical qubits in a way that survives partial blanket coarse-graining. Develop the connection to `Error_Correction.md`.

## References

### Internal

- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — Lean-verified `decoherence_impossibility` and `bra_ket_always_balanced`
- [Measurement_Problem.md](Measurement_Problem.md) — §4a "quantitative content of a measurement"; this doc develops the partner story for the apparent-classical limit
- [Hierarchical_Control.md](Hierarchical_Control.md) — §5 "decoherence as top-down filter"; full bottom-up/top-down architecture
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — Markov blanket as the topological boundary screening internal free-action deficits
- [MRE.md](MRE.md) — per-event $\log 2$ creation quantum
- [Annihilation.md](Annihilation.md) — per-event $\log 2$ release quantum; information ledger conservation
- [Conservation.md](Conservation.md) — §6 information conservation as a novel Noether-style law
- [Entropy.md](Entropy.md) — Hawking-radiation information return; same algebraic mechanism as decoherence
- [Born_Rule.md](Born_Rule.md) — the probability assignment that the observer sees on the apparent decohered state
- [Entanglement.md](Entanglement.md) — §5 no-signaling from local ZFA closure; the same locality that prevents FTL signaling makes coarse-graining the only thing the observer can do
- [Frequency_Synchronization.md](Frequency_Synchronization.md) — the clock rate at which the blanket integrates micro-events
- `BraKetRhoQuCalc.lean` — Lean source for `decoherence_impossibility`
- `Error_Correction.md` — quantum-error-correction angle on apparent decoherence

### External

- Zurek, W. H. (1981). *Pointer basis of quantum apparatus: into what mixture does the wave packet collapse?* Phys. Rev. D 24, 1516 — environment-induced superselection.
- Joos, E., Zeh, H. D. (1985). *The emergence of classical properties through interaction with the environment.* Z. Phys. B 59, 223 — foundational decoherence paper.
- Zurek, W. H. (2009). *Quantum Darwinism.* Nature Physics 5, 181 — environmental selection of pointer states.
- Rovelli, C. (1996). *Relational quantum mechanics.* Int. J. Theor. Phys. 35, 1637 — observer-relative ontology QLF inherits at the substrate.
