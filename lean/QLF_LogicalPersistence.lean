import QLF_ReachableEvent
import Mathlib.Data.Set.Basic

set_option linter.unusedVariables false

/-!
# QLF_LogicalPersistence — from "nature is logical" to "construction only adds" and "no time loops"

`QLF_NoTimeLoops` derives *no time loops* from *construction only adds*, and `QLF_ConstructionAdds`
proves that every construction operator QLF defines only adds. Neither assumes that nature *is* QLF's
construction, but together they leave open why a lawful universe could not have a construction that
subtracts. This module answers that from the one assumption QLF is entitled to: **nature is logical** —
the laws of logic hold at every state of the world.

The setting is the standard semantics of constructive logic (Kripke 1965). States of the world are
ordered by `le w v` ("`v` can follow `w`", reflexive and transitive), atomic facts hold at states, and
implication is read across the future: `φ → ψ` holds at `w` when every later state where `φ` holds has
`ψ`. Nothing else is assumed — not lists, not twists, not QLF's dynamics.

* **`weakening_iff_persistence`** — the logical law of *weakening*, `p → (⊤ → p)` (valid in classical
  and constructive logic alike), holds at every state **iff** every established fact stays established
  at every later state. So "only adds" is not a further postulate: it is what the law means across time.
* **`forces_persistent`** — persistence of atomic facts extends to every formula.
* **`facts_only_grow`** — the facts holding at a state are contained in those holding at any later state.
* **`loop_same_facts`** — two states that each follow the other hold exactly the same facts, so a loop
  can only return to a state indistinguishable from where it began.
* **`no_time_loops_from_logic`** — an *event* is a step to a later state where some new fact holds; no
  chain of events of any length returns to its start. The proof needs only weakening.
* **`histories_are_a_model`** — QLF's histories, ordered by `reachable` with "`A` lies in my past" as
  the facts, satisfy persistence: the construction is one model of the law, not the assumption.

## Honest scope

The assumption is that the world's states form a Kripke frame in which weakening holds — "nature is
logical", read in the semantics constructive logic already uses (QLF's core is constructive,
`Intuitionistic_Logic.md`). From it alone, persistence and the absence of eventful time loops are
theorems. What it does not give is a metric, a dimension, or the field equations: those still come
through QLF's construction and the order→metric bridge. A loop through states that agree on every fact
is not excluded, because nothing happens on it; it is the same state. No axioms.
-/

namespace QLF.LogicalPersistence

/-- Formulas: atomic facts, truth, and implication. -/
inductive Form (A : Type _) where
  | atom : A → Form A
  | top : Form A
  | imp : Form A → Form A → Form A

/-- **A logical world.** States `W` ordered by `le` ("can follow"), reflexive and transitive, with a
    valuation saying which atomic facts hold at which state. -/
structure World (W A : Type _) where
  le : W → W → Prop
  le_refl : ∀ w, le w w
  le_trans : ∀ {u v w}, le u v → le v w → le u w
  val : A → W → Prop

variable {W A : Type _}

/-- What holds at a state. Implication is read across the future, as constructive logic requires. -/
def forces (M : World W A) : W → Form A → Prop
  | w, .atom a => M.val a w
  | _, .top => True
  | w, .imp φ ψ => ∀ v, M.le w v → forces M v φ → forces M v ψ

/-- **Persistence**: an established atomic fact stays established at every later state. -/
def Persistent (M : World W A) : Prop := ∀ a w v, M.le w v → M.val a w → M.val a v

/-- The law of weakening, `p → (⊤ → p)`, for the atomic fact `a`. -/
def weakening (a : A) : Form A := .imp (.atom a) (.imp .top (.atom a))

/-- **Weakening holds everywhere iff facts persist.** The forward direction is "nature is logical ⟹
    construction only adds": the law, read at the earlier state, delivers the fact to every later one. -/
theorem weakening_iff_persistence (M : World W A) :
    (∀ w a, forces M w (weakening a)) ↔ Persistent M := by
  constructor
  · intro hK a w v hwv ha
    exact hK w a w (M.le_refl w) ha v hwv trivial
  · intro hP w a v _ ha u hvu _
    exact hP a v u hvu ha

/-- Persistence of atoms extends to every formula. -/
theorem forces_persistent (M : World W A) (hP : Persistent M) :
    ∀ (φ : Form A) {w v : W}, M.le w v → forces M w φ → forces M v φ
  | .atom a, _, _, hwv, h => hP a _ _ hwv h
  | .top, _, _, _, _ => trivial
  | .imp φ ψ, _, _, hwv, h => fun u hvu hφ => h u (M.le_trans hwv hvu) hφ

/-- **Facts only grow.** Everything that holds at `w` holds at every later state. -/
theorem facts_only_grow (M : World W A) (hP : Persistent M) {w v : W} (hwv : M.le w v) :
    {φ | forces M w φ} ⊆ {φ | forces M v φ} :=
  fun φ h => forces_persistent M hP φ hwv h

/-- **A loop changes nothing.** States that each follow the other hold exactly the same facts. -/
theorem loop_same_facts (M : World W A) (hP : Persistent M) {w v : W}
    (hwv : M.le w v) (hvw : M.le v w) (φ : Form A) : forces M w φ ↔ forces M v φ :=
  ⟨forces_persistent M hP φ hwv, forces_persistent M hP φ hvw⟩

/-- **An event**: a step to a later state at which some new fact holds. -/
def Event (M : World W A) (w v : W) : Prop :=
  M.le w v ∧ ∃ φ, forces M v φ ∧ ¬ forces M w φ

theorem event_chain_le (M : World W A) {a b : W} (h : Relation.TransGen (Event M) a b) :
    M.le a b := by
  induction h with
  | single hab => exact hab.1
  | tail _ hbc ih => exact M.le_trans ih hbc.1

/-- No chain of events ends at a state from which its start can follow. -/
theorem no_event_chain_back (M : World W A) (hP : Persistent M) {a b : W}
    (h : Relation.TransGen (Event M) a b) (hba : M.le b a) : False := by
  cases h with
  | single hab =>
    obtain ⟨_, φ, hb, ha⟩ := hab
    exact ha (forces_persistent M hP φ hba hb)
  | tail hac hcb =>
    obtain ⟨_, φ, hb, hc⟩ := hcb
    exact hc (forces_persistent M hP φ (M.le_trans hba (event_chain_le M hac)) hb)

/-- **No time loops, from logic alone.** If weakening holds at every state, no chain of events of any
    length returns to the state it started from. -/
theorem no_time_loops_from_logic (M : World W A) (hK : ∀ w a, forces M w (weakening a)) (w : W) :
    ¬ Relation.TransGen (Event M) w w :=
  fun h => no_event_chain_back M ((weakening_iff_persistence M).mp hK) h (M.le_refl w)

/-- **QLF's histories are a model.** Histories ordered by `reachable`, with "`A` lies in my past" as the
    fact `A`, form a logical world in which facts persist. -/
def historyWorld (α : Type _) : World (ReachableEvent.Event α) (ReachableEvent.Event α) where
  le := ReachableEvent.reachable
  le_refl := ReachableEvent.reachable_refl
  le_trans := fun h1 h2 => ReachableEvent.reachable_trans h1 h2
  val := fun A w => ReachableEvent.reachable A w

theorem histories_are_a_model (α : Type _) : Persistent (historyWorld α) :=
  fun _ _ _ hwv ha => ReachableEvent.reachable_trans ha hwv

end QLF.LogicalPersistence
