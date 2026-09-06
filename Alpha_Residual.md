# The α residual `+0.036` — 137 is the exact leading EM value; the residual is higher-order EM running

> **Where it stands (§0):** `α⁻¹ = 128 + 9 = 137` is the *exact* leading pure-EM value — **matched** by
> the running (`128 = 2⁷ ≈ α̂⁻¹(M_Z)` to `0.05`, `+9 = 3²` = EM running to the IR). *Matched, not
> confirmed:* the comparison targets were known when the reading was built, so by
> [`ScientificApproach.md`](ScientificApproach.md) **R0a** this is a **retrodiction** — see §0a. The weak-sector
> hypothesis for `+0.036` was tested (W-loop running) and **closed** — the `W` is too heavy to run below
> `M_W` and on-shell `α(0)` has no separate `W` piece. The residual sits at the higher-order-EM scale
> (`~5α`), so `+0.036` is the **higher-order EM running** correction — the same object as the
> closure-resummation tail (§1–§4), in running language.

Companion to [`Alpha.md`](Alpha.md) and [`lean/QLF_AlphaBound.lean`](lean/QLF_AlphaBound.lean).
[Quantum Logical Framework (QLF)](README.md) derives the **leading** inverse coupling
`α⁻¹ = 2⁷ + 3² = 128 + 9 = 137` by construction, parameter-free
([`QLF_FineStructureSubstrate`](lean/QLF_FineStructureSubstrate.lean), `alpha_QLF_eq`). The measured
(CODATA, q²→0 Thomson) value is `α⁻¹ = 137.035999`. The residual `r = +0.035999` is the open piece.

**Binding discipline (the whole point of this file).** The residual must be *derived* from the
substrate, **never tuned** to CODATA. QLF is rich in meaningful constants (`3/8`, `5`, `2/3`, `π`, …),
so a coefficient that hits `0.036` within a percent can always be found by dividing the answer by a
substrate number — that is numerology, not physics. A weighting forced by the closure structure that
*then* gives `0.036` is physics; a weighting chosen to give `0.036` is not.

---

## 0. Reframe (leading hypothesis, per Jim): 137 is the *exact* EM value; the residual is a different sector

`α⁻¹` is not one number — it **runs** with energy. Measured: `α⁻¹(q²→0) = 137.036` (IR / Thomson) and
**`α⁻¹(q² = M_Z²) ≈ 128`** (the weak scale, precisely ~127.95). So QLF's `α⁻¹ = 2⁷ + 3² = 128 + 9` reads
as a *running*, with each integer pinned to a scale:

| QLF term | value | physical reading |
|---|---|---|
| `2⁷` | `128` | the coupling **at the weak scale** `M_Z` — the UV/bare value (`α⁻¹(M_Z) ≈ 128`) |
| `3²` | `+9` | the **electromagnetic** screening running `M_Z → q²→0` (3 spatial axes squared, charged-fermion EM) |
| sum | **`137`** | the **pure-EM** `α⁻¹` in the IR — **exact** |
| residual | `+0.036` | a **sub-leading, weak-scale** effect — the weak gauge bosons (W loops) in the photon vacuum polarization, where the bulk `+9` does not reach |

So **137 is the right leading EM number**, and the structure is quantitatively anchored.

**The running half matches.** `2⁷ = 128` matches `α̂⁻¹(M_Z)` (MS-bar) to `0.05`, and the gap to the
IR is `137.036 − 127.95 = 9.086 ≈ +9`. So `128 + 9 = 137` is *literally* "weak-scale coupling + EM
running = pure-EM IR". This is real, not a coincidence.

**The "weak residual" half was TESTED (swing #1, the W-loop running) and does NOT survive:**
- The `W` is integrated out below `M_W ≈ 80 GeV`, so it contributes **zero** to the `M_Z → q²→0` running
  that builds the IR value (its only window `M_W→M_Z` gives `~0.07–0.28` — wrong size and place).
- On-shell `α(0)` has `Π(0) = 0` by renormalization — **no separate `W` piece** sits inside `137.036`.
- The scale of `0.036` is `≈ 5α` — a **higher-order QED** scale (`(α/π)·9 ≈ 0.021`, 2-loop `≈ 0.027`),
  i.e. the next-order piece of the *electromagnetic* running, not a weak contribution.

**So the sector is electromagnetic after all** — `0.036` is the **higher-order EM running** correction to
the leading `+9`. Crucially, *that is the same object* the closure-census program (§1–§4) computes: "which
partial resummation of the prime-closure series" ≡ "the higher-order QED running correction to `+9`". So
§1–§5 are **not** demoted to the wrong sector — they are the combinatorial form of this sub-leading EM
running. (Only the bracket *coincidentally* spanning `137.036` was never the mechanism.)

**Net of the reframe + swing #1:** `137 = exact leading EM`, anchored to `α̂⁻¹(M_Z) = 2⁷` — **matched
(retrodiction, §0a)**.
`+0.036 = higher-order EM running ≡ the closure-resummation tail` — one object, EM sector, scale `~5α`.
The weak attribution is **closed** (W too heavy, `α(0)` clean).

**Swing #2 (the higher-order running rule).** Further pinned down: the leading `+9` matches the one-loop
QED β-coefficient `(4/3)·Σ_{charged f < M_Z} Q² N_c = 8.89` (1.2% from `d² = 9`) — QLF reads the one-loop
running *as* the directional count. The residual localizes to the dominant `n = 2` (length-4) closures:
of the `C(4,2) = 6`, the physical weight is `0.036/α_bare = 4.61` (irreducible `2`, total `6`), at the
2-loop scale `~5α`. **The exact coefficient is the 2-loop EM running** — well-defined physics, but the
*same boundary the Standard Model has*: the running is **computed**, not derived from a deeper principle.
QLF's equal-weight closure census gets the structure (Dyson `G = 1/(1−I)`), sector (EM), and scale (`~5α`)
right, but the kinematic weight that fixes `4.61`-of-`6` is the 2-loop log structure, not pure counting.

The sections below record the closure-census analysis — the combinatorial form of this sub-leading EM
running.

---

## 0a. The discovery/confirmation firewall, applied to this file

This document is the repository's standing case for **R0a** ([`ScientificApproach.md`](ScientificApproach.md)
§4), so it should be the one that models the rule rather than the one that needs it applied.

> **Anything constructed while the target number was in view is a retrodiction, permanently.** A
> construction becomes capable of *prediction* only once frozen at a named commit, and only for
> consequences that were not used in building it.

Every scale match in §0 rests on knowing `α̂⁻¹(M_Z) ≈ 128` and `α⁻¹(0) = 137.036`, so the `2⁷ ↔ M_Z`
and `3² ↔ EM running` identifications are **retrodictions**: correct, structurally suggestive, and not
confirmation. Three items are not retrodictions, and they are the only things here that can confirm:

| Claim | Physical status | Why |
|---|---|---|
| `α⁻¹ > 137` (one-sided, from `d_eff > 3`) | **Predicted absent** | A falsifiable null; nothing about `137.036` was used to obtain it |
| the bracket `137.0159 < α⁻¹ < 137.0481` | **Predicted absent** (two-sided) | Derived from `central_binom_genfun`; CODATA merely *lands* inside it |
| `no_cosmological_drift_of_alpha` | **Pre-registered prediction** | The SM permits a varying-α field; QLF forbids drift, and the test is not yet decisive |
| `2⁷ ↔ α̂⁻¹(M_Z)`, `3² ↔ EM running` | **Retrodiction** | Targets known at construction time |
| any future residual mechanism | **Retrodiction unless pre-registered** | See the R0 block in §9a |

**The pre-filter, applied before any computation.** A candidate for the residual must (i) change a
**count of ways** ([`Philosophy.md`](Philosophy.md) §3a rule 4) and (ii) be **horizon-dependent**,
because the residual *runs* and capacity is the substrate's own scale axis
(`closedAtHorizon_iff_maxExcursion_le`). **Any fixed rational fails the filter without being
computed.** `dim Gr(3,15)`, `9/250` and `(3/15)²` are of that kind — static objects offered for a
running quantity — and the filter is where they belong, ahead of the 5th-decimal comparison rather
than behind it.

**The local derived-bridge standard is this file's own result.** `censusTail_eq` — the exact census
α-screening tail `512√62/31 − 130` — is a **theorem**, derived from Mathlib's generalized binomial
theorem with nothing chosen ([`QLF_AlphaBound`](lean/QLF_AlphaBound.lean), zero axioms). It sits at the
top of the bridge ladder (`arbitrary → pre-registered → constrained → **derived**`,
[`ScientificApproach.md`](ScientificApproach.md) §5c), inside this problem. Every candidate residual
mechanism is measured against it, as every new axiom is measured against the case where nothing is
left to choose.

