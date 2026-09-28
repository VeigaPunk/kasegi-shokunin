# kasegi-shokunin — Iteration Log

- 2026-09-28 — round 0: minted as shonen.
- 2026-09-28 — round 1: rewrote SKILL.md from a seed stub into grounded craft.
  Evidence walked: `/home/vgpnk/Projects/bounties` — 275 claim dirs under
  `claims/`, 1088 `bounty-map/programs/*.json` records, `docs/claim-runbook.md`
  (operator-gated submission contract), `docs/claim-ready-index.md` (12-item
  queue + blocked gates), `docs/continuation-notes.md` (486-mission partition:
  438 LEARNED honest-zero, 19 RETIRED auth-walled, 26 FAILED-infra, 3
  RETRY-method), `docs/wrap-report.md` (7 packages, 0 clean GO — all
  disclosure-class fixes), `docs/review-verdicts.jsonl` (430 leave / 50
  continue / 6 drop), `docs/autopsies/` (auth-wall/terms-gate retirements),
  `fleets/mission-template.md` (AR14 standing grant + six-file package spec),
  `ops/ev-report.mjs` (fail-closed adjusted-EV formula), exemplar packages
  `claims/cantina-pendle/ingestion-20260915/` (positive-blocked) and
  `claims/bugcrowd-seek/honest-zero/` (terminal honest-zero). New SKILL.md
  carries: pipeline, scope-snapshot checklist, per-platform policy playbook,
  finding-triage decision table, evidence-package anatomy with status.json
  gate semantics, 10 observed disclosure anti-patterns, EV model, cited paths.
  Corpus added per `../CORPUS.md`: `corpus/README.md` index + coverage map,
  `corpus/knowledge/` (claim-package-contract, policy-access-playbook,
  ev-model, terminal-classes, program-quirks — all sourced),
  `corpus/lessons/round-1.md` (what worked/friction/gaps).
- 2026-09-28 — round 3: closed the gate-list gap and walked the VDP corpus.
  Read `ops/claim-check.mjs` (full 233 lines), `ops/claim-index.mjs`,
  `ops/prepare-claims.mjs` → `corpus/knowledge/claim-gates.md` (complete gate
  inventory: file presence, content markers, manifest/redaction binding,
  custodian 3-way head binding, secrets regex, status.json gates incl. the
  GLOBAL duplicate-submission scan and literal `kx-reviewer` role check;
  index error-ranking and payload immutability semantics). Walked
  `vdp-disclosures/anthropic-plugin-dev-cmd-injection/` →
  `corpus/knowledge/vdp-disclosure-packages.md` (4-file shape: ROUTE.md /
  cover-note.md / report.md / SUBMITTED.md; free + attributed decree;
  security.txt Contact → H1 embedded_submissions route; operator sends
  personally). Sampled 5 Cantina sibling ingestions → `program-quirks.md`
  (only dydx repeats positive-blocked-live-precondition; $100 fee is
  Pendle-specific so far). SKILL.md gained the enforced-gate summary + VDP
  sibling-format section. `corpus/lessons/round-3.md` recorded.
- 2026-09-28 — round 4: closed the ledger + evidence-store gaps. Censused
  `ledger/missions.jsonl` (718 lines, 260 missions, 218 programs; dominant
  path SCOPED→PLANNED→LEARNED ×207; SUBMITTED ×3 operator-attributed),
  `telemetry.jsonl` (7218 lines, ~30 event kinds, dispatcher_tick 3680),
  `candidates.jsonl` (8 the-bounty-hunter intake records, b1k-NNN run_ids),
  `imports.jsonl` (evidence_id-bound board imports) →
  `corpus/knowledge/mission-ledger.md` (transition census, appendLedger
  3500-byte O_APPEND cap, gitMutationBlocker, rank.mjs rankings artifacts,
  14-tool ops inventory). Censused `evidence/` (592 program dirs:
  scope-snapshot 583, authorization-envelope 580, honest-zero-record 346;
  raw/ 244, history/ 154, custodian/ 27, b1k-NNN per-run dirs) →
  `corpus/knowledge/evidence-dir.md` (vs claims/*/*/evidence/ contract,
  honest-zero/v1 schema). `vgn-bounty-lab/` confirmed empty `git init`
  (zero commits) — gap closed as nothing-to-learn. `george/` (49G comma.ai
  research dir) has zero claims/ references — parked. SKILL.md gained the
  Mission ledger & audit store section + cited paths.
