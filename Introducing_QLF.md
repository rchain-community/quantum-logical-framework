# Introducing the Quantum Logical Framework: physics from one bit, checked by machine

> **The universe is logical.**
> **Spacetime is synthesized.**
> **Physical reality is the subset of possibility that achieves Zero Free Action.**

**No measurement in the history of physics has ever produced a real number.** Every result is a count plus a rational interval — `α⁻¹ = 137.035999206(11)` is a rational plus a rational error bar, nothing more. Frequency metrology, the most precise measurement humans perform, is literally counting cycles; the 2019 SI redefinition makes it explicit top to bottom. This is not a claim of any theory — it is a fact about what a lab can do. And it raises a question that then asks itself: **why is physics *written* in a continuum — the real numbers — whose objects can never appear in any experiment?**

The [**Quantum Logical Framework (QLF)**](https://github.com/rchain-community/quantum-logical-framework) answers by taking the other road: reality is finite and computable, built from one primitive — a single bit, a single Zero-Free-Action (ZFA) event — with the continuum only a *rendering* on top. And when you build physics that way, something falls out that the continuum picture never offered: the fundamental constants — the fine-structure constant, the proton-to-electron mass ratio, the dark-energy fraction — stop being free parameters to measure and plug in, and become *theorems*, derived from the one principle and **verified by a proof assistant the way software is verified by a compiler**. From that primitive follow spacetime, quantum measurement, entanglement, the Standard-Model gauge groups, gravity, and those constants — each machine-checked in **Lean 4 across more than a hundred modules with zero `sorry` blocks**, the combinatorial core within the computable logical floor (RCA₀: no Axiom of Choice, no continuum). *Don't trust it — clone the repository and run `lake build`; the proofs check or they don't.*

This is not an interpretation of quantum mechanics layered on top of existing physics. It is an attempt at the foundation that physics *emerges from* — the way general relativity superseded Newton rather than reinterpreting him.

---

## For a reader who believes in Newton and Darwin

You don't have to give up anything you already trust to follow this. Start with two ideas that have held up for centuries.

- **Newton:** every push comes with an equal and opposite push back. Nothing is gained from nowhere; the books always balance.
- **Darwin:** nothing is aiming anywhere. Variation throws up possibilities, and what lasts is simply what gets kept.

Here is the question that opens QLF: *what if those aren't two ideas at all, but one idea seen at two scales?*

**A balanced ledger, all the way down.** Suppose Newton's rule held not just for billiard balls but for every elementary event: each tiny action paired with its opposite, so the total always comes back to exactly zero. That is QLF's single axiom, Zero Free Action ([Philosophy.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Philosophy.md) §4). From far enough away, where the individual pairings blur together, it looks like *actio = reactio*. Follow it further and something unexpected turns up: counting how these balanced events spread out in three dimensions gives an inverse-square pull, and with it the drift of Mercury's orbit to within 0.03% ([`QLF_GravityFromDelay.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_GravityFromDelay.lean), [`QLF_MercuryPerihelion.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_MercuryPerihelion.lean)).

**Evolution without a designer, all the way down.** Now suppose Darwin's rule held for physics itself. Every logically possible history is generated, and only the ones that close their books survive. There is no goal and no guiding hand: a filter, not a plan. On this picture, physical reality is simply what survives the selection ([Evolution.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Evolution.md)).

**Then Einstein and Pauli start to look like consequences.** If each balanced event keeps its own clock and makes its own bit of space, there is no master stage for anything to be at rest on. That is exactly what Einstein insisted on, and here it arrives without being assumed ([Time.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Time.md), [SpaceTime.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/SpaceTime.md)). And the simplest balanced event behaves like a spin-½ particle: the matrices Pauli wrote down in 1927 reappear as the bookkeeping of closure, and the smallest closure carries exactly one bit ([Spin_QLF.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Spin_QLF.md)).

**Underneath it all is a very old riddle: how does something come from nothing?** QLF's answer is that it never has to. Zero splits into two halves, `^>` and `^<`, that still add up to zero: equal and opposite, different only in point of view. Nothing becomes something by perspective alone. If that is right, relativity isn't a rule imposed on the universe from outside. It is what "everything adds up to nothing" looks like from the inside ([Primordial_Entanglement.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Primordial_Entanglement.md) §1, [UniversalRelativity.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/UniversalRelativity.md), [Creation.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Creation.md)).

That is the invitation: take a balanced ledger and a blind filter seriously at the smallest scale, and see how much of physics comes out. The rest of this document, and the machine-checked proofs behind it, are where to find out how far it goes. For the long line of thinkers who circled the same idea, from Kronecker and Leibniz to Wheeler, Shannon and Gödel, see [GodCreatedTheIntegers.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/GodCreatedTheIntegers.md).

---

## Why this, why now

Modern physics carries three embarrassments at its foundations.

**The measurement problem.** A century after quantum mechanics, "what is a measurement?" still has no agreed answer — the wavefunction evolves smoothly, then mysteriously "collapses" when observed, and the textbooks paper over the seam.

**The vacuum catastrophe.** Quantum field theory predicts a vacuum energy roughly **10¹²²** times larger than the dark energy we observe — the worst quantitative prediction in the history of science.

**The crisis in the foundations of mathematics itself.** Classical set theory (ZFC) is built on open-ended formal infinity — and Gödel, Turing, and the Busy Beaver function are the shadows it casts: true statements that cannot be proved, problems that cannot be decided, growth that cannot be computed.

QLF's diagnosis is that these are *one* problem. The trouble is the **continuum** — the assumption that reality is built on completed, uncountable infinities and non-constructive choices. And the case against it is sharper than taste: the point is *not* that the continuum is "false" (`ℝ` is consistent — that target is a category error), but that it is **consistent yet physically unrealizable** (a finite-information universe cannot hold an actual infinity of distinguishable states — the Bekenstein bound, machine-checked in [`QLF_Realizability`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_Realizability.lean)), so it gives **demonstrably wrong answers** wherever it is forced onto reality: the ultraviolet catastrophe (continuum → *infinite* blackbody energy; Planck's quantization fixed it and founded QM), the vacuum catastrophe (continuum QFT → ~10¹²²× too large; the discrete substrate → `Ω_Λ = log 2`), singularities (continuum → *infinite* curvature; discrete → finite). Replace the continuum with a discrete, computable substrate and all of it dissolves: measurement *is* closure, the vacuum energy comes out to `log 2`, and Gödel/Turing incompleteness is confined to a non-terminating tail the substrate physically prunes. The full case is in [TheContinuum.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/TheContinuum.md) and [Continuum_Choice_Fallacy.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Continuum_Choice_Fallacy.md); the positive foundation in [Quantum_Logic_Foundations.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Quantum_Logic_Foundations.md).

