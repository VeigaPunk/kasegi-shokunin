# ExecI1Blocks — round-41 I1 correction blocks (three records)

Seat: `ExecI1Blocks` (executor, leaf member; no subagent dispatch, no labrat).
Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — the only repo written to.
Base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` (40-char; the freeze-file literal
`5b29ea1439450b712581edf5f0bf98dfb262ab` is 38 chars and resolves to no git object —
`git rev-parse` on it → `fatal: ambiguous argument`, and the 40-char form resolves to
`5b29ea1439450b712581edf5f0f0bf98dfb262ab`, prefix `5b29ea1`, commit "round-40 verifier
spot-check (integrator, hyaku)"). Claims-freeze commit `fbba3d96cdf8d37c1ea41304a1ba35691329684b`
(verified: `git rev-parse` → same hash). Frozen claims read, not edited:
`.ufo/waves/round-41/claims.json` (C1 predicate + kill_rule, I1 limb).

Disk guard green before work: `/fast/scratch/hyaku` 25% used, 603.6G free; `/tmp` 3%, 125.1G free.

## 1. Deliverable

| path | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-41/wave1/ExecI1Blocks.blocks.txt` | 11 | 6385 | `9a92113601cadc1e5ac35ecc9b1339d133befffaabde07a7a07abc9a03e68f89` |

Contents: exactly three `## BLOCK <record>` sections in the order
`## BLOCK SCORECARD.md`, `## BLOCK LOG.md`, `## BLOCK SHONEN.md`, each followed by one
blank line and exactly one `Correction (round 41):` paragraph. The file is the
landable bytes only — no validation table, no notes, no headings other than the three
block markers the L1 splits on. The L1 lands each block as an append to the named
lane file (the round-40 precedent is `wave1/ExecH2Corrections.txt` → commit `bfca9ae`,
which appended `## BLOCK <file>` + the corrections to each of the three records).

**On the `## BLOCK` markers: keep them.** The round-40 precedent lands them, not
strips them — `git show bfca9ae -- SCORECARD.md` shows the landed hunk beginning
`+## BLOCK SCORECARD.md`, and the three records still carry their markers today
(`SCORECARD.md:1586`, `LOG.md:1721`, `SHONEN.md:205`, each the sole `## BLOCK` line in
its file). The markers are the round's own section-label convention for an
appended correction block, and they are what lets the L1 split one multi-record
deliverable into three lane files. Stripping them would land a section-less
paragraph where every round-40 and round-39 correction sits under a labelled
heading — so the block headings stay, matching `bfca9ae` exactly.

**One file, not two.** A sibling scribe seat also produced
`wave1/ScribeCorrections.full-blocks.txt` for the same three records. The two
deliverables are alternative sources for one landing, not additive: the L1 lands one.
Both now use the same `## BLOCK` organizer convention (the scribe realigned to it
after the round-40 precedent was shown to them), and both satisfy the same limbs:
run through this seat's I1 checker on the freeze tree, the sibling's file lands
`I1 payload=corrections=4,3,3,evidence=present,fences=closed closed=1` (exit 0) and
this file lands `I1 payload=corrections=1,1,1,evidence=present,fences=closed
closed=1` (exit 0) — each block independently names `RevC1Counters.defeats.txt`,
`CritKillRule.md`, `MutH6H10.md` and "not verified", so either can be landed without
the other. The differences are: this file carries exactly **one** `Correction
(round 41)` paragraph per record (3 lines, 11 lines total), where the sibling's
carries 4/3/3 across the three records — the round-40 landed precedent is one to
two paragraphs per record, and the I1 spec's own wording ("the `Correction (round
41)` line set … in SCORECARD.md, LOG.md and SHONEN.md") is satisfied by either
count; this file names the escape states as F1–F8 with the committed heading count
authoritative and no competing count literal; and it carries the Y40 receipt's
sha256 and line count, the `H1–H10 all closed=1` payload detail, and the R7 pointer
for the scratch-Y′ graded tally that is the only committed selftest evidence.

### Structural constraints, measured on the delivered bytes

```
$ cd .ufo/waves/round-41/wave1
$ wc -l -c ExecI1Blocks.blocks.txt
11 6385 ExecI1Blocks.blocks.txt
$ sha256sum ExecI1Blocks.blocks.txt
9a92113601cadc1e5ac35ecc9b1339d133befffaabde07a7a07abc9a03e68f89  ExecI1Blocks.blocks.txt
$ grep -c '^## BLOCK ' ExecI1Blocks.blocks.txt          # 3 block markers
3
$ grep -c '^Correction (round 41)' ExecI1Blocks.blocks.txt   # 3 line-anchored corrections
3
$ grep -c '^\s*```' ExecI1Blocks.blocks.txt             # 0 fence lines (I4)
0
$ grep -cE '^\s*([-*+] |[0-9]+\. )' ExecI1Blocks.blocks.txt   # 0 list items
0
```

Per block (parsed with `re.split(r'^(## BLOCK .+)$', text, flags=re.M)`):

| block | body paragraph lines | first line starts with `Correction (round 41):` | body chars |
|---|---:|---|---:|
| `## BLOCK SCORECARD.md` | 1 | yes | 2103 |
| `## BLOCK LOG.md` | 1 | yes | 2003 |
| `## BLOCK SHONEN.md` | 1 | yes | 2154 |

