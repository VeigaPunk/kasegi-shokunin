# ExecC1RealTree — round 84 wave 1, C1 successor exercised outside its selftest

Seat: leaf executor, item "exercise the frozen candidate outside its selftest".
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only; nothing in the lane tree edited).
Freeze commit `7f76b7eb690cd6e75e7f3e7729cedcb15611b34b` (base `a089ff3d…`), observed as `git rev-parse HEAD`.

Inputs verified byte-identical to the frozen spec:

| file | sha256 | selftest cases |
|---|---|---|
| `.ufo/waves/round-84/c1/recheck-cwd-census.py` (candidate) | `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e` | 33 |
| `corpus/instruments/recheck-cwd-census.py` (landed r83) | `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` | 27 |

All commands ran with `TMPDIR=/fast/scratch/hyaku/kasegi-r84/ExecC1RealTree` (`$S`), cwd = lane root unless stated.
Receipts: `.ufo/waves/round-84/w1/ExecC1RealTree-receipts/` (18 files, sha256 listed at the end).

## E1 — P6 analogue: candidate on the live lane tree

```
$ TMPDIR=$S python3 -B .ufo/waves/round-84/c1/recheck-cwd-census.py \
    --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
    --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
RECHECK-CWD entries=98 noprefix=0 exit2_foreign=0 exit0_foreign=76 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```
- 98 entries; `ls corpus/knowledge/*.md | wc -l` = 98 (worktree count includes the untracked F60 draft `corpus/knowledge/osv-gcs-data-dump-layout.md`, confirmed `?? corpus/knowledge/osv-gcs-data-dump-layout.md`).
- 76 exit0 / 22 exit1 (fail-closed lost-base class) / 0 noprefix / 0 exit2 / 0 exit_other / 0 norecheck / 0 restoration_only; buckets sum to 98.
- stderr empty; default mode printed zero `ENTRY` lines (correct: every entry is prefixed and none exits 2).
- Verbose run on the same tree: 100 lines = 98 `ENTRY` + `RECHECK-CWD` + `RECHECK-CWD-RESULT`, rc=0 (`candidate-real-tree-verbose.out`).

## E2 — candidate vs landed r83 on the same tree

```
$ TMPDIR=$S python3 -B corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>
<identical two lines>, rc=0
$ diff candidate-real-tree.out landed-real-tree.out && diff candidate-real-tree.err landed-real-tree.err
(no output — both diffs empty)
```
Byte-identical stdout and stderr: `sha256(candidate-real-tree.out) == sha256(landed-real-tree.out) == 0aa32988b6ae81300912e8104f53dd684b5a68c2bc44e65555fe11cc6a17e769`. The two implementations agree on the real tree's counts and RESULT; the r84 six checks add selftest coverage, not a changed real-tree verdict.

## E3 — each r84 new check exercised by direct CLI (not via `--selftest`)

Fixtures under `$S/fx/`; each leaf is `# fixture\nrecheck: <value>`.

