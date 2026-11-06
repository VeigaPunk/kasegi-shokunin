# ExecC1Battery — round-81 attempt 1 (wave of 13 seats; this is one seat)

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Freeze commit: `7ad3118c86ee14fde433d73671cc407668533cec` (base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`)
Seat task: score C1 `depth:verifiability` with the frozen counter — the scored receipt.

## Verdict up front

C1 scored with the frozen counter; no false predicate inside this seat's scope (P2, P3, P1, P8, P4 and the 28-new-row inspection).

| limb | result |
|---|---|
| P2 sha256 of the four frozen C1 bytes | all four match `claims.json` (and `controls/c1-candidate-r81.txt`) |
| P3 (twice, cold) | `MUTBAT target_sha256=a3b58aa5… baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3`, rc0 both runs |
| P3 run-to-run agreement | `diff p3-run1.txt p3-run2.txt` empty (all 59 MUTANT lines and the MUTBAT line identical); kept outputs identical 59/59 after normalising scratch paths |
| P1 | `selftest cases=22 failures=0`, rc0 |
| P8 | `mutbat selftest ok …` rc0 |
| P4 | ten FORGERY lines; five `counter=r80` rc0 `killed=56 survived=0 dirty=0 notderived=0`, five `counter=r81` rc1 |
| 28 new rows (M1 M2 S01…S43) | 28 rows, rc=1, exactly one FAIL each, and each FAIL case is the row's declared `kill_cases[0]` |
| P5 / P6 / P7 | not run by this seat (other seats own the tree/pin/static limbs) |

My P3 `MUTANT`/`MUTBAT` lines and my P4 `FORGERY` lines are diff-identical to the freeze-commit controls (`controls/c1-candidate-r81.txt`, `controls/c1-forgeries-r81.txt`), i.e. the frozen controls reproduce from the committed bytes alone.

## 1 Frozen bytes at HEAD (P2 limb)

`git diff 7ad3118c86ee14fde433d73671cc407668533cec -- .ufo/waves/round-81/c1 .ufo/waves/round-81/controls` is empty; `git status --porcelain -- .ufo/waves/round-81 corpus/instruments/recheck-cwd-census.py` shows only untracked `w1/` dispatch files. HEAD is the freeze commit.

| file | sha256 at HEAD | claim | match |
|---|---|---|---|
| `.ufo/waves/round-81/c1/recheck-cwd-census.py` | `a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0` | a3b58aa5…6dbec0 | yes |
| `.ufo/waves/round-81/c1/mutbat.py` | `fa96223b38f93b5fd9a08d11923dc7f7fe7f35a61b734c0cb3503381062843b4` | fa96223b…43b4 | yes |
| `.ufo/waves/round-81/c1/mutant-table.json` | `abcc834eb21102f11a11cc91b7482f68957f988ea91e68e803a82251a216d095` | abcc834e…d095 | yes |
| `.ufo/waves/round-81/c1/build-table.py` | `57ab70e9ff39d591ed98c2de60ee9323b735b981118b3f305ef40d3188f06a7f` | 57ab70e9…6a7f | yes |
| `.ufo/waves/round-81/controls/c1-forgeries-r81.py` | `28fde3871e8fc7ead1f9f345dd39ea4779443c3f451003c997acf9cd48539246` | (executed control; not pinned in claims) | n/a |

The counter printed `MUTBAT target_sha256=a3b58aa5…` in every run, so the scored target is the frozen candidate, not a working-tree variant. The live instrument `corpus/instruments/recheck-cwd-census.py` still hashes `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698`, which is the `target_sha256` recorded in the do-nothing control `controls/c1-donothing-r81.txt` — the do-nothing limb still names the landed r80 bytes.

## 2 P3 — frozen counter, two cold runs

Run 1 (verbatim in Appendix A) and run 2 (verbatim in Appendix B):

```
python3 -B .ufo/waves/round-81/c1/mutbat.py \
  --target .ufo/waves/round-81/c1/recheck-cwd-census.py \
  --table  .ufo/waves/round-81/c1/mutant-table.json \
  --expect-cases 22 --work <scratch>/w --keep <scratch>/keep
```

Both exited 0, wall time 69.5 s and 70.4 s. The two output files are byte-identical (`diff` empty); the two `--keep` trees are identical file-for-file after normalising the scratch path embedded in some detail strings (59/59 `*.out`). So the run-to-run agreement is per row, not just per tally.

Tally reading:

- `rows=59` = 56 non-neutral + 3 neutral, matching the frozen table's class split (55 `assertion` + 1 `exception` + 3 `neutral`).
- `killed=56`, `neutral_ok=3/3`, `survived=miskilled=dirty=notderived=0` — the counter's own pass condition.
- `K-M3 verdict=EXCEPTION-KILL counted=yes` is the one `class=exception` row; the counter counts an exception kill only for a row declared `exception` (`verdict()`/`counts` in `mutbat.py`), so this is the documented rule, not an escape hatch.
- `baseline=ok` is the exact-string limb (`rc==0` and `^selftest cases=22 failures=0$` and zero FAIL lines and no `Traceback`), not merely rc0.

## 3 P1 — candidate selftest

```
TMPDIR=<scratch> python3 -B .ufo/waves/round-81/c1/recheck-cwd-census.py --selftest
…
selftest cases=22 failures=0
```
rc=0. Full output in `ExecC1Battery-receipts/p1-candidate-selftest.txt`.

## 4 P8 — counter selftest

```
mutbat selftest ok got={'T-KILL': 'KILLED', 'T-MIS': 'MISKILLED', 'T-SURV': 'SURVIVED', 'T-ABSENT': 'NOT-DERIVED', 'T-EXC': 'EXCEPTION-KILL', 'T-EXCA': 'EXCEPTION-KILL', 'T-NEU': 'NEUTRAL-OK', 'T-NEUBAD': 'NEUTRAL-BROKEN'} counted={'T-KILL': 'yes', 'T-MIS': 'no', 'T-SURV': 'no', 'T-ABSENT': 'no', 'T-EXC': 'yes', 'T-EXCA': 'no', 'T-NEU': 'yes', 'T-NEUBAD': 'no'} all_killed_exit=True location_forgery_exit=False baseline_forgery_exit=False bad_tables=[True, True, True]
```
rc=0 — including `T-MIS → MISKILLED counted=no`, `T-NEUBAD → NEUTRAL-BROKEN counted=no`, the location forgery exiting non-zero and the baseline-FAIL toy exiting non-zero.

## 5 P4 — five stub forgeries, two counters

All ten lines in Appendix C. Reading:

| forgery | r80 counter | r81 counter |
|---|---|---|
| F1-location | rc=0 `killed=56 survived=0 dirty=0 notderived=0` | rc=1 `miskilled=56 neutral_ok=0/3` |
| F2-selfhash | rc=0 `killed=56 survived=0 dirty=0 notderived=0` | rc=1 `miskilled=56 neutral_ok=1/3` |
| F3-sibling | rc=0 `killed=56 survived=0 dirty=0 notderived=0` | rc=1 `miskilled=56 neutral_ok=0/3` |
| F4-baseline | rc=0 `killed=56 survived=0 dirty=0 notderived=0` | rc=1 `baseline=bad miskilled=56 neutral_ok=0/3` |
| F5-allcases | rc=0 `killed=56 survived=0 dirty=0 notderived=0` | rc=1 `killed=56 miskilled=0 neutral_ok=0/3` |

Every `counter=r80` line ends `killed=56 survived=0 dirty=0 notderived=0` with rc=0; every `counter=r81` line has rc=1 — the r81 tally rejects all five without reading P2 (F5 is rejected on `neutral_ok=0/3` alone while still scoring `killed=56`). That is exactly predicate P4, and it is the counter-independence limb the round-80 routed defect asked for.

## 6 The 28 new rows — exactly one FAIL each, on the declared case

Each row was scored through the frozen table; `rc` and the FAIL line are from the kept output of run 1 (`ExecC1Battery-mutants/<id>.out`, identical to run 2). All 28 rows are `class=assertion`, all rc=1, all with `fails=1`.

| id | rc | the one FAIL line (verbatim) | declared kill_case | case match |
|---|---|---|---|---|
| M1 | 1 | `selftest case=tmpdir-file FAIL ret=-99 stdout="raised=NotADirectoryError(20, 'Not a directory')" stderr=''` | tmpdir-file | yes |
| M2 | 1 | `selftest case=timeout-bucket FAIL got=entries=1,exit0_foreign=1,exit1_foreign=0,exit2_foreign=0,exit_other=0,noprefix=0,norecheck=0 want=entries=1,exit0_foreign=0,exit1_foreign=0,exit2_foreign=0,exit_other=1,noprefix=0,norecheck=0` | timeout-bucket | yes |
| S01 | 1 | `selftest case=prefix-literal FAIL got=entries=3,exit0_foreign=2,exit1_foreign=1,exit2_foreign=0,exit_other=0,noprefix=0,norecheck=0 want=entries=3,exit0_foreign=2,exit1_foreign=1,exit2_foreign=0,exit_other=0,noprefix=2,norecheck=0` | prefix-literal | yes |
| S02 | 1 | `selftest case=prefix-literal FAIL got=entries=3,exit0_foreign=2,exit1_foreign=1,exit2_foreign=0,exit_other=0,noprefix=1,norecheck=0 want=entries=3,exit0_foreign=2,exit1_foreign=1,exit2_foreign=0,exit_other=0,noprefix=2,norecheck=0` | prefix-literal | yes |
| S04 | 1 | `selftest case=conform-limbs FAIL exit2_only ret=0 norecheck_only ret=1` | conform-limbs | yes |
| S05 | 1 | `selftest case=conform-limbs FAIL exit2_only ret=1 norecheck_only ret=0` | conform-limbs | yes |
| S07 | 1 | `selftest case=output-lines FAIL lines6=3 lines8=3 lines1=7 lines15=3` | output-lines | yes |
| S08 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[28]` | gate-predicates | yes |
| S09 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[29]` | gate-predicates | yes |
| S10 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[31]` | gate-predicates | yes |
| S11 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[33]` | gate-predicates | yes |
| S12 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[34]` | gate-predicates | yes |
| S13 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[35]` | gate-predicates | yes |
| S14 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[36, 38]` | gate-predicates | yes |
| S15 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[37]` | gate-predicates | yes |
| S16 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[36, 38]` | gate-predicates | yes |
| S19 | 1 | `selftest case=output-lines FAIL lines6=1 lines8=2 lines1=6 lines15=3` | output-lines | yes |
| S20 | 1 | `selftest case=output-lines FAIL lines6=2 lines8=1 lines1=6 lines15=3` | output-lines | yes |
| S21 | 1 | `selftest case=output-lines FAIL lines6=2 lines8=2 lines1=1 lines15=2` | output-lines | yes |
| S22 | 1 | `selftest case=output-lines FAIL lines6=2 lines8=2 lines1=6 lines15=2` | output-lines | yes |
| S25 | 1 | `selftest case=tmpdir-unset FAIL refused=None raised=TypeError('stat: path should be string, bytes, os.PathLike or integer, not NoneType')` | tmpdir-unset | yes |
| S30 | 1 | `selftest case=usage-guards FAIL usage_ret=0 missing_corpus='recheck-cwd: no corpus/knowledge under /fast/scratch/hyaku/kasegi-r81/ExecC1Battery/w/mutbat-run-t8hcoxb4/recheck-cwd-selftest-8uzf5j_y/case19-empty' lane_ret=0` | usage-guards | yes |
| S31 | 1 | `selftest case=usage-guards FAIL usage_ret=2 missing_corpus=None lane_ret=0` | usage-guards | yes |
| S37 | 1 | `selftest case=conform-limbs FAIL exit2_only ret=1 norecheck_only ret=1` | conform-limbs | yes |
| S39 | 1 | `selftest case=usage-guards FAIL usage_ret=2 missing_corpus='recheck-cwd: no corpus/knowledge under /fast/scratch/hyaku/kasegi-r81/ExecC1Battery/w/mutbat-run-25cc7bf6/recheck-cwd-selftest-6tf6su1r/case19-empty' lane_ret=1` | usage-guards | yes |
| S40 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[30]` | gate-predicates | yes |
| S41 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[32]` | gate-predicates | yes |
| S43 | 1 | `selftest case=gate-predicates FAIL rows=40 expect=40 bad=[39]` | gate-predicates | yes |

28 rows / 28 rows matched; total FAIL lines across the 28 kept outputs = 28, so there is no second, unclaimed failure hiding behind a row's declared case.

## 7 Observations — routed, not verdict changes

These are findings outside the frozen sets; per the kill rule they are routed to round 82 and do not move any verdict.

1. **Case coverage is 15 of 22, not 22.** The union of declared `kill_cases` over the 56 non-neutral rows is 15 case IDs, and the union of case IDs actually failing under any of the 59 mutants is the same 15. Seven selftest cases are never failed by any frozen mutant: `result-main`, `tmpdir-parent`, `scratch-cleanup`, `first-line`, `restoration-only`, `both-headers`, `relabel-detection`. So `killed=56/56` means "every mutant dies on its declared case"; it does not mean the 22 checks are mutation-covered. `result-main` (the RESULT polarity check) is the sharpest gap. Route: add rows for these seven in r82.
2. **S37's FAIL detail is not diagnostic.** Its detail `exit2_only ret=1 norecheck_only ret=1` is byte-identical to the case's passing detail in `NT1.out` (`selftest case=conform-limbs ok exit2_only ret=1 norecheck_only ret=1`). The kill is genuine — the row broadens `line.startswith("restoration-recheck:")` to `startswith("restoration")`, so the norecheck-only fixture counts `restoration_only=1`, and the ok-predicate's unprinted limb `"norecheck=1 restoration_only=0" in out15n` fails while both `ret`s stay 1. Route: the conform-limbs detail should print the limb that failed, otherwise a FAIL line cannot be audited from the kept output alone.
3. **12 of the 28 new rows die on one case ID.** S08–S16, S40, S41 and S43 all kill via `gate-predicates`' `bad=[…]` limb; the case ID is case-matched but cannot discriminate which predicate broke — only the detail does (`bad=[28] … bad=[36, 38] … bad=[39]`). Same for the three `usage-guards` rows and the five `output-lines` rows. Route: split the aggregate predicates case into per-row case IDs, or make the depth claim explicit about detail-level discrimination.
4. **Two different mutations land on the same predicate rows.** S14 (`F1 BoolOp limb deletion`) and S16 (`any → all` quantifier) both report `bad=[36, 38]` from distinct, non-overlapping anchors. Not a defect; it records that predicate rows 36 and 38 each carry two limbs and that one mutant can trip both.
5. **Duplicate anchors are present but not no-ops.** Six anchors are shared by 2–3 rows with different replacements (`return clean_ok is True and limb_log` ×3, `return neg_ok is False and neg_ret_ok …` ×2, `return set(done) == set(required) …` ×2, `first_ran is True and rest_ran is False` ×2, `if tmp is not None and not os.path.isdir …` ×2, `prefix = "cd %s && " % lane` ×2). Every row derived exactly once (`src.count(anchor) == 1`, `notderived=0`), so each is a real mutation; but two rows mutating one line are one line of code, not two independent defects.
6. **The r80-survivor identity of the 28 new rows is only count-aligned here.** The frozen do-nothing control over the landed `420151fd` bytes reads `killed=28 survived=28 neutral_ok=0/3` and the live instrument still hashes `420151fd`, so the aggregate (28 survivors) matches the 28 new rows. This seat did not re-run each new row's mutant against the r80 bytes (the item bounds me to the six named commands). Per-row identity is for the attack/reviewer seats.
7. **Neutral-row mechanism, read from the frozen counter.** `run_selftest()` copies the file into a fresh `tempfile.mkdtemp(dir=work)` before every run, so every row — neutral included — is scored from a moved copy. The three neutral rows are behaviour-preserving edits (NT1: comment after the shebang, shifting every later line by one; NT2: local parameter `counts → cnt`; NT3: trailing comment on `TIMEOUT`), and each must reproduce the exact `cases=22 failures=0` line. This is the limb the F1–F4 forgeries fail (`neutral_ok=0/3`), i.e. the tally is not derivable from the target's bytes alone.

## 8 Method and bounds

- Commands run (all over the committed bytes at HEAD; nothing else executed):
  1. `sha256sum .ufo/waves/round-81/c1/*` (+ `controls/c1-forgeries-r81.py`) and `git diff 7ad3118… -- .ufo/waves/round-81/c1 .ufo/waves/round-81/controls`.
  2. P3 twice, distinct `--work`/`--keep` dirs.
  3. P1 `recheck-cwd-census.py --selftest`.
  4. P8 `mutbat.py --selftest --work <scratch>`.
  5. P4 `controls/c1-forgeries-r81.py --lane <lane> --work <scratch>/forg`.
  6. Kept-output inspection for the 28 new rows (read-only over `--keep`).
- Scratch: `/fast/scratch/hyaku/kasegi-r81/ExecC1Battery` (deleted at the end of the seat). Nothing was written under `/tmp`, no counter/gate output outside scratch, no git/jj writes, no lane-file edits outside `w1/`, no tool installs or upgrades (none needed), no host sysctl or service changes.
- Artifacts: this report; `ExecC1Battery-receipts/` (p1, p3 run1, p3 run2, p4, p8, sha256 list); `ExecC1Battery-mutants/` (28 kept `*.out` for the new rows).

---

## Appendix A — P3 run 1, verbatim (59 MUTANT lines + MUTBAT), rc=0

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 failed_cases=gate-consume,gate-negpolarity,gate-regs counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=gate-consume,gate-negpolarity counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 failed_cases=gate-negpolarity,gate-predicates counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-X1 verdict=KILLED rc=1 fails=1 failed_cases=gate-consume counted=yes
MUTANT K-X2a verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-X2b verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-M8 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-W1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-W2 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-N1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-P1 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-P2 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-G1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-C1 verdict=KILLED rc=1 fails=1 failed_cases=gate-wiring counted=yes
MUTANT K-NP verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-CL verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-T1 verdict=KILLED rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=yes
MUTANT N10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N21 verdict=KILLED rc=1 fails=2 failed_cases=prefix-census,timeout-bucket counted=yes
MUTANT N25 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N26 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N27 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N30 verdict=KILLED rc=1 fails=1 failed_cases=prefix-census counted=yes
MUTANT T1 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT T2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT M1 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-file counted=yes
MUTANT M2 verdict=KILLED rc=1 fails=1 failed_cases=timeout-bucket counted=yes
MUTANT S01 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S02 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S04 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S05 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S37 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S07 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S19 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S20 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S21 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S22 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S08 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S09 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S41 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S40 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S12 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S13 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S14 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S16 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S15 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S43 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S25 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-unset counted=yes
MUTANT S30 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S31 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S39 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT NT1 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT2 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT3 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTBAT target_sha256=a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0 baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
```

## Appendix B — P3 run 2, verbatim (independent `--work`/`--keep`), rc=0

```
MUTANT K-M1 verdict=KILLED rc=1 fails=3 failed_cases=gate-consume,gate-negpolarity,gate-regs counted=yes
MUTANT K-M2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=gate-consume,gate-negpolarity counted=yes
MUTANT K-M4 verdict=KILLED rc=1 fails=2 failed_cases=gate-negpolarity,gate-predicates counted=yes
MUTANT K-M5 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-X1 verdict=KILLED rc=1 fails=1 failed_cases=gate-consume counted=yes
MUTANT K-X2a verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-X2b verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-M8 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-W1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-W2 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-N1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-P1 verdict=KILLED rc=1 fails=1 failed_cases=gate-checkids counted=yes
MUTANT K-P2 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-G1 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-C1 verdict=KILLED rc=1 fails=1 failed_cases=gate-wiring counted=yes
MUTANT K-NP verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT K-CL verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT K-T1 verdict=KILLED rc=1 fails=2 failed_cases=tmpdir-file,tmpdir-refusal counted=yes
MUTANT N10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N21 verdict=KILLED rc=1 fails=2 failed_cases=prefix-census,timeout-bucket counted=yes
MUTANT N25 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N26 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N27 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT N30 verdict=KILLED rc=1 fails=1 failed_cases=prefix-census counted=yes
MUTANT T1 verdict=KILLED rc=1 fails=2 failed_cases=gate-checkids,gate-wiring counted=yes
MUTANT T2 verdict=KILLED rc=1 fails=1 failed_cases=gate-negpolarity counted=yes
MUTANT M1 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-file counted=yes
MUTANT M2 verdict=KILLED rc=1 fails=1 failed_cases=timeout-bucket counted=yes
MUTANT S01 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S02 verdict=KILLED rc=1 fails=1 failed_cases=prefix-literal counted=yes
MUTANT S04 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S05 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S37 verdict=KILLED rc=1 fails=1 failed_cases=conform-limbs counted=yes
MUTANT S07 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S19 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S20 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S21 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S22 verdict=KILLED rc=1 fails=1 failed_cases=output-lines counted=yes
MUTANT S08 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S09 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S10 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S41 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S40 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S11 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S12 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S13 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S14 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S16 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S15 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S43 verdict=KILLED rc=1 fails=1 failed_cases=gate-predicates counted=yes
MUTANT S25 verdict=KILLED rc=1 fails=1 failed_cases=tmpdir-unset counted=yes
MUTANT S30 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S31 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT S39 verdict=KILLED rc=1 fails=1 failed_cases=usage-guards counted=yes
MUTANT NT1 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT2 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT3 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTBAT target_sha256=a3b58aa52ba0744199ee97e6bd837e62c499e3e6af03a2fc26f0e6e3746dbec0 baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3
```

## Appendix C — P4 forgery controls, verbatim (ten FORGERY lines)

```
FORGERY F1-location counter=r80 forgery_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F1-location counter=r81 forgery_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=bc552edb42383017bfa736dbf9c7986fa9b7a57352d65ca04e4cda743b7033f6 baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F2-selfhash counter=r80 forgery_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F2-selfhash counter=r81 forgery_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 2, "NEUTRAL-OK": 1} MUTBAT target_sha256=196d3ecf39f36eca189b7fffaec01e69e289bf0d956bd2d494ab8c90f207d266 baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=1/3
FORGERY F3-sibling counter=r80 forgery_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F3-sibling counter=r81 forgery_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=c05fadc39828af64cc254046c94910f1fdba230b838d2c70cb24677942e0c502 baseline=ok rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F4-baseline counter=r80 forgery_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F4-baseline counter=r81 forgery_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e rc=1 verdicts={"MISKILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=3dc3018124451ee11b90480f23b9e4821372fcdde4ecdad9d955426762044a9e baseline=bad rows=59 killed=0 survived=0 miskilled=56 dirty=0 notderived=0 neutral_ok=0/3
FORGERY F5-allcases counter=r80 forgery_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d rc=0 verdicts={"KILLED": 56} MUTBAT target_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d baseline=ok rows=56 killed=56 survived=0 dirty=0 notderived=0
FORGERY F5-allcases counter=r81 forgery_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d rc=1 verdicts={"KILLED": 56, "NEUTRAL-BROKEN": 3} MUTBAT target_sha256=d60c17cbff3a587883885294076ea5b2baab1d69acc2acbeb32bda848807016d baseline=ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=0/3
```
