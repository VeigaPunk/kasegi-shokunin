# RevReceiptsCanon — round-28 wave-1 receipt-completeness review

Seat: RevReceiptsCanon (reviewer, read-only; no production edit).
Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin (base c9f8b115a098c65356e4b3b6048af45a37ab8395).
Review window: 2026-10-25T17:24Z..17:30Z (UTC). Written at 2026-10-25T17:30Z (UTC).

Scope: map every frozen counter / kill-rule limb / claim condition to the receipt(s) covering it,
name every gap, confirm defect-4 conformance, and audit sha256 + UTC conformance of every receipt.

State at review close: the wave was still settling (instrument digest changed 5 times between
17:24Z and 17:29Z; last observed 95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514).
C1 counters re-run by this seat at 17:29:51Z on 95333e29: bad_fixture_exit=1, BOUNTIES-ABSENT
lines=1, selftest cases=9 failures=0 exit=0, SKILL.md exit=0 LOST-RECORDED=306 bad=0. C2 post-state
measured at ~17:29Z: F12 admitted (awk=12), entries citing S042=1, SOURCES S042 row present
(line 48), census exit 0 (W04 S028/S029 pre-existing only), harness entries=15 pass=15 exit=0,
manifest source-recheck exit 0 on S041 and S042 (12/12 quotes exactly-once), entry recheck line
exits 0 from a foreign cwd.

---

## 1. Frozen counter → receipt map (claims.json C1)

| Condition | Covered by | Verdict |
|---|---|---|
| C1(a) bad-fixture exit → 1 | `receipts/ExecImplC1.txt` (17:29:28Z, at 95333e29: exit=1); `receipts/ExecFixtureRun.txt` (PRE-STATE, exit 0 at c2a9e6c6…); my re-run at 95333e29 | PASS at 95333e29; re-run at close digest required |
| C1(b) bounties BOUNTIES-ABSENT lines → 1 | `receipts/ExecImplC1.txt` (=1); `receipts/ExecFixtureRun.txt` (PRE-STATE =0); my re-run (=1) | PASS at 95333e29 |
| C1(c) --selftest cases=N failures=0 + exit 0 | `receipts/ExecImplC1.txt` (cases=9 failures=0 exit=0); `receipts/ExecInstrSelftest.txt` (PRE-STATE crash, determinism limb to be re-measured post-change); my re-run (cases=9 failures=0 exit=0) | PASS at 95333e29; determinism re-measure at close digest required |
| C1(c) receipt line at the landed sha256 | `receipts/ExecImplC1.txt` (landed_instrument=95333e29…); DRAFT `receipts/ExecReceiptCanonC1.txt` + `wave1/ExecReceiptCanonC1/canonical-block.filled.txt` | **GAP**: canonical `c1-receipt-index.txt` not yet created (L1-only at close) |
| C1(d) SKILL.md no-harm exit 0 / bad=0 / LOST-RECORDED=306 | `receipts/ExecImplC1.txt` (exit 0, 306, bad 0); `receipts/ExecNoHarmC1.txt` (PRE-STATE byte-identical baseline incl. density 150.3/20/652); `receipts/ScribeSkillGate.txt` (verifies on c3629229; warns instrument still moving); my re-run at 95333e29 | PASS at 95333e29; close-digest re-run required |
| C1 kill rule: control reaching after values / non-isolating fixtures | `receipts/ExecFixtureRun.txt` + `.ufo/waves/round-28/c1-controls/*-before.txt` (control clean: 0 / 0 / 0, selftest absent); `receipts/ExecInstrSelftest.txt` (PRE-STATE determinism identical; isolating-fixture limb not runnable before change) | Control clean; fixture-isolation post-change check pending (kills not yet exercised) |
| C1 corpus disclosure (4 files → LOST-RECORDED) | **SUPERSEDED** by L1 `claims-erratum-1.md`: zero backticked anchored bounties cites exist; no verdict-class movement anywhere. `receipts/ExecInstrReadme.txt` CITE-arm probe (0 movement); `receipts/ExecImplC1.txt` (post-arm S042/S041 sweep) | Erratum replaces the frozen annotation; L1 close greps pending |
| Round-27 carry-forward 2 impl notes (FAIL_CLASSES, KASEGI_BOUNTIES, isolating fixtures) | `receipts/ExecImplC1.txt` (details 1-4, all present) | PASS |

## 2. Frozen counter → receipt map (claims.json C2)

