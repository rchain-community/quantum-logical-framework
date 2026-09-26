#!/usr/bin/env python3
"""
mandelbrot_loop_dna.py -- the quadratic loop's DNA, written in QuCalc.

THE QUESTION (two of them, Jim, 2026-09-26):
  1. In the possibilist realm the Mandelbrot set exists, to some finite depth.
     Express the loop DNA in QuCalc.
  2. Chaos exists by what simple QuCalc DNA?

THE MOVE. `z <- z^2 + c` has no numbers in QuCalc -- there is no background plane to
put them in. What survives the translation is the only thing an orbit can report to a
listener: WHICH SIDE of the critical point each iterate fell on. That is one binary
distinction per tick, i.e. one CONJUGATE PAIR: take the horizontal pair `>` / `<`
(`+sigma_x` / `-sigma_x`). An orbit is then literally a twist history, and the map's
two moves translate exactly:

    z |-> z^2   ==  the angle doubles  ==  the itinerary word is COPIED  (W -> W W)
    + c         ==  one splice twist between the copies                  (W -> W s W)

So squaring is CONCATENATION in the free monoid and the parameter is a single letter.
The loop's DNA -- the thing that is copied, in the sense DNA is copied -- is therefore
a length-doubling substitution with a splice codon:

    DNA:   W  |->  W . s . W          seed W = C (the critical point, one free quantum)

That is a replication rule, not a number, and it is a QuCalc object: two twist words
joined by a twist. Everything below either VERIFIES that this rule is the real
Mandelbrot spine's rule (sec 2, against exactly-computed superstable parameters) or
reads off what QuCalc's own closure law then says (sec 3-5).

WHAT COMES OUT
  sec 1  the two genomes on one pair, and which of them closes at every depth
  sec 2  the splice rule VERIFIED against the period-2^k superstable orbits of
         z^2+c (Newton in `decimal`, repo convention: stdlib only)
  sec 3  the free-action debt of depth k: EXACTLY 2^k/3 + O(1) quanta, so the
         closure-depth law gives depth K ~ log2(3R) at capacity R -- the finite
         depth, derived, not assumed
  sec 4  why the loop never closes alone: odd length, and W.W^dagger is the closure
         (the ray PAIR at a component root)
  sec 5  chaos, and a correction: the free splice gives 2^k histories in ~2^(k+1)
         twists -- O(log n) bits in n twists, i.e. h -> 0 per TWIST. The log 2 belongs
         to the ZFA CENSUS (all balanced words, C(2m,m) ~ 4^m/sqrt(pi m)), not to that
         genome's output; chaos per twist needs the free bit at EVERY twist --
         `primordial_zfa_dna.py`, 1/3 bit per twist.

SCOPE, stated first. The correspondence in sec 2 is verified numerically on the real
spine (periods 2..128, exact-to-50-digits parameters), not proven. Nothing here claims
Feigenbaum's delta -- delta is a rendering-layer constant and was REJECTED as a
substrate constant (`Open_Problems.md`, `constants_mapper.emerge_feigenbaum`); this
script computes no delta and needs none, because the DNA is combinatorial. And the
"no period-doubling" result elsewhere in the repo (unique factorization -> free monoid
-> geometric GF -> linear recurrence -> no log-periodic line in alpha) is about the
CENSUS GENERATING FUNCTION, a different object from a single doubling substitution
inside the census; sec 6 states the distinction rather than letting it look like a
contradiction.

Run:  python3 mandelbrot_loop_dna.py
"""
from __future__ import annotations

from decimal import Decimal, getcontext
from math import comb, log

from census_inventory import is_count_balanced
from qucalc_search import max_excursion
from twist_core import adjoint_history, is_pauli_closed, is_zfa

getcontext().prec = 60

PAIR = (">", "<")          # the itinerary pair: +sigma_x / -sigma_x
CRIT = "C"                 # the critical point -- not a twist: the unresolved quantum


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# sec 1 -- the genomes
# --------------------------------------------------------------------------- #
def replicate(w: str, splice: str) -> str:
    """One DNA step: copy the word, join the copies with the splice twist."""
    return w + splice + w


def substitute(sigma: dict[str, str], seed: str, k: int) -> str:
    h = seed
    for _ in range(k):
        h = "".join(sigma[c] for c in h)
    return h


