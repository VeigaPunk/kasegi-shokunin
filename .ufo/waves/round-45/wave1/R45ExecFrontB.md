VERDICT: DRAFT-READY

# R45ExecFrontB — C1/R3 builder B: `r44-frontier-count.py` with `--selftest`

Draft: `.ufo/waves/round-45/wave1/R45ExecFrontB.draft/r44-frontier-count.py` (287 lines, sha256 `353c9d1d3c85eef16aee886b8dc0ebd91c4597a8d30c503ae6d1249c300a57d7`).
Full replacement for `corpus/instruments/r44-frontier-count.py`. The counting function `count_frontier` is byte-identical in logic to the base. I split the old `main` into `run_count` (the counting and printing, the same lines) and `cli`. `cli` injects the counter so the selftest can swap in a mutant. The L1 integrates it. I did not touch the real instrument or any git state.

## F1. Selftest (shape: fixtures in `--work`, 15 graded cases, 6 mutants)

Command: `python3 <draft> --selftest --work /fast/scratch/hyaku/kasegi-r45/R45ExecFrontB/w2`
Printed, tail (the tail of the first run is identical except for the case list above it):
```
case subprocess-cli-expect-27-on-26: ok rc=1 out='frontier rows=26 admitted=26\nfrontier expected=27 admitted=26 verdict=SHORT exit=1\n'
mutant status-compared-to-queued: rejected failing-cases=9
mutant status-read-from-second-cell: rejected failing-cases=9
mutant status-substring-match: rejected failing-cases=1
mutant every-row-admitted: rejected failing-cases=3
mutant any-pipe-line-is-a-row: rejected failing-cases=12
mutant ids-not-collected: rejected failing-cases=3
mutants=6 rejected=6
selftest cases=21 failures=0
exit=0
```
The first run (before I made the `--ids` case use a 26-row fixture) printed all 14 in-process cases as `ok`:
- `26-rows-26-admitted` printed `rc=0 out='frontier rows=26 admitted=26\n'`.
- `27th-admitted-row-counts-27` printed `rows=27 admitted=27`.
- `expect-27-on-27-exits-0` printed `rc=0`.
- `expect-27-on-26-is-SHORT` printed `rc=1` and `verdict=SHORT exit=1`.
- `duplicate-F-id-is-DEFECT` printed `rc=1 out='frontier duplicate-ids=F05 verdict=DEFECT exit=1\n'`.
- `queued-row-is-row-not-admitted` printed `rows=26 admitted=25`.
- `header-and-separator-not-counted` printed `rows=0 admitted=0`.
- `status-in-second-cell-not-admitted` printed `rows=26 admitted=25`.
- `missing-README-is-zero-rows-exit-0` printed `rc=0 out='frontier rows=0 admitted=0\n'`.
- Also run: `duplicate-id-beats-expect`, `not-admitted-is-not-admitted`, `last-row-without-newline-counts`, `--ids-prints-ids-first`, `missing-root-exits-2`.

The tally's `cases=21` is 14 in-process cases, 1 real subprocess CLI case, and the 6 mutants. Each case asserts the exit code and the exact stdout string. The two stderr cases also assert the message text (`cannot read`, `is not a directory`). The mutants are built by string-replacing a source anchor in `inspect.getsource(count_frontier)` and exec'ing it. A missing anchor aborts the selftest. A surviving mutant adds to `failures`. `--selftest` without `--work` uses a fresh temp dir and removes it. With `--work`, only its own subdirectory is removed: `ls -A w w2` printed both empty afterwards.

## F2. Real README of the pure export

`python3 <draft> --root /fast/scratch/hyaku/kasegi-r45/L1/pure` printed `frontier rows=26 admitted=26`, `exit=0`.
With `--expect 26 --ids`: `frontier-ids=F01,F02,...,F26` then `frontier rows=26 admitted=26`, `exit=0`.
With `--expect 27`: `frontier rows=26 admitted=26` then `frontier expected=27 admitted=26 verdict=SHORT exit=1`, `exit=1`.

## F3. Byte-compatibility versus the base script

I ran the base `corpus/instruments/r44-frontier-count.py` and the draft over 12 roots with 4 argv shapes each.
- The roots were the 9 fixture trees, the missing-root path, the missing-README tree and the pure export.
- The argv shapes were `[]`, `--ids`, `--expect 26`, `--expect 27 --ids`.
- I compared return code, stdout and stderr exactly.
- Two argv-error shapes (no `--root`, `--expect x`) were also compared, ignoring the program-name text.

Printed: `compared 46 diffs 0`.

## F4. Do-nothing control

Running the base script as `--selftest` printed `r44-frontier-count.py: error: the following arguments are required: --root`, `exit=2`. So the R3 limb in `r45-routed-defects.py` (`rc != 0 or tokens None`) is red at the base and can only go green with this draft or an equivalent.

## Limitations
- I did not touch SKILL.md or `corpus/instruments/README.md`. The other R3 limb conditions (the registry section with eight-cell rows, the README row) are not in this draft, and I did not run `r45-routed-defects.py`.
- The `ids-not-collected` mutant is only caught through the duplicate-id cases. The counting function does not assert the `ids` list directly except via the `--ids` case.
- The `status-substring-match` mutant is rejected by exactly one case (`not-admitted-is-not-admitted`). If that case is removed, the mutant survives.
- I did not use a labrat probe.
- Scratch `/fast/scratch/hyaku/kasegi-r45/R45ExecFrontB` was removed (`ls` afterwards: no such file). Git status shows only untracked `wave1/` content under round-45 and other round-45 items I did not create.
