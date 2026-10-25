# RevReadme — round 30 review

## Findings

- **High — README admission is not runnable against the admitted F14 entry.** `corpus/README.md` has the expected appended F14 map/frontier rows and the admitted-frontier count command returns 14. However, `python3 corpus/instruments/frontier-recheck-count.py` reports `FAIL F14 ... ids=- ... problems=missing-entry`, `entries=17 pass=16 exit=1`. The knowledge directory listing likewise lacks `japanese-severity-vocabulary-and-impact-model.md`. This contradicts frozen C2's required 17/17 harness pass and means F14's claimed entry is absent in the measured tree.
- **High — expected-list/recheck-audit is out of sync.** `corpus/instruments/knowledge-expected.txt` is still marked round 29 and lists 41 expected entries (42 lines including comments), omitting both the F14 entry and existing `considerthese-proposals-ledger.md`. Running `python3 corpus/instruments/recheck-audit.py` yields `unexpected=corpus/knowledge/considerthese-proposals-ledger.md`, `strict pass=41/42`, and `expect=present expected=41 missing=0 unexpected=1 exit=1`. Thus the required alignment/audit check fails; adding only F14 would still leave the existing unexpected file.

## Verified

- R6 head bytes: current README lines 1–51 and the base revision's same lines have identical SHA-256 `8844a0623a009bf9c0f57c8bed4c56f8a0dcc811ee65025a3f37fa46b5ae5797`.
- README includes appended F14 coverage-map row and frontier row in the existing table shapes (lines 266–284); count command returned `14`.
- C2 harness does not meet 17/17 (observed 16/17, exit 1), as detailed above.

## Residual risk / verification gaps

The requested positive end-to-end F14 entry and 17/17 harness result cannot be certified while the entry file is absent. No LSP device/server is available in this review environment; checks used the specified corpus scripts and direct file reads. No tools installed.