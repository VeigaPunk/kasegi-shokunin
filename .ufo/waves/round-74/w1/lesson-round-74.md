# Round 74 — lesson (kasegi, attempt 1)

DRAFT by seat ScribeLesson (wave w1). The L1 integrates this into `corpus/lessons/round-74.md`; this file is not the landed lesson.

Round: kasegi r74 attempt 1. Frozen claims `.ufo/waves/round-74/claims.json` (freeze commit `847b5379`, full `847b53792d2d29d161cad7d21a33c89df9e52e8d`; base `ccd6a54`, full `ccd6a54bf392922495c4860332665499582e3213`; controls commit `654d877f`, full `654d877f0bd4005fd139c46e5b889f4c1833ddda`). All three hashes resolve: `git rev-parse --verify -q <h>^{commit}`, exit 0 each. Attack/build wave `w1` (13 seats, one v1 wave; results `.ufo/waves/round-74/w1-results.json`). Report: the L1 files `.ufo/reports/round-74/kasegi.md` after the last lane commit (round-73 convention).

Claims: C1 (`depth:verifiability`, counter amendment, RC-1/RC-2/RC-3) and C2 (`coverage`, frontier F52 on S109). Non-claim round work is listed under `## Non-claim work`.

## Gate

Candidates considered this round:

- **S109 — the Fuzzilli project README, `https://github.com/googleprojectzero/fuzzilli` — ADMITTED as F52 (one knowledge entry, `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`).** Access date 2026-11-05. Capture `corpus/source-snapshots/round-74/S109.txt`, sha256 `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`, 375 lines (`sha256sum` exit 0, `wc -l` exit 0). Located quote, capture line 151 (22 words): "A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language ("FuzzIL") which can be mutated and translated to JavaScript." Checks: `grep -cF` of the quote in the capture = 1 (exit 0); `wc -w` of the quote = 22. Registry row: docs, tier A scoped to the project's own README statements, status mined, opened 2026-11-05, recheck 90d.
- **OSV.dev overview page, `https://google.github.io/osv.dev/api/` — REJECTED as a row this round.** Reason: it was opened lead-only for the R73-V2 bullet; it has no capture or manifest in this round, and CORPUS.md SOURCES rule 1 allows a row only after its source is opened in the round that writes the row, with that source captured for the row. Its two statements, quoted verbatim in the round-74 scout receipt (`.ufo/waves/round-74/w1/ScoutSurface.md` §5; fetched 2026-11-05T08:43:42Z UTC, HTTP 200; snapshot sha256 `6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`), are "Currently there are no limits on the API." (snapshot line 36) and "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." (snapshot line 38). They are recorded as lead statements in `## Leads (unopened)`, not as evidence. Flip: a round that needs its rate-limit or response-size statements as admitted ground opens the page with its own capture and manifest.
- **NDSS Symposium 2023 paper about Fuzzilli (named at S109 line 243) — NOT opened.** Reason: outside the frozen scope; claims.json C2 `scope_limit` claims existence and name only. The lead remains, in its own `## Leads (unopened)` bullet. The S109 capture carries no URL for the paper, so the lead names it without one.
- **considerthese candidates (OSV / query API / Fuzzilli tool documentation).** Sweep this round: `grep -rniE 'osv|v1/query|query api|osv\.dev' considerthese/` exit 1 (no match); `grep -rliI 'fuzzilli' considerthese/` exit 1 (no match). No considerthese candidate is recorded for F52. The connector seat's own record is not in the wave dir while this draft is written; the L1 cross-checks it against its report.
- **Held Fuzzilli material — not a candidate.** Project Zero's comparison post (S093, F41, `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md`) is held and distinct: its scope limit keeps the tool method out, which is why the tool's own README is the open ground.

Admitted: S109 / F52. Rejected: the OSV overview page as a row (reason above). Not opened: the NDSS 2023 paper (reason above).

Spot-check result: pending. LEARNING.md requires a non-author spot-check of at least one admit and one reject, recorded as `agree` or `disagree` with a reason. This round has one admit and two non-admissions. The check is the non-author's to write (the L1 names the reviewer); this seat does not write it.

### Gate correction for round 73 (R73-V1, appended 2026-11-05)

Round 73's `## Gate` (`corpus/lessons/round-73.md` lines 14 to 20) records one admitted candidate and its quote checks, and no reject. Its two rejects appear only in its Residuals and report. `grep` of that Gate section for `reject` returns 0 (awk range extract of lines 14 to 20 then `grep -ciE reject`, count 0, exit 1). The rejects are recorded here, with reasons, as LEARNING.md "Files the path writes" requires. `corpus/lessons/round-73.md` is not edited.

