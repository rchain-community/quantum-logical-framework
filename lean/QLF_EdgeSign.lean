import QLF_PhaseRule
import Mathlib

set_option linter.unusedVariables false

/-!
# QLF_EdgeSign — **the phase is a ℤ₂ connection on the closure walk**

[`QLF_PhaseRule`](QLF_PhaseRule.lean) proves the phase of a balanced history is
`(−1)^{#neg} · (−1)^{inv(axis word)}`, a statistic of the *whole word*: the inversion count looks
at every pair of letters. [`Closure_Walk.md`](../Closure_Walk.md) §2 claims it can be pushed onto
the **edges** of the walk — that the sign is local to the step being taken and the lattice point it
is taken from:

> **Edge-sign rule.** The step `x → x + s·e_a` from position `x ∈ ℤ⁴` carries the sign
> `s · (−1)^{ε}`, `ε = Σ_{spatial b ranked above a} x_b (mod 2)`; the gauge axis carries no
> inversion sign. The phase of a history is the product of its edge signs — its holonomy.

The point is the state the sign depends on. Adding a letter of axis `a` at the end of a word creates
one inversion for every earlier letter of an axis ranked above `a`; the number of earlier letters on
axis `b` has the parity of the *position* `x_b` (count `= pos + neg`, position `= pos − neg`). So the
increment is a function of the node the walker stands on, not of the path that brought it there —
which is what makes it a **connection** on the Cayley graph of `ℤ⁴`, and the phase its holonomy.

`closure_walk.py` verified the rule on all 195,416 closures to length 8. Here it is a theorem for
**every** history, balanced or not, and the balanced case then reads the fold off the walk:

* **`holonomy_eq_invCount`** — the walk's ℤ₂ holonomy from the origin is the inversion parity of
  the axis word. Proved by carrying the walker's *counts* alongside its *position* (they agree mod 2,
  `holAux_eq_cntAux`), and showing the count-walk accumulates exactly the inversions
  (`cntAux_eq_cross_add_invCount`, `cross_bump` — one new letter adds `countP (invPair a)`).
* **`connectionPhase_eq_predictedPhase`** — the integer product of edge signs along the walk equals
  `predictedPhase`, the certified two-factor rule, for every history.
* **`fold_eq_connectionPhase`** — for a balanced history the Pauli fold *is* `connectionPhase • I`.

And the flux the rule predicts, decided: the mixed spatial plaquette `^>v<` has holonomy `−1`, its
other orientation `^><v` is `+1`, the spatial-gauge plaquette `^+v−` is `+1`, and going round the
spatial plaquette twice is `+1` — spin-½ as a holonomy (`plaquette_yx`, `plaquette_twice`).

No axioms.
-/

namespace QLF.EdgeSign

open QLF QLF.PhaseRule

-- ==========================================
-- The walk on ℤ⁴
-- ==========================================

/-- The signed unit step of a twist along its own axis: `+1` for `^ > / +`, `−1` for `v < \ −`. -/
def twistStep (t : Twist) : ℤ := if isNegTwist t then -1 else 1

/-- Move the walker: the coordinate of the twist's axis changes by its step. -/
def stepPos (x : Axis → ℤ) (t : Twist) : Axis → ℤ :=
  fun b => if axisOf t = b then x b + twistStep t else x b

/-- The position after a history, walked from `x`. -/
def positionFrom (x : Axis → ℤ) : List Twist → Axis → ℤ
  | [] => x
  | t :: ts => positionFrom (stepPos x t) ts

/-- The signed action vector of a history: its endpoint on `ℤ⁴`, from the origin. -/
def position (ts : List Twist) : Axis → ℤ := positionFrom (fun _ => 0) ts

/-- A position read mod 2 — all the connection needs. -/
def posMod (x : Axis → ℤ) : Axis → ZMod 2 := fun b => (x b : ZMod 2)

-- ==========================================
-- The connection
-- ==========================================

/-- **The connection increment** at a node `x` (mod 2) for a step on axis `a`: the parity of the
    coordinates on the spatial axes ranked above `a` (`X < Y < Z`). A `Z` step and a gauge step add
    nothing — nothing is ranked above `Z`, and the gauge axis commutes with everything. -/
def edgeParity (x : Axis → ZMod 2) : Axis → ZMod 2
  | Axis.I => 0
  | Axis.X => x Axis.Y + x Axis.Z
  | Axis.Y => x Axis.Z
  | Axis.Z => 0

/-- The ℤ₂ holonomy accumulated by walking `ts` from position `x`. -/
def holAux (x : Axis → ℤ) : List Twist → ZMod 2
  | [] => 0
  | t :: ts => edgeParity (posMod x) (axisOf t) + holAux (stepPos x t) ts

/-- **The holonomy of a history**: the connection summed along its walk from the origin. -/
def holonomy (ts : List Twist) : ZMod 2 := holAux (fun _ => 0) ts

/-- `(−1)^p` for a parity `p`. -/
def sgn (p : ZMod 2) : ℤ := if p = 0 then 1 else -1

