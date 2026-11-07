# ScribeGate — round-94 wave-1 seat report

Seat: ScribeGate (leaf; no subagent dispatch). Working dir `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
for every command, scratch `S=/fast/scratch/hyaku/kasegi-r94/ScribeGate` (nothing of mine survives the seat).
Evidence read: freeze `96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`, C1 landing
`d51220aeb4a538b7b211bb2629e83210669cd56d`, C2 landing `996460861d4130ddb2da6b7554e905d3e47504a3`,
base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`. No git/jj mutation, no install, no pacman, no edit outside the
seat's report/draft/receipt paths.

## Verdict

**DRAFTED — Gate (S140) STANDS as re-derived, no claim re-score (scribe seat).** The `## Gate` block, the
M94-1/M94-2 mistake rows (classes `path-shape-keyed-forgery`, `vacuous-control`) and the `## Census` block are
written to `.ufo/waves/round-94/w1/ScribeGate-draft.md` from committed evidence only; each quoted anchor and each
census number was re-derived by this seat, and every "shown able to fail" pointer lands on a committed control line
inside `.ufo/waves/round-94/controls/`. C1 and C2 remain judged on their frozen predicates by the canonical judge;
nothing here re-scores them.

## Behavior

1. Read the frozen artifacts in place: `claims.json`, both control receipts (`c1-controls-r94.txt` 12 controls,
   `c2-controls-r94.txt` 10 controls), `capture-intake-r94.txt`, `redaction-r94.txt`, `source-recheck-r94.txt`,
   the two census receipts, `corpus/source-snapshots/round-94/{S140.txt,manifest.json}`, `corpus/SOURCES.md`,
   `corpus/lessons/round-93.md` (the format and the two carrier mistakes), and the L1's in-progress
   `corpus/lessons/round-94.md` (read only, not edited).
2. Re-derived the gate: byte-exact equality of the three manifest quotes at `S140.txt:4/114/255`, one occurrence
   each, 3 words each; snapshot sha256/bytes/lines equality with the manifest; `source-recheck.py` rc 0.
3. Re-derived the redaction: 82 marker lines, all inside `examples`/`negativeExamples` arrays, 0 non-marker element
   lines inside any array, 82 markers total; committed bytes scan clean with no allowlist row.
4. Ran the census validator twice (the worktree changed under the seat — see Findings F6) and parsed the S140 row
   cell by cell plus both round-94 bullets.
5. Drafted the three blocks, then scanned the draft with the lane's own scanner (hits=0) before committing it to
   the receipt path.

## Gates

- **S140 admit gate:** re-derived, STANDS — quotes exact at 4/114/255 (`occurrences=1`, ≤25 words), manifest
  sha256/bytes/lines match the committed file, `source-recheck.py` rc 0.
- **Intake gate:** the refusal is committed evidence (`rc 3`, two `INTAKE-REFUSED … written=no` lines); the
  committed snapshot is 82 structural marker lines with line numbering preserved.
- **Credential-shaped-bytes gate (round-93 M93-6 discipline):** my draft and this report scan clean
  (`hits=0 files=0`, `rc=0`); no example value was copied anywhere by this seat.
- **Census gate:** `validate` rc 0 with 7 output rows (6 inherited W04 + one `ok`); `census` rows 141
  (tier.A 128 / B 7 / C 6; mined 115 / queued 2 / rejected 24), `FLEET.invalid 0`, `missing 0`.

## Touched surfaces

- `.ufo/waves/round-94/w1/ScribeGate-draft.md` (new; draft only, the L1 owns the lesson).
- `.ufo/waves/round-94/w1/ScribeGate.md` (this report).
- `.ufo/waves/round-94/w1/ScribeGate-receipts/` (12 files, listed below).
- Nothing else: no product code, no `corpus/lessons/round-94.md`, no `corpus/SOURCES.md`, no `MANIFEST.json`,
  no `.ufo/state`, no sibling lane, no fleet-root tracked file.

## Out of scope (not done, deliberately)

- No re-score of C1 or C2; no reading of the claims as anything but their frozen predicates.
- No edits to the lesson, `SOURCES.md`, the counters or the instrument — the L1 commits.
- No re-execution of the 22 frozen controls (they are committed evidence); this seat cites their lines, and only
  re-runs read-only derivations (quote equality, redaction structure, source-recheck, census, scanner).
- No fetch of S140 or S141 (the manifest and the row cells carry the fetch facts).

## Findings

- **F1 — S140 quotes and snapshot are exact.** `sha256 f3fd09e4…`, 25,537 bytes, 563 lines; the manifest's
  `sha256`/`bytes`/`lines` all match; each quote equals its anchor line byte for byte, one occurrence, 3 words
  (`ScribeGate-receipts/07-quote-verify.txt`). The file has a trailing newline, so `split("\n")` yields 564
  elements while `splitlines()` yields the manifest's 563 — a counting artifact, not a mismatch.
- **F2 — the redaction is structurally complete.** 82 markers, all inside `examples`/`negativeExamples` arrays,
  0 non-marker element lines inside any array; ids, keywords, regex lines and array delimiters untouched
  (`08-redaction-structure.txt`). Committed bytes scan clean: `scanned=1 hits=0 files=0 allowed=0 unused_allow=23`.
- **F3 — the intake refusal is real and pre-write.** `INTAKE-REFUSED S140 shape=credential line=534` and
  `shape=gitlab-pat line=7`, `written=no`, rc 3 (committed `capture-intake-r94.txt`). No allowlist row was needed
  for the committed form.
