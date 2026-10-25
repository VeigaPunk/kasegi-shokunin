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

## Round 17 result

| Axis | Score before r17 | Score after r17 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:density | 9 | 9 | Held at the r15 result above; no density move this round. | r15 |
| depth:verifiability | 4 | 4 | `resolve.py` already range-checks resolvable anchors; the pre-edit census records the receipt `:5-6` in range. `anchorcheck.py` now reports `ORIGIN=1` and prints the corrected `SKILL.md:683` range `:5-8`; `MISSING-FILE=46`, `LOST-RECORDED=5`, and `PIN-BROKEN=0` remain. The source is untracked, so this is current-byte evidence only. | r15 (held r17) |
| coverage | 7 | 7 | Held at the r15 result above; no coverage move this round. | r15 |

The round-17 narrative recorded `480/1506`; the round-18 labrat reproduced the
unchanged pre-edit census as **451/1506** = 107 RESOLVES + 224
MIRROR-EQUIVALENT + 120 INTERNAL. The denominator and SKILL row (`222/486`)
matched, so `480` was a numerator transcription error. Round 18 also found
that `resolve.py` ingested its own generated `citation-survival.md` and stripped
leading dots from `.ufo`/`.omp` tokens. The corrected definition excludes that
generated report and preserves leading dots. A complete scratch tree overlaid
with the executor's exact pre-edit SKILL/corpus snapshot supplies the comparable
baseline below; two final runs are byte-identical.

## Round 18 result

| Axis | Score before r18 | Score after r18 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:density | 9 | 9 | Non-target guard only: unchanged instrument, mean **152.9 → 153.9**, path-citation instances **623 → 645**. No density credit claimed; the increase comes largely from making shorthand historical anchors explicit. | r15 (held r18) |
| depth:verifiability | 4 | **4** | `anchorcheck.py SKILL.md`: r17 matcher baseline **196 in-range / 46 bad / 162 distinct / LOST=5 / ORIGIN=1**; broadened r18 matcher on the same pre-edit bytes exposed **205 / 82 / 171 / 5 / 1**; final **209 / 0 / 175 / 104 / 5**, `PIN-BROKEN=0`, `OUTSIDE-BASE=0`. Four exact origin-work receipt anchors now open; all recognized non-openable anchors are explicit rather than silently skipped or reported as unexplained MISSING-FILE. Corrected `resolve.py`: SKILL numerator **228 → 232**, denominator **488 → 503**, so **46.72 % → 46.12 %**; lane total **427/1461 = 29.23 % → 432/1469 = 29.41 %**. Score held: absolute openable set and lane rate improved, but the defined SKILL fraction did not. | r18 (measured, score held) |
| coverage | 7 | 7 | Held at the r15 result; no coverage move this round. | r15 (held r18) |

The independent L2 map classified 79 broad-shape anchors as absent from all
three declared roots and found three exact relative-path survivors in
origin-work; review also resolved the omitted `csv:3` shorthand to the same
receipt CSV. All four new full ORIGIN-WORK ranges were read and semantically
support the receipt claim. Of the original 16 distinct MISSING-FILE paths,
15 are absent from both surviving roots and their git histories; only
`queue.json` has an exact survivor. Name-similar files
(`docs/example-claim-ready-index.md`, `.ufo-missions/groknight/WRAP.md`,
packet `completeness-checklist.md`) were rejected as non-equivalent. The
quoted stale target-repo text `README.rst:706` was de-anchored rather than
mislabelled LOST-TREE. Live files (`SKILL.md`, `corpus/README.md`,
`corpus/knowledge/*.md`) now have zero `MISSING-FILE`, `PAST-EOF`,
`OUTSIDE-BASE`, or `PIN-BROKEN`; pre-r16 lessons retain historical bad anchors
under `citation-bases.md` rule 6.

## Round 19 result — re-census after second root loss (2026-10-14)

Trigger: the OMP/ufo-fsd substrate re-census found that this lane's two
"surviving roots" — `~/Projects/the-bounty-hunter` (frozen mirror) and all of
`~/Projects/origin-work` (incl. `open-bug-bounties`) — are ABSENT
(no relocated copy found under `~`; evidence:
`corpus/knowledge/root-loss-2026-10-12.md`), while `ufo-fsd-alpha` relocated
intact to `~/Projects/ufo-fsd-alpha` @ `964f443e`. This is external drift,
not a lane move; scores are re-reported, not improved.

