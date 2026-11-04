# ScopeConnect — round 64 read-only overlap scan (proposal2 + domain trial + metric gap)

Seat: ScopeConnect (connector, leaf, read-only). Base `d74be00a82c8c2962a0b78442c5daea3af0adaae`. Measured on a `git archive` export of that base in scratch; the lane working tree was not modified. Raw receipts (one invocation each, `run-utc` printed): `.ufo/waves/round-64/w1/ScopeConnect/`. No production, fleet, sibling or shokuknow write. No tool installed.

## Axes named

1. Domain-trial strength for finding qualification (depth:verifiability, input side).
2. Metric gap actually read by the axis counter (depth:verifiability, output side).
3. Sibling/province overlap for command-aware failure diagnosis (overlap risk only).

## 1. proposal2 status

- Source: `considerthese/2026-10-26.md:30` ("Run one end-to-end domain task round … six-file claim package … price through F13/F17/F18 … rebuild a minimal claim checker").
- Already landed in part: claim-checker rebuilt as `corpus/instruments/claim-package-check.py` (r43, commit `5b4a850`). Its blocker, "blocked on a green exemplar" (`corpus/knowledge/considerthese-proposals-ledger.md:115`), is no longer present: `claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` → `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`; `--selftest` → `cases=10 failures=0` (`w1/ScopeConnect/claim-package-exemplar.txt`).
- Still open: a real public disclosed report built into a six-file package and priced. LOG r62/r63 and the ledger (`:170`) keep it "partially landed / domain task open"; SHONEN box 2 unchecked (`SHONEN.md:7`).
- The S094 review (r63 handoff, r64 driver) is documentation-only and is not that task; its own handoff says so (`.ufo/waves/round-63/domain-review-handoff.md`, "Handoff boundary").

## 2. Existing real domain trial — what it exercises today

Two parallel trials on the same source, with different byte bases:

| Trial | Engine | Bytes | Figures / checks | Exercises command-aware failure? |
|---|---|---|---|---|
| r63 `controls/domain-review-ledger-r63.json` | `figure-audit.py` | committed `git show fdccc6da…` | 4 figures, all `grep -F … \| wc -l`, all `want 1` | Only the positive path. Prefreeze 4/4 (`controls/domain-trial-candidate-prefreeze-r63.txt`). |
| r64 `.ufo/waves/round-64/domain-qualification.py` | plain Python | working-tree `corpus/source-snapshots/round-61/S094.txt` | 7 phrase-at-line checks + 4 "arithmetic" checks; receipt `controls/domain-qualification-r64.txt` 11/0 | No. Does not call figure-audit; no rev pin; not in `verify-r64.py` PATHS. |

Defects found by fixture (`w1/ScopeConnect/domain-qualification-fixtures.txt`, scratch copies only):

- **ARITHMETIC block is tautological.** `domain-qualification.py:34-39` hard-codes `expected` booleans and recomputes `0 <= index <= 2` from literals; no source byte is read. 4 of 11 counted checks cannot fail unless the script is edited. The count `checks=11` overstates source grounding.
- **Truncated source → uncaught IndexError, exit 1.** Variant B (S094 cut to 100 lines): traceback `IndexError: list index out of range`, exit 1, no `QUALIFICATION` summary. The documented contract (exit 2 = unreadable) is not met; only OSError/UnicodeError are caught (`:14`).
- **Line-shift is detected** (variant C, one blank line inserted: 7 FAIL, exit 1), **missing file → exit 2** (D), **non-UTF-8 → exit 2** (E), **one drifted phrase → FAIL exit 1** (F). Good.
- **No absence (want-0) figure exists in either trial.** Every r63 figure is a positive count. That is the class where "missing input reads as zero" matters most.

S094 anchors re-checked against the capture: lines 18, 29, 106, 110, 112, 113, 118 match the quoted phrases; manifest sha256 `663ac16d…e804` matches (`corpus/source-snapshots/round-61/manifest.json`).

## 3. Discriminating probe on the HEAD instrument (predata, not scored)

Ledger `w1/ScopeConnect/neg-ledger-probe.json`, run with `figure-audit.py` at d74be00 on the export (`w1/ScopeConnect/neg-figure-probe-base.txt`):