Each body is a single standalone paragraph on one physical line (≤5 lines per block,
one line), plain prose, no fences, no list items — so the `^Correction (round 41)`
line-anchored grep matches exactly one line per record and I4's fence-aware limb
cannot be satisfied by a fenced pseudo-row.

### Required token coverage (all three blocks, not just the union)

`grep -cF` per token over the delivered file: `not verified` 3, `NOT verified` 3,
`RevC1Counters.defeats.txt` 3, `CritKillRule.md` 3, `MutH6H10.md` 3,
`CritKillRule.h6-escapes.sh` 3, `closed=10/10 exit=0` 3, `d0fe34d3` 3,
`frozen counter` 3, `T2` 3, `T4` 3, `T7` 3, `T13` 3, `T14` 3, `F1` 3, `F8` 3.
Every block names every evidence token on its own, so no single block can carry the
evidence for the other two (proved by NC1/NC7 in §3).

### What each block grades, and on what evidence

All three blocks grade round-40 C1 **not verified** on the frozen counter (never
"qualified"), name the kill-rule firing evidence with paths, and state the final
round-40 receipt truth. Per record:

- **SCORECARD.md** — targets the `## Round 40 result` depth:verifiability row
  (`SCORECARD.md:1595`, "**4 (held; verified)**").
- **LOG.md** — targets the `## Round 40 (attempt 2, resumed)` C1 bullet
  (`LOG.md:1728`, "4 held, verified").
- **SHONEN.md** — targets box 3's round-40 evidence line (`SHONEN.md:215`, the
  "r40-closure.sh suite at Y `closed=10/10 exit=0` and graded `--selftest cases=10
  failures=0`" line).

Evidence named by every block:

1. `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` — T2 (substring-value defeat),
   T4 (fenced pseudo-row), T7 (symlinked declaration read outside the export),
   T13 (mention-only registry row), T14 (case/separator scratch escape). Verified in
   the committed bytes: `RevC1Counters.defeats.txt:9` (`== T2 H2 substring defeat`),
   `:13` (`== T4`), `:22` (`== T7`), `:46` (`== T13`), and the T14 block "D4 H6
   name-family case/separator evasion" (`kasegi_r40-stray` → `rc=0 payload=strays=0,read=ok`).
2. `.ufo/waves/round-40/wave2/CritKillRule.md` — the committed escape states, plus the
   committed reproducer `.ufo/waves/round-40/wave2/CritKillRule.h6-escapes.sh`
   (sha256 `2f154c7de7547f633bbb15d18cac94f47429ab8ef052b2febcc49f753080ec44`).
   **Count note (L1 freeze correction 2):** the committed file carries **eight** `### F`
   headings (F1–F8) — `git show fbba3d9:.ufo/waves/round-40/wave2/CritKillRule.md | grep -cE '^### F[0-9]+'`
   → `8` — while the file's own intro prose says "7 distinct escape states reproduced".
   The blocks follow the L1's authoritative correction
   (`.ufo/waves/round-41/wave1/CORRECTIONS-L1.md`): they name F1–F8 and state both
   numbers explicitly, so a reader sees the committed headings and the prose count
   without the blocks silently asserting either count alone.
