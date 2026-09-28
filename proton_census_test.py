#!/usr/bin/env python3
"""
proton_census_test.py -- does the alpha rule transfer to the proton? A pre-registered cross-test.

THE QUESTION (Jim, 2026-09-28, "all three"): (a) give m_p/m_e a finite census structure; (b) find why the
alpha sectors would combine with weight 1/2; (c) test the result with no new parameter.

Alpha_Residual.md sec 9n: the measured alpha lies almost exactly halfway between ARBITRARY listening (every
language: the mode, 137.032002) and GROWN listening (the golden sector, 137.039938) -- a grown share of
g = 0.504. Taking g = 1/2 now would be post-hoc: the number is already known. It becomes evidence only if
its reason predicts something else.

  sec 0  PRE-REGISTRATION -- the candidate reason for 1/2, the construction, and the predictions.
  sec 1  census pi, by sector: the integrated closure probability of the one-axis walk.
  sec 2  alpha under the rule (known, post-hoc: recorded, not counted as evidence).
  sec 3  the proton under the same rule, no new parameter -- the test.
  sec 4  verdict and scope.

Run:  python3 proton_census_test.py
"""
from __future__ import annotations

import math
from decimal import Decimal, getcontext

getcontext().prec = 60

PREREGISTRATION = """
PRE-REGISTRATION (fixed in the commit that adds this file, before it was run; pi by sector had not
been computed when this was written).

  THE CANDIDATE REASON FOR 1/2 -- KET/BRA BALANCE (stated as post-hoc: it was sought after g = 0.504 was
  known). Every ZFA closure has exactly as many generating (ket, action) steps as closing (bra, lift)
  steps -- that balance IS the axiom (bra_ket_always_balanced). Suppose the ket half hears GROWN languages
  (generation is substitution, sec 10 of ZFA_DNA.md) and the bra half hears EVERY language (closure is
  counted, the census). Then the two listenings enter with equal weight, g = 1/2, for every closure -- so
  the rule is universal, not alpha-specific, and must hold for any census-built constant.

  THE CONSTRUCTION FOR THE PROTON. m_p/m_e = 6 pi^5 (QLF_LenzMassRatio). The census makes pi as the
  integrated closure probability of the unbiased one-axis walk:
        pi/2 = integral_0^1 sum_n P_close(2n) x^(2n) dx = sum_n C(2n,n) / (4^n (2n+1))   (the arcsin series)
  -- the TOTAL sector gives pi exactly. Replace C(2n,n) by the sector counts of sec 9m (irreducible
  2.Catalan(n-1), golden Catalan(n+1), all sharing the empty closure at n = 0) to get pi_irr, pi_gold.
  The rule, as for alpha: pi_rule = 1/2 . (pi_irr + pi_tot)/2 + 1/2 . pi_gold, and
  m_p/m_e (rule) = 6 pi_rule^5.

  PREDICTION. The rule does NOT transfer: |m_p/m_e(rule) / 1836.15267343 - 1| > 1e-3, i.e. it is far
  worse than 6 pi^5's own 1.9e-5. Reason, stated first: at the walk's natural coupling 4^-n the sectors
  differ at order one (nothing like alpha's 1/128 suppression), so any fixed mix moves pi a lot.
  If the prediction FAILS (the rule lands within 1e-3), record it: that would be evidence for the ket/bra
  reason. If it holds, the universal-1/2 reason is falsified in this naive form.
"""

MP_ME = Decimal("1836.15267343")     # CODATA 2018/2022 proton-electron mass ratio


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


def catalan(m: int) -> int:
    return math.comb(2 * m, m) // (m + 1)


def sector_pi(count, terms: int = 200_000) -> Decimal:
    """2 x sum_n count(n) / (4^n (2n+1)), n = 0 is the empty closure (count 1 in every sector).
    Terms decay only like n^-2 (total) or n^-3/2 x 1/n (Catalan sectors), so the sum is taken far out
    and the tail is estimated from the terms' asymptotic form."""
    s = Decimal(1)
    ratio = Decimal(1)                       # running C(2n,n)/4^n, exact enough in Decimal
    for n in range(1, terms + 1):
        ratio = ratio * (2 * n - 1) / (2 * n)
        s += Decimal(count(n, ratio)) / (2 * n + 1)
    return 2 * s


def c_total(n, r):  return r                                  # C(2n,n)/4^n
def c_irr(n, r):    return r / (2 * n - 1)                              # 2.Cat(n-1)/4^n
def c_gold(n, r):   return r * 2 * (2 * n + 1) / ((n + 1) * (n + 2))    # Cat(n+1)/4^n


