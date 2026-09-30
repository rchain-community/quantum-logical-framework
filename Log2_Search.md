# Can `Ω_Λ = log 2` be derived? A pre-registered search

The observed dark-energy fraction, Planck `Ω_Λ = 0.685 ± 0.007`, sits within 1.2σ of `log 2 = 0.6931`.
QLF's original derivation of that value is gone
([`Cosmological_Constant.md`](Cosmological_Constant.md) §5.7–§5.8,
[`Gravity_From_Delay.md`](Gravity_From_Delay.md) §9a). This doc asks whether another route derives it.

**The framing, as for α** ([`Alpha_Residual.md`](Alpha_Residual.md) §9j–§9k). `log 2` is a natural mode:
it arises from counting in many independent ways (one bit in nats; `1 − ½ + ⅓ − …`; `Σ 1/(k·2ᵏ)`; one
octave `∫ dω/ω` of a `1/ω` spectrum; the half-life of a memoryless decay). The measured value is another
way. A fit is one way ([`CLAUDE.md`](CLAUDE.md) review note 6), not evidence for any particular mechanism,
and the more ways a number arises the less a match singles one out.

**What any derivation must do.** The data favor a constant `Λ`, and then `Ω_Λ` drifts from 0 to 1. So a
derivation must (a) output `log 2` without it as an input; (b) select our epoch; and (c) make a second
prediction that could fail. Note on (c): in a flat constant-`Λ` universe, `Ω_Λ(t₀) = log 2` alone fixes
`q₀ = −0.540` and `H₀t₀ = 0.958`. Those test the *number*, and every mechanism that gives `log 2` shares
them, so they cannot distinguish one mechanism from another. A mechanism needs a prediction of its own.

---

## Route 1: the octave route — *pre-registered 2026-09-30*

**Setup.** Flat universe with matter and a constant `Λ`, radiation neglected (the epochs in question are
late). Then `Ω_Λ(t) = tanh² x`, `H = H∞ coth x`, `a ∝ sinh^{2/3} x`, with `x = (3/2)H∞ t`. An *octave
condition* compares the universe at age `t` with age `t/2`.

**Pre-registered statements and forecasts** (checked by [`omega_lambda_octave.py`](omega_lambda_octave.py)):

| | Condition | Meaning | Forecast |
|---|---|---|---|
| O1 | `a(t) = 2·a(t/2)` | the universe doubled in size over its last doubling of age | selects `Ω_Λ = 8/9`, not `log 2` |
| O2 | `H(t/2) = 2·H(t)` | the scale-free law `H ∝ 1/t` holds across the last octave | holds only as `t → 0` (matter era); no epoch with `Λ` present |
| G | any algebraic relation among hyperbolic functions of `x` and `x/2` | the whole class of octave conditions | selects an **algebraic** `Ω_Λ`, so never exactly `log 2`, which is transcendental (Hermite–Lindemann) |
| O4 | `Ω_Λ(t₀) = ∫_ω^{2ω} dω′/ω′` | identification: the dark-energy share *is* the e-fold weight of one octave | gives `log 2` by construction; stands only with a derivation and a second prediction |

**Why G holds.** Put `u = tanh(x/2)`. Then `tanh x`, `coth x`, `sinh x / sinh(x/2) = 2cosh(x/2)` and
`a(t)/a(t/2)` are all algebraic in `u`. So a nondegenerate algebraic condition gives algebraic `u`, and
`Ω_Λ = tanh² x = 4u²/(1+u²)²` is algebraic. The closed forms for O1 and O2 were worked out while framing
this route; the script checks them numerically. The forecasts are recorded here so the result is not
chosen after the fact.

**Kill conditions.** O1, O2 and the class G count as a derivation only if they select `Ω_Λ = log 2`
exactly. G says they cannot, so the forecast is that the epoch-condition form of the octave route fails.
O4 counts only if (i) the identification of a *density fraction* with an *octave weight* is derived, with
every factor derived and none chosen to fit, and (ii) it makes a prediction beyond `q₀` and `H₀t₀`. Without
both, O4 is recorded as a restatement of the fit.

**What would change the forecast.** G covers conditions built from `x` and `x/2` through hyperbolic
functions. A condition that involves the elapsed time or the e-fold count *linearly* (for example
`H·t = 1`) is outside G and can give transcendental values. Such conditions are not octave conditions and
belong to a later route.

