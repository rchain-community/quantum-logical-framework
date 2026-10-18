# Same test as lepton_three_at_a_time.py, with a time axis added: electron, muon, tau = d = 4, 5, 6.
# Mass forms (one constant fitted to m_mu/m_e, then predict m_tau):
#   additive:       m = m_e * (1 + c*(N(d)-N(4)))   needs (N6-N4)/(N5-N4) = 16.89
#   multiplicative: m = m_e * (N(d)/N(4))^k         needs ln(N6/N5)/ln(N5/N4) = 0.529
from math import comb, perm, log, factorial
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
rmu, rtau = mmu/me, mtau/me
print(f"targets: additive {(rtau-1)/(rmu-1):.3f}   multiplicative {log(rtau/rmu)/log(rmu):.3f}\n")
counts = {
 "3-subsets C(d,3)":                    lambda d: comb(d,3),
 "3-views containing time C(d-1,2)":    lambda d: comb(d-1,2),
 "3-views, space only C(d-1,3)":        lambda d: comb(d-1,3),
 "ordered 3-frames P(d,3)":             lambda d: perm(d,3),
 "3-faces of the d-cube":               lambda d: comb(d,3)*2**(d-3),
 "rotation/boost planes C(d,2)":        lambda d: comb(d,2),
 "hyperoctahedral 2^d d!":              lambda d: 2**d*factorial(d),
 "signed views sum_{k<=3} C(d,k)2^k":   lambda d: sum(comb(d,k)*2**k for k in range(4)),
 "4-subsets (3 space + time) C(d,4)":   lambda d: comb(d,4),
 "2^d (bits per axis)":                 lambda d: 2**d,
 "4^d (twists per axis)":               lambda d: 4**d,
}
print(f"{'N(d) reading':36s} {'N4,N5,N6':>16s} {'add':>8s} {'mul':>8s}   (tau off, add / mul)")
for name,f in counts.items():
    n4,n5,n6 = f(4),f(5),f(6)
    add = me*(1+(rmu-1)*(n6-n4)/(n5-n4))
    out = f"{name:36s} {str((n4,n5,n6)):>16s} {(n6-n4)/(n5-n4):8.3f} "
    if n4>0:
        mul = me*rmu**(log(n6/n4)/log(n5/n4)); out += f"{log(n6/n5)/log(n5/n4):8.3f}   {100*(add-mtau)/mtau:+6.0f}% / {100*(mul-mtau)/mtau:+6.0f}%"
    print(out)
