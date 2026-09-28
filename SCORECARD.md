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
- **depth proxy** — citation-resolution rate: fraction of SKILL.md /
  corpus path citations that resolve against the live tree, plus attached-fact
  spot-check pass rate (first measured round 12 by independent L2 reviewer;
  round 13 measured the FULL set — scripted classifier `/tmp/kasegi-r13/classify5.py`,
  rules in-file: counted citation = backticked token anchored to a live-tree /
  kasegi / origin-work root; excluded classes: layout-fragment, git-ref/tag,
  schema-id, regex-literal, url, data-quote, name-list/command).

## Axes

| Axis | Score (before r13) | Score (after r13) | Evidence pointer | Last change |
|---|---|---|---|---|
| depth | 8 | **9** | **r13 measured:** full-set citation re-audit — 1100 backticked tokens extracted, **708 counted citations, 705 resolved = 99.6%** (anchored-only 438/441 = 99.3%); the 3 broken repaired in place (`raw-rN/`→`raw/`, `B-bounty-fleet/` zip misattribution, dangling `ufo-fsd-alpha/.ufo/missions/hunt-*`). Attached-fact layer: ~106 atomic checks by 7 independent L2 auditors (2 reviewers, 2 critics, sentinel live-run, revenger intent-reconstruction, executor drafter) + L1 full-source derivation → **~30 defects found, ALL repaired in place** ("round-13 correction/addition" markers across SKILL.md + 12 corpus entries; full list: `corpus/README.md` Known-gaps). New canonical entry `knowledge/triage-thresholds.md` — every gate/constant/weight line-cited, **3-way verified with zero model disagreement** (L1 full read × executor draft × reviewer derivation). r12's 10 repairs: 10/10 numerals CONFIRMED; 2 regressed "19 missions" lines caught+fixed. Sentinel live re-run: 18 MATCH / 4 SKILL-WRONG (repaired) / 0 DRIFT. Audit artifacts: `/tmp/kasegi-r13/` (10 reports + classifier + outputs). Not 10: sampling residuals (claim anatomy ~3.6%; anti-patterns 1 header cite for 10 items) and audits are point-in-time. | r13 |
| coverage | 9 | 9 (verified, denominator reproduced; transparency note above) | proxy 18/18 re-walked round 13: no new/renamed/vanished top-level surface; honest drift recorded instead — `ledger/telemetry.jsonl` live-appends on every `check-freshness.mjs:61` run (7225 lines as of 2026-09-28T21:52:51.978Z; audit runs are appenders), r13 counts carry as-of stamps; 4 unexplained mtime-only touches on `.git` dirs at 18:34/18:37 reported-not-explained (`/tmp/kasegi-r13/scout-drift.md`) | r13 |

Not 10 on coverage: `george/` (49G) stays parked-unwalked (disposition
recorded, contents unexplored) and the 805M `.ufo/bounty-fleet/` is
structure+sample censused, not exhaustively read — both deliberate, not
gaps-by-omission.

## Planned

Round 14 candidate: **depth** — with a corrected premise. The r13 thin-section
census falsified this scorecard's r13 plan ("finding-triage table = thinnest
re-verification margin"): citation-density ranks that table #14/18 (121.9 vs
mean 96.5, all 7 rows concrete+cited). The real thin cohort: **Program-rule
checklist (density 28.6)** and **Disclosure anti-patterns (29.7 — 10 numbered
items behind a single header cite to `docs/wrap-report.md:345`; the source's
per-package GO/NO-GO rows at :13-23 are uncited)**, plus the two prose-only
Claim-hardening rows (SKILL.md:412-413 post-r13 numbering; exemplars exist at
`ufo-archive-2026.md:143-148`). r14 move = per-item citations for both
sections (falsifiable: density ≥ mean) + optional claim-anatomy sampling push
(3.6%→~10%: 20 more `status.json` full reads). Coverage stays 9; the split
into `coverage:claims-pipeline` vs `coverage:target-corpus` remains deferred
until no un-censused surface class is left.

## Retired

None. (No axis saturated: coverage reached 18/18 surfaces at r12 but sub-surface
depth remains — if a future round finds no un-censused surface class left,
coverage MAY be split into `coverage:claims-pipeline` vs `coverage:target-corpus`
rather than retired.)