**Result (2026-09-30): the forecasts held.** Running [`omega_lambda_octave.py`](omega_lambda_octave.py)
after the pre-registration commit (`ef02335`):

| | Result |
|---|---|
| O1 | `Ω_Λ = 0.888889 = 8/9` exactly (`q = −0.833`, `H·t = 1.247`), 28σ from Planck |
| O2 | `H(t/2)/H(t)` falls from `2` at `x → 0` to `1.648` at `Ω_Λ = 0.58` and `1.013` at `Ω_Λ ≈ 1`. It is below 2 at every sampled epoch with `Λ` present |
| G | the `u = tanh(x/2)` identities hold to `2 × 10⁻¹⁵`, so the algebraicity argument stands |
| O4 | `log 2` by construction, at `q₀ = −0.540`, `H₀t₀ = 0.958`, 1.2σ from Planck |

**Verdict on Route 1.** The epoch-condition form of the octave route is **closed**: no octave condition
on a flat constant-`Λ` history can select `log 2`, and the two natural ones select `8/9` and nothing.
O4 is **recorded as a restatement of the fit**. It has no derivation yet, and its only predictions are the
shared `q₀` and `H₀t₀`.

**What an O4 derivation would have to supply.** `∫_ω^{2ω} dω/ω = log 2` is a measure in e-folds, not a
fraction of a whole, so O4 needs a normalization that turns it into one. Three standard ways `log 2`
appears as a genuine *fraction* are candidates for later routes. Each would need its own physical mapping
and its own second prediction:

1. **A log-uniform quantity spanning one e-fold** puts the fraction `log 2` in its lowest octave. This
   needs a reason for the one-e-fold span.
2. **Half-life over mean lifetime**: `T½/τ = log 2` for any memoryless decay. This is the closest to the
   "half kept locally, half lent to the future" picture (`Cosmological_Constant.md` §5.7), if the lent
   share decays with a constant hazard.
