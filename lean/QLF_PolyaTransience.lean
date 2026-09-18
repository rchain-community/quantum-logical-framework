import Mathlib.Data.Nat.Choose.Central
import Mathlib.Data.Nat.Choose.Sum
import Mathlib.Topology.Algebra.InfiniteSum.Real
import Mathlib.Analysis.Normed.Ring.InfiniteSum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
-- Narrow imports (see QLF_PhaseRule): this module never needs `import Mathlib`.

set_option linter.unusedVariables false

/-!
# QLF_PolyaTransience — **not everything closes**: the closure walk is transient

[`Closure_Walk.md`](../Closure_Walk.md) §0: a count-balanced history is a closed walk on `ℤ⁴`, and
the fraction of the uniform possibility measure that *ever* closes is Pólya's return probability
`p₄ = 0.1932…` — so `80.7 %` of possibility never closes, and ZFA is a selection principle with
teeth *because* the frame is four-dimensional (Pólya 1921: the walk is recurrent in `d ≤ 2`,
transient in `d ≥ 3`). This module proves the transience half of that with elementary bounds, and
nothing else: no Stirling, no probability theory, no analysis beyond summable series.

## What is proved

The walk counts are taken in the `ℤ² × ℤ²` split that `closure_walk.py` computes and checks:
`walkCount L = Σ_k C(L,k) · w₂(k) · w₂(L−k)`, with `w₂(2m) = C(2m,m)²` the closed walks of the plane
(its two diagonal coordinates walk independently) and `w₂(odd) = 0`. The bridge from twist histories
to this formula is a separate module ([`Closure_Walk.md`](../Closure_Walk.md) §5); here the formula is
the object.

* **`centralBinom_sq_mul_le`** — `C(2m,m)² · (3m+1) ≤ 16^m`, by induction: the step is the integer
  inequality `4(2m+1)²(3m+4) ≤ 16(m+1)²(3m+1)`, i.e. `19m ≤ 20m`. Hence
  **`w₂_bound`**: `(k+1) · w₂(k) ≤ 4^k`.
* **`walkCount_mul_le`** — `walkCount L · (L+1)(L+2) ≤ 4 · 8^L`, in `ℕ`. The identity
  `C(L,k)(L+1)(L+2) = C(L+2,k+1)(k+1)(L+1−k)` absorbs the two `(k+1)`, `(L−k+1)` factors from
  `w₂_bound`, and `Σ_k C(L+2,k+1) ≤ 2^{L+2}` finishes. So the return weight
  `u_L = walkCount L / 8^L` is at most `4/((L+1)(L+2))`.
* **`returnWeight_summable`**, **`returnWeight_tsum_le_four`** — the expected number of returns
  `G = Σ_L u_L` is finite and at most `4` (telescoping, `telescope`); **`returnWeight_tail_le`** —
  the tail past `N` is at most `4/(N+2)`, which is what turns exact partial sums into a rigorous
  interval for the limit.
* **`renewal_tsum`** — the renewal theorem: if `a` (first-return weights, non-negative, `a 0 = 0`)
  and `u` (return weights, `u 0 = 1`, summable) satisfy `u_L = [L=0] + Σ_k a_k u_{L−k}`, then `a` is
  summable and `Σ a = 1 − 1/Σ u`. Generating functions `U = 1 + A·U` as a Cauchy product of
  summable series. **`renewal_tsum_lt_one`**: `Σ a < 1` — transience.
* **`polya_transience`** — for any first-return weights `a` in renewal relation with `returnWeight`:
  `Σ a ≤ 3/4`. The prime Kraft mass `Σ_π 8^{−|π|}` is such an `a` once `QLF_FirstReturn` supplies the
  Dyson identity as a bijection; then "at least a quarter of possibility never closes" is a theorem,
  and the numerics say `80.7 %`.

The exact constant `p₄` has no closed form (a Watson-type integral), so the limit itself is not a
target; the interval `[partial sum, partial sum + 4/(N+2)]` is.

No axioms.
-/

namespace QLF.PolyaTransience

