# ScribeLesson — round 75 attempt 1 (scribe drafts, scratch-only)

Seat: `ScribeLesson` (leaf; no subagents; read-only against the lane; writes limited to this report and the seat's scratch dir, which is deleted before yield). Frozen claims: `.ufo/waves/round-75/claims.json` (C1 counter amendment, C2 F53 on S110). Base `f9cc05b56170946192a2dcafcc07e90ec611746c`; freeze `748dfb666280adfb1e249fcf6a265c5d9951eefb`; controls `c880047421a386a4a1731034a0a06df07ba23071`.

Nothing below is a measured after-value. Every `<...>` marker is a slot the integrator fills from its receipts; no C1 or C2 after-value is asserted here. Numbers that I did measure carry their command and exit code in `## Measured here`.

## Findings for L1 (integrator)

1. **V74-1 erratum target is not in the lane.** The round-74 report named by the dispatch, `.ufo/reports/round-74/kasegi.md`, is absent from the lane repo (`ls .ufo/reports/round-74/` exit 2). It lives at the fleet root, `/home/vgpnk/Projects/shokunin/.ufo/reports/round-74/kasegi.md` (present, exit 0). Its `entries=89` lines are 20, 46 and 85 (`grep -n 'entries=89' <file>`, 3 hits, exit 0). The erratum must be appended there by the integrator, since fleet-root tracked files are outside seat writes. This seat drafts the erratum text only.
2. **Lead line number moves at tip; the byte-identity claim holds.** The NDSS lead is base line 175 (`git show f9cc05b5:corpus/SOURCES.md | sed -n 175p`). Its line sha256 is `124b3a00b7923080293628af9531a1ae0d07a2341a0740b6f1f6ec8da2adb5a1` at base f9cc05b5 and at round-74 tip dca80cf5 (both exit 0). The S110 row goes after S109 at base line 121, so the lead moves to line 176 at tip by inference from the one-line insert (not measured here; verify with `grep -n 'NDSS Symposium 2023 paper on Fuzzilli' corpus/SOURCES.md` at tip). The line is byte-identical; its number is not. The retirement sentence states both numbers.
3. **Routed, not decided — R6 letter versus registry row insert.** QUALITY R6 says an edit to a line-cited file keeps every existing line at its number, with append-at-end or same-line suffix as the only forms. A mid-file registry row insert (rounds 71, 73, 74 and now S110) shifts every line below it. Round 71's S106 bullet (`corpus/SOURCES.md` line 267 at base f9cc05b5, `grep -n 'moves down by one'` exit 0) already acknowledged the shift. This round follows that practice. L1 should decide whether registry rows are R6-exempt or the table moves to end-of-file. Not resolved by this seat.
4. **R33 remains a duplicate and is not repaired.** `git show f9cc05b5:corpus/QUALITY.md | grep -cE '^\| R33 '` = 2 (exit 0); `... | grep -oE '^\| R[0-9]+ ' | sort | uniq -d` prints `| R33 ` (exit 0), the only duplicate id at base. R122 (drafted below) is the addition-time rule; it does not rewrite line 292 or 550.
5. **Gate-registry row for the census gate is absent at base.** `git show f9cc05b5:SKILL.md | grep -c 'recheck-cwd'` = 0 (exit 1). The sibling row exists: `git show f9cc05b5:SKILL.md | grep -c '^| recheck-audit.py '` = 1 (exit 0), at SKILL.md line 981 in the base file. The C1 landing commit should follow that row shape (`gate`, entry command, exit map, selftest command, pinned-value path, write scope, owner). This seat does not draft the row (outside its drafts list).
6. **Seat count.** `len(json.load(open('.ufo/waves/round-75/w1-spec.json'))['items'])` = 12 (exit 0); the dispatch `counts` field reads `{"spawn": 12, "resume": 0, "total": 12}` (exit 0). The lesson uses 12.

## Drafts

### D1 — `corpus/lessons/round-75.md` skeleton

<<<DRAFT D1 corpus/lessons/round-75.md
# Round 75 — lesson (kasegi, attempt 1)

Round: kasegi r75 attempt 1. Frozen claims `.ufo/waves/round-75/claims.json` (frozen 2026-11-05) — freeze commit `748dfb66` (full `748dfb666280adfb1e249fcf6a265c5d9951eefb`); base `f9cc05b5` (full `f9cc05b56170946192a2dcafcc07e90ec611746c`); controls commit `c8800474` (full `c880047421a386a4a1731034a0a06df07ba23071`). Implementation commits follow the freeze. Attack/build wave `w1`: one v1 wave of **12 seats** (count from `.ufo/waves/round-75/w1-spec.json` `items`; `len(items)` = 12 <CMD-SEATS> exit <X>). Dead seats: <DEAD-SEATS>. Report: <REPORT-PATH>.

Claims: C1 (`depth:verifiability`, counter amendment of `corpus/instruments/recheck-cwd-census.py`: explicit `restoration_only=N` bucket, `norecheck`- and `restoration_only`-aware RESULT gate, sixth selftest case; score held 4, nominal per QUALITY R58) and C2 (`coverage`, frontier F53 on S110, the NDSS Symposium 2023 Fuzzilli paper; one knowledge entry; score held 8). Non-claim round work is listed under `## Non-claim work`. Routed defects M74-6 and V74-1 are the C1 inputs (`claims.json` C1 `routed_defects`).

## Gate

Candidates considered this round:

- **S110 — NDSS Symposium 2023 paper "FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities" (Gross, Koch, Bernhard, Holz, Johns), `https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf`, DOI 10.14722/ndss.2023.24290 — <ADMITTED as F53 | PENDING>.** Admit stands only if capture, manifest and quote checks exit 0 at integration (B4, B5). One knowledge entry `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md`. Capture `corpus/source-snapshots/round-75/S110.txt`, sha256 `<SHA256>`, `<LINES>` lines, `<BYTES>` bytes, fetched `<FETCHED-UTC>`; capture command `<CAPTURE-CMD>` exit `<X>`. Located quotes: `<QUOTE-ANCHORS>` (each `<=25` words; `<WORDCOUNT-CMD>` = `<VALUE>`). Freeze-time fetch facts (HTTP 200, `application/pdf`, 918189 bytes) are the claim text, not re-measured in this lesson.
  - Distinctness screen (B8, narrowed per M74-7): the paper's design, comparison and evaluation ground vs S109 (tool README), S093 (PZ comparison post), S117 and S396 (revenger tool documentation). Per-hit verdicts from `grep -n 'ndss\|Fuzzilli' corpus/SOURCES.md`: `<VERDICT-PER-HIT>`. `grep -ril 'fuzzilli' ../revenger-shokunin/corpus`: `<VERDICT-REVENGER>` (expected: no NDSS paper row).
- **OSV.dev overview page, `https://google.github.io/osv.dev/api/` — REJECTED as a row this round; stays lead-only.** Reason: no capture or manifest is written this round, and `CORPUS.md` rule 1 admits a row only with its source captured in the round that writes it. Flip condition unchanged: a round that needs its rate-limit or response-size statements as admitted ground opens it with its own capture and manifest. Lead text remains in `corpus/SOURCES.md` `## Leads (unopened)`.
- **Project Zero's Fuzzilli-vs-BigSleep comparison (S093, F41) — held, not a candidate.** Already a row; the NDSS paper is a different document with its own statements.
- **Fuzzilli README (S109, F52) — not a candidate.** Admitted in round 74; untouched this round.
- **Assimilation package (`merge/kasegi/SOURCES.append.md`) — REJECTED for adoption this round.** 94 staged ids; 79 collide with the 109-row registry (`.ufo/waves/round-75/controls/assimilation-considerthese-r75.txt`: `reg-ids=109 staged-ids=94 collisions=79`). Adoption stays closed; the r70/r71 L0 questions remain the routing item.
- **considerthese sweep (`considerthese/2026-10-19.md` … `2026-10-26.md`) — verdict: <CONSIDERTHESE-VERDICT>.** Sweep receipt `.ufo/waves/round-75/controls/assimilation-considerthese-r75.txt` (its grep returns the file list and the `Self-improvement suggestions` headings). Reject line required by R119 if no proposal is admitted: `<CONSIDERTHESE-REJECT-LINE>`.

Admitted: S110 / F53 `<PENDING-OR-FINAL>`. Rejected: the OSV overview page as a row (reason above); the assimilation package (reason above); `<CONSIDERTHESE-REJECTS>`.

## Mistakes

| id | class | evidence pointer | captured-by | fix | able to fail |
|---|---|---|---|---|---|
| M75-1 | landing / attribution: the census gate `corpus/instruments/recheck-cwd-census.py` had no gate-registry row in its registry home at base `f9cc05b5` (`SKILL.md`); PROTOCOL.md § Gate standard, Registry clause, says closure grades no gate conformant until its row exists | `git show f9cc05b5:SKILL.md \| grep -c 'recheck-cwd'` = 0 (exit 1); sibling row present: `git show f9cc05b5:SKILL.md \| grep -c '^\| recheck-audit.py '` = 1 (exit 0); fleet-root `PROTOCOL.md` § Gate standard | none: no criterion checks that a gate file has a registry row | row added in the C1 landing commit `<LANDING-SHA>`, shaped as the `recheck-audit.py` row | `git show f9cc05b5:SKILL.md \| grep -c 'recheck-cwd'` = 0 (exit 1) at base; `git show <LANDING-SHA>:SKILL.md \| grep -c 'recheck-cwd'` must print at least 1 (exit 0) |
| M75-2 | number-drift / landing: census values printed at a mid-round tree (`entries=89`) were committed as the round-74 landed state; the tip carries 90 knowledge files, so the printed value is false at the revision it names (V74-1; the M74-2 number-drift class) | fleet-root `.ufo/reports/round-74/kasegi.md` lines 20, 46, 85 (`grep -n 'entries=89'`, 3 hits, exit 0); `corpus/lessons/round-74.md` line 69; `corpus/lessons/round-74-verifier-spotcheck.md` § 2 C1 and § 5 | none: no criterion binds a printed count to the revision that prints it | shape-clause drift expectation named in `.ufo/waves/round-75/claims.json` `notes` (freeze names its revision); R121; erratum below; census re-run at the final tip | `git ls-tree -r --name-only dca80cf5 corpus/knowledge \| grep -c '\.md$'` = 90 (exit 0) vs the printed `entries=89` at fleet report line 85: a comparison of the two prints `89 != 90` |

## Erratum (V74-1) — round-74 landed-state census values superseded

The round-74 values below were measured on the mid-round working tree (89 knowledge files). They are not the values at the round-74 tip `dca80cf5` (90 knowledge files: `git ls-tree -r --name-only dca80cf5 corpus/knowledge | grep -c '\.md$'` = 90, exit 0). The superseded lines are not edited (append-only; round-74 files untouched by this round).

- Fleet-root `.ufo/reports/round-74/kasegi.md`, line 85 (`## Landed-state checks`): "Census on the lane tree → conformant, exit 0; `entries=89` = `ls corpus/knowledge/*.md` = 89." — superseded.
- Same file, lines 20 and 46 (C1 implementation and "After" bullets): census `entries=89 …` — superseded; at `dca80cf5` the count is 90 by construction (`claims.json` `A2_lane_census`).
- `corpus/lessons/round-74.md` line 69 (§ Counters, C1 after): "entries 89 = `ls corpus/knowledge/*.md` 89" — superseded.

Corrected values, to be filled at the final round-75 tip: `<LANDED-CENSUS-LINE>` from `TMPDIR=<scratch> python3 <lane>/corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` run from a foreign cwd, exit `<X>`; `ls corpus/knowledge/*.md | wc -l` = `<KNOWLEDGE-COUNT>`. Declared drift (claims.json `notes`): entries 90 -> 91, exit0_foreign 68 -> 69, restoration_only stays 0. The fleet-root report erratum is appended by the integrator; this lesson carries the text of record.

## Routed defects (not closed by round 75)

- **RC-8 (operator decision, open).** Recheck values still run through `bash -c`. This round keeps one call site (`run_foreign`) before and after the amendment (kill rule (d)); `SentinelCounter` re-measures it: `<SENTINEL-COUNT>`.
- **RC-4, RC-5, RC-6, RC-7:** carried from round 73; not changed by round 75.
- **M74-6 (C1 scope sentence).** Closed by the C1 amendment only if A1-A4 pass; the frozen scope sentence is not reworded. `<C1-VERDICT-LINK>`.
- **M74-3 (R33 collision).** Open: `grep -cE '^\| R33 ' corpus/QUALITY.md` = 2 at base (exit 0) and `<TIP-R33-COUNT>` at tip. R122 states the rule; line 292 and line 550 are not repaired this round.
- **M74-7 (sibling-distinctness sentence).** Round-74 frozen text stays as written in `corpus/lessons/round-74.md`. Round 75's B8 screen is narrowed; the overbroad phrase is not re-asserted.
- **R6 letter versus registry row insert (new, routed to L1).** A mid-file registry row shifts line numbers of every later line in `corpus/SOURCES.md`, including the retired NDSS lead (base 175, tip `<TIP-LEAD-LINE>`). Decision belongs to L1 (see Findings item 3).
- **Assimilation (operator, open since r70/r71).** 79 of 94 staged ids collide; adoption stays closed.

## Registry changes (old -> new)

- **S110:** none -> mined (row added after S109 at `corpus/SOURCES.md` line 122, tip; opened 2026-11-05; recheck none -> 90d; used-by none -> `corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md`). No pre-existing row changed: `git diff f9cc05b5 -- corpus/SOURCES.md` removed lines = `<REMOVED-LINES>` (cmd `<DIFF-CMD>`, exit `<X>`; claim B2 requires 0).
- **Registry rows:** 109 -> 110 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; base 109 in `.ufo/waves/round-75/controls/c2-base-counters-r75.txt`).
- **NDSS lead** (`## Leads (unopened)`, base line 175, tip `<TIP-LEAD-LINE>`): kept byte-identical as history; sha256 of the line `124b3a00…adb5a1` at base and round-74 tip (measured); ground is now S110 / F53, recorded in the round-75 registry note (round-67 convention).
- **Knowledge files:** 90 -> 91 (`ls corpus/knowledge/*.md | wc -l`; base 90 measured). `corpus/instruments/knowledge-expected.txt`: 92 lines / 90 rows -> 93 / 91 (`LC_ALL=C sort -c` exit `<X>`; set-equal to knowledge files `<X>`).
- **Frontier rows:** 52 -> 53 (`corpus/README.md` `## Round-75 admission`; `PROVINCE.md` r75 line).
- **Capture records:** 88 -> 89 (`python3 corpus/instruments/capture-binding-check.py`; base `records=88 bound=88 unbound=0`).
- **Manifest:** new `corpus/source-snapshots/round-75/manifest.json` (`<QUOTE-COUNT>` quotes, S110 only).
- **QUALITY:** R121 and R122 added after line 560 (`corpus/QUALITY.md`). R33 count: `<TIP-R33-COUNT>` (base 2).

