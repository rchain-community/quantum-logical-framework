import QLF_EdgeSign
import QLF_KraftMeasure

set_option linter.unusedVariables false

/-!
# QLF_StationaryPhase — the **signed** half of stationary action

[`QLF_StationaryAction`](QLF_StationaryAction.lean) proves the unsigned statement: the census
multiplicity is symmetric about balance, so its first variation vanishes there and balance is its
mode. That is the classical, Euclidean half. Feynman's argument is about the *signed* sum, where
amplitudes cancel away from the stationary path. This module proves the signed statement for the
actual QLF phase: the ℤ₂ holonomy of the edge-sign connection ([`QLF_EdgeSign`](QLF_EdgeSign.lean)),
which is defined for every history, open or closed.

The signed amplitude from `x` to `y` in `m` steps is

  `amp m x y = Σ_{|u| = m, u walks x → y} connAux x u`,

and from the origin this is exactly the sum of `connectionPhase` = `predictedPhase`
(`amp_origin`).

## What is proved

* **`amp_add`** (Chapman–Kolmogorov): a history splits at any step into two, and its phase factors
  (`connAux_append`).
* **`amp_swap`** (reversal): reversing a path and conjugating each twist runs it backwards. Each
  edge sign flips (`edgeSign_conj`: the connection never reads the coordinate being stepped), so
  `amp m y x = (−1)^m · amp m x y`. The signed transfer kernel is **anti-Hermitian** — the
  conjugate pairing again, now at the level of phases.
* **`return_amplitude_sum_sq`**: the signed return amplitude is a sum of squares,
  `amp (2m) x x = (−1)^m · Σ_y amp m x y ²`. Closure *is* the norm of the half-way amplitude.
* **`amp_closed_translate`**: closed loops carry the same phase wherever they start. Translating
  a path by `v` multiplies its phase by `sgn(shiftPar v u)`, and for a closed loop every axis is
  crossed an even number of times, so the factor is `1`.
* **`signed_mode_at_balance`**: `|amp (2m) 0 x| ≤ |amp (2m) 0 0|` for every endpoint `x`.
  Cauchy–Schwarz on the split plus translation. **The signed amplitude is largest at balance:**
  stationary phase, proved for the QLF phase itself.

* **`ways_mode_at_balance`** — the same argument with weight `1`: the *unsigned* census on all four
  axes peaks at balance, `W(2m) 0 x ≤ W(2m) 0 0`, and the closure count is a sum of squares
  (`ways_return_sum_sq`). This lifts `QLF_StationaryAction`'s one-axis result to `ℤ⁴`.

Checked numerically (exact integers, `stationary_phase_census.py`) to `L = 12`:
`amp (2m) 0 0 = −8, 120, −2144, 41896, …` and the maximum is unique at the origin. No axioms.
-/

namespace QLF.StationaryPhase

open QLF QLF.PhaseRule QLF.EdgeSign Finset

instance : Fintype Axis :=
  ⟨{Axis.I, Axis.X, Axis.Y, Axis.Z}, by intro x; cases x <;> decide⟩

/-- A lattice point of `ℤ⁴`. -/
abbrev Pos := Axis → ℤ

/-- The histories of length `m`. -/
def paths (m : ℕ) : Finset (List Twist) := words Twist m

/-- **The signed amplitude** from `x` to `y` in `m` steps: the sum of edge-sign phases. -/
def amp (m : ℕ) (x y : Pos) : ℤ :=
  ∑ u ∈ (paths m).filter (fun u => positionFrom x u = y), connAux x u

/-- The endpoints reachable from `x` in `m` steps. -/
def reachSet (m : ℕ) (x : Pos) : Finset Pos := (paths m).image (positionFrom x)

/-- From the origin the amplitude is the sum of `connectionPhase`, the certified phase rule. -/
theorem amp_origin (L : ℕ) (y : Pos) :
    amp L 0 y = ∑ u ∈ (paths L).filter (fun u => position u = y), connectionPhase u := rfl

