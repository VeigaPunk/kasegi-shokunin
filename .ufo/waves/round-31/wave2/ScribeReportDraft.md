# ScribeReportDraft — round-31 report body (DRAFT for the L1; not the filed report)

- **Seat:** `ScribeReportDraft` (scribe, leaf — no subagent dispatch, no background job of my own).
- **Round / lane:** kasegi-shokunin round 31 (hyaku run 7), lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- **Base / freeze / landed:** base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze
  `738a77999a00efbca129cfccb28a481037f6241f`; wave-1 integration `eecad59db166e0626ca2472e96ea48bc28a35153`
  (HEAD at every measurement below). Wave-2 edits are **uncommitted** at my read → the L1 fills `<LANE_HASH>`
  (one marker per commit it creates; I never commit).
- **Answering model actually run on:** `opencode-go/deepseek-v4.1-flash` (config route table; no model passed by me).
- **Tooling:** nothing installed or upgraded; no pacman transaction; no network fetch; no git/jj mutation
  (read-only `rev-parse`/`status`/`log`/`show`/`diff` only). No write outside this receipt.
- **Method:** read all 42 wave-2 receipts (41 peer receipts + this one) and the 38 wave-1 receipts as evidence; every number below is copied from a
  receipt's own command output or from my final read-only run in §0. Quotes are ≤25 words with their file location.
  Nothing here is a re-verdict: the canonical judge rules on conflicts (§7), I only report them verbatim.
- **Wave shape:** wave 1 `kasegi-r31-build` 38 seats (scout 5, connector 3, executor 13, scribe 9, reviewer 2, critic 2,
  mutation-tester 3, sentinel 1); wave 2 `kasegi-r31-falsify` 42 seats (executor 17, mutation-tester 7, reviewer 6,
  scribe 5, critic 3, connector 2, scout 1, sentinel 1) — `wave2/ScribeLesson.md` §3.1, from the two dispatch JSONs.

## 0. Quiescence and final bytes (my own read-only run)

All 42 wave-2 seats have a receipt; no writer was active. `2026-10-26T00:50:47Z`:

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ git status --porcelain        # wave-2 edits only (below), no seat mid-write
 M SCORECARD.md ; M SHONEN.md ; M corpus/QUALITY.md ; M corpus/instruments/limb-mutation-check.py
?? corpus/lessons/round-31.md ; ?? .ufo/waves/round-31/wave2/
$ sha256sum (final working-tree bytes)
237fd07cbcb4a12a470e912d1a4b68ff1968fde62f2709b182822fed42d791f4  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
5899e02bc60172ecc1bfff6324fe014ab0b6aa6a6fc7e27335805b678b47e2e5  corpus/QUALITY.md
4076091c3d06d5336858ce7b16a05a8d0722def7f527b8e39b39ac7586a7a9da  SCORECARD.md
2d4468a2dd3e91b3638bb1c40d02fb6b7fa66b82f634c6048810292490d01436  SHONEN.md
3f3a5501ede104fcda3e5b7511bcf2eb71c1c8aa56b08cd1bddfaddb75762503  corpus/lessons/round-31.md  (161 lines, 51728 B)
1f16e37191193af1ccce381842d7ceea422f6a4e8f4b9fffae2e36da7bb692bb  corpus/knowledge/vendor-third-party-finding-coordination.md (160 lines)
5a03c696312bd5fd8fe8307f75bd9723cac97fe3e44f0f3ba46a68607295f6f5  corpus/SOURCES.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
864deb7df810539d3a92a9c520c94e218836233da42378ba774e48bbf339cf1b  LOG.md
```

`source-recheck.py` still reports `fd2e01e8…` after the wave-2 wave; the counter moved to `237fd07c…` only because
`ExecCounterFix` landed the guard fixtures (`wave2/ExecCounterFix.md` §1). `SKILL.md` did **not** move in wave 2
(`81763604…`, unchanged from `eecad59`).

Confirming run (mine, read-only, lane root, final bytes; counter writes only its own `/tmp` scratch):

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
guard invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
guard invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
guard invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
guard cases=3 failures=0
LIMB RA-parse live=0/y mutant=1/n verdict=killed
… 13 LIMB lines, every one killed, every line live ≠ mutant …
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
$ python3 corpus/instruments/recheck-audit.py --quiet
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048
S048:sha256 OK / S048:Q1..Q8 OK occurrences=1      (9 lines)   recheck_exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | grep -E 'F15|entries='
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0
entries=18 pass=18 exit=0
```

This run reproduces `wave2/ExecRegressionC1.md` §2–§4 and `wave2/ExecCensusFinal.md` §1 byte-for-byte on the summary
lines; it is a confirming read, not a second experiment.

## 1. Work performed

### C1 — `depth:verifiability` (score 4, held; target: every named limb load-bearing on the landed bytes, R13)

