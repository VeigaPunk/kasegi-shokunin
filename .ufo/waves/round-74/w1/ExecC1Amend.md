# ExecC1Amend — C1 recheck-cwd counter amendment (scratch-only candidate)

Seat: ExecC1Amend (executor, leaf). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin, freeze 847b53792d2d29d161cad7d21a33c89df9e52e8d (base ccd6a54bf392922495c4860332665499582e3213).
Scope: `corpus/instruments/recheck-cwd-census.py` only, edited in a scratch clone. The lane tree was not written. Nothing was committed, pushed or staged. No tool was installed or upgraded. No pacman transaction was run.

## Deliverables (all under .ufo/waves/round-74/w1/)

- `ExecC1Amend.patch`: unified diff, `diff -u` of the base file against the amended file. `patch --dry-run` against the lane's base file exits 0.
- `ExecC1Amend-selftest.txt`: amended `--selftest` output, with TMPDIR set and unset.
- `ExecC1Amend-census.txt`: clone-tree census and constraint greps.
- `ExecC1Amend-parity.txt`: parity limb, stdout sha256 for both counters.
- `ExecC1Amend-kills.txt`: the four kill receipts, plus the informational mutant censuses and the leak check.
- `ExecC1Amend-run-all.sh`: the single battery script that built the mutants and produced every receipt.
- `ExecC1Amend-battery.log`: raw log of that script (see deviation D4 for one artifact in it).

## Amendment (what changed, and what did not)

Only `selftest()` and the module docstring changed. `first_recheck`, `run_foreign`, `census`, `main`, the CLI parser, the RECHECK-CWD line format, the RESULT line and the exit semantics are byte-identical to base. `TIMEOUT`, the fail-closed behaviour and `DEFAULT_LANE` are unchanged. The diff is 122 lines, 99 insertions and 23 deletions, all inside `selftest()` and the docstring.

Five cases, selftest prints `selftest cases=5 failures=N` and exits `1 if N else 0`:

1. **prefix-census**: the round-73 three-entry fixture, retained. Expected `entries=3 noprefix=2 exit2_foreign=1 exit0_foreign=2`.
2. **result-main**: `main()` runs in-process. Nonconformant fixture (one prefix-less `python3 corpus/instruments/missing.py`) must print `RECHECK-CWD-RESULT nonconformant` and return 1. Conformant positive control (one prefixed `cd <root> && true`) must print `RECHECK-CWD-RESULT conformant` and return 0.
3. **tmpdir-parent**: `tempfile.mkdtemp` is wrapped to record `dir=` kwargs during `census()` on the case-1 fixture. Every recorded `dir` must be `None` or start with the TMPDIR in effect. With TMPDIR unset, only `None` passes. (The first draft used `startswith("")`, which is vacuously true. Closed; see D3.)
4. **scratch-cleanup**: the same recorded calls. No recorded scratch path may still exist after `census()` returns.
5. **first-line**: one entry with two `recheck:` lines, first prefix-less and exit 2 from a foreign cwd, second prefixed and passing. Expected `noprefix=1 exit2_foreign=1`. A last-line reader gives `noprefix=0`.

Constraint receipts (ExecC1Amend-census.txt): `["bash", "-c"` occurs once in base and once in amended. `subprocess` occurs 4 times in both. No `"/tmp"` literal in code; the one `/tmp` occurrence is inside a docstring sentence ("no path is hard-coded under /tmp"). No new bash or subprocess call site.

## Commands and exit codes

Each row is one command in the scratch clone or lane. Full text is in `ExecC1Amend-run-all.sh`.

