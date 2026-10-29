# Seat R46bExecMutbatF29 — r46-mutbat.py v1 → v1.1 (f29 counter extension)

VERDICT: DRAFT-READY

## What was built

`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/r46-mutbat.py` — the complete v1.1 battery (draft only; nothing committed, lane untouched):

- Frozen `F29_MUTANTS` table: 21 triples against `corpus/instruments/r46-f29-gate.py` (3 per limb H1–H7), the R50 pre-freeze mutant set of `.ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt`. Every old substring occurs EXACTLY ONCE in the gate (verified, see below), so each edit is content-addressed and a drifted gate fails loudly.
- `--counter f29` grading with the same caught/equivalent/uncaught predicate and output lines as c1/c2 (`mutbat counter=f29 mutants=21 caught=<k> equivalent=<e> uncaught=<u> baseline_failures=0`).
- f29 grader selection: the f29 selftest when present — the wave-1 draft `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py`, else the committed `corpus/instruments/r46-selftest-f29.py` — invoked via `--counter <mutant gate>` (its CLI is probed from `--help`; `--root`/`--lane` with a mutant tree copy is the fallback shape). When neither selftest is present, the grader falls back to the R50 fixture corpus (`controls/f29-fixture.py` + `controls/f29-defects.py`, plus the receipt's pair-3 `src0740` tree which the shipped `f29-defects.py` does not build): pristine vs mutated gate over all 21 corpus trees, a mutant is caught when any tree's limb-verdict map differs.
- `--counter` choices are now `c1|c2|f29|both|all`; `both` keeps its exact v1 semantics (c1+c2 only) so the frozen C1 claim's `counter_cmd` and the before-value replay remain byte-stable; `all` = c1+c2+f29.
- `--list` now prints all three tables (required).

## Evidence (commands run by me, outputs quoted)

1. c1/c2 byte-compatibility — the c1/c2 mutant-table region and the `run_selftest`/`apply_mutant` helpers were spliced verbatim from the committed v1, then checked:

```
$ python3 verify.py   # imports both modules, compares parsed tables + function bytecode
== (a) c1/c2 tables byte-identical to v1 ==
  c1 identical=True (20 mutants)
  c2 identical=True (21 mutants)
  COUNTER selftest names c1/c2 unchanged: True
  c1/c2 run_selftest body identical: True
  c1/c2 apply_mutant body identical: True
```

2. f29 triples content-addressed — every old substring occurs exactly once in `r46-f29-gate.py`:

```
== (b) f29 triple uniqueness against r46-f29-gate.py ==
  all-unique: True (21 mutants)
```

3. `--list` prints all three tables:

```
== (d) --list prints all three ==
  rc=0 lines=62 prefixes={'c1': 20, 'c2': 21, 'f29': 21}
```

4. Battery f29 run on scratch (fixture-fallback grader; no f29 selftest exists yet) — reproduced three times (`receipts/f29-run1.txt`, `f29-run2.txt`, `f29-run3-sepwork.txt`; identical 21-mutant classification):

```
$ python3 <draft>/r46-mutbat.py --root <lane> --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 \
    --work /fast/scratch/hyaku/kasegi-r46/R46bExecMutbatF29/sepwork --counter f29 --jobs 8
mutant=H1c-src-boundary baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H2a-verified-loose baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H2c-need-empty baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H3b-scope-low baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H3c-kind-dead baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H4a-manifest-unpinned baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H5a-span-wide baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H5b-words-wide baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H6a-counts-loose baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H6b-pin-dropped baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H7b-symlink-dead baseline_failures=0 mutant_failures=1 verdict=caught
mutant=H1b-raw-loose baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=H7a-verdict-or baseline_failures=0 mutant_failures=0 verdict=uncaught
mutant=H7c-okline-loose baseline_failures=0 mutant_failures=0 verdict=uncaught
mutbat counter=f29 mutants=21 caught=18 equivalent=0 uncaught=3 baseline_failures=0   [exit=1]
```
The 11 mutants the receipt records as defect-tree flips (H1c, H2a, H2c, H3b, H3c, H4a, H5a, H5b, H6a, H6b, H7b) are all caught ✓. The 3 uncaught are exactly the provably shadowed/census-dependent ones: H1b (the raw one-live-row clause is dead code: raw==0 ⟹ the F29-presence clause trips; raw≥2 ⟹ dup≥1 ⟹ the counts clause trips), H7a/H7c (census-output-shape mutants; the census script lives at the fleet root and a rc==0 census never lacks the ok line — receipt disclosure (f)). These need the wave-1 selftest's shadowed-clause cases and/or `--equivalent` proofs to reach `uncaught=0`, exactly as the receipt's frozen duty states.

5. Independent per-tree reproduction of the receipt's pairing (first probe run, per-mutant paired-tree limb checks): the receipt's 20 paired rows reproduced (H1c src0740 H1 0→1; H2a vjunk H2 0→1; H2c badnames H2 0→1; H3b thinscope H3 0→1; H4a manws H4 0→1; H5a widespan/longquote H5 0→1; H6a nestedmd/H6b entrymutant H6 0→1; H7b symlink H7 0→1; H1a/H1b/H2b/H3a/H4b/H4c/H5c/H7a/H7c no flip), and the fixture-fallback run also catches mutants beyond their paired tree (whole-corpus grading). Note the fallback's uncaught set (3) is smaller than the receipt's not-shown set (10) because it grades every tree, not only the paired one.

## Findings / risks for the L1

- Receipt gap: the R50 receipt claims 21 mutants ("3 per limb H1-H7") but its pairing table names only 20 and its disclosures name only 9 of the 10 not-shown; H6c is neither paired nor disclosed. I derived `H6c-size-low` as the exact C2 `G6c-size-low` analogue (the clause text `os.path.getsize(os.path.join(root, p)) >= 3000` exists verbatim in f29-gate); it is caught by the fixture corpus (thinsection H6 0→1, the trimmed entry drops below 3000 bytes). Flag: the receipt's own accounting has a one-mutant gap.
- H3c direction: the receipt's row 9 (kindcase → H3c → H3=0 → H3=1) requires the mutant to ACCEPT the "Docs" spelling, so H3c relaxes `!= "docs"` to `not in ("docs", "Docs")` — not the C2 G3c literal-swap (`!= "Docs"`), which would false-red every normal tree. Both satisfy row 9 in isolation; the targeted relaxation is the one shipped.
- H1b direction: `raw-loose` could be `> 1` (accept zero live F29 lines) or `< 1` (accept duplicates); both are provably non-flipping at gate level (the raw clause is belt-and-braces dead code), so the receipt cannot discriminate. Shipped `> 1` to match the paired fencedf29 scenario (raw becomes 0).
- H1a keeps `or dup:` in its new text (mirrors receipt disclosure (a): a duplicate row "also trips `dup`").

## Limitations

- The mandated `--counter c1` line-equality re-run was NOT executed: it is a full battery pass (20 mutant selftest runs; a single c1 selftest run exceeded the 300 s job cap in my probing) and the L1 instructed no new full battery passes. Compensating evidence: the c1/c2 path in the draft is byte-identical to v1 (tables, helpers, bytecode — item 1), so the c1/c2 summaries are reproduced by construction. The wave-2 final measure (`final-measure.sh`) runs it; expect `mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0` and `mutbat counter=c2 mutants=21 caught=8 equivalent=0 uncaught=13 baseline_failures=0` against the untouched base selftests.
- The f29 selftest grader is untested end-to-end: the sibling draft `r46-selftest-f29.py` did not exist during this seat. The battery probes the selftest's `--help` and needs `--counter PATH` (the c1/c2 convention) or a tree-taking `--root`/`--lane`; if it advertises neither, the f29 mode falls back to the fixture corpus and prints a NO-GRADER line only when both are absent. Coordinate the `--counter PATH` contract with R46bExecSelftestF29 before the wave-2 measure.
- UNRESOLVED ANOMALY (needs one L1 look before integration): in all three battery f29 passes (receipts `f29-run1.txt`, `f29-run2.txt`, `f29-run3-sepwork.txt` in the draft's `receipts/`), H1a-counts-loose — and every other mutant the receipt records as not-shown (H2b, H3a, H4b, H4c, H5c, H6c) — printed `mutant_failures=1 verdict=caught`, i.e. the fallback grader found exactly one corpus tree whose verdict map changed. But four isolated single-mutant re-runs of H1a over freshly built identical corpora (direct script, apply_mutant path, instrumented in-process `grade_f29`, and a post-run diff against the surviving `sepwork` corpus) found NO verdict difference for H1a on any of the 21 trees. The battery subprocess runs and the in-process runs differ only in environment (the battery runs set TMPDIR inside the work dir; the harness purged two of the three work corpora at job completion, which is why the third run kept `--work` outside TMPDIR). The 18/3 summary is reproducible; the H1a mf=1 line is not explained — verify which tree/limb it flips before trusting per-mutant counts (the caught/uncaught classification of the other 20 mutants is consistent across all runs and with the receipt).
- The fixture fallback needs the controls' fixture builders; they are committed under `.ufo/waves/round-46/attempt2/controls/` (verified tracked) and are located relative to the instrument's repo root, with the absolute lane path as fallback.

## Tooling

No tools installed or upgraded (none needed; stdlib-only deliverable).

## Scratch

`/fast/scratch/hyaku/kasegi-r46/R46bExecMutbatF29/` — receipts copied into the draft dir, then removed before yield.
