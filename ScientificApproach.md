# The Scientific Method of the Quantum Logical Framework

**How conjectures are generated, tested, rejected, and promoted to results.**

This document is about *method*, not results. It states the rules by which the
[Quantum Logical Framework](README.md) decides what it knows, what it merely suspects, and what it
has ruled out. The evidence ledger lives in
[`Experimental_Consistency.md`](Experimental_Consistency.md), the unresolved questions in
[`Open_Problems.md`](Open_Problems.md), the ontology in [`Philosophy.md`](Philosophy.md), and the
domain derivations in their own documents. Keeping those separate is itself part of the method: a
file that mixes protocol with claims will always end up grading its own work.

> **The point of this file:** QLF should document not merely why it might be right, but exactly how
> it permits itself to be wrong.

---

## Glossary — the vocabulary this document uses

Defined here so this file can be read on its own, without the rest of the repository. Each term links
to where the object is defined or proved.

| Term | What it is |
|---|---|
| **Twist** | One of the eight elementary distinctions `^ v < > / \ + −` — the substrate's alphabet. Each is a *signed Pauli frame element* (`^ = +σ_y`, `> = +σ_x`, `/ = +σ_z`, `+ = +I`, and their negations): [`twist_core.py`](twist_core.py), [`QLF_TwistAlphabet`](lean/QLF_TwistAlphabet.lean) |
| **History** | A finite word over the alphabet — one *way* something can happen. Not a path through a pre-existing space; space is a reading of the history, not its container |
| **Free action `F(h)`** | The unbound part of a history: its total conjugate-pair imbalance, defined in §1a |
| **ZFA · closure** | `F(h) = 0` — every distinction matched by its conjugate. A history achieving it **closes** and persists as an event. Operationally `full_zeno_prune s = []` ([`QLF_QuCalc`](lean/QLF_QuCalc.lean)) |
| **Fold · Pauli closure** | The matrix product of a history's twists. Count balance *entails* that the fold is a Pauli scalar `{±I, ±iI}` — [`count_balanced_pauli_closed`](lean/QLF_TwistAlphabet.lean) |
| **Event** | A closure, and nothing else. No separate collapse, no observer act ([`Philosophy.md`](Philosophy.md)) |
| **Census · inventory** | Exhaustive enumeration of ways, graded by length, depth and phase — [`census_inventory.py`](census_inventory.py). §8 explains why the inventory **is** the apparatus |
| **Multiplicity** | How many ways a closure happens. A closure's frequency *is* its multiplicity ([`Philosophy.md`](Philosophy.md) §3a) |
| **Capacity `R` · horizon** | A finite closure capacity — the deepest excursion a perspective can hold (`closedAtHorizon_iff_maxExcursion_le`). An axis of the census, not a fact about minds |
| **Listening** | What a horizon of capacity `R` *receives*, as against what exists. Capacity-relative; a count is absolute |
| **First closure** | The absorbing reading: a run stops at its first closure, because a closure *is* an event. First closures are prefix-free |
| **Cylinder measure** | `μ(h) = 8^{−|h|}` — the measure Kraft's inequality **forces** on prefix-free first closures ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)). Derived, not chosen; the worked standard of §5 |
| **Substrate · rendering** | The substrate is the finite combinatorial layer (`RCA₀`); a *rendering* is a continuum description read off it. The continuum is a rendering, never an ingredient ([`TheContinuum.md`](TheContinuum.md)) |
| **Bridge** | A map from substrate structure to a physical observable. §5 is the protocol that governs them, and it is where circularity enters if it enters at all |

---

## 1. The premise, and the ontological floor

### 1a. ZFA — what it is, where it came from, and why it is still on trial

**Zero Free Action (ZFA)** is the framework's single premise. *Free action* is the unbound part of a
history: on the 8-twist alphabet each conjugate pair (`^`/`v`, `>`/`<`, `/`/`\`, `+`/`−`) carries a
running imbalance, and the free action is their total magnitude,

$$
F(h) \;=\; |n_{\uparrow} - n_{\downarrow}| \;+\; |n_{\rightarrow} - n_{\leftarrow}| \;+\;
|n_{\nearrow} - n_{\swarrow}| \;+\; |n_{+} - n_{-}|
$$

writing $n_x$ for how many times twist $x$ occurs, one term per conjugate pair.

A history **achieves ZFA** when `F(h) = 0` — every distinction it opened has been matched by its
conjugate, so nothing is left outstanding. That is count balance, and count balance *entails* the
order-sensitive condition too: `count_balanced_pauli_closed` proves every count-balanced history
folds to a Pauli scalar. Operationally, `full_zeno_prune s = []`.

**Where the premise comes from.** It is the substrate reading of **least action**. Physical systems
select histories that extremise action; the substrate's version is sharper and simpler — a history
persists as an event exactly when its *free* action is zero, `S = ∫ℒ dΩ` with `ℒ = 0`
([`Lagrangian_Formulation.md`](Lagrangian_Formulation.md)). Least action is the evidence that
suggested ZFA; ZFA is the discrete condition proposed to underlie it. The derivation now exists for the
unsigned census: the closure is the stationary mode of the multiplicity, and a biased alphabet breaks it
([`Stationary_Action.md`](Stationary_Action.md), `QLF_StationaryAction`).

**Its epistemic status, by this document's own labels: a standing premise under continuous test —
and it stands uncontradicted so far.** It is not an axiom held beyond question. Every invariant
asserted against fresh enumeration, every Lean theorem built on closure, every empirical match in
[`Experimental_Consistency.md`](Experimental_Consistency.md) is a test of it, and the
**predicted-absent list** ([`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §6) is where it is
most exposed: proton decay, a magnetic monopole, a light sterile neutrino, or any persistent state
requiring an unmatched history would contradict it directly. That the premise has survived every
such test to date is a result about the premise, not a licence to stop testing it.

