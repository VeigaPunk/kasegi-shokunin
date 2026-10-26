# Wave 2 receipt — MutCtrAlwaysKilled (counter mutant attack: always-killed)

- Seat: MutCtrAlwaysKilled, round 31 wave 2 (falsify wave), lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only for this seat; all attack work in mktemp scratch).
- Frozen rule under test: `.ufo/waves/round-31/claims.json` C1 `mutants_of_the_counter`: "always-killed (skip the mutant run)" must fail "the 3 controls or the LIMB-line clause", i.e. must NOT print both `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3` with exit 0.
- Model note: probe is deterministic shell/Python work; no model-routed step, none recorded per bound 10.
- Tooling: no tools installed or upgraded (bound 5: nothing needed; no pacman).

## 1. Scratch setup

```sh
LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
D=$(mktemp -d /tmp/mutctr-XXXXXX)          # -> /tmp/mutctr-Kprhoj
mkdir -p "$D/lane"
cp -a "$LANE/corpus" "$D/lane/corpus"      # corpus tree (incl. limb-fixtures the kill commands use)
cp "$LANE/corpus/instruments/limb-ledger.json" "$D/ledger.json"
cp "$LANE/corpus/instruments/limb-mutation-check.py" "$D/counter-pristine.py"
cp "$LANE/corpus/instruments/limb-mutation-check.py" "$D/counter-mutant.py"
```

Lane hashes BEFORE (sha256):

```
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```

Scratch copies hashed identical to the lane files before mutation. Ledger copy has no `copy` extras key, so the counter's own `build_scratch` needs only `corpus/`, which the scratch lane provides; every kill command's `{root}` resolves inside the scratch.

## 2. The mutant (always-killed: skip the mutant run, report killed for every valid row)

`diff -u "$D/counter-pristine.py" "$D/counter-mutant.py"` (both hunks inside `evaluate_row`; the pre-mutant gates — live baseline, find-count, noop, compile, import — are untouched, so `invalid:*` verdicts still fire):

```diff
--- /tmp/mutctr-Kprhoj/counter-pristine.py	2026-10-25 21:27:50.557940276 -0300
+++ /tmp/mutctr-Kprhoj/counter-mutant.py	2026-10-25 21:28:01.684408156 -0300
@@ -441,7 +441,7 @@
             return verdict_row(live_exit, "y", "-", "-", "invalid:import")
     finally:
         shutil.rmtree(scratch, ignore_errors=True)
-    mutant = measure_side(row, make_scratch, mutated, timeout)
+    mutant = {"token": "ok", "exit": row["live_exit"], "display": str(row["live_exit"]), "signal": True}  # MutCtrAlwaysKilled: mutant run skipped
     if mutant["token"] == "timeout":
         return verdict_row(live_exit, "y", mutant["display"], "n", "invalid:timeout")
     if mutant["token"] == "unstable":
@@ -450,7 +450,7 @@
         )
     killed = mutant["exit"] != row["live_exit"] or not mutant["signal"]
     return verdict_row(
-        live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "killed" if killed else "survivor"
+        live_exit, "y", mutant["display"], yes_no(mutant["signal"]), "killed"  # MutCtrAlwaysKilled: always report killed
     )
```

`python3 -m py_compile` of the mutant: `MUTANT_COMPILES`. Mutant sha256 `575b36b785ce7faf13477c56ae2b49e9cd1623704d75b4484b38ad3ee9b7b01f`. The fabricated mutant side mimics the live result (`display = str(row["live_exit"])`, `signal: True`), i.e. the maximally deceptive shape — no obviously impossible mutant column.

## 3. Mutant counter run

`python3 "$D/counter-mutant.py" --ledger "$D/ledger.json" --root "$D/lane"` — full output, `mutant_exit=1`:

```
LIMB RA-parse live=0/y mutant=0/y verdict=killed
LIMB RA-cwd live=0/y mutant=0/y verdict=killed
LIMB RA-paths live=0/y mutant=0/y verdict=killed
LIMB RA-cdroot live=0/y mutant=0/y verdict=killed
LIMB RA-instrument live=0/y mutant=0/y verdict=killed
LIMB RA-own live=0/y mutant=0/y verdict=killed
LIMB RA-completeness live=0/y mutant=0/y verdict=killed
LIMB RA-expect-missing live=0/y mutant=0/y verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=0/y verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=1/y verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=1/y verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/y verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=1/y verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=killed expected=survivor ok=n
limbs=13 killed=13 survivors=0
controls=3 rejected=2
```

## 4. Real counter, run twice

`python3 "$D/counter-pristine.py" --ledger "$D/ledger.json" --root "$D/lane"` — run 1 exit `real1_exit=0`, full output:

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

Run 2: `real2_exit=0`. `diff real-1.txt real-2.txt` empty → `REAL_RUNS_BYTE_IDENTICAL`; both sha256 `9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`. The real counter on the scratch lane reproduces the frozen C1 predicate (`limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`, exit 0), so the harness baseline was live, not PRE-STATE.

## 5. Verdict: KILLED

The mutant's output differs from the real run and is caught by the frozen C1 kill rule on two independent clauses:

1. **Controls clause (the designed catch, and the one that does not depend on my fabrication choice):** `CONTROL CTL-equivalent verdict=killed expected=survivor ok=n`. The expected-survivor control passes every pre-mutant gate (find occurs exactly once, bytes differ, compiles, imports) and therefore reaches the skipped mutant run, where the always-killed mutant stamps `killed`. `rejected` drops 3 -> 2, so the required line `controls=3 rejected=3` is never printed (`controls=3 rejected=2` instead) and `aggregate` returns not-ok -> `mutant_exit=1`. Kill rule tripped: "exits non-zero" + "lacks the exact line `controls=3 rejected=3`" (claims.json C1 `kill_rule`). CTL-noop and CTL-nocompile still reject because their `invalid:noop` / `invalid:nocompile` gates run before the skipped mutant side.
2. **LIMB-line clause (also tripped):** with the fabricated mutant column equal to the live column, all 13 LIMB lines show live-result == mutant-result (`live=0/y mutant=0/y`, `live=1/y mutant=1/y`); kill rule: "any LIMB line shows live-result == mutant-result".

Not a survivor: no hole in the counter, no extra control or ledger row proposed, nothing messaged to ExecCounterFix. The mutant never executes a single limb's kill command against a mutated instrument (13x2 mutant-side runs skipped), yet the ledger's expected-survivor control alone forces a wrong summary and exit 1.

## 6. Restoration / cleanup evidence

- Lane files AFTER (sha256, identical to §1):

```
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
```

- `git -C <lane> status --porcelain -- corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json`: empty (read-only invocation only).
- No lane tree write at any point: mutation, runs, and outputs all under `/tmp/mutctr-Kprhoj` (lane untouched, hashes prove it). Scratch declared disposable by wave scope; removed after receipt:

```sh
rm -rf /tmp/mutctr-Kprhoj
```
