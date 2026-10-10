# The 2026 Discoveries, Read on the Substrate

What QLF already said about each notable physics result of 2026, what can now be proved about it, and
where a result is a test that QLF could fail. The proofs are in
[`lean/QLF_Discoveries2026.lean`](lean/QLF_Discoveries2026.lean) (no axioms). Status labels follow
[`ScientificApproach.md`](ScientificApproach.md) §3.

The list started from Nap Theory's video *The Most Insane Physics Discoveries Of 2026 (That You Haven't
Heard Of)*. Its transcript could not be retrieved, so the topics below come from the primary sources
cited in each section. A topic from the video that is missing here belongs in §13.

## At a glance

| # | Result (2026) | QLF's prior view | What is new here | Status |
|---|---|---|---|---|
| 1 | Baryon number carried by a gluon junction (STAR, *Science*) | Baryon number is a 3-axis winding ([`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean)) | The windowed winding reads the neutron as `B = 0`. Read on the junction, `B = 1` and no flavour change can move it | **proved**, and a correction |
| 2 | Doubly charmed baryons `Ξcc⁺`, `Ωcc⁺` (LHCb) | `Q = (2/3)N − n_g` ([`QLF_QuarkSignature`](lean/QLF_QuarkSignature.lean)) | The charge ladder `3Q = 6 − 3k` with `B = 1` on every rung; charge is generation-blind | **proved** |
| 3 | Entangled Z pairs from Higgs decay (ATLAS) | Entanglement is a shared closure ([`ER_EPR_QLF`](lean/ER_EPR_QLF.lean)) | Two histories close together iff their action vectors are opposite on every axis; an open child forces an open partner | **proved** |
| 4 | Dissipationless 1-D transport (TU Wien) | Conservative logic is free ([`QLF_Fredkin`](lean/QLF_Fredkin.lean)) | Elastic 1-D collisions are permutations: the whole velocity distribution is conserved | **proved** |
| 5 | Altermagnetism in thin, tunable films | Handedness and count balance ([`QLF_Handedness`](lean/QLF_Handedness.lean)) | The d-wave splitting is the only one that is inversion-even and odd under the axis swap | **proved** |
| 6 | Quantum Shapiro steps in cold atoms | Vorticity quantised to `±1` per cell ([`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md)) | `n` vortex–antivortex pairs close for every `n`; the step index is a closure count | **proved** (structural) |
| 7 | IceCube and the 2026 Nobel Prize (Halzen) | Neutrino is Majorana; mixing angles open ([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md)) | μ–τ symmetric mixing sends a `1:2:0` source to exactly `1:1:1` | **proved**, conditional on μ–τ symmetry |
| 8 | A single unexplained event at LZ | No dark-matter particle ([`DarkMatter.md`](DarkMatter.md)) | Kill condition stated | **test pending** |
| 9 | `B → Kπμμ` tension, "charming penguins" (LHCb) | No new particles; hadronic sector open | Prediction: the tension resolves inside the Standard Model | **conjecture**, falsifiable |
| 10 | Vacuum-enhanced superconductivity in a cavity (NbSe₂) | The Casimir effect as a finite census ([`QLF_Casimir`](lean/QLF_Casimir.lean)) | A reading, and the disputed point it has to face | **open bridge** |
| 11 | A 40-year-old CFT energy ladder measured (Caltech) | Ising exponents tested ([`ising_exponent_test.py`](ising_exponent_test.py)) | Where QLF would have to reproduce it | **open** |
| 12 | Pair density waves in UTe₂ | Cooper pairs as shared closures ([`Carbon_Superconductivity.md`](Carbon_Superconductivity.md)) | A reading only | **open** |

## 1. The baryon junction — a correction to QLF, and STAR agrees with it

**The result.** STAR at RHIC tracked baryon number and electric charge through collisions. Baryon
number reaches mid-rapidity about twice as often as the stopped valence quarks predict. The paper
argues that baryon number is carried by the Y-shaped gluon junction joining the three quarks, the
Rossi–Veneziano picture, not by the quarks themselves ([*Science* 393, 727 (2026)][star]).

