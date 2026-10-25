# RevNoHarmC1 — independent no-harm verification, claims.json C1(d)

Seat: RevNoHarmC1 (reviewer, leaf). Round 28 wave 1, lane kasegi-shokunin.
Written: 2026-10-25T17:34:13Z. All commands ran from the lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` with the system `python3`
(same-identity with the frozen counters; relative-path invocation for the
canonical run). No tool installed; pacman pause respected. No LSP device
exists in this session's tool inventory, so caller/definition checks were
text-level; every load-bearing claim below is a runtime measurement, not a
grep opinion.

## State timeline (honest)

- Seat start: live instrument digest = `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`
  = frozen `before.instrument_sha256`. PRE-STATE program executed against those bytes:
  - SKILL.md live run (pre-change): exit 0, stderr empty,
    `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
    — frozen before reproduced exactly; matches committed
    `.ufo/waves/round-28/c1-controls/skill-before.txt`.
  - Do-nothing controls re-verified on pre-change bytes: bad-fixture exit **0**,
    bounties-fixture **0** BOUNTIES-ABSENT lines, `--selftest` exit **1** —
    none reaches an after value; kill rule intact at seat start.
  - Corpus-wide before-table captured (43 files = 4 `corpus/*.md` + 39
    `corpus/knowledge/*.md`): `.ufo/waves/round-28/wave1/RevNoHarmC1/before-corpus-classes.tsv`.
    (Pre-change bytes proven by semantics: `corpus/QUALITY.md` rc=0 despite 1 bad.)
