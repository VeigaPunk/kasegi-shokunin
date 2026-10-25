# ScribeScorecard — round-30 result section (SCORECARD.md)

Seat: `ScribeScorecard-4` (L2 scribe, leaf). Milestone round-30, wave-1 v2.
Axes: depth:verifiability (C1), coverage (C2), depth:density (no-harm).
Assignment: sole writer of SCORECARD.md's round-30 result section — before→after
tables for C1 (4 held) and C2 (7 held), density unchanged 9 (disclosed, not a
score move), capabilities (none added), saturation unchanged (line 9/10, N=3),
and the move-log rows — then Report to
`.ufo/waves/round-30/wave1/ScribeScorecard.md`.

## Axes (named)

- **depth:verifiability** — C1 instrument conformance: A1 named-row missing-entry
  (no FileNotFoundError traceback), A2 duplicate-entry-realpath rejection, B1
  stem==id binding, B2 occurrence/anchor gate; do-nothing control must fail;
  mutants must each flip one limb; real-corpus no-regression.
- **coverage** — C2 F14 admitted (13→14), one entry citing first-registered-this-
  round rows S046/S047, registry 45→47, census exit 0, harness 16/16→17/17,
  per-id source-rechecks exit 0.
- **depth:density** — no score move; measurement change disclosed.

## Evidence measured (bytes labeled, from wave receipts)

