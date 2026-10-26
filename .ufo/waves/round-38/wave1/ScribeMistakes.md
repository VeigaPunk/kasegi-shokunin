# ScribeMistakes — round 38 receipt

seat: ScribeMistakes (scribe, leaf) · round 38 · judged on depth:verifiability
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin · lane head at work: 700153593eb586c70a6499c8ca225ee4d673bc9b
base a173b0c2b98c5ae39599fa9be76027fbbead0b9e · claims freeze 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b
claims read: `.ufo/waves/round-38/claims.json` (not edited). Driver: read-only git + grep only; no lane file written
except this receipt and the deliverable beside it.

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-38/wave1/ScribeMistakes.block.md`

    bytes   8863
    lines   17   (17 newline-terminated)
    sha256  3d0752ac27e46122e238f0d678a2664224998960ce64a4bb4ca1d3df4326ee5f
    shape   `## Mistakes` + blank + 6-line intro + blank + header + separator + 6 data rows
    columns 7 data cells in every row (id, class, event, evidence, captured-by, fix, able to fail)
    fences  0 (no line begins with a three-backtick code fence)
    ids     M38-1 .. M38-6, in the order the item names them

Landable bytes only: no validation table, no property table, no seat notes. The block is the whole
`## Mistakes` section for `corpus/lessons/round-38.md` (absent at head: `ls corpus/lessons/round-38.md`
→ `No such file or directory`, exit 2). Splice it unmodified.

Two deliberate byte choices, both load-bearing for this round's G3:

- Placeholder tokens are **named in prose, never reproduced**. The block contains none of the widened
  vocabulary the round's G3 hunts (`pending:` inside the guillemet marker, the fill token, the lane-hash
  token, the L1-fill phrase, angle-bracket templates such as the r37 final-head spelling), so the lesson
  cannot satisfy its own vocabulary check. A mechanical sweep over the deliverable returned
  `forbidden tokens present: []`.
- No angle-bracket template anywhere; declared-block facts are given as plain numbers (2 lines / 295 B,
  27 lines / 2947 B) rather than reproducing a declaration syntax.

## 2. Measurements (commands and their outputs)

All read-only; every revision is named in the command. `L` is the lane repo.

### 2.1 D-A — scaffolding paste, measured at the r37 judged head and at this round's base

    git -C $L show 2387dcf6:PROVINCE.md | wc -l                                  -> 152
    git -C $L show b56a41680cefd391868c1c370dc063c69d827e7d:PROVINCE.md | wc -l  -> 78
    git -C $L show 2387dcf6:corpus/README.md | wc -l                             -> 454
    git -C $L show b56a41680cefd391868c1c370dc063c69d827e7d:corpus/README.md | wc -l -> 398
    git -C $L show 2387dcf6:PROVINCE.md | grep -nE '^## [0-9]+\. (Deliverable|Validation)'
      -> 90:## 3. Deliverable B — `corpus/README.md` end-of-file block
      -> 134:## 4. Validation on a scratch mirror (append, not edit)
    git -C $L show 2387dcf6:PROVINCE.md | grep -nE '^(`){3}'   -> 81, 96, 124  (3 fences, odd)
    git -C $L show 2387dcf6:corpus/README.md | grep -nE '^(`){3}' -> 426       (1 fence, odd)
    git -C $L show 2387dcf6:corpus/README.md | grep -c '^## Round-37 admission' -> 0
    git -C $L show 2387dcf6:corpus/README.md | grep -cF '## Round-37 admission' -> 1
      -> the single fixed-string hit is `:448`, a pasted table row that itself asserts the anchored
         check reads `1`; measured anchored value on the same bytes is `0`.
    declared blocks (.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md)
      -> :56  sha256 cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545, bytes/lines 295/2
      -> :99  sha256 2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b, bytes/lines 2947/27
    base-state redness at a173b0c2b98c5ae39599fa9be76027fbbead0b9e:
      grep -cF 'Correction (round 38)' PROVINCE.md -> 0 ; corpus/README.md -> 0
      PROVINCE.md fences 81/96/124 (3, odd) ; corpus/README.md fence :426 (1, odd)
      receipt-section headings in PROVINCE.md -> 2 ; 'Validation on a scratch mirror' in README -> 1
      declared-blocks.txt under .ufo/waves/round-38 -> 0 tracked ; r38-closure.sh -> 0 tracked

