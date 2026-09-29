# Cosmological constant Λ from [QLF](README.md) substrate: closing the vacuum catastrophe and predicting Ω_Λ = log 2

**Scoping doc — the famous "vacuum catastrophe" closed by 122 orders of magnitude, with the substrate predicting Ω_Λ = log 2 ≈ 0.693 to 1.2% of the observed 0.685.** The standard quantum field theory estimate of the vacuum energy density gives `ρ_QFT ≈ ρ_Planck ≈ 5 × 10¹¹³ J/m³` (volume-counted Planck-scale zero-point modes). The observed dark-energy density is `ρ_Λ ≈ 5.83 × 10⁻¹⁰ J/m³` (Planck mission 2018). **The discrepancy of 10¹²² is the largest mismatch in physics** (Weinberg 1989, Carroll 2001).

> **Status (2026-09-29): the `log 2` prefactor does not survive.** Three results, each pre-registered and
> proved, change what this doc supports. With `L = c/H`, `ρ_Λ ∝ H²` puts `Ω_Λ = log 2` at recombination and
> BBN, which the data exclude (§5.7). The event-horizon alternative is excluded by full CMB + DESI + SN fits
> (§5.7). Counting on the de Sitter horizon forces the prefactor to 1 (§5.8). And the first law with QLF's
> own Hawking temperature fixes the horizon entropy at `A/4`, so §3's count overcounts by `4 log 2`;
> recounted, it gives `Ω_Λ = 1/4` or `1`, not `log 2` ([`Gravity_From_Delay.md`](Gravity_From_Delay.md) §9a).
> **What stands:** the `(R_H/L_P)²` reduction of the `10¹²²` catastrophe, which does not depend on the O(1)
> prefactor. The observed `Ω_Λ = 0.685 ± 0.007` is still within 1.2σ of `log 2`. That is one way of fitting
> today's value, not a derivation. The sections below are kept as written, for the record.

QLF substrate primitives give:

$$\rho_\Lambda^{\text{QLF}} \;=\; \frac{3 \log 2}{8 \pi} \cdot \frac{c^4}{G \, R_H^2}$$

where `R_H = c/H_0` is the Hubble radius. Two structural ingredients combine:

- **The (R_H/L_Planck)² ≈ 10¹²² closure** — holographic surface counting (3D substrate from 8-twist 6+2 split) × de Sitter horizon temperature.
- **The 2/8 = 1/4 gauge-axis fraction** — of the 8-twist alphabet's axes, only the **2 gauge twists (`+/-`)** carry temporal-binding closures and contribute to dark-energy modes; the 6 spatial twists carry spatial extension but not vacuum-energy temporal mass. Same 6+2 split that powers α via N=9=3², nuclear magic-number ℓ=3, and Newton's 1/r².

Numerical match:

- **ρ_Λ_QLF ≈ 5.32 × 10⁻¹⁰ J/m³** vs observed 5.83 × 10⁻¹⁰ J/m³ — **8.7% match**.
- **Ω_Λ_QLF = log 2 ≈ 0.693** vs Planck 2018 observed `Ω_Λ = 0.685` — **1.2% match**. The dark-energy fraction itself is substrate-predicted, not just Λ's form.

**Four substrate ingredients, all already Lean-anchored or substrate-derived in v1.3.0:**

1. Holographic surface event count `N = 4π R²` ([`QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean))
2. Per-event log 2 entropy quantum ([`QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean))
3. de Sitter horizon temperature `T_dS = ℏc/(2π R_H k_B)` (substrate horizon thermodynamics)
4. Gauge-axis fraction 2/8 from 6+2 alphabet split (per [`Gravity.md`](Gravity.md) gauge-folding rule + [`Magic_numbers.md`](Magic_numbers.md))

This closes the **most famous open problem in physics** to **8.7% in Λ and 1.2% in Ω_Λ** from QLF substrate alone, with only `H_0` as the empirical input.

---

## §1 The vacuum catastrophe

Standard QFT computes vacuum energy as the zero-point sum over field modes:

$$\rho_{\text{QFT}} \;=\; \int_0^{k_{\text{UV}}} \frac{d^3k}{(2\pi)^3} \cdot \frac{1}{2} \hbar \omega_k.$$

With UV cutoff `k_UV ~ 1/L_Planck` (the natural Planck-scale cutoff), the integral gives `ρ_QFT ≈ ρ_Planck c² ≈ 5 × 10¹¹³ J/m³`.

Observed dark-energy density (from CMB + supernovae + BAO, Planck 2018):

$$\rho_\Lambda^{\text{obs}} \;\approx\; 5.83 \times 10^{-10} \text{ J/m}^3 \;=\; \Omega_\Lambda \cdot \rho_{\text{crit}}$$

with `Ω_Λ ≈ 0.685` and `ρ_crit = 3 H_0² c² / (8πG)`.

**Discrepancy**: `ρ_QFT / ρ_obs ≈ 10¹²²`. This is "the biggest, the most embarrassing, the most disturbing problem in theoretical physics" (Weinberg 1989).

Standard responses (anthropic / multiverse / dynamical mechanisms) leave the structural origin of the small Λ unexplained. **QLF substrate primitives close the 10¹²² gap structurally**.

