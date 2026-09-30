### `Carbon_Superconductivity.md`

# Carbon Superconductivity: the ZFA DNA of Graphene

*Where the superconductivity thread starts: the carbon lattices written in the twist alphabet, the substitution rule
that grows graphene, and the magic-angle family of superconducting graphene stacks. A log 2 test was pre-registered
in §5 before it was run, and §5a has the result.*

Graphene only superconducts when two sheets are twisted by about 1.1°. Stack three sheets and the angle moves up by
√2; stack four and it moves up by φ. Why should the ratios the ZFA DNA produces (ZFA_DNA.md §11–13) turn up
in a stack of carbon sheets? And does the log 2 that runs through QLF appear in how these materials
conduct? This document takes the first question as far as it goes and sets up the second as a test.

Script: [`carbon_zfa_dna.py`](carbon_zfa_dna.py) (under a second; every claim in §1–§3 is asserted by it).

---

## 1. Carbon's lattices come from the twist alphabet

The eight twists are the signed unit vectors of four axes ([`Closure_Walk.md`](Closure_Walk.md)). Require the
signs to **alternate**, `+ − + − …`. The running sign sum, which is the coordinate along `(1,…,1)`, is then always 0
or 1. So the walk never leaves a two-layer slab of `ℤ^k`. Height-0 points form sublattice A and height-1 points
form sublattice B. Projecting along `(1,…,1)` is one-to-one on the slab, and the projected bond vectors meet at
`cos θ = −1/(k−1)`:

| axes `k` | lattice | bonds | bond angle | smallest ring |
|---|---|---|---|---|
| 2 | carbyne (sp) | 2 | 180° | none |
| 3 | **graphene (sp²)** | 3 | 120° | 6 |
| 4 | diamond (sp³) | 4 | 109.47° | 6 |

Carbon's three hybridisations are the three slabs. Graphene is the one that uses exactly the three Pauli spatial
axes `x, y, z`. Diamond needs a fourth direction, and the fourth axis of the alphabet is the gauge axis `+−`. As in
the silver thread ([`ZFA_DNA.md`](ZFA_DNA.md) §12), a physical reading of diamond would have to justify treating
that axis as spatial. Graphene needs no such step.

**A closed walk on graphene is a ZFA word.** A walk on the lattice returns when its axis counts balance, and count
balance implies Pauli closure (`count_balanced_pauli_closed`, [`QLF_TwistAlphabet`](lean/QLF_TwistAlphabet.lean)).
The script checks every alternating word to length 8. The closed ones number `3, 15, 93, 639` on graphene and
`4, 28, 256, 2716` on diamond, which are the honeycomb and diamond return counts (OEIS A002898, A002899). Every one
is ZFA, and no other alternating word is.

