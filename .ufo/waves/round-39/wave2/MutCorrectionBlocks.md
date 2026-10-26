# MutCorrectionBlocks — round-39 wave 2 (falsify) receipt

- seat: MutCorrectionBlocks (mutation-tester, leaf; no subagents spawned); judged axis depth:verifiability; milestone round-39
- work window 2026-10-26T20:05Z–20:21Z; lane HEAD at capture `5006097a84305267c9a3e8c1e1d560e60fe41d37` (tip Y); judged head J = `46c66c268502abd1b2c342fc71bf88ccf721845b` (`.ufo/waves/round-39/final-gates/all-gates.txt` `export-ref=`)
- status: **all 16 single-defect mutation scenarios CAUGHT by the review sweep; one frozen-counting-command baseline defect found (F-A: LOG.md anchored count 0); the landed instrument's G5 measured blind to all three mutations of the SCORECARD R2 block**
- deliverable: `.ufo/waves/round-39/wave2/MutCorrectionBlocks.mutations.txt` (raw transcript: detector source, pristine baseline, 16 scenario sweeps + verdicts, landed-suite G5 probes, representative diffs, restoration control)
- authorship: I am not the author of the attacked bytes (the R2 blocks are ExecCorrectionsR2's wave-1 deliverables; the suite is ExecSuiteBuild's). Attack seat per dispatch.

## 1. What was attacked

