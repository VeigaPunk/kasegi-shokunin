# ScribeLedger — round 76, attempt 1 (scribe, leaf, drafts only)

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Freeze `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` (verified: `git -C <lane> rev-parse HEAD` rc 0). Base `a788021675873a96e09e91aa033d8c26ac2fe212` (verified: `git -C <lane> rev-parse 5da54cd…^` rc 0). L1 is `KasegiR76`. I wrote no lane file; my writes are the six drafts, three receipt/evidence files and this report, all under `.ufo/waves/round-76/w1/`.

## Summary

- Six ledger drafts written (README F54 block, knowledge-expected line, PROVINCE line, LOG block, SCORECARD block, lesson skeleton). Each file's header states its placement; the text to apply sits below the line of equals signs.
- **Blocker for C2 (needs an L1 or operator decision before any seat scores):** the committed S111 manifest pins quote Q01 (`API (1.0)`, 9 normalized characters), and `source-recheck.py --source S111` exits 2 on it (`MIN_QUOTE_CHARS = 12`, line 33). Claim B5 ("13 quotes anchor-located, exit 0") is therefore not met by the committed bytes. I did not choose a repair; §Findings lists the options.
- **One deviation from the literal instruction:** the knowledge-expected line must be inserted at line 68, not appended. An append breaks claim B2 (`LC_ALL=C sort -c`, measured rc 1). Inserting passes (rc 0).
- The capture renders the determineversion path with an interior space (`POST /v1experimental/ determineversion`, S111.txt lines 8 and 46). The drafts avoid naming that path in the README and PROVINCE text.
- The README block includes a coverage-map row, following the house pattern of the r72–r75 admission blocks. The assignment named only the frontier row; §Findings item 6 says how to drop it if unwanted.

## Deliverables (all under `.ufo/waves/round-76/w1/`)

| file | placement at integration | content |
|---|---|---|
| `readme-f54-block-draft.md` | end-of-file append after `corpus/README.md` line 1189 | `## Round-76 admission` block: R6 paragraph (sha256, lines, manifest), coverage-map row, F54 frontier row (six cells, NF=8 measured), `[r76 amendment]` line, counts at integration. Quote count left as `<FILL>` (see blocker). |
| `knowledge-expected-line-draft.md` | **insert** between `corpus/knowledge/osv-affected-range-events.md` (line 67) and `osv-post-v1-query-contract.md` (line 68) | the single line `corpus/knowledge/osv-api-surface-and-limits.md`; 93 lines / 91 rows → 94 / 92 |
| `province-line-draft.md` | end-of-file append after `PROVINCE.md` line 223 | one line: F54 admitted on S111; overview page leaves the Leads list; five non-query endpoint contracts stay open |
| `log-r76-draft.md` | end-of-file append after `LOG.md` line 2811 | `## Round 76` block; freeze and base hashes as-is; `<FILL>` for landed measurements; counters table; counting commands |
| `scorecard-r76-draft.md` | end-of-file append after `SCORECARD.md`'s last line | axis rows (depth:verifiability 4→4 nominal R58; coverage 8→8 held; depth:density 9, not targeted); move log; planned-after slots (residual classes; the five non-query endpoints as candidate rows; calibration) |
| `lesson-r76-draft.md` | **new file** `corpus/lessons/round-76.md` (absent at base, measured rc 2) | `## Gate` (F54/S111 pending integration; reject and spot-check slots), `## Mistakes` (two drafting/capture candidates and one blocker candidate, plus `<FILL>` rows), `## Routed defects`, `## Counters`, `## Counting commands` |

Evidence files (named here so they are auditable):
- `ScribeLedger-checks-r76.txt` — receipt of the checks in §Measurements (T1–T14), produced by `bash ScribeLedger-checks-r76.sh`.
- `ScribeLedger-checks-r76.sh` — the driver (copied from scratch; reads the lane, writes only to scratch).

## Measurements

Every value below comes from the command shown, with its exit code. Scratch: `/fast/scratch/hyaku/kasegi-r76/ScribeLedger/`. Lane reads were read-only (`cat`, `grep`, `ls`, `sha256sum`, `wc`, `awk`, `diff`, `sort -c`, `git rev-parse`, and the instruments run with `-B` from scratch or with `--root` on a scratch copy).

