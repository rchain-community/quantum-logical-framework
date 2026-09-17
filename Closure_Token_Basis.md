# A QLF-Native Closure-Token Basis for Semantic Intelligence

**Resolves:** [#65](https://github.com/jimscarver/quantum-logical-framework/issues/65)
**Status:** Definitional specification, with §1's token and its quotient now machine-verified — [`QLF_ClosureEquivalence`](lean/QLF_ClosureEquivalence.lean) defines `closureToken h := (ledger h, twistMatrixFold h)`, proves the induced relation is an equivalence strictly between `=` and count-equivalence, and shows which quantities descend to its classes (the displacement, charge and phase do; `baryonNumber` does not). The rest of this document (§§2–5: the scoring, the grounding map, the learning rule) remains unverified. Each section states explicitly whether it is a definition, a derivation target, or an open problem.

The question #65 forces, sharpened from #52: not "are LLMs semantic engines" but *could a semantic engine run on integer closure machinery instead of float probability machinery, and what exactly is the token, the ledger, and the score?* This document answers each acceptance criterion in turn.

---

## 1. What a fundamental-constant closure token is

**Definition (closure token).** A closure token is a minimal admissible cycle in the 8-twist algebra: an *ordered* history of signed twist operations whose net action is zero under the Zero Free Action postulate. It is identified by **three** data, not by the count alone:

1. **the integer signature** — the count/ledger vector `c ∈ ℤ⁸` over the eight twist generators;
2. **the phase / fold normal form** — the ordered Pauli fold of the history, its scalar in `μ₄ = {±I, ±iI}` (equivalently a path-class / minimal-representative ID that fixes the order-sensitive content);
3. **the closure/admissibility witness** — the decidable receipt `full_zeno_prune history = []` (count balance ∧ Pauli closure).

The count vector alone is deliberately **insufficient**, and this is forced by the substrate, not a stylistic choice: [`QLF_PhaseInformation`](lean/QLF_PhaseInformation.lean) proves `count_does_not_determine_phase` — two histories with the *identical* twist multiset (identical `c`, identical Shannon content) can fold to **opposite** Pauli scalars (`^v<>` → `+I` boson vs `^<v>` → `−I` fermion, `fold_udlr` vs `fold_uldr`). A token identified by `c` alone would collapse exactly the order/phase distinction QLF says count-based (Shannon) accounting misses — here the collapsed distinction is *spin itself*. So the closure token is a **phase-bearing** object: integer ledger **+** fold normal form **+** closure witness. The ledger stays integer-native (criterion §3's win survives); it just is not the *whole* token. **Lean anchor:** [`QLF_ClosureEquivalence`](lean/QLF_ClosureEquivalence.lean) makes this token and its quotient machine-checked — `closureToken`, `ClosureEquiv`, `closureSetoid`/`ClosureClass`; `closureEquiv_finer_than_count` is exactly this paragraph's argument restated on the quotient, and `closureEquiv_coarser_than_eq` shows the token does forget an ordering (the relabeling orbit), so it is a genuine quotient, not identity in disguise. There the witness (3) is carried as the hypothesis `countBalanced`, so the relation is total and the physical reading is its restriction to closed histories.

**Definition (fundamental-constant closure token).** A closure token is *fundamental-constant* when its cycle count at a given order is the integer that appears in a QLF constant derivation. The canonical example is the α combinatorics: the counting argument yields the integer 137. The closure token there is the minimal cycle class whose enumeration produces that count.

*Honest status:* closure tokens are exact objects at the integer/combinatorial layer. They inherit the known gap in the α work — the derivation gives 137, not the measured 137.036. Tokens are well-defined; their claimed correspondence to physical constants carries exactly the same open problem as Alpha.md, no more, no less.

## 2. How closure tokens differ from LLM text tokens

| | LLM text token | Closure token |
|---|---|---|
| Identity | Arbitrary byte-pair symbol; index into a vocabulary | Integer ledger **+ fold normal form** of a closed cycle; structure is intrinsic (order-sensitive, not a bare count) |
| Meaning | Learned float embedding; extrinsic, statistical | Position in the admissibility graph of the twist algebra; intrinsic |
| Validity | None — every token sequence is representable, just more or less probable | Hard — a combination either closes or it does not; ill-formed combinations are *inadmissible*, not low-probability |
| Composition | Concatenation + attention over float weights | Ledger addition in ℤ⁸; the composite is a token iff the summed ledger still closes |
| Failure mode | Fluent nonsense (well-formed strings, no grounding) | Silence (no admissible completion exists) |

The last row is the design payoff: an LLM cannot refuse to emit; a closure engine can, because inadmissibility is structural.

## 3. Probabilities and logits as a reporting layer

**Design commitment:** yes. In this basis, probability is *defined* as a ratio of integer counts:

```
p(b) := N(b) / Σ_b' N(b')
```

where `N(b)` is the number of admissible closure paths extending the current context ledger to candidate `b`. Logits are then log-counts, and softmax is recovered as a display transform over count ratios. The runtime never needs a primitive real: reals appear only at the boundary where counts are normalized for human consumption.

*Honest status:* this mirrors the Born-rule-as-counting reading elsewhere in QLF. It is a definitional move, not a theorem. What *would* elevate it: a Lean proof that count-ratio probabilities over admissible paths satisfy the axioms the float layer currently supplies (normalization, additivity over disjoint branches). That proof does not exist yet and is a legitimate next Lean target — and it would be a nontrivial one, unlike the trivial-arithmetic proofs flagged in earlier review.

## 4. Scoring semantic closure without primitive reals

Score is an integer tuple, compared lexicographically:

1. **Admissibility gate** (0/1): does the candidate's summed ledger close? Failures are excluded, not down-weighted. This replaces the entire logit floor.
2. **Evidence count** (ℤ≥0): number of independent admissible paths from the context ledger to the candidate ledger. More closure routes = more semantic support.
3. **Closure deficit** (ℤ≥0, for partial candidates): L1 distance of the residual ledger from zero — how many twist operations away from closing.
4. **Tiebreak:** minimal ledger length. Occam as smallest closing cycle.

All comparisons are integer comparisons. No division, no floats, no gradients in the scoring path.

*Honest status:* path counting is the expensive step — exact counting is #P-hard in general graph settings, so a practical engine needs bounded-depth enumeration or memoized dynamic programming over ledger states. That is an engineering constraint, not a conceptual defect, but it should be stated up front.

## 5. What an integer/register-native QLF semantic engine requires

In dependency order:

1. **Alphabet enumeration.** Enumerate closure tokens up to cycle length k in the 8-twist algebra, with counts per order. This is computable today with a short script and is the right first artifact — it also directly tests whether the 137 count reappears where the theory says it should.
2. **The grounding map.** A correspondence between natural-language predicates and closure ledgers. **This is the hard, unsolved part.** Nothing in QLF currently provides it. Without it the engine is a formal calculator over twist cycles, not a semantic engine. Any claim otherwise would be the kind of overreach earlier review pushed back on. Candidate approach: learn the map by distillation — use an LLM to label ledger states, then check whether closure structure predicts semantic composition better than chance. Falsifiable, cheap to try.
3. **Ledger kernel.** Integer vector addition, closure check, bounded path counting. This drops directly into the QuantumOS Zero-Force Accounting kernel (Rust/WASM) — the accounting machinery is already integer-native, which is why the QOS-side issue is the natural runtime home.
4. **Comparison harness.** Rank candidate responses by the §4 score and by ordinary LLM logits on the same prompts; measure agreement and divergence. This is the QOS issue ("Prototype integer-ledger closure scoring for Quantum-OS agent decisions") and stays out of scope here.
5. **Learning rule.** What replaces gradient descent? Candidate: discrete search over closure-preserving ledger rewrites. Entirely speculative at this stage; listed as open, not promised.

---

## What this document settles vs. leaves open

**Settled (as definitions):** the token (§1), the token/LLM-token distinction (§2), probabilities as count-ratio reporting (§3), the integer scoring rule (§4), the dependency chain for an engine (§5).

**Open:** the 137 → 137.036 gap (inherited from Alpha.md); the Lean proof that count-ratios satisfy probability axioms; the grounding map (§5.2 — the critical one); tractable path counting; any learning rule.

**Scope boundary per #65:** QLF owns this theory document. QOS owns the runnable prototype. Nothing here claims empirical results.
