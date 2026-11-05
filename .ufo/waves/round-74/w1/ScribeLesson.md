# ScribeLesson — round 74, attempt 1 (wave w1): scoped findings

Seat: `ScribeLesson` (scribe, leaf; no subagents). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Freeze `847b5379` (`847b53792d2d29d161cad7d21a33c89df9e52e8d`), base `ccd6a54` (`ccd6a54bf392922495c4860332665499582e3213`), controls `654d877f` (`654d877f0bd4005fd139c46e5b889f4c1833ddda`). The three hashes resolve: `git rev-parse --verify -q <h>^{commit}`, exit 0 each.

## Deliverables (drafts; the L1 integrates)

- `.ufo/waves/round-74/w1/lesson-round-74.md`: header; `## Gate` (S109 admitted as F52; OSV overview rejected as a row, flip stated; NDSS 2023 paper not opened; considerthese sweep); `## Gate correction for round 73 (R73-V1, appended 2026-11-05)` listing round 73's two rejects; `## Mistakes` (M74-1, M74-2, M74-3); `## Routed defects`; `## Registry changes (old -> new)`; `## Counters`; `## Sourced claim`; `## Non-claim work`; `## Seats` placeholder for the L1.
- `.ufo/waves/round-74/w1/sources-edits.md`: exact lines for (1) the S109 row after line 120; (2) the search-log paragraph after line 168; (3) two Leads bullets after line 172 (OSV overview, NDSS 2023); (4) the Fuzzilli-lead retirement annotation after line 266 (line 172 untouched); (5) the census before/after line.
- `.ufo/waves/round-74/w1/ScribeLesson.evidence.txt`: copies of the scratch outputs cited below (177 lines).
- No lane file was changed. No git mutation, commit, push, stash, checkout, reset or pull. Read-only git only (`rev-parse`, `archive` into scratch).

## Measurements (command, exit code, result)