-- ==========================================
-- Splitting a history
-- ==========================================

theorem positionFrom_append (u w : List Twist) : ∀ x : Pos,
    positionFrom x (u ++ w) = positionFrom (positionFrom x u) w := by
  induction u with
  | nil => intro x; rfl
  | cons t u ih => intro x; simp only [List.cons_append, positionFrom]; exact ih _

theorem connAux_append (u w : List Twist) : ∀ x : Pos,
    connAux x (u ++ w) = connAux x u * connAux (positionFrom x u) w := by
  induction u with
  | nil => intro x; simp [connAux, positionFrom]
  | cons t u ih =>
      intro x
      simp only [List.cons_append, connAux, positionFrom]
      rw [ih]
      ring

theorem sum_paths_append (m n : ℕ) (F : List Twist → ℤ) :
    ∑ ts ∈ paths (m + n), F ts = ∑ u ∈ paths m, ∑ w ∈ paths n, F (u ++ w) := by
  calc ∑ ts ∈ paths (m + n), F ts = ∑ p ∈ paths m ×ˢ paths n, F (p.1 ++ p.2) := by
        apply Finset.sum_nbij' (fun ts => (ts.take m, ts.drop m)) (fun p => p.1 ++ p.2)
        · intro ts hts
          simp only [paths, mem_words] at hts
          simp only [Finset.mem_product, paths, mem_words, List.length_take, List.length_drop, hts]
          omega
        · intro p hp
          simp only [Finset.mem_product, paths, mem_words] at hp
          simp only [paths, mem_words, List.length_append, hp.1, hp.2]
        · intro ts hts
          exact List.take_append_drop m ts
        · intro p hp
          simp only [Finset.mem_product, paths, mem_words] at hp
          exact Prod.ext (List.take_left' hp.1) (List.drop_left' hp.1)
        · intro ts hts
          show F ts = F (ts.take m ++ ts.drop m)
          rw [List.take_append_drop]
    _ = ∑ u ∈ paths m, ∑ w ∈ paths n, F (u ++ w) := Finset.sum_product _ _ _

/-- **Chapman–Kolmogorov.** An `(m+n)`-step amplitude is the `m`-step phase times the `n`-step
    amplitude from where it stopped. -/
theorem amp_add (m n : ℕ) (x z : Pos) :
    amp (m + n) x z = ∑ u ∈ paths m, connAux x u * amp n (positionFrom x u) z := by
  unfold amp
  rw [Finset.sum_filter, sum_paths_append]
  refine Finset.sum_congr rfl (fun u hu => ?_)
  rw [Finset.sum_filter, Finset.mul_sum]
  refine Finset.sum_congr rfl (fun w hw => ?_)
  simp only [positionFrom_append, connAux_append]
  split_ifs <;> ring

-- ==========================================
-- Reversal: the kernel is anti-Hermitian
-- ==========================================

/-- The conjugate twist: the same axis, the opposite sign. -/
def twistConj : Twist → Twist
  | Twist.up => Twist.down
  | Twist.down => Twist.up
  | Twist.left => Twist.right
  | Twist.right => Twist.left
  | Twist.slash => Twist.backslash
  | Twist.backslash => Twist.slash
  | Twist.plus => Twist.minus
  | Twist.minus => Twist.plus

theorem twistConj_twistConj (t : Twist) : twistConj (twistConj t) = t := by cases t <;> rfl

theorem axisOf_twistConj (t : Twist) : axisOf (twistConj t) = axisOf t := by cases t <;> rfl

theorem twistStep_twistConj (t : Twist) : twistStep (twistConj t) = -twistStep t := by
  cases t <;> decide

theorem stepPos_twistConj (x : Pos) (t : Twist) : stepPos (stepPos x t) (twistConj t) = x := by
  funext b
  simp only [stepPos, axisOf_twistConj, twistStep_twistConj]
  split_ifs <;> ring