/-- **The edge sign** of the step `x → x + s·e_a`: `s · (−1)^ε`. -/
def edgeSign (x : Axis → ℤ) (t : Twist) : ℤ :=
  twistStep t * sgn (edgeParity (posMod x) (axisOf t))

/-- The product of edge signs along `ts`, walked from `x`. -/
def connAux (x : Axis → ℤ) : List Twist → ℤ
  | [] => 1
  | t :: ts => edgeSign x t * connAux (stepPos x t) ts

/-- **The connection phase of a history**: the product of its edge signs from the origin. -/
def connectionPhase (ts : List Twist) : ℤ := connAux (fun _ => 0) ts

-- ==========================================
-- The count-walk: the same walk with letter counts instead of positions
-- ==========================================

/-- Increment the count on axis `a`. -/
def bump (c : Axis → ℕ) (a : Axis) : Axis → ℕ := fun b => if a = b then c b + 1 else c b

/-- The connection increment read from counts: the number of earlier letters ranked above `a`. -/
def edgeCount (c : Axis → ℕ) : Axis → ℕ
  | Axis.I => 0
  | Axis.X => c Axis.Y + c Axis.Z
  | Axis.Y => c Axis.Z
  | Axis.Z => 0

/-- The count-walk's total, an integer to be read mod 2. -/
def cntAux (c : Axis → ℕ) : List Twist → ℕ
  | [] => 0
  | t :: ts => edgeCount c (axisOf t) + cntAux (bump c (axisOf t)) ts

/-- Inversions between a fixed prefix (given by its counts `c`) and the letters of `w`. -/
def cross (c : Axis → ℕ) : List Axis → ℕ
  | [] => 0
  | a :: w => edgeCount c a + cross c w

/-- One more earlier letter on axis `a` raises the increment of a later `a'` by one exactly when
    `(a, a')` is an inversion — the 16 cases of the order `X < Y < Z` with `I` outside it. -/
