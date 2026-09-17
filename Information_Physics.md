# Information Physics in QLF — what information *is*, and the notions it grounds

> **"It from bit" made constructive.** Information is not a measure laid on top of physics; in
> the [Quantum Logical Framework (QLF)](README.md) it **is** the physics. All computationally
> generable histories exist a priori as *possibility*, and **nothing happens one way — everything
> happens every way that closes**: Zero Free Action (ZFA) decides which possibilities become
> events, and an event's **multiplicity is its frequency — what happens in the most ways happens
> first** ([`Philosophy.md`](Philosophy.md) §3a). Each closure *is* a resolved distinction — one
> realized bit, and the same event may close through many histories. This document collects the many notions of
> information (Shannon, algorithmic, Fisher, von Neumann/quantum, Bekenstein/holographic,
> Landauer, semantic) and shows, with machine-checked proofs where they exist, how each sits on
> QLF's substrate: **inherited** (a measure QLF sits *on*), **derived** (falls out of counting
> closures), or **rendering** (an emergent continuum object).

This is the physics-and-mathematics-of-information companion to
[`Related_Frameworks.md`](Related_Frameworks.md) Part II (which places these notions as a *measure
stack over an unspecified ontology*), [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) (the
emergence ladder), and [`TheContinuum.md`](TheContinuum.md) (why a finite universe cannot hold
continuum information). It gathers the scattered results — [`MRE.md`](MRE.md),
[`Shannon_And_Phase.md`](Shannon_And_Phase.md), [`Shannon_Overfit.md`](Shannon_Overfit.md),
[`Information_Energy_Equivalence.md`](Information_Energy_Equivalence.md),
[`Relative_Entropy.md`](Relative_Entropy.md), [`Entropy.md`](Entropy.md),
[`Born_Rule.md`](Born_Rule.md) — into one map.

---

## 0. The one-paragraph thesis

Existing mathematics of information is a stack of **measure theories over an unspecified
ontology**: Shannon *counts* distinctions, algorithmic information *prices* descriptions, Fisher
*measures* sensitivity, quantum information *ledgers* resources — **none says what a distinction
*is*, or when one has *happened***. QLF supplies that missing bottom layer:

> **Information = realized distinction = closure receipt.** The abstraction (a two-valued
> distinction) is primary; a ZFA closure is its physical *realization*. The atom is the
> **spin-½ closure**, carrying exactly one bit; every richer measure lives on top.

**Three things, kept apart.** Writing `P` for the computationally generable histories, physical
reality is not `P` but the closing subset, and multiplicity is the count over `P`:

```
P        = all generable histories                      — possibility
E        = { h ∈ P : h achieves ZFA closure }            — events (physical reality)
W(e)     = #{ h ∈ P : h closes to e }                    — multiplicity = frequency
```

Non-closing histories remain *pure possibility*, not realized alternatives
([`Philosophy.md`](Philosophy.md) §3) — but the ways an event *does* close are all taken, and their
count is the frequency. Probability is the normalized view of `W` under incomplete information.

**The epistemic consequence, and it binds this whole document.** A finite census establishes a
**lower bound** on multiplicity: exhibiting `N` ways proves *at least* `N` ways, and exactly `N` only
where completeness of the enumerated sector is separately proved. **Construction proves possibility,
not uniqueness** — a system with more states can always break a finite closure
([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md)). Every "derived" below should be read as *a route
that closes*, never as the only possible route.