/-- The connection at a step never reads the coordinate being stepped. -/
theorem edgeParity_stepPos_own (x : Pos) (t : Twist) :
    edgeParity (posMod (stepPos x t)) (axisOf t) = edgeParity (posMod x) (axisOf t) := by
  cases t <;> simp [edgeParity, posMod, stepPos, axisOf]

/-- **Stepping back flips the edge sign.** -/
theorem edgeSign_conj (x : Pos) (t : Twist) :
    edgeSign (stepPos x t) (twistConj t) = -edgeSign x t := by
  unfold edgeSign
  rw [axisOf_twistConj, twistStep_twistConj, edgeParity_stepPos_own]
  ring

/-- A path run backwards, each twist conjugated. -/
def revConj : List Twist → List Twist
  | [] => []
  | t :: u => revConj u ++ [twistConj t]

theorem length_revConj (u : List Twist) : (revConj u).length = u.length := by
  induction u with
  | nil => rfl
  | cons t u ih => simp [revConj, ih]

theorem revConj_append_single (u : List Twist) (t : Twist) :
    revConj (u ++ [t]) = twistConj t :: revConj u := by
  induction u with
  | nil => simp [revConj]
  | cons s u ih => simp [revConj, ih]

theorem revConj_revConj (u : List Twist) : revConj (revConj u) = u := by
  induction u with
  | nil => rfl
  | cons t u ih => simp [revConj, revConj_append_single, twistConj_twistConj, ih]

theorem positionFrom_revConj (u : List Twist) : ∀ x : Pos,
    positionFrom (positionFrom x u) (revConj u) = x := by
  induction u with
  | nil => intro x; rfl
  | cons t u ih =>
      intro x
      simp only [positionFrom, revConj]
      rw [positionFrom_append, ih]
      simp only [positionFrom]
      exact stepPos_twistConj x t

theorem connAux_revConj (u : List Twist) : ∀ x : Pos,
    connAux (positionFrom x u) (revConj u) = (-1) ^ u.length * connAux x u := by
  induction u with
  | nil => intro x; simp [connAux, revConj, positionFrom]
  | cons t u ih =>
      intro x
      simp only [positionFrom, revConj, connAux, List.length_cons]
      rw [connAux_append, ih, positionFrom_revConj]
      simp only [connAux]
      rw [edgeSign_conj]
      ring

/-- **The signed kernel is anti-Hermitian:** `amp m y x = (−1)^m · amp m x y`. -/
theorem amp_swap (m : ℕ) (x y : Pos) : amp m y x = (-1) ^ m * amp m x y := by
  unfold amp
  rw [Finset.mul_sum]
  apply Finset.sum_nbij' revConj revConj
  · intro u hu
    simp only [Finset.mem_filter, paths, mem_words] at hu ⊢
    refine ⟨by rw [length_revConj, hu.1], ?_⟩
    rw [← hu.2, positionFrom_revConj]
  · intro v hv
    simp only [Finset.mem_filter, paths, mem_words] at hv ⊢
    refine ⟨by rw [length_revConj, hv.1], ?_⟩
    rw [← hv.2, positionFrom_revConj]
  · intro u hu
    exact revConj_revConj u
  · intro v hv
    exact revConj_revConj v
  · intro u hu
    simp only [Finset.mem_filter, paths, mem_words] at hu
    have h := connAux_revConj u y
    rw [hu.2, hu.1] at h
    rw [h, ← mul_assoc, ← mul_pow]
    norm_num

-- ==========================================
-- The return amplitude is a sum of squares
-- ==========================================

/-- Grouping a path sum by endpoint. -/
theorem sum_by_endpoint (m : ℕ) (x : Pos) (h : Pos → ℤ) :
    ∑ u ∈ paths m, connAux x u * h (positionFrom x u) = ∑ y ∈ reachSet m x, amp m x y * h y := by
  rw [← Finset.sum_fiberwise_of_maps_to (s := paths m) (t := reachSet m x) (g := positionFrom x)
      (fun u hu => Finset.mem_image_of_mem _ hu)]
  refine Finset.sum_congr rfl (fun y hy => ?_)
  unfold amp
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl (fun u hu => ?_)
  rw [(Finset.mem_filter.1 hu).2]

