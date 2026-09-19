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

open Finset QLF QLF.PolyaTransience

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

/-- No balanced `Bool` word of odd length: equal counts would force an even total. -/
theorem card_balancedBool_odd (n : ℕ) (hn : ¬ Even n) :
    ((words Bool n).filter (fun l => decide (l.count true = l.count false))).card = 0 := by
  apply Finset.card_eq_zero.mpr
  apply Finset.filter_eq_empty_iff.mpr
  intro l hl
  have hl' := (mem_words n l).mp hl
  have hc : l.count true + l.count false = l.length := List.count_true_add_count_false l
  simp only [decide_eq_true_eq]
  intro heq
  exact hn ⟨l.count false, by omega⟩

-- ==========================================
-- Step 1: the plane, `Plane1 ≃ Bool × Bool`, giving `w₂` directly
-- ==========================================

/-- One plane's four twists: `up`/`down` on one axis, `left`/`right` on the other. -/
inductive Plane1 where
  | up | down | left | right
  deriving BEq, DecidableEq

instance : Fintype Plane1 :=
  ⟨{Plane1.up, Plane1.down, Plane1.left, Plane1.right}, by intro x; cases x <;> decide⟩

/-- Both of the plane's axes are balanced. -/
def balanced1 (l : List Plane1) : Prop :=
  l.count Plane1.up = l.count Plane1.down ∧ l.count Plane1.left = l.count Plane1.right

instance : DecidablePred balanced1 := fun l => by unfold balanced1; infer_instance

/-- The diagonal encoding: `up ↦ (T,T)`, `down ↦ (F,F)`, `left ↦ (T,F)`, `right ↦ (F,T)`. Its two
    coordinates are the plane's two *independent* `±1` walks. -/
def enc1 : Plane1 → Bool × Bool
  | .up => (true, true)
  | .down => (false, false)
  | .left => (true, false)
  | .right => (false, true)

def dec1 : Bool × Bool → Plane1
  | (true, true) => .up
  | (false, false) => .down
  | (true, false) => .left
  | (false, true) => .right

theorem dec1_enc1 (p : Plane1) : dec1 (enc1 p) = p := by cases p <;> rfl

theorem enc1_dec1 (q : Bool × Bool) : enc1 (dec1 q) = q := by
  obtain ⟨a, b⟩ := q; cases a <;> cases b <;> rfl

theorem enc1_injective : Function.Injective enc1 := by
  intro a b h
  have h' := congrArg dec1 h
  rwa [dec1_enc1, dec1_enc1] at h'

theorem count_fst_enc1_true (l : List Plane1) :
    (l.map (Prod.fst ∘ enc1)).count true = l.count Plane1.up + l.count Plane1.left := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, Function.comp_apply, ih]
      cases a <;> simp (config := { decide := true }) [enc1] <;> omega

theorem count_fst_enc1_false (l : List Plane1) :
    (l.map (Prod.fst ∘ enc1)).count false = l.count Plane1.down + l.count Plane1.right := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, Function.comp_apply, ih]
      cases a <;> simp (config := { decide := true }) [enc1] <;> omega

theorem count_snd_enc1_true (l : List Plane1) :
    (l.map (Prod.snd ∘ enc1)).count true = l.count Plane1.up + l.count Plane1.right := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, Function.comp_apply, ih]
      cases a <;> simp (config := { decide := true }) [enc1] <;> omega

theorem count_snd_enc1_false (l : List Plane1) :
    (l.map (Prod.snd ∘ enc1)).count false = l.count Plane1.down + l.count Plane1.left := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, Function.comp_apply, ih]
      cases a <;> simp (config := { decide := true }) [enc1] <;> omega

/-- `balanced1` is exactly both coordinate projections being balanced. -/
theorem balanced1_iff (l : List Plane1) :
    balanced1 l ↔ (l.map (Prod.fst ∘ enc1)).count true = (l.map (Prod.fst ∘ enc1)).count false ∧
                   (l.map (Prod.snd ∘ enc1)).count true = (l.map (Prod.snd ∘ enc1)).count false := by
  rw [count_fst_enc1_true, count_fst_enc1_false, count_snd_enc1_true, count_snd_enc1_false]
  unfold balanced1
  omega

/-- Recover a `Plane1` list from its two coordinate projections. -/
def zipDec1 (l1 l2 : List Bool) : List Plane1 := (l1.zip l2).map dec1

