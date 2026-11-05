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

## Round 37 result

| Axis | Score before r37 | Score after r37 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 (held) | `r37-closure.sh` export suite E1–E14: `closed=14/14 exit=0` at the r37 final lane head; `--selftest` `cases=14 failures=0`; r36 base cc692008 export `closed<14/14 exit=1`; r36 judged head a23dc478 export `closed<14/14 exit=1`. Round-36 verifier routed defects D1–D6 closed (receipt `.ufo/waves/round-37/final-gates/all-gates.txt`). | r37 (held) |
| coverage | 7 | 7 (held) | Frontier F20 (SSVC) admitted 19→20; registry S054 row added (53→54, tier A, mined, opened 2026-10-26); entry `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` cites `source: S054`; harness `entries=23 pass=23 exit=0` incl. `PASS F20 ids=S054`; source-recheck S054 exit 0; census exit 0 (W04 S028/S029 only); knowledge 48→49; junk twin `c2-controls/junk-f20.md` rejected. | r37 (held) |
| depth:density | 9 | 9 | Non-target guard only: SKILL.md append-only (registry rows only); no density move claimed. | r15 (held r37) |

Measured before commit (freeze `224df74d…`): c1-controls/before.txt, c2-controls/before.txt, census-before.txt.
Measured after: `bash corpus/instruments/r37-closure.sh --export-ref aa88877bf921d952137817b91ca76234b206da65` → `closed=14/14 exit=0`; `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → 20; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 54; `python3 corpus/instruments/frontier-recheck-count.py` → `entries=23 pass=23 exit=0`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-37/manifest.json --source S054` → exit 0; `python3 corpus/instruments/capture-binding-check.py` → `records=44 bound=44 unbound=0`; `python3 corpus/instruments/recheck-audit.py --quiet` → `strict pass=49/49 … expected=49 missing=0 unexpected=0 exit=0`; census exit 0.

Anchor ancestor (r36 lane head): `c20300df516eb5575d8db2aaad1f0cf4913e7981` — the r36 Final-lane-commit label previously pointing at the intermediate ancestor e666d902 is corrected per E12 (see round-37 lesson).

