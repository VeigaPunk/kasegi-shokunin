# ExecPipeline — round64 candidate (predata, not frozen)

Axis: depth:verifiability. Nominal score4 held under R58; no coverage, frontier, knowledge, score, source-restoration or security claim. Candidate is not frozen; L1 owns freeze, falsification and integrated verification.

## Deliverable (current revision)

- Candidate: `.ufo/waves/round-64/w1/ExecPipeline/figure-audit.py` (503 lines)
- SHA-256: `c233577dbf0517df29e2c7d938946bc9b06f9c4a8cf4af2654bc058c68c7df01`
- Start bytes: r63 final candidate `.ufo/waves/round-63/w1/ExecPipeline/figure-audit.py`, SHA-256 `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`.
- Diff vs r63 final: `figure-audit-r63-to-r64.diff`, SHA-256 `a7bcbee9f6822aaea860426fe31eedc5a52ba463ec5e84b019c0cd6e5f670c02`.
- Receipts: `receipts/` (one raw invocation each, run UTC on the first line).
- Supersedes the earlier revision (sha `ca1015b2…`, 54 cases).

## Rule

`upstream_stale(head, status)` (lines 79-86): stale when `status > 1`; when `status == 1` and `os.path.basename(head) != "grep"`; negative (signal) statuses are not stale. `heads` records each stage's `argv[0]` (lines 94, 107); the upstream loop (lines 119-120) runs after the unchanged final-stage `derive-exit-N` check. The rule is command-aware (decided per stage by the program name); it does not scan argv tokens, so a file or script named `grep` cannot exempt a non-grep program.

## Selftest

- `EXPECTED_CASES` = 59 (was 43 in r63).
- Changed: `upstream-cat-missing-exit1-stale` (exit 1, reason `derive-upstream-exit-1`) replaces the old retained-zero case.
- Added (16 over r63): cat partial, cut/head/tail missing (exit1), ls/sort missing (exit2 native), sha256sum missing, python counter exit1, python SIGTERM child (negative, ignored, retained control), `grep -c` no-match (ignored), final exit7 over upstream exit1, `&&` first-group non-grep exit1, `&&` second-group non-grep exit1, middle-stage non-grep exit1, `cat grep.txt` missing (named file), `python3 corpus/instruments/grep.py` exit1 (named script, fixture added).
- The negative-signal retained control is `upstream-python-signal-ignored`.

## Observed finite evidence (construction controls, not scoring)

- `receipts/selftest-candidate-r64.txt`: `selftest cases=59 failures=0`, exit 0.
- `receipts/ledger-replay-candidate-r64.txt`: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`, exit 0.
- `receipts/control-r63-guard-r64-selftest.txt` (earlier revision, 54 cases): r63 `>1`-only guard turns 7 cases red; the 5 later cases were not re-run against it.

Native exit codes (measured in scratch, one invocation each): cat missing 1, cat partial 1, cut 1, head 1, tail 1, ls 2, sort 2, sha256sum 1, grep absent 1, grep -c absent 1.

## Residuals

- Only the basename of the literal allow-listed head is read; no executable-path or alias semantics beyond the allow-list were examined.
- Negative statuses beyond the single SIGTERM child are not exhaustively probed.
- `&&` widening is documented; it is not bash pipeline-status equivalence.
- Collector probes and R53 tree probes are not run here.
- Lane working-tree `corpus/instruments/figure-audit.py` hashed to the r63 candidate (not the committed base); L1 to reconcile against master `d74be00`.
- Scratch removed; no installs, git mutations, production or sibling edits, or subagents.

Report: .ufo/waves/round-64/w1/ExecPipeline.md

## Final correction (supersedes all earlier counts and hashes)

- Final candidate: `figure-audit.py`, SHA-256 `c233577dbf0517df29e2c7d938946bc9b06f9c4a8cf4af2654bc058c68c7df01`, 503 lines.
- Final `EXPECTED_CASES` = 59; selftest `cases=59 failures=0` (receipt `receipts/selftest-candidate-r64.txt`).
- The `54`-case count and `ca1015b2…` hash belong to the superseded intermediate revision and are not current.
- Changed anchors versus the superseded revision: `EXPECTED_CASES` line 72; grep.py fixture at lines 367-368; new cases at lines 453-462. Guard anchors (`upstream_stale` 79-86, `heads` 94/107, guard loop 119-120) are unchanged.

## Final correction 2 (supersedes the hash above)

- Final candidate SHA-256: `8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9` (503 lines). Diff SHA-256: `cfa580e93f4dbc71ae4b1953aab5251c0a6e4f60749e057a870d985a7392b69a`.
- Middle-stage case corrected to `cat g.txt | cat missing.txt | wc -l` (line 457; the failing command is now mid-pipeline, previously the first stage). Still expected reason `derive-upstream-exit-1`, want 0.
- Selftest `cases=59 failures=0` (receipt `receipts/selftest-candidate-r64.txt`, run UTC on line 1). Guard anchors unchanged (`upstream_stale` 79-86, `heads` 94/107, guard loop 119-120).
