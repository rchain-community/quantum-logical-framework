import QLF_Handedness
import QLF_NoTimeLoops

set_option linter.unusedVariables false

/-!
# QLF_HandedLoops — equal and opposite action loops in space, never in time; a time loop is an infinity

`QLF_NoTimeLoops` excludes time loops by depth, and `QLF_LogicalPersistence` derives that from the law
of weakening. Neither uses ZFA balance. This module asks what balance itself contributes, with
handedness taken seriously, and whether a time loop is a kind of infinity.

**Equal and opposite, with handedness.** A twist is a handedness on an axis (`QLF_Handedness`), and
every twist is handed (`handedness_ne_zero`). The opposite of a history is its **mirror**: the
Hermitian adjoint, which reverses the order and flips every handedness (`mirror`).

* **`equal_and_opposite_balances`** — a history followed by its mirror has zero net handedness on every
  axis, so it is a ZFA closure, whatever the history was.
* **`equal_and_opposite_advances`** — and it strictly extends the history: the record doubles
  (`mirror_length`). The opposite is not an undo. It is a new set of handed distinctions, each nonzero
  (`mirror_handed`), whose sum cancels.
* **`closure_loops_in_space_not_time`** — the two together. Balance returns the action to zero on every
  axis (a closed loop in action space, `Closure_Walk.md`); the record moves forward.
* **`loopTrain_balanced`**, **`loopTrain_advances`** — repeating a closed loop `k` times stays a closure
  at every `k`, and each repetition strictly extends the last. Going round the loop again is a new
  event, never a return to an old one.

**A time loop is an infinity.**

* **`time_loop_is_infinite_regress`** — an event on a time loop lies in its own past, and in the past of
  that, without end: an infinite descending causal chain.
* **`finite_depth_no_infinite_regress`** — a finite depth that every step raises excludes every infinite
  regress, loops included. This is the general form of `no_time_loop_of_depth`.
* **`regress_without_loop`** — sharpness: an infinite past need not loop (the integers under `<`). So
  time loops are one kind of infinity, and a finite construction excludes all of them.
* **`loop_record_infinite`** — the record of a loop traversed again and again fits in no finite event:
  for every finite history `E`, some number of traversals is not a prefix of `E`. A time loop's complete
  record would be an infinite history, which is a non-terminating computation.
* **`equal_and_opposite_forever`** — the capstone. A history with its mirror, repeated without limit, is a
  closure at every stage, advances at every stage, and has a record no finite event holds. Equal and
  opposite action may repeat forever in space; it never closes a loop in time.

## Honest scope

Balance alone does **not** exclude time loops: the exclusion is the depth (`QLF_NoTimeLoops`), derived
from weakening (`QLF_LogicalPersistence`). What balance adds is that every closure, including the most
symmetric one, is reached by *adding* handed steps, never by removing any, and with `no_unclosing` that
nothing closed can be returned to its past. "A time loop is an infinity" is proved in the precise sense
above (an infinite regress, and an infinite record); it is not a claim about any continuum spacetime,
whose global causal structure still rides on the `order_metric_continuum_limit` bridge. No new axioms.
-/

namespace QLF.HandedLoops

open QLF QLF.Spin QLF.ReachableEvent QLF.NoTimeLoops

-- ==========================================
-- 1. Equal and opposite, with handedness
-- ==========================================

/-- The **mirror** of a history: its Hermitian adjoint. The order is reversed and every handedness is
    flipped, axis by axis. -/
def mirror (ts : List Twist) : List Twist := (ts.map Twist.conj).reverse

/-- Net handedness does not depend on order. -/
theorem handednessOn_reverse (a : Axis) (ts : List Twist) :
    handednessOn a ts.reverse = handednessOn a ts := by
  simp [handednessOn]

/-- The mirror carries the opposite handedness on every axis. -/
theorem handednessOn_mirror (a : Axis) (ts : List Twist) :
    handednessOn a (mirror ts) = - handednessOn a ts := by
  rw [mirror, handednessOn_reverse, handednessOn_map_conj]

/-- The mirror has as many steps as the history. -/
theorem mirror_length (ts : List Twist) : (mirror ts).length = ts.length := by
  simp [mirror]

