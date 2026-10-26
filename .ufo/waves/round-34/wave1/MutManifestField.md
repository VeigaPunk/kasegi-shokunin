# MutManifestField — manifest mutants vs `capture-binding-check.py`

- Round 34, seat `MutManifestField` (L2 wave 1, dispatched by KasegiR34, hyaku run 8).
- Item: field seven manifest mutants against the landed `corpus/instruments/capture-binding-check.py`; controls = the clean round-32/round-34 manifests.
- Date: 2026-10-26. Lane repo read except this receipt; no git/jj commands run; no tool installs (none needed).

## Report

### Detector under test

`corpus/instruments/capture-binding-check.py`, sha256
`3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`.
CLI: `--root <lane-root>` (scanner), `--selftest [--scratch <dir>]` (fixture selftest).
Exit contract: 0 pass / 1 any rule failure / 2 read or shape error.

### Controls — pristine bytes pass (round-32 and round-34 clean manifests)

Commands (run first, before any mutation):

```
python3 corpus/instruments/capture-binding-check.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin   # → lane-control exit=0
python3 corpus/instruments/capture-binding-check.py --root $S/fixture                                      # → fixture-control exit=0
diff $S/out/lane-control.txt $S/out/fixture-control.txt && echo controls-identical=yes
python3 corpus/instruments/capture-binding-check.py --selftest --scratch $S/selftest                       # → selftest exit=0
```

(`$S` = `/fast/scratch/hyaku/kasegi-r34/MutManifestField`; `fixture/` = byte copy of lane `corpus/SOURCES.md` + `corpus/source-snapshots/`.)

Observed outputs, exit codes:

- `lane-control exit=0`, `fixture-control exit=0`, `controls-identical=yes` (diff empty).
- lane-control stdout (13 lines), quoted exactly as captured:

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
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=41 bound=41 unbound=0
```

The two clean targets: `MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0` and
`MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0`, summary `records=41 bound=41 unbound=0`, exit 0.
`orphan=S040-live.txt` is informational only (declared orphan; no FAIL line, exit stays 0) — consistent with C1's "manifest record or orphan listing".

- Selftest (detector sanity, claim C1 expects cases>=19): `selftest exit=0`, full listing:

```
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass
selftest case=duplicate-id-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=pass
selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-detected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-listed exit=0 want=0 verdict=pass
selftest case=nested-snapshot-dir exit=0 want=0 verdict=pass
selftest case=nested-snapshot-missing-manifest exit=1 want=1 verdict=pass
selftest case=dup-record-in-manifest exit=1 want=1 verdict=pass
selftest case=double-https-row exit=1 want=1 verdict=pass
selftest case=rejected-row-anchor exit=1 want=1 verdict=pass
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest case=complete-selftest-report-accepted exit=0 want=0 verdict=pass
selftest cases=23 failures=0
```

### File digests (pristine lane bytes; fixture copies verified equal)

| file | sha256 |
|---|---|
| `corpus/source-snapshots/round-32/manifest.json` | `72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6` |
| `corpus/source-snapshots/round-34/manifest.json` | `d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe` |
| `corpus/SOURCES.md` | `4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6` |
| `corpus/instruments/capture-binding-check.py` | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |

Fixture `corpus/SOURCES.md` digest identical to lane (`4c85ff86…`); fixture manifests are `cp -r` copies of the same bytes.
Whole-fixture-tree digest (sorted relpath+bytes sha256, driver `tree_digest`): `b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651` — every mutant starts and ends at this value.

### Mutants — seven fixtures, all fielded in isolated scratch copies

Driver: `$S/field_mutants.py` (stdlib only; per mutant: fresh `copytree` of the pristine fixture → minimal mutation → checker subprocess → record stdout/exit → restore exact pristine bytes in place → re-run → whole-tree digest compare). Full captured run output follows verbatim (`$S/out/field-mutants-run.txt`, driver exit=0):

```
==============================================================================
mutant=m1-fetched-pending
mutation=round-34 S051 fetched_utc "2026-10-26T05:31:10Z" -> "pending"
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=0 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=2 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=fetched-utc record=S051 dir=round-34 detail=pending
records=41 bound=40 unbound=1
expected_failure=FAIL rule=fetched-utc record=S051 dir=round-34 detail=pending
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m2-fetched-local-offset
mutation=round-34 S051 fetched_utc -> "2026-10-25T23:14:00-03:00"
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=0 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=2 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=fetched-utc record=S051 dir=round-34 detail=local-offset
records=41 bound=40 unbound=1
expected_failure=FAIL rule=fetched-utc record=S051 dir=round-34 detail=local-offset
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m3-nested-hidden-records
mutation=round-34/inner/ hides two captures (S051.txt moved in, S052.txt added), no manifest
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=11 manifest_dirs=10 missing_manifest=1 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=missing-manifest dir=round-34/inner
records=41 bound=41 unbound=0
expected_failure=FAIL rule=missing-manifest dir=round-34/inner
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m4-dup-record
mutation=round-32 manifest: S050 record duplicated (same id and path twice)
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=3 url_bound=3 fetched=3 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=42 with_url=42 with_fetched_utc=4 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=dup-record field=id value=S050 count=2 dir=round-32
FAIL rule=dup-record field=path value=S050.txt count=2 dir=round-32
records=42 bound=42 unbound=0
expected_failure=FAIL rule=dup-record field=id value=S050 count=2 dir=round-32
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m5-double-https-row
mutation=SOURCES.md S050 source cell gains a second https:// token
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=1 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=double-https-row row=S050 n=2
FAIL rule=url-ambiguous record=S050 row=S050 tokens=2 dir=round-32
records=41 bound=40 unbound=1
expected_failure=FAIL rule=double-https-row row=S050 n=2
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m6-rejected-row-anchor
mutation=SOURCES.md S049 status cell mined -> rejected
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=1 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
FAIL rule=rejected-row-anchor record=S049 row=S049 dir=round-32
records=41 bound=40 unbound=1
expected_failure=FAIL rule=rejected-row-anchor record=S049 row=S049 dir=round-32
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
mutant=m7-orphan-capture
mutation=round-34: undeclared capture S099.txt next to the manifest
tree_before=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651
--- checker stdout (exit=1)
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=41 with_url=41 with_fetched_utc=3 with_archival=38 snapshot_dirs=10 manifest_dirs=10 missing_manifest=0 multi_row_url=2 orphans=2 orphan=S040-live.txt orphan=S099.txt
FAIL rule=orphan-capture file=S099.txt dir=round-34
records=41 bound=41 unbound=0
expected_failure=FAIL rule=orphan-capture file=S099.txt dir=round-34
verdict=KILLED
tree_after=b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651 restored=yes
rerun_exit=0 rerun_matches_control=yes
restoration=VERIFIED
==============================================================================
SUMMARY mutant=m1-fetched-pending KILLED restoration=verified
SUMMARY mutant=m2-fetched-local-offset KILLED restoration=verified
SUMMARY mutant=m3-nested-hidden-records KILLED restoration=verified
SUMMARY mutant=m4-dup-record KILLED restoration=verified
SUMMARY mutant=m5-double-https-row KILLED restoration=verified
SUMMARY mutant=m6-rejected-row-anchor KILLED restoration=verified
SUMMARY mutant=m7-orphan-capture KILLED restoration=verified
mutants=7 killed=7 survived=0
```

### Verdict table

| # | mutant | mutation point | named failure observed | exit | verdict |
|---|---|---|---|---|---|
| 1 | m1-fetched-pending | round-34 S051 `fetched_utc` → `"pending"` | `FAIL rule=fetched-utc record=S051 dir=round-34 detail=pending` | 1 | KILLED |
| 2 | m2-fetched-local-offset | round-34 S051 `fetched_utc` → `"2026-10-25T23:14:00-03:00"` | `FAIL rule=fetched-utc record=S051 dir=round-34 detail=local-offset` | 1 | KILLED |
| 3 | m3-nested-hidden-records | `round-34/inner/` holds two captures, no manifest | `FAIL rule=missing-manifest dir=round-34/inner` | 1 | KILLED |
| 4 | m4-dup-record | round-32 S050 record duplicated | `FAIL rule=dup-record field=id value=S050 count=2 dir=round-32` (+ `field=path value=S050.txt count=2`) | 1 | KILLED |
| 5 | m5-double-https-row | SOURCES.md S050 cell gains 2nd `https://` token | `FAIL rule=double-https-row row=S050 n=2` + `FAIL rule=url-ambiguous record=S050 row=S050 tokens=2 dir=round-32` | 1 | KILLED |
| 6 | m6-rejected-row-anchor | SOURCES.md S049 status `mined` → `rejected` | `FAIL rule=rejected-row-anchor record=S049 row=S049 dir=round-32` | 1 | KILLED |
| 7 | m7-orphan-capture | undeclared `round-34/S099.txt` | `FAIL rule=orphan-capture file=S099.txt dir=round-34` | 1 | KILLED |

