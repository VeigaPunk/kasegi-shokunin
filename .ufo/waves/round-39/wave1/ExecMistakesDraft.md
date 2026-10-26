# ExecMistakesDraft — round 39 receipt

seat ExecMistakesDraft (executor, leaf) · round 39 · judged on depth:verifiability
lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` · lane head at work `d65d823e7c84813c192b20ee757a8761f878a61f`
base `480b1a505a2dfc14a4f718d16d63808247214d0a` · claims freeze `dcd31701720a6a4929a32471a62011ed87103421`
read first: `.ufo/waves/round-39/claims.json` (not edited), `.ufo/waves/round-39/c1-controls/before.txt`,
`.ufo/waves/round-39/wave1-spec.json` (item text for this seat and for the R34–R36 / corrections seats).
Driver: read-only git and grep only. No lane file written except this receipt and the deliverable beside it.
`$L` below is the lane repo; every measurement names its revision.

## 1. Deliverable

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-39/wave1/ExecMistakesDraft.mistakes.md`

    lines   6
    bytes   8209
    sha256  bc2137d624d050d1f022519727b3d316e8e887d4ac3072bb4abaa2590f87ec7b
    shape   header + separator + 4 data rows (M39-1 … M39-4, in item order)
    columns 7 data cells per line (8 pipe characters on every line, measured)
    fences  0 lines beginning with three backticks or three tildes
    escaped pipes 0 (no cell needs `\|`, so a naive split on `|` yields the same cells)
    pending vocabulary 0 occurrences

The item says "landable markdown table rows only", so the file carries **no** `## Mistakes` heading and **no**
intro prose — the L1 supplies the heading and any paragraph. The header row is included so the block is a
complete table on its own; if the L1 supplies its own header, drop line 1 and the separator on line 2.
The last column header is spelled `able to fail`, matching the round-38 table's header in
`corpus/lessons/round-38.md:281` (the item's prose spells the field `able-to-fail`; the table it describes
uses the spaced form).

Two byte choices:

- No `|` character appears inside any cell (inline code included). The one command whose literal form
  contains a pipe is written as `grep -cE '^. R[0-9]+ '` with the dot standing in for the leading pipe,
  and the cell says so.
- No placeholder vocabulary: a mechanical grep for the pending marker returns 0, so the row set cannot
  satisfy a placeholder sweep by including the token it hunts.

## 2. Measurements (commands and their outputs)

All read-only. Long lines are cut with `…` where the cut removes only unchanged text; nothing is paraphrased
inside a quoted fragment.

### 2.1 M39-1 — the frozen round-38 C1 could not print 8/8 at the head it named

    git -C $L rev-parse 66703ac
      -> 66703acaaff50529a35be49aa8759d04140720ad

    git -C $L show 9a10b02:.ufo/waves/round-38/claims.json  (C1)
      predicate        "…runs over a `git archive` export of a named lane head (`--export-ref <hash>`; plain run
                        refused, exit 2) and prints `closed=8/8 exit=0` on the round-38 judged head J…"
      G2               "`.ufo/waves/round-38/final-gates/all-gates.txt` in the export has header `all-gates v2`,
                        an `export-ref=<40-hex>` that is REF or an ancestor of REF with `git diff --name-only
                        <export-ref> REF` a subset of {that receipt path}, … eight `G<n> payload=… closed=1`
                        lines, `closed=8/8 exit=0`, …"
      counting[0]      "bash corpus/instruments/r38-closure.sh --export-ref <J> -> closed=8/8 exit=0"
      counting[1]      "bash corpus/instruments/r38-closure.sh --selftest --export-ref <J> -> selftest cases=8 failures=0 exit=0"
      judged_head_rule "The round-38 judged head J is the `export-ref=` value recorded in
                        `.ufo/waves/round-38/final-gates/all-gates.txt`. J is the lane commit that carries every
                        round-38 change except that receipt; the lane tip Y adds only the receipt file…"

    git -C $L show HEAD:.ufo/waves/round-38/final-gates/all-gates.txt | sed -n '1,20p' | nl -ba
        1  all-gates v2
        2  export-ref=66703acaaff50529a35be49aa8759d04140720ad
        3  suite-sha256=85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6
        4  run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e
        5  # Round-38 C1 receipt. export-ref = the judged head … (round-38 lesson, M38-8).
        6  export-ref-run: export-ref=66703acaaff50529a35be49aa8759d04140720ad mode=export lane=…
        8  export-ref-run: G2 payload=receipt=0,sentinel=0,export-ref=0,ancestor=0,diff-clean=0,digest-match=0,
           run-lines=0,closed-line=0,selftest-lines=0,selftest-summary=0,scorecard-ref=1,shonen-ref=1,
           head-token-lines=0 closed=0
       15  export-ref-run: closed=7/8 exit=1
       16  ## run over run-ref
       17  run-header: export-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e mode=export lane=… suite-sha256=…
       (lines 7, 9–14 are G1 and G3–G8 in the same prefixed block, all `closed=1`)

    git -C $L cat-file -e 66703ac:.ufo/waves/round-38/final-gates/all-gates.txt
      -> fatal: path '….ufo/waves/round-38/final-gates/all-gates.txt' exists on disk, but not in '66703ac'
      -> exit 128
    git -C $L cat-file -e 7dd2fcd:.ufo/waves/round-38/final-gates/all-gates.txt
      -> exit 0

    git -C $L show dcd3170:corpus/lessons/round-38.md | grep -c 'M38-8'
      -> 0
    git -C $L show HEAD:.ufo/waves/round-38/final-gates/all-gates.txt | grep -n 'M38-8'
      -> 5:# Round-38 C1 receipt. … (round-38 lesson, M38-8).

