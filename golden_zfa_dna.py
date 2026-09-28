#!/usr/bin/env python3
"""
golden_zfa_dna.py -- the golden thread: phi and the Fibonacci numbers in the ZFA DNA.

THE QUESTION (Jim, 2026-09-28): "i am wondering about the utility of zfa dna with the golden
ratio and fibonacci numbers?" Three places it could live, each checked here rather than asserted:

  sec 1  THE GOLDEN ZFA DNA. The Fibonacci substitution e -> ep, p -> e, run on closure blocks
         (e = the electron closure ^>v<, p = the positron closure ^<v>). It closes at every depth,
         its lengths are Fibonacci numbers, the electron chirality has frequency phi - 1, and its
         block word has complexity n + 1 -- Sturmian: zero entropy, yet it never repeats. The
         simplest non-repeating closure genome, the quasicrystal slot in chaos_emergence.py's
         spectrum.
  sec 2  THE GOLDEN PATH IN THE MANDELBROT SET. Along the Farey path to internal angle 2 - phi,
         the main-cardioid limbs have periods 2, 3, 5, 8, 13, 21 (Devaney 1999). Their root leaves,
         built from words alone and checked against mandelbrot_lamination.py's leaves, have binary
         words that are prefixes of the Fibonacci word -- so the same substitution, 0 -> 01, 1 -> 0,
         generates the external angle of M's golden-mean point, 0.(Fibonacci word)_2.
  sec 3  THE GOLDEN ALPHA WAY -- PRE-REGISTERED. Is there a phi-scale (log-periodic, ratio phi)
         line in the census that could move the residual weight off the mode w = 1/2
         (Alpha_Residual.md sec 9j)? Predictions are fixed below before the probe is run.
  sec 4  THE GOLDEN CENSUS SECTOR, COUNTED. Every closure factors uniquely into prime (first-
         return) closures; on one axis each prime is a + or - excursion, so a closure spells a sign
         word. The golden sector keeps the closures whose sign word is a factor of the Fibonacci
         word -- what golden growth produces locally. Its count at order n is exactly Catalan(n+1),
         and its alpha tail has a closed form.
  sec 5  scope.

Exact arithmetic throughout (int, Fraction); floats only for display and for the sec 3 regression.

Run:  python3 golden_zfa_dna.py            (seconds)
      python3 golden_zfa_dna.py --deep     (also checks the period-13 limb against the lamination, ~2 min)

Companions: ZFA_DNA.md sec 11 (the write-up), primordial_zfa_dna.py (the 1/3-bit DNA),
chaos_emergence.py (the entropy spectrum), mandelbrot_lamination.py (the leaves),
Alpha_Residual.md sec 9j-9l (the alpha weight), genesis.py sec 5c (the ratio-2 probe).
"""
from __future__ import annotations

import io
import itertools
import math
import sys
from contextlib import redirect_stdout
from decimal import Decimal, getcontext
from fractions import Fraction

from qucalc_search import max_excursion
from twist_core import is_zfa

BLOCK = {'e': '^>v<', 'p': '^<v>'}          # electron / positron closures (ZFA_DNA.md sec 1)
GOLDEN = {'e': 'ep', 'p': 'e'}              # the Fibonacci substitution
PHI = (1 + math.sqrt(5)) / 2


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def substitute(word: str, sub: dict[str, str], k: int) -> str:
    for _ in range(k):
        word = ''.join(sub[c] for c in word)
    return word


def complexity(word: str, n: int) -> int:
    """Number of distinct factors (subwords) of length n."""
    return len({word[i:i + n] for i in range(len(word) - n + 1)})


def desubstitute(word: str) -> str:
    """Invert e -> ep, p -> e: read 'ep' as e and a lone 'e' as p."""
    out, i = [], 0
    while i < len(word):
        if word[i:i + 2] == 'ep':
            out.append('e'); i += 2
        else:
            assert word[i] == 'e', "not in the image of the substitution"
            out.append('p'); i += 1
    return ''.join(out)


