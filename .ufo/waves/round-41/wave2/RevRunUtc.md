# RevRunUtc — timestamp falsification

Scope: I2 run-utc/time-basis predicates. No final Y verification claimed.

## Findings

- **No demonstrated I2 defect for timezone-offset commit timestamps.** `ref_utc()` reads `%ct` (epoch seconds) and renders via `TZ=UTC date -u` (`corpus/instruments/r41-closure.sh:464-470`); therefore it normalizes the commit instant, rather than copying `%cI`’s offset representation. In an isolated fixture, an authored offset date was recorded as `%cI=2026-10-27T08:45:24-03:00`, `%ct=1793101524`; the suite’s epoch conversion path represents this instant as UTC. It binds the named ref’s committer instant, not the exported ref, as documented at lines 130-137.
- **I2 also checks current-clock upper bound with skew.** `iso_past()` parses UTC and compares its epoch to current UTC epoch +120 seconds (lines 472-482); receipt shape requires both exact equality to `ref_utc(ref)` and `iso_past` (lines 715-720). Thus a future-dated commit can only pass if its timestamp is within the explicit 120-second tolerance; farther-future `GIT_COMMITTER_DATE` should fail `not-future`, even if receipt text matches that ref.

## Reproduction and gap

Attempted an isolated temporary git fixture (verified top-level equals fixture path) with offset author date; output: `2026-10-27T08:45:24-03:00 1793101524`. Attempts to create a future committer timestamp using `GIT_COMMITTER_DATE=2999-01-01...` were rejected by this host Git as `fatal: invalid date format` (three accepted-format variants attempted). Therefore no future-committer commit or live I2 predicate run was reproduced. The future-date conclusion above is directly supported by the predicate implementation, not claimed as a reproduced mutation result.

Verification gap: no full suite/counter run or final judged-head/Y check performed. No tools installed.