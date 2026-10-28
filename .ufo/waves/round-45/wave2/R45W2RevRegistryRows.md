VERDICT: BROKEN

Scope: registry accuracy of the six rows of `## Round-45 Gates & probes registry addition` (SKILL.md:1146-1155) and the four round-45 rows of corpus/instruments/README.md (lines 994-997), against the integration tree = `git archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4` (export), plus `git archive c950fa3` and `git archive dc5bb8c` (round base) as controls. Every printed line below was produced by a run I performed in this seat. Nothing was committed or mutated; no tool was installed (none needed).

## Cell-level result

| SKILL row (line) | verdict | what does not match |
|---|---|---|
| r44-frontier-count.py (1150) | HOLDS, minor gap | "exit 0 clean" omits that a tree with no corpus/README.md exits 0 (see F5) |
| r44-routed-defects.py (1151) | BROKEN (F1, F6) | selftest cell is false at the integration tree and at the round base |
| wave-registry.py (1152) | HOLDS | — |
| freeze-check.py (1153) | BROKEN (F4) | "fixtures under --work or TMPDIR" is false for selftest case 2 |
| r45-routed-defects.py (1154) | BROKEN (F2) | self-test file named by the row does not exist; `--selftest` rejected |
| r45-c2-gate.py (1155) | BROKEN (F3) | self-test file named by the row does not exist; `--selftest` rejected |

The four README rows (994-997) are cell-for-cell identical to SKILL rows 1150, 1153, 1154, 1155 (checked with a python cell diff: 8 cells each, zero differences), so every finding below applies to both copies.

## Findings

### F1 — BROKEN: SKILL.md:1151 selftest cell "prints `selftest cases=20 failures=0`" is true only at c950fa3
Command (export = 6662a42):
```
python3 corpus/instruments/r44-routed-defects.py --root <export> --selftest --work <dir>
```
Output, exit 1:
```
selftest case=POSITIVE verdict=fail fixed=7 unresolved=1
...
selftest cases=20 failures=1
```
Same command on `base` (dc5bb8c): `selftest case=POSITIVE verdict=fail fixed=7 unresolved=1` / `selftest cases=20 failures=1`, rc=1.
Same command on `c950` (c950fa3 archive): `selftest cases=20 failures=0`, rc=0, 20 `selftest case=` lines.
So the row's selftest cell is correct only for the c950fa3 root; the row names no root for that cell, and its own "measured revision is c950fa3" sentence is the only place that qualifies it. At the integration tree the self-test exits 1. The receipt `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` (line 2 `# tip export c950fa3`, line 24 `selftest cases=20 failures=0`) pins the c950fa3 run, which I reproduced.

### F2 — BROKEN: SKILL.md:1154 and README.md:996 (r45-routed-defects) name a self-test file that is not in the lane commit
Row: "run `corpus/instruments/r45-counters-selftest-c1.py` with --selftest".
```
$ python3 corpus/instruments/r45-counters-selftest-c1.py --selftest
python3: can't open file '.../export/corpus/instruments/r45-counters-selftest-c1.py': [Errno 2] No such file or directory
rc=2
```
`git ls-tree -r --name-only 6662a42 | grep r45-counters-selftest` returns only the two wave1 draft paths `.ufo/waves/round-45/wave1/R45ExecSelftestC{1,2}.draft/r45-counters-selftest-c{1,2}.py`. These are unlanded drafts. Their real CLI (`--help`) is `[--lane LANE] [--base BASE] [--counter COUNTER] [--only ONLY] [--keep]`, and `--selftest` is rejected: `error: unrecognized arguments: --selftest`, rc=2. Also note the counter itself, `r45-routed-defects.py`, printed the 5 `limb R<n>` lines and `routed-defects total=5 fixed=5 unresolved=0 exit=0` against export with `--baseline base`, so the counter line format matches; only the self-test cell is wrong.

### F3 — BROKEN: SKILL.md:1155 and README.md:997 (r45-c2-gate) name a self-test file that is not in the lane commit
Row: "run `corpus/instruments/r45-counters-selftest-c2.py` with --selftest".
The file is absent from the export (same `ls-tree` check). The draft's CLI is `[--lane LANE] [--counter COUNTER] [--do-nothing-control] [--keep]`; `--selftest` → `error: unrecognized arguments: --selftest`, rc=2.

### F4 — BROKEN: SKILL.md:1153 and README.md:995 (freeze-check): "fixtures under --work or TMPDIR" is false for case 2
Export run: `freeze-check.py --selftest --work <dir>` → rc=0, `selftest cases=20 failures=0`, and case 2 prints `... frozen grep read 0 (readme /fast/scratch/hyaku/kasegi-r45/L1/pure/corpus/README.md)`.
Source: `corpus/instruments/freeze-check.py:47` `PURE_DEFAULT = "/fast/scratch/hyaku/kasegi-r45/L1/pure"`; `locate_readme` (lines 184-200) falls back only to that path or to `git show dc5bb8c:corpus/README.md` from the script's repo or cwd.
Control: I copied the script into a scratch tree with `PURE_DEFAULT = "/nonexistent/L1/pure"` and ran it from a non-git cwd:
```
case 2-round44-frozen-grep-real-readme FAIL real base README not found
...
rc=1
```
The unmodified script from the same cwd printed `selftest cases=20 failures=0`, rc=0. So the row's "failures=0" depends on an external L1 scratch path (or a git checkout containing dc5bb8c), not on --work/TMPDIR fixtures as the write-scope cell says. The claimed "(includes the round-44 frozen C2 grep that read 0)" is true: `claim C base_read=0 verdict=FAIL`.