## Counters

- **C1 base, do-nothing control** (`.ufo/waves/round-75/controls/c1-donothing-r75.txt`, header cmd; exit 0): `RECHECK-CWD entries=90 noprefix=0 exit2_foreign=0 exit0_foreign=68 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`; base selftest `selftest cases=5 failures=0`, exit 0.
- **C1 red-before, restoration-only fixture** (`.ufo/waves/round-75/controls/c1-redbefore-restoration-r75.txt`): unamended counter gives `entries=2 noprefix=0 exit2_foreign=0 exit0_foreign=1 exit1_foreign=0 exit_other=0 norecheck=1`, `RECHECK-CWD-RESULT conformant`; the `restoration-ran` marker is absent.
- **C1 after:** A1 selftest `<A1-LINE>` exit `<X>`; A2 lane census `<A2-LINE>` exit `<X>` (at the C1 implementation revision entries = 90); A3 mutant kills M-A, M-B, M-C each `<KILL-LINE>` exit `<X>`; A4 parity `<A4-DELTA>`; exec surface `<BASH-C-COUNT>` (expect 1).
- **C2 base** (`.ufo/waves/round-75/controls/c2-base-counters-r75.txt`): `FRONTIER-CENSUS rows=52 admitted=52 closed=52 problem-rows=0 registry=109`; `entries=55 pass=55 exit=0`; `records=88 bound=88 unbound=0`, capture exit 0; knowledge 90; knowledge-expected 92 / 90 sort-clean; `sources-census.sh validate … kasegi` exit 0 with six inherited W04 warnings.
- **C2 after:** B1 `<B1-VALUE>`; B2 `<B2-VALUE>`; B3 `<B3-VALUE>`; B4 `<B4-VALUE>`; B5 `<B5-VALUE>`; B6 `FRONTIER-PASS F53 ids=S110`, `entries=56 pass=56 exit=<X>` `<B6-LINE>`; B7 `<B7-VALUE>`; B8 `<B8-VERDICTS>`.

