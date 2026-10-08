import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Image
import Mathlib.Order.Basic

set_option linter.unusedVariables false
set_option linter.unusedSectionVars false

/-!
# QLF_DeterministicConsensus — threshold agreement as a pure function, and its safety

The evaluation half of deterministic consensus, stated directly. A fixed policy names the
signers `N` (`|N| = n`) and a threshold `k`. Each signer signs a value for **one** event; the
binding of a signature to that event, policy and epoch is cryptographic and lives outside Lean.
What a verifier holds after checking signatures is a finite set `A` of attestations
`(signer, value)` for that event.

* **`Accepted k A v`** — at least `k` distinct signers back `v`.
* **`Equivocates A s`** — `s` signed two different values: provable misbehaviour, since the
  two attestations together are the evidence (`equivocation_is_evidence`).

## Results (no axioms)

* **`outcome_toFinset_perm`, `outcome_toFinset_dup`** — the outcome depends only on the *set*
  of attestations: arrival order and duplicates cannot change it (determinism).
* **`quorum_intersection_safety`** — if every equivocating signer is among at most `f` faulty
  signers and `n + f < 2k`, no two different values can both be accepted. This is the
  classical quorum-intersection bound (`k > (n+f)/2`; with `n = 3f+1`, `k = 2f+1`).
* **`accepted_monotone`**, **`outcome_stable`** — more attestations can turn *insufficient*
  into *accepted*, never one accepted value into another.
* **`outcome_eq_accepted_iff`** — under the safety bound, the (classically chosen) outcome is
  `accepted v` exactly when `v` reaches the threshold: the choice is forced, so the result is
  a function of the inputs.
* **`split_without_bound`** — without the bound, two honest signers on different values
  both reach a threshold of `1`: the hypothesis is doing work.

## Signatures, Byzantine signers and replay (no axioms)

Signatures enter as an abstract `Scheme` with **unforgeability as a hypothesis** on each honest
signer's key (`Unforgeable`), not as an axiom: Lean cannot prove a cryptographic assumption,
so every theorem holds for any scheme that meets it. Each signature covers a `Context`
(protocol tag, policy, event, epoch); `admit` keeps the statements for one context, from the
policy's signers, that verify.

* **`honest_never_equivocates`** — no messages a Byzantine signer injects can make an honest
  signer appear to equivocate.
* **`byzantine_safety`** — honest signers `H` (unforgeable, one value per context), the rest
  arbitrary with `|N \ H| ≤ f`, `n + f < 2k`: at most one value is accepted, for any bag.
