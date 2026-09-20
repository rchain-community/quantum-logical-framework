# Octonions, G2, and the 3-axes-at-a-time hypothesis — a speculative thread, honestly scoped

Tracking issue: [#162](https://github.com/rchain-community/quantum-logical-framework/issues/162).

> **Where it stands.** QLF's weak `SU(2)` is exactly *one* quaternion triple among the seven the
> octonions' 7 imaginary units decompose into (Fano-plane lines) — a real, independently-verified fact,
> not a citation (`octonion_g2_stabilizers.py`). The stabilizer chain `G2 ⊃ SU(3) ⊃ SU(2)` inside the
> octonion automorphism group reproduces textbook Lie theory exactly from this session's own
> construction, and a genuine quark↔gluon algebraic relation and the `G2` root system (a real
> positive-geometry object) were both computed from it. **What is NOT established:** that this
> octonion-native `su(3)`/`su(2)` is the *same representation* as QLF's own (independently built)
> strong/weak gauge algebras — both are abstractly isomorphic (there is only one `su(3)`, one `su(2)`
> up to isomorphism), which guarantees nothing about a meaningful physical identification. That
> identification is the open target this document exists to track.

This document collects a speculative exploration thread, kept deliberately separate from the
established physics in [`UniversalRelativity.md`](UniversalRelativity.md) and
[`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md) until (if) the open identification below is
resolved. It grew out of asking whether QLF's "3 spatial axes" structure — which already gives the
weak `SU(2)` as one quaternion triple (`Σ₈`, [`lean/BraKetRhoQuCalc.lean`](lean/BraKetRhoQuCalc.lean))
— generalizes to a larger axis set taken **3 at a time**, the natural combinatorics of octonion
multiplication (7 imaginary units, 7 quaternion triples, every *pair* of units lying on exactly one
triple — a Steiner system / Fano plane).

## 1. The construction ([`octonion_g2_stabilizers.py`](octonion_g2_stabilizers.py))

Octonions built via Cayley-Dickson doubling (quaternions → octonions), independently re-derived here,
not imported from a library. Verified: norm-multiplicative (a genuine division algebra), alternative,
non-associative, and the 7 imaginary units decompose into exactly 7 quaternion triples matching the
standard Fano-plane line set `{1,2,3},{1,4,5},{1,6,7},{2,4,6},{2,5,7},{3,4,7},{3,5,6}`.

`Der(O)`, the Lie algebra of derivations of the octonions (`D(xy) = D(x)y + xD(y)`), was computed
directly as the null space of a 512×64 linear system (SVD) — **not looked up** — confirming
`dim Der(O) = 14 = dim g2`. This is the definition of `g2 = Lie(Aut(O))`, machine-checked from scratch.

## 2. The stabilizer chain `G2 ⊃ SU(3) ⊃ SU(2)`

Stabilizing any single imaginary unit (derivations `D` with `D(eᵢ) = 0`) gives an 8-dimensional
subalgebra, for all 7 units alike (`G2` acts transitively on the unit imaginary octonions — the
6-sphere). Verified **non-abelian** (a real bracket check) and **closed** under the Lie bracket
(residual `~1e-16`) — consistent with `su(3)`. Stabilizing a full quaternion triple — structurally
identical to QLF's own weak-`SU(2)` triple — drops to exactly 3 dimensions, consistent with `su(2)`.

**What representation is on the remaining 6 units?** The `SU(3)` stabilizer's action on the other 6
imaginary units has commutant `{I, J}` with `J² = -I` (verified to `1e-14`) — the signature of an
**irreducible complex-type representation**: the realified **fundamental "3"** (quark-like), **not the
adjoint "8"** gluons live in. So this specific 6-unit complement is quark-adjacent, not
glueball-adjacent.

## 3. A real quark↔gluon algebraic relation ([`octonion_quark_gluon_bracket.py`](octonion_quark_gluon_bracket.py))

`g2 = h ⊕ m` via the **Killing form** (the naive Frobenius inner product on the 8×8 derivation
matrices is *not* Ad-invariant and gives a wrong split — caught and fixed during this work). `[h,m]⊂m`
reconfirms `m` (the 6-dim quark-type space) is a genuine `su(3)` representation. `[m,m]` is **not**
confined to `h` — because `G2/SU(3)` is the classical **nearly-Kähler 6-sphere**, a homogeneous space
but *not* a Riemannian symmetric space (that stronger condition would force `[m,m]⊂h` exactly; this was
initially mistaken for a bug before identifying the correct classical fact).

What *is* real: `[m,m]`'s projection onto `h` is **surjective** — every one of the 8 gluon generators
is reachable as a bracket of two quark-type elements — and the gluon-fraction is **exactly `1/2`**, not
merely close to it: summed as a basis-independent energy trace (`‖h-part‖²` vs `‖m-part‖²`) over all 15
pairs of a Killing-orthonormal basis of `m` (not a Monte Carlo estimate — an initial random-sampling
pass gave `~0.50` with std `0.054` across 2000 pairs, consistent with but not establishing the exact
value), both totals come out to `4.000000` on the nose — suggestively equal to `dim(h)/2`. This is the
real-Lie-algebra shadow of the physical `3⊗3̄ = 1⊕8` decomposition (quark-antiquark → singlet + gluon
octet), not identical to it (`m` realifies the complex "3", so this is the closest analogue available
in this structure, not a literal
derivation of QCD's Clebsch-Gordan decomposition).

## 4. G2's root system and a positive-geometry connection ([`octonion_g2_root_system.py`](octonion_g2_root_system.py))

Asked whether this thread bears on [issue #151](https://github.com/rchain-community/quantum-logical-framework/issues/151)'s
positive-geometries RFC: the honest answer is *not directly* — #151's proposal (the count-balance
"ZFA-hedron" and the central-binomial census `C(2n,n)`) connects instead to the alpha-residual thread
([`Alpha_Residual.md`](Alpha_Residual.md) §9f–9i, which works with the *same* `C(2n,n)` census). But
every compact simple Lie algebra's **root system** carries a canonical positive cone — a genuine
positive-geometry object in the technical sense (convex regions with canonical differential forms) used
in the Coxeter/root-system amplitudes literature — and `G2`'s was sitting inside this construction,
unused, until extracted here.

Found a Cartan subalgebra via the **centralizer** of a generic element (avoiding a blind search for a
commuting pair, which fails almost surely by chance), Killing-orthonormalized it, and diagonalized
simultaneously: **12 roots**, 6 short + 6 long, length ratio `√3` to 4 significant figures — the *one*
ratio that uniquely identifies `G2` among rank-2 root systems — at exactly 30° spacing. The convex hull
of all 12 is exactly the long-root hexagon (short roots sit strictly inside); a generic positive-root
split gives a genuine 5-vertex convex cone.

**Honest reading:** this is standard for *any* compact simple Lie algebra, not something specific to
QLF. What's real is that this particular `G2` instance is independently, mutually consistent with
everything else in this document (the multiplication table → `Der(O)` → stabilizer chain → quark/gluon
bracket → root system, all cross-checking cleanly) — and that it is a genuinely **separate**
positive-geometry object from #151's proposal, not a unification of the two.

## 5. A real fix this comparison surfaced ([PR #161](https://github.com/rchain-community/quantum-logical-framework/pull/161), merged)

Cross-checking QLF's own `su(3)` (`lean/QLF_StrongAlgebra.lean`) against the octonion-derived compact
`su(3)` above required knowing precisely which real form QLF's own construction uses — and its example
generators `g1, g3` turned out to be **Hermitian**, not anti-Hermitian (verified directly), so not
literally `su(3)` elements (the compact real Lie algebra is anti-Hermitian traceless matrices — the
same distinction `BraKetRhoQuCalc.lean`'s weak sector already gets right, `τᵢ = i·σᵢ`). Fixed by adding
`h1 := i·g1, h3 := i·g3` (genuinely anti-Hermitian, machine-verified `h1.conjTranspose = -h1`,
non-abelian within the anti-Hermitian slice) purely additively — the existing `g1, g3` and everything
downstream (`QLF_GaugeUnification.lean`) are untouched. See `su3_anti_hermitian_summary`.

This does not yet answer the open identification question below — it only makes QLF's own `su(3)` a
well-posed object to eventually compare against, rather than an ambiguous one (previously, "QLF's
su(3)" could have meant either the compact or split real form; now the genuinely compact generators
exist explicitly, alongside the original Hermitian ones).

## 6. Honest scope — what remains open

- **The physical identification.** Is the octonion-derived `su(3)`/`su(2)` (§2) the *same
  representation* as QLF's own strong/weak gauge algebras, under some natural, physically-motivated
  map — or merely two abstractly-isomorphic-but-unrelated structures? Dimension and type matching alone
  proves nothing (there is only one `su(3)` up to isomorphism). No attempt has been made yet to
  construct or rule out such a map.
- **The `≥5D, 3-at-a-time` hypothesis more broadly.** Octonions (7 imaginary units) are one concrete
  instantiation; whether QLF's physics actually needs or uses this structure, versus it being a
  mathematically clean but physically unmotivated generalization, is undecided.
- ~~**The quark/gluon bracket's ratio.**~~ **Resolved to `1/2` exactly** (§3, an energy-trace invariant,
  not sampling) — but *why* it's exactly `1/2` (e.g. via the nearly-Kähler torsion normalization of
  `G2/SU(3)`, which plausibly forces it) is not derived, only observed and machine-verified.
- **The positive-root cone's canonical form.** Its existence and vertex count are established (§4); its
  literal canonical differential form (the object positive-geometry theory actually studies) has not
  been computed.

None of this is claimed as established QLF physics — it is recorded here, separately, exactly because
it is not yet load-bearing for the claims in `UniversalRelativity.md` or `Forces_From_Three_Axes.md`.

## Scripts

All require `numpy` (and `scipy` for the root-system convex hulls); see
[`alpha_weight6_pslq.py`](alpha_weight6_pslq.py)'s docstring for this environment's venv bootstrap
recipe (network access works; the system Python is externally-managed and needs `--without-pip` +
a manual `get-pip.py`).

- [`octonion_g2_stabilizers.py`](octonion_g2_stabilizers.py) — §1, §2
- [`octonion_quark_gluon_bracket.py`](octonion_quark_gluon_bracket.py) — §3
- [`octonion_g2_root_system.py`](octonion_g2_root_system.py) — §4