| # | command (run from the lane root unless stated) | exit | result |
|---|---|---|---|
| 1 | `sha256sum corpus/source-snapshots/round-74/S109.txt` | 0 | `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486` (matches the pinned sha) |
| 2 | `wc -l < corpus/source-snapshots/round-74/S109.txt` | 0 | 375 |
| 3 | `grep -cF '<L151 quote>' corpus/source-snapshots/round-74/S109.txt`; `wc -w` on the quote | 0; 0 | 1 occurrence at line 151; 22 words |
| 4 | S109 row: `grep '^| S109 '` on the draft, then awk `-F'|'` | 0; 0 | 1 line; 13 fields including outer pipes = 11 cells; 0 cells containing a pipe |
| 5 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (base) | 0 | 108 |
| 6 | scratch dry run: insert the row after line 120, recount | 0 | 109 rows; `sed -n 121p` shows S109; base line 172 byte-identical to line 173 after the insert (`cmp` exit 0) |
| 7 | `grep -cE '^\| S109 ' corpus/SOURCES.md` (base) | 1 | 0 (S109 absent; grep exit 1) |
| 8 | Round-73 Gate reject count: awk range of `corpus/lessons/round-73.md` `## Gate` then `grep -ciE reject` | 1 | 0 (grep exit 1), 7 lines in the Gate section |
| 9 | `grep -nE '^\| R33 ' corpus/QUALITY.md`, then `grep -cE` | 0 | lines 292 and 550 (count 2) |
| 10 | `grep -oE '^\| R[0-9]+ '` on QUALITY, sorted with `sort -V`, tail | 0 | highest id R118; `grep -cE '^\| R1(19\|20) '` = 0 (exit 1), so R119 and R120 are free |
| 11 | `grep -c 'osv.dev/api' corpus/SOURCES.md` | 1 | 0 (no existing OSV lead) |
| 12 | `grep -rniE 'osv\|v1/query\|query api\|osv\.dev' considerthese/` and `grep -rliI fuzzilli considerthese/` | 1; 1 | no match in either |
| 13 | `grep -rliI fuzzilli corpus/ PROVINCE.md README.md` | 0 | 12 files: the S093 entry, its round-60 snapshot and manifest, round-60 and round-61 lessons and their verifier spot-check, the round-73 lesson, README, SOURCES, knowledge-expected, PROVINCE, S109 snapshot |
| 14 | `ls corpus/knowledge/*.md \| wc -l` | 0 | 89 |
| 15 | `wc -l < corpus/instruments/knowledge-expected.txt`; `grep -c '^#'`; `grep -vc '^#'` | 0; 0; 1 | 91 lines; 2 comment lines; 89 rows |
| 16 | dry run: knowledge-expected rows plus the new name, `LC_ALL=C sort -c` | 0 | 90 rows; the new name sorts between `first-psirt-services-framework.md` and `project-zero-fuzzilli-vs-bigsleep-comparison.md`; 92 lines with the two comment lines |
| 17 | C1 census, base export (`git archive ccd6a54` into scratch), `--lane` set to the lane root | 0 | `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant` |
| 18 | same counter on the current tree, `--root` and `--lane` both the lane | 0 | the same line and result |
| 19 | counter run with the export path as `--lane` (my error, recorded in the lesson) | 1 | `noprefix=89`, `nonconformant`; the entries carry the lane path, so the prefix did not match. Not a counter defect |
| 20 | frontier counter, base export, standalone | 0 | `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108`; `entries=54 pass=54 exit=0` |
| 21 | capture-binding check, base export, standalone | 0 | `records=87 bound=87 unbound=0` |
| 22 | capture-binding check, current tree, standalone | 1 | `FAIL rule=missing-manifest dir=round-74` (S109 has no `manifest.json`); the last line still prints `records=87 bound=87 unbound=0` |
| 23 | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`, current tree | 0 | `kasegi ok`; six inherited W04 warnings (S028 S029 S072 S076 S080 S085) |
| 24 | `grep -nF` of the two scout quotes in `.ufo/waves/round-74/w1/ScoutSurface-osv-api-overview-snapshot.txt` | 0; 0 | line 36 "Currently there are no limits on the API."; line 38 "The API has a response size limit of 32MiB when using HTTP/1.1. There is no limit when using HTTP/2." |
| 25 | `sha256sum` and byte count of the scout snapshot | 0; 0 | `6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`, 1810 bytes |
| 26 | `grep -nF` of the round-73 spot-check quote | 0 | line 94 (the spot-check's item 3 row) |

## Findings for the L1

1. **M74-3 (new, found while drafting): QUALITY criterion id R33 is held twice.** Round 38's closure-order row is at `corpus/QUALITY.md:292`; round 73's executable-census row is at `:550`. The round-73 lesson's R33 citation names two rows. The next free id is R119 (proposed for the Gate-reject criterion). The collision fix is the L1's decision; the draft proposes an append-only supersession under R120 that names line 550. Able to fail: row 9 above, count must go from 2 to 1.
2. **M74-2 recurs in a base receipt.** `.ufo/waves/round-74/controls/c2-base-counters-r74.txt` line 7 is `python3 corpus/instruments/capture-binding-check.py | tail -1`, and line 9 `capture-exit=0` is therefore `tail`'s exit. The value is right: row 21 re-measured it standalone (exit 0, `records=87`). The receipt's labelling is wrong. The draft asks for an appended erratum on that receipt (controls are append-only), not an edit.
3. **Pre-landing dependency for C2.** `corpus/source-snapshots/round-74/` has `S109.txt` and no `manifest.json`; row 22 is exit 1. Per QUALITY R20, the manifest lands in the same commit as the capture and entry. Scout receipt §6.2 reports the same.
4. **The OSV overview lead carries both halves of the scout's quote 2.** The page says "There is no limit when using HTTP/2" as well as the HTTP/1.1 limit. The round-73 spot-check recorded only the HTTP/1.1 half, so the draft's lead bullet and its Gate correction quote both halves verbatim from the scout's receipt (row 24), and state that the spot-check did not record the second half. The date is the scout's fetch instant, 2026-11-05T08:43:42Z UTC (curl) and 08:43:58Z (instrument), not the spot-check's re-read date.
5. **NDSS 2023 paper.** The draft adds it as its own `## Leads (unopened)` bullet, because the round brief says "lead remains". The S109 capture gives no URL, so the bullet names it without one. If the L1 meant the Fuzzilli lead line itself to carry the NDSS mention, the wording moves; the retired line stays byte-identical either way.
6. **Search-log counts.** Per the brief: identified 1, screened 1, included 1, excluded 0. The sibling sweep (row 13, 12 files) is named in the paragraph as the negative-claim sweep. Its hits are the held S093/F41 comparison and lessons, not tool documentation. The OSV page and the NDSS paper are stated as not screened in this search.
7. **Considerthese candidate.** None (rows 12). The connector seat's record was not on disk while this draft was written; the lesson leaves the cross-check to the L1.
8. **Spot-check.** Pending the non-author. The draft records one admit and two non-admissions, which is enough for LEARNING.md's "at least one admit and one reject" once the non-author writes it.
9. **Counter argument (my error, disclosed).** Row 19: the census derives its prefix from `--lane`, and the entries carry the lane path. The base reading in row 17 used the lane path and is the valid one. The lesson records both runs.