---

## 1. The forced bracket (two exact closed forms) *(EM-closure reading — demoted; see §0)*

The residual is the sum of higher closure-order corrections, one bare coupling `α_bare = 1/128` per
order. Two extremal countings bound it, both exact and parameter-free:

| Counting | Closures summed | Exact tail | α⁻¹ cap | Status |
|---|---|---|---|---|
| **Total census** | every ZFA closure, `C(2n,n) = 2,6,20,70,…` | `512√62/31 − 130 ≈ 0.048130` | `137.048130` | **proven** (`censusTail_eq`, via `central_binom_genfun`) |
| **Irreducible** | prime closures only, `2·Catalan(n−1) = 2,2,4,10,…` | `126 − 16√62 ≈ 0.015874` | `137.015874` | **proven** (`irreducibleTail_eq` / `irreducibleCap_eq`) |

So, with each closure contributing positively (abelian-EM screening, `em_gauge_abelian`):

> **`263 − 16√62  <  α⁻¹  <  (217 + 512√62)/31`**, i.e. **`137.015874 < α⁻¹ < 137.048130`.**

CODATA `137.035999` sits strictly inside. **Both ends are now machine-verified**
([`QLF_AlphaBound`](lean/QLF_AlphaBound.lean)): the upper via `codata_below_alphaInvCap`/`alphaInvCap_eq`,
the lower via `irreducibleCap_eq` (`137 + irreducibleTail = 263 − 16√62`), with the irreducible count
`2·Catalan(n−1) = 4·C(2n−2,n−1) − C(2n,n)` (`irrCoeff_matches`) making the irreducible tail a linear
combination of `central_binom_genfun` and `censusTail` — **no new axiom**. The resummation
`G·(1 − I) = 1` (`census_irreducible_resummation`) is verified too: the total census is the geometric
resummation of the prime closures.

The total counting **overshoots** (`0.0481`); the irreducible counting **undershoots** (`0.0159`). The
true residual lies between — it is neither "every closure once" nor "primes only".

---

## 2. The single open rule

Everything above is forced. The one unforced quantity is **the weighting between irreducible and total
census** — equivalently, *how strongly the composite (reducible) closures contribute*. Writing the
residual as a mix,

```
r = (1 − w)·irreducibleTail + w·totalCensusTail ,
```

the measured value fixes `w = (r − 0.015874)/(0.048130 − 0.015874) = 0.6239`.

That is the whole problem, reduced to one number: **why `w ≈ 0.624`?**

### 2a. The substrate answer is measured: `w = 1/2` (137.032), not 0.624

The framing "why `w ≈ 0.624`?" quietly assumes the substrate *should* emit 0.624. It does not — and that is now
*measured*, not assumed (`genesis.py` §5b/§5c, `pure_zfa_alpha` / `logperiodic_probe`):

- The octave hierarchy is **scale-invariant**: the self-similarity ratio → 2 with no anomaly, and the
  log-periodic (discrete-scale-invariance) DFT power is `~1.5e-3` — a *null* across every census sector
  `p = 1…4` (peak/rms `~0.3–0.4`; the ratio approaches 2 monotonically = the Stirling correction, not a
  line). No preferred octave ⟹ neither tail is favoured ⟹ the resummation is **equal weight**, `w = 1/2`
  (the same "equal weight per order" the Dyson `G = 1/(1−I)` gives, §4/§9.2). This is the pure-ZFA
  **prediction** `α⁻¹ = 137 + (irred+total)/2 = 137.032002` — a falsifiable number computed before any
  CODATA comparison.

- So `w = 0.624` is the **CODATA-implied** value, not a substrate output. The gap `w: 1/2 → 0.624`
  (`δw ≈ 0.124`, a *quarter* of the interval) is exactly the resummation **depth** — how many 1PI
  insertions contribute as `q² → 0` — which is the vacuum-polarization *running*, a **continuum** quantity
  (§9.2–9.4), not a census truncation. The partial resummations climb monotonically `I → G` (one insertion
  `137.016` ↑ full `137.048`); *which* partial sum is the running integral, not a combinatorial rule. This
  **closes the "find the pure census truncation" door**: no such rule exists, because the truncation depth
  *is* the continuum running.

- **Crank-trap guard (binding):** the interval is only `0.032` wide, so many a-priori fractions near `0.62`
  (`5/8`, `9/14`, `φ−1`) land within `0.001` of CODATA. Proximity after the fact is **not** derivation;
  matching cannot select the rule. The only licensed way to move `w` off `1/2` is a genuine
  discrete-scale-invariance line (peak/rms ≫ 1, *oscillating* self-similarity) appearing in a census sector
  *before* any CODATA comparison — the §5c probe is that pre-registered test, and it is null.

**Net:** the pure-ZFA prediction is `137.032`; the remaining `+0.004` (and the full `+0.036` over the
leading `137`) is the continuum running, the boundary QLF brackets by design — same status as the
Yang–Mills gap and Navier–Stokes (§9.4). The residual is closed *to that boundary*, not to `0.624`.

---

## 3. The gauge-projection test — and why it does *not* derive the residual

The natural mechanism: irreducible closures are abelian (pure photon — EM is the abelian sector,
`em_gauge_abelian`) and contribute fully; composite closures carry the non-abelian electroweak structure
and project onto the physical photon. The photon is the `sinθ_W` projection of the neutral SU(2) boson
(`A = cosθ_W·B + sinθ_W·W³`, so `α_em = sin²θ_W·α₂`). So the **forced** prediction of this mechanism is
composite closures screened by `sin²θ_W = 3/8`:

| composite screening | mechanism | α⁻¹ | err vs CODATA |
|---|---|---|---|
| `sin²θ_W = 3/8` | photon = `sinθ_W·W³` projection — **the natural one** | `137.027970` | **`−0.0080` (misses)** |
| `cos²θ_W = 5/8` | hypercharge/`B` projection | `137.036034` | `+0.0000` |
| gauge `2/8` | `Ω_Λ` fraction | `137.023938` | `−0.0121` |
| spatial `6/8` | 6+2 alphabet | `137.040066` | `+0.0041` |

**The natural projection (`3/8`) misses by `0.008`.** The fraction the data wants is the *complementary*
`5/8 = cos²θ_W` — which is **not** the natural photon projection (it would require composites to be
hypercharge-like, contradicting "composite = non-abelian"). And the 8-twist alphabet admits several
sub-fractions (`2/8, 3/8, 5/8, 6/8`), each giving a different answer. Without an independent rule
selecting *which* fraction and *why* it screens composite (vs irreducible) closures, the `5/8` match is a
**choice, not a derivation**.

> **Honest reversal.** The `3/8` "lead" of the previous draft does not survive. The gauge fractions do
> appear, but the gauge *projection* — taken at its natural value `sin²θ_W = 3/8` — gives `137.028`, not
> `137.036`. The earlier framing also mislabeled the data weight: the data wants composites at `5/8`, not
> `3/8`. **The gauge projection does not derive the residual.**

### 3a. Which fractions a census can carry

The alphabet does not admit an open menu of sub-fractions. The rule that selects them is the
alphabet's own structure, machine-verified, and it is not a choice.

**The alphabet is 4 axes × 2 handednesses.** `QLF_AlphabetNecessity` proves the alphabet is the signed
axis frame, so `|Σ| = 2·|axes|`; a composition-closed axis set is a subgroup of the Klein four-group, so
the axis count is `1, 2` or `4` and never `3` — two distinct spatial axes carry the third with them
(`two_spatial_axes_force_three`), and the gauge axis is what closure requires rather than an addition to
the spatial six (`frame_contains_I`). `6+2` is therefore `3 spatial axes + 1 gauge axis`, each doubled:
the one split of the alphabet there is.

**A census fraction must be a union of whole axes.** `QLF_Handedness` proves ZFA is *zero net handedness
on every axis* (`zfa_iff_handedness_balanced`) — balance is per-axis. A sub-census that takes one
handedness of an axis and not the other is not handedness-balanced and therefore is not a census of
closures at all. So the closure-admissible fractions of the alphabet are exactly

$$
\frac{2}{8},\; \frac{4}{8},\; \frac{6}{8},\; \frac{8}{8} \qquad\text{i.e.}\qquad
\tfrac14,\; \tfrac12,\; \tfrac34,\; 1 .
$$

