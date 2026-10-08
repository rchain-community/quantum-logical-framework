import QLF_TwistAlphabet

set_option linter.unusedVariables false
set_option linter.unusedSectionVars false

/-!
# QLF_TrustClosure — trust links as twist histories, and what balance can and cannot see

A **trust ledger** is a list of signed links: `issuer` vouches for `subject` in a `slot`
(an attribute or role that should have one value per issuer). Signatures are outside this
module; a ledger here is what a verifier holds *after* checking them.

## The encoding (proved)

Reciprocity is **indexed by slot**: a link `a → b` in one role is answered only by a link
`b → a` in the *same* role. For a pair of distinct parties `a ≠ b` and a slot `s`, a link
`a → b` in `s` is the twist `^` and a link `b → a` in `s` is its Hermitian conjugate `v`;
links between other parties or in other slots contribute nothing (`pairHistory`). Then:

* **`pairHistory_countBalanced_iff`** — the `(a, b, s)` history is count-balanced **iff** the
  links are reciprocated in that slot, `flow L a b s = 0`.
* **`reciprocated_pair_pauli_closed`** — so a reciprocated pair is a full ZFA closure: its
  ordered Pauli fold is a scalar in `{±I, ±iI}` (via `count_balanced_pauli_closed`).
* **`handshake_reciprocated`** — a tap that produces `a → b` and `b → a` in one slot is
  reciprocated, so "no dangling trust debt" has a precise meaning: `Reciprocated L`, flow zero
  on every pair in every slot.
* **`mismatched_slot_not_reciprocated`** — `a → b` in one role answered by `b → a` in another
  role is **not** reciprocated: the debt stays open in both slots.

## What balance cannot see (proved — the honest boundary)

* **`reciprocated_append`** — closures compose: two reciprocated ledgers concatenate to a
  reciprocated ledger.
* **`balance_blind_to_equivocation`** — therefore ZFA balance **cannot detect equivocation**.
  Party `0` completes one honest handshake with `1` and another with `2`, both in slot `0`
  (two different values for one slot). Each ledger alone is reciprocated and equivocation-free;
  the union is still reciprocated, yet it equivocates.
* **`equivocation_monotone`** — equivocation is detected only by a verifier that holds *both*
  conflicting links; adding links never hides it.

So the identity claim "double-representation is pruned by ZFA" is false as stated: balance
and uniqueness are independent predicates, and catching an equivocation across separate
verifiers needs the two links to meet (gossip or a shared log). See
`QLF_DeterministicConsensus` for the threshold side.
-/

namespace QLF.Trust

open QLF

/-- A signed trust link: `issuer` vouches for `subject` in `slot`. -/
structure Link where
  issuer : ℕ
  subject : ℕ
  slot : ℕ
deriving DecidableEq, Repr

/-- A verifier's ledger: the signature-checked links it holds. -/
abbrev Ledger := List Link

/-- Number of links `a → b` in slot `s`. -/
def linkCount (L : Ledger) (a b s : ℕ) : ℕ :=
  L.countP (fun l => l.issuer == a && l.subject == b && l.slot == s)

/-- Net trust flow from `a` to `b` in slot `s`: links `a → b` minus links `b → a`, both in `s`. -/
def flow (L : Ledger) (a b s : ℕ) : ℤ :=
  (linkCount L a b s : ℤ) - (linkCount L b a s : ℤ)

/-- **No dangling trust debt**: every pair's links are reciprocated within every slot. -/
def Reciprocated (L : Ledger) : Prop := ∀ a b s, flow L a b s = 0

/-- The twist a single link contributes to the `(a, b, s)` history:
    `a → b` in `s` is `^`, `b → a` in `s` is its conjugate `v`, anything else is silent. -/
def encode (a b s : ℕ) (l : Link) : List Twist :=
  if l.issuer == a && l.subject == b && l.slot == s then [Twist.up]
  else if l.issuer == b && l.subject == a && l.slot == s then [Twist.down]
  else []

/-- The twist history of the pair `(a, b)` in slot `s`, read off a ledger. -/
def pairHistory (L : Ledger) (a b s : ℕ) : List Twist := L.flatMap (encode a b s)

/-- **An issuer equivocates**: it signed two links in one slot naming different subjects. -/
def Equivocates (L : Ledger) (i : ℕ) : Prop :=
  ∃ l₁ ∈ L, ∃ l₂ ∈ L, l₁.issuer = i ∧ l₂.issuer = i ∧ l₁.slot = l₂.slot ∧ l₁.subject ≠ l₂.subject

-- ==========================================
-- Counting the encoded history
-- ==========================================

