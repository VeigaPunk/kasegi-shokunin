# ScribeQuality — round-42 wave-1 receipt

Seat: ScribeQuality (leaf scribe, no dispatch). Round 42, wave 1. Lane:
/home/vgpnk/Projects/shokunin/kasegi-shokunin. Frozen claims read first and not edited:
`.ufo/waves/round-42/claims.json` (base `5053a7f46de35784cff4b56756906e9014a38276`, frozen
2026-10-28T12:05:00Z). Draft head at work: `0566bd66e93d429b2df8b6751cf10cbdc391e79b` (round-42:
frozen claims + controls + wave-1 spec/dispatch; base is an ancestor). `corpus/QUALITY.md` is identical
at base and draft head (`git diff --stat 5053a7f4 HEAD -- corpus/QUALITY.md` prints nothing), so the
byte figures below hold across the round so far. Disk guard green before work (see §5).

## 1. Deliverable

`ScribeQuality.criteria.txt` — the append-only `corpus/QUALITY.md` block for round 42: heading, R6-form
paragraph, table header, rows R39-R42. Landable bytes only.

| Property | Value |
|---|---|
| path | `.ufo/waves/round-42/wave1/ScribeQuality.criteria.txt` |
| lines | 17 |
| bytes | 11005 |
| sha256 | `51e227a885b6f31041a8700436a9279c34dd66665434ac1f401f49290c6ebe1d` |
| rows | 4 (`R39`, `R40`, `R41`, `R42`), one physical line each, exactly 4 pipe characters per row line |

Landing measurement (simulated on a scratch copy, then discarded): appending the block to the current
`corpus/QUALITY.md` (337 lines, 60663 bytes, sha256 `a76f42d76f10c123be853f0575bb347848d38e7dcdabdcb2d4eaaccb32a19ac6`)
yields 354 lines, 42 `^\| R<n> \|` rows, max R number 42, R39 at line 351 and R42 at line 354; the tail
17 lines are byte-identical to the deliverable (`cmp` → exit 0, `APPEND_BYTE_IDENTICAL`). Fenced-code
count in the result is 10 (even → closed at EOF; this block adds no fence). No tabs, no CR, no trailing
whitespace in the deliverable.

R6-form literals were run literally, not derived:

```
$ head -c 60663 corpus/QUALITY.md | sha256sum
a76f42d76f10c123be853f0575bb347848d38e7dcdabdcb2d4eaaccb32a19ac6  -
$ wc -l < corpus/QUALITY.md
337
$ wc -c < corpus/QUALITY.md
60663
```

The block states those figures and carries the standard instruction that the landing commit re-runs
both commands immediately before writing (R19: a draft-time byte figure is a stale premise if an
earlier append in the same round moved it). Prior rows were not edited: R22 226, R23 227, R24 228,
R25 229, R26 249, R27 250, R28 263, R29 264, R30 277, R31 278, R32 291, R33 292, R34 307, R35 308,
R36 309, R37 323, R38 337 (line map from `grep -nE '^\| R[0-9]+ \|' corpus/QUALITY.md`).

## 2. Criteria delivered, and the evidence each rests on