The hexagon is `>v/<^\` (`+x −y +z −x +y −z`): six distinct atoms, ZFA, Pauli fold `+I`. Its two sublattices
are the two twist signs. Graphene's Dirac electrons carry a sublattice pseudospin, and in this picture that label is
the sign alternation itself.

## 2. The carbon DNA: `t ↦ t u′ t w′ t`

Replace each twist by itself interleaved with the opposite twists of the other two axes:

```
>  ↦  > v > \ >    or    > \ > v >
<  ↦  < ^ < / <    or    < / < ^ <        (and so on for ^ v / \)
```

The image of `+e_x` is `3e_x − e_y − e_z = 4e_x − (1,1,1)`, which is `+e_x` scaled by 4 on the sheet. An image
starts and ends with its parent's sign, so the alternation survives and every generation stays on the sheet. The
counts transform linearly, so a closure maps to a closure. Checked through generation 3 from the hexagon:

* **ZFA at every depth**, and the walk never leaves the sheet.
* **Exact self-similarity.** Keep every 5th twist and the parent returns. Block boundaries land exactly on 4× the
  parent's corners, so the hexagon becomes the side-4 hexagon.
* **One free bit per twist.** The order of the interleaved twists is free. It changes no count and no closure,
  only the history. Generation 1 has all `2^6 = 64` images of the hexagon distinct. So

$$h_{\text{graphene}} = \tfrac14 \text{ bit per twist}, \qquad h_{\text{primordial}} = \tfrac13 \ \ (\text{ZFA\_DNA.md §1}).$$

The same rule works on `k` axes, with block length `2k−1`, inflation `k+1` and `(k−1)!` orders per twist:

| `k` | lattice | block | inflation | orders | `h` (bits/twist) |
|---|---|---|---|---|---|
| 2 | carbyne | 3 | 3 | 1 | 0 |
| 3 | graphene | 5 | 4 | 2 | 1/4 |
| 4 | diamond | 7 | 5 | 6 | `log₂6 / 6` = 0.431 |

Carbyne's DNA is forced, because a chain has only one way to grow. Graphene's is the first with a free bit. Like the
primordial DNA's chirality bit, it is carried entirely in the *order* of the twists, which is the one place ZFA does
not charge for. This is one DNA for graphene; the sheet has others, such as the norm-7 rule `x ↦ x ȳ x` that inflates
by `√7` with a 19.1° rotation. Constructing a DNA shows that the sheet can grow this way, not that it must.

## 3. The magic-angle family of superconducting graphene

Stack `n` sheets with alternating twists `+θ, −θ, +θ, …`. This is the sign alternation again, now between
layers. In the chiral limit the stack decouples exactly into bilayers whose couplings are scaled by the eigenvalues
of the `n`-site chain, `2cos(jπ/(n+1))`. So its magic angles are the bilayer's multiplied by those numbers (Khalaf,
Kruchkov, Tarnopolsky & Vishwanath 2019). Park et al. (2022) built the family and found superconductivity in every
member:

| `n` | `2cos(π/(n+1))` | where it lives | predicted | device | `T_c,50%` |
|---|---|---|---|---|---|
| 2 | 1 | | 1.08° | 1.08° | |
| 3 | √2 | `ℤ[ζ₈]`, the substrate lattice | 1.53° | 1.57° | |
| 4 | φ (and 1/φ) | `ℤ[ζ₅]` | 1.75° | 1.77° | 2.76 K |
| 5 | √3 (and 1) | `ℤ[ζ₁₂]` | 1.87° | 1.95° | 1.38 K |

The first four superconducting members sit at `1, √2, φ, √3`. These are the natural ratios of
[`ZFA_DNA.md`](ZFA_DNA.md) §11–13, including √2, the silver lattice's own value.

**What this is.** The ratios are Khalaf et al.'s continuum-model result, not a QLF derivation. The chain eigenvalue
is the spectrum of any `n`-link chain. The devices were built to hit the calculated magic angles, whose real values
sit slightly above the chiral-limit ones (device/prediction = 1.03, 1.01, 1.04). So the agreement is not an
independent test of the ratios. What QLF adds is the placement: the stacking is the same sign alternation as the
sublattice, and the values it produces are the family the ZFA DNA already makes.

## 4. Carbon's superconductors

| material | carbon lattice | `T_c` | source |
|---|---|---|---|
| magic-angle twisted multilayers (`n` = 2–5) | graphene sheets, `k = 3` | ~1–3 K | Park et al. 2022 |
| CaC₆ (intercalated graphite) | graphene sheets, `k = 3` | 11.5 K | Weller et al. 2005 |
| boron-doped diamond | `k = 4` | ~4 K | Ekimov et al. 2004 |
| K₃C₆₀ | fullerene cage: hexagons **and 12 pentagons** | 18 K | Hebard et al. 1991 |
| Cs₃C₆₀ (under pressure) | fullerene cage | 38 K | Ganin et al. 2008 |

**A lead, not a result.** The highest-`T_c` carbon superconductors are the fullerides, and theirs is the only
lattice here that is not a slab. A pentagon is a ring of odd length. An odd ring cannot alternate in sign and cannot
balance its counts, so it is not a closure of §1. It is a defect in the alternation: a disclination, and Euler's
formula forces exactly twelve of them onto a closed cage. Whether breaking the sublattice alternation matters for
pairing would need a count across many materials. Five classes is far too few, so this is recorded as a lead and
nothing more.

## 5. Pre-registered: is the strange-metal scattering rate `log 2`?

*Fixed in the commit that adds this document, before any value below was gathered or computed.*

Above `T_c`, magic-angle graphene and the cuprates share a "strange metal" regime. There the resistivity is linear in
`T` and the scattering rate sits at the Planckian bound,

$$\hbar/\tau = C\,k_B T, \qquad C \approx 1 .$$

**The hypothesis (H_log2).** Each scattering event is one binary closure, and a closure receipts `ΔF = −k_B T log 2`
(`QLF_FreeEnergy`, Landauer). If the event's energy width is that receipt, then `ħ/τ = k_B T log 2`, so
**`C = log 2 = 0.6931`**. The rival is the conventional Planckian `C = 1` (H_1).

**Data, fixed now.** Every value of `C` that is reported *with an uncertainty* in these three papers, taken as
reported. Where a paper gives a range without an uncertainty, half the range is the uncertainty.
1. Legros et al., *Nature Physics* 15, 142 (2019): overdoped cuprates.
2. Cao et al., *PRL* 124, 076801 (2020): magic-angle twisted bilayer graphene.
3. Grissonnanche et al., *Nature* 595, 667 (2021): Nd-LSCO, angle-dependent magnetoresistance.

**Statistic.** The inverse-variance weighted mean `C̄ ± σ̄`, with `χ²` about the mean reported to show the spread.

**Verdict rules.**
* **PASS**: `|C̄ − log 2| ≤ 2σ̄` and `|C̄ − 1| > 2σ̄`.
* **FAIL**: `|C̄ − log 2| > 2σ̄`.
* **UNDECIDED**: anything else, meaning the data cannot tell the two apart.

**Stated prior.** From memory, published values cluster near 1, so I expect FAIL or UNDECIDED. The prior is written
down so that the test cannot be tuned to it. A FAIL would be recorded as such: the Planckian rate is then not the
closure receipt, and the log 2 question for superconductivity moves to the turbulence bridge (§6).

### 5a. Result

Run by [`planckian_log2_test.py`](planckian_log2_test.py). The pre-registration above was frozen in commit `ad8e36f`.

| source | sample | `C` |
|---|---|---|
| Legros 2019 | PCCO + LCCO (electron-doped; one value in the text) | 1.0 ± 0.3 |
| Legros 2019 | Bi2212 · LSCO · Nd-LSCO · Bi2201 | 1.1 ± 0.3 · 0.9 ± 0.3 · 0.7 ± 0.4 · 1.0 ± 0.4 |
| Legros 2019 | (TMTSF)₂PF₆, organic | 1.0 ± 0.3 |
| Cao 2020 | MATBG, `ν = −2 − δ` ("0.2–0.4") | 0.3 ± 0.1 |
| Cao 2020 | MATBG, `ν = −2 + δ` ("1.0–1.6") | 1.3 ± 0.3 |
| Grissonnanche 2021 | Nd-LSCO, angle-dependent magnetoresistance | 1.2 ± 0.4 |

**By the frozen rule the verdict is PASS:** `C̄ = 0.614 ± 0.076`, which is 1.0σ from `log 2` and 5.1σ from 1.

**It is not evidence for `C = log 2`.** The spread statistic registered with the mean says the nine values do not
share one `C`: `χ² = 25.1/8`, `p = 0.0015`. They fall into groups:
* The cuprates and the organic metal sit at `0.99 ± 0.13` (`χ² = 1.0/6`). This group puts `log 2` 2.4σ away.
* Magic-angle graphene sits on two filling branches, 0.2–0.4 and 1.0–1.6.

The mean lands between the groups because the one tightly bounded value, `0.3 ± 0.1`, carries 57 % of the weight.
Three single measurements lie within 1σ of `log 2`, and each of those error bars also covers 1. The hypothesis was
a per-event value that every material shares. No group sits at `log 2`.

So the PASS stands as the rule's output, and the hypothesis is not supported. A weighted mean assumes one
population, and these data contain at least two. What the data do show is that magic-angle graphene's `C` depends
on which side of half filling the sheet is doped. A single universal `C`, `log 2` or 1, cannot produce that.
The filling dependence is the lead worth following next, rather than the Planckian constant.

## 6. Scope, and what comes next

**Established here, by construction and brute force:**
* An alternating-sign walk on `k` axes lives on a slab whose projection is carbyne, graphene or diamond.
* Graphene's closed walks are exactly the alternating ZFA words over the three spatial axes.
* `t ↦ t u′ t w′ t` is a ZFA DNA of graphene, with inflation 4 and `h = 1/4`.
* The magic-angle multilayers realise the chain ratios `1, √2, φ, √3`.

**Not claimed:** any pairing mechanism, or any `T_c`. The slab picture gives carbon's *geometry*, not why its
electrons pair. The existing QLF account of pairing is [`Electricity.md`](Electricity.md) §6 (bath decoupling) and
[`Chemistry.md`](Chemistry.md) §8 (`cooper_pair_boson`).

**Next:**
1. The filling dependence of magic-angle graphene's `C` (§5a): two branches either side of `ν = −2`.
2. **The turbulence bridge.** [`Turbulence.md`](Turbulence.md) gets Kolmogorov's `−5/3` from a constant `log 2` flux
   per octave. The same identity, octave per e-fold = `log 2`, is where the [`Log2_Search.md`](Log2_Search.md) routes
   converged. Superfluids and superconductors carry quantised vortices, and quantum turbulence in a condensate has a
   Kolmogorov range. A pre-registered test of whether that range carries the substrate's `log 2` per octave is the
   natural second route.
3. The fulleride lead of §4, if a count can be framed that could fail.
4. Phase coherence, the second step after pairing (§7, §7a): the trilayer breaks the BKT ceiling and sits near the
   one-bit value. It needs a stiffness measurement that does not assume BKT, and an Ising-exponent check.

## 7. Pre-registered: phase coherence to one bit

*Fixed in the commit that adds this section, before any stiffness or `T_c` value below was gathered.*

Pairing makes bosons, and `cooper_pair_boson` proves it. Superconductivity needs a second step: every pair locks
to one shared phase, so that the condensate is one joint closure. The temperature at which that lock fails is set by
the **phase stiffness** `D_s`, the cost of twisting the phase between neighbouring patches of condensate. This
section counts the ways that step can fail.

**What the substrate allows.** A closed history folds to `±I` and never to `±iI` (`QLF_BalancedPhaseReal`), and a pair
folds to `+I`. So a closure carries at most one bit of phase. **Hypothesis H_1bit (Jim, 2026-09-30): the stiffness
holds the phase to one-bit precision.** Each coherence patch carries a phase in `{0, π}`, and the ways of the
condensate are the configurations of those bits. That count is the Ising model on the lattice of patches. The rival
**H_BKT** is the standard picture: a continuous phase, and a count of vortices (fluxoids, each one ZFA loop,
[`Collective_Electrodynamics.md`](Collective_Electrodynamics.md)). Free vortices appear when their placements
outnumber their cost, which gives the Kosterlitz–Thouless condition `k_B T_c = (π/2) D_s(T_c)`.

**The derived prediction.** Take neighbouring patches with coupling `−J cos(Δθ)`. The zero-temperature stiffness is
`D_s(0) = J`, `√3 J` and `J/√3` on the square, triangular and honeycomb lattices. Restricting the phase to one bit
gives the Ising critical points `T_c/J = 2/ln(1+√2)`, `4/ln 3` and `2/ln(2+√3)`. So

$$r \equiv \frac{k_B T_c}{D_s(0)} = 2.27,\ 2.10,\ 2.63 \quad (\text{H\_1bit, coherence-limited}), \qquad r \le \frac{\pi}{2} = 1.571 \quad (\text{H\_BKT, always}).$$

The BKT ceiling holds because `D_s` falls with temperature and `D_s(T_c) = (2/π) k_B T_c`. `D_s` is in the
convention where that BKT relation reads as written; a paper in another convention is converted to it. The two
hypotheses are separated by a factor of about 1.5 in `r`, and by universality class. H_1bit is Ising, so it has no
universal jump in the stiffness. H_BKT has a jump, from `(2/π) k_B T_c` to zero.

**Data, fixed now.** Every sample in these three papers that reports `D_s(0)` and `T_c`, or the stiffness near `T_c`:
1. Hebard & Fiory, *PRL* 44, 291 (1980): thin aluminium films, a conventional superconductor.
2. Tanaka et al., *Nature* 638, 99 (2025): magic-angle twisted bilayer graphene.
3. Banerjee et al., *Nature* 638, 93 (2025): magic-angle twisted trilayer graphene.

**Tests and verdict rules.**
* **U (universality).** Does any sample show a stiffness jump consistent with `(2/π) k_B T_c`, as the authors report
  it? If yes, H_1bit fails for that material. No jump is **not** support for H_1bit, because twist-angle
  inhomogeneity smears the jump in moiré samples.
* **R (ratio).** Compute `r` per sample with its uncertainty. If any sample has `r > π/2` by more than 2σ, that
  supports H_1bit and excludes H_BKT for that sample. If every sample has `r ≤ π/2`, H_1bit is not supported. That
  outcome cannot tell "the phase is continuous" from "`T_c` is set by pairing, below the coherence temperature",
  so R alone cannot make H_1bit fail.

**Stated prior.** A BKT jump is well established in thin superconducting films, so I expect U to go against H_1bit
for aluminium. I do not know the moiré values, and those are where the question is open.

### 7a. Result

Run by [`phase_coherence_test.py`](phase_coherence_test.py). The pre-registration above was frozen in commit `8c7b2ee`.
Figure values were read by pixel calibration of the published figures.

| sample | `T_c` definition | `r = k_B T_c / D_s(0)` | vs BKT ceiling 1.571 |
|---|---|---|---|
| MATBG (Tanaka), hole side | zero resistance · half resistance | 0.52 · 0.79 | below |
| MATBG (Tanaka), hole side | resistive onset | 1.86 | 18 % above, onset only |
| **TTG (Banerjee)**, all points | zero resistance | **2.2 – 4.2** | above, every point by ≥ 2.3σ |
| TTG, the authors' fitted line | zero resistance | **3.04 ± 0.10** | 14σ above |
| **H_1bit prediction** | coherence-limited | **2.10 – 2.63** | |

**Test R.**
* **Magic-angle trilayer.** The raw data break the BKT ceiling on every point. The points at the top of the dome
  (`r` = 2.2–2.9) overlap the one-bit band, and the fitted slope, 3.0, is 15–45 % above it. By the frozen rule this
  **supports H_1bit and excludes H_BKT for this sample.**
* **Magic-angle bilayer.** It does not discriminate. Its zero-resistance `T_c` sits well below the ceiling, which is
  allowed under either hypothesis if pairing, not coherence, sets `T_c`.

**The caveat the rule did not price.** Banerjee et al. explain the excess by inhomogeneity. If supercurrent flows
in filaments narrower than the device, the microwave measurement underestimates the sheet stiffness. They put the
factor at about 3, but they obtain it by assuming `T_BKT ≈ T_c`, which is the conclusion under test, so it cannot
serve as a correction here. It cannot be excluded either. The trilayer support is therefore conditional: it holds if
the measured `ρ_s0` is the sheet stiffness.

**Test U.** Hebard & Fiory report Kosterlitz–Thouless vortex unbinding in aluminium films, so **H_1bit fails
for aluminium**, as the stated prior expected. This was read from the abstract; the full text was not accessible.
In the moiré samples the stiffness falls through the BKT line without a jump: steeply to zero in the bilayer, and
at `T₀ ≈ T_c/3` in the trilayer, which stays superconducting above `T₀`. Under the frozen rule, no jump is no verdict.

**Where this leaves the one-bit hypothesis:**
* It is **not universal**. A conventional aluminium film behaves as a continuous phase.
* In the **magic-angle trilayer** the measured `T_c/ρ_s0` is about twice what a continuous phase allows, at or
  just above the value a one-bit phase gives.
* That makes the trilayer the lead. What would settle it is an independent measure of the sheet stiffness, one
  that does not assume BKT, for example local (scanning) stiffness or a device of uniform twist angle.
* A second check the one-bit reading makes without new data: its transition is Ising-class, so the specific heat
  and the critical current near `T_c` should carry Ising exponents, not BKT's essential singularity.

## References

- Khalaf, E., Kruchkov, A. J., Tarnopolsky, G. & Vishwanath, A. (2019). Magic angle hierarchy in twisted graphene
  multilayers. *Phys. Rev. B* 100, 085109. [arXiv:1901.10485](https://arxiv.org/abs/1901.10485)
- Park, J. M., Cao, Y., Xia, L., Sun, S., Watanabe, K., Taniguchi, T. & Jarillo-Herrero, P. (2022). Robust
  superconductivity in magic-angle multilayer graphene family. *Nature Materials* 21, 877–883.
  doi:10.1038/s41563-022-01287-1. [arXiv:2112.10760](https://arxiv.org/abs/2112.10760)
- Cao, Y. et al. (2020). Strange metal in magic-angle graphene with near Planckian dissipation. *Phys. Rev. Lett.*
  124, 076801. doi:10.1103/PhysRevLett.124.076801
- Legros, A. et al. (2019). Universal T-linear resistivity and Planckian dissipation in overdoped cuprates.
  *Nature Physics* 15, 142–147. doi:10.1038/s41567-018-0334-2
- Grissonnanche, G. et al. (2021). Linear-in temperature resistivity from an isotropic Planckian scattering rate.
  *Nature* 595, 667–672. doi:10.1038/s41586-021-03697-8
- Weller, T. E., Ellerby, M., Saxena, S. S., Smith, R. P. & Skipper, N. T. (2005). Superconductivity in the
  intercalated graphite compounds C₆Yb and C₆Ca. *Nature Physics* 1, 39–41. doi:10.1038/nphys0010
- Ekimov, E. A. et al. (2004). Superconductivity in diamond. *Nature* 428, 542–545. doi:10.1038/nature02449
- Hebard, A. F. et al. (1991). Superconductivity at 18 K in potassium-doped C₆₀. *Nature* 350, 600–601.
  doi:10.1038/350600a0
- Ganin, A. Y. et al. (2008). Bulk superconductivity at 38 K in a molecular system. *Nature Materials* 7, 367–371.
  doi:10.1038/nmat2179
- OEIS A002898 (honeycomb returns), A002899 (diamond returns).
- Hebard, A. F. & Fiory, A. T. (1980). Evidence for the Kosterlitz-Thouless transition in thin superconducting
  aluminum films. *Phys. Rev. Lett.* 44, 291–294. doi:10.1103/PhysRevLett.44.291
- Tanaka, M. et al. (2025). Superfluid stiffness of magic-angle twisted bilayer graphene. *Nature* 638, 99–105.
  doi:10.1038/s41586-024-08494-7
- Banerjee, A. et al. (2025). Superfluid stiffness of twisted trilayer graphene superconductors. *Nature* 638,
  93–98. doi:10.1038/s41586-024-08444-3
