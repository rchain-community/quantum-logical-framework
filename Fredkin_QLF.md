# The Fredkin Computer in QLF

**A conservative-logic computer built on the [Quantum Logical Framework](README.md)
substrate, where the gate's conservation law and the substrate's admissibility condition
turn out to be the same law.**


*Built at the suggestion of **Van Hovey**, whose idea it was to run Fredkin's machine on the substrate.*

Implementation: [`fredkin_qlf.py`](fredkin_qlf.py) · run it with `python3 fredkin_qlf.py`
Machine-verified core: [`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean)
Interactive: [`fredkin_machine.html`](fredkin_machine.html) —
[**run it live**](https://rchain-community.github.io/quantum-logical-framework/fredkin_machine.html)

---

## 1. Background

Edward Fredkin and Tommaso Toffoli asked in *Conservative Logic* (1982) what computation
looks like if it must obey conservation laws the way physics does. Their answer was the
**Fredkin gate**, a controlled swap:

```
FREDKIN(c; a, b) = (c, a, b)   if c = 0
                 = (c, b, a)   if c = 1
```

Two properties make it a physical primitive rather than a notational one. It is its **own
inverse**, so no computation is lost running it. And it is **conservative**: the outputs
are a permutation of the inputs, so the number of 1s is exactly the number that went in.
Nothing is created and nothing is destroyed — the gate only routes.

Their physical realization was the **billiard ball model**. Unit balls travel on a lattice;
a ball present on a line reads as 1 and an empty line as 0; elastic collisions deflect
balls onto different paths. Conservation of logical 1s is then literally conservation of
balls, and the whole of computation is elastic scattering. The primitive is the
*interaction gate*: two balls on crossing paths either collide, and leave on the two inner
exits, or miss each other and continue on the outer ones.

This mattered because of **Landauer (1961)**: erasing one bit dissipates at least
`kT log 2`. **Bennett (1973)** drew the consequence that computation itself need cost
nothing — only *forgetting* does — and conservative logic is the construction that shows
it, buying reversibility with constants fed in and garbage carried out.

QLF meets this programme at an angle. [`Related_Frameworks.md`](Related_Frameworks.md)
places Fredkin's digital mechanics among the frameworks sharing QLF's discrete substrate
while lacking an admissibility criterion: *everything runs, nothing is selected*. That is
the honest difference, and it is also why the Fredkin gate is the natural thing to build
here. Fredkin has a conservation law and no selection principle; QLF's selection principle
**is** a conservation law.

---

## 2. The identification

QLF admits a history when its signed twist counts vanish — Zero Free Action, the condition
`full_zeno_prune` implements. Fredkin admits a gate when it conserves the count of 1s.

The two conditions are the same *kind* of statement, and under the encoding below they
become the same statement. A Fredkin gate permutes lines. A permutation preserves the
multiset of twists. The signed action vector is a function of that multiset alone.
Therefore **the gate cannot take a realized history to an unrealized one** — not because
we checked, but because it is a relabelling.

This has two faces, and both are load-bearing elsewhere. Mathematically the gate is an
**automorphism of the admissible closure space** — the first rung of the emergence ladder that is a
*map* on the structure rather than more structure ([`Mathematics_From_QLF.md`](Mathematics_From_QLF.md)
Rung 5b). Informationally it is a **bijection**, so information moves without being forgotten and
the receipt is zero — the executable converse of Landauer
([`Information_Physics.md`](Information_Physics.md) §5a). Invertible map, reversible logic,
conserved quantity: on the substrate these are one operation.

The final step is already machine-verified and is what makes this cheap: the keystone
**`count_balanced_pauli_closed`** ([`lean/QLF_TwistAlphabet.lean`](lean/QLF_TwistAlphabet.lean))
proves count balance *entails* Pauli closure for every twist history, cross-axis
interleavings included. So preserving the counts preserves full ZFA — both conjuncts — and
the order-sensitive half comes along for free rather than needing its own argument.

## 3. The encoding

| Object | Encoding | Why |
|---|---|---|
| one ball | `^<v>` | up, left, down, right — the minimal closed plaquette. Count-balanced, Pauli-closed, length 4 = `MIN_ZFA_LENGTH`, so it passes full `twist_core.is_zfa` |
| empty line | the empty history | absence contributes no twists; it is the zero of the algebra, not an invalid history |
| register | concatenation of its lines | so a gate acting on lines acts on the history by permutation |

`^<v>` is **one** ball, not *the* ball. Of the 4096 twist histories of length 4, **168 are
ZFA-closed** — 4.10%. Per the working method ([`Philosophy.md`](Philosophy.md) §3a, rule 1)
the count is the physical content and the exhibited witness is not; a ball happens in 168
ways at this length, and picking one is a presentation choice.

### Why helium

The billiard ball model needs balls that **collide and never stick**. In QLF a bond is a
*shared closure*, and [`Chemistry.md`](Chemistry.md) gives helium valence **0** — a closed
shell with no unshared closure to offer. Two helium atoms therefore have nothing to share
and cannot bond; they can only scatter. The idealization Fredkin and Toffoli had to
*impose* on their balls is here a consequence of the valence rule.

**The bits are physical closures, and you can look at them.** The spacetime constructor takes
deep-linked initial conditions — `kind @ x,y,z v vx,vy,vz` — so the Boolean `11` can be opened as
what it actually is: [two helium closures approaching an interaction region](spacetime_constructor.html#qc=He%20%40%20-6%2C-2%2C0%20v%201.2%2C0.4%2C0%0AHe%20%40%20-6%2C2%2C0%20v%201.2%2C-0.4%2C0).
Not two marks in a truth table but two closures with positions, clocks and trajectories, each able
to enter a later joint closure. **Scope, so the link is not overread:** the constructor *renders*
those closures, it carries no elastic-collision dynamics, and it is a reading rather than a cause
([`Spacetime_Constructor.md`](Spacetime_Constructor.md)). It shows you the inputs; it does not run
the gate. The dynamical two-history question — causal diamonds intersecting into a joint closure —
belongs to [`MultiParticle.py`](MultiParticle.py).

Buckyballs (C₆₀) qualify for the same structural reason — a closed cage, every carbon
saturated within it — and have the practical advantage of being massive enough to behave
ballistically while still demonstrably quantum (Arndt *et al.* 1999). Helium is the cleaner
derivation; C₆₀ is the more plausible apparatus.

---

## 4. Run results

All output below is from `python3 fredkin_qlf.py`, unedited.

**The ball.** `'^<v>'` — `ZFA=True`, `action=(0,0,0,0)`, `pauli_closed=True`.

**The gate is conservative and self-inverse.** All eight inputs:

```
    000 -> 000   weight 0 -> 0   conserved      100 -> 100   weight 1 -> 1   conserved
    001 -> 001   weight 1 -> 1   conserved      101 -> 110   weight 2 -> 2   conserved
    010 -> 010   weight 1 -> 1   conserved      110 -> 101   weight 2 -> 2   conserved
    011 -> 011   weight 2 -> 2   conserved      111 -> 111   weight 3 -> 3   conserved
```

`fredkin ∘ fredkin = id`: **True**.

**The substrate claim.** For every input the encoded history's signed action vector is
`(0,0,0,0)` before and after, and both are ZFA-closed:

```
     in    out   action(in)     action preserved   ZFA(in)  ZFA(out)
    000   000     (0, 0, 0, 0)               True      True      True
    101   110     (0, 0, 0, 0)               True      True      True
    110   101     (0, 0, 0, 0)               True      True      True
    111   111     (0, 0, 0, 0)               True      True      True
```

*(the four unswapped rows are identical and omitted)* — **action vector preserved on every
input: True**.

**The collision conserves balls.**

```
    00 -> 0000   balls 0 -> 0   conserved
    01 -> 0001   balls 1 -> 1   conserved
    10 -> 1000   balls 1 -> 1   conserved
    11 -> 0110   balls 2 -> 2   conserved
```

The `11` row is the collision proper: two balls in, deflected onto the two inner exits.

**Watch the conservation law.** [`fredkin_machine.html`](fredkin_machine.html) animates exactly
these four rows at the top of the page — two balls on crossing tracks, `11` the one to look at:
they meet, deflect onto the inner exits, and the three readouts beside them do not move. Balls in
equals balls out, the signed twist action stays `(0,0,0,0)`, and the information discarded stays
`0`. Press **Reverse** and the collision runs backwards. Everything §2 argues is visible in one
screen there.

**Universality.** Every primitive from the one gate, each verified on its full truth table:

| Gate | Wiring | Output read from |
|---|---|---|
| `NOT x` | `FREDKIN(x; 1, 0)` | first target |
| `x AND y` | `FREDKIN(x; 0, y)` | first target |
| `x OR y` | `FREDKIN(x; 1, y)` | second target |
| `FANOUT x` | `FREDKIN(x; 0, 1)` | control and first target |

```
    NOT:    0->1  1->0
    AND:    00->0  01->0  10->0  11->1
    OR:     00->0  01->1  10->1  11->1
    FANOUT: 0->(0, 0)  1->(1, 1)
```

FANOUT is worth a second look. Its third line carries `NOT x` away as garbage: a duplicate
arrives with its complement attached. Copying is not free, and QLF says why —
[`QLF_NoFreeDuplication`](lean/QLF_NoFreeDuplication.lean), the same principle that forbids
cloning, the diproton, free mitosis and Banach–Tarski
([`Banach_Tarski_QLF.md`](Banach_Tarski_QLF.md)).

**A one-bit full adder, Fredkin gates only.** `sum = a ⊕ b ⊕ cin`,
`carry = (a ∧ b) ∨ (cin ∧ (a ⊕ b))`, every twice-used value fanned out first:

```
    a b cin | sum carry | correct        a b cin | sum carry | correct
    0 0  0  |  0    0   | ok             1 0  0  |  1    0   | ok
    0 0  1  |  1    0   | ok             1 0  1  |  0    1   | ok
    0 1  0  |  1    0   | ok             1 1  0  |  0    1   | ok
    0 1  1  |  0    1   | ok             1 1  1  |  1    1   | ok
```

**Correct on all 8 inputs**, at a cost of **19 Fredkin gates and 29 ancilla lines**. That
ratio is the real economics of conservative logic: the gate count is modest and the
bookkeeping dominates, because nothing may be thrown away.

---

## 4a. Watching it run

[`fredkin_machine.html`](https://rchain-community.github.io/quantum-logical-framework/fredkin_machine.html)
steps the circuits gate by gate, with the three readouts that matter live: the ball count,
the signed twist action, and the ledger. It is worth opening for one reason — **the reverse
button**. Run the adder to the end, press Reverse, and it walks back to the input it started
from, because each gate is its own inverse and the program is just the gate list read
backwards. Nothing is recomputed and nothing is restored from a log; the machine simply has
nowhere to have lost anything.

While it runs, the action vector never leaves `(0,0,0,0)` and the ball count never moves.
That is §2 happening in front of you: a gate permutes wires, so the twist multiset is
untouched, so the history stays realized. The ledger stays at zero for the same reason —
until you look at the garbage panel, which is where the bill actually is.

Verified against the Python before shipping: the same 19 gates, correct on all 8 adder
inputs, balls conserved at every step, and the reverse pass restoring the input on every
one. The page counts 30 garbage wires where `fredkin_qlf.py` reports 29 ancillas — the
adder runs on 32 wires (3 inputs + 29 ancillas) and keeps 2, so 30 are discarded, while the
script counts ancillas *allocated*. Same circuit, two accountings, both stated.

## 5. The free-energy ledger

QLF receipts every realized closure at `ΔF = −log 2`
([`lean/QLF_FreeEnergy.lean`](lean/QLF_FreeEnergy.lean)), which invites an obvious and
wrong inference: 19 gates, therefore 19 bits dissipated.

**An instantaneous zero-free-action closure is free.** The `−log 2` is the receipt of a
**many-to-one** closure — the quantum of *forgetting*. The Fredkin gate maps 8 states onto
8. It is a bijection: no two histories merge, nothing becomes unrecoverable, and there is
no free action left over to dissipate. It costs nothing.

```
    Whole adder, inputs + ancillas -> outputs + garbage:
      19 gates, all bijections    composed cost = 0
```

The bill arrives exactly where the computation stops being one-to-one, which is exactly
where you decline to keep the garbage. Resetting `k` garbage lines to zero is a `2^k → 1`
map:

```
      reset   1 line(s):  1 x log 2 =   0.6931 nat = 1 bit
      reset  29 line(s):  29 x log 2 =  20.1013 nat = 29 bit
```

So the adder is free to run and costs 29 bits to tidy up after.

This is Landauer and Bennett **recovered rather than assumed**. QLF does not have a
separate postulate that erasure costs; it has one quantum attached to closure, and closure
is many-to-one. Reversible computation sits on the free side of that line, and Fredkin's
conservation law is precisely what keeps it there. It is the same distinction
[`Reversibility.md`](Reversibility.md) draws throughout — **reversible logic, irreversible
process** — with the Fredkin computer as the case where the logic stays reversible all the
way to the end and the process never has to commit.

The ledger is now pinned in Lean, no new axioms
([`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean), reusing `QLF_FreeEnergy`):
`garbageBill k = k · log 2` is a function of the **retained-garbage count**, not the gate
count (`garbageBill_eq_closures` — it is `k` copies of the one closure quantum, not a new
postulate); `reversible_run_cost_zero` (`garbageBill 0 = 0`, any depth);
`fredkin_iterate_bijective` (an `n`-deep Fredkin circuit is still a bijection);
`garbageBill_pos_iff` (`0 < garbageBill k ↔ 0 < k` — the bill lands exactly where the map
stops being one-to-one). The **strong reading** — the substrate has no intrinsic erase, so
every `−log 2` is a reset a holder *elects* at a horizon, and a black hole's Hawking unwind
never performs one either — is [`Reversibility.md`](Reversibility.md) §7a (one principle,
three faces: Fredkin / black holes / the [#148](https://github.com/rchain-community/quantum-logical-framework/issues/148) closure horizon).

---

## 6. Honest scope

**Proven, and reused rather than re-argued.** `count_balanced_pauli_closed` — count balance
entails Pauli closure — is machine-verified in Lean with zero `sorry`, and it is what makes
"the gate preserves the twist multiset" enough to conclude "the gate preserves full ZFA".
The gate's conservativity and involutivity are finite facts, checked exhaustively over all
eight inputs.

**Computed.** Everything in §4: the truth tables, the action vectors, the ZFA checks
through `twist_core.is_zfa` (both conjuncts, not a stand-in), the adder over all 8 inputs,
the 168 length-4 closures.

**Modelled, not derived.** The encoding is a choice — one plaquette per ball, concatenation
per register. It is a faithful choice, in that the substrate conclusion follows from the
permutation structure and not from the particular word picked, but a different encoding
would need its own check. The `interaction_gate` is Fredkin and Toffoli's idealized
collision, not a dynamical simulation of two helium atoms.

**Machine-verified.** [`lean/QLF_Fredkin.lean`](lean/QLF_Fredkin.lean) closes the substrate
chain inside Lean, zero `sorry`: `fredkin_involutive`, `fredkin_bijective`,
`fredkin_conserves_weight`, `encode_fredkin_perm` (the gate acts by *permutation*),
`fredkin_preserves_counts`, `encode_countBalanced`, `fredkin_preserves_countBalanced`, and
the payoff `fredkin_preserves_zfa` — the output folds to a Pauli scalar, so both conjuncts
of runtime ZFA hold and neither needed its own argument. `fredkin_bijective` is the ledger's
premise in §5, stated where it can be checked; `garbageBill_eq_closures`,
`reversible_run_cost_zero`, `fredkin_iterate_bijective` and `garbageBill_pos_iff` pin the
rest of §5 (the bill is external, in the retained-garbage count, and the reversible run is
free to any depth).

**Not done here.** No trajectory-level billiard simulation, so no
timing, alignment or error analysis — the known Achilles heel of the billiard ball model,
where trajectory errors compound and the model needs periodic correction it cannot supply
reversibly. And no claim that a helium apparatus is buildable; §3 argues only that if you
want balls that never stick, QLF says why a valence-0 species is the right choice.

**The next step** is the dynamics rather than the logic: a trajectory-level billiard model
in which the collision is a joint closure of two causal diamonds
([`MultiParticle.py`](MultiParticle.py) already builds that interactor), which is where
timing and alignment error would finally become measurable instead of assumed away.

---

## 2026 update

TU Wien's 2026 one-dimensional rubidium gas carried energy and mass with diffusion practically absent:
a quantum Newton's cradle. It is this document's conservative logic in mechanical form. An equal-mass
elastic collision in one dimension swaps two velocities, so any run is a permutation (`run_perm`), the
velocity distribution never changes (`run_count`), every additive charge is conserved
(`run_conserved`) and each collision is an involution (`collide_involutive`), with nothing to pay for
([Discoveries_2026 §4](Discoveries_2026.md#p4)).

## References

- Fredkin, E. & Toffoli, T. (1982). *Conservative logic.* International Journal of
  Theoretical Physics **21**, 219–253.
- Fredkin, E. (1990). *Digital mechanics.* Physica D **45**, 254.
- Landauer, R. (1961). *Irreversibility and heat generation in the computing process.*
  IBM Journal of Research and Development **5**, 183–191.
- Bennett, C. H. (1973). *Logical reversibility of computation.* IBM Journal of Research
  and Development **17**, 525–532.
- Toffoli, T. (1980). *Reversible computing.* MIT LCS Tech Memo MIT/LCS/TM-151.
- Arndt, M. *et al.* (1999). *Wave–particle duality of C₆₀ molecules.* Nature **401**,
  680–682.

**Acknowledgement.** The idea of building Fredkin's machine on the QLF substrate is
Van Hovey's.

**In QLF.** [`Reversibility.md`](Reversibility.md) §7 carries the argument this file is the worked case
for — reversible theories are half-right, and Fredkin is the half they get right.
[`Chemistry.md`](Chemistry.md) is where helium's valence 0 comes from, which is why it can be a billiard
ball. [`Banach_Tarski_QLF.md`](Banach_Tarski_QLF.md) §4 lists `FANOUT`'s garbage line as the computational
costume of *no free duplication*. [`Related_Frameworks.md`](Related_Frameworks.md) places Fredkin among
the neighbours with a discrete substrate and no selection principle — the gap this file closes.
[`QuantumOS.md`](QuantumOS.md) cites him as a digital-physics ancestor.
[`Philosophy.md`](Philosophy.md) §3a is the counting method the 168-ball figure answers to.
[`lean/README.md`](lean/README.md) has the module's full theorem list, and
[`FlowChart.md`](FlowChart.md) places it on the map.
