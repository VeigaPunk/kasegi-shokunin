VERDICT: DRAFT-READY

# Seat R46bExecSelftestF29 — wave-1 selftest for the F29 counter (round 46 attempt 2, C2)

## What I built

One file, the wave-1 deliverable named by the seat card:

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`
(sha256 `23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d`, 906 lines. The L1 integrates
it to `corpus/instruments/r46-selftest-f29.py`; it is NOT committed by me.)

Stdlib only, no git, read-only on `--lane` and `--pure`, scratch under
`$HYAKU_SCRATCH/kasegi-r46/R46bExecSelftestF29` (removed on exit unless `--keep`).
It honours `TMPDIR`/`--work`, accepts `--lane`, `--counter`, `--work`, `--pure`, `--jobs`,
`--do-nothing-control`, `--keep`, `-v`.

Tree recipes are vendored from the two control builders
(`.ufo/waves/round-46/attempt2/controls/f29-fixture.py`, `.../f29-defects.py`); the selftest
prints a provenance line per builder and compares its sha256 against the vendored value, so a
recipe drift is visible instead of silent:

```
note provenance f29-defects.py sha256=2e95d4d4b6cf372a8464803bf82c7ae79d1612dc8060b5a9c18798cfbcbc07c2 matches
note provenance f29-fixture.py sha256=52ea96939c62a71943838ca883d7914dd598f3e7eeb061266975ece7ccb26275 matches
```

## Grading method

Each case is graded **in process** against the imported counter's own `GATES` list, replicating
the counter's `main()` loop including its "a limb that raises is red, never green" rule. The
The import is what makes the shadowed clauses gradeable: the F29 counter has **no**
`R46_PINS_OVERRIDE`-style hook (verified: `grep -n "PINS_OVERRIDE\|getenv"
corpus/instruments/r46-f29-gate.py` → no match), so the selftest overrides `PINS` (and, for the
one H1 clause only, the `frontier` reader) on the imported module for that case's fixture and
restores it immediately afterwards. Nothing outside the case's own tree is touched. The receipt
names four shadowed disclosures ((a), (b), (d), (e)); all four are graded, and the receipt's
disclosure (c) is graded too, because it turns out not to hold (see below).

Command (my own re-run, from the seat scratch):

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py
```

Output (tail):

```
ok   ctl     positive               fixed=7/7 failing=[]
ok   ctl     junk                   fixed=6/7 failing=['H5']
ok   ctl     fabricated             fixed=6/7 failing=['H5']
ok   defect  defect-duprow          fixed=6/7 failing=['H1']
ok   defect  defect-fencedf29       fixed=6/7 failing=['H1']
ok   defect  defect-src0740         fixed=6/7 failing=['H1']
ok   defect  defect-vjunk           fixed=6/7 failing=['H2']
ok   defect  defect-thinsection     fixed=6/7 failing=['H6']
ok   defect  defect-badnames        fixed=6/7 failing=['H2']
ok   defect  defect-row9cells       fixed=5/7 failing=['H3', 'H7']
ok   defect  defect-thinscope       fixed=6/7 failing=['H3']
ok   defect  defect-kindcase        fixed=5/7 failing=['H3', 'H7']
ok   defect  defect-manws           fixed=6/7 failing=['H4']
ok   defect  defect-fewquotes       fixed=6/7 failing=['H4']
ok   defect  defect-dupquote        fixed=6/7 failing=['H4']
ok   defect  defect-widespan        fixed=6/7 failing=['H5']
ok   defect  defect-longquote       fixed=6/7 failing=['H5']
ok   defect  defect-fewspans        fixed=5/7 failing=['H2', 'H5']
ok   defect  defect-nestedmd        fixed=6/7 failing=['H6']
ok   defect  defect-entrymutant     fixed=6/7 failing=['H6']
ok   defect  defect-symlink         fixed=5/7 failing=['H6', 'H7']
ok   clause  clause-a-counts-30     fixed=6/7 failing=['H1']
ok   clause  clause-a-counts-28     fixed=6/7 failing=['H1']
ok   clause  clause-a-raw-once      fixed=6/7 failing=['H1']
ok   clause  clause-b-wordfloor     fixed=6/7 failing=['H2']
ok   clause  clause-d-quotecount    fixed=6/7 failing=['H4']
ok   clause  clause-d-distinct      fixed=6/7 failing=['H4']
ok   clause  clause-e-located       fixed=6/7 failing=['H5']
ok   clause  clause-c-cells-12      fixed=5/7 failing=['H3', 'H7']
ok   ctl     positive-cli           rc=0 gates=7 summary=['f29-gate fixed=7/7 exit=0']
selftest cases=30 failures=0
```

Exit status 0. `selftest cases=<N> failures=<F>` is printed last, so the mutation battery's
`failures=(\d+)` probe reads it (`r46-mutbat.py:run_selftest`).

