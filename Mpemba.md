# The Mpemba effect — anomalous relaxation as a closure census

> **In one sentence.** Hot water can freeze before cold because *how* a system is prepared matters more
> than *how far* it is from the finish. The [Quantum Logical Framework](README.md) makes that precise:
> two preparations carrying the same energy can need wildly different amounts of room to finish, and a
> high-energy preparation that never uses the slow routes gets there first.
>
> **And it explains the century of contradictory experiments.** The effect is real and it belongs to
> *particular preparations*, not to hot water as a class — so an experiment that controls the temperature
> and lets the preparation vary is sampling a distribution in which most draws show nothing. Averaged over
> preparations the crossing disappears; that is a **prediction here, not an embarrassment**.

**What is on this page.** A machine-verified account of the effect's structure — a no-go telling you which
comparisons can never show it, a theorem making room for it, an exhibited and unbounded family of
instances, and a blind test showing why the ensemble average hides what individual preparations do.
Not a quantitative derivation for water; see [§9](#9-honest-scope--and-what-would-make-this-a-result).

**Module:** [`lean/QLF_Mpemba.lean`](lean/QLF_Mpemba.lean) — machine-verified, no axioms
**Blind test:** [`mpemba_census.py`](mpemba_census.py)
**Companions:** [`lean/QLF_ClosureDepthLaw.lean`](lean/QLF_ClosureDepthLaw.lean) (relaxation time *is* the maximum excursion) · [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) (capacity) · [`Philosophy.md`](Philosophy.md) §3a (the method) · [`Entropy.md`](Entropy.md) · [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md)

---

## 1. The everyday effect

Hot water, under some conditions, freezes before cold. Read naïvely — a state farther from equilibrium
arriving sooner — it sounds paradoxical, and for decades the argument was about which mundane mechanism
(evaporation, convection, dissolved gas, supercooling, container coupling) was *the* cause.

Modern work changed the question. The approach to equilibrium is not one race down one track; it is a
sum over **relaxation modes**, some fast and some slow, and what governs the finish is how much of your
starting state sits on the *slow* ones. A hotter preparation can arrive first simply by having less
weight there. In the **strong Mpemba effect** that weight is zero: the slow channel is not merely small,
it is absent, and the speed-up is exponential.

**So the lesson is not about heat.** It is that *distance from equilibrium does not determine relaxation
time.* Something finer does — and that finer thing is what this page makes countable.

<details>
<summary><b>The mode-sum, formally</b></summary>

Write the approach to equilibrium as

$$
\delta p(t) \;=\; \sum_n a_n(X_0)\, e^{-\lambda_n t}\, v_n ,
$$

and the late-time behaviour is governed by the slowest surviving mode. A hotter preparation arrives first
if its amplitude `a_slow` on that mode is smaller; the strong effect is `a_slow = 0` outright (Lu–Raz;
Klich–Raz–Hirschberg–Vucelja). It has been realised in controlled systems — colloidal and trapped-ion —
precisely by engineering the initial state's overlap with the slow mode.

</details>

---

## 2. The picture, in one analogy

> Two people leave a large building.
> One starts **farther** from the exit but stands in an open corridor.
> The other starts **closer** but is in a maze of locked side rooms.
> The farther one can still get out first.

Distance to the exit is the macroscopic variable — temperature, energy, "how far from equilibrium".
Corridors and mazes are the **pathways**. The Mpemba effect is what happens when the pathway structure
outweighs the distance, and the whole content of the sections below is: on this substrate, the pathways
are *countable*, so which preparations can outrun which stops being a matter of interpretation.

---

## 3. What the substrate says

Three plain statements come first; the formal versions follow.

1. **Reaching equilibrium is not modelled here — it *is* closure.** A history settles when its open
   possibilities have all been matched off. Nothing needs to be added to make "relaxation" meaningful.
2. **The time it takes is the deepest excursion the history ever makes.** Not an average, not a fitted
   rate: the furthest the walk ever strays from balance is exactly the capacity needed to finish, and
   exactly how many passes it costs. That is a theorem, not a modelling choice.
3. **Some preparations never use the deep routes at all.** Those finish early regardless of how much
   energy they carry — which is the whole effect, stated without heat, water, or eigenvalues.

The theorem behind point 2, from [`QLF_ClosureDepthLaw`](lean/QLF_ClosureDepthLaw.lean):

> `closedAtHorizon R s ↔ maxExcursion s ≤ R`

**relaxation time = closure depth = the maximum excursion of the phase walk.** Every question about
anomalous relaxation therefore becomes a question about a *census of excursions* — decidable, not
interpretive.

<details>
<summary><b>The technical translation: the closure-depth census</b></summary>

Following the mode picture, define for a preparation `X` the **closure-depth census**

$$
W_X(d) \;=\; \bigl|\lbrace \text{real histories from } X \text{ that first close at depth } d \rbrace\bigr|,
$$

the cumulative fraction closed by capacity `R`,

$$
F_X(R) \;=\; \frac{\sum_{d\le R} W_X(d)}{\sum_d W_X(d)},
$$

and a **closure latency** `τ_X = min{R : F_X(R) ≥ ½}`. `F_X` is exactly a **listening** in this
repository's sense ([`Philosophy.md`](Philosophy.md) §3a rule 2): the capacity-relative count, what a
horizon of capacity `R` actually receives. A **QLF Mpemba effect** is then `τ_H < τ_C` while `H` is the
farther preparation by some macro measure. A useful companion quantity is the discrete **closure hazard**
`Γ_X(R) = W_X(R)/∑_{d≥R} W_X(d)` — of the histories still unresolved at `R`, what fraction close now.

</details>

---

## 4. What is proven

Three machine-verified statements ([`QLF_Mpemba`](lean/QLF_Mpemba.lean), no axioms). They do **not** all
point the same way, which is why they are worth having.

### (a) Measure the distance wrong and the effect is impossible

**In words.** If "farther from equilibrium" means the history's own imbalance, then a farther state can
*never* finish first — not rarely, never. The walk has to travel at least as far as its own imbalance,
so relaxation is bounded below by the distance.

**Formally** — `relaxation_ge_distance`: `|level s| ≤ maxExcursion s`, via `level_le_hmax` (the excursion
is a maximum over prefixes).

**Why it earns its place.** It disciplines everything after it: *any* Mpemba claim on the substrate must
name a distance measure that is not the imbalance. A no-go is what tells you where to stop looking.

### (b) No single number decides how long relaxation takes

**In words.** Two preparations can carry the same energy and sit the same distance from balance, and
still finish at completely different times — one in a single pass, the other needing `n`. So the
macrostate scalar you would naturally reach for provably does not determine the answer. **That is the
room an anomalous ordering needs.**

**Formally** — `equal_length_unequal_relaxation`: at one length `2n` with identical (zero) imbalance, the
pair matching `[+−][+−]…` closes in **one** pass while the nested singlet `[+ⁿ −ⁿ]` needs **`n`**
(`nested_relaxes_slower`).

### (c) The strong effect, translated: an empty sector, not a vanishing eigenmode

**In words.** Arrange a preparation so that *every* one of its histories stays shallow, while a rival
still has some deep ones. Then at that capacity the first is completely finished and the second is not.
The spectral condition "the slow mode has zero amplitude" becomes a plain counting condition: **the deep
sector is empty.**

**Formally** — `strong_mpemba`: if every history of `H` satisfies `maxExcursion ≤ R` while some history of
`C` exceeds `R`, then at capacity `R` the `H` preparation has fully closed and `C` has not, so
`a_slow = 0` becomes

$$
W_H(\text{deep sector}) \;=\; 0 ,
$$

with no appeal to eigenmodes — the deep sector being exactly the large-excursion histories the depth law
identifies.

---

## 5. The blind test — why the effect is hard to duplicate

The criterion is sharp: if an anomalous ordering appears only after the multiplicities have been arranged
to produce one, this is an interpretation of Mpemba, not a derivation. So
[`mpemba_census.py`](mpemba_census.py) draws preparations **uniformly** at a fixed macro parameter, with
nothing tuned about their depth distribution:

| length (energy) | 8 | 16 | 24 | 32 | 48 | 64 |
|---|---|---|---|---|---|---|
| median relaxation | 2 | 3 | 4 | 4 | 5 | 6 |

**No crossings in the median.** Relaxation is monotone in the macro parameter, so the effect does *not*
fall out of a scalar energy averaged over preparations. Stated plainly because it is the honest result —
and because it is the informative one: **this is the substrate's account of why the effect is so hard to
duplicate.** An experiment that fixes the temperature and lets everything else vary is averaging over
exactly this distribution, and the average is flat.

The spread underneath that flat median is enormous, which is the other half of the story: at length 32 the
depth ranges **1 … 13** over 20,000 uniform draws, and the constructible extremes are **1** (pair
matching) and **16** (nested singlet). A scalar macro variable is sitting on top of a census whose values
differ by an order of magnitude — so *individual* comparisons swing wildly while the mean says nothing.

### 5a. The effect is real: individual preparations cross, and often

The monotone medians are a statement about the *ensemble*. The effect is not an ensemble property, and at
the level where it actually lives — particular preparations against particular preparations — it is
there, provably and measurably.

**Proven, and unbounded** (`mpemba_instance`, `mpemba_ordering`): for every `d > 1` and `n > d`, two
balanced preparations closing to the *same* equilibrium, where the one with **more energy** closes
**faster** —

| | preparation | energy (length) | relaxation |
|---|---|---|---|
| hot | pair matching of `n` pairs | `2n` | **1** pass |
| cold | nested fold `[+^d −^d]` | `2d < 2n` | **`d`** passes |

so e.g. 10× the energy closing 10× faster, with the ratio arbitrary.

**And not only for constructed extremes.** Drawing both preparations *uniformly*, a higher-energy history
closes strictly faster with substantial probability:

| energy ratio | 2× (32 vs 16) | 2× (64 vs 32) | 2× (128 vs 64) | 4× (64 vs 16) | 4× (128 vs 32) |
|---|---|---|---|---|---|
| P(hot closes strictly faster) | 0.131 | 0.146 | 0.165 | 0.027 | 0.030 |

A witness found by unbiased search — four times the energy, closing two passes sooner:

```
hot  (length 64, depth 3): +--+--+++----+++---+-+-++-+++---++-+-++-++---+-++++-+-----++++--
cold (length 16, depth 5): ---+-+---+++-+++
```

So the position is sharper than either "no effect" or "hot freezes faster": **the crossing is a real
property of individual preparations and not of the uniform ensemble.** One draw in six or seven at a 2×
energy ratio, and any ratio you like if you are allowed to choose the preparations — but wash the
preparations out and the signal goes with them.

That is precisely how the laboratory effect behaves. Mpemba experiments compare specific preparations, and
their results are famously sensitive to preparation, container, observable, and cooling history; a
consistent effect at fixed temperature is exactly what this census says **should not** be expected.
**Irreproducibility is the signature, not the refutation.**

---

## 6. A trap the substrate makes explicit: comparing different destinations

An earlier version of the test compared time-to-fixpoint across preparations of *differing* imbalance and
produced a striking crossing: median relaxation fell from 4 to 1 as the imbalance rose. It was an
**artifact**, and the substrate says exactly why.

An unbalanced history **never closes**. It stalls at an irreducible core of `|imbalance|` same-sign
twists. So comparing "time until nothing further happens" across preparations of different imbalance
compares arrival at *different destinations* — the fast ones were not reaching equilibrium at all, they
were reaching their own dead ends sooner.

This is the substrate form of the experimental literature's hardest methodological problem: **what does
"freezes first" mean?** Results there depend heavily on the chosen observable and on preparation, and a
2024 experiment attributed much of the apparent variation to differing cooling rates from uncontrolled
convection. The contribution here is not a new mechanism but a sharp statement of the trap: *a relaxation
comparison is only meaningful between preparations that close to the same equilibrium* — on the
substrate, between balanced histories.

---

## 7. Laser cooling — the same census, engineered on purpose

Laser cooling is the clean counterpart, and it is *not* the same mechanism as Mpemba: it **engineers** the
relaxation pathways rather than exploiting an accident of preparation. Red-detuned light makes an ion
preferentially scatter in ways that remove motional energy; in sideband cooling the cycle
`|g,n⟩ → |e,n−1⟩ → |g,n−1⟩` walks the vibrational ladder down. The rate depends on which states the field
couples — transition structure, resonance, selection rules — not on stored energy alone.

In this framework that reads as **engineered multiplicity bias**: the field reorganises the census so that

$$
W(\text{energy-lowering histories}) \;\gg\; W(\text{energy-raising histories}),
$$

and then the method's rule applies unchanged — *what happens in the most ways happens first*
([`Philosophy.md`](Philosophy.md) §3a). Resonance is already a ways-count in this repository:
[`QLF_LineSpectra`](lean/QLF_LineSpectra.lean) shows the joint closure completes in many ways on
resonance and few off it.

**And it suggests the better experiment.** A trapped-ion ladder is an explicitly controllable transition
network, so its multiplicities can be *written down* rather than guessed — unlike freezing water, where
convection, evaporation, dissolved gas and nucleation are all in play at once. The decisive test of
[§4(c)](#c-the-strong-effect-translated-an-empty-sector-not-a-vanishing-eigenmode) would be a laser-cooled
ladder prepared so that the slowest closure class has multiplicity **zero**, and checking whether the
strong-Mpemba point sits where the census says it must.

---

## 8. Why water may have no single cause

Heating changes convection, evaporation and hence mass, dissolved-gas content, nucleation structure,
molecular correlations, and boundary coupling — all at once. The long search for *the* mechanism assumes
these compete.

On the possibilist reading they need not: they are **different ways of altering the same closure-depth
census**. Nothing happens one way; every generable way is real, and what happens in the most ways happens
first. So "what causes the Mpemba effect?" may be the wrong question, with different preparations
realising the crossing through different mechanisms while one condition stays invariant:

> the hotter preparation carries **more multiplicity in fast-closing sectors**, and/or **less in the
> slowest**.

This is offered as a *reading*, not a result. It is consistent with the experimental messiness rather than
explanatory of it, and it makes no quantitative prediction about water.

---

## 9. Honest scope — and what would make this a result

**Proven** (no axioms): the imbalance no-go (`relaxation_ge_distance`); the scalar underdetermination that
makes anomalous ordering possible at all (`equal_length_unequal_relaxation`); the sector translation of the
strong effect (`strong_mpemba`); and an *instance* with an unbounded family behind it, energy as the
distance (`mpemba_instance`) — plus the measured fact that uniform draws cross 13–17% of the time at a 2×
energy ratio ([§5a](#5a-the-effect-is-real-individual-preparations-cross-and-often)). **So the effect is
exhibited on the substrate, not merely permitted.**

**The stance this supports.** The Mpemba effect is real, it is a property of preparations rather than of
temperatures, and its reputation for irreproducibility follows from that rather than counting against it.
An experiment that controls only the macro variable is averaging over a census whose depths span an order
of magnitude, and the average is flat by construction.

**Not proven, and not claimed:** an *ensemble* effect, and any quantitative statement about water. Median relaxation is monotone
in energy, so the crossing lives between individual preparations; whether energy is an admissible distance
measure is exactly what thermomajorization asks of the ordinary effect; and no quantitative claim about
water is made here. What this page supplies is an **ontology, proven scaffolding, and exhibited instances**
— not a derivation of the laboratory phenomenon. Calling it a solved mystery would be the overclaim this
repository's method forbids.

**What would make it a result** — a concrete, falsifiable target:

1. Compute an actual `W_X(d)` census for a *physically specified* preparation (the trapped-ion ladder of
   [§7](#7-laser-cooling--the-same-census-engineered-on-purpose) is the tractable candidate) and show the
   conventional slow-mode amplitudes **emerge** from it — ideally `a_n ∝ Σ_{h ∈ mode n} W(h)·φ(h)`, with
   `φ` the `μ₂` phase that [`QLF_BalancedPhaseReal`](lean/QLF_BalancedPhaseReal.lean) proves closures
   carry.
2. Show that a preparation with suppressed deep-closure multiplicity is *precisely* the one with a
   suppressed slow eigenmode — not merely analogous to it.

If that works, the claim becomes strong and specific: **relaxation eigenmodes are the continuum rendering
of multiplicity classes of real histories.** If it does not, this remains an ontology for anomalous
relaxation plus a proven no-go — worth having, and less than a solution.

---

## Take-away

> - Relaxation speed is set by **pathway structure**, not by distance from equilibrium — the corridor
>   beats the maze.
> - On this substrate the pathways are **countable**, so the question becomes decidable: relaxation time
>   *is* the deepest excursion a history makes.
> - Measure "distance" as imbalance and the effect is **impossible** — a proven no-go that tells you which
>   comparisons are worth running.
> - Same energy, same imbalance, relaxation differing by a factor of `n` — **no scalar decides it**, which
>   is exactly the room the effect needs.
> - The effect is **real but preparation-specific**: individual preparations cross often (13–17% at 2×
>   energy) and constructed ones by any ratio you like, while uniform ensembles show **no crossing at
>   all** — which is why it is so hard to duplicate. Irreproducibility is the signature, not the
>   refutation.
> - Freezing water is **not** derived here. The tractable decisive test is a trapped-ion ladder, where the
>   multiplicities can be written down instead of guessed.

---

## 2026 update

Two 2026 results give this document's "hidden census" a concrete candidate in water. Stockholm
located a liquid–liquid critical point near 210 K and 1,000 atm, and a Hong Kong machine-learning study
found two interconverting local structures, one dense and one open and tetrahedral. Two samples at
one temperature can therefore differ in structure fraction, which is the kind of preparation
dependence the stance here requires. `density_maximum` (`QLF_Discoveries2026`) proves that the
density maximum needs the second structure ([Discoveries_2026 V2](Discoveries_2026.md#v2)). Open: a closure census
that fixes the 4 °C maximum and predicts which preparations cool fastest.

## References

Confident: R. Lu & O. Raz, *PNAS* **114**, 5083 (2017) — Markovian Mpemba and its inverse.
I. Klich, O. Raz, O. Hirschberg & M. Vucelja, *Phys. Rev. X* **9**, 021060 (2019) — the Mpemba index and
anomalous relaxation. A. Kumar & J. Bechhoefer, *Nature* **584**, 64 (2020) — Mpemba in a colloidal
system.

Reported in the survey that prompted this document, and **not independently verified here** — treat the
locators as provisional: a trapped-ion *inverse* Mpemba demonstration (*PRL* **133**, 010403); a
thermomajorization formulation removing the arbitrary distance measure (*PRL* **134**, 107101); a
non-Markovian quantum Mpemba mechanism at exceptional points (*PRL*, 2026); and a 2024 APS March Meeting
water experiment attributing much apparent variation to convection-driven cooling-rate differences.
