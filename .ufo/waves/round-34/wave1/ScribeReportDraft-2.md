# Round 34 report body — DRAFT for the L1 (not the filed report)

Seat `ScribeReportDraft-2` (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
write scope exercised: this file only. The dispatch named the path `wave1/ScribeReportDraft.md`; the
L1's steering message of 2026-10-26 named `wave1/ScribeReportDraft-2.md`, which is this file (the
`-2` suffix is the seat id). Nothing else was written; no product file, no git/jj mutation, no
subagent, no `agent://all`.

**Replacement contract (read first).** Every `<LANE_HASH>` below is for the L1 to replace with the
integration commit. **No `<LANE_HASH>` may survive into the filed report**: C1's kill rule counts
`grep -c '<LANE_HASH>' SCORECARD.md` → `0`, and `critic` finding F1 (§7.2) shows three `<LANE_HASH>`
tokens still alive in `corpus/` — do not copy this draft's placeholders into any lane file. If this
draft is pasted anywhere, run `grep -c 'LANE_HASH'` on the destination after the edit.

Commit naming: base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`; wave-1 spec/dispatch
`206e5108f1190e61b3e2622d21cab8a5d921650c` (lane HEAD at drafting; every `ci`-routed measurement
below was taken at this HEAD with the wave's landings uncommitted in the working copy). Integration
commits are `<LANE_HASH>` — the L1 commits.

Answering model: session route (`opencode-go/deepseek-v4.1-flash` per project context; no seat passes
a model). Tools installed/upgraded: none. Scratch: `/fast/scratch/hyaku/kasegi-r34/ScribeReportDraft`
(created, used for measurement captures, deleted before yielding; verified absent). No network fetch
performed by this seat.

---

## 0. Drafting state and quiescence

- Receipts present at drafting: **61** `*.md` under `.ufo/waves/round-34/wave1/` out of **65**
  declared seats (`swarm-registry.json`, roles executor 19, reviewer 13, scribe 10,
  mutation-tester 7, scout 5, critic 5, connector 3, sentinel 2, simplifier 1). The directory was
  still filling while this draft was written; late seats are named in §8.3.
- Every number in §3 was **run by this seat** in the lane worktree at 2026-10-26T05:42Z (batteries
  `inflight-1.txt`/`inflight-2.txt`, scratch-only, deleted) and cross-checked against the seat
  receipt named in the row. Where a receipt and my run disagree, both are printed (§7).
- The working tree is **dirty by design**: the wave's landings are uncommitted (`git status
  --porcelain`: `M SCORECARD.md`, `M corpus/QUALITY.md`, `M corpus/instruments/capture-binding-check.py`,
  `M corpus/instruments/frontier-recheck-count.py`, `M corpus/source-snapshots/round-26/manifest.json`,
  `M corpus/source-snapshots/round-32/manifest.json`, `M corpus/lessons/round-29.md`,
  `M corpus/lessons/round-33.md`, `M corpus/SOURCES.md`, `M corpus/README.md`,
  `M corpus/instruments/README.md`, `?? corpus/source-snapshots/round-34/`, plus new instruments).
  No "quiescent bytes" claim is made: this is an in-flight draft, and the L1 must re-run the counting
  commands after it commits.

---

## 1. Work performed

Opens: the round targets **C1 `depth:verifiability`** (score 4 — the lane's lowest non-retired axis,
`claims.json` → `lowest_non_retired_axis`) and **C2 `coverage`** (7). `depth:density` (9) is not
claimed; it is measured only as no-harm (`RevNoHarm.md`).

### C1 — the nine round-33 routed defects land with runnable closure checks

- New counter `corpus/instruments/r-defect-closure.sh` (665 lines, 28,512 B, sha256
  `0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1`, bash 5, nine `check_rN()`
  functions). Plain run prints one `R# check=… open=0|1` line per defect plus `closed=K/9`;
  `--root DIR` retargets the same nine checks; `--selftest` runs each check twice (live tree +
  a fixture carrying that check's *original* defect) and passes a case only when the live run is 0
  **and** the broken fixture is rejected. Evidence: `wave1/ExecRDefectClosureSuite.md` §1–§7.
- New counter `corpus/instruments/kill-rule-check.py` (743 lines, 34,914 B, sha256
  `e33a300fc7341f8d6e254fc12441de1ba0ec6252483aeaf6e8806622dba0fc15`). Two independent oracles
  (`selftest-shape`, external fixtures), three exactly-once mutant rows, four controls. Evidence:
  `wave1/ExecKillRuleCheck.md` §1–§6; machine receipt `wave1/ExecKillRuleCheck.json`
  (sha256 `9d6833cb44137ecc53d845402caeefa423e8d13f87a96e5f515074ac20adec3d`).
- Hardened `corpus/instruments/capture-binding-check.py` 492 → 892 lines, 11 → 23 selftest cases,
  new rules: per-file orphan binding, nested snapshot dirs, strict-UTC `fetched_utc`, duplicate
  manifest records, dual-`https://` rows, rejected-row anchors, summary-only selftest rejection.
  Digest `b4182665ba5cf544…b7f9` → `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`.
  Evidence: `wave1/ExecCaptureBindingHarden.md` §1–§4.
- `corpus/instruments/frontier-recheck-count.py` rule A made bidirectional (`aa60b581…` →
  `87b14892dfc42792056c7a9f09a0783e9d749d0478f376841c98bfc25e0a7c29`, +214/−15) with a new
  six-case selftest. Evidence: `wave1/ExecFrontierBidirectional.md` §1–§5.
- Surface repairs for R1–R3, R6–R8: SCORECARD marker fill + `Correction (round 34)`; erratum 2 with
  the per-id restatement and the pre-freeze satisfiability step; QUALITY R20 note + R22/R23/R24;
  round-26 manifest orphan declaration for `S040-live.txt` with a corrected `purpose`; round-32
  manifest strict-UTC `fetched_utc`; round-33 lesson R7 + R4 errata; round-29 M33-3 erratum.
  Evidence: §2 rows 5–15 and the receipts named there.
- Independent review of the whole C1 surface: `RevClaimsFreeze.md` (all counting commands re-run,
  MATCH), `RevC1BeforeAfter.md` (frozen before-values re-derived on base bytes, MATCH),
  `RevRSuite.md`, `RevKillRule.md`, `CritC1Kill.md`, `MutCaptureBindingLimbs.md`,
  `MutKillRuleMutants.md`, `MutSelftestSummary.md`, `MutManifestField.md`, `MutFrontierRuleA.md`.

### C2 — Frontier F17 admitted (16 → 17): Immunefi VSCS v2.2

- Capture `corpus/source-snapshots/round-34/S051.txt` (8,502 B, 175 lines, sha256
  `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5`; HTTP 200; instrument UA;
  `fetched_utc 2026-10-26T05:31:10Z`) and manifest `corpus/source-snapshots/round-34/manifest.json`
  (7,654 B, 122 lines, sha256 `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe`,
  18 assertions Q1–Q18). Evidence: `wave1/ExecSnapshotR34.md` §1–§3.
- Entry `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (113 lines, 11,143 B,
  sha256 `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a`), header `ground: F17`,
  `source: S051`, one Q10-form `recheck:` line. Evidence: `wave1/ScribeEntryF17.md`;
  independent ADMIT `wave1/RevEntryF17.md` §3/§Verdict.
- Registry row `| S051 |` appended at `corpus/SOURCES.md:57` (tier A, kind `docs`, status `mined`,
  opened `2026-10-26`, recheck `90d`), plus one Search-log bullet and three `## Registry changes`
  lines (five added lines, zero deletions). Evidence: `wave1/ExecRegistryAppend.md` §2–§6;
  draft provenance `wave1/ScribeSOURCESRow.md`; search receipt `wave1/ScribeSearchLog.md`.
- Frontier row F17 + coverage-map row + r34 amendment paragraph appended to `corpus/README.md`
  (`:343-368`, +26/0) — the row no other seat owned. Evidence: `wave1/ExecHarnessAfter.md` §3.
- Live drift re-open: fresh capture of the same URL byte-identical to the committed snapshot
  (`cmp` equal, equal sha256, 0 differing lines). Evidence: `wave1/ScoutImmunefiLive.md` §Verdict.
- Negative sweep for the ground: sibling corpora 0 hits for `Immunefi`/`VSCS`/`smart.contract`/
  `Web3`/`blockchain`; staged `merge/kasegi/` package 0 files matching `immunefi|vscs`. Evidence:
  `wave1/ScoutSiblingSweep.md` §1–§3; `wave1/ScribeSOURCESRow.md` §4.

### Non-claim frontier items

- **Assimilation: none.** Id-collision check re-run and reproduced independently:
  `reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7
  slice_malformed_lines=0` (`wave1/ScribeAssimilationGate.md` §baseline/§re-derivation;
  `wave1/ScoutPackageThemes.md` §Verdict). Quarantine slice re-derived with per-row verdicts; no
  staged entry has fully-met flip conditions. No staged row or entry adopted this round.
- **considerthese proposal 6 (event-driven reflections)** mined into `corpus/QUALITY.md` **R23**
  (citation `considerthese/2026-10-25.md:76-77`, 2026-10-25). Evidence:
  `wave1/ScribeQualityDraft.md` (row text for R22/R23/R24); row printed at `corpus/QUALITY.md:227`.
- **Mistakes M34-1 / M34-2** mined into QUALITY **R24** (tightened kill rule: one `selftest case=`
  line per case, `cases>=11`) and **R22** (pre-freeze satisfiability), with the round-33 lesson
  errata (R4 3-of-4, R7 counts). Evidence: `wave1/ScribeQualityDraft.md`,
  `wave1/ExecLessonErrata.md` §1–§3, `wave1/ExecQualityAppends.md` §2.

---

## 2. Landed changes

Commit column: `<LANE_HASH>` = the L1's integration commit (nothing is committed at drafting). The
"measured diff" values are `git diff --numstat 014ee2d7 -- <path>`-class readings taken by the seat
named in the last column, at the in-flight tip.

| # | Change (path) | Commit | Measured diff / digest | Proving receipt |
|---|---|---|---|---|
| 1 | `corpus/instruments/r-defect-closure.sh` (new) | `<LANE_HASH>` | 665 lines, 28,512 B, sha256 `0beafed2…d460d1` | `ExecRDefectClosureSuite.md` §1 |
| 2 | `corpus/instruments/kill-rule-check.py` (new) | `<LANE_HASH>` | 743 lines, 34,914 B, sha256 `e33a300f…0fc15` | `ExecKillRuleCheck.md` §1 |
| 3 | `corpus/instruments/capture-binding-check.py` | `<LANE_HASH>` | 892 lines, sha256 `3d9e5e0d…da99fa`; selftest 11 → 23 cases | `ExecCaptureBindingHarden.md` §1–§2 |
| 4 | `corpus/instruments/frontier-recheck-count.py` | `<LANE_HASH>` | `214 15`; `aa60b581…` → `87b14892…`; guards at `:205`, `:207` | `ExecFrontierBidirectional.md` §1–§3 |
| 5 | `corpus/instruments/README.md` | `<LANE_HASH>` | three appended sections (hardening, rule A, round-34 additions); 656 → 761 → 930 lines, no line above moved | `ExecCaptureBindingHarden.md` §1; `ExecFrontierBidirectional.md` §1; `ExecKillRuleCheck.md` §1 |
| 6 | `corpus/source-snapshots/round-32/manifest.json` | `<LANE_HASH>` | 3 cells (`fetched_utc` ×2, `purpose` sentence); `6e4e719a…` → `72ab4e68…`; 0 records/assertions changed | `ExecManifestR32Normalize.md` §2–§4; `RevManifestR32.md` |
| 7 | `corpus/source-snapshots/round-26/manifest.json` | `<LANE_HASH>` | `sources` byte-identical; `orphans` key + rewritten `purpose`; `1c913132…` → `33ac33c3…` | `ExecS040Orphan.md`; `RevOrphan.md` §2 |
| 8 | `corpus/source-snapshots/round-34/S051.txt` (new) | `<LANE_HASH>` | 8,502 B, 175 lines, sha256 `4fd8ed98…b325a5` | `ExecSnapshotR34.md` §1 |
| 9 | `corpus/source-snapshots/round-34/manifest.json` (new) | `<LANE_HASH>` | 7,654 B, sha256 `d5077f81…42eebe`, 18 assertions | `ExecSnapshotR34.md` §2 |
| 10 | `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (new) | `<LANE_HASH>` | 113 lines, 11,143 B, sha256 `948b202e…5ac1d8a` | `ScribeEntryF17.md`; `RevEntryF17.md` §Verdict |
| 11 | `corpus/SOURCES.md` (S051 row, Search-log bullet, three R8 lines) | `<LANE_HASH>` | 5 added / 0 removed; 50 → 51 rows; `:57` row | `ExecRegistryAppend.md` §2–§6 |
| 12 | `corpus/README.md` (F17 + coverage row + r34 amendment) | `<LANE_HASH>` | `26 0`; F17 at `:361` | `ExecHarnessAfter.md` §3 |
| 13 | `corpus/QUALITY.md` (R20 note, R22, R23, R24) | `<LANE_HASH>` | `head -213` byte-identical (`00781e09…`); rows at `:220-228`; digest `77d99df9…` | `ExecQualityAppends.md` §2–§3; `ScribeQualityDraft.md` |
| 14 | `SCORECARD.md` (R1 fill + erratum 2 + correction + round-34 section) | `<LANE_HASH>` | `31 3` for the R1/R2 edits (`e03fbefa…` → `b8fc8c66…`), then `## Round 34 — frozen claims C1/C2` at `:1121-1243` (+124); markers 2 → **0** (re-checked at 06:00Z) | `ExecScorecardMarkers.md` §2–§4; `ExecErratum2.md` §3; `ScribeScorecard.md` §2–§4 |
| 15 | `corpus/lessons/round-33.md` (R7 + R4 errata) | `<LANE_HASH>` | `108 0`; `head -138` byte-identical (`ca17591d…`) | `ExecLessonErrata.md` §0–§3 |
| 16 | `corpus/lessons/round-29.md` (M33-3 erratum) | `<LANE_HASH>` | `74 0`; `head -263` byte-identical (`78ae8080…`) | `ExecLessonErrata.md` §0 |
| 16b | `corpus/lessons/round-34.md` (new lesson) | `<LANE_HASH>` | 518 lines / 47,524 B: seven required sections + provenance section; digest changes as lanes land | `ScribeLesson.md` §1–§5 |
| 17 | `.ufo/waves/round-34/c2-controls/junk-f17.md` (junk twin) | `29f606d` (freeze) | blob `50f7a84c…`, 940 B; shape counters 3/3; rejected at quote level | `RevJunkTwin.md` §1–§3; `CritC2Kill.md` |
| 18 | `corpus/QUALITY.md` R24 row | `<LANE_HASH>` | row at `:228` (kill rule + one `selftest case=` line per case) | `ExecQualityAppends.md`; suite check R4 |
| 19 | `PROVINCE.md` F17 amendment | **OPEN** | proposed exact bytes, not landed: `PROVINCE.md:74` frontier list still stops at F16 | `ScribeSkillGate.md` §1, §4a |
| 20 | `LOG.md` round-34 entry | `<LANE_HASH>` (L1 owns) | not present at drafting (`grep -c '^## Round 34' LOG.md` → 0) | — (L1) |
| 21 | receipts + machine evidence under `.ufo/waves/round-34/wave1/` | `<LANE_HASH>` | 49 `*.md` + `ExecKillRuleCheck.json` at drafting | §0 |
| 22 | `.ufo/waves/round-34/claims-erratum-1.md` | `<LANE_HASH>` (**untracked at drafting**: `git status --porcelain .ufo/waves/round-34/` → `?? .ufo/waves/round-34/claims-erratum-1.md`) | C1 counting-literal scope ruling (records 40 → 41) | `claims-erratum-1.md`; §3 C1.6 |

Append-only integrity (measured by the seats named): `QUALITY.md` `head -213` identical;
`round-33.md` `head -138` identical; `round-29.md` `head -263` identical; `round-26/manifest.json`
`sources` byte-identical; `round-32/manifest.json` records/assertions identical (`records=2 quotes=14`);
`SOURCES.md` five added lines, zero deletions; `README.md` `26 0`. Deletions exist only where the
frozen claims require them: SCORECARD `3` (the two marker lines' replacement text) and the two
instruments' internal rewrites (`capture-binding-check.py` 87, `frontier-recheck-count.py` 15) —
classified line-by-line in `RevNoHarm.md` §A.

---

## 3. Before → after measurements

### C1 — `depth:verifiability` (4 → held 4)

| # | Counting command (claims.json form) | Before (base `014ee2d` / freeze `29f606d`) | After (working tree at `206e510`, 2026-10-26T05:42Z) | Commit measured |
|---|---|---|---|---|
| 1 | `bash corpus/instruments/r-defect-closure.sh` | instrument absent: `ls_exit=2` (`c1-controls/before.txt`); suite retargeted at base bytes prints `closed=0/9 exit=1` | **`closed=9/9 exit=0`** (9 `R# check=… open=0` lines) | `206e510` + worktree (`ExecRDefectClosureSuite.md` §3, §5) |
| 2 | `bash corpus/instruments/r-defect-closure.sh --selftest` | n/a (absent) | **`selftest cases=9 failures=0`**, exit 0; 9 × `selftest case=R# live=pass fixture=rejected verdict=pass` | same (`ExecRDefectClosureSuite.md` §4) |
| 3 | `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=11 failures=0` (no per-file, nested-dir, strict-UTC, dup-record, dual-https, rejected-anchor, summary-only cases) | **`selftest cases=23 failures=0`**, exit 0 (N=23 ≥ 19); the nine contract-named cases all present; two runs byte-identical (`sha256(stdout) ca3759d1…a3a3a51`) | `ExecCaptureBindingHarden.md` §2 |
| 4 | `python3 corpus/instruments/kill-rule-check.py` | instrument absent (`ls_exit=2`); the frozen round-33 rule let 2 of 4 mutants survive (`c1-controls/before.txt`) | **`mutants=3 killed=3 survivors=0 invalid=0`**, `gates=6 failed=0` at the `ExecKillRuleCheck` pin (`gates=7 failed=0` on the later bytes `RevKillRule.md` §1 measures — one more gate row, same verdict), `controls=4 rejected=4`, exit 0; stdout sha256 `f6ac4b53…c02e573` on two runs | `ExecKillRuleCheck.md` §3 |
| 5 | `grep -c '<LANE_HASH>' SCORECARD.md` | `2` (`:988`, `:1087`) | **`0`** (grep exit 1) + `Correction (round 34)` at `:1116` naming `7963976e`/`014ee2d` | `ExecScorecardMarkers.md` §3–§4; suite R1 |
| 6 | `python3 corpus/instruments/capture-binding-check.py` (C1 instrument baseline) | `records=40 bound=40 unbound=0` exit 0 (round-33 tip `7963976e`) | **`records=41 bound=41 unbound=0`**, exit 0 — `AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt`. The literal **`records=40` is no longer reachable**; `claims-erratum-1.md` rules the invariant `bound=records, unbound=0, exit 0`. Intermediate state observed (S051 capture before its registry row): `FAIL rule=no-row record=S051`, `records=41 bound=40 unbound=1`, exit 1 — rule B failing closed | `claims-erratum-1.md`; `ExecCaptureBindingHarden.md` §3; `ExecS040Orphan.md` §Verification; my run `inflight-2.txt` |
| 7 | round-32 manifest `fetched_utc` shape | `['2026-10-25T23:14:00-03:00', '2026-10-25T23:14:00-03:00']` (local offset in a `_utc` field) | `['2026-10-26T04:16:06Z', '2026-10-26T04:16:16Z']`; offset-count grep `0`; strict-UTC regex true for both | `ExecManifestR32Normalize.md` §3–§4; `RevManifestR32.md` (verdict + strict-UTC section) |
| 8 | round-26 `S040-live.txt` binding | no manifest record, no orphan list; `purpose` said the file "was not present" | `orphans=1 orphan=S040-live.txt`, declared sha256 equals file bytes (`b7f7b55f…e286c`, 33,463 B / 503 lines), `purpose` rewritten; `records=1` unchanged (no inflation) | `ExecS040Orphan.md`; `RevOrphan.md` §2 |
| 9 | `corpus/QUALITY.md` R20 reading | R20 says "exactly one registry-row URL" (superseded global reading) | `Note (round 34)` at `:220-222` names R20 and states the per-id supersession; R22/R23/R24 appended at `:226-228` | `ExecQualityAppends.md` §2–§3; `RevErrata.md` §1 (verdict summary) |
| 10 | round-33 lesson R7 erratum | counts filed as "19"/"23" characters, `S050.txt:69` for the applicability sentence | appended erratum: `19 → 31`, `23 → 22` (`printf\|wc -m` shown), `S050.txt:70` | `ExecLessonErrata.md` §1; suite R7 |
| 11 | `frontier-recheck-count.py` rule A | one-directional: `header-sources-not-rechecked` only; `selection-not-cited-by-entry` dead by construction (`cited` included the recheck line) | both directions enforced (`declared ⊄ recheck` **and** `recheck ⊄ declared`, new problem name `selection-not-declared-by-entry`, guards at `:205`/`:207`); selftest `cases=6 failures=0`; base tool passes the reverse fixture (`exit=0`), landed tool exits 1 | `ExecFrontierBidirectional.md` §2–§5; `ExecRDefectClosureSuite.md` §7 |
| 12 | junk twin control | absent from `corpus/`; frozen control at `.ufo/waves/round-34/c2-controls/junk-f17.md` (blob `50f7a84c`, committed at freeze) | twin still passes shape counters 3/3 **and** is rejected at the byte level: asserted fabricated sentence → `MISMATCH reason=quote-not-found`, exit 1; manifest-missing mode exit 2. **No reviewer REFUSE exists** (§7.1) | `RevJunkTwin.md` §2–§3; `CritC2Kill.md`; `RevC2BeforeAfter.md:282-287` |

**C1 verdict (this draft's reading): every frozen literal reproduces on the landed bytes —
`closed=9/9`, `cases=9 failures=0`, `cases=23 failures=0`, `survivors=0`, markers 0, strict-UTC,
S040 bound-or-listed, rule A bidirectional. Score held at 4.** Two qualifications the L1 should
carry, both receipt-backed: the frozen `records=40` literal is dead (erratum 1 governs, §7.3) and the
junk-twin refusal limb is unmet (§7.1); and the attacker seat shows 3 of 5 vectors leave the kill
rule satisfiable without the certified property (§7.9), so C1 must **not** be described as a
verifiability *increase* in this round.

### C2 — `coverage` (7 → held 7)

| # | Counting command | Before | After | Commit measured |
|---|---|---|---|---|
| 1 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | `16` | **`17`** (F17 at `:361`) | worktree (`ExecHarnessAfter.md` §3; my run) |
| 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `50` | **`51`** | `ExecRegistryAppend.md` §5 |
| 3 | `grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md` | `0` | **`1`** (line 57, NF=13) | same |
| 4 | `grep -lE '^source: S051 ' corpus/knowledge/*.md \| wc -l` | `0` | **`1`** (`immunefi-vscs-v2-2-smart-contract-severity.md`) | `RevC2BeforeAfter.md` §4 |
| 5 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=19 pass=19 exit=0` | **`entries=20 pass=20 exit=0`** incl. `PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051` (note spacing; the literal `PASS F17 ids=S051` is **not** greppable — F-4/`ScoutDatawalk.md` §1) | `ExecHarnessAfter.md` §2–§3 |
| 6 | `source-recheck.py --manifest …round-34/manifest.json --source S051` | `manifest UNAVAILABLE reason=missing`, exit 2 | **exit 0**; `S051:sha256 OK` + 18 assertions, 16 × `occurrences=1`, `Q9`/`Q17` `occurrences=2 anchor=N-ok`, `Q2/Q5/Q6 normalized=markup-whitespace` | `ScribeEntryF17.md` (Q1–Q10 table); my run `inflight-2.txt` |
| 7 | `sources-census.sh validate --root … kasegi` | exit 0, `W04 S028`, `W04 S029`, `ok` | exit 0, **same three lines**, no E-code, no new W | `ExecCensusAfter.md` §2; `RevCensus.md`; `ExecRegistryAppend.md` §2–§6 |
| 8 | knowledge entries / registry histograms | 45 entries; `rows=50`, tier `A=47 B=1 C=2`, status `mined=38 queued=9 rejected=3` | **46 entries**; `rows=51`, tier `A=48 B=1 C=2`, status `mined=39 queued=9 rejected=3` (both histograms sum to 51) | `RevCensus.md` §2–§3 |

**C2 verdict (this draft's reading): every frozen counter hits 20/20, 51, 1, 1, exit 0, exit 0.**
Two qualifications, both receipt-backed: (a) the frozen kill-rule sentence's second limb — "a
non-author reviewer REFUSE on record" — is unmet, and the twin control is mixed and its rejection
line is not executable as phrased (§7.1); (b) the gate is not provenance-sound — a fabricated
capture with a self-consistent manifest passes every counter (§7.14, `CritC2Kill.md` §Verdict).
Score held at 7 on the counted surface; the L1 decides whether (a) or (b) is a kill-rule trigger or
a disclosure.

---

## 4. Sources & frontier

- **Registry 50 → 51.** Added: `S051` (tier **A**, kind `docs`, status `mined`, opened `2026-10-26`,
  recheck `90d`, used-by the F17 entry) — one row, five total added lines, zero cell changed on any
  pre-existing row (`S001–S050 untouched`). Tier histogram A 47 → 48; kind histogram `docs` 38 → 39.
- **Rows touched, old → new:** none. The only row-level statement that changes is the tally
  (`50 → 51`) and the two provenance bullets (live capture, no staged row; no recency claim).
- **Frontier 16 → 17.** F17 = "Immunefi Vulnerability Severity Classification System v2.2 —
  Web3/smart-contract bounty severity classification", status `admitted`, entry
  `knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, sources `S051`. The r34 amendment
  paragraph states `17/17 admitted` and leaves the 0/18 lost-domain denominator untouched.
- **Ground novelty:** sibling sweep 0 hits; staged package 0 hits; the lane's prior platform ladders
  (S043/S044/S049/S050) are reward/severity ladders for other programmes, not a Web3 per-asset-class
  impact table (`CritC2Kill.md` § Verdict, `ScoutSiblingSweep.md` §1).
- **Live re-open:** byte-identical to the committed capture (`ScoutImmunefiLive.md` §Verdict); the
  v2.2 page makes no recency claim, and the S051 row deliberately carries none (the observed v2.3
  page is a fetch observation, not corpus evidence — `ScribeSOURCESRow.md` §3/§5).
- **Assimilation:** none adopted. `reg_ids=51 staged_ids=94 collisions=21` (S031..S051),
  `slice_rows=7`, `slice_malformed_lines=0`; every staged theme re-confirmed refused with its flip
  condition (`ScoutPackageThemes.md` §Verdict; `ScribeAssimilationGate.md`).

---

## 5. Trend verdicts

- **expansion: `improved`.** One admitted frontier row on ground the coverage map did not hold (F17),
  one new knowledge entry (46), one new tier-A row (51), and two new capabilities enter the
  instrument set (`r-defect-closure.sh`, `kill-rule-check.py`). Evidence: §3 C2 rows 1–8;
  `ExecRDefectClosureSuite.md` §1; `ExecKillRuleCheck.md` §1.
- **quality: `improved`.** Nine round-33 routed defects now have runnable closure checks that fail on
  the defect-bearing tree (`closed=0/9` base vs `closed=9/9` landed, `cases=9 failures=0`) and a
  do-nothing control that cannot fake them (fake prints `9/9`, real prints `0/9` on base bytes);
  the surviving-mutant class is instrumented (`survivors=0`, `controls=4 rejected=4`, witness
  `CTL-equivalent` prints `survivor`); the capture-binding selftest more than doubles (11 → 23) and
  the audit gains per-file orphan, nested-dir and strict-UTC rules (`orphans=1`, `fetched=3`,
  `missing_manifest=0`, `multi_row_url=2`); rule A is bidirectional with a base-vs-landed
  discrimination shown (`ExecRDefectClosureSuite.md` §7). Against: three critique receipts find the
  refusal record absent, the `records=40` literal dead, and `<LANE_HASH>` still alive in `corpus/`
  (§7).
- **discernment: `improved`, with routed defects.** In favour: the claims' non-claim mistakes are
  grounded and fixed with checks that can fail (M34-1 → R24 + `kill-rule-check.py`; M34-2 → R22 +
  suite); the junk twin is shown to pass every shape counter and still be rejected at quote level;
  the C2 entry passed a non-author ADMIT on final bytes with an earlier revision superseded and
  disclosed (`RevEntryF17.md` §Verdict); the C1 before-values were independently re-derived on base
  bytes (`RevC1BeforeAfter.md` §Verdict). Against: the C2 kill rule's reviewer limb is unmet; the
  R9 closure check is existence-only; two critics found overclaim-level wording (below). These are
  routed, not resolved, by this seat. Additionally, the sentinel's two axes FAIL on process grounds
  (§7.10: one out-of-lane file still present, four jj working-copy snapshots, one false "no jj
  mutation" declaration) and the attacker seat measures three kill-rule gaps (§7.9); the credential
  scan is clean (§7.11). Discernment credit for the round rests on the *filing* of these findings,
  not on their absence.

---

## 6. SHONEN lines

`SHONEN.md` had not been updated at drafting (`ScribeShonen` seat pending). Lines below are the
shape the L1/ScribeShonen should land, each with the round-34 evidence pointer:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — unchanged
  this round (`ScribeSkillGate.md` §1: blob identical base→freeze→HEAD→worktree, `anchorcheck` 12
  in-range, 0 bad); no new SKILL row is owed because no new gate or capability enters SKILL's text.
- [~] At least one end-to-end domain task executed and logged in LOG.md — F17 admitted end-to-end
  (capture → manifest → entry → registry row → frontier row → harness 20/20 → census exit 0);
  LOG entry is `<LANE_HASH>` (L1).
- [~] Instructions executable by an agent without oral context — nine closure checks + both
  instruments run from the lane root with no arguments (`closed=9/9`, `cases=23 failures=0`,
  `survivors=0`); foreign-cwd/scratch discipline per the seats that measured it (§8.3).
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md` **needs its F17 append at
  integration** (`ScribeSkillGate.md` §1, §4a: the frontier list stops at F16); no sibling holds the
  ground (`ScoutSiblingSweep.md`), no live bounty target was contacted, no credential material in any
  new file (`SentCred` pending — see §8.3).

---

## 7. Findings and conflicts (verbatim, for the judge)

### 7.1 The C2 junk-twin kill is half-demonstrated (reviewer limb missing)

- `RevJunkTwin.md` §Verdict: "the junk-twin control holds. All four seat criteria verified by
  execution: (1) committed at the freeze commit; (2) shape counters pass it `3/3`; (3) the admission
  gate rejects its bytes — fabricated quote `MISMATCH reason=quote-not-found` exit 1, manifest-missing
  mode exit 2; (4) the F17 entry review does not admit the junk bytes".
- `CritOverclaim.md:92-93`: "value 'source-recheck on it fails (exit 2)' proves nothing. No reviewer
  REFUSE for `junk-f17.md` exists in `wave1/` at read time".
- `RevC2BeforeAfter.md:282-287`: "The non-author reviewer REFUSE record was not yet on disk …
  C2's after-value ('non-author reviewer REFUSE on record') is therefore **half-demonstrated**".
- `ExecRegressionC2.md:199-204`: "No receipt records a REFUSE verdict on the junk twin".
- **My own check (2026-10-26T05:45Z):** `grep -rn 'REFUSE' .ufo/waves/round-34/wave1/*.md` returns
  only sentences *about* the absence; no seat issues a REFUSE on the twin.
- **Path conflict:** C1's after-value and the R9 check name `c2-controls/`; the only committed twin is
  `.ufo/waves/round-34/c2-controls/junk-f17.md` (freeze commit `29f606d`, blob `50f7a84c`).
  `corpus/c2-controls/` does not exist (`ls` → exit 2). The suite's R9 limb tests existence of the
  wave-path file only (`R9 check=… junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0`), so the
  "committed under `c2-controls/`" limb is satisfied by a **pre-freeze** artifact rather than by a
  new production control.
- **The two readings disagree; both are on disk. Holds (reviewer):** `RevJunkTwin.md` — see above.
  **Does not hold as frozen (critics):** `CritOverclaim.md` F1 — "the junk-twin rejection limb is
  false as frozen; the twin passes its own recheck at tip" (the twin's `recheck:` line is
  byte-identical to the real entry's, so both exit 0; `source-recheck` never accepts a markdown
  file, so "exit != 0 on the twin" only reproduces by handing it a non-manifest); `CritC2Kill.md`
  G5 — "so 'junk twin rejected' is true for the committed twin against the committed capture, and
  false in general"; `ScoutDatawalk.md` F-1 — "junk-twin rejection has no executable form as
  phrased". `corpus/lessons/round-34.md` §Gate records both readings and declines to adjudicate.
- **The twin is a mixed control.** `ScoutDatawalk.md` F-1b and `CritOverclaim.md` F1b: one of its
  two "fabricated" sentences is true against the capture. My check:
  `grep -c 'Direct theft of any user funds' corpus/source-snapshots/round-34/S051.txt` → `1`
  (`:75`); `grep -c 'five severity levels for smart-contract exploits' …` → `0`. The label at
  `c2-controls/junk-f17.md:17` calls the whole block fabricated.

### 7.2 `<LANE_HASH>` survives in `corpus/` — M34-2's closure is incomplete

- `CritMistakes.md` §F1: "M34-2's closure verdict is false: `<LANE_HASH>` occurs 3 times in
  `corpus/`, and one site still" — the live sites are
  `corpus/lessons/round-33.md:17` and `:126` (the sentence "Its two `<LANE_HASH>` markers are the
  L1's edit" is now false) and `corpus/lessons/round-33-verifier-spotcheck.md:165` (the R1 finding,
  quoted). Counts measured by me: `round-33.md` = 2, spotcheck = 1.
- `ExecScorecardMarkers.md` §6 raised the same residual knowingly and left it to the L1:
  "`corpus/lessons/round-33.md:126` still states … That sentence now describes stale state".
- The C1 kill rule is scoped to `SCORECARD.md` (count 0, holds); it does not sweep `corpus/`.

### 7.3 The frozen `records=40` literal is dead (`claims-erratum-1.md`)

`ExecCaptureBindingHarden.md` §3 "Finding for the L1 (claim text, not the counter)" and
`.ufo/waves/round-34/claims-erratum-1.md`: the audit is corpus-wide, so the S051 record makes the
count 41. The erratum's own text says it was "committed before any final C1/C2 after-state is
measured or reported"; measured now, the file is **untracked** (`??`), so that ordering rests on its
mtime and on the L1's account until the L1 commits it. the intermediate unbound=1 `FAIL rule=no-row record=S051` is shown as rule-B evidence, not
as a defect state. The L1 filed the erratum before integration; this draft cites the erratum, not the
literal.

### 7.4 `kill-rule-check.py --selftest` was inconsistent mid-wave, resolved at the tip

`MutSelftestSummary.md` §8 (side finding): "`kill-rule-check.py --selftest` fails on the landed bytes
(`one-invalid` want/input inconsistency), outside C1's counted surface." My run at 2026-10-26T05:42Z
prints `selftest case=one-invalid got=(2, 0, 1, 1) want=(2, 0, 1, 1) verdict=pass`,
`selftest cases=3 failures=0`, exit 0. Both observations stand for their own timestamps; the tip
passes.

### 7.5 Transient C1/C2 states observed mid-wave (not defects of the tip)

- Harness transient: `RevC2BeforeAfter.md` §5 observed `entries=19 pass=14 exit=1` and
  `selftest cases=4 failures=1` while rule A was being patched; the landed instrument prints
  `entries=20 pass=20 exit=0` and `cases=6 failures=0`.
- Suite transient: `CritOverclaim.md` §2 (findings) observed `selftest cases=9 failures=1` (`R4 … verdict=fail`)
  before the R24 row landed; at 05:40Z and in my run it is `cases=9 failures=0`.
- Capture-binding transient: `FAIL rule=no-row record=S051` / `records=41 bound=40 unbound=1` before
  the registry row landed (`ExecCaptureBindingHarden.md` §3).

### 7.6 Residual `claims.json` literal that no counter can match

`ScoutDatawalk.md` §1: "`PASS F17 ids=S051` is not a grep-able literal: harness prints
`PASS     F17  knowledge/…md ids=S051           exit=0` (`grep -c 'PASS F17 ids=S051'` = 0 at tip)".
Also `RevClaimsFreeze.md` and `ExecRegressionC2.md` note the same literal-spacing deviation. The
harness's own output is the after-value; the claim's ellipsis form is not.

### 7.7 Scope finding from the no-harm seat

`RevNoHarm.md` §D: one `baseline-plain.txt` was written at the **fleet root** during the wave
(author unattributable; content-harm-free, scope violation). The L1 should remove it; it is outside
this seat's write scope.

### 7.8 No-harm numbers (from `RevNoHarm.md`)

`anchorcheck.py SKILL.md` → 12 in-range, 0 bad, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0
OUTSIDE-BASE=0 BASE-ABSENT=0` (all failure classes 0); density mean 201.7 (≥ round-33's 201.7);
`SKILL.md` / `PROVINCE.md` / `LOG.md` untouched this wave. Caveat the seat itself states: the numbers
are in-flight snapshots, and the L1 must re-run `git diff --numstat 014ee2d -- SKILL.md PROVINCE.md
corpus SCORECARD.md LOG.md` at integration.

### 7.9 C1's kill rule is satisfiable without the property it certifies (3 of 5 attack vectors)

`CritC1Kill.md` §Verdict, verbatim in part: "C1's after-predicate **reproduces literally on the
landed bytes** … Nothing in the nine filed defects is still open on the tree I measured.
Falsifying the predicate, **2 of the 5 named vectors are caught** (attack 2 fully; attack 1 for
inert checks and for nine inert checks), **3 leave the kill rule satisfiable without the property it
certifies**": (1c) summary-only suite; (3b) forged verdict guard with a probe-invisible defect;
(4a/4b) fabricated or non-instant `fetched_utc` passing R8 and the instrument; (5) every capture
declared orphan with zero records printing `bound=0 unbound=0`. The seat's own reading: "the gaps do
not falsify the round's stated movement; they do mean C1 must not be cited as a verifiability
*increase* until corrections 1–5 land, and the kill rule should be restated to require exit codes and
per-case lines rather than the bare summary strings." `RevRSuite.md` §5 finds no blocking defect but
records that the R9 limb accepts either `c2-controls/` path (only the wave-dir copy exists) and that
`$LANE_ROOT`-based fixture sourcing is undocumented (fail-closed).

### 7.10 Sentinel scope findings: two FAILs

- `SentScopeFinal.md` §1 **Axis A — FAIL**: "exactly one seat-authored out-of-lane file
  (`baseline-plain.txt`), author and mechanism proven" — content is a pre-fix `capture-binding-check`
  audit capture; my check at 05:47Z: `/home/vgpnk/Projects/shokunin/baseline-plain.txt`, 850 B,
  mtime `02:37`, **still present**. Outside this seat's write scope; the L1 removes it.
- `SentScopeFinal.md` §2 **Axis B — FAIL**: "no git mutation and no seat commit, but four jj
  snapshots plus one receipt that claims none happened" — four seats ran `jj log`/`jj status`
  without `--ignore-working-copy` on the colocated repo (ops recorded; content harm none), and
  `RevErrata.md:12`/`:153` declare "no git/jj mutation", which is false under jj semantics (same
  class as M34-1: overstated cleanliness).
- `CritBoundary.md` §1 corroborates and names the author: "exactly one seat-authored out-of-lane
  write (`baseline-plain.txt`, `RevKillRule`, proven from transcript), plus its in-lane twin
  `selftest-baseline.txt`"; Axis B: "no seat commit/branch/push, nothing staged, but four jj
  working-copy snapshots (2× `jj status`, 2× `jj log`) wrote one commit + `refs/jj/keep` ref + loose
  objects each (43 objects total), and three receipts assert the opposite"; Axis C (siblings,
  shokuknow, bounties) **PASS**; Axis D (scratch) **PASS at snapshot**, with two watch items
  (`ExecRDefectClosureSuite`, `ExecKillRuleCheck`); my check at 05:50Z shows both of those trees
  removed, and only still-running seats' trees under `/fast/scratch/hyaku/kasegi-r34/`.
- `CritC1Kill.md` §Seat hygiene self-reports and corrects the same class: a first write landed at
  `/home/vgpnk/Projects/shokunin/.ufo/waves/round-34/wave1/CritC1Kill.md` (fleet root), was copied
  byte-identically to the lane path and deleted; `ls` on the fleet path now reports absent.

### 7.11 Credential scan clean

`SentCred.md` §Verdict: "**CLEAN.** No credential value, session/cookie/auth value, private URL,
secret-manager reference, e-mail address, phone number, SSH/PGP key, wallet secret, or `.netrc`-style
material in any scanned artifact" — 90 lane artifacts, blocking classes S1/S2 both 0; one INFO flag
(the Immunefi capture carries public login labels and cookie-consent text, no value, no URL).

### 7.12 C2's own mutant matrix: one survivor (anchor ambiguity) and a bounded harness blindness

`MutC2Entry.md` §Mutants: M1 (drop `source:` line) killed; M2 (paraphrase a Q1 quote) killed
(`MISMATCH reason=quote-not-found`); M3a (`anchor: 77` → `12`) killed
(`MISMATCH reason=anchor-broken`); M4 (unregistered `--source S999`) killed. **M3b survived**:
repointing Q9's anchor from 77 to 62 — the identical bullet in the *other* asset-class table —
prints `Q9 OK occurrences=2 anchor=62-ok`, exit 0. The seat's coverage finding: "anchor pins a window,
not the intended occurrence … A guard would need the manifest to pin a distinguishing context line
(e.g. the level heading line), not just the quote's own window." Second finding: "Harness blindness
is bounded by the recheck line's absolute `cd`" — with `--root <scratch lane>` the entry's
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && …` executes against the real lane.
`MutRSuiteChecks.md` (mutant matrix) kills all 18 counter-mutants (9 vacuous checks and 9 deleted checks →
`cases=9 failures=1` / `closed=8/9 exit=1`), corroborating the suite's two-sided selftest.

### 7.13 Instrument bytes drifted during the wave (pin your digests)

Measured by this seat: `corpus/instruments/frontier-recheck-count.py` was `87b14892…` at 05:42Z (the
digest `ExecFrontierBidirectional.md` pins), while `MutC2Entry.md` records `8a79010d…` at session
start and `1be79af6…` after sibling landings ("431 → 433 lines; the diff is the docstring's M33-6/R9
`cited`-set wording … no executable change"). `ExecCensusAfter.md` §1 records further mtimes at
05:46:51Z, 05:47:11Z, 05:48:11Z. Consequence: **every digest in §2 must be re-measured after the L1
commits**; a shape-level digest claim taken mid-wave is not stable. `capture-binding-check.py`
(`3d9e5e0d…`) was stable across my 05:42Z, 05:47Z and 05:53Z reads; `kill-rule-check.py` was
`e33a300f…` at 05:42Z/05:47Z and had moved to `c279d952…` by 05:53Z (table below).

**Tip digests measured by this seat at 2026-10-26T05:53Z** (lane HEAD `206e510`, worktree dirty;
receipt-pinned digests in §2 may name earlier bytes):

| path | sha256 (05:53Z) | matches the receipt pin? |
|---|---|---|
| `corpus/instruments/r-defect-closure.sh` | `8753424c165b5db55a24e54ae2ca5ec84eecf2b1ea52c4c8d9fd174000636ffb` | **no** (`ExecRDefectClosureSuite`/`RevRSuite` pin `0beafed2…`) |
| `corpus/instruments/kill-rule-check.py` | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | **no** (`ExecKillRuleCheck` pins `e33a300f…`) |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` | yes |
| `corpus/instruments/frontier-recheck-count.py` | `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` | no (docstring-only drift per `MutC2Entry.md`) |
| `corpus/instruments/README.md` | `d021b317d2bad47d35d866617962906211df642730bc0f1c3849d4224ac19907` | no (three appends landed) |
| `corpus/source-snapshots/round-34/S051.txt` | `4fd8ed981808b9b9632fd8a4536305e36c82fa98f319bb1cbc7fdb0514b325a5` | yes |
| `corpus/source-snapshots/round-34/manifest.json` | `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe` | yes |
| `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` | `948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a` | yes |
| `corpus/source-snapshots/round-26/manifest.json` | `33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa` | yes |
| `corpus/source-snapshots/round-32/manifest.json` | `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6` | yes |
| `corpus/SOURCES.md` | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` | yes |
| `corpus/README.md` | `876be9cc799751851a93b4177e5c74fd4230bae5e43c555d27dc8bbfe7bf6f29` | yes |
| `corpus/QUALITY.md` | `77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8` | yes (`ExecQualityAppends` `eb20eafc…` was the R22-only state) |
| `SCORECARD.md` | `b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0` | yes |
| `corpus/lessons/round-33.md` | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` | (receipts pin `8d6331fc…` post-R7/R4) |
| `corpus/lessons/round-29.md` | `4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce` | yes |

At these same bytes the counters print `closed=9/9 exit=0`, `survivors=0`,
`records=41 bound=41 unbound=0`, `entries=20 pass=20 exit=0`, and the counts are frontier `17`,
registry rows `51`, S051 rows `1`, knowledge entries `46`, `<LANE_HASH>` in `SCORECARD.md` `0`.

### 7.14 C2's gate is not provenance-sound (fabricated capture would pass every counter)

`CritC2Kill.md` §Verdict: "**C2 holds as declared for the landed tree, and the gate is not
provenance-sound.** Every C2 counter and the `PASS F17 ids=S051` line reproduce at the tip; the
committed S051 capture is byte-identical to two independent live re-captures; the real entry's 17/17
blockquotes and all FC checks hold; the committed twin is rejected when its fabricated quote is
checked against the committed capture (`exit=1`). But the landed checks cannot distinguish a
fabricated capture (construction 1: 17/51/1/1, harness 20/20, source-recheck exit 0,
capture-binding 41/41 exit 0), a fabricated entry body (3a/3b: harness and source-recheck still
pass, anchorcheck sees 0 cites), or an uncited mined row with no source (2: census exit 0,
capture-binding 0). … C2's *evidence* is real this round; its *gate* would not catch the same
construction committed with a self-consistent capture." The round-34 lesson carries the same item as
open item 5 and states C1 is held, not increased (open item 4).

### 7.15 Anchor and literal weaknesses recorded by the round-34 lesson

`corpus/lessons/round-34.md` §Open items (verbatim headings): 7 — "Every assertion occurrences=1"
is false as worded (16 × `occurrences=1`, Q9/Q17 `occurrences=2` with anchors); 8 — "`PASS F17
ids=S051` is not a grep-able literal"; 13 — the 5-line `SOURCES.md` append moves `## Paths` 58→59,
`## Search log` 65→66, `## Leads` 77→79, `## Registry changes` 83→85, deepening the stale
`SOURCES.md:83` citation trail (+7 → +9) without moving cited lines; 16 — one C2 anchor mutant
survives (M3b, §7.12); 12 — the lane stray `selftest-baseline.txt` and the fleet stray
`baseline-plain.txt` must not ride into the integration commit (my check at 06:02Z: the lane file is
absent, the fleet file is still present).

---

## 8. Limits, tooling, artifacts

### 8.1 What this draft does not claim

- No claim that the listed commits exist: nothing is committed at drafting; `<LANE_HASH>` marks the
  L1's integration commit.
- No claim of independence for the receipts it quotes: this seat ran the C1/C2 counters and read the
  seats' evidence, but did not re-derive the mutant matrices, the quota sentences, or the
  `source-recheck` assertions for S051 beyond the run recorded in §3 C2.6.
- The before-column values are from the frozen controls (`c1-controls/before.txt`,
  `c2-controls/before.txt`, `census-before.txt`) as re-derived by `ExecBeforeReceipts.md`
  (PASS, byte-identical after one documented root-path normalization) and by
  `RevC1BeforeAfter.md`/`RevC2BeforeAfter.md`; the numbers printed in §3 are those controls read at
  the freeze commit, not a fresh base run by this seat.
- `PROVINCE.md` F17 append is **not landed**; `SHONEN.md`, `LOG.md`, `SCORECARD.md` round-34 section
  and `corpus/lessons/round-34.md` are not this seat's.

### 8.2 Tooling

No tool installed or upgraded; no package-manager transaction (host-wide pause respected); stdlib
`python3` and coreutils only. Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeReportDraft` deleted
before yielding (verified absent).

### 8.3 Seats absent from the wave directory at drafting (61/65)

Not yet filed at 2026-10-26T06:00Z (list re-checked before yield): `ExecNoHarmFinal`,
`ExecRegressionC1`, `SimplifierCleanup`, `ScribeShonen`. Everything else named in §1–§7 is on disk
and was read; `RevKillRule`, `ScribeLesson` and `ScribeScorecard` landed after the first inventory
and are cited above. Any frozen clause whose only
proof would be one of these is marked in §3 by the receipt name that does exist; where none exists,
the row says so.

### 8.4 Artifacts

- This draft: `.ufo/waves/round-34/wave1/ScribeReportDraft-2.md`.
- Measurement captures (scratch, deleted): `inflight-1.txt` (suite, suite selftest, kill-rule,
  kill-rule selftest), `inflight-2.txt` (capture-binding, selftest, harness, counts, source-recheck,
  digests, sizes), `before-measure.txt`, `before-measure2.txt`, `final.txt` (05:53Z tip digests and counters).
All were removed with the scratch tree before yielding; the figures survive in this file and in the
receipts each row cites.

---

## Report

Seat receipt for `ScribeReportDraft-2` (the section above is the deliverable; this is the evidence).

### Files written by this seat

```
~51.4 KB / 612 lines   .ufo/waves/round-34/wave1/ScribeReportDraft-2.md   (this file; re-read with `wc -lc` / `sha256sum` — the size line cannot carry its own final digest)
```
No product file, no instrument, no manifest, no lesson, no SCORECARD, no LOG, no git/jj mutation, no
write outside the lane. Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeReportDraft` created and removed.

### Commands run by this seat (all read-only; cwd = lane root unless stated)

| # | command | output (tail) | exit |
|---|---|---|---|
| 1 | `git rev-parse HEAD` | `206e5108f1190e61b3e2622d21cab8a5d921650c` | 0 |
| 2 | `ls corpus/instruments/r-defect-closure.sh` (05:31Z, pre-landing) | `No such file or directory` | 2 |
| 3 | `bash corpus/instruments/r-defect-closure.sh` (05:42Z and 05:53Z) | `closed=9/9 exit=0` | 0 |
| 4 | `bash corpus/instruments/r-defect-closure.sh --selftest` | 9 × `selftest case=R# live=pass fixture=rejected verdict=pass`, `selftest cases=9 failures=0` | 0 |
| 5 | `python3 corpus/instruments/kill-rule-check.py` | `mutants=3 killed=3 survivors=0 invalid=0`, `gates=6 failed=0`, `survivors=0` | 0 |
| 6 | `python3 corpus/instruments/kill-rule-check.py --selftest` | `selftest cases=3 failures=0` (incl. `one-invalid got=(2, 0, 1, 1) want=(2, 0, 1, 1) verdict=pass`) | 0 |
| 7 | `python3 corpus/instruments/capture-binding-check.py` | `AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt` / `records=41 bound=41 unbound=0` | 0 |
| 8 | `python3 corpus/instruments/capture-binding-check.py --selftest` | `selftest cases=23 failures=0` (11 cases at base) | 0 |
| 9 | `python3 corpus/instruments/frontier-recheck-count.py` | `PASS F17 … ids=S051 exit=0`; `entries=20 pass=20 exit=0` (`entries=19 pass=19` at base) | 0 |
| 10 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051` | `S051:sha256 OK`, `Q1…Q18 OK`; at base (05:32Z) `manifest UNAVAILABLE reason=missing` | 0 (base: 2) |
| 11 | `grep -c '<LANE_HASH>' SCORECARD.md` | `0` at 05:31Z–06:00Z after a 2-marker read on the HEAD blob (`git show HEAD:SCORECARD.md \| grep -c` → `2`) | 1 (no match) |
| 12 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` / `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `17` / `51` (base: 16 / 50) | 0 |
| 13 | `ls corpus/knowledge/*.md \| wc -l` | `46` (base 45) | 0 |
| 14 | `ls corpus/c2-controls/` | `No such file or directory`; twin exists only at `.ufo/waves/round-34/c2-controls/junk-f17.md` | 2 |
| 15 | `grep -rn 'REFUSE' .ufo/waves/round-34/wave1/*.md` | only sentences about the absence; no seat issues a REFUSE on the twin | 0 |
| 16 | `grep -c 'Direct theft of any user funds' corpus/source-snapshots/round-34/S051.txt` / `grep -c 'five severity levels for smart-contract exploits' …` | `1` / `0` (the twin is a mixed control) | 0 / 1 |
| 17 | `ls -la /home/vgpnk/Projects/shokunin/baseline-plain.txt` | present, 850 B, mtime 02:37 (out-of-lane stray; not removable by this seat) | 0 |
| 18 | `ls -d /fast/scratch/hyaku/kasegi-r34/*/` | only still-running seats' trees remain (5 at 06:03Z); `ExecRDefectClosureSuite`/`ExecKillRuleCheck` trees gone | 0 |
| 19 | `rm -rf -- /fast/scratch/hyaku/kasegi-r34/ScribeReportDraft && test ! -e …` | `scratch_absent=yes` | 0 |

### Digests quoted in this file (re-measured at 05:53Z; see §7.13)

`r-defect-closure.sh` `8753424c…` · `kill-rule-check.py` `c279d952…` · `capture-binding-check.py`
`3d9e5e0d…` · `frontier-recheck-count.py` `1be79af6…` · `round-34/S051.txt` `4fd8ed98…` ·
`round-34/manifest.json` `d5077f81…` · `immunefi-vscs-v2-2-smart-contract-severity.md` `948b202e…` ·
`round-26/manifest.json` `33ac33c3…` · `round-32/manifest.json` `72ab4e68…` · `corpus/SOURCES.md`
`4c85ff86…` · `corpus/README.md` `876be9cc…` · `corpus/QUALITY.md` `77d99df9…` · `SCORECARD.md`
`efa646c8…` (after the round-34 section) · `corpus/lessons/round-33.md` `f69472f3…` ·
`corpus/lessons/round-29.md` `4afb96be…`.

### Tooling

Nothing installed or upgraded; no pacman transaction (host-wide pause); stdlib `python3` and coreutils
only. No network access was used by this seat.

### Limits stated once more

Receipts are the evidence: where a number exists only in a receipt this seat did not re-run, the row
names the receipt. Where a frozen literal and the tree disagree, both are printed (§7). Nothing in
this file is a judgment of the round; the canonical judge resolves §7.1, §7.9 and §7.14.

---

## Report trailer

Report: .ufo/waves/round-34/wave1/ScribeReportDraft-2.md
