# Conservation Laws: Noether's Theorem in [QLF](README.md)

**Every ZFA-preserving symmetry of the 8-twist algebra corresponds to a conservation law.** Noether's theorem in standard physics relates continuous symmetries of the action to conserved quantities; in QLF the same structure is discrete and constructive — the algebra's symmetries are the conservation laws.

This document collects threads scattered across [Energy_Combinatorics.md](Energy_Combinatorics.md), [E_mc2_derivation.md](E_mc2_derivation.md), [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) (conservation as unitarity), [Annihilation.md](Annihilation.md) (per-atom information bookkeeping), [Maxwell.md](Maxwell.md) (charge conservation), and the Lean theorem corpus (`rho_process_always_zfa`, `bra_ket_always_balanced`, `decoherence_impossibility`) into a single statement.

## 1. The principle

In standard physics, **Noether's theorem (1918)** states: every continuous symmetry of the action gives rise to a conserved current. Translation in time → energy. Translation in space → momentum. Rotation → angular momentum. U(1) gauge → electric charge. SU(2) isospin → weak isospin. Etc.

In QLF, the 8-twist algebra has a finite set of **discrete symmetries**, each of which corresponds to a conservation law at the level of ZFA-closed histories:

| 8-twist symmetry | Conserved quantity | Lean / Numerical anchor |
|---|---|---|
| Time-translation (cyclic shift of history) | **Energy** | `rho_process_always_zfa`, [E_mc2_derivation.md](E_mc2_derivation.md) |
| Spatial translation (cyclic shift in axis-orbit) | **Momentum** | `path_integral.py` phase invariance |
| Rotation (axis permutation Y↔X↔Z) | **Angular momentum** | `tau_xy_product`, `tau_yz_product`, `tau_zx_product` in `BraKetRhoQuCalc.lean` |
| Gauge swap (+ ↔ −) | **Electric charge** | `no_magnetic_monopoles`, [Maxwell.md](Maxwell.md) |
| Hermitian conjugation (E ↔ E†) | **Unitary norm / probability** | `bra_ket_always_balanced`, [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) |
| Pauli-fold invariance (identity-mod-phase) | **Information** (per-event $\log 2$ bookkeeping) | [MRE.md](MRE.md), [Annihilation.md](Annihilation.md) |
| Global chirality reflection (LH ↔ RH) | **CPT** (combined) | [CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) |

The conservation law is not a separate axiom; it is a **direct consequence** of the symmetry holding at every ZFA closure. Because every constructible RhoProcess is ZFA (`rho_process_always_zfa`, [RhoQuCalc.lean:382](lean/RhoQuCalc.lean)), every constructible process preserves all of these quantities by construction. They cannot be violated because there is no admissible history in which they are.

**One caveat, developed in §2a.** This exactness holds for the *balance-based* currents — charge, momentum, unitarity/probability, the information ledger — which are **signed counts** protected directly by the machine-verified ZFA-balance theorems. **Energy is the exception.** It is the only quantity in the table above defined as a *multiplicity* (number of histories) rather than a signed count, so the balance theorems do not pin it. Energy conservation is therefore **emergent and only statistically exact** — recovered in the continuum / bound-state limit, not guaranteed at the level of an individual substrate closure. This is the canonical QLF reading, and it is the reading on which the framework's most accurate quantitative prediction (the fine-structure constant, [`Alpha.md`](Alpha.md)) depends; see §2a.

## 1a. The uniform ether is the symmetry substrate

Noether's theorem is only as good as the symmetry it is handed. In QLF that symmetry has a name and a physical seat: it is the **homogeneity of the ZFA vacuum** — the *stateless uniform ether* derived in [`Time.md`](Time.md) §4 (*Time Dilation as Thread Desynchronization*) and [`SpaceTime.md`](SpaceTime.md) §4 (*The Uniform Ether and Lorentz Invariance*). Following Einstein's 1920 Leiden address, that vacuum has real metric structure but **no preferred frame**: every node of the substrate offers statistically the same closure degeneracy $W_{ZFA}$.

That single uniformity is the common root of three results usually stated separately:

