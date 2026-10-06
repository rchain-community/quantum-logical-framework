# Banach–Tarski in QLF — impossible duplication, model-explosion, and mitosis as the possible version

In 1924 Stefan Banach and Alfred Tarski proved that, using the **Axiom of Choice**, a solid ball can
be cut into finitely many pieces and reassembled — by rigid motions alone — into **two** balls each
identical to the original. Volume conjured from nothing. It is the most vivid theorem in mathematics
that says: *something here is not physics.*

The [Quantum Logical Framework](README.md) (QLF) takes Banach–Tarski as a touchstone, and three of its
commitments meet in it:

1. it is the cleanest example of **impossible mathematics** — the continuum-and-choice "ultraviolet
   catastrophe" QLF is built to avoid ([`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md),
   [`TheContinuum.md`](TheContinuum.md));
2. it is the textbook case of **a false axiom certifying an absurdity** — stated *precisely*, the
   ontological (model) version of *ex falso*, not the syntactic one;
3. it is the *impossible* twin of an entirely **possible** duplication — **mitosis**, one cell becoming
   two — and the gap between them is exactly the gap QLF draws between fantasy and the realizable
   substrate.

---

## 1. Banach–Tarski as impossible mathematics

QLF's organizing thesis is that **the continuum and the Axiom of Choice are mathematics' ultraviolet
catastrophe** — formal infinity admitted without a closure condition, the way classical physics once
admitted arbitrarily fine modes until the blackbody spectrum diverged. The fix in both cases is a
cutoff: in physics, the quantum of action; in QLF, the requirement that an object be **constructible in
finite time** — admitted only if it has a finite ZFA closure ([`Philosophy.md`](Philosophy.md),
[`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md)).

Banach–Tarski is the cleanest thing that cutoff excludes. The decomposition is built from a **free group
`F₂`** of rotations whose paradoxical self-partition (`F₂` is equidecomposable with two copies of
itself) is transported onto the sphere; the resulting pieces are **non-measurable** — they have no
volume, no finite description, no procedure that produces them. They exist only because AC *asserts* a
selection (one point from each orbit) with **no construction**. Drop in those pieces and the volume
bookkeeping breaks: five pieces with "no volume" reassemble into twice the ball.

QLF's reading: these pieces are not realizable. A bounded region holds only finite information
(Bekenstein), so it has only finitely many distinguishable states — and an infinite, non-finitely-
describable point-set cannot be faithfully placed inside it. This is machine-checked in
[`lean/QLF_Realizability.lean`](lean/QLF_Realizability.lean): `no_continuum_in_finite_region` (no
injection from an infinite state space into a finite one) and `real_continuum_not_realizable` (its
Bekenstein concretization). The Banach–Tarski pieces are exactly the "gratuitous tail" QLF declines to
make physical ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md): Tegmark makes *all* structures
real, including the Banach–Tarski pathologies; QLF makes only the **realizable** subset real).

**The replacement for Choice.** QLF does not argue with AC on its own ground; it *refuses* it and
substitutes a computable filter. Where AC posits a selection function with no procedure, QLF uses
**`full_zeno_prune`** — a decidable, RCA₀-level selection that keeps exactly the ZFA-closed histories.
No non-constructive choice, no non-measurable set, no paradoxical decomposition: the explosion never
starts.

---

## 1a. The free group — what QLF shares with Banach–Tarski, and what it doesn't

It is tempting to dispatch Banach–Tarski by saying the QLF twist algebra "cannot form the free group
`F₂`." That is **false**, and saying it would weaken the case. QLF *does* generate freely: the twist
strings are the **free monoid** on the 8-letter alphabet — `expand_generation` branches without
relations, giving exponentially many histories (`generated_count`: `4^n` strings of length `2n`,
[`QLF_Firebreak`](lean/QLF_Firebreak.lean)), and the closure census is the central binomial `C(2n,n)`
([`QLF_PhysicalPi`](lean/QLF_PhysicalPi.lean)). That exponential free growth is the direct combinatorial
analog of `F₂`'s — the free group on two generators has `4·3^{n−1}` reduced words of length `n`. QLF has
the free engine; it is **not** too poor to host one. And `F₂` itself is **not** a continuum object — the
standard `F₂ ⊂ SO(3)` is built from two rotations with *rational* matrix entries and is *provably* free
with no Choice at all.

So freeness is not where the paradox's teeth are. By **Tarski's theorem**, a set admits a paradoxical
decomposition **iff** the acting group is **non-amenable** — it has *no* invariant finitely-additive
measure. `F₂` is the canonical non-amenable group; that, not its freeness per se, is the engine. And to
turn the group-theoretic paradox into a *geometric* one — doubling the ball — Banach–Tarski needs two
further ingredients on top: an **uncountable continuum** for `F₂` to act on (the sphere's points), and
the **Axiom of Choice** to select one representative per orbit, producing the non-measurable pieces.

The substrate supplies **none** of the three (anchored in
[`QLF_NoFreeDuplication`](lean/QLF_NoFreeDuplication.lean)):

1. **Amenability by construction.** Every signed twist count is a *conserved additive invariant* — a
   homomorphism `(TopoString, ++) → (ℤ, +)` (`zfa_charge_additive`, reusing `wcount_append`). That is
   precisely the invariant finitely-additive measure `F₂` lacks: the ZFA balance **is** the invariant
   mean. A configuration that conserves an additive charge cannot be cut and reassembled into two copies
   of itself — the charge would have to double.
2. **A finite (amenable) fold.** The free twist-monoid's *physical image* under closure is the **finite**
   order-16 Pauli group (`closure_folds_to_finite_group`, reusing `count_balanced_pauli_closed`): every
   ZFA closure renders to a `PauliScalar`. Finite groups are amenable; no paradox lives in the rendering.
   The free generation happens in the possibility stream; the realized physics is its finite,
   measure-preserving shadow.
3. **No continuum to act on, no Choice to select.** The substrate is countable / finite-information
   (`no_continuum_in_finite_region`, [`QLF_Realizability`](lean/QLF_Realizability.lean)) — there is no
   uncountable orbit space — and `full_zeno_prune` replaces AC, so the non-measurable orbit selection
   never happens.

So relating QLF twists to the free group **strengthens** the argument rather than dodging it: QLF
concedes the free combinatorial richness (the honest move) and then locates Banach–Tarski's actual
dependencies — non-amenability, the continuum, and Choice — showing the substrate omits each, two of them
machine-verified by reuse. The free engine is real; it is just amenable, finite-folded, and acting on a
countable world, so it never doubles anything.

---

## 2. Is it "a false axiom proving anything"? — yes, but precisely

It is tempting to say Banach–Tarski shows ZFC is broken — "from a false axiom you can prove anything,"
*ex falso quodlibet*. That is the right intuition stated the wrong way, and the wrong way is a crank
trap. The precise version:

**Banach–Tarski is *ontological* (model) explosion, not *syntactic* explosion.** ZFC is **consistent**
(as far as anyone knows): it does **not** prove `0 = 1`, so it does not literally prove *every*
sentence. What Banach–Tarski exhibits is different and sharper — the Axiom of Choice is **false in the
intended model**, the physical world, and *an axiom false in the intended model certifies theorems that
are false in that model*: a ball that is two balls. The unsoundness is with respect to the **physical
interpretation**, not with respect to ZFC's own consistency.

QLF states it this way deliberately ([`Millennium.md`](Millennium.md): "by *ex falso quodlibet* an
axiom false-in-the-model makes everything provable; ZFC's Banach–Tarski is the visible symptom";
[`Philosophy.md`](Philosophy.md) §"Unsoundness and Consistency": "a system that proves a falsehood
certifies nothing"). The **binding precision**, load-bearing for every QLF claim about foundations:

> The claim is **consistency ≠ realizability**, *never* "ZFC is inconsistent" or "ℝ is false."

`ℝ` is a consistent structure; one can write endless consistent theories that describe nothing
realizable. Banach–Tarski is the demonstration that *consistent* and *sound-for-physics* are different
properties, and that AC has the first without the second. QLF's quarrel is with **soundness for
physics** — it keeps its own axioms true *in the intended model* by admitting only constructible
objects, so its proofs stay physically sound and no absurdity is certified. (This "false" is
**ontological**, not syntactic — the standard, defensible reading; see
[`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md), [`TheContinuum.md`](TheContinuum.md) §2,
the "five converging strikes": Löwenheim–Skolem, Gödel–Cohen, reverse-math conservativity,
unrealizable, unneeded.)