| item | sha256 (landed working-tree) |
|---|---|
| frontier-recheck-count.py (before→after) | `c8a62888…` → `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |
| source-recheck.py (before→after) | `9fe6a4a0…` → `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` |
| round-30 manifest.json | `dfc8835750bbdcbc2480fc579f7204ba8215d3018d0bd0942e4ea97f3e5e75a6` |
| F14 entry | `f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32` |
| S046.txt / S047.txt / S041.txt | `884481f3…` / `bcf4f605…` / `e18acbf9…` (S041 = round-28 reuse) |
| SOURCES.md (post-append) | `a126a5f339323d5ae417a944d163d75a0427d9c77a5a330308e193dc7b81d927` |
| SKILL.md before/after (density) | `82bdced5…` → `a05c1b47…` (1047→1057 lines, R6 append) |

### C1 — before → after (frozen counters, claims.json C1)

| probe | before (freeze bytes, `c1-controls/before.txt` + `before-run-2.txt`, reproduced by ExecBeforeVerify on an isolated freeze export) | after (landed bytes; ExecMutantsC1/CritC1Kill/ScribeDigest) |
|---|---|---|
| A1 missing-entry | exit 1, uncaught `FileNotFoundError` traceback, no F98 marker | exit 1, `FAIL F98 knowledge/zz-missing.md ids=- exit=- problems=missing-entry`, `entries=1 pass=0 exit=1`, stderr empty |
| A2 duplicate entry | exit 0, `pass=2` on duplicate target | exit 1, `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`, `entries=2 pass=2 exit=1` |
| B1 stem mismatch | exit 0 (`S043:sha256 OK … occurrences=1`) | exit 1, `S043:manifest MISMATCH reason=stem-mismatch` |
| B2 double occurrence | exit 0 (`occurrences=2 anchor=MISSING`) | exit 1 with a failure reason — on the frozen `manifest-b2.json` that reason is `reason=stem-mismatch` (B1 fires first; see note) |

- Do-nothing control at freeze bytes fails all four predicates (control cannot meet target).
- Mutants: A1/A2/B1 each flip exactly one limb; mutant-B2 does not flip on the
  committed fixture (stem-masked) but flips on the supplementary same-stem fixture:
  live exits 1 `reason=occurrence-not-unique`, mutant exits 0 (`occurrences=2
  anchor=MISSING`). B2 limb is load-bearing; committed fixture is not isolating
  (R10-class defect recorded; covered by `--selftest` 9/9 and clean fixture).
- `source-recheck.py --selftest`: `selftest cases=9 failures=0`, exit 0.
- Real-corpus regression leg: full harness at final state `entries=17 pass=17 exit=0`;
  all 34 prior registered source-rechecks (manifests rounds 23–29) exit 0; round-30
  S046/S047/S041 rechecks exit 0. Base-passing rechecks preserved.
- Verdict: **Improved, score held 4.** Kill rule PASS as written (b2 exit 1 names a
  failure reason; no real-corpus regression). B2 fixture-isolation caveat recorded.

### C2 — before → after (frozen counters; `c2-controls/before.txt`, `census-before.txt`, `harness-after.txt`)

| counter | before | after |
|---|---|---|
| frontier admitted (awk) | 13 | **14** (F14 row, `corpus/README.md`) |
| entries citing S04[6-7] | 0 | **1** (the F14 entry) |
| S046+S047 registry rows | 0 | **2** |
| registry total rows | 45 | **47** (A 44 / B 1 / C 2; mined 35, queued 9, rejected 3; malformed 0, dup none, enums none, missing used-by none) |
| sources census validate | exit 0 | **exit 0** (W04 S028/S029 only) |
| frontier harness | entries=16 pass=16 exit=0 | **entries=17 pass=17 exit=0** incl. `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0` |
| source-recheck S046/S047/S041 | n/a (no captures) | exit 0 each; all assertions exactly-once or anchor-verified (S047 Q1 occurrences=3 anchor=123-ok, Q3 occurrences=2 anchor=130-ok) |

- Sourced: F14 entry (38 lines, `f584f06c…`) cites S046/S047 (first registered this
  round; captures from IPA JVN activity report PDF and quarterly registration report)
  plus already-registered S041 (capture reused from round 28). Q1–Q10/R1–R15 bar
  check: non-author RevC2Entry ADMIT (agree); RevC2Registry confirms S046/S047 rows
  clean (E11 was mid-wave only, before the entry landed).
- Verdict: **Improved, score held 7.** Kill rule PASS at the landed bytes.

### depth:density — unchanged 9

- SKILL.md append (round-30 Gates & probes registry section, +10 lines, R6):
  mean 167.5 → 171.1, 22 → 23 blocks, 659 → 662 path-citation instances.
- `anchorcheck.py SKILL.md`: exit 0, verdict classes unmoved (7 in-range / 0 bad /
  LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0).
- Density change disclosed, not claimed as a score move.

## Landing

- `SCORECARD.md`: round-30 section appended after line 782 (the round-29 close-out
  addendum). Appended content = the section reproduced in the next block. Verified:
  pre-append sha256 `90d2067b…` == `head -782` sha256 post-append (existing text
  byte-preserved); file 782 → 835 lines.
- Report: this file (ownership marker; final evidence).

### Appended SCORECARD.md text (round-30 section)

```markdown
## Round 30 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-30/claims.json` (base `a94871315…`,
claims-freeze commit `3c557354…`, wave-1 dispatch commit `002e92ce…`). Receipts
land under `.ufo/waves/round-30/` (`c1-controls/`, `c2-controls/before.txt`,
`census-before.txt`, `harness-after.txt`, `wave1/`).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | A1 exit 1 uncaught `FileNotFoundError` traceback, no named-row marker; A2 exit 0 `pass=2` on a duplicate entry realpath; B1 exit 0 (stem mismatch passes); B2 exit 0 `occurrences=2 anchor=MISSING` (`c1-controls/before.txt`, `before-run-2.txt`) | A1 exit 1 `FAIL F98 knowledge/zz-missing.md … problems=missing-entry` naming row and path; A2 exit 1 `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`; B1 exit 1 `reason=stem-mismatch`; B2 exit 1 with a failure reason (the frozen fixture trips the B1 stem limb first; see B2 note); `source-recheck.py --selftest` 9/9 exit 0; real-corpus regression leg green (full harness 17/17 exit 0; 34 prior registered source-rechecks on manifests rounds 23–29 and round-30 S046/S047/S041 all exit 0) | **Improved, score held 4.** Instruments: `frontier-recheck-count.py` `c8a62888…` → `aa60b581…`; `source-recheck.py` `9fe6a4a0…` → `33602a9d…`. Do-nothing control at freeze bytes reproduces all four before defects (`ExecMutantsC1.md`, `CritC1Kill.md`) — control cannot meet the target. Mutants A1/A2/B1 each flip exactly one limb; mutant-B2 flips on the supplementary same-stem fixture (live exit 1 `reason=occurrence-not-unique`; mutant exit 0) — the committed `manifest-b2.json` (id S045, path B2.txt) has the stem limb fire first, so the frozen B2 counter does not isolate the occurrence limb (R10-class fixture defect, recorded; the limb is covered by the selftest 9-case matrix and the clean same-stem fixture). Kill rule PASS as written (b2 exit 1 names a failure reason; no real-corpus regression). | 30 |
| C2 | coverage (7) | frontier admitted 13; entries citing S04[6-7] 0; registry rows 45; census exit 0; harness entries=16 pass=16 exit=0 (`c2-controls/before.txt`, `census-before.txt`) | frontier admitted **14** (F14 row in `corpus/README.md`); entries citing S046/S047 **1** (the F14 entry); registry rows **47** (S046/S047 appended); census **exit 0** (W04 S028/S029 only); harness **entries=17 pass=17 exit=0** incl. `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0`; source-recheck S046/S047/S041 each **exit 0** on the round-30 manifest (`dfc88357…`), all assertions exactly-once or anchor-verified (S047 Q1 occurrences=3 anchor=123-ok, Q3 occurrences=2 anchor=130-ok) | **Improved, score held 7.** C2 sourced: F14 entry `knowledge/japanese-severity-vocabulary-and-impact-model.md` (`f584f06c…`, 38 lines) cites S046/S047 (first registered this round; captures `S046.txt` `884481f3…` / `S047.txt` `bcf4f605…`) plus the already-registered S041 (capture reused from round 28, `e18acbf9…`). Do-nothing control at base (13/0/45, 16/16, no captures) cannot meet the target. Kill rule PASS at the landed bytes (`harness-after.txt`; `ExecCensusAfter.md`). | 30 |
| depth:density | 9 | mean 167.5, 22 blocks, 659 path-citation instances (SKILL.md `82bdced5…`) | mean **171.1**, 23 blocks, 662 cites (SKILL.md `a05c1b47…`, 1047 → 1057 lines; R6 append of the round-30 Gates & probes registry section); `anchorcheck.py SKILL.md` exit 0, verdict classes unmoved: 7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0 | **Unchanged, no harm.** Density change disclosed, not claimed as a score move (same posture as round 29). | r15 (held r30) |

