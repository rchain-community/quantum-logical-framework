# The Weak Force and the W/Z Bosons in [QLF](README.md)

**The weak sector, consolidated — what QLF derives, what it sketches, and what is open, with the honest three-tier discipline of the rest of the corpus.** Previously this content was scattered across [`Higgs.md`](Higgs.md) §4, [`Standard_Model.md`](Standard_Model.md), [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md), and [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §6.

**Headline:** the **group-theoretic identification of the weak-isospin SU(2) inside the 8-twist algebra is machine-verified** (`weak_isospin_su2`, [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean)). The **quantitative** weak sector — W/Z masses, the Weinberg-angle value, the Fermi constant, the flavor-change vertex — remains explicitly open.

---

## 1. The weak force as a gauge-fold pair-flip

The 8-twist alphabet splits `6 spatial (^v<>/\) + 2 gauge (+-)`. The gauge sector (`+`/`−` folds) is what carries charge and generates mass. In QLF the **weak force is the gauge-fold pair-flip** — the operation that flips gauge content — which is exactly what is needed to restructure one closed history into another of different charge (e.g. `n → p`-deficit, co-produced with its completing lepton — §4a). It is **chirality-mediated**: left-handed loops pair into SU(2)-like doublets, right-handed into singlets, a structure inherited from the half-spin Pauli algebra ([`Standard_Model.md`](Standard_Model.md) §3.4, [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md)).

This is the force as an **operation**. Whether it is also carried by an explicit propagator particle in every context is subtle — see §4.

---

## 2. W and Z as charged / neutral gauge-fold closures

| Boson | charge | QLF structure | depth |
|---|---|---|---|
| W⁺ / W⁻ | ±1 | gauge fold with a **net** charge twist | `R_W` |
| Z | 0 | **balanced** (neutral) gauge fold | `R_Z` |
| photon | 0 | pure spatial fold, **no** gauge twist | `R = 0` |

Mass is the constructing delay of a gauge fold, `m = αR` ([`Higgs.md`](Higgs.md) §4, [`E_mc2_derivation.md`](E_mc2_derivation.md)). So `M_W = α R_W`, `M_Z = α R_Z`, and the photon's masslessness is immediate (`R = 0`). The Weinberg angle is reframed as a **depth ratio**:

$$\cos\theta_W = \frac{R_W}{R_Z}$$

**Honest scope.** This is a *reframing* of the tree-level Standard-Model identity `cos θ_W = M_W/M_Z` (PDG: `80.377/91.188 ≈ 0.8814`), not a derivation: `R_W` and `R_Z` are **not** computed from substrate combinatorics. The structural content QLF adds is only that the charged W carries one extra charge twist on top of the neutral gauge structure, so `R_W < R_Z` — i.e. the angle is a depth difference, not a free parameter. The *number* (the depth ratio) is open (§6).

**The unification-scale value — `sin²θ_W = 3/8`.** There is, however, a structural value the alphabet does fix. The spatial fraction of the 8-twist alphabet is `sin²θ_W = (spatial axes)/(alphabet) = 3/8`, which is *exactly* the **SU(5) grand-unification normalization** `sin²θ_W = 3/8` (Georgi–Glashow). It is the **third** electroweak/cosmological constant read off the same `6 spatial + 2 gauge = 8` split that gives `α` (`N = 3² = 9`, [`QLF_FineStructureSubstrate`](lean/QLF_FineStructureSubstrate.lean); canonical doc [**Alpha.md**](Alpha.md)) and `Ω_Λ` (gauge fraction `2/8 = 1/4`, [`QLF_CosmologicalConstant`](lean/QLF_CosmologicalConstant.lean)) — machine-verified together in `electroweak_substrate_signature` ([`lean/QLF_WeinbergAngle.lean`](lean/QLF_WeinbergAngle.lean)), alongside the tree-level `ρ = 1` (`rho_one_of_mass_relation`) and on-shell `cos²θ_W = (M_W/M_Z)²` (`onshell_weinberg`).

> **Honest scope (load-bearing).** `3/8 = 0.375` is the **unification-scale** value, **not** the measured `sin²θ_W(M_Z) ≈ 0.231` — reaching that needs standard renormalization-group running, which QLF does not derive (the open running-couplings sector). So `3/8` coincides with the established GUT normalization (a genuine group-theoretic value, *not* a fit to data — contrast the `δ = 2/9` Koide-phase **candidate** of §5c, which is a numerical near-miss with no structural argument behind it), the substrate's `3/8` matching it is a structural coherence, and the running + the absolute `W/Z` masses / `G_F` (which need the Higgs VEV) stay open (`weinberg_running_in_progress`).

---

## 3. SU(2)_weak ⊂ Σ₈ — machine-verified (group-theoretic)

[`Standard_Model.md`](Standard_Model.md) §3.4 listed "identify the *specific* SU(2) subgroup of the 8-twist algebra" as open. It is closed at the **Lie-algebra / group level.**

QLF's Σ₈ algebra uses `τᵢ = i σᵢ` (the Pauli matrices scaled by `i`), giving quaternionic squares `τᵢ² = −I` and anti-cyclic products `τxτy = −τz` (machine-verified: `tau_x/y/z_sq`, `tau_xy/yz/zx_product`). Adding the reverse products (`τy τx = +τz`, …), the three generators close under the matrix **commutator** into the su(2) ≅ so(3) Lie algebra:

$$[\tau_i,\tau_j] = -2\,\varepsilon_{ijk}\,\tau_k$$
(machine-verified: `tau_comm_xy/yz/zx`, `weak_isospin_su2`)

and the mixed anticommutators vanish (`{τᵢ,τⱼ} = 0`, `tau_anticomm_*`). Together with `τᵢ² = −I`, the multiplicative group they generate is the **quaternion group** `Q₈ = {±I, ±τx, ±τy, ±τz} ⊂ SU(2)` — the discrete subgroup whose continuous closure is exactly the weak-isospin SU(2).

So **the weak-isospin SU(2) is the τ-quaternion subalgebra of Σ₈** — a concrete, machine-verified identification, not an analogy. (The three *spatial* axes `^v / <> / /\` carry the imaginary-quaternion structure; the gauge folds `+-` carry the charge that distinguishes W from Z.)

**Scope (load-bearing):** this is the **algebra/group** identification only. It does **not** derive the SU(2) coupling `g`, the W/Z masses, the Weinberg-angle value, or the symmetry-breaking scale. Those remain open (§6).

---

## 4. Beta decay — and the W-as-operation vs W-as-particle tension

QLF's account of beta decay ([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md)) is **boundary restructuring**, and — read directly — it **never names the W as a particle**. A free neutron carries topological stress; it relieves it by *unspooling* its Markov-blanket boundary into a **proton** (itself a net-charge *deficit*, not a free observable — see §4a) plus two ejected unforgeable names:

- the **electron** — a highly chiral ZFA loop, `^<v>` (left-handed) vs `^>v<` (right-handed), carrying the asymmetric logical debt;
- the **Majorana neutrino** — a *non-chiral* loop (`^v`) that is its own antiparticle: it is a fixed point of the Hermitian conjugate (conjugate-and-reverse), machine-verified `neutrino_majorana` ([`lean/QLF_Majorana.lean`](lean/QLF_Majorana.lean)). Being self-conjugate, lepton number is violated — a falsifiable QLF commitment: **neutrinoless double-beta decay** ([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) §1).

Concrete anchor: the chiral electron loop `^<v>` is exactly the cross-axis **interleaved closure** machine-verified this cycle — `interleaved_xlvr_folds_to_negI` (`σ_y·−σ_x·−σ_y·σ_x = −I`) in [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean) — a count-balanced ZFA closure that the keystone `count_balanced_pauli_closed` covers.

**The tension, stated plainly.** In QLF, beta decay is mediated by the gauge-fold pair-flip *operation* — the W as a **process**, not an explicit exchanged particle. The W as a **particle** appears explicitly only in the τ-decay vertex (§5). Reconciling the two readings — is the propagator W just the virtual realization of the pair-flip operation, with `R_W` setting its range? — is taken up in **§4c**, which proposes that the two are the same relation at two resolutions.

### 4a. The "proton" is a deficit — the observable is the lepton-balanced atom

It is tempting (and the β-decay accounts do this) to say the neutron decays *into a proton*. But by QLF's own rule — **charged particles do not exist independently** ([`HadronicDepth.md`](HadronicDepth.md) §2.1, [`Electron.md`](Electron.md), [`Bound_States_QLF.md`](Bound_States_QLF.md)) — a bare proton is a net-charge deficit (`count(+) − count(−) = +1`), an *open* Hermitian/gauge half, **not** a completed ZFA closure. The proton is an observable only once its deficit is completed by a counter-charge into a **neutral joint closure**. So wherever the weak sector says "proton" as a stand-alone product, the conceptually correct object is the **closed hydrogen-class atom**.

What makes β decay clean here: it **co-produces the completer**. The same unspooling that leaves a proton-deficit also ejects the electron whose `−1` exactly cancels it — i.e. the *constituents of a neutral (hydrogen-class) closure*, born together, so global neutrality is preserved by construction (`m_p` should be read as `m_H`, a 0.05 % wash, per [`HadronicDepth.md`](HadronicDepth.md) §2.1). The neutral neutron does not produce a free charge; it produces a deficit **and** its completer (the electron), plus the Majorana neutrino.

**The completing lepton's *variety* is a weak / generation degree of freedom.** Exactly as the electron's deficit can be completed by a positron (**positronium**), an antimuon (**muonium**), or a proton (**hydrogen**) ([`Electron.md`](Electron.md), [`Bound_States_QLF.md`](Bound_States_QLF.md)), the **proton's** deficit can be completed by any negative lepton:

| completing lepton | neutral closure | note |
|---|---|---|
| `e⁻` | ordinary hydrogen | the lightest, stable completer |
| `μ⁻` | muonic hydrogen (`pμ⁻`) | deeper-blanket lepton; bound but short-lived |
| `τ⁻` | "tauonic hydrogen" | deepest-blanket lepton — too short-lived to bind |

So "which lepton variety closes the proton" is a **generation** choice, and the deepest variety (τ) is precisely the one whose completion cannot bind — which is *why* the τ is handled not as a bound atom but as the decay-vertex object of §5. This makes the lepton generation an **output of the weak vertex**: the same pair-flip that flips the baryon charge (`n → p`-deficit) also fixes the flavor of the co-produced completing lepton. The variety is weak-sector data, not a free label.

---

### 4b. Electron capture — the same pair-flip, run the other way

β decay converts a neutron into a proton-deficit plus its completer. The **inverse** process runs
the identical gauge-fold pair-flip in the opposite direction:

```
    β⁻ decay      n → p + e⁻ + ν̄        (d → u, the completer ejected)
    e⁻ capture    p + e⁻ → n + ν_e       (u → d, the completer absorbed)
```

Both are one operation — the weak pair-flip of §1 — read in two directions, and §4a is why the
reverse reads so naturally here. A bare proton is a *deficit*; the observable is the neutral
`B = 1` content, ordinarily realized as the hydrogen-class closure with the electron **outside**.
Electron capture is that same neutral content finding a **different, deeper closure of itself**,
with the `−1` folded **in** — exactly the contrast [`proton_neutron_demo.py`](proton_neutron_demo.py)
draws: *hydrogen = `uud` + electron outside; neutron = `udd`, the `−1` folded in (one `u → d`)*.
Nothing is destroyed and nothing is created; one quark flips and the neutral closure reorganizes.

Nothing is smuggled in, either — the electron is not a pre-existing little object pushed inside
the baryon. The **joint** `p + e⁻` closure restructures: the baryon's flavour content changes
`uud → udd`, and the neutrino carries off the residual weak relation.

**What is conserved, stated exactly.** Electric charge: `(+1) + (−1) = 0 → 0`. Baryon number:
`1 → 1` — the signed 3-axis winding is untouched (`baryonNumber`,
[`lean/QLF_BaryonWinding.lean`](lean/QLF_BaryonWinding.lean)), which is what makes this
**not proton decay**. Lepton number is a different matter and QLF has already committed: the
neutrino is Majorana, so it carries no conserved lepton charge and `L` is not exact
([`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) §1). Nothing here needs `L`.

