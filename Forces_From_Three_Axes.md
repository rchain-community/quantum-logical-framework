# Forces from the three axes — a gauge-structure synthesis

**A structural conjecture: the Standard-Model gauge group `U(1) × SU(2) × SU(3)` is the symmetry algebra of [QLF](README.md)'s three spatial axes.** This collects pieces QLF has *separately* — and all three gauge algebras are **machine-verified**: U(1) electromagnetism (`no_magnetic_monopoles`), the weak `SU(2)` (`weak_isospin_su2`), and the strong `SU(3)` (`trace_commutator_zero` + `gluon_commutator_nonzero`), alongside the `N = 9 = 3²` directional-coupling tensor that fixes [α](Alpha.md) — into one reading, motivated by the intuition that **the weak and strong forces are the electromagnetic gauge-twist mechanism seen from different projections of the same 3-axis structure**.

**Read this as a program, not a result.** The verified anchors are marked ✓; the synthesis itself is a conjecture (🔶); what it does *not* do is marked in §6. It derives no coupling constants, no chiral structure, and no masses.

---

## 1. The verified anchors (what QLF already has, separately)

| force | QLF object | algebra | status |
|---|---|---|---|
| **EM** | the `+`/`−` gauge fold (`U(1)` gauge swap) | `u(1)`, dim **1** | ✓ derived; `no_magnetic_monopoles` Lean-verified |
| **weak** | the Σ₈ τ-quaternion subalgebra of the 3 spatial axes (`τᵢ = iσᵢ`) | `su(2)`, dim **3** | ✓ Lie algebra machine-verified — `weak_isospin_su2` ([`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean), [`Weak_Force.md`](Weak_Force.md) §3) |
| **EM coupling α** | the `3 × 3` **directional-coupling tensor**, `N = 9 = 3²` | (of the 3 axes) | ✓ `α = 1/137` to 0.026%, `N = 9` Lean-anchored ([`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1, `QLF_FineStructureSubstrate.lean`) |
| **strong** | the **traceless** part of the `3×3` directional tensor (three-quark Borromean three-fold) | `su(3)`, dim **8 = 3²−1** | ✓ Lie algebra machine-verified — `trace_commutator_zero` (closure) + `gluon_commutator_nonzero` (non-abelian), `strong_su3_summary` ([`lean/QLF_StrongAlgebra.lean`](lean/QLF_StrongAlgebra.lean)) |

Each is tied to the **three spatial axes** `^v / <> / /\` (or the gauge fold `+-`). They have never been tied *together*. This doc does that.

---

## 2. The dimension alignment 🔶

The Standard-Model gauge group has

$$\dim\bigl(U(1) \times SU(2) \times SU(3)\bigr) \;=\; 1 + 3 + 8 \;=\; \mathbf{12}.$$

Every one of these dimensions is a feature of the **three-axis directional structure**:

- The `3 × 3` directional-coupling tensor of the three spatial axes is `u(3)`, of dimension `3² = 9` — this is exactly the **`N = 9`** that fixes α. It splits canonically:
  $$u(3) \;=\; \underbrace{u(1)}_{\text{trace} = 1} \;\oplus\; \underbrace{su(3)}_{\text{traceless} = 3^2 - 1 = 8}.$$
  The **trace** is the single scalar direction — **electromagnetism** `U(1)`. The **traceless** part has dimension **8** — the **eight gluons** of **`SU(3)`**, i.e. the strong force as the traceless directional couplings among the three axes (the same axes whose Borromean three-fold binding is the proton).
 The traceless part being a genuine non-abelian Lie algebra is **machine-verified** (`trace_commutator_zero`: every 3×3 commutator is traceless ⇒ closed under the bracket; `gluon_commutator_nonzero`: it is non-abelian — [`lean/QLF_StrongAlgebra.lean`](lean/QLF_StrongAlgebra.lean)).
- The remaining `su(2)`, dimension **3**, is the **half-spin / τ-quaternion** algebra of the same three axes (`iσₓ, iσᵧ, iσ_z`) — the **weak** force, already machine-verified as `weak_isospin_su2`.

So
$$12 \;=\; \underbrace{9}_{u(3)\ =\ \text{EM}\,\oplus\,\text{color, the }N=9\text{ α tensor}} \;+\; \underbrace{3}_{su(2)\ =\ \text{weak, half-spin}}.$$

The dimensions are not adjustable: `dim u(3) = 9` (the α tensor), `dim su(2) = 3` (verified), `dim su(3) = 9 − 1 = 8`. They add to the SM's 12 with nothing left over.

---

## 3. The reading — "weak & strong are EM from different 3-axis projections" 🔶

Under this synthesis, there is **one** mechanism — the **gauge-twist closure** on the three spatial axes — and the three "forces" are which component of the `3 × 3` directional structure the closure rotates:

- **EM** = the **trace** (`U(1)`): the overall scalar gauge phase (the `+−` fold).
- **strong** = the **traceless** part (`SU(3)`, 8 gluons): the directional couplings *among* the three axes — the same three-foldness that confines quarks Borromean-style.
- **weak** = the **half-spin `SU(2)`** (τ-quaternion): the spinor rotations of the axes — the chirality-mediated pair-flip.

This is precisely the intuition that *the weak and strong forces are electromagnetism seen from different 3-D perspectives*: same gauge-twist closure, different projection (scalar / spinor / tensor) of the one three-axis object. The universal mediator is the **gauge-twist vertex** that already produces α; the gauge *group* is the projection it acts through.

---

## 3a. Completing the unification: projections × densities, and electroweak breaking 🔶

§3 says the three forces are one gauge-twist seen through different projections. Two more pieces close
the loop — the **crisp algebraic form** of "different projections," and the **second axis** (logical
density) that makes them look so different at low energy.

**The crisp form: EM is the *abelian* sector; weak and strong are *non-abelian* projections.** This is
now machine-anchored ([`lean/QLF_GaugeUnification.lean`](lean/QLF_GaugeUnification.lean)):

- **EM = abelian** — the gauge-fold (Pauli scalar) group *commutes* (`em_gauge_abelian`, reusing
  `QLF.PauliScalar.mul_comm`). An abelian generator self-interacts with nothing, so the **photon is
  massless and long-range** — the unbroken `U(1)`.
- **Weak & strong = non-abelian** — the projections *do not commute* (`strong_nonabelian` =
  `gluon_commutator_nonzero`; `weak_isospin_su2`, `[τᵢ,τⱼ]=−2εᵢⱼₖτₖ ≠ 0`). A non-abelian generator
  self-interacts, so these are **short-range, confined / massive**.

So the **abelian/non-abelian split *is* the massless-photon-vs-massive-`W`/`Z` split** — electroweak
unification's heart, restated as substrate structure (`gauge_unification_signature`).

**The gauge *force* (dynamics), machine-verified.** Beyond the algebras, the *interaction* is the
**holonomy** of the closure connection — the Wilson-loop plaquette `A·B·A⁻¹·B⁻¹`: trivial in the abelian
(EM) sector (`em_plaquette_trivial = 1` — flat `U(1)`, massless long-range photon) and non-trivial in the
non-abelian sector (`σxσyσxσy = -1 ≠ 1` — curved `SU(2)`/`SU(3)`, self-interacting `W`/gluon)
([`lean/QLF_GaugeHolonomy.lean`](lean/QLF_GaugeHolonomy.lean)). **Confinement** is the singlet-closure
obstruction: a net-colored state carries an annihilation-odd signed count that is **zero on every ZFA
closure**, so a lone quark *cannot close* — only color singlets are physical (`charged_not_closed`,
`singlet_closure`, [`lean/QLF_Confinement.lean`](lean/QLF_Confinement.lean)); the flux-tube linear
potential is the constructing delay growing with separation. And **mass is the gauge-fold delay** `m=1/R`
— a fold makes mass (`weak_boson_mass_pos`), the abelian photon stays massless, custodial `ρ=1`
([`lean/QLF_HiggsMechanism.lean`](lean/QLF_HiggsMechanism.lean)). The couplings `g₁,g₂,g₃`, the string
tension, and the Higgs VEV stay the open dynamics.

**The second axis — logical density (blanket frequency).** The *same* force looks different at
different Markov-blanket densities (the "different 3-D perspectives" are perspectives *at different
frequencies*):

- **Low density / free** → the abelian limit: ordinary long-range **EM** (massless photon).
- **High density (inside a hadronic blanket)** → the non-abelian **strong** projection dominates —
  confinement, the three-axis Borromean binding.
- **The weak projection is the one that *re-projects the blanket itself*** — a flavour change is a
  change of which 3-D perspective the blanket presents. That is exactly why the weak force
  **catalyzes**: it is the force that transforms one blanket into another (the β⁺ keystone that lets
  two Markov blankets join, [`Fusion.md`](Fusion.md) §3a, [`SEX.md`](SEX.md)).

**Electroweak symmetry breaking = the density threshold.** Above it (high frequency / energy) the
projections are symmetric — all gauge bosons massless, the electroweak symmetry unbroken. Below it the
Markov-blanket structure — QLF's constructive Higgs, the **gauge-fold delay** of
[`Higgs.md`](Higgs.md) §3–4 — **confines the non-abelian projections**: `W`/`Z` acquire mass as
gauge-fold depth (`m = 1/R`, [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md)), while the
abelian trace, the photon, stays free. The projection ratio is the **Weinberg angle `sin²θ_W = 3/8`**
(`sin2_weinberg_substrate_eq`, [`QLF_WeinbergAngle`](lean/QLF_WeinbergAngle.lean)).

**The one statement.** *There is one substrate gauge interaction. The three forces are its **abelian
trace** (EM) and its **non-abelian spatial projections** (weak `SU(2)`, strong `SU(3)`) of the same
three axes, seen at different **logical densities**. The photon is the free abelian limit; the `W`,
`Z`, and gluons are the blanket-confined non-abelian modes. Electroweak symmetry breaking is the
density threshold below which the blanket confines the non-abelian projections and gives them mass; the
weak projection catalyzes because it re-projects the blanket.* This is the same `6+2` / three-axis
structure that fixes `α` (`N=3²`), `Ω_Λ` (`2/8`), `sin²θ_W` (`3/8`), and the `5̄⊕10` generation (§5a).

**Honest scope.** This ties the *proven* pieces — the three gauge algebras, the abelian/non-abelian
split, the Weinberg `3/8`, and Higgs-as-gauge-fold-delay — into one structural unification. It does
**not** derive the gauge *couplings*, the `W`/`Z` mass *values* (which need the Higgs VEV), the RG
running, or the symmetry-breaking dynamics as a field theory (`gauge_unification_in_progress`); those
remain the open electroweak sector (§6, [`Weak_Force.md`](Weak_Force.md) §2).

---

## 3b. And gravity: the fourth force as the geometry of the same closures 🔶

The three gauge forces (§3, §3a) are the gauge-twist **vertex** — how *individual* ZFA closures
interact, the projections of one gauge fold on the three axes. The fourth force, **gravity, is not a
fourth gauge force.** QLF does not try to make gravity a gauge interaction (the move that has defeated
quantum-gravity programs for fifty years). Gravity is the **emergent geometry of the *aggregate* of
closures** — the same events, read collectively instead of individually:

- the **causal order** of the closures is a causal set ([`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean)),
  whose number↔volume and layer-growth give the metric and curvature (Sorkin / Benincasa–Dowker,
  [`QLF_CausalInterval`](lean/QLF_CausalInterval.lean), [`QLF_CausalDimension`](lean/QLF_CausalDimension.lean));
