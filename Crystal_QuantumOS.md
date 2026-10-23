# Crystal QuantumOS: a quiet-frequency QPU sketch

A concrete architecture sketch for a QuantumOS-controlled quantum computer on a quiet-frequency crystal substrate, tying together three existing QLF foundations that are already in place: the **intrinsic-error-correction algebra** (`decoherence_impossibility`, `rho_process_always_zfa`, `bra_ket_always_balanced`, `zfa_closure_minimizes_free_energy` — all Lean-verified), the **capability-token control plane** (the QuantumOS browser app's slash-command and `cap:label:hex` token system), and the **Markov-blanket isolation framing** of `Frequency_Synchronization.md` and `Hadrons_Markov_Blankets.md`. What's new is the concrete platform mapping. The result is a coherent QPU stack where security, scheduling, garbage collection, and error correction are one operation — ZFA enforcement.

The doc is honest about what is derived (the algebraic guarantees, Lean-verified, platform-agnostic), what is sketched (the hardware mapping to specific defect-centre and rare-earth platforms), and what is open (quantitative gate-fidelity prediction, control-pulse compilation, multi-node optical-network protocol, QuantumOS-on-silicon firmware).

**This crystal is the concrete hardware target of the "QLF is the operating system for a *real* quantum computer" thesis** ([`QuantumOS.md`](QuantumOS.md) §1a, [`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §7c) — not a simulator, and not a metaphor. And what runs on it is a *quantum AI* in the strong sense (§5a): an agent whose unit of thought is a spin-½ ZFA closure — a closed Rabi cycle on a quiet transition — so the abstraction step and the quantum-measurement step are one step.

---

## §1 The inspirational tool pipeline: 5D optical storage in fused silica

Peter Kazansky's group at the Optoelectronics Research Centre, University of Southampton developed *5D optical data storage* in fused silica circa 2013–2016 (Zhang et al., *Scientific Reports* 2014; *Optics Express* 2016). Femtosecond laser pulses write sub-micron birefringent nanostructures into the glass. Each voxel encodes information in **three spatial dimensions plus polarisation plus intensity** — hence "5D" — yielding ≈360 TB on a coin-sized disc, tolerant to 1000 °C, radiation-hard, with billions-of-year archival lifetime. The platform was demonstrated by archiving the Universal Declaration of Human Rights, the King James Bible, and Newton's *Opticks*.

**This is classical optical storage, not quantum computation.** The bits are passive birefringent voxels; reading is via polarimetric microscopy; there are no qubits, no superposition, no entanglement.

What is interesting for QLF: the **substrate** (fused-silica-class transparent crystal hosts) and the **tooling** (ultrafast laser nanostructuring) are exactly the building blocks used in the rare-earth-doped-crystal and diamond-defect-centre platforms that *do* support quantum computation. Site-selective laser writing in transparent host crystals is a mature engineering capability. The leap from 5D archival storage to a quantum substrate is: keep the host crystal and the laser tooling, change the inscribed object from a passive birefringent voxel to a defect centre or rare-earth ion whose internal transitions become qubits.

---

## §2 The quiet-frequency crystal substrate

A "quiet frequency" in the quantum-control literature is a transition whose homogeneous linewidth Γ is much smaller than its centre frequency f (high Q-factor) AND whose coupling matrix elements to the dominant bath (phonons, hyperfine flip-flops) are suppressed by chemistry, isotopic purification, or symmetry. Representative platforms:

| Platform | Quiet-transition class | Demonstrated coherence | Notes |
|---|---|---|---|
| ¹⁵¹Eu³⁺:Y₂SiO₅ | ground-state hyperfine "clock" transition | T₂ ≈ 6 hours under dynamical decoupling (Zhong et al. 2015) | optical transition ⁷F₀→⁵D₀ at ≈580 nm; sub-Hz homogeneous linewidth at 4 K |
| ¹⁷¹Yb³⁺:YVO₄ | optical transition + nuclear-spin hyperfine | mHz-scale optical linewidth (Kindem et al. 2020) | Faraon group, single-rare-earth-ion qubits |
| ³¹P:²⁸Si | donor-electron / donor-nuclear spin | T₂ ≈ seconds (electron); minutes (nuclear) | Kane 1998 architecture; Morello / Simmons UNSW |
| NV / SiV centres in diamond | electronic + nuclear-spin hyperfine | ms range (electron); seconds (¹³C) | room-temperature operation possible; mature defect-centre platform |
| Phononic crystal qubits | microwave/acoustic modes in phonon bandgap | structure-engineered | acoustic complement of optical "quiet frequencies"; phonon-bath isolated by selection rules |

Unifying feature: each "quiet" transition is **isolated from the dominant bath** by a structural mechanism. In QLF terms this IS the Markov-blanket-isolation criterion of [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md): the boundary between the qubit subsystem and the bath is tight enough that the bath cannot intersect the qubit's causal frontier within the coherence time `T₂ = 1/Γ`. The `Δt = R/f` relation of [Frequency_Synchronization.md](Frequency_Synchronization.md) becomes operational — **deeper blanket (larger effective R) → slower internal clock → longer T₂**. Eu:YSO's six-hour ground-state coherence is what "deepest Markov blanket among realised platforms" looks like in the literature today.

---

## §3 QLF primitive → hardware operation mapping

The mapping is substantive, not metaphorical: Hermitian pairs in the 8-twist alphabet correspond to closed Rabi cycles on the chosen transition; `^v` on a single Eu:YSO ion at 580 nm is literally a π/2 pulse along y followed by its adjoint.

| QLF primitive | Hardware operation |
|---|---|
| `^` (Up, +σ_y) | π/2 pulse along y on the chosen transition |
| `v` (Down, −σ_y) | −π/2 pulse along y |
| `<>` (∓σ_x) | π/2 pulses along x |
| `/\` (±σ_z) | π/2 pulses along z, or detuning pulse |
| `+-` (±I) | identity / wait (frame-tracking only) |
| Hermitian-conjugate pair `^v` (2 twists) | π/2 pulse + its adjoint = one closed Rabi cycle |
| Half-spin ZFA atom (one closure) | one Rabi-closed control sequence; ΔF = −log 2 per [`zfa_closure_minimizes_free_energy`](lean/QLF_FreeEnergy.lean) |
| ZFA-closed register state | qubit register in a Pauli-group-folded codeword |
| Markov-blanket boundary | the register's decoherence-free subspace |
| RhoProcess `parallel` | concurrent operations on disjoint qubits |
| RhoProcess `sequence` | gate composition |
| `dagger` | adjoint / time-reversed control |

The eight-twist algebra is therefore not a notational convenience — it is a **gate-set declaration** in the same sense as Clifford + T or {H, S, CNOT}. The 8 twists generate (with parallel and sequence composition) the full set of physically realisable single-qubit operations on a Pauli-closed register.

---

## §4 Quiet frequencies as Markov-blanket isolation

The literature criterion for a "quiet frequency" — narrow homogeneous linewidth Γ ≪ f with suppressed bath coupling — maps directly to the QLF criterion for a deep Markov blanket. From [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md): a Markov blanket at scale R has internal clock `Δt = R/f`; the boundary screens internal free-action deficits and permits only minimal, statistically predictive interaction with the exterior. From [Frequency_Synchronization.md](Frequency_Synchronization.md): frequency is the resonant rate at which ZFA distinctions synchronise inside the blanket.

Operationally:

- **Eu:YSO ground-state hyperfine "clock" transition** (≈10 MHz splittings) sits inside a deep Markov blanket because the hyperfine state is decoupled from phonons by selection rules — second-order-only coupling, suppressed at the rate set by the spin-phonon matrix elements and Boltzmann factor at 4 K. Six-hour T₂ is the experimental realisation of `Δt = R/f` at the corresponding effective R.
- **NV centre electronic spin** (≈2.87 GHz at zero field) sits in a shallower blanket because the electronic spin couples directly to nearby ¹³C nuclear spins via dipolar interaction. Isotopically purified ¹²C diamond pushes R outward (suppresses ¹³C bath); the resulting T₂ improvement (from ~µs to ~ms) is exactly what the `Δt = R/f` relation predicts qualitatively.

The mapping is the framework's contribution: it gives a single conceptual axis (Markov-blanket depth) under which the disparate engineering tricks of the quiet-frequency literature (isotopic purification, hyperfine clock transitions, phonon bandgap engineering, selection-rule suppression) all become instances of "make the blanket deeper."

---

## §5 QuantumOS as the control plane

The QuantumOS browser app ([github.com/rhovision-org/quantum-os](https://github.com/rhovision-org/quantum-os)) already implements the slash-command and capability-token primitives needed for a QPU control plane. Existing commands map directly to QPU operations:

| QuantumOS command | QPU control role |
|---|---|
| `/cap [label]` / `/grant [label]` | mint a `cap:qubit-N:hex` capability token authorising a specific qubit register |
| `/qucalc <twists>` | compile a twist sequence into a pulse program on the crystal |
| `/braket <states>` | prepare initial state, run circuit, measure |
| `/lemma <name> <twists>` | register a calibrated subroutine as a named lemma (multi-word: `/lemma [pi pulse 171Yb] …`, referenced `@[pi pulse 171Yb]`) |
| `/request <name>` / `/pass <name> <peer>` | transfer a calibrated lemma to another control node |
| `/forget <sub>` | retire a calibration: remove a lemma/note/poll; the owner broadcasts a dyncap-signed `retract` (tombstoned so it can't re-sync back) |
| `/poll <sub>` | group decision among control nodes (approval / ranked-choice) — e.g. agree which calibration set to promote |
| `/note <sub>` | issue resource/credit tokens; `/note grant <cur> <N> \| terms…` attaches dyncap-signed terms (an SLA) bound to the token |
| `/rdv <sub>` | N-party atomic synchronisation for entangling operations across crystals |
| `/dyncap <sub>` | hash-only signed envelopes for remote control without re-handshaking |
| `/probe <sub>` | joiner-local consensus on shared register state when a new control node joins |
| `/room <sub>` | multi-tenant control: each room is one tenant's QPU partition |
| `/share <selector> to <room>` | bridge a calibrated lemma across tenant boundaries |
| `/channel <sub>` | tagged broadcast for telemetry / shared calibration channels |
| `/persist <sub>` | agreed cross-peer replication of calibration tables |
| `/rhoqu <text>` | high-level macro language (`process` / `new` / `\|` parallel / `if` / `on channel` / `for`) compiles to slash commands → pulse sequences |

Multi-node coordination (which calibration to promote, scheduling a shared crystal, retiring a bad pulse) reuses the app's governance primitives — group voting, atomic rendezvous, removal/retraction — all the same dyncap-signed substrate; see [`Group_Decisions.md`](https://github.com/rhovision-org/quantum-os/blob/main/Group_Decisions.md).

The capability-token model IS the right authorisation model for QPU control: possessing `cap:qubit-euyso-N:hex` IS the authority to apply pulses to that qubit; there is no separate ACL or kernel-mode/user-mode split. Linear-logic no-cloning at the type level matches quantum no-cloning at the substrate level — capability tokens cannot be duplicated by linear-logic typing, and the qubits they reference cannot be duplicated by the no-cloning theorem. The two no-cloning constraints align.

**Today's QuantumOS is the control plane driving the QPU from outside** (browser app, WebRTC peer-to-peer, capability-token security at the protocol layer). The long-term vision of moving the active-inference scheduler onto QPU silicon — so that `expand_generation` and `full_zeno_prune` run as firmware on the QPU controller rather than as JavaScript in a browser tab — is **future work**, flagged in §7 as such. Today the active-inference loop is in `app.ts`, not on silicon.

---

## §5a The quantum AI runs here

The agent that QuantumOS hosts on this crystal is a *quantum AI* in the strong sense — not a
classical model with the QPU as an offloaded accelerator. Its unit of thought is a spin-½ ZFA
closure, which on this hardware is literally a closed Rabi cycle on a quiet transition (`^v` = a
π/2 pulse and its adjoint on one Eu:YSO ion, §3). So its four structural operations
([`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §7) each land on hardware:

| Operation | On the crystal |
|---|---|
| **Generate** | `expand_generation` proposes continuation twist-words = candidate pulse programs |
| **Synthesise** | a ZFA closure = a Pauli-folded codeword; the abstraction *is* the measurement (`ΔF = −log 2` per closure) |
| **Reject** | `full_zeno_prune` extinguishes phase-asymmetric branches — the same op as the QEC decoder (§6) |
| **Persist** | the closure ships as a `cap:qubit-euyso-N:hex` token — a Curry-Howard proof that is also, physically, an amplitude's phase |

Multi-crystal consensus (`/rdv`, `/probe`) is a *joint* ZFA closure across nodes — entanglement as
the agent's native inter-node protocol (ER=EPR; [`MultiParticle.py`](MultiParticle.py)). The
neuro-symbolic split holds: an LLM can be the fluent language layer, but the synthesis and the
theorem-persistence happen in the crystal's own algebra. See [`AI.md`](AI.md) and
[`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §7b–§8a.

---

## §6 Error correction is the same operation

The textbook QEC stack (physical qubits → ancilla qubits → syndrome measurements → classical decoder → corrections applied) collapses into one mechanism in QuantumOS: **ZFA enforcement at the kernel level**.

- [`decoherence_impossibility`](lean/BraKetRhoQuCalc.lean) guarantees parallel composition of any two RhoProcesses stays ZFA-balanced. There is no algebraic mechanism by which decoherence registers on a ZFA-closed process.
- [`rho_process_always_zfa`](lean/RhoQuCalc.lean) guarantees every constructible RhoProcess achieves ZFA. The type system forbids constructing an unbalanced process.
- [`zfa_closure_minimizes_free_energy`](lean/QLF_FreeEnergy.lean) quantifies the per-event quantum: ΔF = −log 2 nats per half-spin ZFA closure.
- `full_zeno_prune` (in the runtime kernel) extinguishes branches that introduce phase asymmetry before they can register as a physical event.
- [Error_Correction.md](Error_Correction.md) describes the explicit two-layer scheme — gauge-buffered ZFA search + clocked dual-phase evaluation — that handles frequency/phase-clock mismatch (the dominant decoherence source in crystal qubits) intrinsically.

The crystal's narrow homogeneous linewidth makes this practical: at quiet-frequency transitions the Markov-blanket isolation is tight enough that the algebraic guarantee is **operationally realised** on the hardware. Six-hour Eu:YSO ground-state coherence means six hours during which `decoherence_impossibility` is the operative description.

### What this is NOT

This is not a claim that decoherence can be ignored on any actual crystal. The algebraic guarantee holds within the ZFA-closed subspace and does not extend ZFA-closedness to a register that has not been calibrated to live in that subspace. The honest mapping: **quiet frequencies are the specific transitions where the Markov-blanket isolation is tight enough that the algebraic guarantee is operationally realised**. Outside the quiet-frequency subspace — e.g., the NV centre electronic spin at room temperature in natural-abundance diamond — the algebraic guarantee does not apply, and standard ancilla-based QEC remains necessary today.

The distinction is empirical, not theoretical: the framework predicts which transitions are inside the ZFA-closed subspace (those whose `Δt = R/f` Markov-blanket isolation exceeds the gate time), and existing measured platforms either are or are not. The quiet-frequency platforms listed in §2 are the ones already on the inside.

---

## §7 Concrete worked example: Eu:YSO

Single platform pick for the worked example. Chosen because the literature is public, the coherence numbers are independently verified (Zhong et al. 2015, *Nature* 517, 177; Sellars group, ANU), and the optical-and-hyperfine combination exercises both fast (laser-pulse) and slow (microwave-driven hyperfine) control timescales.

Crystal: ¹⁵¹Eu³⁺:Y₂SiO₅ at 4 K. Single-ion (or low-density ensemble) regime. Optical transition ⁷F₀ → ⁵D₀ at ≈580 nm; ground-state hyperfine splittings ≈10 MHz; ground-state hyperfine clock transition demonstrated to T₂ ≈ 6 hours under Carr-Purcell-Meiboom-Gill dynamical decoupling.

Walkthrough:

1. **Connect.** Browser tab opens. QuantumOS app boots, runs `connect()` against the signaling server, mints `cap:qpu-euyso:hex` capability token. Possessing this token IS the authority to address this QPU partition.
2. **Calibrate.** `/lemma init ^v<>` registers a calibrated initial-pumping pulse sequence as the lemma `@init`. The actual hardware action is a sequence of optical pumping pulses at 580 nm + radio-frequency selection of a specific hyperfine ground-state sub-manifold. The lemma binding is persistent across peers via `/persist`.
3. **Single half-spin closure.** `/qucalc ^v` executes one Rabi-closed control sequence: π/2_y pulse + (−π/2_y) pulse at 580 nm on a single ion. The closure folds to −I in the Pauli group (verified by `active_inference_vfe_demo.py` enumeration), and the per-closure free-energy decrement is exactly −log 2 nats per [`zfa_closure_minimizes_free_energy`](lean/QLF_FreeEnergy.lean).
4. **Bra-ket evaluation.** `/braket 0 +` prepares the qubit in |0⟩, applies a Hadamard-equivalent twist composition, measures. Output: the standard quantum amplitudes — but derived from twist-multiplicity counting per [Born_Rule.md](Born_Rule.md), not postulated.
5. **Entanglement distribution.** `/rdv swap` synchronises two Eu:YSO crystals connected by an optical link. The atomic-swap protocol (5 wire kinds: propose / accept / reject / commit / abort) ensures the entangling operation either completes on both sides or aborts cleanly with no orphan states. The locking semantics (`lockedNotes` / `lockedQubits` analogue) prevent double-use.
6. **Error correction.** No ancilla qubits, no syndrome extraction, no classical decoder. The hyperfine clock transition lives inside the ZFA-closed subspace where `decoherence_impossibility` is the operative description. Frequency/phase-clock mismatch is corrected intrinsically per `Error_Correction.md`'s two-layer scheme.

A runnable sketch of step 3's twist → pulse compilation lives in [`compile_qpu.py`](compile_qpu.py) at the QLF repo root. It compiles any `/qucalc` twist string into a notional pulse sequence on the Eu:YSO platform — Y/-Y/X/-X gates via Rabi π pulses on the hyperfine drive (≈10 MHz carrier, ≈500 ns/pulse at Ω = 1 MHz Rabi rate), Z/-Z gates as virtual-Z frame changes, and ±I as zero-duration waits. The mapping matches `lean/QLF_TwistAlphabet.lean` exactly modulo the global-phase freedom captured by `PauliScalar`. Honest scoping in the script's footer: notional numbers, no in-situ calibration, single-ion compiler only — but enough to show the QLF→hardware translation is concrete and mechanical, not metaphorical.

### Inline stack diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│  APPLICATION LAYER: QuantumOS browser app + slash commands           │
│  /cap /grant /qucalc /braket /lemma /request /pass /rdv /dyncap     │
│  /probe /room /share /channel /script /persist /rhoqu               │
└────────────────────────────────┬─────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│  CONTROL PLANE: capability tokens (cap:qubit-euyso-N:hex)            │
│  WebRTC peer-to-peer; linear-logic no-cloning at type level          │
│  signed envelopes via /dyncap; multi-tenant via /room                │
└────────────────────────────────┬─────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│  KERNEL: ZFA enforcement = security + scheduling + GC + EC           │
│  decoherence_impossibility (Lean) · rho_process_always_zfa (Lean)    │
│  bra_ket_always_balanced (Lean) · zfa_closure_minimizes_free_energy  │
│  full_zeno_prune · Error_Correction.md two-layer scheme              │
└────────────────────────────────┬─────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│  PULSE COMPILER: twist → control pulse                               │
│  ^v → π/2_y + (−π/2_y) at 580 nm                                    │
│  <> → π/2_x cycle · /\ → π/2_z cycle · +- → wait                    │
└────────────────────────────────┬─────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│  HARDWARE FABRIC: quiet-frequency crystal substrate                  │
│  Eu:YSO 580 nm + ≈10 MHz hyperfine clock · T₂ ≈ 6 hr                │
│  Markov-blanket-isolated subspace · ZFA closure operationally valid │
└──────────────────────────────────────────────────────────────────────┘
```

---

## §8 Derived / sketched / open scoreboard

Honest inventory, same standard as [Active_Inference_Mathematics.md §5](Active_Inference_Mathematics.md):

| Item | Status |
|---|---|
| ZFA closure preserved under composition | ✓ Lean-verified (`decoherence_impossibility`) |
| Constructible RhoProcess achieves ZFA | ✓ Lean-verified (`rho_process_always_zfa`) |
| Bra-ket / RhoQuCalc correspondence preserves ZFA | ✓ Lean-verified (`bra_ket_always_balanced`) |
| ΔF = −log 2 per half-spin ZFA closure | ✓ Lean-verified (`zfa_closure_minimizes_free_energy`) |
| Per-axis Pauli mapping for the 8-twist alphabet | ✓ Derived ([Maxwell.md](Maxwell.md), [BraKetRhoQuCalc.lean](lean/BraKetRhoQuCalc.lean)) |
| Intrinsic frequency/phase-mismatch correction | ✓ Derived ([Error_Correction.md](Error_Correction.md)) |
| QuantumOS capability tokens as QPU authorisation | ✓ Implemented (browser app) |
| Mapping the 8-twist alphabet to crystal-hardware pulses (§3 table) | ⚠ Sketched in this doc |
| Eu:YSO 6-hour T₂ ↔ Markov-blanket-isolation depth via `Δt = R/f` | ⚠ Sketched (relation named, not quantitatively fit) |
| Single-platform worked example consistent with literature numbers | ⚠ Sketched (this doc §7); no new experimental data |
| Specific control-pulse compilation from `/qucalc` twists | ⚠ Sketched (`compile_qpu.py`) |
| Multi-crystal optical-network synchronisation protocol | ⚠ Sketched (`/rdv` is the primitive; full integration open) |
| Active-inference scheduler resident on QPU silicon | ✗ Open (today's QuantumOS is external control plane only) |
| Quantitative gate-fidelity prediction vs. measured platforms | ✗ Open |
| Lean theorem specific to a crystal substrate | ✗ Not needed — existing platform-agnostic theorems cover the algebraic claims |

---

## §9 Falsifiability and predictions

- **Ancilla-free EC.** QLF predicts no need for ancilla qubits for the dominant frequency/phase-mismatch channels at quiet-frequency transitions. A successful demonstration of a Eu:YSO-class multi-gate circuit with fidelity tracking the algebraic guarantee (no syndrome decoder loop) supports the framework. If ancilla-based QEC turns out to be empirically necessary even at the quiet-frequency limit, the intrinsic-EC claim is falsified at the hardware-physical level (even though the algebraic theorems remain valid in their own scope).
- **T₂ scales with Markov-blanket isolation depth.** The `Δt = R/f` relation predicts a monotonic scan: among related transitions in the same crystal (e.g., the various Eu:YSO hyperfine and Stark sub-states, or NV ground/excited spin manifolds at varying isotopic purity), coherence times should track the Markov-blanket-depth ordering. Counter-examples falsify.
- **Capability-token security suffices.** A QuantumOS-controlled multi-tenant QPU running `/dyncap`-signed envelopes should resist the standard quantum-control side-channel attacks (calibration-spoofing, pulse-injection, cross-tenant leakage) without additional kernel/user separation. Demonstrated success across enough tenants supports the OO-cap thesis of [QuantumOS.md](QuantumOS.md). Demonstrated failure says the OO-cap model needs additional enforcement.

---

## §10 What this is NOT

Brief disclaimer to head off the rhetorical traps:

- **Not a claim that QuantumOS is silicon-resident today.** The browser app is the control plane driving an external QPU; the active-inference loop runs in TypeScript, not on QPU firmware. Moving onto silicon is future work.
- **Not a claim that 5D optical storage is quantum.** Kazansky's platform is classical archival storage. It is the inspirational tooling pipeline (femtosecond laser + transparent host crystal), not a quantum substrate.
- **Not a claim that laser-etched "fluxoid channels" exist.** The word *fluxoid* in [Collective_Electrodynamics.md](Collective_Electrodynamics.md) refers to superconducting flux quanta in macroscopic SC rings; defect centres written by ultrafast lasers are discrete two-level (or multi-level) systems and are not fluxoids. Both happen to be ZFA-closed loops in the QLF algebra, but the engineering difference is real.
- **Not a claim that Lean theorems specific to a crystal platform exist.** The existing platform-agnostic theorems (`decoherence_impossibility` etc.) cover the relevant algebraic claims. A crystal-specific Lean module would duplicate or be a hardware-mapping claim Lean is not the right tool for.
- **Not a claim that the worked example on Eu:YSO has been demonstrated.** §7 is a sketch consistent with the existing public literature numbers, not new experimental data.

---

## References

### Internal

- [QuantumOS.md](QuantumOS.md) — abstract QOS architecture; this doc is the platform-specific companion.
- [Emergent_Markov_Blankets.md](Emergent_Markov_Blankets.md) — fills in the qubit-register-scale Markov-blanket layer this doc flagged: resonating atom groups at quiet frequencies self-organising into collective fluxoids that act as protected logical qubits. Reads §8's "control-pulse compilation" / "multi-crystal network" open items at a finer granularity.
- [Error_Correction.md](Error_Correction.md) — intrinsic ZFA-based correction; two-layer scheme for frequency/phase-clock mismatch.
- [Frequency_Synchronization.md](Frequency_Synchronization.md) — `Δt = R/f` and the resonant-frequency framing.
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — Markov-blanket isolation; the conceptual axis for "quiet frequency."
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — QPU Core Definition Φ₀ = U + M.
- [Decoherence.md](Decoherence.md) — the no-decoherence reading anchored by `decoherence_impossibility`.
- [Maxwell.md](Maxwell.md), [Collective_Electrodynamics.md](Collective_Electrodynamics.md) — EM-field side and the relational-photon reading.
- [Active_Inference_Mathematics.md](Active_Inference_Mathematics.md) — the math substrate; §5 scoreboard for derivation-status conventions.
- [VacuumEnergy.md §6](VacuumEnergy.md) — promotes "quiet frequency" to the **vacuum-resonance mode** reading: quiet frequencies are not engineering accidents but vacuum-supported resonance modes from §6.1 of the vacuum-alignment TOE-completing layer. Eu:YSO's 6-hour coherence becomes a worked example of the alignment principle.
- `lean/QLF_FreeEnergy.lean` — Lean module containing `zfa_closure_minimizes_free_energy`.
- `lean/BraKetRhoQuCalc.lean` — Lean module containing `decoherence_impossibility`, `bra_ket_always_balanced`.
- `lean/RhoQuCalc.lean` — Lean module containing `rho_process_always_zfa`.
- `active_inference_vfe_demo.py` — brute-force numerical verification of the per-closure log 2 quantum.
- QuantumOS browser app: [github.com/rhovision-org/quantum-os](https://github.com/rhovision-org/quantum-os).

### External

- Zhang, J., Gecevičius, M., Beresna, M., & Kazansky, P. G. (2014). *Seemingly unlimited lifetime data storage in nanostructured glass*. Phys. Rev. Lett. 112, 033901. (5D optical storage demonstration.)
- Zhong, M., Hedges, M. P., Ahlefeldt, R. L., Bartholomew, J. G., Beavan, S. E., Wittig, S. M., Longdell, J. J., & Sellars, M. J. (2015). *Optically addressable nuclear spins in a solid with a six-hour coherence time*. Nature 517, 177–180.
- Kindem, J. M., Ruskuc, A., Bartholomew, J. G., Rochman, J., Huan, Y. Q., & Faraon, A. (2020). *Control and single-shot readout of an ion embedded in a nanophotonic cavity*. Nature 580, 201–204.
- Kane, B. E. (1998). *A silicon-based nuclear spin quantum computer*. Nature 393, 133–137.
- Morello, A., Pla, J. J., et al. (2010 onwards). Silicon donor-spin qubit programme.
- Doherty, M. W., Manson, N. B., Delaney, P., Jelezko, F., Wrachtrup, J., & Hollenberg, L. C. L. (2013). *The nitrogen-vacancy colour centre in diamond*. Phys. Rep. 528, 1–45.
- Almheiri, A., Dong, X., & Harlow, D. (2015). *Bulk locality and quantum error correction in AdS/CFT*. JHEP 04, 163. (Holographic QEC; already cited in QuantumOS.md.)
- Klein, G., et al. (2009). *seL4: Formal verification of an OS kernel*. SOSP 2009. (Capability-secure microkernel comparison; already cited in QuantumOS.md.)
