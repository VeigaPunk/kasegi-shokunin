VERDICT: BROKEN

Scope: corpus/instruments/freeze-check.py at lane commit 6662a4276b6f7bd61e23e12058414e09dd71b9e4 (round base dc5bb8c6e31efc4a6650819df85e79b72fd64bcd). Attacked the `git archive | tar -x` export only. Mutation target: its own `--selftest` (20 cases). Claim under test: the selftest is a discriminating check on the freeze gate's branches.

## Control (do-nothing)

Command:
  TMPDIR=<scratch>/work python3 <export>/corpus/instruments/freeze-check.py --selftest --work <scratch>/work --base <export>
Output (tail): `selftest cases=20 failures=0`, rc=0, ~1.1 s. sha256 of unmutated file a38d8dc1319ff0bdab1bc557643b192cf201312fe0f7d681e430c40817305888.

## Mutation result: 12 single-line edits, 5 survivors

Each mutant is a copy of the export with exactly one line changed (`diff` confirmed 2 lines of output = one `NNNc NNN` hunk each). Selftest run per mutant, TMPDIR explicit.

| Mutant | Line (export) | Edit | Selftest | Verdict |
|---|---|---|---|---|
| M03 | 167 | `any(ea in ln ...)` -> `any(ln == ea ...)` | failures=0 | SURVIVED |
| M05 | 62 | `(st.st_size, st.st_mtime_ns)` -> `(st.st_size,)` | failures=0 | SURVIVED |
| M06 | 57 | dir snapshot line -> `pass` | failures=0 | SURVIVED |
| M10 | 81 | `os.killpg(p.pid, signal.SIGKILL)` -> `p.kill()` | failures=0 | SURVIVED |
| M11 | 146 | `"{tree}" not in cmd and "{base}" not in cmd` -> `"{tree}" not in cmd` | failures=0 | SURVIVED |
| M01 | 164 | `ln == eb` -> `eb in ln` | failures=2 | killed by 6, 6b |
| M02 | 164 | `ln == eb` -> `ln.startswith(eb)` | failures=1 | killed by 6 |
| M04 | 167 | `if ea is not None and any(` -> `if False and any(` | failures=3 | killed by 3, 3b, 7 |
| M07 | 158 | `if before_snap != after_snap:` -> `if False:` | failures=1 | killed by 12 |
| M08 | 165 | `if matched is None and not timed_out:` -> `if matched is None:` | failures=1 | killed by 8 (got `FC-NO-MATCH, FC-TIMEOUT`) |
| M09 | 156 | `if timed_out:` -> `if False:` | failures=1 | killed by 8 (got `[]`) |
| M12 | 134 | `if cid in seen:` -> `if False:` | failures=1 | killed by 9 |

## Survivors (first)

### S1 M03: expect_after check weakened from substring to whole-line equality (line 167)
- Attacked: `if ea is not None and any(ea in ln for ln in stripped):` -> `any(ln == ea for ln in stripped)`.
- Selftest: `selftest cases=20 failures=0`, rc=0. Cases 3, 3b and 7 all put the after-value as a whole output line, so equality still fires there.
- Should be caught by a new case 3c: `cmd = echo 'T fixed=1 exit=0 (base)'; echo 'T fixed=0 exit=1'; : {tree}`, eb `T fixed=0 exit=1`, ea `T fixed=1 exit=0`, want `FC-AFTER-AT-BASE`.
- Probe (`python3 probe/probe.py <module> p1_after_substring`):
  - control: `finding C FC-AFTER-AT-BASE counter output already contains expect_after 'T fixed=1 exit=0'` / `claims=1 base_ok=0 exit=1`
  - M03: `claims=1 base_ok=1 exit=0`
- Why it matters: a counter that prints the green value with a trailing annotation at the base is the do-nothing-green case the check exists for; M03 passes it.

