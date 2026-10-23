# Bound States as QLF Observables

**Free leptons do not exist as independent QLF observables.** The natural QLF "particles" are **atomic systems** — bound, balanced, joint-ZFA closures of two or more charged constituents. The QLF mass-spectrum derivation targets atomic-system masses (positronium, muonium, hydrogen, etc.) rather than free-lepton mass ratios.

This is the same structural move that [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) makes for photons (a photon is the joint ZFA closure of emitter and absorber, not a free projectile) and that [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) makes for quarks (no asymptotic free quarks; only bound hadrons). Applied to leptons: an electron is not an independent particle whose mass can be extracted in isolation; it is one half of a joint-ZFA bound state, and the bound state is the QLF observable.

---

## §1 Free leptons are not stable QLF closures

Standard particle physics tabulates `m_e ≈ 0.511 MeV`, `m_μ ≈ 105.66 MeV`, `m_τ ≈ 1776.86 MeV` as if these are properties of free particles. Operationally they are extracted from atomic and high-energy experiments; physically, a free lepton has not completed a joint-ZFA closure event.

**Sharpened, and machine-verified** ([`lean/QLF_ElectronClosure.lean`](lean/QLF_ElectronClosure.lean), zero axioms; full account in [`Electron.md`](Electron.md) §1). "Open Hermitian deficit" was the right idea at the wrong level, and the level matters:

- the lepton's **internal cycle** `^<v>` **is** ZFA-closed and folds to `−I` (`electronCycle_countBalanced`, `electronCycle_folds_negI`) — it is a completed half-spin periodic mode, not an unfinished fragment;
- what is open is the **gauge** twist, and that unmatched gauge count **is** the electric charge (`electronCharged_charge = 1`, `electronCharged_not_countBalanced`);
- so **a ZFA-closed history is electrically neutral** (`zfa_closure_is_neutral`) — charge is the *residue of non-closure*, and the contrapositive is the load-bearing half: **a charged history is not an event at all** (`charge_nonzero_not_countBalanced`). Nothing is pending. A free lepton does not *seek* a partner and nothing is owed — it closes or it does not, and if it does not there is no effect and no charge. The bound system is the QLF-physical state because that is where a closure exists, not because a constituent wanted one.

What is usually called Coulomb attraction and repulsion is the **count of joint histories that do close** (`coulomb_is_a_counting_rule`): like charges admit **zero**, opposite charges admit some, and a joint closure exists only where the charges cancel (`joint_closure_total_charge_zero`). No force, no field, no action at a distance — the same framing as [`Spacetime_Constructor.md`](Spacetime_Constructor.md).

Two consequences used below: **Hermitian ⇏ ZFA-closed** (`hermitian_not_implies_zfa` — the prefix `^<v` folds to the Hermitian `−σx` while carrying `F = 1`), and a joint closure places **no constraint on its components** (`joint_closure_allows_unequal_components` — two unbalanced halves of *different lengths* whose joint history closes), so unequal constituent depths are the normal case, not an obstruction.

