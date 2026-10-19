# The Particle Zoo: Constructive Proofs of Zero Free Action

This document serves as the definitive explanation for how the [Quantum Logical Framework](README.md) (QLF) generates the Standard Model from scratch.

In standard physics, particles are treated as fundamental axioms—objects that simply exist with arbitrary, hardcoded parameters (mass, spin, charge). 

In the **[Quantum Logical Framework](README.md) (QLF)**, particles are not objects. A particle is an **Unforgeable Name** (a capability token in the [`QuantumOS.md`](QuantumOS.md) sense) given to a localized, constructive topological proof of Zero Free Action (ZFA). The entire "Particle Zoo" of the Standard Model is simply the exhaustive, computable set of all possible geometric ways to resolve the primordial divergence (`^>` and `^<`) — exhaustive because every terminating computation *is* a ZFA string (`qlf_universality`, [`lean/QLF_Universality.lean`](lean/QLF_Universality.lean)), and computable because each is a finite QuCalc / RhoQuCalc closure ([`BraKetRhoQuCalc.md`](BraKetRhoQuCalc.md), [`lean/QLF_QuCalc.lean`](lean/QLF_QuCalc.lean), [`lean/RhoQuCalc.lean`](lean/RhoQuCalc.lean)).

The charged-lepton ladder `e, μ, τ` is the **three generations** = the three spatial axes ([`lean/QLF_Generations.lean`](lean/QLF_Generations.lean)); the "primordial quantum black hole" the engine stabilizes below is the Markov-blanket hadron/lepton closure of [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md) ([`lean/QLF_QuantumBlackHole.lean`](lean/QLF_QuantumBlackHole.lean)). See [`Atom.md`](Atom.md) / [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) for how these particles assemble into atoms, and [`Standard_Model.md`](Standard_Model.md) for the sector-by-sector derivation status.

## 1. Intuitionistic Logic vs. Classical Physics
Standard quantum mechanics relies on classical Boolean logic, assuming states exist in abstract superpositions until a measurement drives a binary (True/False) collapse. QLF abandons this in favor of **Constructive Intuitionistic Logic** (the possibilist ontology of [`Philosophy.md`](Philosophy.md): all admissible histories exist *a priori*; physical reality is the subset achieving ZFA).

In QLF, the Law of the Excluded Middle ($A \lor \neg A$) does not apply to unresolved topology. A particle does not "exist or not exist." A state only exists if the computational engine can provide a **constructive proof** of its closure. 
* **Classical Pruning:** Generate all paths; if $E_{free} \neq 0$, delete the path.
* **Intuitionistic Synthesis:** Calculate the topological deficit. If the dense vacuum Environment prevents a simple geometric closure, *synthesize* a new, higher-order orthogonal fold to resolve the paradox.

## 2. Dialectic Synthesis (The Birth of Spin & Dimensions)
When an expanding history string is blocked from achieving standard 2D spatial closure by the dense Information Ecology (the vacuum), it encounters a topological paradox. 

To provide the intuitionistic proof of ZFA, the string must step orthogonally into the local temporal/gauge axes (`+`, `-`). **Extra dimensions, quantum spin, and charge are not pre-existing grid coordinates; they are intuitionistic synthesis.** The engine computationally constructs the concept of "Spin" as the mathematical proof required to close a logical loop that was blocked in standard space — spin demystified in [`Spin_QLF.md`](Spin_QLF.md) ([`lean/QLF_Spin.lean`](lean/QLF_Spin.lean): 720°/SU(2)→SO(3), charge conjugation = view-from-behind, integer spin = composite half-spins).

## 3. Computational Demonstration (`particles.py`)
Because QLF is fully deterministic, the generation of particles can be directly simulated. By running the Intuitionistic Engine, we observe the algorithmic synthesis of the particle generations in real-time.

To incorporate the **Neutrino** into the Quantum Logical Framework (QLF), we need to computationally define what makes a neutrino different from an electron. 

