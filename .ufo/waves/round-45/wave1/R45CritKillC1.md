# R45CritKillC1 — falsification of C1 kill rule and after-state

VERDICT: BROKEN

Scope: C1 (depth:verifiability), counter `corpus/instruments/r45-routed-defects.py` (sha256 82004c700decbc3453baa57919ccff71cbfe322a8d2a71b558d75951c24f04ee, identical at freeze commit 8cf62c8 and in the lane worktree), `.ufo/waves/round-45/claims.json` (sha256 bbe40503281c90eb9d70f469d7bac10125b285758ca9675be9894ce6c12c6206, matches `freeze.txt:2`), `.ufo/waves/round-45/controls/freeze-controls.py` (freeze commit 8cf62c8). Read-only; no lane file touched. Fixtures lived in scratch and were removed on exit.

Summary: `fixed=5` is not a measure of the five routed defects. A do-nothing tree plus prose-only edits reaches `fixed=3`. Two print-only stub lines in code plus one 5-line stub file reach `fixed=5 exit=0`. None of the three frozen controls is that tree, so the frozen kill rule does not fire on it. Several limb predicates are weaker than the after-sentence and the routed defects they answer.

## Method

Trees built in scratch (`$HYAKU_SCRATCH/kasegi-r45/R45CritKillC1/`, default `/fast/scratch/hyaku`):
- `base` = copy of `/fast/scratch/hyaku/kasegi-r45/L1/pure` (base dc5bb8c).
- `T0` = `git -C <lane> archive 8cf62c879e6e6b031e67412f8fac1fba0bd378cf | tar -x -C T0` (freeze commit: base + claims, counters, controls, S071/S072 captures and manifest; no wave edits).
- `P` = T0 + prose-only edits: one S072 row inserted after S070 (S070 bytes unchanged), one `Correction (round 45; fixture)` line appended at EOF of `corpus/lessons/round-44.md`, a `## Round-45 additions` block with R47/R48/R49 rows, a SKILL.md registry section, one instruments README row, and `final-attempt3-refiled.txt` containing a bare `--selftest` call with `exit=2` plus a `--root tip --selftest --work scratch` run line with `selftest cases=20 failures=0` and `exit=0`. No code changed.
- `Pflipna` = P with the S072 flip clause `flip: n/a`.
- `PS` = P + two stubs: `corpus/instruments/r44-frontier-count.py` gains 3 lines at the top of `main()`:
  ```
  +    if argv == ["--selftest"]:
  +        print("selftest cases=8 failures=0")
  +        return 0
  ```
  and new file `corpus/instruments/freeze-check.py` (5 lines) that prints `selftest cases=6 failures=0` for `--selftest` and `freeze-check claims=2 base_ok=2` otherwise.

Commands and printed output (verbatim):

```
$ python3 corpus/instruments/r45-routed-defects.py --root base --baseline base      # do-nothing
limb R1 fixed=0 read=row-S072=absent
limb R2 fixed=0 read=quality-not-append-only-or-unchanged
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=0 read=refiled-absent
routed-defects total=5 fixed=0 unresolved=5 exit=1
```
T0 (freeze tree, no wave work) prints the identical five lines and `routed-defects total=5 fixed=0 unresolved=5 exit=1`.

```
== P = prose-only edits (no code), bare call retained in receipt  (exit=1)
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=1 read=refiled=ok original=unchanged
routed-defects total=5 fixed=3 unresolved=2 exit=1
== Pflipna = P with flip clause 'flip: n/a'  (exit=1)
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=0 read=selftest-rc=2-tokens=None
limb R4 fixed=0 read=freeze-check-absent
limb R5 fixed=1 read=refiled=ok original=unchanged
routed-defects total=5 fixed=3 unresolved=2 exit=1
== PS = P + two print-only stubs (r44-frontier-count --selftest, freeze-check.py)  (exit=0)
limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
limb R2 fixed=1 read=criteria=3
limb R3 fixed=1 read=selftest-cases=8
limb R4 fixed=1 read=selftest-cases=6 replay=base_ok=2
limb R5 fixed=1 read=refiled=ok original=unchanged
routed-defects total=5 fixed=5 unresolved=0 exit=0
```

