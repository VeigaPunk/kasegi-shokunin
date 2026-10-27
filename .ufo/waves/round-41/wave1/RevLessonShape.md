# RevLessonShape — wave-1 receipt (round 41, build wave 1)

Seat: `RevLessonShape` · Lane: `kasegi-shokunin` · Run-utc: 2026-10-27T08:26:33Z
Item: **receipt-only** — read `corpus/lessons/round-40.md` fully, list the structural defects the
round-41 lesson must NOT repeat, and produce the round-41 lesson must-carry checklist. This receipt
is the checklist; no separate deliverable file.

Inputs read (all committed lane bytes, read-only): `corpus/lessons/round-40.md` (263 lines, full),
`corpus/lessons/round-40-verifier-spotcheck.md` (§1 §2 §5), `corpus/lessons/round-39.md` (heading
map), `.ufo/waves/round-40/wave1-dispatch.json`, `.ufo/waves/round-40/wave2-dispatch.json`,
`.ufo/waves/round-40/wave2/RevC2Decisions.md`, `.ufo/waves/round-41/claims.json`, `SCORECARD.md`
(`## Round 40 result` + the `Correction (round 40)` block), `.ufo/reports/round-40/kasegi.md`
(fleet repo, read-only). Disk guard green at start (25% used on /fast/scratch/hyaku).

## Part 1 — round-40 lesson structural defects the round-41 lesson must NOT repeat

**S1. Duplicated `## Gate` heading.** `corpus/lessons/round-40.md` carries `## Gate` twice, at L29
and L31 (consecutive). Root cause per `wave2/RevC2Decisions.md` D3: the scribe deliverable
`wave1/ScribeGateBlocks.txt` itself opened with `## Gate` and was pasted under the existing
`## Gate`, so the Gate body began under a second identical heading. The verifier spotcheck §1/§5
records it as D4. Must-not-repeat: exactly one `## Gate`.

**S2. Garbled parenthetical in the census line.** `corpus/lessons/round-40.md` L27 reads:

> `… Registry 59 → 62 rows; tier A +3?mined S016/S017/S019/S020/S021/S023/S025/S060, rejected S061/S062, carried S022/S024 flips); rows touched old→new: …`

`+3?mined` is a mangled `+3 (mined` and the `)` after "flips" is unbalanced. The wave-2 seat
(`RevC2Decisions` D2) and the verifier spotcheck (§2 C2, §5 D4) both had to *reconstruct* the
intended text ("tier A +3 (mined S016/…/S060; rejected S061/S062; carried S022/S024 flips)") instead
of reading it. Must-not-repeat: balanced, machine-checkable prose in the census line.

**S3. Wrong attack-role tallies in the wave-shape line.** `corpus/lessons/round-40.md` L9 states:

> `Attack share: wave 1 17/54 = 31.5%; wave 2 33/35 = 94%; round total 50/89.`

The dispatch JSONs give wave-2 attack roles = reviewer 12 + critic 7 + mutation-tester 6 = **25/35**
(71.4%), and round total = 17 + 25 = **42/89** (47.2%). The report (`.ufo/reports/round-40/kasegi.md`
L12) says exactly that: "Attack roles reviewer/critic/mutation-tester were 17/54 in wave 1 and
25/35 in wave 2 (42/89 overall)." The lesson's `33/35 = 94%` and `50/89` are both wrong (each
overcounts by 8); the verifier spotcheck §1/§5 records it as D5. The wave-1 figure (17/54 = 31.5%)
is the only correct one. Must-not-repeat: never carry tallies from prior prose; recompute from the
dispatch JSON.

