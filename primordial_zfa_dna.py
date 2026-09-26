#!/usr/bin/env python3
"""
primordial_zfa_dna.py -- the primordial ZFA DNA in QuCalc: possibilist chaos that is
self-similar.

THE QUESTION (Jim, 2026-09-26, following `mandelbrot_loop_dna.py`):
  "QuCalc primordial ZFA DNA" -- "possibilistic chaos having self similarity."

THE MOVE. The primordial split is `^` resolving two ways, `^>v<` and `^<v>` --
electron and positron (`Primordial_Entanglement.md` sec 1-2, `QuCalc.md` sec 6): SAME
counts, OPPOSITE order. Make that event the replication rule for EVERY twist, not just
the first one:

    PRIMORDIAL DNA:   t  |->  the closure that starts with t, in either chirality

        ^  |->  ^>v<  |  ^<v>          >  |->  >v<^  |  >^<v
        v  |->  v<^>  |  v>^<          <  |->  <^>v  |  <v>^

Each image is a cyclic rotation of the electron or the positron loop, headed by the
twist it replaces. The `|` is the RhoQuCalc parallel bar: the choice is FREE, and it is
made independently at every twist of every generation. Seed: `^`, the first distinction.

WHAT COMES OUT (each checked below, not asserted)
  sec 1  every image is a ZFA closure (count balance AND Pauli fold = scalar)
  sec 2  CLOSED AT EVERY DEPTH, EVERY REALIZATION: a generation-k history is a
         concatenation of 4^(k-1) closures, so it is ZFA -- and its max_excursion is
         2 at every depth. Contrast `mandelbrot_loop_dna.py` sec 3, where the splice
         genome's debt grows as 2^k/3. This DNA is heard at every capacity horizon.
  sec 3  SELF-SIMILAR, EXACTLY: decimation (keep every 4th twist -- the block heads)
         returns the parent history, for every realization. The parent is written
         entirely in ORDER; the COUNTS of every block are zero. The coarse scale is
         invisible to a tally and fully present to a Pauli fold.
  sec 4  CHAOTIC, EXACTLY: the realizations are all distinct (decimation + chirality
         read-off is a decoder), so generation k has N_k = 2^((4^k - 1)/3) histories
         of length 4^k: entropy -> 1/3 bit per twist, strictly positive.
  sec 5  the free bit IS "ZFA fixes counts, not order": swapping chirality of any block
         changes no count and no closure status, only the history.
  sec 6  scope, and a correction to `mandelbrot_loop_dna.py` sec 5.

Run:  python3 primordial_zfa_dna.py
"""
from __future__ import annotations

import random
from math import log2

from qucalc_search import max_excursion
from twist_core import calculate_action, is_pauli_closed, is_zfa

SEED = "^"
ELECTRON, POSITRON = "^>v<", "^<v>"


def rotations_from(loop: str) -> dict[str, str]:
    """Each twist -> the cyclic rotation of `loop` that starts with it."""
    return {loop[i]: loop[i:] + loop[:i] for i in range(len(loop))}


# DNA[t] = (electron-chirality image, positron-chirality image)
_E, _P = rotations_from(ELECTRON), rotations_from(POSITRON)
DNA = {t: (_E[t], _P[t]) for t in "^>v<"}


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def grow(history: str, bits) -> str:
    """One generation: every twist replaced by its closure; `bits` picks chirality."""
    return "".join(DNA[t][b] for t, b in zip(history, bits))


def realize(k: int, rng: random.Random | None, fixed: int = 0) -> tuple[list[str], list[list[int]]]:
    """Generations 0..k of one realization. rng=None -> all-`fixed` chirality."""
    gens, choices = [SEED], []
    for _ in range(k):
        h = gens[-1]
        bits = [rng.randrange(2) if rng else fixed for _ in h]
        choices.append(bits)
        gens.append(grow(h, bits))
    return gens, choices


def decimate(history: str) -> str:
    return history[::4]


def read_bits(history: str) -> list[int]:
    """Chirality of each block, read back from the history alone."""
    out = []
    for i in range(0, len(history), 4):
        block = history[i:i + 4]
        e, p = DNA[block[0]]
        assert block in (e, p), block
        out.append(0 if block == e else 1)
    return out