- **Spatial homogeneity → momentum** (§3). No point of the ether is privileged, so a cyclic shift of an axis-orbit history is a symmetry; its Noether current is the net spatial-axis count.
- **Time homogeneity → energy** (§2). The rewrite rules are the same at every tick, so absolute time has no handle on a history's multiplicity.
- **No preferred frame → Lorentz invariance.** The same statelessness that makes the two clauses above hold is what makes time dilation reciprocal and $c$ frame-independent (Time.md §4). Wigner's classification of particles by the inhomogeneous Lorentz group (1939, cited below) is the standard-physics image of this: energy, momentum, and spin are the labels of exactly this spacetime symmetry.

**Why this sharpens §2a rather than competing with it.** §2a explains energy's lone-emergent status *structurally* — energy is a multiplicity, not a signed count. The ether picture supplies the matching *physical* reason: the symmetry energy rides on, time-translation homogeneity, is only **statistical**. The ether is *statistically* uniform, not exactly uniform at every event. The signed-count currents (charge, the information ledger) are pinned by exact per-event ZFA balance and need no smoothness assumption — so they are exact regardless. Energy alone inherits its conservation from the ether's homogeneity, and a merely statistical homogeneity can only deliver a merely statistical conservation. **A statistically uniform ether and a statistically conserved energy are the same fact viewed from two sides.**

> Where the vacuum's uniformity is realized by exact per-event balance, the conservation law is exact. Where it rests on the ether's *statistical* smoothness — energy — the law is emergent. Lorentz invariance and energy conservation share one root: vacuum uniformity.

## 2. Energy

From [Energy_Combinatorics.md](Energy_Combinatorics.md): the energy of a QLF system is the **multiplicity** of valid histories at a given length — the number of topological permutations achieving the same ZFA closure. From [E_mc2_derivation.md](E_mc2_derivation.md): mass is the constructing-delay contribution of gauge folds, and $E = mc^2$ recovers the energy in those gauge folds.

The **conservation** follows from the time-translation symmetry of the QuCalc engine: the rewrite rules are time-homogeneous (the same rule applies at every clock tick of [Frequency_Synchronization.md](Frequency_Synchronization.md)). A history $h_1$ at time $t_1$ has the same admissible-extension multiplicity as the same history $h_1$ at time $t_2$; therefore the energy $E(h_1)$ does not depend on absolute time. Across any ZFA-closed process, energy in equals energy out **in the statistical / continuum limit** — see §2a for why this is an ensemble statement about expected multiplicity, not a guarantee at the level of an individual substrate closure.

Per-event bookkeeping ([Annihilation.md §3](Annihilation.md), [MRE.md §2.1](MRE.md)): each 1/2-spin atom carries $\log 2$ nats of information; energy is $E = h \cdot \text{bits} = h \nu$ when bits flow at frequency $\nu$. **Energy conservation = information bookkeeping conservation = ZFA constraint preservation.**

### 2a. Exact vs. emergent: why energy is the lone approximate current

Two readings of "energy conservation" circulate in the QLF corpus, and they are **not** the same claim. This section fixes which is canonical and why.

- **Exact-by-construction (the balance currents).** Charge, momentum, unitarity/probability, and the information ledger are *signed counts* — differences of twist counts (e.g. $\text{charge} = \text{count}(+) - \text{count}(-)$). ZFA closure constrains those differences exactly, and `rho_process_always_zfa` / `bra_ket_always_balanced` make it impossible to construct a history that violates them. For these currents, the §1 "cannot be violated" language is literal.

- **Emergent-by-averaging (energy).** [`QLF_FineStructureSubstrate.lean:177`](lean/QLF_FineStructureSubstrate.lean) states the canonical position directly: "Energy conservation is not a QLF axiom — it is emergent from substrate dynamics. At the substrate event level, individual closures **need not conserve energy**; statistical averaging over many events produces effective conservation at the bound-state scale."

**The canonical QLF position for energy is the second one.** Where the two framings conflict, the emergent/statistical reading governs; the strict "energy in must equal energy out at every closure" phrasing is an overstatement of the ensemble result.

