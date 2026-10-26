# ScribeQualityDraft — round 34, wave 1 (QUALITY.md R3 note / R22 / R23 wording, R24 row)

Seat: `ScribeQualityDraft` (scribe, leaf — no subagent dispatch). Milestone round-34, axes owned
`depth:verifiability` + `coverage`. **This seat writes no product file.** The deliverable is the exact
amendment text, its grounding, and the machine-checkable consequence; `ExecQualityAppends` owns
`corpus/QUALITY.md` this round and applies it, the L1 commits.

No git/jj mutation (`git status/show/diff/rev-parse/cat-file/ls-tree` only, all read-only), no
`agent://all`, no tool installed or upgraded. Scratch: `/fast/scratch/hyaku/kasegi-r34/ScribeQualityDraft/`
(removed before yield — §7).

Two artifacts:

- this receipt;
- `.ufo/waves/round-34/wave1/ScribeQualityDraft-block.txt` — the 18-line / 3971-byte block to write at
  `corpus/QUALITY.md:215-227`, `sha256 41c51a867545eea3b353d7f69c962606860c5744cb9be8ab3c9b11d754afe2bb`
  (`sha256sum` below), so the owner can `cat` it instead of retyping from this file.

## Report

### 1. What was on disk when the seat started, and what it must be measured against

At seat start `ExecQualityAppends` had already appended its assigned draft to the end of
`corpus/QUALITY.md` (its receipt `.ufo/waves/round-34/wave1/ExecQualityAppends.md:27-58`), so the draft
rows exist but are **uncommitted worktree bytes**. That is the state the wording below corrects.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ sha256sum corpus/QUALITY.md ; wc -l corpus/QUALITY.md
eb20eafc6aabc312ba46fe7214860590098aef4f7664064de4a7c888653dc8cb  corpus/QUALITY.md
227 corpus/QUALITY.md
exit=0
$ git show HEAD:corpus/QUALITY.md | wc -l
213
exit=0
$ git status --porcelain corpus/QUALITY.md
 M corpus/QUALITY.md
exit=0
$ grep -n '^| R20 \|^Note (round 34)\|^| R22 \|^| R23 ' corpus/QUALITY.md
169:| R20 | A capture snapshot directory ships its `manifest
220:Note (round 34): R20's 'exactly one registry-row URL' re
226:| R22 | A frozen claim predicate is checked for satisfia
227:| R23 | A lane records an event-driven reflection cadenc
exit=0
$ grep -c '^| R[0-9]\+ |' corpus/QUALITY.md
23
exit=0
```

Consequence for R6 (`corpus/QUALITY.md:75-76`): lines 214-227 are cited by exactly two files, both
round-34 receipts being written now, and by nothing committed —

```
$ grep -rn 'QUALITY\.md:2[0-9][0-9]' --include='*.md' .
./.ufo/waves/round-34/wave1/ExecErratum2.md:94:`ExecQualityAppends` landed R22 (`corpus/QUALITY.md:222`) during my window; its text ("every literal
./.ufo/waves/round-34/wave1/ExecErratum2.md:158:   `corpus/QUALITY.md:222` (digest `eb20eafc…`), landed by another seat during this wave.
./.ufo/waves/round-34/wave1/ExecQualityAppends.md:203:  "exactly one"; the note is at `corpus/QUALITY.md:220-222` and names R20 by number. If the L1 prefers
exit=0
```

So replacing 215-227 **before** the L1's commit is not a rewrite of a filed assertion (R9) and moves no
cited line (R6). After commit the same change would have to take Deliverable B's append-only form.

### 2. Every anchor the drafted text cites, opened and checked

One line per citation, each `path:line` read at its own line (`token` must appear on that line). Command:
`python3 -` over a `(path, line, token)` table, printing `OK`/`FAIL` per row; the full output is quoted.

