# C1 semantic review — round 89 attempt 1 (seat ReviewC1Labels)

Commits: base `090a46f89932324787e00ca20b1007f893934c9a`, freeze `94573d2573dc6cca83454cc65b787d37d96988f5`,
C1 landing `eb5f0df8eaceca617465e493c710e8626e9aa618`. Judged only at the landing commit; findings below are
routed defects and qualifiers, never re-scoring. No lane file was edited.

Method: `git diff 94573d25 eb5f0df8 -- corpus/knowledge/`; every cited range read from
`git archive eb5f0df8 corpus/knowledge` in scratch; citing sites enumerated over `corpus/knowledge/*.md` at the
landing rev; `labels.tsv` checked mechanically against `ReviewC1Semantics.md` at `d0d9f49`; the 785/1797 identity
re-derived from the token scan. Receipts in `ReviewC1Labels-receipts/`.

## 0. Landing shape (pass)

- `git diff --stat 94573d25 eb5f0df8` = **1 file, 9 insertions / 9 deletions**, all
  `corpus/knowledge/triage-thresholds.md`. The 9 changed lines carry **10 citation tokens** (row 178 carries two keys).
- Base and freeze are identical on `corpus/knowledge/` (0 diff lines), so all 9 keys are bare at both. The 5 WRONG
  keys were qualified at the r88 landing `fd33e1bf` and reverted before the r89 base; the 4 FN keys were already
  bare at `fd33e1bf` (they were r88 exclusions, never applied). The landing re-applies all 9 with corrected values.
- No stale bare or qualified form of the 9 keys remains at the landing, except the composite token in F1; no
  adjacent-range token exists (`:34-35`, `:35-37`, `:63-67`, `:66-68`, `:28-30`, `:10-12`, `:9-17`, `:17-26` all
  absent).

## 1. The 9 pairs — all CORRECT

| map pair (key → value) | citing line | cited line text at landing | verdict |
|---|---|---|---|
| `claim-gates.md:34` → `:35` | 222 (decision digest) | L35 "`decision_sha256` matches `/^[a-f0-9]{64}$/i`." | **CORRECT** |
| `claim-gates.md:35-36` → `:36-37` | 225 (manifest binding) | L36-37 "`head_sha256` = final decision's `decision_sha256` = `manifest.expected_head_sha256` — three-way binding." | **CORRECT** |
| `claim-gates.md:63-66` → `:78-80` | 276 (not-claimable heuristics) | L78-80 "Not-claimable heuristics (any triggers error): `claimable===false`, `not_claimable`, `do_not_submit`, `claimability_gap`, `finding_count===0`, verdict matching `/not[-_\s]?claimable\|honest[-_\s]?zero/i`." | **CORRECT** |
| `claim-gates.md:66-67` → `:81-85` | 277 (prior submission) | L81-85 "Prior-submission guard: `submission_performed`, `submitted_url`, or `submission_state:'SUBMITTED'` fails; PLUS a **global** scan of all `claims/*/*/status.json` … duplicate (L184–199)." | **CORRECT** |
| `claim-package-contract.md:28-29` → `:52-53` | 269 (hard gates) | L52-53 "- `claim_review.hard_gates`: `written_scope`, `authorization`, `evidence_integrity`, `no_duplicate_or_prior_submission`." | **CORRECT** |
| `claim-gates.md:10-11` (prefix) | 178 (required files), 179 (manifest file) | L10-11 "Required: `report.md`, `claim_checklist.md`, `custodian-receipts.json`, `provenance.json`, `status.json`, `evidence/manifest.json` (L22–24)." | **CORRECT** |
| `claim-package-contract.md:15` (prefix) | 241 (provenance boundary) | L15 "`provenance.json` \| Agents + requested/resolved models per transition, commands + exit codes, pin (remote + commit), `policy_sha256`, `external_effects_performed: []`, secrets attestation." | **CORRECT** |
| `claim-package-contract.md:9-16` (prefix) | 178 (six required files) | L9-16 the six-file table (`report.md` … `status.json`) | **CORRECT** (see F1) |
| `ops-invariants.md:17-25` (prefix) | 455 (shared constants table) | L17-25 the constants table: delimiter row + `BANNED` … `appendLedger` (3500-byte cap) | **CORRECT** |