**Why energy and not the others.** Energy is the *unique* entry in the §1 table defined as a **multiplicity** — the number of distinct histories achieving a given ZFA closure ([Energy_Combinatorics.md](Energy_Combinatorics.md)) — rather than as a signed count. A signed count is conserved because ZFA balance is a constraint *on that difference*; a multiplicity is not a difference of counts and inherits no such protection. The machine-verified balance theorems therefore pin charge, momentum, and the information ledger exactly, while leaving the energy multiplicity free to fluctuate at the single-event scale. That structural asymmetry — count vs. multiplicity — is the whole reason energy is the one current that only emerges statistically.

**Worked example — the fine-structure leak.** The α = 1/137 derivation makes substrate-level energy non-conservation *quantitative*. The combinatorial bare value is $\alpha_{\text{bare}} = 1/128$; the observed value comes from the emergent-conservation correction

$$\alpha_{\text{QLF}} = \frac{\alpha_{\text{bare}}}{1 + N\,\alpha_{\text{bare}}}, \qquad N = 9,$$

machine-verified as exactly $1/137$ in [`QLF_FineStructureSubstrate.lean`](lean/QLF_FineStructureSubstrate.lean) (`alpha_QLF_eq`). The factor $(1 + N\alpha_{\text{bare}})^{-1}$ is a self-energy-style resummation over the $N = 9$ substrate channels through which a bound state's energy *leaks* into the vacuum. **If energy were exactly conserved at every closure there would be no leak channels, no correction factor, and α would stick at the bare $1/128$.** The measured $1/137$ is precisely the resummed measure of how much energy conservation fails per substrate event. Substrate-level non-conservation is thus not a defect of the framework — it is the source of its most accurate prediction (0.026% from CODATA).

**Consequence for the §2 Noether statement.** The time-translation argument in §2 establishes that energy is *time-homogeneous in expectation*: the admissible-extension multiplicity of a history is independent of absolute time. That delivers conservation of the **ensemble-averaged** energy — the continuum / bound-state limit — not a per-closure guarantee. Read every "energy in = energy out" in this document in that averaged sense. Exact, per-event conservation is the special property of the *balance* currents, which energy alone among the §1 entries does not share.

### 2b. Energy is *created* — half of each event is lent to the future

§2a says energy is not pinned per closure. The residual is **not random — it is directional**: each ZFA event **creates energy**, and conservation is the *local* book-balancing of an inherently expanding ledger. This is the energy analog of [`Reversibility.md`](Reversibility.md): the *same* forward closure that makes a tick of time also makes the energy, and conservation — like reversibility — is **emergent and local, not fundamental**.

**Noether, run the other way.** Energy conservation ⟺ time-translation symmetry. But QLF time is *synthesized* — each event makes its own tick (`f = 1/t`, `ZFAEventDynamics`), and the universe **grows by one closure per event**. A growing universe is *not* time-translation symmetric: the substrate at the next tick is strictly larger than at this one. So by Noether's own logic there is **no exact global energy conservation** — and this is not a QLF peculiarity, it is standard GR cosmology: in an expanding spacetime energy is not globally conserved (the dark-energy density stays fixed while the volume grows, so total vacuum energy *increases*). QLF supplies the constructive mechanism the continuum theory lacks: the creation happens **one ZFA closure at a time**.

**Where the other half goes.** Each event is a balanced *duality* — `future_expansion + local_contraction = 0` (`event_duality_balanced`, `QLF_CosmicInflation`): it expands the future exactly as much as it contracts locally. Read as energy bookkeeping:

- the **local / present half** balances — this *is* the emergent local conservation (the covariant `∇_μ T^{μν} = 0` of GR, the "energy in = energy out" of §2 read in the now);
- the **future half** is lent forward — it is the cosmic expansion itself: the `w = −1` event-synthesis field that is inflation early and dark energy late (`inflation_and_dark_energy_same_field`, reusing the verified `zfa_dynamics_drive_acceleration`), accumulating as `Ω_Λ = log 2` per the substrate's closure quantum (`QLF_CosmologicalConstant`).

