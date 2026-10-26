# Wave 2 receipt — seat MutCtrTimeoutKilled (counter mutant: kill-command timeout counted as killed)

Round 31 / hyaku run 7. Subject: `corpus/instruments/limb-mutation-check.py`.
All attack work in disposable mktemp scratch; the lane tree was never edited by this seat.

## Bytes (sha256)

| role | file | sha256 |
|---|---|---|
| pristine subject (lane, before == after all runs) | `corpus/instruments/limb-mutation-check.py` | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` |
| mutant (scratch `/tmp/mutctrtk.tfrxIX/corpus/instruments/limb-mutation-check.py`) | same path in scratch | `8d648a096d6a22d02c4fad11fb71933b40719167f226479023c4475b7e6729cb` |
| ledger (lane, read-only input, before == after) | `corpus/instruments/limb-ledger.json` | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` |

ExecCounterFix (lane-counter owner) confirmed by message that `c660a95f…` is the pre-state
subject for this probe; every counter invocation below used those bytes.

## The one mutation

Scratch setup: `S=$(mktemp -d /tmp/mutctrtk.XXXXXX); cp -a <lane>/corpus "$S/corpus"`
(copy hash-verified identical: `c660a95f…`). Then a single substitution, applied by the
edit tool to the scratch copy only — the mutant-side kill-command-timeout branch of
`evaluate_row` now reports a hang as `killed` instead of `invalid:timeout`:

```diff
--- /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-mutation-check.py
+++ /tmp/mutctrtk.tfrxIX/corpus/instruments/limb-mutation-check.py
@@ -443,7 +443,7 @@
         shutil.rmtree(scratch, ignore_errors=True)
     mutant = measure_side(row, make_scratch, mutated, timeout)
     if mutant["token"] == "timeout":
-        return verdict_row(live_exit, "y", mutant["display"], "n", "invalid:timeout")
+        return verdict_row(live_exit, "y", mutant["display"], "n", "killed")
     if mutant["token"] == "unstable":
         return verdict_row(
             live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "invalid:mutant-baseline"
```

(The live-side and import-gate timeout branches at lines 422/439 were left untouched;
the docstring's "never `killed`" promise at line 39 is what this mutant violates.)

## Commands and output

### 1. Real counter, run A (lane bytes, `--root` = lane; counter writes only its own temp scratch)

```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-mutation-check.py \
  --ledger /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-ledger.json \
  --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

exit=0, stdout 970 B, stderr 0 B:

```
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
```

### 2. Real counter, run B (identical invocation)

exit=0, stdout 970 B. Byte comparison of the two captured stdouts: **identical**
(`realA == realB -> True`). Determinism on landed bytes confirmed; no timeout row
appears in either run (no kill invocation exceeded the frozen 120 s).

### 3. Mutant counter

```
python3 /tmp/mutctrtk.tfrxIX/corpus/instruments/limb-mutation-check.py \
  --ledger /tmp/mutctrtk.tfrxIX/corpus/instruments/limb-ledger.json \
  --root /tmp/mutctrtk.tfrxIX
```

exit=**0**, stdout 970 B, stderr 0 B — the 17 lines printed are **byte-identical to run A**
(`realA == mutant -> True`), including `limbs=13 killed=13 survivors=0`,
`controls=3 rejected=3`, all 13 `LIMB` lines with live-result != mutant-result, and all
three `CONTROL … ok=y` lines.

## Verdict: SURVIVOR (a hole in the counter, on the landed bytes)

Frozen rule (claims.json, `mutants_of_the_counter`): each counter mutant must fail the
3 controls or the LIMB-line clause, i.e. NOT print both target summary lines with exit 0.
The mutant prints both lines with exit 0 and byte-identical output, so no frozen clause
catches it. Cause: none of the 16 ledger rows (13 limbs + CTL-noop/CTL-nocompile/
CTL-equivalent) exercises the timeout path, so a counter that misclassifies a kill-command
timeout as `killed` is indistinguishable from the real counter on these bytes.

The mutant is observable, not equivalent — two proofs:

1. Its own selftest fails on the timeout fixture (exit=1):
   `selftest invalid-timeout        verdict=killed               want=invalid:timeout      FAIL`
   and `selftest cases=20 failures=1`.
2. Demo mini-lane `/tmp/mutctrtk-demo-9vo8uegs` (probe fixture + one limb `hang` whose
   mutant makes every kill invocation `sleep 200`, signal `^probe ok$`, live_exit 0):

   | counter | output | exit |
   |---|---|---|
   | real (`c660a95f…`) | `LIMB hang live=0/y mutant=timeout/n verdict=invalid:timeout` / `limbs=1 killed=0 survivors=0` | 1 |
   | mutant (`8d648a09…`) | `LIMB hang live=0/y mutant=timeout/n verdict=killed` / `limbs=1 killed=1 survivors=0` | **0** |

   A ledger whose only limb provably hangs gets exit 0 from the mutant counter.

## Proposed smallest fix (for ExecCounterFix; not applied by this seat)

No current control is bound to `invalid:timeout`, and `validate_row` rejects an
`expect: "invalid:timeout"` control because `CONTROL_EXPECTS` omits it — so the fix needs
two counter lines plus one ledger row:

1. Counter: add `"invalid:timeout"` to `CONTROL_EXPECTS` and bind `"CTL-timeout":
   "invalid:timeout"` in `CONTROL_ID_EXPECTS` (2-line change; selftest fixture optional).
2. Ledger, append a 4th control (find text verified to occur exactly once in
   recheck-audit.py on landed bytes, `grep -c` = 1; live kill output proven by run A,
   where every RA row ran `--selftest` live=0/y):

```json
{
  "id": "CTL-timeout",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "capture_output=True).returncode == 0",
  "replace": "capture_output=True).returncode == 0  # CTL-timeout marker",
  "kill": "if grep -qF 'CTL-timeout marker' {inst}; then sleep 200; fi; python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest parseonly\\.md .*\\bok$",
  "expect": "invalid:timeout",
  "note": "guards the invalid:timeout gate: a counter that reports a kill-command timeout as killed flips this control to ok=n"
}
```

Under the real counter this control costs one 120 s timeout window per run (the CLI
timeout is frozen at 120 s) and yields `ok=y`; under the timeout-killed mutant it yields
`verdict=killed expected=invalid:timeout ok=n`, exit 1 — mutant killed by the control
clause. Note: landing it changes the frozen summary to `controls=4 rejected=4`, which
needs a claims.json append (frozen claims; corrections land as separate appended files).

## Restoration / lane integrity

- Lane `limb-mutation-check.py` sha256 before the runs and after all runs:
  `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` (unchanged).
- Lane `limb-ledger.json` sha256 unchanged: `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be`.
- Mutated bytes live only in disposable scratch (`/tmp/mutctrtk.tfrxIX`,
  `/tmp/mutctrtk-demo-9vo8uegs`); no git/jj commands were run anywhere.

No tools were installed or upgraded (none needed). No live bounty targets contacted.
Findings are model-independent; answering model per config route table: zai/glm-5.3-flash.
