VERDICT: BROKEN

# R46bMutF29a — mutation-test of `r46-f29-gate.py` v1 against the R50 receipt's 21 mutants

Scope: `corpus/instruments/r46-f29-gate.py` (sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`,
matching `freeze.txt` `f29-gate-sha256-v1`), the R50 receipt
`.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt`, and the fixture builders
`.ufo/waves/round-46/attempt2/controls/f29-fixture.py` + `f29-defects.py`.
No file under the lane was modified; every mutant lives in scratch (`/fast/scratch/hyaku/kasegi-r46/R46bMutF29a/`),
removed on exit. Scratch-derived evidence is copied into `.ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/`.

## Summary of what I found

1. **The receipt's 20 pairing rows reproduce exactly** — every base limb and every mutant limb, 20/20 — when the
   pairing is rebuilt from the committed fixture builders and the mutant table is re-derived by analogy with the
   committed C2 battery (`r46-mutbat.py` `C2_MUTANTS` G1a..G7c). All 11 FLIP rows and all 9 NOT-SHOWN rows match.
2. **The receipt's "21 mutants" is not 21.** The table has 20 rows and names 20 distinct mutant ids; limb **H6 has
   only 2** (H6a, H6b) — **H6c is missing from the table entirely**, yet the header says
   `## Mutants defined: 21 (3 per limb H1-H7)`. `freeze.txt` repeats `21 mutants, 11 defect-tree flips, 9 disclosed
   with reasons`, so the count `21` is carried into the frozen record. The 21st mutant (`H6c-size-low`,
   `os.path.getsize(...) >= 3000` → `>= 3`) is a real, isolable mutant: it flips H6 on the `thinsection` tree
   (base `entry-bytes-ok=0` → mutant `entry-bytes-ok=1`) and on my `probe-p6` tree. It was neither shown nor
   disclosed.
3. **Three of the nine NOT-SHOWN disclosures are falsified by single-defect trees.** Disclosures **(a) H1a**,
   **(b) H2b**, **(c) H3a** each say the mutant "cannot be isolated at gate level" by any single-defect tree.
   I built such a tree for each and the mutant flips. This is a *coverage* finding, not a contract change: the
   mutants are killable by gate-level trees that the frozen harness does not contain, so the claim's stated
   "frozen duty" (grade (a),(b),(d),(e) on synthetic tables in wave 1) is based on a premise that does not hold
   for (a),(b),(c) — they are isolable at gate level, and the selftest work for them is a duplication, not a
   necessity.

## 1. Rebuilding the pairing — all 20 rows reproduce

The receipt names mutants but publishes no `old -> new` triples (grep for `H1a|H2b|H3a` across the lane finds them
only in the receipt and in a sibling wave-1 draft). I re-derived the triples by analogy with the committed C2
battery's `C2_MUTANTS` (same clause-weakening shape, retargeted at the f29 gate's own literals: 29 rows, `S074`,
`2026-10-29`, 11 cells, 66 entries, 25 words). Every `old` substring occurs exactly once in the gate
(`mutants=21 all-old-substrings-unique`), so no edit could land on the wrong line. The independently-derived
sibling table at `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.py`
agrees with mine on all 21 ids and all 21 `old -> new` pairs (mine differs only in that it anchors `H1c`/`H6a`/`H7a`
on a shorter unique substring).

Trees rebuilt with the committed builders:

```
$ python3 -B controls/f29-fixture.py --mode positive --dir $S/trees/positive --lane <lane>
$ python3 -B controls/f29-defects.py --defect <name> --dir $S/trees/<name> --lane <lane>     # 17 defects
```

Baseline (pristine gate, `corpus/instruments/r46-f29-gate.py`):

```
$ python3 -B corpus/instruments/r46-f29-gate.py --root $S/trees/positive
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

My rebuilt trees are **byte-identical** to the L1's leftover R50 trees (`diff -r` against
`/fast/scratch/hyaku/kasegi-r46/L1/f29r50/def-*`): `positive, duprow, fencedf29, vjunk, thinsection, badnames,
row9cells, thinscope, kindcase, manws, fewquotes, dupquote, widespan, longquote, fewspans, nestedmd, entrymutant,
src0740` all report `BYTE-IDENTICAL to L1 leftover`. (`junk`/`fabricated` differ only in the SOURCES.md row shape —
see §5.) The receipt's pairing lines, reproduced:

```
| pair | defect | mutant | base limb | mutant limb | verdict |
|---|---|---|---|---|---|
| 1 | duprow (duplicate live F29 row) | H1a counts-loose | H1=0 | H1=0 | NOT-SHOWN (a) |
| 2 | fencedf29 (F29 row inside a code fence) | H1b raw-loose | H1=0 | H1=0 | NOT-SHOWN (a) |
| 3 | src0740 (sources cell S0740) | H1c src-boundary | H1=0 | H1=1 | FLIP |
| 4 | vjunk (verified-at gains a comment) | H2a verified-loose | H2=0 | H2=1 | FLIP |
| 5 | thinsection (6-word Scope prose, table kept) | H2b wordfloor-low | H2=1 | H2=1 | NOT-SHOWN (b) |
| 6 | badnames (xrefs to unrelated in-range files) | H2c need-empty | H2=0 | H2=1 | FLIP |
| 7 | row9cells (S074 row loses two cells) | H3a cells-loose | H3=0 | H3=0 | NOT-SHOWN (c) |
| 8 | thinscope (scope cell three words) | H3b scope-low | H3=0 | H3=1 | FLIP |
| 9 | kindcase (kind cell `Docs`) | H3c kind-dead | H3=0 | H3=1 | FLIP |
| 10 | manws (manifest + trailing blank line) | H4a manifest-unpinned | H4=0 | H4=1 | FLIP |
| 11 | fewquotes (only the five core quotes kept) | H4b quotes-low | H4=0 | H4=0 | NOT-SHOWN (d) |
| 12 | dupquote (one quote duplicated) | H4c distinct-dropped | H4=0 | H4=0 | NOT-SHOWN (d) |
| 13 | widespan (quote cited 1-42) | H5a span-wide | H5=0 | H5=1 | FLIP |
| 14 | longquote (30-word real-text quote) | H5b words-wide | H5=0 | H5=1 | FLIP |
| 15 | fewspans (G5 row removed, 6 spans remain) | H5c pass-low | H5=0 | H5=0 | NOT-SHOWN (e) |
| 16 | nestedmd (knowledge/sub/note.md) | H6a counts-loose | H6=0 | H6=1 | FLIP |
| 17 | entrymutant (pinned entry gains a line) | H6b pin-dropped | H6=0 | H6=1 | FLIP |
| 18 | symlink (corpus is a symlink) | H7b symlink-dead | H7=0 | H7=1 | FLIP |
| 19 | row9cells tree, H7 limb | H7a verdict-or | H7=0 | H7=0 | NOT-SHOWN (f) |
| 20 | positive tree, H7 limb | H7c okline-loose | H7=1 | H7=1 | NOT-SHOWN (f) |
```

My rebuild, row for row:

```
pair= 1 defect=duprow       mutant=H1a-counts-loose       limb=H1 receipt=(0,0,NOT-SHOWN (a)) mine=(0,0) match
pair= 2 defect=fencedf29    mutant=H1b-raw-loose          limb=H1 receipt=(0,0,NOT-SHOWN (a)) mine=(0,0) match
pair= 3 defect=src0740      mutant=H1c-src-boundary       limb=H1 receipt=(0,1,FLIP) mine=(0,1) match
pair= 4 defect=vjunk        mutant=H2a-verified-loose     limb=H2 receipt=(0,1,FLIP) mine=(0,1) match
pair= 5 defect=thinsection  mutant=H2b-wordfloor-low      limb=H2 receipt=(1,1,NOT-SHOWN (b)) mine=(1,1) match
pair= 6 defect=badnames     mutant=H2c-need-empty         limb=H2 receipt=(0,1,FLIP) mine=(0,1) match
pair= 7 defect=row9cells    mutant=H3a-cells-loose        limb=H3 receipt=(0,0,NOT-SHOWN (c)) mine=(0,0) match
pair= 8 defect=thinscope    mutant=H3b-scope-low          limb=H3 receipt=(0,1,FLIP) mine=(0,1) match
pair= 9 defect=kindcase     mutant=H3c-kind-dead          limb=H3 receipt=(0,1,FLIP) mine=(0,1) match
pair=10 defect=manws        mutant=H4a-manifest-unpinned  limb=H4 receipt=(0,1,FLIP) mine=(0,1) match
pair=11 defect=fewquotes    mutant=H4b-quotes-low         limb=H4 receipt=(0,0,NOT-SHOWN (d)) mine=(0,0) match
pair=12 defect=dupquote     mutant=H4c-distinct-dropped   limb=H4 receipt=(0,0,NOT-SHOWN (d)) mine=(0,0) match
pair=13 defect=widespan     mutant=H5a-span-wide          limb=H5 receipt=(0,1,FLIP) mine=(0,1) match
pair=14 defect=longquote    mutant=H5b-words-wide         limb=H5 receipt=(0,1,FLIP) mine=(0,1) match
pair=15 defect=fewspans     mutant=H5c-pass-low           limb=H5 receipt=(0,0,NOT-SHOWN (e)) mine=(0,0) match
pair=16 defect=nestedmd     mutant=H6a-counts-loose       limb=H6 receipt=(0,1,FLIP) mine=(0,1) match
pair=17 defect=entrymutant  mutant=H6b-pin-dropped        limb=H6 receipt=(0,1,FLIP) mine=(0,1) match
pair=18 defect=symlink      mutant=H7b-symlink-dead       limb=H7 receipt=(0,1,FLIP) mine=(0,1) match
pair=19 defect=row9cells    mutant=H7a-verdict-or         limb=H7 receipt=(0,0,NOT-SHOWN (f)) mine=(0,0) match
pair=20 defect=positive     mutant=H7c-okline-loose       limb=H7 receipt=(1,1,NOT-SHOWN (f)) mine=(1,1) match
SUMMARY rows=20 receipt-match=20 my-flips=11
```

**Result: 20/20 rows match the receipt, 11 flips — the receipt's own table is faithfully reproduced.**

Note on pair 5: `thinsection` reads H2=1 in the *base* gate (the receipt records base H2=1, mutant H2=1). The
thinsection defect actually reddens **H6** (`entry-bytes-ok=0`), not H2 — the 6-word Scope stub is still inside a
section that also holds the 6-row table, so the section word count stays high. The receipt's pairing therefore
pairs a tree that does not exercise H2 at all with the H2b mutant.

## 2. Do-nothing control (discriminator)

A pristine *copy* of the gate, run from a different path with the same bytes, must produce identical output on
every tree — otherwise a "flip" could be an artifact of path resolution (the gate locates `source-recheck.py`
next to itself via `INSTRUMENTS`):

```
$ python3 -B do-nothing-control.py
badnames       IDENTICAL rc=1 f29-gate fixed=6/7 exit=1
...
positive       IDENTICAL rc=0 f29-gate fixed=7/7 exit=0
probe-f30      IDENTICAL rc=1 f29-gate fixed=6/7 exit=1
...
do-nothing-control-divergences=0
```

`do-nothing-control-divergences=0` over 22 trees. Every flip reported below is therefore attributable to the
mutated line, not to the copy.

## 3. Disclosure (a) — H1a counts-loose — **REFUTED**