Re-run of the frozen controls (`freeze-controls.py --base-export base --lane <lane> --work <scratch>/controls`) reproduces `freeze-controls.txt` exactly: five `expect=RED got=RED` lines, `controls total=5 red=5 green=0`. The frozen control set therefore does not contain PS, Pflipna or any prose-only tree.

## Findings

### F1 — `fixed=5` is reachable without resolving the defects (kill-rule / after-state)
- Attacked: claims.json C1 `kill_rule` ("any control … grades fixed=5") and `after` ("5 of those 5 are resolved … as read by the committed counter").
- Evidence: PS above, `exit=0`, `fixed=5`. Its only code edits are the 3-line `main()` stub in `r44-frontier-count.py` (diff printed above) and the 5-line `freeze-check.py`.
- Prose-only reach: P grades `fixed=3`. R3 and R4 cannot be reached by prose: `r44-frontier-count.py` at base rejects `--selftest` (`selftest-rc=2-tokens=None`), and `freeze-check.py` is absent at base.
- Consequence: C1 `after` is not a statement about the five defects. It is a statement about printed tokens. The kill rule is not triggered because PS is not among its controls (freeze-controls.py:50,51,71,83,97 list only do-nothing-base ×2, c1-marker-only, c2-junk-row, c2-fabricated-quote).

### F2 — the frozen controls are not the cheapest adversary
- Attacked: freeze-controls.py:57-70 (c1-marker-only tree).
- The marker tree is RED for reasons outside its markers. It has no S072 row (R1), no `--root … --selftest --work …` run line (R5, its receipt at line 70 is only `selftest cases=20 failures=0\nexit=0`), no selftest (R3) and no freeze-check (R4). Its QUALITY rows point `enforced-by:` at `corpus/instruments/nothing.py`, which does not exist (lines 61-63), so R2 fails for a reason the control never tests. Adding the invocation line, the S072 row and the enforced-by pointer turns R5 and R2 green (P). The control's RED is therefore not evidence that prose-level markers are rejected.

### F3 — per-limb predicate weaker than the after-sentence / routed defect
- R1 flip (counter line 110, `re.search(r"flip:\s*\S", teaches)`): the base S070 row (`corpus/SOURCES.md:76`, flip clause "flip: the page itself exposes a located, program-specific rule absent from the linked policy text.") matches this regex (python: `flip regex r'flip:\s*\S' matches base S070 teaches: True`). Pflipna with `flip: n/a` also grades R1 fixed=1. Routed defect 1 demanded a *replaced*, *checkable* flip; the predicate accepts any non-empty text, including the base text it was meant to replace.
- R1 placement (counter line 136, `tail` = anything appended to round-44.md): routed defect 1 names `round-44.md` `## Gate` (lesson line 20). P's correction sits at EOF (fixture line 205) and grades R1 fixed=1. Placement is not checked.
- R1 size token (counter line 112, regex on prose): the token "10 029" is never measured. Pinned capture `corpus/source-snapshots/round-45/S072.txt` (manifest `bytes: 10032`) measured by python: `chars= 10030 chars_rstrip_newlines= 10028 ends_with_newline= True`. Neither convention gives the claimed 10029. The counter accepts the token and does not compare it to the capture.
- R1 S070 (counter lines 116-119): S070 must stay byte-identical. Routed defect 1 asked for an appended correction *to the S070 row*. The after-sentence chose row supersession, so this is consistent with the after, but it is not the routed defect's literal remedy. Record as a mismatch between item and predicate.
- R2 grounding (counter line 167, `"corpus/lessons/round-44.md" not in ground`): substring only. Routed defect 2 names M44-3/M44-8, M44-4/M44-7/M44-10 and the spot-check; none is checked.
- R2 enforced-by (counter lines 172-177, `os.path.exists`): accepts a directory. P's R47 row uses ``enforced-by: `corpus` `` and grades criteria=3 (fixed=1).
- R3 (counter lines 189-192): runs the tree's own script and reads only the printed token `selftest cases=N failures=0`. Routed defect 3 asked for "a selftest". PS's print stub satisfies the predicate (`selftest-cases=8`).
- R4 (counter lines 218-220): freeze-check is the tree's script, invoked with `--claims <root>/.ufo/waves/round-45/claims.json`. The counter never reads `freeze.txt` `claims-sha256` (`freeze.txt:2`, bbe40503…). Grep of the counter for binding (`grep -n "sha256\|freeze\|claims\|CENSUS"`) shows sha256 used only for the S072 snapshot (lines 126, 129), no claims or freeze.txt binding. CENSUS (line 55) is an unused constant. Routed defect 4 ("frozen counter string must be run on base before freeze … hold the lane to it") is not checked: neither the claims' `expect_before` nor `expect_after` strings are compared with the counter output.
- R5 (counter lines 230-236; docstring lines 31-34 says "without the failed bare call"): the code checks only `usage:`/`error:` lines, the presence of an `exit=0` line anywhere (line 234, `(^|\s)exit=0\s*$`), a hard-coded `selftest cases=20 failures=0`, and the invocation regex `--root \S+ --selftest --work \S+`. The bare call is not checked for absence. P retains `$ python3 corpus/instruments/r44-routed-defects.py --selftest` followed by `exit=2` and grades R5 fixed=1. The invocation regex also accepts placeholders: the lane worktree receipt `.ufo/waves/round-44/controls/final-attempt3-refiled.txt` (untracked) contains `$ python3 corpus/instruments/r44-routed-defects.py --root <tip> --selftest --work <scratch>`, and the base `final-attempt3.txt` carries the same placeholder form.

