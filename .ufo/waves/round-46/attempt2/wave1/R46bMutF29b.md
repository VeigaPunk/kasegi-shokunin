VERDICT: INFO

# Seat R46bMutF29b — independent mutant battery for `r46-f29-gate.py` (round 46 attempt 2, C2)

## What this seat did

I derived **my own** mutant set for the frozen F29 counter — **49 single-line edits** of
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-f29-gate.py`
(sha256 `a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd`, the v1 hash
recorded in `.ufo/waves/round-46/attempt2/freeze.txt` as `f29-gate-sha256-v1`) — and graded each
against the positive tree and every defect tree shipped in
`.ufo/waves/round-46/attempt2/controls/`. The set is independent of the R50 receipt: I read the
gate's own source to choose the clauses, and only afterwards compared my verdicts to the receipt's.

Mutants are applied to **scratch copies**; the committed counter is never written. The lane's
counter hash was identical before and after every wave:

```
# original gate sha256 (before) = a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd
# original gate sha256 (after)  = a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd
# original gate unchanged = True
```

Grading vocabulary (mine, stated so the numbers are unambiguous):

* **FALSE-GREEN** — the mutant makes a *defective* tree read `fixed=7/7 exit=0`. The gate stops
  rejecting a tree it must reject. This is the class that matters for C2.
* **LIMP-FLIP** — the mutant flips one limb red→green but the tree stays red on another limb.
* **POS-BREAK** — the mutant turns the *positive* tree red (a broken counter, not an escape).
* **SURVIVOR** — no limb changes on any of the 22 trees. The clause is ungraded by the corpus.

## Method and the baseline I measured

Trees were built with the shipped control builders, unchanged:

```
$ python3 controls/f29-fixture.py --mode positive --dir $S/trees/positive
$ python3 controls/f29-defects.py --defect duprow --dir $S/trees/duprow   # ... 17 defects
```

`controls/f29-defects.py` carries **17** defect branches (`duprow fencedf29 vjunk thinsection
badnames row9cells thinscope kindcase manws fewquotes dupquote widespan longquote fewspans
nestedmd entrymutant symlink`). The receipt's pairing table names a **19th** tree, `src0740`, that
the builder cannot produce, so I built it from the receipt's own description ("sources cell
S0740" — the F29 row's fourth cell set to `S0740`):

```
$ diff <(grep '^| F29 |' trees/positive/corpus/README.md) <(grep '^| F29 |' trees/src0740/corpus/README.md)
< | F29 | ... | admitted | corpus/knowledge/github-repository-security-advisories.md | S074 | Keep the maintainer flow distinct from the reporter flow (F28); ... |
> | F29 | ... | admitted | corpus/knowledge/github-repository-security-advisories.md | S0740 | Keep the maintainer flow distinct from the reporter flow (F28); ... |
```

Baseline (pristine counter, 22 trees): `positive` reads `fixed=7/7 exit=0`; every defect tree is
red on the limb the receipt predicts for it, with three trees red on **two** limbs:

```
# BASE positive     fixed=7 H1=1 H2=1 H3=1 H4=1 H5=1 H6=1 H7=1
# BASE duprow       fixed=6 H1=0 H2=1 H3=1 H4=1 H5=1 H6=1 H7=1
# BASE fencedf29    fixed=6 H1=0 H2=1 H3=1 H4=1 H5=1 H6=1 H7=1
# BASE vjunk        fixed=6 H1=1 H2=0 H3=1 H4=1 H5=1 H6=1 H7=1
# BASE thinsection  fixed=6 H1=1 H2=1 H3=1 H4=1 H5=1 H6=0 H7=1
# BASE badnames     fixed=6 H1=1 H2=0 H3=1 H4=1 H5=1 H6=1 H7=1
# BASE row9cells    fixed=5 H1=1 H2=1 H3=0 H4=1 H5=1 H6=1 H7=0
# BASE thinscope    fixed=6 H1=1 H2=1 H3=0 H4=1 H5=1 H6=1 H7=1
# BASE kindcase     fixed=5 H1=1 H2=1 H3=0 H4=1 H5=1 H6=1 H7=0
# BASE manws        fixed=6 H1=1 H2=1 H3=1 H4=0 H5=1 H6=1 H7=1
# BASE fewquotes    fixed=6 H1=1 H2=1 H3=1 H4=0 H5=1 H6=1 H7=1
# BASE dupquote     fixed=6 H1=1 H2=1 H3=1 H4=0 H5=1 H6=1 H7=1
# BASE widespan     fixed=6 H1=1 H2=1 H3=1 H4=1 H5=0 H6=1 H7=1
# BASE longquote    fixed=6 H1=1 H2=1 H3=1 H4=1 H5=0 H6=1 H7=1
# BASE fewspans     fixed=5 H1=1 H2=0 H3=1 H4=1 H5=0 H6=1 H7=1
# BASE nestedmd     fixed=6 H1=1 H2=1 H3=1 H4=1 H5=1 H6=0 H7=1
# BASE entrymutant  fixed=6 H1=1 H2=1 H3=1 H4=1 H5=1 H6=0 H7=1
# BASE symlink      fixed=5 H1=1 H2=1 H3=1 H4=1 H5=1 H6=0 H7=0
# BASE junk         fixed=6 H1=1 H2=1 H3=1 H4=1 H5=0 H6=1 H7=1
# BASE fabricated   fixed=6 H1=1 H2=1 H3=1 H4=1 H5=0 H6=1 H7=1
# BASE src0740      fixed=6 H1=0 H2=1 H3=1 H4=1 H5=1 H6=1 H7=1
```

**Discrimination against a do-nothing control.** Two mutants are deliberate no-ops (a
whitespace-only edit and a comment-only edit). Both must leave every verdict identical, and they
do — `Z0` and `Z1` are SURVIVORs on all 22 trees and read `fixed=7/7 exit=0` on the positive tree,
so the harness is not reporting a "flip" for an inert edit:

```
mutant=Z0-do-nothing-whitespace     f29-gate fixed=7/7 exit=0 f29-gate fixed=6/7 exit=1 f29-gate fixed=6/7 exit=1 f29-gate fixed=5/7 exit=1 f29-gate fixed=5/7 exit=1
mutant=Z1-do-nothing-comment        f29-gate fixed=7/7 exit=0 f29-gate fixed=6/7 exit=1 f29-gate fixed=6/7 exit=1 f29-gate fixed=5/7 exit=1 f29-gate fixed=5/7 exit=1
```

## Finding 1 (headline): one single-line edit defeats the H5 "located quote" rule on two defect trees

**Recipe** — `r46-f29-gate.py:307`, drop the `failed == 0` conjunct of the H5 verdict:

```
old: ok = failed == 0 and uncited <= 0 and len(passed) >= 4 and len(cores) == len(CORES)
new: ok = uncited <= 0 and len(passed) >= 4 and len(cores) == len(CORES)
```

**Command** (mutant copy `mutants/E9-h5-failed-conjunct/r46-f29-gate.py`, sha256
`5517b4b674752c7a57df1d9808506389236b400af7f737ba026cb15bda23f00b`):

```
$ python3 mutants/E9-h5-failed-conjunct/r46-f29-gate.py --root trees/widespan --work work
$ python3 mutants/E9-h5-failed-conjunct/r46-f29-gate.py --root trees/longquote --work work
```

**Output** — the two H5 defect trees that the receipt pairs with `H5a span-wide` and
`H5b words-wide` both read **fully green**:

```
MUTANT E9-h5-failed-conjunct      limb=H5 sha=5517b4b67475 pos=7/7 UP widespan:H5 FULLGREEN widespan UP longquote:H5 FULLGREEN longquote
```

This is beyond the receipt's disclosure set. The receipt's two H5 mutants each relax one
*per-span* cap (the 12-line span width, the 25-word cap); it records no mutant on the aggregate
`failed == 0` veto. Dropping that veto alone lets a mis-cited quote be silently excluded from the
located set while every other conjunct still holds — the gate then accepts the defective tree.
The positive tree is unaffected (`pos=7/7`).

## Finding 2: the receipt's `fencedf29` isolation story is incomplete — the fence filter is the holder

**Recipe** — `r46-f29-gate.py:123`, drop the `fence or` conjunct of the shared `live_lines` helper:

```
old:         if fence or not st or st.startswith("<!--"):
new:         if not st or st.startswith("<!--"):
```

**Output:**

```
MUTANT A1-live-lines-fence-dropped  limb=H1 sha=dbff06592cde pos=7/7 flips=[('fencedf29', 'H1')] full_false_green=['fencedf29']