- A free electron's Hermitian conjugate is its antiparticle, the positron. The pair `(e⁻, e⁺)` together can form a joint ZFA closure — **positronium**.
- A free electron + a proton can close jointly — **hydrogen** ([▶ see it self-assemble](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html#qc=H%20p%2Be%20%40%200%2C0%2C0), and two H share into **H₂** — [▶ see](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html#qc=H%20%40%20-2%2C0%2C0%0AH%20%40%202%2C0%2C0); more molecules in [`Chemistry.md`](Chemistry.md)).
- A free electron + an antimuon can close jointly — **muonium**.

In every case the QLF-physical state is the bound system, not the free constituent.

---

## §2 The natural QLF atomic-system observables

Three pure-Coulomb bound states with measured masses and binding energies:

| Atomic system | Constituents | Mass (MeV) | Binding (eV) |
|---|---|---|---|
| **Positronium** (Ps) | e⁻ + e⁺ | 2 · 0.511 = 1.022 | 6.803 |
| **Muonium** (Mu)     | e⁻ + μ⁺ | 105.66 + 0.511 ≈ 106.17 | 13.541 |
| **Hydrogen** (H)     | e⁻ + p  | 938.27 + 0.511 ≈ 938.78 | 13.598 |

All three are charge-balanced, ZFA-closed bound systems. Each has a well-defined mass and binding energy. These are the observables the QLF mass-spectrum derivation must reproduce.

The τ does not form a stable atomic system; its lifetime (≈ 290 fs) is too short for Bohr-orbital binding. The QLF observable for the third generation is therefore not a "tauonium" but the τ-decay vertex itself — a different kind of joint-ZFA closure event.

---

## §3 The atomic-system mass-spectrum question

The right QLF question:

> **Which QLF closure structures correspond to specific atomic systems, and how does their depth or multiplicity scale with the measured atomic-system mass or binding energy?**

Worked subjects.

### 3.1 Positronium ↔ minimal-qubit joint closure

The minimal joint ZFA closure between a lepton and its Hermitian-conjugate partner is the **half-spin ZFA atom** of [`HALF-SPIN-ZFA-EMBEDDING.md`](HALF-SPIN-ZFA-EMBEDDING.md) §2 — a two-twist Hermitian pair like `^v`. The mass of this closure should map to `m(Ps) = 1.022 MeV`.

The "electron mass" 0.511 MeV is then the QLF observable's *half* — `m(Ps) / 2`, not a free-particle property.

### 3.2 Muonium ↔ asymmetric joint closure

Muonium binds a light electron to a heavier antimuon. The natural QLF reading: a joint closure where one half is the minimal Hermitian pair (electron side) and the other half is a deeper-blanket Hermitian closure (muon side, more qubits to accommodate the heavier mass). Per [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md)'s scale-recursion framing, the muon side sits at a deeper Markov blanket — `Δt = R / f` with larger R.

### 3.3 Hydrogen ↔ lepton-baryon joint closure

Hydrogen binds an electron to a proton. The proton is a composite three-quark closure ([`Particles.md`](Particles.md), [`HadronicDepth.md`](HadronicDepth.md)). The joint ZFA closure of (electron) + (proton-internal) is structurally different from the lepton–antilepton case of positronium or muonium. The QLF mass `m(H) ≈ 938.78 MeV` is dominated by the proton mass; the binding energy 13.6 eV is the residual joint-closure energy after the constituent rest energies.

### 3.4 The right ratios

Measured atomic-system mass ratios:

- `m(Mu) / m(Ps) ≈ 106.17 / 1.022 ≈ 103.9`
- `m(H)  / m(Ps) ≈ 938.78 / 1.022 ≈ 918.6`
- `m(H)  / m(Mu) ≈ 938.78 / 106.17 ≈ 8.84`

Measured atomic-system binding-energy ratios:

- `E(Mu) / E(Ps) ≈ 13.541 / 6.803 ≈ 1.99`  (very close to 2)
- `E(H)  / E(Ps) ≈ 13.598 / 6.803 ≈ 2.00`  (very close to 2)
- `E(H)  / E(Mu) ≈ 13.598 / 13.541 ≈ 1.004` (essentially 1)

The binding-energy structure is dominated by the **reduced-mass** factor in the Bohr formula `E_bind = (μ / m_e) · 13.6 eV`. Hydrogen and muonium have nearly identical reduced masses (because muon-to-electron is heavy-to-light, similar to proton-to-electron), so their bindings are nearly equal. Positronium has reduced mass `m_e / 2`, hence half the binding.

This is standard non-relativistic QM. The QLF derivation should reproduce these ratios from joint-ZFA closure-multiplicity counts.

---

## §4 The τ as a decay-vertex closure

The τ does not form a Bohr-bound atomic system. Its mass corresponds to a different kind of joint-ZFA closure event — the **decay-vertex** for τ⁻ → ν_τ + W⁻ (and the analogous hadronic channels). The energetic threshold `m_τ > m_W − m_ν` and the available phase space at the vertex together determine the mass.

The QLF reading: the τ-decay vertex is a four-body joint ZFA closure (one in, three out) that is allowed at exactly the depth corresponding to the measured mass. This is structurally different from the two-body Bohr-binding closures of positronium / muonium / hydrogen, and needs its own treatment.

---

## §5 What this is NOT

- **Not a claim that free-lepton masses are unmeasurable.** They are extracted from atomic and scattering experiments and are well-tabulated. The claim is that they are *derived* quantities, not direct QLF observables.
- **Not a claim that QLF cannot reproduce lepton-mass ratios.** It claims the right derivational path goes via atomic-system mass observables. The free-lepton ratio `m_μ / m_e ≈ 207` should emerge as a consequence of the atomic-system structure, not as an independent target.
- **Not a new structural insight in the abstract** — "no free particles, all observables are joint closures" is already in [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) (photons), [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) (hadrons), and [`HALF-SPIN-ZFA-EMBEDDING.md`](HALF-SPIN-ZFA-EMBEDDING.md) (half-spin atoms as Hermitian pairs). This doc applies it specifically to leptons.

---

## §6 Open work

- **Map each atomic system to a specific QLF closure structure.** ✓ Done — [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) writes out positronium (symmetric two-electron-half-loop joint closure), hydrogen (electron half-loop + proton internal closure), and muonium (asymmetric electron + antimuon half-loops). Total joint depth `R(bound) = R_A + R_B`; mass `m = α R(bound)`.
- **Compute the QLF mass for each mapped atomic system** ✓ Done at the mapping level — `m(Ps) = 2 m_e`, `m(H) = m_e + m_p`, `m(Mu) = m_e + m_μ` follow directly from the joint-closure-depth decomposition. α is numerically anchored at 10⁻¹⁰ via the QLF Bohr inversion `α = sqrt(2 R_e / R_1)` ([`Hydrogen.md`](Hydrogen.md) §4.1, [`fine_structure_demo.py`](fine_structure_demo.py)). The deeper derivation (`α R_e = m_e` from first-principles QLF closure-multiplicity — i.e. derive R_e itself) is open work joining the Standard-Model mass-spectrum programme.
- **Test the Bohr-formula reduced-mass structure** `E_bind ∝ μ` from QLF closure-multiplicity counts. ✓ Done — `Atomic_Structure_QLF.md` §5 reproduces `E(Mu)/E(Ps) ≈ 2`, `E(H)/E(Ps) ≈ 2`, `E(H)/E(Mu) ≈ 1` from the reduced-mass formula `μ = R_A R_B / (R_A + R_B)`. The full derivation of `13.6 eV = (1/2) m_e α²` from joint-closure multiplicity (rather than the Bohr-model assumption) is sketched in [`Hydrogen.md`](Hydrogen.md) and remains partial.
- **τ-decay-vertex closure**: identify the specific QLF topology for τ⁻ → ν_τ + W⁻ and verify that `m_τ` corresponds to the energetic threshold for this vertex closure. ✗ Open ([`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §6 names the question; the specific topology is not yet pinned).

---

## References

### Internal

- [`HALF-SPIN-ZFA-EMBEDDING.md`](HALF-SPIN-ZFA-EMBEDDING.md) — Hermitian pair as the minimal joint closure; the QLF unit of physical existence.
- [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) — photons as joint emitter-absorber closures, not free particles; the same structural move applied to photons that this doc applies to leptons.
- [`Collective_Electrodynamics.md`](Collective_Electrodynamics.md) — joint ZFA closures as the unit of EM interaction; vector potential as unresolved free action.
- [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) — bound-state framing at the hadronic scale; the "same blanket strategy at every scale" recursion that extends naturally to lepton atomic systems.
- [`Hydrogen.md`](Hydrogen.md) — existing Bohr-derivation of hydrogen levels in QLF language.
- [`Atom.md`](Atom.md) — atomic shell structure derived from QLF.
- [`Standard_Model.md`](Standard_Model.md) §6 — "Mass ratios from multiplicity" open work, scoped here to atomic-system masses.
- [`Active_Inference_Mathematics.md`](Active_Inference_Mathematics.md) §5 scoreboard — "Quantitative mass spectrum" row.

### External

- Particle Data Group, *Review of Particle Physics* — measured lepton masses and atomic-system rest masses.
- Karshenboim, S. G. (2005). *Precision physics of simple atoms: QED tests, nuclear structure and fundamental constants*. Phys. Rep. 422, 1–63 — positronium, muonium, hydrogen precision data.
