VERDICT: DRAFT-READY

# R45ScribeRegistry — C1/R3 registry draft (round 45, kasegi)

Scope: draft only. Output: `.ufo/waves/round-45/wave1/R45ScribeRegistry.draft/registry-append.md` (Part A: SKILL.md block; Part B: four README rows). Nothing committed; no shared file touched. Trees measured: base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd` (git archive), head `5242db6fbf2b3575da6600974f0b5b4292caa62f` (git archive), and the lane worktree where stated. Scratch removed on exit.

## 1. What the draft contains (built and tested)

- Part A: header line exactly as required (`grep -nx` printed `10:## Round-45 Gates & probes registry addition (appended 2026-10-28)`), 8-column header, one row each for r44-frontier-count.py, r44-routed-defects.py, wave-registry.py, freeze-check.py, r45-routed-defects.py, r45-c2-gate.py. Entry commands, verdict maps, self-test spellings, pinned-value paths and write scopes were read from each script's docstring/argparse and then re-run (below).
- Part B: four README rows (r44-frontier-count.py, freeze-check.py, r45-routed-defects.py, r45-c2-gate.py), appended after README line 993. r44-routed-defects.py (line 992) and wave-registry.py (line 993) already have rows and are not duplicated.
- Per-row cell count, printed by parsing the draft with the R3 limb's own rule (`strip("|").split("|")`): every row = 8 cells. `grep -c '\\|'` on the draft printed `escaped-pipes=0`.

## 2. Falsification of the draft against the real R3 limb

Method: loaded `corpus/instruments/r45-routed-defects.py` with importlib and called its real `limb_r3(root, base)` on fixture trees (copies of the base export with the draft applied). Only `run` is stubbed, to return `selftest cases=8 failures=0`, so the limb reaches its SKILL/README row checks. The `r44-frontier-count.py --selftest` flag does not exist (finding 3.1), so an unstubbed run cannot pass R3 at any tree.

Command: `SCR=<scratch> python3 <scratch>/tmp/r3test.py` and `r3test2.py`. Output (quoted):

```
T1 draft applied   : (True, 'selftest-cases=8')
T2 do-nothing base : (False, 'registry-section-absent')
T3 README rows only: (False, 'registry-section-absent')
T4 escaped-pipe row: (False, 'registry-row-r44-frontier-count.py=1')
T5 README row removed: (False, 'readme-row-absent')
T6 duplicated wave-registry row: (False, 'registry-row-wave-registry.py=2')
T7 freeze-check SKILL row dropped (R3 checks only 3 names): (True, 'selftest-cases=8')
```

