#!/usr/bin/env python3
"""
quantum_biology_dna.py -- Schrodinger's aperiodic crystal on the twist substrate.

Companion to Quantum_Biology.md (sections 2 and 3). Every number printed is an exact
integer count or follows from one; nothing is fitted.

THE MAP. Watson-Crick pairs are conjugate pairs of twists on two spatial axes:

    A -> '>'   T -> '<'     (x axis)
    G -> '^'   C -> 'v'     (y axis)

Under this map the reverse complement of a strand IS `twist_core.adjoint_history`
(reverse the order, flip each twist). So a hairpin duplex  w . revcomp(w)  is the rung
W . W-dagger of ZFA_DNA.md section 5.

WHAT IS CHECKED (by enumeration, every sequence up to the stated length):

  sec 1  revcomp(w) == adjoint_history(map(w)) for every w.
  sec 2  every duplex w . w-dagger is a ZFA closure (count-balanced AND Pauli-closed),
         whatever the sequence; and its Pauli fold is (-1)^|w| . I for EVERY w, so the
         closure carries zero bits about the sequence. Persistence is sequence-blind;
         the 2|w| bits of sequence live only in the order of the twists.
  sec 3  the entropy ladder of section 3 of the doc: periodic crystal (0), Fibonacci
         quasicrystal (0, aperiodic but no code), duplex (1 bit/twist = 2 bits per base
         pair), all two-axis closures (-> 2 bits/twist). The number of two-axis closures
         of length 2n is C(2n,n)^2, checked against brute force.
  sec 4  a single strand is a closure only if #A = #T and #G = #C exactly (Chargaff's
         second parity rule made exact); the fraction of strands that are is
         C(2n,n)^2 / 16^n ~ 1/(pi n), checked against brute force.

    $ python3 quantum_biology_dna.py            # n <= 7, a few seconds
    $ python3 quantum_biology_dna.py --max-n 8
"""
import argparse
import itertools
import math
from fractions import Fraction

from twist_core import adjoint_history, calculate_action, is_pauli_closed, pauli_fold

BASE_TO_TWIST = {"A": ">", "T": "<", "G": "^", "C": "v"}
COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}
TOL = 1e-9


def to_twists(seq: str) -> str:
    return "".join(BASE_TO_TWIST[b] for b in seq)


def revcomp(seq: str) -> str:
    return "".join(COMPLEMENT[b] for b in reversed(seq))


def count_balanced(h: str) -> bool:
    return all(a == 0 for a in calculate_action(h))


def fold_scalar(h: str) -> complex:
    a, b, c, d = pauli_fold(h)
    assert abs(b) < TOL and abs(c) < TOL and abs(a - d) < TOL, h
    return a


def sec1_2(max_n: int) -> None:
    print("sec 1-2  duplex w . revcomp(w) as the rung W . W-dagger")
    print("  n   sequences   revcomp==adjoint   closed   distinct fold signs")
    for n in range(1, max_n + 1):
        same = closed = 0
        signs = set()
        for seq in map("".join, itertools.product("ATGC", repeat=n)):
            w = to_twists(seq)
            if to_twists(revcomp(seq)) == adjoint_history(w):
                same += 1
            duplex = w + adjoint_history(w)
            if count_balanced(duplex) and is_pauli_closed(duplex):
                closed += 1
            s = fold_scalar(duplex)
            signs.add(round(s.real) + 1j * round(s.imag))
        total = 4 ** n
        assert same == total and closed == total
        assert signs == {complex((-1) ** n, 0)}, signs
        print(f"  {n}   {total:9d}   {same:16d}   {closed:6d}   {sorted(signs, key=abs)}  = (-1)^{n}")
    print("  => every duplex closes; its fold is (-1)^n I for every sequence:"
          " H(sign | sequence) = 0 bits.\n")


def two_axis_closures(m: int) -> int:
    """Brute-force count of length-m words over > < ^ v with zero net count per axis."""
    return sum(1 for w in itertools.product("><^v", repeat=m) if count_balanced("".join(w)))


def fibonacci_word(k: int) -> str:
    a, b = "0", "01"
    for _ in range(k):
        a, b = b, b + a
    return b


def factor_complexity(word: str, n: int) -> int:
    return len({word[i:i + n] for i in range(len(word) - n + 1)})


def sec3(max_n: int) -> None:
    print("sec 3  the entropy ladder (bits per twist, length 2n)")
    print("  n   periodic   Fibonacci   duplex   all 2-axis closures  [C(2n,n)^2, brute]")
    for n in range(1, max_n + 1):
        exact = math.comb(2 * n, n) ** 2
        if 2 * n <= 10:
            assert two_axis_closures(2 * n) == exact
            tag = "checked"
        else:
            tag = "formula"
        duplex_bits = Fraction(2 * n, 2 * n)            # 4^n duplexes on 2n twists
        all_bits = math.log2(exact) / (2 * n)
        print(f"  {n}   {0:8d}   {0:9d}   {float(duplex_bits):6.3f}   {all_bits:6.3f}"
              f"  [{exact}, {tag}]")
    fw = fibonacci_word(20)
    comp = [factor_complexity(fw, n) for n in range(1, 11)]
    assert comp == [n + 1 for n in range(1, 11)]
    print("  Fibonacci word factor complexity p(n) = n+1 for n = 1..10: Sturmian, aperiodic,"
          " entropy 0.")
    print("  => aperiodicity alone is not a code; the duplex spends half the closure"
          " capacity on the copy.\n")


def sec4(max_n: int) -> None:
    print("sec 4  a single strand closes only under exact Chargaff-2 balance")
    print("  len   closing strands / all   fraction   1/(pi n)")
    for n in range(1, max_n + 1):
        m = 2 * n
        exact = math.comb(m, n) ** 2
        if m <= 10:
            brute = sum(1 for s in itertools.product("ATGC", repeat=m)
                        if s.count("A") == s.count("T") and s.count("G") == s.count("C"))
            assert brute == exact
        frac = exact / 4 ** m
        print(f"  {m:3d}   {exact:>10d} / {4 ** m:<10d}   {frac:.4f}     {1 / (math.pi * n):.4f}")
    print("  => exact single-strand balance is rare and falls as 1/n; genomes obey"
          " Chargaff-2 only approximately,\n     so a single strand is not a closure"
          " and the rule is not evidence for one.\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--max-n", type=int, default=7)
    args = ap.parse_args()
    sec1_2(args.max_n)
    sec3(args.max_n)
    sec4(args.max_n)
    print("All assertions passed.")


if __name__ == "__main__":
    main()