## Sourced claim

C2 rests on S110, opened this round (2026-11-05, capture `corpus/source-snapshots/round-75/S110.txt`, sha256 `<SHA256>`). The knowledge entry cites S110 in its `source:` line and in each content claim. Anchor lines `<ANCHOR-LINES>` were re-read against the capture by `<REVIEWER-SEAT>`; `<WORDCOUNT-CMD>` = `<VALUE>`. The `<TEACHES-PLACEHOLDER>` wording is fixed in the entry's headings before commit.

## Non-claim work

- **V74-1 erratum:** text above; appended to the fleet-root report by the integrator after integration; round-74 lessons not edited.
- **QUALITY R121 and R122:** added (rows below the block in `corpus/QUALITY.md`).
- **SKILL.md gate-registry row for `recheck-cwd-census.py`:** added in the C1 landing commit `<LANDING-SHA>` (Gate standard registry clause; M75-1).
- **Assimilation:** none; closed (79 of 94 collide). Receipt committed.
- **considerthese:** sweep receipt committed; verdict in the Gate section above.

## Seats (wave w1, 12 seats)

Seat names from `.ufo/waves/round-75/w1-spec.json` `items` (12): ExecC1Amend, ExecC2Capture, ExecReplay, ScoutSurface, ScribeEntry, ScribeLesson, ConnectorSweep, ReviewC1, ReviewC2, CriticClaims, MutAuditC1, SentinelCounter. Reports: `<SEAT-REPORT-STATUS>`. Dead seats: `<DEAD-SEATS>`.