# --------------------------------------------------------------------------- #
# sec 1 -- the golden ZFA DNA
# --------------------------------------------------------------------------- #
def sec1() -> str:
    rule("sec 1  THE GOLDEN ZFA DNA: e -> ep, p -> e, ON CLOSURE BLOCKS")
    print("""
Seed e (the electron closure ^>v<). Each generation replaces e by ep and p by e. Every block is a
closure, so every generation is a concatenation of closures. Checked at each depth:
""")
    print(f"  {'k':>3}{'blocks':>8}{'twists':>8}{'ZFA':>6}{'max exc':>9}{'freq(e)':>16}{'= F/F':>12}{'desub':>7}")
    print("  " + "-" * 69)
    w = 'e'
    for k in range(1, 16):
        parent, w = w, substitute(w, GOLDEN, 1)
        h = ''.join(BLOCK[c] for c in w)
        ne = w.count('e')
        assert len(w) == fib(k + 2) and ne == fib(k + 1)
        assert is_zfa(h) and desubstitute(w) == parent
        f = Fraction(ne, len(w))
        print(f"  {k:>3}{len(w):>8}{len(h):>8}{'yes':>6}{max_excursion(h):>9}"
              f"{float(f):>16.12f}{str(f):>12}{'ok':>7}")
    print(f"\n  phi - 1 = {PHI - 1:.12f}   (the frequency converges to it through ratios of Fibonacci numbers)")

    tm = substitute('e', {'e': 'ep', 'p': 'pe'}, 12)             # Thue-Morse on the same blocks
    per = 'e' * len(w)
    print("""
Factor complexity p(n) -- how many distinct block-words of length n occur. Periodic: bounded.
Sturmian: exactly n + 1, the least any non-repeating word can have (Morse & Hedlund 1940).
Positive entropy: exponential.
""")
    print(f"  {'n':>3}{'periodic (all e)':>18}{'golden (Fibonacci)':>20}{'Thue-Morse':>12}")
    for n in range(1, 11):
        pg = complexity(w, n)
        assert pg == n + 1, "golden DNA is not Sturmian"
        print(f"  {n:>3}{complexity(per, n):>18}{pg:>20}{complexity(tm, n):>12}")
    print("""
So the golden DNA sits in chaos_emergence.py's spectrum at h = 0 -- no free bit, fully determined --
yet it is aperiodic: order that never repeats, the one-dimensional quasicrystal. Next to it:
the periodic genome (h = 0, repeats), Thue-Morse (h = 0, aperiodic, more factors), and the
primordial DNA (h = 1/3, one free chirality per closure). Matter and antimatter closures appear
in the ratio phi : 1, and every scale is the previous one with the ratio preserved.""")
    return w


