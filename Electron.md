# Electron in the Quantum Logical Framework (QLF)

**Repository:** [`quantum-logical-framework`](https://github.com/rhovision-org/quantum-logical-framework)
**Document:** `Electron.md`
**Document version:** 3.0 — the core claim sharpened and machine-verified ([`lean/QLF_ElectronClosure.lean`](lean/QLF_ElectronClosure.lean), zero axioms): the electron is a **closed periodic mode**, not an unfinished fragment; **charge is the residue of non-closure**, and it is blind to spin and energy. Resolves the standing inconsistency between "open Hermitian deficit" and the engine's own `ZFA closed: True`. Earlier: 2.1 — run-commands regenerated against the current `particles.py`; ½-spin-information and two-axis-content findings. Aligned with [`Bound_States_QLF.md`](Bound_States_QLF.md)
**Author:** Jim/Grok (synthesized from QLF core axioms, QuCalc engine, `particles.py` v2.2, gauge-folding rule, and the bound-state framing)

## Abstract

> **Handedness is fundamental; charge is not.** A twist *is* a handedness on an axis and nothing else, ZFA *is* zero net handedness on every axis, and charge is the **gauge component** of it — one of four (`zfa_iff_handedness_balanced`, `chiralCharge_eq_handednessOn_gauge`).
>
> **An electron is a closed half-spin periodic mode, not a point carrying a localized charge.** Its internal cycle `^<v>` *is* Zero-Free-Action closed and folds to `−I`. What is **not** closed is its **gauge** twist — and that unmatched gauge count *is* the charge. So the electron is closed on the spatial axes and open on the gauge axis, and the two are different axes of the same alphabet. A **manifest physical event** — preparation, binding, detection — is the larger joint closure in which the gauge deficit is matched. The electron's intrinsic scale is therefore the **period of its closed mode**, never a radius.

In QLF **the electron is not an independent stable observable**, but not because it is an unfinished fragment. It is a completed half-spin cycle carrying one unmatched gauge distinction, which is why it must join a Hermitian-conjugate partner (positron → positronium), a heavier lepton (antimuon → muonium), or a baryon (proton → hydrogen) before the *whole* event closes. The "electron's mass" reported by experiment, `m_e ≈ 0.511 MeV`, is the electron's **gauge-fold-depth contribution** to the bound-state mass — half of `m(positronium)`, the analogous contribution to `m(hydrogen)`, and so on.

*(This supersedes the "free electron is an open Hermitian deficit" reading of version 2.1, which contradicted the engine's own `ZFA closed: True` for `^<v>`. Both statements were right about different levels; §1 separates them.)*

This is the same structural move that [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) makes for photons (joint emitter-absorber closure, not free projectile) and that [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) makes for quarks (no asymptotic free quarks, only bound hadrons). Applied to electrons: an electron is one half of a joint closure, not an isolated particle whose mass can be extracted in isolation. The QLF observables are atomic systems; the "electron" is the gauge-fold contribution of one constituent.

The remainder of this document is a hands-on tutorial. We give the electron's QuCalc topology (the half it contributes to a joint closure), the photon and antiphoton (which jointly satisfy ZFA), and the electron–proton hydrogen formation (a joint-ZFA bound state). Everything runs live in `particles.py` — and every bound state runs *visually* in the [**Spectral Spacetime Constructor**](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html) (the `▶ live` links in the table below open positronium, hydrogen, and muonium; [`Spacetime_Constructor.md`](Spacetime_Constructor.md)).

## Why the Electron Matters

Most everything we experience is due to electrons participating in joint closures — chemistry, light emission, electric currents, biological membranes. The "electron" of standard physics is shorthand for "the leptonic half of a joint-ZFA closure event." Understanding the electron in QLF means understanding which joint closures it can participate in and how its gauge-fold depth contributes to the bound-state mass and binding.

In QLF the electron is not an abstract point particle with mysterious properties. It is a **gauge-folded topological half-loop** — a partial twist sequence containing at least one `+` or `-` fold along the LOCAL gauge axis. By itself the half-loop has not closed; it carries an open Hermitian deficit. When it intersects a Hermitian-conjugate partner's causal frontier, the joint ZFA closure completes, and the gauge-fold depth of the electron's half contributes its share of the bound system's constructing delay and rest energy.

Its **spin is not mysterious either** — it is literally the twists. The electron loop `^<v>` folds to `−I` (a half-spin fermion needing 720° to return, the SU(2)→SO(3) double cover), and the electron is **Dirac** (not its own antiparticle), all machine-verified in [`Spin_QLF.md`](Spin_QLF.md) / [`lean/QLF_Spin.lean`](lean/QLF_Spin.lean) (`fold_electron`, `rotation_360_eq_negI`, `electron_not_majorana`). Charge conjugation = view-from-behind: the positron is the electron's loop read in reverse. Two further facts sharpen this. First, **the electron loop is one bit of information**: the two-valued ½-spin closure carries exactly `log 2` (`spin_half_is_information_atom`, [`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)) — Wheeler's *it from bit* at the electron ([`Information_Physics.md`](Information_Physics.md)). Second, **the loop engages two of the three spatial axes** — `^<v>` folds as `σ_y·(−σ_x)·(−σ_y)·σ_x = −I`, i.e. the x (`<>`) and y (`^v`) axes, not z (`interleaved_xlvr_folds_to_negI`, [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean)); this `{x,y}` content is the verified anchor for what distinguishes the muon and tau (colour *content* vs colour *charge*, [`Particle_Ladder.md`](Particle_Ladder.md) § *Colour content vs colour charge*).

**Lepton flavors.** The electron is the first of the **three lepton flavors** — *e, μ, τ* — the same chiral closure at successive generations, which QLF ties to the three spatial axes (`num_generations_eq_three`, [`QLF_Generations`](lean/QLF_Generations.lean)). A bound state carries whichever flavor its leptonic half is: an electron in positronium/hydrogen, a **muon** in muonium (a deeper-blanket gauge half), a **tau** in the heaviest systems. So "the electron" of this document is *flavor-1*; the μ and τ are its deeper / other-axis versions, and the flavor→mass map (`m_e : m_μ : m_τ`) is the open target ([`Standard_Model.md`](Standard_Model.md) §3.3, [`Weak_Force.md`](Weak_Force.md) §5, [`Bound_States_QLF.md`](Bound_States_QLF.md)).

## 1. The Electron's Two Closures

**The single most important structural fact about the electron is that it closes on one set of axes and not on the other.** Version 2.1 of this document said the free electron was "an open Hermitian deficit" while printing `ZFA closed: True` beside it. Both were right, about different things, and separating them is what the rest of this document rests on.

| Level | Object | Status |
|---|---|---|
| **Internal cycle** (spatial axes) | `^<v>` — the half-spin mode | **Closed.** `#^ = #v`, `#< = #>`, free action `F = 0`, fold `−I` |
| **Charge** (gauge axis) | one unmatched `+` | **Open.** This deficit *is* the electric charge |
| **Manifest event** | the joint closure with a partner | **Closed.** Gauge matched, total neutral |

Machine-verified, zero axioms, in [`lean/QLF_ElectronClosure.lean`](lean/QLF_ElectronClosure.lean):

- `electronCycle_countBalanced` — `^<v>` achieves ZFA;
- `electronCycle_folds_negI` — and folds to `−I`, the half-spin fermion sign (reusing `interleaved_xlvr_folds_to_negI`);
- `electronCharged_charge` — `^<v>+` carries `chiralCharge = 1`;
- `electronCharged_not_countBalanced` — …and is therefore *not* closed. **The charge is exactly the part that did not close.**
- `positronium_countBalanced` / `positronium_neutral` — the joint event closes, and is neutral.

So the electron is not an unfinished particle fragment. It is a **completed periodic mode carrying one open gauge distinction** — and that distinction does not *do* anything. It is not a pending effect, and the electron does not seek a partner. A history carrying non-zero charge simply does not close, and what does not close is not an event (§1b″). What we call the electron's charge shows up only *inside* joint histories that do close.

$$
\boxed{\text{electron} = \text{closed periodic mode} + \text{one unmatched gauge twist}}
$$

Minimal electron topology (spatial cycle + gauge):

`^<v>` + `+` → written `^<v>^+` in the engine's fuller form

- `^` = forward-time seed
- `<` `>` = spatial folds (transverse area) — the **closed** part
- `+` = gauge fold → the **open** part: the charge, and the gauge-fold-depth contribution to bound-state mass

The gauge deficit accumulates a **constructing delay** $\Delta t = R/f$ (topological depth $R$ at vacuum frequency $f$) only when it is matched by a partner. In a positronium binding it joins the positron's mirror gauge twist and the joint closure creates a finite local time at depth $2R$, with rest energy `m(Ps) ≈ 1.022 MeV`. Half of this — `0.511 MeV` — is what conventional physics attributes to the "free electron mass."

### 1a. Hermitian is not the same as ZFA-closed

This deserves its own statement because the two are routinely conflated, and conflating them is what produced the version-2.1 contradiction.

The prefix `^<v` folds to `σ_y·(−σ_x)·(−σ_y) = −σ_x`, which is **Hermitian**. Its history nevertheless has free action `F = 1` — the `<` is unmatched. Adding `>` gives `^<v>`, with `F = 0` and fold `−I`.

$$
\boxed{\text{Hermitian} \;\not\Rightarrow\; \text{ZFA closed}}
$$

Verified as `hermitian_not_implies_zfa` (`electronPrefix_fold`, `neg_sigmax_hermitian`, `electronPrefix_not_countBalanced`). Self-adjointness is a property of the **operator**; closure is a property of the **history**. An intermediate prefix can be a perfectly good mathematical state and still not be a manifest electron event — which is the precise content of *"the electron is manifest only at full cycles."*

### 1b. Charge is emergent — it is the residue of non-closure

`twistCharge` assigns `+1` to `+`, `−1` to `−`, and **zero to all six spatial twists**. Charge is therefore the signed gauge count and nothing else (`chiralCharge_eq_gauge_counts`). The consequence is immediate and sharp:

$$
\boxed{\text{ZFA-closed} \;\Longrightarrow\; \text{electrically neutral}} \qquad \texttt{zfa\_closure\_is\_neutral}
$$

**Charge is not a fundamental property carried by an object.** It is a *count of what has not yet closed*. There is no charge field, no charged point, no charge substance: a history that closes has charge zero, necessarily, and a history that carries charge is by that fact incomplete. This is why charge is conserved (counts of conjugate twists cannot be created singly), why it is quantized (it is an integer count), and why an electron cannot be isolated as a completed event.

### 1b′. What *is* fundamental: handedness

Charge being emergent leaves a question, and it has an answer
([`lean/QLF_Handedness.lean`](lean/QLF_Handedness.lean), zero axioms).

A twist **is** a handedness together with an axis, and nothing else — the alphabet is the signed axis
frame, `Twist ≃ Bool × Axis` ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)). The only
two data an elementary distinction carries are *which axis it distinguishes along* and *which of the
two ways it went*. **Charge is nowhere in the primitives.**

