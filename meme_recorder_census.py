#!/usr/bin/env python3
"""Shared closures of intersecting light cones: what each partner holds.

Answers the pre-registered tests T2, T2b, T3 and T4 of Memetics_QLF.md §8 (results in §9).

Setting: two open strands A, B of length l meet; they make a shared closure when A ++ B
is count-balanced. The coupled sector is where A alone is not balanced. Counts are exact
and uniform over the coupled sector.

T2   H(x_A): bits about A's displacement that B holds (B's displacement is -x_A).
T2b  H(sigma), I(sigma; A), I(sigma; B): is the closure sign bi-local?
T3   mean over pairs of H(sigma | A, B) across uniform shuffles of A and B (the schedule).
T4   records as first closures: probability mass of first closures by depth, on the
     two-letter phase walk of QLF_ClosureMultiplicity and on the 8-twist walk.

Run: python3 meme_recorder_census.py [--max-l 4] [--t4-len 40]
"""
from __future__ import annotations

import argparse
import itertools
import math
from collections import Counter, defaultdict
from fractions import Fraction

from twist_core import pauli_fold, TWISTS

AX = {"^": (0, 1), "v": (0, -1), ">": (1, 1), "<": (1, -1),
      "/": (2, 1), "\\": (2, -1), "+": (3, 1), "-": (3, -1)}


def disp(w: str) -> tuple:
    x = [0, 0, 0, 0]
    for t in w:
        a, s = AX[t]
        x[a] += s
    return tuple(x)


def fold_key(w: str) -> tuple:
    return tuple((round(z.real), round(z.imag)) for z in pauli_fold(w))


def mat_mul(p: tuple, q: tuple) -> tuple:
    a, b, c, d = (complex(*z) for z in p)
    e, f, g, h = (complex(*z) for z in q)
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def H(counts) -> float:
    tot = sum(counts)
    return -sum(c / tot * math.log2(c / tot) for c in counts if c)


def anticommute(t: str, u: str) -> bool:
    a, b = AX[t][0], AX[u][0]
    return a != b and a != 3 and b != 3


def shuffle_odd_fraction(A: str, B: str) -> Fraction:
    """Fraction of interleavings of A and B (each in order) whose reordering parity
    relative to A ++ B is odd. Placing b_j when i letters of A are already down puts b_j
    before a_i..a_{l-1}; each anticommuting pair among those flips the sign."""
    la, lb = len(A), len(B)
    # cost[i][j]: anticommuting letters in A[i:] against B[j]
    cost = [[sum(anticommute(A[k], B[j]) for k in range(i, la)) for j in range(lb)]
            for i in range(la + 1)]
    dp = [[(0, 0)] * (lb + 1) for _ in range(la + 1)]   # (even, odd)
    dp[0][0] = (1, 0)
    for i in range(la + 1):
        for j in range(lb + 1):
            if i == j == 0:
                continue
            ev = od = 0
            if i > 0:
                e, o = dp[i - 1][j]
                ev += e; od += o
            if j > 0:
                e, o = dp[i][j - 1]
                if cost[i][j - 1] % 2:
                    e, o = o, e
                ev += e; od += o
            dp[i][j] = (ev, od)
    e, o = dp[la][lb]
    return Fraction(o, e + o)