**It costs, which is the whole point.** For a *free* proton and electron the neutron is heavier:

```
    m_n − (m_p + m_e) ≈ 939.565 − 938.272 − 0.511 ≈ 0.782 MeV
```

so capture cannot happen spontaneously — ordinary hydrogen is stable precisely because the shallow
closure is the only one its energy budget reaches. Supply that `0.782 MeV`, by heat or by
compression, and a **deeper closure of the same neutral content becomes available**. That is the
capacity reading, and [`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4a.1 takes it up: a closure
can stay protected against decay and still be transformable once it is a constituent of a
higher-capacity joint event. Where nature does this at scale is
[`Decay.md`](Decay.md) §2.4a — stellar collapse, and the neutron star it leaves.

---

### 4c. W as operation and W as particle — two resolutions of one relation

§4 left a tension: QLF reads the weak interaction as a pair-flip *operation*, while the W appears as
a *particle* at the τ vertex. Electron capture is where the two can be reconciled, because resolving
its single vertex splits it in two:

```
    coarse:   e⁻ + u → ν + d                    one joint weak closure
    resolved: e⁻ → ν + W⁻*    and    u + W⁻* → d
```

**The mediator's charge is not put in by hand — it is over-determined.** Each half fixes it alone,
from data the other half never sees:

| half | equation | forces |
|---|---|---|
| lepton | `q_e = q_ν + q_W` | `−1 = 0 + q_W` ⟹ `q_W = −1` |
| quark | `q_u + q_W = q_d` | `2/3 + q_W = −1/3` ⟹ `q_W = −1` |

Two independent computations, one answer. Machine-verified as
`wminus_charge_from_lepton_vertex`, `wminus_charge_from_quark_vertex`, and
`electron_capture_factors_through_wminus` (there is **exactly one** charge making both vertices
work) in [`lean/QLF_ChargeBalance.lean`](lean/QLF_ChargeBalance.lean). So the direct pair-flip
bookkeeping of §4b **factors through** a charged intermediate relation rather than merely tolerating
one, and the W is not an arbitrary extra object: it carries precisely the unit the `u → d` flip
costs and precisely the unit the electron gives up in becoming a neutrino.

**The proposed resolution, and it comes from QLF's own rule rather than from field theory.** §4a
insists a net-charge object is an **open** gauge half, not a completed ZFA closure. A `W⁻` carries a
net charge twist. By QLF's own rule, then, a `W⁻` *cannot* be an independently completed closure —
it is exactly the kind of thing that must be completed by the event containing it:

```
    (e⁻ + u)  →  [ e⁻→ν  |  W⁻*  |  u→d ]  →  (ν + d)
```

**The whole event closes; the internal relation need not.** That is not an evasion — it is the same
statement quantum field theory makes when it says a virtual particle is not an asymptotic
observable, arrived at here from the charge-completion rule instead of from a propagator.

And the two readings then differ only by **capacity**, the same ladder as
[`Law_Of_Exceptions.md`](Law_Of_Exceptions.md) §4a.1:

| capacity | what the weak relation is |
|---|---|
| `E ≪ M_W` | an **internal open relation** of a larger closure — the pair-flip *operation*, no separate object |
| `E ≳ M_W` | enough to let that relation **close on its own** — a real, briefly-existing W *particle* |

So *W as operation* and *W as particle* are one relation at two resolutions, and which you see is a
capacity question rather than a choice of story. A consistency check that costs nothing: QLF's rule
also predicts a lone `W⁻` is never an isolated observable, and it never is — real W production is
always charge-balanced globally.

**This corrects §2's wording.** That table calls `W±` a "gauge-fold **closure**" with a net charge
twist; by §4a's rule a net-charged fold is an open half. Read §2 as describing the *fold structure*
and its depth `R_W`, with completion supplied by the event the fold sits in — not as a claim that a
charged W is a completed closure standing alone.

**Honest scope, at three strengths.** *Proved:* the charge bookkeeping factors through a unique
`−1` relation, over-determined from both sides. *Structural proposal:* `W*` as the internal open
gauge relation of the joint closure, with a real W the case where capacity lets it close — this is a
reading that fits QLF's existing commitments, not a theorem. *Open, and untouched by any of it:* the
W's twist topology, `M_W`, `G_F`, the propagator, and every transition rate (§6). Nothing here
computes a weak amplitude.

---

## 5. The τ-decay vertex — where the W is the named blocker

The electron and muon are handled as two-body bound-state ("Bohr") half-loop closures. The **τ breaks this pattern**: it is too short-lived for bound-state binding. Its decay `τ⁻ → ν_τ + W⁻` is a **multi-body joint ZFA closure** (one in, several out) that fires at an energetic threshold, and the **W's QLF closure topology is the named missing piece** needed to derive `m_τ` ([`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §6, [`Bound_States_QLF.md`](Bound_States_QLF.md) §4). So the W is not peripheral — it is the structural blocker for completing the lepton mass spectrum.

