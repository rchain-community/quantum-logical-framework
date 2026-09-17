import Mathlib

/-!
# QLF_NPlayerPotential — the free-action characterization at the room's arity

[`QLF_PotentialGames`](QLF_PotentialGames.lean) proves *a game has a free-action functional iff it
is a potential game* for two players. A QuantumOS room is `n` players, and
[`Collective_Optimization.md`](https://github.com/rchain-community/quantum-os/blob/main/Collective_Optimization.md)
states the result at that arity — so here it is at that arity. Profiles are dependent functions
`(i : ι) → S i`; a unilateral move is `Function.update s i x`.

* **`HasFreeAction u`** — one global `F` with every unilateral payoff gain the free action released.
* **`IsPotential u P`** — Monderer–Shapley's exact potential, `n` players.
* **`FourCycle u`** — the square condition for every *pair* of players: around the square
  `s → s[i:=x] → s[i:=x][j:=y] → s[j:=y] → s` the four payoff changes sum to zero.
* **`free_action_iff_four_cycle`** — the characterization: **a game admits a free-action
  functional iff its payoff changes are path-independent around every square**, for any number of
  players. Monderer & Shapley (1996), Theorem 2.8: squares suffice — no longer cycle is ever needed.
  `⇒` is telescoping; `⇐` builds the potential player by player (`fourCycle_potential_on`, an
  induction over a `Finset` of players: reset the new player to a base profile, add its own payoff
  difference, and use one square to commute its move past every earlier player's).
* **`nash_iff_closure`**, **`exists_nash_of_potential`** — Nash equilibrium = ZFA closure, and every
  finite `n`-player potential game has a pure one (the potential's maximiser).
* **`common_interest_potential`**, **`welfare_game_potential`** — a shared payoff is a potential game
  with itself as potential; paying every player the total welfare makes least free action welfare
  maximisation — *make the closure joint*, at `n`.

Descent termination is already arity-free ([`QLF_EvolutionaryGames`](QLF_EvolutionaryGames.lean),
`Descent.eventually_fixed`); the two-player module's selection results
(`risk_dominance_is_potential_order`) are 2×2 statements by nature; Young's stochastic-stability
theorem stays cited. No axioms.
-/

namespace QLF.NPlayerPotential

open Function

variable {ι : Type*} {S : ι → Type*} [DecidableEq ι]

/-- **A free-action functional** for `n` players. -/
def HasFreeAction (u : ι → ((j : ι) → S j) → ℝ) : Prop :=
  ∃ F : ((j : ι) → S j) → ℝ,
    ∀ (i : ι) (s : (j : ι) → S j) (x : S i), u i (update s i x) - u i s = F s - F (update s i x)

/-- **An exact potential** for `n` players. -/
def IsPotential (u : ι → ((j : ι) → S j) → ℝ) (P : ((j : ι) → S j) → ℝ) : Prop :=
  ∀ (i : ι) (s : (j : ι) → S j) (x : S i), u i (update s i x) - u i s = P (update s i x) - P s

/-- A potential for the players in `T` only — the induction invariant. -/
def IsPotentialOn (u : ι → ((j : ι) → S j) → ℝ) (T : Finset ι)
    (P : ((j : ι) → S j) → ℝ) : Prop :=
  ∀ i ∈ T, ∀ (s : (j : ι) → S j) (x : S i), u i (update s i x) - u i s = P (update s i x) - P s

/-- **The square condition** for every pair of distinct players. -/
def FourCycle (u : ι → ((j : ι) → S j) → ℝ) : Prop :=
  ∀ (i j : ι), i ≠ j → ∀ (s : (j : ι) → S j) (x : S i) (y : S j),
    (u i (update s i x) - u i s)
    + (u j (update (update s i x) j y) - u j (update s i x))
    + (u i (update s j y) - u i (update (update s i x) j y))
    + (u j s - u j (update s j y)) = 0

theorem hasFreeAction_iff_exists_potential {u : ι → ((j : ι) → S j) → ℝ} :
    HasFreeAction u ↔ ∃ P, IsPotential u P := by
  constructor
  · rintro ⟨F, hF⟩
    refine ⟨fun s => -F s, fun i s x => ?_⟩
    show u i (update s i x) - u i s = -F (update s i x) - -F s
    rw [hF i s x]
    ring
  · rintro ⟨P, hP⟩
    refine ⟨fun s => -P s, fun i s x => ?_⟩
    show u i (update s i x) - u i s = -P s - -P (update s i x)
    rw [hP i s x]
    ring

-- ==========================================
-- ⇒ : a potential game satisfies every square
-- ==========================================

/-- Resetting a player to its own value after a move by another player undoes the first move. -/
theorem update_update_self_of_ne {i j : ι} (hij : i ≠ j) (s : (k : ι) → S k) (x : S i) (y : S j) :
    update (update (update s i x) j y) i (s i) = update s j y := by
  rw [update_comm hij, update_idem]
  have hne : update s j y i = s i := by simp [hij]
  conv_lhs => rw [← hne]
  exact update_eq_self i (update s j y)

theorem update_update_same_self (s : (k : ι) → S k) (j : ι) (y : S j) :
    update (update s j y) j (s j) = s := by
  rw [update_idem]
  exact update_eq_self j s

theorem potential_fourCycle {u : ι → ((j : ι) → S j) → ℝ} {P : ((j : ι) → S j) → ℝ}
    (hP : IsPotential u P) : FourCycle u := by
  intro i j hij s x y
  have t1 := hP i s x
  have t2 := hP j (update s i x) y
  have t3 := hP i (update (update s i x) j y) (s i)
  rw [update_update_self_of_ne hij] at t3
  have t4 := hP j (update s j y) (s j)
  rw [update_update_same_self] at t4
  linarith

-- ==========================================
-- ⇐ : squares build the potential, one player at a time
-- ==========================================

/-- Given a potential for the players in `T` and a base profile `b`, extend it to `insert j T`:
    reset `j` to `b j`, add `j`'s own payoff difference, and commute `j`'s move past each earlier
    player's with one square. -/
theorem fourCycle_potential_on (u : ι → ((j : ι) → S j) → ℝ) (b : (j : ι) → S j)
    (h : FourCycle u) (T : Finset ι) : ∃ P, IsPotentialOn u T P := by
  classical
  refine Finset.induction_on T ?_ ?_
  · exact ⟨fun _ => 0, fun i hi => by simp at hi⟩
  · intro j T hjT ih
    obtain ⟨P, hP⟩ := ih
    refine ⟨fun s => P (update s j (b j)) + (u j s - u j (update s j (b j))), ?_⟩
    intro i hi s x
    by_cases hij : i = j
    · subst hij
      simp only [update_idem]
      ring
    · have hiT : i ∈ T := (Finset.mem_insert.mp hi).resolve_left hij
      have I1 : update (update s i x) j (b j) = update (update s j (b j)) i x :=
        update_comm hij x (b j) s
      have I2 : update (update s j (b j)) j (s j) = s := update_update_same_self s j (b j)
      have I3 : update (update (update s j (b j)) i x) j (s j) = update s i x := by
        rw [update_comm hij, update_idem, update_eq_self]
      have hsq := h i j hij (update s j (b j)) x (s j)
      rw [I2, I3] at hsq
      have hPi := hP i hiT (update s j (b j)) x
      show u i (update s i x) - u i s
        = (P (update (update s i x) j (b j)) + (u j (update s i x) - u j (update (update s i x) j (b j))))
          - (P (update s j (b j)) + (u j s - u j (update s j (b j))))
      rw [I1]
      linarith

/-- **A game admits a free-action functional iff its payoff changes are path-independent around
    every square** — for any number of players. -/
theorem free_action_iff_four_cycle [Fintype ι] [∀ i, Nonempty (S i)]
    {u : ι → ((j : ι) → S j) → ℝ} : HasFreeAction u ↔ FourCycle u := by
  constructor
  · intro hF
    obtain ⟨P, hP⟩ := hasFreeAction_iff_exists_potential.mp hF
    exact potential_fourCycle hP
  · intro h
    obtain ⟨b⟩ : Nonempty ((j : ι) → S j) := ⟨fun j => Classical.arbitrary (S j)⟩
    obtain ⟨P, hP⟩ := fourCycle_potential_on u b h Finset.univ
    exact hasFreeAction_iff_exists_potential.mpr ⟨P, fun i s x => hP i (Finset.mem_univ i) s x⟩

-- ==========================================
-- Equilibria, closures, welfare
-- ==========================================

/-- A Nash equilibrium: no player gains by a unilateral move. -/
def IsNash (u : ι → ((j : ι) → S j) → ℝ) (s : (j : ι) → S j) : Prop :=
  ∀ (i : ι) (x : S i), u i (update s i x) ≤ u i s

/-- A ZFA closure of a free-action functional: no unilateral move lowers it. -/
def IsClosure (F : ((j : ι) → S j) → ℝ) (s : (j : ι) → S j) : Prop :=
  ∀ (i : ι) (x : S i), F s ≤ F (update s i x)

/-- **Nash equilibrium = ZFA closure**, `n` players. -/
theorem nash_iff_closure {u : ι → ((j : ι) → S j) → ℝ} {F : ((j : ι) → S j) → ℝ}
    (hF : ∀ (i : ι) (s : (j : ι) → S j) (x : S i),
      u i (update s i x) - u i s = F s - F (update s i x))
    (s : (j : ι) → S j) : IsNash u s ↔ IsClosure F s := by
  constructor
  · intro hN i x
    have := hF i s x
    have := hN i x
    linarith
  · intro hC i x
    have := hF i s x
    have := hC i x
    linarith

/-- **Every finite `n`-player potential game has a pure Nash equilibrium.** -/
theorem exists_nash_of_potential [Fintype ι] [∀ i, Fintype (S i)] [∀ i, Nonempty (S i)]
    {u : ι → ((j : ι) → S j) → ℝ} {P : ((j : ι) → S j) → ℝ} (hP : IsPotential u P) :
    ∃ s, IsNash u s := by
  classical
  obtain ⟨s, -, hmax⟩ :=
    Finset.exists_max_image (Finset.univ : Finset ((j : ι) → S j)) P Finset.univ_nonempty
  refine ⟨s, fun i x => ?_⟩
  have h1 := hP i s x
  have hm : P (update s i x) ≤ P s := hmax _ (Finset.mem_univ _)
  linarith

/-- **A shared payoff is a potential game** with itself as potential. -/
theorem common_interest_potential (W : ((j : ι) → S j) → ℝ) : IsPotential (fun _ => W) W :=
  fun _ _ _ => rfl

/-- **Make the closure joint, at `n`:** paying every player the total welfare `Σ j, u j` is a
    common-interest game, hence a potential game whose potential is welfare — least free action is
    welfare maximisation. -/
theorem welfare_game_potential [Fintype ι] (u : ι → ((j : ι) → S j) → ℝ) :
    IsPotential (fun _ s => ∑ j, u j s) (fun s => ∑ j, u j s) :=
  common_interest_potential _

/-- **Status.** The free-action characterization holds at any arity (squares suffice), Nash
    equilibria are closures, every finite potential game has one, and welfare is a potential once
    the closure is joint. -/
theorem n_player_summary : True := trivial

end QLF.NPlayerPotential
