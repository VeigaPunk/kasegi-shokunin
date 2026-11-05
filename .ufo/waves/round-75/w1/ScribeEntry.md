# ScribeEntry — round 75, attempt 1, wave w1 — F53 / S110 entry draft

Seat: ScribeEntry-17 (leaf; no subagents; draft-only; no lane write).

## Result

- Draft entry (lane filename `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md`, not yet landed): `.ufo/waves/round-75/w1/entry-draft-fuzzilli-ndss2023.md`.
- Body grounded only in the 24 quotes that ExecC2Capture pinned in `.ufo/waves/round-75/w1/ExecC2Capture-manifest-r75-S110.json`, each at the manifest's own anchor line. All 24 are used. One further line, S109.txt:243 (`Q16-ndss-paper`, pinned in the round-74 manifest), is cited for the distinctness note.
- The entry opens with the provenance trio exactly as the assignment states it, followed by a `ground:` line. It ends with a verification section.
- Comparison outcome: **not stated.** The pinned introduction says the fuzzer "compares well with" Superion and names Superion as "the state-of-the-art method called Superion." (S110.txt:128, 142). The paper's Section VII outcome text is not pinned, and it says the opposite on the full corpus (see Routed item 1). The entry therefore records the comparison design only.

## Commands run (cwd: fleet root unless noted; exit codes given)

