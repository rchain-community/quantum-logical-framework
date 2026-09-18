import Mathlib.Data.Nat.Choose.Central
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Tactic.Ring
import QLF_TwistAlphabet
import QLF_KraftMeasure
import QLF_PolyaTransience
-- Narrow imports (see QLF_PhaseRule): this module never needs `import Mathlib`.

set_option linter.unusedVariables false

/-!
# QLF_ProductWalk — the twist-history ↔ `walkCount` bridge

[`Closure_Walk.md`](../Closure_Walk.md) §5, [issue #157](https://github.com/rchain-community/quantum-logical-framework/issues/157):
`card {ts : List Twist // ts.length = L ∧ countBalanced ts} = walkCount L`, closing the gap left by
`QLF_PolyaTransience`. Proved via the diagonal-coordinate encoding the plane count `w₂` is named
after: `Twist ≃ Fin 4 × Bool` (axis, sign), splitting into two planes `Plane1 = {up,down,left,right}`
and `Plane2 = {slash,backslash,plus,minus}`; within a plane, a further diagonal bijection
`Plane1 ≃ Bool × Bool` turns "both axes balanced" into "both coordinate bits balanced" — independent
`±1` walks — giving `C(k,k/2)²` directly. No axioms.
-/

namespace QLF.ProductWalk

open Finset QLF

-- ==========================================
-- Step 0: balanced `Bool` words, C(n,p) then C(2n,n)
-- ==========================================

/-- Every length-`n` `Bool` word with exactly `p` `true`s: the ordinary binomial count. -/
theorem card_filter_count_true (n p : ℕ) :
    ((words Bool n).filter (fun l => decide (l.count true = p))).card = n.choose p := by
  induction n generalizing p with
  | zero =>
      rcases p with _ | p
      · decide
      · simp [words]
  | succ n ih =>
      have hstep : (words Bool (n + 1)).filter (fun l => decide (l.count true = p)) =
          (univ : Finset Bool).biUnion (fun a =>
            ((words Bool n).image (fun w => a :: w)).filter
              (fun l => decide (l.count true = p))) := by
        rw [words, Finset.filter_biUnion]
      rw [hstep]
      have hinj : ∀ a : Bool, Function.Injective (fun w : List Bool => a :: w) := by
        intro a w₁ w₂ h; simpa using h
      have hdisj : ∀ a ∈ (univ : Finset Bool), ∀ b ∈ (univ : Finset Bool), a ≠ b →
          Disjoint (((words Bool n).image (fun w => a :: w)).filter
                      (fun l => decide (l.count true = p)))
                   (((words Bool n).image (fun w => b :: w)).filter
                      (fun l => decide (l.count true = p))) := by
        intro a _ b _ hab
        apply Finset.disjoint_filter_filter
        refine Finset.disjoint_left.mpr ?_
        intro w hwa hwb
        rw [Finset.mem_image] at hwa hwb
        obtain ⟨u, -, rfl⟩ := hwa
        obtain ⟨v, -, hv⟩ := hwb
        injection hv with hba _
        exact hab hba.symm
      rw [Finset.card_biUnion hdisj]
      have heach_true : (((words Bool n).image (fun w => true :: w)).filter
          (fun l => decide (l.count true = p))).card =
          (if h : 0 < p then ((words Bool n).filter
            (fun w => decide (w.count true = p - 1))).card else 0) := by
        rw [Finset.filter_image, Finset.card_image_of_injective _ (hinj true)]
        split_ifs with hp
        · congr 1
          apply Finset.filter_congr
          intro w _
          have hct : (true :: w).count true = w.count true + 1 := by simp [List.count_cons]
          simp only [hct, decide_eq_true_eq]
          omega
        · apply Finset.card_eq_zero.mpr
          apply Finset.filter_eq_empty_iff.mpr
          intro w _
          have hct : (true :: w).count true = w.count true + 1 := by simp [List.count_cons]
          simp only [hct, decide_eq_true_eq]
          omega
      have heach_false : (((words Bool n).image (fun w => false :: w)).filter
          (fun l => decide (l.count true = p))).card =
          ((words Bool n).filter (fun w => decide (w.count true = p))).card := by
        rw [Finset.filter_image, Finset.card_image_of_injective _ (hinj false)]
        congr 1
      rw [Fintype.sum_bool (fun a => (((words Bool n).image (fun w => a :: w)).filter
          (fun l => decide (l.count true = p))).card)]
      rw [heach_true, heach_false]
      rcases p with _ | p
      · rw [dif_neg (Nat.lt_irrefl 0)]
        rw [ih 0, Nat.choose_zero_right, Nat.choose_zero_right]
      · rw [dif_pos (Nat.succ_pos p), Nat.succ_sub_one, ih p, ih (p + 1)]
        exact (Nat.choose_succ_succ n p).symm

/-- The count of length-`2n` `Bool` words with `n` `true`s and `n` `false`s (balanced) is the
    central binomial coefficient. -/
theorem card_balancedBool_even (n : ℕ) :
    ((words Bool (2 * n)).filter (fun l => decide (l.count true = l.count false))).card =
      Nat.centralBinom n := by
  have hlen : ∀ l ∈ words Bool (2 * n), l.count true = 2 * n - l.count false ∧
      l.count false ≤ 2 * n := by
    intro l hl
    have hl' := (mem_words (2 * n) l).mp hl
    have hc : l.count true + l.count false = l.length :=
      List.count_true_add_count_false l
    omega
  have hcongr : (words Bool (2 * n)).filter (fun l => decide (l.count true = l.count false)) =
      (words Bool (2 * n)).filter (fun l => decide (l.count true = n)) := by
    apply Finset.filter_congr
    intro l hl
    obtain ⟨heq, hle⟩ := hlen l hl
    simp only [decide_eq_true_eq]
    omega
  rw [hcongr, card_filter_count_true]
  unfold Nat.centralBinom
  rfl