/-- Every step of the mirror is handed: the opposite is made of distinctions, not of their absence. -/
theorem mirror_handed (ts : List Twist) : ∀ t ∈ mirror ts, handedness t ≠ 0 :=
  fun t _ => handedness_ne_zero t

/-- **Equal and opposite balances.** A history followed by its mirror has zero net handedness on every
    axis: it is a ZFA closure, whatever the history. -/
theorem equal_and_opposite_balances (ts : List Twist) : countBalanced (ts ++ mirror ts) := by
  rw [zfa_iff_handedness_balanced]
  intro a
  rw [handednessOn_append, handednessOn_mirror]
  omega

/-- **Equal and opposite advances.** The mirror is appended, so the closure strictly extends the
    history it balances. -/
theorem equal_and_opposite_advances {ts : List Twist} (h : ts ≠ []) :
    strictlyPrecedes ts (ts ++ mirror ts) := by
  refine ⟨List.prefix_append ts _, ?_⟩
  intro heq
  have hl : (ts ++ mirror ts).length = ts.length + ts.length := by
    rw [List.length_append, mirror_length]
  have h2 := congrArg List.length heq
  rw [hl] at h2
  have hpos : 0 < ts.length := List.length_pos_iff.mpr h
  omega

/-- **Closure loops in space, not in time.** Equal and opposite action returns the net handedness to
    zero on every axis, while the record strictly advances and doubles in length. -/
theorem closure_loops_in_space_not_time {ts : List Twist} (h : ts ≠ []) :
    (∀ a : Axis, handednessOn a (ts ++ mirror ts) = 0) ∧
    strictlyPrecedes ts (ts ++ mirror ts) ∧
    (ts ++ mirror ts).length = 2 * ts.length := by
  refine ⟨(zfa_iff_handedness_balanced _).mp (equal_and_opposite_balances ts),
    equal_and_opposite_advances h, ?_⟩
  rw [List.length_append, mirror_length]
  omega

-- ==========================================
-- 2. Going round a loop again is a new event
-- ==========================================

/-- A loop `w` traversed `k` times, recorded in order. -/
def loopTrain {α : Type _} (w : List α) : ℕ → List α
  | 0 => []
  | k + 1 => loopTrain w k ++ w

theorem loopTrain_succ {α : Type _} (w : List α) (k : ℕ) :
    loopTrain w (k + 1) = loopTrain w k ++ w := rfl

theorem loopTrain_length {α : Type _} (w : List α) :
    ∀ k, (loopTrain w k).length = k * w.length
  | 0 => by simp [loopTrain]
  | k + 1 => by
    rw [loopTrain_succ, List.length_append, loopTrain_length w k]
    ring

theorem loopTrain_handednessOn (w : List Twist) (a : Axis) :
    ∀ k, handednessOn a (loopTrain w k) = (k : ℤ) * handednessOn a w
  | 0 => by simp [loopTrain, handednessOn_nil]
  | k + 1 => by
    rw [loopTrain_succ, handednessOn_append, loopTrain_handednessOn w a k]
    push_cast
    ring

/-- **A repeated closure stays a closure.** -/
theorem loopTrain_balanced {w : List Twist} (hw : countBalanced w) (k : ℕ) :
    countBalanced (loopTrain w k) := by
  rw [zfa_iff_handedness_balanced] at hw ⊢
  intro a
  rw [loopTrain_handednessOn, hw a]
  simp

/-- **Each traversal strictly extends the last.** Going round the loop again is a new event. -/
theorem loopTrain_advances {α : Type _} {w : List α} (hw : w ≠ []) (k : ℕ) :
    strictlyPrecedes (loopTrain w k) (loopTrain w (k + 1)) := by
  refine ⟨List.prefix_append _ _, ?_⟩
  intro heq
  have hl := congrArg List.length heq
  rw [loopTrain_succ, List.length_append] at hl
  have hpos : 0 < w.length := List.length_pos_iff.mpr hw
  omega

-- ==========================================
-- 3. A time loop is an infinity
-- ==========================================

variable {S : Type _}

/-- An **infinite regress**: an infinite descending causal chain, each event in the strict past of the
    one before it. -/
def InfiniteRegress (step : S → S → Prop) : Prop :=
  ∃ f : ℕ → S, ∀ n, Relation.TransGen step (f (n + 1)) (f n)

/-- **A time loop is an infinite regress.** An event on a loop lies in its own past, and in the past of
    that, without end. -/
