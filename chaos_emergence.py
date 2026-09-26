#!/usr/bin/env python3
"""
chaos_emergence.py -- how chaos emerges from a simple rule, and where the free bit must sit.

THE QUESTION (Jim, 2026-09-26): "you might want to look first at simple chaos emergence."
And the method it sits under: rather than enumerate all ways, find the simplest path --
any way at all is a result that happens in finite time.

THE POINT. Chaos is not an extra ingredient -- no noise, no parameter, no metric, no
control dial. It is free ORDER at positive density. One substitution with one free letter
is enough, but only if the free letter is spent where the closures are:

    mechanism                           free distinctions    twists        h (bits/twist)
    ------------------------------------------------------------------------------------
    cascade (splice fixed)              0                    2^(k+1)-1     0
    free splice, once per doubling      k                    2^(k+1)-1     -> 0
    primordial DNA, one per closure     (4^k-1)/3            4^k           1/3
    unconstrained census                log2 C(2m,m)         2m            -> 1

Active-inference reading (Active_Inference_Mathematics.md sec 3): every closure event is
one free binary distinction, the 50/50 partition that saturates D_KL = log 2 nats
(`active_inference_vfe_demo.py`). So h per twist IS the density of free distinctions, and
chaos emerges exactly when that density is positive. In the twist algebra the simplest
positive density is the primordial 1/3 -- one free chirality per closure, at every scale
at once, so every finite realization is already chaos.

  sec 1  the control: one substitution, one free letter
  sec 2  the onset: spend the free bit at the density of closures
  sec 3  the spectrum: 0 -> 1/3 -> 1, and why 1/3 is the minimal chaos
  sec 4  scope

Run:  python3 chaos_emergence.py
"""
from __future__ import annotations

from math import lgamma, log

from primordial_zfa_dna import DNA, realize
from qucalc_search import max_excursion
from twist_core import calculate_action, is_zfa

LN2 = log(2)


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def h_bits(log2_histories: float, twists: int) -> float:
    """Free distinctions per twist, in bits."""
    return log2_histories / twists


def log2_comb(n: int, k: int) -> float:
    """log2 C(n, k) without building the integer (safe for large n)."""
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / LN2


def flip_block(history: str, i: int) -> str:
    """Swap the chirality of the length-4 block at i -- free ORDER, same counts."""
    block = history[i:i + 4]
    electron, positron = DNA[block[0]]
    return history[:i] + (positron if block == electron else electron) + history[i + 4:]


# --------------------------------------------------------------------------- #
# sec 1 -- the control
# --------------------------------------------------------------------------- #
def control() -> None:
    rule("sec 1  THE CONTROL: ONE SUBSTITUTION, ONE FREE LETTER")
    print("""
The loop DNA of `mandelbrot_loop_dna.py` copies a word and joins the copies with one
splice twist:

    W  |->  W . s . W          seed W = C

Fixed splice: deterministic, one word per depth -- the edge of chaos. Free the splice
(`s` in {>,<}) and each doubling carries a free bit:
""")
    print(f"  {'k':>3}{'words 2^k':>12}{'twists 2^(k+1)-1':>20}{'h (bits/twist)':>17}")
    print("  " + "-" * 53)
    for k in (1, 2, 4, 8, 16, 32):
        words = 2 ** k
        twists = 2 ** (k + 1) - 1
        print(f"  {k:>3}{words:>12}{twists:>20}{h_bits(k, twists):>17.3e}")
    print("""
  Fixed splice: 1 word, h = 0.  Free splice: 2^k words, but the length doubles with them,
  so h -> 0 too. A free bit per DOUBLING is O(log n) bits in n twists: total information
  grows, density vanishes. That is the edge of chaos, not chaos.""")


