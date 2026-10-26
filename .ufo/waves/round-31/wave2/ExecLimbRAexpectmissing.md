# ExecLimbRAexpectmissing — falsify ledger limb `RA-expect-missing` (round 31, wave 2)

Seat: ExecLimbRAexpectmissing (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`, wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`).

Files written: this receipt only. The lane is otherwise read-only for this seat; every probe ran in
`mktemp -d` scratch copies, all deleted at seat end (`ls -d /tmp/raem*` shows only captured output
files, no lane copies). No git/jj mutation (read-only `git rev-parse`, `git log --oneline`,
`git status --porcelain`), no delegation, no background job, no network fetch, no credential
material touched, no tool install/upgrade (nothing needed; pacman not invoked).
Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness route decides; this seat
passed no model).

Measured bytes (landed, identical at seat start and at seat end):

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ sha256sum corpus/instruments/recheck-audit.py corpus/instruments/limb-ledger.json corpus/instruments/limb-mutation-check.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
```

No PRE-STATE label needed: wave 1 had landed and was quiescent (instrument mtime `20:34:54`,
ledger `20:42:39`, counter `21:00:20`, all before this seat started at ~21:19), and the three hashes
above are unchanged across every step below. `claims.json` was not edited.

## 0. The row under test (verbatim, `corpus/instruments/limb-ledger.json:75-82`)

```json
{
  "id": "RA-expect-missing",
  "instrument": "corpus/instruments/recheck-audit.py",
  "find": "sorted(wanted - actual)",
  "replace": "[]",
  "kill": "python3 {inst} --selftest",
  "live_exit": 0,
  "signal": "(?m)^selftest expect-missing .*\\bok$",
  "note": "expected-list missing set collapsed to []: a committed entry deleted from the tree no longer reds the audit; isolated by the expect-missing tree fixture (rc must be 1 and missing_entries must name ghost-absent.md)"
}
```

The patched site is `corpus/instruments/recheck-audit.py:194`
(`return sorted(wanted - actual), sorted(actual - wanted)` inside `expected_mismatch`,
defined at `:188`); the consumer is the exit rule at `:390`
(`expect_ok = not expect_active or (not missing_entries and not unexpected_entries)`).

## 1. Hand re-derivation on the landed bytes (no counter code reused)

### 1a. Scratch copy, byte-identity check

```
$ S=$(mktemp -d /tmp/ra-expect-missing.XXXXXX); cp -a corpus "$S/corpus"; rm -rf "$S/corpus/instruments/__pycache__"
$ sha256sum "$S/corpus/instruments/recheck-audit.py" corpus/instruments/recheck-audit.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  /tmp/ra-expect-missing.zJKDuZ/corpus/instruments/recheck-audit.py
5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09  corpus/instruments/recheck-audit.py
```

Find-string cardinality in the lane (read-only, no copy needed):

```
$ python3 -c "t=open('corpus/instruments/recheck-audit.py',encoding='utf-8').read(); print(t.count('sorted(wanted - actual)'))"
1
```

### 1b. UNMUTATED kill command (cwd = scratch lane root, `{inst}` = scratch instrument)

```
$ cd "$S" && PYTHONDONTWRITEBYTECODE=1 bash -c "python3 $S/corpus/instruments/recheck-audit.py --selftest" > /tmp/raem_live.out 2>/tmp/raem_live.err
LIVE_EXIT=0
signal matches (?m)^selftest expect-missing .*\bok$ : y  (exactly 1 matching line)
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
--- stderr
(empty: 0 bytes)
```

Full live stdout tail of the relevant block (from `/tmp/raem_live.out`):

```
good.md                                                    frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
missing=corpus/knowledge/ghost-absent.md
strict pass=1/1 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=1 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
expect=present expected=2 missing=1 unexpected=0 exit=1
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
```

Sanity: the same command run in the lane itself prints byte-identical output (so the kill result is
not a scratch-only artifact):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/recheck-audit.py --selftest
LANE_SELFTEST_EXIT=0   FAIL_lines=0
$ diff /tmp/raem_lane_selftest.out /tmp/raem_live.out && echo lane_vs_scratch_identical=yes
lane_vs_scratch_identical=yes
```

### 1c. Apply the row's find/replace by hand (python, count asserted, then compile)

```
$ python3 - "$I" <<'PY'
...  find='sorted(wanted - actual)'; rep='[]'
PY
find_occurrences=1
BEFORE: return sorted(wanted - actual), sorted(actual - wanted)
AFTER : return [], sorted(actual - wanted)
changed_bytes=True
$ python3 -m py_compile "$I" && echo compile_exit=0
compile_exit=0
```

