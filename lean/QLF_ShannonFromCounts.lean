import Mathlib

/-!
# QLF_ShannonFromCounts — the `−Σ p log p` form is forced by counting ways (issue #142)

[`QLF_EntropyUniqueness`](QLF_EntropyUniqueness.lean) proved the **uniform** wing: an additive
information measure anchored on the generator is forced to be linear in the closure count,
`H s = |s| · c` — information *is* the log of the number of ways, up to the anchor. This module is
the **distributional** wing, and it needs no analysis: once information is `log ways`, the Shannon
form for a *non-uniform* partition is an identity, not a postulate.

## The setting

Outcomes `i` of a census carry **way-counts** `W i : ℕ` — how many ways the closure happens as
outcome `i` ([`Philosophy.md`](../Philosophy.md) §3a: *a closure's frequency is its multiplicity*).
The total is `W = Σ W i`, and the probabilities are the way-fractions `p i = W i / W`
(`QLF_BornProbability`: Born from counts). Nothing here is a probability postulate — the `p i` are
ratios of integers.

## The three results

* **`log_total_eq_expected_log_add_shannon`** — the way-count decomposition:
  `log W = Σ p i · log (W i) + (−Σ p i · log (p i))`.
  The Boltzmann entropy of the whole is the expected Boltzmann entropy of the cells **plus** the
  Shannon entropy of the partition. So `−Σ p log p` is exactly the information *in the partition* —
  the information that learning the cell buys when information is `log ways`. This is why the
  Shannon form is forced for non-uniform way-counts: it is the only thing `log W − E[log W i]` can be.
* **`shannon_uniform`** — with one way per cell, the partition entropy is `log n`: Shannon *is*
  Boltzmann on the uniform census, recovering the finite wing.
* **`shannon_indep_join`** — for independent censuses (way-counts multiply, `W i · V j`, the
  distributional face of `independent_join_multiplies` in
  [`QLF_CensusShannon`](QLF_CensusShannon.lean)) the partition entropies **add**. Ways multiply,
  information adds — the one fact the log form was chosen to respect, now checked on the general
  distribution rather than the uniform one.

## Honest scope

This is the derivation of the `−Σ p log p` form from counts — **given** that information is
`log ways` (the uniform wing). It is *not* the Faddeev / Baez–Fritz–Leinster uniqueness theorem
(that only this form satisfies the grouping rule with continuity): that is a statement about all
conceivable measures on a continuum of weights, and QLF's claim is the discrete one, that the
census forces the form the way it forces the count. No axioms.
-/

namespace QLF.ShannonFromCounts

variable {ι : Type*} [Fintype ι]

/-- The total number of ways, as a real. -/
noncomputable def total (W : ι → ℕ) : ℝ := ∑ i, (W i : ℝ)

/-- The way-fraction of outcome `i` — the census probability. -/
noncomputable def prob (W : ι → ℕ) (i : ι) : ℝ := (W i : ℝ) / total W

/-- The Shannon entropy of the way-count partition, `−Σ p log p`. -/
noncomputable def shannon (W : ι → ℕ) : ℝ := -∑ i, prob W i * Real.log (prob W i)

theorem total_pos [Nonempty ι] (W : ι → ℕ) (hpos : ∀ i, 0 < W i) : 0 < total W := by
  unfold total
  exact Finset.sum_pos (fun i _ => by exact_mod_cast hpos i) Finset.univ_nonempty

/-- The way-fractions sum to one. -/
theorem sum_prob [Nonempty ι] (W : ι → ℕ) (hpos : ∀ i, 0 < W i) : ∑ i, prob W i = 1 := by
  have htot : total W ≠ 0 := (total_pos W hpos).ne'
  unfold prob total at *
  rw [← Finset.sum_div]
  exact div_self htot

theorem prob_pos [Nonempty ι] (W : ι → ℕ) (hpos : ∀ i, 0 < W i) (i : ι) : 0 < prob W i := by
  unfold prob
  exact div_pos (by exact_mod_cast hpos i) (total_pos W hpos)

/-- **The way-count decomposition.** `log W = Σ pᵢ log Wᵢ + (−Σ pᵢ log pᵢ)`: the Boltzmann
    entropy of the whole is the expected Boltzmann entropy of the cells plus the Shannon entropy
    of the partition. The Shannon form is what is left over — forced, not chosen. -/
theorem log_total_eq_expected_log_add_shannon [Nonempty ι] (W : ι → ℕ) (hpos : ∀ i, 0 < W i) :
    Real.log (total W) = (∑ i, prob W i * Real.log (W i)) + shannon W := by
  have htot : 0 < total W := total_pos W hpos
  have hlog : ∀ i, Real.log (prob W i) = Real.log (W i) - Real.log (total W) := by
    intro i
    unfold prob
    exact Real.log_div (by exact_mod_cast (hpos i).ne') htot.ne'
  unfold shannon
  simp only [hlog, mul_sub, Finset.sum_sub_distrib]
  rw [← Finset.sum_mul, sum_prob W hpos, one_mul]
  ring

/-- **Uniform census: Shannon is Boltzmann.** One way per cell gives `−Σ p log p = log n`. -/
theorem shannon_uniform [Nonempty ι] : shannon (fun _ : ι => 1) = Real.log (Fintype.card ι) := by
  have h := log_total_eq_expected_log_add_shannon (fun _ : ι => 1) (fun _ => Nat.one_pos)
  have htot : total (fun _ : ι => 1) = Fintype.card ι := by
    unfold total
    simp
  rw [htot] at h
  simpa using h.symm

/-- Independent censuses: the joint way-count is the product. -/
def joinW {κ : Type*} (W : ι → ℕ) (V : κ → ℕ) : ι × κ → ℕ := fun x => W x.1 * V x.2

theorem total_join {κ : Type*} [Fintype κ] (W : ι → ℕ) (V : κ → ℕ) :
    total (joinW W V) = total W * total V := by
  unfold total joinW
  rw [Fintype.sum_prod_type, Finset.sum_mul_sum]
  simp [Nat.cast_mul]

theorem prob_join {κ : Type*} [Fintype κ] [Nonempty ι] [Nonempty κ]
    (W : ι → ℕ) (V : κ → ℕ) (hW : ∀ i, 0 < W i) (hV : ∀ j, 0 < V j) (x : ι × κ) :
    prob (joinW W V) x = prob W x.1 * prob V x.2 := by
  unfold prob
  rw [total_join]
  simp only [joinW, Nat.cast_mul]
  rw [div_mul_div_comm]

/-- The core algebra: for positive weights summing to one, the entropy of the product family is
    the sum of the entropies. -/
theorem neg_sum_prod_log_prod {κ : Type*} [Fintype κ]
    (a : ι → ℝ) (b : κ → ℝ) (ha : ∀ i, 0 < a i) (hb : ∀ j, 0 < b j)
    (ha1 : ∑ i, a i = 1) (hb1 : ∑ j, b j = 1) :
    -∑ x : ι × κ, (a x.1 * b x.2) * Real.log (a x.1 * b x.2)
      = (-∑ i, a i * Real.log (a i)) + (-∑ j, b j * Real.log (b j)) := by
  have hlog : ∀ x : ι × κ, Real.log (a x.1 * b x.2) = Real.log (a x.1) + Real.log (b x.2) :=
    fun x => Real.log_mul (ha x.1).ne' (hb x.2).ne'
  simp only [hlog, mul_add, Finset.sum_add_distrib]
  rw [Fintype.sum_prod_type, Fintype.sum_prod_type]
  dsimp only
  have h1 : ∑ i, ∑ j, a i * b j * Real.log (a i) = ∑ i, a i * Real.log (a i) := by
    have : ∀ i, ∑ j, a i * b j * Real.log (a i) = (a i * Real.log (a i)) * ∑ j, b j := by
      intro i
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      ring
    simp only [this, hb1, mul_one]
  have h2 : ∑ i, ∑ j, a i * b j * Real.log (b j) = ∑ j, b j * Real.log (b j) := by
    have : ∀ i, ∑ j, a i * b j * Real.log (b j) = a i * ∑ j, b j * Real.log (b j) := by
      intro i
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      ring
    simp only [this]
    rw [← Finset.sum_mul, ha1, one_mul]
  rw [h1, h2]
  ring

/-- **Independent joins: ways multiply, information adds.** The Shannon entropy of the joint
    census of two independent censuses is the sum — the distributional face of
    `independent_join_multiplies`, and the one property the logarithm exists to deliver. -/
theorem shannon_indep_join {κ : Type*} [Fintype κ] [Nonempty ι] [Nonempty κ]
    (W : ι → ℕ) (V : κ → ℕ) (hW : ∀ i, 0 < W i) (hV : ∀ j, 0 < V j) :
    shannon (joinW W V) = shannon W + shannon V := by
  unfold shannon
  simp only [prob_join W V hW hV]
  exact neg_sum_prod_log_prod (prob W) (prob V) (prob_pos W hW) (prob_pos V hV)
    (sum_prob W hW) (sum_prob V hV)

/-- **Status.** Given information = `log ways` (the uniform wing, `QLF_EntropyUniqueness`), the
    Shannon form for a non-uniform way-count partition is the identity
    `−Σ p log p = log W − Σ p log Wᵢ`, it reduces to `log n` on the uniform census, and it adds on
    independent joins. The form is derived from counting, not postulated. -/
theorem shannon_from_counts_summary : True := trivial

end QLF.ShannonFromCounts