| figure | derive shape | want | HEAD result |
|---|---|---|---|
| pos-present-rev | `git show <rev>:S094 \| grep -F … \| wc -l` | 1 | ok |
| neg-WT-present-absent-phrase | `cat S094 \| grep -F 'SQLite users were impacted' \| wc -l` | 0 | ok (correct zero) |
| **neg-WT-missing-source-cat** | `cat NOPE.txt \| grep -F … \| wc -l` | 0 | **ok — false green** |
| neg-WT-missing-source-grep | `grep -F … NOPE.txt \| wc -l` | 0 | stale, `derive-upstream-exit-2` |
| neg-rev-missing-path | `git show <rev>:NOPE \| …` | 0 | stale, `derive-upstream-exit-128` |
| neg-rev-bad-ref | `git show 000…1:… \| …` | 0 | stale, `derive-upstream-exit-128` |
| pos-WT-want1-absent-phrase | control | 1 | stale (derived 0) |

- The false green is the r64 target class: upstream `cat` exit 1 on a missing file is ignored at HEAD, so a negative qualification passes on an absent source. Under the r64 rule (positive upstream exit >1 except grep exit1) the cat-first row is expected stale and `grep -F … | wc -l` on an existing file still counts zero. [INFERENCE — candidate not built or run by this seat.]
- Use `grep … | wc -l` for negatives. `grep -c` with zero matches is a final-stage exit 1 and reads stale (`derive-exit-1`), which is not the intended zero-count observation.
- `'SQLite users were impacted'` is a valid absence probe: the source says `so SQLite users were not impacted.` (S094.txt:18), so zero matches is the correct reading. Other candidate phrases ("general superiority", "superior", "agents outperform", "released user") all count 0 in S094 (counts taken this run), so they are not discriminating on their own.

## 4. Suggested extension (finite, predata only)

E1 — fold the domain trial into the command-aware engine instead of a separate Python check:
- Rev-pinned positive figures for the four r63 qualifications (unchanged).
- One source-grounded negative: `SQLite users were impacted` want 0 (above).
- One **missing-source absence** figure in cat-first form (`cat <missing> | grep -F … | wc -l`, want 0). This is the only probe in the trial that separates HEAD from the r64 rule at domain level. Pre-freeze it must be a control: base green, expected candidate stale. Do not score it.
- Replace the ARITHMETIC block with a source-grounded figure or delete it and state the count honestly.
- If the trial is retained as committed-input evidence, add `corpus/source-snapshots/round-61/S094.txt` to `verify-r64.py` PATHS (currently absent; `verify-r64.py:17-26`). Today the domain trial is outside the r64 closure.

E2 — exit-code hygiene: if domain-qualification.py survives, wrap the indexing in the same unreadable-source path so truncation exits 2, not an uncaught 1.

Caveat: negative figures prove absence only within the pinned capture; the S094 capture is the only evidence used. No new discovery, severity, reward or exploitability is implied.

## 5. Remaining actual metric gap

