# Round-5 lessons

Round: 5 (2026-09-28). Evidence: `LOG.md` round-5 entry, commit `round-5`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-5/kasegi.md`.

## What I closed

- **`fleets/` control plane → `corpus/knowledge/mission-control.md`.** The layer
  between program records and claim packages was the biggest undocumented
  surface: `fleet-dispatch.mjs` read in full (queue-score weighting,
  2 h leases, tmux pane rotation + reconcile, sole-committer + byte-proofed
  tag/push, UTC-3 dual-method model windows, strict-signature limit
  fallback, SYNC_PATHS), `fleets/missions/` = 584 generated assignments,
  `fleets/run/` = 703-status-file protocol (state census inside), plus the
  claimer + review-orchestrator sibling-L1 contracts.
- **Audit lanes identified:** `.ufo-mission-report-bh*.md` (21 reports,
  every verdict BLOCKED — readiness audit is a new class distinct from
  hunts), `.ufo-warden/` (dispatch ledger), `.ufo-ingestion/` (intake
  cycles + tracker for the separate `origin-work/open-bug-bounties`
  claim tree — a different tree than `claims/`, don't conflate).
- **Resume path documented:** `state-snapshots/` + `RUNBOOK-resume.md` —
  statuses+leases restore, queue self-rebuilds, DONE never redispatches.

## Friction

- `PUT N+` syntax rejected — hashline ops need `<N`/`>N` gap inserts, not
  `N+`. Re-issue after a fresh read of the target range.
- `missions/*.md` count (584) vs ledger `PLANNED` count (219): files
  outlive ledger transitions — census the file tree when claiming coverage,
  not the ledger.

## Parked / open

- `fleets/registry.json` lane→model routing: still likely cross-domain.
- `fleets/ufo-archive-2026/` (10 subdirs incl. missions/sessions/studies)
  — historical archive; worth a census round if a future gap hunt needs
  depth.
- `george/` stays parked (zero claim-package links).
