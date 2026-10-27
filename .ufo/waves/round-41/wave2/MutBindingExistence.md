# MutBindingExistence — S063 manifest binding probe

## Target and detector

Claim attacked: C2 requires S063's manifest record to be bound to its capture and registry URL. Detector: `python3 corpus/instruments/capture-binding-check.py`; independent capture detector: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063`. Ran the pristine counter first from the lane: `records=63 bound=63 unbound=0`, exit 0 (round-41 manifest records=9). All mutations were performed only on a scratch copy under `/fast/scratch/hyaku/kasegi-r41/MutBindingExistence/`; no lane bytes changed.

## Exact mutation results

- Pristine S063 record (`path=S063.txt`, URL and capture_url both `https://www.rfc-editor.org/rfc/rfc9116.txt`): clean baseline binding counter `records=63 bound=63 unbound=0`, exit 0. (Pristine source-recheck was not run separately.)
- Missing capture path mutation: set `path=S063-missing.txt`, leave URL fields and file bytes unchanged. Binding checker still ended `records=63 bound=63 unbound=0`, exit 0 (**survived**). Source-recheck emitted `S063:manifest MISMATCH reason=stem-mismatch`, exit 1. This tests missing-path intent, but the changed basename also violates source-recheck's stem==id constraint, so it does not isolate file existence.
- URL case mutation: set both `url` and `capture_url` to `https://www.rfc-editor.org/RFC/rfc9116.txt`, preserving capture path and all other fields. Binding checker still `records=63 bound=63 unbound=0`, exit 0 (**survived**); source-recheck remained green: `S063:sha256 OK`; Q1/Q2/Q3 `OK`, each occurrences=1 and anchors 330/270/235 OK; exit 0.
- URL trailing-slash mutation: set both URL fields to `https://www.rfc-editor.org/rfc/rfc9116.txt/`, preserving capture path and all other fields. Binding checker still `records=63 bound=63 unbound=0`, exit 0 (**survived**); source-recheck emitted the same SHA/Q1/Q2/Q3 green lines, exit 0.

## Verdict

Coverage finding: capture-binding-check's `bound` counts URL/registry binding plus provenance, not record-path-to-file existence. Its `capture_files()` inventories files and the orphan logic only rejects unlisted actual capture files; it does not require every manifest record's `path` to name a present file. In addition, URL binding compares raw strings against the registry URL token (case-sensitive exact match), but this registry row also contains the identical URL in its `teaches` cell, so `url_row_count(cells, url)>1` increments informational `multi_row_url` without affecting binding. Case/trailing-slash changes in both URL fields remain record-bound because `bind_record` uses exact `record.url` against `row_tokens` only; `capture_url` is unused there. Source-recheck validates local capture content/hash/quotes, not URL identity; it passed both URL mutations.

The missing-path probe's source-recheck red is not evidence of an existence check: it reded at stem mismatch. A controlled missing-file probe retaining `path=S063.txt` but removing/renaming the file was not run, so existence behavior beyond the observed checker code is untested. The user's requested attack is nonetheless demonstrated for the emitted record path and URL variants: binding counter accepts all three mutations. No contract changes made.

Scratch removed by EXIT trap after probing. No tooling installed; no network fetch. No mutating git/jj command.