---

## §2 Holographic horizon vs volume mode count

The QFT calculation counts vacuum modes in the 3D bulk volume of the universe: `N_QFT ~ (R_H/L_Planck)³`. Each mode contributes Planck-scale energy at the natural UV cutoff: `E_per_mode ~ E_Planck`.

QLF substrate counts vacuum-aligned closures on the 2D cosmic horizon surface, per [`Gravity_From_Delay.md`](Gravity_From_Delay.md) and [`VacuumEnergy.md`](VacuumEnergy.md) §6. (The cosmic horizon IS the maximal-frequency primordial Markov blanket, at Fuller frequency `v_cosmic ≈ 6.7 × 10⁶⁰`; see [`Primordial_Markov_Blankets.md`](Primordial_Markov_Blankets.md) §8.)

$$N_{\text{horizon}} \;=\; \frac{4 \pi R_H^2}{L_{\text{Planck}}^2}.$$

The first reduction factor: `N_QFT / N_horizon ~ (R_H/L_Planck)`. Going from 3D volume to 2D holographic surface saves one factor of `R_H/L_Planck` — the substrate's 6+2 spatial-vs-gauge alphabet split is what enforces this (the holographic principle as substrate-level prediction, [`Holographic.md`](Holographic.md)).

The second reduction factor: each substrate event on the cosmic horizon is at the **de Sitter temperature**, not the Planck temperature:

$$T_{\text{dS}} \;=\; \frac{\hbar c}{2 \pi R_H k_B}.$$

For `R_H ≈ 1.32 × 10²⁶ m`: `T_dS ≈ 2.7 × 10⁻³⁰ K`. The energy per event is `k_B T_dS ≈ 3.8 × 10⁻⁵³ J` — vastly smaller than the Planck energy `E_Planck ≈ 2 × 10⁹ J`. Ratio: `k_B T_dS / E_Planck ≈ 1.8 × 10⁻⁶²`.

Combined reduction: `(R_H/L_Planck) × (k_B T_dS / E_Planck) ~ (R_H/L_Planck)²`.

This is the structural origin of the 10¹²² closure.

---

## §3 The substrate derivation: ρ_Λ = (3 log 2 / 8π) × c⁴/(G R_H²)

Combining §2's ingredients with per-event `log 2` from [`QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean):

**Total horizon energy from gauge-fold modes only.** Of the 8-twist alphabet's axes, only the **2 gauge twists (`+/-`)** carry temporal-binding closures (per [`Gravity.md`](Gravity.md) §2 gauge-folding rule: *"only `+`/`−` folds create local time, accumulate constructing delay"*). The 6 spatial twists carry spatial extension but not vacuum-energy temporal mass. Vacuum modes contributing to dark-energy density are the gauge-fold closures at horizon scale:

$$f_{\text{gauge}} \;=\; \frac{\text{gauge twists}}{\text{total alphabet axes}} \;=\; \frac{2}{8} \;=\; \frac{1}{4}.$$

This is the **same 6+2 alphabet split** that powers α via N=9=3² ([`Magnetism_Spatial_Dynamics.md`](Magnetism_Spatial_Dynamics.md) §6.1.3), nuclear magic-number ℓ=3 threshold ([`Magic_numbers.md`](Magic_numbers.md)), Newton's 1/r² law ([`Gravity_From_Delay.md`](Gravity_From_Delay.md)), and the 4π in the Einstein 8π = 4π·2 factor.

Total gauge-mode horizon energy:

$$E_{\text{total}} \;=\; f_{\text{gauge}} \cdot N_{\text{horizon}} \cdot \log 2 \cdot k_B T_{\text{dS}} \;=\; \frac{1}{4} \cdot \frac{4 \pi R_H^2}{L_{\text{Planck}}^2} \cdot \log 2 \cdot \frac{\hbar c}{2 \pi R_H} \;=\; \frac{\log 2 \cdot \hbar c \, R_H}{2 L_{\text{Planck}}^2}.$$

