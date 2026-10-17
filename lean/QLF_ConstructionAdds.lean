import QLF_NoTimeLoops
import QLF_Combinatorics
import ZFAEventDynamics
import ER_EPR_QLF
import QLF_HorizonClosure

set_option linter.unusedVariables false

/-!
# QLF_ConstructionAdds — construction only adds: the no-loop hypothesis discharged

`QLF_NoTimeLoops` proves that a construction whose steps raise a depth has no loops, and takes "each
step adds" as the hypothesis. This module proves that hypothesis for every construction operator QLF
actually defines, and shows that the reverse operation — removing a closure — is not a well-defined
map, so it cannot be a substrate step.

* **`append_strictly_extends`** — appending one element to a history yields a history that strictly
  extends it. Every QLF generator is built from this single operation.
* **`branch_state_extends`**, **`expand_string_extends`**, **`generateNextEvents_extends`** — each of
  QLF's three construction operators (the QuCalc branching step, the combinatoric expansion, and the
  event-dynamics step of `ZFAEventDynamics`) only produces strict extensions of its input.
* **`expand_generation_length`** and **`expand_generation_has_parent`** — the possibilist engine is
  depth-graded: generation `n` holds only histories of length `n`, and every history in generation
  `n + 1` strictly extends one in generation `n`. Nothing generated ever shortens or rewrites a history.
* **`generation_has_no_loops`** — the capstone: the QuCalc generation step has no cycle of any length,
  by `no_time_loop_of_depth` with its hypothesis now proved rather than assumed.
* **`no_unclosing`** — why no subtracting step can be added. Closure is many-to-one: `[+,−]` and `[−,+]`
  both close to the same empty residue, so no function recovers a history from its closed outcome.
  "Un-closing" — returning a closed event to the past it came from — is not a function at all.
* **`closure_receipt_stable`** — and observation cannot undo a closure either: a history closed at
  horizon `R` stays closed at every wider horizon (reusing `closedAtHorizon_mono`).

## Honest scope

This proves "construction only adds" for **QLF's defined operators**: every generator in the Lean
substrate is append-only, and the inverse of closure does not exist as a map. It does not prove that
nature is QLF's construction — that identification is the framework's founding postulate, tested
empirically, not in Lean. Pruning (`full_zeno_prune`) is not an exception: it computes a history's
residue to decide whether it closes; it does not remove anything from the history, which is the event.
No new axioms; `anti_pair_closes` evaluates by `native_decide`, following `conjugate_pair_closes`.
-/

namespace QLF.ConstructionAdds

open QLF.ReachableEvent QLF.NoTimeLoops

variable {α : Type _}

/-- **The one construction move.** Appending an element strictly extends a history. -/
theorem append_strictly_extends (s : List α) (x : α) : strictlyPrecedes s (s ++ [x]) := by
  refine ⟨List.prefix_append s [x], ?_⟩
  intro h
  have := congrArg List.length h
  simp at this

/-- **The QuCalc branching step only adds.** Both branches of `branch_state s` strictly extend `s`. -/
theorem branch_state_extends (s : TopoString) :
    ∀ t ∈ branch_state s, strictlyPrecedes s t := by
  intro t ht
  simp only [branch_state, List.mem_cons, List.not_mem_nil, or_false] at ht
  rcases ht with rfl | rfl
  · exact append_strictly_extends s _
  · exact append_strictly_extends s _

/-- **The combinatoric expansion only adds.** Every string `expand_string s` produces strictly extends
    `s`. -/
theorem expand_string_extends (s : TopoString) :
    ∀ t ∈ expand_string s, strictlyPrecedes s t := by
  intro t ht
  simp only [expand_string, List.mem_map] at ht
  obtain ⟨e, _, rfl⟩ := ht
  exact append_strictly_extends s e

/-- **The event-dynamics step only adds.** Every ZFA event `generateNextEvents h` proposes has a history
    strictly extending `h`. -/
theorem generateNextEvents_extends (h : List _root_.Twist) :
    ∀ e ∈ generateNextEvents h, strictlyPrecedes h e.history := by
  intro e he
  simp only [generateNextEvents, extendTowardZFA, List.mem_filterMap, List.mem_map] at he
  obtain ⟨cand, ⟨t, _, rfl⟩, hsome⟩ := he
  split at hsome
  · obtain rfl := Option.some.inj hsome
    exact append_strictly_extends h t
  · exact absurd hsome (by simp)

