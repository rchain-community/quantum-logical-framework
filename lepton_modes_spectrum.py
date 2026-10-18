"""
Leak test for 2, 3, 4 equal-weight modes, done by Fermi's golden rule.
A weak neutrino channel at frequency D drains power at a rate proportional to
the power spectrum of the mode amplitude a_0(t) near D.  So instead of a
damped channel (whose Lorentzian tail leaks even from a regular orbit), measure
the spectrum directly: fraction of a_0's power in the band [D-0.5, D+0.5].
Also reports the largest Lyapunov exponent for N = 4.
Model and rhs/rk4 are those of lepton_modes_decay_sim.py.
"""
import numpy as np, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from lepton_modes_decay_sim import rk4, equal_weight, lyapunov

def band_power(N, g, D_list, rng, runs, T=1600.0, dt=0.02):
    z = equal_weight(N, rng, runs)
    for _ in range(int(200 / dt)):           # discard transient
        z = rk4(z, dt, g, N)
    n = int(T / dt); rec = np.empty((runs, n), complex)
    for i in range(n):
        z = rk4(z, dt, g, N); rec[:, i] = z[:, 0]
    S = np.abs(np.fft.fft(rec * np.hanning(n), axis=1)) ** 2
    f = 2 * np.pi * np.fft.fftfreq(n, dt)      # angular frequency
    S /= S.sum(axis=1, keepdims=True)
    # measure detuning from each run's own dominant line (the "rest frequency")
    f0 = f[np.argmax(S, axis=1)]
    out = []
    for D in D_list:
        m = np.abs(np.abs(f[None, :] - f0[:, None]) - D) < 0.5
        out.append(np.median((S * m).sum(axis=1)))
    return out

if __name__ == "__main__":
    runs, Ds = 32, (4.0, 8.0)
    print("Largest Lyapunov exponent for N = 4 (32 runs, > 0.02 chaotic)")
    for g in (0.5, 2.0, 4.0, 6.0, 10.0):
        L = lyapunov(4, g, np.random.default_rng(1), runs)
        print(f"  g={g:4.1f}: max {L.max():.4f}, chaotic {int((L > 0.02).sum())}/{runs}", flush=True)
    print("\nGolden-rule leak: median fraction of a_0 power at detuning D (+-0.5) from its main line")
    for g in (2.0, 6.0, 10.0):
        row = [band_power(N, g, Ds, np.random.default_rng(3), runs) for N in (2, 3, 4)]
        for k, D in enumerate(Ds):
            print(f"  g={g:4.1f} D={D:4.1f}:  N=2 {row[0][k]:.1e}   N=3 {row[1][k]:.1e}   N=4 {row[2][k]:.1e}", flush=True)
