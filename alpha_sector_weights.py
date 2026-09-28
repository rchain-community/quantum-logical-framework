#!/usr/bin/env python3
"""
alpha_sector_weights.py -- count the multiplicity of each census sector, and combine them.

THE QUESTION (Jim, 2026-09-28): "count the multiplicity of each sector" -- after "remember the
different ways it can happen all contribute to the value" (Alpha_Residual.md sec 9m). The measured
alpha is a multiplicity-weighted combination of the ways that close; sec 9m left the weights open.

THE SETTING. Every closure factors uniquely into prime (first-return) closures; on one axis a prime
is a + or - excursion, so a closure spells a SIGN WORD (sec 9m). A LISTENING LANGUAGE is the set of
sign words that are heard. Single primes (length-1 words) are always heard -- the irreducible floor
of the bracket -- so a language is {0, 1} plus any subset S of the composite words of length 2..k,
k the capacity. Every closure whose sign word is in the language contributes its census weight.

  sec 0  PRE-REGISTRATION -- the definition of multiplicity and the predictions, fixed before the run.
  sec 1  the per-word weights b_j, exactly, and the three named sectors rebuilt from them.
  sec 2  THE MODE IS EVERY LANGUAGE: w = 1/2 is exactly the uniform average over all languages.
  sec 3  the Sturmian (golden) class: how many languages it holds at capacity k, by brute force.
  sec 4  the two readings combined, against the predictions.
  sec 5  scope: the continuum running is the uncounted sector; the proton mass is not addressed here.

Run:  python3 alpha_sector_weights.py
"""
from __future__ import annotations

import math
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 80

PREREGISTRATION = """
PRE-REGISTRATION (fixed in the commit that adds this file, before it was run).

  DEFINITION. A sector is a class of listening languages that share a count function. Its
  MULTIPLICITY is the number of languages in the class, at capacity k. Every way contributes, so a
  set of sectors combines as  value = sum(m x tail) / sum(m).

  Two readings of "each sector" are run, and both are fixed here:
    (A) EVERY LANGUAGE is a way -- the classes partition all 2^|W_k| languages.
    (B) ONLY THE NAMED SECTORS -- irreducible (1 language), total (1), and the Sturmian class
        (every language whose composite words are exactly the factors of one Sturmian word).

  PREDICTIONS.
    P-A  Reading A gives exactly the census mode, w = 1/2, at every capacity (value -> 137.032002).
         This is not a risky prediction: sec 2 proves it (each composite word is in half of all
         languages). It is registered so that the run checks it and nothing is claimed beyond it.
    P-B  Reading B tends to the golden sector, 137.039938, as k grows, because the Sturmian class
         grows while the other two stay at one language each.
    P-C  Neither reading gives the post-hoc equal-weight mean 137.035970 of sec 9m at any capacity.
         So that mean is NOT supported by language multiplicity; if it appears, record it as a
         failed prediction.
"""


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


S62 = Decimal(62).sqrt()
C = (8 - S62) / 16                   # c(1/128): the one-sign prime series at the bare coupling
IRR = 126 - 16 * S62                 # Lean irreducibleTail_eq
TOT = 512 * S62 / 31 - 130           # Lean censusTail_eq
GOLD = 1032062 - 131072 * S62        # golden_zfa_dna.py sec 4
MEASURED = Decimal("137.035999177")  # CODATA 2022


def b(j: int) -> Decimal:
    """Census weight carried by ONE sign word of length j: 128 x sum_{n>=2} [x^n] c(x)^j / 128^n.
    For j >= 2 every order is >= 2, so b_j = 128 c^j; for j = 1 the order-1 term is removed."""
    return 128 * C - 1 if j == 1 else 128 * C ** j


def tail(counts: dict[int, int]) -> Decimal:
    """Tail of a language with counts[j] words of length j (counts[1] = 2 always)."""
    return sum(n * b(j) for j, n in counts.items())


