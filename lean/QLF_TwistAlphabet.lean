-- QLF_TwistAlphabet.lean
-- The 8-twist alphabet with explicit Pauli-matrix mapping.
--
-- Bridges the abstract PauliScalar group in QLF_Pauli.lean to the concrete
-- σ-matrix interpretation used at runtime in twist_core.py, the zfa-core
-- Rust kernel, and the browser app's zfa.ts. Proves each canonical
-- Hermitian-conjugate pair (`^v`, `v^`, `<>`, `><`, `/\`, `\/`, `+-`, `-+`)
-- folds, under its Pauli-matrix mapping, to the matrix `-I` — the image of
-- `PauliScalar.negOne` under the canonical embedding `PauliScalar → M`.
--
-- This closes the hardware-mapping caveat that QLF_Pauli.lean explicitly
-- flagged as open: "does NOT prove that arbitrary 8-twist sequences fold
-- to PauliScalars under the `^v ↔ ±σ_y, <> ↔ ∓σ_x, /\ ↔ ±σ_z, +- ↔ ±I`
-- mapping." The 8 Hermitian-pair products are exactly the ZFA-closed
-- length-2 sequences in the BFS-enumerated stable-history ensemble, all
-- of which are numerically verified to fold to `-I` in
-- `active_inference_vfe_demo.py`.
--
-- Pauli convention (from CLAUDE.md / Experimental_Consistency.md §2.1):
--   ^v ↔ ±σ_y       (^ = +σ_y, v = -σ_y)
--   <> ↔ ∓σ_x       (< = -σ_x, > = +σ_x)
--   /\ ↔ ±σ_z       (/ = +σ_z, \ = -σ_z)
--   +- ↔ ±I         (+ = +I,   - = -I)

import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.Data.Complex.Basic
import Mathlib.Data.ZMod.Basic
import QLF_Pauli

namespace QLF

/-- A 2×2 complex matrix. -/
abbrev M := Matrix (Fin 2) (Fin 2) ℂ

/-- The 8-twist alphabet. -/
inductive Twist where
  | up          -- ^   = +σ_y
  | down        -- v   = -σ_y
  | left        -- <   = -σ_x
  | right       -- >   = +σ_x
  | slash       -- /   = +σ_z
  | backslash   -- \   = -σ_z
  | plus        -- +   = +I
  | minus       -- -   = -I
deriving BEq, DecidableEq, Repr

-- Pauli matrices (local — BraKetRhoQuCalc.lean has analogues but private).

/-- σ_x = !![0, 1; 1, 0]. -/
noncomputable def σx : M := !![0, 1; 1, 0]

/-- σ_y = !![0, -i; i, 0]. -/
noncomputable def σy : M := !![0, -Complex.I; Complex.I, 0]

/-- σ_z = !![1, 0; 0, -1]. -/
noncomputable def σz : M := !![1, 0; 0, -1]

/-- Pauli-matrix mapping of the 8-twist alphabet. -/
noncomputable def Twist.toMatrix : Twist → M
  | up        => σy
  | down      => -σy
  | left      => -σx
  | right     => σx
  | slash     => σz
  | backslash => -σz
  | plus      => 1
  | minus     => -1

/-- The Hermitian-conjugate map on the 8-twist alphabet:
    `^ ↔ v`, `< ↔ >`, `/ ↔ \`, `+ ↔ -`. -/
def Twist.conj : Twist → Twist
  | up        => down
  | down      => up
  | left      => right
  | right     => left
  | slash     => backslash
  | backslash => slash
  | plus      => minus
  | minus     => plus

-- ==========================================
-- Pauli-square identities: σ_i · σ_i = I
-- ==========================================

theorem sigma_x_sq : σx * σx = (1 : M) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, Matrix.one_apply] <;>
    norm_num

theorem sigma_y_sq : σy * σy = (1 : M) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σy, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, Matrix.one_apply] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_z_sq : σz * σz = (1 : M) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σz, Matrix.mul_apply, Fin.sum_univ_two,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, Matrix.one_apply] <;>
    norm_num

-- ==========================================
-- Hermitian-pair folds to -I (= PauliScalar.negOne)
-- ==========================================

/-- The canonical embedding `PauliScalar → M` mapping each abstract
    scalar to its 2×2 matrix representation. -/
noncomputable def pauliScalarToMatrix : PauliScalar → M
  | PauliScalar.one    => 1
  | PauliScalar.i      => Complex.I • 1
  | PauliScalar.negOne => -1
  | PauliScalar.negI   => -(Complex.I • 1)

/-- **Every Hermitian-conjugate pair from the 8-twist alphabet folds to `-I`**
    under its Pauli-matrix mapping. Direct matrix-algebra computation, by
    case-analysis on the twist; each case reduces to a Pauli-square
    identity (or `1 · -1 = -1` for the gauge pair). -/
theorem hermitian_pair_folds_to_negI (t : Twist) :
    t.toMatrix * t.conj.toMatrix = -(1 : M) := by
  cases t
  case up =>
    show σy * (-σy) = -(1 : M)
    rw [mul_neg, sigma_y_sq]
  case down =>
    show (-σy) * σy = -(1 : M)
    rw [neg_mul, sigma_y_sq]
  case left =>
    show (-σx) * σx = -(1 : M)
    rw [neg_mul, sigma_x_sq]
  case right =>
    show σx * (-σx) = -(1 : M)
    rw [mul_neg, sigma_x_sq]
  case slash =>
    show σz * (-σz) = -(1 : M)
    rw [mul_neg, sigma_z_sq]
  case backslash =>
    show (-σz) * σz = -(1 : M)
    rw [neg_mul, sigma_z_sq]
  case plus =>
    show (1 : M) * (-1) = -(1 : M)
    rw [one_mul]
  case minus =>
    show (-(1 : M)) * (1 : M) = -(1 : M)
    rw [mul_one]

/-- **Hardware-mapping bridge**: every Hermitian-conjugate pair from the
    8-twist alphabet folds, under its Pauli-matrix mapping, to the image
    of `PauliScalar.negOne` under the canonical embedding
    `pauliScalarToMatrix : PauliScalar → M`.

    This closes the caveat that `QLF_Pauli.lean` explicitly flagged as
    open: arbitrary 8-twist Hermitian-conjugate sequences land in the
    Pauli scalar group at the matrix-multiplication level, not only at
    the abstract `PauliScalar` level. Combined with
    `pauli_closed_of_admissible_zfa` and `emergent_blanket_formation`,
    the runtime `is_zfa = is_count_balanced ∧ is_pauli_closed` check is
    now Lean-anchored end-to-end for Hermitian-pair atoms: count balance
    is preserved under concatenation, Pauli closure is preserved under
    concatenation (in the scalar group), AND each individual atom
    actually lands in the scalar group via its explicit σ-matrix
    mapping. -/
theorem hermitian_pair_is_pauli_scalar (t : Twist) :
    t.toMatrix * t.conj.toMatrix = pauliScalarToMatrix PauliScalar.negOne := by
  show t.toMatrix * t.conj.toMatrix = -(1 : M)
  exact hermitian_pair_folds_to_negI t

-- ==========================================
-- N-pair concatenation: the natural generalisation
-- ==========================================
--
-- The N=1 case (a single Hermitian pair folds to -I) is
-- `hermitian_pair_folds_to_negI` / `hermitian_pair_is_pauli_scalar`
-- above. The N>1 case (a concatenation of N Hermitian pairs) follows
-- by induction: each pair contributes -I, and (-1)^N is +I when N is
-- even and -I when N is odd.
--
-- Scope: this covers ZFA-closed sequences built BY CONCATENATION of
-- complete Hermitian pairs (e.g. `^v^v`, `<><>+-`, `^v/\+-`). It does
-- NOT cover cross-axis interleaving of partial pairs (e.g. `^<v>`,
-- where σ_y · -σ_x · -σ_y · σ_x still folds to -I but the algebra
-- requires the σ-product identities `σ_x σ_y = i σ_z` etc. and
-- doesn't reduce to a sequence of independent pair contributions).
-- That fuller bridge is a separate round.

/-- The matrix-product fold over a list of Hermitian-conjugate pairs.
    Each list element `t` represents the first member of its pair; the
    pair `(t, t.conj)` contributes `t.toMatrix * t.conj.toMatrix` to
    the fold. -/
noncomputable def concatPairsMatrixFold (ts : List Twist) : M :=
  ts.foldr (fun t acc => (t.toMatrix * t.conj.toMatrix) * acc) 1

/-- Each list element contributes `-1` (by `hermitian_pair_folds_to_negI`),
    so a list of `N` Hermitian pairs folds to `(-1 : M)^N`. -/
theorem concat_pairs_eq_neg_one_pow (ts : List Twist) :
    concatPairsMatrixFold ts = (-1 : M) ^ ts.length := by
  induction ts with
  | nil => simp [concatPairsMatrixFold]
  | cons t rest ih =>
    show (t.toMatrix * t.conj.toMatrix) * concatPairsMatrixFold rest
        = (-1 : M) ^ (rest.length + 1)
    rw [hermitian_pair_folds_to_negI t, ih, pow_succ']

/-- Concatenation of an EVEN number of Hermitian pairs folds to `+I`. -/
theorem concat_pairs_even (ts : List Twist) (h : Even ts.length) :
    concatPairsMatrixFold ts = (1 : M) := by
  rw [concat_pairs_eq_neg_one_pow]
  exact h.neg_one_pow

/-- Concatenation of an ODD number of Hermitian pairs folds to `-I`. -/
theorem concat_pairs_odd (ts : List Twist) (h : Odd ts.length) :
    concatPairsMatrixFold ts = -(1 : M) := by
  rw [concat_pairs_eq_neg_one_pow]
  exact h.neg_one_pow

/-- **N-pair concatenation closure**: the matrix product of any
    concatenation of N Hermitian-conjugate pairs from the 8-twist
    alphabet lands in the Pauli scalar group `{+I, -I}` — specifically
    `pauliScalarToMatrix PauliScalar.one` when N is even, and
    `pauliScalarToMatrix PauliScalar.negOne` when N is odd.

    The natural N-pair generalisation of `hermitian_pair_is_pauli_scalar`
    (the N=1 case). Closes the concatenation-only subset of the multi-
    pair hardware-mapping bridge — every concatenated-pair ZFA-closed
    sequence (like `^v^v`, `<><>+-`, `^v/\+-`) lands in the Pauli scalar
    group at the matrix level.

    Cross-axis interleaving of partial pairs (e.g., `^<v>`) is OUT of
    scope here; that case still produces a Pauli scalar at the matrix
    level (numerically verified in `active_inference_vfe_demo.py`) but
    the algebra requires the σ-product identities `σ_x σ_y = i σ_z`
    etc., not the pair-by-pair structure used here. -/
theorem concat_pairs_is_pauli_scalar (ts : List Twist) :
    ∃ p : PauliScalar, concatPairsMatrixFold ts = pauliScalarToMatrix p := by
  rcases Nat.even_or_odd ts.length with h | h
  · exact ⟨PauliScalar.one, by rw [concat_pairs_even ts h]; rfl⟩
  · exact ⟨PauliScalar.negOne, by rw [concat_pairs_odd ts h]; rfl⟩

-- ==========================================
-- Cross-axis σ-product identities: σ_i σ_j = ± i σ_k   (i ≠ j)
-- ==========================================
--
-- The 3 squares (σ_i² = I) are above. These are the 6 MIXED products —
-- the algebra the pair-by-pair `concat_pairs_*` theorems explicitly do
-- NOT use, and exactly what cross-axis interleaving (e.g. `^<v>`) needs.
-- Each lands in the `phase • axis-matrix` form `(±i) • σ_k` — the image
-- of a Pauli scalar phase times an axis matrix — which is the data the
-- general normal form will track. Same entrywise `Complex.ext`/`ring`
-- pattern as `sigma_y_sq`.

theorem sigma_xy : σx * σy = Complex.I • σz := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_yx : σy * σx = -(Complex.I • σz) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.neg_apply, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_yz : σy * σz = Complex.I • σx := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_zy : σz * σy = -(Complex.I • σx) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.neg_apply, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_zx : σz * σx = Complex.I • σy := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

theorem sigma_xz : σx * σz = -(Complex.I • σy) := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [σx, σy, σz, Matrix.mul_apply, Fin.sum_univ_two, Matrix.smul_apply,
      Matrix.neg_apply, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const, smul_eq_mul] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

-- ==========================================
-- Interleaved cross-axis closure (first N=2 case beyond concatenated pairs)
-- ==========================================

/-- Plain ordered matrix fold of a twist history: each twist via
    `Twist.toMatrix`, multiplied left-to-right (initialised at `I`).
    Unlike `concatPairsMatrixFold`, this takes a raw history, not a list
    of pair-leaders — so it sees cross-axis interleaving. -/
noncomputable def twistMatrixFold (ts : List Twist) : M :=
  ts.foldr (fun t acc => t.toMatrix * acc) 1

/-- **Interleaved cross-axis closure (N=2)** — the history `^<v>`
    (σ_y · −σ_x · −σ_y · σ_x) is count-balanced (`#^=#v`, `#<=#>`) but is
    NOT a concatenation of adjacent Hermitian pairs, so it is exactly the
    case `concat_pairs_is_pauli_scalar` flags as out of scope. It still
    folds to `-I` — the first cross-axis interleaving brought under proof,
    toward the general `count_balanced ⟹ Pauli scalar` theorem. Direct
    entrywise computation (the cross-axis algebra is `σ_yσ_x = -iσ_z` etc.,
    proved above). -/
theorem interleaved_xlvr_folds_to_negI :
    twistMatrixFold [Twist.up, Twist.left, Twist.down, Twist.right]
      = pauliScalarToMatrix PauliScalar.negOne := by
  simp only [twistMatrixFold, List.foldr_cons, List.foldr_nil, Matrix.mul_one]
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
    simp only [Twist.toMatrix, pauliScalarToMatrix, σx, σy, σz,
      Matrix.mul_apply, Fin.sum_univ_two, Matrix.neg_apply, Matrix.one_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.head_fin_const] <;>
    apply Complex.ext <;>
    simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
          Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
          Complex.ofReal_re, Complex.ofReal_im] <;>
    ring