Receipt's reason (a): *"the H1 counts clause and the one-live-row clause are shadowed at gate level by the later
F29-presence/duplicate-id clauses: any tree that trips counts (rows=28/30) or duplicates the row also trips `dup`
or `entry-shared`, so no single-defect tree isolates them."*

The claim "any tree that trips counts also trips `dup` or `entry-shared`" is false: a tree with an **extra
distinct** admitted row (F30) trips counts (`rows=30 admitted=30 dup=0`) while tripping **neither** `dup` nor
`entry-shared`. I built exactly that tree (`probe-p1`, one line appended to `corpus/README.md`):

```
### P1 disclosure (a)/H1a: extra DISTINCT admitted row F30 (trips counts, not dup, not entry-shared)
  BASE   H1 pass=0 read=rows=30 admitted=30 dup=0   [fixed=6/7]
  MUTANT H1 pass=1 read=rows=29 admitted=29 F29=admitted   [fixed=7/7]
  => FLIP: the mutant IS isolated at gate level by this tree
```

**Accepted? No.** The disclosure's premise is falsified by a one-line tree; H1a *is* isolable at gate level.
Robustness: the flip survives under the C2-analogue edit (`< 29`) but **not** under a variant that keeps `dup`
(`len(rows) < 29 or adm != 29 or dup:` -> my probe tree has `dup=0`, so the `dup` clause still fires; and the
third variant `> 29` also fails to flip). So the refutation is specific to the receipt's own `counts-loose`
edit, which drops `dup` — the same weakening the committed C2 battery's `G1a-counts-loose` performs. The receipt's
*stated reason* is independently wrong (it asserts every counts-tripping tree also trips `dup` or `entry-shared`),
and under the receipt's own edit the mutant is killable.

## 4. Disclosure (b) — H2b wordfloor-low — **REFUTED**

Receipt's reason (b): *"the per-section word floor is shadowed by the section's own table: a section that still
carries its >= 6-row table always clears 25 words, and a section stripped below 25 words loses the table and trips
table-rows."*

The premise is that the table and the prose live in the same section, so gutting the prose leaves the table's words
counted toward the section. But the gate's `sect_words()` counts words in a section **up to the next `##`
heading**, and the table is only counted if it sits inside that section. A tree can gut a **different** section
from the one holding the table. `probe-p7` replaces only the `## Limits` body with one 24-word line; the 6-row
table stays in `## Scope and decision rule`, so `table-rows=6` still holds, `full=3/4` goes red at base, and the
mutant's lowered floor clears it:

```
### P7 disclosure (b)/H2b: the ## Limits section body replaced by one 17-word line (table untouched, all other sections untouched)
  BASE   ... | gate H2 pass=0 read=source=1 verified-at=1 recheck=1 sections=4/4 full=3/4 table-rows=6 xrefs=2/2 anchored=1 | ...
  MUTANT ... | gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1 | ...
  => H2 limb H2: base=0 mutant=1  FLIP (isolated)
```

**Accepted? No.** The mutant is isolable at gate level. Robustness: the flip reproduces under three different
plausible wordfloor edits (25->5, 25->24, and floor dropped to 0), and under a second construction where the Scope
section is gutted and its table relocated to `## Overlap and novelty` (`probe-p2`, base `full=3/4 table-rows=6`
-> mutant `full=4/4 table-rows=6`). The receipt's claim that "a section stripped below 25 words loses the table
and trips table-rows" does not hold: the table can be in another section, and the gate's table-row scan is
document-wide, not section-scoped.

## 5. Disclosure (c) — H3a cells-loose — **REFUTED**

Receipt's reason (c): *"relaxing the 11-cell test to >= 9 re-parses the row but the shifted cells then fail the
status/opened/cadence literals, so the tree stays red: the relaxation is closed by construction (a 9-cell row
cannot satisfy the positional checks)."*

