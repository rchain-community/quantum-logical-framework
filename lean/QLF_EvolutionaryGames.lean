import QLF_PotentialGames

/-!
# QLF_EvolutionaryGames — descent terminates, ways are basins, and the pairing is an ESS

Companion to [`QLF_PotentialGames`](QLF_PotentialGames.lean) (target 1 of the five game-theory
results named on quantum-os #209: *a game has a free-action functional iff it is a potential
game*). This module delivers the other four, each scoped to what is provable as finite
combinatorics — the analytic limits are cited, not reproven.

## Target 3 — free-action descent terminates on potential games

A **`Descent`** is a revision dynamic `step` with a potential `P` that strictly increases whenever
the state moves. On a finite state space every orbit reaches a fixed point
(**`Descent.eventually_fixed`**): among the finitely many orbit points one maximises `P`, and it
cannot move. For a potential game the best-response dynamic is such a descent
(**`improve_increases_potential`**: a unilateral improvement raises `P`), so closure search cannot
cycle — and, as a corollary that needs no dynamics at all, **every finite two-player potential game
has a pure Nash equilibrium** (**`exists_nash_of_potential`**): the potential's maximiser is a
closure. This is the class on which "least free action" is a well-founded search, the
`QLF_Universality` / `QLF_PvsNP` framing made game-theoretic: an equilibrium is `O(n)` to verify
(regret `= 0`) and reached by descent exactly when a potential exists.

## Target 2 — the ways to a closure are its basin

With every orbit ending somewhere, **`orbitEnd`** names where, and the **ways** to a closure `c`
are the states whose orbit ends at `c` — its basin. **`basins_partition`**: the basins of the
closures partition the state space, so under the uniform prior the **frequency of a closure is its
multiplicity** `ways c / |S|` (**`sum_frequency`**), and a state that is not a closure has no ways
at all (**`ways_eq_zero_of_not_fixed`**). This is "what happens in the most ways happens first"
stated for dynamics: measured to two decimals in `evolutionary_census.py --optimize` (the Stag
share of cold runs equals `1 − p*`, Young's basin threshold). The stochastic-stability theorem
proper — that with vanishing mutation the selected closure is the one reached by the most
mutation paths (Kandori–Mailath–Rob 1993; Young 1993) — is the `μ → 0` limit of this count and is
cited.

## Target 4 — symmetry breaking has an exact threshold

In the emergent first-closure race (`evolutionary_census.py --race`) a strand earns `a` against a
copy of itself, `1` against its conjugate (joint closure at depth 0), and `b` against an
orthogonal strand. A population sitting `½ : ½` on one conjugate pair earns `(1 + a)/2` per
encounter; an orthogonal invader earns `b`; the uniform population earns `(1 + a + 4b)/6`.
**`pair_uninvadable_iff`** and **`pair_beats_uniform_iff`**: both comparisons reduce to the same
inequality, **`1 + a > 2b`** — the population must pick a basis exactly when conjugate bonding
beats twice the orthogonal payoff. Measured `a ≈ 0.148, b ≈ 0.247`: `1.148 > 0.494`
(**`measured_threshold_holds`**), which is why every replicator run collapsed onto a single axis.

## Target 5 — the Hermitian pairing is an evolutionarily stable 1 : 1

Within a conjugate pair the game is symmetric anti-coordination: `1` against the partner, `a < 1`
against a copy. **`fisher_half_ess`**: the `½ : ½` mixture is an ESS in Maynard Smith's sense —
against any other mixture `p` it earns strictly more than `p` earns against itself, by exactly
`2(1 − a)(p − ½)²`. Fisher's sex-ratio argument, from closure counting: complementary strands bind
1 : 1 (`SEX.md`). The two inputs are `u(conjugate) = 1`, which is `conjugate_pair_closes`
(`ER_EPR_QLF`), and `a < 1`; the sharper lattice fact that an orthogonal partner beats a copy
(`b > a`, so like-with-like is the *worst* partner) is measured, not proven — a first-passage
inequality on the `ℤ³` walk that remains open.

No axioms.
-/

namespace QLF.EvolutionaryGames

open QLF.PotentialGames

-- ==========================================
-- Target 3: descent terminates
-- ==========================================

/-- A revision dynamic whose potential strictly increases whenever the state moves. -/
structure Descent (S : Type*) where
  step : S → S
  P : S → ℝ
  strict : ∀ s, step s ≠ s → P s < P (step s)

variable {S : Type*}

/-- One step never lowers the potential. -/
theorem Descent.step_le (D : Descent S) (s : S) : D.P s ≤ D.P (D.step s) := by
  by_cases h : D.step s = s
  · rw [h]
  · exact le_of_lt (D.strict s h)

/-- The potential is monotone along orbits. -/
theorem Descent.iterate_le (D : Descent S) (s : S) (n : ℕ) : D.P s ≤ D.P (D.step^[n] s) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply']
    exact le_trans ih (D.step_le _)

/-- **Every orbit reaches a fixed point** on a finite state space: the orbit point maximising
    the potential cannot move. -/
theorem Descent.eventually_fixed [Fintype S] (D : Descent S) (s : S) :
    ∃ n : ℕ, D.step (D.step^[n] s) = D.step^[n] s := by
  classical
  let orbit : Finset S := Finset.univ.filter (fun x => ∃ n : ℕ, D.step^[n] s = x)
  have hne : orbit.Nonempty := by
    refine ⟨s, ?_⟩
    simp only [orbit, Finset.mem_filter, Finset.mem_univ, true_and]
    exact ⟨0, rfl⟩
  obtain ⟨x, hx, hmax⟩ := Finset.exists_max_image orbit D.P hne
  have hx' : ∃ n : ℕ, D.step^[n] s = x := by
    simpa [orbit] using hx
  obtain ⟨n, rfl⟩ := hx'
  refine ⟨n, ?_⟩
  by_contra hmove
  have hlt := D.strict _ hmove
  have hmem : D.step (D.step^[n] s) ∈ orbit := by
    simp only [orbit, Finset.mem_filter, Finset.mem_univ, true_and]
    exact ⟨n + 1, Function.iterate_succ_apply' D.step n s⟩
  have := hmax _ hmem
  linarith

/-- In a potential game a unilateral improvement raises the potential — best response is a
    descent. -/
theorem improve_increases_potential {S₁ S₂ : Type*} {u₁ u₂ P : S₁ → S₂ → ℝ}
    (hP : IsPotential u₁ u₂ P) {a a' : S₁} {b : S₂} (h : u₁ a b < u₁ a' b) :
    P a b < P a' b := by
  have := hP.1 a a' b
  linarith

/-- **Every finite two-player potential game has a pure Nash equilibrium**: the potential's
    maximiser is a closure. -/
theorem exists_nash_of_potential {S₁ S₂ : Type*} [Fintype S₁] [Fintype S₂]
    [Nonempty S₁] [Nonempty S₂] {u₁ u₂ P : S₁ → S₂ → ℝ} (hP : IsPotential u₁ u₂ P) :
    ∃ a b, IsNash u₁ u₂ a b := by
  obtain ⟨⟨a, b⟩, -, hmax⟩ :=
    Finset.exists_max_image (Finset.univ : Finset (S₁ × S₂)) (fun p => P p.1 p.2)
      Finset.univ_nonempty
  refine ⟨a, b, fun a' => ?_, fun b' => ?_⟩
  · have h1 := hP.1 a a' b
    have hm : P a' b ≤ P a b := hmax (a', b) (Finset.mem_univ _)
    linarith
  · have h2 := hP.2 a b b'
    have hm : P a b' ≤ P a b := hmax (a, b') (Finset.mem_univ _)
    linarith

