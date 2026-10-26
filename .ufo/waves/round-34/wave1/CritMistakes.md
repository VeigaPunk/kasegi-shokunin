author: CritMistakes-2 (critic seat, round 34 wave 1, kasegi lane)
lane: kasegi-shokunin @ working tree on base `014ee2d7aa8c3c095ff57ae51097606a9906228c`
claims freeze: `29f606dbdd28aff6fd4573ab4b90788bbb90af13` (committer 2026-10-26 02:28:39 -0300)
write scope: this receipt only (lane repo). No git/jj mutation. Scratch
`/fast/scratch/hyaku/kasegi-r34/CritMistakes/` created and deleted before yield.

# Critique — the lesson's Mistakes rows (M34-1, M34-2, and the rows that are missing)

Assignment: each Mistakes row must carry (1) a real evidence pointer, (2) a `captured-by` (or `none`),
(3) a fix, (4) the fix shown able to fail (a red-before run). Flag any row that is prose without a
reproducible check. This seat is a leaf: it files findings and a verdict, it does not judge the round.

**State at review time.** `corpus/lessons/round-34.md` does not exist (`ls corpus/lessons/round-34*` →
`No such file or directory`, exit 2; ScribeLesson seats still waiting). The Mistakes rows therefore exist
only in the frozen claims (`non_claim_frontier_items.mistake`, two sentences) and in four landed artifacts
that cite those ids (`corpus/QUALITY.md:226,228`, `SCORECARD.md:1034-1035`, `ExecErratum2.md:124`,
`RevClaimsFreeze.md:214`). I critique what exists, and I state the field set the lesson must land — the
round-33 schema the claims point at is `Class / evidence pointer / Captured by / Criterion / Fix /
Verified` (`corpus/lessons/round-33.md:91-96`, M33-1…M33-6).

## Verdict (up front)

| Row | Evidence pointer | captured-by | fix | fix shown able to fail | Row verdict |
|---|---|---|---|---|---|
| M34-1 "all mutants killed" | **real** (4 red-before lines quoted below) | **defect (minor)** — a criterion id, not a seat | **real** (`kill-rule-check.py`) | **yes, measured**: `survivors=0` at tip and `witness_survivors=1 witness_exit=1` on the CTL-equivalent row | **sound** — one field to repair |
| M34-2 `<LANE_HASH>` markers | **real** (2 → 0 at `SCORECARD.md:988,1087`) | **defect** — `none` is falsified by two committed sentences | **incomplete** — the mention sweep was not run; 2 of 3 corpus occurrences survive | **no**: the closure verdict in a landed receipt (`RevErrata.md:44`) is false on one command | **not landable as filed** — three fixes below |
| *M34-3 (missing — required)* post-freeze counting-literal erratum vs R22 | present in bytes, no row anywhere | `CritMistakes` (this seat) + `ScoutDatawalk` F-a | not filed | red-before exists and R22 as written **cannot** produce it | **must be a row** |
| *M34-4 (missing — recommend routed-only)* lane-root scratch file `selftest-baseline.txt` | real | `RevC1BeforeAfter` §F5:238-243 | delete/relocate | check exists (`git ls-files`) | routed defect, **not** a mistake row |

So: **M34-1 passes the assigned bar with one field correction; M34-2 does not pass** — its fix's
"able-to-fail" claim is contradicted by a command; and the round contains at least one further mistake
(the post-freeze erratum against R22) with no row at all, plus a second instance of the same class in the
frozen C2 predicate (`PASS F17 ids=S051`) that greps 0.

---

## F1 — M34-2's closure verdict is false: `<LANE_HASH>` occurs 3 times in `corpus/`, and one site still
asserts the markers are unfilled

