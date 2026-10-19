# Beta Decay and the Nature of the Neutrino

In the Quantum Logical Framework (QLF), nuclear decay is not a random probabilistic event; it is the deterministic restructuring of a topological Markov blanket to relieve logical stress. This document covers β decay as boundary restructuring, and what QLF says about the **nature of the neutrino** — which, on the framework's own principles and **machine-verified**, is **Majorana** (its own antiparticle), carrying the prediction of **neutrinoless double-beta decay** (`0νββ`).

## 1. The neutrino is Majorana — machine-verified

In QLF the **antiparticle** of a configuration is its **Hermitian conjugate** ([Annihilation.md](Annihilation.md)): conjugate every twist (`Twist.conj`) and **reverse the order**, since the adjoint of a product reverses it, `(A·B·C)† = C†·B†·A†`. A particle is **Majorana** (its own antiparticle) exactly when its twist history is a **fixed point** of this operation — a decidable property of the string.

**Machine-verified** ([`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)):

- `neutrino_majorana` — the neutrino loop `^v` **is** a fixed point of conjugate-and-reverse, so the neutrino **is its own antiparticle**.
- `electron_not_majorana` — the electron loop `^<v>` is **not** a fixed point; its conjugate is a *distinct* history (the positron), so the charged lepton is **Dirac**.
- `neutrino_neutral` ([`lean/QLF_Spin.lean`](lean/QLF_Spin.lean)) — being self-conjugate requires the neutrino's **charge and perpendicular-spin chirality to vanish** (`x = −x ⟹ x = 0`, via `majorana_is_neutral`). The neutrino is the same viewed from behind, so it has no charge handedness to flip — a pure flat (σ_y) spin, exactly the "neither charge nor chiral structure" reason below, machine-verified. See [`Spin_QLF.md`](Spin_QLF.md) §6.

The electron case makes this non-vacuous: the same test that calls the neutrino Majorana correctly calls the electron Dirac. And the neutrino comes out as the **unique** self-conjugate fermion for a structural reason — it is the only fermion with neither charge nor a chiral/linked structure, so its minimal non-chiral loop is the only one symmetric under conjugate-and-reverse (charged or chiral histories pick up an order they cannot match after reversal). QLF therefore reproduces, from structure, the real-physics fact that **only the neutrino can be Majorana** (a charged fermion cannot — it would violate charge conjugation).

**The prediction.** A Majorana neutrino means **lepton number is violated**: the neutrino carries no conserved lepton charge to distinguish `ν` from `ν̄`. The signature is **neutrinoless double-beta decay**, `2n → 2p + 2e⁻` (`ΔL = 2`). §1a refines *which* neutrino is Majorana and puts a number on the rate: only ν₁ contributes, giving `m_ββ ≈ 0.25 meV`, about 40× below what LEGEND-1000 or nEXO can reach. So a null at those experiments is **expected**, and a signal there would refute the refinement. This is still the corpus's clearest empirical commitment distinguishable from the Standard Model, which is agnostic on Dirac versus Majorana.

**What this means for `B−L`.** Because the neutrino is Majorana, `B−L` is **not an exactly conserved charge** — it is violated by `ΔL = 2` in `0νββ`. This is consistent with the framework's deeper structure: `B−L` is not even a conserved *signed count*. The obstruction `wcount_zero_on_ZFA` ([`lean/QLF_BMinusL.lean`](lean/QLF_BMinusL.lean)) proves any conserved signed count is **zero on every ZFA closure**, yet the deuteron is a stable neutral closure with `B−L = 1` — so `B−L` is at most a winding-type quantity, and the Majorana neutrino shows it is violated outright. **Electric charge, by contrast, *is* an exactly conserved signed count** (`signed_count_conserved`), and every QLF closure is electrically neutral. So charge is exact; `B−L` is not. (This also places QLF in agreement with, not tension with, the quantum-gravity expectation that gravity admits no exact global symmetries.)

**Honest tier.** The Majorana result is **machine-verified**, conditional on two QLF inputs: the assignment neutrino `= ^v`, and antiparticle `=` Hermitian conjugate (the corpus's convention, principled because the operator adjoint reverses order). *Given* those, Majorana is proved, not argued. The remaining physics content — that `0νββ` actually proceeds at a given rate — is the falsifiable empirical claim the experiments test.

## 1a. Which neutrino is Majorana — refinement (2026-10-19)

`^v` is a one-axis closure. The three neutrino mass states are read as closures on 1, 2 and 4 axes,
which are exactly the sizes a closed axis set can have (`QLF_AlphabetNecessity`). Under that reading,
self-conjugacy is decided by counting orderings ([`Lepton_Generations_Fourier.md`](Lepton_Generations_Fourier.md) §6):

- **ν₁ (one axis) must be Majorana.** Every one-axis minimal closure `[t, t†]` is its own antiparticle (`one_axis_majorana`, [`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)).
- **ν₂ (two axes) and ν₃ (four axes) are Dirac in most ways.** Only 8 of 24 two-axis minimal closures are self-conjugate (`twoAxisMinimal_majorana_count`), and 384 of 40,320 four-axis ones. This is a multiplicity, not a necessity.
- **Koide agrees independently.** Applied to the measured splittings, Koide's `Q = 2/3` needs one negative √m, and in normal ordering it works only with that sign on `m₁` (`m = 0.36, 8.62, 50.1 meV`, `Σm ≈ 0.059 eV`; [`lepton_neutrino_koide.py`](lepton_neutrino_koide.py)).

