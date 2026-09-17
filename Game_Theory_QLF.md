# Game theory from QLF — what the closure census generates, and what it solves

**Status:** two machine-verified modules ([`QLF_PotentialGames`](lean/QLF_PotentialGames.lean),
[`QLF_EvolutionaryGames`](lean/QLF_EvolutionaryGames.lean), no axioms), one exact/numerical tool
([`evolutionary_census.py`](evolutionary_census.py)), five pre-registered runs whose outcomes are
recorded below whichever way they landed, and one operational consequence for the QuantumOS room
([`Collective_Optimization.md`](https://github.com/rchain-community/quantum-os/blob/main/Collective_Optimization.md)).
Origin: quantum-os [#209](https://github.com/rchain-community/quantum-os/issues/209).

> **The one-line result.** *The substrate generates potential games and solves all games.* A game
> has a free-action functional iff it is a potential game (`free_action_iff_four_cycle`); under
> that functional a Nash equilibrium is a ZFA closure (`nash_iff_closure`); least free action
> selects the risk-dominant convention, never the welfare-optimal one
> (`risk_dominance_is_potential_order`); and to maximise welfare you make the closure joint
> (`welfare_game_potential`). Conflict is not in the substrate — it is in the question.

---

## 1. The method, and the three no-gos it produced first

The pilot asked whether "what happens in the most ways happens first"
([`Philosophy.md`](Philosophy.md) §3a) predicts equilibrium selection the way evolutionary game
theory does — Kandori–Mailath–Rob (1993) / Young (1993): with vanishing mutation, the selected
equilibrium is the one reached by the most mutation paths. The test case was the Stag Hunt, where
the risk-dominant and payoff-dominant equilibria differ.

Every step was pre-registered with a kill condition ([`ScientificApproach.md`](ScientificApproach.md)),
and the first three representations were killed — each for a structural reason, recorded rather
than tuned around (R2a):

| representation | payoff | outcome | reason |
|---|---|---|---|
| strand + free continuations | ways the pair closes / a's own ways closed | 216 coordination games, **0 Stag Hunt**; even `P_own` symmetric on 0/861 pairs | closability of `a`'s continuation depends only on `imb(a)+imb(b)` |
| strategy = move set | own ways closed by the partner | asymmetric at last, still **0** | payoff monotone in move-set inclusion: the larger set is simply dominant |
| free-action cost `W/2^F` (parameter-free, both sides in bits) | ways discounted per bit held open | **0** | self-fitness strictly decreasing in depth (`36 > 7.5 > 1`): a deep commitment is never payoff-dominant |

The theorem behind all three is `common_interest_potential`: **a payoff that is the multiplicity
of a shared closure is a potential game** — both players receive the same number, risk dominance
and payoff dominance coincide, and the KMR test cannot fail. By rule 4 that is bookkeeping. A
closure is a shared event; there is no private payoff in it to be captured at a partner's expense.

## 2. What the census's own dynamic does generate

Inverting the question — let the absorbing first-closure census run and read off what it does —
gives a game with nothing imposed. Two open strands share one walk over the six spatial twists;
the run ends when the walk closes `a`, closes `b`, or closes the **pair jointly**
(`imb(walk) = −(imb(a)+imb(b))`, the shared closure of [`Chemistry.md`](Chemistry.md) /
[`SEX.md`](SEX.md)); a player's payoff is the closure event's own cylinder-measure frequency.

Pre-registered and confirmed (`evolutionary_census.py --race`, exact rationals):

* **Complementarity.** The best reply to every strand is its conjugate — `u = 1.000`, joint closure
  at depth 0 (`conjugate_pair_closes`). An orthogonal strand is middling (`≈ 0.25`) and **the same
  strand is the worst partner** (`≈ 0.15`: two identical strands race for one target). Like-with-like
  is blocked, complementary pairs bind — the `pn`-binds / `pp`-blocked pattern of `SEX.md`, from the
  census alone.
* **Fisher's 1 : 1.** Replicator dynamics settle at exactly `½ : ½` within a conjugate pair.
  Machine-checked as an ESS: `fisher_half_ess` — against any other mixture `p`, the `½` mixture earns
  more than `p` earns against itself, by `2(1 − a)(p − ½)²`.
* **A collective basis choice** (not pre-registered — the finding). The uniform population is an
  *unstable* equilibrium; every run collapses to a single conjugate pair and the other two axes go
  extinct, the winner set by initial conditions. The threshold is exact (`pair_uninvadable_iff`,
  `pair_beats_uniform_iff`): the population must pick a basis iff **`1 + a > 2b`** — conjugate
  bonding beats twice the orthogonal payoff; measured `1.148 > 0.494`. The basis belongs to the
  question ([`QLF_BasisIndependence`](lean/QLF_BasisIndependence.lean)); here a population *answers* it.
* **Still no conflict**, with two-axis and doubled strands admitted as players (24 strategies):
  174 anti-coordination pairs, 102 dominance pairs, 0 coordination games, 0 Stag Hunt — and **0
  Prisoner's Dilemmas**: in all 102 dominance relations the dominant strategy is also collectively
  best. The census has no defection structure.

So the substrate's own game is two-level: **anti-coordination within an axis** (complementarity,
a stable 1 : 1) and **coordination across axes** (three symmetric equilibria, symmetry breaking).

## 3. The correction: the game is input, the substrate is the solver

The no-gos were a framing error — the no-fitting rule applied to the wrong object. In an
optimization problem the *objective is given* and the *solver* must be parameter-free, which is
exactly how the room works: it relaxes toward a low-energy consensus for a stated objective. The
canonical encoding, with no constant:

* payoffs `(a, b, c, d)` are data, like a QUBO;
* the **free action of a population state is its total regret** — the gain agents could take by
  switching unilaterally — so **a Nash equilibrium is a ZFA closure** (`nash_iff_closure`); the
  mixed equilibrium shows up as an unstable interior closure (`x = 34` of `50`), the encoding
  checking itself;
* "the ways to arrive" at a closure are its basin under logit revision (`basins_partition`,
  `sum_frequency`: closure frequency is multiplicity); annealing is the inverse temperature rising.

Pre-registered: (i) cold dynamics land by basin, the Stag share equalling `1 − p*` (Young's
threshold); (ii) a slow anneal reaches the payoff-dominant equilibrium more often than a cold
start. **Result** (`--optimize`, N = 50, 200 runs):

| game | payoff-dom | risk-dom | `1 − p*` | cold | anneal |
|---|---|---|---|---|---|
| Stag Hunt (4,0,3,2) | S | H | 0.33 | **0.32** | **0.00** |
| Stag Hunt (5,0,4,3) | S | H | 0.25 | **0.24** | **0.00** |
| Stag Hunt (9,0,8,7) | S | H | 0.12 | **0.13** | **0.00** |
| Prisoner's Dilemma | — | — | — | 0.00 | 0.00 |

(i) holds to two decimals — *most ways is the basin*. (ii) is **killed**: annealing reaches the
payoff-dominant equilibrium in 0 % of runs, worse than cold; the hot phase equilibrates on the
stochastically stable state and cooling locks it in — KMR exactly. The theorem:
`risk_dominance_is_potential_order` — in a symmetric 2×2 game *every* potential satisfies
`P(S,S) − P(H,H) = (a − c) − (d − b)`, so least free action orders the two pure equilibria by risk
dominance whatever the payoff ordering. **The substrate is a reliable optimizer of stochastic
potential — the noise-robust equilibrium — and not of welfare, and no temperature schedule makes
it one.**

## 4. Welfare: make the closure joint

To maximise welfare `W = u₁ + u₂`, change what the closure *is*, not how the substrate relaxes: pay
every player the total. That is a common-interest game, hence a potential game with potential `W`
(`welfare_game_potential`), its closures are the local welfare optima
(`welfare_nash_iff_local_optimum`), and least free action *is* welfare maximisation. Groves/VCG
alignment, read as "score by the shared objective". Pre-registered and run (`--optimize --welfare`):
the three Stag Hunts go from **0 % to 100 %** payoff-dominant, and the Prisoner's Dilemma becomes
**100 % cooperation** (under welfare, cooperation is dominant).

This closes the loop with §1: the games the substrate *generates* are welfare-aligned by
construction, because a joint closure is a shared event with a shared payoff. A given game's
conflict is exactly the gap between private payoffs and the joint closure.

## 5. The boundary

Matching pennies has no free-action functional (`matching_pennies_no_free_action`): its payoff
changes are not path-independent, so there is no potential to descend and the regret dynamics
cycle. That is not a failure — a cycle is the substrate *reporting* that the game is pure conflict
— but it marks the edge: the substrate **generates** potential games, **solves** all games, and the
line between them is where a question's conflict content lives. Whether the census's phase /
interference machinery ([`Born_Rule.md`](Born_Rule.md)) has anything to say about mixed equilibria
as distributions over ways is open, and flagged as speculative.

## 6. The five theorems

| # | statement | anchor |
|---|---|---|
| 1 | a game has a free-action functional iff it is a potential game (Monderer–Shapley's square condition, both directions) — two players, and at any `n` | `free_action_iff_four_cycle` (`QLF_PotentialGames`; `QLF_NPlayerPotential`) |
| 2 | the ways to a closure are its basin; basins partition the state space; closure frequency is multiplicity — the finite form of stochastic stability (KMR/Young's `μ → 0` limit cited) | `basins_partition`, `sum_frequency`, `ways_eq_zero_of_not_fixed` |
| 3 | free-action descent terminates on any finite state space; a unilateral improvement raises the potential; every finite two-player potential game has a pure Nash equilibrium | `Descent.eventually_fixed`, `improve_increases_potential`, `exists_nash_of_potential` |
| 4 | the population picks a basis iff `1 + a > 2b`, and the measured race is past it | `pair_uninvadable_iff`, `pair_beats_uniform_iff`, `measured_threshold_holds` |
| 5 | the `½ : ½` conjugate pairing is an ESS whenever the conjugate beats a copy | `half_is_equilibrium`, `fisher_half_ess` |

Plus the selection and welfare anchors: `nash_iff_closure`, `risk_dominance_is_potential_order`,
`common_interest_potential`, `symmetric_two_by_two_potential`, `welfare_game_potential`,
`welfare_nash_iff_local_optimum`, `matching_pennies_no_free_action`.

## 7. For the room

The falsifiable, theorem-backed content for
[`Collective_Optimization.md`](https://github.com/rchain-community/quantum-os/blob/main/Collective_Optimization.md):

* **Consensus-by-relaxation is conservative.** In a coordination problem with a risk/payoff split,
  a room that anneals converges on the *safe* convention — reliably, and regardless of schedule.
* **The remedy is the objective, not the temperature.** Score candidates by the shared objective
  (`/estimate` on collective value), not by private gain; commitments (`/lemma`) and trust-weighting
  that enlarge the cooperative basin are Groves-style alignment devices. The KMR prediction is a
  step function: a device works iff it moves the basin threshold `p*` across `½`.
* **The next experiment is human.** A real Stag Hunt posed to real peers (the group testing session,
  quantum-os #137): does the room converge on the safe convention as the model says (it does in
  Van Huyck–Battalio–Beil 1990), and does a commitment round flip it only when it crosses the
  threshold?

## Honest scope

The characterization, Nash = closure, pure-equilibrium existence and the welfare theorem are proven at
**any number of players** ([`QLF_NPlayerPotential`](lean/QLF_NPlayerPotential.lean) — the room's arity;
Monderer–Shapley's *squares suffice* proven by a `Finset` induction over players); the selection results
(`risk_dominance_is_potential_order`, the race thresholds) are 2×2 statements by nature; Young's
stochastic-stability theorem is cited, not reproven. The lattice inequality behind "like-with-like is the worst partner" (an
orthogonal partner beats a copy in the ℤ³ first-passage race) is measured, not proven. Everything
numerical is a lower bound with a stable ordering (the 3-D walk is transient; Kraft leakage).

## See also

[`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) Rung 10 · [`Philosophy.md`](Philosophy.md) §3a ·
[`ScientificApproach.md`](ScientificApproach.md) · [`SEX.md`](SEX.md) · [`Chemistry.md`](Chemistry.md) ·
[`QLF_ShannonFromCounts`](lean/QLF_ShannonFromCounts.lean) (the bits both sides of the cost were
measured in) · [`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §8 (the meeting of minds).