Attack share: `<ATTACK-SHARE>`.

## Verdicts (C1, C2)

Verdicts of record are pending. The integrator and the closure verifier write them after the landed-state checks. Nothing in this lesson records a verdict yet.

- C1: `<C1-VERDICT>` (kill rule: any of A1-A4 failing = NOT VERIFIED, honest stop).
- C2: `<C2-VERDICT>` (kill rule: any of B1-B8 failing = NOT VERIFIED, honest stop).

## Counting commands

- C1 after: `TMPDIR=<scratch> python3 corpus/instruments/recheck-cwd-census.py --selftest` (expect `selftest cases=6 failures=0`, exit 0); `cd <foreign-scratch> && TMPDIR=<scratch> python3 <lane>/corpus/instruments/recheck-cwd-census.py --root <lane> --lane <lane>` (expect `entries=90 … norecheck=0 restoration_only=0`, `RECHECK-CWD-RESULT conformant`, exit 0 at the C1 revision).
- C2 after: `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `cd <foreign-scratch> && python3 <lane>/corpus/instruments/source-recheck.py --manifest <lane>/corpus/source-snapshots/round-75/manifest.json --source S110`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` (expect 110); `ls corpus/knowledge/*.md | wc -l` (expect 91).
- Landed-state (V74-1 fix): the census command above at the final tip; `ls corpus/knowledge/*.md | wc -l` at the same revision.
<<<END D1

