#!/usr/bin/env python3
"""
protein_census.py — the folding census: a fold is a closure inventory.

Chemistry.md gets molecules from one rule (a bond is a shared closure) and stops at
stoichiometry, because a small molecule has no shape to speak of. A polymer does. This
script is the census that takes the rule to conformation, and it is built on one
observation: **a backbone step is already a twist**. A chain on the cubic lattice moves by
one of six signed axis displacements, and the 8-twist alphabet is the signed axis frame,
so a conformation IS a twist history (lean/QLF_Folding.lean).

Everything else follows from counting that history:

  * A **contact** is a ZFA closure — the segment between two touching residues plus the
    contact edge has zero net displacement, hence is count-balanced, hence Pauli-closed by
    `count_balanced_pauli_closed`. Verified here at runtime against `twist_core.is_zfa` on
    every contact loop enumerated (invariant I1).
  * Contacts occur only at **odd** sequence separation — the lattice-protein parity rule,
    proven in Lean as a corollary of count balance (I2).
  * The **contact quantum is log 2** (QLF_FreeEnergy): a fold's free energy is
    -(contacts) x log 2 nats, so the lattice contact energy is derived, not fitted.

The output is an **inventory in the shared `closures` schema** — the same one
data/census_inventory.json uses and the Rust `qucalc` crate loads
(rhovision-org/rholo, qucalc/src/lib.rs). Each entry is
`event_classes[branch][class] = {signed, ways}` with **ways held as a coefficient**: a
fold reachable N ways is ONE weighted class, not N terms. That is the whole answer to
Levinthal — the exponential is a number in a record, never a list to be searched — and it
means `qucalc::most_ways_first` ranks these censuses with no new code:

    fold|...          -> most_ways_first gives the native fold
    designability|4x4 -> most_ways_first gives the most designable structure
    loopclosure|...   -> most_ways_first gives the folding ORDER (short loops first)

Usage:
    python3 protein_census.py                # full run, writes data/folding_census.json
    python3 protein_census.py --quick        # cheap re-run + assert every invariant (CI)
    python3 protein_census.py --saw-len 13   # push the 2-D walk census one length deeper
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import defaultdict

import twist_core

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "folding_census.json")

# =============================================================================
# THE BACKBONE IS A TWIST HISTORY
# =============================================================================
# The six signed axis displacements ARE the six spatial twists, under twist_core's own
# axis assignment (^ = +sigma_y, > = +sigma_x, / = +sigma_z). The gauge pair '+'/'-'
# carries phase, not displacement, so it is never a backbone step -- which is why the
# gauge counts of an encoded backbone vanish identically (QLF_Folding.count_encode_plus).

STEPS_3D = {
    (1, 0, 0): '>', (-1, 0, 0): '<',
    (0, 1, 0): '^', (0, -1, 0): 'v',
    (0, 0, 1): '/', (0, 0, -1): '\\',
}
CONJ = {'>': '<', '<': '>', '^': 'v', 'v': '^', '/': '\\', '\\': '/'}


def step_twist(a, b):
    """The twist carrying lattice site `a` to adjacent site `b`."""
    return STEPS_3D[tuple(b[i] - a[i] for i in range(3))]


def backbone_history(sites):
    """The conformation read as a twist history."""
    return ''.join(step_twist(sites[i], sites[i + 1]) for i in range(len(sites) - 1))


def contact_loop(sites, i, j):
    """The closed history of the contact (i, j): the segment i..j plus the contact edge.

    Zero net displacement by construction, so `twist_core.is_zfa` must accept it --
    that is QLF_Folding.contact_is_closure, checked rather than assumed."""
    seg = backbone_history(sites[i:j + 1])
    return seg + CONJ[step_twist(sites[i], sites[j])]


def loop_phase(history):
    """The Pauli phase of a closed loop: +1 or -1.

    Count balance forces the fold to be a REAL scalar (+-I, never +-iI) --
    `balanced_phase_is_real` (lean/QLF_BalancedPhaseReal.lean). Returning None here
    would be a violation, and invariant I5 asserts it never happens."""
    a, b, c, d = twist_core.pauli_fold(history)
    tol = twist_core.PAULI_TOLERANCE
    if abs(b) > tol or abs(c) > tol or abs(a - d) > tol:
        return None
    if abs(a - 1) < tol:
        return 1
    if abs(a + 1) < tol:
        return -1
    return None


# =============================================================================
# THERMODYNAMICS FROM THE CLOSURE QUANTUM
# =============================================================================
# There is one energy scale and it is not fitted: a closure is a many-to-one recognition
# event worth exactly one bit, so `dF = -log 2` nats per contact (QLF_FreeEnergy). A
# conformation with c contacts therefore carries Boltzmann weight
#
#     exp(-E/kT) = 2^(c/T),        E(c) = -c log 2,   T in nats
#
# and at T = 1 nat that weight is exactly 2^c -- an INTEGER. That is the same statement as
# the free-energy quantum, read as a count: closing a binary distinction multiplies the
# ways by two. So the closure-weighted multiplicity g(c)*2^c is still a count of ways, and
# `most_ways_first` on it is the folding transition rather than an energy minimisation.

def thermo(dos, tmin=0.05, tmax=4.0, steps=160):
    """Specific-heat curve from the density of states. Returns the transition temperature.

    T is measured in nats, so T = 1 IS the closure quantum. No parameter enters here that
    is not `log 2`."""
    items = [(int(c), n) for c, n in dos.items() if n]
    if len(items) < 2:
        return {"T_peak": None, "C_max": None, "note": "no transition -- fewer than two classes"}
    log2 = math.log(2)
    best = (None, -1.0)
    curve = []
    for k in range(steps + 1):
        T = tmin + (tmax - tmin) * k / steps
        # log-sum-exp over classes; E(c) = -c log 2 so -E/T = c log2 / T
        m = max(c * log2 / T for c, _ in items)
        z = sum(n * math.exp(c * log2 / T - m) for c, n in items)
        e1 = sum(n * (-c * log2) * math.exp(c * log2 / T - m) for c, n in items) / z
        e2 = sum(n * (c * log2) ** 2 * math.exp(c * log2 / T - m) for c, n in items) / z
        C = (e2 - e1 * e1) / (T * T)
        curve.append([round(T, 4), round(C, 6)])
        if C > best[1]:
            best = (T, C)
    high = None
    for k in range(1, len(curve) - 1):
        if curve[k][1] > curve[k - 1][1] and curve[k][1] >= curve[k + 1][1]:
            high = curve[k][0]
    return {"T_peak": round(best[0], 4), "C_max": round(best[1], 6),
            "T_peak_highest": high,
            "T_units": "nats; T = 1 is the closure quantum log 2",
            "curve": curve[::8]}


# =============================================================================
# SELF-AVOIDING WALKS
# =============================================================================
def _neighbours(p, dim):
    x, y, z = p
    out = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z)]
    if dim == 3:
        out += [(x, y, z + 1), (x, y, z - 1)]
    return out


def walks(nsteps, dim):
    """All self-avoiding walks of `nsteps` steps with the first step fixed.

    Fixing the first step quotients the lattice rotation group (4 in 2-D, 6 in 3-D);
    the full count is recovered by multiplying, and every per-pair statistic below is
    invariant under it."""
    start = (0, 0, 0)
    first = (1, 0, 0)
    if nsteps == 0:
        yield [start]
        return
    path = [start, first]
    seen = {start, first}

    def rec():
        if len(path) == nsteps + 1:
            yield list(path)
            return
        for q in _neighbours(path[-1], dim):
            if q not in seen:
                seen.add(q)
                path.append(q)
                yield from rec()
                path.pop()
                seen.remove(q)

    yield from rec()


def saw_census(nsteps, dim, zfa_check_budget=20000):
    """Enumerate the walks and count, per sequence separation, how many ways a loop closes.

    `closing[l]` is the number of (walk, pair) incidences at separation `l` whose two
    residues are lattice-adjacent -- the multiplicity of a loop closure of that span.
    `opportunities[l]` is how many such pairs were looked at, so the ratio is the
    per-pair closure probability."""
    sym = 4 if dim == 2 else 6
    nres = nsteps + 1
    closing = defaultdict(int)
    signed = defaultdict(int)
    opportunities = defaultdict(int)
    dos = defaultdict(int)
    nwalks = 0
    checked = set()
    zfa_failures = []
    parity_failures = []
    phase_failures = []

    for sites in walks(nsteps, dim):
        nwalks += 1
        ncontacts = 0
        occupied = {p: k for k, p in enumerate(sites)}
        for i in range(nres):
            for j in range(i + 3, nres):
                opportunities[j - i] += 1
        for i in range(nres):
            for q in _neighbours(sites[i], dim):
                j = occupied.get(q)
                if j is None or j <= i + 2:
                    continue
                sep = j - i
                closing[sep] += 1
                ncontacts += 1
                if sep % 2 == 0:                       # I2: parity rule
                    parity_failures.append((i, j))
                loop = contact_loop(sites, i, j)
                ph = loop_phase(loop)
                if ph is None:                          # I5: balanced fold is real
                    phase_failures.append(loop)
                else:
                    signed[sep] += ph
                if len(checked) < zfa_check_budget and loop not in checked:
                    checked.add(loop)
                    if not twist_core.is_zfa(loop):     # I1: a contact IS a closure
                        zfa_failures.append(loop)
        dos[ncontacts] += 1

    return {
        "dim": dim,
        "steps": nsteps,
        "residues": nres,
        "walks_first_step_fixed": nwalks,
        "walks_total": nwalks * sym,
        "closing": {str(k): v for k, v in sorted(closing.items())},
        "dos": {str(k): v for k, v in sorted(dos.items())},
        "collapse": thermo({str(k): v for k, v in sorted(dos.items())}),
        "signed": {str(k): v for k, v in sorted(signed.items())},
        "opportunities": {str(k): v for k, v in sorted(opportunities.items())},
        "zfa_loops_checked": len(checked),
        "zfa_failures": zfa_failures[:5],
        "parity_failures": parity_failures[:5],
        "phase_failures": phase_failures[:5],
    }


# Known self-avoiding-walk counts, square lattice (OEIS A001411) and cubic (A001412).
# An external check that the enumerator is right, not a QLF claim.
KNOWN_SAW = {
    2: [1, 4, 12, 36, 100, 284, 780, 2172, 5916, 16268, 44100, 120292, 324932, 881500,
        2374444],
    3: [1, 6, 30, 150, 726, 3534, 16926, 81390, 387966, 1853886, 8809878],
}


# =============================================================================
# COMPACT STRUCTURES AND DESIGNABILITY (the 4x4 lattice, N = 16)
# =============================================================================
def hamiltonian_contact_sets(w=4, h=4):
    """Every Hamiltonian path on the w x h grid, reduced to its CONTACT SET.

    Reducing a structure to its contacts is not a shortcut -- it is the object. An
    apparatus IS a closure inventory (ScientificApproach.md), and two conformations with
    the same contacts are the same closure inventory. The 8 lattice symmetries preserve
    the contact set, so the quotient happens for free."""
    n = w * h
    cells = [(x, y) for x in range(w) for y in range(h)]
    idx = {c: k for k, c in enumerate(cells)}
    adj = [[] for _ in range(n)]
    for (x, y) in cells:
        for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q in idx:
                adj[idx[(x, y)]].append(idx[q])

    sets = defaultdict(int)
    npaths = 0
    path = []
    used = [False] * n

    def rec(v):
        nonlocal npaths
        path.append(v)
        used[v] = True
        if len(path) == n:
            npaths += 1
            pos = [0] * n
            for order, cell in enumerate(path):
                pos[cell] = order
            contacts = []
            for c in range(n):
                for d in adj[c]:
                    if d > c:
                        i, j = sorted((pos[c], pos[d]))
                        if j - i >= 3:
                            contacts.append((i, j))
            sets[tuple(sorted(contacts))] += 1
        else:
            for q in adj[v]:
                if not used[q]:
                    rec(q)
        used[v] = False
        path.pop()

    for s in range(n):
        rec(s)
    return sets, npaths


def _popcount_table(bits):
    tbl = [0] * (1 << bits)
    for i in range(1, 1 << bits):
        tbl[i] = tbl[i >> 1] + (i & 1)
    return tbl


def designability(contact_sets, n=16):
    """Li-Helling-Tang-Wingreen designability: how many sequences fold to each structure.

    For every HP sequence (a bitmask of hydrophobic positions) the energy of a structure
    is -(H-H contacts) x log 2. Only H-H contacts count, and that is derived rather than
    posited: a polar residue closes with the solvent whether or not it is buried, so no
    free energy is DIFFERENTIALLY released by burying it. Only a closure unavailable from
    water can pay. A sequence folds when exactly one structure attains the maximum.

    `ways` for a structure is then the number of sequences it is the unique answer for --
    a multiplicity over sequence space, which is what designability has always been."""
    pop = _popcount_table(n)
    full = 1 << n
    best = [-1] * full
    best_ct = [0] * full
    best_ix = [-1] * full

    for six, contacts in enumerate(contact_sets):
        nbr = [0] * n
        for (i, j) in contacts:
            nbr[i] |= 1 << j
            nbr[j] |= 1 << i
        e = [0] * full
        for s in range(1, full):
            low = s & -s
            i = low.bit_length() - 1
            s2 = s ^ low
            e[s] = e[s2] + pop[nbr[i] & s2]
        for s in range(full):
            v = e[s]
            if v > best[s]:
                best[s] = v
                best_ct[s] = 1
                best_ix[s] = six
            elif v == best[s]:
                best_ct[s] += 1

    des = [0] * len(contact_sets)
    folders = 0
    for s in range(full):
        if best_ct[s] == 1 and best[s] > 0:
            des[best_ix[s]] += 1
            folders += 1
    return des, folders


# =============================================================================
# HYDROPHOBICITY FROM THE VALENCE RULE
# =============================================================================
# Chemistry.md's rule already decides this. A side chain that is a saturated hydrocarbon
# has NO free valence, so it cannot share a closure with water -- the same argument that
# makes helium a billiard ball (valence 0 => no shared closure => elastic only). A side
# chain carrying an N, O or S with an unshared hydrogen, or a charge, HAS a free valence
# and shares with water. So: free valence on the side chain => P; none => H.
#
# Reference column is the sign of Kyte & Doolittle (1982) hydropathy. Epistemic tag:
# phenomenological match (ScientificApproach.md), and the misses are named, not hidden.
SIDE_CHAINS = {
    # residue: (free valence on side chain?, Kyte-Doolittle hydropathy, description)
    'Gly': (False, -0.4, 'H only -- no side chain at all'),
    'Ala': (False, +1.8, '-CH3'),
    'Val': (False, +4.2, '-CH(CH3)2'),
    'Leu': (False, +3.8, '-CH2CH(CH3)2'),
    'Ile': (False, +4.5, '-CH(CH3)CH2CH3'),
    'Pro': (False, -1.6, 'cyclic hydrocarbon, fused to the backbone'),
    'Phe': (False, +2.8, '-CH2-C6H5'),
    'Met': (False, +1.9, 'thioether -- S fully substituted, no free valence'),
    'Trp': (True,  -0.9, 'indole N-H'),
    'Cys': (True,  +2.5, 'thiol S-H'),
    'Tyr': (True,  -1.3, 'phenol O-H'),
    'Ser': (True,  -0.8, 'hydroxyl O-H'),
    'Thr': (True,  -0.7, 'hydroxyl O-H'),
    'Asn': (True,  -3.5, 'amide N-H2'),
    'Gln': (True,  -3.5, 'amide N-H2'),
    'Asp': (True,  -3.5, 'carboxylate'),
    'Glu': (True,  -3.5, 'carboxylate'),
    'Lys': (True,  -3.9, 'ammonium'),
    'Arg': (True,  -4.5, 'guanidinium'),
    'His': (True,  -3.2, 'imidazole N-H'),
}


def hydrophobicity_check():
    rows = []
    agree = 0
    for res, (free_valence, kd, why) in SIDE_CHAINS.items():
        predicted = 'P' if free_valence else 'H'
        reference = 'H' if kd > 0 else 'P'
        ok = predicted == reference
        agree += ok
        rows.append({"residue": res, "side_chain": why, "free_valence": free_valence,
                     "predicted": predicted, "kyte_doolittle": kd,
                     "reference": reference, "agrees": ok})
    return {"rows": rows, "agree": agree, "total": len(SIDE_CHAINS),
            "misses": [r["residue"] for r in rows if not r["agrees"]]}


# =============================================================================
# THE INVENTORY -- shared `closures` schema (qucalc/src/lib.rs reads this)
# =============================================================================
def loop_closure_closure(sc):
    """`loopclosure|...`: branch = sequence separation, class = separation, ways = closures.

    most_ways_first on this entry returns the loop spans ranked by ways: the short loops close
    in the most ways. Reading that ranking as folding ORDER was tested and withdrawn
    (Protein_Folding.md 5e; most ways does not by itself mean first, MostWays_First.md)."""
    ec = {}
    for sep, ways in sc["closing"].items():
        ec[sep] = {sep: {"signed": sc["signed"].get(sep, 0), "ways": ways}}
    return {
        "preparation": "open chain, dim=%d, %d residues" % (sc["dim"], sc["residues"]),
        "branches": sorted(ec, key=int),
        "event_classes": ec,
        "closure_probability": {k: sc["closing"][k] / sc["opportunities"][k]
                                for k in sc["closing"]},
        "walks_total": sc["walks_total"],
    }


def designability_closure(des, contact_sets, folders, npaths, topk=16):
    order = sorted(range(len(des)), key=lambda i: -des[i])[:topk]
    # The class here is the STRUCTURE, not the contact count: every compact 4x4 structure
    # has exactly 9 contacts, so keying by contact count would merge all 69 into one class.
    # `ways` is the designability -- how many sequences fold to it -- so most_ways_first
    # returns the most designable structure.
    ec = {str(i): {"signed": des[i], "ways": des[i]} for i in order if des[i]}
    return {
        "preparation": "all 2^16 HP sequences on the 4x4 compact lattice",
        "branches": ["designability"],
        "event_classes": {"designability": ec},
        "contacts_per_structure": sorted({len(c) for c in contact_sets}),
        "structures": len(contact_sets),
        "hamiltonian_paths": npaths,
        "sequences_that_fold": folders,
        "designability_max": max(des),
        "designability_mean": sum(des) / len(des),
        "truncated_to_top": topk,
    }


def fold_closure(fc, weighted=False):
    """One census entry per sequence: class = closures achieved, ways = how many ways.

    `weighted=False` counts conformations only -- and `most_ways_first` on it returns the
    COIL, because the unfolded state is the one with the most shapes. That is not a defect
    in the principle, it is the denatured state, and it is what the principle should say at
    high temperature.

    `weighted=True` counts the closure events too. A closure resolves a binary distinction
    and is worth exactly one bit (`dF = -log 2`), so it carries multiplicity 2, and a
    conformation with c contacts is realized `g(c) * 2^c` ways. Still an exact integer,
    still a count. `most_ways_first` on THIS entry returns the native fold once the
    closures outnumber the shapes -- which is the folding transition, not a re-ranking."""
    ec = {}
    for cls, ways in fc["dos"].items():
        scale = (2 ** int(cls)) if weighted else 1
        ec[str(cls)] = {"signed": fc["signed"].get(cls, 0) * scale, "ways": ways * scale}
    return {
        "preparation": fc["sequence"],
        "branches": ["fold"],
        "event_classes": {"fold": ec},
        "weighted_by_closure_multiplicity": weighted,
        "max_hh_contacts": fc["max_hh_contacts"],
        "ground_state_degeneracy": fc["ground_state_degeneracy"],
        "unique_ground_state": fc["unique_ground_state"],
        "free_energy_nats": fc["free_energy_nats"],
        "transition": {k: v for k, v in fc["folding"].items() if k != "curve"},
    }


def fold_census(seq, dim=2, topk=12, zfa_budget=5000):
    """Every conformation of one HP sequence, grouped by contact set.

    class = the number of H-H closures (the closure depth), ways = how many conformations
    realize that contact set, signed = the product of those same closures' Pauli phases,
    summed over the ways.

    The phase multiplies over the H-H contacts ONLY -- the same set that defines the class and
    that the energy function charges. Multiplying over every geometric contact instead would make
    `signed` the signed version of a different quantity than `ways` counts, which is exactly the
    mismatch that made an earlier reading of this census meaningless (a zero-contact class came
    back with |A|/W = 0.179 when an empty product must give 1)."""
    nsteps = len(seq) - 1
    groups = defaultdict(lambda: [0, 0, 0, set()])  # contact-set -> [ways, signed, hh, phases]
    checked = set()
    failures = []
    for sites in walks(nsteps, dim):
        occupied = {p: k for k, p in enumerate(sites)}
        contacts = []
        for i in range(len(sites)):
            for q in _neighbours(sites[i], dim):
                j = occupied.get(q)
                if j is not None and j >= i + 3:
                    contacts.append((i, j))
        hh_contacts = [(i, j) for (i, j) in contacts if seq[i] == 'H' and seq[j] == 'H']
        hh = len(hh_contacts)
        phase = 1
        for (i, j) in hh_contacts:
            loop = contact_loop(sites, i, j)
            ph = loop_phase(loop)
            phase *= 0 if ph is None else ph
        for (i, j) in contacts:
            loop = contact_loop(sites, i, j)
            if len(checked) < zfa_budget and loop not in checked:
                checked.add(loop)
                if not twist_core.is_zfa(loop):
                    failures.append(loop)
        key = tuple(sorted(contacts))
        g = groups[key]
        g[0] += 1
        g[1] += phase
        g[2] = hh
        g[3].add(phase)
    ranked = sorted(groups.items(), key=lambda kv: (-kv[1][2], -kv[1][0]))
    native_hh = ranked[0][1][2]
    native = [k for k, v in ranked if v[2] == native_hh]
    dos = defaultdict(int)
    signed = defaultdict(int)
    for key, v in groups.items():
        dos[v[2]] += v[0]
        signed[v[2]] += v[1]
    dos = {str(k): v for k, v in sorted(dos.items())}
    signed = {str(k): v for k, v in sorted(signed.items())}
    return {"sequence": seq,
            # The phase is very nearly an invariant of the CONTACT SET rather than of the
            # conformation: 1112 of 1113 folds carry one phase across every realization, so
            # |signed| = ways per fold and the class-level cancellation is an artefact of
            # binning different folds together. The single exception is the fold whose only
            # contact spans the whole chain -- the loosest one, and the only one with room for
            # the inversion parity to differ between realizations (Protein_Folding.md 5d).
            "folds_with_mixed_phase": sum(1 for v in groups.values() if len(v[3]) > 1),
            "folds_total": len(groups),
            "conformations": sum(v[0] for v in groups.values()),
            "distinct_contact_sets": len(groups),
            "dos": dos,
            "signed": signed,
            "max_hh_contacts": native_hh,
            "ground_state_conformations": sum(v[0] for k, v in groups.items()
                                              if v[2] == native_hh),
            "ground_state_degeneracy": len(native),
            "unique_ground_state": len(native) == 1,
            "free_energy_nats": -native_hh * math.log(2),
            "folding": thermo(dos),
            "zfa_loops_checked": len(checked),
            "zfa_failures": failures[:5]}


# =============================================================================
# INVARIANTS -- every one of these is a Lean theorem, asserted against fresh data
# =============================================================================
INVARIANTS = [
    "a contact loop achieves ZFA: count-balanced AND Pauli-closed (contact_is_closure)",
    "contacts occur only at odd sequence separation (contact_separation_odd)",
    "a closed loop has even length (closedLoop_even_length)",
    "closed loops compose under concatenation (closedLoop_append)",
    "a count-balanced fold is real, +-I and never +-iI (balanced_phase_is_real)",
    "no gauge twist appears in a backbone encoding (count_encode_plus/minus)",
    "self-avoiding-walk counts match the published lattice series (external check)",
    "fold free energy is -(contacts) x log 2 nats (foldFreeEnergy)",
    "the fold census is mirror-symmetric: counting cannot pick a handedness "
    "(map_mirror_bijective)",
    "the signed census's sign is (-1)^(contacts), a function of the class index "
    "(measured; Protein_Folding.md \u00a75d -- the signed census does no work)",
    "ways is held as a coefficient: the inventory is smaller than the census it summarizes",
]


def _mirror_y(sites):
    return [(x, -y, z) for (x, y, z) in sites]


def check(db, dim=2, nsteps=8):
    """Re-derive every invariant from freshly enumerated data. Returns a list of failures."""
    fails = []

    # I1/I2/I5 -- recorded by saw_census as it enumerates.
    for key, sc in sorted(db.get("saw", {}).items()):
        if sc.get("zfa_failures"):
            fails.append("I1 %s: contact loop is not ZFA: %r" % (key, sc["zfa_failures"]))
        if sc.get("parity_failures"):
            fails.append("I2 %s: even-separation contact: %r" % (key, sc["parity_failures"]))
        if sc.get("phase_failures"):
            fails.append("I5 %s: balanced fold not real: %r" % (key, sc["phase_failures"]))
        for sep in sc["closing"]:
            if int(sep) % 2 == 0:
                fails.append("I2 %s: closures recorded at even separation %s" % (key, sep))
        # I7 -- against the published series.
        series = KNOWN_SAW.get(sc["dim"], [])
        if sc["steps"] < len(series) and sc["walks_total"] != series[sc["steps"]]:
            fails.append("I7 %s: %d walks, published series says %d"
                         % (key, sc["walks_total"], series[sc["steps"]]))

    # I3/I4/I6/I8/I9 -- re-derived here from a fresh enumeration.
    seen_loops = []
    walkset = set()
    hist = defaultdict(int)
    mirror_hist = defaultdict(int)
    for sites in walks(nsteps, dim):
        walkset.add(tuple(sites))
        occupied = {p: k for k, p in enumerate(sites)}
        msites = _mirror_y(sites)
        moccupied = {p: k for k, p in enumerate(msites)}
        for i in range(len(sites)):
            for q in _neighbours(sites[i], dim):
                j = occupied.get(q)
                if j is not None and j >= i + 3:
                    hist[j - i] += 1
                    loop = contact_loop(sites, i, j)
                    if len(seen_loops) < 400:
                        seen_loops.append(loop)
                    if len(loop) % 2 != 0:                       # I3
                        fails.append("I3: closed loop of odd length %r" % loop)
                    if '+' in loop or '-' in loop:               # I6
                        fails.append("I6: gauge twist in a backbone encoding %r" % loop)
            for q in _neighbours(msites[i], dim):
                j = moccupied.get(q)
                if j is not None and j >= i + 3:
                    mirror_hist[j - i] += 1

    if hist != mirror_hist:                                       # I9
        fails.append("I9: the fold census is NOT mirror-symmetric: %r vs %r"
                     % (dict(hist), dict(mirror_hist)))

    for a in seen_loops[:60]:                                     # I4
        for b in seen_loops[:60]:
            if not twist_core.is_zfa(a + b):
                fails.append("I4: concatenation of two closures does not close: %r %r" % (a, b))
                break

    for key, fc in sorted(db.get("folds", {}).items()):           # I8
        want = -fc["max_hh_contacts"] * math.log(2)
        if abs(fc["free_energy_nats"] - want) > 1e-12:
            fails.append("I8 %s: free energy %r is not -(contacts) x log 2 = %r"
                         % (key, fc["free_energy_nats"], want))
        if sum(fc["dos"].values()) != fc["conformations"]:
            fails.append("I8 %s: the density of states does not sum to the conformations" % key)
        for c in fc["dos"]:                                                   # I11
            a = fc["signed"].get(c, 0)
            if a and (a > 0) != (int(c) % 2 == 0):
                fails.append("I11 %s: sign of the signed census at class %s is not (-1)^c"
                             % (key, c))

    # I10 -- ways as a coefficient.
    for name, c in sorted(db.get("closures", {}).items()):
        records = sum(len(v) for v in c["event_classes"].values())
        total_ways = sum(w["ways"] for v in c["event_classes"].values() for w in v.values())
        if records > total_ways:
            fails.append("I10 %s: %d records for %d ways" % (name, records, total_ways))
    return fails


# =============================================================================
# DRIVER
# =============================================================================
DEFAULT_SEQS = {
    # Two 12-residue HP sequences: one designed to fold (a unique maximum-contact
    # structure), one designed not to (a degenerate ground state). The point of the pair
    # is that the SAME rule produces both -- folding is not assumed, it is counted.
    "HPPHPHPHPPHH": "designed folder",
    "HHHHHHHHHHHH": "all-H control -- maximally degenerate",
}


def build(db, saw2=12, saw3=8, do_designability=True, do_folds=True, verbose=True):
    db.setdefault("saw", {})
    db.setdefault("closures", {})

    for dim, upto in ((2, saw2), (3, saw3)):
        for n in range(4, upto + 1):
            key = "dim%d|n%d" % (dim, n)
            if key in db["saw"]:
                continue
            if verbose:
                print("  enumerating %s ..." % key, flush=True)
            db["saw"][key] = saw_census(n, dim)
        top = "dim%d|n%d" % (dim, upto)
        if top in db["saw"]:
            db["closures"]["loopclosure|dim=%d,n=%d" % (dim, upto)] = \
                loop_closure_closure(db["saw"][top])

    if do_folds:
        db.setdefault("folds", {})
        for seq, note in DEFAULT_SEQS.items():
            key = "seq=%s" % seq
            if key in db["folds"]:
                continue
            if verbose:
                print("  folding %s (%s) ..." % (seq, note), flush=True)
            fc = fold_census(seq)
            fc["note"] = note
            db["folds"][key] = fc
            db["closures"]["fold|%s" % key] = fold_closure(fc, weighted=False)
            db["closures"]["foldweighted|%s" % key] = fold_closure(fc, weighted=True)

    if do_designability and "designability" not in db:
        if verbose:
            print("  enumerating the 4x4 compact structures ...", flush=True)
        sets, npaths = hamiltonian_contact_sets()
        contact_sets = [list(k) for k in sorted(sets)]
        if verbose:
            print("    %d Hamiltonian paths -> %d distinct contact sets"
                  % (npaths, len(contact_sets)), flush=True)
            print("  scoring all 2^16 HP sequences ...", flush=True)
        des, folders = designability(contact_sets, n=16)
        db["designability"] = {
            "hamiltonian_paths": npaths,
            "structures": len(contact_sets),
            "sequences_that_fold": folders,
            "max": max(des),
            "mean": sum(des) / len(des),
            "top10": sorted(des, reverse=True)[:10],
            "histogram": {str(k): v for k, v in
                          sorted(defaultdict(int, {d: des.count(d) for d in set(des)}).items())},
        }
        db["closures"]["designability|4x4"] = designability_closure(
            des, contact_sets, folders, npaths)
    return db


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true",
                    help="cheap re-run and assert every invariant (what CI runs)")
    ap.add_argument("--saw-len", type=int, default=12, help="2-D walk census depth")
    ap.add_argument("--saw-len-3d", type=int, default=8, help="3-D walk census depth")
    ap.add_argument("--json", default=DATA_PATH)
    ap.add_argument("--rebuild", action="store_true", help="discard the stored census first")
    args = ap.parse_args()

    db = {}
    if os.path.exists(args.json) and not args.rebuild:
        with open(args.json) as fh:
            db = json.load(fh)

    if args.quick:
        fresh = build({}, saw2=8, saw3=6, do_designability=False, do_folds=False,
                      verbose=False)
        fails = check(fresh, dim=2, nsteps=8)
        fails += check(db, dim=2, nsteps=6)
        for name in ("saw", "closures"):
            if name not in db:
                fails.append("stored census is missing the %r section" % name)
        for key, sc in fresh["saw"].items():
            if key in db.get("saw", {}) and db["saw"][key]["closing"] != sc["closing"]:
                fails.append("%s: stored closure counts differ from a fresh enumeration" % key)
        if fails:
            print("FAILED:")
            for f in fails:
                print("  -", f)
            return 1
        print("protein census OK -- %d invariants asserted against fresh data"
              % len(INVARIANTS))
        return 0

    print("Building the folding census ...")
    db = build(db, saw2=args.saw_len, saw3=args.saw_len_3d)
    db["_comment"] = ("Folding census: a backbone is a twist history, a contact is a ZFA "
                      "closure. Rebuild with protein_census.py. The `closures` section is "
                      "the shared inventory schema that qucalc/src/lib.rs loads.")
    db["_invariants_asserted"] = INVARIANTS
    db["hydrophobicity"] = hydrophobicity_check()

    fails = check(db, dim=2, nsteps=8)
    if fails:
        print("FAILED:")
        for f in fails:
            print("  -", f)
        return 1

    os.makedirs(os.path.dirname(args.json), exist_ok=True)
    with open(args.json, "w") as fh:
        json.dump(db, fh, indent=1, sort_keys=True)
    print("wrote %s" % args.json)
    report(db)
    return 0


def report(db):
    print("\n== loop closure: how many ways a loop of span l closes ==")
    for key in sorted(db["saw"]):
        sc = db["saw"][key]
        if sc["steps"] not in (8, 12) and sc["dim"] == 2:
            continue
        probs = [(int(k), sc["closing"][k] / sc["opportunities"][k]) for k in sc["closing"]]
        probs.sort()
        line = "  %-12s " % key + "  ".join("l=%d:%.4f" % (l, p) for l, p in probs[:6])
        print(line)
    print("\n== designability (4x4, all 2^16 HP sequences) ==")
    d = db.get("designability", {})
    if d:
        print("  %d structures, %d sequences fold uniquely (%.1f%%), max designability %d"
              % (d["structures"], d["sequences_that_fold"],
                 100.0 * d["sequences_that_fold"] / 65536, d["max"]))
        print("  top ten designabilities: %s" % d["top10"])
    print("\n== hydrophobicity from the valence rule ==")
    h = db.get("hydrophobicity", {})
    if h:
        print("  %d/%d agree with the sign of Kyte-Doolittle; misses: %s"
              % (h["agree"], h["total"], ", ".join(h["misses"])))


if __name__ == "__main__":
    sys.exit(main())