Final lane commit: f3246559bed2fd085dde860e00247ce394f02bad (round-37 wave-evidence ancestor; the round's final head is named in the report).

Correction (round 38): the round-37 section's `Final lane commit: f3246559…` line names a wave-evidence anchor ancestor, not a final head; read it as `Anchor ancestor (r37 wave evidence): f3246559bed2fd085dde860e00247ce394f02bad`; the round-37 judged head is 2387dcf6ccfefcfb703783387b9aade8fc82abfa and its tip 83975acc83df4bd8d5eaf463182ae615f2b64546 (verifier §5 D-D).

## Round 38 result

| Axis | Score before r38 | Score after r38 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 (held) | `corpus/instruments/r38-closure.sh` (sha256 `85d33ea9…`, export-mode suite G1–G8) closes the round-37 verifier's routed D-A, D-B, D-C, D3, D-D, D-E and the L1-found D-F; the run over the round-38 head the receipt names, and its `--selftest`, are committed in `.ufo/waves/round-38/final-gates/all-gates.txt`; reds over the base `a173b0c2` and the round-37 verifier's reviewed head `2387dcf6` exports are committed in `.ufo/waves/round-38/final-gates/reds.txt`. | r38 (held) |
| coverage | 7 | 7 (held) | Frontier F21 (OASIS CSAF v2.0 — VEX product-status categories and not-affected justification flags) 20→21; registry S055 54→55 (tier A, kind spec, mined, opened 2026-10-26); entry `corpus/knowledge/csaf-vex-product-status-and-justifications.md` (`source: S055`); capture `corpus/source-snapshots/round-38/S055.txt` (sha256 `63c8ad52…`, 5146 lines) + `manifest.json`; harness `entries=24 pass=24 exit=0` incl. `PASS F21 … ids=S055`; `source-recheck --source S055` exit 0; binding `records=45 bound=45 unbound=0`; audit `expected=50 missing=0 unexpected=0 exit=0`; census exit 0 (W04 S028/S029 only); knowledge 49→50; junk twin `.ufo/waves/round-38/c2-controls/junk-f21.md` rejected (`junk-f21-recheck.txt`: 4× `quote-not-found`, exit 1). | r38 (held) |
| depth:density | 9 | 9 | Non-target guard only: `SKILL.md` gains one EOF Gates & probes row (`r38-closure.sh`); every base line byte-identical; no density move claimed. | r15 (held r38) |

Measured before: claims-freeze commit `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b` (`.ufo/waves/round-38/c1-controls/before.txt`, `c2-controls/before.txt`, `census-before.txt`).
judged head: export-ref of .ufo/waves/round-38/final-gates/all-gates.txt
The C2 values above were measured on the integrated tree that the judged head commits; the C1 run is the receipt itself. This section names no hash for the round-38 head: a commit cannot contain its own hash (QUALITY R33), and the lane tip adds only the receipt file.

**Capabilities: no row enters this round.** `r38-closure.sh` is a closure counter, not a new domain capability; the capability window is unchanged (last entry round 33). **Saturation unchanged:** line 9/10 per owned axis, window N = 3; the lowest non-retired axis stays depth:verifiability (4), which C1 worked.

**Planned for round 39** (appended plan, not a claim): (1) depth:verifiability — an r39 suite that turns the
round-38 attack findings into fixtures and tightened limbs (whole-tail declarations, graded selftest case
lines, seat-identity G4, the four MutG5G8 fixture gaps, pinned r37 bytes for G8); (2) coverage — continue
the frontier from opened VEX/advisory leads (`wave1/ScoutVexLeads.md`) only after re-opening them in-round.

## Distance-to-next-score (round 39, mined from considerthese 2026-10-26 proposal 1)

Mined from `considerthese/2026-10-26.md` proposal 1 ("Make 'distance to next score' explicit"), written 2026-10-26, and landed in round 39. This section states the two promotion bars as criteria a non-author can re-run, and the measured distance at round-39 base `480b1a505a2dfc14a4f718d16d63808247214d0a`. It asserts no score move: a measured distance is not a claim that a score is due, and every figure below is the printed output of the command beside it.

### depth:verifiability, 4 → 5

Both limbs must read at the judged head:

1. **0 gated rechecks.** `python3 corpus/instruments/recheck-audit.py --root . --quiet` prints `executes=<n> gated=0 broken=0` together with `lines=<n> total=<n> pass=<n> ... parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`. A `gated` line is one that runs and fails closed, either on an absent base (`test -d ~/Projects/...`) or on a `LOST-RECORDED` anchor; it is an unsupported current claim until its base exists or its anchor is re-based.
2. **The score-5 audit bar.** `SCORECARD.md:331`: "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims." The dispositions row that restates it is `corpus/knowledge/considerthese-proposals-ledger.md:54`.

**Measured at base** (`python3 corpus/instruments/recheck-audit.py --root .`): `strict pass=50/50 cdroot_fail=0 instrument_fail=0 own_fail=0`, `executes=26 gated=24 broken=0`, `lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`. `python3 corpus/instruments/score-gap.py` prints `gap: 24 of 50 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.

**Distance: 24 gated lines to 0.** 23 of the 24 open with a `test -d ~/Projects/...` guard; all 23 name `~/Projects/bounties` (one of them its `.git`), 6 also test `~/Projects/the-bounty-hunter` and 1 also `~/Projects/origin-work`. The 24th, `corpus/knowledge/citation-bases.md`, fails `anchorcheck.py` on a `LOST-RECORDED` anchor (`md:52`) and a `BASE-ABSENT` anchor (`md:31`). The 23 guards fail on the absent trees (`PROVINCE.md:5-19`), so they turn green only when a base exists; an entry could instead be re-grounded on a committed capture or have its anchors marked `LOST-RECORDED`, and neither has been done for these 23 because it changes what the recheck proves. The lane's reachable half is negative-only: do not add a gated line.

### coverage, 7 → 8

**Criterion** (the r22 measure, `SCORECARD.md:332`; planned for adoption at `SCORECARD.md:178` and never adopted — round 23 kept the r15 denominator, `corpus/lessons/round-23.md:173-177`):

`(20 + F_admitted) / (20 + F_total) = 1.000`, with `F_total` = frontier rows in `corpus/README.md` § Frontier (`grep -cE '^\| F[0-9]+ \|' corpus/README.md`) plus every `corpus/SOURCES.md` registry row still `queued` (an unmined in-scope source stays an uncovered surface until its row is admitted as a frontier topic or rejected with reason and flip — the r23 audit's own point, `.ufo/waves/round-23/build/CoverageDenom.md` § Finding 4), `F_admitted` = those frontier rows whose status cell is `admitted` (`awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md`), and every admitted row's entry passing `python3 corpus/instruments/frontier-recheck-count.py` (`pass` equal to `entries`, exit 0). The Core term stays 20: it is the r22 proposal's constant with no per-item derivation in the lane (`git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/` returns only `SCORECARD.md:332`), so it holds and the frontier and queued terms carry the move.

**Measured at base**: `F` rows 21, admitted 21, non-admitted 0, queued registry rows 9 (S016, S017, S019, S020, S021, S022, S023, S024, S025), so `F_total = 30` and `(20+21)/(20+30) = 41/50 = 0.820`; `frontier-recheck-count.py` prints `entries=24 pass=24 exit=0`. The frontier-only reading gives `(20+21)/(20+21) = 41/41 = 1.000`: numerator and denominator grow together because every topic enumerated so far was admitted in the round that enumerated it, so that reading cannot discriminate 7 from 8 and is not the criterion.

**Distance: 9 queued rows to 0.** 7 are unmined public sources (S016, S017, S019, S020, S021, S023, S025); 2 are superseded-but-unflipped (S022 by S030, S024 by S029) and need a rejected-with-flip row, not new mining. Both exits are in-lane work. A separate cap stays operator-owned: the adopted r15 denominator holds `0/18` domain surfaces present (`corpus/README.md:55-56`, `PROVINCE.md:121-122`), so the ratio above measures the corpus-facing half of coverage only.

**gap@r39:** depth:verifiability `gated=24` of `lines=50` (5 needs 0) · coverage `41/50 = 0.820` strict, `41/41 = 1.000` frontier-only (non-discriminating) · coverage's operator half `0/18` domain surfaces present.


Correction (round 39): the `## Round 38 result` depth:verifiability row overstates the run at the judged head. Its clause "the run over the round-38 head the receipt names, and its `--selftest`, are committed in `.ufo/waves/round-38/final-gates/all-gates.txt`" holds only for the receipt's `run-ref`: the receipt's `export-ref` (`:2`) is J = `66703acaaff50529a35be49aa8759d04140720ad`, and the run over J prints `export-ref-run: closed=7/8 exit=1` with G2 `closed=0` (`:8`, `:15`); the `closed=8/8 exit=0` (`:26`) and `selftest cases=8 failures=0` (`:73`) lines are over `run-ref=7dd2fcd67aa8d3f67616e9fa79049c7c33c3ea8e` (`:4`). Read the row as: eight of eight checks pass over the receipt's run-ref and exactly one (G2) is red over J, structurally, because J cannot contain the receipt that names it. The report's tip run over `f06148c66c6d7aed948cb7024d9f0b9cffe4b95a` (J plus the receipt file only: `git diff --name-only J Y` → `.ufo/waves/round-38/final-gates/all-gates.txt`, `git diff --numstat` 79/0) quoting `closed=8/8 exit=0` and `selftest cases=8 failures=0` is report-quoted only — no committed transcript exists, and `git grep f06148c6` over the tip's tree → 0 hits (exit 1), since the tip cannot carry its own run. Scores unchanged (depth:verifiability 4, held r38); this line corrects the evidence sentence, not the score (non-author verifier `corpus/lessons/round-38-verifier-spotcheck.md` §5 R2, R3).


## Round 39 result

| Axis | Score before r39 | Score after r39 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 (held) | `corpus/instruments/r39-closure.sh` (sha256 2856a210d7838e61ea68e1867b76693abd00916307dea5b830c8574298b4222b), suite G1-G8 closes R1-R4 + attack findings; judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt (claims-erratum-1.md E4); `closed=8/8 exit=0` at Y, graded `selftest cases=8 failures=0`; base/r38-head reds. | r39 (held) |
| coverage | 7 | 7 (held) | Frontier F22 (CISA When to Issue VEX Information) 21->22; registry S057 + rejected S056/S058/S059 (55->59); entry corpus/knowledge/cisa-when-to-issue-vex.md cites S057; harness entries=25 pass=25 incl PASS F22 ids=S057; source-recheck S057 exit 0; binding 46/46; audit expected=51; census exit 0; knowledge 50->51; junk twin rejected. | r39 (held) |
| depth:density | 9 | 9 | Non-target guard only: SKILL.md append-only (one registry row r39-closure.sh); no density move claimed. | r15 (held r39) |

Measured before: claims-freeze commit dcd31701720a6a4929a32471a62011ed87103421 (before-controls). Measured after: see the counting commands in `.ufo/waves/round-39/claims.json` + erratum E1/E2/E4/E5; outputs recorded in `.ufo/waves/round-39/final-gates/` and the C2 recheck receipts.

Judged head: export-ref of .ufo/waves/round-39/final-gates/all-gates.txt (claims-erratum-1.md E4).

**Capabilities: no row enters this round** (r39-closure.sh is a closure counter). **Saturation unchanged:** line 9/10, window N=3; lowest non-retired axis depth:verifiability (4) stays worked.

**Planned for round 40**: (1) depth:verifiability — carry the wave-2 attack findings into r40 fixtures/limbs; continue the 0-gated distance (score-gap measured 24 gated lines; needs external bases or re-grounding). (2) coverage — open the remaining leads (CISA VEX Status Justifications PDF; CSAF v2.1 os/ status; CycloneDX analysis subtree scoped capture) and decide the 9 queued registry rows per the distance-to-next-score criterion.

Correction (round 39): the round-38 tip run f06148c6 is report-only (no committed transcript).
Correction (round 39): the C1 row's `closed=8/8` receipt is not independent proof of the run payload: wave-2 mutation testing found G2 accepts forged payload values, and G6's result is scratch-root dependent (`wave2/CritG2Exploit.md`, `wave2/CritC1Kill.md`). The suite and graded selftests have run green under a quiescent isolated environment, but C1 is **unprovable on the frozen counter** absent an independently captured/reproducible payload. Score remains 4; no score gain is claimed. The SKILL.md r39 registry row is now appended (density remains 9).
| Claim | Axis | Before → after | Counting command and measured commit |
|---|---|---|---|
| C1 | depth:verifiability | 4 → 4 (score held; claim harmed/unprovable, no gain) | `bash corpus/instruments/r39-closure.sh --export-ref 3fa81ef5e7b558030903db71c3bb66cb0ea976a2 --work /fast/scratch/hyaku/kasegi-r39/gates-work` → `closed=7/8 exit=1` (G2 red; Y receipt relation not satisfied at J; report-only measurement); `bash corpus/instruments/r39-closure.sh --selftest --export-ref 3fa81ef5e7b558030903db71c3bb66cb0ea976a2 --work /fast/scratch/hyaku/kasegi-r39/gates-work` → `selftest cases=8 failures=1` (G2 positive red; report-only measurement). Measured commit: `3fa81ef5e7b558030903db71c3bb66cb0ea976a2`. Wave-2 G2 payload mutations also pass the instrument, so the frozen C1 pass claim is not admitted. |
| C2 | coverage | 7 → 7 (verified; score held) | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` 21→22; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` 55→59; `grep -rlE '^source: S057' corpus/knowledge | wc -l` 0→1; `python3 corpus/instruments/frontier-recheck-count.py` 24/24→25/25. After-state measured on commit `3fa81ef5e7b558030903db71c3bb66cb0ea976a2`; pre-state is freeze `dcd31701720a6a4929a32471a62011ed87103421` (`.ufo/waves/round-39/c2-controls/before.txt`). |

## BLOCK SCORECARD.md

Correction (round 40): the `## Round 39 result` depth:verifiability row records "`closed=8/8 exit=0` at Y, graded `selftest cases=8 failures=0`", and the round-39 claims row cites the report-only `3fa81ef5e7b558030903db71c3bb66cb0ea976a2` measurement instead of the final receipt; the committed receipt at Y `8371e7ac9f32cae5ed72f8c28205634603f836fa` (`.ufo/waves/round-39/final-gates/all-gates.txt`, all-gates v5, sha256 8d46d7b251fd6736ba1841814274201176d3a7628f9330e8c9b1917013741471) records `closed=7/8 exit=1` (`run-exit=1`; G2 is its single red, `closed=0` on `diff-clean=0,final-lane-commit=0`) and `selftest failures=1` (`selftest cases=8 failures=1`, `selftest-exit=1`, `G2 positive=fail`), so the 8/8 in that row is withdrawn, not merely qualified; the score stays 4 (held).
Correction (round 40): the two limbs a pass would rest on are not independent of the bytes they grade: G2 accepts receipt shape and digest without comparing recorded `G<n> payload=` values to a captured run (mut-f/g/h/j/k pass, `wave2/CritG2Exploit.md` F2), and G6 greens only while `/fast/scratch/hyaku/kasegi-r39/` is quiet although the seat protocol populates that root (`G6 ... r39=present ... closed=0` with seats live; the Y receipt carries `deviation=non-default --lane`) (`wave2/CritC1Kill.md`); the only 8/8 tally is the attempt-1 receipt at `5006097a` (`all-gates v3`, `run-utc=2026-10-26T21:35:00Z`, after its containing commit), which the round discards. Verifier R2's ask, quoted: "Append `Correction (round 40)` lines naming the final receipt values in each record."

## Round 40 result

| Axis | Score before r40 | Score after r40 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4 (held; verified)** | C1 suite `corpus/instruments/r40-closure.sh` H1–H10 landed. At Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5`: `closed=10/10 exit=0`; graded `--selftest cases=10 failures=0` exit 0; base `a7af2ce` export `closed=3/10 exit=1`; r39 judged head `8371e7a` export `closed=2/10 exit=1`; plain run refused exit 2. Receipt `.ufo/waves/round-40/final-gates/all-gates.txt` at Y is the teed transcript (`time-basis=ref-commit`; `run-utc` read from the ref commit, never wall-clock). | r40 |
| coverage | 7 | **8** | Nine queued rows decided (S016/S017/S019/S020/S021/S023/S025 mined; S022/S024 rejected with reason+flip restored in-row); new rows S060 (mined, F23) + S061/S062 (rejected); frontier F23 admitted 22 → 23; harness `entries=26 pass=26 exit=0`; binding `records=54 bound=54 unbound=0`; census exit 0; measure 43/43 = 1.000. | r40 |

Measured at Y: `closed=10/10 exit=0`; `--selftest cases=10 failures=0`; C2 counters per claims.json after-state (queued among nine 0, mined among nine 7, entries citing nine 7, S060+ rows 3, entries citing S060+ 1, frontier 23). Wave-2 falsification verdicts and routed instrument findings (H2/H3/H6/H9/H1/H5 and H6 family/nested/dot/symlink survivor classes; kill-rule escapes) are recorded in `corpus/lessons/round-40.md` §Wave-2 falsification; no frozen-counter change was made.

**Capabilities: no row enters this round** (r40-closure.sh is a closure counter). **Saturation unchanged:** line 9/10, window N=3; lowest non-retired axis depth:verifiability (4) worked and verified.

Correction (round 41): round-40 C1 is not verified on the frozen counter (NOT verified), because the kill rule's "a committed fixture shows a check passing while its defect is present" limb fires on committed fixtures: `wave2/RevC1Counters.defeats.txt` T2 (`closed=7/80` and `failures=10` accepted as green by substring), T4 (a fenced pseudo-table row), T7 (a declared block read outside the export through a symlink), T13 (a mention-only registry row) and T14 (H6 case/separator strays); `wave2/CritKillRule.md`'s eight committed escape states F1–F8 (L1 freeze correction 2: the committed headings are authoritative) with their committed reproducer `wave2/CritKillRule.h6-escapes.sh`; and `wave2/MutH6H10.md` D2 (pristine H8 accepts a leaf-capped green base as its negative control).
Correction (round 41): the `## Round 40 result` depth:verifiability row's "4 (held; verified)" is withdrawn to score 4 held, not verified: the receipt committed at Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5` (`.ufo/waves/round-40/final-gates/all-gates.txt`, sha256 7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b) records `closed=10/10 exit=0` with H1–H10 all `closed=1` over `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd` (`time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`), and a green suite run is not claim admission when the frozen kill rule fires.
Correction (round 41): the row's `graded --selftest cases=10 failures=0` carries no committed transcript: the Y receipt holds no `selftest` line, and the only committed graded tally is over scratch Y′ (`wave2/RevC1Counters.md` R7, report-only), so the quote is withdrawn as evidence (round-40 verifier D2).
Correction (round 41): the round-41 receipt at its Y tees the transcripts of BOTH the suite run and the graded selftest (I2, `time-basis=ref-commit`, `run-utc` equal to the ref's committer instant), so a Y-level selftest tally can no longer be quoted without its transcript.

Correction (round 41): round-40 C1 is not verified on the frozen counter (NOT verified), because the kill rule's "a committed fixture shows a check passing while its defect is present" limb fires on committed fixtures: `wave2/RevC1Counters.defeats.txt` T2 (`closed=7/80` and `failures=10` accepted as green by substring), T4 (a fenced pseudo-table row), T7 (a declared block read outside the export through a symlink), T13 (a mention-only registry row) and T14 (H6 case/separator strays); `wave2/CritKillRule.md`'s eight committed escape states F1–F8 (L1 freeze correction 2: the committed headings are authoritative) with their committed reproducer `wave2/CritKillRule.h6-escapes.sh`; and `wave2/MutH6H10.md` D2 (pristine H8 accepts a leaf-capped green base as its negative control).
Correction (round 41): the `## Round 40 result` depth:verifiability row's "4 (held; verified)" is withdrawn to score 4 held, not verified: the receipt committed at Y `d0fe34d3fa27ff4de745a0c54c203fa8bf7141e5` (`.ufo/waves/round-40/final-gates/all-gates.txt`, sha256 7f55d540d6f41b5112d11bceb9e60e1d217308476b63ecd8c86c34e87ff1c79b) records `closed=10/10 exit=0` with H1–H10 all `closed=1` over `export-ref=c7aea5ef97902f38289cbdc1cf267068876a62dd` (`time-basis=ref-commit`, `run-utc=2026-10-26T22:32:37Z`), and a green suite run is not claim admission when the frozen kill rule fires.
Correction (round 41): the row's `graded --selftest cases=10 failures=0` carries no committed transcript: the Y receipt holds no `selftest` line, and the only committed graded tally is over scratch Y′ (`wave2/RevC1Counters.md` R7, report-only), so the quote is withdrawn as evidence (round-40 verifier D2).
Correction (round 41): the round-41 receipt at its Y tees the transcripts of BOTH the suite run and the graded selftest (I2, `time-basis=ref-commit`, `run-utc` equal to the ref's committer instant), so a Y-level selftest tally can no longer be quoted without its transcript.

## Round 41 result

| Axis | Score before r41 | Score after r41 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4 (held; not verified)** | C1 `corpus/instruments/r41-closure.sh` landed; Y `0f64b8c5b3522d4db2160db087002e3a5f321880` receipt `.ufo/waves/round-41/final-gates/all-gates.txt` (31 lines, sha256 `0915f51d774e5f4bd744912b6b2a87b7387f5437730bef166457766ca10b9e94`) records `closed=10/12 exit=1`, `selftest cases=12 failures=6`. The final-Y run likewise exits 1; I1/I3 committed defeat mutations survive (`wave2/CritC1KillRule.md`, `wave2/RevC1Counters.md`), and I6's live scratch scan is red. Base and r40-head negatives are red (`I10` payload 3/12 each); plain run refuses exit 2. | r41 (not verified) |
| coverage | 8 | **8 (held; not verified)** | F24 / S063 landed: frontier 23→24; registry 62→63; one entry and capture; source-recheck Q1-Q3 pass; frontier harness 27/27; binding 55/55; audit 60/60; census exit 0; measure 44/44. `CritProvinceBoundary` in the falsify results identifies substantial shared RFC 9116 ground with kake's existing security.txt entry; no coverage score increase is claimed pending the scope ruling in L0. | r41 (scope unresolved) |
| depth:density | 9 | 9 | Non-target guard: `corpus/instruments/density.py` byte-identical to base; no density move claimed. | r15 (held r41) |

Measured before: claims-freeze commit `fbba3d96cdf8d37c1ea41304a1ba35691329684b`; C1 do-nothing control has no suite (plain run exit 127, `c1-controls/do-nothing.txt`); C2 control has F24 absent, frontier 23, registry 62, knowledge 59, harness 26/26, binding 54/54 and audit expected 59 (`c2-controls/before.txt`).

Measured at Y `0f64b8c5b3522d4db2160db087002e3a5f321880`: `bash corpus/instruments/r41-closure.sh --export-ref 0f64b8c5b3522d4db2160db087002e3a5f321880` → `closed=10/12 exit=1`; `bash corpus/instruments/r41-closure.sh --selftest --export-ref 0f64b8c5b3522d4db2160db087002e3a5f321880` → `selftest cases=12 failures=6` exit 1. The receipt is the J run transcript, `time-basis=ref-commit`, `run-utc=2026-10-27T12:16:34Z`; the Y replay still fails I2/I6, while I1/I3 selftest defeats are committed false acceptances. C2 at Y: frontier 24/24 admitted; registry 63 with S063 mined; entries citing S063 1; knowledge files 60; harness 27/27 incl `PASS F24 ids=S063`; binding 55/55; audit 60/60; census exit 0 with only standing W04 S028/S029 warnings; measure 44/44 = 1.000. These measurements do not establish disjoint coverage from kake.

**Capabilities:** no new capability row enters this round (`r41-closure.sh` is a closure counter).

**Saturation unchanged:** line 9/10 per owned axis, window N=3; the lowest non-retired axis remains depth:verifiability (4). C1 worked that axis but did not verify; no score increase is claimed.

**Planned for round 42** (not a claim): build a fresh frozen C1 predicate only after repairing I1's per-correction evidence requirement and I3's token-boundary test; include a green I2/Y receipt and clean scratch baseline before dispatch. Revisit F24 only after the L0 scope ruling on shared RFC 9116 ground with kake.

Correction (round 42): the round-41 standings carry forward unchanged and are not upgraded by this round's drafting: `## Round 41 result` records depth:verifiability `4 (held; not verified)` at Y `0f64b8c5b3522d4db2160db087002e3a5f321880` (`closed=10/12 exit=1`, `selftest cases=12 failures=6`, I1/I3 committed defeats alive, I6 live scratch scan red) and coverage `8 (held; not verified)` (F24/S063 landed; substantial shared RFC 9116 ground with kake; no increase claimed pending the L0 scope ruling). Round 42 opens a NEW frozen counter (C1 `corpus/instruments/r42-closure.sh`, J1-J13 with replay limbs) and a NEW frontier lead (C2 F25); neither replaces, re-scores, or re-verifies the round-41 rows, whose "not verified" cells stand as written.

Correction (round 42): D-r41-1 (self-defect, `SCORECARD.md`) is carried append-only and named once here: the four `Correction (round 41)` lines were appended verbatim twice, and both occurrences are kept as history — no rewrite, no deletion, no reordering. The single occurrence intended by the r41 close is the first; the second is the stray. Round 42's J11 (family F-CORR, no `Correction (round <n>)` block duplicated verbatim) is the check asked to detect this exact committed state; its measurement is the J11 line recorded at Y and no repair of the duplicate is claimed here.

Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1` (`.ufo/waves/round-42/final-gates/all-gates.txt`, instrument `corpus/instruments/r42-closure.sh`), i.e. the committed r41 duplication is detected and excused by this marker, never silently passed.

Correction-dedup (round 42): duplicated Correction (round 41) blocks at SCORECARD.md lines 1602-1605 and 1607-1610 — the second occurrence is the stray; both kept as history.

## Round 42 result

| Axis | Score before r42 | Score after r42 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4 (held; verified at Y — `closed=13/13 exit=0`, `selftest cases=13 failures=0`)** | New frozen counter `corpus/instruments/r42-closure.sh` (landed at J; its four instrument defects repaired under the frozen predicate, erratum 4): export mode only (plain run exit 2; unresolvable `--export-ref` prints its distinct ref-not-found red `ERROR ref-not-found … closed=0 exit=1`), one `J<n> payload=... closed=0\|1` line per check J1-J13, `closed=13/13 exit=0` at Y; graded `--selftest --export-ref Y` thirteen `selftest case=J<n> ... positive=pass ... verdict=pass` lines and `selftest cases=13 failures=0`; base `5053a7f46de35784cff4b56756906e9014a38276` and round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` exports print `closed=5/13 exit=1` and `closed=4/13 exit=1`. J1-J7 close the seven routed families F-EVID / F-TOKEN / F-TABLE / F-DECL / F-SCAN / F-BIND / F-FLIP, each with a replay limb re-executing its committed defeat artifact against the current suite bytes (`replay=…=rejected` on every J1–J7 line); J8 receipt integrity, J9 negative controls, J10 graded-selftest isolation, J11 correction uniqueness (the state named in the dedup line above), J12 no tracked corpus deletions + `density.py` byte-identical, J13 quiescence inside the suite's own scratch root. Receipt at Y `.ufo/waves/round-42/final-gates/all-gates.txt` (teed run + selftest transcript). | r42 (measured at Y) |
| coverage | 8 | **8 (held; verified at Y)** | F25 admitted 24 → 25 with a `corpus/README.md` frontier row and a `PROVINCE.md` amendment; the topic is the CVE Record Format, chosen by the wave-1 scout lead screen against the OSV schema and the NVD API 2.0 schema (both rejected, over machine-readable vulnerability-data standards the lane holds neither), with the two screens rejected (status `rejected`, reason + flip, URL + access date + ≤25-word located quote) recorded in the round-42 lesson Gate block, closing D-r41-2. Registry 63 → 66 (erratum 1: S064 mined + S065/S066 rejected): S064 status `mined`, opened this round, capture `corpus/source-snapshots/round-42/S064.txt` + `manifest.json`, source-recheck pass and capture-binding bound; knowledge 60 → 61 with one entry carrying the provenance trio (`source: S064`, `verified-at:`, executable `recheck:` line) present and passing; harness `entries=28 pass=28 exit=0` including `PASS F25`; binding `records=56 bound=56 unbound=0`; recheck-audit `expected=61 missing=0 unexpected=0 exit=0`; sources census exit 0 with only the standing W04 S028/S029 warnings; measure 45/45 = 1.000; junk twin rejected. F24 / RFC 9116 stays parked (open L0 scope question; not re-mined, not referenced as a candidate). | r42 (measured at Y) |
| depth:density | 9 | 9 | Non-target guard only: J12 requires `corpus/instruments/density.py` byte-identical to base `5053a7f46de35784cff4b56756906e9014a38276` at J and Y; no density move claimed or made. | r15 (held r42) |

Measured before (frozen controls, read at base `5053a7f46de35784cff4b56756906e9014a38276`): `.ufo/waves/round-42/c1-controls/do-nothing.txt` records the r42 suite absent (plain run exit 127, cannot print `closed=13/13`) and the r41 suite at base printing `selftest cases=12 failures=8` / `closed=8/12 exit=1` with the I1 evidence-not-named and I3 mangled-token defeats alive; `.ufo/waves/round-42/c2-controls/before.txt` records frontier rows 24, F25 rows 0, registry 63, S064+ rows 0, knowledge 60, entries citing S064+ 0, harness `entries=27 pass=27 exit=0`, binding `records=55 bound=55 unbound=0`, audit `expected=60 missing=0 unexpected=0 exit=0`. Do-nothing reaches none of the after-state values above.

Measured at Y (the receipt's own commit; lane files never name it): the five counting commands of `.ufo/waves/round-42/claims.json` C1 — plain run (refused exit 2), `--export-ref <Y>` (`closed=13/13 exit=0`), `--selftest --export-ref <Y>` (`selftest cases=13 failures=0`), `--export-ref 5053a7f46de35784cff4b56756906e9014a38276` (`closed=5/13 exit=1`), `--export-ref 1f7464612ac4c44e39886b82e812610d3c039b13` (`closed=4/13 exit=1`) — and the nine C2 counters of the same file (frontier 25, registry 66, S064 mined, entries citing S064 1, knowledge 61, harness `entries=28 pass=28` incl `PASS F25`, binding `records=56 bound=56`, audit `expected=61`, census exit 0). Judged head J is the lane commit carrying every round-42 change except the receipt; Y adds only `.ufo/waves/round-42/final-gates/all-gates.txt`, and lane files never name J by hash.

**Capabilities: no row enters this round** (`r42-closure.sh` is a closure counter; C2 adds a coverage row, not a capability). **Saturation unchanged:** line 9/10 per owned axis, window N=3; the lowest non-retired axis remains depth:verifiability (4), worked this round with its measurement recorded at Y; no score increase is claimed.

**Planned for round 43** (not a claim): (1) depth:verifiability — put the r42 predicate to the verifier's spot-check, carry any new routed attack findings (in-family escapes named by the kill rule, out-of-family findings routed as defects) into r43 fixtures, and keep every J1-J7 replay limb live; the 4 → 5 gap stays gated per the distance-to-next-score section. (2) coverage — decide the remaining screened candidates from the F25 lead screen (including the reject's sibling documents and any queued rows), keep F24 parked until the L0 ruling, and hold the measure at 1.000; the D-r41-2 reject direction is exercised this round (OSV schema and NVD API 2.0 schema screened and rejected).

### Round-42 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 42 | depth:verifiability | 4 (r41 row: held, not verified — r41 suite `closed=10/12 exit=1`, `selftest cases=12 failures=6`, I1/I3 defeats alive, I6 scratch scan red; routed families F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP open) | 4 held — **expected** (`closed=13/13 exit=0` at Y, `selftest cases=13 failures=0`, base `5053a7f` and r41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` each `closed<13/13 exit=1`, plain run exit 2, ref-not-found red distinct, J1-J7 replay limbs rejecting their committed defeats, J11 detecting the duplicated r41 correction state) — **measured at Y** | `corpus/instruments/r42-closure.sh`; `.ufo/waves/round-42/final-gates/all-gates.txt`; `corpus/lessons/round-41-verifier-spotcheck.md` §5 |
| 42 | coverage | 8 (r41 row: held, not verified — frontier 24, registry 63, knowledge 60, harness 27/27, binding 55/55, audit expected=60; F24 scope unresolved) | 8 held — **expected** (F25 24→25 admitted with README row + PROVINCE amendment; registry 64 with S064 `mined` + ≥1 screened reject recorded in the lesson Gate block; knowledge 61 with the provenance trio; harness 28/28 incl `PASS F25`; binding 56/56; audit expected=61; census exit 0; measure 45/45 = 1.000; junk twin rejected) — **measured at Y** | `corpus/README.md` F25 row; `PROVINCE.md` F25 amendment; `corpus/SOURCES.md` S064 row; `corpus/source-snapshots/round-42/{S064.txt,manifest.json}`; `corpus/knowledge/<slug>.md`; `corpus/lessons/round-42-*.md` Gate block |

Correction (round 43): the `corrections=33` literal on SCORECARD.md:1634 — the round-42 correction line that says "the r42 suite at Y prints" the r42 J11 payload — is superseded and stale by one: the live ledger over SCORECARD.md + LOG.md + SHONEN.md is 34 `Correction (round <n>)` lines in four duplicated body groups (all four excused by the round-42 dedup marker) at `ab98fac9dce87130bc4f66de89e30650d63943dc`, re-derived by the round-43 suite's K14 (`bash corpus/instruments/r43-closure.sh --export-ref <ref>`, the limb that reuses the r42 engine's J11 ledger) and by that instrument's own J11 line at the same ref (`.ufo/waves/round-42/final-gates/all-gates.txt:16`); K14 re-derives the count from every export it grades — 34 at that base plus one per `Correction (round 43)` line landed in those three files, 37 once this round's two SCORECARD lines and one LOG line land — so the value is never frozen again in this file. RD42-1.

## Round 43 result

| Axis | Score before r43 | Score after r43 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | **4 (held; not verified by this append — the round-43 kill rule is not re-derived here)** | C1 `corpus/instruments/r43-closure.sh`, export mode only (a plain run refuses exit 2; an unresolvable `--export-ref` prints its distinct `ref-not-found` red). K1-K13 carry the r42 J1-J13 payload grammar and replay limbs unchanged; K14-K19 grade the six routed narrative-evidence defect classes (correction literal, wave-dispatch narrative vs results files, the placeholder promise, the `claims.json` before literal vs its own control, quoted `closed=` values vs committed transcripts, freeze-record ordering). Predicate at Y: one `K<n> payload=... closed=0\|1` line per check K1-K19 and `closed=19/19 exit=0`, exit 0 only at 19/19; `--selftest --export-ref Y` prints nineteen graded `selftest case=K<n> ... positive=pass ... verdict=pass` lines and `selftest cases=19 failures=0`. Negative controls: base `ab98fac9dce87130bc4f66de89e30650d63943dc` `closed=13/19 exit=1` with exactly K14-K19 open; round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` `closed<19/19 exit=1`. Receipt `.ufo/waves/round-43/final-gates/all-gates.txt` is the one unedited tee of the run and the graded selftest at Y. | r43 |
| coverage | 8 | **8 (held; no score increase claimed)** | C2 `corpus/instruments/claim-package-check.py` gates the six-file claim-package contract with eight rules (R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS, R-REPORT, R-NOSECRET), one `RULE <id> verdict=pass\|fail` line each and `package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED\|DEFECT exit=0\|1`; the committed exemplar `corpus/instruments/fixtures/claim-package/exemplar` is `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`, nine committed defect fixtures each `verdict=DEFECT exit=1` on their own rule, and `--selftest` is green on its ten cases (nine defect classes plus the degenerate always-pass control, rejected). The exemplar is built from one public disclosed report captured this round as a new `mined` registry row, documented by `corpus/knowledge/claim-package-gate.md`; `claimable` stays false and the operator gates are named in `claim_checklist.md`. Coverage counters: registry 66 → ≥68 (S067 `mined` + one reject row); entries citing S067 0 → 1; knowledge 61 → 62; capture-binding `records=57 bound=57 unbound=0`; recheck-audit `expected=62`; frontier harness `entries=28 pass=28 exit=0` (no frontier row change, frontier 25 held); census exit 0. The capability row enters on the demo, confirmed in-round: the command prints `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` on the committed exemplar and `selftest cases=10 failures=0`. | r43 |
| depth:density | 9 | 9 | Non-target guard only: `corpus/instruments/density.py` byte-identical to base `ab98fac9dce87130bc4f66de89e30650d63943dc` (blob sha256 `ee803726a3229eb924a6798fe0cf5309dacd33d42c40568da55d5c95f9f54710`, re-derived by `git cat-file blob ab98fac9dce87130bc4f66de89e30650d63943dc:corpus/instruments/density.py \| sha256sum`); no density move claimed or made. | r15 (held r43) |

Measured before (frozen controls, read at base `ab98fac9dce87130bc4f66de89e30650d63943dc`): `.ufo/waves/round-43/c1-controls/do-nothing.txt` records the r43 suite absent at base and the r42 suite — the do-nothing stand-in — over the base export printing `closed=12/13 exit=1` (J8 red only because the base carries commits after the r42 receipt), with all six routed narrative/hygiene defect classes present in committed bytes and no check among the thirteen grading any of them; `.ufo/waves/round-43/c2-controls/before.txt` records registry 66 with S067 onward 0, knowledge 61 with entries citing S067 0, capture-binding `records=56 bound=56 unbound=0`, recheck-audit `expected=61`, frontier harness `entries=28 pass=28 exit=0`, and census exit 0. Do-nothing reaches none of the after-state values above.

## Round-43 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| claim-package-gate | Gate a six-file claim package in one pass against eight contract rules (R-FILES, R-MANIFEST, R-REDACT, R-CUSTODIAN, R-PROVENANCE, R-STATUS, R-REPORT, R-NOSECRET), printing one `RULE <id> verdict=pass\|fail` line per rule plus `package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED\|DEFECT exit=0\|1`, rejecting nine committed defect fixtures by their named rule and proving it with a ten-case `--selftest`. | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar` -> `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` (confirmed in-round; `--selftest` prints `selftest cases=10 failures=0`). | 43 |

**Saturation unchanged:** line 9/10 per owned axis, window N=3; the lowest non-retired axis remains depth:verifiability (4), worked this round with its measurement in the Y receipt; no score increase is claimed. If the demo is confirmed, the `claim-package-gate` entry restarts the capability window (previous entry round 33).

### Round-43 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 43 | depth:verifiability | 4 (r42 row: held, `closed=13/13 exit=0` at Y under the r42 predicate; six routed narrative/hygiene defect classes RD42-1/-2/-3/-4/-5/-6/-8 present in committed bytes and ungraded by J1-J13) | 4 held — **expected** (`closed=19/19 exit=0` at Y; `selftest cases=19 failures=0`; base `ab98fac9` `closed=13/19 exit=1` with exactly K14-K19 open; round-41 head `1f7464612ac4c44e39886b82e812610d3c039b13` red; plain run exit 2; ref-not-found red distinct; every K1-K13 replay limb still rejects its committed defeat; each K14-K19 mutant rejects) — **the Y measurement is the receipt's, not this append's** | `corpus/instruments/r43-closure.sh`; `.ufo/waves/round-43/final-gates/all-gates.txt`; `.ufo/waves/round-43/claims.json` C1 |
| 43 | coverage | 8 (r42 row: held — frontier 25, registry 66, knowledge 61, harness 28/28, binding 56/56, audit expected=61; claim-package gate absent) | 8 held — **expected** (gate `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0` on the exemplar and `verdict=DEFECT exit=1` on nine defect fixtures; selftest green on ten cases; registry ≥68 with S067 `mined` + one reject; knowledge 62 with the S067 entry; binding 57/57; audit expected=62; harness 28/28; census exit 0) — **the Y measurement is the receipt's, not this append's** | `corpus/instruments/claim-package-check.py`; `corpus/instruments/fixtures/claim-package/`; `corpus/knowledge/claim-package-gate.md`; `corpus/SOURCES.md` S067 row; `corpus/source-snapshots/round-43/manifest.json` |
| 43 | depth:density | 9 (no density move queued) | 9 held (non-target guard: `density.py` byte-identical to base, blob sha256 `ee803726a322…`) | `git cat-file blob ab98fac9dce87130bc4f66de89e30650d63943dc:corpus/instruments/density.py \| sha256sum` |

Correction (round 43): this line closes D-r41-1's duplicate-correction state and supersedes the RD42-1 cell without rewriting either: the duplicated `Correction (round 41)` block pair at `SCORECARD.md:1602-1605` and `SCORECARD.md:1607-1610` remains byte-identical history — no deletion, no reorder, no rewrite — and from round 43 that state is graded, not only marker-excused: `corpus/instruments/r43-closure.sh` K14 re-counts `Correction (round <n>)` lines and distinct bodies across `SCORECARD.md`, `LOG.md` and `SHONEN.md` on the K11 ledger semantics and prints `live=corrections=` and `groups=` in its own payload, while the stale `corrections=` cell at `SCORECARD.md:1634` is named as superseded by the round-43 correction block landed for RD42-1, so the cell is superseded, never rewritten. The live count is the K14 line's `live=corrections=` field at the round-43 verification ref, not a literal restated here.

Correction (round 43; appended round 44): the C1 move-log row's base-export literal `closed=13/19 exit=1` is superseded. No committed run of the landed `r43-closure.sh` exists at base `ab98fac9dce87130bc4f66de89e30650d63943dc`; the 13/19 figure came from draft/stub evidence and is not a measured result. The committed control records the r42 stand-in at `closed=12/13 exit=1`, while the r43 suite itself is absent at that base. See `.ufo/waves/round-43/claims-erratum-6.md` and the round-44 control receipt.

## Round-44 capability disposition

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 44 | depth:verifiability | 4 (round-43 score) | 4 held; C1 unverified, no delta | `.ufo/waves/round-44/controls/r44-counter-trial-disposition.txt`; `wave1/R44Critic1.md`, `R44Critic2.md` |
| 44 | coverage | 8 (round-43 score) | 8 held; C2 unverified, no delta | `.ufo/waves/round-44/controls/c2-frozen-counter-replay.txt`; `wave1/R44Critic11.md`; no independent nonauthor spot-check |
| 44 | depth:density | 9 (round-43 score) | 9 held; no target or measurement | `.ufo/waves/round-44/controls/do-nothing.txt` |

The frozen C2 counter `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` prints 0 at both the frozen base and the after tree; it cannot certify F26. The *different* table-aware diagnostic in `controls/c2-counter-audit.txt` returns 25→26, with registry rows 68→70 and knowledge files 62→63. These are structural observations, not a C2 verdict. C1's draft counter is rejected for accepting a marker-only false-green; it was removed from production paths. Round-44 score changes: none. Saturation: unchanged; the lowest non-retired axis remains depth:verifiability at 4.

### Planned evidence gates for round 45

- `depth:verifiability`: freeze a counter over committed artifacts and require red on both the do-nothing export and marker-only mutants before scoring; a correction paragraph alone cannot satisfy a defect.
- `coverage`: freeze a table-correct counter and committed-export basis, then obtain a nonauthor admit/reject spot-check before claiming coverage movement.

### Round-44 move-log rows (attempt 2 — L1 `KasegiR44a2`)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 44 | depth:verifiability | 4 (round-43 score) | 4 held — **measured** (the eight routed round-43 defects read `fixed=0 unresolved=8` at the frozen base and `fixed=8 unresolved=0` at the round-44 tree; the counter's own selftest rejects eleven marker-only mutants, `selftest cases=11 failures=0`). **Score delta: 0** — the axis number stays where the saturation window holds it; the increment is graded under the quality trend, not as a score move | `corpus/instruments/r44-routed-defects.py`; measured commit `8063547d0ce647d6f9eafc3c8d0a502616685218`; `.ufo/waves/round-44/controls/c1-counter-baseline.txt`, `.ufo/waves/round-44/controls/c1-counter-at-commit-A.txt` |
| 44 | coverage | 8 (round-43 score) | 8 held — **measured** (admitted frontier rows 25 → 26; SOURCES registry rows 68 → 70 with S069 `mined` and S070 `rejected`; knowledge entries 62 → 63; source census exit 0). **Score delta: 0** — same saturation reading | `corpus/instruments/r44-frontier-count.py`; measured commit `8063547d0ce647d6f9eafc3c8d0a502616685218`; `.ufo/waves/round-44/controls/c2-frontier-counter.txt`; `corpus/SOURCES.md` S069/S070; `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`; `.ufo/waves/round-44/nonauthor-spotcheck-packet.md` |
| 44 | depth:density | 9 (round-43 score) | 9 held (non-target guard: `density.py` byte-identical to the round-43 base) | `corpus/instruments/density.py` |

Counting commands, one per claim, both re-runnable against an exported tree:

- **C1** — `python3 corpus/instruments/r44-routed-defects.py --root <tree> --baseline <base-export>` → `routed-defects total=8 fixed=<k> unresolved=<n> exit=0|1`; before (frozen base `5ab3a60`) `fixed=0 unresolved=8 exit=1`, after (commit `8063547`) `fixed=8 unresolved=0 exit=0`; selftest `python3 corpus/instruments/r44-routed-defects.py --root <tree> --selftest --work <dir>` → `selftest cases=11 failures=0`.
- **C2** — `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 26` → `frontier rows=<n> admitted=<k>`; before (frozen base `5ab3a60`) `frontier rows=25 admitted=25`, exit 1 (a do-nothing control cannot reach 26); after (commit `8063547`) `frontier rows=26 admitted=26`, exit 0.

Correction (round 44; attempt 2): the attempt-1 disposition above — "C1 unverified, C2 unverified, no score delta" — is superseded by the two measurements above. C1 now has a committed, fail-closed counter and eight append-only repairs; C2's frontier, registry and knowledge movements are measured. The frozen C2 counter string itself is defective and is NOT rewritten: `grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md` reads `0` at the frozen base and `0` at the round-44 tree, because the frontier table's status is its third cell. The declared predicate (admitted frontier rows) and the declared target (26) are unchanged; the table-aware counter measures that same predicate, and the frozen string stays recorded verbatim in `.ufo/waves/round-44/claims.json` and in the round report. The round's non-author admit/reject spot-check is prepared (`.ufo/waves/round-44/nonauthor-spotcheck-packet.md`) and is adjudicated by the closure, not by the lane.

### Round-44 final measurement (post wave-2 integration, attempt 2)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 44 | depth:verifiability | 4 (round-43 score) | 4 held — **measured at the wave-2 integration tree** (the eight routed round-43 defects read `routed-defects total=8 fixed=0 unresolved=8 exit=1` at the frozen base export and `routed-defects total=8 fixed=8 unresolved=0 exit=0` at commit `4aba89c997868e70546ecacbb837ce5bbca811fc`; the hardened counter's selftest grades twenty cases — nineteen mutants plus one positive — `selftest cases=20 failures=0`, and every mutant that fabricates or rewrites a bound artifact is rejected). **Score delta: 0** — the saturation window keeps the axis number; the increment is graded under the quality trend | `corpus/instruments/r44-routed-defects.py` (v2, digest-pinned); `.ufo/waves/round-44/controls/c1-counter-baseline.txt`, `c1-counter-at-commit-B.txt`, `c1-counter-selftest-v2.txt` |
| 44 | coverage | 8 (round-43 score) | 8 held — **measured** (admitted frontier rows 25 → 26 under the duplicate-id-guarded counter; SOURCES registry rows 68 → 70 with S069 `mined` and S070 `rejected`; knowledge entries 62 → 63; source census exit 0; source recheck Q1-Q5 pass; capture binding 58/58; recheck audit 63/63; frontier harness 29/29). **Score delta: 0** — same saturation reading | `corpus/instruments/r44-frontier-count.py`; `.ufo/waves/round-44/controls/c2-frontier-counter-v2.txt`, `noharm-gates-attempt2.txt`; `corpus/SOURCES.md` S069/S070; `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`; `.ufo/waves/round-44/nonauthor-spotcheck-packet.md` |
| 44 | depth:density | 9 (round-43 score) | 9 held (non-target guard: `density.py` byte-identical to the round-43 base) | `corpus/instruments/density.py` |

Counting commands, one per claim, both re-runnable against an exported tree:

- **C1** — `python3 corpus/instruments/r44-routed-defects.py --root <tree> --baseline <base-export>` → `routed-defects total=8 fixed=<k> unresolved=<n> exit=0|1`; before (frozen base `5ab3a60`) `fixed=0 unresolved=8 exit=1`, after (commit `4aba89c`) `fixed=8 unresolved=0 exit=0`; selftest `python3 corpus/instruments/r44-routed-defects.py --root <tree> --selftest --work <dir>` → `selftest cases=20 failures=0`.
- **C2** — `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 26` → `frontier rows=<n> admitted=<k>`; before (frozen base `5ab3a60`) `frontier rows=25 admitted=25`, exit 1 (a do-nothing control cannot reach 26); after `frontier rows=26 admitted=26`, exit 0.

Correction (round 44; falsify wave): the wave-2 seats falsified the first landing's counter and evidence. A fully fabricated evidence tree graded `fixed=8 unresolved=0` (`wave2/R44W2Exec05.md`); presence-only predicates accepted denials, stub emitters, fabricated seat names, filename mentions and a token-only receipt (`wave2/R44W2Rev09.md`); the K17-escape mechanism claim was wrong in substance — the `closed=13/19` token is an AFTER-cell token K17 never grades (`wave2/R44W2Rev02.md`, `wave2/R44W2Revenger01.md`); and the round-44 export-ref sidecar contradicted the paired run receipt. The corrections are the v2 counter (sha256-pinned artifacts, affirmative tokens, ordering checks, refusal logic, names equality), the corrected sidecar, the superseded-registry note and the corrected lesson mechanism statement (`corpus/lessons/round-44.md`, M44-9/M44-10). The frozen claims file and the frozen counter string stay byte-identical.

Correction (round 44; prose numeral): the earlier prose "eleven marker-only mutants" was imprecise — the v1 battery was ten mutants plus one positive (eleven graded cases); the v2 battery is nineteen mutants plus one positive (twenty graded cases).


## Round 45 result

Frozen at `.ufo/waves/round-45/claims.json` (freeze commit `8cf62c879e6e6b031e67412f8fac1fba0bd378cf`, base `dc5bb8c6e31efc4a6650819df85e79b72fd64bcd`). Counter errata and the before-value erratum: `.ufo/waves/round-45/counter-errata.md`. Receipts: `.ufo/waves/round-45/controls/final-measure.txt` (measured at lane commit `3106889`).

| Axis | Score before r45 | Score after r45 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 held — measured, no promotion limb moved | C1 `python3 corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base>`: base `routed-defects total=5 fixed=0 unresolved=5 exit=1`, tip `fixed=5 unresolved=0 exit=0` (`controls/final-measure.txt`) | r45 (held) |
| coverage | 8 | 8 held — measured (+1 admitted frontier row; not a coverage-ratio move) | C2 `python3 corpus/instruments/r45-c2-gate.py --root <tree>`: base `fixed=1/7 exit=1`, tip `fixed=7/7 exit=0`; `r44-frontier-count.py --expect 27`: base 26 (exit 1), tip 27 (exit 0) | r45 (held) |
| depth:density | 9 | 9 held — non-target guard: `density.py` byte-identical; SKILL.md mean 237.4 → 248.4 from an appended registry block, not credited as depth | `controls/final-measure.txt` | r45 (held) |

### Round-45 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 45 | depth:verifiability | 0 of 5 routed defects resolved (base) | 5 of 5 at `3106889` by counter v1.2; the counter was falsified twice (wave 1: v1; wave 2: v1.1) and hardened each time; selftests `cases=85 failures=0` and `cases=115 failures=0` | `corpus/instruments/r45-routed-defects.py`; `.ufo/waves/round-45/counter-errata.md`; `controls/final-measure.txt` |
| 45 | coverage | 26 admitted frontier rows, 70 SOURCES rows, 63 knowledge entries | 27, 72, 64; S071 `mined` (tier A), S072 `rejected` (supersedes S070) | `corpus/README.md` Round-45 admission block; `corpus/knowledge/linux-kernel-security-bugs-reporting-process.md`; `corpus/SOURCES.md` S071/S072; `corpus/source-snapshots/round-45/manifest.json` |

Counting commands, one per claim (re-runnable on an export):

- **C1** — `python3 corpus/instruments/r45-routed-defects.py --root <tree> --baseline <base-export>` → `routed-defects total=5 fixed=<k> unresolved=<n> exit=0|1`; base `fixed=0`, tip `fixed=5`.
- **C2** — `python3 corpus/instruments/r45-c2-gate.py --root <tree>` → `c2-gate fixed=<k>/7 exit=0|1`; base `fixed=1/7`, tip `fixed=7/7`; secondary `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 27`.

The honest reading of the green counters: they are pinned-artifact graders (a tree must carry the genuine bytes); they do not certify that the entry adds analysis beyond restating S071 — that judgment is the non-author closure's, and the wave-2 coverage reviewer found the topic new to the corpus (`wave2/R45W2RevNovelty.md`).

### Round-45 capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| Frozen-counter base replay (`freeze-check.py`) | Replays every frozen counter command at the base export, requires its declared before-line as a whole line and fails when the after-line is already present or the counter mutates the base | `python3 corpus/instruments/freeze-check.py --claims .ufo/waves/round-45/claims.json --tool-root <tree> --base <base-export>` → `freeze-check claims=2 base_ok=2 exit=0`; selftest `cases=27 failures=0` (`controls/final-measure.txt`) | 45 |

### Planned evidence gates for round 46

- `depth:verifiability`: state each claim's before-value per start tree (base and freeze tree) and run `capture-binding-check.py --root` and the census before dispatching a wave.
- `coverage`: obtain a non-author admit/reject spot-check of S071/S072 before any coverage statement beyond +1 row; keep rejected-row captures outside `corpus/source-snapshots/`.

## Round 46 result

Frozen at `.ufo/waves/round-46/claims.json` (freeze commit `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`, base `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`). Counter errata and the classification decision: `.ufo/waves/round-46/counter-errata.md`. Receipts: `.ufo/waves/round-46/controls/final-measure.txt` (measured at lane commit `eb874bc86ad7a6cfec299088e5a2d7ec68cf61b7`), `controls/controls-v1.2.out.txt` (17 controls; 11 red-before), `controls/selftest-vs-frozen-v1.txt`.

| Axis | Score before r46 | Score after r46 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 held — measured (gated rechecks 24 → 22), no promotion limb completed | C1 `python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base>`: base `c1-gate fixed=1/7 exit=1`, tip `fixed=7/7 exit=0`; plain `python3 corpus/instruments/recheck-audit.py --root . --quiet \| grep '^executes='` on the tip prints `gated=22` (base `gated=24`) | r46 (held) |
| coverage | 8 | 8 held — measured (+1 admitted frontier row; not a coverage-ratio move) | C2 `python3 corpus/instruments/r46-c2-gate.py --root <tree>`: base `fixed=1/7 exit=1` (`2/7` at the freeze tree), tip `fixed=7/7 exit=0`; plain frontier rows 27 → 28, SOURCES rows 72 → 73, knowledge files 64 → 65 | r46 (held) |
| depth:density | 9 | 9 held — non-target guard: `density.py` byte-identical; SKILL.md mean 249.1 → 258.7 from the appended registry block, not credited as depth | `controls/final-measure.txt` | r46 (held) |

### Round-46 held-axis promotion limbs (the next claim each held score targets)

- **depth:verifiability 4 → 5** (`## Distance-to-next-score`, `SCORECARD.md:1536`). Limb 1: zero gated rechecks — the base reads `gated=24 of 64`, the tip `gated=22 of 65`: 22 to go. Limb 2: the score-5 audit bar (`SCORECARD.md:331`, "a non-author audit passing 25/25 source chains and 0 unsupported current claims") — untouched, only a non-author closure can grade it. The next claim targets limb 1: the census `wave1/R46ScoutCensus1-8.md` classifies each remaining gated entry as fully, partly or not re-groundable on committed bytes; the DATA-half entries cannot be re-grounded (`wave1/R46Revenger.md`) and need an operator ruling to leave the denominator (L0 kasegi round-15).
- **coverage 8**: the only written promotion heading is `### coverage, 7 → 8` (`SCORECARD.md:1547`); it reads `(20 + F_admitted)/(20 + F_total) = 1.000` at the tip (frontier rows 28, admitted 28, queued registry rows 0). No 8 → 9 criterion exists; none is invented here. Coverage stays held with no promotion limb; the next frontier move is an expansion count, and the operator half (0/18 domain surfaces present) is unchanged.

### Round-46 move-log rows

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 46 | depth:verifiability | 24 of 64 `recheck:` lines gated (`recheck-audit.py` `executes=40 gated=24 broken=0`; `r46-c1-gate.py` `fixed=1/7`) | 22 of 65 at `eb874bc` (`executes=43 gated=22 broken=0`; `fixed=7/7`); the counter read 7/7 on eleven defect trees at v1 and was hardened twice (errata E1, E2); C1's faithfulness rests on a side-by-side reading of 46 rows, which the counter cannot make | `corpus/instruments/r46-c1-gate.py`; `corpus/knowledge/claim-package-contract.md`, `claim-gates.md` (`## Re-ground (round 46)`); `controls/final-measure.txt`; `wave2/R46W2RevGround*.md` |
| 46 | coverage | 27 admitted frontier rows, 72 SOURCES rows, 64 knowledge entries | 28, 73, 65; S073 `mined` (tier A, docs) | `corpus/README.md` Round-46 admission block; `corpus/knowledge/github-private-vulnerability-reporting.md`; `corpus/SOURCES.md` S073; `corpus/source-snapshots/round-46/manifest.json` |

Counting commands, one per claim (re-runnable on an export):

- **C1** — `python3 corpus/instruments/r46-c1-gate.py --root <tree> --baseline <base-export>` → `c1-gate fixed=<k>/7 exit=<c>`; base `fixed=1/7` (the freeze tree reads the same), tip `fixed=7/7`; plain: `bash corpus/instruments/r46-plain-measure.sh <tree>` prints `c1a=23`/`c1b=24` at the base and `c1a=21`/`c1b=22` at the tip; `bash .ufo/waves/round-46/controls/plain-rows.sh <tree> <entry>.md` prints `rows=25 located=25` and `rows=21 located=21`.
- **C2** — `python3 corpus/instruments/r46-c2-gate.py --root <tree>` → `c2-gate fixed=<k>/7 exit=<c>`; base `fixed=1/7`, freeze tree `fixed=2/7`, tip `fixed=7/7`; secondary `python3 corpus/instruments/r44-frontier-count.py --root <tree> --expect 28` (base `verdict=SHORT` exit 1, tip exit 0); plain `c2a=27 → 28`, `c2b=72 → 73`, `c2c=64 → 65`, `c2d=0 → 3`.

The honest reading of the green counters: they are mechanical graders. C1's rows are checked for location, load-bearing and append-only, never for meaning; `controls-v1.2.out.txt` prints `c1 hollow-rows` GREEN as the disclosed limit. The side-by-side row review (`wave2/R46W2RevGround*.md`) found three BROKEN verdicts over 46 rows (overreach and circular witnesses), all reworded in the wave-2 integration; a non-author must re-read the rows before C1 is called verified.

**Capabilities: no row enters this round** (the gates and selftests are counters; `r46-landing-gate.py` has been run on fixtures and replayed on three real report pairs, not yet as the filing gate of a landed round). **Saturation unchanged:** line 9/10 per owned axis, window N = 3; the lowest non-retired axis stays depth:verifiability (4), which C1 worked.

### Planned evidence gates for round 47

- `depth:verifiability`: state each claim's before-value per start tree and run `capture-binding-check.py --root` and the census BEFORE dispatching a wave (round 46 read `bound=59 unbound=1` at the freeze tree); run the single-edit mutant battery (QUALITY R50) against any new counter before freezing it; a re-ground names who read its rows side by side.
- `coverage`: obtain a non-author admit/reject spot-check of S073 before any coverage statement beyond +1 row; append the considerthese ledger row with the pin amendment (the ledger is byte-pinned by C2 G6 this round).


## Round 46 (attempt 2) result

Frozen at `.ufo/waves/round-46/attempt2/claims.json` (freeze commit `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`,
base `04af9bc92229232ea5cce8b32bfe59dd969eb26d`; claims sha256 `ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0`).
The attempt-1 instruments `r46-c1-gate.py` / `r46-c2-gate.py` are byte-identical at the freeze to the base
(the round's C1 work extends their selftests and adds the battery; the only counter amendments are logged
errata E3/E4 in `.ufo/waves/round-46/attempt2/counter-errata.md`).

| Axis | Before | After | Evidence pointer | Last change |
|---|---|---|---|---|
| depth:verifiability | 4 | 4 held — measured (counter mutation coverage closed: the frozen battery's 41 mutants across both attempt-1 counters go from 20 uncaught to 0 uncaught / all caught-or-committed-proof; no promotion limb moved — the promotion limbs live in the Scorecard's own Distance-to-next-score section and are not battery limbs) | before: `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt` (c1 `uncaught=7` of 20, c2 `uncaught=13` of 21, `baseline_failures=0`, BATEXIT=1); after: `controls/final-battery.txt` (c1 `caught+equivalent=20 uncaught=0`, c2 `caught+equivalent=21 uncaught=0`; equivalences: M14 with the 15-tree differential proof, G6b/G7a/G7c with the probe — proofs committed at `corpus/instruments/r46-mutant-equivalents/`); extended selftests `cases=83 failures=0` / `cases=147 failures=0` | r46a2 (held) |
| coverage | 8 | 8 held — measured (admitted frontier rows 28 -> 29 with F29; a +1 row is an expansion count, not a coverage-ratio move — same reading as round 45) | `corpus/instruments/r46-f29-gate.py --root <tree>`: base export `fixed=1/7 exit=1` (`controls/f29-gate-at-base.txt`), freeze tree `fixed=2/7`, tip `fixed=7/7 exit=0`; secondary `r44-frontier-count.py --expect 29`: base 28 exit 1, tip 29 exit 0; plain: frontier rows 28 -> 29, SOURCES rows 73 -> 74, knowledge entries 65 -> 66, absence sweep 2 -> 4 files; source S074 `mined` (capture sha-pinned, 9 quotes OK); census exit 0; capture binding `records=61 bound=61 unbound=0` | r46a2 (held) |
| depth:density | 9 | 9 held — non-target guard | `density.py` byte-identical base -> tip; the SKILL.md mean moves only by the appended Gates & probes registry block, not credited as depth | r46a2 (held) |

### Move log (attempt 2)

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 46a2 | depth:verifiability | battery before: c1 7/20 uncaught (M06, M07, M13, M14, M18, M19, M20), c2 13/21 uncaught (G1c, G2a, G2b, G2c, G3a, G4b, G5c, G6a, G6b, G6c, G7a, G7b, G7c); selftests 76/0 and 137/0 | battery after: 0 uncaught across 41 mutants (every residual a committed-proof equivalence); selftests 83/0 and 147/0; the f29 gate's 21 mutants graded by `r46-selftest-f29.py` through the battery's f29 mode | `controls/mutbat-before.txt` -> `controls/final-battery.txt`; errata E1-E4 |
| 46a2 | coverage | frontier 28 (F01-F28), SOURCES 73, knowledge 65; the maintainer-side advisory lifecycle held nowhere (absence sweep 2 files, both scope-out/context mentions) | frontier 29 (F29 = GitHub repository security advisories, maintainer side, scope-limited), SOURCES 74 (S074 tier A mined), knowledge 66, absence sweep 4 files | `controls/f29-gate-at-base.txt`; `r46-f29-gate.py --root .` = 7/7; the S074 lesson Gate block |

**Capabilities: no row enters this round** (the battery, selftest and gate are counters, not new capabilities).
**Saturation unchanged:** line 9/10 per owned axis, window N = 3; the lowest non-retired axis stays
depth:verifiability (4), which C1 worked. The score is held, not moved: the axis number is a
lane-owned judgment and the promotion limbs did not move; the measured increment is graded under the
quality trend.

## Round 47 result — honest stop (attempt 3)

Frozen claims: `.ufo/waves/round-47/claims.json`, commit `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`; base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`. Measured executable/corpus revision: `f0809bcaefe9f2b576d6e4d7a0d2ed43ebae214d`; receipts `.ufo/waves/round-47/controls/final-measure.txt`, `counts-before.json`, `counts-after.json` under that controls directory.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | 4 held; delta 0 | C1 mechanical limbs 0/11 → 11/11; **claim not fully verified**: its frozen S074 mined→rejected clause is refused because the demonstrated B3 regression is harmful. Wave-1 false-green controls remain valid counterexamples. `r47-routed-defects.py --root TREE`; no promotion limb completed, gated rechecks remain 22. |
| coverage | 8 | 8 held; delta 0 | C2 **unmet**: `r47-f30-gate.py --root TREE` reads 1/7 → 6/7, H1 red. Frontier rows remain 29, not the target 30. ZDI is sourced F02 enrichment, not new frontier. |
| depth:density | 9 | 9 held; no improvement claimed | Frozen `density.py` unchanged; SKILL mean **275.1 → 273.6** (34→35 blocks) due the appended registry block. Numeric regression is disclosed, not reformatted away or called a no-harm pass. The score/promotion bar is not redefined. |

### Round-47 measured move log

- C1: source scaffold lines containing `to append` 2→0; fence markers 4→0; old S074 citation matching lines 54→0 (59→0 occurrences); F29 entry stays 145 lines. S076 re-capture is reproduced twice by the committed instrument. S074 stays mined historical; only used-by changes to the round-46 lesson. This is useful repair, not fulfillment of the frozen harmful transition.
- C2: frontier 29→29; SOURCES 74→76; knowledge entries 66→67. Both new rows are docs/tier-A/mined, S075 for the F02 case and S076 for the reproducible F29 successor. A source-row increase is not coverage.
- Counting command for the plain ledger: `python3 .ufo/waves/round-47/final-counts.py --root TREE`, against the base and measured exports. Final census exit 0; binding 63/63; actual lane-root audit 67/67 with gated=22, broken=0, exit 0. Export-only strict CD-root check fails (66 cdroot_fail); the declared-root supplementary audit is separately receipted, not silently substituted.
- Exact plain-expression misses remain: `supersedes S074` matches 2 lines, not its frozen target 1; broad policy-name-file count is not a new-surface measure. No frozen target or counter byte changes after scoring.

**Capabilities:** none added. **Saturation/retirement:** unchanged; lowest non-retired axis remains depth:verifiability. No axis promotion or universal no-harm assertion is claimed. The round stops honestly; it does not reroll either failed claim.

### Planned evidence gates (not a new round dispatch)

Keep frozen diagnostic evidence separate from semantic admission. Any later proposal must first defeat the actual multiline-comment/fence, invisible-row and status-binding counterexamples; choose uncovered ground before freezing coverage. Preserve historical capture bindings and require a genuinely independent admit/reject spot-check before claiming outside discernment agreement.

## Round 48 result — attempt 2 (C1 verified on its frozen predicate; score held)

Frozen claim C1: `.ufo/waves/round-48/claims.json` (claims sha256 `b8022cdf…`; freeze `3546f70`; base `903d47e`). Frozen counter `corpus/instruments/shonen-form.py` sha256 `0ab32a2c…`, unchanged since `3546f70`. Measured revision `3d7e042` (restored SHONEN.md). Receipts: `.ufo/waves/round-48/attempt2/` (`c1-measure.txt`, `selftest.txt`, `census-end.txt`, `counts-before-after.txt`, `density.txt`, `r2-discrimination.txt`).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | 4 held; delta 0 | C1 predicate **verified** on the frozen counter: base `903d47e` `canonical=0 finding=SF-PREAMBLE exit=1` (356 lines, 52 boxes, archived checklist sha `596122c0…`); measured `3d7e042` `canonical=1 finding=SF-CLEAN exit=0` (12 lines, 4 boxes). Frozen selftest `cases=17 failures=0`. Score not moved: this is a checklist-form repair, and `resolve.py` censuses SKILL.md and corpus only, never SHONEN.md (wave-1 `R48Review28`). The claim is nominal on its axis; disclosed as M48-5, not hidden. |
| coverage | 8 | 8 held; delta 0 | Not claimed. Frontier rows 29→29 (`counts-before-after.txt`); SOURCES 76→77 with S077 (own-work, tier A, mined) as normative form, not frontier ground. |
| depth:density | 9 | 9 held; non-target proxy moved | Proxy disclosed, not reformatted: `density.py` mean on `SKILL.md` 273.6 (35 blocks, base) → 270.1 (36 blocks, working tree), from the appended `Round-48 author-checklist form checker` block (`density.txt`). Score is not claimed to move; same disclosure pattern as round 47. |

### Round-48 attempt-2 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 48a2 | depth:verifiability | `canonical=0 SF-PREAMBLE exit=1`; SHONEN.md 356 lines, 52 author marks | `canonical=1 SF-CLEAN exit=0`; SHONEN.md 12 lines, 4 boxes, pointers resolve | `attempt2/c1-measure.txt`; commit `3d7e042` |
| 48a2 | depth:verifiability (counter) | attempt-1 runner `shonen-form-selftest.py` present, uncommitted, no receipt on record | committed this round; `shonen-form-selftest.py` `cases=17 failures=0`, fixtures SHA pin verified | `attempt2/selftest.txt` |

**Capabilities: none added.** The `shonen-form.py` gate is a protocol-conformance instrument registered in SKILL.md, not a repertoire row. **Saturation unchanged:** line 9/10 per owned axis, window N = 3; lowest non-retired axis remains depth:verifiability (4), and C1 works it nominally (M48-5).

**Non-author verification:** outstanding. Wave-1 seats are lane seats, not outside verifiers; the outside spot-check of this round's admit (S077) and of the reject path is not yet on record.

### Planned for round 49 (not frozen)

1. **depth:verifiability (4, lowest):** route M48-5 and M48-4 into a claim whose counter reads a metric the axis actually measures (`resolve.py` citation survival over SKILL.md and corpus). Before and after from the same census command; no SHONEN-only credit.
2. **Fixture provenance (M48-4):** add a new non-frozen fixture file whose positive control is the shipped SHONEN.md bytes (sha `b1352168…`) and whose mutants cover the unchecked-box-with-evidence shape. The frozen `fixtures.json` is not amended.
## Round 49 result — citation-base grounding (C1) and the CVE Services publication surface (C2)

Frozen claims: `.ufo/waves/round-49/claims.json` (base `9b1662a2fa0e7c7b0ad6c4d45cb7786f27bdd03b`, freeze
commit `1954022d91c2063d0ce25bb5551778bc0b3e70f3`, do-nothing control
`.ufo/waves/round-49/controls/do-nothing.txt`).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0** | C1 verifies on its frozen predicate and moves a metric the axis counter itself reads: the frozen counter `corpus/instruments/citation-ground-check.py` reads `unresolved-class=68` at the base and `unresolved-class=0` with `ledger-rows=68 rows-resolving=68 findings=0` (exit 0) after the repair, and the axis instrument `resolve.py` reads a strictly higher lane rate (see the measurement below). The SCORE is held at 4 because the score-5 bar is a different measurement: `score-gap.py` prints "gap: 22 of 68 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims" and `recheck-audit.py --quiet` prints `executes=46 gated=22 broken=0` — unchanged from round 46, because those 22 gated lines fail closed on the lost domain bases, which only the operator can restore. Named residue: 79 further class members sit in `round-*-verifier-spotcheck.md` and `round-*-aggregator-*.md` lessons the lane may not edit; they are enumerated and disclosed as debt, not repaired. |
| coverage | 8 | **8 held; delta 0** | C2 verifies on its frozen predicate: the frozen counter `corpus/instruments/frontier-recheck-count.py` reads `FRONTIER-CENSUS rows=29 admitted=29 closed=29 problem-rows=0 registry=77` at the base and `FRONTIER-CENSUS rows=30 admitted=30 closed=30 problem-rows=0 registry=78` (`entries=33 pass=33 exit=0`) after the admission. The score is held because the coverage score's denominator is the lost domain root's 18-surface set (0 present, 18 corpus-attested, operator-owned re-scope), not the frontier count; a new frontier row is the lane's frontier measure, not a coverage-score move. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged (`density.py SKILL.md` mean and block count re-measured in the wave receipts). |

### Round-49 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 49 | depth:verifiability | `unresolved-class=68` (class-lane-bare 57, class-fleet-relative 11) | `unresolved-class=0`, `ledger-rows=68`, `rows-resolving=68`, `findings=0`, exit 0 | `.ufo/waves/round-49/controls/do-nothing.txt`; `corpus/instruments/citation-reground-ledger.md`; `corpus/instruments/citation-ground-check.py` (sha256 `988a5370…`, unchanged since the freeze) |
| 49 | depth:verifiability (axis census) | lane total 1071/4696 = 22.81% | strictly higher lane total; 19 repairs create a fresh distinct citation and 49 merge into an existing one | `corpus/instruments/citation-survival.md` (regenerated at the base commit) and the round-49 after-receipt |
| 49 | coverage | `FRONTIER-CENSUS rows=29 admitted=29 closed=29 problem-rows=0 registry=77` | `FRONTIER-CENSUS rows=30 admitted=30 closed=30 problem-rows=0 registry=78`; `entries=33 pass=33 exit=0` | `corpus/knowledge/cve-services-publication-api.md`; `corpus/source-snapshots/round-49/` (S078) |

**Capabilities:** none added. The new counter and the ledger are instruments and evidence, not repertoire rows.
**Saturation unchanged:** line 9/10 per owned axis, window N = 3; the lowest non-retired axis remains
depth:verifiability (4) and the round-49 claim works it on its own counter.
**Non-author verification:** outstanding. Wave-1 seats are lane seats, not outside verifiers; the outside
spot-check of this round's admits (S078, F30) and of its rejects is not yet on record.

### Planned for round 50 (not frozen)

1. **depth:verifiability (4, lowest):** the score-5 bar is "0 gated unsupported claims" and 22 gated
   recheck lines fail closed on the lost domain bases — operator-owned restoration, not a lane move. The
   lane-side lever that is still open is the residue: 79 class members in protected files. Either the
   operator or the aggregator re-grounds them (the lane may not edit those files), or the round declares
   them as permanent debt with a named owner and stops re-measuring them as a lane target.
2. **coverage (8):** the next frontier row must come from a first-party capture that is not the CVE Services
   write path; the round-49 scout seat screened three candidates and its report (in the wave directory) is the
   starting point.

### Round-49 wave disposition — validated, released undispatched (appended 2026-10-30)

The round's 64-seat wave 1 (`.ufo/waves/round-49/wave1-spec.json`, policy v2, validator exit 0) was built,
committed and handed over through `.ufo/waves/round-49/wave1.ready`, and the operator's wrap-up ruling
released it **without spawning a seat**. The two claims therefore verify on their frozen predicates only
(`unresolved-class=68 → 0`; `FRONTIER-CENSUS rows=29 → 30 admitted`), with no falsification credit from a
wave that never ran and no independent non-author verification on record. The verdict lines above stand; the
outside spot-check of this round's admits (S078, F30) and of its rejects is outstanding.


## Round 50 result — census-freshness gate (C1) and the OSV affected-range surface (C2'); freeze superseded

Frozen claims: `.ufo/waves/round-50/claims.v2.json` (base `c5e36360f5226c97d28f1937961b15c90e58827f`), which
SUPERSEDES the inherited `.ufo/waves/round-50/claims.json` freeze (commits `a2de23b`/`28c65eb`) per
`.ufo/waves/round-50/claims-erratum-1.md`: D1 — the frozen C2 surface (EPSS) was already admitted as F19;
D2 — the frozen counter commands name `python3` and `/home/vgpnk/...`, both absent on the host that ran this
round (the binding is shared by all 67 committed entry recheck lines); D3 — the committed
`controls/do-nothing-c2.txt` prints an output no run on this host can produce, and is retained byte-identical
as mistake evidence beside the real `controls/do-nothing-c2-winhost.txt`. All five mistakes are mined in
`corpus/lessons/round-50.md`.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0** | C1 verifies on its re-frozen predicate and is a capability acquisition (row below): the new gate `corpus/instruments/census-freshness-check.py` prints `CENSUS-FRESH=ok files=2` exit 0 at the measured tip (`controls/c1-gate-final.txt`), its committed self-test reads `selftest cases=3 failures=0` with stale-tree and tampered-census fixtures at exit 1 (`controls/c1-gate-selftest.txt`), and its pre-freeze battery reads `mutants=6 closed=5 survivors=1` with the survivor named (`controls/c1-mutbat.txt`). The gate is the fix for the round-49 stale-census mistake and would have caught the base state it inherits: the committed census at base read 201 files / 4758 distinct against a live 202 / 4771 (`.ufo/waves/round-50/r50-live-resolve.txt`). The census of record is regenerated at the tip (204 files / 4807 distinct). Score HELD at 4: the score-5 bar is still `score-gap.py`'s 22 gated lines on the lost domain bases (operator-owned) and the lane-side residue is now named as the 67 host-bound recheck lines (L0 kasegi round-50), not repaired. |
| coverage | 8 | **8 held; delta 0** | C2' verifies on its re-frozen predicate: frontier F31 (OSV affected-range events) admitted on S080 (OpenSSF's own specification page, capture `corpus/source-snapshots/round-50/S080.txt`, sha256 `97b850a4…`, 16 assertions Q1-Q16, `source-recheck.py --source S080` exit 0, `BROKEN=0`), entry `corpus/knowledge/osv-affected-range-events.md`, SOURCES row recording the S065 flip re-open, README F31 row and PROVINCE line appended at EOF. Counter before→after ON THIS HOST: `rows=30 admitted=30 closed=0 problem-rows=30 registry=79`, `entries=33 pass=0`, no F31 line (`controls/do-nothing-c2-winhost.txt`) → `rows=31 admitted=31 closed=1 problem-rows=30 registry=80`, `entries=34 pass=1`, the single pass `PASS F31 ids=S080 exit=0`, all 33 inherited fails exactly `recheck-exit-1` (`controls/c2-counter-final.txt`). Score HELD at 8: the denominator is the lost domain root's 18-surface set (0 present, operator-owned re-scope); F31 moves the frontier measure 30→31, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged. |

### Round-50 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 50 | depth:verifiability | committed census of record stale at base (201 files / 4758 distinct vs live 202 / 4771); nothing failed when a round quoted it | gate exits 0 only on byte-identity with a fresh regeneration (`CENSUS-FRESH=ok files=2`), exit 1 on stale/tampered fixtures, exit 2 unmeasurable; found bytes always restored | `corpus/instruments/census-freshness-check.py`; `controls/c1-gate-final.txt`, `controls/c1-gate-selftest.txt`, `controls/c1-mutbat.txt` (+ `controls/c1-mutbat.py` builder) |
| 50 | coverage | `FRONTIER-CENSUS rows=30 admitted=30 closed=0 problem-rows=30 registry=79`, `entries=33 pass=0` (this host) | `FRONTIER-CENSUS rows=31 admitted=31 closed=1 problem-rows=30 registry=80`, `entries=34 pass=1`, `PASS F31 ids=S080 exit=0` | `controls/do-nothing-c2-winhost.txt` → `controls/c2-counter-final.txt`; `corpus/knowledge/osv-affected-range-events.md`; `corpus/source-snapshots/round-50/` (S080 + manifest) |

**Capabilities:** one row enters the table (demonstrated running this round):

| name | what it can now do | evidence pointer | first-working round |
|---|---|---|---|
| `census-freshness-check` | prove the committed `citation-survival` census of record is byte-identical to what `resolve.py` generates over the current tree, exit 1 on stale or tampered censuses, exit 2 unmeasurable, and leave the found bytes exactly as they were | `python corpus/instruments/census-freshness-check.py <lane-root>` → `CENSUS-FRESH=ok files=2` exit 0; `--selftest` → `selftest cases=3 failures=0`; battery `mutants=6 closed=5 survivors=1` | 50 |

**Saturation:** line 9/10 per owned axis unchanged; the capability entry RESTARTS the stagnation window at
round 50 (last capability entry: 50; prior: 25 per the round-30 erratum, then none until this round). The
lowest non-retired axis remains depth:verifiability (4) and C1 works it on its own instrument.

**Non-author verification:** outstanding. No seat ran (the inherited wave spec is stale against
`claims.v2.json` and no AgentSwarm surface exists on this host); the most recent outside spot-check covers
round 49 (`corpus/lessons/round-49-verifier-spotcheck.md`). The claims verify on their re-frozen predicates
by re-derivable commands only.

### Planned for round 51 (not frozen)

1. **depth:verifiability (4, lowest):** decide the 67-entry host-bound recheck-line class with the operator
   (L0 kasegi round-50): either an authorized portability repair (same-line rewrite per R6, anchors kept, a
   `python3 || python` fallback form proven by F31's entry) or it stays disclosed debt with the operator as
   named owner; the score-5 bar (0 gated unsupported claims) stays operator-owned via `score-gap.py`'s 22
   gated lines.
2. **coverage (8):** the S065 flip is spent by F31; scout a fresh first-party capture for F32 (not the CVE
   Services write path, not EPSS, not OSV) and screen it against the province BEFORE any freeze — the
   round-50 D1 lesson makes the pre-freeze neighbor check mandatory.

## Round 51 result — the routed-defect corrections (C1, C2) and the CISA Vulnrichment surface (C3)

Frozen claims: `.ufo/waves/round-51/claims.json` (commit `73555dbaaea5c18456216b6c2646e97914d7b62b`, base
`bcd5d89a65ab612ef88e3d49cea0ef3cb3ccca09`), landed before implementation. The round-50 non-author closure routed
two first-priority defects (D1 control-provenance mislabel, D2 census-figure drift); both are fixed this round as
claims C1 and C2, and the round's own coverage move landed as C3 (frontier F32, source S081, pre-freeze neighbor
screen vs F18/F20/F22/F25/F30).

**Correction of record (C2, R9):** the round-50 rows in this file and in LOG.md state the census of record as
"204 files / 4807 distinct"; the certified tip census at `021989bf4f5699fa55c6d90abd37ce6ad1caa50a` reads **204
files / 4809 distinct** (GONE 3738, total 10298 — `git show 021989b:corpus/instruments/citation-survival.md`). The
filed 4807 lines above are retained byte-identical; **4809 at `021989b` is the census of record they describe**,
per lesson round-50 Erratum 2. The figures below are quoted from THIS round's final regeneration only (the C2
rule applied to the lane's own bytes).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0** | C1 verifies: the C1 do-nothing control of record is now a receipt this host produced — `controls/do-nothing-c1-winhost.txt` (real run at the c5e3636 export built per-file on this host: instrument absent → `C1_EXIT=2`, this host's `Python313\python.exe` path and backslash-quoted target in the error line), reproduce commands in the receipt header — and `.ufo/waves/round-51/erratum-1-c1-control-provenance.md` relabels the round-50 imported receipt (kept byte-identical) while correcting the factually wrong "Windows CPython error string" claim on probed facts (`controls/probe-host-r51.txt`: python3 = Store stub exit 49, /fast absent, Git-mount path form). Evidence-integrity repair only: the citation-resolution proxy is unchanged (see the census row below), so the score is HELD at 4 — the score-5 bar is still `score-gap.py`'s 22 gated lines on the lost domain bases and the 67 host-bound recheck lines stay operator-owned (L0 kasegi round-50 unanswered, routed around). |
| calibration | verdict-only (not a scored owned axis) | **improved (verdict row per the round-20 freshness precedent; no score asserted)** | C2 verifies: lesson round-50 Erratum 2 (commit `aca3c29`), the LOG round-50 correction below, and this section's correction paragraph name **4809 at `021989b`** as the census of record while every filed 4807 line stayed byte-identical (append-only, R9); rows naming 4809 in lesson-50/LOG/SCORECARD went 0/0/0 at base to 2/3/5 now; the lesson names the regenerated-after-record pattern the C1 gate exists to catch; and the rule was applied to this round's own bytes — the census figures in this section were measured only from the final regeneration at the tip. |
| coverage | 8 | **8 held; delta 0** | C3 verifies: frontier F32 (CISA Vulnrichment ADP enrichment) admitted on S081 (CISA's own README at the default branch `develop`, capture `corpus/source-snapshots/round-51/S081.txt`, sha256 `2da09414…`, 12 assertions Q1-Q12 each exactly-once, `source-recheck.py --source S081` exit 0, receipt `controls/s081-recheck.txt`), entry `corpus/knowledge/cisa-vulnrichment-adp-enrichment.md` with the pre-freeze neighbor screen named against F18/F20/F22/F25/F30, SOURCES rows S081 (mined) + S082 (rejected with reason and flip: the VeigaPunk mirror's history provably lacks the lost checkout's HEAD `1307b8b`), README F32 row + PROVINCE r51 amendment appended at EOF. Counter before→after ON THIS HOST: `rows=31 admitted=31 closed=1 problem-rows=30 registry=80`, `entries=34 pass=1`, zero F32 lines (`controls/do-nothing-c2-r51-winhost.txt`) → `rows=32 admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2`, the F32 pass `PASS F32 ids=S081 exit=0`, all 33 inherited fails exactly `recheck-exit-1` (`controls/c2-counter-final-r51.txt`). Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F32 moves the frontier measure 31→32, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged. |

**Census of record at this round's tip (C2 rule: quoted only from the final regeneration):** base `021989b` read
204 files / 4809 distinct → the round-51 tip reads **206 files / 4868 distinct** (RESOLVES 11, INTERNAL 1075, GONE
3782; total occurrences 10388; lane total 1086/4868 = 22.31%) — the two new corpus files (the F32 entry and the
round-51 lesson) and their citations, certified by the gate receipt `controls/c1-gate-final-r51.txt`
(`CENSUS-FRESH=ok files=2`, exit 0; selftest `controls/c1-gate-selftest-r51.txt`, `selftest cases=3 failures=0`).
**The gate caught this round itself once (recorded, not gamed):** the first regeneration (figures GONE 3785 /
1083/4868 = 22.27%) ran BEFORE this section's two gate receipts existed, and the lesson cites them — so the tip's
first gate re-check read `CENSUS-FRESH=stale` (3 citations GONE→RESOLVES once the receipts landed). The census was
regenerated over the truly final tree and the figures above quote THAT regeneration; the re-measured receipt is
the one of record (freeze rev 3). This is the same regenerated-after-record pattern the round's C2 correction
names in the round-50 lesson — caught by the instrument, on its own round, exactly as designed.

### Round-51 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 51 | depth:verifiability | C1-control receipts reproducible on this host: 0 (the sole C1 control's bytes are an old-Linux-host run: working python3, /fast path); 4 filed places label it host-produced, one claiming a "Windows CPython error string" this host's CPython does not print | 1 (`do-nothing-c1-winhost.txt`, real host run, `C1_EXIT=2`, reproduce commands in-header); the erratum of record names and corrects all four mislabels; the imported file retained byte-identical | `.ufo/waves/round-51/erratum-1-c1-control-provenance.md`; `controls/do-nothing-c1-winhost.txt`; `controls/probe-host-r51.txt` |
| 51 | calibration | rows naming 4809 as a census-of-record figure in lesson-50/LOG/SCORECARD: 0/0/0 (the prose said 4807 everywhere; only the certified census bytes said 4809) | 2/3/2, with every filed 4807 line byte-identical and the final-regeneration rule applied to this round's own figures | lesson round-50 Erratum 2; the LOG round-51 correction above; the correction paragraph in this section |
| 51 | coverage | `FRONTIER-CENSUS rows=31 admitted=31 closed=1 problem-rows=30 registry=80`, `entries=34 pass=1` (this host) | `FRONTIER-CENSUS rows=32 admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2`, `PASS F32 ids=S081 exit=0` | `controls/do-nothing-c2-r51-winhost.txt` → `controls/c2-counter-final-r51.txt`; `corpus/knowledge/cisa-vulnrichment-adp-enrichment.md`; `corpus/source-snapshots/round-51/` (S081 + manifest) |

**Capabilities:** none added (the corrections and the admission use the existing repertoire; the round-50
`census-freshness-check` capability re-demonstrated running this round: gate `CENSUS-FRESH=ok files=2`, selftest
`cases=3 failures=0`).
**Saturation unchanged:** line 9/10 per owned axis; window N = 3 with the last capability entry round 50. The
lowest non-retired axis remains depth:verifiability (4) and C1 works it.
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host); the most recent
outside spot-check is the round-50 closure that routed D1/D2. The claims verify on their frozen predicates by
re-derivable commands only.

### Planned for round 52 (not frozen)

1. **depth:verifiability (4, lowest):** unchanged bar — the 67 host-bound recheck lines and the 22 gated lines
   stay operator-owned (L0 kasegi round-50/46 unanswered); the lane-side lever is none until the operator rules,
   so the next round should NOT re-declare this class as a lane target (the round-49 L0 row already asked).
2. **coverage (8):** the next frontier row must clear the pre-freeze neighbor screen (mandatory since round-50 D1);
   candidate leads: NVD API 2.0 (NIST's own enrichment/search interface — distinct from F25's record format and
   F30's CVE Services write path), OpenSSF Scorecard (repo security health), or the CVE Program's ADP list page as
   a check on F32's scope limit; screen against the province BEFORE any freeze.

## Round 52 result — the routed figure corrections (C2), the R56 quote-count gate (C1), and the NVD API 2.0 surface (C3)

Frozen claims: `.ufo/waves/round-52/claims.json` (freeze commit `29c4bd9dd0aa05a9276be6e3d6b35da7d9ecaa31`, base
`6c0a08e2b99344ff3e82f8a52771af34fccc0155`), landed before implementation. The round-51 non-author closure routed two
figure-level defects and one screen-scope observation; the defects are fixed as claim C2 and the observation is
recorded as the C2 PROVINCE note AND applied as the C3 screen extension. The round's own moves: C1 (capability
acquisition working depth:verifiability, the lowest non-retired axis) and C3 (frontier F33). One post-freeze erratum:
`.ufo/waves/round-52/claims-erratum-1.md` (the C1 instrument was strengthened twice while landing its receipts — the
frozen selftest/audit figures are superseded there; the kill rule only got stronger).

**Correction of record (C2, R9):** the round-51 move-log row in this file records the 4809-row counts as "2/3/2";
the same commit measures **2/3/5** under the round-51 report's own counting command (`grep -c 4809
corpus/lessons/round-50.md LOG.md SCORECARD.md` → 2/3/5, re-measured first-hand this round before anything was
written). The filed "2/3/2" line is retained byte-identical and is superseded by this paragraph — the same
append-only pattern as the round-51 correction of the round-50 4807 figures, and the same D2 class (self-count
drift), this time caught by the closure rather than by the gate; the C1 instrument of this round exists so the
word-count member of that class is caught by a counter next time.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0** | C1 verifies (capability acquisition): `corpus/instruments/gate-quote-audit.py` (final sha `396d720e…`, freeze rev 1b) fail-closes the R56 word-count class — selftest `cases=9 failures=0` (`controls/quote-audit-selftest-r52.txt`); BEFORE state re-derived (`controls/quote-audit-before-r52.txt` rev-1 instrument on the uncorrected tree, exit 1; `controls/quote-audit-before-recheck-r52.txt` final instrument on pre-erratum lesson bytes: MISMATCH + LEDGER-ORPHAN, exit 1) → AFTER (`controls/quote-audit-after-r52.txt`: `annotated=5 ok=5 erratum-on-record=2 failures=0`, exit 0, the round-51 24→17 figure acknowledged by ledger row + lesson erratum text). Evidence-integrity capability only: the citation-resolution proxy is unchanged (see the census row below), so the score is HELD at 4 — the score-5 bar is still `score-gap.py`'s 22 gated lines on the lost domain bases and the 67 host-bound recheck lines stay operator-owned (L0 kasegi round-50 unanswered, routed around). |
| calibration | verdict-only (not a scored owned axis) | **improved (verdict row per the round-20/51 precedents; no score asserted)** | C2 verifies: both routed figure corrections landed append-only — the SCORECARD round-51 move-log "2/3/2" superseded by the correction-of-record paragraph above (2/3/5, filed line byte-identical) and `corpus/lessons/round-51.md` Erratum 1 (the S081 quote is 17 words by `wc -w`, not 24; filed line byte-identical, command in the erratum); plus the PROVINCE r52 adjacency annotation recording the S013.txt:65/F05 downstream-consumer observation with S013 kept out of scope. The D2 class is now instrument-checked, not just re-corrected: the C1 receipts cross-verify this round (BEFORE exit 1 → AFTER exit 0 on the same tree). |
| coverage | 8 | **8 held; delta 0** | C3 verifies: frontier F33 (NVD API 2.0 retrieval interface) admitted on S083 (live response for CVE-2024-3094 at NIST's services host, capture `corpus/source-snapshots/round-52/S083.txt`, sha256 `5c35a51b…`, 13077 bytes, 1 line, 12 assertions Q1-Q12 each exactly-once, `source-recheck.py --source S083` exit 0, receipt `controls/s083-recheck-r52.txt`), entry `corpus/knowledge/nvd-api-2.0-retrieval-interface.md` with the pre-freeze neighbor screen named against F05/F18/F19/F25/F30/F32 and EXTENDED with the downstream-consumer sweep over `corpus/source-snapshots/` per the round-51 closure's observation (receipt `controls/neighbor-screen-r52.txt`, run before the freeze commit); S066's round-42 flip spent by record (row byte-identical); SOURCES rows S083 (mined) + S084 (rejected with reason and flip — the JS-walled developer-hub page, `controls/s084-hub-shell.txt`); README F33 row + admission block appended at EOF; `knowledge-expected.txt` updated (69 entries). Counter before→after ON THIS HOST: `rows=32 admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2`, zero F33 lines (`controls/do-nothing-c3-r52.txt`, base export 6c0a08e built per-file, 506/506) → `rows=33 admitted=33 closed=3 problem-rows=30 registry=84`, `entries=36 pass=3`, `PASS F33 ids=S083 exit=0`, all 33 inherited entry fails exactly `recheck-exit-1` and 30 row fails exactly `missing-pass-line` (`controls/c2-counter-final-r52.txt`). Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F33 moves the frontier measure 32→33, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged. |

**Census of record at this round's tip (C2 rule: quoted only from the final regeneration):** the round-51 tip read
206 files / 4868 distinct → the round-52 tip reads **209 files / 4912 distinct** (RESOLVES 12, INTERNAL 1092, GONE
3808; total occurrences 10471; lane total 1104/4912 = 22.48%) — the new corpus files (the F33 entry and the round-52
lesson) and their citations, certified by the gate receipt `controls/c1-gate-final-r52.txt` (`CENSUS-FRESH=ok`).
Internal consistency: 12+1092+3808=4912; 12+1092=1104. The lesson quotes the figures only by pointer.

### Round-52 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 52 | depth:verifiability | Gate word-count annotations re-derived by any committed counter: 0 (the R56 rule is prose; the round-48 M48-3 class recurred in round-51 as the routed 24-vs-17 figure and was caught by the closure, not by a gate) | 1 fail-closed auditor (`gate-quote-audit.py`, selftest 9 cases 0 failures, BEFORE exit 1 → AFTER exit 0 on the round's own correction) + the errata ledger `gate-quote-errata.txt` (1 row, LEDGER-ORPHAN-checked) | `controls/quote-audit-selftest-r52.txt`; `controls/quote-audit-before-r52.txt` + `controls/quote-audit-before-recheck-r52.txt`; `controls/quote-audit-after-r52.txt`; `.ufo/waves/round-52/claims-erratum-1.md` |
| 52 | calibration | routed figure defects standing: 2 (move-log "2/3/2" vs measured 2/3/5; lesson "24 words" vs measured 17) + 1 unrecorded screen-scope observation (S013.txt:65/F05) | 0 standing: correction-of-record paragraph + lesson Erratum 1 (both append-only, filed lines byte-identical) + the PROVINCE r52 adjacency note; the class is instrument-checked going forward | the correction paragraph above; `corpus/lessons/round-51.md` Erratum 1; PROVINCE r52 annotations |
| 52 | coverage | `FRONTIER-CENSUS rows=32 admitted=32 closed=2 problem-rows=30 registry=82`, `entries=35 pass=2` (this host) | `FRONTIER-CENSUS rows=33 admitted=33 closed=3 problem-rows=30 registry=84`, `entries=36 pass=3`, `PASS F33 ids=S083 exit=0` | `controls/do-nothing-c3-r52.txt` → `controls/c2-counter-final-r52.txt`; `corpus/knowledge/nvd-api-2.0-retrieval-interface.md`; `corpus/source-snapshots/round-52/` (S083 + manifest) |

**Capabilities:** one row enters the table (demonstrated running this round):

| name | what it can now do | evidence pointer | first-working round |
|---|---|---|---|
| `gate-quote-audit` | re-derive every Gate word-count figure in the lane's lessons with `wc -w` semantics and fail closed on unacknowledged drift, >25-word quotes, deleted annotations (completeness floor), stale errata ledger rows and self-referential spans; accept a mismatch only when BOTH the ledger row and the lesson's own erratum text acknowledge it | `python corpus/instruments/gate-quote-audit.py --selftest` → `selftest cases=9 failures=0`; BEFORE `controls/quote-audit-before-r52.txt`/`-recheck` exit 1 → AFTER `controls/quote-audit-after-r52.txt` exit 0 | 52 |

**Saturation unchanged:** line 9/10 per owned axis; window N = 3 with the last capability entry round 52 (this
round's `gate-quote-audit` row RESTARTS the window). The lowest non-retired axis remains depth:verifiability (4) and
C1 works it on its own instrument.
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host); the most recent
outside spot-check is the round-51 closure that routed the defects this round fixes. The claims verify on their
frozen predicates by re-derivable commands only.

### Planned for round 53 (not frozen)

1. **depth:verifiability (4, lowest):** the R56 class now has a gate; the next lane-side lever is the same
   discipline for the OTHER figure classes the round-51 closure routed (self-count figures in move-log rows) — a
   figure-audit sibling that re-derives counting commands recorded in SCORECARD move-log rows, or an explicit
   decision that those stay closure-audited; the 67 host-bound recheck lines and the 22 gated lines stay
   operator-owned (L0 kasegi round-50/46 unanswered) and must NOT be re-declared as a lane target.
2. **coverage (8):** the next frontier row must clear the extended pre-freeze screen (downstream-consumer sweep
   included, mandatory since round 50/51); candidate leads: the NVD schema artifact on csrc.nist.gov (S066's own
   ground — evaluator*/cisa* mirror fields the live response did not show), OpenSSF Scorecard (repo security
   health; screen carefully against F33/F25 neighbors), or the CISA ADP list page as a check on F32's scope limit.

## Round 53 result — the routed D1 equality-limb repair (C1, nominal, held) and the NVD API 2.0 response schema (C2); the routed D2 wording fix (non-claim)

Frozen claims: `.ufo/waves/round-53/claims.json` (freeze commit `23448a2934cb9419bb0475d6262a458b38f2fe3a`, base
`e276dbf6255e0cea5e70456aada7e59e971f5853`), landed before implementation. The round-52 closure routed one defect (D1:
knowledge-expected.txt stale by 2 entries AND the recheck-audit equality limb host-broken on Windows separators) and one
observation (D2: the r52 erratum's "Filed BEFORE the implementation commit" wording, transparent in freeze rev 1b). D1 is
claim C1; D2 landed as a routed non-claim one-line append-only correction (`d9710d2`, filed line byte-identical, counts
1 -> 1 filed / 0 -> 1 marker per the frozen greps, receipt `controls/d2-base-greps-r53.txt`). One post-freeze erratum:
`.ufo/waves/round-53/claims-erratum-1.md` (freeze rev 1b) — two misderived after-literals in the frozen sentences
(C1 selftest completeness total=15 not 14; C2 33 inherited FAIL entry records not 34 — the figure both cited controls
printed), filed before the results landed; the class (R25 not applied to derived literals) is mined in the round-53 lesson.

**Correction of record (none):** no filed figure of an earlier round was found wrong this round; the only corrections are
the round's own post-freeze erratum above and the D2 wording supersession (both recorded where they belong).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal move, labelled per QUALITY R58** | C1 verifies on its frozen predicate: the equality limb of `corpus/instruments/recheck-audit.py` now normalizes BOTH sides to POSIX separators (`_as_posix`), `knowledge-expected.txt` is synced 69 -> 71 (+2: F31 `osv-affected-range-events.md`, F32 `cisa-vulnrichment-adp-enrichment.md` — the r52 closure's D1), and the selftest gains `expect-separator`, a Windows-separator fixture (relpath stub emitting backslashes vs the POSIX list) that the pre-repair bytes FAIL on the same scenario (driver receipt `controls/c1-fixture-red-r53.txt`: `missing=['corpus/knowledge/good.md'] unexpected=['corpus\knowledge\good.md']`) and the repaired bytes pass (exit=0, 0/0; selftest 18 case lines all ok, exit 0 — `controls/c1-after-selftest-r53.txt`; two further members of the same host-broken class repaired and disclosed in the frozen sentence: fixture writes pinned utf-8 — the base selftest CRASHED `UnicodeDecodeError` 0x97, receipt `controls/c1-donothing-r53.txt` — and the cwd fixture made interpreter-free, the Store stub having broken its want=False). The drift class is now catchable and NAMED: the repaired instrument over the UNSYNCED base list prints `expected=69 missing=0 unexpected=2` naming exactly the two routed entries (`controls/c1-catch-r53.txt`), where the base bytes printed `expected=69 missing=69 unexpected=71` — a pure separator artifact in which those names were indistinguishable from noise. On the synced lane tree: `expect=present expected=71 missing=0 unexpected=0` (`controls/c1-after-lane-r53.txt`) — the limb GREEN, stated beside the audit's overall exit 1, which stays red for the disclosed operator-owned host-bound class ONLY (strict pass=1/71 cdroot_fail=67, cwd_fail=3 — figures byte-identical to the do-nothing baseline). Score HELD at 4: the moved object is the equality limb and the expected list; the axis counter itself (the citation-resolution census) is not moved by this repair — the non-moving metric is named (R58), and the score-5 bar stays `score-gap.py`'s gated lines on the lost domain bases, operator-owned (L0 r50/46 routed around). The r31 limb-ledger's RA-expect find tokens stay exactly-once (1/1, receipt `controls/c1-fixture-red-r53.txt`); the limb-mutation REPLAY stays host-bound (kill commands need a real `python3`; every row reads `invalid:live-baseline`) and is disclosed in the lesson, not fixed. |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F34 admitted on S085 — NIST's own JSON Schema artifact for the NVD API 2.0 response (`https://csrc.nist.gov/schema/nvd/api/2.0/cve_api_json_2.0.schema`, capture `corpus/source-snapshots/round-53/S085.txt`, sha256 `4d1c4e77...`, 10394 raw bytes — the SAME count the r42 S066 screen recorded, so the served artifact is unchanged across the two opens; 13 assertions Q1-Q13 each exactly-once, `source-recheck --source S085` exit 0, receipt `controls/s085-recheck-r53.txt`), entry `corpus/knowledge/nvd-api-2.0-response-schema.md` with the extended pre-freeze neighbor screen incl. the downstream-consumer sweep (zero consumers; `controls/neighbor-screen-r53.txt`, run before the freeze commit); S066 re-opened under the UNSPENT term of its own flip (the evaluator*/cisa* mirror fields — the interface-contract term was the one F33's admission spent), the rejected row byte-identical, new row S085 per the S065->S080 precedent; README F34 row + r53 amendment appended at EOF (R6); PROVINCE r53 frontier amendment appended; SOURCES S085 row + search-log + 2 leads (OpenSSF Scorecard, CISA ADP list page — unopened) + registry-changes bullet 84 -> 85; `knowledge-expected.txt` 71 -> 72 sorted. Counter before->after ON THIS HOST: do-nothing `rows=33 admitted=33 closed=3 problem-rows=30 registry=84, entries=36 pass=3`, zero F34 lines (`controls/do-nothing-c2-r53.txt`, base export e276dbf built per-file, 513/513) -> `rows=34 admitted=34 closed=4 problem-rows=30 registry=85`, `entries=37 pass=4`, `FRONTIER-PASS F34 ids=S085`, 33 FAIL entry records all exactly `recheck-exit-1` and 30 row records exactly `missing-pass-line` (`controls/c2-counter-final-r53.txt`; the first run over the DRAFT entry had FAILED F34 — a Limits bullet starting with an S-id parsed as an evidence declaration — fixed before the final measurement, mined in the lesson). capture-binding `records=68 bound=68 unbound=0` exit 0 (`controls/capture-binding-r53.txt`). Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F34 moves the frontier measure 33 -> 34, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round, so the density instrument's input bytes are unchanged. |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51/52 precedents; no score asserted) | D2 (routed, non-claim) lands append-only: `.ufo/waves/round-52/claims-erratum-1.md` gains an `Erratum (round 53)` block superseding the opening sentence's filed-vs-committed wording (authored before, committed with 227d3ed, transparent in r52 freeze rev 1b); the filed sentence stays byte-identical, counts 1 -> 1 filed / 0 -> 1 marker (`controls/d2-base-greps-r53.txt` + the landed tree). The round's own calibration evidence is doubled by claims-erratum-1: two of the round's own frozen after-literals were caught misderived against their own controls and corrected BEFORE the results landed. |

**Census of record at this round's tip (quoted only from the final regeneration):** the round-52 tip read
209 files / 4912 distinct -> the round-53 tip reads **212 files / 4942 distinct** (RESOLVES 12, INTERNAL 1098, GONE
3832; total occurrences 10531; lane total 1110/4942 = 22.45%) — the new corpus files (the F34 entry and the round-53
lesson) and their citations, certified by the gate receipt `controls/c1-gate-final-r53.txt` (`CENSUS-FRESH=ok`).
Internal consistency: 12+1098+3832=4942; 12+1098=1110. The lesson quotes the figures only by pointer.

### Round-53 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 53 | depth:verifiability | equality limb on this host: `expected=69 missing=69 unexpected=71` all-red artifact + selftest crash (UnicodeDecodeError) — no committed counter here can name a real drift; expected list 69 vs tree 71, stale by the 2 entries the r52 closure routed | limb green on the synced tree (`expected=71 missing=0 unexpected=0`), the drift class named by the repaired instrument on the unsynced list (`missing=0 unexpected=2`, exactly F31+F32), fixture red-before/green-after committed in the selftest (expect-separator), selftest 18 cases failures=0 exit 0 | `controls/c1-donothing-r53.txt`; `controls/c1-after-lane-r53.txt`; `controls/c1-catch-r53.txt`; `controls/c1-fixture-red-r53.txt`; `controls/c1-after-selftest-r53.txt` |
| 53 | coverage | `FRONTIER-CENSUS rows=33 admitted=33 closed=3 problem-rows=30 registry=84`, `entries=36 pass=3` (this host, base export) | `FRONTIER-CENSUS rows=34 admitted=34 closed=4 problem-rows=30 registry=85`, `entries=37 pass=4`, `PASS F34 ids=S085` | `controls/do-nothing-c2-r53.txt` -> `controls/c2-counter-final-r53.txt`; `corpus/knowledge/nvd-api-2.0-response-schema.md`; `corpus/source-snapshots/round-53/` (S085 + manifest) |
| 53 | calibration | D2 wording observation standing (r52 closure) + 2 misderived frozen after-literals (caught this round) | D2 append-only correction landed (filed line byte-identical); both literals corrected by claims-erratum-1 before the results landed | `.ufo/waves/round-52/claims-erratum-1.md` Erratum (round 53) block; `.ufo/waves/round-53/claims-erratum-1.md`; `controls/d2-base-greps-r53.txt` |

**Capabilities:** no row enters the table this round — C1 is a repair of the existing `recheck-audit` instrument, not a
new capability; the stagnation window was restarted at round 52 (window N = 3, last capability entry round 52).

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not
active (capability window restarted r52).
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host); the most recent outside
spot-check is the round-52 closure that routed the defects this round fixes. The claims verify on their frozen predicates
by re-derivable commands only.

### Planned for round 54 (not frozen)

1. **depth:verifiability (4, lowest):** the equality limb now travels with the tree on this host; the next lane-side
   lever is the r52-planned figure-audit sibling (re-deriving counting commands recorded in SCORECARD move-log rows) or
   an explicit decision that those stay closure-audited; the 67 host-bound recheck lines, the 3 cwd_fail lines and the
   limb-mutation replay's python3 dependency stay operator-owned (L0 kasegi round-50/46 unanswered) and must NOT be
   re-declared as a lane target.
2. **coverage (8):** the next frontier row must clear the extended pre-freeze screen; the two recorded leads are
   OpenSSF Scorecard (repo security health; screen against held rows before opening) and the CISA ADP list page (a check
   on F32's scope limit); the S085 capture's own external-schema references (cvss-v*.json, ssvc-v2.0.3.json) are a
   further lead family if a future claim needs the referenced vocabulary.

## Round 54 result — the routed D53 figure corrections (non-claim, carry-in), the move-log figure audit (C1, capability acquisition, held), and the OpenSSF Scorecard check documentation (C2)

Frozen claims: `.ufo/waves/round-54/claims.json` (freeze commit `37fc40e1f3cc11cd2b25cf9b38868603a4140e79`, base
`32782bd6b564f80454af853b38868603a4140e79`), landed before implementation with the S086 capture + manifest + the extended
pre-freeze screen + the do-nothing/stand-in receipts in the same commit. The round-53 non-author closure routed three
status-neutral defects; the carry-in landed FIRST as a routed non-claim (`cfdf059`): one appended corrections file
(`.ufo/waves/round-54/controls/routed-d53-corrections.md`) superseding D53-1 (the r53 counter-final receipt trailer's
"34 inherited" vs its own measured `FAIL_entry_records=33`) and D53-2 (the "543 lines" metadata vs `wc -l` 542) with the
measured figures and sha pins — no filed byte edited (receipt `controls/d53-base-greps-r54.txt`; the file's own closure
check prints `d53-corrections=closed` exit 0); D53-3 (prompt-template L2-embed omission) is operator-side, routed via
`.ufo/l0-questions.md` (kasegi round-54 row; same-substance host question stands as kaidoku round-53), never treated as
answered. No post-freeze erratum was needed: every after-literal had been dry-run against the stand-in tree before the
freeze, and the two literals the dry-runs caught (the expected-list sort position; the Q2 anchor) were fixed pre-freeze
(mined in the round-54 lesson).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal capability move, labelled per QUALITY R58** | C1 verifies as a capability acquisition: `corpus/instruments/figure-audit.py` + `figure-audit-ledger.json` re-derive 9 figures recorded in lane records against committed bytes with whole-value comparison — frontier-rows 34, registry-rows 85, knowledge-expected 72, knowledge-files 72 (rev-pinned to 32782bd), capture-lines-s085 542 (naming the superseded 543), capture-bytes-s085 7590, capture-lines-s086 731, capture-sha256-s086 `fa84a017…` (the freeze capture), fail-entry-records 33 (re-running the frontier counter; naming the superseded 34 trailer) — receipts: selftest `cases=5 failures=0` exit 0 (`controls/c1-selftest-r54.txt`); RED control over the two r53 literals AS FILED reads both stale, exit 1 (`controls/c1-red-d53literals-r54.txt` — the routed D53 class is now machine-catchable); GREEN over the lane root `figures=9 ok=9 stale=0` exit 0 (`controls/c1-green-lane-r54.txt`); do-nothing at 32782bd: `git cat-file -e` exit 128, 0 mentions (`controls/c1-donothing-r54.txt`). Causally separable from C2: the green run was taken at the freeze+corrections state, before any C2 byte landed. The allow-list's missing `git ls-tree` head was caught fail-closed by the instrument's own limb pre-commit (mined). Score HELD at 4: the moved object is a new re-derivation capability; the axis counter (the citation-resolution census) is not the moved metric — the non-moving metric is named (R58), and the score-5 bar stays `score-gap.py`'s gated lines on the lost domain bases, operator-owned (L0 r50/46 routed around). |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F35 admitted on S086 — the OpenSSF Scorecard project's own generated check documentation (`https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md`, capture `corpus/source-snapshots/round-54/S086.txt`, sha256 `fa84a017…`, 731 lines, 46441 bytes, two byte-identical opens this round; 14 assertions Q1-Q14 each exactly-once, `source-recheck --source S086` exit 0, receipt `controls/s086-recheck-r54.txt`), entry `corpus/knowledge/openssf-scorecard-checks.md` (4 falsifiable rules with rejected over-generalizations; distinctness vs F24/F17/F31/F18; Limits: aggregate-score/weights/publisher unasserted, moving `main` pinned by sha), the extended pre-freeze screen incl. the downstream-consumer sweep run at base before the freeze (`controls/neighbor-screen-r54.txt`: zero held rows, zero snapshot consumers), README F35 row + r54 amendment appended at EOF (+26/−0), PROVINCE r54 amendment (+2/−0), SOURCES S086 row + search-log + registry bullet 85 -> 86 (+3/−0, no other row touched), `knowledge-expected.txt` 72 -> 73 (insert BEFORE operator-queue.md, `LC_ALL=C sort -c` clean — the sort-position catch is mined). Counter before->after ON THIS HOST: do-nothing `rows=34 admitted=34 closed=4 problem-rows=30 registry=85`, `entries=37 pass=4`, zero F35 lines, FAIL records 33 (`controls/do-nothing-c2-r54.txt`, base export built per-file, 518 corpus files + PROVINCE) -> `rows=35 admitted=35 closed=5 problem-rows=30 registry=86`, `FRONTIER-PASS F35 ids=S086`, `entries=38 pass=5`, FAIL records 33 (=38−5, invariant) (`controls/c2-counter-final-r54.txt`); capture-binding `records=69 bound=69 unbound=0` exit 0, `multi_row_url=7` unchanged 7 -> 7 (`controls/capture-binding-r54.txt`); expect limb `expected=73 missing=0 unexpected=0` (`controls/c2-expect-and-counts-r54.txt`). Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F35 moves the frontier measure 34 -> 35, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round; the new instrument's registration evidence lives in the capabilities row below and its selftest, not in a mid-file SKILL registry insert (R6: SKILL.md is the lane's most line-cited file; disclosed in the lesson Limits). |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51/52/53 precedents; no score asserted) | The carry-in corrections landed append-only with byte pins and a runnable closure check (`d53-corrections=closed`); three of the round's own mistakes were caught BEFORE their data landed (the sort position by `sort -c` in the stand-in; the Q2 anchor by `source-recheck`'s anchor limb; the allow-list head by the audit's own read-only limb), a fourth at the round-end census gate (the S086 row's cell count: E01 fields=12 -> the 11-field row shape, validate exit 0, mined as Mistakes row 6) and all six Mistakes rows carry class/captured-by/fix; the D53-3 operator routing went through the L0 channel rather than being treated as answered. |

