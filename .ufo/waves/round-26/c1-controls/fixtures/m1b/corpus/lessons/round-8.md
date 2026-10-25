# Round-8 lessons

Round: 8 (2026-09-28). Evidence: `LOG.md` round-8 entry, commit `round-8`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-8/kasegi.md`.

## What I closed

- **`fleets/ufo-archive-2026/` — the last named known-gap.** The
  pre-consolidation fleet snapshot (2026-09-06→14) turned out to hold the
  single richest unread artifact class: 19 `missions/claim-*/report.json`
  files from the claim-hardening wave — structured before/after defect
  censuses over real `claims/` packages. Extracted a 22-class defect
  taxonomy (`knowledge/ufo-archive-2026.md`) that is the empirical superset
  of `claim-check.mjs`: gate-binding defects the checker catches, plus the
  checker-invisible layer (stale packet drafts materially wrong about
  affected versions, narratives claiming "verified" for never-executed
  vectors, receipt-drift duplicate-submission hazards).
- **b1k-NNN provenance.** `bounty-keeper/keeper.mjs` is the producer of the
  `b1k-NNN` run_ids that `ledger/candidates.jsonl` and
  `evidence/<program>/b1k-NNN/` still reference — a dangling lineage question
  from round 4 now resolved (16-pane wall, 384 cap, 12h night budget, halted
  `night_budget` after 265 launches).
- **`claim-packages/` naming drift confirmed.** Archive references resolve
  to `claims/<platform>-<program>/<slug>/` — verified live
  (hackerone-coinbase/metamask/mongodb dirs exist; `claim-packages/` gone).

## Friction

- `edit` op syntax: `PUT N=M:` needs a trailing body block; `PUT N.=M:` with
  a bare `=M:` suffix was treated as insert. One mis-landed edit — inserted
  literal text at the wrong line; caught on the diff-shaped tool response,
  repaired by re-reading and CUT/PUT. Lesson: single-line replace is
  `PUT N=N:` + `+` body.

## Parked / open

- `fleets/registry.json` lane→model routing semantics — still flagged
  cross-domain (kumitate); registry-check's seven permanent `@role` errors
  remain a checker-side bug reported round 7.
- `george/` stays parked (no claim-package references it).
- Remaining corpus thinness is depth, not breadth: per-program claim anatomy
  across ~274 dirs (only ~10 sampled); diminishing returns until a new
  defect class appears.

## Cross-domain notes (report, don't absorb)

- `inquiries/bounty-fleet-2026-09-06/` briefs pin L2 routes by operator
  decree dated 2026-09-06 (`@fleet_l2`→grok-4.5:low, kimi executor seats,
  daybreak-blue claim-reviewer) — historical routing law, useful when
  reading archive artifacts, not current routing authority.
- `report.json` `route_failures`+`reroutes` fields show the fleet already
  practiced lane-identity-preserving reroutes before the current
  `model_reroute` telemetry vocabulary.