Final re-run of the delivered file (sha256 `23b528a4…`), after the last edit:

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py
…
ok   clause  clause-c-cells-12      fixed=5/7 failing=['H3', 'H7']
ok   ctl     positive-cli           rc=0 gates=7 summary=['f29-gate fixed=7/7 exit=0']
selftest cases=30 failures=0
```

Exit status 0, 30 `ok` lines, 0 `FAIL` lines.

## Case inventory and what each one pins down

### (1) the positive tree (7/7)

`ctl positive` grades all seven limbs green; `ctl positive-cli` additionally runs the counter's
own CLI on the same tree and requires seven `gate H<n> pass=1` lines and
`f29-gate fixed=7/7 exit=0`:

```
$ python3 corpus/instruments/r46-f29-gate.py --root $S/trees/positive --work $S/tmp/w1
gate H1 pass=1 read=rows=29 admitted=29 F29=admitted
gate H2 pass=1 read=source=1 verified-at=1 recheck=1 sections=4/4 full=4/4 table-rows=6 xrefs=2/2 anchored=1
gate H3 pass=1 read=row-S074=ok
gate H4 pass=1 read=recheck-rc=0 quotes-ok=9 frozen-cores-missing=0
gate H5 pass=1 read=spans=7 located=7 failed=0 uncited=0 cores=5/5
gate H6 pass=1 read=knowledge=66 entries=66 nested-md=66 base-intact=1 entry-bytes-ok=1 symlinks=0
gate H7 pass=1 read=census-rc=0 ok-line=1
f29-gate fixed=7/7 exit=0
```

### (2) every defect tree of the receipt

All 18 rows of the receipt's defect table (17 from `f29-defects.py` plus `src0740`, the one
defect the receipt names that the control builder does not carry — the F29 row's sources cell
reads `S0740`, which the selftest builds itself). Every case asserts the **exact** set of red
limbs, so collateral failures are caught too.

### (3) the gate-level-shadowed clauses

| disclosure | clause | isolating fixture | base reads |
|---|---|---|---|
| (a) | H1 row/duplicate count | `clause-a-counts-30` (30 admitted rows, unique ids) and `clause-a-counts-28` (28 admitted rows, unique ids) — both keep F29 present, admitted, sole and one-live, so only the count term fires | `H1 pass=0 read=rows=30 admitted=30 dup=0` / `rows=28 admitted=28 dup=0` |
| (a) | H1 one-live-F29-row clause | `clause-a-raw-once`: two live F29 rows over a **controlled id set** (the README's own 29 unique rows, duplicate F29 dropped from the graded id set only) | `H1 pass=0 read=F29-row-not-one-live-line` |
| (b) | H2 per-section word floor | `clause-b-wordfloor`: the Scope section is cut to 21 words and its six-row table moves into its own `## Evidence table` section, so the table-row conjunct cannot shadow the floor | `H2 pass=0 read=… full=3/4 table-rows=6 …` |
| (d) | H4 ≥ 8 quote floor | `clause-d-quotecount`: seven valid quotes (all five cores, seven distinct anchors) on a manifest re-pinned to its edited bytes | `H4 pass=0 read=recheck-rc=0 quotes-ok=7 frozen-cores-missing=0` |
| (d) | H4 quote distinctness | `clause-d-distinct`: ten quotes of which one text is duplicated, on a re-pinned manifest | `H4 pass=0 read=recheck-rc=0 quotes-ok=10 frozen-cores-missing=0` |
| (e) | H5 ≥ 4 located spans | `clause-e-located`: a rebuilt-PINS **synthetic capture** whose lines 10-11, 24-25 and 38 carry the five frozen cores, so three located spans hold all five; the entry keeps six cited table rows and exactly three quoted spans | `H5 pass=0 read=spans=3 located=3 failed=0 uncited=0 cores=5/5` |
| (c) | H3 11-cell row shape | `clause-c-cells-12`: a twelve-cell S074 row | `H3 pass=0 read=row-S074=absent-or-malformed-or-not-registry-only hits=1` |

## Discrimination: the selftest catches 19 of 21 natural mutants

