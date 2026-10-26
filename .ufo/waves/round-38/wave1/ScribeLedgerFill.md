# ScribeLedgerFill — round-38 fill of the round-37 disposition section (calibration)

Seat `ScribeLedgerFill` (scribe, calibration). Item: draft `## Round-37 dispositions — filled (round 38)`
for `corpus/knowledge/considerthese-proposals-ledger.md`, byte-exact at
`.ufo/waves/round-38/wave1/ScribeLedgerFill.block.md`. Lane HEAD read while drafting
`700153593eb586c70a6499c8ca225ee4d673bc9b`; round-38 base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`
(claims freeze `9a10b02f…`, read, not edited). Write scope honoured: the deliverable and this receipt
are the only lane files written; every fixture and transcript lived under
`/fast/scratch/hyaku/kasegi-r38/ScribeLedgerFill/`, removed before yield. No mutating git outside two
`git init` fixtures whose `rev-parse --show-toplevel` was verified equal to the fixture dir; no tool
installed; no score move claimed; no `agent://all`; no swarm.

Result in one line: a 23-line / 5,365-byte appendix whose G7 limb is green on a base+block export
(`filled-heading=1,after-original=1,correction=1,rows=7,proposals=7/7 closed=1`) and red on every
mutant that empties it (no rows, six rows, no correction line, no filled heading, unnumbered rows),
with the empty-section range stated as measured (`:38`–`:40`), not as the brief's `L38-L39`.

## 1. Inputs read (read-only)

- `.ufo/waves/round-38/claims.json` — C1 checks (G1–G8), C2, `non_claim_frontier_items.considerthese`
  ("proposal 3 … mined into C1 G4/G6 + a QUALITY criterion; G7 fills the r37 ledger section").
- `corpus/knowledge/considerthese-proposals-ledger.md` at base and in the worktree (identical here:
  `git status --porcelain -- <path>` → 0 lines).
- `considerthese/2026-10-26.md` — the seven proposals this section rows.
- `corpus/lessons/round-37.md:262-286` — `## considerthese 2026-10-26 dispositions`, the status source for
  the "after round 37" column.
- `corpus/lessons/round-36.md:39` — the one-line dispositions that give the "before" column.
- `.ufo/waves/round-37/wave1/ScribeConsiderthese.md` §3–§5 — the round-37 18-row ledger draft (5 + 6 + 7
  rows) and its re-pin notes.
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-37/kasegi.md:25` (fleet, read-only) — the report's
  landed-change claim: "`corpus/knowledge/considerthese-proposals-ledger.md`: round-37 18-row disposition
  table + re-pin note (claims.json shorthand `corpus/considerthese-ledger.md` resolved to this tracked
  ledger — F3 resolution)."
- `corpus/lessons/round-37-verifier-spotcheck.md` §5 (D3, D-E) — the motive cited for row 3.
- `.ufo/waves/round-38/wave1/ExecRefChecker.py:684-720` and `:103-107` — the G7 contract this deliverable
  is measured against.
- `.ufo/waves/round-38/wave1-spec.json` items 31 and 34 — the same-round drafts that supply QUALITY R32/R33
  and the round-38 `## considerthese` section (their content is not quoted here; only the ids are cited).

## 2. Base state measured (the D-F defect)

```
$ git -C <lane> show a173b0c2:corpus/knowledge/considerthese-proposals-ledger.md | nl -ba | sed -n '34,43p'
  34
  35  Round-31 audit at append time, ... asserts no score move ...
  36
  37  ## Round-37 dispositions (appended 2026-10-26, R31 home)
  38
  39
  40
  41  ## Re-pin note (appended 2026-10-26)
  42
  43  As recorded by the round-37 lesson, the row at `:28` pinned score-gap.py at sha256 `855869…` ...
```
- `git show <base>:<ledger> | wc -l` → **43**; `sha256sum` → `fbcbfd193d17a244ca554e53cad835cdce3aee235df9c94097f62c625f2576b0`
  (6,564 bytes).
