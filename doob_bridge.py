#!/usr/bin/env python3
"""
doob_bridge.py — sample ZFA closures uniformly, by the h-transform of the closure walk.

A count-balanced history is a closed walk on ℤ⁴ (one axis per conjugate pair). Conditioning
the free walk to return to the origin at step `L` is **Doob's h-transform**: at position `x`
with `t` steps left, take twist `e` with probability

    P(e | x, t) = h(x + e, t − 1) / h(x, t),     h(x, t) = #walks of length t from x to 0,

and the result is exactly uniform over the `W_L` closures — the step probabilities telescope
to `h(0,0)/h(0,L) = 1/W_L`. `qucalc_search.solve` is the argmax of the same `h` (the mode,
"what happens in the most ways happens first"); this is the sampler. It samples the
*unsigned* census — ways, not the half-spin phase, which is a ℤ₂ holonomy on top of the
walk (`Closure_Walk.md` §2) and cannot drive a sampler (it goes negative).

Why it matters: rejection sampling (draw a random string, keep it if it closes) succeeds
with probability `W_L / 8^L ≈ (8/π²)/L²` — one in 12,000 at `L = 100`. The bridge never
rejects and every sample is Pauli-closed for free (`count_balanced_pauli_closed`).

What is asserted, per run:
  * **exactness, deterministic** — for every sample the product of its step probabilities
    equals `1/W_L` exactly (rationals), so the sampler is uniform by construction, not by test;
  * **exactness, empirical** — at `L = 6` a chi-square of sample counts against the
    enumerated census, per max-excursion stratum and prime/composite;
  * **agreement with the counted layer at scale** — the sample mean of the number of prime
    factors at `L ∈ {20, 50, 100}` versus the exact `F_L / W_L` of `closure_walk.py`.

**Primes only.** Swap `h` for the taboo count `f(x, t)` — walks from `x` that reach the
origin for the *first* time at step `t`, read off the first-return decomposition
`h(x,t) = Σ_s f(x,s)·W_{t−s}` — and the same bridge samples uniformly over the `I_L`
primes (it telescopes to `1/I_L`, since `Σ_e f(e, L−1) = I_L` is the Dyson recursion).
`sample_prime` is that; it never emits a composite and never rejects.

Run:  python3 doob_bridge.py [--samples 20000] [--max-len 100] [--seed 1]
Writes data/doob_bridge.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
from fractions import Fraction
from functools import lru_cache

from closure_walk import prime_factors, counted_layer, closed_walk_count
from census_inventory import balanced_histories, predicted_phase
from qucalc_search import max_excursion

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(_HERE, "data", "doob_bridge.json")

TWISTS = ['^', 'v', '>', '<', '/', '\\', '+', '-']
STEP = {'^': (0, 1), 'v': (0, -1), '>': (1, 1), '<': (1, -1),
        '/': (2, 1), '\\': (2, -1), '+': (3, 1), '-': (3, -1)}


# --------------------------------------------------------------------------- #
# h(x, t): walks of length t from x to the origin, exact
# --------------------------------------------------------------------------- #
def _c1(k: int, v: int) -> int:
    """1-D walks of length k with net displacement v."""
    v = abs(v)
    if v > k or (k + v) % 2:
        return 0
    return math.comb(k, (k + v) // 2)


@lru_cache(maxsize=None)
def _c2(t: int, a: int, b: int) -> int:
    """ℤ² walks of length t with displacement (a, b): split the steps between the axes."""
    a, b = abs(a), abs(b)
    if a + b > t or (t + a + b) % 2:
        return 0
    return sum(math.comb(t, k) * _c1(k, a) * _c1(t - k, b) for k in range(a, t - b + 1))


def h(x: tuple[int, int, int, int], t: int) -> int:
    """ℤ⁴ walks of length t from x to 0 = ℤ² × ℤ² split."""
    a, b, c, d = (abs(v) for v in x)
    if a + b + c + d > t or (t + a + b + c + d) % 2:
        return 0
    return sum(math.comb(t, k) * _c2(k, a, b) * _c2(t - k, c, d)
               for k in range(a + b, t - c - d + 1))


@lru_cache(maxsize=None)
def f_taboo(x: tuple[int, int, int, int], t: int) -> int:
    """Walks of length t from x that reach the origin for the FIRST time at step t.
    First-return decomposition: every walk x→0 in t steps first hits 0 at some s ≤ t
    and then makes a closed walk of length t−s, so h(x,t) = Σ_s f(x,s)·W_{t−s}, and
    f is read off by inverting. f(0,0) = 1; f(0,t>0) = 0 (already at the origin)."""
    if x == (0, 0, 0, 0):
        return 1 if t == 0 else 0
    ht = h(x, t)
    if ht == 0:
        return 0
    return ht - sum(f_taboo(x, s) * closed_walk_count(t - s) for s in range(1, t, 1)
                    if (t - s) % 2 == 0)


# --------------------------------------------------------------------------- #
# the bridge
# --------------------------------------------------------------------------- #
def _bridge(L: int, rng: random.Random, weight, with_prob: bool):
    x = [0, 0, 0, 0]
    out = []
    prob = Fraction(1)
    for t in range(L, 0, -1):
        weights = []
        for e in TWISTS:
            ax, s = STEP[e]
            x[ax] += s
            weights.append(weight(tuple(x), t - 1))
            x[ax] -= s
        total = sum(weights)
        r = rng.randrange(total)                       # exact: no float in the choice
        acc = 0
        for e, w in zip(TWISTS, weights):
            acc += w
            if r < acc:
                break
        ax, s = STEP[e]
        x[ax] += s
        out.append(e)
        if with_prob:
            prob *= Fraction(w, total)
    assert x == [0, 0, 0, 0]
    hist = "".join(out)
    return (hist, prob) if with_prob else hist


def sample_prime(L: int, rng: random.Random, with_prob: bool = False):
    """One PRIME closure of length L (first return to balance at L), uniform over the
    I_L primes: the same h-transform with the taboo count in place of h. Telescopes to
    1/I_L because Σ_e f(e, L−1) = I_L (the Dyson recursion, read as first steps)."""
    return _bridge(L, rng, f_taboo, with_prob)


def sample_closure(L: int, rng: random.Random, with_prob: bool = False):
    """One closure of length L, uniform over the W_L. Optionally returns the exact
    probability the sampler assigned it (a Fraction), for the telescoping check."""
    return _bridge(L, rng, h, with_prob)


def score(x: tuple[int, int, int, int], t: int) -> list[float]:
    """The discrete score ∇ log h at (x, t), per unit step on each axis (half the
    central log-difference). For large t, h is Gaussian with per-axis variance t/4,
    so this → −4·x_i/t: the drift a diffusion model would have to learn."""
    out = []
    for ax in range(4):
        xp = list(x); xp[ax] += 1
        xm = list(x); xm[ax] -= 1
        hp, hm = h(tuple(xp), t - 1), h(tuple(xm), t - 1)
        out.append(0.5 * math.log(hp / hm) if hp and hm else float("nan"))
    return out


# --------------------------------------------------------------------------- #
def chi_square(observed: dict, expected: dict) -> tuple[float, int]:
    keys = [k for k in expected if expected[k] > 0]
    chi = sum((observed.get(k, 0) - expected[k]) ** 2 / expected[k] for k in keys)
    return chi, len(keys) - 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=20000)
    ap.add_argument("--max-len", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)
    rng = random.Random(args.seed)
    result: dict = {"samples": args.samples, "seed": args.seed}

    # 1. deterministic exactness: step probabilities telescope to 1/W_L
    tele = {}
    for L in (4, 6, 8, 12, 20, 50):
        W = closed_walk_count(L)
        ok = all(sample_closure(L, rng, with_prob=True)[1] == Fraction(1, W) for _ in range(50))
        tele[L] = ok
        print(f"L={L:>3}: 50 samples, each assigned probability exactly 1/W_L = 1/{W}: {'OK' if ok else 'FAIL'}")
    result["telescoping_exact"] = tele
    if not all(tele.values()):
        return 1

    # 2. empirical exactness at L = 6 against the enumerated census
    L = 6
    census = list(balanced_histories(L))
    W = len(census)
    strata_exp = {}
    for hh in census:
        key = f"exc={max_excursion(hh)},{'prime' if len(prime_factors(hh)) == 1 else 'composite'},{predicted_phase(hh)}"
        strata_exp[key] = strata_exp.get(key, 0) + 1
    n = args.samples
    strata_obs = {}
    seen = {}
    for _ in range(n):
        hh = sample_closure(L, rng)
        key = f"exc={max_excursion(hh)},{'prime' if len(prime_factors(hh)) == 1 else 'composite'},{predicted_phase(hh)}"
        strata_obs[key] = strata_obs.get(key, 0) + 1
        seen[hh] = seen.get(hh, 0) + 1
    expected = {k: v * n / W for k, v in strata_exp.items()}
    chi, dof = chi_square(strata_obs, expected)
    # individual closures: chi-square over all W_L cells
    chi_all = sum((seen.get(hh, 0) - n / W) ** 2 / (n / W) for hh in census)
    print(f"\nL=6, {n} samples vs enumerated census ({W} closures):")
    for k in sorted(strata_exp):
        print(f"  {k:<28} expected {expected[k]:>9.1f}  observed {strata_obs.get(k, 0):>6}")
    print(f"  strata chi² = {chi:.1f} on {dof} dof (mean {dof}, sd {math.sqrt(2 * dof):.1f})")
    print(f"  per-closure chi² = {chi_all:.0f} on {W - 1} dof (mean {W - 1}, sd {math.sqrt(2 * (W - 1)):.0f})")
    result["L6_check"] = {"W": W, "strata_chi2": chi, "strata_dof": dof,
                          "per_closure_chi2": chi_all, "per_closure_dof": W - 1,
                          "strata": {k: {"expected": expected[k], "observed": strata_obs.get(k, 0)}
                                     for k in sorted(strata_exp)}}

    # 3. at scale: mean prime factors and closure depth vs the counted layer
    counted = counted_layer(max(args.max_len, 50))
    Wd, Fd = counted["W"], counted["F"]
    scale = {}
    print("\nat scale (sample mean ± s.e. vs exact F_L/W_L):")
    for L in sorted({20, 50, args.max_len}):
        if L > args.max_len or L % 2:
            continue
        m = max(200, args.samples // L)
        facs, excs, phases = [], [], {"+1": 0, "-1": 0}
        for _ in range(m):
            hh = sample_closure(L, rng)
            facs.append(len(prime_factors(hh)))
            excs.append(max_excursion(hh))
            phases[predicted_phase(hh)] += 1
        mean_f = sum(facs) / m
        se_f = (sum((f - mean_f) ** 2 for f in facs) / (m - 1) / m) ** 0.5
        exact = Fd[L] / Wd[L]
        mean_e = sum(excs) / m
        rej = 8 ** L / Wd[L]
        print(f"  L={L:>4}: {m} samples; #factors {mean_f:.4f} ± {se_f:.4f} vs exact {exact:.4f} "
              f"({abs(mean_f - exact) / se_f:.1f} s.e.); mean depth {mean_e:.2f}; "
              f"phase +1 {phases['+1'] / m:.3f}; rejection would need 1 in {rej:.3g} strings")
        scale[L] = {"samples": m, "mean_factors": mean_f, "se": se_f, "exact_mean_factors": exact,
                    "mean_max_excursion": mean_e, "phase_plus_fraction": phases["+1"] / m,
                    "rejection_cost_strings_per_sample": rej}
    result["at_scale"] = scale

    # 3b. primes only — the taboo bridge
    print("\nprimes only (taboo h-transform):")
    Id = counted["I"]
    prime_tele = {}
    for L in (4, 6, 8, 12, 20, 50):
        ok = True
        for _ in range(50):
            hh, pr = sample_prime(L, rng, with_prob=True)
            ok &= (pr == Fraction(1, Id[L])) and len(prime_factors(hh)) == 1
        prime_tele[L] = ok
        print(f"  L={L:>3}: 50 samples, each prime and assigned exactly 1/I_L = 1/{Id[L]}: {'OK' if ok else 'FAIL'}")
    if not all(prime_tele.values()):
        return 1
    primes6 = [hh for hh in census if len(prime_factors(hh)) == 1]
    pexp = {}
    for hh in primes6:
        key = f"exc={max_excursion(hh)},{predicted_phase(hh)}"
        pexp[key] = pexp.get(key, 0) + 1
    pobs, pseen = {}, {}
    for _ in range(n):
        hh = sample_prime(6, rng)
        key = f"exc={max_excursion(hh)},{predicted_phase(hh)}"
        pobs[key] = pobs.get(key, 0) + 1
        pseen[hh] = pseen.get(hh, 0) + 1
    I6 = len(primes6)
    pexpected = {k: v * n / I6 for k, v in pexp.items()}
    pchi, pdof = chi_square(pobs, pexpected)
    pchi_all = sum((pseen.get(hh, 0) - n / I6) ** 2 / (n / I6) for hh in primes6)
    print(f"  L=6, {n} samples vs the {I6} enumerated primes: strata chi² = {pchi:.1f} on {pdof} dof; "
          f"per-prime chi² = {pchi_all:.0f} on {I6 - 1} dof (sd {math.sqrt(2 * (I6 - 1)):.0f})")
    pscale = {}
    for L in sorted({20, 50, args.max_len}):
        if L > args.max_len or L % 2:
            continue
        m = max(200, args.samples // L)
        excs = [max_excursion(sample_prime(L, rng)) for _ in range(m)]
        mean_e = sum(excs) / m
        frac = Id[L] / Wd[L]
        print(f"  L={L:>4}: {m} primes; mean depth {mean_e:.2f} (all closures {scale[L]['mean_max_excursion']:.2f}); "
              f"primes are {frac:.3f} of closures, so filtering the closure bridge would waste 1 in {1 / (1 - frac):.2f}")
        pscale[L] = {"samples": m, "mean_max_excursion": mean_e, "prime_fraction_exact": frac}
    result["primes"] = {"telescoping_exact": prime_tele,
                        "L6_check": {"I": I6, "strata_chi2": pchi, "strata_dof": pdof,
                                     "per_prime_chi2": pchi_all, "per_prime_dof": I6 - 1},
                        "at_scale": pscale}

    # 4. the score: discrete ∇ log h against the Gaussian −4x/t
    print("\nscore ∇log h at (x, t) vs Gaussian −4x_i/t:")
    sc = {}
    for x, t in (((3, 0, 0, 0), 21), ((3, 0, 0, 0), 101), ((5, 2, 0, 1), 100), ((5, 2, 0, 1), 400)):
        s = score(x, t)
        g = [-4 * xi / t for xi in x]
        print(f"  x={x}, t={t}: {[round(v, 3) for v in s]}  gaussian {[round(v, 3) for v in g]}")
        sc[f"{x},{t}"] = {"score": s, "gaussian": g}
    result["score_vs_gaussian"] = sc

    ex = [sample_closure(args.max_len, rng) for _ in range(3)]
    result["examples"] = ex
    result["prime_examples"] = [sample_prime(args.max_len, rng) for _ in range(2)]
    print(f"\nthree uniform closures at L={args.max_len}:")
    for e in ex:
        print(f"  {e}  (factors {len(prime_factors(e))}, depth {max_excursion(e)})")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=1)
    print(f"\nwrote {os.path.relpath(OUT_PATH, _HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
