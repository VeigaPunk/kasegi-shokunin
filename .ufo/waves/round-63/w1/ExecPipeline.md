# ExecPipeline — round63 proposal

Axis: depth:verifiability; bounded nominal instrument improvement only, score4 held under R58. No coverage or new-knowledge claim. Proposal is not frozen.

## Deliverable and behavior

Candidate: `.ufo/waves/round-63/w1/ExecPipeline/figure-audit.py`.
Final proposal SHA-256: `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`.
Baseline SHA-256: `a0ddbd40a577d3d9e87dc89dbda0c5eb3237918246c89e0b20a29a47d395f080` (retained as `baseline.py`).

Reviewer F3 docstring-only correction: line38's exit-code summary now explicitly includes upstream positive status >1, matching the detailed rule. Tested hash `e557d2f0ceea9866b40b7b99dd53864a00330ae7481f32e7eeefca2fbf2431e8` → final proposal hash above. Original tested bytes are retained as `figure-audit-tested.py`; all original receipts and `manifest.json` remain untouched and refer to that tested hash. No rerun after this one-line prose correction; L1 owns final-byte verification. Scratch was recreated solely for this correction and deleted after saving.

Minimal execution edit: after communicating with the final stage and waiting every upstream stage, retain the existing nonzero-final `derive-exit-N` return first; then reject the first upstream returncode >1 as `derive-upstream-exit-N`. Upstream exit1 and negative statuses are deliberately unchanged. The module docstring states this exact bound and excludes pipefail/general error detection. No allow-list, flag, parsing, side-effect or sandbox change. No mutbat modification.

Selftest pin increases 35→43. Eight added cases cover the four named probes, grep no-match, a successful pipeline, final exit1, and final7 precedence over upstream2. Error cases bind both audit exit and printed reason. Each confined selftest creates `corpus/instruments/fail.py` containing `raise SystemExit(7)`; the retained external fixture has the same bytes.

## Observed finite evidence

All evidence below is in `.ufo/waves/round-63/w1/ExecPipeline/`. Each `*.txt` receipt is the unedited merged stdout+stderr of exactly one subprocess invocation, opened exclusively once. Commands, cwd, environment overrides, expected exits/reasons, actual exits, verdicts and receipt hashes are retained separately in `manifest.json`. `capture.py` is the reproducible finite capture driver; `fixture/` preserves all six ledger JSON inputs, g.txt and confined fail.py.

| Derive (want) | Baseline audit | Candidate audit | Candidate expectation |
|---|---:|---:|---|
| `cat missing.txt \| wc -l` (0) | 0 | 0 | retained upstream exit1 |
| `grep '[' g.txt \| wc -l` (0) | 0 | 1 | derive-upstream-exit-2 |
| `git show refs/figure-audit-nonexistent \| wc -l` (0) | 0 | 1 | derive-upstream-exit-128 |
| `python3 corpus/instruments/fail.py \| wc -l` (0) | 0 | 1 | derive-upstream-exit-7 |
| `grep absent g.txt \| wc -l` (0) | 0 | 0 | legitimate zero count |
| `cat g.txt \| wc -l` (1) | 0 | 0 | successful count |

Red-before receipts: `baseline-grep-invalid.txt`, `baseline-git-missing-ref.txt`, `baseline-python-exit7.txt` each print a green figure/exit0 despite the required stale expectation; the capture summary grades all three FAIL. Candidate counterparts grade PASS with the exact reasons above. Cat-missing is expressly a retained control, NOT a fourth repaired error: upstream exit1 remains ignored for every program.

`baseline-selftest.txt`: exit0 (35 existing cases). `candidate-selftest.txt`: `selftest cases=43 failures=0`, exit0. `candidate-real-ledger.txt`: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`. Only the candidate ran the real ledger. Its complete derive list was inspected beforehand: Git read operations and text/count/hash commands, no Python counter or write flags. Real-ledger root was the lane directory; all output was captured under this seat. Explicit GIT_DIR pointed at the lane's existing .git for the scratch git-show probe, so its missing-ref result is not merely a not-a-repository error. No Git mutations or fixture commit.

## Bounds, process, handoff

Read lane SKILL, PROVINCE, required QUALITY R17/R50/R53/R58/R72/R82 and the r62 spotcheck. Implemented only in own scratch; copied proposals/evidence under the exclusive output subtree. Scratch `/fast/scratch/hyaku/kasegi-r63/ExecPipeline` was deleted by the completed capture invocation after copying evidence. No production implementation edits, commits, indexes, host configuration changes, tool installs, delegation, live-target tests or mutbat runs. Python observed: 3.14.8, /usr/bin/python3. No LSP tool is mounted in this seat's inventory; semantic lookup was actually unavailable, so the local literal edit used read anchors.

Residuals: all upstream exit1 (including missing cat input), negative signal statuses, allowed flags/counter side effects, PATH/Git configuration and existing timeout/process behavior remain outside the improvement claim. Negative-signal behavior follows the unchanged `>1` bound; no negative-signal execution is claimed. No R17 committed-mutant or R50/R53 breadth certification is made by this seat. L1 owns independent counter/mutant falsification and final integrated verification before freeze; no claim freeze here. Real-ledger validation is host-bound, not a hermetic committed export.

Self-evaluation: accuracy4 (single-invocation receipts and hashes; no exhaustive/error-generalization claim); completeness4 (assigned candidate/probes/selftests/ledger delivered; integration remains L1-owned); clarity4 (cat residual separated from three repairs); actionability4 (candidate, exact commands and fixture inputs retained); conciseness4 (raw evidence linked, not duplicated). Average4.0. Highest-value next action is L1's independent finite counter/mutation evaluation. User-agreement check: this delivers the specified >1-only proposal, not all-error detection.

Report: .ufo/waves/round-63/w1/ExecPipeline.md