3. `.ufo/waves/round-40/wave2/MutH6H10.md` D2 — "the pristine suite accepts a
   leaf-capped green base as its negative control" (`H8 payload=base=7/10,base-exit=1,
   r39=2/10,r39-exit=1 closed=1` on pristine bytes).
4. Final round-40 receipt truth — `.ufo/waves/round-40/final-gates/all-gates.txt` at
   Y40 `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5` (16 lines, sha256
   `7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b`):
   `closed=10/10 exit=0`, H1–H10 all `closed=1`, `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd`
   (J7), `time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`. The blocks state the
   receipt truth exactly as the round-40 verifier read it: **the suite ran green, but the
   frozen kill rule fires, so claim admission is withdrawn** — a green run is not claim
   admission.
5. D2 gap (round-40 verifier routed defect): the Y receipt carries **no** `selftest`
   line (verified: the 16 receipt lines are `all-gates v4`, `export-ref`, `suite-sha256`,
   `time-basis`, `run-utc`, H1–H10, `closed=10/10 exit=0` — no selftest row), so the
   round-40 `cases=10 failures=0` tally quoted beside it is report-only; the only
   committed graded tally is over scratch Y′ (`wave2/RevC1Counters.md` R7). The blocks
   withdraw it as evidence and point at round-41's I2 (the round-41 receipt tees both
   the run transcript and the graded selftest).

## 2. I1 checker spec (design — for the L1 to implement inside `corpus/instruments/r41-closure.sh`)

The I1 limb is **not** in the deliverable; it belongs in the instrument. Design, as
measured in §3:

```
I1 checks the `Correction (round 41)` line set of SCORECARD.md, LOG.md and SHONEN.md
in the export root. Three limbs, all must pass for closed=1:

 (1) FENCE-AWARE LINE-ANCHORED COUNT.  For each record R in
     {SCORECARD.md, LOG.md, SHONEN.md}: scan R with a CommonMark fence state machine
     (opening fence = 3+ backticks or 3+ tildes, up to 3 spaces of indent; closing
     fence = same character, length >= opener). Count lines matching
     /^Correction \(round 41\)/ that are OUTSIDE any fence. Require count >= 1 per
     record; a fenced pseudo-row does not count. If EOF is reached inside an open
     fence, fence state is not CLOSED -> closed=0 (I4).

 (2) EVIDENCE TOKENS.  The union of the three records' counted correction lines must
     contain each of, by fixed-string match (grep -F):
         RevC1Counters.defeats.txt
         CritKillRule.md
         MutH6H10.md
         not verified
     AND the same four tokens must each appear in every record's OWN counted lines
     (the per-record limb; without it a single block could carry the evidence for
     the other two — see NC7).

 (3) Missing record.  Any of the three records absent from the export root ->
     closed=0 (never a vacuous pass).

exit 0 only when closed=1; payload line:  I1 payload=corrections=<c1>,<c2>,<c3>,
evidence=present,fences=closed closed=1
```

Implementation used to validate this design (92 lines, sha256
`01eae5fee77f909a160ed976747c4b15f4876be7d99ca1b89d2fd4f50c120f0a`, run from scratch and
removed at yield): `awk` fence state machine over each record → per-record count and
per-record extracted lines; `grep -qF -- <token>` over the union and over each
record's own extracted lines. Note the `not verified` token is matched case-sensitively
as the lowercase form; the blocks carry both `not verified` and `NOT verified`, so a
case-insensitive implementation of the same limb also passes.

## 3. Evidence — commands actually run, with actual output

### 3.1 Freeze-tree dry run (zero matches today)

The freeze tree at `fbba3d96cdf8d37c1ea41304a1ba35691329684b` carries no round-41
correction line yet, so the I1 limb is red before landing and green after — the
after-state is reachable only by the claimed work.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ git rev-parse fbba3d96cdf8d37c1ea41304a1ba35691329684b
fbba3d96cdf8d37c1ea41304a1ba35691329684b
$ for f in SCORECARD.md LOG.md SHONEN.md; do
    printf '%s: %s\n' "$f" "$(git show fbba3d96cdf8d37c1ea41304a1ba35691329684b:$f | grep -c '^Correction (round 41)')"; done
SCORECARD.md: 0
LOG.md: 0
SHONEN.md: 0
```

The same tree extracted to scratch and run through the I1 checker:

```
$ bash $S/i1-check.sh $S/r4        # freeze tree, blocks NOT landed
I1 payload=corrections=0,0,0,missing=1,fences=closed closed=0
exit=1
```

### 3.2 Positive control (blocks landed on the freeze tree)

```
$ bash $S/i1-check.sh $S/r4        # after appending the three delivered blocks
I1 payload=corrections=1,1,1,evidence=present,fences=closed closed=1
exit=0
```

### 3.3 Negative controls (each must red)