---

## 3. The possible twin — mitosis pays for what Banach–Tarski steals

Banach–Tarski and **mitosis** are the two faces of one coin: duplication. One ball becomes two; one cell
becomes two. The difference is the entire content of QLF's foundations.

Banach–Tarski duplicates **for free**: no information is copied, no energy is spent, no time passes — the
second ball is conjured by re-labeling non-measurable pieces. It is the duplication you get when you
**drop the cost ledger** (AC's free choice).

Mitosis duplicates by **paying**:

- it **copies the information** — DNA is replicated base-by-base, the daughter's genome is *built*, not
  conjured (no second copy appears without first laying down its bits);
- it **spends free energy** — ATP hydrolysis drives replication, spindle assembly, and division; the
  cell does thermodynamic work;
- it **supplies the mass** — the second cell's material is synthesized from nutrients, not summoned from
  the first;
- it **takes time** — division is a sequence of closures, and in QLF time is *synthesized* by closure
  (`f = 1/t`, [`Reversibility.md`](Reversibility.md)); there is no instantaneous copy.

That is duplication with the **ledger kept** — ZFA-closed, conservation-obeying. The per-event price is
exact: each half-spin ZFA closure decrements free energy by `ΔF = −log 2` nats
([`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean), `zfa_closure_minimizes_free_energy`), which *is*
Landauer's `k_BT ln 2` — the irreducible cost of fixing one bit ([`Conservation.md`](Conservation.md),
[`Reversibility.md`](Reversibility.md)). You cannot get two distinguishable closures out of one for
free; you must mint, and pay for, the bits that tell them apart.

The DNA copy has a precise form on the substrate: each strand is the Hermitian adjoint of the other, so the new strand is laid down against a complete record rather than conjured, and the duplex is a closure whatever the message ([`Quantum_Biology.md`](Quantum_Biology.md) §2–§3a).

So mitosis is precisely the duplication Banach–Tarski is *not*: it buys its second copy in information,
energy, mass, and time. Banach–Tarski is what duplication would look like if those bills never came due
— which is to say, it is not physics.

### 3a. The geometric sharpening — the blanket's charge is subdivision-invariant

Banach–Tarski's minimal decomposition uses **five pieces** (Robinson 1947 — four is impossible). It is
tempting to look for that "5" in QLF geometry — the substrate even has a verified `5 = 3 + 2`
([`QLF_BorromeanAngles`](lean/QLF_BorromeanAngles.lean), `total_angular_DOF_eq_five`). **Resist it.** The
Banach–Tarski 5 is `1 + 2×2` — the identity class plus the four "first-letter" classes of `F₂`'s *two*
generators; it is tied to the 2-generator free group, not to QLF's 3 axes, and the Borromean 5 is a count
of *angular degrees of freedom*, a different object. Forcing the identification would be numerology.

What *does* relate — and sharpens mitosis — is the **doubling requirement** itself: *finitely many pieces
reassembling into two copies.* A QLF Markov blanket is a Fuller geodesic sphere carrying **conserved,
subdivision-invariant topological charge**:

- Euler characteristic `V − E + F = 2` at **every** frequency `v` (`primordial_blanket_euler`);
- exactly **12 pentamons**, independent of `v` (`pentamons_invariant` — the universal signature from the
  icosahedron to the cosmic blanket);
- a holographic boundary screen of `20 v²` events carrying `S(v) = 20 v² · log 2` nats
  (`primordial_blanket_information_capacity`).

Subdividing a blanket — refining `v`, the geometric analog of cutting it into finer pieces — **preserves**
all of these: still `χ = 2`, still 12 pentamons (`blanket_charge_subdivision_invariant`,
[`QLF_NoFreeDuplication`](lean/QLF_NoFreeDuplication.lean)). Two blankets have `χ = 4` and 24 pentamons. So
**no decomposition of one blanket — into five pieces or any number — can yield two**, because the charge
is conserved *and* subdivision-invariant. This is the geometric face of §1a's amenability point: the
blanket's `χ`/pentamon count is another invariant the paradox has no room for.

Banach–Tarski evades it only because its five pieces are **non-measurable scatter** — they have no `χ`,
no pentamons, no boundary, no geometry at all; they are choice-selected dust, not blanket-pieces. A
blanket built of finite-information closures **has no such pieces to use**. So to make two blankets it
cannot rearrange — it must **synthesize** the second blanket's conserved structure: a second `χ = 2`, a
fresh set of 12 pentamons, and a doubled holographic screen carrying its own `20 v² · log 2` nats
(`blanket_doubling_doubles_information`). That synthesis *is* mitosis's cost — DNA replication writes the
second boundary's bits, ATP pays the `log 2`-per-event Landauer bill.

This is the sharpened statement: **the conserved geometric structure that Banach–Tarski steals from
nothing is exactly the structure mitosis must build.** The "five pieces" of the impossible version
correspond, in the possible version, not to a piece count but to the subdivision-invariant charge that
has to be *manufactured* — a second 12-pentamon screen, written bit by bit — rather than shuffled.

---

## 4. One principle, four scales — "no free duplication"

The substrate does not merely *fail* to permit free duplication; it **actively forbids** it, and the
prohibition is the same theorem wearing four costumes. (The Lean anchor is
[`lean/QLF_NoFreeDuplication.lean`](lean/QLF_NoFreeDuplication.lean), a reuse-corollary of three already-
verified facts.)

| Scale | "No free copy" | "Must pay / distinguish" |
|---|---|---|
| **Quantum** | No-cloning (Wootters–Zurek 1982): an unknown state can't be copied | Copying a capability is a linear-logic type error / ZFA asymmetry ([`QuantumOS.md`](QuantumOS.md)) |
| **Substrate** | Identical ρ-processes are Pauli-blocked: `fermi_antisym p p = 0` (`identical_copy_pauli_blocked`, reusing `pauli_exclusion`) | `fermi_antisym` is *not* identically zero — distinct processes can differ (`fermi_nonzero_example`) |
| **Nucleonic** | Two *identical* proton blankets can't bind — no diproton (`diproton_pauli_blocked`) | A β⁺ `u→d` step makes them distinguishable so the deuteron closes (`pp_join_requires_distinguishability`, [`Fusion.md`](Fusion.md), [`SEX.md`](SEX.md)) |
| **Cellular** | Two daughters cannot be the *same* instance | Mitosis copies DNA + spends ATP to make distinguishable daughters (structural analogy) |
| **Mathematical** | Banach–Tarski "free" ball-from-nothing is excluded | Realizable duplication pays `ΔF = −log 2` per distinguishing bit (`duplication_pays_log_two`) |

A sixth costume shows up in *computation*, where the same principle is visible as ordinary circuit
bookkeeping: Fredkin's `FANOUT` gate is `FREDKIN(x; 0, 1)`, and its third line carries `NOT x` away as
garbage — a duplicate arrives with its complement attached, and the garbage is what you eventually pay
`ΔF = −log 2` per line to erase. Copying is not free, and the ledger says so
([`Fredkin_QLF.md`](Fredkin_QLF.md) §5).

Read top to bottom, it is one statement: **no free identical copy** — the Pauli/no-cloning floor — and
its corollary **realizable duplication needs distinguishability, bought at a cost**. The quantum
no-cloning theorem is the *quantum* form of "no free Banach–Tarski"; the no-diproton is its *nuclear*
form; mitosis is its *biological* form. QLF already proves the substrate and nuclear forms (no new
axioms — `QLF_NoFreeDuplication` just reuses `pauli_exclusion`, `pp_join_requires_distinguishability`,
and `zfa_closure_minimizes_free_energy`); the cellular form is the natural extension stated as an
analogy.

---

## 5. The unifying statement

> **Banach–Tarski is what duplication looks like when you drop the cost ledger; mitosis is what it looks
> like when you keep it.**

The free, identical, instantaneous copy is exactly the object QLF's finite-construction filter excludes
— the same filter that excludes non-measurable sets, the continuum's uncountable tail, and the
Busy-Beaver horizon. The paid, distinguishable, time-taking copy is exactly what ZFA closure produces —
the same closure behind the half-spin atom, the deuteron, and the local clock. The line between
impossible and possible *duplication* is the line between the **continuum/choice fantasy** and the
**realizable substrate**, drawn one more time, now through the most famous "paradox" in mathematics.

A cell could not perform Banach–Tarski if it tried: the substrate has no free identical copy to give it.
What it can do — and does, every division — is pay the bill. That it must pay is not a limitation
biology happened to inherit; it is the same fact that keeps the universe consistent with itself.

---

## Honest scope

- **Banach–Tarski is a real, consistent ZFC theorem.** The claim throughout is **consistency ≠
  realizability / soundness-for-physics** — *not* "ZFC is inconsistent" or "ℝ is false." The *ex falso*
  point is **ontological (model) explosion** (an axiom false in the intended model certifies absurd
  objects), never syntactic explosion. Banach–Tarski is **not** formalized in Lean — QLF's point is that
  its objects are non-realizable, not that they are inconsistent, so there is nothing to verify and
  much to *decline to import*.
- **The mitosis reading is a structural analogy** — Markov-blanket fission as the biological instance of
  paid duplication — **not** a derivation of cell biology. QLF has no cellular dynamics; this doc
  introduces the analogy and says so. What *is* machine-verified is the substrate/nuclear core
  ([`lean/QLF_NoFreeDuplication.lean`](lean/QLF_NoFreeDuplication.lean), reusing
  [`PauliExclusion.lean`](lean/PauliExclusion.lean), [`QLF_Fusion.lean`](lean/QLF_Fusion.lean),
  [`QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)).
- The **"no free duplication" principle across scales** is a synthesis/reading, anchored where Lean
  exists (the quantum no-cloning, the no-diproton, the `−log 2` cost) and stated as analogy where it does
  not (the cellular scale).
- The **free-group / amenability angle** (§1a) is the honest version: QLF *concedes* the free engine (the
  free twist-monoid is real) and locates the paradox's actual dependencies — non-amenability, the
  continuum, and Choice. **Tarski's theorem** (paradoxical ⟺ non-amenable) is *cited*, not formalized;
  what is machine-verified by reuse is that the substrate carries a conserved additive invariant
  (`zfa_charge_additive`) and folds to a finite, amenable group (`closure_folds_to_finite_group`) — the
  structural reasons it is amenable. Claiming the substrate has *no* free structure would be false and is
  not claimed.
- The **geometric sharpening** (§3a) deliberately *resists* matching Banach–Tarski's "5 pieces" to QLF's
  `5 = 3 + 2` angular DOF — that would be numerology (the two 5s are unrelated objects). What is
  machine-verified is the subdivision-invariance of the blanket's charge (`blanket_charge_subdivision_invariant`,
  reusing `primordial_blanket_euler` + `pentamons_invariant`) and the doubled holographic information
  (`blanket_doubling_doubles_information`); the identification of "writing the second screen" with DNA
  replication / ATP is the *structural analogy* (the mitosis reading), not derived cell biology.

