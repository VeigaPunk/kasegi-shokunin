# MutSelftestGrading — round 39 wave 2 (falsify) receipt

Seat: MutSelftestGrading (mutation tester, leaf; no subagents spawned)
Item: mutate the r39-closure.sh selftest case-line OUTPUT in sandbox copies and record that the
grading layer fails each mutant (failures>0 / non-zero exit)
Route chain captured at spawn: L1 KasegiR39 (inline spawn handoff, hyaku run 9) -> MutSelftestGrading
Axes judged: depth:verifiability
Independence: I did not author the suite under attack (wave-1 landed it); pure attack seat.
Deliverable: .ufo/waves/round-39/wave2/MutSelftestGrading.mutations.txt (written, 14917 bytes)
Run window: 2026-10-26T21:5xZ – 22:0xZ (UTC)

## What I did (commands run, actual output)

1. Read the frozen claims first: `.ufo/waves/round-39/claims.json` and `claims-erratum-1.md`
   (read-only; not edited). Verification ref per E4: Y = 5006097a84305267c9a3e8c1e1d560e60fe41d37
   (= lane HEAD; `git diff --name-only J Y` = the receipt alone, verified), J = 46c66c268502abd1b2c342fc71bf88ccf721845b
   (read from the receipt's `export-ref=`).

2. Verified the attacked bytes are the receipt-bound bytes:
   `sha256sum corpus/instruments/r39-closure.sh` ->
   `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` = the receipt's
   `suite-sha256=`. The battery therefore attacked exactly the landed, pinned bytes.

3. Read the suite's grading machinery at HEAD (judge_selftest_report lines 1634-1660, emitter
   st_verdict line 1367, run_selftest loop line 1665, g2_graded lines 418-447) before mutating.

4. Built the frame in scratch S=/fast/scratch/hyaku/kasegi-r39/MutSelftestGrading:
   pristine copy (digest-equal to the lane bytes), fixture clones lane-Y and lane-J
   (`git clone --no-hardlinks`, detached checkouts inside the fixtures, toplevels asserted,
   `status --porcelain` empty). Deviations `--lane`/`--scratch-root` were REQUIRED and are printed
   by the suite itself (`deviation=non-default --lane`, `deviation=non-default --scratch-root`):
   the live lane worktree holds concurrent wave-2 untracked files which red the pinned r37 suite's
   E9 status limb inside G8's positive limb (measured: `E9 payload=…status-dirty=6… closed=0`,
   r37 `closed=13/14 exit=1`) and would confound every run.

