# Intake surface — bounty-map census, ingestion pipeline, registry decree ledger

All numbers verified live 2026-09-28 by census over
`[lost-tree] ~/Projects/bounties/bounty-map/programs/*.json` (1088 records, 0 parse
failures), `ops/` source reads, and `node ops/check-freshness.mjs` (exit 1).

## Two intake paths, and the second never writes the map

| Path | Producer | Writes | Consumers |
|---|---|---|---|
| Board import | `ops/import-board.mjs --from <board>` (evidence-bound: dataset sha256 + count + `refresh_run_id` vs `refresh_evidence.json`) | `bounty-map/programs/*.json` — new records land `{lane:"executor", mission_state:"DISCOVERED", ev_inputs:{}}`; past-DISCOVERED files are byte-protected | `fleet-dispatch.mjs::buildQueue`, `~/Projects/the-bounty-hunter/ops/ev-report.mjs`, `~/Projects/the-bounty-hunter/ops/rank.mjs`, `~/Projects/the-bounty-hunter/ops/validate.mjs` |
| Ingestion cycle | `.ufo-ingestion/cycle-20260914T171257Z.md` (run `ing4e0158f74cf3`, 16 scouts, grok 403 spending-limit → rerouted `devin/swe-2:max` via `.omp/agents/ing-scout.md`) | `claims/<slug>/ingestion-20260914/` directly — INGESTION.md + claim.json (`stage:"ingestion-seeded"`) | `~/Projects/the-bounty-hunter/ops/claim-index.mjs` queue only |

**The ingestion cycle wrote no map records itself.** 22 claim dirs have
no program record (round-13 correction: the seeding did NOT make all 13
seeded programs map-less — 9 of 13 already had map records: crypto,
auth0-okta, superhuman, amazonvrp, x, wellsfargo-bbp, hyatt, ui, bcny).
Composition, live census round-13: 4 seeded (spacex-starlink, monzo,
personio, yahoo — 7 of the 12 queue rows came from this cycle) + 18
archive-era
dirs (cantina-dydx/euler/morpho/pendle/reserve-protocol/uniswap,
immunefi-1inch-SmartContracts/moneyonchain, sherlock-aave-v4, discord, dji,
riot, adobe, brave, **hackerone-zabbix** — omitted from earlier lists,
nvidia-public, intigriti-c1a89c7e, github-bounty). The ranked table in
`cycle-*.md` (EV-scored, 13 SEEDED / 1 REJECTED / 18 DEFERRED) is the real
curated ranking — richer than anything `~/Projects/the-bounty-hunter/ops/rank.mjs` produces off the map.
~80 more programs are queued for next-cycle evaluation inside the cycle file's
scan queue; that cycle never ran (tracker log's last line is
2026-09-14T17:24:52Z; 20:40:15Z is the `.md` snapshot cycle stamp —
round-12 correction).

## Program-record census (1088, all from one import)

`refresh_run_id` is identical on all 1088 records:
`refresh-20260829T190850329Z` — a single board import; nothing since.

- `mission_state`: DISCOVERED ×1087, PLANNED ×1 (`github-bug-bounty`).
  **The field is write-only drift.** `~/Projects/the-bounty-hunter/ops/import-board.mjs` never advances it;
  `fleet-dispatch.mjs::programState()` (line 74) reads it only for the
  `--dry` log line (line 177). Real mission progress lives in
  `ledger/missions.jsonl`; real dispatch termination is
  `fleets/run/<id>.status.json` TERMINAL (`DONE/PARKED/FAILED/RETIRED`) +
  `attempts()≥2` counted from telemetry park/fail events. 10 of the 12
  schema enum values are never populated. One real writer exists —
  `[lost-base] ~/Projects/the-bounty-hunter/ops/rank.mjs:202-203` bumps DISCOVERED→RANKED — but no RANKED record exists.
  Round-13 correction: "it never ran post-refresh" was an unbounded negative —
  `--write-queue` ran ≥2× on 2026-09-04 (2 `RANKED` lines in
  `ledger/missions.jsonl` in rank.mjs's exact hardcoded append shape incl.
  producer/model/basis/artifact_sha256; one sha matches the still-present
  `ledger/rankings-2026-09-04.json`). Defensible claim: the bump never
  PERSISTED to a program file — the sole curated candidate was already
  PLANNED (`heldByState`, rank.mjs:199-201) and default-basis positives were
  held by the S3 consistency gate. As of 2026-09-28: 1087 DISCOVERED /
  1 PLANNED / 0 RANKED.
