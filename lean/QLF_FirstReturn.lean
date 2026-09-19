import QLF_TwistAlphabet
import QLF_KraftMeasure
import QLF_PolyaTransience
import QLF_ProductWalk
-- Narrow imports (see QLF_PhaseRule): this module never needs `import Mathlib`.

set_option linter.unusedVariables false

/-!
# QLF_FirstReturn — the Dyson bijection: `walkCount` as a renewal sum over first closures

[`Closure_Walk.md`](../Closure_Walk.md) §5, closing [issue #157](https://github.com/rchain-community/quantum-logical-framework/issues/157):
a balanced twist-history of length `L ≥ 1` splits *uniquely* at its first closure into a **prime**
prefix (a balanced history with no proper non-empty balanced prefix of its own) and an arbitrary
balanced remainder. Counting this bijection gives `walkCount L = Σ_{ℓ=1}^{L} I(ℓ) · walkCount(L−ℓ)`
where `I(ℓ)` is the number of length-`ℓ` primes — exactly the renewal relation
`QLF_PolyaTransience.polya_transience` needs, with `a(k) = I(k)/8^k`. The result:
**at least a quarter of possibility never closes is now a theorem about the twist census**
(`at_least_quarter_never_closes`), not a numerical observation. No axioms.
-/

namespace QLF.FirstReturn

open Finset QLF QLF.PolyaTransience QLF.ProductWalk

-- ==========================================
-- Primes: first closures
-- ==========================================

/-- `h` is a **prime** (a first closure): nonempty, balanced, and no proper non-empty prefix of
    `h` is itself balanced. -/
def IsPrime (h : List Twist) : Prop :=
  0 < h.length ∧ countBalanced h ∧ ∀ k, 0 < k → k < h.length → ¬ countBalanced (h.take k)

instance : DecidablePred IsPrime := fun h => by unfold IsPrime; infer_instance

-- ==========================================
-- Split / merge at a closure point
-- ==========================================

theorem drop_balanced_of_prime_take (h : List Twist) (ℓ : ℕ) (hb : countBalanced h)
    (hp : IsPrime (h.take ℓ)) : countBalanced (h.drop ℓ) := by
  obtain ⟨-, hbp, -⟩ := hp
  have hsplit : h = h.take ℓ ++ h.drop ℓ := (List.take_append_drop ℓ h).symm
  unfold countBalanced at hb hbp ⊢
  rw [hsplit] at hb
  simp only [List.count_append] at hb
  omega

theorem append_prime_balanced (p q : List Twist) (hp : IsPrime p) (hq : countBalanced q) :
    countBalanced (p ++ q) := by
  obtain ⟨-, hbp, -⟩ := hp
  unfold countBalanced at hbp hq ⊢
  simp only [List.count_append]
  omega

theorem prime_take_of_prime_append (p q : List Twist) (hp : IsPrime p) :
    IsPrime ((p ++ q).take p.length) := by
  rw [List.take_left]; exact hp

-- ==========================================
-- Uniqueness and existence of the first closure
-- ==========================================

theorem prime_prefix_unique (h : List Twist) (ℓ1 ℓ2 : ℕ) (hl1 : ℓ1 ≤ h.length)
    (hl2 : ℓ2 ≤ h.length) (hp1 : IsPrime (h.take ℓ1)) (hp2 : IsPrime (h.take ℓ2)) :
    ℓ1 = ℓ2 := by
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have heq : (h.take ℓ2).take ℓ1 = h.take ℓ1 := by
      rw [List.take_take, min_eq_left hlt.le]
    obtain ⟨-, hb1, -⟩ := hp1
    obtain ⟨-, -, hu2⟩ := hp2
    have hlen2 : (h.take ℓ2).length = ℓ2 := by rw [List.length_take]; omega
    exact hu2 ℓ1 (by omega) (by omega) (by rw [heq]; exact hb1)
  · have heq : (h.take ℓ1).take ℓ2 = h.take ℓ2 := by
      rw [List.take_take, min_eq_right hgt.le]
    obtain ⟨-, -, hu1⟩ := hp1
    obtain ⟨-, hb2, -⟩ := hp2
    have hlen1 : (h.take ℓ1).length = ℓ1 := by rw [List.length_take]; omega
    exact hu1 ℓ2 (by omega) (by omega) (by rw [heq]; exact hb2)

theorem prime_prefix_exists (h : List Twist) (hb : countBalanced h) (hL : 0 < h.length) :
    ∃ ℓ, ℓ ≤ h.length ∧ IsPrime (h.take ℓ) := by
  classical
  have hex : ∃ k, 0 < k ∧ countBalanced (h.take k) :=
    ⟨h.length, hL, by rw [List.take_length]; exact hb⟩
  have hle : Nat.find hex ≤ h.length :=
    Nat.find_min' hex ⟨hL, by rw [List.take_length]; exact hb⟩
  refine ⟨Nat.find hex, hle, ?_, ?_, ?_⟩
  · rw [List.length_take, min_eq_left hle]; exact (Nat.find_spec hex).1
  · exact (Nat.find_spec hex).2
  · intro k hk0 hklt
    rw [List.length_take, min_eq_left hle] at hklt
    have heq : (h.take (Nat.find hex)).take k = h.take k := by
      rw [List.take_take, min_eq_left hklt.le]
    rw [heq]
    intro hbal
    exact Nat.find_min hex hklt ⟨hk0, hbal⟩

-- ==========================================
-- The per-closure-length fiber, then the sum over closure lengths
-- ==========================================

/-- For a fixed closure length `ℓ`, the balanced histories of length `L` whose first closure is
    exactly `ℓ` are in bijection with pairs (prime of length `ℓ`, balanced of length `L−ℓ`). -/
theorem card_fiber_prime (L ℓ : ℕ) (hℓL : ℓ ≤ L) :
    ((words Twist L).filter (fun h => decide (countBalanced h ∧ IsPrime (h.take ℓ)))).card =
      ((words Twist ℓ).filter (fun p => decide (IsPrime p))).card *
      ((words Twist (L - ℓ)).filter (fun q => decide (countBalanced q))).card := by
  rw [← Finset.card_product]
  apply Finset.card_bij' (fun h _ => (h.take ℓ, h.drop ℓ)) (fun pq _ => pq.1 ++ pq.2)
  case hi =>
    intro h hh
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hh
    obtain ⟨hlen, hbal, hprime⟩ := hh
    have htlen : (h.take ℓ).length = ℓ := by rw [List.length_take]; omega
    have hqlen : (h.drop ℓ).length = L - ℓ := by rw [List.length_drop, hlen]
    have hqbal : countBalanced (h.drop ℓ) := drop_balanced_of_prime_take h ℓ hbal hprime
    simp [Finset.mem_product, Finset.mem_filter, mem_words, htlen, hprime, hqlen, hqbal]
  case hj =>
    intro pq hpq
    obtain ⟨p, q⟩ := pq
    simp only [Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hpq
    obtain ⟨⟨hplen, hpprime⟩, hqlen, hqbal⟩ := hpq
    have hlen : (p ++ q).length = L := by rw [List.length_append, hplen, hqlen]; omega
    have hbal : countBalanced (p ++ q) := append_prime_balanced p q hpprime hqbal
    have htake : (p ++ q).take ℓ = p := by rw [← hplen]; exact List.take_left
    have hprime : IsPrime ((p ++ q).take ℓ) := by rw [htake]; exact hpprime
    simp [Finset.mem_filter, mem_words, hlen, hbal, hprime]
  case left_inv =>
    intro h _
    exact List.take_append_drop ℓ h
  case right_inv =>
    intro pq hpq
    obtain ⟨p, q⟩ := pq
    simp only [Finset.mem_product, Finset.mem_filter, mem_words, decide_eq_true_eq] at hpq
    obtain ⟨⟨hplen, -⟩, -⟩ := hpq
    rw [← hplen]
    simp [List.take_left, List.drop_left]

/-- **The Dyson identity, in card terms.** A balanced history of length `L ≥ 1` splits uniquely at
    its first closure. -/
theorem card_balanced_eq_sum_prime (L : ℕ) (hL : 0 < L) :
    ((words Twist L).filter (fun h => decide (countBalanced h))).card =
      ∑ k ∈ Finset.range L, ((words Twist (k + 1)).filter (fun p => decide (IsPrime p))).card *
        ((words Twist (L - (k + 1))).filter (fun q => decide (countBalanced q))).card := by
  have hpart : (words Twist L).filter (fun h => decide (countBalanced h)) =
      (Finset.range L).biUnion (fun k =>
        (words Twist L).filter (fun h => decide (countBalanced h ∧ IsPrime (h.take (k + 1))))) := by
    apply Finset.ext
    intro h
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq, Finset.mem_biUnion,
      Finset.mem_range]
    constructor
    · intro hh
      obtain ⟨hlen, hbal⟩ := hh
      obtain ⟨ℓ, hℓL, hprime⟩ := prime_prefix_exists h hbal (by omega)
      have htlen : (h.take ℓ).length = ℓ := by rw [List.length_take]; omega
      have hl0 : 0 < ℓ := by have := hprime.1; omega
      refine ⟨ℓ - 1, by omega, hlen, hbal, ?_⟩
      have hℓeq : ℓ - 1 + 1 = ℓ := by omega
      rw [hℓeq]; exact hprime
    · rintro ⟨k, -, hlen, hbal, -⟩
      exact ⟨hlen, hbal⟩
  rw [hpart]
  have hdisj : ∀ k1 ∈ Finset.range L, ∀ k2 ∈ Finset.range L, k1 ≠ k2 →
      Disjoint
        ((words Twist L).filter (fun h => decide (countBalanced h ∧ IsPrime (h.take (k1 + 1)))))
        ((words Twist L).filter (fun h => decide (countBalanced h ∧ IsPrime (h.take (k2 + 1))))) := by
    intro k1 hk1 k2 hk2 hne
    simp only [Finset.mem_range] at hk1 hk2
    apply Finset.disjoint_left.mpr
    intro h hh1 hh2
    simp only [Finset.mem_filter, mem_words, decide_eq_true_eq] at hh1 hh2
    have heq := prime_prefix_unique h (k1 + 1) (k2 + 1) (by omega) (by omega) hh1.2.2 hh2.2.2
    exact hne (by omega)
  rw [Finset.card_biUnion hdisj]
  apply Finset.sum_congr rfl
  intro k hk
  simp only [Finset.mem_range] at hk
  exact card_fiber_prime L (k + 1) (by omega)

-- ==========================================
-- Connecting to `walkCount`, `returnWeight`, and `polya_transience`
-- ==========================================

/-- The number of length-`ℓ` primes. -/
noncomputable def primeCount (ℓ : ℕ) : ℕ :=
  ((words Twist ℓ).filter (fun p => decide (IsPrime p))).card

theorem primeCount_zero : primeCount 0 = 0 := by
  unfold primeCount
  apply Finset.card_eq_zero.mpr
  apply Finset.filter_eq_empty_iff.mpr
  intro p hp
  simp only [decide_eq_true_eq]
  intro hprime
  have h1 := hprime.1
  simp only [mem_words] at hp
  omega

/-- **The Dyson identity.** `walkCount L = Σ_{ℓ=1}^{L} I(ℓ) · walkCount(L−ℓ)` for `L ≥ 1`, reindexed
    as a sum over `k = ℓ − 1 ∈ [0, L)`. -/
theorem walkCount_eq_sum_prime (L : ℕ) (hL : 0 < L) :
    walkCount L = ∑ k ∈ Finset.range L, primeCount (k + 1) * walkCount (L - (k + 1)) := by
  rw [← card_balanced_twist L, card_balanced_eq_sum_prime L hL]
  apply Finset.sum_congr rfl
  intro k _
  unfold primeCount
  rw [card_balanced_twist (L - (k + 1))]

/-- The prime Kraft weight: `a(k) = I(k)/8^k`. -/
noncomputable def a (k : ℕ) : ℝ := (primeCount k : ℝ) / 8 ^ k

theorem a_zero : a 0 = 0 := by unfold a; rw [primeCount_zero]; norm_num

theorem a_nonneg (n : ℕ) : 0 ≤ a n := by unfold a; positivity

theorem a_returnWeight_term (L k : ℕ) (hk : k < L) :
    (primeCount (k + 1) * walkCount (L - (k + 1)) : ℝ) / 8 ^ L =
      a (k + 1) * returnWeight (L - (k + 1)) := by
  unfold a returnWeight
  have hpow : (8 : ℝ) ^ (k + 1) * (8 : ℝ) ^ (L - (k + 1)) = 8 ^ L := by
    rw [← pow_add]; congr 1; omega
  rw [← hpow]
  push_cast
  field_simp

/-- **The renewal relation `polya_transience` needs**, supplied by the Dyson bijection. -/
theorem renewal_relation (L : ℕ) :
    returnWeight L = (if L = 0 then 1 else 0) +
      ∑ k ∈ Finset.range (L + 1), a k * returnWeight (L - k) := by
  rcases Nat.eq_zero_or_pos L with rfl | hL
  · simp [returnWeight_zero, a_zero]
  · rw [if_neg (by omega), Finset.sum_range_succ']
    have hzero : a 0 * returnWeight (L - 0) = 0 := by rw [a_zero]; ring
    rw [hzero, add_zero]
    have hstep : ∑ k ∈ Finset.range L, a (k + 1) * returnWeight (L - (k + 1)) =
        ∑ k ∈ Finset.range L, (primeCount (k + 1) * walkCount (L - (k + 1)) : ℝ) / 8 ^ L := by
      apply Finset.sum_congr rfl
      intro k hk
      exact (a_returnWeight_term L k (Finset.mem_range.mp hk)).symm
    rw [hstep]
    unfold returnWeight
    rw [walkCount_eq_sum_prime L hL, Nat.cast_sum, Finset.sum_div]
    apply Finset.sum_congr rfl
    intro k _
    push_cast
    ring

/-- **At least a quarter of possibility never closes — now a theorem about the twist census.**
    The prime Kraft weight `a(k) = I(k)/8^k` is in renewal relation with the `ℤ⁴` return weight
    (`renewal_relation`, supplied by the Dyson bijection `walkCount_eq_sum_prime`), so
    `QLF_PolyaTransience.polya_transience` applies directly. -/
theorem at_least_quarter_never_closes : ∑' n, a n ≤ 3 / 4 :=
  polya_transience a_zero a_nonneg renewal_relation
