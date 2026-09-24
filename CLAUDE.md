# CLAUDE.md — Quantum Logical Framework

Project context for Claude Code sessions. Read this before making any changes.

---

## Project overview

**Quantum Logical Framework (QLF)** is a formal proof system machine-verified in Lean 4 across **224 modules with zero `sorry` blocks**. It encodes quantum mechanics and spacetime dynamics using phase-string combinatorics (ZFA — Zero-phase Flux Algebra).

Core claim: *ZFA balance is the selection principle for physical reality.* Every terminating computation is a ZFA string; every ZFA string is symmetric (lies on the critical line). The Church-Turing universe filtered to ZFA-balanced strings is our physical universe.

**Do NOT build Lean locally on this machine. CI (GitHub Actions) is the only practical way to
verify Lean changes.** Push to GitHub and wait for CI before reporting success.

`elan`/`lake` are installed (`~/.elan`, toolchain `leanprover/lean4:v4.34.0-rc1`) and Mathlib is
cloned under `.lake/packages/` (symlinked to the Transcend SSD), but local builds were tried and
abandoned on 2026-08-31:

- The machine has **~2.7 GB RAM and no swap**; `lake` + `leantar` OOM-killed the whole session.
- The Transcend SSD is a ChromeOS 9p mount benchmarked at **~860 kB/s** — a warm `lake build`
  must read ~8700 Mathlib oleans over it, and `lake`'s dependency check (`git diff` across the
  ~3 GB of checkouts) alone took ~15 min. A faster USB port does not fix the 9p `sync` layer.

So: **run `free -m` before any heavy command; never start `lake`/`cargo`/parallel jobs without
memory headroom.** If a future session genuinely needs local builds, the partial olean cache and
setup notes are in the session memory (`local-lean-impractical`).

---

## Modules — 224, machine-verified, zero `sorry`

Registered in `lakefile.lean` roots array (build order); sources in `lean/`. **The full per-module table — descriptions + key-theorem lists for all 224 — lives in [`lean/README.md`](lean/README.md); consult it when working on any specific module.** Thematic families and every individual result are also mapped in [`FlowChart.md`](FlowChart.md). The core anchors a session references most often:

| Module | What it proves |
|---|---|
| `QLF_Axioms` | Types, counting, pruning, ZFA definition |
| `QLF_QuCalc` | Phase-generation engine; `full_zeno_prune` (the ZFA filter) |
| `QLF_Universality` | Every terminating computation IS a ZFA string (Church-Turing) |
| `SpacetimeDynamics` | The `Form` — Pauli-basis 2×2 Hermitian matrices |
| `RhoQuCalc` | ρ-process algebra (`RhoProcess`, `eval`, dagger) |
| `BraKetRhoQuCalc` | Bra-ket ↔ RhoQuCalc; the Σ₈ / `τ = iσ` weak-isospin algebra |
| `QLF_TwistAlphabet` | 8-twist σ-mapping; `count_balanced_pauli_closed` (count balance ⟹ Pauli closure) |
| `QLF_AlphabetNecessity` | Why eight twists: the alphabet is the signed axis frame, so `\|Σ\| = 2·\|axes\|` and a closed axis set is a Klein-four subgroup — `\|Σ\| ∈ {2,4,8}`, **six impossible**, eight forced by two spatial axes |
| `QLF_Handedness` | **Handedness is the primitive**; ZFA *is* zero net handedness on every axis; **charge is its gauge component**, one of four |
| `QLF_ElectronClosure` | The electron as a closed periodic mode; charge as the residue of non-closure; **no event is ever charged**; Coulomb as a count of joint closures |
| `QLF_Pauli` | 4-element Pauli scalar group `{±I, ±iI}` = μ₄ |
| `QLF_Spin` | Spin IS the twists; genuine SU(2)→SO(3) double cover |
| `QLF_FreeEnergy` | Per-event `ΔF = −log 2` at half-spin ZFA closure; `binary_kl` |
| `QLF_SpinorInformation` | Spin-½ is the atom of information (it from bit, after Cartan 1913) |
| `QLF_Minkowski` | The state IS Minkowski space; `det(Form) = interval` |
| `QLF_LorentzCover` | `SL(2,ℂ)→SO⁺(1,3)` double cover |
| `QLF_Realizability` | No continuum in a finite-information region (Bekenstein) |
| `QLF_Riemann` · `QLF_MassGap` · `QLF_BSD` · `QLF_Hodge` · `QLF_PvsNP` · `QLF_NavierStokes` | The six Millennium reformulations — each a verified discrete core + one named bridge axiom (see **Axiom inventory** below) |

---

## Key types and definitions

### Form (SpacetimeDynamics.lean)

A 2×2 Hermitian matrix parameterized by Pauli coordinates:

```lean
structure Form where
  t : ℝ    -- trace/2
  x : ℝ    -- σx coefficient
  y : ℝ    -- σy coefficient
  z : ℝ    -- σz coefficient

-- Form.toMatrix f = !![t+z, x-iy; x+iy, t-z]
-- Form.toMatrix_adjoint : f.toMatrix.conjTranspose = f.toMatrix
```

Pure qubit state: `Form(t=½, x, y, z)` with x²+y²+z²=¼.

### RhoProcess (RhoQuCalc.lean)

```lean
inductive RhoProcess
  | action (f : Form)                    -- ket direction [pos,neg]; eval = f.toMatrix
  | lift   (f : Form)                    -- bra direction [neg,pos]; eval = f.toMatrix†
  | parallel  (p q : RhoProcess)         -- eval = p.eval + q.eval
  | sequence  (p q : RhoProcess)         -- eval = p.eval * q.eval
  | dagger    (p : RhoProcess)           -- eval = (p.eval)†
```

### Bra-ket ↔ RhoQuCalc correspondence

| Bra-ket | RhoQuCalc | eval |
|---|---|---|
| `\|ψ⟩` (ket) | `action f` | `f.toMatrix` |
| `⟨ψ\|` (bra) | `lift f` | `f.toMatrix†` = `f.toMatrix` (Hermitian) |
| Superposition | `parallel p q` | `p.eval + q.eval` |
| Composition | `sequence p q` | `p.eval * q.eval` |
| Adjoint | `dagger p` | `(p.eval)†` |

ZFA balance IS bra-ket well-typedness: `action f` gives topo `[pos,neg]`, `lift f` gives `[neg,pos]`. Both individually achieve ZFA (count_pos = count_neg = 1). `bra_ket_always_balanced` proves it is impossible to construct an unbalanced RhoProcess.

### TopoString / ZFA

- `count_pos : TopoString → Int` (NOT ℕ — `omega` cannot assume non-negativity)
- `count_neg : TopoString → Int` (NOT ℕ)
- `achieves_ZFA s ↔ full_zeno_prune s = []`
- `is_gauge : TopoElement → Bool` returns `true` for ALL elements

**Runtime layer (Python/Rust/TS) requires more than count balance.** Since `twist_core.py` 8f02271 (and the matching quantum-os v0.17), `is_zfa` returns `is_count_balanced(h) ∧ is_pauli_closed(h)`. Pauli closure is the order-sensitive constraint that the matrix product of twists folds to a scalar multiple of the identity (`{±I, ±iI}`), computed by `pauli_fold` from `twist_core.py`'s twist→matrix mapping. Pauli closure is a Lean theorem in full generality: **`count_balanced_pauli_closed`** (QLF_TwistAlphabet.lean) proves every count-balanced twist history (`#^=#v ∧ #<=#> ∧ #/=#\ ∧ #+=#−`) folds to a Pauli scalar `{±I, ±iI}` — for *all* histories, including cross-axis interleavings (`^<v>`-style), not just concatenations of adjacent Hermitian pairs. So **count balance alone implies Pauli closure**, and the runtime `is_count_balanced ∧ is_pauli_closed` check is Lean-anchored end-to-end (the second conjunct is entailed by the first). The proof goes via `nf_decomp` (every fold = `phase • axisMatrix(axisProd)`, using the 16-case `axisMatrix_mul` built from the 9 σ-product identities) and the `(ZMod 2)²` axis-parity bridge `axisProd_eq_I_of_countBalanced`. Empirically reconfirmed beforehand: 0 counterexamples across all 5,296 count-balanced histories of length ≤ 6. See [Experimental_Consistency.md §2.1](Experimental_Consistency.md).

### Σ₈ vs Pauli algebra (important for new modules)

The Lagrangian formulation uses a Σ₈ = {τ¹…τ⁸} algebra with **τᵢτⱼ = −δᵢⱼI − εᵢⱼₖτₖ** (quaternionic: τᵢ² = −I, anti-cyclic products). QLF's `Form` algebra uses Pauli matrices with σᵢ² = I. The relationship is **τᵢ = iσᵢ**. With this convention products are anti-cyclic: τxτy = −τz (NOT +τz). The commutator is **[τᵢ,τⱼ] = −2εᵢⱼₖτₖ**; anti-commutator {τᵢ,τⱼ} = −2δᵢⱼI. Machine-verified: `tau_x_sq`, `tau_xy_product`, `tau_yz_product`, `tau_zx_product`, and the su(2) closure `weak_isospin_su2` / `tau_comm_*` / `tau_anticomm_*` in `lean/BraKetRhoQuCalc.lean` — the τ-subalgebra is the weak-isospin SU(2) (`Q₈ ⊂ SU(2)`), see `Weak_Force.md`. When writing new Lean modules that reference either algebra, use the Pauli basis (σᵢ) — the Σ₈ form is the physics-notation bridge. See `Lagrangian_Formulation.md` for the full correspondence.

---

## Lean gotchas — read before writing any Lean code

