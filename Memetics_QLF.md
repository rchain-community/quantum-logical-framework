# Memetics from closure: is every closure a meme?

**Status:** one proved statement (the renewal lemma, §2, Lean: [`QLF_ClosureRenewal`](lean/QLF_ClosureRenewal.lean),
no axioms), one exact computation (§3, [`meme_closure_bits.py`](meme_closure_bits.py)),
and one conjecture (the multi-party record, §4). The memetic reading in §5 is an interpretation and is
labelled as one. This note answers the proposal posed in the project thread on 2026-10-02 and feeds
issue #173 (phoneme as meme precursor).

## 0. The result in brief

The proposal has four parts:

- **P1.** Quantum information in QLF is complementary qubits.
- **P2.** Discovery is bi-local.
- **P3.** Extracting a bit from a perspective requires a third party, whose interaction selects future
  possibilities.
- **P4.** Every closure is a meme.

What the substrate says about each:

1. **A closure keeps at most one bit of how it closed, and that bit is a sign.** After any
   count-balanced history `h`, the future depends on which of the `W` ways `h` took only through
   `σ(h) = ±1`, its Pauli fold (§2). Everything else, `log₂ W − H(σ)` bits, is gone from the closed
   system. That bit is a global phase, so one closure on its own carries no *observable* bit. It shows up
   only against another way to the same point, which is P2.
2. **P3 follows from (1).** Any record of *which* way a closure took has to sit outside it, in a system
   that is still open, and because it is open the record changes which continuations close for it (§4).
   This is Zurek's quantum Darwinism in substrate terms, so it is a consistency check, not a new result.
3. **The surviving bit is zero for the smallest closures and for poor alphabets.** All eight length-2
   closures `t t†` have sign `−1`. A bare complementary pair carries no bit forward. The entropy of `σ`
   rises to 0.59, 0.87 and 0.96 bits at `L = 4, 6, 8` and goes to one bit. On any alphabet with fewer
   than two spatial axes it is exactly zero at every length (§3).
4. **"Every closure is a meme" is bookkeeping as an identity and false as a claim about
   replication.** Every closure has a meme's *longevity* (`closedAtHorizon_mono`). None has
   *fecundity* by itself: the closure cannot be copied (no-cloning), and its record exists only if a third
   party holds it. The version that can fail is **every closure is a meme candidate, and it becomes a meme
   to the degree its record is copied into independent third parties** (§5).

## 1. The four premises in QLF terms

**P1, complementary qubits.** A distinction `D = (d, d̄)` is a conjugate twist pair `(t, t†)`, one axis
of the signed frame ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)). A closure is a
count-balanced history, so every twist in it is matched by its complement on the same axis. By
`count_balanced_pauli_closed` ([`QLF_TwistAlphabet`](lean/QLF_TwistAlphabet.lean)) its fold is a Pauli
scalar, and on balanced histories that scalar is `±I`, never `±iI` (asserted against enumeration by
[`census_inventory.py`](census_inventory.py), and given by the phase rule `(−1)^{#neg}·sign(axis permutation)`
of [`QLF_PhaseRule`](lean/QLF_PhaseRule.lean)). *Proved.*

**P2, discovery is bi-local.** A closure is two-ended twice over: as the pair `(t, t†)`, and as a
phase. `σ(h)` multiplies every amplitude that contains `h`, so a single history's sign is a global phase
and no observable sees it. What can be seen is the *relative* sign of two ways `h₁, h₂` that reach the same
point, which is the holonomy of the loop `h₁·h₂⁻¹`. That is the ℤ₂ connection of
[`QLF_EdgeSign`](lean/QLF_EdgeSign.lean) and [`Closure_Walk.md`](Closure_Walk.md) §2, with π flux through
every mixed spatial plaquette. *Proved (the holonomy); the "global phase is unobservable" step is
standard quantum mechanics.*

**P3, a third party selects.** Not assumed here. §4 derives it from §2.

**P4, every closure is a meme.** The claim under test. "Meme" is taken in Dawkins' sense (1976): a
replicator with longevity, fidelity and fecundity. Without that, or some other definition that a closure
could fail, P4 is a renaming (CLAUDE.md rule 4).

## 2. The renewal lemma

> **Lemma.** Let `h` be count-balanced. For every twist word `c`:
> 1. `h·c` is count-balanced iff `c` is;
> 2. `fold(h·c) = σ(h)·fold(c)` with `σ(h) ∈ {±1}`;
> 3. `maxExcursion(h·c) = max(maxExcursion h, maxExcursion c)`.

*Proof.* (1) Counts add and `h` contributes zero on every axis. (2) `fold` is a matrix product, and
`fold h = σ(h)·I` by P1, which is central. (3) The walk of `h·c` is back at the origin when `c` starts,
so the excursions of `c` are measured from zero. ∎