| Condition | Covered by | Verdict |
|---|---|---|
| C2 counter 1 frontier_admitted → 12 | `receipts/ExecC2Counters.txt` (PRE-STATE 11); `receipts/ScribeReadmeC2.txt` (F12 row landed at README:213); my re-run (=12) | PASS (post-state) |
| C2 counter 2 entries citing S042 → 1 | `receipts/ExecC2Counters.txt` (PRE-STATE 0); `receipts/ScribeEntryC2.txt` (entry landed, source: S041 + source: S042); my measurement (=1) | PASS |
| C2 counter 3 S042 row → 1 | `receipts/ExecC2Counters.txt` (PRE-STATE 0); `receipts/ScribeRegistryC2.txt` (S042 row line 48, tier A, mined, opened 2026-10-25, used-by exactly entry); my grep (=1) | PASS |
| C2 counter 4 census exit 0 + 42 rows | `receipts/ExecC2Counters.txt` (PRE-STATE exit 0, 41 rows); `receipts/ExecCensusDry.txt` (scratch projection 42 rows); `receipts/ScribeRegistryC2.txt` (post-row); my census run at 17:28Z (exit 0, S042 row present, W04 S028/S029 only) | PASS (post-state) |
| C2 counter 5 harness → 15/15 exit 0 | `receipts/ExecC2Counters.txt` (PRE-STATE 14/14); `receipts/ExecHarnessC2.txt` (mid-wave pre-entry crash on absent entry); my run at 17:28Z (15/15 exit 0) | PASS (post-state) |
| C2 manifest pins + Q9 exactly-once | `receipts/ExecManifest.txt` (landed e62ddad1…, first-build Q1 quote-too-short failure fixed); `receipts/ExecHarnessC2.txt` (independent same defect finding, pre-fix); `receipts/ExecReceiptCanonC2.txt` (Q9 audit 12/12); my source-recheck run (both ids exit 0, 12/12 OK) | PASS |
| C2 entry headers source: S041 + source: S042, recheck ids equal, cwd-independent | `receipts/ScribeEntryC2.txt` (headers, sizes, ids equal); my foreign-cwd run (entry recheck line exit 0) | PASS |
| C2 S041 used-by gains entry, old→new logged | `receipts/ScribeRegistryC2.txt` (removed=1 / added=4 incl. used-by log; R8); SOURCES.md lines 77-79 (old→new logged, verbatim) | PASS |
| C2 S042 used-by exactly the entry | `receipts/ScribeRegistryC2.txt` (S042 used-by cell); census E11 satisfier | PASS |
| C2 assimilation Gate ≥1 admit + ≥1 reject, ≤25-word inline quotes | `receipts/ScoutAssimilation.txt` §7 (admit F12; reject staged S044/S045/S046 with 2 inline …23-word quotes); `wave1/ScoutAssimilation.md` | PASS |
| C2 R14 lands + practiced in-round | `receipts/ScribeR14.txt` (R14 appended at QUALITY.md:83; 6 insertions/0 deletions; R6 byte-identical first 77 lines; practice snapshot 53 files/892 KiB at 17:23Z) | PASS |
| C2 kill rules (adopt-without-entry, census≠0, harness<entries, id mismatch, anchor-broken) | `receipts/ScribeReadmeC2.txt` + `receipts/ScribeRegistryC2.txt` + `receipts/ScribeEntryC2.txt` + `receipts/ExecReceiptCanonC2.txt` (all risk limbs named; anchor-broken limb not exercised) | No kill observed; anchor-broken limb unexercised |
| C2 do-nothing control | `receipts/ExecC2Counters.txt` + `.ufo/waves/round-28/c2-controls/before.txt` (11/0/41/14-14) | Control clean |

## 3. Dispatch requirements

| Requirement | Covered by | Verdict |
|---|---|---|
| Reviewer seats inside build wave (r26 defect 2) | wave1/Rev*.md present: RevCloseCheck, RevCounters1, RevCounters2 (inside wave), RevReceiptsCanon (this file); seats RevDensityGuard, RevEntryC2, RevFixturesC1, RevImplC1, RevManifestC2, RevNoHarmC1, RevengerC1/C2 still in flight | Partial; pending seats are runnable gaps |
| Inline ≤25-word Gate quotes in the round lesson (r26 defect 3) | `receipts/ScoutAssimilation.txt` §7 (quotes exist, ≤25 words) | Lesson not yet landed — quote placement in lesson unverifiable until ScribeLesson lands |
| One canonical receipt index at landed digest; no mid-wave canonical artifacts (r26 defect 4) | `assemble-receipts.py` (L1-only emitter); drafts under wave1/ExecReceiptCanonC1/ (template + filled block) and `receipts/ExecReceiptCanonC1.txt`/`ExecReceiptCanonC2.txt` | CONFORMANT at review time: no `c1-receipt-index.txt` or canonical file exists under `.ufo/waves/round-28/` (verified by find at 17:27Z and 17:29Z) |
| Round-27 carried defects (fleet report before returning; expected-list basis) | `receipts/ExecExpectedList.txt` (39 knowledge .md, expected-list 39/41, basis reconciled); ScribeReportDigest.md present | PASS |

## 4. sha256 + UTC conformance audit (every receipt)

