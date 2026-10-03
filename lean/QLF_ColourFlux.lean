import QLF_BaryonWinding

set_option linter.unusedVariables false

/-!
# QLF_ColourFlux — the colour flux from the axis cycle as a transport primitive

`QLF_BaryonWinding` derives the colour ℤ₃ as a symmetry: the cyclic relabeling `cycTwist` of the axes
preserves every baryon number (`baryon_cyc_invariant`). Fold transport alone can never supply the 2π/3
flux (`Carbon_Superconductivity.md` §24, N1–N2). **The framework extension** (§27) takes the axis cycle
`U = (1 − i(σ_x+σ_y+σ_z))/2` as a transport primitive.

The unit-determinant folds of the eight twists form the quaternion group Q₈, and `⟨Q₈, U⟩` is the binary
tetrahedral group, which is isomorphic to `SL(2, F₃)`. That isomorphism is checked exactly, on every product, in
[`colour_flux.py`](../colour_flux.py), and every isomorphism and base vector gives the same flux up to
`ω ↔ ω̄`. This module verifies the `F₃` side:

* `qMat` — the image of the eight twists in `SL(2, 3)`. It satisfies the quaternion relations (`q_sq`,
  `q_ijk`) and is injective (`qMat_injective`); reversal is negation (`qMat_rev`); and conjugation by the
  cycle matrix realises `cycTwist` (`qMat_cyc`).
* `colVec t = qMat t • (1,0)` — **the eight twists are the eight nonzero vectors of `F₃²`**
  (`colVec_ne_zero`, `colVec_injective`, `colVec_surjective`). Reversal is `v ↦ −v`, the gauge pair sits on
  the line fixed by the cycle, and the cycle permutes the `x, y, z` lines exactly as `cycTwist` does
  (`colVec_cyc`). The cycle is symplectic and of order 3.
* **The flux.** Twists on distinct axes have nonzero symplectic product (`flux_ne_zero`), and every pair has the
  **same** value, 1 (`flux_uniform`), whether spatial–spatial or gauge–spatial.
* In the Heisenberg group over `F₃²` (`Heis`), the group the Weyl displacements generate, the commutator of two
  displacements is the central phase `−⟨u,v⟩` (`heis_comm`). So a colour line around a plaquette on axes
  `a, b` picks up `ω^{−1}`: a flux of 2π/3, one orientation everywhere.

No axioms. The extension is the *rule* (a colour line is the Weyl qutrit over this `F₃²`); everything after it
is decided here.
-/

namespace QLF.ColourFlux

open QLF QLF.BaryonWinding

/-- Scalars of `F₃`. -/
abbrev F3 := Fin 3

/-- Vectors of the colour phase space `F₃²`. -/
abbrev V := F3 × F3

/-- A 2×2 matrix over `F₃`, entries `[[a, b], [c, d]]`. -/
structure MatF3 where
  a : F3
  b : F3
  c : F3
  d : F3
  deriving DecidableEq

def MatF3.mul (m n : MatF3) : MatF3 :=
  ⟨m.a * n.a + m.b * n.c, m.a * n.b + m.b * n.d, m.c * n.a + m.d * n.c, m.c * n.b + m.d * n.d⟩

def MatF3.neg (m : MatF3) : MatF3 := ⟨-m.a, -m.b, -m.c, -m.d⟩

def MatF3.det (m : MatF3) : F3 := m.a * m.d - m.b * m.c

def MatF3.act (m : MatF3) (v : V) : V := (m.a * v.1 + m.b * v.2, m.c * v.1 + m.d * v.2)

def MatF3.one : MatF3 := ⟨1, 0, 0, 1⟩

/-- Twist reversal (the Hermitian conjugate on each letter). -/
def revTwist : Twist → Twist
  | Twist.up        => Twist.down
  | Twist.down      => Twist.up
  | Twist.left      => Twist.right
  | Twist.right     => Twist.left
  | Twist.slash     => Twist.backslash
  | Twist.backslash => Twist.slash
  | Twist.plus      => Twist.minus
  | Twist.minus     => Twist.plus

