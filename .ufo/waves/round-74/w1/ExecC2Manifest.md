# ExecC2Manifest — C2 admission fragments for F52 / S109 (round 74, attempt 1)

Seat: ExecC2Manifest (executor, leaf). Scope: C2 only. C1 (recheck-cwd counter) is not in this seat's item. No lane-tree file was edited; no git/jj mutation was run; no tool was installed; no labrat was spawned. All writes are under `.ufo/waves/round-74/w1/` (this report, the manifest, four fragments, `evidence/`). Scratch `/fast/scratch/hyaku/kasegi-r74/ExecC2Manifest` was created, used, and deleted (receipts copied to `evidence/` first).

## Result

- Capture verified unchanged: `sha256sum corpus/source-snapshots/round-74/S109.txt` → `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`, `wc -l` → 375, exit 0 (run twice, both exit 0). Byte count 19630 (`stat -c %s`, exit 0).
- Manifest built from the capture bytes: 16 quotes (claims floor was >=10; item asked 12–16). Every quote is an exact substring of its anchor line (asserted in Python, not transcribed by hand). Max word count 22 (Q01); all others ≤18. Q01 and Q13 contain straight double quotes that match the capture's own bytes.
- `source-recheck.py` returns OK for sha256 and all 16 quotes at their anchors, from two foreign cwds, with identical stdout digests.
- Four drafts written: sources row, README F52 block, PROVINCE line, knowledge-expected line. Cell counts and sort order checked.

## Quote pins (manifest `manifest-r74-S109.json`, anchors are capture line numbers)

| id | anchor | words | locus clause |
|---|---|---|---|
| Q01-definition | 151 | 22 | coverage-guided fuzzer, FuzzIL |
| Q02-semantic-concern | 165 | 18 | JIT semantic correctness |
| Q03-try-catch-contrast | 165 | 15 | try-catch versus runtime-API |
| Q04-swift-c-split | 212 | 18 | Swift/C split |
| Q05-mutation-fuzzer | 215 | 10 | MutationFuzzer |
| Q06-corpus | 217 | 11 | Corpus |
| Q07-evaluator | 220 | 14 | Evaluator |
| Q08-storage | 226 | 6 | Storage |
| Q09-event-driven | 227 | 15 | event-driven design |
| Q10-repl-name | 230 | 9 | REPRL name |
| Q11-repl-reset | 230 | 13 | REPRL reset |
| Q12-tree-hierarchy | 233 | 9 | tree hierarchy |
| Q13-root-16-256 | 236 | 18 | root / 16 / 256 example |
| Q14-targets-dir | 154 | 11 | Targets/ directory |
| Q15-clang-instrumentation | 156 | 15 | coverage instrumentation, clang >= 4.0 |
| Q16-ndss-paper | 243 | 16 | NDSS 2023 existence |

Not pinned (named in the entry body, not in the manifest): MutationFuzzer-adjacent ScriptRunner/Minimizer/Lifter lines (L216, L219, L221) and the Environment line (L218). They are in the capture; the README text in F52 cites them by line.

Clause coverage vs claims.json `pre_freeze_quote_locus`: L151 Q01; L165 Q02, Q03; L212 Q04; L214-L221 Q05, Q06, Q07 (L214 intro and L216/L218/L219/L221 are not pinned); L226-L227 Q08, Q09; L230 Q10, Q11; L233 Q12 and L236 Q13; L154-L156 Q14, Q15 (L155 patches not pinned); L243 Q16. All pinned quotes are located at the claimed loci.

## Commands and exit codes

