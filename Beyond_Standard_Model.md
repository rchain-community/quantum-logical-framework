# Beyond the Standard Model — what [QLF](README.md) derives, predicts, and leaves open

**The honest accounting of where QLF goes past the Standard Model — and where it doesn't.** Companion to [`Open_Problems.md`](Open_Problems.md). The Standard Model is the most precise theory in science, but it has **~19 free parameters** (≈26 once the neutrino sector is included) and **explains none of them** — α, the fermion masses, the mixing angles are measured and plugged in. "Beyond the SM" therefore means two different things, and QLF does genuinely different things in each:

- **(A) Explaining the SM's inputs** — deriving what the SM takes as given. This is *math*, and several pieces are **machine-verified**. It is retrodiction (matching known numbers), not prophecy.
- **(B) Beyond-SM physics** — predictions that differ from, or go past, the SM and await experiment. These **cannot be proved** (physics is empirical); they get tested.

The bright line: ✅ **derived** (machine-verified the value is *not free* but a consequence of substrate structure) · 🔭 **predicted** (falsifiable, untested) · 🔵 **open**.

**Falsifiability at a glance.** The sharp, currently-testable verdicts (details in §3, [`Experimental_Consistency.md`](Experimental_Consistency.md) §10):

| Observation | Verdict on QLF |
|---|---|
| **0νββ detected at LEGEND-1000 / nEXO reach** (`m_ββ ≳ 1 meV`) | ❌ **refutes** the refinement — only ν₁ is Majorana, so `m_ββ ≈ 0.25 meV` ([`Lepton_Generations_Fourier.md`](Lepton_Generations_Fourier.md) §6) |
| **0νββ at `m_ββ ≈ 0.25 meV`** (beyond any planned experiment) | ✅ **supports** — the Majorana ν₁ (`neutrino_majorana`, `one_axis_majorana`) |
| **all three neutrinos shown to be Dirac** (definitive) | ❌ **refutes** — QLF entails a Majorana ν₁ |
| **inverted mass ordering** established (JUNO / DUNE) | ❌ **refutes** the Koide neutrino solution (normal ordering, `Σm ≈ 0.059 eV`) |
| **a dark-matter particle detected** (WIMP, axion-DM, …) | ❌ **refutes** emergent-DM — dark matter is denser logic, no particle |
| **cosmological drift of `α(0)`** confirmed | ❌ **refutes** the substrate — `α` is atemporal (`no_cosmological_drift_of_alpha`) |
| **`α⁻¹` outside `137 < α⁻¹ < 137.048`** | ❌ **refutes** the leading α construction |
| **TeV-scale superpartners** (squarks/sleptons) | ❌ **against** QLF — no doubled spectrum (§3c) |
| **`v_GW ≠ c`** | ❌ **refutes** the synthesized-metric reading |

---

## 1. The SM free-parameter ledger

