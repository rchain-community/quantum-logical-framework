# QuCalc and RhoQuCalc

QuCalc is the discrete logical language of the Quantum Logical Framework.  
RhoQuCalc is its process-calculus extension.

QuCalc defines the **8-twist relational alphabet** and the rule that persistent structures arise only through **Zero Free Action (ZFA)**.  
RhoQuCalc adds **cataloged closures**, **parallel composition**, **replication**, and a **RhoLang-style executable surface syntax** for building larger systems from verified ZFA components.

Together they provide both:

1. a **local quantum-logical algebra** of context-relative twists, and  
2. a **compositional process layer** for assembling multi-particle, entangled, and circuit-like systems.

**Code and proofs.** The runtime engine is [`twist_core.py`](twist_core.py) (reference: [`twist_core.md`](twist_core.md)), with [`QuCalc.py`](QuCalc.py) as the legacy-compatible interface over it. The machine-verified core is [`lean/QLF_QuCalc.lean`](lean/QLF_QuCalc.lean) (the generation engine and the ZFA filter `full_zeno_prune`) and [`lean/RhoQuCalc.lean`](lean/RhoQuCalc.lean) (the process algebra; see [`BraKetRhoQuCalc.md`](BraKetRhoQuCalc.md)).

---

## 1. The Core Claim

There are no absolute directions, no pre-given coordinate grid, and no background time in QuCalc.  
There are only local distinctions expressed as twists relative to context.

A QuCalc expression is not a number.  
It is a **history string** or an open prefix of one.

A history persists only if it closes with **Zero Free Action**.  
A process becomes physically admissible only when its unresolved distinctions are balanced by a valid closure.

This remains the core of the framework.

What has changed is that QuCalc is supported by a higher layer: **RhoQuCalc**.

---

## 2. The 8-Twist Alphabet

QuCalc uses four paired distinction operators:

- `^` and `v` — vertical distinction pair
- `<` and `>` — horizontal distinction pair
- `/` and `\` — depth distinction pair
- `+` and `-` — contextual or gauge distinction pair

These symbols do **not** denote absolute geometric axes.  
They denote **local directions relative to the current fold context**.

Their meaning is relational:

- `^` is only meaningful relative to `v`
- `<` is only meaningful relative to `>`
- `/` is only meaningful relative to `\`
- `+` is only meaningful relative to `-`

The symbols `+` and `-` are especially important. They should not be read as literal clock time coordinates. They represent contextual alternatives, gauge resolution, or branch-relative distinctions within a local history.

---

## 3. History Strings

A QuCalc expression unfolds as a history string.

Examples:

- `^`
- `^<`
- `^/+`
- `^>v<`
- `^>/+v<\-`

A history string is a sequence of local twists.  
It may be:

- an **open prefix**, still carrying free action, or
- a **closed history**, satisfying ZFA.

In QuCalc, persistence is not assumed. It is achieved.

---

## 4. Zero Free Action

The central rule of QuCalc is:

> A history persists only if its net free action closes to zero.

In the simplest counting form:

- `^` balances `v`
- `<` balances `>`
- `/` balances `\`
- `+` balances `-`

But QuCalc requires more than simple cancellation by count.

A valid history must also satisfy **structural closure**.  
That is, it must close as an admissible relational fold, not merely as an accidental tally.

So ZFA means:

1. local distinctions are balanced,
2. the history closes coherently,
3. the resulting string can function as a stable event or reusable closure.

---

## 5. Hermitian Closure

A central QuCalc operation is closure by conjugation.

If `E` is a history string, then its Hermitian conjugate `E†` is formed by reversing the history and complementing each twist:

- `^ ↔ v`
- `< ↔ >`
- `/ ↔ \`
- `+ ↔ -`

A process is structurally complete when its history and conjugate closure annihilate free action.

This is why QuCalc treats persistence as a closure property rather than as an externally imposed law.

---

## 6. Minimal and Composite Closures

The engine now explicitly supports named ZFA closures.

Examples include:

- `ELECTRON = ^<v>` (the fundamental fluxoid — one ZFA loop = minimum action)
- `POSITRON = ^>v<`
- `PHOTON = +-`
- `NEUTRINO = ^+v-`
- `POSITRONIUM = ^<v>^>v<`
- `MUONIUM = ^<v>^>v</\`
- `HYDROGEN = ^<v>^>v</\+-`

These named closures are no longer merely examples in prose.  
They are cataloged and callable through the engine.

This is the key bridge to RhoQuCalc.

---

## 7. What RhoQuCalc Adds

RhoQuCalc extends QuCalc from a history language into a compositional process language.

It adds four practical ideas:

### 7.1 Cataloged Closure

Verified ZFA histories can be registered once and reused by name.

This is handled through the **ZfaCatalog**.

Instead of rediscovering a closure from scratch every time, the engine can retrieve a known admissible ZFA form and apply it compositionally.

### 7.2 ApplyZfa

A process can append a verified closure to an open prefix.

Conceptually:

```text
ApplyZfa(prefix, "POSITRON")
```

This means: take the current open history and compose it with a named verified closure.

This does not replace QuCalc.  
It accelerates and modularizes it.

### 7.3 Parallel Composition

RhoQuCalc supports a process-style parallel operator:

```text
P | Q
```

This means independent histories may be evaluated concurrently as part of the same possibilist computation.

In engine terms, parallel histories are represented as a list of processes and simulated together.

### 7.4 Replication

RhoQuCalc supports replication:

```text
*P
```

This means repeated identical processes or reusable process spawning.

In engine terms, replication expands one history into multiple copies for multi-particle or repeated-process scenarios.

---

## 8. The Engine Structure

The implementation has three distinct layers:

### 8.1 QuCalc Core

The core engine still searches for ZFA closure of open prefixes by constrained branching over the 8 twists.

Its job is:

- start with a prefix,
- branch over admissible next twists,
- reject trivial immediate reversals,
- return the shortest admissible ZFA closure when one is found.

### 8.2 ZfaCatalog

The catalog stores named verified closures.

This turns QuCalc from pure search into reusable constructive composition.

A closure can now be:

- discovered by search,
- named,
- reused compositionally.

### 8.3 PossibilistEngine

The wrapper layer exposes Rho-style process operations:

- `ApplyZfa`
- parallel composition
- replication
- simulation of multiple processes

This is the practical RhoQuCalc layer.

---

## 9. The RhoQuCalc Syntax Layer

A RhoQuCalc transpiler provides a simple RhoLang-style executable notation.

Supported forms currently include:

- `new x1, x2 in P`
- `P | Q`
- `*P`
- `ApplyZfa(prefix, name)`
- simple output forms
- simple input guards as stubs
- `ZFA_...` closure registration

This is not yet full Rholang.  
It is a restricted but useful process notation that compiles into Python using the PossibilistEngine.

So the current architecture is:

```text
RhoQuCalc syntax
      ↓