- One-limb mutation ledger `corpus/instruments/limb-ledger.json` (13 limbs + 3 controls, `{"version":1,…}`) and
  counter `corpus/instruments/limb-mutation-check.py` landed (`eecad59`); merge verified by
  `wave1/ExecLedgerMerge.md` §1–§4 (ledger `version=1 limbs=13 controls=3`).
- `recheck-audit.py` limbs: frozen (a) parse, (b) cwd, (c) paths and strict (d) cdroot, (e) instrument, (f) own mapped,
  then (g) completeness and (h)/(i) expect-missing / expect-unexpected (`wave1/ExecRALimbs.md` §2–§4a; code map
  `wave1/ScoutRALimbMap.md`). Survivor → strengthening: `RA-completeness` was byte-identical under the mutant on
  pre-round bytes, so two `main()`-level selftest cases (`complete-empty`, `complete-missing-line`) were added and the
  mutant now exits 1 with two FAIL lines (`wave1/ExecRALimbs.md` §5). **This strengthening is the work, not a relabel.**
- `source-recheck.py` limbs SR-stem-mismatch / SR-occurrence-not-unique with the isolating fixture pair under
  `corpus/instruments/limb-fixtures/sr/`; both killed, each mutant flips only its own fixture
  (`wave1/ExecSRLimbs.md` §3–§7). This closes the round-30 routed defect M30-1 (B2 tripped B1 first).
- `frontier-recheck-count.py` limbs FR-missing-entry / FR-duplicate-entry with self-contained fixture roots
  (`corpus/instruments/limb-fixtures/fr/`, 2480 B total, no corpus copy; instrument bytes unchanged at `aa60b581…`)
  — `wave1/ExecFRLimbs.md` §A–§D.
- Counter semantics: per-row `invalid:live-baseline` → `invalid:find-count` → `invalid:noop` → `invalid:nocompile` →
  run → `killed|survivor`; 3 controls (no-op, non-compile, equivalent); 20-case `--selftest`; exit 0 iff
  n==k, s==0, all rows valid, rejected==controls (`wave1/ExecCounter.md` §2–§5).
- Entry-list basis: `corpus/instruments/knowledge-expected.txt` extended to 44 entries / 46 lines so the audit's
  expected set matches the new entry (`wave1/ExecExpectedList.md`).
- Wave-2 falsification: 13 per-limb attack seats re-derived every limb by hand and probed alternative mutants
  (`wave2/ExecLimb*.md`); 6 counter-mutant seats (`wave2/MutCtr*.md`); counter repair (`wave2/ExecCounterFix.md`);
  full post-fix regression with every registered source recheck (`wave2/ExecRegressionC1.md` §5: 38 ids / 8 manifests,
  38/38 exit 0); calibration sweep (`wave2/CritCalibration.md`); score-gap review (`wave2/RevScoreGap.md`).
- `corpus/instruments/README.md` and `SKILL.md` gained round-31 registry rows for the counter/ledger and score-gap
  (`wave1/ScribeInstrReadme.md`, `wave1/ScribeSkillGate.md`); `corpus/QUALITY.md` gained R16/R17
  (`wave1/ScribeQuality.md`) and, after the falsify wave, superseding R18/R19 (`wave2/ScribeQualityFix.md`).

### C2 — `coverage` (score 7, held; target: frontier F15 admitted with one grounded entry and a registered source)

- Frontier F15 "A vendor's research programme as an intake route for other vendors' bugs" admitted: `corpus/README.md`
  appended coverage-map row + F15 frontier row (25 insertions, one hunk; `wave1/ScribeReadmeF15.md` §3–§4).
- Capture + manifest: `corpus/source-snapshots/round-31/S048.txt` (97 lines, sha256 `2001ad77…`) and
  `manifest.json` (8 exactly-once quote assertions) via the lane instrument `capture-source.py`
  (`wave1/ExecCapManifest.md`; live 200/81802 B at `wave1/ScoutMSVR.md`).
- Knowledge entry `corpus/knowledge/vendor-third-party-finding-coordination.md` (160 lines, `1f16e371…`), header
  `source: S048`, `ground: F15`, one runnable `recheck:` (`wave1/ExecEntryF15.md` §2–§7).
- Registry row S048 appended inside `## Registry` at `corpus/SOURCES.md:54`, plus a Search-log bullet and an R8
  change-log bullet; 3 added lines, 0 removed (`wave1/ExecRegistryAppend.md` §2, §5–§9).
- Pre-append gates: id-collision scratch and renumber map by document (`wave1/ExecCensusDry.md` §3–§5);
  census dry-run controls (`wave1/ExecCensusDry.md` §1–§2); source-bar review (`wave1/RevSourceBar.md` ADMIT-ROW).