1. `read` of `.ufo/waves/round-75/claims.json` in full, then the C2 target and kill-rule fields via `python3` (exit 0). Frozen after-values B1–B8 and the entry_recheck clause read from the file, unchanged.
2. `read` of `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md` (r74 F52 model) and `corpus/QUALITY.md:531` (R108) (exit 0).
3. Scratch dir created: `/fast/scratch/hyaku/kasegi-r75/ScribeEntry-17/` (mkdir exit 0).
4. Own capture into scratch (the spec's fallback, before the manifest existed):
   `python3 corpus/instruments/capture-source.py --id S110 --url https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf --out $S/S110.txt --kind pdf` → `status=200 fetched_bytes=918189 snapshot_bytes=88072 sha256=0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef utc=2026-11-05T09:50:06Z`, 1869 lines, exit 0. The fetched byte count matches the freeze note (918189). `pdftotext` was already present at `/usr/bin/pdftotext`; nothing was installed.
5. `cmp` of ExecC2Capture's `.ufo/waves/round-75/w1/ExecC2Capture-S110.txt` against my scratch capture: **identical**, both sha256 `0780beaef…e51ef`, 88072 bytes (`cmp` exit 0). My line anchors therefore hold against the lane capture.
6. Distinctness greps (read-only):
   - `grep -c -i 'ndss\|Fuzzilli' corpus/SOURCES.md` → 12 hits (exit 0). Per-hit verdicts: line 100 (S093 row: PZ comparison post, distinct, not used); line 121 (S109 row: README, distinct, not used); lines 134, 173, 245, 247, 250, 253, 255, 267, 270 (round history notes about Fuzzilli leads or rows; no NDSS paper row); line 175 (the NDSS lead, kept byte-identical as history and retired by this round's S110 row, per the B1/B2 clauses). No lane row other than S093 and S109 covers Fuzzilli documentation.
   - `grep -nE '^\|[[:space:]]*S110[[:space:]]*\|' corpus/SOURCES.md` → 0 lines (exit 1): S110 is unused in the lane registry.
   - `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 109 (exit 0), matching the B1 base.
   - `grep -ril 'fuzzilli' ../revenger-shokunin/corpus` → 0 files (grep exit 1): no Fuzzilli mention in the sibling corpus, so no sibling NDSS row exists.
   - Revenger rows exist for the named B8 comparators: `grep -nE '^\|[[:space:]]*S(117|396)[[:space:]]*\|' ../revenger-shokunin/corpus/SOURCES.md` → line 132 (S117, DecFuzzer ISSTA'20 artifact README) and line 411 (S396, trailofbits/mishegos differential x86 decoder fuzzer) (exit 0). Both are tool documentation rows, distinct from this paper.
   - `ls corpus/knowledge/*.md | wc -l` → 90 (exit 0, the base count the C2 clause names).
7. Pinned-quote verification of the final entry (the commands and outputs are in the wave dir as `ScribeEntry-entry-recheck.txt`):
   - Entry quote check (scratch script; parsed each quoted string and its `(S110.txt:N)` / `(S109.txt:N)` anchor, compared against the manifest): 25 quoted strings, 25 anchored, 0 unanchored, **0 not pinned at the same anchor**, 24 of 24 S110 pinned quotes used (exit 0).
   - `python3 corpus/instruments/source-recheck.py --manifest <scratch>/manifest-pinned.json --source S110`, run from the scratch cwd on a copy of ExecC2Capture's manifest with the byte-identical capture as `S110.txt` (exit 0): `S110:sha256 OK`, all 24 quotes `OK` at their anchors (`anchor=N-ok`), 0 MISMATCH, 0 BROKEN. Output saved as `ScribeEntry-entry-recheck.txt`.
   - Word and length limits on the 24 pinned quotes: max 12 words, min 12 normalized characters (exit 0), within B5's ≤25 words and the instrument's 12-character floor.
   - `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-74/manifest.json --source S109` run from the lane root (read-only; exit 0): `S109:Q16-ndss-paper OK occurrences=1 anchor=243-ok`.
   - Sentence-anchor scan: every paper-facing sentence carries an anchor. The 18 sentences without one are the entry's own scope and self-description (what it does not cover, and the distinctness notes), not claims about the paper.
8. Proposal check: `propose.py` built `ScribeEntry-proposed-manifest-additions.json` from 16 candidate quotes (see Routed items). Run with `source-recheck.py` from the scratch cwd: exit 0, all 16 `OK` at their anchors. **Not applied** to any manifest.
9. The earlier 83-quote draft was checked as well (exit 0, 83 of 83 OK against my scratch capture). It was superseded once the pinned manifest appeared (its quotes were not in that manifest), and its evidence files were removed from the wave dir.

Tools installed or upgraded: none. Records under the operator's tooling directive: no pacman, no `uv tool install`, no `npm`, no binary download. `pdftotext`, `qpdf` and `python3` were already present.

## Routed items for KasegiR75 (the integrator)

1. **Comparison contradiction (highest priority, C2 coverage).** The pinned introduction says the fuzzer "compares well with" Superion (S110.txt:128), and the contributions list gives the comparison as "We perform a comprehensive comparison against modern" (S110.txt:140) with the comparator named "the state-of-the-art method called Superion." (S110.txt:142). Section VII says "Overall, Superion outperformed our fuzzer when provided with the full DIE corpus" (S110.txt:1332), and "The final coverage of Superion was 3%, 6%, and 8% larger than our final coverage" (S110.txt:1333). The outcome text is not in ExecC2Capture's manifest, so the entry states no outcome. Before the entry says anything about the outcome, pin P01–P03 (in `ScribeEntry-proposed-manifest-additions.json`) and state the full-corpus result alongside the introduction's wording. Without that, the F53 entry's "evaluation results" scope is limited to the window, counts and age that are pinned.
2. **Root-cause counts do not match the stated total (this entry's reading, R108).** The root-cause counts are printed as 3, 2, 4 and 9 (S110.txt:1101, 1103, 1110, 1114), which sum to 18. The paper states 17 (S110.txt:39, 1041, 1126, 1377). The effect counts (7, 2, 3, 2, 3) and time counts (14, 3) each sum to 17. These root-cause lines are not pinned, so the entry states no breakdown. The discrepancy goes in the round lesson, or into the entry as this entry's reading once P09–P12 are pinned.
3. **Manifest coverage.** ExecC2Capture pinned 24 quotes, mostly short snippets. The semantic-correctness measures (S110.txt:735–758), the IR and mutation loop beyond the pinned lines, the SoFi non-comparison (S110.txt:1228–1238) and the paper's own caveats (S110.txt:1187–1199) are not pinned. The proposal file adds 16 candidate quotes, verified against the byte-identical capture at their anchors. ExecC2Capture or the L1 decides whether to adopt them; this seat did not change the manifest.
4. **Binding the lane manifest.** `source-recheck.py` reads the manifest from `corpus/source-snapshots/round-75/manifest.json`, and its `path` is `S110.txt` relative to that directory. The manifest currently lives only in the wave dir (`ExecC2Capture-manifest-r75-S110.json`). The L1 must copy it, and the capture, to the lane path, so that the B5 command (`cd <foreign cwd> && python3 <lane>/corpus/instruments/source-recheck.py --manifest <lane>/corpus/source-snapshots/round-75/manifest.json --source S110`) runs against the pinned manifest. The entry's `recheck:` line uses that path.
5. **Lane capture identity.** The ExecC2Capture capture is byte-identical to my scratch capture (sha256 `0780beaefb5c0d973c76d4376a0c151345910890fa9a913b68461d71747e51ef`, 88072 bytes, 1869 lines). The entry's anchors are valid against it. If the lane capture ever differs, the anchors must be re-run.
6. **Title spelling.** The capture prints the title as "F UZZILLI" (S110.txt:1), a PDF text-extraction artifact. The manifest pins that exact spelling (`Q01-title`). The entry's source line uses the registry spelling, as the assignment specifies.
7. **Registry and knowledge counts (not done by this seat).** The S110 row, the knowledge file count (90 → 91), the capture binding and the frontier row are the L1's writes. The entry's distinctness note depends on the S109 and S093 rows and on revenger S117 and S396 as they stand.

## Out of scope (not done)

- No lane write: nothing committed, staged, pushed, stashed or checked out; no file under the lane except the wave-dir files below.
- No edits to MANIFEST.json, templates/, scripts/, `.ufo/state/`, `.ufo/watchdog.log`, or any earlier lesson.
- No live target contact: the only network GET was the named NDSS PDF (HTTP 200).
- No CVE or vulnerability identifier in the entry; no exploit or live-fuzzing content.

## Files (all under the wave dir)

- `entry-draft-fuzzilli-ndss2023.md`: the entry draft (25 quotes, all pinned).
- `ScribeEntry-entry-recheck.txt`: the `source-recheck.py` output for the entry's quotes, exit 0.
- `ScribeEntry-proposed-manifest-additions.json`: 16 candidate quotes for P01–P16 (Section VII outcome, root-cause counts, SoFi, caveats), with its `source-recheck.py` output, exit 0. Proposal only; not applied.
- `ScribeEntry.md`: this report.

Scratch directory `/fast/scratch/hyaku/kasegi-r75/ScribeEntry-17/` is removed at the end of this seat (see the final cleanup command).