rho_transpiler.py
      ↓
PossibilistEngine
      ↓
QuCalc core + ZfaCatalog
      ↓
ZFA discovery / composition / simulation
```

---

## 10. Path Integrals in RhoQuCalc

The path-integral module is RhoQuCalc-aware.

It no longer assumes a single prefix only.  
It can now process:

- one history string,
- a list of parallel histories,
- replicated process collections,
- transpiled RhoQuCalc code

This is important because it shifts the framework from single-history reasoning to **structured multiplicity**.

Instead of merely asking whether one prefix closes, the engine can count closure behavior over a process ensemble.

---

## 11. Meaning of Entanglement in This Framework

With RhoQuCalc support, entanglement is best understood not as spooky action at a distance but as **joint closure within a shared context**.

Two or more processes may remain admissible only if their combined history resolves to a valid ZFA structure.

This makes the process language important: it lets QuCalc describe systems of interacting closures rather than isolated strings only.

---

## 12. Working Definitions

### QuCalc

> QuCalc is the 8-twist relational calculus of context-relative history strings whose persistent structures arise from a single closure principle — Zero Free Action — whose two algebraic faces (Pauli closure on the non-abelian side, count balance / Hermitian-pair multiset on the abelian side) jointly define admissibility.

### RhoQuCalc

> RhoQuCalc is the process-calculus extension of QuCalc, adding cataloged ZFA reuse, compositional closure application, parallel composition, replication, and executable RhoLang-style syntax.

### QLF Implementation View

> QuCalc provides the local algebra.  
> RhoQuCalc provides the compositional execution layer.

---

## 13. Minimal Examples

### 13.1 A basic closed history

```text
^>v<
```

This is a minimal spatial ZFA loop.

### 13.2 Applying a named closure

```text
ApplyZfa("^>", "POSITRON")
```

This composes an open prefix with a cataloged closure.

### 13.3 Parallel composition

```text
ApplyZfa(a, "ELECTRON") | ApplyZfa(b, "ELECTRON")
```

This expresses two independent but concurrent closure processes.

### 13.4 Replication

```text
*ApplyZfa(particle, "ELECTRON")
```

This expresses repeated spawning or reuse of a closure process.

---

## 14. What This Clarifies

This document replaces the older picture in which QuCalc appeared to be only a discrete twist engine.

That is still true at the core.  
But the repository supports a stronger formulation:

- QuCalc is the base relational twist algebra.
- RhoQuCalc is the compositional process layer built on top of it.
- ZFA closures are reusable named objects, not only discovered endpoints.
- Multi-process and replicated systems are first-class citizens of the framework.

So QuCalc should now be understood in two tiers:

1. **QuCalc proper** — local history logic in the 8-twist algebra  
2. **RhoQuCalc** — process-level composition over named ZFA closures

---

## 15. Current Scope

This repository has real support for RhoQuCalc, but the language is still in an early constructive stage.

What exists now is enough to support:

- reusable ZFA catalogs
- process composition
- parallel simulations
- replicated process ensembles
- simple transpilation from Rho-style notation

What remains to be strengthened includes:

- richer name semantics
- true communication semantics
- more complete Rho input/output behavior
- tighter mathematical formalization of closure composition

---

## 16. Final Statement

QuCalc is no longer only a language for describing individual twist histories.

With RhoQuCalc support, it becomes a language for building systems of histories from reusable ZFA components.

That is the decisive change.

The framework treats a stable closure not only as the end of a search, but as a named constructive unit in a larger possibilist process algebra.

See also: [zfa-catalog-rho-notation.md](zfa-catalog-rho-notation.md) — pre-verified ZFA closure catalog in RhoLang notation; orders-of-magnitude speedup by reusing named closures instead of re-running BFS.