**What QLF had.** [`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean) defines baryon number as a signed
linking over every 3-twist window: `+1` for a window spanning `x, y, z` cyclically, `−1`
anticyclically, `0` otherwise. A gauge twist has no axis, so any window touching one counts `0`.

**What we found.** QLF's own neutron word, `udd = >^+/+` from
[`QLF_QuarkSignature.nucleon_charges`](lean/QLF_QuarkSignature.lean), has windowed baryon number
**0** (`windowed_neutron_zero`). Each down quark's `+` breaks the windows on either side of it. The
windowed definition is therefore not a baryon number for the full quark signature. It is one only for
words with no interleaved gauge twists, which is how it was calibrated (`baryon_proton` uses `>^/`).

**The fix, and what it proves.** Read the winding on the **junction**, the spatial projection of the
word with every gauge twist removed:

- `junction_nucleons`: proton and neutron both have `B = 1`.
- `junction_insert_gauge`: inserting a gauge twist anywhere leaves junction baryon number unchanged,
  for every word. A W emission or a `u ↔ d` conversion cannot move it. `junction_beta_decay` is the
  instance `n → p`.
- `junction_antiproton`: the antibaryon has `B = −1`, so dagger-oddness survives the projection.

So in QLF baryon number lives on the three-axis skeleton, and the flavour and charge twists hang off it
without touching it. That is the substrate form of STAR's claim, which QLF reached independently: the
carrier is the junction, not the valence flavours. A spatial twist carries both colour axis and
direction, so the junction is not "glue without quarks". It is the colour structure with flavour
stripped off, the part of the word that `QLF_ColourFlux` already treats as colour.

**What it does not settle.** STAR's evidence is a stopping excess in collisions. QLF has no transport
model to predict the factor of two, so this is agreement on the carrier, not on the number.

## 2. Doubly charmed baryons — the charge is blind to generation

**The result.** LHCb's Run 3 detector observed `Ξcc⁺ (ccd)` above 7σ, its first new particle
([arXiv:2603.28456][xicc]). In September it reported `Ωcc⁺ (ccs)` at 8.7σ ([arXiv:2609.21921][omcc]).

**What QLF proves.** The §30 signature gives charge and colour, not generation. A charm quark has the
up quark's word, and generation lives in the fold depth ([`QLF_QuarkMass`](lean/QLF_QuarkMass.lean)).
With one up-type quark per colour axis and `k` down-type conversions:

- `baryon_charge_ladder`: `3Q = 6 − 3k` for every `k`. So `Ξcc⁺⁺` and `Δ⁺⁺` have `+2`; `Ξcc⁺`, `Ωcc⁺`
  and `p` have `+1`; `n` has `0`; `Ω⁻` and `Δ⁻` have `−1`.
- `baryon_ladder_junction`: every rung is one baryon on the junction (from §1).
- `doubly_charmed`: the LHCb states' charges and baryon numbers, decided.

This is a consistency check that QLF passes, not a prediction. Any quark model gets these charges. What
it shows is that the 2026 states need nothing the signature lacks, and that the §1 correction is what
gives them `B = 1`.

## 3. Entangled Z bosons — a shared closure forces anti-correlation

**The result.** ATLAS measured spin correlations in `H → ZZ* → 4ℓ` and rejected a non-entangled
alternative at about 4.7σ: the first entanglement measured between massive vector bosons
([arXiv:2603.26463][atlas]).

**What QLF had.** [`ER_EPR_QLF`](lean/ER_EPR_QLF.lean): two histories are entangled iff their joint
history closes (`SharedClosure`).

**What QLF proves.**

- `countBalanced_append_iff`: two histories close together iff their signed action vectors are
  **exactly opposite on every axis**. That is perfect anti-correlation, which a spin-0 parent imposes
  on its products.
- `forced_sharing`: if the parent closes and one child does not close by itself, the other cannot
  either. The closure is irreducibly shared, not a product of two closures.
- `vector_pair_shared`: an explicit witness with two open vector words that close only together.

**Scope.** The witness words are illustrative. QLF has no derived Z-boson word, and the theorem says
nothing about the measured *degree* of entanglement (the 4.7σ figure is a statistic of a specific
non-entangled alternative). What it says is that a closed parent leaves its products no way to be
separately closed, so "the Higgs's Z bosons are entangled" is structural in QLF, not a surprise.

## 4. A quantum Newton's cradle — conservative logic in mechanical form

**The result.** TU Wien confined rubidium atoms to a one-dimensional line. Energy and mass flowed
through it with diffusion practically absent, even after many collisions ([TU Wien][tuwien]).

**What QLF had.** [`QLF_Fredkin`](lean/QLF_Fredkin.lean): a conservative gate is a permutation, so it
preserves the twist multiset and costs nothing. Only retained garbage costs `log 2` per bit.

**What QLF proves.** An equal-mass elastic collision in one dimension exchanges the two velocities
(momentum and energy conservation leave no other outcome). Modelled as `collide`:

- `collide_perm`, `run_perm`: any sequence of collisions is a permutation of the initial velocities.
- `run_count`: **the whole velocity distribution is invariant.** The gas cannot relax to a thermal
  distribution it did not start in.
- `run_conserved`: every additive charge `Σ f(vᵢ)` is conserved, including momentum, energy and every
  higher power, so there are infinitely many conservation laws, the signature of integrability.
- `collide_involutive`: each collision undoes itself. Nothing is merged, so by the Fredkin ledger
  nothing is paid, and there is no dissipation.

**Scope.** The real gas is quantum (Lieb–Liniger) and only near-integrable. The theorem is the
classical skeleton: it explains why diffusion vanishes and why thermalisation needs something to break
the permutation structure (unequal masses, a transverse degree of freedom, three-body collisions).
The bound on how fast weak breaking thermalises is not derived here.

## 5. Altermagnetism — the d-wave pattern is forced

**The result.** Several 2026 groups reported altermagnetic spin splitting in thin and tunable
materials. Examples are tuned RuO₂ (Minnesota, *PNAS*) and layered Co₁/₄TaSe₂ (UCF). An altermagnet has
zero net magnetisation, like an antiferromagnet, but its bands are spin-split, like a ferromagnet's
([UMN][umn], [APS 2026][aps-alt]).

**What QLF proves.** Put the splitting on the twist alphabet as `altSplit` (`+1` along `x`, `−1` along
`y`, `0` elsewhere):

- `alt_compensated`, `alt_nonzero`: zero net moment, yet a nonzero split.
- `alt_inversion_even`: unchanged under `k → −k` (conjugation keeps the axis).
- `alt_swap_odd`: reversed by the `x ↔ y` swap, the 90° rotation that, combined with a spin flip, is
  an altermagnet's defining symmetry.
- `dwave_forced`: **any** splitting that is inversion-even and odd under the swap is a multiple of
  `altSplit`. The swap alone forces the off-plane and gauge directions to zero. So given the symmetry,
  the d-wave pattern is the only option, not one choice among several.
- `uniform_not_swap_odd`: a ferromagnetic (uniform) splitting cannot carry the symmetry.

This is QLF's count-balance versus order distinction on a magnet. Count balance (zero net moment) does
not mean nothing is there: the structure lives in *how* the balance is arranged across axes.

## 6. Quantum Shapiro steps — the step index counts closures

**The result.** Two teams (LENS/Florence with Fermi gases, Kaiserslautern with a BEC) drove a moving
barrier through a cold-atom Josephson junction and saw quantised Shapiro steps. In the Florence account,
each step corresponds to a definite number of vortex–antivortex pairs nucleated per drive cycle
([Physics World][shapiro]).

**What QLF proves.** A vortex is the closed plaquette `^<v>` and an antivortex its conjugate.

- `pairs_balanced`: `n` pairs form a count-balanced (closed) history **for every `n`**: zero net
  circulation per cycle, however high the step.
- `pairs_length`: the step index is recoverable as a count, `n` pairs being `8n` twists.

The physics is that the chemical-potential step `Δμ = n·hν` is quantised because `n` counts closures.
The proof is structural and modest: it shows the pair picture is consistent at every step, not that the
drive selects step `n`.

## 7. IceCube and the 2026 Nobel Prize — what μ–τ symmetry would buy

**The result.** Francis Halzen received the 2026 Nobel Prize for IceCube and its discovery of
high-energy neutrinos of astrophysical origin ([Nobel press release][nobel]). IceCube's flavour
composition at Earth is consistent with `1 : 1 : 1`.

**What QLF has.** The neutrino is Majorana ([`QLF_Majorana`](lean/QLF_Majorana.lean)), and there are
exactly three angles and one CP phase. The angle **values** are open
([`Standard_Model.md`](Standard_Model.md) §4.2).

**What QLF proves.** `flavour_ratio_mu_tau`: for **any** doubly stochastic weights `w α i = |U_αi|²`
whose μ and τ rows agree, the oscillation-averaged transfer carries a pion-decay source `1 : 2 : 0`
to **exactly** `1 : 1 : 1`. No angle values enter; only the μ–τ equality does.

**What it means for QLF.** The theorem states exactly what a derivation of μ–τ symmetry would buy:
exact `1 : 1 : 1` at the source-to-Earth level, with departures at the size of `θ₂₃ − 45°` and `θ₁₃`.
QLF reads generations as the three spatial axes ([`QLF_Generations`](lean/QLF_Generations.lean)),
and an axis-swap symmetry between two of them would be μ–τ symmetry, but that is a conjecture. With the
measured angles, μ–τ symmetry is broken at a few percent, below IceCube's present flavour resolution.

## 8. LZ's single event — a test QLF could fail

**The result.** On 1 September 2026 LUX-ZEPLIN reported one nuclear-recoil event that known
backgrounds explain poorly. Reports put it near 2.6σ, implying a WIMP mass of at least about
200 GeV if real. The collaboration was explicit that one event is not a discovery ([Berkeley Lab][lz]).

**QLF's position.** [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §6 lists *a fundamental
dark-matter particle* as **predicted absent**. Dark matter is denser logic near masses, and the radial
acceleration relation is derived and blind-tested on SPARC ([`DarkMatter.md`](DarkMatter.md)).

**Kill condition, stated before the data.** If LZ, XENONnT or PandaX confirm a WIMP-like recoil signal
at ≥ 5σ, with a spectrum and rate that a single dark-matter mass fits across detectors, the "no
dark-matter particle" null is **falsified**. QLF's derived RAR would survive only as a description of
the baryonic sector beside a real particle. One event at 2.6σ moves nothing. It is recorded here so the
outcome cannot be rationalised after the fact.

## 9. The B-meson tension — a prediction of no new particle

**The result.** An analysis of `B → Kπμμ` disagrees with the Standard Model, and the tension is tied
to "charming penguins": charm-loop contributions that are hard to compute ([Phys.org][penguin]).

**QLF's position, as a falsifiable null.** QLF predicts no supersymmetric partners, no axion and no
fundamental dark-matter particle ([`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §6). The same
economy predicts no Z′ or leptoquark behind flavour anomalies. CKM unitarity is closure
([`QLF_CKM`](lean/QLF_CKM.lean)), and the hadronic sector is QLF's open frontier, the same frontier as
muon `g − 2` ([`g_minus_2.md`](g_minus_2.md)). **Prediction:** the tension resolves within the
Standard Model as the charm-loop contribution is pinned down. **Kill condition:** a 5σ deviation in a
clean channel (one with negligible charm-loop contamination, such as `B_s → μμ` or lepton-universality
ratios) that a new mediator fits.

