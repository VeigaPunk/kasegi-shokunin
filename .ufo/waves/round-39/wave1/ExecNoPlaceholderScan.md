# ExecNoPlaceholderScan — round 39, wave 1 (leaf executor)

Judged axis: `depth:verifiability`. Item: scan every wave1 deliverable for
placeholder / leftover vocabulary, and check that every deliverable has a
nonempty receipt sibling.

## 1. Deliverable

| field | value |
|---|---|
| path | `.ufo/waves/round-39/wave1/ExecNoPlaceholderScan.placeholder-scan.txt` |
| lines | 330 |
| bytes | 29261 |
| sha256 | `0c99cad2749410e706ecd617ab7be10709452e9049fcf60e0140ecfe907cdfcf` |

Verdict lines as filed in the deliverable:

```
verdict_placeholders: PASS
verdict_receipt_siblings: PASS
verdict_instrument_agreement: PASS
verdict: PASS
```

The filed report is the second run: the first run (20:08:13Z) caught
`ScribeWaveEvidence.index.md` with a not-yet-written receipt and returned
`verdict_receipt_siblings: FAIL`; that seat filed `ScribeWaveEvidence.md` (6506
bytes) minutes later, so the report was regenerated at 20:09:08Z, where 49/49
receipts are present and the gap count is 0 (§5). The item's acceptance condition —
zero hits for the named vocabulary among wave-authored deliverables — is met in
both runs: **0 placeholder-class hits** (§4).

## 2. Method (two independent instruments)

Scope rule (roster-driven, not suffix-guessed): seat names come from
`.ufo/waves/round-39/wave1/swarm-registry.json` (49 members). In the wave dir an
entry is a **receipt** iff its basename is exactly `<SEAT>.md`; every other entry
is a **deliverable** and must have a nonempty `<SEAT>.md` sibling. This matters:
scribes deliver `*.row.md`, `*.append.md`, `*.entry.md`, and fixture seats deliver
directories, so an "everything ending in .md is a receipt" rule would have skipped
~50 real deliverables.

- **Instrument 1** — Python (`scan.py`, scratch): per-line match enumeration,
  classifies every hit, distinguishes `MISSING` / `EMPTY` receipts per file.
- **Instrument 2** — `grep -RnEI` over the deliverable list only (`xcheck.sh`,
  scratch). Reports matched *lines*; instrument 1 counts *matches*. The two are
  compared as `file:line` sets.
- Receipts are scanned in an informational appendix only: a receipt must quote the
  vocabulary it audits, so counting receipt hits would be a self-inflicted
  failure. Hits on receipts are reported anyway (§4.4).
- Self-exclusion: the report quotes the tokens it finds, so
  `ExecNoPlaceholderScan.placeholder-scan.txt` is excluded from its own scan (the
  exclusion is printed in the deliverable header as `self_excluded:`). Without it
  a rerun reports its own report and the instrument is non-idempotent.
- Verdict-bearing patterns, exactly as named in the seat spec: `⟨pending`,
  `<fill>`, `filled by the L1` (case-insensitive), `<LANE_HASH>`, `<r39-`,
  word-bounded `TBD`, word-bounded `TODO`, and any bracketed `[INFERENCE]`-style
  dodge (case-insensitive).

## 3. Instrument validation before use (fixture, scratch only)

Tripwire fixture with one deliverable per pattern class, a clean deliverable, a
directory deliverable, a `*.row.md` deliverable, a missing receipt and an empty
receipt — every class fired, nothing spurious:

```
scanned_at_utc 2026-10-26T19:31:33Z
roster=14 receipts=13 deliverables=14 primary_hits=8 advisory_hits=1
Clean.deliver.txt 26 bytes receipt=Clean.md 8 bytes ok
EmptyReceipt.d.txt 2 bytes receipt=EmptyReceipt.md 0 bytes EMPTY
NoReceipt.d.txt 7 bytes receipt=NoReceipt.md 0 bytes MISSING
P1.d.txt:1 angle-pending '⟨pending'
P2.d.txt:1 fill-tag '<fill>'
P3.d.txt:1 filled-by-l1 'filled by the L1'
P4.d.txt:1 lane-hash-tag '<LANE_HASH>'
P5.d.txt:1 r39-placeholder '<r39-'
P6.d.txt:1 word-TODO 'TODO'
P7.d.txt:1 word-TBD 'TBD'
P8.d.txt:1 inference-dodge '[INFERENCE]'
verdict primary_hits=8 receipt_gaps=2 -> FAIL
```

Negative control (clean tree plus a receipt that quotes the vocabulary) returned
`primary_hits=0 ... PASS` with the quoted receipt visible in the appendix only.
The `grep` instrument returned the same 8 hits on the tripwire and 0 on the
control, and its `file:line` set agreed with instrument 1 on the real wave (§4.3).

## 4. Result at scan time (2026-10-26T20:09:08Z)

```
wave_dir: .ufo/waves/round-39/wave1
roster_seats: 49
receipts: 49
deliverables_scanned: 185
files_scanned: 234
hits: 11
hits_by_class: placeholder=0 quotation=1 pinned-upstream=10
receipt_sibling_gaps: 0
cross_check: python_lines=7 grep_lines=7 agree=yes distinct_lines=7
```

### 4.1 Class A — wave-authored placeholders/leftovers: **0**

No deliverable in the wave contains a named token as a stand-in for unwritten
content. This includes the central C1 artifact: `ExecSuiteBuild.r39-closure.sh`
(75170 bytes) scans clean, as do the `ExecWholeTailFixture`, `ExecGradedSelftestFixture`
and `ExecG4ResultsFixture` fixture trees.

### 4.2 Class B — quotation of the audited vocabulary: 1 line

```
ConnRoleGround.conn.md:7 angle-pending '⟨pending' class=quotation
    ctx: - `corpus/lessons/round-39.md` — ... C1's kill rule also reads it (`⟨pending` count must be 0 at filing). ...
```

The token is inside an inline-code span and states C1's kill rule; it is not a
placeholder. It is still a literal token in a wave-authored deliverable, so a
broad grep over the wave1 tree fires on it (§4.5, §7).

### 4.3 Instrument agreement

11 matches over 7 distinct lines (`;`-free count difference is two lines carrying
two tokens each: `r37-closure.sh:60` and `:698`). The independent grep instrument
sees the same 7 lines:

```
ConnRoleGround.conn.md:7
ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:1255
ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:60
ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:698
ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:1255
ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:60
ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:698
```

### 4.4 Class C — bytes inherited from the digest-pinned instrument: 10 matches / 6 lines

Both copies of `r37-closure.sh` under `ExecPinnedG8Fixture.fixtures/` carry
`filled by the L1`, `<LANE_HASH>`, `TBD`, `TODO` at lines 60, 698 and 1255. Those
bytes are **committed lane bytes, not round-39 authored text**, and G8 requires the
export copy to hash to the pinned digest, so they must not be reworded:

```
== pinned copy sha256 ==
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  .../fixtures/pinned/r37-closure.sh
== committed r37-closure.sh at 2387dcf6 sha256 ==
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  -
== committed at base 480b1a5 ==
0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d  -
== token lines in committed 2387dcf6 copy ==
60:#       0 `filled by the L1` lines and 0 `<LANE_HASH>` marker lines, a
698:      ph=$(grep -cE '<(hash|sha|digest|ref|payload|N|n|id)>|TODO|TBD' "$p"); ph=${ph:-0}
1255:  mk_gates "$d/$p" "$live" 'extra=# TODO fill the export-ref'
```

The hit lines are the instrument's own audit prose, its own grep pattern, and a
mutant generator's deliberate broken line — all pre-existing at the base commit.
`negative-mutated/corpus/instruments/r37-closure.sh` differs from the pinned copy
only in the fixture's own mutation:

