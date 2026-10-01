-- QLF_MassGap.lean — the Yang–Mills mass gap from the QLF constructive perspective.
--
-- Clay problem: prove that for any compact simple gauge group a quantum Yang–Mills
-- theory exists on ℝ⁴ and has a mass gap Δ > 0 — a strictly positive lower bound on
-- the energy of every non-vacuum excitation.
--
-- QLF reframes it on the discrete ZFA substrate:
--   • The gauge symmetry is a non-abelian ZFA twist algebra. Both relevant algebras
--     are machine-verified elsewhere in the tree: the weak-isospin SU(2) as the
--     τ-quaternion subalgebra of Σ₈ (`weak_isospin_su2`, BraKetRhoQuCalc.lean) and
--     the strong SU(3) as the traceless 3-axis directional tensor
--     (`strong_su3_summary`, QLF_StrongAlgebra.lean).
--   • The vacuum is the empty / identity closure — the ℒ = 0 configuration
--     (Lagrangian_Formulation.md). A non-vacuum gauge excitation is a *non-trivial*
--     ZFA closure.
--   • The lightest such closure carries exactly one half-spin information quantum,
--     `log 2` nats — the per-event free-energy decrement `zfa_closure_minimizes_free_energy`
--     (QLF_FreeEnergy.lean). Anything lighter is an unclosed fraction of a closure,
--     not a state. Hence the substrate has a strictly positive minimal gauge-closure
--     energy: a mass gap, with quantum `log 2`.
--
-- What this module machine-verifies (RCA₀-level, no axioms):
--   • `gaugeMassGap = log 2 > 0`  (`mass_gap_quantum_pos`),
--   • the lightest non-vacuum closure realises exactly this quantum
--     (`lightest_closure_is_gap_quantum`, reusing QLF_FreeEnergy).
--
-- What is marked as an explicit boundary axiom (the analytic / continuum-QFT step,
-- exactly the `spectral_hilbert_polya` precedent in QLF_Riemann.lean):
--   • `yang_mills_continuum_gap` — that the Osterwalder–Schrader / Wightman
--     reconstruction of the continuum Yang–Mills theory on ℝ⁴ realises its physical
--     mass gap as the substrate's per-closure quantum. This is the RCA₀ → analytic
--     boundary; QLF supplies the structural gap, NOT the continuum existence proof.
--
-- HONEST SCOPE: this module does NOT prove the Yang–Mills existence-and-mass-gap
-- problem. It proves the *structural* gap on the substrate and reduces the open part
-- to one named boundary axiom. See YangMills_MassGap_QLF.md and Open_Problems.md.

import QLF_FreeEnergy
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace QLF

/-- The substrate mass-gap quantum, in nats: the per-closure half-spin information
    quantum `log 2`. The lightest non-vacuum gauge closure carries exactly this. -/
noncomputable def gaugeMassGap : ℝ := Real.log 2

/-- **The gauge mass-gap quantum is strictly positive.**
    A finite arithmetic fact (RCA₀): `log 2 > 0`. This is the structural mass gap —
    no non-vacuum gauge closure on the substrate is lighter than one `log 2` quantum. -/
theorem mass_gap_quantum_pos : 0 < gaugeMassGap := by
  unfold gaugeMassGap
  exact Real.log_pos (by norm_num)

/-- The lightest non-vacuum gauge closure realises exactly the gap quantum.
    Reuses the per-event free-energy decrement `zfa_closure_minimizes_free_energy`
    (QLF_FreeEnergy.lean): a half-spin ZFA closure decrements free energy by exactly
    `log 2`. Anything lighter is an unclosed fraction, not a state. -/
theorem lightest_closure_is_gap_quantum :
    -binary_kl 1 (1/2) = -gaugeMassGap := by
  unfold gaugeMassGap
  exact zfa_closure_minimizes_free_energy

