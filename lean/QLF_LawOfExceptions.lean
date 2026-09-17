import QLF_ClosureDepth

set_option linter.unusedVariables false

/-!
# QLF_LawOfExceptions — a system with more states always breaks a finite closure

Write-up: [`Law_Of_Exceptions.md`](../Law_Of_Exceptions.md).

> **Law of Exceptions.** There is an exception to every restrictive law except this law.

The aphorism is old (the base form, *"there is an exception to every rule,"* is recorded in English
from the late 16th century, after the Latin `exceptio probat regulam`); the self-referential twist is
folklore. What is *not* folklore is a proof, and self-reference does not supply one: consistency of
"every law but me has an exception" says nothing about whether any particular law actually has one. The
missing premise has to come from somewhere.

**Jim's formulation supplies it: a system with more states can always break a finite closure.** That is
a theorem about capacity, not about sentences, and on the substrate it is already proven — this module
assembles it from `QLF_ClosureDepth`.

## The proof

Model a restrictive law as what it actually is on the substrate: a **finite closure** — a
finite-capacity horizon `closedAtHorizon R` that admits the histories closing within `R` pruning passes
(`QLF_HorizonClosure`, the observer as a finite-information region, `QLF_Realizability`). Then for
**every** capacity `R`:

* **`exceptionTo_not_closed`** — the history `[+^{R+1} −^{R+1}]` is **not** admitted at capacity `R`.
* **`exceptionTo_is_real`** — yet it closes at `R+1`, so it is a *genuine closure*, not a non-history.
  This is the load-bearing half: the exception is real, merely deeper than the law can see.
* **`law_of_exceptions`** — hence every finite closure has a real exception, and the exception is
  **constructed**, not merely asserted to exist.
* **`closure_hierarchy_strict`** — more capacity admits strictly more (monotone by
  `closedAtHorizon_mono`, strict by the witness), so **no finite closure is final**: the hierarchy of
  capacities never saturates.
* **`no_exception_to_unbounded_closure`** — every exception to a finite law is admitted at some
  capacity. So the exceptions are never exceptions to *ZFA*; they are exceptions to a finite budget.
  ZFA imposes no capacity bound — it is a selection principle, not a restriction — which is exactly why
  it is the one law with no exception. `A_L = H`, in the set formulation.

The kill condition is sharp: exhibit any *other* exceptionless law and the Law of Exceptions is false.

## Why laws nevertheless look exceptionless

Because the exceptions are the **least-multiplicity** histories. `QLF_ClosureDepth` counts the strata:
depth 1 holds `2ⁿ` ways (`onePass_ways_iff`) while the maximal depth holds just the nested singlet and
its mirror. So by the most-ways principle ([`Philosophy.md`](../Philosophy.md) §3a) the shallow
closures happen first and overwhelmingly; the deep exception happens *last* — but it happens. A
capacity-1 law admits a vanishing fraction of the census as histories lengthen (measured
`0.667, 0.400, 0.229, 0.127, 0.069, …, 0.0055` at `n = 10`), so a law can be nearly always right and
still have a real exception at every scale.

## Honest scope

What is proven is the substrate statement: *every finite-capacity closure has a real exception, and the
capacity hierarchy is strictly increasing*. The step from that to "every restrictive law in general" is
the modelling assumption that a restrictive law **is** a finite closure — which is the content of Jim's
formulation, not a further theorem. The set-theoretic version sometimes offered as a proof —
`A_L ⊊ H ⟹ ∃ h ∈ H \ A_L` — is a tautology: true for every possible law and every possible
distribution over histories, so by [`Philosophy.md`](../Philosophy.md) §3a rule 3 it is bookkeeping
rather than evidence. The content here is that the exception is **exhibited with its depth**, and that
the hierarchy provably never closes.
-/

namespace QLF.LawOfExceptions

open QLF.HorizonClosure QLF.ClosureDepth

/-- **The exception to a capacity-`R` law**: the nested fold one shell deeper than the law can prune.
    A system with more states than the closure can absorb — here, one more shell of phase excess. -/
def exceptionTo (R : ℕ) : TopoString := nested (R + 1)

/-- The exception is **not admitted** by the capacity-`R` closure: `R` passes cannot peel `R+1`
    shells. -/
theorem exceptionTo_not_closed (R : ℕ) : ¬ closedAtHorizon R (exceptionTo R) :=
  nested_not_closed_before (R + 1) R (by omega)

