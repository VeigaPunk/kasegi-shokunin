VERDICT: DRAFT-READY

Seat R45ExecFreezeA, C1/R4 builder A. Draft: `.ufo/waves/round-45/wave1/R45ExecFreezeA.draft/freeze-check.py` (stdlib only, ~480 lines, python 3.14.8). NOT installed into corpus/instruments (L1 does). No tool installed. No git mutation. Scratch `$HYAKU_SCRATCH/kasegi-r45/R45ExecFreezeA` removed by trap.

## Behavior
`--claims PATH --tool-root DIR --base DIR [--work DIR] [--timeout S=300]` / `--selftest [--work DIR]`.
Per claim: renders `counter_cmd` ({tool}->tool-root, {tree} and {base}->base; str.replace so awk braces survive), runs it via /bin/sh in tool-root, stdout+stderr merged, own process group killed on timeout, child env `R45_FREEZE_CHECK=1`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR inherited. Passes only if: id + counter_cmd + expect_before + expect_after present non-empty; some output line EQUALS expect_before as a whole line (whitespace-trimmed; R41); no output line equals expect_after. Counter exit code is ignored. Finding codes (printed as `finding <id> <code> <detail>` after the claim line): bad-claims-file, bad-schema, no-claims, missing-field, multiline-expect, spawn-error, timeout, before-mismatch, after-at-base. Zero claims -> exit 1.

## Finding 1 — selftest (command run, output printed)
`python3 <draft>/freeze-check.py --selftest --work $S/w`
```
case PASS: 1 good claim, red counter exit 1 [as expected]
case PASS: 2 round-44 frozen string prints 0, expect_before 26 -> FAIL [as expected]
case PASS: 2b table-aware string prints 26 -> ok (tool is not fail-always) [as expected]
case PASS: 3 do-nothing green (prints expect_after at base) -> FAIL [as expected]
case PASS: 3b before line present AND after line present -> FAIL after-at-base only [as expected]
case PASS: 4 claims missing expect_before/expect_after/counter_cmd/id/blank -> FAIL [as expected]
case PASS: 5 crash / command-not-found / absent counter, no matching line -> FAIL [as expected]
case PASS: 6 token only as substring (fixed=0x, xfixed=0, mid-line, closed=7/80) -> FAIL [as expected]
case PASS: 7 counter exceeding --timeout 2 -> FAIL timeout [as expected]
case PASS: 8 child env R45_FREEZE_CHECK=1, TMPDIR passthrough, cwd=tool-root, tree=base [as expected]
case PASS: 9 mixed good+bad claim -> exit 1, base_ok=1 [as expected]
case PASS: 10a empty claims list -> FAIL no-claims [as expected]
case PASS: 10b wrong schema -> FAIL bad-schema [as expected]
case PASS: 10c unreadable JSON -> FAIL bad-claims-file [as expected]
case PASS: 10d multi-line expect_before -> FAIL multiline-expect [as expected]
selftest cases=15 failures=0
```
rc=0. Every case drives the real CLI as a subprocess and asserts exit code, summary counts (`claims= base_ok= exit=`), claim verdict and a stable finding id (case 3b also asserts `before-mismatch` is absent; case 2 asserts `after-at-base` absent and `base_read=0`).

Case 2 note: the real base README (`/fast/scratch/hyaku/kasegi-r45/L1/pure/corpus/README.md`) holds 26 admitted rows, not 25 (25 was the round-44 base; `grep -c '^| F.* | admitted |'` -> 26). expect_before is therefore computed from the copied file (26); the frozen round-44 string prints `0` against it -> `before-mismatch`. Case 2b runs a table-aware regex (`^\| F[0-9]+ \| [^|]* \| admitted \|`) on the same file: prints 26 -> ok, proving the tool is not fail-always.

## Finding 2 — real claims replay (command run, output printed)
`python3 <draft>/freeze-check.py --claims /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-45/claims.json --tool-root /home/vgpnk/Projects/shokunin/kasegi-shokunin --base /fast/scratch/hyaku/kasegi-r45/L1/pure`
```
claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok
claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok
freeze-check claims=2 base_ok=2 exit=0
```
rc=0 (base_ok=2 as required).

## Finding 3 — do-nothing / mutation controls (re-run by me)
- Swapped control: same real claims file with expect_before/expect_after swapped, same command -> rc=1:
```
claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=FAIL
finding C1 before-mismatch no output line equals expect_before 'routed-defects total=5 fixed=5 unresolved=0 exit=0'; exit=1
finding C1 after-at-base base already prints expect_after 'routed-defects total=5 fixed=0 unresolved=5 exit=1'
claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=FAIL
...
freeze-check claims=2 base_ok=0 exit=1
```
- Mutants of the tool run through its own selftest (the selftest must catch each):
  - m1 (`want in line` substring match): `selftest cases=15 failures=2` (cases 6, 9 FAIL).
  - m2 (after-at-base disabled): `selftest cases=15 failures=2` (cases 3, 3b FAIL).
  - m3 (before-mismatch disabled): `selftest cases=15 failures=4` (cases 2, 5, 6, 9 FAIL).
  So cases 2/3/5/6/9 each discriminate a distinct defect; none passes on a do-nothing tool.

## Limitations
- Matching is whole-line equality after trimming; a counter that prints its token inside a longer line (e.g. a prefix) needs `expect_before` to be that full line (by design, R41).
- `counter_cmd` without `{tree}` (the round-44 frozen shape) is run against tool-root cwd, not base; the tool does not warn (only the value mismatch surfaces). Not made a failure because the spec's pass rule does not list it.
- `secondary` and `control` claim fields are not executed.
- Case 2 needs a README source: `$R45_PURE_README`, else the pure export path, else `<script>/../README.md`; if none exists the case FAILs (never skips).
- Timeout case uses `--timeout 2` (extra optional flag; default 300 s as specified); the 300 s default itself was not exercised.
- Counters run via `/bin/sh -c`; commands are trusted claims-file input, as in the freeze.
