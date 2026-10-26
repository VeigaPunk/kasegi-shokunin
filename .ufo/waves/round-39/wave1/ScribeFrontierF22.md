# ScribeFrontierF22 — round-39 scribe receipt

Item: draft the `corpus/README.md` end-of-file amendment block for Frontier F22, deliverable
`.ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md`. Leaf seat; no dispatch.

## Deliverable

- Path: `.ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md`
- Lines: **28** (27 content lines + one trailing empty line, the round-38 landing shape)
- Bytes: **2085**
- sha256: **a8aa90a29215c1ef73e76e7beec8e9dee7b96d3d6f3f00afd4d84a7625b22d25**
- Landed-at-EOF (R6): applied to the current `corpus/README.md` (486 lines) the file becomes
  **514 lines**, 28 added / 0 removed, no existing line renumbered.
- The file holds only landable bytes: heading, one intro paragraph, the 3-cell coverage-map table
  with one row, the 6-cell frontier table with one row, the r39 count-line paragraph. No receipt
  scaffolding, notes, or fences inside the deliverable.

Block content (in order):

1. `## Round-39 admission — coverage map row and Frontier F22 (appended 2026-10-26)`.
2. Intro paragraph: R6 statement, entry `knowledge/cisa-when-to-issue-vex.md`, Frontier F22,
   source S057, source basis = CISA's own "When to Issue VEX Information" page at
   `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information`, capture under
   `corpus/source-snapshots/round-39/`, opened 2026-10-26.
3. Coverage-map row (3 cells), exactly the spec cells:
   `VEX issuance and lifecycle guidance (round 39)` | `knowledge/cisa-when-to-issue-vex.md` |
   `S057 — public primary, opened 2026-10-26`.