- the **thermodynamics** of each local horizon fixes the coefficient `8πG = 2π/η` and `Λ = log 2`
  (Jacobson, [`QLF_EinsteinEquations`](lean/QLF_EinsteinEquations.lean), [`Einstein_Equations.md`](Einstein_Equations.md)).

So the gauge forces are how closures **interact**; gravity is how closures **arrange**. Same substrate,
read at two scales.

**The hinge that joins them is mass = constructing delay.** In §3a, electroweak symmetry breaking gives
`W`/`Z` their mass as **gauge-fold depth** — the constructing delay `m = 1/R`
([`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md)). That *same* delay, aggregated over the
causal-set geometry, is exactly what curves spacetime — gravity sources on mass-energy. So the
gauge-fold delay is **both** the output of the Higgs sector (inertial mass) **and** the source of
gravity (gravitational mass): the **equivalence principle falls out of the substrate** — one delay,
read as inertia at the vertex and as curvature in the geometry. (The graviton is correspondingly *not*
a fundamental gauge boson but spin-2 = four half-spins, a composite,
[`QLF_GravitationalWaves`](lean/QLF_GravitationalWaves.lean).)

**The complete statement — all four forces are ZFA closure.**

> One substrate: ZFA closure. The **gauge forces** are the closure *vertex* — one gauge twist seen as
> its abelian trace (EM) and non-abelian spatial projections (weak `SU(2)`, strong `SU(3)`) at
> different logical densities. **Gravity** is the closure *geometry* — the causal-set curvature and
> horizon thermodynamics of the aggregate. **Mass** — the constructing delay — is the hinge: the
> gauge-fold delay that the Higgs sector reads as inertia is the same delay the geometry reads as
> gravity. Four forces, one closure, joined at mass.

**Honest scope.** Gravity is unified **under** the substrate (emergent geometry), *not* **as** a gauge
force — that is the claim, and it is the right one (gravity has no gauge boson; the graviton is
composite). What stays open is the dynamical side: the discrete d'Alembertian → Ricci on the branching
graph and the continuum field equations (the named causal-curvature rung,
[`Einstein_Equations.md`](Einstein_Equations.md) §6a), and on the gauge side the couplings and the
Higgs VEV (§3a). The *unification* — four forces as one closure, joined at mass — is structural and
substrate-grounded; the quantitative dynamics on each side are the remaining work.

---

## 4. Quark flavors, honestly

The synthesis says **color `SU(3)` = the traceless 3-axis directional tensor**, consistent with the existing Borromean three-quark picture (the three "colors" = the three axes). But the flavor sector is almost entirely open in QLF:

- ✗ **No twist assignments** for the six quark flavors (only the electron `^<v>`, neutrino `^v`, photon `^>` have signatures).
- ✗ **No individual quark masses.**
- ⚠ **Flavor change** (`d → u`) is the gauge-fold pair-flip *operation* ([`Weak_Force.md`](Weak_Force.md) §4); the explicit vertex topology is open.
- ✗ **CKM mixing angles** — open ([`Standard_Model.md`](Standard_Model.md) §4.2).
- ✓ **Confinement** — derived (quarks are fractional ZFA; only Borromean triples close).

So the synthesis upgrades the *gauge* picture (color = traceless 3-axis tensor) but leaves the *flavor* picture where it was: open.

**A structural step on the flavour bullet.** Reading the baryon as a *knot of closures* — the three colour axes (`<>`,`^v`,`/\`) split one per quark (Borromean → `B=+1`), with charge as the gauge direction shared `1/3` per colour — deduces the *content* `uud` (proton, `+1`) / `udd` (neutron, `0`), differing by one `u↔d` gauge-fold pair-flip, and the electron-out (hydrogen) vs electron-in (neutron) contrast. This is the colour-axis-split + `1/3`-share *structural reading*; the explicit per-flavour twist string (bullet 1 above) stays open. See [`Atomic_Structure_QLF.md`](Atomic_Structure_QLF.md) §7.

**A category note on quark masses.** Asking for *quark masses* (e.g. a "quark Koide") is the wrong object in QLF: quarks are fractional ZFA with no independent mass — only hadrons are observables, and the quoted quark masses are scheme-dependent Lagrangian parameters. The physical, observable quantity is the mass *difference* — hadron isospin splittings like `m_n − m_p = (m_d − m_u) − EM`, which *are* the quark flavor step (`d↔u` = the weak vertex). That is the well-posed target; see [`Weak_Force.md`](Weak_Force.md) §5d.

---

## 5. Leptons mirroring quark structure — the "three" 🔶

The companion intuition — *lepton masses mirror proton processes at different frequencies* — finds partial support:

- The three **lepton** generations are three **phases** (120° apart) of one gauge-fold closure ([`Weak_Force.md`](Weak_Force.md) §5b, `koide_two_thirds` machine-verified) — "different frequencies of one closure" made precise.
- The **proton** is three **quarks** (Borromean), with `m_p/m_e = 6π⁵` carrying `|S₃| = 6` (the three-quark permutation) and `π⁵` (a 5-angle hidden-chirality integration) ([`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md), `mass_ratio_QLF_eq`).

