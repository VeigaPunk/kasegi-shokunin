VERDICT: INFO

# Prior-art scout — round-46 hygiene (seat R46ScoutPriors)

Question: which existing criteria (corpus/QUALITY.md R38-R49) and instruments already cover
(a) a frozen counter replayed at base, (b) do-nothing/marker-only controls, (c) a recheck line
that fails closed vs one softened to `true`, (d) append-only checks of lane files, (e) plain
second measurements — with path:line and whether a gate enforces it today; and do R50-R52
duplicate any of it?

Revs read: lane HEAD `323d1f5` (freeze `9f23aab` and base `914ca0b` both verified ancestors via
`git merge-base --is-ancestor`); `git status --porcelain -- corpus SKILL.md SCORECARD.md
SHONEN.md LOG.md PROVINCE.md` printed 0 lines, so working-tree bytes = HEAD bytes for everything
cited; corpus/QUALITY.md and freeze-check.py last changed at `3106889` (round-45 integration).
No LSP device exists in this seat's toolset; every citation below is a file read/grep of those
bytes or a command I executed. Scratch root `/fast/scratch/hyaku/kasegi-r46/R46ScoutPriors/`
(TMPDIR always set explicitly; base tree = unedited copy of the L1's pure base export, verified
64 knowledge entries; removed before this report was yielded).

## (a) Frozen counter replayed at base — COVERED, gate live at freeze time

- R47, corpus/QUALITY.md:380: "A frozen counter is replayed on the cheapest do-nothing control
  (the unmodified base tree ...) and must print its declared before-value BEFORE data ... R47
  binds the declared before-VALUE, read as a whole line, and is mechanised by
  `corpus/instruments/freeze-check.py`, which ... fails with `FC-NO-MATCH` when the line is
  absent or `FC-AFTER-AT-BASE` when the do-nothing tree already reads the after-value"; row ends
  `enforced-by: corpus/instruments/freeze-check.py`.
- Mechanisation: freeze-check.py:25 `REQUIRED = ("counter_cmd", "expect_before", "expect_after")`;
  :163-167 whole-line expect_before equality (`fixed=0` does not match `fixed=0x`, R41) with
  FC-NO-MATCH at :165 and FC-AFTER-AT-BASE at :167; FC-BASE-MUTATED at :160 (counter may not
  change the base, path+size+mtime_ns); exit rule :176-177.
- Enforceable by a gate today: YES — but it is a freeze-time gate, not a standing tree gate.
  This round's freeze record already carries it: .ufo/waves/round-46/freeze.txt:8
  `controls controls/freeze-controls.txt (total=9 red=9 green=0); freeze-check claims=2 base_ok=2`.
- My re-run (frozen counters replayed at the pure base export through freeze-check):
  `TMPDIR=$S/tmp python3 <lane>/corpus/instruments/freeze-check.py --claims <lane>/.ufo/waves/round-46/claims.json --tool-root <lane> --base $S/base --work $S/fc`
  ```
  claim C1 base_read=c1-gate fixed=1/7 exit=1 verdict=ok
  claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok
  freeze-check claims=2 base_ok=2 exit=0
  freeze-check_exit=0
  ```
  Both counters printed exactly their declared expect_before (claims.json:15 and :32) at base.

## (b) Do-nothing / marker-only controls — do-nothing COVERED (gate); marker-only PARTIAL (receipt + kill rule + round-45 selftest)

- Do-nothing at base: R47 (QUALITY.md:380) makes it mandatory per freeze; freeze-check.py:167
  FC-AFTER-AT-BASE is the do-nothing discriminator (docstring :22-23: "a counter already green at
  the base is a do-nothing pass"; selftest cases `3-do-nothing-green-only-after-line` and
  `3b-after-line-present-beside-before-line` at :269-273).
- Marker-only/junk controls exist as committed receipts:
  .ufo/waves/round-46/controls/freeze-controls.txt has nine controls, all red — c1 do-nothing
  (:1), c1 marker-only (:11 "two recheck lines replaced by `true`"), c1 fabricated-anchors (:21),
  c1 single-anchor-file (:31), c1 gutted-entry (:41), c2 do-nothing (:51), c2 junk-row (:61),
  c2 fabricated-quote (:71), c2 uncited-filler (:81), `controls total=9 red=9 green=0` (:91).
- Enforcement of those receipts is by kill rule + non-author reading, not a runner:
  claims.json:13 (C1: "or if any control in controls/freeze-controls.txt grades fixed=7/7"),
  claims.json:30 (C2), same pattern last round (.ufo/waves/round-45/claims.json:13 "(do-nothing
  base, marker-only tree) grades fixed=5", :24).
