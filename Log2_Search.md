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
