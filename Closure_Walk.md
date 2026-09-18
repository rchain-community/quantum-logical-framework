# The Closure Walk — ZFA as a loop on `ℤ⁴`, and the half-spin sign it carries

**Status: exact computational** (counted, checked against fresh enumeration), with one identification
labelled *conjectural* and the physics readings marked as such.
Scripts: [`closure_walk.py`](closure_walk.py) (the counts, the checks, the edge-sign rule) and
[`doob_bridge.py`](doob_bridge.py) (the sampler); records [`data/closure_walk.json`](data/closure_walk.json),
[`data/doob_bridge.json`](data/doob_bridge.json).

## 0. What was learned, and why it matters

A ZFA closure — a count-balanced twist history — is **a closed walk on the four-dimensional lattice `ℤ⁴`**. The
eight twists are the eight unit vectors `±e_a`, one axis per conjugate pair (`^v`, `><`, `/\`, `+−`); the signed
action vector of a history is its position; count balance is *the walk is back at the origin*. Everything below
follows from taking that literally, and four things came out that were not known before:

1. **Selection has teeth only because the frame has more than two axes.** Pólya (1921): the simple walk returns
   to the origin with probability `1` in dimensions `1` and `2`, and with probability `< 1` in dimension `≥ 3`.
   So on a two-axis alphabet (`|Σ| = 4`, which [`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean) allows)
   *every* history would eventually close and `full_zeno_prune` would remove nothing of measure. On the eight-twist
   alphabet the walk is four-dimensional, transient, and the fraction of the uniform possibility measure that
   *ever* closes is Pólya's `p₄ = 0.19320` — measured here as the Kraft mass of the primes, `Σ_π 8^{−|π|}`, to six
   decimals. **The pruned tail has a definite size: 80.7 % of possibility never closes at all.** That the ZFA
   filter is a selection principle rather than a formality is a consequence of dimension, and the dimension is
   the one the alphabet forces. *(Exact mathematics; the physics reading — that this is why eight twists and not
   four — is an interpretation.)*

2. **The closure question lives on a 5-dimensional state, exactly.** Whether a partial history can close, in how
   many ways, and what the substrate does next depend only on `(x ∈ ℤ⁴, steps remaining)`: `h(x, t)` = ways to
   close from `x` in `t` steps. `/solve` is its argmax; the uniform sampler is its ratio; the drift is `−4x/t`.
   The `8^L`-dimensional possibility space is fibred over this low-dimensional base, and for closure the base is
   all there is. This is the low-dimensional view of the high-dimensional space — not an approximation, the
   equalizer of [`Category_Theory_QLF.md`](Category_Theory_QLF.md) with its geometry read off.

3. **The half-spin phase is not in the walk — it is a ℤ₂ connection on the walk's graph, and the closure phase
   is its holonomy.** Same endpoint, same multiset, different order, opposite sign: `^><v = +1`, `^>v< = −1`,
   `^>v<^>v< = +1` — one turn `−1`, two turns `+1`. §2 gives the edge rule and it reproduces the fold phase of all
   195,416 closures to length 8 with zero mismatches. So the walk is *count balance*; **spin-½ is the graph with the
   connection**. Sampling by ways is the classical shadow; the signed sum over holonomies is the quantum content.
   The worry that the census counts balance and not spin is exactly right about the walk and exactly answered by
   the connection.

4. **The constants are fixed, not fitted.** `W_L = (8/π²)·8^L/L²·(1 + O(1/L))`, a long closure returns to balance
   `≈ 1.48` times (bounded, by transience), and the number of closures of a given length is a polynomial factor
   `L^{−2}` times the total — the exponent is `d/2`, the dimension again.

And a correction: [`intermittency_bridge.py`](intermittency_bridge.py)'s "converged `M(∞) = 0.18267`" was a
partial sum truncated at `L = 22`; the limit is `p₄`.

## 1. The walk

