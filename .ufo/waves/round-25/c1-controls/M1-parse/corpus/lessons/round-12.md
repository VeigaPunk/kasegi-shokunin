# Round 12 lessons — the untracked execution layer

## What worked

- **Batched 10-agent fan with adversarial roles paid for itself twice.** The
  two critics falsified 2 of ~15 re-measured prior claims (claims denominator
  275→274; "21 audits all BLOCKED"→22: 20 BLOCKED/2 READY) and the reviewer's
  74-citation audit found 9 mismatches + 1 broken path — all repaired in the
  same round. A coverage move that also measurably repaired depth.
- **Peer cross-checks caught L2 errors in flight.** ExecSkeleton broadcast
  "claim-ship is disjoint from origin/main"; ScoutFleet ran
  `merge-base --is-ancestor` (rc=0, 178-0) and ExecSkeleton self-corrected by
  IRC before anything was published. Lesson: git-topology claims need
  `--is-ancestor`/`rev-list --left-right`, never `log --oneline` eyeballing —
  and siblings should keep cross-checking each other's broadcasts.
- **My own prompt-carried number was wrong and the scout was told to verify
  it.** I briefed "248 entries" for `.ufo/sessions/` (a listing-tool artifact);
  the scout measured 8. Any number handed to an L2 must carry "verify this".
- **The reviewer's living-count distinction.** telemetry.jsonl 7218→7224 is
  append-only drift, not an error — the repair was as-of dating, not chasing
  the number. Living counts in a skill should always carry their date.

## Friction

- 805 M + 507 M + 117 M subtrees force census-by-structure (`du`, `find |
  wc -l`, first/middle/last sampling); full reads are impossible and the
  507 M `bh953b65628b4e` outlier (a foreign Rust tree) inflates any naive
  `.ufo/` file count ~12k.
- The sessions corpus is self-referential (403 hits are agents grepping
  sessions itself) and trap-laden (`no_submission_performed: true` → 471
  false positives). Grep patterns here need negative lookbehind or they lie.
- `check-freshness.mjs` appends telemetry on every "read-only" run (3
  `freshness_check` events added to `ledger/telemetry.jsonl` this round by
  critic runs) — already documented in `ops-invariants.md:109-110`, but worth
  remembering before any "harmless" live-run instruction to an L2.

## Residual gaps

- `.ufo/bounty-fleet/sessions/` (592 M) and `scopes/` (198 M) are
  structure+sample censused, not exhaustively read — recorded as deliberate
  in SCORECARD (not 10 on coverage).
- `george/` stays parked. `.omp/skills/ufo` drifted-fork mechanics + router
  role-contract defects are cross-domain (kumitate/protocol per connector
  matrix) — reported in the round file, not absorbed.
- Whether the 3 report-only bh ids ever had workspaces (deleted vs never
  created) is unobservable from disk.
- The stalled rebase's *cause* and autostash contents are unexamined (git
  mutation banned); L0 question filed.
