# Reversibility in QLF — the reverse *is* the Hermitian conjugate

> **Worked case:** Fredkin's conservative-logic computer, built on the substrate — §7 and
> [`Fredkin_QLF.md`](Fredkin_QLF.md).

In the [Quantum Logical Framework (QLF)](README.md), **time-reversal is the Hermitian conjugate** (the
dagger `†`), and this resolves the old tension between *reversible microscopic laws* and the *forward
arrow of time* — not by a new postulate, but because the two live in different places: reversibility in
the **timeless closure algebra**, the arrow in the **forward synthesis** of closures into the time they
make themselves.

---

## 1. The reverse is the Hermitian conjugate

Machine-verified: the dagger of a process is the conjugate-transpose of its operator,

$$\texttt{eval}(\texttt{dagger}\;p) \;=\; (\texttt{eval}\;p)^{\dagger}$$

(Lean: `eval_dagger`.)

The Hermitian conjugate is *complex-conjugate* **and** *reverse-order* — which is exactly quantum
mechanics' antiunitary time-reversal `T = K · (order reversal)`. QLF says it literally at the twist level:
the antiparticle / time-reverse map is

$$\texttt{antiparticle}(ts) \;=\; (ts.\texttt{map}\;\texttt{conj}).\texttt{reverse} \qquad(\text{conjugate each, reverse the sequence}),$$

and across a *sequence* of closures the dagger reverses the order, `(A B C …)† = … C† B† A†`
(`dagger_sequence_reversal`). It is an **involution** — `antiparticle (antiparticle ts) = ts`
(`antiparticle_involutive`), so `T² = 1`: reversible in principle. (Charge conjugation is the same move
viewed spatially — `C_eq_motional_reversal`, `QLF_Spin`.)

## 2. A physical closure is its own time-reverse (`H = H†`)

Every QLF string maps to a Hermitian spectral mode (`toSpectralMode_hermitian`), and **ZFA balance ⟺
symmetric ⟺ the mode is scalar × identity** — self-adjoint (`spectral_symmetric_eq_scalar_id`). So:

> **A physical (ZFA-balanced) closure equals its own Hermitian conjugate, `H = H†`.** It is a *fixed
> point* of time-reversal. **No arrow lives inside a single closure.**

The bra is the dagger of the ket, `⟨ψ| = |ψ⟩†` — a balanced state is consistent with its own time-reverse
(`bra_ket_always_balanced`, `BraKetRhoQuCalc`).

