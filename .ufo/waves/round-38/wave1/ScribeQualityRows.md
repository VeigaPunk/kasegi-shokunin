# ScribeQualityRows — QUALITY.md R32/R33 append block (round 38)

Status: **block drafted and verified on a scratch copy; NOT landed** — `corpus/QUALITY.md` is outside this
seat's write scope (receipt, one deliverable file, scratch). Draft head
`700153593eb586c70a6499c8ca225ee4d673bc9b` (wave1 spec + dispatch); `corpus/QUALITY.md` at that head is
byte-identical to the round-38 base `a173b0c2…` (both `b17edd4e…`). Axis: depth:verifiability.

Deliverable: `.ufo/waves/round-38/wave1/ScribeQualityRows.block.md` — 14 lines, 3334 bytes, sha256
`60a89a4c49926a64a4917cff20a5a3922ca9211e4536eb114a3d9a43108c4735`. Its bytes are the whole append (leading
blank line included) and contain no notes, no validation text and no headings that are not landed text.

## 1. What the two rows say and what they cite

- **R32** (criterion text verbatim from the item): a front-door append lands only its declared block —
  bytes equal to a `<path> <lines> <sha256>` declaration recorded before landing — and the file's fenced-code
  state at EOF is closed; receipt validation text never lands. Grounded in **M38-1**
  (`corpus/lessons/round-38.md` § Mistakes) via round-37 verifier D-A
  (`corpus/lessons/round-37-verifier-spotcheck.md:159-164`) with the measured size delta
  (`…:113-118`: `PROVINCE.md` 74 added lines, README 56) and the limb gap (`…:169-174`).
- **R33**: closure order — the judged head carries every round artifact including the wave results
  (WAVE-DONE before the judged head); lane files name the judged head by reference to the gate receipt, never
  by a hash they cannot contain; the report is filed after the last lane commit. Grounded in **M38-2**
  (three heads named final, `…:165-168`) and **M38-4** (closure-order recurrence, `…:175-177`), and widens
  `considerthese/2026-10-26.md:31` proposal 3 (2026-10-26) from a status/placeholder gate to closure order.

Both rows cite `corpus/lessons/round-38.md`. The ids agree with the sibling `## Mistakes` draft, read
read-only: `.ufo/waves/round-38/wave1/ScribeMistakes.block.md:12` (M38-1), `:13` (M38-2), `:15` (M38-4).

## 2. R6 preamble — every literal and the command that produced it

| literal in the block | value | command (lane root, draft head `7001535`) | observed |
|---|---|---|---|
| bytes before the append | `43235` | `wc -c < corpus/QUALITY.md` | `43235` |
| lines before the append | `278` | `wc -l < corpus/QUALITY.md` | `278` |
| digest of those bytes | `b17edd4e848e63cbbed7cfe9bcb91b73158a93532c9b75ebb074d25e90f034ab` | `head -c 43235 corpus/QUALITY.md \| sha256sum` | `b17edd4e…f034ab  -` |
| unedited rows | R22 226, R23 227, R26 249, R27 250, R28 263, R29 264, R30 277, R31 278 | `grep -nE '^\| R(22\|23\|26\|27\|28\|29\|30\|31) ' corpus/QUALITY.md` | `226 227 249 250 263 264 277 278` |
| the figure is the tracked figure | — | `git show HEAD:corpus/QUALITY.md \| sha256sum`; `git show a173b0c2…:corpus/QUALITY.md \| sha256sum`; `git --no-optional-locks status --porcelain -- corpus/QUALITY.md` | `b17edd4e…` / `b17edd4e…` / empty (clean) |

The block's six preamble lines state those literals and then say the landing commit re-runs both commands
immediately before writing, because a draft-time byte figure is a stale premise under R19 if an earlier
append in the same round moved it. The block adds no placeholders (see §3.7).

## 3. Verification, every command and its output (all on copies under `$S`, never on the lane file)

`$S=/fast/scratch/hyaku/kasegi-r38/ScribeQualityRows`; `S=/fast/scratch/hyaku/kasegi-r38/ScribeQualityRows; cp corpus/QUALITY.md $S/fixture/corpus/QUALITY.before.md` seeded the copies.