=== mutant=A1-live-lines-fence-dropped tree=fencedf29 ===
  gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
  gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
  gate H3 pass=1 read=row-S074=ok
  gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
  gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
  gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
  gate H7 pass=1 read=census-rc=0 ok-line=1
  f29-gate fixed=7/7 exit=0
```

The receipt's disclosure (a) says the H1 counts clause and the one-live-row clause are
"shadowed at gate level by the later F29-presence/duplicate-id clauses". My A6 probe (disable the
**whole** count line) confirms the shadowing for `fencedf29` but identifies the holder precisely —
and shows it is not the clause the receipt names:

```
=== A6 (whole H1 count line disabled) ===
--- tree=duprow
gate H1 pass=0 read=F29-row-not-one-live-line
f29-gate fixed=6/7 exit=1
--- tree=fencedf29
gate H1 pass=0 read=F29-row-or-entry-missing entry-present
f29-gate fixed=6/7 exit=1
```

The real holder of `fencedf29` is the fence filter *inside* `live_lines` — a shared helper used by
`frontier()`, H2's body extraction, H3's row scan and H5's live-span set. The receipt's mutant set
contains no `live_lines` mutant (its H1 mutants are all inside `h1()`'s body), so this clause was
never graded at gate level.

## Finding 3: `thinsection` is held by H6's size floor, and that floor is isolable

**Recipe** — `r46-f29-gate.py:327`, lower the entry-size floor:

```
old: sized = os.path.getsize(os.path.join(root, p)) >= 3000
new: sized = os.path.getsize(os.path.join(root, p)) >= 100
```

**Output:**

```
MUTANT F1-entry-size-floor         limb=H6 sha=91eaba142421 pos=7/7 flips=[('thinsection', 'H6')] full_false_green=['thinsection']