$$
\boxed{\text{ZFA} \;\Longleftrightarrow\; \text{zero net handedness on every axis}}
\qquad \texttt{zfa\_iff\_handedness\_balanced}
$$

$$
\boxed{\text{charge} \;=\; \text{the \emph{gauge} component of handedness — one of four}}
\qquad \texttt{chiralCharge\_eq\_handednessOn\_gauge}
$$

Count balance was always a statement about handedness: one component per conjugate pair, which is
**why `F(h)` has four terms**. And this is *why* charge cannot see a spin or an energy (§1c) — those
are the other three components, and components of a vector do not mix. Charge is not a different kind
of thing from spin; it is the same primitive read on a different axis.

Three more, each machine-verified:

- **`handedness_ne_zero`** — there is no unhanded distinction. To distinguish at all is to go one way
  rather than the other.
- **`handednessOn_map_conj`** — conjugation negates *every* component. So charge flips **because**
  handedness does, not the other way round; `chiralCharge_conj` is its `Axis.I` case.
- **`electron_neutral_but_handed`** — the electron's cycle has zero net handedness on every axis, and
  every twist in it is handed. **The primitive never vanishes; the derived quantity does.** *Neutral
  does not mean handedness-free — it means handedness balanced.*

**C and P in one line.** `C` flips every component of handedness; `P` (`reflect`) flips one. Charge
is the gauge component, so spatial reflection leaves charge alone by construction
(`reflect_preserves_charge`) while conjugation negates it. The asymmetry between the two is a fact
about how many handedness components each touches — see
[`CP-Violation-and-Chirality.md`](CP-Violation-and-Chirality.md) §1a.

