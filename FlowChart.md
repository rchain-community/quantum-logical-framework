# QLF Flow Chart — a visual map of the framework

> **This is a navigation map of the [Quantum Logical Framework (QLF)](README.md)** — one substrate, five
> families, twelve domains, and the documents that derive each. The **Jump to** and **Open** links are the
> navigation; the visual diagrams live in the rendered version linked below.

The taxonomy: **one substrate → five domain families → twelve domains → the individual results.**


> **The diagrams don't render reliably on GitHub** (a known GitHub Mermaid/dark-theme issue), so this page is the text index. For the **rendered, clickable diagrams** and a **printable PDF** (with internal + external links), open the live version on GitHub Pages: **[rchain-community.github.io/quantum-logical-framework/FlowChart.html](https://rchain-community.github.io/quantum-logical-framework/FlowChart.html)** (or clone/pull and open the local `FlowChart.html`). Regenerate with `python3 tools/build_flowchart_html.py`.

---

## Master map — the substrate and its twelve domains


**Jump to:** [1 Space, time and the continuum](#1-space-time-and-the-continuum) &middot; [2 The fundamental constants](#2-the-fundamental-constants) &middot; [3 Forces](#3-forces) &middot; [4 Atoms and QED](#4-atoms-and-qed) &middot; [5 Gravity and GR](#5-gravity-and-gr) &middot; [6 Cosmology and the dark sector](#6-cosmology-and-the-dark-sector) &middot; [7 Particles and the Standard Model](#7-particles-and-the-standard-model) &middot; [8 Quantum-gravity / TOE pillars](#8-quantum-gravity--toe-pillars) &middot; [9 The Millennium Prize program](#9-the-millennium-prize-program) &middot; [10 Beyond the SM](#10-beyond-the-sm) &middot; [11 Chemistry, molecules and folding](#11-chemistry-molecules-and-folding) &middot; [12 Quantum field theory and renormalization](#12-quantum-field-theory-and-renormalization)

The five families: **Foundations** (1-2, 12) &middot; **Matter and forces** (3, 4, 7) &middot; **Emergent matter** (11) &middot; **Gravity and the cosmos** (5-6) &middot; **Frontiers** (8-10).

**Emergent matter** is the one family that is not fundamental physics. The other four ask what the
substrate *is*; this one asks what it **assembles** once atoms exist — and it earns a family of its own
precisely because nothing in it is a new law. Chemistry, polymers and folding all run on the rule domains
3–4 already established, which is the claim being made by putting them on the map at all.

**Open:** [`README.md`](README.md)

Root reading: **everything derives from the 8-twist substrate under Zero Free Action** —
[`Philosophy.md`](Philosophy.md) (possibilist ontology, and §3a the *working method*: things happen every
way that closes, and what happens in the most ways happens first), [`WHITE_PAPER.md`](WHITE_PAPER.md).

**The method's limit, proven:** [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) — *a system with more
states can always break a finite closure*, so every restrictive law has a real, constructed exception and
no finite closure is final ([`QLF_LawOfExceptions`](lean/QLF_LawOfExceptions.lean)). Capacity turns out to
be an **excursion** budget ([`QLF_ClosureDepthLaw`](lean/QLF_ClosureDepthLaw.lean)), which is why the
proton dissolves at `T_c` and baryon number at `T_EW` while electric charge — whose proof carries no
capacity — has no exception at any scale. Corollary for everything below: **construction proves
possibility, not uniqueness.**

**An application of that same capacity machinery:** [`Mpemba.md`](Mpemba.md) — anomalous relaxation, where
relaxation time *is* the maximum excursion, giving a proven no-go (none for the imbalance measure), a
proven enabler (no scalar determines relaxation), and proven **instances** (more energy closing strictly
faster) — while the ensemble effect and the water phenomenon stay open
([`QLF_Mpemba`](lean/QLF_Mpemba.lean)).

**Foundational logic & mathematics:** the substrate's *logic* is **quantum logic** — argued as the correct
foundation of mathematics (bottom-up, sound vs. exploding) in [`Quantum_Logic_Foundations.md`](Quantum_Logic_Foundations.md),
with the minimal quantum logic `MO2` machine-verified on the substrate (orthomodular + non-distributive,
[`lean/QLF_QuantumLogic.lean`](lean/QLF_QuantumLogic.lean)); and ordinary mathematics *emerging* from it (ℕ,
the ring, `μ₄`, su(2)/su(3), the continuum as completion) in the companion [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md).
The **category-theoretic** shape — the causal-set base category, ZFA as an equalizer, the capacity-horizon
**bifibration** whose free prime-factorisation *forces* self-similarity (and closes the log-periodic channel,
so the α-residual weight `w = 1/2` is structural), the Tannakian/anabelian layer, RhoQuCalc as a dagger SMC —
is collected in [`Category_Theory_QLF.md`](Category_Theory_QLF.md) (a description, not an axiom).
**Truth is objective across observers, and in two ways** ([`lean/QLF_MultiObserver.lean`](lean/QLF_MultiObserver.lean),
no axioms): whether a history closes, and the phase it carries, are the *same in every observer's frame*
(the discrete axis-permutation × gauge-swap group) — so two or more perspectives agree on the truth
(`observers_agree`), witnessed by two independent invariants, the count verdict and the Pauli scalar
(`truth_from_two_perspectives_in_two_ways`). The `/solve` "meeting of minds" consensus is a theorem.
**It from bit:** the unit of information is the two-valued **½-spin closure** — one bit (`log 2` for the spinor
alphabet `{+I,−I}`) vs *zero* for a single-valued vector `{+I}` — the `2π` double-valuedness reproven from the
explicit rotation matrices and grounding the spinor **Cartan** discovered in 1913 as the carrier of information
([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean), [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §Rung 5a).

**Harmonic-closure model:** reality and constructable truth are the *closing spectrum* of frequency-component closures — each frequency `f = 1/R` is one ZFA closure, i.e. a quantum-logical **computation** (a set of Feynman diagrams: path integral = generate, ZFA closure = the firebreak selecting the physical ones) ([`Frequency_Synchronization.md`](Frequency_Synchronization.md) §0).

---

## 1. Space, time, and the continuum


**Connectors:** *causal order* &rarr; Closure-reachability (pre-geometric causal s… &middot; *faithful 3-D render* &rarr; 3 spatial dimensions &middot; *logical latency* &rarr; Time = per-event Planck tick &middot; *synthesize* &rarr; Synthesized spacetime &middot; *RCA_0 floor* &rarr; No continuum / no Choice

**Open:** [`README.md`](README.md) · [`SpaceTime.md`](SpaceTime.md) · [`TheContinuum.md`](TheContinuum.md)

`3` is the minimal dimension that renders any relational structure faithfully — and it reappears
everywhere below ([`SpaceTime.md`](SpaceTime.md) §3a).

---

## 2. The fundamental constants

The `6 spatial + 2 gauge` split (the `3` axes) fixes a family of constants. **α is the flagship.**


**Connectors:** *N = 3^2* &rarr; alpha = 1/137 &middot; *spatial 3/8* &rarr; sin^2theta_W = 3/8 &middot; *gauge 2/8* &rarr; Omega_Lambda = log 2 &middot; *surface ~ r^2* &rarr; Newton 1/r^2 &middot; *l = 3* &rarr; nuclear magic numbers &middot; *6pi^5* &rarr; m_p/m_e = 6pi^5 &middot; *2/alpha* &rarr; m_pi/m_e = 274

**Open:** [`SpaceTime.md`](SpaceTime.md) · [`Alpha.md`](Alpha.md) · [`Weak_Force.md`](Weak_Force.md) · [`Cosmological_Constant.md`](Cosmological_Constant.md) · [`Gravity_From_Delay.md`](Gravity_From_Delay.md) · [`Magic_numbers.md`](Magic_numbers.md) · [`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md) · [`Pion_QLF.md`](Pion_QLF.md) · [`Genesis.md`](Genesis.md)

The census spectrum explorer [`Genesis.md`](Genesis.md) exercises the constants sector end-to-end: the exact `−p/2` census spectral exponent (Lean-anchored, `QLF_CensusWalk`), census → π, and `α⁻¹ = 128 + d²` (`d = 3 → 137`).

**α's full story** (derivation, IR/3-D scale, the running, the no-drift theorem, 4D/5D
over-determination): [`Alpha.md`](Alpha.md). **The `+0.036` residual is now healed to its honest shape**
([`Alpha_Residual.md`](Alpha_Residual.md) §9c): the bracket is two-sided and machine-checked both ends
(`137.01587 < α⁻¹ < 137.04813`), the equal-weight prediction **`137.032` is structural** (`w = ½` forced
by the free-monoid bifibration, not fitted), and `0.036` is **existence-proven** (reachable by a prime
resummation) with its **multiplicity open** — which resummation = the continuum vacuum-polarisation
running, the Standard Model's own frontier. Every substrate mechanism swing is closed; CODATA is an
estimate of the missing count, not a target.

---

## 3. Forces

One gauge-twist mechanism, seen from three projections of the 3-axis structure.


**Connectors:** *abelian* &rarr; U(1) - electromagnetism &middot; *non-abelian, chiral* &rarr; SU(2) - weak &middot; *colour, confined* &rarr; SU(3) - strong &middot; *+ one mass = scale* &rarr; dimensionless couplings &middot; *projection* &rarr; one force, three projections

**Open:** [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) · [`Electricity.md`](Electricity.md) · [`Weak_Force.md`](Weak_Force.md) · [`Alpha.md`](Alpha.md) · [`Forces_From_Alpha.md`](Forces_From_Alpha.md)

---

## 4. Atoms and QED

Everything here is **downstream of the derived α** ([`Alpha.md`](Alpha.md) §10).


**Connectors:** *1/2alpha^2m_e c^2* &rarr; Rydberg / Bohr &middot; *~ alpha^2* &rarr; Dirac fine structure &middot; *loop alpha* &rarr; Lamb shift &middot; *alpha/2pi* &rarr; g-2 &middot; *Z_0/2alpha* &rarr; von Klitzing R_K &middot; *~ alpha^4* &rarr; hyperfine / 21 cm

**Open:** [`Alpha.md`](Alpha.md) · [`Hydrogen.md`](Hydrogen.md) · [`Dirac_Correction.md`](Dirac_Correction.md) · [`Lamb_Shift.md`](Lamb_Shift.md) · [`g_minus_2.md`](g_minus_2.md) · [`Electricity.md`](Electricity.md) · [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md)

---

## 5. Gravity and GR


**Connectors:** *G = L_P^2c^3/hbar* &rarr; Newton's law + G &middot; *43''/century* &rarr; Mercury perihelion &middot; *deltaQ = T deltaS* &rarr; Einstein equations (equation of state) &middot; *causal order -> metric* &rarr; Curvature &middot; *spin-2, v = c* &rarr; Gravitational waves &middot; *Hilbert: delta S = 0 at balance* &rarr; Einstein equations

**Open:** [`Gravity_From_Delay.md`](Gravity_From_Delay.md) · [`Mercury_Perihelion.md`](Mercury_Perihelion.md) · [`Einstein_Equations.md`](Einstein_Equations.md) · [`Curvature.md`](Curvature.md) · [`Stationary_Action.md`](Stationary_Action.md)

---

## 6. Cosmology and the dark sector


**Connectors:** *gauge 2/8* &rarr; Omega_Lambda = log 2 closes the 10^122 catas… &middot; *high-V epoch* &rarr; Inflation (same field) &middot; *denser logic* &rarr; Dark matter (no particle) &middot; *residual w = -1* &rarr; Dark energy &middot; *event rate* &rarr; Age ~ 13.8 Gyr &middot; *freeze-out n/p* &rarr; ^4He fraction Y_p ~ 1/4 &middot; *measured values* &rarr; Concordant with LCDM data &middot; *interpretive pillars* &rarr; Divergent on LCDM interpretation &middot; *equation of state* &rarr; Thermodynamic gravity

**Open:** [`Cosmological_Constant.md`](Cosmological_Constant.md) · [`Curvature.md`](Curvature.md) · [`DarkMatter.md`](DarkMatter.md) · [`SPARC.md`](SPARC.md) · [`AgeOfUniverse.md`](AgeOfUniverse.md) · [`Fusion.md`](Fusion.md) · [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §3a

Dark matter is the closure-balance RAR, blind-tested parameter-free on 147 SPARC galaxies (`a₀ = cH₀/2π`, the `2π` derived; [`SPARC.md`](SPARC.md)). Dark energy is **dynamical** — `ρ_Λ ∝ H²` (Lean-anchored, `QLF_DynamicalDarkEnergy`) — so QLF sits in the *resolution-favorable* class of the **Hubble tension**, and its dark-matter fit votes local (`H₀ ≈ 72.9`); a reframe + vote, not a numeric resolution ([`DarkMatter.md`](DarkMatter.md) §5a).

**Convergence with accepted cosmology (the ledger, [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §3a).** QLF is **concordant with ΛCDM's observational core** — the hot Big Bang, CMB, BBN (`Y_p = 1/4`), the ≈13.8 Gyr age, `Ω_Λ = log 2 ≈ 0.69`, and the `w≈−1` accelerating expansion are all reproduced or left intact (*a Big-Bang-singularity alternative, not a hot-Big-Bang-observation alternative*). It **diverges only on ΛCDM's two interpretive pillars** — particle cold dark matter (→ the RAR/MOND reading above) and a static `Λ` (→ dynamical `ρ_Λ ∝ H²`), i.e. the open, contested questions. Its **deeper convergence** is with accepted **thermodynamic/emergent gravity** (Jacobson 1995, Bekenstein–Hawking, holography), from which it *derives* the Einstein `8πG` coefficient and `Λ = log 2` (`QLF_EinsteinEquations`).

---

## 7. Particles and the Standard Model


**Connectors:** *axis count* &rarr; 3 fermion generations &middot; *Q = 2/3* &rarr; Koide -> m_tau &middot; *3 angles + CP* &rarr; CKM / PMNS mixing &middot; *self-conjugate* &rarr; neutrino is Majorana &middot; *DeltaL = 2* &rarr; beta-decay / 0nubetabeta &middot; *one scale x ratios* &rarr; mass spectrum &middot; *m = 1/R fold delay* &rarr; mass (Higgs mechanism) &middot; *log 2 = one bit* &rarr; spin-1/2 = one bit (it from bit)

**Open:** [`Standard_Model.md`](Standard_Model.md) · [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) · [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md) · [`Spin_QLF.md`](Spin_QLF.md) · [`Higgs.md`](Higgs.md) · [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md)

**It from bit — information is the ½-spin closure.** The unit of information is the two-valued spinor closure: one bit (`log 2`) for `{+I,−I}` vs *zero* for a single-valued vector `{+I}` (a single-valued object cannot express a distinction). The `2π` double-valuedness is reproven from the explicit rotation matrices (`spinor_double_valued_vector_blind`: `+I` on the vector `SO(3)` rep, `−I` on the spin-½ `SU(2)` rep), grounding **Cartan**'s 1913 spinor as its carrier. Priority runs *abstraction → physical*: information **is** the distinction, the ½-spin closure its minimal realization ([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean), [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §Rung 5a).

---

## 8. Quantum-gravity / TOE pillars

QLF meets the three TOE-candidate programs — and reproduces their wins from the substrate.


**Connectors:** *j = 1/2 spin network* &rarr; Loop Quantum Gravity &middot; *C(2n,n) modes* &rarr; String theory &middot; *Q = half-spin shift* &rarr; Supersymmetry &middot; *closure floor mu^2=1/2* &rarr; Planck scale

**Open:** [`README.md`](README.md) · [`LQG_QLF.md`](LQG_QLF.md) · [`StringTheory.md`](StringTheory.md) · [`SUSY_QLF.md`](SUSY_QLF.md) · [`Planck_Scale.md`](Planck_Scale.md)

---

## 9. The Millennium Prize program

The thesis: *the continuum and Choice are mathematics' UV catastrophe* — each problem = a constructive
RCA₀ core + one explicit continuum/Choice boundary axiom.


**Connectors:** *critical line* &rarr; Riemann hypothesis &middot; *log 2 gap quantum* &rarr; Yang-Mills mass gap &middot; *rank = ord* &rarr; Birch-Swinnerton-Dyer &middot; *balanced => algebraic* &rarr; Hodge conjecture &middot; *generate != verify* &rarr; P vs NP &middot; *no blow-up* &rarr; Navier-Stokes

**Open:** [`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md) · [`Riemann-Conjecture-Proof.md`](Riemann-Conjecture-Proof.md) · [`YangMills_MassGap_QLF.md`](YangMills_MassGap_QLF.md) · [`BSD_QLF.md`](BSD_QLF.md) · [`Hodge_QLF.md`](Hodge_QLF.md) · [`P_vs_NP_QLF.md`](P_vs_NP_QLF.md) · [`NavierStokes_QLF.md`](NavierStokes_QLF.md)

Overview: [`Millennium.md`](Millennium.md).

---

## 10. Beyond the SM

What QLF derives that the SM treats as free input, and the falsifiable predictions it makes.


**Connectors:** *not free* &rarr; derived: alpha, Koide, theta-bar=0, Omega_La… &middot; *test now* &rarr; Majorana neutrino -> 0nubetabeta &middot; *scale-free by construction* &rarr; no cosmological drift of alpha(0) &middot; *soft* &rarr; dark matter is not a particle

**Open:** [`Beyond_Standard_Model.md`](Beyond_Standard_Model.md) · [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) · [`Alpha.md`](Alpha.md) · [`DarkMatter.md`](DarkMatter.md)

---

## 11. Chemistry, molecules and folding

The **Emergent matter** family: matter in bulk, from the same one rule — **a bond is a shared closure**,
no forces and no orbitals put in by hand ([`Chemistry.md`](Chemistry.md)). Nothing here is a new law;
everything is domains 3–4 assembled.


**Connectors:** *saturate* &rarr; shared closure = bond &middot; *H2O, CO2, graphite, rust* &rarr; molecules and carbon allotropes &middot; *Pauli holds them apart* &rarr; crystals and condensates &middot; *(v-2)/2 each* &rarr; closure count &middot; *b1 counts them* &rarr; double bond = ring = one closure &middot; *only k is free* &rarr; reaction class &middot; *free valence for water?* &rarr; hydrophobic / polar &middot; *valence 2 is neutral* &rarr; divalent chains &middot; *backbone carries none* &rarr; folding &middot; *only H-H pays* &rarr; folding

**Open:** [`Chemistry.md`](Chemistry.md) · [`Protein_Folding.md`](Protein_Folding.md) · [`lean/QLF_Unsaturation.lean`](lean/QLF_Unsaturation.lean) · [`lean/QLF_Folding.lean`](lean/QLF_Folding.lean) · [`hydrocarbon_census.py`](hydrocarbon_census.py) · [`protein_census.py`](protein_census.py)

**The counting layer.** An atom's valence is what it contributes to a molecule's **closure count**,
`(valence − 2)/2`, and the cycle rank `b₁ = E − V + 1` counts the closures the molecule carries. That
identification does three things at once: the textbook **degree of unsaturation** *is* that count (with
oxygen absent from the formula because its contribution is **zero**); a **ring and a double bond are one
phenomenon**, so `C₆H₁₂` is a single census class; and since a balanced reaction pins `V` and `E`, a
reaction's change in closure count **is** its change in molecule count — addition, elimination and
substitution are that one number ([`QLF_Unsaturation`](lean/QLF_Unsaturation.lean), no axioms).

**Up to folding.** Valence 2 is the neutral element of the count, which is why a divalent monomer makes a
**chain** and why the peptide bond — closure-neutral, 2 molecules in and 2 out — leaves a polypeptide
backbone carrying no closure of its own. So **every closure a folded chain has is a contact**, and a
contact is a ZFA closure in the literal sense: zero net displacement, count-balanced, Pauli-closed by the
keystone ([`QLF_Folding`](lean/QLF_Folding.lean)). The lattice-protein parity rule and the `log 2` contact
quantum follow; the **mirror no-go** — counting cannot select a handedness — bounds what the census can
ever answer ([`Protein_Folding.md`](Protein_Folding.md)).

---

## 12. Quantum field theory and renormalization

A **Foundations** domain: the continuum thesis of domains 1 and 9, applied to physics' most quantitative
framework. **QFT is the continuum limit of the substrate's discrete ZFA-event combinatorics** — it works
because the substrate really is doing sum-over-histories; its infinities appear only where that sum is
pushed to a *continuum* of modes ([`QFT_QLF.md`](QFT_QLF.md)).


**Connectors:** *grade by closure* &rarr; expansion order &middot; *IsDiagram order 0* &rarr; tree level = the closure census &middot; *single binding* &rarr; one loop = the 2/3pi coefficient &middot; *listen at capacity R* &rarr; renormalization = the capacity horizon &middot; *A_R+1 minus A_R* &rarr; counterterm, one finite term &middot; *Q(R) = Q0 2^R* &rarr; running: QED log = census octave count &middot; *prefix-free code* &rarr; Kraft bound: the series converges &middot; *no mode continuum* &rarr; Dyson divergence = continuum artefact

**Open:** [`QFT_QLF.md`](QFT_QLF.md) · [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) · [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean) · [`lean/QLF_FractalDiagram.lean`](lean/QLF_FractalDiagram.lean) · [`lean/QLF_VacuumPolarization.lean`](lean/QLF_VacuumPolarization.lean) · [`lean/QLF_RunningCouplings.lean`](lean/QLF_RunningCouplings.lean) · [`TheContinuum.md`](TheContinuum.md)

**The perturbation series is the possibility tree**, graded not by an external coupling but by **closure
structure** — continuation length, diagram order (`IsDiagram`, the closure↔Feynman-diagram map), or
closure depth ([`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md)). Two orders are proven against
QED: the **tree level is exactly the closure census** (`order_zero_iff_closure`), and the **one loop is the
`2/(3π)` vacuum-polarization coefficient** (`orderOneWeight_eq`), census-sourced and committed before
comparison ([`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean), [`QLF_VacuumPolarization`](lean/QLF_VacuumPolarization.lean)).

**Renormalization is Wilsonian and finite.** The regulator is the **capacity horizon** `R` — a listener of
capacity `R` hears the closures of depth `≤ R`; the counterterm for the step `R → R+1` is a single finite
term `A_{R+1} − A_R`, never a subtracted infinity; the running is `Q(R) = Q₀·2^R`, so the QED logarithm
**is** the census octave count ([`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean)).
And the substrate's series **converges absolutely** in its cylinder measure — `twist_kraft` plus
`|A| ≤ W` — so no Borel resummation, and the Dyson divergence is exposed as an artefact of the mode
continuum the substrate does not have ([`QLF_ExactRG`](lean/QLF_ExactRG.lean), the exact-RG recursion +
finiteness + convergence, no axioms). **The α residual is the worked calibration of the bridge line**
([`Alpha_Residual.md`](Alpha_Residual.md) §9c): QLF proves the census space (two-sided bracket) and proves
`w = ½ → 137.032` structural; the open piece is the *multiplicity* — which continuum resummation — not a
census-truncation rule. Existence proven, multiplicity open — the exact shape of every Millennium bridge,
run to convergence in a case with a measured answer. Every substrate mechanism swing is closed; the
turbulence swing produced a side-derivation (She–Léveque `C₀ = 2` from `/solve` axis-minimality).
**Contrast, once:** the rigorous continuum QFT (a Wightman /
Osterwalder–Schrader theory on ℝ⁴) is not constructed here — that step is the Yang–Mills boundary axiom of
domain 9. What the reformulation proves is that the discrete substrate the continuum is the *limit of*, plus
the one explicit crossing, carries QFT's empirical content.

---

## See also

- [`README.md`](README.md) · [`lean/README.md`](lean/README.md) — project overview + the full Lean module
  table.
- [`Open_Problems.md`](Open_Problems.md) — the honest gap registry (closed / principled-boundary / open).
- [`Beyond_Standard_Model.md`](Beyond_Standard_Model.md) — the derived / predicted / open scorecard.
- [`Alpha.md`](Alpha.md) — one result mapped end to end, as a worked example.
- [`Chemistry.md`](Chemistry.md) · [`Protein_Folding.md`](Protein_Folding.md) — domain 11 end to end: one
  rule (a bond is a shared closure) up through the closure count to a fold as a closure census.
- [`Fredkin_QLF.md`](Fredkin_QLF.md) — conservative logic on the substrate: Fredkin's conservation law
  **is** ZFA count balance ([`QLF_Fredkin`](lean/QLF_Fredkin.lean), no axioms), so a reversible computer
  runs **free** and only erasure is charged. Run it: [`fredkin_machine.html`](fredkin_machine.html).