| SM parameter(s) | QLF status | the *derivation* / prediction |
|---|---|---|
| **α** (EM coupling) | ✅ **derived** to 0.026%; 🔭 **+ a prediction the SM can't make** (no α drift, §3) | `alpha_QLF_eq` = 1/137 — the IR (`q²→0`) coupling of fully-rendered 3-D space; closed form `α(d)=1/(128+d²)` so `only_3d_substrate_gives_137` (2D→1/132, 4D→1/144, 5D→1/153) — α requires a **3-D** substrate. Canonical doc [`Alpha.md`](Alpha.md) |
| **3 charged-lepton masses** | ✅ 1 relation derived; 🔵 2 inputs left | `koide_two_thirds`: `Q=2/3` follows from 3 generations ∧ 2 transverse axes ⇒ `m_τ` from `m_e,m_μ` (0.006%). Scale + Koide angle remain inputs |
| **g₂, g₃** (weak, strong couplings) | 🔵 open | the gauge *algebras* are verified (`weak_isospin_su2`, `trace_commutator_zero`); the couplings are not derived |
| **6 quark masses** | 🔵 open — but *category-corrected* (machine-verified) | quark masses are **non-observable** — a lone quark is not a ZFA closure (`quark_not_closed`, [`lean/QLF_QuarkMass.lean`](lean/QLF_QuarkMass.lean)), so its mass is scheme-dependent; the observable is the **hadron** closure mass and its splittings `m_n−m_p = (m_d−m_u) − EM` (the `d↔u` weak vertex). QLF *predicts* no clean quark-mass relation; the open target is the **hadron splitting spectrum** ([`Weak_Force.md`](Weak_Force.md) §5d) |
| **4 CKM angles+phase** | 🔵 open | flavor change = gauge-fold pair-flip (operation); mixing angles open |
| **Higgs mass, VEV** | 🔵 open | mechanism reframed (gauge-fold delay, [`Higgs.md`](Higgs.md)); the 125 GeV and `v=246 GeV` not derived |
| **neutrino masses, PMNS** | 🔵 open masses; ✅ **mass type fixed**: Majorana (neutrino) vs Dirac (charged), `majorana_mass_only_neutrino` ([`lean/QLF_NeutrinoMass.lean`](lean/QLF_NeutrinoMass.lean)); ✅ **PMNS unitary + `1 Dirac + 2 Majorana = 3` CP phases** (`pmns_total_cp_phases`, [`lean/QLF_PMNS.lean`](lean/QLF_PMNS.lean)); 🔭 **Majorana nature → 0νββ** (§3) | — |
| **θ_QCD** (strong-CP) | ✅ **derived as 0** (no axion) | `theta_zero_on_closure`: every CP-odd topological winding is zero on every ZFA closure ⟹ `θ̄=0` on all physical states — with **no Peccei–Quinn axion** (ZFA closure does the axion's job) ([`lean/QLF_StrongCP.lean`](lean/QLF_StrongCP.lean)) |

**Honest tally:** of the ~19–26 SM parameters, QLF *firmly derives* **one** fundamental coupling (α), **one relation** among the three lepton masses (Koide), and **`θ̄=0`** (the strong-CP angle — with no axion). That is a handful — but the SM derives **zero** (and needs a hypothetical axion to address `θ̄` at all), and the difference is the whole point: see §2. The deeper structural claim — that the *dimensionless force strengths* all root in α (itself `N=3²`) plus the integers `2,7`, leaving **one empirical mass** as the only scale input — is [`Forces_From_Alpha.md`](Forces_From_Alpha.md).

---

## 2. The machine-verified beyond-SM content — *derivation*, not fitting

The SM cannot even *formulate* "why is α 1/137" or "why is Ω_Λ ≈ 0.69." QLF's beyond-SM theorems are not the values (anyone can fit a value) — they are the **counterfactuals proving the values follow** from substrate structure the SM leaves unexplained:

- **α requires 3 spatial dimensions.** `alpha_QLF_eq : alpha_QLF = 1/137` with the closed form `α(d)=1/(128+d²)` (`alpha_at_dim_closed_form`): `alpha_QLF_2d_counterfactual` (2D → 1/132), `alpha_QLF_4d_counterfactual` (4D → 1/144), `alpha_at_dim_five` (5D → 1/153), `only_3d_substrate_gives_137` ([`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean)). The fine-structure constant *and* the 3-dimensionality of space are the same fact — and 3-D is **over-determined**: the higher-`d` values don't merely miss α, they break stable atoms (by QLF's own `V∝1/r^(d−2)` law, Ehrenfest), the nuclear `ℓ=3` magic numbers, and the 3-axis gauge unification at once ([`Alpha.md`](Alpha.md) §4a).
- **Koide `Q=2/3` requires 3 generations and 2 transverse axes.** `koide_two_thirds` ([`lean/QLF_Koide.lean`](lean/QLF_Koide.lean)); only `N=3 ∧ A²=2` give 2/3 ([`koide_tau_demo.py`](koide_tau_demo.py) §3b counterfactuals).
- **Ω_Λ = log 2 requires exactly the 2 gauge axes.** `Omega_Lambda_QLF = Real.log 2` with `only_2_gauge_matches_observed_Omega_Lambda` (4-gauge → 2 log 2, 0-gauge → 0) ([`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)).
- **m_p/m_e = 6π⁵** (`mass_ratio_QLF_eq`, 0.002%), with counterfactuals tying it to 3-quark permutation symmetry.
- **The SM gauge group is the symmetry of the 3 axes** — all three gauge algebras machine-verified (`no_magnetic_monopoles`, `weak_isospin_su2`, `trace_commutator_zero`), dims `1+3+8=12`, `1+8=9=N` ([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)).
- **The neutrino is Majorana, the electron is Dirac** — `neutrino_majorana` / `electron_not_majorana` ([`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)): the antiparticle is the Hermitian conjugate (conjugate-and-reverse), the neutrino loop `^v` is a fixed point of it, the electron loop is not. The SM is *agnostic* on Dirac-vs-Majorana; QLF entails it (given the `^v` assignment), and entails that *only* the neutrino is self-conjugate. So a lepton-number-violating **Majorana mass** is available to the neutrino and *only* the neutrino (`majorana_mass_only_neutrino`, [`lean/QLF_NeutrinoMass.lean`](lean/QLF_NeutrinoMass.lean)) — the charged leptons are Dirac — and the **PMNS** matrix accordingly carries `N−1 = 2` *extra* Majorana phases (`1 Dirac + 2 Majorana = 3` total, `pmns_total_cp_phases`, [`lean/QLF_PMNS.lean`](lean/QLF_PMNS.lean)), unlike CKM's single Dirac phase. The empirical signature is `0νββ` (§3).
- **The strong-CP angle is derived as zero — with no axion.** `theta_zero_on_closure` ([`lean/QLF_StrongCP.lean`](lean/QLF_StrongCP.lean)): every CP-odd (annihilation-odd) signed count is **zero on every ZFA closure** (reusing `wcount_zero_on_ZFA`), so `θ̄=0` on every physical state. The SM has no explanation for the observed `θ̄ < 10⁻¹⁰` (the strong-CP fine-tuning puzzle) and the standard fix postulates a hypothetical **Peccei–Quinn axion**; QLF needs none — ZFA closure does the axion's job. Deriving `θ̄=0` *without a new particle* is a genuine beyond-SM result.
- **Anomaly cancellation is a ZFA charge-balance — every gauge anomaly cancels by construction.** The SM's deepest consistency constraint (the gauge theory is quantum-mechanically consistent only because a set of otherwise-unrelated charge sums all vanish per generation) is, on the substrate, the hypercharge **ledger closing**. Electric neutrality first: a complete generation sums to `Σ Q = 0` (`gen_electric_neutral`, [`lean/QLF_ChargeBalance.lean`](lean/QLF_ChargeBalance.lean)) — the up-type `+2` balancing charged-lepton+down `−2`, so the quark **thirds (forced by the 3 colours) are what make matter neutral**. Then all five gauge anomalies vanish on the SU(5) `5̄⊕10=15` content, with `Y = Q − T₃` from the *derived* `Q` and `T₃`: gravitational, `[U(1)]³`, `[SU(2)]²U(1)`, `[SU(3)]²U(1)`, `[SU(3)]³` — bundled as **`generation_anomaly_free`** ([`lean/QLF_AnomalyCancellation.lean`](lean/QLF_AnomalyCancellation.lean)). The complementary squared-charge census `Σ Nᶜ Q_f² = 8 = 2³` (the 8-twist alphabet size, leptonic 3 + hadronic 5; [`lean/QLF_ChargeCensus.lean`](lean/QLF_ChargeCensus.lean)) is the weight of the census-derived α running ([`Alpha.md`](Alpha.md) §4a, issue [#117](https://github.com/jimscarver/quantum-logical-framework/issues/117)). The SM *imposes* anomaly-freedom as a consistency requirement on hand-assigned hypercharges; QLF *derives* the charges and finds the ledger already closed.

This is the real, provable "beyond SM": **the SM's unexplained constants are derived consequences of one substrate** — verified for a handful, with the *derivation* (not just the value) machine-checked.

---

## 3. The falsifiable predictions — beyond-SM physics, awaiting experiment 🔭

You cannot *prove* beyond-SM physics; you test it. QLF makes **two sharp, clean, currently-testable** commitments the SM cannot.

**(i) Neutrinos are Majorana** (`ν = ν̄`) → **neutrinoless double-beta decay** (`0νββ`).

The SM is *agnostic* (Dirac vs Majorana is open); QLF **entails Majorana** and this is **machine-verified**: the antiparticle is the Hermitian conjugate (conjugate-and-reverse), and the neutrino loop `^v` is a *fixed point* of it — `neutrino_majorana` ([`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)) — while the electron is **not** (`electron_not_majorana`, so the charged lepton is Dirac). The neutrino is the unique self-conjugate fermion (the only one with neither charge nor chiral/linked structure). So lepton number is violated and **`0νββ` (`ΔL=2`) is the signature** ([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) §1, [`Experimental_Consistency.md`](Experimental_Consistency.md) §10). **Refinement (2026-10-19, [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) §1a):** `^v` is the one-axis closure ν₁, which must be Majorana (`one_axis_majorana`); ν₂ and ν₃ (two and four axes) are Dirac in most ways. Only ν₁ drives `0νββ`, so `m_ββ ≈ 0.25 meV`, about 40× below LEGEND-1000 and nEXO. A null there is expected and a signal there refutes the refinement. This is the corpus's clearest empirical commitment distinguishable from the Standard Model.

*What stays open, stated precisely:* QLF fixes ν₁'s **type** (Majorana) and the **count** of PMNS parameters (`pmns_total_cp_phases`), but **not** the *quantitative* sector — the absolute mass scale, the two mass-squared splittings `Δm²₂₁`, `Δm²₃₁` (and the ordering), the three mixing angles, and the CP-phase values are all 🔵 open. Koide applied to the measured splittings *does* pick the ordering (normal) and the masses (`0.36, 8.62, 50.1 meV`), as a pre-registered prediction rather than a derivation ([`Lepton_Generations_Fourier.md`](Lepton_Generations_Fourier.md) §6). A successful derivation would have to deliver all of these from the substrate; none is yet in hand ([`Open_Problems.md`](Open_Problems.md)).

**(ii) The fundamental fine-structure constant `α(0)` does not drift over cosmological time.** The SM treats `α(0)` as a *free input* that varying-constants models can promote to a slowly-drifting scalar field (dilaton-style) — it is *agnostic*. QLF **forbids** it: α is a function of the rendering dimension alone, `α(d)=1/(128+d²)` (`alpha_at_dim_closed_form`) — **no time argument** — so `α(0)=1/137` is an atemporal structural fact (`no_cosmological_drift_of_alpha`, [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean); [`Alpha.md`](Alpha.md) §5). A confirmed cosmological drift of `α(0)` would **falsify the QLF substrate** — it cannot be absorbed by it, unlike in the SM. **Quasar-absorption spectroscopy and atomic-clock comparisons are testing `Δα/α` now**; the mainstream null result is the prediction (the SM-side "running of the *effective* α with energy" is a separate, real effect — [`Alpha.md`](Alpha.md) §4 — not a drift of the fundamental value). A second clean, distinguishable, Lean-anchored commitment.

Softer, also beyond-SM but less sharp:
- **Dark matter is not a particle** — emergent vacuum time-folding ([`DarkMatter.md`](DarkMatter.md)); prediction: no DM particle is found (consistent with decades of null WIMP searches).
- **Matter won over antimatter generically** — the three Sakharov conditions are structurally met (B-violation via winding + Majorana `B−L`, C/CP via the chirality engine + strong-CP, out-of-equilibrium via expansion; `QLF_Baryogenesis`), so a matter excess is generic. The SM has the framework but too little CP violation; QLF shows the conditions hold. The *magnitude* `η_B ≈ 6×10⁻¹⁰` is open (as in the SM, `baryogenesis_in_progress`).
- **Sterile neutrino**, *if* it exists, is a specific pure-gauge (no-spatial-twist) sequence.

---

## 3b. Completeness — no hidden variables (why QLF *supersedes*, not patches) — issue [#78](https://github.com/jimscarver/quantum-logical-framework/issues/78)

QLF takes quantum **completeness** as a result, not a discomfort. There are **no hidden variables**:
the quantum logical (ZFA) description of a system is *complete*, and **entanglement — the quantum
creation operator — is all there is**. Nothing waits underneath to be discovered.

The empirical backing is **quantum computation itself**. High-fidelity QC and quantum error
correction work *only because* the quantum description is **causally closed** — no uncontrolled
sub-quantum channel leaks in. If any "tiny influence" (gravity, a hidden field, a sub-quantum
variable) were a *separate fundamental* input, it would inject uncorrectable errors and large quantum
computations would drift to radically wrong answers. They do not. **The fidelity of quantum
computation is a standing experimental verdict that the quantum logical description has no missing
causal ingredient.**

QLF *strengthens* this rather than merely asserting it: **gravity is emergent from ZFA**, not
fundamental ([`QLF_GravityFromDelay`](lean/QLF_GravityFromDelay.lean),
[`QLF_EinsteinEquations`](lean/QLF_EinsteinEquations.lean)), so it **cannot** be a hidden influence
corrupting the quantum description — it is *made of the same closures*, downstream of the very events
it would supposedly disturb. There is no separate gravitational substrate to leak in. So QLF doesn't
postulate completeness; it **explains** why quantum computation is immune to gravitational (or any
sub-quantum) corruption: there is nothing else of which reality is made.

This is the precise sense in which QLF **supersedes** legacy physics — not by discarding it, but by
being the complete foundation it *emerges from*, exactly as general relativity superseded Newton
(which survives as the low-energy rendering). Legacy physics is the **rendering**; the ZFA substrate
is **what there is**. Consequently the items this document and [`Open_Problems.md`](Open_Problems.md)
mark "open" are **calculational depth — values awaiting derivation, requiring deeper investigation —
not gaps where the theory could be wrong.** The ontology is closed. The one genuine *external* limit
is the continuum/choice boundary of the Millennium program, and that is **ZFC's** proven defect
([`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md)), not QLF's.

---

## 3c. Supersymmetry and the hierarchy problem — neither is required

**Low-energy SUSY is not required and not predicted — QLF favours the LHC null.** In QLF the supercharge is not an operator relating new *particles* to old ones; it is the **half-spin shift** — adjoin one Hermitian twist pair — and boson↔fermion is the **even/odd parity of the closure** (`supercharge_flips_statistics`, `supercharge_boson_to_fermion`; `{Q,Q†}=2P` is two half-spins closing one spacetime event, `two_supercharges_close_event`, [`lean/QLF_Supersymmetry.lean`](lean/QLF_Supersymmetry.lean), [`SUSY_QLF.md`](SUSY_QLF.md)). The symmetry is realized **without a doubled spectrum** — `Q` shifts the *same* closure, it does not mint a superpartner — so there are no squarks or sleptons, and the decades of null LHC superpartner searches are the *expected* result, not a puzzle. (The full super-Poincaré algebra and any high-scale structure stay open, `supersymmetry_in_progress`.)

**And the usual reason for expecting TeV SUSY — the hierarchy problem — is dissolved, not solved.** The hierarchy problem is the worry that the Higgs mass, a *continuum* parameter, receives huge radiative corrections that must be finely cancelled to sit far below the Planck scale — so a symmetry (SUSY) is invoked to *protect* it. QLF removes the premise: **there is no large ratio of fundamental scales that needs protecting**, because the continuum mass scales are not fundamental inputs at all — they are **large-number renderings of discrete ZFA structure**. The Planck/proton ratio is `ln R_p = 14π`, dimensional transmutation from the single integer `b₀ = 7` (§1), not a fine-tuned cancellation; mass is gauge-fold *depth* (`m = 1/R`), an integer of closure with no continuum self-energy to diverge (the UV-finiteness of [`TheContinuum.md`](TheContinuum.md)). A quantity that was never a fundamental continuum input has nothing to protect. So any SUSY-like structure would live only at the **continuum-rendering layer**, never as a new particle spectrum at the TeV scale.

---

## 4. Beyond the SM **and** GR

- **Gravity is emergent**, not a fundamental force — and QLF reproduces GR's first triumph: **Mercury's perihelion advance ≈ 42.98″/century** to 0.03% (`mercury_perihelion_substrate_summary`, [`lean/QLF_MercuryPerihelion.lean`](lean/QLF_MercuryPerihelion.lean)), with `G` and `c` substrate-derived.
- **The cosmological constant** — `Ω_Λ = log 2` (1.2%) closing the **10¹²² "vacuum catastrophe,"** QFT+GR's worst prediction (`only_2_gauge_matches_observed_Omega_Lambda`, [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean)). This is the single most beyond-SM-and-GR result in the corpus.

---

## 5. What QLF does **not** do (the gaps, plainly)

- It does **not** derive most of the SM's *values*: the quark-mass values, the CKM/PMNS angles, the weak/strong coupling values, and the Higgs mass and VEV are all 🔵 open (§1) — the **Yukawa value sector**. The *mechanisms*, however, are machine-anchored: the gauge force as holonomy (`QLF_GaugeHolonomy`), confinement (`QLF_Confinement`), mass = gauge-fold delay + custodial `ρ=1` (`QLF_HiggsMechanism`), mixing unitarity (`QLF_CKM`/`QLF_PMNS`), and the Majorana neutrino mass (`QLF_NeutrinoMass`). (`θ_QCD` is ✅ derived as 0 without an axion.)
- The lepton sector is **constrained, not closed**: `Q=2/3` is derived, but the scale and the Koide angle are inputs ([`Weak_Force.md`](Weak_Force.md) §5c — the angle is `δ = 0.222222047`; `2/9` is a flagged candidate hypothesis, not a derivation).
- α matches at **0.026%**, not exactly — the residual (Schwinger-scale) is open.
- The beyond-SM predictions (§3) **cannot be proved** by theory alone — the Majorana / `0νββ` prediction (though `neutrino_majorana` is machine-verified given the `^v` assignment) awaits an experimental `0νββ` observation; dark-matter-as-denser-logic now makes a **sharp, blind, parameter-free** prediction — the SPARC Radial Acceleration Relation reproduced at the observational floor with `a₀ = cH₀/2π` derived ([`SPARC.md`](SPARC.md)).
- The Riemann-hypothesis link is an **axiom** (`spectral_hilbert_polya`), not a proof.

---

## 6. The honest scorecard

| | count | nature |
|---|---|---|
| SM parameters QLF **derives** (machine-verified) | 1 coupling (α) + `θ̄=0` (strong-CP, no axion) | retrodiction, but the *derivation* is proved |
| Beyond-SM/GR quantities derived | Ω_Λ, Λ, Mercury perihelion, m_p/m_e | retrodiction; several Lean-anchored |
| Falsifiable predictions | 3 sharp (Majorana ν₁, `m_ββ ≈ 0.25 meV`, normal ordering, `neutrino_majorana` / `one_axis_majorana`; **no cosmological drift of α(0)**, `no_cosmological_drift_of_alpha`; **the dark-matter RAR** — blind, parameter-free on 147 SPARC galaxies, [`SPARC.md`](SPARC.md)) + 1 soft (sterile ν) | untested; physics, not proof |
| SM parameters left **open** | the large majority (quarks, CKM, couplings, Higgs numbers, ν masses) | 🔵 |

**Bottom line.** Two senses of "theory of everything" must be kept apart — but they are **not** in
tension, because one is about *what reality is* and the other about *how far we have calculated*:

- **As a foundational *ontology*** — one selection principle (ZFA on the computational possibility
  space) from which the structure of physics emerges — QLF **is** a complete TOE-scope framework. The
  claim "reality is the ZFA-balanced subset of computation" is a TOE-class claim about *what
  everything is*, and §3b makes it sharp: the quantum logical description is **complete** (no hidden
  variables; quantum computation is the experimental verdict; gravity is emergent so cannot be a
  hidden influence). QLF **supersedes** legacy physics the way GR superseded Newton — by being the
  foundation it renders from ([`Active_Inference_Mathematics.md`](Active_Inference_Mathematics.md),
  [`VacuumEnergy.md`](VacuumEnergy.md) §6).
- **As a parameter-complete *derivation*** — having *computed* every SM+gravity constant from the
  substrate — QLF is **not yet finished**, and this document is the honest ledger of the distance: it
  derives α, Koide → m_τ, `θ̄=0`, `Ω_Λ`, m_p/m_e, Mercury, … (§§1–4), and the rest await derivation.
  But "await derivation" is **calculational depth — deeper investigation, normal-science unpacking —
  not a hole where the theory could be wrong.** The ontology is closed; what is open is *which numbers
  we have computed*, not *whether the substrate is the right one*. (The sole genuine *external* limit
  is the continuum/choice boundary of the Millennium program — **ZFC's** proven defect, not QLF's.)

So the precise status is **a TOE-scope ontology with a partial, principled-not-fitted derivation attached** — strictly more than reproducing the SM (which derives *zero* of its parameters), strictly less than deriving it. Calling it a *finished* TOE would be the overclaim; calling it *only* an SM-fit would miss the ontological scope. The line to never blur is the second sense: the open parameters in §1 are open. The clean falsifiable predictions are Majorana / `0νββ` and no `α(0)` drift (§3).

**Two flaws that disqualify competing TOE *ontologies* — and that QLF avoids by construction.** A foundational TOE must not install, as a *fundamental* law, anything that is in fact an emergent present-local accounting identity. Two such mistakes are common:

- **Axiomatizing reversibility.** Reversibility is a real symmetry of the *laws* (the dagger involution; every closure `H = H†`) but not of the *universe* — a TOE that takes it as fundamental omits the irreversible closure, where time, definiteness, and information come from, and must then bolt on a Past Hypothesis, a collapse postulate, or coarse-graining-by-ignorance. Purely-unitary "no collapse" (Everett), the block universe, and deterministic reversible-CA underpinnings ('t Hooft) are the casualties. See [`Reversibility.md`](Reversibility.md) §6.
- **Axiomatizing global energy conservation.** Energy conservation is a real *present-local* balance (Noether's time-translation symmetry, exact only for the signed-count currents) but not a fundamental global law — each closure *creates* energy and lends half to the future (the cosmic expansion / dark energy). A TOE built on a fixed total energy cannot produce a genuinely expanding universe without adding dark energy by hand — string theory's de Sitter / **swampland** difficulty is exactly this. See [`Conservation.md`](Conservation.md) §2b, [`StringTheory.md`](StringTheory.md) §3.

QLF takes neither as an axiom: reversibility and energy conservation are *outputs* of the ZFA closure (its present-local balance), and the arrow of time, the second law, and dark energy are the *same* forward, energy-creating, bit-synthesizing direction of that closure. The fundamental thing is the closure; a TOE that foundationalizes one of its emergent faces has mistaken a consequence for a cause.

---

## 7. References

- [`Open_Problems.md`](Open_Problems.md) — the open-work registry this complements.
- [`Experimental_Consistency.md`](Experimental_Consistency.md) §10 — the falsifiability section; the Majorana / `0νββ` commitment.
- [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) — the three machine-verified gauge algebras.
- [`Weak_Force.md`](Weak_Force.md) §5 — Koide `Q=2/3`, `m_τ`, the Koide angle.
- [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md), [`DarkMatter.md`](DarkMatter.md) — the beyond-SM predictions.
- [`SUSY_QLF.md`](SUSY_QLF.md) — supersymmetry as the half-spin shift; no doubled spectrum, and the hierarchy problem dissolved (§3c).
- [`Cosmological_Constant.md`](Cosmological_Constant.md) — `Ω_Λ = log 2`, the vacuum catastrophe.
- [`CP-Violation-and-Chirality.md`](CP-Violation-and-Chirality.md) §4a–4b — strong-CP `θ̄=0` without an axion, and the Sakharov baryogenesis conditions.
- [`Alpha.md`](Alpha.md) — the canonical α doc: first-principles derivation, the IR / 3-D-rendered scale, the dimension-flow running, the no-cosmological-drift prediction, and the 4D/5D over-determination.
- Lean anchors: `alpha_QLF_eq`, `alpha_at_dim_closed_form`, `no_cosmological_drift_of_alpha`, `koide_two_thirds`, `Omega_Lambda_QLF`, `mass_ratio_QLF_eq`, `mercury_perihelion_substrate_summary`, `weak_isospin_su2`, `trace_commutator_zero`, `neutrino_majorana`, `theta_zero_on_closure`.