```
2c2
< # r37-closure.sh — round-37 closure counter for claim C1 (depth:verifiability).
---
> # r37-closure.sh — round-37 closure counter for claim C2 (depth:verifiability).
```

Receipts that quote the vocabulary (informational, by design) at scan time:
`ExecCorrectionsR2.md:145,146` (the token list it audits), `RevCorrections.md:26`,
`ScribeReportInputs.md:11`, `ScribeShonen.md:159`, `ConnRoleGround.md:13`.

## 5. Receipt siblings

185 deliverables, every one paired with a nonempty `<SEAT>.md`: **0 gaps** at the
filed snapshot. The run that found the one straggler is preserved here because it
is the interesting case:

```
# first run, 20:08:13Z
ScribeWaveEvidence.index.md	54785 bytes	receipt=ScribeWaveEvidence.md	0 bytes	MISSING
```

`ScribeWaveEvidence.md` was absent at 20:08:13Z; it was present at 20:09:02Z
(6506 bytes) and the seat was still appending to it at 20:09:30Z (6912 bytes), so
the regenerated run at 20:09:08Z shows `receipt_sibling_gaps: 0` with 49/49
receipts. Everything else, including all `ScribeRowsRejected.*` rows, both
`ExecSuiteBuild` trees and the multi-directory fixture seats, was already paired in
the first run.
`ExecNoPlaceholderScan.md` (this receipt) is excluded from the gap count as
`receipt_sibling_self` because the report is generated first and the receipt
written from it.

Only one 0-byte file exists in the wave and it is deliberate:
`ExecG4ResultsFixture.fixtures/h-nodir/.keep` (the "no dispatch dir" fixture).

## 6. Advisory sweep (reported, never verdict-bearing)

41 advisory hits reviewed and each classified benign; sampled contexts:

| hit | context | verdict |
|---|---|---|
| `ExecContextGuardCheck.context-check.txt:14`, `ExecNoHarmFixture.guard-demo.txt:288` | `<SEATNAME>` | the spec's own scratch-path token |
| `ExecGradedSelftestFixture.fixtures/{expected.tsv,generate.py,mutants.txt}` | `<TAB>` | column-header notation in fixture format |
| `ExecAssimilationIds.quarantine-verdicts.md:138` | `<TITLE>` | quoted HTTP error body, evidence |
| `ScribeSpotCheckList.checklist.md:17` | `<REF>` | procedure template token |
| `ExecProofSuiteSelftest.proof.txt:33` | `placeholder hashes` | prose describing the reference run |
| `ExecArchiveChecks.base-gates.txt:337,338` | `"pending","tbd","todo"` | quoted `capture-binding-check.py` sentinel list |
| `ExecArchiveChecks.base-gates.txt:449` | `added-placeholders=1` | G3 mutant payload |
| `ExecPinnedG8Fixture.fixtures/*/r37-closure.sh:59,121,150,423,795,1009,1012,1254,1256` | `placeholder` | pinned instrument prose (same digest-pin argument as §4.4) |

`ExecArchiveChecks.base-gates.txt:424` (`added-pending=1,added-placeholders=0`) and
`ExecDiskGuardProbe.disk.txt:104` (`ExecNoPlaceholderScan` as a roster name) showed
up only before the advisory `placeholder` pattern was word-bounded to `\bplaceholder\b`;
my seat name was matching its own substring. Fixed in the instrument, not by
excusing the hit.

## 7. Coordination

`ConnRoleGround` was the only seat whose deliverable carries a literal token, so I
tried to hand them the exact line before the wave closed:

```
Failed: ConnRoleGround is not running. Unknown agent "ConnRoleGround"
```

The seat had already terminated, so the §4.2 hit stands for the L1: cheapest fix is
to reword `ConnRoleGround.conn.md:7` (and `ConnRoleGround.md:13`) as "the U+27E8
pending token count must be 0 at filing", keeping the meaning and removing the
literal. `ConnRoleGround.conn.md` is a cross-axis note, not landed lane text, so
this is a tree-hygiene item, not a landability blocker.