1. `sha256sum …/corpus/source-snapshots/round-74/S109.txt; wc -l …` → c9a7…486, 375; exit 0 (proc `sha_check`, `sha2`).
2. `git -C …/kasegi-shokunin log --diff-filter=A -- corpus/source-snapshots/round-74/S109.txt` → commit 847b5379… (2026-11-05T05:34:37-03:00), exit 0 (proc `gitcap`). Commit message: "round-74: freeze claims C1 … and C2 … capture S109 opened pre-freeze with located clauses". **No fetch instant or HTTP status for S109 exists in the lane** (grep `S109` in `LOG.md`: no hits; no capture receipt file).
3. Python build of the manifest (eval cell "Build S109 manifest from capture bytes"): per-quote assertions `q in lines[anchor-1]`, `len(q.split()) <= 25`, `>= 12` normalized chars — all passed; exit 0. Wave manifest written with `path: "evidence/S109.txt"` (the instrument rejects capture paths outside the manifest directory, so the capture copy lives in `evidence/`). Final-layout manifest written to scratch with `path: "S109.txt"`.
4. Recheck, cwd `/tmp`: `cd /tmp && python3 corpus/instruments/source-recheck.py --manifest .ufo/waves/round-74/w1/manifest-r74-S109.json --source S109` → 16 × OK + `sha256 OK`; **exit 0**; stdout sha256 `cadaa6b856b0f589597207850c2d399c49fbbc5d6768beacba04dfac9b065449`. Receipt: `evidence/recheck-S109-cwd-tmp.txt`.
5. Recheck, second foreign cwd (`<scratch>/cwd2`): same command; **exit 0**; stdout sha256 `cadaa6b8…9449`, identical (digest match = True). Receipt: `evidence/recheck-S109-cwd-scratch.txt`.
6. Final-layout check (manifest beside `S109.txt`, path `S109.txt`), cwd `/tmp`: **exit 0**. Receipt: `evidence/recheck-S109-final-layout.txt`; manifest copy `evidence/manifest-final-layout-S109.json` (cmp against scratch copy: CMP_OK, exit 0).
7. Negative control (one quote's `guided` → `guidedX` in a scratch copy, path re-pointed to the scratch capture): **exit 1**, `Q01-definition MISMATCH reason=quote-not-found`, others OK. Receipt: `evidence/recheck-S109-negative-control.txt`. (A first attempt returned exit 2 `reason=missing` because I had not re-pointed the path; that was my scratch-setup error, not a gate result, and is superseded by the run above.)
8. Cell-pipe check (Python split on `|`): sources row 13 parts = 11 cells; F52 row 8 parts = 6 cells; area row 3 cells. No literal `|` is inside any cell. Result: `cell-count ok: True`.
9. Registry base: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 108, exit 0. After one row: 109 (expected).
10. Knowledge base: `ls corpus/knowledge/*.md | wc -l` → 89, exit 0. After the entry: 90 (expected; the entry file is not in this seat's item and is not in the lane yet).
11. Expected file: base `corpus/instruments/knowledge-expected.txt` → 91 lines, 89 data rows; `LC_ALL=C sort -c` on the base file → exit 0. Composed (base data rows + new line, LC_ALL=C-sorted, headers kept) → `sort -c` exit 0; 92 lines, 90 data rows. New line sits between `corpus/knowledge/first-psirt-services-framework.md` and `corpus/knowledge/github-advisory-database-curation-semantics.md`.
12. Cleanup: `rm -rf -- /fast/scratch/hyaku/kasegi-r74/ExecC2Manifest; ls -d …` → "No such file or directory", exit 2 (absent, as intended).

## Drafts (all in this wave dir)

- `sources-row-S109.md` — one 11-cell registry row, id S109, docs, tier A, mined, opened 2026-11-05, recheck 90d, used-by `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`. Teaches one grounded benefit (S109.txt:165).
- `readme-F52-block.md` — heading `## Round-74 admission — coverage map row and Frontier F52 (2026-11-05)`, Area/source-basis table, six-cell F52 row (topic and next cells carry only capture-located content with line anchors), and the line `[r74 amendment, appended 2026-11-05] The frontier as of round 74 is F01-F52 admitted: F52 at round 74.` followed by a scope sentence. Leading blank line for end-of-file append.
- `province-F52-line.md` — one PROVINCE line in the r73 form: `[r74 Frontier amendment, appended 2026-11-05, end-of-file append per R6] F52 — …; admitted on source S109 in corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md. Scope limit: …` with the claims.json scope_limit text verbatim after "Scope limit:".
- `knowledge-expected-line.txt` — `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` (single line, trailing newline).

## Open items for the L1 (not resolved by this seat)

1. **Fetch metadata is unrecorded.** `fetched_utc` and `http.status` are `null` in the manifest; the instrument does not read them. The L1 should fill them only from a real receipt. None exists in the lane; I did not invent one.
2. **Registry source name.** The row uses "Google Project Zero Fuzzilli" as specified. The capture does not contain that phrase (the entry states this; the owner handle `googleprojectzero` is what the page shows at S109.txt:1 and :62).
3. **Manifest placement.** Apply `evidence/manifest-final-layout-S109.json` as `corpus/source-snapshots/round-74/manifest.json` beside `corpus/source-snapshots/round-74/S109.txt` (path `S109.txt`). That layout passed recheck (exit 0). The wave-dir manifest (`evidence/S109.txt`) passed too but is a wave-local copy.
4. **Not run here (lane-applied state required):** `frontier-recheck-count.py`, `capture-binding-check.py`, `sources-census.sh validate`, the entry's own recheck from a foreign cwd, and the knowledge-expected apply. Those are the L1's checks after applying the four fragments; I did not run them and do not claim them.
5. **Entry file.** `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` is not in the lane. A draft exists at `.ufo/waves/round-74/w1/knowledge-fuzzilli-js-engine-fuzzing-framework.md` (ScribeEntry's, not reviewed here). Its `recheck:` line must match the manifest location the L1 chooses.

## Files written by this seat

- `.ufo/waves/round-74/w1/ExecC2Manifest.md` (this report)
- `.ufo/waves/round-74/w1/manifest-r74-S109.json`
- `.ufo/waves/round-74/w1/sources-row-S109.md`
- `.ufo/waves/round-74/w1/readme-F52-block.md`
- `.ufo/waves/round-74/w1/province-F52-line.md`
- `.ufo/waves/round-74/w1/knowledge-expected-line.txt`
- `.ufo/waves/round-74/w1/evidence/S109.txt` (byte-identical copy of the capture; sha256 c9a7…486)
- `.ufo/waves/round-74/w1/evidence/manifest-final-layout-S109.json`
- `.ufo/waves/round-74/w1/evidence/recheck-S109-cwd-tmp.txt`
- `.ufo/waves/round-74/w1/evidence/recheck-S109-cwd-scratch.txt`
- `.ufo/waves/round-74/w1/evidence/recheck-S109-final-layout.txt`
- `.ufo/waves/round-74/w1/evidence/recheck-S109-negative-control.txt`

## Tooling

None installed or upgraded. Only the stdlib `python3`, `sha256sum`, `wc`, `stat`, `cmp`, `grep`, `ls`, `sort`, and `git -C … log` (read-only) were used.
