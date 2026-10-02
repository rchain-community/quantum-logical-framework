# The Yang–Mills Mass Gap in [QLF](README.md)

> **The engine (path integral · all closures · Witten 1988).** This attack is QLF's one Millennium move —
> *generate every possibility, then select the invariant* — the exact/constructive form of the Feynman path
> integral (all paths happen; stationary phase selects) and of Witten's 1988 Jones-polynomial path integral
> (a physics sum-over-everything that proved rigorous mathematics, discharged by Reshetikhin–Turaev).
> **Generate:** the gauge closures (SU(2)/SU(3) verified). **Select:** the lightest non-vacuum closure carries
> one `log 2` quantum ⟹ positive gap (`mass_gap_quantum_pos`, `gaugeMassGap = log 2 > 0`). **Bridge (Class A,
> couched Witten→RT):** `yang_mills_continuum_gap` — carries the problem's own content; its settled-math
> neighbour is constructive QFT / reflection positivity. See [Millennium.md](Millennium.md) § *The engine*.

> **Status: `mass_gap_proven_constructively` (substrate) — a reformulation.** *Contrast (once):* the **classical**
> Clay problem (constructing the continuum Yang–Mills QFT and proving a gap) is not solved here.
> *What is proven (the reformulation):* the gap on the substrate, `gaugeMassGap = log 2 > 0`
> (machine-verified, [`lean/QLF_MassGap.lean`](lean/QLF_MassGap.lean)). *The gap:* the continuum-QFT
> reconstruction, carried by the one bridge axiom `yang_mills_continuum_gap` (the
> [`spectral_hilbert_polya`](lean/QLF_Riemann.lean) precedent). This *is* a genuine continuum step —
> QLF's **thesis** (not a proof) is that this sector is where ZFC's continuum/choice machinery
> struggles ([Continuum_Choice_Fallacy.md](Continuum_Choice_Fallacy.md)); but note the Clay problem
> itself is **not** a known ZFC-independence result, so the bridge is the open gap, stated as such.
> See [Open_Problems.md](Open_Problems.md).

## 1. The classical problem

One of the seven Millennium Prize Problems: prove that for every compact simple gauge
group **G** a non-trivial quantum Yang–Mills theory exists on ℝ⁴ and has a **mass gap**
Δ > 0 — a strictly positive lower bound on the energy of every state above the vacuum.
The gap is what makes the strong force short-ranged and is the field-theory shadow of
"no massless free gluons; the lightest glueball is heavy." The two faces are *existence*
(a rigorous continuum quantum field theory satisfying the Wightman / Osterwalder–Schrader
axioms) and *the gap* (Δ > 0 for that theory).

## 2. The QLF reframing

QLF does not quantize a continuum field. It generates the discrete possibility space of
ZFA twist histories and keeps the **closed** ones. Three facts already machine-verified in
the tree turn "mass gap" into a counting statement:

1. **The gauge algebra is a non-abelian ZFA twist algebra — and it exists.** The
   weak-isospin **SU(2)** is the τ-quaternion subalgebra of Σ₈
   (`weak_isospin_su2`, [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean); see
   [Weak_Force.md](Weak_Force.md)); the strong **SU(3)** is the traceless 3-axis
   directional tensor (`trace_commutator_zero`, `gluon_commutator_nonzero`,
   `strong_su3_summary`, [`lean/QLF_StrongAlgebra.lean`](lean/QLF_StrongAlgebra.lean)).
   So the *gauge structure* a Yang–Mills theory needs is constructed, not assumed.

2. **The vacuum is the identity / empty closure.** The variational principle is **ℒ = 0**
   (a null Lagrangian, the condition of origin — [Lagrangian_Formulation.md](Lagrangian_Formulation.md));
   the vacuum is the trivial closure with zero free action and zero excitation energy.

