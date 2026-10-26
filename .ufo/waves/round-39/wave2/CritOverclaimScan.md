# CritOverclaimScan — round 39, wave 2 (falsify)

Seat: critic, leaf (no subagents). Axis under judgement: `depth:verifiability`. Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` read at HEAD `5006097a84305267c9a3e8c1e1d560e60fe41d37`
(Y); judged head J = `46c66c268502abd1b2c342fc71bf88ccf721845b` (from `.ufo/waves/round-39/final-gates/all-gates.txt`
`export-ref=`). Base `480b1a50`, claims freeze `dcd31701`.

**Authorship statement.** I wrote none of the bytes under review (wave 1 wrote them; this seat is wave 2).
Nothing below is a self-review.

## Scope and method

Files scanned at HEAD: `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/lessons/round-39.md`,
`corpus/README.md`, `corpus/SOURCES.md`. Round-39 bytes isolated with
`git diff -U0 480b1a5..HEAD -- <file>` → 201 added lines (49 SCORECARD, 15 SHONEN, 15 LOG, 84 lesson,
28 README, 10 SOURCES; deletions 0 in all six). Whole-file scans for the four requested classes:
numbers without commands, universal clauses, unreachable pointers, future-dated evidence. Every number was
re-derived by its own command where one exists; every path was resolved from the file that names it.

Classes: `BLOCKING` = landed text asserts evidence that does not exist; `DEFECT` = frozen/filed criterion
unmet or a re-runnable command contradicts its prose; `PROVENANCE` = true-ish claim attached to the wrong
source; `WORDING` = imprecise but not false; `ADJACENT` = the six files' evidence chain, verified outside them.

## Findings

### H1 — BLOCKING: the SKILL.md `r39-closure.sh` registry row never landed (two files claim it)

- `SHONEN.md:194` — "Gates & probes registry gains the `r39-closure.sh` row … appended at EOF; every base
  line byte-identical; `anchorcheck.py SKILL.md` exit 0".
- `SCORECARD.md:1569` — "Non-target guard only: SKILL.md append-only (one registry row r39-closure.sh)".

Evidence:

```
$ git diff --name-only 480b1a5..HEAD | grep -i skill ; echo rc=$?
rc=1                                  # SKILL.md is not touched anywhere in round 39
$ git log -1 --format='%h %cI %s' -- SKILL.md
66703ac 2026-10-26T16:09:33-03:00 round-38: integrate C1 r38-closure suite + … (judged head)
$ grep -c 'r39' SKILL.md
0
$ grep -c 'r39-closure' SKILL.md
0
$ grep -n 'r38-closure.sh\|r37-closure.sh' SKILL.md | tail -2
1112:| r37-closure.sh | gate | … (round 37) |
1114:| r38-closure.sh | gate | … (round 38) |
```

The last registry row is r38. Both sentences describe a byte change that does not exist in J or Y, so the
`depth:density` "non-target guard only" limb also rests on nothing. (G1 is unaffected: `declared-blocks.txt`
declares the two front doors only, and the suite's G1 payload `declared=2` is consistent with SKILL.md not
being an appended tail.)

Smallest safe correction: strike the clause with a `Correction (round 40)` line in SHONEN/SCORECARD and route
the SKILL.md registry row to round 40 (it is a non-target guard; no axis loses by correcting the record).
If the L1 prefers to honour it this round, landing the row is a new commit → J/Y move and the receipt must be
re-run (suite runs in ~3 s).

### H2 — DEFECT: the LOG.md correction does not satisfy its own frozen counting command (0 of 1)

`LOG.md:1704` carries `- **Correction (round 39):** …`, i.e. the marker is not at line start. E5.7 and
M39-2's "able to fail" command is line-anchored:

```
$ grep -c '^Correction (round 39)' corpus/lessons/round-38.md LOG.md SCORECARD.md SHONEN.md
corpus/lessons/round-38.md:1
LOG.md:0
SCORECARD.md:2
SHONEN.md:1
```

`.ufo/waves/round-39/c1-controls/before.txt` recorded the same four files at `0 0 0 0`; the after-state moved
three of them and left LOG at 0. `LOG.md:1711` ("`Correction (round 39)` blocks in round-38 lesson, LOG,
SCORECARD, SHONEN") and M39-2's per-file `>= 1` test are therefore unmet for LOG under the frozen predicate.
This is not a C1 kill (the suite's G5 counts only the SCORECARD section: `grep -c '^Correction (round 39)'`
at `r39-closure.sh:935`), but it is exactly the R2 defect class the round claims to have swept.

Smallest safe correction: reformat the LOG bullet so a line begins `Correction (round 39):` (content
unchanged), commit, refresh J/Y + receipt.

### H3 — DEFECT: printed `git grep` returns two lines, not "only `SCORECARD.md:332`" (self-reference, R1 class)

`SCORECARD.md:1551` states: "`git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/` returns
only `SCORECARD.md:332`". Reproduced at HEAD:

```
$ git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/
SCORECARD.md:332:| coverage (C2) | 7 | **7** | … 20 corpus-attested Core items + 5 Frontier topics → (20+0)/25 …
SCORECARD.md:1551:`(20 + F_admitted) / (20 + F_total) = 1.000`, with `F_total` = …
```

Line 1551 matches because it quotes the literal pattern — the same self-referential shape as R1/M39-1, one
round later. A non-author re-running the printed command gets 2, so the sentence is false as landed.

Smallest safe correction: narrow the pattern to `'20 corpus-attested Core items'` (then only :332 matches) and
state the measured result, or restate as "returns `:332` and this line, which quotes the pattern".

### H4 — DEFECT: "every figure below is the printed output of the command beside it" is false

`SCORECARD.md:1534` universal clause. Figures whose command is not printed beside them:

- `:1545` "23 of the 24 … 6 also test … 1 also test" — measured (true): 23 knowledge files carry
  `test -d ~/Projects` and all 23 name `~/Projects/bounties`, 6 also `the-bounty-hunter`, 1 `origin-work`;
  no command beside the figure, and `recheck-audit.py --root .` prints per-file gated/PASS, not this tally.
- `:1553` "queued registry rows 9 (S016 … S025)" — measured 9 at base; no command beside it.
- `:1555` "7 are unmined … 2 are superseded (S022 by S030, S024 by S029)" — measured true (`S029 | … |
  supersedes S024`, `S030 | … | supersedes S022`, both unflipped/queued); no command beside it.
- `:1557` "0/18 domain surfaces" — cited by pointer (`corpus/README.md:55-56`, `PROVINCE.md:121-122`), not
  by a command; both pointers do carry the sentence.

Smallest safe correction: replace the universal with "each figure names its measuring command in the
paragraph (guard tallies from the audit's gated set)" and add the two missing greps.

### H5 — PROVENANCE: the coverage criterion is called "the r22 measure" but is new this round

`SCORECARD.md:1549`: "**Criterion** (the r22 measure, `SCORECARD.md:332` …)" followed by
`(20 + F_admitted) / (20 + F_total)`. Line 332 actually proposes
"proposed denominator for adoption next round: 20 corpus-attested Core items + 5 Frontier topics →
(20+0)/25 before, (20+5)/25 after" — a fixed denominator of 25 and no queued-row term. The quoted formula
exists nowhere before this round:

```
$ git grep -n 'F_total' 480b1a5 -- . | wc -l
0
$ awk 'NR==332' SCORECARD.md | grep -o 'proposed denominator[^|]*'
proposed denominator for adoption next round: 20 corpus-attested Core items + 5 Frontier topics → (20+0)/25 before, (20+5)/25 after.
```

Smallest safe correction: label it "extends the r22 Core+Frontier proposal (`:332`) with a queued-row
denominator (new in r39)" and keep `:178` for the never-adopted plan pointer (that pointer is correct).

### H6 — DEFECT: census "tier A +1" is wrong; tier A moves +3

`corpus/lessons/round-39.md:69`: "Registry 55 → 59 rows; tier A +1 (S057), rejected +3."

```
$ git show 480b1a5:corpus/SOURCES.md | awk -F'|' '$2 ~ /^ *S[0-9]+ / && $5 ~ /^ *A *$/ {n++} END{print "base="n+0}'
base=52
$ awk -F'|' '$2 ~ /^ *S[0-9]+ / && $5 ~ /^ *A *$/ {n++} END{print "head="n+0}' corpus/SOURCES.md
head=55
# S056 tier A (rejected), S057 tier A (mined), S058 tier B (rejected), S059 tier A (rejected)
```

"rejected +3" (3→6) is correct. "tier A +1" is false as a registry-composition statement.

Correction: "tier A 52→55 (mined S057; rejected S056, S059), rejected 3→6".

### H7 — DEFECT: the lesson's Q1–Q4 list is not the pin set the recheck verifies

`corpus/lessons/round-39.md:24-27` lists Q2 at `S057.txt:79-81` (the "decisions and timing … not determined
by a strict protocol" sentence) and Q4 at `:183-186`; `:31` claims "recheck exit 0 (Q1-Q4 occurrences=1)".
The manifest pins are different objects:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
```