**Measurement state.** Values above were measured at the landed working-tree bytes
described in `.ufo/waves/round-30/harness-after.txt` (digests pinned there), at
`c1-controls/mutants/` and by `ScribeDigest.md`; earlier red snapshots recorded
mid-wave states (F14 entry/manifest absent, S047 unanchored, census E11) and are
superseded by the final receipts, not hidden.

**B2 fixture note (recorded, not a kill).** The frozen `manifest-b2.json` declares
`id=S045` with `path=B2.txt`, so the B1 stem check fires before the occurrence gate;
the frozen counter b2 exits 1 with `reason=stem-mismatch`. This satisfies the frozen
kill-rule clause (exit 1 + a failure reason) but does not exercise the B2 limb; the
occurrence limb is demonstrated by `--selftest` (9/9) and by the supplementary
same-stem fixture where the live instrument exits 1 `reason=occurrence-not-unique`
and mutant-B2 exits 0 (`ExecMutantsC1.md` §4, `CritC1Kill.md` §3–§4). A corrected
isolating B2 fixture is the recommended follow-up, already recorded in the lesson
receipts.

**recheck-audit open item (outside the frozen claims).** `recheck-audit.py`
prints `expect=present expected=43 missing=0 unexpected=0 exit=1`: the strict
instrument/own limbs reject the new `considerthese-proposals-ledger.md` recheck form
(names no corpus instrument and not its own file), so the audit's exit-0 acceptance
is not met (`ExecExpectedList.md`). Expected-list equality holds; the item is
recorded for the lesson.

**Capabilities: no row added this round.** Per the round-30 assignment no new
capability is planned, and none was demonstrated beyond the frozen predicates: C1
extends the existing `frontier-recheck-harness` and `source-capture` instruments and
C2 exercises the already-recorded `source-capture`, `source-capture-pdf` and
`frontier-recheck-harness` capabilities. The Capabilities table is unchanged; the
stagnation window continues (last capability entry round 25).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With
depth:verifiability at 4 the lowest-axis obligation stays active.

### Round-30 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 30 | depth:verifiability | 4 (A1 traceback/no row marker; A2 duplicate passes; B1 stem passes; B2 double-occurrence passes) | 4 held (A1 exit 1 naming F98; A2 exit 1 naming duplicate; B1 exit 1 reason=stem-mismatch; B2 exit 1 reason present; selftest 9/9; 34 base-passing real rechecks preserved) | `corpus/instruments/frontier-recheck-count.py`, `corpus/instruments/source-recheck.py`, `.ufo/waves/round-30/c1-controls/`, `wave1/ExecImplSourceRecheck.md`, `wave1/ExecMutantsC1.md`, `wave1/CritC1Kill.md` |
| 30 | coverage | 7 (frontier 13, S046/047 citations 0, registry 45, harness 16/16) | 7 held (frontier 14, citations 1, registry 47, census exit 0, harness 17/17, rechecks exit 0) | `corpus/README.md` F14 row, `corpus/SOURCES.md` S046/S047, `corpus/source-snapshots/round-30/manifest.json`, `.ufo/waves/round-30/harness-after.txt` |
```

## Notes / deviations / limits

- **Tool anomaly (reported):** `edit` repeatedly rejected the SCORECARD.md append:
  reads minted tag `#6D42` while edit insisted the current hash was `#3ABA`
  (four attempts; read-then-edit in the same session). To satisfy the L1's
  immediate request I appended via `bash` heredoc (`cat /tmp/sc30-append.md >>
  SCORECARD.md`) instead — a one-shot append-only write, verified byte-preserving:
  pre-append sha256 `90d2067b…` equals post-append `head -782` sha256.
- No tool installed/upgraded (RULES.md read; nothing needed).
- No write outside the lane repo; no git/jj mutation; no live target contact.
- Open items handed to the lesson/L1: (1) frozen B2 fixture is not isolating
  (corrected same-stem fixture recommended); (2) `recheck-audit.py` exit 1 on the
  new `considerthese-proposals-ledger.md` strict form; (3) post-integration re-runs
  at the commit remain owed to `ExecPostCommitRecheck` (values above are working-tree
  measurements; no commit hash asserted).