/-- The axis line of a twist: 0 = gauge, 1 = x, 2 = y, 3 = z. -/
def axisLine : Twist → Fin 4
  | Twist.plus  | Twist.minus     => 0
  | Twist.right | Twist.left      => 1
  | Twist.up    | Twist.down      => 2
  | Twist.slash | Twist.backslash => 3

/-- The twists in `SL(2, F₃)`: the image of the unit-determinant folds `±I`, `±iσ_a`. -/
def qMat : Twist → MatF3
  | Twist.plus      => ⟨1, 0, 0, 1⟩
  | Twist.minus     => ⟨2, 0, 0, 2⟩
  | Twist.right     => ⟨0, 2, 1, 0⟩
  | Twist.left      => ⟨0, 1, 2, 0⟩
  | Twist.up        => ⟨2, 1, 1, 1⟩
  | Twist.down      => ⟨1, 2, 2, 2⟩
  | Twist.slash     => ⟨1, 1, 1, 2⟩
  | Twist.backslash => ⟨2, 2, 2, 1⟩

/-- The axis cycle in `SL(2, F₃)`: a transvection, the image of `U` up to sign. -/
def cycM : MatF3 := ⟨1, 2, 0, 1⟩

/-- Its inverse. -/
def cycMinv : MatF3 := ⟨1, 1, 0, 1⟩

/-- The colour vector of a twist: `qMat t` applied to the gauge base vector `(1, 0)`. -/
def colVec (t : Twist) : V := (qMat t).act (1, 0)

/-- The symplectic form on `F₃²`. -/
def symp (u v : V) : F3 := u.1 * v.2 - u.2 * v.1

def allTwists : List Twist :=
  [Twist.up, Twist.down, Twist.left, Twist.right, Twist.slash, Twist.backslash, Twist.plus, Twist.minus]

-- ===== the twists in SL(2,3): Q₈, reversal, and the cycle =====

theorem qMat_det (t : Twist) : (qMat t).det = 1 := by cases t <;> decide

/-- `i² = j² = k² = −1` with `i, j, k` the `x, y, z` twists and `−1` the `−` gauge twist. -/
theorem q_sq :
    (qMat Twist.right).mul (qMat Twist.right) = qMat Twist.minus ∧
    (qMat Twist.up).mul (qMat Twist.up) = qMat Twist.minus ∧
    (qMat Twist.slash).mul (qMat Twist.slash) = qMat Twist.minus := by decide

/-- `ijk = +1` for `i, j, k = iσ_x, iσ_y, iσ_z` (so `ij = −k`): with `q_sq`, the quaternion presentation of Q₈
    in the orientation `(iσ_x)(iσ_y) = −iσ_z`. -/
theorem q_ijk :
    ((qMat Twist.right).mul (qMat Twist.up)).mul (qMat Twist.slash) = qMat Twist.plus := by decide

theorem qMat_injective (t u : Twist) (h : qMat t = qMat u) : t = u := by
  cases t <;> cases u <;> first | rfl | exact absurd h (by decide)

theorem qMat_rev (t : Twist) : qMat (revTwist t) = (qMat t).neg := by cases t <;> decide

theorem cycM_inv : cycM.mul cycMinv = MatF3.one ∧ cycMinv.mul cycM = MatF3.one := by decide

theorem cycM_det : cycM.det = 1 := by decide

/-- **Conjugation by the cycle realises `cycTwist`** on the twists in `SL(2, 3)`. -/
theorem qMat_cyc (t : Twist) : (cycM.mul (qMat t)).mul cycMinv = qMat (cycTwist t) := by
  cases t <;> decide

-- ===== the eight twists are the eight nonzero vectors of F₃² =====

theorem colVec_ne_zero (t : Twist) : colVec t ≠ (0, 0) := by cases t <;> decide

