# ScribeLessonAmend — scoped findings report (wave 2)

Seat: `L1Kasegi26.ScribeLessonAmend` (leaf; no subagents spawned). Item:
amend `corpus/lessons/round-26.md` (sole owner) with the four wave-1 open
items' resolution and the final measured counter table; report appended lines;
output `.ufo/waves/round-26/wave2/z2.md`.

## Behavior

- Appended `## Integration closure (2026-10-25)` block to
  `corpus/lessons/round-26.md` (lines 149-171; file 148 → 171 lines). No
  earlier block altered — the block was inserted after the pre-existing final
  line (former line 148), verified by re-read of lines 140-171.
- Block records all four wave-1 open items with resolution: (1) `c1-receipt-index.txt`
  regenerated at landed digest `3fc0d751…`, `selftest cases=15 failures=0 exit=0`;
  (2) census E09/E11 cleared by cadence-only S040/S041 recheck cells with
  final-URL/UA prose moved to `## Registry changes`; (3) README/SCORECARD F11
  entry names aligned to actual unsuffixed filenames; (4) `knowledge-expected.txt`
  regenerated to 39 entries.
- Appended the final measured counter table: C1a 1; C1b 1; C1c BRE 0; C1d
  deletion exit 1 + `missing=<name>`; C2 awk 11; precise S041-citing 2;
  census exit 0; frontier 14/14 exit 0.

## Gates

- Sole-owner scope: edit confined to `corpus/lessons/round-26.md`.
- No claims.json / round-25 files touched; no production edit outside the lane's
  owned paths; no VCS mutation; no installs (no tooling change needed — record:
  none).
- Read-only verification of resolution evidence (no reruns): receipt index
  (`c1-receipt-index.txt`), SOURCES.md Registry changes S040/S041 cells,
  README § Frontier F11 row, SCORECARD round-26 C2 row, knowledge-expected.txt
  count (39), c1-live.json expect=present/39.

## Touched surfaces

- `corpus/lessons/round-26.md` — appended lines 149-171 (23 lines).
- `.ufo/waves/round-26/wave2/z2.md` — output (new).
- `.ufo/waves/round-26/wave2/ScribeLessonAmend.md` — this report (new).

## Out-of-scope

- No counter commands rerun; measured-at-integration values recorded as given
  (census exit 0; frontier 14/14; live audit 39/39; deletion exit 1; registry
  grep 1; selftest line 1; fix-control 0; awk 11; precise S041-citing 2).
- No edits to §Fixes / §Routed debt blocks (historical open-item text retained,
  per "do not alter earlier blocks").

## Findings

- All four open items are resolved in the landed tree as claimed; the closure
  block records them with file/line evidence anchors.
- Counter table matches the assignment-specified values exactly.

## Artifact paths

- Append target: `corpus/lessons/round-26.md` (lines 149-171).
- Output: `.ufo/waves/round-26/wave2/z2.md`.
- Report: `.ufo/waves/round-26/wave2/ScribeLessonAmend.md`.
