# Round 23 C1 attack item: placeholder glob can credit an escaping mirror symlink

**Axes:** `depth:verifiability` (C1). **Scope:** read-only source/test inspection of `corpus/instruments/resolve.py` and `corpus/instruments/test_resolve.py`; no production edits and no repository tests run.

## Finding

The bounty-prefixed mirror fallback can report `MIRROR-EQUIVALENT` for a placeholder glob whose selected match is a symlink to a file outside the selected mirror. `under_mirror()` correctly checks `realpath` containment at `resolve.py:194-199`, and the explicit canonical-mirror path applies it at `:219-222`; the bounty fallback instead returns any `exists_any()` result unconditionally at `:210-212`. `exists_any()` replaces `<...>` with `*`, sorts glob matches, and returns the first at `:172-176` (pattern configured at `:88`). The relative mirror fallback likewise returns a hit unconditionally at `:230-233`.

### Concrete falsifier (fixture design; not run through the project test suite)

Use the existing CLI fixture contract from `test_resolve.py:64-111`: an empty fake `HOME`, a selected `KASEGI_MIRROR`, and a lane citation. Put a real `outside-vault/real.mjs` outside the selected mirror and make `mirror/route.mjs` a symlink to it. Submit the path-like citation:

```text
~/Projects/bounties/<entry>.mjs
```

The empty fake HOME makes the primary bounty lookup at `resolve.py:207-209` miss. For the mirror fallback, `exists_any(mirror/<entry>.mjs)` expands to glob `mirror/*.mjs`; the glob selects `mirror/route.mjs`. Its `realpath` is outside `mirror`, but `classify()` returns `MIRROR-EQUIVALENT` at `:211-212` without calling `under_mirror()`. **Required C1 result: `GONE` with an empty resolved path**, because a symlink escape must not count as mirror evidence. This is falsifiable by asserting both the class/path and that `realpath(selected_match)` lies outside `realpath(mirror)`.

A scratch stdlib probe (not the repository tests) confirmed that `glob.glob("<mirror>/*.mjs")` returns a matching symlink pathname while its `realpath` is outside the mirror. The source path above establishes the resulting class; the full resolver CLI/test was intentionally not run in this assignment.

The same missing post-glob confinement exists for relative fallback paths at `resolve.py:230-233` when the lane-root lookup misses and a relative `<placeholder>` glob selects an escaping symlink under the mirror.

## Compatibility invariant

Confinement must be checked on the selected result after literal/brace/glob expansion: a mirror fallback may yield `MIRROR-EQUIVALENT` only when `under_mirror(resolved_path, mirror_root)` is true. Preserve valid confined mirror hits and existing precedence: `test_bounty_control_relative_under_mirror` at `test_resolve.py:249-253` requires the in-mirror bounty mapping to remain `MIRROR-EQUIVALENT`; `test_relative_precedence_internal_then_mirror_then_gone` at `:221-235` requires lane-first `INTERNAL`, a confined mirror-only `MIRROR-EQUIVALENT`, and an absent relative path `GONE`. Existing symlink confinement coverage at `:274-279` exercises the explicit canonical-mirror branch, not either fallback branch.

## Scope limits / verification gaps

This is one source-derived attack item for C1, not a claim that a patch or acceptance run exists. The repository's `test_resolve.py` was inspected but not executed or modified. No tests, builds, linters, or formatters were run; no tools were installed. The adjacent parent-traversal behavior is already represented in C1's frozen `before_observed`; this report isolates the distinct placeholder-glob plus symlink-escape route.
