# R44Review15 — wave size and attack-share accounting

## Finding

**Actionable accounting defect (dispatch exceeds frozen 64-seat design):** the frozen wave design says `waveMinLanes: 64` and `waveMaxLanes: 128` (`.ufo/waves/round-44/wave1-dispatch.json:8-9`), but this round dispatches **66** seats, not 64 (`:16-19`: spawn 66, resume 0, total 66; `:21-25`: registry; direct parse counted 66 member entries). Therefore the actual round is within allowed min/max but is not the frozen 64-seat design. No explicit 64-seat attack-share denominator or accounting rule is present in the frozen claims (`claims.json:7-25`), so attack share cannot be independently reconciled to a stated denominator. Treat this as a design/accounting mismatch, not a claim that the wave violates configured limits.

All 66 registry members have a distinct item (`python3 -c` parse of dispatch JSON: `seats 66`, `all items unique True`); task items are assigned one per seat. There are 20 reviewers; roles comprise reviewers 20, critics 12, mutation-testers 8, executors 8, scouts 8, scribes 5, connectors 3, revenger 1, simplifier 1 (same parse). The assignment-specific item is exactly `R44Review15` in dispatch lines 180-189. I did not find a defined expected share by role or item category, so cannot label any share as numerically wrong beyond the 64-vs-66 design mismatch.

## Do-nothing / scope distinction

Frozen do-nothing evidence is about C1/C2, not seat allocation: `.ufo/waves/round-44/controls/do-nothing.txt:4-13` says eight C1 defects, C2 baseline counts 25/68/62, and missing F26/new knowledge entry. It gives no round-size or attack-share baseline. Claims C1/C2 (`claims.json:7-25`) likewise contain no seat-count acceptance criterion. Thus this finding does not falsify C1/C2 and does not establish that the task outcomes are invalid; it identifies an unaccounted frozen design delta.

## Evidence / limitations

- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `66314015122b9aa32dc40f2f1815df56624c26d1`; dispatch records base/freeze commit `6631401` (dispatch line 1, via log output).
- `python3 -c` parsed `.ufo/waves/round-44/wave1-dispatch.json`: `registry_members 66`, `counts {'spawn': 66, 'resume': 0, 'total': 66}`, role counts above, item_count 66.
- No tools installed.
- Scratch setup attempted at `$HYAKU_SCRATCH/kasegi-r44/R44Review15/`; `HYAKU_SCRATCH` was empty and `mkdir` returned `Permission denied`. No scratch was created; no scratch cleanup possible.
- No git/jj/index or production/shared files were modified by this seat. Existing unrelated worktree entries were observed at start and left untouched.

Report trailer (relative to kasegi-shokunin): `.ufo/waves/round-44/wave1/R44Review15.md`