- 2026-09-28 — round 5: closed the mission-control-plane gap. Read
  `ops/fleet-dispatch.mjs` in full (427 lines) → dispatcher loop
  (queue-score weights, 2 h leases, tmux pane rotation, reconcile-from-
  leases, sole-committer + tag/byte-proof + atomic push, dual-method
  UTC-3 model windows, strict 429-limit detection → grok lane,
  `--sync` SYNC_PATHS allowlist). Censused `fleets/` runtime:
  `missions/` 584 generated L1 assignments (0 without status),
  `run/` 703 status files (PARKED 646, DONE 27 — 13 with claims/
  deliverable — SCOPING 20, RETIRED 6, BLOCKED 2, HUNTING/WRAPPING 2;
  `_`-prefixed seat statuses incl. `_claimer`/`_review-orchestrator`/
  `_b1k-*`), 537 log.gz, `leases.json` 3030 lines, `priority.json`,
  `state-snapshots/` + `docs/RUNBOOK-resume.md` resume procedure.
  Read sibling L1 contracts (`claimer-mission.md` — CDP submissions with
  submitted-record status; `review-mission.md` — 486 drop/continue/leave)
  and audit lanes (`.ufo-mission-report-bh*` 21 readiness audits all
  BLOCKED, `.ufo-warden/` dispatch ledger, `.ufo-ingestion/` claim-ready
  tracker over the origin-work tree) → `corpus/knowledge/mission-control.md`.
  SKILL.md gained Mission control plane section + cited paths.
  `corpus/lessons/round-5.md` recorded.
- 2026-09-28 — round 6: closed the retirement-lane gap. Read
  `ops/park-disposition.mjs` in full (80 lines): dry-run-by-default
  PARKED/FAILED dispositor, first-match regex chain over
  `status.json.detail` (HONEST→LEARNED no-op, H1SPA→RETRY_METHOD,
  AUTH→RETIRE_AUTH, TRANSIENT→RETRY_TRANSIENT, else REVIEW no-op);
  --apply un-parks retries via status-file `rm` + `mission_unparked`
  telemetry, and produces the fixed five-part `docs/autopsies/<id>.md`
  + RETIRED status rewrite + `mission_retired` event. Censused all 31
  autopsies: auth-walled SPA ×27, terms-gate ×1 (SIX), privacy hard
  stop ×1 (Airtable), paused/non-enumerable ×2; generated "Why"
  boilerplate mis-describes non-login sub-causes — Reason (verbatim)
  is authoritative. Re-ran the exact classifier live over
  `fleets/run/` (703 statuses): LEARNED 529 / REVIEW 85 / RETIRE_AUTH
  30 / RETRY 2 — the 85 REVIEW are the same auth-wall class in newer
  wording ("no exact in-scope assets", "active-testing grant",
  "custodian HARD_STOP") the regex misses: parked invisibly, never
  retired. → `corpus/knowledge/retirement-autopsies.md` (producer
  mechanics, schema, sub-cause partition, regex-drift rule: embed a
  literal AUTH keyword in `detail` when parking). SKILL.md gained the
  Retirement lane section, corrected `docs/autopsies/` count 30→31,
  + park-disposition cited path. `corpus/lessons/round-6.md` recorded.

  `corpus/lessons/round-4.md` recorded.

