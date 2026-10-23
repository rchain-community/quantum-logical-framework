# Bra-Ket Notation and RhoQuCalc

Standard quantum mechanics uses Dirac's bra-ket notation to describe states and operators. RhoQuCalc (the ρ-process algebra at the core of QLF) makes the same concepts algebraic and type-safe. This document maps each bra-ket idea to its exact RhoQuCalc counterpart and explains why the correspondence is deeper than a surface analogy.

**Executable demonstration:** [`braket_rho.py`](braket_rho.py) runs all of these identities numerically and checks them.

Here is the exact terminal input and output of the running `braket_rho.py` validation sandbox:

python braket_rho.py -repl

### Application 1: QuantumOS Virtualization & Register Isolation

```text
braket> H |0><0| H†

====================================================================
   Bra-Ket Balance Validator
====================================================================
  input      : H |0><0| H†
  normalized : H |0><0| H†
  tokens     : ['H', '|0>', '<0|', 'H†']
  bras       : 1
  kets       : 1
  operators  : 2
  well-typed : ✓
  result     : operator
  closed     : ✓
  QLF-safe   : ✓
  evaluation : 
[[0.5+0.j 0.5+0.j]
 [0.5+0.j 0.5+0.j]]
(Operator / Density Matrix)
====================================================================

```

### Application 2: Hardware-Locked Cryptography & No-Cloning Enforcement

```text
braket> <0| <1|

====================================================================
   Bra-Ket Balance Validator
====================================================================
  input      : <0| <1|
  normalized : <0| <1|
  tokens     : ['<0|', '<1|']
  bras       : 2
  kets       : 0
  operators  : 0
  well-typed : ✗
  result     : invalid
  closed     : ✗
  QLF-safe   : ✗
  note       : invalid multiplication: B followed by B
====================================================================

```

### Application 3: Active Inference Error Correction Sync

```text
braket> <0|σz|0>

====================================================================
   Bra-Ket Balance Validator
====================================================================
  input      : <0|σz|0>
  normalized : <0|σz|0>
  tokens     : ['<0|', 'σz', '|0>']
  bras       : 1
  kets       : 1
  operators  : 1
  well-typed : ✓
  result     : scalar
  closed     : ✓
  QLF-safe   : ✓
  evaluation : (1+0j) (Scalar Probability Amplitude)
====================================================================

```

## The Key Shift: Density Matrix Picture

Standard bra-ket introduces two kinds of objects:
- **Ket** `|ψ⟩` — a column vector (the state)
- **Bra** `⟨ψ|` — its conjugate transpose (a row vector)

RhoQuCalc works in the **density matrix (Heisenberg) picture** instead. A qubit state `|ψ⟩` is represented by its **density matrix** `ρ_ψ = |ψ⟩⟨ψ|`, which is a 2×2 Hermitian matrix. This is the standard representation for mixed states, open systems, and operator algebras — and it is what `Form.toMatrix` produces.

The `Form` structure parametrizes the space of all 2×2 Hermitian matrices via the Pauli basis:

```
Form(t, x, y, z).toMatrix = t·I + x·σx + y·σy + z·σz
                           = [[t+z,  x-iy],
                              [x+iy, t-z ]]
```

Every 2×2 Hermitian matrix has exactly this form. Pure qubit states on the Bloch sphere are the special case `Form(t=½, x, y, z)` with `x² + y² + z² = ¼`:

| State | Form parameters | Matrix |
|---|---|---|
| `\|0⟩⟨0\|` | `{t=½, x=0, y=0, z=½}` | `[[1,0],[0,0]]` |
| `\|1⟩⟨1\|` | `{t=½, x=0, y=0, z=-½}` | `[[0,0],[0,1]]` |
| `\|+⟩⟨+\|` | `{t=½, x=½, y=0, z=0}` | `[[½,½],[½,½]]` |
| `\|-⟩⟨-\|` | `{t=½, x=-½, y=0, z=0}` | `[[½,-½],[-½,½]]` |
| `σx` | `{t=0, x=1, y=0, z=0}` | `[[0,1],[1,0]]` |
| `σy` | `{t=0, x=0, y=1, z=0}` | `[[0,-i],[i,0]]` |
| `σz` | `{t=0, x=0, y=0, z=1}` | `[[1,0],[0,-1]]` |

---

## The Correspondence Table

| Bra-ket concept | RhoProcess | eval |
|---|---|---|
| State `\|ψ⟩` (ket direction) | `action (Form ψ)` | `ρ_ψ = \|ψ⟩⟨ψ\|` |
| Adjoint `⟨ψ\|` (bra direction) | `lift (Form ψ)` | `ρ_ψ† = ρ_ψ` (Hermitian) |
| Superposition `\|ψ⟩ + \|φ⟩` | `parallel (action ψ) (action φ)` | `ρ_ψ + ρ_φ` |
| Composition `A · B` | `sequence (action A) (action B)` | `A.toMatrix * B.toMatrix` |
| Apply observable: `A\|ψ⟩` | `sequence (action A) (action ψ)` | `A.toMatrix * ρ_ψ` |
| Expectation `⟨ψ\|A\|ψ⟩` | `Tr(sequence (action A) (action ψ))` | `Tr(A · ρ_ψ)` |
| Unitary evolution `U ρ U†` | `sequence (action U) (sequence (action ρ) (lift U))` | `U · ρ · U†` |
| Adjoint `A†` | `dagger (action A)` | `A.toMatrix†` |
| Null process | `zero` | `0` |

