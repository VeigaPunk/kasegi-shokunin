# RevDensityGuard — round 28, wave 1 — density-axis guard receipt

Recorded 2026-10-25T17:33Z (UTC). Lane root /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Scope: density axis (score 9) guard per wave item — density census vs frozen before, base-relative
git diff over SKILL.md / corpus/knowledge/ / corpus/README.md, R6 append-only check. Leaf seat:
no subagents, no background jobs, no tool installs, no VCS writes, no production edits.

## State label

- SKILL.md: **POST-STATE, final** — worktree sha256 `125be37d85ffe6be30a3c372b52d96d8074e3c4d7f4baf835d0f5aed5f56cca6`
  equals the "after" sha in `.ufo/waves/round-28/receipts/ScribeSkillGate.txt` (written 17:28Z);
  ScribeSkillGate receipt present. 1032 → 1035 lines.
- corpus/README.md: **mid-flight at snapshot** (+26 lines at 17:26:54Z → +28 at 17:30:48Z,
  ScribeReadmeC2 still landing). Not density-relevant (instrument reads SKILL.md only) but named
  per item; L1 must re-run the diff post-assemble.
- corpus/knowledge/japanese-domestic-disclosure-workflow.md: **new, untracked** (ScribeEntryC2
  receipt present). Not density-relevant.
- Round-28 receipts dir: 30 files at 17:30:48Z.

## Instrument identity

`corpus/instruments/density.py`, sha256 `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`;
`git diff c9f8b115a098c65356e4b3b6048af45a37ab8395 -- corpus/instruments/density.py` is empty;
last commit touching it is eb5b590 (round 15, 2026-09-28). Same bytes measured r25 → r28, so the
cross-round comparison is valid.

## Measurements (all runs by this seat, exit 0, stdlib python3)

| state | tree | mean dens | blocks | path-cites |
|---|---|---:|---:|---:|
| dispatch "frozen before" | a04cc6c^ (round-25 tip) — re-measured | **154.0** | 19 | 652 |
| actual wave before | base c9f8b11 (worktree was byte-identical: `git show c9f8b11:SKILL.md \| diff -q - SKILL.md` clean, checked 17:19Z) | **150.3** | 20 | 652 |
| post-landing (final SKILL.md) | worktree at 17:29–17:33Z, sha `125be37d…` | **160.2** | 20 | 656 |

Reconciliation of 154.0/19 vs 150.3/20: round-26 commit a04cc6c appended 9 lines, 0 deletions to
SKILL.md — a new `## Gates & probes registry` section (census block 18) inserted above the Cited
paths appendix. Exact arithmetic closure: (154.0×19 + 80.0)/20 = **150.3**; cites unchanged (new
block cites=0). Round-27 touched no corpus bytes (SCORECARD round-27 row). So the dispatch's
frozen before (154.0/19/652) describes the round-25 tip, **not the round-28 freeze base**.

## Findings by severity