- 2026-09-28 — round 7: closed the ops-tail gap — the last name-only
  surface. Read all six undocumented `ops/` scripts in full plus the four
  `sighting*.sh` wrappers and `shared.mjs` constants: `validate.mjs`
  (schema-subset checker + lane referential + strict RFC3339 as_of +
  `--strict` ev_inputs gate), `registry-check.mjs` (7 checks: lane↔kx-card
  bijection w/ mission_l1→mission-template.md exception, @role→primary
  resolution via config.yml, judge empty-bucket+honest.halt note, parked/
  banned/k3-confinement/grok-`:low` pins — verified live: 10 lanes, bijection
  holds), `reroute-drill.mjs` (simulation-only `park:<lane>` → first clean
  bucket entry or `local`, `reroute_drill` telemetry, zero mutation),
  `check-freshness.mjs` (26 h threshold; exit 1 only when a *live-mode*
  source is stale — honest alarm AR4), `import-board.mjs` (pre-write
  binding: dataset sha256+count+refresh_run_id vs refresh_evidence;
  `--verify-binding` checks ledger tail; independent dataset alone filters
  active+public+confirmed_cash+high; per-source live/retained/stale labels;
  protected past-DISCOVERED files never edited but S4 provenance drift →
  telemetry; two-phase write, conflict exit-1; new records land
  lane=executor/DISCOVERED), `finalize-all.mjs` (batch claim sweep:
  DONE-filter → claim-check → commit → byte-proof → `claim-ready/` tag,
  sha-conflict never rewrites → `claim_tag_conflict`; index regen + single
  `--atomic` push; `gitMutationBlocker` preflight+pre-push). `shared.mjs`
  constants recorded: BANNED=[cursor,opencode], PARKED=[] (park lifted
  2026-09-04 → parked checks vacuous), K3_SEATS=[judge,planner].
  Sighting finding: `sighting.sh` missions window tails `fleets/run/*.log`
  which dead-globs post-rotation (0 uncompressed, 537 `.log.gz`);
  `sighting-missions.sh` capture-pane frames are the correct live view.
  → `corpus/knowledge/ops-invariants.md` + `corpus/knowledge/intake-and-
  finalize.md`; SKILL.md gained Ops integrity layer section + 3 cited
  paths; README coverage map + gap marked closed. Live re-run:
  `node ops/registry-check.mjs` exits 1 with 7 `@role` mismatches —
  checker-side bugs (nested `@` aliases not re-resolved, YAML quotes kept
  in resolved values, frozen swe-2 charter pins mismatch primaries), so the
  M4 gate is permanently red; cross-domain, reported not fixed.
  `node ops/validate.mjs` → `OK (1088 programs, 10 lanes, 0 errors)`.
  `corpus/lessons/round-7.md` recorded.

- 2026-09-28 — round 8: closed the archive gap — `fleets/ufo-archive-2026/`,
  the last named known-gap and the richest unread artifact class. Read all
  19 `missions/claim-*/report.json` (2026-09-14 hardening wave over real
  `claims/` packages) plus every sibling dir →
  `corpus/knowledge/ufo-archive-2026.md`: 22-class defect taxonomy that is
  the empirical superset of `claim-check.mjs` (custodian-head mis-binding,
  stale vs missing redaction receipts, status.json field absence,
  missing `submission-draft.md` as the dominant defect, stale packet
  drafts materially wrong, receipt-drift duplicate-submission hazards,
  "verified"-never-executed claims, citation drift, alias-status drift,
  proven-but-not-claimable gamma-deposit class, falsified-by-execution
  elastic exclusion notice); outcome vocabulary (REFINED→DONE / HOLD /
  NOT-SUBMITTABLE / reconcile-only / stop-frontier-saturated;
  `no_submission_performed` is the norm). Provenance resolved:
  `bounty-keeper/keeper.mjs` is the `b1k-NNN` run_id producer
  (265 launched, halted `night_budget`) that `ledger/candidates.jsonl`
  and `evidence/*/b1k-NNN/` reference; archive `claim-packages/*` paths
  are the pre-rename tree (now `claims/<platform>-<program>/<slug>/`,
  verified live). Reconciliation chain recorded: `fleets/run/portal-
  reconciliation-2026-09-11.json` + `.ufo/claim-recovery/final-audit.json`
  + `ledger/candidates.jsonl` do-not-re-hunt + `ledger/missions.jsonl`
  SUBMITTED. SKILL.md gained the "Claim-hardening wave" defect-class
  section + cited path; README coverage map + gap marked closed.
  `corpus/lessons/round-8.md` recorded.