=== mutant=F1-entry-size-floor tree=thinsection ===
  gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
  ...
  gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
  gate H7 pass=1 read=census-rc=0 ok-line=1
  f29-gate fixed=7/7 exit=0
```

The receipt pairs `thinsection` with `H2b wordfloor-low` and records `H2=1 | H2=1` (NOT-SHOWN (b),
"the section keeps its >= 6-row table"). It never records that `thinsection`'s red limb is **H6**,
not H2 — my baseline reads `gate H6 pass=0 read=… entry-bytes-ok=0` — and it carries no mutant on
the size floor. The size floor is independently isolable and its removal makes the whole defective
tree read 7/7.

## Finding 4: my set independently reproduces all 11 of the receipt's flips

Every one of the receipt's 11 recorded flips reappears in my set with an equivalent recipe — this
is the positive control on my harness. Nine of the 12 FALSE-GREENs below are receipt flips
(`A5 B1 B2 C1 D1 E1 E2 F2 H6a`); two more arrive as LIMP-FLIPs (`C2`, `G1`). The three
FALSE-GREENs that are **not** receipt flips — `A1` (fencedf29), `E9` (widespan+longquote) and `F1`
(thinsection) — are Findings 1–3, and they are the substance of this seat:

| my mutant | recipe (one line) | tree that goes green | receipt pair |
|---|---|---|---|
| `A5-s074-boundary-widened` | `re.search(r"\bS074\b", f29[0][4])` → `re.search(r"\bS074\d?\b", f29[0][4])` | `src0740` → 7/7 | pair 3 (H1c) |
| `B1-verified-at-prefix` | `h == "verified-at: " + VERIFIED_AT` → `h.startswith(...)` | `vjunk` → 7/7 | pair 4 (H2a) |
| `B2-xref-need-dropped` | `ok_x = need <= have and refok == len(refs)` → `ok_x = refok == len(refs)` | `badnames` → 7/7 | pair 6 (H2c) |
| `C1-scope-words-floor` | `row[4]) < 8` → `row[4]) < 3` | `thinscope` → 7/7 | pair 8 (H3b) |
| `C2-kind-literal-case` | `row[2] != "docs"` → `row[2] != "Docs"` | `kindcase` H3 (and positive breaks) | pair 9 (H3c) |
| `D1-manifest-pin-dropped` | `if sha(open(man, "rb").read()) != PINS["manifest.json"]:` → `if False:` | `manws` → 7/7 | pair 10 (H4a) |
| `E1-span-width` | `b - a <= 11` → `b - a <= 41` | `widespan` → 7/7 | pair 13 (H5a) |
| `E2-word-cap` | `len(nq.split()) <= 25` → `len(nq.split()) <= 250` | `longquote` → 7/7 | pair 14 (H5b) |
| `F2-content-pin-dropped` | drop `cont == PINS["base-knowledge-content"]` | `entrymutant` → 7/7 | pair 17 (H6b) |
| `G1-symlink-guard-dropped` | drop the `islink(corpus)`/`islink(SOURCES.md)` guard | `symlink` H7 | pair 18 (H7b) |
| `H6a-h6-counts-loose` | relax the three knowledge-dir counts to `>=` | `nestedmd` → 7/7 | pair 16 (H6a) |

Note on `C2`: the receipt's `H3c kind-dead` is the same edit, and the receipt records only the
`kindcase` flip. The same mutant also breaks the positive tree, which the receipt's table does not
say:

```
=== mutant=C2-kind-literal-case tree=positive ===
  gate H3 pass=0 read=bad=kind
  f29-gate fixed=6/7 exit=1
