# MutationCollector — round-64 w1 findings

Seat: MutationCollector (mutation-tester, leaf). Axis: depth:verifiability.
Scope: attack the collector instrument construction only. No production, fleet, sibling, or domain source was edited. No candidate was scored: the figure-audit candidate from ExecPipeline was never run through the collector. Positive controls and mutants are my own instrument construction.

## Target under attack

- Collector: `.ufo/waves/round-64/w1/ExecCollector/c1-probes-r64.py`, sha256 `fe9ba177cfdf3722a2946b5f29dc815c6df8db572221cc3489efd5044e2f196b`, read at run time.
- Contract (from its docstring, read before attacking): `--instrument ABS --work ABS --mode base|candidate`; one 18-figure ledger per invocation; exact comparison of stdout, exit, and empty stderr; exit 0 exact, 1 mismatch, 2 collection error; `--selfcheck` replays fault cases.
- Rule in the collector: per `&&` group, a nonzero native final stage wins (`derive-exit-N`, including negative `-15`); then upstream statuses (base: `>1`; candidate: positive except grep exit 1). Upstream negative statuses are ignored.

## Attack suite

- Source: `.ufo/waves/round-64/w1/MutationCollector/attack-r64-v2.py`, sha256 `a486c4bc3cd2fd128dfc4163524c6027156a95404dc0d8b59fce8d8a5e707f76`.
- Each attack is a CLI-shaped producer (`--ledger --root`) run through the collector's public CLI. Expected verdicts are fixed before running.
- The suite's 18-probe table is an independent copy. The drift check reports `PROBE-TABLE-DRIFT collector_probes=18 equal_to_suite_copy=True`.
- Receipt: `.ufo/waves/round-64/w1/MutationCollector/attack-suite-receipt.txt` (one invocation, run UTC `2026-11-04T18:45:36Z` printed). Result: `SUITE collector=exec-collector-r64 attacks=30 unexpected=2 positive_ok=True`. The suite exits 1 because of the two survivors below.
- Selfcheck receipt: `.ufo/waves/round-64/w1/MutationCollector/selfcheck-receipt.txt` (one invocation, base oracle as pristine control). Result: `HARNESS selfcheck cases=9 failures=0`, exit 0.

### Results

| Group | Attacks | Expected | Observed |
|---|---|---|---|
| Positive controls | A1 base oracle + base mode; A2 candidate oracle + candidate mode | 0 | 0, 0 (`positive_ok=True`) |
| Setup / fail-closed | B1 missing instrument; B2 relative instrument; B3 instrument is a directory; B4 instrument under work; B5 relative work; B6 work outside owned scratch; B7 `wc` absent from PATH; B8 instrument mutates itself; B9 instrument hangs | 2 | 2 ×9, each with the named `HARNESS-ERROR` |
| Fake producers | C1 always-green counterfeit; C2 always stale; C3 correct output + exit 3; C4 stale output + exit 0; C5 empty output + exit 0; C6 one FIG line, no trailer; C7 correct stdout + stderr noise; C8 syntax error; C9 base rule run as candidate; C10 candidate rule run as base; C12 correct records + second conflicting trailer | 1 | 1 ×11 |
| Mutants of the rule | D1 threshold `>1` in candidate; D2 grep exit 1 not exempted; D4 upstream checked before final; D5 negative upstream rejected; D6 negative final ignored; D7 `&&` failure ignored | 1 | 1 ×6 |
| Survivors | C11 honest replay; D3 grep-substring exemption | 1 | 0, 0 (both reported `SURVIVED`) |

All 28 non-survivor attacks matched their expected verdicts. Positive controls are green, so the 1-results are not vacuous.

## Findings

### F1 — honest replay of fixed output passes (survivor, C11)

- Observed: a fabricator that prints the stdout of a truthful candidate-mode run on the same fixed ledger, and exits 1, gets exit 0 from the collector in candidate mode (`ATTACK C11 ... actual=0 verdict=SURVIVED`).
- Cause: the collector's fixtures are constant (`one.txt` body `kasegi-r64\n`, `fail7.py`, `sigterm.py`). Its grading compares stdout and exit to values it computes per run. Nothing in the producer's output depends on a per-run input that the collector chose, so a replay of truthful output is indistinguishable from a fresh run.
- Demand for a finite fix (not applied; collector is ExecCollector's file): vary one input per run with a random token or random line count, and derive the expected derived values from it, so output captured on a previous run cannot match.
- Scope of the claim: this is about the collector's fail-closed boundary against fabricated output, not a sandbox claim.

### F2 — grep-substring exemption survives the eighteen probes (survivor, D3)

- Observed: a mutant that exempts any upstream exit 1 when the word `grep` appears anywhere in the derive string survives all 18 probes (`ATTACK D3 ... actual=0 verdict=SURVIVED`).
- Cause: no probe has a non-grep upstream exit 1 whose derive string contains `grep`. The grep-exemption check is exercised only by `grep zzz-absent one.txt`, which is a true grep.
- Validated fix (scratch copy only, not applied to the collector): add one probe `('grep-named-upstream', '0', (((('cat', 'grep-missing.txt'), ('wc', '-l')),)),)`. On that copy the D3 mutant is `KILLED` (exit 1, `HARNESS probes=19 failures=2`), and the honest candidate oracle still passes (exit 0). I validated candidate mode only; base-mode expectation for this probe (want 0 green) was not run.

### Coverage that holds (killed, with reason)

- D4 (upstream before final): killed by `final-precedes-upstream`.
- D5 (negative upstream rejected) and D6 (negative final ignored): killed by `upstream-negative-signal` and `final-negative-signal`. The collector distinguishes negative handling in both directions.
- D7 (`&&` failure ignored): killed by `and-stops-on-failure` (14 failures in the mutant run).
- C12 (second conflicting trailer): killed by the exact-shape check.
- B8 (self-mutating instrument) and B9 (hang past the 60s collector timeout): both exit 2 with named errors.
- B7 (missing `wc`): exit 2 with `missing-dependencies:wc`.

## Notes and limits

- My first reference collector assumed one figure per invocation. ExecCollector uses one 18-figure ledger, so that reference and its run were discarded and are not evidence. The suite was rebuilt against the 18-figure contract.
- The honest oracle, mutants, and fakes are instrument construction. The oracle implements the docstring rule with a `Popen` staged runner; it is not a candidate and was not compared to ExecPipeline's code.
- Not covered: locale and encoding variants of stdout, concurrent instrument runs, and signals other than SIGTERM.
- Not applied: no change to ExecCollector, ExecPipeline, or any production file. The F1/F2 demands are for L1 to decide.
- Tools: none installed. Interpreter used: `/usr/bin/python3` (system). No pacman, uv, npm, or cargo activity.
- Scratch `/fast/scratch/hyaku/kasegi-r64/MutationCollector` was removed after copying receipts and suite into the output directory.

Report: .ufo/waves/round-64/w1/MutationCollector.md