All 27 `receipts/*` carry ≥1 64-hex sha256 and a 2026-10-25 date line. Deviations:
- `ExecCensusDry.txt`, `ExecManifest.txt`, `ScribeReadmeC2.txt`: date-only "2026-10-25 (UTC)", no HH:MM UTC stamp (minor conformance gap).
- `ExecFixtureRun.txt`, `ExecHarnessC2.txt`, `ExecNoHarmC1.txt`, `ExecInstrSelftest.txt`, `ExecScorecard.txt`, `ScribeSkillGate.txt`, `ScoutAssimilation.txt` (`ScribeFrontierNote.txt` uses full `2026-10-25T17:25:48Z`): minute-granularity UTC stamps only. Acceptable but weaker than the full-second stamps carried by ExecImplC1 (17:29:28Z), ExecC2Counters (17:21:57Z), ExecCaptureS041/S042 (17:22:12Z/17:22:03Z), ScribeR14 (17:23:03Z), ExecRecheckAuditR28 (17:25:38Z), ScribeLog (17:24:28Z).
- Control receipts `.ufo/waves/round-28/c1-controls/*-before.txt`, `c2-controls/before.txt`, `census-before.txt`: no embedded UTC stamp (they are claims-freeze artifacts; byte-conformance is pinned against them by ExecImplC1/ExecNoHarmC1/ExecC2Counters).
- `ScoutAssimilation.txt`: 0 sha256 lines and only date-level UTC (pure command-transcript receipt; no instrument digest recorded). Flagged as the one receipt with no digest coverage at all.

## 5. Named gaps (unlanded / unrun at 17:30Z — an unrun check has not passed)

1. **Canonical `c1-receipt-index.txt`** — L1-only at close, at the landed digest; grep must see exactly 1 `selftest cases=` and exactly 1 `instrument_sha256=` equal to `sha256sum corpus/instruments/anchorcheck.py` (drafts exist in `receipts/ExecReceiptCanonC1.txt` and `wave1/ExecReceiptCanonC1/canonical-block.filled.txt`).
2. **`corpus/lessons/round-28.md`** — absent; ScribeLesson has no receipt/report yet. It must carry the Gate admit/reject quotes and the S041 old→new log (mandated by C2 predicate).
3. **Instrument digest still moving** — last landed 95333e29… at 17:29:28Z; ScribeSkillGate observed 5 digests in ~100 s (c2a9e6c6 → 5f5f725c → e14f75b8 → c79fb7ca → 29aba084 → c3629229 → 95333e29). Every C1 PASS above is at 95333e29; **re-run all C1 counters and selftest determinism at the final committed digest** (ExecImplC1 §7 rerun; ExecInstrSelftest post-change rerun command).
4. **27 dispatched seats had no artifact at 17:29:30Z**: CritC1Kill, CritC1Vacuity, CritC2Admission, CritC2Kill, CritGlobal, ExecScopeSweep, MutArmC1, MutExitC1, MutQuoteC2, MutSelftestC1, RevDensityGuard, RevEntryC2, RevFixturesC1, RevImplC1, RevManifestC2, RevNoHarmC1, RevReceiptsCanon (this file, written now), RevengerC1, RevengerC2, ScoutDatawalk, ScoutGateRegistry, ScoutJpcertRecon, ScribeLesson, ScribeReceiptsC2, SentinelQuality, SentinelScope, SimplBloat. (ExecGateLog/ExecSkillGateSupport/ScribeEntryC2/ScribeSkillGate/ExecImplC1 landed during the review.) Partial scratch dirs exist for MutArmC1/MutExitC1/MutSelftestC1/CritC1Vacuity/RevNoHarmC1/RevengerC1 — those seats were mid-run, not silent.
5. **Kill-rule limbs not exercised post-change**: selftest fixture isolation (limb isolation proof) and manifest anchor-broken (Q9 rejection) counters have no post-change receipt yet.
6. **Corpus-disclosure receipts**: `claims-erratum-1.md` supersedes C1's frozen annotation (0 anchored bounties cites, 0 movement); L1's close-time grep receipts for the 4 named files are not yet in `receipts/`.

## 6. Residual risk / verification gaps

- Timing hazard: multiple receipts were written mid-wave and honestly label themselves PRE-STATE (ExecFixtureRun, ExecNoHarmC1, ExecInstrSelftest, ExecC2Counters, ScribeLog, ScribeScorecard, ScribeCensusNote, ExecRecheckAuditR28). Their after-values must be superseded by close-time L1 re-runs; none of them asserts a pass.
- `ExecRecheckAuditR28.txt` lists `anchorcheck.py 2f707046…` while calling it "the pre-change round-27 byte (c2a9e6c6…)"; the digests disagree. Flagged as an internal inconsistency to reconcile (the anchorcheck hash should be c2a9e6c6… at 17:25:38Z, or the line is a mid-write byte).
- `ScribeFrontierNote.txt` cites base `261a6651…`; `claims.json` records the same revision as the "base" field under `frozen_by` (the official lane base is c9f8b115…). Not a freeze defect, but the seat used the claims.json `base` field rather than the dispatch base.
- E11 ordering was observed and exercised (census exit 1 when entry absent); the post-entry census exit 0 was verified by this seat at 17:28Z and by ExecReceiptCanonC2 at 17:27Z.

## 7. What the L1 must re-run at close (exact commands)

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo bad_fixture_exit=$?
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo selftest_exit=$?   # run twice; diff outputs
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo skill_exit=$?
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
python3 .ufo/waves/round-28/assemble-receipts.py   # L1 emitters the ONE canonical c1-receipt-index.txt at the landed digest
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt
grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt
# C2:
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
python3 corpus/instruments/frontier-recheck-count.py
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
```