private theorem count_encode_up (a b s : ℕ) (hab : a ≠ b) (l : Link) :
    (encode a b s l).count Twist.up =
      if (l.issuer == a && l.subject == b && l.slot == s) then 1 else 0 := by
  unfold encode
  by_cases h₁ : (l.issuer == a && l.subject == b && l.slot == s) = true
  · simp only [h₁, if_true]; decide
  · by_cases h₂ : (l.issuer == b && l.subject == a && l.slot == s) = true
    · simp only [h₁, h₂, if_true, if_false, Bool.false_eq_true]; decide
    · simp only [h₁, h₂, if_false, Bool.false_eq_true]; decide

private theorem count_encode_down (a b s : ℕ) (hab : a ≠ b) (l : Link) :
    (encode a b s l).count Twist.down =
      if (l.issuer == b && l.subject == a && l.slot == s) then 1 else 0 := by
  unfold encode
  by_cases h₁ : (l.issuer == a && l.subject == b && l.slot == s) = true
  · have h₂ : (l.issuer == b && l.subject == a && l.slot == s) = false := by
      simp only [Bool.and_eq_true, beq_iff_eq] at h₁
      obtain ⟨⟨hi, _⟩, _⟩ := h₁
      simp only [Bool.and_eq_false_iff, beq_eq_false_iff_ne]
      left; left; rw [hi]; exact hab
    simp only [h₁, h₂, if_true]; decide
  · by_cases h₂ : (l.issuer == b && l.subject == a && l.slot == s) = true
    · simp only [h₁, h₂, if_true, if_false, Bool.false_eq_true]; decide
    · simp only [h₁, h₂, if_false, Bool.false_eq_true]; decide

private theorem count_encode_other (a b s : ℕ) (l : Link) (t : Twist)
    (ht₁ : t ≠ Twist.up) (ht₂ : t ≠ Twist.down) : (encode a b s l).count t = 0 := by
  unfold encode
  cases t <;> split_ifs <;> first | decide | exact absurd rfl ht₁ | exact absurd rfl ht₂

private theorem count_pairHistory_up (L : Ledger) (a b s : ℕ) (hab : a ≠ b) :
    (pairHistory L a b s).count Twist.up = linkCount L a b s := by
  induction L with
  | nil => simp [pairHistory, linkCount]
  | cons l L ih =>
    simp only [pairHistory, linkCount] at ih ⊢
    rw [List.flatMap_cons, List.count_append, ih, count_encode_up a b s hab, List.countP_cons]
    split_ifs <;> omega

private theorem count_pairHistory_down (L : Ledger) (a b s : ℕ) (hab : a ≠ b) :
    (pairHistory L a b s).count Twist.down = linkCount L b a s := by
  induction L with
  | nil => simp [pairHistory, linkCount]
  | cons l L ih =>
    simp only [pairHistory, linkCount] at ih ⊢
    rw [List.flatMap_cons, List.count_append, ih, count_encode_down a b s hab, List.countP_cons]
    split_ifs <;> omega

private theorem count_pairHistory_other (L : Ledger) (a b s : ℕ) (t : Twist)
    (ht₁ : t ≠ Twist.up) (ht₂ : t ≠ Twist.down) : (pairHistory L a b s).count t = 0 := by
  induction L with
  | nil => simp [pairHistory]
  | cons l L ih =>
    simp only [pairHistory] at ih ⊢
    rw [List.flatMap_cons, List.count_append, ih, count_encode_other a b s l t ht₁ ht₂]

-- ==========================================
-- The encoding theorem
-- ==========================================

/-- **The `(a, b, s)` history is a ZFA closure iff the pair's links in slot `s` are
    reciprocated.** -/
theorem pairHistory_countBalanced_iff (L : Ledger) {a b : ℕ} (s : ℕ) (hab : a ≠ b) :
    countBalanced (pairHistory L a b s) ↔ flow L a b s = 0 := by
  unfold countBalanced flow
  rw [count_pairHistory_up L a b s hab, count_pairHistory_down L a b s hab,
    count_pairHistory_other L a b s Twist.left (by decide) (by decide),
    count_pairHistory_other L a b s Twist.right (by decide) (by decide),
    count_pairHistory_other L a b s Twist.slash (by decide) (by decide),
    count_pairHistory_other L a b s Twist.backslash (by decide) (by decide),
    count_pairHistory_other L a b s Twist.plus (by decide) (by decide),
    count_pairHistory_other L a b s Twist.minus (by decide) (by decide)]
  constructor
  · rintro ⟨h, -, -, -⟩; omega
  · intro h; exact ⟨by omega, rfl, rfl, rfl⟩

/-- **A reciprocated pair is a full ZFA closure**: its ordered Pauli fold is a scalar. -/
theorem reciprocated_pair_pauli_closed (L : Ledger) {a b : ℕ} (s : ℕ) (hab : a ≠ b)
    (h : flow L a b s = 0) :
    ∃ p : PauliScalar, twistMatrixFold (pairHistory L a b s) = pauliScalarToMatrix p :=
  count_balanced_pauli_closed ((pairHistory_countBalanced_iff L s hab).mpr h)

/-- A ledger with no dangling debt makes every pair of distinct parties, in every slot, a
    ZFA closure. -/