/-- **The signed return amplitude is a sum of squares:**
    `amp (2m) x x = (−1)^m · Σ_y (amp m x y)²`. -/
theorem return_amplitude_sum_sq (m : ℕ) (x : Pos) :
    amp (m + m) x x = (-1) ^ m * ∑ y ∈ reachSet m x, amp m x y ^ 2 := by
  rw [amp_add]
  have h1 : ∀ u ∈ paths m, connAux x u * amp m (positionFrom x u) x
      = (-1) ^ m * (connAux x u * amp m x (positionFrom x u)) := by
    intro u hu
    rw [amp_swap m x (positionFrom x u)]
    ring
  rw [Finset.sum_congr rfl h1, ← Finset.mul_sum, sum_by_endpoint m x (fun y => amp m x y)]
  congr 1
  refine Finset.sum_congr rfl (fun y hy => ?_)
  show amp m x y * amp m x y = amp m x y ^ 2
  ring

-- ==========================================
-- Translation: closed loops carry the same phase anywhere
-- ==========================================

theorem stepPos_add (x v : Pos) (t : Twist) : stepPos (x + v) t = stepPos x t + v := by
  funext b
  simp only [stepPos, Pi.add_apply]
  split_ifs <;> ring

theorem positionFrom_add (v : Pos) (u : List Twist) : ∀ x : Pos,
    positionFrom (x + v) u = positionFrom x u + v := by
  induction u with
  | nil => intro x; rfl
  | cons t u ih =>
      intro x
      simp only [positionFrom]
      rw [stepPos_add, ih]

theorem positionFrom_shift (u : List Twist) (x : Pos) :
    positionFrom x u = positionFrom 0 u + x := by
  have h := positionFrom_add x u 0
  rwa [zero_add] at h

theorem posMod_add (x v : Pos) : posMod (x + v) = posMod x + posMod v := by
  funext b
  simp [posMod]

theorem edgeParity_add (p q : Axis → ZMod 2) (a : Axis) :
    edgeParity (p + q) a = edgeParity p a + edgeParity q a := by
  cases a <;> simp only [edgeParity, Pi.add_apply] <;> ring

theorem edgeSign_add (x v : Pos) (t : Twist) :
    edgeSign (x + v) t = edgeSign x t * sgn (edgeParity (posMod v) (axisOf t)) := by
  unfold edgeSign
  rw [posMod_add, edgeParity_add, sgn_add]
  ring

/-- The phase picked up by translating a path by `v`. -/
def shiftPar (v : Pos) : List Twist → ZMod 2
  | [] => 0
  | t :: u => edgeParity (posMod v) (axisOf t) + shiftPar v u

theorem sgn_zero : sgn 0 = 1 := by decide

theorem connAux_add (v : Pos) (u : List Twist) : ∀ x : Pos,
    connAux (x + v) u = connAux x u * sgn (shiftPar v u) := by
  induction u with
  | nil => intro x; simp [connAux, shiftPar, sgn]
  | cons t u ih =>
      intro x
      simp only [connAux, shiftPar]
      rw [stepPos_add, edgeSign_add, ih, sgn_add]
      ring

theorem connAux_shift (u : List Twist) (x : Pos) :
    connAux x u = connAux 0 u * sgn (shiftPar x u) := by
  have h := connAux_add x u 0
  rwa [zero_add] at h

/-- Whether a twist steps on the `X` axis, mod 2. -/
def xBit : Twist → ZMod 2
  | Twist.up => 0
  | Twist.down => 0
  | Twist.left => 1
  | Twist.right => 1
  | Twist.slash => 0
  | Twist.backslash => 0
  | Twist.plus => 0
  | Twist.minus => 0

