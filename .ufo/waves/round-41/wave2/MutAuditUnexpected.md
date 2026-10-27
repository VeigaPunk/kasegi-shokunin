# MutAuditUnexpected — recheck-audit and binding orphan probe

## Mutation and detector

Started from integrated ref `ad7147532cb702b0d541d40499874552183d9132`, copied the lane into isolated `/fast/scratch/hyaku/kasegi-r41/MutAuditUnexpected/lane` (TMPDIR pointed there), and modified only that copy:

1. Added `corpus/knowledge/unlisted-r41-probe.md` with a syntactically valid `recheck:` line, but did not add it to `corpus/instruments/knowledge-expected.txt`.
2. Appended an unreferenced `S999` mined registry row (`https://example.invalid/orphan`) to `corpus/SOURCES.md`, without a capture or manifest record.

Ran the actual checkers against the mutated scratch tree: `python3 lane/corpus/instruments/recheck-audit.py --root "$PWD/lane" --json audit.json` and `python3 lane/corpus/instruments/capture-binding-check.py --root "$PWD/lane"`.

## Actual outputs / verdict

- Recheck audit exit **1**. It printed `unexpected=corpus/knowledge/unlisted-r41-probe.md`, then `lines=61 total=61 pass=61 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1` and `expect=present expected=60 missing=0 unexpected=1 exit=1`. The unlisted markdown does **not** survive silently.
- Capture binding exit **0**. It printed `AUDIT records=63 with_url=63 with_fetched_utc=25 with_archival=38 snapshot_dirs=17 manifest_dirs=17 missing_manifest=0 multi_row_url=4 orphans=1 orphan=S040-live.txt` and `records=63 bound=63 unbound=0`. The unreferenced mined registry row **does** survive this checker silently: no failure and unchanged 63/63 binding count. Binding is record-to-row/capture oriented; it does not enumerate registry rows requiring captures.

Classification for the assigned combined attack: **partially killed** — knowledge-file orphan killed; registry-row orphan survived. This establishes a coverage limitation of capture-binding-check, not a claim that it owns registry completeness.

## Evidence and cleanup

The checked-in instrument/allowlist hashes at probe time were: `recheck-audit.py` `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`; `capture-binding-check.py` `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`; `knowledge-expected.txt` `e030a8af914cadf2415a7887e2526c056f5bb2b9b8625266115c3b5ba0d5828d`. Probe-file hash was `0778b7fb42e63c0b9f7cefc48a19edc43cd01b4d44878a7d47c4f2c6ac8e31b4`; mutated registry hash was `422fa1d99601b5bcfd13d8050c3fefec70e41b9b2481d91cde7288ca9aa7141b`. Mutations were confined to the disposable scratch copy, then the scratch directory was removed. No tools installed. No final Y verification claimed.