### F1 — MEDIUM (pre-existing, round-26/27 origin; NOT a wave-1 write) — stale density before-record
The last SCORECARD-recorded density (154.0 / 652 cites / 19 blocks, rows "held r24/r25", and
re-frozen into this wave's dispatch) does not describe any committed tree after a04cc6c. SCORECARD
round-26 row states it was measured "before the C1 registry-row edit to SKILL.md lands"
(SCORECARD.md:578); the round-27 row carried "unchanged" without re-measuring (SCORECARD.md:601).
Consequences at the freeze base: (a) recorded before ≠ actual before (150.3/20/652); (b) the
r26-inserted block measured **80.0 < BAR_R15 142.5** — below the recorded new-block admission bar —
and no SCORECARD row records it. This is a record-honesty defect in SCORECARD r26/r27 rows and in
the round-28 dispatch freeze, not a wave-1 harm. Wave 1 must NOT be scored against 154.0/19.

### F2 — LOW-MEDIUM (wave-1, ScribeSkillGate) — R6 letter violation, mid-file insert
The landed SKILL.md change is +3/−0: (1) one table row added at line 982, at the end of the
round-26 `Gates & probes registry` table — a **mid-file insertion**, neither an EOF append nor a
same-line suffix; (2) blank + one-sentence note appended at EOF (compliant). The row insert shifts
every pre-existing line ≥983 by +1, against the L1 ownership map ("append at end per R6; never
shift lines") and R6's letter (QUALITY.md:40). Verified impact:
- The motivating line `~/Projects/bounties/ops/{validate,registry-check,reroute-drill,check-freshness}.mjs`
  moved **1007 → 1008** (base → current). Note: the pin `SKILL.md:1000` in
  `corpus/instruments/resolve-dispatch-fixtures.json` (lines 159 and 161 — the only production
  references to SKILL.md:980–1039) was **already inconsistent with base** (line 1007 there), so the
  staleness predates wave 1; the wave's +1 widens it.
- No automated verdict flips: the fixture's runtime cites are embedded literals (`extra_cites` /
  `extra_files`), the `SKILL.md:1000` strings are `why`/comment documentation only.
- `.ufo/waves/round-28/claims.json` and `wave1-spec.json` contain **zero** `SKILL.md:NN` anchors —
  frozen predicates unaffected.
- ScribeSkillGate's own receipt discloses the geometry transparently ("+1 at line 982 … nothing
  above it changed") and does not claim append-at-end for the row.
Density effect of the insert is positive (block 18: 80.0 → 233.3), so no density harm — the defect
is procedural anchor drift. L1 disposition options: accept with the drift recorded beside the
fixture, or relocate the row append at EOF (owner's call; this seat edits nothing).

### F3 — INFO — snapshot-in-flight files
corpus/README.md +28 lines and corpus/knowledge/japanese-domestic-disclosure-workflow.md (new)
were still landing / freshly landed at snapshot time; numbers above cover SKILL.md only.

### F4 — INFO — outside this axis, flagged for owners
SKILL.md line 1035 (the appended note) asserts an **erratum to the frozen C1 `corpus_disclosure`
cell** ("zero backticked anchored `~/Projects/bounties/` citations exist lane-wide … no
verdict-class movement"), pointing at `.ufo/waves/round-28/claims-erratum-1.md` (exists, 2315 B).
Truth of that erratum and of "no verdict-class movement" belongs to the C1 no-harm seats
(frozen disclosure said 4 corpus bounties citations classify LOST-RECORDED); this seat verified
existence of the pointer file only, not the claim. Related: SKILL.md bytes changed after the
claims freeze, so any anchorcheck base pin frozen at c9f8b11 will see new bytes — C1 seats' scope.

## Density verdict

**No density drop attributable to wave 1 as measured.** Post-landing 160.2 / 20 blocks / 656 cites
vs base-state 150.3 / 20 / 652 (+9.9 mean, +4 cites) and vs the stale dispatch before 154.0/19
(+6.2). Both edited blocks are density-positive (block 18: 80.0 → 233.3; block 20: 155.6 → 200.0
absorbing the 2-line note); block 19 (Cited paths) content untouched (diff hunks at line 982 and
EOF only). No block below BAR_R15 142.5 remains. Axis harm: none observed. Procedural harm: F2,
named above.

## Named touched files (watched set, 17:30:48Z snapshot)

- `SKILL.md` — +3 −0 (final; hunks at 982 and 1034–1035)
- `corpus/README.md` — +28 −0 at snapshot (in flight)
- `corpus/knowledge/japanese-domestic-disclosure-workflow.md` — new (untracked)

## Exact re-run commands for L1 post-assemble (from lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/density.py SKILL.md --label r28-guard-final
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff c9f8b115a098c65356e4b3b6048af45a37ab8395 --stat -- SKILL.md corpus/knowledge/ corpus/README.md && git status --porcelain -- corpus/knowledge/
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff c9f8b115a098c65356e4b3b6048af45a37ab8395 -- SKILL.md | grep -cE '^-[^-]'   # expect 0
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff c9f8b115a098c65356e4b3b6048af45a37ab8395 -- SKILL.md | grep '^@@'          # every hunk must be EOF-region for R6; the 982 hunk is F2
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -rnE 'SKILL\.md:(9[89][0-9]|10[0-3][0-9])\b' SCORECARD.md LOG.md corpus/
```

Acceptance: density exit 0; mean ≥ 150.3 (base-state before) with no new block < 142.5;
zero deletions in SKILL.md; every `SKILL.md:98x–103x` production reference reconciled with the
post-F2 line numbers (or F2 disposition applied).

## Tooling record

No tool installed or upgraded (channel n/a). Used only: python3 (stdlib) for the committed
instrument, git read-only (show/diff/log/status/rev-parse), coreutils.

## Honesty notes

All numbers above are from runs executed in this session at the stated trees; the 154.0/19/652
"dispatch before" was re-measured by this seat on `a04cc6c^:SKILL.md`, not taken on faith. Block-19
per-column values quoted for base state come from the 17:19Z run; its content is diff-verified
unchanged post-landing. README/knowledge numbers are snapshots, explicitly not final.
