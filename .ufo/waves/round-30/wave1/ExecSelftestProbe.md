# ExecSelftestProbe — round 30 wave 1

## Axes
- `depth:verifiability`: requested B1/B2 instrument conformance and source recheck evidence.
- `coverage`: F14 entry/recheck evidence.

## Probe results (observed current working-tree bytes)
- `python3 corpus/instruments/source-recheck.py --selftest` → exit **1**; `selftest cases=9 failures=1`. Eight cases pass; `stem-mismatch` FAIL: expected exit 1 / `S901:manifest`, observed exit 0 / `S901:sha256,S901:Q1`. This falsifies the requested B1 acceptance criterion on the bytes measured. File sha256: `0b841d5ddb80f96f0e802eec1e67a0b9ba0606609282d8991759db72ac71a243`.
- Source inspection of current instrument lines 123–126 confirms a stem comparison in `check_source`, but the selftest fixture at lines 342–349 writes `S901.txt` and expects mismatch; therefore its current fixture does not exercise the claimed mismatch. B1 is not demonstrated by this selftest.
- `python3 corpus/instruments/recheck-audit.py` → exit **1**. Output: `lines=42 total=42 pass=42 fail-closed=25 parse_fail=0 cwd_fail=0 paths_fail=0 exit=1`; strict summary `pass=41/42 ... instrument_fail=1 own_fail=1`; expected-list summary `expect=present expected=41 missing=0 unexpected=1 exit=1`, specifically `unexpected=corpus/knowledge/considerthese-proposals-ledger.md`.
- F14 entry probe, `bash -n`, and foreign-cwd recheck were **not runnable**: `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` does not exist in the observed lane tree. This was confirmed by glob and a direct `find` query (no result). No changed corpus entry was available to inspect.

## Changed files
- `.ufo/waves/round-30/wave1/ExecSelftestProbe.md` only.
- No tool installed; no network/target interaction.

## Risks / blockers
- The requested post-B1/B2 source-recheck implementation is not in a passing state at the measured bytes. Another executor is assigned that implementation; rerun selftest only after its landed bytes are present.
- Recheck audit currently fails due to the unlisted `considerthese-proposals-ledger.md` and strict audit classifications above; not altered here because outside this probe's assigned paths.
- F14 entry absent as measured; entry-specific parse/cwd checks remain unproved and should be run when it lands.