# ReviewC1Labels — round-92 wave 1: non-author labels for the round-93 C1 tranche (R140)

Seat: ReviewC1Labels (leaf, non-author). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Pinned rev: `cb1ef2b9856df79c530f3ff1374fa9691ff56233` (C1 landing; base 0628fd2, freeze 9e4f0d6).
No lane edits and no git/jj writes: `git show` / `git archive` read-only only. Frozen `c1/`, `c2/`, `controls/`, `l1/` bytes untouched.

## Deliverables (all under `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/`)

- `round93-labels.tsv` — the labels, 5 columns (`line, key, label, fix, evidence`): 6 rows = 3 label-named edits + 3 no-edit.
- `round93-candidate-lines.txt` — derived post-edit citing lines (437, 438, 454) with per-line sha256; derived, **not applied**.
- `verify-labels-r93.py` + `verify-labels-r93.txt` — verifier and its output (`VERIFY PASS checks=55 failures=0`), reproduced from the receipted copies.
- `list-gone-keys-r93.py` + `gone-r93.txt` — the round-91 GONE scan re-pointed at cb1ef2b9.
- `knowledge-meter-measure-cb1ef2b9.txt` — measure-mode readout.
- `secret-scan-r93.txt` — landed scanner over every receipt file.

## Readings at cb1ef2b9

```
python3 -B .ufo/waves/round-92/c1/knowledge-meter.py --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --measure-rev cb1ef2b9856df79c530f3ff1374fa9691ff56233 --work $S
KNOWLEDGE-METER rev=cb1ef2b9856df79c530f3ff1374fa9691ff56233 rate=960/1944 pct=49.38 mirror_absent=True pinned=archive
HOST rev abs_tokens=127 abs_nongone=23
```
The measure-mode reading of the landing commit equals the frozen C1 `--target 960/1944`.

GONE bare-key scan (round-91 script, re-pointed at cb1ef2b9): `DISTINCT_GONE_BARE_KEYS 5 / SITES 5` — exactly the residual set below. There is no sixth site.

## Labels

| citing site | key | label | edit named |
|---|---|---|---|
| triage-thresholds.md:437 | `intake-surface.md:75-76` | `cell-repair` | replace last cell with `corpus/knowledge/intake-surface.md:89-93` + `SKILL.md:176-178` text (exact text in TSV) |
| triage-thresholds.md:438 | `mission-control.md:37-38` | `cell-repair` | replace last cell with `corpus/knowledge/mission-control.md:55-57` text (exact text in TSV) |
| triage-thresholds.md:454 | `SKILL.md:494-506` | `SKILL.md:827-848` | repoint token `SKILL.md:494-506` → `SKILL.md:827-848` |
| citation-bases.md:14 | `claim-gates.md:3` | CORRECT | none (deliberate counter-example) |
| citation-bases.md:14 | `ops-invariants.md:18` | CORRECT | none (deliberate counter-example) |
| japanese-domestic-disclosure-workflow.md:7 | `japanese-domestic-disclosure-workflow.md` | CORRECT | none (merge-input name, not a cite) |

Exact replacement cell text (also in the TSV, byte-for-byte):

- 437: `` `corpus/knowledge/intake-surface.md:89-93` (round-13 correction: `reward` object on 48 but numeric `reward.min` on only 14 — the reward-exists≠reward.min-numeric conflation, superseding the earlier "`reward.min` present on 48"), `SKILL.md:176-178` (`reward` object exists on 48 records but numeric `reward.min` on only 14 — round-13 correction) ``
- 438: `` `corpus/knowledge/mission-control.md:55-57` (peak → `openai-codex/gpt-6-astra:max`; the round-13 correction records that earlier text said `openai-oauth/`) ``

## Findings (routed; each re-runnable)

1. **Both errata anchors are stale at every rev checked, so the only edit that keeps the errata row true is a full-cell replacement.** `intake-surface.md:75-76` is the name-drift bullet at cb1ef2b9, at 8a1a00c, 0628fd2 and 7483333; the quoted wording "`reward.min` present on 48" was at `intake-surface.md:72` at fb9ac8e (round 11). 437's second reference `SKILL.md:111` is a `claim_checklist.md` line at cb1ef2b9, not the reward sentence; that sentence is `SKILL.md:176-178`. `mission-control.md:37-38` is the sweep bullet at cb1ef2b9, 8a1a00c, 0628fd2, 7483333 and 7483333~1; the pre-round-13 `openai-oauth/gpt-6-astra:max` was at `:50-52` at 7483333~1, and the corrected peak model plus its correction note are at `:55-57`. A token-only qualification would keep a false quote attached to the new anchor (the frozen round-92 EXCLUDED reason), so both rows are `cell-repair` with the exact full last-cell text.
   Re-run: `python3 -B $S/list-gone-keys-r93.py $S`; `git -C <lane> show fb9ac8e:corpus/knowledge/intake-surface.md | sed -n '72p'`; `git -C <lane> show 7483333~1:corpus/knowledge/mission-control.md | sed -n '50,52p'`; `git -C <lane> show cb1ef2b9:SKILL.md | sed -n '111p;176,178p'`.
