"""
2 vs 3 equal-weight modes: can a small perturbation make them chaotic and leak?

Model (the simplest one with N equal, symmetrically coupled, nonlinear modes):
the discrete self-trapping / discrete nonlinear Schrodinger equation on the
complete graph of N sites,
    i da_j/dt = -C * sum_{k != j} a_k  -  g * |a_j|^2 a_j ,
with total power sum |a_j|^2 = 1 split equally (|a_j|^2 = 1/N) and random phases.
Known background (not new): the N=2 dimer is integrable (Eilbeck, Lomdahl &
Scott 1985); the N=3 trimer is not, and can be chaotic.

Two measurements, with the same rules for N = 2 and N = 3:
 1. Chaos: largest Lyapunov exponent (Benettin, two nearby trajectories).
 2. Leak ("neutrino release"): mode 0 is weakly coupled (kappa) to a damped
    outgoing channel b at detuning D, off every linear frequency of the modes:
        i db/dt = (D - i*G) b - kappa * a_0
    Power absorbed from the modes is measured after time T.  By Fermi's golden
    rule it is ~ kappa^2 * (spectral weight of a_0 near D): regular motion has
    a line spectrum and leaks only on resonance; chaotic motion is broadband.
All runs for one (N, g) are integrated together as rows of one array.
"""
import numpy as np

C = 1.0

def rhs(z, g, N, kappa=0.0, D=0.0, G=0.0):
    a = z[:, :N]
    da = 1j * (C * (a.sum(axis=1, keepdims=True) - a) + g * np.abs(a) ** 2 * a)
    if z.shape[1] > N:
        b = z[:, N]
        da[:, 0] += 1j * kappa * b
        db = -1j * ((D - 1j * G) * b - kappa * a[:, 0])
        return np.column_stack([da, db])
    return da

def rk4(z, dt, *args):
    k1 = rhs(z, *args); k2 = rhs(z + dt / 2 * k1, *args)
    k3 = rhs(z + dt / 2 * k2, *args); k4 = rhs(z + dt * k3, *args)
    return z + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

def equal_weight(N, rng, runs):
    return np.exp(2j * np.pi * rng.random((runs, N))) / np.sqrt(N)

def lyapunov(N, g, rng, runs, T=2000.0, dt=0.01, d0=1e-8):
    x = equal_weight(N, rng, runs)
    y = x + d0 * (rng.normal(size=x.shape) + 1j * rng.normal(size=x.shape))
    s = np.zeros(runs)
    for i in range(int(T / dt)):
        x = rk4(x, dt, g, N); y = rk4(y, dt, g, N)
        if i % 10 == 9:
            d = np.linalg.norm(y - x, axis=1); s += np.log(d / d0)
            y = x + (y - x) * (d0 / d)[:, None]
    return s / T

def leak(N, g, D, rng, runs, kappa=0.02, G=0.5, T=1500.0, dt=0.01):
    z = np.column_stack([equal_weight(N, rng, runs), np.zeros(runs)])
    for _ in range(int(T / dt)):
        z = rk4(z, dt, g, N, kappa, D, G)
    return 1.0 - np.sum(np.abs(z[:, :N]) ** 2, axis=1)   # power lost from the modes

if __name__ == "__main__":
    runs, gs = 32, [0.5, 2.0, 4.0, 6.0, 10.0]
    print("1. Largest Lyapunov exponent, equal weight, random phases "
          f"({runs} runs each; > 0.02 counted chaotic)")
    print(f"{'g':>5} | {'N=2 max':>8} {'chaotic':>8} | {'N=3 max':>8} {'chaotic':>8}", flush=True)
    for g in gs:
        row = []
        for N in (2, 3):
            L = lyapunov(N, g, np.random.default_rng(1), runs)
            row.append(f"{L.max():8.4f} {int((L > 0.02).sum()):>5}/{runs}")
        print(f"{g:5.1f} | {row[0]} | {row[1]}", flush=True)

    # linear frequencies: N=2 -> {+1,-1}; N=3 -> {+2,-1,-1}; nonlinear shifts ~ g/N.
    print("\n2. Power leaked into a weak detuned channel (kappa=0.02), mean over runs")
    for g in (2.0, 6.0):
        for D in (6.0, 10.0):
            row = [leak(N, g, D, np.random.default_rng(2), runs).mean() for N in (2, 3)]
            print(f"  g={g:4.1f}  detuning D={D:5.1f}:  N=2 leaked {row[0]:.2e}   "
                  f"N=3 leaked {row[1]:.2e}   ratio {row[1]/max(row[0],1e-300):8.1f}", flush=True)