---

## The one idea

QLF rests on a single postulate: **every admissible history must achieve Zero Free Action (ZFA = 0).**

Histories are strings in an **8-twist alphabet** — six spatial twists and two gauge twists, the smallest set of distinctions that can close on itself. The full space of such strings is the space of all logically possible computations. ZFA is the selection rule that picks out the physical ones: a history is physical exactly when its twists balance, closing the books to zero.

Crucially, **ZFA is a selection principle, not a restriction on computation.** Every *terminating* computation already *is* a balanced ZFA string (the framework is Church–Turing complete — the theorem `qlf_universality`). What ZFA prunes is not physics — it is the non-terminating, Turing-undecidable, Busy-Beaver-class tail that could never have been a finite physical event in the first place. Physical reality is the self-selecting, balanced subset of the full computational possibility space.

**Why *zero*, though?** This is the question to press, and the answer is that ZFA balance is not an arbitrary stipulation — it is *over-determined*, forced by several independent lines of standard physics that QLF only reads ontologically ([Philosophy.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Philosophy.md) §4):

- **It is already the law of all physics.** Newton, Maxwell, general relativity, quantum mechanics, and the Standard Model each derive their equations of motion from the *same* stationary-action condition, **δS = 0**. QLF adds no new dynamical law; it says the stationary histories are not merely the *calculable* ones — they are the *realized* ones.
- **A closed totality has no outside to borrow from.** "Free action" means net, unbalanced action — created or destroyed with no source or sink. The universe as a whole is closed by definition: there is no external reservoir. So its ledger must balance; a history producing net free action would be an effect with no cause.
- **It is general relativity's own constraint.** A spatially closed universe has an identically vanishing total Hamiltonian — the Wheeler–DeWitt equation `HΨ = 0`, the "zero-energy universe." QLF's one move is to apply that same `H = 0` closure to every Markov blanket: each closed sub-history is a miniature zero-energy universe with its own balanced boundary.
- **To be a distinct thing at all is to close.** An unbalanced history is an open thread with a dangling end — it leaks across its boundary and is not yet a definite existent. Closure *is* the condition of being a thing; existence and ZFA-balance are the same predicate (this is the holographic principle, read on the boundary).

