# Round-22 M3/M14 pointer audit

## Scope and axes

Axes: **depth:verifiability** and **coverage**. Read-only comparison of the committed round-22 lesson, the prior README snapshot, and the README as committed in round 22. This report does not alter historical records or production files; it supplies correction wording for a later append-only record.

Repository: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round-22 README/lesson commit: `c8b719d22882863ea7cd89b14c8bc078228001ed`.
Its parent is `67fb678` (short ID observed in `git blame` and history).

## Findings

### M3 — README line pointer stale by eight lines

The round-22 mistake table at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md:15` points to `corpus/README.md:168` for the critic-falsification statement. On the parent README snapshot, `git blame -L 168,169 67fb678 -- corpus/README.md` returns the text beginning “falsification REJECTED with evidence” at line 168 and the `[lost-tree] fleets/claimer-mission.md:29` assertion at line 169. That explains the historical pointer.

Commit `c8b719d` inserted eight coverage-map rows before `## Known gaps` (`git show --format=fuller c8b719d -- corpus/README.md`, hunk `@@ -34,6 +34,14 @@`). In the committed round-22/current README, lines 168–169 instead concern `portal-reconciliation-2026-09-11.json` and `final-audit.json`; the matching M3 statement is at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:176-177`. The line shift is +8; the statement itself remains present.

### M14 — README pointer stale by eight lines; count predates the lesson

The round-22 mistake table at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md:26` points to `corpus/README.md:145` and states that `corpus/lessons/` has 24 files, with none for rounds 2, 16, 18, and 19. On parent `67fb678`, `git blame -L 145,147 67fb678 -- corpus/README.md` confirms lines 145–147 are the round-2 ledger-hole text. After the same eight-row insertion in `c8b719d`, line 145 is an unrelated HARD_STOP/symlink/walk-gates item; the round-2 statement is now at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:153-156`.

The `24` count is also pre-round-22: `git ls-tree -r --name-only 67fb678 -- corpus/lessons | wc -l` returned 24, while the same command at `c8b719d` returned 25, because that commit adds `corpus/lessons/round-22.md`. The four named gap paths remain absent in `c8b719d`; each was checked with `git cat-file -e c8b719d:corpus/lessons/<name>`. The round-22 README itself records 25 files and those four gaps at `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:44`.

## Causal reconstruction and falsifiable check

Both stale pointers still matched the pre-round-22 README. The round-22 commit added eight rows to the coverage map ahead of both target passages, shifting their locations by exactly eight lines without refreshing the M3/M14 evidence pointers in the new lesson. M14's 24-file count likewise matches the parent snapshot, not the round-22 commit containing the newly added round-22 lesson.

Reproduction uses only Git reads and the cited committed files:

```text
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin blame -L 145,147 67fb678 -- corpus/README.md
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin blame -L 168,169 67fb678 -- corpus/README.md
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show c8b719d:corpus/README.md
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree -r --name-only 67fb678 -- corpus/lessons | wc -l
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree -r --name-only c8b719d -- corpus/lessons | wc -l
```

Expected observations: parent target lines 145 and 168 are the intended text; the round-22 README contains those passages at 153–156 and 176–177; tracked lesson counts are 24 then 25.

## Append-only correction wording

Suggested addition to the next lesson or report; do not replace or edit the round-22 record:

> Correction (2026-10-20; round-22 README snapshot `c8b719d22882863ea7cd89b14c8bc078228001ed`): the M3 pointer recorded as `corpus/README.md:168` and M14 pointer recorded as `corpus/README.md:145` in `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-22.md` refer to the parent README. The round-22 commit inserted eight coverage-map rows, moving the corresponding text to `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:176-177` (M3) and `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md:153-156` (M14). M14's 24-file count is the parent-state count; the round-22 commit contains 25 lesson files after adding round-22, while rounds 2, 16, 18, and 19 remain absent. The historical round-22 lesson is retained unchanged.

## Scope limits and confidence

**High confidence** in the line drift, cause, parent-to-round-22 file-count change, and continued absence of the four lesson paths: these are directly falsifiable against the specified Git objects and file lines. The external source named by M3, `fleets/claimer-mission.md:29`, is absent from the `c8b719d` lane tree (`git cat-file -e c8b719d:fleets/claimer-mission.md` failed). Accordingly, this audit verifies the README pointer/text location only; it does **not** re-open or validate the underlying severity decree or decide whether the critic's falsification was correctly rejected. No score/admission claim is made.

Report: .ufo/waves/round-23/build/RevPointers.md