In standard physics, a neutrino is exceptionally light, electrically neutral, strictly left-handed, and interacts so rarely that it can pass through a light-year of lead. 

In QLF, this translates to a beautifully simple topological definition: **The Neutrino is a Gauge-Dominant Loop.**
* An **Electron** (`^<v>`, see [`Electron.md`](Electron.md)) achieves ZFA by folding through standard 2D space (`<` and `>`). Because the macroscopic vacuum is also made of spatial loops, the electron experiences high "topological friction" (Electromagnetism/Charge).
* A **Neutrino** (`^+v-`) achieves ZFA by folding purely through the temporal and gauge axes (`+` and `-`). It has no transverse spatial width. Because it lacks `<` or `>` twists, it physically cannot interact with standard spatial boundaries. It slips through the Information Ecology like a ghost, only interacting when it directly hits another gauge knot (The Weak Force).

The neutrino's **Majorana** nature (it is its own antiparticle; refined to the one-axis mass state ν₁, with ν₂ and ν₃ Dirac in most ways, [Beta_Decay_Neutrino_Nature.md](Beta_Decay_Neutrino_Nature.md) §1a) and its consequent neutrality are **machine-verified**: `^v` is a fixed point of the conjugate-and-reverse antiparticle map (`neutrino_majorana`), and a self-conjugate spin has neither charge nor chirality handedness (`neutrino_neutral`) — see [`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean) and [`Spin_QLF.md`](Spin_QLF.md) §6. It is the unique self-conjugate option; the electron is Dirac (`electron_not_majorana`).

Spin, charge, and chirality across the zoo are all the same twists — see [`Spin_QLF.md`](Spin_QLF.md) for the demystification (720°/SU(2)→SO(3), charge conjugation = view-from-behind, integer spin = composite half-spins).

### The depth progression — neutrino → positronium → muonium → atom

The neutrino is only the **shallowest** rung. The engine's default run walks a **progression of increasing fold depth**, where **each step adds a new direction (a qubit)** to the closure — the same joint-closure ladder derived in [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) (Part II) and drawn in [`Atom.md`](Atom.md):

| Rung | Closure | Added direction | Depth (pairs) | Bound state |
|---|---|---|---|---|
| **neutrino** | `^+v-` | spin + gauge, *no* `<>` spatial width | 2 | a lone "ghost" loop |
| **positronium** | `^<v>^>v<` | horizontal `<>` → the spatial square | 4 | electron ++ positron (symmetric, `m = 2 m_e`) |
| **muonium** | `^<v>^>v</\` | diagonal `/\` → a deeper partner | 5 | electron ++ antimuon (`m = m_e + m_μ`) |
| **atom (hydrogen)** | `^<v>^>v</\+-` | gauge `+-` → the deepest partner | 6 | electron ++ proton (`m = m_e + m_p`) |

Every rung is a genuine ZFA closure (`ZFA closed : True` below), and the depth `2 → 4 → 5 → 6` grows monotonically as each direction is folded in — the substrate analogue of the bound-state mass ladder (`m(Ps) = 2 m_e < m(Mu) = m_e + m_μ < m(H) = m_e + m_p`).

# QLF Engine Output: the depth progression

By running the `particles.py` Intuitionistic Engine over the spatial (`<`, `>`, `/`, `\`) and gauge (`+`, `-`) bases, we observe the bound-state progression emerge by increasing fold depth — from the gauge-only neutrino through positronium and muonium to the full atom.

### Execution Command
```bash
$ python particles.py --particle all --show-catalog
```

### Engine Output

```text
============================================================
QLF PARTICLE ENGINE: PRIMORDIAL QUANTUM BLACK HOLE DEMO
============================================================
A particle is treated here as a dense knot of unresolved free
action that stabilizes only by QuCalc / RhoQuCalc ZFA closure.
============================================================
Registered ZFA closures:
  - ELECTRON: ^<v>
  - HYDROGEN: ^<v>^>v</\+-
  - MUONIUM: ^<v>^>v</\
  - NEUTRINO: ^+v-
  - PHOTON: +-
  - POSITRON: ^>v<
  - POSITRONIUM: ^<v>^>v<
