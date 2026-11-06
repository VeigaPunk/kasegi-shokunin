# MutC1Hunt - round-80 C1 mutant hunt (attempt 1, wave 1, seat MutC1Hunt)

Scope: single transforms of the frozen r80 C1 candidate that are **outside** the frozen
28-row table (`mutant-table.json` sha256 `08d7f3ce...e418`), applied one literal
replacement at a time to an exact scratch copy, then run as
`TMPDIR=$S/t python3 -B <mutant> --selftest`. Every row is a single transform; anchors
occur exactly once in the frozen bytes (71/71 derived, 0 NOT-DERIVED).

Frozen candidate: `.ufo/waves/round-80/c1/recheck-cwd-census.py`
sha256 `420151fdea1187aa308f63536216039746fc9d784f6096c36627b7513e505698`.
Baseline: rc=0, `selftest cases=15 failures=0`; same sha256 after every run
(`BASELINE rc=0 ok=True`, `FROZEN_AFTER 420151fd...5698`).

Detector (frozen-counter-shaped, mutbat.py semantics): rc 0 = SURVIVED; rc != 0 with a
`selftest case=... FAIL` line and no Traceback = KILLED; traceback or no FAIL = DIRTY;
`exception=` FAIL detail = EXCEPTION-KILL. A baseline failure would be inconclusive; none
occurred. For every SURVIVED row an R128 normalized-output diff against the baseline was
computed (scratch paths normalized), plus a crafted probe run against pristine and mutant.

## Totals

| rows | killed | survived | dirty | not-derived | survivors real-gap | survivors equivalent |
|---|---|---|---|---|---|---|
| 71 | 29 | 42 | 0 | 0 | 36 | 6 |

No exact `(anchor, replacement)` pair collides with the frozen 28-row table. Two rows
share an anchor with a frozen row but use a different mechanism: H08 (same anchor as N21,
folds `exit_other` into `exit2_foreign` rather than `exit1_foreign`) and S27 (same anchor
as K-N1, rewrites `wiring_ok` as truthiness rather than to a constant).

R128: 41 of the 42 survivors produce selftest output identical to the baseline after
normalization; only S33 differs (0 stdout chars). Survival is therefore not output noise -
the frozen selftest is silent on all 36 real-gap behaviours below. Survivors are routed
findings for round 81; **no frozen verdict changes** and no frozen byte is edited.

## Rows