---

## action and lift: ket and bra directions

```lean
action f   →  eval = f.toMatrix          topoString [pos, neg]   -- ket: outgoing
lift f     →  eval = f.toMatrix†         topoString [neg, pos]   -- bra: incoming
```

The `eval` values are equal — because `Form.toMatrix_adjoint` proves `f.toMatrix† = f.toMatrix` (Hermitian). But the **topoStrings are opposite**. This is the key:

- `action` encodes an **outgoing** (ket-direction) event: it contributes `[pos, neg]` to the topological string — a positive phase followed by a negative phase
- `lift` encodes an **incoming** (bra-direction) event: it contributes `[neg, pos]` — a negative phase followed by a positive phase

The matrix content is the same (Hermitian matrices are self-adjoint); the topological direction distinguishes ket from bra.

---

## ZFA Balance = Bra-Ket Balance

In a well-formed bra-ket expression, every ket `|ψ⟩` must eventually be paired with a bra `⟨φ|` — otherwise the expression has wrong type (you can't have an uncontracted ket in a scalar or operator result).

In RhoQuCalc, this is **automatic and unconditional**:

```
action f  →  topoString [+, -]  →  count_pos = 1, count_neg = 1
lift f    →  topoString [-, +]  →  count_pos = 1, count_neg = 1
parallel p q  →  topo(p) ++ topo(q)   →  sums preserve balance
sequence p q  →  topo(p) ++ topo(q)   →  sums preserve balance
```

Every `RhoProcess`, no matter how composed, has `count_pos = count_neg` in its topoString. The Lean theorem `rho_process_always_zfa` proves this unconditionally:

```lean
theorem rho_process_always_zfa (p : RhoProcess) : achieves_ZFA (toTopoString p)
```

There is **no way to build a ZFA-unbalanced process** in the calculus. The type system prevents unmatched kets. This is the topological encoding of bra-ket well-typedness.

---

## sequence = Matrix Multiplication = Composition

`sequence p q` evaluates to `p.eval * q.eval` (matrix multiplication). This covers:

**Projector idempotency** (`ρ² = ρ` for pure states):
```
sequence (lift ψ) (action ψ)  →  ρ_ψ * ρ_ψ = ρ_ψ
```

**Orthogonality** (`ρ_ψ · ρ_φ = 0` iff `⟨ψ|φ⟩ = 0`):
```
sequence (lift ψ) (action φ)  →  ρ_ψ * ρ_φ = 0   (for orthogonal ψ, φ)
```

**Overlap** (Tr gives `|⟨ψ|φ⟩|²`):
```
Tr(sequence (lift ψ) (action φ))  =  |⟨ψ|φ⟩|²
```

**Operator application** (`A|ψ⟩⟨ψ|`):
```
sequence (action A) (action ψ)  →  A.toMatrix * ρ_ψ
Tr of above = ⟨ψ|A|ψ⟩
```

**Unitary evolution** (`U ρ U†`):
```
sequence (action U) (sequence (action ρ) (lift U))
  →  U.toMatrix * ρ * U.toMatrix†
```

Verified numerically: `H |0⟩⟨0| H† = |+⟩⟨+|` and `σx |0⟩⟨0| σx† = |1⟩⟨1|`.

---

## parallel = Superposition / Completeness

`parallel p q` evaluates to `p.eval + q.eval` (matrix addition). For states this is:

```
parallel (action ψ) (action φ)  →  ρ_ψ + ρ_φ
```

The completeness relations follow immediately:
```
parallel (action |0⟩) (action |1⟩)  →  |0⟩⟨0| + |1⟩⟨1| = I
parallel (action |+⟩) (action |-⟩)  →  |+⟩⟨+| + |-⟩⟨-| = I
parallel (action |R⟩) (action |L⟩)  →  |R⟩⟨R| + |L⟩⟨L| = I
```

Any orthonormal basis `{|e_i⟩}` satisfies `Σ |e_i⟩⟨e_i| = I` — in RhoQuCalc this is `parallel` over all basis actions.

---

## dagger = Adjoint Involution

```lean
theorem eval_dagger (p : RhoProcess) : eval (dagger p) = (eval p).conjTranspose
```

The involution rules mirror quantum mechanics exactly:
```
dagger (action f)       = lift f              -- ket → bra
dagger (lift f)         = action f            -- bra → ket
dagger (sequence p q)   = sequence (dagger q) (dagger p)  -- (AB)† = B†A†
dagger (parallel p q)   = parallel (dagger p) (dagger q)  -- (A+B)† = A†+B†
```

For a Hermitian Form: `dagger (action f)` and `lift f` have the same `eval` — because `f.toMatrix† = f.toMatrix`.

---

## Pauli Algebra via sequence

The Pauli algebra `σi σj = δij I + i εijk σk` is just matrix multiplication, which is `sequence` in RhoQuCalc:

```
sequence (action σx) (action σx)  →  σx² = I
sequence (action σx) (action σy)  →  σx σy = i σz
sequence (action σy) (action σz)  →  σy σz = i σx
sequence (action σz) (action σx)  →  σz σx = i σy
```

All verified numerically in `braket_rho.py`.

---

## The ρ-Calculus Connection

The deeper motivation for `action`/`lift` comes from the ρ-calculus (Meredith & Radestock 2005). In ρ-calculus:
- `x!(P)` — output on channel `x` (send process `P`) → **ket direction**: outgoing
- `x?(y).Q` — input on channel `x` (receive into `y`, continue as `Q`) → **bra direction**: incoming

`action f` is an output process: it sends the logical Form `f` into the environment. `lift f` is an input process: it receives and conjugates. `sequence (lift f) (action g)` is a **synchronization** — a channel handshake where bra receives what ket sent.

ZFA balance is the condition that every output (ket/action) is matched by a corresponding input (bra/lift) — the process-algebraic version of bra-ket well-typedness. `rho_process_always_zfa` proves the QLF type system enforces this at the level of the logical structure, not as a runtime check.

---

## Summary

RhoQuCalc is bra-ket notation made algebraic, constructive, and type-safe:

| | Bra-ket | RhoQuCalc |
|---|---|---|
| **Picture** | State vector (Schrödinger) | Density matrix (Heisenberg) |
| **Ket** | `\|ψ⟩` column vector | `action (Form ψ)` |
| **Bra** | `⟨ψ\|` row vector | `lift (Form ψ)` |
| **Superposition** | `\|ψ⟩ + \|φ⟩` | `parallel` |
| **Composition** | `AB` matrix product | `sequence` |
| **Adjoint** | `†` | `dagger` |
| **Well-typedness** | Matching bras and kets | ZFA balance (`achieves_ZFA`) |
| **Enforcement** | Type inference (informal) | `rho_process_always_zfa` (machine-verified) |

The formal proof `rho_process_always_zfa` is not just a restatement of bra-ket conventions — it is the machine-verified claim that the QLF type system cannot represent a physically ill-typed quantum expression.

See also: [Hermitian_Conjugacy_Proof.md](Hermitian_Conjugacy_Proof.md) — constructive proof that ZFA closure enforces unitarity; `Form.toMatrix_adjoint` is the formal bridge.

The variational physics foundation underlying this correspondence is covered in [Lagrangian_Formulation.md](Lagrangian_Formulation.md): ZFA balance (`achieves_ZFA`) is the discrete form of S = ∫ℒ dΩ with ℒ = 0, and the security conditions `[H, ρ_S] = 0`, Tr(ρ_S ρ_E) = 0 are grounded there in `rho_process_always_symmetric` and `orthogonality_01`.

---

## Live Evaluation: quantum-os `/braket` command

The [quantum-os](https://github.com/rhovision-org/quantum-os) browser app implements these evaluations live. After connecting, type in the chat input:

**`/braket +`** — evaluates `action(Form_+)`, shows the density matrix of `|+⟩`:

```
ket: |+⟩
  RhoProcess: action(Form_+)
  eval = Form.toMatrix:
  ⎡ 0.5  0.5 ⎤
  ⎣ 0.5  0.5 ⎦
bra: ⟨+|  (eval = ket†  =  ket  [Hermitian: Form.toMatrix_adjoint ✓])
  ZFA: action [+,−]  lift [−,+]  both balanced: ✓
  bra_ket_always_balanced: ✓ (BraKetRhoQuCalc.lean)
```

This matches the table entry `|+⟩⟨+|` = `[[½,½],[½,½]]` exactly.

**`/braket 0 1`** — evaluates `parallel(action(Form_0), action(Form_1))`, the completeness relation:

```
ket: |0⟩ + |1⟩
  RhoProcess: parallel(action(Form_0), action(Form_1))
  eval = Form.toMatrix:
  ⎡ 1  0 ⎤
  ⎣ 0  1 ⎦
bra: ⟨0| + ⟨1|  (eval = ket†  =  ket  [Hermitian: Form.toMatrix_adjoint ✓])
  ZFA: action [+,−]  lift [−,+]  both balanced: ✓
  bra_ket_always_balanced: ✓ (BraKetRhoQuCalc.lean)
```

`|0⟩⟨0| + |1⟩⟨1| = I` — the identity matrix, confirming `{|0⟩, |1⟩}` is a complete orthonormal basis. States supported: `0`, `1`, `+`, `-`, `i`, `-i`. Open the app at **https://rhovision-org.github.io/quantum-os/** and type `/help` for the full command list.
