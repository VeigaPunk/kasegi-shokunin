# Round-65 claims erratum 3 — the driver verifies its own bytes

Appended after erratum 2 (`155737d0863fc4463998f060b58d1c7510f5f96d`) and before the final measured run
(there is no earlier final run against a later tip). Predicate, metric, kill rule, targets and axes unchanged.

## Defect

After errata 1 and 2 the predicate's `driver_sha256` named bytes that no longer existed, and nothing in the
counter enforced the pin: a mutated driver would print a green summary. SentinelScope raised the missing
work guard and worktree-only provenance (S-02/S-03); CriticC1's amendment 2 asked for exactly this check
(`w1/CriticC1.md` § D2, `w1/SentinelScope.md` ≥5).

## Amendment (counter only)

`.ufo/waves/round-65/driver.sha256` sits beside the driver and holds its sha256. At startup the driver prints
`GUARD driver-self-pin PASS` only when `sha256(__file__)` equals that pin; a mismatch or a missing pin prints
`RESULT driver-self-pin FAIL` and exits 1 before any measurement. `--print-inputs` is unaffected.

Amended driver: `.ufo/waves/round-65/verify-r65.py`, sha256
`7f27c4d2fe43db875453478983faa39d44d7aa8ae82b455fb3ff8f039e9f6172`, pinned in `driver.sha256`.
This supersedes the `driver_sha256` of `claims.json` (`533a6d4f…`), erratum 1 (`5aa842ab…`) and erratum 2
(`a5fb3b04…`).

## Re-measured, unchanged

- before: `VERIFY measurements=8 failures=3`, exit 1 at `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
  (`controls/driver-base-donothing-r65.txt`, `GUARD driver-self-pin PASS`);
- construction: 8/0 exit 0 (`controls/driver-construction-r65.txt`);
- final: `controls/final-verification-tip-r65.txt`.

The H1 residual (SIGPIPE masking a later operand's error) remains named open; erratum 3 does not touch it.
