# Mission control plane — `fleets/` runtime + audit lanes

Source: `~/Projects/bounties/ops/fleet-dispatch.mjs` (read in full, 427
lines), `fleets/missions/*.md`, `fleets/run/*`, `fleets/leases.json`,
`fleets/{claimer-mission,review-mission}.md`, `fleets/priority.json`,
`fleets/state-snapshots/`, `ops/sighting*.sh`, `docs/RUNBOOK-resume.md`,
`.ufo-mission-report-bh*.md`, `.ufo-ingestion/`, `.ufo-warden/`.
Counted 2026-09-28.

This is the layer between program records and claim packages: who runs, on
what model, with what lease, and how the result reaches `claims/` and git.

## The dispatcher loop — `ops/fleet-dispatch.mjs`

A tmux-native `/loop` engine over `ufo_sighting:fleet-grid` panes. One tick =
window-flip check → `detectLimit()` → `sweep()` → `periodicSync()` → launch
until `active.size == --max` → `dispatcher_tick` telemetry → 30 s sleep.

- **Queue score** (`buildQueue`): `priority` set +9e12 (`fleets/priority.json`),
  `continue` verdicts +2e12, `curated` EV inputs +1e12, `reward.min*1000`,
  `freshness.live` +1. `DONE` never redispatches; live leases and
  mission-file presence filter the candidate set. EV is ordering, never a
  gate (AR12 — negative-EV dispatches carry an `ev_note`).
- **Lease**: `fleets/leases.json`, `{program_id, mission_id, leased_at,
  expires_at}`; 2 h expiry (3030 lines — includes expired history and
  b1k-seat leases carrying `lease_holder`, `asset`, `official_url`,
  policy hashes). `reconcile()` on restart rebuilds the active map from
  live leases + tmux pane titles — dispatcher stop/start is safe.
- **Launch**: writes `{state:"SCOPING"}` status first, then lease, then
  `tmux split-window` pane titled with the program id running the L1
  (`omp` CLI against `fleets/missions/<id>.md`).
- **Sweep** (terminal states PARKED/DONE/RETIRED/FAILED): `DONE` +
  `deliverable` → `commitClaims` + `finalizePush` + `mission_done`; else
  `mission_parked`/`mission_failed`. Pane killed, lease deleted, slot
  rotates. Pane dead + lease alive + no terminal status → writes
  `{state:"FAILED", detail:"pane exited"}` — budget still counts it.
- **P20/P21**: dispatcher is the sole committer to `claims/`; every commit
  gated on a fresh `ops/claim-check.mjs` run (red = `claim_rejected`
  telemetry, not committed). Commit message:
  `claim(<id>): <verdict> — <title> [mission:… evidence:<12-char>]`.
  Post-commit it verifies a commit actually contains the package bytes and
  that `git diff <sha> -- <rel>` is clean — byte proof, not trust.
- **`finalizePush`** (operator decree 2026-09-04): every accepted package
  gets annotated tag `claim-ready/<id>/<slug>` (`-m` carries bounty value +
  claim URL + manifest prefix). Re-checks claim-check, re-proves the tag
  sha matches accepted bytes (`claim_tag_rejected`/`claim_tag_conflict`
  telemetry on mismatch), then one atomic `git push origin main` + tags
  (`claims_pushed`). All git mutations fail-closed through
  `gitMutationBlocker`.
- **Model routing** (decree 2026-09-04, fixed UTC-3): Beijing off-peak
  12:00–22:00 → `alibaba-token-plan/deepseek-v4-pro:max`; peak →
  `openai-oauth/gpt-6-astra:max`. Applies to NEW launches only — running
  missions keep their pin (contract freeze). Window flip resets the limit
  fallback. An A/B/C `--models-rr a,b,c --rr-until <epochMs>` experiment
  mode exists (telemetry `experiment: l1-model-abc`).
- **`detectLimit()`**: tails `fleets/run/*.log` modified <15 min; strict
  signatures (`usage limit has been reached`, `rate limit exceeded`,
  `429 Too Many`) ANDed with a model-family regex — the TUI status bar
  prints untracked-file counts like `?429`, so a bare 429 regex
  false-positives. On hit: new launches pin `xai-oauth/grok-4.6:low`,
  `model_reroute` telemetry names the evidence file.
- **`--sync` periodicSync**: every 10 ticks commits+push a fixed
  `SYNC_PATHS` allowlist (claims/README, evidence, ledger, docs, ops,
  fleets/missions, registry, mission-template). Never stages claim
  packages, never mutates off `main`; `fleets/run/` is untracked by design.

## `fleets/missions/<program>.md` — 584 generated L1 assignments

Per-program instantiation of `mission-template.md`, not the template
itself. Every file = Godspeed prefix + `# MISSION L1 — <name>` +
authoritative `Program record`/`Program id`/`Official policy URL` +
AR14 standing grant + fleet-learned policy playbook + NEVER list + lane
model pins + six-file deliverable contract + report-back protocol.
All 584 `the-bounty-hunter` contract; all 584 have a status file
(missions w/o status: 0). `fleets/missions/` is inside `SYNC_PATHS` —
assignments are versioned, runtime is not.