Both are a **"three"** of the three axes — three lepton phases, three quark colors. Whether the lepton 3-phase structure and the quark 3-color structure are the *same* three-axis "three" (so that the lepton spectrum literally mirrors the three-quark hadronic structure at scaled frequency/depth) is an open, testable conjecture — the natural next probe of intuition #2. It is **not** established here.

---

## 5a. QLF and SU(5) — reproducing the wins, escaping the failure 🔶

Georgi–Glashow **SU(5)** is the smallest simple group containing `SU(3)×SU(2)×U(1)`. QLF is **not** an
SU(5) GUT — it does not embed the SM in a simple group — yet it has a precise relationship to it: QLF
reproduces SU(5)'s genuine, parameter-free successes from the **same 3-axis substrate**, while its own
topology explains the prediction that *sank* minimal SU(5).

**1. `sin²θ_W = 3/8` — SU(5)'s parameter-free win, read from the substrate.** In SU(5) the value comes
from the trace normalization over the `5̄ = (3 colored d^c) + (2-component lepton doublet)`:
`sin²θ_W = ΣT₃²/ΣQ² = (1/2)/(4/3) = 3/8`. In QLF it is the **spatial fraction** `3/8` (3 spatial twists
/ 8-twist alphabet, [`QLF_WeinbergAngle`](lean/QLF_WeinbergAngle.lean)). The "`5 = 3 + 2`" of SU(5) *is*
QLF's "3 spatial axes + 2 gauge twists" — same `3`, same split, same `3/8`. QLF supplies the **substrate
origin** of the number Georgi–Glashow discovered. (Honest scope unchanged: it is the *unification*
value; the RG running to the measured `0.231` is open, [`Weak_Force.md`](Weak_Force.md) §2.)