### 5a. Attempt — the τ as the deepest generation phase (a Koide-structured mass)

§4a left the τ as "the lepton variety whose completion can't bind." That gives a handle on its **mass**, via the one near-exact empirical relation among the charged leptons — the **Koide relation**:

$$Q \;=\; \frac{m_e + m_\mu + m_\tau}{\left(\sqrt{m_e} + \sqrt{m_\mu} + \sqrt{m_\tau}\right)^2} \;=\; \tfrac{2}{3}$$

(measured 0.6666605 — 0.0009% from 2/3)

**The QLF reading.** `Q = 2/3` is *exactly* equivalent to writing the three √-masses as three phases 120° apart on a circle of radius `√2·M`:

$$\sqrt{m_k} \;=\; M\bigl(1 + \sqrt{2}\,\cos(\delta + \tfrac{2\pi k}{3})\bigr),\qquad k = 0,1,2.$$

Two QLF structures fall directly onto this form:
- the **`2/3`** is the **transverse-axis fraction** — 2 of 3 spatial axes carry the closure (the 6-twist = 2 transverse + 1 longitudinal per axis), the *same* `2/3` as the Lamb prefactor (§5 of [`Lamb_Shift.md`](Lamb_Shift.md)) and the photon polarization sum;
- the **three 120°-spaced phases** are QLF's recurring "three" — the three spatial axes (cf. `N = 9 = 3²` in the α derivation, the three-quark Borromean closure). The three lepton generations are three *phases* of one gauge-fold closure, not three lengths. (This refines the qualitative `N = 4/8/12` loop-length picture of [`Primordial_Entanglement.md`](Primordial_Entanglement.md) §2, which gives the ordering but not the ratios.)

**The payoff (reproducible — [`koide_tau_demo.py`](koide_tau_demo.py)).** If QLF supplies `Q = 2/3` structurally, then `m_e` and `m_μ` **predict** the third-generation mass:

$$m_\tau \;=\; 1776.97\ \text{MeV}\quad\text{vs measured } 1776.86\ \text{MeV}$$

(0.006% agreement)

Only the `2/3` is structural; `m_e, m_μ` are inputs — so this is a *parameter-light prediction* of `m_τ`, the first quantitative handle QLF has on the third-generation mass (previously "no quantitative match", [`Standard_Model.md`](Standard_Model.md) §4.1).

**The τ-decay vertex, in this reading.** The τ is the deepest phase (largest √m). Being the variety that cannot bind (§4a), it appears not as a bound atom but as the weak **decay vertex** `τ⁻ → ν_τ + W⁻`, un-spooling the deepest generation phase into lighter generations + neutrino — and the energetic threshold the vertex satisfies *is* `m_τ`, pinned to ~0.006% by the Koide/transverse-fraction structure. So the "named blocker" has moved from "no handle" to "a structural mass + a vertex reading," with a clear residual open list (below).

**Honest scope (load-bearing).** The overall phase offset `δ` (the Koide angle `≈ 0.2222220` rad, §5c) and the scale `M` are **not** explained — they are why `m_e, m_μ` must still be inputs. And this is the charged-**lepton** sector only; quark generations and CKM are separate. The `Q = 2/3` itself, however, is no longer just an identification — it is **derived** (§5b).

### 5b. Deriving `Q = 2/3` from the closure

The Koide form `√mₖ = M(1 + A·cos(δ + 2πk/N))` — `N` generations as `N` balanced phases of amplitude `A` — gives, by `Σcos = 0` and `Σcos² = N/2`,

$$Q \;=\; \frac{\sum m_k}{\left(\sum \sqrt{m_k}\right)^2} \;=\; \frac{1 + A^2/2}{N}.$$

So `Q = 2/3` follows by construction from **exactly two** structural facts:

| input | value | QLF meaning |
|---|---|---|
| `N` | `3` | three generations = the **three spatial axes** |
| `A²` | `2` | amplitude `√2` = the **two transverse axes** (the one longitudinal axis is the common `1` baseline) |

and nothing else — the counterfactuals are sharp (only `N=3 ∧ A²=2` hits `2/3`):

| `N` | `A²` | `Q = (1+A²/2)/N` |
|---|---|---|
| **3** | **2** | **0.6667 ✓** |
| 2 | 2 | 1.0000 |
| 4 | 2 | 0.5000 |
| 3 | 1 | 0.5000 |
| 3 | 3 | 0.8333 |

So **Koide's `2/3` is QLF's `2 transverse + 1 longitudinal` split over `3` axes** — the *same* split that produces the transverse fraction `2/3` in the Lamb prefactor and the photon polarization sum. The algebra is **machine-verified**: `koide_three_phase` / `koide_two_thirds` ([`lean/QLF_Koide.lean`](lean/QLF_Koide.lean)) prove `3·Σs² = 2·(Σs)²` (hence `Q = 2/3`) from `r² = 2 ∧ Σc = 0 ∧ Σc² = 3/2`, and `koide_phase_witness` shows those hypotheses are satisfiable.

What remains an **identification** (not a proof) is one sharp physical claim: that the lepton `√`-mass vector decomposes as `1` longitudinal baseline `+ 2` transverse 120°-phased oscillations across the `3` generation-axes. That is a far tighter conjecture than "`2/3` happens to match" — it pins the *entire* structure (`N=3`, `A=√2`, balanced phases) to the substrate's `6 = 2+1`-per-axis geometry, leaving only `δ` and `M` as inputs. Demo: [`koide_tau_demo.py`](koide_tau_demo.py) §3b.

### 5c. The Koide angle `δ` — the genuine input (and a `2/9` candidate)

With `Q = 2/3` derived (§5b), the three lepton masses are fixed by **two** inputs: the scale `M` and the overall phase offset `δ` (the Koide angle) — equivalently, `m_e` and `m_μ`. Solving the exact-`Q=2/3` form `√mₖ = M(1 + √2·cos(δ + 2πk/3))` for the measured ratio `m_μ/m_e = 206.768282988` pins

$$\delta = 0.222222047\ \text{rad}.$$

