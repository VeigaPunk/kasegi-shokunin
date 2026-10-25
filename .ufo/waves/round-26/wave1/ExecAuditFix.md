# ExecAuditFix — recheck-audit.py expected-list gate (C1(d) deletion soundness)

Round 26, wave 1 (build). Seat id `L1Kasegi26.ExecAuditFix`.
UTC access date: 2026-10-25.

## Files changed (only)

1. `corpus/instruments/recheck-audit.py` — sole-owner file, extended (123 insertions, 4 deletions vs base).
2. `.ufo/waves/round-26/c1-controls/e1-selftest-live.txt` — live record of selftest lines + exit and scratch-copy audit runs (this seat is the only writer).
3. `.ufo/waves/round-26/wave1/ExecAuditFix.md` — this report.

No other lane file was touched. `claims.json`, round-25 lessons, and all round-25 receipts untouched. No tools installed (Python stdlib only; `python3` 3.14.8).

## Behavior implemented

1. **`--expect PATH`** — new argument. Default resolution: `<root>/corpus/instruments/knowledge-expected.txt` when that file exists; explicit `--expect` pointing at a missing file is treated the same as absent. When active, the expected list is read (one sorted, lane-relative `corpus/knowledge/<entry>.md` filename per line; blank and `#` comment lines skipped) and compared as a set against the audited tree's actual `corpus/knowledge/*.md` entries (`os.path.relpath` against `--root`).
2. **Mismatch output + exit** — for each expected-but-absent entry prints `missing=<name>`; for each extra tree entry prints `unexpected=<name>`; either forces exit 1 (`expect_ok` is ANDed into `ok`). Prints sit in the non-`--quiet` path; the JSON receipt always carries them.
3. **Receipt fields** — added `expected_entries`, `missing_entries`, `unexpected_entries` (arrays) plus `expect` = `"present"`/`"absent"`. When absent/missing, the arrays are empty, `expect="absent"`, and the audit keeps its previous glob-completeness behavior (no re-word of the frozen limbs).
4. **Exit semantics** — 0 only when frozen limbs + strict set + completeness + expected-list equality all hold; 1 otherwise. Documented in the module docstring (expected-list contract: committed alongside knowledge files, drift = red audit).
5. **Selftest** — extended from 13 per-entry fixtures to 15 cases: `expect-missing` (expected list names an absent file → exit 1, receipt `missing_entries` names it) and `expect-unexpected` (tree has an unlisted extra file → exit 1). All 13 pre-existing fixtures and the completeness sanity line still pass. Final line: `selftest cases=15 failures=0 exit=0`.

## Evidence (run, 2026-10-25 UTC)

Selftest (recorded in `c1-controls/e1-selftest-live.txt`, instrument `sha256=3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`):

```
selftest cases=15 failures=0 exit=0        (selftest_exit=0)
selftest expect-missing  exit=1 want=1 missing=['corpus/knowledge/ghost-absent.md'] unexpected=[] ok
selftest expect-unexpected exit=1 want=1 missing=[] unexpected=['corpus/knowledge/extra.md'] ok
```

Scratch-copy audit (`/tmp/r26-execauditfix-scratch`, lane corpus copied; `--cdroot <lane-root>`):

- Baseline (expected list present, match): exit 0, `expect=present expected=37 missing=0 unexpected=0`.
- **Deletion trial** (removed `corpus/knowledge/vdp-disclosure-packages.md`): exit **1**, printed `missing=corpus/knowledge/vdp-disclosure-packages.md`; receipt `missing_entries=['corpus/knowledge/vdp-disclosure-packages.md']`, `unexpected_entries=[]`, `complete=True` (strict still 36/36 — the ONLY red signal is the expected list). This is the C1(d) before→after flip: the same tree without the expected list exits 0 (old hole, reproduced as `noexpect-scratch exit=0`).
- **Extra-file trial** (`/tmp/r26-execauditfix-scratch-extra`): exit **1**, printed `unexpected=corpus/knowledge/unexpected-extra.md`; receipt `unexpected_entries=['corpus/knowledge/unexpected-extra.md']`.
- Explicit `--expect /nonexistent/expected.txt`: `expect=absent`, exit 0 (current behavior preserved).

## Notes / risks

- The sibling seat `ExecExpectedList` had already landed `corpus/instruments/knowledge-expected.txt` (round 26, two-line `#` header, 37 entries) in the lane during this wave; the default resolution picked it up (that is the intended integration, and the `#`-comment handling was needed for it).
- `knowledge-expected.txt` itself is **not** this seat's owned path; it was not created or edited here (only read from the scratch copy).
- Receipt schema grew additively; no existing consumer reads a fixed-length key set that would break.
