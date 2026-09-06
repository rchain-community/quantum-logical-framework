#!/usr/bin/env python3
"""
alpha_residual_deep.py — settle the fractal / Zipf / self-similarity null of
`Alpha_Residual.md` §9b at converged depth.

§9b ran the 8-twist first-closure (prime) census by BRUTE enumeration, capped at
L = 10 (~5 min), and reported the self-similarity probes as **truncation-dominated**:

  "the octave self-similarity ratios are truncation-dominated (the deep excursion
   levels are still filling in at L = 10), and the Zipf rank–frequency slope of the
   prime multiplicities is ≈ −4.7, steepening with depth, not the −1 of a Zipfian law."

This reruns the identical census by an EXACT TRANSFER RECURSION (state
`(v,h,d,l,inv_parity,maxexc)`, no enumeration — the method of `intermittency_bridge.py`),
which reaches L ≈ 24 / R ≈ 12 in seconds, so the deep excursion levels are filled.
Question: does the null (scale-invariant, period-1 cascade — no log-periodic line that
could move the §2a weight `w` off 1/2) survive at converged depth, or was it an artifact?

Matches the repo exactly:
  * prime = count-balanced (all 4 conjugate-pair counts equal) with no proper even
    count-balanced prefix (absorbing / first closure).
  * max-excursion R = max prefix `|v|+|h|+|d|+|l|`  (qucalc_search.max_excursion).
  * phase = (−1)^{#neg} · (−1)^{axis-word inversions},  X<Y<Z  (census_inventory.predicted_phase);
    for a closure #neg = L/2, and inversion parity updates locally (Y flips by #Z parity,
    X by #Y+#Z parity, Z no flip).
  * Kraft cylinder weight 8^{−L}  (QLF_KraftMeasure).

Value-free: 137.036 / 0.036 / w never enter.

Run:  python3 alpha_residual_deep.py [--l-max 22] [--r-max 11]
"""
from __future__ import annotations

import argparse
import math
from collections import defaultdict

# X<Y<Z inversion bookkeeping, per census_inventory.AXIS_ORDER
_STEPS = [("^", 1, 0, 0, 0, "Y"), ("v", -1, 0, 0, 0, "Y"),
          (">", 0, 1, 0, 0, "X"), ("<", 0, -1, 0, 0, "X"),
          ("/", 0, 0, 1, 0, "Z"), ("\\", 0, 0, -1, 0, "Z"),
          ("+", 0, 0, 0, 1, "I"), ("-", 0, 0, 0, -1, "I")]


def first_closure_census(L_max: int, R_max: int):
    """clos[(R, L)] = [n_inv_even, n_inv_odd] for first-closures (absorbing) of
    length L, max-excursion R.  Exact; reproduces brute counts (cross-checked below)."""
    clos: dict[tuple[int, int], list[int]] = defaultdict(lambda: [0, 0])
    live: dict[tuple, int] = {(0, 0, 0, 0, 0, 0): 1}
    for L in range(1, L_max + 1):
        nxt: dict[tuple, int] = defaultdict(int)
        for (v, h, d, l, inv, mx), c in live.items():
            for _nm, dv, dh, dd, dl, ax in _STEPS:
                nv, nh, nd, nl = v + dv, h + dh, d + dd, l + dl
                e = abs(nv) + abs(nh) + abs(nd) + abs(nl)
                if e > R_max:
                    continue
                ninv = inv
                if ax == "Y":
                    ninv ^= d & 1
                elif ax == "X":
                    ninv ^= (v & 1) ^ (d & 1)
                nmx = mx if mx >= e else e
                if nv == 0 and nh == 0 and nd == 0 and nl == 0 and L >= 2:
                    clos[(nmx, L)][ninv] += c
                else:
                    nxt[(nv, nh, nd, nl, ninv, nmx)] += c
        live = nxt
        if not live:
            break
    return clos


# The published first-closure ("prime") counts from Alpha_Residual.md §9b, obtained
# there by brute enumeration (balanced_histories, L <= 10, ~5 min). The transfer
# recursion must reproduce these exactly.
PUBLISHED_PRIMES = {2: 8, 4: 104, 6: 2944, 8: 108136, 10: 4525888}


