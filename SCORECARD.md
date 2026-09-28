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
  2 root zips).
- **depth proxy** — citation-resolution rate: fraction of SKILL.md /
  corpus path citations that resolve against the live tree, plus attached-fact
  spot-check pass rate (first measured round 12 by independent L2 reviewer).

## Axes

| Axis | Score (before r12) | Score (after r12) | Evidence pointer | Last change |
|---|---|---|---|---|
| depth | 8 | 8 (measured baseline + repairs; see below) | `SKILL.md` (18 sections: decision tables w/ real thresholds, gate semantics from full source reads of `ops/claim-check.mjs`+`ev-report.mjs`+`fleet-dispatch.mjs`, 10 observed anti-patterns); 19 `corpus/knowledge/` entries, every claim path-cited. **r12 first measured baseline:** independent L2 audit of 74 citations → 64 OK / 9 spot-mismatch / 1 broken (86.5% clean); all 10 defects repaired in place (marked "round-12 correction"); critics falsified 2 more prior claims (claims denominator 275→274; bh audits 21-all-BLOCKED→22: 20/2-READY), both repaired. Audit table: `/tmp/kasegi-r12/reviewer.md` (re-audit of repairs appended there) | r12 |
| coverage | 7 | 9 | proxy 13/18 before r12 (11 walked + `george/` park + zips dated-snapshot disposition); gaps were the `.ufo/` workspace layer (1.5G: bounty-fleet 805M, sessions 117M, 25 `bh*` workspaces, grok-assessment, claim-recovery), `.omp/`, `pendle-core-v2-public/` (discovered mid-round, never previously named), root `README.md` → closed r12 via `corpus/knowledge/ufo-workspaces.md` + `repo-git-state.md` + `target-checkouts.md`; **18/18 after** | r12 |

Not 10 on coverage after r12: `george/` (49G) stays parked-unwalked
(disposition recorded, contents unexplored) and the 805M `.ufo/bounty-fleet/`
is structure+sample censused, not exhaustively read — both recorded as
deliberate, not gaps-by-omission.

## Planned

Round 13 candidate: **depth** — the r12 audit measured 86.5% clean and all 10
defects were repaired this round; r13 move = independent re-audit of the full
citation set (target ≥95% clean, falsifiable) + re-derive the finding-triage
decision-table thresholds from `claim-check.mjs`/`ev-report.mjs` source (the
thinnest re-verification margin in SKILL.md). Coverage stays at 9: 18/18
surfaces censused, sub-surface exhaustive reads (bounty-fleet sessions/scopes,
george) deliberately open.

## Retired

None. (No axis saturated: coverage reached 18/18 surfaces at r12 but sub-surface
depth remains — if a future round finds no un-censused surface class left,
coverage MAY be split into `coverage:claims-pipeline` vs `coverage:target-corpus`
rather than retired.)
