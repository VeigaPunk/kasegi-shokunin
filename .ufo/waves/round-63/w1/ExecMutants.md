# ExecMutants — r63 prefreeze upstream-guard mutant battery

Seat: ExecMutants (kasegi round-63 w1). Axes: depth:verifiability — falsification breadth
for the new upstream guard before any data lands (R17 exact-once, R50 per-limb breadth,
R53 mutant attack class for the guard limb). Round 63 only; base `fdccc6da`.

## Deliverable

`W/ExecMutants/pipeline-mutbat-r63.py` — sha256
`68b0e71f75f51e352917b5678493835e95d5c3c6ad7934b9f35d41fce317e7c8` (byte-identical copy
validated in seat scratch; scratch deleted after receipts were saved here).

CLI: `python3 pipeline-mutbat-r63.py --instrument /abs/figure-audit.py --work /abs/owned/scratch`.
Exit map (fail-closed, R82): 0 = battery passed; 1 = battery failed (survivor, killed
control, misclassified invalid, pristine failure); 2 = unusable input (missing/unreadable
instrument, unusable `--work`, anchor site count != 1). python3 stdlib only; the selftest
subprocess interpreter is `sys.executable` (host-conditional case-count caveat handled);
writes only under `--work` (per-run dir, removed on exit); sets `HYAKU_SCRATCH` to that
dir so the instrument's selftest fixtures also stay in owned scratch. It is not a sandbox.
The prior `corpus/instruments/figure-audit-mutbat.py` was not touched; this battery is a
separate new file. No production file edits; no git/jj mutation; no tool installs (stdlib
only; pacman pause respected).

## Anchors (exact-once, coordinated with ExecPipeline by direct peer message)

| anchor (substring, indentation-free) | candidate line | sites |
|---|---|---|
| `if p.returncode > 1:` | 107 | 1 |
| `return None, out, "derive-upstream-exit-%d" % p.returncode` | 109 | 1 |

Both must count exactly once or the battery exits 2 before running any mutant.

## Mutants and controls (counts)

7 mutants, both guard limbs at >=3 (R50): threshold limb 3 — `m-threshold-0` (`> 0`,
breaks exit1 retention), `m-threshold-2` (`> 2`, misses grep invalid-regex exit2),
`m-threshold-ge0` (`>= 0`, flags success); refusal/propagation limb 4 — `m-refusal-dead`
(return becomes dead assignment), `m-refusal-skip` (`continue`), `m-refusal-rc-launder`
(`p.returncode = 0`), `m-reason-value-constant` (`% p.returncode` -> `% 1`, marker kept,
killed only because the candidate selftest binds reason strings). Every mutant keeps the
`derive-upstream-exit` prose marker (mechanically asserted), compiles, and must die with
a named `verdict=fail` case — a crash/timeout/missing summary classifies INVALID and is
never counted killed. Controls: `c-equiv-reversed` and `c-equiv-trailing-space` must pass
the selftest; `c-invalid-missing-colon` must fail to compile and never be counted killed.

## Evidence (unedited one-invocation receipts under W/ExecMutants/)

- `base-anchors-receipt.txt` — battery-utc=2026-11-04T16:01:20Z, instrument sha
  `a0ddbd40…395f080` (r62 frozen figure-audit bytes), both anchors `sites=0
  exact-once=fail`, `MUTBAT … verdict=FAIL reason=anchor-sites`, `battery-exit=2`
  (host shell observed exit 2). The unguarded base fails closed, never green.
- `candidate-battery-receipt.txt` — instrument sha
  `e557d2f0ceea9866b40b7b99dd53864a00330ae7481f32e7eeefca2fbf2431e8` (ExecPipeline's
  tested candidate, retained as `W/ExecPipeline/figure-audit-tested.py`), anchors
  `sites=1 exact-once=ok` x2, `PRISTINE selftest_exit=0 cases=43 failures=0`,
  controls held/held/invalid-held, all 7 mutants `killed=1` with named failed cases
  (`upstream-cat-missing-exit1-retained`, `upstream-grep-invalid-stale`,
  `quoted-separator-admitted`), `MUTBAT mutants=7 killed=7 survivors=0 invalid=1
  controls=3 verdict=PASS`, `battery-exit=0` (host shell observed exit 0).
- `candidate-battery-receipt-final.txt` — same verdict over the FINAL candidate bytes
  sha `15bcb6c4fbaaa23c2b85e480dff9b9af52e43442de64661f222d8868dd73b997`
  (`W/ExecPipeline/figure-audit.py`, battery-utc=2026-11-04T16:04:53Z, shell exit 0).
  `diff` of tested vs final shows exactly one changed line (module docstring line 38,
  the fail-closed rule sentence); both guard anchors are byte-identical, and the battery
  re-run on the final bytes repeats anchors sites=1 x2, PRISTINE 43/0, 7/7 killed,
  equivalents held, invalid never killed.
- Per-cat-missing retention (L1's correction): `m-threshold-0` is killed first by
  `upstream-cat-missing-exit1-retained` — the exit1-counting contract is enforced, not
  assumed; the three error probes (grep2/git128/python7) are the stale kills via
  reason-bound cases.

## Limits (disclosed, not generalized)

1. Byte-coupled: valid for candidate bytes whose two guard lines match the anchors; the
   one post-coordination change (docstring-only, e557d2f0… -> 15bcb6c4…) left both
   anchors byte-identical and was re-validated (receipt above); any future guard-line
   change re-opens pinning (battery exits 2, cannot false-green).
2. Kill power is bounded by the candidate selftest's 43 cases: behaviors no case binds
   (e.g. a first-stage failure in a 3+-stage pipeline, or a negative-signal upstream
   status) would not discriminate fire-scope or sign-limb mutants; such mutants were
   deliberately not shipped rather than disclosed as survivors. Negative-signal and 3+
   stage semantics stay unmutated and unclaimed.
3. One invocation per mutant; the battery executes the selected instrument's selftest and
   inherits that instrument's own boundaries.

## Self-evaluation (agent-self-evaluation)

Accuracy 5 — every figure above is copied from the two receipts or the sha256 output;
candidate/base shas independently verified. Completeness 4 — all target asks delivered
(anchors, count, controls, invalid-never-killed, separate evidence, limits); not covered:
no tree-level false-green probes (that is MutationCollector's assigned attack class, and
R53 asks both classes only of the freeze package, not of this one file). Clarity 5 —
tables + receipt quotes. Actionability 4 — L1 can preflight with one command; anchors
re-pin is manual if bytes move. Conciseness 4 — receipts kept raw and separate instead of
inlined. Overall 4.4. Highest-impact improvement: anchor re-pin automation if the
candidate changes post-coordination.

Report: .ufo/waves/round-63/w1/ExecMutants.md
