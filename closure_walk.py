#!/usr/bin/env python3
"""
closure_walk.py — the census as a closed walk on ℤ⁴, and what that fixes.

A count-balanced history is a closed walk of the simple random walk on ℤ⁴: the eight
twists are the unit vectors ±e_a of a four-dimensional lattice (one axis per conjugate
pair; `+/−` is the fourth), and ZFA count balance is *the walk returns to the origin*.
This script measures the constants that identification fixes, checks them against fresh
enumeration, and verifies the ℤ₂ connection that carries the half-spin phase on top of
the walk. Full write-up: `Closure_Walk.md`.

Counted layer (exact integers, default to L = 1000):
  * `W_L`  — closures of length L, via the ℤ²×ℤ² split (O(L) per length);
  * `I_L`  — primes (first returns), from the Dyson recursion `I_L = W_L − Σ I_ℓ W_{L−ℓ}`;
  * `F_L`  — total prime-factor count, so `F_L/W_L` is the mean number of returns;
  * `M(L) = Σ_{ℓ≤L} I_ℓ 8^{−ℓ}` — the Kraft mass of the primes, whose limit is Pólya's
    return probability `p₄ = 0.1932…`: the fraction of the uniform possibility measure
    that ever closes at all.

Enumerated checks (every closure to `--max-len`, 195,416 at 8): factors concatenate back,
every factor is prime and Pauli-closed, prime counts equal `I_L`, factor totals equal
`F_L`, and the **edge-sign rule** — sign of the step `x → x + s·e_a` is
`s · (−1)^{Σ_{spatial b ranked above a} x_b}` — reproduces the fold phase of every
closure (the phase is the holonomy of a ℤ₂ connection on the Cayley graph).

Generative layer: for every prime to `--solve-len`, the least prefix from which
`qucalc_search.solve` regenerates it — how much of a prime is the substrate's own choice.

Run:  python3 closure_walk.py [--max-len 8] [--solve-len 6] [--dp-len 1000]  (~3 min)
Writes data/closure_walk.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from fractions import Fraction

from census_inventory import (balanced_histories, balanced_history_count,
                              is_count_balanced, fold_phase)
from qucalc_search import solve, max_excursion

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(_HERE, "data", "closure_walk.json")
RAW_BITS = 3.0                         # log2 8, one twist


# --------------------------------------------------------------------------- #
# prime factorization — first return to balance
# --------------------------------------------------------------------------- #
def prime_factors(h: str) -> list[str]:
    """The unique factorization of a count-balanced history into primes: split
    at every return of the running action vector to zero."""
    out, start = [], 0
    v = [0, 0, 0, 0]
    idx = {'^': (0, 1), 'v': (0, -1), '>': (1, 1), '<': (1, -1),
           '/': (2, 1), '\\': (2, -1), '+': (3, 1), '-': (3, -1)}
    for i, ch in enumerate(h):
        a, s = idx[ch]
        v[a] += s
        if v == [0, 0, 0, 0]:
            out.append(h[start:i + 1])
            start = i + 1
    assert start == len(h), "not count-balanced"
    return out


def is_prime(h: str) -> bool:
    return len(prime_factors(h)) == 1


# --------------------------------------------------------------------------- #
# the ℤ₂ connection — the half-spin phase as a holonomy on the Cayley graph
# --------------------------------------------------------------------------- #
_AX = {'^': (0, 1), 'v': (0, -1), '>': (1, 1), '<': (1, -1),
       '/': (2, 1), '\\': (2, -1), '+': (3, 1), '-': (3, -1)}
_RANK = {1: 0, 0: 1, 2: 2}          # spatial axes X < Y < Z (census AXIS_ORDER); gauge axis 3 commutes


def edge_sign(x: list[int], a: int, s: int) -> int:
    """Sign carried by the directed edge x → x + s·e_a: the twist's own sign times
    (−1)^(Σ x_b over spatial axes b ranked above a). The parity of the axis-b count so far
    equals the parity of x_b, so this is the inversion count the phase rule adds — a
    function of the node, which is what makes it a connection on the graph."""
    sgn = s
    if a != 3 and sum(x[b] for b in (0, 1, 2) if _RANK[b] > _RANK[a]) % 2:
        sgn = -sgn
    return sgn


def connection_phase(h: str) -> str:
    """Product of edge signs along the path — the holonomy. Equals `fold_phase` on
    every closure (asserted by the enumerated layer)."""
    x = [0, 0, 0, 0]
    sgn = 1
    for c in h:
        a, s = _AX[c]
        sgn *= edge_sign(x, a, s)
        x[a] += s
    return "+1" if sgn > 0 else "-1"


# --------------------------------------------------------------------------- #
# counted layer — W_L, I_L (Dyson), F_L (total factor count), all exact
# --------------------------------------------------------------------------- #
def closed_walk_count(L: int) -> int:
    """`W_L` as a closed walk on ℤ⁴ = ℤ² × ℤ²: split the `L` steps between the two
    planes, each plane closing in `C(k, k/2)²` ways. Equals `balanced_history_count`
    (asserted below for small `L`) but O(L) per length instead of O(L³)."""
    return sum(math.comb(L, k) * math.comb(k, k // 2) ** 2 * math.comb(L - k, (L - k) // 2) ** 2
               for k in range(0, L + 1, 2))


def counted_layer(dp_len: int) -> dict:
    W = {0: 1}
    for L in range(2, dp_len + 1, 2):
        W[L] = closed_walk_count(L)
        if L <= 12:
            assert W[L] == balanced_history_count(L), f"W_{L} split-count mismatch"
    # Dyson: G = 1/(1 − I)  ⟺  W_L = Σ_{ℓ} I_ℓ W_{L−ℓ}, so I_L = W_L − Σ_{ℓ<L} I_ℓ W_{L−ℓ}
    I = {}
    for L in range(2, dp_len + 1, 2):
        I[L] = W[L] - sum(I[l] * W[L - l] for l in range(2, L, 2))
    # F_L = Σ over closures of length L of (#prime factors); first-factor decomposition
    F = {0: 0}
    for L in range(2, dp_len + 1, 2):
        F[L] = sum(I[l] * (W[L - l] + F[L - l]) for l in range(2, L + 1, 2))
    # Kraft mass of the primes, exact rationals — this is M(∞) of intermittency_bridge
    M_partial = {}
    acc = Fraction(0)
    for L in range(2, dp_len + 1, 2):
        acc += Fraction(I[L], 8 ** L)
        M_partial[L] = acc
    assert all(0 < m < 1 for m in M_partial.values()), "prime code not Kraft-legal"
    return {"W": W, "I": I, "F": F, "M_partial": M_partial}


POLYA_P4 = 0.193201673        # P(return to origin), simple random walk on Z^4 (Pólya 1921;
                              # value: Finch, *Mathematical Constants*, §5.9)


def _tail_fit(f, L3: int) -> float:
    """Fit f(L) = f∞ − a/L − b/L² through L3/2, 3L3/4, L3 and return f∞."""
    Ls = [L3 // 2, (3 * L3) // 4, L3]
    Ls = [L - (L % 2) for L in Ls]
    A = [[1.0, -1 / L, -1 / L ** 2] for L in Ls]
    y = [f(L) for L in Ls]

    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    return det([[y[i]] + A[i][1:] for i in range(3)]) / det(A)


def sci(n: int) -> str:
    """`n` in scientific notation without going through float (8^1000 overflows)."""
    d = str(n)
    return d if len(d) < 8 else f"{d[0]}.{d[1:4]}e+{len(d) - 1}"


def rates(counted: dict, dp_len: int) -> dict:
    W, F, M_partial = counted["W"], counted["F"], counted["M_partial"]
    M_trunc = float(M_partial[dp_len])
    # the tail of Σ_π 8^{-|π|} decays like a/L + b/L² (first-return probability ~ L^{-2}
    # in d=4), so a three-point fit on the partial sums pins the limit
    M = _tail_fit(lambda L: float(M_partial[L]), dp_len)
    half = (dp_len // 2) - ((dp_len // 2) % 2)
    save_per_event = -math.log2(M)          # bits every closure event is worth
    rows = {}
    for L in range(2, dp_len + 1, 2):
        w = W[L]
        mean_factors = F[L] / w
        enum_bits = math.log2(w) / L
        prime_bits = (RAW_BITS * L - save_per_event * mean_factors) / L
        rows[L] = {
            "closures": w,
            "primes": counted["I"][L],
            "mean_prime_factors": round(mean_factors, 6),
            "enumerative_bits_per_twist": round(enum_bits, 6),
            "cylinder_prime_bits_per_twist": round(prime_bits, 6),
            "enumerative_ratio": round(enum_bits / RAW_BITS, 6),
            "cylinder_prime_ratio": round(prime_bits / RAW_BITS, 6),
        }
    return {"M_inf": M, "M_truncated": M_trunc, "polya_p4": POLYA_P4,
            "bits_saved_per_closure_event": save_per_event,
            "W_L_L2_over_8L": W[dp_len] * dp_len ** 2 / 8 ** dp_len,   # → 8/π² = 0.8106
            "mean_prime_factors_extrapolated": _tail_fit(lambda L: F[L] / W[L], dp_len),
            "bridge_returns_conjecture": (1 + POLYA_P4) / (1 - POLYA_P4),
            "by_length": rows}


# --------------------------------------------------------------------------- #
# enumerated layer — checks the counted layer against fresh histories
# --------------------------------------------------------------------------- #
def enumerated_layer(max_len: int, counted: dict) -> dict:
    problems = []
    rows = {}
    for L in range(2, max_len + 1, 2):
        n = 0
        primes = 0
        total_factors = 0
        for h in balanced_histories(L):
            n += 1
            fs = prime_factors(h)
            if "".join(fs) != h:
                problems.append(f"L={L}: factors do not concatenate back: {h}")
            for f in fs:
                if not is_count_balanced(f) or not is_prime(f):
                    problems.append(f"L={L}: non-prime factor {f} of {h}")
                if fold_phase(f) is None:
                    problems.append(f"L={L}: factor {f} not Pauli-closed")
            if len(fs) == 1:
                primes += 1
            total_factors += len(fs)
            if connection_phase(h) != fold_phase(h):
                problems.append(f"L={L}: edge-sign rule ≠ fold phase for {h}")
        if n != counted["W"][L]:
            problems.append(f"L={L}: enumerated {n} ≠ counted W_L {counted['W'][L]}")
        if primes != counted["I"][L]:
            problems.append(f"L={L}: enumerated primes {primes} ≠ Dyson I_L {counted['I'][L]}")
        if total_factors != counted["F"][L]:
            problems.append(f"L={L}: Σ#factors {total_factors} ≠ DP F_L {counted['F'][L]}")
        rows[L] = {"closures": n, "primes": primes, "total_factors": total_factors}
    return {"by_length": rows, "problems": problems}


# --------------------------------------------------------------------------- #
# generative layer — seed + /solve
# --------------------------------------------------------------------------- #
def solve_layer(solve_len: int) -> dict:
    """For every prime of length ≤ solve_len, the least seed length k such that
    solve(π[:k]) regenerates π exactly. Reports the distribution of k/|π|."""
    rows = {}
    nonmonotone = 0
    examples = {}
    for L in range(2, solve_len + 1, 2):
        hist = {}       # k -> count of primes with minimal seed k
        n = 0
        for h in balanced_histories(L):
            if not is_prime(h):
                continue
            n += 1
            ok = [False]                                      # k = 0: solve needs a seed
            for k in range(1, L):
                r = solve(h[:k], max_depth=L - k, min_total_len=2)
                ok.append(bool(r.get("solved")) and r.get("history") == h)
            ok.append(True)                                   # k = L: nothing to solve
            kmin = ok.index(True)
            # once the seed is long enough it should stay reconstructible
            if not all(ok[kmin:]):
                nonmonotone += 1
            hist[kmin] = hist.get(kmin, 0) + 1
            if kmin <= L - 3 and L not in examples:
                examples[L] = {"prime": h, "seed": h[:kmin], "seed_len": kmin}
        mean_ratio = sum(k * c for k, c in hist.items()) / (n * L)
        rows[L] = {
            "primes": n,
            "prime_enumerative_bits_per_twist": round(math.log2(n) / L, 6),
            "min_seed_histogram": {str(k): hist[k] for k in sorted(hist)},
            "mean_seed_ratio": round(mean_ratio, 6),
            "generative_bits_per_twist": round(RAW_BITS * mean_ratio, 6),
            "solve_chosen_from_2_short": sum(c for k, c in hist.items() if k <= L - 2),
            "solve_chosen_from_3_short": sum(c for k, c in hist.items() if k <= L - 3),
        }
    return {"by_length": rows, "nonmonotone_primes": nonmonotone, "examples": examples}


# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-len", type=int, default=8, help="enumerated check ceiling")
    ap.add_argument("--solve-len", type=int, default=6, help="seed+/solve ceiling")
    ap.add_argument("--dp-len", type=int, default=1000, help="counted-layer ceiling")
    args = ap.parse_args(argv)

    counted = counted_layer(args.dp_len)
    rt = rates(counted, args.dp_len)
    print(f"prime Kraft mass: M({args.dp_len}) = {rt['M_truncated']:.6f} (exact partial sum), "
          f"extrapolated M(∞) ≈ {rt['M_inf']:.5f}; Pólya Z⁴ return probability = {POLYA_P4}")
    print(f"bits saved per closure event = −log2 M = {rt['bits_saved_per_closure_event']:.4f}")
    print(f"W_L·L²/8^L at L={args.dp_len}: {rt['W_L_L2_over_8L']:.4f}  (8/π² = {8 / math.pi ** 2:.4f}) "
          f"→ a length-L closure is compressible by only 2·log2 L − log2(8/π²) bits in total")
    print(f"mean prime factors per closure: extrapolated {rt['mean_prime_factors_extrapolated']:.4f} "
          f"(bounded — the Z⁴ walk is transient; (1+p₄)/(1−p₄) = {rt['bridge_returns_conjecture']:.4f})")
    print()
    print(f"{'L':>3} {'closures':>14} {'primes':>14} {'E#fac':>7} {'enum':>7} {'prime':>7}   ratio(enum/prime)")
    for L, r in rt["by_length"].items():
        if L <= 12 or L in (16, 32, 64, 128, 200, 400, 600, 800, 1000):
            print(f"{L:>3} {sci(r['closures']):>14} {sci(r['primes']):>14} {r['mean_prime_factors']:>7.3f} "
                  f"{r['enumerative_bits_per_twist']:>7.4f} {r['cylinder_prime_bits_per_twist']:>7.4f}   "
                  f"{r['enumerative_ratio']:.3f} / {r['cylinder_prime_ratio']:.3f}")
    print()

    enum = enumerated_layer(args.max_len, counted)
    for p in enum["problems"]:
        print("PROBLEM:", p)
    print(f"enumerated check to L={args.max_len}: "
          f"{'OK' if not enum['problems'] else 'FAILED'} "
          f"({sum(r['closures'] for r in enum['by_length'].values())} closures, "
          f"unique factorization + Dyson primes + factor totals + edge-sign rule = fold phase)")
    print()

    sl = solve_layer(args.solve_len)
    print(f"seed + /solve, primes of length ≤ {args.solve_len}:")
    for L, r in sl["by_length"].items():
        print(f"  L={L}: {r['primes']} primes, min-seed histogram {r['min_seed_histogram']}, "
              f"mean seed ratio {r['mean_seed_ratio']:.3f} → {r['generative_bits_per_twist']:.3f} bits/twist "
              f"(prime enumerative floor {r['prime_enumerative_bits_per_twist']:.3f}); "
              f"chosen from ≥2 short: {r['solve_chosen_from_2_short']}, ≥3 short: {r['solve_chosen_from_3_short']}")
    print(f"  non-monotone primes (reconstructible then not): {sl['nonmonotone_primes']}")
    for L, ex in sl["examples"].items():
        print(f"  example L={L}: seed {ex['seed']!r} ({ex['seed_len']} twists) → {ex['prime']}")

    out = {
        "raw_bits_per_twist": RAW_BITS,
        "M_inf": rt["M_inf"], "M_truncated": rt["M_truncated"], "dp_len": args.dp_len,
        "polya_p4": POLYA_P4,
        "W_L_L2_over_8L": rt["W_L_L2_over_8L"],
        "mean_prime_factors_extrapolated": rt["mean_prime_factors_extrapolated"],
        "bits_saved_per_closure_event": rt["bits_saved_per_closure_event"],
        "counted": {str(L): r for L, r in rt["by_length"].items()},
        "enumerated_check": {"max_len": args.max_len, "ok": not enum["problems"],
                             "by_length": {str(L): r for L, r in enum["by_length"].items()}},
        "seed_solve": {"solve_len": args.solve_len,
                       "by_length": {str(L): r for L, r in sl["by_length"].items()},
                       "nonmonotone_primes": sl["nonmonotone_primes"],
                       "examples": {str(L): e for L, e in sl["examples"].items()}},
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {os.path.relpath(OUT_PATH, _HERE)}")
    return 1 if enum["problems"] else 0


if __name__ == "__main__":
    sys.exit(main())
