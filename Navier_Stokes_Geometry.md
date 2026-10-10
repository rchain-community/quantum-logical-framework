# The geometry of Navier–Stokes — angular momentum, vorticity, and where QLF avoids the infinity

The dynamics of the substrate geometry ([`Geometry_Of_Space.md`](Geometry_Of_Space.md)) are rotational,
and the [Quantum Logical Framework](README.md) (QLF) already carries the right objects. This doc
formalizes **angular momentum conservation**, then reads the **Navier–Stokes** geometry off it — and
shows precisely **where QLF avoids the blow-up** and **what correction it makes**. The structural
spine is machine-verified in [`lean/QLF_AngularMomentum.lean`](lean/QLF_AngularMomentum.lean).

---

## 1. Angular momentum = circulation

`baryonNumber` ([`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean)) is a **sliding-window sum of
`signTriple`** — the oriented all-three-axes sign (`+1` cyclic `(x,y,z)`, `−1` anticyclic, `0`
otherwise), the discrete **Levi-Civita curl** of three consecutive twist-axes. Summed over the path it
is the **signed 3-axis winding** — orbital angular momentum, the **Kelvin circulation** of the twist
flow, the Noether charge of the substrate's rotational `su(2)` symmetry (`su2_comm_xy`, `QLF_Spin`).

- **`circulation := baryonNumber`** — angular momentum. Calibrated: the Borromean proton `>^/` carries
  `+1`, its antiparticle `−1` (`baryon_antiproton`), a meson `q q̄` cancels to `0` (`baryon_meson`).
- **`circulation_reverses_under_time_reversal`** — angular momentum is a **pseudovector**: time-reversal
  / parity (`antiparticle` = conjugate-and-reverse) flips it, `L → −L`. This is the defining
  transformation of angular momentum, and it is exactly `baryon_dagger_odd` re-read.

So the conserved rotational charge of the geometry is the circulation, T-odd as angular momentum must be.

## 2. Vorticity is the discrete curl — and it is quantized

In fluid dynamics the **vorticity** `ω = ∇×v` is the local rotation rate — the angular momentum density.
On the substrate it is exactly the local curl cell:

- **`vorticity a b c := signTriple (axOf a) (axOf b) (axOf c)`** — the oriented all-three-axes sign of
  three consecutive twist-axes, the per-cell circulation.
- **`vorticity_antisymmetric`** — reversing the cell flips the sign (`ω(c,b,a) = −ω(a,b,c)`): a curl is
  orientation-odd, as it must be (`signTriple_rev`).
- **`vorticity_quantized` — `|ω| ≤ 1`.** Every cell carries **at most one circulation quantum**
  (`signTriple ∈ {−1, 0, +1}`). The vorticity is *quantized*.

## 3. Where QLF avoids the Navier–Stokes infinity

The Clay Navier–Stokes problem is whether a smooth incompressible flow can develop a **finite-time
singularity** — and the sharp criterion (Beale–Kato–Majda) is exactly **vorticity blow-up**: a
singularity forms iff `∫ ‖ω‖_∞ dt → ∞`, i.e. iff the vorticity becomes **unbounded**.

On the substrate that cannot happen:

- **Local: `ω` is capped at one quantum per cell** (`vorticity_quantized`, `|ω| ≤ 1`). There is no
  `ω → ∞` because there is a smallest, largest circulation a cell can hold. The blow-up criterion is
  *unsatisfiable* on the discrete geometry.
- **Global: angular momentum in a finite region is finite** (`circulation_bounded`, `|L| ≤ n`). A
  length-`n` history holds at most `n` circulation quanta — no runaway angular momentum.
- **The continuum's singular vorticity is unrealizable** (`continuum_vorticity_unrealizable`): a
  continuum vorticity value is a real number (`Infinite ℝ`), but a substrate cell holds finite
  information (`Finite R`), so there is **no faithful realization** of an `ℝ`-valued vorticity in a
  finite cell ([`no_continuum_in_finite_region`](lean/QLF_Realizability.lean)).

This gives the existing result `realized_flow_is_stable` ([`QLF_NavierStokes`](lean/QLF_NavierStokes.lean) —
"no realized flow blows up") its **geometric mechanism**: a blow-up would require unbounded vorticity,
and vorticity is capped at one quantum per cell.

## 4. The nature of the correction

The continuum permits `ω → ∞` because it models vorticity as a **real field with no smallest quantum** —
arbitrarily fine, arbitrarily intense rotation concentrated at a point. The substrate **quantizes
circulation to `±1` per cell** and bounds the count per region. That **discreteness is the correction** —
not a regularization bolted on, but the substrate's native floor. It is the *same* cutoff that removes
the ultraviolet catastrophe and the `10¹²²` vacuum catastrophe ([`TheContinuum.md`](TheContinuum.md)):
wherever the continuum produces an infinity by allowing unbounded fineness, the discrete substrate caps
it. The Navier–Stokes would-be singularity is one more instance — and the cap is *angular-momentum
quantization*.

## 5. Deriving the bridge — the Planck cap + Beale–Kato–Majda

The original module posited `navier_stokes_continuum_limit` as one opaque axiom ("the continuum inherits
the substrate's no-blow-up"). With the vorticity quantization in hand, [`QLF_NavierStokesBKM`](lean/QLF_NavierStokesBKM.lean)
**unbundles it into three transparent pieces** — *deriving* the no-blow-up rather than positing it:

1. **Proven (substrate arithmetic, no axiom).** Physical vorticity = circulation quantum / cell area.
   The quantum is `≤ 1` (`vorticity_quantized`) and the cell area is `≥ L_P²` (the Planck floor — no
   coherent sub-Planck cell, [`QLF_PlanckScale`](lean/QLF_PlanckScale.lean)), so physical vorticity is
   **`≤ 1/L_P²`** (`planck_caps_vorticity`): a fixed, *uniform-in-time* cap. The per-cell bound *with a
   smallest cell* is a uniform cap — there is no `ω → ∞`.
2. **Cited (a real theorem, not a QLF posit).** **Beale–Kato–Majda (1984):** a uniform-in-time vorticity
   bound ⟹ the BKM integral `∫₀ᵀ ‖ω‖_∞ dt ≤ M·T` is finite on every `[0,T]` ⟹ no finite-time
   singularity (`beale_kato_majda`). QLF carries no PDE machinery in Lean, so BKM is *cited* — exactly as
   Wallis/Stirling are cited for `π`.
3. **The sharp bridge (the residual gap).** The continuum solution's vorticity *is* the Planck-capped
   substrate vorticity (`continuum_vorticity_planck_capped`) — QLF's continuum-as-rendering thesis applied
   to the vorticity field. Small and precise, it **replaces** the opaque axiom.

From these, **`navier_stokes_no_blowup` is a theorem.** This directly answers *"is the semi-fractal
geometry sufficient?"*: **yes at the fixed Planck floor** — the cap *is* the floor, and there the
no-blow-up follows. The Clay statement lives in the unfloored `v → ∞` limit, which is precisely the
singular limit where a per-cell bound degenerates — and that is exactly the rendering step (3). So the
bridge is not eliminated but **localized**: from "the whole continuum inherits no-blow-up" down to "the
continuum vorticity is the Planck-capped substrate vorticity," with the mechanism explicit and BKM cited.

## 6. Turbulence — the quantized-vortex tangle and the frequency cascade

The same vorticity quantum reframes **turbulence** ([`QLF_Turbulence`](lean/QLF_Turbulence.lean)). First,
the crucial distinction: **it is all Navier–Stokes — but two different questions.** Both turbulence and
the Clay problem are the *same equations*; they split into

- the **regularity** question — global existence & smoothness / no finite-time blow-up. *This* is the
  Clay Millennium problem, and §5 reduces it (vorticity cap + BKM); and
- the **statistics** question — the `−5/3` Kolmogorov spectrum, intermittency, anomalous dissipation.
  *This* is "the turbulence problem," a **distinct and also-open** question, **not** the Clay one.

The vorticity quantum is the one lever under both:

- **Turbulence is a tangle of quantized vortices.** A vortex line is one circulation quantum
  (`vortex_quantum`, `|ω| ≤ 1`); total circulation is an *integer* count of net quanta
  (`circulation_integer_quantized`, `baryonNumber ∈ ℤ`). So the vorticity field is a discrete line-tangle,
  not a continuum — **Onsager–Feynman quantization** (verified in superfluid `He`/BECs) derived from the
  substrate. This makes **classical turbulence the coarse-grained limit of quantum turbulence**, which is
  why superfluid turbulence reproduces the classical Kolmogorov cascade.
- **The cascade is a frequency hierarchy.** An eddy of scale `R` is a closure of frequency `f = 1/R`;
  down the cascade (smaller eddies) the frequency increases (`cascade_frequency_increases`), bounded above
  by the dissipation floor (`cascade_capped` — the Kolmogorov scale, ultimately Planck). Dissipation is
  vortex **reconnection** (a ZFA closure) at the floor, radiating Kelvin waves — the superfluid-turbulence
  mechanism, and the same cap that removes the blow-up.

So the regularity side is *reduced* (§5); the statistics side is *structurally reframed* here
(quantized tangle, frequency cascade, classical = coarse-grained quantum) and taken one concrete,
falsifiable step further in §6a.

## 6a. The −5/3 spectrum and intermittency from self-similar closure statistics

The frequency cascade of §6 is a hierarchy of **fractal ZFA closures at every scale**, and Kolmogorov's
theory *is* a self-similarity statement — so the closure hierarchy has real quantitative content here.
Computation: [`turbulence_intermittency.py`](turbulence_intermittency.py).

**The `−5/3` spectrum, from closure-flux scale invariance.** K41 needs one premise: the energy flux
through the inertial range is scale-invariant. QLF supplies exactly that — each closure carries `log 2`
([`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean)), and if the energy passed from frequency-`f` closures to
their `2f` sub-closures is `f`-independent across the inertial range (the closure hierarchy is exactly
self-similar between injection and the `cascade_capped` floor), then dimensional analysis gives
`E(k) ~ ε^{2/3} k^{−5/3}`. The QLF-specific object is the **flux-invariance lemma** — closure-flux is
octave-independent in the inertial range — now **machine-verified** ([`QLF_Kolmogorov`](lean/QLF_Kolmogorov.lean), `flux_scale_invariant`: the per-closure energy is the octave-independent `log 2` quantum, so a scale-invariant transfer count gives octave-independent flux, sitting on the reused `cascade_frequency_increases`); the `−5/3` exponent is then K41's standard corollary — and *that* is a theorem too: **`kolmogorov_exponents`** proves `(a,b) = (2/3, −5/3)` is the **unique** solution of the dimensional constraints on `E(k) = ε^a k^b` (`−3a = −2`, `2a − b = 3`). The hard invariant every closure model must pass is
`ζ_3 = 1` (the exact `4/5` law), which holds because `⟨W⟩ = 1` *is* flux conservation (`log 2` per
closure, conserved down the cascade).