$$
\boxed{\tfrac38 \text{ and } \tfrac58 \text{ are not closure-admissible census fractions}}
$$

**Two consequences, cutting in opposite directions.**

1. **The gauge-projection route is closed, not merely unlucky.** The available fractions are
   `2/8, 4/8, 6/8, 8/8`, and none of them is the answer: `2/8 → 137.0239`, `4/8 → 137.0320`,
   `6/8 → 137.0401`. There is nothing else to choose, so the route cannot be rescued by re-choosing.
2. **The `5/8` "match" is structurally unavailable.** The fraction the data wants is not a census
   fraction at all, so it is excluded by the alphabet rather than by judgement.

> **A unit distinction, and it is what keeps the Weinberg result untouched.** `sin²θ_W = 3/8` is a ratio
> of **axes to elements** — a gauge-coupling normalization, the SU(5) value, proven as
> `sin2_weinberg_substrate_eq` ([`QLF_WeinbergAngle`](lean/QLF_WeinbergAngle.lean)). A *screening weight*
> is a ratio of **elements to elements**. Two different objects with different admissibility rules, and
> only the second is constrained to `{2/8, 4/8, 6/8, 8/8}`. The table above lists both conventions in one
> column; read `3/8` there as the projection and the rest as census fractions.

---

## 4. What the test *did* establish (a forced structural fact)

Working out the test surfaced an exact, parameter-free relation between the two census generating
functions:

> **`G(x) = 1 / (1 − I(x))`**, where `G(x) = ∑ C(2n,n) xⁿ = (1−4x)^(−1/2)` (total) and
> `I(x) = ∑ 2·Catalan(n−1) xⁿ = 1 − √(1−4x)` (irreducible).

This is exact (`1/√(1−4x) = 1/(1−(1−√(1−4x)))`) and it is the **Dyson / 1PI structure**: the total set of
closures is the *geometric resummation* of the prime (irreducible) closures, exactly as the full
propagator is `1/(1−Π)` of the 1PI self-energy. Combinatorially it says **every ZFA closure is uniquely
an ordered sequence of irreducible (prime) closures** — closure prime-factorization, and a *sequence*
(order matters, as twist histories are ordered) hence geometric, not exponential.

So the open rule is **not** a free "weighting between `I` and `G`" (that framing was itself
numerology-prone). It is sharper: the residual is a **partial Dyson resummation** of the prime-closure
series, and the physical truncation/regularization is what must be derived. The full resummation (`G`,
one `α_bare` per order) overshoots; one prime term (`I`) undershoots; the physical value is a specific
partial resummation whose rule is the genuine open problem.

---

## 5. The curvature route — adjudicated by scale

The other candidate mechanism: the flat directional count `N = d² = 9` (the `3×3` directional tensor on
flat 3-space) acquires a curvature correction `N → 9 + κ` on the curved closure graph, with
`α⁻¹ = 128 + (9 + κ)`. This must be a **static** curvature, not a running effect — running vanishes at
`q²→0`, but CODATA is the IR (Thomson) value, so the correction survives at the IR. The natural source is
the **intrinsic positive curvature** of the directional 2-sphere `S²` (directions in 3-space *are* points
on `S²`).

**The sign is forced and correct.** Positive curvature raises the effective directional count above the
flat `d² = 9`, so `d_eff > 3` and `α⁻¹ > 137` — screening. This matches the proven bound
(`alpha_inv_gt_137`) by construction: a flat or negatively-curved directional space would give the wrong
sign. So far the curvature route is consistent where the gauge route was not.

**The magnitude is the wrong scale.** Matching requires `d_eff = 3.006` (a `0.2%` dimension shift) or
equivalently `κ/N = 0.4%`. But every dimensionless geometric curvature invariant is **O(1)**:

| invariant | value |
|---|---|
| heat-kernel Euler term `χ/6` (S²) | `0.333` |
| icosahedral deficit/vertex `4π/12` (the QLF primordial blanket, `QLF_PrimordialMarkovBlanket`) | `1.047` |
| octahedral deficit/vertex `4π/6` (the 6 axis endpoints `±x,±y,±z`) | `2.094` |
| Gauss–Bonnet total `2πχ` (S²) | `12.57` |

The residual `κ = 0.036` is **10–40× smaller** than any of these. It does *not* sit at the geometric
scale — it sits at the **closure-order scale**: `κ ≈ 4.6·α_bare` (the leading census term is
`6·α_bare = 0.047`). A standalone pure-geometry curvature correction to `d²` would overshoot by one to
two orders of magnitude.

> **Verdict.** Curvature can contribute to the residual **only if it is `α_bare`-suppressed** — i.e. only
> as a *per-closure-order* effect, not as a separate O(1) geometric correction. That is precisely the
> framework's own anticipation that *"the census tail and the discrete curvature may be the same
> object."* The scale test makes it sharp: **curvature is not an independent mechanism; it must be
> identified with the closure-order resummation** of §4. It contributes the right *sign* (positive
> directional curvature ⟹ screening), but the *magnitude* lives in the closure-order sum, not in a
> standalone geometric invariant.

So both routes converge on one open problem: the **partial-resummation rule** of the prime-closure series
(§4) — which, by §5, *is* the discrete curvature of the closure graph, just at the closure-order scale.

---

## 6. Status (corrected)

### 6a. Two-axis status

Mathematical status (what is established about the formal object) and physical status (what is
established about the world) are different questions, and this file's central open item is open on the
second axis only ([`ScientificApproach.md`](ScientificApproach.md) §3).

| Claim | Mathematical | Physical |
|---|---|---|
| bracket `137.015874 < α⁻¹ < 137.048130` (`alphaInvCap_eq`, `irreducibleCap_eq`) | **Proved** | **Predicted absent** — a two-sided null CODATA lands inside |
| `α⁻¹ > 137` from `d_eff > 3` | **Proved** | **Predicted absent** — one-sided, and the honest anchor |
| `censusTail_eq` — the exact screening tail | **Proved** (discharged from axiom) | **Internal** |
| `G = 1/(1−I)` — the Dyson/1PI structure of the closure census | **Proved** | **Internal** |
| `128 + 9 = 137` as weak-scale coupling + EM running | **Exact computational** | **Retrodiction** (§0a) |
| `3/8`, `5/8` not closure-admissible (§3a) | **Proved** | **Internal** — it constrains the menu, not an observable |
| the residual **is** the higher-order EM running | **Conjecture** | **Open bridge** — *this is the whole open problem* |
| the partial-Dyson truncation rule | **Conjecture** | **Open bridge** |

The last two rows are the file's real content.

### 6b. The failure-criterion test, self-applied

Eight candidate bridges stand discarded for one target number: the weak/W-loop sector (§0),
gauge projection at `3/8` (§3), hypercharge `5/8` (§3), the `w = 0.624` weighting (§2a), standalone
curvature (§5), and the three one-term geometric patterns `dim Gr(3,15)`, `9/250`, `(3/15)²` (§9).

That is exactly the shape [`ScientificApproach.md`](ScientificApproach.md) §7a's **criterion (b)**
polices — a programme that replaces a failed bridge every time one fails is protected indefinitely — so
the test is owed rather than the reassurance. It **passes**, for two checkable reasons:

1. **Every rejection is forced by an independent computation**, never selected by proximity to
   `0.036`: the `M_W` threshold (the `W` cannot run below it), the exact bracket, the
   `O(1)`-vs-`O(α_bare)` scale argument, the 5th-decimal miss against `0.035999084(21)`, and the
   per-axis handedness balance of §3a, which excludes two fractions structurally.
2. **The question narrows.** From "which weighting between `I` and `G`" — a framing §4 calls
   numerology-prone — to one named object: **the partial-Dyson truncation rule**.

That is exclusion, not rescue. **The tripwire is recorded with the count:** if the number of discarded
bridges keeps growing while that object does not sharpen further, and the census stops doing the
excluding, criterion (b) has been met and the residual should be reported as beyond the substrate's
reach rather than pending.

### 6c. Summary

- **Forced, exact, and machine-verified (both ends):** the bracket `137.015874 < α⁻¹ < 137.048130` —
  upper `alphaInvCap_eq`/`codata_below_alphaInvCap`, lower `irreducibleCap_eq` (`263 − 16√62`) — plus the
  resummation `G·(1−I) = 1` (`census_irreducible_resummation`), all from `central_binom_genfun`, no axiom.