theorem reciprocated_all_pairs_closed {L : Ledger} (h : Reciprocated L) {a b : ℕ} (s : ℕ)
    (hab : a ≠ b) : countBalanced (pairHistory L a b s) :=
  (pairHistory_countBalanced_iff L s hab).mpr (h a b s)

-- ==========================================
-- Handshakes and composition
-- ==========================================

private theorem linkCount_append (L₁ L₂ : Ledger) (a b s : ℕ) :
    linkCount (L₁ ++ L₂) a b s = linkCount L₁ a b s + linkCount L₂ a b s := by
  simp [linkCount, List.countP_append]

/-- **Closures compose**: concatenating reciprocated ledgers stays reciprocated. -/
theorem reciprocated_append {L₁ L₂ : Ledger} (h₁ : Reciprocated L₁) (h₂ : Reciprocated L₂) :
    Reciprocated (L₁ ++ L₂) := by
  intro a b s
  have e₁ := h₁ a b s
  have e₂ := h₂ a b s
  unfold flow at e₁ e₂ ⊢
  rw [linkCount_append, linkCount_append]
  push_cast
  omega

/-- **A tap handshake is reciprocated**: `i → j` and `j → i`, in the same slot. -/
theorem handshake_reciprocated (i j s : ℕ) :
    Reciprocated [⟨i, j, s⟩, ⟨j, i, s⟩] := by
  intro a b t
  unfold flow linkCount
  simp only [List.countP_cons, List.countP_nil]
  by_cases hi : i = a <;> by_cases hj : j = b <;> by_cases hj' : j = a <;> by_cases hi' : i = b <;>
    by_cases hs : s = t <;> simp_all

/-- **Answering in another role is not reciprocation.** `i → j` in slot `s` and `j → i` in a
    different slot `s'` leave a debt open in slot `s`. -/
theorem mismatched_slot_not_reciprocated {i j s s' : ℕ} (hij : i ≠ j) (hs : s ≠ s') :
    ¬ Reciprocated [⟨i, j, s⟩, ⟨j, i, s'⟩] := by
  intro h
  have e := h i j s
  unfold flow linkCount at e
  simp [List.countP_cons, hij, Ne.symm hij, Ne.symm hs] at e

-- ==========================================
-- What balance cannot see
-- ==========================================

/-- Equivocation is never hidden by holding more links. -/
theorem equivocation_monotone {L L' : Ledger} (hsub : ∀ l ∈ L, l ∈ L') {i : ℕ}
    (h : Equivocates L i) : Equivocates L' i := by
  obtain ⟨l₁, h₁, l₂, h₂, e₁, e₂, es, ne⟩ := h
  exact ⟨l₁, hsub l₁ h₁, l₂, hsub l₂ h₂, e₁, e₂, es, ne⟩

/-- Honest handshake of party `0` with party `1` in slot `0`. -/
def tapWith1 : Ledger := [⟨0, 1, 0⟩, ⟨1, 0, 0⟩]

/-- Honest-looking handshake of party `0` with party `2` in the same slot `0`. -/
def tapWith2 : Ledger := [⟨0, 2, 0⟩, ⟨2, 0, 0⟩]

/-- **ZFA balance is blind to equivocation.** Each ledger alone is reciprocated (a closure)
    and shows no equivocation; their union is still reciprocated, yet party `0` has named two
    different subjects in one slot. Two verifiers holding one ledger each cannot detect it. -/
theorem balance_blind_to_equivocation :
    Reciprocated tapWith1 ∧ Reciprocated tapWith2 ∧
    ¬ Equivocates tapWith1 0 ∧ ¬ Equivocates tapWith2 0 ∧
    Reciprocated (tapWith1 ++ tapWith2) ∧ Equivocates (tapWith1 ++ tapWith2) 0 := by
  have r₁ : Reciprocated tapWith1 := handshake_reciprocated 0 1 0
  have r₂ : Reciprocated tapWith2 := handshake_reciprocated 0 2 0
  refine ⟨r₁, r₂, ?_, ?_, reciprocated_append r₁ r₂, ?_⟩
  · rintro ⟨l₁, h₁, l₂, h₂, e₁, e₂, -, ne⟩
    simp only [tapWith1, List.mem_cons, List.not_mem_nil, or_false] at h₁ h₂
    rcases h₁ with rfl | rfl <;> rcases h₂ with rfl | rfl <;> simp_all
  · rintro ⟨l₁, h₁, l₂, h₂, e₁, e₂, -, ne⟩
    simp only [tapWith2, List.mem_cons, List.not_mem_nil, or_false] at h₁ h₂
    rcases h₁ with rfl | rfl <;> rcases h₂ with rfl | rfl <;> simp_all
  · exact ⟨⟨0, 1, 0⟩, by simp [tapWith1], ⟨0, 2, 0⟩, by simp [tapWith2], rfl, rfl, rfl, by decide⟩

end QLF.Trust
