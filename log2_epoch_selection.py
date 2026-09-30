#!/usr/bin/env python3
"""
log2_epoch_selection.py — Route 7 of Log2_Search.md.

S1: a binary-closure clock (each step closes with probability 1/2) has mean rate E[1/K] = sum 2^-k/k = log 2.
S2: the observed epoch as the peak of the horizon's count of new closures, in flat matter + constant Lambda:
    Omega_L = tanh^2 x, H = H_inf coth x, x = (3/2) H_inf t, Hubble-horizon entropy S ~ H^-2 ~ tanh^2 x.
    S2a: dS/d ln t = t dS/dt ; S2b: dS/dt.
Pre-registered before this script was run. Pure Python.
"""
import math

LOG2 = math.log(2)
PLANCK, SIG = 0.6847, 0.0073


def argmax(f, lo=1e-4, hi=10.0):
    for _ in range(300):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


def dSdx(x):  # S ~ tanh^2 x (units of H_inf^-2); dS/dx = 2 tanh x sech^2 x
    return 2 * math.tanh(x) / math.cosh(x) ** 2


def main():
    print("Route 7 — binary-closure clock and epoch selection (Log2_Search.md)\n")
    s1 = sum(2.0 ** -k / k for k in range(1, 200))
    print(f"S1  E[1/K] for K ~ Geometric(1/2) = {s1:.12f}   log 2 = {LOG2:.12f}")
    print(f"    clock ratio sqrt(E[1/K]) = {math.sqrt(s1):.6f}\n")
    for name, f in (("S2a  dS/d ln t = x dS/dx", lambda x: x * dSdx(x)),
                    ("S2b  dS/dt     ~ dS/dx", dSdx)):
        x = argmax(f)
        ol = math.tanh(x) ** 2
        verdict = "explains 'now'" if abs(ol - PLANCK) <= 2 * SIG else "does not explain 'now'"
        print(f"{name}: peak x = {x:.6f}, Omega_L = {ol:.6f} ({(ol - PLANCK) / SIG:+.1f} sigma from Planck, "
              f"{ol - LOG2:+.5f} from log 2) -> {verdict}")


if __name__ == "__main__":
    main()