- Score-5 gate (`SCORECARD.md:331`): `score-gap.py` on d74be00 prints `gap: 22 of 81 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` (`w1/ScopeConnect/score-gap-base-d74be00.txt`). Figure-audit or domain-trial moves do not change this counter (R58, `corpus/QUALITY.md:415`). Restoring the 22 needs lost roots (`~/Projects/bounties`, `the-bounty-hunter`, `origin-work`); no source-restoration claim is made here.
- Counter-level red found on the same base, not named by the 22-gated figure: `recheck-audit.py --root <export>` exits **1** with `lines=81 total=81 pass=72 fail-closed=22 … cwd_fail=9 … exit=1` (`w1/ScopeConnect/recheck-audit-base-d74be00.txt`). Nine entries fail the frozen cwd limb (`foreign=2`): cisa-vulnrichment-adp-enrichment, cisa-vulnrichment-record-list, github-repository-security-advisories-rest-api, nvd-api-2.0-response-schema, nvd-api-2.0-retrieval-interface, openssf-scorecard-checks, osv-affected-range-events, project-zero-big-sleep-sqlite-variant-analysis, project-zero-fuzzilli-vs-bigsleep-comparison.
- The S094 entry's recheck `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-61/manifest.json --source S094` exits 0 from the lane root and **2** from `/` (`w1/ScopeConnect/s094-recheck-foreign-cwd.txt`: `can't open file '/home/vgpnk/Projects/shokunin/corpus/instruments/source-recheck.py'`). Its r60 sibling (S093) uses the same no-`cd` convention, which the r60 entry records as intentional (`project-zero-fuzzilli-vs-bigsleep-comparison.md:6`).
- Not verified: whether the 9 cwd-limb FAILs were acknowledged anywhere. I grepped LOG.md and the r60/r61 lessons for `recheck-audit`; only `gated=22` appears, which is not exhaustive. Repair options (absolute `cd` prefix, which the r62 lesson records as host-bound, or instrument-side root resolution) are planner/operator choices; none is recommended as a claim here.
- Ledger-closure note for r64: every non-rev derive input in the current figure ledger is already in `verify-r64.py` PATHS (5 paths, `w1/ScopeConnect/ledger-closure-vs-verify-r64.txt`). The domain-trial inputs are not. `.ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py` (PATHS entry) does not yet exist.

## 6. Sibling and province overlap

- No duplicate Big Sleep / SQLite / generate_series coverage in kengaku, kagi, kake, chousa, mado or tameshi corpora (grep: 0 matches). PROVINCE lists kengaku as the LLM-evaluation adjacent lane (`PROVINCE.md` "Adjacent"). The S094:118 "not general superiority" qualification is an LLM-benchmark claim; if it is ever admitted as knowledge, route it through kengaku's bar rather than absorbing it here.
- pipefail / PIPESTATUS semantics exist in siblings: mori-shokunin `corpus/SOURCES.md:76,81` (`S070`/`S075`, GNU Bash manual) and `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`; tsukuroi-shokunin `corpus/SOURCES.md` `S256`/`S257`; kengaku-shokunin `corpus/lessons/round-60.md:40` (PIPESTATUS receipts rule); shokuknow scopes `corpus-expansion-8/9` ScoutSouji (`head -1` SIGPIPE, exit 141). These confirm the negative-status class is separate. figure-audit's `returncode > 1` already ignores negative (signal) statuses, consistent with `figure-audit.py:38-44`. Figure-audit is NOT a pipefail implementation; if the lesson cites pipefail semantics, open the GNU Bash manual freshly into kasegi's own registry instead of reusing mori's S070/S075.
- shokuknow was read-only and not re-scanned beyond the grep hits above.

## Concise references

- considerthese/2026-10-26.md:30 (proposal2); corpus/knowledge/considerthese-proposals-ledger.md:115, :170
- corpus/instruments/claim-package-check.py; corpus/instruments/fixtures/claim-package/exemplar (8/8 WELL-FORMED)
- .ufo/waves/round-63/domain-review-ledger-r63.json; .ufo/waves/round-63/domain-review-handoff.md
- .ufo/waves/round-64/domain-qualification.py:14, :34-39; controls/domain-qualification-r64.txt
- corpus/instruments/figure-audit.py:38-44 (exit rules), :106-109 (upstream >1), :412-424 (r63 cases)
- .ufo/waves/round-64/verify-r64.py:17-26 (PATHS)
- SCORECARD.md:331 (score-5 bar); corpus/QUALITY.md:415 (R58)
- corpus/source-snapshots/round-61/S094.txt:18,29,106,110,112,113,118; manifest.json sha 663ac16d…e804
- corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md:5; project-zero-fuzzilli-vs-bigsleep-comparison.md:6

## Verification

Read-only commands only; receipts with run-utc in `.ufo/waves/round-64/w1/ScopeConnect/`:
`score-gap-base-d74be00.txt`, `recheck-audit-base-d74be00.txt`, `s094-recheck-foreign-cwd.txt`, `neg-figure-probe-base.txt` (+ `neg-ledger-probe.json`), `domain-qualification-fixtures.txt`, `claim-package-exemplar.txt`, `ledger-closure-vs-verify-r64.txt`.
Main agent should not treat any of these as candidate evidence; they are predata context. Scratch `/fast/scratch/hyaku/kasegi-r64/ScopeConnect/` is removed after receipts are copied.