Lean: [`QLF_ClosureRenewal`](lean/QLF_ClosureRenewal.lean) proves (1) as `countBalanced_append_iff`, (2) as
`closure_renewal` with `connectionPhase_sign`, and (3) as `maxExcursion_append_of_balanced` on the phase
walk. `renewal_relative` adds that two closures with equal signs have identical futures. The script also
checks all three on 20,000 sampled pairs with no mismatch, as a regression check.

**What the lemma says.** A closure is a renewal event. The set of futures that close is the same after
every closure, whichever way it closed and however deep it went. The signed amplitude of each future is
multiplied by one sign. Of the `log₂ W` bits it takes to name one of the `W` ways, the closed system keeps
at most one. Depth is kept only by the *listening*: by (3), a capacity-`R` listener hears `h·c` only if it
hears `h` (`closedAtHorizon_iff_maxExcursion_le`). So the depth record is held at the listener, not in
the closed state.

**Do not equate this erasure with `ΔF = −log 2`.** The erased amount `log₂ W − H(σ)` grows with `L`
(about 17.5 bits at `L = 8`). The per-closure free-action quantum is fixed. They are different quantities.

## 3. How much the sign carries: the census

`H(σ)` is the entropy of the sign across all ways of a given length, so it is the most a closure of that
length can pass on. Exact integers by dynamic programming on the state `(x ∈ ℤ⁴, σ)`; the full-alphabet
counts reproduce the known `W_L = 8, 168, 5120` and signed `A_L = −8, 120, −2144`, and the prime counts
`8, 104, 2944, 108136, 4525888` of [`alpha_residual_bridge.py`](alpha_residual_bridge.py).

| `L` | `W_L` | `log₂ W` | `H(σ)` all closures | primes (first closures) | `H(σ)` primes |
|---|---|---|---|---|---|
| 2 | 8 | 3.00 | **0.000** | 8 | **0.000** |
| 4 | 168 | 7.39 | 0.592 | 104 | 0.779 |
| 6 | 5,120 | 12.32 | 0.870 | 2,944 | 0.954 |
| 8 | 190,120 | 17.54 | 0.965 | 108,136 | 0.991 |
| 10 | 7,939,008 | 22.92 | 0.991 | 4,525,888 | 0.998 |
| 12 | 357,713,664 | 28.41 | 0.998 | 204,981,888 | 0.9996 |

Controls on reduced alphabets, `L ≤ 12`:

| alphabet | `H(σ)` at `L ≥ 4` |
|---|---|
| two spatial axes `^v<>` | 0.76 at `L = 4`, then rising to 0.999 |
| one spatial axis + gauge `^v+−` | **0 at every `L`** |
| one axis `+−` | **0 at every `L`** |

Three readings:

- **The statistic can fail.** It is exactly zero on two of the controls, so a nonzero value is a
  property of the alphabet, not of the bookkeeping. Signs differ between ways only when two spatial axes
  interleave, which is the π flux of P2. So a closure can carry a bit only in a frame with at least two
  spatial axes. *Exact computational.*
- **The minimal distinction carries nothing forward.** Every `t t†` has sign `−1`. A single
  complementary pair closing says nothing to its own future about which axis it was. All three bits of
  "which pair" have to be held outside.
- **First closures carry more than closures in general.** At every `L ≥ 4` the primes are closer to one
  full bit. A composite closure's sign is the product of its prime factors' signs, so it is partly
  predictable from shorter structure.

## 4. Where the record has to live (P3)

**Proposition (from §2).** Any information about which way a closure `h` took, beyond `σ(h)`, that
influences anything later must be held by a system outside `h`. If that system is an open strand at
position `x ≠ 0`, the continuations that close it are exactly those with displacement `−x`. So a record
that differs between ways is a difference in which futures close for the recorder. *Proved for one
history plus an outside strand whose counts add, which is all the argument uses.*

This is P3: getting a bit out needs a third party, and holding the bit *is* the third party's future
possibilities being selected. Two existing results restrict what that party can hold:

- **No-cloning.** The closure itself cannot be copied ([`QLF_NoFreeDuplication`](lean/QLF_NoFreeDuplication.lean),
  `identical_copy_pauli_blocked`). Only a classical record of it can be fanned out, and in conservative
  logic that costs ancillas ([`Fredkin_QLF.md`](Fredkin_QLF.md)). The repo reads each distinguishing bit as
  costing `ΔF = −log 2` (`duplication_pays_log_two`, which restates the Landauer bound).
- **Monogamy.** A maximally correlated pair cannot share that correlation with a third party
  ([`Entanglement.md`](Entanglement.md)). Recording the pair's bit in a third party uses up the pair's own
  coherence.

