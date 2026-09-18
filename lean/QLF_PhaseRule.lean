import QLF_TwistAlphabet
import Mathlib.Algebra.Ring.Parity      -- Even.neg_one_pow, Odd.neg_one_pow, Nat.even_or_odd
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
-- Narrow imports on purpose: `import Mathlib` maps ~6 GB of oleans per elaboration, which on a
-- 6.5 GB machine thrashes the page cache and turns a 20 s check into 30 min. Everything below
-- `QLF_TwistAlphabet` is already narrow (Matrix.Hermitian, Complex.Basic, ZMod.Basic).

set_option linter.unusedVariables false

/-!
# QLF_PhaseRule — **the phase of a way, computed**: `φ(h) = (−1)^{#neg} · (−1)^{inv(axis word)}`

[`count_balanced_pauli_closed`](QLF_TwistAlphabet.lean) says a balanced history folds to *some* Pauli
scalar; [`balanced_phase_is_real`](QLF_BalancedPhaseReal.lean) says that scalar is real, `±1`. Neither
says **which**. The census answered empirically — a two-factor rule with 0 counterexamples across all
**8,134,416** balanced histories of length ≤ 10 ([`Experimental_Consistency.md`](../Experimental_Consistency.md)) —
and it was recorded as *verified but not proven*, proven only for the pair sector where the axis word is
constant ([`QLF_PhaseAssignment`](QLF_PhaseAssignment.lean)).

This module proves it, and proves more than was asked:

> **`twist_fold_phase_normal_form`** — for **every** history, balanced or not,
> `fold h = (−1)^(#neg h + inv(axis h)) • canon(axis h)`,
> where `canon` is the sorted product `σx^{#X} σy^{#Y} σz^{#Z}`.
>
> **`phase_rule`** — when the history is count-balanced the sorted product is the identity, so
> `fold h = (−1)^(#neg h + inv(axis h)) • I` — the recorded rule, now a theorem.

## Why the general form comes for free

The two factors are independent and each is elementary once separated:

* **Sign content.** Each twist is `±` an axis matrix (`^ ↦ +σy`, `v ↦ −σy`, `< ↦ −σx`, …), so the signs
  pull straight out of the ordered product: `fold h = (−1)^{#neg} • (axis-only fold)`
  (`twistMatrixFold_eq`). Nothing about order enters here.
* **Order content.** Distinct Pauli matrices *anticommute* — `σyσx = −σxσy`, and likewise for the other
  two pairs (`anti_yx`, `anti_zx`, `anti_zy`, read off the σ-product identities already in
  [`QLF_TwistAlphabet`](QLF_TwistAlphabet.lean)). So sorting the axis word into `X…XY…YZ…Z` costs one
  `−1` per **inversion** — a pair of *distinct* letters standing out of order — and nothing else
  (`axisFold_eq_canon`). Equal letters commute with themselves, which is exactly why the inversion
  count, not the count of all distinct-letter pairs, is the right statistic.

Balance then kills the sorted remainder: `#X`, `#Y`, `#Z` are each even (`#< = #>` etc.), and `σ² = I`,
so `canon = I` (`canon_axisWord_balanced`). The `±i` of `μ₄` never appears because the sorted word is
empty modulo squares — an independent second route to `balanced_phase_is_real`, which drops out here as
`phase_rule_real` without the determinant argument.

The proof is by induction from the head of the history, and the inductive step is the whole content:
pushing one new axis matrix past the accumulated sorted product costs `(−1)` for each *smaller* letter
already there (`canon_cons_X`, `canon_cons_Y`, `canon_cons_Z`) — and the number of smaller letters
already there is precisely the number of inversions that letter creates (`countP_invPair_Y`,
`countP_invPair_Z`). That is the sign of the sorting permutation, assembled one letter at a time.

## What it buys

