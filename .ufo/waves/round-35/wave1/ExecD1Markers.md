# ExecD1Markers — D1 closure (SCORECARD.md lane-commit placeholders)

Seat: ExecD1Markers (leaf). Lane: `kasegi-shokunin`, round 35. Base `3266c9937b03062d9bbc2f436e20820115ed179c`,
claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
Scope: `SCORECARD.md` round-34 section only (D1 of `corpus/lessons/round-34-verifier-spotcheck.md` §6).

## Report

### 1. Defect as routed and as found

`round-34-verifier-spotcheck.md` §6 D1: two unfilled lane-commit placeholders at slot `SCORECARD.md:1129`
(preamble of the round-34 section) and `SCORECARD.md:1240` (closing paragraph of that section), both
"still unfilled at `c1c6a5f`". Re-measured on the base tree before any edit — two sites, one spelling
each, plus no other placeholder family:

```
$ for p in 'the L1 fills' 'fills this line' 'L1 replaces' '<LANE_HASH>' 'filled by the L1'; do printf '%-22s %s\n' "$p" "$(grep -c -- "$p" SCORECARD.md)"; done
the L1 fills           1
fills this line        1
L1 replaces            0
<LANE_HASH>            0
filled by the L1       1
$ grep -n 'the L1 fills\|L1 replaces\|<LANE_HASH>' SCORECARD.md
1129:`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit: the L1 fills this line in the
```

So the `filled by the L1` literal occurred on **1** line (1240) and its sibling spelling on **1** line
(1129). Base digests: `sha256(SCORECARD.md)` = `efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91`,
1243 lines. `grep -c 'c1c6a5f' SCORECARD.md` = 0 (exit 1).

### 2. Edits applied (content-addressed `edit` only; no `write`, no VCS mutation)

**(a) Preamble site, `SCORECARD.md:1129-1130`.** The placeholder clause and the two clauses that the
substitution falsifies were replaced; every other word of the paragraph is unchanged (proof in §3):

```
BASE: **Final lane commit: the L1 fills this line in the closing commit.** This section is written at the
      wave-1 integration state on the bytes digested under § Measurement state, claims no lane-commit hash,
      and deliberately introduces no placeholder token — round-33 R1's defect was a published placeholder,
      the C1 counter reads that count as 0, and nothing here moves it.
CUR : **Final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1). This section
      is written at the wave-1 integration state on the bytes digested under § Measurement state and
      originally carried the placeholder prose this hash replaces; round-33 R1's defect recurred here in
      sentence form, which the round-34 R1 check missed because it matched only the angle-bracket lane-hash
      marker, not this prose form — the round-35 correction note at the end of this section records the
      substitution.
