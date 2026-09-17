#!/usr/bin/env python3
"""evolutionary_census.py — evolutionary game theory on the closure census (quantum-os #209).

Step 1–3 of the plan posted on rchain-community/quantum-os#209: the strategy representation,
the pairwise match primitive, and the payoff→multiplicity mapping with its R6a check — run
BEFORE any population dynamics, because the mapping decides whether the test can fail at all.

Representation.  A strategy is a preparation strand: an open twist history over the six spatial
twists (the pattern contextual_census.py uses for preparations).  A match between strategies
`a` and `b` at horizon `t` is MultiParticle.search_for_entanglement's inner loop: each side
extends by `t` twists and the pair closes when the joint history achieves ZFA
(`twist_core.is_zfa` on `a + ca + b + cb` — the gate is the full ZFA predicate, per
QucalcSearch.md's gotcha, not the aggregate).

Two candidate payoff maps, both read off the census with no free parameter:

  P_joint(a,b) = #{(ca,cb) : is_zfa(a+ca+b+cb)}      the number of ways the PAIR closes
  P_own(a|b)   = #{ca : ∃cb, is_zfa(a+ca+b+cb)}      the number of a's own ways that b closes

R6a check on P_joint.  Joint ZFA is count balance of the concatenation (count balance ⟹ Pauli
closure, `count_balanced_pauli_closed`), and count balance is order-blind, so
P_joint(a,b) = P_joint(b,a): both players always receive the same number.  A symmetric
common-payoff 2×2 game is a potential game, and in a potential game the risk-dominant and the
payoff-dominant equilibrium coincide (both maximise the potential).  So under P_joint the
pre-registered test "does most-ways-first pick the risk-dominant equilibrium" cannot fail — it is
bookkeeping (Philosophy.md §3a rule 4).  Verified numerically below, then set aside.

P_own is not symmetric — b may close many of a's ways while a closes few of b's — so it can
produce coordination games in which risk dominance and payoff dominance DISAGREE: the Stag Hunt
proper.  That is where the population dynamics (steps 4–6) have content, and where the two
readings of "most ways happens first" part company:

  H_naive  the state with the larger diagonal multiplicity (payoff-dominant) is selected;
  H_KMR    the risk-dominant state is selected (Kandori–Mailath–Rob 1993, Young 1993 — the
           state reached by the most mutation paths, i.e. most ways to ARRIVE, not most ways AT).

Pre-registered kill condition for H_naive (to be run in step 4): the risk-dominant equilibrium is
the stochastically stable state on a majority of the Stag-Hunt-type seed pairs found here.

RESULT (recorded, not tuned around — ScientificApproach.md R2a).  At horizons 2 and 3:

  * P_joint is symmetric on every pair (as derived), and so is P_own — 0 of 861 seed pairs differ.
    The reason is general: with free same-length continuations on both sides, whether a's
    continuation is closable depends only on imb(a) + imb(b), a symmetric quantity.  So EVERY
    payoff built from joint ZFA of free continuations is a potential game: 216 coordination games,
    risk == payoff dominance in all 216, Stag-Hunt-type pairs: 0.
  * Making the strategy a behavioural rule (`--alphabets`: the move set a player is willing to
    twist — Y, X, Z, XY, YZ, XZ, XYZ) does make P_own asymmetric (u(Y|XYZ)=4 vs u(XYZ|Y)=8), but
    still yields 0 Stag-Hunt-type games: "own ways closed by the partner" is monotone in move-set
    inclusion, so the larger move set is simply dominant.  A Stag Hunt needs the ambitious
    strategy to be VULNERABLE when unmatched (u(S|H) < u(H|H)); free closure counting never
    punishes ambition, because a bigger alphabet closes more against everyone.

Consequence.  With fitness = closure multiplicity the evolutionary game is a potential game, and
for potential games the stochastically stable state IS the potential maximiser by theorem
(Blume 1993; Young 1993) — "most ways happens first" holds exactly, but as bookkeeping: no
distribution over ways could make it false, so steps 4–6 (Moran + mutation) would have no
content.  A discriminating test needs a payoff that breaks the potential structure — a cost of
holding a deep strand open (the free-action ledger, QLF_FreeEnergy) or an order-/capacity-
asymmetric closure — which is a modelling decision to make openly, not to fit here.

THE FREE-ACTION COST (step 3, second pass — decided openly on #209, not fitted).  The payoff
that breaks the potential structure must be parameter-free or it is a fitted kernel.  Measure both
sides in the census's own units: ways closed → information log₂ W (bits, QLF_ShannonFromCounts);
an open strand's free action F = the capacity it demands (its imbalance — one unclosed half-spin
per unit, one bit each, ΔF = log 2 per closure, QLF_FreeEnergy).  Net information in bits is
log₂ W − F, so

    fitness(a|b) = W_own(a|b) / 2^F(a)        (ways, discounted one factor of 2 per bit held open)

— the Kraft-weighting shape of the census itself, and no free constant.  A "Stag" is a strand
that commits to a deeper closure (F = 2); it pays whether or not the partner matches, so it can
now be VULNERABLE when unmatched.  Pre-registered before the dynamics were run:

  H_naive  the payoff-dominant state (larger diagonal fitness — "most ways AT") is selected;
  H_KMR    the risk-dominant state ("most ways to ARRIVE") is selected.
  Verdict = the absorbing state carrying the stationary mass of the Moran process with mutation
  as μ → 0 at the largest population, computed EXACTLY (birth–death product formula, no
  simulation) for N ∈ {10, 20, 50, 100}, μ ∈ {1e-2, 1e-4, 1e-6}.
  Kill condition for H_naive: risk-dominant wins on a majority of the Stag-Hunt-type pairs.

RESULT OF THE COST GAME (run as pre-registered, horizons 2 and 3): Stag-Hunt-type pairs: 0 — the
Moran verdict was never reached.  Reason: self-fitness is strictly decreasing in depth
(F=0: 36, F=1: 7.5, F=2: ≤ 1 at horizon 2), because a deeper open strand already has fewer
closing ways and the discount lowers it further; so a deep commitment is never payoff-dominant
against a shallower one, and a Stag Hunt requires exactly that.  Depth would need a BENEFIT the
count does not give (bits released at closure ∝ depth, the cascade reading) — a third modelling
choice, at which point the game is being built to produce the phenomenon (R2a).  Stopped there.

THE CENSUS'S OWN DYNAMIC (`--race`, the inversion decided on #209: look for game structure
EMERGING from the first-closure census rather than imposing a game).  Two open strands `a`, `b`
share one walk over the six spatial twists — the substrate's free steps, chosen by neither.  The
absorbing census's own events decide the run: at each step the walk can close `a` alone
(imb(walk) = −imb(a)), `b` alone, or the PAIR jointly (imb(walk) = −(imb(a)+imb(b)), the shared
closure of Chemistry.md / SEX.md); the first event ends the run.  A player's payoff is the
ontological one — did it get closed, own or joint — under the census's cylinder measure 6^−d.
No kernel: the payoff is the closure event's own frequency.  (Identical strands hitting their
common target split the closure: only one of two identical open strands can be absorbed by one
hit; the no-split rule changes only the same-vs-orthogonal order, not the population result.)

Pre-registered: P1 the best reply to any strand is its conjugate (joint closure at depth 0 —
complementarity emerges as anti-coordination); P2 no Stag-Hunt-type pair appears; P3 the
replicator dynamics settle at 1:1 within a conjugate pair (Fisher's sex-ratio argument).

RESULT (depth ≤ 14, exact rationals; ordering stable from depth 8 to 20):
  * P1 holds exactly: u(conjugate) = 1.000 ≫ u(orthogonal) ≈ 0.25 > u(same strand) ≈ 0.15.
    Like-with-like is the WORST partner (two identical strands race for one target),
    complementary pairs bind — SEX.md's pn-binds / pp-blocked pattern, from the census alone.
  * P2 holds: 21 anti-coordination pairs, 0 coordination games, 0 Stag Hunt.
  * P3 holds: every replicator run ends at exactly ½ : ½ within one conjugate pair.
  * NOT pre-registered, observed: the population SPONTANEOUSLY PICKS ONE AXIS.  The uniform
    state is an equilibrium (every strand earns 0.3559 against it) but is unstable; the other
    two axes go extinct, the winner set by initial conditions.  So the emergent structure is
    two-level: anti-coordination within an axis (complementarity, 1:1) and coordination ACROSS
    axes (three symmetric equilibria — a collective basis choice, "the basis belongs to the
    question", QLF_BasisIndependence).  The pair state repels an orthogonal invader
    (0.574 vs 0.247 per encounter).
  Unclosed mass ≈ 0.5–0.7 at these depths is the 3-D walk's transience — Kraft leakage, the
  payoffs are lower bounds with a stable ordering.

    python3 evolutionary_census.py               # seeds of length ≤ 2, horizon 2
    python3 evolutionary_census.py --t 3         # horizon 3 (slower)
    python3 evolutionary_census.py --alphabets   # strategies as move sets, horizons 2 and 3
    python3 evolutionary_census.py --cost        # the free-action-cost game + exact Moran verdict
    python3 evolutionary_census.py --race        # the emergent first-closure race + replicator
"""
import argparse
import itertools
import sys
import time
from collections import Counter

