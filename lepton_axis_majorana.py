"""
Minimal closures on k axes: how many are their own antiparticle (Majorana)?

A minimal closure on k axes uses one twist of each sign on each axis, in any order.
Its antiparticle is the Hermitian conjugate: conjugate every twist and reverse the
order (lean/QLF_Majorana.lean).  A closure is Majorana when it equals its antiparticle.

Result: the Majorana fraction is k! 2^k / (2k)! = 1/(2k-1)!!.
  k = 1: 2 of 2 (always Majorana)      -> the one-axis neutrino nu1
  k = 2: 8 of 24 (Dirac in 2 of 3 ways)
  k = 4: 384 of 40320 (Dirac in 104 of 105 ways)
k = 1 and k = 2 are proved in Lean (one_axis_majorana, twoAxisMinimal_majorana_count).
Closed axis sets have size 1, 2 or 4 (QLF_AlphabetNecessity), so k = 3 is shown only
for comparison.  See Lepton_Generations_Fourier.md section 6.
"""
from itertools import permutations
from math import factorial

def antiparticle(h):
    return tuple((a, -s) for a, s in reversed(h))

for k in (1, 2, 3, 4):
    twists = [(a, s) for a in range(k) for s in (1, -1)]
    total = majorana = 0
    for h in permutations(twists):
        total += 1
        majorana += antiparticle(h) == h
    assert majorana * factorial(2 * k) == total * factorial(k) * 2 ** k
    print(f"k={k}: {majorana} of {total} minimal closures are Majorana "
          f"({majorana / total:.4f}); Dirac in {total - majorana}")