The argument is about a 9-cell row (the `row9cells` defect, which deletes two *middle* cells so every positional
index shifts). But `>= 9` also admits a row with **more** cells. A 12-cell row keeps all eleven positional
indices intact (the extra cell is appended at the end), so the mutant re-parses it and every check passes.
`probe-p3` appends one cell to the S074 registry row:

```
### P3 disclosure (c)/H3a: S074 registry row carries a 12th cell (extra cell appended)
  BASE   H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1   [fixed=5/7]
  MUTANT H3 pass=1 read=row-S074=ok   [fixed=6/7]
  => FLIP: the mutant IS isolated at gate level by this tree
```

**Accepted? No.** The disclosure's "closed by construction" claim is false for the mutant's own edit (`>= 9`);
only the specific 9-cell tree fails to isolate it. Robustness: the flip reproduces under both `>= 9` and `>= 10`
variants. (H3's own census coupling is separately visible: the census reports `file E01 S074 fields=12` on this
tree, so H7 is red both before and after — the H3 flip is still isolated at the limb level, which is the receipt's
own grading unit.)

## 6. Disclosures (d), (e), (f) — accepted

- **(d) H4b/H4c** — *"H4 pins the manifest bytes (H4a, flip shown), so any manifest edit that would exercise the
  quote-count or distinctness floors is already red at the pin; the floors are not isolable at gate level."*
  **Accepted.** Confirmed from the code: `h4` checks `sha(open(man,"rb").read()) != PINS["manifest.json"]` before
  the quote floor and the `distinct` conjunct, so any manifest edit is red at the pin. My own probe (shortening
  the *snapshot* while keeping the manifest pinned) does not flip either mutant:
  `BASE H4 pass=0 read=recheck-rc=1 quotes-ok=0 ... | MUTANT H4 pass=0 read=recheck-rc=1 quotes-ok=0 ... => no-flip`.
- **(e) H5c** — *"the >= 4 located floor is shadowed by `failed == 0` + the H2 table-rows >= 6 conjunct: an entry
  with a 6-row cited table always has >= 4 located spans."*
  **Accepted.** Confirmed from the code and from the snapshot: the five frozen cores are 77+ words apart in the
  normalized snapshot, while a located span holds at most 25 words (`len(nq.split()) <= 25`), so each core needs
  its own span; five cores therefore force at least five located spans, and the `>= 4` floor is unreachable.
  Measured: `core word start indices: [154, 244, 522, 599, 961]`, `min gap between core starts (words): 77`.
  My probe (dropping G4/G5/G6 rows so `cores=3/5`) does not flip H5c:
  `BASE H5 pass=0 read=spans=4 located=4 failed=0 uncited=0 cores=3/5 | MUTANT H5 pass=0 ... cores=3/5 => no-flip`.
- **(f) H7a/H7c** — *"both grade the census OUTPUT shape (`rc == 0` + an `ok` tab line). The census script lives at
  the fleet root and is not mutated by this lane; a tree with census rc=0 never lacks the ok line, so no
  lane-side defect tree isolates them."*
  **Accepted.** Confirmed from `scripts/sources-census.sh`: in `validate` mode the `ok` line is emitted only when
  the lane has no `E`-level finding (`[ "$lane_errors" = 1 ] || emit "$lane	ok	$f"`), and `findings=1` (exit 1)
  is set by the same `E` check. So `rc == 0` and the `ok` line co-occur, and a tree can only make the census print
  an `E` row (never suppress the `ok` line while `rc == 0`). Verified by running the census on my trees:
  `positive rc=0 ok_line=1 out=[file	ok	...]; row9cells rc=1 ok_line=0 out=[file	E01	S074 fields=9]; junk rc=0 ok_line=1`.
  Neither mutant flips on any tree in my sweep.

## 7. The 21st mutant — H6c — missing from the table, and it IS isolable

