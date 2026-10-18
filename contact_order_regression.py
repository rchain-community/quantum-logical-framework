#!/usr/bin/env python3
"""
contact_order_regression.py — the contact-order test, against experiment.

[`Protein_Folding.md`](Protein_Folding.md) §5a derives a prediction and states its kill condition.
The derivation: contacts are independent closures that compose (`closedLoop_append`), so the ways
multiply, `ways = prod_c p(l_c)`; the census measures `p(l) ~ l^-theta`; therefore

    ln(ways) = -theta * SUM_c ln l_c

and reading the fastest fold as the one realized the most ways (an assumption this test checks; see
MostWays_First.md: most ways does not by itself mean first), the folding rate should track the **sum of
the logarithms** of the contact separations -- not the arithmetic mean of the separations, which is
what relative contact order (Plaxco, Simons & Baker 1998) uses.

**Kill condition, stated before the data was looked at** (frozen in the commit that added §5a):
regress `ln k_f` on both; if arithmetic contact order wins consistently, the multiplicative
composition is wrong.

This script runs that regression on the 26 crosslink-free two-state proteins of Weikl (2006),
whose folding rates come from Table 1 of Grantcharova et al. (2001). Contact maps are computed
here from the PDB structures under the Plaxco convention (heavy-atom pairs within 6 A), and
**validated by reproducing Weikl's published rel.CO and rel.logCO columns** before any regression
is run -- 25 of 26 to the printed decimal.

Measures compared:
    rel.CO        (1/(L N)) sum l_c            Plaxco et al. 1998, the standard
    rel.logCO     (1/(N log L)) sum log l_c    Weikl 2006 -- PRIOR ART for the log form
    abs.CO        (1/N) sum l_c
    abs.logCO     (1/N) sum log l_c
    sum.logCO     sum log l_c                  <- the raw QLF quantity, unnormalised
    the same five again over RESIDUE-level contacts, since a closure is one contact and not one
    atom pair -- the QLF-native counting.

Usage:
    python3 contact_order_regression.py --fetch    # download PDBs, recompute, rewrite the table
    python3 contact_order_regression.py            # regress from the stored table (no network)
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(ROOT, "data", "contact_order.json")
PDBDIR = os.environ.get("QLF_PDB_CACHE", os.path.join(ROOT, ".pdb_cache"))

# name, pdb, chain, lo, hi, icode, log10 kf, published rel.CO, published rel.logCO, published L
DATASET = [
    ("Cyt b562",         "256B", "A", None, None, None,  5.30,  7.5, 24.7, 106),
    ("myoglobin",        "1BZP", "A", None, None, None,  4.83,  8.0, 25.1, 153),
    ("lambda-repressor", "1LMB", "3",    6,   85, None,  4.78,  9.4, 26.0,  80),
    ("PSBD",             "2PDD", "A",    3,   43, None,  4.20, 11.0, 24.9,  41),
    ("Cyt c",            "1HRC", "A",    1,  104, None,  3.80, 11.2, 29.6, 104),
    ("Im9",              "1IMQ", "A", None, None, None,  3.16, 12.1, 29.7,  86),
    ("ACBP",             "2ABD", "A", None, None, None,  2.85, 14.3, 32.0,  86),
    ("Villin 14T",       "2VIK", "A", None, None, None,  3.25, 12.3, 33.5, 126),
    ("N-term L9",        "1DIV", "A",    1,   56, None,  2.87, 12.7, 29.6,  56),
    ("Ubiquitin",        "1UBQ", "A", None, None, None,  3.19, 15.1, 33.2,  76),
    ("CI2",              "2CI2", "I",   20,   83, None,  1.75, 15.7, 32.2,  64),
    ("U1A",              "1URN", "A", None, None, None,  2.53, 16.9, 34.7,  96),
    ("Ada2h",            "1AYE", "A",    4,   85,  "A",  2.88, 16.7, 33.0,  80),
    ("Protein G",        "1PGB", "A", None, None, None,  2.46, 17.3, 34.4,  56),
    ("Protein L",        "1HZ6", "A",    1,   62, None,  1.78, 16.1, 33.8,  62),
    ("FKBP",             "1FKB", "A", None, None, None,  0.60, 17.7, 37.3, 107),
    ("HPr",              "1POH", "A", None, None, None,  1.17, 17.6, 34.6,  85),
    ("MerP",             "1AFI", "A", None, None, None,  0.26, 18.9, 36.7,  72),
    ("mAcP",             "1APS", "A", None, None, None, -0.64, 21.7, 40.0,  98),
    ("CspB",             "1CSP", "A", None, None, None,  2.84, 16.4, 35.7,  67),
    ("TNfn3",            "1TEN", "A",  803,  891, None,  0.46, 17.4, 37.6,  89),
    ("TI I27",           "1TIT", "A", None, None, None,  1.51, 17.8, 36.4,  89),
    ("Fyn SH3",          "1SHF", "A", None, None, None,  1.97, 18.3, 36.7,  59),
    ("Twitchin",         "1WIT", "A", None, None, None,  0.18, 20.3, 40.9,  93),
    ("PsaE",             "1PSF", "A", None, None, None,  0.51, 17.0, 34.5,  69),
    ("Sso7d",            "1BNZ", "A", None, None, None,  3.02, 12.2, 30.8,  64),
]


# =============================================================================
# CONTACT MAPS (Plaxco convention: heavy-atom pairs within 6 A)
# =============================================================================
def models(pdbid, chain=None, lo=None, hi=None, icode=None):
    """Heavy atoms per NMR model (one 'model' for an X-ray structure)."""
    out, cur, order, seen = [], [], [], {}

    def flush():
        nonlocal cur, order, seen
        if cur:
            out.append(cur)
        cur, order, seen = [], [], {}

    for line in open(os.path.join(PDBDIR, pdbid + ".pdb")):
        if line[:6] == "MODEL ":
            flush()
        elif line.startswith("ATOM  "):
            if line[16] not in (" ", "A"):                      # alternate locations
                continue
            if chain is not None and line[21] != chain:
                continue
            name = line[12:16].strip()
            elem = line[76:78].strip() or name[:1]
            if elem == "H" or name.startswith("H"):
                continue
            try:
                num = int(line[22:26])
            except ValueError:
                continue
            if lo is not None and not (lo <= num <= hi):
                continue
            if icode is not None and line[26] != icode:
                continue
            key = (line[21], line[22:27])
            if key not in seen:
                seen[key] = len(order)
                order.append(key)
            cur.append((seen[key], float(line[30:38]), float(line[38:46]), float(line[46:54])))
    flush()
    return out


def _cells(atoms, cutoff):
    cell = defaultdict(list)
    for a in atoms:
        cell[(int(a[1] // cutoff), int(a[2] // cutoff), int(a[3] // cutoff))].append(a)
    return cell


def separations(atoms, cutoff=6.0, minsep=1, residue_level=False):
    """Sequence separations of all contacts. Atom-pair (Plaxco) or residue-level (QLF)."""
    cell = _cells(atoms, cutoff)
    c2 = cutoff * cutoff
    seps, pairs = [], set()
    for (i, j, k), bucket in cell.items():
        near = []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for dk in (-1, 0, 1):
                    near.extend(cell.get((i + di, j + dj, k + dk), ()))
        for a in bucket:
            for b in near:
                if b[0] - a[0] < minsep:            # ordered: kills self and double counting
                    continue
                dx, dy, dz = a[1] - b[1], a[2] - b[2], a[3] - b[3]
                if dx * dx + dy * dy + dz * dz <= c2:
                    if residue_level:
                        pairs.add((a[0], b[0]))
                    else:
                        seps.append(b[0] - a[0])
    return [j - i for (i, j) in pairs] if residue_level else seps


def measures(pdbid, chain=None, lo=None, hi=None, icode=None, minsep=1, cutoff=6.0):
    acc = defaultdict(list)
    for atoms in models(pdbid, chain, lo, hi, icode):
        L = max(a[0] for a in atoms) + 1
        acc["L"].append(L)
        for tag, res in (("", False), ("res_", True)):
            seps = separations(atoms, cutoff, minsep, res)
            N = len(seps)
            if not N:
                continue
            s = sum(seps)
            sl = sum(math.log(x) for x in seps)
            acc[tag + "relCO"].append(100.0 * s / (L * N))
            acc[tag + "relLogCO"].append(100.0 * sl / (N * math.log(L)))
            acc[tag + "absCO"].append(s / N)
            acc[tag + "absLogCO"].append(sl / N)
            acc[tag + "sumLogCO"].append(sl)
            acc[tag + "N"].append(N)
    return {k: sum(v) / len(v) for k, v in acc.items()}


# =============================================================================
# REGRESSION
# =============================================================================
def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)


def jackknife(x, y, drop=2):
    """Spread of r over all subsets with up to `drop` points removed (Weikl's error estimate)."""
    from itertools import combinations
    n = len(x)
    rs = []
    for d in range(drop + 1):
        for out in combinations(range(n), d):
            keep = [i for i in range(n) if i not in out]
            rs.append(pearson([x[i] for i in keep], [y[i] for i in keep]))
    m = sum(rs) / len(rs)
    sd = math.sqrt(sum((r - m) ** 2 for r in rs) / len(rs))
    return min(rs), max(rs), sd


def build():
    rows, bad = [], []
    for (name, pid, ch, lo, hi, ic, lk, pco, plog, pL) in DATASET:
        m = measures(pid, ch, lo, hi, ic)
        exact = abs(m["relCO"] - pco) < 0.15 and abs(m["relLogCO"] - plog) < 0.15 \
            and round(m["L"]) == pL
        if not exact:
            bad.append((name, pid, round(m["L"]), pL, round(m["relCO"], 1), pco,
                        round(m["relLogCO"], 1), plog))
        rows.append(dict(name=name, pdb=pid, logkf=lk, pub_relCO=pco, pub_relLogCO=plog,
                         pub_L=pL, reproduces_published=exact,
                         **{k: round(v, 4) for k, v in m.items()}))
    return rows, bad


MEASURES = [
    ("rel.CO        (Plaxco 1998)", "relCO"),
    ("rel.logCO     (Weikl 2006)", "relLogCO"),
    ("abs.CO", "absCO"),
    ("abs.logCO", "absLogCO"),
    ("sum log l     (QLF, raw)", "sumLogCO"),
    ("rel.CO      residue-level", "res_relCO"),
    ("rel.logCO   residue-level", "res_relLogCO"),
    ("abs.logCO   residue-level", "res_absLogCO"),
    ("sum log l   residue-level (QLF)", "res_sumLogCO"),
]


def report(rows):
    y = [r["logkf"] for r in rows]
    print("n = %d two-state proteins (Weikl 2006 set; rates from Grantcharova et al. 2001)\n"
          % len(rows))
    print("%-34s %8s %8s   %s" % ("measure", "r", "|r|", "jackknife |r| range (drop<=2)"))
    results = []
    for label, key in MEASURES:
        x = [r[key] for r in rows]
        r = pearson(x, y)
        lo, hi, sd = jackknife(x, y)
        results.append((abs(r), label, key, r, lo, hi, sd))
        print("%-34s %8.3f %8.3f   [%.3f, %.3f]  sd %.3f"
              % (label, r, abs(r), abs(hi), abs(lo), sd))
    results.sort(reverse=True)
    print("\nbest: %s  (|r| = %.3f)" % (results[0][1].strip(), results[0][0]))
    co = dict((k, abs(pearson([r[k] for r in rows], y))) for _, k in MEASURES)
    print("\ncorrelation between the two contenders themselves:")
    print("  rel.CO vs rel.logCO           r = %.4f"
          % pearson([r["relCO"] for r in rows], [r["relLogCO"] for r in rows]))
    print("  rel.CO vs sum log l           r = %.4f"
          % pearson([r["relCO"] for r in rows], [r["sumLogCO"] for r in rows]))
    return co


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fetch", action="store_true",
                    help="download the PDB structures and recompute the table")
    args = ap.parse_args()

    if args.fetch:
        import urllib.request
        os.makedirs(PDBDIR, exist_ok=True)
        for (_, pid, *_rest) in DATASET:
            dst = os.path.join(PDBDIR, pid + ".pdb")
            if not os.path.exists(dst):
                print("  fetching %s ..." % pid, flush=True)
                urllib.request.urlretrieve(
                    "https://files.rcsb.org/download/%s.pdb" % pid, dst)
        rows, bad = build()
        print("\nVALIDATION: %d / %d reproduce Weikl's published rel.CO, rel.logCO and L"
              % (sum(r["reproduces_published"] for r in rows), len(rows)))
        for b in bad:
            print("   near-miss %-18s %s  L=%s(pub %s) relCO=%s(pub %s) relLogCO=%s(pub %s)" % b)
        os.makedirs(os.path.dirname(TABLE), exist_ok=True)
        with open(TABLE, "w") as fh:
            json.dump(rows, fh, indent=1, sort_keys=True)
        print("wrote %s\n" % TABLE)
    else:
        if not os.path.exists(TABLE):
            print("no stored table; run with --fetch first")
            return 1
        rows = json.load(open(TABLE))

    report(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