| id | rule in one line | primary committed evidence (all paths lane-relative, all reads made this round) | adds over |
|---|---|---|---|
| R39 | a receipt is only ever the unedited tee of one observed run, and its `run-utc` is printed by the run at execution — a ref-commit instant copied into it is a label, not an execution time | `.ufo/waves/round-41/final-gates/all-gates.txt` `:2` `export-ref=1f7464612ac4c44e39886b82e812610d3c039b13`, `:4` `time-basis=ref-commit`, `:5` `run-utc=2026-10-27T12:16:34Z`; `git show -s --format=%ct 1f746461` → `1793103394` → `2026-10-27T12:16:34Z` (same instant); receipt is 31 lines, sha256 `0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94`; `SCORECARD.md:1605` states it as "`run-utc` equal to the ref's committer instant"; r41 verifier step-1 table, `corpus/lessons/round-41-verifier-spotcheck.md:37`, grades it `conformant` | R37 (`:323`) keeps its transcript-or-`report-only` limb; R39 splits the receipt's own byte provenance out as a criterion and forbids two-run composition and a run-utc authored from the ref |
| R40 | evidence that a correction landed is per correction, never a union aggregate; a duplicated block is one correction repeated and counts as a defect, not coverage | `wave2/CritC1KillRule.md:18` (`selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=...evidence=3/3,missing=0`); `wave2/RevCorrectionsFinal.md:5-6` ("`SCORECARD.md` **8**, `LOG.md` **3**, `SHONEN.md` **3** (each meets >=1)"; "collectively name"); `r41-closure.sh:891-914` (`graded` per file, `ev` per stem over the union, `seen` dedupe at `:902-907`); D-r41-1 at `corpus/lessons/round-41-verifier-spotcheck.md:132-134`, duplicates `SCORECARD.md:1602-1605` vs `:1607-1610` byte-identical (`diff` exit 0) | R17/R24 grade instrument limbs and selftest case lines, never the evidence inside a correction |
| R41 | a counted or compared value is read as a whole token and the payload prints the token read; quoted defect evidence is not a result value | `SCORECARD.md:1602` (T2: "`closed=7/80` and `failures=10` accepted as green by substring"); `r41-closure.sh:443-459` (`value_present`); observed I3 `tally=3/3,mangled=0` at `wave2/RevC1Counters.md:24`, `wave2/CritC1KillRule.md:20`; mutant writes `closed=10/100` (`r41-closure.sh:1757-1758`); quoted-defect limb at `wave2/RevCorrectionsFinal.md:8` | R3 names a matcher; R41 fixes what a matcher may read and requires the payload to show the token (a bare `tally=3/3` is ungradable) |
| R42 | a check is repaired only when its selftest's mutant set contains the committed defeat shape for its family and the replay rejection is recorded; a one-line mutant against a duplicated-block defect mutates nothing | `wave2/CritC1KillRule.md:18,20` (`rejected=0 rc=0` for I1 and I3), `:21-22` (`mutants=1/2`, `mutants=0/1`, `verdict=fail`), receipt `all-gates.txt:18,20`; `r41-closure.sh:1683-1690` (`replace_line`, `!done` — first match only), `:1752-1760` (`selftest_case_i3`); family list and kill-rule quote `.ufo/waves/round-42/claims.json` C1; blind-spot instance `corpus/lessons/round-41-verifier-spotcheck.md:148-149` and `wave2/MutFrontierParser.md` | R17 kills a limb with a one-limb mutant and R24 requires a graded case line; neither requires the mutant set to carry the committed defeat |

Mapping to the frozen C1 repair families: R39 -> J8 and the receipt limb; R40 -> J1 (F-EVID) and J11;
R41 -> J2 (F-TOKEN); R42 -> the REPLAY limbs of J1-J7. The r42 claim's seven families are named
verbatim in R42's grounded-in cell (F-EVID, F-TOKEN, F-TABLE, F-DECL, F-SCAN, F-BIND, F-FLIP).

## 3. Commands and observed output

Reads (all from the lane, no writes): `corpus/QUALITY.md` (lines 1-337; several long rows arrive
truncated in the reader and were re-read raw where cited: R37 `:323`, R38 `:337`), `.ufo/waves/round-42/claims.json`,
`corpus/lessons/round-41.md`, `corpus/lessons/round-41-verifier-spotcheck.md` (§1, §5),
`wave2/CritC1KillRule.md`,
`wave2/RevC1Counters.md`, `wave2/RevCorrectionsFinal.md`, `wave2/MutFrontierParser.md`,
`wave2/RevRunUtc.md`, `corpus/instruments/r41-closure.sh` (targeted ranges), `SCORECARD.md:1598-1612`,
`LOG.md`/`SHONEN.md` correction spans, r41 receipt, `.ufo/waves/round-42/wave1/{ScribeScorecard.round42.txt,RevLessonShape.md}`,
`.ufo/waves/round-42/wave1-spec.json` (item 34, my seat spec).

Size and row census:

```
$ wc -l corpus/QUALITY.md; wc -c corpus/QUALITY.md; sha256sum corpus/QUALITY.md
337 corpus/QUALITY.md
60663 corpus/QUALITY.md
a76f42d76f10c123be853f0575bb347848d38e7dcdabdcb2d4eaaccb32a19ac6  corpus/QUALITY.md
$ grep -cE '^\| R[0-9]+ \|' corpus/QUALITY.md
38
$ grep -oE '^\| R[0-9]+ \|' corpus/QUALITY.md | grep -oE '[0-9]+' | sort -n | tail -5
34
35
36
37
38
```

Duplicate corrections (D-r41-1), measured byte-level:

