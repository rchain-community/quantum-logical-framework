# Lepton generations as a Fourier signal — Koide's 2/3 as a power balance

The charged-lepton results from 2026-10-18, stated with the epistemic labels of
[`ScientificApproach.md`](ScientificApproach.md). The background and the open phase `Δ` are in
[`Weak_Force.md`](Weak_Force.md) §5–§5c⁗; the Lean anchors are
[`lean/QLF_Koide.lean`](lean/QLF_Koide.lean) and [`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean).

Rule applied throughout: assume only that nature is logical. QLF's construction is one model, not
a premise.

**Credit.** Koide found `Q = 2/3` (1981–83). Foot gave the 45° form (1994). Brannen found the phase
`δ ≈ 2/9` (2006). Barut's `Σk⁴` mass formula (1979) appears in §5 as the closest counting rule.

## 1. Koide's relation is a Fourier statement — **Proved**

Treat the three √-masses `s_k = √m_k` as a signal over the three generations and take its
discrete Fourier transform. It has one constant mode and one harmonic, and transforming back gives

    √m_k = M (1 + A·cos(δ + 2πk/3)),     k = e, μ, τ.

This form restricts nothing, because every triple of positive numbers has it. So `Q = 2/3` is not
*derived* from `A² = 2`; it **is** `A² = 2` in Fourier coordinates (`koide_three_phase_iff`). The
earlier reading "forced by the two transverse axes" is an identification. Taken per axis (equal
power on each of three axes), it would give `A² = 4` and `Q = 1`, which is wrong.

The basis-free content (`koide_iff_equal_power`):

> **`Q = 2/3` ⇔ the constant (generation-blind) mode and the harmonic (generation-distinguishing)
> mode carry equal power** ⇔ the √-mass vector sits at 45° to `(1,1,1)`.

Measured (PDG masses): constant-mode power 941.523, harmonic power 941.506, ratio **0.99998**.
The angle is 44.9999°. Reproduce with [`lepton_fourier_generations.py`](lepton_fourier_generations.py).

**Open bridge:** why nature splits the power 50/50 between "same for every generation" and
"different per generation". An unbiased one-bit choice between the two sectors has that shape, but
nothing yet connects a closure bit to this split.

## 2. The hierarchy is interference, not a large count — **Proved (given §1)**

At equal power the harmonic is `√2` times the constant mode, so `1 + √2·cos θ` has a zero, and one
generation sits 2.3° from it: the electron. The `~3500×` spread is near-cancellation, quadratically
amplified (Weak_Force §5c⁗ item 1 has the geometry). This is why every counting rule in §5 fails at
the electron. A count of possibilities cannot land on a near-cancelled remainder, and ratios taken
against `m_e` inherit that.

## 3. The phase is not an integer Fourier datum — **Rejected route**

The remaining number is the harmonic's phase, `δ = 0.22223` rad (`Δ = 3δ ≈ 2/3`). An inverse
Fourier transform of *integer* data over three slots has phases equal to the arguments of
Eisenstein integers `p + qω`. The smallest one matching `δ` to `10⁻⁵` is `−439 + 1463ω`, which
costs about 22 bits against about 3 bits for the constant `2/3`. That is a re-encoding, not a
derivation (the description-length criterion of Weak_Force §5c⁗). Mod-9 and other finite-group
structures give rational turn-fractions, and `Δ` is `1/(3π)` of a turn, so they are excluded too.

## 4. Stability and decay: 2 modes vs 3 or more

**Twist-built closures are periodic — Proved.** `twist_fold_pow_four`: the matrix fold `W` of any
twist history satisfies `W⁴ = I` (by `nf_decomp`, a fourth-root-of-unity phase times an axis matrix
that squares to `I`). So a closure made only of twists repeats exactly and can never be chaotic,
whatever the number of axes. Decay therefore needs something outside this finite group, such as a
stretching step or a coupling to a continuum of lighter states.

**Generic equal-weight modes — Numerical evidence (not a QLF derivation).** Model: `N` identical
nonlinear modes, all coupled to each other (the discrete self-trapping equation; the `N = 2` dimer
is integrable, Eilbeck, Lomdahl & Scott 1985). The modes start with equal power and random phases,
32 runs per setting.

| nonlinearity g | 2 modes chaotic | 3 modes chaotic | 4 modes chaotic |
|---|---|---|---|
| 0.5 | 0/32 | 0/32 | 26/32 |
| 2 | 0/32 | 1/32 | 31/32 |
| 4 | 0/32 | 14/32 | 32/32 |
| 10 | 0/32 | 25/32 | 32/32 |

Leak into a weakly coupled, off-resonant extra mode (a stand-in for neutrino emission; the linear
level is about 10⁻⁴). The table gives the time-averaged power the extra mode ends up holding:

| g | 2 active (of 3): median / max | 3 active (of 4): median / max |
|---|---|---|
| 0.5 | 1.9e-4 / 7.6e-4 | 1.2e-4 / 9.0e-4 |
| 4 | 1.3e-4 / 4.6e-4 | 7.4e-5 / 1.2e-2 |
| 10 | 7.6e-5 / 3.9e-3 | 2.9e-3 / 5.6e-2 |

So 2 equal modes never go chaotic, while 3 (or 3 active out of 4) *may*, and the chaotic runs push
10–100× more power into the extra mode. That supports "a 2-mode closure is stable, a 3-mode closure
may decay" as a hypothesis worth deriving inside QLF. It does not derive it, and it gives no
lifetimes. **Kill test:** a QLF version must reproduce the measured `τ_τ/τ_μ = 1.32 × 10⁻⁷`, which
is the `m⁵` law times the τ's 17.8% `eνν` branch (291 fs predicted, 290.3 fs measured). Scripts:
[`lepton_modes_decay_sim.py`](lepton_modes_decay_sim.py), [`lepton_modes_spectrum.py`](lepton_modes_spectrum.py),
[`lepton_three_of_four.py`](lepton_three_of_four.py).

## 5. Counting rules tried and failed — **Rejected routes**

The electron, muon and tau were taken as `d` = 2, 3, 4 dimensions of possibility, as 3-axis views
from `d` axes, and with time added (`d` = 4, 5, 6). Each rule had one constant fitted to `m_μ/m_e`
and then predicted `m_τ`. The data need the second log-step to be only 0.53 of the first, and none
of the rules delivers that:

| rule | best predicted m_τ (measured 1776.86 MeV) |
|---|---|
| `d^k`, `(2d)^L` walk counts | 4643 MeV (+161%) |
| closed lattice walks, no fit | 2589 MeV (+46%) |
| 3-axis views added per view (d = 2, 3, 4) | 421–842 MeV (−53 to −76%) |
| with time (d = 4, 5, 6), best case | −22% (added) / +102% (multiplied) |
| Barut 1979, `1 + (3/2α)Σk⁴`, no free parameter | 1786.15 MeV (+0.52%, ~80σ) |
| Koide, same inputs | 1776.97 MeV (+0.006%, 0.9σ) |

Scripts: [`lepton_dimension_counting.py`](lepton_dimension_counting.py),
[`lepton_three_at_a_time.py`](lepton_three_at_a_time.py), [`lepton_with_time.py`](lepton_with_time.py).
§2 says why: the electron is a cancellation, not a count.

## 6. Status

| claim | status |
|---|---|
| `Q = 2/3` ⇔ `A² = 2` ⇔ equal Fourier power ⇔ 45° | Proved (`koide_three_phase_iff`, `koide_iff_equal_power`) |
| `Q = 2/3` derived from "two transverse axes" | Withdrawn: identification only; the per-axis reading gives `Q = 1` |
| hierarchy = near-cancellation | Proved given `A² = 2` |
| twist-only closures are periodic (`W⁴ = I`) | Proved (`twist_fold_pow_four`) |
| 2 modes stable, 3+ may decay and leak | Numerical evidence, generic model |
| why equal power; the phase `Δ = 2/3`; lifetimes from closures | Open |
