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

5. **The pre-registered tests (§8, §9)** found the following:
   - A shared closure of intersecting light cones leaves each partner holding 5 to 6 bits about the other.
   - Its sign becomes bi-local only for longer strands.
   - When the third party interacts decides most of the sign.
   - Records follow priority, not multiplicity.
   - In a population with content-blind copying, the meme that carries no information wins.
   - With words as closures (§10, §11), equally frequent words add `log₂ k` bits to the outcome of
     competition, and any frequency difference is amplified until those bits collapse.

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

**Conjecture (multi-party), now tested.** When the pair and the third party interleave in one joint
history, edge signs depend on the *total* position, so the pair's sign may not separate from the
recorder's. The proposition above treats the recorder as an additive outside strand. T3 (§9) finds the
sign does **not** separate under interleaving: the interaction schedule decides most of it.

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
- **The multi-party conjecture (§4) fails under interleaving** (§9, T3): the schedule decides the sign.
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

## 9. Results of the pre-registered tests

Scripts: [`meme_recorder_census.py`](meme_recorder_census.py) (T2, T2b, T3, T4; exact, `ℓ ≤ 5`, about a
minute) and [`meme_population.py`](meme_population.py) (T6; seconds). The shuffle-parity rule used for T3
was checked against direct Pauli folds of every interleaving on 300 random pairs, with no mismatch.

| `ℓ` | coupled pairs | `H(x_A)` | `H(σ)` | `I(σ; A)` | `I(σ; A)/H(σ)` | mean `H(σ \| A, B)` over shuffles |
|---|---|---|---|---|---|---|
| 1 | 8 | 3.000 | 0 | 0 | — | 0 |
| 2 | 104 | 4.854 | 0.779 | 0.318 | 0.41 | 0.424 |
| 3 | 5,120 | 4.838 | 0.870 | 0.243 | 0.28 | 0.709 |
| 4 | 161,896 | 5.799 | 0.979 | 0.115 | 0.117 | 0.880 |
| 5 | 7,939,008 | 6.118 | 0.991 | 0.075 | 0.075 | 0.940 |

(`I(σ; B)` equals `I(σ; A)` at every `ℓ`.)

**T2 passes.** Each partner of a shared closure holds 4.8 to 6.1 bits about the other, against at most one
bit kept by a lone closure. The irrelevance criterion is not met, so the light-cone reading of a phoneme
stays in.

**T2b fails as registered, and the trend supports it.** The threshold `I(σ; A) ≤ 0.1·H(σ)` holds only at
`ℓ = 5`. At `ℓ = 2…4` each strand alone predicts a real part of the sign (41%, 28%, 12%). The kill
condition (`> 50%`) is never met. So the sign of a shared closure is bi-local in the limit of long
strands, and short shared closures leak it to each side.

**T3 fails at `ℓ = 2` and passes from `ℓ = 3`.** The interaction schedule decides most of the sign:
0.71, 0.88 and 0.94 bits at `ℓ = 3, 4, 5`. So the §4 conjecture is **false** for interleaved histories:
the pair's sign does not split from the recorder's, and when the recorder interacts matters as much as
what it records. The §4 proposition stands only for a recorder that acts after the closure.

**T4 passes (priority).** Weighted by probability, records made at first closure on the two-letter phase
walk have depth-`d` mass `1/(d(d+1))`: 1/2 at depth 1 and 1/6 at depth 2 (the classical gambler's-ruin
result, reproduced exactly by the script). On the 8-twist walk the masses are 0.125 and 0.032. Depth 1
dominates the records, although depth 2 is the mode of the census at every fixed length `2n ≥ 6`. This
was close to forced: the shortest first closures carry most of the probability. What it adds is that the
renewal lemma makes a record an absorbing event, so priority, not multiplicity, is the ordering that
governs records. Multiplicity governs the census of possibilities.

**T6 passes.** With copying blind to content, the one-axis variant takes over in 20 of 20 seeds, and the
variants die out in the order `k = 4, 3, 2` in 18 of 20 seeds at `R = 6` (20 of 20 at `R = 10`). The
winner is the variant whose closures carry **zero** sign bits (§3). In this model fecundity selects
against information: the meme that spreads is the one that makes the fewest distinctions.

**Phoneme comparison (made because T2 passed): negative.** Phoneme systems are built from several binary
contrasts. The simulation collapses to a single one. So persistence through closure plus content-blind
copying does not produce a phoneme system. Something has to select for distinctness, which this model
does not have. The next model needs a pressure for information, for example a listener that must tell
records apart for a closure to count.

**Net, against the proposal.**

- *Discovery is bi-local* holds for the sign of long shared closures and fails for short ones.
- *Extraction needs a third party* holds (§2, §4).
- The third party's *timing* selects the sign (T3), which is a sharper form of "selecting future
  possibilities" than the record alone.
- Records follow priority (T4).
- Content-blind copying favours memes that carry nothing (T6).

## 10. Memetics with words: the closure naming game (pre-registered)

Jim's proposal, 2026-10-02: words are closures, and different closures with the same frequency add bits
to the end result of meme-frequency competition. This section was committed before
[`meme_naming_game.py`](meme_naming_game.py) was written. Results go in §11.

**Words as closures.** A word is a first closure (a prime) of the 8-twist walk. The substrate produces a
given prime of length `L` with probability `8^{−L}`, so all primes of one length are exactly tied in
frequency: 8 words at `L = 2`, 104 at `L = 4`, 2,944 at `L = 6`. If `k` tied words compete and nothing
but frequency acts, which one wins is a free choice worth `log₂ k` bits. Fitness picks the class and the
tie supplies the information. That is the answer this test puts to T6's negative result.

