# Does what happens the most ways happen first?

Jim's question (2026-10-17): *prove that what happens the most ways happens first. Exceptions? Path integrals?*

**Short answer.** Not in general. The statement is true in one exact sense, true under one extra
hypothesis, and false otherwise, and the counterexamples are small enough to check by hand.

| Reading | Status |
|---|---|
| The most probable *first outcome* is the one with the most ways *of being first* | **Proved**, but it only restates the uniform measure (§1) |
| Two **independent** events: if A has at least as many ways as B at every horizon, A is at least as likely to come first | **Proved** (§2) |
| Two events in **one shared history** | **False**: equal ways at every horizon can still give 3 : 1 (§3.2), and more ways at every horizon can still lose 5 : 7 (§3.3) |
| The shallowest closure has the most ways | **False**, proved in [`QLF_ClosureMultiplicity`](lean/QLF_ClosureMultiplicity.lean) (`depth_one_not_modal`) (§3.1) |
| Path integrals: most ways ⇒ most probable | **False** once ways carry phases. The correct statement is *most ways **in phase*** (stationary phase), and "first" has no general meaning in a real-time path sum (§4) |

All numbers below come from [`most_ways_first.py`](most_ways_first.py) and are exact (rational
arithmetic).

---

## 0. What logic alone gives, and the one extra step

"Ways" is a count. Turning a count into "how likely" needs a measure, and logic alone does not supply
one. The step used here is the **principle of indifference**: when nothing distinguishes one history from
another, give each the same weight. That is the maximum-entropy assignment under no constraints, and it is
the same rule QLF's census uses (every balanced word counts 1). It is an assumption about our ignorance,
not a claim that nature *is* the QLF construction, so it is stated as a bridge and not hidden.

With it, for a finite set of equally weighted histories,