-- ==========================================
-- Normal form: phase (PauliScalar) × axis (Klein four-group)  — Milestone 2
-- ==========================================
--
-- Every ordered fold of twist matrices equals `phase • axis-matrix`, with
-- `phase ∈ {±1, ±i}` and `axis ∈ {I, X, Y, Z}`. The phase absorbs the
-- ±i bookkeeping; the axis lives in the Klein four-group. This is the
-- general structure behind both the pair-by-pair and interleaved closures.
-- Step 1 (this section): the algebra — multiplying two normal forms, and
-- realising each twist as a normal form.

/-- `pauliScalarToMatrix p` left-multiplication, unfolded per scalar — the
    bridge from the abstract phase to a concrete `•`-scaling on matrices. -/
theorem psm_one_mul (A : M) : pauliScalarToMatrix PauliScalar.one * A = A := by
  show (1 : M) * A = A
  rw [one_mul]

theorem psm_negOne_mul (A : M) : pauliScalarToMatrix PauliScalar.negOne * A = -A := by
  show (-1 : M) * A = -A
  rw [neg_one_mul]

theorem psm_i_mul (A : M) : pauliScalarToMatrix PauliScalar.i * A = Complex.I • A := by
  show (Complex.I • (1 : M)) * A = Complex.I • A
  rw [smul_mul_assoc, one_mul]

