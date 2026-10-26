# ExecDeclaredBlocks — round 38: the declared-blocks contract behind G1

Seat `ExecDeclaredBlocks` (leaf, executor; axis depth:verifiability). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only for this seat except this receipt, the
helper beside it and `/fast/scratch/hyaku/kasegi-r38/ExecDeclaredBlocks/`. No lane, fleet, sibling-lane
or source-tree file was written; no mutating git command was run (only `rev-parse`, `ls-files`,
`check-ignore`, `log`, `diff --numstat`, `archive`).

## 0. State read

| object | value |
|---|---|
| lane HEAD at work | `700153593eb586c70a6499c8ca225ee4d673bc9b` |
| round-38 base / claims freeze | `a173b0c2b98c5ae39599fa9be76027fbbead0b9e` / `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` |
| working tree | clean except untracked `.ufo/waves/round-38/wave1{,.ready,.ready.partial}/` (pre-existing + this wave's seats) |
| `PROVINCE.md` / `corpus/README.md` at HEAD | 152 / 454 lines, both newline-terminated |
| `.ufo/waves/round-38/declared-blocks.txt` | absent at this head — the L1 creates it; this seat supplies the generator that writes its lines |
| r37 receipt (block source) | `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`, tracked (`git ls-files --error-unmatch` → yes), 173 lines |
| interpreters | `GNU bash 5.3.20(1)`; `tail (GNU coreutils) 9.12` and `/usr/bin/sha256sum (GNU coreutils) 9.12` — what a child `bash` resolves; `Python 3.14.8` for measurement only |

Deliverable (byte-exact, beside this receipt):

| file | lines | bytes | sha256 | mode |
|---|---|---|---|---|
| `wave1/ExecDeclaredBlocks.gen.sh` | 547 | 21537 | `49925cd44d496074090432319c36d1cecc6e0f2020e53f4ef4b4ebb4977fa77d` | `-rwxr-xr-x` |

It supersedes nothing and is not yet in `corpus/instruments/`; §8 gives the landing path and the
two-line inline core if G1 prefers to inline the check.

## 1. The contract as implemented

One declaration per file, in `<lane>/.ufo/waves/round-38/declared-blocks.txt`:

```text
<path> <lines> <sha256>
```

* `<path>` is lane-relative (leading `/` and `..` are rejected), `<lines>` a positive integer,
  `<sha256>` 64 lowercase hex.
* The assertion is the item's check, verbatim: `tail -n <lines> <path> | sha256sum` == `<sha256>`.
  It is a **suffix** assertion: the file's last `<lines>` lines, byte for byte, are the appended block.
* `<lines>` counts the newline-terminated lines the block adds, plus one when the block's last line is
  unterminated (that line still begins a line of the result). `<sha256>` is **measured, not predicted**:
  `gen` writes the block behind one sentinel line in a probe file, runs `tail -n <lines>` on the probe
  exactly as the check runs it on the target, and digests that output. A host whose `tail` normalises an
  unterminated final line is reported (`tail_view=normalized`) instead of silently emitting a digest the
  check cannot reproduce (measured `exact` on this host, §4).
* Two refusals keep the assertion meaningful: `gen` exits 2 when the target does not end with a newline
  (`cat` would merge the block into the target's last line, which no line-suffix declaration can
  express) and when `<path>` is absolute.
* Optional guard `# base <path> <pre_lines>` additionally requires `wc -l <path>` == `<pre_lines>` +
  `<lines>` once the block has landed. It closes the one hole a suffix check cannot see — junk inserted
  *before* the declared block (tail still matches) — and is only sound for a file whose declared append
  is its last append. `gen` prints the guard it would emit on stderr; stdout stays the single landable
  declaration line.
* Fail-closed edges: an empty/comment-only list is red (`declared=0 … fail=1 exit=1`), duplicate
  declarations for one path are red, and every malformed line is a red declaration, never a usage error.
* Exit codes: 0 pass, 1 a defect is present, 2 a defect in the invocation (unreadable input,
  unterminated target). All scratch under `mktemp -d` (TMPDIR-honouring), removed on exit.

## 2. `gen` and `check` on a real 3-line block (scratch copy of `PROVINCE.md`, 152 lines)

```text
$ git -C <lane> archive HEAD PROVINCE.md corpus/README.md | tar -x -C $S/mirror
$ cd $S/ev/e1 && bash <deliverable> gen PROVINCE.md block3 > declared-blocks.txt && cat declared-blocks.txt
ExecDeclaredBlocks.gen.sh: target=PROVINCE.md pre_lines=152 post_lines=155 block_bytes=62 block_newlines=3 declared_lines=3 tail_view=exact
ExecDeclaredBlocks.gen.sh: optional base guard: # base PROVINCE.md 152
PROVINCE.md 3 d171fab0d6fb3131f7c0ff7cacb4f32e4a0db054d96dd81a1b66d9beb860f5db
$ cd $S/ev/e1 && cat block3 >> PROVINCE.md && wc -l PROVINCE.md
155 PROVINCE.md
$ cd $S/ev/e1 && bash <deliverable> check declared-blocks.txt
OK   PROVINCE.md lines=3 file_lines=155 sha256=d171fab0d6fb3131f7c0ff7cacb4f32e4a0db054d96dd81a1b66d9beb860f5db
declared=1 ok=1 fail=0 base=0 exit=0
```

(`block3` = `[fixture amendment, appended] first\nsecond\nthird\n`; 62 bytes, 3 newlines.)

## 3. Mutants on the same scratch copies — every one red

**One byte flipped inside the appended block** (`correction line two` → `Correction line two`):

```text
$ cd $S/ev/e2 && sed -i 's/^correction line two$/Correction line two/' PROVINCE.md && bash <deliverable> check declared-blocks.txt
FAIL PROVINCE.md lines=3 want=d171fab0d6fb3131f7c0ff7cacb4f32e4a0db054d96dd81a1b66d9beb860f5db got=5a75f1e69e5fc653864e191f2fcf936411f9e92d738d4507b26907c374189ac7 file_lines=155
declared=1 ok=0 fail=1 base=0 exit=1
```

**One extra line appended after the block**:

```text
$ cd $S/ev/e3 && printf 'stray line\n' >> PROVINCE.md && bash <deliverable> check declared-blocks.txt
FAIL PROVINCE.md lines=3 want=d171fab0d6fb3131f7c0ff7cacb4f32e4a0db054d96dd81a1b66d9beb860f5db got=f6e6e59fade9e90b229386b5d667fbb51734c9397fa5b2de3ea55c36523737e9 file_lines=156
declared=1 ok=0 fail=1 base=0 exit=1
```

Both are detected by the digest alone: the check is suffix-anchored, so the last `<lines>` lines are no
longer the block. `file_lines` is reported for diagnosis only — it is not part of the assertion.

**Junk inserted BEFORE the block** (the shape a suffix check cannot see; scratch selftest case T7,
reproduced with a synthetic 3-line fixture):

```text
  tail-only: rc=0 declared=1 ok=1 fail=0 base=0 exit=0
  OK   front.md lines=3 file_lines=7 sha256=0dd57cebe6d4f2dd3c16764174e390d8accb638ed7e0c6d71f4ed228280008cb
  FAIL base front.md file_lines=7 != pre_lines=3 + declared_lines=3 (lines were added before the declared block)
  declared=1 ok=1 fail=1 base=1 exit=1
  clean base guard: rc=0 declared=1 ok=1 fail=0 base=1 exit=0
```

**Missing file, malformed lines, duplicate path, empty list** (each `rc=1`):

```text
  bad-sha     rc=1  FAIL line=1 sha256 must be 64 lowercase hex: 0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF declared=1 ok=0 fail=1 base=0 exit=1
  wrong-sha   rc=1  FAIL front.md lines=3 want=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef got=0dd57cebe6d4f2dd3c16764174e390d8accb638ed7e0c6d71f4ed228280008cb file_lines=6 declared=1 ok=0 fail=1 base=0 exit=1
  bad-lines   rc=1  FAIL line=1 lines must be a positive integer: x declared=1 ok=0 fail=1 base=0 exit=1
  two-fields  rc=1  FAIL line=1 malformed: want "<path> <lines> <sha256>", got 2 field(s): front.md 0dd57cebe6d4f2dd3c16764174e390d8accb638ed7e0c6d71f4ed228280008cb declared=1 ok=0 fail=1 base=0 exit=1
  dup         rc=1  FAIL line=2 duplicate declaration for front.md (one declaration per file; concatenate the round appends into one block file) declared=1 ok=1 fail=1 base=0 exit=1
  empty       rc=1  FAIL empty.txt carries no declaration declared=0 ok=0 fail=1 base=0 exit=1
$ bash <deliverable> check missing.txt --root $S/emptyroot
FAIL corpus/README.md lines=27 file-missing under root=/fast/scratch/hyaku/kasegi-r38/ExecDeclaredBlocks/emptyroot
declared=1 ok=0 fail=1 base=0 exit=1
```

## 4. Trailing-newline edge — measured, not assumed

Block without a final newline, appended to a scratch copy of `corpus/README.md` (454 lines):

```text
block bytes=70 newlines=1 last_byte=107
$ cd $S/ev/e4 && bash <deliverable> gen README.md block-nonl > declared-blocks.txt && cat declared-blocks.txt
ExecDeclaredBlocks.gen.sh: target=README.md pre_lines=454 post_lines=456 block_bytes=70 block_newlines=1 declared_lines=2 tail_view=exact
ExecDeclaredBlocks.gen.sh: optional base guard: # base README.md 454
README.md 2 087f4e0f4e8adfc151c0e709a143ffa2c783716310322a0cdc0759701645beea
sha256 of the block file itself = 087f4e0f4e8adfc151c0e709a143ffa2c783716310322a0cdc0759701645beea
$ cd $S/ev/e4 && cat block-nonl >> README.md && printf 'final byte of README.md = %s\n' "$(tail -c 1 README.md | od -An -tu1 | tr -d ' ')" && bash <deliverable> check declared-blocks.txt
final byte of README.md = 107
OK   README.md lines=2 file_lines=455 sha256=087f4e0f4e8adfc151c0e709a143ffa2c783716310322a0cdc0759701645beea
declared=1 ok=1 fail=0 base=0 exit=0
```

Documented behaviour, in the terms the check is written in:

1. `<lines>` = newlines in the block + 1 = 2 (the unterminated last line still starts a line of the
   result); `wc -l README.md` counts 455 after the append, one fewer than the file's line count as a
   reader sees it — the declaration is about `tail -n`, not about `wc -l`.
2. On this host **`tail -n 2` reprints the unterminated final line verbatim**, with no added newline
   (`tail -c 1` → 107 after the append; `tail_view=exact`). The declared digest is therefore exactly
   `sha256(<block bytes>)`, as the second and third lines above show, and the append byte-identically
   reproduces the block.
3. Verified on both implementations present on this host: `/usr/bin/tail` (GNU coreutils 9.12, what a
   child `bash` resolves) and the wrapper shell's builtin `tail`, on `printf 'x\ny'`:
   `tail -n 2 | od -c` → `x \n y` (3 bytes) for each, digest `9ab9de25…6f9a87` for both. A host whose
   tail *does* normalise (POSIX's older "add a newline" reading) is caught by the `cmp` in `gen`, which
   then prints `tail_view=normalized` rather than a digest that will not reproduce.
4. A target that itself lacks a final newline is refused (exit 2), because the block would merge into
   the target's last line and no suffix declaration could express it:

```text
$ cp $S/ev/e5/no-newline front.md; bash <deliverable> gen front.md block3; echo rc=$?
ExecDeclaredBlocks.gen.sh: target does not end with a newline: front.md (cat would merge the block into its last line; no line-suffix declaration can express that append)
rc=2
```

## 5. The round-37 quoted digests — recomputed, and exactly which bytes they hash

The verifier's quoted digests are the sha256 of the bytes **between the ```` ```text ```` fence and the
closing ```` ``` ````** of `.ufo/waves/round-37/wave1/ScribeFrontierAmendments.md`, each line carrying its
own `\n` — i.e. `sed -n '<range>p'` of that receipt. Fence lines are at 49/52, 67/95, 125/129.

| digest | source lines | bytes | newlines | ends with | preimage |
|---|---|---|---|---|---|
| `cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545` | 50–51 | 295 | 2 | `\n` | an empty line then one 294-byte line: `[r37 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F20 — SSVC (Stakeholder-Specific Vulnerability Categorization) decision-point-based prioritization — admitted round 37; entry \`corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md\` (source S054)` — the leading blank line is part of the block |
| `2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b` | 68–94 | 2947 | 27 | `\n\n` (last line empty) | `## Round-37 admission — coverage map row and Frontier F20 (appended 2026-10-26)` … `surfaces present, and the frontier count stays outside it.` + one blank line; no extra leading newline |

```text
$ sed -n '50,51p' <r37 receipt> | sha256sum
cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545  -
$ sed -n '50,51p' <r37 receipt> | wc -lc
      2     295
$ sed -n '68,94p' <r37 receipt> | sha256sum
2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b  -
$ sed -n '68,94p' <r37 receipt> | wc -lc
     27    2947
$ sed -n '94p' <r37 receipt> | od -c
0000000  \n
0000001
```

These are the same digests the receipt's own §2/§3 property tables claim; both reproduce byte-exactly, so
the r37 numbers were sound. Feeding those exact blocks through `gen` returns the same declarations
(stdout line first, stderr advisory after):

```text
$ cd $S/mirror && bash <deliverable> gen PROVINCE.md $S/ev/prov.block > $S/ev/prov.decl && cat $S/ev/prov.decl
ExecDeclaredBlocks.gen.sh: target=PROVINCE.md pre_lines=152 post_lines=154 block_bytes=295 block_newlines=2 declared_lines=2 tail_view=exact
ExecDeclaredBlocks.gen.sh: optional base guard: # base PROVINCE.md 152
PROVINCE.md 2 cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545
$ cd $S/mirror && bash <deliverable> gen corpus/README.md $S/ev/readme.block > $S/ev/readme.decl && cat $S/ev/readme.decl
ExecDeclaredBlocks.gen.sh: target=corpus/README.md pre_lines=454 post_lines=481 block_bytes=2947 block_newlines=27 declared_lines=27 tail_view=exact
ExecDeclaredBlocks.gen.sh: optional base guard: # base corpus/README.md 454
corpus/README.md 27 2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b
```

(As captured, stdout is the redirected declaration file and the two stderr advisories are the log lines
above it; the declaration is one line, byte-identical to the r37 §2/§3 block digests.)

## 6. The same two declarations against the round-37 LANDED tree → both red (D-A detected)

Export of r37 judged head `2387dcf6ccfefcfb703783387b9aade8fc82abfa`
(`git archive 2387dcf6 PROVINCE.md corpus/README.md`), declaration file = the two lines of §5:

```text
$ cd $S/ev/r37 && cat declared-blocks.txt && bash <deliverable> check declared-blocks.txt
PROVINCE.md 2 cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545
corpus/README.md 27 2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b
FAIL PROVINCE.md lines=2 want=cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545 got=05c4c58ba7f63b67f4dc634317fb9702b663a5431c7d982b216bcc3d7fb8c63f file_lines=152
FAIL corpus/README.md lines=27 want=2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b got=4c2ee1d796e2bee0c1524e4556d7ee88231f4d14e096e5dd58b6c779c380692f file_lines=454
declared=2 ok=0 fail=2 base=0 exit=1
```

Where the bytes actually went (measured on the same export):

```text
$ git -C <lane> diff --numstat b56a41680cefd391868c1c370dc063c69d827e7d 2387dcf6ccfefcfb703783387b9aade8fc82abfa -- PROVINCE.md corpus/README.md
74	0	PROVINCE.md
56	0	corpus/README.md
$ sed -n '79,80p' PROVINCE.md | sha256sum            # the intended 2-line block, byte-identical …
cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545  -
$ tail -n 2 PROVINCE.md | sha256sum                 # … but not at EOF; the tail is scaffolding
05c4c58ba7f63b67f4dc634317fb9702b663a5431c7d982b216bcc3d7fb8c63f  -
$ grep -c '^## Round-37 admission' corpus/README.md
0
$ sed -n '69,94p' <r37 receipt> | sha256sum         # block lines 2..27 …
c7b8b0ca67273ab60f73e212b26709bf8f1dbe85748376cb7a35449db6f78a39  -
$ sed -n '400,425p' corpus/README.md | sha256sum     # … landed contiguously at 400-425 …
c7b8b0ca67273ab60f73e212b26709bf8f1dbe85748376cb7a35449db6f78a39  -
$ sed -n '426,454p' corpus/README.md | wc -l          # … followed by 29 lines of receipt scaffolding
29
```

Reading, without over-claiming: in `PROVINCE.md` the declared block landed byte-identically at 79–80 and
the file then grew 72 lines of scaffolding to 152, so the declared 2-line suffix does not match. In
`corpus/README.md` the block's heading line never landed (`^## Round-37 admission` → 0), its remaining
26 lines landed contiguously at 400–425, and the file ends in §3/§4 scaffolding — the landed append is
56 lines where the declaration is 27. Both are exactly the red the contract is meant to produce. Adding
the base guards for the line counts before the r37 appends makes both limbs red as well:

```text
$ { printf '# base PROVINCE.md 78\n# base corpus/README.md 398\n'; cat declared-blocks.txt; } > declared-base.txt
$ bash <deliverable> check declared-base.txt
FAIL PROVINCE.md lines=2 want=cdfe44e319094957ec583b7c3cd8212b882752b75682d9f1cf4d0b734f20f545 got=05c4c58ba7f63b67f4dc634317fb9702b663a5431c7d982b216bcc3d7fb8c63f file_lines=152
FAIL corpus/README.md lines=27 want=2ebd8cd2881b020cb0e234658adf132cf4741c1d226e1d7c267f7d71c5b7e97b got=4c2ee1d796e2bee0c1524e4556d7ee88231f4d14e096e5dd58b6c779c380692f file_lines=454
FAIL base PROVINCE.md file_lines=152 != pre_lines=78 + declared_lines=2 (lines were added before the declared block)
FAIL base corpus/README.md file_lines=454 != pre_lines=398 + declared_lines=27 (lines were added before the declared block)
declared=2 ok=0 fail=4 base=2 exit=1
```

The contract detects the r37 shape; it does not repair it.

## 7. In-helper selftest — 8 cases, 0 failures, both fixtures

`selftest` re-derives the contract's mutants in `mktemp -d` scratch, using `--root`'s `PROVINCE.md`
when present and a synthetic 3-line fixture otherwise (so it is runnable inside a `git archive` export
or from any cwd):

```text
$ bash <deliverable> selftest --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
selftest fixture=PROVINCE.md root=/home/vgpnk/Projects/shokunin/kasegi-shokunin
selftest case=T1 name=case_T1 result=pass
selftest case=T2 name=case_T2 result=pass
selftest case=T3 name=case_T3 result=pass
selftest case=T4 name=case_T4 result=pass
selftest case=T5 name=case_T5 result=pass
selftest case=T6 name=case_T6 result=pass
selftest case=T7 name=case_T7 result=pass
selftest case=T8 name=case_T8 result=pass
selftest cases=8 failures=0 exit=0
$ bash <deliverable> selftest
selftest fixture=synthetic root=.
selftest case=T1 name=case_T1 result=pass
selftest case=T2 name=case_T2 result=pass
selftest case=T3 name=case_T3 result=pass
selftest case=T4 name=case_T4 result=pass
selftest case=T5 name=case_T5 result=pass
selftest case=T6 name=case_T6 result=pass
selftest case=T7 name=case_T7 result=pass
selftest case=T8 name=case_T8 result=pass
selftest cases=8 failures=0 exit=0
```

| case | fixture mutation | expected | observed |
|---|---|---|---|
| T1 | append the 3-line block, declare, check | ok | `OK front.md lines=3 …`, `exit=0` |
| T2 | flip one byte inside the block (`second` → `secOnd`) | red | `FAIL … want=0dd57ceb… got=9c79b88c…`, `exit=1` |
| T3 | append a stray line after the block | red | `FAIL … want=0dd57ceb… got=2a4c71d4…`, `exit=1` |
| T4 | block with no final newline | lines=nl+1, digest=sha(block), ok | `OK front.md lines=1 …`, last byte ≠ `\n` |
| T5 | target with no final newline | exit 2 + reason | `target does not end with a newline …` |
| T6 | uppercase sha / wrong sha / `x` lines / 2 fields / duplicate path / empty list | rc=1 each | six `FAIL` lines, `exit=1` each (full text in §3) |
| T7 | junk inserted before the block | tail-only green, base guard red | `tail-only: rc=0`; `FAIL base front.md file_lines=7 != pre_lines=3 + declared_lines=3`; clean guard `rc=0` |
| T8 | block ending with a blank line (r37 README shape) | ok, 4 declared lines | `OK front.md lines=4 …`, `tail -n 4` byte-identical to the block |

The selftest's own `FAIL` lines for the two mutation cases, exactly as printed (the `--root` run, so
`file_lines` counts the 152-line `PROVINCE.md` copy plus the 3-line block):

```text
  FAIL front.md lines=3 want=0dd57cebe6d4f2dd3c16764174e390d8accb638ed7e0c6d71f4ed228280008cb got=9c79b88c88dc8b2eb3f3c7bae71d6564e667a49c65aa67f08e075c2dbc9391eb file_lines=155
  FAIL front.md lines=3 want=0dd57cebe6d4f2dd3c16764174e390d8accb638ed7e0c6d71f4ed228280008cb got=2a4c71d4d15e51e01f61c2e77c9d2b53f1a7a24761e03e20f9d73f577efd6b6b file_lines=156
```

T7's pair and T6's six `FAIL` lines are quoted verbatim above; `gen`/`check` run there as separate
processes exactly as the selftest runs them.

## 8. Integration notes for G1 (not done here — the suite is another seat's file)

1. **Landing.** `corpus/instruments/declared-blocks.sh` (any name — messages use `${0##*/}`) or
   `.ufo/waves/round-38/declared-blocks.sh`; the file is path-agnostic and writes nothing but its
   TMPDIR scratch.
2. **Invocation from `r38-closure.sh` export mode**, after extraction to `$EXPORT`:
   `bash "$EXPORT/corpus/instruments/declared-blocks.sh" check "$EXPORT/.ufo/waves/round-38/declared-blocks.txt" --root "$EXPORT"`.
   It exits 0 only when every declared suffix matches (and every optional base guard holds).
3. **Inline equivalent** if G1 prefers no second file — the whole required assertion is
   `want=$(awk -v p="$path" '$1==p {print $3}' "$list"); got=$(tail -n "$lines" -- "$root/$path" | sha256sum | awk '{print $1; exit}'); [ "$got" = "$want" ]`,
   plus the guards that stop the check from being vacuous: list non-empty, one declaration per path,
   64 lowercase hex, positive integer, `tail` output non-empty. Those are the parts this helper adds.
4. **One declaration per file.** If the round appends twice to one file (a `Correction (round 38)`
   paragraph and a block), concatenate the blocks in the order they were appended into one block file
   and declare that: two overlapping suffixes cannot both be "the append", and the checker rejects the
   duplicate instead of guessing.
5. **Base guard is optional and only for last appends.** Do not add `# base` for a file that will be
   appended to again after the declared block, or the guard goes red on a legal later append.
   `gen` prints the guard line it would emit on stderr; nothing is added to stdout.
6. **Fence-state-at-EOF is not this contract's limb.** G1 also requires the fence state to be closed at
   EOF; that is a separate check (another seat's `ExecFenceWalk` evidence). This helper asserts bytes
   of the appended suffix only.
7. **Boundary with the r37 numbers.** §5 and §6 pin *which bytes* `cdfe44e3…`/`2ebd8cd2…` cover, so a
   later claim that the r37 blocks "match their declared digests" can be checked without re-deriving the
   fence math. The r38 declarations themselves must be produced by `gen` from the round-38 block files
   once they exist; nothing here pre-computes them.

## 9. Out of scope, tooling, cleanup

* Out of scope and untouched: `PROVINCE.md`, `corpus/README.md`, `declared-blocks.txt` (absent),
  `corpus/instruments/r38-closure.sh`, SCORECARD/SHONEN/LOG/LESSON, all round-38 C2 artifacts, sibling
  seats' deliverables.
* No network fetch by this seat; no tool install or upgrade; no pacman invocation.
* Scratch `/fast/scratch/hyaku/kasegi-r38/ExecDeclaredBlocks` (`mirror/`, `ev/`, `evidence.sh`,
  `evidence.log`, probe files) removed after this receipt and the helper were written; the only retained
  artifacts are `.ufo/waves/round-38/wave1/ExecDeclaredBlocks.gen.sh` and this receipt.