Scribe-discipline note: my first read of the README heading used a fixed string and returned `1`, which
would have contradicted the routed defect. The anchored read returns `0`; the `1` is the pasted check's
own text. The block states the anchored measurement and cites the contradiction as evidence.

### 2.2 D-B — three heads named final

    all-gates.txt at 2387dcf6, :2   -> export-ref=9492c776724e737caf5815fabc98e59ea04830df
    SCORECARD.md at 2387dcf6, :1505 -> --export-ref aa88877bf921d952137817b91ca76234b206da65
    SHONEN.md at 2387dcf6, :172,176 -> final lane head aa88877bf921d952137817b91ca76234b206da65
    report .ufo/reports/round-37/kasegi.md:3,8,37 -> final lane head 2387dcf6ccfefcfb703783387b9aade8fc82abfa
    git merge-base --is-ancestor 9492c776 aa88877b -> 0 ; aa88877b 2387dcf6 -> 0 ; 9492c776 2387dcf6 -> 0
    stamps: 9492c776 14:59:49−03:00 ; aa88877b 15:00:25−03:00 ; 2387dcf6 15:01:28−03:00
    git diff --name-only 9492c776 2387dcf6
      -> .ufo/waves/round-37/final-gates/all-gates.txt, SCORECARD.md, SHONEN.md

### 2.3 D-C — pending markers in the round-37 lesson

    grep -c 'pending:' corpus/lessons/round-37.md -> 7
    lines 10, 90, 95, 216, 265, 300, 320
    sed -n '83,87p' -> ":85 … but is **not landed**."   (the entry is committed in the same head)
    suite scope, corpus/instruments/r37-closure.sh:59-64 (at 2387dcf6):
      "SCORECARD.md in the export carries 0 L1-fill-phrase lines and 0 lane-hash-marker lines"
      (paraphrased here without the two literal spellings, for the same G3 reason as §1)
      implementation `check_e1()` reads SCORECARD.md only, with both literals assembled from printf so
      the instrument does not contain the tokens it hunts. SHONEN.md and the lesson are never opened.
    committed payload at that head, all-gates.txt:8 -> E1 payload=placeholders=0,lane-hash-markers=0,
      round37-section=1,round37-final-lane-commits=1,bound=1 closed=1

The token-free spelling `pending:` was used in the receipt's own commands so this file stays outside the
vocabulary G3 widens; the equivalence is mechanical (all 7 markers are `pending:` inside the marker
brackets).

### 2.4 D3 — closure order

    git log -1 --format='%cI' 83975acc -> 2026-10-26T15:03:15-03:00
    git show --stat 83975acc           -> .ufo/waves/round-37/kasegi-r37-build-results.json | 392 +++
                                          1 file changed, 392 insertions(+)
    .ufo/watchdog.log:1537             -> 2026-10-26T15:02:47-03:00 complete kasegi round=37
    delta 28 s. git cat-file -e 2387dcf6:.ufo/waves/round-37/kasegi-r37-build-results.json -> exit 128
                git cat-file -e 83975acc:.ufo/waves/round-37/kasegi-r37-build-results.json  -> exit 0
    results file seat count: 64 (json length)

### 2.5 D-F — empty ledger section

    grep -n '^## Round-37 dispositions' corpus/knowledge/considerthese-proposals-ledger.md
      -> 37:## Round-37 dispositions (appended 2026-10-26, R31 home)
    next heading at :41 (`## Re-pin note (appended 2026-10-26)`); rows between :37 and :41 -> 0
    section span 7 lines. Report claim: .ufo/reports/round-37/kasegi.md:25
      -> "round-37 18-row disposition table + re-pin note"