**Reversibility *is* closure — a theorem.** Stronger than "consistent with": *every* open strand closes when
joined to its own dagger. **`dagger_closes`** ([`QLF_QuantumTurbulence`](lean/QLF_QuantumTurbulence.lean)) proves
`ts ++ dagger ts` is count-balanced — a ZFA closure — because the Hermitian conjugation swaps each pair
(`^↔v`, `<↔>`, `/↔\`, `+↔−`, `conj_involutive`) and `reverse` preserves counts, so every conjugate pair
balances (`count x (ts ++ dagger ts) = count x ts + count (conj x) ts`, `count_map_conj`). And the resulting
loop folds to a **real** scalar — fermion `−I` or boson `+I`, never the open-strand quarter-turn `±i`
(**`dagger_closure_folds_real`**, via `balanced_closure_folds_real`). So the `H↔H†` involution is not just a
symmetry of the laws: forward strand + time-reverse *always* achieves ZFA — reversibility realized as closure.

## 3. The arrow is in the *sequencing*, not the laws

If each closure is `H = H†` (no per-event arrow) and the dagger is an involution (reversible), where does
the arrow come from? From the **forward sequencing**. The dagger reverses the *whole product*
(`… C† B† A†`); to apply that reversal as a *process* is to run the history backward — i.e. **to go back
in time**. And in QLF there is **no "back" to go to**, because time is *synthesized by closure*:

$$f = 1/t \qquad(\text{each ZFA event makes its own local time}; \texttt{ZFAEventDynamics}).$$

There is no external time axis in which to perform the reversal: you would have to *un-synthesize the very
time the reversal would run in*. The reverse exists as an **operation on the timeless algebra** (the
dagger); it has **nowhere to run as a process**.

> The laws are time-reversal symmetric (the dagger involution, `H = H†` states). The arrow is the
> condition of being a closure *embedded in its own synthesized time* — not a property of the laws, and
> not a fine-tuned past condition. The observer does not *see* an arrow; the observer *is* the forward
> closure process.

## 4. Two layers of irreversibility — one event

There are two independent reasons you cannot go back, and **the same closure event creates both**:

1. **No meta-time** — each closure synthesizes one tick of local time (`f = 1/t`). Reversing needs an
   outside clock; there is none.
2. **The closure is many-to-one** — it coarse-grains `C(2n,n)` admissible histories into one outcome
   (`disjunct_count_eq_central_binomial`, `QLF_InfoSynthesis`), synthesizing exactly one bit
   `ΔF = −log 2` (`zfa_closure_minimizes_free_energy`, `QLF_FreeEnergy`). Even *with* a meta-time you could
   not uniquely retrodict which history fired — the past is recoverable only up to the closure
   equivalence class.

These are not two phenomena. **Each ZFA closure simultaneously *makes* a tick of time and *discards* the
which-history.** Time and irreversibility are born in the same event — which is exactly why "to be
reversible you would need to go back in time": the time *and* the loss are the same closure, so undoing
the loss means undoing the time, and there is nothing to undo it in.

## 5. Possibility is symmetric; the reachable walk is one-way

§4 located the arrow at the **count** level — forward closure is many-to-one. There is a second,
independent anchor at the **order** level, and it is the same arrow seen structurally: realization is a
*directed walk* through possibility space. Three tiers ([`Evolution.md`](Evolution.md) §3):

- **generated** — all possibility (`expand_generation`, `4ⁿ`);
- **closing** — the ZFA-balanced subset (`C(2n,n)`), the **timeless algebra where the dagger involution
  of §1–§2 lives** — symmetric, no forward/backward;
- **reached** — actual: the closures in *this* history's future cone (`futureCone_subset`).

The reachability relation `reachable A B := A <+: B` (one closure is a *prefix-extension* of another,
[`QLF_ReachableEvent`](lean/QLF_ReachableEvent.lean)) is a **partial order** — reflexive, transitive, and
**antisymmetric** (`reachable_antisymm`). Antisymmetry *is* the no-going-back at the order level: if `A`
reaches `B` and `B` reaches `A` then `A = B`, so the walk never returns to a strictly earlier closure. So
the reversible-logic / irreversible-process split of §3 restates order-theoretically:

> **Tier 2 (possibility) is reversible** — the full ZFA space carries the order-2 `H ↔ H†` involution,
> nothing in it distinguishes forward from backward. **Tier 3 (realization) is a monotone climb** — the
> actual history extends forward in the reachability order and *only* forward (`reachable_antisymm`); the
> passage from tier 2 into tier 3 is one-way.

This is a *distinct* structural anchor from §4's non-injectivity: **non-injectivity (count)** says you
cannot retrodict *which* history closed; **antisymmetry (order)** says you cannot un-reach the closures
you have climbed through. Neither is a fine-tuned past condition — both are properties of the closure
walk itself. (The [`Evolution.md`](Evolution.md) §3 reading — a *possible* niche left unfilled because it
is unreachable from where the actual history stands — is exactly this tier-2-vs-tier-3 gap in the
biological register: the closure exists in symmetric tier-2 possibility, but the one-way tier-3 walk never
climbs to it.)

## 6. The payoff — time-reversal symmetry **is** the critical line

The `H ↔ H†` involution of §1–§2 is the *same* involution behind QLF's
[Riemann program](README.md): its fixed points are the Hermitian (real-eigenvalue) closures, which is the
Hilbert–Pólya / critical-line condition (`spectral_hilbert_polya`, `QLF_Riemann`), and the *same*
`functional_equation_fixed_real` reflection reused by Birch–Swinnerton-Dyer and Hodge
(`bsd_riemann_shared_involution`). So

$$\boxed{\;\text{time-reversal symmetric } (H = H^{\dagger}) \;\;\Longleftrightarrow\;\; \text{real spectrum} \;\;\Longleftrightarrow\;\; \text{on the critical line.}\;}$$

Physical reality is selected as the **self-adjoint = time-reversal-fixed** subset of possibility, and that
selection is the same `H ↔ H†` whose fixed line carries the Riemann zeros. Time-reversal symmetry, the
reality of energies, and the critical line are **one** involution.

## 6a. Why π is already in it — Poisson self-duality  *[structural reading]*

§6 puts the critical line at the fixed axis of `H ↔ H†`. On the continuum side that same axis is the
fixed line of ζ's functional equation `s ↔ 1 − s`, and **π sits in that functional equation for exactly
the reason the involution exists** — not as an extra constant to be explained.

The completed zeta function carries the factor `π^{−s/2} Γ(s/2)`, the Mellin transform of the Gaussian
`e^{−πx}`. The Gaussian is there because `e^{−πx²}` is the **fixed point of the Fourier transform**
(`∫ e^{−πx²} e^{−2πixξ} dx = e^{−πξ²}`), and Poisson summation — *lattice sum = dual-lattice sum* — turns
that fixed-point property into the Jacobi theta identity `θ(1/t) = √t · θ(t)`, hence into ζ's `s ↔ 1 − s`.
Every explicit constant downstream inherits the π: the zero-counting density `N(T) ∼ (T/2π) log(T/2π)`,
and through it the RH-conditional error bounds (Schoenfeld's `√x log x / 8π`).

So the picture is symmetric across the discrete/continuum seam:

| | discrete side | continuum side |
|---|---|---|
| the self-duality | `H ↔ H†` involution (`eval_dagger`, §1) | Fourier: `e^{−πx²}` is its own transform |
| the bridge | twist-history ↔ spectral mode (`toSpectralMode_hermitian`) | Poisson summation (lattice ↔ dual lattice) |
| the fixed set | `H = H†` closures (`spectral_symmetric_eq_scalar_id`) | `Re(s) = 1/2`, fixed axis of `s ↔ 1 − s` |

Poisson summation is the cleanest statement of QLF's "the continuum is a rendering": the lattice sum and
the continuum integral carry the **same information**, so π — the continuum constant it produces — is
realizable, a forward limit of the census counts (`censusTail_eq`, the Wallis/Catalan family), not an
independent transcendental input. The *constant* π is thus not the lever on RH — it is already available
in `RCA₀`, and ζ's functional equation with it. The *census that produces* π is: the discrete count layer
where the reformulation operates (`resonant_computation_for`, the MRE-saturation program), and refining it
is the open constructive direction. The zero **location** stays the `spectral_hilbert_polya` boundary, and
RH-conditional analytic machinery (Schoenfeld's `√x log x / 8π`, the value of Mills' constant it pins down)
sits *downstream* of that boundary.

**Falsifiability (method rule 4).** This is a structural identification — the π that appears and the `1/2`
QLF derives structurally are the same self-duality seen from two sides. It changes no count of ways, so it
is framing-clarifying bookkeeping, not a new prediction; labelled accordingly.

## 7. Are reversible theories wrong? — *half-right*

Not wholesale. Reversibility is a **real** symmetry of the QLF laws (the dagger; every closure `H = H†`),
so a reversible theory has the **law-level algebra right**. It goes wrong only when it treats that as the
*whole* universe. A theory that says the universe is reversible **full stop** — no genuine arrow, no real
measurement, no irreversible synthesis — omits the **closure**, and the closure is where time,
definiteness, and information come from, and it is irreversible (§3–§4).

The tell: any purely-reversible theory must still *explain* the arrow of time, the second law, and
measurement — and can only do so by **smuggling in a non-reversible ingredient**:

- a fine-tuned low-entropy **past boundary condition** (the "Past Hypothesis"),
- a separate **collapse postulate**, or
- coarse-graining **by ignorance** ("we just don't track the microstate").

QLF needs none of these crutches — the closure **is** the arrow, constructively (`full_zeno_prune` +
`disjunctive_closure` + `ΔF = −log 2`).

**The worked case: Fredkin's machine** ([`Fredkin_QLF.md`](Fredkin_QLF.md)). Conservative logic is the
half-right theory built out on the substrate, and building it makes the line above concrete rather than
programmatic. Fredkin & Toffoli's gate is a controlled swap — its own inverse, and *conservative*, its
outputs a permutation of its inputs. Encode a ball as one closed plaquette and a register as the
concatenation of its lines and the gate acts on the history **by permutation**
(`encode_fredkin_perm`), so the twist multiset never moves and the history stays realized:
`fredkin_preserves_zfa`, machine-verified with no QLF axiom. **Fredkin's conservation law and ZFA
count balance are the same law**, which is why his half was right.

What the machine then shows is exactly where the other half goes:

- **The reversible core is free.** `fredkin_bijective` — the gate maps its state space onto itself
  one-to-one, so no two histories merge, nothing becomes unrecoverable, and there is no many-to-one
  closure to receipt. An **instantaneous zero-free-action closure costs nothing**. Run a full adder,
  19 gates, and the ledger stays at zero.
- **The bill is the forgetting, and only that.** Resetting `k` garbage lines is a `2^k → 1` map, and
  *there* the `ΔF = −log 2` quantum is charged, `k` times over.

So Landauer (1961) and Bennett (1973) come **out** of the single closure quantum rather than being
assumed beside it: erasure costs, computation does not, and the boundary between them is whether the
closure is many-to-one — §4's distinction, priced. A reversible theory is not wrong about its own
half; it simply never reaches the step where anything is paid for. Fredkin's machine is the case
where the logic stays reversible all the way to the end and the process never has to commit — and you
can watch it, [`fredkin_machine.html`](fredkin_machine.html) runs the adder backwards to the input it
started from.

So reversible theories are not *false*; they are **incomplete** —
the timeless half (the possibility space, the dagger) without the rendering half (the forward, lossy
closure in synthesized time).

Casualties of the *strong* reversibility claim:

- **Purely-unitary / "no collapse" (Everett):** the unitary algebra is the possibility space, but the
  closure (the OR firing into *one relative world per observer*) is real and irreversible — **many
  observers, not many worlds** (Smolin). Denying the closure is the error.
- **Block universe / eternalism:** the future is not laid out and re-runnable; it is *un-rendered
  possibility*, and "now" is the closure edge. Time is synthesized (`f = 1/t`), not a dimension you can
  drive backward.
- **Deterministic reversible-CA underpinnings** ('t Hooft): a reversible cellular automaton has no genuine
  measurement or arrow; QLF's substrate *selects and prunes* irreversibly — it is not a reversible CA.

And it is the right physics, sharply: QLF's `ΔF = −log 2` per closure **is Landauer's `k_B T ln 2`** — the
irreversible cost of fixing one bit. Reversible *unitary* evolution (the dagger) is real; the moment a
closure yields a *definite* outcome, that step is irreversible — exactly the reversible-gates /
irreversible-measurement split of real quantum computing. "Everything can be reversible computation" is the
claim QLF denies: you can *postpone* the bit, but to **have** a definite world you must close, and closing
costs `log 2` and one tick of time.

And that "one bit" is now a theorem, not a figure of speech — which sharpens the reversible/irreversible
split into *one object seen twice*. The bit a closure fixes is the two-valued **spin-½**: it carries
exactly `log 2` (`binary_kl 1 (1/2) = log 2`) where a *single-valued* object carries none
(`binary_kl 1 1 = 0`), and its `2π` double-valuedness — the very `−I ≠ +I` of the Hermitian-pair fold of
§1 (`hermitian_pair_folds_to_negI`) — is reproven from the explicit rotation matrices
(`spinor_double_valued_vector_blind`), grounding the spinor **Cartan** discovered in 1913
([`lean/QLF_SpinorInformation.lean`](lean/QLF_SpinorInformation.lean)). So the **reversible face** is the
dagger involution on that spinor (`H ↔ H†`, §1–§2), and the **irreversible face** is *fixing its one bit* —
the same ½-spin closure, two readings, with `ΔF = −log 2` the toll of the second (*it from bit*: the
abstraction realized by the closure).

## 7a. "Garbage is never erased" — one principle, three faces  *[structural reading]*

The Fredkin ledger has a strong reading, and it is the same fact the repo already states about black
holes and about closure horizons. **The substrate has no intrinsic erase.** Every twist history is
`H ↔ H†` (§1); every gate that respects ZFA is a permutation of the twist multiset
(`encode_fredkin_perm`) and hence a bijection; a composition of such gates is a bijection to any depth
(`fredkin_iterate_bijective`). Nothing in the generate-and-close machinery is many-to-one. The only
`ΔF = −log 2` bill anywhere is a **reset a holder chooses to perform** on garbage it declines to keep —
`garbageBill k = k · log 2`, a function of the retained-line count and nothing about the circuit
(`garbageBill_eq_closures`, `garbageBill_pos_iff`, [`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean)).

