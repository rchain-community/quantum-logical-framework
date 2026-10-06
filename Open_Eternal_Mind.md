# Open or Closed, Fleeting or Eternal — and Where Mind, Dreams and Synchronicity Fit

A question put to the [Quantum Logical Framework](README.md) (QLF), answered from what the repository
already establishes:

> If the universe is quantum logical rather than physical: is it open or closed, fleeting or eternal?
> What of consciousness, dreams and synchronicities — are they logical too? Can they be typed, and if
> so, in what discrete field?

Every claim below carries one of five labels, following [`ScientificApproach.md`](ScientificApproach.md):

| Label | Meaning |
|---|---|
| **Proved** | A Lean theorem in this repository (zero `sorry`). The label says what the theorem states, which is sometimes much less than the prose around it. |
| **Standard** | Established physics or mathematics that QLF is consistent with and does not add to. |
| **Interpretation** | A reading of proved or standard facts. It cannot be wrong by experiment, and cannot be confirmed by one. |
| **Speculation** | A claim that goes beyond what any of the above supports. |
| **Open** | A question that could be settled and has not been. |

---

## 1. Open or closed?

**Short answer: open-ended in depth, finite at every horizon, and silent on global spatial topology.**

- **Finite at every horizon — Proved.** A finite-information region holds finitely many distinguishable
  states (`no_continuum_in_finite_region`, [`QLF_Realizability`](lean/QLF_Realizability.lean)); the state
  space at any causal horizon is a finite-rank `ℤ[i]`-module ([`The_QLF_State_Space.md`](The_QLF_State_Space.md) §3).
- **Unbounded in depth — Proved, but weak.** `no_terminal_phase` and `order_at_every_scale`
  ([`QLF_LogicalBang`](lean/QLF_LogicalBang.lean)) state that every balanced twist string has a strictly
  longer balanced extension (append `[+, −]`). That is a true fact about strings. It does **not** show that
  the physical universe keeps producing new structure; that step is Interpretation
  ([`Creation.md`](Creation.md) §8c).
- **No global "now" — Proved.** The causal order is a partial order and is not total
  (`causal_order_not_total`). There is no single global time slice, so "the whole universe at one instant"
  is not an object QLF has. **Standard:** relativity already says this.
- **Closed in the bookkeeping sense — Proved + Standard.** Every realized event is a balanced closure
  (`achieves_ZFA`, `bra_ket_always_balanced`). For a spatially closed universe the total Hamiltonian is
  identically zero (ADM / Wheeler–DeWitt `HΨ = 0`), which [`Philosophy.md`](Philosophy.md) reads as ZFA for
  the totality. That reading is Interpretation; `H = 0` itself is Standard.
- **Spatially open or closed — Standard, not QLF.** Measured spatial curvature is consistent with zero
  (Planck 2018 + BAO: `Ω_k = 0.0007 ± 0.0019`). QLF derives no value of `Ω_k` and makes no topology
  prediction. **Open.**
- **Logically open — Interpretation.** The future is un-rendered possibility, not a fixed block
  ([`Reversibility.md`](Reversibility.md)); in the constructive logic QLF uses, `A ∨ ¬A` is not asserted for
  a closure that has not happened ([`Intuitionistic_Logic.md`](Intuitionistic_Logic.md)). This is a choice
  of logic consistent with the formalism, not a consequence of it.

## 2. Fleeting or eternal?

**Short answer: each event is fleeting, records last only as long as they are copied, and the space of
possibilities is timeless. Whether the whole has a beginning or an end is not settled.**

- **Each closure forgets almost everything — Proved.** After a balanced history `h`, everything that
  follows depends on which way `h` closed only through one sign `σ(h) = ±1` (`closure_renewal`,
  [`QLF_ClosureRenewal`](lean/QLF_ClosureRenewal.lean); [`Memetics_QLF.md`](Memetics_QLF.md)). An event is
  fleeting in a precise sense: at most one bit of its "which way" reaches its own future.
- **Persistence is copying — Standard + measured in the repo.** A record survives only if third parties
  hold it redundantly (quantum Darwinism, Zurek 2009). [`Memetics_QLF.md`](Memetics_QLF.md) §9 measures how
  much is held across intersecting light cones. Memory, in brains or in the cosmos, is redundancy, not
  permanence.
