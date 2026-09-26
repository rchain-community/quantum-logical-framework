# Hierarchical Control in QLF

**Relativity crosses frequencies. Fast controls from the bottom up, slow from the top down.** This document develops the hierarchical-control reading of QLF: ZFA closures at the vacuum frequency drive structure up through the scales, Markov-blanket boundaries at each scale screen admissible micro-events from above, and cross-frequency time dilation is the relativistic shadow of frequency mismatch between observer scales.

It also presents the constructive derivation of **Karl Friston's free energy principle** from ZFA — each ZFA closure is one quantum of free-energy minimization, the Markov blanket is the topological realization of Friston's statistical blanket, and active inference is the agent's selection among admissible next closures.

## 1. The hierarchy in QLF

QLF organizes physical structure into a scale hierarchy with two coupled control directions.

### Bottom — fast micro events drive structure upward

The smallest event is a **1/2-spin ZFA atom** ([MRE.md](MRE.md)): a single Hermitian pair $(t, t^\dagger)$ that folds to a scalar in the Pauli group. Each atom contributes exactly $\log 2$ nats of information at the vacuum frequency $f$. Composition of atoms via the parallel operator builds heavier structures:

- $k$ atoms in parallel form a 2k-twist Pauli-closed sequence — composite spin-$k/2$ objects.
- The atom alphabet (4 base pairs: `^v`, `<>`, `/\`, `+-`) suffices to generate every higher-dimensional system via parallel composition, replication, and name restriction ([eight-twists-sufficiency.md](eight-twists-sufficiency.md)).
- Causation runs bottom-up through this composition: atoms → particles → nuclei → atoms (chemical) → matter.

### Middle — Markov-blanket scales

Between the microscopic and the cosmic, **Markov blankets** at the particle, atomic, and hadronic scales each define their own internal clock ([Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md)). The blanket boundary screens internal free-action deficits while permitting only minimal, statistically predictive interaction with the exterior. The constructing delay at scale $R$ is

$$\Delta t_{\text{construct}} = R / f$$

(see [Frequency_Synchronization.md](Frequency_Synchronization.md)). Deeper blankets tick more slowly in coordinate time. The same blanket strategy recurs at every scale — particle → hadron → atom → cell → organism → cosmos. This is the **scale-recursive** structure that makes the hierarchy possible.

### Top — slow macro structure constrains the next micro event

At the largest scale, the **causal frontier** ([AgeOfUniverse.md](AgeOfUniverse.md)) carries the unresolved-distinction entropy of the entire observable universe. **Gravitational warping** ([Gravity.md](Gravity.md)) is this entropy's macroscopic shadow: "relational distortion that emerges when the full ZFA network is partially deconstructed by an observer's Markov blanket." The **holographic boundary** ([Holographic.md](Holographic.md), [QLF_Holographic_Computational_Universe.md](QLF_Holographic_Computational_Universe.md)) encodes which fast micro-events are admissible inside the bulk.

Constraint flows top-down: cosmic-horizon entropy sets the prior for what each blanket can resolve, each blanket sets the prior for what its constituents can resolve, all the way down to the next ZFA atom.

## 2. Cross-frequency relativity

Frequency is not an external parameter ([Frequency_Synchronization.md](Frequency_Synchronization.md)) — it is the resonant rate at which logical distinctions synchronize. Different scales tick at different rates because their internal Markov blankets enforce different $\Delta t = R/f$.

**Time dilation is frequency mismatch between observer frames.** A high-frequency observer (deep in a high-density region — a particle near a black-hole horizon, or a fast-moving frame) experiences proper time at the local blanket's clock rate; a low-frequency observer (in a sparse region) experiences proper time at a different rate. The Lorentz factor between them is exactly the ratio of their internal ZFA event rates.

The "space/time role swap" of Frequency_Synchronization.md is the local face of this cross-frequency relativity: in high-density regions the time axis dominates because gauge-fold events are frequent; in low-density regions the spatial axes dominate because non-gauge closures are frequent. Lorentz transformations are derived as the change-of-basis between frame-local ZFA event rates — not postulated.

## 3. Friston's free energy principle derived from ZFA

Friston's variational free energy (VFE) is

$$F = D_{\text{KL}}(q \mathbin{\Vert} p) - \ln Z$$

where $q$ is the recognition density (the agent's approximate posterior), $p$ is the generative model (its prior), and $Z$ is the normalizer. The free energy principle states that any system maintaining a Markov-blanket boundary minimizes $F$, equivalently minimizes surprise $-\ln p(\text{sensory data})$.

### 3.1 QLF construction

In QLF the same quantities are constructive:

- **The generative model $p$** is the uniform prior over admissible histories within the local Markov blanket's causal frontier. This is exactly the **possibility tree** of [MRE.md §2.1](MRE.md): all branches that are reachable under the orthogonality filter and not yet pruned by ZFA.
- **The recognition density $q$** is the posterior after the current ZFA event: uniform over the realized sub-tree (one of the two halves of the Hermitian-pair partition), zero on the unrealized half.
- **The Markov blanket** is the same object in both frameworks. Friston defines it statistically (internal states conditionally independent of external given blanket); QLF defines it topologically (closed loop screening internal free-action deficits, [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md)). These coincide: a topological ZFA boundary IS a statistical Markov boundary for the agent inside.

### 3.2 Per-event free-energy minimization

Each ZFA closure minimizes $F$ by exactly $\log 2$ nats at the 1/2-spin atom (the per-event maximum proved in [MRE.md §2.1](MRE.md)). The Hermitian-pair structure imposes binary partition, and the 50/50 binary partition saturates information gain. Anything coarser is a composite; anything finer is forbidden.

$$\Delta F = -\log 2 \quad \text{per 1/2-spin ZFA atom}$$

This is **one quantum of free-energy minimization per quantum of ZFA event**. The vacuum frequency $f$ sets the rate at which the system can decrement free energy. Faster blanket clocks mean faster free-energy descent — agents with higher internal frequency are more responsive.

### 3.3 Active inference as ZFA selection

The agent's choice of which next ZFA closure to enact (which Hermitian pair from the admissible set) IS Friston's active inference. The selection criterion — "minimize expected free energy" — reduces to "select the closure that maximizes residual blanket-internal information gain", which by MRE.md is the closure that most-evenly partitions the remaining possibility tree.

This derives [active_inference.md](active_inference.md)'s claim from the algebra rather than asserting it. The agent does not need to *compute* free energy; the algebra makes free-energy minimization the only physically realizable behavior at every blanket scale.

### 3.4 Caveat and status

The construction above is informal — a constructive argument from MRE.md plus the Markov-blanket / active-inference framework. **The Lean formalization is open work**: an actual theorem `zfa_closure_minimizes_free_energy` would require formalizing both the possibility-tree probability space and Friston's KL functional inside Lean 4. The argument is presented here as a derivation in the same standard as the rest of QLF (MRE.md, SpectralGap.md): constructive, falsifiable, with the Lean-verified step flagged.

## 4. Why fast controls bottom-up and slow controls top-down

The hierarchical-control architecture follows from §1–§3.

**Why fast controls bottom-up.** Each ZFA atom is one quantum of free-energy minimization. The vacuum frequency is the rate at which the universe can extract information from the possibility tree. Slowing the rate at which atoms close would leave free energy unminimized — physically impossible because ZFA enforcement (Lean-verified `rho_process_always_zfa`) precludes unresolved closures from persisting. Therefore the universe ticks at vacuum frequency, and structure builds up from the fastest available events.

**Why slow controls top-down.** Each Markov blanket filters which micro-events are admissible at the next instant via its causal-frontier prior. The blanket integrates information across many fast events into a slowly-evolving boundary state. That state IS the prior the agent inside the blanket must condition its next closure on. The cosmic horizon's slow entropy ledger ([AgeOfUniverse.md](AgeOfUniverse.md)) is the highest-level prior — gravitational warping ([Gravity.md](Gravity.md)) and the holographic encoding ([Holographic.md](Holographic.md)) are its expression at the bulk.

**Why relativity crosses frequencies.** Any consistent observer must match its internal clock to its frame-local ZFA event rate. Different scales tick at different rates by construction. Lorentz transformations between scales follow from ZFA closure consistency, not postulated as a separate principle.

## 5. Implications

- **Schrödinger evolution from the bottom-up side** — at the smallest scale, unitary evolution between ZFA closures is the system's free-energy-minimizing trajectory through the possibility tree.
- **Decoherence from the top-down side** — the Markov-blanket boundary's slow priors filter out fast micro-events incompatible with the macro state, producing classical-looking measurement outcomes.
- **Why life exists** — biological agents are nested Markov blankets that minimize free energy at every scale from molecular to cognitive. The hierarchical-control architecture is not a metaphor for life; life is one instance of it.
- **Why the cosmological constant is small** — at the cosmic scale, the slow top-down constraint nearly cancels the fast bottom-up vacuum energy. The residual is what gravity and dark energy measure ([Gravity.md](Gravity.md), [AgeOfUniverse.md](AgeOfUniverse.md)).

## 6. Open work

- **Lean theorem**: ✓ Done — `zfa_closure_minimizes_free_energy` is machine-verified in [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean). The proof reduces to the binary-partition identity `binary_kl 1 (1/2) = Real.log 2`, lifting the standard convention `0·log 0 = 0` via Mathlib's `Real.log` (which is 0 on non-positive inputs). The 50/50 case of MRE.md's proposed `max_relative_entropy_at_half_spin` is captured directly; the strict-inequality bound on non-50/50 partitions remains open.
- **Numerical demonstration**: ✓ Done — `active_inference_vfe_demo.py` enumerates all 4 Hermitian-conjugate pair types, verifies both orderings of each pair achieve ZFA closure (all 8 sequences fold to $-I$ in the Pauli group), and computes $D_{KL}(q \mathbin{\Vert} p) = \log 2 \approx 0.6931$ nats per binary-partition closure event. Enumerates all 168 ZFA-closed 4-twist atoms (of 4096 candidates) and confirms cumulative $\Delta F = -2 \log 2 = -\log 4$ per atom via the additivity of independent closures.
- **Cross-frequency Lorentz derivation**: ✓ Done — [Cross_Frequency_Lorentz.md](Cross_Frequency_Lorentz.md) writes out the Lorentz boost between two Markov-blanket frames as a change of basis on their internal ZFA event rates. Identifies $\gamma = f_A^{\text{proper}} / f_B^{\text{observed-in-}A} = \cosh\varphi$ where $\varphi$ is rapidity; recovers time dilation, length contraction, and interval invariance as direct consequences. Honest scope: re-frames standard SR in QLF language (does not derive $c$ from first principles — that's [UniversalRelativity.md](UniversalRelativity.md)'s job). Lean formalisation of `lorentz_boost_from_zfa_frequencies` is the open next step.
- **Cosmological-constant estimate**: quantify the top-down/bottom-up residual at the cosmic horizon — does it match the observed $\Lambda$?

## References

### Internal

- [MRE.md](MRE.md) — 1/2-spin atom as the per-event free-energy quantum
- [Frequency_Synchronization.md](Frequency_Synchronization.md) — frequency as resonant synchronization rate; $\Delta t = R/f$
- [active_inference.md](active_inference.md) — agent-side claim derived here from the algebra
- [BayesianMechanics.md](BayesianMechanics.md) — "the thing that can happen in the most ways happens first"
- [Hadrons_Markov_Blankets.md](Hadrons_Markov_Blankets.md) — same blanket strategy at different logical densities
- [Gravity.md](Gravity.md) — gravity as macroscopic top-down screening
- [UniversalRelativity.md](UniversalRelativity.md) — Einstein's relativity completed via ZFA event synthesis
- [Holographic.md](Holographic.md), [QLF_Holographic_Computational_Universe.md](QLF_Holographic_Computational_Universe.md) — boundary↔bulk as top↔bottom
- [AgeOfUniverse.md](AgeOfUniverse.md) — cosmic causal frontier
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — $\mathcal{L} = 0$ variational principle
- [eight-twists-sufficiency.md](eight-twists-sufficiency.md) — higher-dimensional systems via parallel composition
- [Experimental_Consistency.md](Experimental_Consistency.md) — §2.1 on the count-balance ∧ Pauli-closure ZFA conjunction

### External

- Friston, K. (2010). *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience 11, 127–138.
- Friston, K. (2019). *A free energy principle for a particular physics*. arXiv:1906.10184.
- Friston, K., Da Costa, L., Sajid, N., Heins, C., Ueltzhöffer, K., Pavliotis, G. A., & Parr, T. (2023). *The free energy principle made simpler but not too simple*. Physics Reports 1024, 1–29.
- Carver Mead, *Collective Electrodynamics* (2000) — fluxoid as phase coupling, foundational to QLF's micro-event picture.

### See also

- [Active_Inference_Mathematics.md](Active_Inference_Mathematics.md) — uses §3's Friston-FEP derivation as the **selection principle of a new mathematical system**: math whose objects are admissible trajectories of a free-energy-minimizing agent. Where this doc derives the FEP from QLF, the meta-doc reads QLF *as* the mathematics that has active inference built into its foundation.
