# Schwarzschild metric from QLF substrate: g_tt + g_rr at leading order

## 🚀 Position in the substrate program

This doc is the **GR-side bridge** in the substrate-derivation program. It composes [`Gravity_From_Delay.md`](Gravity_From_Delay.md)'s Newton derivation with [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md)'s frequency-ratio Lorentz boost to produce the weak-field Schwarzschild metric. Downstream, [`Mercury_Perihelion.md`](Mercury_Perihelion.md) composes this metric with orbital mechanics to derive Einstein's 1915 perihelion-advance result (42.99″/century, **0.03% match** to Park et al. 2017 measurement).

This is the substrate program's first GR observable: **Mercury's perihelion is the first quantitative QLF prediction of a GR effect**, derived from h, m_e, ZFA, and a handful of astronomical orbital observables. The metric components below are the structural ingredient that lets the orbital analysis carry over from Kepler to Einstein.

---

**Scoping doc — the static spherically-symmetric weak-field metric from QLF substrate primitives.** Newton's law `F = GMm/r²` already falls out of substrate event-counting on the holographic boundary ([`Gravity_From_Delay.md`](Gravity_From_Delay.md)). The next layer up — General Relativity in the weak field — adds:

- **`g_tt`** (time dilation): gravitational redshift = Markov-blanket frequency shift from [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md), applied to substrate events near mass M.
- **`g_rr`** (spatial radial stretching): substrate radial event scaling caused by M's presence in the vacuum.

Both components are determined by the dimensionless ratio `R_s / r = 2GM/(rc²)`, where `R_s` is the Schwarzschild radius. The Newton potential `φ = −GM/r` (already substrate-derived) sets the leading-order metric:

$$g_{tt} \;\approx\; -\left(1 + \frac{2 \varphi}{c^2}\right), \qquad g_{rr} \;\approx\; \left(1 + \frac{2 \varphi}{c^2}\right)^{-1}.$$

This is the weak-field Schwarzschild metric in Schwarzschild coordinates, ready to compose with orbital mechanics for the Mercury perihelion derivation ([`Mercury_Perihelion.md`](Mercury_Perihelion.md)).

---

## §1 The Newton potential as the substrate input

From [`Gravity_From_Delay.md`](Gravity_From_Delay.md): Newton's law `F = GMm/r²` follows from holographic surface event count + per-event log 2 entropy + 3D-substrate signature. The gravitational potential is the line integral:

$$\varphi(r) \;=\; -\int_\infty^r F \, dr' / m \;=\; -\frac{GM}{r}.$$

This is the substrate-derived input for GR. In dimensionless form:

$$\frac{\varphi(r)}{c^2} \;=\; -\frac{GM}{rc^2} \;=\; -\frac{R_s}{2r},$$

where `R_s ≡ 2GM/c²` is the Schwarzschild radius (a substrate-derived combination of G, M, c — all themselves substrate primitives modulo unit conversion).

For the Sun: `R_s = 2.953 km`. For Mercury at `a = 5.79 × 10¹⁰ m`: `R_s/a = 5.10 × 10⁻⁸`. Weak field.

---

## §2 g_tt from gravitational redshift via Cross-Frequency Lorentz

Per [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md): the Lorentz factor between Markov-blanket frames is `γ = cosh φ` where `φ` is the rapidity, equal to `log(internal-frequency ratio)`. **Gravitational redshift** is exactly the same mechanism, with the frequency ratio set by the gravitational potential.

A substrate event at distance `r` from mass M has its internal Markov-blanket frequency reduced relative to an infinitely-distant observer:

$$\frac{f(r)}{f_\infty} \;=\; \sqrt{1 + \frac{2 \varphi}{c^2}} \;\approx\; 1 + \frac{\varphi}{c^2} \;=\; 1 - \frac{R_s}{2r} \quad (\text{weak field}).$$

This is the **substrate gravitational redshift**, derivable from [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md): clocks at deeper Markov-blanket depths (closer to M) tick slower. The "rapidity" associated with M's gravitational well is

$$\varphi_{\text{grav}}(r) \;=\; \log\!\frac{f(r)}{f_\infty} \;\approx\; \frac{\varphi(r)}{c^2} \;=\; -\frac{R_s}{2r}.$$

