#!/usr/bin/env python3
"""The closure naming game: memetics with words that are closures (Memetics_QLF.md §10-§11).

A word is a first closure (prime) of the 8-twist walk. The substrate invents a word by
running a uniform twist walk to its first return to balance (retried if it has not
returned by length 6), so a prime of length L is invented with probability ∝ 8^-L and all
primes of one length are tied in frequency.

Minimal naming game (Steels 1995; Baronchelli et al. 2006): N agents with empty
inventories; each step a random speaker and hearer; an empty speaker invents a word; the
speaker utters a uniform word from its inventory; if the hearer holds it both collapse to
it (a joint closure), otherwise the hearer adds it. A run ends at consensus.

T7a  every run reaches consensus
T7b  winner has length 2 in >= 77% of runs
T7c  among length-2 winners the winner is uniform over the 8 words (chi-square p > 0.01,
     entropy >= 2.9 bits)
T7d  control: length-2 invention weights 1.25^-i; winner entropy < 2.9 bits and below the
     entropy of the weights (amplification)

Run: python3 meme_naming_game.py [--runs 400] [--n 200]
"""
from __future__ import annotations

import argparse
import math
import random
from collections import Counter

from census_inventory import fold_phase
from qucalc_search import _PHASE_RANK, max_excursion

STEPS = {"^": (0, 1), "v": (0, -1), ">": (1, 1), "<": (1, -1),
         "/": (2, 1), "\\": (2, -1), "+": (3, 1), "-": (3, -1)}
TWISTS = list(STEPS)
PAIRS = ["^v", "v^", "><", "<>", "/\\", "\\/", "+-", "-+"]   # the 8 length-2 primes
MAX_LEN = 6


def invent(rng: random.Random, weights2=None) -> str:
    """A first closure drawn from the substrate, conditioned on closing by MAX_LEN."""
    while True:
        x = [0, 0, 0, 0]
        w = []
        for _ in range(MAX_LEN):
            t = rng.choice(TWISTS)
            a, s = STEPS[t]
            x[a] += s
            w.append(t)
            if not any(x):
                word = "".join(w)
                if len(word) == 2 and weights2 is not None:
                    word = rng.choices(PAIRS, weights=weights2)[0]
                return word


def play(rng: random.Random, n: int, weights2=None, max_steps: int = 10 ** 7,
         inventor=None, choose=None, invented=None) -> tuple:
    inv = [[] for _ in range(n)]
    for step in range(1, max_steps + 1):
        s, h = rng.sample(range(n), 2)
        if not inv[s]:
            word = inventor(rng) if inventor else invent(rng, weights2)
            inv[s].append(word)
            if invented is not None:
                invented.add(word)
        w = choose(rng, inv[s]) if choose else rng.choice(inv[s])
        if w in inv[h]:
            inv[s] = [w]
            inv[h] = [w]
            if all(len(v) == 1 and v[0] == w for v in inv):
                return w, step
        else:
            inv[h].append(w)
    return None, max_steps


def entropy(c: Counter) -> float:
    tot = sum(c.values())
    return -sum(v / tot * math.log2(v / tot) for v in c.values() if v)


def chi2_sf(x: float, k: int) -> float:
    """Survival function of chi-square with k dof (series for the lower incomplete gamma)."""
    a, z = k / 2, x / 2
    term = summ = 1 / a
    for i in range(1, 500):
        term *= z / (a + i)
        summ += term
    lower = summ * math.exp(-z + a * math.log(z) - math.lgamma(a))
    return max(0.0, 1 - lower)


def report(label: str, winners: list, steps: list, weights2=None) -> None:
    runs = len(winners)
    done = [w for w in winners if w is not None]
    by_len = Counter(len(w) for w in done)
    pairs = Counter(w for w in done if len(w) == 2)
    m = sum(pairs.values())
    exp = [m * (wt / sum(weights2)) for wt in weights2] if weights2 else [m / 8] * 8
    chi = sum((pairs.get(p, 0) - e) ** 2 / e for p, e in zip(PAIRS, exp))
    print(f"\n[{label}] runs {runs}, consensus in {len(done)}, median steps {sorted(steps)[runs // 2]}")
    print(f"  winner length counts: {dict(sorted(by_len.items()))}"
          f"  (length-2 share {by_len[2] / max(1, len(done)):.3f})")
    print(f"  length-2 winners by word: {[pairs.get(p, 0) for p in PAIRS]}")
    print(f"  winner entropy among length-2 winners: {entropy(pairs):.3f} bits (uniform = 3.000)")
    print(f"  chi-square vs uniform: {sum((pairs.get(p, 0) - m / 8) ** 2 / (m / 8) for p in PAIRS):.2f}"
          f"  p = {chi2_sf(sum((pairs.get(p, 0) - m / 8) ** 2 / (m / 8) for p in PAIRS), 7):.4f}")
    if weights2:
        wc = Counter({p: wt for p, wt in zip(PAIRS, weights2)})
        print(f"  entropy of the invention weights: {entropy(wc):.3f} bits")
        print(f"  chi-square vs the invention weights: {chi:.2f}  p = {chi2_sf(chi, 7):.4f}")


