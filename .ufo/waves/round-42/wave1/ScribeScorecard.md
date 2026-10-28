# Seat ScribeScorecard — round 42 receipt

- Seat: `ScribeScorecard` (role: scribe; leaf, no subagent dispatch)
- Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `5053a7f46de35784cff4b56756906e9014a38276`)
- Deliverable: `.ufo/waves/round-42/wave1/ScribeScorecard.round42.txt`
  - lines: **29** (`wc -l`)
  - sha256: **`2c14ad57696ae607e0c4dad44f08e9e055f61cd8d1c4f0e44a89d4d01bb4e25f`**
  - content: landable SCORECARD.md text only (leading blank separator line, two `Correction (round 42)` lines, the required `Correction-dedup (round 42)` marker, `## Round 42 result` with the axis table + before/at-Y lines + capabilities/saturation/planned clauses, and `### Round-42 move-log rows`). No validation notes inside the file.

## Behavior

1. Read the frozen claims (`.ufo/waves/round-42/claims.json`) and extracted the full C1/C2 predicates and kill rules for the exact after-state wording (13 checks J1-J13; seven families F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP; C2 target counters 25 / 64 / 61 / 28-28 / 56-56 / 45-45).
2. Located the D-r41-1 duplicated `Correction (round 41)` blocks and verified the duplication is byte-identical in the **committed** blob, not only the working tree.
3. Drafted the round-42 SCORECARD section against the pool of values the seat can actually observe (hashes, control-file counters, duplicated-block coordinates, defect IDs) and used `<pending>` for **every** round-42 measured value (instrument landing, Y, `closed=13/13`, `selftest cases=13`, base/r41-head reds, ref-not-found red, F25 topic, S064, registry/knowledge/harness/binding/audit/census/measure, F25 screened reject).
4. Carried the r41 honest standings forward explicitly: depth:verifiability `4 (held; not verified)`, coverage `8 (held; not verified)`, no retroactive upgrade, F24 parked.
5. Previewed the append (copy of SCORECARD.md + deliverable) to confirm heading/table structure and that the cited duplicate coordinates remain 1602-1605 / 1607-1610 under append-at-EOF.

## Commands and observed output

```
$ grep -n "Correction (round 41)\|## Round 41 result\|## Round 42\|Planned for round 42\|Correction-dedup" SCORECARD.md
1602..1605, 1607..1610  Correction (round 41): ... (4 lines each occurrence)
1612:## Round 41 result
1628:**Planned for round 42** (not a claim): ...
(grep for "## Round 42" and "Correction-dedup" -> 0 hits; both are introduced by this draft)
$ wc -l SCORECARD.md
1628 SCORECARD.md
```