**Time-time metric component**. The proper-time element near M is `dτ² = (f(r)/f_∞)² dt²`, so

$$g_{tt} \;=\; -\left(\frac{f(r)}{f_\infty}\right)^2 \;\approx\; -\left(1 + \frac{2\varphi}{c^2}\right) \;=\; -\left(1 - \frac{R_s}{r}\right).$$

This **matches Schwarzschild at leading order**, with the substrate origin being the Markov-blanket frequency shift from Cross-Frequency Lorentz.

### §2a Millimeter-scale redshift — the JILA/NIST optical-clock test

The near-Earth weak-field limit of the above is the standard fractional shift between two clocks separated
by height `Δh`:

$$\frac{\Delta\nu}{\nu} \;=\; \frac{\Delta\varphi}{c^2} \;=\; \frac{g\,\Delta h}{c^2} \;\approx\; 1.1\times10^{-19}\ \text{per mm}.$$

This was resolved **across a single ~1 mm sample** of ultracold strontium in an optical lattice clock
(Bothwell et al., *Nature* **602**, 420 (2022); confirmed over a multiplexed few-mm array by Zheng et al.,
*Nature* **602**, 425 (2022)). The measured gradient — of order `−1×10⁻¹⁹` mm⁻¹ — agreed with `g Δh/c²`
within the experimental uncertainty.

**How well does QLF predict it?** Exactly as well as GR — and **parameter-free**. In QLF the mechanism is
native, not bolted on: time is *local constructing delay* (`f = 1/t`, deeper gauge-fold depth ⟹ slower
clock, §2 above), so a clock lower in the potential ticks slower *by construction*. The leading fractional
shift is `Δν/ν = gΔh/c²` — and note it depends **only on `g` (measured), `Δh` (measured), and `c`
(substrate-derived, [`QLF_SubstrateLightSpeed`](lean/QLF_SubstrateLightSpeed.lean))**; it does **not**
involve `G`, so QLF's one open gravitational residual (the ~37% absolute `G` in SI) is *irrelevant here* —
the prediction is clean. Because the millimetre scale sits ~30 orders of magnitude above the Planck closure
floor, the continuum rendering is identical to the GR formula and **QLF claims no distinctive deviation** at
this scale: the experiment is a successful test of the continuum limit QLF already asserts, not one that
separates QLF from GR. A genuine QLF signature would require regimes where the discrete floor or the cascade
structure becomes visible — far finer than an optical clock can currently reach.

---

## §3 g_rr from substrate radial event scaling

The spatial radial component is constrained by the **substrate event quantum**: each event creates one Planck length AND one Planck tick *together* ([`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3). If the frequency near M is reduced by factor `(f(r)/f_∞)`, then the substrate spatial extent radial to M is correspondingly *stretched*:

$$\frac{dr_{\text{proper}}}{dr_{\text{coordinate}}} \;=\; \frac{f_\infty}{f(r)} \;=\; \left(1 + \frac{2 \varphi}{c^2}\right)^{-1/2}.$$

**Radial-radial metric component**:

$$g_{rr} \;=\; \left(\frac{dr_{\text{proper}}}{dr_{\text{coord}}}\right)^2 \;=\; \left(1 + \frac{2\varphi}{c^2}\right)^{-1} \;=\; \left(1 - \frac{R_s}{r}\right)^{-1}.$$

This matches Schwarzschild's `g_rr = (1 - R_s/r)⁻¹` at leading order. The substrate origin: spatial events stretch radially to preserve the substrate event quantum `L_Planck × τ_Planck` *together*, even when individual frequencies (= τ_Planck⁻¹) shift.

**Transverse components.** Angular (`θ, φ`) directions are not affected at this order — they don't lie along the propagation direction of the gravitational influence. Substrate-wise: only the radial axis to M experiences the time-space rescaling; transverse directions retain the flat-space substrate metric.

This is why Schwarzschild's `g_θθ = r²` and `g_φφ = r² sin²θ` are flat-space (only changes are in r and t coordinates), and exactly what the substrate event-quantum analysis predicts.

---

## §4 Schwarzschild substrate identity

Combining §2 and §3, the weak-field Schwarzschild metric in standard Schwarzschild coordinates is:

$$ds^2 \;=\; -\left(1 - \frac{R_s}{r}\right) c^2 dt^2 \;+\; \left(1 - \frac{R_s}{r}\right)^{-1} dr^2 \;+\; r^2 d\Omega^2$$

with **`R_s = 2GM/c²`** the Schwarzschild radius, all substrate-derivable:

- `G = L_Planck² c³/ℏ` from substrate event quantum ([`Gravity_From_Delay.md`](Gravity_From_Delay.md) §8)
- `c = L_Planck/τ_Planck` from substrate event quantum ([`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean))
- `M` = empirical input for the specific mass