# --------------------------------------------------------------------------- #
# sec 1 -- the per-word weights
# --------------------------------------------------------------------------- #
def sec1(K: int = 400) -> None:
    rule("sec 1  THE PER-WORD WEIGHTS, AND THE NAMED SECTORS REBUILT FROM THEM")
    irr = tail({1: 2})
    tot = tail({j: 2 ** j for j in range(1, K + 1)})
    gold = tail({j: j + 1 if j > 1 else 2 for j in range(1, K + 1)})
    for name, got, want in (("irreducible", irr, IRR), ("total", tot, TOT), ("golden", gold, GOLD)):
        assert abs(got - want) < Decimal("1e-60"), name
    print(f"""
A sign word of length j is carried by the closures whose primes, in order, have those signs; one
bare coupling per order gives it the weight b_j = 128 c^j (c = (8 - sqrt 62)/16, the one-sign prime
series at x = 1/128), with the order-1 term removed from b_1:

  b_1 = {b(1):.15f}   b_2 = {b(2):.15f}   b_3 = {b(3):.15e}   (each longer word is ~c = {C:.5f} as heavy)

Rebuilt from the b_j (to 60 digits, against the Lean / sec 9m closed forms):
  irreducible = 2 b_1                        = {irr:.12f}   ok
  total       = sum_j 2^j b_j                = {tot:.12f}   ok
  golden      = 2 b_1 + sum_(j>=2) (j+1) b_j = {gold:.12f}   ok""")


# --------------------------------------------------------------------------- #
# sec 2 -- the mode is every language
# --------------------------------------------------------------------------- #
def capacity_total(k: int) -> Decimal:
    return tail({j: 2 ** j for j in range(1, k + 1)})


def sec2() -> None:
    rule("sec 2  THE MODE IS EVERY LANGUAGE: w = 1/2 EXACTLY")
    print("""
THEOREM. At every capacity k, the average tail over all languages is the midpoint of the irreducible
and the (capacity-k) total tails -- the census mode, w = 1/2.
PROOF. A language is {0,1} plus an arbitrary subset S of the composite words W_k. Each composite word
lies in exactly half of the 2^|W_k| subsets, so it contributes b_|s| / 2 on average:
average = 2 b_1 + (1/2) sum_(s in W_k) b_|s| = (irreducible + total_k) / 2.  QED.

Checked by exhaustive enumeration where it is small enough (every language, exact):
""")
    for k in (2, 3):
        words = [(j, i) for j in range(2, k + 1) for i in range(2 ** j)]
        total = Decimal(0)
        n_lang = 2 ** len(words)
        for mask in range(n_lang):
            total += tail({1: 2}) + sum(b(words[i][0]) for i in range(len(words)) if mask >> i & 1)
        avg = total / n_lang
        mid = (tail({1: 2}) + capacity_total(k)) / 2
        assert abs(avg - mid) < Decimal("1e-60")
        print(f"  k = {k}: {n_lang:>5} languages, average tail = {avg:.15f} = midpoint  ok")
    print(f"""
So the census mode is not only "no scale is privileged" (sec 9j): it is "every listening language
contributes once". As k grows the midpoint tends to (IRR + TOT)/2, alpha^-1 = {137 + (IRR + TOT) / 2:.9f}.""")


# --------------------------------------------------------------------------- #
# sec 3 -- the Sturmian class
# --------------------------------------------------------------------------- #
def sturmian_languages(k: int, n_slopes: int = 6000, length: int = 1500) -> set:
    """Distinct sets of composite factors (lengths 2..k) over Sturmian words, sampled over slopes.
    For an irrational slope the factor set does not depend on the intercept, so slopes suffice."""
    out = set()
    shift = math.sqrt(2) - 1                              # keeps every sampled slope irrational
    for i in range(n_slopes):
        a = (i + shift) / n_slopes
        w = ''.join(str(math.floor((m + 1) * a) - math.floor(m * a)) for m in range(length))
        out.add(frozenset(w[p:p + j] for j in range(2, k + 1) for p in range(length - j)))
    return out


def farey_count(k: int) -> int:
    """Number of Farey fractions in (0,1) of order <= k, plus one: the intervals they cut."""
    return 1 + sum(sum(1 for p in range(1, q) if math.gcd(p, q) == 1) for q in range(2, k + 1))


