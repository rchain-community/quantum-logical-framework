import QLF_PhaseInformation
import QLF_BasisIndependence
import QLF_BaryonWinding

/-!
# QLF_ClosureEquivalence — which different histories count as the same closed state

Issue #148 asked, in plain language: *when the machine says "done", which different stories are
allowed to count as the same result — and which differences still matter?* Issue #152 asked for
the answer as a module. This is it: the **closure token** of a history, the equivalence relation
it induces, and exactly where that relation sits between literal identity and count-equivalence.

## The token

A history is `List Twist` (the 8-twist alphabet of [`QLF_TwistAlphabet`](QLF_TwistAlphabet.lean)),
and it is closed when it is count-balanced — `countBalanced`, which by
`count_balanced_pauli_closed` carries Pauli closure with it. The token keeps two things:

* **the ledger** — the net count of every generator, `ℤ⁸` indexed by the eight twists
  (the abelian / multiset / Shannon face of the history);
* **the fold** — the ordered Pauli product `twistMatrixFold` (the non-abelian / phase face,
  which on a balanced history is a scalar in `μ₄ = {±I, ±iI}`).

`closureToken h := (ledger h, twistMatrixFold h)`, and `ClosureEquiv h₁ h₂` (written `h₁ ∼ h₂`
in prose) `⟺ closureToken h₁ = closureToken h₂`.

[`Closure_Token_Basis.md`](../Closure_Token_Basis.md) §1 lists a third datum, the closure
witness itself; here that witness is `countBalanced h`, carried as a *hypothesis* where a
theorem needs it rather than as a component of the token, so `∼` is a total equivalence on all
histories and the physical reading is its restriction to the balanced ones. The fold is kept as
the matrix rather than as a chosen `PauliScalar`: on balanced histories the two agree
(`count_balanced_pauli_closed`), and the matrix needs no choice function.

## Where the relation sits — the five results

1. **`closureEquiv_is_equivalence`** — `∼` is an equivalence (it is `Eq` on the token), packaged
   as the setoid `closureSetoid`; `ClosureClass` is the quotient.
2. **`closureEquiv_coarser_than_eq`** — `∼` identifies genuinely different histories:
   `^v><` and `><^v` are one twist multiset in two orders with the same fold (the second is the
   `X↔Y` relabeling of the first, and `fold_invariant_swapXY` says relabeling a balanced history
   leaves its fold alone). Closure forgets *this* ordering.
3. **`closureEquiv_finer_than_count`** — but not every ordering: `^v<>` and `^<v>` have the
   same ledger and fold to `+I` and `−I`. This is `count_does_not_determine_phase`
   ([`QLF_PhaseInformation`](QLF_PhaseInformation.lean)) restated on the quotient — the phase
   survives closure as an invariant, and it is the boson/fermion distinction.
4. **`closureEquiv_map_swapXY` / `_swapYZ` / `_flipX` / `_swapGauge`** — every relabeling of
   [`QLF_BasisIndependence`](QLF_BasisIndependence.lean) descends to the quotient: on balanced
   histories, `h₁ ∼ h₂ → h₁.map r ∼ h₂.map r`. The ledger transports by the induced
   permutation of the generators (`count_map_*`) and the fold is invariant (`fold_invariant_*`).
   The basis belongs to the question; the classes do not.