- **F4 — M93-4's fix can fail.** `F1-path-shape-keyed` is rc 1 want 1 PASS: the forged instrument fails K4 with
  `missing=` 30 path|shape pairs — every path a digest basename, `round-1` absent from the whole list — and K9 with
  `lost=` 26 pairs; the pinned candidate passes K9 with `prev_hits=39 lost=none`. The relocated shape keeps only
  the scan-scope prefix the scanner's file-class rules need.
- **F5 — M93-5's fix can fail.** `m3-union-unmapped` is rc 1 want 1 PASS with `LIMB M3 FAIL same_files=True
  bad_lines=1` on a label citing `corpus/QUALITY.md:537`; `m3-union-applied-before-r93` is rc 1 want 1 PASS with
  `traceback=True`, i.e. the round-93 counter crashes on the same input; `m3-union-applied` passes M3
  (`same_files=True bad_lines=0`). The controls assert a limb/traceback observation, not rc alone.
- **F6 — the worktree changed under the seat.** The first census pair (`validate` rc 0 with the six W04 + `ok`;
  `census` `rows 140`) and the second (`validate` rc 0 with the same seven rows; `census` `rows 141`) straddle
  another seat's addition of the S141 row and its bullet to
  `corpus/SOURCES.md` (`git status` shows `M corpus/SOURCES.md`; `corpus/lessons/round-94.md` and
  `.ufo/waves/round-94/l1/` are also untracked). Both runs and both `census` readings are in the receipts. The
  draft's count (141) holds only if the L1 commits S141; dropping it returns the registry to 140.
- **F7 — unobserved claim in the L1's in-progress lesson (qualifier, routed back).** The L1 draft's M94-3 says
  GH013 refused the first round-94 freeze at `S140.txt:192-195` and `:394`. No committed round-94 receipt records
  a GH013 response: `grep -rn GH013 .ufo/waves/round-94/` finds only the wave-spec text, and the host
  `events.log` GH013 mention is dated 2026-10-30 (unrelated). The committed evidence grounds the redaction on the
  intake refusal (rc 3) plus the structural rule; my Gate block claims only that. If the GH013 sentence is kept,
  it needs its remote-error receipt named.
- **F8 — S141 provenance.** The S141 row (kind `code`, tier B, status `rejected`, used-by `—`) and its bullet are
  uncommitted at read time; its cells validate clean and the census counts it (tier.B 6 → 7, rejected 23 → 24).
  The row's teaches cell already carries `REJECTED: …`.

## Receipts

All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated; outputs are stored under
`.ufo/waves/round-94/w1/ScribeGate-receipts/`; `TMPDIR` / scratch under `/fast/scratch/hyaku/kasegi-r94/ScribeGate`.

| command | observed |
|---|---|
| `git log --oneline -4`; `git status --short`; `git show --stat --oneline 96b5033 d51220a 9964608` | rc 0; 4 commits (base, freeze, C1, C2); worktree `M corpus/SOURCES.md`, `M .ufo/waves/round-94/make-wave-r94.py`, untracked `l1/`, `w1*`, `corpus/lessons/round-94.md` — `01-git-state.txt` (52 lines) |
| `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (from the fleet root), run 1 | rc 0; 7 rows (6×W04 + `ok`) — `02-census-validate-140.txt` |
| same command, run 2 (after S141 appeared) | rc 0; 7 rows (same 6×W04 + `ok`) — `03-census-validate-141.txt` |
| `bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi`, run 1 | rc 0; `rows 140`, tier.B 6, rejected 23 — `04-census-mode-140.txt` |
| same command, run 2 | rc 0; `rows 141`, tier.A 128 / B 7 / C 6, mined 115, queued 2, rejected 24, `FLEET.invalid 0`, `missing 0` — `05-census-mode-141.txt` |
| `python3` parse of `corpus/SOURCES.md` (S140/S141 cells, round-94 bullets) | rc 0; both rows 11 cells; 2 round-94 bullets at lines 335 and 336 — `06-sources-rows.txt` |
| `python3` manifest-quote vs committed-snapshot check | rc 0; sha/bytes/lines match; 3 quotes `exact=True occurrences=1 words=3` — `07-quote-verify.txt` |
| `python3` structural redaction check | rc 0; 82 markers in arrays, 0 non-marker element lines — `08-redaction-structure.txt` |
| `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-94/manifest.json` | rc 0; `S140:sha256 OK`, three quotes `occurrences=1 anchor=4/114/255-ok` — `09-source-recheck.txt` |
| `sed -n` of the cited lines in both committed control receipts | rc 0; c2 lines 1,2,9,26,28,31,33; c1 lines 1,2,24,28,35,37,38,42 — `10-controls-cited.txt` |
| `grep -n` `relocate`/`K9` in `c2/capability-check.py` + landed instrument GitLab shapes | rc 0; `relocate` at 503 (sha256(nonce|path)[:12]), K9 at 634; three GitLab regexes at 199-201 — `11-relocate-k9.txt` |
| `python3 -B corpus/instruments/capture-secret-scan.py --files .ufo/waves/round-94/w1/ScribeGate-draft.md` (and this report) | rc 0; `scanned=1 hits=0 files=0 allowed=0 unused_allow=23` — `12-scan-output.txt` |

Artifacts: `.ufo/waves/round-94/w1/ScribeGate-draft.md` (Gate / Mistakes / Census), `.ufo/waves/round-94/w1/ScribeGate.md`
(this report), `.ufo/waves/round-94/w1/ScribeGate-receipts/` (12 files).
