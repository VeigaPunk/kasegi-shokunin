# ScribeLesson — round-79 lesson draft (kasegi, attempt 1)

Seat: `ScribeLesson`, leaf. Scope: prose only — drafted the round-79 lesson in the six-section shape of `corpus/lessons/round-78.md`. Wrote no product code, no lane instrument, no corpus entry, no QUALITY row, no commit.

## Behavior

- Read, in this order: `corpus/lessons/round-78.md` (shape), `.ufo/waves/round-79/claims.json` (both frozen predicates), all eight files under `.ufo/waves/round-79/controls/`, `corpus/source-snapshots/round-79/manifest.json`, `corpus/source-snapshots/round-79/S113.txt`, the three rejected spot-checks `corpus/lessons/round-7{6,7,8}-verifier-spotcheck.md`, `.ufo/waves/round-79/w1-spec.json` (seat count and roles), `corpus/QUALITY.md` tail (last R row), `.ufo/waves/round-79/c1/mutbat.py` table and candidate.
- Drafted `.ufo/waves/round-79/w1/lesson-round-79.md`, 77 lines, six sections in the required order: `## Gate`, `## Mistakes`, `## Sources`, `## Learning`, `## Routed`, `## Seats`.
- Measurements this seat actually took (all read-only; no counter, no gate suite, no scratch writes):
  1. **M79-1 output equivalence.** Python `difflib.unified_diff` of `.ufo/waves/round-78/w1/successor/selftest.out` against `.ufo/waves/round-78/w1/successor/mutants/K-X2.out`, normalized by replacing `/fast/scratch/…` with `<SCRATCH>`: **zero diff lines (identical)**. Raw diff: exactly one hunk, line 9 (the `tmpdir-refusal` line), differing only in the random `recheck-cwd-selftest-…` suffix inside the scratch path. Both files end `selftest cases=13 failures=0`; 14 lines each.
  2. **Quote locatability (CORPUS rule 1).** Plain containment of each of the eight manifest quotes in the committed `S113.txt`: each occurs exactly once in the file and exactly on its declared line — lines 25, 41, 41, 55, 61, 62, 66, 85. Word counts 19/18/12/22/14/7/11/14, all ≤25.
  3. **Snapshot hash.** `sha256sum corpus/source-snapshots/round-79/S113.txt` = `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf`, equal to the manifest pin; 127 lines, 5669 bytes.
  4. **Literal distinctness.** Eight quotes against 92 `corpus/knowledge/*.md` files: 0 hits for each (8/8 zero), matching the claim's "measured 0/8 at freeze".
  5. **Freeze-tree census.** knowledge `.md` files 92; registry S-rows 113 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); `| mined ` 92, `| queued ` 2; `knowledge-expected.txt` 94 lines / 92 `.md` rows; `corpus/README.md` F-rows 56; `F55` in `PROVINCE.md` and `corpus/README.md` 0.
  6. **Frozen-byte hashes.** candidate `eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f`; `mutbat.py` `735d2336550850a0c72c6049e5d7ee1f92dd345332b624578a8b627bcfba3ea9`; `mutant-table.json` `0cb50dc858d0fc5548bc6c22a49171be3326298763c64d5344afe83de2d731e2`, 19 rows (18 `assertion`, 1 `exception`). All three and the manifest are in freeze `9d0b1eb0` (`git cat-file -e` succeeds; `git show --stat 9d0b1eb0` lists them).
  7. **Static structure of the candidate** (no execution): 15 `REQUIRED_CHECKS`; `gate-predicates` = 17 predicate rows in both polarities plus a known-bad/known-good wiring scan; `gate-wiring` = AST scan of the file's own `check()` calls, findings `F1` (constant-`True` ok), `F2` (no predicate call), `F3` (unwired required check).
  8. **Reject-ground check.** `corpus/knowledge/osv-post-v1-query-contract.md:75` lists the experimental endpoints; `:31` carries the case-sensitivity sentence (quoting S108.txt:53); `:47` carries the single-query pagination trigger (quoting S108.txt:136) — i.e. the round-78 Q12 reason named the wrong ground, and `grep -n -i 'threading\|vary'` over F51 finds nothing.