open Finset

-- ==========================================
-- The plane: C(2m,m)² · (3m+1) ≤ 16^m
-- ==========================================

/-- The elementary central-binomial bound, squared to avoid the square root:
    `C(2m,m)² (3m+1) ≤ 16^m`. -/
theorem centralBinom_sq_mul_le (m : ℕ) : (Nat.centralBinom m) ^ 2 * (3 * m + 1) ≤ 16 ^ m := by
  induction m with
  | zero => decide
  | succ m ih =>
      have h : (m + 1) * Nat.centralBinom (m + 1) = 2 * (2 * m + 1) * Nat.centralBinom m :=
        Nat.succ_mul_centralBinom_succ m
      have hpoly : 4 * (2 * m + 1) ^ 2 * (3 * m + 4) ≤ 16 * (m + 1) ^ 2 * (3 * m + 1) := by
        nlinarith
      have key : ((m + 1) ^ 2 * (3 * m + 1)) * ((Nat.centralBinom (m + 1)) ^ 2 * (3 * m + 4))
          ≤ ((m + 1) ^ 2 * (3 * m + 1)) * 16 ^ (m + 1) := by
        calc ((m + 1) ^ 2 * (3 * m + 1)) * ((Nat.centralBinom (m + 1)) ^ 2 * (3 * m + 4))
            = ((m + 1) * Nat.centralBinom (m + 1)) ^ 2 * (3 * m + 1) * (3 * m + 4) := by ring
          _ = (2 * (2 * m + 1) * Nat.centralBinom m) ^ 2 * (3 * m + 1) * (3 * m + 4) := by rw [h]
          _ = 4 * (2 * m + 1) ^ 2 * (3 * m + 4) * ((Nat.centralBinom m) ^ 2 * (3 * m + 1)) := by
              ring
          _ ≤ 4 * (2 * m + 1) ^ 2 * (3 * m + 4) * 16 ^ m := Nat.mul_le_mul_left _ ih
          _ ≤ 16 * (m + 1) ^ 2 * (3 * m + 1) * 16 ^ m := Nat.mul_le_mul_right _ hpoly
          _ = ((m + 1) ^ 2 * (3 * m + 1)) * 16 ^ (m + 1) := by ring
      exact Nat.le_of_mul_le_mul_left key (by positivity)

/-- Closed walks of length `k` on the plane `ℤ²`: `C(k, k/2)²` for even `k` (the two diagonal
    coordinates are independent `±1` walks), none for odd `k`. -/
def w₂ (k : ℕ) : ℕ := if k % 2 = 0 then (Nat.centralBinom (k / 2)) ^ 2 else 0

/-- The plane's return weight decays like `1/k`: `(k+1) · w₂(k) ≤ 4^k`. -/
theorem w₂_bound (k : ℕ) : (k + 1) * w₂ k ≤ 4 ^ k := by
  unfold w₂
  split_ifs with h
  · obtain ⟨m, rfl⟩ : ∃ m, k = 2 * m := ⟨k / 2, by omega⟩
    rw [Nat.mul_div_cancel_left m (by norm_num)]
    calc (2 * m + 1) * (Nat.centralBinom m) ^ 2
        ≤ (3 * m + 1) * (Nat.centralBinom m) ^ 2 := Nat.mul_le_mul_right _ (by omega)
      _ = (Nat.centralBinom m) ^ 2 * (3 * m + 1) := by ring
      _ ≤ 16 ^ m := centralBinom_sq_mul_le m
      _ = 4 ^ (2 * m) := by rw [pow_mul]; norm_num
  · simp

-- ==========================================
-- ℤ⁴ = ℤ² × ℤ²: the closed-walk count and its bound
-- ==========================================

/-- Closed walks of length `L` on `ℤ⁴`, splitting the steps between the two planes. This is
    `closed_walk_count` of `closure_walk.py`; `W_2 = 8, W_4 = 168, W_6 = 5120, W_8 = 190120`. -/
def walkCount (L : ℕ) : ℕ := ∑ k ∈ range (L + 1), L.choose k * w₂ k * w₂ (L - k)