-- ==========================================
-- Target 2: ways are basins
-- ==========================================

/-- Where an orbit ends — a fixed point, by `eventually_fixed`. -/
noncomputable def Descent.orbitEnd [Fintype S] (D : Descent S) (s : S) : S :=
  D.step^[Classical.choose (D.eventually_fixed s)] s

theorem Descent.orbitEnd_fixed [Fintype S] (D : Descent S) (s : S) :
    D.step (D.orbitEnd s) = D.orbitEnd s :=
  Classical.choose_spec (D.eventually_fixed s)

/-- **The ways to a closure**: the number of states whose orbit ends there — its basin. -/
noncomputable def Descent.ways [Fintype S] [DecidableEq S] (D : Descent S) (c : S) : ℕ :=
  (Finset.univ.filter (fun s => D.orbitEnd s = c)).card

/-- **The basins partition the state space.** -/
theorem Descent.basins_partition [Fintype S] [DecidableEq S] (D : Descent S) :
    ∑ c, D.ways c = Fintype.card S := by
  unfold Descent.ways
  rw [← Finset.card_univ]
  exact (Finset.card_eq_sum_card_fiberwise (fun s _ => Finset.mem_univ (D.orbitEnd s))).symm

/-- A state that is not a closure has no ways: nothing ends there. -/
theorem Descent.ways_eq_zero_of_not_fixed [Fintype S] [DecidableEq S] (D : Descent S) (c : S)
    (hc : D.step c ≠ c) : D.ways c = 0 := by
  unfold Descent.ways
  rw [Finset.card_eq_zero, Finset.filter_eq_empty_iff]
  intro s _ h
  have hfix := D.orbitEnd_fixed s
  rw [h] at hfix
  exact hc hfix