- **Right sign, forced:** positive directional-sphere curvature ⟹ `d_eff > 3` ⟹ `α⁻¹ > 137` (§5),
  consistent with `alpha_inv_gt_137`.
- **Open — the value:** both candidate mechanisms tested. **Gauge projection fails** (natural
  `sin²θ_W = 3/8` ⟹ `137.028`, §3). **Standalone curvature is the wrong scale** (geometric invariants are
  O(1), the residual is O(`α_bare`), §5). Both reduce to the **partial Dyson resummation** of the
  prime-closure series, whose truncation rule is underived — and that rule *is* the discrete closure-graph
  curvature at the closure-order scale.
- **Discipline:** no value is claimed. Two pure-geometry/gauge shortcuts are *eliminated*; the open
  problem is *localized* to one object — the resummation truncation rule. Honest progress is the
  eliminations plus the localization, not a number.

Remaining derivation target: the partial-resummation / truncation rule from the closure-order structure
— the single open object both routes reduce to. (The forced bracket and the resummation `G = 1/(1−I)`
are now machine-verified, §1; what is open is *which* partial resummation the physical residual is.)

See [`Alpha.md`](Alpha.md), [`QLF_AlphaBound`](lean/QLF_AlphaBound.lean),
[`QLF_WeinbergAngle`](lean/QLF_WeinbergAngle.lean), [`QLF_CausalDimension`](lean/QLF_CausalDimension.lean),
[`QLF_PrimordialMarkovBlanket`](lean/QLF_PrimordialMarkovBlanket.lean).

---

## 7. The resonance spectrum (binary / octave reading) — the Pauli–Heisenberg lineage

A bit-native reframe (per Jim; "Shannon does not lie" — the QLF substrate *is* information, "it from
bit"). Write `α⁻¹` in binary: each set bit at octave `2ᵏ` = an **active resonance** (a stable ZFA
closure mode). This continues the **Eddington–Pauli–Heisenberg** program — deriving `137` as an
eigenvalue/resonance of the fundamental structure — but on a *discrete, computable* substrate (closures)
rather than Eddington's fit or Heisenberg's continuum nonlinear spinor field. Literally: QLF's `137` is
built from **Pauli's own matrices** (the 8 twists → σ-matrices, `QLF_TwistAlphabet`; closure *is* Pauli
closure, `count_balanced_pauli_closed`; `3² = (σx,σy,σz)²`).

**The spectrum.** `137 = 2⁷ + 2³ + 2⁰ = 10001001₂` — three resonances at octaves **{7, 3, 0}**:

- **octave 7** (`2⁷ = 128 = 1/α_bare`) is a *cascade* of substrate selectivity resonances at octaves
  {4, 2, 1, 0}: `1/16` (alphabet) · `1/4` (gauge) · `1/2` (phase) · `1` (space) `= 2⁻⁷`
  (`QLF_FineStructureSubstrate`); `7 = 4+2+1`.
- **octaves 3, 0** (`8 + 1 = 9 = 3²`): the directional / Pauli-σ tensor.

The leading resonances {7, 3, 0} are **grounded in the substrate** (the cascade + the three axes) and
produce 137. The sub-octave **tail** (first bits at −5, −8, −11, *spaced by 3 = d*) is the higher-order
region.

**Three-order structure** (each term a clean alphabet/axis count):