sys.path.insert(0, ".")
from twist_core import is_zfa, spatial_free_action

SPATIAL = ['^', 'v', '<', '>', '/', '\\']
PAIRS = (('^', 'v'), ('>', '<'), ('/', '\\'), ('+', '-'))


def count_balanced(h: str) -> bool:
    c = Counter(h)
    return all(c[a] == c[b] for a, b in PAIRS)


def continuations(t: int):
    return [''.join(p) for p in itertools.product(SPATIAL, repeat=t)]


def match(a: str, b: str, t: int, conts):
    """Return (P_joint(a,b), P_own(a|b), P_own(b|a)) at horizon t."""
    joint = 0
    own_a = set()
    own_b = set()
    for ca in conts:
        pa = a + ca
        for cb in conts:
            h = pa + b + cb
            # count balance is the cheap necessary condition; the gate is still the full is_zfa
            if count_balanced(h) and is_zfa(h):
                joint += 1
                own_a.add(ca)
                own_b.add(cb)
    return joint, len(own_a), len(own_b)


def classify(u_xx, u_xy, u_yx, u_yy):
    """2×2 symmetric game with row payoffs u(p|q): p's payoff against q.

    coordination: each strategy is a strict best reply to itself.
    payoff-dominant: the diagonal with the larger payoff.
    risk-dominant (Harsanyi–Selten, symmetric case): x iff (u_xx − u_yx) > (u_yy − u_xy).
    """
    coord = u_xx > u_yx and u_yy > u_xy
    if not coord:
        return None
    pd = 'x' if u_xx > u_yy else ('y' if u_yy > u_xx else 'tie')
    dx, dy = u_xx - u_yx, u_yy - u_xy
    rd = 'x' if dx > dy else ('y' if dy > dx else 'tie')
    return pd, rd


