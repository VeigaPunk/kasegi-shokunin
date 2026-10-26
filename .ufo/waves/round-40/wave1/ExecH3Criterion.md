# ExecH3Criterion — round-40 wave 1 receipt

Seat: executor (leaf; no subagent, no task/agent/workpool call, no background job). Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` only. Base `a7af2ce63bce153757d39bf66b366a96caf30c13`;
current HEAD / claims-freeze `5e985b74075dd3813a63d7750966bf8abf693465`; frozen claims read at
`.ufo/waves/round-40/claims.json` (not edited). Route chain captured at spawn: fleet-root cwd → own
scratch `/fast/scratch/hyaku/kasegi-r40/ExecH3Criterion`; every read/write by absolute path; no git/jj
mutation anywhere (only `git rev-parse`, `git status`, `git log`, `git diff --no-index` — read-only).

Disk guard before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` →
`/fast/scratch/hyaku use% 26 free 597.4G`, `/tmp 3%`, `/var/tmp 35%` — green.

## Deliverable

| field | value |
|---|---|
| path | `.ufo/waves/round-40/wave1/ExecH3Criterion.txt` |
| bytes | 3807 |
| lines | 15 |
| sha256 | `84ad5eda9b9ab19cc378d25d966e02eaa3f4f0b2646f4e025f80e4ce307d83f6` |
| shape | round-40 block appended at EOF of `corpus/QUALITY.md`: `## Round-40 additions …` heading + R6-form paragraph (pre-append byte/line/digest figures and the not-edited row list) + the table header row (id / criterion / grounded in) + one criterion row `R37` |
| landing | `cat .ufo/waves/round-40/wave1/ExecH3Criterion.txt >> corpus/QUALITY.md` — append-only at end-of-file; no existing line is edited |

The bytes below are the exact append bytes: nothing else is in the file (no validation text, no receipt
scaffolding, no fences).

````text


## Round-40 additions — run-result quoting and receipt provenance (append-only)

R6 form: every line above keeps its number — this block is appended after line 309 (the file is
53420 bytes before it, `head -c 53420 corpus/QUALITY.md | sha256sum` →
`b379ed92eba012d8d4910526745abfe98ac76c9c538841b83df6799ebdd16fd5`; `wc -l` → 309), and R22 (line 226),
R23 (line 227), R26 (line 249), R27 (line 250), R28 (line 263), R29 (line 264), R30 (line 277), R31
(line 278), R32 (line 291), R33 (line 292), R34 (line 307), R35 (line 308) and R36 (line 309) are not
edited. The landing commit re-runs both commands immediately before writing: a byte figure measured at
draft time is a stale premise under R19 if an earlier append in the same round moved it.

| id | criterion | grounded in |
|---|---|---|
| R37 | A lane record that quotes a run result carries a committed transcript, or the quoting sentence says `report-only` (the R35 family, widened here from `closed=`/selftest quotes to every record that states a head, a tally or a gate outcome) — and a receipt is only the unedited tee of one observed run: its bytes are that invocation's stdout+stderr as written, with no hand-written header, no edited tally and no value the run did not print, and its `run-utc` is printed by the run itself at execution and never post-dates the commit that contains it. A record whose stated head or tally contradicts the committed receipt (M39-2's shape: five r38 lane records state the C1 run/selftest over the judged head where the receipt contradicts them, and the r39 records repeat the class, quoting `closed=8/8` and `failures=0` at the verification ref against the receipt's `closed=7/8` and `failures=1`) is corrected by an appended `Correction (round N)` block naming the receipt's final values, never by softening the earlier claim alone; a receipt whose `run-utc` post-dates its containing commit, or whose tally contradicts the same head's transcript, is a forged record: its result is discarded outright and never promoted, relabeled or counted. | M39-2 (`corpus/lessons/round-39.md:77`, § Mistakes) — routed as R5 by the round-39 verifier (`corpus/lessons/round-39-verifier-spotcheck.md:181-182`: "M39-2 has `captured-by: none` and no criterion. `grep -c M39-2 corpus/QUALITY.md` → 0, against the lane's own new R36. Add the criterion or state in the lesson why not"), with R2 (`:168-173`) supplying the receipt values the records miss and R1 (`:158-167`) minting its provenance limb: `5006097a:.ufo/waves/round-39/final-gates/all-gates.txt` records `run-utc=2026-10-26T21:35:00Z`, after its containing commit `2026-10-26T20:12:12Z`, with an 8/8 tally, while the L1's own run over the same head printed `closed=6/8 exit=1` and `selftest cases=8 failures=2`, and `make-receipt.sh` printed no `run-utc` line — so the committed header was not that script's output. Measured at the pre-append head (commit `5e985b74`, `git status --porcelain corpus/QUALITY.md` empty): `grep -c 'M39-2' corpus/QUALITY.md` → `0` and `grep -c 'R37' corpus/QUALITY.md` → `0`, while R35 (`:308`) already carries the transcript-or-`report-only` limb this row widens — the citation gap R5 names, with the id still unclaimed. M39-3 (`corpus/lessons/round-39.md:78`) records a quote with no committed transcript, the same class from the other direction. Round-40 limbs: H3 of `corpus/instruments/r40-closure.sh` greps this row for `M39-2`; H5 rejects a tampered or future-dated receipt as a graded selftest case; H7 re-runs the suite over the judged head and requires the receipt byte-identical, its `run-utc` printed by the run and not future-dated. At draft head that instrument is untracked (`ls corpus/instruments/r40-closure.sh` → missing), so those limbs are landing requirements, not draft measurements. |
````

