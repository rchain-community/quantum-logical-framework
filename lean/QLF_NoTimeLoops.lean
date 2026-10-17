import QLF_CausalInterval
import QLF_AngularMomentum

set_option linter.unusedVariables false

/-!
# QLF_NoTimeLoops — a constructed universe has no time loops; rotation is unrestricted

Gödel (1949) found an exact solution of Einstein's field equations — rotating dust with a cosmological
constant — in which a closed timelike curve passes through every event. The field equations are local,
so they cannot exclude it: global causal structure is not one of their outputs. This module proves the
substrate statement that excludes it, and shows that the exclusion costs nothing on the rotation side.

* **`no_time_loop_of_depth`** — the general law. *Any* construction in which each step strictly
  increases a natural-number depth (a step adds at least one closure) has **no loops**: the transitive
  closure of the step relation is irreflexive. Nothing about lists, twists or QLF is assumed — only that
  construction adds. This is the precise content of "in a constructed universe there are no time loops".
* **`no_time_loops`** — QLF's instance. Strict causal precedence `A ≺ B` (`B`'s history properly extends
  `A`'s, `strictlyPrecedes`) raises the depth `|A| < |B|` (`strictlyPrecedes_length_lt`), so no chain
  `A ≺ ⋯ ≺ A` of any length exists: no event is in its own strict past.
* **`causalInterval_finite`** — every causal interval `[A,B]` is a finite set (each member is a prefix
  of `B`). Together with `no_time_loops` this is the substrate form of the two conditions that, in the
  continuum, characterise **global hyperbolicity** (causal + compact causal diamonds, Bernal–Sánchez
  2007). Gödel's spacetime is not globally hyperbolic, so it is not a rendering of any QLF causal set.
* **`rotation_unbounded`** — the possibilist half. For every `n` there is a substrate history whose
  circulation (angular momentum, `QLF_AngularMomentum.circulation`) is at least `n`: a train of
  Borromean `x,y,z` vortex cells (`circulation_vortexTrain`, `3k+1` quanta). Rotation is not bounded by
  the no-loop law, so the loop exclusion is *not* a rotation exclusion.
* **`rotation_without_time_loops`** — the conjunction: arbitrarily large rotation exists, and no event
  of any history lies on a time loop. Gödel's rotation is allowed; Gödel's closed timelike curves are not.

## Honest scope

`no_time_loop_of_depth` is fully general and elementary; its force is in the hypothesis (construction
strictly adds depth), which is QLF's postulate, not a derived fact. The continuum translation — "the
rendered metric is globally hyperbolic" — is **not** proved here: it rides on the existing order→metric
bridge `order_metric_continuum_limit` (`QLF_OrderMetric`) plus the cited Bernal–Sánchez
characterisation, and is stated in prose ([`UniversalRelativity.md`](../UniversalRelativity.md) §4b), not
as a new axiom. The module makes no claim that any particular rotating continuum solution *is* rendered,
and no quantitative cosmic-vorticity prediction. Reuses `QLF_CausalInterval` and `QLF_AngularMomentum`;
no new axioms.
-/

namespace QLF.NoTimeLoops

open QLF QLF.ReachableEvent QLF.CausalInterval QLF.BaryonWinding QLF.AngularMomentum

/-- **The general no-loop law.** If every construction step strictly increases a natural-number depth,
    the step relation has no cycles of any length: its transitive closure is irreflexive. A universe
    built by adding closures cannot return to an event it has already passed. -/
theorem no_time_loop_of_depth {S : Type _} (step : S → S → Prop) (depth : S → ℕ)
    (hd : ∀ a b, step a b → depth a < depth b) :
    ∀ a, ¬ Relation.TransGen step a a := by
  have key : ∀ a b, Relation.TransGen step a b → depth a < depth b := by
    intro a b h
    induction h with
    | single hab => exact hd _ _ hab
    | tail _ hbc ih => exact Nat.lt_trans ih (hd _ _ hbc)
  intro a h
  exact Nat.lt_irrefl _ (key a a h)

variable {α : Type _}

/-- **Strict causal precedence** `A ≺ B`: `A` lies in `B`'s past and is a different event, i.e. `B`'s
    history properly extends `A`'s. -/
def strictlyPrecedes (A B : Event α) : Prop := reachable A B ∧ A ≠ B