## `fleets/run/` — file-protocol backchannel (703 status + 537 log.gz)

`<program>.status.json` is the L1→dispatcher heartbeat, written by the
mission itself: `{program, state, detail, deliverable, updated_at}` with
optional evidence fields (`scope_snapshot`, `content_sha256`,
`manifest_sha256`, `finding_count`, `verdict`, `no_submission_performed`…).
Observed state census (703 files, 0 parse errors):

| state | n | meaning |
|---|---|---|
| PARKED | 646 | terminal honest-zero/auth-wall (mirrors LEARNED) |
| DONE | 27 | terminal; 13 carry a `claims/` deliverable, 14 DONE-honest-zero |
| SCOPING | 20 | frozen mid-flight — dispatcher stopped before terminal write |
| RETIRED | 6 | auth-wall/terms-gate, autopsy in `docs/autopsies/` |
| BLOCKED | 2 | seat-level blockers |
| HUNTING/WRAPPING | 2 | frozen mid-flight |

`_`-prefixed statuses are seats, not missions: `_claimer`,
`_review-orchestrator`, `_b1k-134/-148/-157` (hunter runs, `program:null`,
`detail` like `no-claimable-work; leases_held=0`). 119 statuses have no
mission file — b1k seats and programs dispatched before per-program
assignment generation.

`*.log.gz` (537) = gzipped mission TUI pipes; `sighting-missions.sh`
renders live panes via `capture-pane` instead — raw streams are for
post-mortem, rendered frames for watching.

`fleets/state-snapshots/2026-09-05-pre-model-adjust.json` freezes
`{statuses{fname→bytes}, leases}`; `docs/RUNBOOK-resume.md` restores
statuses + leases then relaunches the dispatcher — queue rebuilds from
bounty-map + statuses.

## Sibling L1 contracts

- **`fleets/claimer-mission.md`** — the external-effect lane: operator-
  authenticated burnerchrome at CDP 9222 (attach by URL substring, never
  steal his tab). Submission queue with per-package field plan; severity at
  FULL supported strength (decree 2026-09-05 — strip hedging where evidence
  supports it); any form rejection/captcha → STOP verbatim, never
  improvise. Its `_claimer.status.json` shows the doctrine field and the
  submitted record: mozilla/spotify/airtable got H1 report URLs;
  intel BLOCKED on Intigriti ID-verification; 3cx HELD on operator gate;
  anthropic disclosed free via VDP.
- **`fleets/review-mission.md`** — review orchestrator: daybreak L1 judges
  every non-claim-ready item drop/continue/leave into
  `docs/review-verdicts.jsonl`; lanes pin `gpt-5.6-luna:low`/`grok-4.5:low`/
  `kimi-k2.7-code:high` by cost class. `_review-orchestrator.status.json`:
  `covered: 486`, drop 6 / continue 50 / leave 430.

## Sighting surface — `ops/sighting*.sh`

`ufo_sighting` tmux session, four managed windows (fleet/ledger/missions/
dispatcher) + per-mission panes that the scripts never kill. Board =
jq over `fleets/run/*.status.json` + claims/ git log + leases + telemetry
tail. Sighting windows are display only — authority stays with dispatcher
+ L1s.

## Audit lanes (2nd-generation hunter, 2026-09-14/15)

- **`.ufo-mission-report-bh<hex>.md`** — 22 root-level UFO-FSD mission
  reports; claim-package readiness audits: 20 BLOCKED, **2 READY**
  (`bh0cb2eb6ca20b` intigriti-yahoo, `bh557fda669b20` hackerone-superhuman,
  both claim-check OK) — round-12 correction of round 5's "21, all BLOCKED".
  Flavors: honest-zero-*, `placeholder shell, dispatched in error` (warden
  filter bug, fixed 2026-09-14), participation-gated (Monzo needed own
  UK/EU KYC account — deepest hunt: signature-verified APK acquisition +
  smali-level deeplink trace, recorded as residual lead not-a-finding).
  Reports carry per-artifact sha256; the `.ufo/<runId>/` evidence-dir join
  fails for ≥8/22 (25 workspaces vs 22 reports, two disjoint roots —
  see `ufo-workspaces.md`).
- **`.ufo-warden/`** — readiness dispatcher: `state.json` maps
  program→{runId, findings[], done, doneVia:"tick/handoff-present"};
  `warden.log` = TICK backlog/deadline/present/COMPLETE events.
- **`.ufo-ingestion/`** — intake cycle artifacts: `cycle-<ts>.md` (16
  scout seats per cycle; the 20260914 cycle rerouted all 16 same-identity
  onto devin/swe-2:max after a fleet-wide 403 spending-limit on
  grok-4.5:low — reroutes logged in `reroutes.log`), EV-ranked
  SEEDED/DEFERRED table, `claim-ready-tracker.{json,md}` (~5 min refresh
  tracking `origin-work/open-bug-bounties/claim-packages/` — a DIFFERENT
  tree; READY.md=claimable, BLOCKED.md disqualifies),
  `claim-ready-ledger.json` schema `bounty-hunter-claim-ready-v1`
  (inherited vs this_run accounting; 25 packages / $13,833 expected).