**2. `5̄ ⊕ 10 = 15` — one generation IS the antisymmetric tensor content of QLF's `3 ⊕ 2`.** The `15`
left-handed Weyl fermions of a generation are not an extra input: they are exactly the **rank-≤2
antisymmetric tensors over the fundamental `5`** — rank 1 → the `5` (conjugated to `5̄`), rank 2 →
`Λ²(5)`, of dimension `C(5,2) = 10`. QLF identifies that fundamental with its own split `5 = 3 ⊕ 2`
(the same `3+2` behind `α`, `Ω_Λ`, and `3/8`), and the whole generation falls out:

| SU(5) piece | as a tensor of `5 = 3⊕2` | SM field | count |
|---|---|---|---|
| `5̄` | `3̄ ⊕ 2` | `d^c` ⊕ `(ν,e)` | `3 + 2 = 5` |
| `10` | `Λ²3 ⊕ (3⊗2) ⊕ Λ²2` | `u^c` ⊕ `Q` ⊕ `e^c` | `3 + 6 + 1 = 10` |
| **generation** | rank ≤ 2 antisymmetric | | **`15`** |

Machine-verified in [`lean/QLF_SU5.lean`](lean/QLF_SU5.lean) (`generation_eq_fifteen`,
`ten_decomposition`, `ten_pieces`). Two QLF readings ride along: the antisymmetry of the `10` **is the
Pauli/fermionic wedge** (`pauli_exclusion`) — a generation is the *fermionic* tensor content of the
`3⊕2` substrate; and the count is **15, not SO(10)'s 16** (`so10_eq_sixteen`) — exactly what QLF's
**Majorana neutrino** wants (no independent light Dirac `ν_R`; any `ν_R` is the heavy seesaw partner, a
sterile pure-gauge sequence).

