# MutC1Hunt — beyond-table mutation hunt on the round-79 C1 candidate

Seat: `MutC1Hunt` (leaf, mutation-tester). Lane read-only: nothing under the lane tree was
modified; all candidate bytes, mutants and outputs live under
`.ufo/waves/round-79/w1/MutC1Hunt/`. The frozen C1 bytes and the frozen 19-row table were only
read.

- Target: `.ufo/waves/round-79/c1/recheck-cwd-census.py`
  sha256 `eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f` (matches the frozen
  candidate hash before and after the hunt).
- Frozen table (untouched): `.ufo/waves/round-79/c1/mutant-table.json`, 19 rows.
- Detector, identical for pristine / mutated / restored bytes:
  `TMPDIR=/fast/scratch/hyaku/kasegi-r79/MutC1Hunt python3 -B <file> --selftest`
- Scratch root: `/fast/scratch/hyaku/kasegi-r79/MutC1Hunt` (fixtures and run copies; deleted
  before yield). Python 3.14.8 (system); no tool installed or upgraded.

Verdict rule (seat spec): `KILLED` = rc != 0 with a `selftest case=… FAIL` line and no
`Traceback`; `DIRTY` = rc != 0 without a FAIL line, or with a Traceback; `SURVIVED` = rc 0.

## 1. Baseline and restoration evidence

| run | rc | tail | sha256 |
|---|---|---|---|
| pristine (before) | 0 | `selftest cases=15 failures=0` | `eda49d32…091f2f` |
| pristine (after all runs) | 0 | `selftest cases=15 failures=0` | `eda49d32…091f2f` |

Restored bytes are byte-identical (`sha256` unchanged), and the normalized selftest output is
identical (`out/_baseline.norm.diff` is empty). The only raw difference between the two pristine
runs is the random scratch suffix in the case-13 stderr detail
(`out/_baseline.raw.diff`):

```
-selftest case=tmpdir-refusal ok … stderr='recheck-cwd: TMPDIR …/recheck-cwd-selftest-uslowoxv/no-such-tmpdir is not a directory\n'
+selftest case=tmpdir-refusal ok … stderr='recheck-cwd: TMPDIR …/recheck-cwd-selftest-5zkk4yro/no-such-tmpdir is not a directory\n'
```

## 2. Mutants (30, none is a frozen row)

Membership test: the exact `(anchor, replacement)` pair intersection with the 19 frozen rows is
**0**; every anchor occurs exactly once in the target; each mutant is one literal replacement.
One mutant (`N26`) reuses `K-G1`'s anchor with a different single transform (`==` → `>=`;
`K-G1` replaces the body with `True`), so it is a distinct mutant, not a copy of a frozen row.
All 30 ran under the same `TMPDIR`.