The priority runs **abstraction → physical** (Wheeler's *it from bit*): information *is* the
distinction, and matter/spacetime is what realizing distinctions *looks like*. "Information is
physical" (Landauer) is then the downstream **toll** — realizing a bit is finite and costs
`ΔF = −log 2` — not a reduction of information to matter.

<p align="center"><img src="diagrams/info_stack.svg" alt="The measure stack: a ½-spin atom at the base (1 bit = log 2, DERIVED), then Shannon count (INHERITED), phase (DERIVED), the quantum ledger (READING), and continuum renderings like Fisher geometry (RENDERING), with algorithmic/physical/semantic notions cross-cutting" width="720"></p>

**Quick map.** Every notion of information is one of four things on the substrate:

| Notion | Status | Core claim |
|---|---|---|
| Bit / ½-spin atom | **derived** | one bit = a two-valued ZFA closure |
| Shannon | **inherited** | the census *is* the count |
| Phase | **derived** | independent of the count |
| Algorithmic (AIT) | **stance** | `Ω` is the canonical uncomputable boundary the ontology excises (an analogy, §4 — not derived) |
| Physical / finite | **derived** | no continuum in a finite region; capacity is an **excursion budget**, and the proton's dissolution at `T_c` is the *observed* instance |
| Quantum | **reading** | `ℤ[i]` skeleton; a consistent count-measure (Born *rule* uniqueness open, §6) |
| Fisher | **rendering** | emerges in the continuum limit |
| Semantic | **contributes** | a contradiction carries zero |

**How to read this.** *Information theorists:* §2–§4 (Shannon, phase, AIT) — what QLF inherits and where it adds. *Physicists:* §5–§6 (Bekenstein/Landauer, quantum) + the frequency bridge in §1 — the energy/spacetime toll. *Mathematicians:* §1, §8 + [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) — the atom as the seed of the emergence ladder. Each section marks its status: **machine-checked**, **reading**, **rendering**, **forward work**, or **ontological stance** (collected in §10).

---

## 0a. Inventory: independent routes versus re-exports

The method's rule 4 says converging derivations are **multiplicity**, and multiplicity is what makes a
result dominant — but only *independent* routes count, so they have to be inventoried rather than
tallied. [`Entropy.md`](Entropy.md) §1b does this for `log 2` (17 appearances → **four** independent
routes plus thirteen re-exports). The same discipline applied to this document's own load-bearing
claims:

| Claim | Route | Independent? |
|---|---|---|
| one bit `= log 2` (the atom) | KL of a resolved binary distinction | **independent** — information-theoretic |
| one bit `= log 2` | `2ⁿ` one-pass closures counted ([`onePass_ways_iff`](lean/QLF_ClosureDepth.lean)) | **independent** — pure combinatorics, nothing assumed binary |
| one bit `= log 2` | von Neumann `S(I/2)` | **independent** — spectral |
| one bit `= log 2` | MRE saturation (the per-step ceiling) | **independent** — extremal |
| `ΔF = −log 2`, `Ω_Λ`, area law, Immirzi, mass gap, binding, Casimir… | the same atom re-exported into a physical setting | **re-export** — not further confirmations |
| Shannon additivity | census multiplicity multiplies | independent (but see §2 — it does *not* force `log`) |
| finite information | no injection of an infinite state space | independent — realizability |
| finite information | capacity is an excursion budget ([depth law](lean/QLF_ClosureDepthLaw.lean)) | **independent** — dynamical, and quantitative |
| finite information | the proton dissolves at `T_c ≈ 155 MeV` (quark–gluon plasma) | **observed** — not a derivation; an empirical instance of a capacity being exceeded (§5) |

Note the third status: an **observed** instance is neither a derivation nor a re-export — it is the
place where the picture can be checked against nature rather than against itself.

Reading the re-export column as evidence would be double-counting; the four independent routes to the
atom are the actual strength of the claim. Note which route pays the most rent: the **combinatorial**
one assumes nothing binary — it counts the histories that close in one pass, finds exactly `2ⁿ`, and
`log 2` per closure falls out of the count.

---

## 1. The atom of information — one bit is one half-spin closure

<p align="center"><img src="diagrams/half_spin_bit.svg" alt="A Hermitian pair t·t† folds to −I (360°), two pairs to +I (720°). A single-valued alphabet {+I} carries 0 bits (binary_kl 1 1 = 0); the two-valued spinor alphabet {+I,−I} carries 1 bit = log 2 (binary_kl 1 (1/2) = log 2), the MRE maximum" width="720"></p>

**Claim.** QLF's minimal unit of information is the two-valued **spin-½ closure** — the substrate's
*minimal rotationally covariant two-valued carrier*. A *single-valued* object cannot express a
distinction (carries zero information); a *two-valued* one — the spinor, whose `2π` turn reads
`−I ≠ +I` — carries exactly one bit. What is proven is that the implemented single-valued alphabet
carries `0` and the two-valued spinor alphabet carries `log 2`, and that the increment enters exactly
at the double-cover sign; **not** that spin-½ is the unique conceivable shape for a binary carrier
(that would need a completeness theorem over all constructions — see §0).

**Proof (machine-checked, [`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)).**
Write the binary Kullback–Leibler divergence of a recognition density `q` from a prior `p`,
`D(q‖p) = q·log(q/p) + (1−q)·log((1−q)/(1−p))` (`binary_kl`).

- **Single-valued alphabet `{+I}`** (a prior with one outcome, `p = 1`): resolving it costs
  `D(1‖1) = 1·log 1 + 0·log(0/0) = 0` nats (`single_valued_zero_information`). *A one-valued
  object marks no difference — the formal content of "it cannot express information."*
- **Two-valued alphabet `{+I, −I}`** (uniform prior `p = 1/2`, delta realization `q = 1`):
  `D(1‖½) = 1·log 2 = log 2` nats — exactly one bit (`two_valued_one_bit`).
- **The jump happens exactly at the `−I` sign.** `spin_half_is_information_atom`: `0 < log 2`,
  and the increment is admitted precisely when the double-cover sign `−I ≠ +I` enters.

**Why the *spinor*, not a vector — Cartan (1913).** The `−I` is the double-valued sign of the
`SU(2) → SO(3)` cover, `π₁(SO(3)) = ℤ₂`. It is reproven here from the explicit rotation matrices:
a full `2π` turn is `+I` on the vector (`SO(3)`) representation but `−I` on the spin-½ (`SU(2)`)
representation (`spinor_double_valued_vector_blind`, via `Complex.exp_pi_mul_I`). A vector factors
through `SO(3)` and is *blind* to the winding; the spinor records it. This is the substrate
instance of Cartan's classification of the non-tensorial (spinor) representations of the
orthogonal groups. See [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) § "Rung 5a".

**MRE saturation — the bit is the *maximum*, and it is unique.** On the uniform binary prior,
`D(q‖½) = log 2 − H(q)` with `H` the binary entropy (`binary_kl_uniform_eq_log_two_sub_entropy`),
and `H(q) > 0` for `q ∈ (0,1)` (`binary_entropy_pos`). Hence `D(q‖½) < log 2` for every spread-out
`q` (`binary_kl_uniform_lt_log_two`), with the bound `log 2` attained **only** at the delta
realization — the half-spin ZFA closure. So the spin-½ closure is the *unique* event shape that
both closes and extracts the maximum information per fold: **Maximum Relative Entropy**
([`MRE.md`](MRE.md) §2.1, [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)).

**The atom is also the elementary clock — information *is* the physics.** Space is the set of
positions of ZFA closures; time is the local clock frequency, `f = 1/latency`
([`Time.md`](Time.md), [`SpaceTime.md`](SpaceTime.md)). The *same* ½-spin closure that carries one
bit sets one tick — so **frequency is not an extra physical quantity; it is the rate at which
distinctions are realized**, and mass/energy are `m = ℏf/R`, `E = ℏω` per bit (§5). That is the
concrete content of "information *is* the physics," not a slogan: watch it run — every dot a
closure, colour its frequency — in the interactive constructor
([live](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html),
[`Spacetime_Constructor.md`](Spacetime_Constructor.md)). This discrete-frequency reading is where
QLF completes **Carver Mead's** *Collective Electrodynamics* — his relational, non-projectile
electromagnetism, minus its one residual *continuous*-frequency assumption
([`Collective_Electrodynamics.md`](Collective_Electrodynamics.md) §5).

---

## 2. Shannon information — count / multiplicity (inherited)

**Classical (Shannon 1948).** Information is the reduction of uncertainty over distinguishable
alternatives; entropy `H = −Σ pᵢ log pᵢ` measures multiplicity. Shannon *explicitly disclaims
meaning* (1948: semantics is "irrelevant to the engineering problem").

**QLF relation — pure inheritance.** The closure **census** *is* Shannon counting on the
substrate. Information composes additively because multiplicities multiply:

**Proof ([`lean/QLF_CensusShannon.lean`](lean/QLF_CensusShannon.lean)).** For independent
closures joined in parallel, `W(A ∥ B) = W(A)·W(B)` (`independent_join_multiplies`); a single bit
has multiplicity `2` (`bit_multiplicity`), `n` independent bits multiplicity `2ⁿ`
(`nbit_multiplicity`), so `information = log W` is additive (`multiplicity_composes`). The `log 2`
per closure and the Landauer bridge `ΔF = −log 2` are the per-event quantum
([`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)).

**Why a logarithm at all — because frequency *is* the number of ways.** The quantum happens **every
way that closes**; a closure's **frequency is its multiplicity** — the census count `W` of ways it can
occur — so probabilities are not primitive but way-counts, `pᵢ = Wᵢ/ΣW` (§6). Once information *is* the
count of ways, the shape of the measure is constrained rather than chosen: if A can happen `W_A` ways
and B `W_B` ways, together they happen `W_A·W_B` ways (`independent_join_multiplies`), so for the
information of "A and B" to be the *sum* of the parts the measure must turn multiplication into
addition — `S(A·B) = S(A) + S(B)` with `W(A·B) = W(A)·W(B)`. On the binary uniform census that gives
`S = log W`, Boltzmann's `S = log(number of ways)`, and for uniform ways (`p = 1/W`),
`−Σ pᵢ log pᵢ = log W` (Shannon **is** Boltzmann).

**Where that argument actually stops — a correction worth making precisely.** Additivity over
multiplication does **not** by itself force the logarithm. A function on the positive integers with
`f(mn) = f(m) + f(n)` is a *completely additive arithmetic function*, and such functions are **free on
the primes**: fixing `f(2) = log 2` pins every power of two and says nothing whatever about `f(3)`.
The prime-omega function `Ω(n)` (counting prime factors with multiplicity) is completely additive and
is not a logarithm. So "ways multiply, information adds" forces `S = log W` only on the multiplicative
sub-semigroup generated by the anchor.

That is exactly — and only — what the substrate proves, which is why the honest claim is *stronger*
where it matters and silent where it should be:

- **Proven.** On QLF's own census, which is binary and uniform (`W = 2ⁿ`,
  [`onePass_ways_iff`](lean/QLF_ClosureDepth.lean)), additivity plus the one-bit anchor `c = log 2`
  gives `H = n·log 2 = log W` (`additive_uniform_eq_length_mul`, `additive_unique`,
  [`lean/QLF_EntropyUniqueness.lean`](lean/QLF_EntropyUniqueness.lean)). **The logarithm is forced on
  the census QLF actually has.**
