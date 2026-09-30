#!/usr/bin/env python3
"""
omega_lambda_octave.py — Route 1 (the octave route) of Log2_Search.md.

Pre-registered in Log2_Search.md before this script was run. Flat universe with matter and a constant
Lambda, radiation neglected:
    Omega_L(t) = tanh^2 x,  H = H_inf coth x,  a ~ sinh^(2/3) x,  x = (3/2) H_inf t.
An octave condition compares age t with age t/2.

  O1  a(t) = 2 a(t/2)        forecast: Omega_L = 8/9
  O2  H(t/2) = 2 H(t)        forecast: only as t -> 0
  G   algebraic octave conditions give algebraic Omega_L, never log 2 (checked here through the
      u = tanh(x/2) identities it rests on)
  O4  Omega_L = int_w^2w dw/w = log 2 by construction; prints the predictions every log-2 mechanism shares

Pure Python, no dependencies, under a second.
"""
import math

LOG2 = math.log(2)
PLANCK_OL, PLANCK_SIG = 0.6847, 0.0073     # Planck 2018 TT,TE,EE+lowE+lensing


def omega_L(x):
    return math.tanh(x) ** 2


def q_of(x):
    ol = omega_L(x)
    return 0.5 * (1 - ol) - ol


def Ht_of(x):
    return (2.0 / 3.0) * x / math.tanh(x)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def report(name, x):
    ol = omega_L(x)
    print(f"  {name}: x = {x:.6f}  Omega_L = {ol:.6f}  q = {q_of(x):+.4f}  H t = {Ht_of(x):.4f}")
    print(f"      vs log 2: {ol - LOG2:+.4f}   vs Planck: {(ol - PLANCK_OL) / PLANCK_SIG:+.1f} sigma")
    return ol


def main():
    print("Route 1 — the octave route (Log2_Search.md)\n")

    # O1: a(t)/a(t/2) = (sinh x / sinh(x/2))^(2/3) = 2
    print("O1  a(t) = 2 a(t/2)")
    x1 = bisect(lambda x: (math.sinh(x) / math.sinh(x / 2)) ** (2 / 3) - 2, 1e-6, 20)
    ol1 = report("O1", x1)
    print(f"      closed form 8/9 = {8 / 9:.6f}  (match: {abs(ol1 - 8 / 9) < 1e-9})\n")

    # O2: H(t/2)/H(t) = coth(x/2)/coth(x); = 2 would be the scale-free law across the octave
    print("O2  H(t/2) = 2 H(t)")
    ratios = [(x, (1 / math.tanh(x / 2)) / (1 / math.tanh(x))) for x in (1e-4, 0.01, 0.1, 0.5, 1, 2, 5)]
    for x, r in ratios:
        print(f"      x = {x:<7} Omega_L = {omega_L(x):.4f}  H(t/2)/H(t) = {r:.6f}")
    below = all(r < 2 for x, r in ratios)
    print(f"      ratio < 2 at every sampled x > 0: {below};  -> 2 only as x -> 0 (matter era)\n")

    # G: the identities the algebraicity argument rests on, with u = tanh(x/2)
    print("G   u = tanh(x/2) identities (the algebraicity argument)")
    worst = 0.0
    for x in (0.3, 0.9, 1.7627, 3.0):
        u = math.tanh(x / 2)
        checks = [
            math.tanh(x) - 2 * u / (1 + u * u),
            1 / math.tanh(x) - (1 + u * u) / (2 * u),
            omega_L(x) - 4 * u * u / (1 + u * u) ** 2,
            math.sinh(x) / math.sinh(x / 2) - 2 / math.sqrt(1 - u * u),
        ]
        worst = max(worst, max(abs(c) for c in checks))
    print(f"      max identity error: {worst:.1e}  (all rational/algebraic in u)\n")

    # O4: the identification, and the predictions shared by every log-2 mechanism
    print("O4  Omega_L = int_w^2w dw/w = log 2 (by construction)")
    x4 = math.atanh(math.sqrt(LOG2))
    report("O4", x4)
    print("      q0 and H0 t0 above follow from Omega_L = log 2 alone; they cannot tell mechanisms apart.")


if __name__ == "__main__":
    main()