So "half the energy is lost to the future" is precise: the books balance *at the present node* (local conservation), while the forward half is never returned — it becomes the expanding vacuum. The arrow of time and the creation of energy are **the same event-duality**: the closure that discards the which-history (`ΔF = −log 2`, §2a of [`Reversibility.md`](Reversibility.md)) and synthesizes the next tick is the closure that lends its forward half to the future.

**TOEs that *axiomatize* energy conservation are wrong** — in exactly the way, and for exactly the reason, that TOEs axiomatizing reversibility are wrong ([`Reversibility.md`](Reversibility.md) §6). A theory of everything built on global energy conservation as a *fundamental* law has installed an emergent, local accounting identity as a foundation. It then cannot produce a genuinely expanding universe without bolting on a separate dark-energy term by hand — the very term QLF *derives* as the future half of each event. Energy conservation is real where it is real (the present-local ledger, exact for the signed-count currents), and it is an output, not an input. The fundamental thing is the ZFA closure; conservation, reversibility, and a fixed total energy are three faces of mistaking the *present-local balance* of that closure for the whole of it.

| Statement | Lean |
|---|---|
| each event's duality balances (`expand future = contract local`) | `event_duality_balanced` (`QLF_CosmicInflation`) |
| the forward half = inflation early / dark energy late, one `w=−1` field | `inflation_and_dark_energy_same_field` (`QLF_CosmicInflation`) |
| ZFA events drive the expansion (cosmic acceleration) | `zfa_dynamics_drive_acceleration` (`ZFAEventDynamics`) |
| the accumulated future energy = `Ω_Λ = log 2` | `QLF_CosmologicalConstant` |
| time is synthesized, the universe grows by one closure per tick | `ZFAEventDynamics` (`f = 1/t`), `AgeOfUniverse` (`age_is_finite_and_positive`) |

## 3. Momentum and angular momentum

**Momentum** follows from spatial translation symmetry: cyclic shifts of an axis-orbit history don't change its ZFA-closure status. The conserved current is the net axis-orbit count along each spatial axis — the per-axis B-field component in [Maxwell.md §1](Maxwell.md): $B_x = \text{count}(>) - \text{count}(<)$, etc. A free particle's momentum is the net spatial-axis bias of its history string.

**Angular momentum** follows from rotation symmetry: the τ-algebra $\tau_i \tau_j = -\delta_{ij} I - \varepsilon_{ijk} \tau_k$ (machine-verified `tau_xy_product` etc. in `BraKetRhoQuCalc.lean`) is invariant under cyclic axis permutations. The conserved current is the total spin contribution from each ZFA atom — exactly the spinor structure of [HALF-SPIN-ZFA-EMBEDDING.md](HALF-SPIN-ZFA-EMBEDDING.md).

The discreteness of angular momentum (quantized in $\hbar/2$ units) follows from the discreteness of the 1/2-spin atom: each atom contributes exactly one spin quantum. Higher angular momentum = parallel composition of more atoms.

## 4. Charge

From [Maxwell.md §4.1](Maxwell.md) and the Lean-verified `no_magnetic_monopoles`: ZFA closure requires every individual twist count to be zero, so the net gauge count $\text{charge}(h) = \text{count}(+) - \text{count}(-)$ is zero for any ZFA-closed event. For non-charge-neutral processes (an electron in isolation), the count is non-zero but constant — gauge folds can only be created or destroyed in Hermitian pairs `+−`, so total charge is conserved.

The U(1) gauge symmetry of QED is here the discrete `+` ↔ `−` swap symmetry: any history with the gauge-fold counts exchanged remains ZFA-closed (the global sign of the charge is conventional). The conserved current = the net gauge fold count, which is exactly the QED electric charge in units of $e$.

## 5. Unitarity / probability

From [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md): the sequential composition of an event with its Hermitian conjugate yields ZFA (the Void/Identity). This is the QLF realization of $U U^\dagger = I$ — unitary evolution preserves the norm of the state vector.

Equivalently from [Born_Rule.md](Born_Rule.md): the squared-modulus probability assignment $|A|^2$ is the unique bilinear form consistent with the Hermitian-conjugate symmetry. Probability is conserved because the underlying algebra is Hermitian, and the Hermitian symmetry is preserved at every ZFA closure.