> **Kill condition for the premise itself:** a persistent physical event that requires a history with
> non-zero free action.

### 1b. The floor that follows

Three further commitments are load-bearing for everything below. They are stated once here, in the
form the method actually uses; the full case is in [`Philosophy.md`](Philosophy.md).

**Generable ⟹ real; ZFA decides closure, not existence.**

$$
\text{generable history} \;\Longrightarrow\; \text{real way} \;\xrightarrow{\;\text{ZFA}\;}\;
\text{closed, persistent physical event}
$$

Every history the substrate can generate is a real way. ZFA closure does not decide which histories
*exist* — it decides which ones **persist as events**. This is why census methods are legitimate at
all: counting ways is counting something real, not tallying hypotheticals.

**Information physics is primary** ([`Information_Physics.md`](Information_Physics.md)). The
substrate is informational; matter, geometry, and duration are *readings* of closure structure, not
additional ingredients. This is Wheeler's "it from bit" made constructive [W90], with the classical
notions — Shannon count [Sh48], Landauer's erasure cost [La61], the Bekenstein bound [Be81] —
sitting on the substrate as *inherited*, *derived*, or *rendering-layer* objects, each classified
there rather than assumed here. When a question can be posed as a
question about information — how many ways, carrying what phase, closing at what depth — that is the
level at which it should be answered, and any answer that needs an extra physical postulate has
probably been posed at the wrong level.

**An apparatus is a closure inventory; an observer is a perspective.** There is no observer potency
in QLF, and the method must not smuggle any in. A measurement is a **joint closure** between
histories — nothing causes it, and nothing about it requires an agent. What we call an *apparatus*
just **is** an inventory of closures: the set of histories that can close jointly with the system,
which is precisely what [`census_inventory.py`](census_inventory.py) and
[`contextual_census.py`](contextual_census.py) enumerate. An **observer** adds only a *perspective* —
a finite closure capacity, a listening ([`Philosophy.md`](Philosophy.md) §3a rule 2) — and that
perspective may simply *be* the apparatus. Nothing in a derivation may depend on an observer beyond
the capacity that fixes which closures are received.

**Consequences for wording.** Never write that a measurement happens "when an observer looks", that
possibilities are "merely potential until observed", or that an apparatus "chooses" an outcome.
Write instead: which histories close jointly, at what capacity, in how many ways.

### 1c. The assumption budget

"One premise" is a true statement about **selection** and it should not be made to carry more than
that. ZFA is the single principle deciding *what persists*; it is not the source of the substrate's
**structure**, and it says nothing about **interpretation** — how a substrate object corresponds to a
laboratory quantity. Those are three different kinds of commitment, and running them together is how
a framework comes to look either more assumed or more derived than it is. The budget below counts
them separately, and it is meant to be read as a live ledger: an item's row changes when the work
changes it.

