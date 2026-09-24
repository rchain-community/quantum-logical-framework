/-
  QLF_AxiomAudit.lean — the dependency footprint of QLF's anchor theorems.

  Zero `sorry` is a weak contract. It says every goal was closed; it says nothing about
  *what closed it*. A theorem proved from definitions and a theorem proved from an opaque
  bridge assumption are epistemically different results, and nothing in the source
  distinguishes them — the bridge can sit twenty imports upstream.

  `#print axioms` answers the question the source cannot: for a given constant, exactly
  which axioms the kernel actually used. This module runs it over the anchors a session
  reasons about most, so the build log carries the answer on every push.

  Reading the output. Three names are Lean's own and appear almost everywhere, because
  Mathlib is classical throughout:

      propext          — propositional extensionality
      Classical.choice — global choice
      Quot.sound       — quotient soundness

  These are *not* a QLF assumption and their presence is not a defect. In particular they
  do not contradict the RCA₀ framing: the reverse-mathematical strength of a *statement*
  is a claim about which subsystem of second-order arithmetic proves it, not about which
  axioms a particular Lean formalisation happened to route through. Mathlib's `Finset`,
  `List` and `ℝ` machinery is classical, so a finitary combinatorial theorem picks up
  `Classical.choice` from its libraries while remaining finitary.

  What matters is the fourth kind of name: anything in the `QLF` namespace. That is a
  project bridge assumption, and it should appear only where the inventory says it does.
  The intended split:

      combinatorial core     — no QLF axiom
      derived physics        — no QLF axiom
      Millennium boundaries  — exactly one named bridge (or the named pair), and no more
      cited external results — the classical theorem QLF declines to reformalise

  The complementary audit is `scripts/axiom_audit.sh`, which pins the *declared* axioms
  (lean/axioms.expected) so no assumption can arrive unnoticed. This file reports what the
  proofs actually consume; that one reports what exists to be consumed.
-/

import QLF_Axioms
import QLF_Universality
import QLF_TwistAlphabet
import QLF_PhaseRule
import QLF_KraftMeasure
import QLF_LatticeCalculus
import QLF_Realizability
import QLF_LawOfExceptions
import QLF_AlphaBound
import QLF_Hodge
import QLF_BSD
import QLF_PvsNP
import QLF_Fredkin
import QLF_HorizonBasis
import QLF_MassGap
import QLF_NavierStokes
import QLF_ChargeBalance
import QLF_CensusCurvature
import QLF_LorentzCover
import QLF_RiemannMRE
import QLF_StationaryAction
import QLF_StationaryPhase

/-! ## The combinatorial core — expected: no QLF axiom -/

#print axioms double_fold_identity
#print axioms QLF.qlf_universality
#print axioms QLF.count_balanced_pauli_closed
#print axioms QLF.PhaseRule.phase_rule
#print axioms QLF.twist_kraft
#print axioms QLF.Realizability.no_continuum_in_finite_region
#print axioms QLF.LawOfExceptions.law_of_exceptions
#print axioms QLF.StationaryAction.balance_is_stationary_mode
#print axioms QLF.StationaryPhase.signed_stationary_phase

/-! Fredkin's conservative logic identified with ZFA (Fredkin_QLF.md). `fredkin_preserves_zfa`
    runs through the `count_balanced_pauli_closed` keystone, so it must show the Lean three
    and no QLF axiom — the identification is a theorem, not a bridge. -/

#print axioms QLF.Fredkin.fredkin_preserves_zfa
#print axioms QLF.Fredkin.fredkin_bijective

/-! The horizon rebasing. `horizon_rebasis_is_closure_order_iso` must show no QLF axiom — the whole
    point of the module is that the basis algebra is mathematics and the black-hole step is not in
    it. A QLF name here would mean the open bridge had been quietly assumed. -/

#print axioms QLF.HorizonBasis.horizon_rebasis_is_closure_order_iso
#print axioms QLF.HorizonBasis.reachable_rebased_iff

/-! The Yang-Mills measurement. `continuumGap_nonempty` builds a realization by `rfl` and
    `continuumGap_gap_unique` shows the interface pins its own value, so both must show no
    QLF axiom — which is exactly what makes that boundary definitional in Lean. -/

#print axioms QLF.continuumGap_nonempty
#print axioms QLF.continuumGap_gap_unique
#print axioms QLF.mass_gap_quantum_pos

/-! Navier-Stokes: the boundary here was *removed* rather than merged, because
    `continuumClaim_nonempty` shows it assumed nothing — an uninterpreted `Prop` plus its
    truth is satisfied by `True` and `trivial`. What the module still proves stands on its
    own, and must show no QLF axiom. -/

#print axioms QLF.continuumClaim_nonempty
#print axioms QLF.realized_flow_achieves_zfa

/-! Hodge. The two lines belong together: `hodge_realized_on_substrate` (above) is the
    reformulation theorem and carries no QLF axiom, while `algebraicityBridge_nonempty`
    shows the faithfulness bridge is satisfied by reading every class as algebraic. The
    theorem is real and the bridge, in Lean, excludes nothing — that is the whole distinction
    the module's framing turns on. -/