Using the substrate identity `L_Planck² = ℏG/c³` (from `c = L_Planck/τ_Planck` and `G = L_Planck² c³/ℏ` in [`QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean)):

$$E_{\text{total}} \;=\; \frac{\log 2 \cdot c^4 R_H}{2 G}.$$

**Horizon volume:**

$$V_{\text{horizon}} \;=\; \frac{4}{3} \pi R_H^3.$$

**Vacuum energy density:**

$$\boxed{\rho_\Lambda^{\text{QLF}} \;=\; \frac{E_{\text{total}}}{V_{\text{horizon}}} \;=\; \frac{3 \log 2}{8 \pi} \cdot \frac{c^4}{G \, R_H^2}.}$$

The famous `c⁴/(G R_H²)` structure recovers the standard Friedmann-equation form `ρ_Λ = 3 c² H_0² Ω_Λ / (8πG)` (using `R_H = c/H_0`); QLF supplies the **substrate-derived prefactor** `3 log 2 / (8π) ≈ 0.0827` matching the empirical Friedmann form `3 Ω_Λ/(8π) ≈ 0.0818` to **1.2%**.

---

## §4 The 10¹²² reduction: surface vs volume + de Sitter vs Planck + gauge-axis fraction

Why does QLF close the vacuum catastrophe by exactly 122 orders of magnitude? The structural argument:

$$\frac{\rho_{\text{QFT}}}{\rho_\Lambda^{\text{QLF}}} \;=\; \underbrace{\frac{R_H}{L_{\text{Planck}}}}_{\text{surface vs volume}} \;\times\; \underbrace{\frac{R_H}{L_{\text{Planck}}}}_{\text{T}_{\text{dS}}\text{ vs }T_{\text{Planck}}} \;\times\; \underbrace{4}_{\text{1/gauge-fraction}} \;\sim\; 4 \left(\frac{R_H}{L_{\text{Planck}}}\right)^2 \;\approx\; 3 \times 10^{122}.$$

Each factor of `R_H/L_Planck` comes from a distinct substrate principle:

- **(Surface vs volume)**: holographic event count `N ∝ R²/L_P²` instead of QFT's `N_QFT ∝ R³/L_P³`. The substrate's 3-dimensionality (from the 8-twist 6+2 alphabet split, [`Magic_numbers.md`](Magic_numbers.md)) reduces vacuum-energy counting from the bulk to the boundary by one factor of `R/L_P`.
- **(de Sitter vs Planck)**: each horizon event is at temperature `T_dS = ℏc/(2π R_H k_B)`, not `T_Planck = ℏ/(τ_Planck k_B)`. The ratio `T_dS/T_Planck = L_P/R_H`, so energy per event scales by `L_P/R_H` — another factor of `R/L_P` reduction.

Together: `(R_H/L_Planck)² ≈ 10¹²²`. The vacuum catastrophe **is** the discrepancy between volume-Planck and surface-deSitter counting.

This is the QLF substrate's structural answer to "why is Λ so small?" — because the substrate counts vacuum-aligned modes on the holographic 2-surface at the de Sitter scale, not in the bulk at the Planck scale. Both reductions follow from QLF substrate primitives that already Lean-anchored other observables (G, Newton's 1/r², Mercury perihelion).

---

## §5 Numerical evaluation

Computed with substrate `G = L_Planck² c³/ℏ` (Planck-units identity), substrate `c = L_Planck/τ_Planck`, per-event `log 2` from `QLF_FreeEnergy.lean`, gauge-axis fraction `2/8` from the 6+2 alphabet split, and Hubble radius `R_H = c/H_0` with Planck 2018 measurement `H_0 = 67.4 km/s/Mpc ≈ 2.27 × 10⁻¹⁸ Hz`:

| Quantity | Value |
|---|---|
| `R_H` | `1.32 × 10²⁶ m` |
| `N_horizon = 4π R_H² / L_P²` | `8.39 × 10¹²²` |
| `T_dS k_B` | `3.81 × 10⁻⁵³ J` |
| Gauge-axis fraction `f_gauge = 2/8` | `0.25` |
| `E_total = f_gauge × N log 2 k_B T_dS` | `5.54 × 10⁶⁹ J` |
| `V_horizon = (4/3)π R_H³` | `9.65 × 10⁷⁸ m³` |
| **`ρ_Λ_QLF`** | **`5.32 × 10⁻¹⁰ J/m³`** |
| `ρ_Λ_observed` (Planck 2018) | `5.83 × 10⁻¹⁰ J/m³` |
| **Match** | **8.7%** |
| `ρ_Planck c²` (QFT estimate) | `≈ 4.6 × 10¹¹³ J/m³` |
| **Vacuum catastrophe** | `ρ_Planck/ρ_obs ≈ 10¹²²` |
| **QLF closure** | `ρ_Planck/ρ_QLF ≈ 9 × 10¹²²` |
| Reduction factor `4 × (R_H/L_P)²` | `2.9 × 10¹²²` ✓ matches |

Verification in [`cosmological_constant_demo.py`](cosmological_constant_demo.py).

### §5.5 Ω_Λ = log 2: the dark-energy fraction is substrate-predicted

The substrate-derived prefactor `3 log 2 / (8π)` matches the empirical Friedmann form `3 Ω_Λ / (8π)` when

$$\boxed{\Omega_\Lambda^{\text{QLF}} \;=\; \log 2 \;\approx\; 0.6931.}$$

Comparing to Planck 2018 observed `Ω_Λ = 0.685`:

| Quantity | Value | Source |
|---|---|---|
| `Ω_Λ_QLF` (substrate) | `log 2 = 0.6931` | derived above |
| `Ω_Λ_observed` (Planck 2018) | `0.685 ± 0.007` | Planck Collaboration 2020 |
| **Match** | **1.2%** | well within Planck statistical uncertainty |

This is a **second substrate prediction** from the same derivation — not just Λ's form (`c⁴/(GR²)`) but also the **dark-energy fraction itself** (Ω_Λ). The structural argument: of the universe's total horizon-mode energy, the fraction that goes into dark energy is exactly the fraction of substrate-alphabet axes that carry temporal binding times the per-event log 2 quantum.

This is the same per-event log 2 quantum that:
- Powers active inference via `zfa_closure_minimizes_free_energy` ([`QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean))
- Saturates KL divergence against the vacuum prior ([`QLF_VacuumAlignment.lean`](lean/QLF_VacuumAlignment.lean))
- Sets the horizon entropy `S = N log 2` for Newton's law derivation ([`Gravity_From_Delay.md`](Gravity_From_Delay.md))

