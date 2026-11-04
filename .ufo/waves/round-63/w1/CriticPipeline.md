# CriticPipeline — round63 bounded falsification

Axis: **depth:verifiability** only; nominal score4 held under R58. No coverage/new-ground claim, admission decision, or production edits.

## Strongest counterexample: the named cat case is not exit>1

Real `cat missing.txt` exited **1**, not >1. The actual audit CLI accepted `cat missing.txt | wc -l`, want `0`, with `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`. Therefore a strictly positive-upstream->1 rule cannot reject all four named examples. This is a fixable claim/acceptance inconsistency, not evidence that the >1 improvement itself is unsafe. Do not silently special-case cat or generalize to all errors. Smallest correction: explicitly retain cat-exit1 as a disclosed residual and constrain the finite acceptance predicate to the three >1 cases; if all four must turn red, L1 must explicitly resolve the scope conflict before freeze. No candidate result is asserted.

## Real baseline CLI evidence

Instrument exported read-only from base `fdccc6da803965234c1eff5a0fee38b97e6621c1`; SHA-256 `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080`. Every ledger was executed through the real `figure-audit.py --root … --ledger …` front door on my scratch copy, not by calling internal functions. Scratch Git discovery used a `.git` pointer to the lane Git directory for read-only `git show`; no fixture commit or Git mutation occurred.

| Derive class | Direct upstream status | Audit exit observed | Intended bounded outcome |
|---|---:|---:|---|
| cat missing → wc | 1 | 0 | Four-example expectation says stale; >1 predicate excludes it |
| grep invalid regex → wc | 2 | 0 | stale1 |
| git nonexistent ref → wc | 128 | 0 | stale1 |
| Python fail.py → wc | 7 | 0 | stale1 |
| cat good → Python exit7 → wc | 7 (same script) | 0 | stale1; inspect every non-final stage, not only stage0 |
| Python exit7 → wc && cat tail | 7 (same script) | 0 | stale1; masked group currently admits later group output |
| cat missing → wc && cat tail | 1 | 0 | same exit1 residual |
| grep no-match → wc | 1 (grep semantics) | 0 | retain green0 |
| grep no-match → wc && cat tail | 1 (grep semantics) | 0 | retain green0 and concatenated stdout |
| cat good → final Python exit7 | — | 1, derive-exit-7 | retain stale1 |
| final grep no-match | — | 1, derive-exit-1 | retain stale1 |
| SIGPIPE producer → head -n 1 | negative status, separately observed -13 | 0, derived=x | retain as disclosed negative-status residual |

Distinct risks: **first-stage-only inspection** leaves midstage exit7 masked; **checking only the last && group** loses an earlier failed pipeline. These are falsification obligations for the proposal, not observed candidate defects. Smallest implementation correction is to inspect every waited non-final stage in each pipeline before advancing to the next && group, with the final-stage branch unchanged. Preserve grep-exit1 counting and avoid treating every nonzero status as pipefail. The separate explicit-status SIGPIPE probe returned producer=-13/consumer=0; changing negative statuses is outside assignment.

## Receipts and boundaries

All evidence is under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-63/w1/CriticPipeline/`: `probe.py` contains the complete finite commands, fixture contents and expected exits; `invocation.stdout`/`invocation.stderr` are unedited bytes from one driver invocation (exit0), and every audit/direct probe has separate unedited `.stdout`/`.stderr` files. `results.json` preserves raw argv, derive, want, cwd, expected and observed exits. `baseline-figure-audit.py` preserves the exact tested bytes. `sigpipe-status.py` and `sigpipe-direct.stdout`/`.stderr` preserve the separate explicit-status invocation (exit0).

No candidate existed at the checked `w1/ExecPipeline/**` path; no waiting, polling, speculative candidate execution, lane-wide checks, tool installs or updates. Both scratch invocations removed `/fast/scratch/hyaku/kasegi-r63/CriticPipeline` on exit. Read lane SKILL/PROVINCE, QUALITY R17/R50/R53/R58/R72/R82, and r62 spotcheck; retained its nominal/non-sandbox and outstanding R50 qualifications. This finite input falsification does not substitute for the author's prefreeze mutation battery or certify canonical judgment.

Self-evaluation: accuracy4 (real CLI/raw receipts; candidate absent), completeness4 (requested finite classes covered; no candidate verdict), clarity4 (scope conflict separated from proposal obligations), actionability4 (specific all-stage/&& controls), conciseness4 (raw evidence linked). Average4.0. Highest-impact improvement: settle the exit1 acceptance wording before freeze. User-agreement check: this is a bounded critic report, not approval or a universal safety claim.