theorem walkCount_zero : walkCount 0 = 1 := by decide
theorem walkCount_two : walkCount 2 = 8 := by decide
theorem walkCount_four : walkCount 4 = 168 := by decide
theorem walkCount_six : walkCount 6 = 5120 := by decide
theorem walkCount_eight : walkCount 8 = 190120 := by decide

/-- The binomial identity that absorbs the two denominators:
    `C(L,k)(L+1)(L+2) = C(L+2,k+1)(k+1)(L+1−k)`. -/
theorem choose_mul_succ_succ (L k : ℕ) (hk : k ≤ L) :
    L.choose k * ((L + 1) * (L + 1 + 1))
      = (L + 1 + 1).choose (k + 1) * ((k + 1) * (L + 1 - k)) := by
  have h1 : (L + 1) * L.choose k = (L + 1).choose (k + 1) * (k + 1) := Nat.succ_mul_choose_eq L k
  have h2 : (L + 1).choose (k + 1) * (L + 1 + 1)
      = (L + 1 + 1).choose (k + 1) * (L + 1 + 1 - (k + 1)) := Nat.choose_mul_succ_eq (L + 1) (k + 1)
  have h3 : L + 1 + 1 - (k + 1) = L + 1 - k := by omega
  rw [h3] at h2
  calc L.choose k * ((L + 1) * (L + 1 + 1))
      = ((L + 1) * L.choose k) * (L + 1 + 1) := by ring
    _ = ((L + 1).choose (k + 1) * (k + 1)) * (L + 1 + 1) := by rw [h1]
    _ = ((L + 1).choose (k + 1) * (L + 1 + 1)) * (k + 1) := by ring
    _ = ((L + 1 + 1).choose (k + 1) * (L + 1 - k)) * (k + 1) := by rw [h2]
    _ = (L + 1 + 1).choose (k + 1) * ((k + 1) * (L + 1 - k)) := by ring

