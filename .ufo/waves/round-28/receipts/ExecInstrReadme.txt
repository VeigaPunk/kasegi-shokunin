== Round 28 / wave 1 / seat ExecInstrReadme — instruments README, anchorcheck.py section
== lane repo (cwd for every command): /home/vgpnk/Projects/shokunin/kasegi-shokunin
== lane base: c9f8b115a098c65356e4b3b6048af45a37ab8395 (claims freeze commit)
== written_utc: 2026-10-25T17:34Z (all timestamps UTC)

OWNED PATH (only production file this seat wrote)
  corpus/instruments/README.md

BEFORE / AFTER
  before  sha256: 8c2804eb44d2011f143c94c0677dc72d6e6ef9f5275614741b813f44e5446cde
          source:  git show HEAD:corpus/instruments/README.md | sha256sum  (HEAD = base c9f8b11)
          196 lines
  after   sha256: cf35a643b8d5d9d2eb726d4190e029f275bc5a129e87ccec40d27c9d86d5322b
          327 lines
  git diff --numstat -- corpus/instruments/README.md
          131     0       corpus/instruments/README.md
          (131 insertions, 0 deletions: append-only, existing lines 1-196 unchanged)

R6 EVIDENCE (no existing line moved, no cited source line changed)
  - Append-only diff (119/0), so every pre-existing line keeps its number; the
    section heading is line 198.
  - anchorcheck at the landed instrument digest over the base bytes (exported to
    .ufo/waves/round-28/wave1/ExecInstrReadme/readme-base/README.md) and over the
    edited file produces IDENTICAL output apart from the path field:
      base and new summary: 1 in-range cite instances, 0 bad; 1 distinct anchors;
      LOST-RECORDED=2 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=3
      base_exit=1 new_exit=1
    The exit 1 is PRE-EXISTING (3 BASE-ABSENT cites already in the committed
    README, mirror base absent since 2026-10-12), not introduced by this edit.
  - Static CITE scan of the appended lines (197-327): new_anchors=0. A first draft
    described the selftest escape cite with its `~/Projects/bounties/...:1`
    spelling; that would have added a BOUNTIES-ABSENT anchor to this file, so the
    description was rewritten without a line-anchored token (checked, then 0).
  - Re-checked after the final append (the "flagged by its own rule" paragraph):
    citation-line diff still IDENTICAL, new_anchors still 0, and no appended line
    has an odd backtick count (no code span broken across a newline). Evidence:
    .ufo/waves/round-28/wave1/ExecInstrReadme/final-replay.txt
  - This file is itself flagged by the landed rule, and the section says so: at the
    landed digest the README's own run is 1 in-range, 0 bad, LOST-RECORDED=2,
    BASE-ABSENT=3, exit 1. The 3 BASE-ABSENT are pre-existing round-17/24
    documentation examples (lines 114, 116, 164), unchanged by this edit and
    disclosed in the section rather than relabelled to make the file pass.