2. **Row 454's second token never states the EV formula at cb1ef2b9.** `SKILL.md:494-506` is `ops/park-disposition.mjs` RETRY_TRANSIENT/REVIEW text and the autopsy seven-part body; the strings `p_success`, `gross_value`, `total_cost`, `adjusted_ev` do not occur on 494-506. The formula is `SKILL.md:828-832` (Triage-economics section, starts 805) and the UNKNOWN fail-closed sentence is `846-848`; the label is `SKILL.md:827-848` (fence + formula + terms/guards + fail-closed sentence). Six-decimal `fmt` is 843-844, exit-2 paths 850-855, non-persistence 807-811.
3. **Residual GONE sub-kind after R140:** the 2 errata sites gain label-named edits; the 3 no-edit sites (`citation-bases.md:14` ×2, `japanese-domestic-disclosure-workflow.md:7`) stay GONE by design — the paragraph and the sentence they sit in document the bare forms as the counter-example. So the sub-kind retains exactly 3 GONE sites after this tranche; any later counter must not expect zero.

## Qualifiers for the round-93 counter

- `EXCLUDED` is empty for R140: the frozen exclusion reason is removed because the edit is a full-cell rewrite with the quote corrected at the new anchor, not a repoint under a stale quote.
- New kind vocabulary the frozen round-92 meter does not implement (it would return `unknown` — a loud failure, never a silent wrong edit):
  - `cell-repair`: `fix = "Replace cell with: <EXACT new last-table-cell text>"`; old value = the citing line's current last `|`-cell, stripped; the replacement must not contain `|`.
  - `SKILL.md:N-M` as a `label`: same range rule as `corpus/knowledge/<name>.md:N-M` (old `` `<key>` `` → new `` `<label>` ``), but the target is a lane-root file, so the `corpus/knowledge/` prefix test must not be the only range predicate.
- Candidate lines + sha256 are in `round93-candidate-lines.txt` (437 `022538831b9eef1f6a34d07ec679c71ea30dd768b44dfb81b74013566000145b`, 438 `9d0d80117ef3b019320a09373e643bfccfa9a8c48725bc1a77e5fdc416ba74a2`, 454 `851d6892a5228aa331e191ea967a5bbf0c777943814db7ef74bfb3e423f529f4`).
- The 437 cell replacement drops the stale `SKILL.md:111` token (a claims line). Keeping it would leave the errata row false; the new cell uses `SKILL.md:176-178`.

## Verification (`verify-labels-r93.py`, receipted output)

`VERIFY PASS checks=55 failures=0` (rc=0), run on the receipted copies. The verifier proves:
- 6 rows, 5 columns each, unique `(line, key)`; each key token occurs exactly once on its citing line at cb1ef2b9.
- The 5 non-SKILL keys are GONE and name an existing `corpus/knowledge/` entry; the GONE site set re-derived independently equals the 5 labelled sites exactly.
- Every named range in `label`, `fix` and `evidence` lies inside its entry (claim-gates 160, ops-invariants 141, intake-surface 179, mission-control 171, SKILL.md 1251 lines).
- Both cell rows' current last cells equal the frozen old cells byte-for-byte, and the replacements apply with the pipe count unchanged (5 → 5).
- Every quoted claim exists at its cited lines; the superseded wording exists at fb9ac8e:72 and 7483333~1:50-52.
- `SKILL.md:494-506` states no EV term; `SKILL.md:827-848` carries all four formula lines and the UNKNOWN fail-closed sentence.
- The 3 no-edit rows carry the `No edit` fix (unmapped by construction).

## Residual risk / gaps

- The two errata rows are historical records: the superseded wording is no longer anywhere in the current entries (corrected in round 13), so it is attributed as earlier text and anchored in history (fb9ac8e:72, 7483333~1:50-52). A stricter rule demanding the quote still exist at the cited current lines cannot be satisfied.
- The residual sub-kind stays at 3 GONE sites by design (finding 3); a round-93 target of zero for this sub-kind would be wrong.
- No claim is made about the depth score; this is citation repair only.

## Hygiene

- Landed scanner over all 7 receipt files: `CAPTURE-SECRET-SCAN mode=files scanned=7 hits=0 files=0 allowed=0 unused_allow=19 rc=0`. No fixture bytes, no credential-shaped value, no copy of the scanner/counter/snapshot into the wave dir.
- No network, no tool installs, no sudo, no host mutation. Scratch `/fast/scratch/hyaku/kasegi-r92/ReviewC1Labels` deleted before yield.

## Files written

- `.ufo/waves/round-92/w1/ReviewC1Labels.md` (this report)
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/round93-labels.tsv`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/round93-candidate-lines.txt`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/verify-labels-r93.py`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/verify-labels-r93.txt`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/list-gone-keys-r93.py`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/gone-r93.txt`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/knowledge-meter-measure-cb1ef2b9.txt`
- `.ufo/waves/round-92/w1/ReviewC1Labels-receipts/secret-scan-r93.txt`
