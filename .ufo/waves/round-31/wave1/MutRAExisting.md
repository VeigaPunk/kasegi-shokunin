# MutRAExisting — mutation probe of the EXISTING selftest of corpus/instruments/recheck-audit.py

Round 31, hyaku 7, lane base b374febbb33ccadade78a787279707fd5d2e6e1d. Seat: MutRAExisting (leaf, no dispatch).
Feeds ExecRALimbs (survivor list delivered via agent message before this receipt).

## Method

- Subject: `corpus/instruments/recheck-audit.py` at lane sha256 `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` (read-only; never edited).
- Each of the 9 limbs got a one-limb mutant: the check deleted (replaced by `True` / one conjunct dropped) in a scratch copy under `/tmp/mutRAexisting-1me78dd9/`. Every find string verified to occur EXACTLY ONCE in the lane bytes before mutation; every mutant `py_compile`-clean (exit 0).
- Detector: `python3 <copy> --selftest` (bash cwd = scratch dir). Verdict: `killed` iff mutant exit != baseline exit OR selftest stdout lines change; else `survivor`. Baseline exit 0, 29 stdout lines (reproduced below); baseline passing makes every verdict below conclusive.
- Restoration evidence: lane file sha256 before runs `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`, after runs identical → lane untouched. Scratch copies are disposable (/tmp), mutants left in place there; no lane path was ever written by this seat except this receipt.

## Verdict table

| limb | mutant (find → replace, all count==1 in lane bytes) | verdict | proving line |
|---|---|---|---|
| RA-parse | `limbs["parse"] = parse_ok(line)` → `limbs["parse"] = True` | killed (exit 0→1) | `selftest parseonly.md  pass want=False got=True  | strict want=False got=True  FAIL` |
| RA-cwd | `limbs["cwd"] = lane_rc == foreign_rc and lane_digest == foreign_digest` → `limbs["cwd"] = True` | killed (exit 0→1) | `selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL` |
| RA-paths | `limbs["paths"] = named and not missing` → `limbs["paths"] = True` | killed (exit 0→1) | `selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL` |
| RA-cdroot | `strict["cdroot"] = True if cd_target is None else os.path.abspath(cd_target) == (cdroot or root)` → `strict["cdroot"] = True` | killed (exit 0→1) | `selftest elsewhere.md  pass want=True  got=True  | strict want=False got=True  FAIL` |
| RA-instrument | `strict["instrument"] = bool(instruments) or base_test` → `strict["instrument"] = True` | killed (exit 0→1) | `selftest instonly.md   pass want=True  got=True  | strict want=False got=True  FAIL` (ownonly.md flips too) |
| RA-own | `strict["own"] = own or sourced or base_state` → `strict["own"] = True` | killed (exit 0→1) | `selftest selftesty.md  pass want=True  got=True  | strict want=False got=True  FAIL` (basetest.md flips too) |
| RA-completeness | main(): `complete = len(entries) == total and total > 0` (+`\n    expect_ok` context) → `complete = True` | **survivor** (exit 0, stdout byte-identical, unified diff empty) | absence: no `selftest` line changes; only mutant sha256 differs |
| RA-expect-missing | `expect_ok = not expect_active or (not missing_entries and not unexpected_entries)` → drop `not missing_entries and` | killed (exit 0→1) | `selftest expect-missing  exit=0 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] FAIL` |
| RA-expect-unexpected | same find → `expect_ok = not expect_active or (not missing_entries)` | killed (exit 0→1) | `selftest expect-unexpected exit=0 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] FAIL` |

Tally: limbs=9 killed=8 survivors=1 inconclusive=0.

## Survivor analysis: RA-completeness