| # | command (cwd / key args) | rc | value |
|---|---|---|---|
| M1 | `git -C <lane> rev-parse HEAD` | 0 | `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e` |
| M2 | `git -C <lane> rev-parse 5da54cd…^` | 0 | `a788021675873a96e09e91aa033d8c26ac2fe212` |
| M3 | `ls corpus/knowledge/*.md \| wc -l` | 0 | 91 |
| M4 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 0 | 110 |
| M5 | `grep -c 'F54' corpus/README.md` | 1 (zero matches) | 0 (F54 absent at base) |
| M6 | `grep -c 'Round-76\|Round 76\|round-76'` over README, PROVINCE, LOG, SCORECARD | 1 (zero matches) | 0 in each file |
| M7 | `ls corpus/lessons/round-76.md` | 2 | no such file (lesson is new) |
| M8 | `sha256sum corpus/source-snapshots/round-76/S111.txt`; `wc -lc` (T9) | 0 | `6f92e5b791edcda59ef2f9e566105cb3c944b25eee5753402ad12d374e5581ab`; 48 lines, 1810 bytes |
| M9 | `python3 -B` read of `w1-spec.json` `items` (count only) | 0 | 13 seats: ExecC1Amend, ExecC1Controls, ExecC2Checks (executor ×3); ScoutSurface, ScoutNext (scout ×2); ScribeEntry, ScribeLedger (scribe ×2); ReviewC1, ReviewC2 (reviewer ×2); CriticClaims; MutC1; SentinelC1; ConnectOverlap |
| M10 | T1: `diff` of `grep '^corpus/knowledge/' knowledge-expected.txt \| sort` against the directory listing | 0 | base expected rows equal the directory (91) |
| M11 | T2: `LC_ALL=C sort -c knowledge-expected.txt`; row and line counts | 0 | sort clean; rows 91; lines 93 |
| M12 | T4: APPEND the knowledge row at the end, then `LC_ALL=C sort -c` | **1** | `disorder: corpus/knowledge/osv-api-surface-and-limits.md` at line 94. The literal "append" instruction fails B2. |
| M13 | T5: INSERT the knowledge row before line 68, then `LC_ALL=C sort -c`; counts | 0 | sort clean; lines 94; rows 92; `osv-api-surface-and-limits.md` at line 68 |
| M14 | T6: `diff` base expected against the inserted variant | 1 (differences found, expected) | one added line, `67a68`; no existing line text changes |
| M15 | T7: inserted variant rows equal the directory plus the new name (simulated; file not yet on disk) | 0 | set-equal |
| M16 | T8: NF of the drafted F54 row and of the F53 row | 0 | both NF=8 (six cells) |
| M17 | T10: manifest quotes located at their anchors (python, read-only) | 0 | 13 quotes; `bad=[]`; anchors 21..39; max 19 words per quote |
| M18 | T11: frontier counter `--root <scratch copy>` with the drafted README block and a scratch-only S111 row cloned from S110 | 1 | `FRONTIER-CENSUS rows=54 admitted=54 closed=53 problem-rows=1 registry=111`; `FAIL F54 … problems=missing-entry`; `entries=57 pass=56 exit=1`. The only problem is the entry file, which is not yet on disk; the row enumerates as `admitted`, `ids=S111`. |
| M19 | T13: `source-recheck.py --manifest <committed> --source S111` (read-only, scratch cwd) | **2** | `S111:Q01-api-version UNAVAILABLE reason=quote-too-short-to-be-evidence` |
| M20 | T13b: `grep -n 'MIN_QUOTE_CHARS' corpus/instruments/source-recheck.py` | 0 | line 33: `MIN_QUOTE_CHARS = 12` |
| M21 | T14: `grep -n '1\.0' S111.txt` | 0 | only line 21 (`API (1.0)`) |
| M22 | scratch removal (after receipts were copied) | — | see §Hygiene |

Sibling cross-check (read-only): `ScribeEntry.md` reports the same Q01 blocker (its own `ScribeEntry-recheck-S111.txt`, rc 2) and a scratch experiment with Q01 removed (rc 0, 12 quotes). M19 reproduces the rc 2 on the committed bytes independently.

## Findings for the L1