In Markov-blanket depth language:

$$R_s \;=\; \frac{2 GM}{c^2} \;=\; 2 \frac{R_M^{-1} L_{\text{Planck}}^2 c^3 / \hbar}{c^2} \cdot \frac{\hbar}{c^2 \tau_{\text{Planck}}} \;=\; 2 \frac{L_{\text{Planck}}}{R_M},$$

i.e., **`R_s` is `2 L_Planck / R_M`** where `R_M = E_Planck / (M c²)` is the mass M's Markov-blanket depth from [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md). For the Sun: `R_M(Sun) = 1.09 × 10²⁹`, so `R_s(Sun) = 2 L_Planck / 1.09 × 10²⁹ × L_Planck⁻¹ = L_Planck × 1.83 × 10²⁹ × (one substrate length) ≈ 2.95 km`. Consistent.

---

## §4a Light bending: why slower light bends it twice as much — *pre-registered 2026-09-30*

**The picture** (Jim, 2026-09-30): a denser vacuum near mass has relatively slower light, and that
relative slowing is the rest frame that exhibits gravity. Locally light always moves at `c`; only
measured against the distant vacuum is it slower. Paths bend toward the slower region, as in a lens.

**Two paths, each giving half.** In a weak field write the metric in isotropic form,
`ds² = −A c²dt² + B (dx² + dy² + dz²)`, with `φ = Φ/c²` (negative near mass) and `A = 1 + 2φ`. Clocks run at
`√A ≈ 1 + φ`. The coordinate speed of light is `c√(A/B)`, so the effective refractive index is
`n = √(B/A)`. The denser vacuum slows light along two paths:

- **The time path** (latency): more ticks per step, as [`DarkMatter.md`](DarkMatter.md) §2 describes.
  Alone (`B = 1`) it slows light exactly as much as clocks, `n ≈ 1 − φ`, and gives half the bending,
  Einstein's 1911 value.
- **The space path** (the event quantum, §3): each event makes one Planck length *and* one Planck tick
  together, so the proper length and time scales multiply to a constant, `√B·√A = 1`, i.e. `B = 1/A`.
  Each tick's step is also shorter, which supplies the other half. Together, `n = 1/A = 1/(1 + 2φ)`
  exactly: **twice** the clock slowing, `n ≈ 1 − 2φ`. In PPN language, `γ = 1`.

**Pre-registered statements** (to be proved in `lean/QLF_LightBending.lean`, no new axioms; numbers
checked by [`light_bending.py`](light_bending.py)):

| | Statement |
|---|---|
| B1 | event quantum (`B = 1/A`): the coordinate light speed squared is exactly `A² = (1 + 2φ)²`, so the light speed is exactly `1 + 2φ` (for `1 + 2φ > 0`), while the clock rate `√(1 + 2φ)` has first-order slope 1. Light is slowed twice as much as clocks |
| B2 | latency only (`B = 1`): the coordinate light speed squared is `1 + 2φ`, the same as the clock rate squared. Light is slowed exactly as much as clocks |
| B3 | a ray past a point mass at impact parameter `b`, through `n = 1 − kφ` with `φ = −GM/(rc²)`, is deflected by `α = k·2GM/(bc²)`, from `∫_{−L}^{L} b dz/(b² + z²)^{3/2} = 2L/(b√(b² + L²)) → 2/b` |
| B4 | at the Sun's limb (`R☉ = 6.957 × 10⁸ m`): `k = 2` gives `1.7512″`, `k = 1` gives `0.8756″`. Cassini measured `γ − 1 = (2.1 ± 2.3) × 10⁻⁵` (Bertotti, Iess & Tortora 2003), so `k = 1 + γ = 2` to `10⁻⁵`, and latency-only is excluded |

