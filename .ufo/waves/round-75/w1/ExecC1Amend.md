# ExecC1Amend — round 75 attempt 1, C1 recheck-cwd census counter amendment

Seat: ExecC1Amend (executor, leaf). Lane base: 748dfb666280adfb1e249fcf6a265c5d9951eefb (verified `git -C <lane> rev-parse HEAD`, exit 0). No lane file was written; no git mutation was run. Scratch dir removed (`rm -rf`, exit 0; presence test exit 1 = gone).

## Deliverable

- Scratch-only candidate, delivered as `.ufo/waves/round-75/w1/ExecC1Amend.patch` (150 lines, unified, labels `a/recheck-cwd-census.py` and `b/recheck-cwd-census.py`, for `patch -p1` inside `corpus/instruments/`).
- Base bytes: git blob 32b5529159432c4bc21a5400ef18012274452c48, mode 100755 (`git -C <lane> ls-tree 748dfb66… corpus/instruments/recheck-cwd-census.py`). The patch does not carry the mode; applying it keeps the existing 755 mode.
- Changed areas only: docstring (exclusion paragraph, restoration_only bullet, conformance line, six-case selftest text); new `has_restoration_recheck()` helper; `census()` counts `restoration_only` and prints `RESTORATION-ONLY <name>`; the `RECHECK-CWD` line gains ` restoration_only=%d`; selftest case 6 (restoration-only); `main()` RESULT gate `noprefix==0 and exit2_foreign==0 and norecheck==0 and restoration_only==0`.
- Exec surface unchanged: `bash -c` call sites base=1, amended=1 (`grep -c 'bash", "-c' <file>`, exit 0); `subprocess.run(` amended=1. The restoration value is never passed to `run_foreign`. (Receipt f.)

## Verification receipts (all under `.ufo/waves/round-75/w1/ExecC1Amend-evidence/`)

| Receipt | Command (abbreviated) | Result | Exit |
|---|---|---|---|
| a | `TMPDIR=<scratch>/tmp python3 amended-counter.py --selftest` | `selftest case=restoration-only ok … marker_present=False main_ret=1`; `selftest cases=6 failures=0` | 0 |
| b | amended `--root FX --lane FX` from foreign cwd, FX = fixture r.md (restoration-recheck only) + p.md (cd-prefixed true) | `RESTORATION-ONLY r.md`; `RECHECK-CWD entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=0 exit_other=0 norecheck=0 restoration_only=1`; `RECHECK-CWD-RESULT nonconformant`; marker test `test -e restoration-ran` exit 1 (absent) | 1 (census main) |
| b-base | base counter on same FX (before-survival) | `NORECHECK r.md`; `norecheck=1`; `RECHECK-CWD-RESULT conformant` | 0 |
| c (M-A) | M-A = restoration_only folded into norecheck (`diff -u`: 1 line changed, diff_exit 1) — `--selftest` | `restoration-only FAIL … norecheck=1 restoration_only=0`; `selftest cases=6 failures=1` | 1 |
| c (M-B) | M-B = RESULT keeps only noprefix/exit2_foreign (diff_exit 1) — `--selftest` | `restoration-only FAIL … main_ret=0`; `selftest cases=6 failures=1` | 1 |
| c (M-C) | M-C = restoration value executed through `run_foreign` (diff_exit 1) — `--selftest` | `restoration-only FAIL … marker_present=True`; `selftest cases=6 failures=1` | 1 |
| d0 | base counter `--selftest` (unamended survives) | `selftest cases=5 failures=0` | 0 |
| d | base vs amended `--root <lane> --lane <lane>` from foreign cwd, TMPDIR set | base: `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0` / `conformant` (exit 0). amended: identical fields plus ` restoration_only=0` / `conformant` (exit 0). `diff -u` of stdout: the single changed line is the RECHECK-CWD line; diff_exit 1 | 0 / 0 |
| e-pre | `git show … > base`; `cmp lane-file base` exit 0; `ls corpus/knowledge/*.md \| wc -l` = 90; `diff -u --label a/… --label b/… base amended` | patch 150 lines | diff 1 (expected) |
| e-apply | scratch copy of corpus/instruments with base bytes; `patch -p1 --dry-run`; `patch -p1` | dry-run ok, applied; `cmp patched amended` identical; patched `--selftest` → `selftest cases=6 failures=0` | 0 / 0 / 0 / 0 |
| f | grep count of `bash -c` sites | base 1, amended 1 | (grep exit 0) |

## Frozen A-targets (claims.json C1.after)

- A1 selftest `cases=6 failures=0`, exit 0 — **PASS** (receipt a).
- A2 lane census at base tree (knowledge file count = 90, `ls | wc -l` exit 0; entries=90 by construction): `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0`, `conformant`, exit 0 — **PASS** (receipt d). Drift after C2 (entries=91, exit0_foreign=69) is C2's declared drift and is not measured here.
- A3 kill rule: M-A, M-B, M-C each fail the new selftest with a failing case line and `failures=1`, exit 1; unamended survives (`cases=5 failures=0`, exit 0) — **PASS** (receipts c, d0).
- A4 value parity: every stable field equal between base and amended on the real tree; only stdout delta is inserted `restoration_only=0` — **PASS** (receipt d).

Kill rule (claims C1.kill_rule): none of A1–A4 failed; C1 is verified **at the candidate level** (scratch copy, patch applied to a copy of the base file). Landing into the lane is L1's integration step; this seat did not apply it.

## Deviations and notes

- Case 6 also asserts `exit0_foreign=1` (the p.md entry actually ran). This is stricter than the frozen wording and is consistent with the receipt b expectation; it strengthens, does not weaken, the predicate.
- The `RESTORATION-ONLY <name>` line is printed on every run that hits such a file (not only in verbose mode), mirroring `NORECHECK`. The real tree has none, so receipt d shows no extra line.
- Not in my file set, still open for L1 at landing (claims C1.scope): the `corpus/instruments/README.md` section naming the census and the SKILL.md gate-registry row for `recheck-cwd-census.py` (gate had no row at base). I did not write them.
- Process incident (disclosed): my first export ran under a `trap … EXIT` set in the persistent shell; the trap fired when the shell job exited and removed the scratch dir before the export was read. No receipts had been written yet. I re-exported (`git show … > base-counter.py`, exit 0, 238 lines) without a trap and removed the scratch dir explicitly at the end. No lane or fleet file was affected.
- Tooling: none installed or upgraded.
- Labrat probe: not spawned (not needed for this item).

## Checks for the main agent (post-integration)

1. Apply `ExecC1Amend.patch` with `patch -p1` inside `corpus/instruments/` (base mode 755 retained).
2. `TMPDIR=<scratch> python3 corpus/instruments/recheck-cwd-census.py --selftest` → `selftest cases=6 failures=0`, exit 0.
3. From a foreign cwd: `TMPDIR=<scratch> python3 <lane>/corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` → entries equal to `ls corpus/knowledge/*.md | wc -l` at the final tip (90 before C2; 91 after C2 per declared drift), `restoration_only=0`, `RECHECK-CWD-RESULT conformant`, exit 0.
4. Confirm the README section and SKILL.md registry row land with the counter.