- **Open.** Arbitrary multiplicities and non-uniform distributions need a grouping/regularity axiom
  (Faddeev 1956; Baez–Fritz–Leinster; Knuth's "structure forces the measure"). Neither the theorem nor
  its necessity is established here — `QLF_CensusShannon` says as much.

### 2a. The free monoid on primes — the arithmetic-function argument is the census's own structure

The "completely additive functions are free on the primes" remark above is not an analogy the
substrate happens to resemble. It **is** the census. Every ZFA closure factors **uniquely** into an
ordered sequence of irreducible (prime) closures — the resummation identity `G(x) = 1/(1 − I(x))`,
machine-verified (`census_irreducible_resummation`, [`lean/QLF_AlphaBound.lean`](lean/QLF_AlphaBound.lean),
[`Alpha_Residual.md`](Alpha_Residual.md) §4). So the closures form a **free monoid on the prime
closures**, `Ω(h)` = the number of prime factors is the completely additive grading (the RG
"diagram order", [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md)), and the freedom is
**relation-free by theorem**, not by assumption.

Two information-physics consequences follow, both used elsewhere:

- **The perturbation series converges because the substrate is a prefix code.** The Kraft inequality
  `Σ 8^{−|h|} ≤ 1` (`twist_kraft`, [`lean/QLF_KraftMeasure.lean`](lean/QLF_KraftMeasure.lean)) makes the
  closure-order sum absolutely convergent in its cylinder measure — no Borel resummation, no Lipatov
  analysis. The Dyson divergence of continuum QED is the signature of a *coupling continuum* the
  substrate does not have; over a prefix-free code the sum is finite by counting
  ([`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) §3, [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean)).
- **Self-similarity is forced, and it concentrates the information.** A free monoid gives a geometric
  generating function, hence a *linear* coefficient recurrence, hence scale-invariant `~4ⁿ` growth —
  self-similarity as a theorem, the shadow of the free-monoid structure. And a linear recurrence has
  no period-doubling, so the discrete-scale-invariance / log-periodic channel is **closed by
  structure**. Since factorisation is unique, *every* closure is compositionally organised, so
  self-similar organisation carries the census's whole multiplicity mass — *self-similar things
  dominate existence*, the information-theoretic form of "the most ways happen first"
  ([`Philosophy.md`](Philosophy.md) §3a; [`Category_Theory_QLF.md`](Category_Theory_QLF.md) §3a;
  [`self_similar_closures.py`](self_similar_closures.py)). This is why the α-residual weight `w = 1/2`
  is *structural*, not a fit ([`Alpha_Residual.md`](Alpha_Residual.md) §9b).

---

## 3. Shannon is necessary but *not sufficient* — phase is independent information

**Claim.** The permutation-invariant *count* (Shannon) does not determine the physics; the
**order (phase)** it discards carries independent information.

**Proof ([`lean/QLF_PhaseInformation.lean`](lean/QLF_PhaseInformation.lean)).** Two histories with
the **identical twist multiset** — hence identical Shannon content — can fold to **opposite** Pauli
scalars: `^v<>` → `+I` (a boson / 720° closure, `fold_udlr`) versus `^<v>` → `−I` (the electron's
360° fermion sign, `fold_uldr`, reusing `QLF_Spin.fold_electron`). The count cannot tell them
apart; the phase can — and here the difference *is* spin statistics
(`count_does_not_determine_phase`, `shannon_necessary_not_sufficient`). The same non-count
structure carries time (`f = 1/t`) and mass (`m = ℏf/R`) as frequency
([`Shannon_And_Phase.md`](Shannon_And_Phase.md)). So Shannon is a floor, not the whole story: QLF's
state ring is the Gaussian integers `ℤ[i]`, whose phase `μ₄ = {±1, ±i}` is exactly the information
Shannon throws away ([`The_QLF_State_Space.md`](The_QLF_State_Space.md)).

---

## 4. Algorithmic information (Kolmogorov–Chaitin) — the fantasy boundary

**Classical (Kolmogorov 1965; Chaitin 1975).** The information in an object is the length of its
shortest program; a real is *lawful* iff it has a finite program.

**QLF relation — the sharpest statement of the boundary.** Algorithmic Information Theory makes
QLF's "fantasy tier" **quantitative**. The non-identifiable tail of the overfit theorems
([`Shannon_Overfit.md`](Shannon_Overfit.md), `tail_unconstrained`) is exactly the reals of
**infinite Kolmogorov complexity**; **Chaitin's `Ω`** (the halting probability) sits on the
boundary — *definable yet uncomputable*, the canonical fantasy object with a name. QLF's response
is not a dodge but the correct discipline: the core lives strictly within **`RCA₀`**, below the
Busy-Beaver / `Ω` horizon ([`ReverseMathematics.md`](ReverseMathematics.md)), and non-terminating
computations never achieve ZFA closure. **AIT prices descriptions; ZFA says which descriptions get
receipted.**

**Status — stance, not theorem (a correction).** `full_zeno_prune` is a *terminating* function on
finite `TopoString`s — Lean proves its termination by a decreasing-length measure — so it neither
solves nor instantiates the halting problem, and it is not a realization of `Ω`. Identifying the
pruning boundary with Chaitin's `Ω` is an **ontological stance**: `Ω` is the canonical *example* of
a definable-yet-uncomputable object that a receipt-based ontology excises, and the correspondence is
a reading of that discipline. What is proven is narrower and still substantive: the core sits in
`RCA₀`, and only terminating constructions produce closure receipts.

---

## 5. Physical and finite information (Bekenstein, Gisin, Landauer)

**Classical.** Landauer (1961): *information is physical* — erasing one bit dissipates `k_B T ln 2`.
Bekenstein (1981): a finite region holds *finite* information (bounded by area). Gisin
(2019): a single real number carries infinite information, so no physical quantity is a real.
Zeilinger–Brukner (2003): an elementary system carries *one bit*.

**QLF relation — derived, and it explains *why* finiteness bites.** The Bekenstein/Gisin bound
turns on information being **quantized**: a region holds finitely many distinctions *because each
distinction is a whole bit* — the atomic ½-spin closure of §1 — not an infinitely-divisible sliver.

**Proof ([`lean/QLF_Realizability.lean`](lean/QLF_Realizability.lean)).** With the Bekenstein bound
as premise (a region's distinguishable states form a *finite* type) and a faithful realization
modeled as an injection, there is **no injection from an infinite state space into a finite one**
(`no_continuum_in_finite_region`); hence a real-valued state space is consistent but physically
unrealizable (`real_continuum_not_realizable`, `continuum_consistent_but_unrealizable`). **Finite capacity has a second, sharper consequence: it can always be broken.** `no_continuum_in_finite_region`
says an infinite state space cannot be *injected* into a finite region. The **dynamical** companion says
what a finite capacity *misses*: for every capacity `R` there is a genuine closure it cannot see —
`[+^{R+1} −^{R+1}]`, which fails at `R` yet closes at `R+1`
([`law_of_exceptions`](lean/QLF_LawOfExceptions.lean)) — so no finite closure is final
(`closure_hierarchy_strict`). **A system with more states can always break a finite closure**; this is
the [Law of Exceptions](Law_Of_Exceptions.md) as information physics, and it is why every finite
description has a real exception.

With the depth law it is **exact**: a capacity-`R` horizon closes precisely the histories whose phase
walk never strays further than `R` from balance
([`closedAtHorizon_iff_maxExcursion_le`](lean/QLF_ClosureDepthLaw.lean)). So an information capacity is
an **excursion budget, not a length budget** — capacity `R` admits histories of length `~R²`, since a
balanced walk's mean maximum is `√(πn/2)`. Bekenstein bounds *how much*; the depth law says *which*:
distinguishability is bounded by how far from balance a history is allowed to stray.

**Inventory and capacity are two different quantities.** `log₂ W` is an **inventory** — the number of
bits needed to index `W` ways (`onePass_entropy`: the depth-1 stratum's `2ⁿ` ways are exactly `n` bits;
all balanced length-`2n` histories carry `log₂ C(2n,n) ≈ 2n` bits). `maxExcursion` is a **capacity** —
how far from balance the walk is allowed to stray, and by `closureDepth_eq_maxExcursion` exactly how many
passes closing costs. Conflating them is what produced the earlier `log₂ n` reading of the mean-depth
data; both quantities are real, and the relation between them is the interesting part:

```
inventory (bits) ∝ capacity²          measured  bits / R² = 1.45 → 1.37   for 2n = 16 … 2048
```

drifting toward the `4/π ≈ 1.273` implied by `log₂ C(2n,n) ~ 2n` together with the balanced walk's mean
maximum `E[max] ~ √(πn/2)` (same slow finite-size drift as `E[max]/√(πn/2) = 0.92 → 0.97`). So a
capacity-`R` closure holds `~R²` bits.

That is the **scaling shape of the Bekenstein area law** — `S ∝ R²` — arising here from pure counting,
with no geometry assumed. What is *not* claimed: that the excursion capacity `R` **is** a spatial radius.
That identification is the open bridge; only the scaling coincidence is exhibited (contrast the anchored
area law `S = 4πR² log 2`, [`QLF_GravityFromDelay`](lean/QLF_GravityFromDelay.lean), where `R` is a
radius by construction).

**Why a hadron is admissible here at all — the warrant.** Not by analogy, and the licensing chain should
be stated rather than assumed:

1. **ZFA closure *is* information** — a closure is a resolved distinction, one realized bit (§0, §1).
2. **Information is physical** — realizing a distinction is finite and costs `ΔF = −log 2`.
3. Therefore a physical bound state that *is* a ZFA closure is an information object **by identity**, and
   its capacity is an **information** capacity — so measuring the temperature at which it fails measures
   that capacity.

The proton qualifies on **proven** grounds at step 3: it is a closure of the substrate, with baryon number
a signed 3-axis winding invariant of its history, only the singlet closing, and its prime-3 period
irreducible. So its stability threshold is not *analogous to* an information bound — it **is** one. The
admission is exactly as strong as step 1, which this document marks as an ontological stance (§10), plus
step 3, which is machine-checked; it does not need step 2 to be more than the precise toll-claim used
throughout.

**The observed instance — the proton.** "Information is physical" here has a *measured* consequence, not
only a thermodynamic toll. The proton's stability is **derived** structurally in QLF three times over —
baryon number as a signed 3-axis winding invariant ([`baryonNumber`,
`baryon_dagger_odd`](lean/QLF_BaryonWinding.lean)), only the singlet closes
([`singlet_closure`](lean/QLF_Confinement.lean)), and the prime-3 irreducibility lock
([`prime_freq_irreducible`](lean/QLF_PrimeResonance.lean)) — and QLF predicts the absence of cold proton
decay ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) §5a), which stands. But a structural lock
is a **finite closure**, hence a finite capacity, hence it has a real exception
([`law_of_exceptions`](lean/QLF_LawOfExceptions.lean)) — and nature exhibits it: above
`T_c ≈ 155 MeV` (`≈ 1.8 × 10¹² K`) the proton is not a closure at all, the quark–gluon plasma observed at
RHIC and the LHC. **The proton does not decay; it dissolves.**

Read informationally: raising the temperature raises the **excursion capacity** available to the
constituent history past what the bound closure can absorb, so the receipt stops closing. Temperature
*is* the capacity knob — in the freeze-out model it literally is the pruning budget
([`census_congestion_freezeout.py`](census_congestion_freezeout.py)). So the finite-information claim of
this section is not only a bound one derives (`no_continuum_in_finite_region`) but a threshold one can
**measure**: every bound state has a finite information capacity, and the temperature at which it fails is
that capacity read off. Full treatment, including why this does not conflict with the no-proton-decay
prediction, in [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4a.

**Two capacity levels, and one unbounded case.** Read as information capacities, the physics stratifies by
*what kind of invariant* is being maintained — and the strength of the invariant's proof predicts whether a
capacity exists at all:

| Maintained by | Capacity | Fails at |
|---|---|---|
| a **composite binding** (the proton as a bound closure) | finite | `T_c ≈ 155 MeV` — dissolution, observed |
| a **winding** invariant (baryon number, [`baryonNumber`](lean/QLF_BaryonWinding.lean)) | finite | `T_EW ≈ 160 GeV` — sphalerons; QLF *proves* `B` cannot be a conserved signed count ([`wcount_zero_on_ZFA`](lean/QLF_BMinusL.lean)), so its conservation was capacity-relative from the start |
| an **annihilation-odd signed count** (electric charge, [`signed_count_conserved`](lean/QLF_BMinusL.lean)) | **none** — the proof quantifies over *all* histories, with no depth or excursion budget | never; exact at every scale |


<p align="center"><img src="diagrams/capacity_ladder.svg" alt="A log energy axis from 1 MeV to 10 TeV with three survival bars: the proton as a bound closure ends at T_c = 155 MeV (dissolves, quark-gluon plasma observed); baryon number as a winding invariant runs further and ends at T_EW = 160 GeV (violated by sphalerons, with a dashed exp(-E_sph/T) tail marking the exponentially rare exception below threshold); electric charge as an annihilation-odd signed count runs the full width and continues past the edge with no threshold at any scale" width="820"></p>

Each threshold sits at its sector's **carrier-mass scale** (`Λ_QCD ≈ 200 MeV` → `T_c ≈ 155 MeV`;
`v = 246 GeV` → `T_EW ≈ 160 GeV`; `m_γ = 0` → none), which is why the exceptionless rung is **light**:
mass *is* constructing delay *is* fold depth *is* capacity, so a massless carrier is a zero-capacity one
with no budget to exceed ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4b). In information terms the
photon carries no hidden depth — zero fold, zero entropy ([`Entropy.md`](Entropy.md) §2) — so there is
nothing about it that a rising capacity can exhaust. Which is *why* light terminates the other way: at a
**resonant atom**, by matching rather than exhaustion — and in QLF that termination is constitutive, since
a photon **is** the joint emitter–absorber closure and exists in the ledger only when that closure
completes ([`Photon_Energy_Bits.md`](Photon_Energy_Bits.md) §1). A zero-capacity carrier can only be ended
by a match, never by a budget; the resonance selection is itself a ways-count, so line spectra are
multiplicity spectra ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4c).

So "information is physical" acquires a graded, measurable form: an information capacity exists exactly
when the invariant maintaining a structure is capacity-relative, and the temperature at which it fails
reads that capacity off. Below a threshold the exception is not absent but *exponentially rare* — the
sphaleron rate `~exp(−E_sph/T)` is literally the exception's multiplicity relative to the
closure-preserving ways ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4b).

Capacity
bounds distinguishability (`capacity_bound`, [`lean/QLF_Identifiability.lean`](lean/QLF_Identifiability.lean));
the continuum of "consistent" parameters is unidentifiable
(`consistent_set_continuum`) — the non-identifiability of [`Shannon_Overfit.md`](Shannon_Overfit.md).
The claim is the careful one: **consistency ≠ realizability**, never "`ℝ` is inconsistent."

**Landauer — the dimensionless quantum, with the thermodynamic bridge named.**
`zfa_closure_minimizes_free_energy` proves an *information* identity,
`−D_KL(δ‖uniform₂) = −log 2`; it is not Landauer's thermodynamic erasure theorem. The claim is that
QLF's per-event quantum **is the `ln 2` factor** in `k_B T ln 2` — and that identification requires
the `k_B T` bridge (a temperature and a coupling to a bath), which the KL identity does not supply.
With that bridge, QLF's per-event `ΔF = −log 2` (`zfa_closure_minimizes_free_energy`) *is*
Landauer's `k_B T ln 2` — the cost of fixing one bit. The identification becomes dimensional once
the free-energy unit is fixed by the **local temperature of the observer's Markov blanket**: the
abstract `−log 2` (nats) is then the Landauer cost `k_B T ln 2` in those units — so QLF does not
have "only a dimensionless log," it has the log *plus* the local clock that scales it. And
**`ℏω = 1 bit at frequency ω`** is derived from the per-event `log 2` plus the per-event `ℏω`,
recovering **Margolus–Levitin** (`ℏ` per bit-flip) and Landauer (`k_B T ln 2` per erasure) as
consequences ([`Information_Energy_Equivalence.md`](Information_Energy_Equivalence.md)). This is the
toll side of "information is physical": realizing the abstraction is finite and costs energy/time —
the abstraction itself stays primary.

**Holographic corollary.** Because each closure on a boundary carries exactly one bit, the
Bekenstein/holographic **area bound is a bound on the number of ½-spin closures** the boundary can
host: QLF's horizon entropy `S = 4πR² log 2` is precisely one `log 2` per Planck-patch closure —
the same count as the Loop-Quantum-Gravity `j = ½` punctures ([`LQG_QLF.md`](LQG_QLF.md),
`QLF_LoopQuantumGravity`). Holography is then not a separate postulate but the statement that a
region's information *is* its inventory of realized ½-spin distinctions.

---

### 5a. Reversible transport — information can move without being forgotten

Landauer's `k_B T ln 2` is a price on **erasure**, and it is easy to read it as a price on
computing. QLF says otherwise, and the Fredkin machine ([`Fredkin_QLF.md`](Fredkin_QLF.md)) is
where the distinction becomes executable rather than rhetorical.

The substrate charges one quantum per closure, `ΔF = −log 2`
([`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)) — and a closure is **many-to-one**. That
is the whole of it. Two regimes follow:

| | map | information | receipt |
|---|---|---|---|
| **Reversible transport** | bijection — no two inputs merge | moved, not lost; every input recoverable | **0** |
| **Erasure** | `2^k` distinguishable states → 1 reset state | `k` distinctions destroyed | `k · log 2` |

A Fredkin gate is a permutation of its register — `fredkin_bijective`
([`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean)) — so nothing merges, nothing becomes
unrecoverable, and there is no many-to-one closure to receipt. **An instantaneous
zero-free-action closure is free.** Run a full adder built only from such gates: 19 gates, and
the ledger stays at zero the whole way. The bill arrives exactly where you decline to keep the
garbage — 29 lines, so 29 bits — and nowhere else.

So **Landauer and Bennett (1973) are recovered here, not assumed.** QLF has no separate postulate
that erasure costs; it has one quantum attached to closure, and the boundary between free and
charged is whether the closure is many-to-one. Conservative logic is simply the discipline of
staying on the free side of that line. The ledger is pinned: `garbageBill k = k · log 2` is a
function of the *retained-garbage count*, not the gate count (`garbageBill_eq_closures` — `k`
copies of the one `QLF_FreeEnergy` quantum, not a new postulate); `reversible_run_cost_zero`
(`garbageBill 0 = 0`, any depth); `fredkin_iterate_bijective` (an `n`-deep circuit is still a
bijection); `garbageBill_pos_iff` (`0 < garbageBill k ↔ 0 < k`). The strong reading — the
substrate has *no intrinsic erase*, so every `−log 2` is a reset a holder elects at a horizon —
is [`Reversibility.md`](Reversibility.md) §7a, where it lines up with the black-hole unitary
unwind and the [#148](https://github.com/rchain-community/quantum-logical-framework/issues/148)
closure horizon as one principle.

The `FANOUT` gate is the same principle read as information: `FREDKIN(x; 0, 1)` yields two copies
of `x`, and its third line carries `NOT x` away as garbage. **You get a usable copy only by
carrying the compensating distinction away with it** — no-free-duplication
([`Banach_Tarski_QLF.md`](Banach_Tarski_QLF.md) §4) as a line item. Copying is not free; it is
deferred, and the deferral is visible in the ledger.

The mathematical face of the same fact — the gate is an *automorphism of the admissible closure
space* — is [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) Rung 5b. Watch it run:
[`fredkin_machine.html`](fredkin_machine.html).

## 6. Quantum information — the load-bearing floor (a reading, not a rival)

**Classical.** Von Neumann entropy `S(ρ) = −Tr(ρ log ρ)`; qubits; the stabilizer/Clifford
formalism; resource theories (entanglement as an unspeakable currency).

**QLF relation — the substrate *is* the integer skeleton of quantum information.** The
stabilizer/Clifford fragment is *exactly integer arithmetic on the `ℤ[i]` lattice*
(`QLF_StateSpace`, [`The_QLF_State_Space.md`](The_QLF_State_Space.md)); resource theories are ledger
accounting. The Gottesman–Knill boundary (Clifford vs. the `T`-gate / `ζ₈`) is the boundary of the
**Gaussian-integer / stabilizer fragment** and the onset of **universal** quantum computation — *not*
a continuum boundary (a correction): `ζ₈ = e^{iπ/4}` is an **algebraic** number, and no single gate
introduces a continuum. The true statement is subtler and more useful: Clifford + `T` generates a
**dense** subgroup of `SU(2)`, so the continuum appears only as the **closure** of a discrete generated
group — never inside a finite circuit. That is the continuum-as-rendering thesis in its exact form.

Two pillars:

- **A consistent count-measure — and the bridge it still needs** ([`lean/QLF_BornProbability.lean`](lean/QLF_BornProbability.lean)).
  Three things must be kept apart:

  | Layer | Object | Status |
  |---|---|---|
  | ontology | the multiplicity `Wᵢ` — the count of ways | the substrate's own quantity |
  | reporting | `Wᵢ / Σⱼ Wⱼ` | normalization under incomplete information |
  | proven measure | `\|aᵢ\|² / Σⱼ \|aⱼ\|²` over `ℤ[i]`-norms | **machine-checked** Kolmogorov axioms |

  What is proven: the Gaussian-integer norm-square ratios are non-negative (`bornProb_nonneg`), sum to
  one (`bornProb_sum_eq_one`), and are finitely additive on disjoint events (`eventProb_disjoint_union`)
  — exact `ℚ` arithmetic, no primitive real ([`Born_Rule.md`](Born_Rule.md)). **The exponent half of the bridge is now closed**
  ([`QLF_BornCounting`](lean/QLF_BornCounting.lean)): a realized event is a *closed Hermitian pair*, so
  its way-count is the product of the two legs, and the bra leg being the dagger of the ket makes those
  factors `a` and `star a` (`pairCount_eq_leg_times_dagger`) — exactly the `ℤ[i]` norm
  (`pairCount_eq_norm`). Independently the **modulus cannot be a count at all**: `|1+i| = √2` is
  irrational (`modulus_not_a_count`) while the norm is `2`, so integrality alone forces the square. And
  since existence is all-or-nothing, a single realization gets `1` or `0` (`bornProb_eq_one_iff`,
  `bornProb_eq_zero_iff`) — **every intermediate value is a ratio of counts of binary events, never
  partial existence**. **Uniqueness of the form is also settled, in a stated sense:** `unique_pair_form` shows `a·ā` is the
  *only* form scaling linearly on the ket leg, conjugate-linearly on the bra leg, and normalized on the
  trivial closure — uniqueness **given the pair structure**, not Gleason's theorem, which assumes no form
  at all.
  **The census identification has now been *checked*, and it half-fails** — the informative outcome
  ([`born_generator_check.py`](born_generator_check.py)): exact agreement on the pair generator
  (`norm(1+i) = 2` = two ways; `2ⁿ` for `n` pairs), but *no* Gaussian amplitude exists for branch counts
  that are not sums of two squares (`3, 38, 70, 126 …`), and **no two Gaussian integers stand in norm
  ratio `3:1`** though such Born weights are routine. The forced repair is the multiplicity reading:
  a weight of `3` is **three degenerate unit-norm branches**, not one amplitude of norm `3` — weight is
  the *sum* of norms over degenerate components. **And that residue is now closed**
  ([`QLF_Degeneracy`](lean/QLF_Degeneracy.lean)): the decomposition is fixed by `μ₄` — every closed
  history folds to a Pauli scalar, so a branch is one unit-norm component per way and its amplitude is
  their sum, making every weight a norm automatically. The earlier failures were the wrong comparison:
  **counts are not weights**, `weight = |Σ phases|²`, and the difference *is* interference (orthogonal
  phases ⟹ weight = count, aligned ⟹ `n²`, opposed ⟹ `0`). The phase question is now partly settled as well: it *is* the
  `pauli_fold`, proven for the pair sector, and **balance forces a real phase** — `μ₂`, never `±i`
  ([`QLF_BalancedPhaseReal`](lean/QLF_BalancedPhaseReal.lean)) — so branch amplitudes over the balanced
  census are signed **integers**, not Gaussian integers. Still open: the census↔amplitude identification,
  known false in its naive form. This remains the Born **measure**, not a derivation of the Born
  **rule**.
- **The `ħ/2` uncertainty quantum** ([`lean/QLF_Uncertainty.lean`](lean/QLF_Uncertainty.lean)):
  mapping a continuum value onto its nearest integer twist-count leaves an irreducible half-bin
  spread `= 1/2` (`binning_halfwidth_tight`, `uncertainty_quantum_eq_half`); the conjugate-pair
  product bound rests on the non-commuting Fourier-dual axes (`QLF_Spin.su2_comm_xy`).

The maximally-mixed qubit `ρ = I/2` has von Neumann entropy `log 2` — the *same* one bit the
half-spin closure resolves.

---

## 7. Fisher information / information geometry — a rendering-layer object

**Classical (Fisher; Amari).** Fisher information measures the sensitivity of a distribution to
its parameters; information geometry makes the space of distributions a Riemannian manifold.

**QLF relation — rendering, not foundation.** Fisher structure is a *continuum* object; in QLF it
should **emerge from census statistics in the appropriate limit**, not be postulated — the same
"continuum as rendering" move as `π` from the closure census ([`Physical_Pi.md`](Physical_Pi.md))
and Hilbert space as the metric completion of the `ℤ[i]` lattice. The census walk's scaling limit
is Brownian motion whose generator is the Laplacian (`QLF_CensusBrownian`), the natural home of a
Fisher metric in the continuum limit. Named as forward work, not claimed as done
([`Related_Frameworks.md`](Related_Frameworks.md) Part II §3).

**A first result ([`fisher_from_census.py`](fisher_from_census.py), toward issue #142): the Fisher
metric is the *curvature of the census KL* QLF already has — not a postulate.** The Fisher–Rao metric
is *by definition* the Hessian of a KL divergence, and QLF's census relative entropy `binary_kl` is
machine-checked (`QLF_FreeEnergy`). Computing the Hessian gives, exactly,
`g(θ) = ∂²/∂θ'² D_KL(θ'‖θ)|_{θ'=θ} = 1/(θ(1−θ))` — the Fisher–Rao metric of the census's Bernoulli(θ)
step. At the **balanced / MRE prior `θ = ½`** (the critical-line prior): the *global* bound is
`D_KL(1‖½) = log 2` (the one bit, §1), and its *local curvature* is `g(½) = 4` — the Fisher metric at
the balanced point. The census **walk** accumulates it linearly: `N` steps carry Fisher information
`N·g(θ)` (exact binomial), and the Gaussian continuum limit preserves the leading metric.

**The dually-flat structure comes with the family, and that is the honest framing.** The census's
Bernoulli/multinomial family **is** an exponential family, so it **inherits** the standard dually-flat
geometry — a property of exponential families, not a fresh derivation, and not "Amari's information
geometry derived." The demo verifies the signature structure with the
census KL as the **canonical divergence**: the KL equals the **Bregman divergence** of the
negative-entropy potential `φ = −H` (dual coordinates `θ` natural ↔ `η` expectation, `g = ψ''(θ) =
1/φ''(η)`), and the **generalized Pythagorean theorem** holds — `D(P‖R) = D(P‖Q) + D(Q‖R)` when `Q` is
the information projection of `R` onto a linear family containing `P` (m-geodesic ⊥ e-geodesic). So the
whole of Amari's information geometry — metric, two flat connections, the Pythagorean theorem — is the
census's own, built on the KL the substrate already machine-checks. **Where #142 lands:** the
distributional wing's consistency direction is machine-checked ([`QLF_ShannonFromCounts`](lean/QLF_ShannonFromCounts.lean), §10);
the **continuum** (`n→∞`) rendering of the manifold — the α-connection family in the scaling limit —
is a rendering-layer statement about an exponential family (Amari 2016, Ch. 2–3), settled mathematics
that changes no count of ways ([`Philosophy.md`](Philosophy.md) §3a rule 4), so it is recorded here as
citation rather than pursued as a derivation target.

---

## 8. Semantic information — where QLF *contributes*

**Classical (Carnap–Bar-Hillel 1952; Floridi).** The semantic theory of information notoriously
**collapses on contradiction**: a contradiction is *maximally* informative (it excludes every
model). Floridi patched this by demanding *truthfulness*; no settled mathematics of *meaning*
exists.

**QLF relation — closure-as-receipt dissolves the paradox, as a theorem.**

**Proof ([`lean/QLF_ContradictionReceipt.lean`](lean/QLF_ContradictionReceipt.lean)).** A
contradiction is an *unbalanced ledger* (`count_pos ≠ count_neg`), which admits **no** ZFA closure,
hence carries **zero realized information** — it gets no receipt (`contradiction_no_receipt`, the
contrapositive of `zfa_implies_critical_line`). Realized information is receipt-counted, so a
contradiction carries *none*, not the maximum — the **Bar-Hillel–Carnap paradox dissolved**.

**The inversion of *ex falso*, in information terms.** Classical logic *fears* the one false
statement: by *ex falso quodlibet* it explodes, and "provable" is severed from "true" (Landauer's
bill would be infinite). QLF *requires* it. In the possibilist layer every distinction is affirmed —
the free monoid generates it all — and what turns a piece of that space into an **event** carrying
information is the introduction of **one negation** (a single `−`, "not this") that **closes**: finds
its affirmation and cancels to Zero Free Action. The false statement is the *selection act*, and it
cannot explode because it must close — bounded, local, RCA₀ — or `full_zeno_prune` annihilates it
before it is realized. So a contradiction carries zero information not by patch (Floridi's
truthfulness demand) but because a contradiction is *receiptless by construction*
([`Philosophy.md`](Philosophy.md) §3).

Meaning is then **position in the admissibility graph**: semantic content = what closes with what,
and **information synthesis is disjunctive (OR) closure** — a random possibility stream closing on
a `List.any verify` OR-fold (`disjunctive_closure`, `closure_always_fires`,
[`lean/QLF_InfoSynthesis.lean`](lean/QLF_InfoSynthesis.lean)); the closure-token basis
([`Closure_Token_Basis.md`](Closure_Token_Basis.md)) is a candidate mathematics of semantic
information.

---

## 9. The synthesis — one ontology, the whole stack on top

| Notion | Reference | QLF status | Proof | Anchor |
|---|---|---|---|---|
| The bit (it from bit) | Wheeler; Zeilinger–Brukner | **derived** — one bit = the two-valued ½-spin closure; single-valued = 0 | ✅ machine-checked | `QLF_SpinorInformation`, `QLF_FreeEnergy` |
| Shannon entropy (count) | Shannon 1948 | **inherited** — the census IS Shannon counting; `log` forced on the *binary uniform* census only | ✅ machine-checked (uniform wing); general uniqueness open, and its **necessity** unproven (§2) | `QLF_CensusShannon`, `QLF_EntropyUniqueness` |
| Phase (beyond count) | — | **derived** — count ≠ phase; order is independent information | ✅ machine-checked | `QLF_PhaseInformation` |
| Algorithmic (AIT) | Kolmogorov; Chaitin | **boundary** — `Ω` = the pruning boundary; RCA₀ floor | 🧱 principled boundary (Ω uncomputable) | `QLF_ShannonOverfit`, `full_zeno_prune` |
| Physical/finite | Landauer; Bekenstein; Gisin | **derived** — no continuum in a finite region; `ΔF = −log 2` | ✅ machine-checked | `QLF_Realizability`, `QLF_FreeEnergy` |
| Quantum (von Neumann) | von Neumann; Gottesman | **reading** — `ℤ[i]` skeleton; a consistent integer count-measure; `ħ/2` | ✅ measure machine-checked; Born-*rule* uniqueness + the multiplicity↔norm² bridge open (§6) | `QLF_BornProbability`, `QLF_Uncertainty` |
| Fisher / geometry | Fisher; Amari | **rendering** — the census carries the dually-flat geometry (KL = canonical divergence); metric = census-KL curvature | 🟡 metric + dually-flat structure shown ([`fisher_from_census.py`](fisher_from_census.py)); continuum `n→∞` manifold open (#142) | `QLF_CensusBrownian`, `QLF_FreeEnergy` |
| Semantic | Carnap–Bar-Hillel; Floridi | **contributes** — closure-as-receipt; contradiction carries 0 | ✅ machine-checked | `QLF_ContradictionReceipt`, `QLF_InfoSynthesis` |
| *information = realized distinction* | (the ontology) | the bottom layer itself | ⬛ ontological stance | — |

Every row sits on one sentence: **information = realized distinction = closure receipt**, with the
**½-spin closure as its atom**. Shannon counting, AIT bounds, Fisher geometry, and stabilizer
arithmetic are the measure stack over a now-specified ontology. QLF is the **foundation under the
stack, not a rival to it**. And the atom is not just the base of *this* stack — it is the **seed of
the entire emergence ladder**: the same two-valued closure whose fold-group is `μ₄ = (ℤ[i])ˣ`
generates ℕ (counting closures), the ring `+`/`×` (parallel/sequence), and su(2)/su(3), with the
continuum as their completion ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) § Rung 5a). So
because the same ZFA filter selects physical reality *and* realizable mathematics, "why is
mathematics so effective in physics?" dissolves: effective math = realizable math = the substrate
([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §4, Wigner).

**The empirical case that reality actually *is* "it from bit."** The claim is not only that
information *could* be fundamental — it is that the census yields parameter-free **relations, bounds
and structural numbers**, with residuals and open scales recorded rather than absorbed: the forced
`α⁻¹ > 137` bound, `Ω_Λ = log 2`, `a₀ = cH₀/2π`, Koide `Q = 2/3`, `π` and `ζ(3)` from the finite
census — each an *it* read from *bits*. What is **not** claimed is a parameter-free derivation of all
physical constants: `α` carries an undischarged `+0.036` residual, Koide takes an input mass scale, RG
running is open, and the absolute mass sector is incomplete. Their collective **overdetermination** is
the evidence for an informational substrate, laid out (with its misses at full weight) in
[`Completeness_Evidence.md`](Completeness_Evidence.md) §3.

And it is not only numbers: **the physics that emerges** is *it from bit* too. Spacetime is
synthesized event-by-event from ZFA closures (`ZFAEventDynamics`, the state *is* Minkowski space,
`QLF_Minkowski`); the four forces are relative projections of one gauge-twist closure
([`UniversalRelativity.md`](UniversalRelativity.md) §4a); **mass is constructing delay** (`m = 1/R`);
gravity is the geometry of the closure aggregate (Einstein's equations as the substrate's equation
of state); measurement is a closure, entanglement a shared closure (`ER_EPR_QLF`). Each is an *it*
— a particle, a field, a spacetime interval — realized from *bits* (ZFA closures). So the finding of
§1 (the bit is a proven ½-spin closure), the emergent physics (spacetime, forces, mass, gravity from
closures), and the evidence (the constants come from the bit census) reinforce one another: a proven
atom, a world built from it, and a ledger of parameter-free consequences — Wheeler's *it from bit*,
made constructive end-to-end.

---

## 10. Honest scope

- The **atom** (`single_valued_zero_information`, `two_valued_one_bit`, `spin_half_is_information_atom`,
  `spinor_double_valued_vector_blind`), **Shannon additivity + the uniform-census uniqueness**,
  **phase-not-count**,
  **no-continuum-in-finite-region**, **Born-from-counts**, **`ħ/2`**, and **contradiction-carries-zero**
  are all machine-checked in Lean 4 with zero `sorry`. Cartan's *general* classification of
  orthogonal-group representations is cited settled math, not reproven.
- The **information = realized distinction** identification is an **ontological stance** (the
  abstraction-primary reading), not a theorem — and it should not be dressed as one; what is proven
  is the *quantitative* content on the realization side. See
  [`Related_Frameworks.md`](Related_Frameworks.md) Part II and this repo's discussion of the
  distinction.
- **Fisher-from-census:** the metric is computed and the dually-flat structure verified numerically
  ([`fisher_from_census.py`](fisher_from_census.py)) — but the census family is an exponential family,
  so that structure is **inherited**, not newly derived; the continuum `n→∞` *manifold* is forward
  work (#142).
- **Entropy uniqueness — necessity is *not* settled** (corrected §2). "Ways multiply, information
  adds" does not force the logarithm: completely additive arithmetic functions are free on the primes
  (`Ω(n)` is additive and is not a log). What is proven is the uniform binary case — `W = 2ⁿ` with the
  one-bit anchor gives `H = log W` (`QLF_EntropyUniqueness`) — i.e. **the logarithm is forced on the
  census QLF has**. The general (non-uniform, arbitrary-multiplicity) theorem needs a
  grouping/regularity axiom and is open — in its **necessity** direction. Its **consistency**
  direction is now machine-checked ([`QLF_ShannonFromCounts`](lean/QLF_ShannonFromCounts.lean),
  #142): given `log ways`, the non-uniform partition carries the Shannon form as the identity
  `log W = Σ pᵢ log Wᵢ + (−Σ pᵢ log pᵢ)` (`log_total_eq_expected_log_add_shannon`), reduces to
  `log n` on the uniform census, and adds on independent joins (`shannon_indep_join`) — the grouping
  rule holds with no further axiom. What remains open is only that grouping + regularity *forces*
  `log`.
- **Born:** the `ℤ[i]`-norm ratios form a consistent finite probability measure, and the **exponent** is
  now explained rather than posited — the square is the ket–bra pair, and integrality rules the modulus
  out independently (`QLF_BornCounting`). The **degeneracy decomposition** is fixed by `μ₄`
  (one unit component per way), and **balance narrows that to `μ₂`** — proven — so amplitudes over
  closures are signed integers. **Still open:** the identification of physical multiplicity with the norm
  census, which the generator check showed is **false naively** (counts are not weights) and which is now
  a question about the signed sum over ways; and uniqueness of the `|a|²` form against Gleason-type
  derivations, untouched. Still the Born *measure*, not the Born *rule*.
- **Chaitin's `Ω`:** identifying the pruning boundary with `Ω` is an **ontological stance**, not a
  theorem — `full_zeno_prune` terminates on finite strings by a decreasing-length measure and decides
  no halting question (§4).
- **Clifford ↔ `T`** is the stabilizer-fragment / universality boundary, **not** a continuum boundary:
  `ζ₈` is algebraic; the continuum enters only as the *closure* of the dense group Clifford + `T`
  generates (§6).
- **The atom** is QLF's *minimal rotationally covariant two-valued carrier*; that no other conceivable
  binary carrier could serve would need a completeness theorem (§0, §1).
- "Information is physical" is used in the precise sense: the *toll of realizing* a distinction
  (`ΔF = −log 2`, finite realizability), never a reduction of the abstraction to matter.
- **The proton's admission** (§5) inherits the strength of the *identification* "ZFA closure = realized
  distinction" — an ontological stance, per the item above — together with the machine-checked fact that
  the proton **is** a substrate closure (baryon winding, singlet-only closure, prime-3 irreducibility).
  Given the stance, the dissolution temperature *is* an information-capacity measurement; without it, it
  is a structural analogy. That is the honest dependency, and it is the same stance the whole document
  rests on rather than an extra assumption smuggled in for the proton.

**What would falsify the picture.** A physical **information capacity below the one-bit scale** — a
sub-`log 2` distinguishable degree of freedom that is *not* a whole ½-spin closure — would break the
atomicity thesis; equally, a genuine physical **distinction that is not a closure** (an outcome
realized with no ZFA-balanced receipt) would break "information = realized distinction." Neither is
observed; both are sharp, standing targets.

---

## References

**The bit / it from bit.**
- J. A. Wheeler, *Information, physics, quantum: the search for links*, Proc. 3rd Int. Symp. Found. Quantum Mech. (1989) — "it from bit."
- Č. Brukner & A. Zeilinger, *Information and the structure of quantum theory*, in *Time, Quantum and Information* (2003) — an elementary system carries one bit.
- É. Cartan, *Les groupes projectifs qui ne laissent invariante aucune multiplicité plane*, Bull. Soc. Math. France **41** (1913) 53–96 — the spinor (non-tensorial) representations.

**Classical information / entropy.**
- C. E. Shannon, *A Mathematical Theory of Communication*, Bell Syst. Tech. J. **27** (1948) 379–423, 623–656.
- L. Boltzmann (1877); J. W. Gibbs, *Elementary Principles in Statistical Mechanics* (1902); E. T. Jaynes, *Information Theory and Statistical Mechanics*, Phys. Rev. **106** (1957) 620 — entropy as multiplicity / MaxEnt.
- J. C. Baez, T. Fritz & T. Leinster, *A characterization of entropy in terms of information loss*, Entropy **13** (2011) 1945 — categorical uniqueness of Shannon entropy.
- K. H. Knuth, *Lattices and information* — deriving measures from order structure.

**Algorithmic information.**
- A. N. Kolmogorov, *Three approaches to the quantitative definition of information*, Probl. Inf. Transm. **1** (1965) 1–7.
- G. J. Chaitin, *A theory of program size formally identical to information theory*, J. ACM **22** (1975) 329 — and `Ω`, the halting probability.

**Physical / finite information.**
- R. Landauer, *Irreversibility and heat generation in the computing process*, IBM J. Res. Dev. **5** (1961) 183 — information is physical; `k_B T ln 2` per erasure.
- N. Margolus & L. B. Levitin, *The maximum speed of dynamical evolution*, Physica D **120** (1998) 188 — `ℏ` per operation.
- J. D. Bekenstein, *Universal upper bound on the entropy-to-energy ratio*, Phys. Rev. D **23** (1981) 287.
- N. Gisin, *Indeterminism in physics… are real numbers really real?*, Erkenntnis (2019/2021) — reals carry unphysical infinite information.

**Quantum information.**
- J. von Neumann, *Mathematische Grundlagen der Quantenmechanik* (1932) — the density operator and its entropy.
- D. Gottesman, *The Heisenberg representation of quantum computers* (1998); Gottesman–Knill — the stabilizer/Clifford fragment.

**Information geometry.**
- R. A. Fisher (1925); S. Amari, *Information Geometry and Its Applications*, Springer (2016).

**Semantic information.**
- R. Carnap & Y. Bar-Hillel, *An Outline of a Theory of Semantic Information*, MIT RLE Tech. Rep. 247 (1952) — the contradiction-carries-maximal-information paradox.
- L. Floridi, *Outline of a theory of strongly semantic information*, Minds & Machines **14** (2004) 197 — the truthfulness patch.

**Active inference (the per-event `log 2`).**
- K. Friston, *The free-energy principle: a unified brain theory?*, Nat. Rev. Neurosci. **11** (2010) 127.

## See also

- [`Related_Frameworks.md`](Related_Frameworks.md) Part II — the measure stack; ZFA as its missing bottom layer.
- [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) — the emergence ladder; § Rung 5a (spin-½ = the atom of information); § 4 (Wigner dissolved).
- [`MRE.md`](MRE.md) · [`Shannon_And_Phase.md`](Shannon_And_Phase.md) · [`Shannon_Overfit.md`](Shannon_Overfit.md) · [`Information_Energy_Equivalence.md`](Information_Energy_Equivalence.md) · [`Relative_Entropy.md`](Relative_Entropy.md) · [`Entropy.md`](Entropy.md) · [`Born_Rule.md`](Born_Rule.md).
- [`TheContinuum.md`](TheContinuum.md) — why a finite universe cannot hold continuum information.
- [`Philosophy.md`](Philosophy.md) §6 — the information-ecology ontology; information = realized distinction, the abstraction primary.
- [`Information_Energy_Equivalence.md`](Information_Energy_Equivalence.md) — `ℏω = 1 bit`; the energy toll of realizing a distinction.
- [`AI.md`](AI.md) — the information-processing / dialectical-synthesis reading of the substrate that this doc grounds.
- [`Completeness_Evidence.md`](Completeness_Evidence.md) §3 — the empirical evidence for *it from bit*: parameter-free overdetermination (the *its* come from the *bits*).
- [`UniversalRelativity.md`](UniversalRelativity.md) — the physics that emerges from the same closures: spacetime, the four forces, mass, and gravity as *its* from *bits*.
- [`Fredkin_QLF.md`](Fredkin_QLF.md) — §5a worked out: a reversible computer runs at **zero receipt** because a bijection forgets nothing, and only the many-to-one reset of garbage is charged. Landauer and Bennett recovered from the one closure quantum. Watch it: [`fredkin_machine.html`](fredkin_machine.html).
