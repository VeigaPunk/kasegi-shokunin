# ExecArchiveChecks — base no-harm guard (round-39, wave1)

Seat: ExecArchiveChecks (leaf executor). Axis touched: depth:verifiability (no-harm
witness only — this seat adds no claim surface). Base
`480b1a505a2dfc14a4f718d16d63808247214d0a`; lane HEAD at run
`d65d823e7c84813c192b20ee757a8761f878a61f` (round-39 wave1 spec/dispatch).

Deliverable: `.ufo/waves/round-39/wave1/ExecArchiveChecks.base-gates.txt`
— 497 lines, sha256 `ca3d8fb2b63f4fe20fef82b8a8e8c0e69dd6d75ef344afd8d4758d2d6357b0e1`
(copied byte-exact from scratch; the transcript is the landable evidence, no receipt
scaffolding inside it).

Scratch: `/fast/scratch/hyaku/kasegi-r39/ExecArchiveChecks/` (TMPDIR + both `--work`
dirs bound there), removed before yield.

## 1. Commands run and their actual results

All run from the lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin` with
`TMPDIR=/fast/scratch/hyaku/kasegi-r39/ExecArchiveChecks`. Disk guard was green before
the pass (`/fast/scratch/hyaku 24% use, 610.6G free`).

| # | command | exit | headline |
|---|---|---|---|
| 1 | `python3 corpus/instruments/anchorcheck.py SKILL.md` | 0 | `16 in-range cite instances, 0 bad; 16 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` |
| 2 | `python3 corpus/instruments/density.py SKILL.md --label r39` | 0 | `1114 lines, 27 blocks`, **mean dens 233.1**, 768 path-citation instances |
| 3 | `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json` | 0 | `guard cases=3 failures=0`, `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3` |
| 4 | `python3 corpus/instruments/limb-mutation-check.py` (bare) | 2 | `--ledger is required` (instrument is runnable only in its documented form) |
| 5 | `bash corpus/instruments/r38-closure.sh --export-ref 480b1a5… --work $S/work-live` | 1 | `closed=5/8 exit=1` |
| 6 | `bash corpus/instruments/r38-closure.sh --selftest --export-ref 480b1a5… --work $S/work-selftest` | 1 | `selftest cases=8 failures=3` |
| 7 | `git show 480b1a5…:corpus/instruments/r38-closure.sh \| sha256sum` | 0 | `85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6` = the `suite-sha256=` line both runs printed = worktree bytes |
| 8 | `git status --porcelain` / `-uno` | 0 | `-uno` **empty** (tracked tree clean); 7 untracked L1 dispatch artifacts under `.ufo/waves/round-39/` |
| 9 | `ls -d /fast/scratch/hyaku/kasegi-r3*` | 2 | `kasegi-r39`, `kasegi-r39-l1` only; **kasegi-r37 and kasegi-r38 absent** |

## 2. Which r38-suite G lines are green at base

From run 5 (`closed=5/8 exit=1`), per-line `closed=` is the authoritative reading:

| G | base payload | closed at base |
|---|---|---|
| G1 front doors | `province-correction=1,readme-correction=1,province-fence=closed,readme-fence=closed,declared-blocks=2,declared-ok=1` | **1 (green)** |
| G2 judged-head binding | `…,diff-clean=0,…` (all other limbs 1) | 0 (red) |
| G3 pending-marker resolutions | `resolutions-section=1,line-tokens=8,added-pending=1,added-placeholders=0,diff-read=ok` | 0 (red) |
| G4 results.json seats | `dispatches=1,pairs=1,seats-ok=1,read=ok` | **1 (green)** |
| G5 judged-head-by-reference | `round38-section=1,final-lane-commit-lines=0,correction=1,f3246559=2,anchor-ancestor=2` | **1 (green)** |
| G6 scratch quiescence | `r36=absent,r37=absent,r38=absent,work=outside,tolerated=none,read=ok` | **1 (green)** |
| G7 considerthese ledger | `filled-section=1,correction=1,proposal-rows=7,missing=0` | **1 (green)** |
| G8 r37 carry-over | `r37-suite=1,r37-closed=0,r37-exit=1` | 0 (red) |

Green at base: **G1, G4, G5, G6, G7**. Red at base: **G2, G3, G8** — exactly the
three limbs the round-38 suite can only satisfy on a round-38-judged tree, so
`closed<8/8 exit=1` at base is structural, not a defect. Each red limb's payload
names the single failing clause (`diff-clean=0`, `added-pending=1`, `r37-closed=0`),
so the base reading discriminates.

## 3. Selftest at base (run 6)

`selftest cases=8 failures=3`, exit 1. Per-case positives: G1 pass, G2 fail, G3 fail,
G4 pass, G5 pass, G6 pass, G7 pass, G8 fail — the same five/eight split as run 5, so
the positive limb tracks the live limb. Mutant limbs stayed green on red positives
(all 26 mutants rejected, every rejection naming the reopened limb):

- G1 3/3, G2 6/6, G3 2/2, G4 2/2, G5 4/4, G6 5/5 (+2 accepted clean controls), G7 2/2, G8 2/2.
- `selftest judge=own-report accepted=0` (own report is red at base — the judge does not
  accept a red run), `forged-summary/forged-caselines/forged-failed-cases/forged-detail-free/forged-7-cases rejected=1` (5/5).
- G6 accepted two clean controls whose only residue sat inside **this seat's own
  `--work`** (`…/ExecArchiveChecks/work-selftest/mut/g6-control/kasegi-r38/seat`), i.e.
  the r39 `--work` tolerance behaves as designed and does not mask a foreign leftover.

## 4. Discrepancies against the item's expectations (recorded, not silently dropped)

1. **`git status --porcelain` is not empty** — 7 untracked entries, all L1 round-39
   dispatch artifacts (`.ufo/waves/round-39/{items2.py,build-wave2-final.py,kasegi-r39-build.ready,kasegi-r39-build.ready.dispatched,wave1-plan.err,wave1-run.err,wave1/}`).
   None written by this seat. `git status --porcelain -uno` is empty, so the *tracked*
   tree is clean; the C1 kill-rule phrase "lane working tree not clean at filing" must
   be read as tracked-clean plus wave-dir artifacts, or it would fire on the L1's own
   dispatch files.
2. **HEAD is not base.** HEAD is `d65d823`; `git diff --name-only 480b1a5… HEAD -- corpus/ SKILL.md PROVINCE.md LOG.md SCORECARD.md SHONEN.md`
   prints nothing, so every instrument above ran on base bytes. The r38 suite's own
   `suite-sha256=85d33ea9…` equals `git show 480b1a5…:corpus/instruments/r38-closure.sh | sha256sum`,
   proving the executing bytes are the base commit's bytes, not a working-tree edit.
3. **`r39-closure.sh` is absent at base** (`ls` → no such file), as the C1 before-control
   records. Runs 5–6 therefore exercise the *committed r38* suite; the C1 counter that
   must print `closed<8/8 exit=1` at base is the new r39 suite, which no seat has landed
   yet. This seat cannot measure that instrument and does not claim to.
4. **`limb-mutation-check.py` bare form exits 2**, not a green run; the ledger form is
   the runnable one and is what run 3 records. Both are in the transcript.

## 5. Risks

- G8 red at base is driven by `r37-closure.sh` on the base export (`r37-closed=0,
  r37-exit=1`). If the r39 suite re-uses a carry-over limb of the same shape, its base
  redness will come from the same cause and should not be read as r39 damage.
- The transcript embeds the full 324-line anchorcheck output, including 306
  `LOST-RECORDED` lines. Those are the standing lost-tree citations, unchanged from
  prior rounds (`PIN-BROKEN=0`, `ORIGIN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`), and are
  baseline noise, not new breakage.
- The base reading is a snapshot: sibling wave1 seats were writing under
  `.ufo/waves/round-39/` while it ran. Nothing they touch is read by runs 1–7 except
  live scratch roots (G6) and lane git refs, both of which were consistent at run time.

## 6. Files changed

- `.ufo/waves/round-39/wave1/ExecArchiveChecks.base-gates.txt` (new; 497 lines; sha256
  `ca3d8fb2b63f4fe20fef82b8a8e8c0e69dd6d75ef344afd8d4758d2d6357b0e1`)
- `.ufo/waves/round-39/wave1/ExecArchiveChecks.md` (this receipt)

No lane tracked file, no fleet-root file, no `MANIFEST.json`/`templates/`/`scripts/`/
`.ufo/state/`, no sibling repo, no source tree was written. No git/jj mutation was run
(`git status`, `git show`, `git diff`, `git rev-parse`, `git log` only). No tool was
installed or upgraded, so there is no tool/version/channel row to record. Scratch
`/fast/scratch/hyaku/kasegi-r39/ExecArchiveChecks/` removed before yield.

## 7. Checks the L1 should run after integration

- `bash corpus/instruments/r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a`
  → must print `closed<8/8 exit=1` (this seat's run 5 is the r38 analogue).
- `bash corpus/instruments/r39-closure.sh --selftest --export-ref 480b1a5…` → `cases=8`,
  red positives at base, every mutant rejected.
- `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json`
  → still `limbs=13 killed=13 survivors=0` after the new suite lands.