## 10. Vacuum-enhanced superconductivity — a reading, and the disputed point

**The result.** A USTC team put six-layer NbSe₂ in a terahertz "dark" cavity and saw `T_c` rise by up to
5.4%, with a resonant enhancement when the cavity mode matched the superconducting fluctuations
([*Nature* 2026][nbse2]). A theory preprint argues that within minimal cavity electrodynamics, vacuum
fluctuations in a passive cavity can only *suppress* `T_c` ([arXiv:2608.14784][nogo]).

**The QLF reading.** [`QLF_Casimir`](lean/QLF_Casimir.lean) treats a cavity as a finite census:
the walls change which closures exist, and the force is a finite difference of censuses. In QLF's terms
a cavity changes how many ways a closure can happen, so it can change which closure happens first.
Whether that raises or lowers `T_c` is a sign the census would have to compute. The no-go preprint says
the minimal-coupling sign is negative, so a QLF account of the enhancement would have to come from
outside minimal coupling, where the experiment's own resonance points. Nothing is derived here. The open
bridge is the cavity-restricted pairing census, and its sign is the test.

## 11. The conformal energy ladder — where QLF would have to reproduce it

**The result.** Caltech's Endres group used chains of strontium Rydberg atoms as a quantum simulator
and measured the energy ladders of two conformal field theories. Theory had predicted the rungs' fixed
ratios about 40 years earlier, but no experiment had measured them ([ScienceDaily][cft]).