ALPHABETS = {
    'Y': ['^', 'v'], 'X': ['<', '>'], 'Z': ['/', '\\'],
    'XY': ['^', 'v', '<', '>'], 'YZ': ['^', 'v', '/', '\\'], 'XZ': ['<', '>', '/', '\\'],
    'XYZ': ['^', 'v', '<', '>', '/', '\\'],
}


def match_alphabets(A: str, B: str, t: int):
    """Strategies as move sets: P_own(A|B) counts A's continuations (over A's alphabet) that some
    continuation of B (over B's alphabet) closes."""
    ca_ok, cb_ok, joint = set(), set(), 0
    conts_a = [''.join(p) for p in itertools.product(ALPHABETS[A], repeat=t)]
    conts_b = [''.join(p) for p in itertools.product(ALPHABETS[B], repeat=t)]
    for ca in conts_a:
        for cb in conts_b:
            h = ca + cb
            if count_balanced(h) and is_zfa(h):
                joint += 1
                ca_ok.add(ca)
                cb_ok.add(cb)
    return joint, len(ca_ok), len(cb_ok)


def alphabet_scan():
    names = list(ALPHABETS)
    for t in (2, 3):
        own = {}
        for A in names:
            own[(A, A)] = match_alphabets(A, A, t)[1]
        for A, B in itertools.combinations(names, 2):
            _, oa, ob = match_alphabets(A, B, t)
            own[(A, B)], own[(B, A)] = oa, ob
        print(f"\n== strategies as move sets, horizon t={t}: P_own(A|B) ==")
        print("       " + "".join(f"{n:>6}" for n in names))
        for A in names:
            print(f"{A:>6} " + "".join(f"{own[(A, B)]:6d}" for B in names))
        sh, coord, agree = [], 0, 0
        for x, y in itertools.combinations(names, 2):
            c = classify(own[(x, x)], own[(x, y)], own[(y, x)], own[(y, y)])
            if c:
                coord += 1
                if c[0] == c[1]:
                    agree += 1
                elif 'tie' not in c:
                    sh.append((x, y, c))
        print(f"coordination games: {coord}   risk==payoff: {agree}   STAG-HUNT-TYPE: {len(sh)} {sh}")