theorem edgeCount_bump (c : Axis → ℕ) (a a' : Axis) :
    edgeCount (bump c a) a' = edgeCount c a' + (if invPair a a' then 1 else 0) := by
  cases a <;> cases a' <;> simp +decide [edgeCount, bump, invPair] <;> omega

/-- Bumping the prefix by one letter `a` adds, across the word, the inversions `a` creates. -/
theorem cross_bump (c : Axis → ℕ) (a : Axis) (w : List Axis) :
    cross (bump c a) w = cross c w + w.countP (invPair a) := by
  induction w with
  | nil => simp [cross]
  | cons a' w ih =>
      simp only [cross, List.countP_cons]
      rw [ih, edgeCount_bump]
      omega

/-- **The count-walk accumulates the inversions**: from prefix counts `c`, walking `ts` adds the
    cross inversions with the prefix and the inversions inside `ts`. -/
theorem cntAux_eq_cross_add_invCount (c : Axis → ℕ) (ts : List Twist) :
    cntAux c ts = cross c (axisWord ts) + invCount (axisWord ts) := by
  induction ts generalizing c with
  | nil => simp [cntAux, cross, axisWord, invCount]
  | cons t ts ih =>
      rw [axisWord_cons, invCount_cons]
      simp only [cntAux, cross]
      rw [ih, cross_bump]
      omega

/-- An empty prefix creates no cross inversions. -/
theorem cross_zero (w : List Axis) : cross (fun _ => 0) w = 0 := by
  induction w with
  | nil => rfl
  | cons a w ih => cases a <;> simp [cross, edgeCount, ih]

/-- From the origin the count-walk is exactly the inversion count. -/
theorem cntAux_zero (ts : List Twist) : cntAux (fun _ => 0) ts = invCount (axisWord ts) := by
  rw [cntAux_eq_cross_add_invCount, cross_zero, zero_add]

-- ==========================================
-- Position ≡ count (mod 2): the walk and the count-walk agree
-- ==========================================

/-- Every step is `±1`, i.e. `1` mod 2. -/
theorem twistStep_cast (t : Twist) : ((twistStep t : ℤ) : ZMod 2) = 1 := by
  cases t <;> simp [twistStep, isNegTwist] <;> decide

/-- When positions and counts agree mod 2, so do the two increments. -/
theorem edgeParity_eq_edgeCount (x : Axis → ℤ) (c : Axis → ℕ)
    (hx : ∀ b, (x b : ZMod 2) = (c b : ZMod 2)) (a : Axis) :
    edgeParity (posMod x) a = (edgeCount c a : ZMod 2) := by
  cases a <;> simp [edgeParity, edgeCount, posMod, hx]

/-- The agreement mod 2 survives a step: position moves by `±1`, count by `1`. -/
theorem stepPos_bump_parity (x : Axis → ℤ) (c : Axis → ℕ)
    (hx : ∀ b, (x b : ZMod 2) = (c b : ZMod 2)) (t : Twist) (b : Axis) :
    ((stepPos x t b : ℤ) : ZMod 2) = ((bump c (axisOf t) b : ℕ) : ZMod 2) := by
  simp only [stepPos, bump]
  split_ifs with h
  · push_cast
    rw [hx b, twistStep_cast]
  · exact hx b

/-- **The walk's holonomy is the count-walk's total**, whenever the walker's position and the
    prefix counts agree mod 2. -/
theorem holAux_eq_cntAux (ts : List Twist) : ∀ (x : Axis → ℤ) (c : Axis → ℕ),
    (∀ b, (x b : ZMod 2) = (c b : ZMod 2)) → holAux x ts = (cntAux c ts : ZMod 2) := by
  induction ts with
  | nil => intro x c hx; simp [holAux, cntAux]
  | cons t ts ih =>
      intro x c hx
      simp only [holAux, cntAux]
      push_cast
      rw [edgeParity_eq_edgeCount x c hx, ih (stepPos x t) (bump c (axisOf t)) (stepPos_bump_parity x c hx t)]

/-- **The holonomy is the inversion parity.** The connection summed along the walk from the origin
    equals the inversion count of the axis word, mod 2 — for every history. -/
theorem holonomy_eq_invCount (ts : List Twist) :
    holonomy ts = (invCount (axisWord ts) : ZMod 2) := by
  unfold holonomy
  rw [holAux_eq_cntAux ts (fun _ => 0) (fun _ => 0) (fun b => by simp), cntAux_zero]

-- ==========================================
-- From parity to sign
-- ==========================================

theorem sgn_add (p q : ZMod 2) : sgn (p + q) = sgn p * sgn q := by
  revert p q; decide

theorem sgn_one : sgn 1 = -1 := by decide

/-- `sgn` of a natural number's parity is `(−1)` to that number. -/
theorem sgn_natCast (n : ℕ) : sgn (n : ZMod 2) = (-1 : ℤ) ^ n := by
  induction n with
  | zero => simp [sgn]
  | succ n ih => rw [Nat.cast_succ, sgn_add, ih, sgn_one, pow_succ]

/-- The twist's own sign is `(−1)` to its negativity. -/
theorem twistStep_eq_pow (t : Twist) :
    twistStep t = (-1 : ℤ) ^ (if isNegTwist t then 1 else 0) := by
  cases t <;> simp [twistStep, isNegTwist]

/-- The product of edge signs factors as the sign content times the holonomy's sign. -/
theorem connAux_eq (ts : List Twist) : ∀ x : Axis → ℤ,
    connAux x ts = (-1 : ℤ) ^ negCount ts * sgn (holAux x ts) := by
  induction ts with
  | nil => intro x; simp [connAux, negCount, holAux, sgn]
  | cons t ts ih =>
      intro x
      simp only [connAux, edgeSign, holAux, negCount, List.countP_cons]
      rw [ih, sgn_add, twistStep_eq_pow, pow_add]
      simp only [negCount] at *
      ring

/-- **The edge-sign rule computes the phase rule.** For every history, the product of the edge
    signs along its walk equals `predictedPhase` — `(−1)^{#neg + inv}`. -/
theorem connectionPhase_eq_predictedPhase (ts : List Twist) :
    connectionPhase ts = predictedPhase ts := by
  have hh : holAux (fun _ => 0) ts = (invCount (axisWord ts) : ZMod 2) := holonomy_eq_invCount ts
  unfold connectionPhase predictedPhase
  rw [connAux_eq, hh, sgn_natCast, ← pow_add]

/-- **The fold is the holonomy.** For a balanced history the Pauli product is the scalar
    `connectionPhase ts` — the phase read off the walk's edges, one step at a time. -/
theorem fold_eq_connectionPhase {ts : List Twist} (h : countBalanced ts) :
    twistMatrixFold ts = ((connectionPhase ts : ℤ) : ℂ) • (1 : M) := by
  rw [connectionPhase_eq_predictedPhase]
  exact fold_eq_predictedPhase h

-- ==========================================
-- The flux, decided
-- ==========================================

/-- The mixed spatial plaquette `^>v<` — `Y, X` axes — has holonomy `−1`: π flux. -/
theorem plaquette_yx :
    connectionPhase [Twist.up, Twist.right, Twist.down, Twist.left] = -1 := by decide

/-- The same square traversed as `^><v` is `+1`: the sign is the order, not the endpoint. -/
theorem plaquette_yx_other_order :
    connectionPhase [Twist.up, Twist.right, Twist.left, Twist.down] = 1 := by decide

/-- A spatial–gauge plaquette `^+v−` carries no flux. -/
theorem plaquette_gauge :
    connectionPhase [Twist.up, Twist.plus, Twist.down, Twist.minus] = 1 := by decide

/-- Round the spatial plaquette twice: `+1`. One turn `−1`, two turns `+1` — spin-½ as a holonomy. -/
theorem plaquette_twice :
    connectionPhase [Twist.up, Twist.right, Twist.down, Twist.left,
                     Twist.up, Twist.right, Twist.down, Twist.left] = 1 := by decide

end QLF.EdgeSign