# --------------------------------------------------------------------------- #
# sec 2 -- the onset
# --------------------------------------------------------------------------- #
def onset() -> None:
    rule("sec 2  THE ONSET: SPEND THE FREE BIT AT THE DENSITY OF CLOSURES")
    print("""
The primordial split closes `^` two ways -- `^>v<` and `^<v>` (`Primordial_Entanglement.md`
sec 1-3). Make it the rule for EVERY twist, not once:

    t  |->  (the closure headed by t), chirality free,   seed ^

Every length-4 block is a closure, so generation k is a concatenation of closures and the
free bit is spent once per closure. There are (4^k-1)/3 closures in generation k (one per
block, at every scale), so the density is positive:
""")
    print(f"  {'k':>3}{'twists 4^k':>12}{'closures (4^k-1)/3':>21}"
          f"{'log2 histories':>16}{'h (bits/twist)':>17}")
    print("  " + "-" * 70)
    for k in (1, 2, 4, 6, 8):
        twists = 4 ** k
        log2_hist = (4 ** k - 1) // 3          # = log2 2^((4^k-1)/3)
        print(f"  {k:>3}{twists:>12}{log2_hist:>21}{log2_hist:>16}{h_bits(log2_hist, twists):>17.6f}")
    print("""
  The density (closures)/(twists) -> 1/3, so h -> 1/3 bit per twist. Strictly positive at
  every depth, with no metric, parameter or noise source.

  And the free bit is real order, not a rounding artefact: flip any one block's chirality
  and the counts, the closure status and the excursion are unchanged -- only the history
  changes. (The listener's ledger cannot tell the two realizations apart.)
""")
    gens, _ = realize(4, None, 0)
    h = gens[4]
    flipped = flip_block(h, 4)             # flip the second block, generation 4
    same = calculate_action(h) == calculate_action(flipped) and sorted(h) == sorted(flipped)
    print(f"    block 2 flipped: same counts {same}, "
          f"both ZFA {is_zfa(h) and is_zfa(flipped)}, "
          f"excursion {max_excursion(h)} / {max_excursion(flipped)}, "
          f"histories differ {h != flipped}")


# --------------------------------------------------------------------------- #
# sec 3 -- the spectrum
# --------------------------------------------------------------------------- #
def spectrum() -> None:
    rule("sec 3  THE SPECTRUM: 0 -> 1/3 -> 1")
    print(f"  {'mechanism':<40}{'log2 histories':>16}{'h (bits/twist)':>17}")
    print("  " + "-" * 73)
    rows = [
        ("cascade (splice fixed), depth 32", 0.0, 2 ** 33 - 1),
        ("free splice, once per doubling, k=32", 32.0, 2 ** 33 - 1),
        ("primordial DNA, one per closure, k=8", float((4 ** 8 - 1) // 3), 4 ** 8),
        ("unconstrained census, 2m=20000", log2_comb(20000, 10000), 20000),
    ]
    for label, log2_hist, twists in rows:
        print(f"  {label:<40}{log2_hist:>16.4f}{h_bits(log2_hist, twists):>17.6f}")
    print("""
      0           0           1/3                    1
      |-----------|------------|--------------------|
      edge of chaos          primordial          full shift
      (no free order)        (simplest chaos)    (every twist free)

  Any positive density of free distinctions is chaos; zero density is the edge. The cascade
  and the free splice sit at 0. The primordial construction sits at the first positive
  value the twist algebra offers, 1/3 -- free order at exactly the density of closures. The
  unconstrained census tops out at 1, where every twist is free and ZFA keeps a 1/sqrt(pi m)
  fraction of an exponentially growing set.

  So chaos does not need a dial, a noise source or a metric -- only free order where the
  closures are. The free bit is the whole of it (Philosophy.md sec 3a: "what happens in the
  most ways happens first" -- here the most-ways history is the one whose ORDER ZFA leaves
  open, at density 1/3).""")
    # the numbers, restated
    assert h_bits(0.0, 2 ** 33 - 1) == 0.0
    assert h_bits(32.0, 2 ** 33 - 1) < 1e-8
    assert 0.33 < h_bits(float((4 ** 8 - 1) // 3), 4 ** 8) < 0.334
    assert h_bits(log2_comb(20000, 10000), 20000) > 0.99


# --------------------------------------------------------------------------- #
# sec 4 -- scope
# --------------------------------------------------------------------------- #
def scope() -> None:
    rule("sec 4  SCOPE")
    print("""
  1. h is the entropy of a GENERATION (distinct generation-k histories over their length),
     not the factor complexity of the infinite language. Same caveat as
     `primordial_zfa_dna.py` sec 6.

  2. The three mechanisms are CONSTRUCTIONS, not a classification. Exhibiting one shows it
     happens in some way, never the only way (CLAUDE.md sec 3a). The claim here is narrow:
     the free-splice genome is not chaos per twist, and a single substitution becomes chaos
     as soon as its free bit has positive density.

  3. Nothing here is a physical mechanism. "Chaos" is positive entropy in the twist algebra;
     no identification with a physical instability or with the Feigenbaum delta is made (delta
     is class-dependent and was rejected as a substrate constant, Open_Problems.md).""")


def main() -> None:
    print(__doc__)
    control()
    onset()
    spectrum()
    scope()


if __name__ == "__main__":
    main()
