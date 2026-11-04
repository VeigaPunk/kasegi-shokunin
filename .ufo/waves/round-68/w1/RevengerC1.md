# RevengerC1 — program-execution and write surface of the derive gate at 82b3b7d4

**Verdict: FINDINGS.** The C1 repair closes exactly two spellings: `sort --compress-program` written as `=`, as a separate token, quoted, or after another option, and `git show --textconv` written as that exact token. The program-execution classes they belong to stay open. Three are open for execution: `sort` long-option prefixes (`--compress-prog=`, `--compress-p=`), `git show <commit>` textconv via attributes with no flag, and `git cat-file --textconv/--filters`. A fourth is open through an admitted counter: `frontier-recheck-count.py --root` runs `bash -c` on a recheck line from the root it is given. The frozen C1 predicate does not test any of these, so its pass does not show the class is closed. Nothing in the lane was edited, committed or staged. Scratch is removed; raw receipts are in `round-68/w1/RevengerC1/`.

## Method

- Gate under test: `corpus/instruments/figure-audit.py` at `82b3b7d4`, exported to scratch. sha256 `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8`, matching the pin. Base `d0f48405` exported for contrast, sha256 `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`, matching the pin (`round-68/w1/RevengerC1/gate-sha256.txt`).
- Every probe: a fresh fixture under `/fast/scratch/hyaku/kasegi-r68/RevengerC1/fx.*` (`git -C D rev-parse --show-toplevel` asserted equal to D before any commit), a ledger with one derive, run as `strace -f -qq -e trace=execve,openat python3 -B gate.py --ledger L --root D`. The derive reaches only the program names I placed in the fixture. Each fixture has a `mark.sh` that appends `ran` to `D/MARK`, and that marker is the execution evidence. "Admitted" means the gate's parse did not return `derive-not-read-only` (exit 2 with that reason = refused). Ledger verdicts `stale` are figure verdicts about the derived output, not refusals.
- Host binaries (help captured to `round-68/w1/RevengerC1/help/`): `sort` is **uutils sort 0.8.0** (clap parser, not GNU), `grep` is `pi-uu-grep 0.2.0`, `git 2.56.0`, `python3 3.14.8`, and the uutils `cat/cut/head/tail/ls/wc/tr/sha256sum` are 0.8.0. strace from `/usr/bin/strace` (already installed; nothing installed or upgraded).
- Harness and probe matrix: `round-68/w1/RevengerC1/harness/{probe.py,probes.py,probes2.py}`; raw per-probe JSON in `harness/`-run outputs `jsonl/`, per-probe strace in `traces/`.

## Commands run (representative; full set in harness)

```
git show 82b3b7d4:corpus/instruments/figure-audit.py > $S/gate.py      # sha 10c8…fee8 = pin
git show d0f48405:corpus/instruments/figure-audit.py > $S/base-gate.py  # sha 8147…d247 = pin
python3 -B probe.py sort sort ; … git git ; … env env ; … ro ro ; … py py   # matrix
python3 -B probe.py x x            # big-input compressor + ext-diff + nested (pinned)
PROBE_GATE=$S/base-gate.py PROBE_TAG=BASE- python3 -B probe.py xbase x   # same, base
python3 -B probe.py y y            # git diff.external / textconv isolation
python3 -B probe.py z z            # frontier-recheck bash exec
python3 -B probe.py w w ; PROBE_GATE=…/base-gate.py PROBE_TAG=BASE- python3 -B probe.py basew w
git -C $D show --textc HEAD:t.txt    -> fatal: unrecognized argument: --textc  (rc=128)
git -C $D show --ext-d HEAD          -> fatal: unrecognized argument: --ext-d  (rc=128)
git -C $D show --outp=…/o.txt HEAD   -> fatal: unrecognized argument: --outp=…  (rc=128)
```

## Observed results (marker = count of `ran` lines in the fixture's MARK file)