Read: G2 needs the receipt inside the export; the judged-head rule makes the receipt's own `export-ref` J;
no commit contains a file naming itself, so the J export cannot carry the receipt and G2 is red there. The
receipt is the measurement: 7/8 at J, 8/8 at `run-ref=7dd2fcd6`. Its prose attributes the finding to `M38-8`,
a row the round-38 lesson never minted.

### 2.2 M39-2 — five lane records state the opposite of that receipt

    git -C $L show dcd3170:corpus/lessons/round-38.md | sed -n '21p'   (C1 after-cell, tail)
      -> "suite landed (sha256 `85d33ea9…`, 1473 lines); `closed=8/8 exit=0` and `selftest cases=8 failures=0`
          over the judged head are the receipt `.ufo/waves/round-38/final-gates/all-gates.txt`; base and r37
          reviewed-head reds in `final-gates/reds.txt`"
    git -C $L show dcd3170:corpus/lessons/round-38.md | sed -n '94p'
      -> "8. **C1 receipts at the judged head.** … `--export-ref J` → `closed=8/8 exit=0`; `--selftest
          --export-ref J` → `selftest cases=8 failures=0`; …"
    git -C $L show dcd3170:LOG.md | sed -n '1698p'                     (C1 bullet, tail)
      -> "… Run and selftest over the judged head: `.ufo/waves/round-38/final-gates/all-gates.txt`; reds:
          `final-gates/reds.txt`."
    git -C $L show dcd3170:SCORECARD.md | sed -n '1517p'               (round-38 depth:verifiability row)
      -> "… the run over the round-38 head the receipt names, and its `--selftest`, are committed in
          `.ufo/waves/round-38/final-gates/all-gates.txt`; reds over the base `a173b0c2` … are committed in
          `.ufo/waves/round-38/final-gates/reds.txt`."
    git -C $L show dcd3170:SHONEN.md | sed -n '184,185p'               (box 3 + evidence)
      -> "184: - [~] Instructions executable by an agent without oral context"
      -> "185:       — evidence (round 38): … census exit 0; r38 suite run + selftest over the judged head:
          export-ref of .ufo/waves/round-38/final-gates/all-gates.txt (raw transcript committed there).
          Box stays `[~]`."
    git -C $L show dcd3170:corpus/lessons/round-38.md | grep -c 'closed=8/8'
      -> 2   (:21 and :94)
    git -C $L show dcd3170:corpus/lessons/round-38.md | grep -c 'selftest cases=8 failures=0'
      -> 2   (:21 and :94)
    git -C $L show dcd3170:LOG.md | wc -l
      -> 1702

Against them, from §2.1: `all-gates.txt:15 export-ref-run: closed=7/8 exit=1`, `:4 run-ref=7dd2fcd6…`,
`:16 ## run over run-ref`. Every one of the five sentences points at that file as the judged-head 8/8.