| order | term | value | reading |
|---|---|---|---|
| 1st | `2⁷` | `128` | 8-twist alphabet selectivity cascade |
| 2nd | `3²` | `+9` | three Pauli axes, directional tensor |
| 3rd | `9/250 = d²/250` (Jim's `0.036`) | `+0.036000` | a clean third-order term; `250 = 2·5³`? (angle-DOF, unforced) |
| 4th | the measured detuning | `−0.00000092` | the genuine higher-order shift |

`2⁷ + 3² + 9/250 = 137.036` matches CODATA `137.035999084(21)` to `9×10⁻⁷` — but **not** exactly:
`137.036` is **44σ above** the measurement. So `0.036` is the (excellent) third-order resonance peak and
the measured `…999` is the **real fourth-order detuning** (a resonance sits slightly off its ideal
centre). `9/250` beats the binary-comb `1/28` (off `0.8%`) by 300×, and keeps the `d² = 9` motif — but
`250` is not yet forced, so it is an improved *lead*, not a derivation.

**Why the precision is a gift, not a threat.** Because `α⁻¹` is measured to ~44σ on this digit, the
substrate resonance spectrum has a *sharp falsifiable target* (`137.035999084`, clean 3rd order `9/250`, a
genuine 4th-order detuning). The measurement — not our taste — decides. That is exactly the line between
this program and Eddington's "+1": the **leading {7,3,0} is derived**; the 3rd/4th orders are
structurally-backed *leads* held to the measurement.

**The real test — TAKEN, and NEGATIVE.** Does an *independent* substrate spectral density peak at octaves
{7, 3, 0}? The genuine Hilbert–Pólya object is `toSpectralMode s = diag(count_pos, count_neg)`
([`QLF_Spectral`](lean/QLF_Spectral.lean)): a balanced closure of length `2n` has eigenvalue `n` with
multiplicity `C(2n,n)`. That density is **monotonic** — multiplicity `2, 6, 20, 70, …` (increasing), Born
weight `C/4ⁿ` (decreasing) — with **no peaks** anywhere; at eigenvalues {7,3,0} the multiplicities are just
`3432, 20, 1`. And more fundamentally, **the test conflates two axes**: {7,3,0} are positions in the
binary *value* `137`, while the spectrum is indexed by *eigenvalue* `n` — there is no reason the eigenvalue
density would encode the binary digits of its own coupling value.

**Conclusion:** α⁻¹'s binary octaves {7,3,0} are the digits of the derived `2⁷ + 3²` — a *representation*,
not an independent eigenvalue spectrum. The strong "resonance spectrum" claim is **not supported**. What
survives is real but weaker: `2⁷` is a genuine selectivity *cascade* (octaves {4,2,1,0}) and `3²` the
three Pauli axes — *resonance conditions* (multiplicative selectivity filters), **not** an eigenvalue
density. So the leading `137 = 2⁷ + 3²` stays derived/verified; only the eigenvalue-spectrum reading fails.

**Honest landing of the whole arc.** Across gauge (§3), curvature (§5), weak/W-running (§0), the binary
comb, and the eigenvalue spectrum (here), the pattern held without exception: **`137 = 2⁷ + 3²` is
derived** (cascade + Pauli dimension), exact, zero-axiom, machine-verified; **the residual `+0.036` is a
sub-leading EM effect at `~5α`** (best clean form `9/250 = d²/250`, an improved lead; measured `−9×10⁻⁷` a
real 4th-order detuning, 44σ from `0.036`); and **every *deeper mechanism* for the residual is rejected or
stays a lead.** Like the SM's own running, the residual is — at the current state — *computed, not
principle-derived*. That is the honest boundary.

**Prime-closure stability — a new `d = 3` selection signature (per Jim).** QLF's stable closures are the
*irreducible* (prime) ones (`G = 1/(1−I)`: every closure is an ordered sequence of primes; the
stable=prime↔Riemann program, `QLF_Riemann`). Push that to the coupling itself: require the leading
inverse coupling `α⁻¹ = 128 + d²` to be *irreducible* (a prime integer — a closure that cannot factor into
sub-closures). Then among low dimensions **only `d = 3` qualifies** (machine-checked to `d ≤ 14`; the
`d = 15 → 353` caveat is below):

| `d` | `128 + d²` | |
|---|---|---|
| 1 | 129 = 3·43 | composite |
| 2 | 132 = 2²·3·11 | composite |
| **3** | **137** | **PRIME** |
| 4 | 144 = 12² | composite |
| 5 | 153 = 3²·17 | composite |
| 6 | 164 = 2²·41 | composite |
| 7 | 177 = 3·59 | composite |

`137` is prime, and among `128 + d²` it is the **unique** prime for `d ≤ 14` — **machine-checked**
([`QLF_AlphaRigidity`](lean/QLF_AlphaRigidity.lean): `prime_below_15_only_three`, `inverseAlpha_three_prime`).
**But primality is not an *independent* selector of `d = 3`, and the honest form matters:** the fence is
tight only to `d ≤ 14` — `128 + 15² = 353` is **also prime** (`inverseAlpha_fifteen_prime`), so "prime
output" alone would bless a 15-D rendering. The elementarity (prime) sector therefore *agrees* at `d = 3`
but does **not** exclude on its own; it is the *dimension* sector (6+2 split → `d = 3`) that excludes
`d = 15`. This is precisely the **cross-sector overdetermination** result ([`Alpha.md`](Alpha.md) §6a):
the dimension sector, the bare-coupling sector (`128 = 2⁷`), and elementarity (`137` prime) *meet* at
`α⁻¹ = 137`, and the three overdetermine **jointly**, not each alone. **Honest scope:** this bears on the
*leading value / dimension*, not the residual — and the link "closure-irreducible ↔ integer-prime" is a
suggestive structural reading, not yet derived (it would need the coupling's integer to literally count an
un-factorable closure). The prime-closure *spectrum* (`2·Catalan(n−1) = 2,2,4,10,28,…`) is itself
monotonic, so it adds no resonance peak; the prime tail (`0.0159`) still undershoots the residual. So
primes *agree* on *why 137 / why d=3* (jointly with the other sectors), not the `+0.036`.

---

## 8. The 4D projection — sourcing the `d_eff` excess (leading mechanism candidate, per Jim)

The directional count was treated as purely 3-D (`3² = 9`). But QLF's ontology is **4-D**: 3 rendered
spatial axes **+ 1 synthesized time** (`f = 1/t`). So the directional coupling tensor is `4×4` in
spacetime, and only the spatial block renders as the leading screening:

```
 3D spatial block:  3² = 9     → renders → α⁻¹ = 137  (leading)
 full 4D tensor:    4² = 16    → α⁻¹(d=4) = 144   (only_3d_substrate_gives_137 counterfactual)
 time components:   16 − 9 = 7  (4th row + column)
 measured d_eff = √(137.036 − 128) = 3.006   →  time pushes d just above 3
 residual = 0.036 = a 0.5% leakage of the 7 time-components
```

**Why this is the strongest candidate (three things fall in place, none fitted):**

1. **It *sources* `d_eff > 3`.** The curvature route (§5) needed `d_eff = 3.006` but had no reason for the
   excess (pure geometry is O(1), wrong scale). The 4-D projection supplies it: **the 4th dimension (time)
   leaks into the spatial directional count**, pushing `d_eff` just above 3. The bare posit becomes a
   mechanism.
2. **It explains why the residual is *small*** — the one thing every other candidate had to assume. Time
   is *suppressed*: emergent (`f = 1/t`), not a spatial axis, Lorentzian. So its contribution to the
   spatial screening is naturally a fraction of a percent, not O(1). That is *why* `0.036`, not `7`.
3. **The sign is forced and correct.** Time *adds* to the count ⟹ `d_eff > 3` ⟹ `α⁻¹ > 137` ⟹ screening
   (consistent with `alpha_inv_gt_137`).

The recurring **`5`** gets a 4-D home: a spin-2 (directional / graviton) mode in 4-D has `2J+1 = 5`
polarizations, so `residual ~ 5α = 0.0365` (a 4-D reading of the `5α` that kept recurring; `9/250 = 0.0360`
is still the closer numeric lead, `5α` 1.3% high). Note `9 = 4-D traceless-symmetric tensor` count too
(`4·5/2 − 1 = 9`), so the `9` itself has a spacetime reading.

**Honest boundary — same address, better character.** The underived piece is a single, *physical*
quantity: the **time-suppression factor** (`0.5%`, i.e. `δd = 0.006`). It is a lead, not a derivation. But
instead of "the residual is some unforced number," the open problem is "the residual is the suppressed
leakage of the synthesized time dimension; derive the suppression from `f = 1/t` / the Lorentzian
signature (`QLF_GravityFromDelay`) **before** comparing." That is a concrete, well-posed next swing — and
the best-motivated one in this file, because it gets the sign, the smallness, *and* the `d_eff` excess from
one mechanism (emergent time) rather than three separate posits.

### 8a. Deriving the time-suppression from `f = 1/t` (the swing taken)

`f = 1/t` is structural (`ZFAEventDynamics`: time is defined as `1/t`). Space is *direct* in the free
action; time is its *reciprocal*. So the time mode of the directional tensor enters **inverted**, and
this **forces** — with no fitting — both the **sign** (time adds ⟹ `d_eff > 3` ⟹ `α⁻¹ > 137`, screening)
and the **smallness** (a reciprocal contribution is a fraction of a percent, not O(1)). The *mechanism* is
thus derived, not posited.

The exact magnitude needs the substrate action scale `A` (suppression `~ 1/A²`). Closing it
self-consistently (`A² = α⁻¹`, the coupling setting its own scale) gives
`δ(α⁻¹) = 5·(1/α⁻¹) = 5α`, with **`5` = the spin-2 (directional/graviton) polarizations in 4-D** (`2J+1`)
— so `α⁻¹ = 137 + 5/α⁻¹ = 137.0365`. This **reproduces the `m = 5` self-consistent screening** of the very
first pass, now with the `5` *structurally identified* (spin-2 count, not ad hoc). Three independent routes
— self-consistent screening, the recurring `5α`, and the 4-D projection — **converge on `5 modes × α`.**

**Honest precision.** `5α = 137.0365` is **1.3% high**: the measured residual coefficient is `4.93`, not
`5` (and against a 44σ measurement, 1.3% is a definitive miss in absolute terms). So this is a **derived
mechanism + ballpark** (~`5α`), **not a precision match**. The clean integer `5` detuned to `4.93` is the
higher-order piece — parallel to `137` (prime) detuned to `137.036`. The precise value (`9/250 = 4.93α`)
has no mechanism; the clean `5α` mechanism has no precision.

**Landing of the whole arc.** `137 = 2⁷ + 3²` is exact, zero-axiom, machine-verified, and prime-selected
for `d = 3`. The residual `+0.036` is a **4-D time-suppression effect of order `5α`, with mechanism, sign,
and smallness derived from `f = 1/t`** (the most any swing achieved). The last ~1% — the integer `5` vs the
measured `4.93`, i.e. the action scale to <1% — is the genuine remaining boundary, indistinguishable in
character from the Standard Model's own un-derived running. **Mechanism derived; precision open.**

### 8b. Deriving the action scale `A` — the boundary located (the close)

`A` *is* derivable to its natural value: **self-consistency** (the closure defining α has action `~α⁻¹`),
so `A² = α⁻¹` — fit-free. This gives `δ = 5/A² = 5α = 0.03649` ⟹ `α⁻¹ = 137.0365` (+1.4%). The *other*
clean forced scale, one more selectivity-cascade octave `A² = 2⁸ = 256` (with the full `N = 9`), gives
`9/256 = 0.0352` (−2.3%). **The two forced scales bracket the measurement** (`137.036`); the value the data
wants, `A² = 138.9`, sits between them and is **not a forced substrate number**.

So the last ~1% is **not a missing scale** — it is the **higher-order running tail**: the clean integer
`5` (spin-2 polarizations, the self-consistent leading term) detuned by the running to `4.93`
(`5α − 10α² − … = 0.035954 − …`), an *infinite series*. The measured coefficient is `4.93` (α-units) /
`4.61` (bare-units) — non-integer in both, the signature of a detuned integer, not an unfound count.
Crossing it means *summing the running series* — computed-not-principle-derived even in the SM. There is no
further substrate scale to find; the forced scales bracket it and the gap *is* the running.

**Close of the α-residual investigation.** Everything QLF can force is forced:
`137 = 2⁷ + 3²` (cascade + Pauli dimension), prime-selected for `d = 3`, exact / zero-axiom /
machine-verified; `central_binom_genfun` discharged, the two-sided `√62` bracket and `G = 1/(1−I)`
formalized; and the residual `+0.036` a **4-D time-suppression effect with mechanism, sign, smallness, and
leading magnitude `5α` derived from `f = 1/t`** (self-consistent `A = α⁻¹`, `5` = spin-2 polarizations).
The remaining ~1% — the detuning of the clean `5` to `4.93` — is the higher-order running tail, **the
Standard Model's own un-derived precision frontier**, bracketed by the two forced substrate scales. Going
further would be either fitting (forbidden) or full multi-loop SM physics (not a substrate derivation).
**Mechanism and structure derived; the last percent is the running — the honest boundary.**

---

## 9. Obstacles to continuing (the honest agenda — *not* a surrender)

The leading structure is derived; crossing the last ~1% (the `5 → 4.93` detuning) is blocked by specific,
nameable obstacles. Stated so the work can resume against a concrete target:

1. **It is an infinite series, not a number.** The detuning is the higher-order running tail
   (`5α − 10α² − …`, all orders). Forcing it means deriving the *whole* series, not one more term.
2. **QLF has counting, not kinematics.** The substrate yields combinatorial multiplicities (`C(2n,n)`,
   Catalan, the Dyson `G = 1/(1−I)`) — *equal weight per order*. The running's higher-order coefficients
   come from loop kinematics (logs, phase space, 2-loop integrals) that pure counting does not produce.
   This is the "which partial resummation" gap in another guise (shared with the RG / Yang–Mills program).
3. **A 44σ irrational needs the continuum.** The substrate emits clean integers/rationals (`2⁷, 3², 5`);
   the measured value is irrational to 10 digits. Reproducing it = summing infinitely many continuum
   corrections = the QED running.
4. **That sector is the one QLF brackets *by design*.** QLF's thesis is that the continuum is the
   UV-catastrophe sector (Gödel/Turing/Busy-Beaver). The last ~1% lives precisely there: the discrete
   substrate gives the clean *leading* structure; the continuum running gives the *precision tail*. The
   boundary is philosophically coherent, not accidental — discrete ⟹ leading, continuum ⟹ tail.

**What would unblock it (a real program, not a tweak):**
- **(a) Derive the kinematic weighting from the substrate** — show how the closure census acquires the
  running's higher-order coefficients (the logs / phase space *from counting*). Shared open frontier with
  the RG sector (`QLF_RunningCouplings`, `QLF_BetaFunction`). **Sharpened, falsifiable form**
  ([issue #117](https://github.com/jimscarver/quantum-logical-framework/issues/117)): the residual is the
  substrate reading of **vacuum polarization** as a census-weighted, **horizon-scale-dependent** sum over
  the elementary (prime-count) closure **tower** (`closedAtHorizon`); the value-free first target is to
  derive the **one-loop running coefficient** (`2/3π` per unit charge per fermion) from census counting
  with no reference to `0.035999`. One-term geometric shortcuts (`dim Gr(3,15)=36`, `9/250`, `(3/15)²`)
  are refuted — they match only the *rounded* `0.036`, miss at the 5th decimal (`0.035999084(21)`), and
  are static where the residual runs.
- **(b) Or find an *exact* (non-perturbative) substrate self-consistency** — a closure/eigenvalue condition
  giving the value exactly, not leading-order. The self-consistent `A = α⁻¹` is the *leading* term of such
  a condition; an exact version (if it exists) bypasses the series.

Until (a) or (b) lands, the honest status holds: **leading structure derived; precision tail = the
continuum running QLF brackets.** The obstacle is not a missing number — it is the continuum sector itself.

---

## 9a. The pre-registered bridge for route (a)

Route (a) is the live one, and it runs under **R0** ([`ScientificApproach.md`](ScientificApproach.md)
§4): the bridge is specified in full *before* any comparison, so that a match can count as evidence
rather than as a ninth retrodiction. The target is deliberately **value-free** — the one-loop running
coefficient, not `0.035999`.

| R0 field | Specification |
|---|---|
| **Physical inputs held fixed** | The charged-fermion content below `M_Z` (`Σ Nᶜ Q_f²`), and nothing else. No use of `α⁻¹(0)`, `137.036`, or `0.036` at any step |
| **Substrate representation** | The elementary (prime-count) closure **tower** graded by horizon capacity `R` (`closedAtHorizon`), with each closure weighted by the cylinder measure `8^{−\|h\|}` — *derived*, not chosen ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) |
| **Calculation** | The census-weighted, horizon-dependent sum over that tower — the substrate reading of vacuum polarization |
| **Observable-extraction rule** | Read the coefficient of the leading `log` in the horizon dependence as the one-loop running coefficient per unit charge per fermion |
| **Tolerance** | Exact rational, or a stated bound. Floating-point asymptotics are contaminated past `k*` (R4) and do not count |
| **Comparator** | The QED one-loop coefficient `2/(3π)` per unit charge per fermion — a *known* number, so the comparison is a **retrodiction** for the coefficient itself. What becomes a **prediction** is the next term, extracted from the same frozen construction without re-tuning |
| **Kill condition** | If the census-weighted horizon sum yields no `log`, or a `log` whose coefficient is not `2/(3π)` at the stated tolerance, route (a) is closed and the residual is reported as belonging to the continuum sector |

**Freezing.** The construction counts as frozen at the commit that records it, and only consequences
not used in building it are claimable as predictions (R0a). The `2/(3π)` coefficient is census-anchored
already; the **two-loop** coefficient is the first genuinely unused consequence, and is therefore the
first thing here capable of confirming rather than retrodicting.

**What route (a) does not require.** It requires no reference to `0.036` at any point. A derivation
that reaches the running coefficients from counting delivers the residual as an output; one that
reaches `0.036` by any other path delivers a ninth discarded bridge (§6b).

---

## 9b. Route (a), executed — the search-registry bridge ([`alpha_residual_bridge.py`](alpha_residual_bridge.py))

The §9a construction is now run, value-free, and it splits into three parts with three different
verdicts. Two census layers: the abstract 1-D walk census (`C(2n,n)` total, `2·Catalan(n−1)` prime,
brute-checked, `G = 1/(1−I)` verified as a power series), and — per Jim's steer that *the search event
registry could go deeper* — the **real 8-twist first-closure (absorbing) census** from
[`qucalc_search`](qucalc_search.py) / [`twist_core`](twist_core.py): count-balanced histories (= ZFA
closures by `count_balanced_pauli_closed`) whose no proper even prefix closes. Enumerated primes:
**8, 104, 2944, 108136, 4525888** at lengths 2–10. Binned by max-excursion `R` and weighted by the
Kraft cylinder measure `8^{−L}` ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)), this is a genuine
[`QLF_ExactRG`](lean/QLF_ExactRG.lean) `ClosureSpectrum`: the recursion `Z(N+1) = Z(N) + mass(N)` runs,
`Z` is monotone and Kraft-bounded (`Z_limit ≈ 0.172 < 1`), `amp` converges (`≈ −0.114`).

