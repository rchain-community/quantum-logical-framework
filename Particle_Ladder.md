# The Particle Ladder — vacuum ↔ leptons ↔ hadrons ↔ atoms ↔ black holes

> **One generate-and-close cascade, run both directions.** In the [Quantum Logical Framework
> (QLF)](README.md) the same primitive — a ½-spin Zero-Free-Action (ZFA) closure carrying one bit
> — builds *up* from transient vacuum pairs through leptons, generations, hadrons, and atoms, and
> *down* from black holes by Hawking-unwind back to the vacuum. This document assembles pieces that
> already live across the repo into one coherent ladder, and marks honestly what is **machine-checked**,
> what is **structural** (prose/numeric), and what is **open**.

**Honest framing up front.** QLF already has the *primitives* and most *rungs* of this ladder as
verified or structural results. What is **not** yet done is an explicit map from topological
depth/axis to the observed mass ratios along the *whole* chain (now narrowed to one phase, `Δ = 2/3`,
§5). The temperature-dependent pair-production *rate* has since been reduced: its onset law and shape
are derived from the finite-capacity prune, and what remains is a measurement, not a derivation (§5).
The open piece is named, not glossed. So this is a
**synthesis + honest ledger**, in the style of [`Mysteries_Of_Physics.md`](Mysteries_Of_Physics.md)
and [`Information_Physics.md`](Information_Physics.md) — not a claim that the full ladder is proven.

**Status at a glance** (full detail in §5):

