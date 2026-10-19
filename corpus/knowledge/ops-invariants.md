# Ops integrity layer — shared constants, validators, drill, sighting

Source: `~/Projects/bounties/ops/{shared,validate,registry-check,reroute-drill,
check-freshness,sighting,sighting-board,sighting-dispatcher,sighting-missions}.mjs|.sh`
all read in full; `fleets/registry.json` + `~/Projects/the-bounty-hunter/.omp/agents/` verified 2026-09-28.

These are the fail-closed invariants and the observation deck. None of them
hunt; they gate every mutation and prove the routing rules hold.

## `~/Projects/the-bounty-hunter/ops/shared.mjs` — the constants every other ops file imports

Single source of truth (header comment: "Never duplicate these constants in
another file"). Consumers: validate, registry-check, import-board,
reroute-drill, fleet-dispatch, park-disposition, finalize-all, check-freshness.

| Export | Value | Meaning |
|---|---|---|
| `BANNED` | `['cursor', 'opencode']` | provider tokens that may appear nowhere in registry lanes, config roles, or agent cards — scanned word-boundary `(^|[^a-z])tok([^a-z]|$)` case-insensitive |
| `PARKED` | `[]` | empty since the chatgpt park lifted 2026-09-04 (operator reset; gpt-6-astra probe OK). Empty list → the parked regex is `/(?!)/`, never matches — parked-provider checks are currently no-ops by construction |
| `K3_SEATS` | `['judge', 'planner']` | the only lanes allowed to route k3 |
| `K3_TOKEN` | `/kimi-code\/k3|kimi-k3|moonshot\/kimi-k3/i` | scanned against primary/bucket routes only, never notes |
| `TELEMETRY_EVENTS` | 8 names | the *registry* event kinds (lane_parked, lane_degraded, operator_decree, xask_dry, board_imported, binding_verified, reroute_drill, provenance_drift); runtime kinds are emitted by fleet-dispatch |
| `sha256File` | bytes→hex | returns `null` on absent path — callers must not confuse null with a digest |
| `gitMutationBlocker` | fail-closed preflight | refuses when rebase-merge/rebase-apply/MERGE_HEAD/CHERRY_PICK_HEAD exist (`ACTIVE_GIT_OPERATION`) or HEAD not on `main` (`HEAD_NOT_ON_MAIN`); used by finalize-all, fleet-dispatch commits, --sync |
| `appendLedger` | 3500-byte cap | see `corpus/knowledge/mission-ledger.md` |

## `~/Projects/the-bounty-hunter/ops/validate.mjs` — schema + referential gate (M1)

Runs three layers, one `ERROR <line>` each, exit 1 on any:

1. **Registry sanity**: every lane id collectable for reference checks.
2. **Config/card pins**: `~/Projects/the-bounty-hunter/.omp/config.yml` `modelRoles:` (2-space-indent regex
   `^\s{2}(\w+):\s*(\S+)$`) + `~/Projects/the-bounty-hunter/.omp/agents/` scanned for BANNED.
3. **Program records**: hand-rolled subset validator over
   `bounty-map/schema.json` — honors `type/required/properties/enum/pattern/
   additionalProperties:false/minLength/minimum/maximum`, `format:uri`
   (`^https?://`), `format:date-time` (strict RFC3339 regex — `Z` or
   `±HH:MM`, no bare offsets). Then two referential checks: `freshness.as_of`
   must be RFC3339, and `rec.lane` must be a lane id in `fleets/registry.json`.

`--strict <file>` narrows to one record and adds `ev_inputs` non-empty.
`programs/x.json` auto-prefixes to `bounty-map/`. This is a *subset* checker —
draft-07 features it doesn't implement (oneOf, $ref, dependencies) silently
pass. `~/Projects/the-bounty-hunter/bounty-map/schema.json`'s own `additionalProperties:false` is what makes the
subset enforceable.

## `~/Projects/the-bounty-hunter/ops/registry-check.mjs` — the deep lane bijection (M4)

Owns what validate.mjs doesn't — seven numbered checks, exit 1 per violation:

1. **Lane↔card bijection**: every non-k3 lane needs `~/Projects/the-bounty-hunter/.omp/agents/kx-<lane>.md`;
   every `kx-*.md` needs a lane (orphan detection via set-consumption).
   `mission_l1` is the documented exception — its "card" is
   `fleets/mission-template.md` because L1s spawn as separate omp sessions.
   Verified 2026-09-28: 10 lanes, 6 kx cards (connector/distiller/executor/
   labrat/reviewer/scout + security = kx-security), mission_l1 template —
   bijection holds.
2. **`@role` consistency**: each card's `model:` pin resolves through
   config.yml modelRoles to the lane's `primary`; literal pins compare direct.
3. **Bucket hygiene**: `judge` must have an empty bucket AND a note matching
   `/honest.halt/i` (I1 — honest-halt is designed, not a bug). Other lanes
   with empty buckets need a `/degrade/i` note acknowledging it.
4. **Parked placement**: PARKED providers may sit in buckets, never in
   `primary`. Currently vacuous (PARKED empty).
5. **Banned absence**: BANNED tokens in no lane route, no modelRole, no card.
6. **k3 confinement**: `K3_TOKEN` matches only judge/planner routes and
   `fleet_judge`/`fleet_planner` roles. Live: judge+planner primaries are
   `kimi-code/k3:high`.
7. **Grok effort pin**: any route containing `grok` must end `:low` exactly
   (last-colon split; no suffix = fail). Scout/labrat pin `grok-4.5:low` — OK.

**Live state (2026-09-28): FAIL — and the failure is in the checker, not
the fleet.** Exit 1 with seven `@role` errors on every kx card. Two
mechanics bugs: (a) card pins like `model: "@fleet_volume"` resolve one
hop through `modelRoles` to `"@ufo_deepseek_max"` — the resolved string
keeps its YAML double-quotes *and* the script never re-resolves the
nested `@` alias, so it compares `'"@ufo_deepseek_max"'` ≠ primary;
(b) pins resolving to `devin/swe-2:max` legitimately (frozen
2026-09-15 charter: reasoning seats on unmetered swe-2) still mismatch
the registry primaries. Consequence: the M4 deep-invariant gate is
continuously red → treated as noise → a real lane/card drift would land
invisibly. Cross-domain (`~/Projects/the-bounty-hunter/.omp/` + registry semantics) — reported, not
fixed here. `~/Projects/the-bounty-hunter/ops/validate.mjs` on the same day: `OK (1088 programs, 10 lanes,
0 errors)`.

## `~/Projects/the-bounty-hunter/ops/reroute-drill.mjs` — simulation-only identity proof (I6)

`node ops/reroute-drill.mjs --simulate park:<lane>` — the ONLY valid arg
shape; anything else exits 1. Walks the lane's `bucket` in order, takes the
first entry that is non-BANNED, non-PARKED, non-K3; degrades to literal
`'local'` on exhaustion. Never mutates `~/Projects/the-bounty-hunter/fleets/registry.json`, never spawns, never
networks — its one side effect is a `reroute_drill` telemetry line with
`simulated:true`, `from: primary`, `to: candidate`. Purpose: prove a lane's
identity survives a primary park without exercising real dispatch.

## `~/Projects/the-bounty-hunter/ops/check-freshness.mjs` — honest-alarm staleness (M5)

`node ops/check-freshness.mjs [--from <board-root>]` — board defaults to
`/home/vgpnk/Projects/origin-work/open-bug-bounties`. Requires [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
`~/Projects/origin-work/open-bug-bounties/data/refresh_evidence.json` (run_id + attempted_at_utc) and all three [r22 correction: origin-work base absent since 2026-10-12; test -e failed 2026-10-19; historical]
datasets; missing/malformed → `freshness: ERROR`, exit 1.

Per dataset: timestamp = `last_permitted_check_at_utc ??
last_attempted_check_at_utc ?? snapshot_at_utc` (preference order matters —
a permitted-check beats an attempt). `source_checks` entries carrying a
`live` substring mark the dataset **live-mode**. Verdict: `FRESH` ≤ **26 h**
else `STALE` (26 = 12 h board cron + slack). Exit 1 only when a **live-mode**
source is stale — "honest alarm, AR4"; retained/permission-limited staleness
is reported but doesn't fail. Emits `freshness_check` telemetry every run
(fresh/stale/live_stale/exit).

## Sighting scripts — observation, not authority

`ops/sighting.sh` (default `open`, `close` to tear down) builds four managed
windows in the `ufo_sighting` tmux session — `fleet` (watch sighting-board),
`ledger` (`tail -f telemetry.jsonl`), `missions` (`tail -f fleets/run/*.log`),
`dispatcher` (sighting-dispatcher loop). It kills ONLY the four managed
windows, never the session — mission L1 panes live in the same session and
are untouchable.

- `~/Projects/the-bounty-hunter/ops/sighting-board.sh`: one frame = jq table of `fleets/run/*.status.json` [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]
  (program/state/detail) + `git -C claims log --oneline -8` + lease expiry
  list + telemetry tail. Caveat: `git -C claims` resolves to the parent repo
  (claims/ has no `.git`), so the "claims commits" pane shows repo log —
  right data, historical label.
- `~/Projects/the-bounty-hunter/ops/sighting-dispatcher.sh`: 10 s loop — `pgrep -af fleet-dispatch` (prints [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]
  the restart command when dead), last 5 `dispatcher_tick`, last 8
  `mission_dispatched`.
- `~/Projects/the-bounty-hunter/ops/sighting-missions.sh`: 6 s loop of `tmux capture-pane` frames over every [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]
  non-managed window — the rendered-TUI view. Preferred over the missions
  window when the fleet is idle: `tail -f fleets/run/*.log` matches nothing
  once logs are rotated to `.log.gz` (observed: 0 uncompressed `.log`,
  537 `.log.gz`), so the tail window shows a dead glob.

Display-only: authority stays with `~/Projects/the-bounty-hunter/ops/fleet-dispatch.mjs` + the L1 panes. [r22 correction: the-bounty-hunter base absent since ~2026-10-12; test -e failed 2026-10-19; historical how-to, not runnable]

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/ops/{shared,validate,registry-check,reroute-drill,check-freshness,sighting,sighting-board,sighting-dispatcher,sighting-missions}.mjs/.sh; [lost-base] ~/Projects/the-bounty-hunter/.omp/agents/.
verified-at: 2026-09-28
recheck: on-restoration — test -d ~/Projects/bounties && test -d ~/Projects/the-bounty-hunter && python3 corpus/instruments/anchorcheck.py corpus/knowledge/ops-invariants.md (fails closed today: base absent since 2026-09-28; not re-verifiable; re-scope is L0 kasegi round-15)
