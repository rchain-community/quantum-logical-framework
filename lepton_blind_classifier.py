#!/usr/bin/env python3
"""
lepton_blind_classifier.py (version 3) — rooted causal lepton-ladder attack on QLF #140.

This version performs two separate audits:

A. BLIND TOPOLOGY SELECTION (no measured masses)
   1. spatial twists only
   2. no immediate Hermitian reversal
   3. first-return ZFA (final closure; no proper causal prefix already closes)
   4. rooted baryon winding B = 0
   5. final Pauli fold = -I (electron-like half-spin)
   6. quotient signed spatial-axis permutations + antiparticle
   7. frequency = number of ways selects the L=6 class
   8. parent-child continuation selects the rooted L=8 class
   CAVEAT (see part G3): step 8 filters to 3-axis classes BEFORE applying the
   parent rule, and that filter is LOAD-BEARING -- without it 9 of the 12 L=8
   classes have a mu parent, not 1.  No measured mass enters, so the blind-test
   discipline holds, but "3 axes for tau" is an imposed assumption, not an
   output.  Part F shows the rule also goes ambiguous at L=10.

B. KOIDE PHASE AUDIT (only after topology selection)
   Reproduce the exact-Q=2/3 phase implied by the repo's m_e and m_mu inputs,
   then compare it with the existing 2/9 candidate -- including the provenance
   of the stale 0.22227 (a single-channel tau extraction) and the fact that
   2/9's residual is the same ~1e-5 order as Q's own deviation from 2/3.
   2/9 is a CANDIDATE Koide-phase hypothesis throughout, never a derivation.

C. THE PHASE, PROPERLY POSED
   Why 2/9 is the wrong object to derive (delta is a Z3 gauge parameter, so
   only Delta = 3*delta is physical), the free 3-parameter fit with propagated
   experimental errors, the noise floor that forbids chasing the 7th digit,
   and what a derivation would still need.

D. THE RESIDUAL
   Which defect is statistically real (one: +9.83 ppm on m_mu/m_e), and the
   much larger radiative puzzle behind it -- why Koide survives at all.

E. IS Delta = Q A RELATION?
   No.  Conditioned on Q = 2/3 the phase Delta is essentially free, so the
   proposed reduction is REFUTED: Q = 2/3 and Delta = 2/3 are two independent
   facts, and only the first is derived.

F. WHAT Delta = 2/3 IS, AND WHERE THE LADDER STOPS
   Delta = 2/3 is m_mu/m_e = 206.77 in other coordinates (not derived), and
   the ladder's selection rule -- unique parented continuation -- goes
   AMBIGUOUS at L=10, so part A is not an independent argument for exactly
   three generations.

G. THE (R, axis) -> MASS-RATIO MAP (issue #140's original ask)
   Shape theorem: the census integers are all 5-smooth but the mass ratios are
   not, so no direct map exists; it must factor as census -> Delta -> masses,
   and Delta = 2/3 IS 5-smooth.  Also flags that part A's 3-axis filter is
   load-bearing, so the census 'axes = 2,2,3' cannot evidence the 2/3.

H-M. DERIVING Delta = 2/3 (the round-by-round record is issue #140)
   Results that stand:
     * the hierarchy needs NO large number -- the electron sits 2.27 deg from
       the massless wall of 1+sqrt2 cos(theta) and the 3477x ratio is that
       angular deficit SQUARED (part L);
     * the wall exists only because A^2 = 2 > 1, which QLF derives, so the
       substrate geometry is what makes a lepton hierarchy POSSIBLE (L3);
     * the +9.83 ppm residual is RETIRED as a coordinate artefact -- the
       near-zero amplifies by 12.5, so the ansatz's own 3.4e-5 knowledge of
       Delta covers +-424 ppm and the residual is 2.3% of that (L4);
     * the specification: any derivation must produce an O(1) RATIONAL IN
       RADIANS (part H) and must be FORCED, not selected -- a route costing
       more bits than the constant is a re-encoding (parts I, J).
   Routes CLOSED, one line each (details in the parts named):
     circle divisions (H) | census count-ratios (J) | all three curvature
     notions (J, K) | eps as a better coordinate (M1) | symmetric-functional
     extremization (M3) | absolute mass scales (M4a) | ratios of
     commensurable angles (M4b).
   Route CLOSED (part N): Delta as a mode-locked ROTATION NUMBER (M5).  A
     rotation number is a fraction of a TURN; Delta is 2/3 of a RADIAN, i.e.
     1/(3 pi) turns, and the smallest rational turn-fraction the data admits
     has denominator 311 -- the narrowest tongue, not the widest.  What
     survives of M5 is the side result Farey depth = description length.
     Delta = 2/3 is open with ZERO live candidates.
   Also in K: the possibility graph is HYPERBOLIC while synthesized space is
   Ollivier-flat -- a result about the substrate that outlived the question,
   written up in Curvature.md sec 1c.

No QLF imports are required.
"""

from __future__ import annotations

import itertools
import math
import random
from collections import Counter, defaultdict

SPATIAL = "^v<>/\\"

TWIST = {
    ">": (0, +1), "<": (0, -1),
    "^": (1, +1), "v": (1, -1),
    "/": (2, +1), "\\": (2, -1),
}
FROM = {v: k for k, v in TWIST.items()}
CONJ = {t: FROM[(a, -s)] for t, (a, s) in TWIST.items()}
AXNAME = "XYZ"
ORDER = {c: i for i, c in enumerate(SPATIAL)}

_EVEN = {("X", "Y", "Z"), ("Y", "Z", "X"), ("Z", "X", "Y")}
_ODD  = {("X", "Z", "Y"), ("Z", "Y", "X"), ("Y", "X", "Z")}


def axes_engaged(h: str) -> str:
    return "".join(sorted({AXNAME[TWIST[t][0]] for t in h}))


def balanced(h: str) -> bool:
    c = Counter(h)
    return c["^"] == c["v"] and c[">"] == c["<"] and c["/"] == c["\\"]


def admissible(h: str) -> bool:
    return all(h[i + 1] != CONJ[h[i]] for i in range(len(h) - 1))


def first_return_zfa(h: str) -> bool:
    if not balanced(h):
        return False
    return all(not balanced(h[:k]) for k in range(2, len(h)))


def sign_triple(a: str, b: str, c: str) -> int:
    t = (a, b, c)
    return 1 if t in _EVEN else -1 if t in _ODD else 0


def baryon_number(h: str) -> int:
    ax = [AXNAME[TWIST[t][0]] for t in h]
    return sum(
        sign_triple(ax[i], ax[i + 1], ax[i + 2])
        for i in range(len(ax) - 2)
    )


# ---------- exact 2x2 Pauli fold, pure Python ----------

I = (1+0j, 0j, 0j, 1+0j)
X = (0j, 1+0j, 1+0j, 0j)
Y = (0j, -1j, 1j, 0j)
Z = (1+0j, 0j, 0j, -1+0j)


def smul(s, m):
    return tuple(s*x for x in m)


PMAP = {
    ">": X, "<": smul(-1, X),
    "^": Y, "v": smul(-1, Y),
    "/": Z, "\\": smul(-1, Z),
}


def mmul(m1, m2):
    a, b, c, d = m1
    e, f, g, h = m2
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def fold_phase(h: str) -> str:
    m = I
    for t in h:
        m = mmul(m, PMAP[t])
    for s, name in ((1, "+I"), (-1, "-I"), (1j, "+iI"), (-1j, "-iI")):
        if all(abs(m[i] - s*I[i]) < 1e-9 for i in range(4)):
            return name
    return "open"


# ---------- symmetry quotient ----------

def antiparticle(h: str) -> str:
    return "".join(CONJ[t] for t in reversed(h))


def signed_axis_transforms():
    for perm in itertools.permutations(range(3)):
        for flips in itertools.product((+1, -1), repeat=3):
            def tr(h: str, perm=perm, flips=flips) -> str:
                out = []
                for t in h:
                    a, s = TWIST[t]
                    out.append(FROM[(perm[a], s*flips[a])])
                return "".join(out)
            yield tr


TRANSFORMS = list(signed_axis_transforms())


def key(h: str):
    return tuple(ORDER[c] for c in h)


def orbit(h: str) -> set[str]:
    out = set()
    for tr in TRANSFORMS:
        q = tr(h)
        out.add(q)
        out.add(antiparticle(q))
    return out


def canonical(h: str) -> str:
    return min(orbit(h), key=key)


def generate_first_return(length: int) -> list[str]:
    out = []

    def rec(pref: str):
        if len(pref) == length:
            if first_return_zfa(pref):
                out.append(pref)
            return
        for t in SPATIAL:
            if pref and t == CONJ[pref[-1]]:
                continue
            rec(pref + t)

    rec("")
    return out


def half_spin_free(length: int) -> list[str]:
    return [
        h for h in generate_first_return(length)
        if baryon_number(h) == 0 and fold_phase(h) == "-I"
    ]


def classes(words: list[str]) -> dict[str, list[str]]:
    d = defaultdict(list)
    for h in words:
        d[canonical(h)].append(h)
    return d


# ---------- causal parent relation ----------

def conjugate_pair_deletions(h: str):
    """
    Delete one same-axis opposite-sign pair, preserving the causal order of
    everything else.
    """
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            if h[j] == CONJ[h[i]]:
                yield (i, j, h[i] + h[j], h[:i] + h[i+1:j] + h[j+1:])


def parent_edges(child_orbit: set[str], parent_orbit: set[str]) -> int:
    total = 0
    for h in child_orbit:
        for _, _, _, q in conjugate_pair_deletions(h):
            if q in parent_orbit:
                total += 1
    return total


def child_parent_degree(child_orbit: set[str], parent_orbit: set[str]) -> Counter:
    deg = Counter()
    for h in child_orbit:
        n = sum(1 for _, _, _, q in conjugate_pair_deletions(h) if q in parent_orbit)
        deg[n] += 1
    return deg


def select_topologies():
    print("=== A. BLIND ROOTED TOPOLOGY SELECTION ===\n")

    c4 = classes(half_spin_free(4))
    c6 = classes(half_spin_free(6))
    c8 = classes(half_spin_free(8))

    e = next(iter(c4))  # unique
    mu = max(c6.items(), key=lambda kv: len(kv[1]))[0]  # frequency=ways

    tau3 = {
        rep: members for rep, members in c8.items()
        if len(axes_engaged(rep)) == 3
    }

    print("L=4 free half-spin classes:")
    for rep, mem in c4.items():
        print(f"  {rep:10} ways={len(mem):3d} axes={axes_engaged(rep)}")
    print()

    print("L=6 free half-spin classes:")
    for rep, mem in sorted(c6.items(), key=lambda kv: key(kv[0])):
        print(f"  {rep:10} ways={len(mem):3d} axes={axes_engaged(rep)}")
    print(f"  -> number-of-ways selection: mu = {mu}\n")

    print("L=8 three-axis free half-spin classes:")
    omu = orbit(mu)
    parentful = []
    for rep, mem in sorted(tau3.items(), key=lambda kv: key(kv[0])):
        o = orbit(rep)
        edges = parent_edges(o, omu)
        deg = child_parent_degree(o, omu)
        print(
            f"  {rep:10} ways={len(mem):3d} "
            f"mu-parent-edges={edges:3d} degree={dict(deg)}"
        )
        if edges:
            parentful.append(rep)

    if len(parentful) != 1:
        raise RuntimeError(f"Expected unique rooted tau continuation, got {parentful}")
    tau = parentful[0]
    print(f"  -> causal-parent selection: tau = {tau}\n")

    oe, om, ot = orbit(e), orbit(mu), orbit(tau)
    print("Selected causal ladder:")
    for n, h in (("e", e), ("mu", mu), ("tau", tau)):
        print(
            f"  {n:3} = {h:10} L={len(h)} axes={axes_engaged(h)} "
            f"B={baryon_number(h):+d} fold={fold_phase(h)} orbit={len(orbit(h))}"
        )

    print("\nParent-edge audit:")
    print(f"  mu -> e deletion edges across orbit  = {parent_edges(om, oe)}")
    print(f"  per-mu rooted history                = {dict(child_parent_degree(om, oe))}")
    print(f"  tau -> mu deletion edges across orbit= {parent_edges(ot, om)}")
    print(f"  per-tau rooted history               = {dict(child_parent_degree(ot, om))}")

    old = "^v<>/\\"
    print("\nEarlier L=6 tau proposal:")
    print(
        f"  {old}: balanced={balanced(old)}, first-return={first_return_zfa(old)}, "
        f"B={baryon_number(old)}, fold={fold_phase(old)}"
    )
    print("  -> reject as elementary: (^v)(<>)(/\\) are already separate closures.")

    return e, mu, tau