### 2.6 D-E — scratch leftover

    r37 quiescence limb (corpus/instruments/r37-closure.sh, `check_e9`, at 2387dcf6):
      find "$sroot" -mindepth 1 -maxdepth 1 -type d      -> directories only
    verifier pointer: corpus/lessons/round-37-verifier-spotcheck.md §5 D-E
      (`/fast/scratch/hyaku/kasegi-r37/build-spec.py` remained at closure; "no seat dirs, so E9 is unaffected")
    measured this round (2026-10-26): `ls /fast/scratch/hyaku/kasegi-r37` -> No such file or directory
    so the red in M38-6 is the r37 observation; the row says so rather than implying a live leftover.

## 3. Attribution decisions (where I did not simply copy the item wording)

- **M38-1 captured-by = none.** Verified, not assumed: the r37 placeholder limb reads SCORECARD.md and
  two fixed spellings, so PROVINCE.md and corpus/README.md were never in scope; no r37 check compared an
  append with its declared block (declarations lived in the seat receipt at
  `wave1/ScribeFrontierAmendments.md:56,99`, which nothing read).
- **M38-2 captured-by = R19 for figures only** (the item wrote "R19?"). R19 binds a literal to the command
  that prints it; D-B is a label bound to no head at all. r37 E1 does check that hashes named inside the
  SCORECARD round-37 block resolve and are ancestors — it passed while three heads were called final.
- **M38-3 captured-by = the E1 placeholder limb, too narrow on both axes** — file set (SCORECARD.md only)
  and vocabulary (two spellings). Recorded with both, since widening only the vocabulary would still have
  missed the lesson and SHONEN.md.
- **M38-4 fix cites G4 + QUALITY R33**, because R33's drafted text is exactly the closure-order rule
  (judged head carries every artifact; report filed after the last lane commit). The pre-report direction
  was already fixed at r36 (M36-1); this row covers the post-report direction that no check read.
- **M38-5 and M38-6** follow the item's fixes unchanged; D-F's claim is quoted with its file:line so the
  contradiction is checkable rather than asserted.

## 4. Limits and dependencies (for the L1)

- **R32 and R33 do not exist in `corpus/QUALITY.md` at lane head 7001535** — the last row there is R31
  (`grep -nE '^\| R3[2-9] ' corpus/QUALITY.md` → no match). Both are drafted this round by seat
  ScribeQualityRows (R32 grounded in M38-1, R33 in M38-2/M38-4). If either row is not landed, the fix
  cell naming it must be corrected before this lesson lands; the grounding direction (row → this lesson)
  is the same shape QUALITY R30 uses for M37-2.
- The G-check names (G1..G8) are taken from the frozen claims. No round-38 suite is committed at this
  head (`.ufo/waves/round-38/` holds no `r38-closure.sh`, no `declared-blocks.txt`), so every "able to
  fail" cell names the limb and the r37/base red it must reproduce; **this seat ran none of them**, and
  the block's intro says so.
- Base redness for G1 was measured on `a173b0c2` (PROVINCE.md 152 lines, 2 receipt sections, 3 fences,
  0 correction lines; README 1 fence, 0 anchored heading). It is not a run of `r38-closure.sh`.
- G2's refinement diff for this round is the receipt file alone per the judged-head rule in claims.json;
  the block states the rule, not a hash, because a lane file cannot name the head that contains it.
- Nothing in this receipt claims a knowledge-entry or coverage measurement; C2 is out of this item's scope.

## 5. Scratch and tooling

- No scratch directory was created: no export, work copy or mutation was needed for this item, so nothing
  was bound to a scratch TMPDIR. Verified immediately before yielding:
  `ls -d /fast/scratch/hyaku/kasegi-r38/ScribeMistakes` → `No such file or directory` (exit 2). Nothing
  of mine remains under `/fast/scratch/hyaku/`.
- No tool installed or upgraded; no pacman invocation; no network fetch (no `curl` was run — every input
  was a committed lane file or a read-only fleet log/report).
- Mutating git: none. The only git subcommands used were `show`, `cat-file`, `ls-tree`,
  `merge-base --is-ancestor`, `log`, `diff`, `rev-parse`; plus `grep`, `awk`, `sed`, `wc`, `ls`, `sha256sum`
  and one `python3` shape check over the deliverable.
- Writes: this receipt and `ScribeMistakes.block.md`, both under
  `.ufo/waves/round-38/wave1/`. No other lane, fleet or source-tree file was modified.
