# Glob selects escaped symlink before confined match

## Finding — C1 mirror-fallback soundness gap (falsifiable; not runtime-exercised)

**Counterexample:** In `ResolveCliCase`, leave the fake `$HOME/Projects/bounties/ops/` absent, create an existing external file with `touch_scratch("outside-vault3/real.mjs")`, symlink it into the selected mirror as `ops/a-escape.mjs`, and create a regular in-mirror `ops/z-confined.mjs`. Resolve the citation `` `~/Projects/bounties/ops/*.mjs` ``.

**Expected under C1:** `MIRROR-EQUIVALENT`, with `resolved_path == <selected-mirror>/ops/z-confined.mjs` and domain `bounty`: the valid confined match must remain usable, while no outside target is credited. If the confined file is removed, the escaped-only match must instead be `GONE`.

**Current-source prediction [INFERENCE]:** `MIRROR-EQUIVALENT`, but with `resolved_path == <selected-mirror>/ops/a-escape.mjs`, whose real target is outside the mirror. `exists_any` expands the wildcard, sorts all glob matches, and returns only `matches[0]` (`resolve.py:163-177`). Since `a-escape.mjs` sorts before `z-confined.mjs`, it wins. The bounty-prefixed path then accepts the mirror fallback result without checking `under_mirror` (`resolve.py:202-213`); the realpath check exists at `194-199`, but this branch does not call it. Thus an out-of-root file can be credited as mirror-equivalent despite a valid confined match.

## Exact evidence and test gap

- Frozen C1 requires bounty-prefixed and relative mirror fallback paths not to credit symlink escapes, while preserving valid confined controls (`.ufo/waves/round-23/claims.json:4`).
- `exists_any` uses the first sorted glob result, with no per-result filtering (`corpus/instruments/resolve.py:163-177`).
- Bounty fallback returns `MIRROR-EQUIVALENT` for any result from `exists_any(mirror_root/rel)` (`resolve.py:202-213`); by contrast, explicit canonical mirror paths apply `under_mirror` at `resolve.py:214-222`.
- Current controls exercise a literal bounty mirror match (`test_resolve.py:249-253`) and one explicit-canonical symlink escape (`test_resolve.py:274-279`), but not a bounty glob containing both an earlier escaped symlink and a later confined file. Existing fixture helpers support this case (`test_resolve.py:80-103`).

**Compatibility invariant:** Do not change existing bounty canonical-path precedence (`resolve.py:207-209`), valid mirror-only bounty fallback behavior (`test_resolve.py:249-253`), or the `GONE` result when all candidates are missing/outside. Filter every glob candidate by realpath containment before selecting the first acceptable result; select the confined file in this example, and never report the escaped symlink.

**Scope / verification:** Read-only source inspection only; no fixture or test was run, as assigned. `git diff HEAD -- corpus/instruments/resolve.py corpus/instruments/test_resolve.py` was empty, so these target files have no observed diff at this checkout; this is a falsifiable attack item against the inspected source, not a changed-line attribution. LSP device/status was unavailable (attempted `xd://lsp`; device not mounted), so no references/definition/diagnostics claims are made. No grep was used.