# --------------------------------------------------------------------------- #
def sec1() -> None:
    rule("sec 1  THE DNA TABLE -- EVERY IMAGE IS A CLOSURE")
    print(f"  {'twist':<7}{'electron-rot':<14}{'positron-rot':<14}{'both ZFA?':<11}{'same counts?'}")
    print("  " + "-" * 60)
    for t, (e, p) in DNA.items():
        ok = is_zfa(e) and is_zfa(p)
        same = calculate_action(e) == calculate_action(p) and sorted(e) == sorted(p)
        print(f"  {t:<7}{e:<14}{p:<14}{'yes' if ok else 'NO':<11}{'yes' if same else 'NO'}")
        assert ok and same and e != p
    print("""
  Eight closures, four twists, two chiralities. Each pair differs ONLY in order.""")


def sec2(rng: random.Random) -> list[str]:
    rule("sec 2  CLOSED AT EVERY DEPTH, IN EVERY REALIZATION")
    print(f"  {'k':>3}{'length':>9}{'ZFA (fixed e)':>15}{'ZFA (random)':>14}"
          f"{'excursion':>11}{'splice debt 2^k/3 (Mandelbrot)':>34}")
    print("  " + "-" * 86)
    K = 7
    fixed, _ = realize(K, None, 0)
    rand, _ = realize(K, rng)
    for k in range(1, K + 1):
        zf, zr = is_zfa(fixed[k]), is_zfa(rand[k])
        ex = max(max_excursion(fixed[k]), max_excursion(rand[k]))
        print(f"  {k:>3}{len(rand[k]):>9}{('yes' if zf else 'NO'):>15}{('yes' if zr else 'NO'):>14}"
              f"{ex:>11}{2 ** k / 3:>34.1f}")
        assert zf and zr and ex == 2
    # many random realizations at moderate depth
    for _ in range(300):
        g, _ = realize(4, rng)
        assert is_zfa(g[4]) and max_excursion(g[4]) == 2
    print("""
  Plus 300 further random realizations at k=4: all ZFA, all excursion 2.

  Why: a generation-k history is 4^(k-1) closures laid end to end. Counts add to zero
  and the Pauli fold is a product of scalars. The running free action never leaves
  the current length-4 loop, so it never exceeds 2 -- at ANY depth. The Mandelbrot
  splice genome pays 2^k/3 for depth k and so is heard only to K(R) = log2(3R); the
  primordial genome pays nothing for depth. Depth is free when every copy closes.""")
    return rand


def sec3(rand: list[str]) -> None:
    rule("sec 3  SELF-SIMILAR, EXACTLY -- THE PARENT IS WRITTEN IN ORDER ALONE")
    for k in range(1, len(rand)):
        assert decimate(rand[k]) == rand[k - 1]
    k = 3
    print(f"""  One random realization, generation {k} (length {len(rand[k])}):

    {rand[k]}

  keep every 4th twist (the block heads):

    {decimate(rand[k])}   ==  generation {k - 1}: {decimate(rand[k]) == rand[k - 1]}

  and again:  {decimate(decimate(rand[k]))}   ==  generation {k - 2}

  Checked for every generation of the sec 2 realization (k = 1..{len(rand) - 1}).

  Every length-4 block has ZERO counts on both axes, so a tally of the child sees
  nothing of the parent -- the parent's own counts are lost. Yet the parent is fully
  present: it is the sequence of block HEADS, i.e. pure order. Coarse-graining a
  history in this DNA does not blur it; it returns the previous generation exactly.
  The self-similarity lives in the one place ZFA does not charge for.""")