| id | area | verdict | fails | failing cases |
|---|---|---|---|---|
| N01-gatedict-drop-checkids | GATE_PREDICATES dict entry removed | KILLED | 1 | case=gate-predicates |
| N02-gatedict-wiring-wrong | GATE_PREDICATES value points at the wrong function | KILLED | 2 | case=gate-wiring, case=gate-checkids |
| N03-f1-append-pass | wiring_findings F1 branch | KILLED | 1 | case=gate-predicates |
| N04-f2-cond-invert | wiring_findings F2 branch | KILLED | 3 | case=gate-predicates, case=gate-wiring, case=gate-checkids |
| N05-f3-extend-pass | wiring_findings F3 branch | KILLED | 1 | case=gate-predicates |
| N06-label-int | wiring_findings label filter | KILLED | 3 | case=gate-predicates, case=gate-wiring, case=gate-checkids |
| N07-walk-body | wiring_findings traversal (`walk` → module `body`) | KILLED | 3 | case=gate-predicates, case=gate-wiring, case=gate-checkids |
| N08-check-arity3 | wiring_findings `check()` arity gate `>=2` → `>=3` | SURVIVED | 0 | — |
| N09-consumed-arity | `_calls` consumed() arity `==2` → `>=2` | SURVIVED | 0 | — |
| N10-calls-recurse-true | `_calls` recursion through consumed() → `True` | SURVIVED | 0 | — |
| N11-rows-drop-empty | gate-predicates rows: delete `(predicates_ok([]), False)` | SURVIVED | 0 | — |
| N12-rows-flip | gate-predicates rows: flip `(predicates_ok([(True, False)]), False)` → True | KILLED | 1 | case=gate-predicates |
| N13-sidelog-drop-third | gate-checkids side_logs: drop the third limb | SURVIVED | 0 | — |
| N14-required-drop-wiring | REQUIRED_CHECKS: drop `gate-wiring` | KILLED | 1 | case=gate-checkids |
| N15-required-add-phantom | REQUIRED_CHECKS: add `phantom-check` | KILLED | 1 | case=gate-checkids |
| N16-main-refusal-rc0 | case-13 guard: main refusal returns 0 instead of 2 | KILLED | 1 | case=tmpdir-refusal |
| N17-case13-existing-tmpdir | case-13 guard: point the bogus TMPDIR at a real dir | KILLED | 1 | case=tmpdir-refusal |
| N18-census-exit2-to-3 | census() exit-code bucket `==2` → `==3` | KILLED | 2 | case=prefix-census, case=first-line |
| N19-census-noprefix-invert | census() noprefix test inverted | KILLED | 8 | prefix-census, result-main, first-line, restoration-only, both-headers, relabel-detection, gate-negpolarity, gate-checkids |
| N20-restoration-reader-false | has_restoration_recheck returns False | KILLED | 1 | case=restoration-only |
| N21-census-exitother-to-exit1 | census() `exit_other` +1 → `exit1_foreign` +1 | SURVIVED | 0 | — |
| N22-consumed-noappend | consumed(): drop `sink.append(value)` | KILLED | 2 | case=gate-consume, case=gate-checkids |
| N23-consumed-return-true | consumed() return limb → `True` | KILLED | 1 | case=gate-negpolarity |
| N24-check-done-pass | check(): drop `done.append(case)` | KILLED | 1 | case=gate-checkids |
| N25-gatecheckids-firstsidelog | gate_checkids_ok: `side_logs` → `side_logs[:1]` | SURVIVED | 0 | — |
| N26-gatecheckids-superset | gate_checkids_ok: `set(done) == set(required)` → `>=` | SURVIVED | 0 | — |
| N27-case7-drop-rest-flag | case-7 ok drops `and not rest7` | SURVIVED | 0 | — |
| N28-census-restoration-bucket | census(): restoration_only +1 → norecheck +1 | KILLED | 3 | restoration-only, relabel-detection, gate-checkids |
| N29-gatedict-rename-consume | GATE_PREDICATES key `gate-consume` renamed | KILLED | 3 | case=gate-predicates, case=gate-wiring, case=gate-checkids |
| N30-runforeign-cwd-inherit | run_foreign: `cwd=scratch` → `cwd=None` | SURVIVED | 0 | — |

**Tally: 30 mutants — 20 KILLED, 10 SURVIVED, 0 DIRTY, 0 NOT-DERIVED, 0 frozen-row
duplicates.** Per-mutant diffs, mutant bytes and full outputs: `mutants/` and `out/`.

## 3. Survivors — equivalence judgement

10 survivors: **3 equivalent**, **7 real gaps**. Each judgement is backed by
`survivor_probes.py` → `probes/probes.json` or by the explicit row/predicate argument below.