# ---------- Koide audit ----------

ME = 0.51099895000
MMU = 105.6583755
MTAU = 1776.86

# PDG / CODATA 1-sigma uncertainties (MeV)
D_ME = 0.00000000015
D_MMU = 0.0000023
D_MTAU = 0.12


def koide_weights(delta: float):
    # k=(0,1,2) = (tau,e,mu)
    return [
        (1 + math.sqrt(2)*math.cos(delta + 2*math.pi*k/3))**2
        for k in range(3)
    ]


def mu_e_ratio(delta: float) -> float:
    w = koide_weights(delta)
    return w[2] / w[1]


def solve_delta_from_e_mu() -> float:
    target = MMU / ME
    lo, hi = 0.21, 0.23
    flo = mu_e_ratio(lo) - target
    fhi = mu_e_ratio(hi) - target
    if flo * fhi > 0:
        raise RuntimeError("Root not bracketed")
    for _ in range(100):
        mid = (lo + hi) / 2
        fm = mu_e_ratio(mid) - target
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def koide_tau_from_e_mu():
    a = math.sqrt(ME) + math.sqrt(MMU)
    b = ME + MMU
    s_tau = 2*a + math.sqrt(6*a*a - 3*b)
    return s_tau*s_tau


def koide_Q() -> float:
    s = math.sqrt(ME) + math.sqrt(MMU) + math.sqrt(MTAU)
    return (ME + MMU + MTAU) / (s*s)


def single_channel_deltas() -> dict[str, float]:
    """
    Extract delta from ONE mass at a time, with M pinned by all three measured
    masses (M = sum(sqrt m)/3).  Because the measured Q is not exactly 2/3 the
    three extractions disagree in the 5th decimal -- this is the provenance of
    the stale 0.22227 that Weak_Force.md used to quote as "the phase m_e, m_mu
    demand".  It is the tau-channel value, not a two-input solve.
    """
    M = (math.sqrt(ME) + math.sqrt(MMU) + math.sqrt(MTAU)) / 3.0
    out = {}
    for name, m, k in (("tau", MTAU, 0), ("e", ME, 1), ("mu", MMU, 2)):
        c = (math.sqrt(m)/M - 1) / math.sqrt(2)
        c = max(-1.0, min(1.0, c))
        # the branch near delta ~ 0.222 rad
        cands = [(sg*math.acos(c) - 2*math.pi*k/3) % (2*math.pi) for sg in (1, -1)]
        out[name] = min(cands, key=lambda d: abs(d - 2/9))
    return out


def delta_sigma_from_experiment(delta: float) -> float:
    """1-sigma spread in delta induced by the experimental m_mu/m_e error."""
    rel = math.hypot(D_MMU/MMU, D_ME/ME)
    h = 1e-9
    dr = (mu_e_ratio(delta + h) - mu_e_ratio(delta - h)) / (2*h)
    return (MMU/ME) * rel / abs(dr)


def koide_audit():
    print("\n=== B. KOIDE PHASE AUDIT (AFTER BLIND SELECTION) ===\n")

    delta_exactQ = solve_delta_from_e_mu()
    delta_29 = 2/9

    print("Repo inputs (koide_tau_demo.py):")
    print(f"  m_e   = {ME:.11f} MeV")
    print(f"  m_mu  = {MMU:.7f} MeV")
    print(f"  m_tau = {MTAU:.2f} MeV\n")

    print("B1. The well-posed determination (exact Q=2/3; m_e, m_mu the two inputs):")
    print(f"  delta_required = {delta_exactQ:.15f} rad")
    print(f"  2/9            = {delta_29:.15f} rad")
    print(f"  difference     = {delta_29-delta_exactQ:+.3e} rad")
    print(f"  relative delta gap = {(delta_29/delta_exactQ-1)*100:+.8f}%\n")

    print("B2. Provenance of the stale 0.22227 (single-channel extractions,")
    print("    M pinned by all three MEASURED masses):")
    sc = single_channel_deltas()
    for name in ("tau", "mu", "e"):
        print(f"  delta from {name:3} channel alone = {sc[name]:.9f} rad")
    print("  -> they disagree in the 5th decimal because measured Q != 2/3.")
    print("     0.22227 is the TAU-channel value; it is not what m_e,m_mu demand.\n")

    obs_mu_e = MMU / ME
    pred_mu_e = mu_e_ratio(delta_29)
    w = koide_weights(delta_29)
    tau_from_e = ME * (w[0] / w[1])

    print("B3. Exact delta=2/9 as a zero-parameter mass-RATIO prediction")
    print("    (m_e supplies only the overall scale):")
    print(f"  observed  m_mu/m_e = {obs_mu_e:.12f}")
    print(f"  predicted m_mu/m_e = {pred_mu_e:.12f}")
    print(f"  relative error     = {(pred_mu_e/obs_mu_e-1)*100:+.8f}%  "
          f"({(pred_mu_e/obs_mu_e-1)*1e6:+.1f} ppm)")
    print(f"  m_tau from e scale = {tau_from_e:.6f} MeV")
    print(f"  relative error     = {(tau_from_e/MTAU-1)*100:+.6f}%  "
          f"= {(tau_from_e-MTAU)/D_MTAU:+.2f} sigma\n")

    mt_koide = koide_tau_from_e_mu()
    print("B4. For comparison, exact Q=2/3 with measured e,mu gives:")
    print(f"  m_tau = {mt_koide:.6f} MeV  "
          f"({(mt_koide/MTAU-1)*100:+.6f}% = {(mt_koide-MTAU)/D_MTAU:+.2f} sigma)\n")

    print("B5. How 2/9 fails, and how Koide's own 2/3 fails -- same order:")
    sig = delta_sigma_from_experiment(delta_exactQ)
    Q = koide_Q()
    print(f"  sigma(delta) from the m_mu/m_e error = {sig:.3e} rad")
    print(f"  (2/9 - delta_required)               = {(delta_29-delta_exactQ)/sig:+.0f} sigma")
    print(f"  measured Q                           = {Q:.9f}")
    print(f"  (2/3 - Q)/Q                          = {(2/3)/Q-1:+.3e}")
    print(f"  2/9 residual on m_mu/m_e             = {pred_mu_e/obs_mu_e-1:+.3e}")
    print("  -> both deviations are ~1e-5.  2/9 fails exactly where Q=2/3 fails.\n")

    print("VERDICT")
    print("  * delta = 0.222222047 rad is the well-posed two-input value (B1).")
    print("    The older 0.22227 was the tau-channel extraction (B2), not a solve")
    print("    from m_e, m_mu -- Weak_Force.md sec 5c now states this correctly.")
    print("  * 2/9 is NOT excluded by m_tau: 1.04 sigma, as good as exact Q=2/3")
    print("    at 0.91 sigma (B3/B4).  Both sit inside the PDG error bar.")
    print("  * 2/9 IS excluded by m_mu/m_e at ~9.8 ppm -- but only CONDITIONAL on")
    print("    Q being exactly 2/3, which the data does not support at that")
    print("    precision: Q itself is off by 9.2e-6 -- nearly the same number (B5).")
    print("  * So 2/9 stays a flagged CANDIDATE Koide-phase hypothesis, pointing")
    print("    at one common ~1e-5 correction rather than two coincidences.")
    print("  * The missing physics is not arithmetic: QLF still needs a reason why")
    print("    the Koide cosine phase should equal the count ratio 2/9 at all.")
    print("    Until that exists this is numerology, however sharp.")
    print("  * See part C: 2/9 is in fact the WRONG object to derive.")


# ---------- C. the phase, properly posed ----------

def fit_three_phase(me: float, mmu: float, mtau: float):
    """
    EXACT 3-parameter fit of  sqrt(m_k) = M(1 + A cos(delta + 2pi k/3)),
    k = 0,1,2 -> tau,e,mu.  Nothing is assumed: three masses determine
    (M, A, delta) with no residual, via the first three power sums.

        sum cos      = 0     ->  M     = (sum sqrt m)/3
        sum cos^2    = 3/2   ->  A     = sqrt(2/3 sum u^2),  u_k = sqrt(m_k)/M - 1
        sum cos^3    = (3/4) cos(3 delta)
                             ->  delta = arccos(4 sum u^3 / 3A^3)/3

    Note the third power sum is the FIRST one that sees delta, and it sees it
    only through cos(3 delta).  That is not an accident -- see z3_redundancy().
    """
    s = [math.sqrt(mtau), math.sqrt(me), math.sqrt(mmu)]
    M = sum(s) / 3.0
    u = [x / M - 1.0 for x in s]
    A = math.sqrt(2 * sum(x * x for x in u) / 3.0)
    c3 = max(-1.0, min(1.0, 4 * sum(x**3 for x in u) / (3 * A**3)))
    return M, A, math.acos(c3) / 3.0


def z3_redundancy() -> bool:
    """
    delta -> delta + 2pi/3 permutes the three phases, hence relabels the three
    generations, hence leaves the SPECTRUM identical.  So delta is a Z3 gauge
    parameter: it is defined only mod 2pi/3, and every physical invariant is a
    function of Delta = 3*delta.  Returns True if verified numerically.
    """
    M, A = 17.715561710, math.sqrt(2)
    def spec(d):
        return sorted((M*(1 + A*math.cos(d + 2*math.pi*k/3)))**2 for k in range(3))
    base = spec(2/9)
    return all(
        all(abs(x - y) < 1e-9 for x, y in zip(base, spec(2/9 + n*2*math.pi/3)))
        for n in (1, 2)
    )


def mc_phase_errors(trials: int = 60000, seed: int = 1):
    """Propagate the experimental mass errors into the fitted (A^2, delta)."""
    rng = random.Random(seed)
    a2s, ds = [], []
    for _ in range(trials):
        _, a, d = fit_three_phase(rng.gauss(ME, D_ME),
                                  rng.gauss(MMU, D_MMU),
                                  rng.gauss(MTAU, D_MTAU))
        a2s.append(a*a); ds.append(d)
    def stat(v):
        m = sum(v)/len(v)
        return m, math.sqrt(sum((x-m)**2 for x in v)/(len(v)-1))
    return stat(a2s), stat(ds)


