# Data Compression in QLF — the theory is here, the codec is not

**Status: exact computational (counted), with one identification labelled conjectural.**
Scripts: [`compression_census.py`](compression_census.py) (§2–§5) and [`doob_bridge.py`](doob_bridge.py) (§6); records: [`data/compression_census.json`](data/compression_census.json), [`data/doob_bridge.json`](data/doob_bridge.json).
Companion: [`Shannon_Overfit.md`](Shannon_Overfit.md) §5c (why `K_C` is a boundary object, not a primitive).

QLF does not compress files. What it holds is the *theory* every lossless compressor rests on, machine-verified
in the places that matter — Kraft's inequality (`twist_kraft`, [`QLF_KraftMeasure`](lean/QLF_KraftMeasure.lean)),
Shannon entropy from counts ([`QLF_ShannonFromCounts`](lean/QLF_ShannonFromCounts.lean)), Landauer's `ΔF = −log 2`
per many-to-one closure ([`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean)), and unique factorization of every closure
into primes (`decomposes_into_primes`, `irreducibility_invariant_is_dyson`). This note turns that theory into a
measurement on the substrate's own object: **how many bits does a ZFA closure need**, against the raw
`3 bits/twist` of the eight-letter alphabet?

The answer is *very few fewer than raw* — and the reason is a piece of classical mathematics the census walks
straight into.

## 1. Three codes

| Code | Knows | Cost | Lean anchor |
|---|---|---|---|
| **Enumerative** (block) | the length `L` and the count `W_L` | `log₂ W_L` bits per closure — the Shannon floor for the set | `QLF_ShannonFromCounts`, `balanced_history_count` |
| **Cylinder-prime** (streaming) | nothing in advance | factor into primes; each prime `π` costs `3|π| + log₂ M`, `M = Σ_π 8^{−|π|}` | `twist_kraft` (prefix-free), `decomposes_into_primes` (unique) |
| **Seed + `/solve`** (generative) | the substrate's selection rule | store `k` twists of a prime, regenerate the rest by `qucalc_search.solve` | the `/solve` cascade (least excursion → shortest → phase `+1` → lex) |

The first is the floor; the second is what a stateless encoder that only knows the substrate measure can do; the
third stores only what the substrate would *not* have chosen on its own.

## 2. What the census measured

**Counted layer, exact integers to `L = 1000`** (`W_L` from `balanced_history_count`; primes `I_L` from the Dyson
recursion `I_L = W_L − Σ_{ℓ<L} I_ℓ W_{L−ℓ}`, i.e. `G·(1 − I) = 1`; the mean number of prime factors from
`F_L = Σ_ℓ I_ℓ (W_{L−ℓ} + F_{L−ℓ})`). All three were checked against fresh enumeration of every closure to
`L = 8` (195,416 closures: factors concatenate back, every factor is prime and Pauli-closed, prime counts equal
`8, 104, 2944, 108136`, factor totals equal `F_L`).

| `L` | closures `W_L` | primes `I_L` | mean factors | enumerative bits/twist | cylinder-prime bits/twist |
|---|---|---|---|---|---|
| 2 | 8 | 8 | 1.000 | 1.500 | 1.814 |
| 4 | 168 | 104 | 1.381 | 1.848 | 2.181 |
| 6 | 5,120 | 2,944 | 1.525 | 2.054 | 2.397 |
| 8 | 190,120 | 108,136 | 1.579 | 2.192 | 2.532 |
| 16 | 8.39e11 | 4.86e11 | 1.607 | 2.476 | 2.762 |
| 32 | 6.08e25 | 3.64e25 | 1.582 | 2.677 | 2.883 |
| 64 | 1.22e54 | 7.52e53 | 1.549 | 2.807 | 2.943 |
| 128 | 1.93e111 | 1.21e111 | 1.523 | 2.888 | 2.972 |
| 200 | 8.37e175 | 5.31e175 | 1.511 | 2.922 | 2.982 |
| 1000 | 9.96e896 | 6.44e896 | 1.488 | 2.980 | 2.996 |

Both rates climb toward `3`. **Compression from ZFA closure vanishes per twist.**

**Generative layer, every prime to `L = 6`** (3,056 primes × every seed length, 2.5 min):

| `L` | primes | least seed `k` that regenerates the prime | mean `k/L` | bits/twist | prime floor `log₂ I_L / L` |
|---|---|---|---|---|---|
| 2 | 8 | `k=1`: 8 | 0.500 | 1.500 | 1.500 |
| 4 | 104 | `k=2`: 56 · `k=3`: 48 | 0.615 | 1.846 | 1.675 |
| 6 | 2,944 | `k=3`: 344 · `k=4`: 1,256 · `k=5`: 1,344 | 0.723 | 2.170 | 1.921 |

Reconstructibility is monotone in the seed (0 primes reconstructible from a short seed and not from a longer one).
The last twist is always forced by balance, so `k ≤ L−1` for every prime; **54 % of length-6 primes are the
substrate's own pick from two twists short, 12 % from three** (`'+++'` → `+++---`). The generative code sits
above the enumerative floor, as it must — the seed has to be spelled out at `3 bits/twist` and the primes the
cascade does not choose gain nothing.

## 3. Why so little — the census is a Pólya walk

A count-balanced history is a closed walk of the simple random walk on `ℤ⁴` (one axis per conjugate pair; the
gauge pair `+/−` is the fourth). That single identification explains every number above:

- **`W_L ≈ (8/π²)·8^L / L²`.** The return probability of the `d`-dimensional simple walk at time `L` is
  `2 (d/2πL)^{d/2}`; at `d = 4` that is `8/(π² L²)`. Measured: `W_L·L²/8^L = 0.8098` at `L = 1000`, against
  `8/π² = 0.8106` (the `1/L` correction accounts for the rest). So a length-`L` closure is compressible by exactly
  **`2·log₂ L − log₂(8/π²)` bits in total** — logarithmic, not linear. Count balance is four integer
  constraints; the information they remove is `O(log L)`. Nothing about ZFA is a low-entropy source.

- **The prime Kraft mass is Pólya's return probability.** `Σ_π 8^{−|π|}` is, letter for letter, the probability
  that the `ℤ⁴` walk ever returns to the origin. Exact partial sum `M(1000) = 0.192939`; the tail decays as
  `a/L + b/L²` (first-return probability `~ L^{−2}`), and a three-point fit through `L = 500, 750, 1000` gives
  **`M(∞) = 0.1932015`**, against Pólya's `p₄ = 0.1932017` (Pólya 1921; value in Finch, *Mathematical
  Constants* §5.9) — agreement to six decimals, the fourth pinned as asked. **Every closure event is
  worth `−log₂ p₄ = 2.372 bits`** in the streaming code, and no more.

- **Why the mean number of factors is bounded.** The `ℤ⁴` walk is *transient* (Pólya's theorem: recurrent for
  `d ≤ 2`, transient for `d ≥ 3`), so a long closure returns to balance only finitely often in expectation:
  the mean number of prime factors peaks at `1.607` (`L = 12–16`) and falls toward `1.4800` (three-point fit
  to `L = 1000`; the bridge value `(1 + p₄)/(1 − p₄) = 1.4789` is within the fit's error — *identification
  conjectural*, the sequence is still falling at `L = 1000`: `1.511, 1.498, 1.493, 1.490, 1.488` at `200…1000`). A long closure is
  essentially **one giant prime** with a couple of small ones at the ends, so the prime code saves a bounded
  `≈ 1.5 × 2.37 ≈ 3.5 bits` however long the history — even less than the enumerative `2 log₂ L`.

The vacuum first-closure census is a first-passage problem on the four-dimensional lattice; its dimension `4`
is the alphabet's `|Σ| = 2·|axes|` ([`QLF_AlphabetNecessity`](lean/QLF_AlphabetNecessity.lean)) read as a walk.

### 3a. A correction to the record

[`intermittency_bridge.py`](intermittency_bridge.py) / [`Alpha_Residual.md`](Alpha_Residual.md) §9c report the
first-closure Kraft mass as "converged, `M(∞) = 0.18267…`". That run converged in **capacity `R`** (to `R = 11`)
but was truncated in **length** at `L = 22`; `M(22) = 0.1827` is a partial sum whose `1/L` tail is still
`≈ 0.01` short. The limit is `p₄ = 0.1932`. Nothing downstream changes — leg 2's finding was that the per-octave
multiplier `W(R)` decays, which is about the `R`-profile, not the total — but the number itself should be read
as `M(L ≤ 22)`, not `M(∞)`.

## 4. What this says about compression

1. **A ZFA closure is an incompressible object to leading order.** The Shannon rate of closures is
   `3 − O(log L / L)` bits per twist. The filter selects; it does not shrink. This is the method's rule 4 in
   information-theoretic dress: ZFA "changes a count of ways" by a factor `8/(π²L²)` — a *polynomial* prefactor
   on an exponential, which is exactly what a selection principle (rather than a low-entropy source) looks like.
2. **Primes are the incompressible generators**, as [`Shannon_Overfit.md`](Shannon_Overfit.md) §5c says without
   invoking `K` — and now with a number: the whole redundancy a factorization exposes is `2.37 bits` per event,
   and events are rare (`≈ 1.5` per closure at any length).
3. **The generative route is real but bounded.** `/solve` regenerates the *dominant* closure from a short seed
   (the most-ways closure is the one that needs no spelling out), and the fraction it recovers is a measurable
   census statistic (`54 % / 12 %` at `L = 6`). It is a codec for what the substrate would have done anyway —
   which is the possibilist reading of compression: **you store only the exceptions.**
4. **What would make it a data compressor** — a map from arbitrary bytes into twist histories. None is claimed,
   and the pigeonhole limit holds here as everywhere: there is no universal compressor, in QLF or out of it.

## 5. Falsifiability

The Pólya identification is a prediction with a kill condition: if the exact partial sums `M(L)` ever exceed
`0.1932017` or converge to another value, §3 is wrong. `L = 1000` (36 s, exact integers, `W_L` via the
`ℤ² × ℤ²` split `Σ_k C(L,k) C(k,k/2)² C(L−k,(L−k)/2)²`) gives `0.1932015` — six decimals, not four. The next
falsifier is the factor-count limit, still one digit short of `(1 + p₄)/(1 − p₄)`.

## 6. Lossy compression and diffusion — the census is a Doob bridge

Lossless compression asks how few bits reproduce *this* history; §2–§4 say ZFA barely helps. Lossy compression
and diffusion models ask how few bits reproduce something *typical of the same distribution* — and that is what
closure is made of. Three of QLF's existing objects are already lossy-coding objects under other names:

- **A many-to-one closure is lossy compression with a price tag** — `ΔF = −log 2` per event
  ([`QLF_FreeEnergy`](lean/QLF_FreeEnergy.lean)) *is* Landauer: the free action paid is the information
  discarded, and a bijection pays nothing ([`Fredkin_QLF.md`](Fredkin_QLF.md)).
- **The capacity horizon is the rate parameter** — a listening at capacity `R` receives only the ways with
  `maxExcursion ≤ R` (`closedAtHorizon_iff_maxExcursion_le`); the deeper strata are integrated out. Distortion is
  the strata no longer heard.
- **Seed + `/solve` is a lossy codec once the original is not demanded** — keep `k` twists, regenerate the
  *mode*. The 46 % of length-6 primes that come back different at `k = L−2` come back as the dominant closure:
  distortion = "you were an exception," and the reconstruction is always a closure, never an average
  (method rule 3 — a mean over ways need not be a way; the blur of a lossy image codec is a mean).

**The diffusion correspondence is a theorem, not a metaphor.** A diffusion model runs a forward noising walk and
learns the reverse drift `∇ log p_t` (the score) to walk back to data. A balanced history is the simple walk on
`ℤ⁴` conditioned to return to the origin, and conditioning a walk on its endpoint is **Doob's h-transform**: the
conditioned walk takes step `e` from `x` with `t` steps left with probability `h(x+e, t−1)/h(x, t)`, where
`h(x, t)` = the number of ways to close from `x` in `t` steps. Its drift `∇ log h` *is* the score — and here it
is a count, written down, not learned. `qucalc_search.solve` is the argmax of the same `h` (the mode); the
sampler is the proportional version.

| Diffusion model | QLF |
|---|---|
| forward noising | the free walk on `ℤ⁴` (one axis per conjugate pair) |
| the score `∇ log p` | `∇ log h`, `h` = ways to close — exact, unlearned |
| reverse sampling | the Doob bridge: closure by counting |
| the mode / guidance | `/solve` (least excursion = most ways) |
| a sample ≈ data | a regenerated closure ≈ the original: store only the exceptions |

**`doob_bridge.py` — measured.** `h(x, t)` is computed exactly by the `ℤ² × ℤ²` split; every step draws an
integer in `[0, Σ h)`, so no float enters the choice.

- **Exact by construction, verified deterministically:** for every sample the product of its step probabilities
  is *exactly* `1/W_L` (rationals) — checked for 50 samples at each `L ∈ {4, 6, 8, 12, 20, 50}`, so the sampler
  is uniform over the `W_L` closures by telescoping, not by statistics.
- **Exact empirically:** 20,000 samples at `L = 6` against the enumerated census — strata (max excursion ×
  prime/composite × phase) `χ² = 0.6` on 6 dof; per-closure `χ² = 5210` on 5119 dof (mean 5119, sd 101).
- **Agrees with the counted layer at scale:** sample mean of prime factors `1.629 ± 0.028` at `L = 20` (exact
  `1.601`), `1.570 ± 0.043` at `L = 50` (exact `1.561`), `1.450 ± 0.050` at `L = 100` (exact `1.532`, 1.6 s.e.);
  phase `+1` fraction `≈ 0.5` throughout.
- **The score is Gaussian at scale:** at `x = (5, 2, 0, 1)`, `t = 100`, the discrete `∇ log h` is
  `(−0.200, −0.080, 0, −0.040)` against `−4x_i/t = (−0.2, −0.08, 0, −0.04)`; at `t = 400` both read
  `(−0.05, −0.02, 0, −0.01)`. The drift a diffusion model has to estimate from data is `−4x/t` here, exactly —
  per-axis variance `t/4` because each step moves one of four axes.
- **Efficiency:** rejection sampling (draw a random string, keep it if it closes) needs `8^L/W_L ≈ π²L²/8`
  strings per closure — 518 at `L = 20`, 3,150 at `L = 50`, 12,500 at `L = 100`; the bridge never rejects, and
  every sample is Pauli-closed for free (`count_balanced_pauli_closed`). 76 s for the whole run above, `L = 100`
  included.

**What this is and is not.** It is an exact, unlearned generative model of the census — the thing a diffusion
model approximates, for a distribution whose score is a binomial count. It is a materially better tool than
rejection for generating closures at any length, and it makes the diffusion story concrete: `/solve` = mode,
`doob_bridge` = sample, the same `h`. It is **not** a compressor of external data: a diffusion model's prior is
the data, QLF's prior is the walk, and no map from bytes to census positions is claimed. The one *lossy* codec
it licenses is the one the substrate already runs — store the seed, regenerate the mode, pay `log 2` per
exception dropped.
