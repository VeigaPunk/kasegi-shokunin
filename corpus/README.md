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
| Lessons | `lessons/round-1.md`, `lessons/round-3.md`, `lessons/round-4.md` | `LOG.md` rounds, commits, `.ufo/reports/` |
## Known gaps

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
- `fleets/registry.json` lane→model routing — possibly cross-domain.
- `george/` (49G comma.ai research dir) — parked round 4: no claim package
  references it; revisit only if one does.
