# ScribeLesson — round 34 wave 1 (round lesson)

| field | value |
|---|---|
| seat | `ScribeLesson` (scribe, leaf of the L2 wave) |
| round / lane | kasegi-shokunin round 34 (hyaku run 8, dispatched by `KasegiR34`) |
| lane base | `014ee2d7aa8c3c095ff57ae51097606a9906228c` |
| claims freeze | `29f606dbdd28aff6fd4573ab4b90788bbb90af13` |
| wave-1 dispatch | `206e5108f1190e61b3e2622d21cab8a5d921650c` |
| production path written | `corpus/lessons/round-34.md` (new, 521 lines / 47 679 B) |
| receipt | this file |
| installs / upgrades | **none** (no pacman, no `uv tool`, no `npx`, no binary fetch) |
| git / jj mutations | **none** — `git status`, `git diff`, `git show`, `git log`, `git archive` reads only; no `jj` command of any form |
| scratch | `/fast/scratch/hyaku/kasegi-r34/ScribeLesson/` (base export + 8 captured outputs), **removed before yield**; see §7 |
| fleet root / shokuknow | read-only; no write, no campaign tool run (see §6) |

## Report

### 1. What was composed and from what

`corpus/lessons/round-34.md` carries the seven required sections plus a provenance section:
header (revisions, shape, receipt coverage, answering-model note), `## Frozen claims — before → after`,
`## Gate`, `## Mistakes`, `## considerthese`, `## Census before → after`, `## No-harm`,
`## Open items / unverified`, `## Touched surfaces and provenance`. Every claim's after-value names
either (a) a wave receipt with its section, or (b) one of this seat's own runs quoted below with its
exit code and digest. Receipts read in full: `ExecRDefectClosureSuite`, `ExecCaptureBindingHarden`
(headings + §2/§4), `ExecKillRuleCheck` (headings), `ExecManifestR32Normalize` (headings), `ExecS040Orphan`
(headings), `ExecFrontierBidirectional` (headings), `ExecRegistryAppend` (headings), `ExecSnapshotR34`
(headings), `ExecLessonErrata` (headings), `ExecErratum2`, `ExecQualityAppends`, `ExecScorecardMarkers`,
`ExecHarnessAfter` (headings), `ExecDoNothingReject`, `ExecBeforeReceipts` (headings), `ExecCensusAfter` (§1–§2),
`RevC1BeforeAfter`, `RevC2BeforeAfter`, `RevEntryF17`, `RevRowS051`, `RevClaimsFreeze` (headings), `RevErrata`
(§0–§3), `RevNoHarm`, `RevCensus` (headings), `RevJunkTwin` (verdict), `RevManifestR32` (headings), `RevOrphan`
(headings), `RevRSuite` (headings), `MutC2Entry`, `MutRSuiteChecks` (table), `MutFrontierRuleA` (§5–§6),
`MutKillRuleMutants` (headings), `MutSelftestSummary` (headings), `MutManifestField` (headings),
`MutCaptureBindingLimbs` (headings), `CritC1Kill`, `CritC2Kill`, `CritOverclaim`, `CritMistakes`,
`ScoutImmunefiLive`, `ScoutDatawalk`, `ScoutQuarantine` (headings), `ScoutPackageThemes` (headings),
`ScoutSiblingSweep` (headings), `ScribeAssimilationGate` (§Gate block + R1–R5), `ScribeEntryF17` (headings),
`ScribeSOURCESRow` (headings), `ScribeSearchLog` (headings), `ScribeSkillGate` (headings), `ScribeQualityDraft`
(headings), `SentCred` (verdict), `SentScopeFinal`, `ConnClaims` (headings), `ConnCrossCheck` (headings),
`ConnSibling` (headings). Headings-only reads are stated in the lesson where a number depends on them.

### 2. Frozen-state verification (before the composition batch)

