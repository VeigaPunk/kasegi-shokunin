# ExecFenceWalk — round 38, G1 CommonMark fence walk

Seat: ExecFenceWalk (leaf executor). Item: implement and test the CommonMark fence walk used by gate
G1 as a standalone bash function, deliver it at
`.ufo/waves/round-38/wave1/ExecFenceWalk.sh`.

## Deliverable

| property | value |
|---|---|
| path | `.ufo/waves/round-38/wave1/ExecFenceWalk.sh` |
| lines | 135 |
| bytes | 5118 |
| sha256 | `f5018c464afffe747785d8c8c9c89c1c83fc400749ecb0b5e997fbd9785c322d` |
| mode | `0755` (set by the write tool) |

Surface (the landable bytes are only the script; no notes are inside it beyond its header comment):

```
fence_walk FILE            -> prints `open` or `closed` at EOF
fence_walk FILE trace      -> per line: `<lineno> code|text` (code = line belongs to a fenced block)
ExecFenceWalk.sh FILE          state mode (exit 0; exit 2 if FILE unreadable; exit 1 on usage)
ExecFenceWalk.sh --trace FILE  trace mode
ExecFenceWalk.sh --selftest    built-in fixtures; exit 0 iff all pass
```

Semantics implemented (CommonMark 0.31.2 §4.5): a fence opens, when the walk is closed, on
`^ {0,3}(`{3,}|~{3,})` plus an optional info string (a backtick fence whose info string contains a
backtick is not a fence); while open, only a same-character run of at least the opener's length,
followed by nothing but spaces/tabs, closes it; 4+ spaces of indentation (or a leading tab) is never
a fence; EOF prints the state. The walker is a bash function (`fence_walk`) wrapping one awk program,
so the suite can source the file and call it directly.

## Test 1 — the six named cases (base export `a173b0c2…`, `git archive` into scratch)

Fixture commands (scratch `$S=/fast/scratch/hyaku/kasegi-r38/ExecFenceWalk`, `TMPDIR=$S`):

```sh
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive a173b0c2b98c5ae39599fa9be76027fbbead0b9e \
  | tar -x -C $S/base
printf '```text\ncontent line\n```\n'                 > fx/info-then-close.md
printf '````\ntext\n```text\nstill code\n````\nafter\n' > fx/nested-four.md
printf '    ```\nfour-space indented\n'                > fx/indented-four.md
cp base/corpus/README.md fx/readme-appended.md && printf '```\n' >> fx/readme-appended.md
for f in …; do printf '%s -> %s\n' "$f" "$(bash $W "$f")"; done
```

Actual output (`W=.ufo/waves/round-38/wave1/ExecFenceWalk.sh`):

```
base/PROVINCE.md -> closed
base/corpus/README.md -> open
fx/info-then-close.md -> closed
fx/nested-four.md -> closed
fx/indented-four.md -> closed
fx/readme-appended.md -> closed
```

Line-level facts behind the two base results (trace mode, selected lines):

```
$ bash $W --trace base/PROVINCE.md | awk 'NR==81||NR==96||NR==124'
81 code
96 code
124 code
```

`base/PROVINCE.md` is 152 lines; the round-37 D-A paste opens a fence at line 81 (` ``` `), line 96 is
` ```text ` **content inside that fence**, line 124 (` ``` `) closes it, and lines 125-152 are text,
so the file ends `closed`. A naive toggle over every line matching `^ {0,3}(`{3,}|~{3,})` counts 3
fences (`81`, `96`, `124`) and reports the wrong state (`open`); the walk is what G1 needs.

`base/corpus/README.md` is 454 lines with exactly one fence-ish line, the opener ` ``` ` at line 426,
so it ends `open` — every byte appended after it lands inside a code block. That is the base state the
round-37 D-A append inherited, and the reason G1 must read the *walk*, not a fingerprint count.

## Test 2 — reference renderer agreement (`cmark 0.31.2`, installed on the host, not by this seat)

Reference: `cmark --sourcepos FILE`, whose `<pre data-sourcepos="a:b-c:d">` ranges give the fenced
block line spans; a span is treated as fenced when its first line matches the opener pattern (this
excludes indented code blocks, which the walker does not model). EOF state from the reference is
`open` iff a fenced span reaches the last line and that last line is not a valid closer for it.
Agreement = same set of fenced lines **and** same EOF state.