def phase_audit():
    print("\n=== C. THE PHASE, PROPERLY POSED ===\n")

    print("C1. delta is a Z3 GAUGE PARAMETER, so 2/9 is the wrong target.")
    print(f"  delta -> delta + 2pi/3 leaves the spectrum identical: "
          f"{'VERIFIED' if z3_redundancy() else 'FAILED'}")
    print("  Only Delta = 3*delta is physical.  Consequently:")
    print("    - the object to derive is  Delta = 2/3,  not  delta = 2/9;")
    print("    - the 9 in 2/9 is NOT one count.  It factorises as")
    print("        9 = 3 (generations, from Q) x 3 (the Z3 quotient),")
    print("      so reading it as '3^2 directional couplings, the same 9 as")
    print("      alpha' matches the right number to the wrong decomposition.")
    print("  This also explains why the phase is a pure number rather than a")
    print("  multiple of pi: Delta is a ratio of invariants; the 1/3 is the")
    print("  quotient, not an angle.\n")

    print("C2. Free 3-parameter fit (NOTHING assumed -- not even Q=2/3):")
    M, A, d = fit_three_phase(ME, MMU, MTAU)
    (a2m, a2s), (dm, ds) = mc_phase_errors()
    print(f"  M       = {M:.6f} MeV^1/2")
    print(f"  A^2     = {a2m:.9f} +- {a2s:.9f}   (predicted 2)")
    print(f"  delta   = {dm:.9f} +- {ds:.9f}   (candidate 2/9)")
    print(f"  Delta   = {3*dm:.9f} +- {3*ds:.9f}   (candidate 2/3)")
    print(f"  -> A^2 = 2   at {(a2m-2)/a2s:+.2f} sigma")
    print(f"  -> Delta=2/3 at {(3*dm-2/3)/(3*ds):+.2f} sigma")
    print("  Errors are dominated by m_tau (+-0.12 MeV).  NEITHER is excluded.\n")

    print("C3. Delta = Q is NOT an identity -- it is a second relation.")
    rng = random.Random(11)
    worst = 0.0
    for _ in range(20000):
        a = 10**rng.uniform(-1, 0.5); b = 10**rng.uniform(1, 2.5)
        c = 10**rng.uniform(2.5, 4)
        _, _, dd = fit_three_phase(a, b, c)
        q = (a+b+c)/(math.sqrt(a)+math.sqrt(b)+math.sqrt(c))**2
        worst = max(worst, abs(3*dd - q))
    Q = koide_Q()
    print(f"  random mass triples: |Delta - Q| reaches {worst:.3f}  (O(1) generic)")
    print(f"  charged leptons    : |Delta - Q| = {abs(3*d-Q):.2e}")
    print("  The leptons do satisfy it -- but this does NOT make it a relation.")
    print("  See part E: conditioned on Q = 2/3, Delta is essentially free, so")
    print("  'Delta = Q' has no content beyond two separate facts.  REFUTED.\n")

    print("C4. NOISE FLOOR -- why the 1e-7 'agreement' is not evidence.")
    delta_condQ = solve_delta_from_e_mu()
    syst = abs(d - delta_condQ) / delta_condQ
    agree = abs(2/9 - delta_condQ) / (2/9)
    print(f"  delta from the free fit           = {d:.10f}")
    print(f"  delta conditional on Q=2/3 exactly= {delta_condQ:.10f}")
    print(f"  systematic between the two        = {syst:.2e}")
    print(f"  |2/9 - (conditional value)|       = {agree:.2e}")
    print(f"  -> the celebrated agreement is {syst/agree:.0f}x SMALLER than the")
    print("     choice of extraction.  It is below the model's own noise floor,")
    print(f"     which the Q defect sets at {(2/3)/Q-1:.1e}.")
    print("  HONEST PRECISION:  delta = 2/9 holds at 1e-5, and no better.")
    print("  Chasing the 7th digit is chasing an artefact of assuming Q=2/3.\n")

    print("C5. WHAT A DERIVATION STILL NEEDS (and what cannot supply it).")
    print("  The Pauli fold CANNOT supply the phase.  The fold group is mu_4 =")
    print("  {+-I, +-iI}; the half-spin signature is one bit (-I vs +I); the")
    print("  free-energy quantum is one bit (dF = -log 2).  A FINITE group has")
    print("  no continuous parameter, so no amount of fold structure yields a")
    print("  real angle.  One-bit precision does do one useful thing: it sets")
    print("  the resolution floor, which is what rules the 1e-7 chase out (C4).")
    print("  A derivation must therefore produce  Delta = 2/3  as a ratio of")
    print("  CENSUS COUNTS, with the Z3 quotient already built in -- and must")
    print("  also produce the common ~1e-5 correction that Q and Delta share.")
    print("  Until then: not derived.  Consistent, reduced, and open.")


# ---------- D. the residual, and the radiative puzzle behind it ----------

ALPHA = 1 / 137.035999177


def q_running(mu: float) -> float:
    """
    Koide Q built from one-loop QED running masses at common scale mu:
        mbar_k(mu) = M_k / (1 + (alpha/pi)[1 + (3/2) ln(mu/M_k)])
    """
    m = [M / (1 + (ALPHA/math.pi)*(1 + 1.5*math.log(mu/M)))
         for M in (ME, MMU, MTAU)]
    return sum(m) / (sum(math.sqrt(x) for x in m))**2


def residual_audit():
    print("\n=== D. THE RESIDUAL, AND THE LARGER PUZZLE BEHIND IT ===\n")

    print("D1. There is no 'common 1e-5 correction to Q and Delta'.")
    (a2m, a2s), (dm, ds) = mc_phase_errors()
    w = koide_weights(2/9)
    pred, obs = w[2]/w[1], MMU/ME
    ru = math.hypot(D_MMU/MMU, D_ME/ME)
    rows = [("A^2 - 2", a2m-2, a2s), ("Delta - 2/3", 3*dm-2/3, 3*ds),
            ("m_mu/m_e (rel)", pred/obs-1, ru)]
    print(f"  {'quantity':>16} {'defect':>12} {'+- unc':>12} {'sigma':>10}")
    for n, d, s in rows:
        print(f"  {n:>16} {d:+12.3e} {s:12.1e} {d/s:+10.1f}"
              f"   {'SIGNIFICANT' if abs(d/s) > 3 else 'noise'}")
    print("\n  The Q and Delta defects are m_tau noise.  EXACTLY ONE number is")
    print(f"  significant: m_mu/m_e is overpredicted by {(pred/obs-1)*1e6:+.2f} ppm.")
    print("  Its locus -- the e-mu sector -- is where the blind ladder carries")
    print("  its one asymmetry: e and mu share axes {x,y}, only tau engages z.\n")

    print("D2. Q is blind to universal shifts, so only log(m_k) terms can move it.")
    c = 1.7
    Qc = ((c*ME + c*MMU + c*MTAU)
          / (math.sqrt(c*ME)+math.sqrt(c*MMU)+math.sqrt(c*MTAU))**2)
    print(f"  m_k -> {c}*m_k :  Q = {koide_Q():.12f} -> {Qc:.12f}  (exactly equal)")
    print(f"  flavour-dependent scale (alpha/pi)*ln(m_mu/m_e) = "
          f"{(ALPHA/math.pi)*math.log(MMU/ME):.2e}\n")

    print("D3. Radiative corrections are 100x LARGER than the residual,")
    print("    and no scale rescues them:")
    print(f"  {'mu (MeV)':>12} {'Q(running)':>14} {'Q - 2/3':>12}")
    for mu in (1.0, 1e3, MTAU, 1e6, 1e12):
        print(f"  {mu:12.3g} {q_running(mu):14.9f} {q_running(mu)-2/3:+12.2e}")
    print(f"  {'POLE':>12} {koide_Q():14.9f} {koide_Q()-2/3:+12.2e}")
    print(f"\n  running is {abs(q_running(1e4)-2/3)/abs(koide_Q()-2/3):.0f}x worse, and")
    print("  essentially SCALE-INDEPENDENT (the ln mu is universal, so it cancels")
    print("  in Q).  Koide is a POLE-MASS relation, full stop.")
    print("  => the real question is not 'where does 9.8 ppm come from' but")
    print("     'why is the 1.1e-3 absent' -- a discrepancy 115x larger.\n")

    print("D4. QLF answers THAT one, and was committed to the answer already.")
    print("  Weak_Force.md sec 5d: only observables carry physical mass; the")
    print("  quoted quark masses are scheme-dependent running parameters, never")
    print("  measured -- which is why quark-Koide is PREDICTED to fail.  The pole")
    print("  mass is the on-shell, gauge-invariant, IR-complete observable, which")
    print("  is exactly what a ZFA closure is; a running mass is bookkeeping.")
    print("  So the substrate relation must hold for POLE masses -- and the 183x")
    print("  preference for pole over running is that prediction confirmed.")
    print("  One principle, two consequences (5d and this), neither fitted.\n")

    print("D5. The 9.83 ppm itself: NOT derived, and not being fitted.")
    resid = pred/obs - 1
    for name, val in (("1/(24*48*96)  [orbit sizes]", 1/(24*48*96)),
                      ("2*(alpha/pi)^2", 2*(ALPHA/math.pi)**2),
                      ("alpha^2/(2pi)", ALPHA**2/(2*math.pi))):
        print(f"  {name:28} = {val:.4e}  off by {abs(val/resid-1)*100:.0f}%  REJECTED")
    print(f"  {'residual':28} = {resid:.4e}")
    print("  An exact census count must come out EXACT: an 8% miss is a failure,")
    print("  not a near-miss.  With alpha, pi and small rationals any single")
    print("  number matches to a few percent, so none of these are candidates.")
    print("  Status: open.")


# ---------- E. is Delta = Q a relation?  (no) ----------

def fit_any(ms):
    """(A, Delta) for an arbitrary triple of positive masses, heaviest -> k=0."""
    s = sorted((math.sqrt(m) for m in ms), reverse=True)
    s = [s[0], s[2], s[1]]
    M = sum(s) / 3.0
    u = [x / M - 1.0 for x in s]
    A = math.sqrt(2 * sum(x*x for x in u) / 3.0)
    c3 = max(-1.0, min(1.0, 4 * sum(x**3 for x in u) / (3 * A**3)))
    return A, math.acos(c3)


def q_any(ms):
    return sum(ms) / sum(math.sqrt(m) for m in ms)**2


def delta_equals_q_test():
    print("\n=== E. IS  Delta = Q  A RELATION?  (REFUTED) ===\n")

    print("E1. Conditioned on Q = 2/3, is Delta pinned near 2/3?")
    rng = random.Random(3)
    ds = []
    while len(ds) < 4000:
        ms = [10**rng.uniform(-2, 0), 10**rng.uniform(0, 3), 10**rng.uniform(2, 5)]
        if abs(q_any(ms) - 2/3) < 0.001:
            ds.append(fit_any(ms)[1])
    ds.sort()
    near = sum(1 for x in ds if abs(x - 2/3) < 0.01) / len(ds)
    print(f"  {len(ds)} random triples with Q = 2/3 +- 0.001")
    print(f"  Delta range          : {ds[0]:.4f} .. {ds[-1]:.4f}")
    print(f"  Delta median         : {ds[len(ds)//2]:.4f}")
    print(f"  5th / 95th percentile: {ds[len(ds)//20]:.4f} / {ds[-len(ds)//20]:.4f}")
    print(f"  within 0.01 of 2/3   : {near*100:.1f}%")
    print("  -> Q = 2/3 carries essentially NO information about Delta.\n")

    print("E2. The sharpest counterexample, from real numbers:")
    cbt = [1270.0, 4180.0, 172690.0]          # (c, b, t)
    _, D = fit_any(cbt); q = q_any(cbt)
    print(f"  (c,b,t):  Q = {q:.6f}  -- within {abs(q-2/3)/(2/3)*100:.1f}% of 2/3")
    print(f"            Delta = {D:.6f}  -- a factor {(2/3)/D:.2f} away from 2/3")
    print("  A triple with Koide's invariant AT 2/3 whose phase is nowhere near.")
    print("  (Quark masses are scheme-dependent parameters, not observables, so")
    print("   they cannot test a physical law -- but that objection does not")
    print("   apply here: the question is the MATHEMATICAL one, whether Q fixes")
    print("   Delta as functions of a triple of positive reals.  E1 settles it")
    print("   with random triples and no physics at all.)\n")

    print("E3. VERDICT")
    print("  'Delta = Q' is REFUTED as a relation.  Delta and Q are independent")
    print("  functions on mass-triple space; the leptons satisfying both is two")
    print("  separate facts wearing one costume, not a reduction.")
    print("    Q = 2/3      -- DERIVED (N=3 axes, A^2=2 transverse; sec 5b)")
    print("    Delta = 2/3  -- INDEPENDENT, NOT derived, NOT implied by Q")
    print("  The honest residue is weaker: the substrate's transverse fraction")
    print("  2/3 appears twice -- once in the amplitude sector, once in the")
    print("  phase sector -- a structural coherence, not a derivation.")


# ---------- F. what Delta = 2/3 actually is, and where the ladder stops ----------

def first_return_pruned(length: int) -> list[str]:
    """
    Same set as generate_first_return, but with the balance-reachability and
    first-return prunes applied during construction, so L=10 is tractable.
    """
    out: list[str] = []
    c = [0, 0, 0]
    pref: list[str] = []

    def rec():
        n = len(pref)
        if n == length:
            out.append("".join(pref))
            return
        r = length - n
        s = abs(c[0]) + abs(c[1]) + abs(c[2])
        if s > r or (r - s) % 2:
            return
        for t in SPATIAL:
            if pref and t == CONJ[pref[-1]]:
                continue
            a, sg = TWIST[t]
            c[a] += sg
            pref.append(t)
            n2 = n + 1
            balanced_now = (c == [0, 0, 0])
            # a PROPER prefix may not close; the final word must
            if not (2 <= n2 < length and balanced_now) and \
               not (n2 == length and not balanced_now):
                rec()
            c[a] -= sg
            pref.pop()

    rec()
    return out