/-- The shifted row sum is at most the full row: `Σ_{k ≤ n} C(n+2, k+1) ≤ 2^{n+2}`. -/
theorem sum_choose_shift_le (n : ℕ) :
    ∑ k ∈ range (n + 1), (n + 1 + 1).choose (k + 1) ≤ 2 ^ (n + 1 + 1) := by
  have h := Nat.sum_range_choose (n + 1 + 1)
  rw [Finset.sum_range_succ', Finset.sum_range_succ] at h
  omega

/-- **The return-weight bound, in `ℕ`**: `walkCount L · (L+1)(L+2) ≤ 4 · 8^L`. -/
theorem walkCount_mul_le (L : ℕ) : walkCount L * ((L + 1) * (L + 1 + 1)) ≤ 4 * 8 ^ L := by
  unfold walkCount
  rw [Finset.sum_mul]
  calc ∑ k ∈ range (L + 1), L.choose k * w₂ k * w₂ (L - k) * ((L + 1) * (L + 1 + 1))
      ≤ ∑ k ∈ range (L + 1), (L + 1 + 1).choose (k + 1) * 4 ^ L := by
        apply Finset.sum_le_sum
        intro k hk
        have hkL : k ≤ L := Nat.lt_succ_iff.mp (Finset.mem_range.mp hk)
        calc L.choose k * w₂ k * w₂ (L - k) * ((L + 1) * (L + 1 + 1))
            = (L.choose k * ((L + 1) * (L + 1 + 1))) * (w₂ k * w₂ (L - k)) := by ring
          _ = ((L + 1 + 1).choose (k + 1) * ((k + 1) * (L + 1 - k))) * (w₂ k * w₂ (L - k)) := by
              rw [choose_mul_succ_succ L k hkL]
          _ = (L + 1 + 1).choose (k + 1) * (((k + 1) * w₂ k) * ((L - k + 1) * w₂ (L - k))) := by
              have : L + 1 - k = L - k + 1 := by omega
              rw [this]; ring
          _ ≤ (L + 1 + 1).choose (k + 1) * (4 ^ k * 4 ^ (L - k)) := by
              exact Nat.mul_le_mul_left _ (Nat.mul_le_mul (w₂_bound k) (w₂_bound (L - k)))
          _ = (L + 1 + 1).choose (k + 1) * 4 ^ L := by
              rw [← pow_add, Nat.add_sub_of_le hkL]
    _ = (∑ k ∈ range (L + 1), (L + 1 + 1).choose (k + 1)) * 4 ^ L := by rw [Finset.sum_mul]
    _ ≤ 2 ^ (L + 1 + 1) * 4 ^ L := Nat.mul_le_mul_right _ (sum_choose_shift_le L)
    _ = 4 * 8 ^ L := by
        rw [show (8 : ℕ) = 2 * 4 by norm_num, mul_pow]
        ring

-- ==========================================
-- The return weight, its sum, and its tail
-- ==========================================

/-- The return weight `u_L = W_L / 8^L`: the uniform-measure probability that a history of length
    `L` is count-balanced. -/
noncomputable def returnWeight (L : ℕ) : ℝ := (walkCount L : ℝ) / 8 ^ L

theorem returnWeight_nonneg (L : ℕ) : 0 ≤ returnWeight L := by
  unfold returnWeight; positivity

theorem returnWeight_zero : returnWeight 0 = 1 := by
  simp [returnWeight, walkCount_zero]

/-- `u_L ≤ 4/((L+1)(L+2))`. -/
theorem returnWeight_le (L : ℕ) :
    returnWeight L ≤ 4 / (((L : ℝ) + 1) * ((L : ℝ) + 1 + 1)) := by
  unfold returnWeight
  rw [div_le_iff₀ (by positivity), div_mul_eq_mul_div, le_div_iff₀ (by positivity)]
  exact_mod_cast walkCount_mul_le L

/-- Telescoping: `Σ_{i<n} 4/((i+c)(i+c+1)) = 4/c − 4/(n+c)`. -/
theorem telescope (c : ℝ) (hc : 0 < c) (n : ℕ) :
    ∑ i ∈ range n, (4 : ℝ) / ((i + c) * (i + c + 1)) = 4 / c - 4 / (n + c) := by
  have h : ∀ i : ℕ, (4 : ℝ) / ((i + c) * (i + c + 1)) = 4 / (i + c) - 4 / ((i + 1 : ℕ) + c) := by
    intro i
    push_cast
    rw [div_sub_div _ _ (by positivity) (by positivity)]
    congr 1 <;> ring
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ih, h n]
      push_cast
      ring

/-- Partial sums of the return weight are bounded by `4`. -/
theorem sum_returnWeight_le (n : ℕ) : ∑ i ∈ range n, returnWeight i ≤ 4 := by
  calc ∑ i ∈ range n, returnWeight i
      ≤ ∑ i ∈ range n, (4 : ℝ) / ((i + 1) * (i + 1 + 1)) :=
        Finset.sum_le_sum (fun i _ => returnWeight_le i)
    _ = 4 / 1 - 4 / (n + 1) := telescope 1 one_pos n
    _ ≤ 4 := by
        have : (0 : ℝ) ≤ 4 / ((n : ℝ) + 1) := by positivity
        rw [div_one]
        linarith

/-- **The expected number of returns is finite**: the walk on `ℤ⁴` is transient. -/
theorem returnWeight_summable : Summable returnWeight :=
  summable_of_sum_range_le returnWeight_nonneg sum_returnWeight_le

/-- `G = Σ_L u_L ≤ 4`. -/
theorem returnWeight_tsum_le_four : ∑' L, returnWeight L ≤ 4 :=
  Real.tsum_le_of_sum_range_le returnWeight_nonneg sum_returnWeight_le

/-- **The tail bound**: `Σ_{L > N} u_L ≤ 4/(N+2)` — what makes an exact partial sum a rigorous
    two-sided bound on the limit. -/
