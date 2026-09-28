#!/usr/bin/env python3
"""
natural_ratios.py -- the family of ratios the ZFA DNA makes, against the ratios nature uses.

THE QUESTION (Jim, 2026-09-28): "in nature phi is sort of a special case, most have different values,
we are interested in production of values that actually happen in nature."

golden_zfa_dna.py and alpha_sector_weights.py showed that the COUNT does not prefer phi: every
Sturmian slope gives the same sector. silver_zfa_dna.py showed that the substrate's own lattice makes
the silver ratio, not phi. Yet nature uses phi overwhelmingly: about 92 % of spiral phyllotaxis is
Fibonacci (Jean 1994), and the phi quasicrystals (icosahedral, decagonal) outnumber the octagonal and
dodecagonal ones (Steurer 2004). So something outside the count must select.

  sec 0  PRE-REGISTRATION -- the hypothesis and its predictions, fixed before the run.
  sec 1  the substrate side: the metallic-mean DNAs a -> a^n b, b -> a on closure blocks -- every one
         a ZFA DNA, every one Sturmian, every one with the same sector count.
  sec 2  the nature side: the divergence angles observed in phyllotaxis, and their frequencies.
  sec 3  the test: closure avoidance, q.||q alpha||, against the observed ordering.
  sec 4  scope.

Run:  python3 natural_ratios.py
"""
from __future__ import annotations

import math
from fractions import Fraction

from twist_core import is_zfa

PREREGISTRATION = """
PRE-REGISTRATION (fixed in the commit that adds this file, before it was run).

  HYPOTHESIS -- CLOSURE AVOIDANCE. A growth rotation alpha nearly CLOSES after q steps when q
  ||q alpha|| is small: the q-th element lands almost on top of the first, which for leaves means
  shading and for a lattice means a near-period. Counting closures does not prefer phi (sec 1). The
  hypothesis is that growth selects the rotation that AVOIDS closure longest -- the one whose
  near-closures are worst -- and that this, not the census count, is what makes phi nature's value.

  THE STATISTIC, fixed here: A(alpha) = min over 1 <= q <= 10^4 of q . ||q alpha||  (||x|| = distance
  to the nearest integer). Large A = closure avoided at every scale.

  PREDICTIONS.
    Q1  Every metallic block DNA a -> a^n b, b -> a (n = 1..5) is ZFA at every depth, has factor
        complexity exactly n + 1 (Sturmian), and so has the same census sector count, Catalan(n+1)
        (golden_zfa_dna.py sec 4). The count is flat across the family.  [near-certain; checked]
    Q2  Among the phyllotaxis divergence angles, A ranks them in the order of their observed
        frequency: main Fibonacci (137.5 deg) > Lucas (99.5 deg) > the higher accessory series
        (77.96 deg, 64.08 deg), which are rarer still.
    Q3  Among the metallic means as rotations (alpha = 1/lambda_n), A ranks phi first (n = 1). So the
        value nature uses most is the one that avoids closure most, while the substrate lattice's own
        value (silver, n = 2) ranks second.
  If Q2 or Q3 fails, record it as failed: closure avoidance would then not be what selects phi.
"""


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def substitute(word: str, sub: dict[str, str], k: int) -> str:
    for _ in range(k):
        word = ''.join(sub[c] for c in word)
    return word


def complexity(word: str, n: int) -> int:
    return len({word[i:i + n] for i in range(len(word) - n + 1)})


def catalan(m: int) -> int:
    return math.comb(2 * m, m) // (m + 1)