**QLF's position.** QLF claims that continuum field theory is a rendering of the finite census
([`TheContinuum.md`](TheContinuum.md)). A CFT's scaling dimensions are universal numbers, so the
rendering claim implies they are census data. The Ising exponent test
([`ising_exponent_test.py`](ising_exponent_test.py)) is the nearest existing work. The measured ratios
are now a target: a closure census of the critical chain should give the Ising tower (`0, 1/8, 1`) in
the stated ratios. Until it does, this is **open**.

## 12. Pair density waves in UTe₂ — a reading only

A July 2026 *PNAS* paper finds charge-density-wave peaks in UTe₂ that track a pair density wave coupled to
uniform superconductivity ([arXiv:2603.08688][pdw]), while a hard X-ray study sees no bulk CDW
signature ([NIST][nist]). In QLF a Cooper pair is a shared closure
([`Carbon_Superconductivity.md`](Carbon_Superconductivity.md)), and a pair density wave is a pair whose
closure balances over a wavelength rather than at each site. That is a reading, not a result, and the
experimental picture is itself unsettled.

## 13. Not yet covered

Topics from the Nap Theory video, or from later 2026 results, that are missing above. Add them here
with a source before writing a reading.

## Sources

- STAR Collaboration, "Tracking the baryon number with nuclear collisions", *Science* 393, 727 (2026) — [Rice University news][star]
- LHCb, "Observation of the doubly charmed baryon Ξcc⁺ with the LHCb Run 3 detector" — [arXiv:2603.28456][xicc]; Ωcc⁺ — [arXiv:2609.21921][omcc]
- ATLAS, Z-boson pair entanglement in Higgs decays — [arXiv:2603.26463][atlas]
- TU Wien, "When quantum gases refuse to follow the rules" — [press release][tuwien]
- Altermagnetism: [University of Minnesota][umn]; [APS March Meeting 2026][aps-alt]
- Shapiro steps in ultracold gases — [Physics World][shapiro]
- Nobel Prize in Physics 2026 — [press release][nobel]
- LZ — [Berkeley Lab news, 1 Sept 2026][lz]
- `B → Kπμμ` tension — [Phys.org][penguin]
- Vacuum-enhanced superconductivity in NbSe₂ — [*Nature*][nbse2]; no-go preprint — [arXiv:2608.14784][nogo]
- Conformal ladder — [ScienceDaily][cft]
- UTe₂ pair density wave — [arXiv:2603.08688][pdw]; bulk X-ray null — [NIST][nist]

