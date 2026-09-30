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

**Result (2026-09-30).** Running [`omega_lambda_local_clock.py`](omega_lambda_local_clock.py) after the
pre-registration commit (`fb9cddf`):

- **L1, L1′ hold**, as identities: last octave / last e-fold `= 0.693147180560` at `t = 10⁻⁴⁰` through
  `10¹⁰`, and it equals `T½/τ` for half-per-octave decay. This is the one sense in which `log 2` holds at
  every time by a local clock. It is a ratio of durations.
- **L2 holds:** `ρ_Λ/ρ_total` at today's event is `0.6847` whichever clock labels the event.
- **L2′ as forecast:** `Ω_τ = Ω_Λ/(Ht)²` varies, from `0.210` at `Ω_Λ = 0.1` to `0.758` today and `0.428`
  at `Ω_Λ = 0.95`, and it is not a density fraction.
- **L3 as forecast:** `Ω_Λ = log 2` happens once, at `q = −0.540`, `H·t = 0.958`.
- **L4:** of our last own-clock e-fold, `0.583` was spent accelerating (acceleration began at 7.70 Gyr) and
  `0.292` with `ρ_Λ > ρ_m` (from 10.31 Gyr). Neither is `log 2`.

**Exploratory, not pre-registered.** L2′'s `Ω_τ` peaks near today. The peak is where `sinh 2x = 4x`, at
`Ω_Λ = 0.634` (`q = −0.451`, `Ω_τ = 0.764`), about 7σ from Planck. So "now is when the own-clock
dark-energy share peaks" is also ruled out. It is recorded so that nobody rediscovers it as a hit.

**Verdict on Route 4.** Your reading is right in one precise sense: in log-time, `log 2` is the share of
an observer's last e-fold taken by its last doubling of age, at every epoch. It is also exactly the
half-life-to-mean-life ratio of half-per-octave decay, so Routes 1, 2 and 4 meet at one identity:
**octave / e-fold `= T½/τ = log 2`**. But that is a ratio of durations. The measured `0.685` is a ratio of
densities, which no clock can change (L2). So the route explains why `log 2` is natural on a local clock.
It does not derive the dark-energy fraction, and the "why now" remains: the two coincide at one epoch only.

---

## Where the search stands

| Route | Status |
|---|---|
| 1. Octave, as an epoch condition | closed (no algebraic octave condition can give `log 2`) |
| 1. Octave, as an identification (O4) | a restatement until derived |
| 2. Half-life (memoryless lent share) | closed in its natural form (de Sitter attractor, or a free rate) |
| 3. Drifting Planck tick | excluded by atomic clocks and lunar ranging |
| 4. Log-uniform one e-fold, local clock | `log 2` holds at every epoch as a *duration* ratio (identity); does not reach the *density* ratio |
| 5. Half kept, half lent, on a vacuum clock | no natural rate gives `log 2` (`0.718`, `0.794`); **the bridge `Ω_Λ = (H_Λ/H)²` survives** |
| 5 (fit). Interacting vacuum vs CMB + BAO + SN | `λ = 0.18 ± 0.14`, no significant preference over ΛCDM; `λ = 1` and `λ = 1.106` (attractor `log 2`) excluded at >5σ and >6σ |
| 6. A QLF reason for `√log 2` | none yet; **attractor theorem `Ω* = T/(3ρ_m)`**: the target is a derived transfer law whose stable attractor replaces `log 2` of matter's dilution loss |
| 7. Binary-closure clock + epoch selection | `√log 2` as the tick rate of a binary closure (identity); horizon-count peaks select `Ω_Λ = 0.586` and `1/3`, not ours |
| Remaining | `Σ 2⁻ᵏ/k` with a derived `1/k`; a mechanism that turns the octave/e-fold duration ratio into an energy share |

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

**After Route 4.** The four routes share a single `log 2`: the octave/e-fold ratio, which is also
half-life over mean life. The open problem is now sharper. Is there a mechanism that turns that
*duration* ratio into an *energy* share, and makes it hold at our epoch? For example, energy realized in
proportion to own-clock time spent. Any such mechanism must still pass the early-epoch test.

---

## Route 5: half kept, half lent, on a vacuum clock — *pre-registered 2026-09-30*

**The idea** (Jim, 2026-09-30): the vacuum energy determines the relative clock rate. Route 4's no-go
(L2) says a density ratio cannot be changed by relabelling time. That no-go is escaped if the clock
itself is set by the vacuum energy.

