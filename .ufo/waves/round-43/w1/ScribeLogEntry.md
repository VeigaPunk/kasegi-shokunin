# ScribeLogEntry — round 43 `## Round 43` LOG entry

Seat: `ScribeLogEntry`, leaf scribe, kasegi round 43, one v2 wave `kasegi-r43-hyaku`. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`, lane HEAD at
work time `4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (the freeze commit). No subagent, no swarm, no second judge.

## Deliverable

- `.ufo/waves/round-43/w1/ScribeLogEntry.log-entry.md` — byte-exact append block for `LOG.md`.
- `wc -l` = **153**, `sha256sum` =
  `f9216e6e43357ca12cb4f142ef1670b4b43dd7783f362616942357becf7e0bb1`, 12207 bytes.
- Shape follows `LOG.md`'s newest entry (`## Round 42 (attempt 1, fresh-start)`, `LOG.md:1754-1806`): heading,
  frozen claims, one bullet per work item with a path/command pointer, repairs, mistakes, assimilation,
  considerthese, wave shape, trend verdicts, tooling, next-round plan. It ends with one empty line, matching the
  blank line that closes every earlier entry (`tail -2 LOG.md` → Tooling line + `$`).
- Append position: `LOG.md` already ends with that blank line (1806 lines total), so the block is appended
  directly after it; no separator is added by the appender.

## Required elements, and where each sits

| Required | In the deliverable |
|---|---|
| lane, base | bullet 1 (`ab98fac9…`, freeze commit `4cb6d4ae…`) |
| claims with verdicts | bullet 1 (C1 depth:verifiability 4 held; C2 coverage 8 held, capability acquisition) |
| one bullet per work item | C1 instrument; K1-K13 carried; K14; K15; K16; K17; K18; K19; negative controls/receipt; C2 gate; exemplar; nine fixtures + selftest; registry/capture/counters; knowledge + capability row; repairs; mistakes; assimilation; considerthese — each with its path |
| wave shape, counted from `w1-dispatch.json` | `- Wave shape:` (73 seats; role mix passed through from the registry members; `counts.spawn` 73) |
| attack share | `- Wave shape:` 23/73 = 31.5% (reviewer 11 + critic 7 + mutation-tester 5) |
| dead seats from the results file | `- Wave shape:` `<pending: L1 reads kasegi-r43-hyaku-results.json>` (L1 instruction: never invent the number) |
| sources/frontier | `- C2 . registry, capture and counters:` and `- Trend — expansion:` |
| trend verdicts | `- Trend — expansion / quality / discernment:` |
| tooling | `- Tooling: no pacman transactions …; package/install moves: none this round.` |
| next-round plan | `- Planned for round 44 (not a claim):` (two owned axes) |

## Evidence — commands and their real output

### 1. Claims digest, freeze record, control receipts, lane HEAD

```
$ sha256sum .ufo/waves/round-43/claims.json
a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630  .ufo/waves/round-43/claims.json
$ cat .ufo/waves/round-43/freeze.txt
frozen-at=2026-10-28T16:37:07Z
measured-at-max=2026-10-28T16:34:15Z
claims-sha256=a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630
base=ab98fac9dce87130bc4f66de89e30650d63943dc
$ grep -n 'measured-at=' .ufo/waves/round-43/c1-controls/do-nothing.txt .ufo/waves/round-43/c2-controls/before.txt
…/c1-controls/do-nothing.txt:2:measured-at=2026-10-28T16:32:23Z
…/c2-controls/before.txt:2:measured-at=2026-10-28T16:34:15Z
$ grep -n '^--- C\.\|closed=12/13' .ufo/waves/round-43/c1-controls/do-nothing.txt
25:closed=12/13 exit=1
26:--- C. the six routed r42 defects present at base (the r42 suite cannot see them)
$ git -C <lane> rev-parse HEAD
4cb6d4ae768481e1a14afbedc2d865a060ebacfd
```

