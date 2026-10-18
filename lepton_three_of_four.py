"""
"Four modes, three at a time": k equal-weight active modes (mutually coupled,
C=1, nonlinearity g) plus ONE extra mode detuned by D and weakly coupled (eps)
to every active mode.  The extra mode starts empty.  Off resonance, linear
coupling alone puts only ~k*(eps/D)^2 of the power there and then gives it back;
lasting transfer needs the active modes' motion to have spectral weight near D,
which regular (2-active) motion has only at isolated lines and chaotic
(3-active) motion has broadly.  Compare k = 2 (a 3-mode system) with k = 3
(a 4-mode system, "three at a time").
"""
import numpy as np

def rhs(z, k, g, eps, D):
    a, b = z[:, :k], z[:, k]
    da = 1j * ((a.sum(axis=1, keepdims=True) - a) + g * np.abs(a) ** 2 * a + eps * b[:, None])
    db = -1j * (D * b) + 1j * eps * a.sum(axis=1) + 1j * g * np.abs(b) ** 2 * b
    return np.column_stack([da, db])

def rk4(z, dt, *p):
    k1 = rhs(z, *p); k2 = rhs(z + dt/2*k1, *p); k3 = rhs(z + dt/2*k2, *p); k4 = rhs(z + dt*k3, *p)
    return z + dt/6*(k1 + 2*k2 + 2*k3 + k4)

def extra_power(k, g, eps, D, runs=32, T=3000.0, dt=0.02, seed=4):
    rng = np.random.default_rng(seed)
    z = np.column_stack([np.exp(2j*np.pi*rng.random((runs, k)))/np.sqrt(k), np.zeros(runs)])
    acc, n, start = np.zeros(runs), 0, int(T/dt) // 2
    for i in range(int(T/dt)):
        z = rk4(z, dt, k, g, eps, D)
        if i >= start: acc += np.abs(z[:, k])**2; n += 1
    return acc / n                     # time-averaged power in the extra mode, late half

if __name__ == "__main__":
    eps, D = 0.1, 6.0
    print(f"extra mode: coupling eps={eps}, detuning D={D}; linear off-resonant scale k*(eps/D)^2 = "
          f"{2*(eps/D)**2:.1e} (k=2), {3*(eps/D)**2:.1e} (k=3)")
    print(f"{'g':>5} | {'2 active (of 3): median  max':>30} | {'3 active (of 4): median  max':>30}")
    for g in (0.5, 2.0, 4.0, 6.0, 10.0):
        r = [extra_power(k, g, eps, D) for k in (2, 3)]
        print(f"{g:5.1f} | {np.median(r[0]):14.2e} {r[0].max():9.2e}      | "
              f"{np.median(r[1]):14.2e} {r[1].max():9.2e}", flush=True)
