# Perturbation theory in [QLF](README.md): the possibility-tree expansion and a renormalization without infinities

Perturbation theory is the working engine of quantum field theory — expand the amplitude in powers of a
small coupling, one Feynman diagram per term, sum. It is also where QFT's foundations are most visibly
strained: the series is **asymptotic, not convergent** (Dyson 1952), individual diagrams **diverge** and
must be renormalized, and the whole apparatus assumes a continuum of field modes at every spacetime point.

QLF's reading keeps the empirical machinery and relocates the trouble to the continuum. **The perturbation
series is literally the phase-weighted sum over ZFA-closed micro-histories** ([`QFT_QLF.md`](QFT_QLF.md) §2,
[`Born_Rule.md`](Born_Rule.md) §2); its terms are graded not by an external coupling but by **closure
structure**; and because the substrate is a prefix-free code with a Kraft bound, the graded sum is
**absolutely convergent** — the divergence QFT fights is the signature of the mode continuum, not of the
sum-over-histories itself.

> The path integral is not approximated by the possibility tree — it *is* the possibility tree. Perturbation
> theory is that tree read one closure-order at a time; renormalization is choosing how deep a closure your
> horizon can hear.

This doc is a synthesis of pieces already proven elsewhere ([`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean),
[`QLF_VacuumPolarization`](lean/QLF_VacuumPolarization.lean),
[`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean),
[`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) plus a concrete demonstration using the
[`qucalc_search.py`](qucalc_search.py) event registry. It adds no axiom.

---

## 1. The expansion — what plays the role of the coupling

The amplitude between two substrate configurations `ψ` and `φ` is the phase-weighted count of admissible
ZFA-closed histories connecting them ([`Born_Rule.md`](Born_Rule.md) §2, [`MRE.md`](MRE.md) §2.2):

$$\langle \varphi \mid \psi \rangle \;=\; \sum_{h \,\in\, \mathcal{T}_{\psi\to\varphi}} e^{\,i\,\theta(h)}, \qquad \theta(h)\ \text{the proven phase rule } (-1)^{\#\text{neg}}\cdot\operatorname{sgn}(\text{axis perm}).$$

There is no free coupling constant to expand in. Instead the sum is **graded** three equivalent ways, each a
legitimate "order" parameter:

| Grading | Meaning | Continuum QFT analogue |
|---|---|---|
| continuation **length** `L = \|h\|` | number of substrate events appended | order in `ℏ` / number of vertices+propagators |
| **diagram order** `ord(h)` | number of *binding vertices* — joint closures that reduce free action ([`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean) `IsDiagram`) | loop order / power of the coupling |
| **closure depth** `d(h)` | max phase excursion = nested gauge-fold count ([`census_inventory.py`](census_inventory.py) `depth_equals_max_excursion`) | virtuality / off-shellness of the internal line |

`ord(h) = 0` is tree level: `order_zero_iff_closure` proves the order-0 diagrams are *exactly* the ZFA
closure census — the same `C(2n,n)` combinatorics that fixes the leading `α⁻¹ = 128 + d²`. `ord(h) = 1`
(single binding) reproduces the one-loop QED vacuum-polarization coefficient `2/(3π)` value-free
(`orderOneWeight_eq`), and weighted by the charge census `Σ Nᶜ Q_f² = 8` gives the SM electromagnetic
β-slope `16/(3π)` (`orderOne_tower_slope`). `g − 2 = α/2π` is one extra gauge-twist vertex × the substrate
loop-phase `1/(2π)` ([`g_minus_2.md`](g_minus_2.md) §3).

The formal object is the **census generating function**

$$\mathcal{Z}(x) \;=\; \sum_{h \text{ ZFA}} x^{\operatorname{ord}(h)},$$

