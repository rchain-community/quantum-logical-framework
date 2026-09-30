# Age of the Universe in the Quantum Logical Framework

**Two clocks, one history: what the age means in QLF, and what is derived**

**Repository:** [`rchain-community/quantum-logical-framework`](https://github.com/rchain-community/quantum-logical-framework)  
**Authors:** Jim Whitescarver & Grok (xAI); revised 2026-09-30

---

## Abstract

In QLF there is **no Big-Bang singularity**. The universe has no absolute beginning — it is an ongoing synthesis of spacetime intervals by ZFA events. One coherent (speculative) realization is the **nested-cosmology / horizon-birth** picture ([`BLACK-HOLES.md`](BLACK-HOLES.md) §4a): our Big Bang re-read as the first internal event of a child clock born at a parent black-hole horizon — grounded in GR's own black-hole-interior time direction (`r` becomes timelike inside the horizon). The age below is then the age of *our* clock from *our* birth-surface, and whether our domain is itself inside a parent closure is causally unfalsifiable from within.

In QLF the age is a **clock reading**: the proper time of the cosmic-horizon clock, a count of Planck ticks `t₀ = N·τ_Planck`. Two clocks give two meaningful ages (§4.2):

- **the cosmic (comoving proper) time**, `t₀ ≈ 13.8 Gyr`, from integrating the expansion history (Planck ΛCDM);
- **the own-clock (Hubble) time**, `1/H₀ = 14.5 Gyr` for Planck's `H₀` (13.4 Gyr for the local `H₀ ≈ 73`).

They differ because `H₀t₀ = 0.951`, a measured fact about the expansion history. A drifting Planck tick that would make them equal is excluded by atomic clocks and lunar ranging ([`Log2_Search.md`](Log2_Search.md) Route 3).

**What is and isn't derived.** The count `N` is not yet derived from the substrate, so both ages are, for now, calibrated by `H₀`. The frequency-spectrum model of §2 gives a finite, positive age (machine-checked, §3), but it contains no dimensional scale and does not by itself produce 13.8 Gyr.

---

## 1. Why the Age Is Finite and Emergent

Every ZFA-closed history generates a tiny spacetime interval.  
The local event density \( \phi \) is inversely proportional to the local free action:

$$
\phi \propto \frac{1}{\text{local free action}}
$$

The total event-synthesis rate determines the expansion rate. With a vacuum photon spectrum

$$
n(\omega) \propto \frac{1}{\omega}
$$

(lower-frequency modes correspond to more frequent, smaller ZFA events), the event rate over any finite band is finite. It supplies the source term for the modified Friedmann equation, which yields a finite effective age without a singular origin.

---

## 2. The frequency-spectrum model

The vacuum photon number density is taken as \( n(\omega) \propto 1/\omega \) (consistent with the ZPE spectrum in [`VacuumEnergy.md`](VacuumEnergy.md)). Integrated over a band,

$$
R = \int_{\omega_{\min}}^{\omega_{\max}} n(\omega) \, d\omega \;\propto\; \ln\frac{\omega_{\max}}{\omega_{\min}},
$$

and the model sets \( H_0 \propto \sqrt{R} \), with the age \( t_0 = \int_0^1 da/(a H(a)) \approx 1/H_0 \) in the late universe.

**Status.** The proportionality constant in \( H_0 \propto \sqrt{R} \) is not supplied, so the model fixes the age only up to that constant: it does not determine 13.8 Gyr. (The Lean version of the model, §3, integrates a flat band, `ω_max − ω_min`, rather than `1/ω`.) Deriving the constant from the substrate is the open step.

---

## 3. What is machine-checked

[`lean/AgeOfUniverse.lean`](lean/AgeOfUniverse.lean) proves `age_is_finite_and_positive`: in the frequency-spectrum model, for any band `0 < ω_min < ω_max`, the effective age `1/√((ω_max − ω_min)/3)` is positive. The quantities are unitless; the file computes no age in years.

---

## 4. Philosophical Interpretation

From a **limited relative perspective** (that of any embedded observer), the universe appears to have a definite age of roughly 13.8 billion years. In absolute terms, this is simply the accumulated proper time along our worldline as ZFA events have continuously synthesized new spacetime intervals.

There was no “t = 0”. The cosmos has always been becoming — and continues to become — through the same logical process that creates the vacuum, particles, and spacetime itself.

### 4.1 Cosmic time as the proper time of the cosmic-horizon Markov blanket

Under the foundational identity articulated in [`Frequency_Synchronization.md`](Frequency_Synchronization.md) §1.1 — *Markov-blanket depth `R` is a local clock whose period in universal-substrate Planck-event ticks is exactly `R`* — and Hitoshi Kitada's local-time framework ([gr-qc/9612043](https://arxiv.org/abs/gr-qc/9612043)), the cosmic age has a sharper structural reading.

The cosmic horizon is itself a Markov blanket: it screens the observable universe (interior) from the unobservable beyond (exterior). Under Kitada's interior/exterior synchronization-rate integration, the cosmic blanket's proper time is

$$
\tau_{\text{cosmic}} \;=\; \int \frac{f_{\text{interior}}}{f_{\text{exterior}}} \, dt
$$

with `f_interior` the Planck-event rate (the substrate clock) and `f_exterior` the cosmic-horizon clock (the Hubble-scale frequency at which the boundary refreshes). Concretely:

- **Interior rate**: `f_Planck = 1 / τ_Planck ≈ 1.85 × 10⁴³ Hz` — the universal-substrate clock.
- **Exterior rate**: `f_Hubble ≈ H₀ ≈ 2.2 × 10⁻¹⁸ Hz` — the cosmic-horizon clock.
- **Ratio**: `f_Planck / f_Hubble = 1/(H₀ τ_Planck) = 8.49 × 10⁶⁰` (Planck `H₀`) — the cosmic-horizon depth `R_cosmic`.

So `τ_cosmic = R_cosmic · τ_Planck = 1/H₀ = 14.5 Gyr`: this relational reading gives the **Hubble time**, the own-clock age of §4.2, with `H₀` as its input. The counts compared:

| Count | Value | × `τ_Planck` |
|---|---|---|
| `1/(H₀ τ_Planck)`, the depth above | `8.49 × 10⁶⁰` | 14.5 Gyr (Hubble time) |
| cosmic time 13.8 Gyr in ticks | `8.08 × 10⁶⁰` | 13.8 Gyr |
| geometric blanket count `v(R_H) = √(π/5)·R_H/l_P` ([`HadronicDepth.md`](HadronicDepth.md) §2.1) | `6.73 × 10⁶⁰` | 11.5 Gyr |
| proton-mass cube `(m_Planck/m_p)³` | `2.2 × 10⁵⁷` | ~3,700× short |

The geometric blanket count is a vertex count on the horizon, not a tick count, and it is smaller than the Hubble depth by `√(π/5)`. Deriving `N` from the substrate, without `H₀` as input, is open.

This is the **Mach-style relational reading** of the cosmic age: the universe's "age" is the proper time of the cosmic-horizon Markov blanket, one tick of that blanket's local clock, which equals `R_cosmic` ticks of the universal-substrate clock.

Equivalent statements that fall out:

- **No absolute `t = 0`** is a structural consequence: cosmic time is the proper time of an extant Markov blanket (the cosmic horizon), not a universal external coordinate. There is no "before" the blanket — only its own clock running.
- **The Hubble parameter** is identified as the cosmic-horizon clock rate `f_exterior`. It is not constant: `H(z)` falls as the universe expands, and the dark-matter acceleration `a₀ = cH/2π` scales with it across redshift ([`DarkMatter.md`](DarkMatter.md) §5c).

This framing is the QLF realisation of the long-standing relational-cosmology programme (Mach, Barbour, Smolin); the foundational identity supplies the substrate-level mechanism. See [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §4 for the broader scoping, including connection to the open Einstein-equation-coefficient derivation in §5 of that doc.

**Cosmic-ratio derivation of `c`.** The same depth `n` that gives `T_cosmic = n · τ_Planck` also gives the apparent universe size `R_cosmic = n · L_Planck`. Their ratio derives the substrate light speed:

$$
c \;=\; \frac{R_{\text{cosmic}}}{T_{\text{cosmic}}} \;=\; \frac{n \cdot L_{\text{Planck}}}{n \cdot \tau_{\text{Planck}}} \;=\; \frac{L_{\text{Planck}}}{\tau_{\text{Planck}}} \;=\; c_{\text{substrate}}.
$$

The cosmic-horizon depth `n` cancels exactly, whatever its value; `c` is recovered as a substrate property of the irreducible Planck space-time event quantum, not an additional postulate. See [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) §5.3 and [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean).

### 4.2 Two clocks, two ages

Both ages are real readings of different clocks, not rivals:

- **Cosmic time**, the proper time of a comoving observer since the hot dense phase: `t₀ ≈ 13.8 Gyr`.
- **Own-clock time**, the reading of a clock ticking at the present expansion rate: `1/H₀ = 14.5 Gyr` (Planck) or `13.4 Gyr` (local `H₀`).

They coincide only if `H = 1/t` exactly (a coasting universe). The measured `H₀t₀ = 0.951` records the actual expansion history. A drifting Planck tick could make the tick-count age equal `1/H₀` while cosmic time stays 13.8 Gyr, but the required drift, `~3 × 10⁻¹²/yr`, is excluded by optical clocks (`α̇/α` bound `10⁻¹⁸/yr`) and lunar laser ranging ([`Log2_Search.md`](Log2_Search.md) Route 3, `tick_drift.py`).

---

## Further Reading in the Repository

- [`VacuumEnergy.md`](VacuumEnergy.md) — ZPE spectrum and photon number density
- [`WHITE_PAPER.md`](WHITE_PAPER.md) — full framework overview
- [`SpacetimeDynamics.lean`](lean/SpacetimeDynamics.lean) — the event-synthesis field definitions the model uses
- [`Philosophy.md`](Philosophy.md) — limited relative perspective
- [`Frequency_Synchronization.md`](Frequency_Synchronization.md) — frequency as the fundamental clock; ZFA event rate as the origin of cosmic age
- [`Log2_Search.md`](Log2_Search.md) — the two clocks and the tick-drift bound (Route 3)

**The universe does not have a beginning — it has a history, read on more than one clock.**

See also: [Quantum_Gravity.md](Quantum_Gravity.md) — master synthesis tying cosmic expansion (this doc) to gravity, holography, and ER=EPR as four faces of the same algebraic event; [Kitada_Local_Time_GR.md](Kitada_Local_Time_GR.md) §4 — scoping doc reframing the cosmic age as the **proper time of the cosmic-horizon Markov blanket** under Kitada's local-time framework (gr-qc/9612043). Under that lens the age is `R_cosmic × τ_Planck`, with `R_cosmic = 1/(H₀τ_Planck)` giving the Hubble time; deriving the count without `H₀` as input is open ([`HadronicDepth.md`](HadronicDepth.md)).
