# R46bW2ExecRerunC1 — re-run of the C1 counting chain (round 46 attempt 2, wave 2)

VERDICT: BROKEN

Seat: leaf executor, wave 2, round 46 attempt 2. Item: re-run the C1 counting chain at
fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4 vs base 04af9bc92229232ea5cce8b32bfe59dd969eb26d
(git archive both): battery `--counter c1` (expect uncaught=0), the c2 twin (expect
uncaught=0), the extended selftests c1/c2 baselines (expect failures=0), and the plain
lines (frontier rows, SOURCES rows, knowledge files, absence sweep). All commands below
were re-run by this seat in scratch exports; nothing is taken from a receipt on trust.

## Tree identity (resolved first, it matters)

- `fe0f56b` "round-46 (attempt 2): freeze claims C1 counter-mutation coverage + C2 frontier
  F29, counters v1 (mutbat, f29-gate), S074 capture + manifest-a2, R50 receipt, controls" —
  the FREEZE commit. The item's parenthetical "(integration of wave 1)" does not match this
  hash: the wave-1 integration commit is HEAD `96379ae` "round-46 (attempt 2): wave-1
  integration — F29 entry + S074 row + admission blocks + ledger dispositions; instruments
  (selftests 83/147, selftest-f29, mutbat v1.1, f29-gate v1.1, c2-gate v1.3); errata E1-E4...".
- This seat ran the chain at ALL THREE trees (git archive exports in seat scratch, now
  removed): base `04af9bc` → `base/`, freeze `fe0f56b` → `integ/`, integration `96379ae` →
  `integ2/`. The claims' after-state ("final lane revision") is only reachable at `96379ae`;
  at `fe0f56b` the round's work is not yet in the tree — exactly as the frozen claims'
  `freeze_tree_reading` predicts, so before-values at the freeze are confirmation, not
  falsification. The broken limb below is at the integration commit.

## F1 — C1 battery c2 twin BROKEN at the integration commit (the item's headline)

Command (claims `counter_cmd` shape, at the `96379ae` export):

    $ cd <integ2> && python3 -B corpus/instruments/r46-mutbat.py --root <integ2> \
        --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch>/w-integ2 \
        --counter both --jobs 8

Quoted output (tail; full 20 c1 mutant lines in F2):

    mutbat counter=c1 mutants=20 caught=19 equivalent=1 uncaught=0 baseline_failures=0
    mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1
    BATEXIT=1

Expected `uncaught=0` for the c2 twin; got `BASELINE-DIRTY baseline_failures=-1` — the
battery found no `failures=` token because the tree's own extended c2 selftest crashes at
import. Root cause, committed bytes at `96379ae`
(md5 7a9f7c8b851a6a83913d71732ccdc495, byte-identical to the export):

    $ python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure .../L1/pure2
    Traceback (most recent call last):
      File ".../integ2/corpus/instruments/r46-counters-selftest-c2.py", line 68, in <module>
        EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # the counter's CONTENT_EXEMPT: ...
        ^^^^^^^^^^
    NameError: name 'C1_ENTRIES' is not defined
    EXIT=1

The committed file uses `C1_ENTRIES` at line 68 and defines it at line 69:

    68: EXEMPT_ENTRIES = C1_ENTRIES | {LEDGER}  # ...
    69: C1_ENTRIES = {"claim-gates.md", "claim-package-contract.md"}  # ...

The fix exists ONLY uncommitted in the live lane: `git status --porcelain` shows
` M corpus/instruments/r46-counters-selftest-c2.py`, and the live bytes (md5
131134cefcf70d455ce4c5df60da25d0) have the definition at line 68 BEFORE the use at line 69.
So the wave-1 integration commit shipped a doa instrument and the claim's after-state
("the extended selftests ... keep `failures=0` baselines at the final revision";
battery c2 `uncaught=0`) does not hold at the tree under attack. The same crash is visible
in the working-tree receipt `.ufo/waves/round-46/attempt2/controls/final-battery.txt`
(untracked), which prints `NameError: name 'C1_ENTRIES' is not defined` for
"== selftest c2 (extended+ledger)".