```

## Finding 5: four clauses the receipt never mutates are isolable at gate level (LIMP-FLIP)

These flip a limb red→green on a tree the receipt pairs with a *different* limb, so the receipt's
table does not show the clause exists as a separate load-bearing check.

| my mutant | one-line edit | flip | receipt's pairing for that tree |
|---|---|---|---|
| `B3-table-rows-floor` | `and len(rows) >= 6 and ok_x` → `and len(rows) >= 5 and ok_x` (`:219`) | `fewspans` H2 0→1 | pair 15 (H5c) — disclosure (e) names this conjunct only as a *shadow*, never mutates it |
| `E3-core-count` | `len(cores) == len(CORES)` → `len(cores) >= len(CORES) - 1` (`:307`) | `fewspans` H5 0→1 | pair 15 (H5c) — the receipt's H5c mutant is `len(passed) >= 4`; the *cores* equality is a separate holder |
| `F4-symlink-clause-dropped` | `and sized and not links,` → `and sized and True,` (`:329`) | `symlink` H6 0→1 | pair 18 (H7b) — H6 has its own symlink guard |
| `C8-h3-cells-loose` | `if len(c) == 11:` → `if len(c) >= 9:` (`:230`) | my `row12cells` H3 0→1 | pair 7 (H3a) — see Finding 6 |

Quoted read tokens:

```
MUTANT B3-table-rows-floor           H2     LIMP-FLIP   pos=7/7 fewspans:H2
MUTANT E3-core-count                  H5     LIMP-FLIP   pos=7/7 fewspans:H5
MUTANT F4-symlink-clause-dropped      H6     LIMP-FLIP   pos=7/7 symlink:H6
```

## Finding 6: the receipt's disclosure (c) is too strong — the 11-cell clause IS isolable

The receipt says the 11-cell clause is "closed by construction (a 9-cell row cannot satisfy the
positional checks)". I built a **12-cell** S074 row and applied the same relaxation:

```
MUTANT C8-h3-cells-loose              H3     LIMP-FLIP   pos=7/7 row12cells:H3