```
OK   corpus/QUALITY.md:169 token='| R20 |'
OK   corpus/QUALITY.md:220 token='Note (round 34)'
OK   corpus/QUALITY.md:226 token='| R22 |'
OK   corpus/QUALITY.md:227 token='| R23 |'
OK   corpus/lessons/round-33-verifier-spotcheck.md:167 token='**R2**'
OK   corpus/lessons/round-33-verifier-spotcheck.md:174 token='**R4**'
OK   corpus/lessons/round-33.md:132 token='multi_row_url'
OK   .ufo/waves/round-33/claims-erratum-1.md:9 token='eur-lex.europa.eu'
OK   .ufo/waves/round-33/claims-erratum-1.md:11 token='docs.hackerone.com'
OK   .ufo/waves/round-33/claims-erratum-1.md:17 token='global "URL appears in exactly one registry row"'
OK   .ufo/waves/round-33/claims-erratum-1.md:23 token='Rule B binds each record to its OWN registry row'
OK   .ufo/waves/round-33/claims-erratum-1.md:29 token='dup-id'
OK   .ufo/waves/round-33/claims-erratum-1.md:30 token='S024/S029, S006/S028'
OK   .ufo/waves/round-33/wave1/RevClaimsFreeze.md:75 token='selftest cases=9 failures=0'
OK   .ufo/waves/round-33/wave1/RevClaimsFreeze.md:172 token='F-5'
OK   considerthese/2026-10-25.md:76 token='6. **Event-driven reflections.**'
FAIL considerthese/2026-10-25.md:77 token='push'
     got:    listener on `master` would catch bursts the same morning, and a weekly note would cover idle stretches.
OK   corpus/knowledge/considerthese-proposals-ledger.md:33 token='| 6. Event-driven reflections | `open` |'
OK   SCORECARD.md:1014 token='**Erratum 2, disclosed'
OK   SCORECARD.md:1028 token='Pre-freeze satisfiability step, recorded (QUALITY R22)'
failures 1
exit=0
```

The single `FAIL` is the probe, not the file: proposal 6 wraps, so `push` sits at the end of line 76 and
`listener …` begins line 77. The drafted R23 cell therefore cites `considerthese/2026-10-25.md:76-77` and
quotes the full sentence across the wrap:

```
considerthese/2026-10-25.md:76-77
6. **Event-driven reflections.** The lane did three rounds in under three hours after 4.5 idle days; a push
   listener on `master` would catch bursts the same morning, and a weekly note would cover idle stretches.
```

Read digests of the sources cited (so a later reader can tell whether the anchors moved):

```
$ sha256sum corpus/lessons/round-33-verifier-spotcheck.md corpus/lessons/round-33.md \
    .ufo/waves/round-33/claims-erratum-1.md .ufo/waves/round-33/wave1/RevClaimsFreeze.md \
    considerthese/2026-10-25.md corpus/knowledge/considerthese-proposals-ledger.md SCORECARD.md
435e97b5929beb75fe53b2fe849855fdb8bd851c2a1e621c5dc3d1e7c5063420  corpus/lessons/round-33-verifier-spotcheck.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
dd59d201b692276b1e66cd4554c76ae484be400a985d2b20e5b5fc7bd9615eb9  .ufo/waves/round-33/claims-erratum-1.md
d60fe749a147074417a8935bdf4a0d290601ec61e8d45c4408d7f1d72462f1aa  .ufo/waves/round-33/wave1/RevClaimsFreeze.md
6adc24d64e3c04884d029d380278bb49b50f8e6e9c7bdc1951f56a38c027052e  considerthese/2026-10-25.md
c354ca0242bf7da44589e45c464deba0714dc083e2bf480a6c855ec30a1629c2  corpus/knowledge/considerthese-proposals-ledger.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
exit=0
```

### 3. Deliverable A — exact replacement block for `corpus/QUALITY.md:215-227` (preferred)

Write the 18 lines of `.ufo/waves/round-34/wave1/ScribeQualityDraft-block.txt` over current lines
**215-227**, leaving line 214 (blank) in place. Verbatim:

```
## Round-34 additions — pre-freeze satisfiability, reflection cadence and per-case evidence (append-only)

R6 form: R20's row (line 169) and every earlier line stay byte-identical; the note and the three rows
below are appended at the end of the file.

Note (round 34): the C1 erratum-2 per id reading supersedes R20's "exactly one `corpus/SOURCES.md`
registry-row URL" clause: a record binds to its OWN row, so a URL that also appears in a different
registry row is informational `multi_row_url=N` and is not a failure, while two rows carrying the same id
are `dup-id`. The two instances are S029 (its URL is also the S024 row's) and S006 (also the S028 row's)
(`.ufo/waves/round-33/claims-erratum-1.md:9-13` § Finding; ruling at `:23-32`; `SCORECARD.md:1014`
erratum 2). R20's provenance clause — one `url` plus one fetch-provenance field per record — is
unchanged by this note.

| id | criterion | grounded in |
|---|---|---|
| R22 | A frozen claim's predicate and kill rule are checked for satisfiability against base bytes before the freeze, and that pre-freeze check is recorded with the freeze: every literal constant, count and regex the predicate names is run on the base tree and its observed value printed. An unsatisfiable, self-contradictory or already-superseded literal is corrected before the freeze, never waived after it by an erratum; a predicate that reaches its target only through an after-freeze clarification is a freeze defect of that round, not a measurement. | round-33 verifier spotcheck §5 R2 (`corpus/lessons/round-33-verifier-spotcheck.md:167-169`): C1 froze with "exactly one registry-row URL" and "zero or two+" while two record URLs each sit in two immutable rows, so the frozen kill rule reads the correct instrument as failing and only the after-freeze erratum 1 makes the frozen text and the measured reading agree (`.ufo/waves/round-33/claims-erratum-1.md:17-19`; disclosed at `corpus/lessons/round-33.md:132` open item 8) |
| R23 | A lane records an event-driven reflection cadence: burst activity (several rounds inside one working window) and idle stretches are each reviewed, and the review lands in the next round's lesson, which cites the considerthese file and its date and states that proposal's disposition (mined into a named path, declined, or unchanged with the reason). A proposal left `open` through consecutive lessons with no disposition line is a cadence failure, not neutrality. | `considerthese/2026-10-25.md:76-77` proposal 6 (2026-10-25) — "the lane did three rounds in under three hours after 4.5 idle days; a push listener on `master` would catch bursts the same morning, and a weekly note would cover idle stretches"; `corpus/knowledge/considerthese-proposals-ledger.md:33` records it `open` / `unchanged` with the grep evidence that no landing existed; round 34 mines it into this row (`.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.considerthese`) |
| R24 | A counter's pass is its per-case evidence, not its summary line: a selftest runner prints one `selftest case=<name> exit=<n> want=<n> verdict=pass\|fail` line per case and then `selftest cases=N failures=F`, and fails when the summary is not backed by N verdict lines and by a case count at or above the frozen floor (C1 round 34: N>=19) — a forged or summary-only `cases=N failures=0`, `cases=0` included, is a failure, not a pass. A do-nothing control that prints the counter's target count while running nothing is rejected by this rule, so a kill rule that reads only the summary line is not a kill rule. | round-33 measured: the skip-selftest mutant passed the frozen kill-rule letter by printing `selftest cases=9 failures=0` exit 0 with no fixture executed (`.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75`, finding F-5 at `:172`), and the same receipt records the fake checker's `selftest cases=0 failures=0` exit 0; routed as `corpus/lessons/round-33-verifier-spotcheck.md:174-176` R4, whose fix is this row |
```

What changed against the in-flight draft, and why each change is required:

| in-flight draft | replacement | reason |
|---|---|---|
| R22 criterion cell ends "…never waived by a post-freeze erratum. **Grounded in: round-33 verifier R2; M34-2.**" and its grounding cell cites "M34-2 at …`non_claim_frontier_items.mistake`" | no mistake id; grounding is the R2 defect, erratum 1 and the lesson's open item 8 | the frozen mistake list numbers **M34-2 as the `<LANE_HASH>` placeholders (defect R1)**, not the unsatisfiable freeze — see F1 |
| R22 criterion said "checked for satisfiability …, every literal constant and regex … is run against the base tree" | adds counts, adds *recorded with the freeze*, adds the superseded-literal and after-freeze-clarification limbs | the frozen `after` line asks for "a pre-freeze satisfiability step **recorded**"; a criterion that only forbids waiving states no obligation to record the run |
| R23 criterion embedded "Grounded in: considerthese/2026-10-25.md proposal 6." inside the criterion | grounding moved wholly into the grounding cell, plus the quote, the date, the ledger row and the claims-file mining record | one grounding surface per row, as every other row in the bar does; the empty `open` history is the evidence that the criterion is needed |
| the section has two rows | three rows; heading names per-case evidence | R24 (§ below) and F4 |
| note: "'exactly one registry-row URL' reading **is superseded by** the C1 erratum-2 per-id reading" | "the C1 erratum-2 per id reading **supersedes** R20's 'exactly one …' clause", plus the per-id mechanics, the two instances and the R20 clause that is *not* superseded | the R3 defect is a mis-statement of R20's own rule; the note must say which clause falls (url↔row) and which stands (provenance), and it must carry both spellings a checker may key on (`per id`, `superseded/supersedes`) |

Mechanical consequence on the live bytes (before → after), computed on a copy of the current worktree
file with the block substituted:

```
before_sha256 eb20eafc6aabc312ba46fe7214860590098aef4f7664064de4a7c888653dc8cb
after_sha256  63bdf7db82079ba674e998e32a215564ed630982af2b4a190d249dad1f52a4ba
before_lines 227 after_lines 232 bytes 32342
numstat_vs_worktree 13 added / 8 removed        # the 13 in-flight lines replaced by 18
numstat_vs_HEAD     19 added / 0 removed        # append-only w.r.t. the committed file (R6)
prefix_1_214_identical True
R_rows 24                                       # R1…R24
M34-2_occurrences 0
r24_pipes 5   r18_pipes 6                       # escaped `\|` precedes; see F6
exit=0
```

`git show HEAD:corpus/QUALITY.md` → 213 lines; `diff -u` HEAD→after is `+19 / -0`, i.e. the replacement
is indistinguishable from an append at the committed level.

### 4. Machine check against the landed closure counter (this is the evidence that the text is load-bearing)

`corpus/instruments/r-defect-closure.sh` landed during this seat's window
(`sha256 e1cfd6e82fa1d3d4813214e8ad3f2ab798a182ec3301f4fee82032204c20bea9`, 632 lines). Its `check_r2`
(`:144-165`), `check_r3` (`:169-184`) and `check_r4` (`:188-215`) read exactly the text this seat drafts.
Run against a reduced root (`--root` on a scratch tree holding `SCORECARD.md`,
`corpus/QUALITY.md`, `corpus/lessons/round-33.md` only), twice:

```
# before-bytes = the live worktree file (ExecQualityAppends' in-flight draft)
$ bash corpus/instruments/r-defect-closure.sh --root "$S/rdroot"
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule (cases>=11, one 'selftest case=' line per case) not recorded open=1
closed=4/9 exit=1

# after-bytes = the same root with Deliverable A's block substituted
$ bash corpus/instruments/r-defect-closure.sh --root "$S/rdroot"
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (selftest case= per case, cases>=11) + round-33 lesson R4 3-of-4 erratum open=0
closed=5/9 exit=1
```