**3. QLF is *not* the embedding — and that is a feature.** QLF unifies the forces as the symmetry of the
three spatial axes directly (`dim = 1+3+8 = 12`, with `1+8 = 9 = N`, §2), *not* by embedding the SM in
the simple group SU(5) (`dim 24`). The `24 − 12 = 12` extra SU(5) generators are the **X/Y leptoquark
bosons**. QLF has no fundamental X/Y; in QLF they would be a higher-order gauge-fold **re-entry forbidden
at low logical density**.

**4. No proton decay — escaping SU(5)'s fatal failure.** Minimal SU(5)'s signature is `p → e⁺π⁰` via
X/Y at `τ_p ~ 10³⁰–10³¹ yr` — **experimentally excluded** (Super-K, `τ_p > 2.4×10³⁴ yr`); this killed
minimal Georgi–Glashow. In QLF, **baryon number is a topological winding invariant** (`baryon_dagger_odd`,
[`lean/QLF_BaryonWinding.lean`](lean/QLF_BaryonWinding.lean)) — the proton's 3-axis Borromean linking —
conserved by the low-density vacuum; the re-entry that would unwind it is forbidden. **QLF keeps SU(5)'s
good prediction (`3/8`) and drops its bad one (fast proton decay)**: proton stability is structural, not
fine-tuned.