== C8 row12cells read tokens ==
  BASE                   gate H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1
  BASE                   f29-gate fixed=5/7 exit=1
  C8-h3-cells-loose      gate H3 pass=1 read=row-S074=ok
  C8-h3-cells-loose      f29-gate fixed=6/7 exit=1
```

The relaxed counter parses the first eleven cells of a twelve-cell row and reads H3 **green**
where the pristine counter reads it red. The clause is isolable; the receipt's "closed by
construction" claim is false as stated. (The sibling seat `R46bExecSelftestF29` reached the same
conclusion by a different route — its `clause-c-cells-12` case. My `row12cells` tree is an
independent build.)

## Finding 7: the receipt's `junk` / `fabricated` header readings do not reproduce

The receipt header states `junk tree fixed=3/7 (H2/H5 red: 2/7 quotes located, 0/5 cores)` and
`fabricated tree fixed=3/7 (5/7 located, 4/5 cores)`. The located/cores halves reproduce exactly;
the fixed counts and the "H2 red" claim do not. With the committed builders and the committed
counter I measure **6/7 with only H5 red**:

```
=== mode=junk
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
=== mode=fabricated
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```

H2 stays green on both trees. The sibling seat found the same discrepancy independently.

## Finding 8: the receipt's own accounting is one mutant short of its stated bar

The receipt header says `## Mutants defined: 21 (3 per limb H1-H7)` and `Result: mutants=21`, but
its pairing table has **20 rows**, and the H6 mutants present are only `H6a` and `H6b` — there is
no `H6c`. The receipt's own stated requirement is "R50 requires >= 3 mutants per limb", so H6 is
one mutant short of the bar the receipt sets for itself. My audit of the table:

```
table rows = 20
FLIP rows = 11  NOT-SHOWN rows = 9
mutant ids in table (20): ['H1a counts-loose', 'H1b raw-loose', 'H1c src-boundary', 'H2a verified-loose', 'H2b wordfloor-low', 'H2c need-empty', 'H3a cells-loose', 'H3b scope-low', 'H3c kind-dead', 'H4a manifest-unpinned', 'H4b quotes-low', 'H4c distinct-dropped', 'H5a span-wide', 'H5b words-wide', 'H5c pass-low', 'H6a counts-loose', 'H6b pin-dropped', 'H7b symlink-dead', 'H7a verdict-or', 'H7c okline-loose']
per limb: H1=3 H2=3 H3=3 H4=3 H5=3 H6=2 H7=3
```

(For the record, the missing third H6 mutant is exactly the size floor: the sibling seat's probe
names it `H6c-size-low`, and my `F1` mutates the same clause.)

## Finding 9 (the coverage number the L1 needs): my independent set against the wave-1 selftest

`r46-mutbat.py` has no `--counter f29` branch yet (`--counter c1|c2|both`), so the L1 has to
extend it. To say what that extension must cover, I ran the wave-1 selftest draft
(`.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`, sha256
`23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d`) against **all 49 of my
mutants**, using the battery's own predicate (selftest `failures>0` under the mutant, baseline
`failures=0`):

```
baseline selftest failures = 0
mutants=49 caught=29 uncaught=20 baseline_failures=0
UNCAUGHT ids: A2-entry-cell-dropped,A3-entry-shared-dropped,B4-recheck-count-loosened,B5-cell-word-floor,C4-url-equality-dropped,C5-anchor-locator-range,D2-recheck-pin-dropped,D4-sha-ok-conjunct-dropped,E5-uncited-tolerance,F3-nested-count,G2-ok-line-tab-dropped,G3-verdict-or,Z0-do-nothing-whitespace,Z1-do-nothing-comment,B6-h2-source-line-dropped,B7-h2-recheck-form-loosened,C6-h3-status-literal,C7-h3-opened-literal,E6-h5-live-span-requirement,E7-h5-location-conjunct
```