Manifest `quotes`: Q1 = issuance-is-discretion (L12-14); Q2 = `under_investigation` lifecycle (L132-134);
Q3 = timestamp reaffirmation (L136-138); Q4 = inheritance caution (L184-186). So the lesson's Q2 is
**not pinned**, and its Q4 start line is off by one (183 vs 184). Only Q1 and Q3 match the lesson's list.

Correction: relabel the lesson's list to the manifest pins (Q2 = L132-134 lifecycle), and cite L79-81 as an
unpinned registry-row anchor (the SOURCES row already states it correctly as "business-decision sentences
(L12-14, L79-81)").

### H8 — DEFECT (future-dated/premature): "Wave 2 attacked …" is asserted before wave 2 existed

`corpus/lessons/round-39.md:81-82`: "## Instrument attack findings (wave 2) — routed to round 40.
Wave 2 attacked the landed suite and the C2 artifacts after scoring; findings and verdicts land in `wave2/`
receipts …". At J:

```
$ git ls-tree -r --name-only 46c66c2 .ufo/waves/round-39/ | grep -c 'wave2/'
0
$ git ls-tree -r --name-only 46c66c2 .ufo/waves/round-39/ | grep wave2
.ufo/waves/round-39/build-wave2-final.py
.ufo/waves/round-39/wave2-plan.err
.ufo/waves/round-39/wave2-plan.out
.ufo/waves/round-39/wave2-spec.json
```

Only the plan existed; no receipt. The sentence records an event that had not occurred when committed
(the wave-2 dispatch file and run directory are still untracked at my read).

Correction: "Wave 2 is dispatched to attack …; findings land in `wave2/` receipts and are routed to round 40",
or move the sentence into the post-wave-2 receipt.

### H9 — DEFECT: unreachable pointers in the lesson (four)

Resolved from the lesson's own directory (`corpus/lessons/`) they miss; they exist only under
`.ufo/waves/round-39/`:

| line | pointer as written | resolves from `corpus/lessons/`? | actual |
|---|---|---|---|
| 15 | `c1-controls/before.txt` | MISS | `.ufo/waves/round-39/c1-controls/before.txt` |
| 23 | `wave1/ScribeRowS057.row.md` | MISS | `.ufo/waves/round-39/wave1/ScribeRowS057.row.md` |
| 63 | `wave1/ScribeSpotCheckList.checklist.md` | MISS | `.ufo/waves/round-39/wave1/ScribeSpotCheckList.checklist.md` |
| 68 | `census-before.txt` | MISS | `.ufo/waves/round-39/census-before.txt` |

(`considerthese/2026-10-26.md`, `.ufo/waves/round-23/build/CoverageDenom.md` and `PROVINCE.md:77` do resolve.)
Correction: prefix `.ufo/waves/round-39/`. Cheap, and it is what makes the readiness list re-runnable from the
lesson.

### H10 — WORDING/PROVENANCE: "mined into SCORECARD §Saturation" names the wrong section

`LOG.md:1716` and `corpus/lessons/round-39.md:57-58` say proposal 1 was mined "into SCORECARD §Saturation".
The criteria landed in a new section, `## Distance-to-next-score (round 39, …)` at `SCORECARD.md:1532`;
`## Saturation` (`SCORECARD.md:309`) is unchanged (still the round-22 declaration). A reader greps
§Saturation and finds no criteria.

Correction: "mined into SCORECARD `## Distance-to-next-score` (below §Saturation)".

### H11 — WORDING: "Attack share: wave 2 27/37 = 73%" is underivable as written

`corpus/lessons/round-39.md:9`. The wave-2 spec holds 37 seats:

```
$ python3 -c "import json,collections;d=json.load(open('.ufo/waves/round-39/wave2-spec.json'));print(collections.Counter(i['role'] for i in d['items']))"
Counter({'reviewer': 12, 'critic': 8, 'mutation-tester': 7, 'scout': 4, 'sentinel': 2, 'connector': 2, 'simplifier': 1, 'scribe': 1})
```

27 = reviewer+critic+mutation-tester (12+8+7); the 2 sentinels (do-nothing controls, an attack role) and 4
scouts are excluded without saying so. 27/37 = 72.97 → 73 ✓. Correction: name the role set
("27/37 = 73% counting reviewers, critics and mutation-testers; sentinels excluded").

### H12 — WORDING: "count-line (22/22 admitted)" sits next to "PROVINCE amendment", but PROVINCE has no such line

`corpus/lessons/round-39.md:32`: "**Frontier row** F22 + PROVINCE amendment + count-line (22/22 admitted)."

```
$ grep -n '22/22' PROVINCE.md ; echo rc=$?
rc=1
$ grep -n '22/22' corpus/README.md
510:rewritten (R9): at round 39 the frontier stands at **22/22 admitted** — …
```

Correction: "(count line in `corpus/README.md:510`; PROVINCE carries the F22 amendment only)".

### H13 — ADJACENT: the receipt the six files cite is future-dated

`all-gates.txt` (the C1 evidence for `SCORECARD.md:1567`, `LOG.md:1709`, `SHONEN.md:202`,
`round-39.md:4-6`) records `run-utc=2026-10-26T21:35:00Z`, while the commit that contains it is stamped
earlier:

```
$ git log -1 --format='%h author=%aI committer=%cI' 5006097
5006097 author=2026-10-26T17:12:12-03:00 committer=2026-10-26T17:12:12-03:00   # 20:12:12Z
$ date -u
Mon 26 Oct 2026 08:15:00 PM UTC                                                # 20:15Z at first read
```

The recorded run time is ~83 minutes after the file was committed and after the wall clock. (`claims.json`
`frozen_at_utc: 2026-10-26T20:30:00Z` vs freeze commit `19:26:41Z` shows the same pattern; that file is
outside my six.) This is the only finding that reads as fabricated provenance rather than a wording defect.
Correction: write the observed UTC of the run; if the final receipt is re-run at filing, the timestamp will be
real. No other future-dated calendar date exists in the six files (`grep -nE '2026-1[12]-|2027-|2026-10-(2[7-9]|3[01])'`
→ no output) and `grep -c '⟨pending' corpus/lessons/round-39.md` → 0.

### H14 — ADJACENT: the cited reds are not in `final-gates/`; an untracked `reds.txt` dirties the tree

`SCORECARD.md:1567` and `LOG.md:1709` claim "base/r38-head reds" with no path. `final-gates/` holds one
tracked file plus one untracked:

```
$ git ls-files .ufo/waves/round-39/final-gates/
.ufo/waves/round-39/final-gates/all-gates.txt
$ git status --porcelain .ufo/waves/round-39/final-gates/
?? .ufo/waves/round-39/final-gates/reds.txt        # 601 B, head: closed=1/8 exit=1 (base and r38)
```

The committed reds are at `.ufo/waves/round-39/wave1/ExecSuiteBuild.overlay/run-at-base.txt` and
`run-at-r38head.txt` (both `closed=2/8 exit=1`), which none of the six names. The untracked `reds.txt`
also keeps the working tree non-clean — the frozen C1 kill-rule class "lane working tree not clean at
filing". Correction: point the reds at the committed overlay transcripts and commit or remove `reds.txt`
before the L1 files. (Note the two red transcripts disagree on the count: `2/8` overlay vs `1/8` reds.txt —
different runs; if `reds.txt` is kept, label which run it is.)

### H15 — ADJACENT (reproducibility caveat, not a falsification): 8/8 is a quiescent-instant property

Running the committed suite myself at HEAD, from a live wave-2 scratch:

```
$ bash corpus/instruments/r39-closure.sh --export-ref 46c66c2… --work $S/workJ
closed=5/8 exit=1     # G2=0 (receipt=0, as E4 documents), G6=0, G8=0
$ bash corpus/instruments/r39-closure.sh --export-ref 5006097… --work <isolated work> --scratch-root <isolated>
closed=6/8 exit=1     # G6=0, G8=0; G1,G2,G3,G4,G5,G7 green
```

Diagnosis:
- G6 red: `/fast/scratch/hyaku/kasegi-r39/` held 13 sibling seat dirs at my read — G6 tolerates only this
  run's work chain. Live wave-2 seats red it by construction.
- G8 red: the pinned r37 suite's E9 reads the lane dirty. Manual probe of the pin
  (`git show 2387dcf6…:corpus/instruments/r37-closure.sh`, sha `0da98e37…`):
  `E9 payload=status-read=ok,status-dirty=6,scratch-seat-dirs=0,head-match=1,lane-root=1,scratch-root=absent closed=0`
  — the 6 dirty entries are the untracked wave-2 files (`wave2/`, `wave2-dispatch.json`, …).

So the receipt's 8/8 is reproducible only with a clean lane and no sibling scratch; the six files state the
number without that precondition. It is **not** evidence the recorded run was wrong (G1–G5, G7 and G2-at-Y
are green in my runs; base/r38 controls still red, see below). Correction: state the precondition
("clean tree, scratch quiescent") in SCORECARD/SHONEN/all-gates, and re-run at final filing after cleanup so
the filed number is the last observed one.

## Do-nothing controls — verified

| control | command | observed |
|---|---|---|
| plain run refused | `bash corpus/instruments/r39-closure.sh` | `refusing to run against the live worktree` / `plain_exit=2` ✓ |
| base export red | `--export-ref 480b1a50…` (isolated scratch) | `closed=2/8 exit=1` ✓ |
| r38 judged head red | `--export-ref 66703acaaff50529a35be49aa8759d04140720ad` | `closed=2/8 exit=1` ✓ |
| junk F22 rejected | `grep -c MISMATCH .ufo/waves/round-39/{c2-controls,wave1}/…junk*` | `4` and `4`, exit=1 ✓ |
| C2 before-control | `.ufo/waves/round-39/c2-controls/before.txt` | frontier 21 / registry 55 / S057 0 / knowledge 50 / harness 24-24 / binding 45-45 / audit 50 ✓ |
| suite digest | `sha256sum corpus/instruments/r39-closure.sh` | `2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b` ✓ |

## Verified true (no overclaim found)

- Capture identity: `corpus/source-snapshots/round-39/S057.txt` = 275 lines, 17,971 B,
  sha256 `11c8d6d6…64f2f`; the wave-1 deliverable hashes identically (so the re-open's "byte-identical" holds
  transitively, though `ScoutReopenS057.reopen.txt` compared the stand-in — the committed path was absent at
  that moment; it says so itself).
- S057 row: NF=13, exactly one `https://` token equal to the manifest `url`, kind `docs`, tier `A`, status
  `mined`, opened `2026-10-26`, `recheck 180d`, used-by entry ✓; deliverable byte-identical to the registry row.
- Registry 59 rows; rejected 3→6; knowledge 51; frontier rows 22 / admitted 22; F22 NF=8; F22 sources `S057` ✓.
- `frontier-recheck-count.py` → `entries=25 pass=25 exit=0` incl. `PASS F22 … ids=S057` ✓ (live).
- `capture-binding-check.py` → `records=46 bound=46 unbound=0` ✓; `recheck-audit.py --quiet` →
  `expected=51 missing=0 unexpected=0 exit=0` ✓; census after → `W04 S028`, `W04 S029`, `ok`, exit 0 ✓.
- Assimilation: reg-ids 55, staged-ids 94, collisions 25 (r38's 24 + S055) ✓; quarantine 7 rows split exactly
  2 quote-defective (S037, S054) / 4 unreachable (S048, S068, S069, S070) / 1 unverifiable (S065) ✓; 7
  staged refusals carried ✓.
- r38 receipt line pointers all correct: `:2` export-ref J, `:4` run-ref, `:8` G2 `closed=0`, `:15`
  `export-ref-run: closed=7/8 exit=1`, `:26` `closed=8/8 exit=0`, `:73` `selftest cases=8 failures=0` ✓.
- Corrections present and counted in round-38.md (1), SCORECARD (2), SHONEN (1) ✓ (LOG 0 — H2).
- QUALITY R34/R35/R36 landed and cite M39-1/M39-3/M39-4 ✓; `grep -cE 'M38-5|M38-7' corpus/QUALITY.md` = 1
  (base = 0) ✓; `PROVINCE.md:77` is the F18 amendment ✓; `SCORECARD.md:331` genuinely contains the
  "Threshold for 5 …" quote ✓; `SCORECARD.md:178` is the coverage-plan line with the r22 denominator ✓;
  `round-23.md:173-177` supports "round 23 kept the r15 denominator" ✓.
- README: "every existing line keeps its number" is structurally true (28 additions, 0 deletions); `22/22
  admitted` at `:510`; `0/18` untouched at `:513` ✓.
- SOURCES: "S001–S055 untouched", "55 → 59", "the three rejected rows take 55 to 58" all ✓; the five-term
  base sweep reproduces: `reaffirm` 0, `when to issue` 0 hits; `under_investigation` 7 matching lines (5 in
  the S055 entry + 1 README + 1 SOURCES), all in S055 vocabulary ✓; `issuance`/`inherit` hits unrelated ✓.
- Sibling ruling: 20 sibling lanes enumerated by `ls -d *-shokunin` minus kasegi, all with `.git`; "first
  write, no sibling/shokuknow ground" supported by `ScoutSiblingF22` ✓.
- Wave shape: w1 49 (executor 27, scribe 11, reviewer 6, scout 2, critic 2, connector 1) + w2 37
  (12/8/7/4/2/2/1/1) = 86 ✓.

## Axis impact

- `depth:verifiability` (judged): H1–H3 are the ones that move the axis — a landed evidence claim that is
  false (H1), a frozen counter unmet in the file that claims it (H2), and a printed command that refutes its
  own sentence (H3). The fixes are small and do not weaken any criterion. H4–H12 are precision defects: they
  cost re-derivation but do not change a score by themselves. H13–H15 are the evidence chain: the run
  timestamp is ahead of the clock, the reds are untracked, and 8/8 is only reproducible in a quiescent state.
- `coverage`: C2's counters all reproduce at HEAD; the only coverage-side miss is the census composition
  number (H6), which is a record-accuracy defect, not a coverage loss.
- `depth:density`: H1 removes the only claimed round-39 density artifact; the guard is honestly
  "no change" once the false clause is struck, so no density move is lost.

## Verdict summary

C2 stands on re-measurement (frontier 22, registry 59, knowledge 51, harness 25/25, binding 46/46, audit 51,
junk rejected, census clean). C1's suite is sound where I could run it (G1–G5, G7; controls red as claimed),
but its evidence record carries three fixable defects (H1–H3), one future-dated receipt timestamp (H13), an
untracked reds file (H14), and an unstated quiescence precondition (H15). None of these is a
tradeoff-private choice; all are correctable without touching the frozen predicates — except H2, which needs
one line moved in LOG.md (or an erratum that says the LOG block is bullet-wrapped), and H1, which needs
either a correction line or a new commit that re-runs the receipt.

## Scratch / tooling

Scratch `S=/fast/scratch/hyaku/kasegi-r39/CritOverclaimScan` (plus probe roots
`/fast/scratch/hyaku/overclaim-{scan,base,r38}`), all under `/fast` (23 % used at start); removed after
copying this receipt. No tools installed, no pacman, no network fetch, no git/jj mutation; only read-only
`git` and lane instruments were run. No deliverable file besides this receipt.
