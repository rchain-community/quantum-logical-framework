# Inverse-Fourier reading: treat the three sqrt-masses as a signal on Z3 (k = e, mu, tau)
# and look at its discrete Fourier modes.
import cmath, math
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
s = [math.sqrt(me), math.sqrt(mmu), math.sqrt(mtau)]
w = cmath.exp(2j*math.pi/3)
a = [sum(s[k]*w**(-n*k) for k in range(3))/3 for n in range(3)]   # a0 real, a2 = conj(a1)
dc = 3*abs(a[0])**2; ac = 3*(abs(a[1])**2+abs(a[2])**2)
print(f"DC power {dc:.4f}  AC power {ac:.4f}  AC/DC = {ac/dc:.6f}   (Koide Q=2/3 <=> AC/DC = 1)")
print(f"harmonic amplitude 2|a1|/a0 = {2*abs(a[1])/a[0].real:.6f}  (sqrt2 = {math.sqrt(2):.6f})")
ph = cmath.phase(a[1]) % (2*math.pi/3)
print(f"harmonic phase mod 2pi/3 = {ph:.7f}; candidates 2/9 = {2/9:.7f}, 2pi/3-2/9 = {2*math.pi/3-2/9:.7f}")
# reconstruct: inverse DFT is exactly the Koide form
print("inverse DFT reproduces sqrt-masses:", [round((a[0]+a[1]*w**k+a[2]*w**(2*k)).real,6) for k in range(3)], [round(x,6) for x in s])
# Can integer Fourier data give the phase?  arg of an Eisenstein integer p + q*w, smallest |p|+|q| within tol
delta, tol = 2/9, 1e-5
best = None
for p in range(-2000, 2001):
    for q in range(0, 2001):
        if p == 0 and q == 0: continue
        z = p + q*w
        d = (cmath.phase(z) - delta) % (2*math.pi/3)
        d = min(d, 2*math.pi/3 - d)
        if d < tol:
            n = abs(p)+abs(q)
            if best is None or n < best[0]: best = (n, p, q, d)
    if best and abs(p) > best[0]: break
n,p,q,d = best
print(f"smallest Eisenstein integer with phase = delta (mod 2pi/3) to 1e-5: {p} + {q}w  (|p|+|q| = {n}, cost ~{2*math.log2(n):.0f} bits vs ~3 bits for 2/3)")