**Census of record at this round's tip (quoted only from the final regeneration):** the round-53 tip read
212 files / 4942 distinct -> the round-54 tip reads **215 files / 4978 distinct** (RESOLVES 12, INTERNAL 1107, GONE
3859; total occurrences 10609; lane total 1119/4978 = 22.48%) — the three new corpus files (the F35 entry, the
figure-audit instrument, the round-54 lesson) and their citations, certified by the gate receipt
`controls/c1-gate-final-r54.txt` (`CENSUS-FRESH=ok`) measured after the last corpus/SCORECARD/LOG edit. Internal
consistency: 12+1107+3859=4978; 12+1107=1119. The figures are the regeneration FIXED POINT (the census pair cites
corpus paths itself, so the first regeneration after new corpus files moves the classes once; resolve.py was re-run to
stability and the pair committed is the stable pair). The lesson quotes the figures only by pointer. Bookkeeping move only
(R58 nominal labeling on C1): no citation-resolution move is claimed.

### Round-54 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 54 | depth:verifiability | no committed counter re-derives recorded figures; the r53 trailer's 34 and metadata 543 stood uncaught (routed D53-1/D53-2) | figure-audit capability: 9 recorded figures re-derived, whole-value, fail-closed; the D53 literals AS FILED read stale (red control exit 1); selftest 5/0; green 9/0 exit 0 | `controls/c1-selftest-r54.txt`; `controls/c1-red-d53literals-r54.txt`; `controls/c1-green-lane-r54.txt`; `controls/c1-donothing-r54.txt`; `controls/routed-d53-corrections.md` |
| 54 | coverage | `FRONTIER-CENSUS rows=34 admitted=34 closed=4 problem-rows=30 registry=85`, `entries=37 pass=4`, zero F35 (this host, base export) | `FRONTIER-CENSUS rows=35 admitted=35 closed=5 problem-rows=30 registry=86`, `FRONTIER-PASS F35 ids=S086`, `entries=38 pass=5`, FAIL records 33 invariant | `controls/do-nothing-c2-r54.txt` -> `controls/c2-counter-final-r54.txt`; `corpus/knowledge/openssf-scorecard-checks.md`; `corpus/source-snapshots/round-54/` (S086 + manifest) |
| 54 | calibration | r53 routed D53-1/D53-2 standing + the operator-side D53-3 | corrections file landed append-only with byte pins + closure check exit 0; D53-3 routed via the L0 channel (kasegi round-54 row) | `.ufo/waves/round-54/controls/routed-d53-corrections.md`; `.ufo/waves/round-54/controls/d53-base-greps-r54.txt` |

