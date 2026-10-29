# R46bScoutSelftestC2Gap — mutation walk: `r46-counters-selftest-c2.py` (137 cases) vs `C2_MUTANTS` (21)

VERDICT: DRAFT-READY

Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin. All runs read-only on the lane; scratch /fast/scratch/hyaku/kasegi-r46/R46bScoutSelftestC2Gap (removed at exit). No tool installs were needed or made. Working tree clean for all four instruments touched (`git status --porcelain` on r46-c2-gate.py, r46-counters-selftest-c2.py, r46-mutbat.py, r46-f29-gate.py: empty), so every byte graded below is the committed tip (counter v1.2, commit 93140c1; sha256 prefixes: counter `647bd5b7b6268551`, selftest `ff7104cfc8910071`). Lane tip is ee03806b (wave-spec commit, after freeze fe0f56b7) — the instrument files themselves are unchanged since the freeze commit.

## F1. Baseline re-run at tip — claim premise confirmed

Command: `TMPDIR=$S/tmp HYAKU_SCRATCH=$S python3 corpus/instruments/r46-counters-selftest-c2.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2` (S = my scratch).

Printed tail: `selftest cases=137 failures=0` (exit 0; wall 529.5 s; 137 `ok` lines, 0 `FAIL` lines; probes printed ACCEPTED, not counted).

Hazard noted: the selftest's built-in default is `PURE = "/fast/scratch/hyaku/kasegi-r46/L1/pure"` (selftest :46) and that path does not exist; `L1/` holds `pure2` (F-rows=27, knowledge_md=64, no round-46 snapshot — the correct round-45-shaped base). Every invocation must pass `--pure .../L1/pure2` explicitly, as the claims' canonical battery command already does.

## F2. Do-nothing control (non-vacuity discrimination)

Command: same as F1 plus `--do-nothing-control` (the harness swaps in a stub printing `gate G1..G7 pass=1` / `c2-gate fixed=7/7 exit=0`).

Printed tail (full 137-case run, 693 s wall, exit 1):

```
selftest cases=137 failures=118
```

118 = the 1 null case + all 117 mutant cases fail (`ACCEPTED-targeted-gate-passes` on every targeted gate); all 19 controls pass (the stub trivially reads 7/7). The harness therefore fails a counter that can never say red — the case grading is not vacuous.

## F3. Frozen before-value and per-mutant attribution