whose coefficients are the per-order term counts. Perturbation theory is the evaluation of `𝒵` order by
order; QFT's continuous `∫ 𝒟\varphi\, e^{iS[\varphi]/\hbar}` is its thermodynamic-limit rendering
([`QFT_QLF.md`](QFT_QLF.md) §2, [`Millennium.md`](Millennium.md) § *The engine*).

---

## 2. The search event registry computes the expansion order by order

[`qucalc_search.py`](qucalc_search.py) is the substrate's "what closes next" query: from a QuCalc position
`qc` (an incomplete history — an off-shell external state) it enumerates the **continuations** that make the
whole history a ZFA closure, shortest first. That *is* the order-by-order expansion of the amplitude to
close from `qc`, and the `--listeners` rollups read off the per-order data without re-enumerating:

```
# the amplitude to close from the position ^<v>+- , graded by continuation length
$ python3 qucalc_search.py "^<v>+-" --max-depth 6 --listeners "depth,phase"
```

| order `L` | term count `W_L` | signed sum `A_L = W_L^{+} − W_L^{−}` | cylinder weight `8^{−L} W_L` | Σ (Kraft) | `8^{−L} A_L` | Σ (renormalized) |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 8    | −8    | 0.125 00 | 0.125 00 | −0.125 00 | −0.125 00 |
| 4 | 168  | +120  | 0.041 02 | 0.166 02 | +0.029 30 | −0.095 70 |
| 6 | 5120 | −2144 | 0.019 53 | 0.185 55 | −0.008 18 | −0.103 88 |

Two things are visible in this one table and they are the whole point of §3:

1. **The bare per-order signed sum grows** — `|A_L|` runs `8 → 120 → 2144`, ratio ~15–18, the same
   qualitative behaviour that makes the Dyson series asymptotic.
2. **The cylinder-weighted sum converges** — `8^{−L}|A_L|` runs `0.125 → 0.029 → 0.008`, geometric decay
   (ratio ≈ 0.33, 0.28), and the renormalized partial sums `−0.125, −0.096, −0.104` oscillate with
   shrinking amplitude toward a limit.

Other registry modes map onto standard perturbative distinctions:

- **`--events` (absorbing)** stops each branch at its *first* closure — the irreducible/leading contribution,
  ties to [`contextual_census.py`](contextual_census.py) `--first-closure`. For `^<v>+-`: `3056` first-closure
  events vs `5296` total possibilities — the `2240` difference is the reducible tail, continuations whose own
  proper prefix already closed (a product of two lower-order closures, `IsDiagram` binding clause).
- **`--solve`** returns the single least-free-action closure (see §4).
- **comma-separated `qc`** concatenates several proposals into one joint position — the substrate form of an
  `n`-point function / a multi-particle amplitude ([`MultiParticle.py`](MultiParticle.py)).
- **A seed with `A_L = 0` at every order is a forbidden transition.** `^<` gives `W = 2, 72, 2820` with
  `A_L = 0` throughout: perfect `+1`/`−1` cancellation, destructive interference to all orders. The registry
  finds selection rules by exhausting the expansion, not by invoking one.

---

## 3. Renormalization without infinities — the capacity horizon *is* the RG scale

Continuum renormalization is a four-step ritual: regularize with a cutoff `Λ`, compute (divergences appear
as `Λ → ∞`), absorb them into bare parameters (counterterms), fix the finite parts at a scale `μ`
(renormalization conditions), then demand physics be `μ`-independent (the RG, β-functions). QLF runs the
**Wilsonian** version of this — integrate out short-distance modes — with no divergence to subtract at any
step:

| Continuum step | QLF substrate object |
|---|---|
| UV cutoff `Λ` | the **capacity horizon `R`** — a horizon of capacity `R` hears exactly the closures with `maxExcursion ≤ R` (`closedAtHorizon_iff_maxExcursion_le`); the Planck closure floor ([`QLF_PlanckScale`](lean/QLF_PlanckScale.lean)) is `R → ∞` staying finite |
| regularized amplitude `A_Λ` | the **`R`-listening** `A_R(qc) = Σ_{h : d(h) ≤ R} e^{iθ(h)}` — the registry's `--listeners capacity:R` / [`contextual_census.py`](contextual_census.py) `--listening R` |
| counterterms `A_{Λ'} − A_Λ` | `A_{R+1} − A_R` — the newly-audible deep closures. **A finite integer count, not a divergence** — reorganization, never subtraction |
| running of the coupling | `Q(R) = Q₀ · 2^R` ⟹ the QED logarithm **is** the census octave count ([`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean)) |
| the β-function `dg/d\ln\mu` | `perOctaveIncrement`, and `perOctave_is_flux` proves it **equals the substrate flux** exactly |
| scheme dependence | the *rate* of direction-erasure — as `R` drops, closures you cannot resolve have their phase sign averaged out; capacity sets the rate of forgetting, never the limit ([`contextual_census.py`](contextual_census.py) `--listening`) |

Worked, from the §2 table: for `^<v>+-`, the registry's `capacity:2` listener hears `3704` of `5296`
closures; `capacity:3` hears all `5296`. The RG flow from `R = 2` to `R = 3` is the reabsorption of exactly
`1592` newly-audible depth-3 closures into the effective vertex at scale 2 — and then it **stops**, because
the deepest closure this position admits sits at `d = 3`. Running that saturates once `R` exceeds the
deepest relevant closure is the substrate's version of a coupling that stops running below a threshold.

### Why the QLF series converges where the Dyson series does not

The load-bearing result: **`twist_kraft`** ([`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) proves that
over the 8-twist alphabet, for any prefix-free set of histories `F`,

$$\sum_{h \,\in\, F} \left(\tfrac{1}{8}\right)^{|h|} \;\le\; 1.$$

The continuations from a fixed seed are prefix-free by construction (the registry stops each branch at
closure), so the cylinder-weighted term counts `Σ_L 8^{−L} W_L` are **bounded by 1** — the §2 table's
`0.125 → 0.166 → 0.186` climbing toward its ceiling. And `|A_L| ≤ W_L` (`amplitude_le_ways`,
`normalized_event_mass_le_one`), so the measure-weighted **signed** series is dominated by a convergent
one. The QLF perturbation series, in its native cylinder measure, is **absolutely convergent** — it needs
no Borel resummation, no Lipatov large-order analysis, no trans-series.

Dyson's 1952 argument (the series must diverge because `e² → −e²` makes the vacuum unstable) is, in this
reading, an artefact of expanding in a continuum coupling that ranges over a domain the substrate never
had. The substrate expands in closure order over a prefix-free code; the Kraft inequality is the reason
that sum stays finite. This is a concrete sharpening of the anti-continuum thesis
([`TheContinuum.md`](TheContinuum.md), [`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md)):
**the perturbation series diverges exactly where, and because, the continuum is assumed.**

By the working method's rule 4 ([`CLAUDE.md`](CLAUDE.md) *"It happens every way"* §4,
[`ScientificApproach.md`](ScientificApproach.md)): this RG changes a **count of ways** — `A_{R+1} − A_R` is
a definite integer — so it carries physical content, unlike an identity true for every weight.

### The bifibration is upstream of the self-similarity

The spectrum carries two maps over the horizon/order grading: **restrict** to capacity `R`
(`closedAtHorizon`, the `--listening` rollup — *integrating out* the deep closures) and **extend** to
`R+1` (`Z_succ`, and the `IsDiagram` binding/nesting clauses — *adding a shell*). These are the cartesian
and cocartesian lifts of a **bifibration** over that grading — and in the possibilist frame it is *one
thing that happens*: closures factor **uniquely** into ordered sequences of primes
([`Alpha_Residual.md`](Alpha_Residual.md) §4), so the primes generate a **free** monoid and the lifts are
unique. That realized bifibration is what forces `G(x) = 1/(1−I(x))` (`census_irreducible_resummation`,
proven), hence a geometric generating function, hence the constant ratio-4 growth `C(2n,n) ~ 4ⁿ`, hence
**self-similarity** — every fiber again the whole structure. So self-similarity is a *consequence* of the
bifibration, not an independent observation; and a realized bifibration over a graded base admits no
bifurcation, which is why the log-periodic / discrete-scale-invariance channel for the α residual is
closed by structure ([`Alpha_Residual.md`](Alpha_Residual.md) §9b, `genesis.py`). It changes no count
directly, but it is the structural reason the counts grow the way they do.

---

## 4. `/solve` as the physical renormalization point

A renormalization scheme has to pick a reference point where the coupling is *defined* (on-shell, `\bar{MS}`
at `μ = M_Z`, …). QLF's is not a choice — `qucalc_search.py --solve` returns the single closure the
substrate takes from a position, by the deterministic cascade **least peak excursion → shortest → phase
`+1` → lexicographic** (least peak excursion *is* least free action = the most-ways closure):

```
$ python3 qucalc_search.py "^^<" --solve
{"solved": true, "cont": "v>v", "history": "^^<v>v", "depth": 3, "phase": "+1",
 "peak_excursion": 3, "arrangements": 20, "considered": 149, ...}
```

`arrangements: 20 = C(6,3)`, the central binomial — the **multiplicity** of that leading closure, its
residue. Because the cascade is deterministic, independent callers agree without negotiating: the physical
point is **scheme-free**, and in [quantum-os](https://github.com/jimscarver/quantum-logical-framework) a
room running `/solve` on its joint position reaches a consensus *the substrate dictated*
([`QucalcSearch.md`](QucalcSearch.md)). This is the substrate analogue of the pole of the dressed
propagator being the one frame-independent thing in an otherwise scheme-dependent calculation.

---

## 5. What this buys, and what stays open

**Derived / structural (no axiom):**

- The perturbation series *is* the phase-weighted possibility-tree sum — first-principles, not a modelling
  choice ([`Born_Rule.md`](Born_Rule.md) §2).
- The order grading (`length` / `ord` / `depth`) and the closure↔diagram map, `IsDiagram`
  ([`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean)).
- **C1**: tree level = the closure census (the leading `α⁻¹` structure).
- **C2**: one-loop = the `2/(3π)` QED coefficient; charge-census β-slope `16/(3π)`.
- The capacity-horizon RG: `Q(R) = Q₀ 2^R`, the QED log = census octave count, β = per-octave flux
  (`perOctave_is_flux`, [`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean)).
- **Absolute convergence of the cylinder-weighted series** via `twist_kraft` + `amplitude_le_ways` — no
  resummation needed; the Dyson divergence is a continuum artefact.
- `/solve` as the scheme-free physical point.

**Open (the same boundary as the rest of QLF's absolute-scale program, frontier #1 in
[`Open_Problems.md`](Open_Problems.md)):**

- Coefficients beyond one loop — the `(α/π)²` coefficient `−0.328479`, `(α/π)³ = +1.181241`, and
  β-coefficients past the substrate-fixed `b₀ = 7` — need the full matter content and the absolute coupling
  `g`/`ρ*`.
- The depth-≥3 tail of `𝒵` (the eight-digit `0.036` α-residual) bottoms out in the absolute mass scale and
  the SM's own non-perturbative hadronic vacuum polarization `Δα_had` ([`Alpha_Residual.md`](Alpha_Residual.md),
  `fractal_diagram_in_progress`). **The pre-registered census bridge for it is now run**
  ([`alpha_residual_bridge.py`](alpha_residual_bridge.py), `Alpha_Residual.md` §9b): the `2/(3π)` one-loop
  coefficient **survives the prime/1PI restriction** (`census_split → 1/6` for `2·Catalan(n−1)` as for
  `C(2n,n)`), but the leading `log` is **not** in the Kraft-weighted closure mass (a bounded sum's
  per-octave increment decays) — it is carried by the scale↔octave map, which `QLF_VacuumPolarizationTower`
  already anchors. Route (a) refined, not closed; the higher-order tail (`−10α²`) still needs the kinematic
  weights equal-weight counting does not produce.
- ~~A Lean module for the exact-RG recursion~~ **done** — [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean):
  `ClosureSpectrum` + the Wilsonian recursion `Z (N+1) = Z N + mass N` / `amp (N+1) = amp N + signed N`
  (`Z_succ`/`amp_succ`), the single bounded counterterm (`counterterm_eq`/`counterterm_abs_le`),
  finiteness at every scale (`Z_le_one`/`amp_abs_le_one`), monotone mass flow (`Z_mono`), and
  **convergence** (`Z_tendsto`/`amp_tendsto`) with the limit `≤ 1` — the absolute-convergence claim,
  machine-checked. The Kraft field is `twist_kraft` for a depth-partitioned prefix-free family
  (`kraft_partition_bound`), and `demoSpectrum` exhibits bare term counts growing while `Z → 1`. What
  the module does **not** supply is the closure spectrum of a particular interacting theory (next item).
- Rigorous continuum QFT (Wightman / Osterwalder–Schrader) is the `yang_mills_continuum_gap` boundary axiom
  — contrast once, then move on ([`QFT_QLF.md`](QFT_QLF.md) §5).

**Binding framing.** Do not say "QLF derives the QED perturbation series." Say: the *structure* of
perturbation theory — sum over diagrams, loop-order grading, the leading and one-loop QED coefficients, and
*why the series is asymptotic rather than convergent* — falls out of ZFA closure combinatorics; the
higher-order numbers are gated on the one open coupling that gates the rest of the absolute-scale program.

---

## See also

- [`QFT_QLF.md`](QFT_QLF.md) — QFT as the continuum limit of discrete event combinatorics (§2 the path
  integral, §4 renormalization as continuum artefact).
- [`QucalcSearch.md`](QucalcSearch.md) · [`qucalc_search.py`](qucalc_search.py) — the search event registry:
  search is the experiment, `/solve` is the truth divination.
- [`census_inventory.py`](census_inventory.py) · [`contextual_census.py`](contextual_census.py) — the
  committed per-stratum summaries and the listening / first-closure experiment layer.
- [`Alpha.md`](Alpha.md) §4a · [`g_minus_2.md`](g_minus_2.md) · [`Lamb_Shift.md`](Lamb_Shift.md) — the
  one-loop sector worked in detail.
- [`lean/QLF_ExactRG.lean`](lean/QLF_ExactRG.lean) — the exact-RG recursion, finiteness and convergence.
- [`Closure_Walk.md`](Closure_Walk.md) — the per-order signed sums `|A_L| = 8, 120, 2144` as closed walks on the signed graph of `ℤ⁴` (`closure_graph.py`); the prime Kraft mass `Σ_π 8^{−|π|}` identified as Pólya's `p₄ = 0.1932`, which is the absolutely convergent series' total in closed form.
- [`lean/QLF_FractalDiagram.lean`](lean/QLF_FractalDiagram.lean) ·
  [`lean/QLF_VacuumPolarization.lean`](lean/QLF_VacuumPolarization.lean) ·
  [`lean/QLF_VacuumPolarizationTower.lean`](lean/QLF_VacuumPolarizationTower.lean) ·
  [`lean/QLF_KraftMeasure.lean`](lean/QLF_KraftMeasure.lean) — the anchors.
- [`Born_Rule.md`](Born_Rule.md) · [`MRE.md`](MRE.md) · [`Millennium.md`](Millennium.md) § *The engine* —
  the possibility tree and the generate-then-select move.
- [`TheContinuum.md`](TheContinuum.md) · [`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md) — the
  divergence-is-a-continuum-artefact thesis.