| Axis | Score before r19 | Score after r19 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:density | 9 | 9 | Non-target guard only: mean **153.9 → 154.0**, path-citation instances 645 → 645 (`[lost-base]` marks do not inflate; same instrument, same form). | r15 (held r19) |
| depth:verifiability | 4 | 4 (held by floor) | `anchorcheck.py SKILL.md` before repair: **7 in-range / 202 bad / LOST=104** — every bad instance traced to the two absent bases; after repair: **7 in-range / 0 bad / LOST-RECORDED=306 / BASE-ABSENT=0 / PIN-BROKEN=0 / OUTSIDE-BASE=0**. `resolve.py` regenerated census: SKILL **32/506 = 6.32 %** (r18: 232/503 = 46.12 %), corpus **116/1142 = 10.16 %**, lane **132/1469 = 8.99 %** — the drop is the domain bases vanishing, measured honestly rather than hidden. | r19 (measured, score held) |
| coverage | 7 | 7 | Held; the two surviving-root surfaces the r15 denominator was re-based onto are now 0/2 present. Both censuses (`the-bounty-hunter` file-granularity, `open-bug-bounties` inventory) remain corpus-attested records. Re-scoping is the operator's (same L0 question). | r15 (held r19) |

**Gate repairs (the re-census work itself):** `anchorcheck.py` +
`resolve.py` now DERIVE their roots (`$KASEGI_MIRROR`,
`$KASEGI_ORIGIN_ROOT` → first existing candidate → canonical absent path);
hardcoded roots removed. New `BASE-ABSENT` verdict (own class, not bad) so
an absent tree never masquerades as a missing file. `resolve.py` records
the mirror's absence in the generated census. Live ufo-fsd citations
re-anchored (`ufo-archive-2026.md:31`, `ufo-workspaces.md` ×2 — the
`hunt-*` dangling claim re-verified against the moved tree; the
`UFO_ROOT=` env value kept verbatim as a quote). 202 SKILL + 39 corpus
anchors into absent bases marked `[lost-base]` under the extended
vocabulary (`citation-bases.md` LOST-BASE); first-loss note gained an
append-only errata; PROVINCE.md, SKILL.md and this file carry factual annotations.

**Carried debt (named, with unblock action):**
- `RECEIPT-STORE-LOST`: `submission-review/` receipts (CSV rows 2–3,
  `queue.json:11-12`, k8s + LD JSON receipts) that backed the no-resubmit
  claims are corpus-attested only; r18-recorded byte SHAs preserved in
  `LOG.md`. Unblock: operator restores the `open-bug-bounties` checkout or
  declares the claims permanently attested.
- `MIRROR-SOURCE-LOST`: every `ops/*.mjs`, `bounty-map/schema.json`,
  `fleets/*`, `docs/*`, `.omp/*` line anchor is now uncheckable; the
  `[lost-base]` prefix is the standing marker. Unblock: restore the
  `the-bounty-hunter` mirror (any checkout of HEAD `1cfbd86` satisfies the
  anchors; `$KASEGI_MIRROR` override re-points the gates without edits).
- `ORIGIN-REPO-LOST`: `origin-work/ufo-fsd-alpha` citations that recorded
  historical state (mtime rows, `UFO_ROOT=` env value) stay verbatim as
  quotes; live claims re-anchored to `~/Projects/ufo-fsd-alpha`. Unblock:
  none needed for lane gates (derived `$UFO_SRC` candidates list the new
  path first).

## Planned

Next candidate: **depth:verifiability** (4 remains below coverage 7).
Audit the recorded severity/decree claims for support in the surviving lane
corpus; both former domain bases are absent, not available for comparison.
Do not replace primary sources with circular corpus citations to raise the
resolution fraction. The explicit-mirror override inconsistency is repaired
in the round-17 continuation below; source restoration remains operator-owned.

**Round-22 planned for round 23** (supersedes the paragraph above as the next plan; that text is kept as history):
1. **depth:verifiability** — reconcile STATE D9 stale resolver cells (`SCORECARD.md` r19 row `132/1469`, `116/1142`) against one Git-export census; before: 2 stale cells, after: 0; command: run `resolve.py` in pre/post scratch exports and `diff` the generated `citation-survival.md`. No internal-citation credit.
2. **coverage** — admit F06–F08 (multi-party CVD S018, CNA rules S022, EU CRA S024) through `corpus/QUALITY.md`; before 0/3, after ≤3/3; command: `grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md`. Adopt the r22 coverage denominator (20 Core + Frontier admitted / total) by explicit claim.