| # | Command (abbreviated) | Exit | Result |
|---|---|---|---|
| 1 | `git clone --shared <lane> $S/lane` | 0 | cloned |
| 2 | `git -C $S/lane rev-parse HEAD` | 0 | `847b53792d2d29d161cad7d21a33c89df9e52e8d` |
| 3 | `git -C $S/lane rev-parse --show-toplevel` | 0 | the clone path |
| 4 | `git -C $S/lane diff ccd6a54… 847b5379… -- counter` | 0 | empty: counter identical base vs freeze |
| 5 | `ls $S/lane/corpus/knowledge/*.md \| wc -l` | 0 | 89 |
| 6 | `git -C $S/lane show ccd6a54…:counter > orig.py` | 0 | sha256 `854456db322db2ee7263a0339a2b841515d36ae165c146eaa2708dfc59d3538e` |
| 7 | `git -C $S/lane archive ccd6a54… corpus/knowledge \| tar -x -C $S/base/repo` | 0 | 89 files |
| 8 | (i) `TMPDIR=$S/tmp python3 amended --selftest` | 0 | `selftest cases=5 failures=0` |
| 9 | (i-b) `env -u TMPDIR python3 amended --selftest` (cwd scratch) | 0 | `selftest cases=5 failures=0` |
| 10 | (ii) `TMPDIR=$S/tmp python3 amended --root $S/lane --lane <lane>` | 0 | `RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant` |
| 11 | `ls corpus/knowledge/*.md \| wc -l` on clone | 0 | 89, equals entries |
| 12 | (iii) orig.py on base export, `--lane <lane>` | 0 | stdout sha256 `e1906b886e856fa688f01f08b28a5034e5979adc311d3a040e7642776770f241` |
| 13 | (iii) amended on base export, `--lane <lane>` | 0 | same sha256 |
| 14 | `cmp` of the two stdout streams | 0 | byte-identical |
| 15 | `grep -n 'RECHECK-CWD' c1-base-census-r74.txt` | 0 | lines 3-4 equal the parity stdout |
| 16 | (iv) M4..M7 `--selftest`, TMPDIR set | 1 each | all killed (table below) |
| 17 | (iv-b) M4..M7 `--selftest`, TMPDIR unset | 1 each | all killed (table below) |
| 18 | (iv-c) M4..M7 census on base export (informational) | 0 each | see below |
| 19 | leak check, amended `--selftest` and census, clean TMPDIR | 0, 0 | leftover 0, 0 |
| 20 | `grep -c '\["bash", "-c"'` orig / amended | 0 | 1 / 1 |
| 21 | `grep -c subprocess` orig / amended | 0 | 4 / 4 |
| 22 | `patch --dry-run` of patch on base file | 0 | applies |

## Parity limb (criterion iii)

Stdout of the amended counter on the base export is byte-identical to the base counter's stdout (sha256 `e1906b88…f241` for both) and equals receipt lines 3-4 of `.ufo/waves/round-74/controls/c1-base-census-r74.txt`:

```
RECHECK-CWD entries=89 noprefix=0 exit2_foreign=0 exit0_foreign=67 exit1_foreign=22 exit_other=0 norecheck=0
RECHECK-CWD-RESULT conformant
```

Both exits 0.

## Kill battery (criterion iv, kill rule (a))

Mutants were built from the final amended file by `ExecC1Amend-run-all.sh`. Each is one change:

- **M4** forced conformant: `print("RECHECK-CWD-RESULT %s" % "conformant")`
- **M5** hard-coded parent: `mkdtemp(prefix="recheck-cwd-", dir="/tmp")`
- **M6** scratch leak: `run_foreign` finally → `pass`
- **M7** last-line reader: `first_recheck` keeps the last `recheck:` line

| Mutant | `--selftest` exit (TMPDIR set) | `--selftest` exit (TMPDIR unset) | Failing case line (TMPDIR set) | Verdict |
|---|---|---|---|---|
| M4 | 1 | 1 | `selftest case=result-main FAIL nonconformant ret=1 conformant ret=0` | KILLED |
| M5 | 1 | 1 | `selftest case=tmpdir-parent FAIL calls=3 dirs='/tmp','/tmp','/tmp'` | KILLED |
| M6 | 1 | 1 | `selftest case=scratch-cleanup FAIL calls=3 leftover=3` | KILLED |
| M7 | 1 | 1 | `selftest case=first-line FAIL got=entries=1,exit0_foreign=1,...,noprefix=0` | KILLED |

With TMPDIR unset, the failing lines are `case=result-main FAIL` (M4), `case=tmpdir-parent FAIL dirs='/tmp'` (M5), `case=scratch-cleanup FAIL leftover=3` (M6) and `case=first-line FAIL noprefix=0` (M7). Each case fails for the same reason in both modes.

Informational (criterion iv-c), each mutant's census on the base export against orig: the printed `RECHECK-CWD` line and `RESULT` line are identical to the amended counter for M4, M5 and M7. For M6 the line is identical but the run leaves 89 `recheck-cwd-*` scratch dirs in TMPDIR. This matches red-before evidence: on a conformant tree the census line cannot separate these mutants. Only the selftest kills them.