(`py_compile` left a `__pycache__` in the scratch instrument dir; it was removed before the kill run,
mirroring the counter's `drop_bytecode_cache`.)

### 1d. MUTANT kill command on the same scratch

```
MUTANT_EXIT=1
signal matches : n
(only) FAIL line:  selftest expect-missing  exit=0 want=1 missing=[] unexpected=[] FAIL
--- stderr
(empty: 0 bytes)
```

Hand verdict: **live `0`/`y` → mutant `1`/`n` = killed**, by both exit and signal.

### 1e. Counter line (lane run, scratch-only; run twice, byte-identical)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
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
counter_exit=0   (wall 16.5 s first run, 19.0 s second run)
$ diff /tmp/RAexpectmissing_counter.out /tmp/counter2.out && echo counter_runs_identical=yes
counter_runs_identical=yes
```

**Comparison: hand `live=0/y mutant=1/n verdict=killed` == counter `LIMB RA-expect-missing
live=0/y mutant=1/n verdict=killed`.** No difference → no defect in that line.

Counter writes into the lane: none observed. The lane `recheck-audit.cpython-314.pyc` mtime was
unchanged by a full counter run:

```
$ stat -c '%y' corpus/instruments/__pycache__/recheck-audit.cpython-314.pyc   # before 2nd counter run
2026-10-25 21:20:58.999403671 -0300
$ ... same stat after the run
2026-10-25 21:20:58.999403671 -0300
```

(That `.pyc` was written at 21:20:59, 2.5 s *after* this seat's own mutant run finished at 21:20:56,
by some other concurrent lane seat importing the lane instrument — not by the counter and not by this
seat. Recorded as an observation only; it is not a defect of this limb or of the counter.)

## 2. Discrimination: a SECOND, different one-limb mutant (7 constructed shapes)

Harness: `/tmp/raem_disc.py` — per probe, fresh copy of the LANE `corpus`, one find/replace with the
occurrence count asserted, `py_compile` (cfile outside the tree), then the SAME kill command
`python3 {inst} --selftest` with cwd = scratch root and `PYTHONDONTWRITEBYTECODE=1`. Live reference
is the measured `exit 0` / `signal y` above. `killed` := mutant exit != 0 **or** signal absent.

```
$ python3 /tmp/raem_disc.py
=== D1-inversion (same return site, the two set differences swapped)
find_occurrences=1
py_compile=ok
mutant_exit=1 signal_match=n
expect_missing_line: selftest expect-missing  exit=1 want=1 missing=[] unexpected=['corpus/knowledge/ghost-absent.md'] FAIL
FAIL_lines=2 [... expect-missing ..., ... expect-unexpected ...]
verdict=killed
=== D2-exitrule-conjunct (missing set still computed and reported, but dropped from main()'s exit rule)
find_occurrences=1
py_compile=ok
mutant_exit=1 signal_match=n
expect_missing_line: selftest expect-missing  exit=0 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] FAIL
FAIL_lines=1 [expect-missing]
verdict=killed
=== D3-alt-site-same-semantics (the ledger's semantics at a different site (the return, not the expression))
find_occurrences=1
py_compile=ok
mutant_exit=1 signal_match=n
expect_missing_line: selftest expect-missing  exit=0 want=1 missing=[] unexpected=[] FAIL
FAIL_lines=1 [expect-missing]
verdict=killed
=== D5-no-subtraction (forgets to subtract the tree: every expected name is reported missing)
find_occurrences=1
py_compile=ok
mutant_exit=1 signal_match=n
expect_missing_line: selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md', 'corpus/knowledge/good.md'] unexpected=[] FAIL
FAIL_lines=2 [... expect-missing ..., ... expect-unexpected ...]
verdict=killed
=== D4-name-hardcoded (overfit probe: suppresses only the fixture's literal ghost name)
find_occurrences=1
py_compile=ok
mutant_exit=1 signal_match=n
expect_missing_line: selftest expect-missing  exit=0 want=1 missing=[] unexpected=[] FAIL
FAIL_lines=1 [expect-missing]
verdict=killed
=== D6-order-only (reverses the missing-name order: unobservable while the fixture has ONE missing name)
find_occurrences=1
py_compile=ok
mutant_exit=0 signal_match=y
expect_missing_line: selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
FAIL_lines=0 []
verdict=survivor
=== D7-mixed-tree-conditional (hides missing names only when an unexpected entry is also present: unobservable while no fixture has both)
find_occurrences=1
py_compile=ok
mutant_exit=0 signal_match=y
expect_missing_line: selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
FAIL_lines=0 []
verdict=survivor
```

Probe patches (exact), for reproduction:

| id | site | find | replace |
|---|---|---|---|
| D1 | `:194` | `    return sorted(wanted - actual), sorted(actual - wanted)` | `    return sorted(actual - wanted), sorted(wanted - actual)` |
| D2 | `:390` | `    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)` | `    expect_ok = not expect_active or (not unexpected_entries)` |
| D3 | `:193-194` | `    wanted = set(expected)\n    return sorted(wanted - actual), sorted(actual - wanted)` | `    wanted = set(expected)\n    return [], sorted(actual - wanted)` |
| D5 | `:194` | `sorted(wanted - actual)` | `sorted(wanted)` |
| D4 | `:194` | `sorted(wanted - actual)` | `[n for n in sorted(wanted - actual) if not n.endswith('-absent.md')]` |
| D6 | `:194` | `    return sorted(wanted - actual), sorted(actual - wanted)` | `    return sorted(wanted - actual, reverse=True), sorted(actual - wanted)` |
| D7 | `:194` | `sorted(wanted - actual)` | `(sorted(wanted - actual) if not sorted(actual - wanted) else [])` |

Answer to "does the instrument kill only one specific mutant shape?" — **No: 5 of 7 shapes are
killed, including a name-hardcoded suppression mutant (D4), and the kill is not site-dependent
(D3 relocates the same semantics to a different site and is still killed).** The two survivors are
both blind spots of fixture *shape*, not false kills:

- **D6 (order)** — the expected-list fixture at `recheck-audit.py:256` names exactly **one** absent
  entry, so any permutation of a one-element list is unobservable.
- **D7 (mixed tree)** — the two expected-list fixtures are one-sided by construction
  (`:256` missing only, `:257` unexpected only); no fixture has a deleted **and** an added entry,
  so a mutant that suppresses missing names only when `actual - wanted` is non-empty survives.

Both survivors were also run against real lane bytes (section 4) to see whether the gap is reachable.

## 3. Isolation: is the limb's mutant killed by ITS OWN case, not by collateral damage?

`diff -u` of the unmutated vs mutated selftest stdout (files `/tmp/raem_live.out`,
`/tmp/raem_mut.out`):

```
@@ -13,12 +13,11 @@
 selftest instonly.md   pass want=True  got=True  | strict want=False got=False ok
 selftest completeness lines=13 total=15 complete=False ok
 good.md                                                    frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
-missing=corpus/knowledge/ghost-absent.md
 strict pass=1/1 cdroot_fail=0 instrument_fail=0 own_fail=0
 executes=1 gated=0 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
-lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
-expect=present expected=2 missing=1 unexpected=0 exit=1
-selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
+lines=1 total=1 pass=1 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
+expect=present expected=2 missing=0 unexpected=0 exit=0
+selftest expect-missing  exit=0 want=1 missing=[] unexpected=[] FAIL
 extra.md                                                   frozen=111 strict=111111 lane=0   foreign=0   executes    PASS
```

Exactly 4 output lines differ, all inside the `expect-missing` fixture's own block:

1. `missing=corpus/knowledge/ghost-absent.md` — printed live, **absent** in the mutant.
2. `lines=1 total=1 ... exit=1` → `... exit=0`.
3. `expect=present expected=2 missing=1 unexpected=0 exit=1` → `missing=0 ... exit=0`.
4. `selftest expect-missing ... ok` → `... FAIL`.

The mutant still prints the instrument's normal banner and every other case, and there is no
collateral failure:

```
mutant FAIL lines:                          1   (the expect-missing case only)
mutant lines ending in "ok":               17   (13 per-entry cases + completeness sanity +
                                                expect-unexpected + complete-empty + complete-missing-line)
mutant expect-unexpected: selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
mutant complete-empty / complete-missing-line: both ok
Traceback in mutant stdout+stderr:          0
mutant stderr bytes:                        0
```

So the kill is specific to the limb: `expect-unexpected` (the sibling set difference) and both
`complete*` tree-level fixtures stay green under this mutant, i.e. no unrelated crash and no shared
red is doing the work.

## 4. Does the limb stay load-bearing on real lane bytes? (three audits, same real tree)

Scratch copy of the real `corpus` (44 knowledge entries, real `knowledge-expected.txt`), run with
`--root <scratch> --cdroot /home/vgpnk/Projects/shokunin/kasegi-shokunin` so the real `recheck:`
lines still resolve; the lane is only read.

```
R1 baseline, pristine instrument, full tree
R1_EXIT=0   expect=present expected=44 missing=0 unexpected=0 exit=0
            {'complete': True, 'lines': 44, 'total_knowledge_files': 44}

R2 delete one committed entry (corpus/knowledge/ai-assisted-finding-validation.md), live instrument
R2_EXIT=1   missing=corpus/knowledge/ai-assisted-finding-validation.md
            lines=43 total=43 pass=43 ... exit=1
            expect=present expected=44 missing=1 unexpected=0 exit=1

R3 same deleted-entry tree, LEDGER-mutant instrument
R3_EXIT=0   (no missing= line at all)
            lines=43 total=43 pass=43 ... exit=0
            expect=present expected=44 missing=0 unexpected=0 exit=0

$ diff /tmp/raem_r2.out /tmp/raem_r3.out
44d43
< missing=corpus/knowledge/ai-assisted-finding-validation.md
47,48c46,47
< lines=43 total=43 pass=43 ... exit=1
< expect=present expected=44 missing=1 unexpected=0 exit=1
---
> lines=43 total=43 pass=43 ... exit=0
> expect=present expected=44 missing=0 unexpected=0 exit=0
```

Every one of the 43 surviving entries still passes under the mutant, so the exit flip `1 → 0` is
caused **solely** by the hidden missing set. The fixture's shape (`rc must be 1`, one absent name) is
therefore representative of the real failure, not of a synthetic corner.

Reachability of the two survivors on real bytes — a mixed tree (one entry deleted, one added):

```
R4 live instrument, mixed tree
R4_LIVE_EXIT=1
missing=corpus/knowledge/ai-assisted-finding-validation.md
unexpected=corpus/knowledge/zz-extra.md
expect=present expected=44 missing=1 unexpected=1 exit=1

R4 D7-mutant instrument, identical mixed tree
R4_D7_EXIT=1
unexpected=corpus/knowledge/zz-extra.md
expect=present expected=44 missing=0 unexpected=1 exit=1

$ diff /tmp/raem_r4live.out /tmp/raem_r4d7.out
45d44
< missing=corpus/knowledge/ai-assisted-finding-validation.md
50c49
< expect=present expected=44 missing=1 unexpected=1 exit=1
---
> expect=present expected=44 missing=0 unexpected=1 exit=1
```

D7 does diverge on real bytes, but only in the receipt field: the gate still exits 1 because the
unexpected entry reds it independently. So D7 is receipt-divergent, **gate-equivalent** — it cannot
silently green the audit. D6's divergence is purely cosmetic ordering of a name list. Neither
weakens the frozen row's claim (a deleted committed entry must red the audit).

## 5. Verdict

**`holds`** for the frozen row `RA-expect-missing`.

- Hand trace on the landed bytes (`recheck-audit.py` sha256 `5d4842da…f7f09`): live `exit 0` +
  signal `y`; mutant (`:194` `sorted(wanted - actual)` → `[]`) compiles, runs, `exit 1`, signal `n`
  → killed.
- The counter's `LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed` is **identical** to the
  hand result; the full counter run exits 0 with `limbs=13 killed=13 survivors=0` and
  `controls=3 rejected=3`, reproducible byte-for-byte across two runs.
- Isolation is clean: the mutant's only red is the `expect-missing` case's own block (4 diff lines);
  the other 17 case lines still print `ok`; no traceback, empty stderr; the sibling
  `expect-unexpected` limb stays green.
- The limb is load-bearing on real bytes, not just on the fixture: deleting one committed entry from
  a scratch copy of the real 44-entry tree flips the real audit `1 → 0` under the mutant while all
  43 remaining entries still pass.
- Discrimination: 5 of 7 constructed same-limb mutant shapes killed, including a name-hardcoded
  overfit mutant (D4) and a relocated-site mutant (D3).

**No defect found** in the ledger row, the kill command, the signal, or the counter's line for this
limb. Two non-blocking coverage notes for the L1 to route (both measured, neither affecting the gate):

1. The expected-list fixtures each exercise exactly one missing / one unexpected name
   (`recheck-audit.py:256-257`), so list **ordering** and multi-name aggregation are unpinned
   (D6 survives). A strengthening would be a two-name missing case (e.g. legacy + new entry).
2. No fixture carries a deleted **and** an added entry simultaneously, so a mixed-tree conditional
   mutant survives the selftest (D7). On real bytes it only corrupts the receipt's `missing=`
   accounting — the exit gate stays 1 — so this is a receipt-fidelity gap, not a gate hole.

## 6. Risks

- The kill signal keys on the selftest's print format (`recheck-audit.py:294`). A future reformat of
  that line turns this row into `invalid:live-baseline` (fail-closed, never a silent pass) — safe
  but it would need the ledger's `signal` updated in the same change.
- The signal's `\bok$` tail would also match a hypothetical line ending in `not ok`; no such line
  exists today (measured: exactly 1 match in the live output).
- Concurrent lane seats import the lane instrument (the `21:20:59` `.pyc` above), which pollutes
  `corpus/instruments/__pycache__` in the shared tree. It does not change the instrument bytes
  (hash-stable) and the counter strips `__pycache__` from every scratch copy, so no row is affected;
  worth a lane-level `.gitignore`/cleanup note if the L1 cares about tree cleanliness.