def sec1():
    rule("sec 1  CENSUS PI, BY SECTOR")
    # exact checks of the per-term ratios against integers at small n
    for n in range(1, 12):
        r = Decimal(math.comb(2 * n, n)) / Decimal(4) ** n
        assert abs(c_irr(n, r) - Decimal(2 * catalan(n - 1)) / Decimal(4) ** n) < Decimal("1e-50")
        assert abs(c_gold(n, r) - Decimal(catalan(n + 1)) / Decimal(4) ** n) < Decimal("1e-50")
    N = 200_000
    p_tot, p_irr, p_gold = sector_pi(c_total, N), sector_pi(c_irr, N), sector_pi(c_gold, N)
    # tails beyond N (times the leading 2): total term ~ 1/(2 sqrt(pi) n^1.5) -> 2/(sqrt(pi) sqrt N);
    # irreducible term ~ 1/(4 sqrt(pi) n^2.5); golden term ~ 2/(sqrt(pi) n^2.5); sum n^-2.5 ~ (2/3) N^-1.5
    sp = Decimal(math.pi).sqrt()
    NN = Decimal(N)
    t_tot = 2 / (sp * NN.sqrt())
    t_irr = 2 * (1 / (4 * sp)) * Decimal(2) / (3 * NN * NN.sqrt())
    t_gold = 2 * (2 / sp) * Decimal(2) / (3 * NN * NN.sqrt())
    p_tot, p_irr, p_gold = p_tot + t_tot, p_irr + t_irr, p_gold + t_gold
    print(f"""
  pi from the TOTAL sector        {p_tot:.10f}    (pi = {math.pi:.10f}; the arcsin series, exact in the limit)
  pi from the IRREDUCIBLE sector  {p_irr:.10f}
  pi from the GOLDEN sector       {p_gold:.10f}
  (sums to n = {N:,} plus the asymptotic tail; accurate to ~1e-9, ample for a 1e-3 test)""")
    assert abs(float(p_tot) - math.pi) < 1e-7
    return p_tot, p_irr, p_gold


def sec2():
    rule("sec 2  ALPHA UNDER THE RULE (POST-HOC, RECORDED -- NOT EVIDENCE)")
    s62 = Decimal(62).sqrt()
    irr, tot, gold = 126 - 16 * s62, 512 * s62 / 31 - 130, 1032062 - 131072 * s62
    a = 137 + (irr + tot) / 4 + gold / 2
    print(f"""
  alpha^-1 (rule) = 137 + 1/2 (irr + tot)/2 + 1/2 gold = {a:.9f}   measured 137.035999177
  off {a - Decimal('137.035999177'):+.2e} -- known before the rule was stated, so it cannot support it.""")


def sec3(p_tot, p_irr, p_gold):
    rule("sec 3  THE PROTON UNDER THE SAME RULE -- THE TEST")
    p_rule = (p_irr + p_tot) / 4 + p_gold / 2
    m_rule = 6 * p_rule ** 5
    m_pi = 6 * Decimal(math.pi) ** 5
    rel_rule = m_rule / MP_ME - 1
    rel_pi = m_pi / MP_ME - 1
    held = abs(rel_rule) > Decimal("1e-3")
    print(f"""
  pi (rule)                    {p_rule:.10f}
  m_p/m_e = 6 pi^5             {m_pi:.6f}     off {rel_pi:+.2e}  (the existing result)
  m_p/m_e = 6 pi(rule)^5       {m_rule:.6f}     off {rel_rule:+.2e}
  measured                     {MP_ME}

  PREDICTION (the rule does not transfer, |off| > 1e-3):  {'HELD' if held else 'FAILED -- record it'}""")
    return held


def verdict(held: bool):
    rule("sec 4  VERDICT AND SCOPE")
    if held:
        print("""
  The universal-1/2 reason, in its naive form, is FALSIFIED by the proton: applied with no new parameter,
  the same arbitrary/grown mix that sits near alpha moves 6 pi^5 far off the measured ratio. So either the
  1/2 near alpha is specific to alpha's weak (1/128) coupling, or the ket/bra reason is wrong, or the
  census-pi construction is not the proton's. Each is a live option; none is chosen here.

  What stands: the existing 6 pi^5 (total-sector pi) remains the proton result, and the alpha observation
  g = 0.504 remains a lead without an independent reason.""")
    else:
        print("""
  The prediction FAILED: the rule lands within 1e-3 on the proton too. That is evidence for a universal
  1/2 (ket/bra balance) -- to be scrutinised before it is trusted (the construction of census-pi by
  sector was chosen in advance, but it is one construction).""")
    print("""
  Scope: one construction, fixed in advance; no fitting; no axiom added. The proton's pi^5 is a 5-angle
  integral (Proton_Resonance_R_e.md); using census-pi for each angle is itself an assumption, stated.""")


def main():
    print(__doc__)
    rule("sec 0  PRE-REGISTRATION")
    print(PREREGISTRATION)
    p = sec1()
    sec2()
    held = sec3(*p)
    verdict(held)


if __name__ == "__main__":
    main()