| id | transform | verdict | rc | class | probe / killing evidence |
|---|---|---|---|---|---|
| H01 | noprefix operator flip | KILLED | 1 | detector | FAIL prefix-census, result-main, first-line, restoration-only, both-headers, relabel-detection, gate-negpolarity, gate-checkids |
| H02 | restoration_only counted into norecheck | KILLED | 1 | detector | FAIL restoration-only, relabel-detection, gate-checkids |
| H03 | exit2 branch constant changed | KILLED | 1 | detector | FAIL prefix-census, first-line |
| H04 | exit0 branch constant changed | KILLED | 1 | detector | FAIL prefix-census, restoration-only, both-headers, relabel-detection, gate-checkids |
| H05 | exit1 branch constant changed | KILLED | 1 | detector | FAIL prefix-census |
| H06 | entries counter neutered | KILLED | 1 | detector | FAIL prefix-census, first-line, restoration-only, both-headers, relabel-detection, gate-checkids |
| H07 | noprefix counter neutered | KILLED | 1 | detector | FAIL prefix-census, first-line |
| H08 | exit_other bucket folded into exit2 | KILLED | 1 | detector | FAIL prefix-census |
| H09 | entry TMPDIR set to parent, not fresh scratch | KILLED | 1 | detector | FAIL prefix-census |
| H10 | timeout constant collapsed | KILLED | 1 | detector | FAIL prefix-census, first-line, both-headers |
| H11 | run_foreign scratch cleanup removed | KILLED | 1 | detector | FAIL scratch-cleanup |
| H12 | refusal line moved off stderr | KILLED | 1 | detector | FAIL tmpdir-refusal |
| H13 | tmpdir_refused returns False after printing | KILLED | 1 | detector | FAIL tmpdir-refusal |
| H14 | conform drops restoration_only conjunct | KILLED | 1 | detector | FAIL gate-consume |
| H15 | nonconformant exit code changed to 2 | KILLED | 1 | detector | FAIL result-main, gate-consume |
| H16 | predicates_ok drops bool(rows) | KILLED | 1 | detector | FAIL gate-predicates |
| H17 | checkids side-log test weakened to != [False] | KILLED | 1 | detector | FAIL gate-predicates |
| H18 | GATE_ROWS constant off by one | KILLED | 1 | detector | FAIL gate-predicates |
| H19 | first_recheck reads last recheck line | KILLED | 1 | detector | FAIL first-line |
| H20 | wiring scanner arity bound raised | KILLED | 1 | detector | FAIL gate-predicates, gate-wiring, gate-checkids |
| H21 | F4 finding dropped | KILLED | 1 | detector | FAIL gate-predicates |
| H22 | F3 findings dropped | KILLED | 1 | detector | FAIL gate-predicates |
| H23 | negpolarity predicate rewritten as truthiness (None row) | KILLED | 1 | detector | FAIL gate-predicates |
| H24 | main TMPDIR guard deleted | KILLED | 1 | detector | FAIL tmpdir-refusal |
| H25 | F3 emitted for wired names too | KILLED | 1 | detector | FAIL gate-predicates, gate-wiring, gate-checkids |
| H26 | fixture literal e-exit7 changed to exit 1 | KILLED | 1 | detector | FAIL prefix-census |
| H27 | fresh-cwd fixture neutralised to true | SURVIVED | 0 | real gap | `true` in place of the fresh-cwd fixture keeps every bucket count; composed probe: pristine+cwd-inheritance FAILs prefix-census (rc1) while H27+cwd-inheritance passes (rc0) - the fixture's strength is unasserted |
| H28 | run_foreign cwd swapped to the TMPDIR parent | KILLED | 1 | detector | FAIL prefix-census |
| S01 | prefix literal loses the && anchor | SURVIVED | 0 | real gap | entry `cd <lane>NONSENSE && true` counted prefixed; main ret 1->0 |
| S02 | prefix literal loses its trailing space | SURVIVED | 0 | real gap | entry `cd <lane> &&false` counted prefixed (noprefix 1->0) |
| S03 | glob enumeration no longer sorted | SURVIVED | 0 | real gap | ENTRY order follows readdir (a,b,c -> c,a,b); output determinism unpinned |
| S04 | conform drops exit2_foreign conjunct | SURVIVED | 0 | real gap | census whose only defect is a foreign exit 2 becomes conformant (ret 1->0) |
| S05 | conform drops norecheck conjunct | SURVIVED | 0 | real gap | census whose only defect is a no-header entry becomes conformant (ret 1->0) |
| S06 | DEFAULT_LANE points at fleet root | SURVIVED | 0 | real gap | with only --root the default lane is the fleet root: conformant fixture ret 0->1; DEFAULT_LANE unexercised |
| S07 | verbose defaults to True | SURVIVED | 0 | real gap | ENTRY lines appear without --verbose (0->1) |
| S08 | gate_consume_ok identity test becomes equality | SURVIVED | 0 | real gap | gate_consume_ok(1,[True]) false->true (bool/int identity edge untested) |
| S09 | limb_log test truncated to its first element | SURVIVED | 0 | real gap | gate_consume_ok(True,[True,False]) false->true (extra log entries accepted) |
| S10 | both_headers rest_ran test becomes falsiness | SURVIVED | 0 | real gap | both_headers_ok(True,True,0) false->true (falsiness replaces `is False`) |
| S11 | predicates_ok element equality coerced to truthiness | SURVIVED | 0 | real gap | predicates_ok([('a','b')],1) false->true (elements compared by truthiness) |
| S12 | predicates_ok row count becomes a lower bound | SURVIVED | 0 | real gap | predicates_ok with 2 rows against expect=1 false->true (row count is a lower bound) |
| S13 | side log membership test instead of exact log | SURVIVED | 0 | real gap | gate_checkids_ok(['a'],['a'],[[False,True]]) false->true (membership, not exact log) |
| S14 | F1 BoolOp limb deleted | SURVIVED | 0 | real gap | check("gate-consume", True and gate_consume_ok(x)): pristine F1, mutant silent; no BoolOp fixture |
| S15 | F4 narrowed to constant True arguments | SURVIVED | 0 | real gap | gate_consume_ok(0, log): pristine F4, mutant silent; F4 narrowed to Constant True |
| S16 | F1 BoolOp operand quantifier any->all | SURVIVED | 0 | real gap | check("x", False or True): pristine F1, mutant silent; operand quantifier not pinned |
| S17 | both-headers dropped from GATE_PREDICATES | KILLED | 1 | detector | FAIL gate-predicates |
| S18 | consumed() arity guard removed | SURVIVED | 0 | real gap | check("gate-consume", consumed(x)): pristine F2, mutant raises IndexError; arity guard untested |
| S19 | RESTORATION-ONLY marker print deleted | SURVIVED | 0 | real gap | RESTORATION-ONLY line vanishes while counts stay right; marker text unpinned |
| S20 | NORECHECK marker print deleted | SURVIVED | 0 | real gap | NORECHECK line vanishes; marker text unpinned |
| S21 | ENTRY detail line suppressed | SURVIVED | 0 | real gap | every ENTRY line vanishes; detail output unpinned |
| S22 | ENTRY predicate drops code == 2 | SURVIVED | 0 | real gap | prefixed exit-2 entry loses its ENTRY line; `code == 2` clause unpinned |
| S23 | first_recheck accepts indented header | SURVIVED | 0 | equivalent | indented header is contract-invalid (header must start the line); probe differs only on `   recheck:`, whose value is also mis-sliced; no corpus-valid entry changes |
| S24 | selftest fixture scratch cleanup removed | SURVIVED | 0 | real gap | selftest leaves a recheck-cwd-selftest-* dir under TMPDIR (leftover>0) |
| S25 | tmpdir_refused drops the None guard | SURVIVED | 0 | real gap | TMPDIR unset: pristine rc0, mutant TypeError traceback (None guard untested) |
| S26 | first_recheck value no longer stripped | KILLED | 1 | detector | FAIL prefix-census, result-main, restoration-only, both-headers, relabel-detection, gate-negpolarity, gate-checkids |
| S27 | wiring_ok rewritten as truthiness | SURVIVED | 0 | equivalent | `not xs` == (`xs == []`) for every list; probe identical on [], [x], [x,y]; every call site passes a list [probe identical] |
| S28 | conform noprefix test becomes <= 0 | SURVIVED | 0 | equivalent | noprefix is a non-negative counter, so `== 0` == `<= 0`; probe identical on conformant, noprefix-only and norecheck-only censuses [probe identical] |
| S29 | summary line format changed | SURVIVED | 0 | real gap | summary line reworded (`entries=%d` -> `entries = %d`); format unpinned |
| S30 | usage error exit code returns 0 | SURVIVED | 0 | real gap | unknown argument exits 0 instead of 2 (usage path untested) |
| S31 | missing corpus guard prints instead of exiting | SURVIVED | 0 | real gap | empty root: pristine raises SystemExit, mutant prints conformant and exits 0; missing-corpus guard untested |
| S32 | scratch-cleanup leftover fixed at 0 | SURVIVED | 0 | real gap | scratch-cleanup limb is constant: composed probe (mutant + cleanup removed) rc0/scratch ok while (pristine + cleanup removed) rc1 |
| S33 | capture() no longer restores stdout | SURVIVED | 0 | real gap | capture() stops restoring stdout: selftest exits 0 with 0 stdout chars; the summary line is unasserted |
| S34 | selftest TMPDIR guard deleted | SURVIVED | 0 | equivalent | shipped path: main() guards TMPDIR before selftest() is reachable, so `--selftest` with a bad TMPDIR exits 2 in both; probe differs only through a direct in-process selftest() call (inner guard redundant) |
| S35 | recheck values run under sh, not bash | SURVIVED | 0 | equivalent | /bin/sh -> /usr/bin/bash 5.3.20 on this host; probe counts identical and the selftest passes, so no observable difference for bash/sh-common values here (portability-only risk on dash hosts) [probe identical] |
| S36 | gate-wiring read-failure fallback neutered | SURVIVED | 0 | real gap | unreadable own source: pristine gate-wiring FAIL rc1, mutant rc0 (F0 fallback untested) |
| S37 | restoration header prefix broadened | SURVIVED | 0 | real gap | `restoration-note:` counted restoration_only (exact-header test unexercised) |
| S39 | main passes root where lane belongs | SURVIVED | 0 | real gap | --lane distinct from --root is ignored: conformant fixture ret 0->1 (argument never varied) |
| S40 | neg_ret_ok identity test becomes equality | SURVIVED | 0 | real gap | gate_negpolarity_ok(False,0) false->true (int identity edge) |
| S41 | both_headers first_ran identity test becomes equality | SURVIVED | 0 | real gap | both_headers_ok(True,1,False) false->true (int identity edge) |
| S42 | non-string check label no longer skipped | SURVIVED | 0 | equivalent | valid candidate source has string-literal labels; difference only for `check(42, ...)`, an invalid call |
| S43 | predicate matching becomes case-insensitive | SURVIVED | 0 | real gap | GATE_CONSUME_OK accepted as the predicate: pristine F2, mutant silent (case-insensitive matching) |
| S38 | tmpdir-parent drops the None-parent limb | SURVIVED | 0 | real gap | TMPDIR unset: pristine rc0, mutant tmpdir-parent FAIL rc1 (None-parent limb untested) |