**Capabilities:** one row enters the table this round (recorded in this round section per the round-43/R6-append
practice — the main capabilities table sits mid-file in a line-anchored SCORECARD):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| move-log-figure-audit | Re-derives figures recorded in lane records against committed bytes (rev-pinned or live), whole-value comparison, fail-closed on drift or unreadable input — catches the routed D53 receipt-trailer/metadata number-drift class | `python corpus/instruments/figure-audit.py` -> `FIGURE-AUDIT figures=9 ok=9 stale=0 exit=0` (`.ufo/waves/round-54/controls/c1-green-lane-r54.txt`); selftest `cases=5 failures=0` (`controls/c1-selftest-r54.txt`); red control on the r53 literals AS FILED exit 1 (`controls/c1-red-d53literals-r54.txt`) | 54 |

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not
active (a capability entered the repertoire this round — the stagnation window restarts at 54).
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host; D53-3 routed via L0); the
most recent outside spot-check is the round-53 closure that routed the defects this round fixes. The claims verify on
their frozen predicates by re-derivable commands only.

### Planned for round 55 (not frozen)

1. **depth:verifiability (4, lowest):** the figure-audit ledger grows one round at a time — fold the round-54 figures
   in (rows=35, registry=86, entries=38, pass=5, expected=73) and audit the round's own move-log row, so every future
   figure drift is machine-caught the round after it lands; the 67 host-bound recheck lines, the 3 cwd_fail lines and
   the limb-mutation replay's python3 dependency stay operator-owned (L0 kasegi round-50/46 unanswered) and must NOT
   be re-declared as a lane target.
2. **coverage (8):** the remaining recorded leads are the CISA ADP list page (a check on F32's scope limit) and the
   GitHub repository security advisories REST API (the reproducible S076-capture sibling lead, unopened since round
   47); S086's own unasserted surfaces (aggregate-score computation/weights, publisher/API, Prox) are a further lead
   family if a future claim needs them; every next frontier row clears the extended pre-freeze screen including the
   downstream-consumer sweep.

## Round 55 result — the routed DF-1/DF-2 carry-in (non-claim, addressed first), the figure-audit ledger growth 9 → 17 (C1, capability extension, held), and the GitHub repository security advisories REST API surface (C2)

Frozen claims: `.ufo/waves/round-55/claims.json` (freeze commit `fd7838c1ffc3c4a36de58c9bcf73729d476df94c`, base
`ed60637394b170a4120fda501b9b9c5387f2df24` — the round-54 closure tip), landed before implementation with the S087 capture +
manifest + the extended pre-freeze screen + the do-nothing/stand-in/binding/recheck receipts in the same commit. The round-54
non-author closure (verdict admitted=true) routed two status-neutral defects; the carry-in landed FIRST as a routed non-claim
(`d0237d6`): (DF-2) the before-state receipt cited by cfdf059 but never committed was regenerated as
`.ufo/waves/round-54/controls/d53-base-greps-r54.txt` naming the same five sha pins, the four filed literals each exactly once
at base and the measured 542/7590/33 — every limb re-run live before landing, so every citation resolves; (DF-1) the r54
report/freeze prose "0 mentions in base SCORECARD" superseded by 2 (the cited receipt's own limb prints 2; base bytes re-derive
2 at SCORECARD.md:2102,:2158 — the r52-planned/r53-routed sibling text) via the appended R9-form erratum
`.ufo/waves/round-55/controls/df1-mentions-erratum.md` with its closure check printing `df1-erratum=closed` exit 0 — no filed
byte edited. The one-per-round stand-in dry-run caught the round's biggest own mistake pre-data (the v1 stand-in omitted the
uncommitted capture pair and the counter read F36 `manifest-unreadable`; v2 is the of-record dry-run — mined in the lesson).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal capability-extension move, labelled per QUALITY R58** | C1 verifies: the figure-audit ledger grows 9 → 17 pinned figures (`00832d2`). The round-54 figures fold in rev-pinned to `5108584aab38a1919992c46d0224f6ec1cb59363` (frontier-rows-r54 35, registry-rows-r54 86, entries-r54 38 via the F-row entry-cell comma split, knowledge-expected-r54 73, knowledge-files-r54 73) and the DF-1 do-nothing mention counts are pinned machine-checkably (figure-audit-mentions-base-scorecard 2 — naming the superseded filed-prose 0, mentions-base-log 0, mentions-base-knowledge-expected 0, the latter two via awk whole-count so a zero prints with exit 0). Receipts: selftest `cases=5 failures=0` exit 0 (`controls/c1-selftest-r55.txt`); GREEN over the lane root `FIGURE-AUDIT figures=17 ok=17 stale=0 exit=0` (`controls/c1-green-lane-r55.txt`, run before any C2 byte — every new derive addresses committed revs or the invariant FAIL-record count 33 = 38−5 = 39−6, so the audit stays green across C2); RED control over the DF-1 prose figures AS FILED plus two wrong fold-figures reads 3 stale exit 1 (`controls/c1-red-df1-r55.txt` + `red-df1-ledger.json`); do-nothing at base ed60637 in the freeze commit (`controls/c1-donothing-r55.txt`: 9 ids at base, the new entry ids 0, the base ledger 9/9 green over the lane root). Score HELD at 4: the moved object is the re-derivation repertoire (9 → 17 machine-checked figures), not the citation-resolution census the axis counter reads — the non-moving metric is named (R58), and the score-5 bar stays `score-gap.py`'s gated lines on the lost domain bases, operator-owned (L0 r50/46 routed around). |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F36 admitted on S087 — GitHub Docs' own REST reference page for repository security advisories (`https://docs.github.com/en/rest/security-advisories/repository-advisories`), first admission of the round-47 lead (then SOURCES.md:137, provenance `corpus/source-snapshots/round-47/S076.txt:574`; the lead line's bytes unchanged, flip recorded in the registry bullets), opened 2026-11-01. Capture `corpus/source-snapshots/round-55/S087.txt` (3407 lines, 137738 snapshot bytes over 937712 fetched HTML bytes, sha256 `3eebdf47…`; three same-sha instrument opens + two identical raw-HTML curl opens this round; 14 assertions Q1-Q14 each occurrences=1 at its pinned anchor, `source-recheck --source S087` exit 0). Entry `corpus/knowledge/github-repository-security-advisories-rest-api.md`: attribution, 4 falsifiable claims with rejected over-generalizations (the twelve-endpoint family with per-endpoint permission tiers and the list endpoint's unauthenticated public-resource carve-out; the POST/PATCH create-update pair with the required-body contract and the closed published/closed/draft vocabulary; the standalone ghsa_id-keyed 202-Accepted CVE request; the private-fork route that alone names a second permission set), distinctness vs F28/F29/F30 argued from the neighbor screen, honest Limits (rate limits/plan-gated parameters/response examples/error schemas unasserted; live docs.github.com pinned by sha). Extended pre-freeze screen incl. the downstream-consumer sweep run at base BEFORE the freeze (`controls/neighbor-screen-r55.txt`: the URL held by no README/PROVINCE/knowledge row; only F29 the concepts-lifecycle neighbor; zero snapshot consumers). Committed `d9d77ec`: README F36 row + r55 admission block at EOF (+29/−0), PROVINCE r55 amendment (+2/−0), SOURCES S087 row inserted after S086 + hunt bullet + row-added bullet (+3/−0, zero deleted lines, no existing row touched), `knowledge-expected.txt` 73 → 74 (insert BEFORE `github-repository-security-advisories.md`, `'-' < '.'` byte-wise, `LC_ALL=C sort -c` clean). Counter before→after ON THIS HOST: do-nothing `rows=35 admitted=35 closed=5 problem-rows=30 registry=86`, `entries=38 pass=5`, zero F36 lines, FAIL records 33 (`controls/do-nothing-c2-r55.txt`, per-file base export of ed60637) → `rows=36 admitted=36 closed=6 problem-rows=30 registry=87`, `FRONTIER-PASS F36 ids=S087`, `entries=39 pass=6`, FAIL records 33 (=39−6, invariant) (`controls/c2-counter-final-r55.txt`); capture-binding 69 → `records=70 bound=70 unbound=0` exit 0, `multi_row_url=7` unchanged 7 → 7 (`controls/capture-binding-r55.txt`, both runs pre-freeze, re-confirmed in the final receipt); expect limb 73 → expected=74 missing=0 unexpected=0. Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F36 moves the frontier measure 35 → 36, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round; the round-54 non-target guard reasoning applies unchanged (R6: SKILL.md is the lane's most line-cited file). |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51/52/53/54 precedents; no score asserted) | The carry-in landed append-only with byte pins and runnable closure checks (`df1-erratum=closed` exit 0, and the r54 `d53-corrections=closed` re-derivable); six Mistakes rows in the round-55 lesson carry class/captured-by/fix — two mined routed defects (DF-2 the unresolvable pointer; DF-1 the memory-composed prose count) and four own-catches, three of them BEFORE their data landed (the v1 stand-in's incomplete declared-adds list caught by the dry-run limb; the export-root audit draft caught by the fail-closed derive limb before the of-record receipt; the three non-unique manifest quotes caught by the pre-freeze recheck) and one at the capture's byte-verification step (the MSYS grep CR artifact settled by a byte-level read); the D53-3/AgentSwarm operator routing stays via the L0 channel, never treated as answered. |

