# Round 33 report body — DRAFT for the L1 (not the filed report)

Seat: `ScribeReportDraft` (scribe, leaf; this file is its receipt). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; write scope exercised: this path only.
Answering model: session route, no model passed by this seat (project context reports
`opencode-go/deepseek-v4.1-flash`). Tools installed/upgraded: none. Scratch: none created (all
inputs are lane files or committed bytes; no clone/fixture). No git/jj mutation; read-only git
(`log`/`rev-parse`/`status`/`diff`/`rev-list`) only. No fetch, no live target contacted.

Commit naming used throughout: base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze
`6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; dispatcher-ready + Rule-B erratum `53bfa59ff3fa578818e7e5db04fe60e80ed1eb6f`;
wave-1 integration `9f9848816503aa0cd566fc2efdc5e69ea501a253` (lane tip and `origin/master` at
drafting: `git rev-list --left-right --count origin/master...master` → `0 0`). The L1's LOG entry,
the SCORECARD/SHONEN/lesson commits and the closing commit are `<LANE_HASH>` markers below.

Drafting state: `wave1/*.md` = **64 receipt files of 64 expected seats** at 02:00 -03 (count
command `ls .ufo/waves/round-33/wave1/*.md | wc -l`; this file included). `CritMistakes.md` was the
last to land (02:00), after `ExecWaveEvidencePack.md`'s 04:50:13Z census had named nine absent
seats — that census is a point-in-time measurement of a trickling directory, not a missing-seat
verdict, and every seat it listed has since filed.

---

## Work performed

Opens: the round targets **C1 `depth:verifiability`** (score 4 — the lane's lowest non-retired
axis, `claims.json` `lowest_non_retired_axis`) and **C2 `coverage`** (7). `depth:density` (9) is
not claimed; it is measured only as no-harm.

**C1 — capture-manifest binding.**
- New instrument `corpus/instruments/capture-binding-check.py` (492 lines, sha256
  `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`, stdlib only) implementing
  rules A/B/C of the frozen interface contract under the per-id reading of
  `.ufo/waves/round-33/claims-erratum-1.md`; 11 selftest fixtures, four named counter mutants.
  Evidence: `wave1/ExecCaptureBinding.md` §1–§7; raw dumps `wave1/ExecCaptureBinding/`.
- Legacy manifest upgrade: 38 records across eight manifests gain `url` (byte-exact own-row token),
  `"archival": true` and `archival_note`; `git diff -U0` = 114 insertions, **0** deletion lines;
  independent re-verify `records 38 violations 0`. Evidence: `wave1/ExecManifestUpgrade.md` §3–§6.
- Round-32 manifest created (5,753 B, sha256 `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774`)
  with `url` + `fetched_utc 2026-10-25T23:14:00-03:00` and no `archival` key; 14 assertions all
  `occurrences=1`; credential-marker grep empty. Evidence: `wave1/ExecManifest32.md` §1–§4.
- Final C1 gate run on quiescent bytes, nine gates, one deviation disclosed. Evidence:
  `wave1/ExecRegressionC1.md` §1–§2 (raws `wave1/ExecRegressionC1/`).
- Independent C1 before→after re-derivation: verdict **matches**. Evidence:
  `wave1/RevC1BeforeAfter.md` §6.
- Instrument review: 12/12 probes, a wrong-row false-pass fixture (T8) rejected, erratum
  implementation confirmed load-bearing. Evidence: `wave1/RevC1Instrument.md` §1–§2.
- Rule-B hazard found at base before any seat scored (S029/S006 URLs carried by two registry rows
  each) → L1 erratum 1, filed at `53bfa59`: `claims-erratum-1.md`; detection receipts
  `wave1/ScoutManifestAudit.md` §4, `wave1/ScoutDatawalk.md` §4.
- Attack review of the kill rule: fake rejected, eight blind spots measured (H1–H8).
  Evidence: `wave1/CritC1Kill.md`; carried in `SCORECARD.md:1009-1019`.

**C2 — F16 admission.**
- Entry `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (306 lines, 24,539 B,
  sha256 `1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1`), header `ground: F16`,
  `source: S049` + `source: S050`, one `recheck:` line with its own `cd … &&` prefix. Evidence:
  `wave1/ExecEntryF16.md`.
- Registry rows S049/S050 appended (dataset 48 → 50 rows, tier A 45 → 47, mined 36 → 38; six added
  lines, zero modified). Evidence: `wave1/ExecRegistryAppend.md` §2–§6.
- Frontier row F16 + coverage-map row appended to `corpus/README.md` (26 insertions, 0 deletions).
  Evidence: `wave1/ScribeReadmeF16.md` §3–§4.
- `knowledge-expected.txt` +1 entry (44 → 45). Evidence: `wave1/ExecExpectedList.md`.
- Final C2 counter run, nine frozen commands on quiescent bytes: all met. Evidence:
  `wave1/ExecHarnessC2.md` §1 (incl. the foreign-cwd run §2).
- Census after-state and the six contract census commands with the before-diff. Evidence:
  `wave1/ExecCensusAfter.md` §1–§2.
- Non-author reviewer: Q1–Q10 all `pass`, verdict ADMIT. Evidence: `wave1/RevEntryF16.md` §1.
  Row reviewers: `ADMIT-ROW` for both rows, all six contract rules conformant
  (`wave1/RevRowS049.md`, `wave1/RevRowS050.md`).
- Quote sweep: all 14 manifest pins resolve, 0 failures (`wave1/RevQuoteSweep.md`); Chinese-accuracy
  review of the final entry with six minor findings F1–F6 (`wave1/RevTranslation.md` §Findings).
- Expansion attack: verdict **`partial`** — overlap with F13 named, residual named
  (`wave1/CritExpansion.md` §5); adversarial kill-rule critique (`wave1/CritC2Kill.md`).

**Frontier items.**
- Assimilation theme (CNVD 众测 helpList + 360SRC rules): 2 admits by document, 7 staged-entry
  refusals with flip conditions, 18 id collisions (S031–S048) recorded, guard proof committed in
  `.ufo/waves/round-33/assimilation/`. Evidence: `wave1/ScoutPackageThemes.md`,
  `wave1/ScribeLesson.md`, `corpus/lessons/round-33.md` §Gate.
- Quarantine slice (7 register rows re-derived byte-identically): 0 adopted, 2 refused with exact
  splice reasons, 5 `unreachable`. Evidence: `wave1/ExecQuarantine.md` §1–§6; D6's S037 verdict is
  recorded there and in the lesson.
- considerthese 2026-10-25 proposal 1 (wave-evidence growth): measured, see below. Evidence:
  `wave1/ExecGrowthMeasurement.md`.
- M33-1/M33-2 closures (round-32 manifest; committed watchdog digest) with red-before/green-after
  closure checks: `wave1/ExecErratumCheck.md` §2–§5.
- Routed round-32 defects: D1 LOG entry appended at freeze (`LOG.md:1593`, +4 lines, 0 deletions;
  `ExecErratumCheck.md` §3); D2 frontier step run (lesson + mistakes + census-after);
  D3 cross-domain line (below, §"Cross-domain evidence"); D4 committed digest
  `.ufo/waves/round-33/watchdog-digest.txt` (3 lines, all three compared equal to the fleet log);
  D5 inside C1; D6 quarantine verdict above.

**Scribes (append-only surfaces).** `corpus/QUALITY.md` R20/R21 (`wave1/ScribeQuality.md`),
`corpus/instruments/README.md` round-33 section (`wave1/ScribeInstrReadme.md`), `SKILL.md` R6
append (`wave1/ScribeSkillGate.md`), `PROVINCE.md` F16 line (`wave1/ScribeProvince.md`),
`corpus/README.md` (`ScribeReadmeF16.md`), `corpus/SOURCES.md` Search log (`wave1/ScribeSearchLog.md`),
`SCORECARD.md` round-33 section + capability row (`wave1/ScribeScorecard.md`), `SHONEN.md` evidence
refresh (`wave1/ScribeShonen.md`), lesson `corpus/lessons/round-33.md` (`wave1/ScribeLesson.md`).

**Verification and cleanup seats.** Gate spot-check: **agree** on all four sampled items and one
minor prose finding (`wave1/RevGateSpot.md` §Verdicts, Findings 1). Mistake-mining attack: item 1
sound and reproducible for the three named cases but incomplete for the capture-existence limb, and
item 2 shows the lesson's own sweep block and absence list are not reproducible
(`wave1/CritMistakes.md` §1, §2.3–§2.4). Dedup/cleanup scan: no file over 1 MB, one duplicate
evidence group (9 copies), two empty committed files, one citable `/tmp` path
(`wave1/SimplifierCleanup.md` §1–§5).

**Conformance and hygiene.** Before-receipt reproducibility: both frozen control files reproduced
byte-identically from a `git archive` of the freeze commit, fake checker rejected
(`wave1/ExecBeforeReceipts.md` §C1–§C2). Determinism: counter runs byte-identical twice
(`wave1/ExecDeterminism.md`). Foreign cwd: entry recheck, binding checker and recheck-audit all
exit 0 from `/` and `/tmp` (`wave1/ExecForeignCwd.md`). Scratch discipline: 0 of 55 landed seats
left a tree on disk (`wave1/ExecScratchDiscipline.md` §1). Evidence index: 55 receipts, 0
zero-byte, 0 duplicate digests, 811,563 B (`wave1/ExecWaveEvidencePack.md` §3A). Scope/credential
sentinels: no credential material in any new file, no misroot (`wave1/SentCred.md`,
`wave1/SentScopeFinal.md` F3/F4). Connectors: predicate-structure check (`wave1/ConnClaims.md`),
ownership/cycle check (`wave1/ConnOwnership.md`), sibling overlap (`wave1/ConnSibling.md`).
Census dry-run mirror before the registry write: PASS (`wave1/ExecCensusDry.md`).

---

## Landed changes

Each row ties the change to its proving receipt. Commits are the L1's; `<LANE_HASH>` marks a commit
that did not exist at drafting time (LOG entry, closing commit).

| # | Change (path) | Commit | Measured diff | Proving receipt |
|---|---|---|---|---|
| 1 | `corpus/instruments/capture-binding-check.py` (new) | `9f98488` | new file, 492 lines, sha256 `b4182665…b7f9` | `ExecCaptureBinding.md`; `ExecRegressionC1.md` §2.1 |
| 2 | 8 legacy `corpus/source-snapshots/round-{23,24,25,26,28,29,30,31}/manifest.json` | `9f98488` | `114 insertions(+)`, 0 deletion lines | `ExecManifestUpgrade.md` §5–§6 |
| 3 | `corpus/source-snapshots/round-32/manifest.json` (new) | `9f98488` | 5,753 B; 2 records, `url`+`fetched_utc`, no `archival` | `ExecManifest32.md` §1 |
| 4 | `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (new) | `9f98488` | 306 lines, 24,539 B, sha256 `1f7ac0a2…71d1` | `ExecEntryF16.md`; `RevTranslation.md` header |
| 5 | `corpus/SOURCES.md` rows S049/S050 + Search-log bullet + 3 R8 lines | `9f98488` | `6 added / 0 removed`; 48 → 50 rows | `ExecRegistryAppend.md` §2, §5, §9 |
| 6 | `corpus/README.md` F16 frontier + coverage-map rows | `9f98488` | `26 0`; one hunk `@@ -316,0 +317,26 @@` | `ScribeReadmeF16.md` §3–§4 |
| 7 | `corpus/instruments/knowledge-expected.txt` | `9f98488` | `1 0`; 44 → 45 entries | `ExecExpectedList.md`; `ExecRegressionC1.md` §2.5 |
| 8 | `corpus/QUALITY.md` R20/R21 | `9f98488` | `55 0`; rows at `:169-170` | `ScribeQuality.md`; `SCORECARD.md` (R20/R21 citations) |
| 9 | `corpus/instruments/README.md` round-33 section | `9f98488` | `145 0` | `ScribeInstrReadme.md` |
| 10 | `SKILL.md` R6 append | `9f98488` | `19 0` (`git diff --numstat 690b69da HEAD -- SKILL.md`) | `ScribeSkillGate.md` |
| 11 | `PROVINCE.md` Frontier F16 line | `9f98488` | `2 0` | `ScribeProvince.md` §5 |
| 12 | `SCORECARD.md` round-33 section + `## Round-33 capabilities` | `<LANE_HASH>` (worktree at drafting) | section at `:982`, capability row at `:1074` | `ScribeScorecard.md` |
| 13 | `SHONEN.md` four evidence lines (same-line only, 42 lines before/after) | `<LANE_HASH>` | `31 31`, 0 `[x]` | `ScribeShonen.md` §3–§4 |
| 14 | `corpus/lessons/round-33.md` (new) | `<LANE_HASH>` | header/gate/mistakes/census/no-harm/open items | `ScribeLesson.md`; file §Gate |
| 15 | `LOG.md` round-33 entry | `<LANE_HASH>` (L1 owns LOG.md) | not present at drafting (`grep -c '^## Round 33' LOG.md` → 0) | — (L1) |
| 16 | receipts + evidence dumps under `.ufo/waves/round-33/wave1/` | `<LANE_HASH>` | 64 `*.md` + 4 seat evidence dirs at drafting | `ExecWaveEvidencePack.md` §3A–§3D |
| 17 | `.ufo/waves/round-33/claims-erratum-1.md` | `53bfa59` | Rule-B per-id binding ruling | `ScoutManifestAudit.md` §4; `ExecCaptureBinding.md` §1 |
| 18 | `.ufo/waves/round-33/` planner files, ready marker, `l1-ref/sid-url.tsv` | `53bfa59`, `a6a5023` | 64-seat spec/dispatch | `wave1-spec.json`; `wave1.ready` |

Append-only integrity of every owned scribe surface, measured by `SentScopeFinal.md` §6:
`PROVINCE.md 2 0`, `SKILL.md 43 0` (its reading), `QUALITY.md 55 0`, `README.md 26 0`,
`SOURCES.md 6 0`, `instruments/README.md 139 0`, `knowledge-expected.txt 1 0`, eight manifests
additions-only. **Conflict, stated rather than smoothed:** `SentScopeFinal.md` §6 reports
`SKILL.md 43 0`; this seat measures `git diff --numstat 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 HEAD -- SKILL.md`
→ `19 0`. Both are reported; `ScribeShonen.md` §2.1 and `ExecRegressionC1.md` §2.10 agree on `19 0`.

---

## Before → after measurements

All "after" values are copy-runs on quiescent bytes, measured at the worktree that became
`9f98488`; each receipt states its own quiescence probe. "Commit measured" = the commit whose bytes
the counter read.

### C1 — `depth:verifiability` (4 → held 4)

| # | Counting command (verbatim from `claims.json`) | Before (base/freeze bytes) | After (landed bytes) | Commit measured |
|---|---|---|---|---|
| 1 | `python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"` | instrument absent: `ls_exit=2` (`c1-controls/before.txt`); real checker on base bytes `records=38 bound=0 unbound=38`, `bind_base_exit=1` (`ExecRegressionC1.md` §2.4) | `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2`, `records=40 bound=40 unbound=0`, `run1_exit=0 run2_exit=0`, stdout sha256 `1861fec8…a3c5a9f1` twice | `9f98488` bytes |
| 2 | `python3 corpus/instruments/capture-binding-check.py --selftest; echo "selftest_exit=$?"` | n/a (absent) | `selftest cases=11 failures=0`, `selftest_exit=0`; the six contract-named cases plus five controls | `9f98488` bytes |
| 3 | the per-manifest audit one-liner | `TOTAL records=38 with_url=0 with_fetched_utc=0` | per-dir `url_bound` = records for all nine dirs; `round-32 records=2 url_bound=2 fetched=2 archival=0` | `9f98488` bytes (`ExecErratumCheck.md` §0/§5) |
| 4 | independent second implementation | — | `TOTAL records=40 bound=40 fetched=2 archival=38`; `registry_rows=50`; two cross-id URL pairs = `multi_row_url=2` | `9f98488` bytes (`ExecRegressionC1.md` §2.11) |
| 5 | fake-checker control (`c1-controls/fake-checker.py`) | fake prints `records=38 bound=38 unbound=0` exit 0 on bytes with `with_url=0` | fake prints the same summary on final bytes (`records=40 bound=40 unbound=0`, `cases=0`) → **rejected** because it cannot fail | `9f98488` bytes (`ExecRegressionC1.md` §2.3) |
| 6 | before→after re-derivation | all five frozen before values re-derived on base bytes: **matches** | — | `690b69da` archive (`RevC1BeforeAfter.md` §6) |

Rule-C detail after the landing: the 38 pre-round-32 records carry `archival: true`
(`with_archival=38`) and the two round-32 records carry `fetched_utc` with no archival key
(`ExecRegressionC1.md` §2.1, §2.11).

**Scope of what this proves (stated, because it bounds the held score):** `bound=40` certifies
manifest↔registry *metadata* binding, not capture↔manifest binding. A round-32 tree with its
captures deleted passes (`captures=none`), and a capture rewritten to 18 bytes still passes
(`bound=2 unbound=0`), measured on scratch mutants (`CritMistakes.md` §1.1, §3). The byte-level
evidence is the separate committed `source-recheck.py` run — 40 `:sha256 OK` pins, exit 0, and its
mutants caught with `MISMATCH`/`stem-mismatch`/`UNAVAILABLE` (`CritC1Kill.md`; `SCORECARD.md:1009-1019`)
— so C1's `held 4` rests on the pair, and QUALITY R20's second clause is runnable only through
`source-recheck.py`. `ExecCaptureBinding.md` §8 proposes a rule D (path exists + sha256 matches) as
a contract widening the L1 has not taken; `CritMistakes.md` §4 item 2 repeats the ask.

### C2 — `coverage` (7 → held 7)

| # | Counting command | Before | After | Commit measured |
|---|---|---|---|---|
| 1 | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | `15` | `16` | `9f98488` (`ExecHarnessC2.md` §1 / C2.[1]) |
| 2 | `grep -lE '^source: S049 ' corpus/knowledge/*.md \| wc -l` (and S050) | `S049=0 S050=0` | `S049=1 S050=1` | `9f98488` (C2.[2]) |
| 3 | `grep -cE '^\|[[:space:]]*S049[[:space:]]*\|' corpus/SOURCES.md` (and S050; total: `S[0-9]{3,}`) | `0 / 0 / 48` | `1 / 1 / 50` | `9f98488` (C2.[3]–[5]) |
| 4 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | exit 0, `W04 S028` + `W04 S029` + `ok` | exit 0, **byte-identical three lines**, no E, no new W | `9f98488` (C2.[6]; `ExecCensusAfter.md` §1) |
| 5 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=18 pass=18 exit=0` | `entries=19 pass=19 exit=0` with `PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050` | `9f98488` (C2.[7]) |
| 6 | `source-recheck.py --manifest …round-32/manifest.json --source S049` (and S050) | `manifest UNAVAILABLE reason=missing`, exit 2 | `S049:sha256 OK` + `Q1`–`Q8` `OK occurrences=1`, `recheck49_exit=0`; S050 `sha256 OK` + `Q1`–`Q6`, `recheck50_exit=0` | `9f98488` (C2.[8]/[9]) |
| 7 | six contract census commands | `rows=48`, `tier=A=45 B=1 C=2`, `status=mined=36 queued=9 rejected=3`, malformed 0, dups empty, enum 0, missing-used-by 0 (`census-before.txt`) | `rows=50`, `tier=A=47 B=1 C=2`, `status=mined=38 queued=9 rejected=3`, malformed 0, dups empty, enum 0, missing-used-by 0 | `9f98488` (`ExecCensusAfter.md` §2) |
| 8 | knowledge-entry audit | 44 files, `strict pass=44/44` | 45 files, `strict pass=45/45`, `expect=present expected=45 missing=0 unexpected=0`, `recheck_exit=0` | `9f98488` (`ExecRegressionC1.md` §2.5) |

### No-harm (unowned axis, `depth:density` 9)

| Metric | Before | After | Evidence |
|---|---|---|---|
| `density.py SKILL.md` mean | `191.5`, 24 blocks, 689 cites | `201.7`, 25 blocks, 710 cites, `density_exit=0` | `ExecRegressionC1.md` §2.9; `ExecNoHarmFinal.md` §3 |
| `anchorcheck.py SKILL.md` | 7 in-range, 0 bad, `LOST-RECORDED=306 PIN-BROKEN=0` | 12 in-range, 0 bad, same failure classes, `anchor_exit=0` | `ExecRegressionC1.md` §2.8; `ExecNoHarmFinal.md` §4 |
| `git diff 690b69da -- SKILL.md PROVINCE.md` | — | `19 0` / `2 0`, 0 deletion lines | `ExecRegressionC1.md` §2.10 |

### Considerthese proposal 1 — committed wave-evidence growth (R14)

Command: `git -C . diff --stat <base> <rev> -- .ufo/waves/round-33`, `… --numstat … | awk '{s+=$1}'`,
`git -C . ls-tree -r -l <rev> -- .ufo/waves/round-33 | awk '{s+=$4}'`.
At the integration byte: **132 files, 17,170 insertions, 1,366,042 B** = 27.3 % of a 5 MB budget,
0 corpus copies, 0 scratch trees (`ExecGrowthMeasurement.md` §1–§4). This is a **lower bound** for
the round: it was measured at `9f98488`, before the SCORECARD, SHONEN, lesson and index receipts.
The counter's own controls are in §0 of that receipt (untracked file invisible to `diff`; an
untouched wave dir counts 0).

---

## Sources & frontier

Counting command: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`.

- **Rows before → after: 48 → 50** (`ExecHarnessC2.md` C2.[5]; `ExecRegistryAppend.md` §6).
- **Rows added by tier:** 2 × tier A (S049 CNVD 帮助页; S050 360SRC 外部漏洞处理和评分标准 V2.0);
  tier histogram `A=45 B=1 C=2` → `A=47 B=1 C=2`. Status histogram `mined=36 queued=9 rejected=3`
  → `mined=38 queued=9 rejected=3` (`ExecCensusAfter.md` §2).
- **Rows touched old → new:** **none** — no existing row's status/recheck/used-by cell changed;
  the append is the R8 record (`S001–S048 untouched (logged)`, `ExecRegistryAppend.md` §5).
  Staged→landed cell changes are recorded on the new rows only: S049 staged `opened 2026-10-23` →
  `2026-10-26`; S050 staged `kind spec` → `docs` and `opened 2026-10-23` → `2026-10-26` (same §5).
- **Known line-number displacement (R6 disclosure):** the two rows shift `## Paths` 56 → 58,
  `## Search log` 63 → 65, the round-31 sweep bullet 72 → 74, `## Leads (unopened)` 74 → 77,
  `## Registry changes` 80 → 83, the S043 change-cell line 87 → 90. This deepens the already-routed
  M31-3 staleness of two `corpus/lessons/round-29*` citations; the fix belongs to the lesson owner
  (`ExecRegistryAppend.md` §8).
- **Frontier:** F16 admitted, `15 → 16` admitted rows; the README records the frontier as
  **16/16** in its `[r33 amendment]` paragraph while leaving the round-26 "11/11" prose as history
  (`ScribeReadmeF16.md` §3–§4; `PROVINCE.md` F16 line).
- **Coverage map:** one appended row for the F16 entry; no in-place edit (R6).

---

## Trend verdicts

- **expansion — improved.** Frontier 15 → 16, registry 48 → 50, knowledge entries 44 → 45, all on
  first-party platform documents. Caveats carried, not smoothed: the expansion attack verdict is
  **`partial`** (overlap with F13's reward-ladder ground named, residual named —
  `CritExpansion.md` §5), and `CritC2Kill.md` §5 shows a restatement-shaped entry still passes every
  C2 counter but the reviewer clause.
- **quality — improved.** The new entry passes Q1–Q10 under a non-author reviewer
  (`RevEntryF16.md` §1) with 14 manifest-bound quotes at `occurrences=1` (`RevQuoteSweep.md`);
  `recheck-audit` strict pass 44/44 → 45/45 and `expect … expected=45 missing=0`; QUALITY gains R20
  and R21, both grounded in this round's D5/M33-1 (`ScribeQuality.md`; `corpus/QUALITY.md:169-170`).
  Open against it: `RevTranslation.md` F1 — the S049 question title is transcribed as
  `漏洞提交时…` where the capture reads `提交漏洞时…` (entry L3/L48), plus F2–F6, all minor and none
  touching a manifest-bound string or a number.
- **discernment — improved.** Gate met with more refusals than admits: 2 admits by document vs 7
  staged-entry refusals with explicit flip conditions (`ScribeLesson.md`; `ScoutPackageThemes.md`),
  and 0 adopted / 2 refused / 5 unreachable on the quarantine slice with the exact splice reasons
  (`ExecQuarantine.md` §5). The lane-dispatched gate spot-check agrees on all four sampled items —
  quotes vs a fresh fetch, staged→manifest→landed-row byte equality, the refusal/quarantine
  criteria, and the R20/R21 row citations (`RevGateSpot.md` §Verdicts, lines 20–23). Bounded by:
  no non-author verifier sits on the lane this round (this spot-check is a lane seat, so its
  verdict is `lane-seat`, not independent); `SCORECARD.md` carried no round-32 section for
  calibration (`RevCalibration.md`); and the sample found the lesson's Gate quote lengths misstated
  (finding 9).

---

## SHONEN

One line per box, from `ScribeShonen.md` §3 (all four stay `[~]`; no `[x]` introduced):

- **Box 1 — SKILL.md decision tables/citations:** `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`, 1090 lines, append-only `19 0`; density `201.7` / 25 blocks / 710 cites vs `191.5` / 24 / 689; `anchorcheck` 12 in-range, 0 bad, `PIN-BROKEN=0`.
- **Box 2 — end-to-end task in LOG.md:** newest entry is `## Round 32` at `:1593` (honest stop); no round-33 LOG entry exists at drafting, so the round-33 end-to-end measurement is receipt-only (`ExecRegressionC1.md` §2.1/§2.2) and the box stays `[~]`.
- **Box 3 — instructions executable without oral context:** 45 entries each with one `recheck:`; `strict pass=45/45`, `expected=45 missing=0 unexpected=0`; harness `entries=19 pass=19` with `PASS F16 ids=S049,S050`; S049/S050 source-recheck exit 0 (`recheck49/50_exit=0`).
- **Box 4 — no cross-domain bleed:** `PROVINCE.md` gained only the F16 EOF amendment (`2 0`, 74 lines, sha256 `b57de5d9…abd679`); six-lane sibling sweep `scoped-terms=0` and F16 sits inside kasegi's province (`ConnSibling.md` §1/§3/§4).

---

## Stale-lane

Lane tip `9f9848816503aa0cd566fc2efdc5e69ea501a253` = `origin/master`; `git rev-list --left-right --count origin/master...master` → `0 0`, so the lane is **not** behind or ahead of its remote.
It is **not closed**: at 02:00 -03 `git status --porcelain` shows 18 paths (19 files with
`-uall`) — `SCORECARD.md`, `SHONEN.md`, `corpus/lessons/round-33.md`, two re-edited receipts
(`ExecDeterminism.md`, `ExecEntryF16.md`), twelve receipts written after `9f98488`, and
`wave1/SimplifierCleanup/` (2 evidence files) — and `LOG.md` has no round-33 entry
(`grep -c '^## Round 33' LOG.md` → 0). All 64 seats have a receipt. No stale-base condition
exists: every counter above was run against the worktree that became `9f98488`, and the base tree
was never re-used as an "after" input.

## Cross-domain evidence (D3)

None encountered. The six sibling lanes hold zero F16-scoped material
(`CNVD|360SRC|众测|zc.cnvd.org.cn|security.360.cn|crowdsourced` → `scoped-terms=0` per lane), and two
of them route or disclaim the ground toward kasegi (`chousa-shokunin/corpus/knowledge/scope-refusal-r12.md:21`;
`kake-shokunin/corpus/README.md:464-465` quotes vulnerability handling as outside its province).
`ConnSibling.md` §Findings 1–2, §Province verdict. Nothing was absorbed and PROVINCE was not
re-scoped; the only PROVINCE edit is the F16 Frontier line.

## Assimilation

Theme: Chinese crowdsourced-testing platform scope and reward rules. Outcome: **2 admits by
document** (staged S034 → lane S049 = CNVD helpList; staged S035 → lane S050 = 360SRC rules, both
URLs byte-equal) and **7 refusals**, each with a lane-side reason and flip condition
(`SOURCES.md` id collisions proved S031–S048 take different documents, so adoption is by document
and never by number: `reg_ids=48`, `staged_ids=94`, `collisions=18` in
`.ufo/waves/round-33/assimilation/`). Quarantine slice: **0 adopted, 2 refused, 5 unreachable**;
S037's refusal (spliced field collage: `发布日期`/`实施日期` carry no colon on the live page, and two
blocks are skipped) is the recorded D6 verdict, re-measured on an independent fetch
(`ExecQuarantine.md` §5; `corpus/lessons/round-33.md` §Quarantine slice). The S049 page's tester VPN
credential instructions were never reproduced (Q6): no new file carries a quoted span from the
credential lines (`SentCred.md` §3; `CritBoundary.md`).

## considerthese

`considerthese/2026-10-25.md` proposal 1 (wave-evidence bloat / per-round committed-byte growth)
landed as a measurement, not a policy change: this round committed **1,366,042 B / 132 files /
17,170 insertions** of wave evidence at the integration byte — under a 5 MB budget, with **0**
corpus-copy paths and **0** scratch trees (`ExecGrowthMeasurement.md` §1–§4) — and the receipt
re-measures the round-25 bloat it targets on committed bytes (`3,773 files / 57,511,001 B`, of
which 3,097 paths contain `/corpus/`). R14 is re-affirmed, not amended. No new proposal was mined
beyond it.

## Open L0 questions note

The kasegi round-32 row of `.ufo/l0-questions.md:175` asks: `Ruling wanted: re-dispatch r32 with a
swarm in the next run, or admit the L1-only landing as the round.` Round 33 answers only the
**re-dispatch branch** (a validated 64-seat wave ran; 64 receipts at drafting), so the operator
ruling on whether the L1-only round-32 landing itself counts remains **open and unassumed** by this
report. No new L0 row was filed this round.

---

## Conflicts reported verbatim (for the canonical Rust judge)

1. **C1 predicate sentence vs erratum 1 vs landed instrument — `SentScopeFinal.md` F1 (HIGH).**
   Frozen text (`claims.json`, byte-identical to `6e55c8d`): `every manifest record has a url that
   matches exactly one corpus/SOURCES.md registry-row URL`. Kill rule text in the same file:
   `0 or 2+ matches = failure, name the record id`. Erratum 1 (`claims-erratum-1.md`) rules
   per-id binding and closes: `Predicate sentence, kill rule, counters and the 40/40/0 target are
   unchanged.` The landed instrument implements the erratum and prints `multi_row_url=2`, i.e. two
   records (S029, S006) carry a URL that also sits in another row while `records=40 bound=40
   unbound=0` and exit 0. Reported as filed; this draft does not decide which reading the judge
   applies. Remediation options named by the sentinel: an appended erratum 2 amending the predicate
   sentence, or the literal reading with `bound=38 unbound=2`. `ConnClaims.md` reaches the same
   point from the predicate side ("PATTERN HOLDS", subject to erratum 1 standing).
2. **`SKILL.md` diff size, two readings.** `SentScopeFinal.md` §6: `43 0 SKILL.md`;
   `git diff --numstat 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 HEAD -- SKILL.md` run by this
   seat: `19 0`. `ExecRegressionC1.md` §2.10 also reports `19 0`.
3. **Anchor count, expectation vs measurement.** Round-31 text and two seat items expected
   `7 in-range`; the measurement is `12 in-range, 0 bad` (`ExecRegressionC1.md` D-R33-1,
   `ExecNoHarmFinal.md` §4). Reported unrounded; the five extra anchors are the round-33 SKILL
   append's citations.

## Findings, survivors and open defects

1. **SURVIVOR, C1 counter mutant:** `MutCtrUnbound.md` §Verdict — a mutant that accepts a record
   with no `url` prints `records=2 bound=2 unbound=0` exit 0 on its fixture, i.e. **SURVIVOR** under
   the frozen kill rule as tasked. Not relabelled killed.
2. **SURVIVOR, C2 counter set:** `MutEntryF16.md` §Verdict — `SURVIVOR (coverage finding)`,
   reproduced on `53c48b3b…` and `1f7ac0a2…`: a restatement-shaped entry passes every C2 counter
   except the reviewer clause. Same shape as `CritC2Kill.md` §5.
3. **C1 blind spots, recorded not filed as failures** (`CritC1Kill.md`; `SCORECARD.md:1009-1019`):
   H1–H3 capture bytes/truncation/path traversal (covered only by `source-recheck.py`, whose 40
   `:sha256 OK` pins are the byte-level evidence), H4 nested dirs invisible to the one-level walk,
   H5 `fetched_utc="pending"` discharges rule C, H6 duplicate records inside one manifest, H7 a
   two-token row widens binding, H8 a `rejected` row can anchor a record.
4. **Entry findings still open** (`RevTranslation.md` F1–F6, all minor): F1 question-title
   transcription at entry L3/L48, F2/F3 annotation and overstatement wording, F4 citation range
   `113, 119-124` vs table `119-125`, F5/F6 wrap disclosure nits. None touches a manifest-bound
   string; the entry's `recheck:` line therefore still passes on F1.
5. **Uncommitted surfaces at drafting** (L1 must commit): `SCORECARD.md`, `SHONEN.md`,
   `corpus/lessons/round-33.md`, the untracked receipts, plus the `LOG.md` entry none of them can
   write.
6. **No seat is missing a receipt** (64/64 at 02:00 -03), but three claim-vs-disk / coverage gaps
   are open: (i) `ExecScratchDiscipline.md:75,99` charges `ExecWaveEvidencePack` with "the `rm -rf`
   claim and the disk disagree", while `ExecWaveEvidencePack.md:240` states its scratch was removed
   and `/fast/scratch/hyaku/kasegi-r33/ExecWaveEvidencePack/` still held 9 files at `01:56`
   (that seat's own leftover to rule on; `ExecScratchDiscipline.md` §1 had reported 0 of 55 landed
   seats leaving a tree at its earlier T3 pass); (ii) `CritMistakes.md` §2.3 shows the lesson's
   sweep block does not reproduce (printed `56 receipts` and `BLOCKED files=3 hits=10`; measured
   sets yield 57/62 receipts and `4/16`) and that `corpus/lessons/round-33.md:7` names
   `ScribeScorecard`/`RevC1BeforeAfter` as absent although both receipts predate the lesson; (iii)
   `CritMistakes.md` §2.4 names two pre-lesson attack findings (the `--selftest` forgery wording
   hole, `MutCtrSelftestSkip.md:84`; the substring-loosening world the selftest never builds,
   `MutCtrUrlMismatch.md:180`) that the lesson's M33-1…M33-6 ledger does not carry; its §4 proposes
   appending M33-7/M33-8 plus a re-run sweep with timestamp and listing digest.
7. **Unowned write paths:** `SentScopeFinal.md` F2 (MEDIUM) counts 36 paths outside the FILE
   OWNERSHIP set since base — 1 L1 erratum plus 35 seat evidence fragments in three new
   `wave1/<Seat>/` subdirectories at its sweep (`ExecCaptureBinding/`, `ExecRegressionC1/`,
   `ScribeInstrReadme/`); `ExecWaveEvidencePack.md` §3D lists four by its later census (adding
   `ScribeSkillGate/`). These are in-wave evidence, not production surfaces; reported, not deleted.
8. **Pre-existing, routed:** `corpus/QUALITY.md:77` (R13) cites `README.md:159` which is past EOF at
   the lane root (`ScribeQuality.md` F1, unchanged this round); M31-3 stale `SOURCES.md` line
   citations deepened by this round's row append (§Sources above); `ExecGrowthMeasurement.md` §4
   notes two near-duplicate `ScribeSkillGate` anchor dumps (same size, different bytes) — economy
   observation, not a correctness defect.
9. **Gate prose numbers not taken from the bytes** (`RevGateSpot.md` Findings 1): the lesson's Gate
   table states the S049 quote is "19 characters" and the S050 quote "23 characters"; measured
   lengths are 31 and 22. The quotes, locations (`S049.txt:214`, `S050.txt:591`) and access dates
   are correct, so both admits stand; the counts are a prose defect of the M33-2 class in
   `corpus/lessons/round-33.md` (ScribeLesson's file; not edited here).
10. **Evidence duplication and a citable `/tmp` path** (`SimplifierCleanup.md` §2–§4): nine copies of
    the same 714-byte binding output exist under four paths (7,500 B of redundant evidence; receipts
    cite different paths for identical bytes — presentation, not fabrication); two empty files
    (`wave1-plan.err`, `wave1-run.err`, both `e3b0c442…`) carry no information; and
    `ExecDeterminism.md:172,187` cites a `/tmp` path
    (`/tmp/capture-binding-selftest-ca3wqtcy`) as evidence, which the round's scratch rule forbids as
    citable evidence — the instrument's fixture root honoured `TMPDIR`/`$HYAKU_SCRATCH` only when set.
11. **Calibration note:** `SCORECARD.md` carried no round-32 section at base, so this round's
    before-column is measured at base bytes and the "last change" column stays 31
    (`RevCalibration.md`; `SCORECARD.md:982-998`).

## Artifact paths (lane-relative)

- Report draft / this receipt: `.ufo/waves/round-33/wave1/ScribeReportDraft.md`
- Receipt index the report cites: `.ufo/waves/round-33/wave1/ExecWaveEvidencePack.md` (§3B table, §3C dead seats)
- C1: `wave1/ExecCaptureBinding.md`, `wave1/ExecManifestUpgrade.md`, `wave1/ExecManifest32.md`,
  `wave1/ExecRegressionC1.md` (+ `ExecRegressionC1/` raws), `wave1/RevC1BeforeAfter.md`,
  `wave1/RevC1Instrument.md`, `wave1/CritC1Kill.md`, `wave1/MutCtr{Unbound,UrlMismatch,FetchMissing,SelftestSkip}.md`,
  `wave1/Mut{ManifestLegacy,LegacyManifestDrop}.md`
- C2: `wave1/ExecEntryF16.md`, `wave1/ExecRegistryAppend.md`, `wave1/ScribeReadmeF16.md`,
  `wave1/ExecExpectedList.md`, `wave1/ExecHarnessC2.md`, `wave1/ExecCensusAfter.md`,
  `wave1/RevEntryF16.md`, `wave1/RevRowS049.md`, `wave1/RevRowS050.md`, `wave1/RevQuoteSweep.md`,
  `wave1/RevTranslation.md`, `wave1/MutEntryF16.md`, `wave1/CritExpansion.md`, `wave1/CritC2Kill.md`
- Frontier items: `wave1/ScoutPackageThemes.md`, `wave1/ExecQuarantine.md`, `wave1/ExecGrowthMeasurement.md`,
  `wave1/ExecErratumCheck.md`, `wave1/ScoutF16Sweep.md`, `wave1/ConnSibling.md`, `.ufo/waves/round-33/assimilation/`
- Scribes: `wave1/Scribe{Quality,InstrReadme,SkillGate,Province,SearchLog,Scorecard,Shonen,Lesson}.md`,
  `corpus/lessons/round-33.md`
- Conformance / sentinels: `wave1/Exec{BeforeReceipts,CensusDry,Determinism,ForeignCwd,ScratchDiscipline,WaveEvidencePack}.md`,
  `wave1/Sent{Cred,ScopeFinal}.md`, `wave1/Conn{Claims,Ownership}.md`

## Receipt — commands this seat ran (and their output)

Polling (cap 50 min, 20–59 s interval; the item's rule 9 shape):

```
$ ls .ufo/waves/round-33/wave1/*.md | wc -l     # 01:16 → 02:00 -03
1 … 5 … 22 … 40 … 55 … 60 … 63 … 64              # monotonic; no receipt removed
$ date -Is                                       # drafting stamp
2026-10-26T02:00-03:00
```

State facts cited above, all read-only:

```
$ git rev-parse --short origin/master            # 9f98488
$ git rev-list --left-right --count origin/master...master
0	0
$ git status --porcelain | wc -l                 # 18 at drafting (19 files with -uall)
$ grep -c '^## Round 33' LOG.md                  # 0
$ git diff --numstat 690b69da HEAD -- SKILL.md PROVINCE.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md corpus/instruments/README.md corpus/instruments/knowledge-expected.txt
2	0	PROVINCE.md
19	0	SKILL.md
55	0	corpus/QUALITY.md
26	0	corpus/README.md
6	0	corpus/SOURCES.md
145	0	corpus/instruments/README.md
1	0	corpus/instruments/knowledge-expected.txt
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # 50
$ ls corpus/knowledge/*.md | wc -l                                        # 45
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/{n++} END{print n+0}' corpus/README.md   # 16
$ grep -n 'capture-binding-check' SCORECARD.md | head -1                  # capability row present (:1074)
```

No counter named in `claims.json` was re-run by this seat: every before/after value above is quoted
from the receipt that produced it, on the commit that receipt names. Where this seat ran a command,
it is listed in this section only.
