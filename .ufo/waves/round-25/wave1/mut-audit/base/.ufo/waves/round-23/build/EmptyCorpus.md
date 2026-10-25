# Round 23 C1 — empty-corpus CLI attack item

**Axis:** `depth:verifiability`. **Frozen claim:** C1 in `.ufo/waves/round-23/claims.json:2`.

## Finding: the real CLI aborts on zero extracted citations

Concrete counterexample: invoke the copied real CLI on a lane root whose `SKILL.md` contains only ordinary prose (no path-like backticked token) and which has no `corpus/**/*.md` path citations. `collect()` returns an empty `cites` mapping (`corpus/instruments/resolve.py:250-276`); `main()` consequently constructs `rows == []` (`:286-304`) and writes the TSV header (`:306-314`), then unconditionally evaluates `max(r["nfiles"] for r in rows)` (`:329-330`). Python raises uncaught `ValueError: max() arg is an empty sequence`; the CLI exits unsuccessfully before producing its Markdown report or stdout summary (`:331+`, `:546-557`). This is source-derived; I did not execute the CLI or tests, per assignment.

**Expected result/class:** the empty set has no citation rows, hence no per-citation class (not `GONE`). The CLI should complete with `distinct=0`, zero counts in each terminal class, and empty-denominator rates as `n/a` (`pct()` at `:347-349`). The concrete C1 path-level escape control remains `~/Projects/the-bounty-hunter/../outside-vault/secret.mjs:1` -> **`GONE`**: the fixture deliberately creates the target outside the mirror realpath and asserts that class (`test_resolve.py:255-272`).

## Needed control and compatibility invariant

Add a separate real-CLI no-path-citation control (e.g. `run_cli([])`): assert exit 0, an empty TSV data section, and a zero-distinct summary. This only guards empty-input reporting; it should not change `classify()` or any mirror/relative path policy. The current runner already launches the actual CLI and requires exit 0 (`test_resolve.py:106-139`), but every current case supplies at least one citation (examples at `:178-279`); no empty-citation case is present. Preserve C1's explicit-lane-relative compatibility: the frozen claim says relative `../outside.md` remains `INTERNAL` under the prior lane-relative behavior and is not targeted (`claims.json:2`). Also retain the stated confined mirror, missing-file, and prefix-sibling controls (`test_resolve.py:197-235,249-279`).

## Scope and verification gaps

This is an empty-input CLI liveness/control gap, not evidence that C1's mirror-escape classification is unsound. `git diff` against the frozen base produced no diff for `resolve.py` or `test_resolve.py`, so this observation is not attributed here to a round-23 change. The LSP device is unavailable in this session (`read xd://lsp` returned “No such tool”); no grep was used or treated as semantic evidence. No tests or runtime probes were run.