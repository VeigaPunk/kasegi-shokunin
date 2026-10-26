# SimplifierDocs — round-35 minimality review of the drafted docs

Seat `SimplifierDocs` (simplifier, L2 leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(write scope). Lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims freeze
`617496b9c6e92bc671e7e78b83df69a04470d0e9`.

Assignment: YAGNI/minimality review of the drafted docs — report draft, lesson draft, scorecard
draft, SHONEN edits — each statement evidence-backed; flag filler, repetition and placeholder prose;
propose deletions where content is non-load-bearing, preserving contract-required sections. **This
seat edits no document.** It proposes, measures, and hands the decisions to the L1.

Read instants are stated with every count because **the drafts were moving under this seat**: the
report draft changed digest three times (`0580d593…` → `66f974fb…` → `c1a6871d…`, and again by 06:49Z) between
06:38Z and 06:49Z, and the Gate drop-in grew 202 → 220 lines in the same window. Every number below carries its
read time; a number without one is a defect in this receipt.

Report line numbers below are pinned to the **06:50Z / 407-line** revision of
`ScribeReportDraft.md`, which the drafting seat was still extending (29,930 B at 06:44Z → 34,225 B at
06:49Z). Re-grep the quoted string rather than trusting a number: the draft rewrites sections, so a
coordinate ages faster than its text.

---

## Report

### R1 — What exists, what does not (read 2026-10-26T06:38Z–06:49Z)

| document | in-scope draft | state at read |
|---|---|---|
| report | `.ufo/waves/round-35/wave1/ScribeReportDraft.md` | **exists, complete** — 407 lines / 34,225 B at 06:49Z (29,930 B at 06:44Z; the seat was still appending), no `PENDING` marker left (was 111 lines with 6 at 06:38Z) |
| lesson | `ScribeGateAssimilation.md` §"Gate block" drop-in (220 lines / 19,772 B at 06:47Z) + `ScribeIntegrationNotes.md` Draft A (124 lines / 10,428 B) | **partial** — only the Gate section and the LOG entry are drafted |
| lesson §Mistakes | owned by seat `ScribeMistakesDraft` | **unfiled at 06:49Z** (`ls .ufo/waves/round-35/wave1/ScribeMistakesDraft.md` → absent) |
| lesson §considerthese | no owner filed text | **unfiled** |
| scorecard | owned by seat `ScribeScorecard` | **unfiled at 06:49Z**; `SCORECARD.md` carries only the D1/D2 in-place landings (`git diff SCORECARD.md`, 2 hunks) and **no round-35 section** |
| SHONEN | owned by seat `ScribeShonen` | **unfiled at 06:49Z**; `SHONEN.md` unmodified (`sha256 8d876418…`, 82 lines, 4 boxes at `:5`, `:21`, `:34`, `:54`) |

Of 64 wave-spec items, **23 had no receipt at 06:40Z** (`python3` comm of `wave1-spec.json` item
names against `wave1/*.md` basenames): `ConnClaims, ConnSibling, ConnTrends, CritBoundary,
CritMistakes, CritOverclaim, ExecCensusAfter, ExecDoNothingReject, ExecRegressionC1,
ExecRegressionC2, MutClosureSuite, MutJunkTwin, RevD1D2, RevEntryF18, RevNoHarm, ScribeLesson,
ScribeMistakesDraft, ScribeScorecard, ScribeShonen, SentCred, SentScopeFinal, SimplifierCleanup,
SimplifierDocs`. Four of those are the exact owners of the documents this seat was asked to review,
so §R5 below gives the L1 the filter to apply when they land.

### R2 — Verdict per draft

**Report draft — evidence-bearing, three duplication classes, one arithmetic error.**
Not filler: the C1/C2 subsections (40 + 47 = 87 lines of a 407-line draft at 06:49Z) are measurement tables, and each cell carries the literal
*and* the receipt that printed it (e.g. `:171` `S052` at `corpus/SOURCES.md:58`; `:180-186` capture
digest + `count=1756` + `cvss` 0 with `ExecC2Capture.md` §2–§4). That density is the graded axis
(depth:verifiability) and §R3's stop condition protects it. What does not carry information is
listed in §R3 P1–P6.

**LOG entry draft (Draft A) — evidence-bearing and honest; oversized and 17 slots unfilled.**
It marks each defect's true state (`**landed**`, `**pending the L1's commit**`, `**open**`) instead of
asserting the after-state, e.g. `ScribeIntegrationNotes.md:66-68` "… still **untracked** (`git
ls-files … | wc -l` = 0 at 06:43Z)" and `:75-80` "**D7** … still reads `supersedes R22` = 0 … **the
draft rows are not landed rows**". At 124 lines / 10,428 B it is 2.8× the round-34 entry's 48 lines /
3,735 B (`LOG.md:1601-1648`), and it carries 17 `⟨FILL…⟩` slots (`grep -o '⟨FILL[^⟩]*⟩' | wc -l`).

**Gate drop-in — evidence-bearing; the largest single block in the round's documentation.**
220 lines vs the round-34 lesson's whole Gate section, 120 lines (`corpus/lessons/round-34.md:110-229`).
Its §1a (fetch verdict = property of the invocation: UA/TLS/URL-truncation table, `:113-135`) is new
measured evidence that *corrects round 34's own Gate table* — keep. Its §2 discrimination table
(8 control rows) is receipt-grade.

**QUALITY append (D7 text) — conformant, no cut proposed.** 21 lines / 2,842 B; the `R26` row line is
1,063 chars against the file's own precedent `R19` at 1,082 chars (`corpus/QUALITY.md:103`), and the
`R6 form:` paragraph matches the round-34 block's convention (`corpus/QUALITY.md:217`). Cutting it
would break a local convention without saving a convention-breaking amount.

**Erratum D5 / entry F18 / search-log receipts — evidence-bearing; one product-file defect is open.**
See C-4.

### R3 — Deletion proposals (ranked; each names the contract section it preserves)

**P1 — delete `ScribeIntegrationNotes.md` §B.3 "Reusable skeleton" (44 lines / 1,976 B).**
A template for a *future* round's provenance note inside a round-35 record. It is non-load-bearing:
Draft B itself says "the note already exists; do not rewrite it", and the real note is committed text
(`.ufo/waves/round-34/wave1-results.json.provenance.md`, 5,639 B, digest `e1c44301…` as cited at
`ScribeIntegrationNotes.md:181-199`). Preserves: Draft A (LOG entry) and Draft B §B.1/§B.2 (identity
pin + closure steps) untouched.

**P2 — collapse the `<LANE_HASH>` column in the report's `## Landed changes` table.**
At 06:47Z the report carried **14 `<LANE_HASH>` tokens and 2 `<LOG_COMMIT>`**; in the landing table
every C1/C2/round-close row's commit cell is the same single final commit by construction (the
draft's own header, `:13`, says "final lane commit `<LANE_HASH>`", singular). A column whose every
value is one value is padding: keep the *file list* (it is the landed-surface index) and state the
commit once. Preserves every row's content; removes 6–8 cells of one repeated token and the
placeholder surface the round is closing elsewhere (D1 class).

**P3 — one authority for the seven per-defect before→after pairs.**
The same seven literals are stated in three places: report §C1 table (`:126-165`, 40 lines), LOG
Draft A's C1 bullet (`ScribeIntegrationNotes.md:~60-82`), and the suite's own
`D<i> check=… open=0|1` output (measured below in §R6). Round-34's report had **no** per-defect table
(§Before → after was 25 lines of prose, `.ufo/reports/round-34/kasegi.md:88-112`) and its LOG entry
carried the ledger. Recommendation: the **report** keeps the table (it is the verifiability
artifact), the **LOG** keeps one sentence per claim plus the score, and the seven literals live in the
suite's output. Expected cut ≈ 1.5 KB of the LOG draft; no evidence lost.

**P4 — the report's `## Work performed` claim bullets (`:21-34`, 14 lines) restate the frozen predicate
in reworded form, not verbatim** — measured: 4 shared 8-word shingles against `claims.json`
(0.6% of the report's shingles), so this is *not* byte duplication but a **second authority that can
drift**. Proposal: keep the C2 bullet (it carries the "distinct from CVSS severity" argument the
report must make) and reduce C1 to the after-state with a pointer to `claims.json` at its pinned
sha256 `fe0dae89…` (verified, `sha256sum .ufo/waves/round-35/claims.json`). Saves ≈ 8 lines.

**P5 — the prose placeholder in `## Boundary and open items` must be filled or deleted, never
published.** At 06:50Z one remained: `:385` "**Dead seats and wave completeness.** `<from the wave
registry / L1: names and counts>`" (`<from ` count = 1; it was 2 at 06:39Z, and the sentinel bullet
became the work-items line at `:98`, which names `SentCred`/`SentScopeFinal`/`CritBoundary` instead of
carrying slots). That slot is the D1 class in prose form, and **no
closure check scans the report** (`check_d1` greps `SCORECARD.md` only — `sed -n '/^check_d1()/,
/^}/p' corpus/instruments/r35-defect-closure.sh`). If the sentinel seats file, paste verbatim; if
they die, delete the bullet rather than publish a slot. Tradeoff stated: adding the report path to
`check_d1` would close the hole but changes an instrument's printed readout that its selftests
assert — the L1's call, not this seat's.

**P6 — decide one owner for the no-harm paragraph.** Report `:157-164` (`recheck-audit.py
lines=47 total=47 pass=47 …`, `anchorcheck.py … 0 bad`, `SKILL.md 13/0`, `SCORECARD.md` 15
deletions) overlaps the lesson §No-harm that `ScribeLesson` will draft, which in round 34 was
`corpus/lessons/round-34.md:406-441`. If the lesson owns it, the report keeps one line + pointer.

**P7 — optional: trim the Gate drop-in's §2 control table from 8 rows to 3.** The
`registry -S037` and `register -S054` fixture rows restate the same assertion as the baseline; the
load-bearing rows are `baseline`, `+S052` (the C2 prediction) and `missing registry` (fails closed).
Saves 5 rows. **Only if the L1 wants the lesson's Gate section near round-34's 120 lines**; the
table is not filler, it is budget.

**P9 (optional) — the critic enumerations in `## Boundary and open items` are one line + a pointer
each, not ten.** `:353-363` lists `CritC2Kill`'s six gaps G1–G6 and `:367-375` lists `CritMistakes`
F2/F3 as findings with a per-gap correction pointer. That is the round's open-item register, so it is
load-bearing — but six gap labels in the report plus the same six in `CritC2Kill.md` is two
authorities for one list. Keep the labels and the receipt pointer here, drop the per-gap restatement
(≈ 8 lines), or keep as is and drop them from the lesson's §Open items. Not both.

**P10 — do not cut, and say so in the round record.** The C1/C2 evidence cells, the §1a UA/TLS table,
the D2 "row-scoped by necessity" note, and the `Measurement state` digests are the axis being scored.
After P1–P7 the next deletion removes measured evidence: **that is the stop condition.**

### R4 — Findings that are correctness, not minimality (reported, not fixed)

**C-1 — arithmetic in the report's headline verdict.** `:275-282` reads "**quality: `improved`** —
five of the seven routed defects are closed and measured (D1, D2, D3, D5 closed; D4's record is
digest-verifiable but its `tracked` clause is the L1's commit; D6/D7 are drafted and measured on
copies, not landed)". Four are closed, one is commit-pending, two are unlanded: the sentence's own
parenthetical sums to 4+1+2=7 while its first clause says five. One word to fix ("four"), or
"five closed or commit-pending".

**C-2 — the report pins a stale instrument identity.** `:398-399` pins
`corpus/instruments/r35-defect-closure.sh` `d7ad84384eb4…`, 32,148 B, 773 lines. Measured 06:45Z:
`0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f`, **35,391 B, 834 lines**. The
draft discloses that its digests will move (`:393-396`), so this is not a false claim — but critic
F-1's own smallest fix is "record `sha256sum` **after the last edit**" (`:330-334`), and as drafted
the report would publish a digest that matches no byte of the landed tree. Re-digest at close.

**C-3 — D6's predicate forbids quoting the sentence it corrects (independently confirmed).**
`check_d6` requires `grep -c -F 'did not file a receipt (dead seat' L1Integration.md` **= 0** *and*
`grep -c -F 'Correction (round 35)'` ≥ 1 in the same file. Fixture proof (scratch, deleted):

| fixture | stale | corr |
|---|---|---|
| sentence replaced **and** correction quotes the old wording | **1** → check open | 1 |
| sentence replaced, correction paraphrases ("the dead-seat sentence at :30 was wrong") | **0** → check closes | 1 |

Consequence for the L1, beyond what the report already records (`:322-329`, citing
`RevD5D6D7.md` §F2): the fix method is an **in-place reword of a committed round-34 receipt**, which
is the act round-34's own D4 calls a defect ("A seat transiently rewrote the committed
`wave1/ExecRegressionC1.md`", `corpus/lessons/round-34-verifier-spotcheck.md` D4). The integration
receipt must therefore name the method, and the provenance survives in git history
(`git show <round-34-tip>:…`) rather than in the file.

**C-4 — a wrong digest is live in a product file, and the fix is 8 characters, not a pointer.**
`corpus/SOURCES.md:79` prints `sha256 d69349e8…77e8826`; the capture's tail is `779e8826`, so the
abbreviation drops a `9` (verified: `awk 'NR==79' corpus/SOURCES.md | grep -o 'd69349e8[^ ]*'` →
`d69349e8…77e8826`; full digest `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`).
Round 35 appended **five** R8 lines (`:108-112`, 2,911 chars: 1,216 / 244 / 146 / 790 / 515), of which
the two that address the landed bullet (`:111` 790 chars, `:112` 515 chars) total 1,305 chars and
**neither corrects the digest** — `:111` points the reader at a 4,495-B wave draft for the corrected
value. Minimal repair: append one short R8 statement carrying `d69349e8…779e8826` (or re-state the
bullet's digest in the correction). Append-only discipline is
preserved either way; the pointer-to-a-receipt form is what costs bytes and forces a second fetch.

**C-5 — one stale denominator.** `ScribeQualityDraft.md` F7 quotes `gap: 24 of 46 rechecks …`; the
instrument prints `24 of 47` at 06:46Z (`python3 corpus/instruments/score-gap.py`, exit 0), and the
report already uses 47 (`:289`). If the lesson cites the gap, cite 47 and the read instant.

**C-6 — transient, now reconciled (recorded for the D5 audit trail).** At 03:41Z
`claims-erratum-d5.md` was 256 lines / 12,636 B / `f22a16ff…` while `ScribeErratumD5.md` §8 recorded
254 / 12,445 / `0d304b92…`, and the 12,445-byte prefix hashed to `97122d6f…` (not append-only). At
03:46Z file and receipt agree (262 lines / 13,086 B / `eee0bb57…`). No action; recorded because D5's
artifact identity is part of the closure.

### R5 — The filter for the four unfiled drafts (apply when they land)

For `ScribeLesson` / `ScribeScorecard` / `ScribeShonen` / `ScribeMistakesDraft`, in order:

1. **Every numeric token carries a read instant or a receipt** (§R4 C-2 is this round's live instance).
2. **No slot survives publication.** A `⟨FILL⟩`, `<from …>`, or "the L1 fills" sentence in the
   landed bytes is the D1/R1 class; count them (the suite only counts SCORECARD's two spellings).
3. **One authority per number.** Check the three copies that already exist (report §C1/C2 tables,
   LOG Draft A, SCORECARD rows) before writing a fourth. Restating *with a different rounding or a
   different denominator* is C-5, not brevity.
4. **Keep the contract sections** — lesson: `Frozen claims / Gate / Mistakes / considerthese /
   Census / No-harm / Open items / Touched surfaces / L1 integration appendix`
   (`corpus/lessons/round-34.md` headings 50/110/230/343/380/406/442/513/523); SCORECARD: the
   round-35 claim row in the existing table shape; SHONEN: the four boxes at `:5/:21/:34/:54` plus
   the integration note.
5. **Match the precedent's size or say why.** Round-34: LOG 48 lines, report 180 lines
   (`.ufo/reports/round-34/kasegi.md`), lesson 561 lines with a 120-line Gate. Round-35 drafts are
   currently 124 / 407 / (Gate 220) — each deviation is defensible only where it adds measured
   evidence; otherwise it is budget.

### R6 — Commands, outputs, exit codes (all read-only except this receipt and §R8 scratch)

1. `bash corpus/instruments/r35-defect-closure.sh` (06:45Z) → exit **1**
   ```
   D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
   D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
   D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
   D4 check=tracked=0,provenance=1 open=1
   D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
   D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
   D7 check=supersedes-R22=0,supersedes-R23=0 open=1
   closed=4/7 exit=1
   ```
   (Same readout at 06:36Z and 06:43Z — D4/D6/D7 open across the window.) The frozen after-state
   `closed=7/7` is therefore **not yet true at tip**, as the report itself states at `:278-282`.
2. `sed -n '/^check_d1()/,/^}/p' corpus/instruments/r35-defect-closure.sh` → greps `SCORECARD.md`
   only; `check_d6` → the two literals in `L1Integration.md` only.
3. `sha256sum .ufo/waves/round-35/c1-controls/before.txt .ufo/waves/round-35/c2-controls/before.txt
   .ufo/waves/round-35/census-before.txt .ufo/waves/round-35/c1-controls/fake-suite.sh
   .ufo/waves/round-35/c2-controls/junk-f18.md` → `352d3da2…`, `2835700332…`, `74fc6a26…`,
   `292aaac0…`, `0abec359…`, exit 0 — **all five digests match the drafts' quoted values**.
4. `sha256sum .ufo/waves/round-34/wave1-results.json` → `3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4`,
   `ls -l` → 312,874 B, exit 0 (matches the report's D4 row at `:133`).
5. `sha256sum corpus/source-snapshots/round-35/S052.txt; wc -l …` → `d69349e8…79e8826`, 27,870 lines,
   exit 0 (matches the report's capture paragraph at `:180-186`).
6. `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **18**; `grep -cE '^\|[[:space:]]*S[0-9]{3,}
   [[:space:]]*\|' corpus/SOURCES.md` → **52**; `grep -nE '^\|[[:space:]]*S052[[:space:]]*\|'` → 1
   (`:58`); `grep -c 'd69349e8…77e8826'` on `:79` → 1 (C-4). Exit 0 each.
7. `python3 corpus/instruments/score-gap.py` → exit 0, `gap: 24 of 47 rechecks …` (C-5).
8. `python3 corpus/instruments/score-gap.py` threshold line → `SCORECARD.md:331` (report `:290`
   cites the same line).
9. `python3` comm of spec names vs receipts → **23/64** without a receipt at 06:40Z (§R1).
10. D6 fixture (scratch): `grep -c -F -- 'did not file a receipt (dead seat'` → quoted correction
    **1**, paraphrase **0**; `grep -c -F -- 'Correction (round 35)'` → **1** in both (C-3).
11. `sha256sum corpus/instruments/r35-defect-closure.sh; wc -lc …` → `0ae4b484…`, **834 lines /
    35,391 B** at 06:45Z (C-2).
12. `wc -lc corpus/knowledge/cisa-kev-catalog.md` → 118 lines / 17,643 B at 06:45Z; the report's
    `:355` "117 lines" and the digest it pins were correct at its own read and the entry moved after
    it — a live-value case for §R5 rule 1, not a claim error.
13. Section-size measurements (§R2; report line map at 06:50Z, 407 lines): `## Work performed` 15-102 (88),
    `## Landed changes` 103-120 (18), `## Before → after measurements` 121-125 (5), `### C1` 126-165 (40),
    `### C2` 166-212 (47), `## Sources & frontier` 213-266 (54), `## Trend verdicts` 267-295 (29),
    `## SHONEN` 296-319 (24), `## Boundary and open items` 320-392 (73), `## Measurement state` 393-407 (15); Gate drop-in 220 lines / 19,772 B;
    LOG Draft A 124 lines / 10,428 B; §B.3 44 lines / 1,976 B; QUALITY append 21 lines / 2,842 B;
    `R26` row 1,063 chars vs `R19` 1,082 chars.

### R7 — Digests of the files read (read-time, 06:38Z–06:49Z)

| path | sha256 |
|---|---|
| `.ufo/waves/round-35/wave1/ScribeReportDraft.md` | `c1a6871d5e6a04166718fcfe3ef4c808e5a773f468dfdd146d24a9c4a3c79a1a` (06:47Z; moved again by 06:49Z — 407 lines / 34,225 B) |
| `.ufo/waves/round-35/wave1/ScribeIntegrationNotes.md` | `585c8f2ae52481505dd488e1f87022f93b0b7556e1d079891242b85df5518a6f` |
| `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md` | `00774b35ea853edc978c58c33251cb74610fc5f0dd72033e0bd2881cc6ad9bc7` |
| `.ufo/waves/round-35/wave1/ScribeQualityDraft.md` | `ffe46ad853e70cc47464bb7df266ceaef713cc47104aeadd4635d453b4130e8e` |
| `.ufo/waves/round-35/wave1/ScribeSearchLog.md` | `d62047282dc316615fb3b3917c0b604677110b1d9680b17dfcc61a008e2c007d` |
| `.ufo/waves/round-35/wave1/ScribeEntryF18.md` | `25afabd8e5527c5ffb9339a95c971df9026759dca9a16fb34e0e5999725e7ac9` |
| `.ufo/waves/round-35/wave1/ScribeErratumD5.md` | `56639a33c075851a746be50a026b83fe5542822b3a3ccab986d127898c4c3f35` |
| `.ufo/waves/round-35/wave1/ExecClosureSuite.md` | `d771fb618e9ff3a205d7642657cb6cafc4141388fe6843eeb7ba201dec7d361f` |
| `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` | `b086936919174837f48e04b4209794cc7738716a25abaae3396d43a2dfe5b5a0` |
| `.ufo/waves/round-35/claims-erratum-d5.md` | `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6` (262 lines / 13,086 B) |
| `.ufo/waves/round-35/claims.json` | `fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982` |
| `SCORECARD.md` | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` |
| `corpus/SOURCES.md` | `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba` |
| `corpus/README.md` | `277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2` |
| `corpus/QUALITY.md` | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` (229 lines — the D7 append is **not** applied) |
| `SKILL.md` | `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc` |
| `SHONEN.md` | `8d876418418dda755209634ebff92b91d308ab9c14c18ccd4295ce00cb5d1941` |
| `corpus/instruments/r35-defect-closure.sh` | `0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f` |

### R8 — Scratch, boundary, tooling

- Scratch `/fast/scratch/hyaku/kasegi-r35/SimplifierDocs/` held `suite.out`, `suite2.out`,
  `d6-quote.md`, `d6-norewrite.md`; the two fixture files are quoted in C-3 and were deleted with the
  tree before this receipt was filed (`test -e` → `rc=1` below).
- No document edited; no git/jj command beyond read-only `git diff`/`git log`/`git show -s` reads; no
  `git add`/`commit`/`push`; nothing written under the fleet root, sibling lanes, `bounties/` or
  `/home/vgpnk/Projects/shokuknow`; no shokuknow campaign tool run (`renumber-staged.py`,
  `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` never invoked — the register and
  package were read only).
- Tools installed or upgraded: **none**. No `pacman` transaction (host-wide pause respected), no
  `uv tool`/`npx`/binary install. Used: `bash`, `coreutils`, `grep`, `sed`, `awk`, `sha256sum`,
  `python3` (stdlib), `comm`, `ls`.

### R9 — Limits

- Every count is a 06:38Z–06:49Z reading of a tree that was still being written; the report draft's
  digest changed three times in that window (four observed states). A number quoted here without re-reading is stale by
  construction, which is exactly C-2's point.
- I did **not** re-derive the staged-package id set independently: one attempt globbing
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/*.md` returned `staged_ids=1` (the package files sit
  below that level) and I did not chase it, so §R4 makes no claim about the collision count beyond
  what `ExecIdCollisions.md` and the Gate drop-in both print (21 before the `S052` row, 22 after) and
  what the committed `assimilation/collisions-post-c2` lists (`S031`–`S052` = 22, consistent).
- I reviewed the **drafted** text, not the landed product bytes of D7 (not applied) or of the report
  (not yet in `.ufo/reports/round-35/`).
- The four unfiled drafts (§R1) are unreviewed by construction; §R5 is a filter, not a review.
- I do not judge the round, its scores, or any claim's truth; the gestures above are measurements and
  proposals.

**Bottom line for the L1:** apply P1–P7 and, if the budget is tight, P9 (≈ 60–70 lines / 5–7 KB of non-evidence; P5 is the
only one that is also a closure risk), fix C-1 and C-4 (one word and eight characters), re-pin C-2 at close, and
record C-3's method when landing D6. Everything after that is the graded evidence — cut it and the
round loses the axis it is claiming.

### R10 — addendum after peer confirmation (2026-10-26T06:53Z; C-4 routing)

`ScribeSOURCESRow-2` independently reproduced C-4 and reports the same arithmetic: full digest
`d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`, `D[-8:] = 779e8826`,
`'77e8826' in D` → `False`. Three seats now hold the defect (their F8, `ScribeSearchLog-3`'s
D-R35-SL-1, this seat's C-4), which makes it measured evidence rather than one seat's read.

Two facts the L1 needs, both from that message and verifiable in the lane:

1. **No seat holds the append.** The peer reports it holds no write, and that `ExecRegistryAppend`
   disclaimed round-35 authorship ("it is the round-33 seat"); the lines at `:58`/`:79`/`:108-110` came
   from an unnamed round-35 seat and `:111-112` from another. The repair therefore lands with the L1.
2. **The smallest conforming text already exists**, drafted as an appended R8/R9 statement at
   `ScribeSOURCESRow.md` §1d (heading `:48`; the paste line is the body of the fence at `:56-58`), and it changes no row cell. Landing it
   supersedes my C-4 "minimal repair" sentence — same 8 characters, already worded, no new drafting.
3. **Do not bundle it with `:111`/`:112`.** `:111`'s citation of `:79`'s sha256 (`f2ab0a64…`) is correct
   (it hashes line 79 including its trailing newline, `930274a1…` for the line text alone), so a bundle
   must not imply that citation is wrong; `:111`'s own defects are the §5 size/digest and the
   "superseded by a draft" wording.

C-4's verdict is unchanged; only its ownership is now known to be the L1's.

### R11 — second addendum: peer's final defect list, and one C2 provenance gap it exposes (06:56Z)

`ScribeSOURCESRow-2` closed (receipt `a6c7f874…886adc`) with three unfixed `corpus/SOURCES.md` defects and
one self-correction. Attributed, with what this seat re-verified read-only:

| item | source | re-verified here |
|---|---|---|
| `:79` "7 SOURCES rows" | peer F2 | **independently verified here**: at base `3266c993` the registry carries exactly **5** CISA rows — `S003, S008, S021, S023, S026` — and the file has 7 `cisa` hits in total, the two extras being prose in earlier sweep bullets (`git show 3266c993:corpus/SOURCES.md \| grep -i cisa\| cut -c1-80`; `… \| grep -ci cisa` → 7). So "7 SOURCES rows" is a miscount of grep hits, not rows; the peer's 6-with-`S052` follows at the tip |
| `:79` digest `…77e8826` | peer F8 = C-4 | verified independently (§R4) |
| `:111` "superseded by a draft" + stale §5 citation | peer item | text verified present; the §5 size/digest is the peer's measurement |
| `:112` scope omits `corpus/source-snapshots/` | peer item | **verified material**: `:112` says the zero-hit counts are scoped to `corpus/knowledge/*.md` (46 files), `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md`; `grep -c 'source-snapshots'` on `:112` → 0, and **8** files under `corpus/source-snapshots/` carry the `KEV` token (`grep -rl 'KEV' corpus/source-snapshots/ \| wc -l` → 8) |

**The provenance gap this exposes in the report (new, mine; widened by the peer's F10).** The report's
search-log paragraph (`:216-218`) discloses *one* pre-existing KEV precedent —
`corpus/lessons/round-22.md:91`. Root ground holds two more, both verified here:

- `corpus/source-snapshots/round-24/S009.txt:122` quotes a **secondhand KEV statistic** — "The CISA KEV
  says only about 400 new vulnerabilities were tracked as exploited, and only around 40 of those were
  zero-days" (`awk 'NR==122' … | grep -o '.\{110\}KEV.\{110\}'`);
- `corpus/source-snapshots/round-24/S001.txt:1082` **names CISA KEV as a data source** in its own
  sentence — "…(Information Sharing and Analysis Center), CISA KEV or private …"
  (`awk 'NR==1082' … | tr ' ' '\n' | sed -n '5,20p'`).

F18's admission is unaffected — a statistic or a source-name inside a vendor-facing page is not the
catalog, and the sweep's question is whether the lane holds a source that *prioritises by exploitation
status* — but a sentence reading "the lane held no KEV ground" is false corpus-wide, and the sweep is
**source-level, not string-level** (the peer's own amended wording). Smallest fix: one sentence naming
the four-surface scope and the precedents it excludes (the captures), or the scope alone with the
"pre-existed only at" phrasing dropped.

The peer's `:111` finding is also now sharper than my §R10 note: the cited "4495 bytes,
`dc1a549a…`" for §5 matches none of the three measured states of `ScribeSearchLog.md`
(34,565 B / `4c1ef7ae…`, 41,362 B / `d6204728…`, final **48,898 B / `ee89a818…`**, 670 lines — the last
one re-measured here at 06:58Z). A wave draft cannot supersede a registry line in any case.

Together with C-4 this makes four L1-applied edits on `corpus/SOURCES.md` (`:79` digest, `:79` row count,
`:111` wording, `:112` scope) plus the report sentence above; the peer holds no write authority and
`ExecRegistryAppend` disclaimed round-35 authorship (§R10), so all five land with the L1.
