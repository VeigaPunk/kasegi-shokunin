# AttackA7 — instrument diff review: `recheck-audit.py` expected-list gate (C1(d))

- Seat: `L1Kasegi26.AttackA7` (reviewer, leaf). Round/wave: kasegi-shokunin round 26, wave 2 (falsify + integration closure).
- Date (UTC): 2026-10-25.
- Item: review the landed `recheck-audit.py` changes (git diff vs base `1b076fa7`): `--expect` argument + default resolution, expected-list reading (skip blank/#), set comparison, missing/unexpected receipt fields, exit semantics (0 clean/1 failed), `expect=present/absent` behavior, docstring updated, selftest count 15; flag any path by which a deletion could still pass (e.g. expected file deleted together with an entry), compared against claims' kill rules.
- Verdict: the landed instrument implements the documented behavior and reproduces the claim's C1(d) after-state; **three concrete deletion-pass paths remain** (all demonstrated on the landed bytes); one verifiability regression found (selftest tally line no longer emitted).

## Method (all read-only wrt the lane; scratch only under /tmp/a7scratch)

- Read: `claims.json` (FROZEN), `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md` (F11 row), `corpus/SOURCES.md` (S040/S041 + Registry changes), `corpus/lessons/round-26.md` (incl. integration closure), `corpus/instruments/recheck-audit.py` (landed bytes), `git diff 1b076fa7 -- corpus/instruments/recheck-audit.py`, `corpus/instruments/knowledge-expected.txt`, `.ufo/waves/round-26/c1-receipt-index.txt`, `c1-instrument-digest.txt`, `c1-live.json`, `c1-controls/{m1-*,e1-selftest-live.txt}`, `corpus/source-snapshots/round-26/manifest.json`, both new knowledge entries (via lesson/manifest context).
- Instrument digest check: `sha256sum corpus/instruments/recheck-audit.py` = `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1` — matches `c1-instrument-digest.txt` and `c1-receipt-index.txt:2`.
- Executions: `--selftest` (full output); live lane audit (`--root lane --cdroot lane --quiet`); scratch-mirror variants (full `corpus` copy + 39-entry expected list, `--cdroot <lane-root>`, exactly the C1(d) fixture shape): base / del / del-noexpect / del-synced / emptyexp / typo / rename.

## A. Behavior items — verified

1. **`--expect` + default resolution** (`recheck-audit.py:331-336`): default `<root>/corpus/instruments/knowledge-expected.txt` when the file exists; explicit `--expect` pointing at a missing file is treated the same as absent. Verified by runs: default-present → `expect=present`; explicit-missing → `expect=absent` (no error).
2. **Expected-list reading** (`load_expected`, :178-185): strips whitespace, skips blank lines and `#` comment lines (including indented comments), handles CRLF. Micro-test with mixed blank/comment/CRLF/trailing-space lines returned exactly the three content entries.
3. **Set comparison** (`expected_mismatch`, :188-194): `actual` from `glob(root/corpus/knowledge/*.md)` via `os.path.relpath(p, root)`; returns sorted `wanted - actual` (missing) and `actual - wanted` (unexpected). Verified: deletion → `missing=['corpus/knowledge/vdp-disclosure-packages.md']`; rename → `missing=1 unexpected=1`.
4. **Receipt fields** (:392-395): `expect` ("present"/"absent"), `expected_entries` (raw list), `missing_entries`, `unexpected_entries`; summary line `expect=… expected=… missing=… unexpected=… exit=…` (:426-435). Verified in JSON receipt of the deletion run: `expect=present expected=39 missing=[vdp-disclosure-packages.md] unexpected=[] complete=True pass=38 lines=38 total=38`.
5. **Exit semantics** (:350-352, :440): `ok = passed == len(entries) and complete and strict_passed == total and expect_ok`; process exit 0 iff clean, else 1. Verified: live 0; del/rename/emptyexp 1; del-noexpect/del-synced/typo 0.
6. **Docstring**: updated — expected-list contract paragraphs (default path, `#` comments, set equality, missing/unexpected naming, fallback note), usage lines incl. `--expect PATH`, exit-status paragraph. Present in landed bytes.
7. **Selftest count 15**: the selftest fixture set is 13 per-entry + 2 expected-list fixtures (`expect-missing`, `expect-unexpected`) = 15; running `--selftest` produced all 15 case lines with 0 FAIL and exit 0 (see §C for the tally-line regression).
8. **Live audit reproduces**: exit 0, `strict pass=39/39`, `lines=39 total=39 pass=39 fail-closed=23 executes=16`, `expect=present expected=39 missing=0 unexpected=0 exit=0` — byte-matches `c1-live.json` headline values.

## B. Deletion-pass paths (the attack) — demonstrated on landed bytes

Scratch mirrors: full `corpus` copy at `<root>/corpus/…` with the 39-entry committed expected list, run exactly as the claim's counter (d) (`--root <scratch> --cdroot <lane-root>`).

| # | Scenario | Exit | expect | missing/unexpected | Result |
|---|---|---|---|---|---|
| 1 | delete one entry only | 1 | present | missing=1 (names entry) | gated (claim's after-state reproduced) |
| 2 | delete entry **+ the whole expected file** | **0** | absent | 0/0 | **deletion passes** |
| 3 | delete entry **+ remove its line from expected** (sync edit) | **0** | present (38) | 0/0 | **deletion passes** |
| 4 | explicit `--expect /nonexistent/expected.txt` | **0** | absent | 0/0 | **silent downgrade to weaker gate** |
| 5 | empty expected file (present) | 1 | present | unexpected=39 | safe direction (never silently green) |
| 6 | rename source-recheck-owned entry (`multiparty…` → slug-changed) | 1 | present | missing=1 unexpected=1 | gated (M26-7 class now red) |

- **Path B2**: removing the expected file together with the entry drops the gate to glob-completeness (`expect=absent`), which cannot see the loss (`lines=38 total=38 pass=38` all equal) → exit 0.
- **Path B3**: keeping the committed list ( man the tree (deleting the entry's line, or regenerating the list from the working tree as the integration did) makes set equality vacuous → exit 0.
- **Path B4**: an operator who explicitly asks for the stricter gate with a wrong/missing path silently gets the weaker glob-only gate, exit 0, no warning.
- **Versus claim C1's kill rules**: the C1 kill rule is "any counter misses its after value, or the do-nothing control hits any after value". Under scenarios B2/B3 the frozen counter (d) would *miss its after value* (exit 0, nothing named), so the claim **is still falsifiable** — good — but no executed control (wave-1 mutants `m1-*`, integration fixture) exercises those scenarios, so the gate's demonstrated soundness covers *single-file deletion only*. The literal counter text (`--root <scratch-tree-with-one-knowledge-entry-deleted> …`) leaves it implicit that the scratch must contain the expected file; the after-value (and my reproduction of it) holds only because the fixture includes it.
- **Do-nothing control caveat**: the control is defined over "unchanged committed bytes (instrument, SKILL.md, lessons)"; `corpus/instruments/knowledge-expected.txt` is **untracked** (`git status`: `??`), and the entire round-26 build is currently uncommitted (working tree). The trusted-list assumption (the expected list cannot be edited/deleted alongside an entry) is therefore not yet protected by VCS.

## C. Selftest tally regression (verifiability defect)

- The landed diff **removed** the `print("selftest cases=%d …")` line (present in base `1b076fa7` at :221; current file: zero hits of `selftest cases`). `total_cases = len(cases) + 2` (:302) is now dead (assigned, never used). `--selftest` output ends at `selftest expect-unexpected exit=1 … ok`; **no** `selftest cases=15 failures=0 exit=0` line is emitted.
- Consequences: `c1-receipt-index.txt:4` (`selftest cases=15 failures=0 exit=0`) satisfies the frozen C1(b) grep (`grep -cE 'selftest cases='` → 1, verified) but it is now hand-maintained data rather than an instrument-produced receipt; it cannot be regenerated from instrument output. `ExecAuditFix.md`'s "Final line: `selftest cases=15 failures=0 exit=0`" is contradicted by its own recorded artifact (`e1-selftest-live.txt`, which contains no such line) and by my rerun. The 15-case run itself still passes (13+2, 0 FAIL, exit 0); the number is derivable from code + run, just not emitted. Relevant under the round's own R13/R3 discipline ("receipts produced by the one frozen instrument").

## D. Minor notes

- `expected_entries` is always present in the receipt (empty when `expect=absent`) — additive, no consumer break.
- The docstring says the list is "sorted"; `load_expected` does not enforce/verify sorting, and duplicates are silently deduped by set conversion. Inert for the gate.
- `missing=`/`unexpected=` prints are correctly gated behind `not args.quiet and expect_active`.

## Residual risk / verification gaps

- The three deletion-pass paths (B2/B3/B4) are real bypasses of the C1(d) soundness gate; the claim remains kill-able under them, but they are untested by the round's controls. Mitigations would be: (a) a strict `--expect` mode that errors (exit nonzero) when the given path is missing instead of silently downgrading; (b) making `knowledge-expected.txt` a tracked file with an explicit regeneration control; (c) documenting that the deletion fixture (and any future soundness claim) must define the scenario as entry-only vs coordinated.
- I did not re-run the C1(a)/(c) counters (out of scope: instrument diff); C1(b) caveat in §C.

Report: `.ufo/waves/round-26/wave2/AttackA7.md`
