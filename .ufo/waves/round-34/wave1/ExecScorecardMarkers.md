# ExecScorecardMarkers — round 34, wave 1 (R1)

Seat: `ExecScorecardMarkers` (leaf). Scope: fix routed defect **R1** from
`corpus/lessons/round-33-verifier-spotcheck.md` §5 — `SCORECARD.md` carried two
`<LANE_HASH>` placeholders. Assigned path: `SCORECARD.md` only. No other file written.
No git/jj mutation, no subagent, no scratch tree created (no fixture needed; nothing to delete).
No tool installed or upgraded.

## Report

### 1. Before measurement (unmodified worktree state at seat start)

```
$ grep -n '<LANE_HASH>' SCORECARD.md
988:`<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the
1087:**Round-33 final lane commit: `<LANE_HASH>`** — the L1 replaces this marker. Every value in
exit=0
$ grep -c '<LANE_HASH>' SCORECARD.md
2
$ sha256sum SCORECARD.md
e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3  SCORECARD.md
```

Both markers matched the R1 citation (`:988`, `:1087`) exactly. Matches the frozen before-value
`SCORECARD.md carries 2 <LANE_HASH> markers (R1)` in `.ufo/waves/round-34/claims.json`.

Hash confirmation (the value substituted) — resolved in this repo, not copied from prose:

```
$ git rev-parse --verify '7963976e60b2564860553c6ab4838128d5ca06ea^{commit}'
7963976e60b2564860553c6ab4838128d5ca06ea
$ git log --format='%H %ci %s' -5
206e5108f1190e61b3e2622d21cab8a5d921650c 2026-10-26 02:29:48 -0300 round-34: wave-1 spec (65 seats, v2 policy), validated plan and dispatch
29f606dbdd28aff6fd4573ab4b90788bbb90af13 2026-10-26 02:28:39 -0300 round-34: freeze claims C1/C2 with do-nothing controls, census-before, assimilation guard prep
014ee2d7aa8c3c095ff57ae51097606a9906228c 2026-10-26 02:23:13 -0300 round-33 verifier spot-check (integrator, hyaku): non-author admit/reject
7963976e60b2564860553c6ab4838128d5ca06ea 2026-10-26 02:03:32 -0300 round-33: remaining wave-1 receipts (final 12 seats)
5b7a039e35ebde2676253bc8fc18984bcaad4837 2026-10-26 02:02:52 -0300 round-33: closure — scorecard, SHONEN, lesson (placeholders filled), LOG r33, wave results, final receipts
```

`7963976e…` is the round-33 final lane commit; `014ee2d7…` is the verifier spot-check commit that
sits on top of it and is the round-34 lane base. Both facts are named in the appended correction.

### 2. Edits (two marker replacements + one appended correction)

Edit 1 — `SCORECARD.md:988` (round-33 preamble, "Final lane commit:"):

- removed: `` `<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the ``
- now: `` `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1); the wave-1 value above ``
- the continuation line `is the commit the after-column seats measured, not the closing commit.`
  is unchanged in meaning; only the wrap moved ("the" moved to the previous line).

Edit 2 — `SCORECARD.md:1087` (closing line) → now line 1110 after the sibling R2 insert:

```
**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1). Every value in
```

Edit 3 — appended at the end of the round-33 section (end of file), verbatim:

```
Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
final hash `7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7aa8c3c095ff57ae51097606a9906228c`
after the verifier spot-check commit); the placeholder token no longer occurs in this file, and
the round-34 closure check R1 reads that count as 0.
```

**Deliberate deviation from the dispatch template (disclosed):** the quoted template said
"the two `<LANE_HASH>` placeholders above were replaced with…". Putting that literal token in the
correction would leave one occurrence in the file and break the frozen kill rule
(`<LANE_HASH> still present in SCORECARD.md`) and the counting command
`grep -c '<LANE_HASH>' SCORECARD.md -> 0`. The correction therefore says "lane-hash placeholders".
No other wording was changed; the prefix is exactly `Correction (round 34):` so a closure check
can match it literally, and `R1`, `7963976e…` and `014ee2d7…` are all present.

### 3. After measurement (my edit, before the sibling R2 insert)

```
$ grep -c '<LANE_HASH>' SCORECARD.md
0
grep_exit=1
$ grep -n 'Correction (round 34)' SCORECARD.md
1093:Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
$ grep -c '7963976e60b2564860553c6ab4838128d5ca06ea' SCORECARD.md
3
$ grep -c '014ee2d7aa8c3c095ff57ae51097606a9906228c' SCORECARD.md
1
$ sha256sum SCORECARD.md
442557130f6c890a285489e11b0fe4c8c93acc8713b10debe9a7a15ce39cf9b6  SCORECARD.md
$ git diff --numstat -- SCORECARD.md
8	3	SCORECARD.md
```

`git diff` for my change touches exactly two hunks: `@@ -985,8 +985,8 @@` (preamble marker) and
`@@ -1084,8 +1084,13 @@` (closing marker + correction). No other line in the file changed.

### 4. Integrated state after the concurrent R2 append (sibling seat `ExecErratum2`)

`ExecErratum2` announced it would insert an "Erratum 2" block above my regions; we coordinated
by message (boundaries: it inserts between the Rule-B erratum paragraph and the "C1 blind spots"
paragraph; my three regions are position-independent and the file must end with my correction).
It landed the block at `SCORECARD.md:1014` (+23 lines). Re-measured on the integrated bytes:

```
$ grep -c '<LANE_HASH>' SCORECARD.md
0
exit=1
$ grep -n 'Correction (round 34)' SCORECARD.md
1116:Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
$ grep -n 'filled in round 34, R1' SCORECARD.md
988:`7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1); the wave-1 value above
1110:**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1). Every value in
$ sha256sum SCORECARD.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
$ wc -l SCORECARD.md
1119 SCORECARD.md
$ git diff --numstat -- SCORECARD.md
31	3	SCORECARD.md
```