def moran_stationary(uAA, uAB, uBA, uBB, N, mu, eps=1e-12):
    """Exact stationary distribution of the two-strategy Moran process with mutation on
    i = #A ∈ {0..N}: reproduce ∝ fitness, offspring mutates w.p. mu, replaces a uniform
    individual.  Birth–death chain ⟹ pi_i ∝ ∏_{k=1}^{i} T+(k−1)/T−(k).  Returns pi_N/(pi_0+pi_N)
    — the share of the absorbing mass at all-A."""
    def fit(i):
        if N == 1:
            return uAA, uBB
        fA = ((i - 1) * uAA + (N - i) * uAB) / (N - 1) if i > 0 else 0.0
        fB = (i * uBA + (N - i - 1) * uBB) / (N - 1) if i < N else 0.0
        return max(fA, 0.0) + eps, max(fB, 0.0) + eps
    import math
    logpi = [0.0]
    for k in range(1, N + 1):
        # T+(k-1): from k-1 A's to k
        i = k - 1
        fA, fB = fit(i)
        tot = i * fA + (N - i) * fB
        pA = i * fA / tot
        pB = (N - i) * fB / tot
        Tp = (pA * (1 - mu) + pB * mu) * (N - i) / N
        # T-(k): from k A's to k-1
        i = k
        fA, fB = fit(i)
        tot = i * fA + (N - i) * fB
        pA = i * fA / tot
        pB = (N - i) * fB / tot
        Tm = (pB * (1 - mu) + pA * mu) * i / N
        logpi.append(logpi[-1] + math.log(Tp) - math.log(Tm))
    m = max(logpi)
    w = [math.exp(x - m) for x in logpi]
    return w[N] / (w[0] + w[N])


def cost_game(seeds, own):
    """fitness(a|b) = W_own(a|b) / 2^F(a), F = spatial free action of the seed."""
    F = {a: spatial_free_action(a) for a in seeds}
    u = {(a, b): own[(a, b)] / (2.0 ** F[a]) for (a, b) in own}
    return u, F