5. Controls (all real output in the deliverable):
   - C0 baseline, pristine @ Y on lane-Y: `selftest cases=8 failures=0`, eight graded
     `positive=pass … verdict=pass` lines (G1 4/4, G2 8/8, G3 2/2, G4 6/6, G5 4/4, G6 4/4,
     G7 3/3, G8 3/3), `judge=own-report accepted=1`, six forgeries rejected, exit 0.
     -> the frozen C1 selftest limb REPRODUCES on the landed bytes.
   - C-J collateral control, pristine @ J on lane-J: G2 red `receipt=0` (the documented E4 J-run
     shape), `cases=8 failures=1`, `judge=own-report accepted=0`, exit 1.
   - C-ENV, pristine @ Y on the REAL lane: exit 1, G8 fail-branch; direct r37 probe shows the red
     is `status-dirty=6` (wave-2's own untracked files), head-match=1 — environmental, not a
     landed-bytes defect.
   - C9 do-nothing control, pristine @ Y re-run after all mutants: `cases=8 failures=0`,
     accepted=1, exit 0 — no state pollution.

6. Mutations (single-point edits in sandbox copies; sha256 + exact diff per mutant in the
   deliverable), each run with `--selftest --export-ref Y --lane lane-Y --work … --scratch-root …`:
   - M1 `positive=pass` -> `positive=fail`, verdict=pass kept (sha 15f72ed4…): exit 1,
     `cases=8 failures=1`, `judge=own-report accepted=0`; report forensics: 7 case lines carry
     `positive=fail … verdict=pass`. KILLED.
   - M2 `verdict=` field removed (sha 0c10f83f…): exit 1, accepted=0; verdict-pass-lines 8 -> 0.
     KILLED.
   - M3 duplicate case line (sha b2bac99b…): exit 1, accepted=0; case-lines 8 -> 15, per-id dup 2.
     KILLED.
   - M4 reduced to 7 case lines, G8 suppressed, summary still claims 8 (sha 19fbe21b…): exit 1,
     accepted=0; case-lines=7, G8-lines=0. KILLED.
   - M5 bonus probe, selftest loop reduced to 7 checks (sha 00553743…): exit 1, accepted=0,
     `cases=7 failures=1` AND `selftest problem=cases=7 expected=8` — two independent detection
     layers. KILLED.
   In every mutant run the suite reported failures>0 AND non-zero exit, as the item requires.

7. Attribution (the G2 digest collateral is by design — a mutated copy's sha256 can never equal
   the pinned digest, so G2's anti-tamper limb reds in every mutant run): each mutant's G2 payload
   shows `digest-match=0` with every other limb green (receipt=1, sentinel=1, export-ref=1,
   ancestor=1, diff-clean=1, export-suite=1, run-lines=8) — collateral isolated. The confound-free
   grading proof is the synthetic replay: the PRISTINE judge function (suite sourced, main guard
   skips main) applied to the ACCEPTED C0 baseline report carrying exactly one mutation signature:
   baseline-unmodified -> accepted rc=0; M1/M2/M3/M4 signatures -> rejected rc=1 each. For M1 the
   top-gate counts all pass (cases=8, verdicts=8, summary=1, dup=1), so the rejection comes solely
   from the per-id `positive=pass` requirement — the exact mutation signature.

## Findings

- NO SURVIVORS: all four assigned mutations (plus the bonus loop probe) are killed by the grading
  layer; a summary-only or lying-summary line never satisfies a case. The C1 selftest grading is
  not vacuous.
- Environmental finding for the round (C-ENV): while wave-2 untracked files sit in the lane, the
  C1 selftest counting command cannot print `cases=8 failures=0` on the REAL lane (r37 E9
  status-dirty counts them; measured status-dirty=6). The green window is transient — wave-1
  measured it on a then-clean tree. Any wave-2 re-verification of C1 on the live lane must commit
  or use a clean export-clone and say so. This is a measurement-environment property, not a
  landed-bytes defect; the claims' own J-run/Y-run semantics (E4) are unaffected.
- Design observation (strength, not defect): the G2 digest limb makes any mutated suite copy
  self-identifying (digest-match=0) — suite tampering cannot hide behind a green run.

## Controls run (do-nothing)

- C0 pristine baseline and C9 post-mutant re-run: both `cases=8 failures=0`, accepted=1, exit 0.
- C-J collateral control and C-ENV real-lane control: reds fully explained (receipt=0 at J;
  status-dirty=6 live), no unexplained red anywhere.

## Tooling

No tools installed or upgraded (operator tooling authorization 2026-10-19 acknowledged; bash, git,
awk, sed, sha256sum, python3 sufficed; pacman untouched; no service touched; no network fetches).

## Write scope / cleanup

Writes: this receipt, MutSelftestGrading.mutations.txt (beside it), and scratch
/fast/scratch/hyaku/kasegi-r39/MutSelftestGrading (removed before yield, after the deliverables
were landed). Lane tree, fleet root, shokuknow, sibling repos: read-only. No mutating git/jj
command anywhere: the only git writes were `git clone --no-hardlinks` into scratch and detached
checkouts INSIDE those scratch fixture clones (toplevel-asserted); the lane suite file's sha256 is
identical before (2856a210…) and after all work, with zero tracked modifications
(`git status --porcelain -- corpus/instruments/r39-closure.sh` empty). Disk guard green
throughout (/fast 610G avail, /home 586G avail).

Report: .ufo/waves/round-39/wave2/MutSelftestGrading.md
