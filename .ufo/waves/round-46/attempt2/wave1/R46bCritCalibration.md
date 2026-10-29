VERDICT: HOLDS

## Result-table replay

No contradicted score cell or missing cited receipt was found in the three latest result tables (`SCORECARD.md:1727-1729, 1741-1763, 1776-1803`). I replayed the counters at their named historical base/tip exports; each base was a red do-nothing control and each cited tip produced the recorded after-value.

- **Round 44** (`SCORECARD.md:1727-1728`): using `S=/fast/scratch/hyaku/kasegi-r46/R46bCritCalibration`, `python3 -B "$S/r44tip/corpus/instruments/r44-routed-defects.py" --root "$S/r44base" --baseline "$S/r44base"` printed `routed-defects total=8 fixed=0 unresolved=8 exit=1`; the same command with `--root "$S/r44tip"` printed `routed-defects total=8 fixed=8 unresolved=0 exit=0`. `r44-frontier-count.py --root "$S/r44base" --expect 26` printed `frontier rows=25 admitted=25` and `frontier expected=26 admitted=25 verdict=SHORT exit=1`; tip printed `frontier rows=26 admitted=26` (exit 0).
- **Round 45** (`SCORECARD.md:1747-1761`): `r45-routed-defects.py` printed `routed-defects total=5 fixed=0 unresolved=5 exit=1` at base and `routed-defects total=5 fixed=5 unresolved=0 exit=0` at tip. `r45-c2-gate.py` printed `c2-gate fixed=1/7 exit=1` at base and `c2-gate fixed=7/7 exit=0` at tip; `r44-frontier-count.py --expect 27` printed `frontier rows=26 admitted=26` / `frontier expected=27 admitted=26 verdict=SHORT exit=1` at base and `frontier rows=27 admitted=27` at tip.
- **Round 46 attempt 1** (`SCORECARD.md:1782-1803`): C1 printed `c1-gate fixed=1/7 exit=1` at base and `c1-gate fixed=7/7 exit=0` at `eb874bc`; C2 printed `c2-gate fixed=1/7 exit=1` at base, `c2-gate fixed=2/7 exit=1` at freeze, and `c2-gate fixed=7/7 exit=0` at tip. `r46-plain-measure.sh` printed base `c1a=23`, `c1b=24`, `c2a=27`, `c2b=72`, `c2c=64`, `c2d=0`; tip `c1a=21`, `c1b=22`, `c2a=28`, `c2b=73`, `c2c=65`, `c2d=3`.

The referenced R44/R45/R46 receipts are present in their controls directories; the six `wave2/R46W2RevGround*.md` pointers and the SHONEN sibling-scan reports also exist.

## SHONEN current-state checks

The evidence commands in `SHONEN.md:309-315` did not produce a contradictory red: current `density.py SKILL.md` ended `**mean dens** ... **258.7**`; `anchorcheck.py SKILL.md` printed `16 in-range cite instances, 0 bad; 16 distinct anchors`; current `r46-c2-gate.py` printed `gate G5 pass=1 read=spans=27 located=27 failed=0 uncited=0 cores=5/5` and `c2-gate fixed=7/7 exit=0`; current plain measures were `c1a=21,c1b=22,c2a=28,c2b=73,c2c=65,c2d=3`; `plain-rows.sh` printed `rows=25 located=25` and `rows=21 located=21`. Current recheck audit printed `strict pass=65/65 ... exit=0` and `executes=43 gated=22 broken=0`. F28 remains in `PROVINCE.md`; its cited sibling reports are present. The four `[~]` boxes remain appropriately unpromoted: the block itself says no non-author verifier, and the end-to-end box says no domain task/submission was performed.

## Strongest current-tree counterexample, scoped

`LOG.md:2017` records the **historical** attempt-1 tip `eb874bc` as `capture binding records=60 bound=60 unbound=0`. The same command on that exact archived tip printed `records=60 bound=60 unbound=0` / `binding_rc=0` (also recorded in `.ufo/waves/round-46/controls/final-measure.txt:363-388`), so this is not a stale historical receipt. On the current attempt-2 tree, `python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-binding-check.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` instead printed `FAIL rule=no-row record=S074 dir=round-46-a2` and `records=61 bound=60 unbound=1` (exit 1). This is the in-flight S074 capture before attempt-2 C2 lands its SOURCES row/entry; the frozen after-value explicitly requires `capture binding unbound=0` (`attempt2/claims.json:33`). It affects the pending **coverage** after-state, not the prior attempt-1 measurement. Smallest safe correction: complete and remeasure the already-claimed S074 binding; do not rewrite the historical LOG line.

## Limitations

No live target or submission was tested. The historic counter/selftest receipts were checked; I did not rerun the larger R44/R45/R46 mutation selftest suites. This scan checks current mechanical outputs and cited-path presence, not the semantic correctness of the scored content or a non-author adjudication.