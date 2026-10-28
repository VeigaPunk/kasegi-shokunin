VERDICT: DRAFT-READY

Seat R45ExecFrontA, round 45, C1/R3 (round-44 spot-check §6 item 3: `r44-frontier-count.py` had no selftest).

Draft: `.ufo/waves/round-45/wave1/R45ExecFrontA.draft/r44-frontier-count.py` (full replacement for `corpus/instruments/r44-frontier-count.py`). Nothing else written, no git/jj mutation, scratch `/fast/scratch/hyaku/kasegi-r45/R45ExecFrontA` removed on exit (trap).

## What was built
- The counter is split into pure functions: `count_lines(lines)`, `evaluate(rows, admitted, ids, expect, show_ids)`, plus the `count_frontier(root)` file wrapper. `main()` prints the lines `evaluate` returns.
- `count_lines` takes two keyword-only seams (`row_rx`, `is_admitted`); `evaluate` takes `check_dupes` and `is_short`. Production uses the defaults. The mutants pass altered versions.
- `--selftest [--work DIR]` needs no `--root`. It runs 18 fixture cases through a real subprocess CLI (exit code and exact stdout lines), 15 of those through the in-memory functions, and 10 mutants. Prints `mutants=<k> rejected=<k>` then `selftest cases=<N> failures=<F>` last. Exit 0 iff failures=0.
- The fixture cases cover: 26/26; 27/27; `--expect 27` on 27 (exit 0); `--expect 27` on 26 (SHORT, exit 1); `--expect 26` on 26; `--expect 26` on 27 (also SHORT: the existing `!=` behaviour is pinned); duplicated F05 (DEFECT, also beats `--expect`); a `queued` row (row, not admitted); header and separator not counted (0 rows, and 1 row beside them); status in the SECOND cell (3 rows, 0 admitted); "admitted" only in the note cell; `Admitted` capitalised (case-exact); `--ids` ordering; missing README (0/0, exit 0; and with `--expect 26` SHORT); root not a directory (exit 2). Non-F table rows and a prose `| F99 | admitted |` sit in every fixture and must stay uncounted.
- `--work` fixtures are kept. Without `--work` a `tempfile.mkdtemp()` dir is used and removed.
- Mutants (all must be rejected): status compared to `queued`; status read from cell 2; row regex counts any table row; `admitted` matched anywhere in the line; every row admitted; case-insensitive status; do-nothing counter returning 0/0; duplicate check removed; short check `<` only; short check `>` only.

## Exact outputs (re-runs I performed)
Selftest, final draft:
```
$ python3 r44-frontier-count.py --selftest --work $S/work | tail -4
case mutant/short-check-only-when-below: ok rejected_by=['expect-26-on-27-also-mismatch']
case mutant/short-check-only-when-above: ok rejected_by=['expect-27-on-26-short']
mutants=10 rejected=10
selftest cases=43 failures=0
exit=0
```
`grep -cE 'FAIL|SURVIVED'` on the full selftest output printed `0`. After a default-tmp run (no `--work`), `ls $TMPDIR | wc -l` printed `0`.

The selftest caught a hole in its own first version:
```
case mutant/short-check-only-when-below: FAIL SURVIVED
mutants=10 rejected=9
selftest cases=41 failures=1
```
The first case table never had admitted > expect, so a `<`-only SHORT check passed. The case `expect-26-on-27-also-mismatch` was added and the next run printed `mutants=10 rejected=10`, `failures=0`.

Real README of the pure export:
```
$ python3 r44-frontier-count.py --root /fast/scratch/hyaku/kasegi-r45/L1/pure
frontier rows=26 admitted=26
exit=0
$ ... --root pure --expect 27
frontier rows=26 admitted=26
frontier expected=27 admitted=26 verdict=SHORT exit=1
```
`--ids` on the pure export prints `frontier-ids=F01,...,F26` then the count line.

Do-nothing / old-script control: the existing `corpus/instruments/r44-frontier-count.py --selftest` exits `2` (`error: the following arguments are required: --root`), so the old file cannot pass the new gate. The do-nothing mutant (counter returning 0/0) is rejected by 26/26, 27/27 and `--expect 27` on 27.

Production sabotage (copies of the draft in scratch with the production code broken; the selftest must go red):
```
sab1 (_is_admitted -> == "queued")     exit=1 20 FAIL lines; selftest cases=43 failures=20
sab2 (_is_admitted -> cells[1] == ...) exit=1 24 FAIL lines; selftest cases=43 failures=24
sab3 (duplicate check disabled)        exit=1  4 FAIL lines; selftest cases=43 failures=4
```
(sab2 is the dead round-44 frozen-regex shape; the selftest rejects it.)

Byte-compat of the CLI, old script vs draft (stdout+stderr+exit code diffed) over roots {pure README, duplicated-id README, `/nonexistent`, plus earlier a queued README and a no-README dir} x args {none, `--ids`, `--expect N`, `--expect 1 --ids`}: every pair printed `same` (9/9 in the final run, 20/20 in the earlier run). The only difference is the no-args argparse usage text: it lists `[--root ROOT]`, `[--selftest]` and `[--work WORK]`. The error line `the following arguments are required: --root` and exit 2 are unchanged.

## Limitations
- Case count `cases=43` = 18 CLI + 15 in-memory + 10 mutants. The 3 file-only cases (missing README x2, non-directory root) are not run in-memory, so a mutant that breaks only the file layer (for example crash on a missing README) is caught by the CLI cases, not by the mutant set.
- The case-exact and note-cell cases pin the existing behaviour (`cells[2] == "admitted"`); a future deliberate change must edit both.
- The selftest reads no real README; the 26/26 on the pure export is a separate command, not part of `--selftest`.
- No registry row or `SKILL.md` Gates & probes entry is written (L1 integration, outside my draft directory). Spot-check §6 item 3 asks for a registry row at the instrument's home.
- Nothing was installed.