/-- Strict precedence strictly raises the depth (the history length, the local-clock tick count). -/
theorem strictlyPrecedes_length_lt {A B : Event α} (h : strictlyPrecedes A B) :
    A.length < B.length := by
  rcases h with ⟨hAB, hne⟩
  have hle : A.length ≤ B.length := hAB.sublist.length_le
  refine Nat.lt_of_le_of_ne hle ?_
  intro heq
  exact hne (hAB.eq_of_length heq)

/-- **No time loops.** No event is in its own strict past: there is no chain `A ≺ ⋯ ≺ A` of any
    length. The substrate form of "no closed timelike (or causal) curve". -/
theorem no_time_loops (A : Event α) : ¬ Relation.TransGen strictlyPrecedes A A :=
  no_time_loop_of_depth strictlyPrecedes List.length
    (fun _ _ h => strictlyPrecedes_length_lt h) A

/-- Every event causally between `A` and `B` is a prefix of `B`. -/
theorem causalInterval_sub_inits {A B C : Event α} (h : C ∈ causalInterval A B) :
    C ∈ B.inits := by
  rcases h with ⟨_, hCB⟩
  exact (List.mem_inits C B).mpr hCB

/-- **Causal intervals are finite** — the substrate counterpart of compact causal diamonds. With
    `no_time_loops` this is the discrete form of global hyperbolicity (causal + compact diamonds). -/
theorem causalInterval_finite (A B : Event α) : (causalInterval A B).Finite :=
  (List.finite_toSet B.inits).subset (fun _ hC => causalInterval_sub_inits hC)

/-- One Borromean vortex cell: the cyclic `x,y,z` axis triple `> ^ /` (one circulation quantum,
    `baryon_proton`). -/
def vortex : List Twist := [Twist.right, Twist.up, Twist.slash]

/-- A train of `k` vortex cells. -/
def vortexTrain : ℕ → List Twist
  | 0 => []
  | k + 1 => vortex ++ vortexTrain k

/-- Prepending a vortex cell to a vortex-led history adds three circulation quanta (the three cyclic
    windows `xyz`, `yzx`, `zxy`). -/
theorem baryon_vortex_step (rest : List Twist) :
    baryonNumber (vortex ++ (vortex ++ rest)) = 3 + baryonNumber (vortex ++ rest) := by
  show baryonNumber (Twist.right :: Twist.up :: Twist.slash :: Twist.right :: Twist.up ::
      Twist.slash :: rest) = 3 + baryonNumber (Twist.right :: Twist.up :: Twist.slash :: rest)
  rw [baryonNumber, baryonNumber, baryonNumber]
  simp only [signTriple, axOf]
  omega

/-- A train of `k + 1` vortex cells carries `3k + 1` circulation quanta. -/
theorem circulation_vortexTrain (k : ℕ) :
    circulation (vortexTrain (k + 1)) = 3 * (k : ℤ) + 1 := by
  unfold circulation
  induction k with
  | zero => decide
  | succ n ih =>
    show baryonNumber (vortex ++ (vortex ++ vortexTrain n)) = _
    rw [baryon_vortex_step]
    have h : baryonNumber (vortex ++ vortexTrain n) = 3 * (n : ℤ) + 1 := ih
    rw [h]; omega

/-- **Rotation is unbounded.** For every `n` some history carries at least `n` circulation quanta: the
    substrate places no upper limit on rotation (only the per-cell quantum, `vorticity_quantized`). -/
theorem rotation_unbounded (n : ℕ) : ∃ ts : List Twist, (n : ℤ) ≤ circulation ts :=
  ⟨vortexTrain (n + 1), by rw [circulation_vortexTrain]; omega⟩

/-- **Rotation without time loops.** Arbitrarily large rotation is realizable, and no event of any
    history lies on a time loop. Gödel's rotation is allowed; Gödel's closed timelike curves are not. -/
theorem rotation_without_time_loops :
    (∀ n : ℕ, ∃ ts : List Twist, (n : ℤ) ≤ circulation ts) ∧
    (∀ A : Event Twist, ¬ Relation.TransGen strictlyPrecedes A A) :=
  ⟨rotation_unbounded, no_time_loops⟩

end QLF.NoTimeLoops