### F5 — MINOR: SKILL.md:1150 and README.md:994 (r44-frontier-count) exit map omits the missing-README case
"exit 0 clean" is the only exit-0 description. Measured: a tree with no corpus/README.md, no --expect:
```
r44-frontier-count: cannot read .../tmp/emptyfc/corpus/README.md: [Errno 2] ...
frontier rows=0 admitted=0
rc=0
```
and with `--expect 27`: `frontier expected=27 admitted=0 verdict=SHORT exit=1`, rc=1. The selftest pins this (`missing-readme-is-zero-rows`), so it is intended, but a do-nothing tree passes the default invocation. Relatedly the script docstring (r44-frontier-count.py:19-20) says "at the frozen base the same count is 25"; measured at dc5bb8c and c950fa3 it is `frontier rows=26 admitted=26` — the registry row's own "base reads rows=26 admitted=26" is correct.

### F6 — MINOR: SKILL.md:1151 `--work DIR` must already exist
`--work $S/tmp/does-not-exist` → `FileNotFoundError: ... r44-routed-defects-4z7q6z53`, rc=1 (run_selftest uses `tempfile.mkdtemp(dir=work_root)` without creating it). The row does not say the directory must pre-exist.

## Confirmed (HOLDS)

- r44-frontier-count (1150): export `frontier rows=27 admitted=27` rc=0 (`--expect 27` passes, `--ids` lists F01-F27); base dc5bb8c `frontier rows=26 admitted=26` rc=0, and `--expect 27` on base → `frontier expected=27 admitted=26 verdict=SHORT exit=1` rc=1; `--root corpus/README.md` → rc=2. Selftest: `mutants=10 rejected=10`, `selftest cases=43 failures=0`, rc=0 (also with the default temp dir). 43 = 18 CLI + 15 in-memory + 10 mutants, consistent with the row.
- r44-routed-defects (1151), counter output: c950fa3 → `routed-defects total=8 fixed=8 unresolved=0 exit=0`, rc=0; export → `... fixed=7 unresolved=1 exit=1`, rc=1, with `R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping`; base → identical to export. Mechanism verified: `r44-routed-defects.py:404` takes `log.rfind("## Round 44")`; in the export that is attempt 3 (`LOG.md:1994`), whose section has no `planner=L1`; in c950fa3 it is attempt 2 (`LOG.md:1977`), which has it at line 1980. "Attempt 3 appended a later ## Round 44 section" is accurate. Not a directory → rc=2. Do-nothing: empty tree → `routed-defects total=8 fixed=0 unresolved=8 exit=1`, rc=1.
- wave-registry.py (1152): `wave-registry: wrote ... seats=64 names=64 attack=32`, rc=0; output diffed byte-identical to `.ufo/waves/round-45/wave-registry.txt` (SAME45) and the round-44 invocation with seats=66 is byte-identical to `.ufo/waves/round-44/wave-registry.txt` (SAME44). Disagreement (wave1-results.json with `"seats": 63`): `wave-registry: seats=63 but 64 named seats — refusing to emit`, rc=1, no output file. Unreadable file → `cannot read ...`, rc=2. `--selftest` → argparse usage error, rc=2 (row is correct).
- freeze-check (1153): `.ufo/waves/round-45/claims.json` sha256 = `bbe40503...c6206` = `claims-sha256` in freeze.txt; base-commit claims (8cf62c8) hash identical. Export replay: `claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok`, `claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok`, `freeze-check claims=2 base_ok=2 exit=0`, rc=0. All ten FC-* ids named by the row appear in the source (grep counts 3-8 each). `--tool-root base` → `FC-NO-MATCH`, `freeze-check claims=2 base_ok=0 exit=1`, rc=1 (the counters do not exist at base; discriminates). Selftest with the L1 path present: `selftest cases=20 failures=0`.
- r45-routed-defects (1154) output: export vs base → `limb R1..R5 fixed=1` and `routed-defects total=5 fixed=5 unresolved=0 exit=0`, rc=0; base-as-root, c950fa3-as-root and empty tree → `routed-defects total=5 fixed=0 unresolved=5 exit=1`, rc=1 (do-nothing control, discriminates); not-dir → rc=2.
- r45-c2-gate (1155) output: export → `gate G1..G7 pass=1` then `c2-gate fixed=7/7 exit=0`, rc=0; base and c950fa3 → `c2-gate fixed=1/7 exit=1`, rc=1; empty tree → `fixed=0/7 exit=1`, rc=1; not-dir → rc=2. Pinned manifest `corpus/source-snapshots/round-45/manifest.json` exists.

## Limitations

- Not verified: R1-R5 / G1-G7 predicate content (only the registry cells); the r45 drafts' self-test internals were not run (they are unlanded; I ran only `--help` and a rejected `--selftest` call).
- The "undeclared nonzero -> could-not-evaluate" mappings were not exercised (no fault injection beyond missing files, non-directories and the argparse path).
- freeze-check selftest was tested with a modified copy (PURE_DEFAULT changed) in scratch; I did not test a git-checkout fallback run from inside the lane repo.
- README rows for r44-routed-defects (992) and wave-registry (993) are round-44 rows and outside the four round-45 rows; not checked for cell accuracy beyond the D4/selftest runs above.
- Trees were exported with `git archive` (read-only); the lane working tree was not read.