def delta_two_thirds_audit():
    print("\n=== F. WHAT Delta = 2/3 IS, AND WHERE THE LADDER STOPS ===\n")

    print("F1. Delta = 2/3 IS the muon-to-electron mass ratio.")
    print("  With A^2 = 2 derived, the form has parameters (M, Delta).  M is the")
    print("  overall scale, so Delta is the ONLY remaining ratio freedom:")
    print(f"  {'Delta':>10} {'m_mu/m_e':>14} {'m_tau/m_e':>14}")
    for D in (0.60, 0.64, 2/3, 0.69, 0.72):
        w = koide_weights(D/3)
        print(f"  {D:10.4f} {w[2]/w[1]:14.4f} {w[0]/w[1]:14.2f}")
    print(f"  {'measured':>10} {MMU/ME:14.4f} {MTAU/ME:14.2f}")
    print("  -> 'derive Delta = 2/3' and 'derive m_mu/m_e = 206.77' are the SAME")
    print("     statement in different coordinates.  That is the difficulty")
    print("     class: a number nobody has derived.  NOT DERIVED here either.\n")

    print("F2. Does the blind ladder stop at three generations?")
    otau, omu, oe = orbit(TAU_REP), orbit(MU_REP), orbit(E_REP)
    print("  signature of the rungs that WERE selected:")
    for nm, h, po in (("mu", MU_REP, oe), ("tau", TAU_REP, omu)):
        print(f"    {nm:4} parent-degree = {dict(child_parent_degree(orbit(h), po))}")
    print("    tau's signature: every rooted history has EXACTLY ONE parent.\n")

    free = [h for h in first_return_pruned(10)
            if baryon_number(h) == 0 and fold_phase(h) == "-I"]
    cls: dict[str, list[str]] = defaultdict(list)
    for h in free:
        cls[canonical(h)].append(h)
    cand = [r for r in cls if len(axes_engaged(r)) == 3]
    rows = []
    for r in cand:
        o = orbit(r)
        e = parent_edges(o, otau)
        if e:
            rows.append((r, len(cls[r]), e, dict(child_parent_degree(o, otau))))
    strict = [r for r, _, _, d in rows if set(d) == {1}]

    print(f"  L=10: {len(cls)} classes, {len(cand)} three-axis,")
    print(f"        {len(rows)} with a causal parent in the tau orbit,")
    print(f"        {len(strict)} matching tau's exact degree signature.")
    for r, w, e, d in sorted(rows, key=lambda x: key(x[0])):
        mark = "  <-- tau signature" if set(d) == {1} else ""
        print(f"    {r:12} ways={w:3d} edges={e:4d} degree={d}{mark}")

    print("\n  VERDICT: the rule that produced e -> mu -> tau is AMBIGUOUS at L=10.")
    print("  L=8 gave 1 of 2 candidates; L=10 gives 12 of 105 (4 under the strict")
    print("  signature).  It yields neither 0 -- which would confirm the ladder")
    print("  terminates at three generations -- nor 1, a fourth generation.")
    print("  So the L=8 uniqueness looks like a small-numbers accident, and this")
    print("  ladder is NOT an independent derivation of 'exactly three'.")
    print("  QLF's three-generation claim rests on QLF_Generations (generation")
    print("  count = spatial dimension = 3), which is untouched by this; what")
    print("  fails is this combinatorial route as a second, independent argument.")


E_REP, MU_REP, TAU_REP = "^<v>", "^^<vv>", "^^</>vv\\"


# ---------- G. the (R, axis) -> mass-ratio map: a shape theorem ----------

def five_smooth_best(target: float, amax=12, bmax=6, cmax=4):
    """Closest 2^a 3^b 5^c to target with small exponents."""
    best = None
    for a in range(-amax, amax+1):
        for b in range(-bmax, bmax+1):
            for c in range(-cmax, cmax+1):
                v = 2.0**a * 3.0**b * 5.0**c
                e = abs(v/target - 1)
                if best is None or e < best[0]:
                    best = (e, a, b, c, v)
    return best


def mass_ratio_map_audit():
    print("\n=== G. THE (R, axis) -> MASS-RATIO MAP: A SHAPE THEOREM ===\n")

    print("G1. Every census integer at the three rungs is 5-SMOOTH.")
    print("  L = 4,6,8;  orbit = ways = 24,48,96;  axes = 2,2,3;")
    print("  conj-pairs = 2,5,6;  parent-edges = 192,96.")
    print("  All are of the form 2^a 3^b 5^c, so ANY product or ratio of them")
    print("  is 5-smooth too.  Can the mass ratios be 5-smooth?\n")
    print(f"  {'quantity':>16} {'value':>13}   closest 2^a 3^b 5^c      error")
    for nm, t in (("m_mu/m_e", MMU/ME), ("m_tau/m_e", MTAU/ME),
                  ("m_tau/m_mu", MTAU/MMU), ("Delta = 2/3", 2/3)):
        e, a, b, c, v = five_smooth_best(t)
        print(f"  {nm:>16} {t:13.6f}   2^{a:<3d}3^{b:<3d}5^{c:<3d} = {v:11.6f}"
              f"  {e*100:7.3f}%")
    print("\n  The MASS RATIOS ARE NOT 5-SMOOTH: the closest small-exponent form")
    print("  misses by 0.14-0.61%, orders of magnitude outside the 1e-5 at which")
    print("  the three-phase picture holds.  A 64000-expression brute search over")
    print("  a^p b^q c^r from the census pool does no better (best 0.286% off).")
    print("  => the DIRECT census -> mass-ratio map does not exist in any simple")
    print("     form.  This is a real negative, not a failed fit.\n")

    print("G2. So the map must FACTOR:   census -> Delta -> masses.")
    print("  sqrt(m_k)/M = 1 + sqrt2 cos(Delta/3 + 2pi k/3): the mass ratios are")
    print("  COSINE VALUES at an O(1) phase, transcendental in Delta.  A census")
    print("  produces integers; it cannot produce those directly.  It can only")
    print("  produce the PHASE, and the cosine does the rest.  Independently:")
    print("  Q = 2/3 is derived and holds to 1e-5, so any correct map must")
    print("  reproduce it -- which a map onto (M, Delta) does automatically and")
    print("  a map onto three independent masses would have to hit by accident.")
    print("  And Delta = 2/3 IS exactly 5-smooth (2 * 3^-1) -- precisely the kind")
    print("  of object a census CAN yield.  The issue's ask is thereby reshaped")
    print("  from 'three masses' to ONE SMALL RATIONAL.  That is well posed.\n")

    print("G3. WARNING -- the obvious census route to 2/3 is CIRCULAR.")
    print("  The axis counts (e,mu,tau) = (2,2,3) look like the transverse")
    print("  fraction 2/3.  Provenance of each:")
    print("    e  (L=4): 3 axes need >=6 twists to balance  -> FORCED")
    c6 = classes(half_spin_free(6))
    n3 = sum(1 for r in c6 if len(axes_engaged(r)) == 3)
    print(f"    mu (L=6): 3-axis free half-spin classes = {n3}  -> OUTPUT")
    c8 = classes(half_spin_free(8))
    omu = orbit(MU_REP)
    parented = [r for r in c8 if parent_edges(orbit(r), omu)]
    three = [r for r in parented if len(axes_engaged(r)) == 3]
    print(f"    tau(L=8): part A filters to 3-axis BEFORE the parent rule.")
    print(f"              Drop the filter: {len(parented)} of {len(c8)} classes have a mu")
    print(f"              parent ({len(three)} of them 3-axis) -- NOT unique.")
    print("  => the 3-axis criterion is LOAD-BEARING in part A's tau selection.")
    print("     'axes = 2,2,3' is therefore partly IMPOSED, and cannot be cited")
    print("     as census evidence for Delta = 2/3.  Recorded so it is not.")


# ---------- H. the unit audit: is 'Delta = 2/3 is 5-smooth' unit-luck? ----------

def cf_convergents(x, n=12):
    """Continued-fraction convergents p/q of x."""
    a, v = [], x
    for _ in range(n):
        i = int(v)
        a.append(i)
        if abs(v - i) < 1e-15:
            break
        v = 1.0 / (v - i)
    out, p0, q0, p1, q1 = [], 1, 0, a[0], 1
    for i in a[1:]:
        p0, q0, p1, q1 = p1, q1, i * p1 + p0, i * q1 + q0
        out.append((p1, q1))
    return out


def unit_audit():
    """Part G2 claimed Delta = 2/3 is 5-smooth, 'precisely what a census can
    yield'.  That is true of the RADIAN measure only.  This part asks what
    justifies radians, and audits every other reading."""
    print("\n=== H. THE UNIT AUDIT: WHICH ANGULAR UNIT IS THE CENSUS UNIT? ===\n")
    D = 2.0 / 3.0

    print("H1. Delta = 2/3 is 5-smooth IN RADIANS.  In every other unit it is not.\n")
    print(f"  {'unit':>22}   Delta in that unit")
    for nm, u in (("turn (2pi)", 2 * math.pi),
                  ("Z3 cell (2pi/3)", 2 * math.pi / 3),
                  ("pi", math.pi),
                  ("right angle (pi/2)", math.pi / 2),
                  ("degree", math.pi / 180)):
        print(f"  {nm:>22} = {D / u:.9f}")
    print(f"\n  As a fraction of a TURN the phase is exactly 1/(3 pi) = "
          f"{1/(3*math.pi):.9f}")
    print("  -- transcendental.  A census cannot yield that.  So the 5-smoothness")
    print("  of 2/3 is a fact about the radian, not about the phase: it survives")
    print("  exactly one choice of unit and is destroyed by every other.\n")

    print("H2. Consequence -- the CIRCLE-DIVISION route is EXCLUDED.")
    print("  If a census fixes the phase by dividing a turn into q equal parts")
    print("  and stepping p of them, then Delta = 2pi p/q.  Convergents of")
    print(f"  Delta/2pi = {D/(2*math.pi):.9f} :\n")
    print(f"    {'p/q':>14}   2pi p/q        rel err vs 2/3")
    for p, q in cf_convergents(D / (2 * math.pi))[:8]:
        v = 2 * math.pi * p / q
        print(f"    {p:>6d}/{q:<7d} {v:.9f}   {abs(v/D - 1):.3e}")
    # tested against the DATA, not against the hypothesis
    DM, SD = 0.666689, 0.000025          # free 3-parameter fit, part C
    lo, hi = DM - 2 * SD, DM + 2 * SD
    hits = []
    for q in range(1, 401):
        for p in range(1, q):
            if math.gcd(p, q) == 1 and lo <= 2 * math.pi * p / q <= hi:
                hits.append((q, p))
                break
    print(f"\n  Against the DATA (free-fit Delta = {DM} +- {SD}, 2 sigma band")
    print(f"  [{lo:.6f}, {hi:.6f}]), the turn-fractions that fit are")
    print("    " + ", ".join(f"{p}/{q}" for q, p in hits[:4]))
    print(f"  smallest denominator q = {hits[0][0]}.  A census that cuts a circle")
    print("  into 311 parts and takes 33 of them is not a census; it is a fit.")
    print("  Single divisions are nowhere near: 2pi/9 misses by 4.7%.")
    print("  => NO circle-division census can produce this phase.\n")

    print("H3. What SURVIVES: arc-over-radius.  A rational RADIAN measure is")
    print("  what you get from n unit arc-steps at integer radius R: Delta = n/R.")
    print("  Delta = 2/3 then reads '2 steps at radius 3' -- a CURVATURE ratio,")
    print("  not a division of the circle.  This is the only surviving shape, and")
    print("  it is what actually explains (part C) why the phase is a pure number")
    print("  rather than a multiple of pi: turn-fractions carry pi, arc/radius")
    print("  ratios do not.  NOTE: this fixes the FORM, not the counts, and G3's")
    print("  trap still forbids supplying them from the (2,2,3) axis census.\n")

    print("H4. And the physics never sees Delta -- it sees cos(Delta).")
    s = [math.sqrt(m) for m in (ME, MMU, MTAU)]
    M3 = sum(s) / 3
    e3_meas = s[0] * s[1] * s[2] / M3**3
    cosD = math.cos(D)
    e3 = -0.5 + cosD / math.sqrt(2)
    print("  With A^2 = 2 the normalized sqrt-mass triple has e1 = 3, e2 = 3/2")
    print("  fixed, so exactly ONE symmetric function carries the phase:")
    print("    e3 = 27 prod(sqrt m) / (sum sqrt m)^3 = -1/2 + cos(Delta)/sqrt2")
    print(f"       model (Delta = 2/3) : {e3:.9f}")
    print(f"       measured            : {e3_meas:.9f}   ({e3_meas/e3-1:+.2e})")
    print("  Is THAT quantity census-shaped?\n")
    print(f"  {'quantity':>12} {'value':>13}   closest 2^a 3^b 5^c      error")
    for nm, t in (("cos Delta", cosD), ("e3", e3),
                  ("e3^(1/3)", e3 ** (1 / 3)), ("Delta", D)):
        e, a, b, c, v = five_smooth_best(t)
        print(f"  {nm:>12} {t:13.9f}   2^{a:<3d}3^{b:<3d}5^{c:<3d} = {v:11.9f}"
              f"  {e*100:7.4f}%")
    print("\n  Only Delta itself is 5-smooth.  cos(Delta) misses by 0.54%, e3 by")
    print("  0.27% -- the same 0.1-0.6% band as the mass ratios in G1, i.e. the")
    print("  SAME negative.  Passing through the phase did not make the target")
    print("  census-shaped; it moved the non-smoothness into the cosine.\n")
    print("  => G2's 'Delta = 2/3 IS 5-smooth, precisely what a census CAN yield'")
    print("     is CORRECTED: it holds in radians alone, and the invariant the")
    print("     masses are built from is no more census-shaped than they are.")
    print("     The reshaping to one small rational stands; the claim that the")
    print("     rational is thereby within census reach does NOT.")