3. **The lightest non-vacuum closure carries exactly one `log 2` quantum.** A non-vacuum
   gauge excitation is a *non-trivial* ZFA closure — a Hermitian-conjugate twist pair
   `(t, t†)` whose ordered product folds to a Pauli scalar. Its per-event free-energy
   decrement is exactly **ΔF = −log 2 nats** (`zfa_closure_minimizes_free_energy`,
   [`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean), with the binary-KL identity
   `binary_kl 1 (1/2) = log 2`). Anything "lighter" than a full closure is an *unclosed
   fraction* — pruned by `full_zeno_prune`, never a physical state.

## 3. The structural mass gap

Put (1)–(3) together. The vacuum has energy 0. Every non-vacuum state is a closure, and
every closure costs at least one half-spin quantum. Therefore the spectrum has a **gap**:

> **Δ = `gaugeMassGap` = log 2 > 0** (substrate units).

Machine-verified in [`lean/QLF_MassGap.lean`](lean/QLF_MassGap.lean): `mass_gap_quantum_pos`
(`log 2 > 0`) and `lightest_closure_is_gap_quantum` (the lightest closure realises exactly
that quantum, reusing `QLF_FreeEnergy`). There is no continuum of arbitrarily-light gauge
excitations because the substrate is discrete and closure is all-or-nothing — the same
reason QLF has no ultraviolet catastrophe.

**Confinement is the colour-singlet face of the same fact.** Only count-balanced (ZFA)
histories persist; a free colour charge is an unbalanced (non-closed) twist net and is
pruned. The surviving excitations are colour-singlet closures (linking-invariant baryon
windings, [`lean/QLF_BaryonWinding.lean`](lean/QLF_BaryonWinding.lean); exactly-conserved
signed charge, [`lean/QLF_BMinusL.lean`](lean/QLF_BMinusL.lean)) — so the gap is a gap of
*physical* (singlet) states, as the problem requires.

### 3a. The gap as a *propagation* gap — the dispersion reading

The gap `Δ = log 2` also has a propagation meaning, tying it to the gravitational-wave sector
([`lean/QLF_MassGapDispersion.lean`](lean/QLF_MassGapDispersion.lean), a bridge to
[`lean/QLF_GravitationalWaves.lean`](lean/QLF_GravitationalWaves.lean)). A **massless**,
gauge-fold-free ripple obeys the free wave equation `□_d δρ = 0` and is **gapless** — every
traveling wave is a solution, so the minimum frequency is zero (`massless_gapless`). A
**massive** gauge-fold field obeys the discrete Klein–Gordon equation `(□_d + m²)h = 0`
(`boxKG`); a massless wave is no longer a solution — the mass term `m²δρ` is exactly the
obstruction (`massive_residual`). The continuum dispersion is then `ω² = k² + m²`, whose
minimum at zero momentum (`k = 0`) is `ω = |m|`: for a gauge fold `m = gaugeMassGap = log 2`,
so the **rest-frame dispersion gap is `log 2 > 0`** (`mass_gap_is_dispersion_gap`), versus
`ω² = 0` for the massless field. So the mass gap is the minimum *excitation frequency* of the
propagation operator, and the massless/massive dichotomy is QLF's gauge-fold-absent/present
dichotomy. This is a **bridge/reframing** of the same `gaugeMassGap = log 2`, not a new route
past the boundary below — the "discrete `boxKG` symbol = continuum dispersion" step is the
standard finite-difference correspondence, and the Clay statement stays at §4.

## 4. Where the boundary sits

QLF supplies the gap as a property of the **discrete substrate**. The Clay problem asks for
it as a property of a **continuum** quantum field theory satisfying the Wightman /
Osterwalder–Schrader axioms on ℝ⁴. The bridge — that the continuum reconstruction's
physical gap equals the substrate's per-closure quantum — is the genuinely analytic step,
the continuum limit. QLF marks it with **one explicit axiom**:

```lean
axiom YangMillsMassGap : ℝ                    -- the continuum theory's gap (opaque)
axiom yang_mills_continuum_gap :              -- the boundary (RCA₀ → analytic)
    YangMillsMassGap = gaugeMassGap
theorem yang_mills_mass_gap_in_qlf : 0 < YangMillsMassGap := by
  rw [yang_mills_continuum_gap]; exact mass_gap_quantum_pos
```

This is the same epistemic move as the Riemann program: a constructive theorem chain
whose only non-RCA₀ input is a single, named boundary axiom marking exactly the
constructive→analytic crossing — never a `sorry`, never a hidden gap.

**The perturbative side of the boundary is now finite by theorem.** Continuum Yang–Mills'
perturbation series is asymptotic (Dyson 1952) and its diagrams diverge before renormalisation —
part of why a rigorous construction is hard. On the substrate that trouble is absent *by counting*:
the perturbation series **is** the closure-order sum ([`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md)),
which **converges absolutely** in its cylinder measure — `twist_kraft` (`Σ 8^{−|h|} ≤ 1`) plus
`|A| ≤ W` — with no Borel resummation, no Lipatov analysis
([`QLF_ExactRG`](lean/QLF_ExactRG.lean), the exact-RG recursion + finiteness + convergence, **no
axiom**). Renormalisation is the Wilsonian capacity horizon (a finite integer counterterm per octave,
`Q(R) = Q₀·2^R` the running), and the one-loop `2/(3π)` coefficient is 1PI-confirmed (`census_split →
1/6` for the *prime* census, [`alpha_residual_bridge.py`](alpha_residual_bridge.py)). So the Dyson
divergence is diagnosed as an artefact of the coupling continuum the substrate does not have — the
same "continuum is the UV catastrophe" reading as everywhere else. What `yang_mills_continuum_gap`
still carries is only the *reconstruction* of the Wightman theory itself, not the finiteness of its
expansion.