| Part of the bridge | Verdict | Detail |
|---|---|---|
| **The one-loop coefficient `2/(3π)`** | **SURVIVES — 1PI-confirmed** | `census_split → 1/6` for the **prime** (irreducible / 1PI-loop) census `2·Catalan(n−1)` exactly as for the total `C(2n,n)` or a flat weighting — all reach the Feynman integral `∫₀¹ x(1−x)\,dx = 1/6` by the same dominated limit. So `2/(3π) = (1/6)·(4/π)` is a property of *irreducible* fermion loops, not an artifact of counting reducible ones. The census-anchored coefficient is now shown 1PI-legitimate |
| **The leading `log` from the horizon sum** | **NO — this step of §9a does not hold** | The Kraft-weighted per-octave increment **decays** (`mass(R)` ratios `≈ 0.25, 0.38, 0.26, 0.11` — not constant), because a Kraft sum is bounded by `1` (`twist_kraft`) so its increments must vanish. There is no `log` in the closure *mass*. The QED logarithm is carried by the scale↔octave map `Q(R) = Q₀·2^R` with a **scale-free per-octave count** (`flux_scale_invariant`, [`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean)) — an information-theoretic input the prime census does not itself derive. §9a's "read the leading log of the horizon sum" conflates the census (which gives the coefficient) with the scale map (which gives the log); the test separates them |
| **The higher-order tail** | **UNTOUCHED** | The `−10α²` that detunes the clean `5` to `4.93` (§8b) needs kinematic weights; the equal-weight closure census gives every order weight `1` (§9 obstacle 2). Unchanged |

**Net.** Route (a) is **refined, not closed**: the coefficient part advances (`2/(3π)` is now a
confirmed 1PI/prime object, not just a census fit), the log-carrier is relocated to the scale map
(already Lean-anchored, `QLF_VacuumPolarizationTower`), and the higher-order tail is the same open
piece as before — frontier #1. The `+0.036` value is **not** delivered, and no reference to it entered.

**Fractal / Zipf probe** (per Jim, *"fractals and zipf might close the gap"*): **null, and now confirmed
at converged depth** ([`alpha_residual_deep.py`](alpha_residual_deep.py)). The brute run capped at `L = 10`
left the deep excursion levels unfilled; an exact transfer recursion (state `(v,h,d,l,inv,maxexc)`, the
`intermittency_bridge.py` method) reruns the identical first-closure census to `L ≤ 28` in seconds — the
prime sequence continues `8, 104, 2944, 108136, 4525888, 204981888, 9792786432, 486323201640, …` (first
five as before), ratio climbing `13 → 53`. At that depth: the octave Kraft-mass self-similarity ratio
**decays monotonically with no oscillation** (the forced `twist_kraft` decay, nothing riding on it); the
Zipf rank–frequency slope keeps steepening `−4.2 → −11.2` as the cutoff grows, never approaching `−1`
(not a power law); and the `genesis.py`-style log-periodic probe gives a single-arch residual with
periodogram `peak/rms ≈ 1.4` (O(1), the DSI kill threshold) — a Stirling-type trend, not a
discrete-scale-invariance line. So the census is scale-*invariant* (period-1 cascade), with **no**
bifurcation/log-periodic line that could move the §2a weight `w` off `1/2` — upgraded from "null so far"
to "null at depth". (The `QLF_ExactRG` signed limit also converges: `amp_limit = −0.113574` identical at
`L ≤ 22` and `L ≤ 28`.)

**The prime census is a known sequence — [OEIS A359801](https://oeis.org/A359801), and the identification
carries the null.** `8, 104, 2944, 108136, 4525888, 204981888, …` is *"the number of 4-dimensional cubic
lattice walks that start and end at the origin after `2n` steps, not touching the origin at intermediate
stages"* — which is exactly what the 8-twist first-closure census counts (the 8 twists are `±e₁…±e₄`,
count balance is return to origin, "prime" is first return). This is not a coincidence to explain; it is
what the census *is*. Three consequences: (i) the total census is `INVERT(A359801)` = `A039699` (all 4-D
returns), so QLF's `G = 1/(1−I)` (`census_irreducible_resummation`) **is** the classical first-return /
renewal relation `Q = 1/(1−P)` (Novak 2014) — the free-monoid/bifibration argument has a classical twin
in renewal theory. (ii) The census has a **closed-form generating function**:
`P(x) = 2 − 1/Q(x)`, `Q(x) = ∫₀^∞ e^{−t} I₀(2t√x)⁴ dt` (Bessel). Its only positive-real singularity is the
combinatorial radius `x = 1/64` — a **single dominant real singularity**, which is precisely "no
log-periodic line" stated as an analytic fact, no new argument needed. (iii) The `QLF_ExactRG` `Z_limit`
is `Σ A359801(n)/64ⁿ = P(1/64)` = the **4-D Pólya return probability `≈ 0.193206`** (the truncated
`0.1835` at `L ≤ 24` converges up to it); `amp_limit ≈ −0.1136` is its phase-signed analogue. So the RG
`Z` flow has an exact closed-form limit, a named lattice constant.

**And the null is forced, not lucky — the bifibration is upstream of the self-similarity** (per Jim: *in
the possibilist realm the bifibration is one thing that happens, and it is responsible for the
self-similarity*). The chain: closures factor **uniquely** into an ordered sequence of primes (§4,
"uniquely an ordered sequence of irreducible closures"), so the primes generate a **free** monoid; over
the horizon/order grading that free monoid *is* a **bifibration** — restrict to capacity `R`
(`closedAtHorizon`, the `--listening` cartesian lift, *integrating out*) and extend to `R+1` (`Z_succ`
and the `IsDiagram` binding/nesting clauses, the cocartesian lift, *adding a shell*), with unique lifts
because the factorization is unique. That bifibration forces `G(x) = 1/(1−I(x))`
(`census_irreducible_resummation`, proven), hence a **geometric** generating function, hence a **linear**
coefficient recurrence `G_m = Σ_j I_j G_{m−j}`, hence the constant ratio-4 growth `C(2n,n) ~ 4ⁿ` and
scale-invariant self-similarity — every fiber again the whole structure. So the census is self-similar
*because* the bifibration is realized; and a linear recurrence has **no period-doubling** — bifurcation
needs a nonlinear parameter-dependent map — so the log-periodic channel is closed by structure, not
merely unobserved. This does not hand over `+0.036` — the weight stays `w = 1/2`, which is the point —
but it upgrades §2a's `w = 1/2` from "measured null" to "structural consequence".

**"Self-similarity × number of ways" is exactly what `w = 1/2` already is — and it does not help.**
The residual's per-order weight decomposes as *(per-order weight) × (ways at that order)* with the ways
`= C(2n,n)`. Self-similarity fixes the first factor: a scale-invariant structure has the **same** weight
at every order — a constant — so *self-similarity × ways* `= const · C(2n,n)`, which is the equal-weight
resummation, `w = 1/2`, `α⁻¹ = 137.032`. That is the pure-ZFA prediction, recovered as a *derivation*
rather than a stipulation. Tested modulations that break the constancy were checked and do not land
([`alpha_residual_bridge.py`](alpha_residual_bridge.py) idea, computed): weighting order `n` by the
divisor count `d(n)` (block-lengths it could be a power at) or by `2^{ω(n)}` **overshoots** badly
(`α⁻¹ → 137.096`); weighting each closure by its automorphism group `|Aut(h)|` via the repetition sum
`Σ_m C(2m,m)\,x^m/(1−x^m)` **reduces to the plain total census** (the `x^{2m}` corrections are
negligible at `x = 1/128`). None reaches `w ≈ 0.624`, and — consistent with the paragraph above — a
number-theoretic modulation that *would* move `w` is exactly the nonlinear ingredient the free-monoid
linearity excludes. The `δw` to `0.624` is the continuum vacuum-polarization running integral (§2a), not
a census re-weighting; `census_split` gives its **coefficient** `2/(3π)` (now 1PI-confirmed, §9b table),
not its higher orders.

**The turbulence / intermittency swing — the best-motivated candidate for `δw`, and what it needs.**
The nonlinear ingredient the linear census lacks has a home in the repo already:
**intermittency**. The α running and the turbulent cascade **share one Lean theorem** —
`QLF_Kolmogorov.flux_scale_invariant` carries both the QED octave-count logarithm
([`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean)) and the `−5/3` spectrum
([`Navier_Stokes_Geometry.md`](Navier_Stokes_Geometry.md) §6a) — and the monofractal (flat per-octave,
`w = 1/2`) reading is exactly K41. Real cascades deviate from K41 by a **multifractal** correction: the
per-octave flux multiplier `W` fluctuates, and QLF fixes its law to **log-Poisson / She–Léveque** on
realizability grounds (closures are rare quasi-independent events ⟹ Poisson occupation ⟹ log-Poisson
multiplier, `poissonOccupation`), with `ζ_p = p/9 + 2(1 − (2/3)^{p/3})`, parameters
`μ = 2 − ζ_6 = 0.222`, `β = 2/3`, `C₀ = 2` all **forced**, not fitted (`QLF_Kolmogorov`). Two features
line up: `Δζ(3) = 0` (the 4/5 law is exact), so the clean **3rd-order** term (§7's `9/250` peak) is
*protected*; and the 2nd-moment correction `Δζ(2) = +0.029` is the right sector and scale (`~5α`) for
`δw`. **But it is a lead, not a result:** the step from "intermittency of a velocity field" to
"vacuum-polarization census weight" is a real bridge — which moment `p` vacuum polarization is, whether
its closures are Poisson-occupied in a momentum shell, how `ζ_p` becomes a resummation weight — and the
crude per-order modulations tried so far that land near CODATA were *chosen* (the She–Léveque turnover
factor `(2/3)^{−(n−1)/3}` gives `137.0356`) rather than derived, with `w_impl > 1` signalling the naive
application is wrong. Before any comparison counts, this needs the **R0 pre-registration** of §9a:
the moment identification, the Poisson-occupation check, and the `ζ_p → weight` rule all fixed in a
frozen commit, target **value-free** (the `ζ_2` correction, not `0.035999`). Until then it is the
**most promising open swing** — shared Lean core, forced parameters, right sector — and the first
genuinely new one since the 4-D projection (§8).

---

## 9c. The intermittency swing, pre-registered and run ([`intermittency_bridge.py`](intermittency_bridge.py))

**Pre-registration (R0), frozen at the commit that adds `intermittency_bridge.py`.** The full R0 table
(inputs held fixed, substrate representation, extraction rule, tolerance, comparator, kill condition) is
in the script's header docstring. The essentials: physical input is the 8-twist census and the `/solve`
selection cascade only — **no** use of `α⁻¹(0)`, `137.036`, `0.036` or `w = 0.624`; the comparator is
She–Léveque, forced (`C₀ = 2`, `β = 2/3`, `μ = 2 − ζ₆ = 0.222`, from `QLF_Kolmogorov` /
`Navier_Stokes_Geometry.md` §6a); the target is **value-free** (the parameters and the resulting
`ζ_p`, never `0.035999`). Per Jim's steer, the swing tests the **one** closure the substrate selects
per octave via the handedness listener-listener interaction (`/solve`), not the full-census sum.

**Leg 1 — `C₀`, the codimension of the selected structure: PASS, and it is a *derivation*.** `/solve`
is **axis-minimal** — from a single-axis seed it closes within that one axis, from the vacuum it selects
a 1-D structure (verified across single-axis, multi-axis and gauge seeds). So the selected structure has
codimension `3 − 1 = 2` in 3-D — **She–Léveque's `C₀ = 2`, now derived from the substrate's own
selection rule** (least peak excursion → shortest) rather than posited from "vortex filaments are 1-D".
`Navier_Stokes_Geometry.md` §6a took `C₀ = 2` as "the sole `d`-input"; it is no longer an input.

**Leg 1b — the listener-listener interaction: PASS.** The joint `/solve` of two seeds (the "meeting of
minds", `QucalcSearch.md`) collapses to **one** low-codimension solution — not the union of both
listeners' axis content. Handedness balance selects one solution, which is the "one solution, not all
solutions" the swing is built on.

**Leg 2 — `μ`, the intermittency exponent: run to convergence, and NEGATIVE.** The first-closure census
was pushed to convergence with an **exact transfer recursion** — forward propagation over the state
`(v, h, d, l, inv-parity, max-excursion)`, absorbing at the first return to the origin, phase from
`(−1)^{L/2}·(−1)^{inv}` (for a closure `#neg = L/2` exactly; `inv` = the `QLF_PhaseRule` axis-inversion
parity, its update local because the axis-count parities equal the excursion parities). It reproduces the
brute counts (`8, 104, 2944, 108136, 4525888`, per-phase) exactly, and reaches `R = 11` where the total
first-closure Kraft mass is converged to `M(∞) = 0.18267…`. The per-octave flux multiplier
`W(R) = ΔM(R)/ΔM(R−1)` then reads `0.25, 0.43, 0.52, 0.47, 0.37, 0.28, 0.20, 0.14, 0.09, 0.04` — it rises
to a peak near `R = 4` and then **decays monotonically toward 0**. There is **no inertial range**: the
per-octave census flux does not cascade scale-invariantly, it dies out (the deepest strata hold `O(1)`
closures). So there is no `μ` to extract — not for want of depth, but because the scale-invariant
cascade the swing needs is **not in this census object**. This is the sharper form of §9b: the leading
`log` is not in the Kraft-weighted closure mass, now shown at *converged* depth.

**The seeded census — leg 2 taken to the end of the path, and definitively NEGATIVE.** A turbulent
inertial range needs continuous forcing at an injection scale, so the test was re-posed on a **seeded**
census: start the first-closure recursion from a preparation strand (imbalance = injection scale), for
`R_inj ∈ {0, 2, 4, 6, 8}` and cross-axis `(3,3)`, `(5,5)`. Result: seeding just **shifts the `W(R)`
peak up to `R_inj + 1` and adds a spike** (`W > 1` in the first octave above the seed, because closures
must first clear it), and then `W(R)` **decays monotonically exactly as in the vacuum** — no plateau at
any injection scale. The steady-state reading agrees: the stationary distribution of the capacity-`R`
transfer operator **concentrates near the boundary** (a boundary layer), not scale-invariantly. So the
closure census has **no turbulent inertial range, vacuum or seeded** — the Kraft-weighted closure-flux
is a probability mass that leaks (Kraft bound) and piles up at the floor, not a conserved cascading
quantity. There is no `μ`, and re-posing it will not create one.

**Net.** Leg 1 stands and is real: **`C₀ = 2` is *derived*** from `/solve` axis-minimality (a genuine
contribution back to `Navier_Stokes_Geometry.md` §6a, where `C₀` was "the sole `d`-input"), and the
one-solution handedness selection is confirmed. **Leg 2 is dead**: no cascade in the census, vacuum or
seeded, at converged depth. So the turbulence swing delivered a side-derivation (`C₀`) and **not** the
α-residual magnitude — and the honest landing is §2a's close, now with every mechanism swing exhausted:
**`w = 1/2` is structural; `α⁻¹ = 137.032` is the pure-ZFA prediction; the last `~0.004` (and the full
`+0.036` over `137`) is the continuum vacuum-polarisation running — the Standard Model's own
un-derived precision frontier, which QLF brackets by design.**

---

## 9d. Route (b), explored — the A359801 singularity structure ([`alpha_residual_deep.py`](alpha_residual_deep.py), route_b probe)

Route (b) asks for an *exact* substrate self-consistency rather than an order-by-order sum. The
[OEIS A359801](https://oeis.org/A359801) identification (§9b) hands over the raw material: the prime
census has a **closed-form generating function** `P(x) = 1 − 1/Q(x)`, `Q(x) = ∫₀^∞ e^{−t} I₀(2t√x)⁴ dt`
(the ℤ⁴ worldline / Schwinger integral), radius `1/64`. One real gain and one honest miss:

- **The QED log is *not* an external input — it is the `d = 4` marginal singularity type, shared.**
  `Q(x)`'s singular term at `x = 1/64` is `−κ·(1−64x)·log(1/(1−64x))` with `κ = 2/π²` (confirmed
  numerically: `A039699(n)·n²/64ⁿ → 0.2026`, the local-CLT constant `2·2⁴·(2π)^{−2}·(¼)^{−2}`). `d = 2`
  gives a *divergent* log (recurrent), `d = 3` a `√` (no log), `d = 6` no singular log — **`d = 4` is the
  first even dimension whose closure-return g.f. carries a logarithm**, for exactly the reason QED's
  coupling runs logarithmically in `d = 4` (marginal, dimensionless). §9b's table called the log "an
  information-theoretic input the prime census does not itself derive"; this locates its *origin* — the
  substrate being 4-dimensional (`v,h,d,l`) — even though the coefficient is still not delivered.
- **The coefficient still misses (naive).** The first-return singular constant is
  `B_P = κ·(1−p)² ≈ 0.132` (`p = p_return(ℤ⁴) ≈ 0.193206`, the `Z_limit` of §9b). Against the QED
  one-loop log coefficient this is `B_P / (2/3π) = 3(1−p)²/π ≈ 0.6216`. That is *close to* the §2a
  weight `w ≈ 0.624` — but misses at the third digit, so it goes in the same drawer as the §6b/§9
  one-term coincidences: **flagged, not built on** (method rule 4 — an exact identity would not miss).
- **The renewal = Dyson identity is exact.** `Q(1/64) = 1/(1−p) = G(0,0)` is the lattice Green's
  function, the geometric sum of 1PI first-returns — the lattice analogue of `1/(1−Π(0))`. So
  `Z_limit = p_return(ℤ⁴)` is the substrate's `Π(0)`, an exact closed-form number.

**Positive geometry — scoped, and the right object is *not* the cosmohedron.** `Q(x)` is not a
Tr(φ³) wavefunction (the cosmohedron's setting — an interacting, multi-kinematic-variable rational
function; wrong theory, wrong variable count). It is a **Bessel moment**: `∫₀^∞ e^{−t} I₀(2t√x)⁴ dt` is
the generating function of the **4-D hypercubic lattice Green's function**, equivalently the **3-loop
banana Feynman integral** family (four Bessel factors = four propagators). This is heavily studied —
Bailey–Borwein–Broadhurst–Glasser ([arXiv:0803.1007](https://arxiv.org/abs/0803.1007)) tie 4-D lattice
integrals directly to **4-loop g−2 master integrals**, the QED precision sector the residual lives in;
Glasser–Guttmann ([arXiv:cond-mat/9408097](https://arxiv.org/abs/cond-mat/9408097)) give `Q(1/64) =
G_{ℤ⁴}(0)` in closed hypergeometric form. The associated geometry is a **K3 surface**, `Q(x)` satisfies a
**4th-order Picard–Fuchs ODE** whose singular points are the closure "octave" thresholds
(`x = 1/4, 1/16, 1/36, 1/64`), and its special values are periods / critical L-values of a weight-3
modular form (Broadhurst–Mellit). The scoped calculation: (1) the P–F ODE for `Q(x)` (in the
lattice-Green literature / via `HolonomicFunctions`); (2) its local exponents at `x = 1/64` — the
`(1−64x)log` we found is a resonance (Jordan block) in the local monodromy, the d = 4 marginal signature;
(3) whether the ODE's connection constants or the modular L-values reproduce `2/(3π)` or the two-loop
`−0.328` cleanly. Weeks, not a script, but concrete first moves and the right physics.