[star]: https://news.rice.edu/news/2026/scientists-uncover-new-clue-how-protons-maintain-their-identity
[xicc]: https://arxiv.org/abs/2603.28456
[omcc]: https://arxiv.org/abs/2609.21921
[atlas]: https://arxiv.org/abs/2603.26463
[tuwien]: https://www.tuwien.at/en/tu-wien/news/press-releases/news/wenn-quantengase-sich-nicht-an-die-regeln-halten
[umn]: https://cse.umn.edu/college/news/tuning-nonmagnetic-material-reveals-hidden-magnetic-state
[aps-alt]: https://meetings-archive.aps.org/smt/2026/mar-p38/7/
[shapiro]: https://physicsworld.com/a/shapiro-steps-spotted-in-ultracold-bosonic-and-fermionic-gases/
[nobel]: https://www.nobelprize.org/prizes/physics/2026/press-release/
[lz]: https://newscenter.lbl.gov/2026/09/01/lz-sees-surprising-result-in-search-for-dark-matter/
[penguin]: https://phys.org/news/2026-04-lhc-decay-anomaly-reveals-standard.html
[nbse2]: https://www.nature.com/articles/s41586-026-11037-x
[nogo]: https://arxiv.org/abs/2608.14784
[cft]: https://www.sciencedaily.com/releases/2026/09/260928100554.htm
[pdw]: https://arxiv.org/abs/2603.08688
[nist]: https://www.nist.gov/node/1866511
