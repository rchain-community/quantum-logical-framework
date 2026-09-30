# The Mysteries of Physics in QLF — Addressed, and Remaining

A survey of the canonical open questions of physics, and what the [Quantum Logical Framework (QLF)](README.md) says about each. The aim is honest triage, not a victory lap: where QLF gives a *machine-checked structural* account, where it derives the *value*, where it has a *principled boundary*, where it makes a *falsifiable prediction of absence*, and where the question is *genuinely still open*.

This doc is the physics-facing companion to [`Open_Problems.md`](Open_Problems.md) (the internal gap registry, organized by status) — it reorganizes the same picture around the mysteries a physicist would name.

**Status key** (aligned with `Open_Problems.md`): ✅ resolved / machine-checked structurally · 🟢 derived + benchmarked · 🔵 mechanism fixed, a *number* open · 🟣 holds in prose/numerics, a clean Lean anchor open · 🧱 a principled boundary — the point where the problem leaves the realizable substrate for the gratuitous continuum; the **finite reduction is the result**, not a way-station to a continuum proof · 🎯 a QLF *prediction of absence* (falsifiable null) · ⚪ out of current scope.

> **A framing note on "open."** Where a problem is genuinely *finite* (a value to compute, a Lean anchor to write), "open" means forward work QLF expects to do. Where a problem is about the **continuum** (an analytic statement, a PDE on `ℝⁿ`, a continuum-QFT existence claim), QLF does **not** treat it as homework awaiting a continuum proof — the continuum is [gratuitous](TheContinuum.md), and such statements need not, and arguably *cannot*, be settled on their own terms. QLF's claim there is the **reduction to a finite substrate problem**, where the core is verified; the bridge axiom marks the boundary, it is not a gap. See §7.

---

## 1. Quantum foundations