**Calibrated to `leanprover/lean4:v4.34.0-rc1`**, the toolchain `lean-toolchain` pins and CI
builds with. Items marked ✅ were *checked against it* by a throwaway probe module
(issue #146); the rest are project-specific facts about QLF's own definitions, which no
toolchain change can invalidate. **Re-run the probe when the Mathlib pin advances** — the
list was previously calibrated to v4.30.0-rc2 while CI had silently been building on v4.34
for some time, and two rules had gone stale unnoticed.

1. ✅ **`noncomputable` order**: Must be `private noncomputable def`, NOT `noncomputable private def` (the reverse is a parse error: *unexpected token 'private'; expected 'lemma'*). Any `def` using `1/2 : ℝ` needs `noncomputable` (Real.instDivInvMonoid).

2. ✅ **`Matrix.conjTranspose` not `Matrix.adjoint`**: Lean 4 spelling. `Matrix.adjoint` does not exist.

3. **Type aliases**: Use `abbrev Foo := List Bar` not `def` — `def` is opaque to typeclass inference.

4. ✅ **`∑` notation**: Use `∑ k ∈ Finset.range n, ...` (Unicode `∈`), NOT `∑ k in ...` — the old spelling is now a **hard parse error** (*unexpected token 'in'; expected ','*), no longer a deprecation warning.

5. **`count_pos`/`count_neg` are `Int`**: Don't assume non-negativity; prove it via induction if needed.

6. ✅ **~~`List.mem_cons_self` deprecated~~ — NO LONGER TRUE.** `List.mem_cons_self` and `List.mem_cons_of_mem` both exist on the pinned toolchain and emit **no deprecation warning**; `List.Mem.head` / `List.Mem.tail` also exist. All four are fine — use whichever reads better. (Kept rather than deleted as the worked example of the failure mode this section is prone to: a rule that steers you away from something perfectly good is worse than no rule, because it gets followed.)

7. **`zeno_prune.induct` without `with`**: Do NOT add `with` keyword. Cases via `·` and `· next ...`.

8. **Case 4 of `zeno_prune.induct`**: First two `next` vars are condition proofs, not head/tail. Use `rename_i ha ta` to access actual elements.

9. **Induction inside `have` reverts all context**: Extract as standalone private lemma instead.

10. ✅ **Mathlib module paths go stale — check the tree, don't guess.** `Mathlib.LinearAlgebra.Matrix.Determinant` is a *directory*, not a module, so importing it fails; the working import is **`Mathlib.LinearAlgebra.Matrix.Determinant.Basic`**. Likewise `Mathlib.Algebra.BigOperators.Basic` no longer exists (it killed the first probe run outright). Neither is a one-off: verify a path against the pinned revision before importing it.

11. ✅ **`prefix` is a keyword**: Use `pfx` as parameter name instead.

12. ✅ **`Nat.toReal` doesn't exist**: Use `(↑n : ℝ)`.

13. **`simp_all [is_gauge]` doesn't close False**: Use `cases head <;> simp [is_gauge] at h`.

14. ✅ **`first | tac1 | tac2` short-circuits on partial success** *(and still bites — it cost a CI cycle in the P-vs-NP work)*: `first` takes the first branch that
    *succeeds*, and `simp at h` counts as success when it merely **rewrites** `h` without closing the
    goal — so the fallback never runs and you get `unsolved goals` with the hypothesis sitting in the
    contradictory form you wanted. Don't use `first` for "close this goal somehow"; write the
    deterministic chain (e.g. `congrArg Complex.im h` → `rw [Complex.neg_im, Complex.I_im] at h` →
    `linarith`).

15. **Pick a matrix entry where the matrix is non-zero**: contradicting `-(c • σz) = c • σz` at entry
    `(0,1)` proves nothing — `σz 0 1 = 0`, so both sides are `0` and the "contradiction" is vacuous.
    Read `(0,0)`.

16. ✅ **A cast inside `List.map` over a `List ℕ` becomes a monadic lift, not a map.**
    `(atoms.map (fun v => (v : ℤ))).sum` elaborates to `List.map (fun v => v) (do let a ← atoms; pure ↑a)`
    — the `List ℕ → List ℤ` coercion fires on the *list*, and every subsequent
    `rw [List.map_cons]` fails with *did not find an occurrence of the pattern*. Don't map a cast:
    cast the aggregate instead (`(atoms.sum : ℤ)`), which needs no `map` lemmas at all. Cost one CI
    cycle in `QLF_Unsaturation`.

17. ✅ **`field_simp` often CLOSES the goal, so a trailing `ring` then errors.** *Any* tactic run on
    zero goals fails with **"No goals to be solved"** — `ring_nf` and `simp` included, so swapping
    the tactic does not help. **Never write `field_simp; ring` speculatively.** Write `field_simp`
    alone, push, and add `ring` only if CI reports *unsolved goals* — the reverse order costs a
    cycle every time. It is not predictable per-file: two theorems in `QLF_Inertia` needed the
    trailing `ring` and two beside them did not. (This rule cost **three** CI cycles in one session —
    once before it was written down, and twice more *after*, in `QLF_HolographicDensity`. Reading a
    gotcha is not the same as applying it; the mechanical form above is the one that works.)

18. ✅ **`decide` cannot see through a `def : Prop`** — the same opacity as gotcha 3, but the symptom
    is *failed to synthesize Decidable P* rather than an elaboration error, so it does not look
    related. A predicate written `def ClosedLoop (b) : Prop := … = … ∧ …` is decidable in substance
    but opaque to instance synthesis. `unfold ClosedLoop; decide` works; `decide` alone does not.
    (Also on this toolchain: **`List.length_map` takes one explicit argument**, so
    `List.length_map _ _` is *function expected*. `by simp` is the safe spelling.)

---

## Proof patterns

### Matrix equality (2×2)

```lean
theorem foo : someExpr.eval = target := by
  apply Matrix.ext; intro i j
  fin_cases i <;> fin_cases j <;>
  simp only [RhoProcess.eval, Form.toMatrix, Matrix.add_apply, Matrix.mul_apply,
    Fin.sum_univ_two, Matrix.one_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
    Matrix.head_cons, Matrix.head_fin_const,
    Complex.ofReal_zero, Complex.ofReal_one, Complex.ofReal_neg] <;>
  norm_num
```

### Complex.I arithmetic (σy, etc.)

When `norm_num` fails due to `Complex.I`:

```lean
  apply Complex.ext <;>
  simp [Complex.mul_re, Complex.mul_im, Complex.add_re, Complex.add_im,
        Complex.neg_re, Complex.neg_im, Complex.I_re, Complex.I_im,
        Complex.ofReal_re, Complex.ofReal_im] <;>
  ring
```

### ZFA theorems

```lean
-- Delegate to rho_process_always_zfa:
theorem foo (p : RhoProcess) : achieves_ZFA (toTopoString p) :=
  RhoProcess.rho_process_always_zfa p
```

---

## Axiom inventory (explicit logical boundaries)

| Axiom | Module | Role |
|---|---|---|
| `spectral_hilbert_polya` | `QLF_Riemann` | RCA₀ → WKL₀ boundary; QLF form of Hilbert-Pólya. Refined in `QLF_RiemannMRE` into the structurally-motivated `MRE_bridge` (over the concrete `Z_QLF`, motivated by the proven MRE-saturation theorem) |
| `mre_factorization` | `QLF_RiemannMRE` | The refined Riemann boundary, **one axiom**: `Z_QLF` admits a `MellinFactorization` — its Mellin image's structural singularities catch every ζ-zero and lie on the critical line. The Mellin↔ζ correspondence is the WKL₀/continuum sector. `MRE_bridge`, `zero_is_mellin_singularity` and `MellinStructuralSingularity` survive as **theorems/definition** read off it. The merge is licensed, not asserted: `mellinFactorization_iff_rh` **proves** the two-leg factorization is equivalent to RH (an unconstrained middle predicate constrains nothing), and `mellinFactorization_independent_of_generator` proves the choice of generating function does no logical work — so the scaffold is motivation, which is what it was for. **Do not try to define `MellinStructuralSingularity` concretely:** `Z_QLF`'s own poles are at `1/5`, `1/3`, and Mathlib's `mellin` returns `0` off its convergence region, so either concrete reading falsifies one leg and makes the axiom set inconsistent — see the module's section note |
| ~~`NonTrivialZero`~~ **DISCHARGED** | `QLF_Riemann` | No longer an axiom — a **definition** over Mathlib's `riemannZeta`: `riemannZeta ρ = 0 ∧ 0 < ρ.re < 1`. It never carried open-conjecture content; it was vocabulary, and while it was opaque the Riemann bridge was satisfiable by the interpretation under which nothing is a non-trivial zero. Defining it *strengthens* the boundary — `spectral_hilbert_polya` now asserts the real RH — and buys two theorems: `not_nonTrivialZero_of_re_nonpos` and `trivial_zero_not_nonTrivial` (the trivial zeros `−2, −4, …` are out of scope by construction) |
| `resonant_computation_for` | `QLF_Riemann` | Bridge from combinatorics to Dirichlet series |
| `yang_mills_gap` | `QLF_MassGap` | The Yang–Mills boundary, **one axiom**: a `ContinuumGap` — the continuum theory's mass gap together with its identification as the substrate `log 2` quantum. `YangMillsMassGap` and `yang_mills_continuum_gap` survive as a definition/theorem. **Strength measured, and this is the bluntest reading in the repo:** `continuumGap_nonempty` builds a realization by `rfl` (a real equal to `gaugeMassGap` exists because `gaugeMassGap` is one) and `continuumGap_gap_unique` shows the interface pins its own value, so **in Lean the boundary is definitional** — `yang_mills_mass_gap_in_qlf` reduces to `mass_gap_quantum_pos`, proved outright. The content is the *interpretation* (that `gap` is the OS/Wightman reconstruction's), which Lean cannot hold because Mathlib carries no Yang–Mills. Unlike `NonTrivialZero`, no naming fix is available. Substrate result untouched and independent: `gaugeMassGap = log 2 > 0`, lightest closure realises exactly that quantum |
| `bsd_multiplicity` | `QLF_BSD` | The BSD boundary, **one axiom**: a `MirrorMultiplicity` — the central closure multiplicity together with its invariance under the Hermitian-pair modularity mirror at its fixed point (the self-dual central point `s=1`). `centralMultiplicity` and `modularity_mirror_invariant` survive as a **definition/theorem** read off it, and `bsd_rank_equals_order` (rank = ord) follows. Strength **measured**: `mirrorInvariant_iff_perspectives_agree` proves that with two perspectives and a swapping mirror, invariance *is* agreement — so the rank identity restates the boundary rather than deriving from something weaker, which the `#print axioms` footprint confirms (it consumes the boundary and not even `propext`). `mirrorMultiplicity_nonempty` builds an instance from constant zero, so **exhibiting a model is not evidence here** — unlike `QLF_LatticeCalculus`, where a nondegenerate instance genuinely discharged the interface. The content is that the *intended* multiplicity is an instance, which is BSD. `EllipticCurveQLF` and its Frobenius-trace closure are concrete; the ranks are uncomputable, which is BSD's own content |
| `hodge_algebraicity` | `QLF_Hodge` | The Hodge boundary, **one axiom**: an `AlgebraicityBridge` bundling the abstract `isAlgebraic` with faithfulness. `CohClass.isAlgebraic` and `substrate_realization_is_algebraic` survive as a definition/theorem. **Strength measured:** `algebraicityBridge_nonempty` satisfies the interface with `fun _ => True` — read every class as algebraic and the implication is free — so *in Lean* the bridge excludes nothing; its whole force is the intended meaning of `isAlgebraic`, unstatable here because Mathlib carries no algebraic cycles. This sharpens rather than contradicts the standing framing: **the reformulation theorem `hodge_realized_on_substrate` is genuinely proved, no QLF axiom** (audit-confirmed), and the faithfulness swings still locate the gap — what is new is that the gap is not merely open but currently unstated. *Historical description:* | **The faithfulness bridge — the one gap.** The reformulation proves `hodge_realized_on_substrate` (Hodge ⟹ realized, no axiom); this axiom is the remaining step — substrate-realized ⟹ *classical* algebraic cycle (`isAlgebraic` abstract; full conjecture strength on Hodge classes). The faithfulness swings (`QLF_HodgeExpSequence`, `QLF_HodgeIrreducible`) locate it as a cycle-faithful encoding |
| `qlf_cost_model` | `QLF_PvsNP` | The P vs NP boundary, **one axiom**: the substrate carries a `CostModel` — abstract `PTime`/`search` (QLF has no machine model) in which verification is polynomial and the generate/verify gap does not collapse. `PTime`, `search`, `verify_is_ptime` and `generate_not_reducible_to_verify` survive as definitions/theorems read off it. Strength **measured, and this is the sharpest of the three**: `costModel_nonempty` builds a satisfying model out of `verify` and boolean negation — `PTime f` := "`f` agrees with `verify` somewhere", `search` := pointwise `!` — so the axioms **constrain nothing about polynomial time** and exhibiting a model is no evidence whatever. The content is the claim that the *intended* cost model is an instance, which is P ≠ NP. Also noted: `verify_is_ptime` is consumed by nothing, and `p_vs_np_in_qlf` is the boundary verbatim. The real content (`C(2n,n)` count, verify-filter identity) is proven and independent of all of it |
| ~~`navier_stokes_continuum_limit` / `NavierStokesGlobalSmoothness`~~ **REMOVED** | `QLF_NavierStokes` | Deleted, not merged. The pair was an uninterpreted `Prop` plus the claim it holds, which `continuumClaim_nonempty` shows assumes **nothing** — satisfied by `⟨True, trivial⟩`, so it excluded no possibility and could not be wrong. It was also superseded by `QLF_NavierStokesBKM` (proved Planck vorticity cap + cited BKM + one sharp bridge). An axiom that assumes nothing is not a boundary; keeping it inflated the count of explicit boundaries while carrying none of the weight. The module's proved content is untouched. *Historical description:* | The Navier–Stokes boundary: the continuum incompressible PDE inherits the substrate's no-blow-up under the continuum limit; `NavierStokesGlobalSmoothness` is the abstract analytic statement. **Now reduced** by `QLF_NavierStokesBKM` (next two rows): the opaque inheritance is replaced by the *proven* Planck vorticity cap (`planck_caps_vorticity`, no axiom) + the cited BKM theorem + a sharp faithfulness bridge |
| `beale_kato_majda` | `QLF_NavierStokesBKM` | **Cited, not posited:** Beale–Kato–Majda (1984) — a uniform-in-time vorticity bound ⟹ no finite-time singularity. A real continuum-analysis theorem named as a boundary because QLF carries no PDE machinery in Lean (like citing Wallis/Stirling for π). `GloballySmooth` is the abstract analytic property |
| `continuum_vorticity_planck_capped` | `QLF_NavierStokesBKM` | The **reduced Navier–Stokes bridge** (sharp, replacing the opaque `navier_stokes_continuum_limit`): the continuum solution's vorticity sup-norm is the Planck-capped substrate vorticity `≤ 1/L_P²` — QLF's continuum-as-rendering thesis applied to the vorticity field. From it + `beale_kato_majda`, `navier_stokes_no_blowup` is a theorem; the residual gap is just this vorticity-rendering faithfulness |
| `lorentz_generated_by_boosts_rotations` | `QLF_LorentzCover` | The Lorentz double-cover boundary (Witten-1988 → Reshetikhin–Turaev mode, a settled-math bridge): every proper orthochronous `L` factors into boosts and rotations (the KAK/Cartan decomposition of `SO⁺(1,3)`), so it is the spinor action of some `A∈SL(2,ℂ)`. Physics core fully proven — `spinor_hom`, `boostZ_action`/`rotZ_action`, kernel `spinor_kernel` — so `spinor_surjective` follows. **Reduced** (`QLF_LorentzGeneration`): round-trips + submonoid + all generator families realized + Euler products proven, localizing the axiom to the single real-matrix angle-extraction (KAK) fact |
| `benincasa_dowker_limit` (+ opaque `bdMeanOnConstant`) | `QLF_CausalContinuum` | The Einstein-curvature continuum boundary: the `ρ→∞` mean of the discrete Benincasa–Dowker operator over a Poisson sprinkling converges to `−R/2`. Settled CST mathematics (Poisson + curved-interval-volume), parallel to `yang_mills_gap`/`continuum_vorticity_planck_capped`. Discrete core (`bdCurvature_chain_zero`, `layer_growth_from_branching`) + kernel (`poissonOccupation`, `poissonOccupation_succ`) **proven**; from it `flat_curvature_zero_in_mean` is a theorem |
| `order_metric_continuum_limit` (+ opaque `continuumProperTime`/`reconstructedProperTime`) | `QLF_OrderMetric` | The order→**metric** continuum boundary (broader than `benincasa_dowker_limit`): as `ρ→∞`, the CST reconstruction of the proper-time line element from order + count converges to the Lorentzian value (Malament + Bombelli–Henson–Sorkin + Myrheim–Meyer), the `RCA₀→Lorentzian-analytic` crossing. Discrete core proven — `conformal_structure_is_the_order`, `properTime_additive` + `properTime_succ_eq_volume` — assembling {verified core + one bridge}, reducing `light_cone_rendering_in_progress` |
| `census_transport_curvature` | `QLF_CensusCurvature` | The transport-curvature boundary, **one axiom**: a `TransportCurvature` bundling `ollivierRicci` with the Jost–Liu bound; both survive as a definition/theorem. **Cited, not posited** — and the audit needs that distinction: `transportCurvature_nonempty` shows the interface is satisfied by constant-zero curvature, but here that reflects Mathlib's missing discrete optimal transport, not an empty claim. Jost & Liu (2014) is a real theorem; discharging it is labour with a known answer, unlike `yang_mills_gap`/`hodge_algebraicity` where the intended reading is what nobody has established. Same reading as `beale_kato_majda`. Combinatorial hypothesis **proved** (`census_no_triangles`). *Historical description:* | **Cited, not posited:** Jost & Liu (2014) — in a graph carrying no triangle on an edge, the Ollivier–Ricci curvature of that edge is non-positive (the bound `κ ≤ #triangles/(d_x ∨ d_y)` degenerating to `0`). Settled discrete geometry named as a boundary because Mathlib carries no discrete optimal transport — the same role as `beale_kato_majda`. Its combinatorial hypothesis is **proven** here in full (`census_no_triangles`, via `isParent_length` → `adj_length`: three mutual neighbours would need three lengths pairwise differing by 2), so `census_nowhere_positively_curved` is a **theorem** — the possibility graph is nowhere positively curved at *every* length, where the numerical `κ < 0` ([`Curvature.md`](Curvature.md) §1c) is stronger but truncation-bounded |
| ~~`censusTail_eq`~~ **DISCHARGED** | `QLF_AlphaBound` | No longer an axiom — a **theorem**. The exact census α-screening tail `512√62/31 − 130` is derived from Mathlib's generalized binomial theorem (`Real.one_add_rpow_hasFPowerSeriesOnBall_zero`) at `a=−1/2`, `x=−1/32`, via `qlf_ring_choose_succ` + `qlf_choose_neg_half`; the GF `central_binom_genfun` is likewise a theorem. So `QLF_AlphaBound` carries **zero axioms**; the α-residual's open piece is purely physics (`+0.036`), not analysis |