# --------------------------------------------------------------------------- #
# T8: QuCalc's /solve order as the tie-break (Memetics_QLF.md §12-§13)
# --------------------------------------------------------------------------- #

def invent_len4(rng: random.Random) -> str:
    """A uniform length-4 prime: the substrate conditioned on first return at 4."""
    while True:
        x = [0, 0, 0, 0]
        w = []
        for k in range(4):
            t = rng.choice(TWISTS)
            a, s = STEPS[t]
            x[a] += s
            w.append(t)
            if not any(x):
                break
        if len(w) == 4 and not any(x):
            return "".join(w)


def phys_key(w: str) -> tuple:
    """/solve's order without its last, alphabetical step."""
    return (max_excursion(w), len(w), _PHASE_RANK[fold_phase(w)])


def full_key(w: str) -> tuple:
    """/solve's full order (qucalc_search.solve)."""
    return phys_key(w) + (w,)


def choose_full(rng: random.Random, inv: list) -> str:
    return min(inv, key=full_key)


def choose_phys(rng: random.Random, inv: list) -> str:
    best = min(phys_key(w) for w in inv)
    return rng.choice([w for w in inv if phys_key(w) == best])


def t8(runs: int, n: int, seed: int) -> None:
    import itertools
    def first_return_at_4(p):
        x = [0, 0, 0, 0]
        for k, t in enumerate(p, 1):
            a, sg = STEPS[t]
            x[a] += sg
            if not any(x):
                return k == 4
        return False

    primes4 = sorted("".join(p) for p in itertools.product(TWISTS, repeat=4) if first_return_at_4(p))
    plus = [w for w in primes4 if fold_phase(w) == "+1"]
    print(f"\nT8: {len(primes4)} length-4 primes, {len(plus)} with phase +1;"
          f" excursions {sorted({max_excursion(w) for w in primes4})};"
          f" /solve's best overall: {min(primes4, key=full_key)!r}")
    for label, choose in (("T8a baseline: uniform utterance", None),
                          ("T8b reading 1: full /solve order", choose_full),
                          ("T8c reading 2: physical order only", choose_phys)):
        rng = random.Random(seed)
        winners, best_of_invented = [], 0
        for _ in range(runs):
            invented = set()
            w, _k = play(rng, n, inventor=invent_len4, choose=choose, invented=invented)
            winners.append(w)
            if w == min(invented, key=full_key):
                best_of_invented += 1
        c = Counter(winners)
        pc = Counter(w for w in winners if fold_phase(w) == "+1")
        m = sum(pc.values())
        chi = sum((pc.get(p, 0) - m / len(plus)) ** 2 / (m / len(plus)) for p in plus) if m else 0.0
        top, topn = c.most_common(1)[0]
        print(f"\n[{label}] runs {runs}, consensus in {sum(w is not None for w in winners)}")
        print(f"  phase +1 winners: {m}/{runs} ({m / runs:.3f})")
        print(f"  winner entropy: {entropy(c):.3f} bits; among phase +1 winners {entropy(pc):.3f} bits"
              f" (log2 80 = {math.log2(80):.3f}, log2 104 = {math.log2(104):.3f})")
        print(f"  chi-square, phase +1 winners vs uniform over {len(plus)}: {chi:.1f}"
              f"  p = {chi2_sf(chi, len(plus) - 1):.4f}")
        print(f"  most frequent winner {top!r}: {topn}/{runs};"
              f" winner = /solve's best of the words invented: {best_of_invented}/{runs}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=int, default=400)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--t8", action="store_true", help="run only the QuCalc tie-break test (§12)")
    args = ap.parse_args(argv)
    if args.t8:
        t8(args.runs, args.n, args.seed)
        return 0

    for label, weights2 in (("tied: substrate frequencies", None),
                            ("control: length-2 weights 1.25^-i", [1.25 ** -i for i in range(8)])):
        rng = random.Random(args.seed)
        winners, steps = [], []
        for _ in range(args.runs):
            w, k = play(rng, args.n, weights2)
            winners.append(w)
            steps.append(k)
        report(label, winners, steps, weights2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
