import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
-- Narrow imports (see QLF_PhaseRule): this module never needs `import Mathlib`.

set_option linter.unusedVariables false

/-!
# QLF_StationaryAction — **stationary action is ZFA**: the realized history is the most-ways one

Hamilton's principle `δS = 0` is postulated in every classical field theory. Hilbert's 1915
derivation of general relativity from `S = ∫ R √−g` is that postulate applied to curvature. This
module proves the substrate reason it holds: *what happens in the most ways happens first*
(`Philosophy.md` §3a). The realized history is the mode of the census multiplicity `W`. Because every
twist has its conjugate at equal weight, the mode sits at balance, and there the first variation of
`W` vanishes. With `S ↔ −ħ log W` that is `δS = 0`.

The object is the one-axis census: a `2n`-step `±` history with `k` up-steps, `W(k) = C(2n, k)`,
with balance (ZFA closure) at `k = n`.

* **`ways_symmetric`** — `W(n + d) = W(n − d)`: conjugate symmetry of the multiplicity about balance.
* **`first_variation_zero`** / **`central_difference_zero`** — the discrete first variation at
  balance is `0`: **stationarity**.
* **`balance_is_mode`** and **`balance_strict_max`** — balance is the maximum, and a strict one
  (second variation negative): stationarity of the *realized* kind, a maximum of ways.
* **`straight_path_most_ways`** — among closures of `2n` steps (an `n`-step leg out and an `n`-step
  leg back), the number passing each midpoint height is `C(n,j)²`, maximised at the straight path
  `j = n/2`. The classical (geodesic) trajectory is the path the most ways pass through.

**Kill condition, and why it is not bookkeeping (method rule 4).** The result depends on the
conjugate pairing. If conjugates had unequal weight, the claim would fail:
**`biased_first_variation`** gives weight `2` to each up-step and gets `W'(n+1) = 4·W'(n−1)`, so the
first variation at balance is non-zero and the mode moves off balance (`biased_mode_off_balance`).
Stationarity at the closure is therefore a consequence of ZFA's conjugate symmetry. It is not an
identity that holds for every weighting.

**Scope.** This proves *why the realized history is stationary*. *Which functional* is stationary —
Hilbert's `∫R` — is supplied by the causal-set (Benincasa–Dowker) action on QLF's causal order,
`QLF_CausalContinuum` (`benincasa_dowker_limit`, cited, unchanged). The open step is to identify that
BD count with the multiplicity whose mode is taken. See `Stationary_Action.md`. No axioms.
-/

namespace QLF.StationaryAction

/-- The census multiplicity: `2n`-step `±` histories with `k` up-steps. Balance is `k = n`. -/
def ways (n k : ℕ) : ℕ := (2 * n).choose k

/-- **Conjugate symmetry of the multiplicity about balance.** -/
theorem ways_symmetric (n d : ℕ) (hd : d ≤ n) : ways n (n + d) = ways n (n - d) := by
  unfold ways
  have h1 : n + d ≤ 2 * n := by omega
  have h2 : 2 * n - (n + d) = n - d := by omega
  rw [← Nat.choose_symm h1, h2]

/-- **Stationarity at balance, every order of displacement:** the central difference of `W` about
    the closure vanishes. -/
theorem central_difference_zero (n d : ℕ) (hd : d ≤ n) :
    (ways n (n + d) : ℤ) - (ways n (n - d) : ℤ) = 0 := by
  rw [ways_symmetric n d hd, sub_self]

/-- **The first variation vanishes at the closure** — the discrete `δ log W = 0`. -/
theorem first_variation_zero (n : ℕ) (hn : 1 ≤ n) :
    (ways n (n + 1) : ℤ) - (ways n (n - 1) : ℤ) = 0 :=
  central_difference_zero n 1 hn

/-- **Balance is the mode:** no displacement is realized in more ways than the closure. -/
theorem balance_is_mode (n k : ℕ) : ways n k ≤ ways n n := by
  unfold ways
  have h := Nat.choose_le_middle k (2 * n)
  have h1 : 2 * n / 2 = n := by omega
  rwa [h1] at h

/-- **Strict maximum (negative second variation):** one step off balance is realized in strictly
    fewer ways. -/