- Disclosure: `python3 corpus/instruments/frontier-recheck-count.py | tail -3` was run once, read-only (prints only), to read the pre-round frontier tail (`PASS F53`, `PASS F54`, `entries=57 pass=57 exit=0`). No other lane instrument, counter or the full gate suite was run.
- Sibling artifacts read after they landed mid-draft (read-only; the seats own them, the L1 re-reads the final files): `w1/ExecC1Battery.md` and `w1/ExecC1Battery-mutants/*.out` (two identical `MUTBAT … killed=18 survived=0 dirty=1 notderived=0` runs, rc 1; `K-T1 verdict=EXCEPTION-KILL counted=no`; `K-X2b verdict=KILLED counted=yes`; `K-X2a KILLED`, `K-M8 KILLED`, `K-W2`, `K-C1`, `K-NP` KILLED), `w1/ScoutDistinct.md` (§2 literal 0/8, §3 per-clause table), and the staged C2 entry set under `w1/c2/`. These are cited in the lesson as sibling artifacts, never as this seat's measurements and never as verdicts.

## Gates (recorded by reference, no verdicts)

- C1: frozen predicate `.ufo/waves/round-79/claims.json` C1 entry, P1–P7, kill rule; targets `cases=15 failures=0`, nonexistent `TMPDIR` rc 2, `killed=19/19`, pin rows `cases=15`, exec surface unchanged. Verdict line in the lesson: `L1 fills`.
- C2: frozen predicate `.ufo/waves/round-79/claims.json` C2 entry, B0–B7; targets frontier 54→55, knowledge 92→93, S113 `queued`→`mined`, registry 113 unchanged, distinctness 0/8, census rc 0. Verdict line: `L1 fills`.
- The lesson states each claim by one-sentence summary plus the predicate ids and the frozen bytes, and states no verdict.

## Lesson content delivered (mapped to the seat item)

1. `## Gate`: C1 and C2 by reference to freeze `9d0b1eb0709e47c3c6decc09138b5012a8968924` (base `d16d2124…`) with all frozen hashes; the S113 access record (URL, 2026-11-06, HTTP 200, raw 30242 bytes, snapshot sha256 from the manifest, 127 lines, 5669 bytes); the eight ≤25-word quotes with `S113.txt:<line>`; eight admits; three rejects at `:37`, `:39`, `:64` with their reasons (plus the sample-response non-claim); the S113 status change `queued -> mined`, `—` → entry path, flagged as a pending item the L1 confirms.
2. `## Mistakes`: **M79-1**, class `equivalent-mutant-as-required-kill`, with the measured zero-line normalized diff, `captured-by: none`, the r79 gate-predicates + gate-wiring fix, proposed **R128** text and its show-able-to-fail pair (r78 K-X2 survives on `f6849971`; r79 K-X2b killed on `eda49d32`, receipt `w1/ExecC1Battery-mutants/K-X2b.out`, L1-inserted); **M79-2**, class `frozen-table-class-mismatch` (K-T1), with the counter's counting rule, the measured `killed=18` battery, the two claim-level readings the L1 may take, and proposed **R129**.
3. **Appended correction** for round-78 spot-check item 1, inside `## Gate`, labelled appended-never-in-place: F51:47 holds the pagination trigger, not the threading caveat; the true reason is that `S112.txt:170` qualifies Q10/Q11 (`S112.txt:168`, `:169`); F54's `Not claimed` line at `corpus/knowledge/osv-post-batch-query-contract.md:61` carries the same wrong cite and is corrected by reference only.
4. **Item 4 placement**: the seven S112 quotes are cited by path to the F54 entry's Gate table (`corpus/knowledge/osv-post-batch-query-contract.md:67`), not restated.
5. `## Routed`: R-77-D and R-77-E stay L0 pending; R-77-F has two of four leads still open (`GET /v1experimental/importfindings`, `POST /v1experimental/ubuntu/binary-to-source`) with determineversion taken by F55; r78 spot-check defects 1–5 each mapped to where it is handled or why it stays open; proposed R128 routed to the L1.
6. `## Seats`: **13** seats — executor×3, scribe×2, scout×1, reviewer×3, critic×1, mutation-tester×1, sentinel×1, connector×1 (6 of 13 attack seats), counted from the 13 items of `w1-spec.json`.