The receipt's table enumerates 20 rows and names 20 mutant ids; limb H6 has only two (`H6a`, `H6b`). The header
says `## Mutants defined: 21 (3 per limb H1-H7)` and `freeze.txt` records `21 mutants, 11 defect-tree flips, 9
disclosed with reasons`; `mutants per limb as named: {'H1': 3, 'H2': 3, 'H3': 3, 'H4': 3, 'H5': 3, 'H6': 2, 'H7': 3}`
and `limbs without 3 mutants: ['H6']`. The missing third H6 mutant is `H6c-size-low`
(`os.path.getsize(os.path.join(root, p)) >= 3000` -> `>= 3`), the direct analogue of the committed C2 battery's
`G6c-size-low`. It is a live, isolable mutant:

```
=== C. the receipt's UNLISTED 21st mutant H6c-size-low ===
tree=thinsection    BASE H6 pass=0 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=0 symlinks=0 | MUTANT H6 pass=1 read=... entry-bytes-ok=1 symlinks=0
tree=probe-p6       BASE H6 pass=0 read=... entry-bytes-ok=0 symlinks=0 | MUTANT H6 pass=1 read=... entry-bytes-ok=1 symlinks=0
```

(`probe-p6` is a compact but otherwise fully valid entry of 2734 bytes: `gate H1..H7` all pass except H6's size
floor, and the H6c mutant takes the tree to `fixed=7/7 exit=0`.) So the receipt's R50 requirement of ">= 3 mutants
per limb" is not met by the table, and the mutant that would close the gap is neither shown nor disclosed.

## 8. Full mutant x tree sweep (29 trees x 21 mutants)

Every mutant was run against every tree; a "diff" is a tree where the mutant changes some limb's verdict relative
to the pristine gate:

```
H1a-counts-loose         diffs=3 probe-f30:H1 0->1; probe-p1:H1 0->1; probe-p1-distinct-row:H1 0->1
H1b-raw-loose            diffs=0 NONE (equivalent on every tree)
H1c-src-boundary         diffs=1 src0740:H1 0->1
H2a-verified-loose       diffs=1 vjunk:H2 0->1
H2b-wordfloor-low        diffs=1 probe-p2:H2 0->1
H2c-need-empty           diffs=1 badnames:H2 0->1
H3a-cells-loose          diffs=1 probe-p3:H3 0->1
H3b-scope-low            diffs=1 thinscope:H3 0->1
H3c-kind-dead            diffs=26 badnames:H3 1->0; ... positive:H3 1->0; kindcase:H3 0->1; ...   (see note)
H4a-manifest-unpinned    diffs=1 manws:H4 0->1
H4b-quotes-low           diffs=0 NONE (equivalent on every tree)
H4c-distinct-dropped     diffs=0 NONE (equivalent on every tree)
H5a-span-wide            diffs=1 widespan:H5 0->1
H5b-words-wide           diffs=1 longquote:H5 0->1
H5c-pass-low             diffs=0 NONE (equivalent on every tree)
H6a-counts-loose         diffs=1 nestedmd:H6 0->1
H6b-pin-dropped          diffs=1 entrymutant:H6 0->1
H6c-size-low             diffs=3 probe-p2:H6 0->1; probe-p6:H6 0->1; thinsection:H6 0->1
H7a-verdict-or           diffs=0 NONE (equivalent on every tree)
H7b-symlink-dead         diffs=1 symlink:H7 0->1
H7c-okline-loose         diffs=0 NONE (equivalent on every tree)
```

Note on `H3c-kind-dead`: it flips H3 on 26 trees in the *wrong* direction (`1->0`) because it turns the kind
literal into `!= "Docs"`, which no valid tree satisfies — it makes H3 fail everywhere. Only the `kindcase` tree
gives the receipt's `0->1` flip. That is consistent with the receipt's row 9 but means H3c is a degenerate
mutant; the receipt does not disclose it.

## 9. Incidental finding: the receipt's junk/fabricated control baseline does not reproduce

