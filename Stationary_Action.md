# Stationary Action Is ZFA

**Claim.** Hamilton's principle `δS = 0` is the law every fundamental theory shares. That includes
Hilbert's 1915 derivation of general relativity from `S = ∫ R √−g d⁴x`, where the field equations are
just the stationarity of the curvature action. QLF's claim is that `δS = 0` is **a consequence of ZFA,
not a separate postulate**. The realized history is the one realized in the most ways. Because every
twist has a conjugate of equal weight, the most-ways history sits at balance, and there the first
variation of the multiplicity vanishes.

Lean: [`lean/QLF_StationaryAction.lean`](lean/QLF_StationaryAction.lean). No axioms.

---

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

**The named gap.** The identification in the middle is open. The proof above is for the one-axis
census `W`. That the Benincasa–Dowker count is the log of a multiplicity whose mode the substrate
takes, so that *its* stationarity follows the same way, has not been proved. It is the bridge between
this module and `QLF_CausalContinuum`. No axiom is added for it
([`Open_Problems.md`](Open_Problems.md)).

## §6 Honest scope

* **Unsigned vs signed.** `W` is the *unsigned* census (balance, the classical count). Feynman's
  quantum argument uses the *signed* sum, where stationarity comes from phase cancellation. In QLF the
  phase is the ℤ₂ holonomy of [`QLF_EdgeSign`](lean/QLF_EdgeSign.lean). The result here is the
  classical/Euclidean half. The signed stationary-phase version is the quantum half and is not
  claimed ([`Born_Rule.md`](Born_Rule.md)).
* **One axis.** The four-axis census `walkCount` ([`QLF_ProductWalk`](lean/QLF_ProductWalk.lean))
  factors into per-axis `±` walks. Stating the mode result on it is a routine extension that has not
  been done yet.
* `S ↔ −ħ log W` is an identification (Boltzmann/Jaynes: log-count is entropy; the Euclidean action
  is the log-weight). It is not derived here.

## References

* Hamilton, W. R. (1834). *On a General Method in Dynamics.* Phil. Trans. R. Soc.
* Hilbert, D. (1915). *Die Grundlagen der Physik.* Nachr. Ges. Wiss. Göttingen — `∫R√−g`.
* Feynman, R. P. (1948). *Space-time approach to non-relativistic quantum mechanics.* Rev. Mod. Phys. 20, 367 — stationary phase.
* Jaynes, E. T. (1957). *Information theory and statistical mechanics.* Phys. Rev. 106, 620 — the mode of the count as the realized macrostate.
* Benincasa, D. M. T. & Dowker, F. (2010). *Scalar curvature of a causal set.* PRL 104, 181301.