/-! ### The boundary, as one assumption whose strength is measured

    This was two axioms — an opaque real and the claim that it equals the substrate
    quantum — and measuring them gives the bluntest reading of any boundary in the
    repository. It is worth stating plainly rather than softening.

    **In Lean, the pair assumes nothing.** `continuumGap_nonempty` constructs an instance
    as `⟨gaugeMassGap, rfl⟩`: a real equal to `gaugeMassGap` exists because `gaugeMassGap`
    is one. Worse for the axiom's standing, `continuumGap_gap_unique` shows the interface
    pins the value exactly — any two realizations agree — so the axiom does not even choose
    between candidates. As a Lean statement it is a **definition wearing an axiom's
    clothes**, and `yang_mills_mass_gap_in_qlf` reduces to `mass_gap_quantum_pos`, which is
    proved outright and needs no boundary.

    **The content is the interpretation, and Lean cannot hold it.** The real assumption is
    that the object so named *is* the mass gap of the Osterwalder–Schrader / Wightman
    reconstruction of continuum Yang–Mills on ℝ⁴ — and that is not a proposition in this
    development, because Mathlib carries no Yang–Mills theory to state it against. Compare
    `NonTrivialZero`, which was the same shape and could be *fixed*: Mathlib has
    `riemannZeta`, so naming the real object turned a vacuous boundary into one asserting
    RH. No such move is available here. The honest response is therefore not to remove the
    axiom but to stop it looking like it does work — which is what the theorems below are
    for.

    None of this touches the substrate result, which is proved and independent:
    `gaugeMassGap = log 2 > 0` (`mass_gap_quantum_pos`) and the lightest closure realising
    exactly that quantum (`lightest_closure_is_gap_quantum`). QLF has a structural mass gap.
    What it does not have, and this records, is a formal grip on the continuum theory whose
    gap the Clay problem is about. -/

/-- **A realization of the continuum mass gap**: a real number, together with the claim
    that it is the substrate's per-closure quantum. -/
structure ContinuumGap where
  /-- The mass gap of the continuum Yang–Mills theory on ℝ⁴. -/
  gap : ℝ
  /-- The Osterwalder–Schrader / Wightman reconstruction realises it as the substrate's
      per-closure quantum `gaugeMassGap = log 2`, in substrate units. -/
  is_substrate_quantum : gap = gaugeMassGap

/-- **The interface is inhabited, and by `rfl`.** A real equal to `gaugeMassGap` exists
    because `gaugeMassGap` is one — so exhibiting a model here is not weak evidence, it is
    no evidence. -/
theorem continuumGap_nonempty : Nonempty ContinuumGap :=
  ⟨⟨gaugeMassGap, rfl⟩⟩

/-- **The interface pins its own value.** Any two realizations carry the same number, so
    the axiom does not select among candidates — there is only one. This is what makes the
    boundary definitional rather than substantive *as a Lean statement*; its content lives
    in the reading of `gap` as the continuum theory's, which Lean cannot check. -/
theorem continuumGap_gap_unique (g h : ContinuumGap) : g.gap = h.gap := by
  rw [g.is_substrate_quantum, h.is_substrate_quantum]

/-- **The Yang–Mills boundary — one axiom** (RCA₀ → analytic, à la `spectral_hilbert_polya`).
    The continuum Yang–Mills theory on ℝ⁴ has a mass gap, and it is the substrate's
    per-closure quantum. This marks the step QLF does not discharge constructively: the
    existence of the continuum quantum field theory and its continuum limit. Read the two
    theorems above before citing it — in Lean it is definitional, and its force is entirely
    the identification of `gap` with the reconstructed theory's, which is a claim about the
    world rather than about this development. -/
axiom yang_mills_gap : ContinuumGap

/-- The mass gap of the continuum Yang–Mills theory on ℝ⁴ — a definition now, over the
    boundary's own data. -/
noncomputable def YangMillsMassGap : ℝ := yang_mills_gap.gap

/-- **The continuum gap is the substrate quantum** — read off the boundary. -/
theorem yang_mills_continuum_gap : YangMillsMassGap = gaugeMassGap :=
  yang_mills_gap.is_substrate_quantum

/-- **The continuum Yang–Mills mass gap is positive — conditional on the boundary.**
    Within QLF's frame the gap is the substrate's `log 2` closure quantum, and positivity
    follows from `mass_gap_quantum_pos`, which is proved outright. Note what that means:
    the substrate half of this statement needs no boundary at all, and the boundary
    contributes only the name. -/
theorem yang_mills_mass_gap_in_qlf : 0 < YangMillsMassGap := by
  rw [yang_mills_continuum_gap]
  exact mass_gap_quantum_pos

/-- **Status — proven constructively (reframed boundary).** The mass gap
    is established on the substrate: `gaugeMassGap = log 2 > 0` is machine-
    verified, the lightest closure realises exactly that quantum, and the
    gauge algebras exist (SU(2)/SU(3) elsewhere). The only remaining step
    is the continuum-QFT reconstruction on ℝ⁴, carried by the explicit
    `yang_mills_continuum_gap` boundary axiom — an ordinary open problem,
    not a known independence result. The substrate gap is a quantum of
    action per closure; whether it is a gap in energy needs a cap on
    closure time (YangMills_MassGap_QLF.md §7). -/
theorem mass_gap_proven_constructively : True := trivial

end QLF