**Census of record at this round's tip (quoted only from the final regeneration):** the round-54 tip read
215 files / 4978 distinct → the round-55 tip reads the figures in the gate receipt
`controls/gate-final-r55.txt` (`CENSUS-FRESH=ok`), measured after the last corpus/SCORECARD/LOG edit —
quoted there, not here, so this cell cannot drift from the receipt (the round-54 practice: the lesson quotes
by pointer). Bookkeeping move only (R58 nominal labeling on C1): no citation-resolution move is claimed.

### Round-55 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 55 | depth:verifiability | 9 pinned figures; the r54 figures and the DF-1 mention counts stood un-re-derived; the DF-1 prose drift was caught by the closure judge's reading, not by any lane instrument | 17 pinned figures: the r54 state folds in rev-pinned (35/86/38/73/73) and the DF-1 mentions pin machine-checkably (2/0/0); the prose figures AS FILED read stale (red exit 1); selftest 5/0; green 17/0 exit 0 | `controls/c1-selftest-r55.txt`; `controls/c1-green-lane-r55.txt`; `controls/c1-red-df1-r55.txt`; `controls/c1-donothing-r55.txt`; `.ufo/waves/round-55/controls/df1-mentions-erratum.md` |
| 55 | coverage | `FRONTIER-CENSUS rows=35 admitted=35 closed=5 problem-rows=30 registry=86`, `entries=38 pass=5`, zero F36 (this host, base export) | `FRONTIER-CENSUS rows=36 admitted=36 closed=6 problem-rows=30 registry=87`, `FRONTIER-PASS F36 ids=S087`, `entries=39 pass=6`, FAIL records 33 invariant | `controls/do-nothing-c2-r55.txt` -> `controls/c2-counter-final-r55.txt`; `corpus/knowledge/github-repository-security-advisories-rest-api.md`; `corpus/source-snapshots/round-55/` (S087 + manifest) |
| 55 | calibration | the r54 closure's routed DF-1/DF-2 standing | DF-2 receipt regenerated with every limb re-run live (all citations resolve); DF-1 superseded append-only with a runnable closure check; the machine-catching ledger entries landed with C1 | `.ufo/waves/round-54/controls/d53-base-greps-r54.txt`; `.ufo/waves/round-55/controls/df1-mentions-erratum.md` |

**Capabilities:** the round-54 `move-log-figure-audit` row is extended in place of a new row: the capability's ledger
grows 9 → 17 (the first-working round stays 54; the extension evidence is this round's green/red/selftest receipts —
recorded in this round section per the round-43/R6-append practice).

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not
active (the repertoire moved this round — the ledger grew 9 → 17 with three new receipts).
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host; routed via L0); the most
recent outside spot-check is the round-54 closure that routed the defects this round fixes. The claims verify on their
frozen predicates by re-derivable commands only.

### Planned for round 56 (not frozen)

1. **depth:verifiability (4, lowest):** the figure-audit ledger keeps growing one round at a time — fold the round-55
   figures in (rows=36, registry=87, entries=39, expected=74) rev-pinned to this round's tip, so every future figure
   drift stays machine-caught the round after it lands; the 30 problem-rows / 33 host-bound FAIL records, the 67
   `cd /home/...` recheck lines and the limb-mutation replay's python3 dependency stay operator-owned (L0 kasegi
   round-50/46 unanswered) and must NOT be re-declared as a lane target.
2. **coverage (8):** the remaining recorded leads are the CISA ADP list page (a check on F32's scope limit) and
   S087's own unasserted surfaces (rate limits, plan-gated parameters — the developer-hub pages were JS-walled for the
   lane instrument at S084, so the REST reference's sibling parameter documentation is the checkable form); every next
   frontier row clears the extended pre-freeze screen including the downstream-consumer sweep.

## Round 56 result — the routed DF-3 carry-in (non-claim, addressed first), the figure-audit ledger growth 17 → 27 incl. the census-freshness literals (C1, capability extension, held), and the CISA Vulnrichment published record list surface (C2)

Frozen claims: `.ufo/waves/round-56/claims.json` (freeze commit `6a4cef002891d2e23253a187fb61a58c2fc18c7c`, base
`e166f1bba49446e67de317bff62d3c0b84eb1d7c` — the round-55 closure tip + the integrator's verifier-spotcheck commit),
landed before implementation with the S088 capture + manifest + the extended pre-freeze screen + the do-nothing and
stand-in receipts in the same commit. The round-55 non-author closure (verdict admitted=true) routed one status-neutral
defect (DF-3); the carry-in landed FIRST as a routed non-claim (`77a1394`): the `CENSUS-FRESH=ok` prose in the round-55
report, the SCORECARD round-55 census cell and the LOG round-55 entry is superseded append-only by the R9-form erratum
`.ufo/waves/round-56/controls/df3-census-erratum.md` naming the receipt's own printed limb
(`CENSUS-FRESH=stale … [exit=1]`) as the superseding fact — no filed byte edited, closure check `df3-erratum=closed`
exit 0 — and the fixed-point receipt `.ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt` reproduces the routed
defect end to end over a faithful reconstruction of the round-55 tip (run A with the receipt moved out reads the
committed pair's 1118/3883/1130; the receipt restored flips exactly ONE citation GONE→INTERNAL to 1119/3882/1131 =
22.56%; run C identical — the fixed point; freshness gate ok exit 0), matching the closure verifier's §3 numbers
exactly; the reconstruction's named pitfall is recorded in the receipt (the `.git`/`.git/` citations resolve on any
real worktree disk — excluding them read 2 citations low, which the committed-pair class diff named exactly). One
mid-round claims erratum (`.ufo/waves/round-56/claims-erratum-1.md`, landed with C2 `8c2d9a4`): the freeze's lead-line
counting command mis-typed `want 1`, superseded by `want 3 = 3` (base = tip) with the exact-line sha pin
`90b336a2…` — mined in the lesson.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal capability-extension move, labelled per QUALITY R58** | C1 verifies: the figure-audit ledger grows 17 → 27 pinned figures (`5eab221`) on two limbs. (Fold, the planned-for-56 limb) the round-55 figures enter rev-pinned to `133c575394099abf28ddf1b0125c53aefde3e0fa` (frontier-rows-r55 36, registry-rows-r55 87, entries-r55 39 via the F-row entry-cell comma split, knowledge-expected-r55 74, knowledge-files-r55 74). (Census literals, the DF-3 carry-in's instrument extension) the census-freshness receipt's printed literals enter as whole-value entries: `census-fresh-literal-r55` want `stale` — the filed prose `ok` superseded by the DF-3 erratum, `census-internal-r55-receipt`/`census-gone-r55-receipt` want 1118/3883 (the committed pair of record), `census-fixedpoint-internal-r55`/`census-fixedpoint-gone-r55` want 1119/3882 (the DF-3 fixed-point receipt) — the prose-vs-receipt class AND the two-generation confusion are machine-caught. Receipts: selftest `cases=5 failures=0` exit 0 (`controls/c1-selftest-r56.txt`); GREEN over the lane root `FIGURE-AUDIT figures=27 ok=27 stale=0 exit=0` (`controls/c1-green-lane-r56.txt`, run before any C2 byte and re-run green across the C2 bytes — every new derive addresses committed revs, files C2 does not touch, or the invariant FAIL-record count 33 = 39−6 = 40−7); RED control over the DF-3 prose literal AS FILED (want `ok` against the receipt's printed `stale`) plus the generation-confusion figure (want 3882 against the receipt's printed 3883) reads 2 stale exit 1 (`controls/c1-red-df3-r56.txt` + `red-df3-ledger.json`); do-nothing at base e166f1b in the freeze commit (`controls/do-nothing-c1-r56.txt`: 17 ids at base, the ten new entry ids 0, the base ledger 17/17 green over the lane root). Score HELD at 4: the moved object is the re-derivation repertoire (17 → 27 machine-checked figures), not the citation-resolution census the axis counter reads — the non-moving metric is named (R58), and the score-5 bar stays `score-gap.py`'s gated lines on the lost domain bases, operator-owned (L0 r50/46 routed around). |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F37 admitted on S088 — the CISA Vulnrichment published record list, read through GitHub's own git-trees machine interface at the repository's default ref (`https://api.github.com/repos/cisagov/vulnrichment/git/trees/develop`), first admission of the recorded CISA ADP list-page lead (SOURCES.md:143, named in the round-52 SCORECARD planned-for-53; the lead line's bytes unchanged, sha `90b336a2…` at base and tip, flip recorded in the registry bullets), opened 2026-11-01. Capture `corpus/source-snapshots/round-56/S088.txt` (1 line, 7204 snapshot bytes over 7203 fetched bytes, sha256 `09ce0b10…`; four same-sha instrument opens this round — probe 14:19:12Z, recorded 14:34:05Z, verification 14:34:05Z/14:34:06Z; one raw curl open serves the SAME tree object pretty-printed at 8956 bytes and parses equal, `controls/s088-opens-r56.txt`; 6 assertions Q1-Q6 each occurrences=1 at anchor line 1, `source-recheck --source S088` exit 0). Entry `corpus/knowledge/cisa-vulnrichment-record-list.md`: attribution, 4 falsifiable claims with rejected over-generalizations (the 28 per-year record folders 1999-2026 with no gap, year-form count re-derivable from the capture; the content-addressed self-declared-complete object — top sha `e8d691a5…` pinned, `"truncated":false`, 34 entries — with the representation-variant byte forms parsed equal; the 8501-byte README blob whose round-51 snapshot sha `2da09414…` reproduces same-day, the check on F32's scope limit; the six non-record support entries with flowcharts.md named as process description, not enrichment data), distinctness vs F32/F25/F30/F20 argued from the extended pre-freeze screen, honest Limits (the develop ref is mutable and the pin is the arbiter; byte-stability per representation only; year-folder contents/sync cadence/commit history/rate limits unasserted; the releases variant probed EMPTY). Extended pre-freeze screen incl. the downstream-consumer sweep run at base BEFORE the freeze (`controls/neighbor-screen-r56.txt`: zero held README/PROVINCE/knowledge rows hold the trees-API URL; the repo-URL holders are the S081 row and the round-51 hunt bullet, distinct grounds; snapshot hits only the round-51 capture and this round's own pair). Committed `8c2d9a4`: README F37 row + r56 admission block at EOF (+3682 bytes, pure append), PROVINCE r56 amendment (+1054 bytes, pure append), SOURCES S088 row inserted after S087 + hunt bullet + row-added bullet (inserts only, no existing line modified or deleted), `knowledge-expected.txt` 74 → 75 (insert after `cisa-vulnrichment-adp-enrichment.md`, `LC_ALL=C sort -c` clean). Counter before→after ON THIS HOST: do-nothing `rows=36 admitted=36 closed=6 problem-rows=30 registry=87`, `entries=39 pass=6`, zero F37 lines, FAIL records 33 (`controls/do-nothing-c2-r56.txt`, per-file base export of e166f1b, 531/531) → `rows=37 admitted=37 closed=7 problem-rows=30 registry=88`, `FRONTIER-PASS F37 ids=S088`, `entries=40 pass=7`, FAIL records 33 (=40−7, invariant) (`controls/c2-counter-final-r56.txt`); capture-binding 70 → `records=71 bound=71 unbound=0` exit 0, `multi_row_url=7` unchanged 7 → 7; expect limb 74 → 75 sorted, 75 files. Score HELD at 8: the denominator is the lost domain root's 18-surface set (operator-owned re-scope); F37 moves the frontier measure 36 → 37, not the coverage score. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round; the round-54/55 non-target guard reasoning applies unchanged (R6: SKILL.md is the lane's most line-cited file). |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51..55 precedents; no score asserted) | The DF-3 carry-in landed append-only with byte pins and a runnable closure check (`df3-erratum=closed` exit 0) plus the machine-catching extension the routed fix asked for; the fixed-point receipt REPRODUCES the defect's root cause (exactly one self-referential citation) instead of asserting it; six Mistakes rows in the round-56 lesson carry class/captured-by/fix — one mined routed defect (DF-3) and five own-catches, four before any data landed (the partial-export census flip caught against the verifier's published numbers; the neighbor-screen inline note corrected against its own printed limb; the heredoc-unexpanded receipt limb disclosed in place; the Windows sort.exe PATH resolution) and one at the freeze (the mis-typed counting command, superseded by claims-erratum-1); the D53-3/AgentSwarm operator routing stays via the L0 channel, never treated as answered. |

**Census of record at this round's tip (quoted only from the final regeneration):** the round-55 tip read the figures in
its gate receipt; the round-56 tip's figures AND the freshness limb live only in `controls/gate-final-r56.txt` — no
freshness literal is re-typed into this cell (the DF-3 erratum discipline: the receipt is the only place the status is
asserted, and the receipt is committed in the same commit as the pair it certifies; the receipt is a true tee, so the
pair regenerated inside it already counts the receipt's own citation and the self-reference class cannot recur in this
form). Bookkeeping move only (R58 nominal labeling on C1): no citation-resolution move is claimed.

### Round-56 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 56 | depth:verifiability | 17 pinned figures; the r55 figures stood un-re-derived and no lane instrument read the census-freshness receipt's literals — the DF-3 prose-vs-receipt drift was caught by the closure judge's reading, not by any lane instrument | 27 pinned figures: the r55 state folds in rev-pinned (36/87/39/74/74) and the census literals pin machine-checkably (stale / 1118 / 3883 pre-receipt, 1119 / 3882 fixed point); the DF-3 prose AS FILED reads stale (red exit 1); selftest 5/0; green 27/0 exit 0 | `controls/c1-selftest-r56.txt`; `controls/c1-green-lane-r56.txt`; `controls/c1-red-df3-r56.txt`; `controls/do-nothing-c1-r56.txt`; `controls/df3-census-erratum.md`; `controls/df3-fixedpoint-r55tip.txt` |
| 56 | coverage | `FRONTIER-CENSUS rows=36 admitted=36 closed=6 problem-rows=30 registry=87`, `entries=39 pass=6`, zero F37 (this host, base export 531/531) | `FRONTIER-CENSUS rows=37 admitted=37 closed=7 problem-rows=30 registry=88`, `FRONTIER-PASS F37 ids=S088`, `entries=40 pass=7`, FAIL records 33 invariant | `controls/do-nothing-c2-r56.txt` -> `controls/c2-counter-final-r56.txt`; `corpus/knowledge/cisa-vulnrichment-record-list.md`; `corpus/source-snapshots/round-56/` (S088 + manifest) |
| 56 | calibration | the r55 closure's routed DF-3 standing (prose `ok` vs the receipt's printed `stale [exit=1]`; self-referential citation) | the prose superseded append-only with a runnable closure check; the root cause REPRODUCED in the fixed-point receipt (one citation flips, one regen converges, freshness ok); the machine-catching census-literal ledger entries landed with C1; the class form-banned going forward (true-tee final receipt) | `.ufo/waves/round-56/controls/df3-census-erratum.md`; `.ufo/waves/round-56/controls/df3-fixedpoint-r55tip.txt` |

**Capabilities:** the round-54 `move-log-figure-audit` row is extended in place of a new row: the capability's ledger
grows 17 → 27 (first-working round stays 54; the extension evidence is this round's green/red/selftest receipts —
recorded in this round section per the round-43/R6-append practice).

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not
active (the repertoire moved this round — the ledger grew 17 → 27 with three new receipts and a new red control).
**Non-author verification:** outstanding. No seats ran (no AgentSwarm surface on this host; routed via L0); the most
recent outside spot-check is the round-55 closure that routed the defect this round fixes. The claims verify on their
frozen predicates by re-derivable commands only.

### Planned for round 57 (not frozen)

1. **depth:verifiability (4, lowest):** the figure-audit ledger keeps growing one round at a time — fold the round-56
   figures in (rows=37, registry=88, entries=40, expected=75) rev-pinned to this round's tip, plus the natural next
   limb the census-literal entries open: a `census-fixedpoint-*-r56` pair pinned to the true-tee receipt's own printed
   figures, so the pre-/post-receipt generation discipline stays machine-checked for the round that introduced the
   form. The 30 problem-rows / 33 host-bound FAIL records, the 67 `cd /home/...` recheck lines and the limb-mutation
   replay's python3 dependency stay operator-owned (L0 kasegi round-50/46 unanswered) and must NOT be re-declared as a
   lane target.
2. **coverage (8):** the remaining recorded leads are ISO/IEC 29147/30111 (the ISO standard records), the UK AI
   Security Institute report, the Google Big Sleep reporting surface and S088's own unasserted surfaces (a one-level
   subtree walk into a year folder would pin the per-CVE record-list shape the entry explicitly leaves unasserted);
   every next frontier row clears the extended pre-freeze screen including the downstream-consumer sweep.

## Round 57 result — the figure-audit ledger 27 → 35 with the host-portable fail-entry-records derive repair (C1, depth:verifiability, nominal per R58, score held 4), and the ISO/IEC 29147/30111 standard records F38 on S089 + S090 (C2, coverage, score held 8)

Frozen claims: `.ufo/waves/round-57/claims.json` (freeze commit `6343e2c3882a96b1af86e1ecf4c9deba33361719`, base `eae1d614542e8d30d77e9f4e8b9dea6a11aad138`), landed before the implementation. Host: Linux/omp (run-15). The round-56 closure's routed DF-56-1 (the SHONEN form) is fixed in the report; DF-56-2 is operator-side and named in the report.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal capability-extension move, labelled per QUALITY R58** | C1 verifies on its frozen predicate. The figure-audit ledger grows 27 → 35 pinned figures: the r56 figures fold in rev-pinned to `8a5d7538b0caa50300b1eee88442a230d9a433f2` (frontier-rows-r56 37, registry-rows-r56 88, entries-r56 40, knowledge-expected-r56 75, knowledge-files-r56 75), the r56 true-tee receipt's literals pin (census-fresh-literal-r56 `ok`, census-internal-r56-receipt 1130, census-gone-r56-receipt 3915), and the fail-entry-records derive re-points from the live frontier counter (red on this host at base: `figures=27 ok=26 stale=1 exit=1`, `.ufo/waves/round-57/controls/do-nothing-c1-r57.txt`) to the committed receipt line `FAIL_entry_records=33` (`.ufo/waves/round-53/controls/c2-counter-final-r53.txt:8`). After: `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`; selftest `cases=5 failures=0`; red control 1 (wrong want, registry-rows-r56 87) and red control 2 (mutated r53 receipt, FAIL_entry_records=34) each `stale=1 exit=1` (`.ufo/waves/round-57/controls/c1-red-r57.txt`). |
| coverage | 8 | **8 held; delta 0** | C2 verifies on its frozen predicate: frontier F38 admitted on S089 (ISO/IEC 29147:2018 publisher record, `corpus/source-snapshots/round-57/S089.txt`, sha256 `17ee9c41…0e1dd`) and S090 (ISO/IEC 30111:2019 publisher record, `S090.txt`, sha256 `2074d3a1…6c2976a`), entry `corpus/knowledge/iso-29147-30111-standard-records.md` (four falsifiable claims with rejected over-generalizations), registry rows S089 and S090 (mined, recheck 90d). `FRONTIER-CENSUS rows=37 → 38 admitted=38 closed=38 problem-rows=0 registry=88 → 90`, `FRONTIER-PASS F38 ids=S089,S090`, `entries=40 pass=40 → 41 pass=41 exit=0`. The lead line `corpus/SOURCES.md:137` is byte-unchanged at base and tip (exact-line sha256 `23309b6f…5b39`). Score held: the coverage denominator is operator-owned (the 0/18 lost-domain surfaces); the moved measure is the frontier count. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round. |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51..56 precedents; no score asserted) | Eight round-57 mistakes (M57-1..M57-8) recorded with class, captured-by and fix (`corpus/lessons/round-57.md` § Mistakes). The host-bound derive class was measured at base before any repair and the repair is shown able to fail (red control 2). The wave's attacks found two instrument defects this round that were not in any prior record: the frozen C2 counter admits a stub body (M57-4, probe a2; R67 named open, counter amendment deferred so the frozen predicate is not changed after a probe), and two round-54 figures could not fail on a missing git object (M57-5, R30; repaired, red control `r30-hardening-r57.txt`). Entry Claim 1 anchors corrected to the lines that carry the facts (EntryClaimTable F1). |

**Attack notes (wave-1, `.ufo/waves/round-57/w1/`).** Coverage: the frozen C2 counter passes a one-line stub body that names the two ids in prose (CriticFrontier probe a2, M57-4); C2's admission rests on the frozen predicate and the non-author claim table (EntryClaimTable 53/53 rows; ReopenSources both snapshots reproduce; ScoutSources 14/14 quotes, 28/28 facts), and R67 names the counter limb open. Depth:verifiability: C1 survives its eight kill-rule clauses (ReviewDerive); the comparison limbs are load-bearing (MutateLedger m1/m2/m3/m5 killed), two survivors named open (m4, m6; M57-6); the two round-54 zero-valued derives were fail-open on a missing object and are repaired (M57-5, R68, `controls/r30-hardening-r57.txt`).

### Round-57 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 57 | depth:verifiability | figure-audit `figures=27 ok=26 stale=1 exit=1` at base (the r53 derive re-runs a live counter that reads zero FAIL lines on this host) | `figures=35 ok=35 stale=0 exit=0`; the r56 figures and literals pinned; the derive reads the committed receipt line (host-portable); two red controls (wrong want, mutated receipt) read stale exit 1 | `.ufo/waves/round-57/controls/do-nothing-c1-r57.txt`; `.ufo/waves/round-57/controls/c1-red-r57.txt`; `corpus/instruments/figure-audit-ledger.json` |
| 57 | coverage | `FRONTIER-CENSUS rows=37 admitted=37 closed=37 problem-rows=0 registry=88`, `entries=40 pass=40` (this host, base bytes) | `FRONTIER-CENSUS rows=38 admitted=38 closed=38 problem-rows=0 registry=90`, `FRONTIER-PASS F38 ids=S089,S090`, `entries=41 pass=41` | `.ufo/waves/round-57/controls/do-nothing-c2-r57.txt`; `.ufo/waves/round-57/controls/c2-standin-dryrun-r57.txt`; `corpus/knowledge/iso-29147-30111-standard-records.md`; `corpus/source-snapshots/round-57/` |
| 57 | calibration | the r56 routed DF-56-1 (SHONEN form) standing; the host-bound class unnamed as host-bound | DF-56-1 fixed in the report (`## SHONEN`); host-bound class named and repaired (R65); entry anchors corrected | `corpus/lessons/round-57.md` § Mistakes; `corpus/QUALITY.md` R65, R66 |

**Capabilities:** the `move-log-figure-audit` row (first-working round 54) is extended in place, 27 → 35 pinned figures; its first host-portable derive is this round's green run on the Linux host. No new row enters.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not active (the figure-audit repertoire moved this round).

### Planned for round 58 (not frozen)

1. **depth:verifiability (4, lowest):** fold the round-57 figures into the ledger (frontier-rows-r57 38, registry-rows-r57 90, entries-r57 41, knowledge-expected-r57 76, knowledge-files-r57 76) rev-pinned to the round-57 results tip; the host-bound live-counter derives named by the wave-1 sweep (`.ufo/waves/round-57/w1/ScoutHostBound.md`) move to committed receipts or carry an R65 host line.
2. **coverage (8):** the next frontier row clears the extended pre-freeze screen including the downstream-consumer sweep; candidate leads: the UK AI Security Institute report and the Google Big Sleep reporting surface (both unopened; lead, not row).

## Round 58 result — the figure-audit selftest pin, read-only case, committed mutant battery and the receipt-backed red fixture (C1, depth:verifiability, nominal per R58, score held 4), and frontier F39 on S091, the UK AI Security Institute autonomous cyber-capability progress rate (C2, coverage, score held 8)