### 2.3 M39-3 — the report quotes a tip run with no committed transcript

    sed -n '35,38p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-38/kasegi.md
      36: - `bash corpus/instruments/r38-closure.sh --export-ref 66703acaaff50529a35be49aa8759d04140720ad`
            → **`closed=7/8 exit=1`** (G1, G3–G8 `closed=1`; G2 red: `receipt=0` — J cannot contain the receipt
            that names it). **This is the frozen counting command, and it misses.** The freeze declared G2 to
            read the receipt inside the export *and* declared J to be the receipt's `export-ref` — a self-…
      37: - `bash corpus/instruments/r38-closure.sh --export-ref f06148c66c6d7aed948cb7024d9f0b9cffe4b95a`
            (tip = J + receipt only) → `closed=8/8 exit=0`, every G line `closed=1`; `--selftest
            --export-ref f06148c6…` → `selftest cases=8 failures=0` (8 case lines `positive=pass …
            verdict=pass`; 5 forged-report judges rejected). Run by the L1 at 19:1xZ, lane HEAD = tip,
            worktree clean, `--work` outside the lane and kasegi-r3[678].
      38: - Committed receipt .ufo/waves/round-38/final-gates/all-gates.txt: `all-gates v2`,
            `export-ref=66703aca…`, `run-ref=7dd2fcd6…`, …

    git -C $L grep -c 'f06148c6' f06148c6 -- .
      -> 0 files  (the tip tree names its own hash nowhere)
    git -C $L ls-tree -r --name-only HEAD .ufo/waves/round-38/final-gates/
      -> .ufo/waves/round-38/final-gates/all-gates.txt
         .ufo/waves/round-38/final-gates/reds.txt
    git -C $L show 7dd2fcd:.ufo/waves/round-38/final-gates/all-gates.txt | head -14
        4  # BOOTSTRAP receipt (round 38). The run over export-ref 66703acaaff… itself printed closed=7/8: G2 is
           red there because that commit cannot contain this receipt. This draft …
       10  G2 payload=bootstrap-expected closed=1
    git -C $L show 7dd2fcd:.ufo/waves/round-38/final-gates/all-gates.txt | grep -c 'bootstrap-expected'
      -> 10
    git -C $L show 7dd2fcd:.ufo/waves/round-38/final-gates/all-gates.txt | grep 'case=G1\|closed=8/8\|selftest cases'
      -> selftest case=G1 bootstrap-expected
         closed=8/8 exit=0
         selftest cases=8 failures=0

Read: the committed 8/8 in the lane is over `7dd2fcd6`, whose payload lines are the placeholders
`bootstrap-expected`; a G2 that reads shape is green on it. The tip run the report quotes is real to its
author and unreproducible from the lane: `git grep` at `f06148c6` finds no file mentioning it.