The phase of any way is now **computable without touching a matrix** (`predictedPhase`, an integer:
count the negative twists, count the inversions, take `(−1)` to that power). That is the missing input to
the signed-census → amplitude bridge: to add up how ways interfere, one no longer evaluates `2×2`
products per history but reads a combinatorial sign off the word. Per the working method, this is the
rule for **how ways add**, given that everything happens every way
([`Philosophy.md`](../Philosophy.md) §3a).

*A* proof, not *the* proof — a symplectic-form parity argument over `𝔽₂`, or the `nf_decomp` cocycle
bookkeeping, would likely serve too ([`Law_Of_Exceptions.md`](../Law_Of_Exceptions.md) §7).

No axioms.
-/

namespace QLF.PhaseRule

open QLF

-- ==========================================
-- Anticommutation: distinct Pauli matrices, and past powers
-- ==========================================

/-- `σy σx = −σx σy`. -/
theorem anti_yx : σy * σx = -(σx * σy) := by
  rw [sigma_yx, sigma_xy]

/-- `σz σx = −σx σz`. -/
theorem anti_zx : σz * σx = -(σx * σz) := by
  rw [sigma_zx, sigma_xz, neg_neg]

/-- `σz σy = −σy σz`. -/
theorem anti_zy : σz * σy = -(σy * σz) := by
  rw [sigma_zy, sigma_yz]

/-- `A ^ (n+1) = A * A ^ n` — the left-handed successor law, proved from `pow_succ` so no
    version-specific spelling is relied on. -/
private theorem pow_succ_left' (A : M) (n : ℕ) : A ^ (n + 1) = A * A ^ n := by
  induction n with
  | zero => simp
  | succ k ih => rw [pow_succ, ih, mul_assoc, ← pow_succ, ← ih]

/-- **Anticommuting past a power**: if `A` and `B` anticommute then moving `A` across `B ^ n` costs
    `(−1)^n`. This is the entire order-content of the phase rule, in one lemma. -/
private theorem anticomm_pow {A B : M} (h : A * B = -(B * A)) (n : ℕ) :
    A * B ^ n = ((-1 : ℂ) ^ n) • (B ^ n * A) := by
  induction n with
  | zero => simp
  | succ k ih =>
      have hsc : (-((-1 : ℂ) ^ k)) = (-1 : ℂ) ^ (k + 1) := by ring
      rw [pow_succ_left' B k, ← mul_assoc, h, neg_mul, mul_assoc, ih, mul_smul_comm,
        ← mul_assoc, ← neg_smul, hsc]

/-- `A * A = 1` makes every even power the identity. -/
private theorem pow_even_eq_one {A : M} (hA : A * A = 1) (k : ℕ) : A ^ (k + k) = 1 := by
  induction k with
  | zero => simp
  | succ k ih =>
      have h2 : (k + 1) + (k + 1) = (k + k) + 1 + 1 := by omega
      rw [h2, pow_succ, pow_succ, ih, one_mul, hA]

-- ==========================================
-- The axis word: its ordered fold, its sorted fold, its inversions
-- ==========================================

/-- The ordered matrix fold of a word of axes (the history with its signs stripped). -/
noncomputable def axisFold (w : List Axis) : M :=
  w.foldr (fun a acc => axisMatrix a * acc) 1

theorem axisFold_nil : axisFold [] = 1 := rfl

theorem axisFold_cons (a : Axis) (w : List Axis) :
    axisFold (a :: w) = axisMatrix a * axisFold w := rfl

/-- The **sorted** product `σx^p σy^q σz^r` — what any axis word becomes once its letters are put in
    order `X < Y < Z`. The gauge axis `I` contributes nothing. -/
noncomputable def canonPow (p q r : ℕ) : M := σx ^ p * (σy ^ q * σz ^ r)

/-- The sorted product belonging to a word: its letter multiplicities, in order. -/
noncomputable def canon (w : List Axis) : M :=
  canonPow (w.count Axis.X) (w.count Axis.Y) (w.count Axis.Z)