Frozen claims: `.ufo/waves/round-58/claims.json` (freeze commit `543cac13886b91ac660d788ed20e64ae70ee0fa5`, base `1e5c8f2cdc1c9d14672444c6fca0e67414366494`, frozen_at 2026-11-03T20:48:48Z), landed before the implementation. Implementation `18ddb054a82a59e530ba86b2511bcfa5ecd49b6b` (after-state receipt `.ufo/waves/round-58/controls/after-r58.txt`); wave-1 corrections and evidence `1e9e4b56d6deaf05fae5f36eb5d45b2c83f36f63`; final measured commit `1e9e4b56d6deaf05fae5f36eb5d45b2c83f36f63` (`.ufo/waves/round-58/controls/after-final-r58.txt`, every value as frozen). The round-57 closure routed no score-moving defect; its carry-in DF-56-2 is resolved (see the round report).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal instrument move, labelled per QUALITY R58** | C1 verifies on its frozen predicate: the figure-audit selftest pins its own case count (`EXPECTED_CASES = 6`) and carries the new case `derive-not-read-only-refused`; the committed battery `corpus/instruments/figure-audit-mutbat.py` kills both one-limb mutants of the selftest (m4 `killed=1`, m6 `killed=1`) and leaves the equivalent-patch control held (`mutbat killed=2/2 survivors=0 controls=pass`, exit 0; base: m4 and m6 both survived with exit 0). The red fixture `red-d53-ledger.json` derives from the committed r53 receipt, so its d53-1 verdict is `derived=33 want=34 stale` on this host (base: `derived=UNAVAILABLE`, a degenerate red). Evidence: `after-r58.txt` (C1 sections); `do-nothing-c1-mutants-r58.txt` and `do-nothing-c1-r58.txt` (before). Counting command: `python3 corpus/instruments/figure-audit-mutbat.py`. |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F39 admitted on S091 (the publisher's own statements, one dated blog post), entry `corpus/knowledge/aisi-autonomous-cyber-capability-progress-rate.md`. `FRONTIER-CENSUS rows=38 → 39`, `registry=90 → 91`, `FRONTIER-PASS F39 ids=S091`, `entries=41 → 42 pass=42 exit=0`; `source-recheck --source S091` exit 0 with 9 Q-OK occurrences=1 (capture sha256 `d2ba7199…820618`). Score held: the coverage denominator is operator-owned, as in rounds 53–57; the moved measure is the frontier count. Evidence: `do-nothing-c2-r58.txt` → `after-r58.txt`. Counting command: `python3 corpus/instruments/frontier-recheck-count.py`. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was not edited this round. |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51..57 precedents; no score asserted) | Four round-58 Mistakes (M58-1..M58-4) recorded with class, captured-by and fix (`corpus/lessons/round-58.md` § Mistakes): a stale carry-in line closed by R70; a vacuous read-only case caught by the battery before the freeze; free line anchors that no counter checked (the first F39 draft cited lines one to two off), closed by R71; the export-root measurement recorded. The carry-in DF-56-2 is resolved with its count cited. |

**Capabilities:** no new row. The `move-log-figure-audit` row (first-working round 54) is extended in place: the selftest is pinned (6 cases) and a committed one-limb mutant battery is added; the battery's first demonstration is this round's `after-r58.txt` (C1 section).

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not active (the figure-audit repertoire moved this round and the capability window restarts at 54).

**Non-author verification (wave `w1`, 9 seats, lane-dispatched; results `.ufo/waves/round-58/w1-results.json`):** ScoutSources AGREE (9/9 quotes; independent re-open reproduces the capture); EntryClaimTable PASS WITH CORRECTIONS (33 rows; eight corrections applied in the correction commit); ReviewerC2 PASS (9/9 C2 counting commands reproduce from a clone; two findings applied: the lead line is at `:142` at the tip, and the S091 anchor now covers L22-L23); SiblingOverlap SCOPE CLEAR (0 sibling PROVINCE hits on the nine target tokens; kengaku holds adjacent METR time-horizon ground, reported not absorbed; the PROVINCE scope-limit wording aligned); CriticC1 SURVIVES (caveats: the count pin alone does not guard case substitution; the d53 red control is record-anchored); ExportReplay PARTIAL (14/14 values reproduce; the frontier counter's recheck lines are lane-bound by absolute path); ScoutHostBound2 PASS (0 new host dependencies); SentinelCred FINDINGS (credential scan clean; one medium: the read-only derive gate is a head allow-list that splits only on `|` and `>`; two low provenance notes); MutationC1 PARTIAL (committed battery reproduces; the instrument's selftest kills 7 of 15 one-limb mutants the seat built; eight survive, four of them turn red into green on a real ledger — M58-5, named open). The round's C1 claim is the two-limb claim it was frozen as; the survivors are not claimed as killed. The outside spot-check is the round-58 closure.

### Planned for round 59 (not frozen)

1. **depth:verifiability (4, lowest):** fold the round-58 figures into the figure-audit ledger rev-pinned to the round-58 tip (`frontier-rows-r58 39`, `registry-rows-r58 91`, `entries-r58 42`, `knowledge-expected-r58 77`, `knowledge-files-r58 77`) and add the battery to the ledger's own selftest chain. The R67 counter stub limb (M57-4; `do-nothing-r67-probe-a2-r58.txt`) and the census range-base rule (M57-9 / R69) stay open until the operator answers the kasegi round-57 L0 row; they are not re-declared as lane targets while unanswered.
2. **coverage (8):** the next frontier row must clear the extended pre-freeze screen (neighbor screen including the downstream-consumer sweep) and the anchor-referent table (R71) before the freeze; candidate lead: the Google Big Sleep reporting surface (unopened).

## Round 59 result — the derive gate refuses the frozen shell-chaining probe set P1–P8 (C1, depth:verifiability, nominal per R58, score held 4), and frontier F40 on S092, the Google Issue Tracker README for the Big Sleep findings tracker (C2, coverage, score held 8)

Frozen claims: `.ufo/waves/round-59/claims.json` (freeze commit `00b535758d2cfa4511cda7167b67cdc045b85fb4`, base `69de8d363b2193fdb37d03fd3e235bceeb1c2daa`), landed before the implementation. Implementation `472737847ff31d1255bf1a0745822a5e878e9622` (candidate `corpus/instruments/figure-audit.py` sha256 `32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0`, cmp-verified against the stand-in bytes the freeze measured). The round-58 carry-in (the figure-audit registry rows, defect 1) landed in the same commit as a non-claim. M58-5 is claimed here as C1 on its probe set; its residual is named, not claimed.

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal capability-extension move, labelled per QUALITY R58** | C1 verifies on its frozen predicate. P1–P8 on the base gate: 8 of 8 execute (`markers=1`, `.ufo/waves/round-59/controls/c1-probes-base-r59.txt`); on the landed gate: 8 of 8 refused with `exit=2 markers=0` (`controls/c1-probes-lane-after-r59.txt`); the quoted-separator control stays admitted (exit 0, derived 35); selftest `cases=6 failures=0` → `cases=14 failures=0` (`controls/c1-lane-after-r59.txt`); mutant battery `killed=2/2 survivors=0 controls=pass`; ledger `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`; the red fixture still reads stale. Named open, not claimed: B1 and B2 (backslash-escaped quotes outside quotes), B3 (sed `e`), B4 (awk `system()`), B6 (`sort -o`) execute on base and landed bytes (`controls/c1-residual-base-r59.txt`, `controls/c1-residual-lane-r59.txt`); B5 (newline continuation) is refused on the landed gate and was admitted-as-argument on base. |
| coverage | 8 | **8 held; delta 0** | C2 verifies on its frozen predicate: F40 admitted on S092 (`corpus/knowledge/google-big-sleep-findings-tracker.md`, `controls/c2-lane-after-r59.txt`): `FRONTIER-CENSUS rows=39 → 40 admitted=40 closed=40 registry=91 → 92`, `FRONTIER-PASS F40 ids=S092`, `entries=42 → 43 pass=43 exit=0`; `source-recheck --source S092` exit 0 with 10 Q-OK occurrences=1; `capture-binding records=74 → 75 bound=75 unbound=0`; knowledge 77 → 78 with expected list sorted; the lead bullet bytes unchanged (sha256 `3ed4f54d…`). Score held: the coverage denominator is operator-owned, as in rounds 53–58; the moved measure is the frontier count. |
| depth:density | 9 | 9 held; not re-measured | `SKILL.md` gained a registry section (the round-58 carry-in) and no density-relevant prose; the density instrument was not re-run this round, and no density claim is made. |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51..58 precedents; no score asserted) | Seven Mistakes rows (M59-1..M59-7) in the round-59 lesson with class, captured-by and fix. Three rows with `captured-by: none` now have criteria (R72 for M59-1 and M59-4; R73 for M59-7; R74 for M59-3). The base probe receipt found M59-1 before any claim was frozen-against-data; M59-4 was found after landing by the round's own probe and is named open, not hidden. |

**Capabilities:** new row `derive-gate-chain-refusal` (first working round 59): the figure-audit gate refuses the eight frozen shell-chaining probes; demonstration `bash .ufo/waves/round-59/controls/c1-probe-run.sh corpus/instruments/figure-audit.py <scratch>` → P1 to P8 `exit=2 markers=0` (`controls/c1-probes-lane-after-r59.txt`). Its residual classes are listed in the row's evidence, not claimed. The `move-log-figure-audit` row (first working round 54) is extended in place: the selftest 6 → 14 cases and the probe set.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not active (the derive-gate repertoire moved this round).

### Round-59 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 59 | depth:verifiability | the base derive gate admits 8 of 8 chaining probes; selftest 6 cases | the landed gate refuses 8 of 8; selftest 14 cases; residual classes B1–B4, B6 named open | `controls/c1-probes-base-r59.txt`; `controls/c1-probes-lane-after-r59.txt`; `controls/c1-lane-after-r59.txt`; `controls/c1-residual-base-r59.txt`; `controls/c1-residual-lane-r59.txt` |
| 59 | coverage | `FRONTIER-CENSUS rows=39 admitted=39 closed=39 problem-rows=0 registry=91`, `entries=42 pass=42` | `rows=40 admitted=40 closed=40 problem-rows=0 registry=92`, `FRONTIER-PASS F40 ids=S092`, `entries=43 pass=43` | `controls/do-nothing-c2-r59.txt` → `controls/c2-lane-after-r59.txt`; `corpus/knowledge/google-big-sleep-findings-tracker.md`; `corpus/source-snapshots/round-59/` |
| 59 | calibration | the r58 closure's routed defect 1 (gate registry rows) and M58-5 standing | the registry rows landed (`SKILL.md`, round-59 section); M58-5's probe set claimed as C1, residual named; M59-1..M59-7 mined | `SKILL.md` (round-59 registry addition); `corpus/lessons/round-59.md` § Mistakes; `corpus/QUALITY.md` R72–R74 |

### Planned for round 60 (not frozen)

1. **depth:verifiability (4, lowest):** an escape-aware scanner (a backslash outside quotes escapes the next character; no escapes inside single quotes) with B1 and B2 as its red-before probes, plus the in-program write classes B3, B4 and B6 (remove `sed`, `awk` and the `sort` output flag from the allow-list, or restrict them), each shown by a red-before receipt before the freeze (R72). The docstring allow-list sentence is amended in the same freeze (R74: `grep -c 'allow-list:.*head'` must become at least 1). The round-58 figures fold into the ledger (planned residue) only if it does not share claim space.
2. **coverage (8):** the next frontier row must clear the extended pre-freeze screen and the anchor-referent table (R71) before the freeze. Candidate lead, not opened: the Project Zero post comparing Fuzzilli and BigSleep (`projectzero.google/2026/10/fuzzing-v-AI.html`, surfaced by search, unread); the DeepMind Big Sleep blog remains unopened (the earlier candidate returned 404). Each is a lead, not a row, until opened.

### Wave-1 verdicts and corrections (round 59; `w1-results.json`, WAVE-DONE received; 13 seats spawned, 0 dead, 0 resumed)

