# ExecHarness — round 68 C1 independent reproduction

**Verdict: VERIFIED (C1 both ends reproduced from clean exports; byte-identical to committed receipts) — with 3 findings (none defeats C1).**

Combined receipt: `.ufo/waves/round-68/controls/seat-reproduction-r68.txt`. Raw outputs: `.ufo/waves/round-68/w1/ExecHarness/{base,cand}-{run,clone,fullexport}.out`.

## What I ran
```
S=/fast/scratch/hyaku/kasegi-r68/ExecHarness; L=/home/vgpnk/Projects/shokunin/kasegi-shokunin; TMPDIR=$S/tmp
git -C $L archive d0f48405e7fe44a53a28305785dc4d881a414194 corpus/instruments | tar -x -C $S/base
git -C $L archive 7c4f9f7ec096298b1edd1912249e5864ee73d985 .ufo/waves/round-68/controls | tar -x -C $S/base
git -C $L archive 82b3b7d4704e914eb224e7bb24e57aa9cbd8603f corpus/instruments .ufo/waves/round-68/controls | tar -x -C $S/cand
python3 -B $S/base/.ufo/waves/round-68/controls/c1-probe-run-r68.py --gate $S/base/.ufo/waves/round-68/controls/base-gate-d0f48405.py --work $S/w-base --mode base
python3 -B $S/cand/.ufo/waves/round-68/controls/c1-probe-run-r68.py --gate $S/cand/corpus/instruments/figure-audit.py --work $S/w-cand --mode candidate
```
Pins (sha256sum): base gate used = `controls/base-gate-d0f48405.py` `8147350c…7ad247` (exported base `corpus/instruments/figure-audit.py` is byte-identical, same hash); candidate gate `10c87100…b74fee8` (matches); counter `785e38fd…496b4b` in base export, cand export and live lane.

## Observed
Base (exit=1, wall 17939 ms):
```
MEASURE sort-compress-refused FAIL rc=1 marker_runs=18288
MEASURE git-textconv-refused FAIL rc=1 marker_runs=1
MEASURE read-only-controls-admitted ok controls=5 failed=0
MEASURE selftest FAIL selftest cases=73 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE red-fixture ok rc=1
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=18289
VERIFY measurements=8 failures=4 gate_sha256=8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247 mode=base
```
Candidate (exit=0, wall 15839 ms):
```
MEASURE sort-compress-refused ok rc=2 marker_runs=0
MEASURE git-textconv-refused ok rc=2 marker_runs=0
MEASURE read-only-controls-admitted ok controls=5 failed=0
MEASURE selftest ok selftest cases=77 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE red-fixture ok rc=1
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=8 failures=0 gate_sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 mode=candidate
```
Failure counts 4 and 0 as expected. `diff <(grep -E '^(MEASURE|VERIFY)' controls/c1-base-donothing-r68.txt) <(… base-run.out)` → empty (BASE-IDENTICAL); same for `c1-candidate-trial-r68.txt` vs candidate run (CAND-IDENTICAL).

Extra hardening run (C/D): `--lane` pointed at a fresh `git clone --no-hardlinks` of the lane, toplevel asserted, checked out detached at d0f48405 / 82b3b7d4 (`status --porcelain` 0 lines). Results identical to A/B: failures=4 exit 1 / failures=0 exit 0 (99.57 s for both incl. clones). So the result does not depend on the live lane's dirty working tree.

## Host dependence
Host: GNU coreutils sort 9.12, git 2.56.0, Python 3.14.8, 32 cores. Compressor runs = 18288 in 3/3 base runs (fixture big.txt 480000 bytes, `sort -S 1K`); magnitude depends on sort's buffer floor/merge fan-in per coreutils build, requirement is only >0 for the base and ==0 for the candidate. Textconv driver runs = 1 (base) / 0 (cand). `no-write-side-effect` marker_runs=18289 = 18288+1, consistent.

## Findings / residuals
1. **Seat spec defect (export path):** `git archive d0f48405 … .ufo/waves/round-68/controls` fails (`fatal: pathspec '.ufo/waves/round-68/controls' did not match any files`) — controls first land in 3dfe6f1. I took the controls from 7c4f9f7 (`git diff --stat 3dfe6f1 7c4f9f7 -- .ufo/waves/round-68/controls` empty).
2. **Seat spec count:** the spec asks for "nine MEASURE lines"; the counter emits eight MEASURE lines plus one VERIFY (matching `measurements=8` in the frozen predicate). No missing line.
3. **Counter docstring vs code:** docstring item 3 says "six legitimate read-only derives"; the code has five controls and prints `controls=5` (the frozen predicate says 5/5, so the predicate matches the code; docstring is stale). Also `real-ledger` uses `--lane` (default = live lane tree) and needs a git-backed lane: against a plain `git archive` tree it reads `figures=35 ok=11 stale=24` (all 24 = `git show/ls-tree/cat-file` history derives), giving failures=5 base / 1 cand. Diagnostic only; clean-clone runs pass.

No tools installed. Scratch `/fast/scratch/hyaku/kasegi-r68/ExecHarness` removed. No lane git mutation; only this report, `w1/ExecHarness/`, and `controls/seat-reproduction-r68.txt` written.