The four landed R2 correction blocks (the round-38 verifier's R2 defect: "records overstate C1 at J") and the sweep that is supposed to guard them:

| file | R2 block (HEAD line) | shape | overstate site it sweeps |
|---|---|---|---|
| corpus/lessons/round-38.md | `:311` (file ends there) | column-0 `Correction (round 39):` | `:21` frozen C1 row, `:94` Gate readiness item 8 |
| LOG.md | `:1704` | `- **Correction (round 39):**` bullet | `:1698` round-38 C1 bullet |
| SCORECARD.md | `:1560` | column-0 | `:1517` `## Round 38 result` depth:verifiability row |
| SHONEN.md | `:190` | column-0 | `:185` box-3 round-38 evidence line |

SCORECARD's second correction line `:1579` (`Correction (round 39): the round-38 tip run f06148c6 is report-only …`) is the R3 block, not R2 — left pristine in every scenario.

Every R2 block names the truth tokens `closed=7/8 exit=1` and `run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e` (measured on all four at HEAD); lesson and LOG additionally say "not J".

## 2. Detector — the review sweep as frozen

`sweep.sh` (source embedded in the deliverable) implements the sweep's frozen semantics as four limbs:

- **A** — the frozen counting command, erratum `claims-erratum-1.md` E5 item 7: `grep -c '^Correction (round 39)' <file>` ≥ 1 per file.
- **A'** — the item's own phrasing, unanchored: `grep -c 'Correction (round 39)'` ≥ 1 per file (observation limb).
- **B** — named truth (RevCorrections mandate): a correction-block line (column-0 `Correction (round 39)` or the LOG bullet shape `- **Correction (round 39):**`) must contain `closed=7/8` AND `7dd2fcd6`.
- **C** — append-only (RevCorrections mandate): `git diff --no-index --numstat pristine mutated` must show `deleted == 0`.

Pristine bytes = `git show HEAD:<file>`; every mutation applied to scratch copies under `/fast/scratch/hyaku/kasegi-r39/MutCorrectionBlocks/mut/<scenario>/`; the lane repo was never written. A mutation counts as CAUGHT when a limb that passed pristine for that file fails under the mutation.

## 3. Finding F-A — the frozen R2 counting command is unsatisfiable for LOG.md (baseline defect)

The erratum E5 item 7 command requires "at least 1 per file at the judged head". Measured:

```
$ git show 46c66c2:… # judged head J
corpus/lessons/round-38.md: 1
LOG.md: 0          <-- violation
SCORECARD.md: 2
SHONEN.md: 1
$ grep -c '^Correction (round 39)' … # at HEAD (tip Y): identical — LOG.md:0
```

The LOG correction is a `- **Correction (round 39):**` bullet (`LOG.md:1704`), which the anchored pattern `^Correction (round 39)` cannot match; the other three blocks are column-0 and count. The freeze-time file (dcd3170) has 0 in all four (blocks not yet landed), so the erratum was written blind to the landed shape. This is the same defect class the round itself routed as R1/M39-1 — a frozen counting command the landed bytes cannot satisfy — now on the R2 sweep: the frozen command cannot certify the R2 closure for LOG.md in its own terms. Not fixed by me (write scope); resolution belongs to the L1: either an erratum amendment (bullet-aware or unanchored pattern) or a column-0 reshape of the LOG block.

## 4. Mutation results — 16 single-defect scenarios, all CAUGHT

| scenario (target) | caught by limbs | note |
|---|---|---|
| M1-lesson (label → `round 38`) | A, A', B, C | count limbs fire (1→0) |
| M1-LOG | **B, C only** | A blind at baseline (F-A); A' masked — the Round-39 summary line `:1711` still carries the literal `Correction (round 39)`, so the unanchored count stays 1 |
| M1-SCORECARD | **B, C only** | A: 2→1, still ≥ 1 — the R3 line `:1579` keeps the count alive |
| M1-SHONEN | A, A', B, C | count limbs fire (1→0) |
| M2a-lesson (overstate `:21` rewritten in place, block dropped) | A, A', B, C | |
| M2a-LOG (`:1698` rewritten, bullet `:1704` dropped) | B, C | A' masked by `:1711` as above |
| M2a-SCORECARD (`:1517` rewritten, block `:1560` dropped) | B, C | A kept alive by `:1579` |
| M2a-SHONEN (`:185` rewritten, block `:190` dropped) | A, A', B, C | |
| M2b-* (block KEPT and overstate also rewritten in place) | **C only**, all four files | the grep+truth limbs pass; the append-only diff limb is the sole guard |
| M3-* (label kept, body replaced truth-free) | **B (+C)**, all four files | the named-truth limb is what catches it; count limbs stay green |

Raw sweep outputs for every scenario (all four files × four limbs, with counts) are in the deliverable. Representative diffs (M1-lesson, M2a-SCORECARD, M3-LOG, M2b-lesson) included there.

## 5. Landed-instrument cross-check — G5 is blind to the SCORECARD R2 block (measured)

Minimal scratch git fixtures (guard recipe: `mktemp -d` under scratch, `git init -q`, `rev-parse --show-toplevel` asserted, command-scoped throwaway identity) carrying pristine/mutated SCORECARD.md, run through the **landed** `corpus/instruments/r39-closure.sh` (`--export-ref <fixture> --lane <fixture> --work <scratch> --scratch-root <clean>`; other checks red from fixture-absence, only the G5 line is evidence):

```
pristine:      G5 payload=round39-section=1,final-lane-commit=0,correction=2,correction-labeled=1 closed=1
M1-SCORECARD:  G5 payload=…,correction=1,correction-labeled=1 closed=1   <-- green under the label mutation
M2b-SCORECARD: G5 payload=…,correction=2,correction-labeled=1 closed=1   <-- green under the in-place rewrite
M3-SCORECARD:  G5 payload=…,correction=1,correction-labeled=1 closed=1   <-- green under the truth-free body
```

G5's token set (`f06148c6` + `report-only`) is satisfied by the R3 correction line `:1579` alone, so mutating the R2 block (`:1560`) never moves it. Corroborating code facts: G3's quotable-run pattern `--export-ref[ =]+[0-9a-f]{7,40}` matches **0** of the four R2 correction lines (they quote `export-ref-run:`/`run-ref=`, never `--export-ref <hex>`), so G3 never scans them; no check reads the lesson/LOG/SHONEN correction blocks at all. Net: **the review sweep (grep + named truth + append-only) is the only detector the R2 blocks have — and it catches all three mutations, with the limb dependencies above — while the landed instrument contributes nothing for lesson/LOG/SHONEN and is satisfiable without the R2 block for SCORECARD.**

## 6. Controls

- **Do-nothing (pristine)**: limbs A', B, C pass on all four files; limb A passes on three and FAILS on LOG.md (F-A) — the frozen sweep cannot certify its own pristine baseline for LOG.md.
- **Restoration**: pristine copies byte-exact vs `git show HEAD:` — `RESTORED-EXACT` for all four (sha256 in the deliverable: lesson `7936fb4c…`, LOG `216b6970…`, SCORECARD `b43dabd5…`, SHONEN `44b604ff…`); mutations never touched the pristine dir or the lane.
- **Write scope**: only the two wave2 files named by the item; no lane/fleet/sibling writes; no mutating git command outside the sanctioned scratch fixtures; scratch removed before yield.

## 7. Tooling

None installed (no pacman, no uv/npx/binary installs) — bash, git, awk, grep, diff sufficed.

## 8. For the L1 / round 40

1. **F-A** (E5 item 7 vs LOG.md bullet): amend via erratum (bullet-aware pattern, e.g. `grep -cE '^(Correction \(round 39\)|- \*\*Correction \(round 39\):\*\*)'`) or reshape the LOG block to column 0. Until then the frozen R2 measurement is unsatisfiable for LOG.md.
2. **G5 token set**: adding `closed=7/8`/`7dd2fcd6` to G5's required tokens (or a dedicated limb over the R2 blocks) would close the measured blindness; the R3 line `:1579` currently satisfies G5 alone.
3. **`:1711` masking**: the Round-39 summary bullet in LOG.md carries the literal `Correction (round 39)` and both truth tokens; any unanchored sweep limb must anchor to correction-block shapes (as limb B does) or it can be satisfied by the summary line while the real block is mutated.
