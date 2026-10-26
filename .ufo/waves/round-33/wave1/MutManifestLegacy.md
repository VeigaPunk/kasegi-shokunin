# MutManifestLegacy — round-33 wave1 mutation receipt

- Seat: MutManifestLegacy (mutation tester, leaf — no subagents dispatched, no git/jj mutations, no pacman transactions, no installs, no network fetches).
- Answering model: zai/glm-5.3-flash (recorded per bound 10; the probe itself is model-independent).
- Probe: remove the `url` field from one record in a **scratch copy** of `corpus/source-snapshots/round-24/manifest.json` (exact-once byte patch) and run `corpus/instruments/capture-binding-check.py` against the mutated tree. Detector must exit 1 and name the record (rule B). Unmutated copy must exit as the real tree does.
- Scratch: `/fast/scratch/hyaku/kasegi-r33/MutManifestLegacy` (`HYAKU_SCRATCH` unset → default base), a full copy of `corpus/source-snapshots/` plus `corpus/SOURCES.md` plus the instrument; removed before this receipt was finalized (evidence at the end).

## Inputs (sha256, pinned at copy time)

| artifact | sha256 |
|---|---|
| `corpus/instruments/capture-binding-check.py` (lane, authoritative run) | `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` |
| same, scratch copy | `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` (identical) |
| `corpus/SOURCES.md` (scratch copy) | `fe89b17a2e059ef0d6e934157fef7c72508f1421e87a82a4aafefad40bc68c3c` |
| `corpus/source-snapshots/round-24/manifest.json` pristine | `77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` |
| same, mutated | `82bead0c24b6a7bbfa0aa08f6514f1f106a858715a0c0c8cddc5f556362d6e87` |
| same, restored | `77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` (byte-exact) |

## PRE-STATE run (labeled per bound 6; not citable)

First probe ran while ExecRegistryAppend had not yet appended rows S049/S050 to `corpus/SOURCES.md`: real tree exit=1, `records=40 bound=38 unbound=2` with `FAIL rule=no-row record=S049 dir=round-32` / `FAIL rule=no-row record=S050 dir=round-32` — baseline failure, so that run was INCONCLUSIVE even though the S001 mutant was already named. Waited on the registry rows (`until` poll, ~100 s), then re-ran the identical probe. All runs below are on quiescent bytes.

## Authoritative run (quiescent bytes)

Driver: Python; per run the detector was invoked as
`python3 <tree>/corpus/instruments/capture-binding-check.py --root <tree>` (real tree = lane root with the committed instrument; scratch runs with the pinned copy).

### 1. Real tree, unmutated (baseline) — exit 0

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
```

### 2. Scratch pristine copy — exit 0, output byte-identical to run 1 (`outputs_identical_real_vs_pristine=True`, `records=40 bound=40 unbound=0`)

### 3. Mutated (rule B probe) — exit 1

Patch: removed exactly this byte line (asserted `occurrences_of_removed_line=1`, i.e. exact-once over the manifest bytes) at byte offset 641:

```
      "url": "https://www.first.org/cvss/v4.0/user-guide",
```

Post-patch assertions: mutated file is valid JSON; record S001 has no `url`; all 18 other records byte-identical parsed (`other_records_untouched=True`).

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=18 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=39 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=url-mismatch record=S001 detail=absent dir=round-24
records=40 bound=39 unbound=1
```

Exactly one FAIL line; it names the record (`names_record=True`). Rule B (absent url → unbound) is enforced: bound dropped 40→39, exit 1.

### 4. Restored (exact pristine bytes written back) — exit 0

`manifest_restored_sha=77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` == pristine (`restored_matches_pristine=True`); output identical to run 2 (`restored_output_matches_pristine=True`).

### 5. Stability checks

Real-tree re-run after restore: exit 0, output identical to run 1 (`real_rerun_output_identical=True`); instrument hash unchanged across the probe (`instrument_stable_during_probe=True`).

## Verdict

**KILLED.** Baseline (real tree and pristine copy) exits 0 with `records=40 bound=40 unbound=0`; the url-removal mutant flips the detector to exit 1 and names `record=S001` under `rule=url-mismatch ... detail=absent`; the restored tree is byte-identical (same sha256) and passes again. No surviving-mutant coverage finding.

## Cleanup / restoration evidence

- Scratch tree removed in a `finally` block; after the probe: `ls -d /fast/scratch/hyaku/kasegi-r33/MutManifestLegacy` → `No such file or directory`.
- Lane `corpus/source-snapshots/round-24/manifest.json` post-probe sha256 `77b158caac9ae80890dd2948a72fc2ab2ed8f8be3f5e5f67b5260cce100b00a3` — unchanged; the mutation existed only in the scratch copy.

Report: .ufo/waves/round-33/wave1/MutManifestLegacy.md