def cost_scan(seeds, own, t):
    u, F = cost_game(seeds, own)
    stag_hunt, coord, agree = [], 0, 0
    for x, y in itertools.combinations(seeds, 2):
        c = classify(u[(x, x)], u[(x, y)], u[(y, x)], u[(y, y)])
        if not c:
            continue
        coord += 1
        pd, rd = c
        if pd == rd:
            agree += 1
        elif 'tie' not in (pd, rd):
            stag_hunt.append((x, y, pd, rd))
    print(f"\n=== free-action cost game, horizon {t}: fitness = W_own / 2^F ===")
    print(f"seed pairs: {len(seeds) * (len(seeds) - 1) // 2}   coordination games: {coord}   "
          f"risk==payoff: {agree}   STAG-HUNT-TYPE: {len(stag_hunt)}")
    if not stag_hunt:
        print("no Stag-Hunt-type pair: nothing to test at this horizon")
        return
    Ns, mus = (10, 20, 50, 100), (1e-2, 1e-4, 1e-6)
    naive_wins = kmr_wins = 0
    print(f"{'pair':16} {'F':>5} {'u(x|x)':>8} {'u(x|y)':>8} {'u(y|x)':>8} {'u(y|y)':>8}  pd rd  "
          + "  ".join(f"N={N}" for N in Ns) + "   selected")
    for x, y, pd, rd in stag_hunt:
        row = []
        for N in Ns:
            share = moran_stationary(u[(x, x)], u[(x, y)], u[(y, x)], u[(y, y)], N, mus[-1])
            row.append(share)
        # verdict at the largest N, smallest mu: which absorbing state holds the mass
        sel = 'x' if row[-1] > 0.5 else 'y'
        if sel == pd:
            naive_wins += 1
        if sel == rd:
            kmr_wins += 1
        print(f"{x!r:>7} vs {y!r:<6} {F[x]:d},{F[y]:d} {u[(x,x)]:8.3f} {u[(x,y)]:8.3f} "
              f"{u[(y,x)]:8.3f} {u[(y,y)]:8.3f}   {pd}  {rd}  "
              + "  ".join(f"{r:4.2f}" for r in row) + f"   {sel} (share of x at all-x)")
    n = len(stag_hunt)
    print(f"\nverdict at N={Ns[-1]}, mu={mus[-1]}: payoff-dominant selected on {naive_wins}/{n}, "
          f"risk-dominant selected on {kmr_wins}/{n}")
    print("H_naive " + ("KILLED" if kmr_wins > n / 2 else "survives") +
          " (kill condition: risk-dominant wins on a majority);  H_KMR " +
          ("supported" if kmr_wins > n / 2 else "not supported"))
    # sensitivity: does the verdict depend on mu at the largest N?
    flips = 0
    for x, y, pd, rd in stag_hunt:
        sels = set()
        for mu in mus:
            share = moran_stationary(u[(x, x)], u[(x, y)], u[(y, x)], u[(y, y)], Ns[-1], mu)
            sels.add('x' if share > 0.5 else 'y')
        if len(sels) > 1:
            flips += 1
    print(f"pairs whose verdict at N={Ns[-1]} changes with mu across {mus}: {flips}/{n}")


_STEP = {'^': (0, 1, 0), 'v': (0, -1, 0), '>': (1, 0, 0), '<': (-1, 0, 0),
         '/': (0, 0, 1), '\\': (0, 0, -1)}


def _imb(s):
    v = [0, 0, 0]
    for c in s:
        v = [v[i] + _STEP[c][i] for i in range(3)]
    return tuple(v)


def race_payoff(a: str, b: str, D: int, split: bool = True):
    """Exact first-event masses under the cylinder measure 6^-d for two open strands sharing one
    walk.  Returns (u_a, unclosed) with u_a = mass of runs in which `a` is closed (own or joint)
    before `b` wins the race."""
    from fractions import Fraction
    from collections import defaultdict
    add = lambda u, v: tuple(x + y for x, y in zip(u, v))
    neg = lambda u: tuple(-x for x in u)
    tA, tB, tJ = neg(_imb(a)), neg(_imb(b)), neg(add(_imb(a), _imb(b)))
    mA = mB = mJ = Fraction(0)
    states = {(0, 0, 0): Fraction(1)}
    for d in range(D + 1):
        nxt = defaultdict(Fraction)
        for st, m in states.items():
            if st == tJ:
                mJ += m
                continue
            if st == tA and st == tB:
                if split:
                    mA += m / 2
                    mB += m / 2
                else:
                    mA += m
                    mB += m
                continue
            if st == tA:
                mA += m
                continue
            if st == tB:
                mB += m
                continue
            if d == D:
                continue
            for c in SPATIAL:
                nxt[add(st, _STEP[c])] += m / 6
        states = nxt
    return float(mA + mJ), float(1 - mA - mB - mJ)