theorem psm_negI_mul (A : M) : pauliScalarToMatrix PauliScalar.negI * A = -(Complex.I • A) := by
  show (-(Complex.I • (1 : M))) * A = -(Complex.I • A)
  rw [neg_mul, smul_mul_assoc, one_mul]

/-- The four Pauli axes. Their matrices generate the Pauli group; modulo
    phase they form the Klein four-group. -/
inductive Axis where
  | I | X | Y | Z
deriving DecidableEq, Repr

/-- Axis → its 2×2 matrix. -/
noncomputable def axisMatrix : Axis → M
  | Axis.I => 1
  | Axis.X => σx
  | Axis.Y => σy
  | Axis.Z => σz

/-- Klein four-group law on axes: `I` identity, every element self-inverse,
    `X·Y = Z`, `Y·Z = X`, `Z·X = Y` (and symmetric). -/
def axisMul : Axis → Axis → Axis
  | Axis.I, a       => a
  | a,       Axis.I => a
  | Axis.X, Axis.X  => Axis.I
  | Axis.Y, Axis.Y  => Axis.I
  | Axis.Z, Axis.Z  => Axis.I
  | Axis.X, Axis.Y  => Axis.Z
  | Axis.Y, Axis.X  => Axis.Z
  | Axis.Y, Axis.Z  => Axis.X
  | Axis.Z, Axis.Y  => Axis.X
  | Axis.Z, Axis.X  => Axis.Y
  | Axis.X, Axis.Z  => Axis.Y