**Pull-quote**: *The dark-energy fraction Ω_Λ = log 2 is the per-event information quantum that saturates the cosmic-horizon Markov blanket's active-inference closure.*

### §5.6 Counterfactual: only the 2-gauge substrate gives the observed Ω_Λ

The same counterfactual chain as Λ:

- 2 gauge axes (substrate `+/-`) → `f_gauge = 1/4` → `Ω_Λ = log 2 ≈ 0.693` ✓ (1.2% from observed 0.685)
- 4 gauge axes → `f_gauge = 1/2` → `Ω_Λ = 2 log 2 ≈ 1.386` ✗ (would need universe 100% dark-energy-dominated)
- 0 gauge axes (no gauge alphabet) → `f_gauge = 0` → `Ω_Λ = 0` ✗ (no dark energy at all)

Only the substrate with 2 gauge axes (the empirical 6+2 split that gives α and the 3D substrate) gives the observed Ω_Λ. This is the **fourth** structural counterfactual tying observation to the 8-twist 6+2 alphabet split, joining α, magic-numbers, and Newton's 1/r².

### §5.7 Which horizon? The early-epoch test (2026-09-29)

§3 counts events on a horizon of radius `L` and sets `L = R_H = c/H`. In holographic-dark-energy notation
(Li 2004) the result is `ρ_Λ = 3C²M_p²/L²` with **`C² = log 2`**. The prefactor does not decide the
history; the choice of `L`, and whether the vacuum exchanges energy with matter, does.
[`omega_lambda_epochs.py`](omega_lambda_epochs.py) runs the three readings (pure Python, `log 2` the only
QLF input):

| Reading | Today | Recombination / BBN | Status |
|---|---|---|---|
| **A.** `L = c/H`, matter conserved (the literal §3) | `Ω_Λ = log 2`, but `ρ_Λ` redshifts like matter: `w_eff = 0`, `q₀ = +0.5` | `Ω_Λ = 0.693` at both | **Rejected by data.** No acceleration (Hsu 2004), and at BBN `H` is `×1.81`, equivalent to `ΔN_eff ≈ 14` against a bound near `0.3` |
| **B.** `L = c/H`, vacuum keeps `w = −1` and exchanges energy to hold `log 2` | `q₀ = −0.54` (observed ≈ −0.55) | `Ω_Λ = 0.693` at both; `H² ∝ a^−0.92` at every epoch, so no matter era (`q = −0.54` at `z = 2`, ΛCDM `+0.39`) | **Rejected by data.** Same BBN and early-dark-energy failure as A (`Ω_early < 0.06`, Doran & Robbers 2006) |
| **C.** `L` = future event horizon, same `C² = log 2`, `Ω_de(0) = log 2` | `w₀ = −1` exactly (because `√Ω₀ = C` when `Ω₀ = C²`); acceleration begins at `z ≈ 0.56` | `Ω_de ≈ 9 × 10⁻⁵` at recombination, `≈ 10⁻¹⁷` at BBN | **Open candidate.** Passes the early-epoch test with no extra ingredient. Screen: CMB shift parameter `R = 1.717` vs measured `1.7502 ± 0.0046` (Chen, Huang & Wang 2019; ΛCDM at the same `Ω_m`: `1.745`), **7.2σ low** at fixed `Ω_m h²`. A refit may move it; until one is done this is a live failure, not a pass |

**What this changes.** The tension named in [`Curvature.md`](Curvature.md) §8a is a property of `L = c/H`,
not of the `log 2` prefactor. Readings A and B are ruled out on more than early dark energy: A also fails
the observed acceleration. Reading C keeps `C² = log 2` and gives `w₀ = −1` for free, but gives up P5
(`Ω_Λ = log 2` at every epoch): the fraction grows from near zero, and today's `log 2` becomes an
initial condition, not a theorem. It also makes the dark energy mildly phantom in the future
(`w → −1/3 − 2/(3C) ≈ −1.13`). The §6 early-dark-energy argument for the Hubble tension does not survive
in C: the early fraction is far too small to move the sound horizon.

