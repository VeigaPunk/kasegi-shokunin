# ConnClaims — round 34, wave 1 (R1–R9 cross-index)

Seat: `ConnClaims` (connector/leaf), lane `kasegi-shokunin`, round 34 (hyaku run 8).
Assignment: cross-index the nine round-33 verifier-routed defects R1–R9
(`corpus/lessons/round-33-verifier-spotcheck.md` §5) to their landed fixes — for each,
the fix artifact (file/line), the closure check in `corpus/instruments/r-defect-closure.sh`,
and the receipt that proves it; flag any defect with no fix, no check, or no receipt;
connect R2/R3/R7 to the appended errata; confirm the pre-freeze satisfiability step is recorded.

Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`;
HEAD at measurement `206e510` (wave-1 work uncommitted in the working tree; the L1 commits).
No git/jj mutation, no write outside the lane, no subagent, no tool installed.
Scratch: `/fast/scratch/hyaku/kasegi-r34/ConnClaims/` (removed before yield — §8).

## Verdict

**Coverage complete: all nine defects R1–R9 are mapped to a landed fix artifact, a runnable
closure check, and at least one proving receipt. No defect has a missing fix, a missing check,
or a missing receipt.** R2/R3/R7 are each connected to an appended erratum, and the pre-freeze
satisfiability step is recorded on two surfaces (QUALITY.md R22 row + SCORECARD.md round-33
paragraph). Fresh re-execution of the suite and its counters on the current working tree is
green (`closed=9/9 exit=0`; `--selftest cases=9 failures=0`; base tree `closed=0/9 exit=1`;
`capture-binding-check.py --selftest cases=23 failures=0`; `kill-rule-check.py survivors=0`).

## Report

### 1. Fresh verification runs (this seat, 2026-10-26 ~06:05–06:12Z)

Plain run against the working tree:

```
$ bash corpus/instruments/r-defect-closure.sh ; echo "PLAIN_EXIT=$?"
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (selftest case= per case, cases>=11) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc strict UTC (^YYYY-MM-DDTHH:MM:SSZ$), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
PLAIN_EXIT=0
```

Selftest (the scratch base dir must pre-exist; the suite errors `scratch-missing` exit 2 otherwise —
a harness behaviour, not a defect):

```
$ mkdir -p /fast/scratch/hyaku/kasegi-r34/ConnClaims/selftest-scratch
$ bash corpus/instruments/r-defect-closure.sh --selftest --scratch /fast/scratch/hyaku/kasegi-r34/ConnClaims/selftest-scratch ; echo "SELFTEST_EXIT=$?"
selftest case=R1 live=pass fixture=rejected verdict=pass
selftest case=R2 live=pass fixture=rejected verdict=pass
selftest case=R3 live=pass fixture=rejected verdict=pass
selftest case=R4 live=pass fixture=rejected verdict=pass
selftest case=R5 live=pass fixture=rejected verdict=pass
selftest case=R6 live=pass fixture=rejected verdict=pass
selftest case=R7 live=pass fixture=rejected verdict=pass
selftest case=R8 live=pass fixture=rejected verdict=pass
selftest case=R9 live=pass fixture=rejected verdict=pass
selftest cases=9 failures=0
SELFTEST_EXIT=0
```

Base-tree run (closure semantics: every check exits non-zero while its defect is open), base
exported read-only via `git archive 014ee2d` into scratch:

```
$ bash corpus/instruments/r-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r34/ConnClaims/base-tree ; echo "BASE_EXIT=$?"
R1 check=SCORECARD.md lane-hash-markers=2 open=1
R2 check=no 'Erratum 2' block in SCORECARD.md open=1
R3 check=no appended 'Note (round 34)' below R20 open=1
R4 check=tightened kill-rule requirement not recorded (...) open=1
R5 check=misnamed selftest case 'url-matching-two-rows' still present (count=2) open=1
R6 check=round-26 manifest has no S040-live.txt record and no orphan list open=1
R7 check=round-33 lesson has no appended R7 erratum open=1
R8 check=round-32 manifest carries a non-UTC fetched_utc open=1
R9 check=capture-binding H4-H8 cases missing: per-file-orphan-detected ... summary-only-selftest-rejected open=1
closed=0/9 exit=1
BASE_EXIT=1
```

Claim counters on the current working tree:

```
$ python3 corpus/instruments/capture-binding-check.py --selftest | tail -1 ; echo "CB_EXIT=$?"
selftest cases=23 failures=0            # N=23 >= 19  ✓
$ python3 corpus/instruments/kill-rule-check.py | tail -3 ; echo "KILL_EXIT=$?"
mutants=3 killed=3 survivors=0 invalid=0
gates=6 failed=0
survivors=0                             # ✓
$ grep -c '<LANE_HASH>' SCORECARD.md ; echo "grep_exit=$?"
0                                       # ✓ (grep exit 1, count 0)
```

### 2. Coverage table — R1..R9, all nine mapped

Closure-check line anchors are in `corpus/instruments/r-defect-closure.sh`
(`check_r1` .. `check_r9`; header table at the file's top documents each predicate).

| Defect | Fix artifact (file:line) | Closure check | Receipt proving the fix | Verdict |
|---|---|---|---|---|
| **R1** `<LANE_HASH>` placeholders | `SCORECARD.md:988` + `:1110` (both markers replaced with `7963976e60b…`, count 0) and appended `Correction (round 34)` block at `SCORECARD.md:1116-1119` naming `7963976e` and lane tip `014ee2d` | `check_r1` — marker count 0 AND correction block names both hashes | `wave1/ExecScorecardMarkers.md` (before count=2 at `:988/:1087`, after 0; `git rev-parse` hash proof); reviewer `wave1/RevErrata.md` §2 **PASS** | fix ✓ check ✓ receipt ✓ |
| **R2** frozen kill-rule unsatisfiable | `SCORECARD.md:1014-1027` (`**Erratum 2**` block, inside `## Round 33` at `:982`, before `## Round-33 capabilities` at `:1097`) restating the parenthetical per id (`0 or 2+`, `multi_row_url`, `dup-id`); pre-freeze step recorded `SCORECARD.md:1028-1035` + `corpus/QUALITY.md:226` (`| R22 |` row) | `check_r2` — Erratum 2 inside round-33 section AND R22 row states satisfiability + pre-freeze | `wave1/ExecErratum2.md` (21 added/0 removed lines, block sha `9b413f41…`, post-state sha `b8fc8c66…`); `wave1/ExecQualityAppends.md` (R22 row); reviewer `wave1/RevErrata.md` §3 **PASS** | fix ✓ check ✓ receipt ✓ |
| **R3** QUALITY R20 "exactly one" reading | `corpus/QUALITY.md:220-222` `Note (round 34)` appended below the R20 row (`:169`), stating the per-id reading supersedes "exactly one registry-row URL" and citing erratum 2 | `check_r3` — note below R20 names R20 + quotes "exactly one" + `supersed` + per-id | `wave1/ExecQualityAppends.md` (R6-form append, lines 214-228, pre-sha `00781e09…`); reviewer `wave1/RevErrata.md` §4 item 3 **PASS** | fix ✓ check ✓ receipt ✓ |
| **R4** "all mutants killed" overstatement + weak kill rule | `corpus/QUALITY.md:228` (`| R24 |` row: kill rule tightened to one `selftest case=` verdict line per case, cases>=11); `corpus/lessons/round-33.md:215-247` appended R4 erratum (3-of-4 figure, mutant table, overstatement correction); instrument `corpus/instruments/kill-rule-check.py` (survivor counter) | `check_r4` — R24 row binds `kill rule`+`selftest case=`+per-case AND lesson R4 erratum appended after the `## Touched surfaces` anchor (`:136`) carries 3-of-4 + mutant + overstatement tokens | `wave1/ExecQualityAppends.md` (R24); `wave1/ExecLessonErrata.md` (`+109 −0` on the lesson, R4 heading at `:215`); `wave1/ExecKillRuleCheck.md` (counter contract, controls); fresh `kill-rule-check.py` → `survivors=0` | fix ✓ check ✓ receipt ✓ |
| **R5** misnamed selftest case | `corpus/instruments/capture-binding-check.py:679` — the dup-id fixture case now registered as `duplicate-id-rows`; `url-matching-two-rows` count 0; 21 case tuples (>=11) | `check_r5` — no `url-matching-two-rows` AND >=11 `("name",` tuples | `wave1/ExecCaptureBindingHarden.md` (whole-instrument hardening, post-sha `3d9e5e0d…`, selftest 23 cases incl. `duplicate-id-rows`); mutation evidence `wave1/MutCaptureBindingLimbs.md` | fix ✓ check ✓ receipt ✓ |
| **R6** S040-live.txt orphan | `corpus/source-snapshots/round-26/manifest.json` — top-level `orphans` list declaring `S040-live.txt` (path + non-empty reason + sha256 `b7f7b55f…` + `row: S040` + `captured_url` + strict-UTC `fetched_utc 2026-10-25T12:34:27Z`); `purpose` rewritten to name the two files and drop the false "skipped" text | `check_r6` — record path match or orphan list entry for `S040-live.txt` AND purpose names S040 without "skipped this round" | `wave1/ExecS040Orphan.md` (option (b) rationale: stem-mismatch vs no-row collision documented; schema handoff with `ExecCaptureBindingHarden`); reviewer `wave1/RevOrphan.md` **PASS** (orphan sha256 matches file bytes; instrument rule A2 cases pass) | fix ✓ check ✓ receipt ✓ |
| **R7** char-count / line-cite slips | `corpus/lessons/round-33.md:140-…` appended `Erratum (round 34) — R7` block: 19→31 and 23→22 characters with producing `printf | wc -m` commands (31/22; 33/24 with 「」), and the `S050.txt:69`→`:70` sentence correction with `sed -n '69,71p'` evidence + full citation sweep table | `check_r7` — appended R7 erratum after the anchor with 19→31, 23→22, `S050.txt:70` | `wave1/ExecLessonErrata.md` (producing commands, occurrence binding `grep -cF` → 1 each); reviewer `wave1/RevErrata.md` §4 item 4 **PASS** | fix ✓ check ✓ receipt ✓ |
| **R8** local-offset `fetched_utc` | `corpus/source-snapshots/round-32/manifest.json` — `S049 fetched_utc 2026-10-26T04:16:06Z`, `S050 2026-10-26T04:16:16Z` (both strict UTC, Z-suffix, no offset); purpose clause replaced to state they are verification re-open instants | `check_r8` — every `fetched_utc` matches `^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` with no `[+-]HH:MM` offset | `wave1/ExecManifestR32Normalize.md` (exactly three cells changed; ground truth from `round-33/wave1/ScoutLiveDrift.md` fetch lines); reviewer `wave1/RevManifestR32.md` **PASS** (freeze-vs-tip diff, source-recheck S049/S050 exit 0) | fix ✓ check ✓ receipt ✓ |
| **R9** H4–H8 blind spots + one-directional rule A + no junk twin | (a) `corpus/instruments/capture-binding-check.py` carries the nine H4–H8 case names (`per-file-orphan-detected/listed`, `nested-snapshot-dir`, `fetched-utc-pending-rejected`, `fetched-utc-local-offset-rejected`, `dup-record-in-manifest`, `double-https-row`, `rejected-row-anchor`, `summary-only-selftest-rejected`); (b) `corpus/instruments/frontier-recheck-count.py` rule A bidirectional — new reverse limb `selection-not-declared-by-entry`, `cited` now excludes `source:`/`recheck:` lines; (c) junk twin at `.ufo/waves/round-34/c2-controls/junk-f17.md` | `check_r9` — nine case names present AND rule A proved behaviourally (mirror fixture exit 0, reverse fixture exit 1) AND junk twin exists | `wave1/ExecCaptureBindingHarden.md` (H4–H8 cases + hardening); `wave1/ExecFrontierBidirectional.md` (+214/−15, mirror/reverse proof, base-tool contrast); junk-twin rejection `wave1/RevC2BeforeAfter.md` §8 (shape counters 3/3 pass it — the counter gap — but the admission gate rejects: fabricated quote `quote-not-found` exit 1 on a control manifest, no `corpus/knowledge/` path, no README/SOURCES row); corroborated by `wave1/ExecHarnessAfter.md` §F-B and `wave1/ScoutDatawalk.md` F-1 | fix ✓ check ✓ receipt ✓ |

