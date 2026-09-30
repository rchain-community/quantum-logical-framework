#!/usr/bin/env python3
"""
omega_lambda_vacuum_clock.py — Route 5 (half kept, half lent, on a vacuum clock) of Log2_Search.md.

Pre-registered before this script was run. The vacuum clock ticks at H_L = sqrt(8 pi G rho_L / 3), so
Omega_L = (H_L/H)^2 (V0). Lent (vacuum, w=-1) energy is realized into matter with hazard lambda*H_L,
an interacting vacuum with total nabla T = 0. In e-folds N = ln a:

    dOmega/dN = -lambda Omega^(3/2) + 3 Omega (1 - Omega)                       (V1)
    V2 adds creation Q = gamma H_L rho_c split evenly:
    dOmega/dN = (gamma/2) Omega^(1/2) - lambda Omega^(3/2) + Omega (3(1-Omega) - gamma Omega^(1/2))
    V3: hazard H_L / tau_v, tau_v = int H_L dt = int sqrt(Omega) dN

Pure Python.
"""
import math

LOG2 = math.log(2)


def fixed_point(lam):
    # lam*s = 3(1 - s^2), s = sqrt(Omega) -> 3 s^2 + lam s - 3 = 0
    s = (-lam + math.sqrt(lam * lam + 36)) / 6
    return s * s


def integrate(rhs, om0=1e-9, n_end=40.0, dn=1e-4, record=()):
    om, n, out = om0, 0.0, {}
    marks = sorted(record)
    while n < n_end:
        om = min(max(om + dn * rhs(om, n), 0.0), 1.0)
        n += dn
        while marks and n >= marks[0]:
            out[marks.pop(0)] = om
    return om, out


def main():
    print("Route 5 — half kept, half lent, on a vacuum clock (Log2_Search.md)\n")
    print(f"V0  Omega_L = (H_L/H)^2; Omega_L = log 2 <=> H_L/H = sqrt(log 2) = {math.sqrt(LOG2):.4f}\n")

    for label, lam in (("V1a lambda = 1", 1.0), ("V1b lambda = log 2", LOG2)):
        om_star = fixed_point(lam)
        om_end, marks = integrate(lambda o, n: -lam * o ** 1.5 + 3 * o * (1 - o), record=(2.0, 4.0, 6.0))
        print(f"{label}: fixed point {om_star:.6f}; integrated from Omega = 1e-9 -> {om_end:.6f}")
        early = [marks[k] for k in (2.0, 4.0, 6.0)]
        ratios = [early[1] / early[0], early[2] / early[1]]
        print(f"      early growth per 2 e-folds: x{ratios[0]:.1f}, x{ratios[1]:.1f}  (a^3 would be x{math.exp(6):.0f})")
    print(f"      closed form V1a (19 - sqrt 37)/18 = {(19 - math.sqrt(37)) / 18:.6f}")
    lam_needed = 3 * (1 - LOG2) / math.sqrt(LOG2)
    print(f"V1c lambda giving Omega* = log 2: {lam_needed:.6f}  (check: fixed point {fixed_point(lam_needed):.6f})\n")

    print("V2  with creation gamma (lambda = 1): attractor vs gamma")
    for gamma in (0.0, 0.1, 0.5, 1.0, 2.0):
        rhs = lambda o, n, g=gamma: 0.5 * g * o ** 0.5 - o ** 1.5 + o * (3 * (1 - o) - g * o ** 0.5)
        om_end, _ = integrate(rhs, om0=1e-6)
        print(f"      gamma = {gamma:<4}: Omega -> {om_end:.6f}")
    print()

    print("V3  hazard H_L / tau_v (half per octave of vacuum-clock age)")
    om, tau_v, n, dn = 1e-9, 1e-12, 0.0, 1e-4
    checkpoints = {10.0: None, 20.0: None, 40.0: None, 80.0: None}
    while n < 80.0:
        s = math.sqrt(om)
        om = min(max(om + dn * (-(1 / tau_v) * om * s / 1.0 * 1.0 + 3 * om * (1 - om)), 0.0), 1.0)
        tau_v += dn * s
        n += dn
        for c in checkpoints:
            if checkpoints[c] is None and n >= c:
                checkpoints[c] = (om, tau_v)
    for c, (o, tv) in checkpoints.items():
        print(f"      N = {c:<5}: Omega = {o:.6f}, tau_v = {tv:.3f}")


if __name__ == "__main__":
    main()