### D2 — `corpus/SOURCES.md` round-75 note bullet (appended at end of file; base file ends at line 270)

<<<DRAFT D2 corpus/SOURCES.md (append after the round-74 bullet)
- Round-75 S110 added (paper, scoped tier A, mined, opened 2026-11-05, recheck 90d, used-by corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md). Registry 109 -> 110; no pre-existing status, recheck, used-by, id or URL cell changed (`git diff f9cc05b5 -- corpus/SOURCES.md` removed lines = `<REMOVED-LINES>`, cmd `<DIFF-CMD>`, exit `<X>`). Anchor pinned to the round-75 capture corpus/source-snapshots/round-75/S110.txt (sha256 `<SHA256>`, `<LINES>` lines; quote anchors in corpus/source-snapshots/round-75/manifest.json). The NDSS 2023 Fuzzilli lead bullet is retired as opened: base line 175, tip line `<TIP-LEAD-LINE>` after the one-row insert; the line is kept byte-identical as history (sha256 `124b3a00b7923080293628af9531a1ae0d07a2341a0740b6f1f6ec8da2adb5a1` at base and at round-74 tip, both measured exit 0); its ground is now S110 / F53. The OSV overview page stays a lead (no row, no evidence).
<<<END D2

### D3 — S110 registry row (11 columns; anchor cell pins the round-75 capture)