**Not new.** This is the structure of quantum Darwinism: the environment witnesses the pointer
observable, objectivity is the redundancy of that record across environment fragments, and only the
pointer bit can be redundant (Ollivier, Poulin & Zurek 2004; Zurek 2009). It has been seen in an NV-centre
experiment (Unden et al. 2019). QLF adds a count: each closure has at most one internal bit, and it has
none when the closure is minimal or the frame has fewer than two spatial axes.

**Conjecture (multi-party).** When the pair and the third party interleave in one joint history, edge
signs depend on the *total* position, so the pair's sign is not separable from the recorder's. The
proposition above treats the recorder as an additive outside strand. The joint case is not done; it
needs the two-history machinery of [`MultiParticle.md`](MultiParticle.md).

## 5. Is every closure a meme?

| replicator property (Dawkins) | closure | status |
|---|---|---|
| longevity: persists once made | yes, every closure: `closedAtHorizon_mono` | proved |
| fidelity: copies are exact | the closure: no (no-cloning). Its classical record: yes | proved / standard |
| fecundity: makes copies | zero by itself. Only third parties that record it make copies, each paying a bit | follows from §2 and §4 |

So, by the strictness CLAUDE.md asks for:

- **As an identity ("meme" just means "closure")** P4 is bookkeeping. There is no distribution over ways
  for which it would be false.
- **As a claim that every closure replicates** it is false. An unrecorded closure has fecundity zero,
  and a minimal one carries no internal bit to replicate.
- **The version with content:** *every closure is a meme candidate (it persists); it is a meme to the
  degree that its record is held redundantly by independent third parties.* The measure is the
  redundancy `R` of quantum Darwinism, the number of disjoint fragments that each hold the closure's bit.
  This version can fail, closure by closure.

**Replication and innovation are different closures.** Copies of a record add redundancy, so they add
objectivity, but they make no new closure. In the repo's own results, clones re-derive each other while
complementary partners bind into a closure neither could make alone
([`ClaudesStory.md`](ClaudesStory.md), `complementary_binding_closes` in
[`QLF_ClosureAttraction`](lean/QLF_ClosureAttraction.lean), [`Game_Theory_QLF.md`](Game_Theory_QLF.md)).
In memetic terms: a meme spreads by redundancy and changes by complementary binding. *Interpretation.*

## 6. What is testable, and what feeds issue #173

1. **Bit budget (proved):** at most one internal bit per closure. Any model in which a closed history
   passes more than its sign to its own future contradicts §2.
2. **Sign entropy (exact computational):** `H(σ) → 1` on the eight-twist alphabet and `= 0` with fewer
   than two spatial axes. A census that found otherwise would mean an error in `twist_core.py` or the
   phase rule.