/-- Sort order on axes: `X < Y < Z`, with the gauge axis `I` outside the order entirely. -/
def ordv : Axis → ℕ
  | Axis.I => 0
  | Axis.X => 1
  | Axis.Y => 2
  | Axis.Z => 3

/-- **An inversion**: a later letter `b` that ought to precede the earlier letter `a`. Both must be
    genuine axes — the gauge axis `I` commutes with everything and never inverts. -/
def invPair : Axis → Axis → Bool
  | Axis.I, Axis.I => false
  | Axis.I, Axis.X => false
  | Axis.I, Axis.Y => false
  | Axis.I, Axis.Z => false
  | Axis.X, Axis.I => false
  | Axis.X, Axis.X => false
  | Axis.X, Axis.Y => false
  | Axis.X, Axis.Z => false
  | Axis.Y, Axis.I => false
  | Axis.Y, Axis.X => true
  | Axis.Y, Axis.Y => false
  | Axis.Y, Axis.Z => false
  | Axis.Z, Axis.I => false
  | Axis.Z, Axis.X => true
  | Axis.Z, Axis.Y => true
  | Axis.Z, Axis.Z => false

/-- `invPair` is exactly "out of order, both non-gauge" — the definition by cases agrees with the
    order `ordv`, so `invCount` below really is the inversion count of the word. -/
theorem invPair_iff (a b : Axis) :
    invPair a b = true ↔ (b ≠ Axis.I ∧ ordv b < ordv a) := by
  cases a <;> cases b <;> simp +decide [invPair, ordv]

/-- **The inversion count of an axis word** — the number of pairs standing out of order, i.e. the
    length of the permutation that sorts the word. `(−1)` to this power is the sign of that
    permutation. -/
def invCount : List Axis → ℕ
  | [] => 0
  | a :: w => w.countP (invPair a) + invCount w

theorem invCount_cons (a : Axis) (w : List Axis) :
    invCount (a :: w) = w.countP (invPair a) + invCount w := by
  simp [invCount]

/-- The gauge axis creates no inversions. -/
theorem countP_invPair_I (w : List Axis) : w.countP (invPair Axis.I) = 0 := by
  induction w with
  | nil => rfl
  | cons b w ih => cases b <;> simp +decide [List.countP_cons, invPair, ih]

/-- `X` is the least axis, so it is never inverted with anything after it. -/
theorem countP_invPair_X (w : List Axis) : w.countP (invPair Axis.X) = 0 := by
  induction w with
  | nil => rfl
  | cons b w ih => cases b <;> simp +decide [List.countP_cons, invPair, ih]

/-- A `Y` is inverted by every later `X`. -/
theorem countP_invPair_Y (w : List Axis) : w.countP (invPair Axis.Y) = w.count Axis.X := by
  induction w with
  | nil => rfl
  | cons b w ih =>
      cases b <;> simp +decide [List.countP_cons, List.count_cons, invPair, ih]

/-- A `Z` is inverted by every later `X` and every later `Y`. -/
theorem countP_invPair_Z (w : List Axis) :
    w.countP (invPair Axis.Z) = w.count Axis.X + w.count Axis.Y := by
  induction w with
  | nil => rfl
  | cons b w ih =>
      cases b <;>
        simp +decide [List.countP_cons, List.count_cons, invPair, ih] <;> omega

-- ==========================================
-- One letter at a time: the cost of pushing an axis into the sorted product
-- ==========================================

