import QLF_QuantumTurbulence
import QLF_ClosureRenewal

/-!
# QLF_Duplex — the DNA duplex is a closure that carries no bit of its sequence

Companion to `Quantum_Biology.md` §2 and `quantum_biology_dna.py`.

Map the Watson–Crick pairs onto two conjugate twist pairs (`A ↦ >`, `T ↦ <`, `G ↦ ^`,
`C ↦ v`). Then:

1. the reverse complement of a strand IS its Hermitian dagger (`revcomp_is_dagger`), so a
   duplex `s · revcomp s` is the rung `w ++ dagger w`;
2. every such rung closes (`dagger_closes`, already in `QLF_QuantumTurbulence`), and its fold is
   exactly `(−1)^|w| · I` (`duplex_fold`) — the same matrix for **every** strand of a given
   length (`duplex_fold_sequence_blind`);
3. yet distinct strands give distinct duplexes (`duplex_injective`, `dna_duplex_injective`).

Together (`dna_duplex_order_not_fold`): the closure, and with it its fold, is constant on all
`4ⁿ` duplexes of length `n`, while the duplex itself still determines the sequence. So the
`2n` bits of a gene are held entirely in the order of the twists, the part ZFA does not
charge for, and none of them in the closure. This is Schrödinger's split of a gene into
persistence and specification, on the substrate. Through the renewal lemma of
`QLF_ClosureRenewal` the same holds for the duplex's future (`dna_duplex_renewal`,
`dna_duplex_future_blind`): the one sign a closure may pass on is fixed by length, so the
content can persist only as a copy held outside it (`Memetics_QLF.md` §4–§5). No axioms.
-/

namespace QLF.Duplex

open QLF

-- ==========================================
-- 1. The rung `w ++ dagger w` and its exact fold
-- ==========================================

theorem dagger_cons (a : Twist) (w : List Twist) :
    QuantumTurbulence.dagger (a :: w) = QuantumTurbulence.dagger w ++ [Twist.conj a] := by
  simp [QuantumTurbulence.dagger]

theorem length_dagger (w : List Twist) :
    (QuantumTurbulence.dagger w).length = w.length := by
  simp [QuantumTurbulence.dagger]

theorem fold_singleton (t : Twist) : twistMatrixFold [t] = t.toMatrix := by
  simp [twistMatrixFold]

/-- **The rung folds to `(−1)^|w| · I`.** Peel the outermost pair `a … conj a`: the inside is a
    scalar by induction, so it commutes out, and `a · conj a = −I`
    (`hermitian_pair_folds_to_negI`). -/
theorem duplex_fold (w : List Twist) :
    twistMatrixFold (w ++ QuantumTurbulence.dagger w) = ((-1 : ℂ) ^ w.length) • (1 : M) := by
  induction w with
  | nil => simp [QuantumTurbulence.dagger, twistMatrixFold]
  | cons a w ih =>
    have h1 : a :: w ++ QuantumTurbulence.dagger (a :: w)
        = [a] ++ (w ++ QuantumTurbulence.dagger w) ++ [Twist.conj a] := by
      simp [dagger_cons, List.append_assoc]
    rw [h1, ClosureRenewal.fold_append, ClosureRenewal.fold_append, ih, fold_singleton,
      fold_singleton, List.length_cons, Matrix.mul_smul, Matrix.mul_one, Matrix.smul_mul,
      hermitian_pair_folds_to_negI, pow_succ, mul_smul, neg_one_smul]

/-- **The fold does not see the strand.** Two strands of equal length give rungs with the same
    fold, whatever their twists. -/
theorem duplex_fold_sequence_blind {w w' : List Twist} (h : w.length = w'.length) :
    twistMatrixFold (w ++ QuantumTurbulence.dagger w)
      = twistMatrixFold (w' ++ QuantumTurbulence.dagger w') := by
  rw [duplex_fold, duplex_fold, h]