def sec4(rng: random.Random) -> None:
    rule("sec 4  CHAOTIC, EXACTLY -- 1/3 BIT PER TWIST")
    # decoder round-trip: history -> (parent history, chirality bits) is injective
    for _ in range(500):
        g, ch = realize(4, rng)
        h = g[4]
        for k in range(4, 0, -1):
            assert read_bits(h) == ch[k - 1]
            h = decimate(h)
        assert h == SEED
    # brute force distinctness for small k
    def all_gen(k):
        cur = {SEED}
        for _ in range(k):
            nxt = set()
            for h in cur:
                for m in range(2 ** len(h)):
                    nxt.add(grow(h, [(m >> i) & 1 for i in range(len(h))]))
            cur = nxt
        return cur
    print(f"  {'k':>3}{'length 4^k':>12}{'N_k (brute)':>14}{'2^((4^k-1)/3)':>16}{'bits/twist':>13}")
    print("  " + "-" * 58)
    for k in range(1, 7):
        L, pred = 4 ** k, (4 ** k - 1) // 3
        brute = len(all_gen(k)) if k <= 2 else None
        if brute is not None:
            assert brute == 2 ** pred
        print(f"  {k:>3}{L:>12}{(str(brute) if brute else '(decoder)'):>14}"
              f"{'2^' + str(pred):>16}{pred / L:>13.6f}")
    print("""  ->  1/3

  Brute force at k = 1, 2; for k >= 3 distinctness follows from the decoder, checked
  on 500 random realizations: every history reads back its whole ancestry and every
  chirality bit (decimate for the parent, block identity for the bit). So the map
  (bits) -> history is injective, N_k = prod_j 2^(4^j) = 2^((4^k - 1)/3), and the
  entropy is (1/3) bit per twist -- one free bit per closure, at every scale at once.

  That is possibilist chaos in the strict sense: positive entropy, no metric, no
  parameter, no noise source -- just the order left unwritten.""")


def sec5() -> None:
    rule("sec 5  THE FREE BIT IS 'ZFA FIXES COUNTS, NOT ORDER'")
    print("""
  Flip any one block's chirality in any generation: counts unchanged, ZFA unchanged,
  excursion unchanged, history changed. The listener's ledger cannot tell the
  realizations apart; the histories are all different. The same bit, three ways:

    - the primordial split  ^ -> ^>v< | ^<v>        (matter / antimatter)
    - the minimal doubler   (`doubler.py`)
    - the chaos generator here, applied to every twist at every scale

  Determinism is the special case of a fixed choice. All-electron chirality gives one
  history per generation -- a deterministic self-similar fixed point of the
  substitution (sigma(^) starts with ^), the 2-axis analogue of the Thue-Morse genome
  of `mandelbrot_loop_dna.py` sec 1. Chaos is the same DNA with the bit left free.
  Self-similarity is not traded against chaos: every realization has it (sec 3).""")


def sec6() -> None:
    rule("sec 6  SCOPE, AND A CORRECTION")
    print("""
  1. The 1/3 bit/twist is the GENERATION entropy (distinct generation-k histories
     over their length). The factor complexity of the infinite language (counting
     all length-n subwords) is a separate quantity, NOT computed here.

  2. Closure here is by construction (concatenated closures); what is nontrivial is
     that closure, exact self-similarity and positive entropy hold TOGETHER, in every
     realization, with bounded excursion. No physical identification of the
     generations (e.g. with particle generations) is claimed.

  3. Correction to `mandelbrot_loop_dna.py` sec 5: the splice-free genome
     W -> W.(>|<).W makes 2^k histories of length 2^(k+1)-1, i.e. k bits over
     ~2^(k+1) twists -> ZERO entropy per twist. Its log 2 figure is the entropy of
     ALL balanced words (C(2m,m)), not of that genome's output. One bit per doubling
     is not chaos per twist; one bit per CLOSURE per generation, as here, is.""")


def main() -> None:
    print(__doc__)
    rng = random.Random(20260926)
    sec1()
    rand = sec2(rng)
    sec3(rand)
    sec4(rng)
    sec5()
    sec6()
    rule("THE ANSWER")
    print("""
      PRIMORDIAL ZFA DNA:   t |-> ( the closure headed by t ) , chirality free
                            ^ |-> ^>v< | ^<v>   (and rotations for > v <)
      seed ^ ; ZFA at every depth ; excursion 2 at every depth
      decimation returns the parent exactly  (self-similar, written in order)
      N_k = 2^((4^k-1)/3)  ->  1/3 bit per twist  (chaos)
""")


if __name__ == "__main__":
    main()