def sec3(kmax: int = 9) -> dict[int, int]:
    rule("sec 3  THE STURMIAN (GOLDEN) CLASS: HOW MANY LANGUAGES IT HOLDS")
    print("""
The Sturmian class holds every language whose composite words are exactly the factors of one Sturmian
word -- the golden word and all its siblings at other irrational slopes, j + 1 words of each length j
(so every member has the golden tail). Counted by brute force over slopes:
""")
    print(f"  {'k':>3}{'Sturmian languages':>20}{'all languages':>22}{'share':>14}")
    m = {}
    for k in range(2, kmax + 1):
        langs = sturmian_languages(k)
        assert all(sum(1 for w in L if len(w) == j) == j + 1 for L in langs for j in range(2, k + 1))
        m[k] = len(langs)
        n_words = sum(2 ** j for j in range(2, k + 1))
        print(f"  {k:>3}{m[k]:>20}{'2^' + str(n_words):>22}{float(Fraction(m[k], 2 ** n_words)):>14.3e}")
    print(f"""
  Every sampled language has exactly j + 1 words of each length j. The Sturmian count grows like k^2
  (compare the Farey counts {[farey_count(k) for k in range(2, kmax + 1)]}); the number of all
  languages grows like 2^(2^k). The golden class is polynomial inside a doubly exponential whole.""")
    return m


# --------------------------------------------------------------------------- #
# sec 4 -- the two readings combined
# --------------------------------------------------------------------------- #
def sec4(m: dict[int, int]) -> None:
    rule("sec 4  THE TWO READINGS, COMBINED -- AGAINST THE PREDICTIONS")
    mean = (137 + (IRR + TOT) / 2 + 137 + GOLD) / 2
    print(f"""
  {'k':>3}{'(A) every language':>22}{'(B) named sectors only':>26}{'golden weight in B':>21}""")
    pa_ok = pb_ok = pc_ok = True
    last_b = None
    for k in sorted(m):
        irr_k = tail({1: 2})
        tot_k = capacity_total(k)
        gold_k = tail({j: (j + 1) if j > 1 else 2 for j in range(1, k + 1)})
        a_val = 137 + (irr_k + tot_k) / 2
        wts = {"irr": 1, "tot": 1, "st": m[k]}
        b_val = 137 + (irr_k * wts["irr"] + tot_k * wts["tot"] + gold_k * wts["st"]) / sum(wts.values())
        gw = Fraction(m[k], sum(wts.values()))
        print(f"  {k:>3}{a_val:>22.9f}{b_val:>26.9f}{float(gw):>21.4f}")
        pc_ok &= abs(a_val - mean) > Decimal("1e-4") and abs(b_val - mean) > Decimal("1e-4")
        if last_b is not None:
            pb_ok &= abs(b_val - (137 + GOLD)) <= abs(last_b - (137 + GOLD))
        last_b = b_val
    pa_ok = abs(a_val - (137 + (IRR + TOT) / 2)) < Decimal("1e-15")
    print(f"""
  mode (w = 1/2)          {137 + (IRR + TOT) / 2:.9f}      golden sector   {137 + GOLD:.9f}
  post-hoc mean (sec 9m)  {mean:.9f}      measured        {MEASURED:.9f}

  P-A  every language gives the mode:                         {'CONFIRMED' if pa_ok else 'FAILED'}
  P-B  named sectors only tend to the golden sector:          {'CONFIRMED' if pb_ok else 'FAILED'}
  P-C  neither reading gives the post-hoc mean:               {'CONFIRMED' if pc_ok else 'FAILED -- record it'}

  So language multiplicity does not produce the equal-weight mean. Counted over every language, the
  ways sit at the mode, 0.0040 below the measured value; counted over the named sectors, the growing
  Sturmian class pulls them to the golden sector, 0.0039 above. The measured value lies between the two
  readings. What decides between them -- whether nature's listening is arbitrary or grown -- is not a
  count this file can make.""")


def scope() -> None:
    rule("sec 5  SCOPE")
    print("""
  1. COUNTED. The per-word weights (exact); the theorem that every-language multiplicity is the census
     mode; the Sturmian class size at capacities 2-9 (brute force over slopes); both combinations.
  2. NOT COUNTED. The continuum vacuum-polarisation running (sec 2a) is a sector too -- every way
     contributes -- but its multiplicity is not a census count and is not attempted here.
  3. NOT ADDRESSED. The proton mass scale is outside this file.
  4. NOTHING DERIVED. No value of alpha is derived; no axiom is added.""")


def main() -> None:
    print(__doc__)
    rule("sec 0  PRE-REGISTRATION")
    print(PREREGISTRATION)
    sec1()
    sec2()
    m = sec3()
    sec4(m)
    scope()


if __name__ == "__main__":
    main()