| Item | Kind | Status |
|---|---|---|
| The information atom is a **two-valued** distinction | structural primitive | **Proved in-frame** — `spin_half_is_information_atom` ([`QLF_SpinorInformation`](lean/QLF_SpinorInformation.lean)) |
| An elementary distinction **is a signed element of the observable frame** | structural posit | **Open** — the residual left by the necessity attack below; the one place "8" still rests on a choice |
| The **8-twist alphabet** | derived structure | **Quantized, not chosen** — the alphabet is the signed axis frame, so `\|Σ\| = 2·\|axes\|`, and a composition-closed axis set is a subgroup of the Klein four-group: `\|Σ\| ∈ {2,4,8}`, **six is impossible**, and two distinguishable spatial axes force eight ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean), [`alphabet_necessity.py`](alphabet_necessity.py), [`eight-twists-sufficiency.md`](eight-twists-sufficiency.md) §7) |
| **Conjugate pairing = negation** | definition | Formal — the four pairs are exactly the four axes (`toSignedAxis_conj`), which is why `F(h)` has four terms |
| `F(h)`, and `F(h) = 0` | definition | Formal |
| **ZFA selects what persists** | **the premise** | Standing, under continuous test; kill condition in §1a |
| Generable ⟹ real way | ontology | Interpretive commitment (§1b) — not testable in isolation, load-bearing for census methods |
| **A closure *is* an event** (absorbing/first-closure reading) | event semantics | Physical hypothesis — adopted after the alternatives were rejected (§11) |
| First closures are **prefix-free** | mathematical claim | **Proved** |
| `8^{−\|h\|}` is the cylinder measure | mathematical claim | **Proved** given uniform generation (Kraft/McMillan, [`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) |
| **cylinder measure = event probability** | **physical bridge** | **Open** — the measure is derived; its identification with probability is not. This is the Born frontier (§14) |
| capacity = apparatus resolution | physical bridge | Partially developed — capacity is an inventory axis (§8), which constrains it more than a free parameter |
| twist geometry = physical orientation | physical bridge | **Open** — the context-geometry layer; a word is a history, not a direction |
| substrate event scale = **Planck scale** | dimensional bridge (calibration) | One calibration; by §5 each dimensionful observable is allowed exactly one, and they are counted |
| ZFA ⟹ continuum variational mechanics (`ℒ = 0`) | physical bridge | Open ([`Lagrangian_Formulation.md`](Lagrangian_Formulation.md)) |
| The named Millennium axioms | open bridges | **Measured**, individually, by R6a — see the axiom inventory in [`CLAUDE.md`](CLAUDE.md) and [`Open_Problems.md`](Open_Problems.md) |

Two things this exposes that prose was hiding. The alphabet was carrying a **sufficiency** argument
where it reads as a necessity one — now half-closed, with the residual named. And the row that most
looks like a result, the cylinder measure, is *two* rows: a proved measure and an open bridge.

---

## 2. A new kind of science — on a pruned ruliad

The method here is recognisably in the lineage of *A New Kind of Science* [Wo02]: study a computational
substrate by **enumerating what it does**, rather than by writing down equations and solving them.
Wolfram's ruliad — the entangled limit of all possible rules, all possible computations — is the
right object to have identified. QLF's disagreement is not with the object but with the claim that
the object is already physics.

**The ruliad is unpruned. Physics is not.** By §1, every generable history is a real way, so the
ruliad is real in full; but only histories that reach zero free action **persist as events**. What
QLF studies is therefore the ruliad **filtered by ZFA** — and `qlf_universality` proves the filter
discards no computable physics: every *terminating* computation is already a ZFA string, so what is
pruned is the non-terminating, undecidable, Busy-Beaver tail that could never have been an event
anyway.

$$
\text{ruliad} \;\xrightarrow{\;\text{ZFA}\;}\; \text{the pruned ruliad} \;=\; \text{the physical census}
$$

**Pruning is what makes the science tractable, and it is a methodological point, not a
philosophical one.** Three things become available on the pruned side that do not exist on the
unpruned one:

1. **A measure.** The full ruliad has no canonical measure over its histories — which is why
   "typical rule behaviour" arguments there stay qualitative. Prune to *first closures* and the
   surviving set is prefix-free, so Kraft's inequality [Kr49, McM56] hands over the cylinder measure `8^{−|h|}`
   with nothing chosen ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)). **Selection is what buys
   probability.**
2. **Finiteness at each capacity.** A closure horizon of capacity `R` receives a *finite, decidable*
   set of histories (`closedAtHorizon_iff_maxExcursion_le`), so a claim about the census can be
   settled by exhaustive enumeration rather than by exhibiting a suggestive picture.
3. **A falsifier.** Because the census is complete at each length and capacity, a conjecture can be
   *killed* by the inventory — as most of them have been (§11).

**What QLF inherits from NKS, and must guard against.** The characteristic failure mode of
computational exploration is mistaking a suggestive computation for a law: a picture that looks like
a pattern, a plateau that looks like a limit. Rules **R4** and **R5** exist for exactly this reason,
and both were written after that failure mode bit — a growth constant read at depth 90 that
evaporated by depth 200, and a float census whose roundoff was reporting itself as the answer.
Enumeration is a *generator* of candidates here, never a certifier; certification is Lean.

**Where the observer goes.** NKS makes the observer's computational boundedness central to how the
ruliad is sampled. QLF keeps the boundedness and drops the anthropic framing: by §1 an observer
contributes only a **capacity**, and capacity is an axis of the inventory itself, not a fact about
minds. The apparatus is a closure inventory; the observer is a perspective on it; sampling the
pruned ruliad is a physical relation between histories, not an act of observation.

---

## 3. Epistemic status — two axes

Every claim in this repository carries a status, and the status is not decorative: it determines what
may be built on top of the result. **The status has two axes, and they must be stated separately,**
because they answer different questions — *what is established about the formal object* and *what is
established about the world*. A single column forces those into one verdict, which is exactly the
ambiguity that makes a machine-checked theorem look like a physical result, or a genuine theorem look
like a hedge.

**Axis 1 — mathematical status.** What is established about the formal object.

| Status | Meaning | May be built on? |
|---|---|---|
| **Proved** | Machine-checked Lean theorem, assumptions explicit, axioms named | Yes, freely |
| **Exact computational result** | Exhaustive enumeration or exact rational/integer computation over a stated finite domain | Yes, within that domain |
| **Numerical evidence** | Finite computation suggesting a pattern, no convergence guarantee | Only as motivation |
| **Conjecture** | A proposed generalisation, stated so it can fail | No — state it as an open item |

**Axis 2 — physical status.** What is established about the world. Every arrow in the bridge chain of
§5 has to be typed before this column can be filled in honestly.

| Status | Meaning | May be cited as evidence? |
|---|---|---|
| **Derived bridge** | The substrate→observable map is *forced*, not chosen (the standard: the Kraft measure, §5) | Yes — this is the strongest physical status QLF has |
| **Pre-registered prediction** | Bridge frozen (named commit) before the comparison; consequence not used in constructing it | Yes, and it is the only status that can *confirm* |
| **Retrodiction** | Correct, but the construction was made with the target number in view (R0a) | As consistency only — never as confirmation |
| **Consistency** | Agrees with known physics; mechanism or uniqueness not established | Cite as consistency, never as derivation |
| **Open bridge** | The argument needs a connection it does not have (the named axioms) | Only with the bridge named at each use |
| **Predicted absent** | A falsifiable null: the substrate says the thing does not exist | Yes — this is where the premise is most exposed |
| **Internal** | A fact about the substrate with no physical claim attached | Not applicable — and say so rather than leaving it blank |

**Axis 3 is the record**, and it applies to either axis: **Rejected route** (a candidate tested
against its kill condition and failed — keep it, it constrains the next attempt) and **Superseded**
(an earlier conclusion overturned by a better computation — keep it, with what failed and why).

Worked examples, in the form claims should actually carry:

| Claim | Mathematical | Physical |
|---|---|---|
| `count_balanced_pauli_closed` | **Proved** | **Internal** — a substrate fact, no bridge involved |
| `\|Σ\| ∈ {2,4,8}`, six impossible ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)) | **Proved** | **Internal** — it constrains the *budget*, not an observable |
| `hodge_realized_on_substrate` | **Proved** | **Open bridge** — `substrate_realization_is_algebraic` |
| `gaugeMassGap = log 2 > 0` | **Proved** | **Open bridge** — the identification with the continuum gap |
| `π` and `ζ(3)` from the census | **Exact computational** | **Consistency** |
| `137 < α⁻¹ < 137.048` | **Proved** | **Retrodiction** — the comparison target was known |
| `α(0)` carries no cosmological drift | **Proved** | **Predicted absent** — falsifiable, sharper than the SM |
| `μ(h) = 8^{−\|h\|}` | **Proved** | **Derived bridge** for the measure; the *identification with probability* is a separate row, and it is **Open** |

That last line is the pattern the two-axis split exists to make visible: one sentence was doing the
work of two claims with different statuses.

A programme that keeps producing *rejected routes* while its proved core grows is progressive in
Lakatos's sense [La78]; one that keeps rescuing a claim by adjusting what it means is degenerating.
The labels exist so the difference is visible from the outside — and §7 states the criterion that
decides which of the two this programme is.

Two rules govern the labels:

> **Numerical agreement is not a proof.**
> **Construction proves possibility, not uniqueness** — exhibiting a way something *can* happen never
> shows it is the only way ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md)).

---

## 4. Core methodological rules

**R0 — Pre-register the bridge.** Before any substrate result is compared with a measured number,
state, in this order and in the document that will make the claim: the **physical inputs** held
fixed; their **substrate representation**; the **calculation**; the **observable-extraction rule**;
the **tolerance**; the **comparator** (what the number is being compared against, and its
uncertainty); and the **kill condition**. §7’s blind-battery discipline already enforces this
*inside* the census; R0 is the same discipline applied across the substrate→laboratory arrow, which
is where circularity enters if it enters at all.

> **A formal consequence of the substrate becomes physical evidence only when the
> substrate-to-observable bridge was specified independently of the observation used to test it.**

The issue is never the theorem. It is whether the physical interpretation was fixed independently of
the result it is used to support.

**R0a — The discovery/confirmation firewall.** Anything constructed while the target number was in
view is a **retrodiction**, permanently, and is labelled so on the physical axis of §3 — however
exact, however natural the construction looks. A construction becomes capable of *prediction* only
once it is **frozen**, and freezing is a git fact rather than a rhetorical one: name the commit, and
claim as predictions only those consequences that were not used in building it. The standing case is
α's `+0.036` residual, which is to be **derived, never fitted**; a construction tuned to it would be
a retrodiction even if it landed on every decimal.

**R1 — Inventory before interpretation** (Chamberlin's multiple working hypotheses [Ch1890]). When a question reduces to the finite substrate census,
ask the complete accessible inventory before proposing a mechanism. Constructed examples demonstrate
*possibility*; census statistics test *generality*. The inventory has repeatedly caught claims that
would otherwise have become documentation — including an incorrect `μ₂` phase-factorization claim
that the enumeration rejected on sight.

**R2 — No free fitted kernels.** A contribution rule, weighting, or partition chosen to make the
answer come out is a fitted parameter, however natural it looks. Weightings must be *derived* (the
cylinder measure `8^{−|h|}` is forced by prefix-freeness and Kraft) or the result is bookkeeping
([`Philosophy.md`](Philosophy.md) §3a rule 4).

**R3 — Symmetry-locked agreement is not evidence.** If a proven symmetry forces the number, obtaining
that number tests implementation consistency and nothing else.

> A prediction forced by an already-imposed symmetry does not independently confirm the theory.

`P(+) = P(−) = ½` under an exact branch-exchange symmetry is a regression check, not a Born-rule
result. Every agreement must be checked for this before it is counted.

**R4 — Exact arithmetic before float inference.** Signed censuses run in exact integers or rationals
wherever practical. Floating-point asymptotics need an independent check: a signed transfer-matrix
census is contaminated past `k* ≈ 16 ln 10 / ln(λ₁/λ₂)`, where roundoff — which overlaps the dominant
subspace — is what the answer reports. That failure mode is not hypothetical; it produced a confident
wrong conclusion in this repository.

**R5 — Transient behaviour is not an asymptotic law.** Do not read a limiting constant off a
finite-depth plateau. A growth-rate claim needs at least one of: stability under increasing depth,
term-ratio stabilisation in the tail, a recurrence, the transfer-operator spectrum, an exact
characteristic polynomial, or rigorous bounds. Measured example: the same geometry reads `8.16` at
depth 90 and `0.19` at depth 200.

**R6 — When a model fails, identify *which layer* failed.** A census model has at least three
independent layers — the **measure** over ways, the **phase/amplitude** rule, and the **context
geometry** (how a physical arrangement is encoded). Changing all three at once until the answer
appears is fitting. Establish them separately, and when something breaks, name the layer.

**The rule does not stop at the census.** The same discipline applied to the whole stack gives three
kinds of failure, which have entirely different consequences and must never be run together:

| Failure | What broke | What follows |
|---|---|---|
| **Formal** | The claimed result does not follow from the definitions | Fix the proof. Says nothing about physics |
| **Bridge** | The substrate→observable map was wrong; the substrate is untouched | Fix or abandon *that bridge* — and **record it**, because the count of abandoned bridges for one target is itself evidence (§7) |
| **Substrate** | Every admissible, independently specified bridge fails to reproduce an established phenomenon — or a frozen prediction is contradicted | ZFA is wrong |

R6's three census layers are the fine structure of the middle row. Collapsing the rows in either
direction is a mistake with a name: reading a bridge failure as *"the experiment disagreed, so ZFA is
false"* discards the framework for an encoding error, while reading a substrate failure as *"only
that encoding failed, try another"* is the move that makes a theory unfalsifiable. §7 states when the
second reading has been used up.

**R6a — Measure an assumption's strength; do not describe it.** Zero `sorry` says every goal was
closed and nothing about *what* closed it, so an assumption has to be tested the way a hypothesis is.
The test is one question: **is the interface satisfied by a trivial reading?** Bundle the assumption
into a structure and try to build an instance out of nothing.

The answers sort into kinds that had previously been run together, and the sorting is the point:

| the toy model | reading | what to do |
|---|---|---|
| builds, and the assumption was already superseded | it excludes nothing and something else does the work | **delete it** — an axiom that assumes nothing is not a boundary, it inflates the count while carrying none of the weight |
| builds, but the claim is a real theorem the formalisation cannot state | **cited, not posited** — vacuous *in Lean*, not *in the world*; discharge is labour with a known answer | keep, and label |
| builds, and the intended reading is what nobody has established | the assumption's force is entirely interpretive | keep, and record the measurement beside it so it stops looking like it does work |
| **does not build, because nothing is left to choose** | every object is concrete; the gap is labour, not knowledge | **the standard** — compare new boundaries against it |

Two supporting rules. *Merging assumptions is legitimate only with a proved equivalence* — otherwise
it is a smaller number and the same commitment. And *"construct an inhabitant" does not always
discharge*: a satisfiable interface is evidence only when its instances are hard to come by, so
building the toy is what tells you which case you are in, and there is no way to know in advance.

Read the dependency footprint afterwards rather than trusting the source: an absent `propext` in a
`#print axioms` report is the signature of a pure application — the "theorem" restates its axiom.
Machinery: [`scripts/axiom_audit.sh`](scripts/axiom_audit.sh) pins what exists to be assumed,
[`lean/QLF_AxiomAudit.lean`](lean/QLF_AxiomAudit.lean) reports what the proofs actually consume.

**The rule applies to new work, not only to inherited work** — and that is the part that is easy to
skip. The same pass that removed a vacuous colour claim from the axiom inventory saw one written
back in hours later (`3 = 3` by `rfl`, with prose beside it claiming something the theorem never
touched). The failure mode is always the same shape: **a true statement adjacent to the one you
wanted, asserted as if it were the one you wanted.**

**R2a — A fitted *mechanism* is a fitted kernel too.** R2 forbids choosing a contribution rule to
make an answer emerge. The same prohibition reaches further than it looks, and the sharpest instance
so far was not a weighting but a **group action**.

Testing whether apparatus blindness is representation-theoretic ([`Born_Rule.md`](Born_Rule.md) §8)
needed the relabeling group to act on the transfer operator. The naive permutation action does not
commute with it. A sign twist restores commutation — and the twist was obtained by *solving* for a
diagonal sign matrix that made `TG = GT` hold. That is under-determined: the constraint graph fixes
signs only up to one choice per connected component. The solution found commuted exactly, closed at
the right group order, and made the hypothesis come out `240/240`, then `1584/1584` under a stronger
test.

It was wrong. Deriving the action instead from the phase rule — `flipX ↦ (−1)^{p_X}`,
`swapXY ↦ (−1)^{p_X p_Y}` — gives a *different* commuting action of the same order, and under it the
hypothesis fails and its kill condition is met. The derived action is the physical one, checked
against ground truth by relabeling every word and rebuilding the census; the solved one was an
artifact.

**The lesson is that "it commutes" was not enough of a constraint, and passing two stress tests did
not detect it** — a fitted object reproduces the data it was fitted to, at whatever scale you test.
The check that caught it was not a bigger sample but an independent derivation: the action had to
come from the phase rule, not from the requirement it was supposed to satisfy. Where a proof needs a
structure, **derive the structure from the substrate and verify it against ground truth; never solve
for the structure that makes the proof work.**

**R7 — State the kill condition first** (Popper's falsifiability [Po59] in Platt's operational
form, strong inference [Pl64]). See §7.

---

## 5. The bridge protocol

A **bridge** is a map from substrate structure to a physical observable. Every empirical claim QLF
makes passes through one, and a bridge is where a formally impeccable result can become a physically
empty one. This section states how they are built and how they are graded.

### 5a. Type every arrow

No bridge is a single step. Write it out as a chain, and label each arrow with what *kind* of step it
is — **definition**, **theorem**, **physical identification**, **calibration**, or **conjecture**:

$$
\text{twist history} \;\longrightarrow\; \text{closure invariant} \;\longrightarrow\;
\text{effective physical variable} \;\longrightarrow\; \text{laboratory observable}
$$

An unlabelled arrow is the failure mode: it lets a definition and a conjecture sit in the same
sentence looking alike. Worked, on the measure:

| Arrow | Kind |
|---|---|
| history ⟶ its first closure | **definition** (the absorbing reading — itself a physical hypothesis, budgeted in §1c) |
| first closures ⟶ prefix-free set | **theorem** |
| prefix-free set ⟶ measure `8^{−\|h\|}` | **theorem** (Kraft/McMillan — nothing is chosen) |
| measure ⟶ **event probability** | **physical identification — open** |

Three arrows are settled and the fourth is the whole Born question. Typing them is what makes that
visible in one glance instead of one paragraph.

### 5b. What information physics already forbids

Because the substrate is informational (§1b), a bridge is not a free function. Four constraints
apply before any physics is done, and together they cut down the admissible maps sharply:

1. **Closure invariants only.** Matter, geometry and duration are *readings* of closure structure, so
   an observable must be a function of closure invariants — count, phase, depth, capacity — and
   nothing else. A bridge that needs an ingredient the substrate does not carry is not a bridge; it
   is a new posit, and belongs in the budget.
2. **Calibrations are countable, and rationed.** Substrate quantities are dimensionless counts, so
   each dimensionful observable requires **exactly one** calibration. A bridge introducing a second
   is fitting under another name. Count them, in the budget, per observable.
3. **Capacity is an axis, not a parameter.** An observer contributes only a capacity, and capacity is
   one of the inventory's own axes (§8). "Tune the capacity until it fits" is therefore not available.
4. **A bridge earns physical content only when it changes a count of ways.** A bridge invariant under
   the census is bookkeeping, however faithful it looks ([`Philosophy.md`](Philosophy.md) §3a rule 4).
   State what distribution over ways the bridge would be *false* for; if the answer is "none", it is
   not a bridge.

### 5c. The ladder, and the standard

Bridges are graded, and the grade is a claim about the bridge, not about the result it produces:

$$
\text{arbitrary} \;\longrightarrow\; \text{pre-registered} \;\longrightarrow\;
\text{constrained} \;\longrightarrow\; \textbf{derived}
$$

**The standard is the cylinder measure.** `μ(h) = 8^{−|h|}` was not chosen, and it was not merely
frozen in advance: prefix-freeness plus Kraft's inequality **forces** it, machine-checked in
[`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean). That is a *derived* bridge, and it is what the top
of the ladder looks like in practice, so every new bridge is placed against it — exactly as R6a
places every new axiom against the case where nothing is left to choose. R2's prohibition on free
fitted kernels is the same demand stated negatively; this states it positively, with a worked
example, so "derived" is a comparison rather than an aspiration.

The point of the ladder is that **freezing an encoding is the weakest acceptable move, not the goal.**
A framework that can only pre-register its interpretations has many encodings available and picks
one; a framework that derives them has few, and that is what makes a substrate theory answerable.
Where a bridge cannot yet be derived, the useful intermediate result is a **constraint**: show which
maps §5b admits, and how few of them there are.

### 5d. Three verifications, not two

> **Lean verifies entailment. The census verifies the substrate's own facts. Experiment verifies the
> bridge.**

The two-part version of this maxim — *proof verifies derivation, experiment verifies interpretation* —
omits QLF's middle term and misfiles everything in it. An exhaustive census is neither a derivation
check nor an experiment: by §8 the inventory **is** the apparatus, so enumerating it is not simulating
an experiment but reading the substrate's own facts, which is why *exact computational result* is a
status in its own right (§3) and why calling that layer "simulation" understates it.

---

## 6. The hypothesis lifecycle

$$
\text{conjecture} \;\to\; \text{census} \;\to\; \text{falsification attempt} \;\to\;
\text{invariant} \;\to\; \text{Lean theorem}
$$

1. **Conjecture** a mechanism, in substrate terms, with its kill condition.
2. **Query the inventory** — does the complete census already refute it?
3. **Compute exactly** over a stated finite domain; assert every relevant proven invariant against
   the fresh data.
4. **Reject** if the census disagrees. Record the rejection; it constrains the next attempt.
5. **Promote surviving patterns** to invariants asserted in the checker, then to Lean theorems with
   explicit assumptions.

A pattern that survives steps 1–4 is *numerical evidence*. Only step 5 makes it **proved**.

---

## 7. Kill conditions and blind tests

Every substantial conjecture states, **in advance**:

> **Candidate** — the proposed mechanism.
> **Prediction** — what it should produce.
> **Kill condition** — what result would reject it.

And where a battery of cases is run, it is run **blind**: all geometries printed together, no
per-case tuning, with the symmetry-lock check of R3 applied to every agreement before it counts.

### 7a. The framework-level failure criterion

Kill conditions on individual claims are not enough. A framework that replaces a failed bridge every
time one fails is protected indefinitely, so the criterion for abandoning **ZFA itself** has to be
stated in advance too. There are two, and the second is the one that does real work.

> **(a) Contradiction.** A frozen, pre-registered prediction (R0a) is experimentally contradicted,
> and the bridge that produced it was **derived or constrained** rather than merely chosen. Equally:
> a persistent physical event requiring non-zero free action (§1a), or an observation of anything on
> the predicted-absent list.
>
> **(b) Degeneration.** For some established phenomenon, the sequence of proposed bridges grows while
> each replacement is selected *after* seeing the previous one fail against the target, without an
> independent computation forcing the change — and the question does not sharpen. That is rescue, and
> a long enough run of it means the substrate is not doing the work.

The conclusion that would follow is worth writing out, because a programme that cannot state it is
not answerable: *ZFA is an interesting mathematical and computational structure, and is not a
fundamental description of physical reality.*

**Self-applied, immediately.** §11's table is **eight discarded encodings for a single target** — the
quantum weight. That is precisely the shape criterion (b) describes, so the programme owes the test
rather than the reassurance. It passes, for two checkable reasons: every rejection was **forced by an
independent census computation** rather than selected by proximity to a target number (the horizon
limits degenerate, capacity provably changes only the rate, `merge_le_sum` is a theorem), and the
sequence **narrowed** — it terminated in a *derived* measure and a sharper question than it started
with. That is exclusion, not rescue.

**A second worked case, now run to conclusion: the α residual.** By 2026 the `+0.036` had accumulated
~seven discarded mechanism swings (weak/W-loop, gauge projection at `3/8`, hypercharge `5/8`,
standalone curvature, the `w = 0.624` weighting, self-similarity×ways, turbulence intermittency —
[`Alpha_Residual.md`](Alpha_Residual.md) §6b, §9b–§9c). Criterion (b) asks whether the count grew
*while the question stayed blunt*. It did not. Each rejection was forced by an independent
computation (the `M_W` threshold; the exact `√62` bracket; an `O(1)`-vs-`O(α_bar)` scale argument; a
converged transfer-recursion census showing no inertial range), and the **question closed**: from
"which partial resummation weights the census" to *`w = 1/2` is structural (the free-monoid/bifibration
proof above), so `α⁻¹ = 137.032` is the pure-ZFA prediction and the last `~0.004` is the continuum
vacuum-polarisation running — the Standard Model's own un-derived frontier.* The final swing even
produced a **side-derivation** (She–Léveque's `C₀ = 2` from `/solve` axis-minimality,
[`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md) §6a). Convergence, not degeneration — but the
count is recorded, per the rule, in `Alpha_Residual.md`.

So the count is kept, and the criterion is the count's meaning: **if the number of discarded bridges
for one target grows while the question does not sharpen and the census stops doing the excluding,
(b) has been met.** Record the number in the owning document, not only the survivor.

---

## 8. The role of the inventory — the apparatus itself

[`census_inventory.py`](census_inventory.py) and [`data/census_inventory.json`](data/census_inventory.json)
hold what enumeration actually discovers: how many ways close, graded by length and depth; which
Pauli phase each carries; what a horizon of capacity `R` receives; and the first-closure event
classes of canonical contexts. It **accumulates** — each run keeps what is stored and computes only
what is missing — and it is a **checker**: every proven invariant is asserted against freshly
enumerated data, so a change that breaks one is caught rather than documented.

By §1 this is not a convenience. **The inventory is what an apparatus is** — the closure structure a
system can jointly close with — so querying it is not simulating an experiment, it is reading the
experiment's own definition. An observer contributes only capacity, and capacity is one of the
inventory's own axes.

---

## 9. The role of formal proof

Lean is where a pattern becomes knowledge. The standard is:

- **zero `sorry`**, repository-wide;
- where a genuinely unprovable step is needed, an **explicit `axiom`** with a name, a home, and an
  entry in the axiom inventory — never a silent assumption;
- assumptions visible in the statement, so a theorem cannot quietly require more than it says;
- CI is the arbiter: a Lean claim is not a result until the build is green.

Proof does not settle physics on its own. It settles what follows from what, which is the part that
should never be in doubt while the physics is argued. **Lean verifies entailment, not
interpretation** — the interpretation is the bridge, and §5 is where it is graded. A `#print axioms`
footprint tells you what a theorem consumed; it cannot tell you whether the theorem is about the
world.

**A proof can upgrade a null.** A measured null — "no effect seen" — is weak evidence: absence at the
depth searched. But when a *proof* shows the effect is **structurally excluded**, the null becomes a
consequence. Worked case: the α-residual weight `w = 1/2` was for a long time a *measured* null (no
preferred octave, no log-periodic line — [`genesis.py`](genesis.py)). Then unique prime factorisation
of closures (`census_irreducible_resummation`, a theorem) → the closures are a **free monoid** → the
census generating function is geometric → a **linear** coefficient recurrence → **no period-doubling**.
A linear recurrence *cannot* carry the discrete-scale-invariance line that would move `w` off `1/2`.
So `w = 1/2` is now a structural consequence, not an observation — and the residual's last piece is
thereby pinned to the continuum sector ([`Alpha_Residual.md`](Alpha_Residual.md) §9b,
[`Category_Theory_QLF.md`](Category_Theory_QLF.md) §3a). The two-axis status of §3 in action: the
*mathematical* fact (free monoid ⟹ no bifurcation) closes the *physical* question (is the weight
tunable?).

---

## 10. The role of numerical simulation

Simulation generates candidates and kills them. It does not establish laws. Its outputs are labelled
*exact computational result* (exhaustive/exact over a stated domain) or *numerical evidence*
(suggestive), never *proved*. Every script that claims an invariant asserts it against freshly
computed data, so the claim and its check ship together.

---

## 11. A worked example — attempting to derive quantum weights

The Born-weight investigation is the clearest illustration of this method, because **most of the
proposals failed**, and the failures are what produced the constraints.

| Candidate | Kill condition | Outcome |
|---|---|---|
| Substrate relabeling *is* the quantum basis change | relabeling must mix amplitude classes | **Rejected** — `QLF_BasisIndependence`: relabeling permutes ways without mixing them |
| Flattening system and apparatus into one algebra caused the wash-out | indexed factors must change the weights | **Rejected** — identical probabilities at every horizon (`QLF_IndexedFactors`) |
| Read the weight at an infinite horizon | a horizon-independent value must exist | **Rejected** — both limits degenerate |
| Finite closure capacity rescues it | capacity must change the limit | **Rejected** — capacity changes only the *rate*; direction is erased at every capacity |
| Continue histories past closure | — | **Rejected as physics** — a closure *is* an event; continuing describes a different, longer history |
| **First joint closure** (absorbing census) | direction must survive | **Survived** — direction restored; the run chooses its own stopping depth |
| The depth weighting must be chosen | a derived measure must exist | **Resolved** — first closures are prefix-free, so Kraft forces `μ(h) = 8^{−|h|}` (`QLF_KraftMeasure`) |
| Normalized event weight (multiplicity × squared mean phase) | must reproduce interference | **Rejected** — provably sub-additive (`merge_le_sum`), so no constructive interference |
| Unnormalized amplitude | must converge | **Partial** — converges for 1.4% of geometries, where interference is exact in both directions |

Two corrections belong to the record as much as the results: a `μ₂` phase-factorization claim caught
by the inventory before it became documentation, and two growth-rate readings withdrawn after R4 and
R5 were applied properly. The current question is no longer *which probability formula to choose* —
it is **what invariant distinguishes the amplitude-summable contexts**, which is a sharper question
than the one the investigation started with.

---

## 12. Negative results and the correction protocol

> **Corrections remain part of the scientific record.** — the discipline Feynman called the
> "utter honesty" of leaning over backwards to show how you may be wrong [Fe74].

When a better computation overturns an earlier conclusion: update the owning document, state plainly
what failed and why, name the new constraint, and leave the commit history intact. Do not quietly
replace a wrong conclusion with a right one — the audit trail *is* the evidence that the method
works. A rejected route is a result: it removes a possibility, which is exactly what a finite search
needs.

**Where a rejection goes.** A rejection earns a place in a narrative document only when it *changes
what is believed* — it retracts a published claim, or it closes a route the document was still
proposing. Everything else belongs in the commit message, where it stays searchable and dated
without interrupting the argument a reader is following. A tested-and-empty feature scan is a
result; it is not a section.

---

## 13. Reproducibility requirements

Every quantitative claim in this repository must be reproducible from the repository:

- the command that produces it, with its arguments, named in the document that makes the claim;
- exact arithmetic where the result is exact, and the tolerance stated where it is not;
- the domain of the computation stated (which lengths, which capacities, which geometries);
- the proven invariants asserted in the same run that produces the numbers;
- Lean claims green in CI before they are cited.

---

## 14. The current frontier

What the method says is *open* right now, stated as it should be stated:

- the amplitude layer — which contexts carry a convergent unnormalized weight, and why the threshold
  is realized rather than straddled ([`Born_Rule.md`](Born_Rule.md) §8);
- the **context geometry** layer — what substrate object represents a physical orientation, given
  that a word is a history and not a direction;
- the named bridge axioms of the Millennium reformulations, each an *open bridge* by §3;
- the **alphabet residual** — the alphabet size is now quantized to `{2,4,8}` with six impossible and
  eight forced by two distinguishable spatial axes ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)),
  so what remains is the one posit underneath it: that an elementary distinction *is* a signed element
  of the observable frame of a two-valued system;
