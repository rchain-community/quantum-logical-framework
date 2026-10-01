#!/usr/bin/env python3
"""
fullerene_zfa_dna.py -- the ZFA DNA of the fullerenes, the highest-T_c carbon superconductors (K3C60 18 K,
Cs3C60 38 K). Carbon_Superconductivity.md sec 16.

The Goldberg-Coxeter construction builds every icosahedral fullerene from an Eisenstein integer z = h + k w:
C_{20 T} with T = |z|^2 = h^2 + hk + k^2, the triangulation number of Caspar & Klug (1962). It is the same index as the sheet DNAs
and the moire cells of moire_zfa_dna.py: z scales a patch of the graphene sheet by |z| and rotates it by arg z,
and the fullerene is that patch folded onto the 20 faces of an icosahedron. Its dual is the geodesic icosa-sphere
of Geometry_Of_Space.md sec 1 (the Fuller blanket), whose 12 five-fold vertices (`pentamons_invariant`) are the
fullerene's 12 pentagons.

  sec 1  two independent constructions -- dual of the class-I geodesic subdivision (z = v), and the leapfrog
         operation (z = 1 - w, T x 3) -- and the DNA check: leapfrog twice = z (1 - w)^2 = -3w z, a unit times 3,
         so it must give the same fullerene as subdividing three times as finely. It does.
  sec 2  the sign alternation on a cage. Graphene's sublattices are the two twist signs (carbon_zfa_dna.py sec 1);
         a pentagon is an odd ring, so a cage cannot alternate everywhere. The fewest bonds that must break the
         alternation (the bipartite edge frustration; Doslic & Vukicevic 2007) is a minimum T-join pairing the 12
         pentagons in the dual (Hadlock 1975), computed exactly.
  sec 3  what this gives, and what it does not.

Stdlib only.   Run:  python3 fullerene_zfa_dna.py
"""
from __future__ import annotations

import itertools
import math
from collections import deque

PHI = (1 + 5 ** 0.5) / 2


def rule(t: str) -> None:
    print("\n" + "=" * 78 + "\n" + t + "\n" + "-" * 78)


# --------------------------------------------------------------------------- #
# polyhedra as (faces: list of vertex cycles)
# --------------------------------------------------------------------------- #
def icosahedron():
    pts = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            pts += [(0, s1, s2 * PHI), (s1, s2 * PHI, 0), (s2 * PHI, 0, s1)]
    n = len(pts)
    d2 = lambda a, b: sum((x - y) ** 2 for x, y in zip(pts[a], pts[b]))
    edges = {(a, b) for a in range(n) for b in range(a + 1, n) if abs(d2(a, b) - 4) < 1e-9}
    faces = []
    for a, b, c in itertools.combinations(range(n), 3):
        if (a, b) in edges and (b, c) in edges and (a, c) in edges:
            # orient outward
            u = [pts[b][i] - pts[a][i] for i in range(3)]
            w = [pts[c][i] - pts[a][i] for i in range(3)]
            nrm = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
            cen = [pts[a][i] + pts[b][i] + pts[c][i] for i in range(3)]
            faces.append((a, b, c) if sum(x * y for x, y in zip(nrm, cen)) > 0 else (a, c, b))
    assert len(faces) == 20
    return faces


def geodesic(v: int):
    """Class-I subdivision of the icosahedron at frequency v: triangles over points keyed by barycentric weights."""
    tri = []
    for a, b, c in icosahedron():
        def key(i, j):
            k = v - i - j
            return tuple(sorted((x, w) for x, w in ((a, i), (b, j), (c, k)) if w > 0))
        for i in range(v):
            for j in range(v - i):
                tri.append((key(i + 1, j), key(i, j + 1), key(i, j)))          # "up" triangle
                if i + j < v - 1:
                    tri.append((key(i + 1, j), key(i + 1, j + 1), key(i, j + 1)))   # "down" triangle
    return tri


def dual_of_triangulation(tri):
    """Fullerene from a triangulated sphere: vertices = triangles; faces = cycles of triangles around each point."""
    around = {}
    for t, (p, q, r) in enumerate(tri):
        for x in (p, q, r):
            around.setdefault(x, []).append(t)
    edge_tris = {}
    for t, (p, q, r) in enumerate(tri):
        for e in ((p, q), (q, r), (r, p)):
            edge_tris.setdefault(frozenset(e), []).append(t)
    faces = []
    for x, ts in around.items():
        # order the triangles around x by walking shared edges
        nbr = {t: [] for t in ts}
        for t in ts:
            for e in ((tri[t][0], tri[t][1]), (tri[t][1], tri[t][2]), (tri[t][2], tri[t][0])):
                if x in e:
                    for t2 in edge_tris[frozenset(e)]:
                        if t2 != t and t2 in nbr:
                            nbr[t].append(t2)
        cyc = [ts[0]]
        prev = None
        while len(cyc) < len(ts):
            nxt = [u for u in nbr[cyc[-1]] if u != prev][0]
            prev = cyc[-1]
            cyc.append(nxt)
        faces.append(cyc)
    return faces