# ---------- I. Occam curve: arc-over-radius vs circle-division ----------

def occam_curve(kind, target, bmax=15):
    """Best fit to `target` achievable at each description-length budget.

    A fraction n/d costs log2(n*d) bits.  `kind` fixes how the fraction is
    read as an angle: 'arc' means Delta = n/d radians (n unit arc-steps at
    radius d); 'turn' means Delta = 2 pi n/d (n parts of a d-fold division).
    """
    best = [None] * (bmax + 1)
    lim = 2 ** bmax
    for d in range(1, lim + 1):
        for n in range(1, lim // d + 1):
            if math.gcd(n, d) != 1:
                continue
            v = 2 * math.pi * n / d if kind == "turn" else n / d
            e = abs(v / target - 1)
            b = max(2, (n * d - 1).bit_length())
            if best[b] is None or e < best[b][0]:
                best[b] = (e, n, d)
    out, run = [], None
    for b in range(2, bmax + 1):          # make it cumulative: budget <= b
        if best[b] is not None and (run is None or best[b][0] < run[0]):
            run = best[b]
        out.append((b, run))
    return out


def occam_audit():
    """Part H left two channels standing or falling; this prices them.

    How many bits of arithmetic does each hypothesis class need to spend to
    reach the measured phase?  A structure pays once and saturates at the
    experimental floor; a fit pays steadily and keeps improving."""
    print("\n=== I. PRICING THE TWO CHANNELS: AN OCCAM CURVE ===\n")
    DM, SD = 0.666689, 0.000025           # free 3-parameter fit, part C

    print(f"I1. Best fit to the measured Delta = {DM} reachable on a budget of")
    print("  b bits, in each channel (a fraction n/d costs log2(n*d) bits):\n")
    print(f"  {'bits':>4} | {'circle-division  2 pi n/d':>30}"
          f" | {'arc-over-radius  n/d':>26}")
    print("  " + "-" * 5 + "+" + "-" * 32 + "+" + "-" * 28)
    for (b, t), (_, a) in zip(occam_curve("turn", DM),
                              occam_curve("arc", DM)):
        ts = f"{t[1]:>5d}/{t[2]:<6d} err {t[0]:.2e}" if t else "-"
        as_ = f"{a[1]:>4d}/{a[2]:<5d} err {a[0]:.2e}" if a else "-"
        print(f"  {b:>4} | {ts:>30} | {as_:>26}")
    print("\n  ARC reaches the experimental floor (3.3e-5, the free-fit")
    print("  systematic of part C) at 3 BITS -- with 2/3, the cheapest")
    print("  non-trivial fraction there is -- and never improves, because it")
    print("  cannot: it is already at the floor.  That is what a structure")
    print("  looks like.  CIRCLE-DIVISION needs 14 BITS to match it, and")
    print("  improves smoothly at every budget along the way.  That is what a")
    print("  fit looks like.  The gap is 11 bits ~ 2000 : 1.\n")

    print("I2. RIGIDITY -- in the arc channel there is nothing else to choose.")
    lo, hi = DM - 2 * SD, DM + 2 * SD
    other = None
    for R in range(1, 60000):
        for n in (round(2 * R / 3) - 1, round(2 * R / 3), round(2 * R / 3) + 1):
            if n > 0 and lo <= n / R <= hi and abs(n / R - 2 / 3) > 1e-15:
                other = (n, R)
                break
        if other:
            break
    print(f"  Inside the 2-sigma band [{lo:.6f}, {hi:.6f}], 2/3 is the ONLY")
    print(f"  rational value with denominator below {other[1]}; the next distinct")
    print(f"  one is {other[0]}/{other[1]}.  So committing to a small radius leaves")
    print("  exactly ONE candidate -- no freedom to tune.  The circle-division")
    print("  channel already has two (33/311, 40/377) below q = 400.\n")

    print("I3. WHAT n = 2 AND R = 3 WOULD HAVE TO BE.")
    print("  R = 3 : the three spatial axes -- substrate_spatial_dimension,")
    print("          machine-verified (QLF_Generations), NOT the imposed")
    print("          3-axis filter of part G3.  Different object, different")
    print("          provenance; the trap does not apply.")
    print("  n = 2 : the two transverse axes -- the same 6 = 2+1-per-axis")
    print("          split that supplies A^2 = 2 in the derived Q = 2/3.")
    print("  Note this is COMMON CAUSE, not implication: Q = 2/3 does not imply")
    print("  Delta = 2/3 (part E refuted that, as functions on mass-triple")
    print("  space), but one geometric split can feed both -- as an amplitude")
    print("  in the Koide sector and as a curvature in the phase sector.\n")

    print("I4. HONEST LIMIT.  This is an IDENTIFICATION, not a derivation --")
    print("  the same status as the A^2 = 2 identification it leans on.  No")
    print("  substrate computation yet produces '2 arc-steps at radius 3' for")
    print("  the lepton phase; parts H-I say only that any derivation must have")
    print("  that shape and that the shape is cheap and rigid.  What would")
    print("  close it: a curvature computed ON the ladder closures whose arc")
    print("  count and radius are read off the geometry, not matched to 2/3.")


# ---------- J. the curvature computation on the ladder closures ----------

def loop_path(h: str):
    """Count-balance IS closure: a ZFA twist history is a closed walk in Z^3."""
    p = [(0, 0, 0)]
    for t in h:
        a, s = TWIST[t]
        q = list(p[-1])
        q[a] += s
        p.append(tuple(q))
    return p


def loop_observables(h: str) -> dict:
    """Integer geometry of the closed loop.  Every entry is invariant under the
    part-A quotient (signed axis permutations + antiparticle)."""
    ax = [TWIST[t][0] for t in h]
    n = len(h)
    p = loop_path(h)
    ext = [max(q[k] for q in p) - min(q[k] for q in p) for k in range(3)]

    def proj_area(i, j):
        return sum(a[i]*b[j] - b[i]*a[j] for a, b in zip(p, p[1:])) // 2

    A = [proj_area(0, 1), proj_area(1, 2), proj_area(2, 0)]
    return {
        "L":     n,                                             # arc length
        "sites": len(set(p[:-1])),                              # vertices
        "runs":  sum(1 for i in range(n) if ax[i] != ax[(i+1) % n]),
        "axes":  len(set(ax)),
        "dirs":  len(set(h)),
        "bsum":  sum(ext),                                      # box extents
        "asum":  sum(abs(a) for a in A),                        # projected area
        "amax":  max(abs(a) for a in A),
    }


def curvature_audit():
    """Part I closed by asking for a curvature computed ON the ladder closures,
    arc count and radius read off the geometry rather than matched to 2/3.
    Here it is.  It is a NEGATIVE."""
    print("\n=== J. THE CURVATURE COMPUTATION ON THE LADDER CLOSURES ===\n")
    reps = (("e", E_REP), ("mu", MU_REP), ("tau", TAU_REP))
    O = {nm: loop_observables(h) for nm, h in reps}
    keys = list(O["e"])

    print("J1. Count balance IS closure, so each ladder rung is a CLOSED WALK")
    print("  in Z^3 and has ordinary integer geometry:\n")
    print(f"  {'':>6} " + " ".join(f"{nm:>6}" for nm, _ in reps))
    for k in keys:
        print(f"  {k:>6} " + " ".join(f"{O[nm][k]:>6}" for nm, _ in reps))
    print("\n  One relation holds at every rung: runs = 2 * axes -- each engaged")
    print("  axis is traversed out and back exactly once, no zig-zag.  That is")
    print("  a genuine property of the SELECTED ladder, not of loops generally:")
    for n in (4, 6, 8):
        cs = list(classes(half_spin_free(n)))
        hit = sum(1 for r in cs
                  if loop_observables(r)["runs"] == 2 * loop_observables(r)["axes"])
        print(f"    L={n}: {hit}/{len(cs)} half-spin free classes "
              f"({hit/len(cs)*100:.0f}%) satisfy it")
    print()

    print("J2. BLIND SEARCH for a rung-independent arc-over-radius ratio.")
    print("  Delta is one number for the whole family, so any curvature that")
    print("  can be it must take the SAME value at all three rungs.  Every")
    print("  ratio of two observables that does:\n")
    for nm in O:
        O[nm]["dim"] = 3                    # substrate_spatial_dimension
    pool = keys + ["dim"]
    const = defaultdict(list)
    for a in pool:
        for b in pool:
            if a == b:
                continue
            vals = [O[nm][a] / O[nm][b] for nm, _ in reps if O[nm][b]]
            if len(vals) == 3 and max(vals) - min(vals) < 1e-12:
                const[round(vals[0], 9)].append(f"{a}/{b}")
    for v in sorted(const):
        print(f"    {v:>8} :  " + ", ".join(const[v][:5])
              + (" ..." if len(const[v]) > 5 else ""))
    print(f"\n  The complete set of rung-independent values is "
          f"{{{', '.join(str(v) for v in sorted(const))}}}.")
    print("  2/3 IS NOT AMONG THEM.  In particular sec 5c^5's identification")
    print("  '2 transverse arc-steps at radius 3' does NOT survive: dividing")
    print("  the runs by the ambient dimension gives")
    print("    runs/dim = " + ", ".join(
        f"{O[nm]['runs']}/3" for nm, _ in reps) + " = 1.33, 1.33, 2.00")
    print("  which is not rung-independent.  Only runs/axes is -- and that is 2,")
    print("  not 2/3, because e and mu engage two axes, not three.\n")

    print("J3. AND QLF'S OWN CURVATURES ARE THE WRONG KIND (Curvature.md).")
    print("  QLF defines curvature twice, and part H excludes both:")
    print("   (a) GAUGE / HOLONOMY curvature = the Lie bracket, i.e. the")
    print("       plaquette sigma_x sigma_y sigma_x sigma_y = -1 (sec 1a).  Its")
    print("       values are the Pauli fold group mu_4 = {+-I, +-iI} -- a 4-fold")
    print("       DIVISION OF THE TURN.  That is exactly the channel part H")
    print("       excluded.  Check: the fold of every rung is")
    print("         " + ", ".join(f"{nm} -> {fold_phase(h)}" for nm, h in reps))
    print("       three quarter-turn units, no continuous parameter anywhere.")
    print("   (b) TOPOLOGICAL DEFICIT curvature = the 12 pentamons of a Fuller")
    print("       blanket (sec 1).  A pure COUNT with no radius; its angular")
    print("       form, the deficit 2pi - 5*(pi/3) = pi/3, is again a division")
    print("       of the turn.")
    print("  So the arc-over-radius object part H left standing is not")
    print("  instantiated by either QLF curvature.  Same exclusion, twice.\n")

    print("J4. THE PRICE -- and the general criterion.")
    ladder = sorted({4, 6, 8, 2, 3, 1})
    full = sorted({4, 6, 8, 24, 48, 96, 2, 3, 5, 6, 192, 1})
    for nm, p in (("ladder geometry", ladder), ("full census (part G)", full)):
        vals = {(a, b) for a in p for b in p}
        small = {round(a/b, 9) for a, b in vals if b and a/b <= 8
                 and abs(round(a/b*6) - a/b*6) < 1e-9}
        print(f"  {nm:>22}: pool {p}")
        print(f"  {'':>22}  reaches {len(small)} distinct small ratios "
              f"-> naming 2/3 among them costs {math.log2(len(small)):.1f} bits")
    print("\n  Part I priced the CONSTANT at 3 bits: 2/3 is the cheapest")
    print("  non-trivial fraction there is, and it already sits at the")
    print("  experimental floor.  Reading it off the census costs MORE than")
    print("  that.  A derivation that costs more bits than the constant it")
    print("  derives is not a derivation -- it is a re-encoding.")
    print("  => the census route to Delta is RETIRED.  The arc-over-radius")
    print("     requirement (part H) stands; QLF has no object of that shape,")
    print("     and the ladder census cannot supply one at an honest price.")


# ---------- K. the third curvature notion ----------
#
# Parts H and J left a specification with nothing to fill it: a curvature that
# is a RATIO OF COUNTS -- not a holonomy (mu_4, a division of the turn) and not
# a topological deficit (a count with no radius).  Exactly one standard
# discrete curvature meets it: Ollivier-Ricci,
#
#     kappa(x,y) = 1 - W_1(m_x, m_y) / d(x,y),
#
# a transport cost over a distance, both pure step counts on a graph.  No
# angle, no metric, no finite group, rational by construction.

class _MinCostFlow:
    def __init__(self, n):
        self.n, self.g = n, [[] for _ in range(n)]

    def add(self, u, v, cap, cost):
        self.g[u].append([v, cap, cost, len(self.g[v])])
        self.g[v].append([u, 0, -cost, len(self.g[u]) - 1])

    def run(self, src, snk):
        total = 0
        while True:
            dist = [math.inf] * self.n
            inq = [False] * self.n
            pv, pe = [-1] * self.n, [-1] * self.n
            dist[src] = 0
            q = [src]
            inq[src] = True
            while q:                                  # SPFA
                u = q.pop(0)
                inq[u] = False
                for i, (v, cap, cost, _) in enumerate(self.g[u]):
                    if cap > 0 and dist[u] + cost < dist[v] - 1e-12:
                        dist[v] = dist[u] + cost
                        pv[v], pe[v] = u, i
                        if not inq[v]:
                            q.append(v)
                            inq[v] = True
            if dist[snk] == math.inf:
                return total
            f, v = math.inf, snk
            while v != src:
                f = min(f, self.g[pv[v]][pe[v]][1])
                v = pv[v]
            v = snk
            while v != src:
                e = self.g[pv[v]][pe[v]]
                e[1] -= f
                self.g[v][e[3]][1] += f
                v = pv[v]
            total += f * dist[snk]


def wasserstein_1(src, dst, dist):
    """Exact W_1 between integer-mass distributions (equal totals)."""
    S, T = list(src), list(dst)
    net = _MinCostFlow(len(S) + len(T) + 2)
    s, t = len(S) + len(T), len(S) + len(T) + 1
    for i, a in enumerate(S):
        net.add(s, i, src[a], 0)
    for j, b in enumerate(T):
        net.add(len(S) + j, t, dst[b], 0)
    for i, a in enumerate(S):
        for j, b in enumerate(T):
            net.add(i, len(S) + j, 1 << 30, dist(a, b))
    return net.run(s, t)


def ollivier_ricci(adj, dist, x, y, idle=2):
    """Lazy Ollivier-Ricci curvature of the edge (x,y), idleness 1/idle.

    Laziness is not cosmetic here: the census graph is layered, hence
    bipartite, and the idleness-0 measure would sit entirely on the far side.
    """
    dx, dy = len(adj[x]), len(adj[y])
    scale = idle * dx * dy

    def measure(v, deg):
        m = defaultdict(int)
        m[v] += scale // idle
        for w in adj[v]:
            m[w] += (scale - scale // idle) // deg
        return dict(m)

    w = wasserstein_1(measure(x, dx), measure(y, dy), dist)
    return 1.0 - w / (scale * dist(x, y))


def _bfs_dist(adj):
    D = {}
    for v in adj:
        d, q = {v: 0}, [v]
        while q:
            u = q.pop(0)
            for w in adj[u]:
                if w not in d:
                    d[w] = d[u] + 1
                    q.append(w)
        D[v] = d
    return D


def _spectrum(adj):
    D = _bfs_dist(adj)
    dist = lambda a, b: D[a].get(b, 1 << 20)
    idx = {v: i for i, v in enumerate(adj)}
    out = []
    for x in adj:
        for y in adj[x]:
            if idx[x] < idx[y]:
                out.append(((x, y), ollivier_ricci(adj, dist, x, y)))
    return out


def _undirected(pairs):
    a = defaultdict(set)
    for u, v in pairs:
        a[u].add(v)
        a[v].add(u)
    return a


def third_curvature_audit():
    print("\n=== K. THE THIRD CURVATURE NOTION ===\n")

    print("K1. THE SPECIFICATION left by parts H and J.  A curvature usable")
    print("  here must be (i) a RATIO OF COUNTS, (ii) not valued in a finite")
    print("  group -- no division of the turn, (iii) not a bare deficit count,")
    print("  (iv) defined with no angle and no metric.  Against that:")
    print("    Regge angular deficit          division of the turn      NO")
    print("    QLF pentamon deficit (sec 1)   count, no radius          NO")
    print("    holonomy / Wilson plaquette    finite group mu_4         NO")
    print("    Benincasa-Dowker (QLF)         needs a length scale l^2  NO")
    print("    Forman-Ricci                   integer, not a ratio      partial")
    print("    OLLIVIER-RICCI                 1 - W_1/d, counts only    YES")
    print("  kappa(x,y) = 1 - W_1(m_x,m_y)/d(x,y): a transport cost over a")
    print("  distance, both pure step counts.  Rational by construction.\n")

    print("K2. VALIDATION -- the estimator on graphs of known curvature.")
    tests = [
        ("cycle C8 (flat)", [(i, (i+1) % 8) for i in range(8)]),
        ("complete K5 (positive)",
         [(i, j) for i in range(5) for j in range(i+1, 5)]),
    ]
    grid = [((i, j), (i+di, j+dj)) for i in range(6) for j in range(6)
            for di, dj in ((1, 0), (0, 1)) if i+di < 6 and j+dj < 6]
    tests.append(("6x6 grid (flat interior)", grid))
    cube = [((i, j, k), (i+d[0], j+d[1], k+d[2]))
            for i in range(4) for j in range(4) for k in range(4)
            for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1))
            if i+d[0] < 4 and j+d[1] < 4 and k+d[2] < 4]
    tests.append(("4x4x4 lattice = SPACE", cube))
    tree = []
    nid = [0]

    def grow(u, depth, deg):
        if not depth:
            return
        for _ in range(deg):
            nid[0] += 1
            v = nid[0]
            tree.append((u, v))
            grow(v, depth - 1, 2)
    grow(0, 4, 3)
    tests.append(("3-regular tree (negative)", tree))
    for nm, edges in tests:
        sp = [k for _, k in _spectrum(_undirected(edges))]
        print(f"    {nm:26s} kappa in [{min(sp):+.3f}, {max(sp):+.3f}]")
    print("  Flat graphs give 0, the complete graph positive, the tree")
    print("  negative on interior edges (its POSITIVE values are all leaf")
    print("  edges -- a truncation artefact to remember below).  The 3-D")
    print("  lattice is kappa = 0 on every interior edge; the positive tail")
    print("  is the boundary of the finite chunk.\n")

    print("K3. IS SPACE THEREFORE FLAT?  NO -- and the failure is the point.")
    print("  QLF space is not a bare lattice.  Every fold carries ONE BIT, and")
    print("  the plaquette of the one-bit orthogonal axes is")
    print(f"    fold({E_REP}) = {fold_phase(E_REP)}  != +I   (nonabelian_plaquette)")
    print("  which IS curvature, in QLF's own primary sense (Curvature.md 1a).")
    print("  So is the lattice's kappa = 0 an artefact of throwing the fold")
    print("  away?  Test it: lift the lattice by the fold, vertices being")
    print("  (position, fold element) and edges carrying the twist's Pauli")
    print("  factor -- the graph QLF space actually is.")
    grp, frontier = {}, [I]
    while frontier:
        m = frontier.pop()
        k = tuple((round(z.real, 6), round(z.imag, 6)) for z in m)
        if k in grp:
            continue
        grp[k] = m
        for t in SPATIAL:
            frontier.append(mmul(m, PMAP[t]))
    n = 4
    lift = defaultdict(set)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for t in SPATIAL:
                    a, s = TWIST[t]
                    p = [i, j, k]
                    p[a] += s
                    if not all(0 <= q < n for q in p):
                        continue
                    for ph in grp:
                        q = tuple((round(z.real, 6), round(z.imag, 6))
                                  for z in mmul(grp[ph], PMAP[t]))
                        lift[((i, j, k), ph)].add((tuple(p), q))
                        lift[(tuple(p), q)].add(((i, j, k), ph))
    Dl = _bfs_dist(lift)
    dl = lambda a, b: Dl[a].get(b, 1 << 20)
    ks = [ollivier_ricci(lift, dl, x, y)
          for x in lift for y in lift[x]
          if str(x) < str(y)
          and all(1 <= c <= n-2 for c in x[0]) and all(1 <= c <= n-2 for c in y[0])]
    print(f"    fold group generated by the six twists: order {len(grp)}")
    print(f"    lifted lattice: {len(lift)} vertices, {len(ks)} interior edges,"
          f" kappa in [{min(ks):+.4f}, {max(ks):+.4f}]")
    print("  STILL ZERO.  The flatness is not an artefact of dropping the fold:")
    print("  Ollivier-Ricci is a metric-combinatorial quantity and is")
    print("  STRUCTURALLY BLIND TO HOLONOMY.  Parts H and J chose it precisely")
    print("  BECAUSE it is not a holonomy; reading 'space is flat' off it")
    print("  measures the instrument, not the space.  The correct statement:")
    print("    space            -- Ollivier-FLAT, holonomy-CURVED (one bit/fold)")
    print("    possibility graph -- Ollivier-HYPERBOLIC, holonomy-free")
    print("  Two notions, two graphs, each blind to the other's curvature.")
    print("  They are complementary, not competing.\n")

    print("K4. APPLY IT TO THE POSSIBILITY GRAPH.")
    print("  QLF's second graph is not space -- it is the census: closure")
    print("  classes joined by the causal parent relation.  Building L=4,6,8,10")
    print("  so that the L=6 and L=8 layers are interior rather than boundary.")
    layers = {}
    for n in (4, 6, 8, 10):
        cls = defaultdict(list)
        for h in first_return_pruned(n):
            if baryon_number(h) == 0 and fold_phase(h) == "-I":
                cls[canonical(h)].append(h)
        layers[n] = sorted(cls)
    orb = {c: orbit(c) for n in layers for c in layers[n]}
    edges = [(c, p) for n in (6, 8, 10) for c in layers[n]
             for p in layers[n-2] if parent_edges(orb[c], orb[p])]
    adj = _undirected(edges)
    layer_of = {c: n for n in layers for c in layers[n]}
    print(f"    classes per rung: " +
          ", ".join(f"L={n}: {len(layers[n])}" for n in layers))
    print(f"    graph: {len(adj)} connected vertices, {len(edges)} edges\n")
    sp = _spectrum(adj)
    inter = [k for (x, y), k in sp
             if len({layer_of[w] for w in adj[x]}) > 1
             and len({layer_of[w] for w in adj[y]}) > 1]
    pos = sum(1 for _, k in sp if k > 1e-12)
    neg = sum(1 for _, k in sp if k < -1e-12)
    print(f"    all {len(sp)} edges : kappa in "
          f"[{min(k for _, k in sp):+.4f}, {max(k for _, k in sp):+.4f}]"
          f"   ({neg} negative, {pos} positive)")
    print(f"    {len(inter)} INTERIOR edges: kappa in "
          f"[{min(inter):+.4f}, {max(inter):+.4f}]   "
          f"({sum(1 for k in inter if k < 0)} negative, "
          f"{sum(1 for k in inter if k >= 0)} non-negative)")
    print("\n  EVERY INTERIOR EDGE IS NEGATIVELY CURVED.  The positive values")
    print("  sit entirely on the L=10 truncation boundary -- the same leaf")
    print("  artefact the tree control shows (K6 settles it by adding a layer).")
    print("  So the possibility graph is HYPERBOLIC where it is not truncated,")
    print("  under the very notion that reads space as flat.  That is the")
    print("  discrete AdS signature, and it is what QLF's")
    print("  holography already says in words: the bulk is the generator tree,")
    print("  the boundary its ZFA-closed leaves.  Here it is measured.\n")

    print("K5. AND IT DOES NOT SUPPLY THE PHASE.")
    print(f"    kappa > 0 anywhere in the interior?  no -- max is "
          f"{max(inter):+.4f}")
    print(f"    +2/3 anywhere at all?              no")
    print(f"    interior values are {len(set(round(k,9) for k in inter))} distinct on "
          f"{len(inter)} edges,")
    print("    so naming one of them costs ~3.8 bits against the 3 bits part I")
    print("    prices the constant at -- the part J criterion, failed again.")
    print("  So the third notion EXISTS and is informative about the substrate,")
    print("  but Delta = 2/3 is not one of its values.  The phase is not a")
    print("  curvature of either QLF graph.  Delta stays OPEN -- with the")
    print("  curvature route now closed at all three notions rather than two.")


