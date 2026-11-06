# ScribeLesson — round 82, attempt 1

Seat: `ScribeLesson` (scribe, leaf). Task: draft the round lesson at `.ufo/waves/round-82/w1/lesson-round-82.md` for the L1 to integrate into `corpus/lessons/round-82.md`.

## Behavior

Read `claims.json`, every file in `.ufo/waves/round-82/controls/`, `corpus/lessons/round-81.md`, `corpus/lessons/round-81-verifier-spotcheck.md`, `corpus/QUALITY.md`, the round-82 manifest, `S116.txt`, the draft entry `corpus/knowledge/osv-high-quality-record-import-bar.md`, and the frozen table/counter bytes. Wrote one file, the lesson draft. No lane file edited, no git/jj write, no subagent, no background job, no counter/gate run.

## Checks run (all read-only) and outcomes

| check | command | outcome |
|---|---|---|
| frozen-byte equality | `sha256sum <path>` vs `git show b9589300:<path> \| sha256sum`, 16 paths (claims, candidate, counter, table, builder, entry gate, forgery driver, 7 control receipts, S116.txt, manifest) | 16/16 EQUAL |
| base instrument | `git show 1a50638e:… \| sha256sum`, `git show b9589300:… \| sha256sum` | both `a3b58aa5…dbec0`; the worktree copy is `81677e9d…` (uncommitted) |
| table composition | `python3` over `c1/mutant-table.json` | 63 rows = assertion 59, neutral 3, exception 1; 4 new (`J1 S07M B1 B2`), 2 re-anchored (`S04 S05`); `bucket-sum` 3, `main-default` 1 |
| quote location | `grep -n -F <quote> corpus/source-snapshots/round-82/S116.txt`, six quotes | 1 hit each, rc 0, at lines 25 36 41 44 47 51 |
| quote word counts | `len(quote.split())` per manifest pin | 12 23 6 10 19 13 (83 total) |
| manifest pins | `grep -n '"anchor"' …/manifest.json` | keys at 24 29 34 39 44 49, values = the six snapshot lines |
| M82-1 evidence | `awk '/^## Gate/{g=1} /^## Mistakes/{g=0} g' corpus/lessons/round-81.md \| grep -c 'PENDING-L1'` | **18** (whole file 24; distribution 2 / 18 / 4) |
| M82-1 fix, fail side | same awk over `corpus/lessons/round-81.md`, `grep -c -E 'PENDING-L1\|TBD\|TODO'` | 18 |
| M82-1 fix, pass side | same awk over the draft | **0** |
| receipt fidelity | script: every receipt-shaped line in the draft matched against the union of the control files | 57/57 verbatim, 0 unmatched |
| draft structure | fences balanced 16/16; headings `## Gate`, `### C1`, `### C2`, `## Mistakes`, `### M82-1`, `## Cite-check receipts`, `## Landing values (L1 fills)` | ok |

Not run (out of this seat's scope): any P1–P9 or B0–B8 predicate, `mutbat`, the census, `entry-gate`, `source-recheck`, the lane gate suite, any live fetch.

## Touched surfaces

- Wrote `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-82/w1/lesson-round-82.md` (318 lines, 32149 bytes, sha256 `a43231570c59ea587a7b8b374d7058c33947a0abc1a760e83e07f594244f802c`).
- Wrote this report.
- Scratch `/fast/scratch/hyaku/kasegi-r82/ScribeLesson/` (one file, `base.py` from `git show`), deleted before yield.
- Nothing else created, modified or deleted. No tool installed or upgraded.

## Findings (routed, not verdicts)

1. **Spot-check count vs body count (M82-1's number).** `corpus/lessons/round-81-verifier-spotcheck.md:107` says 24 markers "in the `## Gate` body"; the body holds 18, the file 24 (2 in the L1 section `:3-27`, 4 in § Sources). The landed R133 row (`corpus/QUALITY.md:595`, worktree, uncommitted at measurement) already records 18/24 correctly.
2. **Claims pin-line phrasing.** C2's `source` cell says "six pins at lines 25 36 41 44 47 51". Those are the snapshot anchors; the manifest's `"anchor"` keys sit at lines 24 29 34 39 44 49, and manifest lines 25/36/41/44/47/51 are `},`, `{`, `{`, `"anchor": 47`, `"id": "Q06-reference-urls"`, `]`. The lesson states both readings.
3. **Control-file label slip.** `c1-candidate-r82.txt` heads the three source greps `## P7 analogue`; the claim's predicate id for them is `P8` (P7 is the registry-row check). The lesson quotes the block verbatim and names the mismatch.
4. **Worktree mid-landing at the measurement instant `2026-11-06T21:14:55Z`.** `HEAD` = freeze `b9589300`; uncommitted `M` on `PROVINCE.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/README.md`, `corpus/instruments/knowledge-expected.txt`, `corpus/instruments/recheck-cwd-census.py`, `corpus/knowledge/osv-determineversion-cc-library-versioning.md`, plus untracked `corpus/knowledge/osv-high-quality-record-import-bar.md`. The set grew between two reads of `git status` during the draft (SOURCES.md, QUALITY.md and knowledge-expected.txt appeared after the first read), so the worktree is being written by another seat while this draft runs. Every frozen byte stayed equal to the freeze commit throughout.
5. **Entry vs manifest ranges.** The manifest note gives the Identifiable and example clause lines as `:53-55` / `:57-62`; the entry's § Not claimed (`:69`) gives `:52-55` / `:56-62`, i.e. including the section header lines. Both are true of the snapshot; the lesson states the difference rather than picking one.
6. **Junk-edit arithmetic.** The r82 junk-edit run prints `entries=96 exit0_foreign=67 exit1_foreign=22` (sum 89, seven short) and `ls corpus/knowledge/osv-*.md | wc -l` = 7 — the bucket-sum conjunct's seven missing rechecks, visible in the control without re-running it.

## Out of scope / not claimed

- No verdict line (C1/C2 verdicts are the L1's); the lesson's § Landing values lists landing-only names only.
- No claim that any P1–P9 or B0–B8 predicate is met at a landing commit: no landing commit exists at the measurement instant.
- The lesson does not assert the r82 candidate is landed; it records that the worktree instrument currently carries the candidate bytes uncommitted.
