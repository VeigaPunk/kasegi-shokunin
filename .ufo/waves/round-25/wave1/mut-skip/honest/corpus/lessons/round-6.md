# Round-6 lessons

Round: 6 (2026-09-28). Evidence: `LOG.md` round-6 entry, commit `round-6`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-6/kasegi.md`.

## What I closed

- **`ops/park-disposition.mjs` + `docs/autopsies/` →
  `knowledge/retirement-autopsies.md`.** The retirement half of the
  pipeline was the last undocumented ops surface: classifier precedence
  (LEARNED → RETRY_METHOD → RETIRE_AUTH → RETRY_TRANSIENT → REVIEW),
  autopsy schema + requeue procedure (delete autopsy AND status file),
  and the 31-autopsy sub-cause partition (SPA auth-wall ×27, terms-gate,
  privacy stop, paused/non-enumerable).
- **Found a live fleet defect, not just docs:** re-running the exact
  classifier over today's `fleets/run/` puts 85 parked missions in
  REVIEW (no-action) because their `detail` strings use newer wording
  ("no exact in-scope assets", "custodian HARD_STOP") outside the AUTH
  regex. `status.json.detail` is a machine-consumed field; corpus rule
  now recorded: embed a literal classifier keyword when parking.

## Friction

- None blocking. `PUT >N*:` on a prose line warned and fell back to
  plain gap insert — landed correctly, verified by re-read.
- `uniq -c` over wrapped `Reason (verbatim)` lines undercounts repeated
  causes (lines differ mid-sentence); classify by the "Why"/keyword
  level, not raw string equality.

## Parked / open

- **Actionable upstream finding, not landed:** the AUTH/REVIEW regex
  drift is a real `~/Projects/bounties` ops defect — outside this repo's
  write scope; reported to orchestrator via the round-6 report
  (cross-domain evidence, per PROVINCE.md).
- `fleets/registry.json` lane→model routing — still likely cross-domain.
- `fleets/ufo-archive-2026/` (10 subdirs) — historical archive; next-round
  candidate if gap hunt thins.
- `george/` stays parked (zero claim-package links).