**Intermittency — where the fractal reading bites.** Real turbulence deviates from the K41 monofractal
`ζ_p = p/3` because the cascade is **multifractal**, not monofractal — precisely "fractal closures at
many frequencies, not one." In the random-multiplier framework (`ζ_p = p/3 − log₂⟨W^{p/3}⟩`, with
`ζ_3 = 1` forced), the deviation is the distribution of the per-octave flux multiplier `W`, which QLF
must supply from closure statistics. The computation compares the candidates against measured exponents:

| `p` | K41 `p/3` | She–Leveque (C₀=2, β=⅔) | measured |
|---|---|---|---|
| 2 | 0.667 | 0.696 | 0.70 |
| 4 | 1.333 | 1.280 | 1.28 |
| 6 | 2.000 | 1.778 | 1.78 |
| 8 | 2.667 | 2.211 | 2.13 |

K41 misses at high `p` (RMS 0.242 vs measured) — **that deficit is the intermittency**. The
**parameter-free She–Leveque** log-Poisson cascade fits (RMS 0.029), and its one structural input is
**`C₀ = 2 =` the codimension of the most singular structures = 1-D vortex *filaments* in 3-D space
(`3 − 1 = 2`)** — an object QLF *already has*: its vortex lines are quantized 1-D filaments
(`vortex_quantum`, `circulation_integer_quantized`, Onsager–Feynman). So the parameter the fit needs is
**grounded in the substrate, not fitted**; the log-normal route instead needs `μ ≈ 0.231` (measured
`~0.25`), reducing intermittency to a single number — the **census variance of realized closures per
octave** (`C(2n,n)/4ⁿ` fluctuations).