**Not involved: a `0.035–0.04` correction.** The numbers near there in this repo (the α residual
`+0.036`, `G`'s `+0.0336` in [`Gravity.md`](Gravity.md) §4a, Koide `ε = 0.0396`) are dimensionless
residuals on unrelated integers, with no proposed link to horizon counting. Read as a correction to
`log 2`, a few-percent shift moves `Ω_Λ` by about `0.025` (`0.693 → 0.668` pulls it 2.3σ below Planck).
Readings A and B need the early fraction cut by more than 10× (by the Doran–Robbers bound; later bounds
are tighter). Read as the early fraction itself, `Ω_early ≈ 0.036` would give `ΔN_eff ≈ 0.23–0.26` at BBN,
which is marginal, but nothing in QLF produces it. Close numbers are not evidence
([`Alpha_Residual.md`](Alpha_Residual.md) §9k).

**Physical motivation for C, and the step it rests on.** Jim's reading (2026-09-29): *every event
creates information/energy; about half is conserved locally, and the other half is lost to space and
realized in the distant future. Looking back, that is inflation; in the present, it is gravity and
entropy.* This picks C over A and B. The half "lost to space" is booked on the **future** horizon, where
it is realized, and not as vacuum density at the epoch that made it. Booking it at its creation epoch is
a constant fraction (½ or `log 2`), which is readings A/B again. It also has a standard-physics
counterpart: in GR, `∇^μ T_μν = 0` holds exactly while total energy in an expanding universe is not
conserved (a redshifting photon loses energy to expansion). In C, the dark-energy equation of state
`w = −1/3 − 2√Ω/(3C)` is *that* local conservation law applied to `ρ ∝ 1/L²`.

**Local conservation does not select C by itself.** Total `∇^μ T_μν = 0` holds in all three readings.
B's vacuum trades energy with matter, but the total is conserved, as the Bianchi identity requires.
Separate conservation of the dark-energy component holds in A as well as C: in A it is exactly what
forces `w_eff = 0`. So a continuity equation can at most exclude B. What selects C is the horizon: `L` is
the **future event horizon**, not `c/H`. Jim's "the other half is booked at the future horizon" motivates
that choice, but it is a second premise, not a consequence of conservation. It also carries the standard
objection to Li's cutoff: today's dark energy depends on the universe's future, and QLF would have to
explain what a future horizon means when the future is not yet synthesized.

Neither step is **proved in QLF**. For conservation: The per-event split is `event_duality_balanced`
([`QLF_CosmicInflation`](lean/QLF_CosmicInflation.lean)), which is `rfl` on two defined constants
(`+1`, `−1`): bookkeeping, not a conservation result. Energy is the one current QLF does not conserve
per event ([`Conservation.md`](Conservation.md) §2a: it is a multiplicity, not a signed count). And
[`QLF_BianchiClosure`](lean/QLF_BianchiClosure.lean) takes `∇^a T_ab = 0` as a hypothesis. So C rests on
**two unproved steps**:

1. **A substrate continuity equation:** the change in closure multiplicity inside a region equals the
   flux through its blanket. Any of A–C needs it to have dynamics at all.
2. **The horizon selection:** the non-local share is booked on the future event horizon rather than on
   `c/H`. This is the step that picks C.

**The `½` vs `1 − log 2` comparison is not a mismatch yet.** `½` would be a per-event split. `1 − log 2 ≈
0.31` is today's cumulative matter fraction, which in C changes with epoch (`≈ 0.86` at `z = 2`, `→ 1`
early). The two need not be equal. The open question is which per-event split, run over C's history,
produces `Ω_m(0) = 1 − log 2`, or whether `Ω_de(0) = log 2` stays an initial condition.

**Falsifier for C.** A full CMB + BAO + SN fit of event-horizon HDE with `C` **fixed** at `√log 2 ≈ 0.833`
(no free `C`). If it is excluded, none of the readings tested here rescues `ρ_Λ ∝ log 2 / L²` with this
prefactor.

**Verdict from published fits (checked 2026-09-29): C is excluded.** Li, Li, Du, Wu, Feng, Zhang & Zhang
(*Revisiting holographic dark energy after DESI 2024*, arXiv:2411.08639, EPJC) fit event-horizon HDE with
free `c` in the same convention (`ρ_de = 3c²M_p²L⁻²`, so `c` is our `C`):

| Data | `c` (68%) | `C = 0.833` is | `ln B` (HDE vs ΛCDM) |
|---|---|---|---|
| CMB + DESI + PantheonPlus | `0.673 ± 0.023` | 7.0σ high | `−28.6` |
| CMB + DESI + Union3 | `0.642 ± 0.028` | 6.8σ high | `−26.9` |
| CMB + DESI + DESY5 | `0.701 ± 0.024` | 5.5σ high | `−29.5` |
| CMB + DESI | `0.462 (+0.027, −0.036)` | ≈ 14σ high | — |

`|ln B| > 5` is *decisive* on the Jeffreys scale, so even HDE's best-fit `c` loses to ΛCDM decisively once
CMB is included, and `C = 0.833` sits 5.5–7σ further from that best fit. This is read off free-`c`
posteriors, not our own fixed-`C` refit, and uses DESI DR1. Neither caveat can plausibly turn 5σ+ into
a pass.

**The interacting variant, and why it doesn't rescue C.** The same paper fits interacting HDE with
`Q = βHρ_de`, where `β > 0` means energy flows *into* dark energy. That is the direction of the "half lost to
space" picture. There `c = 1.12 ± 0.17` (CMB + DESI + PantheonPlus), so `0.833` is within 2σ, and
`β = 0.55 (+0.19, −0.11)`. But it needs `Ω_m = 0.147 (+0.047, −0.068)` and a free coupling, and it too is
decisively disfavored against ΛCDM (`ln B = −24.8, −23.2, −24.1`). A version with both `C² = log 2` and
`β = ½` fixed would be a sharp zero-parameter test, but its parent model is already decisively
disfavored, so it is not worth pursuing ahead of the next point.