**The receipt's frozen duty is discharged.** Every mutant that corresponds to a receipt-disclosed
shadowed clause is caught by the wave-1 selftest as built:

| receipt disclosure | my equivalent mutant | selftest verdict |
|---|---|---|
| (a) H1a counts-loose | `A7-h1-counts-loose` | CAUGHT (`failures=1`) |
| (a) H1b raw-loose | `A4-one-live-row-loosened` | CAUGHT (`failures=1`) |
| (b) H2b wordfloor-low | `H2b-h2-wordfloor-low` | CAUGHT (`failures=1`) |
| (c) H3a cells-loose | `C8-h3-cells-loose` | CAUGHT (`failures=1`) |
| (d) H4b quotes-low | `D3-quote-count-floor` | CAUGHT (`failures=1`) |
| (d) H4c distinct-dropped | `H4c-h4-distinct-dropped` | CAUGHT (`failures=1`) |
| (e) H5c pass-low | `E4-passed-floor` | CAUGHT (`failures=1`) |
| (f) H7a verdict-or | `G3-verdict-or` | UNCAUGHT — but proven **equivalent** by the sibling seat (`R46bExecSelftestF29.md`), so closable via the `--equivalent` map |
| (f) H7c okline-loose | `G2-ok-line-tab-dropped` | UNCAUGHT — likewise proven equivalent |

**The open exposure is 16 clauses that neither the receipt nor the wave-1 selftest grades.** They
are SURVIVORs at gate level *and* uncaught by the selftest, so neither the defect-tree corpus nor
the synthetic clause cases can see them:

`A2` (F29 entry cell must name ENTRY, `:172`), `A3` (the entry must not be shared with another
row, `:175`), `B4` (exactly one `recheck:` line, `:191`), `B5` (each table cell ≥ 2 words, `:199`),
`B6` (the `source: S074 — <URL> — ` provenance prefix, `:219`), `B7` (the exact `recheck:` line
form, `:191`), `C4` (the row's first URL must equal the canonical URL, `:250`), `C5` (the anchor
line locator's upper bound, `:246`), `C6` (`status == "mined"`, `:248`), `C7` (`opened == 2026-10-29`,
`:249`), `D2` (the `source-recheck.py` bytes pin, `:264`), `D4` (the `S074:sha256 OK` conjunct,
`:278`), `E5` (`uncited <= 0`, `:307`), `E6` (a frozen core must be *live* text, `:306`), `E7`
(the quoted span must be located **in the snapshot window**, `:300`), `F3` (the `nested == 66`
count, `:329`).

Two of these deserve a note, because "SURVIVOR" understates them:

* **`E7` (drop `and nq in window`) does not flip a verdict, but it destroys the meaning of the
  "located" counter.** On the junk tree the pristine gate reads `located=2 failed=5`; under `E7`
  it reads `located=7 failed=0` — every unlocatable quote is now counted as located. The tree
  stays red only because the *cores* conjunct still fails (`cores=0/5`). The gate's own read token
  no longer reports the truth it is supposed to report.
* **`F3` (relax `nested == 66`) is masked by its sibling conjunct**, because the `nestedmd` tree
  also violates `len(everything) == 66` (`entries=67`). Relaxing the nested count alone leaves the
  tree red on the other term — which is why the receipt's `H6a` mutant relaxes all three counts
  together and does flip it.

If the L1 freezes a battery table drawn from my recipes **and** the equivalent-proof map, the
f29 counter's `uncaught` would be **16**, not 0, unless the selftest gains ~16 more clause cases
(or equivalent proofs). This is a statement about *my* mutant set, not a defect in the wave-1
selftest, which was scoped to the receipt's disclosure list.

## Finding 10: the H5 "quoted text the source does not hold" property needs **two** lines to defeat

Two mutants that are individually SURVIVORs combine into a full escape from the junk and
fabricated trees. This is a 2-line edit, outside my single-line set, but it is the sharpest
statement of the H5 clause structure and I report it for completeness:

```
COMBO (2 lines: drop the location conjunct AND the cores conjunct) sha=25acbee79925
  positive    gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5 | f29-gate fixed=7/7 exit=0
  junk        gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=0/5 | f29-gate fixed=7/7 exit=0
  fabricated  gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=4/5 | f29-gate fixed=7/7 exit=0
```

Individually, `E7` (drop `and nq in window`) leaves the junk tree red (`located=7 failed=0` but
`cores=0/5`) and `E8` (drop the cores conjunct) leaves it red too (`located=2 failed=5`); together
the junk entry — quotes the snapshot does not hold — reads `fixed=7/7 exit=0`.

## Full verdict table for my 49 mutants

Counts over all 49: **12 FALSE-GREEN, 7 LIMP-FLIP, 2 POS-BREAK, 28 SURVIVOR** (of the 28
survivors, 2 are the deliberate no-op controls and 16 are the ungraded clauses of Finding 9).
The first 41 are tabulated in `matrix.tsv` (10 / 6 / 1 / 24); the last 8 come from the round-3 and
round-4 receipts (`round3.py`, `round4.py`).

```
A1-live-lines-fence-dropped      H1  FALSE-GREEN  fencedf29        <- beyond receipt (Finding 2)
A2-entry-cell-dropped            H1  SURVIVOR
A3-entry-shared-dropped          H1  SURVIVOR
A4-one-live-row-loosened         H1  SURVIVOR
A5-s074-boundary-widened         H1  FALSE-GREEN  src0740          <- receipt pair 3
A6-h1-count-line-disabled        H1  SURVIVOR
A7-h1-counts-loose               H1  SURVIVOR
B1-verified-at-prefix            H2  FALSE-GREEN  vjunk            <- receipt pair 4
B2-xref-need-dropped             H2  FALSE-GREEN  badnames         <- receipt pair 6
B3-table-rows-floor              H2  LIMP-FLIP    fewspans:H2      <- beyond receipt (Finding 5)
B4-recheck-count-loosened        H2  SURVIVOR
B5-cell-word-floor               H2  SURVIVOR
B6-h2-source-line-dropped        H2  SURVIVOR
B7-h2-recheck-form-loosened      H2  SURVIVOR
C1-scope-words-floor             H3  FALSE-GREEN  thinscope        <- receipt pair 8
C2-kind-literal-case             H3  LIMP-FLIP    kindcase:H3 (+positive break) <- receipt pair 9
C3-tier-literal                  H3  POS-BREAK
C4-url-equality-dropped          H3  SURVIVOR
C5-anchor-locator-range          H3  SURVIVOR
C6-h3-status-literal             H3  SURVIVOR
C7-h3-opened-literal             H3  SURVIVOR
C8-h3-cells-loose                H3  LIMP-FLIP    row12cells:H3    <- beyond receipt (Finding 6)
D1-manifest-pin-dropped          H4  FALSE-GREEN  manws            <- receipt pair 10
D2-recheck-pin-dropped           H4  SURVIVOR
D3-quote-count-floor             H4  SURVIVOR
D4-sha-ok-conjunct-dropped       H4  SURVIVOR
E1-span-width                    H5  FALSE-GREEN  widespan         <- receipt pair 13
E2-word-cap                      H5  FALSE-GREEN  longquote        <- receipt pair 14
E3-core-count                    H5  LIMP-FLIP    fewspans:H5      <- beyond receipt (Finding 5)
E4-passed-floor                  H5  SURVIVOR
E5-uncited-tolerance             H5  SURVIVOR
E6-h5-live-span-requirement      H5  SURVIVOR
E7-h5-location-conjunct          H5  SURVIVOR
E8-h5-cores-conjunct             H5  LIMP-FLIP    fewspans:H5
E9-h5-failed-conjunct            H5  FALSE-GREEN  widespan+longquote  <- beyond receipt (Finding 1)
E10-h5-passed-conjunct           H5  SURVIVOR
E11-h5-quoted-ascii-filter       H5  POS-BREAK
F1-entry-size-floor              H6  FALSE-GREEN  thinsection      <- beyond receipt (Finding 3)
F2-content-pin-dropped           H6  FALSE-GREEN  entrymutant     <- receipt pair 17
F3-nested-count                  H6  SURVIVOR
F4-symlink-clause-dropped        H6  LIMP-FLIP    symlink:H6       <- beyond receipt (Finding 5)
G1-symlink-guard-dropped         H7  LIMP-FLIP    symlink:H7       <- receipt pair 18
G2-ok-line-tab-dropped           H7  SURVIVOR
G3-verdict-or                    H7  SURVIVOR
H2b-h2-wordfloor-low             H2  SURVIVOR
H4c-h4-distinct-dropped          H4  SURVIVOR
H6a-h6-counts-loose              H6  FALSE-GREEN  nestedmd        <- receipt pair 16
Z0-do-nothing-whitespace         H1  SURVIVOR    (control)
Z1-do-nothing-comment            H6  SURVIVOR    (control)
```