Consequence per the frozen C1 kill_rule: "C1 fails if either battery summary at the final
revision prints uncaught>0 or baseline_failures!=0" — baseline_failures=-1 ≠ 0 for c2.

## F2 — the c1 limb itself HOLDS at the integration commit

Same battery invocation as F1, c1 part, full per-mutant output:

    mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=27 verdict=caught
    mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=9 verdict=caught
    mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M04-L2-one-reground baseline_failures=0 mutant_failures=26 verdict=caught
    mutant=M05-L3-shape-loose baseline_failures=0 mutant_failures=3 verdict=caught
    mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M08-L4-bytes-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M09-L4-planted-dropped baseline_failures=0 mutant_failures=4 verdict=caught
    mutant=M10-L4-symlink-ok baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M11-L5-prefix-flip baseline_failures=0 mutant_failures=5 verdict=caught
    mutant=M12-L5-restore-dropped baseline_failures=0 mutant_failures=3 verdict=caught
    mutant=M13-L6-control-dropped baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M14-L6-exit-ignored baseline_failures=0 mutant_failures=0 verdict=equivalent
    mutant=M15-L7-always-true baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M16-min-rows-5 baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M17-min-token-1 baseline_failures=0 mutant_failures=2 verdict=caught
    mutant=M18-anchor-dirs-wide baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M19-L2-eq-relaxed baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M20-syntax-ignored baseline_failures=0 mutant_failures=1 verdict=caught
    mutbat counter=c1 mutants=20 caught=19 equivalent=1 uncaught=0 baseline_failures=0

caught(19) + equivalent(1) == mutants(20), uncaught=0, baseline_failures=0 — the exact
after-state shape of claim C1 for c1. Every before-uncaught mutant (M06, M07, M13, M18,
M19, M20) is now caught by the extended selftest's new dedicated cases; M14 carries the
committed proof. Extended c1 selftest baseline at the same tree:

    $ python3 -B corpus/instruments/r46-counters-selftest-c1.py --pure .../L1/pure2 \
        --work <scratch>/w-st-c1-integ2 --jobs 8
    residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
    selftest cases=83 failures=0
    EXIT=0