theorem time_loop_is_infinite_regress (step : S → S → Prop) {a : S}
    (h : Relation.TransGen step a a) :
    ∃ f : ℕ → S, f 0 = a ∧ ∀ n, Relation.TransGen step (f (n + 1)) (f n) :=
  ⟨fun _ => a, rfl, fun _ => h⟩

private theorem transGen_depth_lt (step : S → S → Prop) (depth : S → ℕ)
    (hd : ∀ a b, step a b → depth a < depth b) {a b : S} (h : Relation.TransGen step a b) :
    depth a < depth b := by
  induction h with
  | single hab => exact hd _ _ hab
  | tail _ hbc ih => exact Nat.lt_trans ih (hd _ _ hbc)

private theorem regress_depth_bound (step : S → S → Prop) (depth : S → ℕ)
    (hd : ∀ a b, step a b → depth a < depth b) (f : ℕ → S)
    (hf : ∀ n, Relation.TransGen step (f (n + 1)) (f n)) :
    ∀ n, depth (f n) + n ≤ depth (f 0)
  | 0 => by simp
  | n + 1 => by
    have h1 := transGen_depth_lt step depth hd (hf n)
    have h2 := regress_depth_bound step depth hd f hf n
    omega

/-- **A finite depth excludes every infinite regress.** If each step raises a natural-number depth,
    there is no infinite descending causal chain, and in particular no time loop. -/
theorem finite_depth_no_infinite_regress (step : S → S → Prop) (depth : S → ℕ)
    (hd : ∀ a b, step a b → depth a < depth b) : ¬ InfiniteRegress step := by
  rintro ⟨f, hf⟩
  have := regress_depth_bound step depth hd f hf (depth (f 0) + 1)
  omega

private theorem transGen_lt_int {a b : ℤ} (h : Relation.TransGen (fun x y : ℤ => x < y) a b) :
    a < b := by
  induction h with
  | single hab => exact hab
  | tail _ hbc ih => exact lt_trans ih hbc

/-- **Sharpness: an infinite past need not loop.** The integers under `<` have an infinite descending
    chain and no loop. Time loops are one kind of infinity; a finite construction excludes them all. -/
theorem regress_without_loop :
    InfiniteRegress (fun x y : ℤ => x < y) ∧
    ∀ a : ℤ, ¬ Relation.TransGen (fun x y : ℤ => x < y) a a := by
  refine ⟨⟨fun n => -(n : ℤ), fun n => Relation.TransGen.single ?_⟩, ?_⟩
  · show -((n + 1 : ℕ) : ℤ) < -(n : ℤ)
    omega
  · intro a h
    exact lt_irrefl a (transGen_lt_int h)

/-- **The record of a time loop is infinite.** However long a finite history `E` is, some number of
    traversals of a nonempty loop is not a prefix of it: no finite event records the whole loop. -/
theorem loop_record_infinite {α : Type _} {w : List α} (hw : w ≠ []) (E : List α) :
    ∃ k, ¬ (loopTrain w k <+: E) := by
  refine ⟨E.length + 1, fun h => ?_⟩
  have hle := h.length_le
  rw [loopTrain_length] at hle
  have hpos : 0 < w.length := List.length_pos_iff.mpr hw
  nlinarith

/-- **Equal and opposite, forever.** A history with its mirror, repeated without limit, is a ZFA closure
    at every stage and strictly advances at every stage, and no finite event holds its whole record.
    Equal and opposite action may repeat forever in space; it never closes a loop in time. -/
theorem equal_and_opposite_forever {ts : List Twist} (h : ts ≠ []) :
    (∀ k, countBalanced (loopTrain (ts ++ mirror ts) k)) ∧
    (∀ k, strictlyPrecedes (loopTrain (ts ++ mirror ts) k)
      (loopTrain (ts ++ mirror ts) (k + 1))) ∧
    (∀ E : List Twist, ∃ k, ¬ (loopTrain (ts ++ mirror ts) k <+: E)) := by
  have hne : ts ++ mirror ts ≠ [] := fun he => h (List.append_eq_nil_iff.mp he).1
  exact ⟨loopTrain_balanced (equal_and_opposite_balances ts), loopTrain_advances hne,
    loop_record_infinite hne⟩

end QLF.HandedLoops