* **`admitted_was_issued_in_context`** — **context binding**: unforgeability is stated over the
  whole message `(context, value)`, so a statement admitted for context `c` under an honest
  signer's key was issued by that signer *in `c`*. Replaying a signature from another context
  (or editing a statement's declared `ctx`) can only be admitted if the scheme verifies it
  under `c`, which an unforgeable scheme does only for statements actually issued in `c`.
* **`context_ignoring_scheme_not_unforgeable`** — the hypothesis has teeth: a scheme whose
  verification ignores the context fails `Unforgeable` for any honest signer that signs in one
  context and not another. Context binding is therefore a property the scheme must provide.
* **`admit_insert_other_ctx`**, **`outcome_ignores_other_declared_context`** — declared-context
  filtering: a statement whose declared context differs from `c` changes nothing. This step is
  bookkeeping; the cryptographic content is `admitted_was_issued_in_context`.

## What this does not cover

Two verifiers holding *different subsets* can still disagree: one sees *accepted*, the other
*insufficient*. They can never accept two different values (`quorum_intersection_safety`
applied to the union). Making every verifier hold the same set under message loss is
consensus proper, which no deterministic protocol solves in full asynchrony (FLP 1985); a
BFT protocol or a finalized log (e.g. rchain-rust's Casper finality) supplies that.
-/

namespace QLF.Consensus

variable {σ α : Type*} [DecidableEq σ] [DecidableEq α]

/-- The signers backing `v` in an attestation set. -/
def support (A : Finset (σ × α)) (v : α) : Finset σ :=
  (A.filter (fun a => a.2 = v)).image Prod.fst

/-- `v` reaches the threshold: at least `k` distinct signers back it. -/
def Accepted (k : ℕ) (A : Finset (σ × α)) (v : α) : Prop := k ≤ (support A v).card

/-- `s` signed two different values for the same event. -/
def Equivocates (A : Finset (σ × α)) (s : σ) : Prop :=
  ∃ v w, v ≠ w ∧ (s, v) ∈ A ∧ (s, w) ∈ A

/-- The outcomes a verifier can report. -/
inductive Outcome (α : Type*) where
  | accepted (v : α)
  | insufficient
deriving DecidableEq

/-- The evaluation function. -/
noncomputable def outcome (k : ℕ) (A : Finset (σ × α)) : Outcome α :=
  open Classical in
  if h : ∃ v, Accepted k A v then .accepted (Classical.choose h) else .insufficient

theorem mem_support {A : Finset (σ × α)} {v : α} {s : σ} :
    s ∈ support A v ↔ (s, v) ∈ A := by
  unfold support
  simp only [Finset.mem_image, Finset.mem_filter, Prod.exists]
  constructor
  · rintro ⟨s', v', ⟨hm, rfl⟩, rfl⟩; exact hm
  · intro h; exact ⟨s, v, ⟨h, rfl⟩, rfl⟩

/-- Two attestations by one signer on different values are the proof of equivocation. -/
theorem equivocation_is_evidence {A : Finset (σ × α)} {s : σ} {v w : α}
    (hv : s ∈ support A v) (hw : s ∈ support A w) (hne : v ≠ w) : Equivocates A s :=
  ⟨v, w, hne, mem_support.mp hv, mem_support.mp hw⟩

-- ==========================================
-- Determinism: only the set matters
-- ==========================================

/-- Arrival order cannot change the outcome. -/
theorem outcome_toFinset_perm (k : ℕ) {l l' : List (σ × α)} (h : l.Perm l') :
    outcome k l.toFinset = outcome k l'.toFinset := by
  rw [List.toFinset_eq_of_perm l l' h]

/-- Duplicated attestations cannot change the outcome. -/
theorem outcome_toFinset_dup (k : ℕ) (l : List (σ × α)) :
    outcome k (l ++ l).toFinset = outcome k l.toFinset := by
  rw [List.toFinset_append, Finset.union_self]

-- ==========================================
-- Safety: quorum intersection
-- ==========================================

/-- **Quorum-intersection safety.** Signers come from `N` (`|N| = n`); every equivocator is in
    `F` (`|F| ≤ f`); `n + f < 2k`. Then two accepted values are equal. -/
theorem quorum_intersection_safety {k f : ℕ} {N F : Finset σ} {A : Finset (σ × α)}
    (hN : ∀ a ∈ A, a.1 ∈ N) (hF : ∀ s, Equivocates A s → s ∈ F) (hf : F.card ≤ f)
    (hk : N.card + f < 2 * k) {v w : α} (hv : Accepted k A v) (hw : Accepted k A w) :
    v = w := by
  by_contra hne
  have hsubN : support A v ∪ support A w ⊆ N := by
    intro s hs
    rcases Finset.mem_union.mp hs with h | h
    · exact hN _ (mem_support.mp h)
    · exact hN _ (mem_support.mp h)
  have hsubF : support A v ∩ support A w ⊆ F := by
    intro s hs
    obtain ⟨h₁, h₂⟩ := Finset.mem_inter.mp hs
    exact hF s (equivocation_is_evidence h₁ h₂ hne)
  have hU := Finset.card_le_card hsubN
  have hI := Finset.card_le_card hsubF
  have hUI := Finset.card_union_add_card_inter (support A v) (support A w)
  unfold Accepted at hv hw
  omega

-- ==========================================
-- Monotonicity and the forced outcome
-- ==========================================

/-- More attestations never remove support. -/
theorem accepted_monotone {k : ℕ} {A A' : Finset (σ × α)} (hsub : A ⊆ A') {v : α}
    (h : Accepted k A v) : Accepted k A' v := by
  unfold Accepted at h ⊢
  refine le_trans h (Finset.card_le_card ?_)
  intro s hs
  exact mem_support.mpr (hsub (mem_support.mp hs))

/-- **The outcome is forced.** Under the safety bound, `outcome` reports `accepted v` exactly
    when `v` reaches the threshold — the classical choice inside `outcome` has nothing to choose. -/
theorem outcome_eq_accepted_iff {k f : ℕ} {N F : Finset σ} {A : Finset (σ × α)}
    (hN : ∀ a ∈ A, a.1 ∈ N) (hF : ∀ s, Equivocates A s → s ∈ F) (hf : F.card ≤ f)
    (hk : N.card + f < 2 * k) (v : α) :
    outcome k A = .accepted v ↔ Accepted k A v := by
  unfold outcome
  constructor
  · intro h
    split_ifs at h with hex
    · cases h; exact Classical.choose_spec hex
  · intro hv
    have hex : ∃ v, Accepted k A v := ⟨v, hv⟩
    rw [dif_pos hex]
    congr 1
    exact quorum_intersection_safety hN hF hf hk (Classical.choose_spec hex) hv

/-- **Stability.** Once `v` is accepted on `A`, every superset that still satisfies the safety
    hypotheses reports `accepted v`: new inputs cannot flip the result to another value. -/
theorem outcome_stable {k f : ℕ} {N F : Finset σ} {A A' : Finset (σ × α)} (hsub : A ⊆ A')
    (hN : ∀ a ∈ A', a.1 ∈ N) (hF : ∀ s, Equivocates A' s → s ∈ F) (hf : F.card ≤ f)
    (hk : N.card + f < 2 * k) {v : α} (hv : Accepted k A v) :
    outcome k A' = .accepted v :=
  (outcome_eq_accepted_iff hN hF hf hk v).mpr (accepted_monotone hsub hv)

/-- **The bound is needed.** With two signers, each signing a different value and neither
    equivocating (`F = ∅`, `f = 0`), threshold `k = 1` violates `n + f < 2k` and two different
    values are accepted. -/
theorem split_without_bound :
    let A : Finset (Bool × Bool) := {(false, false), (true, true)}
    Accepted 1 A false ∧ Accepted 1 A true ∧ (∀ s, ¬ Equivocates A s) := by
  refine ⟨by unfold Accepted; decide, by unfold Accepted; decide, ?_⟩
  rintro s ⟨v, w, hne, hv, hw⟩
  simp only [Finset.mem_insert, Finset.mem_singleton, Prod.mk.injEq] at hv hw
  rcases hv with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩ <;> rcases hw with ⟨h, rfl⟩ | ⟨h, rfl⟩ <;> simp_all

-- ==========================================
-- Signatures, Byzantine signers and replay
-- ==========================================

/-- What a signature is bound to: protocol tag, policy (signer set and threshold), the exact
    event, and the epoch. In practice each field is a hash; here they are opaque tags. -/
structure Context where
  domain : ℕ
  policy : ℕ
  event : ℕ
  epoch : ℕ
deriving DecidableEq, Repr

/-- A signed statement as received: who, in which context, which value, and the signature. -/
structure Signed (σ α Sig : Type*) where
  signer : σ
  ctx : Context
  value : α
  sig : Sig
deriving DecidableEq

/-- An abstract signature scheme over `(context, value)` messages. -/
structure Scheme (σ α Sig : Type*) where
  verify : σ → Context → α → Sig → Bool

variable {Sig : Type*} [DecidableEq Sig]

/-- **Unforgeability, as a hypothesis on a scheme and a signer.** Every statement that verifies
    under `s`'s key was actually issued by `s` (`issued` is `s`'s own signing log). This is the
    cryptographic assumption (EUF-CMA in the standard model); it is a premise, not an axiom. -/
def Unforgeable (S : Scheme σ α Sig) (issued : σ → Context → α → Prop) (s : σ) : Prop :=
  ∀ c v sg, S.verify s c v sg = true → issued s c v

/-- **An honest signer issues at most one value per context.** -/
def HonestLog (issued : σ → Context → α → Prop) (s : σ) : Prop :=
  ∀ c v w, issued s c v → issued s c w → v = w

/-- **Admission.** From a bag of received statements, keep those for context `c`, from a signer
    in the policy's set `N`, whose signature verifies; reduce each to `(signer, value)`. -/
def admit (S : Scheme σ α Sig) (N : Finset σ) (c : Context) (R : Finset (Signed σ α Sig)) :
    Finset (σ × α) :=
  (R.filter (fun m => m.ctx = c ∧ m.signer ∈ N ∧ S.verify m.signer m.ctx m.value m.sig = true)).image
    (fun m => (m.signer, m.value))

theorem mem_admit {S : Scheme σ α Sig} {N : Finset σ} {c : Context} {R : Finset (Signed σ α Sig)}
    {s : σ} {v : α} :
    (s, v) ∈ admit S N c R ↔
      ∃ m ∈ R, m.signer = s ∧ m.value = v ∧ m.ctx = c ∧ s ∈ N ∧ S.verify s c v m.sig = true := by
  unfold admit
  simp only [Finset.mem_image, Finset.mem_filter, Prod.mk.injEq]
  constructor
  · rintro ⟨m, ⟨hm, hc, hN, hv⟩, rfl, rfl⟩
    exact ⟨m, hm, rfl, rfl, hc, hN, hc ▸ hv⟩
  · rintro ⟨m, hm, rfl, rfl, hc, hN, hv⟩
    exact ⟨m, ⟨hm, hc, hN, hc ▸ hv⟩, rfl, rfl⟩

/-- **Declared-context filtering.** A statement declaring any other context (another event, policy, epoch or
    protocol) contributes nothing to the evaluation of `c`. -/
theorem admit_insert_other_ctx (S : Scheme σ α Sig) (N : Finset σ) {c : Context}
    (R : Finset (Signed σ α Sig)) {m : Signed σ α Sig} (h : m.ctx ≠ c) :
    admit S N c (insert m R) = admit S N c R := by
  unfold admit
  rw [Finset.filter_insert]
  simp [h]

/-- Every admitted signer is in the policy's signer set. -/
theorem admit_signers_in_policy (S : Scheme σ α Sig) (N : Finset σ) (c : Context)
    (R : Finset (Signed σ α Sig)) : ∀ a ∈ admit S N c R, a.1 ∈ N := by
  rintro ⟨s, v⟩ h
  obtain ⟨-, -, -, -, -, hN, -⟩ := mem_admit.mp h
  exact hN

/-- **Honest signers cannot be framed.** If `s`'s key is unforgeable and `s` signs one value
    per context, no bag of messages — whatever Byzantine signers inject — makes `s` equivocate
    in the admitted set. -/
theorem honest_never_equivocates {S : Scheme σ α Sig} {issued : σ → Context → α → Prop}
    {N : Finset σ} {c : Context} {R : Finset (Signed σ α Sig)} {s : σ}
    (hu : Unforgeable S issued s) (hl : HonestLog issued s) :
    ¬ Equivocates (admit S N c R) s := by
  rintro ⟨v, w, hne, hv, hw⟩
  obtain ⟨_, _, -, -, -, -, sv⟩ := mem_admit.mp hv
  obtain ⟨_, _, -, -, -, -, sw⟩ := mem_admit.mp hw
  exact hne (hl c v w (hu c v _ sv) (hu c w _ sw))

/-- **Byzantine-tolerant safety, end to end.** A policy names signers `N` (`|N| = n`); the honest
    ones `H` have unforgeable keys and sign one value per context; the rest (`N \ H`, at most `f`)
    may do anything — sign several values, withhold, or inject arbitrary messages. If
    `n + f < 2k`, then for any received bag `R` at most one value is accepted for context `c`. -/
theorem byzantine_safety {S : Scheme σ α Sig} {issued : σ → Context → α → Prop}
    {N H : Finset σ} {k f : ℕ} {c : Context} {R : Finset (Signed σ α Sig)}
    (hu : ∀ s ∈ H, Unforgeable S issued s) (hl : ∀ s ∈ H, HonestLog issued s)
    (hf : (N \ H).card ≤ f) (hk : N.card + f < 2 * k) {v w : α}
    (hv : Accepted k (admit S N c R) v) (hw : Accepted k (admit S N c R) w) : v = w := by
  refine quorum_intersection_safety (admit_signers_in_policy S N c R) ?_ hf hk hv hw
  intro s hs
  obtain ⟨v', w', -, hv', -⟩ := id hs
  have hN : s ∈ N := admit_signers_in_policy S N c R (s, v') hv'
  refine Finset.mem_sdiff.mpr ⟨hN, fun hH => ?_⟩
  exact honest_never_equivocates (hu s hH) (hl s hH) hs

/-- **Declared-context filtering, at the verdict.** Adding statements that declare other contexts leaves the
    evaluation of `c` exactly as it was. -/
theorem outcome_ignores_other_declared_context (S : Scheme σ α Sig) (N : Finset σ) (k : ℕ) {c : Context}
    (R : Finset (Signed σ α Sig)) {m : Signed σ α Sig} (h : m.ctx ≠ c) :
    outcome k (admit S N c (insert m R)) = outcome k (admit S N c R) := by
  rw [admit_insert_other_ctx S N R h]

/-- **Context binding.** If an honest signer's key is unforgeable, anything admitted for
    context `c` under that key was issued by the signer in `c` — not in some other context
    whose signature was replayed or relabeled. -/
theorem admitted_was_issued_in_context {S : Scheme σ α Sig} {issued : σ → Context → α → Prop}
    {N : Finset σ} {c : Context} {R : Finset (Signed σ α Sig)} {s : σ} {v : α}
    (hu : Unforgeable S issued s) (h : (s, v) ∈ admit S N c R) : issued s c v := by
  obtain ⟨m, -, -, -, -, -, hv⟩ := mem_admit.mp h
  exact hu c v m.sig hv

/-- **A context-ignoring scheme is not unforgeable.** If verification gives the same answer in
    every context, a signer who issued `v` in `c` but not in `c'` has a forgeable key: the same
    signature verifies in `c'`. So `Unforgeable` excludes such schemes; context binding is a
    requirement on the scheme, not something filtering supplies. -/
theorem context_ignoring_scheme_not_unforgeable {S : Scheme σ α Sig}
    {issued : σ → Context → α → Prop} {s : σ} {c c' : Context} {v : α} {sg : Sig}
    (hign : ∀ d d', S.verify s d v sg = S.verify s d' v sg)
    (hsig : S.verify s c v sg = true) (hnot : ¬ issued s c' v) :
    ¬ Unforgeable S issued s := by
  intro hu
  exact hnot (hu c' v sg (by rw [hign c' c]; exact hsig))

end QLF.Consensus
