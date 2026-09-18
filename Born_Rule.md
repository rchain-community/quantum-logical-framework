# The Born Rule, Derived from ZFA

**Standard QM postulates the Born rule** — the probability of observing outcome $\varphi$ given state $\psi$ is $|\langle \varphi | \psi \rangle|^2$. This single postulate, added on top of unitary evolution, is the **measurement axiom** that connects the deterministic Schrödinger equation to probabilistic experimental outcomes. In standard QM no derivation from more fundamental principles is generally accepted; the rule is empirical input.

**QLF derives the Born rule** as a consequence of (a) the uniform-prior structure of the possibility tree, (b) the binary-partition information-gain bound of [MRE.md](MRE.md), (c) the multiplicity principle of [BayesianMechanics.md](BayesianMechanics.md), and (d) the local-ZFA-closure framing of [Measurement_Problem.md](Measurement_Problem.md). The Born rule is not a postulate — it is what the QLF algebra produces when an observer asks "what is the probability that the next ZFA closure yields branch $\varphi$ given the current state $\psi$?"

## 1. The possibility tree and uniform prior

A QLF observer at a given moment has access to a **possibility tree** $\mathcal{T}_\psi$: the set of admissible ZFA-closed histories reachable from the current state $\psi$, filtered by the local Markov blanket's causal frontier ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md), [Hierarchical_Control.md](Hierarchical_Control.md)). Each leaf of $\mathcal{T}_\psi$ is a specific admissible closure satisfying both halves of ZFA (count balance + Pauli closure, per [Experimental_Consistency.md §2.1](Experimental_Consistency.md)).

The **uniform prior** on $\mathcal{T}_\psi$ is the assertion that every admissible leaf is equally probable absent further information. This is the [BayesianMechanics.md](BayesianMechanics.md) "multiplicity principle" — *the thing that can happen in the most ways happens first* — read at the leaf level: each leaf corresponds to one micro-path; equally-counted paths get equal weight.

## 2. From paths to amplitudes

Standard QM associates each branch with a complex amplitude $\langle \varphi | \psi \rangle$. In QLF the amplitude is the **path-integral sum** over all admissible micro-histories that take state $\psi$ to outcome $\varphi$, weighted by the QuCalc phase ([path_integral.py](path_integral.py), [Maxwell.md](Maxwell.md) on the $E = h \cdot \text{bits}$ rule):

$$\langle \varphi | \psi \rangle = \sum_{h \in \mathcal{T}_{\psi \to \varphi}} e^{i \theta(h)}$$

where $\theta(h)$ is the cumulative phase of history $h$ (the QuCalc realization of the Feynman path-integral phase). The sum is over all admissible Pauli-closed paths from $\psi$ to $\varphi$.

This is not new physics — it is the same Feynman path-integral construction, with the path space restricted to admissible ZFA-closed histories. The QLF contribution is making the path space **discrete and combinatorially finite at each causal horizon** (per the BFS saturation noted in [MRE.md §2.2](MRE.md)).

## 3. Born rule as binary-partition optimum

The probability of outcome $\varphi$ given state $\psi$ is the **fraction of the possibility tree that ends at $\varphi$**, weighted by the constructive/destructive interference of contributing paths:

$$P(\varphi | \psi) = \frac{|\sum_{h \in \mathcal{T}_{\psi \to \varphi}} e^{i \theta(h)}|^2}{\sum_{\varphi'} |\sum_{h' \in \mathcal{T}_{\psi \to \varphi'}} e^{i \theta(h')}|^2} = \frac{|\langle \varphi | \psi \rangle|^2}{\sum_{\varphi'} |\langle \varphi' | \psi \rangle|^2}$$

The squared modulus appears because **each path contributes an amplitude with a phase; constructive paths add coherently, destructive paths cancel**, and the resulting count of effective paths is $|A|^2$ when $A$ is the complex sum. The denominator is the normalization across all admissible final states (the **partition function** of the possibility tree).

In the canonical orthonormal case $\sum_{\varphi'} |\langle \varphi' | \psi \rangle|^2 = 1$, this reduces to the standard Born rule

$$P(\varphi | \psi) = |\langle \varphi | \psi \rangle|^2.$$

## 4. Why the squared modulus, not the modulus

A naive reader might ask: why $|A|^2$ rather than $|A|$? **Two of the answers are now machine-verified**
([`lean/QLF_BornCounting.lean`](lean/QLF_BornCounting.lean)), and they are independent of each other:

**(a) The square is the Hermitian pair.** A realized event is not one leg but a *closed pair* — ket and
bra — both required and independently chosen, so the event's way-count is the **product** of the legs'
counts; and since the bra leg is the dagger of the ket, the two factors are $a$ and $\bar a$. Verified as
`pairCount_eq_leg_times_dagger`: $\text{pairCount}(a) = a \cdot a^{\star}$, which is exactly the
$\mathbb{Z}[i]$ norm `bornProb` already uses (`pairCount_eq_norm`). The exponent is not postulated — it
counts the two legs.

**(b) The modulus could not have served, on integrality alone.** A way-count is a cardinality, and
$|a| = \sqrt{re^2+im^2}$ is generally not one: for $a = 1+i$ the modulus is $\sqrt2$, irrational
(`modulus_not_a_count`), while $\text{pairCount}(1+i) = 2$ is a count. Inside a $\mathbb{Z}[i]$
amplitude ontology the norm is the **only** integer invariant available — so the square is forced before
any appeal to (a).

**What individual realizations look like.** Existence is all-or-nothing: a way either closes or it does
not, and `pairCount` is a whole number of ways (`pairCount_is_a_whole_count`). So for a single
realization the rule is trivial — probability $1$ when the branch takes every way
(`bornProb_eq_one_iff`), $0$ when it takes none (`bornProb_eq_zero_iff`). **Every intermediate value is a
ratio of counts of binary events, never partial existence.**

The two older prose arguments, retained as readings rather than proofs:

**Information-theoretic** (from MRE.md). Each ZFA closure is a binary partition of the local possibility tree, with information gain $\leq \log 2$ saturated at the 50/50 split (the per-event maximum of MRE.md §2.1). The probability assignment that saturates this bound at the leaf level is the one for which $-\sum P(\varphi) \log P(\varphi)$ is maximized subject to the path-integral amplitude constraint $\sum P(\varphi) = 1$ and $P(\varphi) \propto |\langle \varphi | \psi \rangle|^2$. The $|A|^2$ form is the unique probability assignment that:
- Reduces to the path-count when phases align (no interference)
- Maximizes the per-event information gain at each closure
- Preserves the unitary norm of the underlying state vector across all measurement contexts

**Algebraic** (from the Pauli structure). The Pauli matrices satisfy $\sigma_i^2 = I$ and $\{\sigma_i, \sigma_j\} = 2\delta_{ij} I$. The squared modulus $|A|^2 = A^* A$ recovers the standard probability structure ($P \geq 0$, $\sum P = 1$) when the underlying amplitudes are complex. Anything else (e.g. $|A|^p$ for $p \neq 2$) breaks the Hermitian-conjugate symmetry that QLF inherits from [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md)'s $E + E^\dagger \equiv \text{ZFA}$.

## 5. Why probability appears at all (the role of the Markov blanket)

In a fully ZFA-closed universe with no observer there is **no probability** — every history is determined. Probability is an **observer-relative** notion that arises because each Markov blanket sees only its own slice of the universal possibility tree ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md), Rovelli's Relational Quantum Mechanics applied at the QLF substrate).

The observer's local possibility tree is the **conditional** possibility tree: those leaves consistent with the observer's history. The uniform prior on this conditional tree is the source of the probability distribution. When the observer measures, they pick one leaf; the post-measurement state is the realized branch.

This is exactly the [Measurement_Problem.md §4a](Measurement_Problem.md) framing: each measurement = one ZFA closure = $\log 2$ nats of information gain per atom, with the specific branch picked according to the Born rule. The "wavefunction collapse" is the observer's possibility tree shrinking by half (per bit).

## 6. The Gleason-theorem connection

Gleason's theorem (1957) shows that for Hilbert spaces of dimension $\geq 3$, the **only** probability measure on the lattice of projection operators that satisfies countable additivity is the Born rule $P(\varphi) = \text{Tr}(\rho \, \Pi_\varphi)$. This is often cited as a derivation of the Born rule from first principles in standard QM.

The QLF construction in §3–4 is consistent with Gleason but goes further: it identifies **what is being assigned probability** (admissible ZFA-closed leaves of the local possibility tree) and **why** (the uniform prior over admissible micro-paths follows from the multiplicity principle and the algebra's Hermitian symmetry). Gleason fixes the form $|\langle \varphi | \psi \rangle|^2$; QLF fixes the underlying ensemble.

## 7. Worked example: spin-1/2 measurement

State $\psi = |z+\rangle$ (spin up along z-axis). Possibility tree for an x-axis measurement: two leaves, $|x+\rangle$ and $|x-\rangle$.

Amplitudes (path-integral sums):
- $\langle x+ | z+ \rangle = 1/\sqrt 2$
- $\langle x- | z+ \rangle = 1/\sqrt 2$

Squared moduli (Born):
- $P(x+) = 1/2$
- $P(x-) = 1/2$

QLF reading: the QuCalc engine starting from a `|z+⟩`-encoded history has two admissible Pauli-closed paths to `|x+⟩` and two to `|x-⟩`, evenly weighted under the uniform prior. The 50/50 outcome is the binary-partition optimum of [MRE.md §2.1](MRE.md), realized at the spin-1/2 atom level. Per-event information gain = $\log 2$ nats, exactly as expected.

For a measurement at angle $\theta$ from the z-axis:
- $\langle \theta+ | z+ \rangle = \cos(\theta/2)$
- $P(\theta+) = \cos^2(\theta/2)$

QLF reading: the path-integral sum gives $\cos(\theta/2)$ as the constructively-interfering contribution; the squared modulus gives the Born probability. The angular dependence is encoded in the Pauli algebra's structure constants, not added as a separate rule.

## 8. Open work

- **Lean theorem — partly delivered.** [`QLF_BornCounting`](lean/QLF_BornCounting.lean) closes the
  *exponent* half (`pairCount_eq_leg_times_dagger`, `modulus_not_a_count`, `born_is_pair_count_ratio`)
  and reduces the rest. **The generator check has now been run**
  ([`born_generator_check.py`](born_generator_check.py)) and its result is mixed and informative: it
  **agrees exactly on the pair generator** (`norm(1+i) = 2` = the two ways a pair closes; `norm((1+i)ⁿ)
  = 2ⁿ` = the `2ⁿ` ways `n` pairs close), and **fails for arbitrary census partitions**, since a
  `ℤ[i]` norm is always a sum of two squares (Fermat) while depth strata such as `38, 14, 70` and
  sign-splits such as `3, 35, 126` are not. Sharpest consequence: **no two Gaussian integers stand in
  norm ratio `3:1`** — `v₃(k)` and `v₃(3k)` differ by one, so exactly one has odd `3`-adic valuation —
  yet `3:1` Born weights are routine (Clebsch–Gordan `3/4` vs `1/4`).
  **The repair is forced, and it is the multiplicity reading itself:** a weight of `3` is *three
  degenerate unit-norm branches*, never one amplitude of norm `3`. Weight is the **sum** of norms over
  degenerate components. **And that question is now answered** ([`QLF_Degeneracy`](lean/QLF_Degeneracy.lean)): the
  decomposition is fixed by `μ₄`. Every closed history folds to a Pauli scalar in `{±1, ±i}`
  (`QLF_Pauli`), so each way carries a *unit* amplitude with a `μ₄` phase and a branch amplitude is
  their **sum** — whence `weight_is_always_a_norm`, and the obstruction disappears because **counts are
  not weights**. `weight = |Σ phases|²`, and the gap from the count *is* interference: orthogonal
  phases give weight = count (exactly why the pair generator matched — its two ways are the orderings
  `+−` and `−+`), aligned phases give `n²`, opposed give `0`. **And the phase question is now partly settled too**
  ([`QLF_PhaseAssignment`](lean/QLF_PhaseAssignment.lean),
  [`QLF_BalancedPhaseReal`](lean/QLF_BalancedPhaseReal.lean)): the phase *is* the history's `pauli_fold`,
  proven for the pair sector — both orderings fold to `−I`, so those ways are **aligned** — and balance is
  proven to force a **real** phase, `μ₂` rather than `μ₄`, so branch amplitudes over the balanced census
  are signed **integers**. The general rule `(−1)^{#neg}·sign(axis permutation)` is verified but not
  proven. Two corrections were recorded in the process: the census pair's ways are *not* orthogonal, and
  alignment is a **sector** property rather than a census one (both phases occur, so a census-spanning
  branch has the *signed* sum as its amplitude). **The general rule is now proven too**
  ([`QLF_PhaseRule`](lean/QLF_PhaseRule.lean)): `φ(h) = (−1)^{#neg + inv(axis word)}` for every balanced
  history at every length (`phase_rule`), and in a stronger form needing no balance hypothesis
  (`twist_fold_phase_normal_form`). So the phase a way carries is a **computable integer read off the
  word** — no matrix product per history — which is exactly the input this section said was missing.
  **What remains open** is the census↔amplitude identification itself — known **false** in the naive
  form (counts are not weights), and now with a *measured* obstruction as well; see the next item.
- **Numerical demo — run, and it does not yet reproduce QM.** [`contextual_census.py`](contextual_census.py)
  does what this item asked: exact signed amplitudes `A = N₊ − N₋` from the proven phase rule (never a
  matrix), preparation as an *open* strand, apparatus specified independently, membership by joint
  closure, over increasing horizons. Two results, and the first is a caution rather than a success:
  * **Transverse geometries give exactly `½` at every horizon — but that is *forced*, not evidence.**
    [`QLF_BasisIndependence`](lean/QLF_BasisIndependence.lean) proves relabeling the axes preserves every
    balanced history's phase, so when the two branches are exchanged by a relabeling fixing the
    preparation, `A₊ = A₋` identically. A number a proven symmetry forces is bookkeeping
    ([`Philosophy.md`](Philosophy.md) §3a rule 4). **Any future Born test must check for this before
    counting an agreement.**
  * **Aligned geometries wash out.** For a fixed preparation the branch ratio climbs monotonically
    toward `1` (`0, .125, .200, … .546` at `k=18`, `.677` at `k=28`), so the weight decays toward `½`;
    letting preparation depth grow with the horizon drives it to `1` instead. Both limits are
    degenerate, so **this partition does not define a horizon-independent probability** — the number is
    set by the depth-to-horizon ratio. Not a proven limit (monotone data is not a theorem), and not a
    refutation of the closure→amplitude idea; it does say a further principle must fix the regime.
  * **Two candidate explanations have been tested and eliminated.** It is *not* an artifact of
    flattening system and apparatus into one Pauli algebra: recomputing with them as independent
    indexed factors ([`QLF_IndexedFactors`](lean/QLF_IndexedFactors.lean)) gives **identical**
    probabilities at every horizon, because a strand's axis parity is determined by its imbalance, so
    the difference is a constant sign per branch and cannot survive `|A|²`. And it is not the phase
    model, which is proven.
  * **Capacity was the live candidate; it has been run, and it does not rescue the partition.**
    Closure is horizon-relative (`closedAtHorizon_iff_maxExcursion_le`), so the weight was read at a
    finite listening capacity `R` — keeping only runs whose free action never exceeds `R` at any
    prefix (`contextual_census.py --listening 2,3,4`, exact integers). **Capacity sets the rate of
    forgetting, never the limit.** The aligned weight still decays to exactly `½` at every capacity,
    with `|P(+) − ½|` falling by `0.666, 0.868, 0.906` per twist at `R = 2, 3, 4`, so a preparation
    stays readable for `τ = 2.5, 7.1, 10.1` twists. And what a long run *does* keep of the
    preparation is **not its direction**: against an asymmetric branch pair — one no relabeling can
    exchange, so nothing is symmetry-forced — the limit depends only on the preparation's axis class,
    and a preparation and its reversal land on the same limit exactly (`/` with `\`, `/>` with `/<`,
    `/^` with `/v`). Direction is precisely what a Born weight must depend on. The mechanism is
    spectral: at fixed capacity the walk is a finite signed transfer operator whose leading eigenvalue
    is a degenerate `±iλ(R)` pair (`λ = 3.991, 4.383, 4.638`, 16-fold top modulus), so every
    preparation collapses onto one dominant subspace and the direction-carrying part decays no slower
    than the spectral gap `λ₂/λ₁ = 0.752, 0.951, 0.979`. **This closes the whole family of long-horizon
    readings**, not just this one: a larger listening horizon remembers longer and forgets just as
    completely. Whatever carries a Born weight is in the **transient** — horizons comparable to the
    preparation itself — which is the regime the depth scan already showed to be depth-to-horizon
    dependent. Physically the substrate is saying something reasonable (free evolution inside a
    bounded capacity thermalises, and a measurement is a *prompt* joint closure, not an infinite free
    run; the coherence numbers are collected in [`Decoherence.md`](Decoherence.md) §4a), but it is not
    yet a Born rule.
  * **First joint closure — the absorbing census — restores direction, and localizes the failure to
    one question.** A closure *is* an event, so continuing a run past it describes a different,
    longer history; the scans above let a run that closed at depth 4 keep contributing at depth 700,
    and that continuation is exactly what mixes direction away. The absorbing census
    (`--first-closure`) stops each run at its **first** joint closure, whichever branch closes it —
    the run chooses its own stopping depth, so no horizon is chosen by us — and it is cross-checked
    against enumeration. Three results:
    - **Direction reaches the outcome again.** Reversing the preparation changes the weights:
      `P(+) = 0.688` vs `0.312` on the ZX-mix at `R = 3`, and `1.000` vs `0.878` for a branch pair no
      relabeling can exchange. Under *every* long-horizon reading a preparation and its reversal
      shared one limit exactly. The aligned geometry closes at depth `0` with `P(+) = 1` exactly, at
      every capacity, and nothing else ever closes — the deterministic case comes out deterministic.
    - **The complementarity is symmetry-forced, so it is bookkeeping — not evidence.** Where the
      branches are exchanged by a relabeling that also reverses the preparation,
      `P(+|ψ) + P(+|ψ̄) = 1` is forced by [`QLF_BasisIndependence`](lean/QLF_BasisIndependence.lean),
      and indeed for a branch pair no relabeling can exchange the sums are `1.878` and `0.352`. The
      symmetry-lock check this section demanded is applied and reported by the script itself.
    - **Unweighted over depth, the stopping scale is a knob.** `P(+|d)` decays monotonically toward
      `½` with closure depth (`1.000, .962, .917, … .690` at `d = 15`, `R = 3`), so both
      aggregations fixed in advance — coherent `|Σ_d A_c(d)|²` and incoherent `Σ_d |A_c(d)|²` —
      drift with the cutoff, agreeing with each other to three digits, so the choice between them is
      not what is at stake.
  * **The depth measure turns out to be counted, not chosen.** First closures are **prefix-free** —
    a run that has closed is not continued, so no first-closure word extends another — which makes
    the global cylinder measure on the Σ₈ tree, `μ(h) = 8^{−|h|}`, available, and **Kraft's
    inequality** bounds the total at `1` by finite counting alone: at a common horizon `K` each
    first closure at depth `d` owns `8^{K−d}` of the `8^K` complete histories, and prefix-freeness
    makes those sets disjoint. The multiplicity reading of the same fact is the QLF one — **an
    earlier closure weighs more because more complete histories contain it** — so this is the
    possibility tree counting itself, not a probability postulate. Capacity then causes **leakage**,
    never renormalisation: the mass that never closes is simply absent, and one conditions once at
    the end. Measured exactly at `R = 3`: Kraft mass `1.000` (aligned), `0.321` (transverse),
    `0.180` (ZX-mix) — at or below `1` and monotone in every geometry, now an asserted invariant of
    the script. *Correction recorded:* the earlier "not a measure" verdict came from dividing depth
    by depth by the surviving **capacity-limited** population, which sums past `1` (`1.02`, `1.11`).
    That was the error, not the measure.
  * **The normalized-event weight — multiplicity × squared mean phase — fixes the divergence and
    is the best-behaved construction so far.** The divergence is a normalisation, not a verdict: the
    raw signed sum treats each closing word as its own outcome, but if the `W` words closing as the
    same event at the same depth are `W` *ways of one event*, the weight carries the many-to-one
    normalisation,
    `B(c) = Σ_d A_c(d)²/(W_c(d)·8^d) = Σ_d (W_c(d)/8^d)·(A_c(d)/W_c(d))²` — **frequency from how
    many ways the event happens, interference from how coherently those ways add.** Nothing is
    fitted (the depth factor is the cylinder measure, the divisor is the event class), and
    **summability is automatic**: `|A| ≤ W` gives `A²/W ≤ W`, so Kraft bounds the total
    ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) whatever the phases do. Measured exactly: it
    **converges absolutely by depth ~16 with no cutoff**, is **nearly capacity-independent**
    (`0.99386152` at `R = 3` vs `0.99383011` at `R = 4`, a fifth-digit difference where every
    earlier reading moved in the first or second), gives aligned `1.000000` and transverse
    `0.500000`, and is exactly complementary under preparation reversal.
  * **Two-path interference — the decisive test — fails, and now provably.** Two paths (families
    of histories sharing an opening segment) that reach the same detector merge into one event, so
    their amplitudes add before the event normalisation. Four runs, one weight, nothing new
    introduced (`contextual_census.py --two-path`): a **matched pair** gives
    `B(A+B) = B(A) + B(B)` exactly — ratio `1.000000`, where quantum mechanics needs `2` for two
    coherent equal-amplitude paths — an unequal pair gives `0.999288`, and the destructive
    configuration gives `0.000000`. **Destructive interference works; constructive interference is
    unavailable.** And it is unavailable *by theorem*, not by accident: merging can only lower the
    weight, `(A₁+A₂)²/(W₁+W₂) ≤ A₁²/W₁ + A₂²/W₂` (Cauchy–Schwarz in Engel form), with equality
    exactly when the two families carry the same mean phase —
    [`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean) `merge_le_sum`,
    `no_constructive_interference`, `merge_eq_sum_iff`. The very inequality that made the weight
    summable is what forbids the enhancement.
  * **The second horn of that dichotomy is not universal — some geometries carry a convergent
    amplitude with no normalisation at all.** *Don't normalise* fails only when the signed census
    outgrows the measure, which is a statement about growth and so is checkable case by case. It
    does not always hold. Measured at capacity 2 (`--coherent 2`, exact rationals): the transverse
    geometry grows `2.2361^d` and the ZX/ZY mixes `2.6458^d`, both **below** the `√8 = 2.828^d`
    threshold, so `T_c = Σ_d A_c(d)·8^{−d/2}` converges absolutely. Since the closures of one
    geometry share a depth parity, the irrational factor is common to both branches and the weight
    is an **exact rational**: aligned `P(+) = 1`; transverse `T₊ = T₋ = 8/13`, `P(+) = 1/2`; the
    mixes `T₊ = −112/195`, `T₋ = 8/195` — amplitude ratio exactly `−1/14`, **`P(+) = 196/197`**.
    With no per-event normalisation, merging paths adds amplitudes, so **interference works in both
    directions**: `B(A+B)/[B(A)+B(B)] = 2.0000` for a matched pair — the factor of two quantum
    mechanics demands — against `0.0000` destructive.
  * **The threshold is forced, not chosen.** A single way carrying unit phase must weigh exactly its
    own cylinder mass — its share of the complete histories. With amplitude scaling as `μ^s` that way
    weighs `μ^{2s}`, so consistency with the counting reading forces `s = 1/2`, hence `8^{−d/2}` and
    the `√8^d` threshold. So where the sum diverges, it diverges for real.
  * **But this is a property of the geometry, not of the capacity — the correction that matters.**
    The absorbing transfer operator's spectral radius is `3.99` at `R = 2` and `4.38` at `R = 3`,
    both *above* `√8`. The low growth above is therefore **subdominant**: those preparations and
    apparatus happen to project out the dominant modes. So the honest statement is that **certain
    preparation–apparatus pairs carry a convergent amplitude and others do not**, and every geometry
    tested at `R ≥ 3` falls in the second class (`3.97^d`–`4.33^d`). Capacity is not the criterion;
    it was the variable that happened to separate the cases first looked at.
  * **The convergent geometries are a structured class, and a very sparse one — surveyed.** Over
    **1,326 preparation–apparatus pairs** at capacity 2, measured from the *terms* of the series at
    depth 200 (a two-point growth fit taken at depth 90 reads a transient — the same geometry gives
    `8.16` there and `0.19` at depth 200, so the estimator matters):
    - **19 pairs converge — 1.4%** — and every one has an **integer** squared growth, `a² = 5` (7
      cases) or `a² = 7` (12 cases);
    - **20 more sit exactly on the threshold**, `a² = 8.000000`, neither growing nor decaying;
    - above the threshold both integers and irrationals occur (`9.000000` in 119 cases, but also
      `8.162278 = 5+√10`, `8.414214 = 7+√2`, up to `15.85`). **Integrality holds exactly at and
      below the threshold; irrationals appear only above it.**
  * **And the class is characterised by a selection rule relating apparatus to preparation.** Reading
    the branch imbalances of all 39 convergent-or-marginal cases:
    - `a² = 7` ⟺ the two branch targets are **antipodal**, `t₊ = −t₋` — e.g. `(1,0,1,0)` against
      `(−1,0,−1,0)`;
    - `a² = 5` ⟺ the branches **share a component anti-aligned with the preparation** and differ by
      a sign flip on another axis — prep `>` (X) with branches both carrying `X = −1`;
    - `a² = 8`, marginal ⟺ the same shape, but with the shared component **orthogonal** to the
      preparation — prep `/` (Z) with branches both carrying `X = −1`.
    So whether an arrangement has a Born weight at all depends on how the apparatus sits relative to
    the prepared direction — antipodal or anti-aligned yes, orthogonal marginal, otherwise no. That
    is a **selection rule**, read off the data rather than proven, and it is the characterisation
    this section previously listed as open.
  * **The invariant that decides it is spectral, and it is a property of the *readout*.** Write the
    branch amplitude as `A_c(d) = u_c · M^d · v_prep`, with `M` the absorbing closure operator,
    `v_prep` the preparation and `u_c` the functional that collects outcome `c`. Then
    > **`a²` is the largest `|λ|²` in the *joint support* of readout and preparation, and an
    > amplitude exists exactly when that is `< 8`.**

    Predicted from the eigen-structure alone, with no series run, against the measured growth over 90
    geometries: **86 agree exactly** (`14.6569`, `14.4326`, `12.9085`, `15.1433`, `15.0027`,
    `15.2350`, … each reproduced to four decimals) and **all 90 agree on the summability verdict**.
    The four exceptions are one family measured at `8.1623` against a predicted `9.0000` — both above
    threshold, so the verdict is unaffected, and `8.1623` is exactly the shape of a pre-asymptotic
    reading (`ScientificApproach.md` R5).
  * **What that explains.** *Divergent* geometries have `a²` equal to the dominant `λ²` **exactly**
    — nothing special happens, the readout sees the fastest mode and inherits it. *Convergent* ones
    are those whose readout is **blind to the dominant modes**: measured overlap `~10⁻¹⁶` against
    `10⁻¹`–`10⁻²` for divergent ones, a switch rather than a gradient. Their growth then drops to a
    subdominant eigenvalue — `√7`, `√5` — which is why the recurring integers appeared at all: they
    are subdominant eigenvalues of an integer matrix. Blindness to the top eigenspace is **necessary
    but not sufficient** (8 of 140 geometries dodge the top and still excite a second-tier mode above
    `√8`); blindness to *everything* above `√8` is necessary and sufficient, which is just the
    criterion restated.
  * **And it dissolves the "realized threshold" worry.** `a² = 8` is *in the spectrum*, so geometries
    landing exactly on it is expected, not a coincidence demanding that the `8` of `√8` and the `8`
    of the alphabet be secretly the same `8`. The earlier imbalance-based rules (antipodal targets,
    shared component anti-aligned with the preparation) are **proxies** for this orthogonality and
    fail as proxies do — antipodal geometries converge only 52% of the time.
  * **The representation-theoretic explanation is refuted — tested and killed.** *Which* apparatus
    words are dominant-blind looked like it should be a symmetry question: exact orthogonality to a
    16-dimensional eigenspace, for 15.6% of readouts, wants a reason. The operator has a candidate
    symmetry — the axis-relabeling group of [`QLF_BasisIndependence`](lean/QLF_BasisIndependence.lean)
    — and the hypothesis was that a readout is blind exactly when its irrep support misses the
    dominant eigenspace's. **It does not.** All 24 blind readouts among 240 tested (`R = 2`, apparatus
    words up to length 3) have isotypic support that *overlaps* the dominant eigenspace, which is the
    kill condition stated in advance, met unambiguously rather than marginally.

    Two structural facts came out of the attempt and stand on their own:

    - **The operator carries a *sign-twisted* action of the relabeling group, not a permutation
      action.** The naive permutation of states does **not** commute with the transfer operator —
      `max|TP − PT| = 2` for every generator. The twist is forced by the phase rule and is a function
      of the state summary: `flipX ↦ (−1)^{p_X}`, `swapXY ↦ (−1)^{p_X p_Y}`, `swapG ↦ (−1)^{|imb_G|}`,
      and so on. With it, commutation is exact (`0.00e+00`) for all six generators, the group closes
      at order 96, and the action reproduces the relabeled census on actual words — checked against
      ground truth by relabeling every word of length ≤ 3 and rebuilding. This is basis independence
      *at the operator level*, and it is why the relabeling theorem needs balance: off balance the
      sign is real, and here it is exactly what makes the action work.
    - **The dominant eigenspace is `8·trivial ⊕ 4·standard` of an `S₃`.** It is `G`-invariant, 16 of
      the 96 elements act trivially on it, so it carries a faithful representation of `G/K ≅ S₃` with
      character `(16, 8, 4)` on classes of size `(1, 3, 2)` — and contains **no copy of the sign
      representation**. That is a genuine constraint on the operator; it simply is not the constraint
      that decides blindness.

    **A near-miss worth recording, because it nearly passed.** A first attempt obtained the twist by
    *solving* for a diagonal sign matrix making the action commute. That is under-determined — the
    constraint graph fixes signs only per connected component — and the solution found was a
    *different* commuting action of the same order 96, under which the criterion appeared to hold
    `240/240`, then `1584/1584` at length 4. It survived two stress tests and failed only when the
    action was *derived* from the phase rule instead of fitted to the commutation requirement, and
    checked against relabeled words. The group action had been fitted, and it fitted the answer too
    ([`ScientificApproach.md`](ScientificApproach.md) R2).

    So the question returns to the operator, as the kill condition said it would: the fallback is the
    transfer-operator characteristic polynomial per apparatus word, with no symmetry shortcut.

  * **What that changes, and what it does not.** The sub-additivity theorem stands exactly as proven
    — it bounds the *normalized* weight everywhere. What was wrong was the conclusion drawn from it:
    the substrate is not universally unable to carry an amplitude. **Still open, and now sharper:**
    *which apparatus words produce dominant-blind readouts* — a combinatorial question about `u_c`
    rather than a search over geometries — and whether the excited eigenvalue set carries physical
    meaning. Whether 1.4% is a physical selection rule or a sign the encoding is too rigid also
    remains open. Not implicated either way: the measure (proven), the phase rule (proven), the
    depth law (proven), event identity (bracketed).
  * **But it does not render an angle, and that is the test that matters.** Sweeping the apparatus
    does not sweep the weight: adding transverse letters one at a time gives
    `2·arccos√P = 0°, 8.99°, 13.04°, 10.37°, 12.89°, 11.13°` for `a = 0…5` — wobbling, never
    accumulating, where a rotation would step. A grid of `m` Z-letters against `n` X-letters sits at
    `0.97–0.99` almost everywhere regardless of `n/m`, with one inversion to `0.075` at `(2,1)`. And
    *order* dominates composition: the same two letters give exactly `½` as X-then-Z and `0.994` as
    Z-then-X. Both values the construction gets right are symmetry-forced (aligned has a single
    closure, transverse is basis-independence), so the free content is precisely the part that is
    not quantum-mechanical. **The measure question is settled; the amplitude question is not.** The
    decisive next test is a geometry whose QM answer is known *and* unforced — two-path
    interference, or the singlet — which needs multi-history closure rather than another weighting.
  * **Under that measure the counting probability converges and the amplitude does not — the sharp
    obstruction.** Conditioned on closure, `P(c | closure)` from multiplicity is knob-free,
    direction-sensitive, and settling in capacity: aligned `1.000`, transverse `0.500`, ZX-mix
    `0.9164 / 0.9023 / 0.9005` at `R = 3 / 4 / 5`, deeper mix `0.8600 / 0.8237 / 0.8151`. But both
    phase-weighted forms **diverge**: a Born weight needs `|A_c(d)|` to grow no faster than
    `√8^d = 2.828^d`, and the measured growth is `3.91^d, 4.35^d, 4.56^d` at `R = 3, 4, 5`, the gap
    *widening* with capacity. **QLF's own phases cancel too weakly to define an amplitude under the
    one measure that makes its counts summable.** And a pure-count probability is not a Born rule
    either, since counts are provably not weights ([`QLF_Degeneracy`](lean/QLF_Degeneracy.lean) —
    interference is real). So the route now has a derived measure, a convergent multiplicity, and a
    **quantitative target**: the signed census would have to cancel down to `2.828^d`.
  * **A method note, recorded because it produced a wrong answer first.** The same scan in floating
    point is contaminated past `k* ≈ 16 ln 10 / ln(λ₁/λ₂)` — about 730 twists at `R = 3` — where the
    subdominant, preparation-dependent part sinks under the roundoff floor and the arithmetic noise,
    which overlaps the dominant subspace, is what the ratio reports: every preparation then *appears*
    to converge to one universal limit, and does not. Signed transfer-matrix censuses get exact
    integers.
- **Remaining canonical cases** — two-spin singlet, Mach–Zehnder, three-path interference — still to be
  run, and to be run **blind**, with the symmetry-lock check above applied to every agreement.
- **Gleason-theorem connection in Lean**: formalize the QLF-side of Gleason's uniqueness — given the uniform prior and the Pauli algebra, $|A|^2$ is the unique probability functional.
- **Quantum contextuality**: Bell-Kochen-Specker theorem is the constraint that probability assignments must be consistent across measurement contexts. QLF's per-context possibility trees should derive this consistency automatically.

## References

### Internal

- [MRE.md](MRE.md) — per-event $\log 2$ binary-partition optimum, information-theoretic foundation
- [BayesianMechanics.md](BayesianMechanics.md) — multiplicity principle: "the thing that can happen in the most ways happens first"
- [Measurement_Problem.md](Measurement_Problem.md) — §4a measurement = ZFA closure = log 2 per atom; this doc develops the probability assignment behind that information gain
- [Hierarchical_Control.md](Hierarchical_Control.md) — Friston FEP derivation; the Born rule is the recognition density $q$ over the conditional possibility tree
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — Markov blanket as the observer-relative conditioning structure
- [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) — $E + E^\dagger \equiv \text{ZFA}$; the Hermitian-conjugate symmetry that makes $|A|^2 = A^* A$ the unique bilinear probability form
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — Σ₈ Pauli algebra; the structure constants encoding measurement-context relationships
- [Entanglement.md](Entanglement.md) — Bell violations from the non-commutative algebra
- [Experimental_Consistency.md](Experimental_Consistency.md) — §2.1 on the count-balance ∧ Pauli-closure ZFA conjunction
- `path_integral.py` — QuCalc path enumeration
- [Closure_Walk.md](Closure_Walk.md) — the possibility tree as a walk on $\mathbb{Z}^4$; the phase as a $\mathbb{Z}_2$ holonomy, so the signed sum $A$ is a walk on the signed graph (`closure_graph.py` reproduces $-8, 120, -2144$ as a matrix power); ways-proportional sampling of closures and primes (`doob_bridge.py`)

### External

- Born, M. (1926). *Zur Quantenmechanik der Stoßvorgänge.* Z. Phys. 37, 863 — original Born rule postulate.
- Gleason, A. M. (1957). *Measures on the closed subspaces of a Hilbert space.* J. Math. Mech. 6, 885 — uniqueness theorem.
- Feynman, R. P. (1948). *Space-time approach to non-relativistic quantum mechanics.* Rev. Mod. Phys. 20, 367 — path integral formulation.
- Caves, C. M., Fuchs, C. A., Schack, R. (2002). *Quantum probabilities as Bayesian probabilities.* Phys. Rev. A 65, 022305 — QBism, the closest standard-QM reading to the QLF derivation here.