<<<DRAFT D3 corpus/SOURCES.md (insert after the S109 row, base line 121)
| S110 | NDSS Symposium 2023, FUZZILLI: Fuzzing for JavaScript JIT Compiler Vulnerabilities (Samuel Gross, Simon Koch, Lukas Bernhard, Thorsten Holz, Martin Johns) — https://www.ndss-symposium.org/wp-content/uploads/2023/02/ndss2023_f290_paper.pdf (DOI 10.14722/ndss.2023.24290) | paper | A | the paper's own statements about its design, its comparison to other fuzzers and its evaluation results; not the Fuzzilli tool README (S109, F52), not Project Zero's Fuzzilli-vs-BigSleep comparison post (S093, F41), and not any live fuzzing | capture corpus/source-snapshots/round-75/S110.txt (sha256 `<SHA256>`, `<LINES>` lines, `<BYTES>` bytes, fetched `<FETCHED-UTC>`; quote anchors `<ANCHOR-LINES>` in corpus/source-snapshots/round-75/manifest.json) | `<TEACHES-PLACEHOLDER: one sentence in the paper's own terms, written after the quotes are located>` | mined | 2026-11-05 | 90d | corpus/knowledge/fuzzilli-ndss2023-jit-fuzzing-paper.md |
<<<END D3

### D4 — `corpus/QUALITY.md` R121 and R122 rows (R6 end-append after line 560)

<<<DRAFT D4 corpus/QUALITY.md (append after line 560 of the base file; line 560 is blank)
## Round-75 addition — shape-clause revision and criterion-id uniqueness (append-only)

R6 form: every earlier line keeps its number; this block is appended at end of file. R122 does not rewrite the R33 rows at lines 292 and 550; R120 (line 559) remains the supersession example.

| id | criterion | grounded in |
|---|---|---|
| R121 | A frozen shape clause (a predicate in a claims.json or freeze note that binds a count, value or listing to the repository) names the revision it was measured at, or names the drift expectation a later admission is declared to produce. A clause binding an absolute value to no named revision is a conformance defect of the freeze; a receipt that prints such a value is read against its own revision, not against the tip. | `corpus/lessons/round-74-verifier-spotcheck.md` § 2 C1 and § 5 V74-1 (census `entries=89` printed at a mid-round tree; the tip has 90 knowledge files, `git ls-tree -r --name-only dca80cf5 corpus/knowledge \| grep -c '\.md$'` = 90, exit 0); the number-drift class of M74-2 in `corpus/lessons/round-74.md` § Mistakes |
| R122 | A criterion id in `corpus/QUALITY.md` is unique at addition time: a new row takes an id that no row holds (`grep -cE '^\| R<id> ' corpus/QUALITY.md` = 0 before the addition). A collision is superseded by a new row that names the superseded row by line and states the supersession; the superseded row is not rewritten in place. R120 is the example: it supersedes the round-73 row R33 at line 550 and leaves the round-38 row at line 292 as held. | `corpus/lessons/round-74.md` § Mistakes M74-3 (`grep -cE '^\| R33 ' corpus/QUALITY.md` = 2, exit 0, at base f9cc05b5 and at the round-74 tip); R120 at line 559 |
<<<END D4

### D5 — Mistake rows and erratum

The Mistakes rows (M75-1, M75-2) and the V74-1 erratum block are inside D1 above, so the lesson skeleton carries them in one place. The erratum names the superseded lines verbatim (fleet-root report lines 20, 46, 85; `corpus/lessons/round-74.md` line 69).

## Measured here

Every number below was produced by the command shown. Exit codes are the shell's `$?` (`set -o pipefail` where a pipe is used). Nothing else in this report is measured.