1. **Append arithmetic.** `wc -c -l` before → `278 43235`; block → `14 3334`; after
   `cat block.md >> fixture/corpus/QUALITY.md` → `292 46569`; `head -c 43235` of the result →
   `b17edd4e…f034ab` (prefix byte-identical); `tail -n 14 | sha256sum` → `60a89a4c…c4735` (the block is
   exactly the file's last 14 lines).
2. **Additivity (R6).** `diff before after | grep -c '^<'` → `0`; `grep -c '^>'` → `14`. Every existing line
   keeps its number; no line is edited.
3. **Table shape.** `awk '{n=gsub(/\|/,"|"); print n}'` over the four table lines → `4 4 4 4` pipes, i.e.
   three cells each; no cell carries an unescaped pipe, so the R6 table keeps its columns.
4. **Id uniqueness.** `grep -cE '^\| R3[23] ' corpus/QUALITY.md` at draft head → `0` (exit 1; the last row is
   R31 at `:278`); on the appended copy → `1` for R32 and `1` for R33.
5. **Declared-block contract** (`wave1/ExecDeclaredBlocks.gen.sh`, the G1 generator, run in `$S/gen` with a
   copy of the pre-append file at `corpus/QUALITY.md`):
   - `gen corpus/QUALITY.md $S/block.md` → `corpus/QUALITY.md 14 60a89a4c49926a64a4917cff20a5a3922ca9211e4536eb114a3d9a43108c4735`,
     stderr `target=corpus/QUALITY.md pre_lines=278 post_lines=292 block_bytes=3334 block_newlines=14 declared_lines=14 tail_view=exact`,
     optional guard `# base corpus/QUALITY.md 278`.
   - `check` on the clean appended copy → `OK   corpus/QUALITY.md lines=14 file_lines=292 sha256=60a89a4c…`,
     `declared=1 ok=1 fail=0 base=0 exit=0`.
   - mutant *junk line appended after the block* → `FAIL corpus/QUALITY.md lines=14 want=60a89a4c… got=51e2958e60a23c5bc93dd8669ed6a887e8bc90a99fc98a062f881b61ea50cc40 file_lines=293`,
     `declared=1 ok=0 fail=1 base=0 exit=1`.
   - mutant *one byte flipped inside the block* (`cannot contain` → `cannot contaIn`) →
     `FAIL … got=98d2df1e771b50760887f23cea8c8c58b9437abaa9c13b713d1ec765efd036ef file_lines=292`, exit 1.
   - mutant *junk inserted before the block* → suffix-only check prints `OK … file_lines=293`, `exit=0`: the
     suffix anchor cannot see a pre-block insertion. With the base guard: `FAIL base corpus/QUALITY.md
     file_lines=293 != pre_lines=278 + declared_lines=14 (lines were added before the declared block)`,
     `declared=1 ok=1 fail=1 base=1 exit=1`. Clean copy with the same guard → `OK base … file_lines=292
     pre_lines=278 declared_lines=14`, `exit=0`.
6. **Fence state** (`wave1/ExecFenceWalk.sh`, the G1 CommonMark walker): before → `closed` (rc 0); after →
   `closed` (rc 0); walker selftest → `selftest cases=10 failures=0`. The block introduces no fence.
7. **Widened placeholder vocabulary (G3's fixed strings + word-bounded tokens), scanned on the block:**
   `⟨pending` 0, `<fill>` 0, `filled by the L1` 0, `<LANE_HASH>` 0, `<r38-` 0, `grep -cwE 'TBD|TODO'` 0. The
   only angle-bracket tokens in the block are `<path> <lines> <sha256>`, which are R32's criterion text
   naming the declaration fields, not a pending marker.
8. **Anchor gate** (`corpus/instruments/anchorcheck.py`, read-only):
   - lane file at draft head → `32 in-range cite instances, 1 bad; 32 distinct anchors; LOST-RECORDED=0
     PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 1;
   - appended copy (`KASEGI_LANE_ROOT=<lane>`) → `38 in-range cite instances, 1 bad; 38 distinct anchors;
     …`, exit 1.
   The single bad class is identical in both runs — `PAST-EOF md:77 README.md:159 (file has 14 lines)`,
   pre-existing and unrelated. The append adds six resolvable anchors and removes none: the spot-check
   `:159-164`, `:113-118`, `:169-174`, `:165-168`, `:175-177` cites and the quoted `PROVINCE.md:80-152`.
9. **Landing check** (to be run by the landing agent after `cat`, `bash -n` clean here):

   ```sh
   cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
   f=${1:-corpus/QUALITY.md}
   pin=60a89a4c49926a64a4917cff20a5a3922ca9211e4536eb114a3d9a43108c4735
   pre=43235
   d=$(tail -n 14 "$f" | sha256sum | cut -d' ' -f1)
   n=$(wc -l < "$f")
   h=$(head -c "$pre" "$f" | sha256sum | cut -d' ' -f1)
   printf 'file=%s tail14=%s lines=%s prefix_sha=%s\n' "$f" "$d" "$n" "$h"
   [ "$d" = "$pin" ] && [ "$n" -eq 292 ] && [ "$h" = b17edd4e848e63cbbed7cfe9bcb91b73158a93532c9b75ebb074d25e90f034ab ] \
     && { echo "quality_block=landed_exact"; exit 0; }
   echo "quality_block=drift"; exit 1
   ```

   Measured on the appended copy → `quality_block=landed_exact`, exit 0. Measured on the unlanded lane file
   as a control → `tail14=cf3bba2c…`, `lines=278`, `quality_block=drift`, exit 1.

## 4. Landing recipe

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
cat .ufo/waves/round-38/wave1/ScribeQualityRows.block.md >> corpus/QUALITY.md
```

then §3.9. Optional, recommended (see F2): append this line to
`.ufo/waves/round-38/declared-blocks.txt` (absent at draft time, `ls` → No such file):

```
corpus/QUALITY.md 14 60a89a4c49926a64a4917cff20a5a3922ca9211e4536eb114a3d9a43108c4735
```

and, if this block is QUALITY.md's last append of the round, the guard `# base corpus/QUALITY.md 278`.
If any file changes `corpus/QUALITY.md` before this block lands, the three preamble literals and the
declaration digest are stale: re-run `wc -c`, `wc -l`, `head -c … | sha256sum` and
`ExecDeclaredBlocks.gen.sh gen corpus/QUALITY.md <block>` and substitute — the preamble already says the
landing commit re-runs both commands.

## 5. Findings

- **F1 — the preamble literals are tracked bytes, not draft estimates.** At `7001535`, HEAD, base
  `a173b0c2` and the worktree all hash `b17edd4e…` for `corpus/QUALITY.md`, so the literals `43235`, `278`
  and the digest describe committed bytes; the re-run clause covers the only way they can go stale (an
  earlier round-38 append to the same file).
- **F2 — G1's declared-block coverage does not include `corpus/QUALITY.md`.** The G1 contract (suite spec)
  names `PROVINCE.md` and `corpus/README.md`; QUALITY.md's 14-line append would be the round's largest
  undeclared markdown append. Declaring it (§4) costs one line and is measured green, with both mutants red
  (§3.5). Stated as a recommendation; this seat writes no lane file.
- **F3 — the suffix anchor alone cannot see a pre-block insertion** (§3.5, junk-before `exit=0`); the
  `# base` guard is what catches it, and it is sound here only because one seat owns QUALITY.md rows this
  round, so this append is the file's last. Recorded so a later round does not read the suffix check as
  sufficient.
- **F4 — gate visibility depended on writing the anchors fully qualified.** Three cites were first drafted as
  bare `:113-118`, `:169-174`, `:175-177` continuation refs, which `anchorcheck.py` does not match; they were
  rewritten to `corpus/lessons/round-37-verifier-spotcheck.md:NNN-MMM` and now resolve (§3.8). This is the
  same invisibility class as round-37 receipt F2.
- **F5 — R32 states its own unmeasured arm.** The criterion names `SKILL.md`, but G1 walks only `PROVINCE.md`
  and `corpus/README.md`; the grounding cell says the SKILL.md arm "is stated as the bar and has no G1 limb
  yet" rather than implying it is measured, per the R21 disclosure pattern.
- **F6 — `corpus/lessons/round-38.md` does not exist at draft time** (`ls corpus/lessons/round-38.md` → No
  such file). Both rows cite it by path only (no `:NN` anchor), so the anchor gate cannot go PAST-EOF on it,
  but the judged head must contain the lesson; the "minted this round" phrasing presumes the M38 rows land in
  that lesson, which the sibling draft already carries (§1). This block and that lesson belong in the same
  judged head J.
- **No suite run is claimed.** `corpus/instruments/r38-closure.sh` and
  `wave1/ExecSuiteBuild.r38-closure.sh` are both absent at my checks (`ls` → No such file), so nothing here
  reads a G1/G3 verdict from the suite; the G-references in the rows describe the suite contract, and the
  declared-block behaviour quoted in §3.5 is the generator's own measured output, not the suite's.

## 6. Tooling and scratch

- No tool installed or upgraded (nothing needed); no package manager run.
- Read-only tools used: `git` (`rev-parse`, `log`, `show`, `status --no-optional-locks`),
  `python3 corpus/instruments/anchorcheck.py`, `bash wave1/ExecDeclaredBlocks.gen.sh`,
  `bash wave1/ExecFenceWalk.sh`, `wc`, `sha256sum`, `awk`, `sed`, `diff`, `cmp`, `od`. The two wave-dir
  scripts were executed, not modified; they wrote only under `TMPDIR=$S/tmp`.
- Scratch `$S=/fast/scratch/hyaku/kasegi-r38/ScribeQualityRows` is removed before this seat yields
  (`rm -rf -- "$S"` after the receipt and the deliverable were copied out); copies made: the block
  (`60a89a4c…`) and this receipt.