INSTRUMENT STATE THIS SECTION DOCUMENTS (measured, not declared)
  landed digest 95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514
  (523 lines); owned by ExecImplC1; pre-change digest
  c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748 is the
  do-nothing control. Counters run by this seat at the landed digest:
    bad fixture      : BASE-ABSENT printed, exit 1            (before: exit 0)
    bounties fixture : grep -c BOUNTIES-ABSENT = 1, exit 1     (before: 0, exit 0)
    --selftest       : `selftest cases=9 failures=0`, exit 0   (before: crash)
    SKILL.md         : 7 in-range, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0
                       OUTSIDE-BASE=0 BASE-ABSENT=0; exit 0   (unchanged)
    corpus sweep     : 44 files (corpus/knowledge/*.md + corpus/*.md + SKILL.md),
                       class_moved=0, exit_moved=5, all BASE-ABSENT-driven:
                       QUALITY.md, citation-bases.md,
                       cra-manufacturer-reporting-duties.md,
                       iso-29147-divergence-and-clause-crosswalk.md,
                       root-loss-2026-10-12.md

WHAT THE APPENDED SECTION DOCUMENTS
  1. Fail-closed exit: FAIL_CLASSES = MISSING-FILE, PAST-EOF, OUTSIDE-BASE,
     PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT -> exit 1 when any count is nonzero;
     LOST-RECORDED stays recorded-not-fail; `bad` stays the historical three-class
     count, so three fail classes move the exit without moving `bad`.
  2. BOUNTIES-ABSENT: CITE gains the `~/Projects/bounties/` arm; root derived like
     MIRROR/ORIGIN ($KASEGI_BOUNTIES wins, else canonical ~/Projects/bounties —
     single candidate, `test -d` exit 1 on 2026-10-25); realpath confinement as in
     the MIRROR arm (escape -> OUTSIDE-BASE); present root + absent file ->
     MISSING-FILE; the frozen `grep -c` counts lines, hence no summary bucket.
  3. --selftest spelling and the landed 9-case set, by name and limb: six fail
     limbs (missing-file, past-eof, outside-base, pin-broken, base-absent,
     bounties-absent) plus three controls at exit 0 (bounties-in-range,
     lost-recorded asserting LOST-RECORDED=1 not 2, clean). Temp dirs, four
     KASEGI_* root overrides, subprocess of the instrument, full class-vector and
     exit assertions.
  4. Corpus disclosure: DECLARED and NOT REPRODUCED.
  5. A re-verify block with the five measured targets.

CORPUS-DISCLOSURE FINDING (the one substantive deviation from the frozen text)
  claims.json C1 says 4 marked bounties citations "newly classify LOST-RECORDED"
  (claim-gates.md, intake-and-finalize.md, mission-control.md,
  source-tree-loss-2026-09-28.md). Measured at the landed digest and at the
  pre-change digest plus an arm-only scratch copy: 0 of the 4 reclassify.
  - The four are plain-text `source:` header lines (claim-gates.md:123,
    intake-and-finalize.md:109, mission-control.md:169,
    source-tree-loss-2026-09-28.md:353) with 0 backticks on each line, so TOK
    never yields them to CITE.
  - Scan of corpus/**/*.md + SKILL.md + LOG.md + SCORECARD.md (2026-10-25T17:24Z,
    before the new section existed): 70 backticked `~/Projects/bounties/…`
    tokens, 0 carrying a `:NN` anchor, 0 matching CITE with or without the arm.
  - Landed 44-file sweep: 0 verdict-class movement anywhere, the four included.
  ExecImplC1 independently reproduced the measurement and did not widen the
  matcher (peer confirmation, 2026-10-25); its blast radius if the L1 later
  authorizes a marked-bare scan is exactly those 4 lines in corpus/knowledge and
  0 in SKILL.md, so the 306/0 no-harm line is unaffected. The README records the
  disclosure as declared and not reproduced, with mechanism and re-run command,
  instead of asserting a count no run produced. Escalated to Main, which
  forwarded it to L1 KasegiR28 and told this seat to proceed as described. A
  correction, if wanted, is an appended corrections file (R25-1), never an edit
  to the frozen JSON.
  Raw evidence: .ufo/waves/round-28/wave1/ExecInstrReadme/disclosure-measurement.txt

LIMITS / HONESTY
  - ScoutGateRegistry's report (.ufo/waves/round-28/wave1/ScoutGateRegistry.md)
    never appeared (checked 17:26Z and 17:34Z); per the task rule this seat
    proceeded against the current bytes. No scout wording is quoted.
  - The first version of the section was written at the pre-change digest and
    said so; it was then rewritten against the landed bytes once the instrument
    settled (digest 95333e29…), so no PRE-STATE figure remains in the final text
    except the explicitly labelled *before* runs.
  - Selftest case names/limbs are transcribed from the landed `_selftest()` code
    and the executor's confirmation; N=9 is not retyped from this receipt alone —
    the section says to quote N from a live run.
  - No tool installed, no pacman transaction, no VCS write; read-only git only.

PEER COORDINATION
  agent://ExecImplC1: sent the disclosure measurement (do not widen the matcher),
  the `grep -c` line-counting warning (no BOUNTIES-ABSENT summary bucket), and a
  request for the exact selftest case list. Replies: same measurement, no
  widening, landed digest 95333e29…, cases=9 with the case list, and the 5-file
  exit movement — all independently re-measured by this seat before documenting.
  agent://Main: escalated the frozen-disclosure discrepancy; orchestrator replied
  that L1 KasegiR28 owns the claim decision and to proceed as documented.

VERDICT
  Documentation delivered in the owned file, append-only, 0 new anchors, with
  before/after anchor output identical. The landed instrument's four counters
  were measured by this seat (bad fixture exit 1; 1 BOUNTIES-ABSENT line;
  selftest cases=9 failures=0 exit 0; SKILL.md 306/0 exit 0) — measurements, not
  a claim of round-level verification, which stays with the L1 and the reviewer
  seats.