`mutants=7 killed=7 survived=0`. No mutant survived; no baseline (control) failure occurred, so no run is inconclusive.

### Restoration evidence

Per mutant, in the same scratch tree: `tree_before == tree_after == b96920218a89dd7449b82819fbcc700a8307c3d411cd3ad4bf0a6e3e884e1651`; restored re-run `exit=0` with stdout byte-identical to `fixture-control.txt` (`rerun_matches_control=yes` in all seven blocks). Lane bytes re-measured after all runs — unchanged:

```
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
d5077f81fc2bc2c843cb2f3e82c673fdf5e4e2431b93cfc3391731ced242eebe  corpus/source-snapshots/round-34/manifest.json
4c85ff8608dda20f6396b201031d9b19f574afd8cde6afc8a8fe47cffc9e77b6  corpus/SOURCES.md
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
```

### Coverage observations (findings, not contract changes — for the L1 to weigh)

1. **m3 blind side, already documented:** after moving `S051.txt` into `round-34/inner/`, rule A printed `MANIFEST round-34 records=1 url_bound=1 fetched=1` unchanged — no rule flags a record whose named capture file is absent (the instrument's docstring records this reverse direction as out of scope; `source-recheck.py` fails closed on a missing capture). The two hidden files also stay out of `orphans=` accounting (`AUDIT … snapshot_dirs=11 manifest_dirs=10 missing_manifest=1 orphans=1` — they belong to the missing-manifest dir). The mutant still fails via `missing-manifest`, so the case is covered; the hidden *files* only become fully auditable once a manifest exists in the nested dir (selftest case `nested-snapshot-dir` exercises that pass path).
2. **m4 counts:** the dup-record failure leaves `records=42 bound=42 unbound=0` — the failure lives in the FAIL lines and exit status, not in `unbound`, matching the docstring's "duplicates leave records/bound/unbound unchanged". Read the exit, not only the summary.
3. **m1/m2 tighten `bound` but not `url_bound`:** provenance failures move `bound=40 unbound=1` while `url_bound` stays 1 — rule B and rule C are independently counted, as designed.
4. **No exit-2 path was required by the item and none was fielded** (all seven named failures are exit 1); exit 2 (read/shape errors) is covered by the checker's own selftest (`UNAVAILABLE` limbs) and was not re-tested here.

### Scratch cleanup (defect check)

```
rm -rf -- /fast/scratch/hyaku/kasegi-r34/MutManifestField
ls /fast/scratch/hyaku/kasegi-r34/ | grep -c MutManifestField   → 0
echo "grep-rc=$?"                                                → grep-rc=1 (scratch dir absent)
```

No scratch tree remains; the mut-* trees were removed by the driver before the final sweep, and the receipt text was secured before deletion.

Report: .ufo/waves/round-34/wave1/MutManifestField.md