/-- **But the rung determines the strand.** The first half of `w ++ dagger w` is `w`. -/
theorem duplex_injective {w w' : List Twist}
    (h : w ++ QuantumTurbulence.dagger w = w' ++ QuantumTurbulence.dagger w') : w = w' := by
  have hlen := congrArg List.length h
  simp only [List.length_append, length_dagger] at hlen
  have hl : w.length = w'.length := by omega
  exact (List.append_inj h hl).1

-- ==========================================
-- 2. Watson–Crick pairing is the Hermitian dagger
-- ==========================================

/-- The four bases. -/
inductive Base where
  | A | T | G | C
deriving DecidableEq, Repr

/-- Watson–Crick complement. -/
def Base.comp : Base → Base
  | .A => .T
  | .T => .A
  | .G => .C
  | .C => .G

/-- The map onto two conjugate twist pairs: A/T on the x axis, G/C on the y axis. -/
def Base.toTwist : Base → Twist
  | .A => Twist.right
  | .T => Twist.left
  | .G => Twist.up
  | .C => Twist.down

/-- Reverse complement of a strand. -/
def revcomp (s : List Base) : List Base := (s.map Base.comp).reverse

theorem toTwist_comp (b : Base) : (Base.comp b).toTwist = Twist.conj b.toTwist := by
  cases b <;> rfl

/-- **The reverse complement is the dagger.** Complementing a base conjugates its twist, and both
    operations reverse the strand. -/
theorem revcomp_is_dagger (s : List Base) :
    (revcomp s).map Base.toTwist = QuantumTurbulence.dagger (s.map Base.toTwist) := by
  simp [revcomp, QuantumTurbulence.dagger, toTwist_comp, Function.comp_def]

/-- A hairpin duplex: the strand followed by its reverse complement. -/
def dnaDuplex (s : List Base) : List Twist :=
  s.map Base.toTwist ++ (revcomp s).map Base.toTwist

theorem dnaDuplex_eq (s : List Base) :
    dnaDuplex s = s.map Base.toTwist ++ QuantumTurbulence.dagger (s.map Base.toTwist) := by
  rw [dnaDuplex, revcomp_is_dagger]

/-- **Every DNA duplex is a closure** (count-balanced, hence Pauli-closed by
    `count_balanced_pauli_closed`). -/
theorem dna_duplex_closes (s : List Base) : countBalanced (dnaDuplex s) := by
  rw [dnaDuplex_eq]
  exact QuantumTurbulence.dagger_closes _

/-- **Every DNA duplex of length `n` folds to `(−1)^n · I`.** -/
theorem dna_duplex_fold (s : List Base) :
    twistMatrixFold (dnaDuplex s) = ((-1 : ℂ) ^ s.length) • (1 : M) := by
  rw [dnaDuplex_eq, duplex_fold, List.length_map]

theorem map_toTwist_injective {s s' : List Base}
    (h : s.map Base.toTwist = s'.map Base.toTwist) : s = s' := by
  induction s generalizing s' with
  | nil =>
    cases s' with
    | nil => rfl
    | cons _ _ => simp at h
  | cons b s ih =>
    cases s' with
    | nil => simp at h
    | cons b' s' =>
      simp only [List.map_cons, List.cons.injEq] at h
      obtain ⟨hb, hs⟩ := h
      have hbb : b = b' := by
        cases b <;> cases b' <;>
          first | rfl | exact absurd hb (by decide) | simp [Base.toTwist] at hb
      rw [hbb, ih hs]

/-- Distinct sequences give distinct duplexes. -/
theorem dna_duplex_injective {s s' : List Base} (h : dnaDuplex s = dnaDuplex s') : s = s' := by
  rw [dnaDuplex_eq, dnaDuplex_eq] at h
  exact map_toTwist_injective (duplex_injective h)

/-- **Persistence and specification separate (Schrödinger's aperiodic crystal).** On duplexes of
    a fixed length, the closure and its fold are the same for every sequence, while the duplex
    still determines its sequence. So the sequence is carried by the order of the twists and
    by nothing the closure records. -/
theorem dna_duplex_order_not_fold {s s' : List Base} (hlen : s.length = s'.length) :
    countBalanced (dnaDuplex s) ∧ countBalanced (dnaDuplex s') ∧
    twistMatrixFold (dnaDuplex s) = twistMatrixFold (dnaDuplex s') ∧
    (dnaDuplex s = dnaDuplex s' → s = s') :=
  ⟨dna_duplex_closes s, dna_duplex_closes s',
    by rw [dna_duplex_fold, dna_duplex_fold, hlen], dna_duplex_injective⟩

-- ==========================================
-- 3. The memetics link: a duplex passes on no bit of its sequence
-- ==========================================

/-- **The renewal lemma for a duplex** (`closure_renewal`, `Memetics_QLF.md` §2). A closure passes
    at most one sign to its future. For a duplex that sign is `(−1)^n`, fixed by the length, so
    the futures that close and their folds are the same for every sequence. -/
theorem dna_duplex_renewal (s : List Base) (c : List Twist) :
    (countBalanced (dnaDuplex s ++ c) ↔ countBalanced c) ∧
      twistMatrixFold (dnaDuplex s ++ c) = ((-1 : ℂ) ^ s.length) • twistMatrixFold c := by
  refine ⟨ClosureRenewal.countBalanced_append_iff (dna_duplex_closes s) c, ?_⟩
  rw [ClosureRenewal.fold_append, dna_duplex_fold, smul_mul_assoc, one_mul]

/-- **No bit of the sequence reaches the future through the closure.** Two duplexes of equal
    length act identically on every continuation. So a gene's content can persist only as a
    record outside the closed duplex (a copy made by a polymerase), which is the memetics
    result that a closure's record lives in third parties. -/
theorem dna_duplex_future_blind {s s' : List Base} (hlen : s.length = s'.length)
    (c : List Twist) :
    twistMatrixFold (dnaDuplex s ++ c) = twistMatrixFold (dnaDuplex s' ++ c) := by
  rw [(dna_duplex_renewal s c).2, (dna_duplex_renewal s' c).2, hlen]

end QLF.Duplex
