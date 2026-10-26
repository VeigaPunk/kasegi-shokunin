# wave2/MutCtrSignalIgnored — counter mutant: ignore the `signal` regex (killed only by exit-code difference)

Date: 2026-10-25. Round 31, hyaku run 7. Lane base b374febbb33ccadade78a787279707fd5d2e6e1d; claims-frozen 738a77999a00efbca129cfccb28a481037f6241f.
Seat scope: one mutation probe of `corpus/instruments/limb-mutation-check.py`. All work ran in scratch under `/tmp/mutctrsig-MutCtrSignalIgnored` (outside the lane and the fleet root); the lane tree was never edited; no git/jj commands; no tool installs (nothing to record under operator 2026-10-19); no pacman; no model calls (bound 10 n/a).

## Subject bytes (before)

```
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  kasegi-shokunin/corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  kasegi-shokunin/corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  /tmp/mutctrsig-MutCtrSignalIgnored/counter-mutant.py   (cp -a of lane counter, pre-mutation)
```

Scratch corpus: `cp -a <lane>/corpus /tmp/mutctrsig-MutCtrSignalIgnored/corpus` (3.4M). Ledger for the mutant run: the scratch copy `corpus/instruments/limb-ledger.json`, root passed via `--root`.

## The mutation (one behavior-bearing point)

Line 451 of the counter — the kill decision in `evaluate_row` — applied to the scratch copy only:

```diff
--- kasegi-shokunin/corpus/instruments/limb-mutation-check.py
+++ /tmp/mutctrsig-MutCtrSignalIgnored/counter-mutant.py
@@ -448,7 +448,7 @@
         return verdict_row(
             live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "invalid:mutant-baseline"
         )
-    killed = mutant["exit"] != row["live_exit"] or not mutant["signal"]
+    killed = mutant["exit"] != row["live_exit"]
     return verdict_row(
         live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "killed" if killed else "survivor"
     )
```

Live-baseline signal gate (lines 425-426), compile/import gates, display fields, and controls logic all left intact — only the signal clause of the kill decision is dropped. Mutant sha256 `9ba4dda95d97cdfb6c65081b47a7052aae0b57bfcb4806e2e2fec6d824a3f27b`.

## Detector runs

### 1. Pristine, run 1 (canonical C1 command, lane bytes)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
```

exit=0, stderr 0 B, real 21.7 s. Full stdout:

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

### 2. Pristine, run 2 (byte-identical check)

Same command. exit=0, stderr 0 B.

```
$ cmp real-1.out real-2.out && echo cmp=identical
cmp=identical
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  real-1.out
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  real-2.out
```

Real counter output is byte-identical across the two runs.

### 3. Mutant counter

```
$ cd /tmp/mutctrsig-MutCtrSignalIgnored && python3 counter-mutant.py --ledger corpus/instruments/limb-ledger.json --root /tmp/mutctrsig-MutCtrSignalIgnored
```

exit=1, stderr 0 B, real 20.4 s. Full stdout:

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
LIMB FR-missing-entry live=1/y mutant=1/n verdict=survivor
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=12 survivors=1
controls=3 rejected=3
```

### 4. Output diff, pristine vs mutant

```diff
--- real-1.out
+++ mutant.out
@@ -9,10 +9,10 @@
 LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
 LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
 LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
-LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
+LIMB FR-missing-entry live=1/y mutant=1/n verdict=survivor
 LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
 CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
 CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
 CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
-limbs=13 killed=13 survivors=0
+limbs=13 killed=12 survivors=1
 controls=3 rejected=3
```

### 5. Restored bytes

```
$ cp -f <lane>/corpus/instruments/limb-mutation-check.py counter-mutant.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  counter-mutant.py   (== pristine)
$ python3 counter-mutant.py --ledger corpus/instruments/limb-ledger.json --root /tmp/mutctrsig-MutCtrSignalIgnored
restored_exit=0
$ cmp real-1.out restored.out && echo restored_cmp=identical
restored_cmp=identical
9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838  restored.out
```

Lane hashes after the whole probe: counter `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f`, ledger `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` — both unchanged from "before"; the lane was never written.

## Verdict: KILLED

- Clause: claims.json C1 `mutants_of_the_counter` — "each counter mutant must fail the 3 controls or the LIMB-line clause, i.e. NOT print both summary lines with exit 0". This mutant passes all three controls (`controls=3 rejected=3`, every `ok=y`) but fails the LIMB-line clause: it prints `limbs=13 killed=12 survivors=1` instead of `limbs=13 killed=13 survivors=0` and exits 1. Under the C1 kill_rule this is simultaneously "its output lacks the exact lines `limbs=13 killed=13 survivors=0` …" and "the counter … exits non-zero".
- Tripwire limb: `FR-missing-entry` — the only ledger limb whose mutant keeps the live exit (mutant exit 1 == live_exit 1) and is killed solely by the signal clause. Ledger note (corpus/instruments/limb-ledger.json, limb FR-missing-entry): "raises FileNotFoundError on the absent entry (traceback, still exit 1), so the kill is by signal". Real counter line `live=1/y mutant=1/n verdict=killed` becomes `live=1/y mutant=1/n verdict=survivor` under the mutant counter.
- Relation to the frozen counter-mutant classes: this probe is the signal-only half of "count-by-exit-code-only" (compile/import gates left intact), and it is still caught — by the LIMB-line clause, without needing the controls clause (the wider compile-dropping variant would additionally flip `CTL-nocompile` to `invalid:import` and fail `rejected=3`).
- No hole found. No extra control or ledger row proposed; ExecCounterFix not messaged (required only on survival).

## PRE-STATE / quiescence note

Wave 1 is landed and quiescent; all four detector runs used the same bytes, and the lane counter/ledger hashes are identical before and after the probe, so no in-flight sibling edit intervened (bound 6). No PRE-STATE labeling needed.

## Cleanup

`/tmp/mutctrsig-MutCtrSignalIgnored` (scratch lane, counter copies, run outputs) removed after this receipt was written. Nothing was written outside this receipt and /tmp.