### S2 M05: base snapshot ignores mtime_ns (line 62)
- Attacked: `snap[...] = (st.st_size, st.st_mtime_ns)` -> `(st.st_size,)`.
- Selftest: passes. Case 12 only creates a new file (set difference catches it); no case touches or rewrites an existing file.
- Should be caught by a new case 12b: `cmd = touch -d '2000-01-01' {tree}/marker.txt; echo 'T fixed=0 exit=1'`, want `FC-BASE-MUTATED`.
- Probe p2:
  - control: `finding C FC-BASE-MUTATED counter changed the base tree: marker.txt` / `claims=1 exit=1`
  - M05: `claims=1 base_ok=1 exit=0`
- Why it matters: the docstring (lines 25-26) promises "relative path + size + mtime_ns"; the mtime half is untested.

### S3 M06: directories are not tracked in the base snapshot (line 57)
- Attacked: `snap[os.path.relpath(p, base) + "/"] = None` -> `pass`.
- Selftest: passes. Case 12 touches a file, never a directory.
- Should be caught by a new case 12c: `cmd = mkdir {tree}/newdir; echo 'T fixed=0 exit=1'`, want `FC-BASE-MUTATED`.
- Probe p3 (fixture reset before each run):
  - control: `finding C FC-BASE-MUTATED counter changed the base tree: newdir/` / `claims=1 exit=1`
  - M06: `claims=1 base_ok=1 exit=0`

### S4 M11: `{base}`-only counter_cmd is wrongly rejected (line 146)
- Attacked: `"{tree}" not in cmd and "{base}" not in cmd` -> `"{tree}" not in cmd`. The docstring (line 24) says "counter_cmd mentions {tree} or {base}", so the `{base}` alternative is contract.
- Selftest: passes. Every selftest counter uses `{tree}`; no case uses only `{base}`.
- Should be caught by a new positive case 4e: `cmd = echo 'T fixed=0 exit=1'; : {base}`, eb `T fixed=0 exit=1`, ea `T fixed=1 exit=0`, want exit 0, no findings.
- Probe p5:
  - control: `claims=1 exit=0` (base_ok=1)
  - M11: `finding C FC-NO-TREE counter_cmd reads neither {tree} nor {base}` / `claims=1 exit=1`

### S5 M10: process-group kill replaced by single-process kill (line 81)
- Attacked: `os.killpg(p.pid, signal.SIGKILL)` -> `p.kill()`.
- Selftest: passes, and wall time is the same as control (1083 ms vs 1082 ms). Case 8 runs `sleep 30`; `bash -c` execs the single command, so `p.kill()` reaches it. The group kill is never exercised.
- Probe p4 (`: {tree}; sleep 20`, timeout 1 s; `sleep` is a forked grandchild holding the stdout pipe):
  - control: `wall_s=1.0`, `finding C FC-TIMEOUT counter exceeded 1 s`
  - M10: `wall_s=20.0`, same finding
- Limitation: the selftest is output-only, so this survivor can be killed only by adding a case with an elapsed-time bound (e.g. under 10 s). I did not add one; the probe demonstrates the gap but the selftest still lacks an assertion for it.

## Killed mutants: what each proves
- M01 and M02 show the whole-line match is pinned by case 6 (`fixed=0x`) and 6b (`xfixed=0`).
- M04 shows the expect_after check is pinned by cases 3, 3b and 7.
- M07, M08, M09 and M12 show the base-mutation, timeout and duplicate-id branches each have a case that fails when disabled.

## Limitations
- Twelve single-line mutants chosen from the five categories named in the task; not exhaustive. Not mutated: the `strip()` calls, `admitted_rows` (selftest helper), exit-code arithmetic. Equivalent mutants (e.g. `base_ok >= len(claims)`) were excluded.
- The probes are my own fixtures in scratch, not the round's claims. I did not run freeze-check against the live counters or claims.
- The control selftest uses `--base <export>`, so case 2 read the export's `corpus/README.md` (27 table-aware admitted rows).
- My first probe run had a fixture bug (`newdir/` persisted across runs, so later runs measured nothing). I fixed it by removing `newdir/` before each check and re-ran all probes; only the corrected run is reported above.
- The "proposed case" text is my suggestion; I verified the behaviour difference with the probe driver, not by editing the selftest.
- Tools: none installed. Mutants were created with the edit tool on copies in scratch. No git/jj mutation, no commits, no fleet or sibling files touched.