**The bridge (V0).** A clock set by the vacuum energy alone can tick only at a rate built from `G` and
`ρ_Λ`. The only such combination with units of 1/time is `√(Gρ_Λ)`, which is `H_Λ = √(8πGρ_Λ/3)`: the
expansion rate the vacuum alone would drive. In a flat universe, relative to the expansion clock `H`,

    Ω_Λ = (H_Λ / H)²

So once the clock is the vacuum's own, `Ω_Λ` *is* a clock statement: the square of the vacuum clock's
rate relative to the expansion clock. (A rate linear in `ρ_Λ` would need an extra scale with units, so
dimensional analysis rules it out.) Consequence: `Ω_Λ = log 2` means the vacuum clock runs at `√log 2 =
0.8326` of the expansion clock, the same number as reading C's `C` (`Cosmological_Constant.md` §5.7).

**The model** (checked by [`omega_lambda_vacuum_clock.py`](omega_lambda_vacuum_clock.py)). Matter
(`w = 0`) and a vacuum ledger (`w = −1`, the lent half). The lent energy is realized into matter with hazard
`λ·H_Λ`: at rate `λ` per unit of vacuum-clock time. Total `∇T = 0` holds (an interacting vacuum, energy
moving from the vacuum into matter), unlike Route 2. In e-folds of expansion `N = ln a`:

    dΩ/dN = −λ·Ω^{3/2} + 3Ω(1 − Ω)

**Pre-registered statements and forecasts** (fixed points worked out while framing; the script integrates):

| | Statement | Forecast |
|---|---|---|
| V1 | the attractor `Ω*` solves `λ√Ω* = 3(1 − Ω*)`; early on `Ω ∝ a³` as in ΛCDM | late-time attractor, so the early-epoch test is passed |
| V1a | `λ = 1`: mean realization time one unit of vacuum-clock time | `Ω* = (19 − √37)/18 = 0.7176` |
| V1b | `λ = log 2`: half realized per unit of vacuum-clock time | `Ω* = 0.794` |
| V1c | the `λ` that would give `Ω* = log 2` | `λ = 3(1 − log 2)/√log 2 = 1.106`, which is not a natural value |
| V2 | half kept locally, half lent: creation `Q = γ·H_Λ·ρ_c` split evenly | the attractor moves with the free `γ`, so it is not a derivation |
| V3 | "half per octave" of vacuum-clock *age* (hazard `H_Λ/τ_v`) | the hazard fades as `τ_v` grows, so `Ω → 1` (de Sitter) |

**What a pass would look like, and what it would predict.** A natural `λ` (no fitting) with `Ω* = log 2`.
Its own predictions would then be: no de Sitter end state (the future settles at `w_tot = −Ω*`); vacuum
energy decaying into matter today at rate `λ·H_Λ·ρ_Λ`, testable with interacting-dark-energy fits; and a
`Ω(z)` history that differs from ΛCDM near `z ~ 1`.

**Kill condition.** It is a derivation only if a natural `λ` gives `Ω* = log 2` exactly with no free
parameter. The forecast is that it does not (V1a–V1c). If so, what survives is V0: the bridge from a
density ratio to a clock-rate ratio.

**Result (2026-09-30).** Running [`omega_lambda_vacuum_clock.py`](omega_lambda_vacuum_clock.py) after the
pre-registration commit (`c78c1ed`):

| | Result |
|---|---|
| V1a | `λ = 1`: integrated from `Ω = 10⁻⁹` to `0.717624`, the closed form `(19 − √37)/18`. Early growth ×400 per 2 e-folds, the ΛCDM `a³` rate |
| V1b | `λ = log 2`: `Ω* = 0.794106` |
| V1c | `Ω* = log 2` needs `λ = 1.105703`, not a natural value |
| V2 | with creation (`λ = 1`): `γ = 0, 0.1, 0.5, 1, 2` gives `Ω* = 0.718, 0.711, 0.686, 0.662, 0.628`. `γ ≈ 0.5` lands near Planck, but `γ` is free: a fit, one way, not a derivation |
| V3 | starting from the self-consistent early solution (`Ω ∝ a²`, vacuum-clock age `τ_v = √Ω`): `Ω = 0.773, 0.948, 0.987, 0.998` at `N = 15, 20, 40, 160`. The hazard fades and `Ω → 1`, as forecast |

**Verdict on Route 5.** No natural repayment rate gives `log 2`: mean life one vacuum-clock unit gives
`0.718`, half-life one unit gives `0.794`, and `log 2` would need `λ = 1.106`. So "half kept, half lent" on
a vacuum clock does not derive the number either.

