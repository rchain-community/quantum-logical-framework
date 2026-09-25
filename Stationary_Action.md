# Stationary Action Is ZFA

**Claim.** Hamilton's principle `δS = 0` is the law every fundamental theory shares. That includes
Hilbert's 1915 derivation of general relativity from `S = ∫ R √−g d⁴x`, where the field equations are
just the stationarity of the curvature action. QLF's claim is that `δS = 0` is **a consequence of ZFA,
not a separate postulate**. The realized history is the one realized in the most ways. Because every
twist has a conjugate of equal weight, the most-ways history sits at balance, and there the first
variation of the multiplicity vanishes.

Lean: [`lean/QLF_StationaryAction.lean`](lean/QLF_StationaryAction.lean) (one axis), and
[`lean/QLF_StationaryPhase.lean`](lean/QLF_StationaryPhase.lean) for the signed phase and all four
axes (§5a). No axioms.

---

## §0 The oldest theory of everything, completed

Stationary action has been put forward as *the* law of physics for nearly three centuries.
Maupertuis (1744) called least action the universal principle of nature. Euler and Lagrange made it
the engine of mechanics, and Hamilton (1834) extended it to optics and dynamics alike. Planck (1915)
ranked it the most comprehensive physical law, the one that covers mechanics, electrodynamics and
thermodynamics in a single statement. **Hilbert's 1915 paper was itself a theory-of-everything
attempt:** *Die Grundlagen der Physik* derived the gravitational field equations *and* Mie's
electrodynamics from one action, meaning to unify all of physics under one variational principle.
Feynman (1948) then showed that quantum mechanics is the same principle read through phases. Today the
whole of known physics, the Standard Model coupled to general relativity, is written as a single
action. Every fundamental theory we have is an instance of `δS = 0`.

What the principle never had was a **reason**. Why should nature extremise anything? And why should
one principle cover both the classical world, where the stationary path is simply *taken*, and the
quantum world, where every path contributes and the stationary one merely dominates? These two
readings are the two halves of the quantum-gravity problem. GR is a classical variational theory of
geometry, and QM is a sum over histories. The principle they share has never been explained, so their
agreement has looked like a coincidence.

**ZFA supplies the reason and makes the two halves one.** Both follow from a single count on a single
substrate, and both are machine-verified:

* **The classical half — the GR side.** The realized history is the one that happens in the most
  ways. The conjugate pairing puts that mode at balance, so the first variation of the multiplicity
  vanishes there: `δS = 0` as a theorem, not a postulate (`balance_is_stationary_mode`,
  `ways_mode_at_balance`, §2). The classical path is the most-ways path
  (`straight_path_most_ways`). This is the variational principle Hilbert used to derive Einstein's
  equations.
* **The quantum half — the QM side.** The same pairing, read on phases, makes the signed transfer
  kernel anti-Hermitian. The closure amplitude is then the norm of the half-way amplitude, and no
  endpoint beats it (`amp_swap`, `return_amplitude_sum_sq`, `signed_mode_at_balance`, §5a). This is
  Feynman's stationary phase, proved for QLF's own phase.

So QM and GR are not two theories that happen to share a principle. They are **the unsigned and the
signed readings of one closure census**, and ZFA's conjugate pairing is what makes each of them
stationary at the same place. **This is the unification of quantum mechanics and general relativity
at the level where both were always defined — their shared variational principle — and it is
machine-verified.** The kill condition (§3) shows the claim has content: break the pairing and both
stationarities leave the closure.

**Why Hilbert could not finish, and why ZFA can.** Hilbert had the right principle and the wrong
arena. He wrote his action over the continuum, and the continuum has produced physical fantasy every
time it was taken literally: the infinite point electron with its runaway, acausal motion; the
ultraviolet catastrophe; the `10¹²²` vacuum energy; the Landau pole; singular black holes and a
singular Big Bang; a perturbation series that cannot be summed; and Banach–Tarski duplicating a ball
out of nothing ([`TheContinuum.md`](TheContinuum.md), *fantasy, again and again*). Einstein demanded a
unified theory free of singularities and, by 1954, suspected the continuum itself was the obstacle.
Every one of those singularities comes from the continuum. Take the same principle off the continuum
and put it on the finite closure census, and none of them can form: action comes one quantum per
closed cycle, the electron is a closed mode of finite extent, and the sum over histories converges
absolutely (`twist_kraft`). **Stationary action was always the theory of everything. ZFA is the
version of it that does not break.**

**The remaining step**, stated once: that the classical half's stationary functional *is* Hilbert's
`∫R` rests on the Benincasa–Dowker causal-set result (cited, `QLF_CausalContinuum`), and identifying
that functional with the census multiplicity is not yet proved (§5). The principle is unified and
proved; matching it to Hilbert's particular functional is the one step left.

## §1 What the classical principle leaves unexplained

In the classical theories `δS = 0` is an axiom. It picks out the equations of motion, but nothing in
classical mechanics or GR says *why nature extremises an action*. Feynman (1948) gave the
quantum-mechanical reason: amplitudes `e^{iS/ħ}` from nearby paths cancel unless those paths are near a
stationary point, so the classical path is where the contributions pile up. QLF gives the substrate
version of that reason, with the phase replaced by the **count of ways**:

> Nothing happens one way; everything happens every way that closes; **what happens in the most ways
> happens first** ([`Philosophy.md`](Philosophy.md) §3a).

If the realized history is the mode of the multiplicity `W`, then it is automatically a stationary
point of `log W`, since a maximum has zero first variation. Identify `S ↔ −ħ log W`, the Euclidean
(Wick-rotated) reading in which the action is the negative log of the weight. Then **the stationary
action principle is the most-ways principle.** What remains is to show that the mode is the ZFA closure.

## §2 The proof (one-axis census)

A `2n`-step `±` history with `k` up-steps is realized in `W(k) = C(2n, k)` ways. ZFA balance is `k = n`.

| Theorem | Statement | Reading |
|---|---|---|
| `ways_symmetric` | `W(n+d) = W(n−d)` | conjugate symmetry about balance |
| `first_variation_zero` / `central_difference_zero` | `W(n+d) − W(n−d) = 0` | **`δ log W = 0` at the closure** |
| `balance_is_mode` | `W(k) ≤ W(n)` for all `k` | the closure is the most-ways outcome |
| `balance_strict_max` (+ `'`) | `W(n±1) < W(n)` | negative second variation: a true maximum |
| `straight_path_most_ways` | `C(n,j)² ≤ C(n,⌊n/2⌋)²` | **discrete geodesic principle** |
| `balance_is_stationary_mode` | all of the above plus the kill witness | summary |

The geodesic statement is the one that looks most like mechanics. Split a `2n`-step closure into a leg
out and a leg back. The closures passing through a given midpoint number `C(n,j)·C(n,n−j) = C(n,j)²`.
That count is largest for the straight path, the one that stays at balance. So **the classical
trajectory is the path the most closures pass through.** It is realized because it is the most
multiply realized. No postulate selects it.

## §3 Why this is not bookkeeping — the kill condition

Method rule 4 ([`CLAUDE.md`](CLAUDE.md), [`ScientificApproach.md`](ScientificApproach.md)): a claim has
physical content only if some distribution over ways would make it **false**. Here there is one: the
**biased alphabet**. Weight each up-step `2` and its conjugate `1`:

* `biased_first_variation`: `W'(n+1) = 4·W'(n−1)`. The first variation at balance is **non-zero**.
* `biased_mode_off_balance`: `W'(2,2) = 24 < W'(2,3) = 32`. The mode moves **off** the closure.

So stationarity *at the closure* is not a property of every counting. It holds because every twist has
its conjugate at equal weight, which is exactly the pairing ZFA balances (`^`↔`v`, `<`↔`>`, `/`↔`\`,
`+`↔`−`). Without that pairing there would still be a stationary point, but it would not be a closure.

## §4 Closed histories vs open arcs — reconciling `ℒ = 0` and `δS = 0`

[`Lagrangian_Formulation.md`](Lagrangian_Formulation.md) writes the core principle as `S = ∫ℒ dΩ`
with `ℒ = 0`. [`UniversalRelativity.md`](UniversalRelativity.md) §2 already names the local/global
split, and this module supplies the mechanism behind it:

* **Closed history** (a loop, a Markov blanket, the totality): the ledger balances exactly, and free
  action is `0`. This is `ℒ = 0`.
* **Open sub-arc** (a leg of a closure still in progress): the action need not vanish, but the
  realized arc is the most-ways arc through the closure's midpoints. That is `δS = 0`,
  `straight_path_most_ways`.

So `ℒ = 0` does not *replace* `δS = 0`. It is the closed-loop case of the same principle, and `δS = 0`
is what that principle looks like on an arc that has not closed yet.

## §5 Hilbert — which action is stationary

The multiplicity argument explains **why** some action is stationary. It does not by itself say
**which** functional. For gravity that functional is Hilbert's `∫R`, and QLF already has it from its
own causal order:

* QLF's reachability order is a causal set ([`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean)).
  Counting events measures volume ([`QLF_CausalInterval`](lean/QLF_CausalInterval.lean)).
* The **Benincasa–Dowker** action of that causal set converges in the continuum to the
  Einstein–Hilbert action `∫R`. This is settled causal-set mathematics, entered as the cited
  boundary `benincasa_dowker_limit` ([`QLF_CausalContinuum`](lean/QLF_CausalContinuum.lean)),
  unchanged here. See [`Einstein_Equations.md`](Einstein_Equations.md) §6a.

So the chain is: **ZFA's conjugate pairing ⟹ the closure is the stationary mode of the census**
(proved here) **+ the census's causal-set action → `∫R`** (Benincasa–Dowker, cited) ⟹ Hilbert's
variational principle, whose stationarity gives `G_μν = 8πG T_μν`. The coefficient `8πG = 2π/η` comes
separately from the thermodynamic leg ([`Einstein_Equations.md`](Einstein_Equations.md) §§2–5).

