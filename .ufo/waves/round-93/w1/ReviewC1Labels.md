# ReviewC1Labels — round-93 wave 1, attempt 1 (C1 tranche 8)

Seat: ReviewC1Labels (leaf, non-author). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Pinned revs: base `e15996bfd2f6eca4af39507a7c5973afbeca8347`, freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`,
C1 landing `ae53b3c6e7e2ce070c2f022d01c1677a8908df1b`, C2 landing `9225954a6e3f177af46bdb9d811c062a4353a552`.
Read-only on git/jj; no lane edits outside this report and its receipts. Scratch
`/fast/scratch/hyaku/kasegi-r93/ReviewC1Labels` removed on exit.

## Verdict

Verdict: 8 CORRECT / 0 PARTIAL / 0 WRONG — the five landed edits (437, 438, 454, 58, 144) are all
CORRECT, and all three no-edit pairs are correct to leave bare. Landed-edit subset: 5 CORRECT /
0 PARTIAL / 0 WRONG.

## The eight label rows and the five landed edits

The landing `ae53b3c` changes exactly one tracked path (`M corpus/knowledge/triage-thresholds.md`),
5 insertions / 5 deletions, 4 hunks. The two cell replacements are byte-identical to the text the
round-92 non-author labels carry (`round93-labels.tsv`, first 6 rows identical); the author appended
the 58/144 rows. The repoints are exactly the label values.

| site | landed value (quoted from `ae53b3c`) | verdict | anchor evidence at `ae53b3c` |
|---|---|---|---|
| 437 (cell) | `` `corpus/knowledge/intake-surface.md:89-93` (round-13 correction: `reward` object on 48 but numeric `reward.min` on only 14 — the reward-exists≠reward.min-numeric conflation, superseding the earlier "`reward.min` present on 48"), `SKILL.md:176-178` (...) `` | **CORRECT** | `intake-surface.md:89-93` = “`curated` = 1, `reward` object on 48 but numeric / `reward.min` on only 14 (round-13 correction; ...) ... from the reward-exists≠reward.min-numeric conflation)”; `SKILL.md:176-178` = “the `reward` / object exists on 48 records (all `source_kind=independent`) but numeric / `reward.min` on only 14 (round-13 correction)”. The errata sentence “`reward.min` numeric on **14**; `reward` object on 48” is true at both anchors; the cell text equals the label's `Replace cell with:` payload byte-for-byte. |
| 438 (cell) | `` `corpus/knowledge/mission-control.md:55-57` (peak → `openai-codex/gpt-6-astra:max`; the round-13 correction records that earlier text said `openai-oauth/`) `` | **CORRECT** | `mission-control.md:55-57` = “12:00–22:00 → `alibaba-token-plan/deepseek-v4-pro:max`; peak → / `openai-codex/gpt-6-astra:max` (round-13 correction: source / fleet-dispatch.mjs:300; earlier text said `openai-oauth/`)”. The errata sentence “Peak-window model is `openai-codex/gpt-6-astra:max`” is true; the cell equals the label payload byte-for-byte. |
| 454 (second token) | `SKILL.md:827-848` | **CORRECT** | `SKILL.md:827-833` = fenced `p_success` / `gross_value` / `total_cost` / `adjusted_ev` block; `:846-848` = “Missing inputs print `UNKNOWN`, never 0/1; ... fail-closed”. The old target `:494-506` is “TRANSIENT = ... → RETRY_TRANSIENT; else **REVIEW = no action**” plus the seven-part autopsy body (`:502-510`), with no EV formula term. |
| 58 | `SKILL.md:191` | **CORRECT** | `SKILL.md:191` = “status-file TERMINAL + telemetry `attempts()≥2`.” The old `:117` is provenance text (“nested in `commands[]` / `[lost-tree] ... provenance.json:29`”). `MAX_ATTEMPTS` occurs 0 times in `SKILL.md` (`grep -c` = 0, rc 1). |
| 144 | `SKILL.md:191` | **CORRECT** | Same anchor; the row's `MAX_ATTEMPTS` value `2` is corroborated by `attempts()≥2` at `:191`; `MAX_ATTEMPTS` itself is not a `SKILL.md` token (0 occurrences). |

### The three no-edit pairs

- `citation-bases.md:14` × `claim-gates.md:3` and `ops-invariants.md:18`: **correct to leave bare.**
  Lines 13-16 are the paragraph that forbids exactly these forms (“do not use a bare
  `ops-invariants.md:18` or `claim-gates.md:3` when the target is in the lane ... a bare cite of a
  file in a subdirectory classifies GONE”), and line 17-18 gives the qualified form. Qualifying the
  counter-example would destroy the documentation.
- `japanese-domestic-disclosure-workflow.md:7` × `japanese-domestic-disclosure-workflow.md`:
  **correct to leave bare.** Line 7 reads “adopts the staged package entry
  `japanese-domestic-disclosure-workflow.md` (`/home/vgpnk/Projects/shokuknow/merge/kasegi/`,
  read-only) ...”. It is a filename in a provenance sentence, not a lane-relative line citation.
  The named package root exists (`/home/vgpnk/Projects/shokuknow/merge/kasegi/`), and the entry is
  staged under it at `knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`, so the
  token is a real package filename; leaving it bare is right.

## Findings (routed; none re-scores C1's frozen predicate)

### F1. Tranche 8 fixed one token of the stale `SKILL.md:494-506` block and left the other four

The same stale EV block is still cited by rows 310-313 as `SKILL.md:498`, `:499`, `:500-501`, `:502`.
At `ae53b3c` those lines are RETRY_* requeue / RETIRE_AUTH / `docs/autopsies/<id>.md` text; the EV
terms moved to `:828-832` when `SKILL.md` grew from 546 lines (`7483333~1`) to 1251. This is the
same defect class the landed 454 edit repaired, still present four times. The full stale set is in
the next-tranche labels below.

### F2. Twenty-nine stale lane-root `SKILL.md:N` ties remain in `corpus/knowledge`

Next-tranche labels (independent, non-author): `.ufo/waves/round-93/w1/ReviewC1Labels-receipts/round94-labels.tsv`
— 29 `(line, key)` rows covering 31 stale range tokens (two rows carry comma-joined tokens), verified
against `ae53b3c` bytes: `ROUND94-LABELS-VERIFY rows=29 distinct_tokens=35 tsv_tokens=31
verified_correct=4 failures=0 PASS rc=0`.

Clusters:

- **Queue score / EV (the same 494-506 family):** 88, 89, 90, 433, 434 cite `SKILL.md:113-114`,
  `:175-176`, `:175`; 310-313 cite `:498`, `:499`, `:500-501`, `:502`; 460 cites `:113-117`.
  Correct current statements: `:182-184` (five-termed queue, with the explicit round-13 correction
  “earlier text omitted `is_live(1)`”), `:255-257` (curated is a boolean, never an EV magnitude),
  `:828-832` (formula), `:191` (attempts rule). Because `SKILL.md` now carries the round-13
  corrections, the affected `SUPERSEDES` cells need historical rewording, not only a token repoint.
- **Operator constants / ledger:** 143 and 151 (`:526` → `:251-253`; the `2 h` lease and
  `ufo_sighting:fleet-grid` are stated, `LEASE_MS`/`SESSION`/`GRID` names are not in `SKILL.md`);
  396 and 459 (`:245-247` → `:335-338`); 397 and 459 (`:146` → `:224-226`, `:246` → `:331-335`);
  390/394 (`:525` → `:321-324` / `:340-346`).
- **Schema / state / windows:** 355 and 356 (`:522` → `:999`; `SKILL.md` states the draft-07
  `additionalProperties:false` bullet but does not enumerate the required keys — the row's own Line
  column points at `schema.json:6` for the key list); 374 (`:111-112` → `:910-913`); 153 (`:14-15` → `:264-266`); 220
  (`:90-91` → `:157-158`); 267 (`:94-95` → `:161-162`).
- **Never-correct ties:** 435's `SKILL.md:10-11` is labelled `drop`: the phrase “EV ordering” occurs
  0 times in `SKILL.md` and no `SKILL.md` commit ever added or removed it (`git log -S` empty); the
  quoted phrase's source is `fleet-dispatch.mjs:10`, already cited. `:10-11` is record-count prose.
- **Off-by-one:** `considerthese-proposals-ledger.md:156` cites `SKILL.md:1163` twice; `:1163` is the
  `r46-c2-gate.py` row, and the `r46-landing-gate.py` row carrying “date-order (committer clocks
  only)” is `:1164`.

### F3. Most stale anchors were correct in the 546-line revision and shifted; three were never correct

At `7483333~1` (546 lines) the old `SKILL.md:90-91`, `:94-95`, `:113-117`, `:146`, `:175-176`,
`:245-247`, `:494-502`, and `:522` did carry the text the rows cite. The file is now 1251 lines, so
those anchors are line-number drift, not author error in the current tranche. `:525` and `:526` were
already weak file-inventory bullets (they named `ops/shared.mjs` / `fleet-dispatch.mjs` but not
`BANNED` or the `LEASE_MS`/`SESSION`/`GRID` constants). Exceptions that were never correct: `:10-11`
(old 10-11 already record-count prose), `:14-15` (old 14 was the “Pipeline” heading), and `:111-112`
(already board-staleness/dispatch-ordering prose at `7483333~1`, not the mission_state ladder).

### F4. “Only attempts statement” holds

Strict `attempts` occurs twice in `SKILL.md`: `:191` (the termination rule) and `:1000` (ledger
inventory prose mentioning “the sole in-repo consumer `attempts()` is regex-only”). Only `:191`
states the rule. `MAX_ATTEMPTS` = 0 occurrences; `LEASE_MS` = 0; `GRID` = 0; `SESSION` = 0;
`official_url` = 0; `1040` = 0 (last at `7483333~1:115`); `curated-EV` = 0 (last at `7483333~1:176`).
The 58/144 `MATCHES` ties are corroborative on the threshold (`≥2` = `MAX_ATTEMPTS = 2`); the
dispatch skip expression itself remains `fleet-dispatch.mjs:103, 46` in the rows' Line column.

### F5. Qualifier on the landed 454 range (no verdict change)

`:827-848` covers the prior claim's two components (formula + UNKNOWN fail-closed) and the
six-decimal `fmt` (`:843-844`), but the exit-2 paths (`:850-855`) and the non-persistence evidence
(`:807-811`) lie outside the range. Those are the triage entry's additions, not the prior claim's
“EV formula + UNKNOWN fail-closed”; the anchor is correct for the claim it prefixes.

## Claim checks I did not run (out of seat)

- I did not execute `knowledge-meter.py`; the C1 P1/P2/M-limb verdict remains the main agent's.
  The byte-level checks here are independent of the counter.
- The meter's M5 checks anchors are in range, not that they point at the named text, so the 31 stale
  tokens above are invisible to it by construction. That is why the next tranche needs content-level
  labels, not only an in-range check.

## Residual risk / gaps

- The stale set was derived from the worktree `corpus/knowledge`; `triage-thresholds.md` and
  `considerthese-proposals-ledger.md` are unmodified vs `ae53b3c` (`git diff --stat` empty), and the
  verifier re-reads every citing line from `ae53b3c` with `git show`.
- Old-revision comparison is a spot-check at `7483333~1` (the last 546-line SKILL), not every
  historical revision.
- The `drop` label for 435 is a judgment (no current target exists); an author could instead rewrite
  the cell to cite `fleet-dispatch.mjs:10` only.
- Row 356's schema-key tie stays weak even after repointing to `:999`; the next tranche should
  qualify or drop it.
- Sibling-seat worktree modifications exist (`LOG.md`, `SCORECARD.md`, C2 knowledge files, manifest);
  none were touched by this seat.

## Receipts

All under `.ufo/waves/round-93/w1/ReviewC1Labels-receipts/`.

| command (abridged) | observed |
|---|---|
| `git rev-parse` base/freeze/C1/C2 | rc 0, 4 commit hashes (`landing-diff.txt`) |
| `git diff-tree --no-commit-id -r --name-status ae53b3c` | rc 0, exactly 1 line: `M corpus/knowledge/triage-thresholds.md` (`landing-diff.txt`) |
| `git diff e15996b ae53b3c -- corpus/knowledge/triage-thresholds.md` | rc 0, 4 hunks, 5 insertions / 5 deletions (`landing-diff.txt`, 53 lines) |
| `cat -n .ufo/waves/round-93/c1/labels.tsv` | rc 0, 9 lines = header + 8 label rows (`labels-rows.txt`) |
| `python3` compare round-92 non-author vs round-93 labels | `header same True`, `first6 same True`; author appends rows 58/144 (`labels-vs-nonauthor.txt`) |
| `python3` cell extraction vs label payload | `CELL==LABEL437/438 row=5: True`, `row=6: True` (`cell-compare.txt`) |
| `git show ae53b3c:corpus/knowledge/intake-surface.md \| sed -n '85,95p'` | rc 0 (`anchors-437-438-454.txt`, 106 lines) |
| `git show ae53b3c:SKILL.md \| sed -n '173,180p'` | rc 0 (`anchors-437-438-454.txt`) |
| `git show ae53b3c:corpus/knowledge/mission-control.md \| sed -n '50,60p'` | rc 0 (`anchors-437-438-454.txt`) |
| `git show ae53b3c:SKILL.md \| sed -n '820,860p'` and `490,510p` | rc 0 (`anchors-437-438-454.txt`) |
| `git show ae53b3c:SKILL.md \| sed -n '185,195p;108,120p'` | rc 0 (`anchors-58-144-noedit.txt`, 68 lines) |
| `git show ae53b3c:SKILL.md \| grep -c MAX_ATTEMPTS` | count 0, grep rc 1 (`final-counts.txt`) |
| `git show ae53b3c:SKILL.md \| grep -n attempts \| wc -l` | 2 lines (`:191` rule, `:1000` inventory) (`final-counts.txt`) |
| `git show ae53b3c:corpus/knowledge/citation-bases.md \| sed -n '10,20p'` | rc 0 (`anchors-58-144-noedit.txt`) |
| `git show ae53b3c:corpus/knowledge/japanese-domestic-disclosure-workflow.md \| sed -n '1,9p'` | rc 0 (`anchors-58-144-noedit.txt`) |
| `find /home/vgpnk/Projects/shokuknow/merge/kasegi -maxdepth 5 -name '*japanese-domestic*'` | rc 0; entry found at `knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md` (`staged-path.txt`) |
| `python3` enumerate every `SKILL.md:N` token in `corpus/knowledge` | 34 raw occurrences, 24 distinct raw anchors; `SKILL.md` 1251 lines (`stale-scan.txt`, 65 lines) |
| `git show 7483333~1:SKILL.md \| sed -n` (8-20, 88-120, 143-149, 173-178, 243-248, 494-506, 520-528) | 546 lines at that rev; every quoted old line saved (`old-skill-7483333.txt`, 97 lines) |
| `sed -n '803,815p' SKILL.md` | rc 0; `:807-811` = “persists nothing — it imports only `readFileSync`/`existsSync` ... `process.exit(0)`” (`skill-803-815.txt`) |
| `sed -n '8,20p' SKILL.md` and `sed -n '1000p' \| grep -o` | rc 0; `:10-11` record-count prose; `:1000` = “the sole in-repo consumer `attempts()` is regex-only, so the fleet never notices” (`skill-8-20-and-1000.txt`) |
| `grep -F` token locations + `git log -S` | 0 matches for `EV ordering`, `curated-EV`, `1040`, `GRID`, `SESSION`, `official_url`, `MAX_ATTEMPTS`, `LEASE_MS`; `formation` only inside “informational”; `git log -S 'EV ordering'` empty (`token-locations.txt`) |
| `sed` all proposed target ranges | rc 0, 178 lines (`target-ranges.txt`) |
| `sed` every citing row at `ae53b3c` | rc 0, 89 lines (`citing-rows.txt`) |
| `python3 -B verify-round94-labels.py` | `ROUND94-LABELS-VERIFY rows=29 distinct_tokens=35 tsv_tokens=31 verified_correct=4 failures=0 PASS`, rc 0 (`verify-round94-labels.txt`) |
| `sha256sum round94-labels.tsv` | `41bc438b04b0531a74bb9e52550fb968c0c818fee3aa315ad7ba99cd527a556b` (`file-inventory.txt`) |
| `wc -l` receipts | TSV 30 lines (header + 29 rows), 5 fields each (`file-inventory.txt`) |
