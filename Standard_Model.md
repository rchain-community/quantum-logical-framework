# The Standard Model from [QLF](README.md) (honest synthesis)

**The Standard Model's particles, interactions, and conservation laws are claimed to follow from the 8-twist algebra plus ZFA closure plus Hermitian-pair structure.** This document is the **honest** version of that claim: what QLF actually derives today, what is a partial sketch with structural plausibility, and what is open work without even a clear path forward.

The structure follows [Conservation.md §8](Conservation.md) (the "what is NOT yet derived" list) but expands the positive content and provides a map of all the pieces.

## 1. The honest scoreboard

| Sector | What QLF says | Status |
|---|---|---|
| **Spin-1/2 algebra (Pauli, Dirac)** | Derived from 8-twist Pauli mapping ([HALF-SPIN-ZFA-EMBEDDING.md](HALF-SPIN-ZFA-EMBEDDING.md), [Lagrangian_Formulation.md](Lagrangian_Formulation.md)) | ✓ Derived; machine-verified `tau_xy_product` etc. |
| **Electron** (mass, charge, spin) | `^<` or `^<v>` chiral fluxoid; mass from gauge fold; charge from gauge-fold parity ([Electron.md](Electron.md), [Atom.md](Atom.md)) | ✓ Structurally derived; mass *ratio* to other leptons is open |
| **Photon** (massless, spin 1) | Pure spatial fold `^>` or `^v` with no gauge folds ([Electron.md §2](Electron.md), [Particles.md](Particles.md)) | ✓ Derived |
| **Neutrino** (left-handed, gauge-only) | non-chiral loop `^v` — **Majorana** (its own antiparticle), machine-verified `neutrino_majorana` ([`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)) per [Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md) | ✓ Structural + Lean-verified; predicts **0νββ** (lepton-number violation), under test (LEGEND/nEXO) |
| **Proton, neutron** (Borromean three-quark) | Three open quarks interlocked under Borromean topology ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md), [HadronicDepth.md](HadronicDepth.md)) | ✓ Structural derivation; mass quantitative match open |
| **Quark confinement** | Quarks are fractional ZFA (cannot exist as isolated unforgeable names) — must group in pairs/triples to form stable composite blankets | ✓ **Machine-verified obstruction** (`charged_not_closed`/`singlet_closure`, [`lean/QLF_Confinement.lean`](lean/QLF_Confinement.lean)): a net-colored state is not a ZFA closure, so only color singlets are physical; the string-tension *value* is open |
| **U(1) electromagnetic** | `+` ↔ `−` gauge swap symmetry of the 8-twist algebra ([Conservation.md §4](Conservation.md), [Maxwell.md](Maxwell.md)) | ✓ Derived; charge conservation Lean-verified via `no_magnetic_monopoles` |
| **Higgs mechanism** | Gauge folds create constructing delay $\Delta t = R/f$ which manifests as rest mass ([Higgs.md](Higgs.md), [Frequency_Synchronization.md](Frequency_Synchronization.md), [E_mc2_derivation.md](E_mc2_derivation.md)) | ⚠ Partial — explains *why* mass exists, not specific Higgs particle mass |
| **CP violation** | Residual clustering of LH/RH topology in the early universe ([CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md), [Annihilation.md §5](Annihilation.md)) | ⚠ Partial — qualitative; CKM matrix angles open |
| **Generation structure (3 lepton families, 6 quarks)** | Higher-order resonant harmonics of primordial split ([Primordial_Entanglement.md §2](Primordial_Entanglement.md), [Particles.md §3](Particles.md)) | ⚠ Partial — structural reason for "more than one", specific generation count open |
| **Strong SU(3) confinement** | Borromean three-element topology is the unique stable three-body closure | ⚠ Partial — SU(3) gauge group identification open |
| **Weak SU(2) doublets** | Pair-grouping under chirality — left-handed particles in SU(2) doublets, right-handed in singlets ([Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md), [Weak_Force.md](Weak_Force.md)) | ⚠ Partial — **Lie-algebra identification machine-verified** (`weak_isospin_su2`: the Σ₈ τ-subalgebra carries `[τᵢ,τⱼ]=−2εᵢⱼₖτₖ`, su(2)≅so(3); `Q₈⊂SU(2)`); doublet representation, coupling `g`, and W/Z masses open |
| **Baryon number conservation** | Topological winding number of composite blankets | ⚠ Partial — Noether-style derivation open |
| **Lepton number conservation** | Chiral fluxoid count of electron-type structures | ⚠ Partial — same |
| **Sterile neutrino** | Would require pure-`+` or pure-`-` gauge sequence with no spatial twists | ✗ Open — experimental status unsettled; QLF predicts a specific topology if it exists |
| **Specific lepton mass ratios** ($m_\mu / m_e \approx 207$, $m_\tau / m_e \approx 3477$) | Would follow from the multiplicity ratios at successive resonant harmonics | ✗ Open — no quantitative prediction yet |
| **CKM matrix angles, neutrino mixing** | Parameter count + CP condition machine-verified (3 angles + 1 phase; KM needs ≥3 generations — `QLF_FlavorMixing`); the angle *values* would follow from the chirality-rotation structure between generations | ⚠ Partial — counting/CP anchored, angle values open |
| **Dark matter sector** | Possibly a class of stable ZFA closures with no `+`–`−` content (no EM coupling) — see [DarkMatter.md](DarkMatter.md) | ✗ Open — qualitative speculation |

**Summary**: roughly 8 derived, 6 partial, 4 fully open. The framework is structurally rich but most quantitative numbers remain to be extracted.

## 2. The derived sector

### 2.1 Spinor algebra and the spin-1/2 carriers

The 8-twist alphabet's quaternionic Σ₈ algebra (`τ_i τ_j = -δ_{ij} I - ε_{ijk} τ_k`, with `τ_i = i σ_i`) is machine-verified in `lean/BraKetRhoQuCalc.lean` via `tau_xy_product`, `tau_yz_product`, `tau_zx_product`. The Pauli algebra it generates is the algebra of spin-1/2, exactly. See [Lagrangian_Formulation.md](Lagrangian_Formulation.md) for the full statement.

The 1/2-spin atom of [MRE.md](MRE.md) is the smallest carrier of this algebra; every Standard Model fermion is built from parallel compositions of these atoms.

### 2.2 Electron, photon, neutrino

From [Electron.md](Electron.md) and [Particles.md](Particles.md):

- **Electron** `^<` (or compositely `^<v>`) — chiral fluxoid that gauge-folds; carries mass via the constructing delay and charge via the gauge parity.
- **Photon** `^>` (or `^v`) — pure spatial fold with no gauge folds; massless; carries no charge; the canonical massless quantum.
- **Neutrino** `^v` — non-chiral loop; no transverse spatial extent; nearly non-interacting; **Majorana** (its own antiparticle): the `^v` loop is a fixed point of the Hermitian conjugate (conjugate-and-reverse), machine-verified `neutrino_majorana`, so lepton number is violated and QLF predicts **0νββ** (per [Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md) §1).

These three are the directly derived light particles. Positron, anti-photon, anti-neutrino follow by Hermitian conjugation ([Annihilation.md §2](Annihilation.md)).

### 2.3 Proton, neutron, and quark confinement

From [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md): three quarks interlock via Borromean topology to form a closed Markov blanket — the proton. Each quark individually has fractional ZFA (it leaks free action) so cannot exist as an isolated unforgeable name; only the Borromean triple is stable.

This is the QLF derivation of quark confinement, **machine-verified** as the singlet-closure obstruction (`charged_not_closed`/`singlet_closure`, [`lean/QLF_Confinement.lean`](lean/QLF_Confinement.lean)): a net-colored state carries an annihilation-odd charge that is zero on every ZFA closure, so a lone quark cannot close — only color singlets are physical. The strong-force binding *scale* (string tension) is open work, but the structural reason for confinement is built into the algebra and Lean-anchored.

### 2.4 U(1) electromagnetism, charge conservation

From [Maxwell.md](Maxwell.md) and [Conservation.md §4](Conservation.md): the gauge pair `+` / `−` is the carrier of charge. The U(1) gauge symmetry is the `+` ↔ `−` swap symmetry of the 8-twist algebra; charge conservation is Lean-verified as `no_magnetic_monopoles` (ZFA closure requires net gauge count = 0 per closed event; for non-neutral systems the count is constant because gauge folds are created/destroyed only in Hermitian pairs).

**Anomaly cancellation / matter neutrality is a ZFA charge-balance** ([`lean/QLF_ChargeBalance.lean`](lean/QLF_ChargeBalance.lean)). Electric charge is a *signed twist count* (`QLF_BMinusL`), so a complete generation's charge ledger *closes*: with QLF's derived charges (neutrino `0`, lepton `−1`, quarks `+2/3`/`−1/3` — the thirds forced by the 3 colours), one generation sums to **`Σ Q = 0 + (−1) + 3·(2/3) + 3·(−1/3) = 0`** (`gen_electric_neutral`). This is not a trivial `0 = 0`: the up-type `+2` balances the charged-lepton-plus-down-type `−2` (`gen_charge_balanced`) — the quark thirds are *exactly* what make the ledger close, so the 3 colours are what make matter neutral. Concrete closures: proton `uud = +1`, neutron `udd = 0`, hydrogen atom neutral (`hydrogen_neutral`). The *squared*-charge census — the QED vacuum-polarization running weight — is the complementary **`Σ Nᶜ Q_f² = 8 = 2³`** (leptonic 3 + hadronic 5, [`lean/QLF_ChargeCensus.lean`](lean/QLF_ChargeCensus.lean)), feeding the census derivation of the α running ([Alpha.md §4a](Alpha.md), issue [#117](https://github.com/jimscarver/quantum-logical-framework/issues/117)).

**The full anomaly-cancellation miracle is the same ledger-closure** ([`lean/QLF_AnomalyCancellation.lean`](lean/QLF_AnomalyCancellation.lean)). The Standard Model is quantum-mechanically consistent only because a set of otherwise-unrelated charge sums *all vanish* per generation — on the substrate, the hypercharge ledger *closes* for **every** gauge current. On the SU(5) `5̄ ⊕ 10 = 15` content ([`QLF_SU5`](lean/QLF_SU5.lean)), with `Y = Q − T₃` fixed by QLF's derived `Q` (thirds from the 3 colours) and `T₃` (weak isospin), all five anomalies vanish: gravitational/`[U(1)]` `Σ Y = 0` (`grav_anomaly_zero`), `[U(1)]³` `Σ Y³ = 0` (`cubic_anomaly_zero`), `[SU(2)]²·U(1)` (`su2_anomaly_zero`), `[SU(3)]²·U(1)` (`su3_mixed_anomaly_zero`), and `[SU(3)]³` (`su3_cubic_anomaly_zero`), bundled as **`generation_anomaly_free`**. So gauge-theory consistency — the SM's deepest structural constraint — is, on the substrate, the ZFA charge-balance of a complete generation.

## 3. The partial sector

### 3.1 Higgs mechanism

From [Higgs.md](Higgs.md): mass is the constructing delay accumulated inside a gauge-folded Markov blanket. The Higgs field, in QLF, is the vacuum's gauge-fold density — the property of the vacuum that determines how much delay each particle accumulates per ZFA closure.

**What's derived**: gauge folds → mass. Why some particles are massive (have gauge folds) and others (photon) are massless.

**What's open**: the specific Higgs particle (a separate boson) with the observed 125 GeV mass; the Yukawa coupling structure that gives different fermions different masses; the Higgs potential's vacuum expectation value.

### 3.2 CP violation and matter dominance

From [CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) and [Annihilation.md §5](Annihilation.md): in a perfectly balanced universe all matter would annihilate. The residual matter dominance arises from slight clustering bias: clusters of one chirality (LH or RH) have thicker Markov-blanket boundaries that out-replicate the boundary annihilation rate, becoming topological attractors.

**What's derived**: why matter survives. The mechanism is consistent and demonstrated in `cp_violation_sim.py`.

**What's open**: the specific CP-violating phase angles in the CKM matrix; the matter/antimatter ratio quantitative match to the observed $\sim 10^{-9}$ baryon-to-photon ratio.

### 3.3 Generations of matter

From [Primordial_Entanglement.md §2](Primordial_Entanglement.md) and [Particles.md §3](Particles.md): if a primordial split doesn't immediately close at length $N=4$ due to environmental pressure, it is driven into higher-order resonance to achieve ZFA: $N=8$ (muon family), $N=12$ (tau family).

**What's derived**: why there are multiple generations; the structural reason for the resonant-harmonic hierarchy.

**What's open**: why exactly **three** generations and not two or four; the specific mass ratios $m_\mu / m_e \approx 207$, $m_\tau / m_\mu \approx 16.8$; the lepton-quark mass-ratio correlation across generations.

**Colour content vs colour charge — the structure question.** A generation is *not* colour-**charged**: leptons are colour **singlets** (`B = 0`, `singlet_closure`), which is exactly *why* they are free (a net-coloured lepton would be confined). But a singlet is not structureless — the electron loop `^<v>` is machine-verified to engage **two** of the three axes, x and y, not z (`interleaved_xlvr_folds_to_negI`, [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean)). Since `num_generations_eq_three` ties the three generations to the three axes, the open structural question is each generation's **axis/colour content** — which axes the muon (`N=8`) and tau (`N=12`) loops occupy relative to the electron's `{x, y}` — held colour-neutral (`B = 0`, else it would be a confined baryon, not a free lepton). *That* content, not a hidden charge, is where the mass ratios above would be decided. Full treatment: [`Particle_Ladder.md`](Particle_Ladder.md) § *Colour content vs colour charge*.

### 3.4 Strong SU(3) and weak SU(2) groups

From [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) and [Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md): the strong force is the Borromean three-quark binding; the weak force is the gauge-fold pair-flip that mediates beta decay.

**What's derived**: the structural reason for confinement (SU(3)-like three-element grouping) and for chirality-mediated weak interactions (SU(2)-like doublet structure). **Both gauge Lie algebras are machine-verified** as the symmetry of the three spatial axes: the **weak SU(2)** is the Σ₈ τ-subalgebra (`[τᵢ,τⱼ] = −2εᵢⱼₖτₖ`, `Q₈ ⊂ SU(2)` — `weak_isospin_su2`), and the **strong SU(3)** is the traceless part of the 3×3 directional tensor (closed under the bracket and non-abelian — `trace_commutator_zero` + `gluon_commutator_nonzero` in [`lean/QLF_StrongAlgebra.lean`](lean/QLF_StrongAlgebra.lean)). With `U(1)` (`no_magnetic_monopoles`), all three SM gauge algebras are verified, with dimensions `1 + 3 + 8 = 12` (`1 + 8 = 9 = N`, the α tensor) — see [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md).

**What's open**: the SU(2) **doublet representation** and coupling `g`; the `SU(3)` `finrank = 8` count (elementary codim-1, not yet a Lean theorem); matching the gauge-boson masses ($W^\pm$, $Z^0$, gluons); the running of the coupling constants (asymptotic freedom).

## 4. The fully open sector

### 4.1 Quantitative mass spectrum

Standard Model masses span 11 orders of magnitude (neutrino at <1 eV, electron at 511 keV, top quark at 173 GeV). QLF says mass comes from gauge-fold constructing delay; the specific delay values for each particle type are open.

Conjectured path: the multiplicity-as-energy framework of [Energy_Combinatorics.md](Energy_Combinatorics.md) plus the topological resonance counting of [HadronicDepth.md](HadronicDepth.md).

**One quantitative handle exists (charged leptons).** The Koide relation `Q = (m_e+m_μ+m_τ)/(√m_e+√m_μ+√m_τ)² = 2/3` holds to 0.0009%, and its `2/3` is **machine-verified** as following by construction from `N=3` (three spatial axes) ∧ `A²=2` (two transverse axes) — `koide_two_thirds` in [lean/QLF_Koide.lean](lean/QLF_Koide.lean), the same `2 transverse + 1 longitudinal` split as the transverse fraction. Given `Q=2/3`, `m_e, m_μ` **predict** `m_τ = 1776.97 MeV` (measured 1776.86, **0.006%**). What remains an input: the lepton-√mass↔axis-phase *identification*, the Koide angle, and the overall scale. See [Weak_Force.md](Weak_Force.md) §5a–5b and [koide_tau_demo.py](koide_tau_demo.py). The quark sector is still open.

### 4.2 Mixing matrices (CKM, PMNS)

The CKM matrix encodes quark mixing across generations; PMNS encodes neutrino mixing. Both have specific angle structures whose origin is unexplained in standard physics.

**What the substrate fixes — the parameter count and the CP condition** (machine-verified, [`lean/QLF_FlavorMixing.lean`](lean/QLF_FlavorMixing.lean)). An `N×N` unitary mixing matrix carries `N(N−1)/2` physical mixing angles (`mixing_angles`) and `(N−1)(N−2)/2` CP-violating phases (`cp_phases`). QLF has **exactly three generations** (`num_generations = 3`, [`QLF_Generations`](lean/QLF_Generations.lean)), so the CKM/PMNS content is exactly **3 angles + 1 CP phase** (θ₁₂, θ₂₃, θ₁₃ + δ; `substrate_mixing_parameters`). And the **Kobayashi–Maskawa condition** falls out: a physical CP phase needs `(N−1)(N−2)/2 ≥ 1`, i.e. `N ≥ 3` — `0` phases for one or two generations (the Cabibbo case has one angle, no CP), `1` for three (`cp_requires_three_generations`). So the substrate's three-ness — the same `3` behind Koide, colour SU(3), and `α`'s `N=3²` — is *why CP violation is possible at all*.

**What the substrate also fixes — unitarity = closure** ([`lean/QLF_CKM.lean`](lean/QLF_CKM.lean)). The mixing matrix is **unitary**, and in QLF unitarity *is* closure: flavor mixing **rotates** flavor without creating or destroying it (the ZFA-balanced total is conserved). For the Cabibbo block `V_ud = cos θ_C`, `V_us = sin θ_C`, the first-row unitarity `|V_ud|² + |V_us|² = cos²θ_C + sin²θ_C = 1` (`cabibbo_row_unitarity`) is just the Pythagorean identity — each up-type quark's branching across down-types sums to 1; the rows are orthogonal (`cabibbo_rows_orthogonal`), giving `V Vᵀ = I` and the closing **unitarity triangle** (the geometric home of the Jarlskog CP area). So CKM unitarity is not an extra postulate — a flavor rotation that preserves closure is exactly an orthogonal/unitary matrix.

**What is open — the angle values.** The mixing-angle *values* (the Cabibbo angle, the large PMNS angles, the phase δ) live in the Yukawa/mass-matrix sector QLF flags as open (the Koide angle δ is itself an input; no quark masses). Conjectured path: chirality-rotation between generations under the resonant-harmonic hierarchy, with a structural contrast — quarks (hidden, confined chirality) mix *small* and hierarchically, leptons (exposed chirality) mix *large* (near tri-bimaximal: `sin²θ₁₂ ≈ 1/3`, θ₂₃ near-maximal, broken by `θ₁₃ ≈ 8.6°`) — read on the same hidden/exposed-chirality axis as the pion/black-hole work. Not derived (`flavor_mixing_in_progress`).

### 4.3 Sterile neutrino, fourth generation, exotic particles

QLF makes no specific prediction for exotic-sector existence beyond the three known generations. Experiments would constrain QLF's resonance structure at higher $N$.

### 4.4 Dark matter, dark energy

From [DarkMatter.md](DarkMatter.md): dark matter may be a class of stable ZFA closures with no `+`–`−` gauge content (and hence no electromagnetic coupling). Speculative.

Dark energy = cosmological constant residual per [Quantum_Gravity.md §5](Quantum_Gravity.md). Qualitatively explained, quantitatively open.

## 5. Why the partials and opens matter

QLF claims to be a discrete substrate from which the Standard Model emerges. Until the partials become derivations and the opens become predictions, the claim is **structurally promising but quantitatively unverified**. The same standard that [Experimental_Consistency.md](Experimental_Consistency.md) applies to fundamental constants applies here: positive structural derivations (§2) are real progress; partial sketches (§3) are research targets; full opens (§4) are honest gaps.

The path forward is to:
1. Pick a single partial item and convert it to a derivation (e.g., the SU(3) confinement scale, which has the most-developed structural account).
2. Extend the numerical demos (`particles.py`, `path_integral.py`, `constants_mapper.py`) to enumerate the resonance hierarchy and check whether the multiplicity-counting reproduces lepton mass ratios.
3. Add a Lean theorem `standard_model_particles_are_zfa_closures` for the derived sector (§2) — even at this scope it would be a substantive formalization.

## 6. Open work

- **Lean theorem**: `standard_model_particles_are_zfa_closures` formalizing the §2 derivations.
- **Numerical demo**: enumerate atomic-system closures via `path_integral.py` (per [`Bound_States_QLF.md`](Bound_States_QLF.md), free-lepton ratios are not the natural QLF observables — atomic-system masses are). Targets: positronium, muonium, hydrogen.
- **Gauge-group identification**: identify the specific SU(3), SU(2), U(1) subgroups of the 8-twist algebra in Lean. The U(1) is done (`no_magnetic_monopoles` already encodes it); SU(2) and SU(3) are open.
- **Mass ratios from multiplicity**: scoped per [`Bound_States_QLF.md`](Bound_States_QLF.md) to atomic-system masses (positronium 1.022 MeV, muonium 106.17 MeV, hydrogen 938.78 MeV). [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) writes out the joint-closure mapping for each atomic system and derives the Bohr reduced-mass scaling `E(Mu)/E(Ps) ≈ 2`, `E(H)/E(Mu) ≈ 1`. The per-qubit reading [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md) gives `m_qubit c² = ℏω = E_Planck / R_qubit` and reproduces all measured mass ratios via `m_X/m_Y = R_Y/R_X` exactly. α is numerically anchored at 10⁻¹⁰ via the QLF Bohr inversion `α = sqrt(2 R_e / R_1)` ([`Hydrogen.md`](Hydrogen.md) §4.1, [`fine_structure_demo.py`](fine_structure_demo.py)). The open piece is the first-principles derivation of the depth `R_e ≈ 2.4 × 10²²` from QLF closure-multiplicity, which under the unit identification would derive `α R_e = m_e` independently of the measured Ry and m_e inputs.
- **Mixing angles from chirality rotation**: develop the structural account into a quantitative prediction.
- **Higgs particle**: distinguish the Higgs *field* (vacuum gauge-fold density, qualitatively derived) from the Higgs *boson* (excitation of that field, observed at 125 GeV); derive the boson mass.

## 2026 update

2026 Standard Model results read on the substrate: the doubly charmed `Ξcc⁺` and `Ωcc⁺`, the baryon
junction, entangled Z pairs, the `B → Kπμμ` tension (GIM proved as `gim_shift`), and CMS's
compositeness limits. See [Discoveries_2026](Discoveries_2026.md#p2) §1–§3, §9 and V9.

## References

### Internal

- [Particles.md](Particles.md) — particle-as-unforgeable-name framing; electron/neutrino derivations
- [Electron.md](Electron.md) — electron and photon worked examples
- [Higgs.md](Higgs.md) — mass-generation via gauge folds
- [Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md) — chirality, the Majorana neutrino (0νββ), beta decay
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — Borromean three-quark topology for hadrons
- [HadronicDepth.md](HadronicDepth.md) — hadronic resonance hierarchy
- [CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) — CP violation and matter dominance
- [HALF-SPIN-ZFA-EMBEDDING.md](HALF-SPIN-ZFA-EMBEDDING.md) — spin-1/2 set-theoretic embedding
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — Σ₈ algebra; Lean-verified spinor structure
- [MRE.md](MRE.md) — 1/2-spin atom as the smallest carrier of the algebra
- [Atom.md](Atom.md) — LH proton / RH electron assignment
- [Maxwell.md](Maxwell.md) — U(1) electromagnetism; charge conservation
- [Conservation.md](Conservation.md) — Noether-style derivations; §8 what is NOT yet derived
- [Frequency_Synchronization.md](Frequency_Synchronization.md) — gauge folds create mass
- [E_mc2_derivation.md](E_mc2_derivation.md) — mass-energy equivalence
- [Energy_Combinatorics.md](Energy_Combinatorics.md) — multiplicity as energy
- [Annihilation.md](Annihilation.md) — Hermitian-pair structure; CP residual
- [DarkMatter.md](DarkMatter.md) — speculative dark-matter framing
- [Quantum_Gravity.md](Quantum_Gravity.md) — dark energy as cosmological-constant residual
- [Primordial_Entanglement.md](Primordial_Entanglement.md) — primordial split → generations of matter
- [eight-twists-sufficiency.md](eight-twists-sufficiency.md) — 8 twists as complete generative kernel
- [Experimental_Consistency.md](Experimental_Consistency.md) — falsifiability framework

### External

- Glashow, S. L. (1961). *Partial-symmetries of weak interactions.* Nucl. Phys. 22, 579 — electroweak unification.
- Weinberg, S. (1967). *A model of leptons.* Phys. Rev. Lett. 19, 1264 — Standard Model.
- Salam, A. (1968). *Weak and electromagnetic interactions.* In *Elementary Particle Theory* (Almqvist).
- 't Hooft, G. (1971). *Renormalizable Lagrangians for massive Yang-Mills fields.* Nucl. Phys. B 35, 167 — renormalization of gauge theories.
- Peskin, M. E., Schroeder, D. V. (1995). *An Introduction to Quantum Field Theory.* Westview Press — canonical reference.
- Workman, R. L. et al. (Particle Data Group) (2024). *Review of Particle Physics.* Prog. Theor. Exp. Phys. 2024, 083C01 — current experimental status.
