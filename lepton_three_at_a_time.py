# Electron, muon, tau as d = 2, 3, 4 dimensions, viewed 3 axes at a time.
# Count N(d) of 3-axis views under several natural readings, then ask what
# the masses need.  Two mass forms, each with ONE free constant fitted to m_mu/m_e:
#   additive:       m(d) = m_e * (1 + c * N(d)/N(3))      -> needs N(4)/N(3) = 16.89
#   multiplicative: m(d) = m_e * (N(d)/N(2))^k            -> needs ln ratio 0.529
from math import comb, perm, log, factorial
me, mmu, mtau, dtau = 0.51099895, 105.6583755, 1776.86, 0.12
rmu, rtau = mmu/me, mtau/me
need_add = (rtau-1)/(rmu-1)
need_mul = log(rtau/rmu)/log(rmu)
print(f"additive target N(4)/N(3) = {need_add:.4f};  multiplicative target ln-step ratio = {need_mul:.4f}\n")
def cube_faces(d,k): return comb(d,k)*2**(d-k) if d>=k else 0
counts = {
 "3-subsets C(d,3)":                     lambda d: comb(d,3),
 "ordered 3-frames P(d,3)":              lambda d: perm(d,3),
 "signed oriented frames 8*P(d,3)":      lambda d: 8*perm(d,3),
 "3-faces of the d-cube":                lambda d: cube_faces(d,3),
 "views incl. lower: sum_{k<=3} C(d,k)": lambda d: sum(comb(d,k) for k in range(4)),
 "signed views sum_{k<=3} C(d,k)2^k":    lambda d: sum(comb(d,k)*2**k for k in range(4)),
 "rotation planes C(d,2)":               lambda d: comb(d,2),
 "hyperoctahedral order 2^d d!":         lambda d: 2**d*factorial(d),
 "twist alphabet 2d":                    lambda d: 2*d,
 "3-views x signs 2^d C(d,3)":           lambda d: 2**d*comb(d,3),
}
print(f"{'N(d) reading':38s} {'N2,N3,N4':>14s} {'add: m_tau':>11s} {'off':>8s} {'mul: m_tau':>11s} {'off':>8s}")
for name,f in counts.items():
    n2,n3,n4 = f(2),f(3),f(4)
    add = me*(1+(rmu-1)*n4/n3)
    if n2>0:
        k = log(rmu)/log(n3/n2); mul = me*(n4/n2)**k
        ms = f"{mul:11.0f} {100*(mul-mtau)/mtau:+7.1f}%"
    else: ms = f"{'n/a (N2=0)':>11s} {'':>8s}"
    print(f"{name:38s} {str((n2,n3,n4)):>14s} {add:11.0f} {100*(add-mtau)/mtau:+7.1f}% {ms}")
print(f"\nBarut increments sum k^4: 0,1,17 -> ratio 17 ({100*(17/need_add-1):+.2f}% from target)")
print(f"Koide benchmark m_tau = 1776.97 MeV (+0.006%)")
