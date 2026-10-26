# kasegi round 40 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

This closes lane-round kasegi 40. I did not author the round, I dispatched no lane work, and I ran no
lane-owned gate or instrument. I edited no lane-authored file. One read-only critic seat
(`KillRuleJudgeR40`, dispatched by this closure, not by the lane) gave a second reading of the C1 kill
rule. Inputs: report `.ufo/reports/round-40/kasegi.md` (fleet repo) and prompt
`.ufo/prompts/kasegi-round-40.md`. Lane base B = `a7af2ce63bce153757d39bf66b366a96caf30c13`. The judged
head J = J7 = `c7aea5ef97902f38289cbdc1cf267068876a62dd` (the receipt's `export-ref`). The verification
ref is Y = `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5` (`git diff --name-only J7 Y` →
`.ufo/waves/round-40/final-gates/all-gates.txt` only). The lane tip is Z =
`b01cbd50d514bb7f8e154b40e0e608be3e6cf217` (`git diff --name-only Y Z` → `LOG.md`, `SCORECARD.md`,
`SHONEN.md`). The frozen claims are in `.ufo/waves/round-40/claims.json`, frozen at `5e985b74`. All reads
below run over `git archive b01cbd50 | tar -x` and `git archive a7af2ce | tar -x` in closure scratch.

Driver digest, copied from the mutable `.ufo/watchdog.log` (lines 1568/1580/1581/1585 at read time):

```
2026-10-26T18:05:47-03:00 launch kasegi round=40 pgid=2886620 driver=hyaku-inline attempt=1
2026-10-26T18:57:11-03:00 lane-dead-no-report kasegi round=40; retry same round (hyaku-inline attempt=1: attempt 1 force-stopped at the request budget mid-round: wave-1 54/54 settled, J5 3074c767 committed with r40-closure.sh mint closed=10/10, Y receipt .ufo/waves/round-40/final-gates/all-gates.txt uncommitted, wave-2 falsify (35 seats) rendered but never dispatched, no report filed)
2026-10-26T18:57:13-03:00 launch kasegi round=40 pgid=2585990 driver=hyaku-inline attempt=2
2026-10-26T19:37:21-03:00 complete kasegi round=40; hyaku-inline attempt=2
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane, last | `git log --format='%an %H %cI' -- .ufo/reports/round-40/kasegi.md` | one commit, `kasegi-shokunin 28dfa1aec352ddb3eb9f5b08570a96039190d3d6`, 19:36:09-03:00. That is after lane tip Z (19:34:36) and before `complete` (19:37:21). Prompt commits `4041929b` (18:05:45) and `271b268b` (18:57:11) are by the same identity, each before its `launch` | conformant |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` on the report, plus the `- [` lines under it | `1`; four `[~]` lines for the four boxes; no `[x]` | conformant |
| Cited lane commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master` for `5e985b74`, `4766b9d`, `bfca9ae`, `8717b8b`, `94abbff`, `3074c767`, `8040db9b`, `c7aea5ef`, `d0fe34d3`, `b01cbd50`, `a7af2ce`, `8371e7a` | all resolve and all are ancestors (exit 0). `B..Z` is 10 commits, all by `kasegi-shokunin`, with 303 files, 37,900 insertions and 9 deletions (all 9 in `corpus/SOURCES.md` cells) | conformant |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state kasegi-shokunin`; `git status --porcelain` | `state branch=master local=b01cbd50… remote=b01cbd50… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | conformant |
| Prompt carries the template contract | read `.ufo/prompts/kasegi-round-40.md` (624 lines) | §1 MISSION/AXES binding (L3-L7); 1–3 claims including the lowest axis (L9-L27); §2b frontier step (L42); §3 L2 floor in one batched call (L80-L82); §4 report path, SHONEN, hash rule and marker rule (L99-L129); §5 commit, push scope and L0 (L131-L140); §6 hyaku addendum (L141) | conformant |
| Report is not a marker | the report names claims, commits and commands | real committed round work | status `ok` |
| Wave records | `jq '.taskCall.tasks\|length' wave{1,2}-dispatch.json`; result entries | build 54 = 54 (executor 18, reviewer 12, scout 11, scribe 6, critic 3, mutation-tester 2, connector 1, sentinel 1); falsify 35 = 35 (reviewer 12, scout 8, critic 7, mutation-tester 6, connector 1, sentinel 1); 89 total; every result entry has non-empty output | conformant |
| Receipt timestamp ≤ containing commit | `run-utc` of `all-gates.txt` vs the committer time of J7 and Y | `run-utc=2026-10-26T22:32:37Z`, which equals J7's committer instant (19:32:37-03:00, `time-basis=ref-commit`) and comes before Y (19:33:07) | conformant |
| Scratch at closure | `ls /fast/scratch/hyaku \| grep -i kasegi` | no `kasegi-r39*`/`kasegi-r40*` leftovers; the only kasegi entry is this closure's own dir (removed after this pass) | conformant |

Defects recorded (status-neutral; routed in §5): the attack-role tallies disagree (D5). Records quote a
selftest-at-Y tally that has no committed transcript, against the lane's own new criterion R37 (D2). The
round-40 lesson has a duplicated `## Gate` heading and a garbled census line (D4). The SKILL.md r40
registry row is split from its table header by a blank line (D6).

## 2. Claims — re-checked at Y/Z

### C1 — depth:verifiability (held 4): NOT VERIFIED (frozen kill rule fires on committed wave-2 fixtures; evidence-verified)

The frozen predicate (claims.json): at Y, `r40-closure.sh --export-ref Y` prints `closed=10/10 exit=0`
and `--selftest --export-ref Y` prints `selftest cases=10 failures=0`; the base and r39-head exports print
`closed<10/10 exit=1`; H1–H10 close the r39 routed defects R1–R7 plus G2/G6. The kill rule includes:
"a committed fixture shows a check passing while its defect is present". I did not run `r40-closure.sh`
(it is a lane gate; PROTOCOL §Gate standard, Closure consequence). Committed evidence read at Z:

- **Receipt.** `.ufo/waves/round-40/final-gates/all-gates.txt` (16 lines, `all-gates v4`):
  `export-ref=c7aea5ef…` (J7) and `suite-sha256=bdbd18a3…`, which equals
  `git show <rev>:corpus/instruments/r40-closure.sh | sha256sum` at 3074c76, 8040db9, c7aea5e and b01cbd50
  (the suite bytes did not change after J5). H1–H10 all read `closed=1`, the last line is
  `closed=10/10 exit=0`, and H8 records `base=3/10,base-exit=1,r39=2/10,r39-exit=1`. The run verdict and the
  negative controls therefore have a committed transcript.
- **Selftest.** The receipt holds no selftest line. The only committed graded tally is wave-2
  `RevC1Counters.md` R7 (`selftest cases=10 failures=0`), run over a scratch Y′ = J5 + the receipt, not the
  final Y. The suite bytes are identical, so this counts as capability evidence, but the Y-level
  `cases=10 failures=0` quoted in SCORECARD/LOG/SHONEN/the report has no transcript (D2).
- **Kill rule fires.** The lane's own committed wave-2 artifacts show checks passing while their defects
  are present:
  - H2: `wave2/RevC1Counters.defeats.txt` T2. Corrections naming `closed=7/80` / `failures=10` return
    `rc=0 payload=corrections=4,named=4,missing=0`; the predicate requires the final values
    `closed=7/8`, `failures=1`.
  - H3: T4. A fenced pseudo-row passes with `rc=0`.
  - H9: T7. A symlinked declaration outside the export passes.
  - H1: T13. A mention-only SKILL.md row passes.
  - H6: T14 (`kasegi_r40-stray` → `rc=0 strays=0`) and the committed fixture script
    `wave2/CritKillRule.h6-escapes.sh` (dot-dir, case, separator and nested escapes).
  - H8: `wave2/MutH6H10.md` §Defect D2. The pristine suite accepts a leaf-capped green base.

  The lesson's framing (`corpus/lessons/round-40.md` §Wave-2 falsification: "no live defect defeats a
  check", survivors routed to round 41) narrows the frozen clause after landing. The lane's own round-39
  standard (`SCORECARD.md` `## Round 39` C1 row: "Wave-2 G2 payload mutations also pass the instrument, so
  the frozen C1 pass claim is not admitted") treats this class as blocking. The independent critic seat
  reached the same ruling (FIRES; H6/H2/H3/H9/H1/H8).
- **Plain re-derivation of the r39 routed defects** (committed bytes, no lane gate):
  - R2 swept: `grep -c 'Correction (round 40)'` → `SCORECARD.md` 2, `LOG.md` 2, `SHONEN.md` 3,
    `corpus/lessons/round-39.md` 2 (base: 0 each). The SCORECARD text names `closed=7/8 exit=1` and
    `selftest cases=8 failures=1`.
  - R5: `grep -cE 'M39-2' corpus/QUALITY.md` 0 → 1, plus the R37 block.
  - R6: `corpus/lessons/round-39.md` +11/−0, with located quotes at L103-L105 for S056/S058/S059.
  - R1: `## Mistakes` M40-1 mines the attempt-1 receipt.
  - R3: the controls are now in the receipt's H8 transcript.
  - R4: no scratch leftover.

  These fixes are real, append-only work. But the claim is the frozen predicate, and the predicate's kill
  rule fires.

The report grades C1 "held; verified". That is an overclaim (calibration). The score stays 4 and no
axis moves down.

### C2 — coverage (7 → 8): VERIFIED (re-measured + evidence-verified)

Re-measured with the frozen counting commands over the extracted trees (base a7af2ce → tip b01cbd50;
Y→Z touches no corpus path):

| Counter | Command | Base | After | Reported |
|---|---|---|---|---|
| nine rows queued | frozen `awk … if(s=="queued")` over S016/17/19/20/21/22/23/24/25 | 9 | 0 | 0 |
| nine rows mined | same, `mined` | 0 | 7 (S016/17/19/20/21/23/25); 2 rejected (S022/S024) | 7 |
| entries citing the nine | `grep -rlE '^source: S0(16\|17\|19\|20\|21\|22\|23\|24\|25)' corpus/knowledge \| wc -l` | 0 | 7 | 7 |
| S06x rows | `grep -cE '^\|[[:space:]]*S06[0-9][[:space:]]*\|' corpus/SOURCES.md` | 0 | 3 | 3 |
| entries citing S06x | `grep -rlE '^source: S06[0-9]' corpus/knowledge \| wc -l` | 0 | 1 (`cyclonedx-analysis-subtree.md`) | 1 |
| frontier rows | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 22 | 23 | 23 |
| registry rows | CORPUS census row count | 59 | 62 | 62 |
| malformed / duplicate ids / enum / missing used-by | CORPUS census commands | 0 / 0 / — / — | 0 / 0 / none / none | — |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | W04 S028, W04 S029, ok, exit 0 (`census-before.txt`) | identical three lines, exit 0 (run by me) | exit 0 |

The frozen threshold is met (mined ≥ 4, and the entry count equals the mined count). The measure
43/43 = 1.000 follows from frontier 23 with 0 queued rows. Harness `entries=26 pass=26` and binding
`records=54 bound=54` are lane instruments, so I verified them from committed evidence only
(`wave2/CritRecordsConsistency.md:38`, `wave2/ConnPatterns.md:20,23`, `wave2/CritC2Fabricate.md:87`)
and did not re-run them. The SOURCES diff, compared column by column, changes only `status`/`used-by` on
the seven mined rows and `status`/`teaches` on S022/S024 (D7).

### Owned-axis harm check

`git diff a7af2ce b01cbd50 -- SCORECARD.md` is +16/−0: two `Correction (round 40)` lines plus the
`## Round 40 result` table. `git diff --numstat` shows zero deletions in `SKILL.md` (+7), `PROVINCE.md` (+3),
`corpus/QUALITY.md` (+14), `corpus/README.md` (+29), `LOG.md` (+15) and `SHONEN.md` (+16). The only deleted
lines in the round are 9 SOURCES cells. depth:density: SKILL.md is append-only (one registry block),
density.py is unchanged (receipt H10 `density=1`), and no move is claimed.

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability | unchanged | C1's frozen kill rule fires on committed wave-2 fixtures; the score is held at 4; the r39 R1–R7 tree fixes re-derive by plain reads, but the claim as frozen does not verify |
| coverage | improved | C2 re-measured 7 → 8 inputs: nine rows decided (7 mined), S060 mined, F23 admitted 22 → 23, census exit 0 |
| depth:density | unchanged | append-only SKILL.md; density instrument byte-identical; no move claimed |

## 3. Discernment spot-check (`corpus/lessons/round-40.md` `## Gate`, at Z)

Each source was re-opened live on 2026-10-26 (curl, HTTP status shown). Quotes were matched on
tag-stripped, whitespace-normalised page text.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S023 CISA CVD Program | admit (mined; `cisa-cvd-program-stages.md`) | `https://www.cisa.gov/resources-tools/programs/coordinated-vulnerability-disclosure-cvd-program`, HTTP 200, 75,587 B (same size as the lane fetch) | agree | The 19-word quote "CISA may disclose vulnerabilities as early as 45 days after the initial attempt to contact the vendor is made" is found once live and at capture L151. It is tier A (the coordinator's own page). The entry scopes the 45 days as the earliest disclosure for an unresponsive vendor, as the source says |
| S060 CycloneDX v1.7 analysis subtree (new row) | admit (mined; F23) | `https://cyclonedx.org/docs/1.7/json/`, HTTP 200, 6,419,901 B | agree | All three located quotes (L7 15 words, L15 18 words, L50 11 words; all ≤25) are found once each live. Capture `S060.txt` sha256 `d6862622…` matches the row and lesson. It closes the round-39 S059 flip ("scoped analysis-subtree capture"). It is a primary spec, so tier A is right |
| S016 Anthropic CVD / S017 Project Zero | admit (mined) | anthropic.com CVD page HTTP 200; projectzero.google 2025/07 HTTP 200 | agree | The quotes "Reports originating from AI-powered discovery are clearly labeled as such." (10 words) and the 20-word one-week transparency sentence are both found live |
| S062 OASIS CSAF v2.1 CSD 04 | reject | `https://docs.oasis-open.org/csaf/csaf/v2.1/` listing HTTP 200 (csd01–csd04, schema/, no `os/`); `…/v2.1/os/` HTTP 404; `csaf-v2.1.html` HTTP 200, 1,231,332 B, front matter "Committee Specification Draft 04", dated 21 October 2026 | agree | The flip has not fired: a draft is not a normative tier-A source while v2.0 (S055) is the only OASIS Standard |
| S061 CISA VEX Status Justifications (June 2022) | reject | PDF HTTP 200, 313,386 B, sha256 `9a4027c6…` (equals the row's recorded digest); `pdftotext` lists the five labels (L51-L55); S055 capture L485 cites this PDF | agree | The labels are already carried normatively by S055, which names this PDF as its reference, so a second row adds no grounded learner benefit this round. Note: the "no lane capture" half of the reason is the lane's own choice, since the PDF was reachable; the redundancy half carries the rejection |
| S022 CNA Rules v4.1.0 | reject (queued → rejected) | S030 row at Z: `supersedes S022 — use current 4.2.0 requirements`, mined, approved 2026-08-20 | agree | The supersession is recorded on both rows and the flip is concrete |

Newly written SOURCES row re-opened: S060 (above). Its ≤25-word quotes are located in the slice and
found live. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → W04 S028,
W04 S029, `ok`, exit 0, identical to `census-before.txt`.

The spot-check agrees with the gate on every sampled admit (S023, S060, S016, S017) and reject (S062,
S061, S022).

## 4. Trend verdicts

- **expansion: improved.** F23 is new frontier ground, admitted 22 → 23. `corpus/knowledge/cyclonedx-analysis-subtree.md`
  (`source: S060`, `ground: F23`) cites a mined row opened this round. There are 8 new admitted entries
  (knowledge files 51 → 59), each citing a mined row. This agrees with the lane.
- **quality: improved.** S060 (a captured, scoped, recheckable row) carries the ground of the uncaptured
  S059. S022/S024 are now marked as superseded by S030/S029. The false round-39 records (R2) now carry
  named corrections. The R6 Gate rows are completed. All eight new entries pass source-recheck per
  `wave2/CritSourceTruth.md`, and four sampled quotes re-located live. No admitted corpus entry failed its
  re-check. Caveat: the round's own claim records overstate C1 (D1/D2). That is a calibration defect
  routed below, not an admitted entry left false. This agrees with the lane.
- **discernment: improved.** This non-author spot-check agrees with the gate on ≥1 admit and ≥1 reject
  (§3: 4 admits, 3 rejects, all agree). The lane graded "unchanged" because no outside check had run when
  it filed; this closure supplies that check.

## 5. Routed defects (kasegi owes these next round)

- **D1 — C1 graded "verified" while its frozen kill rule fires.** `SCORECARD.md` `## Round 40 result`
  (`4 (held; verified)`), the `LOG.md` r40 entry and the report's C1 line state the claim verified. The
  frozen clause "a committed fixture shows a check passing while its defect is present" fires on
  `wave2/RevC1Counters.defeats.txt` T2/T4/T7/T13/T14, `wave2/CritKillRule.h6-escapes.sh` and
  `wave2/MutH6H10.md` D2. Append `Correction (round 41)` lines grading C1 not verified on the frozen
  counter.
- **D2 — Y-level selftest tally quoted without a transcript (violates the lane's own R37).** The
  SCORECARD/LOG/SHONEN r40 lines and the report quote `--selftest --export-ref Y` →
  `cases=10 failures=0`. The receipt has no selftest line, and the only committed graded tally is over
  scratch Y′ (J5 + receipt). `SHONEN.md` L219 says the receipt "records" the selftest values, but it does
  not. Either commit the transcript or mark those quotes `report-only`.
- **D3 — wave-2 instrument survivors (lane self-routed, carried).** H2 needs token-boundary matching. H3
  needs fence awareness. H9 needs symlink escape resolved under the export root. H6 misses
  case/separator, nested and dot-prefixed leftovers (and 4/8 selftest mutants). H1 accepts a mention-only
  row. H5 forgery detection is count-relative, and H7 does not isolate the payload-value comparison. H8's
  acceptance predicate is unkillable (MutH6H10 D2). Also the 7 kill-rule escape states (CritKillRule).
- **D4 — lesson hygiene.** `corpus/lessons/round-40.md` repeats `## Gate` (L29, L31). Census line L27
  reads "tier A +3?mined …" (wave 2 read it as a parenthetical but left it as written). Fix with an
  appended erratum, not a rewrite.
- **D5 — attack-role tally disagreement.** The report says attack roles were 25/35 in wave 2 and 42/89
  overall. `corpus/lessons/round-40.md` L9 says 33/35 = 94% and 50/89. The dispatch JSON shows reviewer 12
  + critic 7 + mutation-tester 6 = 25 in wave 2 and 17 + 25 = 42 overall. The lesson line is wrong.
- **D6 — SKILL.md registry table broken.** `SKILL.md` L1120 (separator) is followed by a blank L1121,
  then the `r40-closure.sh` row at L1122. A blank line ends a Markdown table, so the row renders outside
  its header. Repair with an appended, correctly formed row block.
- **D7 — S022/S024 `teaches` rewritten in place.** CORPUS.md §SOURCES rule 2 lets only
  `status`/`recheck`/`used-by` change in place, while the shape rule requires rejected rows to read
  `REJECTED: …; flip: …`. The queued → rejected transition cannot satisfy both. This is noted for the
  protocol lane (contract ambiguity) and is status-neutral for kasegi; the old→new change is logged in
  the lesson.

SHONEN boxes: all four are `[~]`. Box 2 (end-to-end domain task) still has no live domain hunt, so the
checklist is not fully checkable by a non-author from this round. Promotion is operator-owned.

## 6. Closure

Status `ok`. Claims: C1 not verified (kill rule fires), C2 verified. No axis harmed. **Not admitted**
(`rejected-honest-stop`: one claim does not verify, nothing harmed).
