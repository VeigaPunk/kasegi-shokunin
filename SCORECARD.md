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

**Round-26 planned for round 27** (supersedes the blocks above as the next plan; that text is kept as history). The round-26 plans were taken up as this round's frozen claims C1/C2 (gate-conformance receipt `.ufo/waves/round-26/c1-receipt-index.txt`; F11 frontier admission in `corpus/README.md`). The plan rows below are plans, not commits:
1. **depth:verifiability** (lowest non-retired, 4) — continue instrument soundness on the routed debt named in round 25: make `anchorcheck.py` exit nonzero on unverifiable verdicts and give `CITE` a `~/Projects/bounties/` arm, measurable by the fraction of fail-closed lines that check citations. No internal-citation credit.
2. **coverage** (7) — continue the frontier from the open leads (`corpus/SOURCES.md` § Leads: ISO/IEC 29147/30111 standard records at iso.org), contingent on opening them and clearing Q1–Q6, registering the source rows first.

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

## Round 24 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-24/claims.json` (base
`d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`, lane tip at attempt start `c2480b1`).
The round fixes the two defects the round-23 verifier routed to this lane and
takes one assimilation admission.

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | frontier rechecks exit 0: **3/8** (F01–F05 exit 2 `not-listed`); dispatch matrix **4/8 exit 1** on round-23 bytes | **8/8** and **8/8 exit 0**; with F09's two entries counted, harness **10/10** | **Improved, score held 4.** Counter A (frozen shell form, cwd-pinned, `c1-counterA-shell-{before,after}.txt`): `3/8 → 8/8`. Harness `frontier-recheck-count.py` (`c1-counterA-{before,after}.json`): `3/8 → 10/10`, exit 0. Counter B: baseline bytes `690153ad…` `cases=8 pass=4 exit=1` (`c1-control-baseline.txt`), landed bytes `db5e0767…` `cases=8 pass=8 exit=0` (`c1-fixed.txt`); round-23 containment matrix still `24/24 exit 0` (`c1-containment-regression.txt`). Do-nothing control cannot meet either target. | 24 |
| C2 | coverage (7) | frontier admitted **8**; entries citing a row first registered this round **0** | **9** admitted; **2** entries | **Improved, score held 7.** `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → **8 → 9** (F09). Entries: `authorised-testing-rules-of-engagement.md` (S032) and `statutory-authorization-and-unauthorized-access.md` (S033/S034/S035); counter B corrected by erratum (below): `grep -lE '^source: S03[2-5] ' corpus/knowledge/*.md \| wc -l` → **0 → 2**. Registry **31 → 35** rows (A 29→32, B 0→1; mined 19→23), census exit 0. Refused with reason + flip: `chinese-criminal-thresholds-and-authorisation.md`. | 24 |
| depth:density | 9 | 9 | 9 | **Unchanged, no harm.** `density.py SKILL.md` → mean **154.0**, 652 path-citation instances, 19 blocks, exit 0; `SKILL.md` bytes untouched this round. `anchorcheck.py SKILL.md` → `0 bad`, `LOST-RECORDED=306`, exit 0. | r15 (held r24) |

**C1 scope, named by surface.** Two verifiability instruments: the captured-source
rechecker's manifest coverage for S001–S015 (nothing was captured, so five entries
could only fail closed) and `resolve.py`'s brace/glob dispatch (an empty brace
alternative was dropped; a glob credited `matches[0]` even when it was a dangling
symlink; a brace alternative carrying a `<...>` placeholder was never globbed).
The change is confined to those two instruments plus the CLI guards that stop the
`--help`-as-lane-root census overwrite and an empty-run census write.

**Errata (append-only; filed before the after-measurement).**
1. `frozen_at_utc` in `claims.json` says `2026-10-25T00:00:00Z`; the file's real
   creation time is `07:09:47Z` (wave-1 reviewer receipt). The date is corrected
   here; the freeze still precedes every measurement in this table (first receipt
   `07:09:56Z`).
2. Counter B's frozen command `grep '^source: S1[0-9][0-9] '` assumed the package's
   numbering. Adopted ids continue the registry from S031 → **S032–S035**, so the
   command can never match; the *predicate* (two entries, each citing a row first
   registered this round) is unchanged and is measured by `S03[2-5]`. A frozen
   command that mis-measures its own predicate is a defect in the instrument, not
   a reason to bend the ids (ids follow the document — CORPUS rule 2).
3. The wave-1 `LivenessMatrix` item's L4 (dangling *brace* alternative) could not
   fail the baseline: `brace_expand` already tested `os.path.exists` per
   expansion. The landed matrix's L4 keeps that citation as a post-fix guard and
   adds a bounty/mirror empty-alternative citation, which is what fails on the
   baseline; the receipt prints both citations per case.

**Known blind spot (R11, published not hidden).** Neither matrix has a case with
more than four brace alternatives: a mutant lowering `brace_expand`'s
64-combination bound to 8 scores `8/8` on the dispatch matrix and `24/24` on the
containment matrix while flipping real verdicts (measured round 25 on the landed
bytes: mutant `88122e10…`, `.ufo/waves/round-25/d24-3/receipt.txt`; the
round-24 receipt only measured the baseline base, `4/8`). Degenerate instruments
are separated: always-GONE `1/8`, always-RESOLVES `0/8` (the artefact's own
label, `.ufo/waves/round-24/wave1/LivenessMatrix.md:200-201`).

## Round-24 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| frontier-recheck-harness | Re-verify every admitted Frontier entry from committed captures, with the entry bound to its own recheck line (header sources covered, selections cited, manifest listing them), and score it as `entries=K pass=P exit=0|1` | `corpus/instruments/frontier-recheck-count.py`; `c1-counterA-after.json` (10/10), `c1-counterA-before.json` (3/8) | 24 |
| source-capture | Capture a public document to a committed, hash-pinned text snapshot with a deterministic conversion and a selftest, then assert located quotes offline | `corpus/instruments/capture-source.py` (selftest exit 0), `corpus/source-snapshots/round-24/manifest.json` (19 records, 76 assertions, exit 0) | 24 |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With
depth:verifiability at 4 the lowest-axis obligation stays active.
## Round 25 — frozen claims C1/C2 (2026-10-25)

Frozen at `.ufo/waves/round-25/claims.json` (2026-10-25T08:13:38Z, base `b49948f`).
Counter instrument: `corpus/instruments/recheck-audit.py`, one digest for every receipt,
`c3c19adc…`; receipts `.ufo/waves/round-25/c1-receipt-index.txt`. The round repaired the
counter after a mutation-tester showed the frozen three-limb predicate reachable without
doing the work (`cd <lane> && true` etc.) — a post-freeze counter repair, disclosed in the
report, with the frozen numbers reported beside the strict ones.

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | `lines=35 pass=6` — 23 `broken` (prose hybrids, `bash -n` fails), 6 cwd-dependent, `executes=12 gated=0 broken=23`, exit 1 | frozen surface `lines=35 total=35 pass=35 strict=35`; final tree `lines=37 total=37 pass=37 strict=37`; `executes=14 gated=23 broken=0`, exit 0 | **Improved, score held 4.** Counter (one instrument): before `pass=6` → frozen surface `pass=35` → final tree `pass=37`, all strict limbs green. Independent re-derivation matched 35/35 verdicts with 0 disagreements. Do-nothing control `pass=6` cannot meet the target; mutants M1–M4 each flip exactly one limb (`c1-controls/`). Nothing the counter measures moved a detector: `resolve.py`/`anchorcheck.py`/`source-recheck.py` bytes untouched. | 25 |
| C2 | coverage (7) | frontier admitted **9**; entries citing a row first registered this round **0** | **10**; **2** | **Improved, score held 7.** `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` → 9 → 10; `grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md \| wc -l` → 0 → 2; registry 35 → 40 rows (census exit 0); `frontier-recheck-count.py` `entries=12 pass=12 exit=0`. F10 entries re-grounded from captures S036–S040 (manifest 5 records / 40 assertions, all `occurrences=1`). | 25 |
| depth:density | 9 | 9 | 9 | **Unchanged, no harm.** `density.py SKILL.md` mean **154.0**, 652 path-citation instances, 19 blocks (identical to the pre-round receipt); `anchorcheck.py SKILL.md` `bad=0`, `LOST-RECORDED=306`; `SKILL.md` bytes untouched. | r15 (held r25) |

**C1 speed, named by surface.** The entry-granularity verifiability instrument: every
`corpus/knowledge/*.md` entry's own `recheck:` line. Before, 29 of 35 lines could not be
used to re-derive the entry's evidence (23 could not run at all; 6 depended on the ambient
cwd). After, all 35 are one cwd-independent command; 23 stay fail-closed on absent bases and
14 execute today. The score is held at 4 because the axis's score is the detector
(`resolve.py`/`anchorcheck.py` census), not the form; the round's critic argued the same
independently (`wave1/CritC1Axis.md`). The 23 fail-closed lines record the lost bases of
2026-09-28 / 2026-10-12; they cannot re-verify until an operator restores or re-points those
roots (L0 kasegi round-15 row).

**Counter repair, in the round's own words.** `claims.json` frozen three limbs; a
mutation-tester found the target reachable by degenerate lines; four strict limbs and a
completeness rule were added beside the frozen three (never replacing them); the do-nothing
control and the mutants are receipts in `c1-controls/`. A critic's vacuity findings (limb (b)
is equality, not success; `pass=35` counts form, not re-verification) are published in the
lesson and report, and the `executes/gated/broken` classes make the limit visible in every
receipt.

## Round-25 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| recheck-audit | Audit every corpus entry's `recheck:` line for command form, cwd-invariance and entry binding, with one isolating fixture per limb (14 selftest cases), a do-nothing control, and `executes/gated/broken` classes | `corpus/instruments/recheck-audit.py`; `c1-receipt-index.txt`; `c1-controls/` | 25 |
| source-capture-round-25 | Re-ground five public documents into hash-pinned snapshots and assert 40 located quotes exactly once with an offline manifest recheck | `corpus/instruments/capture-source.py`; `corpus/source-snapshots/round-25/manifest.json` + `source-recheck.py` | 25 |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With
depth:verifiability at 4 the lowest-axis obligation stays active. Planned round 26:
C1 verifiability — make `anchorcheck.py` exit nonzero on unverifiable verdicts and give
`CITE` a `~/Projects/bounties/` arm (the routed debt above, measurable by the fraction of
fail-closed lines that check citations); C2 coverage — continue F10 with the
ISO/IEC 29147/30111 division-of-labour theme only after registering its staged rows.

## Round 26 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-26/claims.json` (freeze commit
`1b076fa7f2fb5e7dd9d87449514eba526043421b`, base `b76676e`, frozen_at_utc
`2026-10-25T12:27:41Z`). Receipts land under `.ufo/waves/round-26/` (C1
receipt index `c1-receipt-index.txt`, controls `c1-controls/`).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | frozen baseline: registry row 0; selftest receipt lines 0; fix-control #3 hits excluding historical 1; deletion-fixture exit 0 (36/36 lines) | claim targets: registry row ≥1; selftest receipt line 1; fix-control hits 0; deletion exit 1 naming the deleted entry | **Score held 4 — gate conformance round**: recheck-audit.py registered as a gate\|probe row in SKILL.md (verdict map, `--selftest` spelling, pinned-value path, write scope, owner); committed selftest receipt line `selftest cases=… failures=0` at the instrument's own sha256 in `c1-receipt-index.txt` (fixes R25-2 cross-reference); fix-control #3 restated to exclude the retained historical `round-24.md:77` line (R25-4); deleting a whole corpus knowledge entry makes the audit exit 1 naming the missing entry. The round proves gate conformance, not a higher score. Evidence pointer: `.ufo/waves/round-26/c1-receipt-index.txt`. | 26 |
| C2 | coverage (7) | frozen baseline: frontier admitted 10; entries citing a row first registered this round 0 | claim targets: frontier admitted 11; entries citing a first-registered-this-round row ≥1 | **Improved, score held 7**: F11 admitted in `corpus/README.md` § Frontier (ISO/IEC 29147/30111 division-of-labour theme, assimilation package; entry paths `knowledge/iso-29147-and-30111-division-of-labour.md`, `knowledge/iso-29147-divergence-and-clause-crosswalk.md`). S041 registered this round (JPCERT/CC 2026 P-guideline capture; snapshot `corpus/source-snapshots/round-26/S041.txt`, sha256-bound quotes in `manifest.json`). Sources census exits 0 at round close (cadence-only recheck cells restored; E09/E11 cleared). Evidence pointer: `corpus/README.md` § Frontier (F11). | r26 |
| depth:density | 9 | 9 | 9 | **Unchanged, no harm.** `density.py SKILL.md` measured at scribe time (before the C1 registry-row edit to SKILL.md lands): mean **154.0**, 652 path-citation instances, 19 blocks; `anchorcheck.py SKILL.md` `bad=0`, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`, exit 0. | r15 (held r26) |

## Round-26 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| source-capture-pdf | Capture a PDF public document to a committed, hash-pinned text snapshot via `pdftotext -enc UTF-8` (`capture-source.py --kind pdf`; flag available since round 24's `source-capture`), with located quotes asserted offline by `source-recheck.py` | `corpus/instruments/capture-source.py` (`--kind pdf`); `corpus/source-snapshots/round-26/manifest.json` + `S041.txt` (sha256 `e18acbf9…`, 7 pinned quotes) | 26 |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With
depth:verifiability at 4 the lowest-axis obligation stays active. Planned round 27:
see `## Planned` above.

## Round 27 — frozen claims C1/C2 (2026-10-25) — honest stop, NOT VERIFIED

Frozen before dispatch in `.ufo/waves/round-27/claims.json` (base `744a0d8`, lane tip at round
start; no in-place edit after freeze — R25-1 complied). Before-receipts committed at
`.ufo/waves/round-27/c1-controls/`, `c2-controls/`, `census-before.txt`. The operator ended the
run mid-round (orchestrator wrap-up): no wave dispatched, no production byte changed.

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | frozen baseline: bad-fixture exit 0 (BASE-ABSENT printed); bounties-fixture 0 BOUNTIES lines; `--selftest` absent; SKILL.md exit 0, bad=0 | not reached | **NOT VERIFIED — no dispatch, instrument unchanged.** Freeze, fixtures, do-nothing receipts and the M27-1 stale-premise capture are committed; the after-state was never produced. | 27 (not verified) |
| C2 | coverage (7) | frozen baseline: frontier admitted 11; entries citing S042: 0; census exit 0 / 41 rows; harness 14/14 | not reached | **NOT VERIFIED — no dispatch, no capture/entry/row.** The staged-package survey (S042 free id, staged S043 = lane S041) is recorded in the round-27 lesson Gate as planning only. | 27 (not verified) |
| depth:density | 9 | 9 | 9 | **Unchanged, no harm.** `SKILL.md` and every corpus byte untouched this round; no density/anchorcheck re-run needed beyond the committed SKILL.md before-receipt (exit 0, bad=0). | r15 (held r27) |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With depth:verifiability at 4
the lowest-axis obligation stays active. Planned round 28: re-freeze C1/C2 with the committed
round-27 fixtures re-run (not re-created), dispatch the build wave with reviewer seats inside it
(round-26 routed defect 2), inline ≤25-word Gate quotes (defect 3), one canonical receipt at the
landed digest (defect 4); carry-forward implementation notes are in `corpus/lessons/round-27.md`.

## Round 28 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-28/claims.json` (base
`c9f8b115a098c65356e4b3b6048af45a37ab8395`, the claims-freeze commit; wave-1 dispatch commit
`94f387cbeb71a532a51ce075f01701a557231e85`). The round re-declares the two claims round 27 froze
and never dispatched (its honest stop, § Round 27 above) and re-runs the committed round-27
fixtures instead of re-creating them (r27 carry-forward 1). Receipts land under
`.ufo/waves/round-28/` (`c1-controls/`, `c2-controls/`, `receipts/`).

**Measurement state (2026-10-25T17:23Z–17:29Z).** The section was drafted while wave 1 was landing
and then completed at the instrument's landed digest
`95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` (523 lines, 17:29Z; the
executor's own artifact records the same value as "landed file digest" in
`.ufo/waves/round-28/wave1/ExecImplC1.diff`). While the seat measured, the file was rewritten in
place: `c2a9e6c6…` → `2f707046…` → `0a24a173…` → `7adfc847…` → `982d7207…` → `5f5f725c…` →
`29aba084…` → `c3629229…` → `95333e29…`. Every intermediate state was rejected as evidence because
it missed at least one target (exit 0 on the bad fixture; `NameError: name '_selftest' is not
defined`; or the bounties cite resolving under the mirror prefix as `BASE-ABSENT`). Every counter
below was run at `95333e29…`, digest checked before and after, and each is reproducible across two
runs. **Still pending at write:** the canonical C1 receipt index
`.ufo/waves/round-28/c1-receipt-index.txt` (absent at 17:29Z; ExecReceiptCanonC1 and the L1 own it),
so frozen counter (c)'s receipt-index limb is unrun. ScribeSkillGate's `SKILL.md` append landed at
17:31Z (sha256 `125be37d…`, +3 lines) and the no-harm limbs were re-measured at those bytes (density
row). The frozen C1 `corpus_disclosure` cell was superseded by
`.ufo/waves/round-28/claims-erratum-1.md`; this seat re-measured the corrected reading and agrees
(0/0/0/15, zero verdict-class movement anywhere). A final re-verification at 17:33Z reproduced every
value in the table with the same digests (`anchorcheck.py` `95333e29…`, `SKILL.md` `125be37d…`);
the only open item remains `.ufo/waves/round-28/c1-receipt-index.txt`.

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | bad-fixture exit **0** (prints `BASE-ABSENT md:2 corpus/knowledge/zz-r27-anchorcheck-missing.md:99`, exit 0); bounties-fixture **0** `BOUNTIES-ABSENT` lines (cite invisible to `CITE`); `--selftest` absent (`FileNotFoundError: '--selftest'`, exit 1); `anchorcheck.py SKILL.md` exit **0**, **bad=0**, LOST-RECORDED=**306**; instrument sha256 `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748` | **Reached at the landed digest `95333e29…` (17:29Z, digest unchanged before and after every run):** bad-fixture exit **1** (same `BASE-ABSENT md:2 …zz-r27-anchorcheck-missing.md:99` line, now failing closed); bounties-fixture **1** `BOUNTIES-ABSENT` line (`~/Projects/bounties/ops/claim-check.mjs:96`, base absent); `selftest cases=9 failures=0`, exit **0**, two runs byte-identical (9 cases, each asserting the complete verdict vector with each of the four bases re-pointed at a fresh temp root via `KASEGI_LANE_ROOT`/`KASEGI_MIRROR`/`KASEGI_ORIGIN_ROOT`/`KASEGI_BOUNTIES`; case 8 is the bare-marker control) — **under the default environment only: an inherited `GIT_DIR` flips the `pin-broken` case, reproduced below**; `anchorcheck.py SKILL.md` exit **0**, **bad=0**, LOST-RECORDED=**306**, `BASE-ABSENT=0`, `PIN-BROKEN=0`, `OUTSIDE-BASE=0`, `ORIGIN=0`, in-range **7**. **Pending:** the receipt-index limb — `.ufo/waves/round-28/c1-receipt-index.txt` was absent at 17:29Z, so frozen counter (c)'s "at the instrument's own sha256" receipt line is not yet produced. | **Kill-rule hit, reproduced at the landed digest and unresolved at write: C1 cannot be recorded as met on these bytes.** Counters (a)–(d) are met in the default environment, but the frozen kill rule's clause "a limb with no failing fixture" fires under an inherited `GIT_DIR` — the `pin-broken` case flips to `IN-RANGE(PIN)` (reproduced below). The score is the L1's to set; this seat records the measurement, not a pass. The frozen disclosure cell is superseded by filed erratum 1, whose corrected reading this seat re-measured — routed, not hidden. Before values re-measured by this seat and by three independent read-only seats at the same digest: `.ufo/waves/round-28/c1-controls/{instrument-digest,bad-fixture,bounties-fixture,selftest,skill}-before.txt`, `.ufo/waves/round-28/receipts/ExecFixtureRun.txt`, `ExecInstrSelftest.txt` (determinism: two runs byte-identical), `ExecNoHarmC1.txt` (SKILL body byte-identical to the frozen before-receipt). Kill rules unchanged from `claims.json` C1. | 28 |
| C2 | coverage (7) | frontier admitted **11**; entries citing S042 **0**; registry **41** rows, census exit 0 (two pre-existing W04 S028/S029 duplicate-url warnings); harness `entries=14 pass=14 exit=0`. Receipts: `.ufo/waves/round-28/c2-controls/before.txt`, `census-before.txt` | **Reached at 17:29Z:** frontier **12** (F12 `knowledge/japanese-domestic-disclosure-workflow.md`, sources S041, S042); entries citing S042 **1**; S042 row **1** (tier A, mined, opened 2026-10-25, used-by exactly the entry); registry **42** rows, `sources-census.sh validate` exit **0** (only the two pre-existing W04 S028/S029 warnings); harness `entries=15 pass=15 exit=0` (F12 line `PASS … ids=S041,S042 exit=0`); `source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042` exit **0**, 6 quotes per source, every one `occurrences=1`; the entry's single `recheck:` line names those same two ids; S041's used-by lists the entry beside its two earlier ISO entries. | **Improved, score held 7 — every limb of the frozen after column is reached.** The score stays 7 because coverage's denominator (the r15 domain-root definition) is unchanged: this adds a twelfth admitted public-practice frontier topic and its first entry, not a restored lost surface. **Critic-reported limit, not an admission kill:** `CritC2Admission.md` finds the staged pre-publication user-notification claim (supported at S041 L229-234) silently omitted from the re-grounded entry and recommends restoring it or disclosing the omission in the entry's Limits. Recorded here; not repaired by this seat (the entry is ScribeEntryC2's file). Evidence pointers: `.ufo/waves/round-28/c2-controls/before.txt`, `census-before.txt`; `.ufo/waves/round-28/receipts/ExecC2Counters.txt` (both passes PRE-STATE), `ExecCaptureS041.txt`, `ExecCaptureS042.txt`, `ExecManifest.txt`, `ScribeReadmeC2.txt`; `corpus/source-snapshots/round-28/{S041.txt,S042.txt,manifest.json}`. Capture digests: S041.txt `e18acbf9…2f5ab47` (147267 B), S042.txt `b432ec16…b9c96966` (60508 B). Kill rules unchanged from `claims.json` C2. | 28 |
| depth:density | 9 | 9 | 9 | **Unchanged verdict, no credit claimed.** At base bytes (`SKILL.md` sha256 `fa09d5b835451f2443fc96353432a330608baf5f3631d1b382141f7e86d64f2d`, `git diff c9f8b115… -- SKILL.md` empty at 17:23Z): `density.py` mean **150.3**, **20** blocks, **652** path-citation instances; `anchorcheck.py` exit 0, bad=0, LOST-RECORDED=306, `BASE-ABSENT=0`, `PIN-BROKEN=0`, `OUTSIDE-BASE=0`. After ScribeSkillGate's R6 append (sha256 `125be37d85ffe6be30a3c372b52d96d8074e3c4d7f4baf835d0f5aed5f56cca6`, 1032 → 1035 lines: one `anchorcheck.py` row in the Gates & probes table plus the round-28 erratum note): mean **160.2**, **20** blocks, **656** cites, and `anchorcheck.py SKILL.md` still exit **0**, **bad=0**, LOST-RECORDED=**306**, every fail class 0. The mean rise is the appended gate documentation's own cites, not new evidence and not a density gain. **Baseline reconciliation (r25/r26's recorded 154.0 / 19 blocks / 652 is stale, not drift):** the same instrument measures r22 bytes (`git show c8b719d:SKILL.md`) at 19 blocks / 154.0 / 652, and r26 bytes (`a04cc6c`, 9 lines added — the `## Gates & probes registry` block, nb=5 ev=4 dens=80.0) at 20 blocks / 150.3 / 652; the new low-density block pulls the unweighted mean while path cites stay 652. Measured and named in `.ufo/waves/round-28/receipts/ExecNoHarmC1.txt` § 2, not inferred. | r15 (held r28) |

**C1 corpus disclosure — the frozen cell is superseded by filed erratum 1, and this seat's
measurement agrees with it.** `claims.json` C1 `corpus_disclosure` asserted that four marked
`[lost-tree]` `~/Projects/bounties/…` citations (`claim-gates.md:123`, `intake-and-finalize.md:109`,
`mission-control.md:169`, `source-tree-loss-2026-09-28.md:353`) "newly classify LOST-RECORDED",
i.e. **1 / 1 / 1 / 16**. Measured at the landed digest `95333e29…` with
`python3 corpus/instruments/anchorcheck.py <file> | grep -c '^LOST-RECORDED '` → **0 / 0 / 0 / 15**,
unchanged from the pre-change baseline; an independent survey for backticked anchored bounties
citations across `corpus/` and `SKILL.md` returns **0 hits**, which is the corrected cell appended
as `.ufo/waves/round-28/claims-erratum-1.md` (L1, appended never in-place, R25-1/R9). Cause, measured:
those four lines are plain prose trailers (`source: [lost-tree] ~/Projects/bounties/…`), and the
instrument's token extractor is backtick-only (`TOK`, `corpus/instruments/anchorcheck.py:152`), so
they are not citations at all; the backticked bounties tokens in the same files — a bare path with
no line anchor, e.g. the header at `corpus/knowledge/claim-gates.md:3` — carry no `:NN` and are not
`CITE` matches either. The arm itself works: a temp fixture carrying a backticked
`[lost-tree] ~/Projects/bounties/ops/claim-check.mjs:5` reports `LOST-RECORDED … (not checked)` and
exit 0, and the instrument's selftest case 8 asserts that the bare trailer is not a token
("exactly the measured corpus behaviour disclosed in the round-28 wave-1 receipt",
`corpus/instruments/anchorcheck.py:296-299`). Net effect: a stronger no-harm result than the frozen
cell predicted — the arm is invisible to every existing byte, and no verdict class moved on any
file (SKILL.md limb above). No corpus file was edited by this seat.

**C1 isolation attack — reproduced at the landed digest (a fact recorded here; the verdict is the
L1's).** `CritC1Kill.md` reports, and this seat independently reproduced, that `--selftest`'s
`pin-broken` case is decided partly by ambient git state: `_selftest()` copies `os.environ` and
overrides only the four `KASEGI_*` roots, so an inherited `GIT_DIR` survives into the case's
`git show deadbeef:pinned.md`. With a temp repo carrying ref `deadbeef` and blob `pinned.md`:

```text
GIT_DIR="<tmp>/.git" python3 corpus/instruments/anchorcheck.py --selftest
selftest FAIL pin-broken: PIN-BROKEN: want 1, got 0; IN-RANGE: want 0, got 1; exit: want 1, got 0
selftest cases=9 failures=1        # exit 1
```

The same bytes with no perturbation print `selftest cases=9 failures=0`, exit 0. Under the
perturbation the `PIN-BROKEN` limb has no failing fixture — the frozen kill rule's second clause
("a limb with no failing fixture"). The instrument's own verdicts are unchanged; the selftest is
not self-contained. Critic-reported, not re-measured here: `outside-base` exercises only the
bounties arm, so the MIRROR/ORIGIN `OUTSIDE-BASE` sub-limbs and the ORIGIN `BASE-ABSENT` sub-limb
have no failing fixture; and with `git` absent from `PATH` the selftest dies in a traceback with no
`selftest cases=` line (on this host `git` is present, so the frozen counters are unaffected).
Suggested fix, from the critic: sanitize `GIT_DIR`/`GIT_OBJECT_DIRECTORY`/`GIT_WORK_TREE`/
`GIT_INDEX_FILE`/`GIT_CEILING_DIRECTORIES`/`GIT_DISCOVERY_ACROSS_FILESYSTEM` out of the case env.
Receipt: `.ufo/waves/round-28/wave1/CritC1Kill.md`.

**In-flight observation, resolved (measured 17:24Z, re-measured 17:29Z).** With the F12 and S042
rows landed but the entry absent, the close-out gates were transiently red: `sources-census.sh validate`
exited **1** with `kasegi E11 S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md`
and the same line for S042, and `frontier-recheck-count.py` raised
`FileNotFoundError: '…/corpus/knowledge/japanese-domestic-disclosure-workflow.md'` (exit 1).
Both were consequences of the missing entry, not of the claims. Once the entry landed both pass —
census exit **0** with **42** registry rows, harness `entries=15 pass=15 exit=0` — so the transient
reds are recorded here only so they are not mistaken for a kill-rule hit, and are superseded by the
measured values above.

**L1 close-out block (run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; an unrun check has not passed).**

```sh
# C1 — re-run at the FINAL commit; values above measured at 95333e29…
sha256sum corpus/instruments/anchorcheck.py
grep -cE 'selftest cases=' .ufo/waves/round-28/c1-receipt-index.txt; grep -oE 'instrument_sha256=[0-9a-f]{64}' .ufo/waves/round-28/c1-receipt-index.txt   # frozen counter (c) receipt limb; index absent at 17:29Z
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bad-fixture.md >/dev/null 2>&1; echo "bad_fixture_exit=$?"
python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT
python3 corpus/instruments/anchorcheck.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo "skill_exit=$?"
python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | grep '^== '
python3 corpus/instruments/density.py SKILL.md --label r28-post | grep -E 'mean dens|Total path'   # required if ScribeSkillGate appended
for f in claim-gates intake-and-finalize mission-control source-tree-loss-2026-09-28; do echo -n "$f "; python3 corpus/instruments/anchorcheck.py corpus/knowledge/$f.md 2>/dev/null | grep -c '^LOST-RECORDED '; done
# C2 — re-run at the FINAL commit; values above measured at 17:29Z
awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
grep -lE '^source: S042 ' corpus/knowledge/*.md | wc -l
grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo "census_exit=$?"
python3 corpus/instruments/frontier-recheck-count.py
python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 --source S042; echo "recheck_exit=$?"
```

**Capabilities: no row added this round.** Per the round-28 assignment no new capability is
planned, and none was demonstrated beyond the frozen predicates: C1 extends an existing gate
instrument (`anchorcheck.py`) and C2 exercises the already-recorded `source-capture`,
`source-capture-pdf` and `frontier-recheck-harness` capabilities. The earlier Capabilities table
is unchanged; the r22 stagnation window continues to the r27 lesson, not restarted here.

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With depth:verifiability at 4
the lowest-axis obligation stays active.

### Round-28 close-out addendum (appended; canonical measurements)

At the final lane commit, the corrected `anchorcheck.py` digest is recorded in
`.ufo/waves/round-28/c1-receipt-index.txt`; C1 after-values re-run against it:
bad-fixture exit 1, BOUNTIES-ABSENT lines 1, `--selftest` cases=9 failures=0
(including the isolated-Git-environment regression), SKILL.md exit 0 with bad=0 and
LOST-RECORDED=306. The C1 disclosure erratum remains: 0 of the four named provenance
trailers are TOK tokens; no verdict class moves anywhere.

C2 close-out: F12 admitted 11→12, entries citing S042 0→1, S042 row 0→1,
registry 41→42; census exit 0; harness entries=15 pass=15 exit=0; both S041 and S042
manifest rechecks exit 0. The expected-list count basis is now aligned: the audit's
working-tree glob has 40 knowledge entries, the ignored-header list has 40 entry
lines / 42 physical lines, and `recheck-audit.py` exits 0 with expected=40,
missing=0, unexpected=0. The two source rechecks use separate `--source` invocations
because the CLI flag is single-valued.

No owned axis is assigned a scalar increase: depth:verifiability remains 4 and coverage
remains 7; both claims are measured improvements with scores held. Depth:density stays
9; after the append-only SKILL.md registry note, `density.py` reports mean 160.2,
20 blocks, 656 path citations (base was 150.3 / 20 / 652). The increase is disclosed,
not claimed as a score move.

## Round 29 — frozen claims C1/C2 (2026-10-25)

**Claim C1 (depth:verifiability, lowest non-retired axis — score held 4):** anchorcheck.py
`--selftest` completeness + hermeticity. Before: cases=9, `limbs=` assertion absent, git-free
run exit 1 + `FileNotFoundError: 'git'` traceback (receipt `c1-controls/before.txt`). After
(instrument sha256 `d0f35f8…`): `selftest cases=12 failures=0`, `limbs=9 covered=9`, exit 0;
git-free run `SKIP pin-broken (git not found)`, `limbs=9 covered=8 skip=1`, `nogit_exit=0`.
Canonical receipt `.ufo/waves/round-29/wave1/c1-receipt-index.txt` pins the digest. Post-wave
truthfulness correction (RevC1Instrument/CritGlobal): skipped limb no longer counted as covered.
Kill rule PASS. SKILL.md no-harm: 7 in-range/0 bad/306 LOST-RECORDED, skill_exit=0.

**Claim C2 (coverage — score held 7):** frontier F13 admitted (12→13) with entry
`corpus/knowledge/program-severity-ladders-and-reward-scales.md` citing rows first registered this
round S043/S044/S045 (42→45). Census exit 0 (W04 S028/S029 only); harness `entries=16 pass=16
exit=0` incl. `PASS F13 … ids=S043,S044,S045`; per-id source-recheck exit 0 each; manifest
`910608e6…` all 12 assertions exactly-once (Q9). Do-nothing control at base cannot meet target.
Kill rule PASS.

**Depth:density unchanged 9:** density mean 150.3→167.5 disclosed (measurement change, not a
score move); anchor verdict classes unmoved. **Capabilities: no row added this round.** Saturation
unchanged: line 9/10, window N=3; lowest-axis obligation stays active.

### Round-29 close-out addendum

At the final lane commit, all frozen counters re-run clean (post-commit-recheck.txt). Wave shape:
one v2 wave, 64 seats; m_flash roles 41/64 (64.1%), attack roles 19/64 (29.7%). Assimilation
theme: program severity ladders and reward scales (merge/kasegi read-only; quarantine slice 7 rows
hand-checked, none adopted); considerthese proposal 5 landed as QUALITY.md R15. Mistakes mined in
`corpus/lessons/round-29.md` §Mistakes (M29-1…M29-9) incl. M28-5 persistence on the frontier
harness and the mid-wave S043 occurrences=12 blind spot. No owned axis is assigned a scalar
increase; depth:verifiability remains 4, coverage remains 7.

## Round 30 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-30/claims.json` (base `a94871315…`,
claims-freeze commit `3c557354…`, wave-1 dispatch commit `002e92ce…`). Receipts
land under `.ufo/waves/round-30/` (`c1-controls/`, `c2-controls/before.txt`,
`census-before.txt`, `harness-after.txt`, `wave1/`).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | A1 exit 1 uncaught `FileNotFoundError` traceback, no named-row marker; A2 exit 0 `pass=2` on a duplicate entry realpath; B1 exit 0 (stem mismatch passes); B2 exit 0 `occurrences=2 anchor=MISSING` (`c1-controls/before.txt`, `before-run-2.txt`) | A1 exit 1 `FAIL F98 knowledge/zz-missing.md … problems=missing-entry` naming row and path; A2 exit 1 `DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md`; B1 exit 1 `reason=stem-mismatch`; B2 exit 1 with a failure reason (the frozen fixture trips the B1 stem limb first; see B2 note); `source-recheck.py --selftest` 9/9 exit 0; real-corpus regression leg green (full harness 17/17 exit 0; 34 prior registered source-rechecks on manifests rounds 23–29 and round-30 S046/S047/S041 all exit 0) | **Improved, score held 4.** Instruments: `frontier-recheck-count.py` `c8a62888…` → `aa60b581…`; `source-recheck.py` `9fe6a4a0…` → `33602a9d…`. Do-nothing control at freeze bytes reproduces all four before defects (`ExecMutantsC1.md`, `CritC1Kill.md`) — control cannot meet the target. Mutants A1/A2/B1 each flip exactly one limb; mutant-B2 flips on the supplementary same-stem fixture (live exit 1 `reason=occurrence-not-unique`; mutant exit 0) — the committed `manifest-b2.json` (id S045, path B2.txt) has the stem limb fire first, so the frozen B2 counter does not isolate the occurrence limb (R10-class fixture defect, recorded; the limb is covered by the selftest 9-case matrix and the clean same-stem fixture). Kill rule PASS as written (b2 exit 1 names a failure reason; no real-corpus regression). | 30 |
| C2 | coverage (7) | frontier admitted 13; entries citing S04[6-7] 0; registry rows 45; census exit 0; harness entries=16 pass=16 exit=0 (`c2-controls/before.txt`, `census-before.txt`) | frontier admitted **14** (F14 row in `corpus/README.md`); entries citing S046/S047 **1** (the F14 entry); registry rows **47** (S046/S047 appended); census **exit 0** (W04 S028/S029 only); harness **entries=17 pass=17 exit=0** incl. `PASS F14 knowledge/japanese-severity-vocabulary-and-impact-model.md ids=S041,S046,S047 exit=0`; source-recheck S046/S047/S041 each **exit 0** on the round-30 manifest (`dfc88357…`), all assertions exactly-once or anchor-verified (S047 Q1 occurrences=3 anchor=123-ok, Q3 occurrences=2 anchor=130-ok) | **Improved, score held 7.** C2 sourced: F14 entry `knowledge/japanese-severity-vocabulary-and-impact-model.md` (`f584f06c…`, 38 lines) cites S046/S047 (first registered this round; captures `S046.txt` `884481f3…` / `S047.txt` `bcf4f605…`) plus the already-registered S041 (capture reused from round 28, `e18acbf9…`). Do-nothing control at base (13/0/45, 16/16, no captures) cannot meet the target. Kill rule PASS at the landed bytes (`harness-after.txt`; `ExecCensusAfter.md`). | 30 |
| depth:density | 9 | mean 167.5, 22 blocks, 659 path-citation instances (SKILL.md `82bdced5…`) | mean **171.1**, 23 blocks, 662 cites (SKILL.md `a05c1b47…`, 1047 → 1057 lines; R6 append of the round-30 Gates & probes registry section); `anchorcheck.py SKILL.md` exit 0, verdict classes unmoved: 7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0 | **Unchanged, no harm.** Density change disclosed, not claimed as a score move (same posture as round 29). | r15 (held r30) |

**Measurement state.** Values above were measured at the landed working-tree bytes
described in `.ufo/waves/round-30/harness-after.txt` (digests pinned there), at
`c1-controls/mutants/` and by `ScribeDigest.md`; earlier red snapshots recorded
mid-wave states (F14 entry/manifest absent, S047 unanchored, census E11) and are
superseded by the final receipts, not hidden.

**B2 fixture note (recorded, not a kill).** The frozen `manifest-b2.json` declares
`id=S045` with `path=B2.txt`, so the B1 stem check fires before the occurrence gate;
the frozen counter b2 exits 1 with `reason=stem-mismatch`. This satisfies the frozen
kill-rule clause (exit 1 + a failure reason) but does not exercise the B2 limb; the
occurrence limb is demonstrated by `--selftest` (9/9) and by the supplementary
same-stem fixture where the live instrument exits 1 `reason=occurrence-not-unique`
and mutant-B2 exits 0 (`ExecMutantsC1.md` §4, `CritC1Kill.md` §3–§4). A corrected
isolating B2 fixture is the recommended follow-up, already recorded in the lesson
receipts.

**recheck-audit open item (outside the frozen claims).** `recheck-audit.py`
prints `expect=present expected=43 missing=0 unexpected=0 exit=1`: the strict
instrument/own limbs reject the new `considerthese-proposals-ledger.md` recheck form
(names no corpus instrument and not its own file), so the audit's exit-0 acceptance
is not met (`ExecExpectedList.md`). Expected-list equality holds; the item is
recorded for the lesson.

**Capabilities: no row added this round.** Per the round-30 assignment no new
capability is planned, and none was demonstrated beyond the frozen predicates: C1
extends the existing `frontier-recheck-harness` and `source-capture` instruments and
C2 exercises the already-recorded `source-capture`, `source-capture-pdf` and
`frontier-recheck-harness` capabilities. The Capabilities table is unchanged; the
stagnation window continues (last capability entry round 25).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With
depth:verifiability at 4 the lowest-axis obligation stays active.

### Round-30 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 30 | depth:verifiability | 4 (A1 traceback/no row marker; A2 duplicate passes; B1 stem passes; B2 double-occurrence passes) | 4 held (A1 exit 1 naming F98; A2 exit 1 naming duplicate; B1 exit 1 reason=stem-mismatch; B2 exit 1 reason present; selftest 9/9; 34 base-passing real rechecks preserved) | `corpus/instruments/frontier-recheck-count.py`, `corpus/instruments/source-recheck.py`, `.ufo/waves/round-30/c1-controls/`, `wave1/ExecImplSourceRecheck.md`, `wave1/ExecMutantsC1.md`, `wave1/CritC1Kill.md` |
| 30 | coverage | 7 (frontier 13, S046/047 citations 0, registry 45, harness 16/16) | 7 held (frontier 14, citations 1, registry 47, census exit 0, harness 17/17, rechecks exit 0) | `corpus/README.md` F14 row, `corpus/SOURCES.md` S046/S047, `corpus/source-snapshots/round-30/manifest.json`, `.ufo/waves/round-30/harness-after.txt` |

### Round-31 erratum to the round-30 section

r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819` was true when it was composed and is **superseded** by the final round-30 ledger-recheck correction, not withdrawn as an error. At composition the strict instrument/own limbs rejected the then-current `considerthese-proposals-ledger.md` recheck form, so the audit printed `expect=present expected=43 missing=0 unexpected=0 exit=1`. The correction changed that recheck to `density.py` over its own entry (`corpus/knowledge/considerthese-proposals-ledger.md:5`, sha256 `d91889e5f7d77c3695c366521c348569b4f29269632e0bfc927105600a6c250d`); the audit now prints `strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0` and `expect=present expected=43 missing=0 unexpected=0 exit=0`, exit 0. The filed paragraph stays byte-identical (append-only, R6/R9).

Pointers: `corpus/lessons/round-30.md` § Close-out erratum (records the ledger-recheck change and the final `strict pass=43/43`, `executes=19 gated=24 broken=0`); `corpus/lessons/round-30-verifier-spotcheck.md` §5 item 4 (routed defect: correct this stale paragraph).

Live re-run, cwd = lane root, quiescent bytes (`corpus/instruments/recheck-audit.py` sha256 `3fc0d751f2a5819879d440f8ef62b607376a8b6914d7edf9fe1b2fc25662d4e1`, unchanged from this wave's red-before digest; working tree clean for `corpus/`):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"
```

Measured 2026-10-25T23:33:27Z, exit 0:

```text
strict pass=43/43 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=19 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=43 total=43 pass=43 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=43 missing=0 unexpected=0 exit=0
```

Measurement limit, recorded rather than hidden: the same command on a `git archive` export of lane base `b374febbb33ccadade78a787279707fd5d2e6e1d` at a different path prints `strict pass=1/43 cdroot_fail=42 instrument_fail=0 own_fail=0 … exit=1`, because strict limb (d) requires the `cd <path> &&` target to equal the audited root (`corpus/instruments/recheck-audit.py:27`, `:137`) and 42 entry rechecks cd to the canonical lane path. A copy-relative run is therefore not a base measurement; the value quoted above is the lane-root one. If `recheck-audit.py` bytes change later this round (the C1 limb work), re-run and label any new value with its date.

Capabilities clause, corrected: the round-30 headline "no row added this round" holds for round 30 (no round-30 capability table exists), but its parenthetical "(last capability entry round 25)" (`SCORECARD.md:825`) is false — round 26 added `source-capture-pdf` (`SCORECARD.md:580-584`, first-working round 26), so the last capability entry as of round 30 is round 26 and any stagnation count starts there. The filed sentence is left byte-identical; this erratum is the correction of record.

## Round 31 — frozen claims C1/C2 (2026-10-25)

Frozen before dispatch in `.ufo/waves/round-31/claims.json` (base `b374febb…`, claims-freeze
commit `738a77999…`, wave-1 integration `eecad59db…`). Receipts land under `.ufo/waves/round-31/`
(`c1-controls/before.txt`, `c1-controls/fake-counter-receipt.txt`, `c2-controls/before.txt`,
`census-before.txt`, `wave1/`, `wave2/`). Wave 2 is a falsify wave: 13 one-limb re-derivations
(`wave2/ExecLimb*.md`), six counter-mutant receipts (`wave2/MutCtr*.md`), two quote re-opens
(`RevQuoteRoles`, `RevQuoteRoutes`), an independent Q1–Q10 entry review (`RevEntryQ`), an
expansion-credit critic (`CritExpansion`), the counter repair (`ExecCounterFix`) and three
no-harm/final counters (`ExecNoHarmDensity`, `ExecCensusFinal`, `ExecRegressionC1`).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | `limb-ledger.json` / `limb-mutation-check.py` absent (`ls_exit=2`, `counter_exit=2`); `source-recheck --selftest` `cases=9 failures=0`; `recheck-audit --quiet` `strict pass=43/43 … exit=0`; frontier harness `entries=17 pass=17 exit=0`; a fake counter that prints both summary lines with 0 `LIMB ` lines is rejected (`c1-controls/before.txt`, `c1-controls/fake-counter-receipt.txt`: `fake LIMB lines: 0`) | 13 `LIMB ` lines (`grep -c '^LIMB '` = 13), every row `live=` ≠ `mutant=`; `limbs=13 killed=13 survivors=0`; `controls=3 rejected=3`; `guard cases=3 failures=0`; exit 0 twice byte-identically (stdout sha256 `d6aefddc…`); `--selftest` `cases=20 failures=0`; no-harm on the same bytes: `strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0` and `expect=present expected=44 missing=0 unexpected=0 exit=0`, `source-recheck --selftest` `cases=10 failures=0`, `anchorcheck --selftest` `cases=12 failures=0` / `limbs=9 covered=9`, harness `entries=18 pass=18 exit=0`, 38 registered source ids over 8 manifests 38/38 exit 0 (`wave2/ExecRegressionC1.md`) | **Verified, score held 4.** The frozen kill rule is met on the repaired final revision: exact summary lines, 13 LIMB lines each with `live` ≠ `mutant`, exit 0 twice byte-identically, and no corpus regression on any leg above. Each row was also re-derived by hand from a scratch copy with the counter's line reproduced — 10 `holds`, 3 `weak` (`RA-cdroot` shape-narrow fixtures, `RA-paths` `named`-conjunct unwitnessed, `FR-missing-entry` signal-only kill; `wave2/ExecLimb*.md` §Verdict), recorded not relabelled. The 3 controls reject (`CTL-noop invalid:noop`, `CTL-nocompile invalid:nocompile`, `CTL-equivalent survivor`, all `ok=y`). Do-nothing control: base bytes have no counter and the fake counter meets the text with 0 `LIMB ` lines, so the target is unreachable without the work. Disclosed and **not** counted as a clause met: the claim's own `mutants_of_the_counter` set was falsified at the wave-1 landing (2 of its 4 frozen mutants survived) and repaired post-freeze — paragraph below. | 31 |
| C2 | coverage (7) | `frontier_admitted=14`, `entries_citing_S048=0`, `rows_S048=0`, `registry_rows=47`, `census_exit=0`, `entries=17 pass=17 exit=0`, `manifest UNAVAILABLE reason=missing`, `recheck_exit=2` (`c2-controls/before.txt`) | frontier admitted **15**; entries citing S048 **1**; `S048` rows **1**; registry rows **48**; census **exit 0** with exactly `W04 S028` + `W04 S029` + `ok` and no `E`/new `W`; harness **`entries=18 pass=18 exit=0`** incl. `PASS F15 knowledge/vendor-third-party-finding-coordination.md ids=S048 exit=0`; `source-recheck --manifest corpus/source-snapshots/round-31/manifest.json --source S048` **exit 0**, 8 assertions every `occurrences=1` (`wave2/ExecCensusFinal.md` §1 — the frozen commands run verbatim from `claims.json`, ten surfaces digested twice 107 s apart with identical hashes; junk-row and base controls re-derived in §2–§4) | **NOT VERIFIED — honest stop, no credit claimed (score stays 7).** All seven frozen counter cells are met on quiescent bytes, but the kill rule's entry clause trips: the independent non-author Q1–Q10 review returns `REFUSE — on Q3 only` (`wave2/RevEntryQ.md` §5). Its ground: `corpus/knowledge/vendor-third-party-finding-coordination.md:84-87` warrants addition 3 with “F10's thesis is a vendor's standing statement about the handling of findings in its *own* products” — no verbatim quote and no location — and that reading is refuted by the crosswalk rows the entry itself cites (`vendor-disclosure-policy-commitments-crosswalk.md:49`, `:66`; §F1 there). The minimal one-bullet fix is named and owned by the L1 (`RevEntryQ` §5). The competing reviewer readings are quoted verbatim below; the ruling is the canonical judge's. A miss is recorded, not narrowed. | 31 |
| depth:density | 9 | mean 171.1, 23 blocks, 662 path-citation instances (r30 `SKILL.md` replayed from `5703f9f`) | mean **191.5**, 24 blocks, 689 cites (`SKILL.md` `81763604…`, 1057 → 1071 lines); `anchorcheck.py` unmoved in every class (7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0, exit 0) | **Unchanged (held 9), no harm; density change disclosed, no score move claimed.** Every pre-existing block row is byte-identical; the whole mean move is the appended block 24, whose resolve fraction is `11/27 = 40.74%` and therefore fails the instrument's own conjunctive bar (≥60%) — recorded as a volume/rule effect, not as new resolvable evidence (`wave2/ExecNoHarmDensity.md` §1, §1c, §1d, §2, §5). | r15 (held r31) |

**Counter-mutant repair, disclosed (post-freeze, round-25 form).** `claims.json` C1
`mutants_of_the_counter` names four counter mutants that attack seats must show are caught. Wave 2
found **two of them surviving byte-identically** — `find-text-not-unique accepted`
(`wave2/MutCtrNonUniqueFind.md` §Verdict: both summary lines, exit 0, stdout sha256 `9b386485…`)
and `never-run-live-baseline` (`wave2/MutCtrNoLiveBaseline.md` §Verdict: byte-identical output,
`9.8 s` vs `20.8 s` wall) — plus one out-of-set survivor, kill-command timeout counted as `killed`
(`wave2/MutCtrTimeoutKilled.md` §Verdict). The other three frozen mutants were caught:
`always-killed` → `controls=3 rejected=2`, `nocompile` → `rejected=2`, `signal-ignored` →
`limbs=13 killed=12 survivors=1`. `ExecCounterFix` then closed all three survivors **inside the
counter** with three implicit guard fixtures on every `--ledger` run (`guard cases=3 failures=0`),
adding no limb and no control, so the frozen counts stay `controls=3 rejected=3` and no claims
amendment is needed (`wave2/ExecCounterFix.md` §1, §4, §5): red-before, all three mutants exit 0
on `c660a95f…` (§3); green-after, each exits 1 on `237fd07c…` (§5 table), with the real run still
exit 0 twice byte-identically (§5). The frozen numbers are reported beside the repaired ones; the
repair is disclosed as a post-freeze repair and is not counted as meeting a frozen clause.

**C2 reviewer conflict, reported verbatim for the canonical judge.** `wave2/RevEntryQ.md` §5:
`REFUSE — on Q3 only`. `wave2/RevQuoteRoles.md` §Verdict summary: `0 HIGH, 2 MEDIUM, 12 LOW`
findings, `none is a claim without a locatable quote`. `wave2/CritExpansion.md` §VERDICT:
**`partial`**, `Not restatement`, and `C2 is not failed by this review` — three sentence-level
edits routed, not applied. `wave2/RevRowS048.md` §Verdict summary: `all six rules CONFORMANT at
row level`, `No medium or high finding.` `wave2/RevQuoteRoutes.md` opens with
`all 8 manifest assertions AGREE`. The round's own lesson reads these as `Non-author reviews agree
on admission` (`corpus/lessons/round-31.md:14`), which does not carry RevEntryQ's filed Q3
REFUSE; this scorecard records the REFUSE as the clause-tripping verdict and leaves the ruling to
the canonical judge. Also recorded, not charged to C2: the expansion critic's `partial` grade and
the routed three-edit correction (`CritExpansion` §6).

**Measurement state.** Values above were measured at lane HEAD `eecad59db…` with `git status
--porcelain corpus/` empty, except the one path that changed after wave 1: the counter, owned by
`ExecCounterFix`. Revisions named: `limb-mutation-check.py` **`237fd07c…`** (820 lines,
post-repair; `c660a95f…` is the pre-repair revision every wave-2 `ExecLimb*`/`MutCtr*` receipt
measured, and `cde7c2b6…` / `f926bf75…` are mid-edit wave-1 states — none is compared to an after
column, M30-3), `limb-ledger.json` `c042adf6…` (unchanged by the repair), `recheck-audit.py`
`5d4842da…`, `source-recheck.py` `fd2e01e8…`, `frontier-recheck-count.py` `aa60b581…`; entry
`1f16e371…`, `README.md` `d9865b2e…`, `SOURCES.md` `5a03c696…`, `knowledge-expected.txt`
`d6f25227…`, manifest `b80f7f92…`, `S048.txt` `2001ad77…` (3755 B, 97 lines), `SKILL.md`
`81763604…`. Mid-wave partial states (`admitted=14`, registry 47, harness 17/17 at
`23:31:56Z`, `wave1/ExecHarnessC2.md` §last) are superseded by the quiescent runs above, not
hidden. The C1 numbers are quoted from `wave2/ExecRegressionC1.md` at the repaired revision; the
13 limb re-derivations were taken on `c660a95f…`, whose LIMB/control lines the repair leaves
unchanged and the regression run reproduces. Several wave-2 seats' poll loops were
auto-backgrounded by the shell tool rather than staying in the foreground; that is disclosed as a
tool artefact, not reported as a foreground run.

**Capabilities: one row enters.** C1's counter and ledger are demonstrated running at the final
revision with the exit-0 output (`wave2/ExecRegressionC1.md`: `limbs=13 killed=13 survivors=0` /
`controls=3 rejected=3`, 13 `LIMB ` lines, two runs byte-identical), so
`limb-mutation-ledger` enters the Capabilities table for round 31 — appended below as
`## Round-31 capabilities`, the round-24/25/26 pattern, because this seat is append-only and does
not edit the master `## Capabilities` table in place. The master table is otherwise unchanged.

## Round-31 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| limb-mutation-ledger | Prove each of 13 named limbs of the lane's three recheck instruments load-bearing on committed bytes: copy the corpus into a fresh scratch lane, run each limb's kill command unmutated (exit + declared signal) and again after an exactly-once find/replace patch that must still compile, print one `LIMB <id> live=… mutant=… verdict=killed\|survivor\|invalid:<reason>` line per row plus three control rows and three guard lines, exit 0 only when `limbs=13 killed=13 survivors=0` and `controls=3 rejected=3`; stdlib only, writes nothing into the lane, runs no git write | `corpus/instruments/limb-mutation-check.py` (sha256 `237fd07c…`), `corpus/instruments/limb-ledger.json` (`c042adf6…`); `.ufo/waves/round-31/wave2/ExecRegressionC1.md`; 13 row re-derivations in `wave2/ExecLimb*.md`; 6 counter-mutant probes in `wave2/MutCtr*.md` | 31 |

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. With depth:verifiability at 4
the lowest-axis obligation stays active. The round-31 `limb-mutation-ledger` entry restarts the
capability window (previous entry round 26); if the canonical judge refuses the row, the
entry-less run since round 26 reaches four admitted rounds and the nudge applies.

### Round-31 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 31 | depth:verifiability | 4 (no limb ledger, no mutation counter; the three recheck instruments' limbs unproven) | 4 held (13 limbs each killed by its own exactly-once patch, 3 controls rejected, exit 0 twice byte-identically; 10 of 13 rows re-derived `holds`, 3 `weak`; frozen predicate met, the C1 counter-mutant set falsified in wave 2 and repaired post-freeze) | `corpus/instruments/limb-mutation-check.py`, `corpus/instruments/limb-ledger.json`, `.ufo/waves/round-31/wave2/ExecLimb*.md`, `wave2/MutCtr*.md`, `wave2/ExecCounterFix.md`, `wave2/ExecRegressionC1.md` |
| 31 | coverage | 7 (frontier 14, entries citing S048 0, registry 47, harness 17/17, manifest absent → recheck exit 2) | 7 held, no credit claimed (frontier 15, entries citing S048 1, registry 48, census exit 0, harness 18/18, recheck exit 0 — but the frozen entry clause is contested by a non-author Q3 REFUSE) | `corpus/README.md:309` F15, `corpus/SOURCES.md:54`, `corpus/source-snapshots/round-31/manifest.json`, `wave2/ExecCensusFinal.md`, `wave2/RevEntryQ.md` |

### Round-31 errata — instrument relabel for the C1 limb change

r31 erratum: the paragraph `recheck-audit open item (outside the frozen claims)` filed at `SCORECARD.md:813-819`
is re-labelled, not rewritten: after the C1 limb work `corpus/instruments/recheck-audit.py` sha256
`5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` prints
`strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0` (`lines=44 total=44`), measured 2026-10-26T00:45Z.

### Round-31 post-wave-2 addendum (residual call `wave3`, appended by the L1)

After the lane commit `fd29aac0dd02f4c6783a0df8c4ba8d0e86414242` the L1 repaired the F15 entry (overlap
section rewritten to concede F10's Cybozu and internal-detection rows, quotes carried in the source
language, route-3/Cisco wording fixes, manifest Q9–Q11 added: 8 → 11 assertions, all `occurrences=1`) and
`score-gap.py` (census `cmd:` pattern). A residual call of five seats re-reviewed at commit
`022b755008777ee143b566cce3cfd0914c9846c0` (receipts `.ufo/waves/round-31/wave3/`): `RevEntryQ2` still
filed **REFUSE on Q3 only** for the first repair (a translated string `"third-party products it uses"`
inside quote marks at S036.txt:15; the Japanese original and `社内での検出` were not carried); the L1 then
replaced both with the verbatim Japanese strings and re-ran the mechanical checks (each string
`grep -c` ≥ 1 at its cited file; `source-recheck` exit 0 with 11 assertions; `recheck-audit` `strict pass=44/44`; harness
`entries=18 pass=18`). That final revision has **no independent re-review**; the C2 admission therefore
rests on the wave-2 `RevEntryQ` (REFUSE on an earlier revision), `RevEntryQ2` (REFUSE on the second
revision, fix applied after it) and the L1's mechanical re-run — reported as an open reviewer conflict for the
canonical judge. `CritExpansion2`: `partial`, restatement clause does not fire. `MutCounterReplay`: all six
published counter mutants are caught by the repaired counter (`237fd07c…`), three of them by the guard-fixture
exit status alone, not by the frozen summary lines. `RevScoreGapFix`: census-command repair verified (D1);
D2 (stub-mode fixture) was not repaired as first applied (`json` was not imported) and is repaired in
the closing commit, with the `KeyError` arm left as a disclosed latent defect. `RevQualityFix`: R17 holds;
R16 weak, R18 defect (no conforming specimen until the relabel above), R19 weaker than its criterion — disclosed in
`corpus/lessons/round-31.md` § Close-out erratum, not repaired.

### Round-31 final addendum — residual call `wave4` (supersedes the "no independent re-review" sentence above)

A second hand-built residual call (2 seats, dispatch `43c364d06ccf5a3d1029c0f7816c8e50b509365b`, receipts `.ufo/waves/round-31/wave4/`) reviewed the final F15 entry revision at lane tip `43c364d`: `RevEntryQ3` — a seat that neither wrote nor earlier reviewed the entry — **ADMIT**, Q1–Q10 all pass, the blocking findings of both earlier REFUSEs resolved on the current bytes, LOW/NIT items only (route-3 note token, one paraphrase outside quotes); `CritQuoteSweep` — `clean`, 0 mismatches among 28 source-bound quote rows (one routed Q33 note on a rejected-inference quote). Both seats are dispatched by this lane, so the verdict is lane-seat, not the non-author closure's. The C2 reviewer conflict is therefore: two REFUSEs on earlier revisions, one ADMIT on the final revision.

## Round 33 — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-33/claims.json` (base
`690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`, claims-freeze commit
`6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`, Rule-B erratum commit `53bfa59f…`, wave-1
integration commit `9f9848816503aa0cd566fc2efdc5e69ea501a253`). **Final lane commit:
`7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1); the wave-1 value above
is the commit the after-column seats measured, not the closing commit. Receipts land under
`.ufo/waves/round-33/` (`c1-controls/`, `c2-controls/`, `census-before.txt`,
`assimilation/`, `watchdog-digest.txt`, `wave1/`; 54 seat receipts plus
`swarm-registry.json` at this seat's gate). This file carried **no round-32 section** at
base (`grep -n '^## ' SCORECARD.md` returns round 31 as the last round heading), so C2's
last-change column stays 31 and every before-column below is measured at this round's
base bytes, not against a round-32 scorecard row. The round-33 subject is capture-manifest
binding (C1) and frontier F16 / Chinese crowdsourced-testing platform scope and reward rules
(C2).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | instrument absent (`ls_exit=2`); manifest audit `TOTAL records=38 with_url=0 with_fetched_utc=0`; `corpus/source-snapshots/round-32/` holds `S049.txt`/`S050.txt` with **no manifest**; `source-recheck` on the absent round-32 manifest prints `manifest UNAVAILABLE reason=missing`, `recheck_exit=2`; the frozen fake checker prints `records=38 bound=38 unbound=0` with `fake_exit=0` and no validation (`c1-controls/before.txt`, `c1-controls/fake-checker-receipt.txt`) | `records=40 bound=40 unbound=0` with `run1_exit=0 run2_exit=0` and byte-identical stdout (sha256 `1861fec8…a3c5a9f1`); `AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2`; `--selftest` `cases=11 failures=0` exit 0; on base bytes the real checker prints `records=38 bound=0 unbound=38` exit 1 and names `FAIL rule=missing-manifest dir=round-32`; the fake prints the same summary there with exit 0 and `--selftest cases=0`, so the kill rule rejects it; no-harm on the same bytes: `strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0`, `expect=present expected=45 missing=0 unexpected=0 exit=0`, `source-recheck --selftest cases=10 failures=0`, harness `entries=19 pass=19 exit=0`, and 40 `:sha256 OK` pins across all nine manifests (the byte half `capture-binding-check.py` does not carry); instrument `b4182665…` (492 lines) (`wave1/ExecRegressionC1.md` §1–§2, `wave1/ExecNoHarmFinal.md` §7, `wave1/CritC1Kill.md` byte arm) | **Verified, score held 4.** Every frozen counter clause is met on quiescent bytes, twice byte-identically, and the do-nothing control cannot reach the target: the base tree has no instrument, no manifest for `round-32`, no `url` on any of its 38 records, and the fake checker that meets the summary text is rejected by the base-byte discriminator. The independent instrument review lands: `**lands** — all six review questions answered yes with code-line and behavioral evidence at the quiescent digest` (`wave1/RevC1Instrument.md` §9); `The counter is falsifiable and satisfies the kill rule's fake-checker clause.` (same file, Verdict 1, on `CritC1Kill` §Verdict 1). Disclosed, not scored as clause work: the frozen kill text's global exactly-one-match parenthetical is superseded by erratum 1 (per-id row binding; a URL shared by two ids is informational `multi_row_url=2` — S024/S029, S006/S028) and the erratum is load-bearing, since a literal global reading rejects the correct instrument (`wave1/CritC1Kill.md` Verdict 3); the critic's seven-plus blind spots H1–H8 (capture bytes, nested dirs, `fetched_utc` presence-only, duplicate records, two-token rows, rejected-row anchors) are spec-level, with H1–H3 covered only when the `source-recheck` byte run is cited beside the checker (`wave1/CritC1Kill.md` Verdict 4, §Disclosures); and `anchorcheck.py SKILL.md` reports **12** in-range anchors rather than the item's 7, five of them added by this round's `SKILL.md` append, with every failure class identical (`wave1/ExecRegressionC1.md` D-R33-1). | 33 |
| C2 | coverage (7) | `frontier_admitted=15`; `S049=0`, `S050=0`; `S049_rows=0`, `S050_rows=0`, `total_rows=48`; census exit 0 with only `W04 S028` + `W04 S029` + `ok`; harness `entries=18 pass=18 exit=0`; `manifest UNAVAILABLE reason=missing`, `recheck_exit=2` (`c2-controls/before.txt`, `census-before.txt`) | frontier admitted **16**; entries citing `source: S049 `/`S050 ` **1 / 1**; `S049` rows **1**, `S050` rows **1**, registry rows **50**; census **exit 0** with exactly the base `W04 S028` + `W04 S029` warnings and no `E` finding; harness **`entries=19 pass=19 exit=0`** including `PASS F16 knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050 exit=0`; `source-recheck` on `corpus/source-snapshots/round-32/manifest.json` **exit 0** for both sources — S049 `sha256 OK` + Q1–Q8, S050 `sha256 OK` + Q1–Q6, all 14 quote assertions `occurrences=1` — and the entry's own `recheck:` line exits 0 from the lane root, `/` and `/tmp`; six contract census commands `rows=50`, `malformed=0`, `tier=A=47 B=1 C=2`, `status=mined=38 queued=9 rejected=3`, `dups=`, `enum_violations=0`, `missing_usedby=0`, and the `diff -u` against `census-before.txt` shows only the expected `+2` rows / `+2` tier-A / `+2` mined deltas (`wave1/ExecHarnessC2.md` §1–§3, `wave1/ExecCensusAfter.md` §1–§3) | **Verified on all nine frozen counters, score held 7**, with the entry clause carried by a non-author ADMIT and the residual reviewer posture reported below rather than narrowed. Row reviews at quiescent bytes return `**ADMIT-ROW**` for S049, which `conforms to SOURCES contract v1 rules 1–6 on every checked cell` (`wave1/RevRowS049.md` §8), and `ADMIT-ROW` for S050 with `All six contract rules CONFORMANT at row level` and `No medium or high finding.` (`wave1/RevRowS050.md` §3). The independent Q1–Q10 review returns `**ADMIT.**` (`wave1/RevEntryF16.md` §7) on entry digest `53c48b3b…` (306 lines); the final lane bytes are `1f7ac0a2…` (306 lines, 24539 B) and carry **no second full Q1–Q10 review** — the delta is a Claim 1 question stem, verified narrow by the mutation probe (`wave1/MutEntryF16.md` §digest history: `edits confined to a Claim 1 question stem — verified here: source: lines on 3/4, recheck: on 7`) and re-measured on the final bytes by the quote sweep's closed finding (`wave1/RevQuoteSweep.md` §6) and by `wave1/RevTranslation.md`. Two findings are recorded, neither a frozen-clause trip: `## Verdict: SURVIVOR (coverage finding)` for the one-sided header-drop mutant, which the receipt itself scopes as *an instrument coverage finding on `frontier-recheck-count.py` rule A, not a defect in the entry*, and the critic's measured junk twin, on which every C2 counter passes, so that `the counter set discriminates **shape**, not content` and novelty/Q3/Q4 rest on the reviewer clause alone (`wave1/CritC2Kill.md` §5). | 33 |
| depth:density | 9 | mean 191.5, 24 blocks, 689 path-citation instances (`SKILL.md` replayed from base `690b69da`) | mean **201.7**, 25 blocks, 710 cites (`SKILL.md` `b11b6085…`, 1071 → 1090 lines); `anchorcheck.py` failure classes unmoved (0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0, exit 0) with in-range 7 → 12; `git diff --numstat` on the append-only files `19 0 SKILL.md`, `2 0 PROVINCE.md`, 0 deletions (`wave1/ExecNoHarmFinal.md` §3–§4, `wave1/ExecRegressionC1.md` §1 rows 7–9, §2.9–§2.10) | **Unchanged (held 9), no harm; the density move is disclosed, no score move claimed.** Both sides were measured with the same committed instrument on the same file: base 191.5 / 24 / 689, final 201.7 / 25 / 710. The whole increase is the appended round-33 gate block (19 lines, 21 citation instances); every fail class in `anchorcheck.py` and the 306 LOST-RECORDED count are identical on both sides. The in-range count rising 7 → 12 is logged as a count change with unchanged classes, not as new resolvable evidence. | r15 (held r33) |

**Rule-B erratum, disclosed (post-freeze, round-25 form).** `claims.json` C1's interface
contract says a `url` that greps to "0 or 2+ matches" is a failure, which read literally
rejects the two cross-id URL pairs the registry has held since round 24 (S024/S029 EUR-Lex,
S006/S028 HackerOne). The L1 filed `.ufo/waves/round-33/claims-erratum-1.md` before any seat
scored: rule B binds a record to its **own** id row by byte-exact token match, a URL shared by
two different ids is informational (`multi_row_url=2`), and two rows with the same id are
`dup-id`. The landed instrument implements it (`case_duplicate_id_rows`, `case_shared_url_passes`)
and the frozen counters are reported under the erratum reading, not the literal one.

**Erratum 2, disclosed (round-34 append, round-25 form).** The frozen C1 kill-rule
parenthetical above — a `url` that greps to "0 or 2+ matches" is a failure — is scoped **per id**,
not globally. `"0 or 2+ matches = failure"` applies within a single record's own id scope: it
reads that record's own `corpus/SOURCES.md` row, so a hit count of zero or two-or-more is about
that one row's id token, not a whole-file or whole-registry count. A URL shared by two *different*
rows is informational (`multi_row_url=N`) and does not fail rule B; two rows carrying the same id
**do** fail, and the instrument names that `dup-id`. At the landed bytes `multi_row_url=2` is
exactly the two manifest records S029 and S006 (their URLs are also the S024 and S028 rows'
URLs), so the global reading would fail both and leave `bound=38` of 40 records, while the per-id
reading binds `records=40 bound=40 unbound=0`. The landed selftest pins both directions
(`case_duplicate_id_rows`, `case_shared_url_passes`). Erratum 1 remains the correction of record
for the round-33 counters; this block restates its reading in the kill rule's own words so the
frozen sentence and the measured reading no longer diverge on their face.

**Pre-freeze satisfiability step, recorded (QUALITY R22).** Before any claim is frozen, each
literal constant and regex in its predicate and kill rule is evaluated against the base bytes for
satisfiability. A literal that is unsatisfiable at base is corrected **before** dispatch, never
waived by a post-freeze erratum. Round 33 froze C1 with two such literals — "exactly one
registry-row URL" and "0 or 2+ matches" — both false against the two shared-URL pairs the registry
had carried since round 24, which is why erratum 1 and this erratum 2 had to be filed after
dispatch. `corpus/QUALITY.md` R22 is the appended criterion, grounded in the routed R2 defect
(`corpus/lessons/round-33-verifier-spotcheck.md` §5 R2) and mistake M34-2.

**C1 blind spots, recorded (not filed as failures).** `wave1/CritC1Kill.md` measures H1–H8:
capture bytes are not bound by the checker (truncated `S050.txt`, deleted `S049.txt` and a
`../` path all leave it exit 0), nested snapshot dirs vanish from the one-level walk,
`fetched_utc="pending"` discharges rule C, duplicate records inside one manifest audit clean, a
row with two `https://` tokens widens binding, and a `rejected` row can anchor a record. H1–H3
are covered by `source-recheck.py` (`40 :sha256 OK`, exit 0 each; mutants caught with
`MISMATCH` exit 1, `stem-mismatch` exit 1, `UNAVAILABLE` exit 2), which is why the after-column
cites that run; H4–H8 remain spec-level gaps. Also recorded rather than hidden: rule C's
`fetched_utc` is the capture-commit timestamp (round-32 manifest `purpose`), not a fetch
instant, and the instrument binds manifest metadata to registry text — it does not prove the
bytes came from the documented URL.

**C2 reviewer posture, reported verbatim for the canonical judge.** `wave1/RevEntryF16.md` §7:
`**ADMIT.**` on `53c48b3b…`, with three below-bar findings (no Chinese word-segmentation
instrument for the ≤25-word quote rule, `source:` anchor lists that summarise rather than
enumerate, and an unscoped whole-file grep reading 3 where the scoped one reads 1). The final
bytes `1f7ac0a2…` differ from the reviewed revision and have no second full Q1–Q10 review; the
lane-seat ADMIT plus the narrow-delta verification above is all the admission rests on. The one
residual content defect the critic reported on the intermediate revision (`entry:280` printing a
stale self-referential `grep` count) does **not** reproduce on the final bytes: this seat ran
that line's own scoped command once on committed `1f7ac0a2…`, and
`awk '/^## Attribution/{f=1} /^## What this adds/{f=0} f' <entry> | grep -c -E 'CVSS|0.85|时效评价|利用代码'`
returns `1`, while the unscoped whole-file grep returns `3` — the entry's printed literal is the
scoped value. That single command is this seat's own read of committed bytes, not a seat
receipt, and it is not a re-review. Also unapplied, and named as a gap rather than a kill: the
critic's request to commit the junk twin and its all-pass output under `c2-controls/` so the
reviewer clause has a control (`wave1/CritC2Kill.md` §6 item 3) — `c2-controls/` still holds
`before.txt` only.

**Measurement state.** Values above were measured at the wave-1 integration commit
`9f98488…` on quiescent bytes with per-seat bookend digests: `corpus/SOURCES.md`
`b22c7f01…` (50 rows), `corpus/README.md` `3779e77f…`, the F16 entry `1f7ac0a2…`,
`corpus/source-snapshots/round-32/manifest.json` `6e4e719a…`, the eight upgraded legacy
manifests `1f6d4fb5…` / `77b158ca…` / `251cb5b2…` / `1c913132…` / `89f51e05…` / `b24a485f…` /
`8aacf77c…` / `5fa37fd7…`, `corpus/instruments/capture-binding-check.py` `b4182665…`,
`corpus/instruments/frontier-recheck-count.py` `aa60b581…`, `source-recheck.py` `fd2e01e8…`,
`knowledge-expected.txt` `3f68b9a2…`, `SKILL.md` `b11b6085…`, `PROVINCE.md` `b57de5d9…`,
`corpus/QUALITY.md` `00781e09…`, `corpus/instruments/README.md` `15dd603e…`. Two in-flight
supersessions are recorded rather than compared: the entry moved `53c48b3b…` → `1f7ac0a2…`
after `ExecHarnessC2`'s bookend (which is why `ExecCensusAfter` prints a different entry digest
than that receipt), and `recheck-audit.py` printed `lines=44 … expected=44` at 04:16Z before the
wave's scribes landed, against `lines=45 … expected=45` after — the first is PRE-STATE and is not
an after column. The counters that C1's capability row depends on were measured by
`ExecRegressionC1` before any SCORECARD append existed (`wave1/ExecRegressionC1.md` D-R33-2);
this section is that landing.

**Capabilities: one row enters.** The C1 instrument is demonstrated running at its final
revision on committed bytes with the exit-0 output, its 11-case selftest, its base-byte failure
and its fake-checker rejection, and it is independently reviewed (`wave1/ExecRegressionC1.md`,
`wave1/ExecDeterminism.md`, `wave1/RevC1Instrument.md`, `wave1/CritC1Kill.md`), so
`capture-binding-check` enters the Capabilities table for round 33 — appended below as
`## Round-33 capabilities`, the round-24/25/26/31 pattern, because this seat is append-only and
does not edit the master `## Capabilities` table in place. The master table is otherwise
unchanged. Per the frozen C1 predicate the row is part of the claim, not a side note: it is the
one clause no counter could observe before this append.

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. The round-33
`capture-binding-check` entry restarts the capability window (previous entry round 31). With
depth:verifiability at 4 the lowest-axis obligation stays active.

## Round-33 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| capture-binding-check | Audit every committed capture snapshot in one pass: walk `corpus/source-snapshots/*/manifest.json`, flag any snapshot dir without a manifest (rule A), bind each record's `url` byte-exactly to its own `corpus/SOURCES.md` registry-row token with `no-row` / `dup-id` / `url-mismatch` / `detail=absent` failure names (rule B, per-id reading of erratum 1), and require `fetched_utc` for `round-32`+ dirs while accepting `archival: true` for older ones (rule C); print one `MANIFEST <round> records=N url_bound=M fetched=K archival=L` line per dir plus an `AUDIT` line and a `records=N bound=M unbound=0` summary, exit 0 / 1 / 2, run an 11-case `--selftest` (the six contract-named cases plus five) against fixture trees in `$HYAKU_SCRATCH`/`$TMPDIR` scratch that are removed at exit, and write nothing into the lane; stdlib only | `corpus/instruments/capture-binding-check.py` (sha256 `b4182665…`, 492 lines); `wave1/ExecRegressionC1.md` §1–§2 (`records=40 bound=40 unbound=0` twice byte-identically, `selftest cases=11 failures=0`, base bytes `unbound=38` exit 1, fake rejected); `wave1/RevC1Instrument.md` §9 `lands`; `wave1/ExecDeterminism.md`; blind spots and their `source-recheck.py` mitigation in `wave1/CritC1Kill.md` | 33 |

### Round-33 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 33 | depth:verifiability | 4 (no capture-binding instrument; 38 manifest records carry no `url`, none carries fetch provenance; the round-32 snapshot dir has no manifest; a summary-printing fake passes) | 4 held (`records=40 bound=40 unbound=0` exit 0 twice byte-identically, 9/9 dirs manifest-bound, 2 round-32 `fetched_utc` + 38 `archival: true`, `selftest cases=11 failures=0`, base bytes fail closed naming `dir=round-32`, fake rejected, 40 sha pins via `source-recheck`, no corpus regression) | `corpus/instruments/capture-binding-check.py`, the nine `corpus/source-snapshots/*/manifest.json`, `corpus/SOURCES.md`, `.ufo/waves/round-33/wave1/{ExecRegressionC1,ExecNoHarmFinal,ExecDeterminism,RevC1Instrument,CritC1Kill}.md` |
| 33 | coverage | 7 (frontier 15, entries citing S049/S050 0/0, registry 48, harness 18/18, manifest absent → recheck exit 2) | 7 held (frontier 16, entries citing 1/1, registry 50, census exit 0 with base warnings only, harness 19/19 incl. `PASS F16`, 14 quote assertions `occurrences=1` exit 0) | `corpus/README.md` F16 row, `corpus/SOURCES.md` S049/S050, `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md`, `corpus/source-snapshots/round-32/manifest.json`, `.ufo/waves/round-33/wave1/{ExecHarnessC2,ExecCensusAfter,RevRowS049,RevRowS050,RevEntryF16}.md` |

**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1). Every value in
this section was measured at the wave-1 integration commit `9f98488…` on the quiescent bytes
digested under § Measurement state; the closing commit may add seat receipts, `LOG.md`,
`SHONEN.md`, `corpus/lessons/round-33.md` and this section itself, none of which any counter
above reads.

Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33
final hash `7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7aa8c3c095ff57ae51097606a9906228c`
after the verifier spot-check commit); the placeholder token no longer occurs in this file, and
the round-34 closure check R1 reads that count as 0.

## Round 34 — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-34/claims.json` (base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims-freeze commit
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`, wave-1 spec/dispatch commit `206e5108f1190e61b3e2622d21cab8a5d921650c`),
together with the do-nothing controls committed at the freeze
(`c1-controls/fake-suite.sh`, `c1-controls/fake-killrule.py`, `c2-controls/junk-f17.md` +
`c2-controls/junk-checker.py`), the frozen before-controls (`c1-controls/before.txt`,
`c2-controls/before.txt`) and `census-before.txt`. **Final lane commit:
`c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1). This section is written at the
wave-1 integration state on the bytes digested under § Measurement state and originally carried the
placeholder prose this hash replaces; round-33 R1's defect recurred here in sentence form, which the
round-34 R1 check missed because it matched only the angle-bracket lane-hash marker, not this prose form
— the round-35 correction note at the end of this section records the substitution. Receipts land under
`.ufo/waves/round-34/` (`c1-controls/`, `c2-controls/`, `census-before.txt`, `claims-erratum-1.md`,
`assimilation/`, `wave1/`; 58 seat receipts at this seat's read). The last round heading at this round's
base is round 33, so C1's and C2's last-change column stays 33 and every before-column below is the
frozen control measured at this round's base bytes. The round-34 subject is instrument-soundness
closure for the nine round-33 verifier-routed defects R1–R9 (C1) and frontier F17 / Immunefi
Vulnerability Severity Classification System v2.2 (C2).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | suite absent (`ls_exit=2`); `capture-binding-check --selftest` **`cases=11 failures=0`**; two survivors of the frozen round-33 rule (`skip-selftest` summary mutant prints `selftest cases=0 failures=0` exit 0; `accept-record-without-url` prints `records=2 bound=2 unbound=0` exit 0); SCORECARD lane-hash markers **2**; round-32 `fetched_utc` `2026-10-25T23:14:00-03:00` ×2; round-26 manifest `records=1 paths=['S041.txt']` with `S040-live.txt` unlisted; `QUALITY.md` R20 `exactly one` ×1 with no appended note; no round-34 erratum in `corpus/lessons/round-33.md`; `frontier-recheck-count.py` rule A one-directional; no junk-twin control (`c2-controls/` absent at base); base-tree audit `records=40 bound=40 unbound=0 exit=0` (`c1-controls/before.txt`, `c2-controls/before.txt`, `.ufo/waves/round-34/census-before.txt`; base audit re-derived by `RevC1BeforeAfter` B8) | `bash corpus/instruments/r-defect-closure.sh` → nine `R# check=… open=0` lines, **`closed=9/9 exit=0`**; `--selftest` → nine `selftest case=R# live=pass fixture=rejected verdict=pass` lines, **`selftest cases=9 failures=0`**, exit 0; on base bytes **`closed=0/9 exit=1`** with a named reason per check; `capture-binding-check --selftest` → **`selftest cases=23 failures=0`** exit 0 (`3d9e5e0d…`, 892 lines), the nine named new cases present; plain audit **`records=41 bound=41 unbound=0 exit=0`** with `missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt` over ten snapshot dirs (erratum 1); `kill-rule-check.py` → `mutants=3 killed=3 survivors=0 invalid=0`, `gates=7 failed=0`, `controls=4 rejected=4`, **`survivors=0`**, exit 0 (`c279d952…`, 881 lines); lane-hash markers **0** + appended `Correction (round 34)` naming `7963976e`/`014ee2d`; round-32 manifest `fetched_utc` `2026-10-26T04:16:06Z`/`04:16:16Z` (`72ab4e68…`); round-26 manifest binds `S040-live.txt` as a declared `orphans` entry with `purpose` corrected (`33ac33c3…`); `QUALITY.md` gains the R20 note, R22 (pre-freeze satisfiability), R23 (reflection cadence) and R24 (per-case kill rule) (`77d99df9…`); `corpus/lessons/round-33.md` carries R7 (`:140`) and R4 (`:215`) errata (`f69472f3…`); rule A bidirectional with both limbs killed at mutation depth (`1be79af6…`); junk twin committed at freeze (`2752a994…`) and rejected | **Verified, score held 4.** Every frozen C1 counter is met on quiescent bytes and the failure direction is demonstrated: the suite reads `0/9` on base bytes, its `--selftest` fixture per case reintroduces that case's own round-33 defect, and the committed do-nothing controls reach the target summary without work (`fake-suite.sh` prints `closed=9/9` with no case table; `fake-killrule.py` prints `survivors=0` and is `opaque` against a real survivor witness). Mutation depth on top: 18/18 suite checks killed (`MutRSuiteChecks`), both rule-A limbs killed (`MutFrontierRuleA`), `skip-selftest` and `accept-record-without-url` killed by the new counter, and the counter's own false-zero route closed three ways (`ExecKillRuleCheck` §9). Independent re-derivation: `RevC1BeforeAfter` (before receipt honest, six counters match), `RevClaimsFreeze` (§3 battery MATCH incl. marker count 0), `RevRSuite`, `CritC1Kill`. Disclosures, not waivers, in the paragraphs below | 33 (held 34) |
| C2 | coverage (7) | `frontier_admitted=16`; registry rows **50**, `S051` rows **0**, entries citing `source: S051` **0**; harness `entries=19 pass=19 exit=0`; `source-recheck` on the absent round-34 manifest `manifest UNAVAILABLE reason=missing`, `recheck_exit=2`; census exit 0 with `W04 S028` + `W04 S029` only; `corpus/knowledge/*.md` 45; junk twin exists at freeze and its shape counters pass it 3/3 (`c2-controls/before.txt`, `c1-controls/fake-controls-receipt.txt`) | frontier admitted **17** (appended `## Round-34 admission` section, 26 inserted / 0 deleted); registry rows **51**, `S051` row **1** (`corpus/SOURCES.md:57`, tier A, `mined`, opened 2026-10-26, `used-by` the entry), 5 inserted / 0 deleted vs freeze; entries citing `source: S051` **1**; `corpus/knowledge/*.md` **46**; harness **`entries=20 pass=20 exit=0`** incl. `PASS F17 knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051 exit=0` and `declared_ids == recheck_ids == ['S051']`; `source-recheck --source S051` → `sha256 OK` + 18 assertions OK, **exit 0** (`4fd8ed98…` capture, `d5077f81…` manifest, `fetched_utc=2026-10-26T05:31:10Z`); census **exit 0** with exactly `W04 S028` + `W04 S029` + `ok`, six-command battery `rows=51 malformed=0 tier=A=48 B=1 C=2 status=mined=39 queued=9 rejected=3 dups=`; junk twin (`2752a994…`, committed at freeze) rejected when its fabricated sentence is checked against the committed capture (`MISMATCH reason=quote-not-found`, exit 1) and not admitted | **Verified on every frozen C2 counter, score held 7**, with two wording deviations disclosed rather than adopted: 16 of 18 assertions print `occurrences=1` and Q9/Q17 print `occurrences=2` under verified anchors `anchor=77-ok`/`anchor=96-ok` (the kill rule's `exit != 0` clause is unaffected), and the junk twin's own `recheck:` line exits 0 because it names the real manifest — the rejection lives in the reviewer-built manifest and in non-admission, not in the counter. Reviewer posture is reported verbatim below: `RevEntryF17` **ADMIT** on `948b202e…`, `RevRowS051` **matches**, `RevJunkTwin` **holds** on all four criteria, `RevCensus`/`RevC2BeforeAfter`/`ExecCensusAfter`/`ExecRegressionC2` all reproduce the counters, and `CritC2Kill`'s verdict is *"C2 holds as declared for the landed tree, and the gate is not provenance-sound"* (G1–G5) | 33 (held 34) |
| depth:density | 9 | mean **201.7**, 25 blocks, 710 path-citation instances (`SKILL.md` `b11b6085…`, 1090 lines — the round-33 final bytes) | mean **201.7**, 25 blocks, 710 cites, 1090 lines; `SKILL.md` and `PROVINCE.md` absent from `git diff --numstat 014ee2d7` (0 lines changed, both sides the same bytes); `anchorcheck.py SKILL.md` → `12 in-range cite instances, 0 bad`, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 (`RevNoHarm` §A–§C, the independent reviewer; no `ExecNoHarmFinal` receipt had landed at this seat's read) | **Unchanged (held 9), no harm, no move claimed.** The round adds instruments, manifests, lessons and registry rows and no `SKILL.md`/`PROVINCE.md` byte, so the density census reproduces round 33 exactly on the same committed instrument; every failure class in `anchorcheck.py` is at its recorded value, and the one authorised deletion set (2 lane-hash marker lines + in-place instrument/manifest replacements) is mapped to frozen-claim text line by line in `RevNoHarm` §A | r15 (held r34) |

**Erratum 1, disclosed (post-freeze, filed by the L1 before any scoring seat).** C1's counting
command named `records=40 bound=40 unbound=0` as the "unchanged C1 instrument baseline"; round-34's
own C2 capture adds the `S051` record, so the audit surface is 41 records. `.ufo/waves/round-34/claims-erratum-1.md`
rules the literal a round-33 scope note and keeps the invariant `bound=records, unbound=0, exit 0`:
measured **`records=41 bound=41 unbound=0 exit=0`**. Intermediate readings are labelled PRE-STATE and
are not after-columns: `records=41 bound=40 unbound=1 exit=1` with `FAIL rule=no-row record=S051`
(`ExecCaptureBindingHarden` §3, before the registry row landed — itself the proof that rule B binds a
record to its row) and `selftest cases=11 failures=0` in `ExecManifestR32Normalize` §4d, measured on
the round-33 instrument bytes before the hardening landed.

**C2 predicate wording, disclosed (no score change).** The frozen sentence "source-recheck S051 prints
every assertion occurrences=1" is not literally true: 16 assertions print `occurrences=1` and Q9/Q17
print `occurrences=2` with verified anchors, exit 0. `RevClaimsFreeze` D-2 files this as the same
summarization-beyond-measured-evidence class the round files as M34-1 and recommends an appended
claims erratum rewording the clause to "every assertion OK (`occurrences=1`, or `occurrences=2` with a
verified anchor for Q9/Q17), `sha256 OK`, exit 0". `ExecSnapshotR34` §6.2, `ExecRegistryAppend` §5,
`RevC2BeforeAfter` counter 6 and `CritC2Kill` §9 report the same measurement. This section reports the
measured shape and does not restate the literal.

**C1 blind spots, recorded (not filed as failures).** `CritC1Kill` attacks the landed instruments and
these survive, each named with its measured route: a two-edit self-mutation that rewrites the
counter's summary line still prints `survivors=0` (the header's `counter_sha256=` is printed but not
compared — bind the counter before trusting the zero; §3b); `fetched_utc` provenance is uncertifiable
by either instrument (any real calendar instant passes; the landed values are provenance-backed by
`ScoutLiveDrift`, which the instruments cannot see; §4); a snapshot directory with `"sources": []`
and every capture declared as an orphan prints `records=0 … unbound=0` at exit 0 — the degenerate
all-orphan route is outside rule A and outside R9 (`ExecRDefectClosureSuite` §11.7 states the same);
the marker check is spelling-brittle (a respelled placeholder passes R1); and the report-verifier's
case-line-count limb is implemented but not self-witnessed by a fixture
(`ExecCaptureBindingHarden` §Peer finding, `CritC1Kill` §Additional states). The kill-rule probe set
is a bounded oracle by construction, the comment-only survivor row is the deliberate instance, and the
suite's R1–R4/R6/R7 checks are presence tests whose fixtures prove they *can* fail, not that the prose
is truthful. C1's "committed" clause for the junk twin is also outside the suite, which reads bytes:
commit membership is the L1's/regression seat's check (`ExecRDefectClosureSuite` §11.3).

**C2 reviewer posture, reported verbatim for the canonical judge.** `RevEntryF17`:
**"ADMIT. The final bytes (`948b202e…`) satisfy Q1–Q10 on measured evidence"** — the earlier
`e71fbcd9…` bytes were superseded before verdict, so the earlier digest quoted in `ExecRegistryAppend`
§1 is PRE-STATE and not the reviewed entry. `RevJunkTwin`: **"the junk-twin control holds"** on
committed-at-freeze membership, shape counters 3/3, gate rejection, and entry-review non-admission;
`CritC2Kill` G5 records that the twin's own declared `recheck:` line exits 0 and that its quoted
sentence is partly real text from `S051.txt:75`, so G5's smallest correction is an erratum defining
the gate invocation. `CritC2Kill`'s residual gaps G1–G4 (no provenance binding, entry body unbound,
`mined` unbound to a capture, harness rule D may leave the tested root) are stated with a smallest
safe correction each and are not round-34 kill clauses. `RevRowS051` finds the row, Search-log bullet
and R8 lines truthful with two prose-only observations; `ExecHarnessAfter` F-A records that the README
F17 row had no owning seat and was appended under L1 authorization (26/0 lines, exactly one row).

**Measurement state.** Values above were measured on the wave-1 working tree with per-seat bookend
digests, and this seat re-read the digests below at the writing moment: `corpus/SOURCES.md`
`4c85ff86…` (105 lines, 51 rows), `corpus/README.md` `876be9cc…`, the F17 entry `948b202e…` (113
lines), `corpus/source-snapshots/round-34/manifest.json` `d5077f81…`, `round-34/S051.txt`
`4fd8ed98…`, `round-32/manifest.json` `72ab4e68…`, `round-26/manifest.json` `33ac33c3…`,
`capture-binding-check.py` `3d9e5e0d…` (892 lines), `r-defect-closure.sh` `357a7e49…` (688 lines),
`kill-rule-check.py` `c279d952…` (881 lines), `frontier-recheck-count.py` `1be79af6…` (433 lines),
`corpus/instruments/README.md` `d021b317…` (960 lines), `corpus/QUALITY.md` `77d99df9…` (228 lines),
`corpus/lessons/round-33.md` `f69472f3…`, `corpus/lessons/round-29.md` `4afb96be…`, `SKILL.md`
`b11b6085…`, `PROVINCE.md` unchanged, `c2-controls/junk-f17.md` `2752a994…`, `claims.json`
`dedb9ea8…` (byte-identical to the freeze commit's blob). Supersessions are recorded rather than
compared: `frontier-recheck-count.py` moved `87b14892…` → `8a79010d…` → `1be79af6…` (docstring and
README-reference only; `MutFrontierRuleA` ran its matrix at both later digests with identical
verdicts, and the author seat confirmed `1be79af6…` final); `QUALITY.md` moved `2bb724fb…` →
`77d99df9…` at the same 228 lines inside its own appended block; `r-defect-closure.sh` moved
`7aca98b3…` → `357a7e49…` between `RevClaimsFreeze`/`RevC1BeforeAfter` and
`ExecRDefectClosureSuite`'s final run, and the earlier R8 descriptor those receipts quote
(`^YYYY-MM-DDTHH:MM:SSZ$`) is the pre-parse generation — the landed R8 also requires a real
`datetime.fromisoformat` instant, added after `CritC1Kill` §4b showed a `…Tgarbage-not-a-timeZ` value
passing the frozen shape regex while rule C calls it `detail=malformed`; `kill-rule-check.py` churned
through seven generations, all named in `ExecKillRuleCheck` §0, with the final `c279d952…` the one the
quoted `survivors=0` run used. One worktree artefact outside the lane is reported, not adopted:
`RevNoHarm` §D found `/home/vgpnk/Projects/shokunin/baseline-plain.txt` (850 B, untracked, sha256
`56f08a92…`) written at the read-only fleet root during the wave — content-harm-free, a seat-scope
violation by an unattributable round-34 participant.

**Capabilities: no row enters this round.** `capture-binding-check` entered the table in round 33 and
its round-33 row's "run an 11-case `--selftest`" clause is superseded by the landed instrument's
**23 cases** (`selftest cases=23 failures=0`, `3d9e5e0d…`); per the L1's integration note that
supersession is recorded here as a note rather than an in-place edit of the round-33 row (this seat is
append-only), and the master `## Capabilities` table is otherwise unchanged. `r-defect-closure.sh` and
`kill-rule-check.py` are demonstrated to their own contract with base-tree failure directions and
mutation batteries, but their capability rows are the L1's decision, not this section's claim.

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. No capability entry enters this
round, so the capability window is not restarted (last entry round 33). With depth:verifiability still
at 4 the lowest-axis obligation stays active, and the C1 blind spots above are the route it points at.

### Round-34 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 34 | depth:verifiability | 4 (suite absent, `selftest cases=11`, two frozen-rule survivors, 2 markers, local-offset `fetched_utc`, unlisted S040 capture, one-directional rule A, no junk-twin control) | 4 held (`closed=9/9 exit=0` / `selftest cases=9 failures=0` / base `closed=0/9 exit=1`; `selftest cases=23 failures=0`; `survivors=0` with 7 gates and 4/4 controls; markers 0 + correction; strict-UTC round-32 stamps; S040 orphan declared; rule A bidirectional; junk twin committed and rejected; 18/18 suite mutants and both rule-A limbs killed) | `corpus/instruments/{r-defect-closure.sh,kill-rule-check.py,capture-binding-check.py,frontier-recheck-count.py}`, `corpus/source-snapshots/round-{26,32}/manifest.json`, `corpus/QUALITY.md`, `corpus/lessons/round-33.md`, `.ufo/waves/round-34/wave1/{ExecRDefectClosureSuite,ExecKillRuleCheck,ExecCaptureBindingHarden,ExecFrontierBidirectional,ExecScorecardMarkers,ExecErratum2,ExecQualityAppends,ExecLessonErrata,ExecS040Orphan,ExecManifestR32Normalize,RevC1BeforeAfter,RevClaimsFreeze,RevRSuite,MutRSuiteChecks,MutKillRuleMutants,MutFrontierRuleA,CritC1Kill}.md` |
| 34 | coverage | 7 (frontier 16, entries citing S051 0, registry 50, harness 19/19, round-34 manifest absent → recheck exit 2, junk twin uncommitted) | 7 held (frontier 17, entries citing 1, registry 51 with S051 row 1, harness 20/20 incl. `PASS F17`, `source-recheck S051` 18 assertions OK exit 0, census exit 0 with base warnings only, 46 knowledge entries, junk twin rejected by the reviewer-built manifest) | `corpus/README.md` F17 row, `corpus/SOURCES.md:57` S051 + `:77` Search-log bullet + `:103-105` R8 lines, `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, `corpus/source-snapshots/round-34/{S051.txt,manifest.json}`, `.ufo/waves/round-34/c2-controls/junk-f17.md`, `.ufo/waves/round-34/wave1/{ExecSnapshotR34,ExecHarnessAfter,ExecRegistryAppend,ExecCensusAfter,ExecRegressionC2,RevC2BeforeAfter,RevCensus,RevRowS051,RevEntryF17,RevJunkTwin,CritC2Kill}.md` |

**Round-34 final lane commit: `c1c6a5f826d2425446347173de527c42991b78b0`** (filled in round 35, D1).
Every value in this section was measured at the wave-1 integration state on the quiescent bytes
digested under § Measurement state; the closing commit may add seat receipts, `LOG.md`, `SHONEN.md`,
`corpus/lessons/round-34.md` and this section itself, none of which any counter above reads.

Erratum (round 35): the round-34 depth:density row measured 0 changed SKILL/PROVINCE lines and mean 201.7; at the tip each file had +1 appended correction line and the measured density mean is 201.2 (unchanged instrument, same definition).

Measurement state for the erratum above, so the two numbers stay bound to bytes: the 201.7 limb is
`git show 206e510:SKILL.md` (`b11b6085…`, 1090 lines, 710 path-citation instances, 25 blocks;
`PROVINCE.md` `b57de5d9…`, 74 lines) and the 201.2 limb is
`git show 3266c9937b03062d9bbc2f436e20820115ed179c:SKILL.md` (`ba5ebe5d…`, 1091 lines, 711 cites,
25 blocks; `PROVINCE.md` `b4bb5fee…`, 75 lines). The one line each comes from the round-34 closing
commit `4b0a9f2` (`diff` = `1090a1091` for `SKILL.md`, `74a75` for `PROVINCE.md`, both `[round-34
correction, appended 2026-10-26, end-of-file append per R6]`). Round-35 appends to `SKILL.md` move the
live-tree mean independently of this erratum — read both figures against the named blobs, not the
working tree (`density.py`, unchanged instrument, same definition).

Correction (round 35): the two lane-commit placeholder sentences above (the preamble's and the closing
paragraph's) were replaced with the round-34 final lane hash `c1c6a5f826d2425446347173de527c42991b78b0`
(the round-34 lane tip at its non-author closure). Neither placeholder spelling occurs in this file any
more; the round-35 closure check reads that count as 0. Nothing else in this section changed.

## Round 35 — frozen claims C1/C2 (2026-10-26)

| Axis | Before | After | Evidence |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 held — D1–D7 closure suite `closed=7/7 exit=0`, base `closed=0/7 exit=1`, `--selftest cases=7 failures=0` | `corpus/instruments/r35-defect-closure.sh` + `r35-fixtures/`; `.ufo/waves/round-35/wave1/{ExecClosureSuite,RevClosureSuite,RevSelftestFixtures,ExecBeforeReceipts,ExecDoNothingReject}.md` |
| coverage | 7 | 7 held — frontier 17→18 (F18 CISA KEV), registry 51→52 (S052), harness `entries=21 pass=21`, source-recheck S052 exit 0, census exit 0 | `corpus/README.md` F18 row, `corpus/SOURCES.md:58` S052, `corpus/knowledge/cisa-kev-catalog.md`, `corpus/source-snapshots/round-35/{S052.txt,manifest.json}` |
| depth:density | 9 | unchanged (no density claim; no-harm guard mean ≈ 201.2) | `wave1/ExecNoHarmFinal.md` |

Measurement state: base `3266c993…`, freeze `617496b9…`, wave-1 spec/dispatch `da2d3c68…`, integration `aa6ad99…`; final lane commit `0aee0ef…` (recorded in the closing commit).

Capabilities: no new capability row this round (the closure suite is a counter instrument; the capability window is not restarted — last entry round 33).

Move-log rows:

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 35 | depth:verifiability | 4 (D1–D7 open; suite absent) | 4 held (`closed=7/7`, base 0/7, selftest 7/7) | r35-defect-closure.sh; scorecard D1–D7 corrections; QUALITY R26/R27 |
| 35 | coverage | 7 (frontier 17, registry 51) | 7 held (frontier 18, registry 52, S052) | F18 row; S052 row; entry; capture/manifest |

Saturation unchanged: line 9/10 per owned axis, window N = 3. Lowest non-retired axis still depth:verifiability (4).

## Round 35 — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-35/claims.json` (sha256
`fe0dae8957c38f9c697b1b851a528bdf516f949f6ee3ba1ca2846e61d1ea2982`, `frozen_at_utc`
`2026-10-26T07:30:00Z`, attempt 1; base `3266c9937b03062d9bbc2f436e20820115ed179c`, claims-freeze
commit `617496b9c6e92bc671e7e78b83df69a04470d0e9`, wave-1 spec/dispatch commit
`da2d3c687f82a9814ee71c91c930cb733050d37c`, one v2 wave of 64 seats), together with the do-nothing
controls committed at the freeze (`c1-controls/fake-suite.sh` `292aaac0…`, `c2-controls/junk-f18.md`
`0abec359…`), the frozen before-controls (`c1-controls/before.txt` `352d3da2…`, `c2-controls/before.txt`
`28357003…`) and `census-before.txt` `74fc6a26…`. Receipts land under `.ufo/waves/round-35/`
(`c1-controls/`, `c2-controls/`, `census-before.txt`, `assimilation/`, `claims-erratum-d5.md`,
`wave1/`; 60 seat receipts at this seat's read). The last round heading at this round's base is round 34,
so C1's and C2's last-change column stays 34 and every before-column below is the frozen control measured
at this round's base bytes. The round-35 subject is instrument-soundness closure for the seven round-34
verifier-routed defects D1–D7 (C1) and frontier F18 / the CISA Known Exploited Vulnerabilities catalog
(C2).

**This section and the integration stub above it.** A 19-line `## Round 35` block carried by integration
commit `0aee0ef…` sits at `SCORECARD.md:1263-1281`, immediately before this section. It is not this
seat's text — no wave receipt claims it, and this seat wrote nothing to `SCORECARD.md` before this append
— and it is thin by construction: three table rows, a measurement-state line and a move-log pair, with no
per-defect evidence. This section is the receipt-grounded record and supersedes it; the closing commit is
the reconciliation point. One cell of the stub is contradicted by measurement and is restated in the guard
row below: its `depth:density` row reads `mean ≈ 201.2`, which is the lane-base blob's value, while the
landed `SKILL.md` measures **220.9** (byte binding in the guard row).

| Claim | Axis | Before | After | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | suite absent (`ls_exit=2`); lane-commit placeholder prose **1** line plus its second spelling **1**; `c1c6a5f` citations **0**; stale `201.7` depth:density-row lines **2**, corrected `201.2` **0**; `SKILL.md` registry greps **0 / 0**; results file tracked **0** and provenance note **0**; `claims-erratum-d5.md` absent; round-34 `L1Integration.md` dead-seat sentence **1**, `Correction (round 35)` **0**; `QUALITY.md` supersedes rows **0 0** (`c1-controls/before.txt`, reproduced 12/12 from the base export by `RevC1BeforeAfter` §2) | `corpus/instruments/r35-defect-closure.sh` (`0ae4b484…`, 834 lines, seven checks D1–D7, 17 clause mutants) reads `closed=7/7 exit=0` on the landed tree — `D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0`, `D2 …erratum-mean=3,row-bytes=1 open=0`, `D3 …registry-r-defect-closure=4,registry-kill-rule=4 open=0`, `D4 …tracked=1,provenance=1 open=0`, `D5 …discriminating-invocation=5,per-id-occurrences=5 open=0`, `D6 …dead-seat-sentence=0,correction-round-35=1 open=0`, `D7 …supersedes-R22=1,supersedes-R23=1 open=0` — and `--selftest` prints `selftest cases=7 failures=0` exit 0; the base export reads `closed=0/7 exit=1` and the committed fake suite is rejected by the suite's own judge (`judge=fake-suite rejected=1`, `judge=fake-plain rejected=1`, `judge=complete-report accepted=1`). Per defect: **D1** both marker spellings 0, round-34 tip hash on 3 lines, appended `Correction (round 35)`; **D2** appended erratum naming the corrected mean `201.2` plus a measurement-state paragraph binding both figures to blobs, stale row's opening bytes intact (`row-bytes=1`); **D3** `SKILL.md:1097-1098` rows for `r-defect-closure.sh` / `kill-rule-check.py`, greps 4 / 4, append `13 0`; **D4** `tracked=1,provenance=1` (results `3afa3581…`, 312874 B; note `e1c44301…`, 5639 B); **D5** erratum present, `discriminating invocation` ×5, `per-id occurrences` ×5; **D6** dead-seat sentence 0, `Correction (round 35)` 1; **D7** `supersedes R22` 1 / `supersedes R23` 1 in `QUALITY.md` (250 lines, `d4f83bb1…`) | **Verified, score held 4.** Both suite counters and all seven per-check payloads were read by this seat on the landed bytes at the writing moment (commands in `.ufo/waves/round-35/wave1/ScribeScorecard.md` §2); the base direction `closed=0/7 exit=1`, the all-fixed-tree `cases=7 failures=0`, the 17/17 mutant credit and the fake-suite rejection are `ExecClosureSuite` §4–§8 with `MutClosureSuite` (14/14 vacuous+delete mutants killed, no survivor) and `MutFixturesLimbs`; the eight per-defect landings are `ExecD1Markers`, `ExecD2DensityRow`, `ExecD3SkillRegistry`, `ExecD4ResultsTrack`, `ScribeErratumD5`, `RevD5D6D7`, `ScribeQualityDraft`, each re-derived by `RevD1D2`/`RevD3D4`/`RevD5D6D7`/`RevC1BeforeAfter`. Disclosed limits in the C1 blind-spots paragraph below | 34 (held 35) |
| C2 | coverage (7) | `frontier_admitted=17`; registry rows **51**, `S052` rows **0**, entries citing `source: S052` **0**; harness `entries=20 pass=20 exit=0`; `source-recheck` on the absent round-35 manifest prints `manifest UNAVAILABLE reason=missing`, `recheck_exit=2`; census exit 0 with `W04 S028` + `W04 S029` only; `corpus/knowledge/*.md` **46** (`c2-controls/before.txt`, reproduced cell-for-cell on a do-nothing export by `MutCounterBase` and `ExecDoNothingReject` §2) | frontier admitted **18** (`corpus/README.md` `277f04ce…`, `28 0`, F18 row); registry rows **52** with the `S052` row at `corpus/SOURCES.md:58` (kind `dataset`, tier A scoped to CISA's own catalog statements, status `mined`, opened 2026-10-26, recheck `90d`, used-by the entry), `5 → 7` insertions append-only, `rows=52 malformed=0`; entries citing `source: S052` **1** — `corpus/knowledge/cisa-kev-catalog.md` (91 lines, `e9de994d…`); capture `corpus/source-snapshots/round-35/S052.txt` (1479694 B, 27870 lines, `d69349e8…`, fetched `2026-10-26T06:32:40Z`, HTTP 200, requested URL == effective URL) with `manifest.json` `06bfcc71…` (5631 B, record S052, five assertions Q1–Q5 anchored at L2/L3/L4/L15472/L19165); harness **`entries=21 pass=21 exit=0`** including `PASS F18 knowledge/cisa-kev-catalog.md ids=S052 exit=0`; `source-recheck S052` **exit 0**, every assertion `occurrences=1`, `sha256 OK`; census **exit 0** with the two base warnings only; `corpus/knowledge/*.md` **47**; `knowledge-expected.txt` `d2e99ca6…` (47 rows) | **Verified, score held 7.** The five C2 counting commands were re-run by this seat on the landed bytes at the writing moment (receipt §2); the junk twin is rejected on the executable route, not on its own `recheck:` line: its two quoted sentences measure **0 / 0** occurrences in the pinned capture and the quote-comparison invocation prints `MISMATCH reason=quote-not-found` exit 1 (`ScribeErratumD5` §3, `ExecDoNothingReject` §3, `MutJunkTwin`), and it is not admitted (no row, no entry, non-author refusal on record). Reviewer posture and residual gaps in the C2 paragraph below | 34 (held 35) |
| depth:density | 9 | mean **201.2**, 25 blocks, 711 path-citation instances (`SKILL.md` `ba5ebe5d…`, 1091 lines — the lane-base blob; `PROVINCE.md` `b4bb5fee…`, 75 lines) | mean **220.9**, 26 blocks, 742 cites (`SKILL.md` `daeff71b…`, 1104 lines; `PROVINCE.md` byte-unchanged), the entire move carried by the EOF-appended block 26 — the D3 Gates & probes registry addition, 12 appended lines in an `13 0` diff, block dens 712.5 | **Unchanged (held 9), no harm, no move claimed.** Both sides measured with the committed `density.py` (`ee803726…`) on named bytes: base 201.2 / 25 / 711, landed 220.9 / 26 / 742. Zero existing `SKILL.md` lines changed, so no reflow or form-gaming is possible; the rise is one new block entering an unweighted mean. `anchorcheck.py SKILL.md` (`d0f35f8c…`, unchanged) reads `16 in-range cite instances, 0 bad; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0, so the verdict-class vector is unmoved (base: 12 in-range, same classes). `git diff --numstat` vs base: `SKILL.md 13 0`, `PROVINCE.md` and `LOG.md` unchanged, `corpus/README.md 28 0`, `corpus/SOURCES.md 7 0`, `knowledge-expected.txt 1 0`, and `SCORECARD.md 33 15` — the only non-append-only production file, whose 15 deletions are exactly the two round-34 placeholder paragraphs D1 was assigned to rewrite in place (`RevNoHarm` §A, `ExecNoHarmFinal` §3) | r15 (held r35) |

**One C1 clause was broken and repaired inside this round, and the repair is disclosed.** At integration
commit `0aee0ef…` the stub block above carried a lane-commit sentence that reprinted the D1 placeholder
verbatim, which re-armed C1's marker clause: on those bytes `r35-defect-closure.sh` read
`D1 check=placeholders=1,…,open=1` → `closed=6/7 exit=1`, i.e. the frozen kill rule
(`claims.json` → C1 `counting_commands[2]`, the literal must count 0) was live-broken by the integration
commit itself. The clause was then reworded in place to name `0aee0ef…` and assert nothing about the
closing commit; this seat measured the repaired tree (`placeholders=0`, `closed=7/7 exit=0`) and reports
the episode rather than the repaired-only state, because the class — a lane-commit sentence that quotes
the placeholder it is meant to remove — is the same one round-34's D1 filed and round-33's R1 before it.
No token of the placeholder is reproduced in this section.

**C1 blind spots, recorded (not filed as failures).** `CritC1Kill` attacks the landed suite and reports
that C1 "survives attack 1(a), the base control and attack 4's literal form; it does not survive attack
1(b), 2, 3 (check-level), 4 (with a mention present) or 5": nothing binds the counter's own bytes, so
"proved by the suite's own `--selftest`" is discharged by the artifact under test (its correction F-1 is a
one-command digest pin, the L1's to land); three of the seven clauses are file-wide literal greps a
negation or a heading satisfies; and the counter cannot see a *prose* placeholder spelling — the suite's
header records that limit, and the D1 clause covers the two literals the frozen kill rule names. `D2`'s
"no deletion" limb is byte survival of the row's opening, not a `git diff --numstat` deletion count,
because neither a `git archive` export nor a fixture tree can run git (`ExecClosureSuite` §2, finding 4).
`RevClosureSuite` and `RevSelftestFixtures` reviewed the suite mid-iteration (`c748dd70…` → `cba8c95b…` →
`d7ad8438…` → `a4f80067…` → `0ae4b484…`) and their two findings are in the landed bytes: the
fixture-detail judgement was anchored at `reason=` and would have rejected the honest report once the tree
went green (fixed to `reason=.*<clause>`), and D5's `erratum-file` clause had no mutant (fixed with a
cascading mutant). Both instruments also read the lane root by default: a copied-tree run reports
`BASE-ABSENT=11` on clean bytes (`ExecNoHarmFinal` F6), which is a verification-seat trap, not a defect.
The kill-rule probe set is a bounded oracle by construction, and the seven checks are presence tests whose
fixtures prove they *can* fail, not that the prose they read is truthful.

**C2 reviewer posture, reported verbatim for the canonical judge.** `RevEntryF18` first verdict:
**"REFUSE — one criterion: Q2, for Claim 4b only."** with both repair paths named; final verdict on the
landed bytes `e9de994d…`: **"ADMIT. Q1–Q10 all PASS"**, with two residual notes (the live-page
directive-status statement remains unregistered by design; the README frontier row was still 17 at that
review's check). `RevRowS052`: **"matches"** on the row, the Search-log bullet and the three R8 lines,
with per-criterion verdicts. `CritC2Kill` records five residual gaps, of which G5 is the one that matters
for the kill rule — `PASS F18 ids=S052` is binding + recheck, narrower than its name suggests — and the
frozen twin clause is only measurable through the quote-comparison invocation the D5 erratum defines;
`MutC2Entry` kills its entry-layer mutants (M1 dropped `source:` line → harness `no-source-line` exit 1;
M2a paraphrased quote → `quote-not-found` exit 1; M4 wrong `--source` → exit 1) and `MutJunkTwin` records
the twin's rejection. Two scope limitations are reported rather than repaired: the landed Search-log
bullet's sweep does not cover `corpus/lessons/*.md`, where one incidental token exists
(`corpus/lessons/round-22.md:91`), and the dispatch URL in the C2 ticket
(`https://www.cisa.gov/known-exploited-vulnerabilities.json`) returns HTTP 404 under three user agents —
the captured feed is the catalog's own JSON path, one directory over, and every registry, manifest and
entry byte carries that path.

**Measurement state.** Values above were measured at the wave-1 integration state (commits `aa6ad99…` and
`0aee0ef…` in the lane) with per-seat bookend digests, and this seat re-read every digest below at the
writing moment: `corpus/SOURCES.md` `0f95a132…` (112 lines, 52 rows), `corpus/README.md` `277f04ce…`
(396 lines), the F18 entry `e9de994d…` (91 lines), `corpus/source-snapshots/round-35/manifest.json`
`06bfcc71…` (5631 B) and `round-35/S052.txt` `d69349e8…` (1479694 B, 27870 lines),
`r35-defect-closure.sh` `0ae4b484…` (834 lines), `kill-rule-check.py` `c279d952…` (881 lines),
`frontier-recheck-count.py` `1be79af6…`, `source-recheck.py` `fd2e01e8…`, `knowledge-expected.txt`
`d2e99ca6…`, `corpus/instruments/README.md` `d021b317…` (960 lines), `corpus/QUALITY.md` `d4f83bb1…` (250
lines), `SKILL.md` `daeff71b…` (1104 lines), `PROVINCE.md` `b4bb5fee…` (75 lines), `claims.json`
`fe0dae89…` (byte-identical to the freeze blob), `.ufo/waves/round-34/wave1-results.json` `3afa3581…` and
its note `e1c44301…`. Supersessions are recorded rather than compared: `claims-erratum-d5.md` moved
`e2e7202d…` (06:38Z) → `0d304b92…` (06:41Z) → `eee0bb57…` (this seat's read) as its §5 attribution was
corrected from C2 to `C1.after[10]` (`RevD5D6D7` F5); the suite moved through the five digests named in
the blind-spots paragraph, and the quoted per-check payloads are the landed `0ae4b484…` run;
`corpus/README.md` and `corpus/SOURCES.md` both grew while the wave ran (`28 0` and `5 0 → 7 0`), the
final counts being 18 frontier rows and 52 registry rows. Two files are non-append-only this round and
both are disclosed above: `SCORECARD.md` (`33 15`, D1's assigned in-place rewrite) and the round-34
`wave1/L1Integration.md` (`3` deletions, the D6 correction, which the suite's own `dead-seat-sentence == 0`
clause forces to be in place rather than appended — `RevD5D6D7` §shape nuance).

**Capabilities: no row enters this round.** `r35-defect-closure.sh` is a defect-closure counter, not a
capability: it demonstrates seven *filed* defects closed and runs a 17-clause mutation battery, but it
adds no new thing the lane can do to the domain. The master `## Capabilities` table and the round-33 row
are unchanged, and the capability window is not restarted (last entry round 33).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. No capability entry enters this round,
so the capability window does not restart. With depth:verifiability still at 4 the lowest-axis obligation
stays active, and the C1 blind spots above are the route it points at; the round's own distance-to-next-
score measurement is filed in `.ufo/waves/round-35/wave1/ExecScoreGap.md` and minted as `QUALITY.md` R26.

### Round-35 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 35 | depth:verifiability | 4 (suite absent; seven D1–D7 defects open on the base export, `closed=0/7`; placeholder prose present; stale density row; gates unregistered; results file untracked; no D5 erratum; stale dead-seat sentence; no supersession rows) | 4 held (`closed=7/7 exit=0` / `--selftest cases=7 failures=0` / base `closed=0/7 exit=1`; 17/17 clause mutants credited, 14/14 vacuous+delete mutants killed; fake suite and fake plain rejected by the judge; seven per-defect payloads green) | `corpus/instruments/r35-defect-closure.sh`, `corpus/instruments/r35-fixtures/`, `SCORECARD.md` D1/D2 corrections, `SKILL.md:1097-1104`, `.ufo/waves/round-34/wave1-results.json` + `.provenance.md`, `.ufo/waves/round-35/claims-erratum-d5.md`, `.ufo/waves/round-34/wave1/L1Integration.md`, `corpus/QUALITY.md` R26/R27, `.ufo/waves/round-35/wave1/{ExecClosureSuite,MutClosureSuite,MutFixturesLimbs,ExecD1Markers,ExecD2DensityRow,ExecD3SkillRegistry,ExecD4ResultsTrack,ScribeErratumD5,RevD5D6D7,ScribeQualityDraft,RevC1BeforeAfter,CritC1Kill}.md` |
| 35 | coverage | 7 (frontier 17, registry 51, entries citing S052 0, harness 20/20, round-35 manifest absent → recheck exit 2, knowledge 46, junk twin committed and unadjudicated) | 7 held (frontier 18, registry 52 with the S052 row, entries citing 1, harness 21/21 incl. `PASS F18 … ids=S052`, `source-recheck S052` five assertions `occurrences=1` exit 0, census exit 0 with the two base warnings only, knowledge 47, junk twin rejected on the quote-comparison route) | `corpus/README.md` F18 row, `corpus/SOURCES.md:58` + `:79` + `:108-110`, `corpus/knowledge/cisa-kev-catalog.md`, `corpus/source-snapshots/round-35/{S052.txt,manifest.json}`, `corpus/instruments/knowledge-expected.txt`, `.ufo/waves/round-35/c2-controls/junk-f18.md`, `.ufo/waves/round-35/wave1/{ExecC2Capture,ExecRegistryAppend,ExecExpectedListSync,ExecDoNothingReject,MutCounterBase,MutC2Entry,MutJunkTwin,RevEntryF18,RevRowS052,RevC2BeforeAfter,CritC2Kill}.md` |

**Round-35 integration commits: `aa6ad99…` (C1 D4/D6/D7 landings) and `0aee0ef…` (integration: lesson,
scorecard stub, SHONEN, LOG, wave receipts, assimilation artifacts).** The closing lane commit is not
known at this seat's read and is not asserted here; every counter above reads committed content and does
not depend on it. Every value in this section was measured on the wave-1 integration bytes digested under
§ Measurement state; the closing commit may add seat receipts, `LOG.md`, `SHONEN.md`,
`corpus/lessons/round-35.md` and this section itself, none of which any counter above reads.

## Round 36 — frozen claims C1/C2 (2026-10-26)

Frozen before dispatch in `.ufo/waves/round-36/claims.json` (sha256 `a6405e71…`, `frozen_at_utc`
`2026-10-26T15:33:19Z`, attempt 1; base `cc692008b0cfd58d18275aa6c4aed79620120799`, claims-freeze commit
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`), together with the frozen before-controls
(`c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…`) and `census-before.txt`
`920e6fd4…` (three lines: `W04 S028`, `W04 S029`, `ok`). No do-nothing control pair was committed at this
freeze: `c1-controls/` carries `before.txt` only, and the round-36 junk twin `c2-controls/junk-f19.md` is a
claim output rather than a base artefact, so the two frozen before-files are the entire control surface.
Receipts land under `.ufo/waves/round-36/` (`c1-controls/`, `c2-controls/`, `census-before.txt`,
`assimilation/`, `wave1/`); `wave1-spec.json` dispatches 64 items. The last round heading at this round's
base is round 35, so C1's and C2's last-change column stays 35 and every before-column below is the frozen
control measured at this round's base bytes. The round-36 subject is instrument-soundness closure for the
routed defects of the round-35 verifier spot-check (§5, six items) plus the standing closure-order defects
(C1), and frontier F19 / FIRST EPSS exploitation-likelihood scoring (C2).

| Claim | Axis | Before (frozen control) | After (expected) | Verdict and evidence | Last change |
|---|---|---|---|---|---|
| C1 | depth:verifiability (lowest non-retired, 4) | suite absent (`suite_missing=1`); `SKILL.md` Gates & probes exact basenames `r35-defect-closure.sh` **0** and `r36-closure.sh` **0** (`r-defect-closure.sh` **3**); round-35 `wave1-results.json` tracked **1** with a beside-provenance note **0**; `claims-erratum-d5.md` present **1**; `L1Integration.md` `Correction (round 35)` **1** and the dead-seat sentence **0**; `QUALITY.md` `supersedes R22` **1** / `supersedes R23` **1**; round-34 depth:density erratum `201.2` **6** and its heading **1**; round-36 lesson absent (`git ls-tree` **0**); placeholder-token greps **0 / 0** (`placeholder_filled=0`, `placeholder_angle=0`); `worktree_clean=0`, `scratch_leftovers=0` | **expected:** `corpus/instruments/r36-closure.sh` committed, run over a `git archive` export of the round-36 lane head (`--export-ref`), printing `closed=9/9 exit=0`, with `--selftest cases=9 failures=0`; round-35 base export `3266c993…` `closed=0/9 exit=1`; round-35 judged head export `0aee0ef…` `closed<9/9 exit=1`; E3 registers both exact basenames; E4 adds the provenance note beside the round-35 results; E5/E6/E7 retained; E8 records the false-evidence-line correction in `corpus/lessons/round-36.md`; E9 quiescent at filing | **pending measurement.** The suite is absent at this seat's read (`git ls-tree -r --name-only b47f2cd -- corpus/instruments/r36-closure.sh` returned 0 paths), so no after value is measured here; the deciding commands are listed under § Verdict state | 35 |
| C2 | coverage (7) | frontier admitted **18** (`corpus/README.md` F-rows, last F18); registry rows **52** (last S052 at `:58`), `S053` rows **0**, entries citing `source: S053` **0**; harness `entries=21 pass=21 exit=0`; `corpus/knowledge/*.md` **47**, no EPSS entry on disk; census exit 0 with `W04 S028` + `W04 S029` only; `junk_present=1` as the frozen control states it | **expected:** frontier **19** (F19 row); registry **53** with the `S053` row; entries citing `source: S053` **1** (`corpus/knowledge/epss-exploit-prediction-scoring.md`); harness `entries=22 pass=22 exit=0` including `PASS F19 ids=S053`; `source-recheck S053` exit 0 against the round-36 manifest; `capture-binding-check.py` exit 0 with the S053 record bound; census exit 0 with the two base warnings only; knowledge **48**; the junk twin `c2-controls/junk-f19.md` rejected (quote-not-found / non-admission) | **pending measurement.** At this read the counters still print the before values (18 / 52 / 47 / 21-21), so every after value is the frozen contract's expected state | 35 |
| depth:density | 9 | mean **220.9**, 26 blocks, 742 path-citation instances (`SKILL.md` `daeff71b…`, 1104 lines; `PROVINCE.md` `b4bb5fee…`, 75 lines) | **expected no move:** any `SKILL.md` change is an EOF-appended Gates & probes block (E3's two registrations), every existing line byte-identical, `PROVINCE.md` unchanged | **no move claimed; no-harm guard pending measurement** on the same committed `density.py` (`ee803726…`) and the same definition | 35 |

**Verdict state.** Every after-cell above is the frozen contract's expected state, not a measurement: at
this seat's read `r36-closure.sh` is absent, the harness prints `entries=21 pass=21 exit=0`, and the three
coverage counters print 18 / 52 / 47. The commands that decide the verdicts, one per line, so closure
appends verdict lines instead of rewriting the table:

    bash corpus/instruments/r36-closure.sh --export-ref "$ROUND36_HEAD"           -> closed=9/9 exit=0
    bash corpus/instruments/r36-closure.sh --export-ref 3266c9937b03062d9bbc2f436e20820115ed179c -> closed=0/9 exit=1
    bash corpus/instruments/r36-closure.sh --export-ref 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -> closed<9/9 exit=1
    bash corpus/instruments/r36-closure.sh --selftest                          -> cases=9 failures=0
    grep -cE '^\| F[0-9]+ \|' corpus/README.md                                 -> 19
    grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md       -> 53
    python3 corpus/instruments/frontier-recheck-count.py                       -> entries=22 pass=22 exit=0
    python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053 -> exit 0
    python3 corpus/instruments/capture-binding-check.py                        -> exit 0
    ls corpus/knowledge/*.md | wc -l                                           -> 48

**Measurement state (round-36 template, values re-read at this draft).** Base `cc692008…`; claims-freeze
commit `b47f2cd…`; `wave1-spec.json` / `wave1-dispatch.json` are the freeze worktree's untracked files, so
no spec/dispatch commit hash is asserted; the wave-1 integration commit, the `r36-closure.sh` digest and
line count, and the round-36 lane-commit anchor are recorded by appended lines at closure, not here.
Harness at this draft: `entries=21 pass=21 exit=0`; expected after: `entries=22 pass=22 exit=0`. Digests on
the freeze bytes: `corpus/SOURCES.md` `0f95a132…` (112 lines, 52 rows), `corpus/README.md` `277f04ce…`
(396 lines, 18 F-rows), `corpus/QUALITY.md` `d4f83bb1…` (250 lines), `SKILL.md` `daeff71b…` (1104 lines),
`PROVINCE.md` `b4bb5fee…` (75 lines), `corpus/instruments/r35-defect-closure.sh` `0ae4b484…` (834 lines),
`capture-binding-check.py` `3d9e5e0d…`, `source-recheck.py` `fd2e01e8…`,
`frontier-recheck-count.py` `1be79af6…`, `knowledge-expected.txt` `d2e99ca6…`, `density.py` `ee803726…`,
`claims.json` `a6405e71…`, `c1-controls/before.txt` `14213f1a…`, `c2-controls/before.txt` `802091d7…`,
`census-before.txt` `920e6fd4…`; `SCORECARD.md` 1404 lines at this draft. Supersessions, if the wave
produces any, are recorded as appended lines naming both digests rather than compared.

**Capabilities: no row enters this round.** `r36-closure.sh` is a closure counter — it demonstrates nine
named defects closed on an exported head — not a new thing the lane can do to the domain. The master
`## Capabilities` table and the round-33 row are unchanged, and the capability window is not restarted
(last entry round 33).

**Saturation unchanged:** line 9/10 per owned axis, window N = 3. No capability entry enters this round,
so the capability window does not restart. The lowest non-retired axis remains **depth:verifiability (4)**;
the round's own distance-to-next-score reading is the L1's to file, and with C1 held 4 by design that
obligation stays active after this round.

### Round-36 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 36 | depth:verifiability | 4 (suite absent; E3 both registrations absent; E4 provenance note absent; E8 lesson absent; E2/E5/E6/E7 already present as guards; placeholder greps 0/0 at base) | 4 held — **expected** (`closed=9/9 exit=0` on the round-36 lane-head export, `--selftest cases=9 failures=0`, round-35 base export `closed=0/9`, round-35 judged head export `closed<9/9`; two registry rows; provenance note; lesson correction; quiescence) — **pending measurement** | `corpus/instruments/r36-closure.sh`, `SKILL.md` Gates & probes registry, `.ufo/waves/round-35/wave1-results.json` + provenance note, `corpus/lessons/round-36.md` |
| 36 | coverage | 7 (frontier 18, registry 52, S053 rows 0, knowledge 47, harness 21/21) | 7 held — **expected** (frontier 19, registry 53, one entry citing S053, harness 22/22 incl. `PASS F19`, recheck and binding exit 0, census exit 0, knowledge 48, junk twin rejected) — **pending measurement** | `corpus/README.md` F19 row, `corpus/SOURCES.md` S053 row, `corpus/knowledge/epss-exploit-prediction-scoring.md`, `corpus/source-snapshots/round-36/{S053.txt,manifest.json}`, `.ufo/waves/round-36/c2-controls/junk-f19.md` |

**Contract risks recorded at draft time (not filed as failures).** Three structural points the closure
seat and the suite author must settle, each measured on the freeze blob: (i) the quiescence check closes on
any export if it reads live-lane status alone — `git status --porcelain` is empty at `b47f2cd` and no
round-36 scratch seat dir exists before dispatch — so the frozen base-export limb `closed=0/9` requires an
E9 leg that is false at `3266c993…`, e.g. binding the exported ref to the lane head recorded at filing or
requiring the export to carry the round-36 lesson; (ii) a lane-commit anchor line cannot cite the commit
that contains it, so the round-36 anchor must name the integration commit or an earlier ancestor (verified
with `git cat-file -e` and `git merge-base --is-ancestor`) and is appended at closure — this block therefore
asserts no closing commit; (iii) `E3` reads exact basenames, and the freeze `SKILL.md` registers
`r-defect-closure.sh` only, so the older suite needs its own `r35-defect-closure.sh` row, not a reworded
`r-defect-closure.sh` row.

**The closing lane commit is not known at this seat's read and is not asserted here.** Every value in this
section was measured on the claims-freeze bytes digested under § Measurement state; the closure may add
seat receipts, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-36.md` and this section itself, none of which
any counter above reads.

Final lane commit: e666d902337a49dcbfc77880939874f39c6f477b

**Round-36 measured closure (appended after integration).** Measured at the final lane head `274fa9ae908db5800013778098f4d426281b46e2` (export run): `r36-closure.sh --export-ref 274fa9ae…` -> `closed=9/9 exit=0`; `--selftest` -> `cases=9 failures=0`; negative controls `3266c993` -> `closed=0/9 exit=1`, `0aee0ef` -> `closed=3/9 exit=1`; C2 counters: frontier rows 19 (`grep -cE '^\| F[0-9]+ \|' corpus/README.md`), registry rows 53 (`S053` row present), entries citing `source: S053` 1, knowledge files 48, harness `entries=22 pass=22 exit=0` incl. `PASS F19 … ids=S053`, `source-recheck --source S053` exit 0 (Q1–Q4 `occurrences=1`), `recheck-audit.py` `strict pass=48/48 … expected=48` exit 0, `capture-binding-check.py` `records=43 bound=43` exit 0, census exit 0 (W04 S028/S029 only). Disclosed limits: the integrated suite's limbs are presence/shape tests; three post-integration attack fixtures are kill-rule-hit classes (E3 retraction-section row, E7 negation row, E8 two bare tokens) plus the wider CritC1Kill matrix — recorded in `corpus/lessons/round-36.md` and `ExecC1SuiteBuild.md` § Post-integration residuals, round-37 backlog.