| history | position on `ℤ⁴` |
|---|---|
| `^` / `v` | `±e₁` (Y) |
| `>` / `<` | `±e₂` (X) |
| `/` / `\` | `±e₃` (Z) |
| `+` / `−` | `±e₄` (gauge) |

A history is a lattice path from the origin; `calculate_action` is its endpoint; `max_excursion` is the largest
`ℓ¹`-distance `|x|₁` it reaches, so **a capacity-`R` horizon is the `ℓ¹` ball of radius `R`**
(`closedAtHorizon_iff_maxExcursion_le`). Closure is `x = 0`. Pauli closure adds nothing to *whether* it closes
(`count_balanced_pauli_closed`) — it decides the sign, §2.

**Counts, exact to `L = 1000`** ([`closure_walk.py`](closure_walk.py); `W_L` via the `ℤ² × ℤ²` split
`Σ_k C(L,k)·C(k,k/2)²·C(L−k,(L−k)/2)²`, primes by the Dyson recursion `I_L = W_L − Σ_{ℓ<L} I_ℓ W_{L−ℓ}`, all
three checked against every enumerated closure to `L = 8`):

| `L` | closures `W_L` | primes `I_L` | mean returns `F_L/W_L` | `W_L·L²/8^L` |
|---|---|---|---|---|
| 2 | 8 | 8 | 1.000 | — |
| 4 | 168 | 104 | 1.381 | — |
| 6 | 5,120 | 2,944 | 1.525 | — |
| 8 | 190,120 | 108,136 | 1.579 | — |
| 16 | 8.39e11 | 4.86e11 | 1.607 | — |
| 100 | 1.9e88 | 1.2e88 | 1.532 | 0.8025 |
| 200 | 8.37e175 | 5.31e175 | 1.511 | 0.8065 |
| 1000 | 9.96e896 | 6.44e896 | 1.488 | 0.8098 |

- `W_L·L²/8^L → 8/π² = 0.8106`: the return probability of the `d`-dimensional walk is `2(d/2πL)^{d/2}`, and
  `d = 4` gives `8/(π²L²)`.
- **`Σ_π 8^{−|π|} = p₄`.** Exact partial sum `M(1000) = 0.192939`; the tail is `a/L + b/L²` (first-return
  probability `~ L^{−2}`); a three-point fit through `L = 500, 750, 1000` gives **`0.1932015`** against Pólya's
  `0.1932017` (Finch, *Mathematical Constants* §5.9). Kill condition: any exact `M(L)` above `0.1932017`.
- **Mean returns `→ 1.4800`** (same fit); the bridge value `(1 + p₄)/(1 − p₄) = 1.4789` is within the fit's error
  but the sequence is still falling at `L = 1000` — *conjectural identification*.
- Primes are `I_L/W_L → 0.646` of closures: most closures are a single first return.

## 2. The connection — where spin-½ lives

The fold phase of a closure is *not* a function of its endpoint. The proven phase rule
(`QLF_PhaseRule`: `(−1)^{#neg} · (−1)^{inversions of the spatial axis word}`) depends on the order of the
letters. But it can be pushed onto the edges of the walk's graph. Adding a letter of spatial axis `a` adds one
inversion for every earlier letter of an axis ranked above `a`; the parity of the axis-`b` count so far equals
the parity of `x_b` (count = pos + neg, `x_b` = pos − neg); so the increment is a function of the **node**:

> **Edge-sign rule.** The directed edge `x → x + s·e_a` carries the sign
> `s · (−1)^{Σ_{b spatial, rank(b) > rank(a)} x_b}`, with spatial rank `X < Y < Z` and the gauge axis
> carrying no inversion sign (it commutes with everything).

The phase of a history is the product of its edge signs — its **holonomy**. Verified: `connection_phase` equals
`fold_phase` on all 195,416 closures to `L = 8`, zero mismatches (asserted on every run). The `s` factor is
`(−1)^{L/2}` on any closure, a global gauge; the content is the inversion sign, and its flux is:

| plaquette | loop | holonomy |
|---|---|---|
| two spatial axes | `^>v<` | **−1** |
| same two axes, other order | `^><v` | +1 |
| spatial × gauge | `^+v−` | +1 |
| the spatial plaquette twice | `^>v<^>v<` | +1 |

**π flux through every mixed spatial plaquette, none through gauge or same-axis plaquettes.** This is
anticommutation drawn on the lattice — the Clifford/Jordan–Wigner cocycle — and it is the half-spin: one turn
around a mixed loop is `−1`, two turns `+1` (`QLF_Spin`, the `SU(2) → SO(3)` double cover, now as a holonomy).
It is Wegner's `ℤ₂` lattice gauge theory, arrived at from the Pauli algebra rather than posited.

Consequences:

- **Balance ≠ spin.** The walk alone is the classical, unsigned census. Every "ways" count in this note is
  unsigned. The physical amplitude ([`Born_Rule.md`](Born_Rule.md)) is the *signed* sum over holonomies.
- **A signed `h` cannot drive a sampler** (it goes negative). That is the sign problem, and here it is the
  quantum/classical divide exactly: interference is what the unsigned walk cannot express.
- **The sufficient statistic for closure and phase together is `(x ∈ ℤ⁴, inversion parity ∈ ℤ₂)`** — four
  integers and one bit. That is the transfer state [`intermittency_bridge.py`](intermittency_bridge.py) already
  uses, and it is why its recursion is local.

## 3. The graph — specification

The directed vector graph of ZFA, at capacity `R`:

- **Nodes.** `(x, σ)` with `x ∈ ℤ⁴`, `|x|₁ ≤ R`, `σ ∈ ℤ₂` (inversion parity). `(2R+1)`-ish in each axis — the
  `ℓ¹` ball has `Σ_{k≤R} 2^k C(4,k) C(R, k)` lattice points (`1, 9, 41, 129, 321, …` for `R = 0…4`), times 2.
  The origin fibre `(0, σ)` is the closure set; `σ` at the origin is the closure phase up to the global
  `(−1)^{L/2}`.
- **Edges.** From every node, one directed edge per twist, `8` in all: `(x, σ) → (x + s·e_a, σ ⊕ ε)` where
  `ε = Σ_{b spatial, rank(b) > rank(a)} x_b mod 2` for spatial `a` and `ε = 0` for the gauge axis. Each edge carries
  the **vector** `s·e_a` and the **sign** `s·(−1)^ε`. Edges leaving the ball are absent (the horizon).
- **Time** is path length; the graph is the Cayley graph of `ℤ⁴` on the eight generators, twisted by the `ℤ₂`
  cocycle and cut at the horizon. It is not a DAG — it has loops — but every history is a directed path from the
  origin, and every closure a directed cycle through it.
- **Counts on the graph.** `h(x, t)` = number of directed paths of length `t` from `x` to the origin (closed form
  via the `ℤ²×ℤ²` split; the horizon version is the transfer recursion). The signed count `A(x, t)` = the same sum
  with each path weighted by its holonomy. `W_L = h(0, L)`; the first-return counts `I_L` are paths that avoid the
  origin until the end.
- **Dynamics on the graph.** `/solve` from `x` = the path to the origin minimising the peak `|x|₁`, then length,
  then phase `+1`, then lex. The uniform sampler = step to neighbour `y` with probability `h(y, t−1)/h(x, t)`
  (Doob's h-transform); the prime sampler = the same with the origin made taboo until the last step.
- **Readings.** Nodes are positions of *free action* (`|x|₁` is the total free action, `local_free_action`); the
  ball is the capacity; a directed cycle is an event; its holonomy is its spin phase; the flux through a
  plaquette is anticommutation. Nothing on the graph is an observer.

**Built, checked and rendered** — [`closure_graph.py`](closure_graph.py) → [`closure_graph.html`](closure_graph.html)
([live](https://rchain-community.github.io/quantum-logical-framework/closure_graph.html); self-contained canvas,
drag to rotate, hover a node for `h(x,t)`) and [`data/closure_graph_R3.json`](data/closure_graph_R3.json). At
`R = 3`: **129 nodes, 528 directed edges** (264 undirected, 56 carrying connection `−1`), **168 plaquettes of
which exactly the 84 spanned by two spatial axes carry π flux**, double cover 258 nodes / 1056 edges. Asserted on
the built graph: the ball sizes `9, 41, 129, 321` for `R = 1…4`; the connection sign is direction-independent
(the twist sign is the direction); every plaquette holonomy is `−1` iff both axes are spatial; and **walking the
graph reproduces the census** — closed walks at the origin number `8, 168, 5120` for `t = 2, 4, 6` (`W_t`), and
with edges weighted by their signs the closed-walk sum is `−8, 120, −2144`, the signed census `Σ phase` exactly
(the `|A_L| = 8 → 120 → 2144` of [`Perturbation_Theory_QLF.md`](Perturbation_Theory_QLF.md), now as a matrix
power on a 129-node graph). So the graph carries both the count and the spin phase, and the signed amplitude of
[`Born_Rule.md`](Born_Rule.md) is a walk on it. The gauge axis is drawn as a skew fourth direction; its edges are
dashed and never carry `−1`.

## 4. The sampler

[`doob_bridge.py`](doob_bridge.py) — at position `x` with `t` steps left, take twist `e` with probability
`h(x+e, t−1)/h(x, t)`. The step probabilities telescope to `h(0,0)/h(0,L) = 1/W_L`, so the sampler is **uniform
over the closures by construction**; the run asserts that for every sample the product of its step probabilities
is exactly `1/W_L` (rationals — no float touches the choice). Checks:

- 20,000 samples at `L = 6` against the enumerated census: strata (excursion × prime/composite × phase)
  `χ² = 0.6` on 6 dof; per-closure `χ² = 5210` on 5119 dof.
- Sample mean of returns `1.629 ± 0.028` / `1.570 ± 0.043` / `1.450 ± 0.050` at `L = 20 / 50 / 100` against the
  exact `1.601 / 1.561 / 1.532`.
- The discrete drift `½·log(h(x+e_a)/h(x−e_a))` at `x = (5,2,0,1)`, `t = 100` is `(−0.200, −0.080, 0, −0.040)`,
  the Gaussian `−4x_i/t` exactly (per-axis variance `t/4`).
- **Primes only:** with the taboo count `f(x,t)` (first arrival at the origin at step `t`, read off
  `h(x,t) = Σ_s f(x,s)·W_{t−s}`) the same bridge is uniform over the `I_L` primes and telescopes to `1/I_L`
  exactly — checked at `L = 4…50`; 20,000 samples at `L = 6` against the 2,944 enumerated primes give strata
  `χ² = 6.3` on 3 dof and per-prime `χ² = 2959` on 2943 dof (sd 77). Primes sit slightly deeper than closures at
  large (mean `|x|₁` peak `11.84` vs `11.41` at `L = 100`). Filtering the closure sampler would have wasted
  `1 − I_L/W_L ≈ 38 %` of draws; the taboo bridge wastes none.
- Rejection (random strings kept if they close) needs `π²L²/8` strings per closure — 12,500 at `L = 100`. The bridge
  never rejects, and every sample is Pauli-closed for free.

The sampler is the exact, unlearned generative model of the *unsigned* census. It is a tool — census members at
any length, primes on demand — and a statement: what a diffusion model estimates from data is, for this
distribution, a binomial count.

## 5. What is *not* established

- Whether the walk's dimension (`4`) being what makes selection non-trivial is *why* the alphabet has eight
  letters is an interpretation; the alphabet count is forced by other means (`QLF_AlphabetNecessity`).
- The mean-returns limit `(1 + p₄)/(1 − p₄)` is conjectural (one digit short).
- The signed count `A(x, t)` on the graph — the quantum content — is defined here but not computed at scale; the
  signed census results are in [`Born_Rule.md`](Born_Rule.md) and [`contextual_census.py`](contextual_census.py).
- Nothing here is Lean. The natural anchors: the edge-sign rule as a restatement of `phase_rule` (it is the same
  rule with the inversion count made node-local — a short proof), and the `ℤ²×ℤ²` count as `balanced_history_count`.

## 6. Provenance

Grew out of asking whether ZFA could compress data: a closure of length `L` needs `3L − 2·log₂L − 0.3` bits,
i.e. is incompressible to leading order — which is *this* result (`W_L ≈ (8/π²)8^L/L²`) read as a rate. The
compression framing was dropped; the walk, its constants, the connection and the graph are what it found.
[`Shannon_Overfit.md`](Shannon_Overfit.md) §5c has the prime-as-incompressible-generator reading.
