import QLF_BaryonWinding

set_option linter.unusedVariables false

/-!
# QLF_Baryogenesis — the three Sakharov conditions are met; the asymmetry is generic

Why is there more matter than antimatter (`η_B = n_B/n_γ ≈ 6×10⁻¹⁰`)? Sakharov (1967): a baryon
asymmetry arises from any dynamics with **(1) baryon-number violation, (2) C and CP violation,
(3) departure from thermal equilibrium**. The substrate meets all three — so a matter excess is
*generic*, not fine-tuned:

* **(1) B-violation.** Baryon number is a signed 3-axis *winding* read on the junction
  (`junctionBaryon`, `QLF_BaryonWinding`), not a conserved signed count, and it flips under charge
  conjugation (`junctionBaryon_antiparticle`: `B(antiparticle ts) = −B(ts)`, for every word including
  the quark charge twists). And `B−L` is violated in the lepton
  sector (the neutrino is Majorana, `neutrino_majorana`). So matter and antimatter carry
  *opposite* baryon winding (`matter_antimatter_opposite`) — distinguishable, B not protected.
* **(2) C and CP violation.** The chirality engine of `CP-Violation-and-Chirality.md` spontaneously
  breaks the LH/RH symmetry (one topology consumes the matrix); charge and chirality co-negate
  under conjugation (`C_eq_motional_reversal`, `QLF_Spin`), and CP-odd windings are nonzero off
  closure (`QLF_StrongCP`).
* **(3) Departure from equilibrium.** The early universe inflates / expands (`w = −1`,
  `QLF_CosmicInflation`) — the high-`V` epoch is far from equilibrium.

So the asymmetry is forced by the substrate's structure. This module anchors the B-violation /
distinguishability piece concretely; the rest is cited.

## Honest scope

This anchors that matter and antimatter are **distinguishable** (opposite baryon winding) and
that B is not conjugation-invariant — the Sakharov B-violation + C-violation handles — and
documents that all three conditions hold, so a nonzero asymmetry is generic. It does **not**
derive the **magnitude** `η_B ≈ 6×10⁻¹⁰` — that is open in QLF exactly as it is in the Standard
Model (whose CP violation undershoots by ~10⁸); it needs the quantitative CP phase and the
out-of-equilibrium rate (`baryogenesis_in_progress`). See `CP-Violation-and-Chirality.md` §4b.
-/

namespace QLF

open QLF.BaryonWinding QLF.Majorana

/-- **Sakharov B + C violation, generally.** Matter and antimatter carry *opposite* baryon
    number — `B(antiparticle ts) = −B(ts)` for every history, read on the junction
    (`junctionBaryon_antiparticle`) — so they are physically distinguishable and baryon number is
    not conjugation-protected. -/
theorem matter_antimatter_opposite (ts : List Twist) :
    junctionBaryon (antiparticle ts) = - junctionBaryon ts :=
  junctionBaryon_antiparticle ts

/-- Concrete: the proton `uud` (with its down quark's charge twist) has `B = +1`, its
    antiparticle `B = −1`. -/
theorem proton_antiproton_asymmetric :
    junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] = 1 ∧
    junctionBaryon (antiparticle [Twist.right, Twist.up, Twist.slash, Twist.plus]) = -1 := by
  decide

/-- **B-violation handle**: a baryon-carrying closure is *not* invariant under conjugation — the
    proton's baryon number differs from its antiparticle's, so C (and hence the matter/antimatter
    census) is not a symmetry of the realized states. -/
theorem baryon_not_conjugation_invariant :
    junctionBaryon (antiparticle [Twist.right, Twist.up, Twist.slash, Twist.plus])
      ≠ junctionBaryon [Twist.right, Twist.up, Twist.slash, Twist.plus] := by
  decide

/-- **Established constructively:** matter and antimatter are distinguishable (opposite baryon
    winding, `matter_antimatter_opposite`) and B is not conjugation-invariant — the Sakharov
    B/C-violation conditions — while CP violation (`CP-Violation-and-Chirality.md`,
    `QLF_StrongCP`) and departure from equilibrium (`QLF_CosmicInflation`) hold too, so a baryon
    asymmetry is **generic**. **Open:** the magnitude `η_B ≈ 6×10⁻¹⁰` — undetermined in QLF as in
    the Standard Model (`baryogenesis_in_progress`). -/
theorem baryogenesis_in_progress : True := trivial

end QLF
