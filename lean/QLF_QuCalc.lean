import QLF_Axioms
import Mathlib.Data.List.Basic

-- QLF_QuCalc.lean — the phase-generation engine and the ZFA filter (`full_zeno_prune`).
-- Language reference: QuCalc.md; runtime counterpart: twist_core.py.

-- ==========================================
-- 1. THE POSSIBILIST EXPANSION ENGINE
-- ==========================================

-- A single quantum-logical branching step. 
-- The universe proposes both a positive and negative extension to the current history.
def branch_state (s : TopoString) : List TopoString :=
  [s ++ [TopoElement.phase LogicPhase.pos], s ++ [TopoElement.phase LogicPhase.neg]]

-- Applies the branching across a superposition of states.
def expand_states : List TopoString → List TopoString
  | [] => []
  | s :: tail => branch_state s ++ expand_states tail

-- The fluxoid QuCalc combinatorial tree. 
-- Generates the complete bounded possibility space at step n.
def expand_generation : Nat → List TopoString
  | 0 => [[]]
  | n + 1 => expand_states (expand_generation n)

-- ==========================================
-- 2. THE ZERO FREE ACTION FILTER
-- ==========================================

-- A computable boolean version of ZFA to filter the discrete generated lists.
-- (This directly maps to the logic in your Python engine).
def achieves_ZFA_bool (s : TopoString) : Bool :=
  (full_zeno_prune s).any is_gauge == false

-- The universal pruning mechanism applied to a specific generation.
-- Paths that do not evaluate to zero net action are physically annihilated.
def find_stable_states (n : Nat) : List TopoString :=
  (expand_generation n).filter achieves_ZFA_bool

-- A generation is resonant (corresponding to a zeta zero) if stable topological loops survive.
def is_resonant_generation (n : Nat) : Bool :=
  (find_stable_states n).length > 0

-- ==========================================
-- 3. COMPLETENESS: ALL PHASE STRINGS ARE GENERATED
-- ==========================================

-- Every string of length n whose elements are all phases appears in expand_generation n.

private lemma expand_states_contains (gen : List TopoString) (init : TopoString)
    (h_init : init ∈ gen) (p : LogicPhase) :
    init ++ [TopoElement.phase p] ∈ expand_states gen := by
  induction gen with
  | nil => simp at h_init
  | cons head tail ih =>
    simp only [expand_states, branch_state, List.mem_append, List.mem_cons]
    rcases List.mem_cons.mp h_init with rfl | htail
    · left; cases p
      · left; rfl
      · right; left; rfl
    · right; exact ih htail

theorem qucalc_generates_all_phase_strings (n : Nat) (s : TopoString)
    (h : s.length = n ∧ ∀ e ∈ s, ∃ p, e = TopoElement.phase p) :
    s ∈ expand_generation n := by
  obtain ⟨h_len, h_phase⟩ := h
  induction n generalizing s with
  | zero =>
    simp only [expand_generation, List.mem_singleton]
    cases s with
    | nil => rfl
    | cons _ _ => simp at h_len
  | succ n ih =>
    have h_ne : s ≠ [] := by intro h; simp [h] at h_len
    let init := s.dropLast
    have h_init_len : init.length = n := by
      simp [init, List.length_dropLast]; omega
    have h_s_eq : init ++ [s.getLast h_ne] = s :=
      List.dropLast_append_getLast h_ne
    have h_init_phase : ∀ e ∈ init, ∃ p, e = TopoElement.phase p := by
      intro e he
      apply h_phase; rw [← h_s_eq]; exact List.mem_append_left _ he
    have h_init_gen : init ∈ expand_generation n := ih init h_init_len h_init_phase
    obtain ⟨p, hp⟩ := h_phase _ (List.getLast_mem h_ne)
    rw [← h_s_eq, hp]
    simp only [expand_generation]
    exact expand_states_contains (expand_generation n) init h_init_gen p

-- ==========================================
-- 4. THE GENERATOR CRITICAL LINE PROOF
-- ==========================================

