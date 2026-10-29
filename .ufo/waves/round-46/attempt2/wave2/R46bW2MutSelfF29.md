VERDICT: BROKEN

# R46bW2MutSelfF29 — mutation test of `corpus/instruments/r46-selftest-f29.py`

Target: landed `corpus/instruments/r46-selftest-f29.py`, sha256 `23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d`, byte-identical at HEAD `96379ae` and in the worktree (`git show HEAD:… | sha256sum` = `sha256sum` of the worktree file). The file is absent from the frozen commit `fe0f56b` (it landed in `96379ae`), so the freeze never ran it.

Test lane: `lane28` = `git archive fe0f56b corpus .ufo/waves/round-46/attempt2/controls` (README with 28 F-rows). The landed selftest cannot run on HEAD (F1), so every mutation below ran against lane28 with the HEAD counter `corpus/instruments/r46-f29-gate.py` unless noted.

## F1 — BROKEN: the landed selftest aborts on the landed lane

- Command: `python3 corpus/instruments/r46-selftest-f29.py --lane <HEAD export> --work W` (HEAD export of `96379ae`).
- Output (rc=1, no case line printed):
  `selftest: lane README carries 29 frontier rows, expected 28`
- Cause: `build_positive` (selftest lines 184-188) asserts that the README carries 28 `| F` rows and then inserts the F29 row itself. HEAD `corpus/README.md` already carries 29 rows (F29 landed in `96379ae`), and the HEAD counter's H1 also requires 29 (`if len(rows) != 29`). So the instrument is internally consistent only with the pre-F29 README.
- Same selftest, lane28 (freeze README) + freeze-era corpus: `selftest cases=30 failures=0`, rc=0 (`freezecounter.txt`). It therefore passes only on a tree that does not contain the F29 row it claims to grade.

## F2 — BROKEN (case): `clause-a-raw-once` cannot isolate its clause

- Mutant CL-H1-raw: in the counter, `if len(raw) != 1:` → `if len(raw) < 0:` (the H1 one-live-F29-row clause deleted).
- Selftest on the mutant: `selftest cases=30 failures=0`, rc=0. The case stays green-as-expected.
- Verbose reason on the mutant:
  `gate H1 pass=0 read=F-rows-visible=30 parsed=29 (duplicate, commented, indented or zero-width ghost rows)`
  Landed control reason for the same case: `gate H1 pass=0 read=F29-row-not-one-live-line`.
- Mechanism: the case's `patch_frontier(controlled_rows(...))` overrides only `mod.frontier` (the parsed rows, 29 unique). `frontier_anywhere()` is not overridden, so it still counts the duplicate F29 row (30) and the H1 `anywhere` clause fires instead. The case's stated isolation ("only H1's one-live-row clause fires") is false; the case would not notice the one-live clause being removed.
- Recipe (verified, scratch only): `fix/selftest-rawonce-fix.py` adds `rawonce_patch`, which additionally sets `mod.frontier_anywhere = lambda root: len(rows)` for that case only (grader-side, restored after). Results:
  - vs landed counter: `selftest cases=30 failures=0` (control clean).
  - vs CL-H1-raw: `FAIL clause  clause-a-raw-once      fixed=7/7 failing=[]  <- expected-red=['H1'] actual-red=[]; tree read 7/7` and `selftest cases=30 failures=1`.

## F3 — per-case mutation (29 cases + positive-cli), 60+1 runs