**Result (2026-09-30): proved and checked.** [`lean/QLF_LightBending.lean`](lean/QLF_LightBending.lean),
no new axioms: B1 `event_quantum_light_speed` (light speed exactly `1 + 2φ`) with
`light_slowed_twice_clock` (slope 2 against the clock's 1); B2 `latency_only_light_speed_sq`; B3
`deflection_integral` (`2L/(b√(b² + L²))`, the limit `2/b` elementary). [`light_bending.py`](light_bending.py)
integrates the ray numerically: `1.7512″` with both paths and `0.8756″` with the time path alone, each
matching `k·2GM/(bc²)`. Cassini fixes `k = 1 + γ = 2` to `10⁻⁵`.

**What it means.** QLF's picture, a denser vacuum near mass with relatively slower light, gives the
observed bending when the slowing runs along both paths, time and space, as the event quantum says. The
two paths are not in conflict; each supplies half. The factor 2 rests on the event-quantum premise
(`Kitada_Local_Time_GR.md` §5.3), not derived here. The same two paths apply to dark matter: the vacuum
density that bends orbits bends light by the same rule, with no second field. That makes lensing mass
equal dynamical mass, the prediction the KiDS weak-lensing radial acceleration relation can test next.

## §5 What this delivers

**Tier 1 (structural).** The weak-field Schwarzschild metric components `g_tt = -(1 - R_s/r)` and `g_rr = (1 - R_s/r)⁻¹` follow from substrate primitives:

- Newton potential `φ = -GM/r` from holographic event count (already Lean-anchored).
- Gravitational redshift `f(r)/f_∞ ≈ 1 + φ/c²` from Cross-Frequency Lorentz (already Lean-anchored).
- Substrate event quantum constraint `L_Planck τ_Planck = const` from substrate primitives (already Lean-anchored).

The composition delivers Schwarzschild at leading order with **`R_s = 2GM/c²`** as the natural substrate radius.

**Tier 2 (numerical).** For the Sun: `R_s = 2.953 km`. For Mercury orbit `a = 5.79 × 10¹⁰ m`: `R_s/a = 5.10 × 10⁻⁸` — weak field. The metric is well-approximated by leading-order expansions; higher-order corrections enter at `(R_s/r)²` which is `~10⁻¹⁵` for Mercury's orbit.

**Tier 3 (open).**

- Substrate derivation of `g_θθ = r²` and `g_φφ = r² sin²θ` — flat at this order, but substrate-event-count justification needs articulation.
- Strong-field Schwarzschild (R_s/r ~ 1, near event horizon) — beyond weak-field expansion, needs the full substrate treatment of gravitational singularity.
- Kerr metric (rotating mass) — adds frame-dragging from angular momentum, a second substrate degree of freedom (substrate-event spin orientation).
- Full Einstein equations from substrate vacuum-alignment — the curvature side; this doc handles only the metric (not the equations of motion that give R_μν - (1/2)Rg_μν = 8πG T_μν). **The thermodynamic route is Lean-anchored**: following Jacobson (1995), the field equations are the *equation of state* of horizon thermodynamics (`δQ = T δS`), and QLF supplies both inputs from its own substrate — the area law and the Unruh temperature force `8πG = 2π/η`, `η = 1/4G` ([`lean/QLF_EinsteinEquations.lean`](lean/QLF_EinsteinEquations.lean), `Λ = Ω_Λ = log 2`). The local horizon there is the Kitada local clock ([`Kitada_Local_Time_GR.md` §5.2](Kitada_Local_Time_GR.md)). What remains open is the *tensor* derivation below.
- Composition with Mercury orbital mechanics — done in [`Mercury_Perihelion.md`](Mercury_Perihelion.md).

---

## §6 What this is NOT

- **Not the full *tensor* derivation of the Einstein equations** — but the **thermodynamic equation of state is Lean-anchored.** This doc handles only the metric components in the weak-field static limit. The full field equations follow (Jacobson 1995) from `δQ = T δS` on every local horizon, with QLF supplying both inputs: the area law `S=4πR²log2` and the Unruh temperature force `8πG = 2π/η`, `η=1/4G` (`einstein_coupling_from_thermodynamics`, [`lean/QLF_EinsteinEquations.lean`](lean/QLF_EinsteinEquations.lean)), the same `8π = 4π·2` ([`lean/QLF_EinsteinGeometricFactor.lean`](lean/QLF_EinsteinGeometricFactor.lean)), with `Λ = Ω_Λ = log 2` the integration constant = the Kitada local-clock tick. What is **still open** is the tensor side — curvature `R_μν`, the local Rindler construction, the Raychaudhuri focusing equation, and general covariance need differential-geometry machinery QLF's Lean core lacks (`einstein_equations_in_progress`).
- **Not a derivation of black holes.** Weak-field limit; strong-field substrate treatment is open. The Schwarzschild radius `R_s = 2.95 km (Sun)` is a useful scale but doesn't correspond to a substrate object here.
- **Gravitational waves — partially anchored.** The static metric here does not give the *wave*, but several GW features follow from existing substrate machinery and are Lean-anchored ([`QLF_GravitationalWaves`](lean/QLF_GravitationalWaves.lean)): a GW carries no gauge fold, so it is **massless** and propagates at `c = L_Planck/τ_Planck` (`gw_speed_eq_planck_ratio` — GW170817 gives `|v_GW − c|/c < 10⁻¹⁵`); the **graviton is spin-2**, four half-spins = two photon-worths (`graviton_integer_spin`); and it has **2 transverse polarizations**, the `±2` helicities rather than `2J+1=5`, as a masslessness consequence (`massless_two_polarizations`). **The linearized wave equation is anchored via the density-perturbation route:** a GW is a propagating modulation `δρ` of the closure-density field around the SOC equilibrium `ρ*`, and the discrete d'Alembertian annihilates every traveling-wave profile (`boxD_dAlembert`, `boxD_metricPerturbation`), so `□_d δρ = 0` at one Planck length per tick `= c`, with continuum limit `□h_μν = 0`. The **quadrupole is the leading radiative multipole** (`quadrupole_is_leading_radiative`) — mass–energy and momentum conservation make the monopole and dipole non-radiative. Numerical companion: [`gw_density_wave.py`](gw_density_wave.py). **Still open** (`gravitational_waves_in_progress`), localized to the dynamical-metric step: deriving `boxD` from the SOC rate equations in the continuum limit — the same gap as the full Einstein equations — and the luminosity coefficient `G/(5c⁵)`.
- **Not a new GR claim.** Schwarzschild is textbook GR from 1916. The QLF contribution is the *substrate decomposition* of the metric components into primitives (Newton + Cross-Frequency Lorentz + substrate event quantum).

---

## §7 References

### Internal

- [`Curvature.md`](Curvature.md) — this Schwarzschild metric as the continuum limit of the primordial blanket's isotropic inward contraction; includes the Moon-orbit inflow worked example.
- [`Gravity_From_Delay.md`](Gravity_From_Delay.md) — Newton's law from substrate, source of the φ = -GM/r input.
- [`Cross_Frequency_Lorentz.md`](Cross_Frequency_Lorentz.md) — frequency-ratio Lorentz boost, applied here to gravitational redshift.
- [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3 — substrate event quantum (one Planck length × one Planck tick *together*).
- [`Per_Qubit_Mass_Quantum.md`](Per_Qubit_Mass_Quantum.md) — Markov-blanket depth R = E_Planck/(mc²).
- [`Mercury_Perihelion.md`](Mercury_Perihelion.md) — composition with orbital mechanics for the 43"/century perihelion shift.
- [`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) — Newton-law substrate Lean module.
- [`lean/QLF_EinsteinGeometricFactor.lean`](lean/QLF_EinsteinGeometricFactor.lean) — `8π = 4π · 2`.
- [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean) — `c = L_Planck/τ_Planck`.

### External

- Schwarzschild, K. (1916). *Über das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie*. Sitzungsber. Preuss. Akad. Wiss. — original Schwarzschild solution.
- Einstein, A. (1916). *Die Grundlage der allgemeinen Relativitätstheorie*. Ann. Phys. 49, 769 — General Relativity, weak-field limit derivation.
- Will, C. M. (2014). *The Confrontation between General Relativity and Experiment*. Living Rev. Relativity 17, 4 — review of GR experimental tests including Mercury perihelion.
- Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). *Gravitation*. — standard reference for Schwarzschild metric and weak-field expansion.