`31 insertions / 3 deletions` = my 8/3 plus the sibling's 23/0. My tail region (marker line,
closing paragraph, correction) verified intact by raw read of `:1106-1119` after the insert; the
R1 predicates (`grep -c` = 0, correction line present, both full hashes present) hold on the
integrated bytes. **Digest caveat:** the integrated digest `b8fc8c66…` is a moving target while
wave 1 is in flight; the R1 counter does not read the digest, and the two marker lines are
positional only in this receipt, never in the check.

### 5. Constraints honoured

- Wrote only `SCORECARD.md` (assigned) and this receipt. No `git add`/`commit`/`push`, no `jj`
  mutation; the L1 commits.
- Did not touch the fleet repo, sibling lanes, `/home/vgpnk/Projects/bounties` or `shokuknow`.
- No subagent, no wave dispatch, no `agent://all`. Peer messages sent: `ExecRDefectClosureSuite`
  (exact landed strings + suggested R1 predicate for `r-defect-closure.sh`; noted that
  `corpus/instruments/r-defect-closure.sh` did not exist yet at my check — `ls_exit=2`), and
  `ExecErratum2` (boundary ack for the concurrent SCORECARD.md insert).
- No scratch directory created, therefore none left on disk.

### 6. Residual references observed, left to the L1 (out of this seat's scope)

- `corpus/lessons/round-33.md:126` still states "Its two `<LANE_HASH>` markers are the L1's edit;
  this lesson does not verify the appended numbers…". That sentence now describes stale state
  (the markers are filled). R7 owns an erratum in that lesson; whether R7's append should also
  sweep this mention is the L1's call — I did not edit the lesson.
- `<LANE_HASH>` still occurs in historical `.ufo/waves/round-3{1,2,3}/*` dispatch/plan/results
  artifacts and in `corpus/lessons/round-33-verifier-spotcheck.md:165` (the R1 finding itself,
  quoted). Neither is read by the R1 counter (`grep -c … SCORECARD.md`); no historical artifact
  was modified.

### 7. Evidence summary

| Item | Value |
|---|---|
| markers before | 2 (`grep -c`, exit 0) at `:988`, `:1087` |
| markers after | 0 (`grep -c`, exit 1) — my edit and integrated |
| substituted hash (×3 in file) | `7963976e60b2564860553c6ab4838128d5ca06ea` |
| lane tip named in correction (×1) | `014ee2d7aa8c3c095ff57ae51097606a9906228c` |
| correction line | `SCORECARD.md:1093` (mine) / `:1116` (integrated), prefix `Correction (round 34):` |
| digest before | `e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3` |
| digest after my edit | `442557130f6c890a285489e11b0fe4c8c93acc8713b10debe9a7a15ce39cf9b6` |
| digest integrated (with R2) | `b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0` |
| diff numstat | mine `8 3`; integrated `31 3` |

R1 as assigned is **landed**: `grep -c '<LANE_HASH>' SCORECARD.md` → 0 plus an appended
correction naming the round-33 final hash and the lane tip. I do not run the round gate
(`r-defect-closure.sh`) or judge the round; that is the L1's post-integration step.