Mutants generated from the landed bytes by exact-string insertion before `    return cases` (anchor count asserted = 1):
- INV-<case>: `_c.red = set() if _c.red else {"H1"}` (inverts the case's red expectation).
- REM-<case>: `_c.build = lambda d: build_positive(d, lane)` (removes the case's fixture mutation).
- CLI-INV: positive-cli expectation changed to `fixed=6/7 exit=1`.

Control `CTRL-none` (unmutated): `selftest cases=30 failures=0`, rc=0.

| case | INV (expectation inverted) | REM (fixture mutation removed) |
|---|---|---|
| positive | DETECT: `FAIL ctl positive fixed=7/7 failing=[] <- expected-red=['H1'] actual-red=[]` | no-op by construction (positive tree has no mutation): `failures=0` (identity control, not a dead case; INV kills it) |
| junk | DETECT (failures=1) | DETECT: `FAIL ctl junk fixed=7/7 ... expected-red=['H5']` |
| fabricated | DETECT | DETECT |
| defect-duprow … defect-symlink (18 rows) | DETECT, FAIL-lines=1 each, target named | DETECT, FAIL-lines=1 each |
| clause-a-counts-30 / -28 | DETECT | DETECT |
| clause-a-raw-once | DETECT | DETECT (but see F2 for the clause it fails to isolate) |
| clause-b-wordfloor | DETECT | DETECT |
| clause-d-quotecount / -distinct | DETECT | DETECT |
| clause-e-located | DETECT | DETECT |
| clause-c-cells-12 | DETECT | DETECT |
| positive-cli (CLI-INV) | DETECT: `FAIL ctl positive-cli rc=0 gates=7 summary=['f29-gate fixed=7/7 exit=0']` | — |

Every inverted/removed case produced exactly one FAIL line naming that case (`summary.txt`, target-FAIL=yes for 30/30 INV, 28/28 non-identity REM). No case is dead under the expectation or fixture mutation.

## F4 — counter-side clause removal (`summary2.txt`, clean run)

Counter copies placed inside a copied `corpus/instruments/` directory (see F7).

| mutant (HEAD counter) | failing cases | predicted | verdict |
|---|---|---|---|
| CL-H1-count (`if dup:` only) | clause-a-counts-28, clause-a-counts-30 | same | MATCH |
| CL-H1-raw (`len(raw) < 0`) | none | clause-a-raw-once | MISMATCH — F2 |
| CL-H2-floor (`else 0` for word floor) | clause-b-wordfloor | same | MATCH |
| CL-H3-cells (`len(c) >= 9`) | clause-c-cells-12 (defect-row9cells not newly flagged) | same | MATCH |
| CL-H4-quotes (`oks >= 1`) | clause-d-quotecount | same | MATCH |
| CL-H4-distinct (text-distinct term dropped) | clause-d-distinct | same | MATCH |
| CL-H5-located (`len(passed) >= 1`) | clause-e-located | same | MATCH |

## F5 — limb-level forced green (`summary2.txt`, clean run)

| limb forced green | failing cases |
|---|---|
| H1 | 6: clause-a-counts-28/-30, clause-a-raw-once, defect-duprow, defect-fencedf29, defect-src0740 |
| H2 | 4: clause-b-wordfloor, defect-badnames, defect-fewspans, defect-vjunk |
| H3 | 4: clause-c-cells-12, defect-kindcase, defect-row9cells, defect-thinscope |
| H4 | 5: clause-d-distinct, clause-d-quotecount, defect-dupquote, defect-fewquotes, defect-manws |
| H5 | 6: clause-e-located, defect-fewspans, defect-longquote, defect-widespan, fabricated, junk |
| H6 | 4: defect-entrymutant, defect-nestedmd, defect-symlink, defect-thinsection |
| H7 | 4: clause-c-cells-12, defect-kindcase, defect-row9cells, defect-symlink |

No limb is masked: each has at least four cases that go red when it is forced green.

## F6 — do-nothing control reports its pass inverted (BROKEN as a signal)

- `--do-nothing-control` on the landed selftest: 29 `FAIL` lines (every red-expecting case, as designed) and `selftest cases=30 failures=0`, **rc=0** (`dn.txt`).
- The control's pass condition is encoded only in the count of FAIL lines; the summary and exit code are identical to a clean real run. A CI step that checks rc or the summary line cannot tell the do-nothing counter from a healthy one.

## F7 — disclosure: discarded first counter run

The first counter-mutant pass (`summary.txt`, CNT-force-* rows) placed the mutated counter outside the instruments directory. The counter's H4 locates `source-recheck.py` via `dirname(realpath(__file__))`, so every counter mutant read `gate H4 pass=0 read=limb-error=FileNotFoundError`, inflating H1-H3 and H5-H7 to 25 failures. Those rows are invalid and are superseded by F4/F5 (`summary2.txt`, mutants inside a copied instruments dir). H4 forced-green (5) was the same in both runs.

## Limitations

- The landed selftest does not run on HEAD (F1); all mutation runs used lane28 (freeze README), not the HEAD lane.
- F2's isolation failure and F4/F5 counter mutants were run against the HEAD counter; the freeze-era counter (`fe0f56b`, different bytes) was not mutated.
- INV/REM are harness-side mutants; the positive-case REM is an identity by construction and is reported as such.
- The selftest grades limb red-sets only, so clause isolation claims (which clause fired) are never checked by the selftest itself; F2 is the one case where that gap is observable and reproducible.
- No live page, S074 quote, or other item was checked here.
- Nothing committed, pushed, or written to git/jj/index. Scratch under `/fast/scratch/hyaku/kasegi-r46/R46bW2MutSelfF29` removed on exit. No packages installed.