**S4. Framing that narrows the frozen clause after landing (the verifier's exact complaint).**
`corpus/lessons/round-40.md` §Wave-2 falsification L216 headlines:

> `**C1 — the suite holds at the verification ref; no live defect defeats a check.**`

The frozen C1 kill rule (round-40 `claims.json`, re-quoted in the round-41 C1 kill rule) is: *"a
committed fixture shows a check passing while its defect is present."* The lane's own round-39
standard (`SCORECARD.md` `## Round 39` C1 row: "Wave-2 G2 payload mutations also pass the
instrument, so the frozen C1 pass claim is not admitted") treats that class as blocking. The
round-40 wave-2 fixtures fire the rule — `wave2/RevC1Counters.defeats.txt` T2 (substring values
`closed=7/80`/`failures=10` accepted), T4 (fenced pseudo-row passes), T7 (symlink out-of-export
declaration passes), T13 (mention-only registry row passes), T14 (H6 case/separator escape),
`wave2/CritKillRule.h6-escapes.sh` (seven escape states), `wave2/MutH6H10.md` D2 (leaf-capped green
base). The lesson's "no live defect defeats a check" swapped the frozen predicate (committed-fixture
based) for a weaker one (live-defect based) and reclassified the firings as "routed to round 41
(instrument robustness; no change to the frozen counter this round)" — narrowing the clause after
landing. The verifier spotcheck §2 C1 rules: kill rule FIRES; C1 not verified. Must-not-repeat: the
wave-2 verdict sentence must rule on the frozen clause verbatim, not on a restated weaker one.

**S5. The narrowed framing carried an overclaim into the record.** Because of S4, the report and
the `SCORECARD.md`/`LOG.md`/`SHONEN.md` round-40 lines grade C1 "held; **verified**" while the
frozen kill rule fires — spotcheck §5 D1. The lesson repeats the "holds" verdict with no pointer to
any correction. Round 41 closes this with `Correction (round 41)` lines grading round-40 C1 **not
verified** on the frozen counter and naming the firing evidence (round-41 C1 check I1); the
round-41 lesson must point at those corrections instead of restating the overclaim.

**S6. A tally quoted as recorded with no committed transcript (lane-criterion violation).** The
lesson's wave-2 section quotes `--selftest --export-ref Y` → `cases=10 failures=0` at Y, and the
SCORECARD r40 row repeats it; but the receipt `.ufo/waves/round-40/final-gates/all-gates.txt` (16
lines, all-gates v4) holds **no selftest line** — the only committed graded tally ran over a
scratch Y′ = J5 + receipt, not over Y. Spotcheck §1/§5 D2: this violates the lane's own R37
criterion (a receipt-quoted tally must have a transcript). Must-not-repeat: the lesson may quote a
suite/selftest tally as "recorded" only if the Y receipt contains it; otherwise mark it
`report-only`.

**S7. `captured-by` discipline in the Mistakes table.** The single round-40 row M40-1 records
`captured-by = none at the time (wave-2 attack found it)`. The finder was later identified —
verifier R1 (round-40 spotcheck §2 C1) — but the row itself names no finder with a receipt path,
so the lesson cannot trace who caught it. Must-not-repeat: every M41-n row's `captured-by` names
the actual catching seat/instrument/verifier with a located receipt, or states the round in which
the finder ran.

## Part 2 — round-41 lesson must-carry checklist

1. **Section skeleton, in this order**: `# Round 41 — kasegi` (revisions + judged-head rule +
   shape line); `## Frozen claims — before → after` table; `## Mistakes`; `## Census`; exactly one
   `## Gate`; under it `### Admitted`, `### Rejected`, the status-change log, the seam check,
   `### Assimilation`, `### Sourced claim`; then `## Wave-2 falsification` for any attack wave.
   Round-40's order is fine; its defect was duplication, not order. No section body may re-open a
   heading a deliverable already opened.

2. **One-Gate rule**: `grep -c '^## Gate' corpus/lessons/round-41.md` must print exactly `1`
   before landing. When a scribe deliverable opens with its own `## Gate` (the S1 root cause), the
   landing seat strips the duplicate; do not paste headings blindly.

3. **Tally arithmetic method**: every share/tally in the lesson is computed from primary counts at
   write time — attack roles = reviewer + critic + mutation-tester seat counts taken from
   `wave<n>-dispatch.json` (not from the prior round's lesson, the report's prose, or memory), and
   the summands are shown in the line, e.g. `Attack share: wave 1 17/54 = 31.5% (12+3+2); wave 2
   25/35 = 71.4% (12+7+6); round total 42/89 = 47.2% (17+25)`. For round 41 the line is computed
   from round-41's own dispatch JSONs. On disagreement with the report, the dispatch JSON wins and
   the discrepancy is recorded as a mistakes row.

4. **Wave-shape line**: names each wave, per-role seat counts summing to the dispatch totals, the
   band, dead-seat count, and the attack-share arithmetic of item 3 — all from the round-41
   dispatch/results files. (Round-40 L9 is the counter-example: `33/35 = 94%` / `50/89`, both wrong.)

5. **Census line**: quotes the census output byte-exactly (`W04 S028`, `W04 S029`, `ok`, exit 0 for
   round 41), states registry before → after (62 → 63), the tier arithmetic spelled out (+1 mined:
   S063), the rows touched old → new (S063's status and used-by cells; the new row appended; the
   search-log bullet), with **balanced parentheses** and no stray punctuation — the L27
   `+3?mined …)` mangling (S2) is the counter-example. A paren-balance check on this line is part
   of landing hygiene.

6. **Frozen-claims table numbers match `claims.json`**: C1 before/after cells state the frozen
   after-values only — `closed=12/12 exit=0` at Y, graded `selftest cases=12 failures=0` with the
   selftest transcript teed in the receipt, base `5b29ea14…` and round-40 judged head
   `c7aea5ef…` exports red, plain run exit 2; C2 cells state frontier 24 (F24), registry 63,
   S063 mined with entry + capture + manifest, harness 27/27, binding 55/55, recheck-audit
   expected=60, measure 44/44 = 1.000, census exit 0. No figure appears in the lesson that the
   frozen counting commands cannot reproduce at Y.

7. **Correction pointers (I1 / spotcheck D1)**: the lesson's account of round-40 C1 points at the
   appended `Correction (round 41)` lines in `SCORECARD.md`, `LOG.md`, `SHONEN.md` that grade
   round-40 C1 **not verified** on the frozen counter and name the firing evidence
   (`wave2/RevC1Counters.defeats.txt` T2/T4/T7/T13/T14, `wave2/CritKillRule.h6-escapes.sh`,
   `wave2/MutH6H10.md` D2). The lesson must not restate the round-40 "held; verified" overclaim
   (S5) anywhere, including the frozen-claims table's "Before" column paraphrase.

8. **No narrowing of the frozen clause**: the wave-2 verdict sentences rule on the frozen kill rule
   as written — *"a committed fixture shows a check passing while its defect is present"* — and say
   explicitly whether it fires. "Routed to round N" may describe follow-up work only after the
   verdict on the frozen clause is stated; it may not replace that verdict (S4 counter-example:
   "no live defect defeats a check").

9. **Receipt-quoted tallies carry transcripts (D2/R37)**: any suite or selftest value the lesson
   quotes as recorded at Y must exist in the round-41 receipt
   (`.ufo/waves/round-41/final-gates/all-gates.txt`), which per the round-41 C1 predicate is the
   teed transcript of BOTH the suite run and the graded selftest (time-basis=ref-commit). Anything
   run outside the receipt is labelled `report-only` (S6 counter-example: Y-level
   `cases=10 failures=0` quoted with no committed transcript).

10. **Sourced-claim pointer (S063)**: the lesson names the source the C2 increment rests on —
    S063 (RFC 9116, kind spec, tier A, mined, opened 2026-10-27) — with its capture
    `corpus/source-snapshots/round-41/S063.txt`, its manifest record, and its entry
    `corpus/knowledge/rfc-9116-security-txt.md` carrying the provenance trio (`source: S063`,
    `verified-at:`, `recheck:`); plus the F24 admission 23 → 24 (coverage-map row + PROVINCE
    amendment) and the instrument tallies (harness `entries=27 pass=27` incl. `PASS F24`,
    binding `records=55 bound=55`, recheck-audit `expected=60`, measure 44/44 = 1.000). Mirror the
    round-40 S060 paragraph shape: claim, evidence paths, and what was rejected this round if any.

11. **Mistakes rows with captured-by criteria**: every M41-n row carries the seven columns
    (id, class, event, evidence, captured-by, fix, able-to-fail). `captured-by` names the actual
    finder — seat id + receipt path, instrument selftest case, or the verifier spotcheck — never a
    bare "none at the time" (S7 counter-example: M40-1). `evidence` gives a located quote or
    commit; `fix` names the closed round-41 check (I1-I12 for C1-class, the landed C2 rows for
    coverage-class) or the routed defect id (D1-D6) it answers.

12. **Wave-2 section is verdict-first, evidence-located**: each attacked claim gets the wave-2
    receipts' verdict quoted with seat names and receipt paths, the routed defects listed with
    their finder ids (round-41's own D-set, if a wave 2 ran), and any committed defect found by
    the attack stated with both the defect and its repair (round-40 counter-example of the right
    shape: the S022/S024 teaches-drop found by `RevC2Decisions` and restored the same wave).

13. **Hygiene gate run by the landing seat before commit**, with the outputs recorded in the
    landing receipt: `grep -c '^## Gate'` = 1; paren-balance scan of the census and shape lines;
    heading-order check (`^# ` / `^## ` / `^### ` map matches the item-1 skeleton); the shape-line
    tallies re-summed from the dispatch JSON; the frozen-claims table diffed cell-by-cell against
    `claims.json`.

14. **Byte discipline**: the lesson is landed as one file, append-style corrections only (per
    spotcheck D4's "fix with an appended erratum, not a rewrite" rule for prior-round defects); no
    placeholder tokens, no lane-hash self-reference (a commit cannot contain its own hash — the
    judged head J is named only by the report, per the round-41 `judged_head_rule`), and every
    quoted receipt span is a located quote from committed bytes.

## Part 3 — verification evidence (commands run, actual output)

All commands run from scratch `S=/fast/scratch/hyaku/kasegi-r41/RevLessonShape` (removed before
yield; TMPDIR bound there). No writes outside the receipt path and scratch; no git/jj mutation.

- Role counts from the dispatch JSONs (defect S3):
  `python3` over `wave1-dispatch.json` → `wave1 54 {executor 18, scout 11, reviewer 12, scribe 6, connector 1, sentinel 1, critic 3, mutation-tester 2}`, attack = 17.
  `wave2-dispatch.json` → `wave2 35 {reviewer 12, scout 8, critic 7, mutation-tester 6, connector 1, sentinel 1}`, attack = 25.
  Arithmetic: 17/54 = 31.5%; 25/35 = 71.4%; 42/89 = 47.2% — matching the report L12 ("17/54 … 25/35 … (42/89 overall)"); lesson L9's `33/35 = 94%` / `50/89` disagree with both.
- Heading map: `grep -nE '^#{1,3} '` on round-40.md → `## Gate` at L29 and L31 (duplicate, S1); round-39.md → single `## Gate` at L18 (the correct shape).
- Census line: `awk 'NR==27'` round-40.md → contains `tier A +3?mined … flips)` (S2), confirmed against `wave2/RevC2Decisions.md` D2's transcription.
- Narrowing sentence: `grep -n 'no live defect'` round-40.md → L216 (S4); frozen kill-rule wording re-read from round-41 `claims.json` C1 kill_rule ("a committed fixture shows a check passing while its defect it names is present — including … T2 … T4 … T7 … T13 … T14 … the CritKillRule seven escape states, the MutH6H10 leaf-capped green base …").
- D2 evidence: round-40 receipt `final-gates/all-gates.txt` holds 16 lines, no selftest line (spotcheck §2 C1); SCORECARD `## Round 40 result` C1 row quotes `graded --selftest cases=10 failures=0` (S6).
- Correction target: SCORECARD L1588-1589 carry the `Correction (round 40)` block naming receipt `8371e7ac…` — the precedent the round-41 `Correction (round 41)` lines follow (item 7).
- Disk guard: `bash scripts/hyaku/disk-guard.sh status` green at start (25% used on /fast/scratch/hyaku, 610.2G free).

No tools installed this seat (none needed). No network fetches.
