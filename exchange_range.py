#!/usr/bin/env python3
"""
exchange_range.py -- does the no-flip exchange reach a distant absorber? (Carbon_Superconductivity.md sec 41;
pre-registered in commit 179ff12, before this script was written).

Emitter at the origin, absorber at R d, R = 1..12. The exchange is a walk of N = R + 2k steps on the cubic lattice
(each step one spatial twist's displacement), k = 0..3. The emitter's twist t sets the class (sec 40a): t on d's
axis = no-flip (s = 0), t perpendicular to d = spin-flip (s = +-1).

  W1  fold sign: each walk counts with c in sigma(t) F(P) sigma(t)^-1 = c F(P); a step on t's axis gives +1,
      any other step -1 (Pauli anticommutation). A(R, k) = signed sum, max |A| over t in the class.
  W2  the twists are the path's ends: first step = t's displacement, last step = t+ read forward, which moves
      with t (sec 38a C1). A(R, k) = number of such walks, max over t in the class.

Test: rho(R) = |A0| / |A1|. Pass if, for every k where both are non-zero, rho(R + 2) <= rho(R) over R = 2..10 and
rho(12) <= rho(2) / 2.

Exact integer arithmetic. Stdlib only, plus twist_core.
Run:  python3 exchange_range.py
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Fr

from twist_core import calculate_action

SPATIAL = ['^', 'v', '>', '<', '/', '\\']
R_MAX, K_MAX = 12, 3


def disp(t):
    v, h, d, _ = calculate_action(t)
    return (h, v, d)


def axis(vec):
    return next(i for i, x in enumerate(vec) if x)


STEPS = [disp(t) for t in SPATIAL]


def walks(start, n, weight):
    """{endpoint: weighted count} of n-step walks from start; weight(step) multiplies per step."""
    cur = {start: 1}
    for _ in range(n):
        nxt = defaultdict(int)
        for (x, y, z), w in cur.items():
            for st in STEPS:
                nxt[(x + st[0], y + st[1], z + st[2])] += w * weight(st)
        cur = nxt
    return cur


def amp_w1(t, d, R, k):
    a = axis(disp(t))
    end = tuple(R * x for x in d)
    return walks((0, 0, 0), R + 2 * k, lambda st: 1 if axis(st) == a else -1).get(end, 0)


def amp_w2(t, d, R, k):
    n, p = R + 2 * k, disp(t)
    end = tuple(R * x for x in d)
    if n == 1:
        return int(p == end)
    inner_end = tuple(e - q for e, q in zip(end, p))
    return walks(p, n - 2, lambda st: 1).get(inner_end, 0)


def classes(d):
    a = axis(d)
    no_flip = [t for t in SPATIAL if axis(disp(t)) == a]
    flip = [t for t in SPATIAL if axis(disp(t)) != a]
    return no_flip, flip


def table(amp, d):
    no_flip, flip = classes(d)
    out = {}
    for k in range(K_MAX + 1):
        for R in range(1, R_MAX + 1):
            a0 = max(abs(amp(t, d, R, k)) for t in no_flip)
            a1 = max(abs(amp(t, d, R, k)) for t in flip)
            out[k, R] = (a0, a1)
    return out


def verdict(tab):
    results = {}
    for k in range(K_MAX + 1):
        rho = {R: Fr(a0, a1) for (kk, R), (a0, a1) in tab.items() if kk == k and a0 and a1}
        if not rho:
            results[k] = 'A1 = 0 or A0 = 0 at every R'
            continue
        span = [R for R in range(2, R_MAX + 1) if R in rho]
        falls = all(rho[R + 2] <= rho[R] for R in span if R + 2 in rho)
        halves = 2 in rho and 12 in rho and rho[12] <= rho[2] / 2
        results[k] = ('falls' if falls and halves else 'does not fall', rho)
    return results


def main():
    d = (1, 0, 0)
    for name, amp in (('W1 fold sign', amp_w1), ('W2 twists as the path ends', amp_w2)):
        tab = table(amp, d)
        # the other five directions must give the same table (cubic symmetry)
        for t in SPATIAL[:]:
            dd = disp(t)
            if dd != d:
                assert table(amp, dd) == tab, (name, dd)
        print(f"=== {name} (d = +x; the other five directions agree) ===")
        res = verdict(tab)
        any_pass = False
        all_a1_zero = True
        for k in range(K_MAX + 1):
            row = [tab[k, R] for R in range(1, R_MAX + 1)]
            print(f"  k={k}  |A0|,|A1| by R: {row}")
            r = res[k]
            if isinstance(r, str):
                print(f"        {r}")
                continue
            label, rho = r
            if any(a1 for (kk, R), (a0, a1) in tab.items() if kk == k):
                all_a1_zero = False
            print(f"        rho: " + ", ".join(f"R{R}={float(v):.4g}" for R, v in sorted(rho.items())))
            print(f"        -> {label}")
            any_pass |= label == 'falls'
        tested = [k for k in range(K_MAX + 1) if not isinstance(res[k], str)]
        ok = tested and all(res[k][0] == 'falls' for k in tested)
        print(f"  {name}: {'PASS' if ok else 'FAIL'}"
              f"{'  (A1 = 0 at every k)' if all_a1_zero else ''}\n")


if __name__ == '__main__':
    main()