theorem colVec_injective (t u : Twist) (h : colVec t = colVec u) : t = u := by
  cases t <;> cases u <;> first | rfl | exact absurd h (by decide)

theorem colVec_surjective : ∀ v : V, v ≠ (0, 0) → v ∈ allTwists.map colVec := by decide

theorem colVec_rev (t : Twist) : colVec (revTwist t) = -colVec t := by cases t <;> decide

/-- **The cycle permutes the colour vectors exactly as `cycTwist` permutes the twists.** -/
theorem colVec_cyc (t : Twist) : colVec (cycTwist t) = cycM.act (colVec t) := by cases t <;> decide

theorem cycM_fixes_gauge : cycM.act (colVec Twist.plus) = colVec Twist.plus := by decide

theorem cycM_order_three : ∀ v : V, cycM.act (cycM.act (cycM.act v)) = v := by decide

theorem cycM_symplectic : ∀ u v : V, symp (cycM.act u) (cycM.act v) = symp u v := by decide

-- ===== the flux =====

/-- **Distinct axes never commute in colour:** twists on different lines have nonzero symplectic product. -/
theorem flux_ne_zero (t u : Twist) (h : axisLine t ≠ axisLine u) : symp (colVec t) (colVec u) ≠ 0 := by
  cases t <;> cases u <;> first | exact absurd rfl h | decide

/-- **One orientation everywhere:** every positive-twist pair, spatial or gauge–spatial, has product 1. -/
theorem flux_uniform :
    symp (colVec Twist.right) (colVec Twist.up) = 1 ∧
    symp (colVec Twist.up) (colVec Twist.slash) = 1 ∧
    symp (colVec Twist.slash) (colVec Twist.right) = 1 ∧
    symp (colVec Twist.plus) (colVec Twist.right) = 1 ∧
    symp (colVec Twist.plus) (colVec Twist.up) = 1 ∧
    symp (colVec Twist.plus) (colVec Twist.slash) = 1 := by decide

-- ===== the Heisenberg group over F₃² (the Weyl displacements) =====

/-- An element `ω^k D(v)` of the Heisenberg group over `F₃²`. The product uses the cocycle `⟨u, v⟩` of the
    symmetric Weyl displacements, read off the explicit 3×3 matrices in `colour_flux.py`. -/
structure Heis where
  v : V
  k : F3
  deriving DecidableEq

def Heis.mul (x y : Heis) : Heis := ⟨x.v + y.v, x.k + y.k + symp x.v y.v⟩

/-- The displacement `D(v)`. -/
def disp (v : V) : Heis := ⟨v, 0⟩

/-- `D(−v)` is the inverse of `D(v)`, so a reversed twist undoes its step. -/
theorem disp_neg_inv : ∀ v : V, (disp v).mul (disp (-v)) = ⟨(0, 0), 0⟩ := by decide

/-- **The commutator of two displacements is the central phase `−⟨u, v⟩`.** -/
theorem heis_comm : ∀ u v : V,
    (((disp u).mul (disp v)).mul (disp (-u))).mul (disp (-v)) = ⟨(0, 0), -symp u v⟩ := by decide

/-- **The colour flux.** A colour line carried around the plaquette `t u t̄ ū` on two distinct axes
    returns with the scalar phase `ω^{−1}`: a 2π/3 flux, the same for every pair of axes. -/
theorem colour_plaquette (t u : Twist) (h : axisLine t ≠ axisLine u)
    (ht : t ∈ [Twist.right, Twist.up, Twist.slash, Twist.plus])
    (hu : u ∈ [Twist.right, Twist.up, Twist.slash, Twist.plus]) :
    (((disp (colVec t)).mul (disp (colVec u))).mul (disp (colVec (revTwist t)))).mul
      (disp (colVec (revTwist u))) = ⟨(0, 0), -symp (colVec t) (colVec u)⟩ := by
  rw [colVec_rev, colVec_rev]; exact heis_comm _ _

end QLF.ColourFlux