`bra_ket_always_balanced` ([BraKetRhoQuCalc.lean:109](lean/BraKetRhoQuCalc.lean)) is the Lean-verified statement: it is algebraically impossible to construct a ZFA-unbalanced RhoProcess, so unitarity violation is not in the space of constructible objects.

## 6. Information (the per-atom ledger)

A novel addition that standard Noether does not have: in QLF, **information itself is a conserved quantity** at the per-event level.

Each ZFA closure releases $\log 2$ nats to the local possibility tree ([MRE.md §2.1](MRE.md)), and each annihilation event releases the same $\log 2$ nats back to the vacuum as massless quanta ([Annihilation.md §3](Annihilation.md)). The total information ledger across creation + annihilation is exactly zero per atom — created and released bits cancel.

The conserved current is the **per-event log-2 bookkeeping**: the difference between information gained and released, summed over all closures in a process, is zero for any ZFA-balanced trajectory. This is the QLF answer to the **black hole information paradox**: Hawking radiation is the topological release of the gauge-fold information that was held inside the constructing delay, returned bit-for-bit to the environment ([Entropy.md §1a](Entropy.md), [Annihilation.md §4.4](Annihilation.md)).

## 7. CPT (combined chirality + parity + time reversal)

[CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) develops the partial-symmetry story: individual C, P, T symmetries are violated by the residual-clustering dynamics that gave matter its dominance. The **combined CPT symmetry**, however, is exact in QLF: the full chirality reflection (swap LH ↔ RH globally, reverse time, conjugate every twist) maps any admissible history to its Hermitian conjugate, which is also admissible.

CPT conservation is the global statement of unitarity (§5): every QLF event has a CPT-conjugate that is also a valid event, with exactly the symmetric branching probabilities. The Sakharov conditions for matter dominance (CP violation + baryon number violation + departure from equilibrium) are satisfied by the residual-clustering dynamics without requiring CPT violation.

## 8. What is NOT (yet) derived

QLF does not yet provide constructive derivations of:

- **Electric charge — exactly conserved; `B−L` — not.** Electric charge *is* an exactly-conserved signed twist count (`signed_count_conserved`, [`QLF_BMinusL`](lean/QLF_BMinusL.lean): any annihilation-odd signed count is invariant under the ZFA dynamics), and every QLF closure is electrically neutral. **`B−L` is different.** The obstruction `wcount_zero_on_ZFA` shows every conserved signed count vanishes on every closure — yet a neutron is neutral while carrying `B−L=1`, and baryon vs antibaryon are count-balanced closures with the *identical* twist multiset yet `B−L = ±1`. So `B−L` is **not** a conserved signed count; it is at most a winding/orientation quantity, and baryon number is Lean-anchored as exactly such a signed 3-axis linking invariant ([`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean): proton `+1`, antiproton `−1`, leptons and mesons `0`). In the lepton sector `B−L` is **violated** — the neutrino is **Majorana** (`neutrino_majorana`, the `^v` loop being its own Hermitian conjugate), so lepton number is not conserved and **neutrinoless double-beta decay** (`Δ(B−L)=2`) is the predicted signature. With `B`-violation (sphaleron/baryogenesis, §7) alongside, QLF admits **no exact global symmetry beyond the gauge charges** — matching the standard quantum-gravity expectation (Banks–Seiberg, swampland). Only electric charge is exact. **The capacity reading** ([`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4b) makes that asymmetry
predictive rather than merely observed: a conservation law's exception scale is set by *what kind of
invariant its proof uses*. A **winding** quantity (baryon number) is capacity-relative, so it must be
violable — and is, above `T_EW ≈ 160 GeV`; a **composite binding** (the proton) likewise, dissolving at
`T_c ≈ 155 MeV`; an **annihilation-odd signed count** (electric charge, `signed_count_conserved`) is proven
invariant for *every* history with no capacity anywhere in the proof, so it has no exception at any scale.
`wcount_zero_on_ZFA` is therefore not just an obstruction to `B−L` — it is the reason `B` *had* to be
violable.
- **Color SU(3) confinement** — requires the Borromean three-quark topology to be derived as the unique stable closure under a specific symmetry. Open.
- **Weak SU(2) doublet structure** — requires a specific 8-twist subgroup to be identified as the weak gauge group. Open.

These are the standard-model gauge-group identifications. The QLF claim is that each will follow from a specific 8-twist symmetry once the identification is worked out; the current document establishes the **methodology** (every ZFA-preserving symmetry → conservation law) without committing to specific identifications for the weak/strong sectors.

## 9. Open work

- **Lean theorem**: `noether_zfa_symmetry_yields_conservation` formalizing the §1 statement. Per §2a this is tractable **only for the balance (signed-count) currents** — charge, momentum, the information ledger — which the existing ZFA-balance theorems already half-prove (`emergent_blanket_formation` is additivity of the conserved count under composition). A Lean statement for **energy** is *not* expected, since energy is a multiplicity and conserved only in the statistical limit; the honest target there is a numerical/statistical demonstration, not a per-closure theorem.
- **Numerical demo**: extend `path_integral.py` to log conserved quantities (energy, momentum, charge, information) along ZFA-closure trajectories and verify constancy.
- **Standard-model identifications**: complete the gauge-group derivations listed in §8.
- **Discrete Noether vs continuous Noether**: formalize the bridge between QLF's discrete symmetries and standard Lie-group continuous symmetries in the continuum limit.

## 2026 update

2026: BASE-STEP's road transport of antiprotons aims at sharper CPT tests. In QLF the antiparticle
mirror conserves length and reverses charge and baryon number for every word, and a history joined to
its mirror always closes (`mirror_closes`) ([Discoveries_2026 V1](Discoveries_2026.md#v1)).

## References

### Internal

- [Energy_Combinatorics.md](Energy_Combinatorics.md) — energy as multiplicity of histories
- [E_mc2_derivation.md](E_mc2_derivation.md) — mass-energy equivalence via gauge-fold constructing delay
- [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) — unitarity as `E + E† ≡ ZFA`
- [Annihilation.md](Annihilation.md) — per-atom information bookkeeping (creation + annihilation cancel)
- [MRE.md](MRE.md) — per-event $\log 2$ quantum, the information ledger
- [Maxwell.md](Maxwell.md) — charge conservation; `no_magnetic_monopoles`
- [Lagrangian_Formulation.md](Lagrangian_Formulation.md) — Σ₈ algebra, `tau_xy_product` etc.
- [HALF-SPIN-ZFA-EMBEDDING.md](HALF-SPIN-ZFA-EMBEDDING.md) — angular momentum from spinor structure
- [CP-Violation-and-Chirality.md](CP-Violation-and-Chirality.md) — partial-symmetry violations; CPT exactness
- [Entropy.md](Entropy.md) — information conservation across Hawking radiation
- [Born_Rule.md](Born_Rule.md) — probability conservation as Hermitian-symmetry consequence
- [Frequency_Synchronization.md](Frequency_Synchronization.md) — time-translation symmetry at the algebra level
- [Time.md](Time.md) — time threads, the stateless uniform ether, Lorentz invariance from vacuum uniformity (§4)
- [SpaceTime.md](SpaceTime.md) — the ZFA network as Einstein's uniform ether; space-side view of Lorentz invariance (§4)

### External

- Noether, E. (1918). *Invariante Variationsprobleme.* Nachr. d. König. Gesellsch. d. Wiss. zu Göttingen — original symmetry/conservation theorem.
- Wigner, E. P. (1939). *On unitary representations of the inhomogeneous Lorentz group.* Ann. Math. 40, 149 — symmetry classification of particles.
- Sakharov, A. D. (1967). *Violation of CP invariance, C asymmetry, and baryon asymmetry of the universe.* JETP Letters 5, 24 — conditions for matter dominance under approximate symmetries.
- 't Hooft, G. (1971). *Renormalizable Lagrangians for massive Yang-Mills fields.* Nucl. Phys. B 35, 167 — gauge-symmetry approach to the standard model.
