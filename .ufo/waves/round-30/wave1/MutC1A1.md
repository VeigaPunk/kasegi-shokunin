# MutC1A1 — mutant-A1 probe on frontier-recheck-count.py (round 30, wave 1)

Seat: MutC1A1 (mutation tester, L2 under KasegiR30). Claim under test: **C1** (depth:verifiability), fixture **A1**. Mutant per claims `mutants` field: *mutant-A1 (drop named-row error) must make A1 exit without the named-row marker*.

## Bytes measured (sha256)

| artifact | sha256 |
|---|---|
| base instrument (freeze copy, = claims base c8a62888…) | `c8a62888354ba60dae85d4510653312413e293c0114177627e2e6770a0b88261` |
| landed (post-update) instrument `corpus/instruments/frontier-recheck-count.py` at probe time | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |
| mutant `.ufo/waves/round-30/c1-controls/mutants/mutant-a1-frontier-recheck-count.py` | `013dd1e537a439e1cb19f2cf9b44141c84190d799f8e3d016cd6eec5f0cfd5b5` |

Instrument-update poll: `.ufo/waves/round-30/c1-controls/mutants/digest-poll.log` line `18:50:40 aa60b581… 0b841d5d…` — the frontier digest at that line equals the working-tree bytes I mutated from (`aa60b581…`), so the update was landed before the probe. [Note] `source-recheck.py` moved again after that poll line (working tree `33602a9d…` at my run time — concurrent sibling work on the B limbs). Irrelevant here: the A1 fixture never reaches a recheck-line execution, and the frontier harness was the only binary under test.

## Mutation (exactly one limb removed)

Copied the landed instrument to `mutants/mutant-a1-frontier-recheck-count.py`, then removed the A1 named-row limb — the missing-entry fail-closed guard in `entry_contract` (docstring item E):

```diff
     full = os.path.join(root, entry_path)
     if not os.path.isfile(full):
         # README rows name entries relative to corpus/ (`knowledge/...`).
         full = os.path.join(root, "corpus", entry_path)
-    if not os.path.isfile(full):
-        return None
     declared, cited, recheck, manifest = [], set(), "", None
```

`diff` of landed vs mutant is exactly those two deleted lines; nothing else changed. With the guard gone, `open(full, encoding="utf-8")` is uncaught for a missing entry — the same shape as the base freeze copy (line 65), restoring M29-4's uncaught `FileNotFoundError`.

## Detector runs (all runs read-only: no `--json`, fixtures untouched)

**Fixed instrument on A1 fixture** (`python3 corpus/instruments/frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1`, cwd = lane repo) — exit **1**, stdout, stderr empty:

```
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
```

Named-row marker present (`F98` + `problems=missing-entry`), no traceback — the limb works on the landed bytes.

**Mutant on A1 fixture** (`python3 .ufo/waves/round-30/c1-controls/mutants/mutant-a1-frontier-recheck-count.py --root .ufo/waves/round-30/c1-controls/harness-root-a1`) — exit **1**, stdout **empty (0 bytes)**, stderr:

```
Traceback (most recent call last):
  File ".../c1-controls/mutants/mutant-a1-frontier-recheck-count.py", line 226, in <module>
    sys.exit(main())
  File ".../c1-controls/mutants/mutant-a1-frontier-recheck-count.py", line 191, in main
    record = evaluate(root, entry)
  File ".../c1-controls/mutants/mutant-a1-frontier-recheck-count.py", line 116, in evaluate
    contract = entry_contract(root, entry_path)
  File ".../c1-controls/mutants/mutant-a1-frontier-recheck-count.py", line 79, in entry_contract
    with open(full, encoding="utf-8") as fh:
FileNotFoundError: [Errno 2] No such file or directory: '.../c1-controls/harness-root-a1/corpus/knowledge/zz-missing.md'
```

`F98` occurrences in mutant stdout+stderr: **0**. `missing-entry` occurrences: **0**. Behavior FLIPPED exactly as the claims `mutants` field requires (exit 1 traceback, no named-row marker).

## Isolation check (mutation touches only the A1 limb)

Mutant vs fixed instrument on the A2 duplicate fixture (`harness-root-a2`): stdout and stderr **byte-identical** (both print `PASS F98` / `PASS F97` / `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md` / `entries=2 pass=2 exit=1`, exit 1). The duplicate-entry limb and all other limbs are unaffected.

## Verdict

**KILLED.** The landed named-row limb is load-bearing for predicate A1: removing it reverts A1 to the M29-4 failure mode (uncaught `FileNotFoundError`, row id never printed), which the C1 kill rule marks as a failure.

## Restoration / scope evidence

- The landed instrument was never edited in place; sha256 before probe = after probe = `aa60b581…` (matches the 18:50:40 poll digest). Nothing to restore.
- The mutant is retained as the deliverable artifact at `.ufo/waves/round-30/c1-controls/mutants/mutant-a1-frontier-recheck-count.py` (tasking-designated directory).
- Fixtures (`harness-root-a1`, `harness-root-a2`) and all other lane bytes untouched; the only files I created are the mutant copy and this report (`.ufo/waves/round-30/wave1/MutC1A1.md`). No git/jj/state/MANIFEST writes; no live-target contact; no tool installs performed.