## What it closes, and the rule it states

- **R5 closed** (round-39 verifier §5 R5: M39-2 has `captured-by: none` and no criterion). The row's id
  is `R37` — the next free id at the pre-append head (`grep -c 'R37' corpus/QUALITY.md` → `0`) — and it
  cites **M39-2** explicitly (token present in the row; H3's read).
- **Limb (a), R35 family:** a lane record that quotes a run result carries a committed transcript under
  the round's `final-gates/` in the judged head, or the quoting sentence says `report-only`; the row
  widens R35 from `closed=`/selftest quotes to every record that states a head, a tally or a gate
  outcome, and requires a record contradicting the committed receipt to be corrected by an appended
  `Correction (round N)` block **naming the receipt's final values**, not by softening the claim.
- **Limb (b), new R37 criterion:** a receipt is only the unedited tee of **one** observed run — its
  bytes are that invocation's stdout+stderr as written, with no hand-written header, no edited tally and
  no value the run did not print — and its `run-utc` is printed by the run itself at execution and never
  post-dates the commit that contains it. A receipt whose `run-utc` post-dates its containing commit, or
  whose tally contradicts the same head's transcript, is a forged record: discarded outright, never
  promoted, relabeled or counted.
- **Grounding** (verified in-lane below): `corpus/lessons/round-39-verifier-spotcheck.md` §5 **R5**
  (`:181-182`) routes the criterion, **R1** (`:158-167`) mints the provenance limb, **R2** (`:168-173`)
  supplies the receipt values the records miss; the **M39-2** row is `corpus/lessons/round-39.md:77`
  (`M39-3` at `:78` is the sibling quote-without-transcript row).

## Evidence — pre-append state of `corpus/QUALITY.md` (measured at HEAD)

````console
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git rev-parse HEAD
5e985b74075dd3813a63d7750966bf8abf693465
$ git status --porcelain corpus/QUALITY.md
                         (empty: the tracked path is clean at HEAD)
$ wc -l corpus/QUALITY.md ; wc -c corpus/QUALITY.md
309 corpus/QUALITY.md
53420 corpus/QUALITY.md
$ sha256sum corpus/QUALITY.md
b379ed92eba012d8d4910526745abfe98ac76c9c538841b83df6799ebdd16fd5  corpus/QUALITY.md
$ head -c 53420 corpus/QUALITY.md | sha256sum
b379ed92eba012d8d4910526745abfe98ac76c9c538841b83df6799ebdd16fd5  -
$ grep -n '^| R\(22\|23\|26\|27\|28\|29\|30\|31\|32\|33\|34\|35\|36\) ' corpus/QUALITY.md | cut -d: -f1 | tr '\n' ' '
226 227 249 250 263 264 277 278 291 292 307 308 309
$ grep -c 'M39-2' corpus/QUALITY.md
0
$ grep -c 'R37' corpus/QUALITY.md
0
$ grep -c '^| R35 ' corpus/QUALITY.md
1
$ ls corpus/instruments/r40-closure.sh
ls: cannot access 'corpus/instruments/r40-closure.sh': No such file or directory
````

The three figures carried in the block's R6 paragraph (309 lines / 53420 bytes / `b379ed92…`) were
re-measured immediately before this receipt was written and were unchanged, so they are true at write
time; under R19 the landing commit must re-run them (`head -c <n> | sha256sum` + `wc -l`), because any
round-40 append ahead of this block moves both.

## Evidence — grounding citations re-opened in-lane

````console
$ grep -n 'R1 — attempt-1\|R2 — round-39 records\|R5 — M39-2' corpus/lessons/round-39-verifier-spotcheck.md | cut -c1-60
158:- **R1 — attempt-1 receipt not mined.** `5006097a:.ufo
168:- **R2 — round-39 records still state C1 8/8 at Y.** `
181:- **R5 — M39-2 has `captured-by: none` and no criterio
$ grep -n 'M39-2\|M39-3' corpus/lessons/round-39.md | cut -c1-70
77:| M39-2 | evidence-record | five r38 lane records state the C1 run/
78:| M39-3 | evidence-record | r38 report quotes tip run f06148c6 (8/8
````

Facts the row quotes, each read from those anchors (not from memory): R1 — `run-utc=2026-10-26T21:35:00Z`
after its containing commit `2026-10-26T20:12:12Z`, an 8/8 tally, the L1's own scratch transcript over
`5006097a` printing `closed=6/8 exit=1` and `selftest cases=8 failures=2`, and `make-receipt.sh` printing
no `run-utc` line (so the committed header was not that script's run). R2 — the r39 records quote
`closed=8/8`/`failures=0` at Y against the committed receipt's `closed=7/8`/`failures=1`. R5 —
`grep -c M39-2 corpus/QUALITY.md` → 0 at the round-39 head: the gap this row closes.

## Evidence — dry landing in scratch (append-only proof)

`cp corpus/QUALITY.md $S/orig.md`; `cp $S/orig.md $S/q3.md`; `cat $S/ExecH3Criterion.txt >> $S/q3.md`:

````console
$ cmp <(head -c 53420 q3.md) /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/QUALITY.md
                         (silent) => prefix bytes identical; no existing line is touched
$ git diff --no-index --numstat orig.md q3.md
15	0	orig.md => q3.md
                         (15 added, 0 deleted; exit 1 as expected for differing files)
$ wc -l orig.md q3.md
309 orig.md
324 q3.md
$ grep -c '^```' orig.md q3.md
orig fences: 10  appended fences: 10
                         (fenced-code state unchanged: the block carries no fence)
$ grep -cE '^\| R[0-9]+ \|.*M39-2' q3.md
1                        (H3-shaped read: exactly one criterion row cites M39-2)
$ awk -F'|' 'NR==324{print "fields="NF}' q3.md
fields=5                 (3 cells + 2 boundary empties: the table row is intact)
$ awk 'NR>=322{p=gsub(/\|/,"|"); printf "%d pipes=%d len=%d\n", NR, p, length($0)}' q3.md
322 pipes=4 len=32       (header)
323 pipes=4 len=13       (separator)
324 pipes=4 len=2985     (R37 row: a pipe anywhere in a cell would make this 5+)
````

## Falsifier caught and fixed during the seat (recorded, not smoothed)

The first draft embedded two pipe-bearing greps (``grep -c '^| R37 '``, ``grep -c '^| R35 '``) inside
the grounded-in cell. Dry-landing it measured `pipes=6 len=2764` on the row line — a broken table cell
for any splitter. Draft 1: 15 lines, 3588 bytes, sha256
`841439a44b5539be801d8cb92b82356bcab6bf15e78257eda02bd0a14cbf4bd2`. Regenerated with the counts stated
pipe-free (`grep -c 'R37'`) and the R35 reference given without a pattern; the generator now asserts
`"|" not in criterion and "|" not in grounded` before writing, and the final row measures `pipes=4`. The
delivered `84ad5eda…` is the asserted pipe-free version.

## Risks / limits of this deliverable

- The row names the round-40 limbs **H3 / H5 / H7** of `corpus/instruments/r40-closure.sh` as landing
  requirements, not measurements: that instrument is absent at draft head (`ls` → No such file). If the
  built suite grades those checks under other ids, that one sentence becomes a stale premise; the frozen
  claims' H5/H7 wording is the authority and the ids match it as written.
- R6 figures (`309` / `53420` / `b379ed92…`) are draft-time by construction; the landing commit must
  re-run `head -c`/`wc -l` and refresh the paragraph if they moved — the block says this itself.
- Id coupling: `ExecMistakesDraft` refers to "the R37 QUALITY criterion"; this row is that R37 and the id
  is unclaimed at the pre-append head (`grep -c 'R37'` → 0), so no collision exists unless another seat
  mints R37 before landing.
- No writes outside the assigned paths: deliverable + this receipt in `.ufo/waves/round-40/wave1/`,
  scratch under `/fast/scratch/hyaku/kasegi-r40/ExecH3Criterion`.

## Scratch

`/fast/scratch/hyaku/kasegi-r40/ExecH3Criterion` created with `mkdir -p` and removed before yield
(`orig.md`, `q.md`, `q2.md`, `q3.md`, `block.py`, `mkreceipt.py` all inside it), so the H6
scratch-sibling check finds no `ExecH3Criterion` dir. Tooling installs: none this seat (no pacman, no
uv/npx/binary install).

VERDICT: DELIVERED — `ExecH3Criterion.txt` (3807 bytes, 15 lines, sha256 `84ad5eda9b9ab19cc378d25d966e02eaa3f4f0b2646f4e025f80e4ce307d83f6`) appends one `R37` criterion
row at EOF of `corpus/QUALITY.md`, citing M39-2 and stating the transcript-or-`report-only` rule plus the
receipt-as-unedited-tee / run-utc-provenance rule; dry landing adds 15 lines and deletes 0.
