# The Spacetime Constructor — quantum logic generating something from nothing

An interactive companion to [SpaceTime.md](SpaceTime.md) and the [Quantum Logical Framework](README.md) (QLF).
Its sibling tool is [`fredkin_machine.html`](fredkin_machine.html) ([`Fredkin_QLF.md`](Fredkin_QLF.md)) — the
same substrate read as a *computer* rather than a world: conservative logic stepping gate by gate, with the
ball count and the twist action held fixed, and a reverse button that walks a full adder back to its input.
Open [`spacetime_constructor.html`](spacetime_constructor.html) in any browser, or run it live on GitHub Pages:
[**spacetime_constructor.html**](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html).
Dependency-free, self-contained, mobile.

---

## The thesis: no forces, no fields — only closures that happen in the most ways

There are **no forces and no fields** here, and **no magical influence at a distance** — nothing reaches across a
gap to push, pull, or signal anything. There are only **ZFA closures**: balanced phase-string histories that come
back to zero ([`QLF_Axioms`](lean/QLF_Axioms.lean), [`QLF_Universality`](lean/QLF_Universality.lean)). And not
closures that merely *can* close — the ones that **do** close, because in a quantum-logical system a thing does not
happen in one way: **it happens every way that is possible**, and what we see is what happens in the **most ways**.

- **Everything happens every possible way.** The one **first distinction** (`+g/−g`, phase 0) unfolds the whole
  closure census — the *logical bang* ([`Creation.md`](Creation.md) §8a, [`QLF_LogicalBang`](lean/QLF_LogicalBang.lean)).
  Something from nothing: no field is posited, no matter is placed, nothing is scripted. Every admissible history is
  taken (possibilist modal realism, [`Philosophy.md`](Philosophy.md)); the substrate does not pick one path.
- **Frequency *is* the number of ways.** A closure's **frequency is its multiplicity** — the count of distinct ways
  it can happen (the census count, `C(2n,n)` and its kin, [`QLF_CensusBrownian`](lean/QLF_CensusBrownian.lean),
  [`QLF_CensusShannon`](lean/QLF_CensusShannon.lean)). The closures that happen in the **most ways** are the abundant,
  low, persistent ones; the few-ways closures are rare and fleeting. So frequency **causes nothing** — it *is* the
  count of ways, and (Born statistics are integer count ratios, [`QLF_BornProbability`](lean/QLF_BornProbability.lean))
  it is why the common things are common. `f = 1/R` reads out as space (*where* the closures are), time (*how fast*
  they tick), and colour (that same rate on the spectrum) — three readings of one count, never a cause.