## Limitations

* **My grading is against the shipped defect corpus, not against a real entry.** The F29 entry
  (`corpus/knowledge/github-repository-security-advisories.md`) does not exist at the freeze; the
  corpus's own fixture entry stands in. The counter pins the 65 other knowledge entries by name
  and content hash, so every tree had to be built from the lane's live corpus — the round-15
  pure export at `/fast/scratch/hyaku/kasegi-r46/L1/pure2` cannot satisfy those pins.
* **`src0740` is my own build.** The receipt names it; `controls/f29-defects.py` does not carry it.
  I reconstructed it from the receipt's parenthetical ("sources cell S0740") and verified by diff
  that only the F29 row's sources cell differs. If the L1 intends a different `src0740`, my
  `A5` result must be re-measured.
* **`row12cells` is my own build** (a twelve-cell S074 row), constructed to test receipt
  disclosure (c). It is not part of the shipped corpus.
* **I did not mutate the fleet-root census script**, so H7's output shape cannot be discriminated at
  gate level — my `G2`/`G3` reproduce the receipt's disclosure (f). The sibling seat's proof that
  both are *equivalent* (not merely uncaught) is not mine; I cite it as the sibling's, and my
  measurements are consistent with it.
* **The wave-1 selftest I graded against is a sibling's uncommitted draft**, not the landed
  `corpus/instruments/r46-selftest-f29.py`. My `caught=29/uncaught=20` figure describes that draft
  at sha256 `23b528a4…`; the L1's integration may change it.
* **`uncaught=20` counts two no-op controls**, which no selftest can catch; and `G2`/`G3`, which
  are closable as equivalents. The actionable number is **16** (Finding 9).
* The 2-line COMBO probe (Finding 10) is outside my single-line mutant set and is reported as
  structural evidence about the H5 clause set, not as a mutant in the battery.
* **No git/jj mutation, no commit, no push.** The lane's counter bytes are unchanged
  (hash identical before and after). The fleet repo, the sibling lanes, `MANIFEST.json` and
  `.ufo/state` were not touched.
* **No package was installed or upgraded** for this seat (Python 3.14.8 standard library only), so
  there is nothing to record under the tooling directive of 2026-10-19.

## Files changed

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/`
  (new; my seat's draft directory) — the nine driver scripts that produced every number above
  (`mutants.py`, `round2.py`, `round3.py`, `round4.py`, `round5.py`, `verify.py`, `regress.py`,
  `selftest_coverage.py`, `quote.py`), the machine-readable verdict matrix
  (`matrix.tsv`, `verify_full.txt`), the mutant-recipe list (`mutants.tsv`) and the selftest
  coverage receipt (`selftest_coverage.txt`).
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bMutF29b.md`
  (new; this report).

Nothing else in the lane, the fleet repo or the sibling lanes was written. Scratch
`/fast/scratch/hyaku/kasegi-r46/R46bMutF29b` was removed after the receipts above were copied into
the draft directory.