- **not** the α residual's *mechanism* any longer — that investigation converged (§7a): `w = 1/2` is
  structural, and the residual's last piece is the continuum running, the SM's own frontier. The
  perturbation-series / exact-RG side is Lean-anchored ([`QLF_ExactRG`](lean/QLF_ExactRG.lean), no
  axiom); what stays open is the continuum vacuum-polarisation running itself, and the four category-theory
  Lean targets of [`Category_Theory_QLF.md`](Category_Theory_QLF.md) §7 (the `full_zeno_prune`
  coreflection first).

---

## 15. Where the evidence lives

- [`Experimental_Consistency.md`](Experimental_Consistency.md) — the empirical ledger: matches,
  precisions, and the falsifier classes
- [`Open_Problems.md`](Open_Problems.md) — the status registry, closed / bounded / open
- [`Philosophy.md`](Philosophy.md) — the ontology and the multiplicity method
- [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) — physics-facing triage, including what QLF
  predicts is **absent** (the falsifiable nulls)
- [`lean/README.md`](lean/README.md) — every module and its theorems
- [`census_inventory.py`](census_inventory.py) · [`contextual_census.py`](contextual_census.py) — the
  inventory and the contextual layer
- [`alphabet_necessity.py`](alphabet_necessity.py) · [`eight-twists-sufficiency.md`](eight-twists-sufficiency.md) —
  the alphabet's own budget row: why the size is `2`, `4` or `8` and never `6`