Ranked by severity. "Pinned" = gate `82b3b7d4`; "base" = `d0f48405`.

| # | shape (derive) | head | pinned gate verdict | base verdict | marker / strace evidence | class | status |
|---|---|---|---|---|---|---|---|
| 1 | `sort --compress-prog=PROG -S 256K big.txt` (also `--compress-p=PROG`) | sort | **ADMITTED** | ADMITTED | **marks 342** (X02, X03) | exec | **OPEN** |
| 2 | `python3 corpus/instruments/frontier-recheck-count.py --root D` (D holds a knowledge entry whose `recheck:` line is `printf ran >> MARK; python3 -I corpus/instruments/source-recheck.py …`) | python3 | **ADMITTED** | not run | **marks 1** (Z1); the payload ran through `bash -c` | exec | **OPEN** |
| 3 | `git show HEAD` on a commit whose `.gitattributes` maps `t.txt diff=x` to `diff.x.textconv=PROG` (no flag) | git show | **ADMITTED** | not run | **marks 1** (Y3); `--no-textconv` gives 0 (Y4) | exec | **OPEN** |
| 4 | `git cat-file --textconv HEAD:t.txt` | git cat-file | **ADMITTED** | not run | **marks 2** (G10) | exec | **OPEN** |
| 5 | `git cat-file --filters HEAD:t.txt` (attribute `filter=x`, `filter.x.smudge=PROG`) | git cat-file | **ADMITTED** | not run | **marks 1** (G20) | exec | **OPEN** |
| 6 | `sort -ro out.txt g.txt`, `sort -uo out.txt …`, `sort --outp=out.txt …`, `sort --out out.txt …` | sort | **ADMITTED** | ADMITTED | `out.txt` created (W02, W03, W06, W07) | write (arbitrary path) | **OPEN, pre-existing** |
| 7 | `python3 corpus/instruments/capture-source.py --id x --url file://D/src.txt --out /abs/outside.txt --kind text` | python3 | **ADMITTED** | not run | `outside/cap-outside.txt` (58 B) written outside the root (P09); the URL is read from any scheme urllib takes | write + read; network via `urlopen` at `capture-source.py:74-75` not run | **OPEN** |
| 8 | in-tree module shadowing: `corpus/instruments/json.py` imported by any admitted counter (`sys.path[0]` is the script dir) | python3 | **ADMITTED** | not run (same grammar) | **marks 1** (P08); the nested gate also imported the shadow (P10 contamination) | exec | **OPEN, latent** (no stdlib-named file in `corpus/instruments` today: `sys.stdlib_module_names` intersection = none) |
| 9 | `sort -T td -S 1K big.txt`, `sort --temporary-directory=td …`, or `TMPDIR=D/td sort -S 1K big.txt` | sort | **ADMITTED** | not run | 45,715 / 45,715 / 45,716 open calls with write flags on `td/sort*` (W08, W09, W10) | write (temp, self-deleting) | **OPEN, bounded** |
| 10 | any admitted python counter importing a sibling (`import probe_helper`) | python3 | **ADMITTED** | not run | `corpus/instruments/__pycache__/probe_helper.cpython-314.pyc` created (P07) | write | **OPEN, low** |
| 11 | `cat /etc/hostname`, `head -n 1 /etc/hostname`, `sort /etc/hostname`, `grep -f /etc/hostname g.txt`, `ls /`, `sha256sum /etc/hostname`, `wc --files0-from=/etc/hostname` | read-only heads | **ADMITTED** | not run | host file contents appear in the derive output (R01–R06 printed output; R07 admitted, exit 1) | read-only (outside lane) | **OPEN** (disclosure, not exec) |
| 12 | `PYTHONPATH=D/envpy` with a `sitecustomize.py` writing MARK, then any admitted python counter | env | not derive-reachable (`PYTHONPATH=… python3 …` refused, P06) | — | **marks 2** (P12; the derive ran and printed 35; the split between gate startup and derive is [INFERENCE] from env inheritance, not measured separately) | exec (env) | environment trust, **OPEN** |
| 13 | `GIT_EXTERNAL_DIFF`, `GIT_CONFIG_COUNT`, `PATH` (head resolution) | env | not derive-reachable | not isolated | E02 (blob show) = 0; E03 not isolated (its marks came from the textconv attribute, not the env var) | exec (env) | **not isolated**; inference only |
| 14 | `tail -f g.txt` (no exit) | read-only head | ADMITTED (inferred from gate code, communicate deadline 300 s) | — | **not run** (would hang the seat); availability only | read-only | inference |