```

Why the second clause had to move with the first: "claims no lane-commit hash" and "deliberately
introduces no placeholder token" become literally false the moment the hash is inserted, and leaving
them would re-publish exactly the stale-prose class D1 is filed under. The replacement keeps the
historically true parts (wave-1 integration state, R1/published-placeholder recurrence) and attributes
the miss to the spelling-brittle check, which is the spotcheck's own diagnosis ("the R1 marker check
only matches the `<LANE_HASH>` spelling"). Everything from "Receipts land" to the end of the paragraph
is byte-identical to base.

**(b) Closing paragraph, `SCORECARD.md:1241`.**

```
BASE: **Round-34 final lane commit: filled by the L1 in the closing commit.** Every value in this section
CUR : **Round-34 final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1).
```

**(c) Appended one correction paragraph at the end of the round-34 section (current `SCORECARD.md:1258-1261`,
the last paragraph of that section):**

```
Correction (round 35): the two lane-commit placeholder sentences above (the preamble's and the closing
paragraph's) were replaced with the round-34 final lane hash `c1c6a5f826d2425446347173de527c42991b78b0`
(the round-34 lane tip at its non-author closure). Neither placeholder spelling occurs in this file any
more; the round-35 closure check reads that count as 0. Nothing else in this section changed.
```

The correction describes the two removed sentences instead of quoting them: the frozen counting command
is `grep -c 'filled by the L1' SCORECARD.md -> 0` (`claims.json` C1 `counting_commands[2]`; instrument
`corpus/instruments/r35-defect-closure.sh:135-137`), so a correction that reprinted the literal would
keep the count at 1 and fail the very check it satisfies. Same choice as the round-34 correction of
record for round 33 (`SCORECARD.md:1116`, "the placeholder token no longer occurs in this file").
The assignment's own prescribed wording ("the 'filled by the L1' placeholders above were replaced …")
was therefore paraphrased — flagged in §6 as the one deliberate deviation.

**(d) Pure wrapping.** Inserted text is longer than the replaced clause, so lines `1129-1140` and
`1241-1244` were re-wrapped to the file's ~100-column convention. Whitespace only; §3 proves the word
stream is preserved.

### 3. Append-only proof (word-stream comparison, not eyeball)

```
$ python3  # normalise whitespace of the round-34 preamble paragraph, base blob vs working tree
suffix-identical: True | suffix-len 570
```

i.e. the 570-character tail from "Receipts land under" to the paragraph's "(C2)." is character-identical
to base, and the only changed region is the placeholder clause quoted in §2(a).

Whole-file scope check — exactly two hunks, both mine by attribution:

```
$ git diff --stat 3266c9937b03062d9bbc2f436e20820115ed179c -- SCORECARD.md
 SCORECARD.md | 48 +++++++++++++++++++++++++++++++++---------------
 1 file changed, 33 insertions(+), 15 deletions(-)
$ git diff -U0 <base> -- SCORECARD.md | grep -E '^@@'
@@ -1129,11 +1129,12 @@ together with the do-nothing controls committed at the freeze
@@ -1240,4 +1241,21 @@ at 4 the lowest-axis obligation stays active, and the C1 blind spots above are t
```

Every deleted line lies inside those two hunks, i.e. inside the two placeholder paragraphs this seat
replaced (11 old lines at `1129-1139`, 4 at `1240-1243`); there is no `-` line anywhere else in the
file, which is the append-only proof for the rest of the document. The sibling round-35 paragraphs
that share the final section (`ExecD2DensityRow`'s `Erratum (round 35)` block at `:1246-1256`) are
insert-only from that seat and are **not** attributed to this one. No table row, no C1/C2
after-column, no other section of `SCORECARD.md` was touched.

### 4. Acceptance checks (final tree, after all peer writes to the file)

```
$ grep -c -- 'filled by the L1' SCORECARD.md
0
exit=1
$ grep -c -- 'the L1 fills' SCORECARD.md
0
exit=1
$ grep -c -- '<LANE_HASH>' SCORECARD.md
0
exit=1
$ grep -c -- 'L1 replaces' SCORECARD.md
0
exit=1
$ grep -c -- 'c1c6a5f' SCORECARD.md
3
exit=0
$ grep -c -- 'Correction (round 35)' SCORECARD.md
1
exit=0
$ sha256sum SCORECARD.md
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md
exit=0
$ wc -l SCORECARD.md
1261 SCORECARD.md
exit=0
```

`grep -c` exits 1 on a zero count: the two placeholder spellings are gone (count 0, exit 1 is the
expected-pass shape for a `-> 0` assertion) and `c1c6a5f` appears on 3 lines — `:1130` (preamble
replacement), `:1241` (closing replacement), `:1259` (correction paragraph) — i.e. `>= 1` at three
independent named locations.

The landed instrument's own predicate reads exactly these two numbers
(`corpus/instruments/r35-defect-closure.sh:130-140`: `placeholders=0,correction-c1c6a5f>=1`, exit 0),
so this seat's tree satisfies D1 without invoking the peer-owned suite (see §5).

Hash provenance (`git cat-file`, read-only):

```
$ git cat-file -e c1c6a5f826d2425446347173de527c42991b78b0^{commit} && echo cat-file-ok
cat-file-ok
$ git log -1 --format='%H%n%an%n%ad' c1c6a5f826d2425446347173de527c42991b78b0
c1c6a5f826d2425446347173de527c42991b78b0
kasegi-shokunin
Mon Oct 26 03:19:01 2026 -0300
```

It is the round-34 lane tip at its non-author closure, as the spotcheck states ("Lane tip:
`c1c6a5f826d2425446347173de527c42991b78b0` (branch `master`)") — not a closing value invented here.

### 5. What this seat deliberately did not do

- Did not run `corpus/instruments/r35-defect-closure.sh` (or its `--selftest`) although it is present as
  an untracked peer artifact: it belongs to the D-suite seat and is still in flight this wave; the C1
  claim's `closed=7/7` / `cases=7 failures=0` numbers are that seat's evidence, not this seat's. D1's
  predicate was verified by its own two `grep -c` commands plus a read of the check block.
- Did not touch `wave1-results.json`, `SKILL.md`, `corpus/`, the D2/D3/D4/D5/D6/D7 surfaces, or any
  file outside `SCORECARD.md`.
- Wrote no stash/commit/branch; the L1 commits.

### 6. Risks / disclosures (for the L1 to judge)

1. **Paraphrased correction vs the assignment's literal wording** (§2c). Required, because the frozen
   kill rule and counting command read the literal string, and the round-34 precedent set the same
   shape. If the L1 wants the literal, the counting command has to change instead.
2. **The preamble paragraph changed more than the placeholder clause** (§2a). Scope is one paragraph,
   disclosed above with the exact before/after text; the alternative was leaving two falsified clauses
   in place. Revertable as a single hunk if the L1 prefers strict append-only.
3. **Line numbers drift while peers append.** The measurements in §4 were taken on the tree that ends
   at this seat's correction paragraph (1261 lines). `ScribeScorecard-3` appends the round-35 section
   after it, and `ExecD2DensityRow` revised its own erratum block earlier in this wave (its sample
   digest `65d69d44…`/1263 lines was read at a different instant than mine); both move line numbers,
   not the three `c1c6a5f` sites or the two zero counts. Re-run the two `grep -c` commands at
   integration; they are line-number independent.
4. **No `<LANE_HASH>` re-introduced.** The replacement sentence says "angle-bracket lane-hash marker"
   instead of the literal, so `grep -c '<LANE_HASH>'` stays 0 (verified in §4's sibling counts) and
   round-34's "markers 0" after-column stays true.
5. **Scratch:** none created — `/fast/scratch/hyaku/kasegi-r35/ExecD1Markers` does not exist
   (`ls` exit 2), so there is no tree to clean up; no tool installed or upgraded (no `uv`/`npx`/binary
   channel used), so nothing to record under the tooling directive.

### 7. Files changed

- `SCORECARD.md` — round-34 section only: two placeholders filled with
  `c1c6a5f826d2425446347173de527c42991b78b0`, one correction paragraph appended, whitespace re-wrap.
  Digest `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` (1261 lines) at this read.
- `.ufo/waves/round-35/wave1/ExecD1Markers.md` (this receipt) — 201 lines,
  `sha256` `a5c8020e5d0dc3773c8a0771824c718edd4a29544cdaea1cfb3f69f4cca812a2` before this line was added.

### 8. Phase 2 — the counter was re-broken by a later write and is now green again

After §4 was measured, the round-35 section landed in `SCORECARD.md` and its measurement-state line
(`:1271`, then) re-introduced the D1 literal:

```
$ grep -c -- 'filled by the L1' SCORECARD.md      -> 1   (line 1271)
$ bash corpus/instruments/r35-defect-closure.sh   (ScribeShonen-3's read)
D1 check=placeholders=1,… open=1
closed=6/7 exit=1
```

This seat was paged by `ScribeShonen-3` and probed `ScribeScorecard-3` (who showed, by grepping every
`wave1` receipt, that `:1263-1281` is no seat's text: it arrived with the integration commit `0aee0ef`).
My one-line reword `edit` was **rejected — "Could not find a close enough match"** — because the bytes
had already changed under me. The line at my read is:

```
Measurement state: base `3266c993…`, freeze `617496b9…`, wave-1 spec/dispatch `da2d3c68…`, integration `aa6ad99…`; final lane commit `0aee0ef…` (recorded in the closing commit).
```

i.e. whoever reconciled it replaced the placeholder prose with the real integration commit
`0aee0ef105395a2f1d6ace7eaeef13871bb26988` (`git cat-file -t` = commit, subject "round-35: integration —
lesson, scorecard, SHONEN, LOG, wave receipts, assimilation artifacts") instead of the wording this seat
had proposed in its rejected edit (that proposed wording is **not** in the file). This seat claims no
credit for the edit and made no write to it.

Current state, measured after the L1's commit `8ce6fb4f2a33a6e1fb0963021905fb20dd58cc05`
("round-35: D1 closure fix — scorecard closing-commit wording"; `git status --porcelain SCORECARD.md`
empty, so the file is committed, not dirty):

```
$ grep -c -- 'filled by the L1' SCORECARD.md
0
exit=1
$ grep -c -- 'c1c6a5f' SCORECARD.md
3
exit=0
$ sha256sum SCORECARD.md
085cffd60be1ad2fac07736e4bbe5c25fb06cace5bdda8707d75352e2575aaaa  SCORECARD.md
$ wc -l SCORECARD.md
1282 SCORECARD.md
```

and with the closure suite now landed, this seat ran it read-only (the wave's editing had stopped for
this file; §5's hold-off applied while the suite was still in flight):

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=3,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0
suite_exit=0
```

D1's own check line (`placeholders=0, …, correction-c1c6a5f=3, open=0`) is the instrument-level
confirmation of §4; the suite's `closed=7/7 exit=0` is the C1 seat's claim, measured here only as a
cross-check.

**Two items this seat escalates instead of editing** (both are other seats' rows; neither is mine to
rewrite — the instruction is explicit that a leaf does not rewrite a sibling's paragraph):

1. **Stale `depth:density` stub row, `SCORECARD.md:1269`**, still reads "unchanged (no density claim;
   no-harm guard mean ≈ 201.2)". `wave1/ExecNoHarmFinal.md:41-63` measures the **landed** `SKILL.md`
   at mean **220.9 / 26 blocks / 742 cites** and binds **201.2** to the `3266c99` blob
   (`ba5ebe5d…`, 1091 lines / 25 / 711). This is the same stale-prose class as round-34's D2. Reported
   to `ScribeScorecard-3` (who is appending a byte-bound guard row) and to the row's author; the row
   needs the 220.9-landed / 201.2-base-blob split if the L1 keeps the stub block.
2. **`final lane commit \`0aee0ef…\`` inside the round-35 section is the *integration* commit**, not the
   closing one (`0aee0ef` is an ancestor of `HEAD` `8ce6fb4`, and further commits landed after it).
   The label is the L1's call; recorded here because a reader would take it as the closing value.