```
$ sha256sum .ufo/waves/round-34/claims.json
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json   (9004 B)
$ sha256sum .ufo/waves/round-34/census-before.txt .ufo/waves/round-34/c1-controls/before.txt \
            .ufo/waves/round-34/c2-controls/before.txt
d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0  (census-before.txt)
d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0  (c1-controls/before.txt)
d90ce017049b99d447ae6f68be0104b11f406d11799557b0f318fa51748db5f0  (c2-controls/before.txt)
$ sha256sum .ufo/waves/round-34/claims-erratum-1.md
6a3cd99e4dc9411293d9fa7b9cb3bb00473598b63ba31359be8c66c88f6bd1bd
$ stat -c '%y' .ufo/waves/round-34/claims-erratum-1.md
2026-10-26 02:36:22.079795631 -0300        # freeze commit committer time 02:28:39 → +7m43s
$ git cat-file -e 014ee2d7aa8c3c095ff57ae51097606a9906228c && git cat-file -e 29f606dbdd28aff6fd4573ab4b90788bbb90af13 \
  && git cat-file -e 206e5108f1190e61b3e2622d21cab8a5d921650c ; echo $?      -> 0
$ python3 -c "...wave1-spec.json..."        -> items=65; roles executor 19, reviewer 13, scribe 10,
                                               mutation-tester 7, scout 5, critic 5, connector 3,
                                               sentinel 2, simplifier 1
$ python3 -c "...wave1-dispatch.json..."    -> schema=ufo-swarm-wave-dispatch-v1, wave=kasegi-r34-build,
                                               counts={spawn:65, resume:0, total:65}, policy.maxLanes=128
```

Three findings recorded in the lesson from this block: the three "before" files are **one** capture
copied three times (`d90ce017…`); the erratum was filed **7m43s after** the freeze commit; and the
spec's 65 items match the dispatch's 65 spawns.