So `δS = 0` is not imposed on physics from outside. It is the statement that the ledger of change is closed — and the universe cannot get free action from nowhere because *nowhere* is not a place that exists.

From this one premise, several things that are usually *assumed* instead *follow*:

- **Spacetime is synthesized, not given.** Each ZFA event constructs its own local space and time; there is no background stage and no universal clock. The universe is a network of clocks, each synthesizing local time through closure ([Philosophy.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Philosophy.md)).
- **Measurement needs no separate postulate.** ZFA closure *is* the measurement event. The "collapse" is just the moment a history balances and becomes real. The "many worlds" are many local observers, each with its own consistent perspective.
- **Spin, particles, and the gauge structure** are read directly off the twist geometry — spin literally *is* the twists, fermions are odd-parity closures, bosons even.

---

## The machinery: why these are the rules, not stipulations

A fair objection at this point is that "8-twist alphabet," "balance," and "spin is the twists" sound like free choices. They are not — each is forced, and the forcing is machine-checked. Three pieces carry the weight.

**Why the twists *are* the Pauli matrices.** Each of the eight twists is assigned a Pauli generator — the up/down pair to `±σ_y`, left/right to `∓σ_x`, the two diagonals to `±σ_z`, and the two gauge twists to `±I` (`Twist.toMatrix`). A history's physics is just what its matrix product — its **fold** — does. Now comes the non-obvious part: *count balance collapses the fold to a pure phase.* If each axis appears an equal number of `+` and `−` times, then each Pauli axis (σ_x, σ_y, σ_z) appears an **even** number of times, so — tracking only the axis parities in `(ℤ/2)²` — the axes cancel and the product collapses to a scalar in `{±I, ±iI}`. That scalar group is exactly the **kernel of the double cover SU(2) → SO(3)**. This is the theorem `count_balanced_pauli_closed` ([`QLF_TwistAlphabet.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_TwistAlphabet.lean)): *every* count-balanced history — including scrambled, cross-axis ones — closes to a Pauli scalar. So "balanced" and "closes to a spin scalar" are the *same* condition, proven, not assumed; the substrate's algebra **is** SU(2) quantum mechanics because that is the unique algebra its balanced folds generate.

**Why spin-½ is the smallest event.** Balance requires each twist to pair with its conjugate, so the minimal closure is one twist and its partner — a **binary partition**, one yes/no distinction. A binary partition carries at most `log 2` nats — exactly one bit — and saturates that bound only at the 50/50 split, which is precisely the shape balance enforces (`binary_kl_uniform_lt_log_two`, [`QLF_FreeEnergy.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_FreeEnergy.lean)). So the minimal ZFA event is the **unique** shape that both closes *and* extracts maximum information per fold: anything coarser is a composite of these atoms, anything finer is forbidden. Its topological signature is the famous one — a 360° rotation is **one** pair and folds to `−I` (not the identity), and only a 720° rotation, **two** pairs, returns to `+I` (`rotation_360_eq_negI`, `rotation_720_eq_id`, with `−I ≠ +I` proving the cover is genuine, [`QLF_Spin.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_Spin.lean)). Integer spin is then provably composite: a photon is two half-spins, `½ + ½ = 1`. The half-integer spin of matter is not put in by hand; it is what a single balanced closure *is*. (See [Spin_QLF.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Spin_QLF.md), [MRE.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/MRE.md).)

