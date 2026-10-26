# ExecD2DensityRow — round-35 D2: stale round-34 depth:density row (append-only erratum)

Seat: `ExecD2DensityRow` (executor, leaf). Round: kasegi-shokunin round 35, hyaku run 8.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope); lane base
`3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9`.

Write scope exercised: **`SCORECARD.md` (two insertion-only `edit` calls at the end of the round-34
section) + this receipt**. Scratch `/fast/scratch/hyaku/kasegi-r35/ExecD2DensityRow/` removed before
yield. No `git add`/`commit`/`push`, no `jj` invocation, no install, no network, no write outside the
lane, no subagent, no `agent://all`. Read-only git plumbing used: `show`, `diff`, `log`, `status`.

## Report

### 1. Assignment and pre-state

D2 as routed: `SCORECARD.md` round-34 `depth:density` row says the row's own measurement is 0 changed
`SKILL.md`/`PROVINCE.md` lines and mean 201.7; at the tip each file has +1 appended correction line and
the mean is 201.2 — fix by **appending** (never by editing the row). Pre-state, after reading
`SCORECARD.md:1121-1243` and `corpus/lessons/round-34-verifier-spotcheck.md:165-198`:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum SCORECARD.md
efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91  SCORECARD.md      # exit 0
$ wc -l SCORECARD.md
1243 SCORECARD.md                                                                     # exit 0
$ grep -c 'round-34 depth:density row' SCORECARD.md   -> 0   (exit 1)
$ grep -c '201\.2' SCORECARD.md                       -> 0   (exit 1)
$ grep -c 'Erratum (round 35' SCORECARD.md            -> 0   (exit 1)
```

The row to correct is base line 1145 (`grep -n 'mean \*\*201.7\*\*, 25 blocks, 710' SCORECARD.md` →
`1145:`; the earlier round-30 row at `1003:` reads `mean 191.5, 24 blocks, 689`, so the pattern is
unique). `SCORECARD.md` was byte-identical to the lane base and to the freeze commit at that instant
(`git diff --numstat 3266c99 -- SCORECARD.md` and `... 617496b ...` both printed nothing, exit 0) — my
append is the first round-35 change to the file.

**The routed evidence pointer does not exist at my read.** `.ufo/waves/round-35/wave1/` contained only
`swarm-registry.json`; `wave1/L1Integration.md` is absent. I therefore re-derived both limbs of the
erratum from committed blobs instead of quoting it (and the erratum names the blobs — §3).

### 2. Independent re-derivation of both limbs (unchanged instrument, same definition)

```
$ for c in 206e510 4b0a9f2 c1c6a5f 3266c99; do git show $c:SKILL.md | sha256sum | cut -c1-8; git show $c:SKILL.md | wc -l; done
206e510 SKILL b11b6085 / 1090 lines
4b0a9f2 SKILL ba5ebe5d / 1091 lines
c1c6a5f SKILL ba5ebe5d / 1091 lines
3266c99 SKILL ba5ebe5d / 1091 lines
206e510 PROVINCE b57de5d9 / 74 lines
3266c99 PROVINCE b4bb5fee / 75 lines                                          # exit 0

$ git show 206e510:SKILL.md > $S/s-206e510.md && python3 corpus/instruments/density.py $S/s-206e510.md --label r34-prebytes | grep -E 'mean dens|Total path'
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.                          # exit 0

$ python3 corpus/instruments/density.py SKILL.md --label r34-tip | grep -E 'mean dens|Total path'   # SKILL.md then = ba5ebe5d / 1091
| | **mean dens** | | | | | | | | **201.2** |
Total path-citation instances: 711 across 25 blocks.                          # exit 0