- Wave-2 falsification: row review (`wave2/RevRowS048.md`), entry Q1–Q10 review (`wave2/RevEntryQ.md`), two quote/reach
  reviews against fresh fetches (`wave2/RevQuoteRoutes.md`, `wave2/RevQuoteRoles.md`), live drift
  (`wave2/ScoutLiveDrift.md`), expansion/restatement attack (`wave2/CritExpansion.md`), final seven-cell census
  (`wave2/ExecCensusFinal.md`), gate spot-check (`wave2/RevGateSpot.md`), assimilation fit (`wave2/ConnAssimilationFit.md`).

### Non-claim frontier items

- **Assimilation** theme = vendor third-party-finding coordination; staged `S080` → lane `S048` **by document**
  (URL byte-equal, staged `S048` is a different page); collision scratch in `.ufo/waves/round-31/assimilation/`
  (`reg-ids` 47, `staged-ids` 94, `collisions` 17, `guard-proof-collisions` `S031`, `quarantine-slice` 7 rows);
  five package entries refused with flip conditions, none relaxed (`wave1/ScoutPackageThemes.md`,
  `wave2/ConnAssimilationFit.md` §2–§3).
- **considerthese proposal 2** mined: read-only `corpus/instruments/score-gap.py` (548 lines, `855869bf…`, selftest
  `fields=7 failures=0`) plus an append-only status flip in `corpus/knowledge/considerthese-proposals-ledger.md`
  (`d91889e5…` → `c354ca02…`, 20 → 35 lines) — no score move asserted (`wave1/ExecScoreGap.md` §6,
  `wave1/ScribeConsiderthese.md` §3–§5).
- **M31-1 stale premise** closed both halves: SCORECARD round-30 paragraph named by an appended erratum
  (`SCORECARD.md:837-860`), and the missing round-30 LOG entry appended (`LOG.md:1469` heading, +115 lines);
  red-before/green-after on the same checks, with mutant controls (`wave1/ExecErratumCheck.md` §1–§2, §6;
  `wave1/ScribeErratum.md`, `wave1/ScribeLogR30.md`). Wave 2 then found the shipped check's own able-to-fail gap
  (deleting the filed paragraph left it green) and superseded it with R18/R19 (`wave2/CritMistakes.md` §2,
  `wave2/ScribeQualityFix.md` §2–§4). `M31-1` is recorded in `corpus/lessons/round-31.md:100`.

## 2. Landed changes

`LOG.md` has **no round-31 entry** at my read: `grep -cE '^## .*[Rr]ound[- ]?31' LOG.md` → `0` (the file's round-31
bytes are the round-30 entry appended by `ScribeLogR30`; `SHONEN.md` says so in box 2). The L1 must append the
round-31 LOG entry at close and tie the rows below to it. Commit column: `eecad59` for wave-1 landings; `<LANE_HASH>`
for the wave-2 working-tree edits the L1 commits.

