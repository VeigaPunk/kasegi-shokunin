# ScribeFinalWaveEvidence — wave-2 evidence index (round 39)

**Item.** Build the wave evidence index (deliverable `.ufo/waves/round-39/wave2/ScribeFinalWaveEvidence.index.md`):
for every file under `.ufo/waves/round-39/wave1/` and `.ufo/waves/round-39/wave2/` list basename, bytes, line count,
sha256; produce the round totals (seat count by role per wave, dead seats if any, residual calls) for the report.
Deliverable only. Leaf seat, no subagent dispatch. Axis: coverage (C2); the artifact also carries the C1/C2 evidence
pointer for the round-39 report.

**Result.** `ScribeFinalWaveEvidence.index.md` written: **444 lines, 80213 bytes, sha256
`55f32e16e0422e7d1489e2fdf4569efcec7c7f61a6d622cc8888323bb57cbaa6`**. It indexes **289 files / 2320059 bytes** —
wave1 **236** (101 top-level artifacts + 135 fixture-pack members in 5 packs), wave2 **53** (all top-level) — with
**unclassified = 0** in both waves, **wave1 seats 49/49** and **wave2 seats 36/37** present at the snapshot instant.
Snapshot stamp inside the file: `2026-10-26T20:37:13Z` (UTC).

## Method (reproducible)

Scratch generator `gen_index.py` (scratch only, deleted after use; behaviour described here so the file can be
regenerated): `os.walk` both wave dirs; per regular file record `len(bytes)`, `wc -l`-semantics newline count
(`bytes.count(b"\n")`, flagged `no-trailing-newline` when the last byte is not `\n`), and `hashlib.sha256` over the
bytes. Seat attribution by longest seat-name prefix of the first path component (`<Seat>.<suffix>` /
`<Seat>.fixtures/…` / `<Seat>.overlay/…`). Kind: `receipt` = `<Seat>.md`, `deliverable` = other top-level
`<Seat>.<suffix>`, `pack member` = file inside a seat pack, `registry` = `swarm-registry.json`. Claim column = the
frozen claim named by the seat's spec `axes` (`depth:verifiability`→C1, `coverage`→C2, both→C1+C2); rows are joined
to the one-line item mandate taken from that seat's `wave{1,2}-spec.json` prompt body. Seat/role/axis metadata comes
from `.ufo/waves/round-39/wave1-spec.json` (49 items), `wave2-spec.json` (37 items) and the two
`swarm-registry.json` files; dispatch accounting from `wave1-dispatch.json`, `wave2-dispatch.json` and the two
`kasegi-r39-{build,falsify}.ready.dispatched` maps.

The generator excludes its own output path from the walk. That exclusion is load-bearing: the first generation
(20:35:49Z) ran when a previous index version was already on disk and produced one row describing its own stale
bytes (`79853 B / 443 lines / 91b145b5…`), i.e. a self-referential row. It was removed and the file regenerated; the
shipped file has no row for itself.

## Evidence (commands run, actual output)

Wave-2 was filling while this seat ran; sampling every 20 s from the dispatcher's end of the wave (monitor written
to scratch, `files` = regular files under `wave2/`):

```
20:16:26Z files=6   bytes=38362
20:19:26Z files=20  bytes=173922
20:22:26Z files=38  bytes=446004      # note: 446105 at 20:22:06 -> a file was rewritten smaller
20:25:46Z files=43  bytes=541883
20:29:46Z files=48  bytes=628856
20:32:46Z STABLE at 48 (no change for 180s)
```

The run was then extended, one late seat (`MutSuiteLimbs`) landed, and the index was generated three times; the two
kept states show why:

```
20:35:39Z  files=51  seats=35/37  dead=['MutSuiteLimbs','ScribeFinalWaveEvidence']
20:36:0xZ  files=52  seats=36/37  dead=['ScribeFinalWaveEvidence']   # MutSuiteLimbs landed mid-window
20:37:13Z  files=53  seats=36/37  dead=['ScribeFinalWaveEvidence']   # shipped snapshot (MutSuiteLimbs.mutations.txt included)
```

Final generation and digest:

```
$ python3 gen_index.py .../wave2/ScribeFinalWaveEvidence.index.md
self-excluded ScribeFinalWaveEvidence.index.md (1 row)
wrote .../wave2/ScribeFinalWaveEvidence.index.md: total=289 w1=236 w2=53 seats present w1 49/49 w2 36/37
     unclassified w1=0 w2=0 bytes=2320059
$ wc -l -c ScribeFinalWaveEvidence.index.md
    444   80213 ScribeFinalWaveEvidence.index.md
$ sha256sum ScribeFinalWaveEvidence.index.md
55f32e16e0422e7d1489e2fdf4569efcec7c7f61a6d622cc8888323bb57cbaa6
```

