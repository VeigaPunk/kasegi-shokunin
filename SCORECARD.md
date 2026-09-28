# kasegi-shokunin — Scorecard

Lane axes per `../MISSION.md`: **depth + coverage** (bounty/security research).
The other four axes (operability, freshness, calibration, adjacency) are worked
by their owning lanes; adjacency evidence from this lane is reported, not
scored here.

Measurement proxies (fixed so before→after is verifiable):

- **coverage proxy** — top-level surfaces of `/home/vgpnk/Projects/bounties`
  (dirs excluding `.git`, plus the 3 root files) that have either (a) a corpus
  entry documenting a full census/full read, or (b) a recorded park
  disposition. Denominator at round 12: **18 items** (15 dirs + README.md +
  2 root zips). Round-13 transparency note: the re-walk reproduced the
  denominator exactly (no new/renamed/vanished dir), but the root actually
  holds 26 files — the 3 counted + `.gitignore` + 22 `.ufo-mission-report-bh*.md`,
  both excluded classes documented in `ufo-workspaces.md`/`repo-git-state.md`;
  counting every file individually the surface set is 41 and coverage is
  41/41 at class granularity. The 18-item denominator stays (by design).
- **depth proxy** — two instruments, both re-runnable: (1) citation-resolution
  rate (r13: 705/708 = 99.6% full-set); (2) per-section evidence density —
  instrument of record `/tmp/kasegi-r14/density.py` (labrat reimplementation
  of the r13 census, calibrated on the exact pre-r13 blob git fc6d398:
  checklist 6/28.6 and anti-patterns 11/29.7 reproduce exactly, mean Δ+0.8,
  all residuals explained — r13's own table arithmetic noise + mutually
  inconsistent date counting). **Bar rule (round-14, fixed):** each repaired
  block must clear the PRE-edit file mean of the same run (r14: 102.5); the
  post-edit mean is self-inflated by the repair itself (142.5) and is NOT
  the bar — compare each block to its own BEFORE. Width sensitivity is
  documented: identical content measures 86.0 as 80-col prose vs 973.3 as a
  single-line-row table, so form must be held constant across measurements.

## Axes

| Axis | Score (before r14) | Score (after r14) | Evidence pointer | Last change |
|---|---|---|---|---|
| depth | 9 | 9 (thin cohort repaired; sub-metrics moved, integer held — see below) | **r14 measured (density.py, same script both sides):** Program-rule checklist **28.6→106.6** (3.7×), Policy access playbook **62.5→462.5** (7.4×), Disclosure anti-patterns **29.7→108.4** (3.6×) — both r13-named thin sections clear the pre-edit mean 102.5 AND r13's recorded 96.5; every checklist bullet, playbook row, and all 10 anti-pattern items now carry per-item `path:line` citations (+ new per-item anchor-map table = r13 repair-3). Claim-hardening prose-only rows re-anchored (123.3→196.7; `ufo-archive-2026.md:145-149`/`:150-154`). Total path-citation instances 275→373. Sampling push: claim-anatomy **10→30/280 = 10.7%** (deterministic stratified `select20.sh`, L1-reproduced; D1-D13 deviation classes → `corpus/knowledge/claim-anatomy-sample.md`). 3 SKILL falsifications repaired in place ("every fix is a disclosure defect" header — 2 NO-GO rows are reproduction gates `docs/wrap-report.md:9,:20-21`; :412 receipt-drift pointers — receipts live in origin-work `submission-review/`, not the two named reconcilers; Immunefi `policy_sha256` overreach — beanstalk provenance has zero hash keys, Immunefi page hashes land as `html_sha256` in keeper telemetry `:181`) + 2 corpus defects (state enum omitted PARKED 248/280; playbook seek-autopsy misattribution) + stale-generated-file annotation (`docs/claim-ready-index.md` on-disk 11 rows vs 12 claim-check-OK — intigriti-yahoo appears only on live regeneration) + telemetry as-of 7225→7227. One critic falsification REJECTED with evidence (decree exists at `fleets/claimer-mission.md:29`; critic grepped only `docs/`; git timeline b3b1b7e3→2ef530c6 proves the override order). **Not 10:** Triage economics 93.3 still below the pre-edit mean (U4 EV-constants lift = r15 plan), Ops integrity 61.1 / Retirement 62.5 / VDP 81.8 blocks unchanged, claim-anatomy census 10.7% not full, keeper "launched 265" not re-derivable (state deleted; annotated UNVERIFIED-by-r14 in reviewer report). | r14 |
| coverage | 9 | 9 (no surface-set change; sub-surface advanced under depth) | proxy denominator stays 18/18 — no new/renamed/vanished top-level surface found this round (no r14 surface walk commissioned; the round worked inside the already-censused `claims/` + `docs/` + `fleets/` surfaces). Claim-anatomy sub-surface 3.6%→10.7% counted under depth, not coverage. Mid-round drift observed and reported, not absorbed: `docs/claim-ready-index.md` mtime-only touch + 2 telemetry appends (`freshness_check` 23:32:22Z, judge-lane `reroute_drill` 23:32:32Z) at 2026-09-28T23:32Z — bytes unchanged (HEAD==worktree, 11 rows both), no cron/timer/live-process match, both L2s alive at that minute attest read-only; actor [UNVERIFIED], reported-not-explained (same treatment as r13's `.git` touches). | r14 |

Not 10 on coverage: `george/` (49G) stays parked-unwalked (disposition
recorded, contents unexplored) and the 805M `.ufo/bounty-fleet/` is
structure+sample censused, not exhaustively read — both deliberate, not
gaps-by-omission.

## Planned

Round 15 candidate: **depth** — finish the r13 thin cohort's last genuine
member: **Triage economics (93.3 < pre-edit mean 102.5)** via r13 repair-4
(U4): lift the concrete EV constants that already exist in the corpus into
the SKILL section — default priors `.7/.7/.25/.6`, effort 60 h, risk 250
(`corpus/knowledge/mission-ledger.md:53-55`, canonical derivation
`triage-thresholds.md`), `ev-report.mjs` exit semantics 0-always/2-on-missing
(`corpus/knowledge/ev-model.md:19-20`) — falsifiable: block dens ≥ pre-edit
mean of the same run, measured with `/tmp/kasegi-r14/density.py` (copy it
into the lane repo if /tmp is swept). Secondary cohort if U4 lands cheap:
Ops integrity 61.1 / Retirement 62.5 / VDP 81.8. Coverage stays 9; the
split into `coverage:claims-pipeline` vs `coverage:target-corpus` remains
deferred; a claim-anatomy census push 10.7%→~20% (+25 reads, same
deterministic rule with a new stride) is the natural first trial of the
`coverage:claims-pipeline` sub-axis. Note: r14's own Planned text cited the
prose-only hardening rows at "SKILL.md:412-413"; the live rows were
:413-414 (pre-r14 numbering) — corrected here, rows now re-anchored.

## Retired

None. (No axis saturated: coverage reached 18/18 surfaces at r12 but sub-surface
depth remains — if a future round finds no un-censused surface class left,
coverage MAY be split into `coverage:claims-pipeline` vs `coverage:target-corpus`
rather than retired.)