The receipt states: *"junk tree `fixed=3/7` (H2/H5 red: 2/7 quotes located, 0/5 cores); fabricated tree
`fixed=3/7` (5/7 located, 4/5 cores)."* Rebuilt from the **committed** `f29-fixture.py`:

```
positive    f29-gate fixed=7/7 exit=0
junk        f29-gate fixed=6/7 exit=1     (H5 red only: located=2 cores=0/5)
fabricated  f29-gate fixed=6/7 exit=1     (H5 red only: located=5 cores=4/5)
```

The H5 read tokens match the receipt exactly (`2/7 located, 0/5 cores`; `5/7 located, 4/5 cores`), but the totals
are 6/7, not 3/7, and H2 is **green** on both — the receipt's own summary line
`junk tree fixed=3/7 (H2/H5 red ...)` and `fabricated tree fixed=3/7` do not describe what the committed builder
produces. The L1's own leftover trees (`/fast/scratch/hyaku/kasegi-r46/L1/f29r50/junk`, `.../fab`, built 17:34,
before the 17:35 fixture commit) do read `fixed=4/7` (H3 red from a 12-cell SOURCES row, H5 red, H7 red) — also
not 3/7. So the receipt's junk/fabricated control baseline is stale relative to the committed fixture; the L1
edited `f29-fixture.py` at 17:35:19 after building those trees at 17:34:43.

## Limitations

- **The mutant table is my re-derivation, not the L1's.** The receipt publishes no `old -> new` triples. I derived
  them from the committed C2 battery's shape; the sibling wave-1 draft
  `R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.py` independently derived the same 21 ids and the same 21
  edit pairs, which is corroboration but not the L1's own artifact. My refutations of (a), (b), (c) hold for the
  edits so derived; (b) additionally holds across three wordfloor variants and two tree constructions, (c) across
  two cell-count variants, (a) only for the `dup`-dropping `counts-loose` edit (which is the receipt's own).
- **"Flipped" here means the mutant changes the limb's verdict on some tree** (the receipt's own grading unit:
  "limb-level pass flip"). For (a) and (b) the mutant also takes the whole gate from `fixed=6/7 exit=1` to
  `fixed=7/7 exit=0`; for (c) the whole gate goes `5/7 -> 6/7` (H7 is independently red on a 12-cell row because
  the census reports `file E01 S074 fields=12`).
- I did not rebuild the census or the `sources-census.sh` — (f) is argued from that script's `validate` block and
  confirmed by running it on my trees.
- Live-target testing was not attempted (documentation-only corpus); the "capture" is a checked-in snapshot.
- I did not evaluate whether the wave-1 selftest grades these mutants correctly — that is a sibling seat's
  deliverable. My finding is only that the *reason* recorded in the frozen receipt for (a), (b) and (c) is false.
- Scratch removed on exit: `/fast/scratch/hyaku/kasegi-r46/R46bMutF29a` (receipts and harness scripts copied into
  `.ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/` first).
- No tool was installed or upgraded for this seat (no `pacman`, `uv tool`, or binary install); the only tools used
  are the pre-installed `python3` (3.14.8) and `bash`/`git` (read-only `log`/`show`/`diff`/`status`).

## Recommendation for the L1 (advisory only — I changed nothing)

1. Correct the frozen record: the receipt has 20 pairing rows and 20 named mutants, not 21; limb H6 has 2, not 3.
   Either add the `H6c-size-low` row (it is a FLIP on `thinsection`/`probe-p6`) or amend the header and `freeze.txt`
   to say 20.
2. Re-derive disclosures (a), (b), (c): each is refuted by a single-defect tree (F30 distinct row; gutted `## Limits`
   section; 12-cell SOURCES row). Those three mutants are gate-isolable and can be graded in the wave-1 harness
   without synthetic tables; only (d), (e), (f) need the selftest route the claim describes.
3. Correct the junk/fabricated control baseline (`3/7` -> `6/7`, H5 only) or state which tree the `3/7` came from,
   since the committed builder no longer produces it.