- `lane`: `executor` ×1088 — decorative; routing lives in
  `fleets/registry.json` lane definitions, not per-program.
- `ev_inputs`: exactly **1** non-empty record (`github-bug-bounty`, curated
  M2 values, `sources.note` cites missions.jsonl mission-0). Consequence:
  `~/Projects/the-bounty-hunter/ops/ev-report.mjs` prints `UNKNOWN` for 1087/1088 programs and `~/Projects/the-bounty-hunter/ops/rank.mjs`'s
  `inputs_basis:"curated"` consistency gate passes on a population of one.
- `reward`: 48 records, **all `source_kind=independent`** — the platform
  (767) and web3 (273) datasets carry no reward fields at all. medians:
  min $500, max $100k; `currency` absent on 20.
- `freshness.label`: `live` 258 / `stale_snapshot` 830. All 258 "live"
  records carry the identical `as_of` = the refresh-run timestamp, so the
  label describes the dataset, not per-program recency. Live check
  2026-09-28: all three datasets 358.2 h stale vs the 26 h threshold —
  `~/Projects/the-bounty-hunter/ops/check-freshness.mjs` exits 1 (honest alarm AR4, currently firing).
- `source_kind`: platform 767 / web3 273 / independent 48, in 1:1 lockstep
  with `board_ref.dataset`.
- Coverage: 586/592 `evidence/` dirs have map records; 252/274 `claims/`
  dirs have map records; **352 map programs were never touched** (no
  evidence dir, no claims dir — platform 239 / web3 95 / independent 18).
- Name-drift pairs where map id ≠ claims/evidence dir name for the same
  program: `bugcrowd-spacex` (map) vs `bugcrowd-spacex-starlink` (claims),
  `github-bug-bounty` (map — the single curated record) vs `github-bounty`
  (claims+evidence), plus all the ingestion slugs. Duplicate-detection and
  any join on program id silently misses these.

## What the dispatcher actually ranks on (`buildQueue`, fleet-dispatch.mjs:88)

```
score = priority_hit(9e12) + continue_verdict(2e12) + curated_ev(1e12)
      + reward.min×1000 + is_live(1)
```

With `priority.json` = 14 programs (a strict subset of the 50
continue-verdict programs — the 9e12 tier only breaks ties inside the
continue cohort), `curated` = 1, `reward` object on 48 but numeric
`reward.min` on only 14 (round-13 correction; one of the 14 is also a
continue hit, so the reward band counts 13): for exactly **1024** records
(796 zero + 228 live-only; round-13 census — earlier "~1040" was derived
from the reward-exists≠reward.min-numeric conflation) the score is 0 or 1
and order
degenerates to readdir order. The 1088-record map contributes almost nothing
to queue order — intake effort paid off only through the separate
`.ufo-ingestion` ranking and `priority.json`/`review-verdicts.jsonl`.
`buildQueue` iterates the map, so ingestion-seeded programs (no map record)
can never be dispatched as new hunts — they enter only through `claims/`
commits.

## `.ufo-ingestion/claim-tracker.py` — a third, weaker claimable definition

