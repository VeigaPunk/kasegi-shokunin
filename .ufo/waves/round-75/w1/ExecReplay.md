# ExecReplay — kasegi round 75 attempt 1, freeze-check replay

Seat: ExecReplay (leaf, replay only). No lane writes; no worktree created (`git worktree list --porcelain`, rc 0: only the main lane entry). Outputs and evidence are in `.ufo/waves/round-75/w1/ExecReplay-evidence.txt` and `ExecReplay-agree.txt`.

## Verdict

All 20 replayed values AGREE with the committed receipts. 0 DISAGREE. The frozen base values hold at the base commit `f9cc05b56170946192a2dcafcc07e90ec611746c`; the controls commit `c880047421a386a4a1731034a0a06df07ba23071` and freeze commit `748dfb666280adfb1e249fcf6a265c5d9951eefb` are both reachable and carry the base as ancestor (`git merge-base --is-ancestor`, rc 0 for both).

## Step 1 — committed bytes exported (never working tree)

| Export | Command | rc | sha256[:16] | bytes |
|---|---|---|---|---|
| base census | `git -C <lane> show f9cc05b5…:corpus/instruments/recheck-cwd-census.py` | 0 | 5ef12c7ff0993752 | 10349 |
| C1 do-nothing receipt | `git show c880047421…:.ufo/waves/round-75/controls/c1-donothing-r75.txt` | 0 | 57e84c616140cd0e | 1428 |
| C1 red-before receipt | `… c1-redbefore-restoration-r75.txt` | 0 | 2f70d1faba124cbb | 811 |
| C2 base receipt | `… c2-base-counters-r75.txt` | 0 | 2f824997d9506183 | 11626 |
| assimilation receipt | `… assimilation-considerthese-r75.txt` | 0 | 20ffc83d1d991848 | 2002 |
| frozen claims | `git show 748dfb6662…:.ufo/waves/round-75/claims.json` | 0 | fca2513e791c9243 | 10791 |

`cmp -s <frozen claims> <lane worktree claims.json>` → rc 0: the lane worktree copy is byte-identical to the frozen claims. Claims read in full; predicates were not reworded.

## Step 2 — C1 base replay

- `python3 recheck-cwd-census.py --selftest` (from foreign cwd, `TMPDIR=<scratch>`) → rc 0. Output: `selftest cases=5 failures=0`, `selftest` case lines all `ok`.
- Real lane tree, foreign cwd: `python3 <base counter> --root <lane> --lane <lane>` → rc 0. Output: `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`.
- Case-6 fixture rebuilt from claims C1 target text (`r.md` = `restoration-recheck: touch <fx>/restoration-ran`, `p.md` = `cd <fx> && true`): rc 0. Output: `NORECHECK r.md`, `RECHECK-CWD entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=0 exit_other=0 norecheck=1`, `RECHECK-CWD-RESULT conformant`. Marker `restoration-ran` absent (`ls` rc 2). The base counter survives the restoration-only file as a plain norecheck entry, as claimed.

Note on process: my first C1 replay cell failed on a Python syntax error and a later cell reused the `out` name, so the first C1 results were lost from kernel state. I re-ran the C1 replay into distinct variables (outputs saved as `replay-{st,lane,fx}.out` in scratch) and compared those. The reported values are from the re-run.

## Step 3 — C2 base replay (archived tree, no worktree)

`git -C <lane> archive f9cc05b5… | tar -x -C <scratch>/base-tree` → rc 0. Then in the archived tree:

- `python3 corpus/instruments/frontier-recheck-count.py` → rc 0. `FRONTIER-CENSUS rows=52 admitted=52 closed=52 problem-rows=0 registry=109`; 52 `FRONTIER-PASS` lines; `entries=55 pass=55 exit=0`.
- `python3 corpus/instruments/capture-binding-check.py` → rc 0. Final line `records=88 bound=88 unbound=0`.
- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → rc 0, `109`.
- `ls corpus/knowledge/*.md | wc -l` → rc 0, `90`.
- `wc -l corpus/instruments/knowledge-expected.txt` → `92`; `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` → rc 0.

## Step 4 — replayed vs committed receipts

`ExecReplay-agree.txt`, 20 lines, `TOTAL_LINES=20 AGREE=20 DISAGREE=0`:

- C1 lane census line: AGREE; C1 lane RESULT line: AGREE.
- C1 selftest case lines (prefix-census, result-main, tmpdir-parent, scratch-cleanup, first-line): AGREE each, with the tmpdir-parent path normalized to `<TMPDIR>` because the receipt ran under a different TMPDIR. `selftest cases=5 failures=0`: AGREE.
- C1 case-6 fixture NORECHECK + census + RESULT lines vs red-before receipt: AGREE.
- C2 FRONTIER-CENSUS line, all FRONTIER-PASS/PASS lines (byte-identical), summary `entries=55 pass=55 exit=0`, frontier exit 0: AGREE.
- C2 capture `records=88 bound=88 unbound=0`, exit 0: AGREE.
- C2 SOURCES S-row count 109, knowledge file count 90, knowledge-expected 92 lines, `LC_ALL=C sort -c` exit 0: AGREE.

## Frozen-claims implications

- C1 base: the do-nothing control passes the real tree (`conformant`, exit 0). The target state is not reachable without the amendment, as claimed.
- C2 base values (52/88/109/90/92) are the pre-landing counts. The claimed after-values are 53, 89, 110, 91, 93 and are not measured here.
- The claimed drift after C2 (entries 90→91, exit0_foreign 68→69) is consistent with the base but not measured by this seat.

## Scope and checks not performed

- No lane writes beyond `.ufo/waves/round-75/w1/ExecReplay*` files. No commit, checkout, reset, stash, or worktree.
- No network access (replay used local committed bytes only). No live-target testing.
- The `scripts/sources-census.sh validate` census (W04 warnings) is not part of my item; not run here.
- No labrat probe was spawned (leaf seat, no falsifiable hypothesis required).
- Tool installs: none.

Evidence: `.ufo/waves/round-75/w1/ExecReplay-evidence.txt` (raw replay output with commands and exit codes), `.ufo/waves/round-75/w1/ExecReplay-agree.txt` (AGREE/DISAGREE ledger).