- 2026-09-28 — round 9: closed the submitted-state gap — the do-not-refile
  set was scattered across six stores with no consolidated list, and the
  archive taxonomy named receipts (4028846, a169f309) absent from `claims/`.
  Live-censused all 280 `claims/*/*/status.json` for submission fields:
  only airtable/spotify/mozilla carry real `submitted_url`/`submitted_at`/
  `submission_state:"SUBMITTED"` + `submit/receipt.md`; ledger
  `missions.jsonl` SUBMITTED rows and `portal-reconciliation-2026-09-11.json`
  agree (mozilla+spotify closed_duplicate, airtable not_established);
  `final-audit.json` pins the same three preexisting reports. Recovered
  three archive-era filings (H1 4028846 k8s-nodebound, Bugcrowd a169f309
  ld-node-stream, e4f41218 mattermost) plus three probable-unverified
  receipts (H1 4028904/4028953 elastic, Bugcrowd 4ecbaf46 aiven —
  login-wall, do-not-refile/do-not-delete). **Live hazard surfaced:**
  queued row 4 `hackerone-anthropic/plugin-dev-test-hook-command-injection`
  (DONE+claimable) is the identical finding (same commit/file/sha256/CWE-78)
  already freely disclosed as `vdp-disclosures/anthropic-plugin-dev-cmd-
  injection/` — the duplicate scan reads only `claims/`; reported upstream,
  not fixed (cross-domain). Field traps recorded: `submission_performed`
  ≠ receipt truth, `submission_url` ≠ `submitted_url`. Aliases are
  machine-readable when used (`duplicate_of` + `submission_state:
  DUPLICATE_OF_SUBMITTED` on hackerone-mozilla; `claim.json alias_of`
  unused repo-wide). L2 sweep found new stores: the `submission-review/`
  receipt tree lives under `~/Projects/origin-work/open-bug-bounties/
  claim-packages/` (submission-receipts.csv 3 rows + 3 orphan receipts =
  the probable set), `_claimer.status.json` submitted[]/disclosed[]
  arrays, `.ufo/bounty-fleet/reports/claim-claim-*.md` reconciles.
  Hygiene: 295 claim dirs, 15 status-less (13 ingestion-seeded stubs +
  stiltsoft partial + t-mobile BLOCKED.md); root zips dated snapshots.
  → `corpus/knowledge/submitted-registry.md`; SKILL.md gained the
  registry section; README gap closed. `corpus/lessons/round-9.md`
  recorded.
- 2026-09-28 — round 10: closed the operator-queue gap — the 12-row
  `docs/claim-ready-index.md` queue had never been audited as a set, and
  round 9 had flagged row 4 without verifying the fingerprint or the
  queue-path defect. Live `claim-check.mjs` re-run on all 12 rows: all OK.
  Source read of `ops/claim-index.mjs` (full file): `claim-hold/*` tags are
  never consumed — the index only lists `claim-ready/*` — so three held
  packages queue anyway (anthropic, wordpress, intel). Row-4 fingerprint
  byte-matched against `vdp-disclosures/anthropic-plugin-dev-cmd-injection/`:
  same commit `d7dbd9a09f59775726ed14bbea8fc9dfdff62f7b`, same file
  `plugins/plugin-dev/skills/hook-development/scripts/test-hook.sh`, same
  captured-source sha256 `ded642e811b4…f0069393`, CWE-78 — verified
  duplicate of the operator's own 2026-09-06 disclosure; do not file.
  `submitted_url` on 9/12 queued rows is a route URL, never a `/reports/`
  receipt — queue membership = never submitted. Per-row residual gates
  extracted from each `claim_checklist.md`: personio takeover proof REQUIRED
  by program OOS (spacex same class, "recommended"); intel
  `submit/BLOCKED-2026-09-11.md` still live (no authed Intigriti session);
  wordpress `submit/channel-block-20260911.md` = historical no-session
  blocker; 8x8 asset `eligible_for_bounty=false` (index flags "No payout
  claim"); mutable-precondition re-verify gates on spacex/amazonvrp/x/
  beanstalk/yahoo. Runbook operator-only steps distilled. Both queue-path
  defects are cross-domain (bounties owner) — reported, not fixed.
  → `corpus/knowledge/operator-queue.md`; SKILL.md gained "Operator queue —
  live audit" section; README coverage map + gap closed.
  `corpus/lessons/round-10.md` recorded.