1. **B5 cannot pass on the committed bytes (blocking for C2).** Q01 is below the command's own floor, so `source-recheck.py --source S111` exits 2 (M19, M20). The only capture line with the version statement is line 21 (M21), so no other located line keeps 13 quotes with a 12-character version ground. The options are:
   - (a) drop Q01 and record 12 quotes. Claim B5 says "13 quotes anchor-located"; under the frozen wording that is false, so C2 is NOT VERIFIED as frozen.
   - (b) keep 13 by re-pinning Q01 to a longer line-21 quote. The capture does not allow one.
   - (c) an operator amendment of B5's wording, decided before any seat scores (the kill rule forbids predicate rewrites after scoring).
   I did not choose. The drafts carry `<FILL>` for the quote count, and the blocker is routed in the lesson's § Routed defects.
2. **knowledge-expected must be an insert (deviation from "append").** Measured in M12 and M13. Lines after 67 shift down by one; no line's text changes (M14). The L1 should confirm `LC_ALL=C sort -c` exits 0 after applying (B2).
3. **Endpoint spelling.** `POST /v1experimental/ determineversion` appears with an interior space at S111.txt lines 8 and 46 (grep, rc 0). The drafts quote the path only in LOG and SCORECARD, with a footnote that the space is the capture's rendering. ScribeEntry's entry quotes it verbatim and reads it as the unspaced path, which is consistent. Nothing in the drafts verifies the live endpoint name; I did not fetch the live site.
4. **F54 row parses.** M16 and M18 show the row is six cells and enumerates as admitted with `ids=S111`. The only problem in the scratch run is the missing entry file. Expected after the entry lands: `entries=57 pass=57` (the claim's B3). I have not measured that; it needs the entry on disk.
5. **Sibling drafts agree with mine.** ScribeEntry's `s111-row-draft.md` says to add the S111 row after the S110 row, which is what M18's scratch simulation does. Its `f54-entry-draft.md` targets `corpus/knowledge/osv-api-surface-and-limits.md`, the same path as my drafts. ScribeEntry drafted no README row and no knowledge-expected line, so there is no conflicting text.
6. **Coverage-map row.** The README block includes one, as the r72–r75 admission blocks do. The assignment named only the frontier row. To drop it, delete the table in the block (its header, separator and row) and the sentence that refers to it.
7. **Quote length.** The 13 manifest quotes have at most 19 words (M17), under the 25-word bound that round 75 measured against (M75-2 class).

## Mistakes and routed defects (mirrored in `lesson-r76-draft.md`)

- Candidate M76 (scribe-found, unverified against the landed bytes): the drafting assignment's "append" wording for the knowledge-expected line conflicts with B2 (M12).
- Candidate M76 (scribe-found): the capture's interior-space endpoint rendering versus the claim's spelling (Finding 3).
- Candidate M76 (scribe-found): a frozen clause whose named command cannot pass on the committed bytes (B5 / Q01, M19). Same class as M75-2.
- Routed defect (C2 B5 blocker): Finding 1; decision belongs to the L1 or operator.

## Not done / limits

- No lane file was written. The six drafts are unapplied by design; the L1 applies them.
- I did not run the C1 counter or any amended-counter measurement; those belong to the executor and reviewer seats.
- The frontier check (M18) used a scratch copy of the corpus with a scratch-only S111 row cloned from S110. It checks parsing and enumeration only, not the real registry row.
- No network access beyond reading the committed capture. I did not fetch `https://google.github.io/osv.dev/api/` myself.
- The drafts contain `<FILL>` slots by design (landed hashes, measured counts, mistake ids). They are not complete ledger text until the L1 fills them.

## Tooling

Installed or upgraded: none. I used coreutils, `python3` stdlib, the existing instruments run read-only, and read-only git. No PATH directory was modified and no pacman transaction was run.

## Hygiene

- Receipts were copied into the wave dir before scratch removal (`ScribeLedger-checks-r76.txt`, `.sh`).
- Scratch `/fast/scratch/hyaku/kasegi-r76/ScribeLedger/` removed: `rm -rf` rc 0, then `ls -A` on it rc 2 (no such file). Other seats' scratch dirs under `/fast/scratch/hyaku/kasegi-r76/` were not touched.