## Retired

None. (No axis saturated. `coverage`'s r12 18/18 was destroyed by an external
event, not by exhaustion, so it is re-based rather than retired; `depth` was
split, not retired — see above.)

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 20 | freshness | measured at HEAD (see lesson) | verdicts recorded per gate, no scalar | `corpus/lessons/round-20-recensus.md` |
| 22 | depth:verifiability | 4 (legacy headers 0/25) | 4 held (headers 25/25, rechecks 25/25 runnable, 23 fail closed; 31 dead-path lines marked) | `corpus/lessons/round-22.md` |
| 22 | coverage | 7 (frontier 0/5, map rows 25) | 7 held (frontier 5/5 admitted, map rows 33) + capability `sources-registry` | `corpus/README.md` § Frontier, `corpus/SOURCES.md` |

## Round 17 continuation — 2026-10-15

The explicit steer reuses round 17 after the recorded round-20 work; prior
round entries are historical and unchanged. Selected lowest axis:
**depth:verifiability (4)**, not coverage 7 or density 9.

| Axis | Before | After | Verdict and evidence | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4** | **Improved measurement correctness**, score held: real copied CLI resolves explicit canonical mirror citations to the selected-root files **0/2 → 2/2**. Frozen SKILL availability remains **32/506 → 32/506** (6.32%, 0 changed verdicts). No restored primary sources or source authenticity claimed. | r17 continuation |
| depth:density | 9 | 9 | **Unchanged**: SKILL bytes identical at both measured commits; no density content or rendering change. | r15 (held r17 continuation) |
| coverage | 7 | 7 | **Unchanged**: PROVINCE bytes and owned surface set identical; missing domain roots are not restored or re-scoped. | r15 (held r17 continuation) |

**Measured before commit:** `4b2e30231c20d3374a39976df5a0f998a6c6f90c`.
**Measured after implementation commit:** `d43e63c8872c4029c7edb9067d8f272642e7885a`.
The later evidence-record commit does not change the measured resolver,
SKILL, or PROVINCE bytes; no self-referential commit hash is asserted.

**Counting command:** `python3 -B -`, with its complete literal stdin in
`corpus/lessons/round-17-mirror-relocation.md` under “Counting command —
both committed resolver revisions”. It executes the real copied CLI twice,
parses its TSV, and counts `RESOLVES` only when the actual resolved path is
the expected relocated file. Observed stdout:

```text
before: distinct=4 resolves=0 mirror=1 internal=0 other=0 gone=3 skill=1/4 corpus=0/0 all=1/4
after:  distinct=4 resolves=2 mirror=1 internal=0 other=0 gone=1 skill=3/4 corpus=0/0 all=3/4
```

The relative control is `MIRROR-EQUIVALENT` on both revisions; the missing
explicit file is `GONE` on both; both CLI exits are 0. The separate
`python3 -B -` command with complete stdin under that lesson's “Frozen
live-input guard” re-derives **32/506** from each committed SKILL/resolver
pair and prints the unchanged SKILL/PROVINCE hashes. Full mutable corpus
census files are intentionally unchanged; documentation additions are not
being presented as recovered source citations.

No axis is retired or split. This is the narrow suffix-join repair named in
`corpus/lessons/round-20-recensus.md:34-35`, not a new restoration or coverage
claim. The pre-existing uncommitted `anchorcheck.py` changes are excluded.

## Round 21 — interactive cutover, blocked before dispatch (2026-10-15)

Actual next round after documented round 20; the old launch counter 17 is
not a verified-round count. The later reused “round 17 continuation” above
is inherited work, not authority to overwrite an earlier round. Its resolver
implementation `d43e63c8872c4029c7edb9067d8f272642e7885a` is preserved.
No preceding completed-round entries or shared ledger rows are rewritten.

Selected lowest LIVE axis: **depth:verifiability (4)**. WWKD:
`plans/wwkd-round-21-authority-audit.md`. The intended severity/decree
authority audit has an exact validated 32-member payload, but **zero
dispatched members**: effective role bindings are generic
`@m_mid`/`@m_fast`/`@m_strong`, not the required composer/grok/antigravity
bindings; `m_antigravity` has no ZFL fallback. No routing overlay was added.
Full alias evidence and gate: `.ufo/rounds/round-21/routing-observation.json`
and `.ufo/rounds/round-21/admission-gate.json`.