/-- An `X` slides in at the front for free — it is the least letter. -/
theorem canonPow_X (p q r : ℕ) : σx * canonPow p q r = canonPow (p + 1) q r := by
  show σx * (σx ^ p * (σy ^ q * σz ^ r)) = σx ^ (p + 1) * (σy ^ q * σz ^ r)
  rw [pow_succ_left' σx p, mul_assoc]

/-- A `Y` must cross the `X` block: `(−1)` for each `X` already there. -/
theorem canonPow_Y (p q r : ℕ) :
    σy * canonPow p q r = ((-1 : ℂ) ^ p) • canonPow p (q + 1) r := by
  show σy * (σx ^ p * (σy ^ q * σz ^ r)) = ((-1 : ℂ) ^ p) • (σx ^ p * (σy ^ (q + 1) * σz ^ r))
  rw [← mul_assoc σy (σx ^ p) (σy ^ q * σz ^ r), anticomm_pow anti_yx p, smul_mul_assoc,
    mul_assoc (σx ^ p) σy (σy ^ q * σz ^ r), ← mul_assoc σy (σy ^ q) (σz ^ r),
    ← pow_succ_left' σy q]

/-- A `Z` must cross both blocks: `(−1)` for each `X` and each `Y` already there. -/
theorem canonPow_Z (p q r : ℕ) :
    σz * canonPow p q r = ((-1 : ℂ) ^ (p + q)) • canonPow p q (r + 1) := by
  show σz * (σx ^ p * (σy ^ q * σz ^ r)) = ((-1 : ℂ) ^ (p + q)) • (σx ^ p * (σy ^ q * σz ^ (r + 1)))
  rw [← mul_assoc σz (σx ^ p) (σy ^ q * σz ^ r), anticomm_pow anti_zx p, smul_mul_assoc,
    mul_assoc (σx ^ p) σz (σy ^ q * σz ^ r), ← mul_assoc σz (σy ^ q) (σz ^ r),
    anticomm_pow anti_zy q, smul_mul_assoc, mul_smul_comm, smul_smul,
    mul_assoc (σy ^ q) σz (σz ^ r), ← pow_succ_left' σz r, ← pow_add]

theorem canon_cons_I (w : List Axis) : canon (Axis.I :: w) = canon w := by
  simp +decide [canon, List.count_cons]

theorem canon_cons_X (w : List Axis) : σx * canon w = canon (Axis.X :: w) := by
  have hc : canon (Axis.X :: w)
      = canonPow (w.count Axis.X + 1) (w.count Axis.Y) (w.count Axis.Z) := by
    simp +decide [canon, List.count_cons]
  rw [hc]
  exact canonPow_X _ _ _

theorem canon_cons_Y (w : List Axis) :
    σy * canon w = ((-1 : ℂ) ^ w.count Axis.X) • canon (Axis.Y :: w) := by
  have hc : canon (Axis.Y :: w)
      = canonPow (w.count Axis.X) (w.count Axis.Y + 1) (w.count Axis.Z) := by
    simp +decide [canon, List.count_cons]
  rw [hc]
  exact canonPow_Y _ _ _

theorem canon_cons_Z (w : List Axis) :
    σz * canon w = ((-1 : ℂ) ^ (w.count Axis.X + w.count Axis.Y)) • canon (Axis.Z :: w) := by
  have hc : canon (Axis.Z :: w)
      = canonPow (w.count Axis.X) (w.count Axis.Y) (w.count Axis.Z + 1) := by
    simp +decide [canon, List.count_cons]
  rw [hc]
  exact canonPow_Z _ _ _

/-- **The cost of one letter** — pushing an axis matrix into the sorted product costs exactly
    `(−1)` per inversion that letter creates with the rest of the word. -/
theorem axisMatrix_mul_canon (a : Axis) (w : List Axis) :
    axisMatrix a * canon w = ((-1 : ℂ) ^ (w.countP (invPair a))) • canon (a :: w) := by
  cases a
  · rw [countP_invPair_I, pow_zero, one_smul, canon_cons_I]
    simp [axisMatrix]
  · rw [countP_invPair_X, pow_zero, one_smul]
    exact canon_cons_X w
  · rw [countP_invPair_Y]
    exact canon_cons_Y w
  · rw [countP_invPair_Z]
    exact canon_cons_Z w

/-- **Sorting an axis word costs the sign of the sorting permutation** — for every word, ordered fold
    = `(−1)^{inversions}` times the sorted product. No balance hypothesis: this is the general fact. -/
theorem axisFold_eq_canon (w : List Axis) :
    axisFold w = ((-1 : ℂ) ^ invCount w) • canon w := by
  induction w with
  | nil => simp [axisFold, canon, canonPow, invCount]
  | cons a w ih =>
      rw [axisFold_cons, ih, mul_smul_comm, axisMatrix_mul_canon, smul_smul, ← pow_add,
        invCount_cons, Nat.add_comm (w.countP (invPair a)) (invCount w)]

-- ==========================================
-- From twists to axes: the sign content
-- ==========================================

/-- The four twists whose Pauli image carries a minus sign: `v ↦ −σy`, `< ↦ −σx`, `\ ↦ −σz`,
    `− ↦ −I`. -/
def isNegTwist : Twist → Bool
  | Twist.up        => false
  | Twist.down      => true
  | Twist.left      => true
  | Twist.right     => false
  | Twist.slash     => false
  | Twist.backslash => true
  | Twist.plus      => false
  | Twist.minus     => true

/-- How many sign-carrying twists a history contains — the first factor of the rule. -/
def negCount (ts : List Twist) : ℕ := ts.countP isNegTwist

/-- The axis a twist lives on: `^v ↦ Y`, `<> ↦ X`, `/\ ↦ Z`, `+− ↦ I` (gauge). -/
def axisOf : Twist → Axis
  | Twist.up        => Axis.Y
  | Twist.down      => Axis.Y
  | Twist.left      => Axis.X
  | Twist.right     => Axis.X
  | Twist.slash     => Axis.Z
  | Twist.backslash => Axis.Z
  | Twist.plus      => Axis.I
  | Twist.minus     => Axis.I

/-- This is the same axis assignment the normal form already used (`twistNF`). -/
theorem axisOf_eq_twistNF (t : Twist) : axisOf t = (twistNF t).2 := by
  cases t <;> rfl

/-- The axis word of a history: its twists with their signs forgotten. -/
def axisWord (ts : List Twist) : List Axis := ts.map axisOf

theorem axisWord_cons (t : Twist) (ts : List Twist) :
    axisWord (t :: ts) = axisOf t :: axisWord ts := rfl

/-- **Each twist is a sign times an axis matrix** — the sign factor separates cleanly from the
    order-sensitive part. -/
theorem twist_toMatrix_signed (t : Twist) :
    t.toMatrix = ((-1 : ℂ) ^ (if isNegTwist t then 1 else 0)) • axisMatrix (axisOf t) := by
  cases t <;>
    simp [Twist.toMatrix, axisOf, axisMatrix, isNegTwist, neg_smul, one_smul]

/-- **The signs pull out of the fold**: an ordered history fold is `(−1)^{#neg}` times the fold of its
    axis word. Order plays no part in this factor. -/
theorem twistMatrixFold_eq (ts : List Twist) :
    twistMatrixFold ts = ((-1 : ℂ) ^ negCount ts) • axisFold (axisWord ts) := by
  induction ts with
  | nil => simp [twistMatrixFold, axisFold, axisWord, negCount]
  | cons t ts ih =>
      have hfold : twistMatrixFold (t :: ts) = t.toMatrix * twistMatrixFold ts := rfl
      have hneg : negCount (t :: ts) = negCount ts + (if isNegTwist t then 1 else 0) := by
        simp [negCount, List.countP_cons]
      have hsc : ((-1 : ℂ) ^ (if isNegTwist t then 1 else 0)) * ((-1 : ℂ) ^ negCount ts)
          = (-1 : ℂ) ^ negCount (t :: ts) := by
        rw [hneg, pow_add]; ring
      rw [hfold, ih, twist_toMatrix_signed, axisWord_cons, axisFold_cons, smul_mul_smul', hsc]

-- ==========================================
-- The phase rule
-- ==========================================

/-- **The phase normal form — for every history, balanced or not.** The ordered Pauli fold of a twist
    history is `(−1)^(#neg + inversions of its axis word)` times the sorted product
    `σx^{#X} σy^{#Y} σz^{#Z}`. Both factors are read off the word; no matrix is multiplied. -/
theorem twist_fold_phase_normal_form (ts : List Twist) :
    twistMatrixFold ts
      = ((-1 : ℂ) ^ (negCount ts + invCount (axisWord ts))) • canon (axisWord ts) := by
  rw [twistMatrixFold_eq, axisFold_eq_canon, smul_smul, ← pow_add]

/-- The `X` letters of an axis word are exactly the `<` and `>` twists. -/
theorem count_axisWord_X (ts : List Twist) :
    (axisWord ts).count Axis.X = ts.count Twist.left + ts.count Twist.right := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      rw [axisWord_cons]
      cases t <;> simp +decide [axisOf, List.count_cons, ih] <;> omega

/-- The `Y` letters of an axis word are exactly the `^` and `v` twists. -/
theorem count_axisWord_Y (ts : List Twist) :
    (axisWord ts).count Axis.Y = ts.count Twist.up + ts.count Twist.down := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      rw [axisWord_cons]
      cases t <;> simp +decide [axisOf, List.count_cons, ih] <;> omega

/-- The `Z` letters of an axis word are exactly the `/` and `\` twists. -/
theorem count_axisWord_Z (ts : List Twist) :
    (axisWord ts).count Axis.Z = ts.count Twist.slash + ts.count Twist.backslash := by
  induction ts with
  | nil => rfl
  | cons t ts ih =>
      rw [axisWord_cons]
      cases t <;> simp +decide [axisOf, List.count_cons, ih] <;> omega

/-- Count balance makes every axis multiplicity even, so the sorted product is the identity. -/
theorem canon_axisWord_balanced {ts : List Twist} (h : countBalanced ts) :
    canon (axisWord ts) = 1 := by
  obtain ⟨hUD, hLR, hSB, _⟩ := h
  have hX : (axisWord ts).count Axis.X = ts.count Twist.right + ts.count Twist.right := by
    rw [count_axisWord_X, hLR]
  have hY : (axisWord ts).count Axis.Y = ts.count Twist.down + ts.count Twist.down := by
    rw [count_axisWord_Y, hUD]
  have hZ : (axisWord ts).count Axis.Z
      = ts.count Twist.backslash + ts.count Twist.backslash := by
    rw [count_axisWord_Z, hSB]
  simp only [canon, canonPow, hX, hY, hZ]
  rw [pow_even_eq_one sigma_x_sq, pow_even_eq_one sigma_y_sq, pow_even_eq_one sigma_z_sq,
    one_mul, one_mul]

/-- **The phase rule, proven.** A count-balanced history folds to
    `(−1)^(#neg twists + inversions of its axis word) · I` — the two-factor rule the census recorded
    with 0 counterexamples over 8,134,416 histories, now a theorem for *all* balanced histories at
    every length. -/
theorem phase_rule {ts : List Twist} (h : countBalanced ts) :
    twistMatrixFold ts = ((-1 : ℂ) ^ (negCount ts + invCount (axisWord ts))) • (1 : M) := by
  rw [twist_fold_phase_normal_form, canon_axisWord_balanced h]

/-- **The phase as a computable integer** — no matrices: count the negative twists, count the
    inversions of the axis word, raise `−1` to the sum. -/
def predictedPhase (ts : List Twist) : ℤ :=
  (-1) ^ (negCount ts + invCount (axisWord ts))

theorem predictedPhase_cast (ts : List Twist) :
    ((predictedPhase ts : ℤ) : ℂ) = (-1 : ℂ) ^ (negCount ts + invCount (axisWord ts)) := by
  first
    | (simp [predictedPhase]; done)
    | (push_cast [predictedPhase]; ring)

/-- **The integer rule computes the fold.** For a balanced history the `2×2` Pauli product equals the
    scalar `predictedPhase ts` — the census's prediction function, certified. -/
theorem fold_eq_predictedPhase {ts : List Twist} (h : countBalanced ts) :
    twistMatrixFold ts = ((predictedPhase ts : ℤ) : ℂ) • (1 : M) := by
  rw [phase_rule h, predictedPhase_cast]

/-- **Second route to `balanced_phase_is_real`.** The phase rule gives `±1` directly — the `±i` of
    `μ₄` cannot arise because the sorted remainder is the identity, not because of a determinant.
    Two independent derivations of one fact: multiplicity, not redundancy. -/
theorem phase_rule_real {ts : List Twist} (h : countBalanced ts) :
    twistMatrixFold ts = 1 ∨ twistMatrixFold ts = -1 := by
  rcases Nat.even_or_odd (negCount ts + invCount (axisWord ts)) with he | ho
  · left; rw [phase_rule h, he.neg_one_pow, one_smul]
  · right; rw [phase_rule h, ho.neg_one_pow, neg_one_smul]

/-- An even sign-plus-inversion count folds to `+I`. -/
theorem phase_rule_even {ts : List Twist} (h : countBalanced ts)
    (he : Even (negCount ts + invCount (axisWord ts))) : twistMatrixFold ts = 1 := by
  rw [phase_rule h, he.neg_one_pow, one_smul]

/-- An odd sign-plus-inversion count folds to `−I`. -/
theorem phase_rule_odd {ts : List Twist} (h : countBalanced ts)
    (ho : Odd (negCount ts + invCount (axisWord ts))) : twistMatrixFold ts = -1 := by
  rw [phase_rule h, ho.neg_one_pow, neg_one_smul]

/-- **Cross-check against the interleaved witness.** `^ < v >` — the cross-axis history that
    `concat_pairs_is_pauli_scalar` could not reach and `interleaved_xlvr_folds_to_negI` settled by a
    direct entrywise computation — is now settled by *counting*: two negative twists (`<`, `v`) and
    three inversions in the axis word `Y X Y X`, total 5, odd, so `−I`. Same answer, no matrix
    arithmetic. -/
theorem phase_of_interleaved_xlvr :
    twistMatrixFold [Twist.up, Twist.left, Twist.down, Twist.right] = -(1 : M) := by
  have hb : countBalanced [Twist.up, Twist.left, Twist.down, Twist.right] := by
    refine ⟨?_, ?_, ?_, ?_⟩ <;> decide
  have he : negCount [Twist.up, Twist.left, Twist.down, Twist.right]
      + invCount (axisWord [Twist.up, Twist.left, Twist.down, Twist.right]) = 5 := by
    decide
  rw [phase_rule hb, he, show ((-1 : ℂ) ^ 5) = -1 by norm_num, neg_smul, one_smul]

/-- **Established constructively, no axioms.** The two-factor phase rule
    `φ(h) = (−1)^{#neg} · (−1)^{inv(axis word)}` — recorded as verified-but-not-proven across
    8,134,416 balanced histories, proven previously only in the pair sector — is a theorem
    (`phase_rule`), and in the stronger unrestricted form `twist_fold_phase_normal_form` that drops the
    balance hypothesis and returns the sorted product `σx^{#X}σy^{#Y}σz^{#Z}` in its place. The two
    factors separate because signs pull out of a product regardless of order (`twistMatrixFold_eq`)
    while distinct Pauli matrices anticommute (`anti_yx`, `anti_zx`, `anti_zy`), so sorting the axis
    word costs exactly one `−1` per inversion (`axisFold_eq_canon`). Balance makes each axis
    multiplicity even, killing the sorted remainder (`canon_axisWord_balanced`), which re-derives
    `balanced_phase_is_real` by a second, independent route (`phase_rule_real`). **Consequence:** the
    phase carried by a way is computable from the word alone (`predictedPhase`,
    `fold_eq_predictedPhase`) — the input the signed-census → amplitude bridge needs, since adding up
    how ways interfere no longer requires evaluating one matrix product per history. -/
theorem phase_rule_summary : True := trivial

end QLF.PhaseRule