Leak check on the amended counter (criterion iv, M6 counterpart): leftover 0 after amended `--selftest` and after amended census, both with TMPDIR set to a clean directory.

## Kill-rule check (claims.json C1)

- (a) All four mutant classes exit nonzero under `--selftest`: PASS (table above).
- (b) Parity limb byte difference: 0 bytes, PASS.
- (c) Conformant positive fixture: case 2 conformant leg prints `RECHECK-CWD-RESULT conformant` and returns 0, PASS.
- (d) No new `bash -c` call site: literal count 1 to 1; `grep -c bash` 2 to 2; subprocess 4 to 4, PASS. RC-8 surface is not expanded.

Frozen after-values: selftest `cases=5 failures=0` exit 0 (PASS); clone census `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0`, conformant, exit 0, `entries=89 == ls | wc -l == 89` (PASS).

## Deviations and defects in my own work

- **D1. Clone cwd.** First clone attempt failed (`Working directory does not exist`) because the scratch dir was not created before the cwd was set. Re-run from the fleet root. The failed attempt mutated nothing.
- **D2. Selftest bug, caught and fixed.** First amended run exited 1 with `TypeError: string indices must be integers` in case 1 and case 5: I unpacked `capture()`'s `(text, ret)` in the wrong order. Fixed both sites, re-ran, and recorded only the passing runs.
- **D3. Vacuous tmpdir check, caught on review and fixed.** The first draft compared against `os.environ.get("TMPDIR") or ""`. With TMPDIR unset, `startswith("")` is always true, so M5 would survive. Changed to `None` or `startswith(expected)` with `expected = TMPDIR or None`. Verified: M5 with TMPDIR unset now fails with `dirs='/tmp'` (it passed under the draft).
- **D4. Parity receipt artifact.** The first parity run wrote its `parity-*-exit=` label into the captured stdout files, so `cmp` reported a spurious diff at line 3. The stdout streams were identical in lines 1-2. The clean run (stdout only, exit captured separately, sha256 compared) is canonical; the `battery.log` copy still carries the spurious diff line and is kept only as a raw log.
- **D5. Extra output lines.** The amended selftest prints one `selftest case=<name> ok|FAIL <detail>` line per case before the final `selftest cases=5 failures=N` line. The final line is the one the predicate names. The round-73 counter also printed a per-case line, so I kept that style. If the predicate is read as "the only stdout line", this is a deviation.
- **D6. Cosmetic label bug.** The informational census loop in my first battery script used single quotes around `info-$m-leftover`, so the label printed literally. Fixed in `run-all.sh` (`info-census-$m-leftover-recheck-dirs`). Not a data issue.
- **D7. Rejected edit.** I sent one malformed anchored edit (placeholder text) that the tool rejected with no effect. No file changed from it.
- **D8. Unset-TMPDIR selftest scratch.** With TMPDIR unset the selftest's scratch goes to the system temp dir. It writes a few small files, far under the 50 MB limit. I ran it with cwd in my scratch to keep it contained.

## Risks and what is not proven

- The kill claim is limited to the four enumerated mutant classes, as the claim's scope states. It asserts nothing about other mutants.
- The conformant positive control validates the RESULT line and exit code. It does not validate the census on a conformant tree beyond case 1's counts.
- Nothing in this report reaches live targets, uses credentials, or runs a port scan. No `bash -c` surface was added or rerouted.
- The clone census and parity limb ran `bash -c` rechecks for the 89 knowledge entries, as the existing counter does. That is RC-8, left open for the operator.

## Checks for the main agent to run after integration

- `python3 corpus/instruments/recheck-cwd-census.py --selftest` expects `selftest cases=5 failures=0` and exit 0.
- `python3 corpus/instruments/recheck-cwd-census.py --root . --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin` expects `RECHECK-CWD ... noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0` and `RECHECK-CWD-RESULT conformant`, exit 0.
- Apply `ExecC1Amend.patch` to `corpus/instruments/recheck-cwd-census.py` (dry-run verified against the base file, sha256 `854456db…538e`).

## Cleanup

Receipts and the patch are copied into the wave dir. The scratch tree `/fast/scratch/hyaku/kasegi-r74/ExecC1Amend` is removed before yield.