| Axis | Before | After | Verdict | Evidence |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 | unchanged | No required audit was dispatched and no new primary source was admitted. Inherited CLI mapping re-proved 0/2→2/2; that is prior implementation evidence, not a round-21 gain. |
| depth:density | 9 | 9 | unchanged | Committed SKILL bytes held; density mean 154.0, 645 citation instances, 18 blocks. `committed-density.json` records command/output/exit 0. |
| coverage | 7 | 7 | unchanged | PROVINCE hash held; no surface restoration, re-scope, or coverage credit. |

**Admission:** `ADMISSION_GATE: BLOCKED failed_requirements=11 verified_round_credit=0`
(exit **1**). Canonical wave plan/render exits **0/0**, 32 members, no task
batch. Passing local behavior: contained resolver suite **10/10**, copied-CLI
smoke exit **0**, revision comparison exit **0**, committed anchorcheck
**7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 /
OUTSIDE-BASE=0 / BASE-ABSENT=0**, exit **0**. Full outputs, not inferred
passes, are under `.ufo/rounds/round-21/`.

**Erratum to the inherited 32/506 claim above:** the old command freezes
SKILL and resolver bytes, but resolves against the mutable working
filesystem. Replayed today it reports **33/506 → 33/506**. Git-exported
inputs report **31/506 → 31/506**; `.git` and the untracked `.ufo/` account
for the two class differences. Both old 32/506 assertions failed (exit **1**)
and are preserved in `frozen-skill-guard.json` and
`snapshot-skill-guard.json`. `revision-comparison.json` prints the class
differences and confirms unchanged frozen maps and SKILL/PROVINCE hashes.
The old filesystem was not snapshotted, so 32/506 is historical, not newly
certified. No source-availability gain is claimed.

**Measured revisions:** inherited before
`4b2e30231c20d3374a39976df5a0f998a6c6f90c`; inherited implementation and
round-open committed input `d43e63c8872c4029c7edb9067d8f272642e7885a`.
Exact counting commands/outputs: `inherited-copied-cli-smoke.json`,
`revision-comparison.json`, `committed-{anchorcheck,density,resolver}.json`
inside `.ufo/rounds/round-21/`. Exported HEAD census:
SKILL **31/506**, corpus **119/1181**, lane **135/1508**. This definition
excludes Git/runtime metadata; it does not silently replace the live census.

**Learning:** expansion unchanged; quality unchanged; discernment unchanged.
No outside spot-check or promotion. `corpus/QUALITY.md` is missing and remains
named conformance debt. No saturation or axis retirement; this is one blocked
interactive attempt, not three consecutive blocked rounds.

**Next:** routing owner supplies authorized effective content→`@m_composer`,
audit→`@m_grok`, connector→`@m_antigravity` with `@m_zfl` fallback.
A fresh UFO L1 session, with the integrator-assigned next monotonic round,
executes the prepared authority audit; no in-session loop or counter reset.
Source restoration and prior named corpus debts remain open. Details and
new-entry corrections: `corpus/lessons/round-21-routing-blocked.md`.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | Curates where kasegi learns: `corpus/SOURCES.md` (contract v1) — opened, scope-tiered rows with anchors, rejected rows with flips, study paths and a search log; all seven contract census commands run clean | `corpus/SOURCES.md`; seven contract census outputs recorded in `corpus/lessons/round-22.md` § Gate (Census block); 27 rows (A=25 C=2; mined=15 queued=10 rejected=2), malformed 0, dup/enum/missing-used-by empty | 22 |

The `sources-registry` capability entered in round 22; the preceding row replaces the rollout's empty repertoire placeholder. New rows require an exercised round demonstration (`AXES.md` §Capabilities).

## Saturation

The lane's saturation line + stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

**Round-22 declaration.** Saturation line: **9/10 on each owned axis**
(depth:density, depth:verifiability, coverage). Stagnation window: **N = 3**
completed, admitted rounds without a capability entry. At 9/4/7 the
lowest-axis obligation stays active; the round-22 `sources-registry` entry
starts the window. Rationale: the r22 planner (two axes far below 9; a lower
line would let the nudge waive the verifiability debt).

