# The Interpretations of Quantum Mechanics, Compared

QLF's possibilist ontology ([`possibilist-ontology.md`](possibilist-ontology.md)) already implies a
reading of quantum mechanics; this document places that reading against the standard interpretations. The
**Many-Worlds** comparison is developed in full below, because that is where the
[`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) does its sharpest work; the others are summarized with
pointers to where each is developed.

## 1. At a glance

| Interpretation | Ontology of the wavefunction / possibilities | QLF's difference | Key doc |
|---|---|---|---|
| **Copenhagen** | epistemic / instrumental; no reality below measurement | possibilities are *ontic* until ZFA closure; measurement is just another closure — no collapse | [`Measurement_Problem.md`](Measurement_Problem.md) |
| **Many-Worlds (Everett)** | all branches actual, on equal footing | only ZFA-closed histories become actual, and they are **capacity-ordered** — modal first, deferred later, the infinite tail pruned | this doc §2 · [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) |
| **Bohmian (pilot-wave)** | particles + a real guiding wave in configuration space | no hidden variables or configuration space; particles *are* the closed twist loops | [`possibilist-ontology.md`](possibilist-ontology.md) |
| **Transactional (RTI)** | possibilities as *res potentia* (offer/confirmation waves) | ZFA = the completed transaction | [`possibilist-ontology.md`](possibilist-ontology.md) |
| **QBism / Relational** | subjective / informational | objective logical possibilities, independent of any observer; the Born rule is *derived*, not imported | [`Born_Rule.md`](Born_Rule.md) |
| **Superdeterminism** ('t Hooft, Hossenfelder–Palmer) | a deterministic hidden state, *correlated with the measurement settings* — statistical independence denied | QLF shares the deflation of "free choice" (a setting is a closure inventory, not an exogenous variable) but has **no hidden values to correlate**; independence of preparation and apparatus is the *factor* structure, and the Bell escape is contextual, not conspiratorial | this doc §5 · [`Entanglement.md`](Entanglement.md) §6 |
| **QLF** | **constructive possibilist**: all admissible histories real until ZFA = 0 | — | [`possibilist-ontology.md`](possibilist-ontology.md) |

## 2. Many Worlds, in order

**The reading.** Possibilism already asserts the Everett premise: every ZFA-closing history is real *a
priori* ([`Philosophy.md`](Philosophy.md) §3) — the full free monoid of eight-twist strings that balance,
nothing discarded. What standard many-worlds does *not* supply, and QLF does, is an **order**. The
multiplicity principle ([`Philosophy.md`](Philosophy.md) §3a) makes a closure's frequency **its census
count of ways**; the modal closures — shallow, maximal-multiplicity — therefore happen **first**, and
within any finite capacity `R` ([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean),
[`QLF_Realizability`](lean/QLF_Realizability.lean)) their relative measure approaches `1` while every
other closure's approaches `0`.

> **The probability of what closes in the most ways is one; every other universe is zero — *relative to
> a listening capacity*, not absolutely.**

That qualification is the whole point. A closure the horizon cannot receive is not *unreal*; it is a zero
**listening** — the count exists, the capacity misses it ([`Philosophy.md`](Philosophy.md) §3a rule 2).
Everett's branches are co-equal and unordered; QLF's are stratified by the excursion budget that receives
them.

**Where the Law of Exceptions does the work.** [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §2 proves
that for **every** finite `R` there is a constructed history — `[+^(R+1) −^(R+1)]` — invisible at
capacity `R` and *genuinely closing* at `R+1`. Those deeper closures are exactly the low-multiplicity
exceptions of [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4: multiplicity falls rapidly with depth
([`QLF_ClosureDepth`](lean/QLF_ClosureDepth.lean) — `2ⁿ` ways at depth one, two at maximal depth), so
they are the histories that happen **last**. The two claims then fit without strain:

* **within our finite horizon** the exceptions remain measure-zero — "they never happen in our time";
* **they are real ZFA events nonetheless**, admitted the moment the budget expands, and
  [`no_final_closure`](lean/QLF_LawOfExceptions.lean) guarantees **no finite horizon is final** — the
  census never saturates, so the deferred is deferred only as long as the horizon is what it is.

**Two zeros, and only one is "deferred."** "They do eventually happen" must not be overread, because there
are *two* kinds of zero here and only one is a deferred event:

* **The deferred zero** is a *finite* closure deeper than our horizon — `[+^(R+1) −^(R+1)]` at capacity
  `R`. It is a real event, admitted at `R+1`
  ([`no_exception_to_unbounded_closure`](lean/QLF_LawOfExceptions.lean)). Every finite ZFA closure is of
  this kind: a finite history has a finite `maxExcursion`, and
  [`closedAtHorizon_iff_maxExcursion_le`](lean/QLF_ClosureDepthLaw.lean) admits it at exactly that
  capacity. So **no finite universe is never-realized** — "not in our time" is always a finite deferral.
* **The pruned zero** is the *unbounded* tail — the infinite, non-terminating histories whose phase walk
  never returns. Those are realized at **no** finite capacity, but not because they are deferred: they are
  **not events at all**. [`qlf_universality`](lean/QLF_Universality.lean) admits exactly the terminating
  computations and prunes the rest before they can become physical ([`Philosophy.md`](Philosophy.md) §1,
  the ultraviolet catastrophe). They are *potential* infinity — the future open, always extensible —
  never *actual*: QLF has no completed infinity ([`Philosophy.md`](Philosophy.md) §1).

[`no_final_closure`](lean/QLF_LawOfExceptions.lean) sits exactly on this seam: the hierarchy never
saturates, so at every horizon there is always a real closure we have not yet realized — yet each such
closure is finite and will be realized at its own depth. What is *never* realized is the completed
totality, the limit of the ladder, which QLF does not count as a thing at all. The many-worlds reading is
therefore not "all branches eventually happen"; it is **"every finite branch happens at its own capacity,
and the infinite remainder is not a branch."**

**"Our time" is a clock, not a stage.** By [`Philosophy.md`](Philosophy.md) §2, time is *synthesized* by
the capacity we inhabit — a local clock, not a global theatre on which branches wait in the wings. So
"not in our time" is not a fact about a preferred frame; it is the observation that a deeper closure
needs a larger excursion budget, and a larger budget is a *different local clock*. Expand the capacity and
the previously-zero alternatives acquire non-zero measure and are realized. This is the proton again
([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4a): cold proton decay is a zero-listening exception at
the capacities we inhabit — QLF predicts its absence *there* — while deconfinement and the sphaleron are
the same closure family becoming real once temperature supplies the budget.

**What this buys over bare MWI.** Standard many-worlds inherits three bookkeeping problems: a preferred
basis to pick, an infinite measure to normalize, and the equal reality of branches whose weight is
absurdly small. The capacity reading dissolves all three — not by fiat, but by what is already proven:

| MWI problem | QLF answer |
|---|---|
| preferred basis | the basis is the **census strata** — depth and excursion, counted in [`QLF_ClosureDepth`](lean/QLF_ClosureDepth.lean), not chosen |
| infinite measure | every *listening* is finite (`closedAtHorizon R` admits a finite set); the infinite census is never what an observer holds |
| equal reality of negligible branches | negligible branches are **real but deferred** — measure-zero within our horizon, non-zero beyond it; "rare and certain" ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4) |

The only absolute filter remains ZFA itself ([`Philosophy.md`](Philosophy.md) §4), which bounds no
capacity; everything below it is horizon-relative, and the Law of Exceptions proves every such horizon is
provisional.

**Honest scope.** What is proven is the substrate statement — the capacity hierarchy is strict and
exhausted by no finite closure — and the census strata it orders. The "one vs zero" phrasing is the
multiplicity reading of [`Philosophy.md`](Philosophy.md) §3a, consistent with the measure settled in
[`Born_Rule.md`](Born_Rule.md) §8 and the decoherence cutoff of [`Decoherence.md`](Decoherence.md) §4a.
This comparison is a *reading* of those results, not a further theorem, and it does **not** touch the
still-open amplitude question ([`Born_Rule.md`](Born_Rule.md) §8): the ordering of *which* worlds close
first is the counting side, while *how much* weight a closing branch carries remains the open half. The
two are adjacent and must not be merged — the stratification is real and proven; the Born weight on top
of it is not yet.

## 3. Copenhagen, and the collapse it postulates

Copenhagen makes the wavefunction epistemic and introduces collapse as an unexplained measurement event.
QLF drops both: possibilities are ontic (possibilism) and a measurement is just another ZFA closure — the
observer's own unresolved prefix composing with the system's open paths. There is nothing to collapse.
The full treatment is [`Measurement_Problem.md`](Measurement_Problem.md).

## 4. QBism, and the Born rule it imports

QBism reads the Born rule as an agent's Bayesian credence, not a fact about the world. QLF keeps the
observer-relative *conditioning* (the Markov blanket's local possibility tree) but makes the underlying
ensemble objective, and derives the Born rule from it rather than postulating it. The full treatment, and
the open questions it still carries, is [`Born_Rule.md`](Born_Rule.md).

## 5. Superdeterminism, and the free variable it correlates

Superdeterminism keeps **both** locality and realism in Bell's theorem by giving up the third
assumption — *statistical independence*, Bell's own "free variables" (1977): the hidden state `λ` is
correlated with the settings `(a,b)`, so pre-assigned local values reproduce the correlations after all.
The standing objection is that the correlation is unexplained and looks fine-tuned — the "conspiracy"
charge (Shimony–Horne–Clauser 1976; the sympathetic modern treatment is Hossenfelder & Palmer 2020).

QLF is regularly *read* as superdeterministic, and the reading deserves a precise answer, because it is
right about the ontology and wrong about the mechanism.

**What QLF shares — the deflation of free choice.** There is no exogenous free variable anywhere in the
framework. A setting is not an input from outside physics: an **apparatus is a closure inventory** and an
observer is only a *perspective*, a finite listening capacity
([`ScientificApproach.md`](ScientificApproach.md) §1b, [`Philosophy.md`](Philosophy.md) §3a rule 2).
Nothing chooses; there is no observer potency to be placed outside the census, and a measurement is a
joint closure between histories rather than an intervention on one. That much of the superdeterminist's
ontology QLF asserts outright — and it is why the Conway–Kochen free-will theorem finds nothing to bite
on here: neither experimenter nor particle carries potency, both are closures.

**What QLF does not share — and this half is decisive.** Superdeterminism's *mechanism* is a correlation
between the setting and a **pre-existing** state. QLF has no such state to correlate. There are no
pre-assigned values on unmeasured axes: `σx` and `σy` at one site do not both hold values, because the
algebra is non-commutative and each axis is a **different closure with its own admissible branch set**
([`Entanglement.md`](Entanglement.md) §6). QLF's Bell escape is therefore the **contextual/algebraic**
one — locality kept, naive realism dropped — not the measurement-independence one. No step in the
derivation of the correlations uses a setting–state correlation, and none would be repaired by adding
one.

**Statistical independence is not sacrificed here; it has an algebraic home.** Preparation and apparatus
are specified **independently** and their censuses enumerated that way — that is literally how
[`contextual_census.py`](contextual_census.py) is built. The substrate reason is
[`indexed_factors_commute`](lean/QLF_IndexedFactors.lean): operators on distinct factors commute, so an
apparatus on its own factor cannot steer the system's census — what it does is select which *joint*
closures happen. Entanglement is exactly the residue that fails to factorize
([`shared_closure_not_factorizable`](lean/QLF_IndexedFactors.lean)) — a shared **past**, not a shared
setting ([`Entanglement.md`](Entanglement.md) §5–6). So measurement independence is a feature of the
factor structure rather than a postulate QLF must give up.

**And the determinism is a different kind.** QLF is not a single-history theory: everything happens every
way that closes; ZFA decides what closes first, and what happens in the most ways happens most often
([`Philosophy.md`](Philosophy.md) §3a).
The determinism is **relational and global** — the census is determinate and its ordering is determinate
([`UniversalRelativity.md`](UniversalRelativity.md) §6a) — while *which* outcome is had is a perspective
inside that census (§2 above), not a value fixed in advance by correlated initial data. Superdeterminism
buys one actual world by correlating hidden data; QLF has all closing worlds, capacity-ordered, and needs
no correlation to buy anything.

**The agency corollary.** None of this touches agency, which is the capacity to *do* — and doing is
closing. What the absence of potency rules out is the libertarian metaphysics of the will, not the
ability of a system to act; determinist traditions have always carried both. Worked out in
[`Philosophy.md`](Philosophy.md) §3c, along with the separate point that an agent is *undeterminable*
from outside.

**Placement.** Superdeterminism is a **neighbour, not a label QLF wears**: nearest at exactly one joint
(no exogenous free variable), different at the two that carry Bell's theorem (no hidden values, no
setting–state correlation), and free of the fine-tuning charge because it never incurs the debt. It sits
with 't Hooft's cellular automaton in [`Related_Frameworks.md`](Related_Frameworks.md) §6 — a discrete
substrate that runs everything, where QLF adds the selection principle that decides what closes.

## See also

* [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §2, §4, §4a — the capacity formulation, "rare and
  certain", and the proton ladder this reading rests on.
* [`possibilist-ontology.md`](possibilist-ontology.md) §3 — the ontology-level comparison this document
  expands.
* [`Measurement_Problem.md`](Measurement_Problem.md), [`Born_Rule.md`](Born_Rule.md),
  [`Decoherence.md`](Decoherence.md) — the adjacent readings.
* [`Entanglement.md`](Entanglement.md) §5–6 — the shared-past account of the correlations and the
  non-commutativity that supplies the Bell violation without hidden variables.
* [`Related_Frameworks.md`](Related_Frameworks.md) §6 — the discrete-substrate neighbours ('t Hooft,
  Fredkin, Wolfram) and the superdeterminism row.

### External

* Bell, J. S. (1977). *Free variables and local causality.* Epistemological Letters 15 — the
  statistical-independence assumption named.
* Shimony, A., Horne, M. A. & Clauser, J. F. (1976). *Comment on "The theory of local beables."*
  Epistemological Letters 13 — the conspiracy objection.
* Conway, J. & Kochen, S. (2006). *The free will theorem.* Found. Phys. 36, 1441.
* Hossenfelder, S. & Palmer, T. (2020). *Rethinking superdeterminism.* Front. Phys. 8, 139.
* 't Hooft, G. (2016). *The Cellular Automaton Interpretation of Quantum Mechanics.* Springer.
