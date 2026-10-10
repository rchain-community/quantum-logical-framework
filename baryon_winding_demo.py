"""
baryon_winding_demo.py
======================

Companion to lean/QLF_BaryonWinding.lean. Baryon number in QLF is a **signed
3-axis linking (winding) number** — not a weight dictionary (B−L was proved not to
be one; QLF_BMinusL). Slide a 3-window along a twist history; add +1 for a window
spanning all three axes (x=</>, y=^/v, z=//\\) in cyclic (x,y,z) order, −1 for
anticyclic, 0 otherwise (gauge twists +/- carry no axis).

This script exhaustively verifies the two general properties the Lean module
relies on / targets:
  * dagger-oddness  B(†ts) = −B(ts)   (antiparticle = Hermitian conj = reverse∘conj)
    => baryon and antibaryon carry ±B.   [exhaustive, all strings len ≤ 5]
  * no-z (lepton/EM sector) => B = 0.    [exhaustive, all strings len ≤ 6]
and shows the calibration the Lean theorems pin down (proton +1, antiproton −1,
leptons 0, meson 0). Pure Python.

Baryon number proper is the winding read on the JUNCTION (the word with its gauge
twists +/- removed; Lean `junctionBaryon`). The windowed B is not gauge-invariant —
one `+` inside the proton word >^/ takes it from 1 to 0 — so the junction checks
below verify, exhaustively on gauge-dressed words, what the Lean theorems state:
  * inserting a gauge twist anywhere never changes Bj      (junction_insert_gauge)
  * Bj(†ts) = −Bj(ts)                                      (junctionBaryon_antiparticle)
  * Bj = B on words with no gauge twist                    (junctionBaryon_eq_of_noGauge)
"""
import itertools

AX = {'^': 'y', 'v': 'y', '>': 'x', '<': 'x', '/': 'z', '\\': 'z', '+': None, '-': None}
CONJ = {'^': 'v', 'v': '^', '<': '>', '>': '<', '/': '\\', '\\': '/', '+': '-', '-': '+'}
CYC = {('x', 'y', 'z'), ('y', 'z', 'x'), ('z', 'x', 'y')}
ANTI = {('x', 'z', 'y'), ('z', 'y', 'x'), ('y', 'x', 'z')}


def sign(a, b, c):
    t = (a, b, c)
    return 1 if t in CYC else (-1 if t in ANTI else 0)


def B(s):
    a = [AX[c] for c in s]
    return sum(sign(a[k], a[k + 1], a[k + 2]) for k in range(len(a) - 2))


def Bj(s):
    """Baryon number: the winding read on the junction (gauge twists removed)."""
    return B(''.join(c for c in s if AX[c] is not None))


def dagger(s):
    return ''.join(CONJ[c] for c in reversed(s))


def header(t):
    print("=" * 72); print("  " + t); print("=" * 72)


def main():
    header("Baryon number B = signed 3-axis linking (winding)")
    print()
    proton = ">^/"
    cases = [("electron ^<v>", "^<v>"), ("neutrino ^v", "^v"), ("photon ^>", "^>"),
             ("muon ^<v>^<v>", "^<v>^<v>"),
             ("proton (Borromean) >^/", proton),
             ("antiproton †(>^/)", dagger(proton)),
             ("meson q q-bar >^/\\v<", proton + dagger(proton))]
    print(f"  {'state':24}{'twists':12}{'B':>4}{'B(dagger)':>11}")
    for n, s in cases:
        print(f"  {n:24}{s:12}{B(s):>+4}{B(dagger(s)):>+11}")

    print()
    header("General properties (exhaustive)")
    print()
    alph = '^v<>/\\+-'
    dag_ok = all(B(dagger(''.join(s))) == -B(''.join(s))
                 for L in range(6) for s in itertools.product(alph, repeat=L))
    print(f"  dagger-odd  B(†ts) = −B(ts)   for ALL strings len ≤ 5 : {dag_ok}")
    noz_ok = all(B(''.join(s)) == 0
                 for L in range(7) for s in itertools.product('^v<>+-', repeat=L))
    print(f"  no-z (lepton/EM) ⟹ B = 0      for ALL such len ≤ 6   : {noz_ok}")
    print()
    print("  => B is conjugation-odd (baryon/antibaryon = ±B) and vanishes on the")
    print("     lepton/EM sector — the baryon-number profile. Lean: QLF_BaryonWinding.")

    print()
    header("Baryon number on the junction (gauge-dressed words, exhaustive)")
    print()
    for n, s in [("proton uud >^/+", ">^/+"), ("neutron udd >^+/+", ">^+/+"),
                 ("antiproton †(>^/+)", dagger(">^/+"))]:
        print(f"  {n:24}windowed B = {B(s):+d}   junction Bj = {Bj(s):+d}")
    words = [''.join(s) for L in range(6) for s in itertools.product(alph, repeat=L)]
    ins_ok = all(Bj(w[:i] + g + w[i:]) == Bj(w)
                 for w in words if len(w) <= 4 for i in range(len(w) + 1) for g in '+-')
    win_breaks = sum(1 for w in words if len(w) <= 4 for i in range(len(w) + 1)
                     for g in '+-' if B(w[:i] + g + w[i:]) != B(w))
    dagj_ok = all(Bj(dagger(w)) == -Bj(w) for w in words)
    agree_ok = all(Bj(w) == B(w) for w in words if '+' not in w and '-' not in w)
    print()
    print(f"  gauge insertion never changes Bj   (all words len ≤ 4, every slot) : {ins_ok}")
    print(f"  ... while it changes windowed B in {win_breaks} of those insertions")
    print(f"  Bj(†ts) = −Bj(ts)                  (all words len ≤ 5)            : {dagj_ok}")
    print(f"  Bj = B on gauge-free words         (all such len ≤ 5)             : {agree_ok}")
    assert ins_ok and dagj_ok and agree_ok and win_breaks > 0


if __name__ == "__main__":
    main()