- Mid-seat, ExecImplC1 landed: live digest became
  `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
  (stable across two hashes 3 s apart; file still uncommitted ` M`).
  Seat flipped POST-STATE; delta measured against the landed bytes. Diff
  archived: `.ufo/waves/round-28/wave1/RevNoHarmC1/landed-instrument.diff`
  (259 insertions, 19 deletions vs HEAD).

## C1(d) result — SKILL.md live run: PASS

At digest `95333e29…`, canonical run `python3 corpus/instruments/anchorcheck.py SKILL.md`:

| Frozen expectation | Measured |
|---|---|
| exit 0 | 0 (stderr empty, 315 stdout lines) |
| bad=0 | 0 |
| LOST-RECORDED=306 | 306 (per-cite lines: 306) |
| PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0 | 0 / 0 / 0 / 0 |
| in-range cite instances=7 | 7 (7 OK lines, 7 distinct anchors) |

Summary line is **byte-identical** to the pre-change frozen line. Full
verdict-class set identical: {SUMMARY:1, LOST-RECORDED:306, OK:7} before =
after; BOUNTIES-ABSENT lines: 0. Archive:
`RevNoHarmC1/skillmd-after-canonical.txt`.

## Corpus-wide delta table: ZERO class movement

43 files scanned before (pre-change bytes) and after (landed bytes), per-file
per-class (in-range, bad, distinct, LOST-RECORDED, PIN-BROKEN, ORIGIN,
OUTSIDE-BASE, BASE-ABSENT, MISSING-FILE, PAST-EOF, BOUNTIES-ABSENT):
**no class moved in any file.** No file gained LOST-RECORDED. Tables:
`RevNoHarmC1/before-corpus-classes.tsv`, `RevNoHarmC1/after-corpus-classes.tsv`.

The 4 disclosed files measured LOST-RECORDED 0→0 (claim-gates.md,
intake-and-finalize.md, mission-control.md) and 15→15
(source-tree-loss-2026-09-28.md).

### F-1 · HIGH — frozen corpus_disclosure is contradicted by the corpus bytes (accuracy defect, NOT a no-harm violation)

claims.json C1 `corpus_disclosure` states 4 corpus *marked* bounties citations
"newly classify LOST-RECORDED instead of being silently skipped". Measured:
the delta is **0**, and it could not be otherwise. Evidence:

- `corpus/knowledge/claim-gates.md:3` — `` `~/Projects/bounties/ops/claim-check.mjs` `` — unmarked, **no `:NN` anchor**.
- `corpus/knowledge/intake-and-finalize.md:3` — `` `~/Projects/bounties/ops/import-board.mjs` `` — unmarked, no anchor.
- `corpus/knowledge/mission-control.md:3` — `` `~/Projects/bounties/ops/fleet-dispatch.mjs` `` — unmarked, no anchor.
- `corpus/knowledge/source-tree-loss-2026-09-28.md:3` — `` `~/Projects/bounties/...` `` — prose ellipsis token, unmarked, no anchor.

CITE (unchanged requirement, incl. the new arm) matches only
`path.ext:NN[-MM]`; LOST-RECORDED additionally requires a `[lost-tree] `/`[lost-base] `
prefix. None of these tokens satisfies either precondition, so the arm cannot
reclassify them. Corpus-wide census: **zero** CITE-shaped bounties tokens in
SKILL.md + corpus (marked or unmarked). The only marked bounties tokens
(`evidence-dir.md:3`, `intake-surface.md:4`, `mission-ledger.md:3`) are
anchorless directory tokens — equally invisible, equally unmoved (0→0).

Recommendation: per the frozen-claims protocol (R25-1), land an appended
correction file recording the true disclosed delta (0 new LOST-RECORDED; the
4 citations are unmarked+anchorless and remain silently skipped), and have the
round lesson state the measured 0. **Nobody should mark/anchor those 4 corpus
citations to manufacture the +4** — that would be fabrication, and out of
every seat's ownership anyway.

### F-2 · MEDIUM — frozen C1 counter 4's `bad` extraction is inert (defect in the frozen counter, before and after)

Counter 4's `sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'` matches nothing
on the real summary line (`…, 0 bad; 7 distinct anchors; …` has no
`bad; <digits> bad`). Verified by execution on pre-change bytes, on the
captured before-output, and replayed against the landed bytes: bad-sed output
is empty in both states; `lost=306` extracts fine. The landed diff keeps the
summary spelling frozen (for the BOUNTIES counter's benefit) and correctly
keeps BOUNTIES-ABSENT off the summary line, but that does not rescue the bad
sed. Consequence for L1: counter 4 will print the exit code and `lost=306`
but **no `bad=` line**; take bad=0 from the archived summary lines
(`RevNoHarmC1/skillmd-after-canonical.txt` and
`.ufo/waves/round-28/c1-controls/skill-before.txt`), and note the inert sed in
the appended correction file. Do not edit claims.json.

### F-3 · INFO — 5 corpus files flip exit 0→1 post-change; intended (a) semantics, not violations

All fail classes are pre-existing and class counts are unchanged:
`corpus/QUALITY.md` (PAST-EOF `README.md:159` vs 14-line file — note bare-name
resolution via LANE_DIRS `.`), and BASE-ABSENT in `citation-bases.md` (1),
`cra-manufacturer-reporting-duties.md` (1),
`iso-29147-divergence-and-clause-crosswalk.md` (5), `root-loss-2026-10-12.md`
(1). BASE-ABSENT is in the frozen FAIL_CLASSES set, so exit 1 is the specified
fail-closed behavior; LOST-RECORDED-only files (e.g. `corpus/README.md`, LR=2)
stay exit 0 — carry-forward 2's "recorded-not-fail" holds. The L1 corpus loop
should expect exactly these 5 nonzero exits and no others.

## Landed-diff sanity (reviewer read of `landed-instrument.diff`)

(g) BOUNTIES-PROVINCE arm added: `KASEGI_BOUNTIES` override + canonical
`~/Projects/bounties`, derived like MIRROR/ORIGIN (carry-forward 2 ✓);
realpath confinement with OUTSIDE-BASE on escape; absence is the new FAIL
class BOUNTIES-ABSENT; summary-line spelling deliberately frozen. Selftest
block added (~137 lines, `_counts` fixture harness) — isolated behind
`--selftest`, no effect on file runs (proven by the zero delta). Exit
semantics now return 1 on FAIL_CLASSES (a) ✓.

## Residual risk and verification gaps

1. Instrument still uncommitted (` M`) at measurement time; if ExecImplC1 or
   L1 changes it again, all POST measurements must be re-bound to the final
   digest. Digest at verification: `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
   (`RevNoHarmC1/instrument-digest-at-verification.txt`).
2. `corpus/QUALITY.md` and `corpus/README.md` were mid-edit by sibling seats
   during both scans; my tables are point-in-time. Re-run the loop below at
   round close; any class movement beyond the disclosed set is a violation.
3. Scan set is exactly the assigned one (`corpus/*.md`, `corpus/knowledge/*.md`,
   SKILL.md). `corpus/lessons/*.md` and `corpus/instruments/*.md` were not
   scanned (out of item scope); their bounties tokens observed in census are
   anchorless, so no movement is expected there either.
4. Selftest limb isolation (c) and fixture counters (a)/(b) belong to
   ExecInstrSelftest/ExecFixtureRun — not exercised here.
5. No LSP server available (device absent from tool inventory); recorded per
   protocol — text and runtime evidence only.

## Canonical re-run for L1 (post-change, from lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/anchorcheck.py        # bind digest, expect 95333e29… or later landed digest
python3 corpus/instruments/anchorcheck.py SKILL.md; echo exit=$?
#   expect exit=0 and byte-identical summary:
#   == SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
for f in corpus/*.md corpus/knowledge/*.md; do python3 corpus/instruments/anchorcheck.py "$f" 2>/dev/null | grep '^== '; done
#   diff class counts against .ufo/waves/round-28/wave1/RevNoHarmC1/{before,after}-corpus-classes.tsv;
#   expect: zero class movement; exactly 5 rc=1 files per F-3.
```

## Verdict

C1(d) no-harm: **PASS** on the measured bytes — SKILL.md verdict classes and
exit unchanged; corpus-wide class delta exactly zero. Two findings for the L1
(F-1 disclosure inaccuracy — HIGH; F-2 inert frozen counter sed — MEDIUM) and
one expected-behavior note (F-3). No actionable no-harm violation remains in
scope.