**Why She–Leveque and not log-normal — closure statistics *select* the class.** The two candidates are not on equal footing. Closures are **rare, quasi-independent events** in a region, so their occupation is **Poisson** — the very object already verified for the causal-set curvature limit (`poissonOccupation`, [`QLF_CausalContinuum`](lean/QLF_CausalContinuum.lean)). A Poisson-multiplier cascade is **log-Poisson** (Dubrulle 1994), *not* log-normal — and log-Poisson with the grounded `C₀ = 2` is exactly She–Leveque. This is decided on **realizability**, not just goodness-of-fit: at high `p` the log-normal `ζ_p` **turns over and decreases** (past `p ≈ 14.5` for `μ = 0.23`), violating the requirement that `ζ_p` be non-decreasing, whereas She–Leveque stays monotone with asymptotic slope `1/9` (the minimum Hölder exponent of the most-singular structures). So QLF's Poisson closure statistics *pick out* the physically correct log-Poisson class and rule the log-normal out — the same "the continuum/unbounded object is unphysical, the discrete one is realizable" move as everywhere in QLF ([`QLF_Realizability`](lean/QLF_Realizability.lean)). The one residual free input is then `β = 2/3`.

**The two log-Poisson parameters, anchored — with their origins kept distinct** ([`QLF_Kolmogorov`](lean/QLF_Kolmogorov.lean)). She–Leveque has exactly two inputs, `C₀` and `β`, and — correcting an earlier conflation — they have **different** origins:

- `C₀ = 2 = d − 1` — the codimension of the most-singular structures, the **1-D vortex filaments** in `d`-space (QLF's quantized vortex *lines*, `vortex_quantum`). This is the **only genuinely `d`-dependent** parameter; at `d = 3`, `C₀ = 2` (`she_leveque_codimension`). **And it is now *derived*, not posited from "vortex filaments are 1-D"**: the substrate's own selection rule `/solve` (least peak excursion → shortest) is **axis-minimal** — from any single-axis seed it closes within that one axis, so the closure the substrate takes is a **1-D structure**, codimension `d − 1 = 2` ([`intermittency_bridge.py`](intermittency_bridge.py) leg 1, `Alpha_Residual.md` §9c, verified across 21 seeds). `C₀ = 2` falls out of the closure-selection cascade, not from an identification made by hand.
- `β = 2/3 = 1 − h` — the **eddy-turnover-time exponent**, where `h` is the velocity Hölder exponent of `δv_ℓ ~ (ε ℓ)^{1/3}`. That `1/3` is **dimensional** — it is the cube-root of the flux `[ε] = L²T⁻³`, the *same* `1/3` behind `−5/3` (`velocity_holder_exponents`: `(c,h)=(1/3,1/3)` forced by `−3c=−1`, `2c+h=1`, exactly as `kolmogorov_exponents` gives `a = 2/3 = 2c`). It is therefore **dimension-independent**, **not `1/d`**. So `β = 2/3` does *not* come from the 3 spatial axes — `she_leveque_beta`: `1 − h = 2/3`.

So `μ = 2 − ζ_6 = 0.222` and the whole `ζ_p` curve follow with **no free parameter**: `β` from the machine-checked dimension-independent velocity exponent (the same `1/3` as `−5/3`), `C₀` from the `/solve` axis-minimality (no longer even a `d`-*input* — it is a *consequence* of the closure-selection cascade). **Honest caveat (the residual posit):** that `β` *equals* the turnover exponent — She–Leveque's identification of the most-singular flux with the inverse eddy-turnover time — is standard turbulence phenomenology, not re-derived here. The `C₀`-side identification (most-singular structures are 1-D) is now discharged by `/solve`; the `β`-side one is not.

**Cross-check that did *not* go the other way (`Alpha_Residual.md` §9c).** The reverse hope — that turbulent *intermittency* would supply the α-residual weight `δw` — was pre-registered and run to the end: the per-octave Kraft-flux multiplier `W(R)` of the closure census was pushed to convergence by an exact transfer recursion, vacuum **and** seeded (every injection scale). It has **no inertial range** — `W(R)` decays and the steady state piles at the floor. The closure census is not a turbulent cascade; the `C₀` derivation is a one-way contribution *from* the `/solve` selection *to* this doc, not a two-way bridge. QLF's contribution is that its dimensional analysis (`velocity_holder_exponents`) and its 1-D quantized vortices supply **both** ingredients, so within the log-Poisson class the intermittency spectrum is parameter-free — not that the log-Poisson model itself is derived from scratch.

**Honest scope — this closes the 🔵 *statistics* item, not the 🧱 regularity boundary.** What is done:
`−5/3` reduced to the flux-invariance lemma + K41; `ζ_3 = 1` exact; intermittency shown to be the
multifractal (fractal-closure) deviation, with She–Leveque's `C₀ = 2` grounded in QLF's quantized vortex
filaments and matching data parameter-free. And the **class is now selected**, not just fitted: Poisson
closures → log-Poisson → She–Leveque, decided on realizability (the log-normal is unphysical at high `p`,
above). With the class fixed and **both parameters anchored** — `β = 1 − h = 2/3` from the machine-checked
dimension-independent velocity exponent `h = 1/3` (the *same* `1/3` as `−5/3`, **not** `1/d`), and
`C₀ = d − 1 = 2` from the vortex-filament codimension (the sole `d`-input) — the intermittency spectrum is
parameter-free from the substrate (`μ = 2 − ζ_6 = 0.222`, matching data). The flux-invariance lemma, the
forced `−5/3`, and the `β`/`C₀` anchors are all Lean-anchored ([`QLF_Kolmogorov`](lean/QLF_Kolmogorov.lean):
`velocity_holder_exponents`, `she_leveque_beta`, `she_leveque_codimension`). What stays open
(`turbulence_statistics_in_progress`): the one residual **posit** — She–Leveque's identification of `β` with
the turnover exponent (most-singular flux = inverse turnover) and of the most-singular structures as 1-D
filaments — is standard phenomenology QLF *supplies the geometry for*, not the log-Poisson model derived from
scratch; and, separately, the Clay regularity boundary of §5, which self-similar frequencies say nothing about. The reading is
**falsifiable**: it lives or dies by whether the most-singular structures are 1-D (`C₀ = d − 1 = 2`, the
`d`-dependent input) and by She–Leveque's turnover identification `β = 1 − h` with the dimension-independent
`h = 1/3` (the same `1/3` as `−5/3`, not `1/d`) — and both can fail cleanly.

## 6b. Emergent closures from a Brownian phase = turbulence, capped — the continuum one closure at a time

> The synthesis of all the turbulence pieces (this geometry + the cascade + the `−5/3` spectrum + the exact
> Brownian closures + the program output) lives in [`Turbulence.md`](Turbulence.md).

This is QLF, so we do **not** sample a Brownian phase and count what happened — we compute *exactly what is most
likely*. [`brownian_closures.py`](brownian_closures.py) does this from the census alone (the census **is** the
return probability, [`QLF_CensusBrownian`](lean/QLF_CensusBrownian.lean)), tying the Brownian phase to turbulence
and contrasting both with the continuum. The organizing thesis (per Jim): **each ZFA closure is a quantum
logical system, and each renders its own continuum — valid up to the next phase change**. The continuum is not
one global object; it is generated closure-by-closure, phase-by-phase, from the exact discrete substrate. That
is *mathematics from QLF* ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md)): the exact census below, its
smooth power-law rendering above, and the phase transitions where the rendering switches. All quantities exact:

- **The exact return law and its continuum rendering.** `u_{2m}(p)` = the exact probability the `p`-pair phase
  is back at the origin after `2m` steps (= the census ratio). Its exact exponent fit is `−0.497 / −0.994 /
  −1.491` for `p = 1,2,3` — the **continuum bridge** `n^{−p/2}` (Wallis/Stirling), the Gaussian propagator of
  the phase, rendered from the exact count.
- **A dimensional phase change (Pólya) — which phases close at all.** With `G(p) = Σ u_{2m}` the expected
  returns, the phase closes with probability `1 − 1/G(p)`: **recurrent** for `p ≤ 2` (`G = ∞`, closes w.p. 1),
  **transient** for `p ≥ 3` — `P = 0.3406 / 0.1932 / 0.1352` for `p = 3,4,5`, matching the **classical Pólya
  constants to four digits**. The transition `p = 2 → 3` is a genuine phase change: below it every phase closes,
  above it most do not — the substrate's selection of **few-axis** closures.
- **First returns are the irreducible closures (each a quantum logical system).** The exact 1-D first-return
  exponent (from `F = 1 − 1/U`) is `−1.516` — the excursion law `~(2m)^{−3/2}`. The exact irreducible census:
  **8** length-2 closures = the **half-spin atoms** (`^v`, `<>`, `/\`, `+−`, …, all `→ −I`); **104** length-4
  two-axis (lepton loops); **2944** length-6 three-axis **Borromean** (proton-class). Every count-balanced
  closure Pauli-closes ([`count_balanced_pauli_closed`](lean/QLF_TwistAlphabet.lean)), so ZFA closure of the
  phase *is* the return to origin, and the **most likely** emergent closure is the shortest first return — the
  half-spin.
- **The octave cascade = turbulence.** The exact closure count per length-octave grows octave-by-octave with
  constant `log 2` per closure — the K41 scale-invariance `QLF_Kolmogorov` turns into the forced `−5/3`; an
  emergent closure ↔ a quantized vortex (§6). The `−5/3` rendering holds *within* an octave regime, up to the
  next phase change. GMC / log-correlated fields unify this cascade with the Riemann critical line.
- **The continuum, one closure at a time (the contrast).** So QLF's continuum is a **patchwork** of
  exact-closure renderings — `n^{−p/2}` (per dimension), `−3/2` (the excursion law), `−5/3` (per octave) — each
  valid up to the next phase change. The *continuum's own* story is the opposite: a single, infinitely-fine,
  non-differentiable object that needs an **external** cutoff for GMC to exist at all and to avoid the
  Navier–Stokes blow-up (§2–§5). In QLF the cutoff is **intrinsic** — the discrete closure under every
  rendering, capped at the Planck floor (= dissipation cutoff = GMC UV cutoff). **The substrate *is* the
  regularization; the continuum is what it renders, phase by phase** — the message of
  [`TheContinuum.md`](TheContinuum.md), made concrete in the Brownian-turbulence cascade.

**Honest scope:** exact combinatorics, not sampling. It *computes* the Brownian structure proven in
`QLF_CensusBrownian` (return law, Pólya constants, excursion law, irreducible census), reads it as the cascade
already anchored in `QLF_Kolmogorov`/§6, and frames the per-closure continuum bridge as *mathematics from QLF*.
It makes **no new prediction** — the census, the settled `−p/2`/`−3/2`/`−5/3` laws, the classical Pólya
constants, and the proven no-blow-up are the references; the GMC↔ζ / GMC↔turbulence ties stay bridge candidates.
Run: `python3 brownian_closures.py`.

## 7. Honest scope

- **Proven on the substrate:** angular momentum = circulation, its pseudovector law, vorticity =
  quantized discrete curl, `|ω| ≤ 1`, `|L| ≤ n`, and the unrealizability of continuum vorticity in a
  finite cell — all machine-verified, no new axioms.
- **The boundary, now removed — the work moved, not the wording.** The opaque `navier_stokes_continuum_limit`
  ([`QLF_NavierStokes`](lean/QLF_NavierStokes.lean)) is replaced (§5) by the *proven* Planck vorticity cap
  + the *cited* BKM theorem + a *sharp* faithfulness bridge `continuum_vorticity_planck_capped`, from
  which `navier_stokes_no_blowup` is a theorem. The residual gap is just the vorticity-rendering
  faithfulness — small, precise, and exactly QLF's continuum-as-rendering thesis. This is a **reduction**,
  **not a Clay proof**: BKM and the faithfulness bridge remain inputs, and the Clay statement is in the
  unfloored `v → ∞` limit (the rendering step), not at the Planck-floored substrate where the result is
  proven.
- **Beale–Kato–Majda** is *cited* as a real 1984 theorem (the standard continuum criterion that names
  what the substrate rules out), not re-derived — QLF has no PDE machinery in Lean.

See also: [`NavierStokes_QLF.md`](NavierStokes_QLF.md) (the existence/smoothness reformulation),
[`Geometry_Of_Space.md`](Geometry_Of_Space.md) (the geometry these dynamics live on),
[`Conservation.md`](Conservation.md) (Noether currents), [`Curvature.md`](Curvature.md) (blanket
deformation), [`TheContinuum.md`](TheContinuum.md) (why discreteness removes the infinities).

## 2026 update

2026 vortex results: cold-atom quantum Shapiro steps, where each step corresponds to a number of
vortex–antivortex pairs nucleated per drive cycle (`pairs_balanced`, [Discoveries_2026 §6](Discoveries_2026.md#p6)),
and the Technion's films of optical phase singularities annihilating in pairs at speeds above light.
Their approach speed `κ/(2√s)` is unbounded (`vortex_speed_unbounded`) but carries no signal
([V4](Discoveries_2026.md#v4)).
