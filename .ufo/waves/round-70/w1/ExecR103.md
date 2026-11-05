# ExecR103 — R70 w1: the 10 new selftest cases are isolated and load-bearing (R103 audit)

Seat: ExecR103 (executor, leaf; no subagents used). Item: for each of the 10 new cases at
`c1051749571caf6a0383b15187fc02cdd21785b5`, (a) the case's clean-run verdict line + the rule it
exercises, (b) the minimal mutant removing exactly that limb with the case turning red. Lane
untouched except this report file.

## Pins and method

- Gate exported with `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive c1051749571caf6a0383b15187fc02cdd21785b5 corpus/instruments/figure-audit.py | tar -x -C /fast/scratch/hyaku/kasegi-r70/ExecR103` → `gate.py`.
- `sha256 gate.py` = `7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5` — matches the frozen candidate pin in `.ufo/waves/round-70/controls/pins-r70.txt`.
- Host python3 3.14.8 (the binaries the gate executes). Selftest run as
  `HYAKU_SCRATCH=TMPDIR=/fast/scratch/hyaku/kasegi-r70/ExecR103 python3 -B gate.py --selftest`.
- Each mutant = one exact source replacement applied once to a copy; full 96-case selftest per mutant; measured failed-set diffed against the whole case list (kill sets below are exhaustive, not sampled).
- No tool installs (none needed; pacman guard respected). Scratch tree removed before yield; receipts are the pasted lines here.

## Baseline (clean selftest)

`selftest cases=96 failures=0`, exit 0, no pin-mismatch line.

```
selftest case=python-head-root-space-refused exit=2 want=2 verdict=pass
selftest case=python-head-root-equals-refused exit=2 want=2 verdict=pass
selftest case=python-head-root-abbrev-refused exit=2 want=2 verdict=pass
selftest case=python-head-out-space-refused exit=2 want=2 verdict=pass
selftest case=python-head-out-equals-refused exit=2 want=2 verdict=pass
selftest case=python-head-out-abbrev-refused exit=2 want=2 verdict=pass
selftest case=python-head-json-refused exit=2 want=2 verdict=pass
selftest case=python-head-dashdash-operand-admitted exit=0 want=0 verdict=pass
selftest case=git-show-no-operand-refused exit=2 want=2 verdict=pass
selftest case=git-show-separator-refused exit=2 want=2 verdict=pass
```

## Limb map (from gate source)

`python_flags_ok`: **L-eq** name==flag equality (after the `name = tok.split("=",1)[0]` split);
**L-pfx** `flag.startswith(name)` unique-argparse-abbreviation; **L-dd** `if tok == "--": return True`
operand scoping; **L-o** short `-o` limb. `git_show_operands_ok`: **G-dd** `"--" in parts[2:]`;
**G-no** `not operands`; **G-sh** per-operand colon/`:/`/brace shape check.

Red signature: for a refused case the mutant admits the derive; the fixture has no such counter/repo,
so the run fails (`derive-exit-2` / `derive-exit-128`) → audit exit 1 vs want 2 → red. For the
admission case the mutant refuses → exit 2 vs want 0 → red. Kill sets are by exhaustive failed-case
diff, not by reason string.

## Case table — verdict line, rule, killer

| # | case | clean verdict | rule exercised | killer mutant(s) (measured) | isolated? |
|---|------|---------------|----------------|------------------------------|-----------|
| 1 | python-head-root-space-refused | `exit=2 want=2 pass` | L-eq on `--root`, token `--root` | M1 {1,2,3} | shared name limb (2,3) |
| 2 | python-head-root-equals-refused | `exit=2 want=2 pass` | L-eq on `--root` via `=`-split, token `--root=.` | M1 {1,2,3}; M8 exclusive {2} | yes (M8) |
| 3 | python-head-root-abbrev-refused | `exit=2 want=2 pass` | L-pfx: `--ro` ⊂ `--root` | M1 {1,2,3}; M3 exclusive {3} | yes (M3) |
| 4 | python-head-out-space-refused | `exit=2 want=2 pass` | L-eq on `--out` (also pfx of `--output`); derive also carries `--url` (2nd limb) | M2′ {4,5,6}; M8′ {2,5} | group only — no single-limb killer |
| 5 | python-head-out-equals-refused | `exit=2 want=2 pass` | L-eq on `--out` via `=`-split + `--url` limb | M2′ {4,5,6}; M8′ {2,5} | group only |
| 6 | python-head-out-abbrev-refused | `exit=2 want=2 pass` | L-pfx: `--ou` ⊂ `--out`,`--output` + `--url` limb | M2′ {4,5,6}; M3′ {3,6} | NO single-limb killer (double-covered) |
| 7 | python-head-json-refused | `exit=2 want=2 pass` | L-eq on `--json` | M4 exclusive {7} | yes |
| 8 | python-head-dashdash-operand-admitted | `exit=0 want=0 pass` | L-dd: after `--`, tokens are operands (`ok.py -- --root` admitted) | M5 exclusive {8} | yes |
| 9 | git-show-no-operand-refused | `exit=2 want=2 pass` | G-no: bare `git show` (= HEAD patch, textconv-driver risk) refused | M6 exclusive {9} | yes |
| 10 | git-show-separator-refused | `exit=2 want=2 pass` | G-dd (`--`→pathspec) AND G-sh (`g.txt` has no `:`) jointly | M7d {10, git-show-commit-form-refused} | NO single-limb killer (see refutation) |