## 8. Coverage limits

- The scan is a snapshot of 2026-10-26T20:09:08Z with 49/49 receipts and 185
  deliverables present. Any wave1 file written after that timestamp is not covered;
  the wave was still moving at filing (`ScribeWaveEvidence.md` was being appended to
  at 20:09:30Z), so rerun §9 before using this as a final gate.
- The scan covers the wave dir only. It says nothing about the lane working tree,
  `corpus/lessons/round-39.md`, or any landed file — C1's own kill rule
  (`grep -c '⟨pending corpus/lessons/round-39.md` = 0) is a separate gate.
- Directories are walked, so fixture-tree payloads (`.tsv`, `.sh`, nested export
  trees) are in scope and are clean apart from the pinned-instrument class.

## 9. Rerun recipe (no scratch scripts needed)

```
cd .ufo/waves/round-39/wave1
PAT='⟨pending|<fill>|filled by the L1|<LANE_HASH>|<r39-|\bTBD\b|\bTODO\b|\[[^]]*[Ii][Nn][Ff][Ee][Rr][Ee][Nn][Cc][Ee][^]]*\]'
grep -RnEI -e "$PAT" . | grep -v '/swarm-registry.json:' | grep -v 'ExecNoPlaceholderScan'
```

At filing time this prints exactly 13 `file:line` entries, all accounted for:

```
./ConnRoleGround.conn.md:7                     <- §4.2 quotation
./ConnRoleGround.md:13                         <- receipt quoting the vocabulary
./ExecCorrectionsR2.md:145                     <- receipt quoting the token list
./ExecCorrectionsR2.md:146                     <- receipt quoting the token list
./ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:60
./ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:698
./ExecPinnedG8Fixture.fixtures/pinned/r37-closure.sh:1255
./ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:60
./ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:698
./ExecPinnedG8Fixture.fixtures/negative-mutated/corpus/instruments/r37-closure.sh:1255
./ScribeReportInputs.md:11                     <- receipt quoting the vocabulary
./RevCorrections.md:26                         <- receipt quoting the token list
./ScribeShonen.md:159                          <- receipt quoting its own grep check
```

i.e. 6 pinned-instrument lines (§4.4), 6 receipt lines that quote the vocabulary,
and the 1 §4.2 quotation. Drop the 7 pinned+quotation lines by excluding
`ExecPinnedG8Fixture` and `ConnRoleGround.conn.md` and the tree is clean. The
deliverable class is exactly the 7 lines of §4.3.

## 10. Files changed, tooling, scratch

- Written: `.ufo/waves/round-39/wave1/ExecNoPlaceholderScan.placeholder-scan.txt`
  (the deliverable, §1) and this receipt. No other file in the lane, the fleet
  root, or any source tree was created, modified or deleted.
- Read-only git only: `git -C <lane> show 2387dcf6:corpus/instruments/r37-closure.sh`
  and the same path at base `480b1a5...`, for the §4.4 digest comparison. No
  mutating git/jj command was run.
- Tooling: no installs, no upgrades (pacman untouched). Instrumentation is
  Python 3 stdlib plus GNU `grep`/`coreutils` already on the host.
- Scratch `/fast/scratch/hyaku/kasegi-r39/ExecNoPlaceholderScan/` removed after
  the deliverable and this receipt were copied out.
- Risks for integration: (a) the §4.2 quotation will fire a broad wave1 grep until
  reworded; (b) the receipt-sibling gap seen in the first run resolved itself when
  `ScribeWaveEvidence.md` landed, so the filed report has 0 gaps — but that seat was
  still writing at 20:09:30Z, so re-check its pairing after it yields; (c) the scan
  is point-in-time (§8) — rerun after the last seat lands.

No blockers.
