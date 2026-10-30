# R47SrLesson — wave-1 lesson draft

## Behavior and artifacts

Draft for L1 integration: `.ufo/waves/round-47/w1/R47SrLesson.draft/round-47.md` (destination `corpus/lessons/round-47.md`; destination not edited).

Axes: depth:verifiability and coverage. Draft includes H1, attempt-3 state, requested freeze-commit placeholder with supplied replacement hash, five mistake rows, eight manifest-located Gate quotes, candidate rejects with flips, present-S075 reservation discharge, exact S068 `one GHSA advisory entry` note, S074 old→new cells, and unfilled non-author spot-check slots. D6 dropped-finding paths use actual attempt2 wave1/wave2 locations supplied by L1, not the erroneous wave2 ConnPatterns fixture pointer.

## Gates and evidence

No shell command, counter, network fetch, battery, build, or test was executed by this scribe. Evidence was read through `read`/`grep`; artifacts created by `write`, corrected with `edit`. No second runtime, delegation, background job, install, git/jj mutation, or scratch fixture was used. No scratch directory was created, so no scratch artifact remains to remove.

Exact observed stored outputs, not rerun results:

- `.ufo/waves/round-47/controls/c1-base.txt:1-13`: eleven red limbs; `routed-defects total=11 fixed=0 unresolved=11 exit=1`, `EXIT=1`.
- `controls/c2-base.txt:1-9`: `f30-gate fixed=1/7 exit=1`, `EXIT=1`.
- `controls/freeze-check.txt:1-4`: names both base readings, `freeze-check claims=2 base_ok=2 exit=0`.
- Do-nothing controls explicitly named by `controls/freeze-controls.txt:1`; fixture successes do not establish an integrated-tree pass.
- `controls/selftest-receipt.txt:44-45`: `selftest cases=43 failures=0 exit=0`, `EXIT=0`.
- `controls/mutbat-receipt.txt:36,58`: C1 `mutants=35 caught=19 equivalent=0 uncaught=16 baseline_failures=0 exit=1`; C2 `mutants=21 caught=3 equivalent=0 uncaught=18 baseline_failures=0 exit=1`. All 34 survivors remain disclosed gaps, not pass/equivalence claims.
- `corpus/source-snapshots/round-47/manifest.json:7-23,30-74`: S075 URL, HTTP 200, UTC capture 2026-10-30T10:35:37Z, digest, body range, and eight Gate quote anchors. Quotes were read with source context `S075.txt:20-27`; no fresh network opening is claimed.
- `corpus/lessons/round-46-verifier-spotcheck.md:179-215`: D5–D8 source evidence; `:229-241` preserves historical trade reconciliation.
- Fleet `.ufo/watchdog.log:1955,1964-1965`: attempt-1 report failure, attempt-2 parse error/no spawn, attempt-3 launch. Initial read of lane `.ufo/watchdog.log` returned `Path not found`; resolved by reading fleet log, without writing there.

Counter commands retained as non-author/L1 integration checks, NOT executed here:

`python3 corpus/instruments/r47-routed-defects.py --root <tree> --baseline <base-export>`

`python3 corpus/instruments/r47-f30-gate.py --root <tree>`

Plain measures and exact D5 byte/section re-derivation are listed in the draft's closure slots. Full mutation battery must not be rerun merely for this report.

## Findings and limits

1. S074 exact frozen transition is status `mined → rejected`, used-by `corpus/knowledge/github-repository-security-advisories.md → corpus/lessons/round-46.md`; recheck `90d → 90d`. Full contract read from `claims.json:13`; draft reflects it and labels it integration contract, not observed landing.
2. ZDI is admitted at current S075: the old reservation is discharged, never reassigned. S076 is a different, superseding F29 capture.
3. REST sibling pointer resolves to `corpus/source-snapshots/round-47/S076.txt:574`; API document itself is still a lead, not an opened/admitted source.
4. Round-47 new mistake is witnessed attempt-1 landing failure; the watchdog's `FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B)` remains a disjunction, not a fabricated diagnosis.
5. F02 overlap remains independent semantic review, not closed by row count or a counter pass. Considerthese dispositions remain historical documentary statuses, not re-measured executions.

Out of scope: product/production edits; final integration, commit/push/publish/adoption; fleet or sibling-lane changes; report landing; scores/judgment; final no-harm result; non-author closure. No tool installed or updated.

## Self-evaluation (not a gate)

Accuracy 4/5 — exact receipts and scoped claims, but no independent live re-open (explicitly left to closure). Completeness 4/5 — all requested lesson elements supplied; final landed-cell evidence necessarily belongs to L1 integration. Clarity 4/5 — separates contract from execution; detailed mistake-table cells are dense. Actionability 4/5 — draft path, source anchors, checks and replacement freeze hash supplied; final result values deliberately absent. Conciseness 4/5 — eight quotes and red-before witnesses are required; integration can trim repeated caveats without turning contracts into results. Mean 4.0/5. Improvement priorities: L1 replace only the explicit freeze placeholder; append genuine final measurements rather than inferring them; independent closure resolve F02 novelty and re-open S075. The user should find the assessment consistent with the narrow scribe role.

Reviewer correction applied: `R47RevLesson` flagged that QUALITY R5 is lesson-specific, while the watchdog proves only a failed report predicate. Removed R5 attribution from M47-5, explicitly preserved the missing-report/missing-lesson distinction, and added failure conditions (unresolved work commit, absent before→after, still-invalid report). No new execution evidence is claimed. The S074 used-by correction already matches frozen `claims.json:13`.

`R47RevD8` correction applied: Gate reject (1) now names the exact lead page URL `https://docs.github.com/en/rest/security-advisories/repository-advisories` (`R47SrD5Diff.md:69`), replacing the category root, and the reservation note stays explicitly conditional on actual S075 integration rather than standalone proof of admission.

`R47RevD8` completion note: REST-pointer item closed as owner-reported corrected; remaining risk is that frozen L10/L11 accept contradictory semantics, so independent sentence review and final integration checks stay owed to Main (this scribe made no counter or semantic verdict of its own).