#print axioms QLF.algebraicityBridge_nonempty

/-! The last two, and the contrast between them is the pass's most useful outcome.

    `transportCurvature_nonempty` is trivially satisfiable like the rest — but that reflects
    Mathlib's missing discrete optimal transport, not an empty claim: Jost & Liu (2014) is a
    real theorem, *cited* rather than posited, and discharging it is labour with a known
    answer.

    `properOrthochronous_id` marks the healthy case. `lorentz_generated_by_boosts_rotations`
    quantifies over a fully concrete class with nothing uninterpreted in it, so there is no
    trivial model to exhibit — there is nothing left to choose. That is the standard the
    other boundaries fall short of. -/

/-! Electron capture: the invariants are proved, the rate is not claimed. These must show no QLF
    axiom — the point of proving only the invariants is to keep "allowed" apart from "derived". -/

#print axioms QLF.electron_capture_charge_balanced
#print axioms QLF.capture_changes_exactly_one_slot
#print axioms QLF.local_capture_charge_conserved
#print axioms QLF.electron_capture_factors_through_wminus

#print axioms QLF.transportCurvature_nonempty
#print axioms QLF.LorentzCover.properOrthochronous_id
#print axioms QLF.census_no_triangles

/-! ## Derived results — expected: no QLF axiom.

    `censusTail_eq` is the discharged one: it was a bridge axiom and is now derived from
    Mathlib's generalized binomial theorem, so `QLF_AlphaBound` carries none. If a QLF
    name reappears here, the discharge regressed. -/

#print axioms QLF.AlphaBound.censusTail_eq
#print axioms QLF.LatticeCalculus.field_equations_hold_on_the_lattice

/-! ## Reformulation theorems — expected: no QLF axiom.

    These are the proven halves of the Millennium reformulations. `hodge_realized_on_substrate`
    is the load-bearing case: Hodge classes are exactly the substrate-realized closures, and
    that is proved outright. It must show no QLF axiom — `substrate_realization_is_algebraic`
    is the *next* step, not this one. -/

#print axioms QLF.hodge_realized_on_substrate

/-! `trivial_zero_not_nonTrivial` is the check that the RH boundary now speaks about ζ:
    an ordinary theorem, about Mathlib's `riemannZeta`, carrying no QLF axiom. It could not
    be stated at all while `NonTrivialZero` was an uninterpreted predicate. -/

#print axioms QLF.trivial_zero_not_nonTrivial

/-! `mellinFactorization_iff_rh` measures the Riemann boundary rather than describing it:
    the two-leg Mellin factorization is equivalent to RH, so the middle predicate buys no
    weakening. A theorem about how much an axiom assumes should itself assume nothing, so
    this line must show no QLF axiom. -/

#print axioms QLF.mellinFactorization_iff_rh
#print axioms QLF.mellinFactorization_independent_of_generator

/-! The BSD counterparts. `mirrorInvariant_iff_perspectives_agree` shows the modularity
    mirror carries no strength beyond the agreement it concludes, and
    `mirrorMultiplicity_nonempty` shows the interface is inhabited by constant zero — so a
    construction cannot discharge that boundary the way `QLF_LatticeCalculus` discharged
    its own. Both must show no QLF axiom. -/

#print axioms QLF.mirrorInvariant_iff_perspectives_agree
#print axioms QLF.mirrorMultiplicity_nonempty

/-! The P-vs-NP counterparts. `realized_count_eq_central_binomial` is the module's real
    content — the `C(2n,n)` count of the verify-filtered set — and must carry no QLF axiom.
    `costModel_nonempty` is the measurement: it builds a cost model out of `verify` and
    boolean negation, so it too must carry none, which is precisely what makes it bad news
    for the boundary rather than good. -/

#print axioms QLF.realized_count_eq_central_binomial
#print axioms QLF.costModel_nonempty

/-! ## Boundaries — expected: exactly the named bridge, and nothing further.

    `bsd_rank_equals_order` should consume `bsd_multiplicity` and no other QLF axiom. Note
    what its footprint lacks: `propext`, `Classical.choice` and `Quot.sound` are all absent,
    which is the signature of a pure application — the machine's own way of saying the
    theorem restates its boundary rather than deriving from it. Compare
    `hodge_realized_on_substrate` above, which carries the Lean three and no QLF name: that
    is what a proof looks like.

    `riemann_hypothesis_in_qlf_via_MRE` should consume `mre_factorization` and *not*
    `spectral_hilbert_polya`. The two routes are independent in *dependency* — neither
    proof reaches through the other's axiom, and the first green audit confirmed it — while
    being equivalent in *strength*, since each is equivalent to RH. Both facts are worth
    having and they are different facts; the audit reports the first one. -/

#print axioms QLF.bsd_rank_equals_order
#print axioms QLF.p_vs_np_in_qlf
#print axioms QLF.riemann_hypothesis_in_qlf
#print axioms QLF.riemann_hypothesis_in_qlf_via_MRE
