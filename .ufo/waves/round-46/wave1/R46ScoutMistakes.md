# R46ScoutMistakes — round-46 mistake mining (kasegi)

VERDICT: INFO

Read-only scout. No edits, no commits, no git mutation. Scratch `/fast/scratch/hyaku/kasegi-r46/R46ScoutMistakes/` (exports of base `914ca0b`, freeze `9f23aab`, round-44 tip `c950fa3`, round-45 tip `2998baa`), removed on exit.

## Ranked candidates (up to 5)

| # | Class | Evidence (path:line) | captured-by (QUALITY.md) | Fix that can be shown to fail first |
|---|---|---|---|---|
| A (recommended) | stale-premise | `corpus/instruments/r44-routed-defects.py:404-407` (`head = log.rfind("## Round 44")`); `LOG.md:1965`, `:1977`, `:1994` | none | bind the round-44 section that states `wave 1 seats:`, not the last `## Round 44` heading |
| B | landing | freeze `9f23aab`: `corpus/instruments/capture-binding-check.py` rule `no-row` on S073; `corpus/SOURCES.md` has 72 rows, no S073 | R20 (exists; gate not run before freeze) | run `capture-binding-check.py --root` on the freeze tree before freezing; it prints rc=1 at `9f23aab` today |
| C | number-drift | `.ufo/waves/round-46/claims.json` C2 `expect_before` = base reading `1/7`; `freeze_tree_reading` = `2/7`; `corpus/instruments/freeze-check.py` replays at base only | none (R47 is base-only) | add a freeze-tree replay: fail when `freeze_tree_reading` is absent or differs from the counter's line at the freeze tree |
| D | attribution / number-drift (timestamp field) | L1 candidate: `.ufo/reports/round-45/kasegi.md` commit `a1f7761` | R33 (exists; satisfied) | refuted at committer time; see below. Not recommended |
| E | scope / attribution (quotes) | `corpus/lessons/round-45.md:14` (M45-4); `corpus/QUALITY.md:16-17` (Q3, Q4) | Q3, Q4 (exist; no gate detects a cut quote) | a quote-completeness fixture: a truncated verbatim span must fail; today it is located |

### A — round-44 counter binds the last round-44 LOG heading (recommended)

Committed bytes: `corpus/instruments/r44-routed-defects.py:404-407`:
```
head = log.rfind("## Round 44")
...
section = log[head:]
```
`LOG.md` round-44 headings (`grep -n 'Round 44' LOG.md`): `1965:## Round 44 (attempt 1, fresh-start)`, `1977:## Round 44 (attempt 2) — L1 ...`, `1994:## Round 44 (attempt 3) — L1 ...`. The attempt-2 section states `wave 1 seats: 66 (...)`; the attempt-3 section does not.

Commands run (scratch export of `914ca0b`):
```
python3 corpus/instruments/r44-routed-defects.py --root . --selftest  →  selftest case=POSITIVE verdict=fail fixed=7 unresolved=1 ; selftest cases=20 failures=1  (rc=1)
python3 corpus/instruments/r44-routed-defects.py --root .            →  R44-D4 status=unresolved detail=the round-44 LOG section does not state the wave-1 seat count
                                                                        routed-defects total=8 fixed=7 unresolved=1 exit=1
```
Discrimination control (scratch export of round-44 tip `c950fa3`, `git cat-file -e` present): `routed-defects total=8 fixed=8 unresolved=0 exit=0`. The same bytes read green at `c950fa3` and red at `914ca0b`: the reading is tree-relative, the defect is in the binding.

Captured-by: none. `grep -n 'rfind\|M45-' corpus/QUALITY.md` → no criterion names the defect or the row (R47 replays frozen counters at base via `freeze-check.py`; the r44 counter is not frozen by it). R36 requires a criterion citing the row or a stated reason; `corpus/lessons/round-45.md:12` (M45-2) gives `none` with no reason.

Fail-first fix check: the POSITIVE case already fails at base (above). A repair that binds the first section stating `wave 1 seats:` must turn POSITIVE green and must keep a mutant that deletes the attempt-2 seat line red.

### B — S073 capture committed before its registry row (recurrence of M45-5)

