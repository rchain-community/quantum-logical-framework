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

-- ==========================================
-- Step 2: the outer split, `Twist ≃ Plane1 ⊕ Plane2`, giving the `C(L,k)` convolution
-- ==========================================

/-- The other plane's four twists: `slash`/`backslash` on one axis, `plus`/`minus` on the other. -/
inductive Plane2 where
  | slash | backslash | plus | minus
  deriving BEq, DecidableEq

instance : Fintype Plane2 :=
  ⟨{Plane2.slash, Plane2.backslash, Plane2.plus, Plane2.minus}, by intro x; cases x <;> decide⟩

/-- Both of the plane's axes are balanced. -/
def balanced2 (l : List Plane2) : Prop :=
  l.count Plane2.slash = l.count Plane2.backslash ∧ l.count Plane2.plus = l.count Plane2.minus

instance : DecidablePred balanced2 := fun l => by unfold balanced2; infer_instance

/-- Relabel `Plane2` onto `Plane1` (`slash↦up`, `backslash↦down`, `plus↦left`, `minus↦right`) — the
    two planes are structurally identical, so this transports `w₂` without re-deriving the diagonal
    bijection. -/
def relabel21 : Plane2 → Plane1
  | .slash => .up | .backslash => .down | .plus => .left | .minus => .right

def relabel12 : Plane1 → Plane2
  | .up => .slash | .down => .backslash | .left => .plus | .right => .minus

theorem relabel12_21 (p : Plane2) : relabel12 (relabel21 p) = p := by cases p <;> rfl
theorem relabel21_12 (p : Plane1) : relabel21 (relabel12 p) = p := by cases p <;> rfl

theorem count_relabel21_up (l : List Plane2) :
    (l.map relabel21).count Plane1.up = l.count Plane2.slash := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, ih]
      cases a <;> simp (config := { decide := true }) [relabel21]

theorem count_relabel21_down (l : List Plane2) :
    (l.map relabel21).count Plane1.down = l.count Plane2.backslash := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, ih]
      cases a <;> simp (config := { decide := true }) [relabel21]

theorem count_relabel21_left (l : List Plane2) :
    (l.map relabel21).count Plane1.left = l.count Plane2.plus := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, ih]
      cases a <;> simp (config := { decide := true }) [relabel21]

theorem count_relabel21_right (l : List Plane2) :
    (l.map relabel21).count Plane1.right = l.count Plane2.minus := by
  induction l with
  | nil => simp
  | cons a t ih =>
      simp only [List.map_cons, List.count_cons, ih]
      cases a <;> simp (config := { decide := true }) [relabel21]

theorem balanced2_iff (l : List Plane2) : balanced2 l ↔ balanced1 (l.map relabel21) := by
  unfold balanced1 balanced2
  rw [count_relabel21_up, count_relabel21_down, count_relabel21_left, count_relabel21_right]

theorem relabel21_comp_relabel12 : relabel21 ∘ relabel12 = id := by
  funext p; exact relabel21_12 p

theorem relabel12_comp_relabel21 : relabel12 ∘ relabel21 = id := by
  funext p; exact relabel12_21 p

/-- **The other plane's balanced count is also `w₂`**, transported from `card_balanced1` along the
    relabeling. -/