---

## References

**Method.**
[Ch1890] T. C. Chamberlin, *The Method of Multiple Working Hypotheses*, Science **15** (1890) 92 —
hold several hypotheses at once so none becomes a pet; the ancestor of R1.
[Po59] K. Popper, *The Logic of Scientific Discovery* (1959) — a claim earns its status from what
would refute it.
[Pl64] J. R. Platt, *Strong Inference*, Science **146** (1964) 347 — the operational form used here:
enumerate alternatives, design the step that excludes one, iterate.
[Fe74] R. P. Feynman, *Cargo Cult Science*, Caltech commencement address (1974) — leaning over
backwards to report what might be wrong; the correction protocol of §12.
[La78] I. Lakatos, *The Methodology of Scientific Research Programmes* (1978) — progressive versus
degenerating programmes, which is what the status labels of §3 make visible.

**Substrate and computation.**
[Wo02] S. Wolfram, *A New Kind of Science* (2002), and the ruliad program — the
computational-substrate commitment and the enumerate-first practice QLF adopts and then prunes by
ZFA (§2). The convergence table in [`README.md`](README.md) places it among the eighteen independent
programs arriving at an informational, computable, closure-bounded reality.
[Si09] S. G. Simpson, *Subsystems of Second Order Arithmetic* (2nd ed., 2009) — the reverse-math
stratification QLF's core works inside (`RCA₀`), and the conservativity results the continuum
argument cites.

**Information.**
[Sh48] C. E. Shannon, *A Mathematical Theory of Communication*, Bell Syst. Tech. J. **27** (1948)
379 — count/multiplicity information and the finite channel capacity.
[Kr49] L. G. Kraft, MSc thesis, MIT (1949); [McM56] B. McMillan, *Two inequalities implied by unique
decipherability*, IRE Trans. Inf. Theory **2** (1956) 115 — the prefix-free inequality that supplies
the closure-depth measure (`QLF_KraftMeasure`).
[La61] R. Landauer, *Irreversibility and heat generation in the computing process*, IBM J. Res. Dev.
**5** (1961) 183 — the `log 2` erasure quantum.
[Be81] J. D. Bekenstein, *Universal upper bound on the entropy-to-energy ratio*, Phys. Rev. D **23**
(1981) 287 — finite information in a finite region, the realizability bound.
[W90] J. A. Wheeler, *Information, Physics, Quantum: The Search for Links* (1990) — "it from bit",
made constructive in [`Information_Physics.md`](Information_Physics.md).

Sources for the *physics* claims live with the claims, in
[`Experimental_Consistency.md`](Experimental_Consistency.md) and the domain documents; this list
covers only the method and the notions it leans on.