### Closed by the repair (refused at parse time, rc=2, marks 0)

- `sort --compress-program=PROG` (equals, S01), `--compress-program PROG` (S02), `'--compress-program=PROG'` quoted (S03), after `-S 1K` (S06), inside `-S1K -r --compress-program=` (S07), attached to a word (S08). Big-input versions X01 (`=`) and X04 (space): **refused, marks 0**; base: **ADMITTED, marks 342** (BASE-X01, BASE-X04). This is the repair working for the named spellings.
- `git show --textconv HEAD:t.txt` (G01, exact token): refused, marks 0. The base receipt in C1 shows it admitted and executed once; I did not re-run base for this probe.
- `git show --ext-diff HEAD` (G05, exact token): refused. Consistent with Y1: `diff.external` alone with no flag does not execute (marks 0).
- `sort -o out.txt`, `sort -oout.txt`, `sort --output=out.txt`: refused (W01, W04, W05). At base I re-ran only W04 and W05 (refused, same); W01 base not re-run.
- `git show --output=o.txt` (G07): refused.
- `python3 -c`, `python3 -I …`, `python3 -m …`, `python3 corpus/instruments/../../x.py`, `PYTHONPATH=… python3 …`: refused (P02–P06).
- `git -c KEY=V show …`, `git -C D show …`, `git show -- --textconv`: refused (G16–G18).
- Git long-option abbreviations `--textc`, `--ext-d`, `--outp`: admitted by the grammar but **git rejects them** (`fatal: unrecognized argument`, rc=128, no output file, no marker). No exec, no write.

## Findings and disagreements for the L1 to adjudicate

1. **The sort compressor class is not closed.** The frozen C1 predicate checks `--compress-program` in three spellings. `--compress-prog=PROG` and `--compress-p=PROG` are admitted and run the compressor **342 times** on the pinned gate (X02, X03), the same as base. This is uutils clap-style long-option prefix matching, and `denied_flag` does an exact `tok == flag or tok.startswith(flag+"=")` check. GNU getopt_long also accepts unique prefixes; I did not run GNU sort (`[INFERENCE]`).
2. **The `git show --textconv` denial closes a flag, not the textconv class.** Y3 shows `git show HEAD` runs the attribute-mapped textconv driver with no flag; only `--no-textconv` disables it (Y4 = 0). The C1 rationale ("refuse the program-execution flag") therefore does not cover the commit-diff path.
3. **The same class is unrefused on `git cat-file`.** `--textconv` (G10, marks 2) and `--filters` (G20, marks 1, smudge via attribute) are not in `DENIED_FLAGS`. The gate's own docstring names git configuration as a residual; this is the measured form.
4. **An admitted counter runs `bash -c` on data read from `--root`** (`frontier-recheck-count.py:269`). Z1 confirms it. This is an exec class through the python head, not a flag.
5. **The sort output-flag holes predate C1.** `-ro`, `-uo`, `--outp=`, `--out` write arbitrary paths at base and at `82b3b7d4` (W02, W03, W06, W07 at both). They are outside C1's named scope but belong to the write class the gate claims to refuse.
6. **The python head admits counters that write to absolute paths and read any URL scheme.** `capture-source.py --out` wrote outside the root and `--url file://` was read (P09). Network egress via `urlopen` is not run.
7. **Script-directory shadowing is real and cheap to block.** P08 and the P10 contamination show that an in-tree `json.py` runs in any admitted counter. A standalone test (`python3` / `python3 -P` / `python3 -I` on a shadow `json.py`) gives marks 1 / 0 / 0, so `-P` (or `-I`, which implies `-P`) blocks it. Shadow surface in the lane today: none.
8. **Over-refusals (not safety issues).** `git ls-tree --format=%(objectname)` is refused by the tokenizer for `(` (G15). `git show -- --textconv` is refused by the denied-flag scan across the whole argv (G18).
9. **Unexplained, not counted.** `git cat-file --batch --textconv < list.txt` (G13) gave `derive-exit-128` in the harness and I did not isolate why. Manual `git cat-file --batch --textconv </dev/null` returns rc 0. Not evidence either way.

