# ExecExpectedList — round 30

## Changed file and behavior
- Updated `corpus/instruments/knowledge-expected.txt` to round-30 sorted tree paths, retaining the existing explanatory comment and adding F14 `japanese-severity-vocabulary-and-impact-model.md` plus `considerthese-proposals-ledger.md` as they appeared in the working tree.
- Expected list currently has **45 lines**: 2 comment lines + 43 entry paths. Initial bytes had **43 lines**: 2 comments + 41 entries. The two added entries were F14 and the simultaneously landing proposals ledger.
- Hash of list at initial generation (before ledger appeared in this seat's directory listing): `98282841943baaf75cabd2f7fef6ac67f2c23aee4a62750093ebbab4e5c854f6`. Later corrected from a fresh glob of the full knowledge tree.

## Verification evidence
Ran `python3 corpus/instruments/recheck-audit.py` twice after regeneration; each printed `expect=present expected=43 missing=0 unexpected=0 exit=1` and process exit 1. The full output also reports `lines=43 total=43 pass=43 fail-closed=25`, and `strict pass=42/43 ... instrument_fail=1 own_fail=1` due to `considerthese-proposals-ledger.md` (FROZEN-ONLY). Thus expected-list equality passes, but the required exit-0 acceptance criterion is NOT met; no claim of success.

The assignment's expected `expected=<n> missing=0 unexpected=0 exit=0` was not achieved. The blocker is outside this file's scope: recheck-audit's strict instrument/own limbs reject the newly landed `considerthese-proposals-ledger.md` recheck (it names no corpus instrument and does not name its own file). I did not alter that entry or the audit instrument. No tests/build/lint were run; the specified audit command was run. No tools installed.