# --------------------------------------------------------------------------- #
# sec 2 -- the golden path in the Mandelbrot set
# --------------------------------------------------------------------------- #
def christoffel_rotations(p: int, q: int) -> list[str]:
    """The q cyclic rotations of the lower Christoffel word of slope p/q (p ones, q - p zeros).
    Their binary values k/(2^q - 1) are the candidate p/q rotation orbit of doubling."""
    c = ''.join(str((i + 1) * p // q - i * p // q) for i in range(q))
    return sorted({c[i:] + c[:i] for i in range(q)})


def rotation_orbit(p: int, q: int) -> list[Fraction]:
    """The p/q rotation orbit of the doubling map, exactly: q angles on which doubling acts as
    rotation by p/q in cyclic order (Bullett & Sentenac 1994; Goldberg 1992)."""
    d = 2 ** q - 1
    orb = sorted(Fraction(int(s, 2), d) for s in christoffel_rotations(p, q))
    assert len(orb) == q
    for x in orb:                                             # the rotation property, checked
        assert orb[(orb.index(x) + p) % q] == (2 * x) % 1, f"{p}/{q}: not a rotation orbit"
    return orb


def root_leaf(p: int, q: int) -> tuple[Fraction, Fraction]:
    """The p/q limb's root leaf: the two orbit angles bounding the characteristic (shortest)
    arc, of length exactly 1/(2^q - 1)."""
    orb = rotation_orbit(p, q)
    gap = Fraction(1, 2 ** q - 1)
    pairs = [(orb[i], orb[i + 1]) for i in range(q - 1) if orb[i + 1] - orb[i] == gap]
    assert len(pairs) == 1, f"{p}/{q}: characteristic arc not unique"
    return pairs[0]


def lamination_leaves(n_max: int) -> set:
    import mandelbrot_lamination as ml
    with redirect_stdout(io.StringIO()):
        leaves, _ = ml.refine_gaps(n_max)
    return {tuple(sorted(l)) for l in leaves}


def sec2(deep: bool) -> None:
    rule("sec 2  THE GOLDEN PATH: FIBONACCI LIMBS, AND THE FIBONACCI WORD AS AN EXTERNAL ANGLE")
    fw = substitute('0', {'0': '01', '1': '0'}, 20)          # the Fibonacci word 0100101001001...
    theta = Fraction(int(fw[:64], 2), 2 ** 64)               # 0.(Fibonacci word)_2 to 64 bits
    print(f"""
The Farey path to internal angle 2 - phi = {2 - PHI:.12f} runs through the main-cardioid limbs
1/2, 1/3, 2/5, 3/8, 5/13, 8/21 -- ratios of Fibonacci numbers, with Fibonacci periods (Devaney 1999).
For each, the root leaf is built from words alone: the p/q rotation orbit of doubling (rotations of
the Christoffel word), and the pair of orbit angles on its characteristic arc of length 1/(2^q - 1).
""")
    check_to = 13 if deep else 8
    leaves = lamination_leaves(check_to)
    print(f"  {'p/q':>6}  {'root leaf':<36}{'binary words':<46}{'in lamination':>14}")
    print("  " + "-" * 104)
    prev = None
    for k in range(3, 9):
        p, q = fib(k - 2), fib(k)
        a, b = root_leaf(p, q)
        wa, wb = format(a.numerator, f'0{q}b'), format(b.numerator, f'0{q}b')
        assert fw[:q] in (wa, wb), f"{p}/{q}: no endpoint is a Fibonacci-word prefix"
        mark = 'yes' if q <= check_to and (a, b) in leaves else ('--' if q > check_to else 'NO')
        assert mark != 'NO', f"{p}/{q}: root leaf is not a lamination leaf"
        print(f"  {f'{p}/{q}':>6}  {f'({a}, {b})':<36}{wa + '  ' + wb:<46}{mark:>14}")
        prev = (a, b)
    print(f"""
  Every root leaf has one endpoint whose word is the Fibonacci word's prefix of that length, and
  every leaf checked (periods <= {check_to}) is a leaf of the lamination. The leaves close in on

      theta* = 0.(Fibonacci word)_2 = 0.{fw[:48]}...
             = {float(theta):.15f}     (period-21 leaf: {float(prev[0]):.15f} .. {float(prev[1]):.15f})

  So the Fibonacci substitution 0 -> 01, 1 -> 0 -- a replication rule of the same kind as the ZFA
  DNA -- writes the external angle of the golden-mean point of M one digit at a time, and each
  Fibonacci-length prefix is a limb's root. The doubling map that reads it is the loop DNA's
  word-copy law (mandelbrot_loop_dna.py). The identification of theta* with the golden-mean
  Siegel parameter, and its transcendence, are Bullett & Sentenac's (1994); here the finite
  leaves are generated and checked, not the limit.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the golden alpha way, pre-registered
# --------------------------------------------------------------------------- #
PREREGISTRATION = """
PRE-REGISTRATION (fixed in the commit that adds this file, before the probe below was run).

  P1  NO CENSUS SECTOR CARRIES A PHI-SCALE LINE. For the genesis.py sectors (p = 1..4 conjugate pairs,
      counts C(2n,n) and the multipair census), fit the Stirling-detrended log2-count residual r(n)
      with a smooth model a + b/n + c/n^2, then add a log-periodic term of period log(phi) in log n.
      A LINE requires the periodic term to cut the residual sum of squares by more than 50 % AND to
      keep its amplitude to within a factor 2 on both halves of the n-range. The same test at
      period log(2) is the control. PREDICTION: no line at phi, no line at 2. Reason, stated first:
      these counts are products of binomials, whose Stirling expansions are power series in 1/n --
      there is no term for a log-periodic line to come from. Only a substitution-generated sector
      has discrete scale invariance.

  P2  THE GOLDEN DNA AS A COUNTING RULE. Read the golden DNA's block word order by order -- order n
      of the census (n >= 2) is counted in full (e) or irreducibly (p) as the (n-1)-th letter of
      the Fibonacci word says -- and sum the census tail. PREDICTION: it does NOT land within the
      theory's precision 0.001 of the measured value. Reason: the order-2 term alone differs by
      0.03 between the two countings, and the first letter is e, so the value sits near the
      total-census end, 137.047.

  Recorded, not predicted (computed while exploring): the golden WEIGHT w = phi - 1 in the linear
  mix (1 - w).irreducible + w.total gives 137.035809 -- one of the 189 fits of Alpha_Residual.md
  sec 9k, and one way the residual closes. Its multiplicity is not counted here.
"""


def census_tail_per_order(letters: str, terms: int = 200) -> Fraction:
    """128 x sum_{n>=2} count_n / 128^n, with order n counted by letter n-2 of `letters`:
    e -> every closure C(2n,n), p -> irreducible 2.Catalan(n-1)."""
    s = Fraction(0)
    for n in range(2, terms + 1):
        c = math.comb(2 * n, n) if letters[n - 2] == 'e' else 2 * math.comb(2 * n - 2, n - 1) // n
        s += Fraction(c, 128 ** n)
    return 128 * s


def log_periodic_probe(p: int, n_max: int, period: float) -> tuple[float, float]:
    """Return (fractional RSS reduction from adding a log-periodic term, amplitude ratio between
    the two halves of the n-range). Least squares by normal equations, small and exact enough."""
    from genesis import multipair_census
    ns = list(range(4, n_max + 1))
    r = []
    for n in ns:
        realized = math.comb(2 * n, n) if p == 1 else multipair_census(p, n)[1]
        smooth = 2 * n * math.log2(2 * p) - (p / 2) * math.log2(math.pi * n)
        r.append(math.log2(realized) - smooth)

    def fit(xs, ys, cols):
        m = len(cols)
        X = [[f(x) for f in cols] for x in xs]
        A = [[sum(X[i][a] * X[i][b] for i in range(len(xs))) for b in range(m)] for a in range(m)]
        y = [sum(X[i][a] * ys[i] for i in range(len(xs))) for a in range(m)]
        for c in range(m):                                   # Gauss-Jordan
            piv = max(range(c, m), key=lambda k: abs(A[k][c]))
            A[c], A[piv], y[c], y[piv] = A[piv], A[c], y[piv], y[c]
            for k in range(m):
                if k != c and A[c][c]:
                    f = A[k][c] / A[c][c]
                    A[k] = [A[k][j] - f * A[c][j] for j in range(m)]
                    y[k] -= f * y[c]
        beta = [y[c] / A[c][c] for c in range(m)]
        rss = sum((ys[i] - sum(beta[j] * X[i][j] for j in range(m))) ** 2 for i in range(len(xs)))
        return beta, rss

    w = 2 * math.pi / period
    smooth_cols = [lambda n: 1.0, lambda n: 1.0 / n, lambda n: 1.0 / n ** 2]
    lp_cols = smooth_cols + [lambda n: math.cos(w * math.log(n)), lambda n: math.sin(w * math.log(n))]
    _, rss0 = fit(ns, r, smooth_cols)
    _, rss1 = fit(ns, r, lp_cols)
    half = len(ns) // 2
    amps = []
    for lo, hi in ((0, half), (half, len(ns))):
        b, _ = fit(ns[lo:hi], r[lo:hi], lp_cols)
        amps.append(math.hypot(b[3], b[4]))
    reduction = 1 - rss1 / rss0 if rss0 else 0.0
    amp_ratio = max(amps) / min(amps) if min(amps) else float('inf')
    return reduction, amp_ratio


def sec3(golden_word: str) -> None:
    rule("sec 3  THE GOLDEN ALPHA WAY -- PRE-REGISTERED")
    print(PREREGISTRATION)
    print("  P1  the probe, run:\n")
    print(f"  {'sector':>8}{'n range':>10}{'period':>9}{'RSS cut':>10}{'amp ratio':>11}{'line?':>7}")
    lines = 0
    for p, n_max in ((1, 120), (2, 80), (3, 60), (4, 45)):
        for label, period in (("log phi", math.log(PHI)), ("log 2", math.log(2))):
            cut, ratio = log_periodic_probe(p, n_max, period)
            line = cut > 0.5 and ratio < 2
            lines += line
            print(f"  {p:>8}{f'4..{n_max}':>10}{label:>9}{cut:>10.3f}{ratio:>11.2f}{'YES' if line else 'no':>7}")
    print(f"\n  P1 outcome: {lines} line(s) found. Predicted: none. "
          f"{'CONFIRMED.' if lines == 0 else 'PREDICTION FAILED -- record it.'}")

    measured = Fraction(137035999177, 10 ** 9)                # CODATA 2022
    v = 137 + census_tail_per_order(golden_word)
    off = float(v - measured)
    print(f"""
  P2  the golden DNA as a per-order counting rule, run:
      first letters {golden_word[:12]}...  ->  alpha^-1 = {float(v):.9f}   (off {off:+.2e})
  P2 outcome: {'lands within 0.001' if abs(off) < 1e-3 else 'does not land within 0.001'}. Predicted: does not land. {'CONFIRMED.' if abs(off) >= 1e-3 else 'PREDICTION FAILED -- record it.'}""")

    s62 = math.sqrt(62)
    irr, tot = 126 - 16 * s62, 512 * s62 / 31 - 130
    wm = (float(measured) - 137 - irr) / (tot - irr)
    print(f"""
  The golden weight, as one way: w = phi - 1 = {PHI - 1:.9f} -> alpha^-1 = {137 + (2 - PHI) * irr + (PHI - 1) * tot:.9f}.
  The convergents of phi - 1 are 1/2, 2/3, 3/5, 5/8, 8/13, 13/21, ... -- and the census mode w = 1/2
  is the first of them. The measured w = {wm:.6f} lies between 8/13 and 5/8 but outside (8/13, 13/21):
  it follows the golden sequence as far as 5/8 and then leaves it. A way, found in finite time;
  how many ways reach it is not counted here.""")


# --------------------------------------------------------------------------- #
# sec 4 -- scope
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# sec 4 -- the golden census sector, counted
# --------------------------------------------------------------------------- #
def catalan(m: int) -> int:
    return math.comb(2 * m, m) // (m + 1)


def prime_sign_word(steps: list[int]) -> str:
    """Factor a closed +-1 walk into its prime (first-return) closures and read each prime's
    sign: '0' for a + excursion, '1' for a - excursion."""
    out, h, start = [], 0, 0
    for i, x in enumerate(steps):
        h += x
        if h == 0:
            out.append('0' if steps[start] > 0 else '1')
            start = i + 1
    return ''.join(out)


def sec4() -> None:
    rule("sec 4  THE GOLDEN CENSUS SECTOR, COUNTED")
    print("""
WHY THIS SECTOR. The golden pattern recurs in nature -- phyllotaxis, shells, branching -- wherever
growth places each new element by the same local rule (Jim, 2026-09-28: "this is justified by the
recurrence of the pattern in nature"). That recurrence is the reason to count the sector; it is a
reason to look, not a derivation.

THE DEFINITION, fixed before the sum was computed. The census already factors every closure into
prime (first-return) closures: IRREDUCIBLE counts one prime, TOTAL counts any sequence of primes
(G = 1/(1 - I)). On one axis a prime is a + or a - excursion (Catalan(n-1) of each), so every
closure spells a sign word. The GOLDEN sector keeps the closures whose sign word is a factor of the
Fibonacci word -- a word the golden substitution produces somewhere. It sits between the two ends:
irreducible allows words of length 1, total allows all 2^k words, golden allows the k + 1 golden
words of length k (sec 1: the language is Sturmian).

Brute force (every closed walk of length 2n, factored and filtered) against the closed form:
""")
    fw = substitute('0', {'0': '01', '1': '0'}, 25)
    facs: dict[int, set] = {}
    print(f"  {'n':>3}{'total C(2n,n)':>15}{'irreducible':>13}{'golden':>9}{'Catalan(n+1)':>14}")
    print("  " + "-" * 54)
    for n in range(1, 10):
        tot = irr = gold = 0
        for ups in itertools.combinations(range(2 * n), n):
            st = [-1] * (2 * n)
            for i in ups:
                st[i] = 1
            wd = prime_sign_word(st)
            k = len(wd)
            if k not in facs:
                facs[k] = {fw[i:i + k] for i in range(len(fw) - k + 1)}
            tot += 1
            irr += k == 1
            gold += wd in facs[k]
        assert tot == math.comb(2 * n, n) and irr == 2 * catalan(n - 1) and gold == catalan(n + 1)
        print(f"  {n:>3}{tot:>15}{irr:>13}{gold:>9}{catalan(n + 1):>14}")

    getcontext().prec = 70                                     # the closed form cancels ~7 digits
    s62 = Decimal(62).sqrt()
    irr_t, tot_t = 126 - 16 * s62, 512 * s62 / 31 - 130
    gold_t = 1032062 - 131072 * s62
    series = 128 * sum(Decimal(catalan(n + 1)) / Decimal(128) ** n for n in range(2, 300))
    assert abs(series - gold_t) < Decimal("1e-45")
    measured = Decimal("137.035999177")                        # CODATA 2022
    a_gold = 137 + gold_t
    w_gold = (gold_t - irr_t) / (tot_t - irr_t)
    a_mode = 137 + irr_t + (tot_t - irr_t) / 2
    mid = (a_mode + a_gold) / 2
    print(f"""
WHY CATALAN(n+1), exactly. With c(x) = sum Catalan(n-1) x^n the prime series of one sign, the
golden sector's series is sum_k (k + 1) c^k = 1/(1 - c)^2 - 1. The Catalan series C satisfies
C = 1 + x C^2, so 1 - c = 1 - xC = 1/C, and 1/(1 - c)^2 = C^2 = (C - 1)/x = sum Catalan(n+1) x^n.
The count depends only on there being k + 1 golden words of length k -- so EVERY Sturmian language,
at any irrational slope, gives the same sector. Counting does not single out phi; the golden word
is the simplest member of the family, and nature's choice of it is the reason given above.

THE ALPHA TAIL, closed form (one bare coupling 1/128 per order, orders 0 and 1 subtracted as before):

  golden tail   = 128 x sum_(n>=2) Catalan(n+1)/128^n = 1032062 - 131072.sqrt(62)
                = 8192 x (irreducible tail) - 130
                = {gold_t:.15f}     (series agrees to 45 digits)

  alpha^-1 (golden sector) = 1032199 - 131072.sqrt(62) = {a_gold:.12f}
  measured (CODATA 2022)                               = {measured:.12f}
  difference                                           = {a_gold - measured:+.3e}
  effective weight w_golden                            = {w_gold:.12f}

  So the golden sector lands 0.0039 ABOVE the measured value, as far above as the census mode
  w = 1/2 ({a_mode:.9f}) lands below it. It is a way the residual closes, counted exactly; it is
  not the measured value.

  EVERY WAY CONTRIBUTES. The measured value is not one way picked out of many: every way that
  closes contributes, as the census tail is already a sum over every closure. So sectors combine,
  weighted by their multiplicities; the mode is where multiplicity peaks (what happens first), not
  the whole of what is measured. What is uncounted is the weights.

  NOTICED AFTER THE FACT, recorded as that: the plain mean of the mode and the golden sector is
  {mid:.12f}, off by {mid - measured:+.2e} -- the combination in which the two sectors carry
  equal multiplicity. Whether they do is the count still to be made; the observation came after
  both values were in hand, so it is a lead, not a result.""")


def scope() -> None:
    rule("sec 5  SCOPE")
    print("""
  1. KNOWN MATHEMATICS, USED AND CITED. Sturmian words and their n + 1 complexity (Morse & Hedlund
     1940); the Fibonacci limbs on the Farey path to the golden mean (Devaney 1999); rotation orbits
     of doubling and the golden-mean angle (Bullett & Sentenac 1994). None of that is new here.

  2. THIS THREAD'S. The closure-block genome (sec 1): a ZFA DNA with zero entropy that never
     repeats, electron : positron = phi : 1 at every scale. And the reading (sec 2): the Fibonacci
     substitution is a replication rule of the DNA's kind, and it writes the golden-mean angle of M
     that the doubling map -- the loop DNA's word-copy law -- reads. The leaves are generated and
     checked; the limit point is cited, not re-proved.

  3. ALPHA. Nothing is derived. Sec 3 records the pre-registered outcomes and the golden weight as
     one way among the 189 of Alpha_Residual.md sec 9k, uncounted. Sec 4 counts the golden census
     sector exactly (Catalan(n+1), a closed-form tail): it lands 0.0039 above the measured value.
     The count is the same for every Sturmian language, so it does not select phi.""")


def main() -> None:
    deep = "--deep" in sys.argv
    print(__doc__)
    w = sec1()
    sec2(deep)
    sec3(w)
    sec4()
    scope()


if __name__ == "__main__":
    main()