### 1b″. No event is ever charged — and Coulomb is a count, not a force

The contrapositive of `zfa_closure_is_neutral` is the load-bearing direction, and it is where the ontology bites:

$$
\boxed{\text{charge} \neq 0 \;\Longrightarrow\; \text{does not close} \;\Longrightarrow\; \text{not an event}}
\qquad \texttt{charge\_nonzero\_not\_countBalanced}
$$

**No event ever carries net charge.** What carries charge is a *non-event*. So an unmatched gauge twist is not a property an object has and acts with, not a field it sources, and not a pending effect waiting for a partner — **it will close or it will not, and if it does not there is no effect and no charge.** Nothing is stored, nothing is owed, nothing waits.

Everything usually attributed to the Coulomb force is then a **count of joint histories that do close**:

| | joint closure | ways |
|---|---|---|
| **any pair** | requires `Q₁ + Q₂ = 0` (`joint_closure_total_charge_zero`) | — |
| **like charges** | **none exists** (`like_charges_do_not_close`) | **0** |
| **opposite charges** | exists (`opposite_charges_close`) | > 0 |

Assembled as **`coulomb_is_a_counting_rule`**. Read it carefully: like charges are not *pushed apart*. There is simply **no closed history in which both occur** — zero ways, and a closure's frequency *is* its multiplicity ([`Philosophy.md`](Philosophy.md) §3a). Opposite charges are not *pulled together*; there are ways, so it happens. **No force, no field, no action at a distance** — the same framing as [`Spacetime_Constructor.md`](Spacetime_Constructor.md): only closures that DO close.

