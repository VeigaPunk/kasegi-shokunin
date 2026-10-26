# RevScratchDiscipline — round-39 wave-1 scratch-discipline review (G6 precursor)

Seat: reviewer, leaf. Item: at wave-1 end, list kasegi-r37/r38/r39 trees under /fast/scratch/hyaku/, flag any seat dir not gone (by name); confirm no /tmp files over 50 MB left by seats; verdict + findings.

Snapshot anchor: 2026-10-26T19:35:56Z (UTC). Wave 1 was still IN FLIGHT at snapshot (dispatch 19:26–19:28Z; wave1 receipts still landing at 19:35:56Z). Disk guard green at review start: /tmp 3% (125.2G free), /var/tmp 35% (585.6G free), /fast/scratch/hyaku 25% (609.7G free).

## Verdict

PASS with watch list. No hard defect exists at snapshot: kasegi-r37 and kasegi-r38 are absent; no seat left any file in /tmp, and no /tmp entry exceeds 50 MB; every wave-1 seat that wrote a receipt before ~19:33Z has already removed its scratch. All remaining scratch presence is attributable to seats still working or in the receipt→teardown window. Final G6 live check at closure remains outstanding and must re-verify.

## Findings by severity

### HIGH
None.

### MEDIUM
- **M1 — Unregistered scratch dir `RevControls-2`** (`/fast/scratch/hyaku/kasegi-r39/RevControls-2`). Absent from the wave-1 dispatch registry (`wave1-dispatch.json` → registry.members has 49 names including `RevControls` but not `RevControls-2`; `RevControls` already cleaned its own dir). Created 19:30:56Z; at snapshot 19:35:56Z it held 14,933 files / 251,053,175 bytes with mtime 19:35:55Z — actively written. Its creation time matches the wave-2 build step (`build-wave2-final.py`, wave dir mtime 19:30Z), so it is most plausibly a wave-2/retry seat's dir rather than an orphan, but the L1 must confirm ownership. It must be gone before the closure G6 check ("r39 holds only its own --work").

### LOW
- **L1 — Receipt→teardown window seats** (receipt written, scratch still present at snapshot — expected to clean on yield; re-verify at closure): ExecConsiderthese (receipt 19:35:37Z, dir 2 files/6,914 B mtime 19:32:31Z), ExecConsidertheseLedger (receipt 19:35:32Z, dir 3 files/34,945 B mtime 19:33:37Z), ExecGradedSelftestFixture (receipt 19:35:29Z, dir 173 files/533,154 B mtime 19:34:42Z), ExecMistakesDraft (receipt 19:35:36Z, dir 1 file/9,133 B mtime 19:32:17Z), ScribeRowS057 (receipt 19:35:52Z, dir 7 files/426,020 B mtime 19:35:18Z).
- **L2 — L1's own scratch `kasegi-r39-l1`** (`/fast/scratch/hyaku/kasegi-r39-l1/`, 7 files: integration-check.sh, integration-checklist.md, landed-texts.md, make-declared-blocks.sh, make-receipt.sh, report-draft.md, report-full.md). Outside the G6 letter (not inside kasegi-r39) but it is wave-era scratch under hyaku named kasegi-r39-*; should be gone at closure too.
- **L3 — Root-level strays under /fast/scratch/hyaku/ (not kasegi-r39 wave-1 files, pre-wave, unattributed owners):** `_d.txt` (18,215 B, mtime 19:25:22Z, a corpus/SOURCES.md S112/unblob diff — kaidoku-flavored content), `line137.txt` (388 B, 18:20:34Z, web-observation verbs table), `base-census.sh` (173,962 B, 07:14:44Z, tsukuroi census script). None from this wave's seats; listed for L1 attribution.
- **L4 — Prior-round debris observed, out of round-39 scope (informational):** ~14 × /tmp/tameshi-r14-evidence-disposition-selftest.* (6.6 MB each, ~90 MB total, idle 88–225 min at review start); /var/tmp/souji-r21-replay-eq45dano (201.8 MB, other lane, pre-wave); /tmp/w5-mado-m52-selftest.* (empty dirs, other lane). All <50 MB per entry; no action taken by this seat.