/-- Membership in a superposition's expansion: `t` is produced from some state `s` of the
    superposition by one branching step. -/
theorem mem_expand_states {t : TopoString} :
    ∀ L : List TopoString, t ∈ expand_states L → ∃ s ∈ L, t ∈ branch_state s
  | [], h => by simp [expand_states] at h
  | s :: tail, h => by
    simp only [expand_states, List.mem_append] at h
    rcases h with h | h
    · exact ⟨s, List.mem_cons_self, h⟩
    · obtain ⟨s', hs', ht⟩ := mem_expand_states tail h
      exact ⟨s', List.mem_cons_of_mem _ hs', ht⟩

/-- **Every history in generation `n + 1` strictly extends one in generation `n`.** -/
theorem expand_generation_has_parent (n : ℕ) :
    ∀ t ∈ expand_generation (n + 1), ∃ s ∈ expand_generation n, strictlyPrecedes s t := by
  intro t ht
  obtain ⟨s, hs, hts⟩ := mem_expand_states (expand_generation n) ht
  exact ⟨s, hs, branch_state_extends s t hts⟩

/-- **The possibilist engine is depth-graded.** Generation `n` holds only histories of length `n`. -/
theorem expand_generation_length : ∀ n, ∀ t ∈ expand_generation n, t.length = n
  | 0, t, ht => by
    simp only [expand_generation, List.mem_cons, List.not_mem_nil, or_false] at ht
    subst ht; rfl
  | n + 1, t, ht => by
    obtain ⟨s, hs, hts⟩ := mem_expand_states (expand_generation n) ht
    have hlen := expand_generation_length n s hs
    simp only [branch_state, List.mem_cons, List.not_mem_nil, or_false] at hts
    rcases hts with rfl | rfl <;> simp [hlen]

/-- One step of the QuCalc generation: `t` is a branch of `s`. -/
def genStep (s t : TopoString) : Prop := t ∈ branch_state s

/-- **The generation step has no loops** — `no_time_loop_of_depth` with its hypothesis proved: each
    step raises the history length (`branch_state_extends`, `strictlyPrecedes_length_lt`). -/
theorem generation_has_no_loops (s : TopoString) : ¬ Relation.TransGen genStep s s :=
  no_time_loop_of_depth genStep List.length
    (fun a b h => strictlyPrecedes_length_lt (branch_state_extends a b h)) s

/-- A closed history leaves the empty residue (every surviving element would be a gauge). -/
theorem prune_eq_nil_of_zfa {s : TopoString} (h : achieves_ZFA s) : full_zeno_prune s = [] := by
  unfold achieves_ZFA at h
  cases hp : full_zeno_prune s with
  | nil => rfl
  | cons x xs =>
    rw [hp] at h
    cases x <;> simp [is_gauge] at h

/-- The reversed conjugate pair `[−, +]` also closes. -/
theorem anti_pair_closes :
    achieves_ZFA [TopoElement.phase LogicPhase.neg, TopoElement.phase LogicPhase.pos] := by
  unfold achieves_ZFA
  native_decide

/-- **No un-closing.** No function recovers a closed history from its closed outcome: `[+,−]` and `[−,+]`
    both close to the empty residue, so any candidate inverse would have to send `[]` to both. Removing a
    closure is not a well-defined operation, so no substrate step can subtract. -/
theorem no_unclosing :
    ¬ ∃ back : TopoString → TopoString,
      ∀ s, achieves_ZFA s → back (full_zeno_prune s) = s := by
  rintro ⟨back, hback⟩
  have h1 := hback _ QLF.conjugate_pair_closes
  have h2 := hback _ anti_pair_closes
  rw [prune_eq_nil_of_zfa QLF.conjugate_pair_closes] at h1
  rw [prune_eq_nil_of_zfa anti_pair_closes] at h2
  have := h1.symm.trans h2
  simp at this

/-- **A receipt stays a receipt.** A history closed at horizon `R` is closed at every wider horizon:
    observation can widen but never revoke a closure. -/
theorem closure_receipt_stable {R R' : ℕ} {s : TopoString} (hR : R ≤ R')
    (h : QLF.HorizonClosure.closedAtHorizon R s) : QLF.HorizonClosure.closedAtHorizon R' s :=
  QLF.HorizonClosure.closedAtHorizon_mono h hR

end QLF.ConstructionAdds