- Mechanical prior art: round 45's counter selftest BUILDS and GRADES a marker-only tree —
  r45-counters-selftest-c1.py:838 `line_case("control-marker-only", m["total"] == 0 and m["rc"] == 1, ...)`;
  and r45-c2-gate.py:30-36 documents v1.1 hardened because wave-1 built marker/junk/fabricated
  trees that v1 graded green. The r46 gates have NO selftest mode (r46-c1-gate.py argparse is
  --entry/--root/--baseline/--work only; r46-c2-gate.py USAGE is `--root TREE` only).
- My re-runs (do-nothing discrimination, both reproduce the receipts byte-for-byte):
  `TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c2-gate.py --root $S/base`
  ```
  gate G7 pass=1 read=census-rc=0 ok-line=1        (all of G1-G6 pass=0; elided here, full 8 lines in run log)
  c2-gate fixed=1/7 exit=1
  ```
  and on my own marker-only mutant (recheck lines of claim-gates.md:125 and
  claim-package-contract.md:68 replaced by `cd <lane> && true`):
  `TMPDIR=$S/tmp python3 <lane>/corpus/instruments/r46-c1-gate.py --root $S/mut --baseline $S/base --work $S/work`
  ```
  gate L1 pass=1 read=gated=22 broken=0 lines=64/base=64
  gate L2 pass=1 read=base-gated=24 regrounded=2 claim-gates.md,claim-package-contract.md
  gate L3 pass=0 read=bad=claim-gates.md,claim-package-contract.md
  gate L4 pass=0 read=bad=claim-gates.md,claim-package-contract.md
  gate L5 pass=0 read=bad=claim-gates.md,claim-package-contract.md
  gate L6 pass=0 read=mutants=0 survivors=none
  gate L7 pass=1 read=still-gated=22 changed=none
  c1-gate fixed=3/7 exit=1
  ```
  identical to controls/freeze-controls.txt:11-20. Enforceable today: do-nothing YES (freeze
  gate); marker/junk PARTIAL — red receipts + kill rules, mechanically graded only inside the
  round-45 selftests; the round-46 controls are not executed by any instrument.

## (c) Fail-closed vs softened-to-`true` — measured hole in the old metric; mechanical only via r46-c1-gate (round-scoped)

- Definitions: recheck-audit.py:66-71 "a line whose lane-root run fails closed (`fail-closed` in
  the receipt) counts as passing its form limbs and is reported separately, because the base it
  guards is absent"; :161-162 class is `"gated" if limbs["parse"] else "broken"`; the summary
  line :447-450 prints "gated = the line runs and fails closed on an absent base".
- The hole, measured by me. On the marker-only mutant:
  `TMPDIR=$S/tmp python3 <lane>/corpus/instruments/recheck-audit.py --root $S/mut | grep -E 'claim-gates|claim-package-contract|^executes=|^lines=|^expect='`
  ```
  claim-gates.md                              frozen=110 strict=110000 lane=0   foreign=0   executes    FAIL
  claim-package-contract.md                   frozen=110 strict=110000 lane=0   foreign=0   executes    FAIL
  executes=42 gated=22 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
  lines=64 total=64 pass=62 fail-closed=22 parse_fail=0 cwd_fail=0 paths_fail=2 exit=1
  expect=present expected=64 missing=0 unexpected=0 exit=1
  ```
  The softened lines leave the `gated` population (24 -> 22): the headline metric moves on
  softening. The audit's exit stays 1 (it was already 1 at baseline for other entries), so the
  only audit-side trace is the per-line FAIL and `paths_fail=2`. The plain reporter moves too and
  never judges:
  `score-gap.py --root $S/tip | grep -E '^recheck: |^gap: '` ->
  ```
  recheck: lines=64 executes=40 gated=24 broken=0 exit=1
  gap: 24 of 64 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
  ```
  vs the same command on the mutant -> `gap: 22 of 64 ...`, and both runs exit 0
  (score-gap.py:53-54: "Exit status: 0 on a complete read (even when the lane's own gates are red
  — the reporter reports, it does not judge)"; gap_line at :215-219).