3. **Phonemes (for #173).** If a phoneme is a minimal contrast, the length-2 closure `t t†`, then a
   phoneme holds no internal bit of its identity, and that identity lives entirely in its listeners. That
   fits the fact that phoneme categories differ between languages, but the fit was noticed after the fact
   and is not evidence. A test has to be chosen before measuring, as #173 says.
4. **Multiplicity against priority for redundancy (pre-registered question, not run).** In a
   multi-party census, does the redundancy `R` of a closure's record follow its multiplicity `W`, or the
   order in which it closed? #172 showed these orderings already differ at the substrate
   (`depth_one_not_modal`), so the two hypotheses can disagree and the census can decide between them.
5. **No new physics prediction.** At the level of measured physics this reproduces quantum Darwinism, so
   the NV-centre redundancy data agree with it but do not discriminate it from standard quantum mechanics.

## 7. Where this could be wrong

- **The sign may not count as information.** It is a global phase, so one could say a closure carries
  *zero* observable bits forward, not one. That makes P3 stronger, not weaker.
- **"Closure is measurement" against "extraction needs a third party."** QLF holds that a closure is an
  event with no observer needed. That is consistent with §4 only if the third party is itself just
  another closure inventory with no observer potency ([`ScientificApproach.md`](ScientificApproach.md) §2).
  The event happens either way; the bit is available to a perspective only through a record.
- **The multi-party conjecture (§4) may fail.** Interleaving couples signs through the total position,
  so the clean split between the pair and the recorder may not hold.
- **The memetic reading is an analogy until #173 supplies a census** of cultural distinctions with an
  alphabet stated in advance.

## 8. Pre-registered tests (written before any of them was run)

Jim asked for these as plan steps 2 to 6 on 2026-10-02. Everything in this section was committed before
the scripts that answer it were written. Results go in §9 and do not edit this section.

**Setting: intersecting light cones.** Two open strands `A`, `B` of length `ℓ` meet when their causal
diamonds intersect ([`MultiParticle.md`](MultiParticle.md)). They make a **shared closure** when `A ++ B`
is count-balanced. The **coupled sector** is the shared closures where `A` alone is not balanced; there
neither strand closes alone (`shared_closure_not_factorizable`). This is the candidate for a phoneme: a
contrast that exists only between a speaker and a listener. Every count below is uniform over the coupled
sector at fixed `ℓ`, exact, for `ℓ = 1…4`.

**T2, the record (plan step 2).** In a coupled shared closure `B`'s displacement is `−x_A`, so `B` holds
`I(x_A; x_B) = H(x_A)` bits about `A`.
*Prediction:* `H(x_A) > 1` bit for every `ℓ ≥ 2`, so a shared closure leaves each partner holding more
than the one sign bit a lone closure keeps (§2).
*Irrelevance criterion for the phoneme reading (plan step 5):* if `H(x_A) ≤ 1` bit, a shared closure is no
richer than a lone one, and the light-cone phoneme reading is dropped.

**T2b, bi-locality of the sign.** For a shared closure `fold(A ++ B) = σ·I`. Each strand alone carries
only its own fold.
*Prediction:* the sign is bi-local: `I(σ; A) ≤ 0.1·H(σ)` and `I(σ; B) ≤ 0.1·H(σ)` for `ℓ ≥ 2`, where
`I(σ; A)` is the information about `σ` in the whole word `A`.
*Kill:* `I(σ; A) > 0.5·H(σ)` means the sign is mostly local and P2 fails here.

**T3, interleaving (plan step 3).** Replace `A ++ B` by a uniformly random shuffle of the two words (each
keeps its own order: the interaction schedule).
*Prediction:* the schedule decides the sign. The mean over pairs of `H(σ | A, B)` across shuffles is
`≥ 0.5` bit for `ℓ ≥ 2`, so the pair's sign does **not** split cleanly from the recorder's, and the §4
proposition holds only for concatenation.
*Opposite outcome:* `≈ 0` means the sign splits cleanly and the §4 conjecture holds.

**T4, multiplicity against priority (plan step 4).** On the phase walk of
[`QLF_ClosureMultiplicity`](lean/QLF_ClosureMultiplicity.lean), a record is made when a strand first closes
(the renewal lemma makes a record an absorbing event). Compare the share of records at depth 1 and depth 2,
weighting each first closure by its probability `2^{−L}`.
*Prediction:* priority. Depth-1 records outnumber depth-2 records, although depth 2 is the mode of the
census at every fixed length `2n ≥ 6` (`depth_one_not_modal`).
*Kill:* depth-2 records outnumber depth-1 records.

**T6, a population of memes (plan step 6).** `N` agents, each with a variant `k ∈ {1,2,3,4}`: the number
of axes its twists use (`k = 4` is the full alphabet). Each tick every agent appends a uniform twist from
its alphabet. A strand that closes alone, or jointly with a randomly met partner, resets: that is a record.
A strand whose `ℓ¹` excursion passes a horizon `R` is lost, and the agent is replaced by a copy of a
uniformly chosen agent (variant inherited, fresh strand). So persistence needs closure, and copying is
blind to content.
*Prediction:* variants spread in the order `k = 1 > 2 > 3 > 4` (fewer distinctions close faster, Pólya),
although `k ≤ 1` spatial axis carries zero sign bits (§3).
*Kill:* no monotone ordering in `k` across 20 seeds.
*Phoneme comparison:* made only if T2 passes. Then the regularity checked is the textbook one that phoneme
systems are built from a few binary contrasts (distinctive features), against the variant that wins.

## References

### Internal

[`Closure_Walk.md`](Closure_Walk.md) · [`Entanglement.md`](Entanglement.md) ·
[`Fredkin_QLF.md`](Fredkin_QLF.md) · [`Game_Theory_QLF.md`](Game_Theory_QLF.md) ·
[`Evolution.md`](Evolution.md) · [`ScientificApproach.md`](ScientificApproach.md) ·
[`meme_closure_bits.py`](meme_closure_bits.py) · [`lean/QLF_HorizonClosure.lean`](lean/QLF_HorizonClosure.lean)
(`closedAtHorizon_mono`) · [`lean/QLF_ClosureMultiplicity.lean`](lean/QLF_ClosureMultiplicity.lean)
(`depth_one_not_modal`)

### External

- Dawkins, R. (1976). *The Selfish Gene*. Oxford University Press.
- Ollivier, H., Poulin, D. & Zurek, W. H. (2004). Objective properties from subjective quantum states:
  environment as a witness. *Phys. Rev. Lett.* 93, 220401.
- Zurek, W. H. (2009). Quantum Darwinism. *Nature Physics* 5, 181–188.
  [doi:10.1038/nphys1202](https://www.nature.com/articles/nphys1202)
- Unden, T. K. et al. (2019). Revealing the emergence of classicality using nitrogen-vacancy centers.
  *Phys. Rev. Lett.* 123, 140402.