/-- Whether a twist steps on the `Y` axis, mod 2. -/
def yBit : Twist → ZMod 2
  | Twist.up => 1
  | Twist.down => 1
  | Twist.left => 0
  | Twist.right => 0
  | Twist.slash => 0
  | Twist.backslash => 0
  | Twist.plus => 0
  | Twist.minus => 0

/-- The number of `X` steps, mod 2. -/
def xPar : List Twist → ZMod 2
  | [] => 0
  | t :: u => xBit t + xPar u

/-- The number of `Y` steps, mod 2. -/
def yPar : List Twist → ZMod 2
  | [] => 0
  | t :: u => yBit t + yPar u

theorem shiftPar_eq (v : Pos) (u : List Twist) :
    shiftPar v u = posMod v Axis.Y * xPar u + posMod v Axis.Z * (xPar u + yPar u) := by
  induction u with
  | nil => simp [shiftPar, xPar, yPar]
  | cons t u ih =>
      simp only [shiftPar, xPar, yPar]
      rw [ih]
      cases t <;> simp only [axisOf, edgeParity, xBit, yBit] <;> ring

theorem posMod_stepPos (x : Pos) (t : Twist) (b : Axis) :
    posMod (stepPos x t) b = posMod x b + (if axisOf t = b then 1 else 0) := by
  simp only [posMod, stepPos]
  split_ifs
  · rw [Int.cast_add, twistStep_cast]
  · rw [add_zero]

theorem xBit_eq (t : Twist) : (if axisOf t = Axis.X then (1 : ZMod 2) else 0) = xBit t := by
  cases t <;> decide

theorem yBit_eq (t : Twist) : (if axisOf t = Axis.Y then (1 : ZMod 2) else 0) = yBit t := by
  cases t <;> decide

theorem xPar_pos (u : List Twist) : ∀ x : Pos,
    posMod (positionFrom x u) Axis.X = posMod x Axis.X + xPar u := by
  induction u with
  | nil => intro x; simp [positionFrom, xPar]
  | cons t u ih =>
      intro x
      simp only [positionFrom, xPar]
      rw [ih, posMod_stepPos, xBit_eq]
      ring

theorem yPar_pos (u : List Twist) : ∀ x : Pos,
    posMod (positionFrom x u) Axis.Y = posMod x Axis.Y + yPar u := by
  induction u with
  | nil => intro x; simp [positionFrom, yPar]
  | cons t u ih =>
      intro x
      simp only [positionFrom, yPar]
      rw [ih, posMod_stepPos, yBit_eq]
      ring

theorem xPar_zero_of_closed (u : List Twist) (hc : positionFrom 0 u = 0) : xPar u = 0 := by
  have h := xPar_pos u 0
  rw [hc] at h
  linear_combination -h

theorem yPar_zero_of_closed (u : List Twist) (hc : positionFrom 0 u = 0) : yPar u = 0 := by
  have h := yPar_pos u 0
  rw [hc] at h
  linear_combination -h

theorem shiftPar_closed (u : List Twist) (x : Pos) (hc : positionFrom 0 u = 0) :
    shiftPar x u = 0 := by
  rw [shiftPar_eq, xPar_zero_of_closed u hc, yPar_zero_of_closed u hc]
  ring

/-- **Closed loops carry the same phase wherever they start.** -/
theorem amp_closed_translate (n : ℕ) (x : Pos) : amp n x x = amp n 0 0 := by
  unfold amp
  have hiff : ∀ u ∈ paths n, (positionFrom x u = x ↔ positionFrom 0 u = 0) := by
    intro u _
    rw [positionFrom_shift u x]
    constructor
    · intro h
      funext b
      have hb := congrFun h b
      simp only [Pi.add_apply, Pi.zero_apply] at hb ⊢
      linarith
    · intro h
      rw [h, zero_add]
  rw [Finset.filter_congr hiff]
  refine Finset.sum_congr rfl (fun u hu => ?_)
  have hc : positionFrom 0 u = 0 := (Finset.mem_filter.1 hu).2
  rw [connAux_shift u x, shiftPar_closed u x hc, sgn_zero, mul_one]