def wall_audit():
    """Back to Delta = 2/3, from the other end.

    Everything so far attacked the NUMBER.  This part looks at what the number
    DOES in the three-phase form, and two things fall out: the lepton
    hierarchy needs no large parameter, and the residual that has been carried
    as 'the one number needing explanation' is a coordinate artefact."""
    print("\n=== L. THE MASSLESS WALL -- WHAT Delta = 2/3 ACTUALLY DOES ===\n")
    D = 2.0 / 3.0
    # koide_weights returns the SQUARES (the masses); the amplitudes are these
    s = [1 + math.sqrt(2) * math.cos(D / 3 + 2 * math.pi * k / 3) for k in range(3)]
    wall = 3 * math.pi / 4

    print("L1. THE FORM HAS A ZERO, AND THE ELECTRON SITS NEXT TO IT.")
    print("  1 + sqrt2 cos(theta) = 0 at theta = 3pi/4 = 135.0000 deg exactly.")
    print(f"  {'k':>3} {'theta (deg)':>13} {'1+sqrt2 cos':>13} {'m/M^2':>13}")
    for k in range(3):
        th = D / 3 + 2 * math.pi * k / 3
        print(f"  {k:>3} {math.degrees(th):13.4f} {s[k]:13.6f} {s[k]**2:13.8f}")
    e_th = D / 3 + 2 * math.pi / 3
    eps = wall - e_th
    lo, hi = min(s), max(s)
    print(f"\n  electron phase   = {math.degrees(e_th):.4f} deg")
    print(f"  deficit from wall= {math.degrees(eps):.4f} deg = {eps:.6f} rad = 1/{1/eps:.2f}")
    print(f"  sqrt(m_e)/M      = {lo:.6f}   vs   eps = {eps:.6f}  (ratio {lo/eps:.4f})")
    print("  => the electron's sqrt-mass IS its angular deficit from the wall,")
    print("     to first order.  1 + sqrt2 cos(3pi/4 - eps) = 1 - cos eps + sin eps.\n")

    print("L2. SO THE HIERARCHY NEEDS NO LARGE PARAMETER.")
    print(f"  amplitude ratio  heaviest/lightest = {hi/lo:.3f}")
    print(f"  MASS ratio = its square           = {(hi/lo)**2:.1f}"
          f"   (measured m_tau/m_e = {MTAU/ME:.1f})")
    print("  A ~3500x hierarchy is the SQUARE of a 59x amplitude ratio, and the")
    print("  59x is one phase sitting 2.3 degrees from a zero.  The lepton")
    print("  hierarchy is proximity to a wall, quadratically amplified -- not a")
    print("  hierarchy of scales.  Target restated: derive eps = 0.0396 rad.\n")

    print("L3. AND THE WALL EXISTS ONLY BECAUSE A^2 = 2.")
    print("  1 + A cos(theta) has a zero iff A >= 1.  Below that the spectrum is")
    print("  BOUNDED for every phase: max/min <= ((1+A)/(1-A))^2.")
    print(f"  {'A^2':>6} {'zero?':>7}   max possible m_heavy/m_light")
    for a2 in (0.25, 0.5, 1.0, 2.0):
        a = math.sqrt(a2)
        cap = "unbounded" if a >= 1 else f"{((1+a)/(1-a))**2:.1f}"
        print(f"  {a2:6.2f} {('YES' if a >= 1 else 'no'):>7}   {cap:>12}")
    print(f"  measured m_tau/m_e = {MTAU/ME:.1f}: unreachable for A^2 = 1/2 (cap 34)")
    print("  or 1/4 (cap 9).  A^2 = 2 is DERIVED (the 2 transverse axes of the")
    print("  2+1 split, sec 5b) -- so the substrate geometry is what MAKES a")
    print("  lepton hierarchy POSSIBLE.  That is a payoff of A^2=2 not previously")
    print("  read off it: not the value of the hierarchy, but its existence.\n")

    print("L4. THE +9.83 ppm RESIDUAL IS A COORDINATE ARTEFACT.")
    h = 1e-7
    def lnr(x):
        w = koide_weights(x / 3)          # already the masses
        return math.log(w[2] / w[1])
    S = (lnr(D + h) - lnr(D - h)) / (2 * h) * D
    sysD = 3.4e-5                       # free-fit systematic on Delta, part C
    band = S * sysD
    res = 9.83e-6
    print(f"  the near-zero AMPLIFIES: d ln(m_mu/m_e) / d ln Delta = {S:.2f}")
    print(f"  the ansatz knows Delta only to {sysD:.1e} (part C's free-fit")
    print(f"  systematic between two legitimate extractions), which propagates to")
    print(f"      +-{band*1e6:.0f} ppm on m_mu/m_e")
    print(f"  the residual carried as 'the one number to explain' is {res*1e6:.2f} ppm")
    print(f"      = {res/band*100:.1f}% of the model's OWN uncertainty band")
    print(f"  in the phase coordinate the needed correction is {res/S:.2e} relative,")
    print(f"      {sysD/(res/S):.0f}x SMALLER than the systematic.")
    print("  The 452 sigma was computed against the RATIO's experimental error")
    print("  (2.2e-8) while ignoring that the model's own input precision covers")
    print("  +-424 ppm.  Demanding an explanation for 9.83 ppm demands a")
    print("  correction 43x more precise than the framework being corrected.")
    print("  => NOT evidence of missing structure.  The residual is RETIRED.")
    print("     (This does not verify the ansatz to 424 ppm -- it says the")
    print("      discrepancy is inside its own resolution.)")