**What survives, and it is new: V0.** If the clock is set by the vacuum energy, then
`Ω_Λ = (H_Λ/H)²` exactly: the dark-energy fraction *is* the squared rate of the vacuum clock relative
to the expansion clock. That is the bridge Route 4 lacked, from a density ratio to a clock ratio, and it
comes from dimensional analysis alone. It turns the search into a clock question: **why would the vacuum
clock run at `√log 2 = 0.8326` of the expansion clock now?** The same number appeared as reading C's `C`,
where it was excluded as a *fixed* holographic constant (§5.7). Here it would be a present-day rate
ratio, a different claim.

**A model worth keeping, as one way.** V1 is a one-parameter interacting-vacuum model (vacuum decaying
into matter at `Q = λH_Λρ_Λ ∝ ρ_Λ^{3/2}`) with a late attractor instead of a de Sitter end state. With
`λ` fitted, it has as many parameters as ΛCDM, and different predictions: `w_tot → −Ω*` in the future and
energy flowing from vacuum into matter today. Whether data prefer it is a separate, testable question.

---

## Route 5 fit: the interacting vacuum against CMB + BAO + SN — *pre-registered 2026-09-30*

**The model.** Route 5's V1: vacuum energy (`w = −1`) decays into matter at `Q = λ·H_Λ·ρ_Λ`, with
`H_Λ/H = √Ω_Λ`. At `λ = 0` it is flat ΛCDM exactly, so the fit asks a nested question: do the data
prefer `λ ≠ 0`? Two values carry QLF meaning: `λ = 1` (mean realization time one vacuum-clock unit,
attractor `Ω* = 0.718`) and `λ = 1.106` (the attractor at `log 2`).

**Data** (checked by [`fit_interacting_vacuum.py`](fit_interacting_vacuum.py)):

- **CMB:** Chen, Huang & Wang 2019 distance priors, the wCDM set (`R = 1.7493`, `l_A = 301.462`,
  `ω_b = 0.02239`, with correlations), `z*` from their Hu–Sugiyama fit. `R` uses the early-time matter
  density, since the vacuum's transfer is negligible there (`Ω_Λ ∝ a³` early).
- **BAO:** DESI DR2 (arXiv:2503.14738) Table IV: BGS `D_V/r_d`, and `D_M/r_d`, `D_H/r_d` with correlations
  for LRG1, LRG2, LRG3+ELG1, ELG2, QSO and Lyα. `r_d` from DESI's eq. (2) (Brieden, Gil-Marín & Verde 2023).
- **SN:** Pantheon+ (Brout et al. 2022), `m_b_corr` for `z_HD > 0.01`, full STAT+SYS covariance, the
  absolute magnitude marginalized analytically.

**Pipeline checks, run first.** (A) DESI BAO alone in flat ΛCDM must give `Ω_m = 0.2975 ± 0.0086` and
`h·r_d = 101.54 ± 0.73 Mpc`. (B) Pantheon+ alone must give `Ω_m = 0.334 ± 0.018`. Each within its 1σ. If
either fails, the model fit is not run until the pipeline is fixed.

**Fits.** ΛCDM (`Ω_m, h, ω_b`) and the interacting vacuum (`+ λ`, free in `[−5, 5]`; `λ < 0` would move
energy from matter into the vacuum), on CMB + BAO + SN (primary) and CMB + BAO. Reported: best-fit
values, `Δχ² = χ²_ΛCDM − χ²_IV`, and the profile `Δχ²(λ)` with its 68% and 95% ranges.

**Decision rule.** The interacting vacuum is **preferred** if `Δχ² > 4` for its one extra parameter
(about 2σ), and otherwise **no preference**. A value of `λ` is **excluded at 95%** if its profile
`Δχ² > 3.84`. Applied to `λ = 0`, `λ = 1` and `λ = 1.106`.

**Forecast.** No numerical forecast. Recent analyses find DESI BAO mildly favoring dark energy that
weakens over time. A vacuum decaying into matter (`λ > 0`) has that character, so a mild preference for
`λ > 0` would not be surprising; whether it reaches `λ ≈ 1` is the question.

**Result (2026-09-30).** Running [`fit_interacting_vacuum.py`](fit_interacting_vacuum.py) after the
pre-registration commit (`0ce3cb9`):

*Pipeline checks passed.* (A) DESI BAO-only flat ΛCDM: `Ω_m = 0.2973 ± 0.0084`, `h·r_d = 101.55 Mpc`
(published `0.2975 ± 0.0086`, `101.54`). (B) Pantheon+ alone: `Ω_m = 0.3314 ± 0.018` (published
`0.334 ± 0.018`), from 1,590 supernovae with `z_HD > 0.01`.

