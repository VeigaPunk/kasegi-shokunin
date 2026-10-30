# R47SrScorecard — wave-1 scorecard addition

Axes: **depth:verifiability**, **coverage**; depth:density is a non-target guard.

## Filing status and evidence boundary

This is an insertion draft for `SCORECARD.md`, not an integrated result or a verification receipt. The insertion below retains the requested round-end shape, but **all after-values are frozen targets pending the L1's integrated-tree measurement and non-author review**. `<MEASURED-COMMIT>`, `<FINAL-COUNTER-RECEIPT>` and `<NON-AUTHOR-REVIEW>` are explicit filing placeholders, not observed artifacts. Do not file the draft as a completed result until those receipts support its after-values; if they disagree, report their actual readings instead. No production files were edited and no counters, battery, git/jj commands, or other runtimes were invoked by this seat.

Observed provenance: `SCORECARD.md:1776-1810` supplies the established result/table/move-log/counting-command/limits/next-gates shape; `SCORECARD.md:1821-1838` supplies the carried scores 4/8/9 and attempt-2 baseline counts 29/74/66. Frozen claims are `.ufo/waves/round-47/claims.json:9-30` (C1) and `:33-51` (C2). The freeze commit is the assignment-provided `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`; `.ufo/waves/round-47/freeze.txt:1-12` records the base and artifact digests, not that commit's identity.

---

## Round 47 result

