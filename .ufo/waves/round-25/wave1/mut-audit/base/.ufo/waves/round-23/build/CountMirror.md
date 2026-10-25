# CountMirror — round 23 build

## Scope and files

Implementation was made only in private clone `/tmp/kasegi-r23-CountMirror-5`, checked out at the observed base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`.

- Added `corpus/instruments/mirror-containment-check.py`.
- Added `corpus/instruments/mirror-containment-fixtures.json`.
- No resolver, corpus, global configuration, or external substrate was changed. In the live repository, this assigned report is the only write.

The checker copies the selected `resolve.py` to a disposable `/tmp` work directory and invokes that copied CLI once with isolated `HOME`, `KASEGI_MIRROR`, and lane fixtures. `--resolver PATH` selects alternate resolver bytes for identical matrix replay; `--fixtures PATH` is also available. Output is JSON Lines: one record per fixture `id` with expected/actual class, followed by total counts, SHA-256 identities for resolver and matrix, and CLI problems. It checks the CLI exit code, TSV schema/rows, stdout `distinct` count, missing/duplicate/unexpected citations, and returns nonzero on mismatches. Bounds are enforced for matrix size, case/setup counts, path lengths, and CLI duration. Setup paths cannot escape the temporary fixture root; intentional escapes resolve only to fixture-created outside files/symlinks.

## Frozen C1 — exact retained items

```json
"C1": {
  "axis": "depth:verifiability",
  "detector": "corpus/instruments/resolve.py classify plus copied real CLI TSV",
  "claim": "Make MIRROR-EQUIVALENT sound: bounty-prefixed and relative mirror fallback paths cannot credit parent traversal or symlink escapes outside the selected mirror. Preserve valid confined mirror and missing-file controls; reject sibling-root prefix confusion.",
  "before_observed": "~/Projects/bounties/../outside.md is MIRROR-EQUIVALENT for a file outside mirror; relative ../outside.md is INTERNAL (not targeted: explicit lane-relative paths keep prior semantics).",
  "after": "All declared mirror-escape and prefix-confusion fixtures classify GONE; confined controls retain expected classes. Before and after use identical fixture inputs and actual copied CLI. Score remains 4; no source availability restoration or corpus-internal citation growth credit.",
  "guard": "Frozen pre-round SKILL, PROVINCE and corpus against each detector; report all changed verdicts, density and anchorcheck. Detector soundness, not stale scorecard-cell editing, is the axis move."
}
```

The matching source is `.ufo/waves/round-23/claims.json:4` at the frozen base. No claim field was edited or recast.

## Matrix coverage and pinned expectations

The committed JSON matrix has 15 IDs. Its eight distinct escaped-path cases all pin `GONE`:

1. `bounty-parent-traversal` — exact cited shape `~/Projects/bounties/../outside.md`.
2. `relative-fallback-symlink` — mirror-only relative path points to a fixture file outside the mirror; `lane_absent` asserts it is not found lane-first.
3. `bounty-symlink-escape` — bounty fallback symlink to an outside file.
4. `nested-symlink-escape` — two-link chain under mirror reaches an outside file; lane path is asserted absent.
5. `placeholder-expansion-escape` — placeholder glob under a parent-traversal suffix matches only outside the mirror.
6. `glob-expansion-escape` — wildcard expansion under a parent-traversal suffix matches only outside the mirror.
7. `canonical-tilde-alias-parent-escape` — explicit canonical tilde alias with parent traversal.
8. `canonical-absolute-alias-symlink-escape` — expanded fake-HOME canonical alias reaches an outside file through a symlink.

Four controls pin the ordinary expected classes: confined bounty and relative mirror fallback are `MIRROR-EQUIVALENT`; confined canonical alias is `RESOLVES`; absent bounty target is `GONE`. The separate `canonical-sibling-prefix-boundary` pins `GONE` while a `-legacy` decoy exists under the selected mirror, preventing a loose prefix alias. `lane-relative-parent-remains-internal` pins `../outside.md` as `INTERNAL`, explicitly distinguishing the frozen lane-relative behavior from mirror fallback. `empty-citation-produces-no-row` pins `NO-ROW`; in the complete matrix it is submitted beside non-empty citations so the CLI does not receive an empty-corpus input.

## Exact retained source evidence and falsifiable finding

- `corpus/instruments/resolve.py:163-177` implements literal, brace, placeholder-to-glob, and wildcard existence checks.
- `resolve.py:194-199` defines realpath containment in `under_mirror`.
- `resolve.py:202-234` shows bounty fallback at 210-213 and relative mirror fallback at 230-233 return `MIRROR-EQUIVALENT` without calling `under_mirror`; explicit canonical alias resolution at 214-222 does call that guard.
- `resolve.py:306-313` writes the CLI TSV consumed by this checker. The existing `test_resolve.py:105-161` documents the local convention of copying the resolver and reading its subprocess TSV and summary rather than asserting resolver source text.
- `resolve.py:329` takes `max()` over emitted rows without an empty-list default.

**Falsifiable source-level finding, not a runtime result:** `[INFERENCE—unrun]` with the checked-in case setup, the current unmodified source should emit an unsafe mirror-equivalent class for the first six escape cases because their escaped target exists and those two fallback branches lack realpath containment. The two explicit-alias escape cases should remain `GONE` under the existing `under_mirror` gate. The copied-CLI matrix will either confirm or falsify those predictions by case ID and TSV class. No CLI run was made in this wave.

## Verification status, risks, and blockers

No tests, builds, linters, or formatters were run, per the assignment's “No tests run yet” instruction. The fixture runner itself is unexecuted. Suggested owner-side probes are:

```text
python3 corpus/instruments/mirror-containment-check.py
python3 corpus/instruments/mirror-containment-check.py --resolver /path/to/baseline/resolve.py
```

The same committed matrix hash is reported for both invocations; a successful result requires the real copied CLI to exit with the pinned code and each ID to match its JSON expected class. The no-row fixture is only an empty citation in a populated batch; the resolver's zero-row `max()` crash remains a source-observed out-of-scope behavior, not patched here. This seat makes no admission or integration claim. No blocker for the scoped implementation was encountered.