-- ==========================================
-- Stationary phase: the signed amplitude peaks at balance
-- ==========================================

/-- **Signed stationary phase.** No endpoint has a larger signed amplitude than the closure:
    `|amp (2m) 0 x| ≤ |amp (2m) 0 0|`. -/
theorem signed_mode_at_balance (m : ℕ) (x : Pos) :
    |amp (m + m) 0 x| ≤ |amp (m + m) 0 0| := by
  have hA : amp (m + m) 0 x = (-1) ^ m * ∑ y ∈ reachSet m 0, amp m 0 y * amp m x y := by
    rw [amp_add]
    have h1 : ∀ u ∈ paths m, connAux 0 u * amp m (positionFrom 0 u) x
        = (-1) ^ m * (connAux 0 u * amp m x (positionFrom 0 u)) := by
      intro u hu
      rw [amp_swap m x (positionFrom 0 u)]
      ring
    rw [Finset.sum_congr rfl h1, ← Finset.mul_sum, sum_by_endpoint m 0 (fun y => amp m x y)]
  have hpow : ((-1 : ℤ) ^ m) ^ 2 = 1 := by
    rw [sq, ← mul_pow]
    norm_num
  have hS0 : ∑ y ∈ reachSet m 0, amp m 0 y ^ 2 = (-1) ^ m * amp (m + m) 0 0 := by
    rw [return_amplitude_sum_sq m 0, ← mul_assoc, ← mul_pow]
    norm_num
  have hSx : ∑ y ∈ reachSet m x, amp m x y ^ 2 = (-1) ^ m * amp (m + m) 0 0 := by
    rw [← amp_closed_translate (m + m) x, return_amplitude_sum_sq m x, ← mul_assoc, ← mul_pow]
    norm_num
  have hsub : ∑ y ∈ reachSet m 0, amp m x y ^ 2 ≤ ∑ y ∈ reachSet m x, amp m x y ^ 2 := by
    calc ∑ y ∈ reachSet m 0, amp m x y ^ 2
        ≤ ∑ y ∈ reachSet m 0 ∪ reachSet m x, amp m x y ^ 2 :=
          Finset.sum_le_sum_of_subset_of_nonneg Finset.subset_union_left
            (fun y _ _ => sq_nonneg _)
      _ = ∑ y ∈ reachSet m x, amp m x y ^ 2 := by
          symm
          apply Finset.sum_subset Finset.subset_union_right
          intro y _ hy
          have hz : amp m x y = 0 := by
            unfold amp
            apply Finset.sum_eq_zero
            intro u hu
            exfalso
            apply hy
            rw [Finset.mem_filter] at hu
            rw [← hu.2]
            exact Finset.mem_image_of_mem _ hu.1
          rw [hz]
          ring
  have hCS := Finset.sum_mul_sq_le_sq_mul_sq (reachSet m 0) (fun y => amp m 0 y)
    (fun y => amp m x y)
  have hsq : amp (m + m) 0 x ^ 2 ≤ amp (m + m) 0 0 ^ 2 := by
    calc amp (m + m) 0 x ^ 2 = (∑ y ∈ reachSet m 0, amp m 0 y * amp m x y) ^ 2 := by
          rw [hA, mul_pow, hpow, one_mul]
      _ ≤ (∑ y ∈ reachSet m 0, amp m 0 y ^ 2) * ∑ y ∈ reachSet m 0, amp m x y ^ 2 := hCS
      _ ≤ (∑ y ∈ reachSet m 0, amp m 0 y ^ 2) * ∑ y ∈ reachSet m x, amp m x y ^ 2 :=
          mul_le_mul_of_nonneg_left hsub (Finset.sum_nonneg (fun y _ => sq_nonneg _))
      _ = ((-1) ^ m) ^ 2 * amp (m + m) 0 0 ^ 2 := by
          rw [hS0, hSx]
          ring
      _ = amp (m + m) 0 0 ^ 2 := by
          rw [hpow, one_mul]
  exact sq_le_sq.mp hsq