theorem enc1_comp_dec1 : enc1 ∘ dec1 = id := by funext q; exact enc1_dec1 q

theorem map_enc1_zipDec1 (l1 l2 : List Bool) :
    (zipDec1 l1 l2).map enc1 = l1.zip l2 := by
  unfold zipDec1
  rw [List.map_map, enc1_comp_dec1, List.map_id]

/-- `ψ` is a left inverse of `φ`: zipping a `Plane1` list's own two coordinate projections
    recovers it exactly. -/
theorem zipDec1_phi (l : List Plane1) :
    zipDec1 (l.map (Prod.fst ∘ enc1)) (l.map (Prod.snd ∘ enc1)) = l := by
  unfold zipDec1
  induction l with
  | nil => simp
  | cons a t ih => simp [List.zip_cons_cons, ih, dec1_enc1]

/-- `φ` is a right inverse of `ψ` on matching-length pairs. -/
theorem phi_zipDec1 (l1 l2 : List Bool) (h : l1.length = l2.length) :
    (zipDec1 l1 l2).map (Prod.fst ∘ enc1) = l1 ∧ (zipDec1 l1 l2).map (Prod.snd ∘ enc1) = l2 := by
  have key := map_enc1_zipDec1 l1 l2
  refine ⟨?_, ?_⟩
  · rw [← List.map_map, key]
    exact List.map_fst_zip (le_of_eq h)
  · rw [← List.map_map, key]
    exact List.map_snd_zip (le_of_eq h.symm)

/-- **The plane's balanced count is exactly `w₂`.** The diagonal bijection turns "both axes
    balanced" into a pair of independent balanced `Bool` walks. -/
theorem card_balanced1 (k : ℕ) :
    ((words Plane1 k).filter (fun l => decide (balanced1 l))).card = w₂ k := by
  set B : Finset (List Bool) :=
    (words Bool k).filter (fun l => decide (l.count true = l.count false)) with hB
  have hcard : ((words Plane1 k).filter (fun l => decide (balanced1 l))).card = (B ×ˢ B).card := by
    apply Finset.card_bij' (fun l _ => (l.map (Prod.fst ∘ enc1), l.map (Prod.snd ∘ enc1)))
      (fun p _ => zipDec1 p.1 p.2)
    · intro l hl
      simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hl
      obtain ⟨hlen, hbal⟩ := hl
      obtain ⟨hb1, hb2⟩ := (balanced1_iff l).mp hbal
      simp only [hB, Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq]
      exact ⟨⟨by simpa using hlen, hb1⟩, by simpa using hlen, hb2⟩
    · intro p hp
      obtain ⟨l1, l2⟩ := p
      simp only [hB, Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hp
      obtain ⟨⟨hl1len, hl1bal⟩, hl2len, hl2bal⟩ := hp
      have hlen : l1.length = l2.length := by rw [hl1len, hl2len]
      simp only [Finset.mem_filter, mem_words, decide_eq_true_eq]
      refine ⟨?_, ?_⟩
      · show (zipDec1 l1 l2).length = k
        unfold zipDec1
        rw [List.length_map, List.length_zip, hl1len, hl2len, min_self]
      · rw [balanced1_iff, (phi_zipDec1 l1 l2 hlen).1, (phi_zipDec1 l1 l2 hlen).2]
        exact ⟨hl1bal, hl2bal⟩
    · intro l _
      exact zipDec1_phi l
    · intro p hp
      obtain ⟨l1, l2⟩ := p
      simp only [hB, Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hp
      obtain ⟨⟨hl1len, _⟩, hl2len, _⟩ := hp
      have hlen : l1.length = l2.length := by rw [hl1len, hl2len]
      obtain ⟨e1, e2⟩ := phi_zipDec1 l1 l2 hlen
      simp [e1, e2]
  rw [hcard, Finset.card_product]
  unfold w₂
  split_ifs with hk
  · have hk2 : 2 * (k / 2) = k := by omega
    have hBcard : B.card = Nat.centralBinom (k / 2) := by
      have hthis := card_balancedBool_even (k / 2)
      rw [hk2] at hthis
      rw [hB]; exact hthis
    rw [hBcard]; ring
  · have hk' : ¬ Even k := by rw [Nat.even_iff]; omega
    have hBcard : B.card = 0 := by rw [hB]; exact card_balancedBool_odd k hk'
    rw [hBcard]