### 2.4 M39-4 — two `captured-by: none` rows with no criterion

    git -C $L show dcd3170:corpus/QUALITY.md | grep -cE '^. R[0-9]+ '
      -> 33        (R1–R33; the dot stands for the row's leading pipe)
    for h in M38-1 M38-2 M38-4 M38-5 M38-7; do git -C $L show dcd3170:corpus/QUALITY.md | grep -c $h; done
      -> 1, 1, 1, 0, 0
    git -C $L show dcd3170:corpus/QUALITY.md | sed -n '291,292p'
      R32 cell  "M38-1 (`corpus/lessons/round-38.md` § Mistakes, minted this round) — routed as D-A by the
                 round-37 verifier …"
      R33 cell  "M38-2 and M38-4 (`corpus/lessons/round-38.md` § Mistakes, minted this round) — D-B: …"
    M38-5 captured-by cell: "none — R31 requires a disposition per touched proposal, but no check reads a row
                 count, so an empty section reads exactly like a filled one"
    M38-7 captured-by cell: "none — the wave context forbade fleet writes and required absolute paths, but
                 nothing enforced it inside a seat's own fixture driver"

Supporting read on the routed pointer (not used in the row): the round-38 spot-check's R4 suggests
"state why not (`LEARNING.md` §Understanding)"; the only `LEARNING.md` on this host is the fleet root's,
88 lines, and

    grep -n '^## Understanding' /home/vgpnk/Projects/shokunin/LEARNING.md
      -> exit 1 (no such section; headings at :26, :40, :55, :73, :82)

so the pointer itself does not resolve. That is why the row's fix names R36 rather than a document section.

## 3. Where R34–R36 and the corrections sweep come from

Both are other seats this wave, not files I could measure:

- `QUALITY.md` at the freeze commit carries 33 rows (R1–R33) and no `M39-` citation
  (`git -C $L show dcd3170:corpus/QUALITY.md | grep -c 'M39-'` → 0). R34 (dry-run a frozen
  counting command over a stand-in head before freeze), R35 (a quoted `--export-ref <hash> -> closed=K/K`
  needs a committed transcript or an explicit report-only label) and R36 (a `captured-by: none` row gets a
  QUALITY criterion citing it in the same round) are specified verbatim in `.ufo/waves/round-39/wave1-spec.json`
  under seat `ExecQualityCriteria`, grounded there in M39-1, M39-3 and M38-5/M38-7 respectively.
- The five-site `Correction (round 39)` sweep is seat `ExecCorrectionsR2` (same spec file: append blocks for
  `corpus/lessons/round-38.md`, `LOG.md`, and the SCORECARD/SHONEN corrections).

The rows name those three criteria and that sweep by number; they do not assert the files already contain
them.

## 4. Risks and notes for the L1

1. **The frozen round-39 claims mis-spell the round-38 judged head.** `.ufo/waves/round-39/claims.json`
   and the dispatch handoff both write `66703aca50529a35be49aa8759d04140720ad` — 37 characters, a dropped
   character rather than a wrong nibble — and `git -C $L rev-parse 66703aca50529a35be49aa8759d04140720ad`
   → `fatal: ambiguous argument … unknown revision`, while the receipt, the report and commit `66703ac` all
   carry `66703acaaff50529a35be49aa8759d04140720ad`. C1's kill rule names the unresolvable spelling, so a
   suite or receipt built from the frozen text verbatim will fail to resolve the r38 arm of its own red
   check. Claims are frozen and I did not touch them; the suite and receipt seats should use the resolvable
   hash. Two wave seats have already recorded the same read independently —
   `wave1/ExecCorrectionsR2.md:157-159` and `wave1/ScribeReportInputs.inputs.md:121-126` (the latter also
   gets `http=422` from the origin API for that string).
2. **Land order.** The rows cite R34–R36 and the corrections sweep. Land the `QUALITY.md` append and the
   `Correction (round 39)` lines before or with the lesson section, or the lesson cites criteria that a
   reader of the same head cannot find.
3. **M39-2's fix is the sweep alone.** No round-39 G-limb reads a prose "over the judged head" sentence that
   names no hash (G3 keys on quoted `export-ref` results); the row says so rather than borrowing G3 for it.
   If a limb is wanted, it has to be written; the row does not claim one exists.
4. **Byte form.** Header row included, `able to fail` spelled as in the round-38 table, no cell contains a
   pipe. If the L1 wants the lesson's own header, drop deliverable lines 1–2.

## 5. Scope, writes, scratch

- Writes: this receipt and the deliverable beside it, both under
  `.ufo/waves/round-39/wave1/`. Nothing else. No mutating git or jj command ran anywhere; every git call is a
  read (`show`, `cat-file -e`, `grep`, `rev-parse`, `diff --name-only`, `ls-tree`, `status --porcelain`,
  `log`, `merge-base`).
- Scratch: `/fast/scratch/hyaku/kasegi-r39/ExecMistakesDraft/` (one JSON copy of the round-38 claims, used
  to read the predicate without a pipe into python). Removed before yielding; verified absent.
- Tooling: none installed, nothing upgraded.
- No sibling lane, fleet-root or shokuknow path was written. No file under `scripts/`, `templates/`,
  `MANIFEST.json`, `.ufo/state/` or `.ufo/watchdog.log` was read for content or written.
