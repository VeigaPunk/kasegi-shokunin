# Round-65 claims erratum 2 — revision-bound frozen inputs, a work guard and a run timeout

Appended after erratum 1 (`a333d8ef7183a9d8bb969c6ec5c29b8db01f7481`) and before the final measured run.
It corrects the driver, not the claim: predicate, metric, kill rule, target values and axes are unchanged.

## Defects (found by the wave's attack seats, before the final measured run)

- **D2 (CriticC1):** the driver read the probe collector, the mutation battery and the candidate from the
  mutable lane worktree, and measurement 8 hashed those worktree bytes — a worktree edit could move both the
  input and its pin. Receipt: `.ufo/waves/round-65/w1/CriticC1.md` § D2.
- **S-02/S-03/S-08 (SentinelScope):** `--work` was unguarded (`--work .` would `git checkout --force` into
  the lane) and measurement children ran without a timeout. Receipts:
  `.ufo/waves/round-65/w1/SentinelScope/10-l1-driver-final.txt`, `08-scan.txt`.

## Amendment (counter only)

1. The three frozen inputs are materialised from the commit that added each path (`git log --diff-filter=A`),
   never from the worktree; the candidate overlay is copied from those bytes; measurement 8 hashes them.
2. `--work` must resolve under `/fast/scratch/hyaku/` unless `VERIFY_R65_ALLOW_WORK=1` is set.
3. Every measurement child runs with a 900 s timeout and records `[timeout 900s]` / exit 124 on expiry.

Amended driver: `.ufo/waves/round-65/verify-r65.py`, sha256
`a5fb3b043a6dbb04325b5fd0e06e0d9545c605726ad063b738de85caf90d36e1`. This supersedes the `driver_sha256`
of `claims.json` (`533a6d4f…`) and of erratum 1 (`5aa842ab…`).

## Unchanged and re-measured

- before: `VERIFY measurements=8 failures=3`, exit 1 at `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`
  (`controls/driver-base-donothing-r65.txt`);
- construction: 8/0, exit 0 (`controls/driver-construction-r65.txt`);
- final: 8/0, exit 0 at `1c36d724c91cdd8585219798ea7cf60bb4f24b5b` (`controls/final-verification-r65.txt`).
- The claim's H1 residual (a SIGPIPE-truncated producer can mask a later operand's error) is **not** fixed by
  this erratum; it is named open in the lesson (M65-7) and the report.