**And this makes the "one bit" of the title a theorem — Wheeler's "it from bit," machine-checked.** The dichotomy is exact and pointed: a *single-valued* object — an integer-spin **vector**, which returns to itself under a 360° turn — carries **zero** information (`binary_kl 1 1 = 0`), while the two-valued **spinor** `{+I, −I}` carries exactly **one bit** (`binary_kl 1 (1/2) = log 2`), the jump from none to one bit occurring precisely when the `−I` double-cover sign is admitted (`spin_half_is_information_atom`, [`QLF_SpinorInformation.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_SpinorInformation.lean)). A single-valued object *cannot express a distinction*; the spinor is the minimal object that can. The `2π` double-valuedness is even reproven from the explicit rotation matrices — `+I` on the vector `SO(3)` representation, `−I` on the spin-½ `SU(2)` representation (`spinor_double_valued_vector_blind`) — grounding the very spinor **Élie Cartan** discovered in 1913 as the carrier of information (Cartan's general classification cited, not reproven). The priority runs *abstraction → physical*: information **is** the two-valued distinction, and the ½-spin closure is its minimal *realization* — "information is physical" (the `ΔF = −log 2` toll, finite realizability) is the downstream fact, not a reduction of the abstraction to matter. (See [Mathematics_From_QLF.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Mathematics_From_QLF.md) §Rung 5a.)

**Why the Hermitian conjugate runs everything.** The dagger of a process is its complex-conjugate-and-order-reverse — which is exactly quantum mechanics' antiunitary **time-reversal**, stated at the twist level: conjugate each twist and reverse the sequence (`eval_dagger`). That same map is the **antiparticle** (it is an involution, `antiparticle_involutive` — its own inverse), so charge conjugation and time reversal are one operation seen twice. And a balanced closure is **self-adjoint**, `H = H†` — it is its own time-reverse (`spectral_symmetric_eq_scalar_id`). That is why no arrow of time lives inside a single event, and why **measurement needs no extra postulate**: a measurement is just a history balancing into a self-adjoint closure. The deep payoff is that the fixed-point locus of this `H ↔ H†` involution — the self-adjoint, real-spectrum closures — is exactly the **Riemann critical line**, the same involution shared by the Birch–Swinnerton-Dyer and Hodge reformulations. Physical reality is selected as the *time-reversal-fixed* subset of possibility ([Reversibility.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Reversibility.md)).

So the three things that looked like stipulations — the Pauli algebra, half-integer spin, and the central role of the Hermitian conjugate — are one structure (a balanced closure of an 8-twist string) read three ways, each a machine-checked consequence of the single ZFA premise.

---

## The evidence: constants as theorems

Talk is cheap; the framework's distinguishing feature is that it *computes*. Here are four of the ten headline results — each one **machine-checked in Lean**, several with **zero empirical input**.