Frozen receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (L1's own battery run at the freeze point) prints, quoted:

```
mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0
```

with per-mutant `mutant_failures`: G1a=2, G1b=5, G1c=0, G2a=0, G2b=0, G2c=0, G3a=0, G3b=1, G3c=94, G4a=1, G4b=0, G4c=2, G5a=1, G5b=2, G5c=0, G6a=0, G6b=0, G6c=0, G7a=0, G7b=0, G7c=0. (C1 side of the same receipt: `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7` — outside my item, reported for context.)

I re-verified the decisive mutants myself by direct case-tree × counter runs (original vs battery-exact mutant copy, applied with the battery's assert-once rule; mutant copies placed under a `corpus/instruments/` tool-root exactly as `r46-mutbat.py apply_mutant` does). Classification of all 21:

| mutant | verdict | class | dedicated evidence |
|---|---|---|---|
| G1a-counts-loose | caught | dedicated | mf=2: `mut-duplicate-f-id`, `mut-extra-f29-row` (both targets={G1}) |
| G1b-path-dropped | caught | dedicated | mf=5: the five `mut-f28-entry-*` path cases (targets={G1}) |
| G1c-src-boundary | uncaught | fixable — new case (R1) | mf=0; no live F28 row ever carries S073 as a bare substring |
| G2a-verified-prefix | uncaught | fixable — new case (R2) | mf=0 |
| G2b-wordfloor-low | uncaught | fixable — new cases (R3a/R3b) | mf=0; both floors shadowed: table words count into the Scope section, and the thinnest real section (Limits) sits at 0 words only when emptied (fails the 5-floor too) |
| G2c-need-empty | uncaught | fixable — new case (R4) | mf=0; the obvious killer `mut-xref-ai-validation-missing` stays red via the `anchored` conjunct (Overlap drops to 1 knowledge ref) — verified |
| G3a-cells-loose | uncaught | equivalent-by-construction (E1) | mf=0; 12-cell craft stayed red under the mutant (run, see E1); <=10 cells → `row[10]` IndexError; >=12 cells shift the mined/date/recheck/used-by literals off positions 7-10 |
| G3b-scope-words-low | caught | dedicated | mf=1: `mut-row-scope-seven-words` |
| G3c-kind-dead | caught | collateral-only (94 control flips); dedicated case specified (R5) | mf=94 are controls/non-G3 mutants turning red (`docs != "Docs"`); no case has a `Docs` kind cell |
| G4a-manifest-unpinned | caught | dedicated | mf=1: `mut-manifest-trailing-newline` (recheck still parses → G4 green under mutant) |
| G4b-quotes-low | uncaught | fixable — new case (R6) | mf=0; every manifest edit is caught by the byte pin first; the two `mut-manifest-quote-removed-Q*` cases stay red at `oks>=8` too |
| G4c-distinct-dropped | caught | dedicated | mf=2: `mut-manifest-duplicate-quote-repinned`, `mut-manifest-six-distinct-anchors-repinned` |
| G5a-span-wide | caught | dedicated | mf=1: `mut-citation-13-lines` (12<=110; `mut-citation-1-589` does NOT flip: 588>110) |
| G5b-words-wide | caught | dedicated | mf=2: `mut-26-word-quote`, `mut-core-inside-33-word-span` |
| G5c-pass-low | uncaught | equivalent-by-arithmetic (E2) | mf=0; see E2 |
| G6a-guards-dead | uncaught | fixable — new case (R7) | mf=0; knowledge-internal symlinks always also break the counts/names pin; only the exempt-shrink guard is isolable |
| G6b-integrity-loose | uncaught | equivalent-by-construction (E3) | mf=0; see E3 |
| G6c-size-low | uncaught | fixable — new case (R8) | mf=0; the shipped builder's unpadded floor is 3284 bytes > 3000, so no existing tree can sit under the pin |
| G7a-verdict-or | uncaught | equivalent-by-census-contract (E4) | mf=0; see E4 |
| G7b-symlink-dead | uncaught | fixable — new case (R9) | mf=0 |
| G7c-okline-loose | uncaught | equivalent-by-census-contract (E5) | mf=0; see E5 |

## F4. The nine missing cases — exact recipes, each executed and proven

All recipes extend the selftest's case list (the `add(Case(...))` lines below drop in verbatim; helper functions named are existing selftest symbols: `sub`, `wr`, `f28_row`, `man_edit`, `land_c1`, `set_section`, `spans`, `XREF_A`, `ENTRY_REL`, `README`, `SOURCES`). Proof method per recipe: build the case tree, run the tip counter (expected target gate red), run the battery-exact mutant counter (expected target gate green → the case would report `ACCEPTED-targeted-gate-passes` → mutant caught). Quoted outputs are `orig-failing` / `mutant-failing` gate lists from my runs.

**R1 (G1c)** — G1 block, after `mut-extra-f29-row`:
```python
add(Case("mut-f28-sources-cell-S0730", "mutant", lambda r: sub(r, README, f28_row(), f28_row().replace("| S073 |", "| S0730 |")), {"G1"}))
```
Proof: orig=`['G1']`, G1c-mutant=`[]` — kills.

**R2 (G2a)** — G2 block:
```python
add(Case("mut-verified-at-trailing-note", "mutant", lambda r: sub(r, ENTRY_REL, "verified-at: 2026-10-28", "verified-at: 2026-10-28 (also checked 2026-10-27)"), {"G2"}))
```
Proof: orig=`['G2']`, G2a-mutant=`[]` — kills.

**R3a/R3b (G2b)** — needs the table out of every counted section (the gate's `sect_words` counts table cells into the Scope section, and its table scan is whole-body). Extend `entry_text()` with the table relocated to the preamble (after the pad line, before `## Scope and decision rule`), then:
```python
add(Case("mut-scope-16-words-table-in-preamble", "mutant",
         lambda r: (sub(r, ENTRY_REL,
             "This synthetic entry records what GitHub's own page says about reporting a security vulnerability privately to the maintainers of a public repository, from the reporter's side only (page body `S073.txt:556-579`). The table below lists each observed question with the page text and the consequence for a claim package.",
             "Word for word: the page says who may report; check enablement first at `S073.txt:564`."),), {"G2"}))
add(Case("mut-falsifiable-8-words", "mutant",
         lambda r: set_section(r, 3, "Check each stated step at `S073.txt:564`."), {"G2"}))
```
Proofs: scope variant orig=`['G2']`, mutant=`[]` (section measures 16 \w+ runs); falsifiable variant orig=`['G2']`, mutant=`[]` (section measures 8 runs: 8 < 12 original floor, 8 >= 1 mutant floor). Both kill. The relocation builder is the only new machinery: the complete-tree control keeps the table in Scope, so the relocation lives in a parametrised builder (e.g. `entry_text(spans, table_in_preamble=False)`), not in the case lambda.

**R4 (G2c)** — G2 xref block; swap the AI xref for a reference to a third real in-range file so `anchored` (>=2 Overlap refs) and `refok` stay green while `need` goes unsatisfied:
```python
add(Case("mut-xref-ai-swapped-for-other-file", "mutant",
         lambda r: sub(r, ENTRY_REL, XREF_A, "corpus/knowledge/" + spare + ":1-2"), {"G2"}))
```
(`spare` is the selftest's existing not-cross-referenced base file.) Proof: orig=`['G2']`, G2c-mutant=`[]` — kills.

**R5 (G3c, dedication)** — G3 block:
```python
add(Case("mut-row-kind-capitalised", "mutant", lambda r: sub(r, SOURCES, "| docs | A | The reporter-side", "| Docs | A | The reporter-side"), {"G3"}, allow={"G7"}))
```
Proof: orig=`['G3','G7']`, G3c-mutant=`['G7']` (G3 green; census E05 collateral allowed) — kills.

**R6 (G4b)** — repin block, after `mut-manifest-six-distinct-anchors-repinned`. The S073 manifest's five cores live in Q3/Q5/Q6/Q7/Q8 and anchors are [560,563,564,566,573,574,577,578], so dropping Q1 leaves 7 distinct quotes, 7 distinct anchors, all cores, recheck printing exactly 7 `OK` lines:
```python
add(Case("mut-manifest-seven-quotes-repinned", "mutant",
         lambda r: man_edit(r, lambda s: s.__setitem__("quotes", [q for q in s["quotes"] if q["id"] != "Q1"])),
         {"G4"}, repin=True, note="isolates the >= 8 quotes floor: 7 located OK quotes, cores intact, distinct, 7 anchors"))
```
Proof: orig=`['G4']`, G4b-mutant=`[]` — kills.

**R7 (G6a)** — G6 C1 block:
```python
add(Case("mut-c1-landed-exempt-entry-truncated", "mutant",
         lambda r: (land_c1(r), wr(r, "corpus/knowledge/claim-gates.md", b"x" * 64)), {"G6"}))
```
Names stay 65, content pin exempts the file, only the `EXEMPT_BASE_SIZE` floor (6742) goes red — the exact `grown` guard G6a deletes. Proof: orig=`['G6']`, G6a-mutant=`[]` — kills.

**R8 (G6c)** — needs a terse builder; the shipped `entry_text()` bottoms out at 3284 unpadded bytes (measured), above the 3000-byte pin. Add `entry_text_terse(spans)` (same skeleton, shorter prose; all four section floors still cleared: measured 234/60/25/15 words) and:
```python
add(Case("mut-entry-terse-2680-bytes", "mutant",
         lambda r: wr(r, ENTRY_REL, entry_text_terse(spans)), {"G6"},
         note="G6 byte floor: a G2-complete 2680-byte entry (measured) sits under the 3000-byte pin"))
```
Proof: orig=`['G6']` with read token `entry-bytes-ok=0`, G6c-mutant=`[]` — kills.

**R9 (G7b)** — G7 block:
```python
add(Case("mut-sources-md-symlink", "mutant",
         lambda r: (shutil.copyfile(os.path.join(r, SOURCES), os.path.join(r, "corpus/SOURCES-real.md")),
                    os.remove(os.path.join(r, SOURCES)),
                    os.symlink("SOURCES-real.md", os.path.join(r, SOURCES))), {"G7"}))
```
Proof: orig=`['G7']`, G7b-mutant=`[]` — the census validates through the symlink and prints its ok line, G3/G6 read through it unaffected — kills.

## F5. The five equivalents — proofs to commit for `--equivalent` (battery prints `equivalent=5, uncaught=0`)

**E1 (G3a, `==11` → `>=9`)**: a row flips a verdict only if `len(c) != 11` yet every positional check passes under the mutant. `len(c) in {9,10}` → `row[10]` raises IndexError → limb red (executed: ten-cell row under the mutant prints `gate G3 pass=0 read=exception-IndexError`). `len(c) >= 12` → the four tail literals (`mined`, `2026-10-28`, cadence, used-by path) must sit at positions 7-10, leaving exactly 3 slots (4-6) for the three content properties (scope>=8w, locator+sha, teaches>=8w) plus id/src/kind/tier at 0-3 = 8 pre-tail cells > 7 available — structurally impossible; executed 12-cell craft (duplicated anchor cell) stayed red under the mutant: orig=`['G3','G7']`, mutant=`['G3','G7']`. Same shape as the f29 receipt's disclosure (c).

**E2 (G5c, `>=4` → `>=1`)**: `ok` requires `cores == 5`; a span carrying two cores must hold both norm'd phrases within 25 words. Measured over the real capture (all 1-12-line windows, all 10 pairs): minimum pair window = 30 words (credit+merge); no pair fits <= 25. Hence cores==5 ⟹ >= 5 passed spans ⟹ `len(passed) >= 4` is implied by the cores conjunct and can never be the sole red limb. Executed no-flip: fabricated-quote tree (orig `['G5']`) stays `['G5']` under the mutant.

**E3 (G6b, drops `len(everything)==65 and nested==65`)**: any knowledge-dir addition changes `everything` and equally changes `base_like`, whose sha must equal `PINS["base-knowledge-names"]` (kept by the mutant) — a nested `.md` requires a new top-level directory, which also enters `listdir`. So every tree red via the dropped clauses is already red via `base_ok`. Executed no-flip: stray.txt tree (orig `['G6']`) stays `['G6']` under the mutant.

**E4 (G7a, `and` → `or`)**: the census emits its ok line only on a clean lane — `scripts/sources-census.sh:745`: `[ "$lane_errors" = 1 ] || emit "$lane	ok	$f"`. Measured: pristine tree rc=0 with exactly one `file	ok	<path>` line; bad-kind tree rc=1 with zero ok lines. Hence ok_line ⟹ rc==0, so `rc == 0 or ok_line` ≡ `rc == 0` ≡ the original conjunct. Executed no-flip: bad-kind tree (orig `['G3','G7']`) stays red under the mutant.

**E5 (G7c, drops trailing `\t`)**: the census's only `ok` emission is `file\tok\t<path>` (line 745), which matches both regexes; no census output line matches `^\S+\tok` without a trailing tab. The relaxed regex is extension-free on census output. Executed no-flip: bad-kind tree stays red under the mutant.

## F6. Receipt sections (a), (b), (d), (e) — how the wave-1 f29 selftest with rebuilt PINS grades each

Grounded in `corpus/instruments/r46-f29-gate.py` (read in full; H1-H7 as documented). Key mechanism fact: the f29 gate has **no** pins-override env hook (unlike the c2 gate's `R46_PINS_OVERRIDE`), so "rebuilt PINS" means the selftest writes a scratch copy of the gate with the `PINS` sha literals substituted (assert-once replacements, the battery's own `apply_mutant` discipline), or imports the module and patches `PINS` before invoking limbs.

**(a) H1a counts / H1b one-live-row.** H1a: synthetic frontier tables with a controlled id set — (i) append `| F30 | extra | admitted | knowledge/<spare>.md | S075 | n |` (unique id, unique entry path → dup=0, ENTRY unshared): H1 red with read `rows=30 admitted=30 dup=0`, counts clause isolated; (ii) delete one non-F29 base row → `rows=28`. These are the trees the receipt says "no single-defect tree isolates" — true for *defect* trees, false for synthetic ones. H1b: the clause is dead code — the `raw` list and the frontier's F29 filter are the same live-line predicate, so `len(raw)!=1` ⟺ F29-count != 1, already returned at `F29-row-or-entry-missing` (0 rows) or at `dup` (>=2 rows, checked earlier). Grade H1b as an equivalence proof (same class as E3 above), with the synthetic duprow tree as the exhibited nearest approach (H1 red with `dup=1`, never `F29-row-not-one-live-line`).

**(b) H2b per-section word floor.** h2's table scan is whole-body while the word floor is per-section (`sect_words` over the heading span) — identical structure to the c2 G2b I proved. Recipe: synthetic entry with the table under its own heading outside the four sections + one section thinned to 10-24 words keeping its anchored cite. Original H2 red only at `full=3/4`; the H2b-loose mutant (25→5) turns it green. The pattern is already proven on the twin gate (R3a: orig=`['G2']`, mutant=`[]`).

**(d) H4b quotes-low / H4c distinct-dropped.** The manifest byte pin shadows both (any quote edit is red at the pin first). Repin trio, porting the c2 selftest's `repin=True` machinery to rebuilt PINS: (d0) control — re-serialised manifest, pins rebuilt to its bytes, nothing else edited → H4 green (validates the repin mechanism itself); (d1) drop one non-core quote from the S074 record (cores intact, >=7 distinct anchors, recheck prints 7 OK) → H4 red only at `oks>=8` → kills H4b-loose (pattern proven: R6); (d2) duplicate one quote, repinned → red only at `distinct` → kills H4c-dropped (pattern proven: mf=2 on the twin gate).

**(e) H5c located>=4 floor.** Same conjunct layout as c2 G5c. Measured on the real S074 capture: no two of the five H5 cores fit any <=25-word/<=12-line window (all 10 pairs checked; closest pair needs 30+ words), so cores==5 ⟹ passed>=5 and the `>=4` floor is implied — H5c-pass-low is equivalent-by-arithmetic (mirror of E2). If L1 wants the floor genuinely exercised instead of disclosed: rebuild the snapshot and manifest synthetically (pack >=2 cores per line), rebuild `PINS["S074.txt"]`/`PINS["manifest.json"]` in the scratch gate copy, and build an entry with exactly 3 located spans carrying all 5 cores → original H5 red only at the floor → the relaxed mutant flips. Primary recommendation: the equivalence proof (it matches the receipt's own framing and needs no fixture machinery).

## F7. Integration requirements for the C1 claim (`uncaught=0` printed)

1. Land R1-R9 (eight killing cases; R5 is the optional G3c dedication — G3c is already caught via 94 collateral control flips).
2. Commit the five equivalence proofs (E1-E5) as files and pass `--equivalent map.json` to the battery; without the MAP the battery prints `uncaught=5` even with all cases landed, because its only predicates are caught and committed-equivalent (`r46-mutbat.py:8-14`).
3. Re-run `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work <scratch> --counter both --jobs 8` and expect `mutbat counter=c2 mutants=21 caught=16 equivalent=5 uncaught=0 baseline_failures=0`.
4. Expected post-landing per-mutant mf (my runs): G1c=1, G2a=1, G2b>=1, G2c=1, G4b=1, G6a=1, G6c=1, G7b=1, plus the pre-existing 8.

## Limitations

- I did not re-run the full 22-invocation battery (22 × ~530 s ≈ 3.2 h); the caught/uncaught column for the 8 already-caught mutants and the aggregate line are quoted from the frozen receipt `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`, and every mutant I propose to change state was graded by direct execution of the exact battery edit against the exact case tree (16 counter runs + 2 census probes, all quoted).
- The mf counts (e.g. G1b=5, G5b=2) are taken from the receipt, not re-attributed case-by-case; my dedicated/collateral attribution for those rests on the case table's `targets=` sets plus the receipt's counts, which agree everywhere I checked.
- The S073/S074 pair-window measurements scan normalised 1-12-line windows of the real captures; they bound the gate's own <=25-word/<=12-line span test but do not model every exotic quoting path.
- pure2 was consumed as-found on disk (27 F-rows, 64 knowledge files); I did not re-verify its sha against any manifest.