4. Frontier row (6 cells): `F22` | `VEX issuance, lifecycle and inheritance guidance (CISA When to
   Issue VEX Information)` | `admitted` | `knowledge/cisa-when-to-issue-vex.md` | `S057` | next =
   `Keep the issuance layer distinct from the CSAF VEX document-content standard; a status update or
   reaffirmation is a new VEX statement, not a rewrite; upstream not_affected inheritance is
   conditional.` (the spec's three clauses rendered as one sentence; no clause added or dropped).
5. `[r39 amendment, appended 2026-10-26] … at round 39 the frontier stands at **22/22 admitted** —
   F01-F08 at round 23, F09 24, F10 25, F11 26, F12 28, F13 29, F14 30, F15 31, F16 33, F17 34,
   F18 35, F19 36, F20 37, F21 38, F22 39. The 0/18 sentence is untouched: …` — same paragraph
   shape and R9 history caveat as the r33/r34/r35/r38 count lines.

## Validation (commands and actual output)

Disk guard before work (green; no heavy pass run): `/fast/scratch/hyaku 24% use, 615.7G free`.

Transcript, run in `S=/fast/scratch/hyaku/kasegi-r39/ScribeFrontierF22` against a scratch copy of
the live lane README plus the block (`bash verify.sh`):

```
$ wc -l "$L/corpus/README.md"
486 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md

$ cp "$L/corpus/README.md" README.orig.md && cat README.orig.md block.md > README.applied.md
$ wc -l README.orig.md README.applied.md
  486 README.orig.md
  514 README.applied.md

$ diff README.orig.md README.applied.md | grep -c '^<'
0
$ diff README.orig.md README.applied.md | grep -c '^>'
28

$ grep -cE '^\| F[0-9]+ \|' README.applied.md
22
$ grep -E '^\| F22 \|' README.applied.md | awk -F'|' '{print NF-2" cells"}'
6 cells
$ grep -F '| VEX issuance and lifecycle guidance (round 39) |' README.applied.md | awk -F'|' '{print NF-2" cells"}'
3 cells

$ grep -c '^## Round-39 admission — coverage map row and Frontier F22 (appended 2026-10-26)$' README.applied.md
1
$ grep -c 'frontier stands at \*\*22/22 admitted\*\*' README.applied.md
1

$ grep -cE '^```|^~~~' README.orig.md      -> 2
$ grep -cE '^```|^~~~' README.applied.md   -> 2
$ grep -cP '\t' README.applied.md          -> 0
$ grep -cE ' +$' README.applied.md         -> 0

$ wc -c block.md ; wc -l block.md ; sha256sum block.md
2085 block.md
28 block.md
a8aa90a29215c1ef73e76e7beec8e9dee7b96d3d6f3f00afd4d84a7625b22d25  block.md

$ tail -c 20 block.md | xxd
00000000: 2073 7461 7973 206f 7574 7369 6465 2069   stays outside i
00000010: 742e 0a0a                                t...
```

Attribution check (Python over `README.applied.md`, comparing the new count line against the r38
count line already in the file):

```
frontier ids in applied file: 22, unique: 22, ordered F01..F22: True
attrib map covers F01-F22: True
F01-F21 attributions identical to the r38 history line: True | F22 round: 39
0/18 sentences: applied 9, orig 8   (the added one is the new paragraph's own restatement)
non-ascii inventory of block: ['—'] only
max block line length: 353 (the single-line frontier row, as in the r38 block)
```

Delivery check: `cp` into the wave dir then `cmp` -> `byte-identical`; both copies hash
`a8aa90a2…25`, `wc -lc` -> `28 2085`.

## Gates touched

- R6 pure-append: removed lines 0; every preceding line keeps its number.
- Frontier count basis used by C2's kill rule (`grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 22`)
  holds after the append.
- Shape gates the reviewer will apply: 6-cell frontier row, 3-cell coverage-map row, `22/22
  admitted` count line listing F01-F22 with round attributions, both blocks pure EOF appends.
- No fence introduced (2 -> 2): the block does not open or close a code fence, so the pre-existing
  round-37 scaffolding fence region (L426-L455) is left exactly as it is.

## Touched surfaces

- Wrote: `.ufo/waves/round-39/wave1/ScribeFrontierF22.readme.append.md` and this receipt. Scratch
  under `/fast/scratch/hyaku/kasegi-r39/ScribeFrontierF22/` (removed before yield).
- No lane-file edits, no fleet/sibling-repo writes, no git or jj mutations, no installs, no network
  fetches, no subagent dispatch.

## Findings and limits

- **Capture identity is deliberately absent.** At drafting time the round-39 artifacts are not in the
  lane working tree: `ls corpus/source-snapshots/round-39 corpus/knowledge/cisa-when-to-issue-vex.md`
  -> both `No such file or directory`, and `grep -n S057 corpus/SOURCES.md` returns nothing. The r38
  intro paragraph carries captured-at timestamp, HTTP status, byte/line counts and a snapshot sha256;
  those cannot be measured yet, so this block states only frozen-claim facts (URL, capture directory,
  `opened 2026-10-26`) and no invented bytes or hashes. If the L1 wants r38-level capture detail in
  the intro, it must be filled from `corpus/source-snapshots/round-39/manifest.json` at landing; the
  block is otherwise complete and needs no edit.
- The block ends with a trailing empty line so the landed tail matches the r38 tail
  (`…stays outside it.\n\n`); that empty line is included in the reported 28 lines / 514-line result.
- `not_affected` in the frontier `next` cell uses the CSAF VEX product-status token verbatim (same
  spelling as F21's row); it contains no pipe or escaped pipe, so the 6-cell split is clean.
- Sibling `ScribeProvinceF22.province.append.md` (already in wave1) names the same F22 entry and
  source S057; the two blocks agree on entry path, id, and round attribution.

## Coordination note — harness row-read gate (ExecHarnessProbe, round 39)

- Row-read limb is green on the delivered bytes: my own cell parse (6 cells) and
  ExecHarnessProbe's run of the harness `FRONTIER_ROW` regex against this block both read
  id `F22`, status `admitted` (exact, no modifier), entry `knowledge/cisa-when-to-issue-vex.md`.
- Landing-time gate, not satisfiable from this seat: the literal `PASS     F22 … ids=S057` plus
  `entries=25 pass=25 exit=0` pair can only be produced once `corpus/knowledge/cisa-when-to-issue-vex.md`
  and `corpus/source-snapshots/round-39/{S057.txt,manifest.json}` are all in the lane; a run now
  measures the 24-row baseline and prints `entries=24 pass=24 exit=0`. ExecHarnessProbe reports
  (their measurement, not re-run here) that an entry landed without its capture reds as
  `recheck-exit-2` because the entry's recheck line cds into the absolute lane root.
- Correction of record: this block's F22 `next` cell carries **no** citation —
  `grep -c 'S057.txt' ScribeFrontierF22.readme.append.md` -> 0 — so the `S057.txt:79-81`
  observation ExecHarnessProbe raised belongs to another artifact. The harness scans only the entry
  file for citations, so `selection-not-cited-by-entry` must be satisfied by the entry body, not by
  this README amendment. ExecHarnessProbe retracted the observation as their own fixture row and
  re-checked this block's L19 cells (their measurement).
- Post-landing confirmation, attributed and not re-run here: with the real entry and capture
  assembled over base `480b1a5`, ExecHarnessProbe measured `FAIL F22 … ids=S057 exit=2
  problems=recheck-exit-2` / `entries=25 pass=24 exit=1` on the unlanded tree and
  `PASS     F22 … ids=S057 exit=0` / `entries=25 pass=25 exit=0` once the cd prefix points at the
  tree carrying entry + capture + manifest (their §H, `.ufo/waves/round-39/wave1/ExecHarnessProbe.harness.txt`).