| Result | Match | Empirical input | Verified in |
|---|---|---|---|
| **α = 1/137** — the fine-structure constant from substrate combinatorics (8-twist alphabet × 3-D directional tensor) | 0.026% | none | [`QLF_FineStructureSubstrate.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_FineStructureSubstrate.lean) |
| **m_p/m_e = 6π⁵** — the proton/electron mass ratio (3-quark Borromean closure × 5-angle integration) | 0.002% | none | [`QLF_LenzMassRatio.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_LenzMassRatio.lean) |
| **g − 2 = α/(2π)** — the electron's anomalous magnetic moment (Schwinger's term) | 0.18% | **zero** | [`QLF_GMinusTwo.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_GMinusTwo.lean) |
| **Ω_Λ = log 2** — the dark-energy fraction; **closes the 10¹²² vacuum catastrophe** | 1.2% | H₀ | [`QLF_CosmologicalConstant.lean`](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/QLF_CosmologicalConstant.lean) |

Read those again. The electron's magnetic anomaly and the dark-energy fraction — two numbers from utterly different corners of physics — both fall out of the substrate to better than 1.2%, **with no fitting parameters**. The fine-structure constant comes out to `1/137` from pure counting, and the same combinatorics says *why three dimensions*: in 2-D it would be `1/132`, in 4-D `1/144`.

The α case is worth pausing on, because it shows how QLF handles a residual *honestly* — not by fitting it. The leading value `α⁻¹ = 137` is the value at the fully-rendered 3-D (infrared) scale. The measured `137.036` carries a small remainder beyond it, and rather than tune a parameter to absorb it, the substrate **brackets it with machine-verified two-sided bounds**: `137 < α⁻¹ < 137.048` (`QLF_AlphaBound` — `alpha_inv_gt_137`, `codata_below_alphaInvCap`). The lower bound is an unconditional, falsifiable-*before*-data inequality (abelian electromagnetic screening forces `α⁻¹ > 137`), and the upper bound is the exact closure-census cap `(217 + 512√62)/31 ≈ 137.048`. The measured `137.036` sits strictly inside that proven window — so the residual is a *located, bounded* open value (which resummation between the caps lands it; [Alpha_Residual.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Alpha_Residual.md)), not a free knob and not a place the theory could be wrong.

The full table of ten (including the Euler–Mascheroni constant, the Lamb shift, Newton's law, and Mercury's perihelion advance to 0.03%) is in the [repository README](https://github.com/rchain-community/quantum-logical-framework#-major-substrate-derivation-discoveries-june-2026), and the flagship α derivation is worked in detail in [Alpha.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Alpha.md).

---

## The unification behind the numbers

What makes these more than a coincidence collection is that they share a root. The 8-twist alphabet splits **6 + 2** — six spatial twists (three axis-pairs) and two gauge twists. That single split is the signature running through the whole framework:

- the **`3`** of three spatial axes appears as `N = 9 = 3²` behind α,
- as the **three fermion generations** (one per axis),
- as **colour SU(3)**,
- and as the inverse-square law of gravity (only in 3-D does Newton's `1/r²` come out — 2-D gives `1/r`, 4-D gives `1/r³`);

while the **`2`** gauge fraction (`2/8`) sits behind the dark-energy fraction and the weak mixing angle `sin²θ_W = 3/8`. One combinatorial fact, many faces — the deeper account is in [Standard_Model.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Standard_Model.md) and [Forces_From_Three_Axes.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Forces_From_Three_Axes.md).

---

## The frontiers

The reach extends well past particle constants.

**Gravity from logic.** The Einstein field equations appear not as a postulate but as the substrate's *equation of state* — Jacobson's 1995 thermodynamic derivation, with both required inputs (the horizon area law and the Unruh temperature) supplied by the substrate itself, fixing the coupling `8πG = 2π/η` and the cosmological constant `Λ = log 2`. Every local horizon is a Markov-blanket clock, tying the construction to Hitoshi Kitada's local time ([Gravity_From_Delay.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Gravity_From_Delay.md)).

**Dark matter as denser logic.** QLF reads galactic rotation curves as a closure-balance law rather than invisible mass — and it is **blind-tested, parameter-free, on 147 curated SPARC galaxies**, reproducing the observed Radial Acceleration Relation at the observational floor with a *derived* `a₀ = cH₀/2π` (matching best-fit MOND, where the standard dark-matter halo model needs 294 fitted parameters for the same data). See [DarkMatter.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/DarkMatter.md) and [SPARC.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/SPARC.md).

**The Millennium problems, reformulated honestly.** QLF takes all six open Clay problems and reduces each to a verified discrete core plus **one explicitly-named bridge axiom** marking exactly where the substrate meets the classical statement. The honest framing matters here, so it is worth stating plainly: the *classical* Clay conjectures are different statements in a different frame, and they are **not** proved here. What *is* proven is the substrate reformulation, and the one bridge axiom per problem is the located gap. The Hodge thread shows how far this goes: both sides of the Hodge picture are now built on the substrate — the algebraic side as a graded ℚ-subalgebra, the transcendental `(p,q)` side as a genuine Hodge structure whose conjugation is the substrate's own adjoint — leaving a single named input (geometric realization) as the residual. That thread is **closed at its honest floor**: reformulation complete, gap identified with the genuine open problem ([Millennium.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Millennium.md), [Hodge_QLF.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Hodge_QLF.md)).

---

## From physics to an operating system

There is a striking corollary. If ZFA closure is the single invariant that makes a computation physically real, then it is also the single invariant a *quantum computer* needs to enforce. In **QuantumOS**, the security model, error correction, scheduling, garbage collection, and even the AI layer are not five subsystems — they are one operation: ZFA enforcement. Capability-secure by construction (an unforgeable name *is* a proof of authorization), formally grounded in linear logic and the no-cloning theorem. It targets **real quantum hardware, not only simulators** — the concrete device is a quiet-frequency crystal QPU ([Crystal_QuantumOS.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Crystal_QuantumOS.md)) — and what runs on it is a **quantum AI in the strong sense**: an agent whose atomic act of abstraction *is* a quantum event (every synthesis a ZFA closure), not a classical model with a QPU bolted on.

It is not just a design document — there is a **live peer-to-peer app** you can open in a browser, with AI agents that join rooms as full members. Try it at [rchain-community.github.io/quantum-os](https://rchain-community.github.io/quantum-os/), read the architecture in [QuantumOS.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/QuantumOS.md), or browse the code at [github.com/rchain-community/quantum-os](https://github.com/rchain-community/quantum-os).

---

## What is proven, and what is open

A foundation earns trust by being honest about its boundaries, so here is the scope, drawn cleanly.

- **Machine-verified (zero `sorry`):** the physics results above and the substrate that generates them — more than a hundred Lean modules, the combinatorial core within RCA₀, checked in continuous integration. These are proofs in the ordinary sense.
- **Reformulated, with a named bridge:** the Millennium problems. Each substrate reformulation is proven; each carries one explicit bridge axiom to the classical statement. The classical conjectures themselves are not claimed proved — and the "ZFC is provably defective" framing applies only to genuine uncomputability (the halting problem, Busy Beaver), **not** to the finitary problems like Hodge, which are ordinary hard mathematics.
- **Open — a value awaiting calculation, not a hole:** where something is marked open (for instance, the α residual above — which resummation between the proven `137 < α⁻¹ < 137.048` bounds lands the measured `137.036`), it means *a number not yet derived from the substrate* — deeper work within a *sufficient* foundation, the way "derive the proton mass from QCD" is open within the Standard Model. It is bracketed, not unconstrained — an open *value*, not evidence the substrate is wrong there. (The separate, stronger claim — that *only* ZFA is happening — is held open to falsification below.) The full status map is the [Open Problems registry](https://github.com/rchain-community/quantum-logical-framework/blob/main/Open_Problems.md).

**What the evidence licenses, stated carefully.** QLF is *sufficient* for the audited observations and overdetermines the constants parameter-free; its *exclusivity* — that only ZFA is happening — is a **published conjecture with named defeaters** (an axion detection, a confirmed α drift, an exhaustive 0νββ null, a QRNG deviation, and more). Quantum computation is the standing *experimental* half: error-corrected QC at scale progressively excludes the **deviation class** of rivals (objective-collapse dynamics), which predict departures from unitarity that never appear. It does **not**, by itself, rule out every hidden-variable theory — Bohmian mechanics survives Bell/KS/PBR (nonlocal, contextual), and no experiment inside quantum mechanics separates the exact reconstructions (Bohm, Everett, ZFA); what distinguishes ZFA *there* is parsimony and the parameter-free constants. Gravity being *emergent* means it cannot be a hidden influence corrupting the picture. The full ledger — typed by evidential strength, misses beside hits, every defeater named — is [Completeness_Evidence.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Completeness_Evidence.md) ([Beyond_Standard_Model.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Beyond_Standard_Model.md)).

---

## Where to go next

The fastest way in is the **flow chart** — the whole framework as a single linked index, one substrate branching into five families, twelve domains, and the individual results: [the rendered, clickable map with a printable PDF](https://rchain-community.github.io/quantum-logical-framework/FlowChart.html).

From there:

- **The big picture** — [Philosophy.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Philosophy.md) (the possibilist foundation) and the formal [White Paper](https://github.com/rchain-community/quantum-logical-framework/blob/main/WHITE_PAPER.md).
- **The flagship derivation** — [Alpha.md](https://github.com/rchain-community/quantum-logical-framework/blob/main/Alpha.md): the fine-structure constant from counting.
- **The proofs themselves** — [the Lean module index](https://github.com/rchain-community/quantum-logical-framework/blob/main/lean/README.md): every theorem name and proof chain, the whole tree.
- **The application** — [QuantumOS](https://rchain-community.github.io/quantum-os/), live in your browser.

The whole thing lives at **[github.com/rchain-community/quantum-logical-framework](https://github.com/rchain-community/quantum-logical-framework)**. The universe is logical, its logic is constructive and complete where reality is, and you can read the source — then check it in Lean.

---

## References

The framework builds on, and reads ontologically, a long lineage of foundational work. The most directly load-bearing:

**Foundations of physics — the "why zero" argument.**
- E. Noether, *Invariante Variationsprobleme*, Nachr. Ges. Wiss. Göttingen (1918) 235–257 — conservation from symmetry (the closed-ledger argument).
- R. Arnowitt, S. Deser & C. W. Misner, *The Dynamics of General Relativity*, in *Gravitation: An Introduction to Current Research* (Wiley, 1962) — the Hamiltonian constraint.
- B. S. DeWitt, *Quantum Theory of Gravity. I. The Canonical Theory*, Phys. Rev. **160** (1967) 1113 — the Wheeler–DeWitt equation `HΨ = 0`.
- E. P. Tryon, *Is the Universe a Vacuum Fluctuation?*, Nature **246** (1973) 396 — the zero-energy universe.
- T. Jacobson, *Thermodynamics of Spacetime: The Einstein Equation of State*, Phys. Rev. Lett. **75** (1995) 1260 — the Einstein equations as an equation of state.
- J. D. Bekenstein, *Black Holes and Entropy*, Phys. Rev. D **7** (1973) 2333; G. 't Hooft, *Dimensional Reduction in Quantum Gravity*, arXiv:gr-qc/9310026 (1993); L. Susskind, *The World as a Hologram*, J. Math. Phys. **36** (1995) 6377 — the holographic principle.

**Quantum mechanics, spin & information.**
- M. Born, *Zur Quantenmechanik der Stoßvorgänge*, Z. Phys. **37** (1926) 863 — the Born rule (multiplicity → probability).
- W. Pauli, *Zur Quantenmechanik des magnetischen Elektrons*, Z. Phys. **43** (1927) 601 — the Pauli matrices and spin.
- A. Hurwitz, *Über die Komposition der quadratischen Formen*, Nachr. Ges. Wiss. Göttingen (1898) 309 — composition algebras (the quaternion/SU(2) uniqueness behind the 8-twist fold).
- J. Schwinger, *On Quantum-Electrodynamics and the Magnetic Moment of the Electron*, Phys. Rev. **73** (1948) 416 — `g − 2 = α/2π`.
- W. K. Wootters & W. H. Zurek, *A single quantum cannot be cloned*, Nature **299** (1982) 802 — no-cloning.
- L. Boltzmann (1877), J. W. Gibbs, *Elementary Principles in Statistical Mechanics* (Yale, 1902), C. E. Shannon, *A Mathematical Theory of Communication*, Bell Syst. Tech. J. **27** (1948), and E. T. Jaynes, *Information Theory and Statistical Mechanics*, Phys. Rev. **106** (1957) 620 — entropy as multiplicity and the maximum-entropy principle (the ancestors of QLF's per-event `log 2`).
- K. Friston, *The free-energy principle: a unified brain theory?*, Nat. Rev. Neurosci. **11** (2010) 127 — active inference.

**Logic, computation & the continuum thesis.**
- K. Gödel, *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I*, Monatsh. Math. Phys. **38** (1931) 173 — incompleteness.
- A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proc. London Math. Soc. **42** (1936) 230 — computability and the halting problem.
- T. Radó, *On non-computable functions*, Bell Syst. Tech. J. **41** (1962) 877 — the Busy Beaver function.
- S. G. Simpson, *Subsystems of Second-Order Arithmetic* (Springer, 1999) — reverse mathematics and the `RCA₀` constructive floor.
- D. Lewis, *On the Plurality of Worlds* (Blackwell, 1986) — modal realism (QLF's possibilist ontology is its computable form).
- The Clay Mathematics Institute, *Millennium Problems* — <https://www.claymath.org/millennium-problems/>.