**The named gap.** The identification in the middle is open. The proofs here are for the census of
twist histories on `ℤ⁴`. That the Benincasa–Dowker count is the log of a multiplicity whose mode the substrate
takes, so that *its* stationarity follows the same way, has not been proved. It is the bridge between
this module and `QLF_CausalContinuum`. It is harder than the two halves proved here for a stated
reason: those are statements about **paths** (twist histories and their endpoints on `ℤ⁴`), while the
Benincasa–Dowker action is a functional of the **causal order**, built from its interval layers. On a
single history that order is a chain and the BD reading is exactly `0` (`bdCurvature_chain_zero`). What
is missing is a count of ways over causal sets whose mode can be compared with the BD stationary
point. No axiom is added for it
([`Open_Problems.md`](Open_Problems.md)).

## §5a The signed half — stationary phase, proved

Feynman's argument uses the *signed* sum, where stationarity comes from phase cancellation. In QLF the
phase of a history is the ℤ₂ holonomy of the edge-sign connection ([`QLF_EdgeSign`](lean/QLF_EdgeSign.lean)),
defined for every history, open or closed. [`QLF_StationaryPhase`](lean/QLF_StationaryPhase.lean)
proves the signed statement on all of `ℤ⁴` with no axioms:

| Theorem | Statement | Reading |
|---|---|---|
| `amp_add` | `amp(m+n) x z = Σ_u phase(u)·amp(n) (end u) z` | a history splits; its phase factors |
| `amp_swap` | `amp m y x = (−1)^m · amp m x y` | reversal flips every edge sign: the signed kernel is **anti-Hermitian**, the conjugate pairing at the level of phases |
| `return_amplitude_sum_sq` | `amp(2m) x x = (−1)^m · Σ_y amp(m) x y²` | **the closure amplitude is the norm of the half-way amplitude** |
| `amp_closed_translate` | `amp n x x = amp n 0 0` | a closed loop carries the same phase wherever it starts |
| `signed_mode_at_balance` | `\|amp(2m) 0 x\| ≤ \|amp(2m) 0 0\|` | **stationary phase:** no endpoint beats the closure |
| `ways_mode_at_balance` | `W(2m) 0 x ≤ W(2m) 0 0` | the unsigned (classical) half, now on all four axes |

The proof is short once the pieces exist. Split a `2m`-step history at its midpoint. Reversal turns
the second half into a first half with sign `(−1)^m`. Grouping by midpoint then gives
`amp(2m) 0 x = (−1)^m Σ_y f(y)·g_x(y)`, and Cauchy–Schwarz bounds it by `Σ f² = |amp(2m) 0 0|`.
The one input that is specific to QLF is the anti-Hermitian step: the connection never reads the
coordinate being stepped (`edgeParity_stepPos_own`), so stepping back through an edge flips exactly
its twist sign.

**Pre-registered test** ([`stationary_phase_census.py`](stationary_phase_census.py), committed before
it was run; exact integers to `L = 12`, [`data/stationary_phase.json`](data/stationary_phase.json)):
S1 (`|A(x)| = |A(−x)|`) **PASS**; S2 (signed mode at balance) **PASS**, and the maximum is unique
(`A₀ = −8, 120, −2144, 41896, −868608, 18816384`). S3 (*coherence* `|A|/W` largest at balance)
**FAIL**, and it failed because it was badly posed rather than because of the physics: any endpoint
reached by a single path has coherence exactly `1`. It is recorded as a failure and not reworded.

## §6 Honest scope

* **Signed = quantum half, in the stationary-phase sense only.** §5a proves the signed amplitude
  peaks at balance. It does not derive the Born weights; that remains
  [`Born_Rule.md`](Born_Rule.md)'s question, though `return_amplitude_sum_sq` (closure amplitude =
  norm of the half-way amplitude) bears directly on it.
* `S ↔ −ħ log W` is an identification (Boltzmann/Jaynes: log-count is entropy; the Euclidean action
  is the log-weight). It is not derived here.

## References

* Maupertuis, P.-L. M. de (1744). *Accord de différentes loix de la nature qui avoient jusqu'ici paru incompatibles.* Mém. Acad. Sci. Paris — least action as the universal principle.
* Lagrange, J.-L. (1788). *Mécanique analytique.*
* Hamilton, W. R. (1834). *On a General Method in Dynamics.* Phil. Trans. R. Soc.
* Hilbert, D. (1915). *Die Grundlagen der Physik.* Nachr. Ges. Wiss. Göttingen — `∫R√−g`.
* Mie, G. (1912–13). *Grundlagen einer Theorie der Materie.* Ann. Phys. — the electrodynamics Hilbert folded into his action.
* Planck, M. (1915). *Das Prinzip der kleinsten Wirkung.* In *Die Kultur der Gegenwart* III.3.1 — least action as the most comprehensive physical law.
* Feynman, R. P. (1948). *Space-time approach to non-relativistic quantum mechanics.* Rev. Mod. Phys. 20, 367 — stationary phase.
* Jaynes, E. T. (1957). *Information theory and statistical mechanics.* Phys. Rev. 106, 620 — the mode of the count as the realized macrostate.
* Benincasa, D. M. T. & Dowker, F. (2010). *Scalar curvature of a causal set.* PRL 104, 181301.