Killed-row failing-case lists are the selftest's own FAIL lines from `logs/<id>.out`.
Survivor probes are re-runnable: `probes.json` holds the full pristine/mutant observations,
`survivors/<id>.py` holds each surviving mutant source, and `logs/<id>.out` holds its run.

## Routed findings for round 81 (survivors, by theme)

1. **Product path / census core** - S01, S02 (prefix literal accepts `cd <lane>NONSENSE`
   and `cd <lane> &&false`); S03 (unsorted glob changes stdout order); S04, S05 (conform
   drops the `exit2_foreign` / `norecheck` conjuncts, so those are not required for
   `RECHECK-CWD-RESULT conformant`); S06 (DEFAULT_LANE); S07 (verbose default); S37
   (restoration header prefix broadened); S29 (summary format); S30 (usage exit 0); S31
   (missing-corpus guard); S39 (main passes `root` where `lane` belongs).
2. **Unasserted output lines** - S19, S20, S21, S22 (RESTORATION-ONLY / NORECHECK /
   ENTRY lines can vanish entirely); S33 (capture() can silence the whole selftest summary
   while rc stays 0).
3. **Predicate edge inputs** - S08, S09, S10, S11, S12, S13, S40, S41: bool/int identity
   (`is` -> `==`), truncated limb logs, truthiness coercion, `>=` row counts, log membership
   instead of exact logs. Every probe input is a value the predicate's documented contract
   rejects and the mutant accepts.
