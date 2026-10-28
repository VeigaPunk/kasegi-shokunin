# R44Critic7 — falsifying defect-7 registration correction

## Finding

**The proposed registration/counter pair can report RD43-7 resolved while the R29 registered-basename contract is false.** The current worktree adds the two round-43 rows in `SKILL.md`, but places them under `## Round-44 registry correction — round-43 instrument basenames` (line 1136), which omits `Gates & probes registry`. The committed section-scoped scanner in `corpus/instruments/r36-closure.sh:280-289` counts rows only inside a heading containing `Gates & probes registry`; I ran that exact `e3_registry_rows` awk logic against the current `SKILL.md`: `r42-closure.sh=1` (positive control), `r43-closure.sh=0`, `claim-package-check.py=0`, while `r44-routed-defects.py=1` under the later proper heading. R29 in `corpus/QUALITY.md:264` requires a row whose name cell is exactly the file basename, and rejects near-name/substrings.

The proposed C1 predicate does not enforce that contract. Current `corpus/instruments/r44-routed-defects.py:51` is:

```python
("RD43-7 gate registry pointer", "claim-package-check.py" in skill and "r43-closure.sh" in skill and "SKILL.md Gates & probes registry" in lesson)
```

Counterexample reproduced in `$HYAKU_SCRATCH/kasegi-r44/R44Critic7/`: I changed only the two SKILL.md name cells to the R29-rejected near-names `claim-package-check-legacy.py` and `r43-closure-old.sh`, leaving their entry-command cells (which contain the original basenames) intact; the lesson still explicitly left the old report pointer uncorrected and merely mentioned `SKILL.md Gates & probes registry`. The committed `e3_registry_rows` logic returned 0 for both basenames, but the round-44 counter printed `RD43-7 gate registry pointer resolved=1` (`frozen_defects=8 fixed=1 unresolved=7 exit=1`). Thus the counter can grant this defect credit without a single valid registration row or a pointer retraction. Its selftest (`--selftest --scratch-root /fast/scratch/hyaku/kasegi-r44/R44Critic7/st`) passed 9/9, but its RD43-7 mutant only removes `r43-closure.sh` from a bare-text fixture (`r44-routed-defects.py:71, 89-90`); it does not test near-name rows, wrong-section rows, or a still-live false pointer.

Second factual defect in the proposed correction prose: `SKILL.md:1138` says the report named a “nonexistent `corpus/instruments/README.md`.” That file exists in the committed tree: `git ls-tree HEAD corpus/instruments/README.md` → `100644 blob 6b15e4448903c88feaf76e205089c4058db47a65`; `test -e corpus/instruments/README.md` → true. The frozen spot-check says the file had zero hits for these names (`corpus/lessons/round-43-verifier-spotcheck.md:30`); it does not say the file is absent. The original fleet report at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/kasegi.md:91` still contains the false pointer and the statement “not yet as `SKILL.md` Gates & probes rows”. A lane-side append must correct that record, not merely add rows.

## Smallest safe correction

1. Put the two exact-basename rows inside a heading containing `Gates & probes registry` (e.g. `## Round-44 Gates & probes registry addition — round-43 instrument basenames`) so the existing section-scoped scanner and R29 recognize them. The current rows themselves use exact name cells, but their current section is excluded by the established scanner.
2. Correct the prose to say the README exists but has no entries for these instruments; append a record correction that names both exact basenames and supersedes the false pointer. Do not call the `corpus/README.md:608` descriptive round-43 note a registered basename under R29.
3. Replace RD43-7’s substring tests with row parsing restricted to `Gates & probes registry` sections and exact first-column basenames; test against a near-name row, a correct basename outside a registry section, and an uncorrected pointer plus an incidental registry phrase. The counter should award credit only when both registrations and the pointer correction are true.

## Do-nothing and verification

The frozen do-nothing control records base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a` and says no R44 correction existed. I replayed the then-current counter against a scratch `git archive 5ab3a60` export as both `--root` and `--baseline`: RD43-7 resolved=0; all eight unresolved; exit 1. This discriminates no-op, but does not protect against the false-green mutant above. `python3 corpus/instruments/anchorcheck.py SKILL.md` on the current worktree reported `16 in-range cite instances, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0. That citation check does not establish registration.

The counter bytes were changing during this live review; the tested predicate was independently re-read at `corpus/instruments/r44-routed-defects.py:51` after the worktree update. No tool was installed. No production file was edited by this seat; scratch is removed before exit.

## Report trailer

Relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`: `.ufo/waves/round-44/wave1/R44Critic7.md`