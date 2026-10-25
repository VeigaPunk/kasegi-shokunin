# Round 11 lessons — intake surface

## What worked

- **Counting beats reading for a 1088-file dataset.** A five-line Python
  census over `bounty-map/programs/*.json` surfaced the decisive facts in one
  pass: `mission_state` DISCOVERED×1087, `lane` executor×1088, `ev_inputs`
  ×1, `reward` ×48, one `refresh_run_id` for everything. Reading samples
  first would have hidden all of it.
- **Cross-referencing directory sets exposed the split-brain.** Joining map
  ids against `evidence/` and `claims/` basenames is what revealed the
  second intake path (22 map-less claim dirs incl. 7/12 queue rows) and the
  name-drift pairs (spacex, github-bounty). Id joins across trees are
  lossy — name normalization is required.
- **Reading the queue scorer rather than trusting field names.** The map
  looks like a state machine, but `programState()` is only a dry-run log
  read; `buildQueue` scores only priority/continue/curated/reward.min. The
  schema's 12-state enum is aspirational — 10 values never populated.
- **Registry as decree ledger.** The "possibly cross-domain" item turned
  out in-domain: `operator_decrees` answers disposition *why* questions
  (3cx never-filed, intel hold, freebie attribution flip) that claim files
  only hint at. Per-key `superseded` markers are the version control — the
  file accretes contradictions, never revises.

## Friction

- `hashline` PUT with a multi-line `+-`/`++`-leading body can mis-apply when
  the range wasn't refreshed after a same-input prior op — one directive
  line leaked into the file; repaired via CUT + single-line PUT. Lesson:
  after any edit response that includes a warning, re-read the touched
  region before continuing.
- `check-freshness.mjs` has been exit-1 for 14 days (358 h vs 26 h): an
  always-on alarm is indistinguishable from no alarm. Noted, not fixed —
  board refresh is the bounties owner's call.

## Residual gaps

- `george/` stays parked. `.ufo/bh*/` mission workspaces, `sessions/`,
  `.ufo/bounty-fleet/`, and `grok-bounty-assessment-20260911` remain
  un-censused — likely working dirs, but unverified.
- The 18-deferred/queued ~80-program frontier in
  `.ufo-ingestion/cycle-20260914T171257Z.md` is enumerated for whoever
  revives the intake cycle; the bounties-side gap (no cycle 2, no map
  records for ingestion claims, dead tracker) is cross-domain — reported,
  not fixed.