### F4 — routed defects still open after the five limbs
1. S070 reject reason: true reason ("overview, no program-specific rule beyond S069 Q5") is not checked; the flip is not checked for checkability (F3); the correction placement is not checked (F3). Open.
2. QUALITY R47/R48/R49: grounding to specific M44 IDs not checked; `enforced-by:` checks existence only. Open.
3. `r44-frontier-count.py`: "give it a selftest" is satisfied by a print line (PS). Open.
4. Freeze hygiene: counter does not pin claims bytes to `freeze.txt` and does not compare claims `expect_*` strings to the counters' output. Open.
5. Receipt: a bare failing call can stay in the refiled file (P). Receipt not checked to come from a run. Open.

### F5 — root cause (for L1 / sentinel seat)
The counter executes tree-controlled scripts (lines 123, 189, 214-219) and grades only their printed tokens. Any limb that depends on a tree-authored script is self-certifying. Only R1 binds content (source-recheck against the frozen manifest and sha-pinned snapshot, `recheck-quotes=2`), and even R1's size token is unmeasured.

### F6 — process tension (not a counter bug)
`wave1.ready` (17:59) and drafts under `wave1/` exist, so seats have been dispatched. Under the frozen kill rule, any predicate tightening after scoring must be logged as counter errata and must keep the predicate sentence. Controls cannot be changed after seats score without the same erratum route. L1 must decide whether the sentence is kept with tighter limbs (errata) or the claim is re-frozen.

## Smallest safe correction (for L1 to decide; not applied)
- Make R3 and R4 behavioural on counter-owned fixtures: the counter builds its own frontier and claims fixtures, runs the tree script on them, and checks exit code and value against independently computed expectations. A print stub then fails.
- R4: compare `claims.json` bytes to `freeze.txt:2` (`bbe40503…`) and compare each claim's `expect_before`/`expect_after` to the counter's printed line at base and at the tip.
- R1: compare the size token to the pinned snapshot's measured length (state the convention) and require the flip clause to change from the base S070 text.
- R5: fail on any line that is the bare `--selftest` call without `--root`/`--work`.
- Controls: add `P` (must be RED with fixed ≤ 3) and `PS` (must be RED) to freeze-controls.py. PS currently grades fixed=5.

## Limitations
- The final lane revision did not exist when I ran (worktree holds untracked wave-1 files). All grades are on fixtures = freeze commit 8cf62c8 + the edits described above, not on the L1's final commit. The kill rule's "at the final lane revision" test is therefore not executed here.
- PS's stubs are my constructions to show what the counter accepts. They do not show what a seat would write.
- `r44-frontier-count.py` and `freeze-check.py` are absent or unselftested at base; I did not evaluate any lane-written version.
- S072 live body was not re-fetched (corpus-only, no live target); the 10029 figure is compared only to the pinned capture.
- C2 counter (`r45-c2-gate.py`) was not analysed beyond re-running freeze-controls.py, which reproduced its control lines.
- No tools installed; no git/jj mutation; no file in the lane, the fleet repo or shared paths written. Scratch removed on exit.