Red lines pasted per case (from the named killer's run):

```
M1:  selftest case=python-head-root-space-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M1:  selftest case=python-head-root-equals-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M1:  selftest case=python-head-root-abbrev-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M2': selftest case=python-head-out-space-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M2': selftest case=python-head-out-equals-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M2': selftest case=python-head-out-abbrev-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M4:  selftest case=python-head-json-refused exit=1 want=2 verdict=fail reasons=derive-exit-2
M5:  selftest case=python-head-dashdash-operand-admitted exit=2 want=0 verdict=fail
M6:  selftest case=git-show-no-operand-refused exit=1 want=2 verdict=fail reasons=derive-exit-128
M7d: selftest case=git-show-separator-refused exit=1 want=2 verdict=fail reasons=derive-exit-128
```

## Mutant table (every row is a measured full selftest run)

| mutant | exact edit | measured failed set | summary |
|--------|-----------|---------------------|---------|
| M1-root-name | `PY_DENIED_FLAGS` minus `--root` | {1,2,3} | `cases=96 failures=3` exit 1 |
| M2a-out-only | minus `--out` | {} | `failures=0` exit 0 (`--out` still prefix-matches `--output`; `--url` also refuses) |
| M2-out-group | minus `--out`,`--output` | {} | `failures=0` exit 0 (`--url` limb still refuses all three) |
| M2′-out+output+url | minus `--out`,`--output`,`--url` (one line) | {4,5,6} | `failures=3` exit 1 |
| Murl-only | minus `--url` | {} | `failures=0` exit 0 |
| M3-abbrev-prefix | `if name == flag or flag.startswith(name):` → `if name == flag:` | {3} | `failures=1` exit 1 |
| M3′-prefix+url | M3 edit + minus `--url` | {3,6} | `failures=2` exit 1 |
| M4-json-name | minus `--json` | {7} | `failures=1` exit 1 |
| M5-dashdash-operand | drop `if tok == "--": return True` in `python_flags_ok` | {8} | `failures=1` exit 1 |
| M6-git-no-operand | `if "--" in parts[2:] or not operands:` → `if "--" in parts[2:]:` | {9} | `failures=1` exit 1 |
| M7a-git-separator-only | `if "--" in parts[2:] or not operands:` → `if not operands:` | {} | `failures=0` exit 0 |
| M7c-colon-limb-only | drop `":" not in t or` from G-sh | {git-show-commit-form-refused} | `failures=1` exit 1 |
| M7d-dash+colon | M7a edit + M7c edit | {10, git-show-commit-form-refused} | `failures=2` exit 1 |
| M8-equals-split | `name = tok.split("=", 1)[0]` → `name = tok` | {2} | `failures=1` exit 1 |
| M8′-split+url | M8 edit + minus `--url` | {2,5} | `failures=2` exit 1 |
| M-o-limb-only | drop the two short `-o` lines in `python_flags_ok` | {} | `failures=0` exit 0 |
| M-scratch-work | minus `--scratch`,`--work` | {} | `failures=0` exit 0 |

## Findings

1. **All 10 cases are load-bearing**: each turns red under a named minimal mutant, with kill sets
   measured exhaustively (no collateral failures beyond the stated sets).
2. **R103 isolation requirement, case 9 — MET.** M6 (admits no-operand `git show`) kills exactly
   `git-show-no-operand-refused` (`failures=1`, `reasons=derive-exit-128`); the other 95 stay green.
3. **R103 isolation requirement, case 10 — REFUTED as stated.** Dropping the `--` limb alone (M7a)
   kills nothing: `cases=96 failures=0`, exit 0, because the same argv (`git show HEAD:g.txt -- g.txt`)
   is independently refused by the G-sh colon limb (`g.txt` is not `rev:path`). Case 10 dies only under
   the two-limb mutant M7d, which collaterally kills `git-show-commit-form-refused` (colon limb shared;
   M7c kills that one alone). So case 10 pins the conjunction G-dd+G-sh, not the `--` limb in
   isolation; the `--` limb is currently shadowed for the whole suite.
4. **Out group (4,5,6) is double-covered by `--url`.** All three derives carry
   `--url file:///dev/null`, itself a denied flag, so no single-limb removal reddens them:
   M2a, M2, Murl-only are all full-green. The minimal killer is the one-line removal of
   {`--out`,`--output`,`--url`} (M2′, kill set exactly {4,5,6}); M3′/{3,6} and M8′/{2,5} give the
   per-spelling attributions. Within the group, `--out` is additionally shadowed by the `--output`
   prefix (M2a green), so {4,5} cannot be separated from 6 by any name-set mutant.
5. **Exclusive single-limb killers exist for cases 2 (M8: the `=`-split parse), 3 (M3: abbreviation
   prefix), 7 (M4), 8 (M5), 9 (M6)** — those five are isolated at limb granularity. Cases 1,2,3 form
   the `--root` name group (M1 kills all three; the three spellings share the `--root` denial, space
   and equals via L-eq, abbrev via L-pfx).
6. **Coverage notes (measured, beyond the 10-case matrix):** `--url` name, short `-o` limb, and the
   `--scratch`/`--work` names are each individually unpinned by the current 96-case suite
   (Murl-only, M-o-limb, M-scratch-work all full-green). `--url` is pinned only jointly via M2′;
   `-o` and `--scratch`/`--work` have no dedicated case at all.

## Verdict

R103 verification PASSES for load-bearing (10/10 cases red under named mutants, kill sets exact) and
PASSES for isolation on 2,3,7,8,9 (exclusive killers) and 1 (group limb, no finer limb exists);
PARTIAL on 4,5 (group-only) and FAILS the stated single-limb isolation for 6 and 10 — both are
conjunction-pinned (6: L-pfx+`--url`; 10: G-dd+G-sh). The claim predicate itself (probe refusal by
name and abbreviation) is unaffected: the gate's refusal behavior is redundant, which is why no
single limb can be isolated for those two cases.
