# kasegi-shokunin — Scorecard

Lane axes per `../MISSION.md`: **depth + coverage** (bounty/security research).
The other four axes (operability, freshness, calibration, adjacency) are worked
by their owning lanes; adjacency evidence from this lane is reported, not
scored here.

**Round-15 structural event, read this first.** The lane's PROVINCE root
`~/Projects/bounties` was removed from the filesystem at
2026-09-28T23:51:31Z (actor UNDETERMINED, data PRESUMED-LOST locally). Both
scored axes are measured against that fact from round 15 on:
`corpus/knowledge/source-tree-loss-2026-09-28.md` is the evidence of record
(detection commands, disappearance window, per-file mirror provenance,
forensic blind spots, the never-re-verifiable DATA-half list). Two roots
survive: the frozen 2026-09-05 code mirror `~/Projects/the-bounty-hunter`
(HEAD `1cfbd86`, 34 files) and `~/Projects/origin-work/open-bug-bounties`
(26 claim packages, `submission-review/` receipts, 43 `.ufo-missions`,
`data/*.json` inventories).

## Measurement proxies (instruments are committed, not /tmp-resident)

All three live in `corpus/instruments/` with their definitions and known limits
in `corpus/instruments/README.md`:

- **depth:density** — `corpus/instruments/density.py <file> --label X`:
  per-block `ev = path-cites + concrete-table-rows + unique-numerics +
  unique-ALL-CAPS-signatures`, `dens = ev*100/nb`. Continuity proven this round
  by an independent L2 reimplementation across three blobs: pre-r13 `fc6d398`
  reproduces r13's recorded mean 96.5 and all four block values; pre-r14
  `7483333` reproduces r14's bar 102.5 and 28.6/29.7/62.5; the live file
  reproduces all 18 BEFORE-r15 values including mean 142.5. Form-sensitivity is
  documented and measured (identical content: 93.3 prose vs 150.0 table).
- **depth:verifiability** (NEW round 15) — `corpus/instruments/resolve.py
  <lane-repo>`: fraction of distinct path-like citations that resolve on disk
  (`RESOLVES` + `MIRROR-EQUIVALENT` + `INTERNAL`), plus
  `corpus/instruments/anchorcheck.py <file>` which proves every mirror
  `path:line` is in range and prints the cited source line for semantic review.
  Census of record: `corpus/instruments/citation-survival.md` (+ `.tsv`).
  Definition-sensitive by construction — three r15 implementations agreed on
  direction, disagreed on absolutes (45.68 % instrument-of-record vs 6.9 %
  strict-live vs 48.2 % concrete-shaped) — so the definition travels with the
  number.
- **coverage** — top-level surfaces of the domain root that have either (a) a
  corpus entry documenting a full census/full read, or (b) a recorded park
  disposition. Round-15 denominator change: the 18-item r12 denominator is now
  **0 present / 18 corpus-attested**, and the surface set is re-based onto the
  two surviving roots (2 items) + the attested 18. Recorded below, not hidden.

**Bar rule (round-15 amendment).** `BAR_R15 = 142.5` is a **frozen declared
constant** = the pre-edit file mean measured at round-15 start. It is not
re-derived post-edit (self-inflating/circular — r14 finding) and not re-derived
per round from the current mean (a compounding survivorship ratchet: 96.5
pristine → 102.5 r14 → 142.5 r15 → ~167.5 projected r16, which loads the most
demand onto exactly the blocks a prior round left thin; both the r15 critic and
labrat derived this independently). From round 16 the bar is **conjunctive**:
a repaired block counts only if `dens ≥ BAR` **and** ≥ 60 % of its path
citations resolve — because density alone rewards citing files that no longer
exist (mutation-tested blind spot: a fabricated `path:line` scores identically
to a real one).

## Axes