Pair notes (none changes a verdict):

The 9/9 CORRECT result confirms the C1 claim's "all CORRECT-target labels" statement at the landing commit.

- **`:35-36` → `:36-37`**: the r88 verdict was WRONG **1/3** (review line 46): sites 223/224 are correct at
  `:35-36` and only the bare site 225 needed `:36-37`. The landing changes only 225; 223/224 keep
  `corpus/knowledge/claim-gates.md:35-36`. Outcome correct, but see F2.
- **`:66-67` → `:81-85`**: the range also covers the global-duplicate clause, which is the *next* row's content
  (278 still cites `:67-70` — labelled WRONG in tranche 5). L81-82 would be the minimal range for row 277;
  over-coverage, not error.
- **`claim-package-contract.md:15`**: `schema_version` is not on L15, but the citing sentence re-cites it at `:13`
  in the next sentence, so the `:15` attribution is exact.
- **`ops-invariants.md:17-25`**: L17 is the table delimiter row (header is L16); all eight data rows are inside.
  Range is one line short of the header, not of the content.

## 2. `labels.tsv` vs the r88 review — 9/9 bound

Every row binds mechanically: the review line holds the cell `| <key> |`, the class marker (`**WRONG` /
`proxy false negative`), the value anchor as a whole token `L<n>` / `L<n>-<m>`, and the FN rows' anchor equals
the key anchor (WRONG rows' anchors differ). Receipt `labels-binding.txt`. One qualifier: F2.

## 3. Tranche-5 labels — 39 keys / 46 citing sites (R140 next-round input)

All 39 r88 `anchor-content-drift` exclusions **not** sampled by `ReviewC1Semantics` (54 − 15) are labelled at
`ReviewC1Labels-receipts/tranche5-labels.tsv`, one row per citing site:

| verdict | sites | keys |
|---|---|---|
| WRONG | 40 | 33 |
| UNCLEAR | 3 | 3 |
| CORRECT | 2 | 2 |
| MENTION (bare-form quotation) | 1 | 1 |

**All 33 WRONG keys have a supporting range in the same entry**; the only sites with none are two of the three
`mission-control.md:13-14` rows (`MAX`, `STAGGER_S` — the entry never states either default). Systematic patterns,
all consistent with entry growth:

- `claim-gates.md` status.json block: citations point at the secrets/symlink block (L51-61); the gates are
  **L67-77** (+16 offset). Rows 261-270 and 278-279.
- `ev-model.md`: citations point at the round-15 anchor-base paragraph (L6-11) or the formula lines' neighbours;
  the formulas are **L14-18** and the schema facts **L22-23**.
- `mission-control.md`: limit/routing/lease citations point at the sweep/P20-P21 block (L37-45); the content is
  **L29, L36, L40, L55-57, L59-60, L61-66**.
- `intake-surface.md`: the queue-score citations point at the census (L68-79, L72); the score is **L80-85**.
- `claim-package-contract.md`: `:25`→L31-34, `:27`→L24-26, `:30`→L54.

This is next-round input, not a finding against C1: `claims.json` `routed_defect_disposition["4"]` explicitly
keeps "the 39 unsampled drift exclusions" out of round 89. What the sample adds is the opposite failure from the
r88 review's 4 proxy false negatives: the lexical rule also **suppressed 33 real drifts**, so the exclusion
hides broken citations rather than merely leaving good ones bare.

## 4. Findings

**F1 — Medium — the `claim-package-contract.md:9-16` prefix repoint is incomplete: one bare citation of the same
entry survives at landing.**
`corpus/knowledge/triage-thresholds.md:457` still reads
```| six-file package contract | `claim-package-contract.md:9-16, 28-38` | MATCHES for gate-enforced rows; … |```
while line 178 was repointed to `corpus/knowledge/claim-package-contract.md:9-16`. Cause: `apply-map.py` replaces
only the backticked exact key, and this token is composite (`:9-16, 28-38` inside one backtick span); `resolve.py`
`is_pathlike` rejects it (space, no `/`), so the counter neither counts nor repoints it — it is outside the meter's
denominator at both revs, and no predicate is falsified. Impact: one file now cites the same entry qualified (178)
and bare (457) — the inconsistency class the r88 review used to justify the FN verdict for `:15`.
Re-run: `git show eb5f0df8:corpus/knowledge/triage-thresholds.md | sed -n '457p'`.

**F2 — Low — the `claim-gates.md:35-36` label loses the site fraction.**
The r88 verdict is WRONG **1/3**; `labels.tsv` records class `WRONG` with no fraction and M9 accepts it. The
landing outcome is right (only the bare site 225 changed), but a later round keyed on the label could "re-anchor"
the qualified token `corpus/knowledge/claim-gates.md:35-36` (2 sites, both correct) into `:36-37` and break them.
Re-run: `git show eb5f0df8:corpus/knowledge/triage-thresholds.md | sed -n '223,225p'`.

**F3 — Low — row 249 asserts the symlink gate is uncovered; the entry states it.**
`triage-thresholds.md:249` ends "— (new; `claim-gates.md:42-47` covers the regex only)", but
`claim-gates.md:54-55` reads "**Blanket symlink ban**: any directory entry that is a symlink errors without
traversal (L104-105)". The correct corpus tie is `corpus/knowledge/claim-gates.md:54-55`; the row was excluded by
the lexical rule and never checked. Re-run: `git show eb5f0df8:corpus/knowledge/triage-thresholds.md | sed -n '249p'; git show eb5f0df8:corpus/knowledge/claim-gates.md | sed -n '54,55p'`.

**F4 — Low — two stale SUPERSEDES rows for the peak model.**
`triage-thresholds.md:155` and `:438` assert `mission-control.md:37-38` "writes `openai-oauth/gpt-6-astra:max`".
The entry at landing writes `openai-codex/gpt-6-astra:max` and records the round-13 correction
(`mission-control.md:55-57`), and L37-38 is the sweep, not the model routing. Both the range and the SUPERSEDES
premise are stale. Re-run: `git show eb5f0df8:corpus/knowledge/triage-thresholds.md | sed -n '155p;438p'; git show eb5f0df8:corpus/knowledge/mission-control.md | sed -n '55,57p'`.

**Info — the 785/1797 identity is mechanically reproducible** from the token scan: 9 tokens removed (all map keys),
8 added (all map values except `corpus/knowledge/claim-package-contract.md:15`, which already existed at base via
`corpus/knowledge/claim-package-gate.md:15`); 1798 − 9 + 8 = 1797, and the 8 new tokens are the INTERNAL additions
(777 + 8 = 785). Receipt `token-arithmetic.txt`.

## 5. Residual risk and verification gaps

- I did not run `knowledge-meter.py` (P1); the L1 receipt carries it. I re-implemented its token scan and label
  binding and reproduced the M1 identity, M2/M3 semantics and M9 pass condition, but did not re-execute
  `resolve.classify` for the ~1800 targets.
- M9 is lexical by construction: it requires the review line to contain the cell, the class marker and the value
  anchor as `L<n>`, not that the anchor is asserted *correct*. A sentence naming a range as wrong would also bind.
  Inherent to the frozen predicate; the non-author source is what raises it above the r88 proxy.
- F1 is invisible to both `apply-map.py` and the counter; any future composite citation (`name:a-b, c-d` in one
  backtick span) will be repointed by neither.
- Tranche-5 verdicts are mine alone (single reviewer, no second label); the supported ranges are line-level and
  should be re-read at the next landing before use.
- C2 is outside this seat; not examined.
- Scratch `/fast/scratch/hyaku/kasegi-r89/ReviewC1Labels` was removed before this report (trap on exit).

## Files written

- `.ufo/waves/round-89/w1/ReviewC1Labels.md` (this report)
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/tranche5-labels.tsv` (39 keys / 46 sites)
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/labels-binding.txt`
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/token-arithmetic.txt`
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/key-scan-base-freeze-landing.txt`
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/stale-and-nearmiss.txt`
- `.ufo/waves/round-89/w1/ReviewC1Labels-receipts/unsampled-39-enum.txt`
