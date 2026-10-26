# SimplReport — round-36 redundancy/drift review of the drafted lesson, scorecard and report

Seat `SimplReport` (simplifier, L2 leaf — no dispatch). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(only lane repo). Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims freeze
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`. Judged axis: calibration. Milestone round-36.
Assignment: review the drafted lesson/scorecard/report for redundancy and drift, produce a **corrections
list (no edits)**, and confirm the report satisfies the required sections in order. This seat edited no
draft and no lane byte; its only writes are this receipt and `/fast/scratch/hyaku/kasegi-r36/SimplReport/`
(removed after the receipt was written). Tooling: none installed or upgraded; no pacman transaction
attempted (host-wide pause). No git/jj mutation; reads were `git show/log/ls-files/cat-file/merge-base`
and greps.

Read instants below are given per artifact because **the drafts moved under this seat**. Where a defect
was fixed in flight, both the defective and the corrected reading are printed. Line numbers are as of the
digest stated; re-grep the quoted string rather than trusting a number.

---

## 1. What was reviewed (state at the stated read, final digests)

| draft | path | state at final read (2026-10-26T15:5xZ) |
|---|---|---|
| report | `.ufo/waves/round-36/wave1/ScribeReportDraft.md` | 425 lines, sha256 `03b3a87b0e…`; 75 `[MEASURE` slots |
| lesson | `wave1/ScribeGateLesson.md` (lesson text inside) | 742 lines, sha256 `5956552d0a…` |
| scorecard | `wave1/ScribeScorecard.md` | 205 lines, sha256 `6711d4c671…` |
| LOG entry | `wave1/ScribeLOG.md` | 146 lines, sha256 `828901a11e…` |
| SHONEN | `wave1/ScribeShonen.md` | 296 lines, sha256 `2eb561fb2a…` |
| cross-check receipts | `ExecC1SuiteBuild`, `ExecC1BaseFail`, `ExecRegressionBase`, `ExecC2Capture`, `ExecC2QuoteOnce`, `ExecManifestChecks`, `ExecCensusReplay`, `ExecScoreGap`, `ExecInstrumentsSynopsis`, `CritMotivation`, `Scout*`, `ScribeMistakes`, `ScribeQualityRows`, `ScribeAssimilationGate`, `ScribeEntryF19`, `ScribeRowS053`, `ExecGateReviewPrep` | all read at the same window |

Earlier reads used in this receipt: report draft 340/399-line revisions, lesson scratch `lesson.md`
390/399/404-line revisions, entry receipt at its 12:41 and 12:43 compositions. Those states are named
where they matter.

Discipline notes: (a) every number in the five drafts traces to a named receipt or a printed command; the
exceptions are the unbacked items filed below (C1, C2, C4 and the frozen-control key at C19). (b) Two peer
notes were sent (ScribeGateLesson, ScribeReportDraft) naming the items now marked *applied* below; both
seats applied them before landing. That is coordination, not edit.

---

## 2. Report section-order conformance (required six, in order)

`ScribeReportDraft.md` headings at `03b3a87b`:

| # | required section | present | line | conformance note |
|---|---|---|---|---|
| 1 | Work performed | yes | 31 | opens by naming C1 (depth:verifiability) and C2 (coverage) and both target axes |
| 2 | Landed changes | yes | 107 | every row tied to the LOG entry and to a commit cell (most still `[MEASURE: commit]`) |
| 3 | Before → after measurements | yes | 131 | one block per claim; counting commands present; measured commit named per block |
| 4 | Sources & frontier | yes | 286 | rows before→after, added by tier, touched old→new, frontier advanced — **missing the row-counting command (C6)** |
| 5 | Trend verdicts | yes | 326 | expansion / quality / discernment, each with evidence, no scalar |
| 6 | SHONEN | yes | 384 | one bullet per box, all `[~]` |

Trailer lines required by the item spec: `**Stale-lane:**` (412), `**Tooling installs:**` (417),
`**Open L0 questions:**` (420) — present, after SHONEN. `grep -c '^## SHONEN'` = 1. No duplicate
`## Report` heading.

**Verdict: order and presence PASS at this read, conditional on C5 (no placeholder text may be published)
and C6 (counting command).** The report will fail the round's marker rule as it stands, not because a
section is missing but because 75 `[MEASURE]` slots and two drafting paragraphs are placeholder text.

---

## 3. Authority ledger this review measured (so corrections rest on bytes, not on drafts)

All read-only, cwd = lane, at `b47f2cd` unless a ref is named.

| surface | value | command |
|---|---|---|
| `SKILL.md` | `daeff71b…`, 1104 lines | `sha256sum`, `wc -l` |
| `SCORECARD.md` | `ed6e931f…`, 1404 lines; `filled by the L1` 0, `<LANE_HASH>` 0; `Final lane commit` at `:987`, `:1129`; `Erratum (round 35)` 1; `round-34 depth:density row` 1; `201.2` 6 lines / 8 occurrences | greps as frozen |
| `LOG.md` / `SHONEN.md` / `PROVINCE.md` | `a576d58c…` 1659 / `90385026…` 160 / `b4bb5fee…` 75 (F18 0, F19 0) | `sha256sum` |
| `corpus/QUALITY.md` | `d4f83bb1…` 250; `supersedes R22` 1, `R23` 1 at `:249-250` | `sha256sum`, greps |
| `corpus/README.md` / `corpus/SOURCES.md` | `277f04ce…` 396 / `0f95a132…` 112; frontier 18; registry 52; tier A 49 / B 1 / C 2; status mined 40 / queued 9 / rejected 3 | frozen greps + python row parse |
| `knowledge-expected.txt` / knowledge | `d2e99ca6…` 49 lines, 47 rows / 47 `*.md` | `grep -c '\.md$'`, `ls` |
| E4 provenance note | **absent**: `ls .ufo/waves/round-35/wave1-results.json*` lists one file (`0d28a45c…`, 391 lines, tracked); the only committed note is round-34's `e1c44301…` | `ls`, `git ls-files` |
| E5 / E6 / E7 | present 1 / `Correction (round 35)` 1 (path-pinned) / 1 & 1 | greps |
| suite negative controls | `3266c993…` → `closed=0/9 exit=1`; `0aee0ef…` → `closed=4/9 exit=1` (E1/E3/E4/E8/E9 open); `b47f2cd` → `closed=5/9 exit=1` | `ExecC1SuiteBuild.md` §Export runs |
| capture | raw 26,804 B sha256 `66fece52…`; normalized 8,448 B / 244 lines sha256 `4ec61c59b0e9aedf…83e9`; manifest `f9590c2b…`; 0 redirects; URL `https://www.first.org/epss/` | `ExecC2Capture`, `ScoutCaptureAvailability` |
| entry deliverable | final bytes **263 lines / 17,374 B / sha256 `36df1b1f9b4f…a641`** (extracted from `ScribeEntryF19.md` between its markers and hashed) | python extract + `sha256sum` |
| S052 digest | real `d69349e86c5cce17146ccb4a…779e8826`; `77e8826` is not a substring (the report's correction is right) | `sha256sum corpus/source-snapshots/round-35/S052.txt` |
| wave shape | 64 seats: executor 18, scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2; spawn 64 / resume 0 | `wave1-spec.json`, `wave1-dispatch.json` |
| watchdog | `launch kasegi round=36` at `.ufo/watchdog.log:1527`; `complete kasegi round=36` 0 | `sed`, `grep -c` |
| 13-of-14 control replay | `c1 7/7 MATCH` (2 derived), `c2 6/7 MATCH, 1 DIFF (junk_present)` | `ExecRegressionBase.md:153-158` |
| submission-layer checks | `grep -c 'Erratum (round 35)'`=1; dead-seat sentence 0; no-harm instrument baseline 26 runs / 26 exit 0 green | greps, `ExecInstrumentsSynopsis.md:12` |

---

## 4. Corrections list (not applied; each names its preserving contract)

Legend: **[applied]** = the drafting seat fixed it in flight after a peer note, verified in the landed
bytes; **[open]** = still present at the final read and needs the L1.

**C1 [open] — SHONEN asserts a provenance note that does not exist.**
`ScribeShonen.md:37` "`0d28a45c…` / 391 lines; **tracked**; provenance note present"; `:205` "(391 lines,
tracked, provenance note beside it)"; `:244` "r35 results tracked + provenance … **OBS present/tracked**".
Measured: tracked = 1, note = **0** (ledger row "E4 provenance note" above). Corrected text: "tracked
`0d28a45c…` (391 lines); the beside-note is **absent** — E4's `provenance-note` limb is 0 at the freeze
and owed as an L1 landing." This is one of two statements across the five documents that would be *false*
in committed bytes (the other is C2); the suite's E4 payload, ScribeScorecard F4, the lesson table and
`ExecRegressionBase` F5 already say 0.

**C2 [open] — LOG claims a fixture corpus that will not land.**
`ScribeLOG.md:119` "Landed `corpus/instruments/r36-closure.sh` + `corpus/instruments/r36-fixtures/`".
`ExecC1SuiteBuild.md` "Deviations" #3: fixtures are generated per selftest case under `--work` "instead of
a committed `corpus/instruments/r36-fixtures/` corpus". Corrected text: drop "+ `corpus/instruments/
r36-fixtures/`"; say "fixtures generated per selftest case under `--work`; no committed fixture corpus".
(The report already carries this wording after C-applied #2.)

**C3 [open] — LOG's adversarial-seat share mixes two definitions.**
`ScribeLOG.md:127`: "adversarial seats 23/64 = 35.9 % (reviewer 10 + critic 6 + mutation-tester 5 +
sentinel 2 — the round-35 entry's 31.2 % counted the same set without sentinel)". Round-35's 31.2 % is
**20/64 = reviewer 10 + critic 5 + mutation-tester 5** (the round-35 lesson/report definition: reviewer +
mutation-tester + critic); it never included sentinels. This round under that definition is **21/64 =
32.8 %**; the 23/64 set is a *different* set. Corrected text: "adversarial seats 21/64 = 32.8 % (reviewer
10 + critic 6 + mutation-tester 5, the round-35 definition); including the 2 sentinels, 23/64 = 35.9 %."
Preserves: one definition per number, comparable across rounds.

**C4 [open] — E4's landing has an owner in no receipt.**
Frozen E4 is "round-35 `wave1-results.json` tracked with provenance note"; the suite implements the
beside-note reading (`ExecC1SuiteBuild.md` E4 limbs; base run `tracked-ref=0,tracked-index=1,
provenance-note=0`) and its landing list #2 asks for `.ufo/waves/round-35/wave1-results.json.provenance.md`.
No seat drafts that file. Corrected text: the report's Landed-changes row (already present) and the LOG
entry must both name this file as an owed L1 landing; if the L1 prefers the alternative reading (the
round-34 note counts), an appended erratum must say so — either way the tracked file alone does not close
E4, and `closed=9/9` is unreachable until the note lands.

**C5 [open] — report publishes as a skeleton with 75 slots.**
`ScribeReportDraft.md:8` "Draft status: **skeleton** …"; `:26` "Still in flight at this draft, so their
deltas stay `[MEASURE]` …"; `grep -c '\[MEASURE'` = 75. The round's marker rule: placeholder text, missing
sections or no evidence pointers = round **failed**. Corrected text: delete both drafting paragraphs and
replace every slot from the post-integration gate run (`ExecGateReviewPrep.md` prints `c1.export-ref`,
`c2.frontier-rows` 19, `c2.registry-rows` 53, `entries=22 pass=22`, `source-recheck`, `capture-binding`,
`quiescence`); retitle from "DRAFT skeleton (ScribeReportDraft receipt)" to the report title.

**C6 [open] — Sources & frontier lacks the row-counting command and contradicts itself.**
Contract: "`SOURCES.md` rows before→after with the counting command". `:288` gives "52 → 53 rows" without
the command; `:298-299` reads "Rows touched old→new: **none** … The one change to pre-existing text is an
appended R9 correction". Corrected text: add `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'
corpus/SOURCES.md` → 53; reword to "rows unchanged (every S001–S052 cell byte-identical); one
append-only correction paragraph follows `:79`". Preserves: the counting evidence and the append-only rule
(R6) without two readings of "touched".

**C7 [open] — two E1–E9 tables in one report (duplicate authority).**
`:152-168` (counter/before/after) and `:171-182` (limb × four refs) both restate the same nine limbs;
17 `^| E…` rows in one document, plus the suite's printed payloads, the scorecard block and the lesson
table = four authorities for the same literals. Corrected text: keep the matrix table (it carries the
final-head column) and let the suite's payload be the literal authority; delete the other table or reduce
it to the five counters the claim's `counting_commands` names. Preserves: every measurement (nothing is
lost; each row's evidence pointer stays).

**C8 [open, advisory] — repeated counters across sections.**
`entries=22 pass=22` appears 3× in the report, 3× in the scorecard, 2× in LOG; knowledge 47→48 appears in
Work performed, Before→after, Trend verdicts and SHONEN. Corrected text: numbers live in Before→after;
Work performed names the counter, Trend verdict cites the section. This is the same class round-35's
`SimplifierDocs` P3/P4 routed; do not cut the evidence cells themselves (they are the graded axis).

**C9 [open] — scorecard attributes everything to the frozen controls.**
`ScribeScorecard.md:42`: "every before-column below is the frozen control measured at this round's base
bytes". The frozen files hold 7 + 7 keys; E2/E4/E5/E6/E7 cells and the r35-base/r35-judged columns are the
seat's own §3 measurements and the suite's payloads. Corrected text: split the attribution three ways —
frozen-control keys ("`c1-controls/before.txt` / `c2-controls/before.txt`"), seat measurements (§3), suite
payloads (`ExecC1SuiteBuild`). Preserves: each cell's provenance.

**C10 [open] — scorecard carries an unset shell variable.**
`ScribeScorecard.md:58`: `--export-ref "$ROUND36_HEAD"` in a block to be committed. Corrected text:
substitute the measured hash at closure (E1 binds the recorded line, not the command), or move the command
into the receipt only. Preserves: the "append verdicts, do not rewrite the table" instruction.

**C11 [open] — lesson carries a pending section into committed bytes.**
`ScribeGateLesson.md:356`: `### Non-author spot-check — result pending`. Corrected text: state it as a
fact with owner — "no non-author spot-check exists at filing; owed to the round-36 verifier" — or omit the
section until the verifier files. Preserves: the lesson's own statement that nothing certifies the round.

**C12 [open] — lesson duplicates the considerthese disposition.**
`ScribeGateLesson.md:408` calls its § considerthese "this seat's summary of the same seven proposals"
while the long-form table is `ScribeConsiderthese.md` §2; both would land. Corrected text: land one — the
receipt's table (it carries per-proposal evidence) — or keep the summary and cite it, not both. This is
the rule the lesson already applies to the assimilation Gate ("paste one of them, not both").
Preserves: the seven dispositions.

**C13 [open, minor] — census block prints an annotation as output.**
The lesson's before block shows three census lines plus `census_exit=0`; the frozen `census-before.txt`
has three lines. Corrected text: label it "exit captured: 0" rather than a fourth output line.

**C14 [open, minor] — stale entry size in the SHONEN ledger.**
`ScribeShonen.md:63,:143,:229` say "262 lines / 17,267 bytes as drafted". The final entry bytes (after the
pre-landing digest fix) are **263 lines / 17,374 B / `36df1b1f…a641`**. Corrected text: mark the 12:41
figures superseded, or drop the size (it is not load-bearing). The lesson already carries the corrected
figures.

**C15 [open] — frozen E4 wording vs implemented check (claim-level, erratum material).**
The predicate's words admit two readings; the suite implements the beside-note reading. Corrected text for
the report/lesson: state which file the note belongs to (round-35's results, round-34's note as the
pattern), and if the L1 adopts the narrower reading, file an appended claims erratum — never edit
`claims.json`. Preserves: R22 (freeze satisfiability) and the no-edit rule.

**C16 [open, guard] — the frozen "five routed defects" count.**
Spot-check §5 routes **six** items. The report (`§5.1–§5.6`), the lesson (`:101` "routed six items … the
frozen claim counts five") and the scorecard (F7) now say six. Corrected text: do not repeat "five" as
fact in any committed document; the count belongs in the appended erratum.
Status evidence: lesson and scorecard fixed in flight; LOG's M36 bullet names the spot-check without a
count ✓.

**C17 [open, low] — the lesson's Mistakes section is anchors-only until integration.**
`ScribeGateLesson.md:366-372` now says the six-field rows "are to be appended under them at integration"
and that "the `M36` grep E8 runs counts either form". That is honest, but E8's literal is weaker than the
minting contract: if the L1 appends only the anchors, the round has four ids with no re-runnable evidence
field. Corrected text: append `ScribeMistakes.md` §1's table under the anchors (it already carries class ·
evidence command+output · captured-by · fix · able-to-fail), or record in the lesson that the anchors are
the committed form and the receipt is the evidence. Preserves: the minting contract the section cites.

**C18 [open] — SHONEN receipt carries 12 integration slots.**
`ScribeShonen.md` holds 12 `⟨…⟩` slots (`grep -c '⟨'` = 12) for the final lane hash, the post-append
digests/lines, the density pair and the sibling ruling. The receipt's own §2.2 is right: fill each from the
named receipt or delete the clause — never publish a slot. The report's SHONEN section carries none ✓.
Preserves: SHONEN's "resolvable evidence pointer" rule.

**C19 [open] — `junk_present=1` is quoted as a before value that is not a base property.**
`ScribeReportDraft.md` quotes it in the C2 before-controls list (with a caveat at the E-check notes);
`ScribeScorecard.md` F5 and `ScribeGateLesson.md` §Gate both flag it. Measured: `c2-controls/` holds
`before.txt` only; `c2-controls/junk-f19.md` is absent at the freeze; `ExecRegressionBase` files the key
DIFF/ambiguous (F6); `claims.json` C2 `before[1]` itself says "junk-f19 absent (control not yet built)".
Corrected text: state the key verbatim, then state it is unbacked and that the twin exists only after this
round lands — do not use it as the twin's before-state anywhere. Preserves: the frozen control is quoted,
not rewritten.

**Applied in flight (recorded for calibration, no action left):**
- report `12/12 MATCH` → "c1 7/7 MATCH (2 derived), c2 6/7 MATCH, 1 DIFF" (`:86`, `:141-142`) — verified
  against `ExecRegressionBase.md:153-158`.
- report `r36-fixtures/` removed from Work performed and Landed changes; replaced with the `--work`
  wording (`ExecC1SuiteBuild` deviation 3).
- report capture-binding after-cell → lane-root `records=43 bound=43 unbound=0`, with the `1/1` fixture
  reading labelled (`:242`); verified against `ExecManifestChecks.md:18,267`.
- report Landed-changes row no longer promises a self-referential lane-commit line (`:118`), matching
  ScribeScorecard F2 and E1's actual limb.
- lesson "the five defects" → "routed six items … the frozen claim counts five" (`:101`).
- lesson PASS attribution → `36df1b1f…a641`, 263 lines / 17,374 B, with `c4f7d5b4…88e0` named as the
  intermediate first-fix revision (`:189-190`); the entry-digest line list corrected to
  `:46,:73,:87,:124,:143,:394`.
- lesson "pasted verbatim" claim for the Mistakes rows replaced by an explicit owed statement (the
  six-field rows are to be appended under the anchors; see C17).

---

## 5. Cross-draft contradiction matrix (what the L1 must reconcile before landing)

| topic | report `03b3a87b` | lesson `5956552d` | scorecard `6711d4c6` | LOG `828901a1` | SHONEN `2eb561fb` | authoritative |
|---|---|---|---|---|---|---|
| E4 beside-note | absent at freeze, owed (fixed) | absent, owed | absent; after-cell says "adds the note" (F4) | measured 0, not listed as landing | **"present"** (C1) | 0 — suite + `ls` |
| fixture corpus | none (fixed) | none | none | **"Landed r36-fixtures/"** (C2) | none | none lands (suite deviation 3) |
| adversarial share | not stated | not stated | not stated | **23/64 = 35.9 % w/ wrong parenthetical** (C3) | not stated | 21/64 = 32.8 % (lesson definition) |
| routed defects | §5.1–§5.6 | six (claim says five) | F7 six | no count | not stated | spot-check §5 = six |
| entry size | — | 263 / 17,374 B ✓ | — | — | **262 / 17,267 B** (C14) | 263 / 17,374 (extracted+hased) |
| `junk_present=1` | quoted with caveat | flagged as unbacked | F5 flagged | not mentioned | not mentioned | unbacked (`ExecRegressionBase` F6) |

---

## 6. Stop condition: what this seat deliberately did **not** call redundant

- **Evidence density is not redundancy.** The per-limb payloads, the capture digests and the per-check
  before/after cells are the artifact the round is scored on; cutting them would remove the axis being
  measured. The report's C1/C2 measurement blocks and the lesson's Gate tables are retained whole.
- **Historical quotations of the forbidden literals are provenance.** The report quotes
  `filled by the L1` (2 occurrences) and `<LANE_HASH>` (3) while explaining and counting E1 — twice and
  three times because one is the E1 prose and one is a counting row; the lesson and LOG quote the stale
  sentence to correct it; `ScribeEntryF19.md:116` quotes the bad digest to disclose it. E1 is
  `SCORECARD.md`-scoped and the suite's own limit is documented. Flagging these as "placeholders left"
  would be a false positive; the only true placeholder classes are C5 (75 report slots), C10 (unset
  variable) and C18 (12 `⟨…⟩` slots in the SHONEN receipt — fill or delete per its own §2.2).
- **`[MEASURE]` in a *receipt* is legitimate.** A draft cannot measure the final head; the defect is
  publishing it (C5), not drafting it.
- **No file deletion is proposed.** The redundancy found is duplicate *statements* inside documents, not
  dead alternate paths; no deletion candidate exists that would not remove evidence. Consequently no
  semantic-reference proof is applicable: these are Markdown prose bytes with no call graph, and every
  claim in §4 rests on literal `grep -c`/`sha256sum`/`git show` output printed above — literal evidence,
  not semantic-caller evidence. (An LSP `references` query is not available for prose and none is
  presented as proof.)

---

## 7. Verdict

- **Report:** required sections present and in order; trailer lines present; one SHONEN heading. It does
  **not** satisfy the marker rule yet: 75 `[MEASURE]` slots plus two drafting paragraphs are placeholder
  text (C5), and § Sources & frontier lacks its counting command (C6). With C5/C6/C7 addressed at
  integration it conforms.
- **Lesson:** evidence-bearing and internally honest; the in-flight fixes are verified. Remaining:
  C11 (pending section), C12 (duplicate considerthese authority), C13 (exit annotation), C17 (six-field
  rows owed under the anchors).
- **Scorecard:** the strongest of the three on self-criticism (F1–F7); remaining: C9 (attribution),
  C10 (unset variable) — both editorial, neither changes a value.
- **LOG/SHONEN:** two hard defects (C1 false provenance note; C2 false fixture landing) and one count
  drift (C3) that must not reach committed bytes; C4 (E4 landing ownership) is the one item that decides
  whether C1 can close.

---

## Report

Item result: reviewed the three primary drafts plus the LOG/SHONEN drafts against the receipts and the
lane bytes, and produced **19 corrections** (C1–C19): 3 statement-level defects that would be false in
committed bytes (C1, C2, C3), 1 unsatisfied-claim blocker with no owner (C4), 5 conformance/publication
items (C5, C6, C7, C10, C11), and 10 attribution/duplication/owed-evidence items (C8, C9, C12–C19).
Seven items were observed live and
corrected in flight by the drafting seats after direct peer notes; each is recorded with both readings.

What was actually run here: `sha256sum`/`wc` over nine lane files; the frozen counting greps (frontier,
registry, E1 tokens, E2/E3/E4/E5/E6/E7 literals); a python row parse for the tier/status histograms; the
entry extraction + hash (which reproduced ExecC2QuoteOnce's PASS digest); `sha256sum` of the S052 capture
to test the digest correction; `git show <ref>:<path>` for six revisions of the round-35 lesson; `sed` of
the watchdog log; and greps over the five draft receipts. Nothing was rebuilt, re-synced or re-run from a
seat's own workflow.

Not measured here (and not claimed): any post-integration value — `closed=9/9`, `entries=22 pass=22`,
frontier 19, registry 53, knowledge 48, census after, quiescence. Those are the L1's gate run
(`ExecGateReviewPrep`), and this receipt asserts none of them.

Scratch `/fast/scratch/hyaku/kasegi-r36/SimplReport/` (audit script, extracted entry) removed after this
receipt was written. No lane file, fleet file, sibling lane or source tree was written; no tool installed.
