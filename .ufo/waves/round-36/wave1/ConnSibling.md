# ConnSibling — round 36 wave 1 (connector seat: sibling-overlap scan consolidation → contested-scope ruling)

Seat id: `ConnSibling`. Assignment: consolidate the two sibling-overlap scan outcomes
(`ScoutF19Sibling.md`, `ExecSiblingSweep.md` in this directory) into the round's adjacency ruling:
(1) is F19/S053 contested by any sibling; (2) does the doctrine assign first.org to this lane;
(3) state the PROVINCE adjacency handling (report, don't absorb); (4) produce the final ruling text
for the lesson. Lane bounds: leaf — no subagent dispatch; no `agent://all`.

Object under protection: C2 / F19 (FIRST EPSS — exploitation-likelihood scoring) / S053
(`corpus/SOURCES.md` S053 row + `corpus/knowledge/epss-exploit-prediction-scoring.md`, both
in-flight by sibling seats at this seat's run time — absent at the freeze head `b47f2cdf`, which is
expected, not a defect).

## Sources consolidated

| source | verdict label | load-bearing content |
|---|---|---|
| `wave1/ScoutF19Sibling.md` | UNCONTESTED | 0 strict hits in 20 sibling lanes + shokuknow; 498 loose files all classified false-positive; kagi SSVC probe noted; 0 doctrine EPSS rows |
| `wave1/ExecSiblingSweep.md` | RATIFIED (uncontested) | hidden-inclusive full-tree sweep: 127 files, `\bEPSS\b` → 0 files; sibling `SKILL.md` `vulnerabilit*` → 0 files; doctrine host check → no `first.org` row exists (caveats A/B/C) |
| this seat's independent re-runs | — | every load-bearing claim above re-executed; outputs below are mine, not quoted |

Label reconciliation: the two labels do not conflict. "UNCONTESTED" (scout) = no sibling holds
EPSS ground. "RATIFIED" (sweep) = the doctrine-host axis plus in-lane occupancy leave F19 in
kasegi's lane with no challenger — the sweep's own body states doctrine has **no** EPSS/FIRST host
row, so its "ratified" is ratification-by-domain-and-occupancy, not by host-table row (see Q2).
Consolidated ruling: **uncontested by every sibling; doctrine-assigned at the domain level only**.

## Q1 — Is F19/S053 contested by any sibling? NO (measured absence, two independent sweeps)

Lane set re-counted: `ls -d /home/vgpnk/Projects/shokunin/*-shokunin` → 21 lanes, 20 siblings swept.

My strict re-run (case-insensitive, word-bounded, whole trees, `.git` excluded):
`grep -rn -i -E '\bEPSS\b|first\.org|exploit prediction scoring'` over every sibling lane →
**1 file**, `mado-shokunin/.ufo/waves/round-25/controls/CtlCacheDelta.py:10`, match `ePss` inside a
base85/zlib-encoded Hyprland cache payload (`DATA = 'c-ri}…'`, a compressed fixture). That is the
identical row the sweep's hit table already carries (`mado … CtlCacheDelta.py | 10 | ePss | no —
fixture key`); it corroborates the sweep rather than adding ground. The scout's case-sensitive
strict sweep → 0 files; the sweep's `\bEPSS\b` decisive test → 0 files. Three regex formulations,
one answer: zero sibling EPSS ground.

Near-miss classes, all re-verified by this seat:

| class | where | count | ruling |
|---|---|---|---|
| `epssweep`/`r98b_epssweep` identifier (Godot epsilon/scale readback test arm) | game-dev-2d | 97 files (re-counted) | no — docs.godotengine.org-domain fixture, no vulnerability content |
| `LeinenEPSSJ24` DBLP key (author-surname substring; ICST24 flaky-test cost paper) | tameshi | 10 files (re-counted: knowledge + 2 `.ufo/evidence/round-47` + 7 wave files) | no — bibliographic key, paper is flaky-test cost |
| encoded/random substring (`ePss`, `epSS`, `ePSs`, `epss`…) | mado, kake, kotoba, kotodama, kaidoku, fleet `research/` | sweep's table, spot-checked 4 | no — fixture keys, OCR noise, patch symbols, binary `strings` dumps |
| `percentile` / `probability of exploit` loose alternatives | audio, kake, kengaku, kumitate, mori, kotodama | 20 files; `probability of exploit` → **0 files** | no — generic statistics vocabulary (EBU R128, Web Vitals p75, OpenAlex fields, io.latency) |
| adjacent vulnerability ground: kagi retained NVD API probes, CVE-2020-10735 | `kagi-shokunin/.ufo/waves/round-28/retained-probes/SrcCve202010735/nvd-api*.json` | 4 files, re-verified `"exploitation":"none","automatable":"no"` + `ssvc` keys | no — CISA-ADP **SSVC** decision points, a different framework from EPSS; retained probe, not a SOURCES row or knowledge entry |
| mori CVSS advisory chrome | `mori-shokunin/corpus/evidence/recheck-r32/S012.src` | re-verified | no — raw fetched GHSA HTML blob, not a taught claim |
| sibling `SKILL.md` domain probe | all 20 lanes | `vulnerabilit*` → **0 files** (sweep's command 5) | kasegi is the fleet's only vulnerability-domain lane |

The only genuine EPSS sentence in scope lives in the shokuknow campaign, not any lane corpus:
`shokuknow/lanes/revenger/round12/measurements/iwsec-program-20241113.txt:2196` — CSS2024 programme
abstract (Vuls maintainers' talk): 「…SSVCやKEV・EPSSなどを利用して考えます。」 It names EPSS as
one of three prioritisation inputs; it carries no method, threshold, or data. It corroborates the
F19 *framing* (exploitation-likelihood scoring triages scanner noise) in the Japanese security
literature; it must not be cited as a source and it contests nothing. (The sweep also recorded a
campaign-side filename/content mismatch — `iwsec-program-20241113.txt` holds the CSS2024 programme —
record-only; nothing in the round-36 claims depends on it.)

Registry/id adjacency (from the sweep, accepted): `S053` exists as a different lane-local row in
kake/tabi/tameshi `corpus/SOURCES.md`; `F19` in game-dev-2d/3d is a lane-local tween/actor finding.
No fleet id collision arises from kasegi's S053/F19.

## Q2 — Does the doctrine assign first.org to this lane? At the domain level, yes; by host-table row, no

Read the doctrine precisely, because the two frontier admissions differ here:

- **F18 (r35) had an explicit doctrine row.** `shokuknow/doctrine/channel-recurrence.md:62` —
  `| cisa.gov | kasegi |` — inside a 187-distinct-host census (168 one-off, recomputed by this seat:
  `grep -c '| \`' channel-recurrence.md` → 187 rows). That is host-level ratification.
- **F19 has no such row.** `grep -c 'first.org' channel-recurrence.md` → **0**; the whole
  `shokuknow/doctrine/` (12 files) carries **0** `first.org` rows, **0** EPSS rows, **0**
  `cve.org`/`nvd.nist.gov` rows, and the only `FIRST` word-matches are the English adverb
  (`coverage-lever.md`, `anchor-craft.md`) — re-verified. So **no doctrine host/channel row assigns
  first.org to kasegi — nor to any sibling**.

What assigns F19's host to this lane is the domain doctrine, three ways:

1. `PROTOCOL.md:457` — "One domain per shokunin; a domain belongs to one shokunin." The
   contested-scope invariant (`:457-461`) routes overlap reports into the lane report for
   integrator arbitration.
2. `PROVINCE.md:30` — the kasegi core "covers triage and claim gates". Exploitation-likelihood
   scoring is a triage/prioritisation input of exactly the claim-gate craft this lane owns; F19
   extends the ladder the lane already holds (F01 CVSS v4 severity → F18 CISA KEV exploitation
   status → F19 EPSS exploitation likelihood).
3. **Prior occupancy of the same standards body.** kasegi's `corpus/SOURCES.md` cites
   `www.first.org` in 3 rows (re-verified): S001 `:7` (FIRST CVSS v4.0 User Guide), S002 `:8`
   (FIRST CVSS v4.0 Specification Document), S018 `:24` (FIRST multi-party coordination
   guidelines v1.1) — mined since rounds 22–24. S053's host is therefore not new to the lane; only
   its `/epss/` path is.

Consequence, stated without smoothing: the 187-host census was computed from the lanes' round 1–2
`CHANNELS.md` and **predates kasegi's first.org mining** — the doctrine host table is stale for
kasegi (26 assigned one-off hosts, `first.org` among none of them). A doctrine channel row for
`first.org` is owed to the shokuknow campaign. That is a **report-only doctrine-state observation**:
shokuknow is read-only to this lane, no doctrine row was or could be written this round, and the
absence of a row does not weaken F19's standing because assignment here operates at the domain
level, where nothing contests it.

## Q3 — PROVINCE adjacency handling (report, don't absorb)

- `PROVINCE.md:25` — "**Refuses:** anything outside this domain; report cross-domain evidence back
  to the orchestrator rather than absorbing it."
- `PROVINCE.md:43-45` — "## Adjacent — Sibling lanes are reported, not absorbed" (chousa, kagi,
  kake, kengaku named).
- `PROTOCOL.md:457-461` — contested scope is **reported in the lane report**; the integrator
  arbitrates by refining `PROVINCE.md` and records the ruling in the round notes; a report left
  unruled by the next completed round is re-flagged; "silence is not a ruling and must never
  default scope to whichever lane wrote first."

Application this round: every sibling hit in Q1's table is **reported** in this ruling, none is
absorbed into kasegi's corpus (the F19 entry grounds solely on kasegi's own S053 capture), and the
one genuine EPSS text in scope is campaign-side and is recorded, not cited.

## Caveats consolidated for the lesson and the entry scribe

- **A (phrasing).** kasegi's round-24 CVSS snapshots (`corpus/source-snapshots/round-24/S001.txt`,
  `S002.txt`) already carry the FIRST site-nav block naming EPSS (lines 153/155/156/159/208). The
  novelty claim must read "**first EPSS ground**", never "EPSS was absent from the lane".
- **B (source discipline).** The CSS2024 programme abstract (Q1) corroborates adjacency framing
  only; do not cite it and do not treat it as doctrine assignment.
- **C (method correction to the scout).** `ScoutF19Sibling.md` records "whole shokuknow … **0
  hits**" for `\bEPSS\b`; the sweep reproduced that the boundary is the failure mode — 「EPSSなど」
  has EPSS followed by the word character な, so `\bEPSS\b` cannot match. Strict anchors against
  Japanese sources must use `(?<![A-Za-z])EPSS(?![A-Za-z])` or go boundary-free. For the sibling
  ruling this changes nothing (the sibling-lane boundary-free sweep finds only ASCII noise), but
  the correction stands for any future CJK-in-scope sweep.

## Final ruling text for the lesson (splice-ready)

> ### Contested scope — none, ruled rather than left silent (F19/S053)
>
> `wave1/ConnSibling.md` consolidates `wave1/ScoutF19Sibling.md` and `wave1/ExecSiblingSweep.md`
> and rules on every EPSS-ground token in the sibling lanes under `PROTOCOL.md:457-461` and kasegi's
> `PROVINCE.md` Adjacent ("Sibling lanes are reported, not absorbed"):
>
> - **All 20 sibling lanes hold zero EPSS ground.** Three independent formulations (the scout's
>   case-sensitive word-bounded sweep, the sweep's hidden-inclusive `\bEPSS\b` decisive test over
>   127 near-match files, and this seat's case-insensitive re-run) return zero sibling files; every
>   near-match resolves to a classified non-ground class: `epssweep` Godot test identifiers
>   (game-dev-2d, 97 files), the `LeinenEPSSJ24` author-surname DBLP key (tameshi), encoded-substring
>   fixture noise (mado/kake/kotoba/kotodama/kaidoku), generic `exploitation` boilerplate and
>   unrelated-sense abstracts, and generic `percentile` statistics vocabulary (20 files;
>   `probability of exploit` → 0 files). No sibling `SKILL.md` mentions `vulnerabilit*` at all —
>   kasegi is the fleet's only vulnerability-domain lane.
> - **Adjacent, not contesting:** kagi's retained NVD API probes carry CISA-ADP **SSVC** fields
>   (`"exploitation":"none"`, `"automatable":"no"`) — a different framework from EPSS, retained as
>   probes, never registered as rows; mori's CVSS mentions are raw advisory fetch blobs; the only
>   genuine EPSS sentence in scope is a CSS2024 conference-programme abstract in the read-only
>   shokuknow campaign (Japanese; names EPSS among SSVC/KEV prioritisation inputs; no method or
>   data) — recorded, not cited. `S053`/`F19` ids in kake/tabi/tameshi and the game-dev lanes are
>   lane-local and raise no fleet collision.
> - **Doctrine assignment, stated precisely:** unlike F18 (whose host is doctrine-ratified at
>   `shokuknow/doctrine/channel-recurrence.md:62`, `cisa.gov → kasegi`), **no doctrine host row
>   assigns first.org to any lane**; the 187-host census predates kasegi's first.org mining. F19's
>   host is assigned to this lane at the domain level — `PROTOCOL.md:457` one-domain doctrine,
>   `PROVINCE.md:30` triage-and-claim-gates core — and by prior occupancy of the same standards
>   body (S001/S002/S018, first.org since rounds 22–24). A doctrine channel row for first.org is
>   owed to the shokuknow campaign (report-only; campaign is read-only to this lane).
> - **Ruling:** F19/S053 is uncontested; no report-to-lane item arises and no `PROVINCE.md`
>   refinement is required by adjacency. (The standing Frontier-amendment bookkeeping tracked by
>   SHONEN/considerthese — proposal 5 landed the owed F18 amendment — is Frontier accounting, not
>   an adjacency requirement.) Entry phrasing per caveat A: "first EPSS ground", never "EPSS absent
>   from the lane".

## Housekeeping

- Writes: this receipt only. No lane/fleet/shokuknow file edited; no doctrine row written; no
  git/jj mutation (read-only `log`/`status`/`grep` only); no tool installed (none needed —
  pacman pause respected); no subagents dispatched; no `agent://all`.
- Ruling-draft path messaged to `ScribeGateLesson` (lesson Gate owner) for splice.
- Scratch `/fast/scratch/hyaku/kasegi-r36/ConnSibling/` (created at seat start, held no fixtures —
  all work was read-only greps) removed before yield; verified empty at exit.

Report: .ufo/waves/round-36/wave1/ConnSibling.md