- **C1 (depth:verifiability, nominal, held 4):** verifies on its frozen predicate — ReviewerC1 VERIFIED (every frozen check reproduces at `4727378`: P1–P8 refused, CTRL admitted, selftest 14/0, mutbat 2/2, ledger 35/35, red fixture stale, scope clean; `w1/ReviewerC1.md`). Not claimed and reported against it: CriticC1 DEFEATED on the security reading (N1 = `git show --output`, N2 = `..` traversal through the python head, and `git show --ext-diff` executing configured commands; `w1/CriticC1.md`); the classes are pre-existing (`controls/c1-xclass-base-r59.txt` = `controls/c1-xclass-lane-r59.txt` in effect). MutationC1 killed 6 of 13 one-limb mutants, seven survive (m2, m2b, m4, m6, m7, m8, m9; `w1/MutationC1.md`; R17 names them open). FuzzDerive: H holds on its bounded sample (68 admitted, 0 marker creations) and is falsified as a universal claim by 28 of 28 targeted B1/B2 derives (`w1/FuzzDerive.md`). ExecCounters MISMATCH, counter-side: frozen counting command 1 with a relative instrument path cannot run literally (M59-11, R77); the measured receipts used the absolute path.
- **C2 (coverage, held 8):** verifies — ReviewerC2 VERIFIED in a fresh clone; ScoutS092 AGREE 10/10 (independent re-open, parsed structure identical); EntryClaimTable PASS WITH CORRECTIONS (27 rows: 23 GROUNDED, 3 OVERREACH, 1 UNGROUNDED), corrections C-1, C-3, C-4, C-5 and the component attribution applied in the entry (`e694478`); C-2 (eleventh pinned quote) deferred because the frozen assertion count is ten; the counters re-run on the corrected bytes (`controls/c2-lane-after-correction-r59.txt`: frontier `rows=40 … registry=92`, `FRONTIER-PASS F40 ids=S092`, `entries=43 pass=43`, recheck Q-OK, binding `75/75`, census exit 0).
- **Non-author checks of the round's other surfaces:** SiblingOverlap SCOPE CLEAR (R1 = C-5); ScoutHostBound PASS; ExecAnchors REFERENTS-HOLD; ExecDiffScope IN-SCOPE; SentinelCred FINDINGS with 0 critical, 0 high, 0 medium, 2 low, 5 info, no credential material (both LOW items KEEP).
- **Registry text corrected:** the figure-audit row no longer says "writes nothing in the lane"; it states the derives are not sandboxed and names the residual classes (`SKILL.md` round-59 section, `e694478`).
- **Score:** depth:verifiability 4 held (nominal); coverage 8 held. No axis harmed: the residual classes are pre-existing on base (`controls/c1-xclass-base-r59.txt`).
- **Trend verdicts:** expansion **improved** (F40 admitted on uncovered ground, a new source kind: the tracker's machine interface); quality **unchanged** (no admitted entry superseded or failing its recheck; the entry corrections were made before the count, recorded as corrections, not as quality gains); discernment **improved** (the non-author claim table found three overreaches and one ungrounded sentence in an admitted entry; the disagreement became corrections and criterion R76).
- **Open, named, and escalated:** the derive gate's security boundary (L0 question, kasegi round-59 row); the seven MutationC1 survivors; the counter defect M59-11; the R67 and R69 operator decisions (re-asked).

## Round 60 result — the figure-audit derive gate becomes escape-aware and refuses the in-program/write-flag classes Q1–Q7 (C1, depth:verifiability, nominal per QUALITY R58, held 4), and frontier F41 on S093, Project Zero's own Fuzzilli-vs-BigSleep comparison (C2, coverage, held 8)

Frozen claims: `.ufo/waves/round-60/claims.json` (freeze commit `66e6241cd7afd6184273ce7df1dcd5328c187367`, base `cdeea55bea09ed08765d3c3d3a56f23db44e66f4`, frozen_at 2026-11-04T13:34:58Z), landed before the implementation, with the mid-round erratum `.ufo/waves/round-60/claims-erratum-1.md` (C2 counting command 8 want 1 → 2; R78). Implementation `7f7dd267283d2a16ca38d4cb05bed92165cb35cd`; the instrument and ledger bytes are cmp-verified from the stand-in (`controls/freeze-digests-r60.txt`).

| Axis | Before | After | Verdict and evidence |
|---|---:|---:|---|
| depth:verifiability | 4 | **4 held; delta 0 — nominal instrument move, labelled per QUALITY R58** | C1 verifies on its frozen predicate. Base: Q1–Q6 each execute (`markers=1`), Q7 is admitted and run (`controls/c1-probes-base-r60.txt`); selftest `cases=14`; docstring limb 0. Landed: Q1–Q7 each `exit=2 markers=0` with `reason=derive-not-read-only`, CTRL-quoted-semicolon `exit=0 derived=35`, CTRL-plain-count `exit=0 derived=1`, the python-traversal residual still admitted (`controls/c1-lane-after-r60.txt`); selftest `cases=20 failures=0`; mutbat `killed=2/2 survivors=0 controls=pass`; ledger `figures=35 ok=35 stale=0 exit=0` after five awk derives were re-expressed in allow-listed heads (`cut`/`tr`/`wc`, `grep`/`wc`); red fixture `stale`; docstring limb **0 → 1** (R74); digests `35f7bcd3…` / `28ad7fef…`. The probe runner resolves the instrument absolute before its per-probe `cd` (R77). |
| coverage | 8 | **8 held; delta 0** | C2 verifies: frontier F41 admitted on S093 (Project Zero's own dated Fuzzilli-vs-BigSleep comparison, capture `corpus/source-snapshots/round-60/S093.txt`, 15 pinned quotes, manifest `…/round-60/manifest.json`), entry `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md`, registry row S093. `FRONTIER-CENSUS rows=40 → 41 admitted=41 closed=41 problem-rows=0 registry=92 → 93`, `FRONTIER-PASS F41 ids=S093`, `entries=43 → 44 pass=44 exit=0`; `source-recheck --source S093` exit 0 with 15 Q-OK lines; `capture-binding records=75 → 76 bound=76 unbound=0`; knowledge `78 → 79` = expected 79, `LC_ALL=C sort -c` exit 0; the stale SOURCES lead bullet corrected (sha `3ed4f54d…` → `6a67537e…`). Score held: the coverage denominator is operator-owned, as in rounds 53–59; the moved measure is the frontier count. |
| depth:density | 9 | 9 held; non-target guard | `SKILL.md` was edited only as factual registry cells (the selftest pin 14 → 20 and the write-scope sentence naming the Q1–Q7 classes and the open residuals). The density instrument was not re-run and no density claim is made. |
| calibration | verdict-only (not a scored owned axis) | improved (verdict row per the round-51..59 precedents; no score asserted) | Seven Mistakes rows (M60-1..M60-7) in `corpus/lessons/round-60.md` with class, captured-by and fix; three criteria added (R78 want measured, R79 write-class probe environment, R80 screen order). The round-59 closure's ten routed defects are addressed in this round's records (capability row, stale calibration counts, quote-count misstatement, SHONEN reconciliation, census durability, lead bullet, Gate wording, pointer accuracy, receipt header label, counting-command literal-runnability). |

**Round-59 calibration-row correction (append-only; the round-59 closure's routed defect 3).** The filed round-59 calibration cell says "Seven Mistakes rows (M59-1..M59-7)" and "Three rows with `captured-by: none`" while listing four criteria. At the round-59 tip the lesson carries **eleven** Mistakes rows (M59-1..M59-11), and **eight** of them carry `captured-by: none` (M59-1, M59-3, M59-4, M59-7, M59-8, M59-9, M59-10, M59-11), covered by six criteria (R72, R74, R73, R75 ×2, R76, R77). The round-59 row's text is not rewritten; this entry is the correction of record.

**Round-59 Gate quote-count correction (append-only; the round-59 closure's routed defect 4).** The round-59 Gate block and report say "maximum 11 words"; the round-59 maximum is **12** words by `wc -w` (Q3, "All issues reported by the project so far can be found [here](https://goo.gle/bigsleep)"). The ≤25-word rule held then and holds now (round-60 maximum: 25, Q13).

### Round-60 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 60 | depth:verifiability | Q1–Q7 probe classes: escaped single/double quote (Q1/Q2), `sed` in-program `e` (Q3), `awk system()` (Q4), `sort -o` (Q5), `git show --output` (Q6) and `--ext-diff` (Q7) execute or are admitted on the base gate; selftest 14; docstring limb 0 | Q1–Q7 refused (`exit=2 markers=0`), both controls admitted, selftest 20/0, mutbat 2/2, ledger 35/35, red fixture stale, docstring limb 1, digests frozen | `.ufo/waves/round-60/controls/c1-probes-base-r60.txt`; `controls/c1-lane-after-r60.txt`; `corpus/instruments/figure-audit.py`; `corpus/instruments/figure-audit-ledger.json` |
| 60 | coverage | `FRONTIER-CENSUS rows=40 admitted=40 closed=40 problem-rows=0 registry=92`, `entries=43 pass=43`; knowledge 78; binding 75; F41 absent | `rows=41 admitted=41 closed=41 problem-rows=0 registry=93`, `FRONTIER-PASS F41 ids=S093`, `entries=44 pass=44`; knowledge 79; binding 76; lead bullet corrected | `.ufo/waves/round-60/controls/do-nothing-c2-r60.txt` → `controls/c2-lane-after-r60.txt`; `corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md`; `corpus/source-snapshots/round-60/` |
| 60 | calibration | round-59's ten routed defects; three of them process/counter classes with no criterion | ten routed defects addressed in the round's records; R78–R80 land with M60-1/M60-3/M60-6; the round's own erratum supersedes a hand-typed want | `corpus/lessons/round-60.md` § Mistakes; `corpus/QUALITY.md` R78–R80; `.ufo/waves/round-60/claims-erratum-1.md` |

**Capabilities:** the round-59 announcement is formalized as a table row (the round-59 closure's routed defect 2), and the `move-log-figure-audit` row is extended in place:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| derive-gate-chain-refusal | The figure-audit derive gate refuses shell-chaining (r59) AND the escaped-quote, in-program (`sed`/`awk` heads removed) and write-flag (`sort -o`, `git show --output/--ext-diff`) classes Q1–Q7, with an escape-aware quote model and two admitted controls; its selftest pins 20 cases and its mutant battery holds 2/2 with an equivalent-patch control | `bash .ufo/waves/round-60/controls/c1-probe-run-r60.sh corpus/instruments/figure-audit.py <scratch>` → Q1–Q7 `exit=2 markers=0`; `c1-lane-after-r60.txt` for the selftest/mutbat/ledger; residual classes named open (python-head traversal; unscreened other heads; counters can write; `$'…'`/`#` unclaimed) | 59 |
| move-log-figure-audit | Re-derives the lane's figure ledger against committed bytes, whole-value, fail-closed; round 60 extends it: selftest 14 → 20 cases, five ledger derives re-expressed in allow-listed heads so removing `awk`/`sed` keeps the ledger green | `python corpus/instruments/figure-audit.py` → `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0` (`controls/c1-lane-after-r60.txt`); selftest `cases=20 failures=0`; mutbat `killed=2/2` | 54 |

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability (4); the nudge is not active (the derive-gate repertoire moved this round: two new capability rows in effect).

### Planned for round 61 (not frozen)

1. **depth:verifiability (4, lowest):** close the residual classes the round-60 claim names instead of re-claiming the same probes: (a) confine the `python3` head so a `..` traversal out of `corpus/instruments/` is refused (red-before probe: the RESIDUAL-python-traversal derive), (b) extend the write-flag screen to every allow-listed head or drop the remaining heads that admit a write flag, and (c) the operator's sandbox decision from the kasegi round-59 L0 row (the gate is not a sandbox) — none of these is a lane target until the L0 row is answered where it needs an operator ruling. The round-59/r60 figures fold into the ledger only if it does not share claim space.
2. **coverage (8):** the SOURCES `Leads (unopened)` section is stale — several listed leads are now admitted rows (ISO records → S089/S090, AISI → S091, GitHub advisories REST API → S087, CISA ADP list → S088); the next round should re-derive the lead list from the registry and open one genuinely unopened candidate (the Project Zero 2024 "From Naptime to Big Sleep" post linked by S093, or the Fuzzilli project's own documentation), clearing the extended pre-freeze screen (R80: its receipt before the freeze) and the anchor-referent table (R71).

### Round-60 wave-1 outcome (13 seats, one v1 wave, 0 dead)

| seat | role | verdict | effect on the round |
|---|---|---|---|
| ScoutS093 | scout | AGREE (independent conversion byte-identical, 15/15 quotes) | confirms the Gate |
| ScoutHostBound | scout | FAIL (H1–H5 in the round's harness; H6 carried) | M60-10, R82; selftest value named host-conditional |
| EntryClaimTable | scribe | PASS (29/29 GROUNDED, quotes ≤ 25 words) | none |
| SiblingOverlap | connector | SCOPE CLEAR + one boundary recommendation | the entry's Limits bullet appended; counters re-run |
| ReviewerC2 | reviewer | VERIFIED (all nine C2 commands reproduce) | none |
| ReviewerC1 | reviewer | VERIFIED on the frozen checks; F1 MAJOR token-spelling screen bypass, F2 wording, F3–F5 | M60-9; SKILL r60 correction; F5 closed with the committed-tree receipt |
| CriticC1 | critic | DEFEATED on the security reading (24 admitted, 9 green, none Q1–Q7) | named open, escalated on L0; frozen predicate intact |
| MutationC1 | mutation-tester | killed 5/13 one-limb mutants; 8 survived | named open (R17) |
| ExecCounters | executor | ALL-MATCH (17 commands, erratum applied) | none |
| ExecAnchors | executor | REFERENTS-HOLD | none |
| ExecDiffScope | executor | OUT-OF-SCOPE relative to the item premise | M60-8 (item text defect) |
| SentinelCred | sentinel | CLEAN | none |
| ExecEscapes | executor | 43 derives: 14 admitted-and-executing (2 green), 10 safe, 19 refused | M60-9; base-vs-candidate receipt |

**Wave-1 non-claim findings (reported, not claimed):** the write-flag screen is token-literal (quoted/clustered/abbreviated/ANSI-C spellings and `sort --compress-program` admitted; `#'` comment-phantom writes with a green audit); 24 write/execute derives admitted, 9 green; no regression against base (`controls/c1-xclass-base-cand-r60.txt`); the new runner is host-bound and not fail-closed, and the selftest's `cases=20` is host-conditional; 8 of 13 one-limb mutants survive the selftest. None of these changes a frozen value; the escalations are the kasegi round-60 L0 line and the round-61 plan. **Trend verdicts:** expansion improved; quality unchanged; discernment improved (the wave's non-author seats found the screen's incompleteness and the harness defects, and the connector's recommendation was applied rather than filed unread).

## Round 61 — measured moves (frozen C1/C2, implementation 13c8060b343e002339ffd72da37ff74514f82765)

Freeze `6f88f3a7f6b9689b49241e3f4a8e551c57a3f766`, base `c33d24ddd11abf1ebdea0dccf7327e9069dd9104`; predicate/counter/kill rules `.ufo/waves/round-61/claims.json`.

| Axis | Before | After | Score delta and evidence |
|---|---|---|---|
| depth:verifiability (lowest) | P1/P2/P3 each execute, markers=1; selftest 20; mutbat 2/2 | P1/P2/P3 each exit=2 markers=0; P4 stays refused; P5/P6 and two regression controls pass; selftest 24/0; mutbat 3/3; ledger35/35; red fixture stale | 4 → 4, delta 0, nominal per R58: figure gate does not feed citation-resolution metric. `bash .ufo/waves/round-61/controls/c1-probe-run-r61.sh corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r61/verify/probes`; other commands in claims.json. Base/stand-in receipts under controls/, measured implementation 13c8060b. |
| coverage | frontier rows41 registry93 entries44 capture76; F42 absent | frontier rows42 registry94 entries45 capture77; F42/S094 admitted; seven pinned quotes pass | 8 → 8, delta 0. `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `.ufo/waves/round-61/controls/c2-standin-r61.txt`; sourced case at corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md, implementation 13c8060b. |
| depth:density | 9 | 9 held | Not targeted or re-measured; SKILL changes are registry facts and an appended historical-pointer correction. |

**Round-60 correction (D1/D8, append-only).** The r60 lesson/LOG/SCORECARD incorrectly said R79/R80 landed: actual rows were R78/R81/R82. R79/R80 land in round 61, with R83 checking actual criterion rows (`controls/carry-in-r61.txt`: base0/0 → after1/1). The r60 statement “two new capability rows in effect” meant ONE new row and ONE existing-row extension. No new capability acquisition is claimed in round 61; C1 extends the existing derive-gate behavior. Current selftest is host-conditional (bare python required), and shell expansion/write-flag residuals remain open.

**Saturation:** 9/10; stagnation window unchanged. Lowest non-retired axis remains depth:verifiability 4; this round works it directly. No score increase or nudge waiver asserted.

### Round-61 settled wave and verdict

WAVE-DONE received; `.ufo/waves/round-61/w1-results.json`, 11 seats in one v1 wave,8 evidence-producing and3 errored/no-output (last recorded401 authentication error; terminal proc statuses unavailable; `seat-error-telemetry.json`). No replacements or residual task call. ReviewC1 and ReviewC2 reproduce both frozen predicates; ExecAnchors holds21 references; ExecRegression's192 comparisons find0 new admissions. C1 verified, C2 verified as lane recommendations; non-author closure still owns admission. Full consumer/sibling screen and sentence table were late safety nets, explicitly recorded process misses, not retroactive prefreeze passes.

Expansion improved (F42 dated SQLite case on S094); quality unchanged; discernment improved via the round-60 outside D1 finding becoming R83 and restored R79/R80. M61-1..M61-10, limitations and exact seat errors are in corpus/lessons/round-61.md. Selftest remains host-conditional. CriticPython's11 encoded-path escapes and two valid MutationPython survivors remain named open; the HarnessAttack collector failures are not fixed by interpreting exit0 as pass.

### Planned for round 62 (not frozen)

1. depth:verifiability (4, lowest): before declaring broader confinement, choose an execution model that validates the same argv it runs; re-measure the quoted-path traversal and valid boundary/prefix mutants against do-nothing controls. Correct the gate's known overbroad docstring before its next digest freeze. Repair the new runner's instrument-under-scratch/dependency masking under a new pre-data predicate, not by changing round61 evidence.
2. coverage (8): screen a genuinely unopened source that directly serves finding review/claim packaging. Fuzzilli documentation remains a lead requiring province/sibling adjudication, not an automatic next admission. Resolve extended-screen/claim-table order before freezing; no extra row quota or score increase is assumed.

**Measured commit (post-wave):** `c819159ad7baec5b9d194f13d9ae81fde38ceddc`. Commands in claims.json re-run once by L1 after WAVE-DONE; `controls/final-verification-r61.txt` reproduces C1 P1–P3 refusal, 24/0, 3/3,35/35 and red stale; C2 rows42/registry94/entries45/capture77/seven quotes/census0. This receipt is evidence only; scores remain4/8 and no new capability row is claimed.

## Round 62 — same-argv execution and CERT/CC responsibility matrix

Frozen claims: `.ufo/waves/round-62/claims.json`, freeze ee6abb037323d849c2a3b6cf6e4d0f52982b1121; base f7dcab84b104ccc03083fa1ad8c38e12830d25c9. Measured implementation: **240f1a44842ea3b0e17129c851b03c07615db518**. The committed-input run is `.ufo/waves/round-62/controls/final-verification-r62.txt`, using a selected git-archive export over a shared clone checked out at the same revision; .git supplies historical pinned objects. Safe extraction refused an inherited round25 fixture symlink in a full archive, so only declared claim surfaces were overlaid. No unsafe extraction or live production fixture mutation was used.

| Axis | Before | After | Score delta, command and evidence |
|---|---|---|---|
| depth:verifiability, lowest | Final named collector on base:10 probes/1 failure exit1, quoted traversal executes markers1; final battery3/5 with two survivors; selftest24/0; ledger35/35 | Named collector10/0; selftest35/0; battery5/5 survivors0 invalid0 controls pass; ledger35/35; red fixture stale exit1; six collector-error controls pass, always-clean counterfeit rejected | **4 →4, delta0, nominal per R58**. Citation-resolution metric is not moved. Commands: `python3 .ufo/waves/round-62/controls/c1-probe-run-r62.py corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r62/verify/probes --mode candidate`; `python3 corpus/instruments/figure-audit.py --selftest`; `python3 corpus/instruments/figure-audit-mutbat.py`; fault-suite command in claims.json. Before receipts c1-do-nothing-*-r62.txt; final committed-run receipt reproduces exact wants and all four digests. |
| coverage | Frontier42, registry94, entries45/45, capture77/77, knowledge80; F43 absent | Frontier43 admitted43 closed43 problem-rows0 registry95, F43/S095 passes; entries46/46, capture78/78,19 anchored assertions pass, knowledge81 expected81 sorted; census0 | **8 →8, delta0**. `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-62/manifest.json --source S095`; `python3 corpus/instruments/capture-binding-check.py`. Before: w1/CounterBase/baseline-receipt.txt. After: final-verification-r62.txt. New ground is CERT/CC's phase-to-five-role attribution, particularly Reporter fix confirmation versus Vendor/Coordinator report validation; generic lifecycle vocabulary is not claimed new. |
| depth:density |9|9 held| Not targeted or re-measured. SKILL changes are two same-line registry factual cells and an appended current-execution correction; no density credit asserted. |

No new capability row, retirement, split, threshold or saturation waiver. Existing figure-audit and derive-gate capabilities are extended, not new acquisitions. Saturation line9/10 remains; lowest non-retired axis depth:verifiability4 was worked nominally. Distance to next score: `python3 corpus/instruments/score-gap.py` on measured commit prints **22 of81 rechecks still gated on a lost base; score5 needs0 gated unsupported claims** (final receipt); this round does not restore those sources.

One settled v1 predata build-and-falsify wave,10 seats; nine evidence-producing, one empty output, no replacement/residual call. ReviewDesign supplies static same-plan source evidence; ScoutS095 independently reproduces the source capture; EntryDraft supplies pre-count sentence table; ScopeConnect narrows novelty before freeze. Frozen predicates were not changed after freezing. No outside discernment/promotion verdict is self-certified.

The exact decoded plan is validated once and executed directly. Quoted legitimate inside-script paths are intentionally newly admitted; there is no universal zero-new-admission claim. Allowed counters, unscreened flags, PATH/configuration, races, upstream pipeline masking and descendant effects remain outside the guarantee. R67 body-substance and R69 census-range-base operator decisions remain open; the new F43 entry rests on source/sentence/role-column review, not structural counters alone.

### Planned after round62 (not frozen)

1. Lowest depth:verifiability remains4. Any further gate claim must select a distinct observed residual with a do-nothing control; a finite option test is not a sandbox. Source restoration and operator-owned decisions are not assumed.
2. Coverage remains8. Before opening another guide subpage, distinguish specific report-package fields or responsibility rules from F43's matrix and held S018/S023; preserve full source/consumer/sibling screening and sentence-table order. No row quota or score increase is promised.

## Round 63 — finite upstream repair; frozen committed-input claim NOT VERIFIED

One frozen claim C1, depth:verifiability (lowest), nominal4 held under R58. Freeze `d690b92a4834d3a51ba86498d9eb6243f00203db`; base `fdccc6da803965234c1eff5a0fee38b97e6621c1`; measured implementation `ff28e544adc228841a8706c5e72f4de3366391cd`. Predicate/counter/kill rule and exact candidate hashes remain unchanged in `.ufo/waves/round-63/claims.json`.

| Axis | Before | After | Verdict / score delta / measurement |
|---|---|---|---|
| depth:verifiability | Candidate-mode collector on exact base: probes8/failures3/exit1; selftest35/0 | Collector8/0, trees8/0, selftest43/0, old battery5/5, new battery7/7 with2 equivalent controls and1 intentionally invalid control, disclosed SQLite qualification trial4/4. BUT frozen selected export omits four local historical-receipt dependencies: real ledger26/35, stale9, VERIFY measurements7/failures1 | **C1 NOT VERIFIED under its own committed-input kill rule; honest stop, 4→4 delta0.** `python3 .ufo/waves/round-63/controls/verify-r63.py --revision ff28e544adc228841a8706c5e72f4de3366391cd --work /fast/scratch/hyaku/kasegi-r63/L1/committed`; raw receipt `controls/final-verification-r63.txt` exit1. Positive local-ledger35/35 prefreeze does not overrule the frozen export failure. |
| coverage |8|8 held| No coverage claim. Registry95→96 is own-work curation only (S096, lesson consumer); frontier43 and knowledge81 unchanged. |
| depth:density |9|9 held| Not targeted or re-measured. SKILL changes are factual registry cells plus bounded execution amendment, not density credit. |

The finite eight-probe candidate-mode collector changes failures=3 to failures=0: grep invalid-regex exit2, missing Git ref exit128, and confined Python exit7 upstream of wc each become stale with their exact derive-upstream-exit-N reason; cat-missing exit1 and grep-no-match exit1 remain green, successful count and && concatenation remain green, final-stage exit1 remains stale. That finite result is observed, but the full claim includes the failed committed-input guard; it is not graded verified by narrowing to the green subset. Final code is byte-identical to frozen candidate15bcb6c4. Operator decisions and broader residuals remain open; no sandbox/pipefail/all-error/source-resolution claim.

The frozen driver is preserved. `controls/verify-r63-supplemental.py` adds only the four missing committed receipt inputs as an explicit NONCLAIM collector correction; it cannot retroactively satisfy the frozen counter or reverse this honest-stop grade. Lesson M63-7 captures the missing-closure mistake; R34/R65/R82 already cover it.

No capability acquisition, score movement, retirement, split or stagnation waiver. Saturation9/10 retained; lowest verifiability4 worked nominally. No new knowledge or frontier admission. Proposal2 from considerthese remains partially landed/domain-task-open; documentation-only review is not the six-file task.

### Planned after round63 (not frozen)

Work the actual lowest metric or choose a distinct observed residual with a failing do-nothing control; do not re-claim the same three repairs. Before any successor freeze, trial the exact committed-input driver with its complete transitive local input closure. Do not infer a passed full export from a successful live-root ledger.

Round63 supplemental result (nonclaim): complete-input replay on `204a627b32671b6e5e1ee682acbe31714c6d46eb` prints7 measurements/0 failures, ledger35/35; `.ufo/waves/round-63/controls/supplemental-verification-r63.txt`. **C1 remains NOT VERIFIED** because its frozen selected-export driver remains7/1. One9-seat v1 wave settled, WAVE-DONE received; no dead seat recorded, no replacement/residual call. Outside admission belongs to subsequent closure.

## Round 64 — finite command-aware upstream failure diagnosis

One sourced claim C1, lowest depth:verifiability, nominal4 held under R58. Base `d74be00a82c8c2962a0b78442c5daea3af0adaae`; frozen record `.ufo/waves/round-64/claims.json`, freeze `5b3cecbe162361b88445948e7f5ddc0c7064d6a6`; measured implementation **a55a7b254f338a9ff4a1f463441f84437d5a3fff**. All prefreeze controls were committed first; the final exact committed driver trial at7f8c633a reads8/3 on base production and8/0 with the candidate overlay, receipts landed9c7ab165 before freeze.

Frozen predicate: On the enumerated committed-input driver, VERIFY measurements=8 failures=0 and exit0; its finite18-probe collector changes7 mismatched records at base to0, representing six non-grep exit1 repairs plus their aggregate trailer, with all enumerated regression, paired-base, selfcheck, mutation/tree, forgery and ledger expectations preserved.

| Axis | Before | After | Score delta, command and evidence |
|---|---|---|---|
| depth:verifiability (lowest) | Final driver8 measurements/3 failures exit1; collector18/7 under candidate expectations; selftest43 | Frozen final driver8/0 exit0; collector18/0; paired exact base18/7 rc1; selfcheck9/0; selftest59/0; retained battery5/5; new12/12 mutants killed (3 per four limbs),21/21 tree probes,2 equivalents/1 control held/2 invalid controls rejected;30/30 counter attacks with honest positives; ledger35/35 | **4→4, delta0, nominal R58.** `python3 -B .ufo/waves/round-64/verify-r64.py --revision a55a7b254f338a9ff4a1f463441f84437d5a3fff --work /fast/scratch/hyaku/kasegi-r64/L1/final --final`. Before/after raw receipts `controls/driver-final-donothing-prefreeze-r64.txt` and `controls/final-verification-r64.txt`; full paths under round64. **C1 verified on its frozen predicate**, no narrowed subset. |
| coverage |8|8 held| No new knowledge/frontier/capability; own-work S097 is curation only, registry96→97. Existing96 rows byte-identical (`controls/source-census-summary-r64.txt`). |
| depth:density |9|9 held| Not targeted or remeasured. SKILL registry facts/current-execution amendment only; no density credit. |

Six repairs are cat missing, partial cat, cut, head, tail and sha256sum missing; ls/sort missing exit2 were already stale and remain regressions. The collector's seventh mismatch is their aggregate trailer, not another repair. Command identity preserves grep no-match1; negative upstream statuses remain ignored, including pre-existing SIGKILL partial-output false green. Final-stage precedence unchanged. No sandbox, authenticity, arbitrary-emulator, source-restoration or score5 claim.

The old figure-audit/derive-gate capabilities are extended; **no new capability row**. Saturation9/10 and stagnation window unchanged; no retirement/split/waiver. Actual metric gap remains22/81 lost-base-gated rechecks. Connector additionally records9 foreign-cwd recheck failures at base; no unclaimed knowledge rewrite or silent repair.

One v1 wave,9 settled current seats,3/9 attack,1 connector, L1 planner; WAVE-DONE received before report. Orchestrator mistakenly cancelled an earlier9 and respawned the unchanged handoff once; those partials are not evidence, not provider failures or lane-requested replacements. `w1-results.json`, lesson and raw final-byte transcripts distinguish early summaries from final8d92eaa0 candidate.

S097 own-work/A grounds local diagnosis; source date and located quotes are inside lesson Gate. Registry96→97 (A86→87, B5/C5 unchanged), mined78→79/rejected18 unchanged; census0 before/after. Domain review corrected from11 including4 unsupported arithmetic checks to7 actual source qualifications; no six-file package or SHONEN box2 credit. R63 remains NOT VERIFIED on its original driver.

### Planned after round64 (not frozen)

Depth:verifiability4 remains lowest. Do not repeat the six exit1 cases or claim source recovery from this runner. Source restoration/operator-owned R67/R69 and province decisions remain open. Any next gate claim must select a distinct observed residual, retain positive controls, reject relevant forgeries, and trial its exact complete committed-input driver before freeze. Coverage8 and density9 are held, not promises of next-round gains.

## Round 65 — signal-fail-closed derive gate (C1, depth:verifiability, nominal 4 held) and F44, the FIRST PSIRT services catalogue (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-65/claims.json` (freeze `57cb8dec1cd3a688b0f8a23f5b6b434656592577`, base `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`, driver `533a6d4f…`); counter erratum `.ufo/waves/round-65/claims-erratum-1.md` (commit `a333d8ef7183a9d8bb969c6ec5c29b8db01f7481`, driver `5aa842ab…`); measured implementation **`1c36d724c91cdd8585219798ea7cf60bb4f24b5b`** (candidate sha256 `86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef`, cmp-pinned in the driver's `input_sha256`).

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | `VERIFY measurements=8 failures=3` exit1 at base; the base gate reads SIGTERM/SIGKILL upstream producers `ok` (`selftest case=upstream-python-signal-ignored exit=0`; `P1/P2 audit_exit=0`); final-stage signal prints `derive-exit--15`; selftest 59/0; ledger 35/35 | `VERIFY measurements=8 failures=0` exit0 at `1c36d724`; `P1/P2/P3` stale with `derive-upstream-signal-15`, `derive-upstream-signal-9`, `derive-signal-15`; SIGPIPE-non-final, clean pipeline and grep-no-match positives stay ok; selftest 63/0; mutbat `killed=4/4 survivors=0 equivalents_held=2 controls_held=1 invalid_rejected=1`; ledger 35/35; collector selfcheck `failures=6` | **4 → 4, delta 0, nominal per R58** (citation-resolution metric not moved). `python3 -B .ufo/waves/round-65/verify-r65.py --revision 1c36d724… --work /fast/scratch/hyaku/kasegi-r65/L1/final --final`; before/after receipts `controls/driver-base-donothing-finaldrv-r65.txt` (8/3 exit1) and `controls/final-verification-r65.txt` (8/0 exit0); partial-output control `controls/partial-output-truncation-r65.txt` (base `ok`, landed `derive-upstream-signal-9 stale`). |
| coverage | `FRONTIER-CENSUS rows=43 admitted=43 closed=43 problem-rows=0 registry=97`; `entries=46 pass=46`; capture `records=78 bound=78 unbound=0`; expected 83 lines / 81 paths; knowledge 81; S098 absent | `rows=44 admitted=44 closed=44 problem-rows=0 registry=98`; `FRONTIER-PASS F44 ids=S098`; `entries=47 pass=47`; `records=79 bound=79 unbound=0`; expected 84 lines / 82 paths; knowledge 82; census exit 0 | **8 → 8, delta 0.** `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-65/manifest.json --source S098` (18 Q-OK); `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` exit 0. New ground: the receiving team's service catalogue — intake with advertised contacts and readiness, qualification through documented quality gates/bug bars with CVSS as an input, the established-finder bypass, reproduction as validation in an isolated environment, disclosure audiences. |
| depth:density | 9 | 9 held | Not targeted or re-measured. SKILL changes are one registry row's factual cells (selftest 59→63, signal semantics) plus a current-execution amendment; no density credit asserted. |

**Residuals named, not claimed:** direct child stages only (grandchildren, shell wrappers, PATH-shadowed binaries, exit-0 wrappers printing partial output are out of scope); SIGPIPE non-final stays benign by documented rule; the gate is not pipefail, not a sandbox, not an authenticity check; the seat-emulator finding (M65-5) shows the documented probe set alone cannot reject a semantic emulator; and the SIGPIPE exemption can mask a later operand's error (`cat big.txt missing.txt | head -n 1` reads green while `cat missing.txt | wc -l` is stale — M65-7, `w1/CriticC1.md` § H1, named open with its round-66 candidate). Source restoration and the operator-owned R67/R69 decisions remain open; the metric gap stays 22 of 82 lost-base-gated rechecks.

**Capabilities:** no new row. The existing `derive-gate-chain-refusal` row is extended in place — the gate now also refuses signal-terminated stages with named reasons while keeping the documented SIGPIPE exception; demonstration `python3 -B .ufo/waves/round-65/verify-r65.py --revision 1c36d724… --final` → 8/0.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round; the nudge is not active (the derive-gate repertoire moved again). No retirement or split.

### Round-65 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 65 | depth:verifiability | signal-killed upstream stages read `ok` (SIGTERM/SIGKILL), final-stage signal labelled `derive-exit--15`; selftest 59 | signal stages stale with `derive-upstream-signal-N` / `derive-signal-N`; SIGPIPE non-final benign by documented rule; selftest 63; mutbat 4/4 | `.ufo/waves/round-65/controls/driver-base-donothing-finaldrv-r65.txt`; `controls/final-verification-r65.txt`; `corpus/instruments/figure-audit.py` |
| 65 | coverage | frontier 43 / registry 97 / entries 46 / capture 78 / knowledge 81; F44 absent | frontier 44 / registry 98 / entries 47 / capture 79 / knowledge 82; F44/S098 admitted; 18 anchored quotes | `.ufo/waves/round-65/controls/base-counters-r65.txt` → `controls/final-verification-r65.txt`; `corpus/knowledge/first-psirt-services-framework.md`; `corpus/source-snapshots/round-65/` |
| 65 | calibration | r64 closure routed five lane defects; M65-1..M65-6 found in-round | all five addressed (lesson § Carry-in); R84–R87 land in QUALITY; two driver defects became erratum 1 before the final run | `corpus/lessons/round-65.md`; `corpus/QUALITY.md` (R84–R87); `.ufo/waves/round-65/claims-erratum-1.md` |

### Planned after round 65 (not frozen)

1. **depth:verifiability (4, lowest):** the next gate claim must select a distinct observed residual with a failing do-nothing control — candidates: the SIGPIPE single-input-operand restriction that closes H1 (M65-7), a held-out probe pair standardised into the probe collector (M65-5), or the exit-0-wrapper partial-output class. Do not re-claim the signal cases.
2. **coverage (8):** before opening another FIRST document, distinguish its ground from F44's service catalogue; the Fuzzilli primary docs and the OpenSSF aggregate-score/API portion remain unopened leads. The extended pre-freeze screen and anchor-referent table run before the freeze (R80).

## Round66 frozen plan — one sourced finite C1

C1, lowest depth:verifiability4, nominal R58; score4→4 delta0 because source-availability/citation-resolution metric is unchanged. Source S099; `.ufo/waves/round-66/claims.json`. Predicate: **VERIFY measurements=12 failures=0 and process exit0 on the exact committed-input counter.**

Base b6db9e818d322726e39cb441f2179d34d4170275 with controls0d5aef2f40dce3129e91419c34b6c46087089b94:12 measurements/3 failures exit1 (`controls/driver-base-final-prefreeze.txt`); stand-in candidate51f299af:12/0 exit0; ID-keyed no-work forgery12/6 exit1, all committed before this freeze. Exact driver5962b7d6f7aa05d118a86387ffb527f1c5dfb6b3e7b18483d99fa7eeb1adad61, collector d788bbc1; all inputs content-pinned by controls/driver-pins.json.

Counting command: `python3 -B .ufo/waves/round-66/w1/ExecCatDriver/verify.py --revision REV --controls-revision 0d5aef2f40dce3129e91419c34b6c46087089b94 --cat-mutbat .ufo/waves/round-66/cat-mutbat.py --work /fast/scratch/hyaku/kasegi-r66/L1/MEASUREMENT --final`. Before uses base revision and omits --final. Final measurement still owed. Any failed RESULT/nonzero defeats C1; frozen target is not narrowed.

Only cat's SIGPIPE exception is restricted, with intentional conservative refusals for multi-input and option-bearing cat; this does not assert a missing input in every newly stale case. Non-cat heads retain the old exception. Coverage8/density9 held, no new knowledge/frontier/capability/score increase or retirement. One v1 wave9, no residual call; L1 planner. Existing unanswered operator decisions stay unanswered.

## Round66 measured result — C1 verifies on the finite frozen predicate

Freeze32a24002c252ec052aa535c6893d53da3004e14f; measured implementation **e8a865da49f3d1ff0e7222830006b3003d4577c0**. Same driver5962b7d6, collector d788bbc1, content pins and controls0d5aef2f as frozen; no counter amendment after freeze.

| Axis | Before | After | Score delta and measurement |
|---|---|---|---|
| depth:verifiability (lowest) | Exact baseb6db9e81 VERIFY12/3 exit1; collector8/3 under candidate expectations; selftest63/0 | Committed final VERIFY12/0 exit0; collector8/0, driver-owned eight shapes under two ids hold, selftest67/0, existing mutant5/5, finite cat mutant3/3 with equivalent held/invalid rejected, real ledger35/35, wrong-want red/right-want green | **4→4 delta0, nominal R58**. Counting command in the frozen plan above, REV=e8a865da49f3d1ff0e7222830006b3003d4577c0; receipt `.ufo/waves/round-66/controls/final-verification-r66.txt` and raw final-children/. |
| coverage |8|8 held| No coverage claim, knowledge/frontier admission or new capability. Registry98→99 is S099 own-work curation only. |
| depth:density |9|9 held| Not targeted or remeasured; live registry facts/current-execution amendment only. No density credit. |

Existing derive-gate and figure-audit capabilities are extended; **no new repertoire row**. Saturation9/10 and stagnation window unchanged; no retirement/split/waiver. Actual score gap remeasured:82 rechecks,60 execute,22 gated on lost bases,0 broken; score5 still requires0 gated unsupported claims (`controls/score-gap-after.txt`, exit0).

ONE v1 wave9 settled (WAVE-DONE before final measurement/report), **8 evidence-producing,1 dead**: MutationCat, `402 Upstream request failed: Insufficient account funds (type=server_error)` on opencode-go/deepseek-v4.1-flash, no output/report. No replacement/residual call. L1 supplemental mutation battery is not output of that seat. L1 planner; three executor, reviewer, critic, mutation-tester, scout, connector, scribe; assigned attack3/9 (completed attack2/8). Results' null outputs are a shared orchestrator kernel-restart limitation; eight seat reports and `seat-error-telemetry.json` provide the actual evidence.

ReviewCat independently43/43 predicted cases holds the finite rule, with18 intentional conservative changes and25 unchanged controls. This does not claim every newly stale case contains an input error: multi-input/option-bearing cat SIGPIPE is deliberately refused, other heads keep their prior exception. Production ledger35/35 and enumerated positives hold; broad semantic authenticity/sandbox/no-regression claims are not made.

### Planned after round66 (not frozen)

Lowest depth:verifiability4 remains. Source restoration and R67/R69/operator security boundaries are still unanswered; do not re-claim this finite cat repair or move its score. A successor must choose a distinct observed residual with a failing no-work control and reject relevant forgeries before freeze. Coverage8 holds; FIRST maturity/Fuzzilli/OpenSSF aggregate/API remain leads requiring their own source/novelty/claim-table gates. Proposal2/end-to-end domain-task credit remains open.

## Round 67 — multi-head SIGPIPE input-count rule (C1, depth:verifiability, nominal 4 held) and F45, the FIRST PSIRT maturity ladder (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-67/claims.json` (freeze `b30820609b033003550f0a99624337f8d50ebef3`, base `8e2a8fe8eb92d7c824902a4b70aab027a9aacee0`, controls revision `7ae95a0662adefff9bca5fed3075d3671a9e000d`); two errata disclosed in `.ufo/waves/round-67/claims-erratum-1.md` (commits `e59c564e65fa6ee9e79dc9f57f74dbf1dd737e9b` and `c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146`), which changed no frozen predicate, probe set or verdict rule. Measured implementation **`c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146`**, production gate sha256 `8147350c411650b4fe3307b50851722025a00cc1e71df2ecff478ea7177ad247`.

Counting command: `python3 -B .ufo/waves/round-67/w1/ExecMultiHeadDriver/verify.py --revision REV --controls-revision c40f0bc8ae95627b60b6f6e893ea00d7b1fd7146 --work /fast/scratch/hyaku/kasegi-r67/L1/FINAL --final`; before uses base `8e2a8fe8` and omits `--final`.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | Base gate `51f299af`: no-work control reads **ok** on `cut`/`wc`/`grep` two-operand SIGPIPE pipelines whose second operand was never opened (`NOWORK-VERDICT … green_on_masked=P9,P10,P11,P12,P13,P14`), and ok on the mid-argv `--` dash-file spellings (native stage0 −13 five of five); selftest 67/0; base probes 20/0 with five collector mismatches on the base gate | `VERIFY measurements=12 failures=0 revision=c40f0bc8 mode=final` exit 0; probes-measured 20/0 with **P9, P10, P11, P19, P20 stale** (`derive-upstream-signal-13` on every −13 face, P10 stale on its non-signal face too) and P12–P18 keeping their base verdicts; shape-identity 20 shapes; selftest 73/0; existing mutbat 5/5; multihead mutbat `killed=7/7 survivors=0 equivalents=3`; real ledger 35/35; red-wrong-want and identity guards hold | **4 → 4, delta 0, nominal per R58** (the citation-resolution metric this axis scores is not read by the gate). Receipt `controls/final-verification-r67.txt`. |
| coverage | `FRONTIER-CENSUS rows=44 admitted=44 closed=44 problem-rows=0 registry=99`; `entries=47 pass=47`; capture `records=79 bound=79 unbound=0`; knowledge 82; F45 absent (lead only) | `rows=45 admitted=45 closed=45 problem-rows=0 registry=101`; `FRONTIER-PASS F45 ids=S100,S101`; `entries=48 pass=48`; `records=81 bound=81 unbound=0`; knowledge 83; expected list 83 entries / 85 lines; census exit 0, six inherited W04 warnings, none on S100/S101 | **8 → 8, delta 0.** `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-67/manifest.json --source S100` (and `--source S101`); `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`. Before counters `controls/c2-base-counters-r67.txt`, after `controls/census-after.txt`. |
| depth:density | 9 | 9 held | Not targeted or re-measured. The SKILL.md change is one current-execution amendment; no density credit asserted. |

**Residuals named, not claimed:** `git` and `python` heads keep the head-blind SIGPIPE rule; descendants and shell wrappers are unobserved; exit-0 partial-output producers (`grep -q`) defeat the rule; PATH/configuration decides which binary a stage is (this host's interactive shell exposes a builtin `grep` that is not the binary the gate resolves); the native face of a streaming stage is not stable (P10 flips between `-13` and `1`), so the claim asserts the verdict and records the face; semantic emulators beyond the finite forgery controls; lost-base source restoration and the unanswered r15/r57/r59/r60 operator decisions.

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is extended in place — the gate now also refuses a SIGPIPE'd read-only stage that named more than one input operand, including a dash-named operand after a mid-argv `--`, while keeping cat's round-66 rule byte-identical.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

### Round-67 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 67 | depth:verifiability | multi-operand SIGPIPE on `cut`/`wc`/`grep` reads `ok` at the base gate while a named input was never opened; mid-argv `--` spelling also reads `ok`; selftest 67 | five repair shapes stale on every observed face; single-input and non-SIGPIPE controls unchanged; selftest 73; multihead mutbat 7/7 with 3 equivalents | `.ufo/waves/round-67/controls/{donothing-multihead-r67.txt,critic-s3s4-confirm-r67.txt,final-verification-r67.txt}` |
| 67 | coverage | frontier 44 / registry 99 / entries 47 / capture 79 / knowledge 82; F45 absent | frontier 45 / registry 101 / entries 48 / capture 81 / knowledge 83; F45/S100/S101 admitted; 46 entry quotes pinned and located | `corpus/knowledge/first-psirt-maturity-document.md`; `corpus/source-snapshots/round-67/`; `controls/{c2-base-counters-r67.txt,census-after.txt}` |
| 67 | calibration | wave payload carried two expectations the base matrix contradicted (P1/P2 base rc0, P8 candidate signal-13); a flaky native face (P10) had been frozen to one reason; a counter sub-assertion scored a diagnostic line as a failure; two writers touched one pinned control | payload preserved and corrected by a committed addendum delivered to the seats; P10/P11/P19/P20 verdict-level with faces recorded; collector findings recorded, not scored; one writer per control, post-commit edit reverted | `corpus/lessons/round-67.md` § Mistakes; `controls/dispatch-addendum-r67.md`; `claims-erratum-1.md` |

### Planned after round 67 (not frozen)

1. **depth:verifiability (4, lowest):** the next gate claim must pick a distinct observed residual with a failing no-work control — candidates named this round: `git`/`python` head SIGPIPE masking, exit-0 partial-output producers (`grep -q`), and wrapper/descendant stages. Do not re-claim the five repaired shapes.
2. **coverage (8):** the F45 figures (three PNGs) are unanchorable in text; a future round may capture them as their own artifact with an image-quote model. FIRST's PSIRT Maturity document is otherwise closed; the OpenSSF aggregate-score/API and Fuzzilli primary docs remain unopened leads.

## Round 68 — program-execution flags refused (C1, depth:verifiability, nominal 4 held) and F46, the OpenSSF Scorecard API contract (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-68/claims.json` (freeze `7c4f9f7ec096298b1edd1912249e5864ee73d985`, base `d0f48405e7fe44a53a28305785dc4d881a414194`, pre-freeze controls `3dfe6f162c9cec8fdbb629738b36fc53a7ce6128`); measured implementation **`82b3b7d4704e914eb224e7bb24e57aa9cbd8603f`**, gate sha256 `10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8`.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | `VERIFY measurements=8 failures=4` exit 1 at the base gate: both program-execution flags admitted and executed (compressor 18288 runs, textconv driver 1 run), selftest 73 cases, write-side-effect FAIL | `VERIFY measurements=8 failures=0` exit 0 at `82b3b7d4`: both probes `rc=2 reason=derive-not-read-only marker_runs=0`, five read-only controls exact, selftest 77/0, mutbat 5/5, ledger 35/35, red fixture stale, no write side effect | **4 → 4, delta 0, nominal per R58** (the axis's citation-resolution metric is not read by this gate). `python3 -B .ufo/waves/round-68/controls/c1-probe-run-r68.py --gate corpus/instruments/figure-audit.py --work /fast/scratch/hyaku/kasegi-r68/L1/FINAL --mode candidate`; before `controls/c1-base-donothing-r68.txt`, after `controls/final-verification-r68.txt`. |
| coverage | `FRONTIER-CENSUS rows=45 admitted=45 closed=45 problem-rows=0 registry=101`; `entries=48 pass=48`; capture `records=81 bound=81`; knowledge 85 lines / 83 entries; F46 absent | `rows=46 admitted=46 closed=46 problem-rows=0 registry=102`; `FRONTIER-PASS F46 ids=S102`; `entries=49 pass=49`; capture `records=82 bound=82 unbound=0`; expected list 86 lines / 84 entries `sort -c` clean; census exit 0 | **8 → 8, delta 0** (the coverage denominator is operator-owned). `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `wc -l` + `grep -vc '^#' corpus/instruments/knowledge-expected.txt`; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; before `controls/c2-base-counters-r68.txt`, after `controls/c2-after-counters-r68.txt`. |
| depth:density | 9 | 9 held | Not targeted or re-measured. `SKILL.md` gains one registry fact (selftest 73 → 77) and one current-execution amendment; no density credit asserted. |

**C1 scope, stated exactly.** The claim's declared spelling set is refused at parse time: `--compress-program` written with `=`, as a separate token, quoted, or after another option; and the exact token `--textconv`. Neither named program runs. The wave's attack seats then defeated the repair **as a class**: unique long-option prefixes of `--compress-program` (`--compress-prog=`, `--compress=`, `--co=`) are admitted by this host's uutils sort and run the compressor (18288 runs each per CriticC1, 9144 per SentinelGate), `git show <commit>` runs a config-declared textconv driver through `.gitattributes` with no flag at all, and `git cat-file --textconv/--filters` still execute. Those classes are named open with receipts under `.ufo/waves/round-68/w1/` and are round 69's candidate ground; they are not claimed here and do not narrow the measured predicate.

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is extended in place — the gate now also refuses the two measured program-execution flags at parse time while keeping every admitted read-only derive byte-identical; demonstration `controls/final-verification-r68.txt` → 8/0.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

### Round-68 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 68 | depth:verifiability | two program-execution flags admitted and executed at the base gate; selftest 73 | both refused at parse time with the programs unexecuted; selftest 77; class-level residuals named open | `.ufo/waves/round-68/controls/{c1-base-donothing-r68.txt,final-verification-r68.txt}`; `w1/{CriticC1,SentinelGate,RevengerC1}.md` |
| 68 | coverage | rows=45 registry=101 entries=48 capture=81 knowledge=83 | rows=46 registry=102 entries=49 capture=82 knowledge=84 | `.ufo/waves/round-68/controls/{c2-base-counters-r68.txt,c2-after-counters-r68.txt}`; `corpus/knowledge/openssf-scorecard-api-contract.md`; `corpus/source-snapshots/round-68/` |
| 68 | calibration | round-67 routed defects V67-1..V67-6 open; `citation-ground-check.py` findings 10 | V67-1/V67-3/V67-4 fixed as appended corrections; V67-2 reduced to findings 6 (`class-lane-bare` 1); V67-5/6 recorded | `corpus/knowledge/first-psirt-maturity-document.md` § Corrections; `.ufo/waves/round-67/controls/driver-pins.json`; lesson § Round-67 disposition |

### Planned after round 68 (not frozen)

1. **depth:verifiability (4, lowest):** close the class the wave opened — prefix-abbreviation denial for the counted/denied heads, the default-textconv path (`git show <commit>` through `.gitattributes`), and `git cat-file --textconv/--filters` — each with a failing no-work control, a mutation limb and a paired base run before the freeze (RevengerC1's ranked table is the candidate list).
2. **coverage (8):** the Fuzzilli primary documentation remains the only unopened lead; the served-instance question (whether `api.scorecard.dev` and `api.securityscorecards.dev` serve the same data) is recorded as unknown, not a lead.

## Round 69 — derive-gate class refusal of the eight measured program-execution/write shapes (C1, depth:verifiability, nominal 4 held) and F47, the GitHub global security advisories REST API (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-69/claims.json` (freeze `9b877fd916308e948b865c44ebc76e6ad322d6a7`, base `656272cf6b753fab7ce249f286b824c87677fdf3`, pre-freeze controls `4d91dcd3f3cfdb3bad0324ac20c30bce489eee61`); measured C1 implementation **`1bd01ee1e6558925e23d3d27a4bb12b88f502656`**, gate sha256 `c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde`; C2 landing **`981115648e4108e1adf5aec010edadac285a0c78`**.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | `VERIFY measurements=13 failures=10` exit 1 at the base gate (= round-68 measured gate `10c87100…`): P1..P8 admitted — compressor 18288 runs per abbreviation spelling, `--outp=`/`-uo` wrote their files, textconv driver and smudge filter ran; selftest 77; write side effect FAIL | `VERIFY measurements=13 failures=0` exit 0 at `1bd01ee1`: P1..P8 `rc=2 reason=derive-not-read-only marker_runs=0 wrote=0`; nine read-only controls exact; selftest 86/0; mutbat 5/5; ledger 35/35; no write side effect | **4 → 4, delta 0, nominal per R58.** `python3 -B .ufo/waves/round-69/controls/c1-probe-run-r69.py --gate <gate exported from 1bd01ee1> --work /fast/scratch/hyaku/kasegi-r69/<seat>/<dir> --mode candidate`; receipts `controls/c1-base-donothing-r69.txt`, `controls/c1-forgery-blanket-r69.txt` (blanket refusal fails 4), `controls/final-verification-r69.txt` |
| coverage | `FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0 registry=102`; `entries=49 pass=49`; capture `records=82 bound=82`; knowledge 86 lines / 84 entries; F47 absent | `rows=47 admitted=47 closed=47 problem-rows=0 registry=103`; `FRONTIER-PASS F47 ids=S103`; `entries=50 pass=50`; capture `records=83 bound=83 unbound=0`; expected list 87 lines / 85 entries `sort -c` clean; census exit 0 | **8 → 8, delta 0** (the coverage denominator is operator-owned). `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `wc -l` + `grep -vc '^#' corpus/instruments/knowledge-expected.txt`; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; before `controls/c2-base-counters-r69.txt`, after `controls/c2-after-counters-r69.txt` |
| depth:density | 9 | 9 held | Not targeted or re-measured. `SKILL.md` gains the selftest pin 77 → 86 and one r69 current-execution amendment; no density credit asserted. |

**C1 scope, stated exactly.** The claim is the enumerated probe set P1..P8 (two `--compress-program` abbreviations, one `--output` abbreviation, one `-o` bundle, `git show HEAD`, `git show ':/fixture'`, `git cat-file --textconv`, `git cat-file --filters`), measured on `/usr/bin/sort` GNU coreutils 9.12 and git 2.56.0. It is not a class or sandbox claim; further shapes found by the wave are residuals in `corpus/lessons/round-69.md`.

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is extended in place — demonstration `controls/final-verification-r69.txt` → 13/0.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

### Round-69 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 69 | depth:verifiability | eight measured exec/write shapes admitted at the round-68 gate; selftest 77 | all eight refused at parse time, programs unexecuted, no file written; selftest 86 | `.ufo/waves/round-69/controls/{c1-base-donothing-r69.txt,final-verification-r69.txt}` |
| 69 | coverage | rows=46 registry=102 entries=49 capture=82 knowledge=84 | rows=47 registry=103 entries=50 capture=83 knowledge=85 | `.ufo/waves/round-69/controls/{c2-base-counters-r69.txt,c2-after-counters-r69.txt}`; `corpus/knowledge/github-global-security-advisories-rest-api.md`; `corpus/source-snapshots/round-69/` |
| 69 | calibration | round-68 routed defects V68-1..V68-5 open; sort identity stated two ways | V68-1/2/5 corrected by an appended erratum; V68-3 worked as C1; V68-4 recorded; QUALITY R101-R103 | `.ufo/waves/round-68/claims-erratum-r69.md`; `corpus/lessons/round-69.md` § Mistakes; `corpus/QUALITY.md` R101-R103 |

**Wave:** one v1 wave of 12 seats; 2 settled (ReviewC1, ReviewC2 — both VERIFIED), 10 dead on a provider 401 (`commandcode/deepseek/deepseek-v4.1-flash`), not replaced. Attack evidence beyond the two reviewers is author-only and labelled so in the lesson.

### Planned after round 69 (not frozen)

1. **depth:verifiability (4, lowest):** pin the two untested `git_show_operands_ok` limbs (no operand; `--`) with selftest cases (R103), and take one named residual with a failing base control — the python-head `--root`/`--out` counters (round-68 RevengerC1 rows 2 and 7) are the strongest candidates.
2. **coverage (8):** land the EUVD rejected row (R102) with a freeze that counts it, and consider "About the GitHub Advisory database" (the curation semantics F47 defers to) as the next F47-adjacent source.

## Round 70 — python-head write/exec/ingress option refusal (C1, depth:verifiability, nominal 4 held) and F48, the GitHub Advisory Database curation semantics (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-70/claims.json` (freeze `e74ba6b5d522b1e91dca3a2d244585d6b7babdc5`, base `e7c02bddaa32a4a70afb2e6278f108e03dca067c`, pins `controls/pins-r70.txt`); measured C1 implementation **`c1051749571caf6a0383b15187fc02cdd21785b5`**, gate sha256 `7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5`; C2 landing **`b4afd8a0206b23a69d8cd65d92070cdfcd4680a7`**.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | `VERIFY measurements=12 failures=9` exit 1 at the base gate `c09b0fb1…`: three `--root` spellings run the fixture entry's `recheck:` payload through `bash -c`, three `--out` spellings write their named outside file, `--json` does both; selftest 86 | `VERIFY measurements=12 failures=0` exit 0 at `c1051749`: P1–P7 `rc=2 reason=derive-not-read-only marker_runs=0 wrote=0`; eight read-only controls exact; selftest 96/0; mutbat 5/5; ledger 35/35; no write side effect. **But the claim's declared universal fails**: `CriticC1` measured 10 read-only derives the candidate refuses and the base re-derives (`--root` on six instruments, `--json` as a stdout flag, and four more), plus the exec class reachable with no option at all and through `--selftest`. | **4 → 4, delta 0, C1 NOT VERIFIED as declared — honest stop** (frozen predicate passes; declared clause "while keeping every read-only derive admitted" refuted). `python3 -B .ufo/waves/round-70/controls/c1-probe-run-r70.py --gate <exported gate> --work /fast/scratch/hyaku/kasegi-r70/L1/FINAL --mode candidate`; before `controls/c1-base-donothing-r70.txt` and the paired clone base `controls/c1-base-donothing-r70-clone.txt`; after `controls/final-verification-r70.txt`; refutation `.ufo/waves/round-70/w1/CriticC1.md` rows 1–17. Fix routed as V70-5/V70-6. |
| coverage | `FRONTIER-CENSUS rows=47 admitted=47 closed=47 problem-rows=0 registry=103`; `entries=50 pass=50`; capture `records=83 bound=83`; expected 87 lines / 85 entries; knowledge 85; F48 absent | `rows=48 admitted=48 closed=48 problem-rows=0 registry=105`; `entries=51 pass=51`; `records=84 bound=84 unbound=0`; expected 88/86 `sort -c` clean; knowledge 86; F48/S105 admitted, S104 rejected row landed; census exit 0 | **8 → 8, delta 0** (the coverage denominator is operator-owned). `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `wc -l` + `grep -vc '^#' corpus/instruments/knowledge-expected.txt`; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; before `controls/c2-base-counters-r70.txt`, after `controls/c2-after-counters-r70-clone.txt` (pinned pre-freeze receipt `controls/c2-after-counters-r70.txt` unchanged, R107). |
| depth:density | 9 | 9 held | Not targeted or re-measured. `SKILL.md` gains the selftest pin 86 → 96 and one r70 current-execution amendment; no density credit asserted. |

**C1 scope, stated exactly.** The claim is the enumerated probe set P1..P7 on this host (python3 3.14.8, `/usr/bin/sort` GNU coreutils 9.12, git 2.56.0). The new rule refuses the named long options and any unique abbreviation of them plus a short `-o`; it is not a sandbox — positional arguments, a counter's own writes on a positional path, non-denied options and the `--` operand boundary stay open, and the lesson names them.

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is extended in place — demonstration `controls/final-verification-r70.txt` → 12/0.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

### Round-70 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 70 | depth:verifiability | python head admits every counter under `corpus/instruments/`; `--root` executes a root-supplied `bash -c` payload, `--out`/`--json` write arbitrary paths; selftest 86 | the seven measured long options refused by name and unique abbreviation plus `-o`; the two R103 `git show` limbs pinned; selftest 96 — **predicate verified, declared universal refuted (10 over-refusals), NOT VERIFIED** | `.ufo/waves/round-70/controls/{c1-base-donothing-r70.txt,final-verification-r70.txt}`; `.ufo/waves/round-70/w1/CriticC1.md` |
| 70 | coverage | rows=47 registry=103 entries=50 capture=83 knowledge=85 | rows=48 registry=105 entries=51 capture=84 knowledge=86; F48/S105 admitted, S104 rejected | `.ufo/waves/round-70/controls/{c2-base-counters-r70.txt,c2-after-counters-r70.txt}`; `corpus/knowledge/github-advisory-database-curation-semantics.md` |
| 70 | calibration | round-69 routed defects V69-1/V69-2/V69-3 open; round-70 process misses M70-1..M70-4 found in-round | V69-1 landed as S104, V69-2 pinned as two cases, V69-3 answered by six attack seats; M70-1..M70-3 became QUALITY R104–R106 | `corpus/lessons/round-70.md` § Mistakes; `corpus/QUALITY.md` R104–R106 |

### Planned after round 70 (not frozen)

1. **depth:verifiability (4, lowest):** land V70-5 first — per-script denial instead of the global name list (`--root` is a read-only pointer in six-plus instruments; `--json` is a stdout flag in `claim-package-check.py`), with the 10 over-refusal rows as paired positive controls — then V70-6 (`--selftest` and the no-argument `frontier-recheck-count.py` spelling). Do not re-claim the seven repaired options as a win; the round's own gate moved and its claim still failed.
2. **coverage (8):** the Fuzzilli primary documentation remains the only unopened lead; the "About the GitHub Advisory database" page is now closed by F48, so a successor must open genuinely new ground (e.g. the OSV schema's own field definitions beyond S080) rather than re-reading curation prose.

## Round 71 — the per-script python-head census in the derive gate (C1, depth:verifiability, nominal 4 held) and F49, the TrendAI ZDI disclosure process and vendor coordination (C2, coverage, 8 held)

Frozen claims: `.ufo/waves/round-71/claims.json` (freeze `0e260a54b0a670cee2915237ac403d37164c749d`, base `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`, pins `controls/pins-r71.txt`); measured C1 implementation **`4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`**, gate sha256 `182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603`; C2 landing **`4e33119`** (capture + entry), registry row **`34faab9`**.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | `VERIFY measurements=25 failures=13` exit 1 at the round-70 gate (`7a8d52eb…`): N8 runs a root-supplied `recheck:` payload through `bash -c` (`marker_runs=1`), N9 `--selftest` admitted, N12 a head absent from any list admitted, and all eight read-only R rows refused (`admitted=0`); selftest 96 | `VERIFY measurements=25 failures=0` exit 0 at `182f4ef7…`: N1-N12 `rc=2 reason=derive-not-read-only marker_runs=0 wrote=0`; R1-R8 admitted and each re-derives its value (`FIG rN … ok`); selftest 106/0; mutbat 5/5; ledger 35/35; no write side effect. `R8`'s pipeline (`grep -c records=84`) now yields an empty value, so that row's value limb is vacuous — routed V71-4 | **4 → 4, delta 0, nominal per R58** (the axis counter `resolve.py` reads citation resolution and this gate does not move it) — and **C1 is NOT VERIFIED as declared**: `AttackC1` measured that the sentence's clause "re-deriving each one's own value" is false for R5-R8, which take the counter's stale-exit branch and compare nothing, and `SentinelC1` measured two regressions against the base gate (see the harm note below). `python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate <gate exported from 4e33119> --work /fast/scratch/hyaku/kasegi-r71/<seat>/FINAL --mode candidate`; receipts `controls/{c1-donothing-r71.txt,c1-base-r71.txt,c1-candidate-trial-r71.txt}` |
| coverage | `FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105`; `entries=51 pass=51`; capture `records=84 bound=84`; knowledge 88 lines / 86 entries; 86 files; F49 absent | `rows=49 admitted=49 closed=49 problem-rows=0 registry=106`; `FRONTIER-PASS F49 ids=S106`; `entries=52 pass=52`; capture `records=85 bound=85 unbound=0` exit 0; expected 89/87 `sort -c` clean; 87 files; census exit 0 (six inherited W04) | **8 → 8, delta 0** (the coverage denominator is operator-owned). `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `wc -l` + `grep -vc '^#' corpus/instruments/knowledge-expected.txt`; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`; before `controls/c2-base-counters-r71.txt`, after `controls/attempt2-tip-counters.txt` |
| depth:density | mean 270.9, 38 blocks, 925 path-citation instances (`SKILL.md` at `3cc8cd4`) | mean **272.6**, 38 blocks, 932 cites, `anchorcheck.py SKILL.md` exit 0 with 0 `BAD` lines | **9 → 9, unchanged, no credit claimed.** `SKILL.md` gains the r71 amendment paragraph and the gate row's selftest pin 96 → 106 (both side effects of C1, not a density target); both sides measured with the committed `density.py` and `anchorcheck.py`. |

**C1 harm note (measured, not repaired in this round).** The per-script census that repairs the round-70 over-refusal re-admits `--root`/`--work`/`--scratch` on **23 censused heads**; one ledger derive wrote **22,012 files** into a ledger-chosen directory against `rc=2` on the round-70 gate, and a basename alias inside `corpus/instruments/` restores the denied flags (2,595 bytes written where the base refused). Both are `SentinelC1`'s regressions 1-2 (`.ufo/waves/round-71/w2/SentinelC1.md` §4). The frozen claim is not narrowed or withdrawn; the round reports the trade and routes V71-7/V71-8 (R115) to round 72. A trade is not an improvement, so the round claims no score move and does not claim the axis unharmed.

**C2 distinctness erratum (appended 2026-11-05).** The frozen C2 sentence listed the 120-day window, the 30/60/90-day shortening, the 15-business-day escalation and the full-versus-limited advisory choice as F49's ground; `ScoutF49` measured all four already held from ZDI's own policy page S075 (`S075.txt:23-25`) in `corpus/knowledge/zdi-disclosure-policy.md`. F49's ground is narrowed to the acquisition-side flow (validate -> severity -> formal monetary offer -> payment -> vendor coordination -> credit or anonymity), the no-limit/no-backlog guarantees, the dossier contents and three measured wording divergences between S106 and S075 (`corpus/README.md` `[r71 erratum 1]`). The row, entry and every counter are unchanged; the coverage score stays 8 and the lesson carries M71-3 / QUALITY R114.

**C1 scope, stated exactly.** The claim is the enumerated probe set N1-N12 and R1-R8 on this host's PATH `python3` 3.14.8, GNU coreutils `sort` 9.12 and git 2.56.0. It is an enumerated option set plus a per-script census, **not** a sandbox: positional arguments, a counter's own writes on a positional path, non-denied options, options after `--`, nested python invoked by an admitted counter, and exec classes not named here stay open and `corpus/lessons/round-71.md` § Residuals names them.

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is extended in place — demonstration `controls/c1-candidate-trial-r71.txt` → 25/0.

**Saturation:** line 9/10 per owned axis; lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

### Round-71 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 71 | depth:verifiability | round-70 global deny list: eight read-only derives refused, exec class reachable with no option (`marker_runs=1`); selftest 96 | per-script denial + fail-closed head census; twelve write/exec/ingress shapes refused at parse time, eight read-only derives admitted and value-matched; selftest 106 | `.ufo/waves/round-71/controls/{c1-donothing-r71.txt,c1-base-r71.txt,c1-candidate-trial-r71.txt}`; `corpus/instruments/figure-audit.py` sha256 `182f4ef7…` |
| 71 | coverage | rows=48 registry=105 entries=51 capture=84 knowledge=86 | rows=49 registry=106 entries=52 capture=85 knowledge=87; F49/S106 admitted | `.ufo/waves/round-71/controls/attempt2-tip-counters.txt`; `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`; `corpus/source-snapshots/round-71/` |
| 71 | calibration | round-70 routed defects V70-5/V70-6 open; the r70 gate's over-refusal class unpinned | V70-5 and V70-6 worked as C1; V71-1/V71-2/V71-3 mined by the lesson's one-limb mutation audit, V71-4 by the L1's R8 reading; QUALITY R110 | `corpus/lessons/round-71.md` § Routed defects; `corpus/QUALITY.md` R110 |

**Non-author verification of this round.** Wave `w2` (12 seats) produced: `VerifyC1` `C1: VERIFIED` on the
frozen predicate; `AttackC1` `C1: NOT VERIFIED as written` (R5-R8 compare no value); `SentinelC1`
`REGRESSIONS=2` (23 heads re-admit a base-denied flag; a basename alias restores denied flags);
`MutateC1` `MUTANTS killed=7/15 survivors=M8a…M8h` (the eight per-script entries of V71-1 are
unpinned, and the round's frozen counter does not kill any of them); `VerifyC2` `C2: VERIFIED`;
`AttackC2` `OUTRUNS=8`, all applied in-round; `ConnectorTable` `NOT SCOPE CLEAR as frozen` on C2's
ground list, recorded as M71-3/R114; `ScoutNext` per-row `DISTINCT` verdicts for the named neighbours.

### Planned after round 71 (not frozen)

1. **depth:verifiability (4, lowest):** land V71-1 — one dedicated selftest case per per-script denial entry (eight entries change the gate's verdict when removed and no case fails without them, so the mutant set is `7/15`); V71-4/V71-6 — the positive rows whose direct command exits nonzero must compare a nonempty value; V71-7/V71-8 (R115) — the re-admission ledger for `--root`/`--work`/`--scratch` on 23 heads and the fixture-name basename alias; V71-9/V71-10 — `freeze-check.py`'s `bash -c` primitive and the `-- --selftest` bypass. All are gate-bytes or counter changes and need their own freeze.
2. **coverage (8):** the Fuzzilli primary documentation remains the only unopened lead in `corpus/README.md` § Leads; a successor round should open genuinely new ground (an acquisition-programme primary source the registry does not hold) rather than re-reading ZDI prose.
3. **calibration:** the round-71 mistake class M71-2 (a claim's after-state landing across two commits, so a seat grading the first commit reports NOT VERIFIED) is carried as QUALITY R111.

## Round 72 — the derive-gate write-root and realpath repair (C1, depth:verifiability, nominal 4 held) and F50, the Bugzilla REST API core v1 bug endpoints on S107 (C2, coverage, 8 held; declared target falsified in one clause)

Frozen claims: `.ufo/waves/round-72/claims.json` (freeze `a34ce4c`, 2026-11-05 00:47 -03). Do-nothing controls `controls/c1-census-donothing-r72.txt` (base gate `182f4ef7…`) and `controls/c2-base-counters-r72.txt`. Candidate gate `corpus/instruments/figure-audit.py` sha256 `4f59bda4…` (final bytes; seats measured `b146c81a…`, differing by one comment line, re-measured on the final bytes); counter `corpus/instruments/derive-head-census.py` sha256 `255fd407…`.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | census READMITTED 19 on base, alias admitted (`c1-census-donothing-r72.txt`); selftest 106 | `derive-head-census.py` `READMITTED=0`, `ALIAS-PROBE verdict=refused rc=2`, `POSITIVE admitted=2/2`, `CENSUS-RESULT ok` exit 0; `figure-audit.py --selftest` `cases=110 failures=0`; ledger `FIGURE-AUDIT figures=35 ok=35 stale=0` exit 0 | **4 → 4, delta 0, nominal per QUALITY R58.** The r72 repair reverses the round-71 measured harm (19 re-admitted write-class pairs, 2 alias bypasses) on the frozen predicate; it does not move the `resolve.py` citation counter, so the score is held. Parity: `K72ExecParity` 494 runs over 247 committed-ledger derive pairs, `IDENTICAL=247 DIFFERENT=0 REGRESSIONS=0`. Sweep: no base-refused row admitted (`K72ExecSweep`). Mutants: `figure-audit-mutbat.py` `killed=5/5 survivors=0 invalid=0 controls=pass` (m7/m9 anchors repointed to the new containment line). |
| coverage | F01–F49 admitted, `FRONTIER-CENSUS rows=49 admitted=49 registry=106`, entries 52, capture 85 bound, knowledge-expected 89/87 | `rows=50 admitted=50 closed=50 problem-rows=0 registry=107`; `FRONTIER-PASS F50 ids=S107`; `entries=53 pass=53 exit=0`; capture `records=86 bound=86 unbound=0`; knowledge-expected 90/88 sort-clean; 88 knowledge files; `sources-census.sh validate … kasegi` exit 0 | **8 → 8, delta 0 (the coverage denominator is operator-owned).** The after-state counters reproduce. **C2 is NOT VERIFIED as declared:** its frozen target names an `api_key` requirement that S107 does not state (zero `api_key` / `API key` / `authentication` lines in the capture, `K72AttackF50` §4). The entry records the absence as a measured limit and does not supply the clause from another source; the frozen wording is not rewritten after a seat scored it (M72-5). |
| calibration | mistake class M71-4 open; round-71 harm reported as "23 heads" | M72-3 states each count with its predicate (19 census pairs / 19 heads; 23 sentinel; 43 / 26 spot-check); M72-5 added for the frozen C2 clause | calibration is not an owned axis of this lane; recorded here for the learning trend only. |

**Verdicts (C1, C2).** C1 `VERIFIED` on its frozen predicate: the census and selftest after-state reproduce on the final bytes, the attack wave's `HOLDS on frozen predicate` (`K72AttackCensus` §5), parity and sweep show no regression against base, and the blanket-refusal positive control fails as designed. C2 `NOT VERIFIED as declared`: the after-state counters reproduce and the entry is grounded in S107, but the declared target's `api_key` clause is falsified by the source (`K72AttackF50` §5: `FALSIFIED on frozen wording`). Per the admission rule the round is **not admitted**; the operator rules on C2 (see `## Open` in the round report).

**Capabilities:** no new repertoire row. The `derive-gate-chain-refusal` row is extended by the census counter's demonstration (`controls/c1-census-donothing-r72.txt` red, the final census green).

**Saturation:** lowest non-retired axis remains depth:verifiability 4, worked nominally this round. No retirement, split or nudge waiver.

**Correction (append-only, R-4):** the round-71 harm figure "23 censused heads" is one of three predicates. The round-72 census measures 19 heads and 19 write-class pairs (15 `--work`, 4 `--scratch`) with `--root` and `--json` outside its set; the sentinel's 23 counts any base-denied name, and the spot-check's 43 / 26 is the ast count over the r71 tables. The round-71 move-log row is not edited.

### Round-72 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 72 | depth:verifiability | r71 gate: `--work`/`--scratch` per script only (19 re-admitted pairs), basename-keyed policy (alias admitted); selftest 106 | global `--work`/`--scratch` denial, realpath-keyed policy, four new selftest cases; selftest 110 | `.ufo/waves/round-72/controls/c1-census-donothing-r72.txt`; `corpus/instruments/derive-head-census.py`; `corpus/lessons/round-72.md` § Mistakes M72-1, M72-2 |
| 72 | coverage | rows=49 registry=106 entries=52 capture=85 knowledge=87 | rows=50 registry=107 entries=53 capture=86 knowledge=88; F50/S107 admitted; C2 target clause falsified | `.ufo/waves/round-72/controls/c2-base-counters-r72.txt`; `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md`; `corpus/source-snapshots/round-72/S107.txt` |
| 72 | calibration | r71 harm count unpinned by predicate; frozen C2 target named an unsourced clause | M72-3 and M72-5 recorded; the harm counts stated per predicate | `corpus/lessons/round-72.md` § Mistakes |

### Planned after round 72 (not frozen)

1. **depth:verifiability (4, lowest):** the round-72 routed defects R-1 (`--json`/`--root` in the census set, a frozen-counter amendment), R-2 (`freeze-check.py` `bash -c` exec with its own census row), R-3 (`sort -T` temp-directory writes), R-6 (regular file named as a fixture head) and M72-4 (the counter's negative branch). Each needs its own freeze before its bytes change; the realpath alias semantics of R-5 needs an operator ruling first.
2. **coverage (8):** the C2 `api_key` clause is an operator decision: either a source that states the API-key rule is opened and admitted as a new claim (not a repair of this one), or the clause is struck from the target by the operator. No further Bugzilla ground is claimed.
3. **calibration:** M72-5 becomes a QUALITY criterion: a frozen target's content clauses must be located in the source it names before the freeze.

**Late-seat amendment (append-only; the verdicts above stand as measured, and these add the revived seats' findings; `corpus/lessons/round-72.md` § Late seats, L72-1…L72-10).** The mutation-tester (`K72Mutate`) killed the four gate mutants that matter (drop `--work`, drop `--scratch`, argv-basename keying, blanket refusal) and found three counter-internal survivors (the POSITIVE limb dropped from `ok`, a forged alias verdict, and the census-membership of the counter itself, which the gate selftest catches). The critic (`K72Falsify`) found C1's universal sentence falsified off-tree (a hand-parsed head with `--url` is admitted; the shipped heads parse with `add_argument`), C1's kill clauses weakened, and C2's kill rule not the complement of its predicate (the copy-only control fails the predicate through a capture-binding exit that the rule does not name). Revised verdicts: C1 **holds on its frozen predicate** with its universal sentence weakened; C2 **counters hold, target falsified in the `api_key` clause, kill rule incomplete**. Neither claim is admitted on its declared sentence; the round is not admitted until the operator rules.

**Parent-ruling amendment (append-only, L1, after WAVE-DONE):** C2's frozen text is preserved in `.ufo/waves/round-72/claims.json`; the narrowed target (api_key, security-group and mandatory-field contract removed) and the complement kill rule are in `.ufo/waves/round-72/claims-amendment-c2.json`, for the operator to accept or reject. The frozen verdict stays NOT VERIFIED AS DECLARED. Parity was re-measured by the L1 on the exact committed bytes (`controls/parity-final-r72.txt`, 247 identical, 0 different), because `K72ExecParity` died on a provider usage limit. Probe rows 10/29 re-measured on the exact bytes (`controls/probe-rows-10-29-r72.txt`).

## Round 73 — the Q10 recheck cwd repair (C1, depth:verifiability, held at 4) and F51, the OSV.dev POST /v1/query contract on S108 (C2, coverage, held at 8)

| Axis | Score before r73 | Score after r73 | Evidence pointer | Last change |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 4 (held; the measured move is on the Q10 recheck instrument, not on the scored `resolve.py` census) | `corpus/instruments/recheck-cwd-census.py`; C1-only candidate `RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22` (base: `noprefix=11 exit2_foreign=10 exit0_foreign=56 exit1_foreign=22`, exit 1); patch `.ufo/waves/round-73/w1/K73ExecRecheck.U3.patch` | r73 |
| coverage | 8 | 8 (held; F51 admitted, the coverage denominator stays operator-owned) | `frontier-recheck-count.py` `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108`, `PASS F51 ids=S108`, `entries=54 pass=54 exit=0`; `capture-binding-check.py` `records=87 bound=87 unbound=0` | r73 |
| depth:density | 9 | 9 (unchanged; not a claim target) | not re-measured this round | r15 (held) |

Claim verdicts: C1 holds on its frozen after-predicate measured on the C1-only tree; its `tree_scope` clause is falsified on the merged tree (prints `entries=89 exit0_foreign=67`); C2 holds on every frozen counter after value. No axis is harmed. Counting commands and base receipts: `.ufo/waves/round-73/controls/c1-donothing-r73.txt`, `c2-donothing-r73.txt`.

Move log (round 73): depth:verifiability — Q10 census (`noprefix` 11 → 0, `exit2_foreign` 10 → 0, `exit0_foreign` 56 → 66); coverage — frontier 50 → 51, registry 107 → 108, entries 53 → 54.

Planned after round 73: (1) counter amendment for RC-1 to RC-3 (`main()` in the selftest, a `/tmp` and leak fixture, a two-recheck-line fixture), frozen with its own do-nothing receipt; (2) operator ruling on RC-8 (whether knowledge recheck values may run in a counter); (3) the R-1 to R-3 write-class work from round 72.

Saturation 9/10 held; no axis retired; no capability row entered this round.

## Round 74 — the recheck-cwd counter amendment that kills the r73 survivors (C1, depth:verifiability, held at 4, nominal R58) and F52, the Fuzzilli README on S109 (C2, coverage, held at 8)

Frozen claims: `.ufo/waves/round-74/claims.json` (freeze `847b5379`, base and controls `ccd6a54`, controls commit `654d877f`). Implementation: `corpus/instruments/recheck-cwd-census.py` amended from `.ufo/waves/round-74/w1/ExecC1Amend.patch` (applied in the lane tree; selftest 1 → 5 cases; body of `first_recheck`, `run_foreign`, `census`, `main` byte-identical). C2 admission: `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`, S109, manifest `corpus/source-snapshots/round-74/manifest.json`.

| Axis | Before | After | Score delta, command and evidence |
|---|---:|---:|---|
| depth:verifiability (lowest) | r73 counter selftest `cases=1`; four routed mutant classes (M4 forced conformant, M5 `/tmp` parent, M6 scratch leak, M7 last-line reader) each exit 0 (`.ufo/waves/round-74/controls/c1-redbefore-mutant-survival-r74.txt`) | `--selftest` `selftest cases=5 failures=0` exit 0; the four mutants each exit 1 (`failures=1`), integrator rebuild and seat battery both; parity byte-identical to the base receipt (`e1906b88…f241`); census `noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0` conformant exit 0 | **4 → 4, delta 0, nominal per QUALITY R58** (the scored `resolve.py` census is not read by this gate). Counting command: `TMPDIR=<scratch> python3 corpus/instruments/recheck-cwd-census.py --selftest` (exit 0, `cases=5 failures=0`). |
| coverage | `FRONTIER-CENSUS rows=51 admitted=51 closed=51 registry=108`; `entries=54 pass=54`; capture `records=87 bound=87`; knowledge 89; expected 91/89 (`.ufo/waves/round-74/controls/c2-base-counters-r74.txt`) | `FRONTIER-CENSUS` 52 admitted; `PASS F52 ids=S109 exit=0`; `entries=55 pass=55 exit=0`; capture `records=88 bound=88 unbound=0` exit 0; registry 109; knowledge 90; expected 92/90 sort-clean; `sources-census.sh validate --root … kasegi` exit 0 | **8 → 8, delta 0** (the coverage denominator is operator-owned). Counting commands: `python3 corpus/instruments/frontier-recheck-count.py`; `python3 corpus/instruments/capture-binding-check.py`; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`. |
| depth:density | not targeted | not re-measured | 9 held (not a claim target; no density credit asserted). |

**Verdicts.** C1 VERIFIED on its frozen after-predicate and kill rule (a)-(d); its scope sentence is WEAKENED as written (M74-6: a `restoration-recheck:`-only file is an entry with `norecheck=1`, while the value-level exclusion holds) and is routed to round 75 with its own freeze. C2 VERIFIED on its frozen counters and kill rule; two clauses (registry-unchanged, capture word-count/anchor) lacked a named command at the freeze and were measured independently by the integrator (`git diff ccd6a54 -- corpus/SOURCES.md`: 0 removed lines; `source-recheck.py`: 16 of 16 `anchor=<n>-ok`, longest quote 22 words). Non-author closure pending (see the lesson's `## Gate` note).

**Capabilities:** no new repertoire row. The existing `derive-gate-chain-refusal` row is not affected; the recheck census's demonstration is `corpus/instruments/recheck-cwd-census.py --selftest` → `selftest cases=5 failures=0`.

**Saturation:** line 9/10 per owned axis is unchanged by this round's score-holding claims; lowest non-retired axis remains depth:verifiability 4 (worked nominally). No retirement, split or nudge waiver. The round is a trial of the end-to-end path (SHONEN box 2 `[~]`), not a score move.

### Round-74 move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|---|
| 74 | depth:verifiability | four routed mutant classes survive the r73 selftest (`cases=1`) | four classes killed by a five-case selftest (`cases=5`); census shape and parity unchanged | `.ufo/waves/round-74/controls/c1-redbefore-mutant-survival-r74.txt`; `.ufo/waves/round-74/w1/ExecC1Amend-{selftest,census,parity,kills}.txt`; `corpus/lessons/round-74.md` § Mistakes M74-6 |
| 74 | coverage | rows=51 registry=108 entries=54 capture=87 knowledge=89 | rows=52 registry=109 entries=55 capture=88 knowledge=90; F52/S109 admitted | `.ufo/waves/round-74/controls/c2-base-counters-r74.txt`; `corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md`; `corpus/source-snapshots/round-74/S109.txt`, `manifest.json` |
| 74 | calibration | r73 Gate lacked a reject line; R33 id held twice; freeze-check replay and capture-exit receipts carried a pipe exit; seat manifest had null provenance | R119 (gate reject line) and R120 (supersession, collision recorded not repaired) added; receipts corrected by appended block; manifest rebuilt by integrator | `corpus/lessons/round-74.md` § Mistakes M74-1..M74-5; `corpus/QUALITY.md` lines 552-559 |

### Planned after round 74 (not frozen)

1. **depth:verifiability (4, lowest):** a counter amendment that makes `restoration-recheck:`-only files and the `norecheck` result explicit (M74-6), with a do-nothing control and its own freeze; the docstring sentence that states the exclusion moves with it.
2. **coverage (8):** the NDSS 2023 Fuzzilli paper is a named lead (existence only); the OSV overview page is a lead whose two statements need their own capture and manifest before any row.
3. **calibration:** the R33 id collision (`corpus/QUALITY.md:292`, `:550`) is renumbered by document in a later round; the sibling-distinctness sentence (M74-7) is narrowed before the next claim freezes.

