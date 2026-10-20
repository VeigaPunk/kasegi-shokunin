# FixMirror — scoped finding and implementation

## Frozen claim and scope

- Frozen claim: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/claims.json`, `C1` (`depth:verifiability`), read at snapshot `D8F5`, line 4.
- Private edit base: commit `922a4dde90b60b465e2b8b241d1fe363f1f27e98`, cloned with `git clone --no-hardlinks` to `/tmp/kasegi-r23-FixMirror-5` and checked out detached.
- Edited only `/tmp/kasegi-r23-FixMirror-5/corpus/instruments/resolve.py` and `/tmp/kasegi-r23-FixMirror-5/corpus/instruments/test_resolve.py`. No production source was edited in the live repository. This report is the only live-repository write.

## Falsifiable finding and retained evidence

At the frozen base, `/tmp/kasegi-r23-FixMirror-5/corpus/instruments/resolve.py` read snapshot `9FA8` showed:

- Lines 194–199 define `under_mirror()` with `realpath()` and `commonpath()` confinement.
- Lines 204–213 classified any `base.startswith(BOUNTY_PREFIXES)` as bounty, then formed a suffix with `base.split("/Projects/bounties", 1)[1]`. This accepts a sibling such as `~/Projects/bounties-x/...`; its suffix begins `-x/...` and can be mapped under the selected mirror.
- Lines 207–212 first preserve a directly existing bounty source, but the mirror fallback returned `MIRROR-EQUIVALENT` on `exists_any()` alone, without calling `under_mirror()`.
- Lines 230–234 check lane-relative paths first, then likewise returned `MIRROR-EQUIVALENT` for any existing mirror fallback without confinement. The explicit canonical-mirror branch at lines 220–222 already used `under_mirror()`.

These observations match the frozen C1 `before_observed` description. A falsifier for bounty fallback uses `KASEGI_MIRROR=/tmp/<test-fixture>/relocated/tbh`, no direct fake-HOME file at `/tmp/<test-fixture>/home/Projects/bounties/../outside-vault/secret.mjs`, and an existing target at `/tmp/<test-fixture>/relocated/outside-vault/secret.mjs`: citation `~/Projects/bounties/../outside-vault/secret.mjs:1` must be `GONE`, not `MIRROR-EQUIVALENT`. Citation `../outside-vault/secret.mjs:1` must also be `GONE` when `/tmp/<test-fixture>/lane/../outside-vault/secret.mjs` is absent. An external symlink target gives the same `GONE` expectation for bounty and relative fallbacks. L1 separately reported a concrete bounty brace-expansion symlink escape; the added pattern cases cover brace, glob, and placeholder expansion, each selecting an external symlink from `/tmp/<test-fixture>/relocated/tbh/`. For prefix confusion, `~/Projects/bounties-x/fleet/mirror-only.json:1` must be `GONE`/`other` when absent from fake HOME even if `/tmp/<test-fixture>/relocated/tbh/-x/fleet/mirror-only.json` exists; a direct fake-HOME sibling file must remain `RESOLVES`/`other`.

The pre-change test file read at snapshot `BAD9` had a confined bounty control at lines 249–253 and canonical-mirror traversal/symlink cases at lines 255–279, but lacked bounty-fallback and relative-fallback escape cases, the `bounties-x` sibling case, and pattern-expansion escape cases.

## Private implementation

- `/tmp/kasegi-r23-FixMirror-5/corpus/instruments/resolve.py`: bounty selection now requires exact root equality or a slash-delimited descendant and derives the suffix from the matched root. The direct-source `exists_any(base)` return remains before fallback confinement. Bounty and relative mirror fallback results now require `under_mirror(p, mirror_root)`. The lane-relative-first return is unchanged. The resolver policy docstring now documents the boundary and confinement rules.
- `/tmp/kasegi-r23-FixMirror-5/corpus/instruments/test_resolve.py`: extended the valid bounty control with an existing direct-source control; added `bounties-x` direct/mirror-only controls; added bounty and relative parent-traversal and symlink-escape fallback cases; added bounty brace, glob, and placeholder fallback symlink cases; and added a `../` lane-relative `INTERNAL` control. Test fixture roots now use `/tmp` with the existing teardown.

The above are implemented assertions, not observed post-change outcomes. No tests, builds, linters, formatters, copied-CLI probes, or detector runs were executed, per assignment. No admission, score, or acceptance credit is claimed. L1 should run the assigned copied-real-CLI fixture and integration checks against the identical inputs.

## Scope limits and tooling

No changes were made to explicit absolute direct-source resolution, relative lane-root precedence, input symlink policy, subprocess execution-environment restrictions, anchor-range behavior, corpus inputs, scorecards, global configuration, or external substrates. LSP was unavailable: the mounted tool inventory exposes no LSP client/interface. The mounted `grep` search in `/tmp/kasegi-r23-FixMirror-5/corpus/instruments` found the resolver call in `resolve.py` and no other instrument callsite for these symbols; this is not represented as an LSP result.
