# MutSRExisting — selftest mutation probe of `source-recheck.py` (round 31, wave 1)

Seat: mutation-test the EXISTING `--selftest` of `corpus/instruments/source-recheck.py` in scratch copies; lane bytes read-only. Detector = `python3 <copy> --selftest`; baseline must pass for a kill verdict to count (it did: exit 0, `selftest cases=9 failures=0`). No tooling installed; no git/jj mutation; no writes outside this receipt and delete-on-exit `tempfile` scratch dirs under `/tmp` (same scratch convention as the C1 counter contract).

## Subject bytes

- Lane file: `corpus/instruments/source-recheck.py`, 403 lines, 16711 bytes.
- sha256 before: `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f`
- sha256 after all runs: `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` (identical — restoration evidence; every mutant was applied to a scratch copy only).
- Same digest as the round-30 settled instrument (`corpus/lessons/round-30.md`, C1 row), so these are the landed bytes.

Method (per mutant): verify `find` occurs exactly once in the pristine text (all six probes: count=1), apply replace, `py_compile` (all six compile), run `--selftest` in a fresh `tempfile.TemporaryDirectory`, compare per-case `SELFTEST` lines against baseline. A case "flips" when its PASS becomes FAIL. Selftest exit 0 with all cases PASS = survivor.

## Baseline (pristine scratch copy)

```
exit=0 stderr=''
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 expected-ids=S901:manifest observed-ids=S901:manifest
SELFTEST double-occurrence PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-anchored PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-out-of-range PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
selftest cases=9 failures=0
```

## Verdict table

| Mutant | Behavior change | selftest exit | Flipped case line(s) | Verdict |
|---|---|---|---|---|
| M1 drop stem==id check | B1 gate deleted | 1 | `stem-mismatch` | killed |
| M2 drop occurrence/anchor gate | B2 `if occurrences > 1 …` block deleted | 1 | `double-occurrence`, `double-occurrence-out-of-range`, `double-occurrence-broken` | killed |
| M3 drop sha256 pin | `if actual != expected:` → `if False:` | 1 | `corrupt` | killed |
| M4 accept out-of-range anchor | upper bound `or anchor > len(raw_lines)` deleted | 1 | `double-occurrence-out-of-range` | killed |
| M5 accept normalized-quote mismatch | final `else` emits OK, no `status = 1` | **0** | none (failures=0) | **SURVIVOR** |
| M1+M2 combined (independence control) | both gates deleted | 1 | `stem-mismatch` + the three `double-occurrence` non-anchored cases | killed |

## M1 — drop the stem==id check (B1)

Diff (pristine → mutant, lines 123–127 context):

```diff
     # B1: the capture file stem must equal the record id (QUALITY Q9).
-    if Path(path).stem != source_id:
-        emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch")
-        return 1
```

Output: `selftest cases=9 failures=1` with

```
SELFTEST stem-mismatch FAIL expected-exit=1 observed-exit=0 expected-ids=S901:manifest observed-ids=S901:sha256,S901:Q1
```

Single killer: `stem-mismatch`. Killed.

## M2 — drop the occurrence-uniqueness/anchor check (B2)

Diff:

```diff
         # missing, out-of-range, or broken anchor is a failure (QUALITY Q9).
-        if occurrences > 1 and anchor_verdict_result != "ok":
-            anchor_reasons = {
-                "missing": "reason=occurrence-not-unique",
-                "out-of-range": "reason=anchor-out-of-range",
-                "broken": "reason=anchor-broken",
-            }
-            emit(out, f"{source_id}:{quote_id}", "MISMATCH", anchor_reasons[anchor_verdict_result])
-            status = 1
-            continue
         if assertion["quote"] in source_text:
```

Output: `selftest cases=9 failures=3` with

```
SELFTEST double-occurrence FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-out-of-range FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-broken FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
```

Killers: three cases. `double-occurrence-anchored` (anchor=6) does NOT flip — correct, since the mutant only removes the failure path and the anchored case still expects exit 0. Killed.

## M3 — drop the sha256 pin check

Diff:

```diff
     actual = hashlib.sha256(source_bytes).hexdigest()
-    if actual != expected:
+    if False:
         emit(out, f"{source_id}:sha256", "MISMATCH", f"expected={expected} actual={actual}")
```

Output: `selftest cases=9 failures=1` with

```
SELFTEST corrupt FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256 observed-ids=S900:sha256,S900:Q1
```

Single killer: `corrupt`. Killed.

## M4 — accept an out-of-range anchor

Diff:

```diff
-    if type(anchor) is not int or anchor < 1 or anchor > len(raw_lines):
+    if type(anchor) is not int or anchor < 1:
         return " anchor=OUT-OF-RANGE", "out-of-range"
```

Output: `selftest cases=9 failures=1` with

```
SELFTEST double-occurrence-out-of-range FAIL expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
```

Kill mechanism: exit and id list stay equal; the case fails only on `expected_substr` — anchor=99 now yields an empty anchor window, so the gate emits `reason=anchor-broken` instead of `reason=anchor-out-of-range`. The `expected_substr` assertions in `run_case` are load-bearing kill evidence. Killed.

## M5 — accept a normalized-quote mismatch — **SURVIVOR**

Diff (the mismatch verdict for a quote absent even after normalization):