Read-only continuous scanner (mission `trk263db49c589`, "~5 min refresh")
watching BOTH `claims/` AND
`~/Projects/origin-work/open-bug-bounties/claim-packages/` — the third
consumer of the sibling tree no ops tool reads (see
`corpus/knowledge/submitted-registry.md`). Its claimable rule is `READY.md` present AND no
`BLOCKED.md` beneath/above — a weaker, earlier standard than
`~/Projects/the-bounty-hunter/ops/claim-check.mjs`; **all 24** of its "claimable" hits are origin-tree packages
($13,733 tracked `expected_usd`, most flagged "claim.json
absent/unparseable"). Outputs: `claim-ready-tracker.{md,json,log}` +
`claim-ready-ledger.json` (first_seen/last_seen per package). The tracker is
**dead**: last cycle stamp 2026-09-14T20:40Z (log's last line 17:24:52Z), silent since; its "continuous"
badge lies. If revived, its origin-tree hits still need the hard gate before
they're queue-worthy.

## `fleets/registry.json` — in-domain; it is the decree ledger, not just routing

Gap resolved (README listed it "possibly cross-domain"): the file is
fleet-owned (`SYNC_PATHS` includes it) and its `operator_decrees` block is
the authoritative store for bounty-domain operator decrees — the *reasons*
behind package dispositions that claim files only gesture at:

- `disclosure_classes_2026_09_05` — paid track = operator submits personally
  under H1 `vgpnk1337` / Intigriti `veigapunk` (attributable, payout rails
  first); freebie class = VDP-only. Guardrail: never mix classes; one past
  misroute happened via mass-bucket submission.
- `freebie_class_attribution_2026_09_06` — **supersedes the anonymity
  clause**: freebie class is ATTRIBUTED (name + email, no payout). Anthropic
  first — this is why `vdp-disclosures/anthropic-*/` ships attributed.
- `claim_queue_2026_09_05` — filing order mozilla → spotify → airtable →
  intel. **3cx: NEVER submitted to their program** — retained for free
  disclosure once operator rep allows publishing without platform-lockout
  risk. Wordpress shelved. Anthropic = freebie VDP. This decree explains the
  queue/history anomalies rounds 9–10 flagged (3cx DONE-but-never-filed is
  decree, not oversight).
- `severity_evidence_trail_2026_09_05` — every package documents severity
  estimate + rationale BEFORE submission; independent model estimate where
  available; never submit an undefendable severity. Origin: a past 9.0+
  finding was VDP-dismissed as nothing.
- `intel_hold_2026_09_06` — no Intigriti ID verification → held (matches the
  live `submit/BLOCKED-2026-09-11.md` on the intel package).
- Routing machinery (for `ops/validate.mjs`/`~/Projects/the-bounty-hunter/ops/registry-check.mjs` context):
  `k3_seats` = judge+planner, `reroute_rules` I3/I6/I7, `omp_seat`, bucket
  fallbacks, `dual_method_schedule` (UTC-3 12–22 → Chinese stack, else
  astra-class), `token_plan_limit_contingency` → grok-only lane.
- Stale-vs-live entries: `model_doctrine.banned_for_routing` still lists
  `gpt-6-astra (guardrails)` while `codex_class_pin` (2026-09-06) routes
  codex-class TO `gpt-6-astra:max` and `catalog_notes` marks astra "LIVE and
  ROUTED" — the doctrine ban is superseded in place, not edited out.
  Bucket annotations "(parked until 2026-09-07)" are stale vs
  `shared.mjs PARKED=[]`. Treat per-key `superseded` markers and decree
  dates as the version control — the file accretes, it does not revise.

## Operational takeaways

1. **Never trust `mission_state`/`lane`/`ev_inputs` in the map.** Real
   state = `ledger/missions.jsonl` + `fleets/run/`; real ranking =
   `priority.json` + continue-verdicts + `.ufo-ingestion/rankings.md`.
2. **Join on program id is lossy.** Map↔claims name-drift (spacex,
   github-bounty, all 13 ingestion slugs) means "does X have a map record"
   needs a name-normalization table, not an id lookup.
3. **The map is 30 days stale and alarmed.** `check-freshness` exit 1 is
   the standing state until the next `refresh-*` import; all `live` labels
   predate it.
4. **Ingestion cycle 2 never ran.** The deferred/queued list (~80 programs,
   incl. PortSwigger, AT&T, Capital One) sits in
   `.ufo-ingestion/cycle-20260914T171257Z.md` — the highest-value unworked
   frontier is enumerated, not hidden.
5. **Registry decrees answer "why" questions claim files can't.** Before
   re-deriving a disposition (3cx non-filing, intel hold, anthropic VDP
   attribution), check `operator_decrees` first.

## Provenance (round-22 correction, appended)

source: [lost-tree] ~/Projects/bounties/bounty-map/programs/*.json census (1088 records), ops/ source reads, and check-freshness run.
verified-at: 2026-09-28
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true