```
$ bash $S/i1-check.sh $S/n1   # CritKillRule.md token dropped from SHONEN only
I1 payload=corrections=1,1,1,missing-tokens=SHONEN.md:CritKillRule.md,fences=closed closed=0   exit=1
$ bash $S/i1-check.sh $S/n2   # SCORECARD correction wrapped in a ``` fence (I4)
I1 payload=corrections=0,1,1,missing=1,fences=closed closed=0                                 exit=1
$ bash $S/i1-check.sh $S/n3   # fence left open at EOF (LOG.md)
I1 payload=corrections=1,1,1,fences=open closed=0                                             exit=1
$ bash $S/i1-check.sh $S/n4   # "not verified" phrase dropped from LOG only
I1 payload=corrections=1,1,1,missing-tokens=LOG.md:not verified,fences=closed closed=0         exit=1
$ bash $S/i1-check.sh $S/n5   # record missing entirely (SHONEN.md)
I1 payload=missing=SHONEN.md closed=0                                                        exit=1
$ bash $S/i1-check.sh $S/n6   # a record with zero corrections (block stripped from LOG.md)
I1 payload=corrections=1,0,1,missing=1,fences=closed closed=0                                 exit=1
$ bash $S/i1-check.sh $S/n7   # MutH6H10.md token dropped from SCORECARD only
I1 payload=corrections=1,1,1,missing-tokens=SCORECARD.md:MutH6H10.md,fences=closed closed=0    exit=1
```

NC7 is the one that justifies limb (2)'s per-record half: with a union-only token
check, NC7 would still be green (LOG and SHONEN still name `MutH6H10.md`), so the
union limb alone does not satisfy "**each** names the kill-rule firing evidence".

### 3.4 Committed-bytes facts the blocks assert (all re-read at the freeze commit)

```
$ git show d0fe34d3:.ufo/waves/round-40/final-gates/all-gates.txt | sha256sum
7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b  -
$ git show d0fe34d3:.ufo/waves/round-40/final-gates/all-gates.txt | wc -lc
     16    1062
