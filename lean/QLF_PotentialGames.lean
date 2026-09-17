import Mathlib

/-!
# QLF_PotentialGames — a game has a free-action functional iff it is a potential game

The game-theory pilot (quantum-os #209, [`evolutionary_census.py`](../evolutionary_census.py))
ended in three negative results and one positive one, and this module is the theorem behind all
four. Every payoff read off the closure census turned out to be a *potential game* — no Stag Hunt
with a risk/payoff split, no Prisoner's Dilemma — and once the game was supplied as **input**
(payoffs as data, free action := regret), relaxation found the risk-dominant equilibrium every
time and never the payoff-dominant one.

## The statements

For a two-player game `u₁ u₂ : S₁ → S₂ → ℝ`:

* **`HasFreeAction`** — there is one global functional `F` such that every unilateral payoff gain
  is exactly the free action it releases: `u₁ a' b − u₁ a b = F a b − F a' b`, and likewise for
  player 2. This is QLF's native reading of a game: profiles are histories, `F` their free
  action, a **closure** (`IsClosure`) a profile no unilateral move can lower.
* **`FourCycle`** — Monderer–Shapley's integrability condition: around every square of unilateral
  moves the payoff changes sum to zero. Path-independence — a discrete "curl-free" field.
* **`free_action_iff_four_cycle`** — the headline: **a game admits a free-action functional iff
  its payoff changes are path-independent.** `⇒` is a telescoping sum; `⇐` builds `F` by a
  canonical path from a base profile and uses the square condition once.
* **`nash_iff_closure`** — under a free-action functional, **Nash equilibrium = ZFA closure**:
  zero regret is zero free action. This is the encoding `evolutionary_census.py --optimize` runs.
* **`potential_unique_up_to_const`** — the functional is unique up to a constant, so "the
  free-action ordering" of profiles is well defined.
* **`common_interest_potential`** — the generative case: a payoff that is a *shared* quantity
  (both players receive the closure count `W`) is a potential game with `F = −W`. This is why the
  census-derived games could not carry conflict (the `--race`, `--alphabets`, `--cost` no-gos).
* **`symmetric_two_by_two_potential`** — every symmetric 2×2 game is a potential game. So the
  Stag Hunt and the Prisoner's Dilemma are *inside* the class the substrate can carry; what the
  census generated was the common-interest **sub**class, where risk and payoff dominance coincide.
* **`risk_dominance_is_potential_order`** — the anchor for the positive result: in a symmetric
  2×2 game with `a = u(S,S), b = u(S,H), c = u(H,S), d = u(H,H)`, **every** potential satisfies
  `P(S,S) − P(H,H) = (a − c) − (d − b)`: the free-action ordering of the two pure equilibria is
  risk dominance, whatever the payoff ordering. Relaxation toward least free action therefore
  selects the risk-dominant convention — Kandori–Mailath–Rob / Young's stochastic stability, read
  as "the closure with the most ways to arrive" — and not the welfare-optimal one. Measured:
  0 % payoff-dominant under annealing across three Stag Hunts.
* **`matching_pennies_no_free_action`** — the boundary: a pure-conflict game violates the square
  condition, so it has **no** free-action functional. The substrate can *solve* it (regret is still
  defined; the dynamics cycle, reporting that there is no potential to descend) but cannot
  *generate* it. **The substrate generates potential games and solves all games**, and the line
  between them is where a question's conflict content lives.

## Honest scope

Two players, arbitrary strategy types, real payoffs; the only hypotheses are the base points the
construction needs. Monderer & Shapley (1996) prove the same characterization for `n` players via
4-cycles; the `n`-player version and the stochastic-stability theorem itself (Young 1993) are
cited, not reproven. No axioms.
-/

namespace QLF.PotentialGames

variable {S₁ S₂ : Type*}

/-- **A free-action functional**: one global `F` such that every unilateral payoff gain is
    exactly the free action released. -/
def HasFreeAction (u₁ u₂ : S₁ → S₂ → ℝ) : Prop :=
  ∃ F : S₁ → S₂ → ℝ,
    (∀ a a' b, u₁ a' b - u₁ a b = F a b - F a' b) ∧
    (∀ a b b', u₂ a b' - u₂ a b = F a b - F a b')

/-- **An exact potential** (Monderer–Shapley): every unilateral payoff change is the change of
    `P`. A potential is the negative of a free-action functional. -/
def IsPotential (u₁ u₂ : S₁ → S₂ → ℝ) (P : S₁ → S₂ → ℝ) : Prop :=
  (∀ a a' b, u₁ a' b - u₁ a b = P a' b - P a b) ∧
  (∀ a b b', u₂ a b' - u₂ a b = P a b' - P a b)

/-- **The square (4-cycle) condition**: payoff changes are path-independent around every square
    of unilateral moves. -/
def FourCycle (u₁ u₂ : S₁ → S₂ → ℝ) : Prop :=
  ∀ a a' b b',
    (u₁ a' b - u₁ a b) + (u₂ a' b' - u₂ a' b) + (u₁ a b' - u₁ a' b') + (u₂ a b - u₂ a b') = 0

theorem hasFreeAction_iff_exists_potential {u₁ u₂ : S₁ → S₂ → ℝ} :
    HasFreeAction u₁ u₂ ↔ ∃ P, IsPotential u₁ u₂ P := by
  constructor
  · rintro ⟨F, h1, h2⟩
    refine ⟨fun a b => -F a b, ?_, ?_⟩
    · intro a a' b
      show u₁ a' b - u₁ a b = -F a' b - -F a b
      rw [h1 a a' b]
      ring
    · intro a b b'
      show u₂ a b' - u₂ a b = -F a b' - -F a b
      rw [h2 a b b']
      ring
  · rintro ⟨P, h1, h2⟩
    refine ⟨fun a b => -P a b, ?_, ?_⟩
    · intro a a' b
      show u₁ a' b - u₁ a b = -P a b - -P a' b
      rw [h1 a a' b]
      ring
    · intro a b b'
      show u₂ a b' - u₂ a b = -P a b - -P a b'
      rw [h2 a b b']
      ring

/-- A potential game satisfies the square condition (telescoping). -/
theorem potential_fourCycle {u₁ u₂ : S₁ → S₂ → ℝ} {P : S₁ → S₂ → ℝ}
    (h : IsPotential u₁ u₂ P) : FourCycle u₁ u₂ := by
  obtain ⟨h1, h2⟩ := h
  intro a a' b b'
  rw [h1 a a' b, h2 a' b b', h1 a' a b', h2 a b' b]
  ring

/-- The square condition yields a potential: integrate along a canonical path from a base profile
    `(a₀, b₀)` — first player 1's move, then player 2's — and use the square once. -/
theorem fourCycle_potential {u₁ u₂ : S₁ → S₂ → ℝ} (a₀ : S₁) (b₀ : S₂)
    (h : FourCycle u₁ u₂) :
    IsPotential u₁ u₂ (fun a b => (u₁ a b₀ - u₁ a₀ b₀) + (u₂ a b - u₂ a b₀)) := by
  refine ⟨?_, ?_⟩
  · intro a a' b
    show u₁ a' b - u₁ a b
      = ((u₁ a' b₀ - u₁ a₀ b₀) + (u₂ a' b - u₂ a' b₀)) - ((u₁ a b₀ - u₁ a₀ b₀) + (u₂ a b - u₂ a b₀))
    have hc := h a a' b₀ b
    linarith
  · intro a b b'
    show u₂ a b' - u₂ a b
      = ((u₁ a b₀ - u₁ a₀ b₀) + (u₂ a b' - u₂ a b₀)) - ((u₁ a b₀ - u₁ a₀ b₀) + (u₂ a b - u₂ a b₀))
    ring

/-- **A game admits a free-action functional iff its payoff changes are path-independent.** -/
theorem free_action_iff_four_cycle [Nonempty S₁] [Nonempty S₂] {u₁ u₂ : S₁ → S₂ → ℝ} :
    HasFreeAction u₁ u₂ ↔ FourCycle u₁ u₂ := by
  constructor
  · intro hF
    obtain ⟨P, hP⟩ := hasFreeAction_iff_exists_potential.mp hF
    exact potential_fourCycle hP
  · intro h
    obtain ⟨a₀⟩ := ‹Nonempty S₁›
    obtain ⟨b₀⟩ := ‹Nonempty S₂›
    exact hasFreeAction_iff_exists_potential.mpr ⟨_, fourCycle_potential a₀ b₀ h⟩

/-- A Nash equilibrium: no unilateral deviation pays. -/
def IsNash (u₁ u₂ : S₁ → S₂ → ℝ) (a : S₁) (b : S₂) : Prop :=
  (∀ a', u₁ a' b ≤ u₁ a b) ∧ (∀ b', u₂ a b' ≤ u₂ a b)

/-- A ZFA closure of a free-action functional: no unilateral move lowers the free action. -/
def IsClosure (F : S₁ → S₂ → ℝ) (a : S₁) (b : S₂) : Prop :=
  (∀ a', F a b ≤ F a' b) ∧ (∀ b', F a b ≤ F a b')

/-- **Nash equilibrium = ZFA closure.** Under a free-action functional, zero regret is zero free
    action: the profile is an equilibrium iff no unilateral move lowers `F`. -/
theorem nash_iff_closure {u₁ u₂ F : S₁ → S₂ → ℝ}
    (h1 : ∀ a a' b, u₁ a' b - u₁ a b = F a b - F a' b)
    (h2 : ∀ a b b', u₂ a b' - u₂ a b = F a b - F a b') (a : S₁) (b : S₂) :
    IsNash u₁ u₂ a b ↔ IsClosure F a b := by
  constructor
  · rintro ⟨hA, hB⟩
    refine ⟨fun a' => ?_, fun b' => ?_⟩
    · have := h1 a a' b
      have := hA a'
      linarith
    · have := h2 a b b'
      have := hB b'
      linarith
  · rintro ⟨hA, hB⟩
    refine ⟨fun a' => ?_, fun b' => ?_⟩
    · have := h1 a a' b
      have := hA a'
      linarith
    · have := h2 a b b'
      have := hB b'
      linarith

/-- **The potential is unique up to a constant**, so the free-action ordering of profiles is
    well defined. -/
theorem potential_unique_up_to_const {u₁ u₂ P Q : S₁ → S₂ → ℝ}
    (hP : IsPotential u₁ u₂ P) (hQ : IsPotential u₁ u₂ Q) (a₀ : S₁) (b₀ : S₂) (a : S₁) (b : S₂) :
    P a b - Q a b = P a₀ b₀ - Q a₀ b₀ := by
  obtain ⟨hP1, hP2⟩ := hP
  obtain ⟨hQ1, hQ2⟩ := hQ
  have e1 := hP1 a₀ a b
  have e2 := hP2 a₀ b₀ b
  have e3 := hQ1 a₀ a b
  have e4 := hQ2 a₀ b₀ b
  linarith

/-- **The generative case.** A shared payoff — both players receive the same closure count `W` —
    is a potential game with `P = W` (free action `−W`). This is why every census-derived game was
    a potential game: a closure is a shared event. -/
theorem common_interest_potential (W : S₁ → S₂ → ℝ) : IsPotential W W W :=
  ⟨fun _ _ _ => rfl, fun _ _ _ => rfl⟩

/-- The row player's payoff table read for the column player: `u₂ a b = u b a`. -/
def swap (u : Bool → Bool → ℝ) : Bool → Bool → ℝ := fun a b => u b a

/-- **Every symmetric 2×2 game satisfies the square condition** — with two strategies per player
    the square's terms cancel in every case. -/
theorem symmetric_two_by_two_fourCycle (u : Bool → Bool → ℝ) : FourCycle u (swap u) := by
  intro a a' b b'
  cases a <;> cases a' <;> cases b <;> cases b' <;> simp only [swap] <;> ring

/-- **Every symmetric 2×2 game is a potential game.** The Stag Hunt and the Prisoner's Dilemma
    are inside the class the substrate can carry; the census generated only the common-interest
    subclass. -/
theorem symmetric_two_by_two_potential (u : Bool → Bool → ℝ) : HasFreeAction u (swap u) :=
  free_action_iff_four_cycle.mpr (symmetric_two_by_two_fourCycle u)

/-- **Risk dominance is the potential order.** Write `S = true`, `H = false`, and
    `a = u S S, b = u S H, c = u H S, d = u H H`. Every potential of the symmetric game satisfies
    `P S S − P H H = (a − c) − (d − b)`: the free-action ordering of the two pure equilibria is
    risk dominance, independent of which pays more. Least free action selects the risk-dominant
    convention. -/
theorem risk_dominance_is_potential_order (u : Bool → Bool → ℝ) (P : Bool → Bool → ℝ)
    (hP : IsPotential u (swap u) P) :
    P true true - P false false
      = (u true true - u false true) - (u false false - u true false) := by
  obtain ⟨h1, h2⟩ := hP
  have e1 := h1 false true true      -- P S S − P H S = u S S − u H S
  have e2 := h2 false false true     -- P H S − P H H = swap u H S − swap u H H
  simp only [swap] at e2
  linarith

/-- Matching pennies: the row player wants to match, the column player to mismatch. -/
noncomputable def mp₁ : Bool → Bool → ℝ := fun a b => if a = b then 1 else -1

noncomputable def mp₂ : Bool → Bool → ℝ := fun a b => -(mp₁ a b)

/-- Pure conflict violates the square condition. -/
theorem matching_pennies_not_fourCycle : ¬ FourCycle mp₁ mp₂ := by
  intro h
  have hc := h false true false true
  norm_num [mp₁, mp₂] at hc

/-- **The boundary.** A pure-conflict game has no free-action functional: the substrate can solve
    it as input, but cannot generate it. -/
theorem matching_pennies_no_free_action : ¬ HasFreeAction mp₁ mp₂ :=
  fun h => matching_pennies_not_fourCycle (free_action_iff_four_cycle.mp h)

/-- **Status.** Free-action games are exactly the potential games (path-independent payoff
    changes); Nash equilibria are their ZFA closures; shared-closure payoffs are the
    common-interest subclass; every symmetric 2×2 game is in the class, ordered by risk dominance
    under any potential; matching pennies is outside. The substrate generates potential games and
    solves all games. -/
theorem potential_games_summary : True := trivial

end QLF.PotentialGames
