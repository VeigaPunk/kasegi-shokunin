# ExecImplC1 — round 29 wave 1

Implemented frozen C1 in `corpus/instruments/anchorcheck.py` only.

- Added a nine-limb registry, with distinct failing cases for bounties/mirror/origin `OUTSIDE-BASE` and mirror/origin `BASE-ABSENT` arms.
- Selftest has 12 cases: nine fail-class cases and three controls. Coverage compares registered names to cases actually executed; missing coverage increments failures.
- Git-free PATH prints `SKIP pin-broken (git not found)`, counts the pin case as skipped/exercised for registry completeness, and exits cleanly. Existing `GIT_*` sanitization remains.
- Fail-class exit behavior and `LOST-RECORDED` recorded-not-fail behavior remain unchanged.

## Evidence

Normal command: `python3 corpus/instruments/anchorcheck.py --selftest`

```text
selftest cases=12 failures=0
limbs=9 covered=9
exit=0
```

Git-free PATH run (PATH contains only a symlink to `python3`):

```text
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
nogit_exit=0
```

Final `anchorcheck.py` SHA-256: `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`.

Diff saved at `.ufo/waves/round-29/wave1/ExecImplC1.diff`. No tools installed or updated. No build/lint/test/formatter run; the two requested selftest executions are the assignment's behavioral checks.

## Risks / blockers

No known blocker. PIN-BROKEN is intentionally skipped when Git is unavailable; the remaining eight fixtures and registry coverage still run. Parent should run post-integration gates and confirm the canonical receipt index records the matching digest.
