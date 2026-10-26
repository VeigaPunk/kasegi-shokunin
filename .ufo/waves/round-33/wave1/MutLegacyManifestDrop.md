# MutLegacyManifestDrop — rule-A mutation probe (round 33, wave 1)

seat: MutLegacyManifestDrop (mutation-tester, leaf; no subagents, no background jobs spawned)
date: 2026-10-26 (receipt stamped 2026-10-26T04:26:28Z)
assignment: mutation-test rule A of `corpus/instruments/capture-binding-check.py` — in a scratch copy, remove an entire legacy manifest file (`round-23/manifest.json`); the checker must exit 1 naming the dir. Report killed|survivor.
lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — read-only to this seat; every run below is against a scratch copy. No lane write, no git/jj mutation, no pacman transaction, no tool install (python3 stdlib was sufficient).

## Bytes under test

- instrument `corpus/instruments/capture-binding-check.py` sha256 `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9` — copy ≡ lane at probe time; re-hashed after the probe, unchanged.
- mutated file `corpus/source-snapshots/round-23/manifest.json` pristine sha256 `1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70`.
- copy fidelity: per-file sha256 lists of the whole copied `corpus/` tree vs the lane diff clean (`COPY_FIDELITY=ok`).
- scratch copy: `cp -a` of the lane `corpus/` tree (1.9 MB) to `$HYAKU_SCRATCH/kasegi-r33/MutLegacyManifestDrop/lane` (`HYAKU_SCRATCH` unset → default `/fast/scratch/hyaku`), taken 2026-10-26 after the S049/S050 registry rows landed (row poll: 21×20 s) and after the round-32 manifest landed (first poll, 1×20 s).
- drift provenance (bound 6): at the first copy the instrument digest was `5fa7868bf91941d8d9d39c71ba00492d347459ef875fa7d930fb244d01510837`; it moved to `b4182665…` (selftest 9→11 cases, `multi_row_url` field added) before the re-copy. Every figure below is from the `b4182665…` bytes; the earlier digest is named for drift provenance only. Lane `SOURCES.md` moved after the copy (copy `24738a86753edc13d66e40790305f785cdecced1dae4143159708627c382099b` vs lane `fe89b17a2e059ef0d6e934157fef7c72508f1421e87a82a4aafefad40bc68c3c` at the post-probe check) — in-flight sibling append; the rule-A detector bytes are the ones that stayed identical.

## Commands and output (all runs `cd "$S"`, `--root "$S/lane"`, `$S=/fast/scratch/hyaku/kasegi-r33/MutLegacyManifestDrop`)

### 0. Baseline — pristine copy

```
$ python3 lane/corpus/instruments/capture-binding-check.py --root "$S/lane"; echo "baseline_exit=$?"
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
baseline_exit=0
```

Baseline gate passes: exit 0 with C1's frozen summary `records=40 bound=40 unbound=0` (38 legacy `archival: true` records + 2 round-32 `fetched_utc` records). A baseline failure would have made the probe inconclusive; it did not fail.

### 0b. `--selftest` on the same bytes (instrument health)

```
$ python3 lane/corpus/instruments/capture-binding-check.py --selftest --scratch "$S/hyaku-scratch"; echo "selftest_exit=$?"
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=url-matching-two-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
selftest_exit=0
```

### 1. Mutation — remove the entire legacy manifest

```
$ cp "$S/lane/corpus/source-snapshots/round-23/manifest.json" "$S/pristine-round-23-manifest.json"
$ sha256sum "$S/pristine-round-23-manifest.json"
1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70  …/pristine-round-23-manifest.json
$ rm "$S/lane/corpus/source-snapshots/round-23/manifest.json"
$ ls "$S/lane/corpus/source-snapshots/round-23/"
S018.txt
S029.txt
S030.txt
S031.txt
```

After the mutation the directory still holds its four captured source files, so it still counts as a snapshot directory under rule A (manifest OR captured files) — the detector must flag it, not silently skip it.

### 2. Mutated run

```
$ python3 lane/corpus/instruments/capture-binding-check.py --root "$S/lane"; echo "mutated_exit=$?"
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=36 with_url=36 with_fetched_utc=2 with_archival=34 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=1
FAIL rule=missing-manifest dir=round-23
records=36 bound=36 unbound=0
mutated_exit=1
```

Expected detector: exit 1 naming the dir. Observed: exit **1** and `FAIL rule=missing-manifest dir=round-23` — the dir is named. The audit line moves coherently (`snapshot_dirs` stays 9 because the captures remain, `manifest_dirs` 9→8, `missing_manifest` 0→1, records 40→36 = the 4 round-23 records leaving the counted set; `multi_row_url` 2→1 because S029's record, one of the two duplicate-URL records, left the set).

### 3. Restore and re-run

```
$ cp "$S/pristine-round-23-manifest.json" "$S/lane/corpus/source-snapshots/round-23/manifest.json"
$ sha256sum "$S/lane/corpus/source-snapshots/round-23/manifest.json"
1f6d4fb50491354d1347676bb3f9a03884ee46f1178d62f3ff11f0b31b8d8e70  …/round-23/manifest.json
$ python3 lane/corpus/instruments/capture-binding-check.py --root "$S/lane"; echo "restored_exit=$?"
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
… (8 further MANIFEST lines identical to baseline) …
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
restored_exit=0
```

## Verdict

**KILLED.** The rule-A mutant (legacy manifest file removed, captures still present) is detected: exit 1 with `FAIL rule=missing-manifest dir=round-23`, exactly the contract's required output shape. Baseline and restored runs both exit 0 with the frozen summary `records=40 bound=40 unbound=0`. No survivor finding; nothing to route to a selftest (the instrument's own `missing-manifest-dir` selftest case already asserts this line at exit 1, and it passed on the tested bytes).

## Restoration evidence

- pristine sha256 `1f6d4fb5…` == post-restore sha256 `1f6d4fb5…` (byte-exact restore of `round-23/manifest.json` in the scratch copy).
- The lane was never written by this seat: lane `round-23/manifest.json` hashes `1f6d4fb5…` both before the probe and at the post-probe drift check; lane instrument hashes `b4182665…` at both points. The `rm` and the restore both operated only on `$S/lane/...` under the scratch tree.
- Scratch removed before yield: `rm -rf -- "$S"`; verification below.

## Notes (observations recorded, not verdicts)

- The tested bytes' docstring documents an "erratum 1" reading of rule B: a record URL that also occurs in another registry row (the registry's pre-existing W04 duplicate-URL rows) is counted informationally (`multi_row_url=N` on the AUDIT line) rather than failed as ambiguous. Baseline prints `multi_row_url=2` with `bound=40 unbound=0`. Recorded as observed on the tested bytes; rule-B semantics belong to the instrument owner's and the C1 critic's surface, not to this rule-A probe.
- Instrument digest drift inside the wave (`5fa7868b…` → `b4182665…`, selftest 9→11 cases) was observed between this seat's first and second copy. Figures here cite only the settled `b4182665…` bytes, per the M31-2 rule (a digest is a measurement with a timestamp, never an identifier).
- Tools installed: none (bound 5 record: nothing beyond stock python3 was needed).
- Scratch dir `$HYAKU_SCRATCH/kasegi-r33/MutLegacyManifestDrop` removed at exit; no seat tree left on disk.