cases=83 > 76, failures=0 (matches the commit message "selftests 83/147" and the after-
claim "cases>76 failures=0"). New dedicated cases observed in the output, incl.
`L3-home-path-in-trailing-comment`, `L3-absolute-home-path-in-trailing-comment` (M06/M07
killers), `L2-newly-gated-entry-not-gated-at-base` (M19), `X-anchor-dir-outside-the-whitelist`
(M18), `L1-cd-target-is-not-valid-bash` (M20), `L6-anchor-escapes-the-scratch-copy`,
`L6-section-ids-not-unique` (M13/M14 region). The equivalents default map
(`corpus/instruments/r46-mutant-equivalents.json`, 4 entries: M14, G6b, G7a, G7c) resolves;
both proof files exist and are non-empty
(`r46-mutant-equivalents/M14-L6-exit-ignored-receipt.txt` 682 bytes, tail
"m14-equivalence trees=15 differing=0";
`r46-mutant-equivalents/G6b-G7a-G7c-equivalence-probe.txt` 3560 bytes, tails
"G6 readings differing between frozen and mutant: 0" / "G7 readings differing between
frozen and the two mutants: 0"). Deep falsification of the equivalence arguments is
outside this item; existence/non-emptiness/internal consistency verified.

## F3 — the freeze tree `fe0f56b` reads the before-state everywhere (as the claims predict)

Plain lines, all three exports (commands exactly as in the claims' `plain` blocks):

    base 04af9bc:      frontier-rows: 28  sources-rows: 73  knowledge-md: 65  absence-files: 2
    freeze fe0f56b:    frontier-rows: 28  sources-rows: 73  knowledge-md: 65  absence-files: 2
    integ2 96379ae:    frontier-rows: 29  sources-rows: 74  knowledge-md: 66  absence-files: 4

Absence sweep files at integ2 (28 -> 4 confirmed, matching the C2 after-claim's "2 -> 4"):

    corpus/knowledge/github-private-vulnerability-reporting.md
    corpus/knowledge/github-repository-security-advisories.md
    corpus/SOURCES.md
    corpus/README.md

Do-nothing control at the freeze tree (battery v1 driver, `--root <integ> --counter c1
--jobs 8`), partial — box load 66-85 from sibling seats, killed by the 3600s tool deadline
after the baseline + 8 mutants:

    mutant=M01-L1-target-24 baseline_failures=0 mutant_failures=26 verdict=caught
    mutant=M02-L1-broken-ignored baseline_failures=0 mutant_failures=8 verdict=caught
    mutant=M03-L1-floor-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    mutant=M04-L2-one-reground baseline_failures=0 mutant_failures=25 verdict=caught
    mutant=M05-L3-shape-loose baseline_failures=0 mutant_failures=3 verdict=caught
    mutant=M06-L3-home-dropped baseline_failures=0 mutant_failures=0 verdict=uncaught
    mutant=M07-L3-home-no-abs baseline_failures=0 mutant_failures=0 verdict=uncaught
    mutant=M08-L4-bytes-dropped baseline_failures=0 mutant_failures=1 verdict=caught
    error: interrupted

These 8 lines are byte-identical to `controls/mutbat-before.txt` (sha256
13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd, re-verified), including
M06/M07 `uncaught` — the before-value reproduces and a do-nothing tree cannot reach
uncaught=0 at the frozen instruments, so the C1 kill-rule control passes for what ran.
The freeze pins in `.ufo/waves/round-46/attempt2/freeze.txt` all verify against the
exports: mutbat-v1 f7a7cdfa…, f29-gate-v1 a1091e24…, S074 1296528d…, manifest-a2
46e8077a…, source-recheck fd2e01e8…; `claims.json` is byte-identical between the freeze
export and the working tree.

Base selftest baselines (before-values, re-run):

    $ cd <base> && python3 -B corpus/instruments/r46-counters-selftest-c1.py --pure ... \
        --work <scratch>/w-st-c1-base --jobs 8
    residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
    selftest cases=76 failures=0
    EXIT=0

matches `controls/selftest-baselines.txt` (76/0).

## F4 — the base c2 selftest before-value is NOT reproducible after the landing

    $ cd <base> && python3 -B corpus/instruments/r46-counters-selftest-c2.py --pure .../L1/pure2
    FAIL control ctl-committed-tip-direct fixed=5/7 failing=['G1', 'G6']  <- control-not-7/7 failing=['G1', 'G6']
           gate G1 pass=0 read=rows=29 admitted=29 dup=0
           gate G6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=0 entry-bytes-ok=1
    selftest cases=137 failures=1
    EXIT=1

`selftest-baselines.txt` says "cases=137 failures=0, c2-exit=0" at base; today the same
command prints failures=1. The attempt-1 selftest's `ctl-committed-tip-direct` control
runs the attempt-1 counter against the COMMITTED TIP (the live lane, 29 rows / 66 entries
after this round's landing) and demands the attempt-1 after-state (28/65) — a
time-dependent control. The before-value was true when the receipt was taken (pre-landing);
it is not stable, and the claims' plain line "base: cases=137 failures=0" no longer holds
verbatim. The landed extended c2 selftest is supposed to replace this control (it reads
the new after-state), but at the integration commit it cannot run at all (F1). The c1
selftest has no such control and stays reproducible (F3).

## F5 — frozen-claims plain-line defect: `grep -c 'def case_'` is vacuous

Claims C1 `plain`: `grep -c 'def case_' corpus/instruments/r46-counters-selftest-c1.py
corpus/instruments/r46-counters-selftest-c2.py  # the case-count move behind the tallies`.
Re-run at every tree:

    base 04af9bc:    def-case c1: 0   def-case c2: 0
    freeze fe0f56b:  def-case c1: 0   def-case c2: 0
    integ2 96379ae:  def-case c1: 0   def-case c2: 0   (also `def case` without underscore: 0, 0)

0 everywhere — the selftests build cases as inline `results.append(...)` calls in `main()`,
not `def case_*` functions, so this counting command reads identically before and after and
cannot show "the case-count move"; only the output tallies move (76 -> 83 for c1; c2's
147 tally is unreachable at the integration commit, F1). The claim's instrument sentence
survives via the tallies, but this plain line as written measures nothing.

## F6 — smaller reference/hygiene defects observed in passing

- Both frozen claims name `"control": ".ufo/waves/round-46/attempt2/controls/freeze-controls.txt"`;
  that file exists neither at the freeze tree (`git ls-tree fe0f56b .ufo/waves/round-46/attempt2/controls/`
  lists 7 files, not this one) nor in the working-tree controls dir. Only a draft copy
  exists at `.ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/freeze-controls.txt`
  (uncommitted modification). The named control path is dangling.
- Working-tree `.ufo/waves/round-46/attempt2/controls/final-battery.txt` (untracked) is
  truncated at 374 bytes, ends mid-file at "== battery c1:", and records `exit=0` for the
  crashing c2 selftest (this seat's re-run of the same instrument exits 1). Any conclusion
  resting on that receipt is unsafe; it is not part of the frozen tree.

## What holds, what is broken (one line each)

- HOLDS at `96379ae`: battery c1 `mutants=20 caught=19 equivalent=1 uncaught=0
  baseline_failures=0`; extended c1 selftest `cases=83 failures=0`; equivalents map + proof
  files committed and non-empty; plain lines 29/74/66/4; freeze-tree before-readings and
  the sha-pinned receipts reproduce (c1 side fully, c2 battery side partial M01-M08).
- BROKEN at `96379ae`: battery c2 twin (`BASELINE-DIRTY baseline_failures=-1`) and the
  extended c2 selftest (`NameError: C1_ENTRIES`, exit 1, no `cases=` line) — the fix is
  sitting uncommitted in the live lane. C1's after-state as claimed ("at the final lane
  revision ... uncaught=0 ... failures=0") therefore does not hold at the wave-1
  integration commit. Also not reproducible: base c2 selftest `cases=137 failures=0`
  (F4), and the claims' `def case_` plain line is vacuous (F5).

## Limitations

- The full do-nothing battery replay at the BASE export was not completed: the freeze-tree
  run reproduced the baseline + mutants M01-M08 byte-identically and was then killed by the
  3600s tool deadline (box load 66-85, sibling seats). Before-values for M09-M20 rest on the
  sha-pinned `mutbat-before.txt` plus the verified byte-identity of the v1 driver and the
  attempt-1 instruments between base and freeze (freeze.txt discloses and this seat
  re-verified the selftest/gate byte-identity).
- The live lane's uncommitted (fixed) c2 selftest was not run to completion — whether the
  fix restores `cases=147 failures=0` and battery c2 `uncaught=0` is unverifiable from any
  committed tree and belongs to the parent's re-integration gate.
- The freeze-tree battery partial covers 8/20 c1 mutants; c2 battery before-lines were not
  re-run at the freeze (same driver-byte argument as above).
- S074 quote-locating, the f29 battery mode, and live-page checks are other seats' items;
  not run here. No live-target testing, no commits, no mutation of git/jj/index; scratch
  removed on exit.

Runs/exits quoted above are this seat's own executions at 2026-10-29 21:00-23:40 UTC in
scratch exports of `04af9bc`/`fe0f56b`/`96379ae` (git archive), TMPDIR under seat scratch,
pure input `/fast/scratch/hyaku/kasegi-r46/L1/pure2` used read-only.