- The mechanical discriminator today is r46-c1-gate L3 (:184-189: the recheck line must name no
  `~/`/`$HOME`/`/home/` path (HOME_RE :62) and must run `r46-c1-gate.py --entry
  corpus/knowledge/<itself>`), backed by L5 append-only (:196-202) and L7 byte-identical
  still-gated lines (:237-239) — my marker-only run above shows L3/L4/L5 pass=0 (fixed=3/7),
  i.e. the counter refuses to credit the softening. Scope limit: round-46 only
  (SECTION = "## Re-ground (round 46)" :54, TARGET_GATED = 22 :55). Pre-r46 no row or instrument
  catches softening; nearest prose is R38 (QUALITY.md:337), which forbids "editing the frozen
  counter to fit the grade" — a grading-side duty, not a recheck-side one. Enforceable today:
  YES via r46-c1-gate (C1 counter_cmd claims.json:14, and post-landing the re-grounded entries'
  own recheck lines self-host it at every future audit); NO via the pre-existing instruments
  alone (demonstrated above).

## (d) Append-only checks of lane files — COVERED per scope, no standing whole-lane gate

- Convention (prose): the R6 form heading every QUALITY addition block — QUALITY.md:341 "R6 form:
  every line above keeps its number ... are not edited" (with pinned prefix `head -c N |
  sha256sum` + `wc -l`), repeated at :376 for the R45 block. I found no instrument that re-derives
  the QUALITY.md prefix digests; enforcement is landing review plus scoped counters.
- Mechanical instances that DO exist today:
  - Knowledge-entry set cannot shrink: recheck-audit.py:44-56 (knowledge-expected.txt set
    equality), :188-194 `expected_mismatch`, :390-391 (expect_ok in the exit rule). My run on a
    scratch tree with one entry deleted:
    `recheck-audit.py --root $S/del --quiet` ->
    ```
    lines=63 total=63 pass=63 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1
    expect=present expected=64 missing=1 unexpected=0 exit=1
    ```
  - QUALITY.md round-block append-only was machine-guarded in round 45: counter limb R2 spec at
    r45-counters-selftest-c1.py:12-13 ("an append-only `## Round-45 additions` block in
    corpus/QUALITY.md") with the mutant `r2-quality-prefix-edited` — "baseline QUALITY.md edited
    (not append-only)" (:663) — expected rejected.
  - Per-entry re-grounds: r46-c1-gate L5 (:196-202, every BASE line except the recheck line is,
    in order, a prefix of the tree's lines); the gutted-entry control (controls:41-50) shows L5
    is the limb that stays red (fixed=6/7) when a body is deleted to un-gate.
  - Whole knowledge dir: r46-c2-gate G6 pins base names AND content by digest (:63-64,
    :283-291); my base run printed `knowledge=64 base-names-intact=1 entry-bytes-ok=0`.
  - Records: R38 (QUALITY.md:337) corrections are appended, "never by softening the grade in
    place"; R39 (:351) receipts are "one invocation writes it once and nothing appends to it or
    edits it afterwards". Closure scripts check QUALITY rows as rows, not prose
    (e.g. r36-closure.sh:414-418 supersession-row grep with the prose-only mutant at :688-690).
- Enforceable today: YES per scope (entry set, round-45/46 counter scopes, per-entry re-grounds);
  NO single standing append-only gate covers SCORECARD.md/LOG.md/SHONEN.md.

## (e) Plain second measurements — NOT covered; convention only, nothing gates it

- Today's practice: claims carry `plain` arrays (claims.json:17-21 for C1, :35-41 for C2), a
  `secondary` counter (:34), and `freeze_tree_reading` (:22, :42). No QUALITY row requires any of
  them and no instrument checks their presence: freeze-check.py:25 REQUIRED lists only
  counter_cmd/expect_before/expect_after.
- Nearest existing rows: R45 (QUALITY.md:371) — a capability row enters SCORECARD only with the
  demonstration command and its printed output (scoped to capability rows, not claims); R43
  (QUALITY.md:369) — "a frozen claim's `before` cell must be the literal its own cited control
  printed" (the r42 mine: before said `closed=10/12` while the cited do-nothing.txt:16 printed
  `closed=8/12`), machine-graded by K17 (`corpus/instruments/r43-limbs/k17-claims-before.sh`,
  named at the R43 row's tail).
- score-gap.py is itself a committed plain-style second measurement for the depth axis
  (README.md:353: "Not a claim; asserts no score move") but by design cannot discriminate
  anything (exit 0 both at tip and on my marker-only mutant, gap 24 vs 22 — runs quoted in (c)).
- Enforceable today: NO. In-vivo motivation for R52: C2's before-value differs per start tree —
  `c2-gate fixed=1/7 exit=1` at base (my run above) vs claims.json:42 "c2-gate fixed=2/7 exit=1
  at the freeze tree (G4 capture + G7 census)" — and no instrument replays the freeze tree
  (freeze-check takes only `--base`; freeze-check.py:20).
- Negative finding: capture-binding-check.py covers NONE of (a)-(e). Its rules A-D bind capture
  manifests to registry rows and provenance (B3 rejected-row-anchor: docstring :44-47, code
  :338-339, selftest case :942-944); no current claim invokes it (claims.json:14 and :31 name the
  r46 gates). It is prior art for content-binding discipline (R49 names it at QUALITY.md:382),
  not for counters/controls/softening/append-only/plain measures.

## R50-R52 vs existing rows

- R50 (landing order: report only after the cited lane commit exists on the remote and is not
  newer than the report commit; draft definition at .ufo/waves/round-46/build-wave1-spec.py:103):
  NO overlap with any existing row. Nearest are R44 (QUALITY.md:370 — orders a freeze label
  against its containing commit; different object, no remote limb) and R39 (:351 — binds a
  receipt's run-utc to execution, not a report to a pushed commit). Keep as drafted; the planned
  instrument is r46-landing-gate.py (spec :103).
- R51 (re-ground must name committed anchors per current claim and keep every old line; spec
  :103): NO existing ROW, but two overlaps to cite in the grounded-in cell: (i) R48
  (QUALITY.md:381) already states the principle for counter limbs ("every limb binds content:
  ... located quotes at their anchors") — R51 applies it to un-gating recheck lines; (ii) it is
  already mechanised for round-46 scope by r46-c1-gate L2/L3/L5/L7 (:182-202, :237-239). The
  row's delta is durability beyond `## Re-ground (round 46)` (:54) and any future un-gating;
  draft it as the generalisation, with r46-c1-gate as enforced-by evidence, or it reads as a
  re-mint of R48.
- R52 (plain second measurement + before-value per start tree; spec :104): PARTIAL DUPLICATE of
  R47 (QUALITY.md:380) — the before-value-at-base half IS R47 and freeze-check already mechanises
  it (my (a) run). Also touches R43 (QUALITY.md:369), which already binds a claim's `before`
  cell to the literal its cited control printed (K17). The genuine deltas: (1) the FREEZE-tree
  second reading (claims.json:22/:42 carry one; nothing replays it), and (2) a REQUIRED plain
  second measurement beside the pinned counter (today ungated). Draft R52 explicitly as those
  two deltas or it duplicates R47/R43.

## Re-run log (all commands I executed; outputs quoted verbatim above)

1. freeze-check replay of both frozen counters at the pure base export -> `freeze-check claims=2 base_ok=2 exit=0` (9.2 s wall).
2. r46-c2-gate do-nothing at pure base -> `c2-gate fixed=1/7 exit=1` (G1-G6 pass=0, G7 pass=1).
3. r46-c1-gate on my marker-only mutant vs base -> `c1-gate fixed=3/7 exit=1` (L1/L2/L7 pass; L3/L4/L5/L6 red).
4. recheck-audit on the mutant -> two `executes FAIL` lines, `executes=42 gated=22`, `paths_fail=2`, exit 1.
5. score-gap at tip -> `gap: 24 of 64 ...` exit 0; on the mutant -> `gap: 22 of 64 ...` exit 0.
6. Deletion mutant (one knowledge entry removed) -> `expect=present expected=64 missing=1 unexpected=0 exit=1`.
7. Read-only git: ancestry of base/freeze vs HEAD; ls-files (all eight instruments tracked);
   `git status --porcelain -- corpus ...` -> 0 lines.

## Limitations

- I re-ran 3 of the 9 controls (c1 do-nothing via freeze-check, c1 marker-only, c2 do-nothing);
  the fabricated-anchors, single-anchor-file, gutted-entry, junk-row, fabricated-quote and
  uncited-filler receipts I read but did not re-derive.
- Scratch recheck-audit runs carry a cd-target mismatch (recheck lines `cd` into the live lane
  while `--root` is a scratch copy), so strict-limb counts in those runs are distorted; the
  frozen-limb verdicts, classes and gated counts quoted are unaffected, and the tip baseline was
  measured with the claims' own command shape (`score-gap.py --root <tree>`).
- I did not replay any counter at the freeze tree — that unchecked second reading is exactly the
  R52 gap identified above.
- The r46 gates have no selftest mode; their nine controls are enforced by kill-rule clauses
  (claims.json:13, :30) plus non-author reading, not by any runner.
- Enforceability verdicts describe mechanisms that exist and run today (freeze-time gate, claim
  counter_cmd at landing, per-entry recheck lines, selftests); none of them is a continuously
  scheduled service — each fires when its round's procedure invokes it.
