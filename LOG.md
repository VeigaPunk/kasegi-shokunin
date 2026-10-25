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
- 2026-09-28 — round 11: closed the intake-surface + registry gaps — the
  last open known-gap and the largest unread structured dataset. Censused
  all 1088 `bounty-map/programs/*.json` (single `refresh_run_id`
  `refresh-20260829T190850329Z`, 30 days stale): `mission_state` is
  DISCOVERED×1087/PLANNED×1 and never advanced — `fleet-dispatch.mjs::
  programState()` reads it only for a `--dry` log line; `lane`=
  executor×1088; `ev_inputs` non-empty×1 (github-bug-bounty curated M2);
  `reward` on 48 independent records only → `buildQueue` degenerates to
  priority(9e12)/continue(2e12)/curated(1e12)/reward.min×1000 for ~1040
  zero-scored records. Coverage join: 586/592 evidence dirs mapped,
  252/275 claims dirs mapped, 352 map programs untouched, 22 map-less
  claims dirs = the `.ufo-ingestion/` cycle (2026-09-14, 16 scouts,
  grok 403 → devin/swe-2:max reroute; EV-ranked 32, seeded 13 → 7 of 12
  queue rows) bypasses the map entirely; name-drift pairs (spacex,
  github-bounty) break id joins. Live verify: `check-freshness` exit 1
  (358 h vs 26 h, standing AR4), `validate` OK. `.ufo-ingestion/
  claim-tracker.py` = dead third watcher (READY.md standard, weaker than
  claim-check; also scans origin-work claim-packages; last run
  2026-09-14T20:40Z). `fleets/registry.json` resolved in-domain: the
  `operator_decrees` block is the authoritative decree ledger — filing
  order mozilla→spotify→airtable→intel, **3cx never-filed decree**
  (free disclosure pending rep, explains rounds 9–10 anomaly), intel
  hold, freebie-class ATTRIBUTED supersedes anonymous, paid-track
  accounts vgpnk1337/veigapunk, severity-evidence-trail; astra is
  simultaneously doctrine-banned and LIVE-routed (in-place superseded
  markers, stale parked notes). → `corpus/knowledge/intake-surface.md`;
  SKILL.md gained Intake surface section + 3 cited paths; README coverage
  map + registry gap CLOSED. `corpus/lessons/round-11.md` recorded.
