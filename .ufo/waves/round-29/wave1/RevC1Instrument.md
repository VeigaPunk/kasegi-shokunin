# RevC1Instrument — C1 review

## Verdict
**Agree with the normal-PATH C1 implementation, with one narrow coverage-reporting defect on the git-free path.** The required ordinary selftest and all three new fixture controls were independently exercised; the documented digest matches the landed bytes.

## Evidence
- Landed `corpus/instruments/anchorcheck.py` SHA-256: `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`; matches `.ufo/waves/round-29/wave1/c1-receipt-index.txt:3`.
- Re-ran final selftest twice at that digest: both `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0.
- Verified each new fixture against an exact baseline copy fetched from `7a6591c1eb8a14f427297980a96fa8bb339f29ee`; baseline SHA-256 `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`. Mirror escape and origin escape each produced exactly `OUTSIDE-BASE` and exit 1; absent origin root produced exactly `BASE-ABSENT` and exit 1. The baseline itself reports `cases=9 failures=0`, no `limbs=` line, and git-free PATH produces `FileNotFoundError: 'git'`, exit 1.
- The nine existing fixtures retain their input/expected-verdict/exit intent (the outside-bounties and mirror-absent case names were made arm-specific; three new cases were inserted). Diff changes are confined to the instrument docstring and selftest/limb region; `main()`'s fail-class exit behavior and `LOST-RECORDED` recorded-not-fail behavior are unchanged.
- Landed git-free PATH run: `SKIP pin-broken (git not found)`, `cases=12 failures=0`, `limbs=9 covered=9`, exit 0, no stderr/traceback.
- No `lsp` device/server is mounted in this session; semantic references/definition/diagnostics were unavailable, so review used the diff and executed behavior, not grep as semantic proof.

## Finding — low severity: skipped PIN-BROKEN is counted as covered
`corpus/instruments/anchorcheck.py:329-334,358-369`: when git is absent the pin fixture is skipped, but the branch appends `pin-broken` to `executed`; `covered` then counts it as an executed limb and prints `limbs=9 covered=9`. This makes the coverage summary claim a fixture ran when it did not. The regular-PATH run does execute and validate PIN-BROKEN, so this does not invalidate the normal 9/9 result or the required git-free exit-0 behavior; it does make the git-free summary misleading. Track skipped names separately and exclude them from `covered` (or explicitly report the reduced coverage) to keep the summary truthful. `n_skip` is incremented but never reported/used.

## Residual risk / verification gaps
The ordinary run proves the nine named cases execute and assert the expected verdict vectors, and the new cases fail on baseline. Git-free mode intentionally cannot exercise PIN-BROKEN. No unrelated build/lint/tests were run. No tools were installed or updated.
