# ScribeWaveEvidence — wave-1 evidence pointer index (round 39)

**Item.** Build the wave-evidence index (deliverable `.ufo/waves/round-39/wave1/ScribeWaveEvidence.index.md`): for every
waveform file present in `.ufo/waves/round-39/wave1/` (receipts + deliverables) list basename, bytes, line count,
sha256, and which claim/item it serves. Deliverable only. Leaf seat; no subagent dispatch. Axes: coverage (C2),
inside the depth:verifiability (C1) record chain it indexes.

**Result.** `ScribeWaveEvidence.index.md` written: **256 lines, 55327 bytes,
sha256 `da6a7e8bc65dc51f7afdd7b45f65d84b34fa7d4de935f820c2c118c0d5ac0776`**. It indexes **235 files**
(100 top-level artifacts + 135 pack members in 5 packs — the four `<Seat>.fixtures` packs plus
`ExecSuiteBuild.overlay`) totalling 1539601 bytes; **49/49** declared wave-1 seats present; **0 unclassified**
paths. The snapshot instant is stamped in the file itself: `2026-10-26T20:09:18Z` (UTC).

## Method (reproducible)

Scratch generator `gen_index.py` (scratch only, deleted after use; described here so the index can be regenerated):
`os.walk` the wave-1 dir; per file record `os.path.getsize`, `wc -l`-semantics newline count
(`bytes.count(b"\n")`, `+` suffix when the last byte is not `\n`), and `hashlib.sha256` over the bytes; attribute each
path to a seat by the longest seat name that is the path's first component or a first-component prefix
(`<Seat>.…` / `<Seat>.fixtures/…`); join to the seat's claim plus a one-line item label; sort by seat then path. The
seat set, claims and labels are the 49 wave-1 items of `.ufo/waves/round-39/wave1-spec.json` crossed with the frozen
`claims.json` (C1 = depth:verifiability, C2 = coverage).

Claim assignment rule (recorded so every row is auditable): an artifact takes the frozen claim whose predicate its
item feeds — C1 for the instrument, fixtures, gate transcripts, corrections, records and guard probes; C2 for the
S057 capture, registry rows, knowledge entry, frontier amendments, harness probes and row/amendment reviews; `C1+C2`
for items whose spec axes name both owned axes (measurements, scorers, cross-lane sweeps, report inputs). Explicit
`C1+C2`: ExecConsiderthese, ExecScoreGap, ScribeReportInputs, ScribeWaveEvidence, ScoutSiblingF22, ScoutReopenS057,
ConnRoleGround. All other `Scribe*` and the capture/frontier/row-review seats are C2; all other `Exec*`, `Rev*` and
`Crit*` are C1. `swarm-registry.json` is pre-wave dispatch bookkeeping, claim `--`.

## Evidence (commands run, actual output)

Wave-1 directory filling in while the wave ran (monitor sampling every 20 s):

```
$ ls -1 .ufo/waves/round-39/wave1/ | wc -l
1                    # 19:31Z: only swarm-registry.json
19:46:03 STABLE at 93   # top-level entries unchanged for 160 s
```

Three index generations, kept to show the wave filling in and that nothing was padded:

```
19:46:54Z  files=199  top=89  packs=110  seats=43/49  missing=6  unclassified=0
           missing: ExecArchiveNoHarmMirror ExecNoPlaceholderScan ExecSuiteBuild ScribeShonen
                    ScribeWaveEvidence CritDesignReview
20:08:20Z  files=233  top=98  packs=135  seats=49/49  missing=0  unclassified=0
20:09:18Z  files=235  top=100 packs=135  seats=49/49  missing=0  unclassified=0   <- shipped
```

Final generation and digest:

```
$ python3 gen_index.py
wrote .../wave1/ScribeWaveEvidence.index.md: files=235 top=100 packs=135 seats=49/49 missing=0 unclassified=0 bytes=1539601
$ wc -c -l ScribeWaveEvidence.index.md
  256 55327 ScribeWaveEvidence.index.md
$ sha256sum ScribeWaveEvidence.index.md
da6a7e8bc65dc51f7afdd7b45f65d84b34fa7d4de935f820c2c118c0d5ac0776  ScribeWaveEvidence.index.md
$ grep -n '^Snapshot:' ScribeWaveEvidence.index.md
5:Snapshot: 2026-10-26T20:09:18Z (UTC) — files indexed: **235** (100 top-level artifacts, 135 fixture-pack
  members in 5 packs); seats with at least one artifact: **49/49**; total bytes: 1539601; unclassified files: **0**.
```

Index-vs-disk consistency, re-hashed row by row after the final write:

```
rows 235 mismatch 0 []
present-not-listed ['ScribeWaveEvidence.index.md']
```

Declared-deliverable completeness, final state (every present seat's declared deliverable paths, taken from the item
bodies):

```
seats present with every declared deliverable present: 49
gaps: []
top-level files: 99          # measured at the 20:08:20Z check; 100 in the shipped 20:09:18Z snapshot
```

Seat-name drift guard: attribution is by path prefix, not basename alone, so members under `<Seat>.fixtures/**`
(G1/G2/G4/G8 packs, including their `.ufo/waves/round-39/*.json` dispatch/result fixtures) and
`ExecSuiteBuild.overlay/**` are attributed to their owning seat. `unclassified=0` means every file in the directory
matched a declared seat or the pre-wave registry — no foreign or misrooted file is present in wave1.

## Findings / limits (reported, not fixed — not my scope)

1. Drift is real inside the wave and the index is a pointer index, not a closure manifest. Observed directly between
   the 20:08:20Z and 20:09:18Z snapshots: `ExecNoPlaceholderScan.md` (its receipt) landed after the first walk's
   file listing, and `ExecNoPlaceholderScan.placeholder-scan.txt` was rewritten (27441 -> 29261 bytes) after it had
   been hashed. Both are correct in the shipped snapshot; any file written after `2026-10-26T20:09:18Z` is unindexed.
   The file states this in its `## Notes` block, and its rows must be re-verified before citation.
2. The index cannot carry its own sha256 (self-reference): it is excluded from its own table by construction, and
   its bytes/line count/sha256 are recorded above. This receipt is written after the snapshot and is likewise absent
   from the table.
3. Claim assignment is an interpretation of each item's mandate against the frozen claim predicates, not a claim
   edit; the rule and the seven `C1+C2` seats are pinned above so the canonical judge can re-derive every row without
   the generator.

## Out of scope / untouched

- No lane, fleet, sibling-lane or source-tree file was written besides the two scoped paths
  (`ScribeWaveEvidence.index.md`, `ScribeWaveEvidence.md`). No git/jj command of any kind was run; no product code,
  judge, claim, axis, route or ledger was modified; no tool was installed; no network fetch was made.
- Deliverable content discipline: the index file contains only index content (header, snapshot line, table,
  missing-seat section, notes) — no receipt scaffolding, no validation tables, no plan text.

## Scratch

Scratch `/fast/scratch/hyaku/kasegi-r39/ScribeWaveEvidence/` (generator, seat map, monitor logs, dry-run index,
`index-rows.json`) removed with `rm -rf` after both scoped files were in place; verified absent:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r39/ScribeWaveEvidence
$ test -e /fast/scratch/hyaku/kasegi-r39/ScribeWaveEvidence && echo PRESENT || echo ABSENT
ABSENT
```

Report: `.ufo/waves/round-39/wave1/ScribeWaveEvidence.md`