The candidate `δ = 2/9 = 0.222222222…` is `7.9 × 10⁻⁷` away in relative terms. **That figure is conditional and is not the honest precision** — see *Honest precision* below, where the free-fit systematic (`3.4 × 10⁻⁵`) is shown to swamp it by `43×`. The older QLF reading of `2/9 = 2/3²` as **(2 transverse axes) / (9 = 3² directional-coupling tensor)** — the `N = 9 = 3²` that fixes α ([`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1) — is **superseded**: the `9` factorises the other way (below).

As a **zero-parameter prediction of the lepton mass ratios** (`δ = 2/9` fixed, `m_e` supplying only the overall scale):

| quantity | `δ = 2/9` predicts | measured | residual |
|---|---|---|---|
| `m_μ/m_e` | `206.770316` | `206.768283` | **`+9.8 ppm`** |
| `m_τ` | `1776.985 MeV` | `1776.86 ± 0.12` | `+0.007 %` = **`1.04 σ`** |

The `9.8 ppm` on `m_μ/m_e` is nominally ~450σ of *that ratio's* experimental error — but it is **not** a `450σ` exclusion of `2/9`. It is the one place where the three-phase picture's overall `~10⁻⁵` defect surfaces in an observable measured to `10⁻⁸`, and Koide's own `Q` misses `2/3` by `9.23 × 10⁻⁶` against this `9.83 × 10⁻⁶` — the same number to within 6%. One common `~10⁻⁵` correction, not two independent failures.

**`2/9` is the wrong object to derive.** The phase `δ` is a **Z₃ gauge parameter**: `δ → δ + 2π/3` permutes the three phases, hence merely relabels the generations, hence leaves the spectrum *identical* (verified exactly, [`lepton_blind_classifier.py`](lepton_blind_classifier.py) §C1). So `δ` is defined only mod `2π/3`, and every physical invariant is a function of

$$\Delta \;\equiv\; 3\delta \;=\; 2/3 .$$

This is visible in the moment expansion: `Σcos = 0` and `Σcos² = 3/2` are `δ`-independent, and the **third** power sum is the first that sees the phase — through `cos(3δ)` alone. Two consequences:

- The `9` in `2/9` is **not one count**. It factorises as `9 = 3` (generations, already carried by `Q`) `× 3` (the Z₃ quotient). Reading it as "`3²` directional couplings, the same `9` that fixes α" matches the right number to the **wrong decomposition**.
- It explains why the phase is a *pure number* rather than a multiple of `π` — the natural target of suspicion. `Δ` is a ratio of invariants; the `1/3` is a quotient, not an angle.

**A proposed reduction `Δ = Q` — and its refutation.** The target `Δ = 2/3` is numerically the Koide invariant `Q = 2/3`, which invites reading them as one relation ("the Z₃-invariant generation phase equals the Koide invariant"), so that the derived `Q = 2/3` would *yield* `Δ = 2/3` and two magic numbers would collapse to one. **That reduction is false.** `Δ` and `Q` are independent functions on mass-triple space:

- Sample mass triples conditioned on `Q = 2/3` (±0.001): `Δ` spans `0.18 … 0.78`, median `0.71`, with only **6%** landing within `0.01` of `2/3`. Knowing `Q = 2/3` tells you essentially nothing about `Δ`.
- The sharpest single counterexample is real: the `(c, b, t)` triple has `Q = 0.6694` — within `0.4%` of `2/3` — yet `Δ = 0.2060`, a factor of **`3.24`** away. A family with Koide's invariant at `2/3` whose phase is nowhere near it.

(The `(c,b,t)` masses are scheme-dependent parameters, not observables, per §5d — but that objection does not apply here. The claim being tested is the *mathematical* one, whether `Q` determines `Δ` as functions of a triple of positive reals; the 4000-sample conditional test uses purely random triples and no physics at all.)

So `Δ = 2/3` and `Q = 2/3` are **two independent facts**, not one. The earlier "`|Δ − Q| = 2.8 × 10⁻⁵` while random triples give `O(1)`" observation is real but does not establish a relation — it is what "both happen to equal `2/3`" looks like. `Q = 2/3` is derived (§5b); `Δ = 2/3` is **not**, and is not implied by it.

What can honestly be said is weaker: the substrate's transverse fraction `2/3` appears **twice** — once in the amplitude sector (`A² = 2 ⟹ Q = 2/3`) and once, independently, in the phase sector (`Δ = 2/3`). That is a structural coherence of the same kind as `sin²θ_W = 3/8` matching the SU(5) normalization (§2) — suggestive, unfitted, and **not a derivation of either**.

**Honest precision — the `10⁻⁷` agreement is not evidence.** The `7.9 × 10⁻⁷` figure above is obtained *conditional on `Q = 2/3` exactly*. Extracting `δ` instead from a free three-parameter fit to the three measured masses (assuming nothing, not even `Q`) gives `δ = 0.2222296` — a **systematic of `3.4 × 10⁻⁵`** between the two legitimate extractions, `43×` larger than the celebrated agreement. The whole three-phase picture is only accurate to `~10⁻⁵` (the `Q` defect). So:

> **`δ = 2/9` holds at `10⁻⁵`, and no better.** Chasing the seventh digit is chasing an artefact of assuming `Q = 2/3`.

At that honest precision, with experimental errors propagated (dominated by `m_τ = 1776.86 ± 0.12`), the free fit gives `A² = 1.999963 ± 0.000041` and `Δ = 0.666689 ± 0.000025` — so `A² = 2` sits at `−0.91 σ` and `Δ = 2/3` at `+0.89 σ`. **Neither is excluded.**

**What cannot supply the phase.** The Pauli fold **cannot**: the fold group is `μ₄ = {±I, ±iI}`, the half-spin signature is one bit (`−I` vs `+I`), and the free-energy quantum is one bit (`ΔF = −log 2`). A *finite* group has no continuous parameter, so no amount of fold structure yields a real angle. One-bit precision does do one useful thing — it sets the resolution floor, which is exactly what rules the `10⁻⁷` chase out of court. A derivation must therefore produce `Δ = 2/3` as a ratio of **census counts** with the Z₃ quotient already built in. **Not derived. Consistent, reduced, and open.**

### 5c′. The residual: one number, and a much larger puzzle behind it

**There is no "common `10⁻⁵` correction to `Q` and `Δ`."** That was an over-reading. With experimental errors propagated, both defects are `m_τ` noise:

| | defect | uncertainty | |
|---|---|---|---|
| `A² − 2` | `−3.69 × 10⁻⁵` | `± 4.1 × 10⁻⁵` | `−0.91 σ` — **not significant** |
| `Δ − 2/3` | `+2.22 × 10⁻⁵` | `± 2.5 × 10⁻⁵` | `+0.89 σ` — **not significant** |
| `m_μ/m_e` | `+9.83 × 10⁻⁶` | `± 2.2 × 10⁻⁸` | `+452 σ` — **significant** |

Exactly **one** number appears to need explaining: the model (`A² = 2` *and* `Δ = 2/3` both exact, `M` the only freedom) overpredicts `m_μ/m_e` by **`+9.83 ppm`**. (**Superseded by §5c⁗:** that `452σ` is measured against the *ratio's* experimental error while the model's own knowledge of `Δ` — `3.4 × 10⁻⁵` — covers `±424 ppm`, because the electron sits next to a zero of the three-phase form and amplifies by `12.5`. The residual is `2.3%` of the model's own band, and is **retired**. The paragraph below is retained for the locus it identifies, which remains the right place to look if a correction is ever needed.) The locus is the **e–μ sector** — which is also where the blind ladder carries its one structural asymmetry: `e = ^<v>` and `μ = ^^<vv>` share axis content `{x,y}`, while only `τ = ^^</>vv\` engages `z` ([`lepton_blind_classifier.py`](lepton_blind_classifier.py) §A). The symmetric three-phase ansatz treats all three alike; the substrate does not. Suggestive of where a correction lives — **not** a calculation of it.

**The larger puzzle: why the relation survives radiative corrections at all.** `Q` is invariant under `mₖ → c·mₖ`, so flavour-*universal* corrections cancel exactly; only the flavour-dependent `log mₖ` terms can move it. Those are not small — `(α/π)·ln(m_μ/m_e) ≈ 1.24 × 10⁻²`. Running the pole masses to a common scale with one-loop QED gives

$$Q_{\text{running}} - 2/3 \;\approx\; +1.13 \times 10^{-3},$$

**183× worse than the pole-mass defect** of `−6.2 × 10⁻⁶`. And there is **no scale that rescues it**: the `μ`-dependence enters as a common `ln μ` factor, which cancels in `Q`, so `Q_running` is essentially scale-*independent* and never returns to `2/3` (verified from `1 MeV` to `10¹² MeV`, §D). **Koide is a pole-mass relation, full stop.**

So the real question is not "where does `9.8 ppm` come from" but **"why is the `1.1 × 10⁻³` absent"** — a discrepancy 115× larger. This is the long-standing Koide puzzle (it is what Sumino's family-gauge cancellation was built to address).

**QLF already answers that one — and was committed to the answer before the question arose.** §5d's principle is that *only observables carry physical mass*: the quoted quark masses are "scheme-dependent *running* Lagrangian parameters (MS-bar at a chosen scale), never measured," which is why QLF **predicts** clean mass relations live among the observables and are absent among the quark parameters. The pole mass is the on-shell, gauge-invariant, IR-complete observable — precisely what a ZFA closure *is*. A running mass is bookkeeping. So the substrate relation must hold for **pole** masses, and the `183×` preference for pole over running is that prediction confirmed. One principle — observables are physical, schemes are not — yields both the *failure* of quark-Koide (§5d) and the *pole-mass form* of lepton-Koide. Neither was fitted.

**The `9.83 ppm` itself is not derived, and is not being fitted.** Candidates checked and **rejected**: `1/(24·48·96)` from the blind-ladder orbit sizes (`9.04 × 10⁻⁶`, 8% off — an exact census count must come out *exact*, so an 8% miss is a failure, not a near-miss); `2(α/π)²` (10% off); `α²/2π` (14% off). With `α`, `π` and small rationals, any single number can be matched to a few percent; that is not evidence and none of these are carried as candidates. **Open.**

### 5c″. `Δ = 2/3` is the muon-to-electron mass ratio

With `A² = 2` derived (§5b), the three-phase form has parameters `(M, Δ)`. `M` is the overall scale, so **`Δ` is the sole remaining ratio freedom** — fixing it fixes every dimensionless charged-lepton mass ratio:

| `Δ` | `m_μ/m_e` | `m_τ/m_e` |
|---|---|---|
| `0.6400` | `131.13` | `2304.6` |
| **`2/3`** | **`206.7703`** | **`3477.47`** |
| `0.6900` | `334.49` | `5415.7` |
| *measured* | `206.7683` | `3477.23` |

So **"derive `Δ = 2/3`" and "derive `m_μ/m_e = 206.77`" are the same statement in different coordinates.** That is the honest difficulty class: the muon-to-electron mass ratio, which no framework has derived. Writing it as a phase makes it look like an angle waiting for a geometric argument; it is not. **Not derived.**

**A negative result on the blind ladder.** The rooted causal ladder `e = ^<v>` → `μ = ^^<vv>` → `τ = ^^</>vv\` ([`lepton_blind_classifier.py`](lepton_blind_classifier.py) §A) selects each rung by *unique parented continuation*: at `L = 8`, exactly 1 of the 2 three-axis candidates has a causal parent in the μ orbit. Carried to the next rung, **the rule fails to select**: at `L = 10` there are 105 three-axis candidates, **12** with a causal parent in the τ orbit, and **4** matching τ's exact degree signature (every rooted history having exactly one parent). Neither `0` — which would confirm the ladder terminates at three generations — nor `1`, a fourth generation.

So the `L = 8` uniqueness is plausibly a small-numbers accident, and **this ladder is not an independent derivation of "exactly three generations."** QLF's generation-count claim rests on [`QLF_Generations`](lean/QLF_Generations.lean) (generation count = `substrate_spatial_dimension` = 3), which this does not touch; what fails is the combinatorial ladder as a *second, independent* argument for it.

**And the `L = 8` rung is less blind than it looks.** Part A filters to three-axis classes *before* applying the parent rule. Drop that filter and **9 of the 12** `L = 8` classes have a causal parent in the μ orbit — not one — with three sharing the degree-`{1:n}` signature. So the **three-axis criterion is load-bearing** in the τ selection: it is an imposed structural assumption, not an output of the search. (It is not a *mass* input, so the blind-test discipline is intact — but it is an assumption and is labelled as one.)

### 5c‴. The `(R, axis) → mass-ratio` map — a shape theorem

The map [#140](https://github.com/jimscarver/quantum-logical-framework/issues/140) originally asked for does **not exist in the form requested.** Every census integer at the three rungs is 5-smooth (`L = 4,6,8`; `orbit = ways = 24,48,96`; `axes = 2,2,3`; `conj-pairs = 2,5,6`; `parent-edges = 192,96`), hence so is every product and ratio of them — but the mass ratios are not: the closest small-exponent `2^a3^b5^c` misses `m_μ/m_e` by `0.286%`, `m_τ/m_e` by `0.610%`, `m_τ/m_μ` by `0.232%`, orders of magnitude outside the `10⁻⁵` at which the three-phase picture holds, and a 64 000-expression brute search over the census pool does no better. A real negative, not a failed fit.

**So the map must factor: `census → Δ → masses`.** Analytically the ratios are cosine values at an `O(1)` phase, transcendental in `Δ`, which a census cannot produce directly — only the phase, with the cosine doing the rest; structurally, any correct map must reproduce the derived `Q = 2/3`, automatic for a map onto `(M, Δ)` and accidental for one onto three independent masses. **The ask is thereby reshaped from three masses to one small rational, which is well posed** — that reshaping is the result. Whether a census can then *reach* that rational is answered in §5c⁗: no.

> **Arithmetic note (why an older `δ = 0.22227` was wrong).** That value comes from extracting `δ` from the **τ** channel alone using `M = (Σ√m)/3` over all three *measured* masses. Because measured `Q ≠ 2/3`, the three single-channel extractions disagree in the fifth decimal — `0.222270` (τ), `0.222233` (μ), `0.222221` (e) — so no one of them is "the phase `m_e, m_μ` demand." The two-input solve of §5c is the well-posed determination. Reproduce with [`lepton_blind_classifier.py`](lepton_blind_classifier.py) §B.

### 5c⁗. Deriving `Δ = 2/3` — what stands, what is closed, and the specification that remains

`Δ` is the sole remaining ratio freedom (§5c″), so this is where the lepton sector's open work is. Seven rounds of attack are recorded in [#140](https://github.com/jimscarver/quantum-logical-framework/issues/140); this section keeps the **results** and delegates the dead ends to a list. All of it is reproducible with [`lepton_blind_classifier.py`](lepton_blind_classifier.py) (parts H–N).

**1. The hierarchy needs no large number.** `1 + √2·cos θ = 0` at `θ = 3π/4` **exactly** — a massless wall. At `Δ = 2/3` the electron's phase sits `2.2676°` from it, and `√m_e/M = 0.040350` **is** that angular deficit to first order. The heaviest/lightest amplitude ratio is `58.970`; squared, `3477.5` against the measured `m_τ/m_e = 3477.2`. So the `~3500×` lepton hierarchy is **proximity to a wall, quadratically amplified** — not a hierarchy of scales, and not a fine-tuning: the deficit is `15.1%` of the available gap `π/12`, an `O(1)` fraction.

**2. And the wall exists only because `A² = 2`.** `1 + A·cos θ` has a zero **iff** `A ≥ 1`; below that the spectrum is capped for *every* phase at `((1+A)/(1−A))²` — `34×` at `A² = 1/2`, `9×` at `A² = 1/4`, against a measured `3477` that needs `A² ≥ 0.934`. `A² = 2` is **derived** (the two transverse axes of the `6 = 2+1` split, §5b), so **the substrate geometry is what makes a lepton hierarchy possible at all** — not its value, but its existence.

**3. The `+9.83 ppm` residual is retired.** The near-zero amplifies: `d ln(m_μ/m_e)/d ln Δ = 12.48`. §5c knows `Δ` only to `3.4 × 10⁻⁵`, which propagates to **`±424 ppm`** on `m_μ/m_e` — so the residual is `2.3%` of the model's own uncertainty band, and `43×` inside the systematic in the phase coordinate. §5c′'s `452σ` measured it against the *ratio's* experimental error while ignoring the model's own input precision. Not evidence of missing structure. (This does not *verify* the ansatz to `424 ppm`; the discrepancy simply sits inside its own resolution.)

**4. The specification any derivation must meet.** Two constraints, both earned:

- **`O(1) rational in radians.`** `Δ = 2/3` is 5-smooth in **radians alone** — as a fraction of a turn it is `1/(3π)`, transcendental, and the smallest turn-fraction fitting the data has denominator `311`. So no division of the circle can produce it; only an arc-over-radius (curvature-shaped) reading survives.
- **Forced, not selected.** Pricing hypothesis classes by description length, `Δ = 2/3` costs `log₂6 = 2.58` bits and already sits at the experimental floor, where circle-division needs `14` bits and improves at every budget on the way. Hence the criterion that has done most of the work here: **a derivation costing more bits than the constant it derives is a re-encoding, not a derivation.** Any route offering a menu of `N` options costs `log₂N` bits and must beat `3`.
- **Not a dynamics on the phase circle.** A rotation number is a fraction of a *turn*, and by the first clause `Δ` is `1/(3π)` of one — so no circle map on the generation-phase circle can mode-lock at it (§6, the closing of the last candidate). Whatever produces `Δ` must produce a rational number of **radians**, and the only quantity with that unit is an arc over a radius: `n` unit steps at integer radius `R`. That fixes the *shape* of any future candidate before it is written down.

**5. Closed routes.** Each was attacked and failed; details in [#140](https://github.com/jimscarver/quantum-logical-framework/issues/140).

| route | why it is closed |
|---|---|
| `δ = 2/9` as the target | `δ` is Z₃ gauge; only `Δ = 3δ` is physical, and the `10⁻⁷` agreement is an artefact of assuming `Q = 2/3` |
| `Δ = Q` (two magic numbers → one) | **refuted** — independent functions on mass-triple space; `(c,b,t)` has `Q` within `0.4%` of `2/3` and `Δ` a factor `3.24` away |
| a direct `(R, axis) → mass-ratio` map | census integers are 5-smooth, the mass ratios are not (`0.14–0.61%` off); must factor through `Δ` |
| a census count-ratio for `Δ` | costs `3.7–4.1` bits against the constant's `3` — a re-encoding. And `(e,μ,τ)` axis counts `(2,2,3)` are circular: `τ`'s `3` is imposed by a filter |
| any division of the circle | as a turn-fraction the phase is `1/(3π)`; smallest fitting denominator `311` |
| curvature on the ladder closures | rung-independent ratios are exactly `{1/2, 1, 2}`; `2/3` absent, and `runs/dim` is not rung-independent |
| all three QLF curvature notions | holonomy (`μ₄`) and pentamon deficit are divisions of the turn; Ollivier–Ricci gives no positive interior curvature and no `2/3` ([`Curvature.md`](Curvature.md) §1c) |
| `ε = 0.0396` as a better coordinate | `ε = π/12 − 2/9` — a transcendental minus a rational, algebraically *worse* than `Δ` |
| extremizing a symmetric functional | with `A² = 2`, `e₁` and `e₂` are fixed, so every one is a function of `cos Δ` alone; `0` of `8` pre-registered candidates stationary at `2/3` |
| an absolute mass scale | `ε` is dimensionless and `M` is free, so no absolute-mass statement constrains it |
| `Δ = (2π/3)/π` | the `π` cancels **trivially** — `2/3` rewritten at identical bit cost. Every rational is a ratio of commensurable angles |
| `Δ` as a mode-locked **rotation number** | a rotation number is a turn-fraction; `Δ` is `2/3` of a *radian* = `1/(3π)` turns, and the smallest rational turn-fraction the data admits is `33/311` — the *narrowest* tongue (`~10⁻³⁰` of the `2/3` tongue below criticality, `~2 × 10⁵×` narrower even at `K = 1`), not the widest. The one escape (lock on another circle, convert at "1 rad per turn") is the unit smuggling of the first row. Part N |

**6. The last candidate, closed — and what it leaves behind.** `Δ` as a mode-locked **rotation number** was the one route that seemed to *fit* §4 rather than be excluded by it: rotation numbers are `O(1)` rationals, the locking is forced by the dynamics, and `2/3` has Stern-Brocot depth `2` — one of the widest Arnold tongues. It fails on units. A rotation number counts **turns** per iterate; `ρ = 2/3` is two-thirds of a turn, `4π/3` rad, and the quantity here is two-thirds of a **radian**. In turns `Δ = 1/(3π)`, transcendental (§4, first clause), and the smallest rational turn-fraction inside the data's `2σ` band is `33/311` — a tongue of depth in the hundreds. Computed exactly for the sine circle map (period-`q` tangency, [`lepton_blind_classifier.py`](lepton_blind_classifier.py) part N): tongue widths fall as `K^q` below criticality, so the `33/311` tongue is `~K³⁰⁸` — `10⁻³⁰` at `K = 0.8` — of the `2/3` tongue's width, and even at `K = 1`, where the tongues fill the line and widths go as `q^{−2.6}`, it is `~2 × 10⁵×` narrower. The wide-tongue argument, made in the right units, points the other way: a mode-locked `Δ` would sit in the *narrowest* tongue the data allows. The one escape — a map on some other circle locking at `2/3` turns, with the phase then set to `ρ × (1 radian)` — puts the whole content into the conversion factor, the unit choice §4 showed the 5-smoothness lives in.

What survives of the candidate is its side result, which is about rationals rather than leptons: **Farey depth and description length are the same ordering**, so the Occam curve of §4 is Farey structure's shadow. What it leaves behind is the third clause of the specification — **no dynamics on the phase circle** can do this; the object must carry the unit *arc over radius*, `n` steps at radius `R` — and §5c⁗'s own earlier finding that QLF exhibits no object of that shape on the ladder closures (rung-independent ratios are `{1/2, 1, 2}`).

> **Status.** **`Δ = 2/3` is open with zero live candidates.** Twelve routes closed, three structural results standing (no large number needed; `A² = 2` permits a hierarchy at all; the residual retired), and a three-clause specification any future candidate must meet *before* it is computed: an `O(1)` rational in radians, forced not selected, and of arc-over-radius shape. The scale `M` (§5c) and the `Δ` value remain the charged-lepton sector's only inputs.

---

### 5d. Quarks: it's the mass *difference* that's physical, not the mass

A natural next question is whether the *quark* masses satisfy a Koide-like relation — "quark masses from leptons." They do not (`(u,d,s) → Q=0.567`, mixed triplets `0.73–0.85`; only the heaviest `(c,b,t) ≈ 0.669` drifts near `2/3`, where QCD dressing is least, and even there within the large quark-mass uncertainties). **But that is consistent with QLF, not a failure of it — and the test was the wrong object.**

In QLF a quark is **fractional ZFA**: it does not exist independently (the same principle that makes the proton a deficit, §4a). A confined quark has **no physical mass of its own**; only the composite closure — the hadron — is an observable. Standard physics agrees: the quoted "quark masses" are scheme-dependent *running* Lagrangian parameters (MS-bar at a chosen scale), never measured. So "quark Koide" tests non-observables, and QLF *predicts* clean mass relations should live among the **observables** (leptons, hadrons) and be absent among the quark parameters — exactly what the data shows.

**Where the physics actually lives is the mass *difference*.** Individual quark masses are not observable, but quark-flavor *differences* manifest as **observable hadron isospin splittings**:

$$m_n - m_p = 1.2933\ \text{MeV} \;=\; \underbrace{(m_d - m_u)}_{\text{flavor step, }n\text{ heavier}} \;-\; \underbrace{\text{(EM self-energy)}}_{p\text{ heavier}}.$$

The `d ↔ u` flavor step **is** the weak vertex — the gauge-fold pair-flip of §4. So the `n–p` splitting is the *energy of the flavor-change closure step*, an observable tied directly to the machine-verified weak structure, even though the absolute quark masses are not. (Its **sign** — neutron heavier, so the proton is stable and hydrogen exists — is one of the most consequential facts in physics.) The analogous statement holds for `π± − π0` and the other isospin multiplets.

So the right QLF target is **not** a quark-mass Koide (which QLF's own confinement principle says should not exist) but the **hadron mass *splittings*** = flavor-step energy minus EM closure-depth difference — observable, gauge-sector, and connected to the weak vertex. This remains **open** (we do not yet derive `m_n − m_p` from closure structure; the loose ratios `(m_n−m_p)/m_e ≈ 2.53`, `(m_d−m_u)/m_e ≈ 5` are flagged as coincidences, not relations) — but it is the *tractable, well-posed* form of "connecting the quarks," replacing the category error of asking for their absolute masses.

---

### 5e. Attempt — the n–p splitting from closure structure

Taking §5d's target literally: can QLF derive `m_n − m_p = 1.2933 MeV`? It is two gauge-sector pieces (this decomposition is standard, recast in QLF terms; reproducible in [`np_splitting_demo.py`](np_splitting_demo.py)):

$$m_n - m_p \;=\; \underbrace{(m_d - m_u)}_{\text{strong flavor step, }n\text{ heavier}} \;-\; \underbrace{\Delta E_{\text{EM}}}_{\text{EM closure difference, }p\text{ heavier}}.$$

**The EM half — QLF fixes its sign and scale.** The two baryons are Borromean three-quark closures differing only in quark *charge* (the `+−` gauge-fold content): proton `uud`, neutron `udd`. The charge structure alone determines the EM sign:

| | `Σ qᵢ²` (self-energy) | `Σ_{i<j} qᵢqⱼ` (Coulomb) |
|---|---|---|
| proton `uud` | `1` | `0` |
| neutron `udd` | `2/3` | `−1/3` |
| **p − n** | **`+1/3`** | **`+1/3`** |

Both differences are positive: the proton has more quark self-energy *and* less Coulomb attraction, so **EM makes the proton heavier** (`ΔE_EM > 0`) — the correct sign for keeping the proton stable. The magnitude comes from QLF's own constants: `α·ℏc/R_p = (1/137)(197.3)/(0.84 fm) = 1.71 MeV` (α the substrate value `alpha_QLF_eq`, `R_p` the proton blanket depth), and with the `O(1/3)` charge factors the required `ΔE_EM ≈ 1.22 MeV` sits squarely inside it. **So QLF — α + proton depth + the quark-charge gauge structure — fixes the EM half's sign and order of magnitude.**

**The strong half — open, and *not* from charge.** `(m_d − m_u) ≈ 2.5 MeV` makes the neutron heavier and *is* the `d↔u` weak vertex (§4). A natural guess is that this comes from the down–up *charge* difference — but it cannot, for two structural reasons. (i) **Wrong direction:** the down quark is *less* charged (`|q_d| = 1/3 < |q_u| = 2/3`) yet *heavier*, so mass is anti-correlated with `|charge|` here — "more charge ⇒ more mass" runs backwards. (ii) **Sign symmetry:** charge *sign* alone cannot split masses — a quark and its charge-conjugate have equal mass (the `swap_topo`/CPT symmetry of the `+−` folds). In fact the two halves of the splitting push *opposite* ways: charge makes the proton heavier (the EM half), while the strong step makes the neutron heavier *despite* the down being less charged — and the strong half wins (proton stable ⇒ hydrogen exists). So the strong `d↔u` step is genuinely separate from charge; it is the bare flavor mass difference, **open** here and itself unexplained in the Standard Model (the down–up Yukawa asymmetry).

**The net — a hard cancellation, not shortcut.** `m_n − m_p ≈ (+2.5) − (1.2) ≈ +1.3 MeV` is a delicate sub-MeV cancellation of two ~MeV gauge-sector effects, the same one that required lattice QCD+QED (BMW 2015) to compute from first principles. QLF supplies the **structure** and the **EM scale**; it does **not** supply the cancellation.

So this is an honest **partial**: the decomposition is clean, the EM half's sign and ~MeV scale fall out of QLF's `α` + proton depth + gauge structure, and the strong half + precise value stay open. The sign result is not nothing — *neutron heavier ⇒ proton stable ⇒ hydrogen and chemistry exist*, and QLF gets that sign from charge structure alone.

**The cleaner observable: `m_n − m_H`.** Comparing the neutron to the *proton* compares a neutral closure to a charge *deficit* (§4a) — which is why the EM piece had to be separated. The QLF-natural comparison is between two **neutral observable closures**: the neutron and the hydrogen *atom*. Their gap,

$$m_n - m_H \;=\; 0.782\ \text{MeV},$$

is exactly the energy of the (Majorana) neutrino in **bound-state beta decay** `n → H + ν` — a real (rare, ~4×10⁻⁶) channel in which the neutron decays *directly into a hydrogen atom*. This is the literal realization of §4a: the neutron unspools into hydrogen's constituents and sheds `m_n − m_H` into the neutrino. So the clean QLF statement of the weak transition is **neutron-closure → hydrogen-closure + ν** — two neutral observables, the gap carried by the neutrino. Its being *small and positive* makes the free neutron unstable but long-lived (~880 s, rate ∝ `Q⁵`), and the margin is anthropic (free neutrons decay, bound neutrons in nuclei are stable, chemistry exists; `m_n < m_H` would give a stable neutron and *unstable hydrogen*). **Honest:** quantitatively `m_n − m_H = (m_n − m_p) − m_e`, so it carries the same strong−EM content above — it is the *right observable*, not new derivational power.

**Electron out vs electron in.** The two are the *same* neutral, `B=1` content arranged two ways — the difference is **where the electron's `−1` sits**. In **hydrogen** it is *outside* the baryon (the `uud` proton's `+1` deficit completed by a lepton electron → a stable atom); in the **neutron** it is folded *inside* (one `u→d` flip → `udd`, a single metastable closure). The decay `n → H + ν̄` simply hands the electron back outside. The three-colour-qubit `uud`/`udd` knot reading of this is [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §7.

### 5f. Deuterium stability — a positive structural result

Where the quark masses (§5d) and the strong `d↔u` step (§5e) are open, deuterium *stability* is a place QLF can speak **positively**, because it rests on machine-verified **Pauli exclusion** plus the §5e neutron margin.

**Existence + uniqueness (Pauli).** The deuteron binds only in the spin-triplet, `L=0` channel. By Fermi antisymmetry, two *identical* nucleons (`pp` or `nn`) are forbidden that channel — so **there is no diproton or dineutron**. Only `np` binds, because the neutron and proton are **distinguishable** closures (differing by one `d↔u` flavor step). Distinguishable ⇒ no Pauli block ⇒ the bound triplet is available. This is anchored in QLF's verified Pauli exclusion (`pauli_exclusion : [A,A]=0`, with `fermi_nonzero_example` showing it is a genuine non-vacuous constraint — [`lean/PauliExclusion.lean`](lean/PauliExclusion.lean)). So the deuteron is the *unique* simplest bound nucleus, for a reason QLF has.

**Stability (the bound neutron can't unspool).** `d → p+p+e⁻+ν̄` needs `m_d > 2m_p + m_e = 1877.06 MeV`, but `m_deuteron = 1875.61 MeV` — short by `1.44 MeV`, **forbidden**. Two QLF facts conspire: the diproton *isn't a closure* (Pauli again), and the joint-closure binding (`B_d = 2.224 MeV`) exceeds the free-neutron unspooling energy (`0.782 MeV`, §5e), so binding stabilizes the neutron — the §5e "bound neutrons are stable" point in its simplest case.

**Positive vs. open.** The deuteron's *existence, uniqueness, and stability* are structural QLF results (Pauli + `d↔u` distinguishability + the §5e margin). The binding-energy *magnitude* (`2.224 MeV`) is open (nuclear/QCD dynamics, same level as the strong step). **The payoff:** no-diproton (Pauli) is the *deuterium bottleneck* — why stars fuse slowly and controllably rather than burning all their hydrogen at once — and QLF gets that structural reason from verified Pauli exclusion. (Cf. [`Fusion.md`](Fusion.md).)

### 5g. Heavy leptons: an RH electron shell over a proton-mirroring core (conjecture)

A structural proposal for what makes a heavy lepton heavy, tying together §5b (Koide 3-phase), §5f, and the `m_p/m_e = 6π⁵` bridge. A heavy lepton (`μ`, `τ`) is:

- **External — a right-handed, weak-singlet electron identity.** Same charge, spin, EM coupling, and chiral loop as the electron (lepton *universality* — μ and τ are electrons from outside). Being the **RH (weak-singlet)** component, it is EM-only and does **not** couple to the leak vertex.
- **Core — a balanced, closed structure that *mirrors the proton's internals*** (a three-fold / Borromean, binding-dominated closure) at a *deeper* substrate scale (a different frequency). It carries the generation/flavor content and the bulk of the mass.
- **Leak — the LH-doublet channel.** The W bleeds the core into neutrinos (`μ⁻ → e⁻ + ν̄_e + ν_μ`), at the weak rate `Γ ∝ G_F² m⁵`. Deeper core ⇒ faster leak: `τ_μ/τ_τ = (m_τ/m_μ)⁵/BR(eνν) = 7.55×10⁶` vs measured `7.57×10⁶` (**0.3%**) — and *why* the τ can't bind (§4a).

**The payoff — it unifies the two "threes."** The Koide **3-phase** lepton generations (§5b) and the proton's **3-quark Borromean** closure become *the same three-fold*: the lepton generation core *is* a proton-mirror. This makes `m_p/m_e = 6π⁵` legible — the proton is the electron's heavy core (the `|S₃| = 6` three-quark permutation is the shared three-fold) — and is the structural form of the "leptons mirror proton processes at different frequencies" intuition.

**The tension (load-bearing).** Charged leptons are **pointlike to ~10⁻¹⁹ m** — no substructure seen — while the proton has structure at ~1 fm. So a proton-mirroring core cannot be a literal proton inside the muon; it must sit ~10⁴× *deeper*, **fully closed/balanced so only the electron identity shows externally** (the closure hides it as confinement hides the proton's quarks). Self-consistent, but substrate-level and not directly resolvable at current scales.

**Status: a research-direction conjecture.** The one solid quantitative anchor is the `m⁵` leak (`τ_μ/τ_τ` to 0.3%). Not derived: the precise proton-mirror core, the lepton masses (open, Koide-constrained, §5b–5c), and a resolvable test. Recorded as the structural form of intuition #2 — coherent and unifying, but conjecture.

---

## 6. Honest open list (quantitative weak sector)

- **The Koide angle `δ`** — the genuine remaining lepton-sector input (§5c). The two-input solve gives `δ = 0.222222047`; `2/9` is a flagged **candidate hypothesis** matching it to `7.9 × 10⁻⁷`, with a `9.8 ppm` residual on `m_μ/m_e` — the same `10⁻⁵` order as `Q`'s own deviation from `2/3`. Not a derivation.
- **`R_W`, `R_Z` from first principles** — the structure `M = αR` is there; the depths are not computed, so the absolute W/Z masses are open. The **Weinberg angle** has a structural value at the *unification* scale, `sin²θ_W = 3/8` (the spatial/alphabet fraction = the SU(5) GUT normalization, `QLF_WeinbergAngle`); open is the **RG running** down to the measured `0.231`. That renormalization sector is substrate-fixed at the coefficient level: logarithmic running with the `2π` loop phase and UV-finiteness from the substrate floor ([`QLF_RunningCouplings`](lean/QLF_RunningCouplings.lean)); the β-triple `(b₁,b₂,b₃) = (41/10, −19/6, −7)` from QLF counts + the universal one-loop weights ([`QLF_ElectroweakBeta`](lean/QLF_ElectroweakBeta.lean), reproducing the QCD `b₀ = 7`); the flow *direction* (down from `3/8`, since `b₁ − b₂ > 0`); and the **GUT-scale structure** — the unification formula with QLF's derived slope `109/15` and target `3/8` ([`QLF_GUTScale`](lean/QLF_GUTScale.lean)), reducing the GUT scale to the `M_Z` coupling gap. What remains for the `0.231` and the absolute `M_GUT` *values* is the `M_Z` couplings — the absolute-scale sector (frontier #1), the *same* boundary the SM/MSSM hit, since they fit the couplings and run up, deriving no `M_GUT` either — plus the depth ratio `R_W/R_Z`. *(The `ln(M_Pl/M_GUT) ≈ 2π` proximity is pre-buried as non-robust: Planck-convention and model dependent, not a result.)*
- **The SU(2) coupling `g` and the breaking scale** (the Higgs VEV `v ≈ 246 GeV`) — not derived; [`Higgs.md`](Higgs.md) reframes the *mechanism* (gauge-fold delay) but not the numbers.
- **Fermi constant `G_F`** — no derivation anywhere in the corpus.
- **The τ-decay-vertex topology** — §5a gives a mass handle (Koide `Q=2/3` ⇒ `m_τ` to 0.006%) and a vertex reading (deepest-phase un-binding), but: **deriving `Q=2/3` from the τ-closure**, the **Koide angle `δ = 0.222222047`** (`2/9` a flagged candidate, §5c), and the **scale `M`** are open (`m_e, m_μ` are still inputs).
- **Why exactly three generations** — structurally Lean-anchored: the generation count = `substrate_spatial_dimension = 3`, the same `3` as Koide's phases, colour SU(3), and `α`'s `N=3²` ([`QLF_Generations`](lean/QLF_Generations.lean), `three_axis_signature`); this *reduces* "why 3 generations" to "why 3 spatial dimensions" — which is **derived** as the minimal dimension in which any relational/causal graph renders faithfully (every finite graph embeds crossing-free in ℝ³; 2D fails for non-planar graphs), so the closure graph's rendering is minimally 3D ([`SpaceTime.md`](SpaceTime.md) §3a, [`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean)). The quark generations and the lepton↔quark mass correlation remain separate and open.
- **Flavor change** (`d → u + e⁻ + ν̄`) — the explicit topological flavor-change process is not detailed.
- **Hadron mass splittings** (`m_n − m_p`, `π±−π0`, …) — §5e: the EM half's sign and ~MeV scale fall out of QLF (α + proton depth + quark-charge gauge structure), but the strong `d↔u` flavor-step energy and the precise sub-MeV cancellation are open. This is the well-posed "connect the quarks" target (the *difference*, not absolute masses).
- **CKM / PMNS mixing angles** — open ([`Standard_Model.md`](Standard_Model.md) §4.2).

