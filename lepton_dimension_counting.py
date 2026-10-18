# Test: electron, muon, tau as d = 2, 3, 4 "dimensions of possibility".
# Each family has ONE free parameter, fitted to m_mu/m_e; it then predicts m_tau/m_e.
import math
from math import comb, lgamma, log, exp, pi
me, mmu, mtau, dtau = 0.51099895, 105.6583755, 1776.86, 0.12
r_mu, r_tau = mmu/me, mtau/me
print(f"measured: m_mu/m_e={r_mu:.3f}  m_tau/m_e={r_tau:.1f}  m_tau/m_mu={mtau/mmu:.3f}")
print(f"log steps: ln(mu/e)={log(r_mu):.3f}  ln(tau/mu)={log(mtau/mmu):.3f}  ratio={log(mtau/mmu)/log(r_mu):.3f}")
def closed_walks(d, n):  # closed walks of length 2n on Z^d (exact, via multinomial DP over axes)
    # number = sum over (n1..nd) sum=n of (2n)!/prod(ni!^2)
    from functools import lru_cache
    @lru_cache(None)
    def f(k, m):  # ways to distribute m pairs over k axes, weighted 1/(ni!)^2
        if k == 0: return 1 if m == 0 else 0
        return sum(f(k-1, m-i) / math.factorial(i)**2 for i in range(m+1))
    return math.factorial(2*n) * f(d, n)
def fit(fn, lo, hi):  # solve fn(3,p)/fn(2,p) = r_mu by bisection on log
    g = lambda p: log(fn(3, p)) - log(fn(2, p)) - log(r_mu)
    a, b = lo, hi
    for _ in range(200):
        m = (a+b)/2
        if g(a)*g(m) <= 0: b = m
        else: a = m
    return (a+b)/2
fams = {
 "d^k (power of dimension)":        (lambda d,k: d**k, 0.1, 100),
 "(2d)^L (open walks, L steps)":    (lambda d,L: (2*d)**L, 0.1, 100),
 "d!^k":                            (lambda d,k: math.factorial(d)**k, 0.1, 100),
 "unit-sphere surface S_{d-1}*R^(d-1)": (lambda d,R: 2*pi**(d/2)/math.gamma(d/2)*R**(d-1), 1.0001, 1e6),
 "ball volume V_d(R)":              (lambda d,R: pi**(d/2)/math.gamma(d/2+1)*R**d, 1.0001, 1e6),
 "exp(k d^2)":                      (lambda d,k: exp(k*d*d), 0.01, 10),
 "Barut-like 1+c*sum_{j<d-1} (j+1)^4": (lambda d,c: 1+c*sum((j+1)**4 for j in range(d-2)), 0.001, 1e4),
}
print(f"\n{'family':40s} {'param':>10s} {'pred tau/e':>11s} {'pred m_tau':>11s} {'off':>8s}")
for name,(fn,lo,hi) in fams.items():
    p = fit(fn, lo, hi); pred = fn(4,p)/fn(2,p)
    print(f"{name:40s} {p:10.4f} {pred:11.1f} {pred*me:11.1f} {100*(pred*me-mtau)/mtau:+7.1f}%")
# closed walks with integer n
print("\nclosed walks C_d(2n) on Z^d (integer n, no fit):")
best=None
for n in range(1,40):
    c2,c3,c4 = (closed_walks(d,n) for d in (2,3,4))
    if best is None or abs(log(c3/c2/r_mu))<abs(log(best[1]/r_mu)): best=(n,c3/c2,c4/c2)
n,a,b = best; print(f"  best n={n}: C3/C2={a:.1f} (need {r_mu:.1f})  C4/C2={b:.0f} -> m_tau={b*me:.0f} MeV ({100*(b*me-mtau)/mtau:+.0f}%)")
# Koide benchmark: same inputs (m_e, m_mu), zero new parameters
a=math.sqrt(me)+math.sqrt(mmu); b=me+mmu; st=2*a+math.sqrt(6*a*a-3*b)
print(f"\nKoide Q=2/3 benchmark: m_tau={st**2:.2f} MeV ({100*(st**2-mtau)/mtau:+.4f}%, {(st**2-mtau)/dtau:+.1f} sigma)")
# Barut (1979), zero free parameters: m = m_e (1 + 3/(2 alpha) * sum_{k<=N} k^4), N = d - 2
alpha = 1/137.035999
for N,(lab,meas) in zip((1,2),(("mu",mmu),("tau",mtau))):
    m = me*(1+1.5/alpha*sum(k**4 for k in range(N+1)))
    print(f"Barut N={N} ({lab}): {m:.2f} MeV vs {meas} ({100*(m-meas)/meas:+.2f}%)")