```
$ awk 'NR>=1592 && NR<=1628 ...' SCORECARD.md   # numbered view
1602 Correction (round 41): round-40 C1 is not verified ...
1603 Correction (round 41): the `## Round 40 result` depth:verifiability row's ...
1604 Correction (round 41): the row's `graded --selftest cases=10 failures=0` ...
1605 Correction (round 41): the round-41 receipt at its Y tees ...
1606 (blank)
1607 (repeat of 1602)
1608 (repeat of 1603)
1609 (repeat of 1604)
1610 (repeat of 1605)
```

```
$ diff <(sed -n '1602,1605p' SCORECARD.md) <(sed -n '1607,1610p' SCORECARD.md) && echo IDENTICAL
IDENTICAL
```

Committed-blob cross-check (the working tree is unmodified, so the coordinates are not a tree-only artifact):

```
$ git hash-object SCORECARD.md ; git rev-parse HEAD:SCORECARD.md
b5fa7b5cf52f640a010bf3d904ef5c7d604fdeff
b5fa7b5cf52f640a010bf3d904ef5c7d604fdeff
$ git show HEAD:SCORECARD.md | sed -n '1602,1610p'   # same 4+4 lines, 1606 blank
$ git status --porcelain SCORECARD.md                 # empty
```

```
$ cat .ufo/waves/round-42/c2-controls/before.txt
frontier rows: 24 / F25 rows: 0 / registry rows: 63 / S064+ rows: 0 / knowledge files: 60 /
entries citing S064+: 0 / harness: entries=27 pass=27 exit=0 /
binding: records=55 bound=55 unbound=0 / audit: expect=present expected=60 missing=0 unexpected=0 exit=0
```

```
$ cat .ufo/waves/round-42/c1-controls/do-nothing.txt
r42 suite absent at base: `bash corpus/instruments/r42-closure.sh` -> exit 127, cannot print closed=13/13
r41 suite at base: `--export-ref 5053a7f4...` -> `selftest cases=12 failures=8`, `closed=8/12 exit=1`
```

```
$ ls corpus/instruments/ | grep -i r42 ; ls corpus/source-snapshots/ | tail -5
(no r42 instrument at read time)
round-37 round-38 round-39 round-40 round-41        # no round-42 snapshot dir yet
```

```
$ awk '{gsub(/\\\|/,""); n=gsub(/\|/,"|"); if (n>0) printf "%d pipes=%d\n", NR, n}' ScribeScorecard.round42.txt
9..13 pipes=6   (result table: 5 columns, escaped `closed=0\|1` inside a cell)
25..28 pipes=6  (move-log table: 5 columns)
```

Append preview (SCORECARD.md copy + deliverable, scratch only):

```
1628|**Planned for round 42** (not a claim): ...
1629|(blank)
1630|Correction (round 42): the round-41 standings carry forward unchanged ...
1634|Correction-dedup (round 42): duplicated Correction (round 41) blocks at SCORECARD.md lines 1602-1605 and 1607-1610 — the second occurrence is the stray; both kept as history.
1636|## Round 42 result
1637|table header
1651|### Round-42 move-log rows
```

Final deliverable stats:

```
$ wc -l .ufo/waves/round-42/wave1/ScribeScorecard.round42.txt
29
$ sha256sum .ufo/waves/round-42/wave1/ScribeScorecard.round42.txt
2c14ad57696ae607e0c4dad44f08e9e055f61cd8d1c4f0e44a89d4d01bb4e25f
```

## Gates (seat-scoped)

| Gate | Result |
|---|---|
| claims.json read, not edited | pass (only `json.load` reads) |
| Dedup marker template matched verbatim, coordinates filled from measurement | pass — line 6 of the deliverable: `...lines 1602-1605 and 1607-1610 — the second occurrence is the stray; both kept as history.` |
| D-r41-1 named exactly once as a correction + once as the dedup marker | pass (`Correction (round 42): D-r41-1 ...` and the marker; no other occurrence in lane files written by this seat) |
| r41 standings honest and unchanged | pass — `4 (held; not verified)` and `8 (held; not verified)` quoted from `## Round 41 result`, no upgrade |
| No invented measured values | pass — every round-42 value carries `<pending>`; all hard numbers trace to claims.json, the two control files, or SCORECARD lines 1616/1622 |
| Deliverable holds only landable bytes | pass — no validation table/notes inside the `.txt` |
| Tables well-formed | pass — 6 pipes per row for both 5-column tables |
| Writes confined to allowed paths | pass — two files under `.ufo/waves/round-42/wave1/` + scratch; no edit to SCORECARD.md, LOG.md, SHONEN.md, corpus, fleet root or other lanes |
| No mutating git/jj | pass (read-only: `git show`, `git hash-object`, `git rev-parse`, `git status`, `git log`) |
| Disk guard green before work | pass — `/tmp` 5%, `/var/tmp` 36%, `/fast/scratch/hyaku` 27% free-use 592.6G |

## Touched surfaces

Written (2 files, both untracked seat outputs):
- `.ufo/waves/round-42/wave1/ScribeScorecard.round42.txt`
- `.ufo/waves/round-42/wave1/ScribeScorecard.md` (this receipt)

Read-only: `.ufo/waves/round-42/{claims.json,c1-controls/do-nothing.txt,c2-controls/before.txt,wave1-spec.json}`, `SCORECARD.md`, `corpus/lessons/round-41-verifier-spotcheck.md`, `corpus/instruments/` and `corpus/source-snapshots/` listings.

Scratch: `/fast/scratch/hyaku/kasegi-r42/ScribeScorecard/` (preview copy only) — removed at end of seat; verified absent.

## Findings / limits

1. **D-r41-1 confirmed as committed history:** lines 1602-1605 and 1607-1610 are byte-identical (diff exit 0) in both the working tree and `HEAD:SCORECARD.md` (blob `b5fa7b5c...`); line 1606 is the only separator. No rewrite was made, per the r41 verifier's append-only instruction.
2. **Dedup coordinates are append-stable only if landing is append-at-EOF.** If the L1 inserts anything before line 1602 (e.g. a reordered correction block), the cited ranges must be recomputed before landing; the draft does not pin a blob hash for SCORECARD.md, so landing edits do not invalidate the text, only the numbers.
3. **All round-42 after-state values are `<pending>` by design:** at this seat's read, `corpus/instruments/r42-closure.sh` and `corpus/source-snapshots/round-42/` do not exist, so no Y measurement, no `closed=13/13`, no `selftest cases=13`, no F25 topic/S064 identity could be observed. The draft names the claims' target values only as targets with pending tags; it does not assert them.
4. **Adjacency QC:** the deliverable begins with one blank line so that a verbatim append leaves a separator after the existing `**Planned for round 42**` paragraph (previewed at line 1629); the seat did not modify `SCORECARD.md`.
5. **No network fetches, no tool installs** (`uv`/`npx`/binaries unused); no pacman run (host pause respected).
6. **Out of scope, deliberately untouched:** the r42 suite itself, C1/C2 counters, `SKILL.md` registry rows, lesson Gate block, `LOG.md`/`SHONEN.md` additions except the correction text drafted here for SCORECARD, and any J/Y hash claims. The move-log rows' After cells remain `**<pending> measurement**`, matching the round-36 precedent for draft-time rows.
7. **F24 / RFC 9116** is mentioned only as parked (per claims); it is not treated as a candidate or re-mined.