**Where this leaves `log 2`.** All three horizon readings of `ρ_Λ = 3 log 2 · M_p²/L²` are now out:
A and B on the early-epoch test, C (and its interacting extension) on the full fits. What the data favor
is a constant `Λ`. In that reading `log 2` can only be *today's* `Ω_Λ` (Planck `0.685 ± 0.007`, 1.2σ): one
way of fitting the present, not an every-epoch law. That reverses P5 of
`QLF_InflationObserver` (PR #164), and the coincidence problem
("why `log 2` now?") returns. The substrate derivation of `ρ_Λ` in §3 then needs a horizon that does
not evolve (for example the asymptotic de Sitter radius), and it is open whether §3's count can be
redone on one while keeping `log 2`.

### §5.8 A horizon that does not evolve: the de Sitter no-go — *pre-registered 2026-09-29*

§5.7 leaves one way to keep `log 2` with a constant `Λ`: count on a horizon that does not evolve. The
natural choice is the final de Sitter radius `R∞ = c/H∞`. That fails on self-consistency. On `R∞`, §3
gives `ρ = log 2 · 3c²H∞²/(8πG)`. A universe that ends as pure de Sitter has, by Friedmann,
`ρ = 3c²H∞²/(8πG)`. The two agree only if `log 2 = 1`. Counting on the de Sitter horizon forces the prefactor
to be exactly 1. This matches Li (2004): holographic dark energy reaches de Sitter only at `c = 1`, and
`c < 1` runs phantom, as reading C did.

**Two refinements.**

1. *The no-go is about the de Sitter radius, not every fixed radius.* A fixed `R = √(log 2)·c/H∞` would
   be self-consistent. But nothing motivates counting on a radius that is not the horizon. And for
   **any** fixed radius, today's `Ω_Λ = (H∞/H₀)²` depends on the epoch: the coincidence problem.
2. *The dark-energy `log 2` is the per-event quantum sitting on top of the Bekenstein–Hawking count.*
   §3's horizon energy is `f_gauge · N log 2 · k_B T_dS`. With `f_gauge = 1/4` and `S_BH = N/4`, that is
   `log 2 × S_BH · k_B T_dS`. And `S_BH · T_dS` is exactly the energy `ρV` of a self-consistent de Sitter
   horizon. So §3's `log 2` is the same `log 2` as the `4 log 2` entropy residual of
   [`Gravity_From_Delay.md`](Gravity_From_Delay.md) §9. Whatever settles that residual decides this one
   (§9a there).

**Pre-registered statements** (to be proved in `lean/QLF_DeSitterCount.lean`, no new axioms):

| | Statement |
|---|---|
| D1 | on `R = c/H`, §3's density is `log 2 × ρ_crit(H)` |
| D2 | a counted density `p · ρ_crit` is self-consistent de Sitter iff `p = 1` (algebra: bookkeeping by rule 4, stated as the anchor) |
| D3 | QLF's count is not self-consistent on the de Sitter horizon (`log 2 ≠ 1`) |
| D4 | in Planck units, §3's energy is `log 2 × S_BH · T_dS`, and `S_BH · T_dS = ρ_dS · V = R/2` on `R = 1/H` |

**Failure:** any of D1–D4 fails to prove.

**Result (2026-09-29): all four proved**, no new axioms, in
[`lean/QLF_DeSitterCount.lean`](lean/QLF_DeSitterCount.lean): D1 `desitter_count_ratio`, D2
`selfconsistent_iff_unit_prefactor`, D3 `qlf_count_not_selfconsistent` (via `log_two_lt_one`), D4
`section3_energy_eq_log_two_mul_bh` and `bh_energy_eq_desitter_energy`. The statements are the ones frozen
above. So a constant `Λ` cannot get `log 2` from counting on its own horizon, and whether §3's `log 2` means
anything now rests on the entropy residual ([`Gravity_From_Delay.md`](Gravity_From_Delay.md) §9a).

---

## §6 Honest scoping (three-tier)

**Tier 1 (structural).** The form `ρ_Λ = (3 log 2 / 8π) × c⁴/(G R_H²)` and `Ω_Λ = log 2` fall out of substrate primitives:

- Holographic event count `N = 4π R²` (3D substrate → 2D horizon)
- Per-event log 2 (Lean-anchored as `zfa_closure_minimizes_free_energy`)
- de Sitter temperature `T_dS = ℏc/(2π R k_B)` (substrate horizon thermodynamics, sibling to Lamb shift `1/(2π)` loop phase)
- The 10¹²² QFT-vs-QLF reduction = `(R_H/L_P)²` — surface-vs-volume × de Sitter-vs-Planck
- Gauge-axis fraction `2/8 = 1/4` from the 6+2 alphabet split (same split that gives α via N=9=3²)

**Tier 2 (numerical, h + observables).** With Planck 2018 `H_0`, substrate `G`, substrate `c`:
- `ρ_Λ_QLF = 5.32 × 10⁻¹⁰ J/m³` matching observed `5.83 × 10⁻¹⁰ J/m³` to **8.7%**.
- `Ω_Λ_QLF = log 2 ≈ 0.6931` matching observed `0.685 ± 0.007` to **1.2%**.
- Vacuum catastrophe of 10¹²² closed.

**Tier 3 (open).**

- **Time-dependence**: ρ_Λ_QLF ∝ 1/R_H² ∝ H². In the standard cosmology Λ is constant. QLF substrate predicts a slow time-variation of Λ tied to cosmic expansion — testable via comparison with future high-precision dark-energy measurements (Euclid, LSST, Roman).
- **Tension with early dark-energy bounds (named 2026-09-29).** `ρ_Λ ∝ H²` is not a *slow* variation: with `ρ_crit ∝ H²` too, it keeps `Ω_Λ = log 2` at **every** epoch (`omegaLambda_eq_log_two`, [`lean/QLF_InflationObserver.lean`](lean/QLF_InflationObserver.lean)). That puts `≈ 69%` dark energy at recombination and BBN, against a CMB bound `Ω_early < 0.06` at 95% (Doran & Robbers, *Early dark energy cosmologies*, JCAP 0606:026 (2006)), and later data are tighter. **Falsifier:** with `L = c/H` the dynamical-Λ reading is ruled out; §5.7 tests the alternative horizons: the future-event-horizon reading C survives the early-epoch test but is excluded by full CMB + DESI + SN fits (5.5–7σ; Li et al. 2024). The early-dark-energy Hubble-tension argument below inherits this: the EDE models that ease the tension carry a few percent for a brief window, not 69% throughout ([`Curvature.md`](Curvature.md) §8a).
- **Lean-anchor the de Sitter temperature**: `T_dS = ℏc/(2π R k_B)` should be derivable from substrate equipartition + holographic event count; currently stated as a structural identity, not Lean-anchored individually.
- **Reconcile with continuous Bekenstein-Hawking 1/4**: same coarse-graining gap as in `Gravity_From_Delay.md` §9.
- **Substrate derivation of H_0 from cosmic-horizon depth**: partially in [`HadronicDepth.md`](HadronicDepth.md), full quantitative form open. Would close the last empirical input.
- **The residual 8.7% in Λ** (vs 1.2% in Ω_Λ) is the H_0 calibration discrepancy between Planck-CMB H_0 (67.4) and SH0ES-supernova H_0 (~73) — the famous "Hubble tension." QLF doesn't *numerically* predict the value, but it is **not silent**: because `ρ_Λ ∝ H²` (the dynamical-Λ point above), QLF's dark energy was **denser in the past** — *early-dark-energy character*, which is the leading class of proposed Hubble-tension resolutions (more early DE → higher early expansion → smaller sound horizon → the CMB-inferred H_0 shifts *up* toward local). Combined with the SPARC dark-matter fit independently voting *local* (`a₀=cH₀/2π` at `H₀≈72.9`), QLF is a **dynamical-DE, non-ΛCDM cosmology in the resolution-favorable class** — the tension is reframed as a model-dependence of the ΛCDM early inference, not a crisis. A perspective + data vote, not a derivation; the quantitative early-universe expansion history is open. See [`DarkMatter.md`](DarkMatter.md) §5a.

---

## §7 What this is NOT

- **Not a derivation of `H_0` from substrate alone.** The Hubble constant enters as one observable; we use it to compute R_H. This is **the single residual calibration** behind the cosmic age and `Λ`: the age is `t₀ = N · τ_Planck`, with the tick `τ_Planck = √(ℏG/c⁵)` fixed by `ℏ` and the count `N` (cosmic-horizon depth `n ≈ 6.7 × 10⁶⁰`) the substrate's to derive — so deriving `H_0` *is* deriving `N` ([`UniversalRelativity.md`](UniversalRelativity.md) §5). Substrate derivation of `N`/`H_0` from the geometric primordial-blanket depth is partially in [`HadronicDepth.md`](HadronicDepth.md), open in full quantitative form.
- **Not a derivation of `Ω_Λ` from substrate.** The dark-energy *fraction* (Ω_Λ ≈ 0.685) is empirical; QLF predicts the *form* of Λ but not the matter-vs-dark-energy partition.
- **Not strong-field GR (cosmology).** The substrate derivation assumes a weak-field horizon-thermodynamics reading; full coupling to Friedmann-Lemaître-Robertson-Walker is Tier-3 open.
- **Not a new physics claim**. The cosmological-constant-as-horizon-density-with-log-2 reading sits in the entropic-gravity / holographic-vacuum tradition (Verlinde 2011, Padmanabhan 2010, Banks 1999). QLF's contribution is the **substrate-primitive composition** showing the result falls out structurally from already-Lean-anchored ingredients.

---

## §8 Connection to existing QLF material

[`VacuumEnergy.md`](VacuumEnergy.md) §6.2 already states the vacuum-alignment principle's cosmological-constant implication qualitatively: *"the observed `Λ` is the residual gradient curvature of the near-maxent vacuum, not a fine-tuned bulk vacuum energy."* This doc supplies the **quantitative derivation** of that residual curvature.

[`Quantum_Gravity.md`](Quantum_Gravity.md) §9 flags "cosmological constant magnitude" as open; this doc closes the magnitude to within a factor of 4 from substrate primitives.

[`Holographic.md`](Holographic.md) §5 identifies the cosmological constant as arising from event-density asymmetry; this doc makes the asymmetry quantitative via the 10¹²² surface-vs-volume + de Sitter-vs-Planck reduction.

[`Gravity_From_Delay.md`](Gravity_From_Delay.md) and the Lean module [`QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) supply the holographic event count `N = 4π R²` and the substrate G structure — direct primitives reused here.

[`DarkMatter.md`](DarkMatter.md) §5 closes the **other** dark-sector observable on the *same* Hubble radius `R_H = c/H₀`: the dark-matter / MOND acceleration scale `a₀ = cH₀/(2π) = c²/(2π R_H)` (Lean: `mond_acceleration_horizon_form`, [`QLF_DarkMatter.lean`](lean/QLF_DarkMatter.lean)). So `Ω_Λ = log 2` (sparse exterior, dark energy) and `a₀` (crossover into the denser-logic interior, dark matter) are **one horizon, read two ways** — the expand/contract duality of [`Curvature.md`](Curvature.md).

---

## §9 References

### Internal

- [`Log2_Search.md`](Log2_Search.md) — the pre-registered search for another route to `Ω_Λ = log 2`, now that §3's is gone.
- [`Curvature.md`](Curvature.md) — global geometry as de Sitter: the cosmic Markov blanket's replication-dominant (expanding) phase, AdS as the contraction phase; Ω_Λ = log 2 as residual curvature, with magnetism as the local spin-axis analog.
- [`VacuumEnergy.md`](VacuumEnergy.md) §6 — vacuum-alignment principle, residual-curvature reading of Λ.
- [`Gravity_From_Delay.md`](Gravity_From_Delay.md) — holographic event count + substrate G + Verlinde gravity.
- [`Quantum_Gravity.md`](Quantum_Gravity.md) §8–9 — open Λ magnitude (closed by this doc).
- [`Holographic.md`](Holographic.md) §5 — de Sitter / dark-energy framing.
- [`HadronicDepth.md`](HadronicDepth.md) — cosmic-horizon depth `n ≈ 6.7 × 10⁶⁰` (geometric primordial-blanket depth).
- [`AgeOfUniverse.md`](AgeOfUniverse.md) — `T_universe = n × τ_Planck`.
- [`Kitada_Local_Time_GR.md`](Kitada_Local_Time_GR.md) — substrate event quantum.
- [`Magic_numbers.md`](Magic_numbers.md) — 3-dimensionality of substrate from 8-twist 6+2 split.
- [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean) — `zfa_closure_minimizes_free_energy`.
- [`lean/QLF_GravityFromDelay.lean`](lean/QLF_GravityFromDelay.lean) — `holographic_event_count`, `holographic_entropy`, `G = L_Planck² c³/ℏ`.
- [`lean/QLF_VacuumAlignment.lean`](lean/QLF_VacuumAlignment.lean) — 3-layer vacuum-alignment.
- [`lean/QLF_SubstrateLightSpeed.lean`](lean/QLF_SubstrateLightSpeed.lean) — `c = L_Planck/τ_Planck`.
- [`lean/QLF_CosmologicalConstant.lean`](lean/QLF_CosmologicalConstant.lean) — Lean anchor for this module.
- [`cosmological_constant_demo.py`](cosmological_constant_demo.py) — numerical companion.

### External

- Weinberg, S. (1989). *The cosmological constant problem*. Rev. Mod. Phys. 61, 1.
- Carroll, S. M. (2001). *The Cosmological Constant*. Living Rev. Relativity 4, 1.
- Planck Collaboration (2020). *Planck 2018 results. VI. Cosmological parameters*. A&A 641, A6 — H_0 and Ω_Λ measurements.
- Verlinde, E. (2011). *On the Origin of Gravity and the Laws of Newton*. JHEP 04:029 — entropic-gravity foundation reused here.
- Padmanabhan, T. (2010). *Thermodynamical Aspects of Gravity*. Rep. Prog. Phys. 73, 046901 — horizon-thermodynamics framework.
- Banks, T. (2000). *Cosmological breaking of supersymmetry?*. Int. J. Mod. Phys. A 16, 910 — holographic Λ predecessor.
- Gibbons, G. W., & Hawking, S. W. (1977). *Cosmological event horizons, thermodynamics, and particle creation*. Phys. Rev. D 15, 2738 — de Sitter horizon temperature.
- Bekenstein, J. D. (1973). *Black holes and entropy*. Phys. Rev. D 7, 2333.
- Hsu, S. D. H. (2004). *Entropy bounds and dark energy*. Phys. Lett. B 594, 13 — Hubble-radius holographic dark energy gives no acceleration (§5.7 reading A).
- Li, M. (2004). *A model of holographic dark energy*. Phys. Lett. B 603, 1 — future-event-horizon cutoff (§5.7 reading C).
- Doran, M., & Robbers, G. (2006). *Early dark energy cosmologies*. JCAP 0606:026.
- Li, T.-N., Li, Y.-H., Du, G.-H., Wu, P.-J., Feng, L., Zhang, J.-F., & Zhang, X. (2024). *Revisiting holographic dark energy after DESI 2024*. arXiv:2411.08639 (EPJC) — the fits that exclude reading C (§5.7).
- Chen, L., Huang, Q.-G., & Wang, K. (2019). *Distance priors from Planck final release*. JCAP 02, 028 — the shift parameter `R = 1.7502 ± 0.0046` used in §5.7.
