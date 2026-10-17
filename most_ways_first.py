"""Does what happens the most ways happen first?  Exact checks for MostWays_First.md.

Fair coin flips stand in for histories with no preferred step.  "Ways by horizon n" is the
number of length-n strings that already contain a pattern, so it is 2^n * P(T <= n).

Prints:
  1. HHT vs THH: identical ways at every horizon, yet THH comes first 3 times in 4 (Penney).
  2. HHH vs TTHH: HHH has at least as many ways at every horizon n <= 60, yet in one shared
     history TTHH comes first 7 times in 12.  With two independent histories HHH wins, as the
     race theorem (section 2 of the doc) requires.
  3. QLF closure census W(n,d): the mode is d=2, the shallowest horizon is d=1.
"""
from fractions import Fraction as F
from functools import lru_cache


def step(p, s, c):
    """KMP automaton: longest prefix of p that is a suffix of p[:s]+c."""
    t = p[:s] + c
    while t and not p.startswith(t):
        t = t[1:]
    return len(t)


def first_hit(p, N):
    """dist[n] = number of length-n strings whose first occurrence of p ends at n."""
    dist, v = [0] * (N + 1), {0: 1}
    for n in range(1, N + 1):
        w = {}
        for s, c0 in v.items():
            for c in "HT":
                t = step(p, s, c)
                if t == len(p):
                    dist[n] += c0
                else:
                    w[t] = w.get(t, 0) + c0
        v = w
    return dist


def ways_by(p, N):
    d = first_hit(p, N)
    return [sum(d[m] * 2 ** (n - m) for m in range(1, n + 1)) for n in range(N + 1)]


def shared_race(a, b):
    """Exact P(a occurs before b) in ONE stream of fair flips (linear solve on suffix states)."""
    states = sorted({a[:i] for i in range(len(a))} | {b[:i] for i in range(len(b))}, key=len)
    idx = {s: i for i, s in enumerate(states)}

    def nxt(s, c):
        t = s + c
        if t.endswith(a):
            return "A"
        if t.endswith(b):
            return "B"
        while t not in idx:
            t = t[1:]
        return t

    k = len(states)
    M = [[F(int(i == j)) for j in range(k)] + [F(0)] for i in range(k)]
    for s in states:
        for c in "HT":
            n = nxt(s, c)
            if n == "A":
                M[idx[s]][k] += F(1, 2)
            elif n != "B":
                M[idx[s]][idx[n]] -= F(1, 2)
    for col in range(k):
        piv = next(r for r in range(col, k) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        M[col] = [v / M[col][col] for v in M[col]]
        for r in range(k):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return M[idx[""]][k]


def independent_race(a, b, N=80):
    da, db = first_hit(a, N), first_hit(b, N)
    pa = [F(v, 2 ** n) for n, v in enumerate(da)]
    pb = [F(v, 2 ** n) for n, v in enumerate(db)]
    ca = [sum(pa[: n + 1]) for n in range(N + 1)]
    cb = [sum(pb[: n + 1]) for n in range(N + 1)]
    lt = sum(pb[j] * ca[j - 1] for j in range(1, N + 1))
    gt = sum(pa[i] * cb[i - 1] for i in range(1, N + 1))
    return float(lt), float(gt)


@lru_cache(None)
def walks(m, d, c):
    """±1 words of length m from level c to level 0 that never leave [-d, d]."""
    if abs(c) > d:
        return 0
    if m == 0:
        return 1 if c == 0 else 0
    return walks(m - 1, d, c + 1) + walks(m - 1, d, c - 1)


def N_census(n, d):
    """N(n,d) of lean/QLF_ClosureMultiplicity.lean: balanced histories closing by depth d."""
    return walks(2 * n, d, 0)


def W_census(n, d):
    return N_census(n, d) - (N_census(n, d - 1) if d >= 1 else 0)


if __name__ == "__main__":
    H = 60
    for a, b in [("HHT", "THH"), ("HHH", "TTHH")]:
        wa, wb = ways_by(a, H), ways_by(b, H)
        dom = all(x >= y for x, y in zip(wa, wb))
        eq = wa == wb
        print(f"{a} vs {b}: ways by n=3..9  {a}={wa[3:10]}  {b}={wb[3:10]}")
        print(f"   {a} has >= ways at every n <= {H}: {dom}   identical: {eq}")
        print(f"   one shared history:   P({a} first) = {shared_race(a, b)}")
        lt, gt = independent_race(a, b)
        print(f"   independent histories: P({a} first) = {lt:.4f}, P({b} first) = {gt:.4f}")
    print("QLF closure census W(n,d), d = 1..n:")
    for n in range(3, 9):
        row = [W_census(n, d) for d in range(1, n + 1)]
        mode = 1 + row.index(max(row))
        print(f"   n={n}: {row}   shallowest d=1, modal d={mode}")
