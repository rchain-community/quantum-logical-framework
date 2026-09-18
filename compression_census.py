#!/usr/bin/env python3
"""
compression_census.py — can the substrate compress its own histories, and by how much?

QLF holds the *theory* of lossless compression already: Kraft's inequality
(`twist_kraft`, QLF_KraftMeasure), Shannon entropy from counts
(`QLF_ShannonFromCounts`), Landauer's `ΔF = −log 2` per many-to-one closure
(`QLF_FreeEnergy`), and unique factorization of every closure into primes
(`decomposes_into_primes`, `irreducibility_invariant_is_dyson`). This script turns
that theory into a measurement. Nothing here compresses a file — the input is
the substrate's own object, a ZFA closure (a count-balanced twist history), and
the question is how many bits one needs versus the raw `3 bits/twist` of the
8-letter alphabet.

Three codes, from the most knowledge to the least:

  1. **Enumerative (block) bound** — `log2 W_L / L` bits per twist, where `W_L`
     is the count of closures of length `L` (`balanced_history_count`). This is
     the Shannon floor for the set: no lossless code of length-`L` closures beats
     it. Exact, counted, no enumeration.

  2. **Cylinder-prime code (streaming)** — factor the closure into primes (first
     returns to balance; unique, `decomposes_into_primes`) and code each prime `π`
     with the substrate's own measure, `q(π) = 8^{−|π|} / M`, `M = Σ_π 8^{−|π|}`.
     The prime lengths never need to be known in advance and the code is
     prefix-free by construction (`twist_kraft`): cost `3|π| + log2 M` per factor,
     i.e. every closure *event* saves exactly `−log2 M` bits. `M` is the vacuum
     first-closure Kraft mass, converged at `0.18267…` (`intermittency_bridge.py`),
     recomputed here from the Dyson recursion `I_L = W_L − Σ I_ℓ W_{L−ℓ}`.

  3. **Seed + /solve (generative)** — keep only a prefix of a prime and let
     `qucalc_search.solve` regenerate the rest: the decoder is the substrate's
     own selection rule (least excursion → shortest → phase +1 → lex). Stores
     `k` raw twists for a prime of length `|π|`; ratio `k/|π|`. Only the primes
     the substrate *would have chosen* from a short seed compress this way —
     the fraction that do, by how much, is the measurement ("the most ways
     happen first", read as a codec).

Invariants asserted against fresh enumeration (all length ≤ `--max-len`):
  * every closure factors uniquely into primes, and the factors concatenate back;
  * the enumerated prime counts equal the Dyson recursion `I_L`;
  * `Σ_{closures of length L} #factors` equals the DP total `F_L`;
  * the cylinder-prime code is Kraft-legal (`Σ q(π) ≤ 1` at every truncation).

Run:  python3 compression_census.py [--max-len 8] [--solve-len 6] [--dp-len 200]  (~2 min)
Writes data/compression_census.json.
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
OUT_PATH = os.path.join(_HERE, "data", "compression_census.json")
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
# counted layer — W_L, I_L (Dyson), F_L (total factor count), all exact
# --------------------------------------------------------------------------- #
def counted_layer(dp_len: int) -> dict:
    W = {0: 1}
    for L in range(2, dp_len + 1, 2):
        W[L] = balanced_history_count(L)
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


def rates(counted: dict, dp_len: int) -> dict:
    W, F, M_partial = counted["W"], counted["F"], counted["M_partial"]
    M_trunc = float(M_partial[dp_len])
    # the tail of Σ_π 8^{-|π|} decays like a/L (first-return probability ~ L^{-2} in d=4),
    # so one Richardson step on the partial sums estimates the limit
    half = (dp_len // 2) - ((dp_len // 2) % 2)
    M = 2 * M_trunc - float(M_partial[half])
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
            "mean_prime_factors_extrapolated": 2 * F[dp_len] / W[dp_len] - F[half] / W[half],
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
    ap.add_argument("--dp-len", type=int, default=200, help="counted-layer ceiling")
    args = ap.parse_args(argv)

    counted = counted_layer(args.dp_len)
    rt = rates(counted, args.dp_len)
    print(f"prime Kraft mass: M({args.dp_len}) = {rt['M_truncated']:.6f} (exact partial sum), "
          f"extrapolated M(∞) ≈ {rt['M_inf']:.5f}; Pólya Z⁴ return probability = {POLYA_P4}")
    print(f"bits saved per closure event = −log2 M = {rt['bits_saved_per_closure_event']:.4f}")
    print(f"W_L·L²/8^L at L={args.dp_len}: {rt['W_L_L2_over_8L']:.4f}  (8/π² = {8 / math.pi ** 2:.4f}) "
          f"→ a length-L closure is compressible by only 2·log2 L − log2(8/π²) bits in total")
    print(f"mean prime factors per closure: extrapolated {rt['mean_prime_factors_extrapolated']:.4f} "
          f"(bounded — the Z⁴ walk is transient)")
    print()
    print(f"{'L':>3} {'closures':>14} {'primes':>14} {'E#fac':>7} {'enum':>7} {'prime':>7}   ratio(enum/prime)")
    for L, r in rt["by_length"].items():
        if L <= 12 or L in (16, 24, 32, 48, 64, 96, 128, 200):
            print(f"{L:>3} {float(r['closures']):>14.4g} {float(r['primes']):>14.4g} {r['mean_prime_factors']:>7.3f} "
                  f"{r['enumerative_bits_per_twist']:>7.4f} {r['cylinder_prime_bits_per_twist']:>7.4f}   "
                  f"{r['enumerative_ratio']:.3f} / {r['cylinder_prime_ratio']:.3f}")
    print()

    enum = enumerated_layer(args.max_len, counted)
    for p in enum["problems"]:
        print("PROBLEM:", p)
    print(f"enumerated check to L={args.max_len}: "
          f"{'OK' if not enum['problems'] else 'FAILED'} "
          f"({sum(r['closures'] for r in enum['by_length'].values())} closures, "
          f"unique factorization + Dyson primes + factor totals)")
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
