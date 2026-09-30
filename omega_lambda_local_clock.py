#!/usr/bin/env python3
"""
omega_lambda_local_clock.py — Route 4 (log-uniform over one e-fold, by a local clock) of Log2_Search.md.

Pre-registered before this script was run. Local clock: log-time tau = ln t. Flat matter + constant
Lambda: Omega_L = tanh^2 x, H t = (2/3) x coth x, q = (1 - 3 Omega_L)/2, x = (3/2) H_inf t.

  L1   last octave / last e-fold of own-clock time = log 2 at every epoch (identity)
  L1'  = T_half / tau_mean for half-per-octave decay (identity)
  L2   density ratios are clock-independent (illustrated by reparametrizing time)
  L2'  naive Omega_tau = Omega_L / (H t)^2 varies with epoch
  L3   Omega_L = log 2 only at one epoch (q = -0.540)
  L4   shares of our last own-clock e-fold spent (a) accelerating, (b) with rho_L > rho_m (Planck LCDM)
Pure Python.
"""
import math

LOG2 = math.log(2)
OL0 = 0.6847  # Planck 2018


def ol(x):
    return math.tanh(x) ** 2


def Ht(x):
    return (2 / 3) * x / math.tanh(x)


def x_of_OL(o):
    return math.atanh(math.sqrt(o))


def main():
    print("Route 4 — log-uniform over one e-fold, by a local clock (Log2_Search.md)\n")

    print("L1  last octave / last e-fold, in log-time")
    for t in (1e-40, 1.0, 13.8, 1e10):
        print(f"      t = {t:<8g}: (ln t - ln(t/2)) / (ln t - ln(t/e)) = {(math.log(t) - math.log(t / 2)) / 1.0:.12f}")
    lam = 1.0  # half per octave: hazard per e-fold of age = log2 / log2
    print(f"L1' half per octave: T_half = log 2 e-folds, tau_mean = 1/lambda = {1 / lam:.1f} e-fold,"
          f" ratio = {LOG2 / (1 / lam):.12f}\n")

    print("L2  density ratio under a change of clock (t -> s = t^3, t -> ln t): the ratio at an event")
    x = x_of_OL(OL0)
    print(f"      rho_L/rho_tot at today's event = {ol(x):.6f} whichever clock labels the event "
          "(densities are per volume, not per unit time)\n")

    print("L2' naive own-clock Omega_tau = Omega_L / (H t)^2")
    for o in (0.1, 0.3, 0.5, 0.6847, LOG2, 0.8, 0.95):
        xx = x_of_OL(o)
        print(f"      Omega_L = {o:.4f}: H t = {Ht(xx):.4f}, Omega_tau = {o / Ht(xx) ** 2:.4f}")
    print()

    print("L3  Omega_L = log 2 happens once:")
    x3 = x_of_OL(LOG2)
    print(f"      x = {x3:.4f}, q = {(1 - 3 * LOG2) / 2:+.4f}, H t = {Ht(x3):.4f}\n")

    print("L4  our last own-clock e-fold (t0/e to t0), Planck LCDM, shares in log-time")
    x0 = x_of_OL(OL0)
    x_start = x0 / math.e                       # x is proportional to t
    x_acc = x_of_OL(1 / 3)                      # q = 0
    x_eq = x_of_OL(0.5)                         # rho_L = rho_m
    def share(xa):
        lo = max(xa, x_start)
        return max(0.0, math.log(x0 / lo)) if lo < x0 else 0.0
    sa, sb = share(x_acc), share(x_eq)
    print(f"      (a) accelerating:      {sa:.4f}   (log 2 = {LOG2:.4f}, diff {sa - LOG2:+.4f})")
    print(f"      (b) rho_L > rho_m:     {sb:.4f}   (diff {sb - LOG2:+.4f})")
    print(f"      acceleration began at t = {x_acc / x0:.4f} t0 = {13.80 * x_acc / x0:.2f} Gyr;"
          f" rho_L = rho_m at {13.80 * x_eq / x0:.2f} Gyr")


if __name__ == "__main__":
    main()