**5. Charge quantization without the multiplet.** SU(5)'s other genuine win — `Q_proton = −Q_electron`
*exactly*, because quarks and leptons share a multiplet — QLF gets independently: charge is an
**exactly-conserved signed twist count** (`signed_count_conserved`,
[`lean/QLF_BMinusL.lean`](lean/QLF_BMinusL.lean)) and every closure is neutral, so charges are quantized
and balanced with no unifying multiplet needed.

**The honest reading.** SU(5) is a *partial rendering* of the substrate's `3+2` structure — right where
it reflects the genuine "3 axes + 2 gauge" counting (the `3/8`, the `5̄⊕10` generation, charge
quantization, one coupling at high scale), wrong to promote the X/Y re-entry modes to fundamental gauge
bosons (hence the proton decay that does not happen). QLF unifies *below* SU(5): not a bigger group, the
shared 3-axis tensor `N=9`. **Scope:** the `3/8` is the unification value (running open); the `5̄⊕10`
result anchors the **counting and group-theoretic decomposition under the `5=3⊕2` identification**, not
the hypercharges, the chirality, or the per-field twist-closure map (`su5_generation_content_in_progress`);
QLF derives no GUT scale, X/Y masses, or proton-lifetime number.

---

## 6. What this is NOT

- **Not a derivation of the Standard Model.** This is a **dimension/structure alignment** (`12 = 1 + 3 + 8`, with `1 + 8 = 9 = N`) plus a conjecture that the gauge group *is* the three-axis symmetry. It derives **no** coupling constants, **no** running, **no** chiral structure (why `SU(2)_L` is left-handed), **no** hypercharge assignments, and **no** masses.
- **The `su(3)` algebra is Lean-verified, but only the algebra.** `trace_commutator_zero` + `gluon_commutator_nonzero` prove the traceless 3×3 matrices are a non-abelian Lie algebra (the gauge algebra of the strong force). What is *not* machine-proved is the `finrank = 8` count (it is the elementary codimension-1 trace constraint, `8 = 3² − 1`, not yet a Lean `finrank` theorem) — and, as for all three legs, **no coupling, no confinement scale, no asymptotic freedom**. The example generators `g1, g3` are Hermitian, not the genuine anti-Hermitian `su(3)` elements — `h1 := i·g1, h3 := i·g3` (added alongside, `su3_anti_hermitian_summary`) are the compact-real-form witnesses, matching `BraKetRhoQuCalc.lean`'s `τᵢ = i·σᵢ` weak-sector convention.
- **A separate, speculative thread — octonions.** [`Octonion_G2_Unification.md`](Octonion_G2_Unification.md) explores whether this `SU(3)`/weak-`SU(2)` structure generalizes to a larger (octonion, 7-imaginary-unit) axis set taken 3 at a time; it independently reproduces the classical `G2 ⊃ SU(3) ⊃ SU(2)` stabilizer chain and a real quark/gluon bracket relation, but does **not** establish that this octonion-native `su(3)`/`su(2)` is the same representation as the one here — kept separate until (if) that identification is resolved.
- **Not electroweak unification or a GUT.** No symmetry-breaking scale, no unification of couplings, no proton-decay prediction.
- **Not a quark-flavor theory.** Flavors, masses, and CKM stay open (§4).

