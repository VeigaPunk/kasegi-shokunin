# Round-60 claims erratum 1 — C2 counting command 8 `want`: 1 → 2

Filed 2026-11-04T13:36Z, after the freeze (commit `66e6241`) and after the implementation was measured on the lane tree,
before the round report.

Frozen record: `.ufo/waves/round-60/claims.json`, C2 `counting_commands[7]`:

    grep -c 'the tracker is opened as S092' corpus/SOURCES.md   # want: 1

Observed on the implemented tree (`.ufo/waves/round-60/controls/c2-lane-after-r60.txt`): **2**.

The two lines carrying the phrase, both part of the declared C2 correction:

1. the corrected lead bullet itself, under `## Leads (unopened)` — `- Big Sleep reporting beyond the tracker linked by Project Zero: the tracker is opened as S092 …`;
2. the `## Registry changes` bullet that records the old → new correction and quotes the same new text.

The frozen C2 kill rule does not reference this count and no other frozen value depends on it. The superseding value is
**2**; the command is otherwise unchanged. The defect's class and criterion: R78 — a frozen counting command's want is
measured against the frozen tree before the freeze.