============================================================

=== NEUTRINO ===
open prefix         : ^+v-
constituents        : one self-closing loop (gauge axis)
engine closure      : ^+v-
final history       : ^+v-
fold depth (pairs)  : 2
ZFA closed          : True
hermitian conjugate : +^-v
interpretation      : Primordial quantum black hole successfully gauge-folded into a stable ZFA particle closure.

=== POSITRONIUM ===
open prefix         : ^<v>^>v<
constituents        : electron ^<v> ++ positron ^>v< (spatial square)
engine closure      : ^<v>^>v<
final history       : ^<v>^>v<
fold depth (pairs)  : 4
ZFA closed          : True
hermitian conjugate : >^<v<^>v
interpretation      : Primordial quantum black hole successfully gauge-folded into a stable ZFA particle closure.

=== MUONIUM ===
open prefix         : ^<v>^>v</\
constituents        : electron ++ antimuon (+ diagonal axis)
engine closure      : ^<v>^>v</\
final history       : ^<v>^>v</\
fold depth (pairs)  : 5
ZFA closed          : True
hermitian conjugate : /\>^<v<^>v
interpretation      : Primordial quantum black hole successfully gauge-folded into a stable ZFA particle closure.

=== ATOM ===
open prefix         : ^<v>^>v</\+-
constituents        : electron ++ proton (+ diagonal + gauge axes)
engine closure      : ^<v>^>v</\+-
final history       : ^<v>^>v</\+-
fold depth (pairs)  : 6
ZFA closed          : True
hermitian conjugate : +-/\>^<v<^>v
interpretation      : Primordial quantum black hole successfully gauge-folded into a stable ZFA particle closure.

Depth progression (each step adds a direction / qubit):
  neutrino     depth=2  ^+v-           ->
  positronium  depth=4  ^<v>^>v<       ->
  muonium      depth=5  ^<v>^>v</\     ->
  atom         depth=6  ^<v>^>v</\+-     

Vacuum ecology summary:
  resolved histories : 4
  baseline density   : 4.0
```

Reading the output: each rung is an **open prefix** (the unresolved divergence) the engine gauge-folds into a closed history whose `ZFA closed` flag is `True`, and the **fold depth grows `2 → 4 → 5 → 6`** as each new direction is added. The **neutrino** `^+v-` closes through spin + gauge only — no `<`/`>` spatial width, hence the "ghost" non-interaction. **Positronium** `^<v>^>v<` is the symmetric joint closure of an electron `^<v>` and a positron `^>v<` (mutual Hermitian conjugates — particle ↔ antiparticle = the reversed-and-conjugated history). **Muonium** adds the diagonal `/\` fold (a deeper partner), and the **atom** (hydrogen) adds the gauge `+-` fold (the deepest, electron ++ proton). The vacuum ecology then records all four as resolved histories in the [`VacuumEnergy.md`](VacuumEnergy.md) information ecology.

To inspect the bare half-loops instead of the bound states, run `python particles.py --particle constituents` (electron, positron, fluxoid); a single rung with `--particle muonium`, etc.

---

See also: [eight-twists-sufficiency.md](eight-twists-sufficiency.md) — proof that the 8-twist alphabet is the complete generative kernel for all particles and dimensions; [Standard_Model.md](Standard_Model.md) — honest synthesis mapping every Standard Model sector to its QLF derivation status (derived / partial / open); [Atom.md](Atom.md) / [Atomic_Structure_QLF.md](Atomic_Structure_QLF.md) — how these particles assemble into atoms; [Spin_QLF.md](Spin_QLF.md) — spin, charge, and chirality as twists.