- T1 passes the draft; T2/T3 (do-nothing control) fail as they must; T5/T6 show the README and exactly-one rules bite.
- T4: a `\|` inside a cell fails the 8-cell check, but the message misreports it as `registry-row-…=1` (a row count), which is misleading. The draft therefore uses no pipe in any cell (see the draft's integrator note).
- T7 (finding 3.2): the frozen R3 limb grades only r44-frontier-count.py, r44-routed-defects.py and wave-registry.py. Deleting the freeze-check.py row, or any r45-* row, leaves R3 green.

## 3. Counter and script findings (each re-run; quoted output)

### 3.1 r44-frontier-count.py — R3 selftest is absent (confirmed live)
- `python3 corpus/instruments/r44-frontier-count.py --root <base>` → `frontier rows=26 admitted=26` (exit 0).
- `… --root <head> --expect 27` → `frontier expected=27 admitted=26 verdict=SHORT exit=1` (exit 1). Matches claims.json secondary `base: frontier rows=26 admitted=26 exit 1` for the base-side expectation.
- `… --root <head> --selftest` → `usage: r44-frontier-count.py [-h] --root ROOT [--expect EXPECT] [--ids]` / `error: unrecognized arguments: --selftest` (exit 2). So R3's selftest component is unmet, and the draft's self-test cell states the flag as the repair target, marked absent at base.
- Docstring discrepancy: the OUTPUT section promises `frontier rows=<n> admitted=<k> exit=0|1`; the code prints no exit token. The draft's verdict cell describes the actual output.
- Docstring staleness: it says the frozen base count is 25; measured base dc5bb8c is 26.

### 3.2 r45-routed-defects.py (R1–R5) — all five limbs at base and head; R5 depends on an untracked file
- Base and head exports: `routed-defects total=5 fixed=0 unresolved=5 exit=1`; reads `row-S072=absent`, `quality-not-append-only-or-unchanged`, `selftest-rc=2-tokens=None`, `freeze-check-absent`, `refiled-absent`.
- Lane worktree, same counter (`--root <lane> --baseline <base>`): `limb R5 fixed=1 read=refiled=ok original=unchanged` and `routed-defects total=5 fixed=1 unresolved=4 exit=1`. `git status --short` shows `?? .ufo/waves/round-44/controls/final-attempt3-refiled.txt` and `git ls-files` for it prints 0. So R5 goes green only because the receipt is an untracked worktree file; the committed head does not have it. The L1 must commit that file for R5 to count at the final revision.
- Control: claims.json `counter_cmd` is the same command; freeze-controls.txt do-nothing control `control do-nothing-base counter=C1 routed-defects total=5 fixed=0 unresolved=5 exit=1 expect=RED got=RED` — re-run at base gives the same `fixed=0 unresolved=5 exit=1`.
- Pinned claims: `sha256sum .ufo/waves/round-45/claims.json` → `bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206`, equal to `freeze.txt` `claims-sha256:` value.

### 3.3 r45-c2-gate.py (G1–G7)
- Base: `gate G1 pass=0 read=rows=26 admitted=26 dup=0`, `gate G2 pass=0 read=F27-rows=0`, `gate G3 pass=0 read=row-S071=absent-or-malformed`, `gate G4 pass=0 read=manifest-absent`, `gate G5 pass=0 read=F27-rows=0`, `gate G6 pass=0 read=knowledge=63`, `gate G7 pass=1 read=census-rc=0`, `c2-gate fixed=1/7 exit=1` (equals claims `expect_before`).
- Head: `gate G4 pass=1 read=recheck-rc=0 quotes-ok=5 frozen-cores-missing=0`; `c2-gate fixed=2/7 exit=1`. G1, G2, G3, G5 and G6 are still red at head (no F27 row yet), as expected.
- G7 is a real check: `bash sources-census.sh validate --file /nonexistent/SOURCES.md` → `ERROR: --file not found: /nonexistent/SOURCES.md`, exit 2; with the real file → exit 0. Read-only: census output goes to stdout unless `OUT` is set.
- Do-nothing control re-run: C2 base 1/7 exit 1 (matches the recorded control). Junk-row and fabricated-quote controls are recorded in freeze-controls.txt and were not re-run by me.

### 3.4 r44-routed-defects.py (D1–D8) — red at the frozen base
- Base `dc5bb8c` and head `5242db6` and lane worktree all: `R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping` and `routed-defects total=8 fixed=7 unresolved=1 exit=1`.
- Cause (read from source): D4 uses `head = log.rfind("## Round 44")` (r44-routed-defects.py:404), i.e. the LAST round-44 heading, `## Round 44 (attempt 3)` at LOG.md:1994. The only `planner=L1` in LOG.md is at line 1980 (`grep -c 'planner=L1' LOG.md` → 1), inside the attempt-2 section. So the D4 limb is a scoping defect in the counter, not a missing record.
- Its own selftest: `r44-routed-defects.py --root <head> --selftest --work <existing dir>` → `selftest case=POSITIVE verdict=fail fixed=7 unresolved=1`, 19 other cases `verdict=pass`, and `selftest cases=20 failures=1` (exit 1). The mutant battery is rejected correctly; only the positive case is red. The draft's self-test cell records this measured state.
- `--work` must already exist: a missing dir gives an uncaught `FileNotFoundError` traceback (exit 1), not a verdict.

### 3.5 wave-registry.py — emitter edges
- `--results .ufo/waves/round-44/wave1-results.json --out <scratch>` → `wave-registry: wrote … seats=66 names=66 attack=40`, exit 0.
- Mismatch fixture (`seats` 3, one named) → `wave-registry: seats=3 but 1 named seats — refusing to emit`, exit 1, no output file.
- Edge: a results list with no named entry and no `seats` key → uncaught `ZeroDivisionError: division by zero` at line 100 (`100.0 * attack / seats`), exit 1, no output file. Not a silent pass (no file is written), but the refusal path is not the one the docstring describes. Recorded in the draft row.
- `--selftest` → argparse `unrecognized arguments: --selftest`, exit 2: the emitter has no self-test; the row says so.
- The committed `.ufo/waves/round-44/wave-registry.txt` exists (1008 bytes).

### 3.6 freeze-check.py — not present
- `ls corpus/instruments/freeze-check.py` at the lane checkout → `No such file or directory`. The row is the contract from claims.json and the R4 limb (`freeze-check claims=2 base_ok=2`, selftest N >= 6); its verdict wording is marked as contract, not measured. It is valid only in the commit that lands the script.

### 3.7 Cross-cutting
- Fleet-root dependency: r45-c2-gate.py (G7) and r45-routed-defects.py both default to `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`; r45-routed-defects.py defines `CENSUS` (line 55) and never uses it (dead code). The draft's pinned-value cells name the fleet script for G7 and the override variable.
- The SKILL.md and README anchors match the existing rows for r44-routed-defects.py and wave-registry.py; the existing README rows use `\|` inside cells, which the R3 limb's naive split would not accept in SKILL.md, so the draft avoids pipes in all cells.

## 4. Limitations and what the L1 must do

- The freeze-check.py row is contract-only (not measured). Re-check its row once the script lands: its `--selftest` count and replay line must match what is written.
- The `r44-frontier-count.py --selftest` row describes the R3 repair target; R3 cannot be green until that flag is added. Its verdict cell is the spec, not a measured state.
- The R3 limb test used a stub for the sub-selftest subprocess; it isolates the row checks only.
- Not re-run by me: the C1 marker-only control and the C2 junk-row and fabricated-quote controls (recorded in freeze-controls.txt).
- Exports: git archive of dc5bb8c and of HEAD 5242db6; the pure export path given in the task was not used.
- Nothing was committed, pushed, or written to SKILL.md, README, LOG.md, MANIFEST.json, .ufo/state or any shared file. Scratch under `$HYAKU_SCRATCH/kasegi-r45/R45ScribeRegistry` removed on exit.
- Install/update: none performed by this seat.