## See also

- [`Continuum_Choice_Fallacy.md`](Continuum_Choice_Fallacy.md) · [`TheContinuum.md`](TheContinuum.md) ·
  [`Philosophy.md`](Philosophy.md) — the continuum/choice = UV-catastrophe thesis and the five strikes.
- [`Millennium.md`](Millennium.md) — the *ex falso*/false-in-the-model framing and the 1924 citation.
- [`Mathematics_From_QLF.md`](Mathematics_From_QLF.md) — realizable math vs the gratuitous (Banach–Tarski)
  tail; QLF vs Tegmark.
- [`SEX.md`](SEX.md) · [`Fusion.md`](Fusion.md) — the nucleonic "one becomes two needs distinguishability."
- [`Conservation.md`](Conservation.md) · [`Reversibility.md`](Reversibility.md) — the `−log 2` ledger,
  Landauer, synthesized time.
- [`QuantumOS.md`](QuantumOS.md) — no-cloning as linear-logic / capability security.

---

## The capacity reading

Banach–Tarski is consistency without realizability. The companion statement about *laws* rather than
objects is the **Law of Exceptions**: a system with more states can always break a finite closure, so
every restrictive law has a real exception and no finite closure is final —
[`Law_Of_Exceptions.md`](Law_Of_Exceptions.md), machine-verified in
[`lean/QLF_LawOfExceptions.lean`](lean/QLF_LawOfExceptions.lean). Both are the same discipline applied at
different altitudes: what a finite capacity can instantiate, versus what a finite capacity can legislate.