| | CMB + BAO + SN (primary) | CMB + BAO |
|---|---|---|
| ΛCDM `χ²`, best fit | 1418.69; `Ω_m = 0.304`, `h = 0.685` | 13.30; `Ω_m = 0.303`, `h = 0.686` |
| interacting `χ²`, best fit | 1417.06; `Ω_m = 0.336`, `h = 0.678`, `λ = +0.18` | 13.23; `λ = −0.07` |
| `Δχ²` (ΛCDM − interacting) | 1.62: **no preference** | 0.07: **no preference** |
| `λ` | `+0.18 ± 0.14` (parabolic, from the profile); 95% grid range `[−0.07, +0.43]` | 95% grid range `[−0.57, +0.43]` |
| `λ = 0` (ΛCDM) | `Δχ² = 1.62`, allowed | `0.07`, allowed |
| `λ = 1` (attractor `0.718`) | `Δχ² = 31.3`, **excluded** | `17.6`, **excluded** |
| `λ = 1.106` (attractor `log 2`) | `Δχ² = 39.4`, **excluded** | `21.3`, **excluded** |

(At `λ ≥ 1.18` the profile fit did not converge; that is beyond every value the decision rule tests.)

**What it shows.** The data allow a vacuum slowly decaying into matter, with a mild, not significant
preference for it once supernovae are included (`λ ≈ 0.18`, about 1.3σ from ΛCDM). This is the same
direction as DESI's hints of weakening dark energy. At that `λ` the late-time attractor would be
`Ω* ≈ 0.94`, not pure de Sitter. The QLF-natural rates are **excluded**: `λ = 1` at more than 5σ and
`λ = 1.106`, the rate that would put the attractor at `log 2`, at more than 6σ. So this route to `log 2`
is closed by data, not only by naturalness. What survives from Route 5 is the vacuum-clock bridge
`Ω_Λ = (H_Λ/H)²`, and a slow interacting vacuum as one way the data allow.

---

## Route 6: a QLF reason for the `√log 2` clock ratio (2026-09-30)

**First, what the clock ratio is.** `H_Λ/H = √Ω_Λ` is an identity (V0). So a reason for the vacuum clock
running at `√log 2` of the expansion clock *is* a reason for `Ω_Λ = log 2`. The clock language is a
useful reframing, but by itself it supplies no mechanism.

**Three classes of mechanism.** Everything tried so far falls into one of three classes:

1. **Fixed at every instant** (a horizon count, a per-event ratio). The share is the same at every epoch,
   so it fails the early-epoch test whatever its value (§5.7; `QLF_InflationObserver` P5).
2. **Tied to an epoch** (octave conditions, a fixed half-life). This needs a time scale, and QLF has none
   to supply without putting in the age or `H₀`.
3. **A late-time attractor** (an interacting vacuum, Route 5). The share starts small (`Ω ∝ a³` early, as
   in ΛCDM) and settles to `Ω*`. Every late observer sees about `Ω*`, so "why now" becomes "why late",
   which observers existing only after structure forms answers. **This is the only class that passes
   both constraints without an input.** The target is therefore a law whose attractor is `log 2`.

**A general result for class 3.** Take any interacting vacuum: energy moves from the vacuum into matter
at rate `T` per e-fold, so `ρ_Λ′ = −T` and `ρ_m′ = −3ρ_m + T`. Then `Ω′ = −T/ρ_total + 3Ω(1 − Ω)`, and at
any fixed point

    Ω* = T / (3ρ_m)

**The late-time dark-energy share equals the fraction of matter's dilution loss that the vacuum
replaces.** This holds for every transfer law. Checked numerically for three repayment clocks (expansion
`T = λρ_Λ`, vacuum `T = λ√Ω·ρ_Λ`, vacuum²/expansion `T = λΩ·ρ_Λ`): each settles to a share equal to its
replaced fraction, to six digits.

**What that does to "half kept, half lent".** Read at the attractor, "the vacuum hands back half of
what dilution takes" gives `Ω* = 1/2`, not `log 2`. `log 2` is the replaced fraction when "half" is meant
*continuously*: `log 2` per unit is the continuous rate that halves over one unit (`e^{−log 2} = 1/2`),
the same octave/e-fold identity as Routes 1, 2 and 4. So `Ω* = log 2` would say: *at the attractor, the
vacuum refills matter at the continuous rate that halves per unit of dilution*. That is a precise
candidate. It is not yet a derivation, for two reasons:

- **It needs a derived transfer law `T(Ω)`**, not a stated fraction. A law that refills a fixed fraction
  `r` of the dilution loss makes `Ω = r` an *unstable* fixed point (`Ω′ = 3(1 − Ω)(Ω − r)`), so it cannot
  be the attractor. The natural stable laws above need `λ = 0.921, 1.106, 1.328` to put the attractor at
  `log 2`, and none of those is a natural value.
- **It needs a reason why the continuous form is the right reading of "half".**

**The Landauer reading, and why it fails.** One more QLF-native source: each QLF event realizes one bit,
at free energy `k_B T log 2` (`QLF_FreeEnergy`), while the continuum first law counts entropy in nats (`k_B T`
per unit). A vacuum clock ticking once per bit against an expansion clock ticking once per nat would run
at exactly `√log 2`. But this counts one bit per nat of horizon entropy, which is the overcount the first
law excludes (`QLF_HorizonFirstLaw`), and it is class 1, so it fails the early-epoch test as well.

**Where this leaves the search.** QLF has no reason yet for the `√log 2` clock ratio. The problem is
narrower than before, though: find a transfer law, derived from the substrate, whose stable late-time
attractor replaces `log 2` of matter's dilution loss. If one exists, its own predictions follow: no de
Sitter end state (`w_tot → −log 2`, `q → −0.540` in the future), and energy flowing from the vacuum into
matter today at `T = 3 log 2 · ρ_m` per e-fold. Both can be tested against interacting-dark-energy fits.

---

## Route 7: a binary-closure clock, and choosing the epoch by the most ways — *pre-registered 2026-09-30*

**Where the square root could come from (S1).** Take a clock that ticks when a binary closure completes,
each substrate step closing with probability ½. The number of steps to closure `K` is geometric, and the
clock's mean rate relative to the substrate clock is `E[1/K] = Σ_{k≥1} 2⁻ᵏ/k = log 2`. If energy is rate
(`E = hf`), that is an energy ratio of `log 2`, and Friedmann's `H ∝ √ρ` turns it into the clock ratio
`H_Λ/H = √log 2` (Route 5, V0). This is an identity. It is also the Route 1/2/4 octave/e-fold ratio, now
as a closure *rate*. As a per-event statistic it holds at every epoch, which the early-universe data
exclude (§5.7). So S1 can explain `log 2` only as the value at a *selected* epoch.

**Selecting the epoch by the most ways (S2).** QLF's rule is "what happens in the most ways happens first;
report the mode". QLF counts closures on horizons (the holographic count, `S ∝ A`). So the observed epoch
would be where the horizon's count of new closures peaks. Two versions, fixed here before computing, in
flat matter + constant `Λ` (`Ω_Λ = tanh²x`, `H = H∞ coth x`, `x = (3/2)H∞ t`), with Hubble-horizon
entropy `S ∝ H⁻²`:

| | Count | Peak condition |
|---|---|---|
| S2a | new horizon closures per own-clock e-fold, `dS/d ln t` | argmax over `x` |
| S2b | new horizon closures per unit cosmic time, `dS/dt` | argmax over `x` |

Checked by [`log2_epoch_selection.py`](log2_epoch_selection.py). **Decision rule.** A version *explains
"now"* if its peak `Ω_Λ` lies within 2σ of Planck (`0.685 ± 0.007`). It *derives `log 2`* only if the peak
is exactly `log 2` (a closed form). No forecast. Two versions are tested; a single match among them would
carry a look-elsewhere factor of two.

**Result (2026-09-30).** Running [`log2_epoch_selection.py`](log2_epoch_selection.py) after `bde65a4`:

- **S1 holds** as an identity: `E[1/K] = 0.693147180560 = log 2`, so a binary-closure clock runs at
  `√log 2 = 0.832555` of the substrate clock once `H ∝ √ρ` is applied. This is a QLF reason for the
  *square root* and for *`log 2` as a rate*.
- **S2a fails:** new horizon closures per own-clock e-fold peak at `Ω_Λ = 0.586`, 13.5σ from Planck.
- **S2b fails:** new horizon closures per unit cosmic time peak at `Ω_Λ = 1/3` exactly, the onset of
  acceleration (`q = 0`), 48σ from Planck.

**Verdict on Route 7.** QLF has a clean reason for the *form* of the clock ratio: a binary closure's mean
tick rate is `log 2`, and the Friedmann square root makes it `√log 2`. What it still lacks is a reason
for the *epoch*. Neither horizon count selects ours. The two ingredients are now separated: `log 2` as a
closure rate (derived, every-epoch), and a selection of "now" (open).