- 2026-09-28 — round 12: closed the `.ufo/` runtime-layer gap — the last
  un-censused surface class (round-11 residual) — and repaired the corpus's
  first measured citation audit. Created `SCORECARD.md` (coverage proxy
  13/18→18/18 top-level surfaces; axis move: coverage 7→9). Fan: 10 L2s in
  one batch (4 scouts per surface, 2 executors incl. skeleton/drafter, 2
  critics falsifying rounds 9–11, connector sibling-overlap matrix, reviewer
  citation audit). Walked: `.ufo/bh*` ×19 + 6 nested (warden-dispatched
  readiness-audit workspaces; 25 vs 22 reports = 19 shared/3 report-only/6
  workspace-only/1 phantom; `reroutes.jsonl` 121 records all grok/xai
  403/429 → `devin/swe-2:max`; state.json program-keyed runId overwrites;
  yahoo READY provenance split bh7609023286b0↔bh0cb2eb6ca20b),
  `.ufo/bounty-fleet/` 805M (bounty-keeper tree per `keeper.mjs:48-63`;
  second `missions.jsonl` 525 rows/184 run_ids; 265 launched/249 reported/184
  ledgered → 81 unledgered; two halts launch_cap@64+night_budget; b1k-248+251-265
  silent truncation; `report.md` vs `reports/`, `session/` vs `sessions/`
  traps), `.ufo/sessions/` (exactly 8 bpolish seats — "248 entries" falsified;
  omp recorder v3, 2026-09-15; refile verdict NONE, `submitted_url` all null;
  `no_submission_performed:true` → 471-false-positive grep trap),
  `.ufo/grok-bounty-assessment-20260911/` (historical, zero live consumers;
  scorer extracted in full — NA-exclusion + gcd-fold; 88.30/100 descriptive +
  gate BLOCKED, `clean_repository_closure` fail×266 unpassable by
  construction; self-invalidating — frozen scorer re-run fails today because
  `validate-review-output.mjs:58` re-reads live line ranges),
  `.ufo/claim-recovery/` (final-audit pins corroborate round 9 but are
  superseded in place by the gamma package's 09-14 readiness-audit), `.omp/`
  (second routing truth: uncommitted config.yml rewrites all six `fleet_*`
  roles; registry-check RED 7 violations; 4 non-registry cards invisible to
  every check; skills/ufo drifted fork), root `README.md` ("9 lanes" stale=10,
  describes git HEAD not live router) + `.gitignore` (asymmetric,
  load-bearing) + `pendle-core-v2-public/` (63M shallow clone `f242659`=v6.10.0,
  pin-bound; 187/255 provenance.json carry pins; claim-check never validates
  them). **Live-infra hazard surfaced + escalated to L0:** repo stalled
  mid-interactive-rebase since before 2026-09-11 (detached 58acb6d8, 0
  commands left, autostash), gitMutationBlocker fail-closes → no fleet
  commit/tag/push; 903 dirty entries; all Sep 7–15 work working-tree-only;
  claims/ 198 tracked files vs 3361 on disk (20/274 dirs); 49G george/ + 1.5G
  .ufo/ untracked AND un-ignored (`git add -A` ingestion risk); all 12 tags
  pushed; `claim-ship` = merged ancestor with superseded `claim-ready:`
  messages. 656 claims files cite `.ufo/` paths; 51/543 JSON refs already
  dangling; no gate resolves them → copy-bytes rule. Citation audit (74
  checked): 64 OK/9 mismatch/1 broken — all 10 repaired (bh audits "21 all
  BLOCKED"→22: 20 BLOCKED/2 READY superhuman+yahoo; claims denominator
  275→274 program dirs, 295 packages; archive missions 19→20; histogram
  BLOCKED 16→15 + OPERATOR_GATED nested-not-top-level; duplicate_of targets
  3892215 only, 3721615 is portal-reconciliation-only; "only ops writers"
  false — rank.mjs:203 + 4 others; wordpress redaction-receipt path; tracker
  24/24 origin-tree + log-end 17:24:52Z; telemetry as-of dated). Round-9 LOG
  wording "+ submit/receipt.md" for all three submitted packages was critic-
  falsified (only mozilla has one) — the registry table itself was already
  correct; LOG history not rewritten. New corpus:
  `knowledge/ufo-workspaces.md`, `knowledge/repo-git-state.md`,
  `knowledge/target-checkouts.md`; SKILL.md gained "UFO runtime workspaces"
  section + 8 cited paths; README coverage map + 3 gaps CLOSED.
  `corpus/lessons/round-12.md` recorded.
- 2026-09-28 — round 13: depth axis-move — the full-set citation re-audit +
  three-way threshold re-derivation planned at r12, executed as the lane's
  largest audit fan (10 L2s in one batch: 2 reviewers, 2 critics, sentinel,
  2 scouts, connector, executor-drafter, revenger; 7 returned usable audits).
  First order: committed round-12's artifacts LATE in both repos (r12 ended
  without its commit+push; kasegi fc6d398, main-repo report 5309290).
  **Measured: depth 8→9.** Citation layer: 1100 backticked tokens extracted
  from SKILL.md + 20 corpus entries; the assigned reviewer degraded and
  failed (fabricated "108 modules" totals — rejected; its citations.json +
  extraction scripts were kept and L1 finished the audit deterministically,
  `/tmp/kasegi-r13/classify{2,3,4,5}.py` with in-file rules): **708 counted
  citations, 705 resolved = 99.6%** (anchored-only 438/441 = 99.3%) vs r12's
  86.5% on a 74-citation sample. 3 truly broken, repaired: evidence-dir
  `raw-rN/` → real naming is `raw/` (244 dirs); submitted-registry
  `B-bounty-fleet/` layout is in the ALL-zip (469 members) only, not the
  468-file `claim-ready-packages` zip (numbered top-level dirs);
  ufo-workspaces `ufo-fsd-alpha/.ufo/missions/hunt-*` dangles — no
  `missions/` dir exists in that tree, the label survives only in transcript
  text. Fact layer (~106 atomic checks across 5 auditors + L1 source reads):
  ~30 defects found, ALL repaired in place ("round-13 correction/addition"
  markers; full enumeration in `corpus/README.md` Known-gaps). Headlines:
  reroute universals → distributions (23/121 non-grok causes incl. 429
  token-plan ×5; `devin/swe-2:max` target 88/121, 8 null, 25 other); keeper
  run_ids 184→183 (runless `bountyfleet1` off-by-one) → unledgered 81→82;
  "2 unparseable" → 0 (b1k-002/133 are valid JSON using `state:"PARKED"`,
  no `transition` key); candidates 116→105 distinct program_ids (111/118
  rows carry one); sessions grep tallies all irreproducible (strict
  `(?<!no_)submission_performed:true` = 4 files not 9; tolerant 20;
  `.ufo`-wide 16; naive 471/61 → 402 lines/91 files, jsonl-only 385/76;
  null `submitted_url` ~51 → 56/61); "grep Outcome over all 22" impossible
  (13/22 contain the string; the 2-READY/20-BLOCKED tally holds via
  disposition markers); `3d28a716` stamp "18:26" → author=committer
  2026-09-06T05:42:43-03:00; tracked claims 20 → 19 program dirs +
  `claims/README.md`; pendle 10 → 6 top-level dirs + 9 files; pin taxonomy
  → verified census (187 files/188 occurrences = 152 top-level + 35 nested;
  157 bare 40-hex + 24 dicts + 3 nulls; the `{cmd,exit}` "family" doesn't
  exist; sparse-clone objects live in `steps[]`); archive-missions 19→20 in
  BOTH regressed lines (ufo-archive-2026.md:11, SKILL.md:385 — r12 fixed
  only :5); queued-hold rows 3→**4** (8x8 `claim-hold` tag exists since
  2026-09-05T19:28:41-03:00, misrecorded absent); `submitted_url` is null
  on all 12 queued rows — route URLs live in `submission_url`/`claim_url`/
  `submit-payload.json`; crypto package severity critical → **Low
  (C:L,I:N,A:N)** ("critical" = wildcard asset's reward tier); superhuman
  "lab-credential-redaction" gate nonexistent (generic attachment hygiene
  only, claim_checklist.md:26); peak model `openai-oauth/` →
  `openai-codex/gpt-6-astra:max` (fleet-dispatch.mjs:300); usage-limit
  signatures 3→**4** (+`usage_limit_reached`, :272); `reward.min` numeric on
  **14** not 48 (48 = reward OBJECT); "~1040" degenerate records → exactly
  **1024** (796 zero + 228 one); queue score is FIVE-termed (+`is_live(1)`,
  :110) and `priority.json` (14) is a strict SUBSET of the 50 continue
  programs — the 9e12 tier only breaks ties inside the continue cohort;
  seeded-13 "without map records" → 9/13 HAVE records (map-less: only
  spacex-starlink/yahoo/monzo/personio; 22 map-less = 4 seeded + 18
  archive-era, `hackerone-zabbix` restored to the archive list); "rank.mjs
  never ran post-refresh" (unbounded negative) → ran ≥2× 2026-09-04 (2
  RANKED ledger lines in its hardcoded append shape; one sha matches
  `rankings-2026-09-04.json`) — the BUMP never persisted (heldByState :199-201
  + S3 gate); tracker "last cycle 20:40Z" → `tracker.log` last line
  17:24:52Z (20:40 = the .md snapshot mtime); telemetry 7218 → **7225 as of
  2026-09-28T21:52:51.978Z** — `check-freshness.mjs:61` appends one line per
  run INCLUDING audit runs ("read-only" fleet tooling is not write-free),
  and the worktree file carries **3 committed merge-conflict markers** (09-06
  merge; JSON.parse fails on exactly 3; invisible to regex-only `attempts()`);
  rankings "~30" → 234 files/229 stamps, zero consumers; 35 distinct event
  keys (naive `grep -o` undercounts `attempt_reset` 92%: 7065 compact vs 143
  spaced lines). **New derived dead code:** `fleet-dispatch.mjs:200` reads
  schema-impossible `ev_inputs.adjusted_ev` (`additionalProperties:false`,
  0/1088) → every `mission_dispatched` logs `adjusted_ev:"unknown"`, the
  negative-EV `ev_note` branch (:204) is dead — AR12 "ledgered honestly"
  holds only in the unknown direction; the :10 in-file comment "EV ordering
  (curated first…)" is doubly false (curated ranks third; "EV" is a boolean);
  two pane crashes exhaust a program's MAX_ATTEMPTS=2 hunt budget (:82,:327).
  claim-check facts added to corpus: blanket symlink ban (:105), 5 MiB
  per-file cap (:111), secrets scan reads EVERY non-symlink file ≤5 MiB as
  UTF-8 (not "text files"), HARD_STOP emits TWO errors (:83-84), title-dup
  threshold 16 chars (:194), strict `adjusted_ev > 0` cutoff (ev-report:91),
  exit 2 for missing arg AND missing file, unparseable → WARNING+exit 0,
  basis column never exercised live (0/1088 `sources[].basis`), full
  `rank.mjs:55-58` DEFAULTS (.7/.7/.25/.6, 60h, 25, 0, 0, 250 → default
  p_success .0735). **New canonical entry `knowledge/triage-thresholds.md`**
  (queue admission filters, score weights + collision bound `reward.min<1e9`,
  dispatcher constants, all claim-check gate tables with error strings, EV
  contract, schema table, shared constants, telemetry register, §9 correction
  ledger) — three-way verified: L1 full-source read × executor draft ×
  reviewer derivation, ZERO model disagreement. Sentinel live-run layer
  (safety-gated: claim-check/ev-report/validate proven write-free from
  source; claim-index + check-freshness EXCLUDED as writers): 281
  `status.json` = 280 packages (PARKED 248/DONE 15/BLOCKED 15/SUBMITTED 2)
  + 1 evidence-copy trap (`bugcrowd-seek/honest-zero/evidence/status.json`,
  PARKED — the 281st); 15 DONE → 12 OK + 3 FAIL (doit 7/github-bounty 8/3cx
  8 errors) exactly matching the generated index; VDP duplicate byte-proven
  (sha256 `ded642e8…` identical, commit d7dbd9a, CWE-78, row still passes
  claim-check); live EV github-bug-bounty 0.9×0.8×0.35×0.7=0.1764, gross
  1764, cost 1250, adjusted 514, positive true. `docs/claim-runbook.md` read
  in full (69 lines; the r10 distillation upgraded to line-cited §A/§B/§C).
  README: `program-quirks.md` was index-orphaned (19 rows for 20 entries) —
  indexed; new recorded gaps: claim-anatomy ~3.6% sampled (≈10/280
  line-by-line), round-2 lesson/LOG hole (history not rewritten),
  positive-blocked weak attestation (2 instances, free-form, gate-invisible
  — annotated in SKILL.md). Adjacency (reported, not absorbed;
  `/tmp/kasegi-r13/connector.md`): `fleets/registry.json` ownership
  CONTESTED (kasegi r11 in-domain decree reading vs kumitate r1
  orchestration claim) → aggregator arbitrates; kagi README cites kake
  SKILL.md:104-107 for the shared CDP lease, now at :116-119 → kagi fixes;
  kotoba inventories a CLAUDE.md inside `george/` → kasegi park stands,
  qualified as unexplored-by-kasegi. Hazards: EvRevenger ran
  check-freshness pre-reconciliation → +1 telemetry line (disclosed, not
  reverted — revert = second mutation); transient EDQUOT zeroed
  ThresholdsReviewer's report file (structured output preserved);
  CitationsReviewer failed degraded (output rejected, artifacts reused); 4
  unexplained mtime-only touches on `.git` dirs 18:34:30/18:37:11 (actor
  [UNVERIFIED]; no locks, rebase state reproduces, not lane-originated —
  scout-drift.md + SCORECARD coverage row). SCORECARD: depth 8→9, coverage
  9→9 (denominator reproduced 18/18; transparency note: 26 root files not
  3; per-file surface set 41/41 class-covered); r14 premise CORRECTED by
  the density census (thin cohort = Program-rule checklist 28.6 +
  anti-patterns 29.7; the triage table ranks #14/18). Mid-round operator
  rule (binding): domain source repos are READ-ONLY — lane compliant (zero
  git writes to `~/Projects/bounties`; pushes only VeigaPunk/kasegi-shokunin
  + VeigaPunk/shokunin). `corpus/lessons/round-13.md` recorded.
- 2026-09-28 — round 14: depth axis-move — the r13 thin-cohort per-item
  citation repair, executed per the corrected r14 plan. 10-L2 batched fan
  (3 scouts, 2 executors, critic, reviewer, connector, revenger, labrat);
  all 10 returned usable output (zero degraded L2s this round).
  **Measured: thin cohort repaired; depth integer held at 9** (Not-10 list in
  SCORECARD). Instrument: `/tmp/kasegi-r14/density.py` (labrat reimplementation
  of the r13 census, calibrated on the exact pre-r13 blob fc6d398 — checklist
  6/28.6 and anti-patterns 11/29.7 reproduce EXACTLY, mean Δ+0.8, residuals
  traced to r13's own table-arithmetic noise + mutually inconsistent date
  counting), same script before (HEAD 7483333) / after: Program-rule checklist
  **28.6→106.6**, Policy access playbook **62.5→462.5**, Disclosure
  anti-patterns **29.7→108.4**; both named sections clear the pre-edit mean
  102.5 (bar rule fixed this round: the post-edit mean 142.5 is self-inflated
  by the repair — compare each block to its own BEFORE). Path-citation
  instances 275→373. Claim-hardening's two prose-only rows re-anchored
  (repair-8; item 13 = `ufo-archive-2026.md:145-149`, item 14 = `:150-154` —
  reviewer's final line numbers; the SCORECARD plan's own ":412-413" reference
  was actually :413-414). All 10 anti-pattern items carry per-item anchors +
  a new per-item anchor-map table (repair-3 deliverable) + a 4-fact
  "same source, not itemized" addendum (wrap `:83`,`:92`,`:99`,`:107`,`:155-157`).
  **3 SKILL falsifications repaired in place** ("round-14 correction" markers):
  (1) header "every fix is a disclosure defect" — FALSIFIED by 2 agents + L1
  read (wrap `:9` defines NO-GO as an open reproduction gate; `:20-21` are
  technical gates); (2) `:412` receipt-drift reconciler pointers — 4028846 /
  a169f309 are in NEITHER `portal-reconciliation-2026-09-11.json` (`:9-11` =
  the Sep-11 trio only) NOR `final-audit.json` (zero grep matches); the real
  store is origin-work `submission-review/` (`receipts/*.json:5-6`,
  `submission-receipts.csv:2-3`, `queue.json:12`) which SKILL `:446-448`
  itself names two sections later; (3) Immunefi `policy_sha256` overreach —
  beanstalk provenance has zero hash keys; Immunefi page hashes land as
  `html_sha256` in keeper telemetry `:181`; the Cantina/HackenProof legs
  stand (pendle `provenance.json:32-33`, atomone `:36`). **One critic
  falsification REJECTED with evidence:** the 2026-09-05 severity decree
  EXISTS at `fleets/claimer-mission.md:29` (critic grepped only `docs/`);
  L1+executor+revenger three-way concordance; git timeline proves the
  override order (wrap fixes b3b1b7e3 19:54 −03:00 → decree applied 2ef530c6
  20:56 −03:00, overriding wrap `:23`'s airtable keep-the-ceiling advice;
  applied at airtable `claim_checklist.md:32`). **Claim-anatomy sampling push
  (recorded gap U1) 3.6%→10.7%:** 20 new full `status.json` reads via
  deterministic stratified rule (`select20.sh`: universe 280, 17 already-read
  excluded, strata quota 0/2/2/2/14, even-index stride; byte-identical
  re-runs; L1 re-ran: universe=280 eligible=263 selected=20, PARKED 16 /
  BLOCKED 2 / DONE 2, SIG 4). D1-D13 deviation classes → new canonical entry
  `corpus/knowledge/claim-anatomy-sample.md`. Headlines: **260/280 (92.9%)**
  deviate from the canonical required-key set (20/280 conformant);
  `claim_review` present 26/280; `claimable` absent 241/280 (exactly the
  b1k-* cohort, 232/233); `manifest_sha256` absent/null 84/280; `verdict` =
  free-form slug (249 distinct/280; undocumented suffixes `-identity` ×121,
  `-host-binding` ×69); D11 state enum omitted PARKED (248/280) →
  `claim-package-contract.md:31` repaired; D12 DONE ≠ filed (spacex-starlink
  + hackerone-x `claimable:true` with `submitted_url:null`;
  `submission_performed===true` = 0/280). SKILL anatomy section carries the
  reality annotation (contract realized in 20/280; six-file set held 18/20;
  hyatt + northwestern-mutual at 1/6 canonical). Checklist section: all 18
  top-level scope-snapshot keys documented (SKILL named 9+2); `:47`
  reward-band/currency FALSIFIED against the SEEK exemplar (only
  `reward_table_url:16` null — true anchors starbucks-japan `:112-118` +
  sherlock-106 `:12-15`; 29/785 carry `currency`); `coverage.status` second
  value `insufficient_for_authorization` (opus-guard `:24`; 58/785 carry
  coverage.status — L1-re-derived); `provenance.json.pin` = four live shapes
  (object / bare string / nested in commands[] / version), not one fixed key;
  `program-quirks.md` linked from SKILL at last (closes r13 repair-2's SKILL
  half). Corpus playbook attribution repaired: "(seek, openai, spacex
  autopsies)" → openai/spacex/blofin autopsies verified (`:6` each), seek has
  NO autopsy (its evidence = snapshot `:54` + BLOCKED.md); `stop_reason`
  anchored to `authorization-envelope.json:49`. Generated-file staleness
  annotated: `docs/claim-ready-index.md` on-disk = **11 rows** (generated
  stamp `:3` 2026-09-06T01:35:16Z) vs **12** claim-check-OK packages — the
  12th (intigriti-yahoo, DONE + `claimable:true` `:2`,`:11`) appears only on
  live regeneration; SKILL `:115` annotated. **Hazards:** mid-round
  unverified actor at 2026-09-28T23:32Z — `freshness_check` (23:32:22.884Z)
  + judge-lane `reroute_drill` simulated (23:32:32.720Z) telemetry appends
  (7225→7227; SKILL as-of refreshed) + mtime-only touch on
  `docs/claim-ready-index.md` (bytes UNCHANGED: HEAD==worktree==11 rows; the
  generator did not run — content stamp still 09-06); no cron/systemd-timer/
  live-process match; an attached `ufo_sighting` tmux (created 15:24) hosts a
  separate live agent session (window 2, "1 running agent"); the two L2s
  alive that minute (labrat, executor-checklist) both attest read-only; not
  lane-originated; actor [UNVERIFIED] — reported-not-explained, same
  treatment as r13's `.git` touches. **Adjacency** (reported, not absorbed;
  `/tmp/kasegi-r14/connector.md`): `fleets/registry.json` is NOT contested —
  the integrator ruled the semantic split at r10 (decree ledger → kasegi;
  routing + registry-check tooling → kumitate;
  `.ufo/reports/round-10/protocol.md:249-252`, `AGGREGATE.md:667`); r13's
  "CONTESTED" flag was stale on our side; D-76 remains open only for
  recording the ruling in both provinces. Kotoba's
  `sibling-description-rewrites-round8.md:259-310` repeats kasegi
  policy-intake facts (derivative snapshot, drift risk); inbound SKILL
  line-cites from siblings/main-repo docs are listed in connector.md — r14's
  renumbering shifts them; siblings re-cite at their own lanes' discretion.
  **Method lessons** (`corpus/lessons/round-14.md`): the density proxy is
  form-sensitive (identical content = 86.0 at 80-col prose vs 973.3 as a
  single-line-row table) → block-vs-BEFORE bar fixed in SCORECARD; three-way
  derivation is load-bearing (critic missed `fleets/`, executor missed the
  I8 definition at `fleets/mission-template.md:20` — L1 found both);
  executor despawn-second-yields overwrote scratch drafts AFTER L1
  integration — integrate from the first verified yield. L1 independently
  derived all 10 item anchors + the checklist anchor set + the decree git
  timeline before integrating. Zero writes to `~/Projects/bounties` by this
  lane (the +2 telemetry lines are external — disclosed, not reverted;
  revert = second mutation). `corpus/lessons/round-14.md` recorded.
