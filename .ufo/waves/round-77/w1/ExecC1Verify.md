# ExecC1Verify — round-77 w1, C1 build+verify (scratch-only)

Seat: ExecC1Verify (leaf executor; no subagents, no background services, no installs — stdlib
python3/bash/git only, pacman untouched). Scope: C1 (depth:verifiability) build+verify of the
recheck-cwd census amendment, entirely in scratch
`/fast/scratch/hyaku/kasegi-r77/ExecC1Verify/` (removed before yield; receipts copied into this
report dir first). Lane reads only; the only lane writes are the files in this report dir.
No git/jj mutation anywhere (read-only `show|rev-parse|log|status|cmp` only).

Lane state observed (read-only): HEAD = `539a43877809bd90b6f506e8fd24a6d871598cd5` (the freeze
commit, "round-77: freeze C1 … and C2 …"), parent `2e53fc7` (round-76 base). `git status
--porcelain` shows 6 untracked paths only (w1 dispatch/spec/ready/w1 dir, `corpus/lessons/round-77.md`);
`corpus/knowledge/` is clean, so the census inputs are the frozen tree.

## Verdict line

- **A1 PASS** — `python3 -B .ufo/waves/round-77/c1-amended-reference.py --selftest` → rc=0,
  last line `selftest cases=12 failures=0`, byte-identical to
  `controls/c1-reference-selftest-r77.txt`. (Verified on the frozen reference bytes; the
  landing-commit bytes are L1's to produce and are outside this seat.)
- **A2 PASS** — `TMPDIR=$S/tmp python3 -B <reference> --root <lane> --lane <lane>` → rc=0,
  printed exactly `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69
  exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0` + `RECHECK-CWD-RESULT
  conformant`; `cmp` vs `controls/c1-base-realtree-census-r77.txt` = BYTE-IDENTICAL.
- **A3-rebuild PASS** — all five mutants rebuilt from `c1-mutant-transforms.md` (not copied
  from controls) are byte-identical to the controls copies (sha256 equal, `cmp` clean), and
  all five kill: rc=1 each, with the exact expected verdict classes (table below).
- **A6 PASS** — diff base→reference touches only the module docstring's `--selftest` sentence
  and `selftest()` (docstring + body, incl. its nested `check()` and case comments);
  `first_recheck()`, `has_restoration_recheck()`, `run_foreign()`, `census()`, `main()` are
  byte-identical to base (difflib hunks + `ast.get_source_segment` equality both).

## 1. Base export and hashes (step 1)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show \
    2e53fc74776824898b5c5eb914aeddc19a091157:corpus/instruments/recheck-cwd-census.py \
    > $S/base-counter.py          # rc=0
$ sha256sum $S/base-counter.py
e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a  base-counter.py
```
Expected `e666ae11…a21a` — **MATCH**. Both commits verified present:
`git rev-parse --verify 2e53fc7…^{commit}` and `…539a438…^{commit}` → rc=0.

Frozen reference: `sha256sum .ufo/waves/round-77/c1-amended-reference.py` →
`18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33` — **MATCH** (expected
`18bfc439…8a33`).

## 2. A6 structural check (step 2)

`difflib.unified_diff` base→reference: 175 diff lines, exactly 6 hunks, all inside two
regions — hunk `@@ -28,9 +28,10 @@` (module docstring `--selftest` sentence: "six cases" →
"twelve checks … gate …"), and hunks `@@ -120,15 +121,25 @@`, `@@ -157,6 +168,7 @@`,
`@@ -177,7 +189,8 @@`, `@@ -229,8 +242,8 @@`, `@@ -240,12 +253,89 @@` (all inside `def
selftest():` up to its `finally:` — REQUIRED_CHECKS, `done.append`, case-2/case-6 comments,
cases 7–8, the registration, the four gate checks, the `cases=%d failures=%d` print).
Independent AST check (`ast.get_source_segment` on both parses):

```
A6 first_recheck()            BYTE-IDENTICAL
A6 has_restoration_recheck()  BYTE-IDENTICAL
A6 run_foreign()              BYTE-IDENTICAL
A6 census()                   BYTE-IDENTICAL
A6 main()                     BYTE-IDENTICAL
A6 selftest() identical? False     # expected: this is the amendment
module docstring differs: True     # expected: the --selftest sentence
```

Claim's case-6 RESULT limb move confirmed in the diff: `ret6 == 1 and
"RECHECK-CWD-RESULT nonconformant" in out6` removed from `check("restoration-only", …)` and
reborn as `regs["restoration-only-result"] = lambda out, ret: (…)`, consumed by
gate-regs/gate-consume/gate-negpolarity/gate-checkids. Evidence:
`ExecC1Verify-a6-diff.txt`.

## 3. Reference runs (step 3)

```
$ python3 -B $REF --selftest                                    # rc=0
selftest cases=12 failures=0                                     # last line
$ cmp <out> controls/c1-reference-selftest-r77.txt               # BYTE-IDENTICAL

$ TMPDIR=$S/tmp python3 -B $REF --root $LANE --lane $LANE        # rc=0
RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
$ cmp <out> controls/c1-base-realtree-census-r77.txt             # BYTE-IDENTICAL
```
All 12 case lines `ok` (prefix-census, result-main, tmpdir-parent, scratch-cleanup,
first-line, restoration-only, both-headers, relabel-detection, gate-regs, gate-consume,
gate-negpolarity, gate-checkids). Full outputs: `ExecC1Verify-reference-selftest.txt`,
`ExecC1Verify-realtree-census.txt`.

## 4. Mutant rebuild and kills (steps 4–5)

Rebuilt in scratch from the frozen transform table only (each replacement asserted to match
exactly once). sha256 rebuilt == controls, and `cmp` clean for all five:

| id | rebuilt sha256 (= controls) | rc | FAIL lines observed | traceback | last line |
|----|------------------------------|----|----------------------|-----------|-----------|
| K-M1 | `c274649223deecdc228345cc49a2c0075d23893a9233f500667650b550f6a2b9` | 1 | L9 `gate-regs FAIL registered=[]`; L10 `gate-consume FAIL no-registration`; L11 `gate-negpolarity FAIL no-registration` | 0 | `selftest cases=12 failures=3` |
| K-M2 | `b7772949f3b70f169c441714bdf5e87e3cf3283bf431e524c976edc4d2ba6f23` | 1 | L11 `gate-negpolarity FAIL neg_ok=True` (gate-consume ok clean_ok=True) | 0 | `selftest cases=12 failures=1` |
| K-M3 | `1fd8d29ad085ce0367c2d3cd74fbd3149f04d8d3378e3da9b2c1f7c5e3968f3f` | 1 | L10 `gate-consume FAIL exception=NameError("name 'out6' is not defined")`; L11 `gate-negpolarity FAIL not-evaluated-after-exception` | 0 | `selftest cases=12 failures=2` |
| K-M4 | `7f5bb9360d9eaa38b9d8b5ea76d4b68e4fbec652c6cf3bb65f144eee0787d67e` | 1 | L11 `gate-negpolarity FAIL neg_ok=False` (gate-consume ok clean_ok=True) | 0 | `selftest cases=12 failures=1` |
| K-M5 | `b7af772223131dc6081fb8561db26dbeca2911cc3ae9ac6d9fef605b7cbb5ff0` | 1 | L11 `gate-checkids FAIL missing=['both-headers'] extra=[]` | 0 | `selftest cases=11 failures=1` |

All five match the transforms doc's expected verdicts and its committed-derivation sha
prefixes (`c2746492…`, `b7772949…`, `1fd8d29a…`, `7f5bb936…`, `b7af7722…`). K-M2 is the
required m2b-class kill: assertion failure (`gate-negpolarity FAIL neg_ok=True` with the
closure neutered), no traceback — R127 satisfied. K-M3 dies as an exception-class kill
(`NameError` logged as the exception class, closure never evaluated after), which is the
documented non-semantic class, distinct from K-M2's assertion kill. Every run output is
byte-identical to its committed receipt `controls/m*-*.py.out` (5/5 `cmp` clean).
Per-run outputs: `ExecC1Verify-m1.txt` … `ExecC1Verify-m5.txt`.

TMPDIR note: a first pass ran with `TMPDIR=$S/tmp` and differed from the committed `.out`
receipts on exactly one line (`selftest case=tmpdir-parent … dirs='…/tmp',…` vs
`dirs=None,None,None`) — that detail line embeds the generator's TMPDIR. Re-run in the
spec's exact form (no TMPDIR override) reproduces every receipt byte-for-byte; both passes
are recorded (`ExecC1Verify-runs-tmpdir.txt`, `ExecC1Verify-outdiff.txt`,
`ExecC1Verify-final-runs.txt`).

## 5. Commands and environment

All runs under `python3 -B` (no .pyc writes). Realtree census ran with `TMPDIR=$S/tmp`
(scratch); scratch parents verified inside TMPDIR by the counter's own tmpdir-parent check.
Representative invocations (all rc shown above):

```
git -C <lane> show 2e53fc7…:corpus/instruments/recheck-cwd-census.py > $S/base-counter.py
python3 -B .ufo/waves/round-77/c1-amended-reference.py --selftest
TMPDIR=$S/tmp python3 -B .ufo/waves/round-77/c1-amended-reference.py --root <lane> --lane <lane>
env -u TMPDIR python3 -B $S/m{1..5}.py --selftest
```

## 6. Evidence files (this dir)

- `ExecC1Verify-a6-diff.txt` — full unified diff base→reference (175 lines)
- `ExecC1Verify-sha256.txt` — hash manifest: base export, reference, 5 rebuilt mutants, 5 controls copies
- `ExecC1Verify-reference-selftest.txt`, `ExecC1Verify-realtree-census.txt` — reference runs
- `ExecC1Verify-m1.txt` … `ExecC1Verify-m5.txt` — mutant runs (byte-identical to controls/*.out)
- `ExecC1Verify-runs-tmpdir.txt`, `ExecC1Verify-outdiff.txt`, `ExecC1Verify-final-runs.txt` — TMPDIR-variant pass, its single-line diff vs receipts, and the final byte-identical pass
- `ExecC1Verify-lane-state.txt` — lane HEAD/log/porcelain snapshot at run time

## 7. Risks / blockers

- None for C1 within this seat's scope. A1's landing-commit clause and A2's post-C2 drift
  expectation (entries=92, exit0_foreign=70) are L1 integration-time facts, not verifiable
  from the frozen reference alone.
- `corpus/lessons/round-77.md` is untracked in the working tree; it is not a census input
  (`corpus/knowledge/` only) and does not affect A2's byte-identity.