---

## 7. What this is NOT

- **Not a quantitative weak sector.** No W/Z mass, no Weinberg-angle number, no `G_F`, no coupling `g` is claimed to be derived. Only the **group-theoretic** SU(2) identification is asserted as closed.
- **Not a doublet-representation theory.** `weak_isospin_su2` identifies the SU(2) *Lie algebra*; it does not construct the left-handed doublets / right-handed singlets as representations, nor explain why only left-handed fields couple.
- **Not an explicit W propagator in beta decay.** QLF's β-decay is boundary restructuring; the W-as-particle is, so far, only the τ-vertex object (§4–5).
- **Not a replacement for the Higgs mechanism's numbers.** [`Higgs.md`](Higgs.md) reframes mass generation as gauge-fold delay; the 125 GeV Higgs mass and the Yukawa structure stay open.
- **Not a from-nothing derivation of the lepton masses (§5a–5b).** `Q = 2/3` *is* derived (machine-verified) — but **from** the structural inputs `N = 3` (three axes), `A² = 2` (two transverse axes), and balanced phases. What is *not* proved is the **identification** that the lepton `√`-mass vector actually has that `1 longitudinal + 2 transverse / 3-axis-phase` structure; the Koide angle `δ` and scale `M` remain inputs, so `m_e, m_μ` are still needed to predict `m_τ`. It is a parameter-light prediction with a derived invariant — **not** a closed derivation of the full generation spectrum, and **not** a claim that the lepton-mass↔axis-phase identification is itself proved.

