# C1LineNumberIntegrity — wave-2 falsification of FixRecheckLines.md (round 25)

Seat: `L1Kasegi25.C1LineNumberIntegrity` (read-only scout). Lane root:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, HEAD = `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`
(the claim's `base_revision`; no C1 commit exists, so "before" = HEAD bytes, "after" = worktree bytes).
No VCS write, no spawn, no install (bash/git/python3/diff already present). Attack target:
`.ufo/waves/round-25/wave1/FixRecheckLines.md` — "29 edits, one line each", "no line added, dropped
or moved", "no cited line number moved" (anchorcheck byte-identical).

## Verdict: CONFIRMED (wave-1 result stands; no correction needed)

All four sub-claims reproduce exactly:

1. **29 edits** — `git diff --numstat -- corpus/knowledge` = 29 rows, every row `1 1` (non-`1 1` count = 0).
2. **One-line-for-one-line, in place** — stronger than numstat: all 29 hunks are `@@ -N +N @@`
   with identical old/new offsets and no count field (`grep -cE '^@@ -[0-9]+ \+[0-9]+ @@'` = 29;
   position/count mismatches = 0). Per-file `diff <(git show HEAD:$f) $f` yields exactly one
   `NcN` change block per file, nothing else (`files_not_1c1=0`). No delete+reinsert at a
   different position anywhere — so no line number can have moved.
3. **Only `recheck:` lines** — diff body has 29 `-recheck:` + 29 `+recheck:` and **zero** other
   changed lines (`grep -E '^[+-]' | grep -vE '^(--- |\+\+\+ |[+-]recheck:)'` = 0).
   Transformation equivalence re-derived by parsing the diff (not trusting the receipt):
   23 `on-restoration — <CMD> (<NOTE>)` → `cd <lane> && <CMD>  # on-restoration — <NOTE>`
   (CMD/NOTE verbatim) + 6 plain lines → `cd <lane> && ` prefixed verbatim; `mismatch=0`.
4. **No cited line number moved** — replicated the wave-1 method (`git archive HEAD` → /tmp, run
   the *extracted* tree's own `anchorcheck.py` from its root vs worktree copy, compare byte-wise)
   extended from 1 file (report) to **all 29**: outputs byte-identical for every file, including
   every `md:NNN` anchor number. `anchorcheck_29_identical_fail=0`.

Supporting counts: 37 files carry `^recheck:` = 29 changed + 6 byte-identical conformers
(report's named six verified `git diff --quiet HEAD` clean) + 2 untracked C2 files
(`vendor-disclosure-*.md`). Report's 29-file list = `git diff --name-only` output exactly
(`FILE_LISTS_IDENTICAL`).

## Commands / outputs / exits (all run 2026-10-25, lane root unless noted)

```
$ git diff --numstat -- corpus/knowledge | wc -l ; git diff --numstat -- corpus/knowledge | awk '$1!=1||$2!=1' | wc -l
29
0                                                          # exit 0

$ git diff -U0 -- corpus/knowledge > /tmp/c1-ck.diff
$ grep -c '^@@' /tmp/c1-ck.diff ; grep -c '^-recheck:' /tmp/c1-ck.diff ; grep -c '^+recheck:' /tmp/c1-ck.diff
29
29
29
$ grep -E '^[+-]' /tmp/c1-ck.diff | grep -vE '^(--- |\+\+\+ |[+-]recheck:)' | wc -l
0
$ grep -cE '^@@ -[0-9]+ \+[0-9]+ @@' /tmp/c1-ck.diff
29
$ grep -E '^@@' /tmp/c1-ck.diff | sed -E 's/^@@ -([0-9]+)(,([0-9]+))? \+([0-9]+)(,([0-9]+))? @@.*/\1|\3|\4|\6/' | awk -F'|' '{if($1!=$3||$2!=""||$4!="")m++} END{print "hunks="NR" mismatches="(m+0)}'
hunks=29 mismatches=0

$ for f in $(git diff --name-only -- corpus/knowledge); do diff <(git show HEAD:$f) $f; done \
    | (count NcN blocks per file)      # files_not_1c1=0; every block flanked by '< recheck:'/'>' recheck:' only

$ python3 (pair each -recheck with its +recheck; verify verbatim CMD/NOTE or verbatim body)
on_restoration_rewrites=23 plain_prefixes=6 mismatch=0 total_pairs=29
plus_lines_with_comment_marker= 23

$ git archive HEAD | tar -x -C /tmp/c1-head2
$ for f in <29 files>: (cd /tmp/c1-head2 && python3 corpus/instruments/anchorcheck.py $f) vs
                       (cd <lane> && python3 corpus/instruments/anchorcheck.py $f); cmp -s
anchorcheck_29_identical_fail=0          # every pair byte-identical

$ for the six claimed-untouched files: git diff --quiet HEAD -- <f> && echo UNCHANGED
all six UNCHANGED

$ sort(report's 29 names) vs git diff --name-only -- corpus/knowledge | sort
FILE_LISTS_IDENTICAL
$ grep -l '^recheck:' corpus/knowledge/*.md | wc -l
37
```

## Methodology caveat (self-corrected during attack)

A naive anchorcheck comparison — extracted only the 29 files into `/tmp` and invoked the lane's own
script on them — produced `BASE-ABSENT` differences vs the worktree. That was an artifact: the tool
resolves anchor pins against the **lane root of the tree it runs in**, so a 29-file partial tree
lacks the pins and falls back to the absent `the-bounty-hunter` base. Replicating the wave-1 method
exactly (`git archive HEAD` full tree, run `/tmp/c1-head2/corpus/instruments/anchorcheck.py` from
`/tmp/c1-head2` as cwd) gives byte-identical output for all 29 files. The wave-1 report's method was
correct; its single-file sample is now strengthened to 29/29.

## Minor observations (not falsifications)

- `git status --porcelain -- corpus/knowledge | wc -l` now = 31 (29 `M` + 2 `??` C2 files), vs the
  report's `= 29, all M` — written before C2's two untracked files landed. Stale-by-design, not wrong
  for its timestamp; the `git diff` scope it claims remains exact.
- The claim "no cited line number moved" is proven *structurally* (29 single-line in-place swaps at
  identical offsets) and *instrumentally* (anchorcheck byte-identical, all 29 files). Both agree.

## Tooling record

No installs/upgrades; used system `git`, `bash`, `diff`, `grep`, `sed`, `awk`, `python3`, `tar`.