/-- **Stationary phase from ZFA — summary.** The signed closure amplitude is `(−1)^m` times a sum
    of squares, and no endpoint beats it. -/
theorem signed_stationary_phase (m : ℕ) :
    amp (m + m) 0 0 = (-1) ^ m * ∑ y ∈ reachSet m 0, amp m 0 y ^ 2 ∧
    ∀ x : Pos, |amp (m + m) 0 x| ≤ |amp (m + m) 0 0| :=
  ⟨return_amplitude_sum_sq m 0, signed_mode_at_balance m⟩

-- ==========================================
-- The unsigned count on all four axes (the classical half, on ℤ⁴)
-- ==========================================

/-- **The census multiplicity** from `x` to `y` in `m` steps: how many histories make the walk. -/
def ways (m : ℕ) (x y : Pos) : ℤ :=
  ∑ u ∈ (paths m).filter (fun u => positionFrom x u = y), (1 : ℤ)

theorem ways_add (m n : ℕ) (x z : Pos) :
    ways (m + n) x z = ∑ u ∈ paths m, ways n (positionFrom x u) z := by
  unfold ways
  rw [Finset.sum_filter, sum_paths_append]
  refine Finset.sum_congr rfl (fun u hu => ?_)
  rw [Finset.sum_filter]
  refine Finset.sum_congr rfl (fun w hw => ?_)
  simp only [positionFrom_append]

/-- Reversal is a bijection between walks `y → x` and walks `x → y`. -/
theorem ways_swap (m : ℕ) (x y : Pos) : ways m y x = ways m x y := by
  unfold ways
  apply Finset.sum_nbij' revConj revConj
  · intro u hu
    simp only [Finset.mem_filter, paths, mem_words] at hu ⊢
    refine ⟨by rw [length_revConj, hu.1], ?_⟩
    rw [← hu.2, positionFrom_revConj]
  · intro v hv
    simp only [Finset.mem_filter, paths, mem_words] at hv ⊢
    refine ⟨by rw [length_revConj, hv.1], ?_⟩
    rw [← hv.2, positionFrom_revConj]
  · intro u hu
    exact revConj_revConj u
  · intro v hv
    exact revConj_revConj v
  · intro u hu
    rfl

theorem ways_by_endpoint (m : ℕ) (x : Pos) (h : Pos → ℤ) :
    ∑ u ∈ paths m, h (positionFrom x u) = ∑ y ∈ reachSet m x, ways m x y * h y := by
  rw [← Finset.sum_fiberwise_of_maps_to (s := paths m) (t := reachSet m x) (g := positionFrom x)
      (fun u hu => Finset.mem_image_of_mem _ hu)]
  refine Finset.sum_congr rfl (fun y hy => ?_)
  unfold ways
  rw [Finset.sum_mul]
  refine Finset.sum_congr rfl (fun u hu => ?_)
  rw [(Finset.mem_filter.1 hu).2, one_mul]

/-- **The closure count is a sum of squares:** `W(2m) x x = Σ_y W(m) x y ²`. -/
theorem ways_return_sum_sq (m : ℕ) (x : Pos) :
    ways (m + m) x x = ∑ y ∈ reachSet m x, ways m x y ^ 2 := by
  rw [ways_add]
  have h1 : ∀ u ∈ paths m, ways m (positionFrom x u) x = ways m x (positionFrom x u) := by
    intro u hu
    exact ways_swap m x (positionFrom x u)
  rw [Finset.sum_congr rfl h1, ways_by_endpoint m x (fun y => ways m x y)]
  refine Finset.sum_congr rfl (fun y hy => ?_)
  show ways m x y * ways m x y = ways m x y ^ 2
  ring

