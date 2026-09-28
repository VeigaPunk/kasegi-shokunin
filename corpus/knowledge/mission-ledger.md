# Mission ledger — `ledger/*.jsonl` + rankings artifacts

Source: `~/Projects/bounties/ledger/` (missions.jsonl 718 lines,
telemetry.jsonl 7218 lines, candidates.jsonl 8, imports.jsonl 8, ~30
`rankings-<ts>.json` artifacts), `ops/shared.mjs`, `ops/rank.mjs`,
`ops/import-board.mjs`, `ops/fleet-dispatch.mjs`, `docs/plan-round0.md`.
Counted 2026-09-28.

## Writer contract

`ops/shared.mjs::appendLedger(root, kind, entry)` is the only writer.
Append-only — never rewrites history. Three kinds: `telemetry` | `missions` |
`imports`. Serialized lines are capped at **3500 bytes** so concurrent
cross-session `O_APPEND` writes stay atomic (POSIX PIPE_BUF); oversize entries
are replaced by a `{truncated:true}` marker, never split.

## `missions.jsonl` — hunter-contract state machine

One line per transition: `{ts, mission_id, program, transition, producer,
model, note?, artifact?}`. Observed transitions (count over 718 lines /
260 mission_ids / 218 programs):

| Transition | Count | Meaning (observed) |
|---|---|---|
| `DISCOVERED` | 1 | board-imported program record created |
| `NORMALIZED` | 1 | record rewritten with field-level provenance |
| `DEDUPED` | 1 | collision resolved |
| `SCOPED` | 232 | scope-snapshot taken (the AR14 bounded policy read) |
| `RANKED` | 3 | EV-ranked by `ops/rank.mjs` |
| `PLANNED` | 219 | hunt plan written (`fleets/missions/<program>.md` exists) |
| `EXECUTED` | 1 | hunt ran |
| `EVIDENCED` | 2 | evidence package assembled |
| `VERIFIED` | 1 | review passed |
| `SUBMISSION_PREPARED` | 1 | `prepare-claims.mjs` payload staged |
| `SUBMITTED` | 3 | operator actually submitted (mozilla, spotify, airtable) |
| `DISCLOSED_FREE` | 1 | VDP disclosure path |
| `LEARNED` | 244 | terminal: honest-zero / parked — the dominant exit |

Dominant path: `SCOPED→PLANNED→LEARNED` (207 missions). `SCOPED→LEARNED` (9)
is the park-at-scope path (auth wall / no assets). Deepest observed path:
`SCOPED→PLANNED→EVIDENCED→VERIFIED→SUBMISSION_PREPARED→LEARNED`
(immunefi-gamma). Full pipeline `EXECUTED→EVIDENCED→VERIFIED` is rare —
most missions terminate at LEARNED without a claim deliverable, matching the
486-mission partition in `terminal-classes.md`. `SUBMITTED` only ever
follows operator action; it is a ledger fact, not a fleet transition.

`ops/rank.mjs` suppresses duplicate `RANKED` attestations (scans the ledger
for a same-mission last-line), emits `rankings-<YYYYMMDDTHHMMSSZ>.json`
(-1/-2 suffix bumps so sha256 attestations never break), and advances
`mission_state` `DISCOVERED→RANKED` in the program record. Rankings artifact
shape: `{generated_at, defaults{ev defaults}, ranked[{id, expected_reward,
p_success, gross_value, total_cost, adjusted_ev, inputs_basis}], unknown[]}`.
`inputs_basis:"curated"` vs `default_estimate` distinguishes real EV inputs
from the default prior set (p_in_scope .7, p_repro .7, p_unique .25,
p_accepted .6, effort 60h, risk 250).

## `telemetry.jsonl` — dispatcher heartbeat

~30 event kinds. Observed distribution: `dispatcher_tick` 3680,
`mission_parked` 1188, `mission_dispatched` 1167, `fleet_synced` 249,
`freshness_check` 233, `binding_verified` 224, `lease_claimed` 107,
`attempt_reset` 68, `operator_decree` 58, `mission_retired`/`_claimed`/`_done`
31/31/26, `claim_rejected` 16, `mission_failed` 21, `claim_commit_failed/blocked`,
`model_reroute`, `lane_parked`, `lane_degraded`, `provenance_drift`.

`ops/shared.mjs::TELEMETRY_EVENTS` enumerates the *registry* kinds
(lane_parked, lane_degraded, operator_decree, xask_dry, board_imported,
binding_verified, reroute_drill, provenance_drift); `fleet-dispatch.mjs`
emits the runtime kinds (dispatcher_tick, mission_*, claim_*, fleet_synced).
`gitMutationBlocker(root)` fail-closes every git-mutating path on active
rebase/merge/cherry-pick or HEAD not on `main`; blocked mutations log
`claim_commit_blocked`/`claim_push_blocked` instead of failing silently.

## `candidates.jsonl` — external hunter intake

8 records written by `the-bounty-hunter` runs (`run_id` b1k-NNN):
`{program_id, name, scope_url, reliable, offers_bounties, safe_harbor,
public_scope, slice, decision, scope_file, notes}`. `decision` is either
`"<run> claim"` (candidate for mission selection) or `no-claimable-work`
with `program_id:null`. `scope_file` points at
`.ufo/bounty-fleet/scopes/<program>/SCOPE*.md` — scope bytes live in the
.ufo tree, the ledger only references them.

## `imports.jsonl` — board-import binding

`ops/import-board.mjs` is fail-closed: refuses to run unless the ledger's
last `board_imported` event `evidence_id` matches the board's
`refresh_evidence.json` evidence_id exactly (`importsLedger` check).
Records `{run_id, evidence_id, counts{written, live, snapshot_retained,
stale_snapshot, collisions, protected}}`. First import wrote 1087 programs:
258 live, 829 stale_snapshot — the board feed is mostly stale snapshots
by design (freshness is a label, not a gate).

## Ops inventory (all consumers/producers)

| Tool | Role |
|---|---|
| `shared.mjs` | invariants + `appendLedger` + `gitMutationBlocker` + `sha256File` |
| `validate.mjs` | schema + referential checks (M1) |
| `import-board.mjs` | one-way run-id-bound board feed (M3/M6) |
| `registry-check.mjs` | lane/model invariants, k3-seat count (M4) |
| `reroute-drill.mjs` | simulated park→reroute telemetry drill (M4) |
| `check-freshness.mjs` | staleness verdicts (M5) |
| `rank.mjs` | EV ranking → rankings artifacts + RANKED lines |
| `ev-report.mjs` | per-program adjusted-EV (fail-closed UNKNOWN) |
| `fleet-dispatch.mjs` | tmux mission spawner, lease/claim/commit loop, telemetry |
| `park-disposition.mjs` | unpark/retire dispositions → telemetry |
| `claim-check.mjs` | package validator (see `claim-gates.md`) |
| `claim-index.mjs` | operator queue generator |
| `prepare-claims.mjs` | deterministic payload staging |
| `finalize-all.mjs` | batch finalize |
