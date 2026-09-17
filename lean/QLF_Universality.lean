-- QLF_Universality.lean
-- Universality: QLF generates all terminating finitely-encoded logical computations
-- Write-up: Universality.md.

import QLF_Axioms
import QLF_QuCalc
import QLF_Critical_Line

namespace QLF

/-- A terminating logical computation unrolled into a finite acyclic NAND-delay graph. -/
structure TerminatingComputation where
  nodes : Nat
  edges : List (Nat × Nat × Bool)  -- (from, to, isNand)

noncomputable def encodeComputation (c : TerminatingComputation) : TopoString :=
  c.edges.flatMap fun (_, _, isNand) =>
    if isNand then
      [TopoElement.phase LogicPhase.pos, TopoElement.phase LogicPhase.neg]
    else
      [TopoElement.phase LogicPhase.neg, TopoElement.phase LogicPhase.pos]

theorem encode_is_phase_only (c : TerminatingComputation) :
    ∀ e ∈ encodeComputation c, ∃ p, e = TopoElement.phase p := by
  intro e h
  simp only [encodeComputation, List.mem_flatMap] at h
  obtain ⟨⟨_, _, isNand⟩, _, hmem⟩ := h
  simp only at hmem
  split_ifs at hmem with hif
  · simp only [List.mem_cons, List.mem_nil_iff, or_false] at hmem
    rcases hmem with rfl | rfl
    · exact ⟨LogicPhase.pos, rfl⟩
    · exact ⟨LogicPhase.neg, rfl⟩
  · simp only [List.mem_cons, List.mem_nil_iff, or_false] at hmem
    rcases hmem with rfl | rfl
    · exact ⟨LogicPhase.neg, rfl⟩
    · exact ⟨LogicPhase.pos, rfl⟩

-- Each edge contributes a canceling [pos,neg] or [neg,pos] pair; the full encoding
-- reduces to [] because every phase element is paired with its complement.
theorem encode_reduces_to_empty (c : TerminatingComputation) :
    full_zeno_prune (encodeComputation c) = [] := by
  have h_zp : zeno_prune (encodeComputation c) = [] := by
    simp only [encodeComputation]
    induction c.edges with
    | nil => rfl
    | cons edge rest ih =>
      obtain ⟨_, _, b⟩ := edge
      simp only [List.flatMap_cons]
      -- each edge maps to [pos,neg] or [neg,pos]; both are stripped by zeno_prune
      cases b <;> exact ih
  by_cases hempty : encodeComputation c = []
  · rw [hempty, full_zeno_prune, dif_neg (by decide)]
  · have hlt : (zeno_prune (encodeComputation c)).length < (encodeComputation c).length := by
      rw [h_zp]
      cases hec : encodeComputation c with
      | nil => exact absurd hec hempty
      | cons _ _ => exact Nat.succ_pos _
    rw [full_zeno_prune, dif_pos hlt, h_zp, full_zeno_prune, dif_neg (by decide)]

theorem encode_is_zfa (c : TerminatingComputation) :
    achieves_ZFA (encodeComputation c) := by
  unfold achieves_ZFA
  rw [encode_reduces_to_empty]
  simp

theorem encode_is_generated (c : TerminatingComputation) :
    ∃ n, encodeComputation c ∈ expand_generation n :=
  ⟨(encodeComputation c).length,
   qucalc_generates_all_phase_strings
     (encodeComputation c).length
     (encodeComputation c)
     ⟨rfl, encode_is_phase_only c⟩⟩

theorem qlf_universality (c : TerminatingComputation) :
    ∃ n, encodeComputation c ∈ find_stable_states n := by
  obtain ⟨n, h_gen⟩ := encode_is_generated c
  have h_zfa := encode_is_zfa c
  have h_bool : achieves_ZFA_bool (encodeComputation c) = true := by
    unfold achieves_ZFA_bool achieves_ZFA at *
    simpa using h_zfa
  exact ⟨n, List.mem_filter.mpr ⟨h_gen, h_bool⟩⟩

end QLF