/-- **The exception is real** — it closes at capacity `R+1`. This is what makes it an exception rather
    than a non-history: the law is not wrong about what fails to close, it is blind to a closure that
    exceeds its budget. -/
theorem exceptionTo_is_real (R : ℕ) : closedAtHorizon (R + 1) (exceptionTo R) :=
  nested_closed_at_d (R + 1)

/-- **The Law of Exceptions, substrate form.** Every finite closure has a real exception: for every
    capacity `R` there is a history that genuinely closes (at `R+1`) yet is not admitted at `R`. The
    witness is constructed, so this is not an existence claim resting on self-reference. -/
theorem law_of_exceptions (R : ℕ) :
    ∃ s : TopoString, closedAtHorizon (R + 1) s ∧ ¬ closedAtHorizon R s :=
  ⟨exceptionTo R, exceptionTo_is_real R, exceptionTo_not_closed R⟩

/-- **A system with more states can always break a finite closure** (Jim's formulation). More capacity
    admits everything the smaller capacity did (monotone) and strictly more besides — so the capacity
    hierarchy is strictly increasing and **no finite closure is final**. -/
theorem closure_hierarchy_strict (R R' : ℕ) (h : R < R') :
    (∀ s : TopoString, closedAtHorizon R s → closedAtHorizon R' s) ∧
      ∃ s : TopoString, closedAtHorizon R' s ∧ ¬ closedAtHorizon R s := by
  refine ⟨fun s hs => closedAtHorizon_mono hs (le_of_lt h), ?_⟩
  refine ⟨exceptionTo R, ?_, exceptionTo_not_closed R⟩
  exact closedAtHorizon_mono (exceptionTo_is_real R) (by omega)

/-- **No finite closure is the last one.** For every capacity there is a strictly larger one admitting
    more — the corollary that forbids any finite law from being complete. -/
theorem no_final_closure (R : ℕ) :
    ∃ R' : ℕ, R < R' ∧ ∃ s : TopoString, closedAtHorizon R' s ∧ ¬ closedAtHorizon R s :=
  ⟨R + 1, by omega, exceptionTo R, exceptionTo_is_real R, exceptionTo_not_closed R⟩

/-- **The unbounded closure has no exception.** Every exception to a finite law is itself admitted at
    some capacity, so nothing here is an exception to closure *as such* — only to a finite budget. ZFA
    bounds no capacity (it is a selection principle, not a restriction), which is why it is the one law
    the mechanism cannot bite. -/
theorem no_exception_to_unbounded_closure (R : ℕ) :
    ∃ R' : ℕ, closedAtHorizon R' (exceptionTo R) :=
  ⟨R + 1, exceptionTo_is_real R⟩

/-- **Uniqueness, the sharp kill condition.** If a capacity-`K` law has no exception, it is not one of
    the finite closures — contradiction with `law_of_exceptions`. So no finite closure is exceptionless,
    and exhibiting any exceptionless law other than the unbounded one refutes the Law of Exceptions. -/
theorem no_finite_closure_is_exceptionless (K : ℕ)
    (h : ∀ s : TopoString, closedAtHorizon (K + 1) s → closedAtHorizon K s) : False := by
  obtain ⟨s, hreal, hnot⟩ := law_of_exceptions K
  exact hnot (h s hreal)

/-- **Established constructively:** the Law of Exceptions on the substrate, with no axiom. Every
    finite-capacity closure has a **constructed** real exception (`law_of_exceptions`, witness
    `[+^{R+1} −^{R+1}]`, real by `exceptionTo_is_real`), the capacity hierarchy is **strictly**
    increasing (`closure_hierarchy_strict`) so no finite closure is final (`no_final_closure`), no
    finite closure is exceptionless (`no_finite_closure_is_exceptionless`), and every such exception is
    admitted at some capacity (`no_exception_to_unbounded_closure`) — so the unbounded ZFA closure,
    which restricts nothing, is the one law with no exception. **Modelling assumption (not a theorem):**
    that a restrictive law *is* a finite closure. **Method note:** the exceptions are the
    least-multiplicity histories (two ways at maximal depth against `2ⁿ` at depth 1), which is why laws
    look exceptionless — the most ways happen first, so the exception happens last. -/
theorem law_of_exceptions_summary : True := trivial

end QLF.LawOfExceptions