Scratch harness (copied into this seat's draft dir as
`r46-selftest-f29-mutprobe.py`, receipt `r46-selftest-f29-mutprobe.txt`) copies
`corpus/instruments/` per mutant, applies one single-line edit to a copy of
`r46-f29-gate.py`, and runs the selftest with `--counter <mutant copy>`; a mutant is *caught*
when the selftest reports `failures>=1` (the battery's own predicate). The mutant ids are the
receipt's own names; the edits are the natural single-line relaxations.

```
probe exit=0
mutant=H1a-counts-loose         caught mutant_failures=1
mutant=H1b-raw-loose            caught mutant_failures=1
mutant=H1c-src-boundary         caught mutant_failures=1
mutant=H2a-verified-loose       caught mutant_failures=1
mutant=H2b-wordfloor-low        caught mutant_failures=1
mutant=H2c-need-empty           caught mutant_failures=1
mutant=H3a-cells-loose          caught mutant_failures=1
mutant=H3b-scope-low            caught mutant_failures=1
mutant=H3c-kind-dead            caught mutant_failures=27
mutant=H4a-manifest-unpinned    caught mutant_failures=1
mutant=H4b-quotes-low           caught mutant_failures=1
mutant=H4c-distinct-dropped     caught mutant_failures=1
mutant=H5a-span-wide            caught mutant_failures=1
mutant=H5b-words-wide           caught mutant_failures=1
mutant=H5c-pass-low             caught mutant_failures=1
mutant=H6a-counts-loose         caught mutant_failures=1
mutant=H6b-pin-dropped          caught mutant_failures=1
mutant=H6c-size-low             caught mutant_failures=1
mutant=H7a-verdict-or           uncaught mutant_failures=0
mutant=H7b-symlink-dead         caught mutant_failures=1
mutant=H7c-okline-loose         uncaught mutant_failures=0
mutants=21 caught=19
```

The two remaining uncaught mutants are **provably equivalent**, not holes:

* `H7a-verdict-or` turns `return p.returncode == 0 and ok_line` into `or`. In the fleet census's
  `validate` mode the ok line is emitted iff there is no E-code
  (`scripts/sources-census.sh:745`: `[ "$lane_errors" = 1 ] || emit "$lane	ok	$f"`), and the
  script's exit code is non-zero exactly when there is an E-code. So on every tree
  `rc == 0 ⇔ ok_line == 1`, and `and` ≡ `or`. Confirmed on a hand-made registry:
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $T/corpus/SOURCES.md`
  prints `file	ok	$T/corpus/SOURCES.md` and `rc=0`; a malformed row prints no ok line and
  `rc=1`. No tree can separate the two operators.
* `H7c-okline-loose` turns the ok-line regex `^\S+\tok\t` into `^\S+\tok`. The census emits the
  ok line as `lane<TAB>ok<TAB>value`, so the tab the strict regex demands is always there; the
  relaxed regex adds no match on any census output. Also equivalent.

Both belong in the battery's `--equivalent` map (with the receipts above), not in a selftest
catch. This is exactly the receipt's disclosure (f) ("the census script lives at the fleet root
and is not mutated by this lane"); my finding sharpens it: they are *equivalent*, so the L1 can
close them with a proof instead of leaving them uncaught.

`H3a-cells-loose` (the 11-cell shape relaxed to `len(c) >= 9`) was caught by the new
`clause-c-cells-12` case: the receipt's disclosure (c) claims the relaxation "is closed by
construction (a 9-cell row cannot satisfy the positional checks)", which is true for nine- and
ten-cell rows (the positional checks then read `row[9]`/`row[10]` and fail or raise), but **not**
for a twelve-cell row: the relaxed mutant parses the first eleven cells and reads H3 green while
the base counter reads it red. The receipt's disclosure (c) is therefore too strong; the clause
is isolable and the selftest now grades it.

## Do-nothing control

`--do-nothing-control` grades every case against a stub counter whose seven limbs always read
green. Every red-expecting case must then be reported FAIL and the all-green case must still
pass; an unexpected outcome is counted as a failure.

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py --do-nothing-control
note do-nothing control counter: …/work/do-nothing-counter.py
FAIL ctl     junk                   fixed=7/7 failing=[]  <- expected-red=['H5'] actual-red=[]; tree read 7/7
FAIL defect  defect-duprow          fixed=7/7 failing=[]  <- expected-red=['H1'] actual-red=[]; tree read 7/7
…
FAIL clause  clause-e-located       fixed=7/7 failing=[]  <- expected-red=['H5'] actual-red=[]; tree read 7/7
ok   ctl     positive               fixed=7/7 failing=[]
FAIL ctl     positive-cli           rc=0 gates=0 summary=[]
note control: the stub counter reads green everywhere; every red-expecting case must be reported FAIL (unexpected outcomes counted as failures above)
selftest cases=30 failures=0
```

Exit status 0: 29 red-expecting cases reported FAIL, the one all-green case reported ok, the CLI
case failed (the stub has no CLI), and no unexpected outcome. So the suite is not satisfiable by
a counter that simply reports success.

## Discrepancies against the frozen receipt (measured, not inferred)

1. **The receipt's junk/fabricated readings are wrong.** The receipt header says
   `junk tree fixed=3/7 (H2/H5 red: 2/7 quotes located, 0/5 cores)` and
   `fabricated tree fixed=3/7 (5/7 located, 4/5 cores)`. The located/cores halves reproduce
   exactly, but the fixed counts do not: with the committed builders and the committed counter I
   measure `fixed=6/7` for both (only H5 red):

```
=== mode=junk
gate H5 pass=0 read=spans=7 located=2 failed=5 uncited=0 cores=0/5
f29-gate fixed=6/7 exit=1
=== mode=fabricated
gate H5 pass=0 read=spans=7 located=5 failed=2 uncited=0 cores=4/5
f29-gate fixed=6/7 exit=1
```

   H2 stays green on both trees (the junk/fabricated rewrites keep the table shape, the cites and
   the section floors), so the receipt's "H2/H5 red" does not reproduce. My selftest encodes the
   measured clause-level reading (H5 red, every other limb green); the L1 may want to amend the
   receipt text at integration (the receipt is a control record, not a counter).

2. **`thinsection` does not trip H2.** The receipt pairs `thinsection` with `H2b wordfloor-low`
   and records `H2=1 | H2=1`; my run confirms H2 stays green (the section keeps its six-row table,
   so the section's word count stays above 25). The defect's real effect is H6: the shortened
   entry falls under the 3000-byte floor (`gate H6 pass=0 read=… entry-bytes-ok=0`). The receipt
   does not record that. My selftest expects `H6` red for that tree and `H2` green.

3. **`fewspans` trips two limbs.** The receipt lists `H5=0` for `fewspans`; the tree also trips
   H2, because dropping the G6 row leaves five table rows under the `>= 6` conjunct
   (`gate H2 pass=0 read=… table-rows=5 …`, `gate H5 pass=0 read=spans=6 located=6 failed=0 uncited=0 cores=4/5`).
   The receipt's pairing table records only the paired limb, so this is a recording gap, not a
   contradiction.

4. **`row9cells` and `kindcase` also trip H7.** The receipt's pair 19 already records
   `H7=0` on the `row9cells` tree; the same holds for `kindcase` (the census rejects the `Docs`
   enum: `gate H7 pass=0 read=census-rc=1 ok-line=0`). My selftest expects both limbs red.

## Limitations

* The selftest builds its trees from the **lane's committed corpus** (`--lane`), not from
  `--pure`: the F29 counter pins the 65 other knowledge entries by name and by content hash, and
  the available pure export (`/fast/scratch/hyaku/kasegi-r46/L1/pure2`, a round-15 base export)
  holds 64 knowledge files, which cannot satisfy the pins. `--pure` is accepted for interface
  parity with the C1/C2 selftests and is ignored. If the lane's knowledge directory ever drifts
  from the freeze tip, the positive tree stops reading 7/7 and the selftest says so.
* The F29 entry's bytes are not pinned by the counter, so the selftest's own entry fixtures are
  free text; they are graded by the counter's clauses, not against the future real entry. The
  real entry (authored elsewhere in this wave) is not exercised by this selftest.
* `clause-a-raw-once` is the one case that cannot be built from files alone: the counter derives
  its "one live F29 row" clause from the same regex it uses to count rows, so a duplicate F29 row
  always trips the duplicate-id clause first. The clause is therefore graded with a controlled id
  set (the receipt's own prescription: "the wave-1 selftest grades them on synthetic tables with
  a controlled id set"). The override is restored immediately and touches only the imported
  module of the case under test.
* `clause-e-located` needs a synthetic capture because the real capture's five frozen cores sit
  too far apart (lines 10, 13, 24, 25, 38) for three ≤ 25-word located spans to carry all five;
  the case therefore re-pins both the capture and the manifest for its fixture only. It is a
  fixture-level grade of the floor clause, not a claim about the real capture.
* The mutation evidence above uses my own natural single-line relaxations under the receipt's
  mutant names; the frozen mutant table for `--counter f29` is not in the tree
  (`r46-mutbat.py` currently knows `c1` and `c2` only), and `r46-mutbat.py` is a shared
  production file that this seat may not edit. The battery extension and its `--equivalent`
  proofs for `H7a`/`H7c` are the L1's to land.
* No package was installed or upgraded for this seat (stdlib only); nothing to record under the
  tooling directive.

## Files changed

* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`
  (new; the wave-1 deliverable — the L1 integrates it to `corpus/instruments/r46-selftest-f29.py`)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.py`
  (new; the mutation harness that produced the receipt below, kept as evidence)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.txt`
  (new; the mutation receipt: `mutants=21 caught=19`)
* `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.md`
  (new; this report)

Nothing else in the lane, the fleet repo or the sibling lanes was written; no git or jj command
was run that mutates state. The seat scratch
`/fast/scratch/hyaku/kasegi-r46/R46bExecSelftestF29` was removed after the runs above (the
receipts were copied into the draft dir first).