- Mutated site verified to be main()'s production rule (`complete = True` at 4-space indent inside `def main()`; the selftest's own oracle line `complete = len(entries) == total and total > 0 and all(...)` — 8-space indent, in `selftest()` — was left intact and still evaluates False in the fixture).
- Why nothing fires: the `selftest completeness lines=13 total=15 complete=False ok` fixture recomputes completeness locally over `collect()` output and asserts its own recomputation — it never calls `main()` on the missing-line tree, so the production `ok = passed == len(entries) and complete and strict_passed == total and expect_ok` rule is unexercised. The two expected-list fixtures DO call `main()` but reach rc=1 via `expect_ok`, masking a falsified `complete`.
- Coverage finding for ExecRALimbs (per C1 contract, strengthening is the owning executor's work): a fixture that runs `main(["--root", <tree with one .md lacking a recheck line>, "--cdroot", tree])` and requires rc==1 would kill this mutant and only this mutant.

## Commands and outputs

Command pattern (per copy): `python3 /tmp/mutRAexisting-1me78dd9/<copy>.py --selftest`

Baseline (pristine copy, exit 0):

```
selftest good.md       pass want=True  got=True  | strict want=True  got=True  ok
selftest prose.md      pass want=False got=False | strict want=False got=False ok
selftest cwd.md        pass want=False got=False | strict want=False got=False ok
selftest ghost.md      pass want=False got=False | strict want=False got=False ok
selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
selftest sourced.md    pass want=True  got=True  | strict want=True  got=True  ok
selftest basetest.md   pass want=True  got=True  | strict want=False got=False ok
selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
selftest completeness lines=13 total=15 complete=False ok
good.md                                                    frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
missing=corpus/knowledge/ghost-absent.md
strict pass=1/1 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=1 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=2 missing=1 unexpected=0 exit=1
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
extra.md                                                   frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
good.md                                                    frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
unexpected=corpus/knowledge/extra.md
strict pass=2/2 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=2 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=2 total=2 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=1 missing=0 unexpected=1 exit=1
selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
```

Mutant unified diffs (exit code after each header; `RA-completeness` diff is empty = byte-identical stdout):

RA-parse (exit 1):
```diff
--- baseline --selftest
+++ RA-parse --selftest
@@ -11,3 +11,3 @@
 selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
-selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
+selftest parseonly.md  pass want=False got=True  | strict want=False got=True  FAIL
 selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
```

RA-cwd (exit 1):
```diff
--- baseline --selftest
+++ RA-cwd --selftest
@@ -2,3 +2,3 @@
 selftest prose.md      pass want=False got=False | strict want=False got=False ok
-selftest cwd.md        pass want=False got=False | strict want=False got=False ok
+selftest cwd.md        pass want=False got=True  | strict want=False got=True  FAIL
 selftest ghost.md      pass want=False got=False | strict want=False got=False ok
```

RA-paths (exit 1):
```diff
--- baseline --selftest
+++ RA-paths --selftest
@@ -3,3 +3,3 @@
 selftest cwd.md        pass want=False got=False | strict want=False got=False ok
-selftest ghost.md      pass want=False got=False | strict want=False got=False ok
+selftest ghost.md      pass want=False got=True  | strict want=False got=False FAIL
 selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
```

RA-cdroot (exit 1):
```diff
--- baseline --selftest
+++ RA-cdroot --selftest
@@ -5,3 +5,3 @@
 selftest degenerate.md pass want=True  got=True  | strict want=False got=False ok
-selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
+selftest elsewhere.md  pass want=True  got=True  | strict want=False got=True  FAIL
 selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
```

RA-instrument (exit 1):
```diff
--- baseline --selftest
+++ RA-instrument --selftest
@@ -6,3 +6,3 @@
 selftest elsewhere.md  pass want=True  got=True  | strict want=False got=False ok
-selftest ownonly.md    pass want=True  got=True  | strict want=False got=True  FAIL
 selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
@@ -12,3 +12,3 @@
 selftest parseonly.md  pass want=False got=False | strict want=False got=False ok
-selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
+selftest instonly.md   pass want=True  got=True  | strict want=False got=True  FAIL
 selftest completeness lines=13 total=15 complete=False ok
```

RA-own (exit 1):
```diff
--- baseline --selftest
+++ RA-own --selftest
@@ -7,5 +7,5 @@
 selftest ownonly.md    pass want=True  got=True  | strict want=False got=False ok
-selftest selftesty.md  pass want=True  got=True  | strict want=False got=False ok
+selftest selftesty.md  pass want=True  got=True  | strict want=False got=True  FAIL
 selftest sourced.md    pass want=True  got=True  | strict want=True  got=True  ok
-selftest basetest.md   pass want=True  got=True  | strict want=False got=False ok
+selftest basetest.md   pass want=True  got=True  | strict want=False got=True  FAIL
 selftest basestate.md  pass want=True  got=True  | strict want=True  got=True  ok
```

RA-completeness (exit 0 — survivor, no output change):
```diff
--- baseline --selftest
+++ RA-completeness --selftest
```

RA-expect-missing (exit 1):
```diff
--- baseline --selftest
+++ RA-expect-missing --selftest
@@ -18,5 +18,5 @@
 executes=1 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
-lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
-expect=present expected=2 missing=1 unexpected=0 exit=1
-selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
+lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
+expect=present expected=2 missing=1 unexpected=0 exit=0
+selftest expect-missing  exit=0 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] FAIL
 extra.md                                                   frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
```

RA-expect-unexpected (exit 1):
```diff
--- baseline --selftest
+++ RA-expect-unexpected --selftest
@@ -26,4 +26,4 @@
 executes=2 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
-lines=2 total=2 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
-expect=present expected=1 missing=0 unexpected=1 exit=1
-selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
+lines=2 total=2 pass=2 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
+expect=present expected=1 missing=0 unexpected=1 exit=0
+selftest expect-unexpected exit=0 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] FAIL
```

## Hashes

- Lane `corpus/instruments/recheck-audit.py` (pristine, before AND after all runs — restoration evidence): `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`
- Mutant copies (sha256):
  - RA-parse `938ede31f90d6e39f3881c0b24b7799e80fe974aa4f82222852afaa7ae1e6fce`
  - RA-cwd `e9328df09f71617913f427df19d25a8111426ea00e3f775ca85f3bacc413d99a`
  - RA-paths `ce8fb000b067338b3dc8e899348dce5da3293ebb2287dc6cdd341ea8a3563b41`
  - RA-cdroot `6f7cfe5341d057a26ac08547b9ef85cc09055f41812c00cd27c1a65fd402bd5f`
  - RA-instrument `a4369ca1923759d8605bf0a28851217fa48844cca075b35a95a50fb27710e652`
  - RA-own `c7f9e8323b12537bf75dca6d6fb00ed40bdef1bd07b030daefab5f0aa962621f`
  - RA-completeness `048388299391bbde573db8e01f5774fcfe75facfcb65fd59aaab0d9d7bc9f17a`
  - RA-expect-missing `6288d91a7d2a2065959e59b4da1a3386e6b9c68fc36ad6ac98bc2e2948272908`
  - RA-expect-unexpected `a3bbb1575ec4fd20d35f9b4b5d1fe7ea6cbb623616812e96262be91ee2426a48`

## find-count intel for the ledger rows (verified against lane bytes, count==1 unless noted)

Unique: `limbs["parse"] = parse_ok(line)`, `limbs["cwd"] = lane_rc == foreign_rc and lane_digest == foreign_digest`, `limbs["paths"] = named and not missing`, `strict["cdroot"] = True if cd_target is None else os.path.abspath(cd_target) == (cdroot or root)`, `strict["instrument"] = bool(instruments) or base_test`, `strict["own"] = own or sourced or base_state`, `expect_ok = not expect_active or (not missing_entries and not unexpected_entries)`.
NOT unique alone: `complete = len(entries) == total and total > 0` occurs twice (selftest oracle contains it as a prefix, 8-space indent + ` and all(...)` tail); a ledger row for RA-completeness needs continuation context (e.g. `...total > 0\n    expect_ok`) to satisfy find-count==1.

No git/jj commands were run in the lane; no lane bytes other than this receipt were written.