The digest `claims-sha256` equals the live `sha256sum` of `claims.json`; `frozen-at` (16:37:07Z) is later than
both `measured-at` lines (16:32:23Z, 16:34:15Z) — the K19 ordering the entry states. The only `closed=` token the
entry quotes (`closed=12/13`) is line 25 of the committed c1 control.

### 2. Wave counts and role mix (counted, never estimated)

```
$ python3 -c "…json.load('.ufo/waves/round-43/w1-dispatch.json')…"
members=73 spawn=73
roles=connector:2,critic:7,executor:23,mutation-tester:5,revenger:2,reviewer:11,scout:9,scribe:10,sentinel:2,simplifier:2
attack=23/73=31.5%
```

The attack share uses the definition the round-42 verifier spot-check records as the reported one
(`reviewer+critic+mutation-tester`, `corpus/lessons/round-42-verifier-spotcheck.md` §7 "Non-defects"), which also
matches the milestone's `23/73`.

### 3. S067 capture facts used by the exemplar bullet

```
$ python3 -c "…ExecSourceCapture.manifest.json…"
{'id': 'S067', 'url': 'https://curl.se/docs/CVE-2023-38545.html', 'fetched_utc': '2026-10-28T16:39:59Z',
 'bytes': 13940, 'snapshot_bytes': 6446, 'lines': 131,
 'sha256': '327bc909e01ee3dc78272c06d3d568b78e92e5b4c35c7e527394422d763b238b',
 'raw_sha256': 'e9038f569b4dfe6b9fc0e2b8e984bba908f093254de4f928c636d98ae3372a30'}
```

Matches `.ufo/waves/round-43/w1/ExecSourceCapture.provenance.txt` (HTTP 200, 0 redirects, UA
`kasegi-shokunin/1.0`, fetch 16:39:58Z–16:39:59Z).

### 4. Registry rows (landed in the wave)

```
$ python3 -c "…ExecRegistryRows.rows.txt…"
S067 A mined corpus/knowledge/claim-package-gate.md
S068 A rejected —
```

11 columns per row; S067 `mined` with `used-by corpus/knowledge/claim-package-gate.md`, S068 `rejected` with a
reason + flip cell. This is the landed deliverable the entry's `66 → 68` bullet points at.

### 5. K19 limb — observed payload lines quoted by the entry

```
$ grep -n '^K19 payload' .ufo/waves/round-43/w1/ExecK19Freeze.transcript.txt | head -3
32:K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
36:K19 payload=freeze=present,order=ok,sha=match closed=1
49:K19 payload=freeze=present,order=bad,sha=match closed=0
```

The entry quotes only the base red and the freeze-commit green, both read from this transcript.

### 6. K16 self-check on my own block (the check that grades `## ` sections)

The landed K16 limb was sourced and run over a scratch export of lane HEAD, with and without my block appended
to `LOG.md`:

```
$ . .ufo/waves/round-43/w1/ExecK16Placeholder.sh
$ check_k16 $S/live        # export of 4cb6d4a, unmodified LOG.md
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
$ check_k16 $S/live-block  # same export, my block appended to LOG.md
payload=sections=492,promises=1,fenced=0,unresolved=1 closed=0
```

`sections` rises by exactly 1 (my `## Round 43` heading); `promises` and `unresolved` do not move.
So the block adds no placeholder promise and is not a K16 red of its own; K16 stays open at base only on
`corpus/lessons/round-42.md`'s `## Wave-2 falsification`, which the corrections block names. The K16 detector's
five clauses (`when the <subject> reports`, `to be filled`, `TBD`, `pending the <subject> wave`, `… is a
placeholder|stub`) do not match the three `<pending: L1>` tokens this entry carries.

### 7. K14 self-check on my own block (the check that grades correction-count literals)

The landed K14 limb was sourced and run over the same two scratch exports:

```
$ . .ufo/waves/round-43/w1/ExecK14Corrections.sh
$ check_k14 $S/live
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
$ check_k14 $S/live-block
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
```

Payload identical with and without the block: it contributes no correction-count literal, so it cannot add a
stale literal and cannot mask the one the corrections block supersedes. (The limb's own transcript shows the
after-correction states `literals=3 … superseded=2 … closed=1` at lines 63 and 74.)

### 8. K15 self-check on my own block (the check that grades the wave sentence)

Three scratch states: lane export without the block; the same export with the block appended; the same export with
the block **and** a scratch `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` holding `seats: 73` and 73 result
records (the dispatcher's own shape, `inline-dispatcher.py:290`).

```
$ . .ufo/waves/round-43/w1/ExecK15WaveNarrative.sh
$ check_k15 $S/live                    # no block
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:11 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 wave=wave2 round=42 stated-seats=36 unbacked=no-evidence
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
$ check_k15 $S/live-block              # block, no results file (repeats the three lines above, plus:)
K15 detail=LOG.md:1934 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 payload=sentences=6,unbacked=4,superseded=0,mismatch=0 closed=0
$ check_k15 $S/live-block-res          # block + results file (seats=73, 73 results)
K15 payload=sentences=6,unbacked=3,superseded=0,mismatch=0 closed=0
```

(States B and C are quoted as the delta against state A: B adds the round-43 detail line and one to `unbacked`;
C removes it again, leaving exactly A's three detail lines and A's `unbacked=3`.)

The limb parses the block's wave sentence as `wave=kasegi-r43-hyaku round=43 stated-seats=73`; it is unbacked
only while the results file is absent and becomes backed (drops out of the detail list, `unbacked` returns to the
round-42 count, `mismatch=0`) as soon as the results file carries `seats` 73 equal to its 73 result records.

### 9. K18 self-check on my own block (quoted `closed=` / `cases=` values)

```
$ . .ufo/waves/round-43/w1/ExecK18Transcript.sh
$ check_k18 $S/live
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
$ check_k18 $S/live-block
K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
```

Identical with and without the block: it contributes no unbacked quote (the one `closed=` token it carries is the
committed control's `closed=12/13`, and the quote census does not move). The limb's `unbacked=3` at base are the
round-42 RD42-5 quotes the `de09313` transcript is landed to back — not this block.

### 10. Token audit of the deliverable

```
$ grep -cE 'corrections=[0-9]+|groups=[0-9]+' ScribeLogEntry.log-entry.md
0
$ grep -oE 'closed=[0-9]+/[0-9]+' ScribeLogEntry.log-entry.md
closed=12/13
$ grep -oE 'selftest cases=[0-9]+' ScribeLogEntry.log-entry.md
(none)
$ grep -n 'dispatched\|round total' ScribeLogEntry.log-entry.md
35:  that asserts a named `kasegi-r<NN>-<word>` wave was dispatched, requires its
127:- Wave shape: one v2 wave `kasegi-r43-hyaku`, 73 seats dispatched — executor 23, reviewer 11, scribe 10,
```

- No correction-count literal, so the block cannot add a K14 stale literal.
- One `closed=` token, backed by the committed c1 control (above); the pending tokens are non-numeric.
- Line 35 describes K15's own predicate and carries no wave name that matches `kasegi-r<NN>-<word>` (the placeholders
  `<NN>`/`<word>` are not a wave id); line 127 is the one asserted wave and it names
  `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` and `seats` 73 in the same bullet.
- No `round total` anywhere in the block.

## Landing checklist for the L1 (must run before appending)

1. Replace the three tokens `<pending: L1>` — one dead-seat token and the two in the C1 bullet
   (`closed=<pending: L1>`, `selftest cases=<pending: L1>`) — from the one final-gates run. Until then the block is
   deliberately silent on the numbers, per KasegiR43's instruction; do not leave a token in the landed file.
2. The wave sentence is backed only when `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` exists with
   `seats: 73` and 73 result records (the K15 limb requires `seats == len(results)`; the inline dispatcher writes
   `<dispatch-dir>/<wave>-results.json` with exactly that shape, `scripts/hyaku/inline-dispatcher.py:290`).
3. Every `w1/…` path the block cites must exist at landing (each is a seat deliverable): `ExecCarryChecks.transcript.txt`,
   `ExecCarryChecks.declared-blocks.txt`, `ExecK14Corrections.transcript.txt`, `ExecK15WaveNarrative.transcript.txt`,
   `ExecK16Placeholder.transcript.txt`, `ExecK17ClaimsBefore.transcript.txt`, `ExecTranscriptDe0931.md`,
   `ExecK19Freeze.transcript.txt`, `ExecK19Freeze.freeze-format.txt`, `ExecNegCtlReceipt.md`,
   `ExecGateManifest.transcript.txt`, `ExecGateSelftest.transcript.txt`, `ExecGateFixtures.index.txt`,
   `ExecRegistryRows.rows.txt`, `ExecSourceCapture.provenance.txt`, `ScoutAssimilation.md`, `ScoutSiblingOverlap.md`.
   Present when the block was finalized (`ls` check): `ExecK14Corrections.*`, `ExecK15WaveNarrative.*`,
   `ExecK16Placeholder.*`, `ExecK17ClaimsBefore.*`, `ExecK18Transcript.sh`, `ExecK19Freeze.*`,
   `ExecGateManifest.transcript.txt`, `ExecGateProvReport.rules.py`, `ExecGateChain.*`, `ExecGateSelftest.*`,
   `ExecGateFixtures.index.txt`, `ExecRegistryRows.rows.txt`, `ExecSourceCapture.*`, `ExecTranscriptDe0931.*`,
   `ScoutSiblingOverlap.md`, `ScoutAssimilation.md`, `ScribeCorrections.*`. Still in flight: `ExecCarryChecks.*`
   and `ExecNegCtlReceipt.md` — confirm those two at landing.
4. If the final-gates run does not reach the frozen after-state, the C1/C2 bullets (and only those) must be
   regenerated from the receipt before appending; the block must not carry a `closed=`/`cases=` value the
   committed transcript does not print (K18).

## Not run, and why

- No run of `corpus/instruments/r43-closure.sh` — it is not committed at draft time and had not landed as a wave
  deliverable either (`ls .ufo/waves/round-43/w1 | grep ExecSuiteSkeleton` → no match), while at HEAD the path is
  absent (`ls` in the c1 control: `No such file or directory`). The entry therefore attributes no measured value
  to the composite and hands its two summary cells to the L1; the per-limb runs above are the evidence.
- No counts read from `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` — the wave settles only after all
  seats return, so no seat output existed at draft time (dir listing showed only `swarm-registry.json` and the
  landed deliverables).
- K17 does not read `LOG.md` at all — it grades claims.json `before`/`after` cells against the control receipts,
  and running it over the tree with the block appended leaves its result unchanged
  (`K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0`), so no block-side
  check applies. K14, K15, K16 and K18 are verified above.

## Scope and boundaries

- Wrote only this receipt, the deliverable beside it, and scratch under
  `/fast/scratch/hyaku/kasegi-r43/ScribeLogEntry/` (removed before yield). No lane file, fleet-root file, sibling
  lane, or `~/.local/bin` touched; the scratch export copies were made with `git -C <lane> archive` (read-only) and
  all edits in scratch.
- No mutating git/jj command anywhere; the one `git archive` and the `git log`/`rev-parse` reads are read-only.
- Declined an out-of-scope registry fix for a souji `SOURCES.md` line (peer `W1ScribeLessonGate`) — not this
  lane, not this seat's file.
- Tooling: no pacman transactions (host-wide pause); no package/install move; no network fetch from this seat
  (the S067 fetch belongs to `ExecSourceCapture` and its provenance was read, not repeated).