Row-by-row re-verification after the final write (`verify_rows.py`: parse every table row, re-walk both dirs,
compare bytes/lines/sha256 as a tuple):

```
rows=289 disk_files=290 mismatch=0 unlisted=1
UNLISTED ScribeFinalWaveEvidence.index.md
paths present in both waves: ['ConnRoleGround.md', 'swarm-registry.json']
```

`mismatch=0` = every indexed row reproduces from the bytes on disk. `unlisted=1` is the index itself
(self-exclusion). `ConnRoleGround.md` and `swarm-registry.json` legitimately exist in both waves as distinct bytes;
the index lists each under its own wave table.

Independent spot-check of rows with coreutils (`sha256sum`, `stat -c%s`, `wc -l`), not the generator:

```
ConnRoleGround.md   a2e1f11c21f7b7e8505312d5c7c29fd2cfa1fccfab7dd0098240e6a78ad5a507  bytes=4468  lines=44
CritFreezeAudit.md  35dc606d6117823942c9efe6fa5cdf7fa05753a476d5f17bf034fe1022e806ae  bytes=24517 lines=394
ConnC1C2.md         8b197c32a0192cce13d2085d563fb1cb9274428a837f0f09a0825a136e2da4d4  bytes=5510  lines=61
CritOverclaimScan.md 3fa22d69bf24fcfe91af87b2475636c1757608af56d964bdd9f16674e5d0a2cf bytes=22355 lines=377
MutSuiteLimbs.md    8758900ab2f9a185c80fb44977f432f0e44853c70b2661a72b38ced18e5505ba  bytes=14298 lines=224
RevCensusFinal.md   25107044e9a06c6a37e204c4fb700c302ab68ad770dc26c799c2faaaf6069db8  bytes=9672  lines=168
```

All six match their index rows.

## Round totals (in the deliverable, restated for the report)

### Seat counts by role

| role | wave1 declared | wave1 with artifact | wave2 declared | wave2 with artifact |
|---|---:|---:|---:|---:|
| connector | 1 | 1 | 2 | 2 |
| critic | 2 | 2 | 8 | 8 |
| executor | 27 | 27 | 0 | 0 |
| mutation-tester | 0 | 0 | 7 | 7 |
| reviewer | 6 | 6 | 12 | 12 |
| scout | 2 | 2 | 4 | 4 |
| scribe | 11 | 11 | 1 | 0 |
| sentinel | 0 | 0 | 2 | 2 |
| simplifier | 0 | 0 | 1 | 1 |
| **total** | **49** | **49** | **37** | **36** |

Wave-1 spec, wave-1 dispatch registry (49 members) and the wave-1 results file (49 results) agree seat for seat:
`missing=[] extra=[] dupes=[]`. Wave-2 spec (37 items) and `wave2/swarm-registry.json` (37 members) also agree
exactly (`registry_not_in_spec=[] spec_not_in_registry=[]`).

### Dead seats

- **wave1**: none — 49/49 declared seats own at least one artifact; 0 declared `Report:`/deliverable paths missing.
- **wave2**: none outside this seat. `MutSuiteLimbs` was artifact-less in the 20:35:39Z sample and is the one seat
  that landed inside the snapshot window (`MutSuiteLimbs.md` 14668 B, then rewritten to 14298 B, plus
  `MutSuiteLimbs.mutations.txt` 49617 B); it is indexed at its final bytes. The only declared seat with no artifact
  at the snapshot is **ScribeFinalWaveEvidence** (this index's author: the index and this receipt are written after
  the walk — the index cannot contain itself). After this receipt lands, wave2 is 37/37.

### Residual calls

| field | wave1 (build) | wave2 (falsify) |
|---|---|---|
| dispatch `counts.spawn` | 49 | 37 |
| dispatch `counts.resume` | 0 | 0 |
| dispatch `counts.total` | 49 | 37 |
| `resumeSends` entries | 0 | 0 |
| `policy.maxLanes` | 64 | 64 |
| residual lane capacity (maxLanes − total) | 15 | 27 |
| dispatch call recorded (`*.ready.dispatched` stamp) | 2026-10-26T16:30:46 | 2026-10-26T17:14:00 |
| seats whose agent id carries a name-dedup suffix | 6 | 6 |