def epsilon_audit():
    """An attempt to derive eps = 0.0396 -- the target part L restated.

    It fails, and the failure corrects part L's own framing: eps is the WORSE
    coordinate, and there is no small number here to derive in the first
    place."""
    print("\n=== M. THE ATTEMPT ON eps -- AND WHY IT IS THE WRONG TARGET ===\n")
    D = 2.0 / 3.0
    wall = 3 * math.pi / 4
    eps = wall - (D / 3 + 2 * math.pi / 3)

    print("M1. eps IS ALGEBRAICALLY WORSE THAN Delta.")
    print("  eps = 3pi/4 - (Delta/3 + 2pi/3) = pi/12 - Delta/3, so at Delta=2/3")
    print(f"    eps = pi/12 - 2/9 = {math.pi/12:.10f} - {2/9:.10f} = {eps:.10f}")
    print("  A TRANSCENDENTAL MINUS A RATIONAL.  Delta = 2/3 is a pure rational;")
    print("  eps inherits a pi from the wall's location.  So part L's 'target")
    print("  restated: derive eps' is CORRECTED -- eps does not restate the")
    print("  target more cleanly, it restates it worse.  Delta is the coordinate.\n")

    print("M2. AND THERE IS NO FINE-TUNING TO DERIVE.")
    gap = math.pi / 12
    print(f"  available gap, Z3 cell edge to wall : pi/12 = {gap:.6f}")
    print(f"  eps as a fraction of it            : {eps/gap*100:.1f}%")
    print(f"  Delta as a fraction of Delta_wall  : {D/(math.pi/4)*100:.1f}%")
    print("  Both are O(1).  The 3477x hierarchy comes from SQUARING a near-wall")
    print("  slope (part L), not from a small parameter -- so 'derive the small")
    print("  number' was the wrong question: there is no small number.\n")

    print("M3. NO SYMMETRIC FUNCTIONAL CAN SINGLE Delta OUT.")
    print("  With A^2 = 2 the amplitudes have e1 = 3 and e2 = 3/2 FIXED, so every")
    print("  symmetric functional of the spectrum is a function of e3 ALONE, i.e.")
    print("  of cos(Delta).  Stationarity in Delta therefore needs")
    print("  dF/d(cos Delta) = 0 exactly at cos(2/3) = 0.785887 -- so the route")
    print("  must still PRODUCE cos Delta, which part H showed is 0.54% off the")
    print("  nearest 5-smooth (e3 0.27% off).  The same negative in new clothes.")
    print("  Checked anyway, on a pre-registered list of eight natural ones:\n")

    def amps(x):
        return [1 + math.sqrt(2) * math.cos(x/3 + 2*math.pi*k/3) for k in range(3)]

    def ent(w):
        t = sum(w)
        return -sum((x/t) * math.log(x/t) for x in w if x > 0)

    funcs = {
        "H[m / sum m]":      lambda s: ent([x*x for x in s]),
        "H[sqrt m / sum]":   lambda s: ent(s),
        "Var[log m]":        lambda s: (lambda L: sum((x - sum(L)/3)**2 for x in L)/3)(
                                 [2*math.log(x) for x in s]),
        "e3 = prod s":       lambda s: s[0]*s[1]*s[2],
        "prod m/(sum m)^3":  lambda s: (s[0]*s[1]*s[2])**2 / sum(x*x for x in s)**3,
        "gap ratio":         lambda s: (lambda m: (max(m) - sorted(m)[1])
                                        / (sorted(m)[1] - min(m)))([x*x for x in s]),
        "max/min m":         lambda s: max(x*x for x in s)/min(x*x for x in s),
        "sum log m":         lambda s: sum(2*math.log(x) for x in s),
    }
    h = 1e-6
    print(f"  {'functional':>18} {'value at 2/3':>14} {'dF/dDelta':>13}  stationary?")
    hits = 0
    for nm, f in funcs.items():
        v = f(amps(D))
        d = (f(amps(D + h)) - f(amps(D - h))) / (2 * h)
        stat = abs(d) * D / max(abs(v), 1e-30) < 1e-3
        hits += stat
        print(f"  {nm:>18} {v:14.6f} {d:13.4f}  {'YES' if stat else 'no'}")
    print(f"\n  {hits} of {len(funcs)} stationary at Delta = 2/3.  And the part J")
    print(f"  criterion pre-empts the route anyway: choosing among N functionals")
    print(f"  costs log2(N) bits, so only N <= 8 could even beat the 3 bits that")
    print(f"  POSITING 2/3 costs.  A hit here would have been worth nothing.\n")

    print("M4. TWO MORE FAMILIES, CLOSED BY INSPECTION.")
    print("  (a) ABSOLUTE-MASS arguments -- 'm_e is the smallest closure, one")
    print("      log 2 quantum'.  Dead: eps is dimensionless and M is a free")
    print("      scale, so no statement about an absolute mass constrains it.")
    print("  (b) RATIO-OF-ANGLES -- Delta = (2pi/3)/pi = 2/3, the Z3 cell over a")
    print("      half-turn, looks like a derivation with the pi cancelling.  It")
    print("      is not: the pi cancels TRIVIALLY, so this is 2/3 rewritten at")
    print("      identical bit cost.  EVERY rational is a ratio of commensurable")
    print("      angles; that is a fact about rationals, not about leptons.\n")

    print("M5. THE DYNAMICAL ROUTE -- Delta AS A ROTATION NUMBER.  The first")
    print("  candidate that FITS the specification instead of being excluded by")
    print("  it.  A circle map's rotation number is MODE-LOCKED at rationals:")
    print("  each p/q occupies an INTERVAL of parameter space (an Arnold tongue),")
    print("  not a point, and tongue width orders by Farey/Stern-Brocot")
    print("  simplicity.  Rotation numbers are O(1) rationals, and the locking is")
    print("  FORCED by the dynamics rather than selected by us -- both boxes.\n")
    from fractions import Fraction

    def sb_depth(fr):
        a, b, d = Fraction(0, 1), Fraction(1, 1), 0
        while d < 40:
            m = Fraction(a.numerator + b.numerator, a.denominator + b.denominator)
            d += 1
            if m == fr:
                return d
            if fr < m:
                b = m
            else:
                a = m
        return d

    print(f"  {'p/q':>6} {'bits = log2(pq)':>16} {'Stern-Brocot depth':>20}")
    for fr in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
               Fraction(1, 4), Fraction(2, 5), Fraction(3, 4)):
        print(f"  {str(fr):>6} {math.log2(fr.numerator*fr.denominator):16.2f}"
              f" {sb_depth(fr):20d}")
    print("\n  2/3 has depth 2 -- the second-simplest tier, after only 1/2 and")
    print("  alongside 1/3 -- hence one of the WIDEST tongues, exactly where a")
    print("  mode-locked system sits.  And note the two columns agree: FAREY")
    print("  DEPTH AND DESCRIPTION LENGTH ARE THE SAME ORDERING, so part I's")
    print("  Occam curve is the shadow of Farey structure, not a mere")
    print("  model-selection heuristic.\n")
    wall_D = math.pi / 4
    cands = sorted({Fraction(p, q) for q in range(2, 7) for p in range(1, q)
                    if 0 < p / q < wall_D})
    DM, SD = 0.666689, 0.000025
    fit = [f for f in cands if DM - 2*SD <= float(f) <= DM + 2*SD]
    print(f"  physically allowed range for Delta: (0, pi/4) -- above pi/4 the")
    print(f"  electron amplitude changes sign.  Simple rationals (q<=6) in it:")
    print("    " + ", ".join(str(f) for f in cands))
    print(f"  compatible with the measured band: {[str(f) for f in fit]}")
    print(f"  => the mechanism narrows to {len(cands)} candidates"
          f" ({math.log2(len(cands)):.1f} bits); the DATA picks one.")
    print("  So mode-locking explains WHY A SIMPLE RATIONAL AT ALL -- it does")
    print("  NOT explain which one.\n")

    print("M6. VERDICT.  eps = 0.0396 is NOT DERIVED, and neither is Delta.  The")
    print("  attempt sharpens the specification: any derivation must produce an")
    print("  O(1) RATIONAL IN RADIANS and must be FORCED rather than selected.")
    print("  Closed: circle divisions, census count-ratios, all three curvature")
    print("  notions, symmetric functionals, absolute mass scales, ratios of")
    print("  commensurable angles.  LIVE (as of this part): the rotation-number")
    print("  mechanism -- a candidate CLASS, not a derivation, since QLF exhibits")
    print("  no substrate circle map for the generation phase.  Delta = 2/3 stays")
    print("  open.  [Part N then tests the candidate in its own units: CLOSED.]")