| # | changed surface | change | commit | proving receipt |
|---|---|---|---|---|
| 1 | `corpus/instruments/limb-ledger.json` | new: 13 limbs + 3 controls | `eecad59` | `wave1/ExecLedgerMerge.md` §1–§3 |
| 2 | `corpus/instruments/limb-mutation-check.py` | new counter; wave-2 guard fixtures (`c660a95f…` → `237fd07c…`, +81/−8) | `eecad59` + `<LANE_HASH>` | `wave1/ExecCounter.md`; `wave2/ExecCounterFix.md` §5 |
| 3 | `corpus/instruments/recheck-audit.py` | `selftest()` only: duplicate fixture-write loop deleted, two `main()`-level completeness cases added (`3fc0d751…` → `5d4842da…`) | `eecad59` | `wave1/ExecRALimbs.md` §2, §5–§6 |
| 4 | `corpus/instruments/source-recheck.py` | `selftest()` only: `quote-absent` case pinning `reason=quote-not-found` + help text (`33602a9d…` → `fd2e01e8…`) | `eecad59` | `wave1/ExecSRLimbs.md` §8; `git diff b374feb..HEAD -- corpus/instruments/source-recheck.py` |
| 5 | `corpus/instruments/limb-fixtures/{sr,fr}/` | isolating fixtures + NOTE.txt (10 files, 2480 B fr tree) | `eecad59` | `wave1/ExecSRLimbs.md` §3; `wave1/ExecFRLimbs.md` "Files written" |
| 6 | `corpus/instruments/knowledge-expected.txt` | 43 → 44 entries / 46 lines | `eecad59` | `wave1/ExecExpectedList.md` |
| 7 | `corpus/instruments/score-gap.py` | new read-only reporter (not a claim) | `eecad59` | `wave1/ExecScoreGap.md` §1–§6 |
| 8 | `corpus/instruments/README.md` | round-31 append (counter, ledger, score-gap; superseded-digest note) | `eecad59` | `wave1/ScribeInstrReadme.md` §1–§6 |
| 9 | `corpus/knowledge/vendor-third-party-finding-coordination.md` | new F15 entry, 160 lines | `eecad59` | `wave1/ExecEntryF15.md`; `wave2/RevEntryQ.md` |
| 10 | `corpus/SOURCES.md` | S048 row at `:54` + search-log + R8 bullet (3 added, 0 removed) | `eecad59` | `wave1/ExecRegistryAppend.md` §2, §8 |
| 11 | `corpus/source-snapshots/round-31/{S048.txt,manifest.json}` | capture (97 lines) + 8-assertion manifest | `eecad59` | `wave1/ExecCapManifest.md` §1–§4 |
| 12 | `corpus/README.md` | coverage-map row + F15 row + 15/15 amendment (+25) | `eecad59` | `wave1/ScribeReadmeF15.md` §3–§4 |
| 13 | `PROVINCE.md` | F12–F15 amendment, 20 insertions, 0 deletions | `eecad59` | `wave1/ScribeProvince.md` §5–§6 |
| 14 | `SKILL.md` | round-31 Gates & probes registry addition (+14) | `eecad59` | `wave1/ScribeSkillGate.md` §1–§3 |
| 15 | `corpus/QUALITY.md` | R16/R17 (+7) then R18 (supersedes R16) / R19 (supersedes R13) (+61) | `eecad59` + `<LANE_HASH>` | `wave1/ScribeQuality.md` §1; `wave2/ScribeQualityFix.md` §4 |
| 16 | `SCORECARD.md` | r31 erratum (+25) then round-31 claims/move-log/capabilities (+87) | `eecad59` + `<LANE_HASH>` | `wave1/ScribeErratum.md` "Append performed"; `wave2/ScribeScorecard.md` §4 |
| 17 | `LOG.md` | round-30 entry appended (+115); **no round-31 entry yet** | `eecad59` | `wave1/ScribeLogR30.md` §5–§6 |
| 18 | `corpus/knowledge/considerthese-proposals-ledger.md` | round-31 status-flip section (+15), proposal 2 → mined | `eecad59` | `wave1/ScribeConsiderthese.md` §3–§4 |
| 19 | `corpus/lessons/round-31.md` | new lesson, 161 lines: Gate, M31-1…M31-7, O1–O6, census, no-harm, open items | `<LANE_HASH>` | `wave2/ScribeLesson.md` §1–§4 |
| 20 | `SHONEN.md` | four box evidences replaced with round-31 readings (+34/−11); all boxes stay `[~]` | `<LANE_HASH>` | `wave2/ScribeShonen.md` §1–§3 |

Not landed / not this round's write: the SCORECARD relabel naming the landed `44/44` (`wave2/CritMistakes.md` O5;
`wave2/ScribeQualityFix.md` §5.1), the lesson's two missing `git show b374febb…` command qualifiers
(`wave2/RevGateSpot.md` F1), the F15 sentence edits in `wave2/RevEntryQ.md` §5 / `wave2/CritExpansion.md` §6, the
score-gap defect in `wave2/RevScoreGap.md`, and the stale-census relabel in `wave2/ExecNoHarmDensity.md` §6. The two
check tightenings O3/O4 *did* land, as R18 and the tightened CHECK B' (`corpus/QUALITY.md:102`, `:136-143`).

## 3. Before → after measurements

### C1 — depth:verifiability (measuring commit: `eecad59`; wave-2 counter fix at `<LANE_HASH>`)

Before values are the frozen do-nothing control at base `b374febbb` (`.ufo/waves/round-31/c1-controls/before.txt`);
after values are my final run in §0, matching `wave2/ExecRegressionC1.md` §2–§4 and `wave2/ExecCounterFix.md` §5.