## Round 22 — kaika: provenance disclosure + frontier expansion (2026-10-19)

Steered round 22 (round 21 blocked with zero credit consumed 21). Worktree
`kaika/round`, base `94aace2`. Setup (not a claim): `corpus/QUALITY.md` minted —
Q1–Q6 entry criteria and R1–R6 record criteria, each citing its mined mistake in
`corpus/lessons/round-22.md` § Mistakes. Two claims, distinct axes, causally
separable (C1 reads only the 25 legacy entries; C2 reads only the new entries,
registry, index and province).

| Axis | Before | After | Verdict and evidence | Last change |
|---|---:|---:|---|---|
| depth:verifiability (C1, lowest axis) | 4 | **4** | **Improved, score held.** Legacy knowledge entries carrying `source:`/`verified-at:`/`recheck:` (appended end-of-file `## Provenance` block, so no existing line anchor shifts): **0/25 → 25/25** each. `recheck:` lines runnable **0/25 → 25/25**: 23 fail closed (exit 1, base absent), 2 pass (exit 0: citation-bases anchorcheck, root-loss absence test). Dead-path lines carrying a same-line historical marker **0 → 31** (22 named by the r20 audit + 9 still-current how-tos/assertions found by the r22 critic); presence-wording sweep **8 → 5**, the 5 residual hits reviewed benign (past tense, or the relocated `~/Projects/ufo-fsd-alpha`, which is present). Nothing re-verified against a lost base; resolver rise is all INTERNAL and **not credited** (GONE 1383 → 1383). Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims. | 22 |
| coverage (C2) | 7 | **7** | **Improved, score held.** Frontier topics admitted **0/5 → 5/5** (`corpus/README.md` § Frontier F01–F05; F06–F08 queued with opened S-rows). Coverage-map rows **25 → 33**. `PROVINCE.md` Core/Frontier/Adjacent **0 → 3** (classification, not a re-scope). Capability `sources-registry` enters. Score held: the r15 domain-root definition is unchanged by public-practice entries (r22 critic); proposed denominator for adoption next round: 20 corpus-attested Core items + 5 Frontier topics → (20+0)/25 before, (20+5)/25 after. | 22 |
| depth:density | 9 | 9 | **Unchanged, no harm.** 18 pre-existing blocks keep identical nb/cites/tbl/num/sig/ev/dens (block 18's `lines` span 37→38 only, from the blank separator before the new block); new block `Frontier decision table (round 22)` = 155.6 ≥ BAR_R15 142.5 with 7/7 path cites resolving (conjunctive bar met); file mean 154.0 → 154.0. | r15 (held r22) |

**Counting commands** (run from the lane root; the before tree is
`git archive 94aace2`):

```sh
# C1 — legacy headers + recheck exit codes
for k in source verified-at recheck; do n=0; for f in $(git ls-tree --name-only 94aace2 corpus/knowledge/); do grep -q "^$k:" "$f" && n=$((n+1)); done; echo "$k $n/25"; done
for f in $(git ls-tree --name-only 94aace2 corpus/knowledge/); do r=$(grep -m1 '^recheck:' "$f" | sed 's/^recheck: //; s/^on-restoration — //; s/ (fails closed.*//'); bash -c "$r" >/dev/null 2>&1; echo $?; done | sort | uniq -c
# anchors into legacy entries unshifted: every original line is a prefix of its current line
for f in $(git ls-tree --name-only 94aace2 corpus/knowledge/); do git show 94aace2:$f | awk -v F="$f" 'BEGIN{while((getline l < F)>0) c[++n]=l} {if (index(c[NR],$0)!=1) bad++} END{print bad+0}'; done | sort | uniq -c
grep -c 'r22 correction' $(git ls-tree --name-only 94aace2 corpus/knowledge/) | awk -F: '{s+=$2} END{print s}'
for f in $(git ls-tree --name-only 94aace2 corpus/knowledge/); do grep -nE 'the-bounty-hunter|origin-work|open-bug-bounties|~/projects' "$f" | grep -E 'live|LIVE|not gone|moved|surviv|true home|PRESENT|present|exists|still' | grep -vE '\[lost-(base|tree)\]|historical|r22 correction|ABSENT|absent|^[0-9]+:(source|recheck|verified-at):'; done | wc -l
# C2 — frontier, map, province, registry
grep -cE '^\| F0[1-5] .*\| admitted \|' corpus/README.md
awk '/^## Coverage map/{f=1;next}/^## /{f=0} f&&/^\| /{n++} END{print n-2}' corpus/README.md
grep -cE '^## (Core|Frontier|Adjacent)' PROVINCE.md
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   # + the six other contract census commands
# no-harm
python3 corpus/instruments/density.py SKILL.md --label r22; python3 corpus/instruments/anchorcheck.py SKILL.md
```

Resolver (scratch copies only, never the live tree): base `skill=32/506
corpus=140/1212 all=156/1539`, round-22 `skill=39/513 corpus=187/1259
all=203/1586`; every added token INTERNAL, GONE unchanged — reported, not
credited. **Measured before:** `94aace2`. **Measured after:** the round-22
commit (hash in `LOG.md` round-22 entry's successor record and the fleet report;
no self-referential hash is asserted here).

**Provider exhaustion.** The first executor seats (sources, provenance,
entries, index) died or stalled on `resource_exhausted` (free-model rate
limit); they were cancelled and re-dispatched fresh on the re-routed bucket.
No claim was shrunk.

## Round 23 — frozen claims (2026-10-20)

Base: `922a4dde90b60b465e2b8b241d1fe363f1f27e98`. Machine-readable
preregistration: `.ufo/waves/round-23/claims.json`, written before dispatch.
This replaces the r22 next-plan's stale-cell reconciliation as the lowest-axis
claim: editing a reported cell does not improve the registered detector.

1. **C1 depth:verifiability (lowest, score 4): detector soundness.**
   The actual `resolve.py` credits an outside-mirror file as
   MIRROR-EQUIVALENT through a bounty-parent path. Confine bounty and relative
   mirror fallbacks using the same realpath boundary as explicit mirror
   citations, reject prefix-sibling confusion, and measure the real copied CLI
   against the same persisted expected fixture matrix before and after.
   This is instrument correctness, not restored primary sources or a rise in
   citation availability; the score remains 4. Preserve direct-source and
   lane-relative semantics. Frozen pre-round SKILL/corpus outputs and all
   changed verdicts are a required no-harm disclosure.
2. **C2 coverage (score 7): F06–F08 admitted 0/3 → 3/3**, contingent on opening
   official FIRST, current CNA rules, and CRA Article 14/71 text and clearing
   Q1–Q6. Public-practice frontier denominator frozen at eight topics:
   5/8 → 8/8. The historical lost-root denominator and score 7 are not
   redefined. C1 is independently measurable with no frontier entry present;
   C2 is independently measurable with the original resolver.

Round-22 verifier correction: its C1 was REJECTED-HONEST-STOP, not an
admitted depth improvement. The earlier “improved, score held” rows remain
historical author assessments; headers/historical notices are provenance and
freshness work, not detector-defined depth credit. Evidence:
`corpus/lessons/round-22-verifier-spotcheck.md`; learning and routed-debt
closure belong to `corpus/lessons/round-23.md`.

## Round 23 — result (attempt 2, 2026-10-25)

Frozen claims and base are unchanged from `.ufo/waves/round-23/claims.json`
(base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`). Lane tip at attempt start
`1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a`. Neither claim restores a lost
domain source; no axis is redefined.

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest, 4) | escape fixtures credited `MIRROR-EQUIVALENT`: **0/6 GONE**; matrix 7/13, exit 1 (do-nothing control, baseline `922a4dd` bytes) | **6/6 escape GONE, 7/7 controls preserved, matrix 13/13, exit 0** | **Improved, score held 4.** Command: `python3 corpus/instruments/mirror-containment-check.py --resolver .ufo/waves/round-23/c1-baseline-resolver.py --json .ufo/waves/round-23/c1-baseline.json` vs the same command without `--resolver` (`c1-fixed.json`); both print `matrix_sha256=5e61a33e…b5e76a9`, so the inputs are identical. Code: `resolve.py` `bounty_suffix()` exact-root boundary plus `under_mirror()` on the bounty and relative fallbacks. Guard: frozen `922a4dd` export, both detectors → `changed=0 added=0 dropped=0`, `mirror=0` (published as vacuous). Score held: instrument correctness, no source restoration or citation-availability change; the lane-relative `INTERNAL` carve-out is disclosed, not generalized. | 23 |
| C2 | coverage (7) | F06–F08 admitted **0/3**; frontier **5/8**; entry rechecks exit 2 (manifest absent) | **3/3 admitted; frontier 8/8**; rechecks exit 0 for S018/S029/S030 with three failing controls (exit 1/2/1) | **Improved, score held 7.** Commands: `grep -cE '^\| F0[6-8] .*\| admitted \|' corpus/README.md` → **0 → 3**; `grep -cE '^\| F0[1-8] .*\| admitted \|' corpus/README.md` → **5 → 8**; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S0xx` → exit 0 ×3. Entries `knowledge/multiparty-vulnerability-coordination.md` (S018), `cna-assignment-and-vulnerability-rules.md` (S030, supersedes S022), `cra-manufacturer-reporting-duties.md` (S029, supersedes S024). Score held: the r15 domain-root denominator is untouched by public-practice entries. | 23 |

**No axis harmed.** depth:density was not touched this round; the resolver,
matrix and manifest are read-only inputs to `SKILL.md` density except for the new
instrument files outside the density measurement's scope. `SCORECARD.md`'s earlier
r22 rows remain historical author assessments; the r22 verifier's
REJECTED-HONEST-STOP correction stands.

**Capability entry.** `mirror-containment-matrix` — the lane can now replay a
frozen detector matrix on real copied CLI bytes with a do-nothing control, and
fail closed on digest/quote corruption. Exercised this round (**24/24** landed-bytes and
**12/24** do-nothing-control receipts on `matrix_sha256=d05b1e0c…`, three failing
recheck controls). Evidence:
`corpus/instruments/mirror-containment-check.py`,
`corpus/instruments/mirror-containment-fixtures.json`,
`corpus/source-snapshots/round-23/manifest.json`, `corpus/lessons/round-23.md`
§ Attempt 2. First working round: 23. This restarts the r22 stagnation window.

**Wave conformance (honest).** Wave 1 inherited (`kasegi-r23-build`, 64 seats,
committed registry + 44 reports). Wave 2 `kasegi-r23-falsify` (36 seats, 19 attack
roles) validated under the v1 policy and was refused at dispatch by the host job
limit (`Background job limit reached (100)`, all lanes); refusal filed at
`.ufo/waves/round-23/falsify/refusal-1.json`. No seat replaced, split or shrunk,
so this round's fresh attack wave did not run.

### Round 23 — errata after the falsify wave (2026-10-25)

Append-only corrections to the result table above; the earlier cells stand as the
first landing's assessment.

- **C1 measurement superseded.** The finalized matrix has **24 cases (12 escape, 12
  control)**, `matrix_sha256=d05b1e0c…b809`. Do-nothing control (baseline
  `922a4dd` bytes): escape **0/12 GONE**, controls 12/12, 12/24 pass, exit 1. Landed
  bytes: **24/24, exit 0**, `resolver_sha256=690153ad…ea2d`. The earlier "6/6,
  13/13" cells describe the first matrix and are kept as history. The checker now
  also asserts the `resolved_path` column and records `checker_sha256`, and per case the `method` and `domain` the CLI reported; two cases
  (lane-first ordering, mirror-root prefix sibling) exist because mutation seats
  proved the earlier matrix could not see them.
- **C1 scope wording.** The axis move is **mirror-fallback soundness**, not
  "detector soundness": the lane-relative `INTERNAL` branch is unconfined and the
  bounty literal hit is reported as written. Both are pinned as controls
  (`path_tolerance: carve-out` makes the lane escape visible in every receipt) and
  named in `resolve.py`'s policy docstring.
- **C2 sources cell corrected.** F07's admitted authority is **S031** (CNA
  Operational Rules 4.2.6, approved 2026-10-14, effective 2026-10-20), which
  supersedes S030 (4.2.0) and, through it, S022. The r22 plan text above that names
  S022/S024 as the round-23 admission sources is historical; the registry rows
  S022/S024 remain `queued` and their `teaches` cells are unchanged (R8).
- **C2 count command.** `grep -cE` was column-agnostic; the frozen counter is now
  `awk -F'|' '$2 ~ /^ *F0[1-8] / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'
  corpus/README.md` → 8 (F06–F08 variant → 3). Receipts: four rechecks exit 0;
  three failing controls exit 1/2/1.
- **F01–F05 residual debt named.** Their `recheck:` lines exit 2 `not-listed`
  (no capture exists for S001–S015). Not repaired this round; disclosed in
  `corpus/lessons/round-23.md`.
