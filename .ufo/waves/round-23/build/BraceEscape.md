# C1 brace-expansion symlink escape falsifier

Axes in scope: `depth:verifiability` (C1 detector); coverage of a distinct bounty-fallback escape case.

## Finding — moderate: bounty brace fallback can credit an outside symlink

A concrete counterexample under the existing copied-CLI fixture layout:

1. Set `HOME` to the fixture home and `KASEGI_MIRROR` to `<fix>/relocated/tbh` as `test_resolve.py` does (lines 66–75, 119–135).
2. Create a regular file `<fix>/outside-vault/secret.mjs`, then symlink `<fix>/relocated/tbh/fleet/link.mjs` to that outside file.
3. Do not create a canonical bounty path for the token `~/Projects/bounties/fleet/{absent,link}.mjs:1`; leave the `absent` expansion missing.
4. Expected result under frozen C1: `GONE`, empty resolved path, domain `bounty`. Neither a canonical bounty file nor a confined mirror file supplies the citation; the only mirror-side match resolves outside the selected mirror.

Why this falsifies the current behavior: `classify` enters the bounty branch at `resolve.py:204–206`. `exists_any(base)` first checks the literal path (`:165–167`); for the missing braced literal it calls `brace_expand` and returns the first existing expansion (`:168–171`). With the fixture above, the matching expansion is the symlink pathname under the mirror; `os.path.exists` follows its target and returns true. The mirror fallback at `:210–212` accepts any nonempty method and returns `MIRROR-EQUIVALENT` without checking confinement. `under_mirror` already compares real paths (`:194–199`), but the bounty fallback does not call it. In contrast, the explicit canonical-mirror branch does call it (`:219–222`). Thus the candidate is reported as mirror evidence although `realpath(<mirror>/fleet/link.mjs)` is outside `<mirror>`.

Relevant test coverage: the existing in-mirror bounty control is only a literal path (`test_bounty_control_relative_under_mirror`, `test_resolve.py:249–253`). The escaping-symlink test uses an explicit canonical-mirror citation (`:274–279`), so it exercises the guarded branch, not bounty fallback. Add a CLI fixture combining a bounty-prefixed brace alternative with an escaping symlink; assert `GONE`, blank path, `bounty` domain. A falsifiable expected current result for the described inputs is `MIRROR-EQUIVALENT` with the symlink pathname.

## Compatibility invariant

Keep existing lane-first relative behavior: when the lane file exists, classify it as `INTERNAL` even if a mirror duplicate exists (`test_resolve.py:221–235`); C1's frozen `before_observed` explicitly excludes changing that prior lane-relative `../outside.md` behavior. For bounty fallback, a real file under the selected mirror must remain `MIRROR-EQUIVALENT` (literal control at `:249–253`), while a missing fallback remains `GONE` (missing-file control at `:197–208`). The new negative case must be based on resolved-target confinement, not a blanket ban on braces or bounty citations.

## Scope and verification limits

Read the frozen C1 claim (`claims.json:4`), resolver, and full relevant resolver test class. No tests were run and no source/test files were changed. `git diff` against the frozen base showed no diff for `resolve.py` or `test_resolve.py`; this is an uncovered implementation route / wave2 attack item, not a claim that a new resolver diff introduced it. The LSP device is not mounted (`xd://lsp` returned “No such tool”), so no LSP status/references/definition/diagnostics were available; this report relies on directly read code and test behavior, not grep or an LSP semantic claim. No dynamic fixture result is claimed.