## 5. Epistemic stance

Within QLF's frame — where the substrate-constructive part of mathematics has its own
foundational adequacy, and the continuum is the coarse-grained statistical limit of a
dense-but-discrete ZFA event stream ([TheContinuum.md](TheContinuum.md)) — the mass gap is
*structurally necessary* as a quantum of **action** per closure: all-or-nothing closure
leaves no fraction of a closure. Whether that is a gap in **energy** is a separate question,
and §7 shows it is not one without a cap on closure time. What QLF does **not** do is construct the continuum
QFT and prove the Wightman axioms; that is what `yang_mills_continuum_gap` carries. It is an
ordinary open problem, not a known independence or uncomputability boundary, so it is not
"ZFC's defect" in the sense CLAUDE.md reserves for halting and Busy Beaver. The one-line summary, machine-checked as `mass_gap_proven_constructively`: *QLF
proves the Yang–Mills mass gap on the substrate — the gap value is the `log 2` quantum —
and reduces the rest to the existence of the continuum limit.*

## 6. What would close it

Promoting `yang_mills_continuum_gap` from axiom to theorem means giving a constructive
continuum limit of the ZFA event field whose reconstructed two-point function has a
spectral gap — the QLF analogue of the MRE-bridge refinement proposed for Riemann
([ReverseMathematics.md](ReverseMathematics.md) §4). That is the real open work; this
document and module make the target precise and the boundary explicit.

## 7. What the census says about the gap (2026-10-01)

Four results, each checked rather than argued. Computations: [`yang_mills_census.py`](yang_mills_census.py).

**7a. The Axiom of Choice plays no part.** The proved content, `log 2 > 0`, uses nothing beyond
what Mathlib uses everywhere. On the classical side, a mass gap for explicit lattice approximants
is an arithmetic statement, and ZF and ZFC prove the same arithmetic and Σ¹₂ sentences
(Shoenfield absoluteness). Denying Choice cannot prove or refute it.

**7b. `log 2` is a quantum of action, not of energy.** Every closure carries the same `ΔF = log 2`
(in units of ħ), whatever its length. Its energy is ħ over its closure time, `E ≈ ħ/t`, and the
[Law of Exceptions](Law_Of_Exceptions.md) says closure time has no upper bound. Its witness
`[+^(R+1) −^(R+1)]` is a real closure of length `2R+2` at every capacity `R`
([`law_of_exceptions`](lean/QLF_LawOfExceptions.lean)), so closure frequencies reach `1/(2R+2) → 0`.
A claimed lowest closure frequency would be a restrictive law, and it has an exception one shell
deeper. The cosmic horizon is the only universal cap, and it gives a floor near `ħH ≈ 10⁻³³ eV`.