| # | counting command | before (base `b374febbb`) | after (`eecad59` + `<LANE_HASH>`) |
|---|---|---|---|
| 1 | `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` | absent: `counter_exit=2`, `ls_exit=2` | `limbs=13 killed=13 survivors=0`; `controls=3 rejected=3`; 13 `LIMB ` lines, every `live` ≠ `mutant`; `guard cases=3 failures=0`; exit **0** |
| 2 | same, twice + `cmp` | n/a | byte-identical, stdout sha256 `d6aefddca50293347c348646479bbe406745ad3163422b27edefcea861264270` (both runs) |
| 3 | `python3 corpus/instruments/limb-mutation-check.py --selftest` | n/a | `selftest cases=20 failures=0`, exit 0 |
| 4 | `python3 corpus/instruments/recheck-audit.py --quiet` | `strict pass=43/43`; `executes=19 gated=24`; `lines=43`; `expected=43`; exit 0 | `strict pass=44/44`; `executes=20 gated=24 broken=0`; `lines=44`; `expected=44 missing=0 unexpected=0`; exit 0 |
| 5 | `python3 corpus/instruments/source-recheck.py --selftest` | `selftest cases=9 failures=0` | `selftest cases=10 failures=0` |
| 6 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=17 pass=17 exit=0` | `entries=18 pass=18 exit=0` incl. `PASS F15 … ids=S048` |
| 7 | `sha256sum` of the three instruments | `3fc0d751…` / `33602a9d…` / `aa60b581…` | `5d4842da…` / `fd2e01e8…` / `aa60b581…` (frontier unchanged) |
| 8 | ledger/counter digests | absent | ledger `c042adf6…` (unchanged through wave 2); counter `c660a95f…` at `eecad59` → `237fd07c…` after the guard fix |

C1 predicate: met on the final bytes. Disclosed deviation: the frozen `counter_commands` do not name `--selftest` or
the guard lines; the counter now also prints 3 `guard …` lines + `guard cases=3 failures=0`, which are neither limbs
nor controls and never enter the two counts (`wave2/ExecCounterFix.md` §4, §6).

### C2 — coverage (measuring commit: `eecad59`; no C2 file moved in wave 2)

Before = `.ufo/waves/round-31/c2-controls/before.txt` (base `b374febbb`); after = `wave2/ExecCensusFinal.md` §1 and my
§0 run.

| # | counting command | before | after |
|---|---|---|---|
| 1 | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | `14` | `15` |
| 2 | `grep -lE '^source: S048 ' corpus/knowledge/*.md \| wc -l` | `0` | `1` |
| 3 | `grep -cE '^\|[[:space:]]*S048[[:space:]]*\|' corpus/SOURCES.md` | `0` | `1` |
| 4 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | `47` | `48` |
| 5 | `scripts/sources-census.sh validate --root … kasegi` | `W04 S028`, `W04 S029`, `ok`, exit **0** | same three lines, exit **0** (no new E/W) |
| 6 | `python3 corpus/instruments/frontier-recheck-count.py` | `entries=17 pass=17 exit=0` | `entries=18 pass=18 exit=0`, includes `PASS F15 … ids=S048` |
| 7 | `source-recheck.py --manifest corpus/source-snapshots/round-31/manifest.json --source S048` | manifest absent: `UNAVAILABLE reason=missing`, exit **2** | 8 × `OK occurrences=1`, `sha256 OK`, exit **0** |

Junk-row control (scratch only): a bare S048 registry row with no entry and no capture leaves frontier 14, citations 0,
harness 17/17, and is flagged `W03 S048 mined but unused`; `source-recheck` exits 2
(`wave2/ExecCensusFinal.md` §4). Do-nothing re-derivation matches `c2-controls/before.txt` cell for cell.

## 4. Sources & frontier

- **Registry rows:** `47 → 48` (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`;
  base re-derivation from `git archive b374febb…` printed 47). Histograms (`sources-census.sh census`, live):
  `tier.A 45 / tier.B 1 / tier.C 2` vs base `44 / 1 / 2`; `status.mined 36 / queued 9 / rejected 3` vs base
  `35 / 9 / 3`; `FLEET.missing 0`; `census_summary_exit=0` (`wave2/ExecCensusFinal.md` §3b).
- **Rows touched:** `0` modified. `diff base-SOURCES current` → 3 `>` lines and 0 `<` lines; the row is new S048, the
  other two are the Search-log bullet and the R8 bullet. No status/recheck/used-by cell changed on a pre-existing row
  (`wave1/ExecRegistryAppend.md` §8). R6 drift disclosed: the insert at `:54` shifted cited lines below it
  (`wave2/RevRowS048.md` INFO-1; `corpus/lessons/round-31.md` M31-3, **open**).
- **Frontier:** admitted rows `14 → 15`; the only advanced row is **F15**
  (`corpus/README.md:309`, status `admitted`, entry `knowledge/vendor-third-party-finding-coordination.md`,
  sources `S048`). F01–F14 rows untouched; the older "14/14" sentence is retained as history under R9 and an appended
  amendment states 15/15 (`wave1/ScribeReadmeF15.md` §3–§4; `PROVINCE.md` F12–F15 amendment).
- **Census exit codes:** before `0` (frozen `census-before.txt`), after `0` diffed against it — the only diff is the
  frozen file's own trailing wrapper line `census_exit=0` (`wave2/ExecCensusFinal.md` §3a).
- **Assimilation (theme: vendor third-party-finding coordination):** staged package entry
  `vendor-third-party-finding-coordination-2026-10-23.md` admitted as a lane **rewrite**, not as staged bytes
  (staged `48e9de4e…` → landed `1f16e371…`; `wave2/RevGateSpot.md` F5). Id-collision lists in
  `.ufo/waves/round-31/assimilation/`: `reg-ids` = 47 lane ids `S001…S047`; `staged-ids` = 94 ids `S031…S124`;
  `collisions` = 17 ids `S031…S047` (base blob); `guard-proof-collisions` = `S031` (5 bytes `S031\n`);
  `quarantine-slice` = 7 round-30 quarantine rows. Landed collision set is **18** (`S031…S048`), the new member being
  the lane's own S048 (`wave2/RevGateSpot.md` F4); the renumber **map** is `S080 → S048` by document, with the
  `used-by` path changed from the date-suffixed staged name to `corpus/knowledge/vendor-third-party-finding-coordination.md`
  (`wave1/ExecCensusDry.md` §5; `wave1/ExecRegistryAppend.md` §2). **Caveat:** RevGateSpot disagrees with calling
  `guard-proof-collisions` a "guard proof" — it is the first collision id, not a sensitivity demonstration
  (`wave2/RevGateSpot.md` (d); lesson Gate caveat).
- **Refusals:** four round-31 refusals (`cn-crowdsourced-testing-roles-and-conduct.md`,
  `program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md`,
  `chinese-crowd-testing-national-standard-2026-10-23.md`) plus one standing round-30 refusal, each with digests and
  flip conditions; no Q/R bar relaxed, no refused file copied (`wave2/ConnAssimilationFit.md` §2; `wave2/RevGateSpot.md` F5).
- **considerthese proposal mined:** proposal 2 — `score-gap.py` + ledger flip (see §1). Its first field prints
  `recheck: lines=44 executes=20 gated=24 broken=0 exit=0`; gap line `24 of 44 rechecks still gated on a lost base`.
  A reviewer found a `defect` in the reporter (see §7) — the mining stands, the instrument does not yet pass review
  (`wave2/RevScoreGap.md` §Verdict).

## 5. Trend verdicts

Definitions read from `/home/vgpnk/Projects/shokunin/LEARNING.md:33-35`.

- **expansion — improved.** Net new admitted entry on ground the base tree did not hold: F15 entry admitted, citing
  the `mined` row S048; base-tree sweep for `MSVR|MSRC|research programme|coordinator of vulnerabilities|not developed by`
  returned 0 hits (`wave2/CritExpansion.md` §1). Frontier 14 → 15. **Caveat:** credit rests on two residuals
  (self-named coordinator; conditional internal-research route), not the entry's claimed three — the critic's
  `partial` verdict and the reviewer's Q3 `REFUSE` both narrow it (`wave2/CritExpansion.md` §6, `wave2/RevEntryQ.md` §5).
- **quality — harmed (narrow, correctable before close).** An admitted entry was found false in one warrant sentence and
  left unmarked at my read: `wave2/RevEntryQ.md` F1 files Q3 `REFUSE` for the sentence at entry `:84-87`, refuted by
  `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:49, :66`; no erratum or edit is in the tree.
  LEARNING counts "found false or stale and left unmarked" against quality; landing the routed correction flips this
  line. Counterweights, which do not clear that clause: the bar gained R16/R17 and then R18/R19 with runnable checks
  (`wave2/ScribeQualityFix.md` §4), the audit moved 43/43 → 44/44 at exit 0, and two of the three survivor events were
  closed by strengthening, the third disclosed and not landed (`corpus/lessons/round-31.md` M31-5). Also open: 12
  `stale-live` statements across `SHONEN.md`, `SKILL.md`, `SCORECARD.md`, `corpus/README.md` and
  `corpus/instruments/README.md` (`wave2/CritCalibration.md` §2, "Mismatch count: 12 stale-live").
- **discernment — improved.** Every refusal's criteria were re-derived on the staged bytes and every flip condition
  names the rows to capture; the admission was re-derived by document, not by id (two independent seats:
  `wave2/ConnAssimilationFit.md` §2–§3 and `wave2/RevGateSpot.md` (b)/(c), the latter labelled `lane-seat`, not an
  outside verifier). Disagreements became criteria: R18/R19 supersede R16/R13 after the wave-2 attack
  (`wave2/CritMistakes.md` §2, §6; `wave2/ScribeQualityFix.md` §2–§4), and M31-7/O1–O6 record the counter-mutant holes
  (`corpus/lessons/round-31.md:100-124`). **Limit:** R18's residual (a forged line carrying the live pair and the filed
  address still reads as closure) is disclosed in the row itself, and the C2 Q3 disagreement is recorded but not
  converted into a criterion.

## 6. SHONEN lines

`SHONEN.md` (`2d4468a2…`, +34/−11) keeps the header and four `[~]` boxes; no box is ticked (no non-author verifier is on
record). Verbatim (boxes condensed to their evidence sentence):

- `- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources` — "density.py SKILL.md prints
  mean dens 191.5 over 24 blocks and 689 path-citation instances"; anchorcheck `7 in-range cite instances, 0 bad`;
  the mean move is only the appended block 24, "whose resolvable share is 11/27 = 40.74%, so the receipt claims no
  quality gain for it".
- `- [~] At least one end-to-end domain task executed and logged in LOG.md` — round-30 entry at `LOG.md:1469`; C1 counter
  `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`; C2 census exit 0, harness `entries=18 pass=18`;
  "No round-31 `LOG.md` entry exists yet at HEAD `eecad59`; the box stays `[~]`."
- `- [~] Instructions executable by an agent without oral context` — 44/44 entries audited, `strict pass=44/44` from
  lane root and `/`, harness `PASS F15 … ids=S048`, S048 recheck exit 0 with 8 assertions.
- `- [~] No cross-domain bleed (PROVINCE.md still accurate)` — PROVINCE `20/0` append naming F12–F15; sibling sweep found
  zero MSVR / zero vendor-research hits across six sibling corpora; `kake-shokunin/corpus/README.md:457-460` refuses
  vulnerability intake.

## 7. Conflicts and open items (reported verbatim; the canonical judge rules)

1. **C2's entry clause is contested.** C2's kill rule includes "the entry fails any QUALITY.md Q1-Q10 under the
   non-author reviewer". `wave2/RevEntryQ.md` §5: "**REFUSE** — on **Q3 only**", because "No quote and no location are
   given for `F10's thesis is …`" and the claim is refuted by committed bytes the entry itself cites. Against it:
   `wave2/RevQuoteRoles.md` finds "0 HIGH, 2 MEDIUM, 12 LOW" and says "none is a claim without a locatable quote";
   `wave2/CritExpansion.md` verdict "**`partial`**" with "C2 is not failed by this review"; `wave2/RevRowS048.md` finds
   "all six rules **CONFORMANT** at row level"; `wave2/RevQuoteRoutes.md` finds "No high and no medium finding" and all
   8 manifest assertions AGREE; `wave1/CritC2Kill.md` §5–§7 held expansion credit and met the mechanical predicate.
   `wave2/ScribeScorecard.md` §5 records C2 as "NOT VERIFIED, honest stop, no credit claimed (score stays 7)";
   `SCORECARD.md:947` reads "7 held, no credit claimed … the frozen entry clause is contested by a non-author Q3 REFUSE".
   My draft follows that: **C2's mechanical cells are met; the entry clause is not cleared.**
2. **C1's counter-mutant set was falsified at first landing and repaired post-freeze.** Three survivors on the pre-fix
   counter `c660a95f…`: `wave2/MutCtrNoLiveBaseline.md` ("SURVIVOR — a hole in the frozen counter-kill detector."),
   `wave2/MutCtrNonUniqueFind.md` ("SURVIVOR — coverage hole in the frozen counter design"), `wave2/MutCtrTimeoutKilled.md`
   ("SURVIVOR (a hole in the counter, on the landed bytes)"). Repair at `237fd07c…` closes all three through three
   implicit guard fixtures without changing the frozen counts (`wave2/ExecCounterFix.md` §4–§5), and all six mutants
   now exit 1 (`wave2/ExecCounterFix.md` §5 table). Residual disclosed: `invalid:import` and
   `invalid:mutant-baseline` are still not guard fixtures (`wave2/ExecCounterFix.md` §7).
3. **Limb rows: 10 `holds`, 3 `weak`.** `weak` for RA-paths (a same-limb survivor at the `named` conjunct, so the limb
   is only half-witnessed), RA-cdroot (shape-narrow fixtures) and FR-missing-entry (mutant output is a bare traceback;
   the whole discrimination rests on one regex) — `wave2/ExecLimbRApaths.md` §4–§6, `wave2/ExecLimbRAcdroot.md` §Verdict,
   `wave2/ExecLimbFRmissingentry.md` §5. No row defect; each recommends fixtures/rows the L1 may route. Separately,
   `RA-expect-unexpected` `holds` but reports two stdout-only survivors (`wave2/ExecLimbRAexpectunexpected.md` §5–§6).
4. **Shipped M31-1 checks had an able-to-fail gap; superseded, not silently kept.** `wave2/CritMistakes.md` §2.1 and
   `wave2/MutErratumCheck.md` §5 show deletion/exemption survivors; `wave2/ScribeQualityFix.md` §2.1 lists
   "Rows 3, 4, 6, 7, 8, 10, 11 are the survivors". R18 (`QUALITY.md:102`) supersedes R16, R19 (`:103`) supersedes R13,
   with `bash -n`-clean checks at `:110-157`. Still routed and **not landed**: SCORECARD needs the r31 relabel naming
   `44/44` (`wave2/ScribeQualityFix.md` §5.1; `wave2/CritMistakes.md` O5); CHECK B's h3 tolerance (O4); the lesson's two
   base-state commands lack their `git show b374febb…` qualifier (`wave2/RevGateSpot.md` F1).
5. **`score-gap.py` is `defect` on review** (`wave2/RevScoreGap.md` §Verdict): the census block's `cmd:` "provably
   cannot produce the `census-lane` value it sits above", and the `--selftest` `recheck-mode=stub` fallback crashes
   `KeyError: 'recheck'`. Non-claim item; no score effect; owner is the L1.
6. **Committed census of record is round-20 stale.** `corpus/instruments/README.md:16-18` calls it current;
   `wave2/ExecNoHarmDensity.md` §3c measures `SKILL 55/547 = 10.05%` vs committed `32/506 = 6.32%`, lane
   `388/2263 = 17.15%` vs `134/1480 = 9.05%`. `score-gap.py` quotes the committed figures; the two are not the same
   population (denominator 1480 → 2263).
7. **Twelve `stale-live` statements** (SHONEN numbers, `SKILL.md:1069` counter digest `f926bf75…` that exists in no git
   object, `SCORECARD.md:839` present-tense `43/43`, `corpus/README.md:74-76`, `instruments/README.md:1-3`, and more)
   — `wave2/CritCalibration.md` §2. Only SHONEN's and part of SKILL's prose were refreshed this wave; the SKILL/README
   stale lines were not this round's write paths.
8. **Scope/commit hygiene (report-only).** `wave2/SentScopeFinal.md` F1: "109 fixture files, 52 symlinks and one
   81,802 B raw page … sit beside 69 owned deliverables"; F2: the census dry-run root is 52 symlinks into the live
   corpus; also recorded: six inherited round-29/30 leftovers, the fleet-root `demo-cwd.txt`, and the `E12`-forced row
   placement. `wave2/SentScopeW1.md` F5 records one contradictory in-flight read (straddling the S048 append).

## 8. Artifacts and limits

- **Wave-1 receipts (38):** `.ufo/waves/round-31/wave1/*.md` — chiefly `ExecCounter.md`, `ExecLedgerMerge.md`,
  `ExecRALimbs.md`, `ExecSRLimbs.md`, `ExecFRLimbs.md`, `ExecEntryF15.md`, `ExecRegistryAppend.md`,
  `ExecCapManifest.md`, `ExecCensusDry.md`, `ExecHarnessC2.md`, `ExecScoreGap.md`, `ExecErratumCheck.md`,
  `ScribeErratum.md`, `ScribeLogR30.md`, `ScribeQuality.md`, `ScribeReadmeF15.md`, `ScribeProvince.md`,
  `ScribeInstrReadme.md`, `ScribeSkillGate.md`, `ScribeConsiderthese.md`, `CritC1Kill.md`, `CritC2Kill.md`,
  `RevSourceBar.md`, `RevClaimsFreeze.md`, `ConnSibling.md`, `SentScopeW1.md`, `MutRAExisting.md`,
  `MutSRExisting.md`, `MutFRExisting.md`.
- **Wave-2 receipts (41 + this):** `.ufo/waves/round-31/wave2/*.md` — 13 `ExecLimb*`, 6 `MutCtr*`,
  `ExecCounterFix.md`, `ExecRegressionC1.md`, `ExecCensusFinal.md`, `ExecNoHarmDensity.md`, 6 `Rev*`,
  `CritExpansion.md`, `CritMistakes.md`, `CritCalibration.md`, `ScoutLiveDrift.md`, 2 `Conn*`, `SentScopeFinal.md`,
  `ScribeLesson.md`, `ScribeQualityFix.md`, `ScribeScorecard.md`, `ScribeShonen.md`.
- **Frozen inputs:** `.ufo/waves/round-31/claims.json`, `c1-controls/{before.txt,fake-counter.py,base-instrument-digests.txt}`,
  `c2-controls/before.txt`, `census-before.txt`, `assimilation/`.
- **Limits:** (a) wave-2 edits are uncommitted; every `<LANE_HASH>` is the L1's to fill, and post-commit digests must be
  re-read before the final report cites them (the counter is already known to move within a wave). (b)
  `UNVERIFIED: LOG.md` has no round-31 entry, so the "tied to the LOG entry" requirement is unmet until the L1 appends
  it. (c) `UNVERIFIED: C2's entry clause` is contested (§7.1) — no number changes, but the clause cannot be called met.
  (d) `score-gap.py` and the citation census are open defects, so neither is cited as evidence of quality. (e) This
  receipt's own numbers are a single read at `2026-10-26T00:50Z` on the working tree at `eecad59`; the L1's post-commit
  run is the value of record. (f) `UNVERIFIED: no non-author (outside-lane) verifier` ran this round; every review cited
  here is a lane seat, and `wave2/RevGateSpot.md` labels itself `lane-seat` for that reason.
- **Bounds:** wrote only this receipt; no git/jj mutation, no tool install, no network fetch, no live target contact,
  no fleet-root or sibling-lane write.

## 9. Report trailer

```
Report: .ufo/waves/round-31/wave2/ScribeReportDraft.md
```

This file is the draft report body only. The L1 files the final report at the fleet path; this seat never touches it.
Sections §1–§2 satisfy "Work performed" and "Landed changes"; §3 is "Before → after measurements"; §4 is
"Sources & frontier"; §5 the trend verdicts; §6 the SHONEN lines; §7 the verbatim conflicts the canonical judge rules on.

