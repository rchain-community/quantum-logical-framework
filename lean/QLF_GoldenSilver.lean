-- QLF_GoldenSilver.lean
-- The exact results of the golden/silver threads (ZFA_DNA.md §11–§14, Alpha_Residual.md §9m–§9n).
--
-- 1. EVERY LISTENING LANGUAGE CONTRIBUTES ONCE ⟹ THE CENSUS MODE (`listening_average`).
--    A listening language hears the always-heard primes plus any subset S of the composite
--    sign words W. Summed over every subset, each word is heard in exactly half of them:
--        2 · Σ_{S ⊆ W} Σ_{x ∈ S} b x = 2^|W| · Σ_{x ∈ W} b x.
--    So the uniform average over all languages is the midpoint of the irreducible and total
--    tails — the census mode w = 1/2 (alpha_sector_weights.py sec 2).
--
-- 2. THE GOLDEN SECTOR'S ALGEBRA (`catalan_inverse`, `catalan_at_bare_coupling`,
--    `golden_tail_eq`). With C = 1 + x C² (the Catalan series) and c = x C (one sign of prime),
--    C · (1 − x C) = 1, so 1/(1 − c)² = C²: the golden sector Σ_k (k+1) c^k counts Catalan(n+1)
--    (golden_zfa_dna.py sec 4). At the bare coupling x = 1/128, C = 64 − 8√62, and the golden
--    tail 1032062 − 131072√62 is 8192 × (the irreducible tail 126 − 16√62) − 130.
--
-- 3. THE SILVER INFLATION (`rho_pow_four`, `silver_comm_rho`, `silver_sq`). On Z⁴ = Z[ζ₈] the
--    45° rotation ρ has ρ⁴ = −1; the silver matrix S = 1 + ρ + ρ⁻¹ (the twist DNA t ↦ t⁻ t t⁺ on
--    counts) commutes with ρ and satisfies S² = 2S + 1, so every eigenvalue λ has λ² = 2λ + 1:
--    λ = 1 ± √2, the silver ratio (silver_zfa_dna.py).
--
-- Zero axioms.

import Mathlib.Algebra.BigOperators.Group.Finset.Powerset
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FinCases

namespace QLF

open Finset

-- ==========================================
-- 1. Every listening language contributes once
-- ==========================================

/-- **The census mode is every language.** Summed over all subsets `S` of a finite set of words
`W`, the heard weight `Σ_{x∈S} b x` totals `2^|W| / 2` times the full weight: each word lies in
exactly half of the subsets. -/
theorem listening_average {α : Type*} [DecidableEq α] (W : Finset α) (b : α → ℝ) :
    2 * ∑ S ∈ W.powerset, ∑ x ∈ S, b x = 2 ^ W.card * ∑ x ∈ W, b x := by
  refine Finset.induction_on W ?_ ?_
  · simp
  · intro a W ha ih
    have h : ∀ t ∈ W.powerset, ∑ x ∈ insert a t, b x = b a + ∑ x ∈ t, b x := by
      intro t ht
      exact Finset.sum_insert (fun hat => ha (Finset.mem_powerset.1 ht hat))
    rw [Finset.sum_powerset_insert ha, Finset.sum_congr rfl h, Finset.sum_add_distrib,
      Finset.sum_const, Finset.card_powerset, Finset.card_insert_of_notMem ha,
      Finset.sum_insert ha, nsmul_eq_mul]
    push_cast
    linear_combination 2 * ih

-- ==========================================
-- 2. The golden sector's algebra
-- ==========================================

/-- **The Catalan inverse.** If `C = 1 + x C²`, then `C (1 − x C) = 1`: with `c = x C` the one-sign
prime series, `1/(1 − c) = C`, so the golden sector `Σ_k (k+1) cᵏ = 1/(1 − c)² − 1 = C² − 1`,
whose coefficients are `Catalan(n+1)`. -/
theorem catalan_inverse {R : Type*} [CommRing R] (x C : R) (hC : C = 1 + x * C ^ 2) :
    C * (1 - x * C) = 1 := by
  linear_combination hC

/-- At the bare coupling `x = 1/128` the Catalan series takes the value `64 − 8√62`. -/
theorem catalan_at_bare_coupling :
    (64 - 8 * Real.sqrt 62 : ℝ) = 1 + (1 / 128) * (64 - 8 * Real.sqrt 62) ^ 2 := by
  have h : Real.sqrt 62 ^ 2 = 62 := Real.sq_sqrt (by norm_num)
  linear_combination (-1 / 2 : ℝ) * h

/-- **The golden tail** is `8192` times the irreducible tail, less `130`. -/
theorem golden_tail_eq :
    (1032062 - 131072 * Real.sqrt 62 : ℝ) = 8192 * (126 - 16 * Real.sqrt 62) - 130 := by
  ring

-- ==========================================
-- 3. The silver inflation on Z⁴ = Z[ζ₈]
-- ==========================================

/-- Multiplication by `ζ₈` on `Z⁴`: `e₀ ↦ e₁ ↦ e₂ ↦ e₃ ↦ −e₀`. -/
def rho : Matrix (Fin 4) (Fin 4) ℤ :=
  !![0, 0, 0, -1;
     1, 0, 0, 0;
     0, 1, 0, 0;
     0, 0, 1, 0]

/-- The silver inflation `1 + ζ + ζ⁻¹` — each twist flanked by its octagonal neighbours. -/
def silver : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 1, 0, -1;
     1, 1, 1, 0;
     0, 1, 1, 1;
     -1, 0, 1, 1]

/-- The eight twists are the eighth roots of unity: `ρ⁴ = −1`. -/
theorem rho_pow_four : rho * rho * rho * rho = -1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rho, Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply, Matrix.neg_apply]

/-- `S = 1 + ρ + ρ⁻¹`, with `ρ⁻¹ = −ρ³`. -/
theorem silver_eq : silver = 1 + rho - rho * rho * rho := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [silver, rho, Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply]

/-- The silver inflation respects the octagonal rotation. -/
theorem silver_comm_rho : silver * rho = rho * silver := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [silver, rho, Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply]

/-- **`S² = 2S + 1`**: every eigenvalue satisfies `λ² = 2λ + 1`, so `λ = 1 ± √2` — the silver ratio. -/
theorem silver_sq : silver * silver = silver + silver + 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [silver, Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply]

end QLF