/-- The frequency of a closure under the uniform prior: its multiplicity over the state count. -/
noncomputable def Descent.frequency [Fintype S] [DecidableEq S] (D : Descent S) (c : S) : ℝ :=
  (D.ways c : ℝ) / Fintype.card S

/-- **Frequency is multiplicity**: the closure frequencies sum to one. -/
theorem Descent.sum_frequency [Fintype S] [DecidableEq S] [Nonempty S] (D : Descent S) :
    ∑ c, D.frequency c = 1 := by
  unfold Descent.frequency
  rw [← Finset.sum_div]
  have h : (∑ c, (D.ways c : ℝ)) = Fintype.card S := by
    exact_mod_cast D.basins_partition
  rw [h]
  exact div_self (by exact_mod_cast Fintype.card_ne_zero)

-- ==========================================
-- Target 4: the symmetry-breaking threshold
-- ==========================================

/-- A resident of a `½ : ½` conjugate-pair population: `a` against a copy, `1` against the
    partner. -/
noncomputable def residentPayoff (a : ℝ) : ℝ := (a + 1) / 2

/-- An orthogonal invader earns `b` against both members of the pair. -/
def invaderPayoff (b : ℝ) : ℝ := b

/-- The mean payoff in the uniform six-strand population: `1` against the conjugate, `a` against
    the copy, `b` against the four orthogonal strands. -/
noncomputable def uniformPayoff (a b : ℝ) : ℝ := (1 + a + 4 * b) / 6

/-- **The pair state repels an orthogonal invader iff `1 + a > 2b`.** -/
theorem pair_uninvadable_iff (a b : ℝ) : invaderPayoff b < residentPayoff a ↔ 2 * b < 1 + a := by
  unfold invaderPayoff residentPayoff
  constructor <;> intro h <;> linarith

/-- **The pair state out-earns the uniform population iff `1 + a > 2b`** — the same threshold. -/
theorem pair_beats_uniform_iff (a b : ℝ) : uniformPayoff a b < residentPayoff a ↔ 2 * b < 1 + a := by
  unfold uniformPayoff residentPayoff
  constructor <;> intro h <;> linarith

/-- The measured race payoffs (`a ≈ 0.148`, `b ≈ 0.247`) are past the threshold: the population
    must pick a basis. -/
theorem measured_threshold_holds : (2 * 0.247 : ℝ) < 1 + 0.148 := by norm_num

-- ==========================================
-- Target 5: the 1 : 1 pairing is an ESS
-- ==========================================

/-- Expected payoff of a mixture `p` (share on one strand) against a mixture `q`, in the
    symmetric anti-coordination game with `a` against a copy and `1` against the conjugate. -/
noncomputable def E (a p q : ℝ) : ℝ :=
  p * q * a + p * (1 - q) + (1 - p) * q + (1 - p) * (1 - q) * a

/-- Every mixture earns the same against `½`: the mixed equilibrium. -/
theorem half_is_equilibrium (a p : ℝ) : E a p (1 / 2) = E a (1 / 2) (1 / 2) := by
  unfold E
  ring

/-- **Fisher's `1 : 1` is an ESS** whenever the conjugate beats a copy (`a < 1`): against any other
    mixture `p`, the `½` mixture earns strictly more than `p` earns against itself — by exactly
    `2(1 − a)(p − ½)²`. -/
theorem fisher_half_ess (a p : ℝ) (ha : a < 1) (hp : p ≠ 1 / 2) :
    E a p p < E a (1 / 2) p := by
  have key : E a (1 / 2) p - E a p p = 2 * (1 - a) * ((p - 1 / 2) * (p - 1 / 2)) := by
    unfold E
    ring
  have h1 : 0 < 1 - a := by linarith
  have h2 : 0 < (p - 1 / 2) * (p - 1 / 2) := mul_self_pos.mpr (sub_ne_zero.mpr hp)
  have h3 : 0 < 2 * (1 - a) * ((p - 1 / 2) * (p - 1 / 2)) :=
    mul_pos (mul_pos two_pos h1) h2
  linarith

/-- **Status.** Descent terminates on potential games and every finite potential game has a pure
    equilibrium; the ways to a closure are its basin and closure frequency is multiplicity; the
    population picks a basis iff `1 + a > 2b`; and the `½ : ½` conjugate pairing is an ESS. -/
theorem evolutionary_games_summary : True := trivial

end QLF.EvolutionaryGames