Frozen at `.ufo/waves/round-47/claims.json` (freeze commit `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`, base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`). Measured implementation commit: `<MEASURED-COMMIT>`; integrated-tree counter receipt: `<FINAL-COUNTER-RECEIPT>`; independent semantic closure: `<NON-AUTHOR-REVIEW>`. Until those placeholders are replaced with observed evidence, the after column is the frozen target, **not an achieved result**.

| Axis | Score before r47 | Score after r47 | Evidence pointer | Last change |
|---|---:|---|---|---|
| depth:verifiability | 4 | 4 held — measured upon final receipt; routed-defect target 0/11 → 11/11, no promotion claimed | `corpus/instruments/r47-routed-defects.py`; `.ufo/waves/round-47/controls/c1-base.txt:12-13` reads `routed-defects total=11 fixed=0 unresolved=11 exit=1`; target `fixed=11 unresolved=0 exit=0` awaits `<FINAL-COUNTER-RECEIPT>` | r47 (held; measurement pending) |
| coverage | 8 | 8 held — measured upon final receipt; target +1 admitted frontier row, not a coverage-ratio move | `corpus/instruments/r47-f30-gate.py`; `controls/c2-base.txt:8-9` reads `f30-gate fixed=1/7 exit=1`; freeze tree `2/7` per `claims.json:50`; target `7/7 exit=0` and counts 29 → 30 / 74 → 76 / 66 → 67 await `<FINAL-COUNTER-RECEIPT>` | r47 (held; measurement pending) |
| depth:density | 9 | 9 held — non-target guard; no density credit claimed | Frozen targets concern routed defects and F30 admission, not density (`claims.json:9-18,33-42`); no density measurement or byte-identity check is asserted here | r47 (held) |

### Round-47 move-log rows

| Round | Axis | Before | After (target; replace only on measured receipt) | Evidence |
|---|---|---|---|---|
| 47 | depth:verifiability | Routed D5–D8 closure 0/11, unresolved 11; same reading at the freeze tree | 11/11, unresolved 0: SOURCES scaffold removed and original bullets landed; F29 false sentences corrected and spans re-anchored; S076 supersedes S074 with reproducible capture provenance; REST-API lead, ZDI reservation and S068 precision notes recorded | `corpus/instruments/r47-routed-defects.py`; `controls/c1-base.txt:1-13`; `claims.json:13-18,29`; `<FINAL-COUNTER-RECEIPT>`; `<NON-AUTHOR-REVIEW>`; pre-freeze battery `controls/mutbat-receipt.txt:36,58` remains limited, not green |
| 47 | coverage | Frontier 29 (F01–F29), SOURCES 74, knowledge 66 | Frontier 30 (F30 = Zero Day Initiative disclosure policy, third-party broker acquisition-disclosure timeline); SOURCES 76; knowledge 67; S075 `mined`, tier A. S075 is C2's new source; S076 is C1 D7's superseding capture row, not a second C2 admission | `corpus/README.md` F30 admission block; `corpus/SOURCES.md` S075/S076; `corpus/source-snapshots/round-47/S075.txt` and `manifest.json`; `claims.json:36-46`; `<FINAL-COUNTER-RECEIPT>`; `<NON-AUTHOR-REVIEW>` |

Counting commands, one per claim (re-runnable on an export; `<tool-export>` contains the frozen instruments, `<tree>` is the tree under measurement, and `<base-export>` is the frozen base export):

- **C1** — `python3 <tool-export>/corpus/instruments/r47-routed-defects.py --root <tree> --baseline <base-export>` → `routed-defects total=11 fixed=<k> unresolved=<u> exit=<c>`; observed base `fixed=0 unresolved=11 exit=1` (`controls/c1-base.txt:12-13`), same freeze reading (`claims.json:29`); frozen target `fixed=11 unresolved=0 exit=0`.
- **C2** — `python3 <tool-export>/corpus/instruments/r47-f30-gate.py --root <tree>` → `f30-gate fixed=<k>/7 exit=<c>`; observed base `fixed=1/7 exit=1` (`controls/c2-base.txt:8-9`), freeze `2/7` (`claims.json:50`); frozen target `7/7 exit=0`. This is an admission predicate, not a scalar coverage trend.

The do-nothing controls are named explicitly: `controls/c1-base.txt` and `controls/c2-base.txt`; `controls/freeze-check.txt:1-4` replays those readings and records `freeze-check claims=2 base_ok=2 exit=0`. A base that does nothing does **not** satisfy either claim. `controls/selftest-receipt.txt:44-45` records `selftest cases=43 failures=0 exit=0` for the tree probes, including positive fixtures; this is separate from counter-mutant coverage.

The honest counter reading: these are mechanical graders, not semantic witnesses. The pre-freeze battery records C1 **35 mutants / 19 caught / 16 uncaught**, C2 **21 / 3 / 18**, each `equivalent=0 baseline_failures=0 exit=1` (`controls/mutbat-receipt.txt:36,58`). All **34 survivors remain disclosed gaps**, not closed or equivalent; no `uncaught=0` or full mutation-coverage claim is made. A green final counter would not erase those limits. C1 requires the non-author's side-by-side reading of the corrected F29 sentences and S076 body spans, preservation and actual section placement of the landed bullets, and the D8 distinctions. C2 requires live quote location and a non-author admit/reject reading of F30's actionable broker rule and F02/F15 division; a new numbered row alone does not settle overlap (`claims.json:14,18,38,41`). Neither semantic closure has been observed by this scribe.

**Capabilities:** these gates and selftests are counters, not new domain capabilities; no capability addition is evidenced here. **Saturation unchanged:** line 9/10 per owned axis, window N = 3; the lowest non-retired axis stays **depth:verifiability (4)**. Scores remain 4/8/9; no invented promotion criterion or scalar trend is introduced.

### Planned evidence gates for round 48

- `depth:verifiability`: carry forward the round-47 non-author closure's actual routed findings and the 34 disclosed counter-mutant survivors; distinguish a counter repair from a source-chain repair. Freeze each next claim only after documenting its base/freeze readings and do-nothing control; any changed predicate needs its own observed receipts. Do not treat the current tree-probe pass as proof of full mutation coverage or a score-5 audit.
- `coverage`: require the non-author F30 admit/reject and F02/F15 overlap reading before a statement beyond the measured +1 admission count; preserve source attribution (S075 admission versus S076 provenance repair). Select the next frontier only from opened, scoped evidence under the existing quality gates; no F31 admission or 8 → 9 criterion is assumed.

---

## Seat findings and handoff

- **Behavior:** drafted the round-47 insertion only, with explicit unobserved-after labels and filing placeholders; preserved the Round-46 tone, three axes, two move-log rows, two rerunnable counting commands, honest limits, next gates and saturation line.
- **Gates:** read existing receipts only. Do-nothing baseline is red for both claims; the recorded tree selftest is green; the recorded mutation battery is red with 34 survivors. Integrated end-state and semantic gates are unrun by this seat, not passed.
- **Touched surface:** `.ufo/waves/round-47/w1/R47SrScorecard.md` only. No scratch was created, so none remains to remove. No tools were installed or updated.
- **Out of scope:** product integration, counters/fixtures, new executions, live-source review, score promotion, canonical judgment, commits, publishing and adoption into shokuknow.
- **Conflict preserved verbatim from the assignment:** “A seat text asking you to confirm uncaught=0 is superseded by this observed receipt: report the gaps, do not fabricate a pass.” The supplied receipts support that correction.
- **Artifact:** `.ufo/waves/round-47/w1/R47SrScorecard.md` (this file). The L1 must replace filing placeholders with its measured commit and actual counter/semantic receipts, retaining any red outcomes.

Self-evaluation: accuracy 4/5 (after-values explicitly remain targets, not observations); completeness 4/5 (all requested sections supplied, final evidence necessarily L1-owned); clarity 4/5 (status is separated from insertion); actionability 4/5 (two exact export commands and named filing placeholders); conciseness 4/5 (the provenance/status boundary adds length necessary to prevent a false completion claim). Overall 4.0/5. Highest-impact improvement is binding the L1's final receipts, then replacing the conditional after-language with their actual outcomes. Self-check: the user should receive a usable draft, not a fabricated completed scorecard.