| check | command (run from lane or stated cwd) | output | exit |
|---|---|---|---|
| freeze commit resolves | `git rev-parse --verify -q 748dfb66…51eefb^{commit}` | resolves | 0 |
| base is an ancestor of freeze | `git merge-base --is-ancestor f9cc05b5… 748dfb66…` | ancestor | 0 |
| base SKILL.md census row | `git show f9cc05b5:SKILL.md \| grep -c 'recheck-cwd'` | `0` | 1 |
| base SKILL.md audit sibling row | `git show f9cc05b5:SKILL.md \| grep -c '^\| recheck-audit.py '` | `1` | 0 |
| S110 unused at base | `git show f9cc05b5:corpus/SOURCES.md \| grep -c '^\| S110 '` | `0` | 1 |
| registry rows at base | `git show f9cc05b5:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `109` | 0 |
| NDSS lead line sha, base | `git show f9cc05b5:corpus/SOURCES.md \| sed -n 175p \| sha256sum` | `124b3a00…adb5a1` | 0 |
| NDSS lead line sha, tip dca80cf5 | `git show dca80cf5:corpus/SOURCES.md \| sed -n 175p \| sha256sum` | `124b3a00…adb5a1` (identical) | 0 |
| SOURCES.md base line count | `git show f9cc05b5:corpus/SOURCES.md \| wc -l` | `270` | 0 |
| R33 rows at base | `git show f9cc05b5:corpus/QUALITY.md \| grep -cE '^\| R33 '` | `2` | 0 |
| duplicate criterion ids at base | `git show f9cc05b5:corpus/QUALITY.md \| grep -oE '^\| R[0-9]+ ' \| sort \| uniq -d` | `\| R33 ` (only duplicate) | 0 |
| R121 / R122 at base | `git show f9cc05b5:corpus/QUALITY.md \| grep -cE '^\| R12[12] '` | `0` | 1 |
| QUALITY.md base line count | `git show f9cc05b5:corpus/QUALITY.md \| wc -l` | `560` | 0 |
| knowledge files, base | `git ls-tree -r --name-only f9cc05b5 corpus/knowledge \| grep -c '\.md$'` | `90` | 0 |
| knowledge files, round-74 tip | `git ls-tree -r --name-only dca80cf5 corpus/knowledge \| grep -c '\.md$'` | `90` | 0 |
| lane has round-74 report | `ls .ufo/reports/round-74/` (lane) | no such directory | 2 |
| fleet-root round-74 report | `grep -n 'entries=89' /home/vgpnk/Projects/shokunin/.ufo/reports/round-74/kasegi.md` | lines 20, 46, 85 | 0 |
| round-74 lesson counter line | `grep -n 'entries 89' corpus/lessons/round-74.md` | line 69 | 0 |
| seat count | `python3 -c "…len(json.load(open('.ufo/waves/round-75/w1-spec.json'))['items'])"` | `12` | 0 |
| dispatch counts | `python3 -c "…json.load(…w1-dispatch.json)['counts']"` | `{"spawn": 12, "resume": 0, "total": 12}` | 0 |
| round-74 SOURCES bullet present | `grep -c '^- Round-74 S109' corpus/SOURCES.md` | `1` | 0 |
| SOURCES.md final byte | `tail -c1 corpus/SOURCES.md \| od -c` | newline (append point = after line 270) | 0 |
| assimilation collision receipt | read `.ufo/waves/round-75/controls/assimilation-considerthese-r75.txt` | `reg-ids=109 staged-ids=94 collisions=79` | 0 (cat) |
| C1 do-nothing receipt | read `.ufo/waves/round-75/controls/c1-donothing-r75.txt` | `entries=90 … norecheck=0`, conformant, `selftest cases=5 failures=0` | 0 (cat) |
| C1 red-before receipt | read `.ufo/waves/round-75/controls/c1-redbefore-restoration-r75.txt` | `entries=2 … norecheck=1`, conformant; marker absent | 0 (cat) |
| C2 base receipt | read `.ufo/waves/round-75/controls/c2-base-counters-r75.txt` | rows 52, entries 55/55, records 88, registry 109, knowledge 90, knowledge-expected 92/90 | 0 (cat) |

Not run by this seat: no lane instrument (census, frontier, capture, source-recheck) was executed; the C1/C2 after-values are placeholders, and the base values above are read from committed receipts. No tool was installed or upgraded. No subagent was spawned.

## Self-check of drafts (run before yield; see the validator line in the scratch log)

- S110 row (D3): 11 cells, no unescaped `|` inside any cell.
- M75-1 and M75-2 rows: 6 cells each; pipes inside code are escaped as `\|`.
- R121 and R122 rows (D4): 3 cells each.