```
$ printf 'SCORECARD: '; grep -n '^Correction (round 41)' SCORECARD.md | cut -d: -f1 | tr '\n' ' '; echo
SCORECARD: 1602 1603 1604 1605 1607 1608 1609 1610 
$ printf 'LOG+SHONEN: '; grep -n '^Correction (round 41)' LOG.md SHONEN.md | cut -d: -f1,2 | tr '\n' ' '; echo
LOG+SHONEN: LOG.md:1736 LOG.md:1737 LOG.md:1738 SHONEN.md:221 SHONEN.md:222 SHONEN.md:223 
$ grep -c '^Correction (round 41)' SCORECARD.md LOG.md SHONEN.md
SCORECARD.md:8
LOG.md:3
SHONEN.md:3
$ diff <(sed -n '1602,1605p' SCORECARD.md) <(sed -n '1607,1610p' SCORECARD.md) && echo DUP_IDENTICAL
DUP_IDENTICAL
```

Receipt provenance (R39 ground):

```
$ grep -n 'time-basis\|run-utc\|export-ref\|suite-sha256' .ufo/waves/round-41/final-gates/all-gates.txt | head -5
1:all-gates v1
2:export-ref=1f7464612ac4c44e39886b82e812610d3c039b13
3:suite-sha256=3971a112c077dd4ffb5536bf0956db0572fb022f19ec135349d639cd96fc52fd
4:time-basis=ref-commit
5:run-utc=2026-10-27T12:16:34Z
$ wc -l .ufo/waves/round-41/final-gates/all-gates.txt; sha256sum .ufo/waves/round-41/final-gates/all-gates.txt
31
0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94  .ufo/waves/round-41/final-gates/all-gates.txt
$ git show -s --format='%H %cI %ct' 1f7464612ac4c44e39886b82e812610d3c039b13
1f7464612ac4c44e39886b82e812610d3c039b13 2026-10-27T09:16:34-03:00 1793103394
$ TZ=UTC date -u -d @1793103394 +%Y-%m-%dT%H:%M:%SZ
2026-10-27T12:16:34Z
```

Verifier citation for the same value (compressed from the table cell at
`corpus/lessons/round-41-verifier-spotcheck.md:37`):
`receipt run-utc=2026-10-27T12:16:34Z = J committer instant (09:16:34-03:00, time-basis=ref-commit);
receipt lands at Y (09:31:58-03:00) | conformant`. The r41 reading and R39's rule differ in scope
(conformant on "not future-dated / equals the ref" vs "the instant identifies the run"): reported
verbatim in §6, not adjudicated here.

Instrument code sites cited in the block (line numbers verified this round):

```
$ grep -n 'value_present()\|qualified_corrections()\|check_i1()\|check_i3()\|replace_line()\|selftest_case_i3()' corpus/instruments/r41-closure.sh
443:value_present()   884:qualified_corrections()   891:check_i1()   950:check_i3()
1683:replace_line()   1752:selftest_case_i3()
$ grep -n 'ROUND40_TALLY=\|EVIDENCE=\|RECORDS=' corpus/instruments/r41-closure.sh
242:ROUND40_TALLY=closed=10/10
249:RECORDS=(SCORECARD.md LOG.md SHONEN.md)
250:EVIDENCE=(RevC1Counters CritKillRule MutH6H10)
```

`replace_line` body (`:1683-1690`) contains the once-only guard `!done && $0 ~ pat { print rep; done = 1; next }`.
`check_i1` counts `graded` once per file and `ev` once per evidence stem across the three files
(`:902-907`: `for stem in "${EVIDENCE[@]}" ... case "$seen" in *" $stem "*) continue ;; ... ev=$((ev + 1))`).

## 4. Scratch experiment — the duplicate-defeat mechanism, measured

Scratch root `/fast/scratch/hyaku/kasegi-r42/ScribeQuality`, `TMPDIR` bound to it; a copy of `SCORECARD.md`
and the extracted `value_present` function (`sed -n '443,459p' corpus/instruments/r41-closure.sh`); the
same awk replacement `selftest_case_i3` applies (`closed=10/100`, one line vs all matching lines).
Output, verbatim:

```
correction_lines=8 bounded_truth_hits_before=2
replace_first: replaced_lines=1 correction_lines=8 bounded_truth_hits_after=2
replace_all: correction_lines=8 bounded_truth_hits_after=0
mutated_line_accepts_closed=10/10=NO
substring_7/80_accepted=NO
substring_failures=10_accepted=NO
exact_10/10_accepted=YES
I3_expected_needle_tally=2/3 -> replace_all_hits=0 ...
```

Interpretation (labelled as inference from these measurements plus the code sites above): the
`value_present` matcher itself is token-correct on every probe; the I3 negative fixture is defeated by
the duplicated correction block, because `replace_line` rewrites only the first matching line and two
of the eight correction lines (`1603`, `1608`) carry a bounded `closed=10/10` that survives. Only
replacing every duplicate drives the bounded hits to 0 — the condition under which the mutant's
expected `tally=2/3` becomes reachable. This is the measured shape R40/R41/R42 encode: per-correction
grading (R40), a payload that shows the token read (R41), and a mutant set that carries the committed
defeat shape (R42). No lane file was modified by this experiment; the scratch copy was disposable.