| r84 check (docstring claim) | command | observed | verdict |
|---|---|---|---|
| noprefix-only (G-1): one or two prefix-less passing entries ⇒ nonconformant | `--root $S/fx/bare1 --lane $S/fx/bare1` (value `true`) | `ENTRY c-bare.md noprefix=1 foreign_exit=0`; `entries=1 noprefix=1 exit0_foreign=1`; `RESULT nonconformant`; rc=1 | holds |
| noprefix-only, boundary `!=1` | `--root $S/fx/bare2 --lane $S/fx/bare2` (two `true` entries) | `noprefix=2 exit0_foreign=2`; `nonconformant`; rc=1 | holds |
| summary-fields (G-2): exact printed RECHECK-CWD line, exit1=2 / exit_other=1 | `--root $S/fx/sum --lane $S/fx/sum` (pass + 2×`exit 1` + `exit 7`) | exactly `RECHECK-CWD entries=4 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=2 exit_other=1 norecheck=0 restoration_only=0`; rc=0; no ENTRY line | holds |
| entry-bare-pass (G-3): default mode prints ENTRY of a prefix-less passing entry | `--root $S/fx/bare1 --lane $S/fx/bare1` (default, no `--verbose`) | `ENTRY c-bare.md noprefix=1 foreign_exit=0` printed | holds |
| argv-values (G-4/G-6/G-7): trailing `--root` ⇒ rc 2 usage, no traceback | `python3 -B $C --root` | stdout empty; stderr `usage: recheck-cwd-census.py [--root DIR] [--lane DIR] [--verbose] \| --selftest`; rc=2; `grep -c Traceback` = 0 | holds |
| argv-values: trailing `--lane` | `python3 -B $C --lane` | same usage line, stdout empty, rc=2, 0 tracebacks | holds |
| argv-values: relative `--root` reported absolute | `cd $S/fx/relcwd; --root nosuch-rel --lane nosuch-rel` | stderr `recheck-cwd: no corpus/knowledge under /fast/scratch/…/fx/relcwd/nosuch-rel` (absolute), no traceback, rc=1 | holds (path claim) |
| argv-values: `--selftest` honoured in any position | `--selftest --verbose`, `--verbose --selftest` | both `selftest cases=33 failures=0`, rc=0 | holds |
| verbose-order (G-5): `--verbose` before `--root` is the verbose flag | `--verbose --root $S/fx/pref --lane $S/fx/pref` (one prefixed `true`) | `ENTRY a-prefixed.md noprefix=0 foreign_exit=0`; rc=0; default run on the same tree prints no ENTRY line | holds |
| entry-set (G-8): default mode silent for prefixed exit-0 and exit-7 entries | default run on `$S/fx/sum` (contains prefixed exit0 + exit7) | zero `ENTRY` lines; rc=0 | holds |
| entry-set: timed-out value renders `foreign_exit=-1` in exit_other | in-process `m.TIMEOUT = 1` over a prefixed `exec sleep 30` entry + a prefixed `true` entry | verbose: `ENTRY h.md noprefix=0 foreign_exit=-1`, `exit_other=1`, `RESULT conformant`, rc=0; default: no ENTRY, `exit_other=1` | holds |

No docstring claim in the six new checks was contradicted by observable CLI behaviour. All 33 selftest checks pass (`--selftest --verbose` → 34 lines, last line `selftest cases=33 failures=0`, rc=0, stderr empty).

## E4 — selftest hygiene (leaves nothing behind, restores state)

1. Clean scratch delta with `TMPDIR=$S`: file listing of `$S` before vs after one `--selftest` run (receipt files excluded from both snapshots):
```
selftest rc=0
SCRATCH-DELTA=NONE (identical before/after)   count before=74 after=74
```
   (An earlier raw count 70→74 was concurrent sibling writes from a parallel call in this same shell — two redirect receipts plus one verbose receipt — not selftest residue; the isolated re-run shows zero delta. Dedicated `TMPDIR` dirs `selfTmp1`/`selfTmp3` also held 0 entries after the selftest.)
   `/tmp` net change: 0 new `recheck-cwd*` (9 pre-existing empty dirs at 05:59 predate this seat; every run here passed `TMPDIR=$S`).
