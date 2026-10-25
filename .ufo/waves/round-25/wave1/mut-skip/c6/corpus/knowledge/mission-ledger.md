# Mission ledger — `ledger/*.jsonl` + rankings artifacts

Source: `[lost-tree] ~/Projects/bounties/ledger/` (missions.jsonl 718 lines,
telemetry.jsonl **7225 lines as of 2026-09-28T21:52:51.978Z** — round-13
correction: the r12 count 7218 was time-of-audit; the file grows on every
`[lost-base] ~/Projects/the-bounty-hunter/ops/check-freshness.mjs:61` invocation, including audit runs, candidates.jsonl
8, imports.jsonl 8, **234** `rankings-<ts>.json` artifacts over 229 distinct
stamps — round-13 correction: "~30" was a transcription of the event-kind
count), `ops/shared.mjs`, `ops/rank.mjs`, `ops/import-board.mjs`,
`ops/fleet-dispatch.mjs`, `docs/plan-round0.md`. Counted 2026-09-28, counts
carry as-of stamps where the file is live-appended.

## Writer contract

`ops/shared.mjs::appendLedger` (root, kind, entry) is the only writer.
Append-only — never rewrites history. Three kinds: `telemetry` | `missions` |
`imports`. Serialized lines are capped at **3500 bytes** so concurrent
cross-session `O_APPEND` writes stay atomic (POSIX PIPE_BUF); oversize entries
are replaced by a `{truncated:true}` marker, never split.

Round-13 caveat: "append-only" describes the writer contract, not the file
bytes — the worktree `telemetry.jsonl` carries **3 committed git
merge-conflict marker lines** from a 2026-09-06 merge (worktree lines
4460 `<<<<<<< HEAD` / 4462 `=======` / 4480 `>>>>>>> 3d28a716` at the
7224-line state; present in HEAD and index too, which hold 6383 lines vs the
worktree's 7225). `JSON.parse` fails on exactly those 3 lines; the sole
in-repo consumer `fleet-dispatch.mjs:80-85 attempts()` filters by regex and
never parses, so the corruption is invisible to every gate.

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
| `SUBMISSION_PREPARED` | 1 | `~/Projects/the-bounty-hunter/ops/prepare-claims.mjs` payload staged |
| `SUBMITTED` | 3 | operator actually submitted (mozilla, spotify, airtable) |
| `DISCLOSED_FREE` | 1 | VDP disclosure path |
| `LEARNED` | 244 | terminal: honest-zero / parked — the dominant exit |

Dominant path: `SCOPED→PLANNED→LEARNED` (207 missions). `SCOPED→LEARNED` (9)
is the park-at-scope path (auth wall / no assets). Deepest observed path:
`SCOPED→PLANNED→EVIDENCED→VERIFIED→SUBMISSION_PREPARED→LEARNED`
(immunefi-gamma). Full pipeline `EXECUTED→EVIDENCED→VERIFIED` is rare —
most missions terminate at LEARNED without a claim deliverable, matching the
486-mission partition in `corpus/knowledge/terminal-classes.md`. `SUBMITTED` only ever
follows operator action; it is a ledger fact, not a fleet transition.

`ops/rank.mjs` suppresses duplicate `RANKED` attestations (scans the ledger
for a same-mission last-line), emits `rankings-<YYYYMMDDTHHMMSSZ>.json`
(-1/-2 suffix bumps so sha256 attestations never break), and advances
`mission_state` `DISCOVERED→RANKED` in the program record. Rankings artifact
shape: `{generated_at, defaults{ev defaults}, ranked[{id, expected_reward,
p_success, gross_value, total_cost, adjusted_ev, inputs_basis}], unknown[]}`.
`inputs_basis:"curated"` vs `default_estimate` distinguishes real EV inputs
from the default prior set — round-13 correction, full set from
`[lost-base] ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` DEFAULTS: p_in_scope .7, p_reproducible .7, p_unique .25,
p_accepted .6, effort_hours 60, opportunity_rate 25, direct_cost 0,
delay_cost 0, expected_risk_cost 250 (earlier text omitted opportunity_rate
and the zero costs).

## `telemetry.jsonl` — dispatcher heartbeat

35 distinct event keys live (round-13 census; the r4 text said "~30").
Census method matters: count LINES matching `"event"\s*:\s*"<name>"`
(excluding non-event `"kind":` lines) — the file mixes 7065 compact
`"event":"x"` with 143 spaced `"event": "x"` lines, and a naive
`grep -o '"event":"X"'` undercounts `attempt_reset` by 92% (5 vs 68) and
`lease_claimed` by 20% (86 vs 107). Observed distribution: `dispatcher_tick` 3680,
`mission_parked` 1188, `mission_dispatched` 1167, `fleet_synced` 249,
`freshness_check` 233, `binding_verified` 224, `lease_claimed` 107,
`attempt_reset` 68, `operator_decree` 58, `mission_retired`/`_claimed`/`_done`
31/31/26, `claim_rejected` 16, `mission_failed` 21, `claim_commit_failed/blocked`,
`model_reroute`, `lane_parked`, `lane_degraded`, `provenance_drift`.

`ops/shared.mjs::TELEMETRY_EVENTS` enumerates the *registry* kinds
(lane_parked, lane_degraded, operator_decree, xask_dry, board_imported,
binding_verified, reroute_drill, provenance_drift); `~/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs`
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
| `~/Projects/the-bounty-hunter/ops/shared.mjs` | invariants + `appendLedger` + `gitMutationBlocker` + `sha256File` |
| `~/Projects/the-bounty-hunter/ops/validate.mjs` | schema + referential checks (M1) |
| `~/Projects/the-bounty-hunter/ops/import-board.mjs` | one-way run-id-bound board feed (M3/M6) |
| `~/Projects/the-bounty-hunter/ops/registry-check.mjs` | lane/model invariants, k3-seat count (M4) |
| `~/Projects/the-bounty-hunter/ops/reroute-drill.mjs` | simulated park→reroute telemetry drill (M4) |
| `~/Projects/the-bounty-hunter/ops/check-freshness.mjs` | staleness verdicts (M5) |
| `~/Projects/the-bounty-hunter/ops/rank.mjs` | EV ranking → rankings artifacts + RANKED lines |
| `~/Projects/the-bounty-hunter/ops/ev-report.mjs` | per-program adjusted-EV (fail-closed UNKNOWN) |
| `~/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` | tmux mission spawner, lease/claim/commit loop, telemetry |
| `~/Projects/the-bounty-hunter/ops/park-disposition.mjs` | unpark/retire dispositions → telemetry |
| `~/Projects/the-bounty-hunter/ops/claim-check.mjs` | package validator (see `corpus/knowledge/claim-gates.md`) |
| `~/Projects/the-bounty-hunter/ops/claim-index.mjs` | operator queue generator |
| `~/Projects/the-bounty-hunter/ops/prepare-claims.mjs` | deterministic payload staging |
| `~/Projects/the-bounty-hunter/ops/finalize-all.mjs` | batch finalize |

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/ledger/; [lost-base] ~/Projects/the-bounty-hunter/ops/check-freshness.mjs, ops/rank.mjs, and dispatcher/ledger producers; round-13 corrections.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --selftest
