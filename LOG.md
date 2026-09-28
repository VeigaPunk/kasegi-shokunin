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

  `corpus/lessons/round-4.md` recorded.