### 3. Errata connections and the pre-freeze satisfiability step

- **R2 → Erratum 2** (`SCORECARD.md:1014-1027`): restates the frozen kill-rule parenthetical
  "0 or 2+ matches = failure" scoped **per id**, names `multi_row_url` and `dup-id`, and pins
  the landed reading (`records=40 bound=40 unbound=0` vs the literal `bound=38`). The same
  block cites erratum 1 as the correction of record. This is the round-34 append the frozen
  C1 after-column requires ("erratum 2 appended in the round-33 section restating the per-id
  parenthetical").
- **R3 → QUALITY note + erratum 2**: the `Note (round 34)` at `corpus/QUALITY.md:220-222`
  explicitly cites "the C1 erratum-2 per-id reading" as the superseding authority for R20's
  "exactly one registry-row URL" sentence — so R3's correction is anchored to the same erratum
  substance as R2, on the record surface R20 lives on.
- **R7 → lesson erratum**: `corpus/lessons/round-33.md:140` appended `Erratum (round 34) — R7`
  carries both limbs (counts and the `S050.txt:70` sentence cite) with producing commands,
  matching the R7 closure check token-for-token.
- **Pre-freeze satisfiability step — recorded, two surfaces**: (1) `corpus/QUALITY.md:226`
  `| R22 |` criterion row ("checked for satisfiability against base bytes before freeze … an
  unsatisfiable literal is fixed before data, never waived by a post-freeze erratum",
  grounded in R2 and M34-2); (2) `SCORECARD.md:1028-1035` paragraph "Pre-freeze satisfiability
  step, recorded (QUALITY R22)" naming the two round-33 unsatisfiable literals. Confirmed.

### 4. Observations (named, none blocking)

1. **Junk-twin path precision.** The C1/C2 claims say "under `c2-controls/`"; the landed twin is
   at `.ufo/waves/round-34/c2-controls/junk-f17.md` (the round-34 wave controls directory, beside
   `c1-controls/`), not a repo-root `c2-controls/`. `check_r9` accepts either path and prints the
   resolved one (`junk=.ufo/waves/round-34/c2-controls/junk-f17.md`). The rejection evidence is
   independent of location. No defect; recorded so the judge reads the claim against the right path.
2. **`kill-rule-check.py` in-flight digest drift.** `wave1/ExecKillRuleCheck.md` pins the counter
   at sha256 `e33a300f…`; the current working-tree bytes hash to `7a20e724…` (file mtime 02:43:37
   is after that receipt's 02:41:52 — a sibling seat ran its patcher against the file after the
   author yielded). The C1 counting command on the **current** bytes still prints
   `survivors=0`, all six gates ok (§1). The L1 should confirm the bytes at commit time; the R4
   closure check re-reads the file live and passes.
3. **R6 disposition.** The fix chose the spotcheck's remedy (b) — explicit orphan declaration —
   over (a) adding a `sources` record, for reasons documented in `ExecS040Orphan.md`
   (`source-recheck.py` stem-mismatch vs `capture-binding` no-row). The C1 claim text allows
   either ("manifest record or orphan listing"); satisfied.
4. **Suite authorship receipt.** `wave1/ExecRDefectClosureSuite.md` is the suite's own seat
   receipt (plain 9/9, selftest 9/9, base 0/9, fake-suite discrimination, R9 mirror/reverse
   base-vs-landed contrast). My §1 runs independently reproduce those results on the current tree.

### 5. File digests (working tree at measurement, sha256)

```
0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1  corpus/instruments/r-defect-closure.sh
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
7a20e724659ffa35ccce2f5072232c409e7b79d2e33fda878b5589c989d697f1  corpus/instruments/kill-rule-check.py   (in flight; receipt pins e33a300f…)
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa  corpus/source-snapshots/round-26/manifest.json
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md
```

### 6. Receipt inventory used (all under `.ufo/waves/round-34/wave1/`)

ExecRDefectClosureSuite.md (suite author), ExecScorecardMarkers.md (R1), ExecErratum2.md (R2),
ExecQualityAppends.md (R3 note + R22 + R24), ExecLessonErrata.md (R4 + R7 errata),
ExecCaptureBindingHarden.md (R5 rename + R9 H4–H8 cases + summary-only rejection),
ExecS040Orphan.md (R6), ExecManifestR32Normalize.md (R8), ExecFrontierBidirectional.md (R9 rule A),
ExecKillRuleCheck.md (R4 counter), RevErrata.md (R1/R2/R3/R7 reviewer PASS),
RevManifestR32.md (R8 reviewer PASS), RevOrphan.md (R6 reviewer PASS),
RevC1BeforeAfter.md (independent C1 before/after), RevC2BeforeAfter.md §8 (junk-twin rejection),
MutCaptureBindingLimbs.md + MutSelftestSummary.md (limb/summary mutants), ScoutDatawalk.md (F-1).

### 7. No writes outside scope; no commits

Only this receipt was written (lane path `.ufo/waves/round-34/wave1/ConnClaims.md`). No git/jj
mutation; no fleet/shokuknow/sibling-lane access; no subagent dispatch; no `agent://all`.

### 8. Scratch cleanup

`/fast/scratch/hyaku/kasegi-r34/ConnClaims/` (base-tree export, selftest scratch, capture-binding
scratch) removed before yield:

```
$ rm -rf /fast/scratch/hyaku/kasegi-r34/ConnClaims && test ! -e /fast/scratch/hyaku/kasegi-r34/ConnClaims && echo "scratch gone"
scratch gone
```