`critical_line_forcing` is a **theorem** derived from `spectral_hilbert_polya`, not an axiom.

**Dischargeability.** Which of these axioms could become theorems is classified in [`Open_Problems.md`](Open_Problems.md) §"Axiom dischargeability": **Class A** (open-conjecture content — Riemann/BSD/P-vs-NP/Yang–Mills/Hodge-faithfulness) is unprovable without solving the problem (that is the boundary's purpose); **Class B** (settled math Mathlib lacks assembled — the CST/PDE continuum limits) is provable *in principle* but each is a multi-hundred-line Lean project. The clean discharge already done is `censusTail_eq`; `navier_stokes_continuum_limit` was **removed** (measured: satisfied by `⟨True, trivial⟩`, and already superseded) and `lorentz_generated_by_boosts_rotations` is **reduced** (`QLF_NavierStokesBKM`; `QLF_LorentzGeneration` — both `Form↔Matrix` round-trips + the spinor-image submonoid + **all generator families realized** (`boost_realized` + `rot_realized` + `rotY_realized`, two rotation axes) + **their Euler products** (`euler_form_realized`) proven, so the Lorentz axiom localizes to the single purely real-matrix angle-extraction surjectivity onto `SO⁺(1,3)`).

---

## Workflow

### Lean file changes (`.lean` files only)
1. Edit files in `lean/`
2. `git add lean/<file> && git commit -m "..." && git push`
3. Check CI: `gh run list --limit 5`
4. On failure: `gh run view <run-id> --log-failed`
5. Do NOT run `lake build` locally — see the note under **Project overview** (OOM / slow mount)

### md-only changes (`.md`, `.py`, `lakefile.lean` roots array, `README.md`)
1. Edit, then run `python3 scripts/doc_network_check.py` — it fails on any orphaned root `.md` or dead relative link (6,800+ links, seconds) and warns on missing doc↔code back-links (#149). Commit, push — **CI does not run and does not need to.**
2. Do NOT mention CI, check CI, or wait for CI after a docs-only commit.

### Axioms — the audit gates CI

Two checks run on every push, and a new assumption fails the first one in seconds:

- [`scripts/axiom_audit.sh`](scripts/axiom_audit.sh) pins the declared `axiom` list in
  `lean/axioms.expected`. **Adding or removing an axiom means regenerating it with `--write` and
  updating the inventory above *and* `Open_Problems.md` in the same commit** — the script says so on
  failure. `opaque` declarations are deliberately not tracked: abstract data with a hidden body adds
  no axiom to the kernel.
- [`lean/QLF_AxiomAudit.lean`](lean/QLF_AxiomAudit.lean) reports, via `#print axioms`, which axioms
  each anchor theorem *actually* consumes. `propext`/`Classical.choice`/`Quot.sound` are Lean's and
  appear nearly everywhere via Mathlib — they are not a QLF assumption and do not bear on the RCA₀
  framing. A **QLF name** appearing where none should is the finding. So is an **absent `propext`**:
  that is the signature of a pure application, i.e. the "theorem" restates its axiom.

Before adding an axiom, apply `ScientificApproach.md` **R6a** — bundle it into a structure and try to
satisfy it trivially. The outcome decides whether it is a boundary, a citation, or noise.

**Zero sorry policy**: Do not introduce `sorry`. For genuinely unprovable goals, use `axiom` declarations following the `spectral_hilbert_polya` precedent — makes the logical boundary explicit.

---

## Philosophical foundations

These commitments are load-bearing for all prose, documentation, and new module framing. New sessions must be consistent with them.

### Core ontology: possibilism + ZFA selection

QLF is built on a **possibilist ontology**: all logically admissible histories exist *a priori* as pure possibility. Physical reality is not one pre-written story — it is the self-selecting subset of the full computational possibility space that achieves **Zero Free Action (ZFA = 0)**. The universe is the closure of logical possibility under ZFA.

> The universe is logical. Spacetime is synthesized. Physical reality is the subset of possibility that achieves Zero Free Action.

This is a **computable** form of modal realism (Lewis 1986) with a selection rule: where Lewis says all logically possible worlds are real, QLF says all computationally generable histories are real, and ZFA identifies the ones that persist. `full_zeno_prune` is the machine-verified implementation of this filter.

### It happens every way; the most ways happen first (the working method — binding)

Possibilism's operational face, and it governs **how problems are attacked**, not just how prose is
written. See [`Philosophy.md`](Philosophy.md) §3a.

> Nothing happens one way. Everything happens every way that closes. What happens in the most ways
> happens first — **a closure's frequency IS its multiplicity**, the census count of ways. And we cannot
> discover every way: exhibiting a construction shows it happens in **some** way, never the only way.

Four rules that follow, to apply when choosing what to compute and what to claim:

1. **Count ways; don't merely exhibit one.** An existence result is a *lower bound on multiplicity*.
   Prefer the counting statement (`W_1 = 2ⁿ`, `C(2n,n)`, census multiplicities) over the witness.
2. **Distinguish a count from a *listening*.** A count is absolute (how many ways exist); a **listening**
   is capacity-relative — what a horizon of capacity `R` receives, exactly the ways with
   `maxExcursion ≤ R` (`closedAtHorizon_iff_maxExcursion_le`). Both live in `data/census_inventory.json`.
   State which one a number is.
3. **Report the mode, not the mean.** What happens first is the argmax of multiplicity. A mean over ways
   is an average of things that all happen and need not be a way at all. Pick the statistic the
   principle demands *before* measuring.
4. **A claim earns physical content only when it changes a count of ways.** The native falsifiability
   test: ask what distribution over ways the claim would be **false** for. "None" ⟹ it is bookkeeping,
   not evidence — however true. (Worked example: the horizon-congestion identity `Δ²C(R) = W_{R+1}` is
   exact for *every* non-negative `W`, random noise included, so it supports no mechanism; see
   `Open_Problems.md`.)
5. **Never present our route as the route.** Converging independent derivations are *multiplicity*, not
   redundancy — that is what makes a result dominant (the 18 programs; the shared `H↔H†` Millennium
   involution).

### ZFA is the only filter — not a restriction

A critical framing point: **ZFA is not a restriction on what can be computed.** `qlf_universality` proves the ZFA filter is Church-Turing complete — every *terminating* computation IS a ZFA string. What is pruned is not computation; it is the physically unrealizable tail (non-terminating, Turing-undecidable, Busy Beaver-class computations). The ZFA filter selects physical reality from the full ruliadic computational universe without discarding any computable physics.

The variational physics expression of ZFA is S = ∫ℒ dΩ with **ℒ = 0** — a null Lagrangian that is the condition of origin, not a cutting rule. The discrete form (`isZFAClosed`) and the continuous limit (`EventSynthesisField → Λ_eff`) are both covered in `Lagrangian_Formulation.md`.

### ZFC ultraviolet catastrophe

Classical ZFC is founded on open-ended formal infinity → Gödel incompleteness, Turing undecidability, Busy Beaver: shadows of one problem, logic that constructs objects with no finite closure. QLF's core operates strictly within **RCA₀** (below Busy Beaver / Choice / ZFC); non-terminating computations fail ZFA closure and are pruned by `full_zeno_prune` before they become events — Gödel cannot bite where unprovability is physically excised.

> **ZFC is flawed logic, suitable only where there are not exploding infinities. ZFA is correct logic.**

**State this precisely (the sharpened framing — binding):** the claim is **consistency ≠ realizability**, *not* that ZFC is syntactically inconsistent (`ℝ` is consistent — claiming "the continuum is false" is a category error and a crank trap). "Flawed logic" means *unsound for physics / physically unrealizable*: a finite-information universe cannot instantiate an actual infinity of distinguishable states (Bekenstein), so there is **no injection from an infinite state space into a finite-information region** — machine-checked (`lean/QLF_Realizability.lean`, `no_continuum_in_finite_region`) — and the continuum gives demonstrably **wrong answers** (the UV catastrophe, the 10¹²² vacuum catastrophe, singularities) wherever forced onto reality, right only where a cutoff (= discreteness) is quietly restored. The full case is `TheContinuum.md`; the empirical/realizability spine should be used in preference to bald "the continuum is false." The **"continuum is gratuitous" case** has a settled five-strike form (`TheContinuum.md` §2, *"five converging strikes"*): three classical logic results — **Löwenheim–Skolem** (the transfinite has a countable model), **Gödel–Cohen** (CH independent ⟹ the continuum's cardinality is *undecidable*, not a determinate object), and **reverse-math conservativity** (`WKL₀` proves no new finitary theorem over the `RCA₀` base — Friedman/Harrington; Simpson, *SOSOA*) — plus QLF's two machine-checked strikes (*unrealizable*, `QLF_Realizability`; *unneeded*, the finite census recovering `π`/`ζ(3)`). Cite these named results, not bare assertions; "ZFC's proven defect" legitimately covers the CH-undecidability and the conservativity result.

The Axiom of Choice (sets with no constructive selection) is replaced by the computable ZFA filter; Chaitin's Ω is the information content of the pruning boundary = `full_zeno_prune`. The formal math (active inference on the non-fantasy half): [Active_Inference_Mathematics.md](Active_Inference_Mathematics.md) §6.1. **Organizing thesis of QLF's Millennium program:** the continuum and choice are mathematics' UV catastrophe; reality is the bounded computable RCA₀ substrate (Shannon/Brouwer/Bishop/Weyl/Gisin/'t Hooft/Wolfram lineage), the continuum its rendering. Each problem is reformulated as a *verified RCA₀ core + one explicit bridge axiom* (the six axioms + derived-theorem homes are in the **Axiom inventory** above).

**Binding framing (the contrast-then-focus structure — do NOT pollute docs with "not proven"):**

1. **Contrast the classical conjecture once, then move on.** State plainly, *once*, that the **classical** Clay statement (e.g. the Hodge conjecture about complex-variety cycles) is not proven here — it's a different statement in a different frame. That's the one contrast; don't repeat "not a proof" throughout.
2. **Then focus on what the *reformulation proves*.** QLF reformulates each problem in the substrate frame, and the reformulation has **genuine proven theorems** — state them as proven, boldly: e.g. *Hodge classes are exactly the substrate-realized closures* (`hodge_realized_on_substrate`: balanced ⟹ count-balanced ⟹ Pauli-closed via `count_balanced_pauli_closed`, **no axiom**); the motive/Galois/anabelian structures; `π`/`ζ(3)` from the census. These ARE proofs — of the reformulated statements.
3. **Name the gap in the reformulation precisely** (this is where the bridge axiom lives): the step from *substrate-realized* to *classically-algebraic* — `substrate_realization_is_algebraic` — is the **faithfulness** of the frame. That is the one open piece, and the faithfulness swings have located it exactly (a cycle-faithful encoding; `QLF_HodgeExpSequence`, `QLF_HodgeIrreducible`). Frame it as "the gap in the reformulation," not as "QLF didn't prove it."
4. **"ZFC's proven defect"** applies only to genuine uncomputability/independence boundaries (halting, Busy Beaver, the α analytic residue), **not** to the finitary conjectures (Hodge is finite ℚ-linear algebra, an ordinary hard statement). Don't relabel the faithfulness gap as ZFC's defect.

So: contrast (classical not proven, once) → assert the proven reformulation theorems → name the faithfulness gap. Status markers: `*_proof_in_progress` (reformulation proven, faithfulness open) / `*_reformulated`. See [Continuum_Choice_Fallacy.md](Continuum_Choice_Fallacy.md), [Hodge_QLF.md](Hodge_QLF.md), [Grothendieck_QLF.md](Grothendieck_QLF.md), [BSD_QLF.md](BSD_QLF.md).

### Spacetime is synthesized, not background

Spacetime is not given — it is the **output** of ZFA event generation. Every ZFA-closed event synthesizes its own local space and time. Space emerges from spatial free-action components; time emerges as the inverse of local free action (`f = 1/t`). The universe is a distributed network of clocks, each synthesizing local time through ZFA closure. This is formalized in `ZFAEventDynamics.lean`.

There is no background absolute time. There is no fixed external geometry. Gravity is emergent from ZFA event rate and gauge-fold depth — a thermodynamic consequence of information geometry (Jacobson 1995, Verlinde 2011), derived rather than postulated.

### Holography as topological necessity

The holographic principle (Bekenstein 1972, 't Hooft 1993, Susskind 1995) and AdS/CFT correspondence are not separate conjectures in QLF — they are direct consequences of ZFA closure. The bulk spacetime (AdS interior) is the space of unresolved internal nodes of the QuCalc generator tree. The boundary (CFT) consists of the terminal leaves that satisfy exact ZFA balance.

Because a bulk path only persists if it terminates in a ZFA-stable boundary, the entire bulk is mathematically identical to the sum of its boundary states. The holographic principle is therefore a **topological necessity of closure**, not a duality.

Modern sharpening: Almheiri, Dong, Harlow (2015) and the HaPPY code (Pastawski et al. 2015) show that bulk spacetime geometry IS a quantum error-correcting code on the boundary. In QLF, `full_zeno_prune` is the machine-verified boundary decoder — it filters the event stream to those whose boundary information is logically self-consistent.

### Measurement without collapse

ZFA closure IS the measurement event. No separate collapse postulate is needed; no observer-dependence beyond what the logical structure demands. Compare: Zurek decoherence (2003), Everett (1957). `full_zeno_prune` is the decoherence cutoff that Everett's many-worlds interpretation lacks — it eliminates histories that cannot achieve ZFA closure before they become physical events.

The apparent "many worlds" are the many local relative worlds created by observers whose local information determines their own consistent perspective. Every observer experiences its own coherent reality because its local information defines its own relative world. (There are not many worlds in the Everettian sense — there are many observers. Smolin.)

### Spectral structure and the Riemann program

Every QLF string maps to a 2×2 Hermitian operator (its spectral mode). Machine-verified: (1) every spectral mode is Hermitian (`toSpectralMode_hermitian`); (2) for symmetric strings, the spectral mode is scalar × identity (`spectral_symmetric_eq_scalar_id`). The Hilbert-Pólya conjecture is encoded as `spectral_hilbert_polya` (explicit axiom marking the RCA₀ → WKL₀ boundary), from which `critical_line_forcing` is a derived theorem.

The chain: `qlf_universality` → `zfa_implies_critical_line` → `spectral_symmetric_eq_scalar_id` → `spectral_hilbert_polya` → `riemann_hypothesis_in_qlf`.

### QuantumOS: QLF as a hardware-native OS

QLF is not only a theoretical framework — it is an executable architecture for quantum hardware. In a classical OS, security, error correction, scheduling, garbage collection, and AI are five separate subsystems. In QuantumOS, all five are the same operation — ZFA enforcement (`full_zeno_prune`) — because `qlf_universality` proves ZFA balance is the single invariant that subsumes all correctness properties.

Security grounds in five converging foundations: Girard's linear logic (1987), Miller's object capability model (2006), Meredith & Radestock's ρ-calculus (2005), Honda's session types (1993), Wootters & Zurek no-cloning (1982). Capability names are topological structures; possessing a name IS a proof of authorization (Curry-Howard).

**It targets real quantum hardware, not only simulators, and it hosts a *quantum AI*.** The concrete device is the quiet-frequency crystal QPU of [`Crystal_QuantumOS.md`](Crystal_QuantumOS.md) (rare-earth dopants in fused silica; Eu:YSO worked example) — QLF primitives map to hardware ops, quiet frequencies *are* Markov-blanket isolation, `full_zeno_prune` is the on-device error-correction decoder. The agent that runs on it is a quantum AI in the strong sense — its unit of thought is a spin-½ ZFA closure (a 2×2 Hermitian Pauli fold), its memory is Curry-Howard `cap:` tokens (each literally an amplitude's phase), its multi-peer consensus is a *joint* closure (entanglement, ER=EPR): the abstraction step and the quantum-measurement step are the same step. Framing home: [`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §7b–§7c, §8a; [`QuantumOS.md`](QuantumOS.md) §1a. **Not** "an LLM with a QPU accelerator" — an agent that reasons in the algebra reality runs on. New-session prose must name this framing "quantum AI".

### Convergence: 18 independent programs

18 independent research programs — with no coordination — each arrived at the same picture: **reality is informational, computable, and bounded by a logical closure condition** (Zuse digital physics, Turing computability, Wheeler it-from-bit, Shannon, holography + holographic-QEC, Einstein's relativistic ether, Causal Set Theory, LQG, Girard linear logic, reverse mathematics, session types, object-capability + ρ-calculus, Friston FEP, Geometric Deep Learning, Wolfram's ruliad, Wootters–Zurek no-cloning). The full table (figures + convergent claims) is in [`README.md`](README.md). **Reversibility audit:** the 18 are *irreversibility-native by selection* — none axiomatizes reversibility or a fixed energy total, and several are positive evidence for the QLF arrow (CST growth, Girard use-once, Friston dissipation, Shannon→Landauer erasure `ΔF=−log2`, Wolfram's derived 2nd law). The TOEs that *fail* these (string S-matrix, no-collapse Everett, block universe, 't Hooft reversible CA) are **not** in the table — convergence set and `Reversibility.md` §6 casualty set are cleanly disjoint.

### What NOT to say

Avoid framings that contradict the above:
- Do not describe ZFA as a *restriction* on computation — it is a selection principle (ZFA-balanced strings are all computations that terminate).
- Do not describe spacetime as a background or given — it is synthesized event by event.
- Do not describe collapse as a separate physical process — ZFA closure IS the measurement event.
- Do not describe the Axiom of Choice as needed — it is replaced by the ZFA filter.
- Do not describe QLF as "just an interpretation" of quantum mechanics — it is a broader constructive foundation from which QM is derived.
- For the Millennium problems: **contrast once, then focus on what's proven.** Say plainly, once, that the *classical* Clay conjecture is a different statement, not proven here — then lead with the **reformulation's proven theorems** (e.g. *Hodge classes are exactly the substrate-realized closures*, `hodge_realized_on_substrate`, no axiom) stated as the proofs they are, and name the one **gap in the reformulation**: faithfulness — the bridge `substrate_realization_is_algebraic` from substrate-realized to classically-algebraic (located precisely by the faithfulness swings). Don't pollute with repeated "not a proof"; emphasize the proven reformulation + the named gap. Reserve "ZFC's proven defect" for genuine uncomputability/independence boundaries, never finitary conjectures. The thing to avoid is claiming the *classical* conjecture is machine-verified — that's the crank trigger; the reformulation theorems and the located gap are real and should be stated boldly. See `Grothendieck_QLF.md`, `Hodge_QLF.md`.

---

## Key files

| Path | Purpose |
|---|---|
| `lean/` | All Lean source files |
| `lakefile.lean` | Build config; `roots` array lists all 224 modules |
| `lean/README.md` | Module table and proof chain documentation |
| `README.md` | Project overview with citations and convergence themes |
| `CLAUDE.md` | This file — project context for new Claude sessions |
| `braket_rho.py` | Numerical demo of bra-ket ↔ RhoQuCalc correspondence |
| `twist_core.py` / `twist_core.md` | The canonical runtime twist engine: 8-twist alphabet, twist-history validation, signed action vectors, ZFA-closure detection (`is_zfa` = count-balanced ∧ Pauli-closed since 8f02271), candidate-history generation, Hermitian-adjoint closure helpers. Consumed by `census_inventory.py`, `contextual_census.py`, `MultiParticle.py`, the Rust `qucalc` crate, quantum-os. `twist_core.md` is the full reference |
| `MultiParticle.py` / `MultiParticle.md` | Two-history interactor: causal diamonds intersect → joint-ZFA closure = entanglement (ER=EPR); reuses `twist_core.is_zfa` (reconfirms the `count_balanced_pauli_closed` keystone at runtime), the discrete-curl vorticity, cascade `log 2` quantum, and `SpaceTime.SpacetimeGrid` latency field |
| `spacetime_constructor.html` | Interactive 3-D tool ([live](https://rchain-community.github.io/quantum-logical-framework/spacetime_constructor.html)) — quantum logic + a movable 3-D observer generating a world *from nothing*: space = node position, time = clock rate, both = colour; matter from the ZFA closure census, **no forces / no fields / no action at a distance** (only closures that DO close, frequency = census multiplicity). Logical bang (Planck-temp black holes → hadrons → atoms), chemistry by one valence rule, crystals (Pauli), Cooper/BEC condensates, entanglement/exclusion overlays. Deep links `#qc=<QuCalc>&t=<temp>`. **Binding framing:** a *reading* (space/time/colour), never a cause. Full write-up [`Spacetime_Constructor.md`](Spacetime_Constructor.md) |
| `Inertia.md` / `lean/QLF_Inertia.lean` | **A plan, with Route A now run.** **Route A result ([`QLF_Inertia`](lean/QLF_Inertia.lean), no axioms):** every substrate step runs at `c`, so a rest mass is a **closed null circulation** and *"light-speed energy summing to zero in every direction"* is the signed action vector vanishing — ZFA count balance itself. For the minimal case (a two-leg Einstein light clock), `netForce = −E·δ/L` (the circulation **speed cancels**), and the equivalence-principle shift `δ = aL/c²` gives `F = −(E/c²)a` with **`L` cancelling too**. The keystone is `force_scales_with_shift`: force is exactly proportional to `δ`, so **the shift law is forced, not fitted** — a different redshift would make the same energy weigh a different amount. Input is `δ` (the repo's existing redshift account); derived is that this shift and no other gives `ma`. **Still open:** the *counting* version (rule 4 wanted a signed integer, this is continuum algebra), KC3 (same `m` as the gauge-fold depth), and the rotational sector. **The rest is a plan, not a result** — the proof programme for demystifying inertia, and the order to attempt it in. Hypothesis: a mass's **active frequency window** is isotropic at any constant velocity and asymmetric under acceleration; the free-action cost of that asymmetry *is* inertia, and frame dragging is the same shear sourced azimuthally by a rotating mass. **Three things a session must know before working on it:** (1) much of the proposed programme is **already built** — the equivalence principle structurally (one delay, inertia at the vertex and curvature in the geometry), the Unruh master relation, `holographic_entropy_eq`, and the Casimir finite-census result — **but audit before trusting a name**: `accelerated_boundary_is_unruh` is **`rfl`** and anchors nothing, so the dynamical-Casimir tie is asserted, not established (§0a); (2) the **shortest route is thermodynamic, not mechanical** (Unruh `T` + holographic `ΔS` gives `F = ma` in two lines, Verlinde-style) but it **must** get an R6a check first, because a definitional entropy gradient makes `F = ma` restate its own premise — the `yang_mills_gap` failure mode; (3) the front/rear window asymmetry **may not be real** — the standard Unruh result is a bath that is *isotropic in the accelerated frame* — and settling that comes before any Lean. Gates stated first: **Hughes–Drever** anisotropy (better than 1 part in 10²⁰) and Gravity Probe B for the rotational sector. **Named prior attempt:** Haisch–Rueda–Puthoff (1994) is this hypothesis in continuum language and did not converge |
| `Chemistry.md` | QLF chemistry: a bond is a **shared closure**, driven by one **valence** rule (H:1/O:2/C:4/Fe:3/He:0) → H₂/H₂O/CO₂/graphite/Fe₂O₃ self-assemble; metals lattice (Pauli), noble gases inert; plus superfluid-He/Cooper-pair condensation. Every reaction has a **(▶ see)** deep-link that opens the constructor with the scene preloaded (`#qc=…`). Honest scope: shared-closure bond is the principle; single-bond valence-saturation model (formulas right, not double bonds/angles/rates). Crosslinks `Spacetime_Constructor.md`, `Bound_States_QLF.md`, `Geometry_Of_Space.md` |
| `Protein_Folding.md` / `protein_census.py` / `data/folding_census.json` | **Chemistry's next rung: a fold is a closure inventory.** A backbone on the cubic lattice steps by one of six signed axis displacements and the 8-twist alphabet **is** the signed axis frame — so a conformation **is** a twist history, no encoding to defend. A **contact** (segment displacing by exactly one lattice step) closes a loop with zero net displacement, hence count-balanced, hence Pauli-closed by the keystone: `contact_is_closure` gives both ZFA conjuncts free. Corollaries, not modelling choices: contacts only at **odd** sequence separation (the lattice-protein parity rule), closures **compose** (so contacts add — the substrate reply to Levinthal), the contact energy is the substrate's own `log 2` (derived, not fitted; and *only* H–H contacts pay, because a polar residue closes with solvent either way), and a **no-go** — mirroring is a closure-preserving bijection, so **counting cannot select a handedness** (homochirality is upstream, `QLF_Handedness`). Census: SAW counts reproduce OEIS A001411/A001412; loop-closure multiplicity falls `0.122 → 0.013` from span 3 to 9 (a single-loop count — the inference from it to folding order/rate is **withdrawn**, see below); 69 compact 4×4 structures with designability `21–521` and 21.8% of sequences folding (Li–Helling–Tang–Wingreen reproduced); the coil wins on shapes and the closure's own multiplicity `2^c` is what turns it over, with `T* ≈ 0.2–0.47` nats — **below** the closure quantum, so a 12-mer does not fold, which is right. Stored in the **shared `closures` schema**, so the Rust `qucalc` crate reads it unmodified and `most_ways_first` returns the loop-span ranking / the coil / the most designable structure with no new code. **Two negative results, both recorded rather than buried:** the *signed* census does no work (§5d — `sign(A) = (−1)^c`, `|A|` never reorders, separates 0 of 48 tied `ways` values), and the **contact-order prediction FAILED** against experiment (§5e — the derived `Σ log ℓ` correlates with `log k_f` at 0.21 vs 0.91 for plain relative contact order, so the multiplicity-factorization *bridge* is withdrawn; `closedLoop_append` stands, but multiplicities do not factorize over contacts). So the fold census does **not** predict folding rates — do not restate that it does |
| `hydrocarbon_census.py` / `Chemistry.md` §10 | **"Degree of unsaturation" IS the closure count.** The formula students memorise, `DoU = (2C+2+N−H−X)/2`, is the **cycle rank** `b₁ = E − V + 1 = Σ(vᵢ−2)/2 + 1` of the molecular graph, so each element's coefficient is `(valence−2)/2` — and **oxygen is absent because its coefficient is zero**, a cancellation rather than a convention (`divalent_neutral`). Three corollaries: **a double bond and a ring are one phenomenon**, an independent closure, so `C₆H₁₂` is a single census class holding cyclohexane and every hexene; **saturated = zero closures**, so `CₙH₂ₙ₊₂` follows rather than being stipulated; and **valence 2 is the neutral element**, which is *why* a divalent monomer makes a chain (so every closure a polymer has is a contact — what `QLF_Folding` assumes). **And a reaction's change in closure count IS its change in molecule count** (`reaction_delta`) — a balanced reaction pins `V` and `E`, so `b₁ = E − V + k` leaves only `k` free, making organic chemistry's taxonomy one number: addition `Δ=−1`, elimination `+1`, substitution/condensation `0` (class fixes the sign, piece-count the magnitude). The **peptide bond** is in the neutral class, so a polypeptide backbone carries no closure of its own. Census: max degree 4 as the only rule reproduces the alkane series (A000602) through C₁₄; the merged class gives C₄H₈→5, C₅H₁₀→10, C₆H₁₂→25, each the textbook total. Lean: [`QLF_Unsaturation`](lean/QLF_Unsaturation.lean), no axioms. **Not** closed: *where* the closures sit (resonance, regiochemistry), and stereochemistry — a valence graph is mirror-symmetric, the same no-go as `Protein_Folding.md` §7 |
| `Spacetime_Constructor.md` | Full write-up of `spacetime_constructor.html`. Reframed thesis: **no forces, no fields, no action at a distance** — only ZFA closures that **DO** close (not "can"), because in quantum logic things happen **every way possible** and reality is what happens in the **most ways**; a closure's **frequency IS its multiplicity** (the census count of ways), read out as space/time/colour — never a cause. Generated *from nothing* by the first distinction unfolding the census, seen from one 3-D observer perspective, **enhanced** (not caused) by the background-radiation spectrum. Covers every panel: generation-from-nothing, the movable observer frame, band selector, foam Brownian walk, Pauli-bound crystals, black holes, QuCalc create, field readout, Vacuum ρ(T). Companion to `SpaceTime.md` (§7 is now just a live-see pointer) and the numerical `MultiParticle.py` |
| `proton_neutron_demo.py` / `SEX.md` | Model of the proton♂/neutron♀ pairing (issues #53/#57): `pn` binds where `pp`/`nn` are Pauli-blocked, the bond stabilizes the decaying neutron; complementarity → collective intelligence. Room best practices live in quantum-os `Room_Best_Practices.md` |
| `BraKetRhoQuCalc.md` | Reference doc for bra-ket ↔ RhoQuCalc correspondence |
| `Lagrangian_Formulation.md` | Variational formulation: ℒ=0 as origin, Σ₈ algebra, Zeno stationarity, decoherence impossibility; Lean theorem anchors for all claims |
| `ScientificApproach.md` | **The method, not the results** — how QLF decides what it knows: the ontological floor (generable ⟹ real, ZFA decides closure not existence; **an apparatus IS a closure inventory and an observer is only a perspective**, so no observer potency may enter a derivation; information physics primary), the **epistemic status labels** (proved / exact computational / numerical evidence / conjecture / phenomenological match / open bridge / rejected route / superseded), seven methodological rules (inventory before interpretation; no free fitted kernels; symmetry-locked agreement is not evidence; exact arithmetic before float; transient ≠ asymptotic law; name the failing *layer* — measure vs phase vs context geometry; kill condition stated first), the hypothesis lifecycle, the correction protocol, and the Born-weight investigation as a worked case study of mostly-failed candidates |
| `Philosophy.md` | Possibilist ontology; ZFA as sole fundamental axiom |
| `Mpemba.md` | **Anomalous relaxation as a closure census** — relaxation to equilibrium *is* closure, and its time *is* the maximum excursion (`closedAtHorizon_iff_maxExcursion_le`), so three things become decidable: a **no-go** (`relaxation_ge_distance` — if distance means the imbalance, relaxation is bounded below by it, so the effect is *impossible* for that measure), an **enabler** (`equal_length_unequal_relaxation` — at one length and equal imbalance, relaxation differs by a factor of `n`, so no scalar determines it), and a **translation** (`strong_mpemba` — the spectral `a_slow = 0` becomes sector emptiness `W_H(deep) = 0`). **The stance: the effect is real and preparation-specific, and that is why it is hard to duplicate** — instances are proven and unbounded (`mpemba_instance`), unbiased draws cross 13–17% of the time at a 2× energy ratio, while the blind test's *ensemble medians* are monotone with no crossing at all ([`mpemba_census.py`](mpemba_census.py)). An experiment that fixes temperature and lets preparation vary is averaging over a census whose depths span an order of magnitude, so **irreproducibility is the signature, not the refutation**. Still an ontology plus proven scaffolding and exhibited instances, **not** a quantitative derivation for water. Records the destination trap (unbalanced histories never close, so comparing time-to-fixpoint across imbalances compares different destinations — the substrate form of "what does *freezes first* mean"), laser cooling as engineered multiplicity bias with a trapped-ion ladder as the tractable test, and what would make it a result |
| `Law_Of_Exceptions.md` | **The Law of Exceptions, proven** — *there is an exception to every restrictive law except this law*. The aphorism is folklore (late-16th-c. base form) and self-reference proves nothing; the set version `A_L ⊊ H ⟹ ∃h∉A_L` is a tautology (bookkeeping by the method's rule 3). **Capacity earns the premise:** a restrictive law IS a finite closure (`closedAtHorizon R`), and *a system with more states can always break a finite closure* — for every `R` the fold `[+^{R+1}−^{R+1}]` is unadmitted at `R` yet **genuinely closes at `R+1`** (`law_of_exceptions`), the hierarchy is strictly increasing so no finite closure is final, and every exception is admitted at *some* capacity — so unbounded ZFA, which restricts nothing, is the unique exceptionless law. Laws look exceptionless because exceptions are the **least-multiplicity** histories (2 ways at max depth vs `2ⁿ` at depth 1). Not Gödel — the witnesses are *decidable terminating* closures, the ladder is capacity not consistency. Corollary: **construction proves possibility, not uniqueness** ([`lean/QLF_LawOfExceptions.lean`](lean/QLF_LawOfExceptions.lean)) |
| `Banach_Tarski_QLF.md` | Banach–Tarski (1924) as QLF's touchstone: impossible mathematics (AC's free duplication, excluded by the realizability filter); the precise *ex falso* reading (**ontological/model** explosion, **consistency ≠ realizability**, never "ZFC inconsistent"); and its *possible* twin **mitosis** — one cell pays (DNA copy + ATP + `ΔF=−log2`) for what Banach–Tarski steals. The "no free duplication" principle at four scales (no-cloning ↔ no-diproton ↔ no-free-mitosis ↔ no-Banach–Tarski), Lean-anchored in `QLF_NoFreeDuplication` |
| `Navier_Stokes_Geometry.md` | The geometry of Navier–Stokes — angular momentum = circulation (`baryonNumber` = Σ `signTriple`, the discrete curl; the `su(2)` Noether charge, a pseudovector under T); vorticity = the local discrete curl, **quantized to `±1`/cell** so it cannot diverge; **where QLF avoids the blow-up** (Beale–Kato–Majda vorticity-blow-up is unsatisfiable on the discrete geometry) and **the correction** (quantization/discreteness, the same cutoff as the UV/vacuum catastrophes). Lean: [`lean/QLF_AngularMomentum.lean`](lean/QLF_AngularMomentum.lean); the continuum-PDE limit stays the `QLF_NavierStokes` boundary |
| `Geometry_Of_Space.md` | The geometry of inner and outer space — one closure-resonance substrate. The Fuller geodesic icosa-blanket (machine-verified V/E/F, χ=2, 12 pentamons, McKay/E₈) at every scale; the 2-D screen ↔ 3-D bulk holography + the 1D→2D→3D dimension ladder; crystals as macroscopic resonant lattices; **prime frequencies = irreducible modes**; **higher frequencies dominate** (cosmic receiver the exception); the **half-spin prime-3 keystone** ("balanced and prime"). Lean anchor [`lean/QLF_PrimeResonance.lean`](lean/QLF_PrimeResonance.lean). Synthesizes `Primordial_Markov_Blankets.md` / `Crystal_QuantumOS.md` / `Prime_Topology_Stability.md` / `Consciousness.md` |
| `Consciousness.md` | A QLF model of consciousness — the frequency-hierarchy of resonant closures. Self-awareness = a self-modeling (finite, terminating) Markov blanket; conscious thought = the highest-frequency bound closure (binding raises frequency = gamma/global-workspace ignition); cosmic/meditative consciousness = quieting the internal closures to **receive** a low-frequency external **joint** closure (de Sitter horizon / collective). **Qualia hypothesis (§6):** qualia = self-awareness *coupled to* cosmic consciousness (the shared joint-closure ground) — neither alone; a two-factor dual-aspect stance, not a proof. Structural skeleton (architecture, not qualia) machine-verified ([`lean/QLF_Consciousness.lean`](lean/QLF_Consciousness.lean)). Synthesizes `TheQuantumBrain.md` / `TheBigProblem.md` / `Philosophy.md` §2 |
| `Category_Theory_QLF.md` | **The category-theoretic structure of QLF, collected** (issue #155). The base category = the causal-set poset (`Event = List α`, `reachable = <+:`, thin, `QLF_ReachableEvent`); histories under `++` = the **free monoid** (`Mathematics_From_QLF.md` Rung 2). **ZFA as a universal property** — count balance IS the **equalizer** of the signed-action hom and zero into `ℤ⁴` (Pauli closure entailed by `count_balanced_pauli_closed`); `full_zeno_prune` as a possible **coreflection** (open). **The bifibration** — the grading to `(ℕ,≤)` with cartesian (`--listening`, integrate out) and cocartesian (`Z_succ`, add a shell) lifts; **§3a its load-bearing consequence**: unique prime factorization → free monoid → `G = 1/(1−I)` → linear recurrence → self-similarity forced + the log-periodic channel closed by structure (why `w = 1/2` is structural). Plus the Tannakian/motivic/anabelian layer (`QLF_MotivicGalois`, `QLF_Anabelian` — proven functors + groups), RhoQuCalc as a **dagger SMC** internal language, `MO2` as the internal logic (`QLF_QuantumLogic`). **Binding: method rule 4 — CT is a description, no axiom, no count.** Open Lean targets: the coreflection, the bifibration formalized, `RhoProcess/≈` is a †-SMC, the general orthomodular representation theorem |
| `Mathematics_From_QLF.md` | How mathematics emerges from the substrate — the emergence ladder (ℕ from counting closures; `+`/`×` = parallel/sequence composition; the unit group `μ₄=(ℤ[i])ˣ`; su(2)/su(3); the continuum as completion), the bootstrapping resolution (substrate generates, Mathlib renders, conservativity ⟹ not circular), how QLF is distinct from reverse mathematics (generative + active-inference selection + ontological commitment, vs RM's descriptive/neutral stratification), whether the resolution applies to the metalanguage (reflexively yes — verification is itself a ZFA closure — with the Gödel-II residue relocated to the finite-computation floor), and **why mathematics is so effective in physics (Wigner dissolved: effective math = realizable math = the substrate; effectiveness tracks realizability, which also explains where it fails)** |
| `Game_Theory_QLF.md` · `evolutionary_census.py` · `game_log_analysis.py` · `lean/QLF_PotentialGames.lean` · `lean/QLF_EvolutionaryGames.lean` · `lean/QLF_NPlayerPotential.lean` | **Game theory from QLF — potential games generated, all games solved** (Rung 10 of `Mathematics_From_QLF.md`; quantum-os #209). Five theorems: free-action functional ⟺ potential game; ways = basin, closure frequency is multiplicity (finite KMR/Young); descent terminates + every finite potential game has a pure Nash equilibrium; basis choice iff `1 + a > 2b`; Fisher's 1:1 as an ESS. The story: Three pre-registered no-gos, one theorem and one positive result. Payoffs *derived* from closure counts are always potential games — no Stag Hunt, no Prisoner's Dilemma (`common_interest_potential`: a closure is a shared event); the census's own first-closure race yields complementarity (best reply = conjugate, `u=1`; same strand worst), a 1:1 polymorphism, and spontaneous axis symmetry-breaking. With the game as **input** (regret = free action, so **Nash = ZFA closure**, `nash_iff_closure`), relaxation finds the **risk-dominant** convention every time and the payoff-dominant one never (`risk_dominance_is_potential_order`); to maximise welfare, **make the closure joint** — pay everyone the total, a potential game with potential `W` (`welfare_game_potential`; measured 0 % → 100 %). Headline theorem: **a game has a free-action functional iff it is a potential game** (`free_action_iff_four_cycle`); matching pennies is outside. The substrate generates potential games and solves all games. For the room: score by the shared objective, not private gain; the conservative-convention problem is fixed by the objective, not the temperature |
| `fredkin_qlf.py` / `Fredkin_QLF.md` | **Fredkin's conservative logic on the substrate.** Fredkin & Toffoli (1982): the gate is a controlled swap, self-inverse and *conservative* (outputs are a permutation of inputs). In QLF that conservation law **is** ZFA count balance — a gate permutes lines, a permutation preserves the twist multiset, so the signed action vector is unchanged and by `count_balanced_pauli_closed` full ZFA carries over, both conjuncts. Ball = `^<v>` (the minimal closed plaquette; **168** of 4096 length-4 histories close, so the count is the content, not the witness); vacuum = the empty history. Helium is the billiard ball *because* `Chemistry.md` valence 0 ⟹ no shared closure ⟹ no bond ⟹ elastic only; C₆₀ for the same cage reason. Verified over full truth tables: conservativity, involutivity, the BBM interaction gate, NOT/AND/OR/FANOUT, and a Fredkin-only full adder (19 gates, 29 ancillas). **Binding framing:** an instantaneous zero-free-action closure is **free** — `ΔF = −log 2` receipts a *many-to-one* closure and a bijection has none, so the reversible core costs 0 and the bill is exactly the garbage you decline to keep (29 bits). Landauer/Bennett derived, not assumed |
| `Reversibility.md` | Time-reversal = the Hermitian conjugate (`eval_dagger`); a balanced closure is `H=H†` (self-time-reverse, no per-event arrow); the arrow is forward *sequencing* in synthesized time (`f=1/t`), reversal = "go back in time" with no meta-axis; the `H↔H†` involution = the critical line (Hilbert–Pólya). Reversible *logic*, irreversible *process* |
| `Open_Problems.md` | Gap registry: closed / principled-boundary / open items, each with its owning doc. Update here + owning doc when a status changes |
| `census_inventory.py` / `data/census_inventory.json` | **The inventory database — counts, listenings and QuCalc folds, accumulated.** What enumeration actually discovers: how many ways close (graded by length and closure depth) and which Pauli phase each way carries. **It accumulates** — each run keeps what is stored and computes only what is missing, so the record is fleshed out over time by pushing one length deeper (`--twist-len 8`, `--phase-len 20`; the fold census is `8^L`, the depth census `2^L`, so those set the practical ceilings). And it is a **checker**: every proven invariant is asserted against freshly enumerated data, so a change to `twist_core.py` that breaks one is caught — count balance ⟹ Pauli closure; count balance ⟹ the fold is `±I` never `±iI`; unbalanced histories *do* reach `±iI`; closure depth = max phase excursion; one-pass closures number `2ⁿ`; the deepest stratum holds exactly `2`. Also records which strata counts are Gaussian norms — mostly not: **counts are not weights**. Its other verified-not-proven finding, the phase rule `(−1)^{#neg}·sign(axis permutation)`, is now **proven** (`QLF_PhaseRule`), so the enumeration is its discovery record and a regression check, not its warrant. **Now carries a `closures` layer** — the one contextual section of an otherwise universal file: for a small fixed set of canonical geometries, the first-closure event classes with `(W, A)` (how many ways close as that outcome *first* at that depth, and their signed total), from which the multiplicity mass `Σ W/8^d`, the normalized-event weight `Σ A²/(W·8^d)` and both splits follow without re-enumerating. Three further invariants come with it, Lean-anchored to [`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean): the cylinder mass stays `≤ 1` (`twist_kraft`), `|A| ≤ W`, and the normalized weight stays under the mass (`normalized_event_mass_le_one`) — **11 proven invariants asserted, up from 8** |
| `qucalc_search.py` / [`QucalcSearch.md`](QucalcSearch.md) | **The "what closes next" query — Python reference + CLI.** From a QuCalc position `qc`, enumerate the admissible **continuations** (twist words to append so the whole history is a ZFA closure), shortest first. **Not a deployed dependency** — quantum-os computes the same `/search` + `/solve` client-side in the browser (quantum-os#119); `--serve` here is optional local/research HTTP, and `QucalcSearch.md`'s contract is the spec the TS port pins. **Framing (binding):** **search is the experiment** — it asks the substrate which a-priori possibilities close from a position and lays the space out (concurrent search + shared listeners = several *perspectives* on one closure inventory; no observer potency, `ScientificApproach.md` §2). **`/solve` is the truth divination** — truth is what closes, and of the ways a position closes the substrate takes *one* (least free action = the most-ways closure); the deterministic cascade makes it a reading every caller shares, not an opinion. **In quantum-os `/solve` is the meeting of minds** — run on a room's joint position (peers' `/qlf-action` proposals concatenated), every peer computes the same closure, so the room reaches consensus *the substrate dictated, not negotiated* (joiner-local like `/poll`; `QLF_as_Intelligence.md` §8). A *query*, not a stored layer: nothing cached or written, always current with `twist_core.py` (contrast `census_inventory.py` = committed per-stratum summaries + Lean-invariant checker). Cheap by construction — the seed's action vector fixes what every continuation must supply, so candidates are count-prefiltered before any Pauli fold, and by `count_balanced_pauli_closed` the survivors are all closed so the fold only reads off the phase. **Optional local HTTP** (`--serve [--host 0.0.0.0] [--port] [--max-depth-cap N] [--max-concurrent N]`): `GET /search?qc=&max_depth=&limit=&mode=&listeners=&stream=` → streamed `application/x-ndjson` (`_meta` first line, one closure per line `{cont,history,len,depth,phase}`, `_done` trailer with `listeners`/`per_seed`), CORS-open, read-only, stateless, `429` at the concurrency cap. **`mode=events`** = absorbing (stop each branch at its first closure — the possibilities/events split, ties to `contextual_census.py --first-closure`); default is all **possibilities**. **`listeners=phase,depth,capacity:R,head:N`** = one enumeration, several rollups (`capacity:R` is the QLF listening); `stream=0` returns only the rollup. **`qc` comma-separated** = concurrent search over several seeds, listeners aggregate. **`GET /solve?qc=&max_depth=`** = the complement: one JSON answer, *the* closure the substrate takes (cascade: least peak excursion → shortest → phase `+1` → lexicographic — deterministic so callers agree; least excursion *is* least free action = the most-ways closure), or `{solved:false, residual, completion}`; comma-sep `qc` is *concatenated* (not separate seeds). Stable contract (`version`, additive routes stay `1.0`). No SSD / no precompute — see `QucalcSearch.md`. Depth ceiling: 6 on a constrained host (~3 s), 7 on a real one (~1–2 s, where "~10 K possibilities" lands); hard cap 7. Gotcha for the TS port: gate on `signedAction·every(0) ∧ isPauliClosed`, *not* the weaker aggregate `achievesZfa`. quantum-os client-side impl: quantum-os#119 (#117 closed) |
| `contextual_census.py` | **The experiment layer to the inventory's substrate layer** — the contextual census, built as a falsification test for the Born question ([`Born_Rule.md`](Born_Rule.md) §8). Amplitudes come from the *proven* phase rule, never a matrix; a preparation is an **open** strand; apparatus and preparation are specified independently; every geometry runs at increasing horizons and is printed blind. Modes: `--depth-scan` (the raw wash-out), `--listening R` (capacity-relative closure: capacity sets the *rate* of forgetting, never the limit, and direction is erased), `--spectrum R` (the transfer operator behind that), `--first-closure R` (the **absorbing** census — a closure *is* an event, so the run chooses its own stopping depth; restores direction, and the cylinder measure `8^{−d}` is forced by prefix-freeness), `--two-path R` (the four-run interference test that found the sub-additivity no-go), `--coherent R` (the **unnormalized** amplitude, exact rationals — summable for those preparation–apparatus pairs whose signed census grows below the forced `√8^d` threshold, where interference works in both directions). **Exact integers throughout** — the float scan is contaminated past `k* ≈ 16 ln 10 / ln(λ₁/λ₂)`, where roundoff makes every preparation appear to share one limit |
| `Perturbation_Theory_QLF.md` | **Perturbation theory = the possibility-tree expansion; renormalization = the capacity horizon.** The QFT perturbation series *is* the phase-weighted sum over ZFA-closed histories ([`Born_Rule.md`](Born_Rule.md) §2), graded by closure structure — continuation length / diagram order (`IsDiagram`, [`QLF_FractalDiagram`](lean/QLF_FractalDiagram.lean)) / closure depth — not by an external coupling. [`qucalc_search.py`](qucalc_search.py) computes it order-by-order from a seed position; `--events` = leading skeleton, `--listeners capacity:R` = the RG-scale-restricted sum, `--solve` = the scheme-free physical point. **Renormalization is Wilsonian and finite:** the `R`-listening is the regularized amplitude, `A_{R+1} − A_R` the (finite integer) counterterm, `Q(R)=Q₀·2^R` the running (QED log = census octave count, β = per-octave flux, [`QLF_VacuumPolarizationTower`](lean/QLF_VacuumPolarizationTower.lean) `perOctave_is_flux`). **The series converges absolutely** in its cylinder measure — `twist_kraft` (`Σ 8^{−\|h\|} ≤ 1`, [`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)) + `\|A_L\| ≤ W_L` — so no Borel resummation; the Dyson divergence is a continuum artefact. Demonstrated with real registry data (bare `\|A_L\|` grows `8→120→2144`, cylinder-weighted decays `0.125→0.029→0.008`). No axiom. Open: higher-loop coefficients + the depth-≥3 `𝒵` tail, gated on frontier #1 |
| `self_similar_closures.py` | **Self-similar ZFA closures, exhibited and counted** (`Philosophy.md` §3a). A *self-similar closure* is a prefix of the fixed point of a balanced length-doubling substitution `σ` that is a ZFA closure at every `σ^k(a)` — its left half is `σ^{k-1}(a)`, the identical structure. Canonical: the **Thue-Morse closure** `+--+-++-` (`σ(+)=+−`, `σ(−)=−+`), self-similar at the string level *and* the prime-factorization level (its prime word over `{+−,−+}` is itself Thue-Morse — the free-monoid/bifibration self-similarity of [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md) §3). One per conjugate pair (`^vv^v^^v`, `><<><>><`, `/\\/\//\`, `+--+-++-`); **80** single-pair families from length-2 blocks (64 aperiodic), multi-axis products add dozens, block length `2m` gives `C(2m,m)²` per pair → unbounded. All at `max_excursion = 1` — heard at every horizon, the concrete form of *self-similar things dominate existence* |
| `Closure_Walk.md` · `closure_walk.py` · `doob_bridge.py` · `data/closure_walk.json` · `data/doob_bridge.json` | **ZFA closure IS a closed walk on `ℤ⁴`** — the eight twists are `±e_a`, count balance is *back at the origin*, a capacity-`R` horizon is the `ℓ¹` ball. Four results, exact to `L = 1000` and checked against every closure to `L = 8`: (1) **selection has teeth only because `d ≥ 3`** — **Lean: [`QLF_PolyaTransience`](lean/QLF_PolyaTransience.lean)**, `polya_transience`: the `ℤ⁴` walk is transient by elementary bounds (`W_L(L+1)(L+2) ≤ 4·8^L`, so `Σ u ≤ 4` and any first-return mass is `≤ 3/4`); the twist-history ↔ `walkCount` bridge is **[`QLF_ProductWalk`](lean/QLF_ProductWalk.lean)** (`card_balanced_twist`), and the Dyson bijection is **[`QLF_FirstReturn`](lean/QLF_FirstReturn.lean)** (`at_least_quarter_never_closes`, closing issue #157); Pólya: the walk is recurrent in `d ≤ 2` (a two-axis alphabet would prune nothing of measure) and transient in `d = 4`, where the fraction of possibility that *ever* closes is `p₄ = 0.19320`, measured as the prime Kraft mass `Σ_π 8^{−|π|} = 0.1932015` — **80.7 % of possibility never closes**; (2) closure lives on the 5-dim state `(x, t)`: `h(x,t)` = ways to close, `/solve` = argmax, sampler = ratio, drift `−4x/t`; (3) **the half-spin phase is a ℤ₂ connection on the walk's Cayley graph** — edge `x → x+s·e_a` carries `s·(−1)^{Σ_{b>a spatial} x_b}`, phase = holonomy, π flux through every mixed spatial plaquette (`^>v< = −1`, `^>v<^>v< = +1`), 0 mismatches on 195,416 closures; **Lean: [`QLF_EdgeSign`](lean/QLF_EdgeSign.lean)** — `holonomy_eq_invCount` / `connectionPhase_eq_predictedPhase` for every history, `fold_eq_connectionPhase` on balanced ones, plaquette fluxes decided, no axioms; **balance ≠ spin** — the walk is the unsigned classical census, the signed sum is the quantum content; (4) `W_L = (8/π²)8^L/L²(1+O(1/L))`, returns bounded at `≈1.48`. §3 is the **graph spec** (nodes `(x ∈ ℤ⁴, σ ∈ ℤ₂)`, 8 signed vector edges, finite at any `R`), **built and rendered** by `closure_graph.py` → `closure_graph.html` ([live](https://rchain-community.github.io/quantum-logical-framework/closure_graph.html)): at `R=3` 129 nodes / 528 edges / 168 plaquettes (84 with π flux), and walking the signed graph reproduces the signed census `−8, 120, −2144` exactly. `doob_bridge.py`: exact uniform sampler over closures (telescopes to `1/W_L`) and over primes (taboo count, `1/I_L`). Corrects `intermittency_bridge.py`'s `M(∞)` (an `L ≤ 22` partial sum). Grew out of a compression question — a closure is incompressible to leading order, which is result (4) read as a rate; that framing was dropped |
| `alpha_residual_bridge.py` | **The `Alpha_Residual.md` §9a pre-registered R0 test, executed** (`Alpha_Residual.md` §9b). Value-free (`137.036` / `0.036` never enter). Two census layers — the abstract 1-D walk (`C(2n,n)` / `2·Catalan(n−1)`, `G = 1/(1−I)` verified) and the **real 8-twist first-closure census** from [`qucalc_search`](qucalc_search.py) (primes `8, 104, 2944, 108136, 4525888` at length ≤ 10) — built into a [`QLF_ExactRG`](lean/QLF_ExactRG.lean) `ClosureSpectrum` (Kraft weight `8^{−L}`, graded by max-excursion), recursion run (`Z` monotone/bounded, `amp` converges). **Three-part verdict:** the **`2/(3π)` coefficient SURVIVES** — `census_split → 1/6` for the prime (1PI) census too, so it is 1PI-legitimate; the **leading `log` is NOT in the census mass** — the Kraft sum is bounded so its per-octave increment decays, the log is carried by the scale↔octave map (`flux_scale_invariant`); the **higher-order tail is the continuum running**, not a census-truncation rule. **The healed framing** (`Alpha_Residual.md` §9b–§9c, `Alpha.md`): the bracket is two-sided/proved, `w = ½ → 137.032` is **structural** (bifibration ⇒ no log-periodic line ⇒ no shift), `0.036` is **existence-proven** with its **multiplicity open** = the continuum vacuum-polarisation running (the SM's frontier). CODATA is an estimate of the missing count, not a target. Fractal/Zipf/bifurcation probe **null** (consistent with `genesis.py`). `--max-len 8` ≈ 30 s, `10` ≈ 5 min |
| `intermittency_bridge.py` | **The pre-registered R0 test of the turbulence/intermittency swing for the α residual `δw`** (`Alpha_Residual.md` §9c — the commit adding this file is the R0 freezing point). Value-free (`137.036` / `0.036` / `w=0.624` never enter). Tests the **one** closure the substrate selects per octave via the handedness listener–listener interaction (`/solve`), not the full census. **Leg 1 — `C₀`: PASS, a derivation** — `/solve` is axis-minimal (single-axis seeds close single-axis, verified across 21 seeds), so the vacuum's selected structure is 1-D and `C₀ = 3−1 = 2` — She–Léveque's codimension, now *derived from `/solve`* not posited from vortex-filament geometry. **Leg 1b — listener–listener: PASS** — joint `/solve` of two seeds collapses to one low-codim solution, not the union. **Leg 2 — `μ`: NEGATIVE (converged).** An **exact transfer recursion** (state `(v,h,d,l,inv,maxexc)`, no numpy — reproduces the brute counts) pushes the first-closure census to convergence (`M(∞) = 0.18267`, `R = 11`); the per-octave Kraft-flux multiplier `W(R) = ΔM(R)/ΔM(R−1)` peaks near `R = 4` then **decays monotonically toward 0** — **no inertial range** in the vacuum census, so no `μ` to extract (converged, not depth-limited). Leg 2 as posed on the vacuum fails. Net: **half-standing** — `C₀` derived + selection mechanism confirmed; `δw`/`+0.036` NOT delivered |
| `intermittency_seeded.py` | **Leg 2 re-posed on a SEEDED census (an injection scale), taken to the end of the path** (`Alpha_Residual.md` §9c). Seeds the transfer recursion from a preparation strand for `R_inj ∈ {0,2,4,6,8}` + cross-axis; three readings (seeded first-closure `W(R)`, first-passage sub-cascade ratios, steady-state stationary distribution). **All negative: no inertial range at any injection scale.** Seeding shifts the `W(R)` peak to `R_inj+1` and adds a spike, then `W(R)` decays exactly as the vacuum; the steady state concentrates at the boundary. The Kraft-weighted closure-flux leaks (`twist_kraft`) and piles at the floor — not a conserved cascading quantity. **Leg 2 is definitively dead**; the turbulence swing delivered only the `C₀` side-derivation. Honest landing: `w = 1/2` structural, `α⁻¹ = 137.032` the pure-ZFA prediction, the last `~0.004` = the continuum running |
| `Mysteries_Of_Physics.md` | Physics-facing survey of the canonical open questions (quantum foundations, spacetime/gravity, cosmology, the Standard Model, the deep/meta questions) and what QLF says about each — addressed/structural, value-open, principled boundary, predicted-absent (falsifiable nulls), or genuinely open. The reader's-eye companion to `Open_Problems.md` (which is status-organized) |
| `QuantumOS.md` | QLF as capability-secure OS kernel for QPUs |
| `FlowChart.md` · `FlowChart.html` | **Both are GENERATED** — do not edit either. The source is [`tools/flowchart_source.md`](tools/flowchart_source.md) (the Mermaid original); `python3 tools/build_flowchart_html.py` emits the clickable HTML *and* the Mermaid-stripped `.md` index. Two side files are **per-block arrays indexed by section order** (0 = master map, 1..N = domains) and must be extended when a domain is added: `tools/flowchart_clickmaps.json` (node id → doc, makes boxes clickable) and `tools/flowchart_edge_labels.json` (`per_block_edges` restoring connector labels, plus `master_domain_verbs`). **Check for drift before rebuilding:** the checked-in `FlowChart.md` has been hand-edited ahead of its source before, and a rebuild silently discards that — simulate the build (strip ```mermaid blocks from the source, diff against `FlowChart.md`), port anything the live file has back into the source, and only then run the builder. The taxonomy line (*one substrate → N families → M domains*) is **copy-pasted into `README.md`, `Introducing_QLF.md` and `UniversalRelativity.md`** as well as the source and the builder's intro string — update all five or it goes stale |
| `.github/workflows/` | CI configuration |