The defensible claim is narrow and worth stating plainly: **all three gauge algebras are machine-verified** — `U(1)` (`no_magnetic_monopoles`), `SU(2)` (`weak_isospin_su2`), and `SU(3)` (`trace_commutator_zero` + `gluon_commutator_nonzero`) — and their dimensions `1 + 3 + 8 = 12`, with `1 + 8 = 9 = N` the α directional tensor, line up exactly with the Standard-Model gauge group as the symmetry of the three spatial axes. That makes "all three forces from the three axes" a sharp, falsifiable target rather than a slogan — though the couplings, chirality, and masses remain entirely open.

---

## 7. References

### Internal (QLF)
- [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean) — `weak_isospin_su2` (the `SU(2)` anchor).
- [`Weak_Force.md`](Weak_Force.md) — the weak sector; §3 (SU(2)⊂Σ₈), §5b (lepton 3-phases / Koide).
- [`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1 — α from the `N = 9 = 3²` directional-coupling tensor; `QLF_FineStructureSubstrate.lean`.
- [`Standard_Model.md`](Standard_Model.md) §3.4, §6 — U(1)/SU(2)/SU(3) status; gauge-group identification as open work.
- [`Hadrons_Markov_Blankets.md`](Hadrons_Markov_Blankets.md), [`Proton_Resonance_R_e.md`](Proton_Resonance_R_e.md) — the three-quark Borromean proton; `m_p/m_e = 6π⁵`.
- [`Conservation.md`](Conservation.md) §8 — the "every ZFA-preserving symmetry → conservation law" methodology (which this synthesis instantiates for the gauge sector).
- [`Open_Problems.md`](Open_Problems.md) — registry status.

### External
- The Standard Model gauge group `SU(3)_c × SU(2)_L × U(1)_Y` (dim 8 + 3 + 1 = 12); the eight gluons of `SU(3)`; `su(N)` has dimension `N² − 1`.
- Grand-unified theories (SU(5), SO(10)) — QLF does **not** embed the SM in a simple group, but it has a precise relationship to SU(5) (§5a): it reproduces the parameter-free wins (`sin²θ_W=3/8`, the `5̄⊕10=15` generation, charge quantization) from the same `3+2` substrate, and its baryon-winding topology explains the *non*-observation of proton decay that sank minimal SU(5).