1. **OSV overview page, `https://google.github.io/osv.dev/api/` — rejected (not captured, no row).** Round 73 Residual 2: "The OSV overview page (`api/`) is not captured; its rate-limit and response-size statements are not claimed." Round 73's spot-check (`corpus/lessons/round-73-verifier-spotcheck.md` §4 item 3) re-read the live page and recorded it as stating "Currently there are no limits on the API" and a 32 MiB limit for HTTP/1.1; it did not record the HTTP/2 half. The round-74 scout receipt quotes both statements verbatim (`.ufo/waves/round-74/w1/ScoutSurface.md` §5). Now recorded as a lead (R73-V2), not as a row.
2. **considerthese OSV / query-API proposal — rejected (grep found no matching proposal).** Round 73 lesson line 53: "`considerthese/` was not mined for an OSV or query-API proposal: `K73ConnectSiblings` §4 reports the grep and its result." The spot-check (`corpus/lessons/round-73-verifier-spotcheck.md` §4 item 4) re-ran `git grep -niE 'osv|v1/query|query api|osv\.dev' <head> -- considerthese/`, which returned no matches.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M74-1 | landing/recording: round 73's `## Gate` omitted its two rejected candidates, against LEARNING.md "Files the path writes" (Gate = candidates considered, admitted, rejected with reasons). Found by the round-73 non-author spot-check (R73-V1), not by any criterion | `corpus/lessons/round-73.md` lines 14 to 20 (Gate: zero reject mentions, count 0, exit 1); `corpus/lessons/round-73-verifier-spotcheck.md` §4 items 3 and 4 sampled both rejects | none: no criterion made a Gate reject checkable | this lesson's `## Gate` lists rejects with reasons; the correction block above; proposed criterion R119 (below) | Gate section of the round-73 lesson, `grep -ciE reject` = 0 (exit 1) today; after R119 is applied, a round Gate must show at least 1 reject line, or the explicit line "none this round" with the carried rejects named |
| M74-2 | number-drift / landing: the first freeze-check replay block printed `replay-exit=0` for a pipeline, not the counter, and its C1 line never printed; the same class sits in the base receipt `c2-base-counters-r74.txt`, whose `capture-exit=0` (line 9) is the exit of `capture-binding-check.py \| tail -1` (command line 7) | `.ufo/waves/round-74/controls/freeze-check-replay-r74.txt` lines 4 to 5 (first block) against the appended correction (lines 12 to 16); `.ufo/waves/round-74/controls/c2-base-counters-r74.txt` lines 7 to 9 | none | instruments run standalone with their own exit captured before any tee or pipeline. The correction block ran clean. Re-measured here: `capture-binding-check.py` at a base export (`git archive ccd6a54`) run standalone, exit 0, `records=87 bound=87 unbound=0` (value matches the receipt; the receipt's exit label does not) | `grep -n 'tail -1' .ufo/waves/round-74/controls/c2-base-counters-r74.txt` = 1 hit today; closed by an appended erratum on that receipt naming line 9 and the standalone run, not by editing the receipt |
| M74-3 | id collision / landing (found by this seat while drafting): criterion id R33 is held twice in `corpus/QUALITY.md`. Line 292 is the round-38 closure-order row; line 550 is the round-73 executable-census row. The round-73 lesson's R33 citation therefore names two rows. Highest id in use is R118 | `corpus/QUALITY.md` lines 292 and 550 (`grep -nE '^\| R33 '` exit 0, two hits); `grep -oE '^\| R[0-9]+ '` tail, max R118 | none: no counter checks QUALITY ids for uniqueness | L1 decides. Proposed: an append-only supersession row for the line-550 criterion under the next free id (R120), naming `corpus/QUALITY.md:550`, so R33 keeps only its round-38 meaning | `grep -cE '^\| R33 ' corpus/QUALITY.md` = 2 (exit 0) today; must be 1 after the fix |

Proposed QUALITY criterion (for the L1; not landed by this draft): **R119** — "Every round lesson's `## Gate` records a reject, a line naming a rejected candidate with its reason, or the explicit line `none this round — carried rejects named` followed by the carried rejects. A Gate with neither fails the round's census." Grounded in M74-1 (`corpus/lessons/round-73.md` lines 14 to 20; the R73-V1 spot-check). R119 is the next free id (R118 is the highest in use). Able to fail: the Gate grep above returns 0 on round 73 and returns at least 1 on this round.

## Routed defects (carried, not closed by this draft)

- **RC-1, RC-2, RC-3 (counter, mutation).** The targets of C1. Their closure is the L1's after-values (`--selftest cases=5 failures=0`, census shape, parity, kill rule (a) to (d)). Red-before receipt: `.ufo/waves/round-74/controls/c1-redbefore-mutant-survival-r74.txt`.
- **RC-4 (claim text, falsified), RC-5 (weakened), RC-7 (dead seat).** Carried as recorded in round 73. Not changed by this round.
- **RC-6 / R73-V3 (tree scope).** The merged-tree census prints `entries=89 … exit0_foreign=67` (round 73's C1 line on the merged tree). Recorded as falsified as written; the frozen `tree_scope` clause is not rewritten.
- **RC-8 (operator decision, open).** Recheck values still run through `bash -c` in the census. This round neither expands nor reroutes that surface. Routed around, not decided.
- **Pre-landing dependency for C2.** `corpus/source-snapshots/round-74/` holds `S109.txt` with no `manifest.json`. `capture-binding-check.py` on the current tree prints `FAIL rule=missing-manifest dir=round-74` and exits 1. The entry lands with its manifest in the same commit (CORPUS / QUALITY R20). Expected to clear when the manifest lands.

## Registry changes (old -> new)

- **S109:** none -> mined (row added after S108, `corpus/SOURCES.md` line 120; opened 2026-11-05; recheck none -> 90d; used-by none -> `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`). No pre-existing row changed.
- **Registry rows:** 108 -> 109. Base: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 108 (exit 0, measured this seat). After: L1 measures.
- **Fuzzilli lead:** retired as opened. `corpus/SOURCES.md` line 172 stays byte-identical as history; its retirement is an annotation in `## Registry changes` (round-67 convention), not an edit to the lead line. The ground is now S109 (F52).
- **Leads added (R73-V2 and the NDSS lead):** the OSV overview bullet (lead, not evidence; its two statements named as lead statements only, quoted with the round-74 scout's fetch instant 2026-11-05T08:43:42Z UTC, `ScoutSurface.md` §5) and the NDSS 2023 paper bullet (existence and name only, outside frozen scope).
- **Census before -> after:** before, `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0 with `kasegi ok` and six inherited W04 warnings (S028, S029, S072, S076, S080, S085) (`.ufo/waves/round-74/controls/census-before-r74.txt`; re-run by this seat, exit 0, same six warnings). After: L1 records the after-census.
- **Knowledge-expected:** 91 lines / 89 rows -> 92 lines / 90 rows (`corpus/instruments/knowledge-expected.txt`). Base measured here: `wc -l` 91 (exit 0), 2 comment lines, 89 rows. Dry run in scratch: the new row `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` sorts between `first-psirt-services-framework.md` and `project-zero-fuzzilli-vs-bigsleep-comparison.md`; `LC_ALL=C sort -c` exit 0 on the 90-row set.
- **Knowledge files:** 89 -> 90 (`ls corpus/knowledge/*.md | wc -l` = 89, exit 0 base).
- **Frontier rows:** 51 -> 52. Base: `python3 corpus/instruments/frontier-recheck-count.py` in a base export, exit 0, `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108`, `entries=54 pass=54 exit=0`.
- **Capture records:** 87 -> 88. Base: `capture-binding-check.py` in a base export, exit 0, `records=87 bound=87 unbound=0`.

## Counters (base measured by this seat; after-values by the L1)

- C1 base census, measured on the lane tree with `--lane` set to the lane root the entries name: `python3 corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>`, exit 0, `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`. Same values in `controls/c1-base-census-r74.txt`.
- Seat correction, recorded for the record: the first base-export run passed the export path as `--lane`, so every entry's `cd` prefix mismatched and the census printed `noprefix=89`, `RECHECK-CWD-RESULT nonconformant`, exit 1. That was a wrong `--lane` argument, not a counter defect. The counter derives its prefix from `--lane`, and the entries carry the lane root path. The run with the correct `--lane` is the one above.

## Sourced claim

C2 rests on S109, opened and captured this round (2026-11-05): the README at `https://github.com/googleprojectzero/fuzzilli` is the source for every content clause of F52. Its anchor lines (151, 154 to 156, 165, 212, 214 to 221, 226 to 227, 230, 233 to 236, 243) were re-read against the capture in this seat, and each named clause is present at its line. The knowledge entry cites S109 (claims.json C2 `entry`). The entry's own recheck from a foreign cwd and the manifest's quote checks are the L1's after-values, not this draft's.

## Non-claim work

- **End-to-end claim-package trial (SHONEN box 2; `considerthese/2026-10-26.md` item 2, "Run one end-to-end domain task round"; R73-V5).** Not a claim. Its evidence and result belong to its own seat's report; this lesson does not score it. The L1 cites that report here.
- **R73-V1.** Recorded above (`## Gate correction for round 73`).
- **R73-V2.** Recorded as the OSV overview lead bullet (`corpus/SOURCES.md` `## Leads (unopened)`).
- **R73-V4.** Post-landing round-73 counter receipts were committed before the freeze (`.ufo/waves/round-73/controls/`).
- **R73-V6.** Freeze-check replay before candidate measurement: `.ufo/waves/round-74/controls/freeze-check-replay-r74.txt`, with the correction block (see M74-2).

## Seats

L1 fills this section from `.ufo/waves/round-74/w1-results.json` (not on disk while this draft is written).