- **Forgetting has a price — Proved + Standard.** Each many-to-one closure costs `ΔF = −log 2`
  ([`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean)), which is Landauer's bound. Reversible steps cost nothing.
- **The possibility landscape is timeless — Interpretation.** "The map is timeless, the journey is
  synthesized" ([`Time.md`](Time.md) §1). This is the possibilist ontology
  ([`possibilist-ontology.md`](possibilist-ontology.md)), not a theorem.
- **No absolute beginning — Interpretation.** The "logical bang" is the minimal closure `[+, −]`
  (`first_distinction_closes`, Proved as a fact about that string). Saying the universe therefore has no
  first moment, or that our Big Bang is the inside of a parent horizon, is Speculation that
  [`AgeOfUniverse.md`](AgeOfUniverse.md) itself calls causally unfalsifiable from within.
- **No heat death — Speculation.** [`Creation.md`](Creation.md) §8c argues that a global heat death needs
  a single global system, which a non-total causal order lacks. The Lean results it cites are the string
  facts above. Standard ΛCDM predicts an asymptotically de Sitter future, and QLF has no quantitative
  model that departs from it. The repo's own attempt to tie dark energy to `log 2` at every epoch failed
  ([`Cosmological_Constant.md`](Cosmological_Constant.md) status note, §5.7–§5.8; `qlf_count_not_selfconsistent`
  in [`QLF_DeSitterCount`](lean/QLF_DeSitterCount.lean)). **Open.**

## 3. Consciousness, dreams and synchronicity — are they logical?

### Consciousness

[`Consciousness.md`](Consciousness.md) is the repo's model. Its status, stated more strictly than that
document does:

- **What the Lean proves.** `QLF_Consciousness` defines `freq R = 1/R`, `bind a b = min a b` and
  `consciousPeriod = min`, and proves facts about `min` and `1/R` on naturals. These are correct and very
  small. That consciousness *is* the highest-frequency bound closure is a definition placed into the model,
  not something derived.
- **What is Standard.** Gamma-band binding and global-workspace ignition are real empirical literatures.
  QLF maps onto them; it does not predict anything they do not already say.
- **What is Interpretation.** The dual-aspect stance (a closure from outside is physics, from inside is
  experience) and the two-factor qualia account (§6 there) are positions, stated as such.
- **What is testable.** Conscious access should track narrow-linewidth, isolated oscillatory modes
  ([`Consciousness.md`](Consciousness.md) §5; [`Quantum_Biology.md`](Quantum_Biology.md) §5a gives the
  quiet-frequency criterion in numbers). This is the one claim that can fail.

So: yes, consciousness is "logical" in QLF in the sense that its architecture is modeled as closures. The
felt quality is not derived from anything.

### Dreams

The repo has no account of dreams; this is new, and it is Interpretation using the existing model.

In `Consciousness.md` terms, sleep gates off the external sensory closures, so the fastest bound closure is
internal: the self-model replaying and recombining stored records. A dream is then a closure whose content
comes from **records** (copies held in the brain) rather than from current joint closures with the world.

This puts real pressure on `Consciousness.md` §6. That section says a self-model *without* coupling to
external joint closures is a "functional zombie" with no felt quality. Dreams are felt, and their content is
largely internal. Either (a) stored records count as coupling, in which case the zombie test loses its
force, or (b) dream experience depends on residual external coupling, which predicts that dream vividness
should fall as sensory coupling falls (it does not obviously do so: REM sleep has strong sensory gating and
vivid dreams). **Open**, and worth stating as a challenge to §6 rather than as support for it.

### Synchronicity

Also new here. QLF has a definite answer, and it is deflationary.

- **Proved/Standard: no signalling.** In QLF, correlations between distant closures come only from a shared
  past ([`Entanglement.md`](Entanglement.md) §5); entanglement cannot carry a chosen message. This is the
  standard no-signalling theorem.
- **Consequence.** A correlation between two events with no common cause and no signal, selected for its
  *meaning* to an observer, would be a signalling-class effect. QLF forbids it for the same reason quantum
  mechanics does.
- **What QLF does allow.** Shared closures in overlapping past light cones do correlate distant records
  ([`Memetics_QLF.md`](Memetics_QLF.md) §9). So "meaningful coincidence" has a QLF reading: common causes
  in a shared past, plus the observer's selection of which coincidences to notice. That is the ordinary
  base-rate explanation, said in closure language.
- **Falsifiable.** A pre-registered synchronicity effect above base rates would refute standard quantum
  mechanics and QLF together. None has survived such testing.

So synchronicity is "logical" in QLF only as correlated records with a common past. Acausal meaning is not
in the framework, and adding it would break the part of the framework that agrees with experiment.

## 4. Can they be typed, and in what discrete field?

**Yes, structurally, and no field is needed to do it.** The repo already has a type system, and it is ZFA
itself.

- **Typing is balance — Proved.** A `RhoProcess` is well-typed exactly when it is ZFA-balanced: kets have
  topology `[pos, neg]`, bras `[neg, pos]`, and an unbalanced process cannot be built
  (`bra_ket_always_balanced`, [`BraKetRhoQuCalc`](lean/BraKetRhoQuCalc.lean)). A closure is a term of the
  type `{w : List Twist // countBalanced w}`. In the constructive reading, a closure is a proof of its own
  balance ([`Intuitionistic_Logic.md`](Intuitionistic_Logic.md)).
- **So any closure is typed**: a perception, a thought, a dream, a meme. What QLF does *not* have is a type
  that tells a dream from a perception. That would be a predicate on where the closure's content comes from
  (current joint closure vs. stored record), and it is not defined. **Open**, and definable.

The algebraic structures the repo actually uses, smallest first:

| Structure | What lives there | Is it a field? | Status |
|---|---|---|---|
| `𝔽₂ = ℤ/2` | The one bit a closure keeps: its sign `σ = ±1`. Closures fold to `±I`, never `±iI` (`QLF_BalancedPhaseReal`), so the closure phase group is `μ₂ ≅ (𝔽₂, +)` | **Yes** — the only finite field the repo's closure data uses | Proved |
| `𝔽₂²` (Klein four) | Axis parity of a twist string; a closed axis set is a Klein-four subgroup (`QLF_AlphabetNecessity`, `axisProd_eq_I_of_countBalanced`) | A 2-dimensional vector space over `𝔽₂` | Proved |
| `μ₄ = (ℤ[i])ˣ` | Phases of open (unclosed) folds, `{±1, ±i}` (`QLF_StateSpace`, `QLF_AlgebraEmergence`) | No — a cyclic group | Proved |
| `ℤ[i]` | Amplitudes (path sums of `μ₄` phases) and the state space, a finite-rank `ℤ[i]`-module per horizon | No — a ring (a lattice) | Proved |
| `ℚ` / `ℚ(i)` | Born probabilities `(a²+b²)/Z` are rational; `ℚ(i)` is the smallest field containing the amplitudes | Yes, but infinite | Proved (`ℚ`) / Standard (`ℚ(i)`) |
| `ℂ`, Hilbert space | Continuum completion of the lattices | Yes; never realized in a finite region | Interpretation of `no_continuum_in_finite_region` |

So the direct answer to "in what discrete field" is: **the record of any closure, mental or physical, lives
over `𝔽₂`; amplitudes live in the ring `ℤ[i]`, not a field; and dividing (to get probabilities) needs `ℚ`.**

One addition that is not in the repo, labeled Standard mathematics: if a *finite* field that keeps the full
phase group `μ₄` is wanted, the smallest is `𝔽₅ = ℤ[i]/(2+i)`, where `i ↦ 2` (since `2² = 4 = −1`). Reducing
modulo 5 keeps the phases but loses the sizes `a² + b²` that Born probabilities need, so it cannot replace
`ℤ[i]` and `ℚ`. Nothing in QLF currently requires it.

## 5. Summary

| Question | Answer | Label |
|---|---|---|
| Open or closed? | Finite at every horizon, unbounded in depth, no global now; spatial topology undetermined | Proved (weakly, for depth) + Standard; topology Open |
| Fleeting or eternal? | Each closure keeps one bit; records last by redundant copying; the possibility space is timeless | Proved + Standard; timelessness Interpretation |
| Beginning or end? | No first moment and no heat death are argued, not shown | Speculation; Open |
| Is consciousness logical? | Its architecture is modeled as closures; the felt quality is not derived | Lean definitions + Interpretation; one testable prediction |
| Dreams? | Internally sourced closures from stored records; they challenge the zombie criterion of `Consciousness.md` §6 | Interpretation; Open |
| Synchronicity? | Only as common-cause correlation; acausal meaningful correlation is ruled out by no-signalling | Standard; falsifiable |
| Can they be typed? | Yes: ZFA balance is the type system, and every closure is a term | Proved |
| In what field? | Closure records over `𝔽₂`; amplitudes in the ring `ℤ[i]`; probabilities in `ℚ` | Proved |