- **A 3-D perspective renders it.** A closure is a **3-axis closed walk** — one balanced ±1 history per axis
  (`#^=#v ∧ #<=#> ∧ #/=#\`) — and *its own walk draws the space it occupies*. The world is not drawn *in* a 3-D box;
  the 3-D box is drawn *by* the closures, from the vantage of one observer (below).
- **The background radiation *enhances* the generation.** The vacuum's background radiation spectrum — the
  Gibbons–Hawking glow of the horizon ([`QLF_HorizonTemperature`](lean/QLF_HorizonTemperature.lean)) — sets how much
  of the churning logical foam **freezes out as persistent matter**. Turn it up and more of what is already happening
  survives as real particles, atoms, nuclei, black holes. It is an *amplifier* on the generation, never its cause.

Everything below is a consequence: closures that **do** happen — every way, the most-ways ones dominating — with no
force, no field, and no action at a distance.

---

## Generation from nothing

**The vacuum is never dead.** Even at absolute zero the substrate keeps closing balanced matter–antimatter pairs
that flicker straight back to possibility — the quantum **foam**, the `Ω_Λ = log 2 ≠ 0` floor
([`QLF_CosmologicalConstant`](lean/QLF_CosmologicalConstant.lean)). This is the generator running with no input:
logic producing balanced pairs from nothing, because a lone net charge cannot close
([`QLF_Confinement.charged_not_closed`](lean/QLF_Confinement.lean)) but a balanced pair can. The census unfolds
lightest-first, so the abundant low modes (electrons) dominate and heavier closures (muons, nucleons) appear as
the logic reaches them — the frequency ordering is the *shape* of the unfolding, not its cause.

**The background radiation enhances the freeze-out.** A slider runs (log-scaled) over the vacuum's background
radiation from **absolute zero** through the **CMB (2.7 K, the default)** to the **Planck temperature (~10³² K)**.
It does not create closures — it decides how many of the ones the logic is already generating **persist as real
matter** versus **flicker back as virtual foam**: cold ⇒ almost all foam (a seething but empty-looking vacuum);
warm ⇒ matter freezes out; near the Planck top ⇒ black holes. Heating walks the generated world forward through
cosmic history rather than switching anything on.

**This is the Big Bang, from the inside.** The hottest setting is the earliest instant. Turn the background down
from the Planck top and the constructor walks the *logical bang*'s phases outward on its own: a plasma of tiny
**Planck-mass black holes** → **hadrons** emerging as they Hawking-cascade (the nucleon ring `p`, `n`) →
recombination into **atoms** as it cools. None of it is scripted — it falls out of ZFA and the census, so the tool
reproduces **primordial black holes** and the **hadron epoch** as consequences of the substrate, not inputs.
(Legacy pictures like "recombination at ~3000 K" are one rendering of the same closure dynamics; we obey ZFA and
let them emerge, never hardcode them.) The Planck black-hole genesis — the Compton = Schwarzschild crossing at
`μ² = 1/2` — is computed exactly in [`genesis.py`](genesis.py) §7 / [`Genesis.md`](Genesis.md)
([`QLF_QuantumBlackHole`](lean/QLF_QuantumBlackHole.lean), [`QLF_PlanckScale`](lean/QLF_PlanckScale.lean)).

---

## The 3-D perspective — existence is what a limited observer carves out of nothing

**All possible logical systems already exist — and, taken whole, they add to nothing.** Every admissible closure
exists *a priori*, the full space of balanced histories ([`QLF_Universality`](lean/QLF_Universality.lean),
[`Philosophy.md`](Philosophy.md)). But they are **perfectly balanced**: every closure has its conjugate, matter has
its antimatter, and the total sums to zero — ZFA = 0, exactly the **net free energy** the readout holds at **0**.
From an unlimited, god's-eye view there is therefore *no thing at all* — only the balanced All, adding to nothing.

**What makes anything exist is the observer's limit.** A something appears only because a perspective is **bounded**:
an observer sees a finite slice — a Markov blanket at the origin of its own horizon
([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean): *observation is bounded closure*), carrying finite information
([`QLF_Realizability`](lean/QLF_Realizability.lean)). Inside that horizon the cancellation is incomplete, so the
balance **reads out as a world** — matter, space, time — while its conjugate sits outside the cut. Existence is not
in the substrate; it is in the *perspective*. There are not many worlds, only **many observers**, each cutting its
own something out of the same balanced nothing (Smolin; [`Philosophy.md`](Philosophy.md)). This is why the tool is
drawn from exactly **one** frame, and why the total still reads **0**: you are watching one observer's limited cut of
a whole that cancels.

So the world is drawn from that one observer's frame — the stick figure. He *is* the **frame origin**, and every view
operation is his:

- **Orbit** (drag off him) spins the generated world around him.
- **Zoom** homes in *from the observer* — his screen position is the fixed point of the zoom, not the display
  centre.
- **Grabbing the observer** (or `Shift`-drag anywhere) **trucks the whole perspective with him**: the observer and
  the entire scene translate together, because moving the frame origin moves everything relative to it.

There is no god's-eye spin (auto-spin is opt-in). This is also why the **background glow arrives from the sky
inward**: it is the Gibbons–Hawking radiation of the de Sitter **horizon**, emitted on the outer shell and
travelling in toward the observer — not a source inside.

---

## Reading the generated world (frequency is a label, not a driver)

**Mass, redshift, and time dilation are one reading.** Mass is not placed — it *arises* as the closures lower the
local ZFA degeneracy `w_ZFA` (the possibilist gradient, [SpaceTime.md](SpaceTime.md) §5). Near a mass, clocks tick
slower **and** redden together; far away they run fast and blue. Gravitational time dilation and gravitational
redshift are not two effects — they are the single rate drop, shown as one colour shift. Telemetry reads the
deepest-well clock ratio and the redshift `z`.

**Select a frequency band — a microscope, not a knob.** Two **log sliders** over rest frequency `f = m/mₑ` (since
`E = m = 1/R`) select a band `[f_lo, f_hi]`. The visible spectrum is then *stretched across the band* — band-low →
red, band-high → violet — so a narrow band spreads the full rainbow across just those frequencies; closures outside
the band dim, and **Capture** takes only the in-band closures. It filters *which generated closures you look at*;
it changes nothing about what the logic generates.

**Click to identify.** Pause and click anything — it names itself by its frequency reading (`m = 1/R`): a particle
by its rest-mass frequency and **spin** — the twist itself, two-component (σ_y `↑`/`↓` **and** σ_x `→`/`←`, e.g. `↑→`;
[`QLF_Spin`](lean/QLF_Spin.lean)); an atom by its
constituents; a field node by its own spin (from the census walk that placed it); a **photon by its frequency**
(`E = ℏω`: 438 THz red … 769 THz violet, or a γ-ray from annihilation); a **black hole** by its mass, charge `Q`
and spin `J`; a hadron *as a quantum black hole*; a virtual flicker *as a vacuum fluctuation*.

**Spin webs — entanglement and exclusion.** Two overlays draw the spin relationships between closures. **Entanglement**
(ER=EPR — a shared closure) joins spin **singlets** — anti-correlated pairs — `↑↔↓` on the σ_y axis (blue) and `→↔←`
on σ_x (orange). **Exclusion** joins **identical**-spin closures (the same state that cannot coincide) — the degeneracy
web Pauli pressure holds apart ([`PauliExclusion`](lean/PauliExclusion.lean)), in red. Opposites correlate; likes exclude.

**The field readout.** Collapsible; counts **atoms, molecules, particles, foam (virtual particles), and black
holes** — hover any count for a per-type breakdown (which species, or each black hole's `M/Q/J`). It gives the
**total energy** as `E = m = 1/R` (in `mₑ`, and in GeV on hover — a proton reads its 0.938 GeV), with both books:
the **gross** content/activity (matter + vacuum foam + radiation) and the **net free energy** — matter(+) minus
antimatter(−) — which for a balanced vacuum is **0 = Zero Free Action**, the founding principle shown directly on
the telemetry. It also tracks **matter vs antimatter**: every vacuum process makes balanced pairs and every decay
conserves, so `M − M̄` holds at **0** — a genuine excess would require the Sakharov conditions
([`QLF_Baryogenesis`](lean/QLF_Baryogenesis.lean)), which this vacuum does not provide.

**The vacuum's energy density — dark energy is the floor, not a constant.** The **Vacuum ρ** readout gives the
physical energy density (real `T`, scale-independent), with regimes named on hover:
- **dark energy** — the cold floor, the cosmological-constant term. QLF derives it,
  `ρ_Λ = (3 log 2 / 8π)·c⁴/(G R_H²) ≈ 3.35 GeV/m³`, matching the measured value to ~1%
  ([`Cosmological_Constant.md`](Cosmological_Constant.md) §3).
- **dark matter** — scales as `(T/T_CMB)³`, overtaking the floor just above the CMB.
- **vacuum energy** — the thermal term `∝ T⁴`, reaching the **Planck density (~5×10¹¹³ J/m³)** at the Planck
  temperature.

So the famous **10¹²² "vacuum catastrophe" is just the two ends of this one axis** — dark energy the floor, the
Planck density the ceiling — walked live by the slider.

---

## How the generated world moves and binds

**Interaction is the geometry, not a force.** A body moves *down the local `w_ZFA` latency gradient* — `−∇w`,
mass-independent (the equivalence principle; the well depth already carries the mass). Every body sources that
field, so they interact automatically. There is no wall: a body that drifts far out free-streams into the vacuum
(the ultimate absorber) — nothing bounces off an invisible sphere.

**The vacuum foam nudges the matter — a ZFA-balanced Brownian walk.** An immersed closure is buffeted by the
surrounding foam, so real particles execute a **random walk on top of their gradient drift** — Einstein's Brownian
motion with the foam as the medium. The walk is **not dice**: each kick is the step of a **closed census walk** (a
ZFA-balanced ±1 history, [`QLF_CensusBrownian`](lean/QLF_CensusBrownian.lean) /
[`QLF_Turbulence`](lean/QLF_Turbulence.lean)) drawn from the same census that draws the space. Because the walk is
*closed*, its increments **sum to zero over each period** — zero net impulse, no net energy added: a ZFA-obedient
jitter, not a hidden force. (`Vacuum jitter` toggle, default on.)

**Bound states assemble themselves.** A free proton and electron drift together and **recombine into hydrogen**
(emitting a photon); two hydrogens **bond into H₂** (a shared closure, the bond line); a matter atom meeting
**antihydrogen annihilates**. Atoms are the real observables (free leptons are not stable closures,
[`Bound_States_QLF.md`](Bound_States_QLF.md)) — a proton nucleus with an electron on a tilted orbital shell.

**Pauli exclusion holds matter apart.** Attraction alone would collapse everything into the wells. Matter keeps its
size because **identical fermions cannot occupy the same state** ([`PauliExclusion`](lean/PauliExclusion.lean)):
same-kind fermions repel at short range, and that degeneracy pressure balances the infall — the outward half of
every stable structure. So a **crystal** holds: seed a lattice and Pauli pressure vs the wells settles it into a
self-bound solid (a *macroscopic resonant lattice*, [`Geometry_Of_Space.md`](Geometry_Of_Space.md)), breathing at
finite temperature rather than freezing dead — no pinning, no external force. (A proton repels a proton, but not an
antiproton, which it annihilates with — exclusion is between identical fermions.)

**Unstable closures decay — deterministically.** The muon and free neutron are not the deepest closure, so they
decay to lighter products (`n → p + e⁻ + ν̄`; `μ⁻ → e⁻ ν̄_e ν_μ` — charge, baryon and lepton number conserved),
while the proton and electron persist. Decay is **not a random timer**: each lifetime is the census inverse-CDF of
the exponential, so the *population* decays exponentially — deterministic ensemble statistics of the prime bath
([`Decay.md`](Decay.md) §1a).

**Photons interact along their path, and are received.** A photon **bends in the latency field** — the `w_ZFA`
gradient acts as a refractive index, so light lenses toward mass (the interaction is the geometry), running dead
straight only in flat vacuum, always at speed `c` (the gradient turns the direction, never the magnitude — the
uniform stateless ether ⇒ local Lorentz invariance). The background sky is emitted on the horizon as a
**hierarchical cascade** — twice as many photons at half the energy (`1 : 2 : 4`), red-dominated with a few blue.
That cascade *is* QLF's zero-point spectrum made visible: number per frequency `n(ω) ∝ 1/ω`, so the energy per
octave is flat (`1·ω = 2·½ω = 4·¼ω`) — the scale-invariant, infrared-dominated vacuum spectrum of
[`VacuumEnergy.md`](VacuumEnergy.md), the opposite of QFT's ultraviolet-heavy zero-point sea (and why there is no
`10¹²⁰` catastrophe — the weight sits in the soft, not the hard, modes). A photon **ends when a local observer
receives it** (a measurement, marked by a flash); otherwise the **vacuum is the ultimate absorber**, and the
absorbed energy returns to the vacuum account — never vanishing.

---

## Create your own — QuCalc

The scene is **editable as QuCalc**. **Capture** serialises what the observer can *see* — the closures **on screen**,
narrowed to the **selected frequency band** (magnification and frequency both limit his reach) — one ZFA closure per
line (`kind twist @ x,y,z`), with the verified folds (electron `^<v>`, positron `<^>v` = its adjoint,
[`QLF_PhaseInformation`](lean/QLF_PhaseInformation.lean)). Type or paste closures and **Replace** (clears first) or
**Inject** (adds) to instantiate them through the same engine, so the dynamics keep running. **Macros** expand named
composites: `positronium`, `muonium`, light nuclei (`deuteron`, `helium3`, `alpha`), and hadrons shown as their
**confined quark content** (`proton_uud`, `pion+`) — a **free quark is rejected**, a colour-singlet obstruction
forbidding it from closing ([`QLF_Confinement`](lean/QLF_Confinement.lean)). **Atoms come in elements** — hydrogen,
helium, carbon, oxygen, iron — each a nucleus of `Z` protons + `N` neutrons with `Z` electrons on its shells (heavier
⇒ bigger nucleus, deeper latency well, more mass).

**Chemistry — one rule.** A bond is a **shared closure**, and a single **valence** rule drives every reaction: two
isolated atoms with free valence (H:1, O:2, C:4, Fe:3, He:0) that drift within range share a closure until saturated.
From that one rule, molecules self-assemble — **H₂, H₂O, CO₂**, carbon networks (**graphite**), and metal oxides
(**Fe₂O₃ rust**) — while noble gases stay inert and metals lattice rather than form discrete metal molecules. Full
account in [`Chemistry.md`](Chemistry.md). And **crystals**: pick an element and a lattice
(`lattice sc|bcc|fcc n spacing motif @ x,y,z`, or the element dropdown + SC/BCC/FCC buttons) — Pauli pressure then
holds the lattice together (iron BCC as a metal; cold **helium Bose-condenses into a superfluid**). New closures
never stack — Pauli exclusion places each in the nearest free spot. *A URL hash `#qc=…` preloads any of these scenes,
so links can open a live demo.* Hash parameters: `#qc=<QuCalc>` (the scene), `&t=<0..1>` (temperature), and
`&oct=<1..12>` (harmonic octaves). **Any preset scene defaults to a single harmonic octave** (`oct=1`) so the
injected particles render at full brightness rather than being dimmed across the octave spread — pass `&oct=6`
to restore the hierarchical vacuum-foam look.

---

## No probability — the census draws the world

The constructor uses **no randomness**. Genesis ([`Genesis.md`](Genesis.md), [`genesis.py`](genesis.py)) starts from
the first distinction and builds the exact census; a ZFA-balanced ±1 history is a **closed walk**, and three of them
interleave into a **3-axis closure** (the `−3/2` census exponent). Each node is placed by such a closure's own walk —
its maximal excursion in 3-space — so the world is literally *drawn out by the closures*: *each closure renders its own
continuum, one closure at a time*. Scalar needs (orbit planes, phases, emission directions) read the same closures as
base-2 fractions. Probability is not a primitive — Born statistics are integer count ratios
([`QLF_BornProbability`](lean/QLF_BornProbability.lean)); even decay is deterministic ensemble logic — and the same
census that yields `π` ([`QLF_PhysicalPi`](lean/QLF_PhysicalPi.lean)) here yields the geometry.

---

## Honest scope

The constructor is a **qualitative** visualization: a latency field (`f ∝ w_ZFA`) with illustrative particle
dynamics, not the ZFA engine of [`twist_core.py`](twist_core.py) or a solved metric. Lifetimes encode *ordering*
(muon short, neutron longer, proton/electron stable), not literal ratios — real μ (2.2 µs) and free n (~880 s) differ
by 10⁸, impossible to show on one timescale. It is the companion picture to the numerical engine in
[`MultiParticle.py`](MultiParticle.py) / [`MultiParticle.md`](MultiParticle.md), where the same shared-closure
entanglement is computed rather than drawn.