theorem returnWeight_tail_le (N : ℕ) : ∑' i, returnWeight (N + 1 + i) ≤ 4 / ((N : ℝ) + 2) := by
  apply Real.tsum_le_of_sum_range_le (fun i => returnWeight_nonneg _)
  intro n
  have hc : (0 : ℝ) < (N : ℝ) + 2 := by positivity
  calc ∑ i ∈ range n, returnWeight (N + 1 + i)
      ≤ ∑ i ∈ range n, (4 : ℝ) / ((i + ((N : ℝ) + 2)) * (i + ((N : ℝ) + 2) + 1)) := by
        apply Finset.sum_le_sum
        intro i _
        calc returnWeight (N + 1 + i)
            ≤ 4 / ((((N + 1 + i : ℕ) : ℝ) + 1) * (((N + 1 + i : ℕ) : ℝ) + 1 + 1)) :=
              returnWeight_le _
          _ = 4 / ((i + ((N : ℝ) + 2)) * (i + ((N : ℝ) + 2) + 1)) := by
              push_cast
              ring
    _ = 4 / ((N : ℝ) + 2) - 4 / (n + ((N : ℝ) + 2)) := telescope _ hc n
    _ ≤ 4 / ((N : ℝ) + 2) := by
        have : (0 : ℝ) ≤ 4 / ((n : ℝ) + ((N : ℝ) + 2)) := by positivity
        linarith

-- ==========================================
-- The renewal theorem: Σ a = 1 − 1/Σ u
-- ==========================================

/-- **Renewal.** First-return weights `a` (`a 0 = 0`, non-negative) and return weights `u`
    (`u 0 = 1`, non-negative, summable) with `u_L = [L = 0] + Σ_{k ≤ L} a_k u_{L−k}` satisfy
    `Σ a = 1 − 1/Σ u`: the generating-function identity `U = 1 + A·U`, as a Cauchy product of
    summable series. -/
