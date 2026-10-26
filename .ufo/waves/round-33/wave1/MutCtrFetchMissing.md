# MutCtrFetchMissing — counter-mutant probe of `capture-binding-check.py` rule C (round 33, wave 1)

Seat: one mutation, one fixture, one verdict. Mutation: **drop the rule-C requirement that round-32+ records carry `fetched_utc` (archival allowed for all)** — the claims.json `mutants_of_the_counter` entry `skip-fetched_utc-requirement`. Applied to a scratch copy only; lane bytes never written. Detector: the checker run against a fixture lane tree holding a round-32 record that lacks `fetched_utc`. Kill rule: the checker must exit 1 on that fixture (C1 kill rule: "either round-32 record lacks `fetched_utc`" is a failure, and the checker must name the record). Pristine baseline must meet the kill rule for the verdict to count.

Verdict summary: **KILLED** — the mutant exits 0 where the kill rule requires exit 1, so the mutant fails the kill rule; the behavioral detector catches the mutation. No survivor, no coverage finding.

## Subject bytes

- Lane file: `corpus/instruments/capture-binding-check.py`, 491 lines.
- sha256 before copy: `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79`
- sha256 after all runs: `4bc7aed36308bec5a9101e34e5d1b0951ba734ffb6f4002fe693ca4d0c1a4f79` (identical — quiescent across the whole probe window).
- Restoration evidence: the mutation was applied only to the scratch copy `/fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing/mutant.py`; the lane file was never opened for writing, so there was nothing to restore. The before/after hash equality above plus the lane-original detector run below (identical output to the pristine copy) prove the probe ran on unchanged bytes.
- State note: at probe time the file is untracked in git (`git status --porcelain -- corpus/instruments/capture-binding-check.py` → `?? corpus/instruments/capture-binding-check.py`; `git cat-file -e 6e55c8d:corpus/instruments/capture-binding-check.py` → "exists on disk, but not in '6e55c8d…'"). The verdict below is pinned to the working-tree bytes by the hash above; the L1's later commit is expected to land exactly these bytes. (The file also changed twice while this seat was reading it, 431 → 491 lines, before stabilizing at `4bc7aed3…`; all runs below are on the stabilized snapshot.)
- Read-only git used: `log`, `cat-file -e`, `status --porcelain`. No git/jj mutation anywhere.

## Fixture

Built by the pristine copy's own selftest builder `case_modern_without_fetched` (the instrument's own `round-32-record-without-fetched_utc` case), so the fixture format is by construction the one the subject's selftest asserts on:

```
$ python3 -c "import importlib.util,sys; spec=importlib.util.spec_from_file_location('cbc',sys.argv[1]); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); m.case_modern_without_fetched(sys.argv[2]); print('fixture-built', sys.argv[2])" "$S/pristine.py" "$S/fixture"
fixture-built /fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing/fixture
```

Tree: `fixture/corpus/SOURCES.md`, `fixture/corpus/source-snapshots/round-32/{manifest.json,S001.txt}`. Manifest record:

```
{
  "archival": true,
  "id": "S001",
  "path": "S001.txt",
  "quotes": [],
  "sha256": "0000…0000",
  "url": "https://example.invalid/alpha"
}
```

