# The 2026 Discoveries, Read on the Substrate

What QLF already said about each notable physics result of 2026, what can now be proved about it, and
where a result is a test that QLF could fail. The proofs are in
[`lean/QLF_Discoveries2026.lean`](lean/QLF_Discoveries2026.lean) (no axioms). Status labels follow
[`ScientificApproach.md`](ScientificApproach.md) §3.

Part I takes the twelve segments of Nap Theory's video *The Most Insane Physics Discoveries Of 2026
(That You Haven't Heard Of)* in order. The experimental details in Part I are as the video reports
them; the papers it names are cited. Part II covers other 2026 results the video does not.

# Part I — The video's twelve discoveries

| # | Discovery (as reported) | QLF | Status |
|---|---|---|---|
| [V1](#v1) | Antiprotons moved by truck in a trap (BASE-STEP, CERN) | The antiparticle is the time-mirror: same mass, opposite charge and baryon number, for every word | **proved**; CPT null predicted |
| [V2](#v2) | Water as two interconverting liquids | Two closure inventories; the Mpemba stance gains a mechanism | **proved** (two-state density maximum); census to compute |
| [V3](#v3) | Vacuum `ss̄` twins surviving as spin-aligned `ΛΛ̄` (STAR) | A history joined to its mirror always closes; separation decoheres a shared closure | **proved** (closure) |
| [V4](#v4) | Phase singularities outrunning light (Technion) | Pattern features carry no closure, so no signal (`no_ftl_in_epr`); pairs annihilate as closures | **proved** (speed unbounded, no signal) |
| [V5](#v5) | Time crystals: acoustic beads (NYU), 144-qubit sheet (IBM) | Period doubling from `σ² = I`; non-reciprocity is a shared closure with the field | **proved** (single spin) |
| [V6](#v6) | Sodium clusters of 5,000–10,000 atoms in superposition (Vienna) | No collapse threshold below closure; objective collapse predicted absent | **consistent**; null predicted |
| [V7](#v7) | Collapse models imply a jitter in time | Time has a grain (one event), but no collapse-driven random walk | **proved** (bounded grain vs unbounded walk); no jitter predicted |
| [V8](#v8) | Thorium-229 nuclear clocks with feedback loops (TU Wien/PTB, Tsinghua) | `α = 1/(128 + d²)` has no time argument | **proved** (`α` cannot drift); kill condition stated |
| [V9](#v9) | CMS: no quark substructure to 17–37 TeV | A quark is one twist; substructure only at the event scale | **consistent**; null predicted |
| [V10](#v10) | False-vacuum decay on a Rydberg ring (Tsinghua) | An alternating ring closes iff it is even | **proved** |
| [V11](#v11) | Exact "spacetime crystals" of critical collapse (Ecker, Ecker, Grumiller) | Finite information puts a floor under the smallest black hole | **proved** (floor) |
| [V12](#v12) | The Einstein–Rosen bridge as a mirror in time (Gaztañaga et al.) | QLF's bra–ket closure already pairs a forward history with its mirror | **convergence**, proved core |

<a id="v1"></a>

## V1. The antimatter truck — CPT as a theorem about words

**Reported.** On 24 March 2026, CERN's BASE-STEP team drove 92 trapped antiprotons around the site by
truck, the first road transport of usable antimatter. The aim is to move them to a magnetically
quieter lab and improve on BASE's comparisons, which already match the proton's charge-to-mass ratio
to 16 parts per trillion and its magnetic moment to about 1.5 parts per billion.

**QLF.** The antiparticle is the Hermitian conjugate read backwards (`antiparticle`, from
[`QLF_Majorana`](lean/QLF_Majorana.lean)). Section §8 of the module proves, for **every** word:

- `antiparticle_length`: the mirror has the same number of events, so the same mass in QLF's account
  (mass as fold depth, [`Higgs.md`](Higgs.md)).
- `charge3W_antiparticle`: the charge is exactly opposite.
- `junctionBaryon_antiparticle`: the baryon number on the junction is exactly opposite (Part II §1).

So BASE's mirror is structural: QLF has no parameter that could make the proton and antiproton
masses differ. **Prediction:** every BASE comparison stays null at any precision, including the 100×
improvement the transport is meant to enable. **Kill condition:** a reproducible proton–antiproton
mass, charge-to-mass or moment difference. The matter excess itself is a separate, open question
(baryogenesis, magnitude `η_B` open in [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §3).

<a id="v2"></a>

## V2. Two liquids in every glass

**Reported.** A Stockholm team (*Science*, 26 March 2026) flash-melted glassy ices and probed the
liquid with an X-ray laser, finding a liquid–liquid critical point near 210 K and about 1,000 atm. A
City University of Hong Kong team (*Nature Physics*, 4 June 2026) let unsupervised machine learning
sort simulated water into a dense, disordered structure and a lighter, tetrahedral one that
continually turn into each other.

**QLF.** In [`Chemistry.md`](Chemistry.md) a bond is a shared closure, and water's valence rule gives
its four hydrogen-bond sites. The two structures are then two closure inventories: four shared
closures in a tetrahedron (open, ice-like) or a crowded arrangement with a fifth neighbour
(dense). Room-temperature water, lying beyond the critical point, is a superposition-of-ways: both
inventories happen, weighted by how many ways each closes.

This gives [`Mpemba.md`](Mpemba.md) something it lacked. Its stance is that the Mpemba effect is real
but preparation-specific, because relaxation depends on a hidden census rather than on temperature.
Water's two-structure population is a concrete candidate for that hidden census: two samples at one
temperature can carry different structure fractions. **Open:** a closure census that reproduces the
density maximum near 4 °C, and the prediction it would make for which preparations cool fastest.

**What is proved** (`density_maximum`, `no_anomaly_single`). In the simplest two-state model the open,
low-density fraction falls with temperature, shrinking the volume at rate `k`, while both structures
expand normally (coefficient `β`). If the open structure exists (`k > 0`), the volume has a strict
minimum, so the density a maximum, at `T₀ = k/2β > 0`. Without it (`k ≤ 0`), heating never shrinks
the liquid. So the density maximum *requires* the second structure: Röntgen's 1892 idea in one line.
The model fixes the mechanism, not the 4 °C; that number needs the census.

<a id="v3"></a>

## V3. Twins from the vacuum

**Reported.** STAR at Brookhaven (*Nature*, announced 4 February 2026) found `Λ`–`Λ̄` pairs from proton
collisions with spin correlation of about 18 ± 4%. Pairs emitted close together were fully aligned, as
virtual `ss̄` pairs in the vacuum should be; widely separated pairs lost the alignment.

**QLF.** A vacuum pair is a history joined to its own mirror, and `mirror_closes` proves every such
pair closes, for every word. In [`ER_EPR_QLF`](lean/ER_EPR_QLF.lean) a shared closure *is*
entanglement, so the vacuum twins are entangled from birth, not by later interaction. When the
pair's members close separately with their surroundings (more interactions as they separate), the
shared closure is diluted into a larger one. That is decoherence in QLF, and it predicts exactly the
pattern seen: alignment survives when the twins stay close and fades when they spread. The video
notes STAR cannot yet say whether the surviving link is quantum entanglement or classical
correlation. QLF says it starts as entanglement. Whether it still is at the detector is the open part.

<a id="v4"></a>

## V4. Darkness faster than light

**Reported.** A Technion team (*Nature*, April 2026) filmed phase singularities in phonon polaritons
in hexagonal boron nitride at 3 fs resolution. Singularities of opposite twist approached each other,
sped up without limit and annihilated, outrunning light just before meeting, as Nye and Berry
predicted in 1974.

**QLF.** A singularity is a feature of the pattern, not a closure. In QLF only closures carry events,
and `no_ftl_in_epr` already shows that a connection between spacelike ends transmits nothing. So
superluminal singularities break nothing, for the same reason the moon-sweeping laser spot doesn't.
Pair creation and annihilation conserves twist: a vortex with its antivortex is the mirror pair of
V3, and closes (`pairs_balanced`, Part II §6). `vortex_speed_unbounded` proves the
divergence: if two singularities annihilate with separation `κ√s` (`s` the time left), their approach
speed `κ/(2√s)` exceeds every bound, the speed of light included, at some moment before they meet. The
square-root law is the generic local form of a pair annihilation (Nye and Berry); it is assumed here,
not derived from the twist census.

<a id="v5"></a>

## V5. Time crystals

**Reported.** NYU (*Physical Review Letters*, February 2026) levitated two unequal polystyrene beads
in a standing sound wave. Each pushes on the other unequally through scattered sound, and the pair
falls into a self-sustained oscillation. IBM, NIST and Basque Quantum (*Nature Communications*,
January 2026) built a two-dimensional time crystal on 144 qubits.

**QLF.** Two results apply.

- **Period doubling** (`period_doubling`): flip a spin with `σx` once per drive period and it returns
  only every second period, since `σx² = I` but `σx ≠ I`. That is the discrete time crystal's
  signature at the level of one spin. The many-body rigidity that makes the rhythm robust is not
  proved here.
- **Non-reciprocity is a shared closure.** The beads' unequal pushes look like a broken third law
  until the sound's momentum is counted. In QLF that is `countBalanced_append_iff` (Part II §3): the
  beads alone are open, and the field carries exactly the opposite imbalance. Newton's third law holds
  for the closure, not for the visible part of it.

<a id="v6"></a>

## V6. A lump of metal in two places

**Reported.** Vienna (*Nature*, 22 January 2026) showed interference of sodium clusters of 5,000–10,000
atoms (over 170,000 u), reaching a macroscopicity of 15.5, about ten times the previous record.

**QLF.** Superposition is parallel histories, and measurement is closure, with no separate collapse
([`Measurement_Problem.md`](Measurement_Problem.md)). A cluster that closes with nothing on its way
through the interferometer stays in superposition however massive it is. QLF already lists objective
collapse (GRW, CSL, Penrose) among the rivals that larger superpositions should progressively exclude
([`Completeness_Evidence.md`](Completeness_Evidence.md)). **Prediction:** no mass threshold for
interference. Only isolation limits it. **Kill condition:** a reproducible loss of contrast scaling
with mass that no decoherence channel accounts for.

<a id="v7"></a>

## V7. A tremor beneath every second

**Reported.** Bortolotti, Curceanu, Diósi, Manti and Piscicchia (*Physical Review Research*, January
2026) showed that CSL and Diósi–Penrose collapse can be written as random fluctuations of gravity.
Those fluctuations would give every clock an unavoidable jitter, around 10⁻²⁸ s (CSL) or 10⁻³¹ s
(Diósi–Penrose) per year, growing like a random walk.

**QLF.** QLF agrees that time has a grain. Time is synthesized one closure event at a time
([`Time.md`](Time.md)), so it is counted, not continuous. But the grain is a count, not noise. A
clock's elapsed time is an integer number of events, read with an error of at most one event however
long it runs; nothing accumulates. **Prediction:** no collapse-driven clock jitter, consistent with QLF's
no-collapse stance (V6). The two pictures differ in growth: collapse models predict uncertainty
rising like `√t`, QLF a bound that does not grow. Both halves are proved:
`tick_error_bounded` (counted time errs by less than one event, for every duration) and
`random_walk_unbounded` (a jitter `σ√t` exceeds every bound). Neither is measurable with present
clocks, but they disagree about growth, which is what a long-baseline comparison (pulsars against
atomic clocks, as the video suggests) would test.

<a id="v8"></a>

## V8. A clock inside the nucleus

**Reported.** In June 2026, Thorsten Schumm's group at TU Wien (with PTB) and Shiqian Ding's group at
Tsinghua independently locked lasers to the 8.3 eV thorium-229 nuclear transition in calcium fluoride
crystals: the first nuclear clocks. Vienna used theirs straight away to search for ultralight dark
matter and found none. The transition is expected to be thousands of times more sensitive to changes
in `α` than atomic clocks.

**QLF.** Two existing predictions are now tested by the most sensitive instrument there is.

- **No drift of `α`.** `α(d) = 1/(128 + d²)` depends on dimension only, with no time argument
  ([`QLF_FineStructureSubstrate`](lean/QLF_FineStructureSubstrate.lean)). **Kill condition:** any
  confirmed variation of `α` in nuclear-versus-atomic clock comparisons. The existing
  `no_cosmological_drift_of_alpha` is `True := trivial` and anchored nothing. `alpha_cannot_drift`
  now proves the claim: a continuous history of `α` whose every value is `1/(128 + d²)` for some
  natural `d` is constant. The value set is countable, so it contains no interval for `α` to move
  through. A measured drift would therefore show `α` is not a substrate count.
- **No ultralight dark-matter field.** QLF predicts no dark-matter particle or field (Part II §8), so
  Vienna's null is the expected result.

<a id="v9"></a>

## V9. Is there anything inside a quark?

**Reported.** CMS (26 March 2026) compared dijet angular distributions from 138 fb⁻¹ at 13 TeV with
the most precise Standard Model predictions and found agreement. Quark compositeness is excluded below
17 or 37 TeV depending on the model. Searches for extra dimensions, quantum black holes, dark-matter
mediators and axion-like particles found nothing.

**QLF.** In the §30 signature a quark is one twist (the down quark adds one gauge twist), and a twist is
a single closure event. QLF's quarks are therefore point-like down to the event scale, the Planck scale,
not some intermediate preon scale. **Prediction:** no compositeness signal at any collider energy. The
other CMS nulls match QLF's predicted absences: no axion, no fundamental dark-matter particle
([`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §6), and no Higgs-sector new physics
([`Higgs.md`](Higgs.md)).

<a id="v10"></a>

## V10. The universe ending in a ring of atoms

**Reported.** Tsinghua (*Physical Review Letters*, 27 March 2026) prepared an even ring of Rydberg
atoms in the higher of two alternating patterns, tilted by site-resolved lasers, and watched it decay
to the lower one through bubble nucleation. The decay rate followed Coleman's exponential dependence
on the inverse tilt. The ring had to be even for the alternating pattern to close.

**QLF.** `ring_closes_iff_even` proves the ring point: an alternating ring is a closure exactly when its
number of sites is even. An odd ring forces a defect somewhere. It is the same parity rule as
contacts at odd sequence separation in [`Protein_Folding.md`](Protein_Folding.md).

On our own vacuum: the Standard Model's metastability comes from running the Higgs quartic up to the
Planck scale ([`Higgs.md`](Higgs.md)), the kind of continuum extrapolation QLF says fails at the event
scale. In QLF the vacuum is the closure, zero free action, and no history has less than zero
imbalance. **Conjecture:** our vacuum is absolutely stable, not metastable. Not testable now, and not
proved here.

<a id="v11"></a>

## V11. Crystals made of spacetime

**Reported.** Christian Ecker, Florian Ecker and Daniel Grumiller (*Physical Review Letters*, May 2026)
found exact formulas for Choptuik's discretely self-similar critical solutions by solving gravity in
the limit of many dimensions and working back. At threshold, the solution repeats on ever smaller
scales; just above it, black-hole mass scales as a power (`γ ≈ 0.37`) of the distance from threshold,
with no lower limit, and the exact threshold hosts a naked singularity.

**QLF.** QLF puts a floor under that. A finite region holds finite information
([`QLF_Realizability`](lean/QLF_Realizability.lean)), so initial data can be tuned only to finite
precision. `critical_mass_floor` proves the consequence: with `B` bits of tuning, the mass is at least
`C·2^{−γB} > 0`. Arbitrarily small black holes and the naked singularity both need infinite tuning,
which no realizable region has. The physical floor is the Planck mass, where a closure becomes its own
horizon ([`Planck_Scale.md`](Planck_Scale.md)). Discrete self-similarity itself is the continuum face
of QLF's self-similar closures ([`self_similar_closures.py`](self_similar_closures.py)), though nothing
here derives the echo period `Δ ≈ 3.44`.

<a id="v12"></a>

## V12. A bridge between two directions of time

**Reported.** Gaztañaga, with Kumar and Marto (*Classical and Quantum Gravity*, January 2026), read the
Einstein–Rosen bridge as a pairing of a forward-in-time and a backward-in-time component of a quantum
field in curved spacetime, not as a tunnel. Information crossing a horizon keeps evolving in the mirror
direction. The video presents it as a debated proposal.

**QLF.** This is the closest convergence in the list, and QLF reached it independently. In
[`BraKetRhoQuCalc`](lean/BraKetRhoQuCalc.lean) a ket is a forward history and a bra its time-reversed
mirror; ZFA balance *is* bra–ket well-typedness. [`Reversibility.md`](Reversibility.md) identifies
time reversal with the Hermitian conjugate. `mirror_closes` now proves the general form: **any history
joined with its time mirror closes**. And [`ER_EPR_QLF`](lean/ER_EPR_QLF.lean) identifies the bridge
with a shared closure. So in QLF the Einstein–Rosen bridge is a closure of a history with its mirror,
which is the temporal reading Gaztañaga proposes. The cosmological claims (a bounce, relic black holes
as dark matter, the CMB parity asymmetry) are theirs, not QLF's.

# Part II — Other 2026 results

## At a glance

| # | Result (2026) | QLF's prior view | What is new here | Status |
|---|---|---|---|---|
| [1](#p1) | Baryon number carried by a gluon junction (STAR, *Science*) | Baryon number is a 3-axis winding ([`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean)) | The windowed winding reads the neutron as `B = 0`. Read on the junction, `B = 1` and no flavour change can move it | **proved**, and a correction |
| [2](#p2) | Doubly charmed baryons `Ξcc⁺`, `Ωcc⁺` (LHCb) | `Q = (2/3)N − n_g` ([`QLF_QuarkSignature`](lean/QLF_QuarkSignature.lean)) | The charge ladder `3Q = 6 − 3k` with `B = 1` on every rung; charge is generation-blind | **proved** |
| [3](#p3) | Entangled Z pairs from Higgs decay (ATLAS) | Entanglement is a shared closure ([`ER_EPR_QLF`](lean/ER_EPR_QLF.lean)) | Two histories close together iff their action vectors are opposite on every axis; an open child forces an open partner | **proved** |
| [4](#p4) | Dissipationless 1-D transport (TU Wien) | Conservative logic is free ([`QLF_Fredkin`](lean/QLF_Fredkin.lean)) | Elastic 1-D collisions are permutations: the whole velocity distribution is conserved | **proved** |
| [5](#p5) | Altermagnetism in thin, tunable films | Handedness and count balance ([`QLF_Handedness`](lean/QLF_Handedness.lean)) | The d-wave splitting is the only one that is inversion-even and odd under the axis swap | **proved** |
| [6](#p6) | Quantum Shapiro steps in cold atoms | Vorticity quantised to `±1` per cell ([`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md)) | `n` vortex–antivortex pairs close for every `n`; the step index is a closure count | **proved** (structural) |
| [7](#p7) | IceCube and the 2026 Nobel Prize (Halzen) | Neutrino is Majorana; mixing angles open ([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md)) | μ–τ symmetric mixing sends a `1:2:0` source to exactly `1:1:1` | **proved**, conditional on μ–τ symmetry |
| [8](#p8) | A single unexplained event at LZ | No dark-matter particle ([`DarkMatter.md`](DarkMatter.md)) | Kill condition stated | **test pending** |
| [9](#p9) | `B → Kπμμ` tension, "charming penguins" (LHCb) | No new particles; hadronic sector open | GIM: only mass differences enter; the tension should resolve inside the Standard Model | **proved** (GIM); prediction falsifiable |
| [10](#p10) | Vacuum-enhanced superconductivity in a cavity (NbSe₂) | The Casimir effect as a finite census ([`QLF_Casimir`](lean/QLF_Casimir.lean)) | A reading, and the disputed point it has to face | **open bridge** |
| [11](#p11) | A 40-year-old CFT energy ladder measured (Caltech) | Ising exponents tested ([`ising_exponent_test.py`](ising_exponent_test.py)) | Where QLF would have to reproduce it | **open** |
| [12](#p12) | Pair density waves in UTe₂ | Cooper pairs as shared closures ([`Carbon_Superconductivity.md`](Carbon_Superconductivity.md)) | A reading only | **open** |

<a id="p1"></a>

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

<a id="p2"></a>

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

<a id="p3"></a>

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

<a id="p4"></a>

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

<a id="p5"></a>

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

<a id="p6"></a>

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

<a id="p7"></a>

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

<a id="p8"></a>

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

<a id="p9"></a>

## 9. The B-meson tension — a prediction of no new particle

**The result.** An analysis of `B → Kπμμ` disagrees with the Standard Model, and the tension is tied
to "charming penguins": charm-loop contributions that are hard to compute ([Phys.org][penguin]).

**QLF's position, as a falsifiable null.** QLF predicts no supersymmetric partners, no axion and no
fundamental dark-matter particle ([`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md) §6). The same
economy predicts no Z′ or leptoquark behind flavour anomalies. CKM unitarity is closure
([`QLF_CKM`](lean/QLF_CKM.lean)), and the hadronic sector is QLF's open frontier, the same frontier as
muon `g − 2` ([`g_minus_2.md`](g_minus_2.md)). `gim_shift` and `gim_degenerate` prove the
GIM mechanism in QLF's unitarity-as-closure form: if the CKM factors of a flavour-changing loop sum to
zero, the loop depends only on mass differences and vanishes for degenerate masses. What survives in
`b → s` is the top term and the charm term, and the charm term is exactly the hadronically uncertain
"charming penguin". **Prediction:** the tension resolves within the Standard Model as the charm-loop
contribution is pinned down. **Kill condition:** a 5σ deviation in a
clean channel (one with negligible charm-loop contamination, such as `B_s → μμ` or lepton-universality
ratios) that a new mediator fits.

<a id="p10"></a>

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

<a id="p11"></a>

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

<a id="p12"></a>

## 12. Pair density waves in UTe₂ — a reading only

A July 2026 *PNAS* paper finds charge-density-wave peaks in UTe₂ that track a pair density wave coupled to
uniform superconductivity ([arXiv:2603.08688][pdw]), while a hard X-ray study sees no bulk CDW
signature ([NIST][nist]). In QLF a Cooper pair is a shared closure
([`Carbon_Superconductivity.md`](Carbon_Superconductivity.md)), and a pair density wave is a pair whose
closure balances over a wavelength rather than at each site. That is a reading, not a result, and the
experimental picture is itself unsettled.

<a id="p13"></a>

## 13. Not yet covered

Later 2026 results go here, each with a source before a reading is written.

## Sources

- Nap Theory, *The Most Insane Physics Discoveries Of 2026 (That You Haven't Heard Of)* — [YouTube](https://youtu.be/NwKzvBN9wh4). Part I's experimental details and the papers named there are as reported in the video.

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