theorem renewal_tsum {u a : ℕ → ℝ} (hu0 : u 0 = 1) (ha0 : a 0 = 0)
    (ha : ∀ n, 0 ≤ a n) (hun : ∀ n, 0 ≤ u n)
    (hren : ∀ L, u L = (if L = 0 then 1 else 0) + ∑ k ∈ range (L + 1), a k * u (L - k))
    (hsum : Summable u) :
    Summable a ∧ ∑' n, a n = 1 - 1 / ∑' n, u n := by
  have hle : ∀ n, a n ≤ u n := by
    intro n
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · rw [ha0, hu0]; norm_num
    · have h := hren n
      rw [if_neg (Nat.pos_iff_ne_zero.mp hn), zero_add] at h
      rw [h]
      have hterm : a n * u (n - n) ≤ ∑ k ∈ range (n + 1), a k * u (n - k) :=
        Finset.single_le_sum (f := fun k => a k * u (n - k))
          (fun k _ => mul_nonneg (ha k) (hun _)) (Finset.mem_range.mpr (Nat.lt_succ_self n))
      simpa [hu0] using hterm
  have hsa : Summable a := Summable.of_nonneg_of_le ha hle hsum
  refine ⟨hsa, ?_⟩
  have hGpos : 0 < ∑' n, u n := hsum.tsum_pos hun 0 (by rw [hu0]; norm_num)
  have hna : Summable fun n => ‖a n‖ := by
    simpa only [Real.norm_eq_abs, abs_of_nonneg, ha] using hsa
  have hnu : Summable fun n => ‖u n‖ := by
    simpa only [Real.norm_eq_abs, abs_of_nonneg, hun] using hsum
  have hind : HasSum (fun L : ℕ => if L = 0 then (1 : ℝ) else 0) 1 := hasSum_ite_eq 0 1
  have hconv : (fun L => ∑ k ∈ range (L + 1), a k * u (L - k))
      = fun L => u L - (if L = 0 then 1 else 0) := by
    funext L
    rw [hren L]
    ring
  have hcp : (∑' n, a n) * ∑' n, u n = ∑' L, ∑ k ∈ range (L + 1), a k * u (L - k) :=
    tsum_mul_tsum_eq_tsum_sum_range_of_summable_norm hna hnu
  rw [hconv, hsum.tsum_sub hind.summable, hind.tsum_eq] at hcp
  have hGne : ∑' n, u n ≠ 0 := ne_of_gt hGpos
  calc ∑' n, a n = (∑' n, a n) * (∑' n, u n) / ∑' n, u n := (mul_div_cancel_right₀ _ hGne).symm
    _ = (∑' n, u n - 1) / ∑' n, u n := by rw [hcp]
    _ = 1 - 1 / ∑' n, u n := by rw [sub_div, div_self hGne]

/-- **Transience**: the total first-return weight is strictly less than one. -/
theorem renewal_tsum_lt_one {u a : ℕ → ℝ} (hu0 : u 0 = 1) (ha0 : a 0 = 0)
    (ha : ∀ n, 0 ≤ a n) (hun : ∀ n, 0 ≤ u n)
    (hren : ∀ L, u L = (if L = 0 then 1 else 0) + ∑ k ∈ range (L + 1), a k * u (L - k))
    (hsum : Summable u) : ∑' n, a n < 1 := by
  rw [(renewal_tsum hu0 ha0 ha hun hren hsum).2]
  have hGpos : 0 < ∑' n, u n := hsum.tsum_pos hun 0 (by rw [hu0]; norm_num)
  have : 0 < 1 / ∑' n, u n := one_div_pos.mpr hGpos
  linarith

/-- A bound on the expected number of returns bounds the first-return mass: `Σ u ≤ 4 ⟹ Σ a ≤ 3/4`. -/
theorem renewal_tsum_le {u a : ℕ → ℝ} (hu0 : u 0 = 1) (ha0 : a 0 = 0)
    (ha : ∀ n, 0 ≤ a n) (hun : ∀ n, 0 ≤ u n)
    (hren : ∀ L, u L = (if L = 0 then 1 else 0) + ∑ k ∈ range (L + 1), a k * u (L - k))
    (hsum : Summable u) (hG : ∑' n, u n ≤ 4) : ∑' n, a n ≤ 3 / 4 := by
  rw [(renewal_tsum hu0 ha0 ha hun hren hsum).2]
  have hGpos : 0 < ∑' n, u n := hsum.tsum_pos hun 0 (by rw [hu0]; norm_num)
  have : 1 / 4 ≤ 1 / ∑' n, u n := one_div_le_one_div_of_le hGpos hG
  linarith

-- ==========================================
-- Pólya transience for the closure walk
-- ==========================================

/-- **Pólya transience for the closure walk.** Any first-return weights `a` in renewal relation
    with the `ℤ⁴` return weight have total mass at most `3/4`: at least a quarter of possibility
    never closes. With `a` the prime Kraft weights `I_L / 8^L` (supplied by the first-return
    bijection of `QLF_FirstReturn`) this is the substrate statement; numerically the mass is
    `0.1932`, so the true figure is `80.7 %`. -/
theorem polya_transience {a : ℕ → ℝ} (ha0 : a 0 = 0) (ha : ∀ n, 0 ≤ a n)
    (hren : ∀ L, returnWeight L
      = (if L = 0 then 1 else 0) + ∑ k ∈ range (L + 1), a k * returnWeight (L - k)) :
    ∑' n, a n ≤ 3 / 4 :=
  renewal_tsum_le returnWeight_zero ha0 ha returnWeight_nonneg hren
    returnWeight_summable returnWeight_tsum_le_four

/-- The same, as strict transience: the first-return mass is below one. -/
theorem polya_transience_lt_one {a : ℕ → ℝ} (ha0 : a 0 = 0) (ha : ∀ n, 0 ≤ a n)
    (hren : ∀ L, returnWeight L
      = (if L = 0 then 1 else 0) + ∑ k ∈ range (L + 1), a k * returnWeight (L - k)) :
    ∑' n, a n < 1 :=
  renewal_tsum_lt_one returnWeight_zero ha0 ha returnWeight_nonneg hren returnWeight_summable

end QLF.PolyaTransience