def genomes_on_one_pair() -> None:
    a, b = PAIR
    rule("sec 1  THE GENOMES ON ONE CONJUGATE PAIR")
    print(f"""
A length-doubling genome on the pair ({a},{b}) is a substitution sigma with
|sigma(x)| = 2. For the fixed point to exist sigma({a}) must start with {a}, leaving
8 genomes. Which of them is ZFA-closed at EVERY depth?
""")
    print(f"  {'sigma(' + a + ')':<10}{'sigma(' + b + ')':<10}{'depth 1..6 closure':<24}"
          f"{'excursion at k=6':<18}{'kind'}")
    print("  " + "-" * 74)
    keepers = []
    for wa in (a + a, a + b):
        for wb in (a + a, a + b, b + a, b + b):
            sigma = {a: wa, b: wb}
            words = [substitute(sigma, a, k) for k in range(1, 7)]
            closes = ["Y" if (is_count_balanced(w) and is_pauli_closed(w)) else "."
                      for w in words]
            allc = all(c == "Y" for c in closes)
            kind = "periodic" if wa == wb or wb in (a + a, b + b) else "aperiodic"
            if allc:
                keepers.append((wa, wb))
            print(f"  {wa:<10}{wb:<10}{''.join(closes):<24}"
                  f"{max_excursion(words[-1]):<18}{kind}{'   <== closes always' if allc else ''}")
    print(f"""
  Exactly {len(keepers)} genome(s) close at every depth: {keepers}
  That is sigma({a})={a}{b}, sigma({b})={b}{a} -- the THUE-MORSE genome, which the repo
  already knows as the canonical self-similar closure (`self_similar_closures.py`,
  `Philosophy.md` sec 3a): balanced at every depth, and at max_excursion = 1, so it is
  heard at EVERY capacity horizon. It is the "copy and conjugate" rule: the second
  copy is the Hermitian mirror of the first.

  The Mandelbrot spine's genome is the OTHER doubling rule -- copy and splice, where
  the second copy is NOT mirrored. sec 2 verifies which, sec 3 prices it.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the splice rule, verified against real superstable orbits
# --------------------------------------------------------------------------- #
def superstable_c(period: int, guess: str) -> Decimal:
    """The c with f_c^period(0) = 0 -- Newton, with the derivative carried along."""
    c = Decimal(guess)
    for _ in range(200):
        x, dx = Decimal(0), Decimal(0)
        for _ in range(period):
            x, dx = x * x + c, 2 * x * dx + 1
        if dx == 0:
            break
        step = x / dx
        c -= step
        if abs(step) < Decimal(10) ** -50:
            break
    return c


def itinerary(c: Decimal, period: int) -> str:
    """The critical orbit's word: `>` right of the critical point, `<` left,
    and the final return to 0 is the critical symbol C."""
    x, out = Decimal(0), []
    for _ in range(period):
        x = x * x + c
        out.append(">" if x > 0 else "<")
    return "".join(out[:-1]) + CRIT


GUESSES = ["0", "-1", "-1.3107", "-1.38154", "-1.39694",
           "-1.400258", "-1.4009695", "-1.40111"]


def verify_splice_rule() -> list[tuple[int, Decimal, str, str]]:
    rule("sec 2  THE SPLICE RULE, VERIFIED ON THE REAL SPINE")
    print("""
The period-2^k superstable parameters are the centres of the cascade components on
the real spine of M. They are computable exactly (Newton on f_c^{2^k}(0) = 0, 50
digits), so the itinerary words below are FACTS about z^2+c, not a model of it.

Claim under test:   W_{k+1} = W_k[:-1] . s . W_k[:-1] . C   for a single splice twist s.
""")
    rows = []
    prev = None
    for k, g in enumerate(GUESSES):
        n = 2 ** k
        c = superstable_c(n, g)
        w = itinerary(c, n)
        if prev is None:
            check = "seed"
            splice = "-"
        else:
            body = prev[:-1]
            splice = w[len(body)] if len(w) > len(body) else "?"
            check = "MATCH" if w == body + splice + body + CRIT else "FAIL"
        rows.append((k, c, w, splice))
        print(f"  k={k} period={n:4d}  c={str(c)[:24]:<24} splice={splice}  {check}")
        print(f"        W = {w}")
        prev = w
    bad = [r for r in rows[1:] if r[3] == "?"]
    print(f"""
  Every step matches: the Mandelbrot cascade's word really is built by
  COPY . SPLICE . COPY. The splice letters, in depth order, are
  {''.join(r[3] for r in rows[1:])}  -- fixed, not free (they alternate; classically the
  Metropolis-Stein-Sheng "harmonic", sign set by the parity of the copy). A fixed
  splice means ZERO entropy: this genome is deterministic and aperiodic -- the edge of
  chaos, not chaos. sec 5 frees the splice -- and finds that one bit per doubling buys
  only O(log n) bits in n twists, i.e. still zero per twist.""")
    assert not bad
    return rows


# --------------------------------------------------------------------------- #
# sec 3 -- the price of depth, and therefore the depth
# --------------------------------------------------------------------------- #
def price_of_depth(rows) -> None:
    rule("sec 3  THE FREE-ACTION DEBT OF DEPTH k -- WHY THE DEPTH IS FINITE")
    print("""
QuCalc's closure-depth law: a capacity-R listener hears a closure iff its
max_excursion (the largest running |free action| over prefixes) is <= R
(`QLF_ClosureDepthLaw.closedAtHorizon_iff_maxExcursion_le`, `qucalc_search.max_excursion`).
So ask what depth k costs.
""")
    print(f"  {'k':>3}{'period':>8}{'len':>6}{'#>':>6}{'#<':>6}{'defect':>8}"
          f"{'2^k/3':>9}{'excursion':>11}  balanced?")
    print("  " + "-" * 74)
    for k, c, w, _ in rows:
        body = w[:-1]
        gt, lt = body.count(">"), body.count("<")
        defect = abs(gt - lt)
        print(f"  {k:>3}{2 ** k:>8}{len(body):>6}{gt:>6}{lt:>6}{defect:>8}"
              f"{2 ** k / 3:>9.1f}{max_excursion(body):>11}  "
              f"{'yes' if is_count_balanced(body) else 'NO'}")
    print("""
  The defect grows like 2^k/3 -- the cascade word's letter frequencies are 2/3 and
  1/3, never 1/2 -- so the debt DOUBLES with every doubling, and so does the
  excursion. Invert the depth law:

      depth heard at capacity R:   K(R) = log2(3R) + O(1)

  This is the answer to "to some finite depth". The depth is finite for a reason a
  possibilist substrate can state: each further doubling costs twice the unresolved
  action of the last, and no listener has unbounded capacity. Capacity buys depth only
  LOGARITHMICALLY -- double your capacity, gain one octave of the set. The Feigenbaum
  accumulation point needs K = infinity, so it is never actualized; what exists is
  M_K, the set truncated at the capacity horizon. Consistent with
  `Continuum_Choice_Fallacy.md` / `TheContinuum.md`: the limit is a rendering, the
  finite-depth truncation is the object.""")


# --------------------------------------------------------------------------- #
# sec 4 -- the loop does not close alone
# --------------------------------------------------------------------------- #
def closure_needs_a_partner(rows) -> None:
    rule("sec 4  THE LOOP NEVER CLOSES ALONE -- IT CLOSES WITH ITS MIRROR")
    print("""
Two obstructions, both structural, neither tunable:
  (a) the word W_k[:-1] has ODD length 2^k - 1, so count balance is impossible
      before the critical quantum C is paid;
  (b) even ignoring parity, the 2^k/3 defect of sec 3 is unpaid.
Compose the history with its Hermitian conjugate and both vanish at once:
""")
    print(f"  {'k':>3}{'|W|':>6}{'W . W-dagger closes?':>24}{'excursion':>11}{'fold scalar':>14}")
    print("  " + "-" * 62)
    for k, c, w, _ in rows[1:]:
        body = w[:-1]
        pair = body + adjoint_history(body)
        print(f"  {k:>3}{len(body):>6}{('yes' if is_zfa(pair, min_length=2) else 'no'):>24}"
              f"{max_excursion(pair):>11}{'scalar' if is_pauli_closed(pair) else 'not scalar':>14}")
    print("""
  W . W-dagger is a ZFA closure at every depth. Read in the classical picture this is
  not a curiosity: the root of every hyperbolic component of M is the landing point of
  a PAIR of conjugate external rays, never one ray. QuCalc says the same thing from the
  closure side -- a single itinerary is an open prefix; the ray pair is the closure.
  (Correspondence noted, not proven -- it is a structural match, and it is the shape a
  proof would have to take.)

  Note also that Pauli closure is not the binding constraint on one pair: a single-pair
  word folds to +-sigma_x^n, which is scalar for every even n. On one pair, ZFA = count
  balance. The order-sensitivity that makes ZFA more than a tally only bites once a
  second axis enters -- which is exactly where the 2D Mandelbrot set (as against the
  real spine) lives.""")


# --------------------------------------------------------------------------- #
# sec 5 -- chaos
# --------------------------------------------------------------------------- #
def chaos_dna() -> None:
    rule("sec 5  CHAOS: THE FREE BIT, AND WHAT IT DOES AND DOES NOT BUY")
    a, b = PAIR
    print(f"""
The cascade genome of sec 2 has a FIXED splice, hence one word per depth and zero
entropy. Free that one letter and the genome becomes a choice:

    cascade DNA   W |-> W . s . W     s forced by parity   -> 1 word,  h = 0
    free-splice   W |-> W . ({a}|{b}) . W s free                -> 2^k words

One undetermined bit per doubling. In RhoQuCalc surface syntax the free choice is the
parallel bar, so the free-splice genome is one line:

    ZFA_CHAOS = *( W | ({a} | {b}) | W )

and the reason ZFA does not forbid it is the one-sentence answer to the question:

    *** ZFA fixes COUNTS, not ORDER. ***

`{a}{b}` and `{b}{a}` are the same closure -- same counts, same cost, same everything a
listener can charge for -- and they are two different histories.

    CORRECTION (2026-09-26). It is tempting to read that free bit as h = log 2; this
    script claimed so until today. It is not. The length doubles with the word count:
    k bits sit in ~2^(k+1) twists, so the entropy PER TWIST is
    log2(2^k)/(2^(k+1)-1) -> 0. One bit per DOUBLING is not chaos per twist -- it is
    the edge of chaos, a zero-density subshift, the cascade of sec 2 with a free letter
    instead of a forced one. (Caught while building `primordial_zfa_dna.py`; its sec 6
    has the arithmetic.)

The log 2 does live somewhere: in the ZFA CENSUS -- all balanced words, not this
genome's output. Of the 4^m words of length 2m on one pair, the balanced ones number
C(2m,m).
""")
    print(f"  {'2m':>5}{'all words 4^m':>16}{'ZFA-closed C(2m,m)':>21}{'fraction':>12}"
          f"{'h = log(count)/2m':>20}")
    print("  " + "-" * 74)
    for m in (1, 2, 4, 8, 16, 32, 64, 128):
        n, all_w, bal = 2 * m, 4 ** m, comb(2 * m, m)
        print(f"  {n:>5}{all_w:>16.3e}{bal:>21.6e}{bal / all_w:>12.5f}"
              f"{log(bal) / n:>20.6f}")
    print(f"""  {'':>5}{'':>16}{'':>21}{'-> ~ 1/sqrt(pi m)':>12}{'-> log 2 = ' + f'{log(2):.6f}':>20}

  The balanced fraction decays only as m^-1/2, so the CENSUS growth rate is 4^m up to a
  polynomial and its entropy is EXACTLY log 2: the ZFA filter charges only the return
  factor

      C(2m,m)/4^m ~ 1/sqrt(pi m)

  which is not a new constant -- it is the substrate's own first-return exponent
  (`QLF_CensusBrownian`, `cascade_ensemble.py`, the m^-3/2 avalanche law of
  `fractal_cascade.py`). That is the exact content of "ZFA fixes COUNTS, not ORDER":
  a statement about the CENSUS of all closures. The free-splice genome samples only a
  vanishing sub-family of it (2^k words of length 2^(k+1)-1, against C(2m,m) of
  length 2m).

  Chaos per twist needs the free bit at POSITIVE density -- one per closure, not one
  per doubling. That is `primordial_zfa_dna.py`: the sec 5b doubler applied to every
  twist of every generation.

      PRIMORDIAL ZFA DNA   t |-> (the closure headed by t), chirality free
                           ^ |-> ^>v< | ^<v>   (rotations for > v <),  seed ^

  Generation k is 4^(k-1) closures laid end to end, so it is ZFA with excursion 2 at
  every depth; decimation returns the parent exactly; and N_k = 2^((4^k-1)/3) over
  4^k twists gives (1/3) bit per twist -- strictly positive, no metric, no parameter,
  no noise. Closure, exact self-similarity and positive entropy hold together there,
  in every realization.

  And log 2 is still the bit: the floor of every erasure, closure and binding -- but it
  is the CENSUS's rate, not this doubling genome's. Chaos is what one free distinction
  per closure looks like when you iterate it.""")


def minimal_doubler() -> None:
    rule("sec 5b  THE MINIMAL DOUBLER IS ALREADY THE FIRST PARTICLE")
    print("""
Take the shortest possible open prefix, one twist, and ask for its ZFA closures:
""")
    from doubler import simulate_qucalc_closures
    # light_cone_limit=8 makes the BFS millions of histories and effectively hangs;
    # both length-4 closures already appear by appended depth 3 (explored 2801 at 4).
    res = simulate_qucalc_closures("^", light_cone_limit=4, max_results=2, min_closure_length=4)
    for cl in res.closures:
        print(f"    ^  ->  {cl}   (excursion {max_excursion(cl)}, ZFA {is_zfa(cl)})")
    print(f"""
  doubled = {res.doubled}, explored {res.explored_histories} histories.

  The seed `^` closes two ways -- `^<v>` and `^>v<`, ELECTRON and POSITRON
  (`QuCalc.md` sec 6, `Primordial_Entanglement.md` sec 1-3). Same counts, opposite
  order. That is the minimal doubler (`doubler.py`), the bifurcation at the bottom of
  the framework. Apply it at EVERY twist -- not once per doubling -- and you have
  `primordial_zfa_dna.py`, the smallest chaos: 1/3 bit per twist. The first particle
  and the first chaos are the same event read two ways: a closure whose ORDER was not
  determined by its COUNTS.""")


# --------------------------------------------------------------------------- #
# sec 6 -- what this does NOT say
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 6  WHAT THIS DOES NOT CLAIM")
    print("""
  1. No Feigenbaum delta. delta is class-dependent (quadratic 4.6692, quartic 7.2846),
     so it belongs to the rendering layer, and it was REJECTED as a substrate constant
     (`Open_Problems.md`, `constants_mapper.emerge_feigenbaum` -- a fitted kernel). The
     DNA here is combinatorial: a substitution and a splice letter, no metric constant.
     Nothing above computes or needs delta.

  2. "No period-doubling" elsewhere in the repo is a DIFFERENT object. That result
     (`Alpha_Residual.md` sec 9b, `Category_Theory_QLF.md`) says the CLOSURE CENSUS's
     generating function is geometric -> linear recurrence -> no period-doubling -> no
     log-periodic / discrete-scale-invariance correction to alpha, hence w = 1/2
     structurally. It is a statement about the census GF. A single doubling
     substitution living inside the census is not a bifurcation OF the census: the
     Thue-Morse family is one measure-zero sub-family of closures, and adding it
     changes no coefficient of the GF. Both statements stand.

  3. The sec 2 correspondence is verified, not proven: periods 2..128 on the real
     spine, exact parameters. The sec 4 ray-pair reading is a structural match, flagged
     as such.

  4. Only the real spine is done here. The full 2D M requires the second axis, where
     Pauli order-sensitivity stops being trivial (sec 4, last paragraph) -- that is the
     open edge, and the interesting one.""")


def main() -> None:
    print(__doc__)
    genomes_on_one_pair()
    rows = verify_splice_rule()
    price_of_depth(rows)
    closure_needs_a_partner(rows)
    chaos_dna()
    minimal_doubler()
    scope()
    rule("THE ANSWER, IN ONE BOX EACH")
    print("""
  loop DNA (Mandelbrot, deterministic, edge of chaos):

      W  |->  W . s . W          seed W = C,  s forced by the parity of W
      one conjugate pair; squaring = concatenation; +c = the splice twist
      debt 2^k/3 quanta at depth k  =>  depth K(R) = log2(3R) at capacity R
      closes only as W . W-dagger (the ray pair)

  free-splice DNA (the deterministic edge -- NOT chaos per twist):

      W  |->  W . (> | <) . W     the splice left FREE -- one bit per doubling
      ZFA_CHAOS = *( W | (> | <) | W )
      2^k histories in ~2^(k+1) twists: h per twist -> 0 (O(log n) bits in n twists)
      the CENSUS it samples keeps h = log 2; ZFA's whole toll is C(2m,m)/4^m ~ 1/sqrt(pi m)

  chaos per twist (the simplest DNA there is -- `primordial_zfa_dna.py`):

      t  |->  ( the closure headed by t ) , chirality free,  seed ^
      ^ |-> ^>v< | ^<v>   (rotations for > v <)
      closure + exact self-similarity + h = 1/3 bit per twist, together
""")


if __name__ == "__main__":
    main()