5. **`invariant_iff_class_function`** — a quantity `f` descends to the quotient exactly when
   it respects `∼`. Then the concrete verdicts:
   * `axisWindingVector` (the `ℤ³` net spatial displacement that
     [`Pointer_Swap_Fuzz.md`](../Pointer_Swap_Fuzz.md) specified in prose — its first Lean
     definition), `gaugeCharge` (the gauge component of the ledger, charge per
     [`QLF_Handedness`](QLF_Handedness.lean)), and the fold scalar **are** class functions;
   * **`baryonNumber` is not** (`baryonNumber_not_class_function`): `>^/<v\` and its `X↔Y`
     relabeling `^>/v<\` are one class — same ledger, same fold — with baryon numbers `4` and
     `−4`. `baryonNumber` is a sliding-window *linking* sum
     ([`QLF_BaryonWinding`](QLF_BaryonWinding.lean)), sequence-dependent by construction, so it
     belongs to the pre-closure process, exactly as `Pointer_Swap_Fuzz.md` §"The
     receipt-quotient model" says.

So closure forgets the right things: it discards the order *within* a class (the relabeling
orbit) while keeping the phase, the displacement, and the charge. What it does not keep is the
linking — which is therefore a fact about how a state was generated, not about the state.

## Honest scope

Assembly of existing results; no new axioms. Not attempted: the continuum / order→metric step
([`QLF_OrderMetric`](QLF_OrderMetric.lean) keeps it), and the α-residual that
`Closure_Token_Basis.md` inherits from `Alpha.md`.
-/

namespace QLF.ClosureEquivalence

open QLF QLF.PhaseInformation QLF.BasisIndependence QLF.BaryonWinding

-- ==========================================
-- The ledger and the token
-- ==========================================

/-- **The ledger**: the count of every generator, as `ℤ⁸` indexed by the eight twists. -/
def ledger (h : List Twist) (t : Twist) : ℤ := (h.count t : ℤ)

/-- Two histories have the same ledger exactly when every generator count agrees. -/
theorem ledger_eq_iff {h₁ h₂ : List Twist} :
    ledger h₁ = ledger h₂ ↔ ∀ t : Twist, h₁.count t = h₂.count t := by
  constructor
  · intro e t
    have ht := congrFun e t
    unfold ledger at ht
    exact_mod_cast ht
  · intro hc
    funext t
    unfold ledger
    rw [hc t]

/-- **The closure token**: the ledger together with the ordered Pauli fold. -/
noncomputable def closureToken (h : List Twist) : (Twist → ℤ) × M :=
  (ledger h, twistMatrixFold h)

/-- **Closure equivalence**: two histories close to the same state when their tokens agree. -/
def ClosureEquiv (h₁ h₂ : List Twist) : Prop := closureToken h₁ = closureToken h₂

theorem closureEquiv_iff {h₁ h₂ : List Twist} :
    ClosureEquiv h₁ h₂ ↔ ledger h₁ = ledger h₂ ∧ twistMatrixFold h₁ = twistMatrixFold h₂ := by
  constructor
  · intro e
    unfold ClosureEquiv closureToken at e
    exact Prod.mk.inj e
  · rintro ⟨hl, hf⟩
    unfold ClosureEquiv closureToken
    rw [hl, hf]

-- ==========================================
-- 1. It is an equivalence
-- ==========================================

/-- **`∼` is an equivalence relation** — reflexive, symmetric, transitive. -/
theorem closureEquiv_is_equivalence : Equivalence ClosureEquiv := by
  unfold ClosureEquiv
  exact ⟨fun _ => rfl, fun e => Eq.symm e, fun e₁ e₂ => Eq.trans e₁ e₂⟩

/-- The setoid of histories under closure equivalence. Kept as a `def`, not an instance, so it
    never competes with Mathlib's permutation setoid on lists. -/
def closureSetoid : Setoid (List Twist) := ⟨ClosureEquiv, closureEquiv_is_equivalence⟩

/-- **The closure classes** — the reportable states. -/
abbrev ClosureClass : Type := Quotient closureSetoid

-- ==========================================
-- 2. Coarser than equality: closure forgets an ordering
-- ==========================================

/-- `^v><` is count-balanced. -/
theorem balanced_udrl :
    countBalanced [Twist.up, Twist.down, Twist.right, Twist.left] := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> rfl

/-- **`∼` is strictly coarser than `=`.** `^v><` and `><^v` are different histories with one
    token: same ledger (one of each of `^ v > <`), and the same fold — the second is the `X↔Y`
    relabeling of the first, which leaves a balanced fold unchanged (`fold_invariant_swapXY`). -/
theorem closureEquiv_coarser_than_eq :
    ∃ h₁ h₂ : List Twist, h₁ ≠ h₂ ∧ ClosureEquiv h₁ h₂ := by
  refine ⟨[Twist.up, Twist.down, Twist.right, Twist.left],
          [Twist.right, Twist.left, Twist.up, Twist.down], ?_, ?_⟩
  · decide
  · rw [closureEquiv_iff]
    refine ⟨ledger_eq_iff.mpr (fun t => by cases t <;> rfl), ?_⟩
    have hmap : [Twist.up, Twist.down, Twist.right, Twist.left].map swapXY
        = [Twist.right, Twist.left, Twist.up, Twist.down] := rfl
    rw [← hmap]
    exact (fold_invariant_swapXY balanced_udrl).symm

-- ==========================================
-- 3. Finer than count: closure keeps the phase
-- ==========================================

/-- **`∼` is strictly finer than count-equivalence.** Two histories with one ledger that are
    *not* closure-equivalent: `^v<>` and `^<v>` fold to `+I` and `−I`
    (`count_does_not_determine_phase`). The phase survives closure. -/
theorem closureEquiv_finer_than_count :
    ∃ h₁ h₂ : List Twist, ledger h₁ = ledger h₂ ∧ ¬ ClosureEquiv h₁ h₂ := by
  obtain ⟨ts₁, ts₂, hc, _, _, hf⟩ := count_does_not_determine_phase
  exact ⟨ts₁, ts₂, ledger_eq_iff.mpr hc, fun e => hf (closureEquiv_iff.mp e).2⟩

-- ==========================================
-- 4. Relabelings descend to the quotient
-- ==========================================

/-- Any relabeling that permutes the generator counts and preserves balanced folds descends
    to closure classes. -/
theorem closureEquiv_map_of {r : Twist → Twist}
    (hcount : ∀ (t : Twist) (ts : List Twist), (ts.map r).count t = ts.count (r t))
    (hfold : ∀ ts : List Twist, countBalanced ts →
      twistMatrixFold (ts.map r) = twistMatrixFold ts)
    {h₁ h₂ : List Twist} (b₁ : countBalanced h₁) (b₂ : countBalanced h₂)
    (e : ClosureEquiv h₁ h₂) : ClosureEquiv (h₁.map r) (h₂.map r) := by
  rw [closureEquiv_iff] at e ⊢
  obtain ⟨el, ef⟩ := e
  refine ⟨?_, ?_⟩
  · rw [ledger_eq_iff] at el ⊢
    intro t
    rw [hcount t h₁, hcount t h₂]
    exact el _
  · rw [hfold _ b₁, hfold _ b₂, ef]

/-- **The `X↔Y` relabeling respects closure equivalence** on balanced histories. -/
theorem closureEquiv_map_swapXY {h₁ h₂ : List Twist}
    (b₁ : countBalanced h₁) (b₂ : countBalanced h₂) (e : ClosureEquiv h₁ h₂) :
    ClosureEquiv (h₁.map swapXY) (h₂.map swapXY) :=
  closureEquiv_map_of count_map_swapXY (fun _ h => fold_invariant_swapXY h) b₁ b₂ e

/-- **The `Y↔Z` relabeling respects closure equivalence** on balanced histories. -/
theorem closureEquiv_map_swapYZ {h₁ h₂ : List Twist}
    (b₁ : countBalanced h₁) (b₂ : countBalanced h₂) (e : ClosureEquiv h₁ h₂) :
    ClosureEquiv (h₁.map swapYZ) (h₂.map swapYZ) :=
  closureEquiv_map_of count_map_swapYZ (fun _ h => fold_invariant_swapYZ h) b₁ b₂ e

/-- **The `X` reversal respects closure equivalence** on balanced histories. -/
theorem closureEquiv_map_flipX {h₁ h₂ : List Twist}
    (b₁ : countBalanced h₁) (b₂ : countBalanced h₂) (e : ClosureEquiv h₁ h₂) :
    ClosureEquiv (h₁.map flipX) (h₂.map flipX) :=
  closureEquiv_map_of count_map_flipX (fun _ h => fold_invariant_flipX h) b₁ b₂ e

/-- **The gauge swap respects closure equivalence** on balanced histories. -/
theorem closureEquiv_map_swapGauge {h₁ h₂ : List Twist}
    (b₁ : countBalanced h₁) (b₂ : countBalanced h₂) (e : ClosureEquiv h₁ h₂) :
    ClosureEquiv (h₁.map swapGauge) (h₂.map swapGauge) :=
  closureEquiv_map_of count_map_swapGauge (fun _ h => fold_invariant_swapGauge h) b₁ b₂ e

-- ==========================================
-- 5. Invariants are exactly the class functions
-- ==========================================

/-- **A quantity descends to the closure classes iff it respects `∼`.** The forward direction
    reads it off the quotient; the backward direction is `Quotient.lift`. -/
theorem invariant_iff_class_function {α : Type*} (f : List Twist → α) :
    (∃ g : ClosureClass → α, ∀ h, f h = g (Quotient.mk closureSetoid h)) ↔
      ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → f h₁ = f h₂ := by
  constructor
  · rintro ⟨g, hg⟩ h₁ h₂ e
    rw [hg, hg, @Quotient.sound _ closureSetoid _ _ e]
  · intro hf
    exact ⟨Quotient.lift f hf, fun _ => rfl⟩

/-- **The axis winding vector** — net signed displacement along each spatial axis, `ℤ³`:
    `(#> − #<, #^ − #v, #/ − #\)`. The geometry quotient of `Pointer_Swap_Fuzz.md`, now in Lean. -/
def axisWindingVector (h : List Twist) : ℤ × ℤ × ℤ :=
  (ledger h Twist.right - ledger h Twist.left,
   ledger h Twist.up - ledger h Twist.down,
   ledger h Twist.slash - ledger h Twist.backslash)

/-- **The gauge charge** — the gauge component of the ledger, `#+ − #−`. -/
def gaugeCharge (h : List Twist) : ℤ := ledger h Twist.plus - ledger h Twist.minus

/-- The ledger is a class function (it is a component of the token). -/
theorem ledger_class_function :
    ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → ledger h₁ = ledger h₂ :=
  fun _ _ e => (closureEquiv_iff.mp e).1

/-- **The axis winding vector is a closure invariant.** -/
theorem axisWindingVector_class_function :
    ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → axisWindingVector h₁ = axisWindingVector h₂ := by
  intro h₁ h₂ e
  unfold axisWindingVector
  rw [ledger_class_function h₁ h₂ e]

/-- **The gauge charge is a closure invariant.** -/
theorem gaugeCharge_class_function :
    ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → gaugeCharge h₁ = gaugeCharge h₂ := by
  intro h₁ h₂ e
  unfold gaugeCharge
  rw [ledger_class_function h₁ h₂ e]

/-- **The fold scalar is a closure invariant** — the phase survives closure. -/
theorem fold_class_function :
    ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → twistMatrixFold h₁ = twistMatrixFold h₂ :=
  fun _ _ e => (closureEquiv_iff.mp e).2

/-- `>^/<v\` is count-balanced. -/
theorem balanced_rusldb :
    countBalanced [Twist.right, Twist.up, Twist.slash, Twist.left, Twist.down, Twist.backslash] := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> rfl

/-- `>^/<v\` and its `X↔Y` relabeling `^>/v<\` are closure-equivalent. -/
theorem rusldb_equiv_ursdlb :
    ClosureEquiv
      [Twist.right, Twist.up, Twist.slash, Twist.left, Twist.down, Twist.backslash]
      [Twist.up, Twist.right, Twist.slash, Twist.down, Twist.left, Twist.backslash] := by
  rw [closureEquiv_iff]
  refine ⟨ledger_eq_iff.mpr (fun t => by cases t <;> rfl), ?_⟩
  have hmap : [Twist.right, Twist.up, Twist.slash, Twist.left, Twist.down, Twist.backslash].map
      swapXY = [Twist.up, Twist.right, Twist.slash, Twist.down, Twist.left, Twist.backslash] := rfl
  rw [← hmap]
  exact (fold_invariant_swapXY balanced_rusldb).symm

/-- **Baryon number is not a closure invariant.** One class, two values: `>^/<v\` links
    `+4` (four cyclic `x,y,z` windows) and its relabeling `^>/v<\` links `−4`. The linking is a
    fact about the generating sequence, not about the closed state. -/
theorem baryonNumber_not_class_function :
    ¬ ∀ h₁ h₂ : List Twist, ClosureEquiv h₁ h₂ → baryonNumber h₁ = baryonNumber h₂ := by
  intro H
  have h := H _ _ rusldb_equiv_ursdlb
  exact absurd h (by decide)

/-- Hence `baryonNumber` does not descend to the closure classes. -/
theorem baryonNumber_no_descent :
    ¬ ∃ g : ClosureClass → Int, ∀ h, baryonNumber h = g (Quotient.mk closureSetoid h) :=
  fun hex => baryonNumber_not_class_function ((invariant_iff_class_function _).mp hex)

/-- **Status.** The closure token and its quotient are machine-checked: `∼` is an equivalence,
    strictly between `=` and count-equivalence (it forgets the relabeling orbit, keeps the phase),
    every relabeling descends to it, and the invariants are exactly the class functions — the
    displacement, the charge and the phase are; the linking number is not. -/
theorem closure_equivalence_summary : True := trivial

end QLF.ClosureEquivalence