```diff
         else:
-            emit(out, f"{source_id}:{quote_id}", "MISMATCH", "reason=quote-not-found")
-            status = 1
+            emit(out, f"{source_id}:{quote_id}", "OK", "reason=quote-not-found-accepted")
     return status
```

Output: `selftest cases=9 failures=0`, exit 0. Zero case lines flip.

Equivalence ruled out by probe (scratch manifest, id S902, capture present and hash-matched, quote `an entirely absent sentinel phrase here` absent from it):

```
pristine   exit=1 stdout=['S902:sha256 OK', 'S902:Q1 MISMATCH reason=quote-not-found'] stderr=''
M5-mutant  exit=0 stdout=['S902:sha256 OK', 'S902:Q1 OK reason=quote-not-found-accepted'] stderr=''
```

Coverage finding: none of the 9 selftest cases exercises the `reason=quote-not-found` path — every fixture quote occurs in its capture. Per the seat protocol this is reported to ExecSRLimbs (messaged); strengthening the fixture set (e.g., a quote-absent case, which would also pin the `MIN_QUOTE_CHARS` gate's neighbors) is the owner's call, not a contract change from this seat.

## Independence of the 9 cases against M1 and M2 (M30-1 follow-up)

The frozen round-30 B2 fixture was confounded: its record (id S045, path `B2.txt`) tripped B1 first, so the B2 mutant did not flip on it (`corpus/lessons/round-30.md` M30-1). Question here: do the existing selftest cases kill M1 and M2 independently?

Per-case flip matrix (F = flips to FAIL, · = stays PASS):

| Case | M1 only | M2 only | M1+M2 |
|---|---|---|---|
| clean | · | · | · |
| corrupt | · | · | · |
| missing-source | · | · | · |
| missing-manifest | · | · | · |
| stem-mismatch | **F** | · | **F** |
| double-occurrence | · | **F** | **F** |
| double-occurrence-anchored | · | · | · |
| double-occurrence-out-of-range | · | **F** | **F** |
| double-occurrence-broken | · | **F** | **F** |

- Killer sets are disjoint: M1 killed only by `stem-mismatch`; M2 killed only by `double-occurrence`, `double-occurrence-out-of-range`, `double-occurrence-broken`.
- Each killer is stem-correct (the three `double-occurrence*` manifests use id S900 with path `S900.txt`), so B2 kills never route through B1 — the exact confound of M30-1 is absent from the selftest.
- Under M1+M2 combined, the union of four cases still fails; each single mutant's killer also kills under the combined mutant.
- Verdict: **yes, independent** — B1 and B2 each have at least one dedicated killer case, and no case kills both.

Boundary: this proves the committed `--selftest` discriminates the two limbs on the landed bytes. It says nothing about the separate round-31 C1 limb-ledger fixtures (`limb-fixtures/sr/**`, owned by ExecSRLimbs); those must stand on their own bytes.

## Post-fix re-run (survivor closed by owner)

ExecSRLimbs added a `quote-absent` selftest case (quote absent from the capture; expected exit 1, ids `S900:sha256,S900:Q1`, expected_substr `S900:Q1 MISMATCH reason=quote-not-found`, so a status-label-only flip also dies) and closed M5. Re-run of the identical 5-mutant probe + M1+M2 control on the new bytes:

- Subject digest (before and after this re-run): `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` — the §"Subject bytes" digest `33602a9d…` above refers to the pre-fix state this report's diffs and baseline were taken on; do not mix the two columns (M30-2 discipline).
- All six `find` strings still occur exactly once in the new bytes.
- Baseline: `selftest cases=10 failures=0`, exit 0; `SELFTEST quote-absent PASS expected-exit=1 observed-exit=1`.

| Mutant (post-fix bytes) | selftest exit | Flipped case line(s) | Verdict |
|---|---|---|---|
| M1 drop stem==id check | 1 | `stem-mismatch` | killed |
| M2 drop occurrence/anchor gate | 1 | `double-occurrence`, `double-occurrence-out-of-range`, `double-occurrence-broken` | killed |
| M3 drop sha256 pin | 1 | `corrupt` | killed |
| M4 accept out-of-range anchor | 1 | `double-occurrence-out-of-range` | killed |
| M5 accept normalized-quote mismatch | 1 | `quote-absent` | **killed (was survivor)** |
| M1+M2 combined | 1 | union of the four above-B2 cases | killed |

Post-fix survivor count: **0 of 5**. M5's sole killer is the new `quote-absent` case; it kills neither M1 nor M2 (quote occurs 0 times, so the B2 gate is irrelevant; the fixture is stem-correct), so the §independence matrix and its "yes, independent" verdict are unchanged on 10 cases. Owner evidence: `wave1/ExecSRLimbs-scratch/proof.txt`.

## Handoff

- Survivor messaged to ExecSRLimbs (agent write, this run): M5 finding + independence result + pointer to this receipt.
- Checks Main may want: rerun `python3 corpus/instruments/source-recheck.py --selftest` on quiescent lane bytes (expect `selftest cases=10 failures=0`, exit 0); re-verify `sha256sum corpus/instruments/source-recheck.py` = `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` (pre-fix bytes were `33602a9d…`, the state the §diffs/baseline above were measured on).