4. **Gate-wiring scanner limbs** - S14 (F1 BoolOp limb), S15 (F4 non-True constants),
   S16 (BoolOp `any` -> `all`), S18 (`consumed()` arity -> crash), S36 (F0 unreadable-source
   fallback), S43 (case-insensitive predicate match).
5. **Environment / harness self-protection** - H27 (fixture neutralisation undetected;
   composed with cwd inheritance it survives where pristine fails); S24 (selftest scratch
   dir leaks); S25, S38 (TMPDIR-unset paths: crash / tmpdir-parent FAIL); S32
   (scratch-cleanup `leftover` limb constant).

## Equivalent survivors (not routed as gaps)

| id | why equivalent |
|---|---|
| S23 | indented header is contract-invalid (header must start the line); probe differs only on `   recheck:`, whose value is also mis-sliced; no corpus-valid entry changes |
| S27 | `not xs` == (`xs == []`) for every list; probe identical on [], [x], [x,y]; every call site passes a list |
| S28 | noprefix is a non-negative counter, so `== 0` == `<= 0`; probe identical on conformant, noprefix-only and norecheck-only censuses |
| S34 | shipped path: main() guards TMPDIR before selftest() is reachable, so `--selftest` with a bad TMPDIR exits 2 in both; probe differs only through a direct in-process selftest() call (inner guard redundant) |
| S35 | /bin/sh -> /usr/bin/bash 5.3.20 on this host; probe counts identical and the selftest passes, so no observable difference for bash/sh-common values here (portability-only risk on dash hosts) |
| S42 | valid candidate source has string-literal labels; difference only for `check(42, ...)`, an invalid call |

## Restoration evidence

Frozen bytes hashed before and after the hunt (`frozen-before.txt` / `frozen-after.txt`):
candidate `420151fd...5698`, counter `b47276d1...d450`, table `08d7f3ce...e418`, builder
`e0a8c714...e0ef3`, manifest `85cd2f26...ba1`, snapshot S114 `e1ccfb9b...88d2`, claims
`c9343d81...5204`; the ten control files are listed with their hashes. Both hash lists are
identical; no frozen byte, no instrument, no lane file outside this wave directory was
written. No git/jj mutation was issued; no tool was installed. Scratch root
`/fast/scratch/hyaku/kasegi-r80/MutC1Hunt` was deleted after outputs were copied here.

## Reproduce

```
S=/fast/scratch/hyaku/kasegi-r80/MutC1Hunt; mkdir -p $S/t
TMPDIR=$S/t python3 -B driver.py        # 71 rows, ~12 s
```
`driver.py` is copied beside this report; output dirs `logs/`, `survivors/`, `results.json`,
`probes.json`, `baseline.out`.
