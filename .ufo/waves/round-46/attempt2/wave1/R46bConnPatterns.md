VERDICT: INFO

Seat R46bConnPatterns — cross-seat pattern scan (round 46 attempt 2, wave 1), run last per the card.
Read every sibling report present at writing: 47 of 64 wave-1 reports
(`wave1/*.md`), plus the drafts they cite and the frozen artifacts (claims.json,
freeze.txt, controls/*.txt, S074.txt, manifest.json, r46-f29-gate.py, r46-mutbat.py,
both counter selftests, the gate-pin-amendment draft). Unlanded at writing (stated as a
limitation, not silently skipped): ExecSelftestC1, ExecSelftestC2, ExecMutbatF29,
MutBattery, MutF29b, MutSelfC1a, MutSelfC2b, ScoutSelftestC1Gap, RevMutbat,
RevSelftestDiff, CritKillC1, CritFreeze, ExecControls, ExecPlain,
ScribeLog, ScribeShonen, ScribeSkillRegistry. Two reports landed while this report was
being finalized and are incorporated: R46bMutSelfC1b (own-set mutation test of the C1
selftest — see S9) and R46bExecFixtureHarness (merged fixture builder + receipt-rebuild
selftest; VERDICT DRAFT-READY, consistent with S1/C2). Everything below is quoted with seat name
and located line; every discrepancy I assert was either re-run by me or corroborated by
≥2 independent seats. No lane/fleet file was edited; no git/jj mutation; scratch
`/fast/scratch/hyaku/kasegi-r46/R46bConnPatterns` removed on exit. No tools installed.

=====================================================================
(1) SHARED DEFECTS FOUND BY >= 2 SEATS (same false-green class)
=====================================================================

S1. The frozen R50 receipt's junk/fabricated control baseline is stale: receipt says
    `fixed=3/7 (H2/H5 red)`; the committed fixture + committed counter measure
    `fixed=6/7` with H2 GREEN. Seven independent sources, one root cause.
    - My own re-run (this seat): `python3 controls/f29-fixture.py --mode junk --dir …
      && python3 corpus/instruments/r46-f29-gate.py --root <junk>` printed
      `gate H2 pass=1 read=… table-rows=6 …`, `gate H5 pass=0 read=spans=7 located=2
      failed=5 uncited=0 cores=0/5`, `f29-gate fixed=6/7 exit=1`; fabricated printed
      `spans=7 located=5 failed=2 cores=4/5`, `fixed=6/7 exit=1`.
    - R46bExecSelftestF29.md "Discrepancies 1" (quote: "the receipt's junk/fabricated
      readings are wrong … I measure `fixed=6/7` for both (only H5 red)").
    - R46bCritKillC2.md ("junk reads 6/7 with H2 green … `gate H2 pass=1`").
    - R46bScribeEntryD.md Finding 2 (`fixed=6/7 exit=1`, H2 `table-rows=6` on both).
    - R46bScribeEntryB.md F-7 (tail: `f29-gate fixed=6/7 exit=1` for both modes).
    - R46bRevF29H4H5.md F8 ("the R50 receipt's junk/fabricated fixed totals do not
      reproduce at the freeze export … `fixed=6/7 exit=1` for both, H2 green in both").
    - R46bMutF29a.md §9 gives the root cause: the L1 built the receipt's junk/fab trees
      at 17:34:43 and then EDITED `controls/f29-fixture.py` at 17:35:19, so the receipt
      numbers came from a pre-edit fixture; its own leftover trees read `fixed=4/7`,
      "also not 3/7". Root cause located, not inferred.
    Same false-green class: a frozen control receipt grading red where the committed
    harness is green. The gate itself is fine; the control text is wrong.

S2. `r46-f29-gate.py` H1 reads comment-concealed frontier/registry rows as live — a
    defect tree grades 7/7. Two seats, two constructions, same class.
    - R46bRevF29H1.md F4 (`a6-comment-oneline-f29`): one-line HTML comment smuggling a
      second F29 row → `gate H1 pass=1 read=rows=29 admitted=29 F29=admitted`,
      `f29-gate fixed=7/7 exit=0`.
    - R46bSimplifierDrafts.md O-1: the gate's copied `live_lines` (r46-f29-gate.py:115-126)
      is weaker than r46-c2-gate.py:120-132 (skips only lines *starting* with `<!--`);
      a tree with the F29 row and S074 row hidden inside multi-line comment blocks grades
      `fixed=7/7 exit=0`, while the attempt-1 counter on the same shape reads red
      (`c2-gate fixed=2/7 exit=1`). SimplifierDrafts explicitly notes R46bRevF29H1
      "reached the same hole independently … corroborated, not a one-off".
    Both seats note the R50 receipt's mutant/disclosure set does not cover this class.

S3. Both committed selftests default `--pure` to a dead path; a bare invocation crashes
    with FileNotFoundError instead of a usage error. Two seats, same one-line fix.
    - R46bScoutPureRecipe.md §1 (`PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` at
      selftest-c1.py:47 and selftest-c2.py:47; "PURE DEAD (missing)"; both tracebacks quoted).
    - R46bSentScratch.md F1 (same grep, same crash, plus the contrast with r45's clean
      `return 2` guard; recommends `required=True` — identical to ScoutPureRecipe's §5 fix).
    Impact: the freeze replay and any standalone reviewer re-run hits a traceback; the
    battery itself is unaffected (it passes `--pure` explicitly).

S4. The C2 selftest hardcodes a stale attempt-1 seat scratch dir, ignores TMPDIR, and has
    no `--work` flag; killed runs leave orphans in a shared directory. Two seats.
    - R46bSimplifierDrafts.md O-3 (selftest-c2.py:282 `seat_dir = … "R46W2ExecSelftestC2"`).
    - R46bSentScratch.md F2 (proves TMPDIR is ignored; lists three orphan `c2st-*` dirs;
      recommends the C1 selftest's line-575 resolution).

S5. `r46-mutbat.py`'s `equivalent` predicate accepts a ZERO-BYTE proof file, weaker than
    C1's own kill rule ("missing, empty, or falsified"). Two seats, same line.
    - R46bSimplifierDrafts.md O-2 (r46-mutbat.py:169 `mid in eq and os.path.isfile(eq[mid])`;
      "an empty file in the `--equivalent` map is graded `equivalent` … would still print
      `uncaught=0`").
    - R46bSentGateIntegrity.md Finding 5 (same line; exploit run: empty proof →
      `verdict=equivalent`; "The rule's protection therefore depends on a reviewer reading
      each proof by hand").
    This is the C1-axis mirror of S1: the number the kill rule consumes can be green
    without the rule's stated condition holding.

S6. On the post-F29 tree (29 rows / 66 entries / ledger grown) the frozen c2-gate — and
    the v1.3 ledger-exemption amendment built for it — CANNOT print 7/7, and the C2
    selftest's committed-tip control feeds the C1 battery's baseline. Three seats converge.
    - R46bRevClaimsErrata.md Finding 2.3 (G1 pins `len(rows) != 28` at r46-c2-gate.py:179,
      G6 pins `len(names) == 65` at :347; "the frozen counter cannot print 7/7 there
    regardless of the F29 content's quality").
    - R46bExecLedgerDraft.md §4 (measured: v1.3 draft on the 66-entry tree →
      `gate G6 pass=0 … base-intact=0`, `c2-gate fixed=5/7 exit=1`; on 65+ledger → 7/7).
    - R46bExecGatePinAmend.md F1/F2 (its own draft "does not and cannot fix this"; the
      battery's `ctl-committed-tip-direct` runs on the live lane → `BASELINE-DIRTY` →
      C1 kill rule `baseline_failures!=0` fires). My own diff of the amendment draft
      confirms line 350 still reads `len(names) == 65 …`.
    Same class: hard count pins that a growth claim necessarily breaks; all three seats
    leave the fix to the L1 (counters are read-only for seats).

S7. c1-gate's recorded 1/7↔7/7 pair is era-dependent: against the attempt-2 base 04af9bc9
    BOTH roots read 2/7. Three seats report the same 2/7 readings; one names the root cause.
    - R46bRevC1Lineage.md F1 (root cause: attempt-1's re-grounding landed BEFORE base
      04af9bc9 was cut, so `gated=22 == TARGET_GATED` and L1 passes at the do-nothing base;
      the 1/7↔7/7 pair only reproduces against the era baseline 914ca0b, reproduced
      byte-exact on pure2).
    - R46bExecNoharm.md F8 (`c1-gate fixed=2/7 exit=1` at base-vs-base and base-vs-live;
      "structural, not a regression").
    - R46bRevNoHarm.md Finding 2 (live-vs-base do-nothing 2/7, byte-identical readings).
    Not a contradiction once explained — but any seat spec that replays c1-gate against
    04af9bc9 expecting 1/7 or 7/7 produces a false regression flag.

S8. Census-output equivalence of the census-shape mutants is confirmed on BOTH counters
    independently: c2 G7a/G7c and f29 H7a/H7c are `rc==0 ⇔ ok-line` equivalent. Two seats.
    - R46bScoutSelftestC2Gap.md E4/E5 (census emits the ok line iff no E-code, script
      sources-census.sh:745; extension-free regex).
    - R46bExecSelftestF29.md (same two proofs for H7a/H7c on the f29 counter; recommends
      closing via the `--equivalent` map).
    R46bMutSelfC2a.md §4.1 independently re-proves G5c/G6b/G7a/G7c equivalents with
    per-pair word measurements on the real capture.

S9. (Landed at finalization; single seat, C1 selftest surface) An own-set mutation test
    of the COMMITTED C1 selftest shows the 76-case baseline misses whole clause families:
    R46bMutSelfC1b.md §3 derived 24 single-line mutants of r46-c1-gate.py disjoint from
    the battery table ("exact (old,new) overlaps with battery: []"), and ~20 of them
    SURVIVE the committed selftest (`failures=0`), each confirmed by an independent
    differential probe — e.g. N09-duplicate-row-id, N14-stray-table-rows, N15-cd-strip-
    allows-semicolon ("survived | DIFFERENT"). This is the C1-side instance of the
    false-green class S1/S5 warn about on other surfaces: the case-count baseline
    (76/0) is clean while whole clauses are unexercised. The wave's C1 selftest extender
    (ExecSelftestC1, unlanded at writing) is the seat meant to close exactly this; the
    point for the L1 is that the coverage hole is measured independently of the battery's
    own 20-mutant table.

=====================================================================
(2) CONTRADICTIONS BETWEEN TWO SEATS' VERDICTS ON THE SAME ARTIFACT
=====================================================================

C1. Frozen receipt junk/fabricated = `3/7` vs six seats' + my `6/7` — see S1. Resolved by
    R46bMutF29a.md §9's located root cause (fixture edited after the trees were built).
    Same artifact, opposite verdicts, explained.

C2. R50-receipt mutant count: `controls/f29-r50-receipt.txt` header and `freeze.txt` say
    "21 mutants, 11 defect-tree flips, 9 disclosed"; the table has 20 rows and H6 has only
    two mutants. R46bMutF29a.md §2/§7 (the missing `H6c-size-low` "is a live, isolable
    mutant … neither shown nor disclosed") vs the frozen record. R46bExecSelftestF29.md
    built `clause-c-cells-12` to grade H3a, implicitly treating the table as 21. The
    frozen count is wrong; the 21st mutant is real and killable.

C3. R50 receipt disclosures (a)/(b)/(c) claim H1a/H2b/H3a "cannot be isolated at gate
    level". R46bMutF29a.md §3-5 REFUTES all three with single-defect gate-level trees:
    (a) `probe-p1` "extra DISTINCT admitted row F30 … `BASE H1 pass=0` / `MUTANT H1
    pass=1` … the mutant IS isolated at gate level"; (b) `probe-p7` gutted `## Limits`
    (table in another section) flips H2; (c) `probe-p3` 12-cell S074 row flips H3.
    R46bExecSelftestF29.md is consistent (it grades (a)/(b)/(d)/(e) — and added (c) — in the
    selftest), so the wave's selftest work stands; what is false is the receipt's stated
    REASON. The claim's "frozen duty" premise ("not isolable at gate level") holds only
    for (d)/(e)/(f).

C4. R46bScoutSelftestC2Gap.md E1 classes c2 `G3a-cells-loose` as "equivalent-by-
    construction" (its 12-cell craft "stayed red under the mutant"). R46bMutSelfC2a.md §5
    contradicts with an end-to-end run: "appending the extra cell at the END of the row
    leaves positions 0..10 untouched … G3 itself flips" (`pristine … 'G3': 0` → `mutant …
    'G3': 1`). Resolution: MutSelfC2a's refutation stands — the E1 proof tested a craft
    that duplicated the anchor cell MID-row (shifting the positional literals); the
    append-at-end 12-cell row is the killer, so G3a needs a real selftest case, not an
    equivalence proof. (Same shape as MutF29a's f29 H3a refutation, C3 above.)

C5. R46bRevClaimsErrata.md Finding 3.3: "no `.ufo/waves/round-46/attempt2/counter-
    errata.md` exists" — vs R46bScribeLesson.md F10: the attempt-2 errata file "exists …
    written during this wave, frozen at `fe0f56b7`". I checked directly: the file EXISTS on
    disk, created 18:29 local, `git status --porcelain` shows `??` (untracked), and
    `git cat-file -e fe0f56b7:…/counter-errata.md` → "exists on disk, but not in
    'fe0f56b7'". Both seats are half-right: RevClaimsErrata's git-visible claim is false,
    ScribeLesson's "frozen at fe0f56b7" is false; the truth is an untracked wave-work file
    that the L1 must commit (or not) at integration.

C6. R46bScribeEntryF.md §3.4 prints `f29-gate fixed=7/7 exit=1` for its composed tree,
    while §3.6 prints `fixed=7/7 exit=0` for the restored entry and the gate's own code
    returns `0 if fixed == 7 else 1` (r46-f29-gate.py:366, read by me). Every other seat's
    7/7 reading carries exit=0 (e.g. R46bScribeEntryA.md §2.2, R46bScribeAdmission.md F4).
    Internal inconsistency in EntryF's report — the exit code in §3.4 is misprinted; the
    7/7 itself is not contradicted.

C7. Regression replay: R46bRevengerEscapes.md §6 ("No rebuilt defect tree reads green …
    no regression found") vs R46bRevPriorEscapes.md Finding 1 ("REGRESSION … the C1
    rebuild now reads red (hole closed), the C2 rebuild still reads green"). Same
    campaign, opposite headlines — but the trees differ: RevengerEscapes replayed the three
    CHEAPEST v1 trees (all flipped red at v1.2); RevPriorEscapes rebuilt R46MutC2a's S2
    junk-filler-row tree, which v1.2 still tolerates (bounded: exactly `real_rows − 6`
    junk rows). Both honest; together they delimit the v1.2 residual rather than contradict.

C8. The nature of the S074 capture: entry drafts B/C/D/F assert "the whole capture is
    body (prose)" (see M1 below), while R46bScoutF29Live.md F2 classes capture lines
    1, 4, 5, 6, 7 as "page chrome / the 'Who can use this feature?' callout" and
    R46bScribeEntryA.draft:9 says "its body prose is S074.txt:8-42 and the rest of the
    capture is page chrome and site navigation". Same artifact, opposite verdicts; the
    pinned bytes and the live scout side with A (see M1).

=====================================================================
(3) DRAFTS AGREEING ON A FACT THE SOURCE DOES NOT SUPPORT (M46-3 CLASS)
=====================================================================

M1. "The whole capture is body (prose), with no navigation chrome." Origin: every C2 entry
    drafter's card repeats it — `grep -c "the whole capture is body" wave1-spec.json` → 6
    (cards A-F), baked into build-wave1-spec.py. The drafts then assert it as their own
    observation of the pinned capture:
    - R46bScribeEntryB.draft/github-repository-security-advisories.md:11 ("the whole
      capture is that body") and :89 ("all 42 lines are body prose").
    - R46bScribeEntryC.draft/…:9 ("captured whole (42 lines, S074.txt:1-42; the whole
      capture is body prose, with no navigation chrome)").
    - R46bScribeEntryD.draft/…:89 ("the whole capture is page body").
    - R46bScribeEntryF.draft/…:9 and :43 ("the whole capture is body").
    - R46bScribeRowsC.draft/rows.md:18 (the S074 anchor cell: "the whole capture is the
      page body") — i.e. the fact would be committed into corpus/SOURCES.md.
    - Also asserted in report prose: R46bScribeEntryB.md F-1 ("The whole capture is body
      prose"), R46bScribeEntryD.md ("42 lines, whole capture is body").
    The pinned source does not support it: `cat -n corpus/source-snapshots/round-46-a2/
    S074.txt` line 4 is `Copy markdown` (a UI button label), lines 1 and 7 are
    `In this article` (in-page TOC markers). R46bScoutF29Live.md F2 located all 42 pinned
    lines in the live page and measured that exactly lines 1, 4, 5, 6, 7 are absent from
    the `.md` rendering — "page chrome / the 'Who can use this feature?' callout". Worse,
    the drafts quote line 6 (the callout) as located ground (EntryC draft QUOTE 1,
    EntryB draft Q02 cite S074.txt:6). Dissenting draft: R46bScribeEntryA.draft:9
    ("the rest of the capture is page chrome and site navigation") — corroborating
    evidence the claim is false. The f29 gate does not grade this sentence, so it is an
    honesty defect (M46-3), not a counter hole: the L1 should fix the wording in whichever
    entry/row it lands (EntryA's phrasing, or delete the sentence). EntryE's draft does
    not carry the claim.

M2. (Minor, same class-adjacent) All six entry drafts present the temporary-private-fork
    fact as part of the new maintainer-side ground; R46bCritNovelty.md finding 3 says do
    NOT count G3 as novel — "F28 already records the temporary private fork and says only
    the repository maintainer can merge changes from it (corpus/knowledge/github-private-
    vulnerability-reporting.md:23) … avoid presenting the fork fact alone as novel". The
    drafts' Overlap sections do contrast F28 on actor/stage, so this is a framing fix, not
    a falsification — but if L1 lands a draft whose "What is new here" leads with the fork,
    it repeats an overclaim the critic flagged in every draft it reviewed.

=====================================================================
(4) THE SINGLE MOST LOAD-BEARING OPEN QUESTION FOR L1 INTEGRATION
=====================================================================

Q1. How does the L1 make C2's own counter grade the post-F29 tree without breaking C1's
    measurement — given the counters are read-only for seats and every seat left it
    unresolved?

    Chain of established facts (each from ≥1 seat, key ones re-verified by me):
    (a) Frozen c2-gate G1 hard-pins 28 rows and G6 hard-pins 65 knowledge names
        (R46bRevClaimsErrata.md Finding 2.3; r46-c2-gate.py:179,347).
    (b) The v1.3 ledger-exemption amendment (R46bExecGatePinAmend.draft/r46-c2-gate.py,
        sha 10c3d816…) correctly implements R46bScoutLedger.md's three-touch spec
        (CONTENT_EXEMPT + EXEMPT_BASE_SIZE + re-derived pin 2c4ccfb6…; R46bRevLedgerAmend.md
        F8 independently proves the pin re-derivation is unavoidable) but keeps
        `len(names) == 65` at draft line 350 — my own diff of the draft against the frozen
        counter shows the five-edit change touches nothing else.
    (c) On the final tree (29 rows, 66 entries, ledger 30696→40803 bytes) the amended
        counter reads ≤5/7 (R46bExecLedgerDraft.md §4 measured 5/7 and 6/7 on the two
        intermediate trees; R46bExecGatePinAmend.md F1 measured 6/7 and 5/7).
    (d) The C2 selftest's `ctl-committed-tip-direct` case runs the counter on the live lane
        and must read 7/7 (R46bExecGatePinAmend.md F2; the case is at line 540 of the
        amendment's own selftest draft — read by me); the battery runs that selftest with
        `--lane` defaulting to the live lane (r46-mutbat.py:97-107), so a red committed-tip
        control prints `BASELINE-DIRTY` and fires C1's kill rule
        (`baseline_failures!=0`, claims.json C1).
    (e) Widening G1/G6 is itself a counter-limb change that C1's kill rule allows only as a
        logged erratum with a plain re-derivation (claims.json C1 kill_rule; R46bRevLedgerAmend.md
        "counter-errata question" section takes the byte-pin-amendment side and lists the four
        disclosure conditions (a)-(d) the erratum must meet, else "C1 must be read UNVERIFIED
        on the frozen counter").
    So the L1 must land a SECOND amendment (G1/G6 widened to 29/66 + the F29 entry exempted
    from the base-names pin — exactly what R46bExecLedgerDraft.md §4 told the owning seat)
    together with the battery/selftest M-table touch-ups (SentScratch.md F3: any edit to
    r46-c1-gate.py:232 must land with the battery's M20 old-substring or the battery aborts),
    and the whole bundle must be logged in the attempt-2 errata file (the untracked one from
    C5) with plain re-derivations. If any link is skipped, either C2's gate can never print
    7/7 on the landed tree, or C1's battery prints BASELINE-DIRTY, or the amendment is an
    unlogged limb change. No seat could do this; it is entirely the integration call.

    Sharpening addendum from R46bSentGateIntegrity.md Finding 1 (HIGH, single seat but
    load-bearing): even a perfectly widened counter's `uncaught=0` is currently only as
    strong as the tree's self-report — the battery executes the TREE's own selftest
    unpinned and reads `failures=(\d+)` out of its stdout (r46-mutbat.py:98-107), and a
    tree-shipped stub selftest can print the exact `uncaught=0 BATEXIT=0` after-state with
    zero real coverage (exploit run quoted). For THIS round's honest lane tree the number
    is still meaningful, but the C1 after-value's integrity rests on reviewers reading the
    extended selftests, not on the instrument — worth one errata sentence at integration.

Secondary open questions the L1 also owes (named, not ranked): which of six gate-equivalent
entry drafts to land — the gate cannot discriminate them (R46bCritKillC2.md: an entry with
NO decision rule grades 7/7; H1 also accepts a junk-id row and an F29 sources cell of
"S074; S999"), and four of the six carry the M1 sentence; the receipt-text corrections from
S1/C2/C3 (the receipt is a control record, and R46bExecSelftestF29.md, R46bMutF29a.md and
R46bRevF29H4H5.md each recommend amending it at integration); and the two-seat collision on
r46-counters-selftest-c2.py (R46bExecGatePinAmend.md F4 messaged R46bExecSelftestC2 with its
five edits — the L1 must merge the extension and the ledger-mirror edits, which both touch
land_c1 and the CONTENT_EXEMPT mirror).

=====================================================================
LIMITATIONS
=====================================================================
- I am a read-only connector; every check above is either a quote from a landed sibling
  report or a re-run I performed (the junk/fabricated gate runs in §S1; the errata-file
  existence check in §C5; the amendment-draft diff and the all-body greps; the gate exit-code
  reading). I did not re-run the battery (multi-hour at this host's 160-270 load on 32
  cores per R46bMutSelfC2a.md §4 — R46bScribeScorecard.md F1 independently hit a 2400 s
  wall clock mid-battery) and I did not re-derive any frozen before-value beyond the three
  gate runs above.
- 17 of 64 wave-1 reports had not landed at writing (listed at the top). The heaviest C1
  seats (ExecSelftestC1/C2, ExecMutbatF29, MutBattery, MutSelfC1a, ScoutSelftestC1Gap)
  are mid-run; their verdicts can only add C1-mutation detail. If one of them contradicts a
  pattern above, the contradiction is the finding — the patterns here are cross-seat and
  each cites ≥2 independent sources except where marked "single seat" (S9, and the
  SentGateIntegrity addendum to Q1).
- Line numbers cited inside drafts/reports are as of the files at writing (several drafts
  were moving targets: R46bSimplifierDrafts.md §7 records the f29 selftest draft moving
  861→876 lines during its read).
- A /tmp path is cited nowhere; my only scratch, `/fast/scratch/hyaku/kasegi-r46/
  R46bConnPatterns`, was removed after the three confirmatory gate runs; every other check
  above reads committed lane bytes or quotes sibling reports' printed output.
