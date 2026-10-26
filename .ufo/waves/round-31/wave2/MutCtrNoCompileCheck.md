# MutCtrNoCompileCheck — counter mutant probe: drop the py_compile gate

Round kasegi-shokunin r31, wave 2 (falsify wave; wave 1 quiescent). Judged axes: depth:verifiability, coverage.
Target: `corpus/instruments/limb-mutation-check.py` (lane bytes untouched; all attack work in an mktemp scratch copy).
Assigned mutation (ONE): delete the `py_compile` gate in `evaluate_row`, so a non-compiling mutant is no longer stopped as `invalid:nocompile`.
Environment: Python 3.14.8, Arch linux x64. No tools installed or upgraded (nothing needed; pacman untouched per orchestrator pause).
Quiescence: `git status --porcelain` on the two subject files was empty before and after the probe (bound 6 satisfied; no PRE-STATE labels needed).

## 1. Pristine state

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin status --porcelain -- corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json
(empty)
$ sha256sum <lane>/corpus/instruments/limb-mutation-check.py <lane>/corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  limb-ledger.json
```

Scratch lane: `S=$(mktemp -d /tmp/mutctr.XXXXXXXXXX)` → `/tmp/mutctr.1wlI2KNcP4`; `cp -a <lane>/corpus $S/corpus` (10 files under `corpus/instruments/limb-fixtures/`).

## 2. Real counter, twice — baseline and byte-identity

```
$ python3 $S/corpus/instruments/limb-mutation-check.py --ledger $S/corpus/instruments/limb-ledger.json --root $S
real1_exit=0 ; real2_exit=0
STDOUT_BYTE_IDENTICAL ; STDERR_BYTE_IDENTICAL   # cmp real1 vs real2, both streams; 970 bytes
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

13 `LIMB ` lines, each live-result != mutant-result; both target summary lines; exit 0. Wall time ~38 s per run.

## 3. The mutant (scratch copy only)

```
$ diff -u <lane>/corpus/instruments/limb-mutation-check.py $S/corpus/instruments/limb-mutation-check.py
--- <lane>/corpus/instruments/limb-mutation-check.py
+++ $S/corpus/instruments/limb-mutation-check.py
@@ -432,8 +432,6 @@
             return verdict_row(live_exit, "y", "-", "-", "invalid:noop")
         write_bytes(instrument_path, mutated)
         drop_bytecode_cache(instrument_path)
-        if not compiles(instrument_path, scratch):
-            return verdict_row(live_exit, "y", "-", "-", "invalid:nocompile")
         imported = import_verdict(instrument_path, scratch, timeout)
         if imported == "timeout":
             return verdict_row(live_exit, "y", "-", "-", "invalid:timeout")
```

That is the entire mutation: the `compiles()` gate inside `evaluate_row` (counter lines 435-436) is deleted; everything else byte-identical.

## 4. Mutant run — full output and exit

```
$ python3 $S/corpus/instruments/limb-mutation-check.py --ledger $S/corpus/instruments/limb-ledger.json --root $S
mutant_exit=1
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
CONTROL CTL-nocompile verdict=invalid:import expected=invalid:nocompile ok=n
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=2
```

`$ diff -u $S/real1.txt $S/mutant.txt` shows exactly two changed lines:

```
-CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
+CONTROL CTL-nocompile verdict=invalid:import expected=invalid:nocompile ok=n
-controls=3 rejected=3
+controls=3 rejected=2
```

All 13 LIMB lines are byte-identical to the real run (every ledger limb mutant still compiles, so the dropped gate never fires for them).

## 5. Verdict: KILLED

Frozen rule (claims.json C1, `mutants_of_the_counter`): each counter mutant must "fail the 3 controls or the LIMB-line clause, i.e. NOT print both `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3` with exit 0."

- The mutant prints `limbs=13 killed=13 survivors=0` but `controls=3 rejected=2` and exits 1.
- **Clause violated: the 3-controls clause.** `CTL-nocompile` (ledger controls[1], expect `invalid:nocompile`) is no longer rejected — its verdict flips to `invalid:import` — so `rejected=2 != controls=3`, the exact line `controls=3 rejected=3` is absent, and the counter exits 1 instead of 0. Any closure diffing the counter command's output or exit rejects the mutant.
- LIMB-line clause unaffected and intact (13/13 killed, live != mutant on every line).

Honest-scope note: dropping `py_compile` alone does NOT make a non-compiling mutant count as killed — the counter's import gate (docstring lines 332-349) independently intercepts the syntax-broken `CTL-nocompile` patch as `invalid:import` (`exec_module` raises, non-zero exit, no sentinel). What the mutation actually destroys is the verdict taxonomy: `invalid:nocompile` becomes unreachable, so "does not compile" and "raises at import" become indistinguishable — exactly the distinction `CTL-nocompile` is bound to. No kill inflation occurred, the defense-in-depth held, so this is not a survivor: no extra control/ledger row is proposed and ExecCounterFix needs no fix. (A counter mutant that dropped BOTH the compile gate and the import gate would mislabel `CTL-nocompile` as killed; outside this seat's assigned single mutation, recorded as observation only.)

Supplementary probe (not the frozen rule, same single mutant): the mutant's own `--selftest` fails exactly one internal fixture —

```
$ python3 $S/corpus/instruments/limb-mutation-check.py --selftest
mutant_selftest_exit=1
selftest invalid-nocompile      verdict=invalid:import       want=invalid:nocompile    FAIL
```

— so the counter's internal fixture layer independently detects the same mutation (1 FAIL, exit 1), while the frozen kill is carried by the CTL-nocompile control on the ledger run.

## 6. Restoration evidence

- Lane `limb-mutation-check.py` sha256 after probe: `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` — identical to before.
- Lane `limb-ledger.json` sha256 after probe: `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` — identical to before.
- The only edited bytes were `/tmp/mutctr.1wlI2KNcP4/corpus/instruments/limb-mutation-check.py`, a disposable mktemp scratch copy (tasking: all attack work in mktemp scratch); scratch deleted after this receipt.
- No git/jj mutation was run anywhere; no writes outside the scratch and this receipt; no contact with /home/vgpnk/Projects/shokuknow; no live bounty targets contacted.

## 7. Commands as run (verbatim; $S = /tmp/mutctr.1wlI2KNcP4, ephemeral)

```
S=$(mktemp -d /tmp/mutctr.XXXXXXXXXX) && cp -a /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus "$S/corpus"
python3 "$S/corpus/instruments/limb-mutation-check.py" --ledger "$S/corpus/instruments/limb-ledger.json" --root "$S"   # x2, byte-identical
# edit tool: delete the two compiles()-gate lines in "$S/corpus/instruments/limb-mutation-check.py"
diff -u /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-mutation-check.py "$S/corpus/instruments/limb-mutation-check.py"
python3 "$S/corpus/instruments/limb-mutation-check.py" --ledger "$S/corpus/instruments/limb-ledger.json" --root "$S"   # mutant run
diff -u "$S/real1.txt" "$S/mutant.txt"
python3 "$S/corpus/instruments/limb-mutation-check.py" --selftest
sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-mutation-check.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/limb-ledger.json
```