The flavour state `ν_e` is mostly ν₁ (`|U_e1|² ≈ 0.68`), which is why the electron neutrino behaves as
Majorana. The Dirac partners of ν₂ and ν₃ are not free right-handed particles. They are field nodes of
opposite handedness, set near matter by the electrons (Jim's hypothesis; it must reproduce the MSW
strength `√2·G_F·n_e`). The five pre-registered tests with kill conditions are in
`Lepton_Generations_Fourier.md` §6: normal ordering with `Σm ≈ 0.059 eV`, `m_ββ = |U_e1|²·m₁ ≈ 0.25 meV`,
`N_eff = 3`, the MSW strength, and at most a few-percent environment dependence.

This **narrows** §1 rather than contradicting it. `neutrino_majorana` still holds for `^v`, which is now
ν₁. The phrase "the neutrino is Majorana" should be read as "ν₁ is Majorana".

## 2. Beta decay as boundary restructuring

A hadron (like a neutron) is a Markov blanket — a macroscopic context that hides complex fractional logic (quarks) from the surrounding vacuum environment.

A free neutron contains a topological stress (excess bound action) relative to the vacuum. To achieve a more stable bisimilarity with the environment, the neutron must restructure its Markov blanket into a lower-energy proton. (The proton is a net-charge *deficit*, not a free observable: it is completed into a neutral hydrogen-class closure by a negative lepton — and the β-decay event co-produces exactly that completer, the electron below. Which lepton variety completes it — `e⁻`/`μ⁻`/`τ⁻` → hydrogen / muonic / tauonic — is a generation degree of freedom; see [Weak_Force.md](Weak_Force.md) §4a.)

* **The Unspooling:** the neutron opens its topological boundary, unspooling the excess logic.
* **The Ejection:** this logic must immediately resolve to preserve global ZFA. It splits into two unforgeable names:
  1. **The Electron:** a highly chiral, tightly bound ZFA loop (`^<v>`) that carries away the asymmetric logical debt — and being chiral, it has a *distinct* antiparticle (the positron): the electron is Dirac.
  2. **The Majorana Neutrino:** a *non-chiral* loop (`^v`) whose Hermitian conjugate is identical to itself, hence its own antiparticle. It carries away the residual relational momentum without disturbing the chiral balance of the new system.

**β⁺ as the key to the first fusion.** Read forward instead of as decay, the same `u→d` blanket
restructuring is the **fusion-enabling step** of every star. Two identical proton blankets are
Pauli-insulated — `pauli_exclusion` forbids a bound diproton — so the pp-chain's first step
`p + p → ²H + e⁺ + ν_e` *must* convert one proton to a neutron (β⁺) to make the pair distinguishable
before the blankets can join into a deuteron. The weak β⁺ is therefore the precondition for the first
Markov-blanket join, and its weak-mediated rarity is what makes the Sun burn slowly; see
[`Fusion.md`](Fusion.md) §3a and [`SEX.md`](SEX.md) (the deuteron distinguishability condition).

## 3. Neutrino oscillation — a norm-preserving closure rotation

Oscillation is the **slow phase evolution** of the neutrino's three-axis closure. The flavor eigenstates
`ν_e, ν_μ, ν_τ` are different *orientations* of the same twist combinatorics, mixed unitarily by the PMNS
matrix. If all three were Majorana, that mixing would carry `N−1 = 2` extra phases beyond the CKM
count; with only ν₁ Majorana (§1a) the physical count of extra phases is open again (`majorana_phases`, [`lean/QLF_PMNS.lean`](lean/QLF_PMNS.lean); [`Standard_Model.md`](Standard_Model.md) §4.2).
Machine-verified in [`lean/QLF_NeutrinoOscillation.lean`](lean/QLF_NeutrinoOscillation.lean):

- **Driven by fold-depth mass splittings.** In QLF mass is gauge-fold depth, `m = 1/R`
  ([`QLF_HiggsMechanism`](lean/QLF_HiggsMechanism.lean)), so the oscillation phase runs on the
  mass-squared splitting `Δm² = m_i² − m_j² = 1/R_i² − 1/R_j²` (`deltaMSq`). It **vanishes iff the fold
  depths are equal** (`no_oscillation_iff_degenerate`): oscillation *requires* non-degenerate depths — i.e.
  nonzero (Majorana) masses ([`QLF_NeutrinoMass`](lean/QLF_NeutrinoMass.lean)). Degenerate closures don't
  oscillate; the empirical fact that neutrinos *do* oscillate is the statement that their fold depths differ.
