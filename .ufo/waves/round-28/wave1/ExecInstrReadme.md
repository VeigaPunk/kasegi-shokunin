# ExecInstrReadme — round 28 wave 1

Seat: leaf, documentation. Owned path (only production file written):
`corpus/instruments/README.md`. Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
lane base `c9f8b115a098c65356e4b3b6048af45a37ab8395`.

## Delivered

Appended `## Round-28 amendment — anchorcheck.py fails closed (C1)` (heading line
198). 131 insertions, 0 deletions (`git diff --numstat` → `131 0`), so every
pre-existing line keeps its number. Before
`8c2804eb44d2011f143c94c0677dc72d6e6ef9f5275614741b813f44e5446cde` (196 lines),
after `cf35a643b8d5d9d2eb726d4190e029f275bc5a129e87ccec40d27c9d86d5322b`
(327 lines).

R6 measured, not inferred: `anchorcheck.py` at the landed digest over the base
bytes (exported to `.ufo/waves/round-28/wave1/ExecInstrReadme/readme-base/`) and
over the edited file produce byte-identical output apart from the path field
(`IDENTICAL`, both exit 1). A static CITE scan of lines 197-327 finds 0 new
anchors; an earlier draft spelled the selftest escape cite with its
`~/Projects/bounties/…:1` form and was rewritten because that would have added a
`BOUNTIES-ABSENT` anchor to this file. No appended line has an odd backtick count.

The section documents the required semantics plus a fifth disclosure:

1. **Fail-closed exit.** `FAIL_CLASSES` = `MISSING-FILE`, `PAST-EOF`,
   `OUTSIDE-BASE`, `PIN-BROKEN`, `BASE-ABSENT`, `BOUNTIES-ABSENT` → exit 1 when
   any count is nonzero, else 0; `LOST-RECORDED` stays recorded-not-fail. `bad`
   remains the historical three-class count, so three fail classes move the exit
   without moving `bad` — the text says to read the exit, not only the summary.
2. **`BOUNTIES-ABSENT`.** `CITE` gains the `~/Projects/bounties/` arm; root
   derived like MIRROR/ORIGIN (`$KASEGI_BOUNTIES` wins, else canonical
   `~/Projects/bounties`, single candidate, `test -d` exit 1 on 2026-10-25);
   realpath confinement (escape → `OUTSIDE-BASE`); present root + absent file →
   `MISSING-FILE`; the frozen `grep -c` counts lines, so no summary bucket.
3. **`--selftest` spelling and the landed 9-case set**, named by limb: six fail
   limbs (`missing-file`, `past-eof`, `outside-base`, `pin-broken`, `base-absent`,
   `bounties-absent`) plus three controls at exit 0 (`bounties-in-range`,
   `lost-recorded` asserting `LOST-RECORDED=1` not 2, `clean`); temp dirs, four
   `KASEGI_*` overrides, subprocess, full class-vector and exit assertions.
4. **Corpus disclosure** — declared and not reproduced (below).
5. **This file is flagged by its own rule** — the README's own run is 1 in-range,
   0 bad, `LOST-RECORDED=2`, `BASE-ABSENT=3`, exit 1; the three are pre-existing
   round-17/24 documentation examples (lines 114, 116, 164), disclosed rather
   than relabelled.

Plus a re-verify block whose five targets were all measured at the landed digest.

## Landed instrument, measured by this seat

Digest `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
(523 lines); pre-change `c2a9e6c6…` is the do-nothing control.

| counter | before | after (measured here) |
|---|---|---|
| bad fixture exit | 0 (BASE-ABSENT printed) | **1** |
| bounties fixture `grep -c BOUNTIES-ABSENT` | 0 | **1** |
| `--selftest` | crash, `FileNotFoundError: '--selftest'` | **`selftest cases=9 failures=0`, exit 0** |
| SKILL.md | 7 in-range, 0 bad, `LOST-RECORDED=306`, all other buckets 0, exit 0 | **identical, exit 0** |
| corpus sweep | 44 files, exits as committed | **0 class movement, 5 exits 0→1** |

The five exit flips are all BASE-ABSENT-driven: `QUALITY.md`,
`citation-bases.md`, `cra-manufacturer-reporting-duties.md`,
`iso-29147-divergence-and-clause-crosswalk.md`, `root-loss-2026-10-12.md`.
Evidence: `.ufo/waves/round-28/wave1/ExecInstrReadme/final-replay.txt`.

The section was first written at the pre-change digest (contract + PRE-STATE
labels) and rewritten once the instrument settled, so no figure in the final text
is a projection; the only pre-change numbers left are the explicitly labelled
*before* runs.

## Finding: the frozen corpus disclosure does not reproduce

Claims C1 says 4 marked bounties citations (claim-gates, intake-and-finalize,
mission-control, source-tree-loss-2026-09-28) "newly classify LOST-RECORDED".
Measured at the landed digest, at the pre-change digest, and on an arm-only
scratch copy: **0 of 4 reclassify**.

- The four are plain-text `source:` header lines (`claim-gates.md:123`,
  `intake-and-finalize.md:109`, `mission-control.md:169`,
  `source-tree-loss-2026-09-28.md:353`), 0 backticks per line, so `TOK` never
  yields them to `CITE`.
- Scan of `corpus/**/*.md` + `SKILL.md` + `LOG.md` + `SCORECARD.md` at 17:24Z:
  70 backticked `~/Projects/bounties/…` tokens, **0** with a `:NN` anchor, 0
  matching `CITE` with or without the arm.
- Landed 44-file sweep: 0 verdict-class movement anywhere, the four included.

ExecImplC1 independently reproduced this, did not widen the matcher, and put the
blast radius of a future marked-bare scan at exactly those 4 lines in
`corpus/knowledge` and 0 in `SKILL.md` (so the 306/0 no-harm line is unaffected).
Main forwarded the finding to L1 `KasegiR28` and told this seat to proceed as
described. A correction belongs in an appended corrections file (R25-1), never
in the frozen JSON; the same warning about `grep -c` counting lines (no
`BOUNTIES-ABSENT=` summary bucket) was sent to ExecImplC1 before it landed and
the landed docstring carries that rule.

## Evidence

- `.ufo/waves/round-28/receipts/ExecInstrReadme.txt` — seat receipt (digests,
  R6 evidence, counters, limits).
- `.ufo/waves/round-28/wave1/ExecInstrReadme/final-replay.txt` — landed-digest
  replay of all five targets plus the R6 diff.
- `.ufo/waves/round-28/wave1/ExecInstrReadme/readme-base/` — base-bytes export,
  before/after anchorcheck output.
- `.ufo/waves/round-28/wave1/ExecInstrReadme/disclosure-measurement.txt` — raw
  disclosure measurement (token scan, per-file live-vs-arm, sweep).
- `.ufo/waves/round-28/wave1/ExecInstrReadme/anchorcheck-scratch.py`,
  `anchorcheck-base.py` — arm-only replay copy and base-bytes copy (never the
  live file).

## Limits

- `ScoutGateRegistry.md` never appeared (checked 17:26Z and 17:34Z); per the task
  rule this seat proceeded against the current bytes, and no scout wording is
  quoted.
- Selftest case names and N=9 are transcribed from the landed `_selftest()` code
  and the executor's confirmation; the README itself tells readers to quote N
  from a live run.
- This seat measured the instrument; round-level verification of C1 stays with
  the L1 and the reviewer seats.
- No tool installed, no pacman transaction, no VCS write; read-only git only.