| Rung / claim | Status |
|---|---|
| ½-spin atom = one bit, `ΔF = −log 2` | ✅ machine-checked |
| 3 generations = 3 axes; Koide `⟹ m_τ` | ✅ machine-checked |
| baryon needs all 3 colours (confinement) | ✅ machine-checked |
| particle = quantum black hole (Compton = Schwarzschild) | ✅ machine-checked |
| decay = Hawking unwind, `log 2` released per unlock | ✅ machine-checked |
| mass spectrum = one exponentially-generated scale | ✅ machine-checked |
| bound-state atoms · fusion channel opening · temperature → stable rung | ◻ structural / modeled |
| pair-production mechanism (deterministic census + thermal freeze-out) | ◻ modeled — constructor + [`pair_production_demo.py`](pair_production_demo.py) |
| **`(R, axis) → observed mass ratios`** along the full chain | 🔵 **open — the priority gap** |
| analytic pair-production rate: onset law + shape derived from `boundedPrune`, residual is a measurement (#141) | ◻ reduced — [`census_congestion_freezeout.py`](census_congestion_freezeout.py) |

<p align="center"><a href="#rung-links"><img src="diagrams/particle_ladder.svg" alt="Bidirectional ladder: up the left (vacuum pair → lepton → generations e/μ/τ → hadron → atom → collective), down the right (black hole → Hawking unwind releasing log 2 → cascade → vacuum), hinged by particle = quantum black hole (Compton = Schwarzschild); creation is a deterministic census, temperature sets the freeze-out fraction" width="760"></a></p>

> The diagram is a static picture — GitHub can't make image regions clickable. **The per-box links to the QLF explanation of each layer are the table just below** (each doc in turn links to the live constructor).

<a id="rung-links"></a>**Each ladder box → its QLF explanation:**

| Ladder box | QLF explanation of that layer | live |
|---|---|---|
| **0 · Vacuum pair** | [`Creation.md`](Creation.md) — creation = separation of nothing into conjugate pairs (why the first distinction is two-valued) | [▶ e⁺e⁻](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=positronium%20%40%200%2C0%2C0) |
| **1 · Stable lepton (½-spin)** | [`Spin_QLF.md`](Spin_QLF.md) — spin *is* the twists; the ½-spin closure | |
| **2 · Generations e/μ/τ** | [`Standard_Model.md`](Standard_Model.md) — three generations = the three spatial axes | |
| **3 · Hadron / proton** | [`Quarks.md`](Quarks.md) — colour = the three axes; Borromean confinement | |
| **4 · Atom** | [`Bound_States_QLF.md`](Bound_States_QLF.md) — atoms as bound joint-ZFA closures (the real observables) | [▶ H](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=H%20%40%200%2C0%2C0) |
| **5 · Collective** | [`Chemistry.md`](Chemistry.md) — one valence rule; crystals, condensates | |
| **Black hole** | [`BLACK-HOLES.md`](BLACK-HOLES.md) — finite interiors, no singularity | |
| **Hawking / unwind** | [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md) — hadron = quantum black hole; decay = Hawking evaporation | |
| **Cascade** | [`Decay.md`](Decay.md) — the census-exponential prime-slip cascade | |
| **Vacuum (return)** | [`Creation.md`](Creation.md) §8a — the logical bang / Stage 0 | |
| **Hinge · particle = quantum BH** | [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md) — Compton = Schwarzschild (`QLF_QuantumBlackHole`) | |
| *Dynamics* | [`pair_production_demo.py`](pair_production_demo.py) — census creation + freeze-out | [▶ full cascade](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#t=0.95) |

---

## 1. The primitives (each already anchored)

| Primitive | What it is | Anchor |
|---|---|---|
| **The atom of the ladder** | one ½-spin ZFA Hermitian pair (bra-ket closure folding to `±I`); carries exactly one bit, `ΔF = −log 2` | `QLF_SpinorInformation`, `QLF_FreeEnergy` ([`Information_Physics.md`](Information_Physics.md)) |
| **Gauge fold `+−`** | a closure carrying a constructing delay `Δt = R/f` → local time + a Planck-scale Markov blanket (a primordial quantum-black-hole seed) | `QLF_PlanckScale` (`planck_self_dual`, `coherent_iff_subplanck`) |
| **Depth `R` / frequency `f`** | number of nested/sequential folds; sets the mass–frequency scale (`m = ℏf/R`) and the local clock rate (`f = 1/t`) | [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md), [`Time.md`](Time.md) |
| **Three axes** | the three spatial twist axes generate the three fermion generations | `num_generations_eq_three`, `generations_from_three_axes_constructive` ([`lean/QLF_Generations.lean`](lean/QLF_Generations.lean)) |
| **Temperature = logical density** | *precisely:* the local ZFA-closure rate (equivalently the inverse latency, `f = 1/latency`); it does **not** create pairs (the census does, §2) — it sets the **freeze-out fraction** of created pairs that persist as real vs virtual | [`Time.md`](Time.md), [`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean), [`Spacetime_Constructor.md`](Spacetime_Constructor.md) |

**The particle = micro-black-hole identity is proven.** A closure is a Markov-blanket horizon; the
Compton radius equals the Schwarzschild radius exactly at the Planck mass (`compton_eq_schwarzschild_iff`,
[`lean/QLF_QuantumBlackHole.lean`](lean/QLF_QuantumBlackHole.lean)), so **every hadron is a quantum
black hole** and a particle's decay is that black hole's Hawking evaporation
([`Hadron_BlackHoles.md`](Hadron_BlackHoles.md)). This is the hinge that lets the *same* ladder run
from particles to black holes and back.

---

## 2. The upward ladder — vacuum → atoms

| Stage | Object | Structure / depth | QLF status |
|---|---|---|---|
| **0. Vacuum fluctuation** | transient pair (e.g. `e⁺e⁻`), a horizon-open/unbalanced closure | `R ≈ 1`, short-lived | ✅ conjugate-pair closure (`ER_EPR_QLF`, `conjugate_pair_closes`); promotion *onset law* derived from the finite-capacity prune, normalisation `K_e` an input (#141, §5) |
| **1. Stable lepton** | one ½-spin (+ optional gauge fold) | `R` small | ✅ spin = twists (`QLF_Spin`); ν is Majorana (`neutrino_majorana`), e is Dirac |
| **2. Heavier generations** | same topology, deeper fold / higher-frequency axis | axis 2, 3 | ✅ **3 generations = 3 axes** (`num_generations_eq_three`); Koide `Q=2/3 ⟹ m_τ` (`three_generations_satisfy_koide`); free-lepton mass *ratios* not the observable (bound systems are) |
| **3. Hadron / proton** | three-axis colour-locked closure + gauge (Borromean) | `R` larger | ✅ **needs all three colours** (`baryon_needs_all_three_axes`, `single_colour_not_baryon`); confinement = a topological necessity; hadron = quantum BH (`compton_eq_schwarzschild_iff`) |
| **4. Atom** | lepton + hadron complementary joint-ZFA closure | bound state | ✅ structural — the QLF observable is the *bound* system (positronium/muonium/hydrogen), not the free lepton ([`Bound_States_QLF.md`](Bound_States_QLF.md)) |
| **5. Collective** | many atoms phase-locked | crystal / molecule / condensate | ✅ chemistry (one valence rule), crystals (Pauli), Cooper/BEC ([`Chemistry.md`](Chemistry.md), `QLF_CondensedMatter`) |

**Promotion rule (virtual → real) — two parts, and the split matters.** This is subtler than "heat
makes pairs," and the constructor already gets it right (reproduced outside the browser in
[`pair_production_demo.py`](pair_production_demo.py)):

- **Creation is a *deterministic census* cascade — no dice, no thermal gate.** Pairs are read out of
  the census by frequency (`m = 1/R`), so the *species ratios are the census multiplicities* —
  lightest dominate (`e⁺e⁻ : μ⁺μ⁻ : p p̄` in the illustrative model ≈ `0.90 : 0.075 : 0.025`), **not**
  a Boltzmann factor. "The census draws the space" (`QLF_CensusBrownian` / `QLF_BornProbability`).
- **Temperature only sets the *freeze-out fraction* — real vs virtual.** A created pair persists as
  **real** matter with a fraction that rises with the local logical density (temperature); at `T=0`
  every pair is virtual foam, near the Planck top ~97% are real. Persisting one bit still pays
  `ΔF = −log 2`. So heating does not *make* the heavier species — it lets more of the already-drawn
  census *stay*.

**Open:** calibrating the census buckets to the *measured* onsets (`e⁺e⁻ ~10¹⁰ K`, then `μ`, then `p`)
and deriving the freeze-out fraction analytically from the census — the constructor's edges are
illustrative, the *mechanism* is the QLF content (§5).

**Generation rule.** The three generations are the *same* topological pattern realized on the three
independent spatial axes (`generations_from_three_axes_constructive`). That the count is exactly three
is proven; the **mass ratios** `m_e : m_μ : m_τ` as functions of depth/axis are the open quantitative
target — QLF fixes one relation (Koide) and the *structure* (one scale, exponentially generated,
`spectrum_one_scale`, `log_transmuted_hierarchy`, [`lean/QLF_MassSpectrum.lean`](lean/QLF_MassSpectrum.lean)),
not the full ladder of ratios (`mass_spectrum_in_progress`).

### Colour *content* vs colour *charge* — the real question for μ and τ

The ladder raises a sharp question: since both colour and the generation count come from the same
**three spatial axes**, what is the colour structure of the muon and tau? The key is to split **net
colour charge** from **colour content** — they answer differently.

- **Net colour charge — firm.** Leptons are colour **singlets**: `B = 0`, no net colour, and *therefore
  free* — a net-coloured particle is confined (`singlet_closure`; a lone colour axis gives `B = 0`,
  `single_colour_not_baryon`). This is *why* we see free muons, and it does not change across generations.
- **Colour content — real, and mostly open.** A singlet is **not** structureless. The electron loop
  `^<v>` is machine-verified to engage **two** axes — `σ_y·(−σ_x)·(−σ_y)·σ_x = −I`, i.e. the x (`<>`) and
  y (`^v`) axes, *not* z (`interleaved_xlvr_folds_to_negI`, [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean)).
  So leptons carry genuine axis/colour content, and it is not obviously the same for every generation.

So the right question is not "do μ, τ carry colour?" (no *net* charge — they're free) but **"what is each
generation's axis/colour content?"** Since `num_generations_eq_three` ties the three generations to the
three axes, the natural hypothesis is that each generation is a chiral loop engaging a **different set of
axes** — the electron's verified content being `{x, y}`, with the muon and tau reaching the third axis
(the other coordinate planes `{y,z}`, `{z,x}`, or a deeper multi-axis winding). *What those "colours" are*
— which axes each generation occupies — is the open, promising structure, exactly as the second look
suggests.

**The one guardrail (confinement).** Whatever the content, a lepton must stay a colour-*neutral* singlet
(`B = 0`): "μ has two colours, τ three" has to mean a two-/three-axis **singlet**, not a coloured
(confined) state — otherwise it would be a Borromean baryon, not a free lepton. Distinguishing a 3-axis
lepton singlet from the 3-axis *baryon* (`B ≠ 0`, `baryon_needs_all_three_axes`) is precisely the content
to pin down.

**Where a proof would live.** Derive the μ and τ twist loops, read off their axis content, verify `B = 0`,
and show that content reproduces the Koide-constrained mass ratios — the `(R, axis) → mass-ratio` map
(§5, `mass_spectrum_in_progress`; the lepton↔quark mass correlation is still "separate and open,"
[`Quarks.md`](Quarks.md)). The electron's verified `{x, y}` content is the one anchor to build from.

**A first computational step** ([`lepton_flavor_axes.py`](lepton_flavor_axes.py), toward issue #140) enumerates
the short spatial ZFA closures and classifies them by axis content, splitting `B=0` **lepton singlets** from
`B≠0` **baryons**: the electron is one of the two-axis `{x,y}` singlets, and 1-axis, other-2-axis, and full
3-axis `{x,y,z}` **singlets** all exist — e.g. at length 6 the 3-axis content splits into **144 `B=0`
singlets** (candidate "three-colour" lepton content, `^v<>/\`) vs **576 `B≠0` baryons** (correctly confined).
So a colour-neutral 3-axis lepton genuinely exists and is distinct from the 3-axis baryon.

**This connects directly to Koide — the open piece is now *located*.** `QLF_Koide` derives `Q = 2/3` from
`N = 3` axes ∧ `A² = 2` — the **two *transverse* axes**, the one longitudinal axis being the common "1"
(`koide_two_thirds`, verified `Q = 0.6667` to 0.001%; `m_τ = 1776.97` MeV, 0.006%). And the electron `^<v>`
verifiably engages exactly **two axes `{x,y}`** — so **`{x,y}` *is* Koide's two transverse axes**, and the
longitudinal `z` is the "1" the electron does *not* engage. QLF_Koide already names the remaining input as
"the identification of the lepton √-mass vector with this 1-longitudinal + 2-transverse three-axis
structure; the Koide angle and overall scale stay open." **That is exactly issue #140**, now with the
electron's `{x,y}` as a *verified anchor*: the muon and tau reach the longitudinal `z` (the 3-axis content,
the 144 `B=0` singlets), and pinning their √-mass↔axis identification + the Koide angle + scale is the
open derivation.

---

## 3. The downward ladder — black holes → vacuum

The particle↔black-hole identity (§1) makes the descent the *same* ladder run in reverse:

| Stage | Process | QLF reading |
|---|---|---|
| **Black-hole seed** | a deep gauge-folded closure with a horizon blanket | primordial quantum BH (a particle *is* a micro-BH; `compton_eq_schwarzschild_iff`) |
| **Hawking / unwind** | one-step horizon re-entry of `+−` folds | pair emission; each unwound ½-spin atom **releases exactly `log 2`** back to the vacuum (`unlock_releases_log_two`, [`Annihilation.md`](Annihilation.md)) — unitary, charge/`J` preserved |
| **Cascade** | sequential unlocking of nested folds (prime phase-slip) | heavier → lighter generations, the reverse of §2 (`prime_slip_is_quarter_turn`, `collective_dump_positive`, [`lean/QLF_PrimeCascadeDecay.lean`](lean/QLF_PrimeCascadeDecay.lean); [`Decay.md`](Decay.md)) |
| **Final** | residual ½-spin pairs or pure vacuum | return to Stage 0 |

**Nested blankets → recursive cosmology without singularity.** Because a black-hole interior is a
child Markov blanket, it can host its own ladder — the *logical bang* drawn from inside
([`Creation.md`](Creation.md) §8a, `QLF_LogicalBang`), a fresh Stage-0 at the collapsed floor rather
than a metric singularity (`planck_length_floor`).

---

**Falsifiability.** The ladder's structural commitments are sharp enough to break:

| Observation | Verdict |
|---|---|
| a **fourth fermion generation** | ❌ tension with 3 generations = 3 axes (`num_generations_eq_three`) |
| a definitive **Dirac neutrino** (0νββ excluded) | ❌ tension with the Majorana Stage-1 lepton |
| a **new fundamental particle at the hadron scale** (WIMP-like) | ❌ against "hadron = quantum BH, no extra particle spectrum" |
| a **stable free quark** | ❌ refutes colour-locked confinement (`single_colour_not_baryon`) |
| black-hole evaporation shown **non-unitary** (information lost) | ❌ against the closure/unwind reading (`unlock_releases_log_two`) |

---

## 4. The one dynamics — generate, close, and temperature

The whole ladder is a single loop, both directions:

- **Generate.** The QuCalc engine expands every admissible twist history (the path-integral *generate* step).
- **Select.** Only ZFA-balanced histories persist (`full_zeno_prune` — the *firebreak*).
- **Temperature = logical density.** Which depth/`R` is stable is set by the local closure rate; heating shifts the stable rung up the ladder (pair thresholds), cooling lets it recombine down (atoms, then chemistry).
- **Cascade.** Prime-/depth-synchronized unlocks produce the sequential transitions (§3).
- **Photon.** Every emission/absorption is a joint-ZFA handshake, not a flying projectile ([`Collective_Electrodynamics.md`](Collective_Electrodynamics.md)).

**This is not a thought experiment — it runs.** The [interactive constructor](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html) *is* this ladder: heat the vacuum toward the Planck top and watch **black holes form → Hawking-cascade into hadrons → cool into nuclei → recombine into atoms → do chemistry**, from the census alone, nothing scripted ([`Spacetime_Constructor.md`](Spacetime_Constructor.md)).

- [▶ heat to the Planck top — the full cascade](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#t=0.95)
- [▶ a transient e⁺e⁻ vacuum pair](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=positronium%20%40%200%2C0%2C0) · [▶ an α (⁴He) closure](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=alpha%20%40%200%2C0%2C0) · [▶ a hydrogen atom](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=H%20%40%200%2C0%2C0)

---

## 5. The scorecard — proven, structural, open

**✅ Machine-checked (the rungs and the hinge):**
- the ½-spin atom carries one bit / `ΔF = −log 2` (`QLF_SpinorInformation`, `QLF_FreeEnergy`);
- **3 generations = 3 axes** (`num_generations_eq_three`); Koide `⟹ m_τ` (`three_generations_satisfy_koide`);
- **baryon needs all three colours**; confinement (`baryon_needs_all_three_axes`, `single_colour_not_baryon`);
- **particle = quantum black hole**; Compton = Schwarzschild at the Planck mass (`compton_eq_schwarzschild_iff`);
- **decay = Hawking unwind**, each unlock releasing `log 2` (`unlock_releases_log_two`, `collective_dump_positive`);
- the Planck closure floor — no singularity (`planck_length_floor`, `planck_self_dual`);
- the mass spectrum is **one scale, exponentially generated** (`spectrum_one_scale`, `log_transmuted_hierarchy`).

**◻ Structural (prose / numeric, mechanism anchored, value not derived):**
- bound-state atoms (positronium/muonium/hydrogen) as the QLF observables ([`Bound_States_QLF.md`](Bound_States_QLF.md));
- the fusion rungs — `pp` Pauli-blocked, the `pn`/deuteron channel opens (`diproton_pauli_blocked`, `deuteron_channel_closes`);
- the temperature → stable-rung correspondence, demonstrated in the constructor but not analytically derived.

**🔵 Open (real research, not doc-work — do not fake):**
- **The priority gap — narrowed from a mass map to one phase.** A direct `(R, axis) ↦ observed mass
  ratio` census map is a **proven negative**: every census integer at the lepton rungs is 5-smooth, the
  measured mass ratios are not, off by `0.14–0.61%` — orders of magnitude outside where the model
  otherwise holds ([`Weak_Force.md` §5c‴](Weak_Force.md#5c-the-r-axis--mass-ratio-map-a-shape-theorem)).
  The map instead factors `census → Δ → masses`: three phases `1+√2·cos(Δ/3+2πk/3)` at a single rational
  `Δ = 2/3` (`m_μ/m_e = 206.77`) reproduce the Koide relation and `m_τ/m_e` to `0.01%`, and the `~3500×`
  hierarchy is now understood structurally — proximity to a derived "massless wall" `1+√2 cos θ=0`
  (`A²=2` from the two transverse axes), quadratically amplified, not a hierarchy of scales
  ([`Weak_Force.md` §5c⁗](Weak_Force.md#5c-deriving--23--what-stands-what-is-closed-and-the-specification-that-remains)).
  **What's still open:** deriving `Δ = 2/3` itself as a *forced*, not selected, `O(1)` rational — twelve
  routes tried and closed (census count-ratio, circle division, all three curvature notions, symmetric
  spectral functionals, absolute-mass arguments, and last the mode-locked rotation number — a rotation
  number is a turn-fraction and `Δ` is `1/(3π)` of a turn, so the data admits no locking below
  denominator `311`), **zero live candidates**; a three-clause specification any future one must meet
  (`O(1)` rational in radians, forced, of arc-over-radius shape); full
  history in [#140](https://github.com/jimscarver/quantum-logical-framework/issues/140).
- **The pair-production rate — reduced to one measurement (#141, closed).** The *mechanism* is modeled
  (deterministic census creation + thermal freeze-out, [`pair_production_demo.py`](pair_production_demo.py)),
  the **onsets are calibrated** ([`pair_freezeout_calibration.py`](pair_freezeout_calibration.py)) to the
  textbook e→μ→p temperatures (~10¹⁰, 10¹², 10¹³ K), and the **functional form is now derived, not posited**:
  running the actual `boundedPrune` against a thermal pruning budget `R ~ Poisson(λ(T))`, the linear onset
  `T_onset ∝ d_s ∝ m` *emerges* from `λ(T)=T`, and the shape is a Poisson-tail freeze-out **sharper** than
  the constructor's logistic — a distinct, testable prediction ([`census_congestion_freezeout.py`](census_congestion_freezeout.py)).
  What remains is not a derivation gap but a **measurement**: under `λ(T) ∝ T^p` the onset scales as
  `T_onset ∝ d^{1/p}`, so the onset-vs-mass log–log slope *is* the budget exponent (`slope 1 ⟺ λ ∝ T`).
  Inputs kept honest: `K_e` (the absolute normalisation) and the linearity of `λ(T)`.
- absolute mass scale (`v = R_stable`, frontier #1, [`Open_Problems.md`](Open_Problems.md)).

**Deliberately *not* built:** a "unified Lean module" for the ladder. It would be reuse-only — re-exporting the theorems above with no new content — so it is not worth a module. The ladder's value is as this synthesis; each rung is already verified in its own module.

---

## See also

- [`Bound_States_QLF.md`](Bound_States_QLF.md) — free leptons are not QLF observables; atoms are (Stage 4).
- [`Decay.md`](Decay.md) · [`Annihilation.md`](Annihilation.md) — the downward ladder; decay = Hawking unwind, `log 2` released per atom.
- [`BLACK-HOLES.md`](BLACK-HOLES.md) · [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md) — the particle = quantum-black-hole identity, the hinge of the two directions.
- [`HALF-SPIN-ZFA-EMBEDDING.md`](HALF-SPIN-ZFA-EMBEDDING.md) · [`Spin_QLF.md`](Spin_QLF.md) — the ½-spin atom.
- [`Creation.md`](Creation.md) §8a — the logical bang; Stage 0 and nested-blanket recursion.
- [`Information_Physics.md`](Information_Physics.md) — each rung a closure carrying bits; `it from bit`.
- [`Spacetime_Constructor.md`](Spacetime_Constructor.md) — the ladder, running live, temperature-driven.
- [`Open_Problems.md`](Open_Problems.md) — the open quantitative rungs, kept in sync.