| id | judgement | one-line reason and evidence |
|---|---|---|
| N08-check-arity3 | **equivalent** | `check(case, ok, detail)` is a fixed 3-arg nested helper (AST arity probe: 3); a 2-arg call raises `TypeError` before any wiring scan, so the `>=2`→`>=3` gate differs only on non-runnable input. |
| N09-consumed-arity | **equivalent** | `consumed(sink, value)` is a fixed 2-arg helper (AST arity probe: 2); a 3-arg call raises `TypeError`, so `==2`→`>=2` is unreachable. |
| N10-calls-recurse-true | **real gap** | Inside `consumed(...)`, `_calls` returns True without checking the predicate name: `check("gate-consume", consumed(x, gate_negpolarity_ok(False)), "")` yields pristine `F2:gate-consume:1` + `F3:gate-consume`, mutant neither (probe `N10`, differs=true). Wrong predicate wrapped in consumed() is accepted as wired. |
| N11-rows-drop-empty | **real gap** | The rows table is unregistered, so deleting a passing polarity row is invisible. Masking probe: `predicates_ok` → `return (not rows) or all(...)` (differs only on `rows==[]`) is killed on pristine (`gate-predicates FAIL rows=17 bad=[14]`, rc1) but survives on N11 (`cases=15 failures=0`, rc0). |
| N13-sidelog-drop-third | **equivalent** | The dropped limb `predicates_ok([(True, False)]) is False` is the same proposition over the same input as `rows[13] = (predicates_ok([(True, False)]), False)`; any defect that flips it flips the row, so no defect can be masked. |
| N21-census-exitother-to-exit1 | **real gap** | No fixture produces an exit code outside {0,1,2}. Probe: a prefixed entry `cd <root> && exit 7` gives pristine `exit_other=1, exit1_foreign=0`; mutant `exit_other=0, exit1_foreign=1`. (Note P5 does not require `exit1_foreign=0`, only `exit_other=0`.) |
| N25-gatecheckids-firstsidelog | **real gap** | Rows falsify only `side_logs[0]`; probe `gate_checkids_ok(["a"],["a"],[[True],[False]])` is pristine False, mutant True (and `[[False],[True]]` stays False, so only the first log is load-bearing). |
| N26-gatecheckids-superset | **real gap** | The `done ⊃ required` direction is untested: probe `done=["a","b"], required=["a"]` is pristine False, mutant True. Masking probe: N26 + the N14 transform (REQUIRED_CHECKS loses `gate-wiring`) runs `cases=15 failures=0` rc0, while N14 alone is KILLED by gate-checkids. |
| N27-case7-drop-rest-flag | **real gap** | Case 7 no longer asserts that the both-header entry's `restoration-recheck:` never executed. Simulated regression `rest7=True`: pristine ok False, mutant ok True (probe `N27`); case 6's marker check does not cover case 7's entry. |
| N30-runforeign-cwd-inherit | **real gap** | The "fresh foreign cwd" invariant is asserted by no fixture (all fixture commands are cwd-independent or fail anywhere). Probe: unprefixed `python3 probe.py` with `probe.py` only in the caller cwd gives pristine `exit2_foreign=1, exit0_foreign=0`; mutant `exit2_foreign=0, exit0_foreign=1`. |

## 4. Composites of frozen rows (out of frozen scope; routed only)

Four composites (the three required probes plus one additional pair). Composites are reported,
never scored: they are outside the frozen 19-row scope.

| composite | rows | verdict | fails | failing cases |
|---|---|---|---|---|
| X1-K-W2+K-C1 | K-W2 + K-C1 | **SURVIVED** | 0 | — |
| X2-K-P2+K-C1 | K-P2 + K-C1 | KILLED | 1 | case=gate-wiring |
| X3-K-N1+K-P1 | K-N1 + K-P1 | KILLED | 1 | case=gate-checkids |
| X4-K-X2b+K-N1 | K-X2b + K-N1 | KILLED | 1 | case=gate-predicates |

X1 is an **escape**: both the gate-wiring check's `ok` argument and the gate-checkids check's
`ok` argument are replaced by `True`, i.e. both consumers of the wiring scanner are removed in
one mutant. The single run still *prints* the finding and the empty log but exits 0
(`out/X1-K-W2+K-C1.out`):

```
selftest case=gate-wiring ok findings=['F1:gate-checkids:500', 'F1:gate-wiring:472', 'F2:gate-checkids:500', 'F2:gate-wiring:472', 'F3:gate-checkids', 'F3:gate-wiring']
...
selftest case=gate-checkids ok missing=[] extra=[] side_logs=[[True], [], [True]]
selftest cases=15 failures=0        (rc=0)
```

X2, X3, X4 stay killed, and each kill names the backstop that caught the pair: gate-wiring's own
scan (X2), the third side log (X3), and the rows table (X4, `bad=[11]`).

