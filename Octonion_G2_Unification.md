# Octonions, G2, and the 3-axes-at-a-time hypothesis — a speculative thread, honestly scoped

Tracking issue: [#162](https://github.com/rchain-community/quantum-logical-framework/issues/162).

> **Where it stands.** QLF's weak `SU(2)` is exactly *one* quaternion triple among the seven the
> octonions' 7 imaginary units decompose into (Fano-plane lines) — a real, independently-verified fact,
> not a citation (`octonion_g2_stabilizers.py`). The stabilizer chain `G2 ⊃ SU(3) ⊃ SU(2)` inside the
> octonion automorphism group reproduces textbook Lie theory exactly from this session's own
> construction, a genuine quark↔gluon algebraic relation was found and its exact `1/2` ratio *explained*
> via Schur's lemma (§3), and the `G2` root system (a real positive-geometry object, §4) was extracted.
> **The physical identification — checked, and it fails (§6):** the octonion construction forces
> `su(2)` to be a literal Lie subalgebra of `su(3)`; QLF's own gauge structure (and the actual Standard
> Model) has them as independent product factors on different-dimensional representation spaces, with no
> such nesting claimed anywhere. So the direct "same structure" reading of the octonion picture does
> *not* hold — a real, checked answer, not an unresolved gap.

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

**Why exactly `1/2`, not just that it is.** `Λ²_ℝ(m)` (15-dim) decomposes under `su(3)` as an 8-dim
block (`→ h`) + a 1-dim trace block (predicted to vanish — Schur's lemma: no equivariant map from a
trivial representation into the nontrivial irreducible `m`) + a 6-dim block isomorphic to `m` itself
(`Λ²_ℂ(ℂ³) ≅ 3̄`, matching `m`'s own representation type). Verified directly: the bracket map
`Λ²(m) → g2` has **rank 14/15 with an exact 1-dimensional kernel**, exactly as predicted, and its
nonzero singular values split into **exactly two distinct values** — `1/√2` with multiplicity 8 (the
`h`-block) and `√(2/3)` with multiplicity 6 (the `m`-block) — a **pure scalar on each irreducible
block**, exactly as Schur's lemma requires for an equivariant map. The `1/2` split follows because
`8·(1/√2)² = 6·(√(2/3))² = 4` exactly — these two specific, now-identified scalars, not a coincidence
of the whole 15-dimensional map.

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

This does not yet answer the open identification question — it only makes QLF's own `su(3)` a
well-posed object to eventually compare against, rather than an ambiguous one (previously, "QLF's
su(3)" could have meant either the compact or split real form; now the genuinely compact generators
exist explicitly, alongside the original Hermitian ones).

## 6. The physical identification — a structural mismatch, not just an unproven abstract fact

The naive question "is the octonion-derived `su(3)`/`su(2)` the same as QLF's own?" is not actually
answerable by checking whether an isomorphism *exists* — abstract representation theory guarantees one
trivially (there is only one `su(3)` and one `su(2)` up to isomorphism, so any two 8- and 3-dimensional
compact non-abelian Lie algebras with the right bracket relations are automatically isomorphic; this
proves nothing). The real, checkable content is in *how the two algebras relate to each other* within
each construction — and there the two pictures diverge structurally.

**In the octonion/`G2` construction (§2), `su(2)` is *necessarily* a genuine Lie subalgebra of
`su(3)`** — stabilizing a full quaternion triple `{e1,e2,e3}` is a strictly smaller condition than
stabilizing just `e1`, so the 3-dimensional stabilizer sits *inside* the 8-dimensional one by
construction, sharing generators, acting within the same ambient `g2`.

**In QLF's own construction, this nesting does not hold, and isn't claimed to.** Grepping the whole
repository for any stated `su(2) ⊂ su(3)` relationship finds none — `Alpha.md`'s forces section states
the gauge group is `U(1)×SU(2)×SU(3)`, a **direct product** of three independent factors
([`Forces_From_Three_Axes.md`](Forces_From_Three_Axes.md)), matching the real Standard Model's
`SU(3)_c × SU(2)_L × U(1)_Y` — color and weak isospin are independent quantum numbers, not one nested
in the other. Concretely: QLF's weak `SU(2)` (`Σ₈`, `τx,τy,τz`) acts on a **2-dimensional spinor
space**; QLF's strong `SU(3)` (`g1,g3,h1,h3`, `QLF_StrongAlgebra.lean`) acts on a **3-dimensional axis
space**. These are different representation spaces for a different physical quantum number, with no
embedding of one algebra into the other stated or provable from what's in the codebase.

**So the octonion picture predicts a structural relationship — literal subalgebra nesting — that
neither QLF's own construction nor the actual Standard Model has.** This is a real argument against the
naive identification, not a failure to find one: if the octonion `su(3)`/`su(2)` were "the same" as
QLF's in a physically meaningful sense, the nesting would have to show up somewhere in QLF's own gauge
structure, and a direct search finds no such claim — QLF treats them, correctly by the SM's own lights,
as independent product factors.

## 7. Honest scope — what remains open

- ~~**The physical identification.**~~ **Answered, negatively, with a structural reason** (§6): the
  octonion picture forces `su(2) ⊂ su(3)` as a literal subalgebra; QLF's own construction (and the
  actual Standard Model) has them as independent product factors acting on different-dimensional
  representation spaces, with no such nesting claimed or provable anywhere in the codebase. This doesn't
  rule out a looser or differently-framed connection, but the direct "same structure" reading fails.
- **The `≥5D, 3-at-a-time` hypothesis, revisited in light of §6.** Is the octonion
  structure's forced nesting a hint that a *different* labeling of QLF's axes/generators (not the naive
  "one octonion unit = one axis" reading used throughout §1–§5) might reconcile the two — or is the
  mismatch evidence the whole approach doesn't map onto QLF's specific gauge structure? Undecided.
- ~~**The quark/gluon bracket's ratio.**~~ **Resolved to `1/2` exactly, and explained** (§3): the
  bracket map is a pure scalar on each of two irreducible blocks (Schur's lemma), `1/√2` on the 8-dim
  `h`-block and `√(2/3)` on the 6-dim `m`-block, with `8·(1/√2)² = 6·(√(2/3))² = 4` producing the split.
  What's *not* derived: why those two specific scalars (`1/√2`, `√(2/3)`) — presumably the nearly-Kähler
  torsion normalization of `G2/SU(3)` fixes them, but that connection hasn't been made.
- **The positive-root cone's canonical form.** Its existence and vertex count are established (§4). A
  first attempt at the literal canonical differential form (naive vertex-fan triangulation, summing an
  elementary triangle canonical form) was **tried and failed its own consistency check**: on a plain
  square, all 4 fan-triangulations agreed (a weak test — a quadrilateral only has 2 distinct
  triangulations, both captured trivially); on the actual pentagon, the 5 fan-triangulations gave
  genuinely different values, so the naive formula is wrong for `n ≥ 5` and no canonical form is
  asserted. Needs a proper positive-geometry reference, not another guess.

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