```
$ grep -rc '<LANE_HASH>' corpus/ | grep -v ':0$'
corpus/lessons/round-33.md:2
corpus/lessons/round-33-verifier-spotcheck.md:1
total_corpus=3
$ grep -n "L1's edit" corpus/lessons/round-33.md
7:…the two header placeholders are the L1's edit (open item 1).
126:…Its two `<LANE_HASH>` markers are the L1's edit; this lesson does not verify the appended numbers…
$ grep -n '<LANE_HASH>' SCORECARD.md      # the C1-scoped count
(no output)  count=0
$ git show 014ee2d:SCORECARD.md | grep -n '<LANE_HASH>'
988:`<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the
1087:**Round-33 final lane commit: `<LANE_HASH>`** — the L1 replaces this marker. Every value in
base_count=2
```

Against the landed receipt that closes R1:

`.ufo/waves/round-34/wave1/RevErrata.md:44` — "Repo-wide `<LANE_HASH>` occurrences remain only in
historical round-31/32/33 wave specs/results/receipts and round-34 planner/control files (… ) — **none in
`SCORECARD.md` or any `corpus/` production file**. The C1 claim scopes the count to `SCORECARD.md`;
satisfied."

That sentence is falsified by the first two commands: `corpus/lessons/round-33.md` is a `corpus/`
production file and carries the token twice, and `:126` still states the markers are unfilled and
L1-owned. The same seat family already knew this — `ExecScorecardMarkers.md:140-145` discloses
`round-33.md:126` and leaves it "the L1's call". So two committed round-34 receipts state different
values for one byte surface, and the one that states `none` is the review-side closure.

**Why the C1 claim still verifies.** The frozen kill rule scopes `<LANE_HASH>` to `SCORECARD.md`
(`claims.json` C1 `kill_rule`; counting command `grep -c '<LANE_HASH>' SCORECARD.md -> 0`), and that
reads 0. This is a Mistakes-row defect, not a C1 defect.

**Class of the row.** M34-2 is filed as "landing / reference-drift". A reference-drift row whose fix does
not sweep every mention is the same drift one file over: `:126` now describes state that no longer exists.
Round 33's R7 erratum already sets the standard this row must meet — it classified *every* `S050.txt:69`
citation in the lane and the fleet report in a table before correcting them
(`corpus/lessons/round-33.md:190-204`, "**Every citation of `:69` for that sentence is corrected to
`:70`**", sweep re-run at `RevErrata.md:94`, 8 matches / 4 files, each classified).

**Smallest safe correction** (append-only; no in-place rewrite of round-33 bytes):
1. Append a correction line to `corpus/lessons/round-33.md` (below the R7 erratum block, same file since
   round 34 already appends there) reading: the two `<LANE_HASH>` markers at `SCORECARD.md:988,1087` were
   replaced in round 34 (`7963976e…`, correction paragraph `SCORECARD.md:1116-1119`); open items 1 and 2
   at `:7,:126` and the table cell at `:17` describe the pre-replacement state.
2. Append a correction to `RevErrata.md`'s scope line (as a separate file in the wave dir, or as an L1
   erratum — this seat cannot edit a peer receipt) naming the three corpus occurrences and the one
   legitimate one (`round-33-verifier-spotcheck.md:165` must quote the token; it is R1's finding).
3. M34-2's closure check becomes sweep-shaped, not file-shaped:
   `grep -rc '<LANE_HASH>' corpus/ SCORECARD.md | grep -v ':0$'` must equal exactly
   `corpus/lessons/round-33-verifier-spotcheck.md:1`. Red-before for that check: the base tree above
   (`round-33.md:2` plus the verifier quote).

## F2 — M34-2's `captured-by: none` is falsified as literally written

`claims.json` `non_claim_frontier_items.mistake`: "M34-2: `<LANE_HASH>` placeholders filed in
SCORECARD.md (R1) — class landing/reference-drift; **captured-by none**; fix = replacement + appended
correction + closure check."

But the markers were recorded, with their addresses, before the verifier routed them:

```
$ grep -n "L1's edit" corpus/lessons/round-33.md
7:…the two header placeholders are the L1's edit (open item 1).
126:…Its two `<LANE_HASH>` markers are the L1's edit…
$ sed -n '17p' corpus/lessons/round-33.md | grep -o '.\{90\}LANE_HASH.\{60\}'
…row under `## Round-33 capabilities` (`SCORECARD.md:1074`), appended with two `<LANE_HASH>` markers for the L1 to fill (`wave1/ScribeScorecard.md` §3
```

`round-33.md:17` names `wave1/ScribeScorecard.md` §3 as the source of the count. So the field is true only
under a narrower definition — *no seat filed it as a defect* — and false under the definition round-33
used ("**Captured by:** no seat in round 32 — i.e. captured by none", `round-33.md:91`), because three
round-33 artifacts name it.

**Smallest safe correction**: M34-2's row must read
"captured-by: `none` **as a defect** (the markers were recorded as an intended L1 handoff at
`corpus/lessons/round-33.md:7,17,126`, so no seat treated them as drift); first filed as a defect by the
round-33 verifier R1 (`round-33-verifier-spotcheck.md:165-166`)". That is a one-line append; it does not
disturb the frozen claim or its id.

## F3 — M34-1's `captured-by: R13` answers a different question than M34-2's `none`

`claims.json`: "captured-by **R13** existed but was not applied to the mutant-obligation sentence".
`corpus/QUALITY.md:77` is criterion **R13** ("A counter's before and after are produced by one frozen
instrument whose limbs are each shown load-bearing by an isolating fixture… *A discrimination figure (a
mutant's score) is a measurement, not a construction*"). R13 is exactly the right criterion and it does
cover the overstatement — but it is a criterion, not a capturing seat, and the sibling row uses the field
for seats (`none`). Under round-33's schema the criterion has its own field (`**Criterion:**`).

The seats that actually held the truth are named in committed receipts, and this seat checked them:

```
$ grep -n "cases=0 failures=0" .ufo/waves/round-33/wave1/MutCtrSelftestSkip.md
63:selftest cases=0 failures=0
68:selftest cases=0 failures=0
73:No fixture case ran (zero `selftest case=` verdict lines…) …exit 0.
$ grep -n "SURVIVOR" .ufo/waves/round-33/wave1/MutCtrUnbound.md
136:Mutant exits 0 with `unbound=0` while record S002 carries no `url` → **SURVIVOR** under the frozen kill rule.
212:**SURVIVOR** under the frozen C1 kill rule as tasked (plain run): …prints `records=2 bound=2 unbound=0` and exits 0
```

**Smallest safe correction**: `captured-by: MutCtrSelftestSkip` (`cases=0 failures=0` exit 0 at `:63,68`)
`and MutCtrUnbound` (`SURVIVOR` at `:136,212`) — the report then summarized past two committed receipts;
`criterion missed: R13`; `routed by: round-33 verifier R4`. Also worth one clause: M34-1 is a recurrence
of **M33-6** ("two survivor events, both closed by a clause outside the plain-run rule",
`corpus/lessons/round-33.md:96`) — the same limb-oracle class, one round apart, which is the strongest
argument for the row existing at all.

## F4 — M34-1's fix does pass the able-to-fail bar — measured here, not argued

I ran the landed counter (read-only against the tree; scratch under `/fast/scratch`):

```
$ PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/kill-rule-check.py --scratch /fast/scratch/…/kr
exit=0
mutant=skip-selftest-summary killed=1
mutant=accept-record-without-url killed=1
mutant=per-file-binding-removal killed=1
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 …real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
GATE ok name=pristine-selftest / pristine-fixtures / pristine-determinism / rows-valid / controls / survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=6 failed=0
survivors=0
```

This is a genuine "shown able to fail": the `CTL-equivalent` row is a comment-only patch that compiles and
cannot be seen by any probe, and the tool reports it as a survivor with `witness_exit=1`
(`kill-rule-check.py:41-43,66-67` state exactly that intent). The do-nothing fake prints `survivors=0`
and is rejected as `opaque` (`differs=1`). Red-before is real and already committed: the frozen round-33
rule admitted both mutants (`MutCtrSelftestSkip.md:63` prints `cases=0 failures=0` exit 0;
`MutCtrUnbound.md:212` prints `records=2 bound=2 unbound=0` exit 0), which is what R22/R24 record.

**Caveat the row must not lose.** The red-before is the *old* rule's receipts, not a re-run of the old
rule: the round-33 kill rule was frozen prose with no executable form, so "the fix can fail" and "the old
rule passed" rest on different artifacts. The row should say so in one clause (R13's own second sentence:
"if it was not run on the landed bytes, the receipt says so"). Otherwise the row repeats M34-1's mistake —
summarizing past what was measured.

## F5 — M34-3 (missing row): the round filed a post-freeze counting-literal erratum eight minutes after
freezing a criterion that forbids exactly that, and the criterion cannot see it

The two artifacts:

```
$ sed -n '226p' corpus/QUALITY.md
| R22 | …every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. … |
$ sed -n '1,5p' .ufo/waves/round-34/claims-erratum-1.md
# Round-34 cl erratum 1 — C1 counting-literal scope (filed by the L1, pre-integration)
Filed: 2026-10-26, before any scoring seat's verdict was finalized (wave still in flight; this is the L1's record, mirroring round-33's Rule-B erratum discipline).
$ git log --format='%h %ci' -1 29f606db… ; stat -c '%y' .ufo/waves/round-34/claims-erratum-1.md
29f606d 2026-10-26 02:28:39 -0300        # freeze commit
2026-10-26 02:36:22.079795631 -0300      # erratum file, +7m43s after the freeze commit
```

Erratum 1 rescopes the frozen counting literal `records=40 bound=40 unbound=0` to
`records=41 bound=41 unbound=0` (measured at tip: `python3 corpus/instruments/capture-binding-check.py` →
`AUDIT records=41 … orphans=1 orphan=S040-live.txt`, `records=41 bound=41 unbound=0`, exit 0).

This is **not** an R22 violation as R22 is written, and that is the defect: R22's test is base-only, and
the literal was *true* at base — `git diff --stat 7963976e 014ee2d -- corpus/source-snapshots
corpus/instruments corpus/SOURCES.md` prints nothing (`diff_exit=0`), so the freeze tree's audit surface
is the round-33 one the verifier re-measured at `records=40`. The reviewer says so itself:

`.ufo/waves/round-34/wave1/RevClaimsFreeze.md:163-169` — "D-1 (disclosed) — … the frozen literal was
true at the freeze tree (§3). No action needed beyond the erratum's own disclosure requirement".

So the class that actually recurred is **satisfiable at base, falsified by the round's own planned data**,
and a base-bytes satisfiability step (R22 as landed) passes it by construction. Two consequences the
lesson owes a row for:

1. **The criterion is under-specified by exactly one limb.** R22 must also evaluate each literal against
   base **+ the round's declared after-adds** (this round: `+ S051.txt/manifest record` ⇒ the audit prints
   41, so `records=40` is unsatisfiable-on-arrival and is fixed *before* the freeze, killing erratum 1).
   Red-before for that limb: the base-only test accepts `records=40` (`diff_exit=0` above) while the
   planned-state test rejects it (`records=41` at tip) — a difference the current criterion cannot produce.
2. **The second instance, unfiled and unrepaired.** The frozen C2 predicate carries a literal that greps
   0 on the landed tree:

   ```
   $ grep -n 'PASS F17 ids=S051' .ufo/waves/round-34/claims.json
   57: "predicate": "…harness prints entries=20 pass=20 exit=0 incl. `PASS F17 ids=S051`; …"
   $ python3 corpus/instruments/frontier-recheck-count.py   # exit=0, entries=20 pass=20 exit=0
   20:PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
   $ grep -c 'PASS F17 ids=S051' <harness output>
   0
   ```

   `ScoutDatawalk.md:54(a)` measured this; `RevClaimsFreeze.md:205-208` downgraded it by judgment —
   "accurate as a description; only a literal-grep reading fails" — with no command producing that
   verdict. It is the same class as erratum 1 (a frozen literal no evaluator can satisfy), it survived
   the round's freeze, and it has neither an erratum nor a row. The C2 kill rule does not enforce it
   (`harness entries/pass != 20/20` only), so C2 is unharmed; the *criterion* is what failed.

**Row to add** (M34-3, minted as a separate appended file — the frozen claims cannot be edited and the
numbering is theirs): class *freeze satisfiability*; evidence pointers `.ufo/waves/round-34/claims.json:1`
(`frozen_at_utc 05:00:00Z`) + `claims-erratum-1.md` (mtime `02:36:22`, sha256 `6a3cd99e…`) +
`corpus/QUALITY.md:226` + `frontier-recheck-count.py` output line 20 vs `claims.json:57`; captured-by
`CritMistakes` (this seat) for the R22-vs-erratum-1 pairing, `ScoutDatawalk` F-a for the harness literal;
fix = R22 planned-state limb + reword the C2 after-list to the column-truth
`PASS     F17  …ids=S051`; able-to-fail = the two commands above.

## F6 — M34-4: recommend routed-defect, not a mistake row

`selftest-baseline.txt` (1552 B, sha256 `ca3759d1…`, mtime 02:37) sits untracked at the **lane root**
(`git ls-files --error-unmatch selftest-baseline.txt` → "did not match any file(s) known to git";
`grep -rIl 'selftest-baseline' .` → 1 file, `RevC1BeforeAfter.md`). It is already captured with a check
(`RevC1BeforeAfter.md:238-243`, F5: "a seat's manual capture left in the lane root instead of
`/fast/scratch/…` or the wave dir. Not deleted by me (not my file); the L1 should drop it"), so the
"captured-by + reproducible check" bar is met and it needs no mistake row; it needs a disposition before
the integration commit or it lands in the corpus root. Note the trap: the same file is the evidence
`RevC1BeforeAfter.md:37` reads for the 23-case baseline, so deleting it must not orphan that line — the
receipt already quotes the count inline, so deletion is safe.

## F7 — the one landed *false provenance* in the id set (carried, not created, by this round)

`M34-2` is cited as R22's second grounding at three sites plus one reviewer mapping, while the frozen
claims define M34-2 as the marker defect:

```
$ grep -n 'M34-2' corpus/QUALITY.md SCORECARD.md .ufo/waves/round-34/wave1/ExecErratum2.md .ufo/waves/round-34/wave1/RevClaimsFreeze.md
corpus/QUALITY.md:226:… Grounded in: round-33 verifier R2; M34-2.   (R22 row)
SCORECARD.md:1035:(`corpus/lessons/round-33-verifier-spotcheck.md` §5 R2) and mistake M34-2.
ExecErratum2.md:124:…grounded in the routed R2 defect … and mistake M34-2.
RevClaimsFreeze.md:214:M34-1 → QUALITY R24 grounding; M34-2 → QUALITY R22 grounding; both rows present.
$ jq -r '.non_claim_frontier_items.mistake' .ufo/waves/round-34/claims.json
M34-1: … M34-2: <LANE_HASH> placeholders filed in SCORECARD.md (R1) — class landing/reference-drift; captured-by none; …
```

R22's subject is the unsatisfiable-literal defect (R2); M34-2's subject is the marker defect (R1). R24's
pairing with M34-1 is correct, so the table is internally inconsistent: one row cites the right mistake,
the other cites its neighbour. A freeze-verification seat then propagated the mapping
(`RevClaimsFreeze.md:214`), and `ExecQualityAppends.md:220-226` + `ScribeQualityDraft.md:151,217-241`
both flagged it and deliberately left the mandated text in place ("its substantive finding is passed to
the L1 rather than silently applied"), so this is disclosed, not concealed — but it is **still in the
landed bytes**.

**Smallest safe correction**: do not renumber. M34-3 above *is* the right grounding for R22; append a
one-line correction at `QUALITY.md:226`'s row (and the SCORECARD paragraph) reading "R22's second
grounding is M34-3 (post-freeze counting-literal erratum, appended `.ufo/waves/round-34/claims-erratum-2.md`);
M34-2 grounds R1's row." The check that this correction is real: for every `M34-<n>` citation in
`corpus/` and `SCORECARD.md`, the id's own row text must name the same surface — e.g.
`grep -n 'M34-2' corpus/QUALITY.md` must not sit on a criterion about literal satisfiability.

## What the lesson must not do

- Must not restate M34-1/M34-2 with `Verified:` lines that re-quote this seat's or a peer's numbers without
  the command (that is M34-1's own class). Every `Verified:` line needs `command → output → exit`.
- Must not mint M34-3 inside `corpus/lessons/round-34.md` alone. The frozen claims own the numbering;
  `claims-erratum-1.md` is the L1's own precedent for how a post-freeze correction lands (separate file,
  named id, disclosure on every surface that reads it). The lesson may then cite the appended file.
- Must not treat `selftest-baseline.txt` as evidence and as a defect at once: cite `RevC1BeforeAfter.md:37`
  for the baseline count, and record the file's disposition.

## Report

All commands run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` on the working tree
(`git rev-parse HEAD` → `206e5108f1190e61b3e2622d21cab8a5d921650c`; base commit `014ee2d7…`; 12 modified +
9 untracked paths, none written by this seat). Scratch `/fast/scratch/hyaku/kasegi-r34/CritMistakes/`
created with `mkdir -p` and removed before yield.

### R1 — base vs tip marker count (F1)

```
$ grep -c '<LANE_HASH>' SCORECARD.md
0                                                        # exit 1 (no match line)
$ git show 014ee2d:SCORECARD.md | grep -n '<LANE_HASH>'
988:`<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the
1087:**Round-33 final lane commit: `<LANE_HASH>`** — the L1 replaces this marker. Every value in
base_count=2                                             # exit 0
$ grep -rc '<LANE_HASH>' corpus/ | grep -v ':0$'
corpus/lessons/round-33.md:2
corpus/lessons/round-33-verifier-spotcheck.md:1
total_corpus=3                                           # exit 0
$ grep -n "L1's edit" corpus/lessons/round-33.md
7:…the two header placeholders are the L1's edit (open item 1).
126:…Its two `<LANE_HASH>` markers are the L1's edit; this lesson does not verify…
$ sed -n '17p' corpus/lessons/round-33.md | grep -o '.\{90\}LANE_HASH.\{60\}'
…appended with two `<LANE_HASH>` markers for the L1 to fill (`wave1/ScribeScorecard.md` §3
```

### R2 — M34-1 counter run (F4)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/kill-rule-check.py --scratch /fast/scratch/hyaku/kasegi-r34/CritMistakes/kr
exit=0
mutants=3 killed=3 survivors=0 invalid=0
controls=4 rejected=4
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 …differs=1 stable=1
gates=6 failed=0
survivors=0
```

### R3 — C1 audit at tip (F5, erratum-1 scope)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/capture-binding-check.py
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0                            # exit 0
$ git diff --stat 7963976e 014ee2d -- corpus/source-snapshots corpus/instruments corpus/SOURCES.md
(no output)  diff_exit=0        # freeze tree audit surface == the round-33 tree measured at records=40
```

### R4 — C2 harness literal (F5.2)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 corpus/instruments/frontier-recheck-count.py
20:PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
entries=20 pass=20 exit=0                                # exit 0
$ grep -c 'PASS F17 ids=S051' <harness stdout>
0                                                        # exit 1
$ grep -n 'PASS F17 ids=S051' .ufo/waves/round-34/claims.json
57:      "predicate": "…harness prints entries=20 pass=20 exit=0 incl. `PASS F17 ids=S051`; …"   # exit 0
```

### R5 — freeze/erratum ordering (F5)

```
$ git log --format='%h %ci %s' -1 29f606dbdd28aff6fd4573ab4b90788bbb90af13
29f606d 2026-10-26 02:28:39 -0300 round-34: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard prep
$ stat -c '%y %n' .ufo/waves/round-34/claims.json .ufo/waves/round-34/claims-erratum-1.md
2026-10-26 02:28:36.449012312 -0300 .ufo/waves/round-34/claims.json
2026-10-26 02:36:22.079795631 -0300 .ufo/waves/round-34/claims-erratum-1.md      # +7m43s
```

### R6 — red-before receipts for M34-1 (F3/F4)

```
$ grep -n "cases=0 failures=0" .ufo/waves/round-33/wave1/MutCtrSelftestSkip.md
63:selftest cases=0 failures=0
68:selftest cases=0 failures=0
73:No fixture case ran (zero `selftest case=` verdict lines…); …exit 0.
$ grep -n "SURVIVOR" .ufo/waves/round-33/wave1/MutCtrUnbound.md
136:Mutant exits 0 with `unbound=0` while record S002 carries no `url` → **SURVIVOR** under the frozen kill rule.
212:**SURVIVOR** under the frozen C1 kill rule as tasked (plain run): …`records=2 bound=2 unbound=0`…exit 0
```

### R7 — misc probes

```
$ ls corpus/lessons/round-34*                → No such file or directory, exit 2 (lesson not landed)
$ grep -n '^| R13' corpus/QUALITY.md         → 77:| R13 | A counter's before and after are produced by one frozen instrument…
$ grep -n '^| R22' corpus/QUALITY.md         → 226 (row quoted in F5)
$ grep -n 'M34' corpus/QUALITY.md SCORECARD.md
226:R22 …; M34-2.   228:R24 …; M34-1 …   1035:…and mistake M34-2.
$ git ls-files --error-unmatch selftest-baseline.txt
error: pathspec 'selftest-baseline.txt' did not match any file(s) known to git   # exit 1
$ grep -rIl 'selftest-baseline' .            → ./ufo/waves/round-34/wave1/RevC1BeforeAfter.md (1 file)
$ grep -n "erratum\|R22\|records=40" .ufo/waves/round-34/wave1/RevClaimsFreeze.md
78,96,102,108,116,143,163-169 (D-1),180,187,214,230,247,249
```

### File digests (sha256) at the reviewed bytes

```
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
435e97b5929beb75fe53b2fe849855fdb8bd851c2a1e621c5dc3d1e7c5063420  corpus/lessons/round-33-verifier-spotcheck.md
dedb9ea8063ac9e0420a2ea6123e34fa1dda1b8e20a09ae4c83d9c9d671c0850  .ufo/waves/round-34/claims.json
6a3cd99e4dc9411293d9fa7b9cb3bb00473598b63ba31359be8c66c88f6bd1bd  .ufo/waves/round-34/claims-erratum-1.md
096dfb9060829554305b1003494c1248d22e038234d791014a394ca45f602d61  corpus/instruments/kill-rule-check.py
8a79010d557dc9b24c6cd763bc6d2b5f8c3febe0fafde408a8c752107f57499c  corpus/instruments/frontier-recheck-count.py
ca3759d1c4a047ec1a27f4d6bc8b64df4d6e21a29b74ef9904ccbe91be3a3a51  selftest-baseline.txt
34c8ce3cc64a8a37a1789e4deb5573886dbcc4cea3403f891ce94d3f0feabf2d  .ufo/waves/round-34/wave1/RevErrata.md
cc1322ad7e61e145e836f8a1a27256fedf64162c0df915c13851266b65091e80  .ufo/waves/round-34/wave1/ExecScorecardMarkers.md
712bfad1b7ec883cf1d41e75ae16ff1427686a50f3ca0a521a69cb1ca60ea511  .ufo/waves/round-34/wave1/RevClaimsFreeze.md
9cdbb9e3a084eebfcd51e402020c3e43276757e93f4db5c16398e5f08be9204f  .ufo/waves/round-34/wave1/RevC1BeforeAfter.md
72f0ba421336b42aec03de90dbe1cf152c64214575a17cabc2555afe1ed6b5f8  .ufo/waves/round-34/wave1/ExecQualityAppends.md
59fa45ddab79d38e91cc5a3b82032e14792558a8c03ae327140ec9c6ced862ed  .ufo/waves/round-34/wave1/ScribeQualityDraft.md
```

### Tooling

None installed, none upgraded. `python3` (system, 3.x) and `git` (read-only: `show`, `diff`, `log`,
`ls-files`, `rev-parse`, `status`, `check-ignore`) only; no `pacman`, no network.

### Scratch

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/CritMistakes
$ ls -d /fast/scratch/hyaku/kasegi-r34/CritMistakes
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/CritMistakes': No such file or directory   # exit 2, as intended
```