theorem ways_closed_translate (n : ℕ) (x : Pos) : ways n x x = ways n 0 0 := by
  unfold ways
  have hiff : ∀ u ∈ paths n, (positionFrom x u = x ↔ positionFrom 0 u = 0) := by
    intro u _
    rw [positionFrom_shift u x]
    constructor
    · intro h
      funext b
      have hb := congrFun h b
      simp only [Pi.add_apply, Pi.zero_apply] at hb ⊢
      linarith
    · intro h
      rw [h, zero_add]
  rw [Finset.filter_congr hiff]

/-- **The classical half on ℤ⁴:** no displacement is realized in more ways than the closure,
    `W(2m) 0 x ≤ W(2m) 0 0`, on all four axes at once. -/
theorem ways_mode_at_balance (m : ℕ) (x : Pos) : ways (m + m) 0 x ≤ ways (m + m) 0 0 := by
  have hA : ways (m + m) 0 x = ∑ y ∈ reachSet m 0, ways m 0 y * ways m x y := by
    rw [ways_add]
    have h1 : ∀ u ∈ paths m, ways m (positionFrom 0 u) x = ways m x (positionFrom 0 u) := by
      intro u hu
      exact ways_swap m x (positionFrom 0 u)
    rw [Finset.sum_congr rfl h1, ways_by_endpoint m 0 (fun y => ways m x y)]
  have hS0 : ∑ y ∈ reachSet m 0, ways m 0 y ^ 2 = ways (m + m) 0 0 :=
    (ways_return_sum_sq m 0).symm
  have hSx : ∑ y ∈ reachSet m x, ways m x y ^ 2 = ways (m + m) 0 0 := by
    rw [← ways_closed_translate (m + m) x, ways_return_sum_sq m x]
  have hsub : ∑ y ∈ reachSet m 0, ways m x y ^ 2 ≤ ∑ y ∈ reachSet m x, ways m x y ^ 2 := by
    calc ∑ y ∈ reachSet m 0, ways m x y ^ 2
        ≤ ∑ y ∈ reachSet m 0 ∪ reachSet m x, ways m x y ^ 2 :=
          Finset.sum_le_sum_of_subset_of_nonneg Finset.subset_union_left
            (fun y _ _ => sq_nonneg _)
      _ = ∑ y ∈ reachSet m x, ways m x y ^ 2 := by
          symm
          apply Finset.sum_subset Finset.subset_union_right
          intro y _ hy
          have hz : ways m x y = 0 := by
            unfold ways
            apply Finset.sum_eq_zero
            intro u hu
            exfalso
            apply hy
            rw [Finset.mem_filter] at hu
            rw [← hu.2]
            exact Finset.mem_image_of_mem _ hu.1
          rw [hz]
          ring
  have hCS := Finset.sum_mul_sq_le_sq_mul_sq (reachSet m 0) (fun y => ways m 0 y)
    (fun y => ways m x y)
  have hsq : ways (m + m) 0 x ^ 2 ≤ ways (m + m) 0 0 ^ 2 := by
    calc ways (m + m) 0 x ^ 2 = (∑ y ∈ reachSet m 0, ways m 0 y * ways m x y) ^ 2 := by rw [hA]
      _ ≤ (∑ y ∈ reachSet m 0, ways m 0 y ^ 2) * ∑ y ∈ reachSet m 0, ways m x y ^ 2 := hCS
      _ ≤ (∑ y ∈ reachSet m 0, ways m 0 y ^ 2) * ∑ y ∈ reachSet m x, ways m x y ^ 2 :=
          mul_le_mul_of_nonneg_left hsub (Finset.sum_nonneg (fun y _ => sq_nonneg _))
      _ = ways (m + m) 0 0 ^ 2 := by rw [hS0, hSx]; ring
  have h0 : 0 ≤ ways (m + m) 0 0 := by
    unfold ways
    exact Finset.sum_nonneg (fun _ _ => zero_le_one)
  have habs := sq_le_sq.mp hsq
  rw [abs_of_nonneg h0] at habs
  exact le_trans (le_abs_self _) habs

end QLF.StationaryPhase
