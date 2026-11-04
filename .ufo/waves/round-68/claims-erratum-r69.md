# Round-68 claims — appended correction (written round 69; `claims.json` bytes unchanged)

Routed by the round-68 non-author spot-check (`corpus/lessons/round-68-verifier-spotcheck.md:45-49`, V68-1).

- `claims.json` `"frozen_at": "2026-11-04T21:52:00Z"` is a hand-typed value later than the commit that
  ships it. The actual freeze time is the committer date of `7c4f9f7ec096298b1edd1912249e5864ee73d985`
  (`git log -1 --format=%cI 7c4f9f7e` → 2026-11-04T18:50:37-03:00 = 21:50:37Z), which precedes the
  implementation commit `82b3b7d4` (21:50:54Z). Commit order was correct; the declared field was not.
  Round 69's `claims.json` names no clock time of its own and defers to its freeze commit's committer date.
- V68-2: the round-68 report printed the base selftest line as `ok`; the committed receipt
  `controls/c1-base-donothing-r68.txt` reads `MEASURE selftest FAIL selftest cases=73`. The receipt is
  authoritative.
- V68-5: `controls/seat-reproduction-r68.txt` names "GNU coreutils sort 9.12" — that is the binary the gate
  executes (`/usr/bin/sort`, measured round 69: `.ufo/waves/round-69/controls/c1-base-donothing-r69.txt`
  `HOST` line). The round-68 report, `w1/RevengerC1.md` and `w1/CriticC1.md` statements that the host sort is
  "uutils sort 0.8.0" describe the omp bash tool's builtin `sort`, not the gate's binary. The round-68 counter
  docstring's "six legitimate read-only derives" runs five (`controls=5`); the R68 gate comment's "420 KB
  fixture" is 480000 bytes (60000 lines of 8 bytes) and was corrected in the round-69 gate comment.