3. **Geometric halving with harmonic weight**: `Σ 2⁻ᵏ/k = log 2` is the expected `1/k` when each step
   passes on half (the census's Kraft weighting). This needs a derived reason for the `1/k`.

Conditions outside G, which involve the elapsed time linearly (like the two-clock agreement `H·t = 1`,
reached at `Ω_Λ = 0.737`), are a separate route. At `Ω_Λ = log 2` the two clocks read `H·t = 0.958`, which
is not a natural value, so that route also needs a new idea rather than a known marker.

---

## Route 2: the half-life route — *pre-registered 2026-09-30*

**The idea.** "Each event creates energy; about half is kept locally, and half is lent to the future and
realized later" ([`Cosmological_Constant.md`](Cosmological_Constant.md) §5.7). For any memoryless decay,
half-life over mean lifetime is `T½/τ = log 2`. Can the lent share, as a density fraction, come out as
`log 2`?

**The model** (checked by [`omega_lambda_halflife.py`](omega_lambda_halflife.py)). Flat universe, two
ledgers: matter (`w = 0`) and a lent ledger (`w = −1`). Energy is created at rate `Q = γ H ρ_c`, with
`ρ_c` the critical density. That is self-similar, and `γ` is its strength. Half goes to matter, half to
the lent ledger. The lent ledger is realized into matter with hazard `k/t`: `k = 1` is "half per octave"
measured in the observer's own clock, and `k = log 2` is "half per e-fold of age". In own-clock time
`τ = ln t`, with `h = Ht`:

    dΩ/dτ = (γ/2)·h − k·Ω + 3h·Ω(1 − Ω)
    dh/dτ = h − (3/2)·h²·(1 − Ω)

**Pre-registered forecasts** (worked out while framing; the script integrates the equations to check them):

| | Statement | Forecast |
|---|---|---|
| H1 | `k = 1` (half per octave), any `γ > 0` | no steady share: `Ω_Λ → 1` and `h → ∞`, the de Sitter attractor |
| H2 | `k = log 2` (half per e-fold) | same as H1: `Ω_Λ → 1` |
| H3 | steady shares need `k > 2`, and then `Ω` solves `γ/(3(1 − Ω)) = (k − 2)Ω` | depends on the free `γ`, so it is not a derivation of any number |
| H4 | any steady share is the same at every epoch | excluded by the early-epoch data whatever its value (§5.7), like P5 of `QLF_InflationObserver` |

**Why `log 2` does not appear as the share.** In this model `log 2` can only enter as a rate (`k`). The
share it produces is set by `k` and `γ` through an algebraic fixed-point condition, not by `T½/τ`.

**Also recorded.** Creating energy at rate `Q` violates total `∇^μ T_μν = 0`, which the Einstein
equations require (`QLF_BianchiClosure` takes it as a hypothesis). So this model is outside GR as it
stands, the same unproved step as the continuity equation of §5.7.

**Kill condition.** The route counts only if some version yields a density share of exactly `log 2`
that (a) selects our epoch rather than holding at every epoch, (b) has no free rate chosen to fit, and
(c) makes a prediction beyond `q₀` and `H₀t₀`.

**Result (2026-09-30): the forecasts held.** Running [`omega_lambda_halflife.py`](omega_lambda_halflife.py)
after the pre-registration commit (`f46394a`):

- **H1 and H2:** for `k = 1` and `k = log 2`, at `γ = 0.01, 0.1, 1`, the lent share runs to `Ω = 1` and `H·t`
  diverges within 15–24 own-clock e-folds: the de Sitter attractor, as §5.8 found by another route.
- **H3:** steady shares exist only for `k > 2` and small `γ`. Examples: `k = 3, γ = 0.1 → Ω = 0.0345`;
  `k = 4, γ = 1 → Ω = 0.2113`; for larger `γ` there is no steady share and `Ω → 1`. The integrated runs
  land on the fixed points. The share moves with the free `γ`.
- **H4** is structural: a steady share is epoch-independent, so it fails the early-epoch test whatever
  its value.

**Verdict on Route 2: closed in this form.** "Half kept, half lent" with memoryless realization either
runs to pure de Sitter (half per octave, or per e-fold) or gives a share set by a free creation rate.
`log 2` enters only as a rate. A version that works would need a lent ledger that dilutes (`w > −1`) or a
realization rate tied to something other than the age, and it would still have to fix our epoch.

---

## Route 3: a drifting Planck tick — *pre-registered 2026-09-30*

**The idea.** If Planck's constant changes with time, then the tick `τ_P = √(ħG/c⁵)` drifts. Age counted
in ticks then differs from cosmic time, and your two ages, `1/H₀` (own clock) and 13.8 Gyr (cosmic),
might both be right.

**What "`ħ` changes" can mean.** Only dimensionless variation is observable (Duff 2002). The tick measured
against an atomic clock is `τ_P/τ_atomic = α²·√(Gm_e²/ħc)`. So a drift of the tick shows up as a drift
of `α`, of the gravitational coupling, or both.

**Pre-registered statements** (checked by [`tick_drift.py`](tick_drift.py)):

| | Statement |
|---|---|
| T1 | with `τ_P ∝ t^β`, the age in ticks times today's tick is `t₀/(1 − β)` |
| T2 | making that equal `1/H₀` requires `β = 1 − H₀t₀`: `0.049` for Planck ΛCDM, `0.042` if `Ω_Λ = log 2` |
| T3 | the drift today is `β/t₀ ≈ 3.5 × 10⁻¹²/yr`. Through `α` alone that is `α̇/α ≈ 1.8 × 10⁻¹²/yr`, against the optical-clock bound `1.0(1.1) × 10⁻¹⁸/yr` (Lange et al. 2021). Through gravity alone it is `≈ 7 × 10⁻¹²/yr`, against the lunar-ranging bound `Ġ/G = (7.1 ± 7.6) × 10⁻¹⁴/yr` (Hofmann & Müller 2018) |
| T4 | a drift of either size cannot turn a count into an O(1) share like `log 2`; at most it shifts which epoch is "now" |

**Forecast.** Excluded, by about `10⁶` through `α` and about `100×` through gravity. QLF also claims
`α_G = exp(−28π)` as a derived constant (`Gravity.md` §4a), which would itself forbid a drift through the
gravitational sector.

**Kill condition.** The route survives only if a drift within the bounds reconciles the two ages or
yields `log 2`. The forecast is that neither happens.

**Result (2026-09-30): the forecasts held.** Running [`tick_drift.py`](tick_drift.py) after `f46394a`:

- **T1:** direct integration matches `t₀/(1 − β)`: `β = 0.049` turns 13.80 Gyr of cosmic time into
  14.51 Gyr of ticks × today's tick, which is `1/H₀`.
- **T2:** `β = 0.0493` (Planck ΛCDM) or `0.0420` (`Ω_Λ = log 2`).
- **T3:** the required drift today is `3.6 × 10⁻¹²/yr` (ΛCDM) or `3.0 × 10⁻¹²/yr` (`log 2`). Through `α`
  alone that is `α̇/α ≈ 1.5–1.8 × 10⁻¹²/yr`, about `7–8 × 10⁵` times the optical-clock limit. Through
  gravity alone it is `≈ 6–7 × 10⁻¹²/yr`, `79–93σ` from the lunar-ranging value.
- **T4:** a drift of this size shifts which epoch is "now"; it does not create an O(1) share.

**Verdict on Route 3: excluded.** A drifting Planck tick could in principle make both ages true, with the
age in ticks equal to `1/H₀` and the cosmic age equal to 13.8 Gyr. The drift that would take is ruled out
by atomic clocks and lunar ranging by large factors. So the two ages stay different quantities, and
`H₀t₀ ≠ 1` stands as a measured fact about the expansion history, not a clock artefact. Allowed drifts
(below `~10⁻¹³/yr` through gravity) change the tick-count age by less than `0.2%` over a Hubble time.

---

## Where the search stands

| Route | Status |
|---|---|
| 1. Octave, as an epoch condition | closed (no algebraic octave condition can give `log 2`) |
| 1. Octave, as an identification (O4) | a restatement until derived |
| 2. Half-life (memoryless lent share) | closed in its natural form (de Sitter attractor, or a free rate) |
| 3. Drifting Planck tick | excluded by atomic clocks and lunar ranging |
| Remaining | log-uniform over one e-fold; `Σ 2⁻ᵏ/k` with a derived `1/k`; conditions linear in time |

The common thread: every route that gives the *same* share at every epoch is excluded by the early
universe. Every route that selects an epoch needs a time scale that QLF does not yet supply without
putting in the age itself.

---

## Route 4: log-uniform over one e-fold, by a local clock — *pre-registered 2026-09-30*

**The idea** (Jim, 2026-09-30): `log 2` may hold at *any* time when read by a local clock. The natural
local clock is log-time `τ = ln t`, the observer's own clock of #164, in which every epoch looks the same.
A quantity spread evenly in `τ` over one e-fold has the fraction `log 2` in its top octave.

**Pre-registered statements** (checked by [`omega_lambda_local_clock.py`](omega_lambda_local_clock.py)):

| | Statement | Status before running |
|---|---|---|
| L1 | in any observer's last e-fold of own-clock time (`t/e` to `t`), its last doubling of age (`t/2` to `t`) takes up exactly `log 2`, at every epoch | an identity: bookkeeping by rule 4, stated as the anchor |
| L1′ | L1 is the same number as Route 2's `T½/τ`: half per octave means a mean lifetime of one e-fold | an identity |
| L2 | a ratio of energy densities at one event, including `Ω_Λ = ρ_Λ/ρ_total`, is unchanged by relabelling time | so no local clock makes `Ω_Λ` itself `log 2` at every epoch; L1's `log 2` is a ratio of *durations* |
| L2′ | the naive own-clock substitute `Ω_τ = ρ_Λ/(3H_τ²/8πG)` with `H_τ = d ln a/dτ = H·t` is `Ω_Λ/(Ht)²` | forecast: it varies with epoch, so it is not `log 2` at every epoch either, and it is not a density fraction (the shares no longer sum to 1) |
| L3 | the measured `0.685` is a density ratio, inferred from `H(z)` | forecast: linking it to L1 needs the two to coincide, and with a constant `Λ` they coincide at one epoch only (`q = −0.540`). So the route does not remove the "why now" |
| L4 | two observable duration fractions of the last e-fold of our own clock, in Planck ΛCDM: (a) the share spent accelerating (`q < 0`); (b) the share with `ρ_Λ > ρ_m` | no forecast. A match to `log 2` would be one way, not a derivation, because these fractions change with epoch |

**Kill condition.** The route derives the measured `Ω_Λ` only if it gives a *density* share of `log 2`
that holds at our epoch without being tuned, and that survives the early-epoch test. L2 says no local
clock can do that for `Ω_Λ` itself. So the forecast is that Route 4 yields a true every-epoch clock identity
(L1) but not the measured dark-energy fraction.