Registry row: `| S001 | Fixture source — https://example.invalid/alpha | docs | A | … |` (single row, URL byte-equal to the record's `url` — rule B satisfied).

Fixture design note: the record carries `archival: true` and lacks only `fetched_utc`. This isolates the round-32 clause from rule C's general clause (`fetched_utc` OR `archival`): a record lacking both would be rejected by the general clause under pristine AND mutant, making the probe vacuous (the mutant could never flip it). With `archival: true`, the general clause passes and only the round-32-specific requirement stands between the fixture and exit 0.

## Mutation

`find` occurs exactly once in the pristine text (verified by grep: 1 match, line 162). `py_compile` of the mutant: `compiled-ok`. Full diff, pristine → mutant:

```diff
162c162
<         return has_fetched, has_fetched, has_archival
---
>         return (has_fetched or has_archival), has_fetched, has_archival
```

One line, inside `provenance_ok`'s modern branch (`round_no is None or round_no >= MODERN_ROUND`): the modern branch now returns the legacy clause, so `"archival": true` satisfies rule C for every round — the round-32+ `fetched_utc` requirement is dropped. No other line touched.

## Detector runs (same fixture, same command shape)

```
$ python3 "$S/pristine.py" --root "$S/fixture"; echo "pristine_exit=$?"
MANIFEST round-32 records=1 url_bound=1 fetched=0 archival=1
AUDIT records=1 with_url=1 with_fetched_utc=0 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=provenance-missing record=S001 dir=round-32
records=1 bound=0 unbound=1
pristine_exit=1
```

```
$ python3 "$S/mutant.py" --root "$S/fixture"; echo "mutant_exit=$?"
MANIFEST round-32 records=1 url_bound=1 fetched=0 archival=1
AUDIT records=1 with_url=1 with_fetched_utc=0 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
records=1 bound=1 unbound=0
mutant_exit=0
```

```
$ python3 kasegi-shokunin/corpus/instruments/capture-binding-check.py --root "$S/fixture"; echo "lane_original_exit=$?"
MANIFEST round-32 records=1 url_bound=1 fetched=0 archival=1
AUDIT records=1 with_url=1 with_fetched_utc=0 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=provenance-missing record=S001 dir=round-32
records=1 bound=0 unbound=1
lane_original_exit=1
```

Flipped lines pristine → mutant: the `FAIL rule=provenance-missing record=S001 dir=round-32` line disappears; the summary flips `records=1 bound=0 unbound=1` → `records=1 bound=1 unbound=0`; exit 1 → 0. The `MANIFEST`/`AUDIT` count lines are identical (they count, they do not gate).

## Supplementary detector: the instrument's own `--selftest`

Independent second detector (the subject's own 11-case selftest, run with `--scratch "$S/st"`). Pristine: `selftest cases=11 failures=0`, exit 0 — all cases pass, baseline sound. Mutant: `selftest cases=11 failures=1`, exit 1, with exactly one flipped case:

```
selftest case=round-32-record-without-fetched_utc exit=0 want=1 verdict=fail
selftest problem=exit=0 want=1 case=round-32-record-without-fetched_utc
selftest problem=missing='FAIL rule=provenance-missing record=S001 dir=round-32' case=round-32-record-without-fetched_utc
selftest problem=missing='records=1 bound=0 unbound=1' case=round-32-record-without-fetched_utc
```

The other ten cases (including `pre-round-32-record-without-archival`, still exit 1, and both passing cases) are unaffected — the mutation is isolated to the round-32 provenance clause, and the selftest's dedicated killer case catches it.

## Verdict

**KILLED.** The kill rule requires exit 1 on a lane tree whose round-32 record lacks `fetched_utc`; the pristine bytes meet it (exit 1, naming `record=S001`), the mutant does not (exit 0, `bound=1 unbound=0`, no FAIL line). The mutant therefore fails the C1 kill rule — the `skip-fetched_utc-requirement` counter mutant from claims.json `mutants_of_the_counter` is caught by the behavioral detector. The mutated point (`provenance_ok`'s modern branch, the only place `MODERN_ROUND` gates behavior) is load-bearing for rule C's round-32 `fetched_utc` requirement; dropping it silently flips the verdict on exactly the artifact class C1 exists to reject. Bytes differ AND behavior differs, so this is not a quote-only/equivalent-class survivor. No coverage finding; nothing to route to the instrument owner.

## Out-of-scope observation (owner's file, not edited by this seat)

The module docstring says `--selftest` runs "against ten fixture lane trees" while `CASES` has 11 entries (selftest output above: `cases=11`). Cosmetic doc drift only — behavior and the ≥6-case contract are fine. Left to ExecCaptureBinding; no peer message sent (bound 3: no peers named in this item), no edit to a file this seat does not own.

## Bounds compliance

- Lane writes: this receipt only. No other lane path written; no fleet-root, sibling-lane, shokuknow, template, script, state, watchdog, or MANIFEST writes.
- Tooling: nothing installed (operator 2026-10-19 channel unused); `python3` 3.14.8 preexisting.
- No network fetches, no live-target contact, no credential material anywhere.
- Scratch: `/fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing/` (HYAKU_SCRATCH unset → default); removed before yield, evidence appended below.

## Scratch cleanup

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing
$ ls -d /fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing 2>&1; echo "cleanup_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r33/MutCtrFetchMissing': No such file or directory
cleanup_exit=2
```

Scratch dir removed (the seat's `kasegi-r33/` parent remains, empty of this seat's tree). Receipt was written to the wave dir before removal; no evidence lived only in scratch.
