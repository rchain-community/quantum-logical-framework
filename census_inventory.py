#!/usr/bin/env python3
"""
census_inventory.py — build and verify the census inventory database.

The inventory is what we actually discover when we enumerate: **counts** (how many
ways close, graded by length and depth), **listenings** (how many of those ways a
given capacity can actually receive), and **QuCalc folds** (the Pauli phase each
way carries).

A *listening* is not a synonym for a count — it is the capacity-relative one, and
the distinction is a theorem rather than a metaphor. A count is absolute: how many
ways exist. A listening is what a horizon of capacity `R` can close, and by
`QLF_ClosureDepthLaw.closedAtHorizon_iff_maxExcursion_le` that is exactly the ways
whose phase walk never strays further than `R` from balance:

    count(2n)        = |{ balanced histories of length 2n }|          = C(2n, n)
    listening(2n, R) = |{ those with maxExcursion <= R }|             <= count(2n)

So the same census sounds different to different capacities — a shallow observer
hears only the shallow closures, a deeper one hears more (`lines_mono`), and no
finite capacity hears everything (`law_of_exceptions`). Both have turned up repeatedly in this program — the log-2 quantum,
the depth law, the Born-weight work — and each time they were recomputed from
scratch. This script keeps them in one place, in `data/census_inventory.json`.

It is a **checker**, not just a store. Every invariant we have proven in Lean is
asserted here against freshly enumerated data, so a change to `twist_core.py` that
breaks one shows up immediately:

  * count balance ⟹ Pauli closure        (QLF_TwistAlphabet.count_balanced_pauli_closed)
  * count balance ⟹ the fold is ±I       (QLF_BalancedPhaseReal.balanced_phase_is_real)
  * unbalanced histories DO reach ±iI     (QLF_BalancedPhaseReal.unbalanced_can_be_imaginary)
  * closure depth = max phase excursion   (QLF_ClosureDepthLaw.closedAtHorizon_iff_maxExcursion_le)
  * one-pass closures number 2^n          (QLF_ClosureDepth.onePass_ways_iff)
  * the deepest stratum holds exactly 2   (QLF_ClosureMultiplicity.W_self)
  * the second stratum is 2*3^(n-1) - 2^n  (QLF_ClosureMultiplicity.W_two)
  * depth 1 is never modal for n >= 3     (QLF_ClosureMultiplicity.depth_one_not_modal)
  * phase = (-1)^(#neg) x sign(axis perm)  (QLF_PhaseRule.phase_rule)
  * first closures are prefix-free, so sum W/8^d <= 1  (QLF_KraftMeasure.twist_kraft)
  * the normalized-event weight stays under that mass  (QLF_KraftMeasure.normalized_event_mass_le_one)

The last two belong to the **closure layer**, which is new here and is the one contextual
section of an otherwise universal file. The generic census above is substrate data — it knows
nothing about any experiment. A preparation-and-apparatus is an experiment, and there are
indefinitely many, so what is stored is only the reusable part: for a small fixed set of
canonical geometries, the first-closure event classes with the pair

    (W, A)   how many ways close as that outcome first at that depth, and their signed total

from which every derived quantity follows without re-enumerating — the **multiplicity mass**
`sum W/8^d`, the **normalized-event weight** `sum A^2/(W.8^d)` = mass times squared mean phase,
and the split each induces. Those two splits are not two guesses; they **bracket every possible
notion of "same event"**, since refining an event quotient raises the weight by Cauchy-Schwarz
(`QLF_KraftMeasure.merge_le_sum`) and the finest quotient is exactly the multiplicity mass.
That same inequality is why the normalized weight cannot be the Born rule: merging two paths
into one event can only *lower* it, so constructive interference is unavailable — measured in
`contextual_census.py --two-path`, and proven in `QLF_KraftMeasure.no_constructive_interference`.

That last one used to live in the verified-not-proven list below; it is now a
theorem for every balanced history at every length (and, without the balance
hypothesis, QLF_PhaseRule.twist_fold_phase_normal_form), so the enumeration here
is its discovery record and a regression check rather than its warrant.

and one finding that is verified-not-proven, recorded so it stays honest:

  * which depth-stratum counts are Gaussian norms (they mostly are not — see
    born_generator_check.py; counts are not weights)

It **accumulates**. Each run keeps everything already discovered and computes only
what is missing, so the database can be fleshed out over time by pushing one length
deeper as compute allows:

    python3 census_inventory.py                      # fill in anything missing, verify all
    python3 census_inventory.py --twist-len 8        # push the fold census one step deeper
    python3 census_inventory.py --phase-len 20       # push the depth census deeper
    python3 census_inventory.py --verify             # recheck stored entries, write nothing
    python3 census_inventory.py --quick              # CI gate: fast subset, seconds not minutes
    python3 census_inventory.py --rebuild            # discard and recompute from scratch

`--quick` is what CI runs. It re-enumerates only the small lengths (fold <= 6,
depth <= 12, a few seconds), compares them against what is stored, and asserts every
invariant over the *whole* stored file. So a regression in `twist_core.py` is caught
by the recomputation, and a corrupted or hand-edited database by the assertions,
without paying for the deep lengths on every push.

Cost, measured rather than guessed (~48,000 histories/sec on one core, and the
script prints the count and a progress line before spending it):

    fold census   length  8         190,120 histories     seconds
                  length 10       7,939,008 histories     ~3 minutes
                  length 12     357,713,664 histories     ~2 hours
                  length 14  16,993,726,464 histories     ~4 days  — sample instead
    depth census  length 20       1,048,576 to sift       ~1 minute
                  length 24      16,777,216 to sift       the practical ceiling

Currently stored: fold census to 10, depth census to 20. Anything past those is a
deliberate decision, not something a plain run will wander into — a plain run
recomputes nothing that is already stored.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from fractions import Fraction
from itertools import product
from math import comb

from twist_core import pauli_fold

# Resolve relative to this file, not the working directory: running from elsewhere
# used to silently miss the stored database and rebuild everything from scratch.
_HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_HERE, "data", "census_inventory.json")

TWISTS = ['^', 'v', '>', '<', '/', '\\', '+', '-']
CONJ_PAIRS = [('^', 'v'), ('>', '<'), ('/', '\\'), ('+', '-')]
NEG_TWISTS = {'v', '<', '\\', '-'}
AXIS = {'^': 'Y', 'v': 'Y', '>': 'X', '<': 'X', '/': 'Z', '\\': 'Z', '+': 'I', '-': 'I'}
AXIS_ORDER = {'X': 0, 'Y': 1, 'Z': 2}

# Defaults for a first build; later runs keep whatever is already stored and only
# extend it (pass --twist-len / --phase-len to push deeper).
DEFAULT_TWIST_LEN = 6
DEFAULT_PHASE_LEN = 16


# --------------------------------------------------------------------------- #
# the QuCalc fold: which mu4 phase a way carries
# --------------------------------------------------------------------------- #
def fold_phase(history: str):
    """Return the scalar phase of the Pauli fold, or None if it is not a scalar."""
    a, b, c, d = pauli_fold(history)
    if abs(b) > 1e-9 or abs(c) > 1e-9 or abs(a - d) > 1e-9:
        return None
    for p, name in ((1, "+1"), (-1, "-1"), (1j, "+i"), (-1j, "-i")):
        if abs(a - p) < 1e-9:
            return name
    return None


def is_count_balanced(history: str) -> bool:
    return all(history.count(x) == history.count(y) for x, y in CONJ_PAIRS)


def predicted_phase(history: str) -> str:
    """The empirical two-factor rule: sign content x permutation sign."""
    sign = (-1) ** sum(1 for ch in history if ch in NEG_TWISTS)
    axes = [AXIS[ch] for ch in history if AXIS[ch] != 'I']
    inversions = sum(
        1
        for i in range(len(axes))
        for j in range(i + 1, len(axes))
        if axes[i] != axes[j] and AXIS_ORDER[axes[i]] > AXIS_ORDER[axes[j]]
    )
    sign *= (-1) ** inversions
    return "+1" if sign == 1 else "-1"


# --------------------------------------------------------------------------- #
# the phase census: closure depth (TopoString +/- alphabet)
# --------------------------------------------------------------------------- #
def zeno_prune(s):
    out, i, n = [], 0, len(s)
    while i < n:
        if i + 1 < n and s[i] == -s[i + 1]:
            i += 2
        else:
            out.append(s[i]); i += 1
    return out


def closure_depth(s) -> int:
    depth = 0
    while s:
        s = zeno_prune(s); depth += 1
    return depth


def max_excursion(s) -> int:
    m = c = 0
    for x in s:
        c += x
        m = max(m, abs(c))
    return m


def is_gaussian_norm(n: int) -> bool:
    """n is a Z[i] norm iff every prime = 3 (mod 4) occurs to an even power."""
    if n < 0:
        return False
    if n == 0:
        return True
    m, p = n, 2
    while p * p <= m:
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p; e += 1
            if p % 4 == 3 and e % 2 == 1:
                return False
        p += 1
    return m % 4 != 3


# --------------------------------------------------------------------------- #
# enumeration
# --------------------------------------------------------------------------- #
def balanced_history_count(length: int) -> int:
    """How many count-balanced histories a length has — exactly, without enumerating."""
    from math import factorial
    half, total = length // 2, 0
    for a in range(half + 1):
        for b in range(half + 1 - a):
            for c in range(half + 1 - a - b):
                d = half - a - b - c
                total += factorial(length) // (
                    factorial(a) ** 2 * factorial(b) ** 2 * factorial(c) ** 2 * factorial(d) ** 2)
    return total


def balanced_histories(length: int):
    """Generate every count-balanced history of the given length, directly.

    Filtering 8^L is hopeless past length 6; generating the multiset permutations of
    each balanced letter-multiset is ~90x cheaper at length 8 and ~135x at length 10
    (190,120 and 7,939,008 histories respectively).
    """
    half = length // 2
    letters = [c for pair in CONJ_PAIRS for c in pair]

    def perms(counts, prefix):
        if len(prefix) == length:
            yield ''.join(prefix)
            return
        for ch in letters:
            if counts[ch]:
                counts[ch] -= 1
                prefix.append(ch)
                yield from perms(counts, prefix)
                prefix.pop()
                counts[ch] += 1

    for a in range(half + 1):
        for b in range(half + 1 - a):
            for c in range(half + 1 - a - b):
                d = half - a - b - c
                counts = {}
                for (x, y), k in zip(CONJ_PAIRS, (a, b, c, d)):
                    counts[x] = k
                    counts[y] = k
                yield from perms(counts, [])


# --------------------------------------------------------------------------- #
# indexed factors: what changes when twists carry a subsystem label
# --------------------------------------------------------------------------- #
# QuCalc does not need new primitive twists for many-body systems -- it needs INDEXED
# copies of the same eight, `(factor, twist)`, so that an operation on factor 1 and one
# on factor 2 are independent uses of the same alphabet. The physics that indexing
# changes is not the alphabet but the ALGEBRA: independent factors act as sigma (x) I and
# I (x) sigma, which COMMUTE, where a flat concatenation puts both in one Pauli algebra
# where distinct axes anticommute.
#
# The consequence that matters is about closure, not phase. A Kronecker product is a
# scalar exactly when each factor is, so in the indexed (product) model a joint closure
# requires EACH factor to close on its own. In the flat model a factor may be left open
# and balanced by the other -- which is precisely SharedClosure, QLF's entanglement.
#
# So the two models are not competitors and neither is a correction of the other; they
# are two sectors, and the split is what this section counts:
#
#   product sector  -- both factors close alone: independent subsystems, tensor-valid
#   coupled sector  -- neither closes alone but the pair does: entanglement, flat-only
#
# The gauge pair `('+','-')` survives into the product sector; the axis pair `('^','v')`
# -- the primordial entanglement witness of ER_EPR_QLF -- does not. Indexing therefore
# cannot simply replace concatenation: an interaction that binds two factors is a genuine
# Pauli STRING (sigma (x) sigma), not a product of single-factor operators.


MU4 = {"+1": 1, "-1": -1, "+i": 1j, "-i": -1j}


def axis_multiset_parities(history: str) -> tuple[int, int, int]:
    """Parities of the X, Y and Z letter multiplicities."""
    return tuple(sum(1 for ch in history if AXIS[ch] == k) % 2 for k in "XYZ")


def folds_to_scalar(history: str) -> bool:
    """Does this history fold to a Pauli scalar on its own?

    `axisProd = I` in QLF_TwistAlphabet's `(ZMod 2)^2` embedding (`Z = X + Y`), which is
    all three axis multiplicities sharing a parity -- weaker than count balance, and
    weaker than each multiplicity being even.
    """
    a, b, c = axis_multiset_parities(history)
    return a == b == c


def build_factor_inventory(max_len: int, keep: dict | None = None) -> dict:
    """Split every balanced history at every cut point and classify the two factors.

    Each cut of a balanced history is one way of reading it as two indexed subsystems, so
    this reuses the same enumeration as the fold census and costs no more.
    """
    out = dict(keep or {})
    phase_factorization_violations = list((keep or {}).get("_violations", []))
    for L in range(2, max_len + 1, 2):
        if str(L) in out:
            continue
        product_sector = coupled_sector = independent = 0
        witnesses = {"product": [], "coupled": []}
        for h in balanced_histories(L):
            for i in range(1, L):
                a, b = h[:i], h[i:]
                a_closes, b_closes = is_count_balanced(a), is_count_balanced(b)
                if a_closes and b_closes:
                    independent += 1                      # two separate closures, not one event
                    continue
                if folds_to_scalar(a) and folds_to_scalar(b):
                    product_sector += 1
                    if len(witnesses["product"]) < 6:
                        witnesses["product"].append([a, b])
                else:
                    coupled_sector += 1
                    if len(witnesses["coupled"]) < 6:
                        witnesses["coupled"].append([a, b])
                # The phase must factorize wherever both factors fold to scalars -- but in
                # `mu_4`, not `mu_2`. An open factor is not count-balanced, so
                # `balanced_phase_is_real` does not apply to it and its scalar may be
                # `+-i`; `predicted_phase` cannot represent that, and using it here was an
                # error the checker caught. The `mu_2` rule is for closures; a FACTOR of a
                # closure needs the full group.
                if folds_to_scalar(a) and folds_to_scalar(b):
                    pa, pb, pj = fold_phase(a), fold_phase(b), fold_phase(h)
                    if None in (pa, pb, pj) or MU4[pj] != MU4[pa] * MU4[pb]:
                        phase_factorization_violations.append([a, b])
        shared = product_sector + coupled_sector
        out[str(L)] = {
            "independent_pairs": independent,
            "shared_closures": shared,
            "product_sector": product_sector,
            "coupled_sector": coupled_sector,
            "coupled_fraction": round(coupled_sector / shared, 6) if shared else None,
            "witnesses": witnesses,
        }
    out["_violations"] = phase_factorization_violations
    return out


# keep the full history lists only while they are small; beyond this store aggregates
FULL_LISTING_MAX_LEN = 6


# --------------------------------------------------------------------------- #
# build
# --------------------------------------------------------------------------- #
def build_fold_inventory(max_len: int, keep: dict | None = None) -> dict:
    """Exhaustive twist histories: folds, grouped by phase, plus the rule check.

    Lengths already present in `keep` are reused rather than recomputed."""
    out = dict((keep or {}).get("by_length", {}))
    rule_violations = list((keep or {}).get("phase_rule_violations", []))
    unbalanced_imaginary = list((keep or {}).get("unbalanced_imaginary_witnesses", []))
    prior_len3 = (keep or {}).get("unbalanced_imaginary_count_len3", 0)
    for L in range(2, max_len + 1, 2):
        if str(L) in out:
            continue
        expected = balanced_history_count(L)
        print(f"   computing fold census at length {L}: {expected:,} balanced histories"
              f"{' — this takes a while' if expected > 1_000_000 else ''}...", flush=True)
        done = 0
        tally = {"+1": 0, "-1": 0, "+i": 0, "-i": 0}
        samples = {"+1": [], "-1": [], "+i": [], "-i": []}
        for h in balanced_histories(L):
            done += 1
            if expected > 1_000_000 and done % 500_000 == 0:
                print(f"      {done:,} / {expected:,} ({100*done/expected:.0f}%)", flush=True)
            p = fold_phase(h)
            assert p is not None, f"count-balanced but not Pauli-closed: {h!r}"
            tally[p] += 1
            if L <= FULL_LISTING_MAX_LEN or len(samples[p]) < 8:
                samples[p].append(h)
            if p != predicted_phase(h):
                rule_violations.append(h)
        by_phase = samples
        n_plus, n_minus = tally["+1"], tally["-1"]
        out[str(L)] = {
            "count": sum(tally.values()),
            "n_plus": n_plus,
            "n_minus": n_minus,
            "n_imaginary": tally["+i"] + tally["-i"],
            "signed_amplitude": n_plus - n_minus,
            "weight_of_signed_amplitude": (n_plus - n_minus) ** 2,
            "histories_listed_in_full": L <= FULL_LISTING_MAX_LEN,
            "histories_by_phase": by_phase,
        }
    # the exception: unbalanced histories DO reach +-i
    if not unbalanced_imaginary:
        for tup in product(TWISTS, repeat=3):
            h = ''.join(tup)
            if is_count_balanced(h):
                continue
            if fold_phase(h) in ("+i", "-i"):
                unbalanced_imaginary.append(h)
        prior_len3 = len(unbalanced_imaginary)
    return {
        "by_length": out,
        "phase_rule": "(-1)^(#neg twists) * sign(permutation sorting the axis word)"  # proven: QLF_PhaseRule.phase_rule
        ,
        "phase_rule_violations": rule_violations,
        "unbalanced_imaginary_witnesses": sorted(unbalanced_imaginary)[:12],
        "unbalanced_imaginary_count_len3": prior_len3 or len(unbalanced_imaginary),
    }


def build_depth_inventory(max_len: int, keep: dict | None = None) -> dict:
    out = dict(keep or {})
    for n in range(1, max_len // 2 + 1):
        if str(2 * n) in out:
            continue
        if 2 * n >= 18:
            print(f"   computing depth census at length {2*n}: 2^{2*n} = {2**(2*n):,} "
                  f"histories to sift...", flush=True)
        dist, law_ok = {}, True
        for tup in product((1, -1), repeat=2 * n):
            if sum(tup) != 0:
                continue
            s = list(tup)
            d = closure_depth(s)
            dist[d] = dist.get(d, 0) + 1
            if d != max_excursion(s):
                law_ok = False
        total = sum(dist.values())
        mode = max(dist, key=lambda k: dist[k])
        # listening(R): what a capacity-R horizon receives — cumulative in depth.
        listening = {}
        cum = 0
        for k in range(1, n + 1):
            cum += dist.get(k, 0)
            listening[str(k)] = {"ways_heard": cum, "fraction": round(cum / total, 6)}
        out[str(2 * n)] = {
            "listening_by_capacity": listening,
            "total_ways": total,
            "central_binomial": comb(2 * n, n),
            "strata": {str(k): v for k, v in sorted(dist.items())},
            "one_pass_ways": dist.get(1, 0),
            "deepest_stratum": dist.get(n, 0),
            "modal_depth": mode,
            "depth_equals_max_excursion": law_ok,
            "strata_that_are_gaussian_norms": {
                str(k): is_gaussian_norm(v) for k, v in sorted(dist.items())
            },
        }
    return out


# --------------------------------------------------------------------------- #
# first closures: the contextual layer, and the cylinder measure it lives on
# --------------------------------------------------------------------------- #
# Deliberately a *small fixed* set of contexts. The generic census above is universal substrate
# data; a preparation-and-apparatus is an experiment, and there are indefinitely many of those.
# What is stored here is the reusable part -- per event class the pair (W, A) that every derived
# quantity is computed from -- for the canonical geometries the Born work keeps returning to.
CLOSURE_CONTEXTS = [
    ("aligned",    "/",  ["\\", "/"]),
    ("transverse", "/",  [">\\", "<\\"]),
    ("mix-ZX",     "/",  ["\\>", "/<"]),
]
CLOSURE_CAPACITIES = (3, 4)


def build_closure_inventory(depth: int, keep: dict | None = None) -> dict:
    """First-closure event classes per context, with the cylinder-measure quantities.

    A closure **is** an event, so a run that has closed is not continued and the first closures of
    one experiment are prefix-free. That gives the depth weighting for free -- the cylinder measure
    `8^-d` on the Sigma_8 tree, with Kraft's inequality capping the total at 1
    (`QLF_KraftMeasure.twist_kraft`). Stored per event class `(branch, depth)`:

        W   how many ways close as that outcome, first, at that depth
        A   their signed total, from the proven phase rule

    and the two quantities built from them: the **multiplicity mass** `sum W/8^d` (a probability
    once conditioned on closing at all) and the **normalized-event weight**
    `sum A^2/(W . 8^d)` = multiplicity mass times squared mean phase.
    """
    from contextual_census import first_closure_census                      # the experiment layer

    out = dict(keep or {})
    for name, prep, branches in CLOSURE_CONTEXTS:
        for R in CLOSURE_CAPACITIES:
            key = f"{name}|R={R}"
            if key in out and out[key].get("depth", 0) >= depth:
                continue
            A, _ = first_closure_census(prep, branches, R, depth)
            W, _ = first_closure_census(prep, branches, R, depth, signed=False)
            classes, kraft, weight, amp_le_ways = {}, Fraction(0), Fraction(0), True
            for i in range(len(branches)):
                per = {}
                for d in range(depth + 1):
                    if W[i][d]:
                        per[str(d)] = {"ways": W[i][d], "signed": A[i][d]}
                        kraft += Fraction(W[i][d], 8 ** d)
                        weight += Fraction(A[i][d] ** 2, W[i][d] * 8 ** d)
                        if abs(A[i][d]) > W[i][d]:
                            amp_le_ways = False
                classes[branches[i]] = per
            mass = [sum(Fraction(W[i][d], 8 ** d) for d in range(depth + 1) if W[i][d])
                    for i in range(len(branches))]
            norm = [sum(Fraction(A[i][d] ** 2, W[i][d] * 8 ** d)
                        for d in range(depth + 1) if W[i][d]) for i in range(len(branches))]
            out[key] = {
                "preparation": prep,
                "branches": branches,
                "capacity": R,
                "depth": depth,
                "event_classes": classes,
                "kraft_mass": round(float(kraft), 12),
                "normalized_event_mass": round(float(weight), 12),
                "multiplicity_split": (round(float(mass[0] / sum(mass)), 12) if sum(mass) else None),
                "normalized_split": (round(float(norm[0] / sum(norm)), 12) if sum(norm) else None),
                "amplitude_le_ways": amp_le_ways,
                "kraft_bound_holds": kraft <= 1,
                "normalized_under_kraft": weight <= kraft,
            }
    return out


def _script_commit() -> str:
    """The commit this script was last changed in, plus a dirty marker.

    Deliberately no wall-clock timestamp: the database is a pure function of the
    script and the requested lengths, so a run that adds nothing should rewrite
    the file byte-for-byte identically. A build date would make every no-op run
    a diff.
    """
    def git(*args: str) -> str | None:
        try:
            out = subprocess.run(("git", *args), cwd=_HERE, capture_output=True, text=True)
        except OSError:
            return None
        return out.stdout.strip() if out.returncode == 0 else None

    commit = git("log", "-1", "--format=%h", "--", "census_inventory.py")
    if not commit:
        return "unknown"
    dirty = git("status", "--porcelain", "--", "census_inventory.py", "twist_core.py")
    return f"{commit}-dirty" if dirty else commit


def provenance(twist_len: int, phase_len: int) -> dict:
    """What produced these numbers — for copies of this file living elsewhere.

    Inside this repo it is decoration: `--quick` re-derives the cheap lengths on
    every push, so the file cannot silently drift from the code. It earns its
    place downstream, where a vendored copy (the Rust `qucalc` crate reads the
    `closures` layer; so does quantum-os) otherwise has no way to say which
    version of the census it is holding.
    """
    return {
        "script": "census_inventory.py",
        "script_commit": _script_commit(),
        "fold_census_to": twist_len,
        "depth_census_to": phase_len,
        "closure_depth": CLOSURE_DEPTH,
        "regenerate": f"python3 census_inventory.py --twist-len {twist_len} "
                      f"--phase-len {phase_len}",
    }


def build(twist_len: int, phase_len: int, keep: dict | None = None) -> dict:
    keep = keep or {}
    max_twist = max(twist_len, keep.get("max_twist_length", 0))
    max_phase = max(phase_len, keep.get("max_phase_length", 0))
    return {
        "_comment": "Census inventory: counts and QuCalc folds. Rebuild with census_inventory.py.",
        "_provenance": provenance(max_twist, max_phase),
        "_invariants_asserted": [
            "count balance => Pauli closure (count_balanced_pauli_closed)",
            "count balance => fold is +-I, never +-iI (balanced_phase_is_real)",
            "unbalanced histories do reach +-iI (unbalanced_can_be_imaginary)",
            "closure depth = max phase excursion (closedAtHorizon_iff_maxExcursion_le)",
            "one-pass closures number 2^n (onePass_ways_iff)",
            "the deepest stratum holds exactly 2 (QLF_ClosureMultiplicity.W_self)",
            "the second stratum is 2*3^(n-1) - 2^n (QLF_ClosureMultiplicity.W_two)",
            "depth 1 is never the modal depth for n >= 3 "
            "(QLF_ClosureMultiplicity.depth_one_not_modal)",
            "phase factorizes over independent factors (QLF_IndexedFactors.phase_factorizes)",
            "a joint closure of independent factors needs each factor closed (kron is scalar "
            "iff both are)",
            "first closures are prefix-free, so their cylinder mass sum W/8^d is at most 1 "
            "(QLF_KraftMeasure.twist_kraft)",
            "a signed class total never exceeds its way count, |A| <= W",
            "the normalized-event weight sum A^2/(W.8^d) stays under the Kraft mass "
            "(QLF_KraftMeasure.normalized_event_mass_le_one)",
        ],
        "max_twist_length": max_twist,
        "max_phase_length": max_phase,
        "folds": build_fold_inventory(twist_len, keep.get("folds")),
        "depths": build_depth_inventory(phase_len, keep.get("depths")),
        "factors": build_factor_inventory(min(twist_len, 8), keep.get("factors")),
        "closures": build_closure_inventory(CLOSURE_DEPTH, keep.get("closures")),
    }


# --------------------------------------------------------------------------- #
# verify
# --------------------------------------------------------------------------- #
def check(db: dict) -> list[str]:
    """Assert every proven invariant against the data. Returns a list of failures."""
    fail = []
    folds, depths = db["folds"], db["depths"]

    for L, rec in folds["by_length"].items():
        if rec["n_imaginary"] != 0:
            fail.append(f"balanced history folds to +-i at length {L} "
                        f"(contradicts balanced_phase_is_real)")
    if folds["phase_rule_violations"]:
        fail.append(f"phase rule violated by {len(folds['phase_rule_violations'])} histories")
    factors = db.get("factors", {})
    if factors.get("_violations"):
        fail.append(f"phase failed to factorize over independent factors for "
                    f"{len(factors['_violations'])} pairs")
    for L, rec in factors.items():
        if L.startswith("_"):
            continue
        if rec["shared_closures"] and rec["product_sector"] == 0:
            fail.append(f"no product-sector shared closures at length {L} "
                        f"(the indexed model would be empty)")
        if rec["coupled_sector"] == 0 and rec["shared_closures"]:
            fail.append(f"no coupled-sector closures at length {L} "
                        f"(entanglement would be impossible)")

    for key, rec in db.get("closures", {}).items():
        if not rec["kraft_bound_holds"]:
            fail.append(f"closure context {key}: cylinder mass {rec['kraft_mass']} exceeds 1 "
                        f"(contradicts QLF_KraftMeasure.twist_kraft -- the first-closure set "
                        f"cannot be prefix-free, or a run was counted twice)")
        if not rec["amplitude_le_ways"]:
            fail.append(f"closure context {key}: a signed class total exceeded its way count")
        if not rec["normalized_under_kraft"]:
            fail.append(f"closure context {key}: normalized-event mass "
                        f"{rec['normalized_event_mass']} exceeds the Kraft mass "
                        f"{rec['kraft_mass']} (contradicts normalized_event_mass_le_one)")

    if folds["unbalanced_imaginary_count_len3"] == 0:
        fail.append("no unbalanced imaginary witness found "
                    "(contradicts unbalanced_can_be_imaginary)")

    for L, rec in depths.items():
        n = int(L) // 2
        if rec["total_ways"] != rec["central_binomial"]:
            fail.append(f"length {L}: total ways != C(2n,n)")
        if rec["one_pass_ways"] != 2 ** n:
            fail.append(f"length {L}: one-pass ways {rec['one_pass_ways']} != 2^{n} "
                        f"(contradicts onePass_ways_iff)")
        if rec["deepest_stratum"] != 2:
            fail.append(f"length {L}: deepest stratum {rec['deepest_stratum']} != 2 "
                        f"(contradicts W_self)")
        if n >= 2 and rec["strata"].get("2", 0) != 2 * 3 ** (n - 1) - 2 ** n:
            fail.append(f"length {L}: second stratum {rec['strata'].get('2', 0)} != "
                        f"2*3^{n - 1} - 2^{n} (contradicts W_two)")
        if n >= 3 and rec["modal_depth"] == 1:
            fail.append(f"length {L}: modal depth is 1 (contradicts depth_one_not_modal)")
        if not rec["depth_equals_max_excursion"]:
            fail.append(f"length {L}: depth != max excursion (contradicts the depth law)")
    return fail


CLOSURE_DEPTH = 14
QUICK_TWIST_LEN = 6
QUICK_PHASE_LEN = 12


def compare_shared(fresh: dict, stored: dict) -> list[str]:
    """Compare every length present in both, ignoring depth of coverage."""
    out = []
    f_folds = fresh.get("folds", {}).get("by_length", {})
    s_folds = stored.get("folds", {}).get("by_length", {})
    for L in sorted(set(f_folds) & set(s_folds), key=int):
        for field in ("count", "n_plus", "n_minus", "n_imaginary", "signed_amplitude"):
            if f_folds[L][field] != s_folds[L][field]:
                out.append(f"fold census length {L}: {field} recomputed as "
                           f"{f_folds[L][field]}, stored says {s_folds[L][field]}")
    f_dep, s_dep = fresh.get("depths", {}), stored.get("depths", {})
    for L in sorted(set(f_dep) & set(s_dep), key=int):
        for field in ("total_ways", "one_pass_ways", "deepest_stratum", "modal_depth", "strata"):
            if f_dep[L][field] != s_dep[L][field]:
                out.append(f"depth census length {L}: {field} differs from stored")
    return out


def _arg(flag: str, default: int) -> int:
    if flag in sys.argv:
        return int(sys.argv[sys.argv.index(flag) + 1])
    return default


def main() -> int:
    verify = "--verify" in sys.argv
    quick = "--quick" in sys.argv
    rebuild = "--rebuild" in sys.argv

    stored = {}
    if os.path.exists(DB_PATH) and not rebuild:
        with open(DB_PATH) as fh:
            stored = json.load(fh)

    if quick:
        # CI gate: recompute the cheap lengths from scratch, compare, then assert
        # every invariant over the whole stored file.
        if not stored:
            print(f"FAIL: {DB_PATH} missing")
            return 1
        recomputed = build(QUICK_TWIST_LEN, QUICK_PHASE_LEN, None)
        fails = check(stored) + compare_shared(recomputed, stored)
        for msg in fails:
            print(f"FAIL: {msg}")
        if fails:
            return 1
        nf = len(stored["folds"]["by_length"])
        nd = len(stored["depths"])
        print(f"quick check passed: recomputed fold census to length {QUICK_TWIST_LEN} and depth "
              f"census to length {QUICK_PHASE_LEN}, matched the stored values, and all "
              f"{len(stored['_invariants_asserted'])} proven invariants hold over the full stored "
              f"database ({nf} fold lengths, {nd} depth lengths).")
        return 0

    twist_len = _arg("--twist-len", max(DEFAULT_TWIST_LEN, stored.get("max_twist_length", 0)))
    phase_len = _arg("--phase-len", max(DEFAULT_PHASE_LEN, stored.get("max_phase_length", 0)))

    fresh = build(twist_len, phase_len, None if rebuild else stored)
    fails = check(fresh)

    if verify:
        if not stored:
            print(f"FAIL: {DB_PATH} missing — run without --verify to build it")
            return 1
    else:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w") as fh:
            json.dump(fresh, fh, indent=1, sort_keys=True)
        added = (len(fresh["folds"]["by_length"]) - len(stored.get("folds", {}).get("by_length", {}))
                 + len(fresh["depths"]) - len(stored.get("depths", {})))
        print(f"wrote {DB_PATH} ({added} new entries; "
              f"fold census to length {fresh['max_twist_length']}, "
              f"depth census to length {fresh['max_phase_length']})")

    f = fresh["folds"]
    print("\nFOLD INVENTORY (count-balanced twist histories)")
    print("   len   ways   phase +1   phase -1   phase +-i   signed amplitude")
    for L, rec in sorted(f["by_length"].items(), key=lambda kv: int(kv[0])):
        print(f"   {L:>3} {rec['count']:>6} {rec['n_plus']:>10} {rec['n_minus']:>10}"
              f" {rec['n_imaginary']:>11} {rec['signed_amplitude']:>18}")
    print(f"   phase rule: {f['phase_rule']}")
    print(f"   violations: {len(f['phase_rule_violations'])}")
    print(f"   unbalanced witnesses reaching +-i (length 3): "
          f"{f['unbalanced_imaginary_count_len3']}, e.g. {f['unbalanced_imaginary_witnesses'][:4]}")
    here, nxt = fresh["max_twist_length"], fresh["max_twist_length"] + 2
    grow = balanced_history_count(nxt) / balanced_history_count(here)
    print(f"   next rung: --twist-len {nxt} enumerates "
          f"{balanced_history_count(nxt):,} balanced histories, {grow:.0f}x length {here}.")
    print("   This is the census at its ceiling -- push it only for a question that needs")
    print("   folds, and expect the run to be the cost of the answer.")

    fa = fresh.get("factors", {})
    if fa:
        print("\nFACTOR INVENTORY (each cut of a balanced history read as two indexed subsystems)")
        print("   len   shared   product sector   coupled sector   coupled fraction")
        for L, rec in sorted(((k, v) for k, v in fa.items() if not k.startswith("_")),
                             key=lambda kv: int(kv[0])):
            print(f"   {L:>3} {rec['shared_closures']:>8} {rec['product_sector']:>16}"
                  f" {rec['coupled_sector']:>16} {rec['coupled_fraction']:>18}")
        print("   product sector = both factors close alone (tensor-valid, indexing keeps it)")
        print("   coupled sector = neither closes alone but the pair does = entanglement,")
        print("   which exists only under flat concatenation -- so indexing cannot replace it.")

    print("\nDEPTH INVENTORY (+/- phase census)")
    print("   len   ways   one-pass   deepest   modal depth   depth = max excursion")
    for L, rec in sorted(db_items(fresh), key=lambda kv: int(kv[0])):
        print(f"   {L:>3} {rec['total_ways']:>6} {rec['one_pass_ways']:>10}"
              f" {rec['deepest_stratum']:>9} {rec['modal_depth']:>13}"
              f"   {'yes' if rec['depth_equals_max_excursion'] else 'NO'}")

    cl = fresh.get("closures", {})
    if cl:
        print("\nCLOSURE INVENTORY (first joint closures: the contextual layer)")
        print("   a closure IS an event, so first closures are prefix-free and their cylinder mass")
        print("   sum W/8^d cannot exceed 1 (QLF_KraftMeasure.twist_kraft) — the shortfall is the")
        print("   runs that never close here, which capacity removes rather than reweighs.")
        print(f"   {'context':<16}{'kraft mass':>12}{'normalized':>12}{'P(+) ways':>12}"
              f"{'P(+) weight':>13}")
        for key in sorted(cl):
            rec = cl[key]
            ms = rec["multiplicity_split"]
            ns = rec["normalized_split"]
            print(f"   {key:<16}{rec['kraft_mass']:>12.6f}{rec['normalized_event_mass']:>12.6f}"
                  f"{(f'{ms:.6f}' if ms is not None else '-'):>12}"
                  f"{(f'{ns:.6f}' if ns is not None else '-'):>13}")
        print("   the two splits bracket every possible notion of \"same event\": refining a")
        print("   quotient raises the weight (Cauchy-Schwarz), so the normalized split is the")
        print("   coarsest reading and the multiplicity split the finest.")

    print("\nLISTENING — what a capacity-R horizon receives (fraction of the census)")
    caps = [1, 2, 3, 4, 5]
    print("   len  " + "".join(f"   R={c:<6}" for c in caps))
    for L, rec in sorted(db_items(fresh), key=lambda kv: int(kv[0])):
        cells = []
        for c in caps:
            e = rec["listening_by_capacity"].get(str(c))
            cells.append(f"   {e['fraction']:<8.4f}" if e else "   {:<8}".format("1.0000"))
        print(f"   {L:>3}  " + "".join(cells))
    print("   a shallow capacity hears only the shallow closures; no finite capacity")
    print("   hears everything (law_of_exceptions), and each step up adds lines (lines_mono).")
    p_here = fresh["max_phase_length"]
    print(f"   next rung: --phase-len {p_here + 2} sifts {2 ** (p_here + 2):,} walks, "
          f"4x length {p_here}.")
    print("   This census is nowhere near its ceiling -- it is the cheap one to push when")
    print("   a question is about depth or listening rather than folds.")

    print()
    if fails:
        for msg in fails:
            print(f"FAIL: {msg}")
        return 1
    print(f"all {len(fresh['_invariants_asserted'])} proven invariants hold on the enumerated data.")
    return 0


def db_items(db):
    return db["depths"].items()


if __name__ == "__main__":
    raise SystemExit(main())