- Rows inside the round-37 section: `awk '/^## Round-37 dispositions/{f=1;next} /^## /{f=0} f && /^\|/' | wc -l`
  → **0**. Whole file `grep -c '^|'` → **16**, so a whole-file row count is green while this section is empty.
- Headings in the file: `:18 Limits`, `:22 Round-31 status flips`, `:37 Round-37 dispositions`, `:41 Re-pin note`.
- **Measured correction to the brief:** the brief said "L38-L39 blank"; at base there are **three** blank
  lines, `:38`, `:39` and `:40`, and the next heading is `:41`. The landed text states the measured span.

## 3. Deliverable

Path `.ufo/waves/round-38/wave1/ScribeLedgerFill.block.md` — **23 lines, 5,365 bytes, sha256
`48070a374bb06b40ce912dee0976c71b4a27f526a91d74e53149a9d25fd50520`**, byte-identical to the draft
(`cmp` → `BYTE_IDENTICAL`). Structure: heading `## Round-37 dispositions — filled (round 38)` (em dash
`e2 80 94`), the `Correction (round 38):` paragraph as the **first line after the heading** (line 2),
then one 5-column table (header + separator + 7 data rows), then a `Scope:` paragraph.

Landing form: `cat .ufo/waves/round-38/wave1/ScribeLedgerFill.block.md >> corpus/knowledge/considerthese-proposals-ledger.md`
(the base file's last byte is `\n`). Result measured in a base+block fixture: **66 lines**, **11,929
bytes** (6,564 + 5,365), sha256 `b498a5a3bdfab0841f66856b99216f99aef008e59d60e81601cab037c39921ad`; the
base 6,564 bytes are an exact prefix of the appended file (`head -c 6564 | cmp - <base>` →
`PREFIX_IDENTICAL`), i.e. append-only with zero deletions. Appending changes the file's own `recheck:`
reading: `density.py <file> --label proposal-ledger` mean dens **177.3 → 224.7**, exit 0 both sides.

Row statuses, with the source of each column:

| # | before | after r37 | after r38 |
|---|---|---|---|
| 1 | `open` (`round-36.md:39` item 1) | `open` (`round-37.md:268-270`) | `open` (unchanged) |
| 2 | `open` (`round-36.md:39` item 2; `SHONEN.md:164-165`) | `open` (`round-37.md:271`; `SHONEN.md:173-174`) | `open` (unchanged) |
| 3 | `mined → landed r36` (`QUALITY.md:263` R28; `r36-closure.sh:93-108`) | `mined → landed r36, hardened r37` (`round-37.md:272-273`) | `mined → landed r38` (C1 G4/G6 + R33) |
| 4 | `open` (`QUALITY.md:83` R14 only) | `open` (`round-37.md:274-276`, 7,266 files / 96.2 %, 95.1 % bytes) | `open` (unchanged; operator-owned) |
| 5 | `mined → landed r36` (`PROVINCE.md:77`) | `unchanged` (`round-37.md:277`) | `unchanged` (`PROVINCE.md:77` at base) |
| 6 | `open` (`round-36.md:39` item 6) | `open` (`round-37.md:278`) | `open` (unchanged) |
| 7 | `open` (`round-36.md:39` item 7) | `mined → landed r37` claimed, actually partial (`round-37.md:279-286`) | `mined → landed (partial)` (this section) |

Round-38 evidence measured for the rows that change or restate a number:

```
$ git -C <lane> ls-tree -r -l a173b0c2 | awk -F'\t' '{split($1,f," "); n++; bytes+=f[4]; if ($2 ~ /^\.ufo\//){u++; ub+=f[4]}} END{...}'
files=7348 bytes=121102259
.ufo_files=7065 ufo_bytes=115120172
pct_files=96.1 pct_bytes=95.1
$ git show a173b0c2:.gitattributes | grep -ci lfs
0
$ git show a173b0c2:SCORECARD.md | grep -c 'Threshold for 8'
0
$ git show a173b0c2:corpus/instruments/score-gap.py | grep -n 'THRESHOLD_RE'
76:THRESHOLD_RE = re.compile(r"Threshold for 5: [^|]*?claims\.")
$ git show a173b0c2:corpus/QUALITY.md | grep -nE '^\| R(28|31) \|' | cut -c1-40
263:| R28 | A round's claims rest on committed paths at the
278:| R31 | A considerthese proposal that a round touches ca
$ git show a173b0c2:corpus/QUALITY.md | sed -n '278p' | grep -o 'corpus/knowledge/considerthese-proposals-ledger.md'
corpus/knowledge/considerthese-proposals-ledger.md
$ git -C <lane> ls-tree -r --name-only a173b0c2 -- considerthese/ | wc -l
8                        # 2026-10-19.md … 2026-10-26.md, one file per day
$ git -C <lane> ls-tree -r --name-only a173b0c2 -- corpus/considerthese-ledger.md | wc -l
0                        # the 18-row path the r37 lesson names does not exist
$ git show a173b0c2:PROVINCE.md | sed -n '77p' | cut -c1-90
[r36 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F18 — CISA K...
```

## 4. Validation — the G7 limb of the round-38 checker, real code

Checker: `.ufo/waves/round-38/wave1/ExecRefChecker.py` (`suite-sha256=05dcafcedaaa6126eb531abc7030c4c1b846dc29340b4507e04d28352daeeb00`
in every run). Each fixture was `mktemp -d -p $S`, `git init -q`, toplevel verified equal to the fixture,
seeded from `git archive a173b0c2`, base committed, then the variant appended and committed.

| run | tree under test | G7 payload |
|---|---|---|
| control | real lane, `--export-ref a173b0c2` (no block) | `filled-heading=0,after-original=0,correction=0,rows=0,proposals=0/7 closed=0` |
| positive | base + this block | `filled-heading=1,after-original=1,correction=1,rows=7,proposals=7/7 closed=1` |
| m1 | block minus the `7.` row | `rows=6,proposals=6/7 closed=0` |
| m2 | block minus the `Correction (round 38)` line | `correction=0,rows=7 closed=0` |
| m3 | rows appended with the filled heading removed | `filled-heading=0,rows=0 closed=0` |
| m4 | numbering changed to `1 ` … `7 ` (no dot/paren) | `rows=0,proposals=0/7 closed=0` |
| m5 | numbering changed to `1)` … `7)` | `rows=7,proposals=7/7 closed=1` — the checker's `^([0-9]+)[.)]` accepts it (tolerance, not a defect of this block) |
| m6 | `Correction (round 37)` instead of `(round 38)` | `correction=0,closed=0` |
| m7 | heading + correction line only, no table | `correction=1,rows=0 closed=0` |

Other checks on the deliverable:

```
$ grep -c -e '⟨pending' -e '<fill>' -e 'filled by the L1' -e '<LANE_HASH>' -e '<r38-' block.md
0
$ grep -cE '\b(TBD|TODO)\b' block.md
0
$ awk -F'|' '/^\|/{print NF}' block.md | sort | uniq -c      # 5-column rows incl. header/separator
      9 7
$ awk '/^## Round-37 dispositions — filled/{f=1;next} /^## /{f=0} f && /^\|/' <appended file> | wc -l
9        # header + separator + 7 data rows
```
Fence walk over the block (CommonMark backtick/tilde state machine, run in Python over the draft):
`fence state at EOF of block: closed` — no triple fence is introduced, so the file's fence state stays
closed and the block cannot open a fence that swallows later text.

## 5. Calibration notes — where the brief and the bytes disagree

1. **`L38-L39` vs `:38`–`:40`.** The brief says the empty body is two lines; `nl -ba` and `cat -A` on the
   base blob show three blank lines (`:38`, `:39`, `:40`) before `## Re-pin note` at `:41`. The landed text
   states the measured span. This is the one place the deliverable intentionally departs from the brief's
   wording.
2. **"the round-37 report says a disposition table landed" is exact and quotable.** Fleet report `:25`
   names the 18-row table as landed in this file; the file's `:37` section has 0 rows. Both facts are in
   the landed correction.
3. **The 18-row ledger never landed as a file.** `corpus/considerthese-ledger.md` (r37 lesson `:264`,
   sha256 `7c232983…` in the round-37 receipt) is absent at base (`ls-tree` → 0). What exists is this
   file: the round-30 table (2026-10-25's six rows, `:11-16`), the round-31 flip block, the empty round-37
   heading and the re-pin note. After this append the file rows 13 of the 18 proposals the round-37 draft
   carried (6 + 7) and the 2026-10-24 five remain unrowed. Row 7's `(partial)` status says this; it does
   not silently close the round-37 overclaim.
4. **R33 is a same-round append, not a landed row at base.** `corpus/QUALITY.md` ends at R31 `:278` at base;
   R32/R33 are drafted by `ScribeQualityRows` this round and the `non_claim_frontier_items` entry in
   `claims.json` is the declaration that proposal 3 is mined into C1 G4/G6 plus that criterion. Row 3's
   "after round 38" status is true only when that QUALITY block lands in the same judged head; the
   dependency is stated in the evidence cell by naming it as the round-38 append.
5. **Rows 1, 2, 4, 6 say `open (unchanged)` on the strength of two things**, stated so a reader can check
   them: the base measurement, and the absence of any landing in the round-38 frozen claims. They are not
   a re-measurement at the judged head, which does not exist while the wave runs. No row claims a score
   move and no axis is touched.
6. **Two measurement slips, recorded rather than hidden.** (a) The first footprint attempt used
   `git ls-tree -r -l` with the wrong field index and printed `total bytes +inf` / blank `.ufo` counts; it
   was discarded and re-run with `-F'\t'` (numbers in §3). (b) A fixture `git diff --numstat HEAD~1 HEAD`
   failed (`bad revision 'HEAD~1'`) because that fixture's base tree was never committed; the append-only
   property is instead evidenced by the byte-prefix `cmp` in §3.
7. **The `Scope:` paragraph is deliberately inside the section.** It is landable text (it states the
   documentary limit, the append-only bar and the unrowed 2026-10-24 set), not receipt scaffolding; no
   validation table, heading or seat note from this receipt is in the deliverable.

## 6. Findings / conflicts (recorded, not resolved here)

- **F1 — D-F root cause is a landed draft, not a lost file.** The empty `:37` heading is what a landed
  section heading looks like when the section body (the 18-row ledger) was delivered as a *separate* new
  file that never landed, while the r37 report recorded the table as landed in this file. Both halves of
  that mismatch are still visible at base: empty body here, absent `corpus/considerthese-ledger.md` there.
- **F2 — the round-37 lesson's item-7 conflict is still unresolved in the bytes.** Lesson `:281-286`
  records that landing must make "R31 + ledger" cite one path; R31 already cites this file, the lesson
  still names the new file, and that new file does not exist. This section makes the dispositions
  reachable at the path R31 names; it does not amend the lesson (out of this seat's scope).
- **F3 — the round-37 density re-pin note is untouched.** `:41-43` records the score-gap.py re-pin owed
  under R19; nothing in this append edits or satisfies it.

## 7. Out of scope / limits

- Only the seven 2026-10-26 proposals are rowed. The 2026-10-24 five, the 2026-10-25 six (present only in
  the older 4-column table) and the 18-row three-date ledger stay outside this section.
- No lane instrument was run over the lane itself (no `r38-closure.sh`, no `recheck-audit.py`): the suite
  is not yet delivered and closure runs are the L1's. The only instrument executions are the checker runs
  in §4 against fixtures.
- Statuses cite committed lines at base `a173b0c2`; a line pin that moves in the same commit is not
  re-derived here.
- No claim about C1 or C2, no axis attribution, no score move. Calibration is the only axis this seat
  touched.

## 8. Tooling and scratch

- No tool installed or upgraded (nothing was needed beyond `git`, `awk`, `python3` already on the host).
- Scratch `/fast/scratch/hyaku/kasegi-r38/ScribeLedgerFill/` removed before yield; the only live traces are
  this receipt and the deliverable in `.ufo/waves/round-38/wave1/`.
