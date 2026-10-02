#!/usr/bin/env python3
"""A population of memes on the closure walk (Memetics_QLF.md §8 T6, results in §9).

N agents. Each has a variant k in {1,2,3,4}: its twists use the first k axes of
(Y, X, Z, gauge), so k = 2 is the two-spatial-axis alphabet and k = 4 the full one.
Each tick every agent appends a uniform twist from its alphabet. A strand that closes
alone, or jointly with the partner it meets this tick (displacements cancel), resets:
that is a record. A strand whose l1 distance from balance passes the horizon R is lost,
and the agent is replaced by a copy of a uniformly chosen agent (variant inherited,
fresh strand). Persistence needs closure; copying is blind to content.

Only the walk position matters for any of these rules, so agents carry x in Z^4.

Run: python3 meme_population.py [--seeds 20] [--n 400] [--horizon 6] [--ticks 2000]
"""
from __future__ import annotations

import argparse
import random

STEPS = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1), (3, 1), (3, -1)]
ALPHABET = {k: STEPS[: 2 * k] for k in (1, 2, 3, 4)}


def run(seed: int, n: int, horizon: int, ticks: int) -> dict:
    rng = random.Random(seed)
    variant = [1 + (i % 4) for i in range(n)]
    x = [[0, 0, 0, 0] for _ in range(n)]
    records = {k: 0 for k in ALPHABET}
    losses = {k: 0 for k in ALPHABET}
    order = list(range(n))
    extinct = {}
    for tick in range(1, ticks + 1):
        for i in range(n):
            a, s = rng.choice(ALPHABET[variant[i]])
            x[i][a] += s
        for i in range(n):
            if not any(x[i]):
                records[variant[i]] += 1
        rng.shuffle(order)
        for p in range(0, n - 1, 2):
            i, j = order[p], order[p + 1]
            if any(x[i]) and all(x[i][c] + x[j][c] == 0 for c in range(4)):
                records[variant[i]] += 1
                records[variant[j]] += 1
                x[i] = [0, 0, 0, 0]
                x[j] = [0, 0, 0, 0]
        for i in range(n):
            if sum(map(abs, x[i])) > horizon:
                losses[variant[i]] += 1
                variant[i] = variant[rng.randrange(n)]
                x[i] = [0, 0, 0, 0]
        present = set(variant)
        for k in ALPHABET:
            if k not in present and k not in extinct:
                extinct[k] = tick
        if len(present) == 1:
            break
    share = {k: variant.count(k) / n for k in ALPHABET}
    return {"share": share, "records": records, "losses": losses, "extinct": extinct}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", type=int, default=20)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--horizon", type=int, default=6)
    ap.add_argument("--ticks", type=int, default=2000)
    args = ap.parse_args(argv)

    mean = {k: 0.0 for k in ALPHABET}
    monotone = 0
    winners = {k: 0 for k in ALPHABET}
    for seed in range(args.seeds):
        r = run(seed, args.n, args.horizon, args.ticks)
        sh = r["share"]
        for k in ALPHABET:
            mean[k] += sh[k] / args.seeds
        winners[max(sh, key=sh.get)] += 1
        ex = r["extinct"]
        big = args.ticks + 1                  # never extinct within the run
        if sh[1] > sh[4] and ex.get(4, big) <= ex.get(3, big) <= ex.get(2, big) <= ex.get(1, big):
            monotone += 1
        if seed < 3:
            print(f"seed {seed}: share {sh}  extinct at tick {r['extinct']}\n"
                  f"        records {r['records']}  losses {r['losses']}")
    print(f"\nN={args.n} R={args.horizon} ticks<={args.ticks} seeds={args.seeds}")
    print("mean final share by variant k:", {k: round(v, 4) for k, v in mean.items()})
    print("seeds won by each k:", winners)
    print(f"seeds where variants die out in the order k = 4, 3, 2: {monotone}/{args.seeds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