- 2026-09-28 — round 15: depth axis-move, forced into a **source-loss
  re-anchor** — the PROVINCE root `~/Projects/bounties` was removed from the
  filesystem at **2026-09-28T23:51:31Z**, ~36 s after the watchdog launched
  this round (`watchdog.log` 20:50:55-03:00) and 19 min after r14's last
  verified observation of the tree (telemetry appends 23:32:22Z/23:32:32Z).
  **Detection** (L1, the round's first command — a domain snapshot, per r14
  lesson 4): `ls -d ~/Projects/bounties` → `No such file or directory`;
  full-depth `find /home/vgpnk -type d \( -name bounties -o -name
  cantina-pendle -o -name bounty-fleet \)` (158.6 s) and `-name missions.jsonl`
  → empty, with exactly one swallowed EACCES stderr line re-run and recorded
  (`nc8r6-ExLibRouteCheck/.ufo/scopes/tmp-r35-eacces-1488153`, mode-000,
  Sep 25, unrelated); `/scratch` depth ≤ 4 → empty;
  `~/.local/share/Trash/{files,info}` → never initialized (no trash store);
  `/proc/mounts` → `/home` is btrfs subvol `@home`, no separate/unmounted
  volume; a `find / -xdev` sweep is worthless here because `/home` is its own
  mount (L1 method error, caught and corrected in-round). A critic L2
  independently re-derived the absence (both casings, the 40-entry `~/Projects`
  listing, full-root name sweep, rename-window sweep, `docker inspect` on all 31
  containers, 72 deleted-but-open fds) and killed the "house-tidy swarm" actor
  hypothesis (`~/.ufo/house-tidy-round0-plan.md` exists, zero execution
  artifacts). **Actor UNDETERMINED**; the single honest blind spot is that btrfs
  subvolume enumeration returns `Operation not permitted` for this user and
  `/.snapshots` is root-only. **Data PRESUMED-LOST locally**; a sentinel L2's
  timeline bounds the event to 23:32Z–23:51:31Z with concurrent activity at
  `origin-work/ufo-fsd-alpha` 20:53:17, `origin-work/tmp` 20:53:56,
  `origin-work/open-bug-bounties/.git` 20:57:10 and an attached `ufo_sighting`
  tmux (4 windows, created 15:24:42) hosting a separate live agent session
  (panes captured read-only, never sent keys). Evidence of record:
  `corpus/knowledge/source-tree-loss-2026-09-28.md` (§1 detection, §2 window,
  §3 the 18 gone surfaces, §4 the survivors, §5 anchor-base rule, §6
  resolvability, §7 the never-re-verifiable DATA-half list, §9 the nine L2
  corrections, §10 measurements). Operator decisions requested in
  `../.ufo/l0-questions.md` (reorg vs deletion · recoverability · PROVINCE
  re-point) — the lane made none of those calls itself.
  **Survivors, measured not assumed.** (1) `~/Projects/the-bounty-hunter` —
  frozen 2026-09-05 code mirror, HEAD `1cfbd86` (A=C 12:35:36-03:00) over
  `37c3668` (v0.1.0, 09:06:07-03:00), tag `v0.1.0`, clean worktree, 34 files /
  8 dirs, remote `VeigaPunk/the-bounty-hunter`; revenger forensics: `.git`
  crtime 09:01:51, reflog holds only the two commits (no clone/fetch), 0 packs /
  48 loose objects, `git fsck` clean ⇒ the local repo is the **origin** of that
  remote, and 9 of 10 sampled `ops/*.mjs` are byte-identical to `37c3668` (only
  `finalize-all.mjs` new + `fleet-dispatch.mjs` modified in `1cfbd86`, whose
  message overstates its own delta). Per-file provenance (L1 reads + 3 scouts,
  sha256-pinned): `ops/ev-report.mjs` 92 ln `ba5485ed6a5d` — **all 14 recorded
  spans at 0 offset**, anchor-compatible; `ops/rank.mjs` 249 ln `e724186c1330`
  — `DEFAULTS :55-59` exact, and its own consistency gate `:126-137` still
  hard-pins `adjusted_ev === 514` at `:136`; `bounty-map/schema.json` 68 ln —
  `ev_inputs :32-52` (corpus `ev-model.md` said `:32-51`, off by one →
  repaired); `ops/park-disposition.mjs` 80 ln — classifier regexes `:18-21`
  verbatim, autopsy writer `:53-74`; **diverged**: `ops/fleet-dispatch.mjs`
  330 ln vs the lost 427 (`mission-control.md:3`) — 3-term score at `:97` vs
  5 terms at `:110`, no `priority.json`/`review-verdicts` reader anywhere,
  `LEASE_MS :43`/`MAX_ATTEMPTS :44`/`TERMINAL :45` vs `:45`/`:46`/`:47`,
  `adjusted_ev` telemetry `:152`/`:155`/`:156` vs `:200`/`:204`, `MODEL :32`
  `qwen3.8-max:xhigh` vs `deepseek-v4-pro:max`, peak `:221`
  `gpt-daybreak-blue-latest:max` vs `gpt-6-astra:max`, family regex `:192` vs
  `:271`, `SYNC_PATHS[0] :269` `claims` vs `claims/README.md`, no `GRID`;
  `ops/shared.mjs` 41 ln — **no `gitMutationBlocker`**; `ops/claim-check.mjs`
  83 ln / **19** `err(` sites vs 233 / 48, with `symlink`, `NO_SCOPE_OBJECTION`,
  `matched_grant_id`, `decision_sha256`, `manifest_sha256`, `claim_review`,
  `finding_count`, `submission_performed`, `BLOCKED.md`, `schema_version` all at
  0 hits; a fourth marker: `lessons/round-4-aggregator-audit.md:28` records 14
  `ops/*.mjs`, the mirror has 13. No second copy of any ops file exists on disk,
  so the live revisions survive **only as corpus quotations**. (2)
  `~/Projects/origin-work/open-bug-bounties` — 26 claim-package dirs + 3 files
  (**0** `status.json`: pre-dates the six-file contract),
  `claim-packages/submission-review/claims` 21 entries, 43 `.ufo-missions`,
  5 `data/*.json` inventories, git HEAD `1307b8b`; the mirror's
  `ops/check-freshness.mjs:14` defaults its board to exactly this path, so the
  two survivors are wired together by the ops code. Inventoried, **not
  censused** → the r16 coverage move.
  **Repairs landed (all mirror anchors L1-verified; `anchorcheck.py` over the
  whole `SKILL.md`: 196 in-range cite instances, 0 past-EOF).**
  `## Triage economics` 93.3 → **131.4**: per-constant cites for the four
  formula terms, `isNum`/`fmt`, the 10-input print loop, all four exit
  branches, the strict `> 0` verdict; the `rank.mjs` run contract + a 7-row
  admission table (reward-floor `unknown`, incomplete-curated `unknown`,
  non-positive never queued, **default-basis positives held** "not sufficiently
  evidenced", duplicate-`RANKED` suppression with fail-open history, the
  DISCOVERED-only advance that never regresses, the top-5 custodian skeleton);
  new derived arithmetic — default priors give `adjusted_ev = 0.0735 ×
  reward.min − 1750`, break-even `reward.min > 23 809.52`, observed max 10 000
  → **−1015**, so every default-basis program is negative-EV and the `:123`
  sort degenerates to `reward.min` desc (AR12 in arithmetic); the
  `expected_reward` two-sources trap (`ops/rank.mjs:92`/`:104` vs
  `ops/ev-report.mjs:78`); dual-base citing for `fleet-dispatch.mjs` with
  `[lost-tree]` markers. Exit semantics are **runnable-verified**, not just
  cited: an L2 smoke-ran a byte-identical copy outside the mirror
  (`/tmp/kasegi-r15/ev-smoke`, copy sha256 == mirror sha256) and observed exit
  2 / exit 2 / WARNING+all-UNKNOWN+0 / `total_cost` finite with `adjusted_ev`
  UNKNOWN on a missing factor / string `"0.5"` rejected per key / exactly-0 →
  `false` / and the round-13 record reproducing 0.1764 · 1764 · 1250 · **514** ·
  true. `## Ops integrity layer` 61.1 → **111.5**: mirror cites for every
  constant (`BANNED :7` + the word-boundary scan `ops/validate.mjs:56`,
  `PARKED :8` and the vacuous `/(?!)/` token `ops/validate.mjs:28`,
  `K3_SEATS :9`/`K3_TOKEN :11`, `sha256File :25-31`, the 3500-byte
  `PIPE_BUF` cap `:33-34`/`:38-39`, validate's 8 gate families, registry-check's
  7 checks incl. the grok-`:low` pin, reroute-drill's simulation contract,
  check-freshness `THRESHOLD_H = 26 :15` + its per-run telemetry append `:61`),
  `gitMutationBlocker` marked absent-from-mirror, the finalize-all divergence
  recorded (mirror = the 39-line genesis version, `:25` only `rev-parse
  --verify` + skip-existing-tag), the sighting windows cited literally
  (`ops/sighting.sh:8`,`:12`,`:17`,`:18`,`:24`), and a new **do-not-run
  hazard**: all 11 mirror ops scripts derive `root` from `import.meta.url`, so
  running one in place would mutate a read-only product repo (and ENOENT on the
  first `appendLedger` — no `ledger/` there) [INFERENCE, never executed].
  **New invariant defect found and proved**: `TELEMETRY_EVENTS`
  (`ops/shared.mjs:13-22`, 8 names) is imported by nothing — `grep -rn` over the
  mirror returns only the declaration and `appendLedger:36-41` never checks the
  name — while the ops scripts append **17** distinct `event:` values, of which
  4 are whitelisted; 4 whitelisted names are appended by no ops script. A
  decorative whitelist, same class as the decorative bounty map.
  `## VDP disclosure packages` 81.8 → **117.4**: the whole surface is now
  stamped corpus-attested, with the mirror-negative proof (0 hits for
  `vdp|disclos|no.?payout|disclosed_free` in any `ops/*.mjs`; only
  `fleets/mission-template.md:50`, `docs/genesis-plan.md:15`,`:17`, two agent
  cards; `ops/finalize-all.mjs:20` filters `state !== 'DONE'` with no
  `DISCLOSED_FREE` case). `## Retirement lane` 62.5 → **93.0**: the four
  classifier regexes quoted with cites, first-match order, the RETRY requeue
  mechanism (`:45-49`), the RETIRED rewrite + `mission_retired` (`:75-78`), and
  the **"five-part" autopsy claim falsified → seven** (4 bold metadata lines
  `:56-59` + 3 `##` sections `:61`,`:67`,`:72`) — `SKILL.md` said five while
  listing seven; `corpus/knowledge/retirement-autopsies.md:38` repaired the same
  way. Preamble + `## Cited paths` header now state the loss, the three anchor
  bases and the measured resolvability. Two unsupported
  `ops/claim-index.mjs:4` cites ("tags are provenance only" — string absent from
  the mirror file) marked `[lost-tree]`; one past-EOF corpus cite annotated
  (`submitted-registry.md:105`).
  **Instruments committed** (`corpus/instruments/`, was `/tmp`-resident and one
  sweep from being lost): `density.py`, `resolve.py`, `anchorcheck.py`, a
  README with definitions + measured limits + the bar rule, and the census of
  record `citation-survival.{md,tsv}`. Continuity proved by an independent L2
  reimplementation across three blobs: pre-r13 `fc6d398` reproduces r13's mean
  96.5 and all four block values; pre-r14 `7483333` reproduces r14's bar 102.5
  and 28.6/29.7/62.5; the live file reproduces all 18 BEFORE-r15 values.
  **Measured**: density file mean 142.5 → **152.8**, path-citation instances 376
  → **622**; resolvability SKILL 47/289 = 16.26 % → **221/485 = 45.57 %**,
  corpus 13.29 % → 15.00 %, lane 14.09 % → **25.50 %**. `BAR_R15 = 142.5`
  frozen as a declared constant and **not cleared** by any of the four blocks in
  prose form — published as a failure rather than gamed, because the labrat
  measured the *unchanged* thin block at 100.0 as prose vs 150.0 as a
  single-line-row table (r14's own record: 86.0 vs 973.3), i.e. the bar is
  reachable by reformatting alone. Bar rule amended for r16: conjunctive with a
  ≥ 60 % resolvability gate, since the mutation tester proved density rewards a
  fabricated `path:line` exactly as much as a real one (8 killed / 4 survived,
  4 blind spots recorded). `SCORECARD.md`: `depth` **split** into
  `depth:density` 9 → 9 and `depth:verifiability` 2 → **4** (the two
  sub-metrics moved in opposite directions, so one integer hid the state; the
  split exposes a worse number), `coverage` 9 → **7** (denominator 0/18
  present, 1 of 2 surviving roots censused).
  **L2 fleet**: 15 subagents in one batched dispatch (3 scouts, 2 executors,
  critic, reviewer, connector, labrat, revenger, sentinel, simplifier,
  distiller, mutation-tester), all read-only, all writing distinct
  `/tmp/kasegi-r15/` files. L1 re-derived every integrated anchor itself and
  rejected two executor claims that failed that check (a `[corpus-attested]`
  stamp misplaced onto mirror-verifiable DEFAULTS; a `:201-205` live-tree span
  no source records). Connector: 339 `Projects/bounties` references across all
  8 lane repos + main (221 path-shaped, 133 in `corpus/knowledge/`), no sibling
  had recorded the disappearance, 4 lanes wrote after 23:51Z without mentioning
  it; `the-bounty-hunter` reported as **mixed scope** (kasegi = bounty
  EV/claim/policy semantics, kumitate = orchestration/tooling, integrator
  arbitrates the repo split) and its remote is outside the `MISSION.md:49-56`
  push allow-list — nothing was pushed there. Distiller: 66 duplicate EV/triage
  statements across 4 files, 22 CODE-half vs 14 DATA-half facts, canonical-home
  map delivered for r16. **Zero writes under `~/Projects/**` by this lane**
  (attested by two L2s independently); nothing reverted, nothing re-created.
  `corpus/lessons/round-15.md` recorded.
- 2026-09-28 — round 17: selected the lowest axis, `depth:verifiability` (4),
  and extended `anchorcheck.py` for the explicit ORIGIN-WORK root only. The
  checker now emits `IN-RANGE(ORIGIN)`, applies realpath/commonpath confinement
  (`OUTSIDE-BASE`), rejects non-files, and reports separate `ORIGIN` and
  `OUTSIDE-BASE` counters. `SKILL.md:683` now anchors lines 5–8 of the
  `k8s-nodebound-token-impersonation.json` receipt: report id, URL, submitted
  date, and status. The source is untracked at open-bug-bounties HEAD
  `1307b8b`; observed SHA-256
  `daaee21c387ff6b2103043e53db1794bb6b6b4eb0c9444bc615aa48ca476122b`.
  Before/after smoke: the baseline checker silently skipped the valid citation
  (0 checked); final fixture reports `ORIGIN=1`, one in-range anchor, and
  `PAST-EOF`, `OUTSIDE-BASE`, `MISSING-FILE` for three negatives. Full
  `SKILL.md` output moved 195→196 in-range anchors, with 46 missing, 5
  lost-recorded, 0 pin-broken, `ORIGIN=1`, `OUTSIDE-BASE=0`.
  `resolve.py` already line-checked resolvable paths, so the lane score is held
  at **4→4**, not credited as a new resolvability gain; its current census is
  480/1506 overall and 222/486 for SKILL. Ten L2s were dispatched in one
  batch; independent critic/reviewer/connector/sentinel/labrat reports
  confirmed the distinction between checker coverage and resolver rate, the
  untracked-source limit, and the exact-root read-only boundary. No external
  source files were changed. See `.ufo/reports/round-17/kasegi.md`.
- 2026-09-29 — round 18: selected the lowest axis,
  **depth:verifiability (4)**, and completed the planned missing-anchor triage.
  Round-open baseline with the r17 checker was **196 in-range / 46 bad / 162
  distinct / LOST-RECORDED=5 / ORIGIN=1**. Broadening the checker over the same
  pre-edit `SKILL.md` exposed its hidden surface: **205 in-range / 82 bad / 171
  distinct**. The old token cleanup stripped leading dots, so `.omp/...` and
  `.ufo/...` were silently mangled; its CITE regex ignored `corpus/`,
  `claims/`, `evidence/`, `.ufo/`, `receipts/`, `csv`, `jsonl`, `rst`, `txt`,
  `py`, and `ts`. Round 18 preserves leading dots, recognizes those anchored
  shapes, supports explicit realpath-confined
  `~/Projects/the-bounty-hunter/` anchors, and reports the correct base on a
  mirror traversal failure.
  **Triage verdict.** Independent L2 census found 15 of the original 16
  distinct missing paths absent from lane, mirror, origin-work, and the two
  surviving repos' histories; only `queue.json` has an exact survivor.
  Name-similar candidates were rejected on content: the mirror
  `docs/example-claim-ready-index.md` is 14 lines / 7 rows / 2026-09-05, not
  the cited 32+ line / 11-row / 2026-09-06 file; groknight `WRAP.md`, packet
  completeness checklists, and origin-work reconciliation are different
  artifacts. Historical sources are now explicit `[lost-tree]` anchors rather
  than apparent openable paths. Context-explicit bare Pendle, Yahoo, 3CX, and
  WordPress anchors were expanded to their full historical paths. The quoted
  stale target-repo text `README.rst:706` was de-anchored with its missing-base
  caveat instead of falsely labelling it LOST-TREE.
  **Four exact re-anchors** now use full ORIGIN-WORK paths:
  `submission-receipts.csv:2`, `submission-receipts.csv:3`,
  `receipts/ld-node-stream-tls-bypass.json:5-6`, and `queue.json:11-12`.
  Reviewer read every range and confirmed the report IDs/URLs and three-report
  note support the no-resubmit claim. The source tree is mutable and all four
  receipt-store files are git-untracked; current-byte SHA-256 evidence:
  CSV `3ed3e6959fc9b005630461c93045f5a2887d64f3d436c69549e87c024ffb80b9`,
  queue `1fa7cb8b1aab2a74a214fc511e0393b72265cbeef023129a1a80365c5f1f676d`,
  LaunchDarkly receipt
  `49525f86053003af053a6ed7a56c1176777682a339bd1ba651189854dab3ce2e`.
  No durable blob-pin is claimed.
  **Measured final:** `anchorcheck.py SKILL.md` = **209 in-range / 0 bad /
  175 distinct / LOST-RECORDED=104 / ORIGIN=5 / PIN-BROKEN=0 /
  OUTSIDE-BASE=0**. Every live corpus file (`corpus/README.md` +
  `corpus/knowledge/*.md`) also has zero bad anchors; three live-file defects
  were made explicit LOST-RECORDED. Pre-r16 lesson anchors remain historical
  under citation-bases rule 6. Density guard: mean **152.9 → 153.9**, path
  citation instances **623 → 645**; no density credit claimed.
  **Resolver correction.** The r15 resolver ingested its own generated
  `citation-survival.md` and stripped leading dots, contradicting its
  byte-identical claim. It now excludes that output, uses trailing-only
  punctuation cleanup, and names the committed instrument in generated output.
  The executor's preserved pre-edit Markdown snapshot was overlaid onto a
  complete scratch copy so both sides used one corrected definition: SKILL
  **228/488 = 46.72% → 232/503 = 46.12%**; corpus
  **246/1145 = 21.48% → 247/1144 = 21.59%**; lane
  **427/1461 = 29.23% → 432/1469 = 29.41%**. Two consecutive final runs had
  byte-identical stdout and outputs: census SHA-256
  `4d3874706d7fd31a0fa9bcdde88ca2f531f12eb6abeca6798732f7c4bef5d46a`
  (Markdown) and
  `95c6a2328a8ff35336470f843c17a797a4b2078e1c7313c04cc383be5b4602e4`
  (TSV). The score stays **4→4**: absolute openable anchors and lane rate
  improved, but the defined SKILL fraction fell after honest denominator
  expansion.
  **Behavioral smoke:** a nine-case `/tmp` fixture proved lane, `.omp` mirror,
  explicit mirror, origin CSV, and LOST-RECORDED positives plus distinct
  MISSING-FILE, PAST-EOF, ORIGIN traversal, and MIRROR traversal negatives.
  It caught and then verified the mirror-base diagnostic repair. `SKILL.md`
  final SHA-256
  `62582f91770bb8a3ad208a861ad735b9c052c635f84c18ab678413089bd3ec7d`;
  `anchorcheck.py`
  `443ff50f62f823977660d7d688f5070acaae1bf973f34b4be59ee84a05fe02e0`;
  `resolve.py`
  `b44247e1eeb192d23f9de9d92a38a031280b091b544532dad3999755ccbafee4`.
  **Inherited work:** round 16 was operator-terminated with citation-base
  normalization in flight; its live-document rewrites and
  `corpus/knowledge/citation-bases.md` were verified and completed here.
  Round-17 ORIGIN support and its log/report are included in the same first
  commit after those interrupted rounds.
  **L2 fleet:** 9 agents in one batched call — 2 scouts, critic, reviewer,
  revenger, executor, connector, labrat, sentinel — all read-only over lane
  and surviving roots, writing only `/tmp/kasegi-r18/`. Census, invisible-token
  enumeration, falsification, semantic anchor review, provenance recovery,
  independent edit map, sibling overlap, baseline, and regex-adversarial
  reports all returned. Connector found no sibling copy of the lost sources.
  **Routing relay:** effective config shows
  `modelRoles.m_swe=devin/swe-2:max` but
  `retry.fallbackChains.m_swe=null`; Daybreak is a separate role, so the
  operator's intended exact `m_swe → daybreak-blue:max` chain is **not visible**.
  No genuine m_swe capacity failure occurred; no advancement was observed or
  forced, and no config or frozen-contract bytes were changed.
- 2026-10-14 — round 19 (re-census after second root loss): both roots the
  round-15 re-base depended on — `~/Projects/the-bounty-hunter` (frozen
  mirror, HEAD `1cfbd86`) and the whole `~/Projects/origin-work` tree — are
  ABSENT (detected 2026-10-14T12:44Z; no relocated copy under `~`; actor
  UNDETERMINED, evidence `corpus/knowledge/root-loss-2026-10-12.md`). The
  OMP substrate `ufo-fsd-alpha` relocated intact to
  `~/Projects/ufo-fsd-alpha` @ `964f443e`. Survey before repair:
  `anchorcheck.py SKILL.md` → **7 in-range / 202 bad / LOST=104**
  (every bad instance an absent-base citation, classes (a)+(b));
  `resolve.py` → 6 RESOLVES / 1341 GONE; density mean 153.9 (guard).
  Repairs: instruments DERIVE their roots (`$KASEGI_MIRROR`,
  `$KASEGI_ORIGIN_ROOT` → first existing candidate → canonical absent path;
  `$UFO_SRC`/`ufo-fsd-alpha` candidates in anchorcheck); new `BASE-ABSENT`
  verdict (own class, not bad) so an absent tree cannot masquerade as a
  missing file; 202 SKILL + 39 corpus anchors into absent bases marked
  `[lost-base]` under the extended citation-bases vocabulary; live ufo-fsd
  citations re-anchored (`ufo-archive-2026.md:31`, `ufo-workspaces.md` ×2,
  `hunt-*` dangling claim re-verified on the moved tree); first-loss note +
  PROVINCE + SKILL header carry append-only factual annotations; lessons
  untouched per rule 6. After: `anchorcheck.py SKILL.md` → **7 in-range /
  0 bad / LOST-RECORDED=306 / BASE-ABSENT=0 / PIN-BROKEN=0 /
  OUTSIDE-BASE=0**; `resolve.py` regenerated census SKILL 32/506 = 6.32 %,
  corpus 116/1142 = 10.16 %, lane 132/1469 = 8.99 % (drop is the domain
  bases vanishing, recorded honestly); density 154.0, cites 645.
  SCORECARD: density 9→9, verifiability 4→4 (held by the r18 definition;
  the measured fraction fell), coverage 7→7. Carried debt named:
  RECEIPT-STORE-LOST, MIRROR-SOURCE-LOST, ORIGIN-REPO-LOST (unblock actions
  in `SCORECARD.md` round-19 row).

## 20 — re-census round (freshness axis-move)

2026-10-14 · steered round 20 · axis: freshness · 32-lane fleet wave + parent integration.

Full round detail: `corpus/lessons/round-20-recensus.md`. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/`.

## Round 17 continuation — 2026-10-15 — explicit mirror citations

Selected **depth:verifiability (4)**, below coverage 7 and density 9.
The explicit steer reuses round 17 after the recorded round-20 work; all
earlier entries and the filed report are preserved, not renumbered.
Motivation: `corpus/lessons/round-20-recensus.md:34-35` named suffix-joining
onto derived roots as an unlanded narrow fix. At lane baseline
`4b2e30231c20d3374a39976df5a0f998a6c6f90c`, a copied resolver CLI with
isolated HOME and a populated `KASEGI_MIRROR` classified **0/2** explicit
canonical mirror citations as resolving, despite the mirror-relative control
being `MIRROR-EQUIVALENT`; the missing-file control remained `GONE`.
Exact stdout: `distinct=4 resolves=0 mirror=1 internal=0 other=0 gone=3 skill=1/4 corpus=0/0 all=1/4`.
Resolver baseline SHA-256:
`97012403e89a94d2478249de4fa198f873520328df14e4432b1040c564e03294`.

The bounded implementation in `corpus/instruments/resolve.py` maps exact
canonical `MIRROR_CANDIDATES` prefixes (tilde or expanded HOME, root or
slash-delimited descendants) to the selected mirror root. It retains
`RESOLVES`/domain `other`, reports the actual selected-root path, rejects
realpath escapes, and never falls back to stale canonical bytes. Existing
bounty, relative and unrelated absolute-root branches are unchanged.
`corpus/instruments/README.md` documents this contract at the end of the
file, preserving its older line anchors. This is measurement correctness,
not a recovered source tree, receipt authentication, or a live-score increase.
The pre-existing user edits to `anchorcheck.py` and its cache are excluded.

**Committed verification:** measured the same copied-CLI fixture at
implementation commit `d43e63c8872c4029c7edb9067d8f272642e7885a`:
**0/2 → 2/2** explicit citations resolve to their expected selected-root
files, with unchanged relative/missing controls and CLI exit 0 on both
revisions. After stdout:
`distinct=4 resolves=2 mirror=1 internal=0 other=0 gone=1 skill=3/4 corpus=0/0 all=3/4`.
Resolver SHA-256 after:
`d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903`.
The full counting command, literal stdin, expected-path definition and
per-revision output are recorded in
`corpus/lessons/round-17-mirror-relocation.md`; SCORECARD names both measured
commit hashes, not its own future record commit. Frozen committed SKILL
resolution is **32/506 → 32/506**, with 0 changed verdicts; SKILL and
PROVINCE bytes are identical. Scores remain verifiability 4, density 9,
coverage 7. Measurement correctness improved; live source availability did not.

Nine L2 roles were dispatched in one native host-routed craft batch:
MirrorPlan (planner), MirrorOverlap (connector), MirrorImpl/MirrorCases/
MirrorDocs (three executors), MirrorEvidence (scribe), MirrorSurface (scout),
MirrorReview (reviewer), MirrorCritic (critic). No per-task model alias or
routing configuration was set. This is not a generic UFO validated wave:
its taxonomy/floor conflicts with the mission-required planner batch.
The connector's bounded sibling scan found no sibling production consumer
or competing owner for this lane-local resolver; kumitate's ufo-fsd
citation checker is an independent surface, not a caller to migrate.

**Historical erratum, not a rewrite:** the older round-17 LOG entry's
`480/1506` numerator is superseded by the round-18 correction
**451/1506** (`SCORECARD.md:88-96`), not by a fresh restoration claim.
The filed round-17 report's old SKILL `222/486` is historical; this
continuation measures **32/506** against the named commits. Its old
`SKILL.md:683` location is not a current line pointer. The new report
assessment adds the missing SHONEN section; no promotion is asserted.

## Round 21 — 2026-10-15 — interactive cutover; routing blocked

Selected lowest LIVE axis **depth:verifiability (4)**; density 9 and
coverage 7 are guards. Highest documented round is 20 (`SCORECARD.md`,
`a5cbf77`/`644ed37`/`de625f9`/`ea36dfc`; shared MANIFEST entry 138 annotates
lane round 20). The launch counter 17 is not a verified completion count.
WWKD saved before work at `plans/wwkd-round-21-authority-audit.md`.
This is one blocked attempt; **no verified-round credit**, no saturation
claim, and no round loop in this session.

**Inherited work reconciled, not erased.** Initial HEAD
`d43e63c8872c4029c7edb9067d8f272642e7885a` already contains the explicit
mirror resolver fix. Initial dirty LOG/SCORECARD continuations and the
untracked `corpus/lessons/round-17-mirror-relocation.md` and
`corpus/instruments/test_resolve.py` are retained as interrupted lane work.
The test's one-line fixture containment repair adds `dir=HERE` so its
temporary writes match its repository-local contract. The pre-existing
two-line `anchorcheck.py` root-join change and cache remain unchanged and
excluded. `initial-hashes.json` under `.ufo/rounds/round-21/` preserves
initial byte hashes; admission checks preserve SKILL, PROVINCE, resolver,
dirty anchorcheck and inherited lesson bytes.

**Named correction to “Round 17 continuation — 2026-10-15” above.**
Its historical prompt does not authorize reusing a completed number after
round 20. Its nine-role craft dispatch is not a validated 32-member wave
under this interactive contract, and is not counted as a newly verified
round. Its assertion that the later evidence-record commit changes no
resolver/SKILL/PROVINCE bytes still holds for those production files; the
inherited fixture test is now durably recorded with the containment repair.
The older shared round-17 report was read-only, not overwritten.

**Exact routing blocker.** `cfg://task/agentModelOverrides` reports executor
`@m_mid`, scribe/simplifier/scout/mutation-tester `@m_fast`,
reviewer/sentinel/revenger/connector `@m_mid`, critic `@m_strong`.
Required content aliases are `@m_composer`, audit aliases `@m_grok`,
connector `@m_antigravity` with `@m_zfl` fallback.
`cfg://retry/fallbackChains` reports `m_antigravity: []`.
All four named aliases exist, but the required role/fallback bindings do
not. No config writes, routing overlays, concrete model pins, capacity
failure probes, hidden substitutes, or second L1 were used.
Metadata is persisted in `.ufo/rounds/round-21/routing-observation.json`.

**Wave:** `.ufo/rounds/round-21/wave-spec.json` has 32 distinct meaningful
scopes: 25 knowledge entries, four high-risk SKILL interfaces, and three
cross-cuts. Canonical `ufo-swarm-wave.mjs plan` and `run` both exited **0**;
complete output is in `wave-plan.json` and `wave-render.json`.
**Zero members dispatched**: native `task` cannot realize the required
bindings. The rendered registry has unassigned handles, not completion
evidence. The known contract-sync/self-iter Phase 0 failures were not rerun;
no native judgment is claimed.

**Own behavioral verification.** Final contained CLI regression:
`python3 -B corpus/instruments/test_resolve.py` → **10/10**, exit **0**
(`contained-resolver-regressions.json`). Re-executed actual copied CLI over
`4b2e30231c20d3374a39976df5a0f998a6c6f90c` versus
`d43e63c8872c4029c7edb9067d8f272642e7885a`: explicit expected-path hits
**0/2→2/2**, relative/missing controls unchanged, both CLI exits **0**;
wrapper `COPIED_CLI_SMOKE: PASS explicit_expected_paths=0/2->2/2 controls=unchanged`,
exit **0** (`inherited-copied-cli-smoke.json`). This is old resolver
mapping correctness, not a round-21 source-recovery or axis improvement.

**Named correction to the inherited 32/506 availability guard.** Replaying
its frozen-code/live-filesystem command produced **33/506** on both
revisions and its 32 assertion failed, exit **1**
(`frozen-skill-guard.json`). Exporting the commits produced **31/506** on
both sides and the same assertion failed, exit **1**
(`snapshot-skill-guard.json`). Exact difference: `.git` and `.ufo/` are
`GONE` in Git exports and `INTERNAL` in today's lane root. A comparison
that declares both input definitions confirms unchanged frozen class maps
and SKILL/PROVINCE hashes, exit **0** (`revision-comparison.json`).
The specific old 32/506 filesystem was not preserved. Failures remain in
the evidence record; no assertion was silently re-pinned or called green.
The new-entry erratum is `corpus/lessons/round-21-routing-blocked.md`;
the inherited corpus lesson is byte-preserved.

**Committed-input instruments**, revision
`d43e63c8872c4029c7edb9067d8f272642e7885a`, in an owned Git-exported
snapshot (never the dirty anchorcheck):
`== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
(exit **0**);
density mean **154.0**, **645** path cites / **18** blocks (exit **0**);
resolver
`distinct=1508 resolves=10 mirror=0 internal=125 other=0 gone=1373 skill=31/506 corpus=119/1181 all=135/1508`
(exit **0**). Full outputs and counting commands are in
`.ufo/rounds/round-21/committed-anchorcheck.json`,
`.ufo/rounds/round-21/committed-density.json`,
`.ufo/rounds/round-21/committed-resolver.json`; definition/hashes in
`frozen-input-definition.json`. Generated snapshot census files are named
`frozen-head-citation-survival.*`, not installed as the live census.

**Own round-local admission evaluation:** full command, every verdict line,
stdout/stderr and exit **1** in
`.ufo/rounds/round-21/admission-gate.json`:
`ADMISSION_GATE: BLOCKED failed_requirements=11 verified_round_credit=0`.
Ten wrong role bindings plus the missing connector fallback block dispatch.
Global config SHA-256 remained
`08788ddcbbb48180b987e6f54b517af294c85cacceb07bdd594843a53e668dcc`.
No new product gate is registered. `corpus/QUALITY.md` is missing;
conformance debt, no fabricated quality authority. `MINT.md` absent; no
mint/promotion. No outside non-author spot-check.

**Verdicts:** depth:verifiability unchanged (4→4), depth:density unchanged
(9→9), coverage unchanged (7→7); expansion/quality/discernment unchanged.
No current authority/severity/decree change was admitted without the
required wave. Source-loss and prior corpus debts remain named, not fixed.

**Boundary and continuation:** no push, network research, sibling/source
mutation, shared-ledger/report mutation, credential contents, native
transcript bodies, or journal contents. Shape-only pane check returned
`%16 node /dev/pts/17`, exit **0** (`interactive-pane-shape.json`); the
operator's interactive composer was not replaced with a log watcher.
Routing owner must supply authorized effective composer/grok/antigravity
bindings and ZFL fallback; missing quality bar needs grounded criteria
before knowledge admission. Fresh-session continuation/report/receipt
artifacts belong only inside this repository's `.ufo/`. A local blocked
receipt must not be represented as Sighting acceptance or a verified round.

## Round 21 publication — 2026-10-15 — local report and continuation

Owned reconciliation committed as
`67fb678ae6b148e5f38ca74bbf77143bc5be5973`, lane identity, pathspec-limited.
The report was then written at `.ufo/reports/round-21/kasegi.md`, citing that
actual commit; fresh-session handoff is `.ufo/continuations/round-21.md`.
The corpus index names both the preserved inherited lesson and the new
round-21 correction. No shared report or ledger was changed.

**Receipt prerequisite re-measured on the real surface.** The selected
Sighting launch's identity/path metadata has no assigned task key or
applicable expected prompt/config receipt binding. Nested dispatch and
provenance keys also lack them; the canonical `.ufo/*pending*`/`.ufo/*queue*`
name sweep found no matching files. This is not authority to synthesize a
`task_<24 hex>` key. Public launch prompt/config digests were measured and
persisted in `.ufo/rounds/round-21/launch-file-hashes.json`.

Canonical `ufo-mission-result.mjs create-receipt` was actually invoked using
the observed run/session, source prompt/config digests, real local report,
producer `kasegi-shokunin`, and `iteration.decision=blocked`, omitting the
unavailable key. Exact refusal:
`{"schema":"ufo-mission-result-error-v1","code":"invalid_id","message":"taskKey is not a safe local identity","details":{}}`
— exit **1**, no receipt file created. Full input and output:
`.ufo/rounds/round-21/receipt-input.json` and
`.ufo/rounds/round-21/receipt-mint-attempt.json`; prerequisite record:
`receipt-preflight.json`. Receipt validation was not run on a nonexistent
receipt and no Sighting completion command followed the failed mint.
The integrator must supply the real applicable binding; a local report is
not accepted completion evidence.

Timestamped own-mission observation at 2026-10-15T05:19:02.329572Z:
899.474 seconds since launch, just below two 450-second ticks; **progressing**
on the real work commit above (`owned-mission-liveness.json`). The report
flags this same owned mission as progressing if it crosses that review
threshold during publication. No sibling liveness/process control or
elapsed-budget stop was inferred. This remains one blocked attempt,
**zero verified-round credit**, all axis/trend verdicts unchanged.

## 2026-10-16 — protocol conformance: SCORECARD contract fields

Operator rollout per the 2026-10-16 fleet amendment (fleet-root `84bade0`): appended the missing `SCORECARD.md` contract sections. Already present as real sections: axes (`## Axes`), planned (`## Planned`), retired (`## Retired`). Added by this rollout: `## Capabilities` (empty repertoire table, placeholder row only) and `## Saturation` (deferral line naming the lane's next-round obligation).
No axis claim was made and no score moved: purely additive scaffolds, no verdicts, no numbers, no round executed.

## Round 22 — 2026-10-19 — kaika: QUALITY bar, source registry, frontier, provenance disclosure

Steered round 22 (r21 blocked, zero credit, consumed 21); worktree `kaika/round`,
base `94aace2`; no collision (`.ufo/reports/round-22/kasegi.md` absent at start).
Claims: **C1 depth:verifiability** (lowest axis, 4) and **C2 coverage** (7) with
capability `sources-registry`. Setup: `corpus/QUALITY.md` (Q1–Q6, R1–R6), each
criterion citing its mined mistake in `corpus/lessons/round-22.md`.

**L2 swarm.** One batched call of 12 (planner, connector, 4 executors, scribe,
scout, labrat, critic, reviewer, sentinel), each prompt led by `/skill:godspeed` +
the verbatim directive. Two earlier batch attempts were refused by the session's
100-job cap and started nothing. All four executor seats then hit provider
exhaustion (`resource_exhausted`, free-model rate limit); they were cancelled and
re-dispatched fresh in one batch on the re-routed bucket. Post-integration
reviewer/critic/sentinel ran as a second batch of 3.

**Motivating evidence.** STATE dossier §3/§5: 0/25 provenance headers, no
QUALITY bar, no Frontier, no PROVINCE structure, 22 D10 live dead-path lines.
ART dossier: CVSS v4, CVD timelines, safe harbor vs scope, AI-assisted finding
validation and CWE Top 25 2025 method are uncovered or program-specific only (scout
sweep: `/tmp` record summarized in the report, commands `git grep -niE … 94aace2`).

**Landed.** 25 legacy entries: appended `## Provenance (round-22 correction,
appended)` blocks (`source:`/`verified-at:`/`recheck:`; 23 rechecks fail closed,
2 pass) + 31 same-line `[r22 correction …; historical]` markers (22 from the r20 audit class, 9 more found by the r22 post-critic: `submitted-registry.md` :9, :21, :23; `intake-and-finalize.md` :84, :95; `ops-invariants.md` :121, :126, :129, :135). Five admitted
entries (S001–S015 re-opened). `corpus/SOURCES.md` 27 rows, census clean.
`corpus/README.md` +8 map rows + `## Frontier` F01–F08; `PROVINCE.md` Core/Frontier/
Adjacent (classification, not re-scope). SKILL.md: one appended block `## Frontier
decision table (round 22)` (155.6 ≥ BAR_R15, 7/7 cites resolve).

**Caught before commit (M17).** Inserting headers at line 2 shifted every
path:line anchor into the legacy entries by +3 (anchorcheck printed
`mission-control.md:3` as the new verified-at line). Headers moved to an
appended block; all 25 files' original lines are prefix-identical to `94aace2`;
anchorcheck summaries for SKILL.md and four anchor-heavy entries equal base.
Numstat "deletions" in six files are same-line suffix appends (16 hunks, 0
non-prefix).

**Re-verification (freshness).** Lost roots re-tested 2026-10-19:
`~/Projects/bounties`, `~/Projects/the-bounty-hunter`, `~/Projects/origin-work`
absent; `~/Projects/ufo-fsd-alpha` present (root-loss recheck exit 0).

**Verdicts (pending non-author verification).** C1 improved, score held 4;
C2 improved, score held 7; capability `sources-registry` enters; depth:density
held 9 (18 pre-existing blocks' value columns unchanged, block 18 `lines` 37→38 from the separator; mean 154.0 → 154.0). Resolver rise (SKILL
32/506 → 39/513, corpus 140/1212 → 187/1259) is all INTERNAL, GONE 1383 → 1383 —
reported, not credited. No push (standing operator rule overrides MISSION.md
commit-then-push).

**Post-integration review fixes (second L2 batch, before commit).** Reviewer:
a backticked placeholder recheck in the lesson counted as a GONE resolver token
→ unbackticked; `repo-git-state.md` recheck passed vacuously (0 cites) →
rewritten to fail closed on `~/Projects/bounties/.git`; S024's Article 14(2)(a)
quote matched only a secondary mirror and EUR-Lex Article 14 was unreachable to
L1 too → row narrowed to the opened recitals, still `queued`. Critic: 9 more
still-current how-tos/assertions marked; `corpus/README.md:5` global "everything
read from bounties" claim given a same-line scope correction. Sentinel: Q6's
literal vault-scheme text would trip the commit credential sweep → reworded;
no live-target, signed-URL or injection findings.


## 2026-10-17 — README: Devin wiki link

- Operator directive (2026-10-17): insert the Devin wiki link into the README header of every repository with a generated wiki.
- Change: `README.md` created (lane-header convention) with a `**Wiki:**` link to https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/kasegi-shokunin?branch=master.
- Evidence: the org's Devin wiki index lists this repo's generated wiki; sibling lane READMEs carry the same `**Wiki:**` header.
- Documentation-only change; no round run, no axis moved, no verdict changed.

## 2026-10-25 — round 23: detector soundness + F06–F08 admission (attempt 2)

- Frozen claims unchanged (`.ufo/waves/round-23/claims.json`, base `922a4dde`):
  C1 depth:verifiability mirror-fallback soundness; C2 coverage F06–F08 0/3 → 3/3.
  Lane tip at attempt start `1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a` (inherited
  checkpoint `8bf9807`, "policy-paused, unadmitted, no task resumption").
- C1 landed: `corpus/instruments/resolve.py` gains `bounty_suffix()` (exact-root
  boundary; `bounties-x` is an ordinary other root) and applies
  `under_mirror(realpath)` to the bounty and relative mirror fallbacks. Counter:
  new `corpus/instruments/mirror-containment-check.py` replays the frozen
  13-case `mirror-containment-fixtures.json` on real copied CLI bytes. Baseline
  `922a4dd` bytes: escape **0/6 GONE**, matrix 7/13, exit 1 (do-nothing control,
  `.ufo/waves/round-23/c1-baseline.json`). Landed bytes: escape **6/6 GONE**,
  controls 7/7, **13/13, exit 0** (`.ufo/waves/round-23/c1-fixed.json`). Both runs
  print `matrix_sha256=5e61a33e…b5e76a9`.
- C1 no-harm guard: frozen `git archive 922a4dd` export run through both detectors
  — `changed=0 added=0 dropped=0`, identical summaries
  (`distinct=1589 … all=208/1589`). `mirror=0` on this host makes that diff
  vacuous; published as vacuity, the matrix carries the evidence.
- C2 landed: `corpus/source-snapshots/round-23/manifest.json` minted (19 quote
  assertions, three snapshot digests). The three published rechecks now exit 0
  (`S018`, `S029`, `S030`); failing controls exit 1/2/1 (flipped digest, missing
  source, fabricated quote). `corpus/README.md` § Frontier F06–F08 flipped
  `queued → admitted` with entries and current sources (S018; S030 supersedes
  S022; S029 supersedes S024). Counts: F06–F08 **0 → 3**, frontier **5/8 → 8/8**.
- Mistakes mined: M6 (inherited state presented as landed; the fix had to be
  re-implemented), M7 (F08 Article 71 quote was a paraphrase — corrected to
  `This Regulation shall apply from 11 December 2027.`), M8 (`<u>` markup in S030's
  4.1.9 line now disclosed), M9 (frozen C1 predicate vs literal-hit carve-out,
  pinned as a control), M10 (guard vacuity disclosed), M11 (entry recheck pointed
  at a manifest that did not exist). All in `corpus/lessons/round-23.md`.
- Census: `scripts/sources-census.sh validate --root … kasegi` exit 0 (30 rows,
  W04 warnings on the S028/S029 reused URLs).
- Waves: wave 1 inherited (`kasegi-r23-build`, 64 seats, 44 reports); wave 2
  `kasegi-r23-falsify` (36 seats, 19 attack roles) validated under the v1 policy,
  refused once at the host job limit (`.ufo/waves/round-23/falsify/refusal-1.json`),
  then dispatched intact after capacity freed.
- Lane commit: `953c27880a97e8d3aaf8fac44c97e0252cddcddf` (round-23 work).

## 2026-10-25 — round 23, after the falsify wave (36 seats)

- The wave attacked the first landing and found real defects; all were repaired
  before the closing commit `2712c99268ff71e465304ce3846d52f5cf4af1a6`.
- C1 matrix grown 13 → **20 cases** (9 escape, 11 control): absolute-arm cases,
  literal-present carve-out controls, brace/glob expansion cases. Do-nothing
  control on the final matrix: escape **0/9**, controls 11/11, 12/20, exit 1.
  Landed bytes: **20/20, exit 0** (`resolver_sha256=fce5b84b…`, `matrix_sha256=4e39f65c…`).
- Checker hardened: fixture-name confinement (a doctored matrix could unlink a
  host file), `resolved_path` assertion per class, process-group timeout,
  per-case containment, bounded stored output, checker sha + UTC stamp in the
  receipt. The lane-relative `INTERNAL` carve-out is now a labelled pin
  (`carve-out:path-outside-internal`), not a silent pass.
- F07 corrected to the **current** CNA rules: v4.2.6 (approved 2026-10-14,
  effective 2026-10-20) supersedes v4.2.0, and 4.2.11 changed SHOULD→MUST. New
  row S031 + normalized `pdftotext` snapshot (49154 B) + 10 assertions; entry
  rewritten with rule-number locations only (no page claims). The inherited
  `build/CnaFix.md` had found this on 2026-10-20 and no corpus file disclosed it.
- C2: four rechecks exit 0 (`S018`, `S029`, `S030`, `S031`), controls 1/2/1;
  receipts `.ufo/waves/round-23/c2-recheck-S0xx.txt` and `c2-controls.txt`.
  Residual debt named: F01–F05 rechecks exit 2 `not-listed` (no capture exists).
- Frontier counter made field-exact (`awk` on the status column) and the three
  new Coverage-map rows appended; README provenance line extended to 33 entries.
- Final seal: matrix **23 cases** (11 escape, 12 control), fixed **23/23 exit 0**
  (`resolver fce5b84b…`, `matrix 332a5fe9…`), do-nothing control **0/11 escape GONE**,
  12/23, exit 1. Two cases added after mutation seats proved the earlier matrix could
  not see lane-first ordering or the mirror-root prefix sibling; the bare-glob case
  was replaced by the discriminating hop form. `source-recheck.py` now applies a
  declared normalization (`normalized=markup-whitespace`), implementing
  `considerthese/2026-10-24.md` proposal 1; QUALITY gains Q8 and R10.
- Rescue pass after the last seats: docstring prose rescoped (module header names
  r23; the round-19 comment no longer claims BOUNTY keeps plain exists?GONE; the
  root-only bounty rule stated in the policy, not only in a code comment), and one
  more escape case added (`bounty-root-underscore-sibling`, a same-name continuation
  the boundary must reject). Final matrix **24 cases (12 escape, 12 control)**,
  fixed **24/24 exit 0** (`resolver 690153ad…`, `matrix d05b1e0c…`), do-nothing
  control **0/12 escape GONE**, 12/24, exit 1.

## 2026-10-25 — round 24 (C1 verifiability instruments, C2 assimilation/F09)

Frozen claims `.ufo/waves/round-24/claims.json`; base `d0a3f6a`, tip at start
`c2480b1`. Two claims, distinct axes, both measured; no axis harmed.

- **C1 depth:verifiability — the two routed verifier defects, fixed and measured.**
  Counter A (every Frontier entry's own `recheck:`): **3/8 → 8/8** (frozen shell
  form, cwd-pinned); the F09 entries make it **10/10** under the new harness
  `corpus/instruments/frontier-recheck-count.py`, which refuses a line that is not
  a `source-recheck.py` invocation, whose `--source` set does not cover the entry's
  header sources, or names a manifest that does not list them. Counter B
  (`resolve.py` dispatch): **4/8 exit 1 → 8/8 exit 0** on
  `resolve-dispatch-check.py` + `resolve-dispatch-fixtures.json` (8 cases, 4
  liveness / 4 control, class **and** resolved path asserted), with the round-23
  containment matrix still **24/24 exit 0**. Resolver changes: an empty brace
  alternative in a real set is now a literal expansion (a bare `{}` stays a
  placeholder), a brace alternative that carries a `<...>` placeholder is globbed,
  the glob branch credits the first match that *exists*, and the CLI refuses a
  non-directory root and an empty census run (wave-1 seat truncated
  `citation-survival.*` with `--help`; restored byte-exact).
- **C1 captures.** `corpus/instruments/capture-source.py` (HTML/PDF/text →
  UTF-8 text, deterministic, `--selftest` exit 0) + `source-snapshots/round-24/`
  (19 captures, 77 assertions, `source-recheck.py` exit 0). `source-recheck.py`
  now rejects a quote shorter than 12 normalized characters, prints the
  occurrence count it observed, and verifies an optional `anchor` line (the
  round-23 manifest's one non-unique assertion now reads `anchor=10-ok`).
- **C2 coverage — F09 admitted (8/8 → 9/9) with two entries, re-grounded in-lane.**
  `authorised-testing-rules-of-engagement.md` (S032 NIST SP 800-115 Appendix B)
  and `statutory-authorization-and-unauthorized-access.md` (S033 e-Gov
  consolidated text, with S034 MIC page and S035 NPA commentary). Registry
  **31 → 35** rows (S032 A, S033 A, S034 B, S035 A; mined 19→23), census exit 0
  with only the two pre-existing W04s. Package `chinese-criminal-thresholds-and-
  authorisation.md` **refused**: its own cited 第二百八十五条 lacks the
  情节严重 element it asserts (Q2/Q4), its `recheck:` cannot fail closed, and it
  points at `ground: F12`, which the lane does not have. S034's title corrected
  `防止 → 禁止` before landing (log only; row added this round).
- **Assimilation (§10).** Package `/home/vgpnk/Projects/shokuknow/merge/kasegi`,
  read-only. Collision check: lane registry max S031 vs staged S031–S124 →
  **1 collision (S031, HackerOne policy set vs CNA Rules 4.2.6)**; guard proved on
  an indented scratch fixture (`assimilation/guard-proof.txt`: 0-3-space pattern
  catches it, column-zero-only does not). Map `assimilation/renumber-map.tsv`:
  S123→S032, S039→S033, S040→S034, S041→S035; the other 90 staged rows are not
  adopted and get no id.
- **Docs/contracts.** QUALITY gains Q9 (assertion binding), R11 (counter
  instruments publish their discrimination), R12 (a recheck line is measured
  against the entry that owns it); `corpus/instruments/README.md` gains the
  round-24 section including the published blind spot; `corpus/README.md`
  provenance line, F09 row, coverage-map rows and frontier denominator updated;
  `PROVINCE.md` Frontier F01–F09.
- **Waves.** Wave 1 `kasegi-r24-build` 43 seats (scout 22, reviewer 7, executor 5,
  scribe 3, critic 3, mutation-tester 1, connector 1, sentinel 1), all reports
  landed. Wave 2 `kasegi-r24-falsify` 35 seats (attack roles 24/35 = 69%)
  validated under the v1 policy; first dispatch refused at the host job limit
  (`wave2-refusal-1.json`), payload resent unchanged.

## Round 25 — 2026-10-25 — recheck lines made executable; vendor disclosure policies admitted as F10

Frozen claims `.ufo/waves/round-25/claims.json` (C1 depth:verifiability **4**, the lowest
non-retired axis; C2 coverage **7**); base `b49948f`, lane HEAD at this entry `98261ebaf06b6415badaec362c69623d0e1db880`.

- **C1 depth:verifiability — every entry's own `recheck:` line, made executable.** Counter
  `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json`
  (one instrument digest for every receipt, `c3c19adc…`): before `lines=35 pass=6
  executes=12 gated=0 broken=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`; frozen surface
  after `lines=35 pass=35 strict=35 exit=0`; final tree `lines=37 pass=37 strict=37 exit=0`,
  `executes=14 gated=23 broken=0`. 29 of the 35 original lines were rewritten — the 23 prose
  hybrids `on-restoration — <CMD> (<NOTE>)` became `cd <lane> && <CMD>  # on-restoration — <NOTE>`,
  and the 6 cwd-dependent lines gained the prefix; `git diff --numstat` is `1 1` on each of the
  29 files. The 23 fail-closed lines still fail closed, now against the documented absent bases
  (exit 2 → 1), not a syntax error.
- **C1 disclosed limits.** (i) C2's two entries take the audited surface from 35 to 37 files, so
  the frozen `lines=35` literal is reported for the frozen surface while the final tree measures
  `lines=37`; both receipts are produced by the same instrument digest. (ii) The counter was
  repaired after the freeze: a mutation-tester showed the frozen three-limb predicate reachable
  by degenerate lines (`cd <lane> && true`, `test -e <own file>`, `--selftest`); four strict
  limbs and a completeness rule now sit beside the frozen three, and the degenerate controls are
  `--selftest` fixtures. (iii) The `executes/gated/broken` classes make "37/37 form-conformant;
  14 execute today, 23 gated" the honest sentence — never "37 entries re-verified today".
- **C2 coverage — F10 admitted on five captures, entries 0 → 2.** Counters:
  `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 9 → 10;
  `grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md | wc -l` → 0 → 2;
  census → exit 0, rows 40. Entries: `vendor-disclosure-policies-as-corpus-objects.md`
  (S036–S039) and `vendor-disclosure-policy-commitments-crosswalk.md` (S040 crosswalked against
  S036/S038/S039). Registry 35 → 40 (S036–S040, tier A, mined 23 → 28). Manifest 5 records /
  40 assertions, all `occurrences=1`; `frontier-recheck-count.py` entries=12 pass=12 exit=0.
- **Assimilation (§10).** Package read-only; id collision check: 5 ids (S031–S035), guard proved
  on an indented fixture. Staged → lane: S055→S036, S056→S037, S057→S038, S060→S039,
  S068→S040. Admitted 5 rows; refused the staged `vendor-cvd-policy-crosswalk-2026-10-23.md`
  (Q3: "two conditions" is four in its own bytes of record; Q7: prose recheck; F20 row does not
  exist). Five further staged entries not adopted (id collisions in the S031–S035 zone and
  ground rows F11/F19/F20 that do not exist). The claims.json planned reject reason ("Cisco
  unreachable") was falsified by this round's capture log and corrected.
- **Routed defects D24-1…D24-5 — closed.** D24-1: this entry and the report cite the lane HEAD
  at write time. D24-2: one number, 76 assertions over 19 records, with its counting command in
  `corpus/instruments/README.md`; SCORECARD corrected; the round-24 lesson carries an appended
  erratum (R9). D24-3: the bound-64→8 mutant is now measured on the landed bytes (mutant
  `88122e10…`: dispatch 8/8, containment 24/24 — `.ufo/waves/round-25/d24-3/receipt.txt`).
  D24-4: one reconciling sentence in the round-25 lesson, receipt as authority. D24-5:
  cwd dependence 6 → 0.
- **Census.** Before: exit 0, rows 35, A=32 B=1 C=2, mined=23 queued=9 rejected=3, W04 ×2
  (S028/S029 pre-existing). After: exit 0, rows 40, A=37 B=1 C=2, mined=28 queued=9 rejected=3,
  same two W04, no new warnings.
- **Waves.** Two v1 waves. Wave 1 `kasegi-r25-build`: 38 seats (reviewer 12, scout 7,
  executor 5, scribe 5, critic 4, mutation-tester 2, connector 1, sentinel 1, simplifier 1);
  wave 2 `kasegi-r25-falsify`: 32 seats (reviewer 16, critic 7, scout 4, mutation-tester 2,
  simplifier 1, sentinel 1, connector 1), dispatched after wave 1 against 32 distinct attack
  items. Total 70 seats. Wave-2 reports are under `.ufo/waves/round-25/wave2/`; final
  dead/refused counts are from `wave2/swarm-registry.json` and `wave2-dispatch.json`.
- **Tooling.** No tool installed or upgraded; no pacman transaction attempted.
- Final wave-2 correction: role mix is reviewer 16, critic 7, scout 4, mutation-tester 2,
  simplifier 1, sentinel 1, connector 1 (32 total); all 32 reports landed, 0 dead seats, 0
  dispatch refusals. The final round-25 capture manifest has 5 records / 40 assertions after
  adding the missing S036 third-party-products assertion (anchor 15); all source rechecks exit 0.

## Round 26 — 2026-10-25 — recheck-audit gate conformance; F11 ISO/IEC 29147/30111 division-of-labour admitted

Frozen claims `.ufo/waves/round-26/claims.json` (frozen_at_utc 2026-10-25T12:27:41Z): C1 depth:verifiability **4** (lowest non-retired axis, held) and C2 coverage **7** (held). Round base (claims freeze commit) `1b076fa7f2fb5e7dd9d87449514eba526043421b`; lane HEAD at this entry `1b076fa` with the wave-1 build in flight — verdicts are measured at wave close, and this entry records the frozen gate lines with the observations available at write time.

- **C1 depth:verifiability — recheck-audit gate conformance (fixes R25-2, R25-4, lane-declared entry-deletion soundness).** Instrument unchanged at freeze, `recheck-audit.py` sha256 `c3c19adc…`; live baseline `c1-live.json` prints `lines=37 pass=37 strict=37 complete=true exit=0` on the 37-entry tree. Frozen limbs: (a) SKILL.md gains a gate|probe registry row for recheck-audit.py (verdict map, `--selftest` spelling, pinned-value path, write scope, owner) — currently **0** rows, target ≥1; (b) a committed selftest receipt line `selftest cases=… failures=0` in `.ufo/waves/round-26/c1-receipt-index.txt` at the instrument's own sha256 — file not yet present at write, target 1; (c) fix-control #3 restated to exclude the retained historical `round-24.md:77` line — `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l` → **0** at write (the only match is the excluded historical line); (d) deleting a whole `corpus/knowledge` entry flips the audit exit 0 → **1 naming the missing entry** (before: exit 0, 36/36 lines — the expected-list contract on top of the completeness rule). Kill rule: any counter misses its after value, or the do-nothing control hits any after value; control receipts land in `.ufo/waves/round-26/c1-controls/`.
- **C2 coverage — F11 admitted: ISO/IEC 29147/30111 division-of-labour theme, re-grounded on a fresh capture of the JPCERT/CC 2026 partnership guideline (S041).** Frontier 10 → **11** (`awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md`); ≥1 entry cites a row first registered this round (at write, 1 knowledge file matches `^source: S04[0-9] ` — the round-25 F10 entry's S040; S041 is the round's first-registered row); sources census `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exits 0 at round end. Kill rule: a source row appended without an admitted entry citing it. Assimilation (§10): staged S076 (division-of-labour anchor) / S064 (付録6 §4 + 参考1 anchor) adopted by document as **S041**; rejects with reason + flip retained (vendor-cvd-policy-crosswalk, chinese-criminal-thresholds-and-authorisation); quarantine slice S037/S054/S048/S065/S068/S069/S070. `PROVINCE.md` Frontier now carries the F11 sentence (this wave's scribe append).
- **Tools touched.** `recheck-audit.py` **expected-list contract** — limb (d), above: the audit verifies against an expected entry list, so a deleted knowledge entry is named and exits 1. `capture-source.py` **pdf kind** (`--kind pdf` via `pdftotext`, poppler 26.08.0, pre-existing): S041 capture @ `2026-10-25T12:34:17Z` — status 200, fetched 1,338,665 B → snapshot 147,267 B, sha256 `e18acbf9…`, 2,354 lines, staged at `corpus/source-snapshots/round-26/S041.txt` (executor receipt `wave1/ExecCaptureS041.md`).
- **Gate/verdict lines (frozen counters, lane root).** C1(a) `grep -cE '^\| [^|]+ \| gate\|probe ' SKILL.md` 0 → ≥1; C1(b) `grep -cE 'selftest cases=' .ufo/waves/round-26/c1-receipt-index.txt` 0 → 1; C1(c) `grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l` 1 → 0 (observed 0 at write); C1(d) `python3 corpus/instruments/recheck-audit.py --root <scratch-tree-with-one-knowledge-entry-deleted> --cdroot <lane-root>` exit 0 → 1 naming the deleted entry; C2 frontier `awk …` 10 → 11; C2 `grep -lE '^source: S04[0-9] ' corpus/knowledge/*.md | wc -l` 0 → ≥1; C2 `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0. After-values are this round's targets; receipts land in `.ufo/waves/round-26/` (c1-receipt-index.txt, c1-live.json, c1-controls/, c2-controls/).
- **Tooling.** No tool installed or upgraded; no pacman transaction attempted (host-wide pacman paused). `pdftotext` 26.08.0 present before the round; `capture-source.py`'s pdf kind uses it.
