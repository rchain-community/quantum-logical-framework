# Group Decisions Demo: A Team Decides, Issues, and Records — over a P2P Room

A worked, multi-peer walkthrough of collaborative **governance** in the live
[quantum-os](https://github.com/rhovision-org/quantum-os) browser app: a team picks a
venue by **ranked-choice vote**, records the outcome as a **decision of record**,
issues a **terms-bearing IOU** that the recipient must **accept** before
redeeming, and **retracts** a mistaken entry. Every step is the *same* ZFA
operation as the logic in [`AI.md`](AI.md) — dyncap-signed envelopes plus a
deterministic, joiner-local tally.

This is the companion demo to the syllogism walkthrough in [`AI.md`](AI.md)
(*Live Collaboration Script*). For the full map of decision processes the
interface supports — approval, ranked-choice, consensus, atomic rendezvous,
delegation, sortition, conviction voting — see
[`Group_Decisions.md`](https://github.com/rhovision-org/quantum-os/blob/main/Group_Decisions.md)
in quantum-os.

---

## Why this needs no server

quantum-os has no central authority to count votes, hold a tally, or declare a
winner. Each decision step is two ingredients:

- **Dyncap-signed envelopes** — every ballot, nomination, and note is a
  hash-chained message attributable to its sender; you cannot forge another
  peer's contribution.
- **A deterministic, joiner-local tally** — every peer recomputes the outcome
  from the contributions it holds. Same inputs → same result on every machine, so
  the group converges on one answer without trusting anyone to count.

Possessing the room capability token **is** the franchise. The cast: **Alice**
(organizer), **Bob**, **Carol**, **Dave**, **Eve** — five peers in the room
`https://rhovision-org.github.io/quantum-os/#room=cap:room:…`. Lines prefixed `·` are
system output; `[Name→]` marks what other peers receive via broadcast.

---

## Part 1 — Collect the options, then vote (ranked-choice)

### Step 1 — Alice opens a poll for nominations

Alice opens a **ranked-choice** poll with *no* fixed options — the group will
nominate venues, then rank them.

```
Alice> /poll new Where should we hold the team dinner? ranked
· 🗳 poll opened — "Where should we hold the team dinner?" [ranked-choice · open for ideas]
·   anyone: /poll add <option>   ·   then /poll vote a > b > c
```

A poll card appears for every peer, with an **add-an-option** box and a 🗳 marker
in the sidebar's *Polls* list.

### Step 2 — the group nominates (open nominations)

Anyone adds candidates — from the card or the command. Options are keyed by a
**content hash**, so identical suggestions auto-merge and ballots can't be
scrambled by broadcast ordering.

```
Bob>   /poll add Ramen House
Carol> /poll add Pizza Forno
Dave>  /poll add Taqueria Uno
Eve>   /poll add Ramen House          ·  (merges — already nominated)
```

Each `/poll add` broadcasts a `poll-option` envelope; the card lists three
options: **Ramen House**, **Pizza Forno**, **Taqueria Uno**.

### Step 3 — everyone ranks their preferences

Members vote by clicking the card in preference order, or by command (`>`
separates ranks). Re-voting replaces a prior ballot (latest wins).

```
Alice> /poll vote Ramen House > Taqueria Uno
Bob>   /poll vote Ramen House > Pizza Forno
Carol> /poll vote Pizza Forno > Ramen House
Dave>  /poll vote Pizza Forno > Taqueria Uno
Eve>   /poll vote Taqueria Uno > Ramen House
```

Each ballot is a dyncap-signed `poll-ballot` of option **ids** (not text), so
every peer tallies the same thing.

### Step 4 — Alice closes; instant-runoff resolves the split

```
Alice> /poll close
· 🗳 poll closed — "Where should we hold the team dinner?" · winner: Ramen House (5 votes)
·   round 1: Ramen House:2  Pizza Forno:2  Taqueria Uno:1  — out: Taqueria Uno
·   round 2: Ramen House:3  Pizza Forno:2  — majority
```

First preferences were a three-way split (2 / 2 / 1) that a plain plurality vote
would leave tied at the top. Instant-runoff eliminates the lowest (**Taqueria
Uno**), transfers Eve's ballot to her second choice (**Ramen House**), and
**Ramen House** clears a majority of continuing ballots (3 of 5). Elimination ties
break deterministically by smallest option id, so every peer agrees without
coordination. The result is logged as a **permanent transcript line** on every
peer — it survives card re-renders and scroll-back.

---

## Part 2 — Record the decision

A vote is ephemeral; a *decision of record* is durable. Alice mints the outcome as
a **multi-word lemma** — a natural-language name any peer can reference with
`@[…]`, that syncs to all peers and persists across reloads.

```
Alice> /lemma [team dinner is at Ramen House] ^v
· lemma registered: @[team dinner is at Ramen House]  =  ^v
·   ZFA: ✓   cap: cap:team-dinner-is-at-Ra…:…  (an unforgeable record of the decision)
Bob> /qucalc @[team dinner is at Ramen House]
·   achieves_ZFA: ✓   (the ratified decision, re-checkable by anyone)
```

The lemma is the room's shared, machine-checkable record of what was decided.

---

## Part 3 — Issue a terms-bearing IOU and accept it

Alice is fronting the reservation, so she issues each attendee a **seat note** that
carries its terms. Terms are bound to the note by a **stamp**: the issuer mints a
note whose token commits to a hash of the terms, and a relayer can't alter the
text without changing the note's identity.

### Step 5 — declare a currency and grant a terms-stamped seat

```
Alice> /note declare DINNER
· declared currency: DINNER   authority: cap:token-DINNER:…
Alice> /note grant DINNER 1 | Admits one to the Ramen House team dinner, 2026-06-20 19:00. Redeem with the organizer.
· minted: DINNER~fa3d4691 1  · 📜 terms fa3d4691
·   cap:note-DINNER~fa3d4691:…
·   terms: Admits one to the Ramen House team dinner, 2026-06-20 19:00. Redeem with the organizer.
Alice> /note pass DINNER~fa3d4691 1 Bob
· DINNER~fa3d4691 1 → Bob
```

"DINNER" with these terms is the series **`DINNER~fa3d4691`** — a different terms
text would be a different series (`DINNER~<other hash>`), even for the same
currency. The dyncap-signed `note-series` declaration publishes the terms text to
the room; the stamp `fa3d4691` is exactly `termsHash8(terms)`.

### Step 6 — Bob receives, and must accept before redeeming

```
[Alice→] · received DINNER~fa3d4691 1 from Alice  · 📜 terms fa3d4691
·   terms: Admits one to the Ramen House team dinner … (/note accept DINNER~fa3d4691 to agree)
Bob> /note redeem DINNER~fa3d4691 1 Alice
· ⚠ DINNER~fa3d4691 carries terms you have not accepted:
·   Admits one to the Ramen House team dinner, 2026-06-20 19:00. Redeem with the organizer.
·   review, then:  /note accept DINNER~fa3d4691   (then re-run redeem)
Bob> /note accept DINNER~fa3d4691
· ✓ accepted terms for DINNER~fa3d4691  (hash fa3d4691)
Bob> /note redeem DINNER~fa3d4691 1 Alice
· redeemed DINNER~fa3d4691 1 → Alice   ·   awaiting receipt…
```

Redemption is gated on acceptance — the moment value is claimed is the moment the
holder agrees to the terms. Alice (the issuer) honors it and returns a receipt:

```
[Bob→] · Bob redeems DINNER~fa3d4691 1
· honored: DINNER~fa3d4691 1 for Bob
·   receipt: cap:receipt-DINNER~fa3d4691:…
[Alice→] · DINNER~fa3d4691 1 redemption honored by Alice
```

`/note terms DINNER` lists the currency's series; `/note terms DINNER~fa3d4691`
prints the full text and whether you've accepted it.

---

## Part 4 — Correct the record (removal & retraction)

Earlier, Carol fat-fingered a duplicate decision lemma. Because gossiped state
otherwise heals back from the next peer's sync, removal uses **tombstones**: the
author broadcasts a dyncap-signed `retract` that everyone honors, and it can't
re-sync back.

```
Carol> /lemma [dinner venu is Ramen House] ^v      ·  (typo: "venu")
   …later…
Carol> /forget lemma [dinner venu is Ramen House]
· @[dinner venu is Ramen House] retracted
```

The typo'd lemma is dropped on every peer and tombstoned; the correct
`@[team dinner is at Ramen House]` stands. A non-author who tries to forget it
would only hide it from their own view. The same `/forget` (or the sidebar ✕)
removes a stray poll or a note.

---

## Part 5 — Durability without a server

When every browser leaves, the room's memory would normally vanish. The headless
**memory-peer daemon** ([`quantum-os/scripts/qos-cli`](https://github.com/rhovision-org/quantum-os/tree/main/scripts/qos-cli))
persists and re-serves the room's public state to future joiners: the decision
lemma, the `DINNER~fa3d4691` terms-series, and Carol's retraction tombstone all
survive a restart — and the daemon **honors the author's retraction**, so it never
resurrects the typo'd lemma.

---

## Summary

| Step | Who | Command | Feature | ZFA reading |
|---|---|---|---|---|
| 1 | Alice | `/poll new … ranked` | open-nomination poll | a room-level closure awaiting contributions |
| 2 | all | `/poll add …` | content-hash nominations | each option a balanced atom |
| 3 | all | `/poll vote a > b > c` | ranked ballots (signed) | per-peer closures |
| 4 | Alice | `/poll close` | instant-runoff tally | deterministic joiner-local synthesis |
| — | Alice | `/lemma [team dinner …]` | decision of record | the ratified result as an unforgeable token |
| 5 | Alice | `/note grant … \| terms` | terms-stamped series | obligation bound to a terms commitment |
| 6 | Bob | `/note accept` → `redeem` | acceptance-gated redemption | claiming value = agreeing to terms |
| 7 | Carol | `/forget lemma [...]` | owner retraction + tombstone | a closure the room un-ratifies |

Decision and derivation are one mechanism. A vote is a closure the room ratifies;
an IOU is a closure that carries its obligations; a retraction is a closure
withdrawn. The same dyncap-signed, joiner-local substrate carries all of them —
see [`Group_Decisions.md`](https://github.com/rhovision-org/quantum-os/blob/main/Group_Decisions.md)
for the broader family, and [`QuantumOS.md`](QuantumOS.md) for how this is the
same operation as scheduling, security, and error correction in the kernel.