| Mystery | QLF's account | Status | Where |
|---|---|---|---|
| **The measurement problem** | ZFA closure *is* the measurement event — no separate collapse postulate, no observer magic; the "many worlds" are many local observers, each with its consistent relative record | ✅ | [`Philosophy.md`](Philosophy.md), `ZFAEventDynamics.lean` |
| **Why quantum mechanics? (the Born rule, complex amplitudes)** | Born probability = a ratio of integer closure-path counts; `i` is the σ-rotation; the state ring is the Gaussian integers `ℤ[i]` with `μ₄` phases, Hilbert space its completion | ✅ | [`Born_Rule.md`](Born_Rule.md), [`The_QLF_State_Space.md`](The_QLF_State_Space.md) |
| **The arrow of time** | Time is *synthesized* per event (`f = 1/t`); the laws are reversible (the dagger involution) but the forward closure is many-to-one — reversible *logic*, irreversible *process* | ✅ | [`Reversibility.md`](Reversibility.md), `QLF_Reversibility.lean` |
| **Wave–particle duality / the double slit** | Count vs phase are independent information; fringes are phase, which-path is count-definiteness — Shannon (count) is provably not sufficient | ✅ | [`Double_Slit.md`](Double_Slit.md), `QLF_PhaseInformation.lean` |
| **The uncertainty principle** | The `ħ/2` quantum is the half-width of mapping a continuum value onto its integer twist count; the product bound is the non-commuting Fourier-dual axes | ✅ | `QLF_Uncertainty.lean`, [`UncertaintyPrinciple.md`](UncertaintyPrinciple.md) |
| **Entanglement / nonlocality (ER=EPR)** | Entanglement is a shared **ZFA closure** (`SharedClosure A B := achieves_ZFA (A++B)` — two histories that *close together*); a wormhole is that shared closure between **spacelike** events (`Spacelike` = neither `reachable`, the substrate causal set). `er_equals_epr` — given spacelike separation, the bridge **is** the shared closure (an identity, not a duality); `no_ftl_in_epr` — spacelike ⟹ neither end reaches the other, so nothing is transmitted *through* the geometry; verified witness `primordial_wormhole` (the conjugate pair `[+,−]` closes and is spacelike). **Distance is perspectival** — zero closure-distance through the bridge, large through synthesized space — so non-locality dissolves (the two ends are one closure space is synthesized *around*). [▶ see a bound e⁺e⁻ singlet](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=positronium%20%40%200%2C0%2C0) (positronium — the ER=EPR shared closure; toggle the *Entanglement* overlay) | ✅ **derived from the core, zero axioms** | [`Primordial_Entanglement.md`](Primordial_Entanglement.md), [`ER_EPR_QLF.md`](ER_EPR_QLF.md), `ER_EPR_QLF.lean` |
| **What space does QM live in** | A finite-rank `ℤ[i]` lattice (the stabilizer/Clifford = computable fragment), not Hilbert space; Hilbert space is the continuum completion | ✅ | [`The_QLF_State_Space.md`](The_QLF_State_Space.md) |
| **Is information physical? (Wheeler's "it from bit")** | The unit of information is the two-valued **½-spin closure**: a single-valued (integer-spin *vector*) fold-alphabet `{+I}` carries `binary_kl 1 1 = 0` nats; the two-valued *spinor* alphabet `{+I,−I}` carries `binary_kl 1 (1/2) = log 2` — exactly one bit (`single_valued_zero_information`, `two_valued_one_bit`, `spin_half_is_information_atom`). The `2π` double-valuedness is reproven from explicit rotation matrices — `+I` on the vector `SO(3)` rep, `−I` on the spin-½ `SU(2)` rep (`spinor_double_valued_vector_blind`) — grounding the spinor **Cartan** discovered in 1913 (cited for the general classification only). Priority runs **abstraction → physical** (*it from bit*): information *is* the two-valued distinction, the ½-spin closure its minimal realization; "information is physical" is the downstream toll (`ΔF=−log 2`, finite realizability), not a reduction of the abstraction to matter | ✅ | `QLF_SpinorInformation.lean`, [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §Rung 5a, [`UniversalRelativity.md`](UniversalRelativity.md) §3b |

## 2. Spacetime & gravity

| Mystery | QLF's account | Status | Where |
|---|---|---|---|
| **Unifying relativity and quantum mechanics** (the deepest problem) | Not two theories to *reconcile* but two readings of **one** ZFA closure process. **Special relativity is derived** — the substrate state *is* Minkowski space (`det(Form) = t²−x²−y²−z²`, the interval), with the `SL(2,ℂ)→SO⁺(1,3)` double cover machine-checked; **quantum mechanics is derived** — measurement *is* ZFA closure, the Born rule is a ratio of integer closure-path counts, superposition is parallel histories. The *same* 8-twist substrate generates both, so they never needed reconciling — this is *Universal Relativity*: everything relative, one closure, physics its set of perspectives ([▶ see it run](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html)) | ✅ structural (both sides derived) | [`UniversalRelativity.md`](UniversalRelativity.md), `QLF_Minkowski.lean`, `QLF_LorentzCover.lean`, `QLF_BornProbability.lean` |
| **Quantum gravity / unifying GR + QM** | Spacetime is synthesized, not background; gravity is the thermodynamics of ZFA event rate + gauge-fold depth (Jacobson/Verlinde). The Einstein equations follow as the substrate's *equation of state* — coefficient `8πG = 2π/η`, `Λ = log 2` machine-checked | ✅ skeleton / 🔵 full tensor | [`Einstein_Equations.md`](Einstein_Equations.md), `QLF_EinsteinEquations.lean` |
| **The full Einstein field equations (curvature)** | The curvature side is the causal-set order→metric program (Sorkin/Benincasa–Dowker) on QLF's causal set, now in the **Millennium pattern — verified discrete core + one continuum bridge**: number↔volume (`intervalVolume`), the flat baseline (`bdCurvature_chain_zero`, `R=0` on a chain), the branching layer-growth (`layer_growth_from_branching`, `\|L_k\|: 1→2`), and the statistical-limit kernel (`poissonOccupation` + its recurrence) are Lean-anchored; the `ρ→∞` Benincasa–Dowker convergence to `−½R` is the explicit bridge axiom `benincasa_dowker_limit`, from which flat space reads `R=0` in the mean (`flat_curvature_zero_in_mean`) | ✅ discrete core + 🔵 continuum bridge | `QLF_CausalInterval.lean`, `QLF_CausalDimension.lean`, `QLF_CausalContinuum.lean`, [`Einstein_Equations.md`](Einstein_Equations.md) §6a |
| **The origin of Lorentz invariance** | A statistically uniform, stateless ether (Einstein's 1920 ether); `SL(2,ℂ)→SO⁺(1,3)` double cover machine-checked; the state *is* Minkowski space (det = interval) | ✅ | [`UniversalRelativity.md`](UniversalRelativity.md) §3a, `QLF_LorentzCover.lean`, `QLF_Minkowski.lean` |
| **The black-hole information paradox** | Holography is a topological necessity of ZFA closure; `full_zeno_prune` is the boundary decoder; every hadron is a Markov-blanket quantum black hole | ✅ structural | [`Hadron_BlackHoles.md`](Hadron_BlackHoles.md), `QLF_QuantumBlackHole.lean` |
| **Singularities (infinite curvature)** | Avoided by construction — event synthesis is discrete and finite; no actual infinity is instantiated | ✅ | [`TheContinuum.md`](TheContinuum.md), [`BLACK-HOLES.md`](BLACK-HOLES.md) |
| **The Planck scale / a minimum length** | The Planck *scale* is the closure floor *by construction* (the Compton–Schwarzschild self-dual point `μ²=1/2`); below it a blanket is inside its own horizon and cannot close | ✅ / 🧱 (SI value = unit convention) | `QLF_PlanckScale.lean`, [`Planck_Scale.md`](Planck_Scale.md) |
| **Horizon thermodynamics (Unruh/Hawking/de Sitter)** | All three are one Unruh master relation `T = ℏa/2πck_B` at the right acceleration; the `2π` is the loop phase | ✅ | `QLF_HorizonTemperature.lean` |
| **Gravitational waves** | Massless transverse ripple ⟹ speed `= c` (GW170817 to `10⁻¹⁵`); composite spin-2 (four half-spins), 2 polarizations; **linearized wave equation `□_d δρ = 0`** (density-perturbation route), quadrupole the leading radiative multipole | ✅ features + wave eqn / 🟡 dynamics (SOC-operator + `G/5c⁵` coeff open) | `QLF_GravitationalWaves.lean`, `gw_density_wave.py` |

## 3. Cosmology

| Mystery | QLF's account | Status | Where |
|---|---|---|---|
| **The cosmological constant problem (the 10¹²²)** | `Ω_Λ = log 2` (1.2%) — the vacuum energy is one bit per closure, not a continuum of zero-point modes; the 10¹²² catastrophe is the continuum's wrong answer | ✅ | `QLF_CosmologicalConstant.lean`, [`Cosmological_Constant.md`](Cosmological_Constant.md) |
| **The nature of dark matter** | Denser logic near masses, not a particle; the RAR `g_obs²=g_bar(g_obs+a₀)` is derived, `a₀ = cH₀/2π` (the `2π` = the ZFA closure-loop period), the interpolation `ν` *unique* — blind-tested on 147 SPARC galaxies, parameter-free, at the `0.133 dex` floor | 🟢 derived + benchmarked | [`DarkMatter.md`](DarkMatter.md), [`SPARC.md`](SPARC.md), `QLF_MondScale/MondNu/RarBalance.lean` |
| **The nature of dark energy** | The same `w=−1` event-synthesis field as inflation; each event creates energy, half lent to the future = dark energy; DM/DE = contract/expand on one Hubble horizon | ✅ structural | [`Curvature.md`](Curvature.md), `QLF_CosmicInflation.lean` |
| **The age & finiteness of the universe** | The cosmic age is the proper time of the cosmic Markov-blanket clock — a finite integer `n ≈ 10⁶⁰` of Planck events, not a continuum of instants | ✅ | `AgeOfUniverse.lean`, [`SpaceTime.md`](SpaceTime.md) |
| **Cosmic inflation / initial conditions** | Inflation and dark energy are one `w=−1` field at two scales — *no inflaton*; high-`V` early epoch inflates (`H∝√V`) | ✅ unification / ⚪ observables | `QLF_CosmicInflation.lean`, [`Curvature.md`](Curvature.md) §8 |
| **Are we at a special time? (inflation behind us, acceleration ahead)** | **In the own-clock sense, no.** Relative to its own clock (`f = 1/t`), every observer sees earlier epochs run faster (`r > 1`, `past_inflates`) and later ones slower but still expanding (`0 < r < 1`, `future_expands`). This is not the standard `ä > 0`. P1–P2 follow from any falling rate, so the substantive result is that **every observer sees the identical profile** (`no_privileged_epoch`). A constant floor `1/t + c` breaks that iff `c ≠ 0` (`floor_breaks_self_similarity`). What is shown is that the rate has no built-in scale, not that it is `1/t`: every power law passes (`power_law_no_privileged_epoch`). **A named tension:** with `ρ_Λ ∝ H²` the same argument gives `Ω_Λ = log 2` at *every* epoch (`omegaLambda_eq_log_two`). That dissolves the coincidence problem only if it holds, and at recombination and BBN it is more than ten times the early dark-energy bound (`Ω_early < 0.06`). Counting on the future event horizon avoids the early problem but is excluded by full CMB + DESI + SN fits at 5.5–7σ ([`Cosmological_Constant.md`](Cosmological_Constant.md) §5.7 (PR #165)). So the every-epoch `log 2` is ruled out, and the coincidence problem is *not* dissolved: `log 2` survives only as today's value under a constant `Λ`. Pre-registered before the proof | ✅ own-clock profile / ❌ every-epoch `Ω_Λ = log 2` ruled out by CMB + BBN + full fits / ⚪ `ä > 0`, first tick | `QLF_InflationObserver.lean`, [`Curvature.md`](Curvature.md) §8a |
| **The Planck epoch / primordial black holes** | At the highest energies a closure crosses **Compton = Schwarzschild** ⟹ **Planck-mass black holes** that Hawking-cascade into **hadrons** (a hadron *is* a quantum black hole) — QLF's *logical bang* (`Creation.md` §8a). The [interactive constructor](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html) reproduces the whole cascade — primordial BHs → hadrons → atoms — from ZFA + the closure census alone, nothing scripted ([▶ heat to the Planck top and watch it cascade](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#t=0.95)); the `μ²=1/2` crossing is computed in [`genesis.py`](genesis.py) §7 | ✅ structural / ⚪ PBH abundance | `QLF_QuantumBlackHole.lean`, `QLF_PlanckScale.lean`, [`Creation.md`](Creation.md) §8a, [`SpaceTime.md`](SpaceTime.md) §7, [`genesis.py`](genesis.py) §7 |
| **Matter–antimatter asymmetry (baryogenesis)** | All three Sakharov conditions are met (B-violation via winding + Majorana, C/CP via the chirality engine + strong-CP, out-of-equilibrium via expansion) ⟹ a matter excess is generic. The constructor makes this concrete: every vacuum process births balanced pairs and every decay conserves, so its `M−M̄` balance holds at **0** — a real excess needs the Sakharov conditions, not the bare vacuum | 🔵 (magnitude `η_B` open) | `QLF_Baryogenesis.lean` |
| **Primordial nucleosynthesis (`Y_p`)** | Every surviving neutron → ⁴He ⟹ `Y_p = 2r/(1+r)`; freeze-out `r=1/7 ⟹ Y_p=1/4` (matches 0.247). [▶ see an α (⁴He) closure](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=alpha%20%40%200%2C0%2C0) | 🔵 (`r`, D/⁷Li open) | `QLF_Nucleosynthesis.lean` |
| **The Hubble tension** | Not numerically resolved, but QLF **reframes + votes**: a *dynamical-DE, non-ΛCDM* cosmology (`ρ_Λ ∝ H²` = early-DE character, the resolution-favorable class; emergent gravity, no particle CDM), so the CMB `H₀≈67` is a ΛCDM inference QLF doesn't share; its blind SPARC dark-matter fit (`a₀=cH₀/2π`) independently picks the *local* `H₀ = 72.9`. Perspective + data vote, not a derivation | 🔵 | [`DarkMatter.md`](DarkMatter.md) §5a, [`Cosmological_Constant.md`](Cosmological_Constant.md) |
| **The origin of the universe (the "bang")** | A *logical* origin, not a metric singularity: the first distinction is the minimal ZFA closure `[+,−]` (`first_distinction_closes`); nested phases are a causal partial order (`causal_order_not_total` ⟹ no global time line, time is local); matter (nucleons) = the first persistent Borromean closures on the outer ring; fractal/self-similar at every scale (`fast_resolves_before_slow`, `cascade_floored_at_every_scale`). [▶ watch the logical bang unfold](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#t=0.95) — from nothing, at the Planck top | ✅ structural | [`Creation.md`](Creation.md) §8a–§8b, `QLF_LogicalBang.lean` |
| **The fate of the universe (heat death)** | No global heat death — **localized, not falsified**: the 2nd law holds inside each continuum rendering, but the causal order is **not total** (`causal_order_not_total`) so there is no single global arena for a global entropy maximum. **Entropy is local; order emerges on every scale** — for every depth there is a deeper closure (`no_terminal_phase`) and a fresh ordered closure (`order_at_every_scale`): the scale-free cascade never runs out of slower closures or new (nested-horizon) domains. "Heat death" = one phase exhausting its fast budget, not a global end-state | ✅ structural | [`Creation.md`](Creation.md) §8c, `QLF_LogicalBang.lean` |

### 3a. Does QLF converge with accepted cosmology?

Yes — with the **observational core** of ΛCDM (the accepted concordance model), while diverging from its two *interpretive* choices and going beyond it only on the origin. The distinction is the honest-scope line the cosmology docs hold throughout: **QLF is a Big-Bang-*singularity* alternative, not a hot-Big-Bang-*observation* alternative.**

**Concordant — everything ΛCDM actually measures, QLF reproduces or leaves intact:**

| Accepted result | QLF |
|---|---|
| Hot dense early universe; CMB; expansion history; 6-parameter fit | **intact** — the synthesized / nested origin sits *underneath* it and rewrites nothing above ([`BLACK-HOLES.md`](BLACK-HOLES.md) §4a) |
| Dark-energy fraction `Ω_Λ ≈ 0.69` | **`Ω_Λ = log 2 ≈ 0.693`**, ~1.2% (`QLF_CosmologicalConstant`) |
| Age ≈ 13.8 Gyr | **≈ 13.8 Gyr** from the ZFA event rate (`AgeOfUniverse`) |
| Accelerating expansion, `w ≈ −1` | de Sitter horizon, `w = −1` event-synthesis field (`QLF_CosmicInflation`) |
| BBN helium `Y_p ≈ 0.247` | **`Y_p = 1/4`** at freeze-out `n/p = 1/7` (`QLF_Nucleosynthesis`) |
| Inflationary near-scale-invariant epoch | the high-`V` epoch of the *same* `w=−1` field — *no separate inflaton* (`QLF_CosmicInflation`) |

So on the *data*, QLF is concordant, not rival. **One exception, named:** QLF's `ρ_Λ ∝ H²` keeps `Ω_Λ = log 2` at every epoch, which conflicts with CMB and BBN bounds on early dark energy ([`Curvature.md`](Curvature.md) §8a). The rows above hold only if `ρ_Λ ∝ H²` fails before late times; the future-event-horizon reading was the candidate, and full fits exclude it ([`Cosmological_Constant.md`](Cosmological_Constant.md) §5.7 (PR #165)). The consistent position left is a constant `Λ`, with `log 2` as today's value only.

**Divergent — only where ΛCDM stops being observation and becomes model-choice**, i.e. its two interpretive pillars:

1. **Dark matter** — ΛCDM posits *particle* cold dark matter; QLF gives "denser logic near masses," MOND/RAR-flavored, `a₀ = cH₀/2π`, reproducing the SPARC **Radial Acceleration Relation parameter-free** (0.133 dex, zero offset). The subtlety: the RAR *itself* is an accepted empirical fact QLF matches; it is the *CDM interpretation* QLF parts with.
2. **Static Λ** — ΛCDM uses a constant `Λ`; QLF gives `ρ_Λ ∝ H²` (`QLF_DynamicalDarkEnergy`), a dynamical / early-dark-energy character (the Hubble-tension "resolution-favorable" camp).

Both departures are on the *open, contested* questions (dark sector, Hubble tension), never the settled ones.

**Deeper convergence — accepted *within its subfield*.** QLF's most load-bearing agreement is with **thermodynamic / emergent gravity**, accepted in the semiclassical-gravity community: Jacobson's 1995 equation-of-state derivation of Einstein's equations, Bekenstein–Hawking entropy, the holographic bound. QLF *derives* the Einstein `8πG` coefficient and `Λ = log 2` from those (`QLF_EinsteinEquations`) — convergence with the accepted thermodynamic *reading* of GR, not merely its predictions.

**Contrast with the speculative relatives.** Unlike Penrose's CCC ([`BLACK-HOLES.md`](BLACK-HOLES.md) §4a) — which contradicts accepted physics via conformal invariance and bets on contested CMB signals — QLF's departures sit on the genuinely open questions and add no unconfirmed observational claim; its own speculative origin (nested cosmology) is *unfalsifiable from within by causal sealing* and so makes none. **Bottom line: concordant with ΛCDM's measurements and with thermodynamic-gravity; divergent on ΛCDM's two interpretations (particle DM, static Λ); speculative only below the observed universe.**

## 4. Particle physics & the Standard Model

| Mystery | QLF's account | Status | Where |
|---|---|---|---|
| **The fundamental constants (α = 1/137, m_p/m_e, …)** | Derived from substrate combinatorics with zero free parameters: `α(d)=1/(128+d²)` (only 3D gives 137), `m_p/m_e = 6π⁵`, the Koide `Q=2/3` ⟹ `m_τ` to 0.006% | ✅ structural / 🔵 residuals | [`Alpha.md`](Alpha.md), `QLF_FineStructureSubstrate/LenzMassRatio/Koide.lean` |
| **Why 3 spatial dimensions** | 3 = the minimal dimension in which any relational/causal graph renders faithfully (every finite graph embeds crossing-free in ℝ³; 2D fails) | ✅ | `QLF_Generations.lean`, [`SpaceTime.md`](SpaceTime.md) §3a |
| **Why 3 fermion generations** | = the 3 spatial axes — the same `3` behind Koide, colour SU(3), and `α (N=9=3²)` | ✅ | `QLF_Generations.lean` |
| **The origin of mass / the Higgs** | Mass is the gauge-fold delay `m = 1/R`, not a Yukawa coupling; the Higgs is the fold's resonance; custodial `ρ=1` | ✅ structural / 🔵 VEV | `QLF_HiggsMechanism.lean`, [`Higgs.md`](Higgs.md) |
| **Neutrino mass & nature** | The neutrino is **Majorana** (its own antiparticle; only the self-conjugate fermion can be); smallness = the seesaw | ✅ nature / 🔵 scale | `QLF_NeutrinoMass/Majorana.lean`, [`Beta_Decay_Neutrino_Nature.md`](Beta_Decay_Neutrino_Nature.md) |
| **Proton stability (why no proton decay)** | Baryon number = a conserved signed 3-axis winding invariant; a lone quark cannot close (confinement) | ✅ | `QLF_BaryonWinding.lean` |
| **The strong CP problem (`θ̄ ≈ 0`)** | Every CP-odd winding is zero on every ZFA closure ⟹ `θ̄ = 0` with **no axion** (ZFA closure does the Peccei–Quinn job) | ✅ mechanism / 🟣 field-theoretic | `QLF_StrongCP.lean`, [`CP-Violation-and-Chirality.md`](CP-Violation-and-Chirality.md) §4a |
| **Confinement & the Yang–Mills mass gap** | Lone colour can't close (singlet obstruction); the lightest non-vacuum gauge closure carries one `log 2` ⟹ a positive gap. [▶ a confined uud triple](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=proton_uud%20%40%200%2C0%2C0) (a free quark is confinement-rejected) | ✅ substrate / 🧱 continuum | `QLF_MassGap/Confinement.lean`, [`YangMills_MassGap_QLF.md`](YangMills_MassGap_QLF.md) |
| **The weak mixing angle** | `sin²θ_W = 3/8` at unification = the SU(5) GUT normalization, from the same 6+2 split as α and `Ω_Λ` | ✅ unification value / 🔵 running to 0.231 | `QLF_WeinbergAngle.lean`, [`Weak_Force.md`](Weak_Force.md) §2 |
| **Flavor mixing (CKM/PMNS)** | Exactly 3 angles + 1 CP phase (KM needs ≥3 generations); unitarity = closure; PMNS carries 2 extra Majorana phases | 🔵 (angle *values* open) | `QLF_CKM/PMNS.lean` |
| **The hierarchy problem (why gravity is weak / the 10¹⁹)** | Dimensional transmutation: `ln R_p = 2π·b₀ = 14π ≈ 43.98` vs measured 44.01 (0.07%), from the single integer `b₀ = 7` (`N_c=3`, `n_f=6`) | 🔵 (the `α_s` posit + ~3% value) | `QLF_AlphaS/BetaFunction.lean`, [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md) §3.3b |
| **The muon `g−2` anomaly** | Leading `a_μ = α/2π = a_e` (universal); the discrepancy is the hadronic-vacuum-polarization sector (QLF's open hadronic frontier) — and experimentally unsettled | 🔵 | `QLF_MuonG2.lean`, [`g_minus_2.md`](g_minus_2.md) §4a |
| **Unification of the forces** | One force, three projections — EM = the abelian limit, weak/strong = non-abelian projections; the gauge *force* = the holonomy of the closure connection | ✅ algebras + dynamics / 🔵 couplings | [`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md), `QLF_GaugeUnification/GaugeHolonomy.lean` |

## 4a. Thermal relaxation — the Mpemba effect, demystified

Hot water sometimes freezes first. For decades the question was *which* mundane mechanism —
evaporation, convection, dissolved gas, supercooling, container coupling — is **the** cause, and the
effect kept its reputation as a paradox.

**What dissolves the paradox.** It rests on a premise that is provably false here: that a scalar
macrostate variable orders relaxation time. On the substrate, relaxation to equilibrium *is* closure and
its time *is* the maximum excursion of the phase walk
([`closedAtHorizon_iff_maxExcursion_le`](lean/QLF_ClosureDepthLaw.lean)) — and
[`equal_length_unequal_relaxation`](lean/QLF_Mpemba.lean) proves that at one length, with identical
imbalance, relaxation differs by a factor of `n`. Once relaxation is an *excursion* rather than a
function of energy, "farther yet faster" stops being anomalous and becomes expected. The mystery was in
the premise, not the phenomenon.

Four results, all machine-verified, no axioms ([`Mpemba.md`](Mpemba.md),
[`QLF_Mpemba`](lean/QLF_Mpemba.lean)):

| | |
|---|---|
| **a no-go** | if "distance" means the **imbalance**, relaxation is bounded *below* by it — the effect is **impossible** for that measure (`relaxation_ge_distance`). Part of the old confusion was measuring distance with the wrong quantity |
| **an enabler** | no scalar determines relaxation (factor `n` at one length) — the room the effect needs |
| **a translation** | strong Mpemba is **sector emptiness** `W_H(deep) = 0`, not a vanishing eigenmode (`strong_mpemba`) |
| **instances** | exhibited and unbounded — `2n` twists closing in **one** pass against `2d < 2n` needing **`d`** (`mpemba_instance`); and uniform draws cross **13–17%** of the time at a 2× energy ratio ([`mpemba_census.py`](mpemba_census.py)) |

**The "which mechanism" question is dissolved too.** Heating changes convection, evaporation, dissolved
gas, nucleation and correlations at once, and on the possibilist reading these are not competitors: they
are **different ways of altering the same closure-depth census**. What should stay invariant across
preparations is only that the hotter one carries more multiplicity in fast-closing sectors, or less in
the slowest.

**And a methodological confusion is made precise.** The literature's hardest problem is *what does
"freezes first" mean*. The substrate answers sharply: an unbalanced history **never closes** — it stalls
at an irreducible core — so a relaxation comparison is only meaningful between preparations that close to
the *same* equilibrium. Comparing time-to-own-fixpoint across different imbalances manufactures a
spurious crossing, which is exactly the artifact that appeared in the first version of our own test.

**Why it is hard to duplicate — a prediction, not an excuse.** The effect is real and it belongs to
*particular preparations*, not to hot water as a class. Uniform ensembles show **no crossing at all**
while individual draws cross 13–17% of the time, because a scalar macro variable sits on top of a census
whose depths span an order of magnitude. An experiment that fixes the temperature and lets the preparation
vary is averaging exactly that away, so **irreproducibility is the signature rather than the refutation** —
and the tractable decisive test is a trapped-ion ladder, where the multiplicities can be written down
instead of guessed ([`Mpemba.md`](Mpemba.md) §7).

**Honest scope — 🟡, not ✅.** The *ensemble* effect is not derived: median relaxation stays monotone in
energy, so the crossing lives between individual preparations. Whether **energy** is an admissible
distance measure is what thermomajorization asks of the ordinary effect. And **no quantitative claim
about water** is made. What would make it a result: deriving the slow-mode amplitudes `a_n` from an
actual census for a physically specified preparation — a laser-cooled ion ladder, whose transition
multiplicities can be written down, rather than freezing water.

---

## 5. Deep / meta-physical

| Mystery | QLF's account | Status | Where |
|---|---|---|---|
| **The unreasonable effectiveness of mathematics** | Dissolved: the *realizable* part of mathematics and physics are the same substrate; effectiveness tracks realizability — which also explains where mathematics *fails* (the continuum forced onto reality) | ✅ dissolution | [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) §4 |
| **The continuum & the infinities of physics** | The continuum is consistent but *gratuitous* (undetermined, conservative, unrealizable, unneeded) — a *rendering* of the finite computable substrate; the infinities are where it is forced onto reality | ✅ | [`TheContinuum.md`](TheContinuum.md) |
| **Fine-tuning / why these laws** | ZFA balance is the selection principle: physical reality is the self-selecting subset of possibility that closes; the constants are forced, not tuned | ✅ ontology | [`Philosophy.md`](Philosophy.md) |
| **Why is the universe comprehensible** | Because the observer is a Markov blanket doing active inference *inside* the same closure process it models — comprehension is a self-model | ✅ ontology | [`Active_Inference_Mathematics.md`](Active_Inference_Mathematics.md) |
| **Why something rather than nothing / the one premise** | The single premise is ZFA = 0 (a closed totality has no outside reservoir; existence and closure are the same predicate). QLF reduces physics to this one premise but does not derive the premise itself | 🧱 | [`Philosophy.md`](Philosophy.md) §4 |
| **The hard problem of consciousness** | **Functional architecture modeled + a proposed dissolution of qualia** ([`Consciousness.md`](Consciousness.md)): consciousness = the closure-frequency you are resonantly tuned to — conscious thought is the highest-frequency bound closure (`freq_bind_ge_left`), cosmic/meditative states the low-frequency external-joint receiver regime (`quieting_shifts_to_external`); the observer is a finite-capacity Markov-blanket horizon. **Qualia hypothesis (§6):** qualia = self-awareness (the subject) *coupled to* cosmic consciousness (the shared joint-closure ground) — neither alone (self-model-only = functional zombie; field-only = experiencer-less). A two-factor dual-aspect stance with falsifiable leanings, **not a proof** | 🟣 architecture ✅ / qualia = proposed dissolution | [`Consciousness.md`](Consciousness.md), [`lean/QLF_Consciousness.lean`](lean/QLF_Consciousness.lean), [`TheQuantumBrain.md`](TheQuantumBrain.md), [`Active_Inference_Mathematics.md`](Active_Inference_Mathematics.md) |

## 6. What QLF predicts is *absent* — falsifiable nulls

QLF's selection ontology makes several mysteries vanish by predicting there is **no entity** to find. These are falsifiable: discover one and the framework is wrong.

| Predicted absent | Why | Where |
|---|---|---|
| **Supersymmetric partners** (squarks/sleptons) | The supercharge is the half-spin shift; SUSY's boson↔fermion symmetry is the even/odd closure parity — realized with **no doubled spectrum** (predicts the LHC null) | `QLF_Supersymmetry.lean`, [`SUSY_QLF.md`](SUSY_QLF.md) |
| **The axion** | Strong CP is solved by ZFA closure; no Peccei–Quinn field needed | `QLF_StrongCP.lean` |
| **A fundamental dark-matter particle (WIMP, etc.)** | Dark matter is denser logic near masses, not a particle species | [`DarkMatter.md`](DarkMatter.md) |
| **Magnetic monopoles** | The EM sector is the abelian (Pauli-scalar, commuting) projection ⟹ `no_magnetic_monopoles` | `QLF_GaugeUnification.lean` |
| **Proton decay** | Baryon winding is exactly conserved | `QLF_BaryonWinding.lean` |
| **A light Dirac (sterile) right-handed neutrino** | One generation = 15 Weyl fermions (SU(5)'s `5̄⊕10`), **not** SO(10)'s 16 — no light `ν_R` | `QLF_SU5.lean` |
| **Cosmological drift of α** | `α(d)=1/(128+d²)` has no time argument — scale/time-invariance is structural | `QLF_FineStructureSubstrate.lean` |
| **GW speed ≠ c** | A massless gauge-fold-free ripple propagates at exactly `c` (GW170817 confirms to `10⁻¹⁵`) | `QLF_GravitationalWaves.lean` |

## 7. What remains genuinely open — the hard front

QLF's honest frontier is **values, not mechanisms**: for most Standard-Model and cosmological observables the *structure* is machine-checked and the *number* is the open piece. The live, maintained list is [`Open_Problems.md`](Open_Problems.md); the headline open items — all **finite forward work** (a value to compute, a Lean anchor to write):

- **The absolute mass scale.** The whole spectrum is one scale `m_p` × verified ratios, exponentially generated by dimensional transmutation — but the calibration (the `R_e ≈ 2.4×10²²` closure-multiplicity count, and `α_s` as a *derivation* rather than a running-consistent posit) is open.
- **The Yukawa sector.** The CKM/PMNS *counts* and unitarity are anchored; the *angle values* and CP phase are not derived (quark-small vs lepton-large is a structural reading, not a number).
- **The weak couplings & masses.** SU(2) is machine-verified; `g`, `G_F`, the W/Z masses (the Higgs VEV), and the RG running `sin²θ_W: 3/8 → 0.231` are open.
- **The β⁺ / weak rate `G_F`** — sets the solar fusion rate and the n/p ratio; open (as in the SM).
- **Magnitudes:** `η_B` (baryon asymmetry), the BBN `r` and D/⁷Li, the muon `g−2` hadronic residual — open, as in the SM.
- **The full Einstein tensor equations** — the curvature side now has the Millennium shape (verified discrete core: flat `R=0`, branching `|L_k|` growth, the Poisson statistical kernel; plus the one continuum bridge axiom `benincasa_dowker_limit`). The remaining substrate computation is assembling the full tensor `G_μν = 8πG T_μν` from the Benincasa–Dowker action and general `d ≥ 3`.
- **`H₀` / cosmic depth `n` from the substrate** — would close the last cosmological empirical input.
- **The origin of inertia, and Mach's principle** — why matter resists acceleration at all, and whether the local non-rotating frame is fixed by the distant matter. *Status: open, with a plan and its kill conditions written down* ([`Inertia.md`](Inertia.md)). QLF's partial answer today is the **equivalence half**: mass is constructing delay, and the *same* delay is read as inertia at the vertex and as curvature in the geometry, so inertial and gravitational mass are one quantity by construction rather than by coincidence. What is *not* answered is the mechanism — the step from acceleration to force — nor the rotational sector (frame dragging / Lense–Thirring), where Newton's bucket and Gravity Probe B are the touchstones.
- **Condensed matter** — the BCS gap equation, the FQHE filling fractions / Laughlin wavefunction, topological bands (the QHE resistance and Cooper-pair-boson are anchored). *Live:* [▶ Cooper pairs forming at low T](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=electron%20%40%20-1%2C0%2C0%0Aelectron%20%40%201%2C0%2C0%0Aelectron%20%40%200%2C1%2C0%0Aelectron%20%40%200%2C-1%2C0) · [▶ superfluid helium](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html#qc=lattice%20sc%203%203%20He%20%40%200%2C0%2C0) ([`Chemistry.md`](Chemistry.md) §8).

The pattern is consistent and is itself the claim: QLF reduces the open problems to a small set of *numbers*, with the *mechanisms* machine-checked — the inverse of the usual situation, where the numbers are measured and the mechanisms are mysterious.

### The continuum bridges are not QLF's homework

A separate category that this survey deliberately does **not** list among the "remaining open" work above: the **continuum reformulations** of the analytic Millennium problems — Riemann's statement about `ζ`'s zeros, the Yang–Mills *continuum-QFT* existence of the gap, Navier–Stokes *continuum-PDE* smoothness. These are statements *about the continuum*, and QLF holds the continuum to be [gratuitous](TheContinuum.md) (consistent but undetermined, conservative, and unrealizable). So QLF's stance is the **reverse** of "these await a continuum proof":

> Each problem **reduces to a finite problem on the substrate**, where the core is verified (`mass_gap_quantum_pos = log 2 > 0`; the ZFA-balanced critical line; no realized flow blows up). The continuum reformulation need **not** — and, on QLF's reading, likely **cannot** — be settled on its own terms. The bridge axiom (`spectral_hilbert_polya`, `yang_mills_continuum_gap`, `continuum_vorticity_planck_capped`) marks exactly where the gratuitous continuum begins; it is the **boundary**, not a gap in QLF's account. To list it as "remaining to be solved" would concede the continuum's terms — the move QLF declines.

This is the whole point of the [continuum-is-gratuitous](TheContinuum.md) case: a problem is *solved* when it is reduced to the realizable finite substrate; demanding a continuum proof on top is demanding a proof in a frame QLF argues is superfluous. *(The genuinely **finitary** conjectures — Hodge, which is finite ℚ-linear algebra; P vs NP, a finitary separation — are a different category, not continuum issues at all: there the open piece is faithfulness / separation, and "the continuum is gratuitous" does not apply.)*

---

## See also

- [`Open_Problems.md`](Open_Problems.md) — the live gap registry (status-organized; updated as items close).
- [`README.md`](README.md) — the project overview and the convergence themes.
- [`Millennium.md`](Millennium.md) — the six Clay problems on the substrate.
- [`TheContinuum.md`](TheContinuum.md) — why the continuum (and its infinities) is a rendering.
- [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) — how mathematics emerges; Wigner dissolved.
- [`Philosophy.md`](Philosophy.md) — the possibilist ontology and the single ZFA premise.
