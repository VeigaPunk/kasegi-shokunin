# R44Review14 — Scorecard target semantics

## Finding

**Actionable semantic defect: the frozen C1/C2 targets do not define the requested score delta, and the scorecard cannot truthfully claim one from their counters alone.** `SCORECARD.md:1665-1669` establishes three score axes (depth:verifiability 4, coverage 8, depth:density 9) and the preceding row is explicit that round 43 claimed no increase (`SCORECARD.md:1667-1669`). The frozen R44 claims instead specify C1's defect-closure predicate and C2's coverage counts (`.ufo/waves/round-44/claims.json:8-24`), with no score-before/after values, score mapping, or statement that these observables earn a score-point change. The C1 instrument named there is the routed-defects counter, not a score instrument. Thus achieving the counters can support completion of the frozen predicates, but cannot on its own prove a lowest-axis score delta or scorecard update.

The selected axis is also ambiguous if “lowest axis” means the minimum numeric score: `SCORECARD.md:1667-1669` gives depth:verifiability=4 and coverage=8, while `SCORECARD.md:1679` calls depth:verifiability the lowest non-retired axis. The latter is consistent with the historically named saturation rule, but the C1/C2 freeze does not declare a target axis or connect either predicate to a score change. Do not infer a delta from the word “target.”

## Do-nothing discrimination

Frozen control at `.ufo/waves/round-44/controls/do-nothing.txt:2-13` pins base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`, records eight unresolved defects/no R44 counter, and records C2 baseline 25 frontier rows, 68 source rows and 62 knowledge files; it establishes these after-state predicates cannot be obtained by doing nothing. It does **not** measure score-before/after or establish a score delta. This is a defect in scorecard-target semantics, not a claim that C1/C2 are already satisfied or that the no-op reaches them.

## Evidence / limits

Exact evidence read: `claims.json:8-24`; `controls/do-nothing.txt:2-13`; `SCORECARD.md:1665-1687` (including the R43 move-log showing held scores and no increase). Read-only inspection only. No runtime counter, score calculation, commit mutation, or tool installation was performed. `HYAKU_SCRATCH` was empty; scratch setup was not attempted, so no scratch artifacts exist. No tool installed.