/-- Phase cocycle for axis multiplication: the `±i` (or `±1`) factor by
    which `axisMatrix W * axisMatrix W'` differs from `axisMatrix (W·W')`.
    Reads off the σ-product identities (`σ_xσ_y = +iσ_z`, `σ_yσ_x = −iσ_z`, …). -/
def cocycle : Axis → Axis → PauliScalar
  | Axis.I, _       => PauliScalar.one
  | _,       Axis.I => PauliScalar.one
  | Axis.X, Axis.X  => PauliScalar.one
  | Axis.Y, Axis.Y  => PauliScalar.one
  | Axis.Z, Axis.Z  => PauliScalar.one
  | Axis.X, Axis.Y  => PauliScalar.i
  | Axis.Y, Axis.X  => PauliScalar.negI
  | Axis.Y, Axis.Z  => PauliScalar.i
  | Axis.Z, Axis.Y  => PauliScalar.negI
  | Axis.Z, Axis.X  => PauliScalar.i
  | Axis.X, Axis.Z  => PauliScalar.negI

/-- **Axis multiplication with cocycle phase** — the matrix product of two
    axis matrices is the cocycle phase times the Klein-product axis matrix.
    The 16 cases reduce to the 9 σ-product identities plus the identity
    rows. This is the algebraic crux of the normal form. -/