## Process incidents (disclosed)

- **Write-path error, corrected.** My first two writes used relative `.ufo/...` paths. The write tool resolved them against the fleet root (`/home/vgpnk/Projects/shokunin`), creating `/home/vgpnk/Projects/shokunin/.ufo/waves/round-74/w1/{lesson-round-74.md,sources-edits.md}`. Fleet-root git reported `?? .ufo/waves/round-74/` (untracked; created that morning by these writes). I moved both files into the lane path with `mv -n` (no clobber; both targets absent beforehand, exit 0 each), then ran `rmdir` on the two fleet-root directories (both exit 0, so they held nothing else). Fleet-root `git status --porcelain -- .ufo/waves/round-74` is empty afterwards. No fleet-root tracked file was touched. Later writes used absolute paths.
- **One `sed -i ''` call with no file argument** (in a scratch check). It had no target and changed nothing.

## Tools

None installed, upgraded or removed. Commands used: `sha256sum`, `wc`, `grep`, `awk`, `sed` (reads only), `cmp`, `sort`, `mv -n` (own drafts only), `rmdir` (own empty dirs only), `git rev-parse`, `git archive` (read-only into scratch), `python3` (the four read-only instruments: `recheck-cwd-census.py`, `frontier-recheck-count.py`, `capture-binding-check.py`, and the repo's `scripts/sources-census.sh validate`).

## Left for the L1 (not done by this seat)

- Apply `sources-edits.md` (row, search-log paragraph, two Leads bullets, retirement annotation, census after-line).
- Land the knowledge entry, `manifest.json`, `knowledge-expected` rows (91/89 to 92/90), README F52 (frontier 51 to 52) and the capture-binding after-counts (87 to 88).
- Decide the QUALITY R33 collision (M74-3) and land R119 if accepted.
- Append the erratum on `c2-base-counters-r74.txt` (M74-2).
- Fill the lesson's `## Seats` from `w1-results.json`; name the non-author spot-check; file `.ufo/reports/round-74/kasegi.md` after the last lane commit.
- The end-to-end trial (`considerthese/2026-10-26.md` item 2, R73-V5) is owned by its own seat's report; the lesson only cross-references it.

## Scratch

`/fast/scratch/hyaku/kasegi-r74/ScribeLesson` held the base export, dry-run files and command outputs. Copies of the cited outputs are in `ScribeLesson.evidence.txt`. The directory is deleted before this seat yields.
