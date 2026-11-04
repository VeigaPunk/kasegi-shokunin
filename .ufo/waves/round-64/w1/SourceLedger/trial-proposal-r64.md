# Bounded disclosed-finding qualification trial — proposal (mines considerthese 2026-10-26 proposal 2)

Status: PROPOSAL ONLY. Not run, not scored, not a six-file claim package, not SHONEN box 2. Nothing here adds a knowledge entry, coverage frontier, or score credit.

## What proposal 2 asks and what this narrows it to

Proposal 2 (`considerthese/2026-10-26.md:30`) asks for an end-to-end domain task: one public disclosed report, a six-file claim package, pricing, and a rebuilt claim checker. The r63 handoff already took only the documentation-review half on S094 (four qualifications). That leaves the instrument question open: the existing trial can pass while its anchors are weak. This proposal keeps the single finding (S094, the Big Sleep SQLite account) and changes only how the qualification is measured.

## Why the existing trial is too weak to disclose as “qualified”

1. Count-only anchors: the r63 ledger's four figures are `git show … | grep -F <phrase> | wc -l` with want 1. A phrase repeated elsewhere would still pass, and the count does not say which line.
2. Python-side checks not run by the command-aware runner: `.ufo/waves/round-64/domain-qualification.py` checks phrases by hard-coded line numbers and reads the working tree, not committed bytes. Its ARITHMETIC rows compute `column - 1` with no located value for `SERIES_COLUMN_START` (name at capture L51, value absent). See M64-5.
3. No negative control: nothing shows the trial goes red when the source is wrong. The grep no-match zero preserved by S097 is only a zero count, not an anchor test.

## Proposed design (all figures through `corpus/instruments/figure-audit.py`, committed bytes, pinned revision)

Positive located-line figures (line number is the value, so a moved or duplicated phrase fails the whole-value compare):

| id | derive (literal argv, `git show <rev>:…`) | want |
|---|---|---|
| S094-release-line | `git show REV:corpus/source-snapshots/round-61/S094.txt \| grep -n -F 'before it appeared in an official release' \| cut -d: -f1` | 18 |
| S094-sentinel-line | `… \| grep -n -F 'a special sentinel value -1' \| cut -d: -f1` | 27 |
| S094-negative-index-line | `… \| grep -n -F 'iCol being calculated as -2' \| cut -d: -f1` | 110 |
| S094-cpu-hours-line | `… \| grep -n -F '150 CPU-hours of fuzzing' \| cut -d: -f1` | 113 |
| S094-comparison-limit-line | `… \| grep -n -F 'highly experimental results' \| cut -d: -f1` | 118 |
| S094-constant-name-line | `… \| grep -n -F 'SERIES_COLUMN_START' \| cut -d: -f1` | 51 (name only; value not claimed) |

Expected behaviour on base, measured-before-freeze: each derive prints its line; a multi-line match prints two numbers and fails the whole-value compare (fail-closed); a missing phrase makes grep exit 1 mid-pipeline (ignored), leaves cut with empty stdout, and gives derive-empty stale. Those three cases are the proposal's own finite checks, not yet run.

Negative-control ledger (separate file; the runner must exit 1 and print the pinned reason; pass means it fails as expected):

| id | derive | expected base reason | expected candidate reason (inference) |
|---|---|---|---|
| neg-absent-cat | `cat corpus/source-snapshots/round-61/S094-absent.txt \| grep -n -F 'before it appeared' \| cut -d: -f1` | derive-empty | derive-upstream-exit-1 |
| neg-absent-git | `git show REV:corpus/source-snapshots/round-61/S094-absent.txt \| grep -n -F 'before it appeared' \| cut -d: -f1` | derive-upstream-exit-128 | derive-upstream-exit-128 |

The neg-absent-cat row is the designed discriminator: the verdict stays stale in both worlds, but the reason changes only under the S097 rule. That is the measurable diagnostic gain; it is not a new claim about exploitability.

## Falsification and kill rules (pre-registered before any run)

- Trial fails if any positive row prints a value other than its pinned line, or if the negative ledger exits 0.
- Trial fails if neg-absent-cat reports derive-empty under the candidate. That would mean the r64 rule did not reach the cat stage.
- Trial fails if the S094 source sha256 in the receipt differs from the committed capture digest recorded at review time.
- Any use of ARITHMETIC rows, Python-derived indices, or the working-tree read is out of this trial.

## Non-claims (must appear in any disclosure)

No exploitability, no reproduction, no released-user impact beyond the publisher's own sentence, no bounty eligibility, no severity score, no target action, no submission. Attribution stays with the publisher's account. The trial measures whether the qualification anchors are precise and whether the runner fails closed; it does not validate the finding.

## Ordering

Run only after L1 freezes the S097 candidate and after the trial ledger is committed or pinned by digest. Do not run in the same invocation as the candidate probes.
