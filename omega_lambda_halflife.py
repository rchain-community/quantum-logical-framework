#!/usr/bin/env python3
"""
omega_lambda_halflife.py — Route 2 (the half-life route) of Log2_Search.md.

Pre-registered before this script was run. Flat universe; matter (w=0) and a lent ledger (w=-1).
Creation Q = gamma*H*rho_c, half to each ledger; the lent ledger realizes into matter with hazard k/t.
In own-clock time tau = ln t, with h = H t and Omega = rho_lent/rho_c:

    dOmega/dtau = (gamma/2) h - k Omega + 3 h Omega (1 - Omega)
    dh/dtau     = h - (3/2) h^2 (1 - Omega)

Forecasts: k = 1 and k = log 2 give no steady share (Omega -> 1); steady shares need k > 2 and depend on
the free gamma via gamma/(3(1-Omega)) = (k-2) Omega. Pure Python, a few seconds.
"""
import math


def run(k, gamma, om0=1e-3, h0=2 / 3, tau_end=40.0, dt=1e-3):
    om, h, tau = om0, h0, 0.0
    while tau < tau_end:
        dom = 0.5 * gamma * h - k * om + 3 * h * om * (1 - om)
        dh = h - 1.5 * h * h * (1 - om)
        om = min(max(om + dt * dom, 0.0), 1.0)
        h += dt * dh
        tau += dt
        if h > 1e6:
            break
    return om, h, tau


def steady(k, gamma):
    """Solve gamma/(3(1-Om)) = (k-2) Om on (0,1); None if no root."""
    if k <= 2:
        return None
    f = lambda o: gamma / (3 * (1 - o)) - (k - 2) * o
    grid = [i / 10000 for i in range(1, 10000)]
    for a, b in zip(grid, grid[1:]):
        if f(a) * f(b) <= 0:
            lo, hi = a, b
            for _ in range(80):
                m = 0.5 * (lo + hi)
                lo, hi = (m, hi) if f(lo) * f(m) > 0 else (lo, m)
            return 0.5 * (lo + hi)
    return None


def main():
    print("Route 2 — the half-life route (Log2_Search.md)\n")
    for label, k in (("H1  k = 1 (half per octave)", 1.0), ("H2  k = log 2 (half per e-fold)", math.log(2))):
        print(label)
        for gamma in (0.01, 0.1, 1.0):
            om, h, tau = run(k, gamma)
            print(f"      gamma = {gamma:<5} -> Omega = {om:.6f}, h = H t = {h:.3g} at tau = {tau:.1f}")
        print()
    print("H3  steady shares for k > 2: gamma/(3(1-Omega)) = (k-2) Omega")
    for k in (3.0, 4.0):
        for gamma in (0.1, 1.0, 3.0):
            s = steady(k, gamma)
            om, h, _ = run(k, gamma, tau_end=60)
            print(f"      k = {k}, gamma = {gamma:<4}: fixed point {s if s is None else round(s, 6)}; integrated Omega = {om:.6f}")
    print("\n      The share moves with the free gamma, so no number is derived.")
    print(f"      log 2 = {math.log(2):.6f} appears only as a rate (k), never as the resulting share.")


if __name__ == "__main__":
    main()
