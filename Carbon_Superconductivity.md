### `Carbon_Superconductivity.md`

# Carbon Superconductivity: the ZFA DNA of Graphene

*Where the superconductivity thread starts: the carbon lattices written in the twist alphabet, the substitution rule
that grows graphene, and the magic-angle family of superconducting graphene stacks. A log 2 test is pre-registered
in §5 before it is run.*

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
1. Run the §5 test.
2. **The turbulence bridge.** [`Turbulence.md`](Turbulence.md) gets Kolmogorov's `−5/3` from a constant `log 2` flux
   per octave. The same identity, octave per e-fold = `log 2`, is where the [`Log2_Search.md`](Log2_Search.md) routes
   converged. Superfluids and superconductors carry quantised vortices, and quantum turbulence in a condensate has a
   Kolmogorov range. A pre-registered test of whether that range carries the substrate's `log 2` per octave is the
   natural second route.
3. The fulleride lead of §4, if a count can be framed that could fail.

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
