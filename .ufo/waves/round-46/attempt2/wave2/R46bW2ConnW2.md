VERDICT: INFO

Seat R46bW2ConnW2 — cross-seat scan (round 46 attempt 2, wave 2), run last per the card.
Read 25 of 32 wave-2 reports (`wave2/*.md`) plus the frozen artifacts (claims.json, freeze.txt,
counter-errata.md, controls/*.txt, S074.txt, manifest.json, the landed instruments, and the L1's
in-progress working-tree fixes). Unlanded at writing (stated as a limitation, not silently
skipped): R46bW2ExecRerunC1, R46bW2ExecRerunLive, R46bW2RevClaimC1, R46bW2MutSelfC1,
R46bW2CritErrata2 — all C1-chain seats whose territory is independently covered below by
R46bW2MutSelfC2, R46bW2RevSelftestW2, R46bW2SentFinal, R46bW2CritVerdictC1 and the L1's own
live receipts. Every finding below names the artifact attacked, the attacking seat(s) with the
section, and the quoted output; where cheap I re-ran the check myself (marked "own run").
Timeline note: while this report was being written the L1 began landing wave-2 integration
fixes IN THE WORKING TREE (uncommitted, observed 21:36–22:03 local): the c2 selftest import
order repaired, the f29 selftest's 28-guard widened to 28/29, the f29-gate ledger floor bumped
30696→40843, the c2-gate g2 junk clause reworked, and f29 equivalence proofs added to
`r46-mutant-equivalents.json` + a new proofs file. Each fix is noted under its finding. The scan
below is against the landed integration tree `96379ae` the wave was dispatched to attack; the
parenthetical "(fix in progress)" marks what the L1 had already started.

Headline: C2's counting chain HOLDS at the integration (5+ seats, all limbs re-run green), but
the C1 instrument chain is BROKEN at the landed tree — three of its five instruments cannot run
there as committed, and no committed after-receipt exists. Nothing in C2's content surface is
contradicted; every C2 after-value was independently re-derived.

=====================================================================
(1) FINDINGS CONFIRMED BY >= 2 SEATS
=====================================================================

F1. The landed c2 selftest is dead at import; the C1 after-state's c2 baseline is ungradeable
    and the c2 battery leg prints BASELINE-DIRTY.
    Artifact attacked: corpus/instruments/r46-counters-selftest-c2.py:68-69 (landed 96379ae).
    Eight seats quote the identical crash:
    - R46bW2RevSelftestW2 Finding 1 (with attribution: both wave-1 drafts are correct —
      ExecSelftestC2 draft 0457a192 has no LEDGER code, pin-amend draft 37a723c0 has the correct
      order — "the merge MOVED C1_ENTRIES … to AFTER EXEMPT_ENTRIES … the L1's own integration
      receipt records the crash, not a pre-existing failure").
    - R46bW2SimplW2 F1 (`python3 -I … --help` (rc=1) → NameError; "the ten mut-g* cases the
      extension adds … are all unreachable").
    - R46bW2CritCalib2 finding 1 (SCORECARD.md:1823,1831 / SHONEN.md:341-343 / LOG.md:2025,2030
      report 147/0 "and describe the C2 mutation coverage as closed" — false at the tree).
    - R46bW2CritHonestStop honest-stop list item 1.
    - R46bW2RevRegistryText FINDING 1 ("the committed instrument cannot print
      `selftest cases=<N> failures=<F>` at all").
    - R46bW2MutSelfC2 F1 (+ "mutbat counter=c2 BASELINE-DIRTY baseline_failures=-1 (exit 1)").
    - R46bW2RevClaimC2 F2. R46bW2SentFinal D1.
    - The L1's own untracked controls/final-battery.txt records the same traceback.
    Claim consequence (R46bW2RevSelftestW2): "C1's after-condition … is FALSE for c2 as landed,
    and the c2 battery grading is unreachable … `expect_after`'s c2 line cannot be produced by
    the committed instruments at the tip."
    Own run: confirmed the traceback verbatim against the landed bytes, and confirmed the L1's
    working-tree fix now parses (`--help` rc=0). (Fix in progress.)

F2. Even with the import fixed, the extended c2 selftest cannot reach failures=0 against the
    committed v1.3 counter: 147/101, all 101 on G2's new junk==0 conjunct (erratum E3 landed
    the conjunct after the selftest drafts were built and receipted against v1.2).
    - R46bW2RevSelftestW2 Finding 2: same draft, `--lane <fe0f56b export>` →
      `selftest cases=147 failures=0` (reproduces the executor receipt); `--lane <96379ae
      export>` → `selftest cases=147 failures=101`; "errata E2 nonetheless asserts 'Baselines
      stay failures=0' — that sentence is falsified for c2."
    - R46bW2MutSelfC2 F2/F3/F5: junk-free counter → `selftest cases=147 failures=1`; under the
      committed counter G2a/G2b/G2c "are not caught by their own line (C reads `ok`)" — the
      other seven dedicated cases are caught only with junk-induced collateral G2 failures;
      `ctl-committed-tip-direct` "can never read 7/7" at the tip (5/7).
    - R46bW2SentFinal D1: scratch line-swap → `selftest cases=147 failures=101 exit=1` (18
      control FAILs, 83 mutant FAILs).
    - The L1's own controls/final-battery-rerun.txt (untracked, 21:38): "selftest c2 (fixed
      import): … selftest cases=147 failures=101".
    (Fix in progress: the L1 is reworking the g2 junk clause in the working tree.)

F3. The landed f29 selftest cannot run on the landed tree: hardcoded expected-28 frontier rows
    abort every invocation (`selftest: lane README carries 29 frontier rows, expected 28`),
    so `r46-mutbat --counter f29` prints BASELINE-DIRTY and the R50 receipt's frozen duty
    (selftest + f29 battery mode reach caught-or-equivalent for the 21 mutants) is unevidenced
    at the landed tree.
    - R46bW2MutBattery2 F1 ("The committed selftest therefore cannot run on the tree it ships
      in"). R46bW2MutSelfF29 F1 ("passes only on a tree that does not contain the F29 row it
      claims to grade"). R46bW2SimplW2 F2 (the committed final-measure.sh driver "exits nonzero
      at the tip"). R46bW2RevRegistryText FINDING 3. R46bW2RevClaimC2 F1. R46bW2SentFinal D4.
    - Same 28-assert one layer down in the pinned fixture: R46bW2RevRegistryText FINDING 4 and
      R46bW2RevClaimC2 F5 (`controls/f29-fixture.py --mode positive --lane <live>` →
      `AssertionError: 29`; "the R50 receipt's control readings are not reproducible at the
      final tree").
    Own run: confirmed the abort on the live lane pre-fix; post-fix (L1 working tree) the
    selftest runs `selftest cases=30 failures=0` rc=0 on the landed lane. (Fix in progress.)

F4. The battery and selftests are non-hermetic: `--root` is never handed to the c2/f29 selftests,
    `LANE` is hardcoded to the live lane, and the f29 gate is path-bound (`LANE_CD` in H2's
    recheck shape) — a tree whose recheck names another path reads red and an export cannot be
    graded as shipped.
    - R46bW2MutBattery2 F2 ("This is why `--root` cannot retarget the f29 mode").
    - R46bW2MutSelfC2 F4 ("The grader does not grade the tree under --root" — `run_selftest`
      passes no `--counter`; the selftest default `LANE` is hardcoded line 53).
    - R46bW2SentFinal D5 (c2 selftest copies snapshot/knowledge "from the live lane … not from
      the tree under test … the battery is not hermetic to --root").
    - R46bW2RevSelftestW2 secondary: the equivalents map values are CWD-relative and the
      battery checks them with a bare `os.path.isfile` (R46bW2SentFinal D6: a run from another
      cwd "would turn equivalents into uncaught silently"; isfile does not check non-empty —
      the wave-1 S5 class).

F5. The claims' before/selftest baselines are not reproducible from the pinned base 04af9bc9:
    the extended c1 selftest CRASHES against the base export (AssertionError in
    m_anchor_moved), the only working `--pure` is the unpinned pre-round export (914ca0b / the
    L1's pure2), and both selftests still carry the dead `/fast/scratch/.../L1/pure` default.
    - R46bW2RevRegistryText FINDING 2: `python3 … r46-counters-selftest-c1.py --pure $S/base
      --work … --jobs 8` → `AssertionError: mutation was a no-op on corpus/knowledge/
      claim-gates.md`, EXIT=1; root cause located (the case's regex cannot match the first G1
      row's line-RANGE anchor `:101-108`); "the wave-1 receipt … was produced against a scratch
      pure tree … not reproducible at the final tree".
    - Own run: reproduced the identical AssertionError against a fresh `git archive 04af9bc9`
      export, rc=1. This adjudicates the apparent contradiction with R46bW2CritVerdictC1 (see
      C1 below): that seat's 83/0 used the L1's pure2, not the pinned base.
    - R46bW2MutSelfC2 F8 and R46bW2SentFinal D2: with the base export as `--pure`, BOTH selftests
      fail preconditions (`AssertionError: claim-gates.md`); only the 914ca0b-era export works;
      "the claims' do-nothing control … is not reproducible from the base commit alone".
    - R46bW2SentFinal §3: counter-errata.md E2's claim that "Both dead --pure defaults now point
      at the committed map pattern (SentScratch F1 fix: --pure required, no dead absolute
      default)" is FALSE — both selftests still default `PURE = "/fast/scratch/hyaku/kasegi-r46/
      L1/pure"` (c1 :57/:649, c2 :54/:459), dead on disk; running c1 bare → FileNotFoundError.
      (Cross-wave: wave-1 R46bConnPatterns S3 reported the same dead defaults; the erratum
      claimed the fix; it did not land.)

F6. No committed after-receipts exist for either claim, and the one untracked receipt is
    internally inconsistent (records the c2 NameError traceback, then a pipeline-masked
    `exit=0`, then ends mid-file at `== battery c1:`); the receipts the round's own new
    SCORECARD/SHONEN/LOG rows cite are absent from the integration commit.
    - R46bW2CritVerdictC1 finding 2 (final-battery.txt "not committed and stops at line 10 …
      contains neither battery summary"). R46bW2CritHonestStop honest-stop items 1-2
      (final-measure.txt / final-battery.txt / freeze-controls.txt all missing at 96379ae; the
      claims' named control pointer `controls/freeze-controls.txt` dangles — confirmed by my own
      `ls`: No such file; R46bW2RevClaimC2 F4). R46bW2CritCalib2 finding 2. R46bW2RevSelftestW2
      secondary. R46bW2RevClaimC2 F3 ("not committed, not named by the claims, and not
      trustworthy as a measurement"). R46bW2RevRegistryText FINDING 1 (the `exit=0` "comes from
      a `| tail` pipeline masking the crash's real exit 1").
    Own run: a trivial `cmd | tail -1; echo rc=$?` over the crashing selftest prints the
    abort line and rc=0 — the exact masking mechanism, demonstrated live.

F7. The dispatch header mislabels the freeze commit: `fe0f56b` is called "integration of wave 1"
    but is the claims/counter FREEZE; the wave-1 integration (the only tree where the C2
    after-values exist) is `96379ae` (HEAD). Six seats independently flagged and worked around
    it: R46bW2ExecRerunC2 Finding 1, R46bW2CritHonestStop "Target identity",
    R46bW2MutBattery2 F6 ("Tree-identity"), R46bW2MutGate1 scope note, R46bW2MutSelfF29 F1,
    R46bW2SentFinal opening paragraph. Smallest safe correction (R46bW2CritHonestStop): "pin the
    FALSIFY target to the integration hash, preserving fe0f56b as the freeze hash."
    Own run: `git log --oneline` confirms 96379ae = "wave-1 integration", fe0f56b = "freeze
    claims …". (Not a lane defect; a dispatch-labeling defect every seat had to route around.)

F8. The frozen c2-gate (v1.3) reads 5/7 at the integration tip — G1 hard-pins 28 rows/F28-only,
    G6 hard-pins 65 entries — matching its committed receipt byte-for-byte; disclosed by errata
    E3 ("the new after-state is graded by r46-f29-gate.py, not by the attempt-1 instrument").
    R46bW2MutPinAmend Finding 0 (G6 red "caused by the F29 entry, not the ledger"; "the report
    must carry it"), R46bW2ExecRerunC2 Finding 5 ("equals, line for line, the commit's own
    receipt"), R46bW2MutNoHarm B3 (freeze 7/7, HEAD 5/7, base 7/7), R46bW2CritCalib2 and
    R46bW2RevRegistryText limitations, R46bW2SentFinal §1 table. No seat reports this as a
    regression; it is the disclosed consequence of the C2 landing on a frozen counter.

F9. Equivalence-proof quality gaps against the C1 kill rule ("a mutant with neither a failing
    selftest case nor a committed proof keeps the claim red"):
    - f29: H1b, H7a, H7c are uncaught with NO committed proof at the landed tree —
      R46bW2MutBattery2 F3/F4 ("uncaught, no proof … FAIL", with argued-but-uncommitted
      equivalence proofs); the L1's own rerun receipt shows `mutbat counter=f29 mutants=21
      caught=18 equivalent=0 uncaught=3 baseline_failures=0` even after adding the three map
      entries (22:03 state). (Fix in progress: map now names f29-H1b-H7a-H7c-proofs.md.)
    - c2: G6b's committed proof argues a clause that does not exist (`ledger_ok` is not in g6) —
      R46bW2MutSelfC2 F6 ("the committed proof does not prove the battery's mutant … the
      'committed proof' condition is nominal for G6b"; the equivalence itself likely holds, 8-tree
      differential 0 differing).
    - G7a/G7c equivalence rests on the fleet-root census script, which no gate pins —
      R46bW2MutBattery2 F4 caveat, R46bW2MutSelfC2 F7, R46bW2SentFinal §3 (`CENSUS` hardcoded at
      f29-gate.py:102 / c2-gate.py:60, sha256 today `3fb72615…`, "The gate's verdict changes if
      that file changes").

F10. The landed F29 entry carries four false/unsupported statements (M46-3 class); two were
     flagged in wave 1 and landed anyway.
    - Item 3's conditional mis-states the source trigger: the entry packages "if the project
      uses another numbering authority's identifier" where S074.txt:26's actual condition is
      coverage ("GitHub cannot assign CVEs to your project if it is covered by another CNA") —
      a false-pass recipe at the F29/F07 seam (a project covered-but-not-yet-assigned by the
      most-appropriate-scope CNA false-passes). R46bW2CritScope Finding 1 (VERDICT BROKEN),
      quoting the entry, cna-assignment-and-vulnerability-rules.md:36 ("The CNA with the most
      appropriate scope MUST be contacted and given the first opportunity to assign") and
      S074.txt:26. Own read of entry:131-139 confirms the wording.
    - "S074.txt:1-42 is the whole capture and all 42 lines are body prose" — false (lines 1/4/7
      are page chrome). R46bW2RevEntryClaims finding 1 + wave-1 R46bConnPatterns M1 (×2
      cross-wave; wave-1 recommended the fix; the sentence landed anyway).
    - "in the order the page states it" for decision-rule steps 3-4 — the page states the CVE
      request (S074.txt:25) before the fix-version duty (:38). R46bW2RevEntryClaims finding 2 +
      R46bW2ScoutS074Live F1 (×2, independent methods — line anchors vs live-page char offsets).
    - "the three cases at S074.txt:40,42 let a maintainer publish without a fix version" — case
      40 says "wait to disclose … when the fix is ready"; only :41-42 permit. R46bW2ScoutS074Live
      F2 (single seat; quoted capture lines).
    - Gate-side false greens on the admission shape: a no-decision-rule entry and an
      "S074; S999 (claimed same-ground source)" source-spray entry both grade 7/7 (H1 checks
      neither actionability nor source exclusivity) — R46bW2CritHonestStop honest-stop item 3
      (citing the measured wave-1 runs) and R46bW2CritVerdictC2 ("not machine-graded … Require a
      non-author seat to review that criterion"; the non-author reviews R46bW2RevEntryClaims /
      R46bW2CritScope did review it, producing the defects above).

F11. The R50 receipt and frozen record need the correction errata the round already half-knows
     about (never smooth these into a scalar score):
    - junk/fabricated controls read `fixed=6/7 exit=1` (H2 green), not the receipt's 3/7 —
      wave-1 R46bConnPatterns S1 (seven seats) + R46bW2CritHonestStop honest-stop item 4.
    - disclosure (e)'s stated reason is wrong: the located-floor shadowing is the five-core
      cover argument (min 5 located quotes for 5 cores), not the 6-row table —
      R46bW2MutGate2 F6.
    - the "9 disclosed" tally vs the receipt's own corrected 10 not-shown (H6c) —
      R46bW2MutBattery2 F3, R46bW2CritHonestStop item 4, R46bW2RevRegistryText limitation 2.
    - R46bW2MutGate1 F5/F7/F8/F10 add that several R50 "not isolable at gate level" disclosures
      have gate-level counterexamples (duplicate non-F29 id via W1; 11+-cell row direction;
      core floor/span width; duplicate `## Registry`) — consistent with wave-1 C3's refutation
      of disclosures (a)/(b)/(c).

Confirmed HOLDS-side facts (for balance; each from >=2 seats): C2's full counting chain at
96379ae (f29-gate 7/7, frontier 29/29, recheck 9/9, binding unbound=0, census exit 0, absence
2→4) — R46bW2ExecRerunC2 Finding 3, R46bW2RevClaimC2 §1, R46bW2CritCalib2 re-scan,
R46bW2ScoutCensusPair; claims.json byte-identical post-freeze — own `diff` (empty) +
R46bW2RevClaimC2 §1.5; live page unchanged at 582877 bytes with every quote present —
R46bW2ScoutS074Live, R46bW2RevEntryClaims, R46bW2RevClaimC2; c1-gate still rejects the
attempt-1 P1/P2/P3 probes — R46bW2RevengerW2; the landing gate kills 13/13 mutants —
R46bW2MutLanding; f29-gate v1 H4/H5/H6 survivors are all pin-equivalent, and v1.1 closed the
midline-comment hole — R46bW2MutGate2; >=8 novel practitioner questions — R46bW2CritNovelty2;
lesson Gate-block quotes Q1-Q9 verified — R46bW2RevLessonGate.

=====================================================================
(2) CONTRADICTIONS BETWEEN SEATS (each named, none left smoothed)
=====================================================================

C1. c1 selftest health at the integration tree. R46bW2CritVerdictC1 finding 1 reports
    re-deriving `selftest cases=83 failures=0` from an archive of 96379ae (reads as: the c1
    instrument is healthy). R46bW2RevRegistryText FINDING 2 (+ my own run) shows the same
    committed bytes CRASH against the claims-pinned base export (`AssertionError: mutation was a
    no-op on corpus/knowledge/claim-gates.md`, rc=1). Resolution: different `--pure`.
    CritVerdictC1 used the L1's pure2 (its text says `--pure <pure>`; R46bW2RevSelftestW2 used
    the same pure2 and also got 83/0); RevRegistryText and I used the documented base export
    04af9bc9. Both readings are true; the defect is that the plain measure as documented
    (`--pure` = pinned base) aborts, and the passing configuration depends on an unpinned
    scratch export (F5). Not a contradiction once the invocation is named — but the report must
    not cite "83/0" without naming the pure.

C2. R46bW2MutGate1 (VERDICT BROKEN: 16 exit-level false greens on gate v1.1, each with a
    counterexample tree) vs R46bW2MutGate2 (VERDICT HOLDS: all 12 survivors of the frozen v1
    H4/H5/H6 set equivalent under pins). Resolution: disjoint scopes and kill semantics — v1.1
    vs frozen v1; all seven limbs vs H4/H5/H6 only; exit-level-with-counterexample vs per-limb
    pass-bit. Together they bound the gate rather than contradict: single-clause weakenings of
    v1.1 open 16 demonstrated holes, while every v1 H4/H5/H6 survivor is pin-equivalent. The
    receipt disclosures each seat corrects are different limbs ((a)-(f) vs (e)).

C3. R46bW2CritScope (VERDICT BROKEN: item-3 false-pass recipe) vs R46bW2RevEntryClaims (VERDICT
    HOLDS: "the rule itself is actionable and correctly sourced"). Resolution: different seams
    of the same artifact — the four-step rule is actionable as a checklist (RevEntryClaims §11),
    while its item-3 conditional mis-states the source's trigger (CritScope). Compatible; both
    land on the L1 fix list (F10).

C4. c1-gate at the integration: R46bW2ExecRerunC2 Finding 4 prints `c1-gate fixed=2/7 exit=1`
    at 96379ae while R46bW2RevengerW2 §1 prints `c1-gate fixed=7/7 exit=0` at fe0f56b.
    Resolution: different `--baseline` — 04af9bc9 vs the era pure 914ca0b (the wave-1 S7
    era-dependence, both seats quote their commands). Not a regression on either side.

=====================================================================
(3) THE THREE FINDINGS THE L1 MUST FIX BEFORE THE REPORT (ranked)
=====================================================================

RANK 1 — Make the C1 instrument chain runnable and re-run it at the final revision, then commit
    honest receipts. As landed (96379ae): the c2 selftest dies at import (F1); even repaired it
    is 147/101 against the committed v1.3 counter (F2); the f29 selftest aborts on the landed
    lane (F3); the c1 selftest crashes against the pinned base export (F5); and the battery's
    c2 and f29 legs both print BASELINE-DIRTY — while the only after-receipt is a truncated,
    mislabeled untracked file (F6) and the round's own SCORECARD/SHONEN/LOG cells cite receipts
    that do not exist at the commit. Until this is fixed and re-run, neither C1's after-value
    (`uncaught=0` both counters, extended selftest failures=0 baselines) nor the f29 frozen duty
    can be evidenced, and the honest-stop list is the report's headline. The L1 has already
    started (import order, f29 28/29 guard, g2 junk rework, ledger floors — all uncommitted in
    the working tree at writing); what remains visible from here: re-base or relax
    `ctl-committed-tip-direct` (it can never read 7/7 at a 29-row/66-entry tip), fix
    m_anchor_moved for the pinned base (or pin a reproducible pure and document it), finish the
    ledger-floor bump on r46-c2-gate.py's EXEMPT_BASE_SIZE (still 30696 in the working tree —
    own grep at writing; the f29-gate LEDGER_MIN_BYTES was bumped to 40843 but the c2-gate
    constant MutPinAmend attacked was not), then run controls/final-measure.sh to completion and
    commit the full receipts without pipeline-masked exit codes.

RANK 2 — Close the equivalence-proof gaps the C1 kill rule prices in. The f29 mode has three
    uncaught mutants (H1b, H7a, H7c) whose proofs were uncommitted at the landed tree; the L1's
    22:03 rerun still shows `uncaught=3` with `equivalent=0` even after adding the map entries
    (map values are CWD-relative — SentFinal D6 — so verify the battery actually consumes them);
    G6b's committed proof argues a non-existent clause and is nominal for the battery's mutant
    (MutSelfC2 F6 — rewrite it around the pin arithmetic, which does hold); G7a/G7c's proof
    rests on an unpinned fleet-root census script (pin its sha in the proof). Without this, the
    battery's `uncaught=0` line — the number the kill rule consumes — stays red or nominal.

RANK 3 — Fix the four landed-entry wording defects (F10): item 3's trigger ("uses another
    numbering authority's identifier" → coverage by another CNA, directing assigner selection
    back to F07), the false "whole capture is body prose" sentence (lines 1/4/7 are chrome),
    the "in the order the page states it" overstatement for steps 3-4, and the "three cases …
    publish without a fix version" overcount (case :40 says wait to disclose). All are one-line
    wording fixes; two were wave-1 findings that landed anyway. Separately, log the receipt
    corrections F11 names (3/7→6/7 controls; the (e) reason; 9-vs-10 tally; fixture
    rebuildability) as errata against the frozen record, and repair the dangling
    controls/freeze-controls.txt pointer in claims.json's `control` field.

Secondary (named, not ranked): pin or hermeticize the instrument path constants (LANE_CD,
LANE, CENSUS, the dead --pure defaults — SentFinal §3 proves erratum E2's fix claim false);
fix the f29-gate docstring "v1."→v1.1 and the registry row's "planned" status (RevRegistryText
FINDING 5, SimplW2 F6); land the F29 Search-log / Registry-changes bullets as real sections
(the committed draft-scaffold blocks carry line references stale by +1/+13/+23 —
ScoutCensusPair Finding 6); decide the two cosmetic receipt-format questions (do-nothing
control signal encoded only in FAIL-line count — MutSelfF29 F6; `grep -c 'def case_'` prints
0/0 — RevRegistryText gap 3, RevSelftestW2 secondary).

=====================================================================
LIMITATIONS
=====================================================================
- Read-only connector: no lane/fleet file was edited (the only writes are this report and my
  scratch), no git/jj mutation, no installs. Scratch `/fast/scratch/hyaku/kasegi-r46/
  R46bW2ConnW2` removed on exit.
- 5 of 32 wave-2 reports were unlanded at writing (ExecRerunC1, ExecRerunLive, RevClaimC1,
  MutSelfC1, CritErrata2); all are C1-chain seats whose territory is covered by the landed
  seats cited above, but their per-mutant lines (esp. MutSelfC1's c1 set M06-M20) are quoted
  here only via second-hand corroboration, not read first-hand. If any lands before the L1
  finalizes, re-check it against F1-F3.
- The L1's integration was actively moving while this report was written; every "(fix in
  progress)" note is a 21:36-22:03 working-tree observation, uncommitted, and must be re-verified
  at the next commit. Findings are stated against the landed integration tree 96379ae that the
  wave was dispatched to attack.
- Re-runs I performed myself: claims.json byte-diff vs fe0f56b (empty); c1 selftest vs a fresh
  04af9bc9 export (AssertionError, rc=1); f29 selftest on the live lane pre-fix (28-abort) and
  post-fix (30/0); c2 selftest --help pre/post fix; EXEMPT_BASE_SIZE / LEDGER_MIN_BYTES greps;
  the `| tail` exit-masking demonstration. Everything else is quoted from the named seats.
- Live-page state is quoted from ScoutS074Live / RevEntryClaims / RevClaimC2 (read-only fetches,
  HTTP 200, 582877 bytes); I made no live fetch.