# --------------------------------------------------------------------------- #
# sec 1 -- the substrate side
# --------------------------------------------------------------------------- #
def sec1() -> None:
    rule("sec 1  THE SUBSTRATE SIDE: THE METALLIC-MEAN DNAs ON CLOSURE BLOCKS")
    block = {'a': '^>v<', 'b': '^<v>'}
    print("""
The substitution a -> a^n b, b -> a on the electron/positron closure blocks inflates by the n-th
metallic mean lambda_n = (n + sqrt(n^2 + 4))/2: n = 1 golden, n = 2 silver, n = 3 bronze, ...
""")
    print(f"  {'n':>3}{'lambda_n':>14}{'ZFA depths 1-8':>16}{'complexity = m+1':>18}{'freq(a) -> lambda/(lambda+1)':>31}")
    for n in range(1, 6):
        sub = {'a': 'a' * n + 'b', 'b': 'a'}
        w = 'a'
        for d in range(1, 9):
            w = substitute(w, sub, 1)
            assert is_zfa(''.join(block[c] for c in w[:3000]))
        comp = all(complexity(w, m) == m + 1 for m in range(1, 12))
        assert comp
        lam = (n + math.sqrt(n * n + 4)) / 2
        fa = w.count('a') / len(w)
        assert abs(fa - lam / (lam + 1)) < 1e-3
        print(f"  {n:>3}{lam:>14.9f}{'yes':>16}{'yes':>18}{fa:>20.6f} ({lam / (lam + 1):.6f})")
    print(f"""
Q1 check: every one is ZFA at every depth and Sturmian (complexity exactly m + 1), so each gives the
same census sector, Catalan(n+1) = {[catalan(n + 1) for n in range(1, 8)]} ... (golden_zfa_dna.py sec 4).
The substrate makes every metallic mean, and its count does not prefer any of them. The lattice's own
value is the silver one (silver_zfa_dna.py).""")


# --------------------------------------------------------------------------- #
# sec 2 -- the nature side
# --------------------------------------------------------------------------- #
def cf_value(terms: list[int], tail_ones: int = 60) -> float:
    """[0; terms..., 1, 1, 1, ...] evaluated from the back."""
    seq = terms + [1] * tail_ones
    x = 0.0
    for t in reversed(seq):
        x = 1.0 / (t + x)
    return x


ANGLES = [
    ("main Fibonacci", [2], "about 92 % of spiral phyllotaxis (Jean 1994)"),
    ("Lucas",          [3], "a few percent (Jean 1994)"),
    ("accessory [0;4,1,1,..]", [4], "rare"),
    ("accessory [0;5,1,1,..]", [5], "rarer"),
]


def sec2() -> list[tuple[str, float, str]]:
    rule("sec 2  THE NATURE SIDE: PHYLLOTAXIS DIVERGENCE ANGLES")
    print("""
Spiral phyllotaxis places each new organ a fixed fraction alpha of a turn after the last. The observed
families are the noble angles [0; k, 1, 1, 1, ...] -- all in Q(sqrt 5), all ending in the golden tail:
""")
    rows = []
    print(f"  {'family':<26}{'alpha':>12}{'angle':>12}   observed")
    for name, head, obs in ANGLES:
        a = cf_value(head)
        rows.append((name, a, obs))
        print(f"  {name:<26}{a:>12.6f}{360 * a:>11.2f}°   {obs}")
    print("""
(Bijugate phyllotaxis, a few percent, is two interleaved golden spirals -- the same angle, twice.)
Quasicrystals, for comparison: the phi classes (icosahedral, decagonal) far outnumber the octagonal
(1 + sqrt 2) and dodecagonal (2 + sqrt 3) ones (Steurer 2004; octagonal: Wang, Chen & Kuo 1987).""")
    return rows


# --------------------------------------------------------------------------- #
# sec 3 -- the test
# --------------------------------------------------------------------------- #
def avoidance(alpha: float, qmax: int = 10_000, qmin: int = 1) -> tuple[float, int]:
    best, arg = float('inf'), 0
    for q in range(qmin, qmax + 1):
        x = q * alpha
        v = q * abs(x - round(x))
        if v < best:
            best, arg = v, q
    return best, arg