Charge conservation is not a law imposed on a dynamics either. It is the condition under which a joint history closes at all — there is nothing for it to be violated by.

### 1c. There is no charge *between* electrons of different energy or spin

This is the sharpest consequence, and it is a theorem rather than a stance.

Spin and energy are **spatial** content — the axis word and its depth. Charge lives on the **gauge** axis. Since `twistCharge` vanishes on every spatial twist, no amount of spatial content changes the charge:

$$
\boxed{\Gamma_{\text{charge}}\big[(m,s),(n,s')\big] \;\text{is independent of } m, n, s, s'}
$$

- `twistCharge_eq_zero_of_spatial` — every spatial twist is charge-neutral;
- `chiralCharge_determined_by_gauge` — charge is a function of the gauge counts alone;
- **`no_charge_between_spatial_modes`** — two electron modes carrying the same gauge deficit and *any* spatial content whatever (different harmonics, opposite spins) have **exactly zero** charge difference.

**The electromagnetic weight cannot see a spin or an energy.** There is no charge between two electrons of different energy, and none between opposite spins — the differential is identically zero, by construction of the alphabet, not by cancellation.

Two independent confirmations of the same structure, in the coherent channel rather than the charge count:

- **Distinct full-cycle harmonics have zero coherent overlap** — `cycleOverlap_distinct` / `harmonics_orthogonal`: a root of unity other than `1` sums to zero over a full period, because the cycle closes. This is *why* a quantity is invariant only at a completed cycle: over anything less, the cross terms survive.
- **The two spin channels are orthogonal projectors** — `spin_projectors_orthogonal` (`P↑P↓ = 0`, with `projUp_eq_half`/`projDown_eq_half` identifying them as the spectral projectors of `σ_z`).

Together: `channelKernel_diagonal` gives `Γ[(m,s),(n,s')] = δ_mn δ_ss'`. **Different harmonics or orthogonal spin channels carry no persistent coherent cross term.**

> **Scope, stated once and precisely.** What is proven is that the charge *difference* between modes is exactly zero and the coherent cross term vanishes — so no closure channel is opened or closed by a difference of spin or energy, and the electromagnetic weight is **spin-blind and energy-blind**. What is *not* claimed is that the shared gauge imbalance disappears: both electrons carry the same unmatched `+`. But by §1b″ that imbalance is **not an effect** — it is what makes certain joint histories close and others not exist at all. Two electrons of different energies do enter joint events (§1e), in however many ways there are; QLF's content is that the count of those ways does not depend on their spins or energies *through the charge*.
>
> **This is a prediction, not a retreat.** Standard QED agrees and QLF *derives* it: the direct Coulomb term is exactly spin-independent, and all spin dependence of two-electron energies (the singlet–triplet splitting) comes from exchange — which is closure blocking, not charge. QLF says that had to be so, because charge and spin do not live on the same axes.

### 1d. Manifest only at full cycles

Putting §1a and §1c together gives the manifestation rule:

> **A quantity becomes physically invariant only at a completed closure.**

Below a full cycle the cross terms between harmonics do not vanish, the free action is non-zero, and there is no invariant to read. At the completed cycle `F = 0`, the fold is a Pauli scalar (`count_balanced_pauli_closed`), the harmonic cross terms vanish exactly, and the mode has a definite phase. Manifestation is not an observer acting; it is a cycle closing.

### 1e. Different energies and spins *do* enter one event

The reading to avoid is that non-matching modes cannot interact. They can — what cannot happen is a completed event with unmatched conserved distinctions. Verified directly as **`joint_closure_allows_unequal_components`**: two open halves, neither balanced, **of different lengths**, whose joint history closes.

$$
\boxed{\text{individual modes need not match; the complete event must close}}
$$

For two electrons, the joint closure condition is the ordinary one —

$$
E_1 + E_2 = E_3 + E_4, \qquad \mathbf{p}_1 + \mathbf{p}_2 = \mathbf{p}_3 + \mathbf{p}_4, \qquad Q_{\rm in} = Q_{\rm out}
$$

— with `E₁ ≠ E₂` allowed, opposite spins allowed, and the interaction operator Hermitian throughout. Ordinary electron–electron scattering is therefore **not** a counterexample to ZFA; it is an instance of it. The QLF statement with teeth is the negative one:

> Every physically completed electron–electron process admits a globally closed representation. Candidate histories with unmatched residual action do not occur as completed events.

### 1f. The electron has no radius — its scale is its wavelength

QLF assigns the electron **no hard intrinsic radius**, and the honest form of that claim is an *absence*: no length parameter occurs anywhere in the closure predicate. `countBalanced` and the fold are functions of the word alone. There is nothing in the theory for a radius to be.

What the closure *does* fix is a **period**. From `E = hν`:

$$
T = \frac{h}{E}, \qquad\text{at rest}\quad E = m_ec^2 \;\Rightarrow\; T_C = \frac{h}{m_ec^2}, \qquad
\boxed{\lambda_C = c\,T_C = \frac{h}{m_ec}}
$$

verified as `rest_period_times_c`. And the **full cycle is `2π` radians**, which is why the Compton wavelength rather than the reduced one is the manifest scale:

$$
\lambda_C = 2\pi\,\bar\lambda_C, \qquad \bar\lambda_C = \frac{\hbar}{m_ec} \;\;(\text{one radian})
$$

verified as `compton_full_cycle`. Four distinct scales, kept distinct:

| Scale | What it is |
|---|---|
| **Compton** `λ_C = h/m_ec` | the rest/internal closure scale — one full cycle |
| **reduced Compton** `ƛ_C = ħ/m_ec` | one radian of that cycle, not a manifest length |
| **de Broglie** `λ_dB = h/p` | the translational spatial phase scale (`closureWavelength`) |
| **localization width** | a context-dependent wavepacket property, not intrinsic |
| ~~radius~~ | **no such quantity** — nothing in the closure predicate carries a length |

### 1h. Where this could be falsified — and where it contradicts the Standard Model

Sorted by the classes of [`Experimental_Consistency.md`](Experimental_Consistency.md) §10, because the distinction is what the claim is worth. **Class B contradicts the SM; Class A does not**, and calling a Class A result a discriminator is exactly the error [`ScientificApproach.md`](ScientificApproach.md) R0a exists to prevent.

**Class B — QLF says what the SM does not.**

| Prediction | Why it differs from the SM | Kill condition |
|---|---|---|
| **Exact global charge neutrality** | Every event is a closure and every closure is neutral (`zfa_closure_is_neutral`); a charged history is not an event at all (`charge_nonzero_not_countBalanced`). A net-charged universe is not suppressed — **there is no history that realizes it.** The SM conserves charge by gauge invariance but leaves the *total* a free initial condition | A confirmed non-zero net cosmic charge density, at any magnitude. Present bounds: `\|q_p+q_e\|/e < 10⁻²¹`, neutron charge `< 10⁻²¹ e`, CMB-isotropy limits |
| **α(0) cannot drift** | Charge is an **integer count** of unmatched gauge twists (`chiralCharge_eq_gauge_counts`) and an integer has no dynamical variable to drift along — `no_cosmological_drift_of_alpha` ([`Alpha.md`](Alpha.md), scoped to the leading value). The SM permits promoting α to a slowly varying field, and varying-constant models do exactly that | A **confirmed** cosmological α drift — quasar absorption lines (Webb et al., `Δα/α ~ 10⁻⁵`), Oklo, optical clocks at `10⁻¹⁷/yr`. **The most accessible QLF-vs-SM discriminator in this sector** |
| **Like charges admit zero joint closures** | `like_charges_do_not_close` — not a strong repulsion, *no closed history*, at any coupling and in any dimension. The SM computes a repulsive potential, which is a different kind of statement and does not forbid exotic like-charge binding a priori | A genuine **two-body** bound state of like charges with **no mediating third closure**. Cooper pairs and bipolarons do **not** count — they bind through the lattice, a third closure, so their joint history is neutral overall (`SharedClosure`) |

**Class A — QLF derives what the SM computes.** These are *consistency*, not discriminators, and are listed so they are not mistaken for evidence:

- exact spin-independence of the **electrostatic** coupling (§1c) — QED gets the same zero by computation;
- exact `|q_e| = |q_p|` — the SM arranges it by anomaly cancellation, QLF gets it from the count;
- no charge creation, no electron decay — gauge invariance forbids it in the SM too.

> **One scope correction owed to §1c.** "All spin dependence is exchange" is right for the **charge–charge** term only. Spin also enters electromagnetism through the **current** sector — Breit, spin–orbit, spin–spin — which in QLF is the winding/circulation ([`QLF_AngularMomentum`](lean/QLF_AngularMomentum.lean), the discrete curl), a *different substrate object* from `chiralCharge`. The theorem says charge cannot see spin; it does not say electromagnetism cannot.

### 1g. Claim and evidence

Statuses on the two axes of [`ScientificApproach.md`](ScientificApproach.md) §3 — mathematical (what is established about the formal object) and physical (what is established about the world).

| Claim | Mathematical | Physical | Anchor |
|---|---|---|---|
| The electron's internal cycle is ZFA-closed and folds to `−I` | **Proved** | **Internal** | `electronCycle_countBalanced`, `electronCycle_folds_negI` |
| Hermitian ⇏ ZFA-closed | **Proved** | **Internal** | `hermitian_not_implies_zfa` |
| Charge = unmatched gauge count; closed ⟹ neutral | **Proved** | **Consistency** — reproduces conservation and quantization of charge | `chiralCharge_eq_gauge_counts`, `zfa_closure_is_neutral` |
| **ZFA is zero net handedness on every axis** | **Proved** | **Internal** — the selection principle restated in the primitive | `zfa_iff_handedness_balanced` |
| **Charge is the gauge component of handedness, one of four** | **Proved** | **Internal** — explains §1c rather than restating it | `chiralCharge_eq_handednessOn_gauge` |
| **Handedness never vanishes; a closure is balanced, not handedness-free** | **Proved** | **Internal** | `handedness_ne_zero`, `electron_neutral_but_handed` |
| **C flips four components, P flips one; parity cannot touch charge** | **Proved** | **Consistency** — reproduces the C/P asymmetry structurally | `handednessOn_map_conj`, `reflect_preserves_charge` |
| **No event is ever charged** | **Proved** | **Internal** — the ontological consequence: an unclosed history has no effect | `charge_nonzero_not_countBalanced` |
| **Coulomb is a count of joint closures, not a force** | **Proved** | **Consistency** — like/unlike behaviour reproduced with no force, field, or action at a distance | `coulomb_is_a_counting_rule`, `like_charges_do_not_close`, `opposite_charges_close` |
| **No charge difference between modes of different energy or spin** | **Proved** | **Consistency** — the direct Coulomb term *is* spin-independent in QED; here it is derived rather than computed | `no_charge_between_spatial_modes`, `chiralCharge_determined_by_gauge` |
| Distinct harmonics / opposite spins carry no coherent cross term | **Proved** | **Internal** | `channelKernel_diagonal`, `harmonics_orthogonal`, `spin_projectors_orthogonal` |
| Unequal components can enter one closed event | **Proved** | **Consistency** — Møller scattering at unequal energies | `joint_closure_allows_unequal_components` |
| `λ_C = c·T_C = h/m_ec`; full cycle is `2π` | **Proved** | **Consistency** — standard kinematics, no new content claimed | `rest_period_times_c`, `compton_full_cycle` |
| The electron has no hard radius | **Absence, not a theorem** | **Open** — a null that experiment can only bound | no length parameter in the closure predicate |
| `m_e = 0.511 MeV` as gauge-fold-depth share | **Not derived** | **Open bridge** — the flavor→mass map | [`Bound_States_QLF.md`](Bound_States_QLF.md) |

### Bound systems the electron half-loop completes

| Joint closure | Partner | Bound-state mass | Joint topology (schematic) |
|---|---|---|---|
| **Positronium** ([▶ live](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html#qc=positronium%20%40%200%2C0%2C0)) | Positron `v>v-` | 1.022 MeV | `^<v>^+ · v<v>v-` (electron half + positron half) |
| **Hydrogen** ([▶ live](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html#qc=H%20%40%200%2C0%2C0)) | Proton (three-quark composite) | 938.78 MeV | electron half + proton internal closure |
| **Muonium** ([▶ live](https://rhovision-org.github.io/quantum-logical-framework/spacetime_constructor.html#qc=muonium%20%40%200%2C0%2C0)) | Antimuon (deeper-blanket gauge half) | 106.17 MeV | electron half + antimuon half (asymmetric blanket depths) |

In each case the "electron" of this document contributes the same gauge-fold-depth `R_e` to the joint closure. The bound-state mass is `R_e + R_partner` (modulo joint-closure binding corrections), not `R_e` alone. See [`Bound_States_QLF.md`](Bound_States_QLF.md) for the spectrum.

### Run the electron half-loop yourself

```bash
python particles.py --particle electron
```

**Sample output (the electron's internal cycle):**
```text
=== ELECTRON ===
open prefix         : ^<v>
constituents        : one fluxoid (^<v>)
engine closure      : ^<v>
final history       : ^<v>
fold depth (pairs)  : 2
ZFA closed          : True
hermitian conjugate : <^>v
```

Note `ZFA closed: True` — and it is not a bug. The engine is reporting the **internal cycle** `^<v>`, which genuinely closes (§1). The open part is the *gauge* twist, which this history does not contain; add it (`^<v>+`) and the same engine reports the deficit. The electron becomes a manifest physical event when a partner matches that gauge twist.

## 2. Photon Folds Forward in Time — Antiphoton Satisfies ZFA

A photon is a **massless joint closure** that requires no gauge fold. It is a pure forward-time spatial closure between an emitter and an absorber — see [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) and [`Collective_Electrodynamics.md`](Collective_Electrodynamics.md).

The two halves of the joint photon closure:

- Photon half (forward-time): `^>`
- Antiphoton half (conjugate, backward-time): `v<`

When they meet they form the joint closure with exactly Zero Free Action:

`^>` ∘ `v<`  ⟹  net action = 0  (the joint photon closure)

This is the **same structural move** as for the electron — both photons and electrons are halves of joint closures. The difference: the photon's halves have no gauge fold, so the joint closure has zero constructing delay and the photon is massless; the electron's halves have a gauge fold, so the joint closure has finite delay and finite rest energy.

### Run the photon–antiphoton pair

```bash
# The photon's gauge loop (the engine's minimal massless closure)
python particles.py --particle photon
```

**Sample photon output:**
```text
=== PHOTON ===
open prefix         : +-
constituents        : one gauge loop (+-)
engine closure      : +-
final history       : +-
fold depth (pairs)  : 1
ZFA closed          : True
hermitian conjugate : +-
```

The two halves together close with zero free action — this is the QLF reading of every "photon" we ever detect: a joint emitter-absorber event, not a free projectile.

## 3. Electron–Proton Joint Closure (Hydrogen)

The proton is a composite Markov blanket with three-quark internal closures and gauge folds ([`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md), [`HadronicDepth.md`](HadronicDepth.md)). The electron half-loop joins the proton in a joint-ZFA bound state — **hydrogen**.

Hydrogen is the natural QLF observable: a charge-balanced, ZFA-closed joint event with mass `m(H) ≈ 938.78 MeV` and binding `E_bind ≈ 13.6 eV`. The electron's gauge-fold-depth contribution to the bound state is `m_e ≈ 0.511 MeV`; the proton contributes the rest. The binding energy is the residual joint-closure correction after the constituent rest energies.

Electron–proton **scattering** (rather than binding) is a transient joint closure that does not stabilise. Excess distinctions are emitted as photon joint closures (per §2). Hydrogen formation is the stable case. Note that the scattering partners need not match in energy or depth — §1e proves unequal components can enter one closed event — and that nothing in the closure depends on their spins or energies *through the charge* (§1c).

### Run the hydrogen joint closure

```bash
python particles.py --particle atom
```

**Sample interaction output:**
```text
=== ATOM ===   (hydrogen — electron ++ proton)
open prefix         : ^<v>^>v</\+-
constituents        : electron ++ proton (+ diagonal + gauge axes)
engine closure      : ^<v>^>v</\+-
final history       : ^<v>^>v</\+-
fold depth (pairs)  : 6
ZFA closed          : True
```

The output describes the **joint** closure, not the electron alone. The "electron's mass" of `m_e ≈ 0.511 MeV` is its share of the constructing delay distributed across the bound system.

## 4. Quick Reference Commands

| Demonstration | Command | What you see |
|---|---|---|
| Electron cycle (closed) + its gauge twist (open) | `python particles.py --particle electron` | The internal cycle closing; the gauge twist that does not, and so is not an event on its own |
| Photon half (massless) | `python particles.py --particle photon` | Pure forward-time spatial half-closure |
| Photon gauge loop (massless) | `python particles.py --particle photon` | Net action = 0 (joint event) |
| Hydrogen joint closure (e⁻ + p) | `python particles.py --particle atom` | Gauge handshake + photon emission; joint hydrogen bound state |

## 5. Links to More Advanced Reading

- [`lean/QLF_Handedness.lean`](lean/QLF_Handedness.lean) — **what is fundamental**: handedness is the primitive, ZFA is its balance on every axis, charge is its gauge component. Zero axioms.
- [`CP-Violation-and-Chirality.md`](CP-Violation-and-Chirality.md) §1a — the same primitive at the cosmological scale: a universe whose primitive is handedness has no reason to be handedness-symmetric.
- [`lean/QLF_ElectronClosure.lean`](lean/QLF_ElectronClosure.lean) — **the machine-verified core of §1**: the two closures, Hermitian ⇏ ZFA, charge as the gauge residue, no charge between spatial modes, harmonic and spin orthogonality, the closure period. Zero axioms.
- [`lean/QLF_Spin.lean`](lean/QLF_Spin.lean) — `fold_electron`, `chiralCharge`, `chiralCharge_conj` (charge conjugation = view from behind), `electron_not_majorana`.
- [`Bound_States_QLF.md`](Bound_States_QLF.md) — **the framing of this doc**: free leptons are not QLF observables; atomic systems are. Positronium, muonium, hydrogen as the natural mass observables. Reduced-mass Bohr binding structure.
- [`Delayed_Choice_Eraser.md`](Delayed_Choice_Eraser.md) — the same joint-closure framing applied to photons; the canonical "retrocausality" experiment dissolves once the photon is a Hermitian-pair handshake with no free-projectile interpretation.
- [`Collective_Electrodynamics.md`](Collective_Electrodynamics.md) — joint ZFA closures as the unit of EM interaction; vector potential as unresolved free action.
- [`HALF-SPIN-ZFA-EMBEDDING.md`](HALF-SPIN-ZFA-EMBEDDING.md) — the half-spin ZFA atom (Hermitian pair) as the minimal joint closure; the QLF unit of physical existence.
- [`Particles.md`](Particles.md) — full particle zoo and gauge-folding rule.
- [`Standard_Model.md`](Standard_Model.md) §3.3 — the three **lepton flavors** (e, μ, τ) as the three generations; colour *content* vs *charge*.
- [`Particle_Ladder.md`](Particle_Ladder.md) — where the electron sits on the vacuum↔atoms↔black-holes ladder; the flavor / colour-content question.
- [`Information_Physics.md`](Information_Physics.md) — the electron loop as one bit (½-spin = the atom of information, *it from bit*).
- [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md) — proton as composite Markov blanket; bound-state framing at the hadronic scale.
- [`Frequency_Synchronization.md`](Frequency_Synchronization.md) — constructing delay $\Delta t = R/f$.
- [`Hydrogen.md`](Hydrogen.md) — existing Bohr derivation of hydrogen levels in QLF language.
- [`Annihilation.md`](Annihilation.md) — the photon `^>` + antiphoton `v<` joint closure; electron–positron annihilation as a positronium-class joint event.
- [`Higgs.md`](Higgs.md) — gauge-fold-depth as the QLF mechanism for the gauge-fold contribution to bound-state mass.
- [`Entropy.md`](Entropy.md) — entropy conservation in joint closures.

## Conclusion

In QLF the electron is **not a free particle with mass `m_e ≈ 0.511 MeV`**, and it is **not an unfinished fragment either**. It is a **closed half-spin periodic mode carrying one unmatched gauge twist** — and that twist is its charge. It binds with a positron to form positronium, with an antimuon to form muonium, or with a proton to form hydrogen, because a manifest event is the larger closure in which the gauge deficit is matched. The "electron mass" of conventional physics is the gauge-fold-depth contribution to that joint closure, half of `m(positronium)` and the analogous contribution to `m(hydrogen)`.

Three things follow, each machine-verified:

$$
\boxed{\text{electron} = \text{closed periodic mode}}, \qquad
\boxed{\text{charge} = \text{residue of non-closure}}, \qquad
\boxed{\text{scale} = \text{closure wavelength},\; \text{not a radius}}
$$

And underneath all three, the primitive they are made of: **handedness**. A twist is a handedness on an axis and nothing else; ZFA is zero net handedness on every axis; charge is the gauge component of it. *Neutral does not mean handedness-free — it means handedness balanced.*

And the sharp one: **charge is blind to spin and energy**, because charge lives on the gauge axis and spin and energy live on the spatial axes. There is no charge *between* two electrons of different energy or different spin — the difference is exactly zero (`no_charge_between_spatial_modes`), and the coherent cross term between distinct harmonics or opposite spin channels is exactly zero as well (`channelKernel_diagonal`).

What remains is the common gauge imbalance both carry — and that is not an effect. **No event is ever charged** (`charge_nonzero_not_countBalanced`): a history with non-zero charge does not close, and what does not close is not an event and has no effect at all. The electron does not seek a partner and nothing is owed. It closes or it does not. What we call attraction and repulsion is the count of joint histories that DO close (`coulomb_is_a_counting_rule`) — **zero ways** for like charges, some for opposite. No force, no field, no action at a distance.

Photons are the same structural class: joint emitter-absorber closures, not free projectiles. The difference is the gauge fold — present in the electron half-loop, absent in the photon half-loop. Hence electrons contribute mass to their joint closures and photons do not.

Most everything we experience is the chemistry, light, and electric current of these joint closures. Understanding the electron in QLF means understanding which joint closures it can participate in — and the QLF observables are those joint closures, not the constituent halves.

**Don't shut up and calculate. Run it.**

Clone the repo, run the commands above, and watch the joint closures emerge from the same QuCalc engine.

See also: [`Bound_States_QLF.md`](Bound_States_QLF.md) — the framing of this doc, made explicit and scoped across positronium, muonium, hydrogen, and the τ-decay-vertex closure.

*Aligned with `Bound_States_QLF.md` — free leptons are not QLF observables; atomic systems are.*
