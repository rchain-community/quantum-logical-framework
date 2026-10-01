# Electricity

**Current, voltage, resistance, Ohm's law, Joule heating, and superconductivity from the gauge-fold substrate.**

**Repository:** [`rchain-community/quantum-logical-framework`](https://github.com/rchain-community/quantum-logical-framework)
**Author:** Jim Whitescarver
**Date:** June 9, 2026

---

## The one premise, and the thesis

This document rests on the single conditional the whole framework rests on:

> **The universe IS a quantum-logical system, and physical reality is the subset of admissible histories that achieve Zero Free Action (ZFA = 0).**

Charge is already settled in QLF: it is the net gauge-fold count, `charge(h) = count(+) − count(−)` ([Maxwell.md](Maxwell.md), [Conservation.md](Conservation.md) §4), conserved because gauge folds are created and destroyed only in Hermitian `+−` pairs (`no_magnetic_monopoles`, [`lean/ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean)). Electricity is what happens when that charge **moves**. The thesis:

> **Conduction is gauge-fold transport, and resistance is the latency of finding a ZFA closure to hop through — the very same `Δt ∝ 1/W_ZFA` that QLF uses for time dilation and gravity.** Ohm's law is its linear response; Joule heating is the per-event `log 2` (Landauer) dumped to the lattice bath; superconductivity is a quiet-frequency channel with no pruning to scatter into — the same frequency isolation that carries the quantum brain; and the quantum of resistance is the vacuum impedance divided by `2α`, fixed by the same `α` QLF derives from the substrate.

Each claim below is backed numerically by [`electricity_demo.py`](electricity_demo.py).

## 1. Charge and current

Charge is the gauge-fold imbalance `count(+) − count(−)`; the U(1) gauge symmetry of QED is the discrete `+`↔`−` swap ([Conservation.md](Conservation.md) §4). **Current** is the missing kinetic piece: the net rate at which gauge-folded carriers are transported per clock tick. [Maxwell.md](Maxwell.md)'s Ampère term already names it — "the conduction current `J` is the net flow velocity of gauge-imbalanced threads" — and we make it precise:

$$I = \frac{dq}{dt} = n\,q\,v_d \quad\text{(carriers × charge × drift velocity)},$$

with `v_d` the mean forward drift of the carriers' history strings per tick. No charge moves without a bias to move it — that bias is voltage.

## 1a. Current and the magnetic field

A current doesn't just move charge — it builds a magnetic field, and QLF says why. The magnetic field here is a **net spatial-axis twist count**, `B_x = count(>) − count(<)` (and likewise y, z; [Maxwell.md](Maxwell.md) §1) — the same per-axis count that is a history's *momentum* ([Conservation.md](Conservation.md) §3). A current is gauge-folded carriers drifting along an axis; that directed transport imprints a **circulating** spatial-axis bias on the surrounding vacuum, and that circulation *is* B. Ampère's law,

$$\nabla\times\mathbf{B} = \mu_0\mathbf{J}\ \;(+\,\mu_0\varepsilon_0\,\partial_t\mathbf{E}),$$

is then the statement that the **curl of the spatial-twist-count field equals the gauge-fold transport rate** `J` ([Maxwell.md](Maxwell.md) Eq. 4). Equivalently, in integral form `∮ B·dl = μ₀ I_enc`: the circulation of the count field around any loop returns the enclosed transport rate, independent of the loop radius. The right-hand rule is the chirality of the transport fixing the sense of the circulation; a solenoid or electromagnet is a current organizing the vacuum's spin-orientation bias along the coil axis ([Magnetism_Spatial_Dynamics.md](Magnetism_Spatial_Dynamics.md)). Current and field are two readings of one transport — and a static `count(+) − count(−)` imbalance with *no* transport is pure charge with no field, exactly as `∇·B = 0` requires (`no_magnetic_monopoles`). [`electricity_demo.py`](electricity_demo.py) checks the circuital law numerically: `∮ B·dl = μ₀ I` to machine precision, independent of radius.

## 2. Voltage — the free-action gradient that drives transport

Voltage is **energy per charge**: the free-action gradient that biases which way a carrier's next closure resolves. The QLF electric field is the transverse momentum-exchange rate of the ZFA event stream ([Maxwell.md](Maxwell.md) §2, `∇·E = ρ/ε₀`); the potential difference is its line integral, `V = ∫ E·dl`. Each carrier carries `ℏω` of energy at its internal Markov-blanket frequency ([Information_Energy_Equivalence.md](Information_Energy_Equivalence.md), [Per_Qubit_Mass_Quantum.md](Per_Qubit_Mass_Quantum.md)); voltage is the work per unit charge the field does pushing that closure forward. An EMF is any non-electrostatic source of the same gradient.

## 3. Resistance is ZFA-closure latency

Here is the load-bearing identification. A carrier advances only when it finds a ZFA closure to hop into, and — exactly as in [Time.md](Time.md) §2 / [SpaceTime.md](SpaceTime.md) §2 — the **latency of that resolution is the inverse of the available closure degeneracy**:

$$\Delta t \;\propto\; \frac{1}{W_{ZFA}}.$$

`W_ZFA` is the number of admissible closures open to the next hop. **Scattering** — phonons, impurities, lattice disorder — is the pruning of those paths: it lowers `W_ZFA`, raises the per-hop latency, and so raises resistance:

$$R \;\propto\; \frac{1}{W_{ZFA}}.$$

The Drude form `σ = nq²τ/m` is the continuum limit, with the relaxation time `τ` precisely this closure latency. [`electricity_demo.py`](electricity_demo.py) confirms it: simulating carriers whose closure rate is `∝ W_ZFA`, the fitted resistance times `W_ZFA` is constant across `W = 1,2,4,8` (`R·W ≈ 250` each), i.e. `R ∝ 1/W_ZFA`.

This is a **unification, not an analogy**: resistance, time dilation, and gravity are the *same* `1/W_ZFA` latency — resistance is latency for charge transport, time dilation is latency for event synthesis ([Time.md](Time.md) §4), and gravity is its spatial gradient ([Curvature.md](Curvature.md) §3, [Gravity.md](Gravity.md)). A resistor, a clock in a gravity well, and an infalling mass are running the same closure-search slowdown.

## 4. Ohm's law

Ohm's law is the **linear response** of §3: the driving free-action gradient equals the transport rate times the per-carrier closure latency,

$$V = I R \qquad\text{(continuum: } J = \sigma E\text{)}.$$

In the demo, current is linear in voltage to a least-squares fit of `R² = 0.995–0.9996`, with slope `1/R` — Ohm's law emerges directly from latency-limited gauge-fold transport. Non-ohmic behaviour (diodes, breakdown) is where the closure availability `W_ZFA` itself depends on the field, breaking linearity.

## 5. Joule heating = Landauer dissipation

A scattered hop is a closure that was **pruned** — and pruning is irreversible bit resolution. Each such event dumps the per-event `log 2` quantum ([MRE.md](MRE.md)) to the lattice bath as heat: `kT ln 2` per bit (Landauer), `ℏω` per bit in the quantum limit ([Information_Energy_Equivalence.md](Information_Energy_Equivalence.md) §4). Summed over the carrier stream, that dissipation **is** Joule heating:

$$P = I^2 R = (\text{irreversible closures/s}) \times kT\ln 2.$$

The demo reads this off: 1 W dissipated at 300 K corresponds to `3.48×10²⁰` irreversible `log 2` closures per second. Joule's law is QLF's information ledger paid out to the phonon bath.

## 6. Superconductivity = frequency-isolated coherent transport

If resistance is the cost of pruning, then zero resistance means **no pruning** — a transport channel with no scattering paths to fall into. That is precisely a **quiet frequency**: a transition whose linewidth is far below its centre frequency and whose coupling to the bath (phonons, flip-flops) is suppressed by symmetry or chemistry, i.e. a *deep Markov blanket* ([Crystal_QuantumOS.md](Crystal_QuantumOS.md) §2/§4, [VacuumEnergy.md](VacuumEnergy.md) §6.1). Inside such a ZFA-closed channel, `decoherence_impossibility` ([`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean), [Decoherence.md](Decoherence.md)) guarantees there is no admissible process that scatters the carrier out — so the current persists.

- **Cooper pairs** are two half-spin closures synchronized onto one coherent ZFA path — a single deep-blanket carrier the bath cannot resolve into its parts. That a two-half-spin pair is an integer-spin **boson** (so it can condense) is machine-verified: `cooper_pair_boson` ([`lean/QLF_CondensedMatter.lean`](lean/QLF_CondensedMatter.lean)), the same composite-spin fact as the photon (`boson_even_pairs`, [`QLF_Spin`](lean/QLF_Spin.lean)).
- **Critical temperature** is the blanket-depth threshold: below `T_c` the channel's isolation outweighs the thermal scattering rate.
- **Meissner effect / flux quantization** is ZFA-loop closure: a superconductor is a single macroscopic Context that folds its topology to stay ZFA-balanced, trapping flux in integer ZFA loops (`1 fluxoid ≡ 1 ZFA loop`, [Collective_Electrodynamics.md](Collective_Electrodynamics.md)).
- **Carbon.** The graphene superconductors, their lattice as a ZFA DNA, and pre-registered tests of the strange-metal rate, phase coherence and the pairing gap: [Carbon_Superconductivity.md](Carbon_Superconductivity.md). That document (§6, item 7) also notes a tension with this section. Here phonons are only the bath `T_c` must decouple from; in phonon-mediated superconductors (CaC₆) they are also the glue. A QLF reading would separate a phonon that closes jointly with the pair, inside its blanket, from one that prunes it from outside.

This is the **same mechanism as the quantum brain** ([TheQuantumBrain.md](TheQuantumBrain.md) §3): frequency-isolated coherence in a warm, noisy environment. A superconductor and a savant's resonant circuit are two faces of one thing — a bath-decoupled coherent ZFA channel. The demo shows the limit cleanly: with the field switched off, a normal channel's drift relaxes to ~0 (finite `R`) while a coherent quiet-frequency channel's drift persists at 1.0 (`R = 0`).

## 7. The quantum of resistance: `R_K = Z₀/(2α)`

Conductance comes in quanta of `G₀ = 2e²/h`; the resistance quantum (von Klitzing constant, the quantum-Hall plateau unit) is `R_K = h/e²`. Because `α = e²/(2 ε₀ h c)`,

$$R_K = \frac{h}{e^2} = \frac{1}{2\varepsilon_0 c\,\alpha} = \frac{Z_0}{2\alpha}, \qquad Z_0 = \mu_0 c \approx 376.730\ \Omega,$$

so **the quantum of resistance is the impedance of free space divided by `2α`**. The demo confirms `R_K = Z₀/(2α) = 25812.807 Ω` to a ratio of `1.00000000` against CODATA. In QLF this is not a coincidence: `α` is *derived from the substrate* — `α_QLF = 1/128 · (1+9α)⁻¹ = 1/137.000` to 0.026%, Lean-anchored as `alpha_QLF_eq` in [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) (canonical doc: [**Alpha.md**](Alpha.md); full prose [Magnetism_Spatial_Dynamics.md](Magnetism_Spatial_Dynamics.md) §6.1). The quantized resistance plateaus of the quantum Hall effect are therefore **the substrate's `α` made macroscopically visible**, scaled by the vacuum impedance — the most precisely measured resistance in metrology reading back the same combinatorial constant QLF computes from the 8-twist alphabet. This is machine-verified: `von_klitzing_substrate` ([`lean/QLF_CondensedMatter.lean`](lean/QLF_CondensedMatter.lean)) proves `R_K = Z₀/(2α) = Z₀·137/2` on the substrate α, with the integer-QHE plateaus `R_xy = R_K/ν` (`hall_resistance`). The BCS gap equation and topological band structure remain open (`condensed_matter_in_progress`); the *fractional* quantum Hall effect gets a first structural step in §7a.

## 7a. The fractional quantum Hall hierarchy — closures within closures

The **fractional** quantum Hall effect (FQHE) is a closures-within-closures tower, and its most famous law — the **odd-denominator rule** — follows from QLF closure *parity*. Computation: [`fqhe_hierarchy.py`](fqhe_hierarchy.py); Lean: [`QLF_FQHE`](lean/QLF_FQHE.lean).

In the composite-fermion picture (Jain 1989) each FQHE state is an electron with an **even** number `2s` of magnetic flux quanta attached, filling `p` composite-fermion Landau levels: `ν = p/(2sp ± 1)` (the Jain sequence). QLF reads the identical move as nested closures:

- **attaching one flux quantum = binding one even-pair fold = a boson closure** (`boson_even_pairs`, [`QLF_Spin`](lean/QLF_Spin.lean)); attaching `2s` of them nests `s` boson-closures inside the electron closure — a closure-of-closures (the `bind` fold of [`QLF_Consciousness`](lean/QLF_Consciousness.lean));
- **the composite must stay a fermion** (it is still an electron): fermion × boson = fermion, and fermion parity is **odd** (`fermion_odd_pairs`). This is *why* the attached flux count `2s` is **even** — an odd attachment would flip the statistics to bosonic and the state could not close as an electron;
- **therefore the denominator `2sp ± 1` is odd** (`2sp` is even). The odd-denominator rule of Abelian FQHE **is** the fermionic-closure parity.

The enumeration confirms the rule and its two falsifiable consequences:

1. **Every generated fraction is odd-denominator** — 23/23 across `s = 1,2` (forced: `2sp ± 1` with `2sp` even);
2. **the tower reproduces the observed principal fractions** — all 10 (`1/3, 2/5, 3/7, 4/9, 2/3, 3/5, 4/7, 5/9, 1/5, 2/7`);
3. **even-denominator states (`5/2, 7/2`) fall *outside* the fermion tower** — QLF reads them as a **paired (boson-paired) closure**, non-Abelian (Moore–Read Pfaffian), a *different* closure, not a parity violation. So the dichotomy **odd ⇔ unpaired fermionic / even ⇔ paired non-Abelian** is a prediction, and it matches the data exactly (no Abelian even-denominator state is observed; `5/2` and `7/2` are indeed the paired ones).

**The stability ordering is the closure-depth ordering** — now machine-checked ([`QLF_FQHE`](lean/QLF_FQHE.lean)). The frequency-hierarchy reading makes a falsifiable structural prediction for *which* states are most robust: the **closure depth** is the denominator `2sp ± 1` (how deep the nested tower goes; `jainDenom`), and deeper nesting = higher-frequency/deeper closure = **smaller gap = less stable**. The *ordering structure* is proven arithmetic: the depth is **odd** (`jainDenom_odd` — the odd-denominator rule again), it **strictly increases with the composite-fermion level `p`** (`jainDenom_depth_mono`), so higher-`p` states are deeper/less-stable; and **particle-hole partners `ν ↔ 1−ν` share the depth** — the partner of `p/D` is `(D−p)/D`, the same `D` (`particle_hole_same_depth`) — so they have ~equal gaps. Both predictions hold in experiment: the observed activation-gap ordering `1/3 ~ 2/3 > 2/5 ~ 3/5 > 3/7 ~ 4/7 > 4/9 …` is exactly the closure-depth ordering `3 < 5 < 7 < 9`, with `ν` and `1−ν` matched (`2/3 ~ 1/3`). **The one physical premise** — deeper = smaller gap — is named, not derived (as everywhere in QLF, the ordering is grounded and the absolute gap scale, Coulomb `e²/εℓ_B`, is the residual).

**Honest scope.** *Grounded:* the odd-denominator rule (closure parity), the odd/even ⇔ unpaired/paired dichotomy, and the **stability ordering** (gap decreasing with closure depth; particle-hole degeneracy) — all matching data. *Open* (`fqhe_hierarchy_in_progress`, the same 2D many-body boundary as [`QLF_Anyons`](lean/QLF_Anyons.lean)): the absolute **gap values** (the Coulomb scale `e²/εℓ_B` that sets the magnitudes) and the Laughlin/Jain many-body wavefunction — the many-body dynamics QLF's Lean does not yet carry. As everywhere in QLF, the *scaling/ordering* is grounded and the *absolute scale* is the residual. It complements [`QLF_Anyons`](lean/QLF_Anyons.lean)'s braiding phase (`laughlin_phase θ = π/m`) with the *filling-fraction* side.

## 8. What the demo shows

[`electricity_demo.py`](electricity_demo.py) (pure Python, ~2 s) backs the six claims numerically:

1. **Ohm's law** — `I` linear in `V` (fit `R² ≈ 0.999`).
2. **`R ∝ 1/W_ZFA`** — `R·W_ZFA ≈ 250` constant across `W = 1,2,4,8`.
3. **Superconductivity** — coherent quiet-frequency channel keeps drift = 1.0 with the field off; normal channel decays.
4. **Conductance quantum** — `G₀ = 77.4809 µS`, `R_K = Z₀/(2α) = 25812.807 Ω` (ratio `1.00000000`).
5. **Joule = Landauer** — 1 W at 300 K ↔ `3.48×10²⁰` `log 2` closures/s.
6. **Ampère** — `B = μ₀I/2πr` around a wire, and the circulation `∮ B·dl = μ₀ I` independent of radius (current builds the circulating spatial-axis count field).

## 9. Framing: one premise, then derivation

Granting the premise, the rest is derivation. Charge is the gauge-fold count; current is its transport; resistance is closure latency; Ohm, Joule, and superconductivity follow.

- **Lean-anchored:** charge / `∇·B = 0` (`no_magnetic_monopoles`); the substrate `α` (`alpha_QLF_eq`); coherence (`decoherence_impossibility`); the per-event `log 2` (`zfa_closure_minimizes_free_energy`, [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)).
- **Entailed by the premise:** resistance = `1/W_ZFA` latency (unified with time dilation and gravity); Ohm's law as its linear response; Joule heat = Landauer dissipation; superconductivity = quiet-frequency isolation; `R_K = Z₀/(2α)`.
- **Open quantitative targets:** first-principles carrier-scattering rates and `ρ(T)` for specific materials, and `T_c` from blanket-depth vs thermal scattering — open by *specification*, not by doubt about the mechanism. The Ampère/Faraday curl equations (`∇×B = μ₀J`, `∇×E = −∂B/∂t`) are now **machine-verified at the conservation level** on the time-indexed event sequence ([`QLF_MaxwellCurl.lean`](lean/QLF_MaxwellCurl.lean), #93): Faraday's boundary EMF telescopes to minus the net flux change (`faraday_integral`), so a closed magnetic cycle induces zero net EMF (`faraday_closed_cycle`); Ampère-Maxwell is the dual with source + displacement current (`ampere_integral`) — joining the already-verified divergence equations (the full 3-D vector `∇×` is the continuum rendering).

### Predictions and falsifiers

- **Shared latency.** A material's electrical relaxation time and its (gravitational/kinematic) clock latency are the same `1/W_ZFA` resource; anything that lowers carrier `W_ZFA` (disorder) raises resistance monotonically — a system where added scattering channels lower resistance would falsify the latency identity.
- **Superconductivity = bath decoupling.** `T_c` should track how decoupled the pairing channel is from the phonon bath (isotope effect, phonon-bandgap engineering as blanket-deepening); a superconducting channel demonstrably strongly bath-coupled would falsify the quiet-frequency reading.
- **Dissipation floor.** Irreversible charge resolution cannot dissipate less than `kT ln 2` per bit; a measured per-carrier dissipation below the Landauer floor would falsify the information-ledger account.

---

## References

### Internal

- [Maxwell.md](Maxwell.md) — charge `= count(+) − count(−)`; E/B fields from twists; `∇·B=0`, `∇·E=ρ/ε₀`; `J` as gauge-imbalanced thread flow
- [Conservation.md](Conservation.md) §4 — charge conservation; U(1) `=` `+`↔`−` swap
- [`lean/ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean) — `no_magnetic_monopoles` (`∇·B = 0`, charge conservation)
- [Time.md](Time.md) §2/§4, [SpaceTime.md](SpaceTime.md) §2 — latency `Δt ∝ 1/W_ZFA`; the resistance ↔ time-dilation unification
- [Curvature.md](Curvature.md) §3, [Gravity.md](Gravity.md) — gravity as the `W_ZFA` gradient; same latency as resistance
- [MRE.md](MRE.md), [Information_Energy_Equivalence.md](Information_Energy_Equivalence.md) §4 — per-event `log 2`; Landauer / `ℏω` per bit (Joule heating)
- [Crystal_QuantumOS.md](Crystal_QuantumOS.md) §2/§4, [VacuumEnergy.md](VacuumEnergy.md) §6.1 — quiet frequencies = deep Markov blankets (superconductivity)
- [Decoherence.md](Decoherence.md), [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean) — `decoherence_impossibility` (no scattering inside a ZFA-closed channel)
- [Collective_Electrodynamics.md](Collective_Electrodynamics.md) — superconductor as a unified Context; `1 fluxoid ≡ 1 ZFA loop`
- [TheQuantumBrain.md](TheQuantumBrain.md) §3 — the same frequency-isolation mechanism in the brain
- [Magnetism_Spatial_Dynamics.md](Magnetism_Spatial_Dynamics.md) §6.1, [`lean/QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) — `α` from substrate (`alpha_QLF_eq`); fixes `R_K = Z₀/(2α)`
- [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean) — `zfa_closure_minimizes_free_energy` (the per-event `log 2`)
- [`electricity_demo.py`](electricity_demo.py) — runnable companion (the six numerical checks above)

### External

- Ohm, G. S. (1827). *Die galvanische Kette, mathematisch bearbeitet.* — `V = IR`.
- Drude, P. (1900). *Zur Elektronentheorie der Metalle.* Ann. Phys. 306, 566 — `σ = nq²τ/m`.
- Landauer, R. (1961). *Irreversibility and heat generation in the computing process.* IBM J. Res. Dev. 5, 183 — `kT ln 2` per erased bit.
- Bardeen, J., Cooper, L. N. & Schrieffer, J. R. (1957). *Theory of superconductivity.* Phys. Rev. 108, 1175 — Cooper pairing.
- von Klitzing, K. (1980). *New method for high-accuracy determination of the fine-structure constant based on quantized Hall resistance.* Phys. Rev. Lett. 45, 494 — `R_K = h/e²` and its tie to `α`.

### See also

- [TheQuantumBrain.md](TheQuantumBrain.md) — frequency-isolated coherence applied to cognition
- [Curvature.md](Curvature.md) — the `1/W_ZFA` latency as gravity; resistance is its charge-transport face
- [README.md](README.md) — the convergence of independent programs on an informational, computable, closure-bounded reality