### Positive controls (pass)
- kasegi-r37: absent. kasegi-r38: absent. (G6 precondition satisfied.)
- /tmp oversize: zero entries >50 MB by du over every top-level /tmp entry (mount `/tmp/.mount_appimap0T6hX`, 363.1 MB, excluded: AppImage mount point, idle ≈59 h, pre-wave, not a seat file; stat-size scan agreed).
- No kasegi wave-1 seat left anything in /tmp. Wave-era (≥19:26Z) /tmp entries all attribute elsewhere: harness (ecc-* session files, omp-worker-stderr, claude-tool-count), Chromium profile dir, other lanes (kaidoku-r40, souji-r33-close, /tmp/c1fr.py + /tmp/c1w1.py + /tmp/fr.py = round-40 counter prep, other workstream). /tmp/r39rows.txt, /tmp/r39c1-entry.md, /tmp/kaidoku-r39-census-start.txt are kaidoku-lane round-39 files (mtimes 17:27–17:33Z, pre-wave, <5 KB). /tmp/tmp.X4sDfXMVlC existed at 19:30Z and was already gone by 19:34Z (transient mktemp, owner-cleaned).
- Completed-seat cleanup: every seat with a receipt written before 19:33Z has zero scratch residue — ConnRoleGround, ExecArchiveChecks, ExecAssimilationIds, ExecCaptureStability, ExecContextGuardCheck, ExecCorrectionsR2, ExecDiskGuardProbe, ExecFrontierCapture, ExecFrontierLeads, ExecG4ResultsFixture, ExecJunkRecheck, ExecQualityCriteria, ExecScoreGap, ExecSeatIdentitySpec, ScoutReopenS057, ScoutSiblingF22, ScribeFrontierF22, ScribeProvinceF22, ScribeRowsRejected, ScribeSearchLog, ScribeLessonGate, ScribeReportInputs, ExecPinnedG8Fixture (18 dispatched seats' dirs gone; includes the heaviest early mirrors).

## Snapshot evidence (2026-10-26T19:35:56Z)

26 dirs present under /fast/scratch/hyaku/kasegi-r39 (mine: RevScratchDiscipline), total 2,763,639,582 B ≈ 2.76 GB. `mtimeZ | files | bytes | dir`:

```
19:32:02Z | files=4 | 33466 | CritDesignReview
19:34:41Z | files=98 | 190532 | CritFreezeAudit
19:34:08Z | files=14980 | 251083781 | ExecArchiveNoHarmMirror
19:35:31Z | files=7465 | 125365023 | ExecCensusAfterMirror
19:32:31Z | files=2 | 6914 | ExecConsiderthese
19:33:37Z | files=3 | 34945 | ExecConsidertheseLedger
19:34:42Z | files=173 | 533154 | ExecGradedSelftestFixture
19:35:40Z | files=119500 | 2006921013 | ExecHarnessProbe
19:32:17Z | files=1 | 9133 | ExecMistakesDraft
19:35:31Z | files=162 | 169042 | ExecNoHarmFixture
19:33:16Z | files=38 | 25053 | ExecNoPlaceholderScan
19:32:04Z | files=32 | 15722 | ExecProofSuiteSelftest
19:35:34Z | files=5 | 593846 | ExecRunbookChecks
19:35:10Z | files=7466 | 125438576 | ExecSuiteBuild
19:35:13Z | files=164 | 125459 | ExecWholeTailFixture
19:34:00Z | files=15 | 78189 | RevAssimilationBlock
19:35:55Z | files=14933 | 251053175 | RevControls-2
19:34:35Z | files=12 | 807521 | RevCorrections
19:34:27Z | files=5 | 21428 | RevFrontierAmendments
19:34:24Z | files=4 | 34481 | RevRowsCensus
19:32:45Z | files=1 | 3 | RevScratchDiscipline
19:35:55Z | files=14 | 411160 | ScribeEntryF22
19:35:18Z | files=7 | 426020 | ScribeRowS057
19:35:41Z | files=8 | 156426 | ScribeShonen
19:35:52Z | files=5 | 48721 | ScribeSpotCheckList
19:31:56Z | files=5 | 56799 | ScribeWaveEvidence
```

Dispatch reconciliation (wave1-dispatch.json registry.members, 49 seats): 18 dispatched with scratch already gone; 31 present dirs matched dispatched names; 1 present dir unmatched (RevControls-2, M1). Heaviest working dirs: ExecHarnessProbe (2.0 GB, 119,500 files — mutant-testing workspace), ExecArchiveNoHarmMirror (251 MB), RevControls-2 (251 MB), ExecCensusAfterMirror (125 MB), ExecSuiteBuild (125 MB) — all well within disk-guard headroom; footprint shrank 713 MB → 2.76 GB peak-shaped as mutant/fixture seats ran, with cleanup tracking completion.

Commands used (read-only): `bash scripts/hyaku/disk-guard.sh status`; `find /fast/scratch/hyaku/{kasegi-r37,kasegi-r38,kasegi-r39}`; per-dir `du`/`stat`/`os.walk` census; `du -sm` over all /tmp top-level entries; `find /tmp -newermt` wave-era sweep; `python3` reconciliation of wave1-dispatch.json members vs os.listdir. No writes outside my receipt and my scratch. No tools installed.

## Residual risk and verification gaps

- Snapshot is pre-closure: 20 seats were still working and 5 were in the teardown window. G6's kill rule ("any leftover kasegi-r37/r38/r39 scratch entry at filing") can only be certified live at closure — re-run the listing then; the watch names are M1, L1 (5 seats), L2 (kasegi-r39-l1), plus my own dir (removed, verified below).
- RevControls-2 ownership is inferred from timing (created 19:30:56Z ≈ wave-2 build 19:30Z), not proven; L1 confirmation pending.
- Receipts landing after 19:35:56Z are not covered by the completed-seat positive-control list.

## My cleanup

Scratch S=/fast/scratch/hyaku/kasegi-r39/RevScratchDiscipline/ removed before yield; post-removal check at 2026-10-26T19:39Z shows the dir absent from the kasegi-r39 listing (exit evidence in session log; G6 will re-verify live).