$$P(E) = \frac{\#\{\text{histories in which } E\}}{\#\{\text{histories}\}} .$$

"First" also needs care. There are two different orders in play:

* **Logical order (horizon order).** In QLF a closure at horizon `d` is a closure at every `d' ≥ d`
  (`closedAtHorizon_mono`). Depth 1 is decided before depth 2 by construction.
* **Race order (time order).** Two events A and B compete in a growing history, and we ask which one
  occurs at an earlier step.

## 1. The exact but trivial version  *(Proved)*

Let `T` be the step at which something first happens, on a finite set of equally weighted histories.
Then `P(T = t) = w(t) / total`, where `w(t)` counts the histories whose first occurrence is at `t`. So
the most probable first-occurrence step is the one with the most ways of being the first occurrence.

This is true and useless as physics. It says "most ways of being first ⇒ most likely first", which only
restates the measure. The interesting claim compares *how many ways an event has overall* with *whether it
comes first*, and that needs §2.

## 2. The race theorem for independent events  *(Proved)*

**Setting.** Two events A and B, with first-occurrence times `T_A`, `T_B`. "A has at least as many ways
as B at every horizon" means: among histories of length `n`, at least as many already contain A as
contain B, for every `n`. Under the uniform measure that is `P(T_A ≤ n) ≥ P(T_B ≤ n)` for all `n`, i.e.
`T_A` is stochastically smaller than `T_B`.

**Theorem.** If moreover `T_A` and `T_B` are independent, then `P(T_A < T_B) ≥ P(T_B < T_A)`.

**Proof.** Let `G(a,b) = 1[a<b] − 1[b<a]`. It is non-decreasing in `b` and antisymmetric:
`G(a,b) = −G(b,a)`. Let `T_A'` be an independent copy of `T_A`. For each fixed `a`, since `T_B` is
stochastically larger than `T_A'` and `G(a,·)` is non-decreasing, `E G(a, T_B) ≥ E G(a, T_A')`. Averaging
over `a` with the distribution of `T_A` (allowed because `T_A` is independent of both) gives
`E G(T_A, T_B) ≥ E G(T_A, T_A') = 0`, the last equality by antisymmetry and exchangeability. And
`E G(T_A, T_B) = P(T_A < T_B) − P(T_B < T_A)`. ∎

So **"what happens the most ways happens first" holds when the competitors do not share histories**:
separate systems, separate coin streams, separate light cones with no common events. The independence
hypothesis cannot be dropped, as §3 shows.

## 3. Exceptions

### 3.1 Shallowest is not most ways  *(Proved in Lean, PR #172)*

For balanced histories of length `2n`, `W(n,d)` counts those whose closure depth is exactly `d`.
`depth_one_not_modal` proves `W(n,1) = 2^n < W(n,2)` for `n ≥ 3`:

| n | W(n,1), W(n,2), … | modal depth |
|---|---|---|
| 3 | 8, 10, 2 | 2 |
| 5 | 32, 130, 70, 18, 2 | 2 |
| 7 | 128, 1330, 1246, 546, 154, 26, 2 | 2 |
| 8 | 256, 4118, 4858, 2518, 880, 208, 30, 2 | **3** |

Depth 1 is first in the *logical* order and is never the mode for `n ≥ 3`; the mode moves deeper as `n`
grows (computed, `n = 8` already has mode 3). This is not a contradiction to reconcile: "first" here is the
minimum of the depth distribution and "most ways" is its mode, two different statistics of the same
random variable. The selection rule QLF uses is "reached first", which is justified by irrevocability
(`closedAtHorizon_mono`), not by multiplicity.

### 3.2 Equal ways at every horizon, 3 : 1 in the race  *(Standard: Penney's game, 1969)*

Flip a fair coin and wait for HHT or THH. Both patterns are contained in exactly the same number of
strings of every length (reversal maps one set onto the other): 1, 4, 12, 31, 74, 168, 369, … for lengths
3, 4, 5, …. Yet in one shared sequence **THH comes before HHT with probability 3/4**. The reason is
overlap: any HHT not at the very start is preceded by a T, and that T followed by HH has already completed
THH.

With two *independent* sequences the race is a tie (0.457 each, the rest being simultaneous finishes), as
§2 requires.

### 3.3 More ways at every horizon, and still second  *(Computed, exact)*

HHH against TTHH. HHH is shorter and has at least as many ways at every length checked (n ≤ 60):

| length | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|
| strings containing HHH | 1 | 3 | 8 | 20 | 47 | 107 | 238 |
| strings containing TTHH | 0 | 1 | 4 | 12 | 32 | 79 | 186 |

* Independent sequences: HHH first 0.557, TTHH first 0.405. Most ways wins, as §2 says.
* One shared sequence: **TTHH first with probability 7/12.** Most ways loses.

Once TT has appeared (which happens early), the next HH completes TTHH before any HHH can form, so TTHH's
ways sit on top of HHH's prefixes and pre-empt them.

**What decides a race in a shared history is overlap, not multiplicity.** This is the general exception,
and it is the one that matters for QLF, because competing closures in one history share events. It fits
the earlier memetics finding that the interleaving schedule, not the count, decides which closure's sign
survives ([`Memetics_QLF.md`](Memetics_QLF.md) T3).

### 3.4 Smaller exceptions

* **Unequal weights.** If histories are not equally weighted (energy, bias, a driven process), counts are
  not probabilities and §2 applies only to weighted counts.
* **Whole-history versus step-by-step counting.** Uniform weight on *complete* histories makes the next
  step proportional to the number of completions through it, not to the number of one-step options (the
  difference between the maximal-entropy random walk and the ordinary one). "Ways" must say which.
* **Ties.** With equal counts and independence the race is a tie, and nothing about multiplicity breaks it.

## 4. Path integrals

### 4.1 Where the count sits

Feynman's amplitude is a sum over histories, `K = Σ_h e^{iS(h)/ħ}`. QLF already writes its amplitude the
same way, with the phase rule `θ(h) = (−1)^{#neg} · sgn(axis perm)`
([`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) §1, [`Born_Rule.md`](Born_Rule.md) §2).

`W(n,d)` is the **unsigned** version of that sum: every history weighted `+1`. So W plays the role of the
path-integral measure only where all phases agree. Two facts locate that:

* In the one-axis census behind `W(n,d)`, every balanced word of length `2n` has exactly `n` negative
  steps and a single axis, so all of them carry the same phase `(−1)^n`. There is **no interference
  there**, and amplitude and count agree up to an overall sign. (Derived from the stated phase rule.)
* With the full alphabet, phases differ between histories and they cancel. The signed census grows like
  `(2+2√3)^L / L²` against `8^L / L²` unsigned, a loss of `ln(8/(2+2√3)) ≈ 0.381` per step
  ([`YangMills_MassGap_QLF.md`](YangMills_MassGap_QLF.md), census table). That is QLF's own measured case
  of "many ways, little amplitude".

### 4.2 What replaces "most ways" when ways have phases  *(Standard)*

As `ħ → 0` (actions large compared with the phase quantum), the sum is dominated by histories near a
**stationary** action, `δS = 0`, because there neighbouring histories have nearly equal phase and add,
while elsewhere they cancel. So the least-action path is exactly *the place where the most ways agree in
phase*. The correct path-integral version of the slogan is:

> **What happens is what the most ways *in phase* allow**, and its probability is `|Σ e^{iθ}|²`, not the count.

Exceptions on this side are standard physics:

* **Destructive interference.** Many ways, zero amplitude: the dark fringes of a double slit
  ([`Double_Slit.md`](Double_Slit.md)).
* **Tunnelling.** No real stationary history exists, yet the event happens, carried by a complex saddle
  (instanton) with weight `e^{−S_E/ħ}`.
* **No small parameter.** When actions are of order `ħ`, no single family dominates and "most ways" picks
  nothing out.

### 4.3 "First" in a path integral  *(Standard)*

A real-time path sum has no general notion of "which event came first". There is no self-adjoint time
operator (Pauli's objection), and first-arrival times need an absorbing boundary or a detector model, which
breaks the unitary sum. "First" is well defined in the **Euclidean** (imaginary-time, `e^{−S_E/ħ}`,
positive-weight) sum, which is a counting problem again. There the theory of first passage holds
(Kramers escape, Freidlin–Wentzell large deviations): the first exit is dominated by the single
least-action path, weighted by `e^{−ΔS}`, and the number of ways enters only as a prefactor. So even in
the Euclidean case, **weight beats count** at leading order, and count decides only among equal weights,
under the same independence/overlap caveats as §2–§3.

`W(n,d)` with all weights equal is exactly the Euclidean case with constant action per step: entropy
only. That is why §2 and §3 apply to it directly.

## 5. Summary for QLF

1. "Most ways ⇒ first" is a theorem only for **independent** competitors (§2). For competitors sharing a
   history it fails, and overlap decides (§3.2–3.3).
2. QLF's "reached first" selection rule does not need multiplicity. It rests on irrevocability
   (`closedAtHorizon_mono`), which is a logical-order fact, and §3.1 shows multiplicity points elsewhere.
3. With phases, the right quantity is the **coherent** count, and stationary phase is the precise form of
   "most ways". In the one-axis census phases are uniform, so W *is* the amplitude up to sign; with the full
   alphabet it is not (signed suppression 0.381 per step).

4. **Scope of the working principle.** [`Philosophy.md`](Philosophy.md) §3a states "what happens in the
   most ways happens first — a closure's frequency IS its multiplicity". The second half (frequency =
   multiplicity) is §0 under indifference and stands. The first half is a theorem only for independent
   competitors (§2); for closures that share a history it can fail (§3.2–3.3), and "the mode" and "the
   first" are different statistics (§3.1). Rule 3 there ("report the mode") is right for frequency
   questions and wrong for priority questions.

**Open.** (a) A Lean statement of the §2 race theorem over finite distributions. (b) A QLF closure race
in one shared history (two closure patterns on the 8-twist alphabet) to measure how often multiplicity and
priority disagree, the closure analogue of §3.3. (c) Whether the modal depth's growth (~√n) has a proof.

## References

* W. Penney, "Problem 95: Penney-Ante", *J. Recreational Math.* 2 (1969) 241; L. J. Guibas and A. M.
  Odlyzko, "String overlaps, pattern matching, and nontransitive games", *J. Combin. Theory A* 30 (1981)
  183–208.
* M. Shaked and J. G. Shanthikumar, *Stochastic Orders* (Springer, 2007), ch. 1 (usual stochastic order).
* R. P. Feynman, *Rev. Mod. Phys.* 20 (1948) 367; R. P. Feynman and A. R. Hibbs, *Quantum Mechanics and
  Path Integrals* (1965), ch. 2 (stationary phase and the classical limit).
* W. Pauli, *Handbuch der Physik* 24 (1933), on the absence of a time operator.
* H. A. Kramers, *Physica* 7 (1940) 284; M. I. Freidlin and A. D. Wentzell, *Random Perturbations of
  Dynamical Systems* (1984).
* Z. Burda, J. Duda, J. M. Luck, B. Waclaw, "Localization of the maximal entropy random walk",
  *PRL* 102 (2009) 160602.