def lstsq(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intc = my - slope * mx
    return slope, intc


def periodogram_peak(resid):
    """Crude log-space periodogram: scan angular frequency, return (peak, rms, omega*)."""
    n = len(resid)
    if n < 4:
        return float("nan"), float("nan"), float("nan")
    rms = (sum(r * r for r in resid) / n) ** 0.5
    best = (0.0, 0.0)
    om = 0.3
    while om < math.pi:
        re = sum(r * math.cos(om * k) for k, r in enumerate(resid))
        im = sum(r * math.sin(om * k) for k, r in enumerate(resid))
        amp = (re * re + im * im) ** 0.5 * 2 / n
        if amp > best[0]:
            best = (amp, om)
        om += 0.02
    return best[0], rms, best[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--l-max", type=int, default=22)
    ap.add_argument("--r-max", type=int, default=11)
    args = ap.parse_args()
    L_max = args.l_max - (args.l_max % 2)
    R_max = args.r_max
    print(__doc__.split("Run:")[0])
    print("=" * 78)
    print(f"transfer recursion:  L_max = {L_max}, R_max = {R_max}\n")

    clos = first_closure_census(L_max, R_max)

    # ---- prime counts by length (extend 8,104,2944,108136,4525888 ...) --------
    by_L = defaultdict(int)
    for (R, L), (ce, co) in clos.items():
        by_L[L] += ce + co
    print("prime (first-closure) counts by length")
    prev = None
    for L in sorted(by_L):
        r = f"   ratio to L−2: {by_L[L] / prev:.4f}" if prev else ""
        # counts fully converged only when R_max >= L//2
        conv = "" if R_max >= L // 2 else "   (R-capped: undercount)"
        print(f"  L={L:>2}:  {by_L[L]:>16,}{r}{conv}")
        prev = by_L[L]

    ok = all(by_L.get(L) == n for L, n in PUBLISHED_PRIMES.items() if R_max >= L // 2)
    mism = {L: (by_L.get(L), n) for L, n in PUBLISHED_PRIMES.items()
            if R_max >= L // 2 and by_L.get(L) != n}
    print(f"\n  cross-check vs §9b brute counts (L ≤ 10): "
          f"{'MATCH' if ok else 'MISMATCH ' + str(mism)}")

    # ---- census by excursion level R (summed over all L) ---------------------
    cnt_by_R = defaultdict(int)
    mass_by_R = defaultdict(float)
    signed_by_R = defaultdict(float)
    for (R, L), (ce, co) in clos.items():
        base = 1 if (L // 2) % 2 == 0 else -1
        npl, nmi = (ce, co) if base == 1 else (co, ce)
        cnt_by_R[R] += ce + co
        mass_by_R[R] += (ce + co) * 8.0 ** -L
        signed_by_R[R] += (npl - nmi) * 8.0 ** -L
    Rs = sorted(cnt_by_R)

    print("\noctave (excursion) census — counts, Kraft mass, self-similarity ratios")
    print(f"  {'R':>3} {'prime count':>18} {'Kraft mass':>14} {'signed mass':>14}"
          f" {'cnt ratio':>10} {'mass ratio':>10}")
    for i, R in enumerate(Rs):
        cr = mr = float("nan")
        if i:
            cr = cnt_by_R[R] / cnt_by_R[Rs[i - 1]]
            mr = mass_by_R[R] / mass_by_R[Rs[i - 1]]
        print(f"  {R:>3} {cnt_by_R[R]:>18,} {mass_by_R[R]:>14.3e} {signed_by_R[R]:>14.3e}"
              f" {cr:>10.4f} {mr:>10.4f}")

    # deep-tail behaviour of the two ratio sequences
    cnt_ratios = [cnt_by_R[Rs[i]] / cnt_by_R[Rs[i - 1]] for i in range(1, len(Rs))]
    mass_ratios = [mass_by_R[Rs[i]] / mass_by_R[Rs[i - 1]] for i in range(1, len(Rs))]
    tail = slice(len(Rs) // 2, None)
    def describe(name, seq):
        t = seq[tail]
        if len(t) < 3:
            print(f"  {name}: too short"); return
        spread = max(t) - min(t)
        # monotone?
        mono = all(t[k] <= t[k - 1] + 1e-9 for k in range(1, len(t))) or \
               all(t[k] >= t[k - 1] - 1e-9 for k in range(1, len(t)))
        # oscillating around mean?
        mean = sum(t) / len(t)
        signs = [1 if x > mean else -1 for x in t]
        flips = sum(1 for k in range(1, len(signs)) if signs[k] != signs[k - 1])
        print(f"  {name} tail {[round(x,4) for x in t]}")
        print(f"     spread={spread:.4f}  {'MONOTONE (converging / Stirling)' if mono else ''}"
              f"  sign-flips about mean = {flips}/{len(t)-1}"
              f"  {'-> OSCILLATING (log-periodic candidate)' if flips >= len(t)-2 and not mono else ''}")
    describe("count-ratio", cnt_ratios)
    describe("mass-ratio ", mass_ratios)

    # ---- Zipf slope, and its drift with the depth cutoff --------------------
    print("\nZipf rank–frequency slope of prime multiplicities per (L,R) cell")
    for cut in sorted({8, 12, 16, L_max}):
        if cut > L_max:
            continue
        cells = sorted((ce + co for (R, L), (ce, co) in clos.items()
                        if L <= cut and ce + co > 0), reverse=True)
        if len(cells) < 3:
            continue
        xs = [math.log(k + 1) for k in range(len(cells))]
        ys = [math.log(c) for c in cells]
        s, _ = lstsq(xs, ys)
        print(f"  L ≤ {cut:>2}:  slope = {s:>7.3f}   ({len(cells)} cells)"
              f"   {'≈ −1 Zipfian' if abs(s + 1) < 0.3 else 'not Zipfian'}")
    print("  (if the slope keeps steepening as L↑ and never approaches −1, the census is")
    print("   not Zipfian — §9b's reading, tested here for drift, not just one cutoff)")

    # ---- log-periodic / DSI probe (genesis.py style) -----------------------
    print("\nlog-periodic (discrete-scale-invariance) probe — genesis.py style")
    xs = [float(R) for R in Rs if mass_by_R[R] > 0]
    ys = [math.log(mass_by_R[R]) for R in Rs if mass_by_R[R] > 0]
    s, c = lstsq(xs, ys)
    resid = [y - (s * x + c) for x, y in zip(xs, ys)]
    peak, rms, om = periodogram_peak(resid)
    print(f"  log(mass_by_R) vs R:  slope = {s:.4f}  (pure power law => flat residual)")
    print(f"  residuals: {[round(r,4) for r in resid]}")
    print(f"  periodogram  peak = {peak:.3e}   rms = {rms:.3e}   peak/rms = {peak/rms:.2f}"
          f"   omega* = {om:.2f}  (period {2*math.pi/om:.2f} octaves)")
    print(f"  genesis.py criterion: a real log-periodic line needs peak/rms >> 1 AND a")
    print(f"  monotone-free residual.  peak/rms ≈ O(1) => Stirling correction, NOT DSI.")

    # ---- ExactRG recursion at this depth ---------------------------------
    Z = amp = 0.0
    for R in Rs:
        Z += mass_by_R[R]
        amp += signed_by_R[R]
    print(f"\nQLF_ExactRG recursion at L≤{L_max}:  Z_limit = {Z:.6f} (<1: {Z < 1})   "
          f"amp_limit = {amp:.6f}")
    print(f"  (§9b at L=10 reported Z_limit ≈ 0.172, amp_limit ≈ −0.114)")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("  Compare the deep count/mass ratio tails and periodogram peak/rms against")
    print("  §9b.  A stabilising ratio + peak/rms ≈ O(1) + steepening (non-Zipfian) slope")
    print("  = the null is REAL, not truncation: scale-invariant period-1 cascade, no")
    print("  log-periodic line, w stays structurally 1/2.  An oscillating ratio or a")
    print("  dominant periodogram peak that PERSISTS with depth would reopen the channel.")


if __name__ == "__main__":
    main()