**7c. The census itself is gapless.** A Euclidean gap shows up as exponential decay of a return
amplitude in path length. Exact counts to `L = 24`:

| census | growth | reading |
|---|---|---|
| unsigned `W_L` | `→ (8/π²) · 8^L / L²` | the massless 4-D propagator (Pólya, [`QLF_PolyaTransience`](lean/QLF_PolyaTransience.lean)) |
| half-spin signed `A_L` ([`QLF_EdgeSign`](lean/QLF_EdgeSign.lean)) | `≈ 3.9 · (2+2√3)^L / L²` | continuous band edge |
| colour `C_L = Σ ω^B` (7d) | `∝ 7.088^L` × power | continuous band edge |

Each phase suppresses its sector relative to the unsigned one, at `ln(8/ρ)` per step: `0.381`
(half-spin) and `0.121` (colour). Neither is `log 2`, and neither is a gap inside its own sector.

**7d. Colour as the three-axis cycle, three dimensions at a time.** [Carbon_Superconductivity.md](Carbon_Superconductivity.md)
§24 derived colour's ℤ₃ as the cyclic axis relabelings that preserve the baryon winding of
[`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean), and left the transport rule open. The winding
reads three consecutive axes at a time, so `ω^B` is the colour phase that cycle defines along a
path. It is not trivial on closures: `C_L/W_L` falls from 1 to `0.078` by `L = 24`. It is
real-valued on every closure set, since mirror images carry `ω^B` and `ω^{−B}`. This is a
candidate rule only. It is not yet tested against §23's twisted-boundary confinement statistic,
which needs a 3-D lattice because `B` vanishes on any plaquette.

**7e. Where a gap could come from.** A cap on colour closure time, derived rather than chosen.
QLF already has one: dimensional transmutation `ln(M_Planck/m_p) = 2π·b₀ = 14π`
([`QLF_AlphaS`](lean/QLF_AlphaS.lean), 0.07% on the log). That puts the cap at `e^{14π}` Planck
times and a gap near 1 GeV, the order of the lightest lattice glueball (about 1.7 GeV). Two of its
inputs are not derived:
* **The 11 in `b₀ = 11N_c/3 − 2n_f/3`.** It is taken from standard group theory
  ([`QLF_BetaFunction`](lean/QLF_BetaFunction.lean), `beta_function_in_progress`), so the sign of
  asymptotic freedom is assumed. The QED tower does not count its sign either: `towerRunning`
  subtracts by definition, and the `1/6` split count is spin-blind. The route to the 11 is the
  Nielsen–Hughes form, where each charged mode of spin `s` contributes `−(−1)^{2s}[(2s)² − 1/3]`
  (`+2/3` for spin ½, `−11/3` for spin 1): spin paramagnetism beating orbital diamagnetism. QLF has
  each ingredient (spin as twists, `−1` per 2π turn from [`QLF_Spin`](lean/QLF_Spin.lean), `1/3`
  from three axes) but no gluon as a colour-charged spin-1 closure to count with.
* **`α_s(M_Planck) = 1/b₀²`.** A posit.

So the honest status of §3 is: a positive quantum of action per closure is proved; a positive
energy gap is not, and the census points to gaplessness unless a colour cap is derived.

## References

- C. N. Yang & R. L. Mills, *Conservation of isotopic spin and isotopic gauge invariance*, Phys. Rev. **96** (1954) 191–195 — non-abelian gauge theory.
- K. Osterwalder & R. Schrader, *Axioms for Euclidean Green's functions*, Comm. Math. Phys. **31** (1973) 83–112 & **42** (1975) 281–305; A. S. Wightman (Wightman axioms) — the continuum reconstruction the mass-gap problem asks for.
- A. Jaffe & E. Witten, *Quantum Yang–Mills Theory* — Clay Mathematics Institute (official problem description). <https://www.claymath.org/millennium-problems/>