## 5. Gates, scope and hygiene

- Writes made: `.ufo/waves/round-42/wave1/ScribeQuality.criteria.txt` (deliverable) and this receipt.
  Nothing else. `git status --porcelain corpus/QUALITY.md .ufo/waves/round-42/claims.json` → 0 lines
  (both unmodified). `corpus/QUALITY.md` was only read and copied.
- No git/jj mutation anywhere; no lane commit; no push; no fleet-root or shokuknow write; no sibling
  lane touched; no `~/.local/bin` or PATH write.
- Tool installs: none. Network fetches: none. No host service touched.
- Disk guard at start: green — `/tmp` 5% used / 122.2G free, `/var/tmp` 36% / 576.0G,
  `/fast/scratch/hyaku` 27% / 590.7G (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`).
- Scratch removal: the `trap ... EXIT` did not fire under the bash wrapper (the directory survived two
  trap-guarded invocations: 660K, `QUALITY.md`, `SCORECARD.md`, `first.md`, `all.md`, `vp.sh`). It was
  removed explicitly (`rm -rf -- /fast/scratch/hyaku/kasegi-r42/ScribeQuality`) and verified absent:
  `scratch_present=no`. A transient `/tmp/r41block.md` used for one diff was removed
  (`tmp_leftover=no`). This is recorded as a wrapper behaviour, not as evidence of cleanup by trap.
- Deliverable re-measured after scratch removal and the citation corrections: `deliverable_lines=17 bytes=11005
  sha256=51e227a885b6f31041a8700436a9279c34dd66665434ac1f401f49290c6ebe1d`.
- Unedited-by-me, read-only inputs: `.ufo/waves/round-42/wave1/ScribeScorecard.round42.txt` (no
  QUALITY/R39-R42 references), `.ufo/waves/round-42/wave1/RevLessonShape.md` (lesson-shape review;
  no M42 ids written at read time).

## 6. Findings and known limits

1. **The suite the block names is not committed at draft head.** `ls corpus/instruments/r42-closure.sh`
   → `No such file or directory`; `git ls-files corpus/instruments/r42-closure.sh | wc -l` → 0, while
   `r41-closure.sh` → 1. Every `Round-42 limbs: J<n>` sentence in R39-R42 is therefore a landing
   requirement, stated as such, not a measurement. No J-limb was run.
2. **R39 vs the r41 verifier, reported verbatim.** The r41 verifier reads the same receipt conformant
   (`round-41-verifier-spotcheck.md:37`); R39 says a ref-copied instant is not evidence of when the run
   executed. Both statements are in the block/receipt; the conflict is left for the canonical judge.
3. **Lesson ids are the L1's plan, not landed bytes.** R40/R41 cite `M42-1` and `M42-2` as the
   round's `## Mistakes` rows per the frozen wave-1 spec (item 30: "M42-1 (evidence-union class...),
   M42-2 (token-boundary class...)"), but `corpus/lessons/round-42.md` and
   `wave1/ScribeLesson.lesson.md` did not exist when this draft was written. If the lesson lands other
   ids, the criterion citations must be aligned to the lesson's ids at landing; the primary evidence
   paths in the same cells are independent of the ids.
4. **One root defect explains three r41 observations.** The I1 `evidence=3/3` escape, the I3
   `tally=3/3,mangled=0` escape, and the I1/I3 `rejected=0` mutants share the duplicated correction
   block plus `replace_line`'s first-match-only rewrite (measured in §4). Any r42 fixture that repairs
   one of these by replacing a single line will not repair the others.
5. **Scope of the drafting claim.** This seat drafts criteria only. It made no verdict on C1 or C2, ran
   no suite or counting instrument, and did not test the deliverable against the not-yet-written r42
   suite. The block's landing success depends on R19's re-measurement at the landing commit.

## 7. Out of scope / not touched

`corpus/QUALITY.md` (append only at landing by the L1), `PROVINCE.md`, `corpus/README.md`, `SKILL.md`,
`corpus/lessons/*` (including round-42), `SCORECARD.md`, `LOG.md`, `SHONEN.md`, `SOURCES.md`,
`corpus/instruments/*`, `claims.json`, `considerthese/*`, all `.ufo/reports/*`, the fleet repo, other
lanes, `/home/vgpnk/Projects/shokuknow`. No subagents dispatched.

Report: .ufo/waves/round-42/wave1/ScribeQuality.md