**The game.** This is the minimal naming game (Steels 1995; Baronchelli et al. 2006). There are `N = 200`
agents with empty inventories. Each step a random speaker and hearer are drawn. A speaker with an empty
inventory invents a word by running the substrate: a uniform twist walk until its first return to balance,
retried if it has not returned by length 6. The speaker utters a uniformly chosen word from its inventory.
If the hearer already holds it, the two record the same closure (a joint closure) and both inventories
collapse to that word. Otherwise the hearer adds it. A run ends at consensus. 400 runs.

**Predictions.**
- **T7a.** Every run reaches consensus on a single word.
- **T7b (priority).** The winner has length 2 in at least 77% of runs. 77% is the length-2 share of
  inventions, `0.125 / (0.125 + 104/8⁴ + 2944/8⁶)`.
- **T7c (the tie supplies bits).** Among runs won by a length-2 word, the winner is uniform over the 8
  words: a chi-square test does not reject uniformity at `p = 0.01`, and the observed entropy is at least
  2.9 bits.
- **T7d (control).** Give the 8 length-2 words invention weights in the ratio `1.25^{−i}`, `i = 0…7`,
  everything else unchanged. The winner entropy falls below 2.9 bits. Further, competition **amplifies**
  frequency differences, so the winner entropy is below the entropy of the invention weights themselves.

**Kill.** T7c fails (a clearly non-uniform winner inside a tied class). The proposal that ties are where
the bits come from would then be wrong for this game.

## 11. Results of the closure naming game

Run: `python3 meme_naming_game.py` (400 runs per condition, `N = 200`, seed 7, about ten seconds).

| | tied (substrate frequencies) | control (weights `1.25^{−i}`) |
|---|---|---|
| runs reaching consensus | 400 / 400 | 400 / 400 |
| winner of length 2 | 400 / 400 | 400 / 400 |
| length-2 winners by word | 54, 51, 35, 64, 45, 55, 44, 52 | 209, 108, 46, 20, 12, 3, 2, 0 |
| winner entropy | **2.981 bits** (uniform 3.000) | **1.817 bits** |
| chi-square against uniform | 10.56, `p = 0.16` | 760, `p ≈ 0` |
| entropy of the invention weights | — | 2.826 bits |

**T7a passes.** Every run reaches consensus on one word.

**T7b passes, more strongly than registered.** Length-2 words win every run, against a 77% share of
inventions. Competition amplifies the priority of the most frequent class.

**T7c passes.** Inside the tied class the winner is uniform: 2.98 of a possible 3 bits, and uniformity is
not rejected. So Jim's proposal holds in this game. Different closures with the same frequency add
`log₂ k` bits to the outcome. Fitness picks the class, and the tie is where the information comes from.

**T7d passes, including amplification.** A 1.25-fold frequency step between neighbouring words becomes
roughly a two-fold step between winners. The winner entropy (1.82 bits) is a full bit below the
entropy of the weights (2.83 bits). So the bits survive only while the tie is exact. Any frequency
difference is amplified, and the information the tie carried collapses toward the favoured word.

**What this adds to T6.** Content-blind copying selects the class that closes most readily, and that
class carries no sign bit. But a class can hold many words of equal frequency, and which of them the
population adopts is free. That free choice is the population's information: a convention worth
`log₂ k` bits. It is fragile in the same proportion that frequency competition is strong.
*Interpretation:* in this model, a language's information sits in its arbitrary, equally available
conventions, not in what fitness selects.

## 12. QuCalc as the tie-break (pre-registered)

Jim's proposal, 2026-10-02: the QuCalc of each meme may suggest a rule for breaking ties. `/solve`
([`QucalcSearch.md`](QucalcSearch.md)) already ranks closures in a fixed order: least peak excursion,
then shortest, then phase `+1`, then alphabetical order of the twists. This section was committed before the
test code was written. Results go in §13.

**What the cascade can do here.** All 8 length-2 words have excursion 1, length 2 and phase `−1`, so only
the alphabetical step separates them. All 104 length-4 primes have excursion 2, and the phase step splits
them 80 (`+1`) to 24 (`−1`). So the test uses length 4.

**The game.** As in §10, but every invented word is a uniform length-4 prime (the substrate conditioned on
first return at 4), so all 104 words are tied in frequency. Three ways to choose what a speaker utters
from its inventory:

- **Baseline:** uniformly, as in §10.
- **Reading 1 (full cascade):** the word the whole `/solve` order ranks first, alphabetical step included.
- **Reading 2 (physical cascade):** uniformly among the inventory words that are best by excursion,
  length and phase. The alphabetical step is left out.

400 runs each, `N = 200`.

**Predictions.**
- **T8a (baseline).** Phase `+1` winners make up 70% to 84% of runs (80/104 = 77%), and the winner entropy
  is at least 6.3 bits (log₂ 104 = 6.70; finite sampling lowers the estimate by about 0.19).
- **T8b (reading 1).** The winner is the cascade's best among the words invented in that run in at least
  95% of runs, one single word wins at least 90% of runs, and the winner entropy is below 0.5 bit. The
  convention is set by the substrate's order, not by the population.
- **T8c (reading 2).** Phase `+1` wins at least 95% of runs, and among those wins the winner is uniform
  over the 80 phase `+1` words: chi-square does not reject uniformity at `p = 0.01`, and the entropy is
  at least 6.0 bits (log₂ 80 = 6.32, minus about 0.14 for sampling).

**Kill.** T8c fails: the physical cascade either does not select phase `+1`, or it breaks the tie further
than the phase alone does.

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