Read this narrowly, because the root is reduced: `closed=4/9` / `5/9` are **not** the lane's closure
state — R1/R5/R6/R8/R9 in that root read `absent` (the fixture tree carries three files, and R5/R9's
`capture-binding-check.py` and R6/R8's manifests were not copied). What the pair measures is the only
thing this seat claims: with the in-flight text, **R4's prose limb is open**; with Deliverable A's block it
is closed, and R2/R3 stay closed across the rewording (their token sets are preserved: `Note (round 34)`,
`R20`, `exactly one`, `supersed`, `per id`; `satisfiab`, `pre-freeze`). So the R24 row is not decoration —
without it, or without equivalent prose in `SCORECARD.md` (`check_r4` accepts either file), R4 cannot
close.

### 5. Deliverable B — append-only fallback (if 215-227 are committed as they stand)

Append at EOF; it corrects the R22 grounding without rewriting a filed row and adds R24 under its own
heading:

```
## Round-34 corrections and addition 2 — R22 grounding fix and per-case evidence (append-only)

Note (round 34, grounding correction): the R22 row above cites "mistake M34-2" as its second grounding.
The frozen mistake list numbers M34-2 as the `<LANE_HASH>` placeholders filed in SCORECARD.md (defect R1),
not the unsatisfiable freeze (`.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.mistake`), so
R22's satisfiability grounding is the routed R2 defect alone
(`corpus/lessons/round-33-verifier-spotcheck.md:167-169`), with erratum 1 as the record of the unreachable
literal (`.ufo/waves/round-33/claims-erratum-1.md:17-19`). The R22 criterion text stands as filed; the same
correction applies to `SCORECARD.md:1034-1035` and `.ufo/waves/round-34/wave1/ExecErratum2.md:124`.

## Round-34 addition 2 — a counter's pass is its per-case evidence (append-only)

| id | criterion | grounded in |
|---|---|---|
| R24 | <the R24 row from Deliverable A, verbatim> |
```

### 6. Findings (reported, not fixed — the L1 decides)

- **F1 — the R22 grounding cites a mistake id that names a different defect, on three surfaces.** The
  frozen list reads, verbatim (`.ufo/waves/round-34/claims.json`, `non_claim_frontier_items.mistake`):
  "M34-1: round-33 report claimed 'all mutants killed' … (R4). **M34-2: `<LANE_HASH>` placeholders filed in
  SCORECARD.md (R1)** — class landing/reference-drift; captured-by none". The three surfaces attributing
  satisfiability to M34-2: `corpus/QUALITY.md:226` (in-flight R22, criterion *and* grounding cell),
  `SCORECARD.md:1034-1035` ("grounded in the routed R2 defect … and mistake M34-2"), and
  `.ufo/waves/round-34/wave1/ExecErratum2.md:124`. `ExecQualityAppends` already discloses the weaker form
  of this in its own receipt ("M34-2 is cited from the frozen claims file only",
  `ExecQualityAppends.md:206-208`) — but the citation is not thin, it is wrong. Two defensible fixes:
  (a) drop the mistake id and ground R22 in R2 alone (Deliverable A/B take this route — R2 *is* the frozen
  record of the defect); (b) mint **M34-3** in `corpus/lessons/round-34.md` § Mistakes for "froze a claim
  on an unsatisfiable literal" and repoint all three surfaces, which requires the lesson seat to define it
  and the two other files to be corrected in the same landing. Pick one; do not leave the three surfaces
  disagreeing with the frozen list.
- **F2 — `ExecErratum2.md` cites the R22 row four lines short.** `:94` and `:158` say
  `corpus/QUALITY.md:222`; measured `grep -n '^| R22 '` → `226`, and `:222` is the last line of the note
  ("failure (SCORECARD round-33 section, erratum 2)."). The digest it pairs with (`eb20eafc…`) is the
  file's own, so the receipt is checkable; the line is not. Under Deliverable A's block the row stays at
  226.
- **F3 — R24 sits outside the frozen non-claim list.** `claims.json` names R23 as the only new criterion
  ("considerthese proposal 6 … it becomes a QUALITY.md criterion (R23)"), and the wave's own frozen prompt
  text advertises "record R1–R23" (`.ufo/waves/round-34/build-spec.py:45`; 66 occurrences in
  `wave1-spec.json`). Minting R24 is a criterion-level addition the claim freeze did not enumerate. My
  read of the dispatcher's "draft the R24 row **if** the wave's mutations surface a new criterion" is that
  the condition is met by measurement, not by preference: `check_r4`'s prose limb is unsatisfied on the
  in-flight bar (§4) and the class has a round-33 measured specimen (F7). But the L1 must decide whether
  R24 lands this round or waits for round 35 with a claims line of its own; the Deliverable B split exists
  so R24 can be applied or withheld independently of the R3/R22/R23 corrections.
- **F4 — R23's own obligation lands in a file that does not exist yet.** `test -e corpus/lessons/round-34.md`
  → `exit=1`. The criterion requires the mining to be recorded in "the next round's lesson"; the drafted
  grounded-in cell therefore **does not cite** `corpus/lessons/round-34.md` (round-31's M31-4 precedent:
  rows citing a lesson that did not exist when written were flagged at `corpus/lessons/round-31.md:147`).
  The lesson seat must record `considerthese/2026-10-25.md:76-77` (with the date and "mined → QUALITY R23")
  or R23's first instance is a criterion with no witness. Messaged to `ScribeLesson` (§ below).
- **F5 — "below the R20 row" is line order, not adjacency.** The note sits at 220 against R20 at 169
  (+51; the R20/R21 section's command block intervenes). The landed `check_r3` keys on `note > r20`
  (`r-defect-closure.sh:178`), which the placement satisfies; a future check that keys on an adjacency
  window would fail a correct file. Recorded so the next round's suite does not "fix" it into adjacency
  and move every line in between.
- **F6 — `check_r4`'s prose limb is a paragraph test, not a row test.** `para_grep` (`:117-123`) matches
  with `awk RS=""`, so the three tokens need only co-occur in one blank-line-separated block; QUALITY's
  round-34 table (note + R22/R23/R24) is one such block. It passes today only because R24 carries all
  three tokens together, but a later edit that splits `kill rule` / `selftest case=` / `per case` across
  R22 and R24 would still read `open=0`. If R24 lands, the durable check is `grep '^| R24 |'` plus the
  three tokens on that row — the same tightening R24 asks of other counters.
- **F7 — why R24 is the right carrier and not a restatement of R17/R19.** R17 assigns each limb a
  one-limb mutant; R18/R19 bind closure checks to bytes; R13 binds before/after to one instrument. None of
  them says the summary line must be backed by case lines. The round-33 specimen is measured and committed:
  the skip-selftest mutant printed `selftest cases=9 failures=0` exit 0 **without running a fixture** and
  passed the frozen kill-rule letter (`.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75`), with the fake
  checker printing `selftest cases=0 failures=0` exit 0 in the same receipt; the verifier routed the fix
  as R4 (`corpus/lessons/round-33-verifier-spotcheck.md:174-176`). The R24 criterion generalizes that
  routing, and its "do-nothing control … rejected" clause is the same discriminator the landed suite uses
  for itself (`r-defect-closure.sh:24-32`: nine `selftest case=R#` lines, "a summary line alone cannot
  satisfy that").
- **F8 — R24 names no round-34 instrument, deliberately.** At composition `corpus/instruments/kill-rule-check.py`
  is absent (`ls` → `No such file or directory`, `exit=2`), `capture-binding-check.py` is mid-edit
  (`sha256 3d9e5e0d…`, 23 `("` case-tuple lines, one `summary-only-selftest-rejected` hit), and
  `r-defect-closure.sh` landed only during this window. Naming any of them as a landed specimen would be
  contract-only evidence presented as execution evidence, so the R24 cell grounds on round-33 committed
  bytes only. If the wave lands them, add their receipt paths to the grounding cell — the criterion does
  not depend on it.
- **F9 — the note corrects R20 by appended text, and says so.** A reader of `corpus/QUALITY.md:169` alone
  still sees "exactly one". That is the R3-required shape (append-only note naming R20), but it is worth
  one line in the round-34 lesson: the bar now has a clause corrected in a note rather than in its row,
  and the note's own words are the only place the per-id mechanics live. The alternative R6 form — a
  same-line suffix on `:169` — remains open per `ExecQualityAppends.md:202-205`; it would keep all anchors
  and put the correction where a row-only reader sees it. My wording works in either case; only the
  placement differs.

### 7. Scratch

```
$ ls -d /fast/scratch/hyaku/kasegi-r34/ScribeQualityDraft
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/ScribeQualityDraft': No such file or directory
exit=2
```

(before-bytes copy, the assembled after-bytes, the HEAD copy, the diff and the reduced `--root` fixture
tree were all under that directory; nothing outside it and the two wave-1 artifacts above was written).

### 8. Out of scope / not claimed

No axis verdict, no score claim, no product edit, no verification of the instruments' own selftests
(not mine to run), no judgment of R4's lesson-side erratum (the suite reported it closed on the current
`corpus/lessons/round-33.md` copy — `sha256 f69472f3…`, `+109/-0` vs HEAD at read time — which is
`ExecLessonErrata`'s evidence, not mine).

Commands run: `sha256sum`, `wc`, `grep`, `sed`, `diff`, `git status/show/cat-file`, `ls`, `test`,
`python3` (anchor table, assembly, digests), and `bash corpus/instruments/r-defect-closure.sh --root` twice
against the reduced scratch root. Every one exited 0 except the `ls -d` cleanup probe (2, expected) and the
two reduced-root suite runs (1, expected: R5/R6/R8/R9 absent in that fixture). No other instrument was
executed; no tool was installed.

## Addendum — state at yield (the owner moved `corpus/QUALITY.md` after §1)

`ExecQualityAppends` did **not** apply Deliverable A. It appended its own R24 and left R22/R23 as they
were. Measured at yield:

```
$ sha256sum corpus/QUALITY.md ; wc -l corpus/QUALITY.md
2bb724fb65ef37e9c9af954cb932bb5e7f21c5576b726be55e1bf541012d1090  corpus/QUALITY.md
228 corpus/QUALITY.md
exit=0
$ grep -n '^| R24 |' corpus/QUALITY.md
228:| R24 | A counter's mutant kill rule is recorded and tightened: the selftest
exit=0
$ grep -c 'M34-' corpus/QUALITY.md ; grep -n 'M34-2' corpus/QUALITY.md | cut -c1-100
2
226:| R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal const
```

So Deliverables A/B remain corrections of the **landed** rows, and F1 is now visible in the committed-to-be
file (`:226` still carries M34-2).

Four defects in the landed R24 (`:228`), all measured, none of which flips the closure counter:

| # | landed text | measured / routed record |
|---|---|---|
| a | "`corpus/lessons/round-33-verifier-spotcheck.md:173-175` (R4 — **3 of 4 mutants survived** the frozen rule)" | direction inverted: R4 reads "C1 counter mutants **3/4 under the frozen kill rule**: skip-selftest survives …" and `RevClaimsFreeze.md:75,172` records M1/M2/M3 caught, M4 NOT caught → **3 killed, 1 survived**. Also the cite starts one line early: R4's heading is `:174` and its text runs `:174-176`; `:173` is R3's tail ("bytes violate (S029, S006). Amend by appended note …"). |
| b | "with cases**>=11**" | stale floor: this round's C1 floor is **N>=19** (`.ufo/waves/round-34/claims.json` C1 counting command; `ExecCaptureBindingHarden` item 8: "`selftest cases=N failures=0` with N>=19"). A criterion that pins 11 forbids this round's counter. |
| c | "A counter's mutant kill rule **is recorded and tightened**" | shape: an act in the past tense, not an obligation the next counter can fail; every other R row states a test, not a landing. |
| d | "the selftest clause requires one `selftest case=<name>` verdict line per case with cases>=11, so a summary-only forgery (cases=0 failures=0) cannot satisfy it" | the forged-`cases=0` case is excluded, but the equality between the declared `cases=N` and the number of printed verdict lines is only implied by "per case": no clause makes a forged `cases=19 failures=0` with **zero** case lines fail *because the counts disagree*, and the row does not name the counter's frozen floor separately from the general one. Deliverable A's R24 states both conjuncts ("fails when the summary is not backed by N verdict lines and by a case count at or above the frozen floor"). |

Token-level check of the landed row (the suite's own limb, replicated, not re-run):

```
'kill rule' 1   'selftest case=' 1   'per case' 1   '>=11' 1   'survived' 1
```

`check_r4`'s limb 1 (`r-defect-closure.sh:188-201`, `para_grep 'kill rule' 'selftest case=' 'per case'`)
therefore reads **closed on a row that misstates the measurement it cites and pins the wrong floor**. That
is precisely the discriminator R24 is about, turned on its own row: the closure counter cannot tell a
correct criterion from a plausible sentence.

`ScribeLesson` replied (it owns `corpus/lessons/round-33.md`, not round-34's lesson): it declines to mint
M34-* ids in a round-33 file, reports its file digest as `120937c6…`, and states that round 33's lesson
already records the survivor events (M33-6, present at `corpus/lessons/round-33.md:96`). Measured lane file
at yield: `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` (`+109/-0` vs HEAD —
`ExecLessonErrata`'s errata append). The digest difference is consistent with the file moving after that
seat's measurement; **[INFERENCE]** — I did not see the revision they hashed. Their point 1 concerns the
*lesson*; M34-1 as frozen names the round-33 *report* lines 41/49, so the two records can both stand. No
action taken: the round-34 lesson's § Mistakes ownership and the M34-2/M34-3 decision are the L1's.

My §4 run used `corpus/lessons/round-33.md` at `f69472f3…`, which is still the current digest, so the R4
lesson-limb reading stands at this byte.

## Addendum 2 — owner dispositions and the bytes as they will land

`ExecQualityAppends` replied after my addendum: it accepted findings 1 and 3 (direction inverted; cite off
by one) and fixed **the R24 grounding cell only**; it referred 2 (floor `cases>=11` vs this round's N>=19)
and 4 (row shape) to the L1, because the row wording was supplied verbatim by KasegiR34; for that same
reason it did not adopt my block. Measured on the tree after that edit:

```
$ sha256sum corpus/QUALITY.md ; wc -l corpus/QUALITY.md ; git diff --numstat -- corpus/QUALITY.md
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
228 corpus/QUALITY.md
15      0       corpus/QUALITY.md
exit=0
$ sed -n '228p' corpus/QUALITY.md      # grounding cell only, criterion text unchanged
… | `corpus/lessons/round-33-verifier-spotcheck.md:174-176` (R4) and the round-34 erratum at
`corpus/lessons/round-33.md:215-226` — the frozen rule **caught 3 of 4**, skip-selftest (M4) survived
(`.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75,172`, finding F-5); M34-1 at … (the 'all mutants killed'
overstatement) |
```

The corrected citations resolve, checked at their own lines: `round-33-verifier-spotcheck.md:174` is
`- **R4** C1 counter mutants 3/4 …`; `corpus/lessons/round-33.md:215` is
`## Erratum (round 34) — R4: "all mutants killed" overstated; the frozen kill rule caught 3 of 4`, and
`:225-226` read "the counter's four mutants were killed **3 of 4 (3/4)** under the frozen kill rule as
written, plus a separate plain-run survivor" (the erratum's table continues after `:226`, so `215-226` is a
block address for heading + prose, which is how it is cited).

State that stands, and what is still open for the L1:

- **Resolved by the owner:** the inverted direction (addendum defect a) and the one-line-early cite
  (defect c). F1 is **not** resolved: `corpus/QUALITY.md:226` still carries M34-2 in both cells
  (`grep -c 'M34-' corpus/QUALITY.md` → `2`, at `:226` and `:228`).
- **Open, referred to the L1:** the pinned floor `cases>=11` against this round's C1 floor N>=19
  (`claims.json` C1 counting command), and the past-tense shape. If both stand, the bar and the claim
  describe the same instrument with different floors; one line in the round-34 lesson (or SCORECARD) naming
  that R24's floor is the counter's own would keep them from disagreeing on their face.
- **My block's expected digest in §3 is superseded as a target**, because the file gained a row after I
  assembled it (`eb20eafc…` → `77d99df9…`). The block text itself is unchanged
  (`sha256 41c51a86…`); if the L1 adopts it, re-assemble against `77d99df9…` (replace 215-227) and
  recompute, rather than aiming at `63bdf7db…`.
- `check_r4`'s row limb stays green on the landed row (owner's emulation, `row_limb_exit=0`, and no
  SCORECARD fallback paragraph, `scorecard_para_exit=1`); the four defects in the addendum are therefore
  invisible to the counter, which is the gap F6 names.