### 3. Composition batch — C1 counters (the claim's own commands)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ                                   -> 2026-10-26T05:48:55Z (first), 05:54:57Z (last)
$ bash corpus/instruments/r-defect-closure.sh ; echo "plain_exit=$?"
R1 … R9  (nine `check=… open=0` lines)
closed=9/9 exit=0
plain_exit=0
$ bash corpus/instruments/r-defect-closure.sh --selftest ; echo "selftest_exit=$?"
selftest case=R1 live=pass fixture=rejected verdict=pass   (… R2–R9 identical)
selftest cases=9 failures=0
selftest_exit=0
$ python3 corpus/instruments/kill-rule-check.py ; echo "kill_exit=$?"
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
kill_exit=0
$ python3 corpus/instruments/capture-binding-check.py --selftest ; echo "cbb_self_exit=$?"
23 `selftest case=… verdict=pass` lines
selftest cases=23 failures=0
cbb_self_exit=0
$ python3 corpus/instruments/capture-binding-check.py ; echo "cbb_exit=$?"
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
cbb_exit=0
$ grep -c '<LANE_HASH>' SCORECARD.md ; echo "grep_exit=$?"       -> 0 / grep_exit=1
```

Digest drift inside the composition window (recorded in the lesson, because it makes any undigested
after-value unfalsifiable): `r-defect-closure.sh` `0beafed2…` → `357a7e49…` → **`2a635bf5…`**;
`kill-rule-check.py` `7a20e724…` → **`c279d952…`** (plain-run gate count 6 → 7);
`SCORECARD.md` `b8fc8c66…` → **`efa646c8…`** when `ScribeScorecard` appended the round-34 section.

### 4. Composition batch — C2 counters, census and Gate material

```
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                                                    -> 17
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                          -> 51
$ grep -cE '^\|[[:space:]]*S051[[:space:]]*\|' corpus/SOURCES.md                                -> 1
$ grep -lE '^source: S051 ' corpus/knowledge/*.md | wc -l                                       -> 1
$ ls corpus/knowledge/*.md | wc -l                                                              -> 46
$ python3 corpus/instruments/frontier-recheck-count.py ; echo "harness_exit=$?"
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0
harness_exit=0
$ grep -c 'PASS F17 ids=S051' <harness output> ; echo "grep_exit=$?"                            -> 0 / grep_exit=1
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-34/manifest.json --source S051
S051:sha256 OK + 18 assertions OK   (Q9 occurrences=2 anchor=77-ok; Q17 occurrences=2 anchor=96-ok)
recheck_exit=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
$ grep -n 'simplified 5-level scale' corpus/source-snapshots/round-34/S051.txt   -> 46:At Immunefi, we classify bugs on a simplified 5-level scale:
$ grep -c 'Direct theft of any user funds, whether at-rest or in-motion, other than unclaimed yield' … -> 1  (line 75)
$ git diff --stat 7963976e 014ee2d -- corpus/source-snapshots corpus/instruments corpus/SOURCES.md
(no output) ; diff_exit=0        # base and freeze audit surfaces are identical → `records=40` was true at base only
$ grep -nE '^\| R2[0-9] \||^Note \(round 34\)' corpus/QUALITY.md
169 R20 · 170 R21 · 220 Note (round 34) · 226 R22 · 227 R23 · 228 R24
$ grep -n 'Erratum (round 34)' corpus/lessons/round-33.md   -> 140 (R7) and 215 (R4)
$ grep -n 'Erratum 2, disclosed|Pre-freeze satisfiability step|Correction (round 34)' SCORECARD.md
1014 / 1028 / 1116
```

Quiescence is **not** claimed: receipts were still landing during composition (53 → 57 → 59 → 61 files
at `05:48:55Z` / `05:56Z` / `05:58Z` / `05:59Z`), and `ExecNoHarmFinal`, `ExecRegressionC1`,
`ScribeShonen`, `ScribeReportDraft`, `SimplifierCleanup` were still absent at the last count. One
receipt is filed as `ScribeReportDraft-2.md` while the spec name is `ScribeReportDraft`; the lesson
states the name drift rather than repairing it.

### 5. No-harm batch (this seat's own, since no no-harm receipt had landed)

```
$ python3 corpus/instruments/density.py SKILL.md               -> mean dens 201.7; 710 cites / 25 blocks; exit=0
$ python3 corpus/instruments/anchorcheck.py SKILL.md           -> 12 in-range, 0 bad; LOST-RECORDED=306;
                                                                  PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0; exit=0
$ (base tree) git archive 014ee2d | tar -x -C $S/base
$ (base tree) python3 corpus/instruments/density.py SKILL.md   -> mean dens 201.7; 710 / 25
$ (base tree) python3 corpus/instruments/anchorcheck.py SKILL.md -> 12 in-range, 0 bad; LOST-RECORDED=306; all classes 0
$ git diff --numstat 014ee2d -- SKILL.md PROVINCE.md LOG.md SCORECARD.md corpus/ | sort -k3
31	3	SCORECARD.md
487	87	corpus/instruments/capture-binding-check.py
220	15	corpus/instruments/frontier-recheck-count.py
291	0	corpus/instruments/README.md
74	0	corpus/lessons/round-29.md
109	0	corpus/lessons/round-33.md
15	0	corpus/QUALITY.md
26	0	corpus/README.md
5	0	corpus/SOURCES.md
12	1	corpus/source-snapshots/round-26/manifest.json
3	3	corpus/source-snapshots/round-32/manifest.json
# SKILL.md, PROVINCE.md, LOG.md absent → 0 changes; deletions total 109 across 5 files
$ git status --porcelain   (extract)
 M .ufo/waves/round-33/wave1/ScribeReportDraft.md
 M SCORECARD.md … M corpus/source-snapshots/round-32/manifest.json
?? corpus/instruments/{kill-rule-check.py,r-defect-closure.sh}
?? corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
?? corpus/source-snapshots/round-34/
?? selftest-baseline.txt
```

Unowned writes on disk at composition: lane `selftest-baseline.txt` (1552 B, `ca3759d1…`, `02:37:05`);
fleet root `baseline-plain.txt` (850 B, `56f08a92…`, `02:37:04`; both attributed to one `RevKillRule`
transcript by `wave1/SentScopeFinal.md` §1 A1); ` M .ufo/waves/round-33/wave1/ScribeReportDraft.md`
(37/0 append); four jj working-copy snapshots (`SentScopeFinal` §2 B2) against one receipt that claims
none (`RevErrata.md:12,153`). Sentinels: fleet root **FAIL (1 file)**, lane git/jj **FAIL**, shokuknow
**PASS**, scratch **PASS at snapshot**.

### 6. Scope compliance

- Wrote exactly two lane paths: `corpus/lessons/round-34.md` and this receipt. No other lane file edited.
- No `git add/commit/push`, no `git checkout/reset`, **no `jj` command at all** (so no working-copy
  snapshot — `SentScopeFinal`'s B2 class does not apply to this seat).
- Fleet root `/home/vgpnk/Projects/shokunin`: read-only (`git status`, `git diff`, `git show`, `git log`,
  `scripts/sources-census.sh validate` which writes nothing without `--out`).
- `/home/vgpnk/Projects/shokuknow`: never written; none of `renumber-staged.py`, `merge-plan.py`,
  `quote-lint.py`, `absent-defect-register.py` was run.
- No subagents, no wave dispatch, no `agent://all`; one inbound `CloseTabiR29` broadcast was explicitly
  misaddressed to another lane's seats and needed no action.

### 7. Scratch cleanup

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/ScribeLesson && ls -d /fast/scratch/hyaku/kasegi-r34/ScribeLesson ; echo "exists_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/ScribeLesson': No such file or directory
exists_exit=2
```

Contents removed: `base/` (a `git archive 014ee2d` export used for the before-column density/anchorcheck
runs) and the captured outputs `suite.out`, `suite-self.out`, `kill.out`, `cbb.out`, `cbb-self.out`,
`harness.out`, `recheck.out`, `census.out`, `parse.py`. **No tree left on disk.**

### 8. Digests

```
73b8bdbb400f83903113c9372984120001bfdc2f56d4b6a95b73b1c6ca14014c  corpus/lessons/round-34.md   (521 lines / 47679 B)
2a635bf5  corpus/instruments/r-defect-closure.sh          c279d952  corpus/instruments/kill-rule-check.py
3d9e5e0d  corpus/instruments/capture-binding-check.py    1be79af6  corpus/instruments/frontier-recheck-count.py
efa646c8  SCORECARD.md      77d99df9  corpus/QUALITY.md    4c85ff86  corpus/SOURCES.md
876be9cc  corpus/README.md  f69472f3  corpus/lessons/round-33.md
72ab4e68  round-32/manifest.json   d5077f81  round-34/manifest.json   33ac33c3  round-26/manifest.json
948b202e  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
2752a994  .ufo/waves/round-34/c2-controls/junk-f17.md
dedb9ea8  .ufo/waves/round-34/claims.json        6a3cd99e  .ufo/waves/round-34/claims-erratum-1.md
```

### 9. Findings for the L1 (no verdicts claimed; this seat is not a judge)

1. **`LANDED_HASH_PENDING`** in the lesson header is yours to fill; nothing else is a placeholder.
2. **Two contested items are reported verbatim, not resolved**: the junk-twin rejection limb
   (`RevJunkTwin` holds vs `CritOverclaim` F1/F1b + `CritC2Kill` G5 + `ScoutDatawalk` F-1/F-1b) and the
   `records=41` literal (`claims-erratum-1`).
3. **Provisional mistake rows M34-3, M34-5, M34-6** need a separate appended erratum before any surface
   cites those ids; M34-4 is minted from the author seat's own disclosure. `QUALITY.md:226` currently
   grounds R22 on M34-2 (the marker defect) — `CritMistakes` F7 says M34-3 is the right grounding.
4. **Re-run the three C1 commands at quiescence and quote them with committed digests** (`CritOverclaim`
   F3: `closed=8/9` at `05:38Z` vs `9/9` at `05:40Z`; two of the three digests moved again during this
   receipt's own composition).
5. **Strays must not ride into the integration commit**: lane `selftest-baseline.txt`, fleet
   `baseline-plain.txt`. Deleting the lane one is safe for `RevC1BeforeAfter.md:37` (the 23-case count is
   quoted inline there).
6. **C1 gaps (4 routes + R1 spelling) and C2 gate gaps G1–G5** are named in the lesson's § Open items;
   neither claim is cited as an increase, both are recorded held.
7. **Anchor drift deepened** by +2 on the `SOURCES.md:83` trail (`RevRowS051` §7); routed to
   `corpus/lessons/**`, not fixed here.

Report: .ufo/waves/round-34/wave1/ScribeLesson.md
