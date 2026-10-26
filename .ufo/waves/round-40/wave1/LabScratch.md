# LabScratch receipt (round 40, wave 1)

Deliverable: `.ufo/waves/round-40/wave1/LabScratch.txt` (51 lines, sha256 `4d04e6bb24245b89b60fa91ad75f0e37a0eb43f301ecd6c0cca4d866fafc4c52`) holds the full transcripts. No lane edits. No tools installed.

## Observed (all 2026-10-26, lane HEAD 5e985b74075dd3813a63d7750966bf8abf693465, `--export-ref 8371e7ac9f32cae5ed72f8c28205634603f836fa`, `--work $S/w<X>`)

Before: `ls -d /fast/scratch/hyaku/kasegi-r3*` found nothing.

| run | scratch state | G6 line | overall |
|---|---|---|---|
| A 21:19:01Z | no stray | `G6 payload=r37=absent,r38=absent,r39=absent,work=outside,tolerated=none,read=ok closed=1` | `closed=6/8 exit=1` |
| B 21:19:02Z | `kasegi-r39-stray/seat/leftover.txt` | identical to A: `r39=absent ... closed=1` | `closed=6/8 exit=1` |
| C 21:19:03Z | `kasegi-r39/stray-seat/f` (exact name) | `G6 payload=r37=absent,r38=absent,r39=present,work=outside,tolerated=none,read=ok closed=0` | `closed=5/8 exit=1` |

## Findings
1. G6 is a live read of the host scratch root. In `r39-closure.sh` (lines 879-913) it checks only the exact directory names `$sroot/kasegi-r37`, `kasegi-r38` and `kasegi-r39`. This is source-confirmed at lines 880-913, not just inferred from the run output.
2. The `kasegi-r39-stray/` sibling the assignment named is **not detected**. G6 stays `closed=1` with `r39=absent`, so a stray sibling with a different name passes silently. r40's H6 must scan by prefix, for example `kasegi-r39*` and `kasegi-r40*`, because the exact-name check misses it.
3. An exact `kasegi-r39/` entry flips G6 to red (`r39=present`) and costs one check (6/8 becomes 5/8). That is the environment coupling: the same ref gives different closures depending on host scratch state.
4. The ref is the same in all three runs, and the G6 outcome differs only with scratch state. `suite-sha256=2856a210...222b` was identical in the three runs.
5. With no stray, the export of the r39 head prints `closed=6/8 exit=1` on this host. G2 is red (`ancestor=0, diff-clean=0, closed-line=0, selftest-summary=0, final-lane-commit=0`) and G8 is red (`r37-closed=0, r37-exit=1`). G8 runs the pinned r37 suite, which takes its own live reads against the lane. The lane is at HEAD 5e985b7 with a dirty tree (15 porcelain lines of untracked wave files), not at Y. That is a second host coupling, and it is why this run does not reproduce the final r39 receipt value `closed=7/8`. I did not isolate which G2 clause fails beyond the payload counters.
6. `df -h /fast/scratch/hyaku` after cleanup: `/dev/nvme1n1p2 804G size, 201G used, 604G avail, 25% /fast`. Disk guard: `/fast/scratch/hyaku 25% 603.0G free`, `/tmp 3% 125.2G`, `/var/tmp 35% 585.2G`. Before the run it showed 26% and 601.9G free.

## Cleanup
Strays `kasegi-r39-stray/` and `kasegi-r39/` removed (`ls -d /fast/scratch/hyaku/kasegi-r3*` found nothing afterward). The scratch dir `/fast/scratch/hyaku/kasegi-r40/LabScratch` is removed after this receipt is written.
