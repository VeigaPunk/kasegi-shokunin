# kasegi-shokunin corpus — index

Proprietary memory for the bounty & security research domain. Everything here
was read from `/home/vgpnk/Projects/bounties` on 2026-09-28; each entry names
its source. No generic filler.

## Coverage map

| Area | Entry | Source basis |
|---|---|---|
| Claim-package contract | `knowledge/claim-package-contract.md` | `fleets/mission-template.md` + live packages |
| Complete claim-gate list | `knowledge/claim-gates.md` | `ops/claim-check.mjs`, `ops/claim-index.mjs`, `ops/prepare-claims.mjs` (read in full) |
| Policy access per platform | `knowledge/policy-access-playbook.md` | `mission-template.md`, `docs/autopsies/`, `claims/bugcrowd-seek/` |
| Triage economics | `knowledge/ev-model.md` | `ops/ev-report.mjs`, `bounty-map/schema.json` |
| Mission outcome statistics | `knowledge/terminal-classes.md` | `docs/continuation-notes.md`, `docs/review-verdicts.jsonl`, `docs/wrap-report.md` |
| VDP disclosure packages | `knowledge/vdp-disclosure-packages.md` | `vdp-disclosures/anthropic-plugin-dev-cmd-injection/` + `claims/*-vdp-no-payout/` |
| Mission ledger + ops | `knowledge/mission-ledger.md` | `ledger/*.jsonl` census, `ops/shared.mjs`/`rank.mjs`/`import-board.mjs`/`fleet-dispatch.mjs`, `docs/plan-round0.md` |
| Mission control plane | `knowledge/mission-control.md` | `ops/fleet-dispatch.mjs` full read, `fleets/missions|run|leases|priority|state-snapshots`, `claimer-mission.md`, `review-mission.md`, sighting scripts, `RUNBOOK-resume.md`, `.ufo-mission-report-bh*`, `.ufo-ingestion/`, `.ufo-warden/` |
| Per-program audit store | `knowledge/evidence-dir.md` | `evidence/` census (592 dirs), `ops/fleet-dispatch.mjs`, `evidence/bugcrowd-seek/`, `evidence/sherlock-8/` |
| Retirement + autopsies | `knowledge/retirement-autopsies.md` | `ops/park-disposition.mjs` full read, `docs/autopsies/` 31-file census, `fleets/run/` live classifier re-run |
| Ops integrity layer | `knowledge/ops-invariants.md` | `ops/shared.mjs` (BANNED/PARKED/K3/TELEMETRY_EVENTS/gitMutationBlocker), `validate.mjs`, `registry-check.mjs`, `reroute-drill.mjs`, `check-freshness.mjs`, `sighting*.sh` — all read in full |
| Board intake + batch finalize | `knowledge/intake-and-finalize.md` | `ops/import-board.mjs` (binding/P6/P7/S4) + `ops/finalize-all.mjs` (claim sweep/tag/atomic push) — full reads |
| Claim-hardening defect taxonomy + archive | `knowledge/ufo-archive-2026.md` | `fleets/ufo-archive-2026/` full walk: 19 `claim-*` report.json defect censuses, keeper/whipper (b1k-NNN origin), inquiries briefs, programs/ old evidence shape |
| Submitted-state / do-not-refile registry | `knowledge/submitted-registry.md` | live census: all `claims/*/*/status.json` submission fields (19 signatures), `ledger/missions.jsonl` SUBMITTED/DISCLOSED_FREE, `portal-reconciliation-2026-09-11.json`, `final-audit.json`, `origin-work/open-bug-bounties/claim-packages/submission-review/` (real receipt store), VDP `SUBMITTED.md`, `claim-ready/*`+`claim-hold/*` tags, `_claimer.status.json`, 15 status-less stub dirs |
| Lessons | `lessons/round-1.md`, `lessons/round-1-aggregator-audit.md`, `lessons/round-3.md` … `lessons/round-9.md` | `LOG.md` rounds, commits, `.ufo/reports/` |
## Known gaps

- ~~ops tail (`validate`/`registry-check`/`reroute-drill`/`check-freshness`/
  `finalize-all`/sighting scripts + `shared.mjs` constants) name-only~~ —
  CLOSED round 7: `knowledge/ops-invariants.md` + `knowledge/intake-and-finalize.md`.

- ~~`ops/claim-check.mjs` gate list~~ — CLOSED round 1:
  `knowledge/claim-gates.md` holds the full extracted gate list.
- Cantina fee/precondition pattern: siblings sampled (dydx same blocker class;
  morpho/euler/uniswap/reserve honest-zero) — see `program-quirks.md`.
- ~~`vgn-bounty-lab/` unwalked~~ — CLOSED round 4: empty `git init`, zero
  commits, nothing to learn (`knowledge/evidence-dir.md` §adjacent dirs).
- ~~`evidence/` per-program vs `claims/*/evidence/` unexamined~~ — CLOSED
  round 4: `knowledge/evidence-dir.md` (592-dir census + record schemas).
- ~~`ledger/` writers/state machine undocumented~~ — CLOSED round 4:
  `knowledge/mission-ledger.md` (transition counts, telemetry event census,
  ops inventory).
- ~~`fleets/ufo-archive-2026/` unwalked~~ — CLOSED round 8:
  `knowledge/ufo-archive-2026.md` (19-mission defect taxonomy, b1k-NNN
  keeper origin, `claim-packages/`→`claims/` naming drift, reconciliation
  evidence chain).
- `fleets/registry.json` lane→model routing — possibly cross-domain.
- `george/` (49G comma.ai research dir) — parked round 4: no claim package
  references it; revisit only if one does.
- ~~No consolidated do-not-submit list~~ — CLOSED round 9:
  `knowledge/submitted-registry.md` (3 verified H1 + 3 archive-era live in
  origin-work tree + 3 probable orphans + 1 VDP; Anthropic claim↔VDP
  same-finding collision verified by live claim-check OK; origin-work
  corpus outside every scan; field-spelling + polarity traps; 15
  status-less stub dirs; root zips = dated snapshots).
