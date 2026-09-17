# Pointer-Swap Fuzz as the Pre-Geometric Mechanism Behind Operational 3D

**Resolves:** [#62](https://github.com/jimscarver/quantum-logical-framework/issues/62)
**Status:** Mechanism specification, more speculative than the closure-token spec ([#65](https://github.com/jimscarver/quantum-logical-framework/issues/65), [`Closure_Token_Basis.md`](Closure_Token_Basis.md)). Each stage below is tagged **[Definition]**, **[Analogy]**, or **[Open]**. Only Stage 4 currently yields a computation that could falsify the picture; that computation is the proposed resolution artifact — and a first cut of it is run in [`pointer_swap_fuzz.py`](pointer_swap_fuzz.py) (see §Stage 4).

The [Quantum Logical Framework](README.md) settled the *counting* layer of dimension elsewhere; this doc isolates the *mechanism* layer.

## Scope boundary (what #42 settled, what this covers)

[#42](https://github.com/jimscarver/quantum-logical-framework/issues/42) settled the *counting* layer: 8-twist alphabet → 6+2 split → 3 axis-pairs → apparent 3D. That is combinatorics ([`QLF_Generations`](lean/QLF_Generations.lean), [`SpaceTime.md`](SpaceTime.md) §3a) and stays closed.

This document covers the *mechanism* layer #62 isolates: how n-dimensional pointer-swap dynamics becomes sparse operational 3D *for an embedded observer*. The pipeline, in Allen's framing:

```
pointer-swap fuzz → chromodynamic binding → sparse relational geometry → embedded observer sees 3D
```

Four stages, taken in order.

---

## Stage 1 — Pointer-swap fuzz **[Definition]**

Allen's intuition: information cannot disconnect; incessant swapping is the "grease in the gears." Formalized:

**Definition (swap).** A swap is a transposition of pointer assignments between two substrate nodes — an involution on the reference graph that preserves each node's closure ledger.

**Definition (fuzz).** No admissible substrate state is static: connectivity (the no-disconnection constraint) forces every state to lie on a nontrivial swap orbit. The *fuzz* is the orbit itself — the equivalence class of states under rapid swapping. **Observables are swap-invariants only.** Anything that changes under a swap is below the resolution of any embedded observer, by construction.

This is the load-bearing definitional move of the whole document: "fuzz" is not noise added to a geometry; it is the statement that pre-geometric state is only defined up to swap orbit, and geometry can only be built from orbit invariants. It is the same pre-spatial discipline as the spin guardrail ([`Spin_QLF.md`](Spin_QLF.md) §9, [#107](https://github.com/jimscarver/quantum-logical-framework/issues/107)): the primitive is a process over closures, not a thing moving in existing space.

*Status:* internally consistent as a definition. Not yet connected to the Lean substrate — the swap group action on twist signatures is definable in Lean today and would be a legitimate (nontrivial) formalization target.

## Stage 2 — The 8-gluon / 3-bit index **[Open — currently a count coincidence]**

The tempting identification: SU(3) has 8 generators; the twist alphabet has 8 elements; 3 axis-pairs give a 3-bit operational index with 8 values. Three eights.

Plainly: **a coincidence of counts is not a map.** dim(su(3)) = 8 buys nothing by itself — plenty of unrelated structures have cardinality 8. What would elevate this to a result:

- A concrete homomorphism from the swap group acting on twist signatures into SU(3) (or its adjoint action), and
- Preservation of structure constants — the twist-algebra composition rules must land on the su(3) commutation relations, not merely match in dimension.

No such construction exists in the repo. Until one does, the gluon connection is stated as a *conjectured correspondence*, never a derivation. This is the same discipline applied to the 137 vs 137.036 gap in [`Alpha.md`](Alpha.md): name the exact missing object rather than blur past it. The missing object here is the homomorphism. (QLF's strong sector *does* carry a real `su(3)` — the traceless 3-axis directional tensor of [`QLF_StrongAlgebra`](lean/QLF_StrongAlgebra.lean), `gluon_commutator_nonzero` — so the target algebra exists; the missing piece is the swap-group → that-algebra map, not the algebra.)

## Stage 3 — Binding as the selector of the rendering **[Analogy]**

The claim: chromodynamic/strong-force binding is *why* 3D becomes the lived rendering rather than one option among many.

Structural reading in QLF terms: confinement admits only color-neutral composites as free states ([`QLF_Confinement`](lean/QLF_Confinement.lean), `charged_not_closed` — a net-colored state is not a ZFA closure). Translated: only **swap-closure-neutral composites** — bundles whose internal ledgers fully close — are stable against the fuzz. Their internal swap degrees of freedom are saturated inside the bundle; what remains externally visible is exactly the residual 3 axis-pair structure from the 6+2 split. The Borromean three-colour necessity ([`QLF_QuarkStructure`](lean/QLF_QuarkStructure.lean), `baryon_needs_all_three_axes`) is the same "all three axes required to close" that leaves 3 external axes. Atoms/protons are then sparse relational nodes: closure-neutral bundles embedded in, and screened from, the fuzz.

*Status:* this is an **analogy to confinement, not a derivation of it or from it**. It becomes a result only if one shows, from the swap dynamics of Stage 1, that closure-neutral composites are precisely the swap-orbit fixed structures — i.e., the only entities whose external description is fuzz-independent. That proof does not exist. It also silently depends on Stage 2's missing homomorphism (without the su(3) map, "chromodynamic" is a borrowed word, not a mechanism).

## Stage 4 — Sparse relational rendering, and the one falsifiable check **[Definition + computable test]**

The claim: apparent volume is not filled space; it is delayed relational rendering — relational addresses resolved on demand when interactions require them.

**Correction (per [#112](https://github.com/jimscarver/quantum-logical-framework/issues/112) — the fuzz is not the test object).** The raw pointer fuzz must not be reified into a geometry. Stated sharply:

> **Raw pointer fuzz has no geometry to measure. Operational geometry appears only after matter integrates recurring bit-flip coincidence patterns into stable closure receipts.**

This is the receipt ontology QLF uses everywhere: only **closures** are receipts ([`Completeness_Evidence.md`](Completeness_Evidence.md) §2a — *measurement is counting*, the raw substrate is not itself observable), and closure is horizon-relative ([`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean)). So the decisive object is **not** the raw swap graph — it is the **quotient of the fuzz by atomic integration**: the classes of recurring coincidence patterns that matter latches into stable closure receipts. Geometry is measured on *that* quotient, never on the pointer layer.

**The real test:** "embedded observers see 3D" ⟺ the **dimension of the atom-latched coincidence-receipt classes is 3** — growth measured on the receipt quotient (after atomic integration), not on the raw swap graph. This is the causal-set move (Myrheim–Meyer; [`QLF_CausalDimension`](lean/QLF_CausalDimension.lean)), but applied to the receipts, which *are* the causal-set events — not to the sub-observable fuzz beneath them.

**The raw-swap-graph model below is a toy — safe as a spec, but not the intended object.** The first-cut computation builds distance and ball growth on the *raw* swap graph (`d(A,B)` := minimal swaps carrying node A's ledger to node B's; `V(r)` := nodes within swap-distance r). It reifies the fuzz — nodes, paths, distances — exactly as the correction warns against, so its exponent is a property of the *modeled graph*, not of rendered geometry. Read it as fixing the falsifiable *shape* of the question (dimension is measured, not assumed), **not** as the decisive run:

- Exponent ≈ 3 on the toy: suggestive of the shape only — the raw graph is not the receipt quotient.
- Exponent ≠ 3: informative about the toy's split, not a verdict on the mechanism.

The decisive object is the receipt quotient (open item #1). A mechanism claim that cannot fail is what earlier review flagged; this one can — once it is tested on the right object.

### First-cut computation — read the result honestly

[`pointer_swap_fuzz.py`](pointer_swap_fuzz.py) builds one concrete instantiation of the Stage-4 swap graph (nodes = reorderings of one closure ledger; edges = single **adjacent transpositions**, the minimal unbiased reading of "swap of pointer assignments" that does *not* bake in any spatial dimension) and measures the ball-growth exponent three ways (log-log fit, volume-doubling exponent, local slope). **The model is a construction, not the unique reading of the spec** — the swap generating set has genuine freedom, and a different-but-faithful reading could move the exponent. The script prints its exact modelling choices so they can be challenged.

**What the first cut actually gives:**

| swap graph | nodes | growth exponent |
|---|---|---|
| S₃ / S₄ / S₅ / S₆ full permutations | 6 / 24 / 120 / 720 | permutohedron, degree `L−1` → **3 exactly at L=4** |
| balanced 2 pairs (len 4) | 6 | ~0.8 (too small to read) |
| balanced 3 pairs (len 6) | 90 | log-log 1.5; doubling peaks ~1.8 |
| **balanced 4 pairs (len 8)** | 2520 | log-log 2.4; **volume-doubling exponent peaks ≈ 2.9** before finite-size saturation |

Two honest signals fall out, neither rigged (the model bakes in no axes):

1. The adjacent-swap permutohedron of `L` distinct pointers has growth degree `L−1`, which equals **3 precisely at `L = 4`** — the length of the minimal ZFA chiral closure (the electron loop `^<v>`, `fold_electron`). So this reading yields 3D iff the operative swap length is the fundamental 4-twist fluxoid — a substantive tie to the minimal closure, **not** a free knob, though *why* `L=4` is operative is not derived.
2. The **length-8, four-complement-pair balanced closure** — i.e. the full 8-twist alphabet's own count-balanced structure — has a volume-doubling exponent that **peaks near 3** (≈2.9) in its pre-saturation regime. The 8-twist substrate's own closure class carries a growth dimension close to 3.

Treat these as *one instantiation's evidence*, not a verdict: on finite graphs a growth "dimension" is an estimate (the exponents drift with radius and saturate), and the balance constraint suppresses swap directions so the number is generating-set-dependent. **The content of the raw-graph toy is that the question is computable and falsifiable, a first computation exists, and it lands near 3 for the two substrate-natural closure lengths (4 and 8) rather than for an arbitrary one.** But per #112 this toy tests the *wrong object* — the raw swap graph, not the receipt quotient.

**Finite-size ladder — the raw-graph exponent diverges ([`Genesis.md`](Genesis.md) §4b, run [`genesis.py`](genesis.py)).** The extrapolation the caveat above demands: it measures the raw binary `(k,k)` swap-graph ball-growth `D(k)` up a size ladder, to test whether `D` *converges*. It does not — `D` climbs straight past 3 and keeps rising, at a steady increment ≈ `0.27` per `k` (`D ~ k·log2/log k → ∞`):

```
k (=(k,k))    #nodes   diam     D(k)
         4        70     16   1.6094
         5       252     25   1.8808
         6       924     36   2.2302
         7      3432     49   2.5124
         8     12870     64   2.7744
         9     48620     81   3.0146  > 3
        10    184756    100   3.2184  > 3
D increments D(k+1)-D(k): [0.271, 0.349, 0.282, 0.262, 0.24, 0.204]
linear slope of D vs k  : 0.2728  (steady & positive)
```

So the raw graph's "≈3 at moderate size" is a **crossing, not a limit** — an *independent, quantitative confirmation* of the "drifts with the string length" caveat, and the sharpest reason the raw graph is the wrong #62 object (for the *external* 3-D rendering). The instrument that *does* converge — stably, size-independently — is the receipt quotient below. **The raw-graph excess is not waste, though** ([`Genesis.md`](Genesis.md) §"the particle zoo"): the receipt quotient is the *externally rendered* 3-D, and the raw graph's growth *beyond* 3 is read as the **internal gauge/color dimensions** — degrees of freedom not perceived as space, manifesting as the stronger (color) force. External 3-D + internal-color is a clean split of the two swap measures.

### The receipt-quotient model (issue #112) — the right object, built

The decisive object is the geometry of the **atom-latched coincidence receipts**, not the raw fuzz. A receipt is a ZFA closure, and its **swap-invariant content** (observables are swap-invariants only, Stage 1) is its per-axis signed count — define the

> **axis-winding vector** `axisWindingVector(ts) := (x⁺−x⁻, y⁺−y⁻, z⁺−z⁻) ∈ ℤ³`,

the net signed twist count along each spatial axis-pair. Because it is a *count*, it is genuinely permutation-invariant — reordering the history leaves it fixed — so it *is* swap-invariant content, and the raw fuzz (reorderings) is exactly what the quotient onto `axisWindingVector` discards. **Now in Lean:** [`QLF_ClosureEquivalence`](lean/QLF_ClosureEquivalence.lean) defines `axisWindingVector` (as the `ℤ³` projection of the `ℤ⁸` ledger) and proves it is a class function of the closure quotient (`axisWindingVector_class_function`), while `baryonNumber_not_class_function` proves the distinction drawn in the correction that follows — the same class carries baryon numbers `4` and `−4`. **(Correction, #114/#112 — this is a distinct object from `baryonNumber`.** QLF's `baryonNumber` ([`QLF_BaryonWinding`](lean/QLF_BaryonWinding.lean)) is a signed 3-axis *linking* scalar — a sliding-window sum of oriented `signTriple`, **sequence-dependent** and hence *not* swap-invariant — so it is a chirality/linking invariant, not the displacement quotient. Both are winding-style receipt invariants; they are not the same object, and the geometry quotient is `axisWindingVector`, not `baryonNumber`.)** Atomic integration = latching one coincidence = `±1` along one axis of `axisWindingVector`, so **the receipt quotient is the `ℤ^d` lattice** with `d` = the number of axis-pairs, and its ball `V(r)` is the `L¹` ball `|{v ∈ ℤ^d : |v|₁ ≤ r}|` (the Delannoy number). Computed in [`pointer_swap_fuzz.py`](pointer_swap_fuzz.py):

| `d` = #axis-pairs | 1 | 2 | **3** | 4 |
|---|---|---|---|---|
| receipt-quotient growth dimension (doubling exp) | 0.98 | 1.96 | **2.94** | 3.92 |

The growth dimension is **exactly `d`, stably** — independent of closure size (contrast the raw permutohedron's `L−1`, which drifts with the string length). **For the 8-twist alphabet, `6` spatial twists `/2 = 3` axis-pairs** (the 6+2 split, [`QLF_Generations`](lean/QLF_Generations.lean) / [`QLF_FineStructureSubstrate`](lean/QLF_FineStructureSubstrate.lean)), so `d = 3` and the receipt quotient **renders as 3D**. This is **not baked in**: a `d`-axis-pair alphabet gives dimension `d` (the `d = 1,2,4` rows prove the exponent tracks the axis count, not a chosen 3). Geometry is the axis-windings of the closures — the 3 spatial axes — measured on the receipts, never on the raw fuzz, exactly as #112 required. **This back-stops the α cross-sector theorem** ([`Alpha.md`](Alpha.md) §6a): that theorem cites this receipt-quotient growth dimension as the *mechanism*-layer evidence for `d = 3` (alongside the counting-layer 6+2 split), so the result here lands the check the α overdetermination joint explicitly depends on — the residual being the posited atomic-integration map, not the exponent.

**Residual (named, not rigged):** that atomic integration = `axisWindingVector` accumulation is the modelling *map* — the per-axis signed count is a genuine swap-invariant of the closure, but the *identification* of atomic integration with `±1` steps of it is posited, not derived; and the continuum limit of the `ℤ³` lattice is the usual order→metric step ([`QLF_CausalDimension`](lean/QLF_CausalDimension.lean) / [`QLF_OrderMetric`](lean/QLF_OrderMetric.lean)). (`baryonNumber` sits alongside as the *linking/chirality* scalar, a separate receipt invariant — not this displacement quotient.)

---

## Settled vs. open

**Settled (as definitions):** swap, fuzz-as-orbit, observables-as-invariants (Stage 1); relational distance and apparent volume (Stage 4); the precise statement of what "sees 3D" means (growth exponent 3).

**Modelled (the receipt quotient, #112):** the decisive object — growth dimension of the atom-latched coincidence receipts (their swap-invariant axis-windings) — is built and computed: it equals the axis-pair count `d`, **stably**, and `d = 3` for the 8-twist alphabet, so the receipt quotient renders 3D (`pointer_swap_fuzz.py`, receipt-quotient section). The residual is the modelling map (atomic integration = axis-winding accumulation) + the lattice→continuum step, both named above.

**Open, in order of importance:**
1. The swap-group → su(3) homomorphism (Stage 2) — the difference between a gluon connection and a numerology.
2. Closure-neutral composites as swap-fixed structures (Stage 3) — turns the confinement analogy into a theorem target.
3. Lean formalization of the swap action (Stage 1) + the `ℤ³`-lattice → continuum step (`QLF_CausalDimension`/`QLF_OrderMetric`).

**What this document does not claim:** that QCD is derived, that 3D is proven emergent, or that the fuzz picture is anything more than a formally stated, now-falsifiable hypothesis.

## References

### Internal
- [`Genesis.md`](Genesis.md) §4b (run: [`genesis.py`](genesis.py)) — the finite-size extrapolation ladder showing the raw binary swap-graph exponent **diverges** (does not converge to 3), quantifying the "drifts with string length" caveat; and (§2) the exact `−p/2` census spectral exponent that counts conjugate pairs.
- [`Closure_Token_Basis.md`](Closure_Token_Basis.md) — the closure-token alphabet the Stage-4 swap graph is built over (#65); the two specs are composable.
- [`SpaceTime.md`](SpaceTime.md) §3a — the counting layer (#42): why the faithful rendering of the closure graph is minimally 3D.
- [`Spin_QLF.md`](Spin_QLF.md) §9 — the same pre-spatial discipline (process over closures, not motion in existing space).
- [`Alpha.md`](Alpha.md) — the "name the missing object" discipline applied to the α residual (the model for Stage 2's honesty).
- [`Open_Problems.md`](Open_Problems.md) — `pointer_swap_fuzz_in_progress`.

### Lean anchors
- [`lean/QLF_ReachableEvent.lean`](lean/QLF_ReachableEvent.lean) — the pre-geometric relational skeleton (causal set, no coordinates) the swap graph refines.
- [`lean/QLF_CausalDimension.lean`](lean/QLF_CausalDimension.lean) — dimension measured from a relational graph (the Myrheim–Meyer / growth-exponent move).
- [`lean/QLF_StrongAlgebra.lean`](lean/QLF_StrongAlgebra.lean) — the real `su(3)` target algebra of Stage 2.
- [`lean/QLF_Confinement.lean`](lean/QLF_Confinement.lean), [`lean/QLF_QuarkStructure.lean`](lean/QLF_QuarkStructure.lean) — closure-neutral (color-neutral) composites of Stage 3.

### External
- L. Bombelli, J. Lee, D. Meyer, R. Sorkin (1987), *Space-time as a causal set*, Phys. Rev. Lett. **59** 521 — dimension from a relational order.
- J. Myrheim (1978), *Statistical geometry*, CERN TH-2538 — the growth/ordering-fraction dimension estimator.
