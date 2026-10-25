# Round-7 lessons

Round: 7 (2026-09-28). Evidence: `LOG.md` round-7 entry, commit `round-7`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-7/kasegi.md`.

## What I closed

- **The ops tail — last name-only surface.** Six `ops/` scripts plus the
  four `sighting*.sh` wrappers and the `shared.mjs` constants were cited
  but unread. Full reads → `knowledge/ops-invariants.md` (shared constants:
  BANNED=cursor/opencode, PARKED empty since 2026-09-04, K3_SEATS
  judge/planner, gitMutationBlocker; validate.mjs schema-subset +
  referential checks; registry-check.mjs seven-check lane↔card bijection;
  reroute-drill simulation-only lane identity proof; check-freshness 26 h
  live-source alarm; sighting windows) and `knowledge/intake-and-finalize.md`
  (import-board binding/P6/P7/S4 mechanics; finalize-all batch claim sweep).
  Every `ops/` file is now first-read, not inferred.

## Friction

- Minor: `PUT >N*:` again fell back to plain gap insert on a prose
  paragraph — landed correctly after re-read. Cosmetic triple-blank cleanup
  needed after the insert.
- `git -C claims log` inside `sighting-board.sh` resolves to the parent
  repo (claims/ has no `.git`) — the "claims commits" pane label is
  historical. Verified: `claims/.git` absent. Recorded as a display caveat,
  not a bug worth fixing upstream.

## Parked / open

- `fleets/registry.json` full lane→model schema — partly absorbed now
  (registry-check reads it), but route semantics belong to kumitate.
- `fleets/ufo-archive-2026/` (10 subdirs) — historical archive, next-round
  candidate if gaps thin further.
- `george/` stays parked (zero claim-package links).
- Corpus coverage is near-total for `~/Projects/bounties` ops/docs/ledger/
  claims surfaces; remaining depth is per-program claim anatomy (274
  program dirs, sampled ~8) — diminishing returns unless a new pattern
  class appears.

## Live-verification findings (cross-domain, reported not fixed)

- **`ops/registry-check.mjs` is permanently red.** Seven `@role` errors on
  every kx card — but the mechanics bugs are in the checker: nested
  `modelRoles` aliases (`fleet_volume` → `"@ufo_deepseek_max"`) are resolved
  one hop only and keep their YAML quotes; the frozen 2026-09-15 charter
  pins reasoning seats on `devin/swe-2:max` while registry primaries say
  alibaba/xai. A gate that never passes stops being a gate.
- `ops/validate.mjs` is green: `OK (1088 programs, 10 lanes, 0 errors)`.
