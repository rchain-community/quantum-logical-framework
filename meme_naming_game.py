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


def play(rng: random.Random, n: int, weights2=None, max_steps: int = 10 ** 7) -> tuple:
    inv = [[] for _ in range(n)]
    for step in range(1, max_steps + 1):
        s, h = rng.sample(range(n), 2)
        if not inv[s]:
            inv[s].append(invent(rng, weights2))
        w = rng.choice(inv[s])
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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--runs", type=int, default=400)
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)

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