def leapfrog(faces):
    """Leapfrog of a cubic polyhedron (truncation of its dual): nodes = (face, edge) incidences; T multiplies by 3."""
    def edges_of(f):
        return [frozenset((f[i], f[(i + 1) % len(f)])) for i in range(len(f))]
    new_faces = []
    vertex_faces = {}
    for fi, f in enumerate(faces):
        es = edges_of(f)
        new_faces.append([(fi, e) for e in es])            # the face shrinks to a ring of its edge-nodes
        for v in f:
            vertex_faces.setdefault(v, []).append(fi)
    for v, fs in vertex_faces.items():                       # each old vertex (degree 3) becomes a hexagon
        assert len(fs) == 3
        shared = {}
        for f1, f2 in itertools.combinations(fs, 2):
            e = set(edges_of(faces[f1])) & set(edges_of(faces[f2]))
            e = [x for x in e if v in x]
            assert len(e) == 1
            shared[frozenset((f1, f2))] = e[0]
        f1, f2, f3 = fs
        e12, e23, e31 = shared[frozenset((f1, f2))], shared[frozenset((f2, f3))], shared[frozenset((f3, f1))]
        new_faces.append([(f1, e31), (f1, e12), (f2, e12), (f2, e23), (f3, e23), (f3, e31)])
    return new_faces


# --------------------------------------------------------------------------- #
def invariants(faces):
    verts = {v for f in faces for v in f}
    edges = {frozenset((f[i], f[(i + 1) % len(f)])) for f in faces for i in range(len(f))}
    sizes = sorted(len(f) for f in faces)
    deg = {}
    for e in edges:
        for v in e:
            deg[v] = deg.get(v, 0) + 1
    return len(verts), len(edges), len(faces), sizes, set(deg.values())


def dual_distances(faces):
    """Face adjacency (shared edge) and BFS distances between pentagons."""
    edge_faces = {}
    for fi, f in enumerate(faces):
        for i in range(len(f)):
            edge_faces.setdefault(frozenset((f[i], f[(i + 1) % len(f)])), []).append(fi)
    adj = {fi: set() for fi in range(len(faces))}
    for fs in edge_faces.values():
        a, b = fs
        adj[a].add(b)
        adj[b].add(a)
    pents = [fi for fi, f in enumerate(faces) if len(f) % 2 == 1]
    dist = {}
    for p in pents:
        d = {p: 0}
        q = deque([p])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if w not in d:
                    d[w] = d[u] + 1
                    q.append(w)
        dist[p] = d
    return pents, dist


def frustration(faces) -> tuple[int, list[int]]:
    """Minimum number of bonds breaking the sign alternation = minimum T-join of the odd faces in the dual
    (planar graphs, Hadlock 1975) = minimum-weight perfect matching of the pentagons by dual distance."""
    pents, dist = dual_distances(faces)
    n = len(pents)
    D = [[dist[pents[i]][pents[j]] for j in range(n)] for i in range(n)]
    best = {0: 0}
    full = (1 << n) - 1
    memo = {}

    def solve(mask):
        if mask == full:
            return 0
        if mask in memo:
            return memo[mask]
        i = next(b for b in range(n) if not mask >> b & 1)
        r = min(D[i][j] + solve(mask | 1 << i | 1 << j) for j in range(i + 1, n) if not mask >> j & 1)
        memo[mask] = r
        return r

    nearest = sorted(min(D[i][j] for j in range(n) if j != i) for i in range(n))
    return solve(0), nearest


