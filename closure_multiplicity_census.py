#!/usr/bin/env python3
"""
closure_multiplicity_census.py — how many ways close at each depth, and where the mode sits.

Issue #171 asked whether "what happens in the most ways happens first" holds for the closure
census, and asked that the answer be counted rather than assumed. A balanced, gauge-free history
of length 2n is a +-1 bridge; by the depth law (QLF_ClosureDepthLaw) its closure depth is its
maximum excursion. So

    N(n, d) = # bridges of length 2n confined to [-d, d]   (closing BY depth d)
    W(n, d) = N(n, d) - N(n, d - 1)                         (closing AT depth d)

N is computed exactly by the transfer recurrence that lean/QLF_ClosureMultiplicity.lean proves
equal to the census (`N_eq_dp`). Nothing about the ordering is built in.

RESULT (Outcome C of the issue)
  * W(n,1) = 2^n and W(n,n) = 2 are recovered (Lean: W_one, W_self).
  * W(n,2) = 2*3^(n-1) - 2^n (Lean: W_two), which beats W(n,1) for every n >= 3
    (Lean: depth_one_not_modal). Depth 1 is modal only for n <= 2.
  * The strata are unimodal with modal depth d*(n) ~ sqrt(n): 2 for n = 3..7, 3 for n = 8..13,
    4 at n = 20, 10 at n = 100, 29 at n = 800. The depth-1 share is 2^n / C(2n,n) -> 0.
  * So "shallowest closes first" holds (a capacity-R horizon closes exactly maxExcursion <= R),
    but "shallowest is most ways" is false from n = 3 on. The sqrt(n) growth is observed here,
    not proved.

Run:  python3 closure_multiplicity_census.py          # table + checks, n <= 30 and a few large n
      python3 closure_multiplicity_census.py --brute  # also cross-check N against brute force, n <= 9
"""
from itertools import product
from math import comb, isqrt
import sys


def bounded_bridges(n: int, d: int) -> int:
    """N(n, d): +-1 walks of 2n steps from 0 to 0 that never leave [-d, d]."""
    if d < 0:
        return 0
    v = [0] * (2 * d + 1)
    v[d] = 1
    for _ in range(2 * n):
        w = [0] * (2 * d + 1)
        for i, c in enumerate(v):
            if c:
                if i > 0:
                    w[i - 1] += c
                if i < 2 * d:
                    w[i + 1] += c
        v = w
    return v[d]


def strata(n: int) -> list[int]:
    """[W(n,1), ..., W(n,n)]."""
    N = [bounded_bridges(n, d) for d in range(n + 1)]
    return [N[d] - N[d - 1] for d in range(1, n + 1)]


def brute_strata(n: int) -> list[int]:
    out = [0] * (n + 1)
    for w in product((1, -1), repeat=2 * n):
        s, m = 0, 0
        for x in w:
            s += x
            m = max(m, abs(s))
        if s == 0:
            out[m] += 1
    return out[1:]


def modal_depth(ws: list[int]) -> int:
    return max(range(len(ws)), key=lambda i: ws[i]) + 1


def unimodal(ws: list[int]) -> bool:
    k = modal_depth(ws) - 1
    return all(ws[i] <= ws[i + 1] for i in range(k)) and \
        all(ws[i] >= ws[i + 1] for i in range(k, len(ws) - 1))


def main() -> int:
    fail = []
    if "--brute" in sys.argv:
        for n in range(1, 10):
            if strata(n) != brute_strata(n):
                fail.append(f"n={n}: recurrence disagrees with brute force")
        print("brute-force cross-check n <= 9:", "ok" if not fail else "FAILED")

    print(f"{'n':>4} {'d*':>3} {'d*/sqrt n':>9}  {'monotone':>8}  W(n,1..min(n,6))")
    for n in list(range(1, 31)) + [50, 100, 200, 400, 800]:
        ws = strata(n)
        if sum(ws) != comb(2 * n, n):
            fail.append(f"n={n}: strata do not sum to C(2n,n)")
        if ws[0] != 2 ** n:
            fail.append(f"n={n}: W(n,1) != 2^n (contradicts W_one)")
        if ws[-1] != 2:
            fail.append(f"n={n}: W(n,n) != 2 (contradicts W_self)")
        if n >= 2 and ws[1] != 2 * 3 ** (n - 1) - 2 ** n:
            fail.append(f"n={n}: W(n,2) != 2*3^(n-1) - 2^n (contradicts W_two)")
        strict = all(ws[i] > ws[i + 1] for i in range(len(ws) - 1))
        ds = modal_depth(ws)
        if n >= 3 and (strict or ds == 1):
            fail.append(f"n={n}: depth 1 modal (contradicts depth_one_not_modal)")
        if not unimodal(ws):
            fail.append(f"n={n}: strata are not unimodal")
        print(f"{n:>4} {ds:>3} {ds / n ** 0.5:>9.3f}  {str(strict):>8}  {ws[:6] if n <= 20 else ''}")

    print()
    print("depth-1 share 2^n / C(2n,n):",
          ", ".join(f"n={n}: {2 ** n / comb(2 * n, n):.3g}" for n in (3, 10, 30, 100)))
    if fail:
        print("\nFAILED:\n  " + "\n  ".join(fail))
        return 1
    print("\nall checks hold: W(n,1)=2^n, W(n,n)=2, W(n,2)=2*3^(n-1)-2^n, depth 1 not modal for "
          "n>=3, strata unimodal.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