$ diff <(git show 206e510:SKILL.md) <(git show 4b0a9f2:SKILL.md)
1090a1091
> [round-34 correction, appended 2026-10-26, end-of-file append per R6] The `capture-binding-check.py` row above pins di…
$ diff <(git show 206e510:PROVINCE.md) <(git show 4b0a9f2:PROVINCE.md)
74a75
> [r34 Frontier amendment, appended 2026-10-26, end-of-file append per R6] F17 — Immunefi Vulnerability Severity Class…  # exit 0
```

So the +1 line per file is **exactly one appended line each** (not a rewrite): `SKILL.md` 1090 → 1091
and `PROVINCE.md` 74 → 75, both landing in the round-34 closing commit `4b0a9f2`, and the mean moves
**201.7 → 201.2** with the committed `density.py` on both sides (710 → 711 path cites, 25 blocks both).
That is D2's premise, re-measured rather than inherited: the row's 0-changed-lines / 201.7-after column
is the pre-closing-commit state (`b11b6085`, the round-33 final bytes), and the round-34 section was
written before the R6 correction append reached the file.

### 3. The edits (insertion-only; frozen literal first, provenance second)

Both were `edit` calls with content-addressed `old_string`s, anchored on the then-current unique tail
sentences; no `write` on a shared file, no whole-file rewrite.

1. Anchored on `and this section itself, none of which any counter above reads.` →
   appended the frozen erratum sentence verbatim:

```
Erratum (round 35): the round-34 depth:density row measured 0 changed SKILL/PROVINCE lines and mean 201.7; at the tip each file had +1 appended correction line and the measured density mean is 201.2 (unchanged instrument, same definition).
```

2. Anchored on that sentence → appended a measurement-state paragraph directly beneath it, because
   the live-tree mean moved during the wave (§5) and a bare "at the tip" would itself become the next
   stale-at-tip claim:

```
Measurement state for the erratum above, so the two numbers stay bound to bytes: the 201.7 limb is
`git show 206e510:SKILL.md` (`b11b6085…`, 1090 lines, 710 path-citation instances, 25 blocks;
`PROVINCE.md` `b57de5d9…`, 74 lines) and the 201.2 limb is
`git show 3266c9937b03062d9bbc2f436e20820115ed179c:SKILL.md` (`ba5ebe5d…`, 1091 lines, 711 cites,
25 blocks; `PROVINCE.md` `b4bb5fee…`, 75 lines). The one line each comes from the round-34 closing
commit `4b0a9f2` (`diff` = `1090a1091` for `SKILL.md`, `74a75` for `PROVINCE.md`, both `[round-34
correction, appended 2026-10-26, end-of-file append per R6]`). Round-35 appends to `SKILL.md` move the
live-tree mean independently of this erratum — read both figures against the named blobs, not the
working tree (`density.py`, unchanged instrument, same definition).
```

Neither edit touched the stale row, `SKILL.md`, `PROVINCE.md`, or any other lane file.

### 4. Verification against the frozen acceptance checks (final state, post-edit)

```
$ grep -c 'round-34 depth:density row' SCORECARD.md
1                                                                             # exit 0   (>= 1 required)
$ grep -c '201\.2' SCORECARD.md
2                                                                             # exit 0   (>= 1 required; erratum sentence + provenance paragraph)
$ grep -c 'Measurement state for the erratum above' SCORECARD.md
1                                                                             # exit 0
$ grep -c 'filled by the L1' SCORECARD.md
0                                                                             # exit 1 = count 0 (C1 marker clause; see §5)
$ git diff --numstat 3266c9937b03062d9bbc2f436e20820115ed179c -- SCORECARD.md
33	15	SCORECARD.md                                                           # exit 0  (D1 reworded twice inside my verification window: 23/13 -> 33/13 -> 33/15; my hunks are `+` side only)
$ git diff 3266c9937b03062d9bbc2f436e20820115ed179c -- SCORECARD.md | grep -c '^-[^-]'
15                                                                            # exit 0
$ git diff -U0 3266c99 -- SCORECARD.md | grep '^@@'
@@ -1129,11 +1129,12 @@ together with the do-nothing controls committed at the freeze
@@ -1240,4 +1241,21 @@ at 4 the lowest-axis obligation stays active, and the C1 blind spots above are t # exit 0
$ sha256sum SCORECARD.md
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md  # exit 0  (last read; scribe appends after)
$ wc -l SCORECARD.md
1261 SCORECARD.md                                                              # exit 0
```

**Stale row bytes untouched (byte identity, not a diff read):**

```
$ git show 3266c99:SCORECARD.md | grep 'mean \*\*201.7\*\*, 25 blocks, 710' | sha256sum | cut -c1-16
0f0b804b2225d4ac
$ grep 'mean \*\*201.7\*\*, 25 blocks, 710' SCORECARD.md | sha256sum | cut -c1-16
0f0b804b2225d4ac                                                              # exit 0   ROW_BYTES_IDENTICAL=yes
```

**The 15 deletions in `git diff <base>` are not mine.** They are exactly ExecD1Markers' two replaced
lane-commit placeholder paragraphs (hunk `-1129,11` = the preamble, hunk `-1240,4` = the closing
paragraph, which D1's authorised D1 fix rewrote in place; 13 deletions at my first read, 15 after
D1's second reword). My contributions are on the `+` side only: `-1240,4 +1241,21` is D1's reworded
closing paragraph plus blank line plus **my** erratum sentence plus blank line plus **my** provenance
paragraph. A seat reading only `numstat` would see the deletions and must attribute them to D1, not to
D2.

### 5. Cross-seat evidence, and one live-state hazard the L1 must see

- **D1 concurrency (coordinated, not a collision).** I messaged `ExecD1Markers` before writing and
  again after; SCORECARD.md ordering ended as: my erratum (line 1246) → my provenance paragraph
  (1248-1256) → D1's `Correction (round 35)` (1258-1261). My first post-append read caught D1's
  correction quoting the removed literal back into the file, `grep -c 'filled by the L1'
  SCORECARD.md` = **2**; I reported the exact lines to D1 rather than editing their paragraph, and
  their reword brought the count to **0** (`grep -c 'filled by the L1'` → 0, exit 1). The C1 marker
  clause therefore reads 0 on measured output, not on assertion.
- **`SKILL.md` moved under the measurement.** A D3 seat appended the two Gates & probes registry rows
  during my wave: `SKILL.md` 1091 → **1104 lines**, `git diff --numstat 3266c99 -- SKILL.md` =
  `13 0`, and the live-tree instrument now prints

```
$ python3 corpus/instruments/density.py SKILL.md --label r35-verify | grep -E 'mean dens|Total path'
| | **mean dens** | | | | | | | | **220.9** |
Total path-citation instances: 742 across 26 blocks.                          # exit 0
```

  So **201.2 is the round-34 tip value, not a live-tip value**; the working tree reads 220.9 (26
  blocks, the new registry block) as of this receipt. `PROVINCE.md` is still 75 lines / `b4bb5fee…`
  (unchanged this round). This is the same staleness class D2 itself is about, which is why §3 edit 2
  binds both figures to named blobs instead of leaving "at the tip" floating. Any later round-35
  scorecard row or verifier pass that prints a density mean from the working tree is measuring a
  different byte set than the erratum's.
- `ScribeScorecard-3` is appending the new `## Round 35` section **after** D1 and me; it confirmed my
  erratum at 1246 and D1's reword below it with `filled by the L1` = 0 at its own read. My final digest
  `51337bf1…` (1261 lines, D1's `Correction (round 35)` at 1258-1261 as the tail) is therefore a
  **checkpoint, not the file's closing digest** — the scribe's section will move both. No `## Round 35`
  heading existed at my last read.

### 6. Deviations, limits, risks

1. **Routed evidence substituted.** `wave1/L1Integration.md` (the routed source for "mean is 201.2")
   does not exist in the wave dir at my read; I measured the two blobs with the committed instrument
   instead and cited the blobs in the erratum. Nothing was taken on trust; nothing was fabricated.
2. **One paragraph beyond the frozen literal.** The assignment specified the erratum sentence; I added
   the measurement-state paragraph (§3 edit 2) because the live mean moved to 220.9 during the same
   wave. The frozen sentence is present verbatim and unaltered at line 1246; the addition is clearly
   labelled and carries no score, no cell value, and no edit to the round-34 row.
3. **Append order.** D1's edits landed between my pre-read and my first append, so my paragraph sits
   between D1's rewritten closing paragraph and D1's correction note rather than strictly last. Both
   are at the end of the round-34 section, and the file tail (D1's correction) is intact for the
   scribe's anchor.
4. **Not judged here.** Whether the round-35 row should restate the density number, and whether the
   erratum's 201.2/220.9 split needs a further round-35 note, are the L1's integration decisions. I
   report the measurements; I do not score the round.

### 7. Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r35/ExecD2DensityRow/` (blob exports `s-206e510.md`,
`s-4b0a9f2.md`, `s-c1c6a5f.md`, `s-3266c99.md`, `p-*.md`, `SKILL-round34.md`, `ev/verify.txt`,
`ev/verify-after.txt`, `ev/density.txt`) is deleted before yield; the evidence quoted above is inlined
in this receipt. No scratch tree remains on disk at seat end.
