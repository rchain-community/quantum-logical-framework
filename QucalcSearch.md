# QuCalc Search — the "what closes next" query

[`qucalc_search.py`](qucalc_search.py) answers one question over the QLF substrate:

> From this QuCalc position, what are the admissible **next closures**?

Given a twist history `qc`, it enumerates the **continuations** — twist words you can
append so the whole history is a ZFA closure (count-balanced ∧ Pauli-closed) — shortest
first. `qucalc_search.py` is the **Python reference implementation + CLI**; it also has an
optional local HTTP mode (`--serve`) for research use. [quantum-os](https://github.com/rchain-community/quantum-os)
computes the same `/search` and `/solve` **client-side in the browser** from its own ZFA
primitives — no deployed service ([quantum-os#119](https://github.com/rchain-community/quantum-os/issues/119)) —
using the contract and cascade below as the spec.

It is a **query, not a stored layer.** Nothing is cached, nothing is written, the answer
is always current with [`twist_core.py`](twist_core.py). Contrast
[`census_inventory.py`](census_inventory.py) (per-stratum summaries, committed, a Lean-invariant
regression checker) and [`contextual_census.py`](contextual_census.py) (the Born-question
experiment layer). This one is the interactive middle: the actual histories reachable from
one point.

## What search and solve are

**Search is the experiment.** All admissible histories exist *a priori* as pure possibility
(QLF possibilism); `/search` *asks the substrate which of them close* from a position and
lays the whole possibility space out. That is the generative act —
`contextual_census.py` is "the experiment layer" for the same reason, and this is its
interactive form. A concurrent search (`qc=a,b,c`) with shared `listeners` is several
positions co-read through one set of rollups; at the substrate that is all the method allows
— *an apparatus is a closure inventory; an observer is only a perspective on it, contributing
a capacity and nothing else* ([`ScientificApproach.md`](ScientificApproach.md) §2). The
`capacity:R` listener is that perspective made concrete: one census heard by horizons of
different reach.

**Solve is the truth divination.** Truth in QLF is what *closes* — a completed process, a
closure receipt, not a standing proposition ([`Philosophy.md`](Philosophy.md) §9); the future
is *un-rendered possibility* ([`Reversibility.md`](Reversibility.md) §8). Of the ways a
position can close, the substrate takes **one** — the least free action, the shallowest-horizon
closure, the one a widening horizon reaches **first** (`QLF_ClosureDepthLaw`). That one is the
*truth of the position*, and `/solve` names it. It is **not** the depth reached the most ways:
[`QLF_ClosureMultiplicity`](lean/QLF_ClosureMultiplicity.lean) counts the strata and finds the
second outnumbering the first for every history length `2n ≥ 6` (`depth_one_not_modal`), with the
modal depth growing like `√n` (issue #171). "First" and "most ways" are different orderings, and
`/solve` uses the first — because what is reached first can never be contradicted: once a history
closes at a horizon it stays closed at every wider one (`closedAtHorizon_mono`,
[`QLF_HorizonClosure`](lean/QLF_HorizonClosure.lean)), so no deeper closure can undo it. Because the cascade is
deterministic, it is a reading, not an opinion — every caller divines the same answer.

**In [quantum-os](https://github.com/rchain-community/quantum-os), solve is the meeting of
minds.** Run `/solve` on a room's **joint position** — every peer's `/qlf-action` proposal
concatenated in order — and the deterministic cascade returns the one closure. Every peer
computes it identically, so the room reaches a shared conclusion **the substrate dictated,
not one negotiated**: consensus by closure, joiner-local like the `/poll` tally
([`QLF_as_Intelligence.md`](QLF_as_Intelligence.md) §8, the room as one distributed synthesis,
peers as Markov-blanket sub-agents). `mode=events` makes the search side of this literal —
a closure *is* an event, so the absorbing run reports the first way each branch resolves.

*(Framing, grounded in the possibilist ontology — the possibility structure is already there;
search reads it, solve names the one the substrate takes. Neither creates it.)*

## Why no precompute / no on-disk index

A depth-6 continuation search is ~260k raw candidates, count-prefiltered to a few thousand
before any Pauli fold runs — a few seconds on a small box, sub-second elsewhere. That is
cheaper than reading a ~1 MB cache entry back over a slow mount, and it never goes stale.
Run `python3 qucalc_search.py --time` for the numbers on the current host. If repeat-query
load is ever measured, the cache to add is one SQLite keyed by the state summary
`(imbalance vector, axis parity, depth)` — not a new census layer.

## How the search stays cheap

The seed's signed action vector `(v,h,d,l)` fixes what every continuation must supply:
exactly `−(v,h,d,l)`. So

1. **feasibility** — a length-`k` continuation can hit `need` only if `k ≥ Σ|need_i|` and
   `k ≡ Σ|need_i| (mod 2)`; infeasible depths are skipped whole;
2. **count prefilter** — each candidate tuple's own action vector is checked against `need`
   *before* any string is built;
3. **Pauli fold** — runs only on the ~2–5% that already count-balance, and by
   `QLF_TwistAlphabet.count_balanced_pauli_closed` those are *all* Pauli-closed, so the fold
   here only reads off **which** scalar (the phase), never gates admission.

## Possibilities vs events

The default stream is the **possibilities** — *every* closure within `max_depth`, including
continuations whose own prefix already closed. Pass `mode=events` (`--events` on the CLI) for
the **events**: a closure *is* an event, so a branch is not extended past its first closure.
The event continuations are prefix-free — each the *first* way that branch closes — which is
the absorbing census of [`contextual_census.py`](contextual_census.py) `--first-closure` and
the `closures` layer of [`census_inventory.py`](census_inventory.py). From `^<v>+-` at
depth 6: 5296 possibilities, 3056 events.

## Listeners — one enumeration, several rollups

`listeners=<spec>` runs the search once and reports aggregates alongside (or instead of) the
stream. `count` is always on.

| listener | reports |
|---|---|
| `phase` | closures per Pauli scalar `{+1,-1,+i,-i}` |
| `depth` | closures per appended-twist count |
| `capacity:R` | the QLF **listening** — `heard` / `missed` split by whether `max_excursion ≤ R` (`QLF_ClosureDepthLaw`) |
| `head:N` | the first `N` continuation words verbatim |

`stream=0` suppresses the per-closure lines and returns only the `_done` rollup — the right
call when the consumer wants the ~10 K aggregate, not every string. `qc` may be
comma-separated for a **concurrent search** over several seeds; listeners aggregate across
all of them and `per_seed` carries the per-seed counts.

```
GET /search?qc=^<v>+-&max_depth=6&stream=0&listeners=phase,depth,capacity:2,capacity:3
GET /search?qc=^<v>+-,+-+-&max_depth=6&mode=events&listeners=capacity:2,head:20
```

## CLI

```
python3 qucalc_search.py "^<v>+-" --max-depth 6                 # closures, plain words
python3 qucalc_search.py "^<v>+-" --max-depth 6 --json          # NDJSON records
python3 qucalc_search.py "^<v>+-" --max-depth 6 --count-only    # just the count
python3 qucalc_search.py "^<v>+-" --max-depth 6 --events \
        --listeners phase,depth,capacity:2                      # events + rollups
python3 qucalc_search.py "^<v>+-,^^<" --max-depth 4 --listeners phase   # concurrent seeds
python3 qucalc_search.py --time                                 # benchmark this host
```

## HTTP endpoint (local / research use)

```
python3 qucalc_search.py --serve --port 8765
python3 qucalc_search.py --serve --host 0.0.0.0 --port 8765 --max-depth-cap 7 --max-concurrent 2
```

**Not a deployed dependency.** `qucalc_search.py` is the **Python reference implementation +
CLI**; `--serve` is here for local research use. quantum-os does **not** call it over HTTP —
its `/search` and `/solve` compute [client-side in the
browser](https://github.com/rchain-community/quantum-os/issues/119), reusing the ZFA
primitives it already has (`signedAction`, `isPauliClosed`, `pauliFold`) and the deterministic
`/solve` cascade below. The contract in this section is the **spec that TS port conforms
to** — same routes, same `version`, same cascade — not a service anyone has to keep alive.

### Contract (the spec — `version` field; the TS port pins it)

| route | response |
|---|---|
| `GET /` | `{service, version, usage, alphabet, caps}` |
| `GET /health` | `{ok: true}` |
| `GET /search?qc=<hist[,hist…]>&max_depth=<int>&limit=<int>&mode=<possibilities\|events>&listeners=<spec>&stream=<0\|1>` | `200 application/x-ndjson`, streamed |
| `GET /solve?qc=<hist[,hist…]>&max_depth=<int>` | `200 application/json`, one answer |
| | `400 {error}` — bad `qc` / non-integer params / unknown listener |
| | `429 {error}` — host at `--max-concurrent`, retry |

The `/search` stream, one JSON object per line, flushed as produced:

```
{"_meta": true, "qc": ["..."], "max_depth": D, "limit": L, "stream": true,
 "mode": "possibilities", "version": "1.0"}                                  ← params after clamping
{"cont": "vv>", "history": "^^<vv>", "len": 6, "depth": 3, "phase": "-1"}    ← one closure (omitted if stream=0)
 …                                                                            shortest depth first
{"_done": true, "seeds": [...], "mode": "...", "found": K, "elapsed_s": F,
 "truncated": <hit limit?>, "per_seed": {...}|null, "listeners": {...}}
```

`depth` = appended twists; `phase` = the Pauli scalar the whole history folds to
(`{"+1","-1","+i","-i"}`, per [`QLF_PhaseRule`](lean/QLF_PhaseRule.lean); a balanced history
is always real `±1`, per `QLF_BalancedPhaseReal`).

### `/solve` — the one closure the substrate takes

The complement of `/search`: where `/search` renders *every* way to close, `/solve` picks
*the* one — least free action — or reports the residual. A comma-separated `qc` is
**concatenated** into one position (unlike `/search`, where seeds are separate). One JSON
answer, not a stream — the point is to return a decision, not a set.

```
{"solved": true, "qc": "^^<", "cont": "v>v", "history": "^^<v>v",
 "depth": 3, "phase": "+1", "peak_excursion": 3, "arrangements": 20,
 "considered": 149, "searched_depth": 5, "version": "1.0"}
{"solved": true, "qc": "^<v>+-", "already_closed": true, "history": "^<v>+-", …}
{"solved": false, "qc": "^^^^^^^^", "residual": [-8,0,0,0], "floor_depth": 8,
 "searched_depth": 6, "reason": "beyond max_depth", "completion": "vvvvvvvv", "version": "1.0"}
```

The selection cascade — deterministic, so independent callers agree without coordinating:

> **least peak excursion → shortest depth → phase `+1` → lexicographic history**

Least peak excursion *is* least free action: the shallowest-horizon closure is the one a
capacity-`R` horizon closes first (`QLF_ClosureDepthLaw`), and that ordering is what the
cascade applies to name a representative — the **truth of the position**. It is not the
"most ways" ordering: across the balanced census the modal depth is `2` for lengths `6 … 14`
and grows like `√n`, so depth 1 is never the most numerous stratum past length 4
([`QLF_ClosureMultiplicity`](lean/QLF_ClosureMultiplicity.lean), `depth_one_not_modal`). The
cascade is unchanged; only its justification is corrected
(see *What search and solve are* above). Determinism is the point: it makes `/solve` a
reading every caller shares, which is what turns it into a consensus mechanism in a room.
`mode=events` is implied. Depth strategy: the natural closure depths are `floor` and
`floor+2` (parity, `floor = Σ|residual|`) — search there first, widen to `max_depth` only if
that misses. `considered` is the event set that was ranked (capped at 5000; the winner is
always shallow, so the cap does not bite in practice).

CORS `Access-Control-Allow-Origin: *` on every response; `OPTIONS` preflight answered. The
service is **read-only and stateless**. `max_depth` is clamped to the deployment's
`--max-depth-cap`; `limit` to 100 000.

### Running `--serve` on a constrained host

Each concurrent `/search` holds only its generator (a few MB — `itertools.product` is lazy,
only the streamed line is materialised), so memory is dominated by `--max-concurrent`, not
result size. On a small box set `--max-depth-cap 6` (≈ 3 s worst case) and
`--max-concurrent 2`. Depth 7 is ~2 M candidates (tens of seconds on a slow CPU); depth 8
is disallowed by the hard cap.

## Client examples (for a local `--serve` instance)

These consume the NDJSON stream from a local `python3 qucalc_search.py --serve`. The
in-browser quantum-os implementation ([quantum-os#119](https://github.com/rchain-community/quantum-os/issues/119))
does not use HTTP — it runs the same enumeration natively — but these show the contract's
shape and are the reference for the TS port's behaviour (`_meta` line, closures
shortest-first, `_done` trailer).

### TypeScript / browser peer (`fetch` + streaming NDJSON)

Works in the browser and in Node ≥ 18. `QUCALC_SEARCH_URL` is the deployed endpoint.

```ts
const QUCALC_SEARCH_URL = "http://qucalc.internal:8765";

export interface Closure {
  cont: string;      // twist word appended to qc
  history: string;   // the full closed history
  len: number;
  depth: number;     // appended twists
  phase: "+1" | "-1" | "+i" | "-i";
}

/** Stream the admissible next closures from a QuCalc position. */
export async function* qucalcSearch(
  qc: string,
  opts: { maxDepth?: number; limit?: number; signal?: AbortSignal } = {},
): AsyncGenerator<Closure, { found: number; elapsedS: number; truncated: boolean }> {
  const u = new URL("/search", QUCALC_SEARCH_URL);
  u.searchParams.set("qc", qc);
  if (opts.maxDepth != null) u.searchParams.set("max_depth", String(opts.maxDepth));
  if (opts.limit != null) u.searchParams.set("limit", String(opts.limit));

  const res = await fetch(u, { signal: opts.signal });
  if (!res.ok) throw new Error(`qucalc_search ${res.status}: ${(await res.json()).error}`);

  const reader = res.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buf = "";
  let done = { found: 0, elapsedS: 0, truncated: false };
  for (;;) {
    const { value, done: end } = await reader.read();
    if (end) break;
    buf += value;
    let nl: number;
    while ((nl = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, nl).trim();
      buf = buf.slice(nl + 1);
      if (!line) continue;
      const obj = JSON.parse(line);
      if (obj._meta) continue;                      // params echo, after clamping
      if (obj._done) { done = { found: obj.found, elapsedS: obj.elapsed_s, truncated: obj.truncated }; continue; }
      yield obj as Closure;
    }
  }
  return done;
}

// usage: offer the next closures at a room's current QuCalc state
const ctrl = new AbortController();
const byPhase: Record<string, string[]> = {};
for await (const c of qucalcSearch("^<v>+-", { maxDepth: 6, limit: 10_000, signal: ctrl.signal })) {
  (byPhase[c.phase] ??= []).push(c.cont);
  if (Object.values(byPhase).flat().length >= 200) ctrl.abort();   // stop early, server sees the hangup
}
```

### Rust peer / `zfa-core` (`ureq`, blocking, no async runtime needed)

```rust
// Cargo.toml:  ureq = { version = "2", features = ["json"] }  |  serde = { version = "1", features = ["derive"] }  |  serde_json = "1"
use std::io::{BufRead, BufReader};

#[derive(serde::Deserialize, Debug)]
pub struct Closure {
    pub cont: String,
    pub history: String,
    pub len: u32,
    pub depth: u32,
    pub phase: String, // "+1" | "-1" | "+i" | "-i"
}

/// Stream admissible next closures; `on_closure` is called per result as it arrives.
pub fn qucalc_search(
    base: &str, qc: &str, max_depth: u32, limit: u32,
    mut on_closure: impl FnMut(Closure),
) -> Result<(usize, f64), Box<dyn std::error::Error>> {
    let resp = ureq::get(&format!("{base}/search"))
        .query("qc", qc)
        .query("max_depth", &max_depth.to_string())
        .query("limit", &limit.to_string())
        .call()?;

    let (mut found, mut elapsed) = (0usize, 0.0);
    for line in BufReader::new(resp.into_reader()).lines() {
        let line = line?;
        if line.trim().is_empty() { continue; }
        let v: serde_json::Value = serde_json::from_str(&line)?;
        if v.get("_meta").is_some() { continue; }
        if v.get("_done").is_some() {
            found = v["found"].as_u64().unwrap_or(0) as usize;
            elapsed = v["elapsed_s"].as_f64().unwrap_or(0.0);
            continue;
        }
        on_closure(serde_json::from_value(v)?);
    }
    Ok((found, elapsed))
}

// usage
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (found, secs) = qucalc_search("http://qucalc.internal:8765", "^<v>+-", 6, 10_000, |c| {
        println!("{:>8}  ->  {}  [{}]", c.cont, c.history, c.phase);
    })?;
    eprintln!("{found} closures in {secs:.3}s");
    Ok(())
}
```

### Notes for consumers

- **Abort to stop early.** Dropping the reader / aborting the fetch closes the socket; the
  server catches the hangup and stops enumerating. Don't rely on `limit` alone if you only
  want the first few — a small `limit` is still the cheaper signal.
- **`_meta` is the accepted-params echo.** If it shows a smaller `max_depth` than you asked,
  the deployment's `--max-depth-cap` clamped it.
- **`429`** means the host is at `--max-concurrent`; back off and retry, or run against a
  second instance.
- **Phase is always `±1` for a balanced history** (`QLF_BalancedPhaseReal`); `±i` only
  appears if you pass an already-unbalanced `qc` whose continuation cannot rebalance the
  gauge axis — which the search would not return as a closure anyway, so in practice
  consumers see only `+1` / `-1`.