theorem balance_strict_max (n : ℕ) : ways n (n + 1) < ways n n := by
  unfold ways
  have h := Nat.choose_succ_right_eq (2 * n) n
  have h2 : 2 * n - n = n := by omega
  rw [h2] at h
  have hpos : 0 < (2 * n).choose n := Nat.choose_pos (by omega)
  by_contra hc
  have hc' : (2 * n).choose n ≤ (2 * n).choose (n + 1) := Nat.le_of_not_lt hc
  have h3 : (2 * n).choose n * (n + 1) ≤ (2 * n).choose (n + 1) * (n + 1) :=
    Nat.mul_le_mul hc' (le_refl (n + 1))
  rw [h] at h3
  nlinarith

/-- The same on the other side, by conjugate symmetry. -/
theorem balance_strict_max' (n : ℕ) (hn : 1 ≤ n) : ways n (n - 1) < ways n n := by
  rw [← ways_symmetric n 1 hn]
  exact balance_strict_max n

/-- Closures of `2n` steps split as an `n`-step leg out and an `n`-step leg back. Those whose first
    leg has `j` up-steps number `C(n,j)·C(n,n−j)`. -/
def throughMidpoint (n j : ℕ) : ℕ := n.choose j * n.choose (n - j)

theorem throughMidpoint_sq (n j : ℕ) (hj : j ≤ n) : throughMidpoint n j = (n.choose j) ^ 2 := by
  unfold throughMidpoint
  rw [Nat.choose_symm hj, pow_two]

/-- **The straight path is the most-ways path** — the discrete geodesic principle. More closures
    pass through the balanced midpoint `j = n/2` than through any other. -/
theorem straight_path_most_ways (n j : ℕ) : throughMidpoint n j ≤ throughMidpoint n (n / 2) := by
  rw [throughMidpoint_sq n (n / 2) (Nat.div_le_self n 2)]
  by_cases hj : j ≤ n
  · rw [throughMidpoint_sq n j hj]
    exact Nat.pow_le_pow_left (Nat.choose_le_middle j n) 2
  · unfold throughMidpoint
    rw [Nat.choose_eq_zero_of_lt (by omega), Nat.zero_mul]
    exact Nat.zero_le _

/-! ## The kill condition: break the conjugate pairing and stationarity at balance fails -/

/-- Multiplicity under a *biased* alphabet: each up-step weighted `2`, its conjugate `1`. -/
def biasedWays (n k : ℕ) : ℕ := 2 ^ k * (2 * n).choose k

/-- **Without conjugate symmetry the first variation at balance is non-zero:**
    `W'(n+1) = 4·W'(n−1)`. -/
theorem biased_first_variation (n : ℕ) (hn : 1 ≤ n) :
    biasedWays n (n + 1) = 4 * biasedWays n (n - 1) := by
  unfold biasedWays
  have hs := ways_symmetric n 1 hn
  unfold ways at hs
  rw [hs]
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  simp only [Nat.add_sub_cancel]
  ring

/-- Concretely (`n = 2`): under bias the mode is *not* the closure. -/
theorem biased_mode_off_balance : biasedWays 2 2 < biasedWays 2 3 := by
  decide

/-- **Stationary action from ZFA — summary.** At the closure the first variation of the
    multiplicity vanishes and the closure is its strict maximum. Break the conjugate pairing and the
    first variation is no longer zero. -/
theorem balance_is_stationary_mode (n : ℕ) (hn : 1 ≤ n) :
    ((ways n (n + 1) : ℤ) - (ways n (n - 1) : ℤ) = 0) ∧
    (∀ k, ways n k ≤ ways n n) ∧
    ways n (n + 1) < ways n n ∧
    biasedWays n (n + 1) ≠ biasedWays n (n - 1) := by
  refine ⟨first_variation_zero n hn, balance_is_mode n, balance_strict_max n, ?_⟩
  rw [biased_first_variation n hn]
  have hpos : 0 < biasedWays n (n - 1) := by
    unfold biasedWays
    exact Nat.mul_pos (Nat.two_pow_pos _) (Nat.choose_pos (by omega))
  omega

end QLF.StationaryAction