Dedup-suffixed ids (evidence of same-name registrations preceding the recorded dispatch call, i.e. earlier calls in
this session, not additional seats): wave1 `ExecScoreGap-2`, `ScribeShonen-5`, `RevControls-2`, `RevRowsCensus-2`,
`ConnRoleGround-2`, `ExecSuiteBuild-2`; wave2 `RevSuiteDesign-2`, `CritC1Kill-4`, `CritC2Kill-5`, `MutC2Row-4`,
`ConnC1C2-4`, `ConnRoleGround-4`. The numeric suffix is a lower bound on prior registrations of that name
(`CritC2Kill-5` ⇒ at least five). No wave-39 dispatch is a resume: `counts.resume=0` and `resumeSends=[]` in both
dispatch files.

## Findings / limits (reported, not fixed — outside this seat's write scope)

1. **The wave-1 index is stale on two rows.** Re-measuring all 235 rows of `wave1/ScribeWaveEvidence.index.md`
   against disk: 1 file unindexed there (`ScribeWaveEvidence.index.md` itself), 0 vanished, **2 rows changed**:
   `ExecNoPlaceholderScan.md` 12420 B/263 lines/`08566ad1…` → 14299 B/293 lines/`02a022f0…` (mtime 20:10:08Z) and
   `ScribeWaveEvidence.md` 6644 B/114 lines/`5383c906…` → 6959 B/120 lines/`56d41265…` (mtime 20:09:44Z). Both
   rewrites are post-snapshot of that index; the shipped index here carries the current bytes.
2. **In-wave drift is not hypothetical.** `MutSuiteLimbs.md` was hashed at 14668 B and rewritten to 14298 B within
   the snapshot window; the wave-2 monitor saw total bytes drop (446105 → 446004 at 20:22:26Z) and rise again
   (520308 → 521694 at 20:25:26Z; 541883 → 542123 at 20:26:06Z). Any citation of wave artifacts must be by sha256,
   which is why the index carries them.
3. **A first-generation self-reference was caught and removed** (row describing the index's own previous bytes,
   `79853 B / 91b145b5…`). The generator now excludes its output path; the shipped file has no self row.
4. **Snapshot is not final state.** The index lists 289 files; after this receipt the two wave dirs hold 291 files
   (wave1 236, wave2 55). Anything written after `20:37:13Z` is unindexed. The index states this in its `## Notes`
   block, together with the line-count semantics (`wc -l`) and the self-exclusion rule.
5. **Claim column is attribution, not judgment.** It reproduces each seat's spec `axes`; the judged predicates stay
   in `claims.json`, untouched. The three wave-1 `C1+C2` seats and the nine wave-2 `C1+C2` seats visible in the
   deliverable are the seats whose spec names both owned axes.
6. **Cross-wave duplication: zero.** No wave-2 file is byte-identical to any wave-1 file (0 shared sha256 over 236
   vs 53 files); the only shared *paths* are `ConnRoleGround.md` and `swarm-registry.json`, each with different
   bytes. Wave-2 evidence was not copied from wave-1 artifacts.
7. **Trailer convention is not uniform** (informational, not a defect): 4/49 wave-1 receipts and 12/36 wave-2
   receipts contain a literal `Report:` trailer; most receipts end with their findings sections instead. The wave-2
   item bodies themselves mandate the trailer, so this is a per-seat formatting choice, orthogonal to artifact
   presence.

## Out of scope / untouched

- Wrote exactly two paths in the lane: this receipt and
  `.ufo/waves/round-39/wave2/ScribeFinalWaveEvidence.index.md`. No other lane, fleet, sibling-lane or source-tree
  file was created or modified; nothing under `.ufo/state/`, `.scratch/`, `scripts/`, `corpus/` or `MANIFEST.json`.
- Read-only throughout: no git/jj command of any kind was run (no mutation, no clone, no fixture); no product code,
  claim, axis, route, ledger or judgment touched; no tool installed or upgraded; no network fetch; no pacman.
- Scratch: `/fast/scratch/hyaku/kasegi-r39/ScribeFinalWaveEvidence/` only (`gen_index.py`, `coverage.py`,
  `verify_rows.py`, `monitor.sh`, `monitor.txt`, `coverage.json`, `stats.json`, dry-run index), removed with
  `rm -rf` before yielding; verified absent:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r39/ScribeFinalWaveEvidence
$ test -e /fast/scratch/hyaku/kasegi-r39/ScribeFinalWaveEvidence && echo PRESENT || echo ABSENT
ABSENT
```

Report: `.ufo/waves/round-39/wave2/ScribeFinalWaveEvidence.md`