## 5. Masking probes (survivor pair constructions; routed only)

| construction | result |
|---|---|
| `predicates_ok → (not rows) or all(...)` on pristine | KILLED: `gate-predicates FAIL rows=17 bad=[14]`, rc1 |
| same defect on the N11 (deleted empty-row) base | SURVIVED: `cases=15 failures=0`, rc0 |
| `REQUIRED_CHECKS` loses `gate-wiring` (N14 transform) alone | KILLED: `gate-checkids FAIL` |
| same defect on the N26 (superset) base | SURVIVED: `cases=15 failures=0`, rc0 |

## 6. r78 K-X2 equivalence receipt

Same detector, same `TMPDIR`. Files read only; hashes unchanged by the runs.

| file | sha256 | rc | tail |
|---|---|---|---|
| `round-78/w1/successor/recheck-cwd-census.py` | `f68499715f38b6e74f368c441766954a240d7f5036d68157110e5017c8457db1` | 0 | `selftest cases=13 failures=0` |
| `round-78/w1/successor/mutants/K-X2.py` | `f28c489f327efb89f492f0efb4b217eb8e083608228b36781f6ffc2f98d39907` | 0 | `selftest cases=13 failures=0` |

Normalizing the random scratch path (`recheck-cwd-selftest-[A-Za-z0-9_]+` →
`recheck-cwd-selftest-<RAND>`), the two outputs are **identical**; `r78/normalized.diff` is
empty. The only raw difference is the random suffix inside the case-13 stderr detail
(`r78/raw.diff`):

```
-selftest case=tmpdir-refusal ok … stderr='recheck-cwd: TMPDIR …/recheck-cwd-selftest-a2zuh56c/no-such-tmpdir is not a directory\n'
+selftest case=tmpdir-refusal ok … stderr='recheck-cwd: TMPDIR …/recheck-cwd-selftest-0_hmbkij/no-such-tmpdir is not a directory\n'
```

Verdict: **identical** (normalized), consistent with the r78 K-X2 survivor being behaviourally
equivalent under the r78 harness.

## 7. Notes and hypothesis corrections

- N01/N29 were expected to survive as "gate-set registration removal"; both were **KILLED** by
  gate-predicates. Reason: the expected `wiring_findings(bad_src)` finding list hard-codes
  `F3:<name>` for all five gate names, so removing or renaming a gate entry changes the
  expected-vs-actual set. Evidence over hypothesis.
- N23 (`consumed()` returns True) was expected to survive; it is **KILLED** by
  `gate-negpolarity`, because the same `consumed()` wrapper feeds the negative-polarity limb, so
  returning True makes `neg_ok=True` on the conformant case-2 outputs.
- Only the composite that removes *both* the scanner consumer and the ids consumer (X1) escapes;
  the pairs that leave one consumer intact are killed.
- Routed findings (never rule changes; frozen bytes untouched): the X1 composite escape, and the
  seven real-gap survivor classes above (N10, N11, N21, N25, N26, N27, N30). These are coverage
  findings against the frozen 19-row scope; they do not alter the C1 verdict.

## 8. Files written (all under `.ufo/waves/round-79/w1/`)

- `MutC1Hunt.md` — this report.
- `MutC1Hunt/run_hunt.py`, `MutC1Hunt/survivor_probes.py`, `MutC1Hunt/summary.json`,
  `MutC1Hunt/hunt.log`.
- `MutC1Hunt/mutants/` — 30 mutant `.py` bytes + 30 unified `.diff` files.
- `MutC1Hunt/out/` — 30 mutant outputs, 4 composite outputs, 3 masking-probe outputs, baseline
  (pristine/normalized) outputs and raw diffs.
- `MutC1Hunt/composites/` — 4 frozen-row composites (`.py` + `.diff`) and 3 masking constructions.
- `MutC1Hunt/probes/probes.json` — survivor probes (values, census counts, arity, masking).
- `MutC1Hunt/r78/` — r78 candidate and K-X2 raw/normalized outputs, `normalized.diff` (empty),
  `raw.diff` (random-suffix only).