theorem axisMatrix_mul (W W' : Axis) :
    axisMatrix W * axisMatrix W'
      = pauliScalarToMatrix (cocycle W W') * axisMatrix (axisMul W W') := by
  cases W <;> cases W' <;>
    simp only [axisMatrix, cocycle, axisMul, pauliScalarToMatrix,
      sigma_x_sq, sigma_y_sq, sigma_z_sq, sigma_xy, sigma_yx, sigma_yz,
      sigma_zy, sigma_zx, sigma_xz, smul_mul_assoc, neg_mul, one_mul, mul_one]

/-- A normal form: a Pauli scalar phase together with an axis. -/
abbrev NF := PauliScalar × Axis

/-- Realise a normal form as a matrix: phase times axis matrix. -/
noncomputable def evalNF (s : NF) : M := pauliScalarToMatrix s.1 * axisMatrix s.2

/-- Each twist IS a normal form: a sign phase (`one`/`negOne`) and an axis.
    `^v ↔ Y`, `<> ↔ X`, `/\ ↔ Z`, `+- ↔ I`; the leading sign matches
    `Twist.toMatrix`. -/
def twistNF : Twist → NF
  | Twist.up        => (PauliScalar.one,    Axis.Y)
  | Twist.down      => (PauliScalar.negOne, Axis.Y)
  | Twist.left      => (PauliScalar.negOne, Axis.X)
  | Twist.right     => (PauliScalar.one,    Axis.X)
  | Twist.slash     => (PauliScalar.one,    Axis.Z)
  | Twist.backslash => (PauliScalar.negOne, Axis.Z)
  | Twist.plus      => (PauliScalar.one,    Axis.I)
  | Twist.minus     => (PauliScalar.negOne, Axis.I)

/-- Each twist's matrix is the realisation of its normal form. -/
theorem twist_toMatrix_eq_evalNF (t : Twist) : t.toMatrix = evalNF (twistNF t) := by
  cases t <;>
    simp only [Twist.toMatrix, twistNF, evalNF, axisMatrix, psm_one_mul, psm_negOne_mul]

-- ==========================================
-- Scalar-phase homomorphism & commutation  — Milestone 2 step 2
-- ==========================================

/-- Pauli scalar phase as a complex number (`i^k`). -/
def coePS : PauliScalar → ℂ
  | PauliScalar.one    => 1
  | PauliScalar.i      => Complex.I
  | PauliScalar.negOne => -1
  | PauliScalar.negI   => -Complex.I

/-- The matrix of a phase is that complex scalar times the identity. -/
theorem pauliScalarToMatrix_eq (p : PauliScalar) :
    pauliScalarToMatrix p = coePS p • (1 : M) := by
  cases p <;> simp [pauliScalarToMatrix, coePS, neg_smul, one_smul]

/-- `coePS` is multiplicative (the ℤ/4 phase group → ℂ). -/
theorem coePS_mul (p q : PauliScalar) : coePS (p * q) = coePS p * coePS q := by
  -- `*` is `PauliScalar.mul` by the instance; `change` exposes it (defeq) so
  -- `simp [PauliScalar.mul]` can iota-reduce the match on constructor args.
  change coePS (PauliScalar.mul p q) = coePS p * coePS q
  cases p <;> cases q <;>
    simp [coePS, PauliScalar.mul, Complex.I_mul_I, mul_neg, neg_mul, neg_neg, mul_one, one_mul]

/-- `pauliScalarToMatrix` is multiplicative: the four scalar matrices form a
    group under matrix multiplication, isomorphic to the `PauliScalar` ℤ/4. -/
theorem pauliScalarToMatrix_mul (p q : PauliScalar) :
    pauliScalarToMatrix p * pauliScalarToMatrix q = pauliScalarToMatrix (p * q) := by
  simp only [pauliScalarToMatrix_eq, smul_mul_assoc, one_mul, smul_smul, coePS_mul]

/-- A Pauli scalar matrix commutes with every 2×2 matrix (it is `c • I`). -/
theorem psm_comm (p : PauliScalar) (A : M) :
    A * pauliScalarToMatrix p = pauliScalarToMatrix p * A := by
  simp only [pauliScalarToMatrix_eq, mul_smul_comm, smul_mul_assoc, mul_one, one_mul]

-- ==========================================
-- Fold decomposition: every history = phase • axisMatrix(axisProd)  — Milestone 2 step 3
-- ==========================================

/-- Product of two scaled matrices: scalars and matrices factor cleanly
    (the matrices over ℂ form a ℂ-algebra). -/
theorem smul_mul_smul' (c d : ℂ) (X Y : M) : (c • X) * (d • Y) = (c * d) • (X * Y) := by
  rw [smul_mul_assoc, mul_smul_comm, smul_smul]

/-- A twist's matrix in `phase • axis` form (the `evalNF` recast via `coePS`). -/
theorem twist_toMatrix_smul (t : Twist) :
    t.toMatrix = coePS (twistNF t).1 • axisMatrix (twistNF t).2 := by
  simp only [twist_toMatrix_eq_evalNF, evalNF, pauliScalarToMatrix_eq, smul_mul_assoc, one_mul]

/-- `axisMatrix_mul` recast in `phase • axis` form. -/
theorem axisMatrix_mul_smul (W W' : Axis) :
    axisMatrix W * axisMatrix W' = coePS (cocycle W W') • axisMatrix (axisMul W W') := by
  rw [axisMatrix_mul]
  simp only [pauliScalarToMatrix_eq, smul_mul_assoc, one_mul]

/-- The axis product of a history: the Klein-group fold of each twist's axis. -/
def axisProd (ts : List Twist) : Axis :=
  ts.foldr (fun t acc => axisMul (twistNF t).2 acc) Axis.I

/-- **Normal-form decomposition** — every twist history's ordered matrix fold
    is a Pauli scalar phase times the axis matrix of its `axisProd`. Holds for
    ALL histories; count balance (next) forces the axis to `I`, leaving a pure
    scalar. The inductive step pushes the new twist's phase past the
    accumulated scalar (`psm_comm`/`smul`) and combines axes via
    `axisMatrix_mul`. -/
theorem nf_decomp (ts : List Twist) :
    ∃ p : PauliScalar, twistMatrixFold ts = coePS p • axisMatrix (axisProd ts) := by
  induction ts with
  | nil =>
    refine ⟨PauliScalar.one, ?_⟩
    simp [twistMatrixFold, axisProd, axisMatrix, coePS, one_smul]
  | cons t rest ih =>
    obtain ⟨p, hp⟩ := ih
    refine ⟨(twistNF t).1 * p * cocycle (twistNF t).2 (axisProd rest), ?_⟩
    show t.toMatrix * twistMatrixFold rest
        = coePS ((twistNF t).1 * p * cocycle (twistNF t).2 (axisProd rest))
          • axisMatrix (axisMul (twistNF t).2 (axisProd rest))
    rw [hp, twist_toMatrix_smul, smul_mul_smul', axisMatrix_mul_smul, smul_smul,
        ← coePS_mul, ← coePS_mul]

-- ==========================================
-- Count balance ⟹ trivial axis  — Milestone 2 step 4
-- ==========================================

/-- The Klein four-group of axes embedded in `(ZMod 2)²`: `I ↦ 0`, `X ↦ (1,0)`,
    `Y ↦ (0,1)`, `Z ↦ (1,1)`. Under this map `axisMul` becomes addition, so an
    axis is trivial iff its vector is zero. -/
def axisToVec : Axis → ZMod 2 × ZMod 2
  | Axis.I => (0, 0)
  | Axis.X => (1, 0)
  | Axis.Y => (0, 1)
  | Axis.Z => (1, 1)

/-- `axisToVec` is a group homomorphism `(Axis, axisMul) → ((ZMod 2)², +)`. -/
theorem axisToVec_mul (a b : Axis) :
    axisToVec (axisMul a b) = axisToVec a + axisToVec b := by
  cases a <;> cases b <;> decide

/-- The embedding is injective at the identity: zero vector ⟹ trivial axis. -/
theorem axisToVec_eq_zero {a : Axis} (h : axisToVec a = 0) : a = Axis.I := by
  cases a <;> first | rfl | exact absurd h (by decide)

/-- The axis vector of a history is the sum of its per-twist axis vectors
    (the homomorphism carried over the `axisProd` fold). -/
theorem axisToVec_axisProd (ts : List Twist) :
    axisToVec (axisProd ts) = (ts.map (fun t => axisToVec (twistNF t).2)).sum := by
  induction ts with
  | nil => simp [axisProd, axisToVec]
  | cons t rest ih =>
    have e : axisProd (t :: rest) = axisMul (twistNF t).2 (axisProd rest) := rfl
    rw [e, axisToVec_mul, ih, List.map_cons, List.sum_cons]

/-- The summed axis vector of a history, in terms of per-twist counts: the X
    component counts `< > / \`, the Y component counts `^ v / \` (since `/ \`
    carry the Z axis = X+Y). -/
theorem map_axisVec_sum (ts : List Twist) :
    (ts.map (fun t => axisToVec (twistNF t).2)).sum
      = ( (ts.count Twist.left : ZMod 2) + ts.count Twist.right
            + ts.count Twist.slash + ts.count Twist.backslash,
          (ts.count Twist.up : ZMod 2) + ts.count Twist.down
            + ts.count Twist.slash + ts.count Twist.backslash ) := by
  induction ts with
  | nil => simp [Prod.ext_iff]
  | cons t rest ih =>
    rw [List.map_cons, List.sum_cons, ih, Prod.ext_iff]
    cases t <;>
      refine ⟨?_, ?_⟩ <;>
      simp (config := { decide := true }) [twistNF, axisToVec, List.count_cons,
            Prod.fst_add, Prod.snd_add, Nat.cast_add, Nat.cast_one] <;>
      ring

/-- **Count balance** on a twist history: each Hermitian-conjugate pair occurs
    equally often — the discrete signed action vector vanishes (matches the
    runtime `calculate_action = 0` in `twist_core.py`). -/
def countBalanced (ts : List Twist) : Prop :=
  ts.count Twist.up = ts.count Twist.down ∧
  ts.count Twist.left = ts.count Twist.right ∧
  ts.count Twist.slash = ts.count Twist.backslash ∧
  ts.count Twist.plus = ts.count Twist.minus

/-- **Count balance forces the trivial axis.** Each axis occurs an even number
    of times (`#^=#v` ⇒ `σ_y` appears `2·#^` times, etc.), so the `(ZMod 2)²`
    axis-vector sum is zero, hence `axisProd = I`. -/
theorem axisProd_eq_I_of_countBalanced {ts : List Twist} (h : countBalanced ts) :
    axisProd ts = Axis.I := by
  apply axisToVec_eq_zero
  rw [axisToVec_axisProd, map_axisVec_sum]
  obtain ⟨hUD, hLR, hSB, _⟩ := h
  have key : ∀ a b c d : ZMod 2, a = b → c = d → a + b + c + d = 0 := by decide
  rw [Prod.ext_iff]
  refine ⟨key _ _ _ _ ?_ ?_, key _ _ _ _ ?_ ?_⟩
  · rw [hLR]
  · rw [hSB]
  · rw [hUD]
  · rw [hSB]

/-- **Pauli closure from count balance** — the keystone. Every count-balanced
    twist history folds, under the 8-twist Pauli mapping, to a Pauli scalar
    `{+I, -I, +iI, -iI}`. This closes the cross-axis-interleaving case that
    `concat_pairs_is_pauli_scalar` flagged as out of scope: it holds for ALL
    count-balanced histories, not only concatenations of adjacent Hermitian
    pairs. Runtime ZFA (`is_count_balanced ∧ is_pauli_closed`) is therefore
    Lean-anchored end-to-end — count balance alone implies Pauli closure. -/
theorem count_balanced_pauli_closed {ts : List Twist} (h : countBalanced ts) :
    ∃ p : PauliScalar, twistMatrixFold ts = pauliScalarToMatrix p := by
  obtain ⟨p, hp⟩ := nf_decomp ts
  refine ⟨p, ?_⟩
  rw [hp, axisProd_eq_I_of_countBalanced h]
  simp [axisMatrix, pauliScalarToMatrix_eq]

-- ==========================================
-- Twist-built closures are periodic (no chaos from twists alone)
-- ==========================================

/-- Every axis matrix squares to the identity. -/
theorem axisMatrix_sq (a : Axis) : axisMatrix a * axisMatrix a = 1 := by
  cases a
  · show (1 : M) * 1 = 1; exact mul_one 1
  · show σx * σx = 1; exact sigma_x_sq
  · show σy * σy = 1; exact sigma_y_sq
  · show σz * σz = 1; exact sigma_z_sq

/-- Every Pauli scalar phase is a fourth root of unity. -/
theorem coePS_pow_four (p : PauliScalar) : coePS p ^ 4 = 1 := by
  have hI : Complex.I ^ 4 = 1 := by
    rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, Complex.I_sq]; norm_num
  cases p
  · show (1 : ℂ) ^ 4 = 1; norm_num
  · show Complex.I ^ 4 = 1; exact hI
  · show (-1 : ℂ) ^ 4 = 1; norm_num
  · show (-Complex.I) ^ 4 = 1; rw [neg_pow, hI]; norm_num

/-- **Twist-built histories are periodic.** The ordered matrix fold of ANY
    twist history, closed or not, satisfies `W⁴ = I`: by `nf_decomp` it is a
    fourth-root-of-unity phase times an axis matrix that squares to `I`. So a
    closure built only from twists repeats exactly with period dividing 4 and
    cannot be chaotic, however many axes it uses. Decay or chaos needs
    something outside this finite group (a stretching step, a coupling to a
    continuum). See Lepton_Generations_Fourier.md §4. -/
theorem twist_fold_pow_four (ts : List Twist) : twistMatrixFold ts ^ 4 = 1 := by
  obtain ⟨p, hp⟩ := nf_decomp ts
  have hA : axisMatrix (axisProd ts) ^ 4 = 1 := by
    rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, pow_two (axisMatrix (axisProd ts)),
      axisMatrix_sq, one_pow]
  rw [hp, smul_pow, hA, coePS_pow_four, one_smul]

end QLF
