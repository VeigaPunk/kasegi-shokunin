# ExecErratum2 — round-34 wave-1 receipt (R2)

Seat: ExecErratum2 (leaf executor), lane `kasegi-shokunin`, round 34, base `014ee2d7aa8c3c095ff57ae51097606a9906228c`.
Assigned: **R2** — append an "erratum 2" block to the `SCORECARD.md` round-33 section restating the
frozen kill-rule parenthetical per id and recording the pre-freeze satisfiability step.

## Report

### Scope

Only `SCORECARD.md` was written (one append-only insertion; no line of the existing file was
reworded or removed). No other lane file, no fleet repo, no shokuknow, no git/jj mutation.
No tools installed; no package-manager transaction.

### Pre-state

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum SCORECARD.md
442557130f6c890a285489e11b0fe4c8c93acc8713b10debe9a7a15ce39cf9b6  SCORECARD.md   # 1096 lines
$ git show 014ee2d7aa8c3c095ff57ae51097606a9906228c:SCORECARD.md | sha256sum
e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3  -   # 1091 lines (lane base blob)
$ grep -c 'erratum 2' SCORECARD.md ; echo "exit=$?"
0
exit=1
```

The 1096-line pre-state already carried `ExecScorecardMarkers`' uncommitted R1 edit (two
`<LANE_HASH>` → `7963976e60b2564860553c6ab4838128d5ca06ea` replacements + trailing `Correction (round 34)`
paragraph). That seat was messaged before my write and acked it had finished editing; it asked only
that its two replacements stay intact and that the file still end with its Correction paragraph.

### Insert location and shape

Inserted between the round-33 `**Rule-B erratum, disclosed (post-freeze, round-25 form).**` paragraph's
last line (`SCORECARD.md:1012`, "...not the literal one.") and `**C1 blind spots, recorded (not filed as
failures).**` (now `:1037`). New block: `SCORECARD.md:1014-1035`, with the blank separator at `:1036`.
Unique anchor used: the paragraph-ending line plus the following blank line plus the `C1 blind spots`
heading.

```
$ diff -u /fast/scratch/hyaku/kasegi-r34/ExecErratum2/SCORECARD.before.md SCORECARD.md > append.diff; echo "diff_exit=$?"
diff_exit=1                      # files differ, expected
$ grep -c '^+[^+]' append.diff ; grep -c '^-[^-]' append.diff
21                               # non-blank added lines
0                                # no removed lines at all
```

The block is 23 physical lines: 21 non-blank lines + 1 blank line between its two paragraphs + the
trailing blank separator before the `C1 blind spots` heading. **0 deletions** attributable to this seat.

### Post-state evidence (measured 2026-10-26T05:31–05:33Z)

```
$ sha256sum SCORECARD.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
$ wc -l SCORECARD.md
1119 SCORECARD.md                 # 1096 pre-state + 23 inserted
$ cat SCORECARD.md:1014-1035 | md5sum
9b413f415be0851a0cd00f86363a0315  -   # digests the inserted block bytes
$ grep -n 'Erratum 2\|erratum 2' SCORECARD.md
1014:**Erratum 2, disclosed (round-34 append, round-25 form).** The frozen C1 kill-rule
1033:had carried since round 24, which is why erratum 1 and this erratum 2 had to be filed after
$ grep -n '0 or 2+ matches = failure\|multi_row_url=N\|dup-id\|QUALITY R22\|pre-freeze satisfiability' SCORECARD.md
1016:not globally. `"0 or 2+ matches = failure"` applies within a single record's own id scope: it
1019:rows is informational (`multi_row_url=N`) and does not fail rule B; two rows carrying the same id
1020:**do** fail, and the instrument names that `dup-id`. At the landed bytes `multi_row_url=2` is
1028:**Pre-freeze satisfiability step, recorded (QUALITY R22).** Before any claim is frozen, each
$ grep -c '<LANE_HASH>' SCORECARD.md ; echo "exit=$?"
0
exit=1
$ grep -n 'Correction (round 34' SCORECARD.md
1116:Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
$ grep -n '7963976e60b2564860553c6ab4838128d5ca06ea' SCORECARD.md
988:... (filled in round 34, R1); ...            # sibling's first replacement, intact
1110:**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1). ...
1117:final hash `7963976e...` (lane tip `014ee2d...`   # inside sibling's Correction paragraph
$ git diff --numstat -- SCORECARD.md
31	3	SCORECARD.md     # the 3 deletions are the sibling's three placeholder lines, not this seat's
```

The file still ends with the sibling's Correction paragraph (tail lines `1116-1119`), and both of its
marker replacements are byte-intact; my block sits above both.

### R22 dependency (cross-seat, read-only)

```
$ grep -c '^| R22 ' corpus/QUALITY.md ; echo "exit=$?"
1
exit=0
$ sha256sum corpus/QUALITY.md
eb20eafc6aabc312ba46fe7214860590098aef4f7664064de4a7c888653dc8cb  corpus/QUALITY.md   # 227 lines
```

`ExecQualityAppends` landed R22 (`corpus/QUALITY.md:222`) during my window; its text ("every literal
constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable
literal is fixed before data, never waived by a post-freeze erratum") is the criterion my block names,
and its own grounding cites "SCORECARD round-33 section, erratum 2" back. So the R2 closure limb
"pre-freeze satisfiability step is recorded (QUALITY R22 row exists)" has both halves on disk.

### Appended block (verbatim, `SCORECARD.md:1014-1035`)

```text
**Erratum 2, disclosed (round-34 append, round-25 form).** The frozen C1 kill-rule
parenthetical above — a `url` that greps to "0 or 2+ matches" is a failure — is scoped **per id**,
not globally. `"0 or 2+ matches = failure"` applies within a single record's own id scope: it
reads that record's own `corpus/SOURCES.md` row, so a hit count of zero or two-or-more is about
that one row's id token, not a whole-file or whole-registry count. A URL shared by two *different*
rows is informational (`multi_row_url=N`) and does not fail rule B; two rows carrying the same id
**do** fail, and the instrument names that `dup-id`. At the landed bytes `multi_row_url=2` is
exactly the two manifest records S029 and S006 (their URLs are also the S024 and S028 rows'
URLs), so the global reading would fail both and leave `bound=38` of 40 records, while the per-id
reading binds `records=40 bound=40 unbound=0`. The landed selftest pins both directions
(`case_duplicate_id_rows`, `case_shared_url_passes`). Erratum 1 remains the correction of record
for the round-33 counters; this block restates its reading in the kill rule's own words so the
frozen sentence and the measured reading no longer diverge on their face.

**Pre-freeze satisfiability step, recorded (QUALITY R22).** Before any claim is frozen, each
literal constant and regex in its predicate and kill rule is evaluated against the base bytes for
satisfiability. A literal that is unsatisfiable at base is corrected **before** dispatch, never
waived by a post-freeze erratum. Round 33 froze C1 with two such literals — "exactly one
registry-row URL" and "0 or 2+ matches" — both false against the two shared-URL pairs the registry
had carried since round 24, which is why erratum 1 and this erratum 2 had to be filed after
dispatch. `corpus/QUALITY.md` R22 is the appended criterion, grounded in the routed R2 defect
(`corpus/lessons/round-33-verifier-spotcheck.md` §5 R2) and mistake M34-2.
```

Facts quoted in the block are read from committed receipts, not re-measured here:
`multi_row_url=2` / S029 / S006 (`.ufo/waves/round-33/wave1/CritC1Kill.md:123,209`; the landed
`AUDIT` line already in this scorecard), the `bound=38` global reading
(`corpus/lessons/round-33-verifier-spotcheck.md:167-169` R2 — "the frozen parenthetical that literally
read `bound=38`", now also quoted by QUALITY R22's grounding cell), and the selftest case names
(`capture-binding-check.py --selftest`, round-33 capability row).

### Scratch

```
$ rm -rf /fast/scratch/hyaku/kasegi-r34/ExecErratum2 && test -e /fast/scratch/hyaku/kasegi-r34/ExecErratum2; echo "exists_exit=$?"
exists_exit=1                    # tree removed; before/after copies and the diff were scratch-only
```

## Findings

- **R2 is landed**: the erratum-2 block is in the round-33 section at `SCORECARD.md:1014-1035`, pure
  insertion (0 deletions), digest `b8fc8c66…`, and it states both required claims — the per-id scope of
  `"0 or 2+ matches = failure"` (shared URL = informational `multi_row_url=N`, same-id rows = `dup-id`)
  and the pre-freeze satisfiability step pointing at QUALITY R22.
- **Verdict: no score move claimed by this seat** (C1's held-4 verdict is the L1's read).

## Risks / open items

1. `corpus/instruments/r-defect-closure.sh` did not exist at measurement time
   (`ls corpus/instruments/r-defect-closure.sh` → `No such file or directory`, exit 2), so I could not
   read or run its R2 check. The block carries the token set the task's R2 description names
   (`erratum 2`, "per id", `0 or 2+ matches`, `multi_row_url=N`, `dup-id`, "pre-freeze satisfiability",
   `QUALITY R22`); if the landed suite keys on different literal wording, that is an integration read
   for the L1, and the wording here is the one the frozen claims sentence uses.
2. The R2 check's second limb requires the QUALITY R22 row to exist; it does at
   `corpus/QUALITY.md:222` (digest `eb20eafc…`), landed by another seat during this wave.
3. `SCORECARD.md` was co-dirty when I edited it (`ExecScorecardMarkers`' R1 edit). My insert shifts that
   seat's later anchors by +23 lines (closing marker 1087 → 1110, Correction paragraph 1093-1096 →
   1116-1119). I re-verified both `7963976e…` replacements and the trailing Correction paragraph after my
   write; the seat was messaged with the integrated digest `b8fc8c66…`, `<LANE_HASH>` count 0, and
   `grep -n 'Correction (round 34'` → `1116`.