```
cd <export of 9f23aab> && python3 corpus/instruments/capture-binding-check.py --root .   → FAIL rule=no-row record=S073 dir=round-46 ; records=60 bound=59 unbound=1 ; rc=1
cd <export of 914ca0b> && python3 corpus/instruments/capture-binding-check.py --root .   → rc=0
git show 9f23aab:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   → 72 ; grep -c S073 → 0
```
The lane working tree printed the same `FAIL rule=no-row record=S073 dir=round-46`. Same class as `corpus/lessons/round-45.md:15` (M45-5): the rule existed and was not run before the artifact was frozen. Limitation: the row is expected to land with F28, so the red is likely transient; the freeze commit itself stays red.

### C — before-value read at base only (M45-1 recurrence, partly captured)

`.ufo/waves/round-46/claims.json` now carries `"freeze_tree_reading": "c2-gate fixed=2/7 exit=1 at the freeze tree (G4 capture + G7 census)."` for C2. Reproduced on the freeze export: `python3 corpus/instruments/r46-c2-gate.py --root .` → `c2-gate fixed=2/7 exit=1` (output printed by the run, scratch `f9-c2.txt`). `corpus/instruments/freeze-check.py:19-24` checks that some output line equals `expect_before`; it replays only at the base. The freeze-tree value is recorded in prose and never graded.

Captured-by: none for the freeze-tree case. A fix to check: remove `freeze_tree_reading` from a scratch copy of `claims.json`; a grader that reads it must go red. Not executed (freeze-check does not read the field).

### D — report/commit ordering (L1 candidate): not supported at committer time

```
git -C /home/vgpnk/Projects/shokunin show -s --format='%h author=%an %ad | committer=%cn %cd' a1f7761b
  → a1f7761b author=kasegi-shokunin Wed Oct 28 19:30:06 2026 -0300 | committer=kasegi-shokunin Wed Oct 28 19:37:42 2026 -0300
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show -s --format='%h author=%an %ad | committer=%cn %cd' 2998baab
  → 2998baa author=kasegi-shokunin Wed Oct 28 19:36:30 2026 -0300 | committer=kasegi-shokunin Wed Oct 28 19:36:31 2026 -0300
%at / %ct: report 1793226606 / 1793227062 ; lane 1793226990 / 1793226991
```
The spot-check's ordering (`corpus/lessons/round-45-verifier-spotcheck.md:22`, §6.1) compares the report's author time (19:30:06) with the lane's author time (19:36:30). The filing time (committer, R33 "the report is filed after the last lane commit") is 19:37:42, 71 s after the lane's committer time. The report names `2998baa`, which exists in the lane repo, not in the fleet repo (`git -C /home/vgpnk/Projects/shokunin cat-file -e 2998baa…` → rc=1), so the report was committed in the fleet repo, after its cited hash.

Captured-by: R33 (`corpus/QUALITY.md:292`), satisfied. A checker on `%ct` passes at this commit and at a do-nothing control, so the defect exists only if `%at` is chosen. Not recommended as the round's mistake.

### E — quote completeness passes a cut quote (M45-4)

`corpus/lessons/round-45.md:14` records a cut QA quote, a "strongly recommends" turned into "not yet permitted", and CVE/linux-distros rows out of scope. `git show 2998baa:corpus/source-snapshots/round-45/S071.txt` contains `the logistics of QA and large scale rollouts which require release` (line 314) and the located-substring check accepts a truncated span:
```
"for up to 7 calendar days from the start of the release process" located words=13
"for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days" located words=21
```
Captured-by: Q3 and Q4 exist (`corpus/QUALITY.md:16-17`), but no gate detects a cut span or a strength change. Fix to show failing first: a completeness fixture where the located span stops mid-sentence must fail. Not executed.

## Other round-45 items considered and dropped

- M45-3 (vacuous counters): captured by R48 now; not live.
- M45-6 (attribution of the S070 correction): the correction names both lines (`round-44.md:22`, `:131`); not reproduced.
- M45-7 (freeze-check scratch dependency): `grep -n '/fast/scratch' corpus/instruments/freeze-check.py` finds no hit; fixed.
- S072 duplicate-URL W04 (spot-check §6.4): intended census warning, not a defect.

## Limitations

- Captured-by checks read `corpus/QUALITY.md` by grep; semantic coverage of R-rows was not re-read in full.
- Fail-first fixes are described and not implemented (read-only seat).
- The freeze-tree and round-44 counter runs are from `git archive` exports in scratch; the lane working tree was read but not modified.
- Scratch removed on exit.