-- ZERO SORRY THEOREM: The Generator Respects the Critical Line.
-- This is the mathematical bridge proving that no matter how the universe expands,
-- the physical constraint of ZFA forces all surviving reality onto strict symmetry.
theorem generated_stable_states_are_symmetric (n : Nat) (s : TopoString) (h_in : s ∈ find_stable_states n) : is_symmetric s := by
  -- 1. Extract the filtering condition from the list membership
  have h_filter : achieves_ZFA_bool s = true := 
    List.of_mem_filter h_in
  
  -- 2. Unfold the boolean evaluation to match our logical Axiom Prop
  unfold achieves_ZFA_bool at h_filter
  
  -- 3. Construct the logical Prop required by the Axioms theorem
  have h_zfa : achieves_ZFA s := by
    unfold achieves_ZFA
    -- Lean 4's `simpa` bridges the gap, translating the boolean `==` to the logical `=`
    simpa using h_filter
    
  -- 4. Invoke the master topological theorem from QLF_Axioms.lean
  exact zfa_implies_critical_line s h_zfa

-- ==========================================
-- 5. EMERGENT MARKOV BLANKET FORMATION
-- ==========================================
--
-- A "blanket" in the `Emergent_Markov_Blankets.md` sense is a group of
-- ZFA-balanced atoms whose collective concatenation forms a higher-order
-- closed structure. Here we prove the count-balance half of ZFA is
-- preserved under pairwise and N-ary concatenation: symmetric atoms
-- compose into a symmetric collective.
--
-- The full ZFA condition (count balance ∧ Pauli closure, per
-- Experimental_Consistency.md §2.1) is enforced at runtime
-- (twist_core.py, zfa-core Rust kernel, the browser app's tokenTwists).
-- Promoting Pauli closure to a Lean theorem (`pauli_closed_of_admissible_zfa`)
-- remains open work and is the natural next round; see CLAUDE.md
-- "Runtime layer requires more than count balance."

private lemma count_pos_append (s₁ s₂ : TopoString) :
    count_pos (s₁ ++ s₂) = count_pos s₁ + count_pos s₂ := by
  induction s₁ with
  | nil => simp [count_pos]
  | cons head tail ih =>
    show count_pos (head :: (tail ++ s₂)) = count_pos (head :: tail) + count_pos s₂
    rw [count_pos_cons, count_pos_cons, ih]
    omega

private lemma count_neg_append (s₁ s₂ : TopoString) :
    count_neg (s₁ ++ s₂) = count_neg s₁ + count_neg s₂ := by
  induction s₁ with
  | nil => simp [count_neg]
  | cons head tail ih =>
    show count_neg (head :: (tail ++ s₂)) = count_neg (head :: tail) + count_neg s₂
    rw [count_neg_cons, count_neg_cons, ih]
    omega

/-- Binary emergent blanket formation: the count-balance half of ZFA
    closure is preserved under pairwise concatenation. Two symmetric
    atoms compose into a symmetric collective. -/
theorem emergent_blanket_formation_binary
    (s₁ s₂ : TopoString) (h₁ : is_symmetric s₁) (h₂ : is_symmetric s₂) :
    is_symmetric (s₁ ++ s₂) := by
  unfold is_symmetric at h₁ h₂ ⊢
  rw [count_pos_append, count_neg_append]
  omega

/-- **Emergent Markov blanket formation**: any list of symmetric (count-
    balanced) atoms concatenates into a symmetric collective.

    Formal Lean witness for the §2.1 claim of `Emergent_Markov_Blankets.md`:
    a resonating group `G` of `N` atoms forms a Markov blanket whose
    boundary satisfies the count-balance half of ZFA. The Pauli-closure
    half is a runtime-checked invariant (`twist_core.py`, `zfa-core`
    Rust kernel) whose Lean formalisation remains open work
    (`pauli_closed_of_admissible_zfa`, per Experimental_Consistency.md
    §2.1 and the CLAUDE.md note that the runtime layer requires more
    than count balance). -/
theorem emergent_blanket_formation
    (atoms : List TopoString) (h : ∀ a ∈ atoms, is_symmetric a) :
    is_symmetric (atoms.foldr (· ++ ·) []) := by
  induction atoms with
  | nil =>
    unfold is_symmetric
    simp [count_pos, count_neg]
  | cons head tail ih =>
    simp only [List.foldr]
    apply emergent_blanket_formation_binary
    · exact h head (List.Mem.head _)
    · apply ih
      intro a ha
      exact h a (List.Mem.tail _ ha)