## Residuals (not run)

- `tail -f` (row 14): inferred from gate code; not run.
- capture-source network egress (`urlopen` to an HTTP host), and `limb-mutation-check.py` which writes instrument bytes into a scratch copy (`limb-mutation-check.py:279–286, 407, 428, 444`): source evidence only.
- Counter write flags, source evidence only (not run): `citation-ground-check --json`, `kill-rule-check --json`, `mirror-containment-check --json`, `recheck-audit --json`, `resolve-dispatch-check --json`, `gate-quote-audit --json`, `frontier-recheck-count --json`, `wave-registry --out` (`wave-registry.py:47`), `freeze-check --work`, `r46-c1-gate --work` (copytree/rmtree), `r46-landing-gate` (git commit/push inside its own fixtures, `:326–409`), `capture-binding-check.py:801` (`os.remove` of an S001 snapshot).
- Env: `HYAKU_SCRATCH` (figure-audit selftest writes), `PATH` head resolution, `GIT_EXTERNAL_DIFF`, `GIT_CONFIG_COUNT`: not isolated.
- GNU `sort`/`grep`: not installed or not tested; all sort/grep results are uutils/pi-uu-grep.

## Ranked table for round 69 (what the evidence supports)

1. **sort long-option prefixes** (`--compress-prog`, `--compress-p`, `--out`, `--outp`): one fix covers both the exec and write rows. Option: refuse any `--` token not in an explicit sort allow-list, not a denylist of exact names.
2. **`git show` commit-diff textconv and `git cat-file --textconv/--filters`**: either auto-append `--no-textconv --no-ext-diff` to every admitted `git show` and refuse `cat-file --textconv/--filters` in the grammar, or refuse both. Y3 and G10/G20 are the test cases.
3. **`frontier-recheck-count.py --root`**: the counter is the exec primitive. Either refuse `--root` outside the lane, or treat its `recheck:` runner as a counter-level change.
4. **Python head**: require `-P` (or `-I`) for admitted counters, and refuse `--out`/`--json`/`--work`/`--root` arguments that resolve outside the lane. Note `-P` is a flag the gate would have to add or require; it cannot be inferred from the derive string today.
5. **Write-temp (`sort -T`, `TMPDIR`) and `__pycache__`**: low; mention in the residual list, not a priority.

## Confidence

High for the measured rows (marker counts and strace events are direct). Medium for the git textconv default (Y3, one fixture, one git version). Not measured: GNU sort, network egress, `tail -f`, env rows 13.

## Cleanup and tooling

- Scratch `/fast/scratch/hyaku/kasegi-r68/RevengerC1/` removed after the harness and receipts were copied into `round-68/w1/RevengerC1/harness/`.
- Nothing written under the lane except this report and `round-68/w1/RevengerC1/`. No lane file, counter, claim, ledger, `.ufo/state/`, or fleet file was edited.
- Tooling: none installed or upgraded. Used the existing `/usr/bin/strace`, `git`, `python3`, and the host's uutils coreutils.