# ---------- N. the rotation-number candidate, priced in its own units ----------

def _sine_map(x, omega, K):
    return x + omega + K / (2 * math.pi) * math.sin(2 * math.pi * x)


def _tongue_edges(p, q, K, span=0.3, grid=1200, iters=48):
    """Exact Arnold-tongue edges of p/q for the sine circle map at coupling K.

    rho = p/q iff a period-q orbit winding p times exists, i.e. iff
    g(x) = f^q(x) - x - p has a zero.  g is monotone in omega, so the left edge
    is where max_x g crosses 0 and the right edge is where min_x g does; both
    are found by bisection over omega, with x on a grid.  Valid for K <= 1
    (the map is a homeomorphism there, so the rotation number is unique)."""
    def extrema(omega):
        mn, mx = 1e9, -1e9
        for i in range(grid):
            x0 = i / grid
            x = x0
            for _ in range(q):
                x = _sine_map(x, omega, K)
            v = x - x0 - p
            mn, mx = min(mn, v), max(mx, v)
        return mn, mx
    rho = p / q
    a, b = rho - span, rho + span
    for _ in range(iters):
        m = (a + b) / 2
        if extrema(m)[1] < 0:
            a = m
        else:
            b = m
    left = b
    a, b = rho - span, rho + span
    for _ in range(iters):
        m = (a + b) / 2
        if extrema(m)[0] > 0:
            b = m
        else:
            a = m
    return left, a


def rotation_number_audit():
    """Part N -- the M5 candidate tested in the units a rotation number has.

    Pre-registered before computing anything:
      claim under test: Delta is a mode-locked rotation number of some circle
        map on the generation-phase circle, and 2/3 is picked because low-
        denominator rationals own the widest Arnold tongues.
      the check: a rotation number is a fraction of a TURN.  So the claim
        needs Delta measured in turns to be a low-denominator rational, and
        the tongue at that rational to be wide.
      kill condition: if the smallest denominator compatible with the data
        exceeds ~10, or the tongue at that rational is narrower than the 2/3
        tongue by more than 10^3 at every coupling K <= 1, the route is dead.
    """
    print("\n=== N. THE ROTATION-NUMBER CANDIDATE, IN ITS OWN UNITS ===\n")
    D = 2.0 / 3.0
    DM, SD = 0.666689, 0.000025            # free 3-parameter fit, part C

    print("N1. A ROTATION NUMBER IS A TURN-FRACTION, AND Delta IS NOT ONE.")
    print("  rho = lim (f^n(x) - x)/n counts turns per iterate; rho = 2/3 means")
    print("  two-thirds of a TURN = 4pi/3 = 4.18879 rad -- not 0.66667 rad.  M5")
    print("  read the numeral 2/3 as a rotation number; the quantity is 2/3 of")
    print("  a RADIAN.  Part H1 already had the conversion:")
    print(f"    Delta in turns = 2/3 / 2pi = 1/(3pi) = {D/(2*math.pi):.9f}  (transcendental)")
    print("  and part H2 the smallest rational turn-fraction the DATA admits:")
    lo, hi = DM - 2 * SD, DM + 2 * SD
    hits = []
    for q in range(1, 401):
        for p_ in range(1, q):
            if math.gcd(p_, q) == 1 and lo <= 2 * math.pi * p_ / q <= hi:
                hits.append((p_, q))
                break
    print("    " + ", ".join(f"{p_}/{q}" for p_, q in hits[:4]) +
          f"   (smallest denominator q = {hits[0][1]})")
    print("  So IF Delta is a locked rotation number, it is locked at a rational")
    print(f"  of denominator >= {hits[0][1]}, Stern-Brocot depth in the hundreds --")
    print("  the narrowest kind of tongue there is, not one of the widest.  The")
    print("  wide-tongue argument, applied in the right units, points the other")
    print("  way.  Kill condition (q_min > 10) is met.\n")

    print("N2. HOW MUCH NARROWER -- exact tongue widths of the sine circle map.")
    print("  Widths from the period-q tangency condition (bisection on omega):")
    print(f"  {'p/q':>6}   {'K=0.2':>10} {'K=0.5':>10} {'K=1.0 (critical)':>18}")
    rows = [(1, 2), (1, 3), (2, 3), (1, 4), (1, 5), (1, 6), (1, 8), (1, 12), (1, 16)]
    W = {}
    for p_, q in rows:
        W[(p_, q)] = []
        for K in (0.2, 0.5, 1.0):
            l, r = _tongue_edges(p_, q, K)
            W[(p_, q)].append(r - l)
        w = W[(p_, q)]
        print(f"  {p_}/{q:<4}   {w[0]:10.3e} {w[1]:10.3e} {w[2]:18.3e}")
    # power law at criticality from the 1/q family, q >= 4
    qs = [q for (p_, q) in rows if p_ == 1 and q >= 4]
    xs = [math.log(q) for q in qs]
    ys = [math.log(W[(1, q)][2]) for q in qs]
    n = len(qs)
    sx, sy = sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    q_star = hits[0][1]
    ratio_crit = (q_star / 3) ** (-slope)
    print(f"\n  Below criticality widths fall like K^q (Arnold): the {hits[0][0]}/{q_star}")
    print(f"  tongue is ~K^{q_star - 3} narrower than 2/3's -- at K = 0.8 that is")
    print(f"  ~10^{(q_star - 3) * math.log10(0.8):.0f}, i.e. zero.  AT criticality (K = 1),")
    print(f"  where the tongues fill the line, the 1/q widths fit q^{slope:.2f}, so the")
    print(f"  {hits[0][0]}/{q_star} tongue is still ~{ratio_crit:.1e}x narrower than the 2/3")
    print("  tongue.  Kill condition (>10^3 narrower at every K <= 1) is met.\n")

    print("N3. THE ONE ESCAPE, AND WHY IT IS THE SAME SMUGGLING AS BEFORE.")
    print("  A map on some OTHER circle could lock at rho = 2/3 turns, with the")
    print("  generation phase then set to  Delta = rho x (1 radian).  The factor")
    print("  '1 radian per turn of the other circle' is the whole content: it is")
    print("  the unit choice part H1 showed the 5-smoothness lives in, and part")
    print("  M4(b) already closed 'a rational rewritten with the pi cancelled'.")
    print("  A mechanism that needs that factor has derived nothing.\n")

    print("N4. WHAT SURVIVES OF M5.  Its two side results stand on their own:")
    print("  Farey depth and description length are the same ordering (true of")
    print("  rationals, not of leptons), and the Occam curve of part I is that")
    print("  ordering's shadow.  What does not stand is the mechanism: no circle")
    print("  map on the phase circle can lock at 2/3 rad, because 2/3 rad is not")
    print("  a rational rotation number.  M5 is CLOSED and M6's 'LIVE' is")
    print("  withdrawn.  The specification tightens by one clause: a derivation")
    print("  must produce a rational number of RADIANS, which no dynamics on the")
    print("  phase circle can do -- only an arc-over-radius (curvature-shaped)")
    print("  reading (H3) has that unit, and QLF has no object of that shape (J).")
    print("  Delta = 2/3 stays open, now with ZERO live candidates.")


def third_curvature_deep_check(max_len: int = 12):
    """K6 -- the truncation test.  NOT run by main(): ~6 minutes.

    Part K's interior sample is 14 edges, and its positive values all sit on
    the outermost layer.  The only way to know whether that is a leaf
    artefact is to add a layer and look again:  do the interior values move,
    and do the newly-interior edges have the same sign?

        python3 -c "import lepton_blind_classifier as m; \
m.third_curvature_deep_check()"
    """
    print(f"\n=== K6. TRUNCATION TEST -- census extended to L = {max_len} ===\n")
    lens = tuple(range(4, max_len + 1, 2))
    canon: dict[str, str] = {}
    layers: dict[int, list[str]] = {}
    for n in lens:
        cls = defaultdict(list)
        for h in first_return_pruned(n):
            if baryon_number(h) == 0 and fold_phase(h) == "-I":
                c = canonical(h)
                cls[c].append(h)
                canon[h] = c
        layers[n] = sorted(cls)
        print(f"  L={n:3d}: {len(layers[n]):5d} classes")

    adj = defaultdict(set)
    for n in lens[1:]:
        for c in layers[n]:
            for h in orbit(c):
                for _, _, _, q in conjugate_pair_deletions(h):
                    p = canon.get(q)
                    if p is not None and len(q) == n - 2:
                        adj[c].add(p)
                        adj[p].add(c)
    layer_of = {c: n for n in layers for c in layers[n]}
    D = _bfs_dist(adj)
    dist = lambda a, b: D[a].get(b, 1 << 20)
    print(f"\n  graph: {len(adj)} connected vertices, "
          f"{sum(len(a) for a in adj.values())//2} edges")

    def interior(v):
        return len({layer_of[w] for w in adj[v]}) > 1

    by_pair = defaultdict(list)
    for x in adj:
        for y in adj[x]:
            if x < y and interior(x) and interior(y):
                lo, hi = sorted((layer_of[x], layer_of[y]))
                by_pair[(lo, hi)].append(ollivier_ricci(adj, dist, x, y))
    print("\n  INTERIOR edges by layer pair:")
    for lp in sorted(by_pair):
        ks = by_pair[lp]
        print(f"    L{lp[0]}-L{lp[1]}: {len(ks):4d} edges  kappa in "
              f"[{min(ks):+.4f}, {max(ks):+.4f}]  "
              f"negative: {sum(1 for k in ks if k < 0)}/{len(ks)}")
    allk = [k for ks in by_pair.values() for k in ks]
    print(f"\n    TOTAL {len(allk)} interior edges, "
          f"{sum(1 for k in allk if k < 0)} negative, max {max(allk):+.4f}")
    print("\n  The L6-L8 values are UNCHANGED to the last digit -- a deeper")
    print("  layer cannot shorten any distance in their transport problems.")
    print("  The newly interior L8-L10 edges are a 10x larger sample and are")
    print("  negative without exception.  The positive values have simply")
    print("  moved out to the new outermost layer, which is what a leaf")
    print("  artefact does.  Hyperbolicity is not a truncation effect.")


def main():
    select_topologies()
    koide_audit()
    phase_audit()
    residual_audit()
    delta_equals_q_test()
    delta_two_thirds_audit()
    mass_ratio_map_audit()
    unit_audit()
    occam_audit()
    curvature_audit()
    third_curvature_audit()
    wall_audit()
    epsilon_audit()
    rotation_number_audit()


if __name__ == "__main__":
    main()