def sec1():
    rule("sec 1  FULLERENES FROM THE EISENSTEIN DNA, TWO WAYS")
    print("""
  dual of the class-I geodesic sphere at frequency v (z = v, T = v^2), and leapfrog (z -> (1 - w) z, T -> 3T):
""")
    print(f"  {'construction':<34}{'z':>9}{'T':>4}{'atoms':>7}{'bonds':>7}{'faces':>7}{'pentagons':>11}{'hexagons':>10}{'deg':>5}")
    out = {}
    c20 = dual_of_triangulation(geodesic(1))
    cands = [("C20  dodecahedron = dual geodesic v=1", "1", 1, c20),
             ("C60  leapfrog(C20)", "1-w", 3, leapfrog(c20)),
             ("C80  dual geodesic v=2", "2", 4, dual_of_triangulation(geodesic(2))),
             ("C180 leapfrog(leapfrog(C20))", "(1-w)^2", 9, leapfrog(leapfrog(c20))),
             ("C180 dual geodesic v=3", "3", 9, dual_of_triangulation(geodesic(3))),
             ("C240 leapfrog(C80)", "2(1-w)", 12, leapfrog(dual_of_triangulation(geodesic(2)))),
             ("C320 dual geodesic v=4", "4", 16, dual_of_triangulation(geodesic(4)))]
    for name, z, T, faces in cands:
        V, E, F, sizes, degs = invariants(faces)
        assert V == 20 * T and E == 30 * T and V - E + F == 2 and degs == {3}
        assert sizes.count(5) == 12 and set(sizes) <= {5, 6}
        out[name] = faces
        print(f"  {name:<34}{z:>9}{T:>4}{V:>7}{E:>7}{F:>7}{sizes.count(5):>11}{sizes.count(6):>10}{'3':>5}")
    print("""
  Every one is a fullerene: 20T atoms, 30T bonds, all atoms 3-bonded, exactly 12 pentagons (the pentamons of
  Geometry_Of_Space.md) and 10(T-1) hexagons, V - E + F = 2.""")
    return out


def sec2(out):
    rule("sec 2  THE SIGN ALTERNATION ON A CAGE")
    print("""
On the flat sheet every bond joins a + site to a - site (the two sublattices are the two twist signs). A pentagon
is an odd ring, so on a cage some bonds must join equal signs. The fewest such bonds, exactly:
""")
    print(f"  {'fullerene':<34}{'T':>4}{'frustrated bonds':>18}{'fraction':>10}{'pentagon gaps (dual distance)':>32}")
    res = {}
    for name, faces in out.items():
        V, E, *_ = invariants(faces)
        F, nearest = frustration(faces)
        T = V // 20
        res[name] = (F, nearest)
        print(f"  {name:<34}{T:>4}{F:>18}{F / E:>10.3f}{str(sorted(set(nearest))):>32}")
    a, b = res["C180 leapfrog(leapfrog(C20))"], res["C180 dual geodesic v=3"]
    assert a == b
    print(f"""
  The DNA check: leapfrog twice and the v = 3 subdivision give the same C180 (same counts, same frustration
  {a[0]}, same pentagon gaps), as z (1-w)^2 = -3w z requires: the composition of DNAs is multiplication of their
  Eisenstein integers, up to a unit.

  The frustrated bonds are 6 x (the gap between pentagon pairs): the 12 pentagons pair off, each pair joined by a
  shortest string of broken bonds. For z = h + k w the gap is h + k, the number of triangular-lattice steps in z:
  1 (C20), 2 (C60 = (1,1), C80 = (2,0)), 3 (C180), 4 (C240 = (2,2), C320 = (4,0)). So the frustration is exactly
  6(h + k), while the bonds number 30(h^2 + hk + k^2): the broken fraction falls as 1/sqrt(T), and in the flat
  limit the sheet alternates everywhere.""")
    return res


def sec3():
    rule("sec 3  WHAT THIS GIVES, AND WHAT IT DOES NOT")
    print("""
Given: the fullerenes are the Eisenstein DNA of graphene folded onto the icosahedron -- the same index z as the
moire cells, composing by multiplication -- with the 12 pentamons of the geodesic blanket as their pentagons.
The sign alternation that makes graphene's sublattices fails on exactly 6 strings of broken bonds, one per pair
of pentagons; C60 is the smallest cage whose pentagons are isolated (no two adjacent).

Not claimed: anything about T_c. The fullerides superconduct by electrons doped into C60's three-fold degenerate
LUMO, with phonon and Jahn-Teller coupling and strong correlation near a Mott state (Ganin et al. 2008); none of
that is in this count. The one structural difference the substrate does see is the broken alternation: C60 is
the only superconducting carbon in Carbon_Superconductivity.md sec 4 whose lattice cannot carry the two signs
everywhere, and it has the highest T_c. That is recorded as a lead, as in sec 4; five materials are not a count.
The natural next check would be a family: the fullerides' T_c against their frustration fraction (C60 versus the
doped higher fullerenes), which would need data on doped C70/C76/C84 superconductivity.""")


if __name__ == "__main__":
    out = sec1()
    sec2(out)
    sec3()
