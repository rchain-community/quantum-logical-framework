# The Double-Slit Experiment in [QLF](README.md)

Feynman called the double slit "the only mystery" of quantum mechanics. In QLF it is not a mystery — it is the **physical face of a machine-checked theorem**: `count_does_not_determine_phase` ([`lean/QLF_PhaseInformation.lean`](lean/QLF_PhaseInformation.lean)). The fringe pattern is *phase* information that the *count* (Shannon) cannot carry; a which-path measurement trades that phase for count-definiteness; and "measurement" is just ZFA closure, so no collapse postulate is needed. The whole experiment is the count/phase distinction of [`Shannon_And_Phase.md`](Shannon_And_Phase.md), drawn on a screen.

---

## 1. The setup in QLF

A particle is not a tiny ball and not a literal wave — it is a **history exploring the possibility tree**. Between source and screen, the substrate generates every admissible ZFA-closed history (`expand_generation`); the physical event is the one that closes. Two open slits define **two families of admissible sub-histories** reaching a given screen point `φ`: the bundle `A` through the upper slit and the bundle `B` through the lower slit.

The amplitude at `φ` is the path-integral sum already derived in [`Born_Rule.md`](Born_Rule.md) §2 — the QuCalc realization of Feynman's sum-over-histories, with the path space restricted to admissible Pauli-closed histories:

$$\langle \varphi \mid \psi \rangle \;=\; \sum_{h \,\in\, \mathcal{T}_{\psi \to \varphi}} e^{\,i\,\theta(h)}\;=\; A_A + A_B,$$

where `θ(h)` is the cumulative QuCalc phase of history `h`, and `A_A`, `A_B` are the phase-coherent sums over the two slit bundles.

---

## 2. The fringes are phase, not count

The screen intensity is the Born-rule probability ([`Born_Rule.md`](Born_Rule.md) §3):

$$P(\varphi) \;\propto\; |A_A + A_B|^2 \;=\; |A_A|^2 + |A_B|^2 + 2\,\mathrm{Re}\!\left(A_A^{*} A_B\right).$$

The first two terms are the **counts** — how many ways to reach `φ` through each slit, the Shannon/multiplicity content. The third term — the **cross term** — is the fringe, and it is set entirely by the **phase difference** `θ_A − θ_B` (the path-length difference, accumulated as QuCalc phase). Bright fringe where the two bundles are in phase, dark where they are out of phase.

This is exactly `count_does_not_determine_phase` on a screen: across neighbouring screen points the *number* of contributing paths barely changes, yet the *intensity* swings from bright to dark — **same count, opposite result, because the phase differs.** The interference pattern is pure phase information; the count cannot encode it. (The same theorem says two histories with the identical twist multiset fold to `+I` vs `−I`; here two screen points with the same path-count light up or stay dark depending on phase.)

---

## 3. Which-path measurement: trading phase for count

Put a detector at the slits to learn *which* slit the particle went through. The fringes vanish — you get two plain bumps, `|A_A|^2 + |A_B|^2`, the bare counts. Why, in QLF?

A which-path detector is **an extra ZFA closure** that resolves the path into a **definite count distinction** ("upper" vs "lower"). By the count↔phase conjugacy — the [uncertainty principle](UncertaintyPrinciple.md), which in QLF *is* the Fourier-duality between the count face and the phase face — sharpening the path-count **smears the relative phase** `θ_A − θ_B` across the ensemble. The cross term `2 Re(A_A^* A_B)` then averages to zero, and only the counts survive. No fringe.

Nothing collapses in the textbook sense. The which-path closure simply moves the information from the **phase** (where the count cannot hold it) into a **count** (which Shannon can) — and by conjugacy you cannot keep both. Measurement is synchronization/closure, not a separate physical process ([`Measurement_Problem.md`](Measurement_Problem.md)). Erase the which-path record after the fact and the phase coherence is restored in the coincidence-sorted subset — the **delayed-choice quantum eraser**, already worked out in [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md).

---

## 4. Wave–particle "duality" dissolved

There is no paradox because the substrate is always **discrete histories**:

- The "**wave**" is the *phase structure of the multiplicity* — the `e^{iθ(h)}`-weighted sum over admissible paths. Interference is what phase-weighted counting looks like.
- The "**particle**" is the *single realized ZFA closure* — one history out of the multiplicity, selected with Born probability (the multiplicity principle, *the thing that can happen in the most ways happens most often*, [`Born_Rule.md`](Born_Rule.md), [`MRE.md`](MRE.md)).

"Goes through both slits" means the **possibility stream explores both bundles**; "lands as a dot" means **one closure realizes**. The two descriptions are the phase face and the count face of the one closure — the very pair the double slit is built to expose.

---

## 5. Honest scope

- The **mechanism** is the QLF content and it rests on proven pieces: the path-integral amplitude and interference Born rule ([`Born_Rule.md`](Born_Rule.md)), the count/phase separation (`count_does_not_determine_phase`, machine-checked), and measurement-as-closure ([`Measurement_Problem.md`](Measurement_Problem.md)). The which-path → no-fringe step is the uncertainty conjugacy ([`UncertaintyPrinciple.md`](UncertaintyPrinciple.md)).
- The **quantitative fringe spacing** (slit separation, de Broglie wavelength `λ = h/p`) is set by the phase-accumulation rate, i.e. the frequency-synthesis relations (`m = ℏf/R`, momentum ↔ phase) developed in [`Frequency_Synchronization.md`](Frequency_Synchronization.md) and [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md); it is not re-derived here. This doc owns the *structural* reading — fringes = phase, which-path = count, conjugacy = no fringes.

**The takeaway:** the double slit is the laboratory demonstration that amplitude (count) is not enough — phase is independent information. QLF proved that as a theorem; the screen shows it as light and dark.

## See also

- [`Shannon_And_Phase.md`](Shannon_And_Phase.md) · [`lean/QLF_PhaseInformation.lean`](lean/QLF_PhaseInformation.lean) — the count/phase separation, proved.
- [`Born_Rule.md`](Born_Rule.md) · [`Superposition.md`](Superposition.md) · [`Measurement_Problem.md`](Measurement_Problem.md) — amplitudes, superposition, closure-as-measurement.
- [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) — the eraser variant (fringes in coincidence subsets).
- [`UncertaintyPrinciple.md`](UncertaintyPrinciple.md) — the count↔phase conjugacy behind which-path-erases-fringes.
