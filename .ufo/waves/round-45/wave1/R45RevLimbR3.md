VERDICT: BROKEN

# R45RevLimbR3 — C1 limb attack on `limb_r3` (corpus/instruments/r45-routed-defects.py:187-207)

Scope: read-only attack on limb R3 (routed defect spot-check §6 item 3, `r44-frontier-count.py` unregistered with no selftest). Counter sha256 `82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee` (lane file, unmodified). Lane repo not written; no git mutation; all construction in scratch `/fast/scratch/hyaku/kasegi-r45/R45RevLimbR3` (removed on exit).

## Predicate attacked (frozen)

Docstring R3 (r45-routed-defects.py:22-28): "r44-frontier-count.py is a registered gate: `--selftest` prints `selftest cases=N failures=0` with N >= 8; SKILL.md carries a `## Round-45 Gates & probes registry addition` table with eight-cell rows for r44-frontier-count.py, r44-routed-defects.py and wave-registry.py; corpus/instruments/README.md has a row for r44-frontier-count.py."

`limb_r3` (lines 187-207) checks, in order: `r44-frontier-count.py --selftest` rc==0 and token `selftest cases=N failures=0` with N>=8; SKILL.md is append-only vs base; an appended `## Round-45 ...` section contains exactly one 8-cell row each for the three names; README has an `r44-frontier-count.py` row. It never runs the script on a fixture, never reads a verdict map, never checks a pinned path, and never checks that the cases ran.

## Recipe (cheapest tree that reads fixed=1 — `v3`)

Start: pure base export (`/fast/scratch/hyaku/kasegi-r45/L1/pure`, copied to `base` and `v3`); no snapshot change needed for R3.

1. Replace `corpus/instruments/r44-frontier-count.py` (3610 bytes at base) with one 37-byte line:
   `print("selftest cases=8 failures=0")`
2. Append to `SKILL.md` a section `## Round-45 Gates & probes registry addition (appended 2026-10-28)` with three 8-cell rows (`r44-frontier-count.py`, `r44-routed-defects.py`, `wave-registry.py`), each with a stub verdict map and `none` pinned paths.
3. Append one row `| r44-frontier-count.py | probe | ... | stub | - | - | - | stub |` to `corpus/instruments/README.md`.

Printed output (`python3 r45-routed-defects.py --root <v3> --baseline <base>`):
```
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=1 read=selftest-cases=8
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=1 unresolved=4 exit=1
```
Direct run of the stub (`cat -n` + invocation): `     1	print("selftest cases=8 failures=0")` then `selftest cases=8 failures=0`, rc=0. The counter's own docstring (line 22) says R3 needs "a registered gate"; this tree has a registered-looking row whose pinned path is `none` and whose script prints a constant. The defect the limb stands for (no real selftest, unregistered probe) is still present: the real script is gone and the registry describes nothing.

Byte-level diff vs base (`diff -rq base v3`, top-level files): `SKILL.md`, `corpus/instruments/README.md`, `corpus/instruments/r44-frontier-count.py` (the other lines in that diff are scratch-only symlinks under `.ufo/waves/round-31/...`, which are relative `../../corpus/instruments` links in the copy and resolve inside the scratch tree; they are not read by the counter).

## Constructions tried (6 distinct; >=5 required)

Run with the same counter and baseline. Output lines are verbatim.

| # | tree | limb R3 printed |
|---|---|---|
| 0 | do-nothing base (`--root base --baseline base`) | `limb R3 fixed=0 read=selftest-rc=2-tokens=None` |
| 1 | v1: 48-byte stub only, no SKILL/README | `limb R3 fixed=0 read=registry-section-absent` |
| 2 | v2: 37-byte stub + SKILL section, no README row | `limb R3 fixed=0 read=readme-row-absent` |
| 3 | v3: 37-byte stub + SKILL section + README row (**cheapest winner**) | `limb R3 fixed=1 read=selftest-cases=8` |
| 4 | v4: 48-byte stub + SKILL heading with prose only (no rows) + README row | `limb R3 fixed=0 read=registry-row-r44-frontier-count.py=0` |
| 5 | v5: real base script untouched + prose marker in SKILL + README row (marker-only) | `limb R3 fixed=0 read=selftest-rc=2-tokens=None` |
| 6 | full tree: 3-line stub with `--selftest` branch + SKILL + README | `limb R3 fixed=1 read=selftest-cases=8` |

The real script at base prints, for its own selftest call (`python3 corpus/instruments/r44-frontier-count.py --selftest`, rc=2):
```
usage: r44-frontier-count.py [-h] --root ROOT [--expect EXPECT] [--ids]
r44-frontier-count.py: error: the following arguments are required: --root
```
That is the defect text. The base real counter with `--root --expect 27` prints `frontier rows=26 admitted=26` / `frontier expected=27 admitted=26 verdict=SHORT exit=1`, so the honest script does count; the stub does not.

## Discrimination

- Do-nothing control (row 0) and marker-only (row 5) both grade R3 fixed=0; the limb discriminates real-vs-absent. It does not discriminate stub-vs-real: rows 3 and 6 both pass, and row 3 is the 37-byte print.
- The counter's exit remains 1 on every row (R1, R2, R4, R5 unchanged), so this does not change the C1 total on its own. It does show R3 is satisfiable by a fabricated artifact, which is the kill-rule concern for C1 ("counter prints fixed<5 ... or any control grades fixed=5"); the frozen controls (`controls/freeze-controls.txt`) do not include a stub-R3 tree.

## Secondary observation (C2 secondary command, not a C2 limb)

`claims.json` C2 `secondary` = `r44-frontier-count.py --root {tree} --expect 27` (expected to exit 1 at base). On the one-line stub (v3) the same command prints `selftest cases=8 failures=0` and exits 0 (run: `rc=0`). `grep -n frontier-count corpus/instruments/r45-c2-gate.py` returns nothing, so the C2 gate itself does not call this script; only the claims' secondary command is spoofed.

## Limitations

- Single-machine construction in scratch; no lane commit, no shared file touched. Lane file `corpus/instruments/r44-frontier-count.py` (sha not changed, 3610 bytes, mtime 17:33) and lane `SKILL.md`/`README.md` have no stub rows (grep count 0).
- I attacked only R3. R1, R2, R4, R5 are unchanged in the tree and each prints fixed=0; the C1 total is not tested as a whole.
- The stub's rows are honest about being stubs (`stub`, `none`); the limb does not inspect those cells, so a disclosed stub passes equally.
- The frozen control set has no stub-R3 control; my marker-only control (row 5) is a close analogue, not the frozen file itself.
- Scratch-only relative symlinks under `.ufo/waves/round-31/...` (pure export) are inert for the counter.

## Suggested repair (for L1 decision; not applied)

Tighten the R3 predicate so a constant print cannot satisfy it, e.g. require the selftest output to list per-case lines `selftest case=<id> verdict=pass|fail` (the convention already used by `r44-routed-defects.py` in the README), require the script to produce a frontier count on a fixture root, and require each registry row's pinned path to exist. L1 must decide whether that is a counter erratum (predicate sentence unchanged) or a predicate change, which the kill rule forbids after a seat has scored.
