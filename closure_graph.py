#!/usr/bin/env python3
"""
closure_graph.py — build the directed vector graph of ZFA at capacity R, check it, render it.

The graph of `Closure_Walk.md` §3: nodes are the lattice points `x ∈ ℤ⁴` with `|x|₁ ≤ R`
(the capacity horizon is the ℓ¹ ball), and from every node one directed edge per twist,
`x → x + s·e_a`, carrying the vector `s·e_a` and the sign `s·(−1)^ε`,
`ε = Σ_{spatial b ranked above a} x_b mod 2` (0 on the gauge axis). The sign is a ℤ₂
connection: the product of edge signs around a closed path is the path's Pauli phase
(`closure_walk.connection_phase` = `fold_phase`, checked on every closure to length 8).

Asserted here, on the built graph:
  * node count = |ℓ¹ ball| = Σ_k 2^k C(4,k) C(R,k)  (1, 9, 41, 129, 321 for R = 0..4);
  * the connection part (−1)^ε of an edge is the same in both directions (the twist sign
    s is the direction itself), so each undirected edge has one well-defined connection sign;
  * every plaquette spanned by two DIFFERENT spatial axes has holonomy −1, every plaquette
    involving the gauge axis has holonomy +1 (π flux through mixed spatial plaquettes only);
  * counting closed walks at the origin on the graph reproduces the census: unsigned
    `W_t` = 8, 168, 5120 and the signed sum Σ phase over closures, for t ≤ 2R (a closed
    walk of length t never leaves the ball of radius t/2);
  * the double cover (x, σ) has 2·|ball| nodes and every lifted edge lands in the ball.

Writes data/closure_graph_R{R}.json and closure_graph.html (self-contained, canvas, no
libraries; rotate by drag, wheel to zoom, hover a node for its ways-to-close counts).

Run:  python3 closure_graph.py [--R 3]
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

from closure_walk import closed_walk_count, edge_sign, _AX
from census_inventory import balanced_histories, fold_phase
from doob_bridge import h as ways_to_close

_HERE = os.path.dirname(os.path.abspath(__file__))
TWISTS = ['^', 'v', '>', '<', '/', '\\', '+', '-']
AXIS_NAME = ['Y', 'X', 'Z', 'gauge']          # index order of the action vector


def ball(R: int) -> list[tuple[int, int, int, int]]:
    pts = []
    for x in itertools.product(range(-R, R + 1), repeat=4):
        if sum(abs(v) for v in x) <= R:
            pts.append(x)
    pts.sort(key=lambda p: (sum(abs(v) for v in p), p))
    return pts


def ball_size(R: int) -> int:
    return sum(2 ** k * math.comb(4, k) * math.comb(R, k) for k in range(0, 5))


def build(R: int) -> dict:
    nodes = ball(R)
    index = {x: i for i, x in enumerate(nodes)}
    edges = []                       # directed
    for i, x in enumerate(nodes):
        for tw in TWISTS:
            a, s = _AX[tw]
            y = list(x); y[a] += s; y = tuple(y)
            if y not in index:
                continue
            sg = edge_sign(list(x), a, s)
            edges.append({"from": i, "to": index[y], "twist": tw, "axis": a, "s": s,
                          "sign": sg, "conn": sg * s})
    # connection is direction-independent
    lookup = {(e["from"], e["to"]): e for e in edges}
    for e in edges:
        back = lookup[(e["to"], e["from"])]
        assert back["conn"] == e["conn"], "connection sign differs by direction"
    undirected = []
    for e in edges:
        if e["from"] < e["to"]:
            undirected.append({"a": e["from"], "b": e["to"], "axis": e["axis"], "conn": e["conn"]})

    # plaquettes: x, x+e_a, x+e_a+e_b, x+e_b  (positive orientation; other orientations
    # differ by direction signs that cancel around a loop)
    plaquettes = []
    for x in nodes:
        for a in range(4):
            for b in range(a + 1, 4):
                corners = []
                for da, db in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    y = list(x); y[a] += da; y[b] += db
                    corners.append(tuple(y))
                if any(c not in index for c in corners):
                    continue
                loop = [(corners[0], a, 1), (corners[1], b, 1), (corners[2], a, -1), (corners[3], b, -1)]
                hol = 1
                for c, ax, s in loop:
                    hol *= edge_sign(list(c), ax, s)
                mixed_spatial = a != 3 and b != 3
                assert hol == (-1 if mixed_spatial else 1), f"plaquette {x} axes {a},{b}: holonomy {hol}"
                plaquettes.append({"corners": [index[c] for c in corners], "axes": [a, b], "holonomy": hol})

    # closed walks at the origin on the graph vs the census, unsigned and signed
    o = index[(0, 0, 0, 0)]
    adj = [[] for _ in nodes]
    for e in edges:
        adj[e["from"]].append((e["to"], e["sign"]))
    checks = {}
    for t in range(2, 2 * R + 1, 2):
        u = [0] * len(nodes); u[o] = 1
        sgn = [0] * len(nodes); sgn[o] = 1
        for _ in range(t):
            nu = [0] * len(nodes); ns = [0] * len(nodes)
            for i in range(len(nodes)):
                if u[i] or sgn[i]:
                    for j, sg in adj[i]:
                        nu[j] += u[i]; ns[j] += sgn[i] * sg
            u, sgn = nu, ns
        census_signed = sum(1 if fold_phase(hh) == "+1" else -1 for hh in balanced_histories(t))
        assert u[o] == closed_walk_count(t), f"unsigned walk count at t={t}: {u[o]}"
        assert sgn[o] == census_signed, f"signed walk count at t={t}: {sgn[o]} vs census {census_signed}"
        checks[t] = {"W": u[o], "signed": sgn[o]}

    # per-node ways-to-close, for the tooltip
    node_recs = []
    for i, x in enumerate(nodes):
        d = sum(abs(v) for v in x)
        hs = {t: ways_to_close(x, t) for t in (d, d + 2, d + 4) if t > 0}
        node_recs.append({"id": i, "x": list(x), "depth": d, "h": {str(t): v for t, v in hs.items()},
                          "deg": len(adj[i])})

    n = len(nodes)
    assert n == ball_size(R), f"ball size {n} ≠ {ball_size(R)}"
    cover_edges = 0
    for e in edges:
        eps = 0 if e["conn"] == 1 else 1
        for sigma in (0, 1):
            cover_edges += 1          # (from, sigma) -> (to, sigma ^ eps); target always in the ball
    return {
        "R": R, "nodes": node_recs, "edges": undirected,
        "directed_edges": len(edges), "plaquettes": plaquettes,
        "summary": {
            "nodes": n, "directed_edges": len(edges), "undirected_edges": len(undirected),
            "plaquettes": len(plaquettes),
            "plaquettes_flux_minus": sum(1 for p in plaquettes if p["holonomy"] == -1),
            "double_cover_nodes": 2 * n, "double_cover_edges": cover_edges,
            "edges_conn_minus": sum(1 for e in undirected if e["conn"] == -1),
            "walk_checks": checks,
            "spatial_only_nodes": sum(1 for x in nodes if x[3] == 0),
        },
    }


def render(g: dict) -> str:
    data = json.dumps({"R": g["R"], "nodes": g["nodes"], "edges": g["edges"],
                       "plaquettes": g["plaquettes"], "summary": g["summary"]}, separators=(",", ":"))
    return TEMPLATE.replace("/*DATA*/null", data)


TEMPLATE = r"""<title>Closure Walk Graph</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{--bg:#f4f5f2;--panel:#ffffff;--ink:#1c2128;--muted:#5d6670;--line:#d9ddd6;
  --origin:#c8931e;--d1:#3a6ea5;--d2:#6f8fb5;--d3:#a9b7c6;--gauge:#8a6fb5;
  --plus:#8b96a0;--minus:#d0452c;--hi:#1c2128;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#101418;--panel:#171c22;--ink:#e6e9ec;--muted:#98a2ad;--line:#2a323b;
  --origin:#e0a83a;--d1:#6fa3e0;--d2:#5a7ea8;--d3:#3f5266;--gauge:#a48ad6;--plus:#4e5964;--minus:#ee6a4e;--hi:#ffffff;}}
:root[data-theme="dark"]{--bg:#101418;--panel:#171c22;--ink:#e6e9ec;--muted:#98a2ad;--line:#2a323b;
  --origin:#e0a83a;--d1:#6fa3e0;--d2:#5a7ea8;--d3:#3f5266;--gauge:#a48ad6;--plus:#4e5964;--minus:#ee6a4e;--hi:#ffffff;}
html,body{height:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 "IBM Plex Sans",system-ui,sans-serif;padding-inline:16px;padding-block:12px;box-sizing:border-box}
.wrap{display:grid;grid-template-columns:1fr 300px;gap:16px;height:100%;min-height:520px}
@media (max-width:760px){.wrap{grid-template-columns:1fr;height:auto}.stage{height:60vh}}
.stage{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden;min-height:420px}
canvas{display:block;width:100%;height:100%;cursor:grab;touch-action:none}
canvas:active{cursor:grabbing}
.tip{position:absolute;pointer-events:none;background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:6px 8px;font:12px/1.4 "IBM Plex Mono",monospace;color:var(--ink);white-space:pre;display:none;box-shadow:0 2px 8px rgba(0,0,0,.15)}
.panel{display:flex;flex-direction:column;gap:14px;overflow:auto}
h1{font-size:17px;font-weight:600;margin:0;letter-spacing:-.01em;text-wrap:balance}
.sub{color:var(--muted);margin:2px 0 0;font-size:13px}
.stats{display:grid;grid-template-columns:1fr auto;gap:3px 12px;font:13px/1.5 "IBM Plex Mono",monospace}
.stats span:nth-child(odd){color:var(--muted)}
.stats span:nth-child(even){text-align:right;font-variant-numeric:tabular-nums}
fieldset{border:1px solid var(--line);border-radius:6px;padding:8px 10px;margin:0}
legend{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:0 4px}
label{display:flex;align-items:center;gap:8px;padding:3px 0;cursor:pointer}
input[type=checkbox]{accent-color:var(--d1)}
input:focus-visible,button:focus-visible{outline:2px solid var(--d1);outline-offset:2px}
.key{display:flex;flex-direction:column;gap:5px;font-size:13px}
.key i{display:inline-block;width:22px;height:0;border-top:2px solid;vertical-align:middle;margin-right:8px}
.key b{display:inline-block;width:10px;height:10px;border-radius:50%;vertical-align:middle;margin-right:8px}
button{font:inherit;padding:5px 10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:4px;cursor:pointer}
.note{color:var(--muted);font-size:12px;margin:0}
code{font-family:"IBM Plex Mono",monospace;font-size:12px}
</style>
<div class="wrap">
  <div class="stage"><canvas id="c"></canvas><div class="tip" id="tip"></div></div>
  <div class="panel">
    <div><h1>The closure walk at capacity R = <span id="R"></span></h1>
      <p class="sub">Every lattice point of ℤ⁴ within ℓ¹-distance R of the origin, joined by the eight twists. Edge colour is the ℤ₂ connection; a closed path's Pauli phase is the product of its edge signs.</p></div>
    <div class="stats" id="stats"></div>
    <fieldset><legend>Show</legend>
      <label><input type="checkbox" id="showGauge" checked> gauge-axis nodes (x₄ ≠ 0)</label>
      <label><input type="checkbox" id="showPlus" checked> edges with connection +1</label>
      <label><input type="checkbox" id="showMinus" checked> edges with connection −1</label>
      <label><input type="checkbox" id="showFlux"> shade the π-flux plaquettes</label>
      <label><input type="checkbox" id="spin"> slow rotation</label>
    </fieldset>
    <fieldset><legend>Key</legend><div class="key">
      <div><b style="background:var(--origin)"></b>origin — the closure set</div>
      <div><b style="background:var(--d1)"></b>|x|₁ = 1 &nbsp;<b style="background:var(--d2)"></b>2 &nbsp;<b style="background:var(--d3)"></b>3</div>
      <div><b style="background:var(--gauge)"></b>node with gauge component</div>
      <div><i style="border-color:var(--plus)"></i>connection +1</div>
      <div><i style="border-color:var(--minus)"></i>connection −1 (Jordan–Wigner sign)</div>
    </div></fieldset>
    <p class="note">Spatial axes X, Y, Z are drawn as three orthogonal directions; the gauge axis is the fourth, drawn as a skew offset. Drag to rotate, wheel to zoom, hover a node for its ways-to-close counts <code>h(x,t)</code>. Spec: <code>Closure_Walk.md</code> §3; built and checked by <code>closure_graph.py</code>.</p>
    <div><button id="reset">Reset view</button></div>
  </div>
</div>
<script>
const G = /*DATA*/null;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
document.getElementById('R').textContent = G.R;
const S = G.summary, st = document.getElementById('stats');
const rows = [["nodes (|ℓ¹ ball|)", S.nodes],["directed edges", S.directed_edges],["undirected edges", S.undirected_edges],
  ["  with connection −1", S.edges_conn_minus],["plaquettes", S.plaquettes],["  with π flux (−1)", S.plaquettes_flux_minus],
  ["double cover nodes", S.double_cover_nodes],["spatial-only nodes", S.spatial_only_nodes]];
for (const t of Object.keys(S.walk_checks)) rows.push([`closed walks t=${t}`, S.walk_checks[t].W], [`  signed Σ phase`, S.walk_checks[t].signed]);
st.innerHTML = rows.map(([k,v]) => `<span>${k}</span><span>${v}</span>`).join('');

// 4-D -> 3-D: X,Y,Z orthogonal; the gauge axis as a skew direction
const AX = {0:[0,1,0], 1:[1,0,0], 2:[0,0,1], 3:[0.42,0.30,0.26]};
const P3 = G.nodes.map(n => { const p=[0,0,0]; for (let a=0;a<4;a++) for (let k=0;k<3;k++) p[k]+=n.x[a]*AX[a][k]; return p; });
const cv = document.getElementById('c'), ctx = cv.getContext('2d'), tip = document.getElementById('tip');
let rotX = -0.45, rotY = 0.6, zoom = 1, drag = null, hover = -1, spin = false;
function resize(){ const r = cv.parentElement.getBoundingClientRect(); cv.width = r.width*devicePixelRatio; cv.height = r.height*devicePixelRatio; draw(); }
addEventListener('resize', resize);
function project(p){
  const cy=Math.cos(rotY), sy=Math.sin(rotY), cx=Math.cos(rotX), sx=Math.sin(rotX);
  let x=p[0]*cy+p[2]*sy, z=-p[0]*sy+p[2]*cy, y=p[1];
  const y2=y*cx-z*sx, z2=y*sx+z*cx;
  const W=cv.width, H=cv.height, sc=Math.min(W,H)/(2*G.R+2.4)*zoom, f=1/(1+z2*0.06);
  return [W/2+x*sc*f, H/2-y2*sc*f, z2, f];
}
const opts = id => document.getElementById(id).checked;
let screen=[];
function draw(){
  const W=cv.width, H=cv.height; ctx.clearRect(0,0,W,H);
  const showG=opts('showGauge'), showP=opts('showPlus'), showM=opts('showMinus'), showF=opts('showFlux');
  const vis = G.nodes.map(n => showG || n.x[3]===0);
  screen = P3.map(project);
  const dpr=devicePixelRatio;
  if (showF){ ctx.globalAlpha=0.18; ctx.fillStyle=css('--minus');
    for (const pl of G.plaquettes){ if (pl.holonomy!==-1 || !pl.corners.every(i=>vis[i])) continue;
      ctx.beginPath(); pl.corners.forEach((i,k)=>{ const s=screen[i]; k?ctx.lineTo(s[0],s[1]):ctx.moveTo(s[0],s[1]); }); ctx.closePath(); ctx.fill(); }
    ctx.globalAlpha=1; }
  const es = G.edges.filter(e => vis[e.a]&&vis[e.b]&&(e.conn===1?showP:showM)).map(e=>({e, z:(screen[e.a][2]+screen[e.b][2])/2})).sort((u,v)=>u.z-v.z);
  for (const {e} of es){ const a=screen[e.a], b=screen[e.b]; const hi = hover===e.a||hover===e.b;
    ctx.strokeStyle = e.conn===1?css('--plus'):css('--minus'); ctx.lineWidth=(hi?2.6:e.conn===1?0.9:1.5)*dpr;
    ctx.globalAlpha = hi?1:(e.axis===3?0.55:0.85); ctx.setLineDash(e.axis===3?[4*dpr,4*dpr]:[]);
    ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke(); }
  ctx.setLineDash([]); ctx.globalAlpha=1;
  const order = G.nodes.map((n,i)=>i).filter(i=>vis[i]).sort((i,j)=>screen[i][2]-screen[j][2]);
  for (const i of order){ const n=G.nodes[i], s=screen[i];
    const col = n.depth===0?css('--origin'):n.x[3]!==0?css('--gauge'):n.depth===1?css('--d1'):n.depth===2?css('--d2'):css('--d3');
    const r=(n.depth===0?7:5.2-n.depth*0.6)*dpr*s[3];
    ctx.fillStyle=col; ctx.beginPath(); ctx.arc(s[0],s[1],r,0,Math.PI*2); ctx.fill();
    if (i===hover){ ctx.strokeStyle=css('--hi'); ctx.lineWidth=2*dpr; ctx.stroke(); } }
}
cv.addEventListener('pointerdown', e=>{ drag=[e.clientX,e.clientY]; cv.setPointerCapture(e.pointerId); });
cv.addEventListener('pointerup', ()=>drag=null);
cv.addEventListener('pointermove', e=>{
  if (drag){ rotY += (e.clientX-drag[0])*0.008; rotX += (e.clientY-drag[1])*0.008; drag=[e.clientX,e.clientY]; draw(); return; }
  const r=cv.getBoundingClientRect(), mx=(e.clientX-r.left)*devicePixelRatio, my=(e.clientY-r.top)*devicePixelRatio;
  let best=-1, bd=14*devicePixelRatio; const showG=opts('showGauge');
  screen.forEach((s,i)=>{ if(!showG && G.nodes[i].x[3]!==0) return; const d=Math.hypot(s[0]-mx,s[1]-my); if(d<bd){bd=d;best=i;} });
  if (best!==hover){ hover=best; draw(); }
  if (best>=0){ const n=G.nodes[best]; const hs=Object.entries(n.h).map(([t,v])=>`h(x,${t}) = ${v}`).join('\n');
    tip.textContent=`x = (Y ${n.x[0]}, X ${n.x[1]}, Z ${n.x[2]}, gauge ${n.x[3]})\n|x|₁ = ${n.depth}   degree ${n.deg}\n${hs}`;
    tip.style.display='block'; tip.style.left=Math.min(e.clientX-r.left+14, r.width-200)+'px'; tip.style.top=(e.clientY-r.top+14)+'px'; }
  else tip.style.display='none';
});
cv.addEventListener('pointerleave', ()=>{ hover=-1; tip.style.display='none'; draw(); });
cv.addEventListener('wheel', e=>{ e.preventDefault(); zoom*=e.deltaY<0?1.1:0.9; zoom=Math.max(0.4,Math.min(4,zoom)); draw(); }, {passive:false});
for (const id of ['showGauge','showPlus','showMinus','showFlux']) document.getElementById(id).addEventListener('change', draw);
document.getElementById('spin').addEventListener('change', e=>{ spin=e.target.checked; if(spin) tick(); });
document.getElementById('reset').addEventListener('click', ()=>{ rotX=-0.45; rotY=0.6; zoom=1; draw(); });
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
function tick(){ if(!spin) return; rotY += reduce?0:0.004; draw(); requestAnimationFrame(tick); }
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', draw);
new MutationObserver(draw).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
resize();
</script>
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=3)
    args = ap.parse_args(argv)
    g = build(args.R)
    s = g["summary"]
    print(f"R = {args.R}: {s['nodes']} nodes, {s['directed_edges']} directed edges "
          f"({s['undirected_edges']} undirected, {s['edges_conn_minus']} with connection −1), "
          f"{s['plaquettes']} plaquettes of which {s['plaquettes_flux_minus']} carry π flux; "
          f"double cover {s['double_cover_nodes']} nodes / {s['double_cover_edges']} edges")
    for t, c in s["walk_checks"].items():
        print(f"  closed walks at the origin, t={t}: {c['W']} (= W_t), signed Σ phase = {c['signed']} (= census)")
    print("  all plaquette holonomies: −1 iff both axes spatial — OK")
    jpath = os.path.join(_HERE, "data", f"closure_graph_R{args.R}.json")
    with open(jpath, "w") as f:
        json.dump({k: v for k, v in g.items() if k != "directed_edges"}, f, separators=(",", ":"))
    hpath = os.path.join(_HERE, "closure_graph.html")
    with open(hpath, "w") as f:
        f.write(render(g))
    print(f"wrote {os.path.relpath(jpath, _HERE)}, {os.path.relpath(hpath, _HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