Three faces of the one principle:

- **Fredkin.** The reversible computer runs indefinitely at zero free-energy cost *as long as the
  garbage is retained*. The bill is external, optional, and exactly the `k` bits you overwrite — not a
  property of having computed.
- **Black holes** ([`BLACK-HOLES.md`](BLACK-HOLES.md) §3, §3a). The Hawking unwind is the closure run
  backward: the emitted spectrum matches the seed frequency, the unitary information ledger is returned,
  and the exact *gauge* charge comes back as hair. A QLF black hole never performs the many-to-one
  erase either — there is no information *paradox* because there is no erasure *step*. (What is not
  returned is the non-conserved global `B−L`, because that was never an exactly-conserved signed count
  — §3a — not because information was destroyed.)
- **The closure horizon** ([#148](https://github.com/rchain-community/quantum-logical-framework/issues/148)).
  Closure quotients generating histories by their surviving invariants (the ledger, the Pauli scalar,
  the winding) — many microscopic histories map to one closed state. Those distinctions become
  **inaccessible from the closed state**, not destroyed: an information horizon over generating history,
  the paint-mixing analogy. "Closure forgets the right things" = it forgets the path and keeps the
  homotopy class.

So *"reversible logic, irreversible process"* sharpens: the **logic** is reversible all the way down
(no erase primitive), and the **process** is irreversible only as forward sequencing in synthesized
time (§3) plus whatever resets a holder elects. Erasure is never forced on the substrate — it is a
choice made at a horizon, and the bill is precisely the garbage declined.

**Falsifiability (method rule 4).** This claim would be false for a substrate carrying an intrinsic
irreversible primitive — a many-to-one gate that no history can avoid. QLF has none: every closure is
`H = H†` and every ZFA-respecting gate is a permutation. So this is a structural consequence of the
existing theorems, not a new prediction — labelled accordingly.

## 8. What we can say, if the universe is quantum logical

The second law, decoherence, measurement-without-collapse, and the arrow of time are **one thing** — the
forward, many-to-one, bit-synthesizing direction of ZFA closure, in a time it makes itself. The universe is
**microscopically reversible** (the dagger involution; each closure `H = H†`) and **macroscopically
forward-only** (the synthesis), and *constructively* so — `full_zeno_prune` + `disjunctive_closure` +
`ΔF = −log 2`, not a hand-waved "we just don't track the microstate." No separate arrow postulate, no
fine-tuned initial condition: the arrow is the embedding, and reversal is an algebra operation with no
time to run in.

**Energy conservation is the same lesson.** Just as reversibility is a real symmetry of the *laws* but
not of the *universe*, energy conservation is a real *present-local* balance but not a fundamental global
law: each closure that synthesizes a tick of time also *creates* energy, lending half forward (the cosmic
expansion / dark energy) while the present half balances. The arrow of time and the creation of energy are
the **same** forward event-duality — a TOE that axiomatizes either reversibility *or* global energy
conservation has mistaken the present-local balance of the closure for the whole of it. See
[`Conservation.md`](Conservation.md) §2b.

## Lean anchors

| Statement | Lean |
|---|---|
| the reverse = the Hermitian conjugate | `eval_dagger` (`RhoQuCalc`) |
| dagger reverses the sequence `(AB)† = B†A†` | `dagger_sequence_reversal` (`BraKetRhoQuCalc`) |
| time-reverse is an involution (`T² = 1`) | `antiparticle_involutive` (`QLF_Majorana`) |
| charge conjugation = motional/time reversal | `C_eq_motional_reversal` (`QLF_Spin`) |
| every closure's mode is Hermitian | `toSpectralMode_hermitian` (`QLF_Spectral`) |
| **balanced ⟺ `H = H†`** (self-time-reverse) | `spectral_symmetric_eq_scalar_id` (`QLF_Spectral`) |
| **strand + its dagger is always a ZFA closure** (reversibility *is* closure) | `dagger_closes` (`QLF_QuantumTurbulence`) |
| a dagger-closure folds to a real `±I` (never `±i`) | `dagger_closure_folds_real` (`QLF_QuantumTurbulence`) |
| forward closure is many-to-one (`C(2n,n)` histories → 1) | `disjunct_count_eq_central_binomial` (`QLF_InfoSynthesis`) |
| reachability is an antisymmetric partial order (no un-reaching) | `reachable_antisymm`, `futureCone_subset` (`QLF_ReachableEvent`) |
| each closure synthesizes one bit `ΔF = −log 2` | `zfa_closure_minimizes_free_energy` (`QLF_FreeEnergy`) |
| time is synthesized, `f = 1/t` | `ZFAEventDynamics` |
| `H = H†` fixed points = the critical line | `spectral_hilbert_polya` (`QLF_Riemann`), `functional_equation_fixed_real` |
| **capstone:** reverse is involutive **but** forward closure is many-to-one | `time_reverse_involutive_but_closure_degenerate` (`QLF_Reversibility`) |
| **conservative logic is ZFA**: a Fredkin gate acts by permutation, so it preserves closure | `encode_fredkin_perm`, `fredkin_preserves_zfa` (`QLF_Fredkin`) |
| a reversible gate is a bijection — nothing merges, so nothing is receipted | `fredkin_involutive`, `fredkin_bijective` (`QLF_Fredkin`) |
| an `n`-deep reversible circuit is still a bijection (free-side premise survives composition) | `fredkin_iterate_bijective` (`QLF_Fredkin`) |
| **the erasure bill is external**: `k · log 2` in the retained-garbage count, not the gate count; running is free | `garbageBill_eq_closures`, `reversible_run_cost_zero`, `garbageBill_pos_iff` (`QLF_Fredkin`) |

## Honest scope

The pieces are each machine-verified; this document is the **synthesis** that names how they fit —
*reverse = dagger*, *balanced = `H = H†` = self-time-reverse*, *arrow = forward sequencing in synthesized
time*, *`H ↔ H†` = critical line*. The packaging theorem contrasting the **involutive** time-reverse
(`antiparticle_involutive`, a bijection) with the **non-injective** forward closure (`C(2n,n) ≥ 2`
histories per closure) is verified as **`time_reverse_involutive_but_closure_degenerate`**
(`QLF_Reversibility`, no new axioms — both halves reuse existing theorems). §7's Fredkin case is verified on the same footing —
`encode_fredkin_perm` and `fredkin_preserves_zfa` (`QLF_Fredkin`, no QLF axiom in the footprint), with
`fredkin_bijective` carrying the free-ledger claim; what is *not* a Lean statement there is the reading
of a gate as one physical event, which [`Fredkin_QLF.md`](Fredkin_QLF.md) §6 marks as modelled. The
remaining synthesized-time framing (there is no meta-axis in which to *run* the reverse) is prose
grounded in `ZFAEventDynamics` (`f = 1/t`), not a further Lean obligation. §6a's π/Poisson identification
is likewise prose — a reading of standard analytic number theory against the verified `H ↔ H†` involution,
carrying no Lean obligation and, by method rule 4, no new count. The `†` here is the `*`-involution of
the substrate's state ring — a finite-rank `ℤ[i]`-lattice, not Hilbert space; see
[`The_QLF_State_Space.md`](The_QLF_State_Space.md). See [`Decoherence.md`](Decoherence.md),
[`Entropy.md`](Entropy.md), [`Conservation.md`](Conservation.md), [`Philosophy.md`](Philosophy.md), and the
synthesized-spacetime account in [`ZFAEventDynamics.lean`](lean/ZFAEventDynamics.lean).