$ git show fbba3d9:.ufo/waves/round-40/wave2/CritKillRule.md | grep -cE '^### F[0-9]+'
8
$ git show fbba3d9:.ufo/waves/round-40/wave2/CritKillRule.h6-escapes.sh | sha256sum
2f154c7de7547f633bbb15d18cac94f47429ab8ef052b2febcc49f753080ec44  -
$ git rev-parse 5b29ea1
5b29ea1439450b712581edf5f0f0bf98dfb262ab
$ git rev-parse 5b29ea1439450b712581edf5f0bf98dfb262ab     # the 38-char freeze literal
fatal: ambiguous argument '5b29ea1439450b712581edf5f0bf98dfb262ab': unknown revision or path not in the working tree.
```

## 4. Rationale — why these bytes

- **The claim being corrected is a claim about verification, so the correction must
  itself be verifiable.** Each block names the committed artifact path, the specific
  fixture identifier (T2/T4/T7/T13/T14, F1–F8, D2) and the exact receipt bytes it
  rests on, so a reader can re-derive the ruling with plain reads — no lane gate, no
  inference.
- **Grade, do not qualify.** The verifier's ruling is "NOT VERIFIED on the frozen
  counter"; the freeze kill rule's own firing clause is quoted in each block so the
  correction is self-explaining without the reader having the claim file open.
- **Receipt truth stated, then subordinated.** Each block first states the round-40
  receipt truth verbatim (`closed=10/10 exit=0`, the export-ref, `time-basis`, `run-utc`)
  and then says the truth does not buy admission while the kill rule fires. Reporting
  only the green number would repeat the round-40 overclaim; reporting only the red
  would be false.
- **Both corrections to the freeze are honoured.** The 38-char base literal is not
  cited anywhere in the blocks (the blocks concern the round-40 artifacts, which are
  named by path, not by the round-41 base), and the escape-state count is stated as
  "F1–F8 — eight committed headings; the file's own intro prose counts them
  differently, and the round-41 freeze correction … makes the committed headings
  authoritative", per `.ufo/waves/round-41/wave1/CORRECTIONS-L1.md` item 2. The
  committed heading count (8) is the only count asserted; the file's contradicting
  intro prose is disclosed rather than repeated as a second number, so no
  seven-count literal competes with the eight in the same record
  (`grep -cF '7 distinct escape states' ExecI1Blocks.blocks.txt` → `0`;
  `grep -coE '\bseven\b'` → `0`; `grep -cF 'F1'` → `3`, `grep -cF 'F8'` → `3`).
- **The receipt is cited by digest, not just by path.** Each block carries the Y40
  receipt's sha256 (`7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b`)
  and its line count (16 lines), so a reader can confirm it read the same bytes the
  round-40 verifier did rather than a re-render.
- **D2 is closed in the same breath.** The blocks withdraw the uncommitted
  `cases=10 failures=0` tally and point at I2, so the correction does not leave the
  round-40 records quoting a number the round-41 receipt never carried.
- **Prose, one paragraph, one line.** Round-40's landed blocks are single-line
  paragraphs; the same shape is used here so the `^Correction (round 41)` anchor and
  the I4 fence-aware limb behave identically against the round-40 and round-41 sets.

## 5. Conduct, hygiene, tooling

- **Writes (only):** `.ufo/waves/round-41/wave1/ExecI1Blocks.blocks.txt` (the
  deliverable) and `.ufo/waves/round-41/wave1/ExecI1Blocks.md` (this receipt). No
  lane file, no fleet file, no sibling lane repo, no source tree
  (`/home/vgpnk/Projects/shokuknow` untouched), no PATH directory, no
  `.ufo/state/`, no MANIFEST.json, no templates/, no scripts/, no SKILL.md /
  SCORECARD.md / LOG.md / SHONEN.md / PROVINCE.md / corpus/knowledge edit.
- **Git:** read-only only (`rev-parse`, `show`, `cat-file`, `log -S`, `status`,
  `diff --stat`, `archive` was not needed). No mutating git or jj command anywhere;
  no commit, add, push, checkout, reset, stash; no jj command. No fixture repo was
  built, so the `show-toplevel` assertion was not applicable.
- **Scratch:** `S=/fast/scratch/hyaku/kasegi-r41/ExecI1Blocks/`, created with
  `mkdir -p`, all work copies (freeze-tree extracts `r4`, `n1`–`n7`, the checker
  script) bound under it, `TMPDIR` for the checker's own `mktemp -d` was the inherited
  one under `/tmp` and cleaned by the script's own `trap`. The scratch directory is
  removed before yield (`rm -rf -- "$S"`), so no `kasegi-r41*` sibling survives from
  this seat.
- **Tooling:** nothing installed or upgraded (no `pacman`, no `uv tool install`, no
  `npx`, no binary download). `bash`, `awk`, `grep`, `git`, `python3` were already
  present. No network fetches.
- **Disk guard:** checked before work — `/fast/scratch/hyaku` 25% used, 603.6G free
  (green); no heavy pass was run without a green guard.

## 6. Risks and open items

- **Two deliverables exist for the same three records.** This seat's
  `ExecI1Blocks.blocks.txt` (11 lines / 6385 B / sha256 `9a921136…`, 1 correction
  paragraph per record) and the sibling scribe seat's
  `ScribeCorrections.full-blocks.txt` (18 lines / 5009 B / sha256 `ee3ffa76…`, 4/3/3
  paragraphs) both pass this seat's I1 checker on the freeze tree
  (`corrections=1,1,1` and `corrections=4,3,3`, both `evidence=present,fences=closed
  closed=1`, exit 0) and both use the same `## BLOCK` organizer convention. They are
  alternative sources for ONE landing: the L1 must land exactly one, or the records
  would carry duplicate `Correction (round 41)` paragraphs. The I1 spec wording is
  satisfied by either paragraph count; the round-40 landed precedent was 2/2/3.
- **The escape-state count is resolved in the live claims file.** The frozen
  predicate text still says "the seven committed CritKillRule escape states", but
  the live `.ufo/waves/round-41/claims.json` now carries two L1 errata that supersede
  it: `errata[0]` ("base hash literal" — the 38-char literal corrected to the
  40-char `5b29ea1439450b712581edf5f0f0bf98dfb262ab`, found by seat ScribeShonenLog)
  and `errata[1]` ("I11 escape-state count" — "the committed wave2/CritKillRule.md
  carries EIGHT '### F' headings (F1-F8; its own intro prose says 7) … I11 payload
  must read escapes=8 and red=8, naming F1-F8"). Verified in the live file: `base`
  resolves to the 40-char literal (5 occurrences), the 38-char form survives only
  inside the `errata[0]` quote (1 occurrence). The blocks already assert the eight
  committed headings and cite the freeze correction, so they are consistent with the
  erratum; the suite's I11 payload must read `escapes=8` / `red=8`.
- **Paragraph length.** Each block is one physical line of ~2000 characters, matching
  the round-40 landed blocks exactly. No seat requirement caps line length — only the
  ≤5-lines-per-block count, which is met at 1.
