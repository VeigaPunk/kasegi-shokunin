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

## Retired

None. (No axis saturated. `coverage`'s r12 18/18 was destroyed by an external
event, not by exhaustion, so it is re-based rather than retired; `depth` was
split, not retired — see above.)

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 20 | freshness | measured at HEAD (see lesson) | verdicts recorded per gate, no scalar | `corpus/lessons/round-20-recensus.md` |

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
