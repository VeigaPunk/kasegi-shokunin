# ReviewEquiv — independent review of M79-1 (read-only)

Seat: ReviewEquiv (leaf, read-only). Scratch used and deleted: `/fast/scratch/hyaku/kasegi-r79/ReviewEquiv/`.
Tools installed: none. Lane tree, corpus and instruments not written.

Inputs (sha256 verified against the frozen candidate):
- r78 candidate `round-78/w1/successor/recheck-cwd-census.py` (sha f6849971…), mutant `mutants/K-X2.py` (sha f28c489f…), diff `mutants/K-X2.diff` (line 365: `clean_ok is True and limb_log == [True]` → `True and limb_log == [True]`).
- r79 frozen candidate `round-79/c1/recheck-cwd-census.py` sha `eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f` (matches claims.json); scratch copy byte-identical.
- Frozen mutant table `round-79/c1/mutant-table.json` (19 rows) read for coverage.

Commands: all selftests run as `TMPDIR=<scratch dir> python3 -B <file> --selftest` (scratch paths normalised to `<S>` below).

## Half A — r78 K-X2 is equivalent under the r78 harness; no added assertion of the same fact kills it

Step 1 (reproduce):
- r78 candidate: `selftest cases=13 failures=0`, rc 0.
- K-X2 mutant: `selftest cases=13 failures=0`, rc 0.
- Normalised diff of the two outputs: only the scratch TMPDIR name lines differ (`tmpdir-parent` dirs and `tmpdir-refusal` path, which embed the per-run TMPDIR). All 13 case lines, including `gate-consume ok clean_ok=True limb_log=[True]`, are identical.
- Reproduced claim: neutering the assertion to True leaves selftest output unchanged. Holds.

Step 2 (falsify "no added assertion of the same fact can kill it"):
Scratch copies of the r78 candidate; added check registered in `REQUIRED_CHECKS` so the exact-set `gate-checkids` does not fail for an honest reason.
- A. `check("gate-consume-log", limb_log == [True], ...)` added, unmutated: rc 0, `selftest cases=14 failures=0`.
- A + K-X2 transform applied: rc 0, `selftest cases=14 failures=0`. Output diff vs unmutated A: empty. Mutant survives; the added log assertion does not kill it.
- B. `check("gate-consume-clean", clean_ok is True, ...)` added (plus log check), unmutated: rc 0, `cases=15 failures=0`.
- B + K-X2 transform: rc 0, `cases=15 failures=0`. Output diff vs unmutated B: empty. Survives.
- Mechanism: K-X2 changes only a conjunct whose value is True on every input the harness feeds it (`limb(out6, ret6)` is always True), so no output-level assertion can distinguish mutant from original. This is equivalence relative to the harness inputs.
- [INFERENCE, not run] Without registering the added name, `gate-checkids` (exact `frozenset` equality) would fail on the unmutated tree. That is a harness-maintenance cost, not a kill.

Verdict Half A: **HOLDS** (for K-X2, for both added-assertion forms tested, and by mechanism for any output-level assertion of the same fact).

## Half B — "the class is killed only by a structural limb (gate-wiring) or by a predicate tested in both polarities": **BREAKS**

Judgement of the r79 kill of K-X2b (assertion call neutered to True):
- Transform T3: `check("gate-consume", gate_consume_ok(clean_ok, limb_log),` → `check("gate-consume", True,`.
- Output: `selftest case=gate-wiring FAIL findings=['F1:gate-consume:486', 'F2:gate-consume:486', 'F3:gate-consume']`; `gate-checkids FAIL side_logs=[[True],[False],[True]]`; `selftest cases=15 failures=2`; rc 1.
- Assessment: genuine structural observable. The scanner reads the call site against an independent `GATE_PREDICATES` table; its verdict does not come from the mutant's runtime behaviour, so it is not a tautology. Its limit: `_calls` matches only the callee name (and `consumed(log, pred(...))`), never the arguments.

Single transforms of the r79 candidate that survive with byte-identical output (run, rc 0, `selftest cases=15 failures=0`, output identical to the frozen run except scratch paths; `gate-wiring ok findings=[]`):
- **T1 (argument neutered):** line 486 `gate_consume_ok(clean_ok, limb_log)` → `gate_consume_ok(True, limb_log)`.
  - Passes gate-wiring: `_calls` accepts any arguments.
  - Passes gate-predicates: its rows test `gate_consume_ok` directly, not the call-site argument.
  - Passes gate-consume: `clean_ok` is True on the fixture.
  - It neuters the same fact K-X2 neutered (the clean-run assertion to True), in a place no frozen row covers (the table's K-X1 and K-X2b kill by other means).
- **T2 (RESULT limb conjunct neutered):** line 368 `ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out` → `True and "RECHECK-CWD-RESULT nonconformant" in out`.
  - The `ret` conjunct is redundant on harness inputs: a conformant output never contains "nonconformant".
  - No frozen row covers it. K-M2 neuters the whole closure to `True` (killed by gate-negpolarity); the conjunct-level neutering survives.

Consequence: the claimed "killed only by" limb set is not closed. Per `claims.json` kill_rule, T1 and T2 are routed findings, not verdict changes for the frozen 19-row table (P3 is not affected by this review).

Verdict Half B: **BREAKS** (T1 and T2 survive the r79 harness with byte-identical output and are neutering-to-True or conjunct-neutering transforms outside the frozen table).

## Routed findings (for the r80 successor; not applied)
1. Gate-wiring should bind the predicate's first argument to the value produced by the limb call (structural), not only to the callee name — closes T1.
2. The RESULT limb needs a negative input for the `ret` conjunct (a case where text matches but ret != 1) or the `ret` test must be removed as dead — closes T2.
3. The QUALITY criterion as stated ("killed only by structural limb or predicate-in-both-polarities") should name argument-level binding explicitly, or it will be falsified by T1 again.

## Verification gaps
- Frozen counter `mutbat.py` (19 rows) and predicates P1–P7 were not run (outside this seat's scope).
- M79-1 mined-mistake text was not read; the review tests the claim exactly as stated in the assignment.
- The T1/T2 probes were single selftest runs; no mutbat run on them.