2. `--selftest` with `TMPDIR` unset: rc=0, `selftest cases=33 failures=0` (docstring's "unset TMPDIR is not refused" holds).
3. Two selftests in one process (`importlib.util.spec_from_file_location` + `m.selftest()` twice), receipt `selftest-twice.txt`:
```
run1_rc=0 run2_rc=0 raw_identical=False normalized_identical=True
cwd_restored=True timeout_restored=True run_foreign_restored=True
lines_run1=34 lines_run2=34 ; case_order_identical=True
last_run1='selftest cases=33 failures=0' last_run2='selftest cases=33 failures=0'
```
   `raw_identical=False` is only the random `tempfile.mkdtemp` suffix inside three detail strings (`tmpdir-refusal`, `tmpdir-file`, `usage-guards`, `argv-values`); after normalizing `recheck-cwd-selftest-<suffix>` → `SCRATCH` the 34 lines are identical. cwd (`case 29`'s `os.chdir`) and the globals the selftest patches (`TIMEOUT`, `run_foreign`, `selftest`, `has_restoration_recheck`) are all restored.

## Routed defects

**D1 (LOW; documentation vs behaviour; PRE-EXISTING — identical on landed r83; not covered by any of the 33 checks).**
The docstring states `Exit 1: a non-conforming tree. Exit 2: harness or read error.` Two harness/read-error paths exit 1 instead, and one of them emits an uncaught traceback:

```
S=/fast/scratch/hyaku/kasegi-r84/ExecC1RealTree
mkdir -p $S/fx/sym/corpus/knowledge
ln -sfn $S/fx/sym/corpus/knowledge/missing-target.md $S/fx/sym/corpus/knowledge/dangling.md
printf '# fixture\nrecheck: cd %s && true\n' "$S/fx/sym" > $S/fx/sym/corpus/knowledge/p.md
TMPDIR=$S python3 -B .ufo/waves/round-84/c1/recheck-cwd-census.py --root $S/fx/sym --lane $S/fx/sym; echo rc=$?
```
observed (candidate, `dangling.out`/`dangling.err`): empty stdout, rc=1, stderr
`FileNotFoundError: [Errno 2] No such file or directory: '…/corpus/knowledge/dangling.md'` under a `Traceback (most recent call last)` from `main` → `census` → `first_recheck`.
Same command against `corpus/instruments/recheck-cwd-census.py` (landed r83) gives the identical traceback and rc=1 (`landed-dangling.err`) — not a r84 regression.

Second path at the same docstring line:
```
mkdir -p $S/fx/relcwd && cd $S/fx/relcwd
TMPDIR=$S python3 -B <candidate> --root nosuch-rel --lane nosuch-rel; echo rc=$?
```
observed: rc=1 (not 2), stderr `recheck-cwd: no corpus/knowledge under /fast/…/relcwd/nosuch-rel`; landed r83 identical. Here exit 1 collides with the documented "non-conforming tree" code, so a caller cannot distinguish "bad `--root`" from "tree nonconformant" by exit status.
Suggested fix (for the L1, not applied here): either map read failures to exit 2 (catch `OSError` around `first_recheck`/`open`, and use `sys.exit(2)` for the missing-`corpus/knowledge` case after printing the same named message), or amend the docstring to say a malformed `--root` also exits 1. A new selftest case would be needed either way; the current 33 do not exercise any unreadable-`*.md` or missing-root path beyond the named-message string.
Impact on the frozen claims: none observed — P1 (selftest), P2 (sha256), P6 (lane-tree census, rc 0) are unaffected; P3/P4/P5 were not run by this seat.

## Observations (not routed)

- **O1** `--selftest` short-circuits argument validation: `--selftest --bogus` runs the selftest (rc 0, `cases=33 failures=0`) and never prints the usage line, while `--bogus` alone gives usage rc=2. Consistent with the docstring's "--selftest is honoured in any position", but it means no argv validation happens in selftest mode (`selftest-bogus.out`).
- **O2** `TMPDIR` set-but-empty is refused: `TMPDIR= … --root …` → rc=2, stderr `recheck-cwd: TMPDIR  is not a directory` (double space from the empty value). Matches the docstring's "a TMPDIR that is not an existing directory exits 2"; noted because some harnesses export an empty `TMPDIR` instead of unsetting it.
- **O3** Host `/tmp` currently holds 9 empty `recheck-cwd-*` directories dated 05:59:06 — not created by this seat (every run here used `TMPDIR=$S`, and the `TMPDIR`-unset run left a net delta of 0). Recorded for host accounting only.

## Scope notes

- Ran only the candidate/landed census and selftest over the frozen bytes and scratch fixtures; no mutbat, no counter, no entry-gate (P3/P4/P5/P7/P8 belong to other seats).
- No tool installs or upgrades; no pacman, no sudo, no host mutation. No git/jj writes; `git status`/`git rev-parse` read-only.
- Scratch `/fast/scratch/hyaku/kasegi-r84/ExecC1RealTree` deleted after the receipts were copied.

## Files written

- `.ufo/waves/round-84/w1/ExecC1RealTree.md` (this report)
- `.ufo/waves/round-84/w1/ExecC1RealTree-receipts/` — 19 files:
  `candidate-real-tree.out`, `landed-real-tree.out` (identical sha256 `0aa32988…`), `candidate-real-tree-verbose.out`,
  `bare-one.out`, `bare-two.out`, `summary.out`, `verbose-order.out`, `default-prefixed.out`,
  `trailing-root.out`, `trailing-lane.out`, `relative-root.out`, `selftest-S.out`, `selftest-verbose.out`,
  `selftest-twice.txt`, `selftest-bogus.out`, `dangling.out`, `dangling.err`, `landed-dangling.err`, `tmpdir-empty.err`