```
$ cmark --version
cmark 0.31.2 - CommonMark converter
$ python3 cmp.py <files>
base/PROVINCE.md: lines=152 cmark_blocks=[(81, 124)] cmark_code_lines=44 walker_code_lines=44 cmark_state=closed walker_state=closed agreement=yes
base/corpus/README.md: lines=454 cmark_blocks=[(426, 454)] cmark_code_lines=29 walker_code_lines=29 cmark_state=open walker_state=open agreement=yes
fx/info-then-close.md: lines=3 cmark_blocks=[(1, 3)] cmark_code_lines=3 walker_code_lines=3 cmark_state=closed walker_state=closed agreement=yes
fx/nested-four.md: lines=6 cmark_blocks=[(1, 5)] cmark_code_lines=5 walker_code_lines=5 cmark_state=closed walker_state=closed agreement=yes
fx/indented-four.md: lines=2 cmark_blocks=[] cmark_code_lines=0 walker_code_lines=0 cmark_state=closed walker_state=closed agreement=yes
fx/readme-appended.md: lines=455 cmark_blocks=[(426, 455)] cmark_code_lines=30 walker_code_lines=30 cmark_state=closed walker_state=closed agreement=yes
```

Adversarial extras compared the same way (all `agreement=yes`):

```
fx/backtick-info.md: lines=2 cmark_blocks=[] cmark_code_lines=0 walker_code_lines=0 cmark_state=closed walker_state=closed agreement=yes
fx/tilde-inner-backtick.md: lines=4 cmark_blocks=[(1, 4)] cmark_code_lines=4 walker_code_lines=4 cmark_state=closed walker_state=closed agreement=yes
fx/indent-open-close.md: lines=4 cmark_blocks=[(1, 3)] cmark_code_lines=3 walker_code_lines=3 cmark_state=closed walker_state=closed agreement=yes
```

(`fx/backtick-info.md` = ` ```a`b ` — CommonMark rejects a backtick fence whose info string holds a
backtick, so neither side opens a block. `fx/tilde-inner-backtick.md` = `~~~` / ` ``` ` / … / `~~~` —
the backtick line is content. `fx/indent-open-close.md` — 2-space opener, 3-space closer, both legal.)

Reference agreement: **9/9 files, on both the fenced-line set and the EOF state.**

## Test 3 — built-in selftest

```
$ bash $W --selftest
case=info-string-then-close expected=closed observed=closed verdict=pass
case=unclosed-at-eof expected=open observed=open verdict=pass
case=nested-four-backtick expected=closed observed=closed verdict=pass
case=nested-four-all-code expected=4 observed=4 verdict=pass
case=indented-four-space expected=closed observed=closed verdict=pass
case=tilde-fence expected=closed observed=closed verdict=pass
case=tilde-not-closed-by-backtick expected=closed observed=closed verdict=pass
case=tilde-backtick-line-is-content expected=3 observed=3 verdict=pass
case=backtick-in-info-string expected=closed observed=closed verdict=pass
case=appended-closer-closes expected=closed observed=closed verdict=pass
selftest cases=10 failures=0
exit=0
```

The two `expected=4` / `expected=3` rows assert the *line classification*, not just the EOF state: in
the 4-backtick fixture all four lines (opener, 3-backtick line, ` ```text ` line, 4-backtick closer)
must be code, and in the tilde fixture the embedded ` ``` ` line must be code.

## Notes for the gate

- G1 can call `fence_walk "$file"` after sourcing, or `bash …/ExecFenceWalk.sh "$file"`, and require
  `closed`. To prove an appended block is not swallowed, `--trace` gives the per-line classification.
- Base state for the two front-door files: `PROVINCE.md` = `closed` (the D-A paste is self-contained at
  81-124), `corpus/README.md` = `open` at 426. G1's `closed` assertion on README therefore depends on
  the round-38 correction closing that fence; the walker will show `closed` only then.
- No tool was installed, upgraded or removed by this seat; `cmark` 0.31.2 was already on the host
  (`/usr/bin/cmark`) and was used read-only. No pacman invocation. No network fetch.
- No lane file outside the wave dir was written or edited; the base tree was read through
  `git archive` into scratch. No git/jj mutating command was run (no fixture repo either).

## Scratch

`/fast/scratch/hyaku/kasegi-r38/ExecFenceWalk/` (base export, `fx/`, `cmp.py`) was removed after this
receipt and the deliverable were in place; `ls -d` on it fails after removal.