## Findings (routed, for the L1)

1. **F-L79-1 — the brief's snapshot-hash hint is wrong, the manifest governs.** The seat brief hinted `f4bce053…6f10`; the manifest pin and `sha256sum` over the committed snapshot both give `f4bce05304157a593dcea94f400238e3eda62f73e6678a6e296260a428138ebf`. The lesson records the manifest value and says so explicitly.
2. **F-L79-2 — registry count 112 vs 113 is a pre-row vs freeze-tree difference, not a conflict.** `controls/c2-donothing-counters-r79.txt` prints 112 S-rows; the freeze commit adds the S113 row and the freeze tree measures 113, matching B1/B3 and `measured_before`. No claim amendment needed; the control file's own header says "before the S113 row".
3. **F-L79-3 — M79-1's evidence is a zero-line normalized diff, not an inspection.** The r78 K-X2 transform (`clean_ok is True and …` → `True and …`) is behaviourally equivalent because the harness only exercises `clean_ok=True`; the raw difference is one scratch-suffix. Any later seat that cites K-X2 as an "assertion kill" without this normalization repeats the defect.
4. **F-L79-4 — the C2 entry does not exist yet at the freeze tree.** `corpus/knowledge/osv-determineversion-cc-library-versioning.md` is absent and `corpus/SOURCES.md:125` still reads `queued` with `—`; the lesson marks every after-value as a B2/B3 target and the status change as pending, so no line can be read as landed. The staged draft is at `w1/c2/` and is the L1's to integrate.
5. **F-L79-5 — C1's P3 target is unreachable on the frozen bytes; the seam is the frozen table's `class` field.** The battery receipt (sibling, two identical runs) prints `killed=18 survived=0 dirty=1 notderived=0`, rc 1, because K-T1 is classed `assertion` in `mutant-table.json` while failing as `tmpdir-refusal FAIL ret=-99 … exception=FileNotFoundError(2, 'No such file or directory')`; `mutbat.py:93` counts `EXCEPTION-KILL` only for rows classed `exception`. K-T1's own `expect` string already says "(exception caught as ret=-99)". Under the frozen kill rule C1 therefore reads NOT VERIFIED unless the L1/operator rules on the claim (reclass the row as a freeze amendment and re-score, or amend P3's counting clause). The lesson records this as M79-2 + a routed conflict; no seat edits the table. Proposed **R129** (class derived from the observed failure mode before freeze).

## Touched surfaces

Written (only these):

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/lesson-round-79.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ScribeLesson.md` (this file)

Read-only: `corpus/lessons/*`, `corpus/knowledge/*`, `corpus/source-snapshots/round-79/*`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`, `PROVINCE.md`, `.ufo/waves/round-79/{claims.json,controls/*,c1/*}`, `.ufo/waves/round-78/w1/successor/*`, `.ufo/waves/round-79/w1-spec.json`, `git log/show/cat-file` (read-only).

## Out of scope (not done, deliberately)

- No edit to `corpus/QUALITY.md` (proposed R128 is text in the lesson only), no edit to `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, any knowledge entry, any instrument, or any sibling wave artifact.
- No counter run (P3 battery), no candidate selftest run, no gate suite, no `git`/`jj` write, no install, no scratch directory created (no writes outside the two files above).
- No verdicts: every gate line the lesson carries says `L1 fills`.