---

## 8. References

### Internal (QLF)
- [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean) — `weak_isospin_su2`, `tau_comm_xy/yz/zx`, `tau_anticomm_*`, the Σ₈ τ-algebra (machine-verified).
- [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean) — `interleaved_xlvr_folds_to_negI` (the chiral electron loop `^<v>`); `count_balanced_pauli_closed`.
- [`koide_tau_demo.py`](koide_tau_demo.py) — §5a reproducible: Koide `Q` from measured masses, the `m_τ` prediction from `m_e, m_μ, Q=2/3`, and the three-phase equivalence.
- [`np_splitting_demo.py`](np_splitting_demo.py) — §5e reproducible: the `m_n − m_p` decomposition, the EM half's sign + scale from the quark-charge gauge structure and `α·ℏc/R_p`.
- [`Primordial_Entanglement.md`](Primordial_Entanglement.md) §2 — the `N=4/8/12` generation loop-length picture refined by §5a's phase reading.
- [`Higgs.md`](Higgs.md) §4 — W/Z as gauge-fold closures, `m = αR`, `cos θ_W = R_W/R_Z`.
- [`Standard_Model.md`](Standard_Model.md) §§2–4 — the honest scoreboard; weak SU(2) row.
- [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) — beta decay as boundary restructuring; the Majorana neutrino (`neutrino_majorana`) and the `0νββ` prediction.
- [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §6, [`Bound_States_QLF.md`](Bound_States_QLF.md) §4 — the τ-decay vertex (the W blocker).
- [`Lagrangian_Formulation.md`](Lagrangian_Formulation.md) — the Σ₈ algebra and `τᵢ = iσᵢ`.
- [`Open_Problems.md`](Open_Problems.md) — registry status of the weak-sector items.

### External
- Glashow–Weinberg–Salam electroweak unification (SU(2)_L × U(1)_Y); the Higgs mechanism.
- PDG — `M_W = 80.377 GeV`, `M_Z = 91.1876 GeV`, `cos θ_W = M_W/M_Z ≈ 0.881`, `G_F = 1.1664×10⁻⁵ GeV⁻²`.
- The quaternion group `Q₈` and `SU(2)` as unit quaternions (the algebraic identity behind §3).