def race_game(D: int = 14):
    import random
    n = len(SPATIAL)
    U = [[race_payoff(a, b, D)[0] for b in SPATIAL] for a in SPATIAL]
    print(f"=== the emergent first-closure race, six open unit strands, depth <= {D} ===")
    print("u(a|b) = P(a closed, own or joint, before b wins):")
    for i, a in enumerate(SPATIAL):
        print(f"  {a:>2} " + " ".join(f"{U[i][j]:6.3f}" for j in range(n)))
    for i, a in enumerate(SPATIAL):
        br = max(range(n), key=lambda j: U[j][i])
        print(f"  best reply to {a!r}: {SPATIAL[br]!r} ({U[br][i]:.3f})")
    kinds = {'coord': 0, 'anti': 0, 'dominance': 0}
    sh = []
    for i, j in itertools.combinations(range(n), 2):
        uxx, uxy, uyx, uyy = U[i][i], U[i][j], U[j][i], U[j][j]
        if uxx > uyx and uyy > uxy:
            kinds['coord'] += 1
            c = classify(uxx, uxy, uyx, uyy)
            if c and c[0] != c[1] and 'tie' not in c:
                sh.append((SPATIAL[i], SPATIAL[j]))
        elif uyx > uxx and uxy > uyy:
            kinds['anti'] += 1
        else:
            kinds['dominance'] += 1
    print(f"pair types: {kinds}   Stag-Hunt-type: {sh}")

    def replicator(x, steps=20000, dt=0.05):
        for _ in range(steps):
            f = [sum(U[i][j] * x[j] for j in range(n)) for i in range(n)]
            phi = sum(x[i] * f[i] for i in range(n))
            x = [x[i] + dt * x[i] * (f[i] - phi) for i in range(n)]
            tot = sum(x)
            x = [v / tot for v in x]
        return x
    random.seed(1)
    print("replicator dynamics from random starts -> final shares (^ v < > / \\):")
    for _ in range(6):
        x = [random.random() for _ in range(n)]
        tot = sum(x)
        xf = replicator([v / tot for v in x])
        axes = [(xf[0] + xf[1]), (xf[2] + xf[3]), (xf[4] + xf[5])]
        win = max(range(3), key=lambda k: axes[k])
        pair = (xf[2 * win], xf[2 * win + 1])
        print("  " + " ".join(f"{v:.3f}" for v in xf) +
              f"   axis shares {axes[0]:.2f} {axes[1]:.2f} {axes[2]:.2f}  winning pair split "
              f"{pair[0]:.3f}:{pair[1]:.3f}")
    x = [1 / n] * n
    f = [sum(U[i][j] * x[j] for j in range(n)) for i in range(n)]
    print(f"uniform state: every strand earns {f[0]:.4f} (an equilibrium) -- unstable above")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t', type=int, default=2, help='horizon: continuation length per side')
    ap.add_argument('--maxseed', type=int, default=2, help='max seed length')
    ap.add_argument('--alphabets', action='store_true', help='strategies as move sets (see docstring)')
    ap.add_argument('--cost', action='store_true', help='the free-action-cost game + exact Moran verdict')
    ap.add_argument('--race', action='store_true', help='the emergent first-closure race + replicator dynamics')
    args = ap.parse_args()
    if args.alphabets:
        alphabet_scan()
        return
    if args.race:
        race_game()
        return

    seeds = [''.join(p) for L in range(1, args.maxseed + 1)
             for p in itertools.product(SPATIAL, repeat=L)]
    conts = continuations(args.t)
    print(f"seeds: {len(seeds)} (length ≤ {args.maxseed}), continuations per side: {len(conts)} "
          f"(horizon {args.t}), joint pairs per match: {len(conts)**2}")

    t0 = time.time()
    # self-matches and cross-matches, cached; P_own is asymmetric so store both orders
    joint = {}
    own = {}
    for a in seeds:
        j, oa, _ = match(a, a, args.t, conts)
        joint[(a, a)] = j
        own[(a, a)] = oa
    for a, b in itertools.combinations(seeds, 2):
        j, oa, ob = match(a, b, args.t, conts)
        joint[(a, b)] = j
        joint[(b, a)] = j
        own[(a, b)] = oa      # a's ways closed by b
        own[(b, a)] = ob      # b's ways closed by a
    print(f"census done in {time.time() - t0:.1f}s")

    # ---- R6a on P_joint: symmetric ⟹ risk dominance ≡ payoff dominance ----
    print("\n=== R6a: P_joint (ways the PAIR closes) ===")
    import random
    random.seed(0)
    sample = random.sample(list(itertools.combinations(seeds, 2)), min(120, len(seeds) * (len(seeds) - 1) // 2))
    asym = sum(1 for a, b in sample if joint[(a, b)] != match(b, a, args.t, conts)[0])
    print(f"P_joint(a,b) != P_joint(b,a) on {asym} of {len(sample)} sampled pairs "
          f"(expected 0: joint ZFA is count balance, order-blind)")
    n_coord = n_agree = 0
    for x, y in itertools.combinations(seeds, 2):
        c = classify(joint[(x, x)], joint[(x, y)], joint[(y, x)], joint[(y, y)])
        if c:
            n_coord += 1
            if c[0] == c[1]:
                n_agree += 1
    print(f"coordination games under P_joint: {n_coord}; risk-dominant == payoff-dominant in "
          f"{n_agree} of them  (expected all: a symmetric common-payoff game is a potential game)")
    print("=> under P_joint the KMR test cannot fail: bookkeeping, set aside.")

    # ---- P_own: the asymmetric map ----
    print("\n=== P_own (a's OWN ways closed by b) ===")
    n_coord = 0
    stag_hunt = []
    agree = 0
    for x, y in itertools.combinations(seeds, 2):
        u_xx, u_xy, u_yx, u_yy = own[(x, x)], own[(x, y)], own[(y, x)], own[(y, y)]
        c = classify(u_xx, u_xy, u_yx, u_yy)
        if not c:
            continue
        n_coord += 1
        pd, rd = c
        if pd == rd:
            agree += 1
        elif 'tie' not in (pd, rd):
            stag_hunt.append((x, y, (u_xx, u_xy, u_yx, u_yy), pd, rd))
    print(f"seed pairs: {len(seeds) * (len(seeds) - 1) // 2}   coordination games: {n_coord}   "
          f"risk==payoff: {agree}   STAG-HUNT-TYPE (risk != payoff, no tie): {len(stag_hunt)}")
    for x, y, u, pd, rd in stag_hunt[:20]:
        print(f"  {x!r:6} vs {y!r:6}  u(x|x)={u[0]:3d} u(x|y)={u[1]:3d} u(y|x)={u[2]:3d} u(y|y)={u[3]:3d}"
              f"   payoff-dominant={pd}  risk-dominant={rd}")
    if len(stag_hunt) > 20:
        print(f"  ... {len(stag_hunt) - 20} more")
    if args.cost:
        cost_scan(seeds, own, args.t)
        return
    if stag_hunt:
        print("\nPre-registered for step 4 (Moran process with vanishing mutation on these pairs):")
        print("  H_naive: payoff-dominant state selected;  H_KMR: risk-dominant state selected.")
        print("  Kill condition for H_naive: risk-dominant wins on a majority of the pairs above.")
    else:
        print("\nNo Stag-Hunt-type pair at this horizon: the census game is a pure potential game "
              "here and steps 4–6 would have no content. Try a larger --t before concluding.")


if __name__ == "__main__":
    main()
