# MutC1B1 — mutant-b1 probe (source-recheck.py B1 stem check removed)

Seat: MutC1B1 (L2 mutation tester, kasegi round-30 wave 1, hyaku run 7).
Claim under test: C1 predicate limb (B1) — "a source-recheck manifest record whose id != capture file stem exits 1 (reason=stem-mismatch)".
Probe time: 2026-10-25T18:52:22Z–18:55:13Z (UTC). Working tree only; no git/jj, `.ufo/state`, MANIFEST, or sibling writes; no live-target contact; no tool installs.

## Bytes measured (sha256)

| state | file | sha256 |
|---|---|---|
| pristine / landed (update live at probe time; ≠ frozen base `9fe6a4a0…` per `c1-controls/before.txt`) | `corpus/instruments/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` |
| mutant (landed bytes minus B1 limb) | `.ufo/waves/round-30/wave1/mutant-b1/mutant-b1-source-recheck.py` | `680766883932f89d793b9eae8324181e4d6cfea84b934375fb5e37bf12c3617e` |
| restored scratch copy | `.ufo/waves/round-30/wave1/mutant-b1/source-recheck.py` | `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` (== landed) |
| diff (pristine → mutant) | `.ufo/waves/round-30/wave1/mutant-b1/mutant-b1.diff` | `8c258305c2da9add17152d7f0715d3ec06b7f81836cbf8014947961ee8bbe0b3` |
| fixture manifest | `.ufo/waves/round-30/c1-controls/q9/manifest-b1.json` | `d2e09c89b06159997d54e31c1b290479241cdb31aac1acc6ff54cba8b8ee7d63` |
| fixture capture (id S043 → path `S045.txt`, stem mismatch) | `.ufo/waves/round-30/c1-controls/q9/S045.txt` | `f583a3965348a90c4b306a4a5c83fde48c1a81366874f409b62717645ebb0f86` (matches manifest pin) |

Method: byte-exact `cp` of the landed instrument into an isolated scratch dir, then a single `edit` removing exactly the B1 limb (4 lines: comment, `if Path(path).stem != source_id:`, `emit(...reason=stem-mismatch)`, `return 1`). Diff confirms the mutation touches nothing else. Detector = `python3 <instrument> --manifest .ufo/waves/round-30/c1-controls/q9/manifest-b1.json --source S043; echo exit=$?`, run identically on pristine, mutated, and restored bytes (QUALITY R13: measurement on landed bytes; R11: counter discrimination).

## Mutant definition (unified diff)

```diff
--- corpus/instruments/source-recheck.py
+++ .ufo/waves/round-30/wave1/mutant-b1/source-recheck.py
@@ -120,11 +120,6 @@
     if not isinstance(path, str) or not path or Path(path).is_absolute():
         emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-path")
         return 2
-    # B1: the capture file stem must equal the record id (QUALITY Q9).
-    if Path(path).stem != source_id:
-        emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch")
-        return 1
-
     expected = record.get("sha256")
     if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
         emit(out, f"{source_id}:manifest", "UNAVAILABLE", "reason=invalid-sha256")
```

## Detector runs (actual outputs)

1. Pristine (landed `33602a9d…`), 2026-10-25T18:52:22Z:
   ```
   S043:manifest MISMATCH reason=stem-mismatch
   b1_exit_pristine=1
   ```
2. Mutant (`68076688…`), 2026-10-25T18:54:36Z — **the flip**:
   ```
   S043:sha256 OK
   S043:Q1 OK normalized=markup-whitespace occurrences=1
   b1_exit_mutant=0
   ```
3. Restored scratch (re-copied from landed; `33602a9d…`), 2026-10-25T18:54:46Z:
   ```
   S043:manifest MISMATCH reason=stem-mismatch
   b1_exit_restored=1
   ```

## Verdict

**KILLED.** Baseline (pristine) detector passed, so the measurement is conclusive: removing exactly the B1 stem-check limb flips the B1 fixture from exit 1 (`reason=stem-mismatch`) to exit 0, reproducing the frozen do-nothing-control output shape recorded in `c1-controls/before.txt` (`S043:sha256 OK` / `S043:Q1 OK normalized=markup-whitespace occurrences=1` / `b1_exit=0`). The new limb in the landed instrument is load-bearing for the C1 B1 predicate; this is a coverage confirmation, not a contract change.

## Restoration evidence

- Live instrument `corpus/instruments/source-recheck.py` was never opened for writing; sha256 `33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f` before (18:52:22Z), mid-probe, and after (18:55:13Z).
- Scratch copy `.ufo/waves/round-30/wave1/mutant-b1/source-recheck.py` restored to pristine bytes (sha256 equal to landed); detector re-run on restored bytes matches pristine (exit 1, same message).
- Mutant preserved for audit at `.ufo/waves/round-30/wave1/mutant-b1/mutant-b1-source-recheck.py` with its diff at `mutant-b1.diff`.

Scope note: bounded probe — one fixture (B1), one limb, three detector runs. The mutant was not run against other fixtures (B2/A1/A2/real manifests), and no other behavior was exercised or claimed.