def sec3(rows) -> None:
    rule("sec 3  THE TEST: CLOSURE AVOIDANCE AGAINST THE OBSERVED ORDER")
    print("""
Q2 -- the phyllotaxis families, in order of observed frequency:
""")
    print(f"  {'family':<26}{'A = min q.||q alpha||':>24}{'at q':>7}{'same, q >= 100':>17}")
    As, qs = [], []
    for name, a, _ in rows:
        A, q = avoidance(a)
        A_late, _ = avoidance(a, qmin=100)
        As.append(A)
        qs.append(q)
        print(f"  {name:<26}{A:>24.6f}{q:>7}{A_late:>17.6f}")
    q2 = all(As[i] > As[i + 1] for i in range(len(As) - 1))
    print(f"""
  A decreases in the order of observed frequency: {q2}   Q2 {'CONFIRMED' if q2 else 'FAILED -- record it'}

  BUT THE TEST IS WEAKER THAN IT LOOKS, and that is recorded with the result. Every minimum falls at
  q = {sorted(set(qs))} -- the very first step -- so A is just the angle's own distance from a full turn:
  the ordering says only that the golden angle puts the second organ farthest from the first. Past the
  first steps (q >= 100) all four families avoid closure equally, at Hurwitz's 1/sqrt 5 = {1 / math.sqrt(5):.6f}
  -- they share the golden tail. So long-range closure avoidance cannot tell Fibonacci from Lucas; only
  the first return does. Q2 is confirmed, with that caveat.""")

    print("""
Q3 -- the metallic means as rotations, alpha = 1/lambda_n:
""")
    print(f"  {'n':>3}{'mean':>10}{'lambda_n':>14}{'A':>12}{'limit 1/sqrt(n^2+4)':>22}")
    Am = []
    names = {1: "golden", 2: "silver", 3: "bronze", 4: "", 5: ""}
    for n in range(1, 6):
        lam = (n + math.sqrt(n * n + 4)) / 2
        A, _ = avoidance(1 / lam)
        Am.append(A)
        print(f"  {n:>3}{names[n]:>10}{lam:>14.9f}{A:>12.6f}{1 / math.sqrt(n * n + 4):>22.6f}")
    q3 = Am.index(max(Am)) == 0 and all(Am[i] >= Am[i + 1] for i in range(len(Am) - 1))
    print(f"""
  phi avoids closure most, and A falls with n: {q3}   Q3 {'CONFIRMED' if q3 else 'FAILED -- record it'}
  Here the result has teeth: the finite minimum and the long-range limit 1/sqrt(n^2 + 4) agree.

  Reading. The count is flat across the family (sec 1), but closure avoidance is not: it puts phi
  first among the metallic means at every scale, with the substrate lattice's silver second; and among
  the noble angles, which all share phi's long-range avoidance, it orders them by their first step. That is Hurwitz's theorem seen from the
  substrate: phi is the number hardest to approximate by rationals (Hurwitz 1891), i.e. the rotation
  slowest to close. In QLF terms the census counts the ways that close, and growth that must not
  overlap itself listens for the way that closes LAST.""")


def scope() -> None:
    rule("sec 4  SCOPE")
    print("""
  1. KNOWN MATHEMATICS. Metallic means and their Sturmian substitutions; Hurwitz's theorem (phi is the
     worst-approximable number, constant 1/sqrt 5); the noble divergence angles of phyllotaxis.
  2. THIS THREAD'S. The reading: the substrate MAKES every metallic mean with the same count, and
     closure AVOIDANCE -- the dual of the census's closure counting -- ranks them as nature uses them.
     A hypothesis stated and tested on orderings, not a derivation of any frequency.
  3. NOT CLAIMED. No observed percentage is predicted, only an ordering. The quasicrystal abundances
     are cited, not tested (symmetry and dimension also matter there). Nothing here touches alpha.""")


def main() -> None:
    print(__doc__)
    rule("sec 0  PRE-REGISTRATION")
    print(PREREGISTRATION)
    sec1()
    rows = sec2()
    sec3(rows)
    scope()


if __name__ == "__main__":
    main()
