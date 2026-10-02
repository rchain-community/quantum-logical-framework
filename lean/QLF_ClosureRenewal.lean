import QLF_EdgeSign
import QLF_ClosureDepth

/-!
# QLF_ClosureRenewal — a closure keeps one sign of how it closed

Companion to `Memetics_QLF.md` §2 and `meme_closure_bits.py`.

A closure is a renewal event. If a twist history `h` is count-balanced, then for every
continuation `c`:

1. `h ++ c` is count-balanced iff `c` is (`countBalanced_append_iff`): the futures that
   close are the same whichever way `h` closed;
2. `fold (h ++ c) = σ(h) • fold c` with `σ(h) = connectionPhase h ∈ {1, −1}`
   (`closure_renewal`, `connectionPhase_sign`): the only trace of *which* way `h` took
   that reaches the future is one sign;
3. on the phase walk, a history back at balance contributes its depth only through a
   `max` (`maxExcursion_append_of_balanced`): a capacity-`R` listener hears `s ++ t`
   iff it hears both, so depth is held by the listening, not by the closed state.

So of the `log₂ W` bits needed to name one of the `W` ways a closure can close, the
closed history passes at most one forward. Any further record of how it closed has to
be held outside it. No axioms.
-/

namespace QLF.ClosureRenewal

open QLF QLF.PhaseRule QLF.EdgeSign QLF.ClosureDepth

-- ==========================================
-- 1. The futures that close do not depend on the way
-- ==========================================

/-- **Count balance is additive.** After a balanced `h`, a continuation closes the
    whole history iff it closes on its own. -/
theorem countBalanced_append_iff {h : List Twist} (hb : countBalanced h) (c : List Twist) :
    countBalanced (h ++ c) ↔ countBalanced c := by
  obtain ⟨h1, h2, h3, h4⟩ := hb
  simp only [countBalanced, List.count_append]
  constructor
  · rintro ⟨a, b, d, e⟩
    exact ⟨by omega, by omega, by omega, by omega⟩
  · rintro ⟨a, b, d, e⟩
    exact ⟨by omega, by omega, by omega, by omega⟩

-- ==========================================
-- 2. One sign survives
-- ==========================================

/-- The ordered fold is a monoid homomorphism `(List Twist, ++) → (M, *)`. -/
theorem fold_append (a b : List Twist) :
    twistMatrixFold (a ++ b) = twistMatrixFold a * twistMatrixFold b := by
  induction a with
  | nil => simp [twistMatrixFold]
  | cons t rest ih =>
    simp only [twistMatrixFold, List.cons_append, List.foldr_cons] at ih ⊢
    rw [ih, Matrix.mul_assoc]

/-- The closure sign is `±1`. -/
theorem connectionPhase_sign (ts : List Twist) :
    connectionPhase ts = 1 ∨ connectionPhase ts = -1 := by
  rw [connectionPhase_eq_predictedPhase]
  unfold predictedPhase
  rcases Nat.even_or_odd (negCount ts + invCount (axisWord ts)) with he | ho
  · left; exact he.neg_one_pow
  · right; exact ho.neg_one_pow

/-- **The renewal lemma.** After a closure `h`, the set of closing futures is the
    vacuum's, and every future's fold is the vacuum fold times the one sign `σ(h)`. -/
theorem closure_renewal {h : List Twist} (hb : countBalanced h) (c : List Twist) :
    (countBalanced (h ++ c) ↔ countBalanced c) ∧
      twistMatrixFold (h ++ c) = ((connectionPhase h : ℤ) : ℂ) • twistMatrixFold c := by
  refine ⟨countBalanced_append_iff hb c, ?_⟩
  rw [fold_append, fold_eq_connectionPhase hb, smul_mul_assoc, one_mul]

/-- **Two ways, one comparison.** Two closures of the same continuation differ only by
    the ratio of their signs: what a later observable can see of *which* way is the
    relative sign, which is the bi-local holonomy of `QLF_EdgeSign`. -/
theorem renewal_relative {h₁ h₂ : List Twist} (hb₁ : countBalanced h₁) (hb₂ : countBalanced h₂)
    (c : List Twist) (hs : connectionPhase h₁ = connectionPhase h₂) :
    twistMatrixFold (h₁ ++ c) = twistMatrixFold (h₂ ++ c) := by
  rw [(closure_renewal hb₁ c).2, (closure_renewal hb₂ c).2, hs]

-- ==========================================
-- 3. Depth is held by the listening
-- ==========================================

/-- The running maximum never falls below its starting value. -/
theorem exc_ge (c : Int) (t : TopoString) : c.natAbs ≤ exc c t := by
  cases t with
  | nil => simp [exc]
  | cons x t => simp only [exc]; exact le_max_left _ _

/-- The excursion of a concatenation splits at the junction. -/
theorem exc_append (c : Int) (s t : TopoString) :
    exc c (s ++ t) = max (exc c s) (exc (c + (s.map imb).sum) t) := by
  induction s generalizing c with
  | nil =>
    simp only [List.nil_append, exc, List.map_nil, List.sum_nil, add_zero]
    exact (max_eq_right (exc_ge c t)).symm
  | cons x s ih =>
    simp only [List.cons_append, exc, List.map_cons, List.sum_cons]
    rw [ih (c + imb x), add_assoc, max_assoc]

/-- **Depth after balance.** A history back at balance passes its depth to what follows
    only through a `max`. -/
theorem maxExcursion_append_of_balanced {s : TopoString} (hs : (s.map imb).sum = 0)
    (t : TopoString) :
    maxExcursion (s ++ t) = max (maxExcursion s) (maxExcursion t) := by
  unfold maxExcursion
  rw [exc_append, hs, add_zero]

end QLF.ClosureRenewal
