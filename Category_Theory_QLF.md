# The category-theoretic structure of QLF

Category-theoretic structure surfaces all over QLF, each time introduced ad hoc for one job: a free
monoid here, a fibration there, a Tannakian category in the Millennium program, a dagger involution in
the process algebra. This doc collects them into one picture and says, for each, whether it is
**proven** (machine-checked), **structural** (a faithful reorganisation of proven results), or
**speculative** (a direction, not a claim).

> **Binding frame (method rule 4, [`Philosophy.md`](Philosophy.md) §3a).** Category theory here is a
> *description*. It introduces no axiom, changes no count of ways, and predicts nothing on its own. Its
> value is that it names the structure the proven results already have — and, in one place (the
> bifibration → self-similarity chain, §3), turns an empirical null into a structural consequence.

Companion to [`Grothendieck_QLF.md`](Grothendieck_QLF.md) (the Millennium/Tannakian layer, largely
built) and [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) (the emergence ladder, ℕ upward).

---

## 1. The base category — the causal set of events

**Objects:** events, `Event α := List α` (a finite history of closure steps; `α` the twist alphabet).
**Morphisms:** reachability, `reachable A B := A <+: B` (list-prefix), one arrow `A → B` iff `A` is a
prefix of `B` ([`lean/QLF_ReachableEvent.lean`](lean/QLF_ReachableEvent.lean)).

This is a **thin category** (at most one arrow between any two objects) — equivalently a **poset**:
`reachable_refl`, `reachable_trans`, `reachable_antisymm` are all machine-checked. It is the
**pre-geometric causal set**: no metric, no coordinates, order *is* causal order
([`QFT_QLF.md`](QFT_QLF.md) §1a). The `futureCone A := {B | reachable A B}` is the representable
presheaf / the principal up-set at `A`.

**Status: proven.** The poset laws are Lean theorems. Reading it as "a category" adds nothing the poset
did not already say — which is the point of a thin category.

**The observer group acts on it, and the closure structure is invariant.** A change of observer frame
is an element of the discrete symmetry group (the 48 signed axis permutations × the gauge swap,
`QLF_BasisIndependence`). It acts on histories by relabeling, and **the ZFA closure verdict and the
phase of a closure are fixed points** — `closure_verdict_frame_independent`, `phase_frame_independent`,
so `observers_agree` ([`lean/QLF_MultiObserver.lean`](lean/QLF_MultiObserver.lean), no axioms). In
categorical terms the frame group acts by automorphisms of the census, and `countBalanced` /
`twistMatrixFold` are the invariants of that action — the closure and its phase are **objective**, the
same from two or more perspectives, and witnessed *two independent ways* (the count route and the
Pauli route). "Truth is what closes" is therefore not observer-relative.

### 1a. Histories under composition — the free monoid

Closures concatenate. `List α` under `++` with `[]` as unit is the **free monoid on `α`**
([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) Rung 2) — associativity and identity for free,
no relations. As a **one-object category** (the delooping `B(List α)`) its single hom-set is all of
`List α` and composition is `++`. Counting is a monoid homomorphism `List α → ℤ` (counts add over
`++`), and the signed action vector is a homomorphism `List Twist → ℤ⁴`.

**Status: proven** (`Mathematics_From_QLF.md` Rung 2; the homomorphism property is `count_append`-style
lemmas in `QLF_Axioms`).

---

## 2. ZFA as a universal property

`achieves_ZFA s` is `full_zeno_prune s = []` — and the count part, `count_pos s = count_neg s` on every
axis, is exactly an **equalizer**:

$$
\text{ZFA-balanced histories} \;=\; \mathrm{eq}\!\left( \; \text{List Twist}
\;\rightrightarrows\; \mathbb{Z}^4 \; \right), \qquad
\text{the two maps: } s \mapsto (\#{\uparrow}-\#{\downarrow},\,\dots) \ \text{ and } \ s \mapsto 0.
$$

The signed-action homomorphism and the zero homomorphism agree exactly on the count-balanced histories;
that subobject is their equalizer in **Mon** (and in **Set**). Since **count balance ⟹ Pauli closure**
(`count_balanced_pauli_closed`, [`QLF_TwistAlphabet`](lean/QLF_TwistAlphabet.lean)), this single
equalizer *is* full ZFA — the second conjunct is entailed, not a separate condition.

**Its geometry, read off** ([`Closure_Walk.md`](Closure_Walk.md)): the signed-action hom lands in `ℤ⁴`, so a history is a lattice path and the equalizer is the set of *closed walks* on `ℤ⁴`; the fibre over `x` is the set of paths ending at `x`, and `h(x, t)` = its cardinality at length `t` is what `/solve` maximises and the uniform sampler follows. The Pauli phase is not a function on the base — it is a `ℤ₂` cocycle on the Cayley graph (π flux through every mixed spatial plaquette), so the *signed* census is the equalizer lifted to the double cover.

**`full_zeno_prune` as a reduction.** It rewrites a history to a normal form by cancelling adjacent
conjugate pairs; the ZFA-closed histories are its fibre over `[]`. It is the substrate's
**normalisation functor** onto reduced words — the analogue of free-group reduction. Whether it is
literally the counit of a **coreflection** (a right adjoint to the inclusion of reduced words) is
**not yet checked**; the reduction is confluent and terminating (RCA₀, `QLF_QuCalc`), which is the
hypothesis such a statement would need.

**Status: structural** (the equalizer reading is a faithful restatement of `count_balanced_pauli_closed`
+ the definitions). **Open:** the coreflection/adjunction claim for `full_zeno_prune` — a candidate
Lean target, and the sharpest concrete question in [#155](https://github.com/rchain-community/quantum-logical-framework/issues/155).

---

## 3. The grading and the bifibration

QLF grades histories three equivalent ways ([`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md)
§1): by **capacity horizon** `R` (`closedAtHorizon`, max excursion), by **diagram order** `o`
(`IsDiagram`, [`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean)), by **closure depth**. Each is a
**functor to `(ℕ, ≤)`**, and `closedAtHorizon_mono` ([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean))
is its functoriality: once closed at `R`, closed at every `R' ≥ R`.

Over that grading the substrate carries **two** lifting operations:

| direction | operation | in QLF | turbulence reading |
|---|---|---|---|
| **cartesian** (pullback / restrict) | `R+1 → R` | the `--listening` capacity restriction ([`contextual_census.py`](contextual_census.py)); `closedAtHorizon R` | *integrating out* the deep closures (Wilsonian) |
| **cocartesian** (pushforward / extend) | `R → R+1` | `ClosureSpectrum.Z_succ` ([`QLF_ExactRG`](lean/QLF_ExactRG.lean)); the `IsDiagram` binding & nesting clauses | *adding a shell* to the RG flow |

Together they are a **bifibration** over the grading poset. The colimit of the cocartesian tower is
`QLF_ExactRG`'s `Z(∞)` — the bare, un-renormalised theory — and it is **finite** (`Z_le_one`,
`twist_kraft`): the bifibration's total space has bounded fibres.

### 3a. Why the bifibration is *load-bearing* (self-similarity is downstream of it)

This is the one place category theory does more than relabel. In the possibilist view the bifibration
is **one thing that happens**: closures factor **uniquely** into ordered sequences of primes
([`Alpha_Residual.md`](Alpha_Residual.md) §4), so the primes generate a **free monoid** and the
cocartesian lifts (append a prime) are unique. That forces the resummation identity
`G(x) = 1/(1 − I(x))` (`census_irreducible_resummation`, [`QLF_AlphaBound`](lean/QLF_AlphaBound.lean),
**proven**), hence a **geometric** generating function, hence a **linear** coefficient recurrence
`G_m = Σ_j I_j G_{m−j}`, hence the constant ratio-4 growth `C(2n,n) ~ 4ⁿ` — **scale-invariant
self-similarity**, every fibre again the whole structure.

Consequences, stated as they are used elsewhere:

* **Self-similarity is a *theorem*, not an observation** — it is the shadow of the free-monoid
  bifibration ([`Philosophy.md`](Philosophy.md) §3a: *self-similar things dominate existence*;
  [`self_similar_closures.py`](self_similar_closures.py): the Thue–Morse closure `+--+-++-` is
  self-similar at the string *and* prime-factorisation level, and there are unboundedly many).
* **No bifurcation.** A linear recurrence has no period-doubling, so the **log-periodic /
  discrete-scale-invariance channel is closed by structure** — which is why the α-residual weight
  `w = 1/2` is a *structural consequence*, not merely a measured null
  ([`Alpha_Residual.md`](Alpha_Residual.md) §2a, §9b; [`genesis.py`](genesis.py)).

**Status: proven** (`census_irreducible_resummation`, `Z_succ`, `closedAtHorizon_mono`) for the pieces;
**structural** for "these two lifts are a bifibration" and the self-similarity chain. This chain is the
main result of the doc.

---

## 4. The Tannakian / motivic / anabelian layer

Already largely built ([`Grothendieck_QLF.md`](Grothendieck_QLF.md)):

* **A Tannakian category of motives** with a **motivic Galois group** — `MotiveAut` (tensor
  automorphisms of the fibre functor) is a genuine **group**, machine-checked (`comp`/`id`/`symm`,
  `comp_assoc`, `symm_comp`, `comp_symm`), non-trivial, with the Tate object the trivial representation
  ([`QLF_MotivicGalois`](lean/QLF_MotivicGalois.lean)).
* **The `H ↔ H†` involution** is that layer's **duality** — the Tannakian/adjoint symmetry, the same
  self-dual locus behind the Riemann critical line and the BSD central point
  (`millennium_involution_unified`, [`QLF_AnabelianGalois`](lean/QLF_AnabelianGalois.lean)).
* **The anabelian functor** `closurePi1 : Event → Set(Event)` (a closure ↦ its future-cone causal
  groupoid) is **fully faithful** — `anabelian_fully_faithful`, `closurePi1_injective`,
  `reachable_iff_pi1_subset` ([`QLF_Anabelian`](lean/QLF_Anabelian.lean)): the geometry is recovered
  from the combinatorial closure.
* **Profinite étale `π₁`** — an inverse limit of finite covers, profinite by construction
  (`etale_pi1_profinite_in_progress`).

**Status: proven** for the group structure and the fully-faithful functor; **one axiom** each in the
Millennium bridges (the Class-A boundaries — [`CLAUDE.md`](CLAUDE.md) axiom inventory), which is where
the open-conjecture content sits, not the category theory.

---

## 5. RhoQuCalc as the internal language — a dagger symmetric monoidal category

`RhoProcess` with `eval` into 2×2 matrices ([`BraKetRhoQuCalc.md`](BraKetRhoQuCalc.md)) is exactly the
shape of **Abramsky–Coecke categorical quantum mechanics**:

| RhoQuCalc | categorical role | `eval` |
|---|---|---|
| `action f` (ket `\|ψ⟩`) / `lift f` (bra `⟨ψ\|`) | generating morphisms | `f.toMatrix` / `f.toMatrix†` |
| `sequence p q` | composition `∘` | `p.eval * q.eval` |
| `parallel p q` | the monoidal sum `⊕` (superposition) | `p.eval + q.eval` |
| `dagger p` | the **dagger** `(-)†` — an involutive, identity-on-objects, contravariant functor | `(p.eval)†` |

`eval_dagger` (`(dagger p).eval = (p.eval)†`) and the Hermitian-pair structure make `†` a genuine
dagger. `bra_ket_always_balanced` says every constructible `RhoProcess` is ZFA-balanced — the internal
language **cannot express an unbalanced term**, the syntactic form of "possibility is the free monoid,
ZFA is the only filter." Curry–Howard closes the loop: in QuantumOS a **capability name is a proof**
(possessing the name = a proof of authorisation, [`QuantumOS.md`](QuantumOS.md)).

**Status: structural** — the dagger/monoidal reading is a faithful restatement of the `eval` laws and
`eval_dagger`; a full Lean statement "RhoProcess/≈ is a †-SMC" is not written (the quotient by
`eval`-equality is the missing step, cf. [#152](https://github.com/rchain-community/quantum-logical-framework/issues/152)).

---

## 6. The internal logic — the orthomodular lattice `MO2`

The propositions of a ZFA system form the **minimal quantum logic `MO2`** — the height-2 orthomodular,
non-distributive lattice `0 < {x, x⊥, z, z⊥} < 1` — machine-verified complete and axiom-free
([`QLF_QuantumLogic`](lean/QLF_QuantumLogic.lean): `le`, `sup`, `inf`, `compl` all by `decide`;
`orthomodular`, non-distributivity). This is the **subobject structure** of the base category read
logically: incompatible closures (x-spin vs z-spin) are the incomparable atoms.

**Status: proven** for `MO2` (the minimal case); **open** is the general representation theorem — that
an *arbitrary* orthomodular ZFA proposition lattice embeds into a projection lattice (`QLF_QuantumLogic`
§ honest scope).

---

## 7. The picture, and what is genuinely open

**One diagram.** The free monoid of histories (§1a), filtered by the ZFA equalizer (§2), graded to
`(ℕ,≤)` and carrying the restrict/extend bifibration (§3), whose prime-factorisation is free (§3a) —
that free-ness forcing self-similarity and killing the log-periodic channel. On the realised
(closed) objects: the causal-set poset (§1), its anabelian `closurePi1` functor and the motivic Galois
group acting through `H↔H†` (§4), the `MO2` internal logic (§6), and RhoQuCalc as the †-SMC internal
language (§5).

**Genuinely open (Lean targets, roughly in order of tractability):**

1. **`full_zeno_prune` as a coreflection** (§2) — is reduction-to-normal-form a right adjoint to the
   inclusion of reduced words? The confluence/termination hypotheses are in hand.
2. **The bifibration, formalised** (§3) — the grading functor to `(ℕ,≤)` and the cartesian/cocartesian
   lifts as a Lean structure over `QLF_ExactRG` + `QLF_HorizonClosure`.
3. **`RhoProcess/≈` is a †-SMC** (§5) — needs the quotient by `eval`-equality
   ([#152](https://github.com/rchain-community/quantum-logical-framework/issues/152)).
4. **The general orthomodular representation theorem** (§6) — the hard one; a real research problem, not
   a formalisation exercise.

None of these changes a physical prediction. What they would buy is a single verified statement of the
structure that is currently assembled from a dozen modules — and, for (1) and (2), a cleaner home for
the self-similarity result that already does real work in the α-residual program.

---

## See also

- [`Grothendieck_QLF.md`](Grothendieck_QLF.md) — the motivic/anabelian/Tannakian layer in full.
- [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) — how ℕ, the ring, `μ₄`, su(2)/su(3), the
  continuum emerge; the free monoid is Rung 2.
- [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) §3 — the bifibration in the RG context.
- [`Alpha_Residual.md`](Alpha_Residual.md) §3a, §9b — the bifibration → self-similarity → `w = 1/2`
  chain doing work.
- [`Philosophy.md`](Philosophy.md) §3a — *self-similar things dominate existence*; §3 the *ex falso*
  inversion; §9 the dialectic correspondence and its one-directional framing rule.
- [`lean/QLF_QuantumLogic.lean`](lean/QLF_QuantumLogic.lean) · [`lean/QLF_Anabelian.lean`](lean/QLF_Anabelian.lean) ·
  [`lean/QLF_MotivicGalois.lean`](lean/QLF_MotivicGalois.lean) · [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean) ·
  [`lean/QLF_ReachableEvent.lean`](lean/QLF_ReachableEvent.lean) — the anchors.
- Issue [#155](https://github.com/rchain-community/quantum-logical-framework/issues/155) — the spec this
  doc answers.