def shared_closure_layer(l: int) -> dict:
    words = ["".join(p) for p in itertools.product(TWISTS, repeat=l)]
    by_x = defaultdict(list)
    for w in words:
        by_x[disp(w)].append(w)
    fk = {w: fold_key(w) for w in words}

    pairs = 0
    x_dist = Counter()
    sig = Counter()
    sig_given_A = defaultdict(Counter)   # keyed by A's (x, fold): the whole word is redundant
    sig_given_B = defaultdict(Counter)
    shuffle_H = 0.0
    shuffle_cache: dict = {}
    for x, As in by_x.items():
        if x == (0, 0, 0, 0):
            continue                      # coupled sector only
        Bs = by_x.get(tuple(-c for c in x), [])
        if not Bs:
            continue
        for A in As:
            for B in Bs:
                m = mat_mul(fk[A], fk[B])
                s = round(m[0].real)
                assert abs(abs(s) - 1) < 1e-9 and abs(m[1]) < 1e-9 and abs(m[0] - m[3]) < 1e-9
                pairs += 1
                x_dist[x] += 1
                sig[s] += 1
                sig_given_A[(x, fk[A])][s] += 1
                sig_given_B[(tuple(-c for c in x), fk[B])][s] += 1
                key = ("".join("XYZG"[AX[t][0]] for t in A), "".join("XYZG"[AX[t][0]] for t in B))
                if key not in shuffle_cache:
                    shuffle_cache[key] = shuffle_odd_fraction(A, B)
                q = float(shuffle_cache[key])
                shuffle_H += 0.0 if q in (0.0, 1.0) else -(q * math.log2(q) + (1 - q) * math.log2(1 - q))

    h_sig = H(sig.values())

    def cond(table):
        return sum(sum(c.values()) / pairs * H(c.values()) for c in table.values())

    return {
        "l": l, "coupled_pairs": pairs, "H_xA": H(x_dist.values()),
        "sign_plus": sig[1], "sign_minus": sig[-1], "H_sigma": h_sig,
        "I_sigma_A": h_sig - cond(sig_given_A), "I_sigma_B": h_sig - cond(sig_given_B),
        "mean_H_sigma_given_AB_over_shuffles": shuffle_H / pairs if pairs else 0.0,
    }


def first_closure_mass_1d(max_len: int) -> dict:
    """Two-letter phase walk: mass 2^-L of first returns at length L, by depth."""
    mass = defaultdict(Fraction)
    # state: (position, max |position|) for paths that have not yet returned
    cur = Counter({(1, 1): 1, (-1, 1): 1})
    for L in range(2, max_len + 1):
        nxt = Counter()
        for (p, m), c in cur.items():
            for s in (1, -1):
                q = p + s
                if q == 0:
                    mass[m] += Fraction(c, 2 ** L)
                else:
                    nxt[(q, max(m, abs(q)))] += c
        cur = nxt
    return dict(mass)


def first_closure_mass_8(max_len: int) -> dict:
    """8-twist walk on Z^4: mass 8^-L of first returns, by l1 max excursion."""
    steps = list(AX.values())
    mass = defaultdict(Fraction)
    cur = Counter()
    for a, s in steps:
        x = [0, 0, 0, 0]; x[a] += s
        cur[(tuple(x), 1)] += 1
    for L in range(2, max_len + 1):
        nxt = Counter()
        for (x, m), c in cur.items():
            for a, s in steps:
                y = list(x); y[a] += s; y = tuple(y)
                if y == (0, 0, 0, 0):
                    mass[m] += Fraction(c, 8 ** L)
                else:
                    nxt[(y, max(m, sum(map(abs, y))))] += c
        cur = nxt
    return dict(mass)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max-l", type=int, default=4)
    ap.add_argument("--t4-len", type=int, default=40)
    ap.add_argument("--t4-len8", type=int, default=12)
    args = ap.parse_args(argv)

    print("T2 / T2b / T3: coupled shared closures A ++ B, |A| = |B| = l")
    print(f"{'l':>2} {'pairs':>9} {'H(x_A)':>7} {'sigma +/-':>17} {'H(sigma)':>8}"
          f" {'I(s;A)':>7} {'I(s;B)':>7} {'H(s|A,B) shuffles':>18}")
    for l in range(1, args.max_l + 1):
        r = shared_closure_layer(l)
        print(f"{l:>2} {r['coupled_pairs']:>9} {r['H_xA']:>7.3f} "
              f"{r['sign_plus']:>8}/{r['sign_minus']:<8} {r['H_sigma']:>8.4f}"
              f" {r['I_sigma_A']:>7.4f} {r['I_sigma_B']:>7.4f}"
              f" {r['mean_H_sigma_given_AB_over_shuffles']:>18.4f}")

    print(f"\nT4: first-closure (record) mass by depth")
    m1 = first_closure_mass_1d(args.t4_len)
    tot1 = sum(m1.values())
    print(f"  two-letter phase walk, L <= {args.t4_len} (captured mass {float(tot1):.4f}):")
    for d in sorted(m1)[:5]:
        print(f"    depth {d}: {float(m1[d]):.6f}")
    m8 = first_closure_mass_8(args.t4_len8)
    tot8 = sum(m8.values())
    print(f"  8-twist walk, L <= {args.t4_len8} (captured mass {float(tot8):.6f}):")
    for d in sorted(m8)[:6]:
        print(f"    depth {d}: {float(m8[d]):.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