| Axis | Score (before r15) | Score (after r15) | Evidence pointer | Last change |
|---|---|---|---|---|
| depth:density | 9 | **9** (held: 4 blocks repaired, mean up, bar NOT cleared — recorded, not gamed) | `density.py` on `SKILL.md`, same script both sides: file mean **142.5 → 152.9**, path-citation instances **376 → 623**. Repaired blocks: Triage economics **93.3 → 131.4**, Ops integrity **61.1 → 111.5**, VDP **81.8 → 117.4**, Retirement **62.5 → 93.0**. `BAR_R15 = 142.5` not cleared by any of the four in prose form; the lane publishes that instead of reformatting (identical old content measures 100.0 as prose vs 150.0 as a table, so clearing the bar by form alone is possible and proves nothing). New source-backed content, not padding: the `rank.mjs` run contract + 7-row admission table (`ops/rank.mjs:46-49`, `:92-96`, `:105-108`, `:151`, `:161-165`, `:175`, `:178-190`, `:200-204`, `:209-219`, `:247`), the default-prior break-even arithmetic (0.0735 × `reward.min` − 1750 → break-even `reward.min > 23 809.52`; observed max 10 000 → **−1015**, so every default-basis program is negative-EV and the `:123` sort degenerates to `reward.min` desc), the `expected_reward` two-sources trap (`ops/rank.mjs:92`/`:104` vs `ops/ev-report.mjs:78`), the `TELEMETRY_EVENTS` decorative-whitelist finding (8 declared, 0 importers, 17 appended event names, 4 whitelisted), the do-not-run-in-place hazard (11 scripts, `root` from `import.meta.url`), and runnable-verified exit semantics (byte-identical copy smoke run: exit 2 / exit 2 / WARNING+UNKNOWN+0 / strict `> 0` / the 514 record reproduced). 5 defects repaired: autopsy "five-part" → **seven** (`ops/park-disposition.mjs:56-59` + `:61`,`:67`,`:72`), `bounty-map/schema.json:32-51` → `:32-52`, `triage-thresholds.md`'s 32 `SKILL.md:NNN` cites pinned to blob `fc6d398` (8/8 sampled spans verified), 2 unsupported `ops/claim-index.mjs:4` cites marked `[lost-tree]`, 1 past-EOF corpus cite annotated. | r15 |
| depth:verifiability | 2 (first measurement this round: 16.26 % SKILL) | **4** (45.68 % SKILL, 28.53 % lane) | `resolve.py` census of record `corpus/instruments/citation-survival.md`: SKILL.md **47/289 = 16.26 % → 222/486 = 45.68 %**; corpus **129/971 = 13.29 % → 396/1297 = 30.53 %** (the corpus jump is new mirror-anchored files — `source-tree-loss-2026-09-28.md`, `lessons/round-15.md`, `instruments/README.md` — not repaired old ones); lane total **156/1107 = 14.09 % → 410/1437 = 28.53 %**. Fixed point disclosed, not chased: these files cite each other, so each recording pass moves the rate < 0.1 pp; the committed census file is authoritative. `anchorcheck.py` over the whole of `SKILL.md`: 194 in-range mirror citation instances, **0 past-EOF** (the 47 MISSING-FILE are lost-tree/package-relative anchors the mirror never contained). Not higher: **704 genuine citations point at files that no longer exist** (the r13/r14 rate was 705/708 = 99.6 % resolved — the proxy did not change, the filesystem did), 21 corpus knowledge files carry 765 lost-tree `path:line` cites of which only 1 file is anchor-base-pinned so far, and mirror name-survival ≠ content survival (2 corpus cites are past the mirror EOF; `ops/claim-check.mjs` is 83 lines/19 `err(` sites vs the live 233/48). | r15 (axis split this round) |
| coverage | 9 | **7** | Denominator moved under the axis: the r12 18-item surface set is **0/18 present**, 18/18 corpus-attested as-of 2026-09-28T23:32Z (`source-tree-loss-2026-09-28.md` §3 lists every surface with its recorded census). Two surviving roots entered the province and are only partly covered: `~/Projects/the-bounty-hunter` **censused this round** at file granularity (34 files, 8 dirs, per-file `wc -l` + sha256 + provenance verdict for 11 files, full reads of `ev-report.mjs`/`park-disposition.mjs`/`shared.mjs`, targeted reads of `rank.mjs`/`fleet-dispatch.mjs`/`validate.mjs`/`registry-check.mjs`/`check-freshness.mjs`/`reroute-drill.mjs`/`claim-check.mjs`/`sighting.sh`/`schema.json`/`mission-template.md`) = 1/2; `~/Projects/origin-work/open-bug-bounties` **top-level inventory only** (26 package dirs + 3 files, 0 `status.json`, `submission-review/claims` 21 entries, 43 `.ufo-missions`, 5 `data/` inventories, git HEAD `1307b8b`) = 0/1 censused → the round-16 move. Not lower: no surface that still exists is unexplored without a recorded disposition, and the 18 attested censuses are intact. | r15 |

### Axis split recorded (AXES.md:20-24)

`depth` was split into **`depth:density`** and **`depth:verifiability`** at
round 15, on evidence: the two sub-metrics moved in **opposite directions**
this round (density up 142.5 → 152.9 with four blocks repaired; verifiability
collapsed from 99.6 % citation resolution to 45.68 % because the cited tree was
deleted), so a single integer hid the state that actually matters — whether a
reader can open what the skill cites. Splitting exposes a *worse* number rather
than concealing it, which is the test for whether a split is honest. No axis
retired.

## Planned

Round 16 candidate: **depth:verifiability** (lowest scored axis at 4).
Concrete move: anchor-base-pin the remaining **20** `corpus/knowledge/*.md`
entries the way `triage-thresholds.md` was pinned this round (each gets a
header naming its base — mirror `1cfbd86`, `[lost-tree]` as-of
2026-09-28T23:32Z, or origin-work — and every `SKILL.md:NNN` cross-cite is
pinned to a git blob), then re-run `resolve.py` + `anchorcheck.py` and publish
before → after. Falsifiable target: lane resolvability 28.53 % → ≥ 40 % with
zero past-EOF anchors in `corpus/knowledge/`. Secondary (same round if cheap):
move the `TELEMETRY_EVENTS` decorative-whitelist derivation into its canonical
home `corpus/knowledge/ops-invariants.md` (distiller's ownership map:
`/tmp/kasegi-r15/distiller.md`, 66 duplicate statements across 4 files,
22 CODE-half vs 14 DATA-half facts), and repair `## Pipeline` (13.3, the last
block below 100 — 2.3× below bar; per-stage cites to
`fleets/mission-template.md` + the mirror ops files). Coverage follow-up:
census `~/Projects/origin-work/open-bug-bounties` (the one surviving root still
uncensused) — that is the natural first trial of a `coverage:surviving-roots`
sub-axis, and the `coverage:claims-pipeline` vs `coverage:target-corpus` split
stays deferred until a live claims pipeline exists again.

## Retired

None. (No axis saturated. `coverage`'s r12 18/18 was destroyed by an external
event, not by exhaustion, so it is re-based rather than retired; `depth` was
split, not retired — see above.)