theorem card_balanced2 (k : ℕ) :
    ((words Plane2 k).filter (fun l => decide (balanced2 l))).card = w₂ k := by
  rw [← card_balanced1 k]
  apply Finset.card_bij' (fun l _ => l.map relabel21) (fun l _ => l.map relabel12)
  · intro l hl
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hl
    obtain ⟨hlen, hbal⟩ := hl
    have hbal' : balanced1 (l.map relabel21) := (balanced2_iff l).mp hbal
    simp [Finset.mem_filter, mem_words, hlen, hbal']
  · intro l hl
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hl
    obtain ⟨hlen, hbal⟩ := hl
    have hbal' : balanced2 (l.map relabel12) := by
      rw [balanced2_iff, List.map_map, relabel21_comp_relabel12, List.map_id]
      exact hbal
    simp [Finset.mem_filter, mem_words, hlen, hbal']
  · intro l _
    rw [List.map_map, relabel12_comp_relabel21, List.map_id]
  · intro l _
    rw [List.map_map, relabel21_comp_relabel12, List.map_id]

-- ------------------------------------------
-- The marker, the two subsequences, and `riffle` (their inverse)
-- ------------------------------------------

/-- Which plane a twist belongs to: `true` for the four in `Plane1`. -/
def isPlane1 : Twist → Bool
  | .up | .down | .left | .right => true
  | .slash | .backslash | .plus | .minus => false

def matchP1 : Twist → Option Plane1
  | .up => some .up | .down => some .down | .left => some .left | .right => some .right
  | _ => none

def matchP2 : Twist → Option Plane2
  | .slash => some .slash | .backslash => some .backslash | .plus => some .plus
  | .minus => some .minus | _ => none

/-- The `Plane1` subsequence of a twist history, in order. -/
def plane1Sub (ts : List Twist) : List Plane1 := ts.filterMap matchP1

/-- The `Plane2` subsequence of a twist history, in order. -/
def plane2Sub (ts : List Twist) : List Plane2 := ts.filterMap matchP2

/-- Which of the two planes each position belongs to. -/
def marker (ts : List Twist) : List Bool := ts.map isPlane1

def fromP1 : Plane1 → Twist
  | .up => .up | .down => .down | .left => .left | .right => .right

def fromP2 : Plane2 → Twist
  | .slash => .slash | .backslash => .backslash | .plus => .plus | .minus => .minus

theorem matchP1_fromP1 (p : Plane1) : matchP1 (fromP1 p) = some p := by cases p <;> rfl
theorem matchP2_fromP1 (p : Plane1) : matchP2 (fromP1 p) = none := by cases p <;> rfl
theorem matchP1_fromP2 (p : Plane2) : matchP1 (fromP2 p) = none := by cases p <;> rfl
theorem matchP2_fromP2 (p : Plane2) : matchP2 (fromP2 p) = some p := by cases p <;> rfl

/-- Reassemble a twist history from a marker pattern and its two plane subsequences. -/
def riffle : List Bool → List Plane1 → List Plane2 → List Twist
  | [], _, _ => []
  | true :: _, [], _ => []
  | true :: m, p :: l1, l2 => fromP1 p :: riffle m l1 l2
  | false :: _, _, [] => []
  | false :: m, l1, p :: l2 => fromP2 p :: riffle m l1 l2

/-- `riffle` recovers a twist history from its own marker and subsequences. -/
theorem riffle_correct (ts : List Twist) :
    riffle (marker ts) (plane1Sub ts) (plane2Sub ts) = ts := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      cases t <;>
        simp [marker, plane1Sub, plane2Sub, matchP1, matchP2, isPlane1,
          List.filterMap_cons, riffle, fromP1, fromP2, ih]

/-- `riffle` is well-formed: given a marker and matching-length subsequences, it reconstructs
    exactly the marker and the two subsequences back. -/
theorem riffle_wf (m : List Bool) (l1 : List Plane1) (l2 : List Plane2)
    (h1 : l1.length = m.count true) (h2 : l2.length = m.count false) :
    marker (riffle m l1 l2) = m ∧ plane1Sub (riffle m l1 l2) = l1 ∧
      plane2Sub (riffle m l1 l2) = l2 := by
  induction m generalizing l1 l2 with
  | nil =>
      simp only [List.count_nil] at h1 h2
      have hl1 : l1 = [] := List.length_eq_zero_iff.mp h1
      have hl2 : l2 = [] := List.length_eq_zero_iff.mp h2
      subst hl1; subst hl2
      simp [riffle, marker, plane1Sub, plane2Sub]
  | cons b m ih =>
      cases b with
      | true =>
          have hc1 : (true :: m).count true = m.count true + 1 := by simp [List.count_cons]
          have hc2 : (true :: m).count false = m.count false := by simp [List.count_cons]
          rw [hc1] at h1
          rw [hc2] at h2
          cases l1 with
          | nil => simp at h1
          | cons p l1 =>
              have h1' : l1.length = m.count true := by
                simp only [List.length_cons] at h1; omega
              obtain ⟨im, i1, i2⟩ := ih l1 l2 h1' h2
              refine ⟨?_, ?_, ?_⟩
              · simp [riffle, marker, isPlane1, im]
              · simp [riffle, plane1Sub, matchP1_fromP1, i1]
              · simp [riffle, plane2Sub, matchP2_fromP1, i2]
      | false =>
          have hc1 : (false :: m).count true = m.count true := by simp [List.count_cons]
          have hc2 : (false :: m).count false = m.count false + 1 := by simp [List.count_cons]
          rw [hc1] at h1
          rw [hc2] at h2
          cases l2 with
          | nil => simp at h2
          | cons p l2 =>
              have h2' : l2.length = m.count false := by
                simp only [List.length_cons] at h2; omega
              obtain ⟨im, i1, i2⟩ := ih l1 l2 h1 h2'
              refine ⟨?_, ?_, ?_⟩
              · simp [riffle, marker, isPlane1, im]
              · simp [riffle, plane1Sub, matchP1_fromP2, i1]
              · simp [riffle, plane2Sub, matchP2_fromP2, i2]

theorem length_marker (ts : List Twist) : (marker ts).length = ts.length := by simp [marker]

theorem length_plane1Sub (ts : List Twist) : (plane1Sub ts).length = (marker ts).count true := by
  induction ts with
  | nil => simp [plane1Sub, marker]
  | cons t ts ih =>
      cases t <;>
        simp (config := { decide := true })
          [plane1Sub, marker, matchP1, isPlane1, List.filterMap_cons, List.count_cons] <;>
        exact ih

theorem length_plane2Sub (ts : List Twist) : (plane2Sub ts).length = (marker ts).count false := by
  induction ts with
  | nil => simp [plane2Sub, marker]
  | cons t ts ih =>
      cases t <;>
        simp (config := { decide := true })
          [plane2Sub, marker, matchP2, isPlane1, List.filterMap_cons, List.count_cons] <;>
        exact ih

-- ------------------------------------------
-- `countBalanced` is exactly both subsequences being balanced
-- ------------------------------------------

theorem count_up_plane1Sub (ts : List Twist) :
    ts.count Twist.up = (plane1Sub ts).count Plane1.up := by
  induction ts with
  | nil => simp [plane1Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane1Sub, matchP1, List.filterMap_cons, List.count_cons, ih]

theorem count_down_plane1Sub (ts : List Twist) :
    ts.count Twist.down = (plane1Sub ts).count Plane1.down := by
  induction ts with
  | nil => simp [plane1Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane1Sub, matchP1, List.filterMap_cons, List.count_cons, ih]

theorem count_left_plane1Sub (ts : List Twist) :
    ts.count Twist.left = (plane1Sub ts).count Plane1.left := by
  induction ts with
  | nil => simp [plane1Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane1Sub, matchP1, List.filterMap_cons, List.count_cons, ih]

theorem count_right_plane1Sub (ts : List Twist) :
    ts.count Twist.right = (plane1Sub ts).count Plane1.right := by
  induction ts with
  | nil => simp [plane1Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane1Sub, matchP1, List.filterMap_cons, List.count_cons, ih]

theorem count_slash_plane2Sub (ts : List Twist) :
    ts.count Twist.slash = (plane2Sub ts).count Plane2.slash := by
  induction ts with
  | nil => simp [plane2Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane2Sub, matchP2, List.filterMap_cons, List.count_cons, ih]

theorem count_backslash_plane2Sub (ts : List Twist) :
    ts.count Twist.backslash = (plane2Sub ts).count Plane2.backslash := by
  induction ts with
  | nil => simp [plane2Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane2Sub, matchP2, List.filterMap_cons, List.count_cons, ih]

theorem count_plus_plane2Sub (ts : List Twist) :
    ts.count Twist.plus = (plane2Sub ts).count Plane2.plus := by
  induction ts with
  | nil => simp [plane2Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane2Sub, matchP2, List.filterMap_cons, List.count_cons, ih]

theorem count_minus_plane2Sub (ts : List Twist) :
    ts.count Twist.minus = (plane2Sub ts).count Plane2.minus := by
  induction ts with
  | nil => simp [plane2Sub]
  | cons t ts ih => cases t <;> simp (config := { decide := true }) [plane2Sub, matchP2, List.filterMap_cons, List.count_cons, ih]

instance : DecidablePred countBalanced := fun ts => by unfold countBalanced; infer_instance

theorem countBalanced_iff (ts : List Twist) :
    countBalanced ts ↔ balanced1 (plane1Sub ts) ∧ balanced2 (plane2Sub ts) := by
  unfold countBalanced balanced1 balanced2
  rw [count_up_plane1Sub, count_down_plane1Sub, count_left_plane1Sub, count_right_plane1Sub,
      count_slash_plane2Sub, count_backslash_plane2Sub, count_plus_plane2Sub, count_minus_plane2Sub]
  tauto

-- ------------------------------------------
-- The per-marker fiber, then the sum over all markers
-- ------------------------------------------

/-- For a fixed marker `m`, the twist-histories carrying it are in bijection with pairs of
    balanced subsequences on the two planes. -/
theorem card_fiber_marker (L : ℕ) (m : List Bool) (hm : m ∈ words Bool L) :
    ((words Twist L).filter (fun ts => decide (countBalanced ts ∧ marker ts = m))).card =
      w₂ (m.count true) * w₂ (m.count false) := by
  rw [← card_balanced1 (m.count true), ← card_balanced2 (m.count false), ← Finset.card_product]
  apply Finset.card_bij' (fun ts _ => (plane1Sub ts, plane2Sub ts)) (fun p _ => riffle m p.1 p.2)
  · intro ts hts
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hts
    obtain ⟨hlen, hbal, hmark⟩ := hts
    have hb := (countBalanced_iff ts).mp hbal
    have hlen1 : (plane1Sub ts).length = m.count true := by rw [length_plane1Sub, hmark]
    have hlen2 : (plane2Sub ts).length = m.count false := by rw [length_plane2Sub, hmark]
    simp [Finset.mem_product, Finset.mem_filter, mem_words, hlen1, hlen2, hb.1, hb.2]
  · intro p hp
    obtain ⟨l1, l2⟩ := p
    simp only [Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hp
    obtain ⟨⟨hl1len, hb1⟩, hl2len, hb2⟩ := hp
    obtain ⟨im, i1, i2⟩ := riffle_wf m l1 l2 hl1len hl2len
    have hlenr : (riffle m l1 l2).length = L := by
      rw [← length_marker (riffle m l1 l2), im]; exact (mem_words L m).mp hm
    have hbalr : countBalanced (riffle m l1 l2) := by
      rw [countBalanced_iff, i1, i2]; exact ⟨hb1, hb2⟩
    simp [Finset.mem_filter, mem_words, hlenr, hbalr, im]
  · intro ts hts
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hts
    obtain ⟨_, _, hmark⟩ := hts
    rw [← hmark]; exact riffle_correct ts
  · intro p hp
    obtain ⟨l1, l2⟩ := p
    simp only [Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hp
    obtain ⟨⟨hl1len, _⟩, hl2len, _⟩ := hp
    obtain ⟨_, i1, i2⟩ := riffle_wf m l1 l2 hl1len hl2len
    simp [i1, i2]

/-- **The bridge theorem.** Balanced twist-histories of length `L` are counted exactly by
    `walkCount L` — the `ℤ²×ℤ²` split `qucalc_search.py`/`closure_walk.py` compute, now bridged
    all the way from twist histories. -/
theorem card_balanced_twist (L : ℕ) :
    ((words Twist L).filter (fun ts => decide (countBalanced ts))).card = walkCount L := by
  have hpart1 : (words Twist L).filter (fun ts => decide (countBalanced ts)) =
      (words Bool L).biUnion (fun m =>
        (words Twist L).filter (fun ts => decide (countBalanced ts ∧ marker ts = m))) := by
    apply Finset.ext
    intro ts
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq, Finset.mem_biUnion]
    constructor
    · rintro ⟨hlen, hbal⟩
      exact ⟨marker ts, by rw [mem_words, length_marker, hlen], hlen, hbal, rfl⟩
    · rintro ⟨m, _, hlen, hbal, _⟩
      exact ⟨hlen, hbal⟩
  rw [hpart1]
  have hdisj1 : ∀ m1 ∈ words Bool L, ∀ m2 ∈ words Bool L, m1 ≠ m2 →
      Disjoint ((words Twist L).filter (fun ts => decide (countBalanced ts ∧ marker ts = m1)))
               ((words Twist L).filter (fun ts => decide (countBalanced ts ∧ marker ts = m2))) := by
    intro m1 _ m2 _ hne
    apply Finset.disjoint_left.mpr
    intro ts hts1 hts2
    simp only [Finset.mem_filter, decide_eq_true_eq] at hts1 hts2
    exact hne (hts1.2.2.symm.trans hts2.2.2)
  rw [Finset.card_biUnion hdisj1]
  have hstep1 : ∀ m ∈ words Bool L, ((words Twist L).filter
      (fun ts => decide (countBalanced ts ∧ marker ts = m))).card =
      w₂ (m.count true) * w₂ (L - m.count true) := by
    intro m hm
    rw [card_fiber_marker L m hm]
    have hlen := (mem_words L m).mp hm
    have hc : m.count true + m.count false = m.length := List.count_true_add_count_false m
    have : m.count false = L - m.count true := by omega
    rw [this]
  rw [Finset.sum_congr rfl hstep1]
  have hpart2 : words Bool L = (Finset.range (L + 1)).biUnion
      (fun k => (words Bool L).filter (fun m => decide (m.count true = k))) := by
    apply Finset.ext
    intro m
    simp only [Finset.mem_biUnion, Finset.mem_range, Finset.mem_filter, decide_eq_true_eq]
    constructor
    · intro hm
      have hlen := (mem_words L m).mp hm
      have : m.count true ≤ m.length := List.count_le_length
      exact ⟨m.count true, by omega, hm, rfl⟩
    · rintro ⟨k, _, hm, _⟩
      exact hm
  rw [hpart2]
  have hdisj2 : ∀ k1 ∈ Finset.range (L + 1), ∀ k2 ∈ Finset.range (L + 1), k1 ≠ k2 →
      Disjoint ((words Bool L).filter (fun m => decide (m.count true = k1)))
               ((words Bool L).filter (fun m => decide (m.count true = k2))) := by
    intro k1 _ k2 _ hne
    apply Finset.disjoint_left.mpr
    intro m hm1 hm2
    simp only [Finset.mem_filter, decide_eq_true_eq] at hm1 hm2
    exact hne (hm1.2.symm.trans hm2.2)
  rw [Finset.sum_biUnion hdisj2]
  have hstep2 : ∀ k ∈ Finset.range (L + 1),
      (∑ m ∈ (words Bool L).filter (fun m => decide (m.count true = k)),
        w₂ (m.count true) * w₂ (L - m.count true)) =
      L.choose k * w₂ k * w₂ (L - k) := by
    intro k _
    have hconst : ∀ m ∈ (words Bool L).filter (fun m => decide (m.count true = k)),
        w₂ (m.count true) * w₂ (L - m.count true) = w₂ k * w₂ (L - k) := by
      intro m hm
      simp only [Finset.mem_filter, decide_eq_true_eq] at hm
      rw [hm.2]
    rw [Finset.sum_congr rfl hconst, Finset.sum_const, smul_eq_mul, card_filter_count_true]
  rw [Finset.sum_congr rfl hstep2]
  rfl