- **Unitary — total number conserved.** The two-flavor probabilities `P_surv = 1 − sin²2θ·sin²(Δm²L/4E)`
  and `P_app = sin²2θ·sin²(Δm²L/4E)` sum to `1` (`two_flavor_unitarity`) and lie in `[0,1]`
  (`two_flavor_prob_bounds`), rooted in PMNS unitarity `cos²θ + sin²θ = 1` (`mixing_unitary`). Flavor is
  rotated, not lost.
- **Oscillation is a rotation, not a decay.** Writing the state as a flavor polarization vector `P`, the
  evolution is a **precession** `dP/dt = Ω × P`. Because `P·(Ω×P) = 0` (`dot_cross_self`), `P` is always
  orthogonal to its own rate of change, so `‖P‖²` — the total neutrino number — is **conserved**
  (`flavor_precession_conserves_number`). This is the sharp distinction from §2's β-decay: oscillation
  *reorients* a persisting closure, whereas decay *ends* one (drives it out of ZFA balance,
  [`Decay.md`](Decay.md) §1).

**Turbulence-driven (collective) conversion.** In a dense turbulent cascade the rain of prime `±i`
phase-slips ([`Turbulence.md`](Turbulence.md), [`Decay.md`](Decay.md) §2.1) adds a term
`Γ_p Φ_p(t) S(t)·n̂_prime × P` to the precession — but this only *adds to the rotation axis*
`Ω = ω_vac + κ·n̂_prime`, so it **still conserves neutrino number** (`prime_kick_conserves_number`): the
bath *re-orients and accelerates* the oscillation (rapid, collective flavor conversion — the discrete
analogue of supernova collective oscillations / the collisional flavor instability) without creating or
destroying neutrinos. So the QLF-internal supernova mechanism ([`Decay.md`](Decay.md) §2.4) seeds the
lepton chemistry by *converting* flavor, not by number non-conservation.

**Collective conversion in a dense gas — still number-conserving.** In a supernova core or neutron-star
merger the neutrinos are dense enough that the `νν` refractive potential makes each neutrino's precession
axis a **mean field** built from the whole ensemble — the driver of *collective* flavor conversion (slow
bipolar, fast ELN-crossing, collisional). QLF renders this as the many-body extension of the *same*
rotation: the mean field is just another axis `Ω`, so the single-particle theorem already applies, and the
**total** polarization `P₁+P₂+…` precesses as a whole (`cross_add`, the generator is linear), giving
`dot(ΣP)(Ω×ΣP)=0` — the total neutrino number is **exactly conserved** (`collective_total_conserved`).
Collective conversion rearranges the flavor *distribution*, never the number, matching the standard
conservation laws. And QLF supplies a concrete **seed** the ordinary theory has to assume: correlated
turbulent prime `±i` slips across an ensemble sitting near an ELN crossing act as the discrete seed of the
fast instability, adding a `∝ Φ_p` piece to its growth rate — the collective equations stay of precession
form, only the effective axis/seed is modified. **Open (named formal targets):** the many-body mean-field
limit that recovers the standard `νν` Hamiltonian `H_νν ∼ √2 G_F ∫(1−v̂·v̂')(ϱ−ϱ̄) d³p′`, the discrete
analogue of an **ELN angular crossing** (an imbalance in the distribution of closure orientations), and the
prime-kick strength `κ` / synchronization `S` — left open exactly as the mixing angles and absolute `Δm²`.

**Honest scope.** The oscillation *structure* — unitarity, number conservation, the fold-depth `Δm²`
driver — is machine-verified; the mixing *angles* and the absolute `Δm²` values are the open Yukawa/mass
sector (`pmns_in_progress`), and the *rate* of the prime-driven conversion is the phenomenological
[`prime_cascade_decay.py`](prime_cascade_decay.py) coupling (the open coupling-strength residual).

---

See also: [Annihilation.md](Annihilation.md) — develops the LH `^<v>` vs RH `^>v<` chiral twist patterns as Hermitian pairs whose composition folds to identity (the algebraic content of pair annihilation); the unspooling described in §2 is the same topological unwinding read at the hadron scale. [Weak_Force.md](Weak_Force.md) — consolidates the weak sector and flags the tension that this account mediates β decay by a gauge-fold pair-flip *operation* without an explicit W *particle* (which appears only in the τ-decay vertex). [`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean) — the machine-verified self-conjugacy of the neutrino loop.

## 2026 update

Francis Halzen received the 2026 Nobel Prize for IceCube and astrophysical neutrinos. IceCube's
flavour ratio at Earth is consistent with `1 : 1 : 1`. `flavour_ratio_mu_tau` (`QLF_Discoveries2026`)
proves that any doubly stochastic, μ–τ symmetric mixing sends a pion-decay source `1 : 2 : 0` to exactly
`1 : 1 : 1`. QLF does not yet derive μ–τ symmetry, so this is what the derivation would buy
([Discoveries_2026 §7](Discoveries_2026.md#p7)).
